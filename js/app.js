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

        /** Cached formatted output after a successful parse */
        this.currentOutput = null;

        /** Cached metadata for display */
        this.currentMetadata = null;

        this._bindElements();
        this._bindEvents();
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
            if (self.currentOutput) {
                self.copyToClipboard(self.currentOutput.full, 'Full output copied to clipboard');
            }
        });

        this.btnCopyContent.addEventListener('click', function () {
            if (self.currentOutput) {
                self.copyToClipboard(self.currentOutput.contentOnly, 'Content copied to clipboard (without metadata)');
            }
        });

        this.btnDownload.addEventListener('click', function () {
            if (self.currentOutput) {
                const code = self.currentMetadata && self.currentMetadata.moduleCode
                    ? self.currentMetadata.moduleCode
                    : 'ParseMaster_output';
                self.downloadAsTxt(self.currentOutput.full, code + '_extracted.txt');
            }
        });

        this.btnReset.addEventListener('click', function () {
            self.reset();
        });
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

        // Populate output area
        this.outputArea.value = output.full;

        // Check if content is empty
        if (!output.contentOnly || output.contentOnly.trim() === '--- CONTENT START ---') {
            this.showError('This document appears to be empty or contains no text content.');
        }

        // Announce to screen readers
        this._announce('Document processed successfully. ' +
            result.stats.totalParagraphs + ' paragraphs extracted.');
    }

    reset() {
        this.currentOutput = null;
        this.currentMetadata = null;
        this.resultsSection.classList.add('hidden');
        this.processingSection.classList.add('hidden');
        this.uploadSection.classList.remove('hidden');
        this.hideError();
        this.fileInput.value = '';
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
