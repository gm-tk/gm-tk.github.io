/**
 * Tests for the Module Development mode conversion flow (Session 2).
 *
 * Drives ModeToggle.handleModuleConversion() — the Activate handler — with
 * injected synchronous mocks so the orchestration is exercised headlessly:
 *
 *   • a synchronous DocxParser-style mock whose parse() mirrors the real
 *     contract by running the [TITLE BAR] intro-skipper (_findContentStart),
 *     making the template path's reuse of the existing skip observable;
 *   • a spy OutputFormatter that delegates to the real (loaded) formatter while
 *     recording formatAll() calls — formatAll() is the existing pipeline entry
 *     that emits from contentStartIndex;
 *   • a MediaListConverter stub returning text synchronously.
 *
 * Because every injected dependency is synchronous, handleModuleConversion()
 * returns the output array directly (in the browser it returns a Promise).
 */

'use strict';

function mcfPara(text) {
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: {}, hyperlink: null }],
            text: text,
            heading: null,
            listLevel: 0,
            listNumId: null,
            listFormat: null,
            isListItem: false
        }
    };
}

// Synchronous DocxParser-style mock. parse() runs _findContentStart() (the
// [TITLE BAR] intro-skipper) exactly like the real DocxParser, so the template
// path genuinely invokes the existing skip and reports the start index.
function mcfTemplateParser(content) {
    return {
        parseCalls: [],
        findStartCalls: 0,
        _findContentStart: function () {
            this.findStartCalls++;
            for (var i = 0; i < content.length; i++) {
                var t = content[i] && content[i].data && content[i].data.text;
                if (t && t.toUpperCase().indexOf('[TITLE BAR]') !== -1) {
                    return { index: i, found: true };
                }
            }
            return { index: 0, found: false };
        },
        parse: function (file) {
            this.parseCalls.push(file);
            var cs = this._findContentStart();
            return {
                content: content,
                contentStartIndex: cs.index,
                contentStartFound: cs.found,
                metadata: {}
            };
        }
    };
}

// Spy formatter delegating to the real OutputFormatter (loaded by the runner),
// recording formatAll() invocations.
function mcfSpyFormatter() {
    var real = new OutputFormatter();
    return {
        formatAllCalls: [],
        formatAll: function (r) { this.formatAllCalls.push(r); return real.formatAll(r); },
        formatMetadata: function (m) { return real.formatMetadata(m); },
        formatContent: function (c, s, f) { return real.formatContent(c, s, f); },
        _stripEmptyRedText: function (t) { return real._stripEmptyRedText(t); }
    };
}

// Synchronous MediaListConverter stub.
function mcfMediaConverter() {
    return {
        convertCalls: [],
        convert: function (file) {
            this.convertCalls.push(file);
            return 'MEDIA-LIST TEXT for ' + (file && file.name);
        }
    };
}

function mcfToggle(parser) {
    return new ModeToggle({
        parser: parser || mcfTemplateParser([mcfPara('[TITLE BAR] X'), mcfPara('Body')]),
        formatter: mcfSpyFormatter(),
        mediaListConverter: mcfMediaConverter()
    });
}

