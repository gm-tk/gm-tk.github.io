/**
 * Tests for the Module Development conversion flow.
 *
 * Drives ModeToggle.handleModuleConversion() with injected synchronous mocks: a
 * DocxParser-style mock returning a canned parse result per file, and a spy
 * OutputFormatter delegating to the real formatter. The REAL MediaListConverter
 * is used (it defaults from the global) so the Writer's-Template-vs-Media-List
 * AUTO-CLASSIFICATION is exercised for real: a parse with a `[TITLE BAR]` is the
 * Writer's Template; one with a media-list header table is the Media List.
 */

'use strict';

function mcfPara(text) {
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: {}, hyperlink: null }],
            text: text, heading: null, listLevel: 0, listNumId: null, listFormat: null, isListItem: false
        }
    };
}
function mcfCell(text) {
    return { paragraphs: [{ runs: [{ text: text, formatting: {}, hyperlink: null }], text: text, isListItem: false }] };
}
function mcfRow(cells) { return { cells: cells.map(mcfCell) }; }
function mcfMediaTableBlock() {
    return {
        type: 'table',
        data: {
            rows: [
                mcfRow(['Item No.', 'WTPg No.', 'Item Type', 'Description', 'Source', 'URL']),
                mcfRow(['', 'p3', 'Image', 'A photo', 'iStock', 'https://x/gm1.jpg'])
            ]
        }
    };
}
// A Writer's-Template parse result (computes the [TITLE BAR] start index like the real parser).
function wtResult(content) {
    var idx = 0, found = false;
    for (var i = 0; i < content.length; i++) {
        var t = content[i].data && content[i].data.text;
        if (t && t.toUpperCase().indexOf('[TITLE BAR]') !== -1) { idx = i; found = true; break; }
    }
    return { content: content, contentStartIndex: idx, contentStartFound: found, metadata: {} };
}
function mlResult() {
    return { content: [mcfMediaTableBlock()], contentStartIndex: 0, contentStartFound: false, metadata: {} };
}
function wtFile(name, content) { return { name: name, _result: wtResult(content) }; }
function mlFile(name) { return { name: name, _result: mlResult() }; }

function mcfParser() {
    return { parseCalls: [], parse: function (f) { this.parseCalls.push(f); return f._result; } };
}
function mcfSpyFormatter() {
    var real = new OutputFormatter();
    return { formatAllCalls: [], formatAll: function (r) { this.formatAllCalls.push(r); return real.formatAll(r); } };
}
function mcfToggle(parser) {
    // mediaListConverter defaults to the real (global) one → real classification.
    return new ModeToggle({ parser: parser || mcfParser(), formatter: mcfSpyFormatter() });
}

