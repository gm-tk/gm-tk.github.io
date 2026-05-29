'use strict';

/**
 * ModeToggle — top-level mode shell for PageForge (Module Development Mode, Session 1).
 *
 * PageForge now exposes two top-level modes selected via a two-option switch
 * rendered above both front-page bodies:
 *
 *   • Module Development mode (default on load) — a streamlined front page with
 *     two independent, optional .docx upload slots (Writer's Template + Media
 *     List) and a single Activate button. It carries NO phase selector, NO
 *     template selector and NO HTML-related controls.
 *   • Standard mode — the existing PageForge front page (#upload-section) with
 *     its drop zone, template selector and Convert button, shown unchanged.
 *
 * This module owns ONLY the mode shell: the toggle, the Module Development
 * front-page state (which files are staged, whether Activate is enabled) and
 * the visibility relationship between the two front pages. It deliberately
 * contains NO conversion logic — handleModuleConversion() is a stub left for
 * Session 2, and there is no results/download page yet (Session 3).
 *
 * Design for testability: the class is a state machine first and a DOM adapter
 * second. All mode/upload state lives in plain properties and pure methods so
 * the Node test runner (which has no DOM) can exercise it directly. Every DOM
 * touch is isolated behind an injected `document` and degrades to a no-op when
 * an element is absent.
 */
class ModeToggle {
    /**
     * @param {Object} [options]
     * @param {Document} [options.document] - Document to bind against (browser).
     *        Omit in unit tests to run as a pure state machine.
     * @param {boolean} [options.autoInit=true] - When a document is supplied,
     *        resolve elements + bind events immediately.
     */
    constructor(options) {
        options = options || {};

        /** @type {string} Active mode — defaults to Module Development. */
        this.mode = ModeToggle.MODES.MODULE;

        /**
         * Staged files for the two Module Development upload slots. Each value
         * is the staged File (browser) or a marker object (tests); null = empty.
         * @type {{ template: *, mediaList: * }}
         */
        this.uploads = { template: null, mediaList: null };

        /** Resolved DOM element references (populated by init when bound). */
        this.els = {};

        this._document = options.document || null;

        // Conversion dependencies — constructor-injected so the conversion flow
        // is headless-testable; each defaults to the corresponding browser
        // global (lazily, via the _get* accessors) when omitted.
        this._parser = options.parser || null;
        this._formatter = options.formatter || null;
        this._mediaListConverter = options.mediaListConverter || null;

        /**
         * Converted output files for the Session 3 results page to consume. Each
         * entry is { source, filename, content }; one per uploaded slot. Stays
         * null until Activate runs a (non-no-op) conversion.
         * @type {?Array<{source: string, filename: string, content: string}>}
         */
        this.moduleOutputs = null;

        if (this._document && options.autoInit !== false) {
            this.init();
        }
    }

    // ------------------------------------------------------------------
    // Mode state (pure — no DOM required)
    // ------------------------------------------------------------------

    /** @returns {string} The active mode ('module' | 'standard'). */
    getMode() {
        return this.mode;
    }

    /** @returns {boolean} True when Module Development mode is active. */
    isModuleDevMode() {
        return this.mode === ModeToggle.MODES.MODULE;
    }

    /** @returns {boolean} True when Standard mode is active. */
    isStandardMode() {
        return this.mode === ModeToggle.MODES.STANDARD;
    }

    /**
     * Activate a mode and synchronise the DOM (when bound). Unknown values are
     * ignored so a stray radio value can never desync the shell.
     *
     * @param {string} mode - 'module' | 'standard'
     * @returns {string} The active mode after the call.
     */
    setMode(mode) {
        if (mode !== ModeToggle.MODES.MODULE && mode !== ModeToggle.MODES.STANDARD) {
            return this.mode;
        }
        this.mode = mode;
        this._applyVisibility();
        return this.mode;
    }

    /**
     * Flip to the opposite mode.
     * @returns {string} The active mode after toggling.
     */
    toggleMode() {
        return this.setMode(this.isModuleDevMode()
            ? ModeToggle.MODES.STANDARD
            : ModeToggle.MODES.MODULE);
    }

    /** @returns {boolean} Whether the Module Development front page is visible. */
    isModuleDevVisible() {
        return this.isModuleDevMode();
    }

    /** @returns {boolean} Whether the Standard front page (#upload-section) is visible. */
    isStandardVisible() {
        return this.isStandardMode();
    }

