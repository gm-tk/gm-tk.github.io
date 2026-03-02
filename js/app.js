/**
 * App — UI controller for ParseMaster.
 *
 * Manages file upload (drag-and-drop + click-to-browse), progress
 * display, output rendering, clipboard copy, and file download.
 */

'use strict';

class App {
    constructor() {
        this.parser = new DocxParser();
        this.formatter = new OutputFormatter();
        this.tagNormaliser = new TagNormaliser();
        this.pageBoundary = new PageBoundary(this.tagNormaliser);
        this.templateEngine = new TemplateEngine();
        this.htmlConverter = new HtmlConverter(this.tagNormaliser, this.templateEngine);

        /** Cached formatted output after a successful parse */
        this.currentOutput = null;

        /** Cached metadata for display */
        this.currentMetadata = null;

        /** Cached tag/page analysis for debug panel */
        this.currentAnalysis = null;

        /** Currently selected template ID */
        this.selectedTemplateId = null;

        /** Generated HTML files keyed by filename */
        this.generatedHtmlFiles = {};

        /** Ordered list of generated filenames */
        this.generatedFileList = [];

        /** Currently selected HTML file index for display */
        this.currentHtmlFileIndex = 0;

        /** Output mode: 'html' or 'text' */
        this.outputMode = 'html';

        this._bindElements();
        this._bindEvents();
        this._initTemplateEngine();
    }

    // ------------------------------------------------------------------
    // DOM references
    // ------------------------------------------------------------------

    _bindElements() {
        this.dropZone = document.getElementById('drop-zone');
        this.fileInput = document.getElementById('file-input');
        this.uploadSection = document.getElementById('upload-section');
        this.processingSection = document.getElementById('processing-section');
        this.resultsSection = document.getElementById('results-section');
        this.progressStatus = document.getElementById('progress-status');
        this.progressSteps = document.getElementById('progress-steps');
        this.metadataPanel = document.getElementById('metadata-panel');
        this.statsPanel = document.getElementById('stats-panel');
        this.outputArea = document.getElementById('output-area');
        this.btnCopyAll = document.getElementById('btn-copy-all');
        this.btnCopyContent = document.getElementById('btn-copy-content');
        this.btnDownload = document.getElementById('btn-download');
        this.btnReset = document.getElementById('btn-reset');
        this.errorPanel = document.getElementById('error-panel');
        this.errorMessage = document.getElementById('error-message');
        this.toast = document.getElementById('toast');
        this.debugPanel = document.getElementById('debug-panel');
        this.debugContent = document.getElementById('debug-content');
        this.debugToggle = document.getElementById('debug-toggle');
        this.templateDropdown = document.getElementById('template-dropdown');
        this.templateAutoLabel = document.getElementById('template-auto-label');
        this.outputModeToggle = document.getElementById('output-mode-toggle');
        this.htmlFileSelector = document.getElementById('html-file-selector');
        this.htmlFileDropdown = document.getElementById('html-file-dropdown');
    }

    // ------------------------------------------------------------------
    // Event binding
    // ------------------------------------------------------------------

    _bindEvents() {
        const self = this;

        // Drag-and-drop
        this.dropZone.addEventListener('dragover', function (e) {
            e.preventDefault();
            e.stopPropagation();
            self.dropZone.classList.add('drag-over');
        });

        this.dropZone.addEventListener('dragleave', function (e) {
            e.preventDefault();
            e.stopPropagation();
            self.dropZone.classList.remove('drag-over');
        });

        this.dropZone.addEventListener('drop', function (e) {
            e.preventDefault();
            e.stopPropagation();
            self.dropZone.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                self.handleFile(files[0]);
            }
        });

        // Click-to-browse
        this.dropZone.addEventListener('click', function () {
            self.fileInput.click();
        });

