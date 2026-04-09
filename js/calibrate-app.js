/**
 * CalibrateApp — Controller for the standalone Conversion Error Log page.
 *
 * Handles data deserialisation from sessionStorage, CalibrationManager instantiation,
 * auto-population of snapshot form fields from sessionStorage keys set by the
 * Visual Comparison Review page's "Copy to Snapshot" buttons, and navigation.
 *
 * This is a standalone controller for calibrate.html — it does not depend on
 * App, DocxParser, ReviewApp, or any other main-page class.
 */

'use strict';

class CalibrateApp {
    constructor() {
        /** Deserialised calibration data */
        this.calibData = null;

        /** CalibrationManager instance */
        this.calibrationManager = null;

        this._loadData();
        this._bindElements();
        this._initCalibrationManager();
        this._bindEvents();
        this._populateFromSessionStorage();
    }

    // ------------------------------------------------------------------
    // Data loading
    // ------------------------------------------------------------------

    /**
     * Load calibration-specific data from sessionStorage.
     */
    _loadData() {
        try {
            var raw = sessionStorage.getItem('pageforge_calibrate_data');
            if (raw) {
                this.calibData = JSON.parse(raw);
            }
        } catch (e) {
            console.error('CalibrateApp: Failed to load calibration data:', e);
            this.calibData = null;
        }
    }

    // ------------------------------------------------------------------
    // DOM references
    // ------------------------------------------------------------------

    _bindElements() {
        this.moduleCodeDisplay = document.getElementById('calibrate-module-code');
        this.btnBack = document.getElementById('btn-back');
        this.toast = document.getElementById('toast');
    }

    // ------------------------------------------------------------------
    // CalibrationManager initialisation
    // ------------------------------------------------------------------

    _initCalibrationManager() {
        var self = this;
        this.calibrationManager = new CalibrationManager({
            showToast: function (msg) { self.showToast(msg); },
            getModuleCode: function () {
                return (self.calibData && self.calibData.metadata && self.calibData.metadata.moduleCode) || '';
            },
            getTemplateName: function () {
                return (self.calibData && self.calibData.templateName) || '';
            },
            getGeneratedFileList: function () {
                return (self.calibData && self.calibData.generatedFileList) || [];
            }
        });
        this.calibrationManager.init();

        // Populate source file dropdown
        if (this.calibData && this.calibData.generatedFileList) {
            this.calibrationManager.populateSourceFileDropdown();
        }

        // Show module code badge
        if (this.moduleCodeDisplay && this.calibData && this.calibData.metadata && this.calibData.metadata.moduleCode) {
            this.moduleCodeDisplay.textContent = this.calibData.metadata.moduleCode;
            this.moduleCodeDisplay.classList.remove('hidden');
        }
    }

    // ------------------------------------------------------------------
    // Event binding
    // ------------------------------------------------------------------

    _bindEvents() {
        var self = this;

        // Back button — try to close the tab, fallback to review page
        if (this.btnBack) {
            this.btnBack.addEventListener('click', function (e) {
                e.preventDefault();
                if (window.opener) {
                    window.close();
                } else {
                    window.location.href = 'review.html';
                }
            });
        }

        // Listen for focus events to auto-populate from sessionStorage
        window.addEventListener('focus', function () {
            self._populateFromSessionStorage();
        });
    }

    // ------------------------------------------------------------------
    // Auto-population from sessionStorage
    // ------------------------------------------------------------------

    /**
     * Check sessionStorage for snapshot data from the Review page's
     * "Copy to Snapshot" buttons. If found, pre-populate form fields,
     * auto-select the source file, and clear the keys.
     */
    _populateFromSessionStorage() {
        var wtContent = sessionStorage.getItem('pageforge_snapshot_wt');
        var pfContent = sessionStorage.getItem('pageforge_snapshot_pf');
        var humanContent = sessionStorage.getItem('pageforge_snapshot_human');
        var snapshotFile = sessionStorage.getItem('pageforge_snapshot_file');

        var populated = false;

        if (wtContent) {
            var wtField = document.getElementById('snapshot-original');
            if (wtField) {
                wtField.value = wtContent;
                populated = true;
            }
            sessionStorage.removeItem('pageforge_snapshot_wt');
        }

        if (pfContent) {
            var pfField = document.getElementById('snapshot-pageforge');
            if (pfField) {
                pfField.value = pfContent;
                populated = true;
            }
            sessionStorage.removeItem('pageforge_snapshot_pf');
        }

        if (humanContent) {
            var humanField = document.getElementById('snapshot-human');
            if (humanField) {
                humanField.value = humanContent;
                populated = true;
            }
            sessionStorage.removeItem('pageforge_snapshot_human');
        }

        if (snapshotFile) {
            var sourceSelect = document.getElementById('snapshot-source-file');
            if (sourceSelect) {
                // Auto-select the matching option
                for (var i = 0; i < sourceSelect.options.length; i++) {
                    if (sourceSelect.options[i].value === snapshotFile) {
                        sourceSelect.selectedIndex = i;
                        break;
                    }
                }
            }
            sessionStorage.removeItem('pageforge_snapshot_file');
        }

        // Trigger form validation if we populated anything
        if (populated && this.calibrationManager) {
            this.calibrationManager._updateLogButtonState();
        }
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
}

// ------------------------------------------------------------------
// Boot
// ------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    window.calibrateApp = new CalibrateApp();
});
