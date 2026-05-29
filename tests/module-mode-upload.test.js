/**
 * Tests for Module Development mode upload state (Session 1).
 *
 * Two independent, optional .docx slots — Writer's Template and Media List.
 * Activate is disabled only when BOTH slots are empty, and enabled as soon as
 * at least one file is staged (template only, media list only, or both). These
 * tests verify the enable/disable rule, the button's disabled property staying
 * in sync, and the recorded upload state for each combination.
 */

'use strict';

// A minimal document exposing only the Activate button, so the disabled
// property can be asserted end-to-end without a full DOM.
function mmActivateButton() {
    return {
        id: 'btn-module-activate',
        disabled: false,
        addEventListener: function () {}
    };
}

function mmDocWith(activateBtn) {
    return {
        getElementById: function (id) {
            return id === 'btn-module-activate' ? activateBtn : null;
        }
    };
}

var MM_TEMPLATE = { name: 'WriterTemplate.docx' };
var MM_MEDIA = { name: 'MediaList.docx' };

describe('ModeToggle — Module Development upload state', function () {

    it('disables Activate when no files are staged', function () {
        var btn = mmActivateButton();
        var toggle = new ModeToggle({ document: mmDocWith(btn) });
        assertFalse(toggle.isActivateEnabled(), 'activate disabled with no files');
        assertTrue(btn.disabled, 'activate button reflects disabled state on load');
        assertDeepEqual(toggle.getUploadState(), { template: false, mediaList: false });
    });

    it('enables Activate with the Writer\'s Template only', function () {
        var btn = mmActivateButton();
        var toggle = new ModeToggle({ document: mmDocWith(btn) });
        toggle.setUpload('template', MM_TEMPLATE);
        assertTrue(toggle.isActivateEnabled(), 'activate enabled with template only');
        assertFalse(btn.disabled, 'activate button enabled with template only');
    });

    it('enables Activate with the Media List only', function () {
        var btn = mmActivateButton();
        var toggle = new ModeToggle({ document: mmDocWith(btn) });
        toggle.setUpload('mediaList', MM_MEDIA);
        assertTrue(toggle.isActivateEnabled(), 'activate enabled with media list only');
        assertFalse(btn.disabled, 'activate button enabled with media list only');
    });

    it('enables Activate with both files', function () {
        var btn = mmActivateButton();
        var toggle = new ModeToggle({ document: mmDocWith(btn) });
        toggle.setUpload('template', MM_TEMPLATE);
        toggle.setUpload('mediaList', MM_MEDIA);
        assertTrue(toggle.isActivateEnabled(), 'activate enabled with both files');
        assertFalse(btn.disabled, 'activate button enabled with both files');
    });

    it('records template-only state correctly', function () {
        var toggle = new ModeToggle();
        toggle.setUpload('template', MM_TEMPLATE);
        assertDeepEqual(toggle.getUploadState(), { template: true, mediaList: false });
        assertTrue(toggle.hasUpload('template'), 'template slot recorded');
        assertFalse(toggle.hasUpload('mediaList'), 'media list slot empty');
    });

    it('records media-list-only state correctly', function () {
        var toggle = new ModeToggle();
        toggle.setUpload('mediaList', MM_MEDIA);
        assertDeepEqual(toggle.getUploadState(), { template: false, mediaList: true });
        assertFalse(toggle.hasUpload('template'), 'template slot empty');
        assertTrue(toggle.hasUpload('mediaList'), 'media list slot recorded');
    });

    it('records both-files state correctly', function () {
        var toggle = new ModeToggle();
        toggle.setUpload('template', MM_TEMPLATE);
        toggle.setUpload('mediaList', MM_MEDIA);
        assertDeepEqual(toggle.getUploadState(), { template: true, mediaList: true });
        assertTrue(toggle.hasUpload('template'), 'template slot recorded');
        assertTrue(toggle.hasUpload('mediaList'), 'media list slot recorded');
    });
});
