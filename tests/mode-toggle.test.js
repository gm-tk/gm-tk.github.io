/**
 * Tests for the top-level Module Development mode shell + toggle (Session 1).
 *
 * The production test runner has no DOM, so these tests drive ModeToggle with a
 * minimal injected mock document. They cover the default mode, toggling between
 * modes, the visibility relationship between the two front pages, and the
 * control contract (Module Development exposes two upload slots and no
 * phase/template selector; Standard keeps its template selector).
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
        'upload-section': mtMockEl({ id: 'upload-section', className: 'hidden' }),
        'mode-option-module': mtMockEl({ id: 'mode-option-module', tagName: 'input', type: 'radio', value: 'module', checked: true }),
        'mode-option-standard': mtMockEl({ id: 'mode-option-standard', tagName: 'input', type: 'radio', value: 'standard' }),
        'module-template-input': mtMockEl({ id: 'module-template-input', tagName: 'input', type: 'file', accept: '.docx' }),
        'module-template-drop': mtMockEl({ id: 'module-template-drop' }),
        'module-template-info': mtMockEl({ id: 'module-template-info', className: 'hidden' }),
        'module-template-name': mtMockEl({ id: 'module-template-name' }),
        'module-media-input': mtMockEl({ id: 'module-media-input', tagName: 'input', type: 'file', accept: '.docx' }),
        'module-media-drop': mtMockEl({ id: 'module-media-drop' }),
        'module-media-info': mtMockEl({ id: 'module-media-info', className: 'hidden' }),
        'module-media-name': mtMockEl({ id: 'module-media-name' }),
        'btn-module-activate': mtMockEl({ id: 'btn-module-activate', tagName: 'button', disabled: true }),
        // Standard-mode controls (owned by app.js; present so we can assert them).
        'file-input': mtMockEl({ id: 'file-input', tagName: 'input', type: 'file', accept: '.docx' }),
        'template-dropdown': mtMockEl({ id: 'template-dropdown', tagName: 'select' }),
        'btn-convert': mtMockEl({ id: 'btn-convert', tagName: 'button', disabled: true })
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
        assertFalse(toggle.isStandardMode(), 'isStandardMode false by default');
    });

    it('toggle switches to Standard mode', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        ctx.els['mode-option-standard']._fire('change', { target: ctx.els['mode-option-standard'] });
        assertEqual(toggle.getMode(), 'standard', 'mode should be standard after toggling');
        assertTrue(toggle.isStandardMode());
    });

    it('toggle switches back to Module Development mode', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        ctx.els['mode-option-standard']._fire('change', { target: ctx.els['mode-option-standard'] });
        assertEqual(toggle.getMode(), 'standard', 'sanity: switched to standard');
        ctx.els['mode-option-module']._fire('change', { target: ctx.els['mode-option-module'] });
        assertEqual(toggle.getMode(), 'module', 'mode should return to module');
        assertTrue(toggle.isModuleDevMode());
    });

    it('hides the Standard front page while in Module Development mode', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        assertTrue(ctx.els['upload-section'].classList.contains('hidden'),
            'standard #upload-section should be hidden in module mode');
        assertFalse(ctx.els['module-dev-section'].classList.contains('hidden'),
            'module-dev section should be visible in module mode');
    });

    it('hides the Module Development front page while in Standard mode', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        toggle.setMode('standard');
        assertTrue(ctx.els['module-dev-section'].classList.contains('hidden'),
            'module-dev section should be hidden in standard mode');
        assertFalse(ctx.els['upload-section'].classList.contains('hidden'),
            'standard #upload-section should be visible in standard mode');
    });

    it('exposes exactly two upload slots on the Module Development page', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        assertNotNull(toggle.els.templateInput, 'writer template input resolved');
        assertNotNull(toggle.els.mediaInput, 'media list input resolved');
        assertEqual(toggle.els.templateInput.type, 'file', 'template slot is a file input');
        assertEqual(toggle.els.mediaInput.type, 'file', 'media list slot is a file input');
        var uploads = toggle.getControlManifest('module').filter(function (c) { return c.kind === 'upload'; });
        assertEqual(uploads.length, 2, 'module mode declares exactly two upload slots');
        assertDeepEqual(ModeToggle.UPLOAD_SLOTS, ['template', 'mediaList'], 'upload slots are template + mediaList');
    });

    it('exposes no phase/template selector controls on the Module Development page', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        var selectors = toggle.getControlManifest('module').filter(function (c) { return c.kind === 'selector'; });
        assertEqual(selectors.length, 0, 'module mode declares no selector (phase/template) controls');
        var ids = toggle.getControlManifest('module').map(function (c) { return c.id; });
        assertFalse(ids.indexOf('template-dropdown') !== -1, 'template-dropdown is not a module control');
    });

    it('keeps the Standard page rendering its phase/template controls when active', function () {
        var ctx = mtBuildDoc();
        var toggle = new ModeToggle({ document: ctx.doc });
        toggle.setMode('standard');
        assertFalse(ctx.els['upload-section'].classList.contains('hidden'), 'standard front page visible');
        var selectors = toggle.getControlManifest('standard').filter(function (c) { return c.kind === 'selector'; });
        assertTrue(selectors.length >= 1, 'standard mode keeps a template selector control');
        var dropdown = ctx.doc.getElementById('template-dropdown');
        assertNotNull(dropdown, 'template-dropdown element present in standard front page');
        assertEqual(dropdown.tagName, 'SELECT', 'template selector is a <select>');
    });
});
