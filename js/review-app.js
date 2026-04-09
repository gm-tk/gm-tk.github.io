/**
 * ReviewApp — Controller for the Visual Comparison Review page.
 *
 * Handles data deserialisation from sessionStorage, three-panel rendering,
 * file map interaction, template-aware CSS injection for rendered HTML,
 * synchronised scrolling with 6-tier intelligent content matching (Sync Mode),
 * Raw HTML toggle, human reference file upload, "Copy to Snapshot" buttons
 * that save to sessionStorage for the standalone Conversion Error Log page, and
 * a Conversion Error Log button that opens calibrate.html.
 *
 * This is a standalone controller for review.html — it does not depend on
 * App, DocxParser, CalibrationManager, or any other main-page class. It
 * loads its data from sessionStorage (serialised by App._serialiseForReview()).
 */

'use strict';

// -----------------------------------------------------------------------
// Template-to-CSS Mapping for iframe rendering
// -----------------------------------------------------------------------

var CSS_MAPPING = {
    '1-3': { stylesheets: [
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/colourSchemes/1-3.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/styles.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/bootstrap.min.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/bsReset.css'
    ]},
    '4-6': { stylesheets: [
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/4-6.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/styles.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bootstrap.min.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bsReset.css'
    ]},
    '7-8': { stylesheets: [
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/7-8.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/styles.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bootstrap.min.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bsReset.css'
    ]},
    '9-10': { stylesheets: [
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/9-10.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/styles.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bootstrap.min.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bsReset.css'
    ]},
    'NCEA': { stylesheets: [
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/colourSchemes/NCEA.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/styles.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/bootstrap.min.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/bsReset.css'
    ]},
    'combo': { stylesheets: [
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/colourSchemes/combo.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/styles.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/bootstrap.min.css',
        'https://tekuradev.desire2learn.com/shared/refresh_template/css/bsReset.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/combo.css'
    ]},
    'ECH': { stylesheets: [
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/ECH.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/styles.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bootstrap.min.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bsReset.css'
    ]},
    'inquiry': { stylesheets: [
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/_colourSchemes.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/colourSchemes/inquiry.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/styles.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bootstrap.min.css',
        'https://tekura.desire2learn.com/shared/refresh_template/css/bsReset.css'
    ]}
};

// -----------------------------------------------------------------------
// ReviewApp Class
// -----------------------------------------------------------------------

