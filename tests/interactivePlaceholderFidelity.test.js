/**
 * Session G — interactive placeholder fidelity tests.
 *
 * The placeholder shell (dashed border + tier colours + data-table preview
 * format) MUST remain visually identical to Session F. Only the FIDELITY of
 * captured content increases: childBlocks, conversationEntries, writerNotes,
 * and associatedMedia all surface inside the existing placeholder body.
 *
 * Synthetic block-stream fixtures (no .docx).
 */

'use strict';

var fidNormaliser = new TagNormaliser();
var fidExtractor = new InteractiveExtractor(fidNormaliser);

function _fidPara(text, opts) {
    opts = opts || {};
    var run = { text: text };
    if (opts.isRed) run.formatting = { isRed: true };
    return { type: 'paragraph', data: { text: text, runs: [run] } };
}
function _fidTable(headers, rows) {
    var allRows = [];
    if (headers) {
        allRows.push({
            cells: headers.map(function (h) {
                return { paragraphs: [{ text: h, runs: [{ text: h }] }] };
            })
        });
    }
    for (var r = 0; r < rows.length; r++) {
        allRows.push({
            cells: rows[r].map(function (cell) {
                return { paragraphs: [{ text: cell, runs: [{ text: cell }] }] };
            })
        });
    }
    return { type: 'table', data: { rows: allRows } };
}

describe('InteractiveExtractor — placeholder captures childBlocks', function () {
    it('flip_card placeholder lists every captured [front] / [back] child', function () {
        var blocks = [
            _fidPara('[flip card]'),
            _fidTable(['Front', 'Back'], [['A', 'B'], ['C', 'D']]),
            _fidPara('[front] Front One'),
            _fidPara('[back] Back One'),
            _fidPara('[front] Front Two'),
            _fidPara('[back] Back Two'),
            _fidPara('[body]')
        ];
        var out = fidExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Child blocks:') !== -1,
            'placeholder shows Child blocks section');
        assertTrue(html.indexOf('Front One') !== -1, 'Front One present');
        assertTrue(html.indexOf('Back One') !== -1, 'Back One present');
        assertTrue(html.indexOf('Front Two') !== -1, 'Front Two present');
        assertTrue(html.indexOf('Back Two') !== -1, 'Back Two present');
        // Visual shell unchanged: dashed border + Tier 1 green colour
        assertTrue(html.indexOf('border: 2px dashed green') !== -1,
            'tier 1 green dashed border preserved');
        assertTrue(html.indexOf('TIER 1 INTERACTIVE') !== -1,
            'tier label preserved');
    });
});

describe('InteractiveExtractor — placeholder captures conversation entries', function () {
    it('speech_bubble Conversation layout shows entries in order with labels', function () {
        var blocks = [
            _fidPara('[speech bubble Conversation layout]'),
            _fidPara('Prompt 1: First question'),
            _fidPara('AI response: First answer'),
            _fidPara('Prompt 2: Second question'),
            _fidPara('AI response: Second answer'),
            _fidPara('[body]')
        ];
        var out = fidExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Conversation entries:') !== -1,
            'Conversation entries section header present');
        assertTrue(html.indexOf('Prompt 1:') !== -1);
        assertTrue(html.indexOf('First answer') !== -1);
        assertTrue(html.indexOf('Prompt 2:') !== -1);
        assertTrue(html.indexOf('Second answer') !== -1);
        // Order check: Prompt 1 must appear before Prompt 2
        assertTrue(html.indexOf('Prompt 1') < html.indexOf('Prompt 2'),
            'conversation order preserved');
    });
});

describe('InteractiveExtractor — placeholder captures boundary writer notes', function () {
    it('hint_slider with red-text CS note surfaces a Writer note line', function () {
        var blocks = [
            _fidPara('[hint slider]'),
            _fidTable(['Hint', 'Slide'], [['hint a', 'slide a']]),
            _fidPara('CS: keep slide labels short', { isRed: true }),
            _fidPara('[body]')
        ];
        var out = fidExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Writer note:') !== -1,
            'Writer note line present');
        assertTrue(html.indexOf('keep slide labels short') !== -1,
            'CS note text included');
    });
});

describe('InteractiveExtractor — placeholder captures associated media', function () {
    it('speech bubble (conversation) with inline [image] URL lists it under Associated media', function () {
        var blocks = [
            _fidPara('[speech bubble Conversation layout]'),
            _fidPara('Prompt 1: hello'),
            _fidPara('[image] https://example.com/img.png'),
            _fidPara('AI response: hi'),
            _fidPara('[body]')
        ];
        var out = fidExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Associated media:') !== -1,
            'Associated media section present');
        assertTrue(html.indexOf('https://example.com/img.png') !== -1,
            'image URL surfaced inside placeholder');
    });
});

describe('InteractiveExtractor — visual shell is unchanged', function () {
    it('Tier 2 placeholder still uses red dashed border + warning icon', function () {
        var blocks = [
            _fidPara('[drag and drop]'),
            _fidTable(['A', 'B'], [['1', '2']])
        ];
        var out = fidExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('border: 2px dashed red') !== -1,
            'tier 2 red dashed border preserved');
        assertTrue(html.indexOf('INTERACTIVE PLACEHOLDER') !== -1,
            'tier 2 label preserved');
        assertTrue(html.indexOf('\u26A0\uFE0F') !== -1,
            'warning icon preserved');
        // Data-table preview format unchanged
        assertTrue(html.indexOf('<table style="width:100%;') !== -1,
            'data-table preview format unchanged');
    });
});
