/**
 * App — UI controller for PageForge.
 *
 * Manages file upload (drag-and-drop + click-to-browse), staged file
 * handling, Convert button, progress display, multi-file output rendering,
 * clipboard copy, individual and bulk file download (ZIP), and debug panel.
 */

'use strict';

class App {
    constructor() {
        this.parser = new DocxParser();
        this.formatter = new OutputFormatter();
        this.tagNormaliser = new TagNormaliser();
        this.layoutTableUnwrapper = new LayoutTableUnwrapper(this.tagNormaliser);
        this.blockScoper = new BlockScoper(this.tagNormaliser);
        this.pageBoundary = new PageBoundary(this.tagNormaliser);
        this.templateEngine = new TemplateEngine();
        this.interactiveExtractor = new InteractiveExtractor(this.tagNormaliser);
        this.htmlConverter = new HtmlConverter(this.tagNormaliser, this.templateEngine, this.interactiveExtractor);
        this.outputManager = new OutputManager();

        /** Cached formatted output after a successful parse */
        this.currentOutput = null;

        /** Cached metadata for display */
        this.currentMetadata = null;

        /** Cached tag/page analysis for debug panel */
        this.currentAnalysis = null;

        /** Currently selected template ID (from dropdown manual selection) */
        this.selectedTemplateId = null;

        /** Auto-detected template ID (from module code) */
        this.autoDetectedTemplate = null;

        /** Whether the user has manually selected a template */
        this.userManuallySelectedTemplate = false;

        /** Staged file waiting for conversion */
        this.stagedFile = null;

        /** Generated HTML files keyed by filename */
        this.generatedHtmlFiles = {};

        /** Ordered list of generated filenames */
        this.generatedFileList = [];

        /** Currently selected filename for preview */
        this.selectedPreviewFile = null;

        /** Generated interactive reference document text */
        this.interactiveReferenceDoc = '';

        /** Collected interactive data */
        this.collectedInteractives = [];

        this._bindElements();
        this._bindEvents();
        this._initTemplateEngine();

        this._debugPanelRenderer = new DebugPanelRenderer({
            debugPanel: this.debugPanel,
            debugContent: this.debugContent,
            outputManager: this.outputManager,
            templateEngine: this.templateEngine
        });
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
        this.outputArea = document.getElementById('output-area');
        this.btnDownloadZip = document.getElementById('btn-download-zip');
        this.btnDownloadText = document.getElementById('btn-download-text');
        this.btnReset = document.getElementById('btn-reset');
        this.fileListPanel = document.getElementById('file-list-panel');
        this.outputLayout = document.getElementById('output-layout');
        this.previewFilename = document.getElementById('preview-filename');
        this.btnCopyPreview = document.getElementById('btn-copy-preview');
        this.btnDownloadPreview = document.getElementById('btn-download-preview');
        this.errorPanel = document.getElementById('error-panel');
        this.errorMessage = document.getElementById('error-message');
        this.toast = document.getElementById('toast');
        this.debugPanel = document.getElementById('debug-panel');
        this.debugContent = document.getElementById('debug-content');
        this.debugToggle = document.getElementById('debug-toggle');
        this.templateDropdown = document.getElementById('template-dropdown');
        this.templateAutoLabel = document.getElementById('template-auto-label');
        this.btnConvert = document.getElementById('btn-convert');
        this.stagedFileInfo = document.getElementById('staged-file-info');
        this.stagedFileName = document.getElementById('staged-file-name');
        this.stagedTemplateHint = document.getElementById('staged-template-hint');
    }

    // ------------------------------------------------------------------
    // Event binding
    // ------------------------------------------------------------------