    // ------------------------------------------------------------------
    // Module Development upload state (pure — no DOM required)
    // ------------------------------------------------------------------

    /**
     * Record (or clear) a staged file for one of the two upload slots.
     *
     * @param {string} slot - 'template' | 'mediaList'
     * @param {*} file - The staged File, or null/undefined to clear the slot.
     * @returns {boolean} Whether the slot now holds a file.
     */
    setUpload(slot, file) {
        if (!this.uploads.hasOwnProperty(slot)) {
            return false;
        }
        this.uploads[slot] = file || null;
        this._renderSlot(slot);
        this._syncActivate();
        return !!this.uploads[slot];
    }

    /**
     * Clear a staged file from a slot.
     * @param {string} slot - 'template' | 'mediaList'
     */
    clearUpload(slot) {
        this.setUpload(slot, null);
    }

    /**
     * @param {string} slot - 'template' | 'mediaList'
     * @returns {boolean} Whether the slot currently holds a file.
     */
    hasUpload(slot) {
        return !!(this.uploads.hasOwnProperty(slot) && this.uploads[slot]);
    }

    /** @returns {boolean} True when at least one of the two slots holds a file. */
    hasAnyUpload() {
        return this.hasUpload('template') || this.hasUpload('mediaList');
    }

    /**
     * Activate is enabled when at least one of the two optional files is staged
     * (template only, media list only, or both).
     * @returns {boolean}
     */
    isActivateEnabled() {
        return this.hasAnyUpload();
    }

    /**
     * Boolean snapshot of the two slots, for the UI and for tests.
     * @returns {{ template: boolean, mediaList: boolean }}
     */
    getUploadState() {
        return {
            template: this.hasUpload('template'),
            mediaList: this.hasUpload('mediaList')
        };
    }

    // ------------------------------------------------------------------
    // Control manifest (declarative contract — pure)
    // ------------------------------------------------------------------

    /**
     * The controls each front page owns, by kind. This is the contract the
     * static HTML and Sessions 2–3 must honour: Module Development exposes two
     * upload slots and one button and NO selector (phase/template) controls;
     * Standard keeps its file input, template selector and Convert button.
     *
     * @param {string} mode - 'module' | 'standard'
     * @returns {Array<{id: string, kind: string, slot?: string}>}
     */
    getControlManifest(mode) {
        var manifest = ModeToggle.CONTROL_MANIFEST[mode];
        return manifest ? manifest.slice() : [];
    }

    // ------------------------------------------------------------------
    // Conversion entry point (Session 2)
    // ------------------------------------------------------------------

    /**
     * Activate handler: convert whichever of the two optional files are staged
     * and store one output per slot on `this.moduleOutputs` for Session 3.
     *   • Writer's Template → the existing pipeline as-is (intro-skip NOT
     *     re-implemented): DocxParser.parse() runs the [TITLE BAR]
     *     _findContentStart boundary detection (discarding the leading generic
     *     statements + checklists), then OutputFormatter.formatAll() emits from
     *     contentStartIndex. See docs/31 for the full rationale.
     *   • Media List → MediaListConverter: straight full conversion, no skipping,
     *     no phase/template processing.
     * Returns a Promise (browser, async parse) or the output array directly
     * (sync test parser). No files staged → no-op: returns [], state stays null.
     * @returns {(Array|Promise<Array>)}
     */
    handleModuleConversion() {
        if (!this.isActivateEnabled()) {
            return []; // no files staged → no-op
        }
        var self = this;
        var slots = [];
        if (this.hasUpload('template')) { slots.push('template'); }
        if (this.hasUpload('mediaList')) { slots.push('mediaList'); }

        var results = slots.map(function (slot) { return self._convertSlot(slot); });
        if (results.some(function (r) { return r && typeof r.then === 'function'; })) {
            return Promise.all(results).then(function (outs) { return self._finishConversion(outs); });
        }
        return self._finishConversion(results);
    }