describe('Module Development conversion flow — auto-classification', function () {

    it('classifies a [TITLE BAR] .docx as the Writer\'s Template', function () {
        var toggle = mcfToggle();
        toggle.setDocxFiles([wtFile('OSAI201.docx', [mcfPara('[TITLE BAR] X'), mcfPara('Body')])]);
        var outputs = toggle.handleModuleConversion();
        assertEqual(outputs.length, 1, 'one output');
        assertEqual(outputs[0].source, 'template', 'classified as Writer\'s Template');
        assert(outputs[0].content.indexOf('Body') !== -1, 'body content present');
        assertEqual(toggle._formatter.formatAllCalls.length, 1, 'formatAll invoked');
    });

    it('classifies a media-table .docx as the Media List', function () {
        var toggle = mcfToggle();
        toggle.setDocxFiles([mlFile('OSAI201 Media List.docx')]);
        var outputs = toggle.handleModuleConversion();
        assertEqual(outputs.length, 1, 'one output');
        assertEqual(outputs[0].source, 'mediaList', 'classified as Media List');
        assert(outputs[0].content.indexOf('Description') !== -1, 'media-list text produced (header row)');
    });

    it('produces template + media-list outputs from two .docx, regardless of upload order', function () {
        var toggle = mcfToggle();
        // Media List uploaded FIRST — classification, not position, decides.
        toggle.setDocxFiles([mlFile('M.docx'), wtFile('T.docx', [mcfPara('[TITLE BAR] X'), mcfPara('Body')])]);
        var outputs = toggle.handleModuleConversion();
        assertEqual(outputs.length, 2, 'two outputs');
        assertDeepEqual(outputs.map(function (o) { return o.source; }), ['template', 'mediaList'],
            'template first, then media list');
    });

    it('the Writer\'s Template path runs the [TITLE BAR] intro-skip + formatAll', function () {
        var parser = mcfParser();
        var toggle = mcfToggle(parser);
        toggle.setDocxFiles([wtFile('T.docx',
            [mcfPara('GENERIC CHECKLIST front matter'), mcfPara('[TITLE BAR] Module'), mcfPara('Body text')])]);
        var outputs = toggle.handleModuleConversion();
        assertEqual(parser.parseCalls.length, 1, 'parsed once');
        assertEqual(toggle._formatter.formatAllCalls.length, 1, 'formatAll invoked once');
        var text = outputs[0].content;
        assert(text.indexOf('GENERIC CHECKLIST') === -1, 'leading checklist discarded by the intro-skip');
        assert(text.indexOf('Body text') !== -1, 'module body retained');
    });

    it('Activate with no files staged is a no-op', function () {
        var parser = mcfParser();
        var toggle = mcfToggle(parser);
        assertDeepEqual(toggle.handleModuleConversion(), [], 'no-op returns []');
        assertEqual(parser.parseCalls.length, 0, 'parser not invoked');
        assertNull(toggle.moduleOutputs, 'state untouched');
    });

    it('outputs carry standardised "<CODE> <label>_parsed.txt" filenames', function () {
        var toggle = mcfToggle();
        toggle.setDocxFiles([
            wtFile("OSAI201 AI Digital Citizenship Writer's Template.docx", [mcfPara('[TITLE BAR] X'), mcfPara('B')]),
            mlFile('OSAI201 AI Digital Citizenship Media List.docx')
        ]);
        var outputs = toggle.handleModuleConversion();
        var by = {};
        for (var i = 0; i < outputs.length; i++) { by[outputs[i].source] = outputs[i]; }
        assertEqual(by.template.filename, 'OSAI201 Writers Template_parsed.txt');
        assertEqual(by.mediaList.filename, 'OSAI201 Media List_parsed.txt');
    });

    it('writes converted outputs to moduleOutputs', function () {
        var toggle = mcfToggle();
        assertNull(toggle.moduleOutputs, 'null before conversion');
        toggle.setDocxFiles([wtFile('T.docx', [mcfPara('[TITLE BAR] X'), mcfPara('B')])]);
        var outputs = toggle.handleModuleConversion();
        assert(toggle.moduleOutputs === outputs, 'moduleOutputs holds the returned array');
    });

    // ---- both inputs always surface (the dual-file fix) ---------------------

    it('a Writer\'s Template AND a Media List uploaded together both appear (neither dropped)', function () {
        var notes = [];
        var toggle = new ModeToggle({
            parser: mcfParser(), formatter: mcfSpyFormatter(),
            notify: function (m) { notes.push(m); }
        });
        toggle.setDocxFiles([
            wtFile('OSAI501 Writers Template.docx', [mcfPara('[TITLE BAR] AI'), mcfPara('Body')]),
            mlFile('OSAI501 Media List.docx')
        ]);
        var outputs = toggle.handleModuleConversion();
        assertEqual(outputs.length, 2, 'both inputs produce an output — neither is dropped');
        assertDeepEqual(outputs.map(function (o) { return o.source; }), ['template', 'mediaList'],
            'Writer\'s Template first, Media List second');
        assertEqual(notes.length, 0, 'no "extra document ignored" toast for a normal WT + ML pair');
    });

    it('never drops an input: two same-kind .docx both surface with disambiguated filenames', function () {
        var notes = [];
        var toggle = new ModeToggle({
            parser: mcfParser(), formatter: mcfSpyFormatter(),
            notify: function (m) { notes.push(m); }
        });
        // Two Writer's Templates sharing a module-code stem → same derived filename.
        toggle.setDocxFiles([
            wtFile('OSAI501 Writers Template.docx', [mcfPara('[TITLE BAR] One'), mcfPara('B1')]),
            wtFile('OSAI501 alternate.docx', [mcfPara('[TITLE BAR] Two'), mcfPara('B2')])
        ]);
        var outputs = toggle.handleModuleConversion();
        assertEqual(outputs.length, 2, 'both same-kind documents are converted (none ignored)');
        assertDeepEqual(outputs.map(function (o) { return o.source; }), ['template', 'template']);
        assert(outputs[0].filename !== outputs[1].filename, 'the colliding filename is disambiguated');
        assert(outputs[1].filename.indexOf('(2)') !== -1, 'the second copy gets a numeric suffix');
        assertEqual(notes.length, 0, 'no document is announced as ignored');
    });

    it('each output is the clean {source, filename, content} shape (no internal carriers leak)', function () {
        var toggle = mcfToggle();
        toggle.setDocxFiles([
            wtFile('OSAI501 Writers Template.docx', [mcfPara('[TITLE BAR] X'), mcfPara('B')]),
            mlFile('OSAI501 Media List.docx')
        ]);
        var outputs = toggle.handleModuleConversion();
        outputs.forEach(function (o) {
            assertDeepEqual(Object.keys(o).sort(), ['content', 'filename', 'source'],
                'output exposes only source/filename/content');
        });
    });

    it('uses a fresh parser per .docx so two uploads never share parse state', function () {
        // Reproduces the real-browser bug: DocxParser.parse is async + stateful,
        // so one shared instance parsing both files concurrently returned the
        // Media List wearing the Writer's Template's content (two "Writer's
        // Template" outputs). A fresh parser per file fixes it.
        var made = [];
        var toggle = new ModeToggle({
            parserFactory: function () {
                var p = { calls: [], parse: function (f) { this.calls.push(f); return f._result; } };
                made.push(p);
                return p;
            },
            formatter: mcfSpyFormatter()
        });
        toggle.setDocxFiles([
            wtFile('OSAI501 Writers Template.docx', [mcfPara('[TITLE BAR] AI'), mcfPara('Body')]),
            mlFile('OSAI501 Media List.docx')
        ]);
        var outputs = toggle.handleModuleConversion();
        assertEqual(made.length, 2, 'a fresh parser instance is made for each uploaded file');
        assertEqual(made[0].calls.length, 1, 'first parser handled exactly one file');
        assertEqual(made[1].calls.length, 1, 'second parser handled exactly one file');
        assertDeepEqual(outputs.map(function (o) { return o.source; }), ['template', 'mediaList'],
            'WT→template and ML→mediaList, classified from independent parses');
    });
});
