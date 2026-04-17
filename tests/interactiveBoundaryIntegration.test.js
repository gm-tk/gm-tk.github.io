/**
 * Session G — interactive boundary integration tests.
 *
 * Real .docx fixtures are not present in this repo, so the cases below use
 * inline SYNTHETIC block-stream fixtures replicating the key structural
 * patterns from the writer-template module families:
 *   • OSAI401 lesson 1 — [hint slider] hint/slide pairs
 *   • OSAI401 — [speech bubble] Conversation layout (Prompt/Response)
 *   • OSAI201 — known interactive (flip card) startBlockIndex / endBlockIndex
 *   • Body paragraph between two interactives renders OUTSIDE both
 *   • generateReferenceDocument() surfaces the new sub-sections
 *
 * Synthetic fixture
 */

'use strict';

var intNormaliser = new TagNormaliser();
var intExtractor = new InteractiveExtractor(intNormaliser);

function _intPara(text, opts) {
    opts = opts || {};
    var run = { text: text };
    if (opts.isRed) run.formatting = { isRed: true };
    return { type: 'paragraph', data: { text: text, runs: [run] } };
}
function _intTable(headers, rows) {
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

describe('Integration — OSAI401 (synthetic) [hint slider] captures all hint/slide pairs', function () {
    it('boundary captures table + closes at [body]', function () {
        // Synthetic fixture replicating OSAI401 lesson 1 [hint slider] shape
        var blocks = [
            _intPara('[hint slider]'),
            _intTable(
                ['Hint', 'Slide'],
                [
                    ['Hint one', 'Slide one'],
                    ['Hint two', 'Slide two'],
                    ['Hint three', 'Slide three']
                ]
            ),
            _intPara('[body]'),
            _intPara('Body paragraph after the slider.')
        ];
        var out = intExtractor.processInteractive(blocks, 0, 'OSAI401-01.html', '1', false);
        assertNotNull(out);
        assertEqual(out.startBlockIndex, 0);
        assertEqual(out.endBlockIndex, 1,
            'boundary closes after the data table at [body]');
        assertNotNull(out.dataTable);
        assertEqual(out.dataTable.rows.length, 4,
            'table preserves header row + 3 hint/slide pairs');
    });
});

describe('Integration — OSAI401 (synthetic) speech_bubble Conversation layout', function () {
    it('captures all Prompt/Response entries in order', function () {
        // Synthetic fixture
        var blocks = [
            _intPara('[speech bubble Conversation layout]'),
            _intPara('Prompt 1: What is OSAI?'),
            _intPara('AI response: A learning module.'),
            _intPara('Prompt 2: Tell me more.'),
            _intPara('AI response: It teaches AI concepts.'),
            _intPara('[body]')
        ];
        var out = intExtractor.processInteractive(blocks, 0, 'OSAI401-02.html', '2', false);
        assertEqual(out.conversationEntries.length, 4);
        assertEqual(out.conversationEntries[0], 'Prompt 1: What is OSAI?');
        assertEqual(out.conversationEntries[3], 'AI response: It teaches AI concepts.');
    });
});

describe('Integration — OSAI201 (synthetic) flip card boundary indices', function () {
    it('startBlockIndex / endBlockIndex are correct after a heading scaffold', function () {
        // Synthetic fixture replicating an OSAI201 [flip card] inside an activity
        var blocks = [
            _intPara('Some intro paragraph.'),                  // 0
            _intPara('[Activity 1] Match the items'),           // 1
            _intPara('[flip card]'),                            // 2 — start
            _intTable(['Front', 'Back'],
                [['Term A', 'Definition A'], ['Term B', 'Definition B']]),  // 3
            _intPara('[front] Term A'),                         // 4 — child
            _intPara('[back] Definition A'),                    // 5 — child
            _intPara('[body]'),                                 // 6 — close
            _intPara('Continuing body content.')
        ];
        var out = intExtractor.processInteractive(
            blocks, 2, 'OSAI201-01.html', '1', /* insideActivity */ true);
        assertEqual(out.startBlockIndex, 2);
        assertEqual(out.endBlockIndex, 5,
            'boundary ends at the last consumed [back], NOT at [body]');
        assertEqual(out.childBlocks.length, 2);
    });
});

describe('Integration — body paragraph between two interactives is NOT leaked', function () {
    it('paragraph between two flip cards stays outside both boundaries', function () {
        // Synthetic fixture
        var blocks = [
            _intPara('[flip card]'),                       // 0
            _intPara('[front] F1'),                        // 1
            _intPara('[back] B1'),                         // 2
            _intPara('[body]'),                            // 3 — close (not consumed)
            _intPara('Outside body paragraph.'),           // 4 — must NOT be in either interactive
            _intPara('[flip card]'),                       // 5
            _intPara('[front] F2'),                        // 6
            _intPara('[back] B2')                          // 7
        ];
        var first = intExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        var second = intExtractor.processInteractive(blocks, 5, 'test.html', null, false);
        assertEqual(first.endBlockIndex, 2,
            'first card boundary ends BEFORE the body paragraph');
        assertTrue(second.startBlockIndex === 5,
            'second card starts AT the second flip card');
        // The body paragraph index (4) must fall OUTSIDE both ranges.
        assertTrue(4 > first.endBlockIndex && 4 < second.startBlockIndex,
            'body paragraph index 4 is between the two interactives');
    });
});

describe('Integration — generateReferenceDocument() surfaces new sub-sections', function () {
    it('reference doc includes Child Blocks / Conversation Entries / Boundary Writer Notes / Associated Media', function () {
        var blocks = [
            _intPara('[speech bubble Conversation layout]'),
            _intPara('Prompt 1: hello'),
            _intPara('[image] https://example.com/x.png'),
            _intPara('AI response: world'),
            _intPara('CS: tone should be friendly', { isRed: true }),
            _intPara('[body]')
        ];
        var out = intExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        var doc = intExtractor.generateReferenceDocument([out.referenceEntry], 'TEST');
        assertTrue(doc.indexOf('Conversation Entries') !== -1,
            'doc surfaces Conversation Entries section');
        assertTrue(doc.indexOf('Prompt 1: hello') !== -1,
            'first conversation entry text included');
        assertTrue(doc.indexOf('Associated Media') !== -1,
            'doc surfaces Associated Media section');
        assertTrue(doc.indexOf('https://example.com/x.png') !== -1,
            'image URL included in reference doc');
        assertTrue(doc.indexOf('Boundary Writer Notes') !== -1,
            'doc surfaces Boundary Writer Notes section');
        assertTrue(doc.indexOf('tone should be friendly') !== -1,
            'CS note text included in reference doc');
    });

    it('flip_card reference doc surfaces Child Blocks list', function () {
        var blocks = [
            _intPara('[flip card]'),
            _intTable(['Front', 'Back'], [['A', 'B']]),
            _intPara('[front] Front One'),
            _intPara('[back] Back One'),
            _intPara('[body]')
        ];
        var out = intExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        var doc = intExtractor.generateReferenceDocument([out.referenceEntry], 'TEST');
        assertTrue(doc.indexOf('Child Blocks') !== -1,
            'Child Blocks section present');
        assertTrue(doc.indexOf('[front]') !== -1, 'front child sub-tag present');
        assertTrue(doc.indexOf('[back]') !== -1, 'back child sub-tag present');
    });
});
