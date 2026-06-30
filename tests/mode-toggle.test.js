/**
 * Tests for the top-level mode shell + toggle. The two V1.5 modes are
 * **Module Development** (default) and **Page Stitcher** (re-labeled/re-wired
 * from V1's dropped Standard mode, per spec §9). The runner has no DOM, so these
 * drive ModeToggle with a minimal injected mock document: default mode, toggling,
 * the visibility relationship between the two front pages, and the control
 * contract (Module Development = two upload slots + no selector; Page Stitcher =
 * base + sections uploads + a Stitch button).
 */

'use strict';

// ---- Minimal DOM mock -------------------------------------------------------

function mtMockEl(opts) {
    opts = opts || {};
    var classes = (opts.className || '').split(/\s+/).filter(Boolean);
    var listeners = {};
    var el = {
        id: opts.id || '',
        tagName: (opts.tagName || 'div').toUpperCase(),
        type: opts.type || null,
        value: opts.value || '',
        checked: !!opts.checked,
        disabled: !!opts.disabled,
        accept: opts.accept || null,
        textContent: '',
        files: [],
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

function mtBuildDoc() {
    var els = {
        'module-dev-section': mtMockEl({ id: 'module-dev-section' }),
        'stitch-section': mtMockEl({ id: 'stitch-section', className: 'hidden' }),
        'mode-option-module': mtMockEl({ id: 'mode-option-module', tagName: 'input', type: 'radio', value: 'module', checked: true }),
        'mode-option-stitcher': mtMockEl({ id: 'mode-option-stitcher', tagName: 'input', type: 'radio', value: 'stitcher' }),
        'module-docx-input': mtMockEl({ id: 'module-docx-input', tagName: 'input', type: 'file', accept: '.docx' }),
        'module-docx-drop': mtMockEl({ id: 'module-docx-drop' }),
        'module-docx-info': mtMockEl({ id: 'module-docx-info', className: 'hidden' }),
        'module-docx-name': mtMockEl({ id: 'module-docx-name' }),
        'btn-module-activate': mtMockEl({ id: 'btn-module-activate', tagName: 'button', disabled: true }),
        // Page Stitcher controls (owned by PageStitcherMode; present so we can assert them).
        'stitch-input': mtMockEl({ id: 'stitch-input', tagName: 'input', type: 'file', accept: '.html' }),
        'btn-stitch': mtMockEl({ id: 'btn-stitch', tagName: 'button', disabled: true })
    };
    return {
        els: els,
        doc: { getElementById: function (id) { return els[id] || null; } }
    };
}

// ---- Tests ------------------------------------------------------------------

describe('ModeToggle — mode shell + toggle', function () {

    it('defaults to Module Development mode on load', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        assertEqual(toggle.getMode(), 'module', 'default mode should be module');
        assertTrue(toggle.isModuleDevMode(), 'isModuleDevMode true by default');
        assertFalse(toggle.isStitcherMode(), 'isStitcherMode false by default');
    });

    it('toggle switches to Page Stitcher mode', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        ctx.els['mode-option-stitcher']._fire('change', { target: ctx.els['mode-option-stitcher'] });
        assertEqual(toggle.getMode(), 'stitcher', 'mode should be stitcher after toggling');
        assertTrue(toggle.isStitcherMode());
    });

    it('toggle switches back to Module Development mode', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        ctx.els['mode-option-stitcher']._fire('change', { target: ctx.els['mode-option-stitcher'] });
        assertEqual(toggle.getMode(), 'stitcher', 'sanity: switched to stitcher');
        ctx.els['mode-option-module']._fire('change', { target: ctx.els['mode-option-module'] });
        assertEqual(toggle.getMode(), 'module', 'mode should return to module');
        assertTrue(toggle.isModuleDevMode());
    });

    it('hides the Page Stitcher front page while in Module Development mode', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        assertTrue(ctx.els['stitch-section'].classList.contains('hidden'),
            'page stitcher #stitch-section should be hidden in module mode');
        assertFalse(ctx.els['module-dev-section'].classList.contains('hidden'),
            'module-dev section should be visible in module mode');
    });

    it('hides the Module Development front page while in Page Stitcher mode', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        toggle.setMode('stitcher');
        assertTrue(ctx.els['module-dev-section'].classList.contains('hidden'),
            'module-dev section should be hidden in stitcher mode');
        assertFalse(ctx.els['stitch-section'].classList.contains('hidden'),
            'page stitcher #stitch-section should be visible in stitcher mode');
    });

    it('exposes one Word-documents upload area on the Module Development page', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        assertNotNull(toggle.els.docxInput, 'Word-documents input resolved');
        assertEqual(toggle.els.docxInput.type, 'file', 'docx area is a file input');
        var uploads = toggle.getControlManifest('module').filter(function (c) { return c.kind === 'upload'; });
        assertEqual(uploads.length, 1, 'module mode declares exactly one upload area');
        assertDeepEqual(ModeToggle.UPLOAD_SLOTS, ['docx'], 'the only upload area is docx');
    });

    it('exposes no phase/template selector controls on the Module Development page', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        var selectors = toggle.getControlManifest('module').filter(function (c) { return c.kind === 'selector'; });
        assertEqual(selectors.length, 0, 'module mode declares no selector (phase/template) controls');
        var ids = toggle.getControlManifest('module').map(function (c) { return c.id; });
        assertFalse(ids.indexOf('template-dropdown') !== -1, 'template-dropdown is not a module control');
    });

    it('Page Stitcher mode exposes one upload area and a Stitch button', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        toggle.setMode('stitcher');
        assertFalse(ctx.els['stitch-section'].classList.contains('hidden'), 'page stitcher front page visible');
        var manifest = toggle.getControlManifest('stitcher');
        var uploads = manifest.filter(function (c) { return c.kind === 'upload'; });
        assertEqual(uploads.length, 1, 'stitcher exposes a single (base + sections) upload container');
        var ids = manifest.map(function (c) { return c.id; });
        assertTrue(ids.indexOf('stitch-input') !== -1, 'has the one upload container');
        assertTrue(ids.indexOf('btn-stitch') !== -1, 'has the Stitch button');
        var selectors = manifest.filter(function (c) { return c.kind === 'selector'; });
        assertEqual(selectors.length, 0, 'no phase/template selector in stitcher mode');
    });
});
