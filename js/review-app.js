/**
 * ReviewApp — Controller for the Visual Comparison Review page.
 *
 * Handles data deserialisation from sessionStorage, three-panel rendering,
 * file map interaction, synchronised scrolling (Sync Mode), Raw HTML toggle,
 * human reference file upload, and calibration tool integration.
 *
 * This is a standalone controller for review.html — it does not depend on
 * App, DocxParser, or any other main-page class. It loads its data from
 * sessionStorage (serialised by App._serialiseForReview()).
 */

'use strict';

class ReviewApp {
    constructor() {
        /** Deserialised data from main page */
        this.data = null;

        /** Human reference files (from transfer + uploaded on this page) */
        this.humanReferenceFiles = [];

        /** Currently selected filename */
        this.selectedFile = null;

        /** Sync mode enabled flag */
        this.syncModeEnabled = false;

        /** Raw HTML mode enabled flag */
        this.rawHtmlMode = false;

        /** Currently highlighted block index (for copy-to-snapshot) */
        this.highlightedBlockIndex = null;

        /** CalibrationManager instance */
        this.calibrationManager = null;

        this._loadData();
        this._bindElements();
        this._bindEvents();
        this._initCalibrationManager();
        this._render();
    }

    // ------------------------------------------------------------------
    // Data loading
    // ------------------------------------------------------------------

    /**
     * Load serialised data from sessionStorage.
     */
    _loadData() {
        try {
            // Try chunked storage first
            var chunkCount = sessionStorage.getItem('pageforge_review_chunks');
            var raw;
            if (chunkCount) {
                var count = parseInt(chunkCount, 10);
                var parts = [];
                for (var i = 0; i < count; i++) {
                    var chunk = sessionStorage.getItem('pageforge_review_chunk_' + i);
                    if (chunk) parts.push(chunk);
                }
                raw = parts.join('');
            } else {
                raw = sessionStorage.getItem('pageforge_review_data');
            }

            if (!raw) {
                this.data = null;
                return;
            }

            this.data = JSON.parse(raw);

            // Load transferred human reference files
            if (this.data.humanReferenceFiles && this.data.humanReferenceFiles.length > 0) {
                this.humanReferenceFiles = this.data.humanReferenceFiles.slice();
            }
        } catch (e) {
            console.error('ReviewApp: Failed to load data from sessionStorage:', e);
            this.data = null;
        }
    }

    // ------------------------------------------------------------------
    // DOM references
    // ------------------------------------------------------------------

    _bindElements() {
        this.fileMapList = document.getElementById('file-map-list');
        this.syncModeToggle = document.getElementById('sync-mode-toggle');
        this.btnRawHtmlToggle = document.getElementById('btn-raw-html-toggle');
        this.moduleCodeDisplay = document.getElementById('review-module-code');

        // PageForge panel
        this.pageforgeIframe = document.getElementById('pageforge-iframe');
        this.pageforgeFilename = document.getElementById('pageforge-filename');
        this.pageforgeRaw = document.getElementById('pageforge-raw');
        this.pageforgeRawCode = document.getElementById('pageforge-raw-code');

        // Human reference panel
        this.humanIframe = document.getElementById('human-iframe');
        this.humanFilename = document.getElementById('human-filename');
        this.humanUploadPrompt = document.getElementById('human-upload-prompt');
        this.humanNoMatchMsg = document.getElementById('human-no-match-msg');
        this.humanRaw = document.getElementById('human-raw');
        this.humanRawCode = document.getElementById('human-raw-code');
        this.refDropzone = document.getElementById('review-ref-dropzone');
        this.refFileInput = document.getElementById('review-ref-file-input');
        this.refUploaded = document.getElementById('review-ref-uploaded');
        this.btnUploadMore = document.getElementById('btn-upload-more-ref');
        this.refFileInputExtra = document.getElementById('review-ref-file-input-extra');

        // Writer template panel
        this.writerContent = document.getElementById('writer-content');
        this.writerFilename = document.getElementById('writer-filename');

        // Copy-to-snapshot buttons
        this.btnCopyPfToSnapshot = document.getElementById('btn-copy-pf-to-snapshot');
        this.btnCopyHumanToSnapshot = document.getElementById('btn-copy-human-to-snapshot');
        this.btnCopyWriterToSnapshot = document.getElementById('btn-copy-writer-to-snapshot');

        // Toast
        this.toast = document.getElementById('toast');
    }