class ReviewApp {
    constructor() {
        /** Deserialised data from main page */
        this.data = null;

        /** Human reference files uploaded on this page */
        this.humanReferenceFiles = [];

        /** Currently selected filename */
        this.selectedFile = null;

        /** Sync mode enabled flag */
        this.syncModeEnabled = false;

        /** Raw HTML mode enabled flag */
        this.rawHtmlMode = false;

        /** Currently highlighted block index (for copy-to-snapshot) */
        this.highlightedBlockIndex = null;

        /** Guard flag to prevent scroll feedback loops */
        this._scrollSyncLock = false;

        this._loadData();
        this._bindElements();
        this._bindEvents();
        this._bindScrollSync();
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
        this.btnCalibrationTool = document.getElementById('btn-calibration-tool');
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
        this.writerPanelBody = document.getElementById('writer-panel-body');

        // Panel body containers (for scroll sync)
        this.pageforgePanelBody = document.getElementById('pageforge-panel-body');
        this.humanPanelBody = document.getElementById('human-panel-body');

        // Copy-to-snapshot buttons
        this.btnCopyPf = document.getElementById('btn-copy-pf');
        this.btnCopyHuman = document.getElementById('btn-copy-human');
        this.btnCopyWt = document.getElementById('btn-copy-wt');

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

        // Conversion Error Log button
        if (this.btnCalibrationTool) {
            this.btnCalibrationTool.addEventListener('click', function () {
                self._openConversionErrorLog();
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

        // Copy-to-snapshot buttons (save to sessionStorage)
        if (this.btnCopyWt) {
            this.btnCopyWt.addEventListener('click', function () {
                self._copyToSessionStorage('wt');
            });
        }
        if (this.btnCopyPf) {
            this.btnCopyPf.addEventListener('click', function () {
                self._copyToSessionStorage('pf');
            });
        }
        if (this.btnCopyHuman) {
            this.btnCopyHuman.addEventListener('click', function () {
                self._copyToSessionStorage('human');
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
    // Conversion Error Log launcher
    // ------------------------------------------------------------------

    /**
     * Open the standalone Conversion Error Log page.
     * Serialises calibration-specific data to sessionStorage.
     */
    _openConversionErrorLog() {
        try {
            var calibData = {
                generatedFileList: (this.data && this.data.generatedFileList) || [],
                metadata: (this.data && this.data.metadata) || {},
                templateName: (this.data && this.data.templateName) || ''
            };
            sessionStorage.setItem('pageforge_calibrate_data', JSON.stringify(calibData));
            window.open('calibrate.html', '_blank');
        } catch (e) {
            console.error('ReviewApp: Failed to open conversion error log:', e);
            this.showToast('Failed to open conversion error log');
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
            this.moduleCodeDisplay.textContent = this.data.metadata.moduleCode;
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
                if (pageData.type === 'overview') {
                    typeLabel = 'OV';
                } else {
                    typeLabel = 'L' + pageData.lessonNumber;
                }
            }
            var hasRef = this._hasMatchingReference(filename);

            html += '<div class="file-map-entry" data-filename="' + this._esc(filename) + '" tabindex="0" role="button">';
            html += '<div class="file-map-entry-row">';
            html += '<span class="file-map-name">' + this._esc(filename) + '</span>';
            html += '<span class="file-map-type">' + this._esc(typeLabel) + '</span>';
            if (hasRef) {
                html += '<span class="file-map-ref-badge" title="Human reference available">REF</span>';
            }
            html += '</div>';
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
    // Template-aware CSS injection
    // ------------------------------------------------------------------

    /**
     * Inject LMS template CSS into HTML for rendered display in iframes.
     * Also removes the idoc_scripts.js script tag and injects sync highlight styles.
     *
     * @param {string} htmlString - Raw HTML string
     * @param {string|null} templateAttribute - Template attribute value (e.g., '4-6')
     * @returns {string} Modified HTML string with CSS injected
     */
    _injectCssForRendering(htmlString, templateAttribute) {
        // Detect template from HTML if not provided
        if (!templateAttribute) {
            var templateMatch = htmlString.match(/template\s*=\s*"([^"]+)"/);
            if (templateMatch) {
                templateAttribute = templateMatch[1];
            }
        }

        // Build link tags
        var linkTags = '';
        if (templateAttribute && CSS_MAPPING[templateAttribute]) {
            var sheets = CSS_MAPPING[templateAttribute].stylesheets;
            for (var i = 0; i < sheets.length; i++) {
                linkTags += '<link rel="stylesheet" href="' + sheets[i] + '" />\n';
            }
        }

        // Inject sync highlight style
        var syncStyle = '<style>.pf-sync-highlight { outline: 3px solid #f59e0b !important; '
            + 'background-color: rgba(245, 158, 11, 0.15) !important; '
            + 'transition: outline 0.3s, background-color 0.3s; }</style>\n';

        // Insert before </head>
        if (linkTags || syncStyle) {
            var headCloseIdx = htmlString.indexOf('</head>');
            if (headCloseIdx === -1) headCloseIdx = htmlString.indexOf('</HEAD>');
            if (headCloseIdx !== -1) {
                htmlString = htmlString.substring(0, headCloseIdx) + linkTags + syncStyle + htmlString.substring(headCloseIdx);
            }
        }

        // Remove idoc_scripts.js script tag
        htmlString = htmlString.replace(/<script[^>]*idoc_scripts\.js[^>]*><\/script>/gi, '');

        return htmlString;
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

        // Store raw content for raw HTML mode
        this._currentPageforgeHtml = htmlContent;

        // Annotate HTML with data-pf-block attributes for sync mode
        var annotated = this._annotateHtml(htmlContent, filename);

        // Inject template CSS for rendered view
        var templateAttr = (this.data && this.data.templateAttribute) || null;
        var injected = this._injectCssForRendering(annotated, templateAttr);

        if (this.rawHtmlMode) {
            this._showRawHtml('pageforge', htmlContent);
        } else {
            if (this.pageforgeIframe) {
                this.pageforgeIframe.classList.remove('hidden');
                this.pageforgeIframe.srcdoc = injected;
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

            // Store raw content for raw HTML mode
            this._currentHumanHtml = refFile.content;

            // Inject template CSS — detect from human file's own template attribute,
            // fall back to PageForge's template
            var templateAttr = null;
            var humanTemplateMatch = refFile.content.match(/template\s*=\s*"([^"]+)"/);
            if (humanTemplateMatch) {
                templateAttr = humanTemplateMatch[1];
            } else if (this.data) {
                templateAttr = this.data.templateAttribute || null;
            }
            var injected = this._injectCssForRendering(refFile.content, templateAttr);

            if (this.rawHtmlMode) {
                this._showRawHtml('human', refFile.content);
            } else {
                if (this.humanIframe) {
                    this.humanIframe.classList.remove('hidden');
                    this.humanIframe.srcdoc = injected;
                }
                if (this.humanRaw) this.humanRaw.classList.add('hidden');
            }
        } else {
            // No matching reference — show upload prompt
            this._currentHumanHtml = null;
            if (this.humanIframe) this.humanIframe.classList.add('hidden');
            if (this.humanRaw) this.humanRaw.classList.add('hidden');
            if (this.humanUploadPrompt) this.humanUploadPrompt.classList.remove('hidden');

            if (this.humanReferenceFiles.length > 0) {
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
     * Annotate generated HTML with data-pf-block and data-pf-activity
     * attributes for sync mode click detection.
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
                var blockIdx = 0;
                for (var i = 0; i < children.length; i++) {
                    var child = children[i];
                    child.setAttribute('data-pf-block', String(blockIdx));

                    // Annotate activity wrappers
                    var activityEl = child.querySelector('.activity[number]');
                    if (!activityEl && child.classList && child.classList.contains('activity')) {
                        activityEl = child;
                    }
                    if (activityEl && activityEl.getAttribute('number')) {
                        child.setAttribute('data-pf-activity', activityEl.getAttribute('number'));
                    }

                    // Also check for activity number in HTML comments
                    // (interactive placeholders use comments like Activity: 1A)
                    var childHtml = child.innerHTML || '';
                    var activityCommentMatch = childHtml.match(/Activity:\s*(\w+)/);
                    if (activityCommentMatch && !child.getAttribute('data-pf-activity')) {
                        child.setAttribute('data-pf-activity', activityCommentMatch[1]);
                    }

                    // Annotate inner elements for finer sync matching
                    var innerElements = child.querySelectorAll('h2, h3, h4, h5, p, ul, ol, div.whakatauki, div.videoSection, div.alert, div.hintSlider, img');
                    for (var j = 0; j < innerElements.length; j++) {
                        innerElements[j].setAttribute('data-pf-inner', blockIdx + '-' + j);
                    }

                    blockIdx++;
                }
            }

            // Also annotate structural elements
            var menuContent = doc.getElementById('module-menu-content');
            if (menuContent) {
                menuContent.setAttribute('data-pf-block', 'menu');
            }
            var header = doc.getElementById('header');
            if (header) {
                header.setAttribute('data-pf-block', 'header');
            }
            var footer = doc.getElementById('footer');
            if (footer) {
                footer.setAttribute('data-pf-block', 'footer');
            }

            // Serialise back
            return '<!doctype html>' + doc.documentElement.outerHTML;
        } catch (e) {
            return htmlContent;
        }
    }

    // ------------------------------------------------------------------
    // Sync mode — 6-Tier intelligent content matching
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
                        self._syncToBlock(blockAttr, target);
                        return;
                    }
                    target = target.parentElement;
                }
            });
        } catch (e) {
            console.warn('ReviewApp: Could not attach iframe click handler:', e.message);
        }
    }

    /**
     * Synchronise all panels to a specific block.
     * @param {string} blockIndex - Block index string from data-pf-block
     * @param {HTMLElement} clickedElement - The element clicked in the PageForge iframe
     */
    _syncToBlock(blockIndex, clickedElement) {
        this.highlightedBlockIndex = blockIndex;

        // Highlight in PageForge iframe
        this._highlightInIframe(this.pageforgeIframe, blockIndex);

        // Sync Writer Template panel (direct index match)
        this._syncWriterPanel(blockIndex);

        // Sync Human Reference panel using 6-tier matching
        this._syncHumanPanelIntelligent(clickedElement, blockIndex);

        // Show copy-to-snapshot buttons
        this._showCopyToSnapshotButtons();
    }

    /**
     * Highlight a block in an iframe by data-pf-block attribute.
     * @param {HTMLIFrameElement} iframe
     * @param {string} blockIndex
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
     * @param {string} blockIndex
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
     * Intelligent 6-tier content matching for the Human Reference panel.
     * Tries progressively less specific matching strategies.
     *
     * @param {HTMLElement} clickedElement - Element clicked in PageForge iframe
     * @param {string} blockIndex - Block index from data-pf-block
     */
    _syncHumanPanelIntelligent(clickedElement, blockIndex) {
        if (!this.humanIframe || this.humanIframe.classList.contains('hidden')) return;

        var doc;
        try {
            doc = this.humanIframe.contentDocument || this.humanIframe.contentWindow.document;
        } catch (e) {
            return;
        }

        // Ensure sync highlight style is injected
        if (!doc.getElementById('pf-sync-style')) {
            var style = doc.createElement('style');
            style.id = 'pf-sync-style';
            style.textContent = '.pf-sync-highlight { outline: 3px solid #f59e0b !important; '
                + 'background-color: rgba(245, 158, 11, 0.15) !important; '
                + 'transition: outline 0.3s, background-color 0.3s; }';
            doc.head.appendChild(style);
        }

        // Remove previous highlights
        var prev = doc.querySelectorAll('.pf-sync-highlight');
        for (var i = 0; i < prev.length; i++) {
            prev[i].classList.remove('pf-sync-highlight');
        }

        var matched = false;

        // --- Tier 1: Structural element matching ---
        if (!matched && clickedElement) {
            var structId = this._findStructuralId(clickedElement);
            if (structId) {
                var structEl = doc.getElementById(structId);
                if (structEl) {
                    this._highlightAndScroll(structEl);
                    matched = true;
                }
            }
        }

        // --- Tier 2: Activity number anchoring ---
        if (!matched && clickedElement) {
            var activityNum = this._extractActivityNumber(clickedElement);
            if (activityNum) {
                var actEl = doc.querySelector('[number="' + activityNum + '"]');
                if (actEl) {
                    this._highlightAndScroll(actEl);
                    matched = true;
                }
            }
        }

        // --- Tier 3: Heading text matching ---
        if (!matched && clickedElement) {
            var heading = this._extractHeadingText(clickedElement);
            if (heading) {
                var headingLower = heading.toLowerCase().trim();
                var headings = doc.querySelectorAll('h1, h2, h3, h4, h5');
                for (var hi = 0; hi < headings.length; hi++) {
                    var hText = (headings[hi].textContent || '').toLowerCase().trim();
                    if (hText === headingLower) {
                        this._highlightAndScroll(headings[hi]);
                        matched = true;
                        break;
                    }
                }
            }
        }

        // --- Tier 4: Word group matching ---
        if (!matched && clickedElement) {
            var visibleText = (clickedElement.textContent || '').trim();
            if (visibleText.length >= 10) {
                var wordGroups = this._extractWordGroups(visibleText, 4, 10);
                if (wordGroups.length > 0) {
                    var bestMatch = this._findByWordGroups(doc, wordGroups);
                    if (bestMatch) {
                        this._highlightAndScroll(bestMatch);
                        matched = true;
                    }
                }
            }
        }

        // --- Tier 5: Previous block anchoring ---
        if (!matched && clickedElement) {
            var pfDoc;
            try {
                pfDoc = this.pageforgeIframe.contentDocument || this.pageforgeIframe.contentWindow.document;
            } catch (e) {
                pfDoc = null;
            }

            if (pfDoc) {
                var currentIdx = parseInt(blockIndex, 10);
                if (!isNaN(currentIdx)) {
                    for (var bi = currentIdx - 1; bi >= 0 && bi >= currentIdx - 5; bi--) {
                        var prevBlock = pfDoc.querySelector('[data-pf-block="' + bi + '"]');
                        if (!prevBlock) continue;

                        // Try activity number
                        var prevActivity = this._extractActivityNumber(prevBlock);
                        if (prevActivity) {
                            var prevActEl = doc.querySelector('[number="' + prevActivity + '"]');
                            if (prevActEl) {
                                // Found anchor, offset forward
                                var nextSibling = prevActEl.parentElement;
                                while (nextSibling && nextSibling.nextElementSibling) {
                                    nextSibling = nextSibling.nextElementSibling;
                                    break;
                                }
                                if (nextSibling) {
                                    this._highlightAndScroll(nextSibling);
                                    matched = true;
                                }
                                break;
                            }
                        }

                        // Try heading text
                        var prevHeading = this._extractHeadingText(prevBlock);
                        if (prevHeading) {
                            var prevHeadingLower = prevHeading.toLowerCase().trim();
                            var allHeadings = doc.querySelectorAll('h1, h2, h3, h4, h5');
                            for (var phi = 0; phi < allHeadings.length; phi++) {
                                if ((allHeadings[phi].textContent || '').toLowerCase().trim() === prevHeadingLower) {
                                    // Found anchor, scroll to next sibling
                                    var anchorParent = allHeadings[phi].closest('.row') || allHeadings[phi].parentElement;
                                    if (anchorParent && anchorParent.nextElementSibling) {
                                        this._highlightAndScroll(anchorParent.nextElementSibling);
                                    } else {
                                        this._highlightAndScroll(allHeadings[phi]);
                                    }
                                    matched = true;
                                    break;
                                }
                            }
                            if (matched) break;
                        }
                    }
                }
            }
        }

        // --- Tier 6: Proportional position estimation ---
        if (!matched) {
            try {
                var pfBody = this.pageforgeIframe.contentDocument.getElementById('body');
                var humanBody = doc.getElementById('body');
                if (pfBody && humanBody && clickedElement) {
                    var pfScrollHeight = pfBody.scrollHeight || 1;
                    var clickedOffset = clickedElement.offsetTop || 0;
                    var proportion = clickedOffset / pfScrollHeight;
                    var humanScrollTarget = proportion * (humanBody.scrollHeight || 0);
                    humanBody.scrollTo({ top: humanScrollTarget, behavior: 'smooth' });
                }
            } catch (e) {
                // Fallback failed
            }

            if (!matched) {
                this.showToast('No matching content found in human reference');
            }
        }
    }

    /**
     * Highlight an element and scroll it into view with auto-remove.
     * @param {HTMLElement} element
     */
    _highlightAndScroll(element) {
        element.classList.add('pf-sync-highlight');
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });

