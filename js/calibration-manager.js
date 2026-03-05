/**
 * CalibrationManager — Calibration Comparison Tool for PageForge.
 *
 * Manages human reference file upload, comparison snapshot logging,
 * snapshot display, and calibration report export. This is a development
 * tool for internal algorithm refinement — it sits alongside the main
 * conversion workflow and is accessed AFTER a conversion has been completed.
 *
 * IMPORTANT NOTES:
 * - Content differences between human reference files and PageForge output
 *   are expected. The human developer may have received direct feedback and
 *   made edits to the final HTML without updating the Writer Template.
 * - Writer comments/instructions (red text) in the Writer Template are
 *   development guidance only — they will not appear in the human-developed
 *   HTML files.
 * - All data is ephemeral — it only persists in memory during the current
 *   session. When the page reloads or a new file is parsed, all calibration
 *   data is cleared. This is consistent with PageForge's privacy model
 *   (no data storage).
 */

'use strict';

class CalibrationManager {
    /**
     * @param {object} options
     * @param {function} options.showToast - Function to display toast notifications
     * @param {function} options.getModuleCode - Function returning current module code
     * @param {function} options.getTemplateName - Function returning current template name
     * @param {function} options.getGeneratedFileList - Function returning array of generated filenames
     */
    constructor(options) {
        this._showToast = options.showToast || function () {};
        this._getModuleCode = options.getModuleCode || function () { return ''; };
        this._getTemplateName = options.getTemplateName || function () { return ''; };
        this._getGeneratedFileList = options.getGeneratedFileList || function () { return []; };

        /** Uploaded human reference files */
        this.humanReferenceFiles = [];

        /** Logged comparison snapshots */
        this.calibrationSnapshots = [];

        /** Next snapshot ID */
        this._nextSnapshotId = 1;

        this._bound = false;
    }

    // ------------------------------------------------------------------
    // Initialisation
    // ------------------------------------------------------------------

    /**
     * Bind DOM elements and wire up events. Called once after the
     * calibration panel HTML has been added to the page.
     */
    init() {
        if (this._bound) return;
        this._bound = true;

        this._bindElements();
        this._bindEvents();
    }

    /**
     * Cache references to calibration DOM elements.
     */
    _bindElements() {
        this.panel = document.getElementById('calibration-panel');
        this.dropzone = document.getElementById('calibration-dropzone');
        this.fileInput = document.getElementById('calibration-file-input');
        this.uploadedFilesList = document.getElementById('calibration-uploaded-files');
        this.snapshotOriginal = document.getElementById('snapshot-original');
        this.snapshotPageforge = document.getElementById('snapshot-pageforge');
        this.snapshotHuman = document.getElementById('snapshot-human');
        this.snapshotNotes = document.getElementById('snapshot-notes');
        this.snapshotSourceFile = document.getElementById('snapshot-source-file');
        this.btnLogSnapshot = document.getElementById('btn-log-snapshot');
        this.btnClearForm = document.getElementById('btn-clear-snapshot-form');
        this.snapshotCount = document.getElementById('snapshot-count');
        this.snapshotList = document.getElementById('snapshot-list');
        this.btnExport = document.getElementById('btn-export-calibration');
        this.btnCopy = document.getElementById('btn-copy-calibration');
        this.btnClearAll = document.getElementById('btn-clear-all-snapshots');
    }

    /**
     * Wire up all calibration event listeners.
     */
    _bindEvents() {
        var self = this;

        // --- Human reference file upload ---

        if (this.dropzone) {
            this.dropzone.addEventListener('dragover', function (e) {
                e.preventDefault();
                e.stopPropagation();
                self.dropzone.classList.add('drag-over');
            });

            this.dropzone.addEventListener('dragleave', function (e) {
                e.preventDefault();
                e.stopPropagation();
                self.dropzone.classList.remove('drag-over');
            });

            this.dropzone.addEventListener('drop', function (e) {
                e.preventDefault();
                e.stopPropagation();
                self.dropzone.classList.remove('drag-over');
                var files = e.dataTransfer.files;
                self._handleReferenceFiles(files);
            });

            this.dropzone.addEventListener('click', function () {
                self.fileInput.click();
            });
        }

        if (this.fileInput) {
            this.fileInput.addEventListener('change', function () {
                if (self.fileInput.files.length > 0) {
                    self._handleReferenceFiles(self.fileInput.files);
                }
                // Reset so the same files can be re-selected
                self.fileInput.value = '';
            });
        }

        // --- Snapshot form validation ---

        var formFields = [this.snapshotOriginal, this.snapshotPageforge, this.snapshotHuman];
        for (var i = 0; i < formFields.length; i++) {
            if (formFields[i]) {
                formFields[i].addEventListener('input', function () {
                    self._updateLogButtonState();
                });
            }
        }

        // --- Snapshot form actions ---

        if (this.btnLogSnapshot) {
            this.btnLogSnapshot.addEventListener('click', function () {
                self._logSnapshot();
            });
        }

        if (this.btnClearForm) {
            this.btnClearForm.addEventListener('click', function () {
                self._clearForm();
            });
        }

        // --- Export actions ---

        if (this.btnExport) {
            this.btnExport.addEventListener('click', function () {
                self._exportReport();
            });
        }

        if (this.btnCopy) {
            this.btnCopy.addEventListener('click', function () {
                self._copyReport();
            });
        }

        if (this.btnClearAll) {
            this.btnClearAll.addEventListener('click', function () {
                self._clearAllSnapshots();
            });
        }
    }