    /**
     * Convert one staged slot to an output descriptor { source, filename,
     * content }. Returns the descriptor directly, or a Promise of it when the
     * underlying parser is asynchronous (browser).
     * @param {string} slot - 'template' | 'mediaList'
     */
    _convertSlot(slot) {
        var self = this;
        var file = this.uploads[slot];
        if (slot === 'template') {
            // Reuse the existing writer's-template pipeline; the intro-skip lives
            // inside parse() (_findContentStart) + formatAll() (contentStartIndex).
            return ModeToggle._resolveMaybe(this._getParser().parse(file), function (result) {
                return {
                    source: 'template',
                    filename: self._deriveFilename(file, '_parsed.txt'),
                    content: self._getFormatter().formatAll(result).full
                };
            });
        }
        return ModeToggle._resolveMaybe(this._getMediaListConverter().convert(file), function (text) {
            return {
                source: 'mediaList',
                filename: self._deriveFilename(file, '_media_list.txt'),
                content: text
            };
        });
    }

    /** Persist the converted outputs to app state and return them. */
    _finishConversion(outputs) {
        this.moduleOutputs = outputs;
        return outputs;
    }

    /**
     * Derive a sensible output filename: the input stem (sans a trailing .docx,
     * case-insensitive) + the given suffix, with a safe fallback when the file
     * has no usable name. e.g. "ENGS301.docx" + "_parsed.txt" → "ENGS301_parsed.txt".
     */
    _deriveFilename(file, suffix) {
        var stem = ((file && file.name) ? String(file.name) : '').replace(/\.docx$/i, '').trim();
        if (!stem) { stem = (suffix.indexOf('media') !== -1) ? 'media-list' : 'writer-template'; }
        return stem + suffix;
    }

    // ------------------------------------------------------------------
    // Lazy dependency accessors — injected instance wins, else browser global.
    // ------------------------------------------------------------------

    _getParser() {
        if (!this._parser && typeof DocxParser !== 'undefined') { this._parser = new DocxParser(); }
        return this._parser;
    }

    _getFormatter() {
        if (!this._formatter && typeof OutputFormatter !== 'undefined') { this._formatter = new OutputFormatter(); }
        return this._formatter;
    }

    _getMediaListConverter() {
        if (!this._mediaListConverter && typeof MediaListConverter !== 'undefined') {
            this._mediaListConverter = new MediaListConverter();
        }
        return this._mediaListConverter;
    }

    // ------------------------------------------------------------------
    // DOM adapter (no-ops when unbound or an element is missing)
    // ------------------------------------------------------------------

    /**
     * Resolve element references, bind events and apply the initial (default)
     * mode. Only runs when a document was supplied; every lookup tolerates an
     * absent element so a partial document never throws.
     */
    init() {
        if (!this._document) {
            return;
        }
        var doc = this._document;
        function get(id) {
            return doc.getElementById ? doc.getElementById(id) : null;
        }

        this.els = {
            moduleSection: get('module-dev-section'),
            standardSection: get('upload-section'),
            modeModuleRadio: get('mode-option-module'),
            modeStandardRadio: get('mode-option-standard'),
            templateInput: get('module-template-input'),
            templateDrop: get('module-template-drop'),
            templateInfo: get('module-template-info'),
            templateName: get('module-template-name'),
            mediaInput: get('module-media-input'),
            mediaDrop: get('module-media-drop'),
            mediaInfo: get('module-media-info'),
            mediaName: get('module-media-name'),
            activateBtn: get('btn-module-activate')
        };

        this._bindModeEvents();
        this._bindSlotEvents('template', this.els.templateInput, this.els.templateDrop);
        this._bindSlotEvents('mediaList', this.els.mediaInput, this.els.mediaDrop);
        this._bindActivate();

        this._applyVisibility();
        this._syncActivate();
    }

    _bindModeEvents() {
        var self = this;
        function onChange(e) {
            var value = e && e.target && e.target.value;
            if (!value) {
                value = (self.els.modeStandardRadio && self.els.modeStandardRadio.checked)
                    ? ModeToggle.MODES.STANDARD
                    : ModeToggle.MODES.MODULE;
            }
            self.setMode(value);
        }
        if (this.els.modeModuleRadio && this.els.modeModuleRadio.addEventListener) {
            this.els.modeModuleRadio.addEventListener('change', onChange);
        }
        if (this.els.modeStandardRadio && this.els.modeStandardRadio.addEventListener) {
            this.els.modeStandardRadio.addEventListener('change', onChange);
        }
    }