describe('Module Development conversion flow — handleModuleConversion', function () {

    it('template-only upload produces exactly one output', function () {
        var toggle = mcfToggle();
        toggle.setUpload('template', { name: 'Tmpl.docx' });
        var outputs = toggle.handleModuleConversion();
        assertEqual(outputs.length, 1, 'exactly one output for template-only');
        assertEqual(outputs[0].source, 'template', 'the output is the template conversion');
        assertEqual(toggle._mediaListConverter.convertCalls.length, 0, 'media converter not invoked');
    });

    it('media-list-only upload produces exactly one output', function () {
        var parser = mcfTemplateParser([mcfPara('x')]);
        var toggle = mcfToggle(parser);
        toggle.setUpload('mediaList', { name: 'Media.docx' });
        var outputs = toggle.handleModuleConversion();
        assertEqual(outputs.length, 1, 'exactly one output for media-list-only');
        assertEqual(outputs[0].source, 'mediaList', 'the output is the media-list conversion');
        assertEqual(parser.parseCalls.length, 0, 'writer template parser not invoked');
        assertEqual(toggle._mediaListConverter.convertCalls.length, 1, 'media converter invoked once');
    });

    it('both files uploaded produce exactly two outputs', function () {
        var toggle = mcfToggle();
        toggle.setUpload('template', { name: 'T.docx' });
        toggle.setUpload('mediaList', { name: 'M.docx' });
        var outputs = toggle.handleModuleConversion();
        assertEqual(outputs.length, 2, 'exactly two outputs when both are staged');
        var sources = outputs.map(function (o) { return o.source; });
        assertDeepEqual(sources, ['template', 'mediaList'], 'template first, media list second');
    });

    it('the writer\'s template path invokes the existing intro-skipping function', function () {
        var content = [
            mcfPara('GENERIC CHECKLIST front matter'),
            mcfPara('[TITLE BAR] Module'),
            mcfPara('Body text')
        ];
        var parser = mcfTemplateParser(content);
        var toggle = mcfToggle(parser);
        toggle.setUpload('template', { name: 'T.docx' });
        var outputs = toggle.handleModuleConversion();

        // parse() ran the [TITLE BAR] boundary detection, and formatAll() (the
        // existing pipeline entry) emitted from contentStartIndex.
        assertEqual(parser.parseCalls.length, 1, 'template parsed exactly once');
        assertTrue(parser.findStartCalls >= 1, 'intro-skip function (_findContentStart) was invoked');
        assertEqual(toggle._formatter.formatAllCalls.length, 1, 'existing formatAll pipeline invoked for the template');

        // The intro-skip discarded the leading checklist; module body retained.
        var text = outputs[0].content;
        assert(text.indexOf('GENERIC CHECKLIST') === -1, 'leading checklist discarded by the intro-skip');
        assert(text.indexOf('Body text') !== -1, 'module body content retained');
    });

    it('writes converted outputs to the expected state field (moduleOutputs)', function () {
        var toggle = mcfToggle();
        assertNull(toggle.moduleOutputs, 'moduleOutputs is null before conversion');
        toggle.setUpload('template', { name: 'T.docx' });
        var outputs = toggle.handleModuleConversion();
        assert(toggle.moduleOutputs === outputs, 'moduleOutputs holds the returned output array');
        assertEqual(toggle.moduleOutputs.length, 1, 'state field carries the produced output');
        assertNotNull(toggle.moduleOutputs[0].content, 'stored output carries content');
    });

    it('Activate with no files staged is a no-op', function () {
        var parser = mcfTemplateParser([mcfPara('x')]);
        var toggle = mcfToggle(parser);
        var outputs = toggle.handleModuleConversion();
        assertDeepEqual(outputs, [], 'no-op returns an empty array');
        assertEqual(parser.parseCalls.length, 0, 'parser not invoked with no files');
        assertEqual(toggle._mediaListConverter.convertCalls.length, 0, 'media converter not invoked with no files');
        assertNull(toggle.moduleOutputs, 'state field left untouched (null) on a no-op');
    });

    it('outputs carry standardised "<CODE> <label>_parsed.txt" filenames for the template and media list', function () {
        var toggle = mcfToggle();
        toggle.setUpload('template', { name: 'OSAI201 AI Digital Citizenship Writer\'s Template.docx' });
        toggle.setUpload('mediaList', { name: 'OSAI201 AI Digital Citizenship Media List.docx' });
        var outputs = toggle.handleModuleConversion();
        var bySource = {};
        for (var i = 0; i < outputs.length; i++) { bySource[outputs[i].source] = outputs[i]; }
        assertEqual(bySource.template.filename, "OSAI201 Writer's Template_parsed.txt",
            'template → <CODE> Writer\'s Template_parsed.txt (descriptive middle segment dropped)');
        assertEqual(bySource.mediaList.filename, 'OSAI201 Media List_parsed.txt',
            'media list → <CODE> Media List_parsed.txt (suffix unified to _parsed)');
    });
});
