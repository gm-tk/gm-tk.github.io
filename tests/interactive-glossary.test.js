/**
 * Glossary interactive — boundary detection + structured renderer tests.
 *
 * Locks in the invariants:
 *   • Boundary detection captures consecutive `Term – Meaning` paragraphs
 *     after `[glossary]`, terminating at the next interactive marker, the
 *     next heading, or the next paragraph that does not match the entry
 *     shape — none escape into trailing `<p>` tags after the placeholder.
 *   • Each entry is split on the FIRST en-dash (U+2013) into term/meaning.
 *     Parenthetical abbreviations in the term (e.g. `Generative AI (Gen AI)`)
 *     are preserved verbatim — the parser does NOT split on parentheses.
 *   • The emitted HTML matches the canonical structure from the issue:
 *     a single outer `<div class="row">`, `<table class="table table-fixed">`,
 *     a single `<tr class="title-g">` header row sitting OUTSIDE `<tbody>`,
 *     and one `<tr>` per entry inside `<tbody>`. No `<thead>`. No leftover
 *     red-dashed placeholder div.
 *
 * Synthetic block-stream fixtures (no .docx).
 */

'use strict';

var _glossNorm = new TagNormaliser();
var _glossTpl = new TemplateEngine();
_glossTpl._data = TemplateEngine._embeddedData();
_glossTpl._loaded = true;
var _glossExtractor = new InteractiveExtractor(_glossNorm);
var _glossConverter = new HtmlConverter(_glossNorm, _glossTpl, _glossExtractor);

function _glossPara(text) {
    return { type: 'paragraph', data: { text: text, runs: [{ text: text }] } };
}

function _glossConvert(blocks) {
    var pageData = {
        type: 'lesson',
        lessonNumber: 1,
        filename: 'GLOS-01.html',
        contentBlocks: blocks
    };
    var config = {
        gridRules: { defaultContent: 'col-md-8 col-12' },
        imageDefaults: { class: 'img-fluid', placeholderBase: 'https://placehold.co' }
    };
    return _glossConverter.convertPage(pageData, config);
}

// Canonical fixture from the issue — 5 entries with en-dash separator.
function _glossCanonicalEntries() {
    return [
        _glossPara('Algorithm – A set of step-by-step instructions used to perform a task or solve a problem.'),
        _glossPara('GPS navigation – A satellite-based system that helps you find a location or directions.'),
        _glossPara('AI technologies – Tools or systems that use artificial intelligence to perform tasks.'),
        _glossPara('Generative AI (Gen AI) – AI that creates new content such as text, images or sound.'),
        _glossPara('Large language model (LLM) – An AI system trained on huge amounts of text to understand and generate human language.')
    ];
}

function _glossDirectRender(blocks, tagIndex) {
    // The block-renderer builds procToRawMap by skipping pageBreaks/empty blocks.
    // For these synthetic fixtures every block is a non-empty paragraph, so the
    // map is the identity 0..N-1 — replicate that here so the renderer can
    // resolve raw indices the same way it does at runtime.
    var procToRawMap = blocks.map(function (_, i) { return i; });
    var glossary = new InteractiveGlossary(_glossNorm, _glossConverter);
    return glossary.render(blocks, tagIndex, blocks, procToRawMap);
}

describe('Glossary interactive — boundary captures all canonical entries', function () {
    it('captures all 5 consecutive entry paragraphs after [glossary]', function () {
        var blocks = [_glossPara('[glossary]')].concat(_glossCanonicalEntries());
        var out = _glossDirectRender(blocks, 0);
        assertNotNull(out, 'renderer should succeed when ≥1 entry follows [glossary]');
        assertEqual(out.consumedRawIndices.length, 5,
            'all 5 entry rawBlock indices must be marked consumed');
        // Indices 1..5 are the entry paragraphs.
        for (var k = 0; k < 5; k++) {
            assertEqual(out.consumedRawIndices[k], k + 1,
                'consumedRawIndices[' + k + '] should be ' + (k + 1));
        }
    });
});