    _bindSlotEvents(slot, input, drop) {
        var self = this;
        if (input && input.addEventListener) {
            input.addEventListener('change', function () {
                var file = input.files && input.files.length ? input.files[0] : null;
                self.setUpload(slot, file);
            });
        }
        if (drop && drop.addEventListener) {
            drop.addEventListener('click', function () {
                if (input && input.click) { input.click(); }
            });
            drop.addEventListener('keydown', function (e) {
                if (e && (e.key === 'Enter' || e.key === ' ')) {
                    if (e.preventDefault) { e.preventDefault(); }
                    if (input && input.click) { input.click(); }
                }
            });
            drop.addEventListener('dragover', function (e) {
                if (e && e.preventDefault) { e.preventDefault(); }
                if (drop.classList) { drop.classList.add('drag-over'); }
            });
            drop.addEventListener('dragleave', function () {
                if (drop.classList) { drop.classList.remove('drag-over'); }
            });
            drop.addEventListener('drop', function (e) {
                if (e && e.preventDefault) { e.preventDefault(); }
                if (drop.classList) { drop.classList.remove('drag-over'); }
                var files = e && e.dataTransfer && e.dataTransfer.files;
                if (files && files.length) {
                    self.setUpload(slot, files[0]);
                }
            });
        }
    }

    _bindActivate() {
        var self = this;
        if (this.els.activateBtn && this.els.activateBtn.addEventListener) {
            this.els.activateBtn.addEventListener('click', function () {
                self.handleModuleConversion();
            });
        }
    }

    /**
     * Toggle `.hidden` between the two front-page containers and keep the mode
     * radios in sync. No-ops for any element that is absent.
     */
    _applyVisibility() {
        var moduleActive = this.isModuleDevMode();
        this._setHidden(this.els.moduleSection, !moduleActive);
        this._setHidden(this.els.standardSection, moduleActive);
        if (this.els.modeModuleRadio) { this.els.modeModuleRadio.checked = moduleActive; }
        if (this.els.modeStandardRadio) { this.els.modeStandardRadio.checked = !moduleActive; }
    }

    /** Reflect a slot's staged state in its file-info indicator. */
    _renderSlot(slot) {
        var info = slot === 'template' ? this.els.templateInfo : this.els.mediaInfo;
        var name = slot === 'template' ? this.els.templateName : this.els.mediaName;
        var file = this.uploads[slot];
        if (name) {
            if (file && typeof file === 'object' && 'name' in file) {
                name.textContent = file.name;
            } else if (!file) {
                name.textContent = '';
            }
        }
        this._setHidden(info, !file);
    }

    /** Enable/disable the Activate button from current upload state. */
    _syncActivate() {
        if (this.els.activateBtn) {
            this.els.activateBtn.disabled = !this.isActivateEnabled();
        }
    }

    /** Add/remove the shared `.hidden` class, guarding missing elements. */
    _setHidden(el, hidden) {
        if (el && el.classList) {
            if (hidden) {
                el.classList.add('hidden');
            } else {
                el.classList.remove('hidden');
            }
        }
    }
}

// Static contracts assigned post-declaration to avoid static-class-field
// support concerns in older runtimes (and to keep them visible to the
// vm-loaded Node test runner).
ModeToggle.MODES = { MODULE: 'module', STANDARD: 'standard' };
ModeToggle.UPLOAD_SLOTS = ['template', 'mediaList'];
ModeToggle.CONTROL_MANIFEST = {
    module: [
        { id: 'module-template-input', kind: 'upload', slot: 'template' },
        { id: 'module-media-input', kind: 'upload', slot: 'mediaList' },
        { id: 'btn-module-activate', kind: 'button' }
    ],
    standard: [
        { id: 'file-input', kind: 'upload' },
        { id: 'template-dropdown', kind: 'selector' },
        { id: 'btn-convert', kind: 'button' }
    ]
};

/**
 * Resolve a value that may be a Promise (browser, async .docx parsing) or a
 * plain value (headless tests with a synchronous parser). Keeps the conversion
 * flow synchronously testable while remaining fully async in the browser.
 */
ModeToggle._resolveMaybe = function (value, fn) {
    return (value && typeof value.then === 'function') ? value.then(fn) : fn(value);
};

// Browser bootstrap — skipped under the DOM-less Node test runner.
if (typeof document !== 'undefined' && document.addEventListener) {
    document.addEventListener('DOMContentLoaded', function () {
        var toggle = new ModeToggle({ document: document });
        if (typeof window !== 'undefined') {
            window.pageForgeMode = toggle;
        }
    });
}
