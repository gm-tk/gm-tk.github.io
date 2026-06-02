'use strict';

/**
 * ModuleResultsPage — Module Development mode results / download screen (Session 3).
 *
 * Reached after Activate runs the Session 2 conversion: ModeToggle._finishConversion
 * calls ModuleResultsPage.present() once the converted outputs are on
 * ModeToggle.moduleOutputs. This screen is purely a DOWNLOAD SURFACE — it lists
 * the converted plain-text output file(s) (one per uploaded slot) and offers an
 * instant download control for each, reusing the existing OutputManager download
 * helper (the canonical Blob + URL.createObjectURL + <a download> + click + revoke
 * primitive in js/output-manager.js#downloadFile). It deliberately carries NO
 * phase/template controls and NO HTML preview, and exposes a single control to
 * return to the Module Development front page — mirroring Standard mode's "Parse
 * Another File" reset, which simply toggles section `.hidden` visibility.
 *
 * Mirroring ModeToggle, this is a state machine first and a DOM adapter second:
 * all navigation/output state lives in pure methods so the DOM-less Node test
 * runner can exercise it directly, and every DOM touch is isolated behind an
 * injected `document` and degrades to a no-op when an element is absent.
 */
class ModuleResultsPage {
    /**
     * @param {Object} [options]
     * @param {Document} [options.document] - Document to bind against (browser).
     *        Omit in unit tests to run as a pure state machine.
     * @param {Object} [options.outputManager] - Download helper owner. Defaults
     *        lazily to a fresh browser-global OutputManager; injectable so tests
     *        can assert the helper is called with the right filename + content.
     * @param {Function} [options.onReturn] - Optional hook fired after returning
     *        to the front page (browser bootstrap may re-sync). Omitted in tests.
     */
    constructor(options) {
        options = options || {};
        this._document = options.document || null;
        this._outputManager = options.outputManager || null;
        this._onReturn = options.onReturn || null;

        /** @type {Array<{source: string, filename: string, content: string}>} */
        this.outputs = [];
        /** @type {boolean} Whether the results screen is the active surface. */
        this.visible = false;

        /** Resolved DOM element references (populated by init when bound). */
        this.els = {};

        if (this._document) {
            this.init();
        }
    }

    // ------------------------------------------------------------------
    // Pure state (no DOM required)
    // ------------------------------------------------------------------

    /** @returns {Array} A copy of the outputs currently shown. */
    getOutputs() {
        return this.outputs.slice();
    }

    /** @returns {boolean} Whether at least one output is present. */
    hasOutputs() {
        return this.outputs.length > 0;
    }

    /** @returns {boolean} Whether the results screen is the visible surface. */
    isResultsVisible() {
        return this.visible;
    }

    /**
     * The download items the screen presents — one per produced output, in the
     * order produced. Pure, derived from the stored outputs so tests can assert
     * which downloads appear without a DOM.
     * @returns {Array<{source: string, label: string, filename: string}>}
     */
    getDownloadItems() {
        return this.outputs.map(function (o) {
            return {
                source: o.source,
                label: ModuleResultsPage.SLOT_LABELS[o.source] || o.source,
                filename: o.filename
            };
        });
    }

    /**
     * The controls the results screen owns, by kind: one `download` per output
     * plus one `back` control. It declares NO `selector` (phase/template) and NO
     * `preview` control — the screen is purely a download surface. Mirrors the
     * ModeToggle.getControlManifest contract so the "no phase/template/preview"
     * invariant is assertable headlessly.
     * @returns {Array<{kind: string, source?: string, filename?: string}>}
     */
    getControlManifest() {
        var controls = this.outputs.map(function (o) {
            return { kind: 'download', source: o.source, filename: o.filename };
        });
        controls.push({ kind: 'back' });
        return controls;
    }

    /**
     * The ordered next-steps instructions shown beneath the downloads — pure so
     * the content (and its step count) is assertable without a DOM. Each entry
     * is the inner HTML of one ordered-list step.
     * @returns {Array<string>}
     */
    getNextSteps() {
        return ModuleResultsPage.NEXT_STEPS.slice();
    }

    // ------------------------------------------------------------------
    // Navigation (DOM adapter — no-ops when unbound or an element is absent)
    // ------------------------------------------------------------------

