/**
 * Tests for Module Development mode upload state.
 *
 * One upload area: the Word-documents container (1–2 .docx — a Writer's Template
 * and/or a Media List, auto-classified at Convert). Activate is disabled only
 * when it is empty and enabled as soon as it holds a file. These verify the
 * enable/disable rule, the button's disabled property staying in sync, and the
 * recorded upload state.
 */

'use strict';

// A minimal document exposing only the Activate button, so the disabled property
// can be asserted end-to-end without a full DOM.
function mmActivateButton() {
    return { id: 'btn-module-activate', disabled: false, addEventListener: function () {} };
}
function mmDocWith(activateBtn) {
    return {
        getElementById: function (id) {
            return id === 'btn-module-activate' ? activateBtn : null;
        }
    };
}

var MM_WT = { name: 'WriterTemplate.docx' };
var MM_MEDIA = { name: 'MediaList.docx' };

describe('ModeToggle — Module Development upload state', function () {

    it('disables Activate when nothing is staged', function () {
        var btn = mmActivateButton();
        var toggle = new ModeToggle({ document: mmDocWith(btn) });
        assertFalse(toggle.isActivateEnabled(), 'activate disabled with no files');
        assertTrue(btn.disabled, 'activate button reflects disabled state on load');
        assertDeepEqual(toggle.getUploadState(), { docx: false });
    });

    it('enables Activate with one Word document', function () {
        var btn = mmActivateButton();
        var toggle = new ModeToggle({ document: mmDocWith(btn) });
        toggle.setDocxFiles([MM_WT]);
        assertTrue(toggle.isActivateEnabled(), 'activate enabled with a .docx');
        assertFalse(btn.disabled, 'activate button enabled with a .docx');
    });

    it('enables Activate with two Word documents', function () {
        var btn = mmActivateButton();
        var toggle = new ModeToggle({ document: mmDocWith(btn) });
        toggle.setDocxFiles([MM_WT, MM_MEDIA]);
        assertTrue(toggle.isActivateEnabled(), 'activate enabled with two .docx');
        assertFalse(btn.disabled);
    });

    it('records docx state correctly', function () {
        var toggle = new ModeToggle();
        toggle.setDocxFiles([MM_WT]);
        assertDeepEqual(toggle.getUploadState(), { docx: true });
        assertTrue(toggle.hasDocx(), 'docx recorded');
    });

    it('clears docx state back to empty', function () {
        var toggle = new ModeToggle();
        toggle.setDocxFiles([MM_WT]);
        assertTrue(toggle.hasDocx(), 'staged');
        toggle.setDocxFiles([]);
        assertFalse(toggle.hasDocx(), 'cleared');
        assertDeepEqual(toggle.getUploadState(), { docx: false });
    });

    it('the one Word-documents container accepts up to two .docx', function () {
        var toggle = new ModeToggle();
        assertEqual(toggle.setDocxFiles([MM_WT, MM_MEDIA]), 2, 'both .docx held in the single container');
        assertEqual(toggle.docxFiles.length, 2);
        toggle.setDocxFiles([]); // clear
        assertFalse(toggle.hasDocx(), 'cleared');
    });

    it('resetSession clears staged documents + outputs and disables Activate', function () {
        var btn = mmActivateButton();
        var toggle = new ModeToggle({ document: mmDocWith(btn) });
        toggle.setDocxFiles([MM_WT, MM_MEDIA]);
        toggle.moduleOutputs = [{ source: 'template', filename: 'x', content: 'y' }];
        assertTrue(toggle.isActivateEnabled(), 'sanity: enabled with files staged');
        assertFalse(btn.disabled, 'sanity: Convert enabled with files staged');
        toggle.resetSession();
        assertFalse(toggle.hasDocx(), 'staged documents cleared');
        assertNull(toggle.moduleOutputs, 'produced outputs cleared');
        assertDeepEqual(toggle.getUploadState(), { docx: false }, 'upload state empty after reset');
        assertTrue(btn.disabled, 'Convert disabled again after a full reset');
    });
});