        setTimeout(function () {
            element.classList.remove('pf-sync-highlight');
        }, 2000);
    }

    /**
     * Find the structural ID of the nearest structural ancestor.
     * @param {HTMLElement} el
     * @returns {string|null}
     */
    _findStructuralId(el) {
        var current = el;
        while (current) {
            var id = current.id;
            if (id === 'header' || id === 'footer' || id === 'module-menu-content') {
                return id;
            }
            current = current.parentElement;
        }
        return null;
    }

    /**
     * Extract activity number from an element or its ancestors.
     * @param {HTMLElement} el
     * @returns {string|null}
     */
    _extractActivityNumber(el) {
        var current = el;
        while (current) {
            // Check data-pf-activity attribute
            var pfActivity = current.getAttribute ? current.getAttribute('data-pf-activity') : null;
            if (pfActivity) return pfActivity;

            // Check number attribute on .activity
            var numAttr = current.getAttribute ? current.getAttribute('number') : null;
            if (numAttr) return numAttr;

            // Check for activity number in HTML comments
            if (current.innerHTML) {
                var commentMatch = current.innerHTML.match(/Activity:\s*(\w+)/);
                if (commentMatch) return commentMatch[1];
            }

            current = current.parentElement;
        }
        return null;
    }

    /**
     * Extract heading text if element is or contains a heading.
     * @param {HTMLElement} el
     * @returns {string|null}
     */
    _extractHeadingText(el) {
        // Check if element itself is a heading
        var tag = (el.tagName || '').toLowerCase();
        if (/^h[2-5]$/.test(tag)) {
            return el.textContent;
        }
        // Check child headings
        var heading = el.querySelector('h2, h3, h4, h5');
        if (heading) {
            return heading.textContent;
        }
        return null;
    }

    /**
     * Extract word groups (n-grams) from text for matching.
     * @param {string} text
     * @param {number} groupSize - Words per group
     * @param {number} maxGroups - Maximum groups to return
     * @returns {Array<string>}
     */
    _extractWordGroups(text, groupSize, maxGroups) {
        // Filter out stop words
        var stopWords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'is', 'it', 'by', 'as', 'be', 'if', 'so', 'no', 'up', 'do'];

        var words = text.toLowerCase().split(/\s+/).filter(function (w) {
            return w.length > 2 && stopWords.indexOf(w) === -1;
        });

        if (words.length < groupSize) {
            return words.length > 0 ? [words.join(' ')] : [];
        }

        var groups = [];
        var step = Math.max(1, Math.floor((words.length - groupSize) / (maxGroups - 1)));

        for (var i = 0; i <= words.length - groupSize && groups.length < maxGroups; i += step) {
            groups.push(words.slice(i, i + groupSize).join(' '));
        }

        return groups;
    }

    /**
     * Find the best matching element in a document using word groups.
     * @param {Document} doc
     * @param {Array<string>} wordGroups
     * @returns {HTMLElement|null}
     */
    _findByWordGroups(doc, wordGroups) {
        var elements = doc.querySelectorAll('p, h2, h3, h4, h5, li, td, th, div');
        var bestMatch = null;
        var bestScore = 0;

        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            var elText = (el.textContent || '').toLowerCase();
            if (elText.length < 5) continue;

            var score = 0;
            for (var g = 0; g < wordGroups.length; g++) {
                if (elText.indexOf(wordGroups[g]) !== -1) {
                    score++;
                }
            }

            if (score > bestScore && score >= 2) {
                bestScore = score;
                bestMatch = el;
            }
        }

        return bestMatch;
    }

    // ------------------------------------------------------------------
    // Proportional scroll sync
    // ------------------------------------------------------------------

    /**
     * Bind scroll event handlers to all three panel containers.
     * When Sync mode is ON, scrolling any panel proportionally scrolls the others.
     * Uses a lock flag to prevent feedback loops.
     */
    _bindScrollSync() {
        var self = this;

        // Debounce helper — returns a function that only fires after `delay` ms of inactivity
        function debounce(fn, delay) {
            var timer = null;
            return function () {
                var args = arguments;
                var ctx = this;
                if (timer) clearTimeout(timer);
                timer = setTimeout(function () { fn.apply(ctx, args); }, delay);
            };
        }

        /**
         * Get the scrollable element for a given panel, depending on current view mode.
         * For rendered view: the iframe's contentDocument scrolling element.
         * For raw HTML view: the .review-raw-view container.
         * For writer panel: the .review-writer-body container.
         */
        function getScrollable(panel) {
            if (panel === 'pageforge') {
                if (self.rawHtmlMode && self.pageforgeRaw && !self.pageforgeRaw.classList.contains('hidden')) {
                    return self.pageforgeRaw;
                }
                try {
                    if (self.pageforgeIframe && !self.pageforgeIframe.classList.contains('hidden')) {
                        var doc = self.pageforgeIframe.contentDocument || self.pageforgeIframe.contentWindow.document;
                        return doc.scrollingElement || doc.documentElement;
                    }
                } catch (e) { /* cross-origin */ }
                return null;
            } else if (panel === 'human') {
                if (self.rawHtmlMode && self.humanRaw && !self.humanRaw.classList.contains('hidden')) {
                    return self.humanRaw;
                }
                try {
                    if (self.humanIframe && !self.humanIframe.classList.contains('hidden')) {
                        var doc = self.humanIframe.contentDocument || self.humanIframe.contentWindow.document;
                        return doc.scrollingElement || doc.documentElement;
                    }
                } catch (e) { /* cross-origin */ }
                return null;
            } else if (panel === 'writer') {
                return self.writerPanelBody || null;
            }
            return null;
        }

        /**
         * Get scroll fraction (0..1) for a scrollable element.
         */
        function getScrollFraction(el) {
            if (!el) return 0;
            var maxScroll = el.scrollHeight - el.clientHeight;
            if (maxScroll <= 0) return 0;
            return el.scrollTop / maxScroll;
        }

        /**
         * Set scroll fraction for a scrollable element.
         */
        function setScrollFraction(el, fraction) {
            if (!el) return;
            var maxScroll = el.scrollHeight - el.clientHeight;
            if (maxScroll <= 0) return;
            el.scrollTop = fraction * maxScroll;
        }

        /**
         * Handle scroll from a source panel — sync other two panels.
         */
        function onPanelScroll(sourcePanel) {
            if (!self.syncModeEnabled) return;
            if (self._scrollSyncLock) return;

            self._scrollSyncLock = true;

            var sourceEl = getScrollable(sourcePanel);
            if (!sourceEl) { self._scrollSyncLock = false; return; }

            var fraction = getScrollFraction(sourceEl);
            var panels = ['pageforge', 'human', 'writer'];

            for (var i = 0; i < panels.length; i++) {
                if (panels[i] === sourcePanel) continue;
                var targetEl = getScrollable(panels[i]);
                if (targetEl) {
                    setScrollFraction(targetEl, fraction);
                }
            }

            // Release lock after a short delay to allow programmatic scrolls to settle
            setTimeout(function () { self._scrollSyncLock = false; }, 50);
        }

        var debouncedPfScroll = debounce(function () { onPanelScroll('pageforge'); }, 16);
        var debouncedHumanScroll = debounce(function () { onPanelScroll('human'); }, 16);
        var debouncedWriterScroll = debounce(function () { onPanelScroll('writer'); }, 16);

        // Store debounced handlers so we can re-attach after iframe reloads
        this._debouncedPfScroll = debouncedPfScroll;
        this._debouncedHumanScroll = debouncedHumanScroll;
        this._debouncedWriterScroll = debouncedWriterScroll;

        // Writer panel — a regular DOM element, bind once
        if (this.writerPanelBody) {
            this.writerPanelBody.addEventListener('scroll', debouncedWriterScroll);
        }

        // For raw HTML containers — bind once
        if (this.pageforgeRaw) {
            this.pageforgeRaw.addEventListener('scroll', debouncedPfScroll);
        }
        if (this.humanRaw) {
            this.humanRaw.addEventListener('scroll', debouncedHumanScroll);
        }

        // For iframes, we re-attach on each iframe load (since contentDocument changes)
        if (this.pageforgeIframe) {
            this.pageforgeIframe.addEventListener('load', function () {
                self._attachIframeScrollHandler(self.pageforgeIframe, debouncedPfScroll);
            });
        }
        if (this.humanIframe) {
            this.humanIframe.addEventListener('load', function () {
                self._attachIframeScrollHandler(self.humanIframe, debouncedHumanScroll);
            });
        }
    }

    /**
     * Attach scroll handler to an iframe's content document.
     * @param {HTMLIFrameElement} iframe
     * @param {Function} handler
     */
    _attachIframeScrollHandler(iframe, handler) {
        try {
            var doc = iframe.contentDocument || iframe.contentWindow.document;
            var scrollEl = doc.scrollingElement || doc.documentElement;
            if (scrollEl) {
                // Use the document-level scroll event since scrollingElement may not fire events directly
                (iframe.contentWindow || iframe.contentDocument.defaultView).addEventListener('scroll', handler);
            }
        } catch (e) {
            // Cross-origin — cannot attach
        }
    }

    // ------------------------------------------------------------------
    // Text normalisation & fuzzy anchor matching
    // ------------------------------------------------------------------

    /**
     * Normalise text for fuzzy matching: lowercase, strip HTML tags,
     * collapse whitespace, remove punctuation.
     * Shared across scroll-position preservation and sync logic.
     *
     * @param {string} text - Raw text (may contain HTML tags)
     * @returns {string} Normalised text
     */
    static normaliseTextForMatch(text) {
        if (!text) return '';
        // Strip HTML tags
        var stripped = text.replace(/<[^>]+>/g, ' ');
        // Decode common entities
        stripped = stripped.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ').replace(/&#\d+;/g, ' ');
        // Lowercase
        stripped = stripped.toLowerCase();
        // Remove punctuation except apostrophes within words
        stripped = stripped.replace(/[^\w\s'āēīōūĀĒĪŌŪ]/g, ' ');
        // Collapse whitespace
        stripped = stripped.replace(/\s+/g, ' ').trim();
        return stripped;
    }

    /**
     * Extract a textual anchor from the element currently visible at the top
     * of the scrollable area. Returns an object with the anchor text snippet
     * and the element's approximate scroll offset.
     *
     * @param {string} panel - 'pageforge', 'human', or 'writer'
     * @returns {{ anchorText: string, scrollFraction: number }|null}
     */
    _extractVisibleAnchor(panel) {
        if (panel === 'writer') {
            if (!this.writerPanelBody) return null;
            var scrollTop = this.writerPanelBody.scrollTop;
            var blocks = this.writerPanelBody.querySelectorAll('.writer-block');
            var bestBlock = null;
            for (var i = 0; i < blocks.length; i++) {
                if (blocks[i].offsetTop >= scrollTop - 10) {
                    bestBlock = blocks[i];
                    break;
                }
            }
            if (!bestBlock && blocks.length > 0) bestBlock = blocks[blocks.length - 1];
            if (bestBlock) {
                var text = (bestBlock.textContent || '').trim();
                var norm = ReviewApp.normaliseTextForMatch(text);
                var maxScroll = this.writerPanelBody.scrollHeight - this.writerPanelBody.clientHeight;
                return {
                    anchorText: norm.substring(0, 120),
                    scrollFraction: maxScroll > 0 ? scrollTop / maxScroll : 0
                };
            }
            return null;
        }

        // For iframe panels (rendered view)
        var iframe = (panel === 'pageforge') ? this.pageforgeIframe : this.humanIframe;
        var rawView = (panel === 'pageforge') ? this.pageforgeRaw : this.humanRaw;

        if (this.rawHtmlMode && rawView && !rawView.classList.contains('hidden')) {
            // Extract from raw view
            return this._extractAnchorFromRawView(rawView);
        }

        if (!iframe || iframe.classList.contains('hidden')) return null;

        try {
            var doc = iframe.contentDocument || iframe.contentWindow.document;
            var scrollEl = doc.scrollingElement || doc.documentElement;
            var scrollTop = scrollEl.scrollTop;

            // Find the element nearest to the current scroll position
            var candidates = doc.querySelectorAll('h1, h2, h3, h4, h5, p, li, td, th, div.activity, div.alert, div.whakatauki, div.videoSection, img');
            var bestEl = null;
            var bestDist = Infinity;

            for (var i = 0; i < candidates.length; i++) {
                var rect = candidates[i].getBoundingClientRect();
                // getBoundingClientRect is relative to viewport; we want elements near top
                var dist = Math.abs(rect.top);
                if (dist < bestDist) {
                    bestDist = dist;
                    bestEl = candidates[i];
                }
            }

            if (bestEl) {
                var text = (bestEl.textContent || '').trim();
                var norm = ReviewApp.normaliseTextForMatch(text);
                var maxScroll = scrollEl.scrollHeight - scrollEl.clientHeight;
                return {
                    anchorText: norm.substring(0, 120),
                    scrollFraction: maxScroll > 0 ? scrollTop / maxScroll : 0
                };
            }
        } catch (e) {
            // Cross-origin
        }
        return null;
    }

    /**
     * Extract a visible-anchor from a raw HTML view container.
     * Scans lines of the raw code to find which line is at the top of the viewport.
     *
     * @param {HTMLElement} rawViewContainer - The .review-raw-view element
     * @returns {{ anchorText: string, scrollFraction: number }|null}
     */
    _extractAnchorFromRawView(rawViewContainer) {
        var scrollTop = rawViewContainer.scrollTop;
        var maxScroll = rawViewContainer.scrollHeight - rawViewContainer.clientHeight;
        var fraction = maxScroll > 0 ? scrollTop / maxScroll : 0;

        // Get the raw text content and find the line visible at the top
        var codeEl = rawViewContainer.querySelector('code');
        if (!codeEl) return { anchorText: '', scrollFraction: fraction };

        var rawText = codeEl.textContent || '';
        var lines = rawText.split('\n');

        // Estimate the line at the current scroll position
        if (lines.length === 0) return { anchorText: '', scrollFraction: fraction };

        var lineHeight = rawViewContainer.scrollHeight / lines.length;
        var approxLine = Math.floor(scrollTop / lineHeight);
        approxLine = Math.max(0, Math.min(approxLine, lines.length - 1));

        // Extract text from this line and nearby lines for anchor
        var anchorLines = [];
        for (var i = approxLine; i < Math.min(approxLine + 5, lines.length); i++) {
            var trimmed = lines[i].trim();
            if (trimmed.length > 0) {
                anchorLines.push(trimmed);
                break;
            }
        }

        var anchorText = ReviewApp.normaliseTextForMatch(anchorLines.join(' '));
        return {
            anchorText: anchorText.substring(0, 120),
            scrollFraction: fraction
        };
    }

    /**
     * Scroll a raw HTML view to the line best matching an anchor text.
     * Falls back to proportional scroll if no match found.
     *
     * @param {HTMLElement} rawViewContainer - The .review-raw-view element
     * @param {string} anchorText - Normalised anchor text to search for
     * @param {number} fallbackFraction - Proportional scroll fallback (0..1)
     */
    _scrollRawViewToAnchor(rawViewContainer, anchorText, fallbackFraction) {
        if (!rawViewContainer) return;

        var codeEl = rawViewContainer.querySelector('code');
        if (!codeEl || !anchorText) {
            // Fallback to proportional
            var maxScroll = rawViewContainer.scrollHeight - rawViewContainer.clientHeight;
            rawViewContainer.scrollTop = fallbackFraction * maxScroll;
            return;
        }

        var rawText = codeEl.textContent || '';
        var lines = rawText.split('\n');
        if (lines.length === 0) return;

        // Search for the anchor in the raw text lines
        var bestLine = -1;
        var bestScore = 0;

        // Split anchor into words for partial matching
        var anchorWords = anchorText.split(/\s+/).filter(function (w) { return w.length > 2; });
        if (anchorWords.length === 0) {
            var maxScroll = rawViewContainer.scrollHeight - rawViewContainer.clientHeight;
            rawViewContainer.scrollTop = fallbackFraction * maxScroll;
            return;
        }

        for (var i = 0; i < lines.length; i++) {
            var normLine = ReviewApp.normaliseTextForMatch(lines[i]);
            if (!normLine) continue;

            var score = 0;
            for (var w = 0; w < anchorWords.length; w++) {
                if (normLine.indexOf(anchorWords[w]) !== -1) {
                    score++;
                }
            }

            if (score > bestScore) {
                bestScore = score;
                bestLine = i;
            }
        }

        // Require at least 30% of words to match
        if (bestLine >= 0 && bestScore >= Math.max(1, Math.ceil(anchorWords.length * 0.3))) {
            var lineHeight = rawViewContainer.scrollHeight / lines.length;
            rawViewContainer.scrollTop = bestLine * lineHeight;
        } else {
            // Fallback to proportional
            var maxScroll = rawViewContainer.scrollHeight - rawViewContainer.clientHeight;
            rawViewContainer.scrollTop = fallbackFraction * maxScroll;
        }
    }

    /**
     * Scroll a rendered iframe to the element best matching an anchor text.
     * Falls back to proportional scroll if no match found.
     *
     * @param {HTMLIFrameElement} iframe
     * @param {string} anchorText - Normalised anchor text to search for
     * @param {number} fallbackFraction - Proportional scroll fallback (0..1)
     */
    _scrollIframeToAnchor(iframe, anchorText, fallbackFraction) {
        if (!iframe || iframe.classList.contains('hidden')) return;

        try {
            var doc = iframe.contentDocument || iframe.contentWindow.document;
            var scrollEl = doc.scrollingElement || doc.documentElement;

            if (!anchorText) {
                var maxScroll = scrollEl.scrollHeight - scrollEl.clientHeight;
                scrollEl.scrollTop = fallbackFraction * maxScroll;
                return;
            }

            var candidates = doc.querySelectorAll('h1, h2, h3, h4, h5, p, li, td, th, div.activity, div.alert, div.whakatauki');
            var bestEl = null;
            var bestScore = 0;
            var anchorWords = anchorText.split(/\s+/).filter(function (w) { return w.length > 2; });

            if (anchorWords.length === 0) {
                var maxScroll = scrollEl.scrollHeight - scrollEl.clientHeight;
                scrollEl.scrollTop = fallbackFraction * maxScroll;
                return;
            }

            for (var i = 0; i < candidates.length; i++) {
                var elText = ReviewApp.normaliseTextForMatch(candidates[i].textContent || '');
                if (!elText) continue;

                var score = 0;
                for (var w = 0; w < anchorWords.length; w++) {
                    if (elText.indexOf(anchorWords[w]) !== -1) {
                        score++;
                    }
                }

                if (score > bestScore) {
                    bestScore = score;
                    bestEl = candidates[i];
                }
            }

            if (bestEl && bestScore >= Math.max(1, Math.ceil(anchorWords.length * 0.3))) {
                bestEl.scrollIntoView({ block: 'start' });
            } else {
                var maxScroll = scrollEl.scrollHeight - scrollEl.clientHeight;
                scrollEl.scrollTop = fallbackFraction * maxScroll;
            }
        } catch (e) {
            // Cross-origin
        }
    }

    /**
     * Scroll the Writer Template panel to the position best matching an anchor text.
     * Falls back to proportional scroll if no match found.
     *
     * @param {string} anchorText - Normalised anchor text to search for
     * @param {number} fallbackFraction - Proportional scroll fallback (0..1)
     */
    _scrollWriterToAnchor(anchorText, fallbackFraction) {
        if (!this.writerPanelBody) return;

        if (!anchorText) {
            var maxScroll = this.writerPanelBody.scrollHeight - this.writerPanelBody.clientHeight;
            this.writerPanelBody.scrollTop = fallbackFraction * maxScroll;
            return;
        }

        var blocks = this.writerPanelBody.querySelectorAll('.writer-block');
        var bestBlock = null;
        var bestScore = 0;
        var anchorWords = anchorText.split(/\s+/).filter(function (w) { return w.length > 2; });

        if (anchorWords.length === 0) {
            var maxScroll = this.writerPanelBody.scrollHeight - this.writerPanelBody.clientHeight;
            this.writerPanelBody.scrollTop = fallbackFraction * maxScroll;
            return;
        }

        for (var i = 0; i < blocks.length; i++) {
            var blockText = ReviewApp.normaliseTextForMatch(blocks[i].textContent || '');
            if (!blockText) continue;

            var score = 0;
            for (var w = 0; w < anchorWords.length; w++) {
                if (blockText.indexOf(anchorWords[w]) !== -1) {
                    score++;
                }
            }

            if (score > bestScore) {
                bestScore = score;
                bestBlock = blocks[i];
            }
        }

        if (bestBlock && bestScore >= Math.max(1, Math.ceil(anchorWords.length * 0.3))) {
            bestBlock.scrollIntoView({ block: 'start' });
        } else {
            var maxScroll = this.writerPanelBody.scrollHeight - this.writerPanelBody.clientHeight;
            this.writerPanelBody.scrollTop = fallbackFraction * maxScroll;
        }
    }

    // ------------------------------------------------------------------
    // Raw HTML toggle (with scroll-position preservation)
    // ------------------------------------------------------------------

    _toggleRawHtmlMode() {
        // Step 1: Extract anchor from the current PageForge rendered/raw view BEFORE switching
        var anchor = this._extractVisibleAnchor('pageforge');

        // Step 2: Toggle the mode flag and update button
        if (this.rawHtmlMode) {
            this.btnRawHtmlToggle.classList.add('review-raw-btn-active');
            this.btnRawHtmlToggle.textContent = 'Rendered';
        } else {
            this.btnRawHtmlToggle.classList.remove('review-raw-btn-active');
            this.btnRawHtmlToggle.innerHTML = '&lt;/&gt; Raw HTML';
        }

        // Step 3: Reload panels (this switches the view)
        if (this.selectedFile) {
            this._loadPageforgePanel(this.selectedFile);
            this._loadHumanPanel(this.selectedFile);
        }

        // Step 4: After loading, scroll all panels to the anchor position
        if (anchor) {
            var self = this;
            // Use requestAnimationFrame to wait for rendering to complete
            requestAnimationFrame(function () {
                // A second rAF ensures layout is stable
                requestAnimationFrame(function () {
                    self._restoreScrollFromAnchor(anchor);
                });
            });
        }
    }

    /**
     * Restore scroll positions across all three panels based on a textual anchor.
     * Used after toggling Raw HTML mode.
     *
     * @param {{ anchorText: string, scrollFraction: number }} anchor
     */
    _restoreScrollFromAnchor(anchor) {
        var anchorText = anchor.anchorText;
        var fraction = anchor.scrollFraction;

        // Temporarily disable sync to avoid feedback loops during restoration
        var wasSyncEnabled = this.syncModeEnabled;
        this.syncModeEnabled = false;
        this._scrollSyncLock = true;

        if (this.rawHtmlMode) {
            // Switched TO raw HTML: scroll raw views + writer to anchor
            this._scrollRawViewToAnchor(this.pageforgeRaw, anchorText, fraction);
            this._scrollRawViewToAnchor(this.humanRaw, anchorText, fraction);
        } else {
            // Switched TO rendered: scroll iframes to anchor
            // Iframes need a load event to be ready; use a timeout as fallback
            var self = this;
            var pfDone = false;
            var humanDone = false;

            function scrollPf() {
                if (pfDone) return;
                pfDone = true;
                self._scrollIframeToAnchor(self.pageforgeIframe, anchorText, fraction);
            }

            function scrollHuman() {
                if (humanDone) return;
                humanDone = true;
                self._scrollIframeToAnchor(self.humanIframe, anchorText, fraction);
            }

            if (this.pageforgeIframe && !this.pageforgeIframe.classList.contains('hidden')) {
                this.pageforgeIframe.addEventListener('load', function onLoad() {
                    self.pageforgeIframe.removeEventListener('load', onLoad);
                    scrollPf();
                });
                setTimeout(scrollPf, 500);
            }

            if (this.humanIframe && !this.humanIframe.classList.contains('hidden')) {
                this.humanIframe.addEventListener('load', function onLoad() {
                    self.humanIframe.removeEventListener('load', onLoad);
                    scrollHuman();
                });
                setTimeout(scrollHuman, 500);
            }
        }

        // Scroll writer panel to anchor
        this._scrollWriterToAnchor(anchorText, fraction);

        // Restore sync mode after a delay
        var self = this;
        setTimeout(function () {
            self.syncModeEnabled = wasSyncEnabled;
            self._scrollSyncLock = false;
        }, 600);
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
    // Copy-to-snapshot buttons (save to sessionStorage)
    // ------------------------------------------------------------------

    _showCopyToSnapshotButtons() {
        if (this.btnCopyWt) this.btnCopyWt.classList.remove('hidden');
        if (this.btnCopyPf) this.btnCopyPf.classList.remove('hidden');
        if (this.btnCopyHuman && this._findReference(this.selectedFile)) {
            this.btnCopyHuman.classList.remove('hidden');
        }
    }

    _hideCopyToSnapshotButtons() {
        if (this.btnCopyWt) this.btnCopyWt.classList.add('hidden');
        if (this.btnCopyPf) this.btnCopyPf.classList.add('hidden');
        if (this.btnCopyHuman) this.btnCopyHuman.classList.add('hidden');
    }

    /**
     * Copy highlighted content to sessionStorage for the Conversion Error Log page.
     * @param {string} type - 'wt', 'pf', or 'human'
     */
    _copyToSessionStorage(type) {
        var content = '';
        var blockIndex = this.highlightedBlockIndex;

        if (type === 'wt') {
            // Get writer template content for this block
            var pageData = this._getPageData(this.selectedFile);
            if (pageData && pageData.contentBlockTexts && blockIndex !== null && blockIndex !== 'menu' && blockIndex !== 'header' && blockIndex !== 'footer') {
                var idx = parseInt(blockIndex, 10);
                if (!isNaN(idx)) {
                    content = pageData.contentBlockTexts[idx] || '';
                }
            }
            if (content) {
                sessionStorage.setItem('pageforge_snapshot_wt', content);
                this.showToast('Writer Template content copied for snapshot');
            } else {
                this.showToast('No writer template content to copy');
            }
        } else if (type === 'pf') {
            content = this._getHighlightedHtml(this.pageforgeIframe, blockIndex);
            if (content) {
                sessionStorage.setItem('pageforge_snapshot_pf', content);
                sessionStorage.setItem('pageforge_snapshot_file', this.selectedFile || '');
                this.showToast('PageForge content copied for snapshot');
            } else {
                this.showToast('No PageForge content to copy');
            }
        } else if (type === 'human') {
            content = this._getHighlightedHtml(this.humanIframe, null);
            if (content) {
                sessionStorage.setItem('pageforge_snapshot_human', content);
                this.showToast('Human reference content copied for snapshot');
            } else {
                this.showToast('No human reference content to copy');
            }
        }
    }

    /**
     * Get the outerHTML of the currently highlighted element in an iframe.
     * @param {HTMLIFrameElement} iframe
     * @param {string|null} blockIndex
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
                this.showToast('Rejected "' + file.name + '" \u2014 only .html files accepted');
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