    // ------------------------------------------------------------------
    // Human reference file handling
    // ------------------------------------------------------------------

    /**
     * Process uploaded reference files — validate, read content, store.
     * @param {FileList} files - The uploaded files
     */
    _handleReferenceFiles(files) {
        var self = this;
        var generatedFiles = this._getGeneratedFileList();

        for (var i = 0; i < files.length; i++) {
            var file = files[i];

            // Validate .html extension
            if (!file.name.toLowerCase().endsWith('.html')) {
                this._showToast('Rejected "' + file.name + '" — only .html files accepted');
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
            if (alreadyUploaded) {
                continue;
            }

            // Read file content
            (function (f) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    var matched = generatedFiles.indexOf(f.name) !== -1;
                    self.humanReferenceFiles.push({
                        filename: f.name,
                        content: e.target.result,
                        size: f.size,
                        matchedToGenerated: matched
                    });
                    self._renderUploadedFiles();
                };
                reader.readAsText(f);
            })(file);
        }
    }

    /**
     * Render the list of uploaded human reference files.
     */
    _renderUploadedFiles() {
        if (!this.uploadedFilesList) return;

        if (this.humanReferenceFiles.length === 0) {
            this.uploadedFilesList.innerHTML = '';
            return;
        }

        var html = '';
        for (var i = 0; i < this.humanReferenceFiles.length; i++) {
            var file = this.humanReferenceFiles[i];
            var sizeStr = this._formatFileSize(file.size);
            var statusClass = file.matchedToGenerated ? 'calibration-file-matched' : 'calibration-file-unmatched';
            var statusText = file.matchedToGenerated ? 'Matched' : 'Unmatched';

            html += '<div class="calibration-file-item" data-index="' + i + '">';
            html += '<span class="calibration-file-name">' + this._escapeHtml(file.filename) + '</span>';
            html += '<span class="calibration-file-size">' + sizeStr + '</span>';
            html += '<span class="' + statusClass + '">' + statusText + '</span>';
            html += '<button class="btn btn-sm calibration-file-remove" type="button" '
                + 'data-index="' + i + '" title="Remove this file">&#10005;</button>';
            html += '</div>';
        }

        this.uploadedFilesList.innerHTML = html;

        // Bind remove buttons
        var self = this;
        var removeBtns = this.uploadedFilesList.querySelectorAll('.calibration-file-remove');
        for (var i = 0; i < removeBtns.length; i++) {
            removeBtns[i].addEventListener('click', function (e) {
                e.stopPropagation();
                var idx = parseInt(this.getAttribute('data-index'), 10);
                self._removeReferenceFile(idx);
            });
        }
    }

    /**
     * Remove a reference file by index.
     * @param {number} index
     */
    _removeReferenceFile(index) {
        if (index >= 0 && index < this.humanReferenceFiles.length) {
            var removed = this.humanReferenceFiles.splice(index, 1);
            this._renderUploadedFiles();
            this._showToast('Removed ' + removed[0].filename);
        }
    }

    // ------------------------------------------------------------------
    // Source file dropdown population
    // ------------------------------------------------------------------

    /**
     * Populate the source file dropdown with generated filenames.
     */
    populateSourceFileDropdown() {
        if (!this.snapshotSourceFile) return;

        var files = this._getGeneratedFileList();

        // Clear existing options (except the placeholder)
        while (this.snapshotSourceFile.options.length > 1) {
            this.snapshotSourceFile.remove(1);
        }

        for (var i = 0; i < files.length; i++) {
            var opt = document.createElement('option');
            opt.value = files[i];
            opt.textContent = files[i];
            this.snapshotSourceFile.appendChild(opt);
        }

        // Reset to placeholder
        this.snapshotSourceFile.selectedIndex = 0;
    }

    // ------------------------------------------------------------------
    // Snapshot form
    // ------------------------------------------------------------------

    /**
     * Update the Log Snapshot button enabled/disabled state
     * based on required field content.
     */
    _updateLogButtonState() {
        if (!this.btnLogSnapshot) return;

        var hasOriginal = this.snapshotOriginal && this.snapshotOriginal.value.trim().length > 0;
        var hasPageforge = this.snapshotPageforge && this.snapshotPageforge.value.trim().length > 0;
        var hasHuman = this.snapshotHuman && this.snapshotHuman.value.trim().length > 0;

        this.btnLogSnapshot.disabled = !(hasOriginal && hasPageforge && hasHuman);
    }

    /**
     * Log a new snapshot from the current form values.
     */
    _logSnapshot() {
        var original = this.snapshotOriginal ? this.snapshotOriginal.value : '';
        var pageforge = this.snapshotPageforge ? this.snapshotPageforge.value : '';
        var human = this.snapshotHuman ? this.snapshotHuman.value : '';
        var notes = this.snapshotNotes ? this.snapshotNotes.value : '';
        var sourceFile = this.snapshotSourceFile ? this.snapshotSourceFile.value : '';

        if (!original.trim() || !pageforge.trim() || !human.trim()) {
            return;
        }

        var snapshot = {
            id: this._nextSnapshotId++,
            timestamp: new Date().toISOString(),
            sourceFile: sourceFile || '',
            originalContent: original,
            pageforgeOutput: pageforge,
            humanOutput: human,
            notes: notes
        };

        this.calibrationSnapshots.push(snapshot);

        // Clear form
        this._clearForm();

        // Update display
        this._renderSnapshotList();
        this._updateExportButtonState();

        this._showToast('Snapshot #' + snapshot.id + ' logged');
    }

    /**
     * Clear all form fields without logging.
     */
    _clearForm() {
        if (this.snapshotOriginal) this.snapshotOriginal.value = '';
        if (this.snapshotPageforge) this.snapshotPageforge.value = '';
        if (this.snapshotHuman) this.snapshotHuman.value = '';
        if (this.snapshotNotes) this.snapshotNotes.value = '';
        if (this.snapshotSourceFile) this.snapshotSourceFile.selectedIndex = 0;
        this._updateLogButtonState();
    }

    // ------------------------------------------------------------------
    // Snapshot list display
    // ------------------------------------------------------------------

    /**
     * Render the list of logged snapshots.
     */
    _renderSnapshotList() {
        if (!this.snapshotList) return;

        // Update count badge
        if (this.snapshotCount) {
            this.snapshotCount.textContent = '(' + this.calibrationSnapshots.length + ')';
        }

        if (this.calibrationSnapshots.length === 0) {
            this.snapshotList.innerHTML = '<p class="snapshot-empty-state">'
                + 'No snapshots logged yet. Use the form above to document discrepancies.</p>';
            return;
        }

        var html = '';
        for (var i = 0; i < this.calibrationSnapshots.length; i++) {
            var snap = this.calibrationSnapshots[i];
            var time = this._formatTime(snap.timestamp);
            var preview = this._truncate(snap.originalContent, 80);
            var fileDisplay = snap.sourceFile ? this._escapeHtml(snap.sourceFile) : '<i>No file</i>';
            var hasNotes = snap.notes && snap.notes.trim().length > 0;

            html += '<div class="snapshot-entry" data-snapshot-id="' + snap.id + '">';
            html += '<div class="snapshot-entry-header">';
            html += '<span class="snapshot-entry-number">#' + snap.id + '</span>';
            html += '<span class="snapshot-entry-file">' + fileDisplay + '</span>';
            html += '<span class="snapshot-entry-time">' + time + '</span>';
            html += '<button class="btn btn-sm snapshot-delete" type="button" '
                + 'data-snapshot-id="' + snap.id + '" title="Delete this snapshot">&#10005;</button>';
            html += '</div>';
            html += '<span class="snapshot-preview-text">' + this._escapeHtml(preview) + '</span>';
            html += '<details class="snapshot-entry-details">';
            html += '<summary>View full snapshot</summary>';
            html += '<div class="snapshot-full-content">';
            html += '<div class="snapshot-full-field">';
            html += '<strong>1. Original Writer Template Content:</strong>';
            html += '<pre>' + this._escapeHtml(snap.originalContent) + '</pre>';
            html += '</div>';
            html += '<div class="snapshot-full-field">';
            html += '<strong>2. PageForge Generated Output:</strong>';
            html += '<pre>' + this._escapeHtml(snap.pageforgeOutput) + '</pre>';
            html += '</div>';
            html += '<div class="snapshot-full-field">';
            html += '<strong>3. Human Developer Correct Output:</strong>';
            html += '<pre>' + this._escapeHtml(snap.humanOutput) + '</pre>';
            html += '</div>';
            if (hasNotes) {
                html += '<div class="snapshot-full-field" data-has-notes="true">';
                html += '<strong>4. Notes:</strong>';
                html += '<pre>' + this._escapeHtml(snap.notes) + '</pre>';
                html += '</div>';
            }
            html += '</div>';
            html += '</details>';
            html += '</div>';
        }

        this.snapshotList.innerHTML = html;

        // Bind delete buttons
        var self = this;
        var deleteBtns = this.snapshotList.querySelectorAll('.snapshot-delete');
        for (var i = 0; i < deleteBtns.length; i++) {
            deleteBtns[i].addEventListener('click', function (e) {
                e.stopPropagation();
                var id = parseInt(this.getAttribute('data-snapshot-id'), 10);
                self._deleteSnapshot(id);
            });
        }
    }

    /**
     * Delete a snapshot by ID after user confirmation.
     * @param {number} id
     */
    _deleteSnapshot(id) {
        if (!confirm('Delete snapshot #' + id + '?')) return;

        for (var i = 0; i < this.calibrationSnapshots.length; i++) {
            if (this.calibrationSnapshots[i].id === id) {
                this.calibrationSnapshots.splice(i, 1);
                break;
            }
        }

        this._renderSnapshotList();
        this._updateExportButtonState();
        this._showToast('Snapshot #' + id + ' deleted');
    }

    // ------------------------------------------------------------------
    // Export
    // ------------------------------------------------------------------

    /**
     * Update the export/copy button enabled/disabled state.
     */
    _updateExportButtonState() {
        var hasSnapshots = this.calibrationSnapshots.length > 0;
        if (this.btnExport) this.btnExport.disabled = !hasSnapshots;
        if (this.btnCopy) this.btnCopy.disabled = !hasSnapshots;
    }

    /**
     * Generate the calibration report as plain text.
     * @returns {string}
     */
    _generateReport() {
        var moduleCode = this._getModuleCode() || 'Unknown';
        var templateName = this._getTemplateName() || 'Unknown';
        var now = new Date();
        var dateStr = now.toISOString().replace('T', ' ').replace(/\.\d+Z$/, ' UTC');
        var total = this.calibrationSnapshots.length;

        var lines = [];
        lines.push('==========================================');
        lines.push('PAGEFORGE CALIBRATION REPORT');
        lines.push('==========================================');
        lines.push('Module: ' + moduleCode);
        lines.push('Template: ' + templateName);
        lines.push('Generated: ' + dateStr);
        lines.push('Total Snapshots: ' + total);
        lines.push('');
        lines.push('IMPORTANT CONTEXT FOR ANALYSIS:');
        lines.push('- The "Original Content" shows raw parsed text from the Writer Template');
        lines.push('  document BEFORE PageForge attempted to convert it.');
        lines.push('- The "PageForge Output" shows what the current algorithm actually produced.');
        lines.push('- The "Human Output" shows what a human developer correctly produced —');
        lines.push('  this is the TARGET that PageForge should aim to replicate.');
        lines.push('- Note: The human reference files may have text content differences from');
        lines.push('  the Writer Template due to post-production edits made directly to the');
        lines.push('  HTML files (not reflected back in the Writer Template).');
        lines.push('- Note: Writer comments/instructions (red text) in the Writer Template');
        lines.push('  may not appear in the human HTML files, as they served only as');
        lines.push('  development guidance.');
        lines.push('');
        lines.push('==========================================');

        for (var i = 0; i < this.calibrationSnapshots.length; i++) {
            var snap = this.calibrationSnapshots[i];
            var num = i + 1;

            lines.push('');
            lines.push('------------------------------------------');
            lines.push('SNAPSHOT ' + num + ' of ' + total);
            lines.push('------------------------------------------');
            lines.push('Source File: ' + (snap.sourceFile || 'Not specified'));
            lines.push('Logged: ' + snap.timestamp);
            lines.push('');
            lines.push('--- ORIGINAL WRITER TEMPLATE CONTENT ---');
            lines.push(snap.originalContent);
            lines.push('');
            lines.push('--- PAGEFORGE GENERATED OUTPUT ---');
            lines.push(snap.pageforgeOutput);
            lines.push('');
            lines.push('--- HUMAN DEVELOPER CORRECT OUTPUT ---');
            lines.push(snap.humanOutput);
            lines.push('');
            lines.push('--- NOTES ---');
            lines.push(snap.notes && snap.notes.trim() ? snap.notes : 'No notes provided.');
            lines.push('');
            lines.push('------------------------------------------');
        }

        lines.push('');
        lines.push('==========================================');
        lines.push('END OF CALIBRATION REPORT');
        lines.push('==========================================');

        return lines.join('\n');
    }

    /**
     * Export the calibration report as a downloadable .txt file.
     */
    _exportReport() {
        if (this.calibrationSnapshots.length === 0) {
            this._showToast('No snapshots to export');
            return;
        }

        var report = this._generateReport();
        var moduleCode = this._getModuleCode() || 'PageForge';
        var filename = moduleCode + '_calibration_report.txt';

        var blob = new Blob([report], { type: 'text/plain;charset=utf-8' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this._showToast('Exported ' + filename);
    }

    /**
     * Copy the calibration report to the clipboard.
     */
    _copyReport() {
        if (this.calibrationSnapshots.length === 0) {
            this._showToast('No snapshots to copy');
            return;
        }

        var report = this._generateReport();
        var self = this;

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(report).then(function () {
                self._showToast('Calibration report copied to clipboard');
            }, function () {
                self._fallbackCopy(report);
            });
        } else {
            this._fallbackCopy(report);
        }
    }

    /**
     * Fallback clipboard copy using textarea + execCommand.
     * @param {string} text
     */
    _fallbackCopy(text) {
        var textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            this._showToast('Calibration report copied to clipboard');
        } catch (e) {
            this._showToast('Failed to copy. Please try again.');
        }
        document.body.removeChild(textarea);
    }

    /**
     * Clear all snapshots after user confirmation.
     */
    _clearAllSnapshots() {
        if (this.calibrationSnapshots.length === 0) {
            this._showToast('No snapshots to clear');
            return;
        }

        if (!confirm('Clear all ' + this.calibrationSnapshots.length + ' logged snapshots? This cannot be undone.')) {
            return;
        }

        this.calibrationSnapshots = [];
        this._nextSnapshotId = 1;
        this._renderSnapshotList();
        this._updateExportButtonState();
        this._showToast('All snapshots cleared');
    }

    // ------------------------------------------------------------------
    // Full reset
    // ------------------------------------------------------------------

    /**
     * Reset all calibration data. Called when "Parse Another File" is
     * clicked or a new conversion starts.
     */
    reset() {
        this.humanReferenceFiles = [];
        this.calibrationSnapshots = [];
        this._nextSnapshotId = 1;

        if (this.uploadedFilesList) {
            this.uploadedFilesList.innerHTML = '';
        }

        this._clearForm();
        this._renderSnapshotList();
        this._updateExportButtonState();

        // Hide the panel
        if (this.panel) {
            this.panel.removeAttribute('open');
        }
    }

    // ------------------------------------------------------------------
    // Utility helpers
    // ------------------------------------------------------------------

    /**
     * Format a file size in bytes to a human-readable string.
     * @param {number} bytes
     * @returns {string}
     */
    _formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    /**
     * Format an ISO timestamp to a short time string (HH:MM).
     * @param {string} isoString
     * @returns {string}
     */
    _formatTime(isoString) {
        try {
            var d = new Date(isoString);
            var h = String(d.getHours()).padStart(2, '0');
            var m = String(d.getMinutes()).padStart(2, '0');
            return h + ':' + m;
        } catch (e) {
            return '';
        }
    }

    /**
     * Truncate a string to a maximum length, adding ellipsis if needed.
     * @param {string} str
     * @param {number} maxLen
     * @returns {string}
     */
    _truncate(str, maxLen) {
        if (!str) return '';
        var trimmed = str.replace(/\n/g, ' ').trim();
        if (trimmed.length <= maxLen) return trimmed;
        return trimmed.substring(0, maxLen) + '\u2026';
    }

    /**
     * Escape HTML special characters.
     * @param {string} str
     * @returns {string}
     */
    _escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
}
