/**
 * Tests for the standardised Module Development mode download filenames.
 *
 * Module Development conversion names each downloadable .txt as
 *   `<MODULE_CODE> <label>_parsed.txt`
 * where the module code is the leading token of the source .docx filename (any
 * descriptive middle segment is dropped), <label> is "Writer's Template" or
 * "Media List", and BOTH outputs share the unified `_parsed.txt` suffix (the
 * Media List is no longer `_media_list`). The logic lives in
 * ModeToggle._deriveFilename / _deriveModuleCode (js/mode-toggle.js); these are
 * pure, DOM-free string helpers, so they are exercised directly against a
 * headless ModeToggle instance (no document). Helper names are prefixed `mdf`
 * to avoid collisions with the other module-dev test files sharing the vm
 * global scope. This covers ONLY the Module Development filename generation;
 * Standard mode filenames (js/app.js) are untouched.
 */

'use strict';

function mdfToggle() {
    // No document → pure state machine; _deriveFilename touches no DOM.
    return new ModeToggle();
}

describe('Module Development mode — standardised download filenames', function () {

    it('builds the Writer\'s Template filename for a given module code', function () {
        var name = mdfToggle()._deriveFilename(
            { name: 'OSAI201 AI Digital Citizenship.docx' }, "Writer's Template");
        assertEqual(name, "OSAI201 Writer's Template_parsed.txt",
            'template → "<CODE> Writer\'s Template_parsed.txt"');
    });

    it('builds the Media List filename for a given module code', function () {
        var name = mdfToggle()._deriveFilename(
            { name: 'OSAI201 AI Digital Citizenship.docx' }, 'Media List');
        assertEqual(name, 'OSAI201 Media List_parsed.txt',
            'media list → "<CODE> Media List_parsed.txt"');
    });

    it('both filenames conform to the "<MODULE_CODE> ... _parsed.txt" pattern', function () {
        var toggle = mdfToggle();
        var file = { name: 'OSAI201 AI Digital Citizenship.docx' };
        var tmpl = toggle._deriveFilename(file, "Writer's Template");
        var media = toggle._deriveFilename(file, 'Media List');
        var pattern = /^OSAI201 .+_parsed\.txt$/;
        assertTrue(pattern.test(tmpl), 'template matches <CODE> ... _parsed.txt: ' + tmpl);
        assertTrue(pattern.test(media), 'media list matches <CODE> ... _parsed.txt: ' + media);
    });

    it('drops any descriptive middle segment from the source filename', function () {
        // The middle "AI Digital Citizenship" descriptor must not survive into
        // the generated name — only the leading module code is kept.
        var name = mdfToggle()._deriveFilename(
            { name: 'OSAI201 AI Digital Citizenship Writer\'s Template.docx' }, "Writer's Template");
        assertEqual(name, "OSAI201 Writer's Template_parsed.txt",
            'descriptive middle segment dropped, code + label retained');
        assertTrue(name.indexOf('AI Digital Citizenship') === -1,
            'no descriptive middle segment remains in the filename');
    });

    it('uses the unified _parsed suffix for the Media List (never _media_list)', function () {
        var name = mdfToggle()._deriveFilename(
            { name: 'OSAI201 AI Digital Citizenship.docx' }, 'Media List');
        assertTrue(name.indexOf('_media_list') === -1, 'no legacy _media_list suffix: ' + name);
        assertTrue(/_parsed\.txt$/.test(name), 'ends with the unified _parsed.txt suffix: ' + name);
    });

    it('prefixes a differently-formatted module code correctly', function () {
        // A bare-code filename (no descriptor) and a different code format still
        // produce a correctly <CODE>-prefixed name.
        var name = mdfToggle()._deriveFilename({ name: 'ENGS301.docx' }, "Writer's Template");
        assertEqual(name, "ENGS301 Writer's Template_parsed.txt",
            'bare-code filename still yields the correct <CODE> prefix');
    });

    // ------------------------------------------------------------------
    // Position-independent module-code detection (bug fix). The code must be
    // found by SHAPE (letters immediately followed by digits) wherever it sits
    // in the filename, not merely as the leading token.
    // ------------------------------------------------------------------

    it('detects a module code that is the TRAILING token', function () {
        var name = mdfToggle()._deriveFilename(
            { name: 'AI Digital Citizenship OSAI201.docx' }, "Writer's Template");
        assertEqual(name, "OSAI201 Writer's Template_parsed.txt",
            'trailing code token is detected and used as the prefix');
    });

    it('detects a module code in the MIDDLE of the filename', function () {
        var name = mdfToggle()._deriveFilename(
            { name: 'AI Digital OSAI201 Citizenship.docx' }, 'Media List');
        assertEqual(name, 'OSAI201 Media List_parsed.txt',
            'mid-filename code token is detected and used as the prefix');
    });

    it('detects the code with a descriptor on BOTH sides', function () {
        var name = mdfToggle()._deriveFilename(
            { name: "Writer's ENGS301 Template.docx" }, "Writer's Template");
        assertEqual(name, "ENGS301 Writer's Template_parsed.txt",
            'code surrounded by descriptors on both sides is still chosen');
    });

    it('does NOT pick a leading non-code word as the prefix (original bug repro)', function () {
        // Original bug: the leading token "Writer's" (no digits) was wrongly used
        // as the prefix instead of the real code later in the name.
        var name = mdfToggle()._deriveFilename(
            { name: "Writer's Template OSAI201.docx" }, "Writer's Template");
        assertEqual(name, "OSAI201 Writer's Template_parsed.txt",
            'leading non-code word must not be chosen over the real code');
        assertTrue(name.indexOf('OSAI201 ') === 0,
            'prefix is the code, not the leading descriptor: ' + name);
    });

    it('falls back to the leading token when NO token matches the code shape', function () {
        var name = mdfToggle()._deriveFilename(
            { name: 'Untitled Document Draft.docx' }, "Writer's Template");
        assertEqual(name, "Untitled Writer's Template_parsed.txt",
            'no detectable code → leading token preserved (historical behaviour)');
    });

    it('still prefixes a bare-code filename correctly under shape detection', function () {
        var name = mdfToggle()._deriveFilename({ name: 'ENGS301.docx' }, 'Media List');
        assertEqual(name, 'ENGS301 Media List_parsed.txt',
            'bare-code filename still yields the correct <CODE> prefix');
    });

    // ------------------------------------------------------------------
    // Code embedded INSIDE a token (underscores/hyphens), document-metadata
    // preference, and case normalisation.
    // ------------------------------------------------------------------

    it('extracts a code embedded mid-token by underscores and purges the rest', function () {
        var name = mdfToggle()._deriveFilename({ name: 'Copy_CEDO501_WT.docx' }, 'Writers Template');
        assertEqual(name, 'CEDO501 Writers Template_parsed.txt',
            'CEDO501 found inside "Copy_CEDO501_WT"; every other part discarded');
        assertTrue(name.indexOf('Copy') === -1 && name.indexOf('_WT') === -1, 'no junk survives');
    });

    it('upper-cases a lower-case code found mid-token', function () {
        var name = mdfToggle()._deriveFilename({ name: 'copy_cedo501_media_list.docx' }, 'Media List');
        assertEqual(name, 'CEDO501 Media List_parsed.txt', 'lower-case code normalised to upper-case');
    });

    it('prefers the document-extracted module code over the filename', function () {
        var name = mdfToggle()._deriveFilename(
            { name: 'random_draft_v2.docx' }, 'Media List',
            { metadata: { moduleCode: 'CEDO501' } });
        assertEqual(name, 'CEDO501 Media List_parsed.txt',
            'metadata.moduleCode wins when the filename has no clear code');
    });
});