describe('Glossary interactive — rendered HTML is free of orphan entry <p> tags', function () {
    it('integration: convertPage emits the glossary table and no trailing <p>Algorithm…</p>', function () {
        var blocks = [_glossPara('[glossary]')].concat(_glossCanonicalEntries());
        var html = _glossConvert(blocks);

        assertTrue(html.indexOf('<table class="table table-fixed">') !== -1,
            'rendered HTML should contain the glossary table');
        assertTrue(html.indexOf('<p>Algorithm –') === -1,
            'Algorithm entry must NOT escape as a trailing <p>');
        assertTrue(html.indexOf('<p>GPS navigation –') === -1,
            'GPS navigation entry must NOT escape as a trailing <p>');
        assertTrue(html.indexOf('<p>Large language model (LLM) –') === -1,
            'LLM entry must NOT escape as a trailing <p>');
        // Red-dashed placeholder shell from the broken output must be absent.
        assertTrue(html.indexOf('border: 2px dashed #c0392b') === -1,
            'leftover red-dashed placeholder div must not be emitted for glossary');
    });
});

describe('Glossary interactive — boundary terminates at a following heading', function () {
    it('does NOT swallow [H3] Types of AI into the glossary', function () {
        var entries = _glossCanonicalEntries();
        var blocks = [_glossPara('[glossary]')]
            .concat(entries)
            .concat([
                _glossPara('[H3] Types of AI'),
                _glossPara('There are two main categories of AI in everyday use.')
            ]);
        var out = _glossDirectRender(blocks, 0);
        assertNotNull(out);
        assertEqual(out.consumedRawIndices.length, 5,
            'only the 5 entry rows are consumed; [H3] is not consumed');

        var html = _glossConvert(blocks);
        assertTrue(html.indexOf('Types of AI') !== -1,
            'integration: H3 heading text must still render after the glossary');
        assertTrue(html.indexOf('<table class="table table-fixed">') !== -1,
            'integration: glossary table is still emitted');
        // The H3 text must NOT appear inside the glossary table.
        var tableStart = html.indexOf('<table class="table table-fixed">');
        var tableEnd = html.indexOf('</table>', tableStart);
        var tableSlice = html.slice(tableStart, tableEnd);
        assertTrue(tableSlice.indexOf('Types of AI') === -1,
            'H3 heading text must not be swallowed inside the glossary table');
    });
});

describe('Glossary interactive — entry parsing splits on first en-dash', function () {
    it('splits Term – Meaning on the FIRST occurrence of –', function () {
        var glossary = new InteractiveGlossary(_glossNorm, _glossConverter);
        var entry = glossary._parseEntry('Algorithm – A set of step-by-step instructions used to perform a task or solve a problem.');
        assertNotNull(entry);
        assertEqual(entry.term, 'Algorithm');
        assertEqual(entry.meaning,
            'A set of step-by-step instructions used to perform a task or solve a problem.');
    });

    it('returns null when the line lacks an en-dash separator', function () {
        var glossary = new InteractiveGlossary(_glossNorm, _glossConverter);
        assertEqual(glossary._parseEntry('No separator here'), null);
    });
});

describe('Glossary interactive — parenthetical abbreviations preserved verbatim', function () {
    it('keeps "Generative AI (Gen AI)" and "Large language model (LLM)" intact', function () {
        var glossary = new InteractiveGlossary(_glossNorm, _glossConverter);
        var genAi = glossary._parseEntry(
            'Generative AI (Gen AI) – AI that creates new content such as text, images or sound.');
        assertNotNull(genAi);
        assertEqual(genAi.term, 'Generative AI (Gen AI)');

        var llm = glossary._parseEntry(
            'Large language model (LLM) – An AI system trained on huge amounts of text to understand and generate human language.');
        assertNotNull(llm);
        assertEqual(llm.term, 'Large language model (LLM)');

        // Confirm the rendered HTML preserves the parentheses.
        var blocks = [_glossPara('[glossary]')].concat(_glossCanonicalEntries());
        var html = _glossConvert(blocks);
        assertTrue(html.indexOf('Generative AI (Gen AI)') !== -1,
            'rendered HTML preserves "Generative AI (Gen AI)"');
        assertTrue(html.indexOf('Large language model (LLM)') !== -1,
            'rendered HTML preserves "Large language model (LLM)"');
    });
});

