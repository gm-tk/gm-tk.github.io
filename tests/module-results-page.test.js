/**
 * Tests for the Module Development mode results / download screen (Session 3).
 *
 * The production test runner has no DOM, so these tests drive ModuleResultsPage
 * either as a pure state machine (no document) or with a minimal injected mock
 * document. They cover: rendering the screen after a conversion; showing exactly
 * the downloads for the file(s) actually produced (template only, media list
 * only, both); the download control delegating to the existing OutputManager
 * helper with the correct filename + content; the absence of any phase/template
 * or HTML-preview controls; the return-to-front-page navigation; and the
 * empty-state guard.
 */

'use strict';

// ---- Minimal DOM mock -------------------------------------------------------

function mrpMockEl(opts) {
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

function mrpBuildDoc() {
    var els = {
        'module-results-section': mrpMockEl({ id: 'module-results-section', className: 'hidden' }),
        'module-dev-section': mrpMockEl({ id: 'module-dev-section' }),
        'module-results-list': mrpMockEl({ id: 'module-results-list' }),
        'module-results-empty': mrpMockEl({ id: 'module-results-empty', className: 'hidden' }),
        'btn-module-back': mrpMockEl({ id: 'btn-module-back', tagName: 'button' }),
        'mode-option-module': mrpMockEl({ id: 'mode-option-module', tagName: 'input' }),
        'mode-option-standard': mrpMockEl({ id: 'mode-option-standard', tagName: 'input' })
    };
    return {
        els: els,
        doc: { getElementById: function (id) { return els[id] || null; } }
    };
}

// Spy OutputManager mirroring the real download-helper surface (addFile / getFile
// / downloadFile / clear) so tests can assert the helper is invoked with the
// correct filename and content.
function mrpSpyOutputManager() {
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

// Output descriptor fixtures matching ModeToggle.moduleOutputs entries.
function mrpTemplateOut() {
    return { source: 'template', filename: 'ENGS301_parsed.txt', content: 'PARSED TEMPLATE BODY' };
}
function mrpMediaOut() {
    return { source: 'mediaList', filename: 'ENGS301_media_list.txt', content: 'MEDIA LIST BODY' };
}

// ---- Tests ------------------------------------------------------------------

describe('ModuleResultsPage — Module Development results / download screen', function () {

    it('renders the results screen after a conversion completes', function () {
        var ctx = mrpBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        assertFalse(page.isResultsVisible(), 'results screen hidden before show()');
        page.show([mrpTemplateOut(), mrpMediaOut()]);
        assertTrue(page.isResultsVisible(), 'results screen visible after show()');
        assertFalse(ctx.els['module-results-section'].classList.contains('hidden'),
            'results section revealed');
        assertTrue(ctx.els['module-dev-section'].classList.contains('hidden'),
            'Module Development front page hidden while results are shown');
        assertEqual(page.getDownloadItems().length, 2, 'two download controls rendered');
        assertTrue(ctx.els['module-results-list'].innerHTML.indexOf('module-download') !== -1,
            'download buttons rendered into the list container');
    });

    it('shows the writer\'s template download when only the template was converted', function () {
        var page = new ModuleResultsPage();
        page.show([mrpTemplateOut()]);
        var items = page.getDownloadItems();
        assertEqual(items.length, 1, 'exactly one download for template-only');
        assertEqual(items[0].source, 'template', 'the download is the template output');
        assertEqual(items[0].label, "Writer's Template", 'labelled as the Writer\'s Template');
        assertEqual(items[0].filename, 'ENGS301_parsed.txt', 'carries the template output filename');
    });

    it('shows the media list download when only the media list was converted', function () {
        var page = new ModuleResultsPage();
        page.show([mrpMediaOut()]);
        var items = page.getDownloadItems();
        assertEqual(items.length, 1, 'exactly one download for media-list-only');
        assertEqual(items[0].source, 'mediaList', 'the download is the media list output');
        assertEqual(items[0].label, 'Media List', 'labelled as the Media List');
        assertEqual(items[0].filename, 'ENGS301_media_list.txt', 'carries the media list output filename');
    });

    it('shows both downloads when both files were converted', function () {
        var page = new ModuleResultsPage();
        page.show([mrpTemplateOut(), mrpMediaOut()]);
        var items = page.getDownloadItems();
        assertEqual(items.length, 2, 'two downloads when both were produced');
        var sources = items.map(function (i) { return i.source; });
        assertDeepEqual(sources, ['template', 'mediaList'], 'template first, media list second');
    });

    it('download control invokes the existing download helper with the correct filename and content', function () {
        var om = mrpSpyOutputManager();
        var page = new ModuleResultsPage({ outputManager: om });
        page.show([mrpTemplateOut()]);
        var ok = page.triggerDownload('ENGS301_parsed.txt');
        assertTrue(ok, 'triggerDownload found and downloaded the output');
        assertEqual(om.addFileCalls.length, 1, 'the helper registered exactly one file');
        assertEqual(om.addFileCalls[0].filename, 'ENGS301_parsed.txt', 'helper got the correct filename');
        assertEqual(om.addFileCalls[0].content, 'PARSED TEMPLATE BODY', 'helper got the correct content');
        assertEqual(om.downloadCalls.length, 1, 'existing downloadFile helper invoked once');
        assertEqual(om.downloadCalls[0], 'ENGS301_parsed.txt', 'downloadFile invoked with the correct filename');
    });

    it('shows no HTML preview and no phase/template controls on the screen', function () {
        var page = new ModuleResultsPage();
        page.show([mrpTemplateOut(), mrpMediaOut()]);
        var manifest = page.getControlManifest();
        var selectors = manifest.filter(function (c) { return c.kind === 'selector'; });
        var previews = manifest.filter(function (c) { return c.kind === 'preview'; });
        assertEqual(selectors.length, 0, 'no phase/template selector controls on the results screen');
        assertEqual(previews.length, 0, 'no HTML preview control on the results screen');
        var kinds = manifest.map(function (c) { return c.kind; }).filter(function (k, i, a) { return a.indexOf(k) === i; }).sort();
        assertDeepEqual(kinds, ['back', 'download'], 'screen owns only download + back controls');
    });

    it('return-to-front-page control navigates back to the Module Development front page', function () {
        var ctx = mrpBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([mrpTemplateOut()]);
        assertTrue(page.isResultsVisible(), 'sanity: results visible after show()');
        // Fire the back control exactly as a user click would.
        ctx.els['btn-module-back']._fire('click', {});
        assertFalse(page.isResultsVisible(), 'results screen hidden after returning');
        assertTrue(ctx.els['module-results-section'].classList.contains('hidden'),
            'results section hidden after returning');
        assertFalse(ctx.els['module-dev-section'].classList.contains('hidden'),
            'Module Development front page revealed after returning');
    });

    it('guards the empty state when no outputs are present', function () {
        var ctx = mrpBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([]);
        assertFalse(page.hasOutputs(), 'no outputs after an empty show()');
        assertDeepEqual(page.getDownloadItems(), [], 'no download items in the empty state');
        var downloads = page.getControlManifest().filter(function (c) { return c.kind === 'download'; });
        assertEqual(downloads.length, 0, 'no download controls in the empty state');
        assertFalse(ctx.els['module-results-empty'].classList.contains('hidden'),
            'empty-state message revealed when there is nothing to download');
        assertEqual(ctx.els['module-results-list'].innerHTML, '', 'download list cleared in the empty state');
        assertTrue(page.isResultsVisible(), 'the (empty) results screen is still the active surface');
    });

    it('hides the results screen when the top-level mode is switched', function () {
        var ctx = mrpBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([mrpTemplateOut()]);
        assertTrue(page.isResultsVisible(), 'sanity: results visible after show()');
        // Switching mode must not leave the results screen stacked over a front page.
        ctx.els['mode-option-standard']._fire('change', { target: ctx.els['mode-option-standard'] });
        assertFalse(page.isResultsVisible(), 'results screen no longer the active surface after a mode switch');
        assertTrue(ctx.els['module-results-section'].classList.contains('hidden'),
            'results section hidden after a mode switch (ModeToggle owns which front page shows)');
    });
});