    // ------------------------------------------------------------------
    // Event binding
    // ------------------------------------------------------------------

    _bindEvents() {
        var self = this;

        // Sync mode toggle
        if (this.syncModeToggle) {
            this.syncModeToggle.addEventListener('change', function () {
                self.syncModeEnabled = self.syncModeToggle.checked;
                self._updateSyncModeIndicator();
                if (!self.syncModeEnabled) {
                    self._hideCopyToSnapshotButtons();
                }
            });
        }

        // Raw HTML toggle
        if (this.btnRawHtmlToggle) {
            this.btnRawHtmlToggle.addEventListener('click', function () {
                self.rawHtmlMode = !self.rawHtmlMode;
                self._toggleRawHtmlMode();
            });
        }

        // Human reference file upload (main dropzone)
        if (this.refDropzone) {
            this.refDropzone.addEventListener('dragover', function (e) {
                e.preventDefault();
                e.stopPropagation();
                self.refDropzone.classList.add('drag-over');
            });
            this.refDropzone.addEventListener('dragleave', function (e) {
                e.preventDefault();
                e.stopPropagation();
                self.refDropzone.classList.remove('drag-over');
            });
            this.refDropzone.addEventListener('drop', function (e) {
                e.preventDefault();
                e.stopPropagation();
                self.refDropzone.classList.remove('drag-over');
                self._handleReferenceFiles(e.dataTransfer.files);
            });
            this.refDropzone.addEventListener('click', function () {
                if (self.refFileInput) self.refFileInput.click();
            });
        }

        if (this.refFileInput) {
            this.refFileInput.addEventListener('change', function () {
                if (self.refFileInput.files.length > 0) {
                    self._handleReferenceFiles(self.refFileInput.files);
                }
                self.refFileInput.value = '';
            });
        }

        // Upload more button
        if (this.btnUploadMore) {
            this.btnUploadMore.addEventListener('click', function () {
                if (self.refFileInputExtra) self.refFileInputExtra.click();
            });
        }

        if (this.refFileInputExtra) {
            this.refFileInputExtra.addEventListener('change', function () {
                if (self.refFileInputExtra.files.length > 0) {
                    self._handleReferenceFiles(self.refFileInputExtra.files);
                }
                self.refFileInputExtra.value = '';
            });
        }

        // Copy-to-snapshot buttons
        if (this.btnCopyWriterToSnapshot) {
            this.btnCopyWriterToSnapshot.addEventListener('click', function () {
                self._copyHighlightedToField('original');
            });
        }
        if (this.btnCopyPfToSnapshot) {
            this.btnCopyPfToSnapshot.addEventListener('click', function () {
                self._copyHighlightedToField('pageforge');
            });
        }
        if (this.btnCopyHumanToSnapshot) {
            this.btnCopyHumanToSnapshot.addEventListener('click', function () {
                self._copyHighlightedToField('human');
            });
        }

        // PageForge iframe click handler (for sync mode)
        if (this.pageforgeIframe) {
            this.pageforgeIframe.addEventListener('load', function () {
                self._attachIframeClickHandler(self.pageforgeIframe);
            });
        }
    }

    // ------------------------------------------------------------------
    // Calibration manager initialisation
    // ------------------------------------------------------------------

    _initCalibrationManager() {
        var self = this;
        this.calibrationManager = new CalibrationManager({
            showToast: function (msg) { self.showToast(msg); },
            getModuleCode: function () {
                return (self.data && self.data.metadata && self.data.metadata.moduleCode) || '';
            },
            getTemplateName: function () {
                return (self.data && self.data.templateName) || '';
            },
            getGeneratedFileList: function () {
                return (self.data && self.data.generatedFileList) || [];
            }
        });
        this.calibrationManager.init();

        // Populate the source file dropdown
        if (this.data && this.data.generatedFileList) {
            this.calibrationManager.populateSourceFileDropdown();
        }
    }

    // ------------------------------------------------------------------
    // Initial rendering
    // ------------------------------------------------------------------

