/**
 * OutputManager — Manages generated output files for ParseMaster.
 *
 * Stores generated HTML files and the interactive reference document,
 * provides file listing with metadata, and handles individual and
 * bulk downloads (ZIP via JSZip).
 */

'use strict';

class OutputManager {
    constructor() {
        /** @type {Array<Object>} Stored file entries */
        this.files = [];
    }

    /**
     * Add a generated file to the output collection.
     *
     * @param {Object} fileInfo
     * @param {string} fileInfo.filename - Output filename
     * @param {string} fileInfo.content - File content string
     * @param {string} fileInfo.type - 'html' or 'reference'
     * @param {string} fileInfo.pageType - 'overview', 'lesson', or 'reference'
     * @param {number|null} fileInfo.lessonNumber - Lesson number or null
     * @param {number} [fileInfo.size] - Byte count (defaults to content.length)
     */
    addFile(fileInfo) {
        var entry = {
            filename: fileInfo.filename,
            content: fileInfo.content,
            type: fileInfo.type || 'html',
            pageType: fileInfo.pageType || 'html',
            lessonNumber: fileInfo.lessonNumber !== undefined ? fileInfo.lessonNumber : null,
            size: fileInfo.size || fileInfo.content.length
        };
        this.files.push(entry);
    }

    /**
     * Get the list of stored files with metadata.
     *
     * @returns {Array<Object>} File list with formatted sizes
     */
    getFileList() {
        var list = [];
        for (var i = 0; i < this.files.length; i++) {
            var f = this.files[i];
            list.push({
                filename: f.filename,
                type: f.type,
                pageType: f.pageType,
                lessonNumber: f.lessonNumber,
                size: f.size,
                sizeFormatted: this._formatSize(f.size)
            });
        }
        return list;
    }

    /**
     * Get the content of a specific file by filename.
     *
     * @param {string} filename
     * @returns {string|null} File content or null if not found
     */
    getFileContent(filename) {
        for (var i = 0; i < this.files.length; i++) {
            if (this.files[i].filename === filename) {
                return this.files[i].content;
            }
        }
        return null;
    }

    /**
     * Get a file entry by filename.
     *
     * @param {string} filename
     * @returns {Object|null} File entry or null
     */
    getFile(filename) {
        for (var i = 0; i < this.files.length; i++) {
            if (this.files[i].filename === filename) {
                return this.files[i];
            }
        }
        return null;
    }

    /**
     * Download an individual file.
     *
     * @param {string} filename
     */
    downloadFile(filename) {
        var file = this.getFile(filename);
        if (!file) return;

        var mimeType = file.type === 'html'
            ? 'text/html;charset=utf-8'
            : 'text/plain;charset=utf-8';

        var blob = new Blob([file.content], { type: mimeType });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = file.filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    /**
     * Download all files as a ZIP archive using JSZip.
     *
     * @param {string} zipFilename - Name for the ZIP file
     * @returns {Promise<void>}
     */
    async downloadAsZip(zipFilename) {
        if (typeof JSZip === 'undefined') {
            throw new Error('JSZip is not available');
        }

        var zip = new JSZip();
        for (var i = 0; i < this.files.length; i++) {
            zip.file(this.files[i].filename, this.files[i].content);
        }

        var blob = await zip.generateAsync({ type: 'blob' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = zipFilename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    /**
     * Copy a file's content to the clipboard.
     *
     * @param {string} filename
     * @returns {Promise<boolean>} Whether the copy succeeded
     */
    async copyToClipboard(filename) {
        var content = this.getFileContent(filename);
        if (content === null) return false;

        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(content);
                return true;
            }
        } catch (e) {
            // Fall through to fallback
        }

        // Fallback for older browsers
        try {
            var textarea = document.createElement('textarea');
            textarea.value = content;
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            textarea.style.top = '-9999px';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            return true;
        } catch (e) {
            return false;
        }
    }

    /**
     * Clear all stored files.
     */
    clear() {
        this.files = [];
    }

    /**
     * Get the total number of stored files.
     *
     * @returns {number}
     */
    getFileCount() {
        return this.files.length;
    }

    /**
     * Get count of HTML files only.
     *
     * @returns {number}
     */
    getHtmlFileCount() {
        var count = 0;
        for (var i = 0; i < this.files.length; i++) {
            if (this.files[i].type === 'html') count++;
        }
        return count;
    }

    /**
     * Format a byte size into a human-readable string.
     *
     * @param {number} bytes
     * @returns {string} Formatted size (e.g., "12.1 KB")
     */
    _formatSize(bytes) {
        if (bytes < 1024) {
            return bytes + ' B';
        } else if (bytes < 1024 * 1024) {
            return (bytes / 1024).toFixed(1) + ' KB';
        } else {
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        }
    }
}