        // Keyboard: Enter/Space to trigger file picker
        this.dropZone.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                self.fileInput.click();
            }
        });

        this.fileInput.addEventListener('change', function () {
            if (self.fileInput.files.length > 0) {
                self.handleFile(self.fileInput.files[0]);
            }
        });

        // Action buttons
        this.btnCopyAll.addEventListener('click', function () {
            if (self.outputMode === 'html' && self.generatedFileList.length > 0) {
                var filename = self.generatedFileList[self.currentHtmlFileIndex];
                var htmlContent = self.generatedHtmlFiles[filename] || '';
                self.copyToClipboard(htmlContent, 'HTML source copied to clipboard');
            } else if (self.currentOutput) {
                self.copyToClipboard(self.currentOutput.full, 'Full output copied to clipboard');
            }
        });

        this.btnCopyContent.addEventListener('click', function () {
            if (self.outputMode === 'html' && self.generatedFileList.length > 0) {
                var filename = self.generatedFileList[self.currentHtmlFileIndex];
                var htmlContent = self.generatedHtmlFiles[filename] || '';
                self.copyToClipboard(htmlContent, 'HTML source copied to clipboard');
            } else if (self.currentOutput) {
                self.copyToClipboard(self.currentOutput.contentOnly, 'Content copied to clipboard (without metadata)');
            }
        });

        this.btnDownload.addEventListener('click', function () {
            if (self.outputMode === 'html' && self.generatedFileList.length > 0) {
                var filename = self.generatedFileList[self.currentHtmlFileIndex];
                var htmlContent = self.generatedHtmlFiles[filename] || '';
                self._downloadAsFile(htmlContent, filename, 'text/html;charset=utf-8');
            } else if (self.currentOutput) {
                const code = self.currentMetadata && self.currentMetadata.moduleCode
                    ? self.currentMetadata.moduleCode
                    : 'ParseMaster_output';
                self.downloadAsTxt(self.currentOutput.full, code + '_parsed.txt');
            }
        });

        this.btnReset.addEventListener('click', function () {
            self.reset();
        });

        // Template dropdown
        this.templateDropdown.addEventListener('change', function () {
            self.selectedTemplateId = self.templateDropdown.value;
            // Hide auto-detected label when user manually changes
            self.templateAutoLabel.classList.add('hidden');
        });

        // Output mode toggle
        if (this.outputModeToggle) {
            this.outputModeToggle.addEventListener('click', function () {
                self._toggleOutputMode();
            });
        }

        // HTML file selector dropdown
        if (this.htmlFileDropdown) {
            this.htmlFileDropdown.addEventListener('change', function () {
                self.currentHtmlFileIndex = parseInt(self.htmlFileDropdown.value, 10);
                self._displayCurrentHtmlFile();
            });
        }
    }

    // ------------------------------------------------------------------
    // Template engine initialisation
    // ------------------------------------------------------------------

    /**
     * Load template configurations and populate the dropdown.
     */
    async _initTemplateEngine() {
        try {
            await this.templateEngine.loadTemplates();
            var list = this.templateEngine.getTemplateList();
            for (var i = 0; i < list.length; i++) {
                var option = document.createElement('option');
                option.value = list[i].id;
                option.textContent = list[i].name;
                this.templateDropdown.appendChild(option);
            }
        } catch (err) {
            console.error('TemplateEngine initialisation failed:', err);
        }
    }

    /**
     * Auto-detect template from module code and update the dropdown.
     *
     * @param {string|null} moduleCode
     */
    _autoDetectTemplate(moduleCode) {
        var detected = this.templateEngine.detectTemplate(moduleCode);
        if (detected) {
            this.templateDropdown.value = detected;
            this.selectedTemplateId = detected;
            this.templateAutoLabel.classList.remove('hidden');
        }
    }

    // ------------------------------------------------------------------
    // File handling
    // ------------------------------------------------------------------

    async handleFile(file) {
        // Validate file type
        if (!file.name.toLowerCase().endsWith('.docx')) {
            this.showError(
                'Please upload a .docx file. Other formats (PDF, .doc, .txt) are not supported.'
            );
            return;
        }

        // Large file warning
        if (file.size > 20 * 1024 * 1024) {
            this._addProgressStep('⚠ Large file detected (' +
                Math.round(file.size / 1024 / 1024) + ' MB). This may take a moment.');
        }

        this.hideError();
        this.showProcessing();

        const self = this;

        // Wire up progress callback
        this.parser.onProgress = function (msg) {
            self._addProgressStep(msg);
        };

        try {
            const result = await this.parser.parse(file);
            const output = this.formatter.formatAll(result);

            self.currentOutput = output;
            self.currentMetadata = result.metadata;

            // Auto-detect template from module code
            self._autoDetectTemplate(result.metadata.moduleCode);

            // Run tag normalisation and page boundary analysis
            self._addProgressStep('Normalising tags...');
            var analysis = self._runAnalysis(result);
            self.currentAnalysis = analysis;
            self._addProgressStep('Detecting page boundaries...');
            self._addProgressStep('Tag analysis complete: ' +
                analysis.totalTags + ' tags found, ' +
                analysis.pages.length + ' pages detected');

            // Run HTML conversion if a template is selected
            self._addProgressStep('Loading template configuration...');
            self._runHtmlConversion(analysis, result);

            self.showResults(result, output);
        } catch (err) {
            self.hideProcessing();

            if (err.message === 'MISSING_DOCUMENT_XML') {
                self.showError(
                    'This .docx file doesn\'t contain the expected document structure (word/document.xml missing).'
                );
            } else if (err.message === 'INVALID_XML') {
                self.showError(
                    'The document XML could not be parsed. The file may be corrupted.'
                );
            } else if (err.message === 'MISSING_BODY') {
                self.showError(
                    'This .docx file doesn\'t contain a document body element.'
                );
            } else if (err.message && err.message.indexOf('not a valid zip') !== -1) {
                self.showError(
                    'This file appears to be corrupted or is not a valid .docx file.'
                );
            } else if (err.message && err.message.indexOf('End of central directory') !== -1) {
                self.showError(
                    'This file appears to be corrupted or is not a valid .docx file.'
                );
            } else {
                self.showError(
                    'An unexpected error occurred while processing the file: ' + err.message
                );
            }

            console.error('ParseMaster error:', err);
        }
    }

    // ------------------------------------------------------------------
    // UI state management
    // ------------------------------------------------------------------

    showProcessing() {
        this.uploadSection.classList.add('hidden');
        this.resultsSection.classList.add('hidden');
        this.processingSection.classList.remove('hidden');
        this.progressSteps.innerHTML = '';
    }

    hideProcessing() {
        this.processingSection.classList.add('hidden');
    }

    showResults(result, output) {
        this.processingSection.classList.add('hidden');
        this.resultsSection.classList.remove('hidden');

        // Populate metadata panel
        this._renderMetadata(result.metadata);

        // Populate stats panel
        this._renderStats(result.stats, result.contentStartFound);

        // Show output based on current mode
        if (this.generatedFileList.length > 0) {
            this.outputMode = 'html';
            this._populateHtmlFileDropdown();
            this._displayCurrentHtmlFile();
            this._updateOutputModeUI();
        } else {
            this.outputMode = 'text';
            this.outputArea.value = output.full;
            this._updateOutputModeUI();
        }

        // Check if content is empty
        if (!output.contentOnly || output.contentOnly.trim() === '--- CONTENT START ---') {
            this.showError('This document appears to be empty or contains no text content.');
        }

        // Render debug panel
        if (this.currentAnalysis) {
            this._renderDebugPanel(this.currentAnalysis);
        }

        // Announce to screen readers
        var announceMsg = 'Document processed successfully. ' +
            result.stats.totalParagraphs + ' paragraphs extracted.';
        if (this.generatedFileList.length > 0) {
            announceMsg += ' Generated ' + this.generatedFileList.length + ' HTML files.';
        }
        this._announce(announceMsg);
    }

    reset() {
        this.currentOutput = null;
        this.currentMetadata = null;
        this.currentAnalysis = null;
        this.selectedTemplateId = null;
        this.generatedHtmlFiles = {};
        this.generatedFileList = [];
        this.currentHtmlFileIndex = 0;
        this.outputMode = 'html';
        this.resultsSection.classList.add('hidden');
        this.processingSection.classList.add('hidden');
        this.uploadSection.classList.remove('hidden');
        this.hideError();
        this.fileInput.value = '';
        if (this.debugPanel) {
            this.debugPanel.classList.add('hidden');
        }
        // Reset template dropdown
        this.templateDropdown.selectedIndex = 0;
        this.templateAutoLabel.classList.add('hidden');
        // Reset HTML file dropdown
        if (this.htmlFileDropdown) {
            this.htmlFileDropdown.innerHTML = '';
        }
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorPanel.classList.remove('hidden');
        this.uploadSection.classList.remove('hidden');
        this._announce('Error: ' + message);
    }

    hideError() {
        this.errorPanel.classList.add('hidden');
    }

    // ------------------------------------------------------------------
    // Progress steps
    // ------------------------------------------------------------------

    _addProgressStep(message) {
        const step = document.createElement('div');
        step.className = 'progress-step';

        // Check mark for completed steps (all but the last are "done")
        step.textContent = message;

        this.progressSteps.appendChild(step);
        this.progressStatus.textContent = message;

        // Scroll to bottom
        this.progressSteps.scrollTop = this.progressSteps.scrollHeight;
    }

    // ------------------------------------------------------------------
    // Metadata rendering
    // ------------------------------------------------------------------

    _renderMetadata(metadata) {
        const items = [];

        if (metadata.moduleCode) {
            items.push({ label: 'Module Code', value: metadata.moduleCode });
        }
        if (metadata.subject) {
            items.push({ label: 'Subject', value: metadata.subject });
        }
        if (metadata.course) {
            items.push({ label: 'Course', value: metadata.course });
        }
        if (metadata.writer) {
            items.push({ label: 'Writer', value: metadata.writer });
        }
        if (metadata.date) {
            items.push({ label: 'Date', value: metadata.date });
        }

        // Add selected template
        if (this.selectedTemplateId) {
            try {
                var config = this.templateEngine.getConfig(this.selectedTemplateId);
                items.push({ label: 'Template', value: config._templateName });
            } catch (e) {
                // Ignore — template may not be loaded yet
            }
        }

        if (items.length === 0) {
            this.metadataPanel.innerHTML =
                '<span class="metadata-empty">No metadata detected in document boilerplate</span>';
            return;
        }

        let html = '';
        for (let i = 0; i < items.length; i++) {
            html += '<div class="metadata-item">' +
                '<span class="metadata-label">' + this._esc(items[i].label) + ':</span> ' +
                '<span class="metadata-value">' + this._esc(items[i].value) + '</span>' +
                '</div>';
        }
        this.metadataPanel.innerHTML = html;
    }

    // ------------------------------------------------------------------
    // Stats rendering
    // ------------------------------------------------------------------

    _renderStats(stats, contentStartFound) {
        const items = [
            { label: 'Paragraphs', value: stats.totalParagraphs },
            { label: 'Tables', value: stats.totalTables },
            { label: 'Hyperlinks', value: stats.totalHyperlinks },
            { label: 'Deletions removed', value: stats.deletionsRemoved },
            { label: 'Insertions kept', value: stats.insertionsKept },
            { label: 'SDT wrappers unwrapped', value: stats.sdtUnwrapped },
            { label: 'Red text segments', value: stats.redTextSegments },
            {
                label: 'Content start',
                value: contentStartFound
                    ? 'Block #' + stats.contentStartParagraph
                    : 'Not found (showing all)'
            }
        ];

        let html = '';
        for (let i = 0; i < items.length; i++) {
            html += '<div class="stat-item">' +
                '<span class="stat-value">' + this._esc(String(items[i].value)) + '</span>' +
                '<span class="stat-label">' + this._esc(items[i].label) + '</span>' +
                '</div>';
        }
        this.statsPanel.innerHTML = html;
    }

    // ------------------------------------------------------------------
    // Clipboard
    // ------------------------------------------------------------------

    async copyToClipboard(text, successMsg) {
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(text);
                this.showToast(successMsg || 'Copied to clipboard');
            } else {
                // Fallback for older browsers
                this._fallbackCopy(text);
                this.showToast(successMsg || 'Copied to clipboard');
            }
        } catch (err) {
            // Fallback
            try {
                this._fallbackCopy(text);
                this.showToast(successMsg || 'Copied to clipboard');
            } catch (e) {
                this.showToast('Failed to copy. Please select and copy manually.');
            }
        }
    }

    _fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        textarea.style.top = '-9999px';
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }

    // ------------------------------------------------------------------
    // Download
    // ------------------------------------------------------------------

    downloadAsTxt(text, filename) {
        const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        this.showToast('Downloaded ' + filename);
    }

    // ------------------------------------------------------------------
    // Toast notification
    // ------------------------------------------------------------------

    showToast(message) {
        this.toast.textContent = message;
        this.toast.classList.add('visible');

        var self = this;
        clearTimeout(this._toastTimer);
        this._toastTimer = setTimeout(function () {
            self.toast.classList.remove('visible');
        }, 3000);
    }

    // ------------------------------------------------------------------
    // Accessibility helpers
    // ------------------------------------------------------------------

    _announce(message) {
        var announcer = document.getElementById('sr-announcer');
        if (announcer) {
            announcer.textContent = message;
        }
    }

    // ------------------------------------------------------------------
    // Tag & Page Analysis
    // ------------------------------------------------------------------

    /**
     * Run tag normalisation and page boundary analysis on parsed content.
     *
     * @param {Object} parserResult - Result from DocxParser.parse()
     * @returns {Object} Analysis results for debug display
     */
    _runAnalysis(parserResult) {
        var contentBlocks = parserResult.content;
        var startIndex = parserResult.contentStartIndex;
        var moduleCode = (parserResult.metadata && parserResult.metadata.moduleCode) || 'MODULE';

        // Process all content blocks from content start onwards
        var allTags = [];
        var unrecognisedTags = [];
        var redTextInstructions = [];
        var redTextOnlyCount = 0;
        var whitespaceOnlyCount = 0;
        var tagsByCategory = {};

        for (var i = startIndex; i < contentBlocks.length; i++) {
            var block = contentBlocks[i];
            var blockText = this._getBlockTextForAnalysis(block);
            var processed = this.tagNormaliser.processBlock(blockText);

            if (processed.isRedTextOnly) {
                redTextOnlyCount++;
            }
            if (processed.isWhitespaceOnly) {
                whitespaceOnlyCount++;
            }

            for (var t = 0; t < processed.tags.length; t++) {
                var tag = processed.tags[t];
                allTags.push({
                    raw: tag.raw,
                    normalised: tag.normalised,
                    category: tag.category,
                    level: tag.level,
                    number: tag.number,
                    id: tag.id,
                    modifier: tag.modifier,
                    blockIndex: i
                });

                if (!tag.normalised) {
                    unrecognisedTags.push({
                        raw: tag.raw,
                        blockIndex: i
                    });
                }

                // Count by category
                var cat = tag.category || 'unknown';
                if (!tagsByCategory[cat]) {
                    tagsByCategory[cat] = 0;
                }
                tagsByCategory[cat]++;
            }

            for (var r = 0; r < processed.redTextInstructions.length; r++) {
                redTextInstructions.push({
                    text: processed.redTextInstructions[r],
                    blockIndex: i
                });
            }
        }

        // Run page boundary detection
        var contentFromStart = contentBlocks.slice(startIndex);
        var pages = this.pageBoundary.assignPages(contentFromStart, moduleCode);

        return {
            totalTags: allTags.length,
            tags: allTags,
            unrecognisedTags: unrecognisedTags,
            redTextInstructions: redTextInstructions,
            redTextOnlyCount: redTextOnlyCount,
            whitespaceOnlyCount: whitespaceOnlyCount,
            tagsByCategory: tagsByCategory,
            pages: pages
        };
    }

    /**
     * Get text from a content block for analysis (mirrors page boundary logic).
     *
     * @param {Object} block - A content block {type, data}
     * @returns {string} Text content
     */
    _getBlockTextForAnalysis(block) {
        if (block.type === 'paragraph' && block.data) {
            var runs = block.data.runs || [];
            var text = '';
            for (var i = 0; i < runs.length; i++) {
                var run = runs[i];
                if (!run.text) continue;
                var chunk = run.text;
                var fmt = run.formatting || {};
                if (fmt.isRed) {
                    chunk = '\uD83D\uDD34[RED TEXT] ' + chunk + ' [/RED TEXT]\uD83D\uDD34';
                }
                text += chunk;
            }
            return text;
        }
        if (block.type === 'table' && block.data) {
            var texts = [];
            var rows = block.data.rows || [];
            for (var r = 0; r < rows.length; r++) {
                var cells = rows[r].cells || [];
                for (var c = 0; c < cells.length; c++) {
                    var paras = cells[c].paragraphs || [];
                    for (var p = 0; p < paras.length; p++) {
                        var paraRuns = paras[p].runs || [];
                        var paraText = '';
                        for (var ri = 0; ri < paraRuns.length; ri++) {
                            if (!paraRuns[ri].text) continue;
                            var ch = paraRuns[ri].text;
                            var f = paraRuns[ri].formatting || {};
                            if (f.isRed) {
                                ch = '\uD83D\uDD34[RED TEXT] ' + ch + ' [/RED TEXT]\uD83D\uDD34';
                            }
                            paraText += ch;
                        }
                        if (paraText) texts.push(paraText);
                    }
                }
            }
            return texts.join(' ');
        }
        return '';
    }

    // ------------------------------------------------------------------
    // Debug Panel rendering
    // ------------------------------------------------------------------

    /**
     * Render the debug panel with tag normalisation and page boundary results.
     *
     * @param {Object} analysis - Analysis results from _runAnalysis
     */
    _renderDebugPanel(analysis) {
        if (!this.debugPanel || !this.debugContent) return;

        var html = '';

        // --- Template Configuration Results ---
        html += this._renderDebugTemplateSection(analysis);

        // --- Tag Normalisation Results ---
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Tag Normalisation Results</h4>';

        // Summary stats
        html += '<div class="debug-stats">';
        html += '<span class="debug-stat">Total tags: <b>' + analysis.totalTags + '</b></span>';
        html += '<span class="debug-stat">Unrecognised: <b>' + analysis.unrecognisedTags.length + '</b></span>';
        html += '<span class="debug-stat">Red text instructions: <b>' + analysis.redTextInstructions.length + '</b></span>';
        html += '<span class="debug-stat">Red-text-only blocks: <b>' + analysis.redTextOnlyCount + '</b></span>';
        html += '<span class="debug-stat">Whitespace-only blocks: <b>' + analysis.whitespaceOnlyCount + '</b></span>';
        html += '</div>';

        // Category breakdown
        var categories = analysis.tagsByCategory;
        var catKeys = Object.keys(categories);
        if (catKeys.length > 0) {
            html += '<div class="debug-categories">';
            html += '<span class="debug-label">By category:</span> ';
            for (var ci = 0; ci < catKeys.length; ci++) {
                html += '<span class="debug-category-badge">' +
                    this._esc(catKeys[ci]) + ': ' + categories[catKeys[ci]] + '</span>';
            }
            html += '</div>';
        }

        // Tag list
        if (analysis.tags.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>All tags (' + analysis.tags.length + ')</summary>';
            html += '<table class="debug-table"><thead><tr>' +
                '<th>Block</th><th>Raw</th><th>Normalised</th><th>Category</th><th>Details</th>' +
                '</tr></thead><tbody>';
            for (var i = 0; i < analysis.tags.length; i++) {
                var tag = analysis.tags[i];
                var details = '';
                if (tag.level) details += 'level=' + tag.level + ' ';
                if (tag.number) details += 'number=' + tag.number + ' ';
                if (tag.id) details += 'id=' + tag.id + ' ';
                if (tag.modifier) details += 'modifier=' + tag.modifier;
                details = details.trim();

                var rowClass = tag.normalised ? '' : ' class="debug-unrecognised"';
                html += '<tr' + rowClass + '>' +
                    '<td>' + tag.blockIndex + '</td>' +
                    '<td><code>' + this._esc(tag.raw) + '</code></td>' +
                    '<td>' + (tag.normalised ? this._esc(tag.normalised) : '<em>unrecognised</em>') + '</td>' +
                    '<td>' + (tag.category || '-') + '</td>' +
                    '<td>' + (details || '-') + '</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';
            html += '</details>';
        }

        // Unrecognised tags
        if (analysis.unrecognisedTags.length > 0) {
            html += '<details class="debug-details debug-warning">';
            html += '<summary>Unrecognised tags (' + analysis.unrecognisedTags.length + ')</summary>';
            html += '<ul>';
            for (var u = 0; u < analysis.unrecognisedTags.length; u++) {
                html += '<li>Block #' + analysis.unrecognisedTags[u].blockIndex +
                    ': <code>' + this._esc(analysis.unrecognisedTags[u].raw) + '</code></li>';
            }
            html += '</ul>';
            html += '</details>';
        }

        // Red text instructions
        if (analysis.redTextInstructions.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>Red text instructions (' + analysis.redTextInstructions.length + ')</summary>';
            html += '<ul>';
            for (var ri = 0; ri < analysis.redTextInstructions.length; ri++) {
                html += '<li>Block #' + analysis.redTextInstructions[ri].blockIndex +
                    ': <code>' + this._esc(analysis.redTextInstructions[ri].text) + '</code></li>';
            }
            html += '</ul>';
            html += '</details>';
        }

        html += '</div>';

        // --- Page Boundary Results ---
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Page Boundary Results</h4>';

        html += '<div class="debug-stats">';
        html += '<span class="debug-stat">Pages detected: <b>' + analysis.pages.length + '</b></span>';
        html += '</div>';

        if (analysis.pages.length > 0) {
            html += '<table class="debug-table"><thead><tr>' +
                '<th>File</th><th>Type</th><th>Lesson</th><th>Blocks</th><th>Rules Applied</th>' +
                '</tr></thead><tbody>';
            for (var pi = 0; pi < analysis.pages.length; pi++) {
                var page = analysis.pages[pi];
                var rulesHtml = '';
                if (page.boundaryDecisions && page.boundaryDecisions.length > 0) {
                    for (var d = 0; d < page.boundaryDecisions.length; d++) {
                        var dec = page.boundaryDecisions[d];
                        rulesHtml += '<span class="debug-rule-badge">Rule ' + dec.rule +
                            ': ' + this._esc(dec.action) + '</span> ';
                    }
                } else {
                    rulesHtml = '-';
                }

                html += '<tr>' +
                    '<td><code>' + this._esc(page.filename) + '</code></td>' +
                    '<td>' + this._esc(page.type) + '</td>' +
                    '<td>' + (page.lessonNumber !== null ? page.lessonNumber : '-') + '</td>' +
                    '<td>' + page.contentBlocks.length + '</td>' +
                    '<td>' + rulesHtml + '</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';

            // Boundary decision details
            var allDecisions = [];
            for (var ai = 0; ai < analysis.pages.length; ai++) {
                var pg = analysis.pages[ai];
                if (pg.boundaryDecisions) {
                    for (var di = 0; di < pg.boundaryDecisions.length; di++) {
                        allDecisions.push({
                            page: pg.filename,
                            decision: pg.boundaryDecisions[di]
                        });
                    }
                }
            }

            if (allDecisions.length > 0) {
                html += '<details class="debug-details">';
                html += '<summary>Boundary rule details (' + allDecisions.length + ' rules fired)</summary>';
                html += '<ul>';
                for (var bd = 0; bd < allDecisions.length; bd++) {
                    var item = allDecisions[bd];
                    html += '<li><b>' + this._esc(item.page) + '</b> &mdash; Rule ' +
                        item.decision.rule + ': ' + this._esc(item.decision.reason) + '</li>';
                }
                html += '</ul>';
                html += '</details>';
            }
        }

        html += '</div>';

        this.debugContent.innerHTML = html;
        this.debugPanel.classList.remove('hidden');
    }

    // ------------------------------------------------------------------
    // Debug — Template section
    // ------------------------------------------------------------------

    /**
     * Render template configuration info for the debug panel.
     *
     * @param {Object} analysis - Analysis results
     * @returns {string} HTML string
     */
    _renderDebugTemplateSection(analysis) {
        var html = '';
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Template Configuration</h4>';

        if (!this.selectedTemplateId) {
            html += '<p style="font-size:0.82rem;color:var(--color-text-secondary);">No template selected.</p>';
            html += '</div>';
            return html;
        }

        var config;
        try {
            config = this.templateEngine.getConfig(this.selectedTemplateId);
        } catch (e) {
            html += '<p style="font-size:0.82rem;color:var(--color-error);">Error loading template config.</p>';
            html += '</div>';
            return html;
        }

        // Summary stats
        html += '<div class="debug-stats">';
        html += '<span class="debug-stat">Template ID: <b>' + this._esc(this.selectedTemplateId) + '</b></span>';
        html += '<span class="debug-stat">Name: <b>' + this._esc(config._templateName) + '</b></span>';
        html += '<span class="debug-stat">HTML template attr: <b>' + this._esc(config._templateAttribute) + '</b></span>';
        html += '</div>';

        // Key config differences from base
        var diffs = this._getConfigDiffs(config);
        if (diffs.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>Key configuration (' + diffs.length + ' differences from base)</summary>';
            html += '<table class="debug-table"><thead><tr>' +
                '<th>Property</th><th>Value</th>' +
                '</tr></thead><tbody>';
            for (var i = 0; i < diffs.length; i++) {
                html += '<tr>' +
                    '<td><code>' + this._esc(diffs[i].key) + '</code></td>' +
                    '<td>' + this._esc(diffs[i].value) + '</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';
            html += '</details>';
        }

        // Skeleton preview (first 50 lines for overview page)
        var moduleCode = (this.currentMetadata && this.currentMetadata.moduleCode) || 'MODULE';
        var totalPages = analysis.pages ? analysis.pages.length : 1;

        try {
            var skeleton = this.templateEngine.generateSkeleton(config, {
                type: 'overview',
                lessonNumber: null,
                filename: moduleCode + '-00.html',
                moduleCode: moduleCode,
                englishTitle: 'Module Title',
                tereoTitle: null,
                totalPages: totalPages,
                pageIndex: 0
            });

            var skeletonLines = skeleton.split('\n');
            var previewLines = skeletonLines.slice(0, 50);
            var truncated = skeletonLines.length > 50;

            html += '<details class="debug-details">';
            html += '<summary>Overview page skeleton preview (' + skeletonLines.length + ' lines)</summary>';
            html += '<pre style="padding:0.5rem;font-size:0.75rem;overflow-x:auto;background:var(--color-bg);margin:0;">';
            html += this._esc(previewLines.join('\n'));
            if (truncated) {
                html += '\n... (' + (skeletonLines.length - 50) + ' more lines)';
            }
            html += '</pre>';
            html += '</details>';
        } catch (e) {
            // Skeleton generation failed — skip preview
        }

        // Footer navigation links for each page
        if (analysis.pages && analysis.pages.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>Footer navigation (' + analysis.pages.length + ' pages)</summary>';
            html += '<table class="debug-table"><thead><tr>' +
                '<th>Page</th><th>Prev</th><th>Next</th><th>Home</th>' +
                '</tr></thead><tbody>';
            for (var pi = 0; pi < analysis.pages.length; pi++) {
                var page = analysis.pages[pi];
                var prevLink = pi > 0
                    ? moduleCode + '-' + String(pi - 1).padStart(2, '0') + '.html'
                    : '-';
                var nextLink = pi < analysis.pages.length - 1
                    ? moduleCode + '-' + String(pi + 1).padStart(2, '0') + '.html'
                    : '-';
                html += '<tr>' +
                    '<td><code>' + this._esc(page.filename) + '</code></td>' +
                    '<td>' + (prevLink !== '-' ? '<code>' + this._esc(prevLink) + '</code>' : '-') + '</td>' +
                    '<td>' + (nextLink !== '-' ? '<code>' + this._esc(nextLink) + '</code>' : '-') + '</td>' +
                    '<td>Yes</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';
            html += '</details>';
        }

        html += '</div>';
        return html;
    }

    /**
     * Get notable differences between a resolved config and base defaults.
     *
     * @param {Object} config - Resolved template config
     * @returns {Array<{key: string, value: string}>}
     */
    _getConfigDiffs(config) {
        var diffs = [];

        // Body class
        if (config.bodyClass !== 'container-fluid') {
            diffs.push({ key: 'bodyClass', value: config.bodyClass });
        }

        // Footer class
        if (config.footerClass !== 'footer-nav') {
            diffs.push({ key: 'footerClass', value: config.footerClass });
        }

        // Header titles
        var overviewTitles = config.headerPattern &&
            config.headerPattern.overviewPage &&
            config.headerPattern.overviewPage.titles;
        if (overviewTitles && overviewTitles.indexOf('tereo') !== -1) {
            diffs.push({ key: 'headerPattern.overviewPage.titles', value: overviewTitles.join(', ') });
        }

        var lessonTitles = config.headerPattern &&
            config.headerPattern.lessonPage &&
            config.headerPattern.lessonPage.titles;
        if (lessonTitles && lessonTitles.indexOf('tereo') !== -1) {
            diffs.push({ key: 'headerPattern.lessonPage.titles', value: lessonTitles.join(', ') });
        }

        // Module menu lesson labels
        var lessonLabels = config.moduleMenu &&
            config.moduleMenu.lessonPage &&
            config.moduleMenu.lessonPage.labels;
        if (lessonLabels) {
            diffs.push({ key: 'moduleMenu.lessonPage.labels.success', value: lessonLabels.success });
        }

        // Overview tabs
        var overviewTabs = config.moduleMenu &&
            config.moduleMenu.overviewPage &&
            config.moduleMenu.overviewPage.tabs;
        if (overviewTabs && overviewTabs.length !== 2) {
            diffs.push({ key: 'moduleMenu.overviewPage.tabs', value: overviewTabs.join(', ') });
        }

        // Navigation
        if (config.navigation) {
            diffs.push({ key: 'navigation', value: config.navigation });
        }

        // Content duplication
        if (config.contentDuplication) {
            diffs.push({ key: 'contentDuplication', value: config.contentDuplication });
        }

        return diffs;
    }

    // ------------------------------------------------------------------
    // HTML conversion pipeline
    // ------------------------------------------------------------------

    /**
     * Run the HTML conversion pipeline on analysed pages.
     *
     * @param {Object} analysis - Analysis results from _runAnalysis
     * @param {Object} parserResult - Result from DocxParser.parse()
     */
    _runHtmlConversion(analysis, parserResult) {
        if (!this.selectedTemplateId || !analysis.pages || analysis.pages.length === 0) {
            return;
        }

        var config;
        try {
            config = this.templateEngine.getConfig(this.selectedTemplateId);
        } catch (e) {
            console.error('HtmlConversion: Failed to get template config:', e);
            return;
        }

        var moduleCode = (parserResult.metadata && parserResult.metadata.moduleCode) || 'MODULE';
        var moduleInfo = {
            moduleCode: moduleCode,
            englishTitle: this._extractTitle(parserResult, 'english'),
            tereoTitle: this._extractTitle(parserResult, 'tereo'),
            totalPages: analysis.pages.length,
            overviewContent: null
        };

        this.generatedHtmlFiles = {};
        this.generatedFileList = [];

        for (var i = 0; i < analysis.pages.length; i++) {
            var page = analysis.pages[i];
            this._addProgressStep('Generating HTML: ' + page.filename + '...');

            try {
                var fullHtml = this.htmlConverter.assemblePage(page, config, moduleInfo);
                this.generatedHtmlFiles[page.filename] = fullHtml;
                this.generatedFileList.push(page.filename);
            } catch (e) {
                console.error('HtmlConversion: Error generating ' + page.filename + ':', e);
                this.generatedHtmlFiles[page.filename] = '<!-- Error generating this page: ' + e.message + ' -->';
                this.generatedFileList.push(page.filename);
            }
        }

        this._addProgressStep('Done! Generated ' + this.generatedFileList.length + ' HTML files.');
    }

    /**
     * Extract a title (English or Te Reo) from the parsed content.
     *
     * @param {Object} parserResult - Parser result
     * @param {string} type - 'english' or 'tereo'
     * @returns {string} Title text
     */
    _extractTitle(parserResult, type) {
        // Try to find the title from the content after [TITLE BAR]
        var content = parserResult.content;
        var startIdx = parserResult.contentStartIndex || 0;
        var foundTitleBar = false;

        for (var i = startIdx; i < content.length && i < startIdx + 10; i++) {
            var block = content[i];
            if (block.type !== 'paragraph' || !block.data) continue;

            var text = block.data.text || '';
            var runs = block.data.runs || [];
            var fullText = '';
            for (var r = 0; r < runs.length; r++) {
                if (runs[r].text) fullText += runs[r].text;
            }

            // Check for title bar
            if (fullText.toLowerCase().indexOf('title bar') !== -1 ||
                text.toLowerCase().indexOf('title bar') !== -1) {
                foundTitleBar = true;
                // The title text is usually on the same line after the tag or on the next block
                var cleanedTitle = fullText.replace(/\[.*?\]/g, '').trim();
                if (cleanedTitle && type === 'english') {
                    // May contain both English and Te Reo separated by spaces
                    return cleanedTitle;
                }
                continue;
            }

            // After title bar, look for the main heading
            if (foundTitleBar && block.data.heading) {
                var headingText = '';
                for (var hr = 0; hr < runs.length; hr++) {
                    if (runs[hr].text && !(runs[hr].formatting && runs[hr].formatting.isRed)) {
                        headingText += runs[hr].text;
                    }
                }
                if (headingText.trim() && type === 'english') {
                    return headingText.trim();
                }
            }
        }

        return type === 'english' ? 'Module Title' : '';
    }

    // ------------------------------------------------------------------
    // Output mode management
    // ------------------------------------------------------------------

    /**
     * Toggle between HTML and text output modes.
     */
    _toggleOutputMode() {
        if (this.outputMode === 'html') {
            this.outputMode = 'text';
            this.outputArea.value = this.currentOutput ? this.currentOutput.full : '';
        } else {
            this.outputMode = 'html';
            this._displayCurrentHtmlFile();
        }
        this._updateOutputModeUI();
    }

    /**
     * Update UI elements to reflect the current output mode.
     */
    _updateOutputModeUI() {
        if (this.outputModeToggle) {
            if (this.outputMode === 'html') {
                this.outputModeToggle.textContent = '\u{1F4C4} Switch to Text Output';
                this.outputModeToggle.title = 'Switch to legacy text output';
            } else {
                this.outputModeToggle.textContent = '\u{1F310} Switch to HTML Output';
                this.outputModeToggle.title = 'Switch to HTML output';
            }
        }

        // Show/hide HTML file selector
        if (this.htmlFileSelector) {
            if (this.outputMode === 'html' && this.generatedFileList.length > 0) {
                this.htmlFileSelector.classList.remove('hidden');
            } else {
                this.htmlFileSelector.classList.add('hidden');
            }
        }

        // Update button labels
        if (this.outputMode === 'html' && this.generatedFileList.length > 0) {
            this.btnCopyAll.textContent = '\u{1F4CB} Copy HTML Source';
            this.btnCopyContent.textContent = '\u{1F4CB} Copy HTML Source';
            this.btnDownload.textContent = '\u{1F4BE} Download .html';
        } else {
            this.btnCopyAll.textContent = '\u{1F4CB} Copy All to Clipboard';
            this.btnCopyContent.textContent = '\u{1F4CB} Copy Content Only';
            this.btnDownload.textContent = '\u{1F4BE} Download as .txt';
        }
    }

    /**
     * Populate the HTML file dropdown with generated filenames.
     */
    _populateHtmlFileDropdown() {
        if (!this.htmlFileDropdown) return;
        this.htmlFileDropdown.innerHTML = '';

        for (var i = 0; i < this.generatedFileList.length; i++) {
            var option = document.createElement('option');
            option.value = i;
            option.textContent = this.generatedFileList[i];
            this.htmlFileDropdown.appendChild(option);
        }
    }

    /**
     * Display the currently selected HTML file in the output area.
     */
    _displayCurrentHtmlFile() {
        if (this.generatedFileList.length === 0) return;
        var filename = this.generatedFileList[this.currentHtmlFileIndex];
        var htmlContent = this.generatedHtmlFiles[filename] || '';
        this.outputArea.value = htmlContent;
    }

    /**
     * Download content as a file with specified MIME type.
     *
     * @param {string} content - File content
     * @param {string} filename - File name
     * @param {string} mimeType - MIME type
     */
    _downloadAsFile(content, filename, mimeType) {
        var blob = new Blob([content], { type: mimeType });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        this.showToast('Downloaded ' + filename);
    }

    // ------------------------------------------------------------------
    // HTML escaping
    // ------------------------------------------------------------------

    _esc(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }
}

// ------------------------------------------------------------------
// Boot
// ------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    window.app = new App();
});