    _bindEvents() {
        var self = this;

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
            var files = e.dataTransfer.files;
            if (files.length > 0) {
                self.stageFile(files[0]);
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
                self.stageFile(self.fileInput.files[0]);
            }
        });

        // Convert button
        if (this.btnConvert) {
            this.btnConvert.addEventListener('click', function () {
                self.convertDocument();
            });
        }

        // Global action buttons
        if (this.btnDownloadZip) {
            this.btnDownloadZip.addEventListener('click', function () {
                self._handleDownloadZip();
            });
        }

        if (this.btnDownloadText) {
            this.btnDownloadText.addEventListener('click', function () {
                self._handleDownloadText();
            });
        }

        this.btnReset.addEventListener('click', function () {
            self.reset();
        });

        // Preview panel buttons
        if (this.btnCopyPreview) {
            this.btnCopyPreview.addEventListener('click', function () {
                self._handleCopyPreview();
            });
        }

        if (this.btnDownloadPreview) {
            this.btnDownloadPreview.addEventListener('click', function () {
                self._handleDownloadPreview();
            });
        }

        // Template dropdown
        this.templateDropdown.addEventListener('change', function () {
            if (self.templateDropdown.value) {
                self.selectedTemplateId = self.templateDropdown.value;
                self.userManuallySelectedTemplate = true;
                // Hide auto-detected label when user manually changes
                self.templateAutoLabel.classList.add('hidden');
            }
        });

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
     * Auto-detect template from module code. Stores the detected template
     * internally but does NOT change the dropdown selection. Shows a hint
     * near the staged file info instead.
     *
     * @param {string|null} moduleCode
     */
    _autoDetectTemplate(moduleCode) {
        var detected = this.templateEngine.detectTemplate(moduleCode);
        if (detected) {
            this.autoDetectedTemplate = detected;
            // Show hint near staged file
            if (this.stagedTemplateHint) {
                try {
                    var config = this.templateEngine.getConfig(detected);
                    this.stagedTemplateHint.textContent = 'Auto-detected: ' + config._templateName;
                    this.stagedTemplateHint.classList.remove('hidden');
                } catch (e) {
                    // Ignore — template config not available
                }
            }
        }
    }

    /**
     * Get the resolved template ID to use for conversion.
     * Manual dropdown selection takes priority over auto-detected.
     *
     * @returns {string|null}
     */
    _getResolvedTemplateId() {
        if (this.userManuallySelectedTemplate && this.selectedTemplateId) {
            return this.selectedTemplateId;
        }
        return this.autoDetectedTemplate || null;
    }

    // ------------------------------------------------------------------
    // File staging (upload without conversion)
    // ------------------------------------------------------------------

    /**
     * Stage a file for conversion. Validates and stores the file,
     * extracts module code for template auto-detection, and enables
     * the Convert button. Does NOT trigger full parsing/conversion.
     *
     * @param {File} file
     */
    stageFile(file) {
        // Validate file type
        if (!file.name.toLowerCase().endsWith('.docx')) {
            this.showError(
                'Please upload a .docx file. Other formats (PDF, .doc, .txt) are not supported.'
            );
            return;
        }

        this.hideError();

        // Store the staged file
        this.stagedFile = file;

        // Show staged file info
        if (this.stagedFileInfo && this.stagedFileName) {
            this.stagedFileName.textContent = file.name;
            this.stagedFileInfo.classList.remove('hidden');
        }

        // Update drop zone appearance
        this.dropZone.querySelector('.drop-zone-title').textContent = 'File staged — click to change';

        // Extract module code from filename for template auto-detection
        var moduleCodeMatch = file.name.match(/[A-Z]{4}\d{3}/);
        var moduleCode = moduleCodeMatch ? moduleCodeMatch[0] : null;

        // Reset manual template selection flag when a new file is staged
        this.userManuallySelectedTemplate = false;
        this.autoDetectedTemplate = null;
        if (this.stagedTemplateHint) {
            this.stagedTemplateHint.classList.add('hidden');
        }

        // Reset dropdown to default
        this.templateDropdown.selectedIndex = 0;
        this.templateAutoLabel.classList.add('hidden');

        // Auto-detect template
        if (moduleCode) {
            this._autoDetectTemplate(moduleCode);
        }

        // Enable Convert button
        if (this.btnConvert) {
            this.btnConvert.disabled = false;
        }

        this._announce('File staged: ' + file.name + '. Click Convert Document to process.');
    }

    // ------------------------------------------------------------------
    // Conversion pipeline (triggered by Convert button)
    // ------------------------------------------------------------------

    /**
     * Run the full conversion pipeline on the staged file.
     * This is what used to happen automatically on file upload.
     */
    async convertDocument() {
        if (!this.stagedFile) {
            this.showError('No file staged. Please upload a .docx file first.');
            return;
        }

        var file = this.stagedFile;

        // Large file warning
        if (file.size > 20 * 1024 * 1024) {
            this._addProgressStep('\u26A0 Large file detected (' +
                Math.round(file.size / 1024 / 1024) + ' MB). This may take a moment.');
        }

        this.hideError();
        this.showProcessing();

        // Resolve which template to use
        this.selectedTemplateId = this._getResolvedTemplateId();

        var self = this;

        // Wire up progress callback
        this.parser.onProgress = function (msg) {
            self._addProgressStep(msg);
        };

        try {
            var result = await this.parser.parse(file);
            var output = this.formatter.formatAll(result);

            self.currentOutput = output;
            self.currentMetadata = result.metadata;

            // If we didn't detect a template from filename, try from parsed metadata
            if (!self.selectedTemplateId && result.metadata.moduleCode) {
                var detected = self.templateEngine.detectTemplate(result.metadata.moduleCode);
                if (detected) {
                    self.selectedTemplateId = detected;
                }
            }

            // Run tag normalisation and page boundary analysis
            self._addProgressStep('Normalising tags...');
            var analysis = self._runAnalysis(result);
            self.currentAnalysis = analysis;
            self._addProgressStep('Detecting page boundaries... (' + analysis.pages.length + ' pages)');
            if (analysis.blockScopes) {
                var scopedCount = analysis.blockScopes.filter(function(b) { return b.blockType; }).length;
                self._addProgressStep('Block scoping complete: ' + scopedCount + ' scoped blocks');
            }
            self._addProgressStep('Tag analysis complete: ' +
                analysis.totalTags + ' tags found, ' +
                analysis.pages.length + ' pages detected');

            // Run HTML conversion if a template is selected
            self._addProgressStep('Loading template: ' +
                (self.selectedTemplateId ? self.templateEngine.getConfig(self.selectedTemplateId)._templateName : 'default') + '...');
            self._runHtmlConversion(analysis, result);

            // Store all outputs in OutputManager
            self._storeOutputs();

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

            console.error('PageForge error:', err);
        }
    }

    // ------------------------------------------------------------------
    // Store outputs in OutputManager
    // ------------------------------------------------------------------

    /**
     * Store all generated files in the OutputManager.
     */
    _storeOutputs() {
        this.outputManager.clear();

        // Store HTML files
        for (var i = 0; i < this.generatedFileList.length; i++) {
            var filename = this.generatedFileList[i];
            var content = this.generatedHtmlFiles[filename] || '';
            var pageType = 'lesson';
            var lessonNumber = null;

            if (i === 0) {
                pageType = 'overview';
            } else {
                pageType = 'lesson';
                lessonNumber = i;
            }

            this.outputManager.addFile({
                filename: filename,
                content: content,
                type: 'html',
                pageType: pageType,
                lessonNumber: lessonNumber
            });
        }

        // Store interactive reference document
        if (this.interactiveReferenceDoc) {
            var moduleCode = (this.currentMetadata && this.currentMetadata.moduleCode) || 'MODULE';
            this.outputManager.addFile({
                filename: moduleCode + '_interactives.txt',
                content: this.interactiveReferenceDoc,
                type: 'reference',
                pageType: 'reference',
                lessonNumber: null
            });
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

        // Render file list and show preview
        if (this.generatedFileList.length > 0) {
            this._renderFileList();
            // Auto-select first file
            var firstFilename = this.generatedFileList[0];
            this._selectFile(firstFilename);
            // Show HTML layout
            if (this.outputLayout) {
                this.outputLayout.classList.remove('hidden');
            }
        }

        // Check if content is empty
        if (!output.contentOnly || output.contentOnly.trim() === '--- CONTENT START ---') {
            this.showError('This document appears to be empty or contains no text content.');
        }

        // Render debug panel (now includes conversion summary)
        if (this.currentAnalysis) {
            this._debugPanelRenderer.render({
                analysis: this.currentAnalysis,
                metadata: this.currentMetadata,
                collectedInteractives: this.collectedInteractives,
                interactiveReferenceDoc: this.interactiveReferenceDoc,
                selectedTemplateId: this.selectedTemplateId
            });
        }

        // Announce to screen readers
        var announceMsg = 'Document processed successfully. ';
        if (this.generatedFileList.length > 0) {
            announceMsg += 'Generated ' + this.generatedFileList.length + ' HTML files.';
        }
        if (this.collectedInteractives && this.collectedInteractives.length > 0) {
            announceMsg += ' Found ' + this.collectedInteractives.length + ' interactive components.';
        }
        this._announce(announceMsg);
    }

    reset() {
        this.currentOutput = null;
        this.currentMetadata = null;
        this.currentAnalysis = null;
        this.selectedTemplateId = null;
        this.autoDetectedTemplate = null;
        this.userManuallySelectedTemplate = false;
        this.stagedFile = null;
        this.generatedHtmlFiles = {};
        this.generatedFileList = [];
        this.selectedPreviewFile = null;
        this.interactiveReferenceDoc = '';
        this.collectedInteractives = [];
        this.blockScoper.warnings = [];
        this.outputManager.clear();
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
        // Clear file list
        if (this.fileListPanel) {
            this.fileListPanel.innerHTML = '';
        }
        // Reset staged file info
        if (this.stagedFileInfo) {
            this.stagedFileInfo.classList.add('hidden');
        }
        if (this.stagedTemplateHint) {
            this.stagedTemplateHint.classList.add('hidden');
        }
        // Reset drop zone text
        var dropTitle = this.dropZone.querySelector('.drop-zone-title');
        if (dropTitle) {
            dropTitle.textContent = 'Drop your .docx file here or click to browse';
        }
        // Disable Convert button
        if (this.btnConvert) {
            this.btnConvert.disabled = true;
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
        var step = document.createElement('div');
        step.className = 'progress-step';

        // Check mark for completed steps (all but the last are "done")
        step.textContent = message;

        this.progressSteps.appendChild(step);
        this.progressStatus.textContent = message;

        // Scroll to bottom
        this.progressSteps.scrollTop = this.progressSteps.scrollHeight;
    }

    // ------------------------------------------------------------------
    // File List rendering
    // ------------------------------------------------------------------

    /**
     * Render the file list panel with all generated files.
     */
    _renderFileList() {
        if (!this.fileListPanel) return;

        var self = this;
        var files = this.outputManager.getFileList();
        this.fileListPanel.innerHTML = '';

        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            var entry = this._createFileEntry(file);
            this.fileListPanel.appendChild(entry);
        }
    }

    /**
     * Create a file entry DOM element.
     *
     * @param {Object} file - File metadata from OutputManager.getFileList()
     * @returns {HTMLElement}
     */
    _createFileEntry(file) {
        var self = this;

        var entry = document.createElement('div');
        entry.className = 'file-entry';
        entry.setAttribute('data-filename', file.filename);
        entry.setAttribute('tabindex', '0');
        entry.setAttribute('role', 'button');
        entry.setAttribute('aria-label', 'Preview ' + file.filename);

        // File icon
        var icon = file.type === 'reference' ? '\uD83D\uDCCB' : '\uD83D\uDCC4';

        // File metadata description
        var metaText = '';
        if (file.pageType === 'overview') {
            metaText = 'Overview';
        } else if (file.pageType === 'lesson') {
            metaText = 'Lesson ' + file.lessonNumber;
        } else if (file.pageType === 'reference') {
            metaText = 'Interactive Reference';
            if (this.collectedInteractives && this.collectedInteractives.length > 0) {
                metaText += ' \u00B7 ' + this.collectedInteractives.length + ' interactives';
            }
        }
        metaText += ' \u00B7 ' + file.sizeFormatted;

        entry.innerHTML =
            '<div class="file-info">' +
                '<span class="file-icon">' + icon + '</span>' +
                '<div class="file-details">' +
                    '<span class="file-name">' + this._esc(file.filename) + '</span>' +
                    '<span class="file-meta">' + this._esc(metaText) + '</span>' +
                '</div>' +
            '</div>' +
            '<div class="file-actions">' +
                '<button class="btn btn-sm file-download" type="button" title="Download ' + this._esc(file.filename) + '">\uD83D\uDCBE</button>' +
                '<button class="btn btn-sm file-copy" type="button" title="Copy to clipboard">\uD83D\uDCCB</button>' +
            '</div>';

        // Click to select/preview
        entry.addEventListener('click', function (e) {
            // Don't select if clicking action buttons
            if (e.target.closest('.file-actions')) return;
            self._selectFile(file.filename);
        });

        // Keyboard: Enter/Space to select
        entry.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                self._selectFile(file.filename);
            }
        });

        // Download button
        var downloadBtn = entry.querySelector('.file-download');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                self.outputManager.downloadFile(file.filename);
                self.showToast('Downloaded ' + file.filename);
            });
        }

        // Copy button
        var copyBtn = entry.querySelector('.file-copy');
        if (copyBtn) {
            copyBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                self.outputManager.copyToClipboard(file.filename).then(function (ok) {
                    if (ok) {
                        self.showToast('Copied ' + file.filename + ' to clipboard');
                    } else {
                        self.showToast('Failed to copy. Please try again.');
                    }
                });
            });
        }

        return entry;
    }

    /**
     * Select a file and display it in the preview panel.
     *
     * @param {string} filename
     */
    _selectFile(filename) {
        this.selectedPreviewFile = filename;

        // Update visual highlighting
        var entries = this.fileListPanel.querySelectorAll('.file-entry');
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].getAttribute('data-filename') === filename) {
                entries[i].classList.add('selected');
            } else {
                entries[i].classList.remove('selected');
            }
        }

        // Update preview content
        var content = this.outputManager.getFileContent(filename);
        if (content !== null) {
            this.outputArea.value = content;
        }

        // Update preview filename display
        if (this.previewFilename) {
            this.previewFilename.textContent = filename;
        }
    }

    // ------------------------------------------------------------------
    // Global action handlers
    // ------------------------------------------------------------------

    /**
     * Handle "Download All as ZIP" button click.
     */
    async _handleDownloadZip() {
        if (this.outputManager.getFileCount() === 0) {
            this.showToast('No files to download');
            return;
        }

        var moduleCode = (this.currentMetadata && this.currentMetadata.moduleCode) || 'MODULE';
        var zipFilename = moduleCode + '_html_files.zip';

        try {
            await this.outputManager.downloadAsZip(zipFilename);
            this.showToast('Downloaded ' + zipFilename);
        } catch (e) {
            this.showToast('Failed to create ZIP: ' + e.message);
        }
    }

    /**
     * Handle "Download Text Template" button click.
     * Downloads the formatted text output as a .txt file.
     */
    _handleDownloadText() {
        if (!this.currentOutput) {
            this.showToast('No text output available');
            return;
        }

        var code = this.currentMetadata && this.currentMetadata.moduleCode
            ? this.currentMetadata.moduleCode
            : 'PageForge_output';
        var filename = code + '_parsed.txt';
        var blob = new Blob([this.currentOutput.full], { type: 'text/plain;charset=utf-8' });
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

    /**
     * Handle preview panel "Copy" button click.
     */
    _handleCopyPreview() {
        if (!this.selectedPreviewFile) {
            this.showToast('No file selected');
            return;
        }

        var self = this;
        this.outputManager.copyToClipboard(this.selectedPreviewFile).then(function (ok) {
            if (ok) {
                self.showToast('Copied ' + self.selectedPreviewFile + ' to clipboard');
            } else {
                self.showToast('Failed to copy. Please try again.');
            }
        });
    }

    /**
     * Handle preview panel "Download" button click.
     */
    _handleDownloadPreview() {
        if (!this.selectedPreviewFile) {
            this.showToast('No file selected');
            return;
        }

        this.outputManager.downloadFile(this.selectedPreviewFile);
        this.showToast('Downloaded ' + this.selectedPreviewFile);
    }

    // ------------------------------------------------------------------
    // Metadata rendering
    // ------------------------------------------------------------------

    _renderMetadata(metadata) {
        var items = [];

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

        // Add pages generated
        if (this.generatedFileList.length > 0) {
            items.push({ label: 'Pages', value: this.generatedFileList.length + ' HTML files' });
        }

        // Add interactive count
        if (this.collectedInteractives && this.collectedInteractives.length > 0) {
            var tier1 = 0;
            var tier2 = 0;
            for (var ic = 0; ic < this.collectedInteractives.length; ic++) {
                if (this.collectedInteractives[ic].tier === 1) tier1++;
                else tier2++;
            }
            items.push({
                label: 'Interactives',
                value: this.collectedInteractives.length +
                    ' (Tier 1: ' + tier1 + ', Tier 2: ' + tier2 + ')'
            });
        }

        if (items.length === 0) {
            this.metadataPanel.innerHTML =
                '<span class="metadata-empty">No metadata detected in document boilerplate</span>';
            return;
        }

        var html = '';
        for (var i = 0; i < items.length; i++) {
            html += '<div class="metadata-item">' +
                '<span class="metadata-label">' + this._esc(items[i].label) + ':</span> ' +
                '<span class="metadata-value">' + this._esc(items[i].value) + '</span>' +
                '</div>';
        }
        this.metadataPanel.innerHTML = html;
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
        var textarea = document.createElement('textarea');
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
        var blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
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

        // Unwrap layout tables BEFORE any analysis or conversion
        // This modifies the content array in-place, replacing layout tables
        // with their cell content as individual paragraph blocks
        try {
            this.layoutTableUnwrapper.unwrapLayoutTables(contentBlocks, startIndex);
        } catch (e) {
            console.error('Layout table unwrapping failed:', e);
        }

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

        // Run block scoping analysis
        var contentFromStart = contentBlocks.slice(startIndex);
        var blockScopeResults = null;
        try {
            blockScopeResults = this.blockScoper.scopeBlocks(contentFromStart);
        } catch (e) {
            console.error('Block scoping analysis failed:', e);
        }

        // Run page boundary detection
        var pages = this.pageBoundary.assignPages(contentFromStart, moduleCode);

        return {
            totalTags: allTags.length,
            tags: allTags,
            unrecognisedTags: unrecognisedTags,
            redTextInstructions: redTextInstructions,
            redTextOnlyCount: redTextOnlyCount,
            whitespaceOnlyCount: whitespaceOnlyCount,
            tagsByCategory: tagsByCategory,
            pages: pages,
            blockScopes: blockScopeResults,
            blockScopeWarnings: this.blockScoper.warnings || []
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

        // Reset collected interactives for this conversion run
        this.htmlConverter.collectedInteractives = [];

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

        // Collect interactives and generate reference document
        this.collectedInteractives = this.htmlConverter.collectedInteractives || [];
        if (this.collectedInteractives.length > 0) {
            this._addProgressStep('Extracting interactive data... (' +
                this.collectedInteractives.length + ' interactives)');
            this.interactiveReferenceDoc = this.interactiveExtractor.generateReferenceDocument(
                this.collectedInteractives, moduleCode
            );
            this._addProgressStep('Generating interactive reference document...');
        } else {
            this.interactiveReferenceDoc = '';
        }

        this._addProgressStep('Done! Generated ' + this.generatedFileList.length +
            ' HTML files' + (this.interactiveReferenceDoc ? ' + interactive reference.' : '.'));
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
        var fullTitleText = '';

        for (var i = startIdx; i < content.length && i < startIdx + 20; i++) {
            var block = content[i];
            if (block.type !== 'paragraph' || !block.data) continue;

            var text = block.data.text || '';
            var runs = block.data.runs || [];
            var fullText = '';
            var nonRedText = '';
            for (var r = 0; r < runs.length; r++) {
                if (runs[r].text) {
                    fullText += runs[r].text;
                    if (!(runs[r].formatting && runs[r].formatting.isRed)) {
                        nonRedText += runs[r].text;
                    }
                }
            }

            // Check for title bar
            if (fullText.toLowerCase().indexOf('title bar') !== -1 ||
                text.toLowerCase().indexOf('title bar') !== -1) {
                foundTitleBar = true;
                // The title text may be on the same block (non-red portion after the tag)
                var cleanedTitle = nonRedText.replace(/\[.*?\]/g, '').trim();
                if (cleanedTitle) {
                    fullTitleText = cleanedTitle;
                    break;
                }
                // Also try the full text with tags stripped
                var altClean = fullText.replace(/\[.*?\]/g, '').trim();
                if (altClean) {
                    fullTitleText = altClean;
                    break;
                }
                continue;
            }

            // After title bar, look for the first non-empty content block
            // (could be a heading or a regular paragraph with the title text)
            if (foundTitleBar) {
                // Try non-red text first
                var titleCandidate = nonRedText.replace(/\[.*?\]/g, '').trim();
                if (!titleCandidate) {
                    // Fall back to full text with tags stripped
                    titleCandidate = fullText.replace(/\[.*?\]/g, '').trim();
                }
                if (titleCandidate) {
                    fullTitleText = titleCandidate;
                    break;
                }
            }
        }

        if (!fullTitleText) {
            // Last resort: try metadata subject
            if (parserResult.metadata && parserResult.metadata.subject) {
                fullTitleText = parserResult.metadata.subject;
            } else {
                return type === 'english' ? 'Module Title' : '';
            }
        }

        // Convert ALL CAPS titles to title case
        fullTitleText = this._convertToTitleCase(fullTitleText);

        // Split on double-space or space-pipe-space to separate English and Te Reo titles
        var titleParts = fullTitleText.split(/  +| \| /);
        var englishTitle = (titleParts[0] || '').trim();
        var tereoTitle = titleParts.length > 1 ? titleParts.slice(1).join('  ').trim() : '';

        // If no double-space split found, try splitting at sentence-ending
        // punctuation boundary (e.g., "Picture This! Whakaahuatia Tēnei!")
        if (!tereoTitle && englishTitle) {
            var sentenceSplit = englishTitle.match(/^(.+[!?.])\s+(.+)$/);
            if (sentenceSplit) {
                // Check if the second part looks like Te Reo (contains macrons
                // or common Māori words)
                var secondPart = sentenceSplit[2];
                if (/[\u0100\u0101\u0112\u0113\u012A\u012B\u014C\u014D\u016A\u016B]/.test(secondPart) ||
                    /\b(?:te|nga|ki|ko|he|ka|kei|wh[aeiou])/i.test(secondPart)) {
                    englishTitle = sentenceSplit[1].trim();
                    tereoTitle = secondPart.trim();
                }
            }
        }

        if (type === 'english') {
            return englishTitle || fullTitleText;
        } else if (type === 'tereo') {
            return tereoTitle;
        }

        return '';
    }

    /**
     * Convert ALL CAPS text to title case.
     * Only converts if the text is predominantly uppercase.
     *
     * @param {string} text - Input text
     * @returns {string} Title-cased text
     */
    _convertToTitleCase(text) {
        if (!text) return text;

        // Only convert if text is predominantly uppercase (>60% uppercase letters)
        var letters = text.replace(/[^a-zA-Z\u00C0-\u024F]/g, '');
        if (!letters) return text;
        var upperCount = (letters.match(/[A-Z\u00C0-\u00DE\u0100\u0112\u012A\u014C\u016A]/g) || []).length;
        if (upperCount / letters.length < 0.6) return text;

        // Title case: lowercase everything, then capitalize first letter of each word
        return text.replace(/\S+/g, function (word) {
            return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
        });
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