describe('Glossary interactive — single outer <div class="row"> wrapper', function () {
    it('emits exactly one outer row wrapper for the interactive', function () {
        var blocks = [_glossPara('[glossary]')].concat(_glossCanonicalEntries());
        var html = _glossConvert(blocks);

        var glossaryStart = html.indexOf('<div class="alert">');
        assertTrue(glossaryStart !== -1, 'alert wrapper must be present');

        // Walk backwards to count the row wrappers between the start of
        // bodyContent and the alert wrapper. The renderer's canonical output
        // is: row → col-md-8 col-12 → alert → row → col-12 → h4 → table.
        // So exactly one outer "row" + one inner "row" sit before the table.
        var beforeAlert = html.slice(0, glossaryStart);
        var rowMatches = beforeAlert.match(/<div class="row">/g);
        assertTrue(rowMatches !== null && rowMatches.length === 1,
            'exactly one outer <div class="row"> precedes the alert wrapper, got: ' +
            (rowMatches ? rowMatches.length : 0));
    });
});

describe('Glossary interactive — table structure: title-g header outside tbody, 5 rows inside', function () {
    it('emits <tr class="title-g"> before <tbody>, no <thead>, and 5 <tr> inside <tbody>', function () {
        var blocks = [_glossPara('[glossary]')].concat(_glossCanonicalEntries());
        var html = _glossConvert(blocks);

        var tableStart = html.indexOf('<table class="table table-fixed">');
        assertTrue(tableStart !== -1, 'glossary table must be emitted');
        var tableEnd = html.indexOf('</table>', tableStart);
        var tableSlice = html.slice(tableStart, tableEnd);

        assertTrue(tableSlice.indexOf('<thead>') === -1,
            'no <thead> element should be emitted');

        var titleRowIdx = tableSlice.indexOf('<tr class="title-g">');
        var tbodyIdx = tableSlice.indexOf('<tbody>');
        assertTrue(titleRowIdx !== -1, '<tr class="title-g"> must be present');
        assertTrue(tbodyIdx !== -1, '<tbody> must be present');
        assertTrue(titleRowIdx < tbodyIdx,
            '<tr class="title-g"> must sit OUTSIDE / before <tbody>');

        var tbodySlice = tableSlice.slice(tbodyIdx, tableSlice.indexOf('</tbody>', tbodyIdx));
        var trMatches = tbodySlice.match(/<tr>/g);
        assertTrue(trMatches !== null && trMatches.length === 5,
            'exactly 5 <tr> rows inside <tbody> for the canonical 5-entry fixture, got: ' +
            (trMatches ? trMatches.length : 0));
    });
});

