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
});
