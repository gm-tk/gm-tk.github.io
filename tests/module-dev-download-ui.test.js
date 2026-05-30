/**
 * Tests for the Module Development results-screen download UI additions:
 *   • a "Download All" control shown only when BOTH .txt outputs are present,
 *     which reuses the single-file download helper once per file; and
 *   • a next-steps instructions panel (ordered list of six steps) rendered
 *     beneath the downloads whenever there is at least one output.
 *
 * These drive ModuleResultsPage with a minimal injected mock document (no real
 * DOM in the Node runner) and an injected spy OutputManager so the download
 * helper invocations are assertable. Helper names are prefixed `mdd` to avoid
 * collisions with the other module-dev test files sharing the vm global scope.
 */

'use strict';

// ---- Minimal DOM mock -------------------------------------------------------

function mddMockEl(opts) {
    opts = opts || {};
    var classes = (opts.className || '').split(/\s+/).filter(Boolean);
    var listeners = {};
    var el = {
        id: opts.id || '',
        tagName: (opts.tagName || 'div').toUpperCase(),
        innerHTML: '',
        textContent: '',
        classList: {
            add: function (c) { if (classes.indexOf(c) === -1) { classes.push(c); } },
            remove: function (c) { var i = classes.indexOf(c); if (i !== -1) { classes.splice(i, 1); } },
            contains: function (c) { return classes.indexOf(c) !== -1; }
        },
        addEventListener: function (ev, fn) { (listeners[ev] = listeners[ev] || []).push(fn); },
        click: function () { el._fire('click', {}); },
        _fire: function (ev, e) {
            var fns = listeners[ev] || [];
            for (var i = 0; i < fns.length; i++) { fns[i](e || {}); }
        }
    };
    return el;
}

function mddBuildDoc() {
    var els = {
        'module-results-section': mddMockEl({ id: 'module-results-section', className: 'hidden' }),
        'module-dev-section': mddMockEl({ id: 'module-dev-section' }),
        'module-results-list': mddMockEl({ id: 'module-results-list' }),
        'module-results-empty': mddMockEl({ id: 'module-results-empty', className: 'hidden' }),
        'module-download-all-bar': mddMockEl({ id: 'module-download-all-bar' }),
        'module-next-steps': mddMockEl({ id: 'module-next-steps', className: 'hidden' }),
        'btn-module-back': mddMockEl({ id: 'btn-module-back', tagName: 'button' }),
        'mode-option-module': mddMockEl({ id: 'mode-option-module', tagName: 'input' }),
        'mode-option-standard': mddMockEl({ id: 'mode-option-standard', tagName: 'input' })
    };
    return {
        els: els,
        doc: { getElementById: function (id) { return els[id] || null; } }
    };
}

// Spy mirroring the real OutputManager download-helper surface so we can assert
// the canonical downloadFile() primitive is invoked once per produced file.
function mddSpyOutputManager() {
    return {
        addFileCalls: [],
        downloadCalls: [],
        _store: {},
        addFile: function (info) { this.addFileCalls.push(info); this._store[info.filename] = info; },
        getFile: function (filename) { return this._store[filename] || null; },
        downloadFile: function (filename) { this.downloadCalls.push(filename); },
        clear: function () { this._store = {}; }
    };
}

function mddTemplateOut() {
    return { source: 'template', filename: 'ENGS301_parsed.txt', content: 'PARSED TEMPLATE BODY' };
}
function mddMediaOut() {
    return { source: 'mediaList', filename: 'ENGS301_media_list.txt', content: 'MEDIA LIST BODY' };
}

function mddCount(haystack, needle) {
    return haystack.split(needle).length - 1;
}

// ---- Tests ------------------------------------------------------------------

describe('ModuleResultsPage — Download All + next-steps download UI', function () {

    it('renders the Download All button when BOTH .txt outputs are present', function () {
        var ctx = mddBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([mddTemplateOut(), mddMediaOut()]);
        assertTrue(page.hasBothOutputs(), 'both outputs present → hasBothOutputs() true');
        var barHTML = ctx.els['module-download-all-bar'].innerHTML;
        assertTrue(barHTML.indexOf('btn-module-download-all') !== -1,
            'Download All button rendered into the bar when both files are ready');
        assertTrue(barHTML.indexOf('Download All') !== -1, 'button carries the "Download All" label');
    });

    it('hides the Download All button when only one output is present', function () {
        var ctxT = mddBuildDoc();
        var pageT = new ModuleResultsPage({ document: ctxT.doc });
        pageT.show([mddTemplateOut()]);
        assertFalse(pageT.hasBothOutputs(), 'template-only → hasBothOutputs() false');
        assertEqual(ctxT.els['module-download-all-bar'].innerHTML, '',
            'no Download All button for a template-only run');

        var ctxM = mddBuildDoc();
        var pageM = new ModuleResultsPage({ document: ctxM.doc });
        pageM.show([mddMediaOut()]);
        assertFalse(pageM.hasBothOutputs(), 'media-only → hasBothOutputs() false');
        assertEqual(ctxM.els['module-download-all-bar'].innerHTML, '',
            'no Download All button for a media-list-only run');
    });

    it('Download All invokes the single-file download helper exactly twice, once per file', function () {
        var om = mddSpyOutputManager();
        var page = new ModuleResultsPage({ outputManager: om });
        page.show([mddTemplateOut(), mddMediaOut()]);
        // The button's click handler delegates to triggerDownloadAll().
        var count = page.triggerDownloadAll();
        assertEqual(count, 2, 'both outputs downloaded');
        assertEqual(om.downloadCalls.length, 2, 'existing downloadFile helper invoked exactly twice');
        assertDeepEqual(om.downloadCalls, ['ENGS301_parsed.txt', 'ENGS301_media_list.txt'],
            'helper invoked once per file, in output order');
    });

    it('renders the next-steps instructions panel with its six ordered steps', function () {
        var ctx = mddBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([mddTemplateOut(), mddMediaOut()]);
        assertEqual(page.getNextSteps().length, 6, 'six canonical next-steps defined');
        var panel = ctx.els['module-next-steps'];
        assertFalse(panel.classList.contains('hidden'), 'next-steps panel revealed when outputs exist');
        assertTrue(panel.innerHTML.indexOf('<ol') !== -1, 'steps rendered as an ordered (numbered) list');
        assertEqual(mddCount(panel.innerHTML, '<li>'), 6, 'exactly six <li> steps rendered');
        assertTrue(panel.innerHTML.indexOf('Next steps') !== -1, 'panel carries the next-steps heading');
    });

    it('next-steps instructions contain the Continue with Google and HTML Convertor strings', function () {
        var ctx = mddBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([mddTemplateOut()]);
        var html = ctx.els['module-next-steps'].innerHTML;
        assertTrue(html.indexOf('Continue with Google') !== -1, 'mentions the Continue with Google sign-in option');
        assertTrue(html.indexOf('HTML Convertor') !== -1, 'mentions opening the HTML Convertor project');
    });

    it('clears and hides the next-steps panel (and Download All) in the empty state', function () {
        var ctx = mddBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([]);
        assertEqual(ctx.els['module-next-steps'].innerHTML, '', 'next-steps panel cleared with no outputs');
        assertTrue(ctx.els['module-next-steps'].classList.contains('hidden'),
            'next-steps panel hidden in the empty state');
        assertEqual(ctx.els['module-download-all-bar'].innerHTML, '',
            'no Download All button in the empty state');
    });
});
