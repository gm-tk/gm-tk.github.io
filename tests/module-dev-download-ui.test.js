/**
 * Tests for the Module Development results-screen next-steps instructions panel
 * (an ordered list of five steps) rendered beneath the per-file downloads
 * whenever there is at least one converted output.
 *
 * These drive ModuleResultsPage with a minimal injected mock document (no real
 * DOM in the Node runner). Helper names are prefixed `mdd` to avoid collisions
 * with the other module-dev test files sharing the vm global scope.
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
        'module-next-steps': mddMockEl({ id: 'module-next-steps', className: 'hidden' }),
        'btn-module-back': mddMockEl({ id: 'btn-module-back', tagName: 'button' }),
        'mode-option-module': mddMockEl({ id: 'mode-option-module', tagName: 'input' }),
        'mode-option-stitcher': mddMockEl({ id: 'mode-option-stitcher', tagName: 'input' })
    };
    return {
        els: els,
        doc: { getElementById: function (id) { return els[id] || null; } }
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

describe('ModuleResultsPage — next-steps download UI', function () {

    it('renders the next-steps instructions panel with its five ordered steps', function () {
        var ctx = mddBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([mddTemplateOut(), mddMediaOut()]);
        assertEqual(page.getNextSteps().length, 5, 'five canonical top-level next-steps defined');
        var panel = ctx.els['module-next-steps'];
        assertFalse(panel.classList.contains('hidden'), 'next-steps panel revealed when outputs exist');
        assertTrue(panel.innerHTML.indexOf('<ol class="next-steps-list">') !== -1, 'steps rendered as an ordered (numbered) list');
        assertTrue(panel.innerHTML.indexOf('<ol type="a" class="next-steps-sublist">') !== -1, 'step 4 carries the nested (a/b/c) upload sub-list');
        assertEqual(mddCount(panel.innerHTML, '<li>'), 7, 'five top-level steps plus two nested (a/b) sub-items');
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

    it('clears and hides the next-steps panel in the empty state', function () {
        var ctx = mddBuildDoc();
        var page = new ModuleResultsPage({ document: ctx.doc });
        page.show([]);
        assertEqual(ctx.els['module-next-steps'].innerHTML, '', 'next-steps panel cleared with no outputs');
        assertTrue(ctx.els['module-next-steps'].classList.contains('hidden'),
            'next-steps panel hidden in the empty state');
    });
});