describe('Glossary interactive — structural equivalence to canonical reference', function () {
    it('matches every required tag, class, and term/meaning text content', function () {
        var blocks = [_glossPara('[glossary]')].concat(_glossCanonicalEntries());
        var html = _glossConvert(blocks);

        // Required structural anchors from the canonical reference.
        var requiredAnchors = [
            '<div class="col-md-8 col-12">',
            '<div class="alert">',
            '<div class="col-12">',
            '<h4>Glossary</h4>',
            '<div class="table-responsive">',
            '<table class="table table-fixed">',
            '<tr class="title-g">',
            '<th>Term</th>',
            '<th>Meaning</th>',
            '<tbody>',
            '</tbody>',
            '</table>'
        ];
        for (var a = 0; a < requiredAnchors.length; a++) {
            assertTrue(html.indexOf(requiredAnchors[a]) !== -1,
                'rendered HTML must contain ' + requiredAnchors[a]);
        }

        // Term/meaning text content for each canonical entry.
        var canonicalPairs = [
            ['Algorithm', 'A set of step-by-step instructions used to perform a task or solve a problem.'],
            ['GPS navigation', 'A satellite-based system that helps you find a location or directions.'],
            ['AI technologies', 'Tools or systems that use artificial intelligence to perform tasks.'],
            ['Generative AI (Gen AI)', 'AI that creates new content such as text, images or sound.'],
            ['Large language model (LLM)', 'An AI system trained on huge amounts of text to understand and generate human language.']
        ];
        for (var p = 0; p < canonicalPairs.length; p++) {
            var rowHtml = '<tr><td>' + canonicalPairs[p][0] + '</td><td>' +
                canonicalPairs[p][1] + '</td></tr>';
            assertTrue(html.indexOf(rowHtml) !== -1,
                'rendered HTML must contain row for "' + canonicalPairs[p][0] + '"');
        }
    });
});

describe('Glossary interactive — multiple [glossary] blocks render independently', function () {
    it('two separate glossary markers each produce their own rendered table', function () {
        var blocks = [
            _glossPara('[glossary]'),
            _glossPara('Algorithm – A set of steps.'),
            _glossPara('GPS navigation – Satellite navigation system.'),
            _glossPara('[H3] Section break'),
            _glossPara('[glossary]'),
            _glossPara('AI technologies – Tools that use AI.'),
            _glossPara('Generative AI (Gen AI) – AI that creates content.')
        ];
        var html = _glossConvert(blocks);

        var firstTable = html.indexOf('<table class="table table-fixed">');
        var secondTable = html.indexOf('<table class="table table-fixed">', firstTable + 1);
        assertTrue(firstTable !== -1, 'first glossary table must be emitted');
        assertTrue(secondTable !== -1, 'second glossary table must be emitted');
        assertTrue(firstTable !== secondTable,
            'the two tables must occupy distinct positions in the output');

        // First table: 2 entries
        var firstTableEnd = html.indexOf('</table>', firstTable);
        var firstSlice = html.slice(firstTable, firstTableEnd);
        var firstTbody = firstSlice.slice(firstSlice.indexOf('<tbody>'),
            firstSlice.indexOf('</tbody>'));
        var firstTrs = firstTbody.match(/<tr>/g);
        assertTrue(firstTrs !== null && firstTrs.length === 2,
            'first glossary should have 2 entries, got: ' + (firstTrs ? firstTrs.length : 0));

        // Second table: 2 entries
        var secondTableEnd = html.indexOf('</table>', secondTable);
        var secondSlice = html.slice(secondTable, secondTableEnd);
        var secondTbody = secondSlice.slice(secondSlice.indexOf('<tbody>'),
            secondSlice.indexOf('</tbody>'));
        var secondTrs = secondTbody.match(/<tr>/g);
        assertTrue(secondTrs !== null && secondTrs.length === 2,
            'second glossary should have 2 entries, got: ' + (secondTrs ? secondTrs.length : 0));
    });
});

describe('Glossary interactive — empty glossary falls through to placeholder', function () {
    it('a [glossary] marker with no following entries does not emit the structured table', function () {
        var blocks = [
            _glossPara('[glossary]'),
            _glossPara('[H3] Next heading'),
            _glossPara('Body content after the heading.')
        ];
        var out = _glossDirectRender(blocks, 0);
        assertNull(out, 'renderer should return null when no entries are captured');

        var html = _glossConvert(blocks);
        assertTrue(html.indexOf('<table class="table table-fixed">') === -1,
            'no glossary table when there are no entries');
        // The generic interactive placeholder should still mark the position.
        assertTrue(html.indexOf('INTERACTIVE') !== -1,
            'fallback path should still emit a placeholder marker');
    });
});