    /**
     * Show the results screen for the given outputs: store them, render the
     * download list (or an empty-state when none), hide the Module Development
     * front page and reveal the results section.
     * @param {Array<{source: string, filename: string, content: string}>} outputs
     * @returns {Array} The outputs now shown.
     */
    show(outputs) {
        this.outputs = Array.isArray(outputs) ? outputs.slice() : [];
        this._renderList();
        this._renderNextSteps();
        this.visible = true;
        this._setHidden(this.els.frontSection, true);
        this._setHidden(this.els.resultsSection, false);
        return this.outputs;
    }

    /**
     * Return to the Module Development front page — mirrors Standard mode's
     * reset: hide the results section, reveal the front page. The produced
     * outputs are left intact (a fresh Activate re-renders them).
     */
    returnToFrontPage() {
        this.visible = false;
        this._setHidden(this.els.resultsSection, true);
        this._setHidden(this.els.frontSection, false);
        if (typeof this._onReturn === 'function') {
            this._onReturn();
        }
    }

    // ------------------------------------------------------------------
    // Download (reuses the existing OutputManager helper)
    // ------------------------------------------------------------------

    /**
     * Download one produced output by filename via the existing OutputManager
     * helper: register the {filename, content} on first use, then call its
     * downloadFile() (the canonical Blob + object-URL + anchor-click primitive).
     * @param {string} filename
     * @returns {boolean} Whether a matching output was found and downloaded.
     */
    triggerDownload(filename) {
        var output = this._findOutput(filename);
        if (!output) {
            return false;
        }
        var om = this._getOutputManager();
        if (!om) {
            return false;
        }
        if (typeof om.getFile === 'function' && !om.getFile(output.filename)) {
            om.addFile({
                filename: output.filename,
                content: output.content,
                type: 'text',
                pageType: 'text'
            });
        }
        om.downloadFile(output.filename);
        return true;
    }

    _findOutput(filename) {
        for (var i = 0; i < this.outputs.length; i++) {
            if (this.outputs[i].filename === filename) {
                return this.outputs[i];
            }
        }
        return null;
    }

    _getOutputManager() {
        if (!this._outputManager && typeof OutputManager !== 'undefined') {
            this._outputManager = new OutputManager();
        }
        return this._outputManager;
    }

    // ------------------------------------------------------------------
    // DOM adapter
    // ------------------------------------------------------------------

    /**
     * Resolve element references and bind the back control. Only runs when a
     * document was supplied; every lookup tolerates an absent element.
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
            resultsSection: get('module-results-section'),
            frontSection: get('module-dev-section'),
            list: get('module-results-list'),
            empty: get('module-results-empty'),
            nextSteps: get('module-next-steps'),
            backBtn: get('btn-module-back'),
            modeModuleRadio: get('mode-option-module'),
            modeStandardRadio: get('mode-option-standard')
        };
        this._bindBack();
        this._bindModeReset();
    }

    _bindBack() {
        var self = this;
        if (this.els.backBtn && this.els.backBtn.addEventListener) {
            this.els.backBtn.addEventListener('click', function () {
                self.returnToFrontPage();
            });
        }
    }

    /**
     * Switching top-level mode while the results screen is up must not leave it
     * stacked over the other front page. Bind both mode radios to hide the
     * results section on change; ModeToggle._applyVisibility owns which FRONT
     * page is then shown, so this only ever hides (never reveals) a section.
     */
    _bindModeReset() {
        var self = this;
        function onModeChange() { self._hideForModeChange(); }
        [this.els.modeModuleRadio, this.els.modeStandardRadio].forEach(function (radio) {
            if (radio && radio.addEventListener) {
                radio.addEventListener('change', onModeChange);
            }
        });
    }

    /** Hide the results surface (only) when the top-level mode changes. */
    _hideForModeChange() {
        this.visible = false;
        this._setHidden(this.els.resultsSection, true);
    }

