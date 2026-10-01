'use strict';

/**
 * PageForgeToast — the standalone, user-facing toast notification.
 *
 * In V1 the toast lived on the Standard `App` class (`App.showToast`), which
 * rendered into the page's single `#toast` element. Standard mode is dropped in
 * this build, so the render logic is lifted VERBATIM into this small standalone
 * module (set `#toast` text, add the `visible` class, then remove it after the
 * same 3000 ms) and exposed as a global singleton, `window.pageForgeToast`.
 * `MediaListConverter`'s browser fallback now calls `window.pageForgeToast.show`
 * instead of the dropped Standard App's showToast.
 *
 * Engineering conventions (matches the carried-over modules):
 *   - State machine first, DOM adapter second: all DOM access is isolated behind
 *     an injected `document` and every method no-ops when `#toast` is absent, so
 *     the DOM-less Node test runner can construct and call it directly.
 *   - Constructor-injected dependencies, lazily defaulting to browser globals.
 */
class PageForgeToast {
    /**
     * @param {Object} [options]
     * @param {Document} [options.document] - injected in tests; defaults to the
     *        browser `document` global at call time.
     * @param {number} [options.duration] - visible duration in ms. Defaults to
     *        3000, matching V1's `App.showToast`.
     */
    constructor(options) {
        options = options || {};
        this._document = options.document || null;
        this._duration = (typeof options.duration === 'number') ? options.duration : 3000;
        this._toastTimer = null;
    }

    /**
     * Show a transient toast message.
     *
     * Render logic lifted verbatim from V1's `App.showToast`: set the `#toast`
     * element's text, add the `visible` class, then remove it after `duration`
     * (clearing any in-flight timer first so rapid calls don't truncate early).
     * No-ops when there is no document or no `#toast` element (headless / absent),
     * preserving the carried-over "DOM access no-ops when an element is absent"
     * contract.
     *
     * @param {string} message
     */
    show(message) {
        var doc = this._getDocument();
        if (!doc || typeof doc.getElementById !== 'function') { return; }

        var toast = doc.getElementById('toast');
        if (!toast) { return; }

        toast.textContent = message;
        toast.classList.add('visible');

        var self = this;
        clearTimeout(this._toastTimer);
        this._toastTimer = setTimeout(function () {
            toast.classList.remove('visible');
        }, this._duration);
    }

    // ------------------------------------------------------------------
    // Lazy dependency accessor — injected instance wins, else browser global.
    // ------------------------------------------------------------------

    _getDocument() {
        if (!this._document && typeof document !== 'undefined') {
            this._document = document;
        }
        return this._document;
    }
}

// Self-bootstrap a shared singleton onto the browser global, mirroring how V1's
// single `App` instance owned the toast. Guarded so the DOM-less Node test
// runner can load this file without side effects.
if (typeof window !== 'undefined') {
    window.pageForgeToast = window.pageForgeToast || new PageForgeToast();
}
