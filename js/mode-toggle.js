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
 *   • Page Stitcher mode — a separate front page (#stitch-section) for
 *     recombining a SPLIT-MODE module (base homepage + per-section files) into
 *     one single-page module. Its controls are owned by PageStitcherMode; this
 *     shell only switches it in/out of view.
 *
 * This module owns ONLY the mode shell: the toggle, the Module Development
 * front-page state (which files are staged, whether Activate is enabled) and
 * the visibility relationship between the two front pages, and orchestrates the
 * Activate conversion (Session 2) plus navigation to the results/download
 * screen (Session 3), each delegated to a dedicated sibling sub-module.
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
         * Staged Word documents — 1–2 `.docx` (a Writer's Template and/or a Media
         * List, dropped into one container and auto-classified by content at
         * Convert). An array so the upload area accepts one or more files.
         * @type {Array}
         */
        this.docxFiles = [];

        /** Resolved DOM element references (populated by init when bound). */
        this.els = {};

        this._document = options.document || null;

        // Conversion dependencies — constructor-injected so the conversion flow
        // is headless-testable; each defaults to the corresponding browser
        // global (lazily, via the _get* accessors) when omitted.
        this._parser = options.parser || null;
        this._parserFactory = options.parserFactory || null;
        this._formatter = options.formatter || null;
        this._mediaListConverter = options.mediaListConverter || null;
        this._filenameHelper = options.filenameHelper || null;

        // Comment-capture dependencies (additive; all optional + lazily defaulted
        // to browser globals).
        this._commentInserter = options.commentInserter || null;
        this._commentData = options.commentData || null;
        this._notify = options.notify || null;

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

    /** @returns {string} The active mode ('module' | 'stitcher'). */
    getMode() {
        return this.mode;
    }

    /** @returns {boolean} True when Module Development mode is active. */
    isModuleDevMode() {
        return this.mode === ModeToggle.MODES.MODULE;
    }

    /** @returns {boolean} True when Page Stitcher mode is active. */
    isStitcherMode() {
        return this.mode === ModeToggle.MODES.STITCHER;
    }

    /**
     * Activate a mode and synchronise the DOM (when bound). Unknown values are
     * ignored so a stray radio value can never desync the shell.
     *
     * @param {string} mode - 'module' | 'stitcher'
     * @returns {string} The active mode after the call.
     */
    setMode(mode) {
        if (mode !== ModeToggle.MODES.MODULE && mode !== ModeToggle.MODES.STITCHER) {
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
            ? ModeToggle.MODES.STITCHER
            : ModeToggle.MODES.MODULE);
    }

    /** @returns {boolean} Whether the Module Development front page is visible. */
    isModuleDevVisible() {
        return this.isModuleDevMode();
    }

    /** @returns {boolean} Whether the Page Stitcher front page (#stitch-section) is visible. */
    isStitcherVisible() {
        return this.isStitcherMode();
    }

    // ------------------------------------------------------------------
    // Module Development upload state (pure — no DOM required)
    // ------------------------------------------------------------------

    /**
     * Record (or clear) the staged Word documents — 1–2 `.docx` (a Writer's
     * Template and/or a Media List, in any order, dropped into one container).
     * They are auto-classified by content at Convert.
     * @param {Array|FileList} files
     * @returns {number} How many .docx are now staged.
     */
    setDocxFiles(files) {
        this.docxFiles = this._toArray(files);
        this._renderDocx();
        this._syncActivate();
        return this.docxFiles.length;
    }

    /** @returns {boolean} Whether any Word documents are staged. */
    hasDocx() {
        return Array.isArray(this.docxFiles) && this.docxFiles.length > 0;
    }

    /** Normalise a FileList/array to a plain array. */
    _toArray(files) {
        var arr = [];
        if (files && files.length) { for (var i = 0; i < files.length; i++) { arr.push(files[i]); } }
        return arr;
    }

    /**
     * Activate is enabled when at least one Word document (a Writer's Template
     * and/or a Media List) is staged.
     * @returns {boolean}
     */
    isActivateEnabled() {
        return this.hasDocx();
    }

    /**
     * Boolean snapshot of the upload area, for the UI and for tests.
     * @returns {{ docx: boolean }}
     */
    getUploadState() {
        return { docx: this.hasDocx() };
    }

    /**
     * Full session reset for the Module Development flow: discard every staged
     * document and any produced outputs, clear the file input, and re-sync the
     * front page (empty staged-file info, Convert disabled). This backs the
     * results screen's "Convert another module" control. (The "Back" control
     * instead returns to the front page WITHOUT clearing, so the user can
     * re-check what they uploaded.)
     * @returns {{ docx: boolean }} The (now empty) upload state.
     */
    resetSession() {
        this.docxFiles = [];
        this.moduleOutputs = null;
        if (this.els && this.els.docxInput) {
            // Clear the native picker so the same file can be re-selected and the
            // control no longer reports the previous selection.
            try { this.els.docxInput.value = ''; } catch (e) { /* some inputs disallow */ }
        }
        this._renderDocx();
        this._syncActivate();
        return this.getUploadState();
    }

    // ------------------------------------------------------------------
    // Control manifest (declarative contract — pure)
    // ------------------------------------------------------------------

    /**
     * The controls each front page owns, by kind. Module Development exposes one
     * upload slot and one button and NO selector (phase/template) controls;
     * Page Stitcher exposes a base-homepage upload, a lessons multi-upload and a
     * Stitch button.
     *
     * @param {string} mode - 'module' | 'stitcher'
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
     * Activate handler. Parses each staged `.docx` once (carrying its native
     * comments), AUTO-CLASSIFIES each as a Writer's Template (has a `[TITLE BAR]`)
     * or a Media List (no title bar / has a media table), and stores one output
     * per produced file on `this.moduleOutputs` for the results screen:
     *   • Writer's Template → OutputFormatter.formatAll() from contentStartIndex.
     *   • Media List → MediaListConverter.convertParsedResult().
     *
     * Additively performs native Word COMMENT CAPTURE: surviving Creative-Services
     * comments surface as red notes in the Writer's Template .txt (body-anchored +
     * Media-List-row comments matched into the body by media id); for a media-only
     * upload, surviving media comments are appended to the Media List .txt + toast.
     *
     * Returns a Promise (browser, async parse) or the output array directly
     * (sync test mocks). No files staged → no-op: returns [], state stays null.
     * @returns {(Array|Promise<Array>)}
     */
    handleModuleConversion() {
        if (!this.isActivateEnabled()) {
            return []; // no files staged → no-op
        }
        var self = this;
        // Parse every staged .docx once, each on its OWN parser instance (a
        // shared parser would let two concurrent async parses clobber each
        // other — see _makeParser), keeping the source File alongside its parse.
        var docxItems = this.docxFiles.map(function (f) {
            return ModeToggle._resolveMaybe(self._makeParser().parse(f), function (res) {
                return { file: f, result: res };
            });
        });
        return this._resolveArray(docxItems, function (items) {
            return self._buildModuleOutputs(items);
        });
    }

    /**
     * Classify each parsed .docx (Writer's Template vs Media List), run comment
     * capture (the first Writer's Template receives the first Media List's
     * media-row comments matched into its body), and assemble ONE output per
     * uploaded document. EVERY input is converted and surfaced — a document is
     * never silently dropped. Outputs keep Writer's-Template(s) first, Media
     * List(s) second; a filename collision (e.g. two same-kind docs) is
     * disambiguated so each stays separately downloadable.
     */
    _buildModuleOutputs(docxItems) {
        var self = this;
        var templates = [], mediaLists = [];
        docxItems.forEach(function (it) {
            if (!it || !it.result) { return; }
            if (self._classifyDocx(it.result, it.file) === 'mediaList') {
                mediaLists.push(it);
            } else {
                templates.push(it);
            }
        });

        var inserter = this._getCommentInserter();
        var firstWt = templates[0] || null;
        var firstMl = mediaLists[0] || null;
        var mlMediaComments = firstMl ? this._mediaCommentsFrom(firstMl.result) : [];

        var outputs = [];

        templates.forEach(function (it) {
            if (inserter && it === firstWt) {
                try {
                    // Annotate the parsed blocks with red comment notes in place
                    // (WT body comments + Media-List media-row comments), then
                    // the existing formatAll() emits them.
                    inserter.captureIntoTemplate(it.result, mlMediaComments);
                } catch (e) { /* comment capture must never break conversion */ }
            }
            outputs.push({
                source: 'template',
                _file: it.file,
                _label: 'Writers Template',
                _result: it.result,
                content: self._getFormatter().formatAll(it.result).full
            });
        });

        mediaLists.forEach(function (it) {
            var mediaText = self._getMediaListConverter().convertParsedResult(it.result);
            if (!firstWt && inserter && it === firstMl) {
                // Media-only upload: surviving media comments have no body to
                // attach to — append them to the Media List .txt and toast.
                try {
                    var fb = inserter.renderMediaOnly(mlMediaComments);
                    if (fb && fb.notes && fb.notes.length) {
                        mediaText = mediaText + '\n\n' + fb.header + '\n' + fb.notes.join('\n');
                        self._notifyToast(fb.toast);
                    }
                } catch (e) { /* fallback is best-effort */ }
            }
            outputs.push({ source: 'mediaList', _file: it.file, _label: 'Media List', _result: it.result, content: mediaText });
        });

        this._assignOutputFilenames(outputs);
        return this._finishConversion(outputs);
    }

    /**
     * Resolve each output's `<CODE> <label>_parsed.txt` filename, disambiguating a
     * collision (e.g. two documents classified alike) with a numeric suffix so
     * every uploaded document stays separately downloadable. Strips the transient
     * `_file`/`_label` carriers, leaving each output as {source, filename, content}.
     */
    _assignOutputFilenames(outputs) {
        var used = {};
        for (var i = 0; i < outputs.length; i++) {
            var o = outputs[i];
            var base = this._deriveFilename(o._file, o._label, o._result);
            var name = base;
            if (used[base]) {
                var dot = base.lastIndexOf('.');
                var stem = (dot === -1) ? base : base.slice(0, dot);
                var ext = (dot === -1) ? '' : base.slice(dot);
                name = stem + ' (' + (used[base] + 1) + ')' + ext;
            }
            used[base] = (used[base] || 0) + 1;
            o.filename = name;
            delete o._file;
            delete o._label;
            delete o._result;
        }
    }

    /**
     * Classify a parsed .docx: 'template' (has a [TITLE BAR]) or 'mediaList' (no
     * title bar AND a recognised media table, or a "media list" filename). Defaults
     * to 'template' so an unrecognised doc never silently loses its content.
     */
    _classifyDocx(result, file) {
        if (result && result.contentStartFound) { return 'template'; }
        var mlc = this._getMediaListConverter();
        if (mlc && typeof mlc.hasMediaTable === 'function' && mlc.hasMediaTable(result)) {
            return 'mediaList';
        }
        if (/media\s*list/i.test((file && file.name) || '')) { return 'mediaList'; }
        return 'template';
    }

    /** Media-row comments (carrying rowUrl/rowUrls) from a parsed result. */
    _mediaCommentsFrom(result) {
        var out = [];
        var content = (result && result.content) || [];
        for (var i = 0; i < content.length; i++) {
            var cs = content[i] && content[i].comments;
            if (!cs) { continue; }
            for (var j = 0; j < cs.length; j++) {
                var c = cs[j];
                if (c && (c.rowUrl || (c.rowUrls && c.rowUrls.length))) { out.push(c); }
            }
        }
        return out;
    }

    /** Persist the converted outputs and navigate to the results screen. */
    _finishConversion(outputs) {
        this.moduleOutputs = outputs;
        ModuleResultsPage.present(this, outputs);
        return outputs;
    }

    /**
     * Standardised Module Development output filename `<MODULE_CODE> <label>_parsed.txt`:
     * the module code is the input filename's leading token (any descriptive middle
     * segment dropped); both outputs use the unified `_parsed.txt` suffix (the Media
     * List is no longer `_media_list`); <label> is "Writers Template"/"Media List".
     * The module code is resolved from the document (metadata.moduleCode) or the
     * filename (see ModeToggleFilename), so junk around the code is discarded.
     */
    _deriveFilename(file, label, result) {
        return (this._filenameHelper || ModeToggleFilename).deriveFilename(file, label, result);
    }

    // ------------------------------------------------------------------
    // Lazy dependency accessors — injected instance wins, else browser global.
    // ------------------------------------------------------------------

    /**
     * A parser for ONE document. `DocxParser` carries per-document state and its
     * `parse()` is async, so a single shared instance parsing two uploads
     * concurrently would corrupt the second result (the Media List comes back
     * wearing the Writer's Template's content). Hand out a FRESH parser per
     * document instead. An injected factory wins (tests use it to prove per-file
     * isolation); a single injected parser is reused as-is (a stateless sync
     * mock); otherwise build a new DocxParser each call.
     */
    _makeParser() {
        if (this._parserFactory) { return this._parserFactory(); }
        if (this._parser) { return this._parser; }
        if (typeof DocxParser !== 'undefined') { return new DocxParser(); }
        return null;
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

    /** The comment-author whitelist/filter data (injected or browser global). */
    _getCommentData() {
        if (this._commentData) { return this._commentData; }
        if (typeof window !== 'undefined' && window.PageForgeCommentAuthors) {
            return window.PageForgeCommentAuthors;
        }
        return null;
    }

    /**
     * The comment inserter, built lazily from the loaded data. Returns null when
     * the comment modules or the data aren't available (→ capture is a no-op),
     * which is what keeps the inherited conversion flow byte-identical in tests.
     */
    _getCommentInserter() {
        if (this._commentInserter) { return this._commentInserter; }
        if (typeof CommentInserter === 'undefined' || typeof CommentFilter === 'undefined') {
            return null;
        }
        var data = this._getCommentData();
        if (!data) { return null; }
        this._commentInserter = new CommentInserter({
            filter: new CommentFilter(data),
            formatter: this._getFormatter(),
            mediaMatch: data.media_match || null,
            notePrefix: (data.render && data.render.prefix) || undefined
        });
        return this._commentInserter;
    }

    /** Surface a user-facing toast (injected sink in tests, else the global). */
    _notifyToast(message) {
        if (!message) { return; }
        if (typeof this._notify === 'function') { this._notify(message); return; }
        if (typeof window !== 'undefined' && window.pageForgeToast &&
            typeof window.pageForgeToast.show === 'function') {
            window.pageForgeToast.show(message);
        }
    }

    // ------------------------------------------------------------------
    // Async plumbing
    // ------------------------------------------------------------------

    /** Resolve an array of maybe-promise values, then call fn. Sync when all sync. */
    _resolveArray(arr, fn) {
        var anyThenable = arr.some(function (v) { return v && typeof v.then === 'function'; });
        if (!anyThenable) { return fn(arr); }
        return Promise.all(arr.map(function (v) { return Promise.resolve(v); })).then(fn);
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
            stitcherSection: get('stitch-section'),
            modeModuleRadio: get('mode-option-module'),
            modeStitcherRadio: get('mode-option-stitcher'),
            docxInput: get('module-docx-input'),
            docxDrop: get('module-docx-drop'),
            docxInfo: get('module-docx-info'),
            docxName: get('module-docx-name'),
            activateBtn: get('btn-module-activate')
        };

        this._bindModeEvents();
        this._bindDocxSlot();
        this._bindActivate();

        this._applyVisibility();
        this._syncActivate();
    }

    _bindModeEvents() {
        var self = this;
        function onChange(e) {
            var value = e && e.target && e.target.value;
            if (!value) {
                value = (self.els.modeStitcherRadio && self.els.modeStitcherRadio.checked)
                    ? ModeToggle.MODES.STITCHER
                    : ModeToggle.MODES.MODULE;
            }
            self.setMode(value);
        }
        if (this.els.modeModuleRadio && this.els.modeModuleRadio.addEventListener) {
            this.els.modeModuleRadio.addEventListener('change', onChange);
        }
        if (this.els.modeStitcherRadio && this.els.modeStitcherRadio.addEventListener) {
            this.els.modeStitcherRadio.addEventListener('change', onChange);
        }
    }

    /** Bind the Word-documents container (1–2 .docx; click / keyboard / drag-drop). */
    _bindDocxSlot() {
        var self = this;
        var input = this.els.docxInput, drop = this.els.docxDrop;
        if (input && input.addEventListener) {
            input.addEventListener('change', function () { self.setDocxFiles(input.files); });
        }
        if (drop && drop.addEventListener) {
            drop.addEventListener('click', function () { if (input && input.click) { input.click(); } });
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
                if (files && files.length) { self.setDocxFiles(files); }
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
        this._setHidden(this.els.stitcherSection, moduleActive);
        if (this.els.modeModuleRadio) { this.els.modeModuleRadio.checked = moduleActive; }
        if (this.els.modeStitcherRadio) { this.els.modeStitcherRadio.checked = !moduleActive; }
    }

    /** Reflect the Word-documents container's staged state — the file name(s). */
    _renderDocx() {
        if (this.els.docxName) {
            this.els.docxName.textContent = this.hasDocx()
                ? this.docxFiles.map(function (f) { return (f && f.name) || 'document.docx'; }).join(', ')
                : '';
        }
        this._setHidden(this.els.docxInfo, !this.hasDocx());
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
ModeToggle.MODES = { MODULE: 'module', STITCHER: 'stitcher' };
ModeToggle.UPLOAD_SLOTS = ['docx'];
ModeToggle.CONTROL_MANIFEST = {
    module: [
        { id: 'module-docx-input', kind: 'upload', slot: 'docx' },
        { id: 'btn-module-activate', kind: 'button' }
    ],
    stitcher: [
        { id: 'stitch-input', kind: 'upload', slot: 'files' },
        { id: 'btn-stitch', kind: 'button' }
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