    /**
     * Render the download list into #module-results-list (one styled row + a
     * Download button per output), or reveal the empty-state when there are no
     * outputs. No-ops when the list element is absent (headless).
     */
    _renderList() {
        var list = this.els.list;
        if (!list) {
            return;
        }
        if (!this.hasOutputs()) {
            list.innerHTML = '';
            this._setHidden(this.els.empty, false);
            return;
        }
        this._setHidden(this.els.empty, true);
        var html = '';
        for (var i = 0; i < this.outputs.length; i++) {
            var o = this.outputs[i];
            var label = ModuleResultsPage.SLOT_LABELS[o.source] || o.source;
            html +=
                '<div class="file-entry" data-filename="' + this._escAttr(o.filename) + '">' +
                    '<div class="file-info">' +
                        '<span class="file-icon" aria-hidden="true">📄</span>' +
                        '<div class="file-details">' +
                            '<span class="file-name">' + this._esc(o.filename) + '</span>' +
                            '<span class="file-meta">' + this._esc(label) + '</span>' +
                        '</div>' +
                    '</div>' +
                    '<div class="file-actions">' +
                        '<button class="btn btn-primary module-download" type="button" ' +
                            'data-filename="' + this._escAttr(o.filename) + '" ' +
                            'title="Download ' + this._escAttr(o.filename) + '">' +
                            '💾 Download</button>' +
                    '</div>' +
                '</div>';
        }
        list.innerHTML = html;
        this._bindDownloads(list);
    }

    _bindDownloads(list) {
        var self = this;
        if (!list.querySelectorAll) {
            return;
        }
        var btns = list.querySelectorAll('.module-download');
        for (var i = 0; i < btns.length; i++) {
            (function (btn) {
                if (btn.addEventListener) {
                    btn.addEventListener('click', function () {
                        self.triggerDownload(btn.getAttribute('data-filename'));
                    });
                }
            })(btns[i]);
        }
    }

    /**
     * Render the next-steps instructions panel into #module-next-steps whenever
     * there is at least one output to act on: a heading plus the canonical
     * ordered (numbered) list of conversion steps. Clears + hides the panel in
     * the empty state. No-ops when the panel element is absent (headless).
     */
    _renderNextSteps() {
        var panel = this.els.nextSteps;
        if (!panel) {
            return;
        }
        if (!this.hasOutputs()) {
            panel.innerHTML = '';
            this._setHidden(panel, true);
            return;
        }
        var steps = ModuleResultsPage.NEXT_STEPS;
        var items = '';
        for (var i = 0; i < steps.length; i++) {
            items += '<li>' + steps[i] + '</li>';
        }
        panel.innerHTML =
            '<h3 class="next-steps-title">' + ModuleResultsPage.NEXT_STEPS_HEADING + '</h3>' +
            '<ol class="next-steps-list">' + items + '</ol>';
        this._setHidden(panel, false);
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

    _esc(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    _escAttr(s) {
        return this._esc(s).replace(/"/g, '&quot;');
    }
}

// Static contracts assigned post-declaration (kept visible to the vm-loaded Node
// test runner and free of static-class-field support concerns).
ModuleResultsPage.SLOT_LABELS = {
    template: "Writer's Template",
    mediaList: 'Media List'
};

// Next-steps instructions shown beneath the downloads. Author-controlled UI
// chrome (not writer content), so the inline <code> markup is embedded directly.
ModuleResultsPage.NEXT_STEPS_HEADING =
    'Next steps — convert these files into finalized HTML';
ModuleResultsPage.NEXT_STEPS = [
    'Log in to the CS Claude account. On the sign-in screen, ' +
        'choose the <code>Continue with Google</code> option — do not sign ' +
        'in with the email option.',
    'Once you are logged in, open the <code>HTML Convertor</code> project.',
    'Inside that project, start a new chat.',
    'Into that new chat, upload all three files:' +
        '<ol type="a" class="next-steps-sublist">' +
            '<li>the Writer’s Template <code>.txt</code></li>' +
            '<li>the Media List <code>.txt</code></li>' +
            '<li>HTML files of an example module as a reference</li>' +
        '</ol>',
    'Submit the message to have the content converted into the finalized HTML files.'
];

/**
 * Show (lazily creating + caching the page on the toggle) the results screen for
 * the outputs a ModeToggle conversion just produced. Called from
 * ModeToggle._finishConversion so navigation happens automatically when the
 * Activate conversion completes. No-ops gracefully when bound to a document-less
 * toggle (the DOM-less test runner).
 *
 * @param {Object} toggle - The ModeToggle instance (provides `_document`).
 * @param {Array} outputs - The converted output descriptors.
 * @returns {?ModuleResultsPage}
 */
ModuleResultsPage.present = function (toggle, outputs) {
    if (!toggle) {
        return null;
    }
    if (!toggle._resultsPage) {
        toggle._resultsPage = new ModuleResultsPage({ document: toggle._document });
    }
    toggle._resultsPage.show(outputs);
    return toggle._resultsPage;
};