    _render() {
        if (!this.data) {
            this._showNoDataMessage();
            return;
        }

        // Show module code
        if (this.moduleCodeDisplay && this.data.metadata && this.data.metadata.moduleCode) {
            this.moduleCodeDisplay.textContent = 'Module: ' + this.data.metadata.moduleCode;
        }

        // Render file map
        this._renderFileMap();

        // Render uploaded reference files list
        this._renderRefFileList();

        // Auto-select first file
        if (this.data.generatedFileList && this.data.generatedFileList.length > 0) {
            this._selectFile(this.data.generatedFileList[0]);
        }
    }

    /**
     * Show message when no data available.
     */
    _showNoDataMessage() {
        if (this.fileMapList) {
            this.fileMapList.innerHTML = '<p class="file-map-empty">No data available. '
                + 'Please process a document in PageForge first, then click '
                + '"Visual Comparison Review".</p>';
        }
    }

    // ------------------------------------------------------------------
    // File map rendering
    // ------------------------------------------------------------------

    _renderFileMap() {
        if (!this.fileMapList || !this.data) return;

        var self = this;
        var html = '';

        for (var i = 0; i < this.data.generatedFileList.length; i++) {
            var filename = this.data.generatedFileList[i];
            var pageData = this._getPageData(filename);
            var typeLabel = '';
            if (pageData) {
                typeLabel = pageData.type === 'overview' ? 'Overview' : 'Lesson ' + pageData.lessonNumber;
            }
            var hasRef = this._hasMatchingReference(filename);

            html += '<div class="file-map-entry" data-filename="' + this._esc(filename) + '" tabindex="0" role="button">';
            html += '<span class="file-map-name">' + this._esc(filename) + '</span>';
            html += '<span class="file-map-type">' + this._esc(typeLabel) + '</span>';
            if (hasRef) {
                html += '<span class="file-map-ref-badge" title="Human reference available">REF</span>';
            }
            html += '</div>';
        }

        this.fileMapList.innerHTML = html;

        // Bind click handlers
        var entries = this.fileMapList.querySelectorAll('.file-map-entry');
        for (var j = 0; j < entries.length; j++) {
            entries[j].addEventListener('click', function () {
                var fn = this.getAttribute('data-filename');
                self._selectFile(fn);
            });
            entries[j].addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    var fn = this.getAttribute('data-filename');
                    self._selectFile(fn);
                }
            });
        }
    }

    // ------------------------------------------------------------------
    // File selection
    // ------------------------------------------------------------------

    /**
     * Select a file and update all three panels.
     * @param {string} filename
     */
    _selectFile(filename) {
        this.selectedFile = filename;
        this.highlightedBlockIndex = null;
        this._hideCopyToSnapshotButtons();

        // Update file map highlight
        var entries = this.fileMapList.querySelectorAll('.file-map-entry');
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].getAttribute('data-filename') === filename) {
                entries[i].classList.add('selected');
            } else {
                entries[i].classList.remove('selected');
            }
        }

        // Update all three panels
        this._loadPageforgePanel(filename);
        this._loadHumanPanel(filename);
        this._loadWriterPanel(filename);
    }

    // ------------------------------------------------------------------
    // PageForge panel
    // ------------------------------------------------------------------

    _loadPageforgePanel(filename) {
        if (this.pageforgeFilename) {
            this.pageforgeFilename.textContent = filename;
        }

        var htmlContent = this.data.generatedHtmlFiles[filename];
        if (!htmlContent) {
            if (this.pageforgeIframe) this.pageforgeIframe.srcdoc = '<p>No content available</p>';
            return;
        }

        // Annotate HTML with data-pf-block attributes for sync mode
        var annotated = this._annotateHtml(htmlContent, filename);

        if (this.rawHtmlMode) {
            this._showRawHtml('pageforge', htmlContent);
        } else {
            if (this.pageforgeIframe) {
                this.pageforgeIframe.classList.remove('hidden');
                this.pageforgeIframe.srcdoc = annotated;
            }
            if (this.pageforgeRaw) this.pageforgeRaw.classList.add('hidden');
        }
    }

    // ------------------------------------------------------------------
    // Human reference panel
    // ------------------------------------------------------------------

    _loadHumanPanel(filename) {
        if (this.humanFilename) {
            this.humanFilename.textContent = filename;
        }

        var refFile = this._findReference(filename);

        if (refFile) {
            // Has matching reference — show iframe
            if (this.humanUploadPrompt) this.humanUploadPrompt.classList.add('hidden');
            if (this.humanNoMatchMsg) this.humanNoMatchMsg.classList.add('hidden');
            if (this.btnUploadMore) this.btnUploadMore.classList.remove('hidden');

            if (this.rawHtmlMode) {
                this._showRawHtml('human', refFile.content);
            } else {
                if (this.humanIframe) {
                    this.humanIframe.classList.remove('hidden');
                    this.humanIframe.srcdoc = refFile.content;
                }
                if (this.humanRaw) this.humanRaw.classList.add('hidden');
            }
        } else {
            // No matching reference — show upload prompt
            if (this.humanIframe) this.humanIframe.classList.add('hidden');
            if (this.humanRaw) this.humanRaw.classList.add('hidden');
            if (this.humanUploadPrompt) this.humanUploadPrompt.classList.remove('hidden');

            if (this.humanReferenceFiles.length > 0) {
                // Files uploaded but none match this filename
                if (this.humanNoMatchMsg) {
                    this.humanNoMatchMsg.textContent = 'No matching human reference file uploaded for ' + filename;
                    this.humanNoMatchMsg.classList.remove('hidden');
                }
            } else {
                if (this.humanNoMatchMsg) this.humanNoMatchMsg.classList.add('hidden');
            }
            if (this.btnUploadMore) this.btnUploadMore.classList.remove('hidden');
        }
    }

    // ------------------------------------------------------------------
    // Writer template panel
    // ------------------------------------------------------------------

    _loadWriterPanel(filename) {
        if (this.writerFilename) {
            this.writerFilename.textContent = filename;
        }

        if (!this.writerContent) return;

        var pageData = this._getPageData(filename);
        if (!pageData || !pageData.contentBlockTexts || pageData.contentBlockTexts.length === 0) {
            this.writerContent.innerHTML = '<p class="review-no-content">No parsed content available for this page.</p>';
            return;
        }

        var html = '';
        for (var i = 0; i < pageData.contentBlockTexts.length; i++) {
            var blockText = pageData.contentBlockTexts[i];
            if (!blockText || !blockText.trim()) continue;

            html += '<div class="writer-block" data-block-index="' + i + '">';
            html += '<span class="writer-block-index">#' + i + '</span>';
            html += '<pre class="writer-block-text">' + this._esc(blockText) + '</pre>';
            html += '</div>';
        }

        this.writerContent.innerHTML = html || '<p class="review-no-content">No content blocks found.</p>';
    }

    // ------------------------------------------------------------------
    // HTML annotation for sync mode
    // ------------------------------------------------------------------

    /**
     * Annotate generated HTML with data-pf-block attributes by wrapping
     * children of <div id="body"> with block index markers.
     *
     * @param {string} htmlContent - Raw HTML string
     * @param {string} filename - Current filename for page data lookup
     * @returns {string} Annotated HTML string
     */
    _annotateHtml(htmlContent, filename) {
        try {
            var parser = new DOMParser();
            var doc = parser.parseFromString(htmlContent, 'text/html');
            var bodyDiv = doc.getElementById('body');

            if (bodyDiv) {
                var children = bodyDiv.children;
                for (var i = 0; i < children.length; i++) {
                    children[i].setAttribute('data-pf-block', String(i));
                }
            }

            // Also annotate module menu content if present
            var menuContent = doc.getElementById('module-menu-content');
            if (menuContent) {
                menuContent.setAttribute('data-pf-block', 'menu');
            }

            // Inject highlight style into the document
            var style = doc.createElement('style');
            style.textContent = '.pf-sync-highlight { outline: 3px solid #f59e0b !important; '
                + 'background-color: rgba(245, 158, 11, 0.15) !important; '
                + 'transition: outline 0.3s, background-color 0.3s; }';
            doc.head.appendChild(style);

            // Serialise back
            return '<!doctype html>' + doc.documentElement.outerHTML;
        } catch (e) {
            // If annotation fails, return original
            return htmlContent;
        }
    }

    // ------------------------------------------------------------------
    // Sync mode — iframe click handling
    // ------------------------------------------------------------------

    /**
     * Attach click handler to iframe content document for sync mode.
     * @param {HTMLIFrameElement} iframe
     */
    _attachIframeClickHandler(iframe) {
        var self = this;
        try {
            var doc = iframe.contentDocument || iframe.contentWindow.document;
            doc.addEventListener('click', function (e) {
                if (!self.syncModeEnabled) return;

                e.preventDefault();

                // Find nearest ancestor with data-pf-block attribute
                var target = e.target;
                while (target && target !== doc.body) {
                    var blockAttr = target.getAttribute ? target.getAttribute('data-pf-block') : null;
                    if (blockAttr !== null) {
                        var blockIndex = blockAttr === 'menu' ? 'menu' : parseInt(blockAttr, 10);
                        self._syncToBlock(blockIndex, target);
                        return;
                    }
                    target = target.parentElement;
                }
            });
        } catch (e) {
            // Cross-origin restriction or iframe not ready
            console.warn('ReviewApp: Could not attach iframe click handler:', e.message);
        }
    }

    /**
     * Synchronise all panels to a specific block index.
     * @param {number|string} blockIndex
     * @param {HTMLElement} clickedElement - The element clicked in the PageForge iframe
     */
    _syncToBlock(blockIndex, clickedElement) {
        this.highlightedBlockIndex = blockIndex;

        // Highlight in PageForge iframe
        this._highlightInIframe(this.pageforgeIframe, blockIndex);

        // Sync Writer Template panel
        this._syncWriterPanel(blockIndex);

        // Sync Human Reference panel
        if (clickedElement) {
            var textSnippet = (clickedElement.textContent || '').trim().substring(0, 100);
            this._syncHumanPanel(textSnippet);
        }

        // Show copy-to-snapshot buttons
        this._showCopyToSnapshotButtons();
    }

    /**
     * Highlight a block in an iframe by data-pf-block attribute.
     * @param {HTMLIFrameElement} iframe
     * @param {number|string} blockIndex
     */
    _highlightInIframe(iframe, blockIndex) {
        try {
            var doc = iframe.contentDocument || iframe.contentWindow.document;

            // Remove previous highlights
            var prev = doc.querySelectorAll('.pf-sync-highlight');
            for (var i = 0; i < prev.length; i++) {
                prev[i].classList.remove('pf-sync-highlight');
            }

            // Add highlight to matching block
            var target = doc.querySelector('[data-pf-block="' + blockIndex + '"]');
            if (target) {
                target.classList.add('pf-sync-highlight');
                target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } catch (e) {
            // Ignore cross-origin errors
        }
    }

    /**
     * Scroll the Writer Template panel to the matching block.
     * @param {number|string} blockIndex
     */
    _syncWriterPanel(blockIndex) {
        if (!this.writerContent) return;

        // Remove previous highlights
        var prev = this.writerContent.querySelectorAll('.writer-block-highlight');
        for (var i = 0; i < prev.length; i++) {
            prev[i].classList.remove('writer-block-highlight');
        }

        var target = this.writerContent.querySelector('[data-block-index="' + blockIndex + '"]');
        if (target) {
            target.classList.add('writer-block-highlight');
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Auto-remove highlight after 3 seconds
            setTimeout(function () {
                target.classList.remove('writer-block-highlight');
            }, 3000);
        }
    }

    /**
     * Find and scroll to matching content in the Human Reference iframe.
     * Uses fuzzy text matching.
     * @param {string} textSnippet
     */
    _syncHumanPanel(textSnippet) {
        if (!this.humanIframe || this.humanIframe.classList.contains('hidden')) return;
        if (!textSnippet || textSnippet.length < 5) return;

        try {
            var doc = this.humanIframe.contentDocument || this.humanIframe.contentWindow.document;

            // Remove previous highlights
            var prev = doc.querySelectorAll('.pf-sync-highlight');
            for (var i = 0; i < prev.length; i++) {
                prev[i].classList.remove('pf-sync-highlight');
            }

            // Find best matching element using text similarity
            var bestMatch = null;
            var bestScore = 0;
            var searchText = textSnippet.toLowerCase().replace(/\s+/g, ' ');

            // Walk meaningful content elements
            var elements = doc.querySelectorAll('h1, h2, h3, h4, h5, p, div, li, td, th, span');
            for (var i = 0; i < elements.length; i++) {
                var el = elements[i];
                var elText = (el.textContent || '').toLowerCase().replace(/\s+/g, ' ').trim();
                if (!elText || elText.length < 3) continue;

                var score = this._textSimilarity(searchText, elText);
                if (score > bestScore) {
                    bestScore = score;
                    bestMatch = el;
                }
            }

            if (bestMatch && bestScore > 0.3) {
                // Inject highlight style if not already present
                if (!doc.getElementById('pf-sync-style')) {
                    var style = doc.createElement('style');
                    style.id = 'pf-sync-style';
                    style.textContent = '.pf-sync-highlight { outline: 3px solid #f59e0b !important; '
                        + 'background-color: rgba(245, 158, 11, 0.15) !important; '
                        + 'transition: outline 0.3s, background-color 0.3s; }';
                    doc.head.appendChild(style);
                }

                bestMatch.classList.add('pf-sync-highlight');
                bestMatch.scrollIntoView({ behavior: 'smooth', block: 'center' });

                // Auto-remove highlight after 3 seconds
                setTimeout(function () {
                    bestMatch.classList.remove('pf-sync-highlight');
                }, 3000);
            } else {
                this.showToast('No matching content found in human reference file');
            }
        } catch (e) {
            // Ignore cross-origin errors
        }
    }

    /**
     * Calculate text similarity score between two strings (0-1).
     * Uses substring overlap scoring.
     * @param {string} search
     * @param {string} target
     * @returns {number}
     */
    _textSimilarity(search, target) {
        if (!search || !target) return 0;

        // Exact match
        if (search === target) return 1;

        // Check substring containment
        if (target.indexOf(search) !== -1) return 0.9;
        if (search.indexOf(target) !== -1) return 0.8;

        // Word overlap score
        var searchWords = search.split(/\s+/).filter(function (w) { return w.length > 2; });
        var targetWords = target.split(/\s+/).filter(function (w) { return w.length > 2; });

        if (searchWords.length === 0) return 0;

        var matches = 0;
        for (var i = 0; i < searchWords.length; i++) {
            for (var j = 0; j < targetWords.length; j++) {
                if (searchWords[i] === targetWords[j]) {
                    matches++;
                    break;
                }
            }
        }

        return matches / searchWords.length;
    }

    // ------------------------------------------------------------------
    // Raw HTML toggle
    // ------------------------------------------------------------------

    _toggleRawHtmlMode() {
        if (this.rawHtmlMode) {
            this.btnRawHtmlToggle.classList.add('review-raw-btn-active');
        } else {
            this.btnRawHtmlToggle.classList.remove('review-raw-btn-active');
        }

        if (this.selectedFile) {
            this._loadPageforgePanel(this.selectedFile);
            this._loadHumanPanel(this.selectedFile);
        }
    }

    /**
     * Show raw HTML in a panel's raw view.
     * @param {string} panel - 'pageforge' or 'human'
     * @param {string} htmlContent
     */
    _showRawHtml(panel, htmlContent) {
        if (panel === 'pageforge') {
            if (this.pageforgeIframe) this.pageforgeIframe.classList.add('hidden');
            if (this.pageforgeRaw) {
                this.pageforgeRaw.classList.remove('hidden');
                if (this.pageforgeRawCode) {
                    this.pageforgeRawCode.textContent = htmlContent;
                }
            }
        } else if (panel === 'human') {
            if (this.humanIframe) this.humanIframe.classList.add('hidden');
            if (this.humanRaw) {
                this.humanRaw.classList.remove('hidden');
                if (this.humanRawCode) {
                    this.humanRawCode.textContent = htmlContent;
                }
            }
        }
    }

    // ------------------------------------------------------------------
    // Sync mode indicator
    // ------------------------------------------------------------------

    _updateSyncModeIndicator() {
        var pfPanel = document.getElementById('panel-pageforge');
        if (pfPanel) {
            if (this.syncModeEnabled) {
                pfPanel.classList.add('review-sync-active');
            } else {
                pfPanel.classList.remove('review-sync-active');
            }
        }
    }

    // ------------------------------------------------------------------
    // Copy-to-snapshot buttons
    // ------------------------------------------------------------------

    _showCopyToSnapshotButtons() {
        if (this.btnCopyWriterToSnapshot) this.btnCopyWriterToSnapshot.classList.remove('hidden');
        if (this.btnCopyPfToSnapshot) this.btnCopyPfToSnapshot.classList.remove('hidden');
        if (this.btnCopyHumanToSnapshot && this._findReference(this.selectedFile)) {
            this.btnCopyHumanToSnapshot.classList.remove('hidden');
        }
    }

    _hideCopyToSnapshotButtons() {
        if (this.btnCopyWriterToSnapshot) this.btnCopyWriterToSnapshot.classList.add('hidden');
        if (this.btnCopyPfToSnapshot) this.btnCopyPfToSnapshot.classList.add('hidden');
        if (this.btnCopyHumanToSnapshot) this.btnCopyHumanToSnapshot.classList.add('hidden');
    }

    /**
     * Copy the highlighted block's content to a snapshot form field.
     * @param {string} field - 'original', 'pageforge', or 'human'
     */
    _copyHighlightedToField(field) {
        var content = '';
        var blockIndex = this.highlightedBlockIndex;

        if (field === 'original') {
            // Get writer template content for this block
            var pageData = this._getPageData(this.selectedFile);
            if (pageData && pageData.contentBlockTexts && blockIndex !== null && blockIndex !== 'menu') {
                content = pageData.contentBlockTexts[blockIndex] || '';
            }
        } else if (field === 'pageforge') {
            // Get the HTML of the highlighted block from the PageForge iframe
            content = this._getHighlightedHtml(this.pageforgeIframe, blockIndex);
        } else if (field === 'human') {
            // Get the highlighted content from the Human Reference iframe
            content = this._getHighlightedHtml(this.humanIframe, null);
        }

        // Populate the form field
        var textarea;
        if (field === 'original') {
            textarea = document.getElementById('snapshot-original');
        } else if (field === 'pageforge') {
            textarea = document.getElementById('snapshot-pageforge');
        } else if (field === 'human') {
            textarea = document.getElementById('snapshot-human');
        }

        if (textarea && content) {
            textarea.value = content;
            textarea.dispatchEvent(new Event('input'));
            this.showToast('Content copied to snapshot field');
        } else if (!content) {
            this.showToast('No highlighted content to copy');
        }
    }

    /**
     * Get the outerHTML of the currently highlighted element in an iframe.
     * @param {HTMLIFrameElement} iframe
     * @param {number|string|null} blockIndex
     * @returns {string}
     */
    _getHighlightedHtml(iframe, blockIndex) {
        try {
            var doc = iframe.contentDocument || iframe.contentWindow.document;
            var highlighted = doc.querySelector('.pf-sync-highlight');
            if (highlighted) {
                return highlighted.outerHTML;
            }
            if (blockIndex !== null && blockIndex !== undefined) {
                var block = doc.querySelector('[data-pf-block="' + blockIndex + '"]');
                if (block) return block.outerHTML;
            }
        } catch (e) {
            // Ignore
        }
        return '';
    }

    // ------------------------------------------------------------------
    // Human reference file handling
    // ------------------------------------------------------------------

    /**
     * Handle uploaded reference files.
     * @param {FileList} files
     */
    _handleReferenceFiles(files) {
        var self = this;

        for (var i = 0; i < files.length; i++) {
            var file = files[i];

            // Validate .html extension
            if (!file.name.toLowerCase().endsWith('.html')) {
                this.showToast('Rejected "' + file.name + '" — only .html files accepted');
                continue;
            }

            // Avoid duplicates
            var alreadyUploaded = false;
            for (var j = 0; j < this.humanReferenceFiles.length; j++) {
                if (this.humanReferenceFiles[j].filename === file.name) {
                    alreadyUploaded = true;
                    break;
                }
            }
            if (alreadyUploaded) continue;

            // Read file content
            (function (f) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    var matched = self.data && self.data.generatedFileList
                        ? self.data.generatedFileList.indexOf(f.name) !== -1
                        : false;
                    self.humanReferenceFiles.push({
                        filename: f.name,
                        content: e.target.result,
                        size: f.size,
                        matchedToGenerated: matched
                    });
                    self._renderRefFileList();
                    self._renderFileMap();

                    // If the current file now has a reference, reload
                    if (self.selectedFile === f.name) {
                        self._loadHumanPanel(f.name);
                    }

                    self.showToast('Uploaded ' + f.name);
                };
                reader.readAsText(f);
            })(file);
        }
    }

    /**
     * Render the uploaded reference files list.
     */
    _renderRefFileList() {
        if (!this.refUploaded) return;

        if (this.humanReferenceFiles.length === 0) {
            this.refUploaded.innerHTML = '';
            return;
        }

        var self = this;
        var html = '';
        for (var i = 0; i < this.humanReferenceFiles.length; i++) {
            var file = this.humanReferenceFiles[i];
            var sizeStr = this._formatFileSize(file.size);
            var statusClass = file.matchedToGenerated ? 'calibration-file-matched' : 'calibration-file-unmatched';
            var statusText = file.matchedToGenerated ? 'Matched' : 'Unmatched';

            html += '<div class="calibration-file-item" data-index="' + i + '">';
            html += '<span class="calibration-file-name">' + this._esc(file.filename) + '</span>';
            html += '<span class="calibration-file-size">' + sizeStr + '</span>';
            html += '<span class="' + statusClass + '">' + statusText + '</span>';
            html += '<button class="btn btn-sm calibration-file-remove" type="button" '
                + 'data-index="' + i + '" title="Remove">&#10005;</button>';
            html += '</div>';
        }

        this.refUploaded.innerHTML = html;

        // Bind remove buttons
        var removeBtns = this.refUploaded.querySelectorAll('.calibration-file-remove');
        for (var j = 0; j < removeBtns.length; j++) {
            removeBtns[j].addEventListener('click', function (e) {
                e.stopPropagation();
                var idx = parseInt(this.getAttribute('data-index'), 10);
                if (idx >= 0 && idx < self.humanReferenceFiles.length) {
                    var removed = self.humanReferenceFiles.splice(idx, 1);
                    self._renderRefFileList();
                    self._renderFileMap();
                    if (self.selectedFile) self._loadHumanPanel(self.selectedFile);
                    self.showToast('Removed ' + removed[0].filename);
                }
            });
        }
    }

    // ------------------------------------------------------------------
    // Data lookup helpers
    // ------------------------------------------------------------------

    /**
     * Get page data for a given filename.
     * @param {string} filename
     * @returns {Object|null}
     */
    _getPageData(filename) {
        if (!this.data || !this.data.pageData) return null;
        for (var i = 0; i < this.data.pageData.length; i++) {
            if (this.data.pageData[i].filename === filename) {
                return this.data.pageData[i];
            }
        }
        return null;
    }

    /**
     * Find a matching human reference file by filename.
     * @param {string} filename
     * @returns {Object|null}
     */
    _findReference(filename) {
        for (var i = 0; i < this.humanReferenceFiles.length; i++) {
            if (this.humanReferenceFiles[i].filename === filename) {
                return this.humanReferenceFiles[i];
            }
        }
        return null;
    }

    /**
     * Check if a matching reference file exists.
     * @param {string} filename
     * @returns {boolean}
     */
    _hasMatchingReference(filename) {
        return this._findReference(filename) !== null;
    }

    // ------------------------------------------------------------------
    // Toast notification
    // ------------------------------------------------------------------

    showToast(message) {
        if (!this.toast) return;
        this.toast.textContent = message;
        this.toast.classList.add('visible');

        var self = this;
        clearTimeout(this._toastTimer);
        this._toastTimer = setTimeout(function () {
            self.toast.classList.remove('visible');
        }, 3000);
    }

    // ------------------------------------------------------------------
    // Utility helpers
    // ------------------------------------------------------------------

    _esc(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    _formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
}

// ------------------------------------------------------------------
// Boot
// ------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    window.reviewApp = new ReviewApp();
});
