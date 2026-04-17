/**
 * Tests for Session F — interactive-boundary detection algorithm
 * (`InteractiveExtractor._consumeInteractiveBoundary` and the new fields
 * populated on `processInteractive()`'s return: startBlockIndex /
 * endBlockIndex / childBlocks / conversationEntries / writerNotes /
 * associatedMedia / dataTable).
 *
 * Uses small synthetic block-stream fixtures (inline objects, no .docx).
 */

'use strict';

var boundaryNormaliser = new TagNormaliser();
var boundaryExtractor = new InteractiveExtractor(boundaryNormaliser);

function paraBlock(text, opts) {
    opts = opts || {};
    var run = { text: text };
    if (opts.isRed) run.formatting = { isRed: true };
    return {
        type: 'paragraph',
        data: { text: text, runs: [run] }
    };
}

function tableBlock(headers, rows) {
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

describe('InteractiveExtractor — boundary algorithm: flip_card', function () {
    it('captures [front]/[back] children + primary data table, closes at [body]', function () {
        var blocks = [
            paraBlock('[flip card]'),                     // 0 — start
            tableBlock(['Front', 'Back'], [['A', 'B']]),  // 1 — primary dataTable
            paraBlock('[front] Front copy'),              // 2 — child
            paraBlock('[back] Back copy'),                // 3 — child
            paraBlock('[body]'),                          // 4 — end signal (NOT consumed)
            paraBlock('More body content')
        ];
        var out = boundaryExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out, 'processInteractive returns a record');
        assertEqual(out.startBlockIndex, 0);
        assertEqual(out.endBlockIndex, 3);
        assertEqual(out.childBlocks.length, 2);
        assertEqual(out.childBlocks[0].tag.normalised, 'front');
        assertEqual(out.childBlocks[1].tag.normalised, 'back');
        assertNotNull(out.dataTable, 'dataTable captured');
    });
});

describe('InteractiveExtractor — boundary algorithm: speech_bubble conversation', function () {
    it('captures four Prompt/AI response paragraphs, closes at [body]', function () {
        var blocks = [
            paraBlock('[speech bubble Conversation layout]'),  // 0 — start (conversation)
            paraBlock('Prompt 1: What is AI?'),                // 1 — conv entry
            paraBlock('AI response: A field of study.'),       // 2 — conv entry
            paraBlock('Prompt 2: Give an example.'),           // 3 — conv entry
            paraBlock('AI response: Image recognition.'),      // 4 — conv entry
            paraBlock('[body]'),                               // 5 — end
            paraBlock('Body after the bubble.')
        ];
        var out = boundaryExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        assertEqual(out.startBlockIndex, 0);
        assertEqual(out.endBlockIndex, 4);
        assertEqual(out.conversationEntries.length, 4);
        assertEqual(out.conversationEntries[0], 'Prompt 1: What is AI?');
        assertEqual(out.conversationEntries[3], 'AI response: Image recognition.');
    });
});

describe('InteractiveExtractor — boundary algorithm: hint_slider with red-text note', function () {
    it('captures data table + writer note, closes at [body]', function () {
        var blocks = [
            paraBlock('[hint slider]'),                                 // 0 — start
            tableBlock(['Hint', 'Slide'], [['hint text', 'slide text']]), // 1 — table
            paraBlock('CS: please keep hint text short', { isRed: true }), // 2 — writer note
            paraBlock('[body]'),                                        // 3 — end
            paraBlock('more body')
        ];
        var out = boundaryExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        assertEqual(out.startBlockIndex, 0);
        assertEqual(out.endBlockIndex, 2);
        assertNotNull(out.dataTable);
        assertTrue(out.writerNotes.length >= 1,
            'writerNotes should capture the CS instruction, got: ' +
            JSON.stringify(out.writerNotes));
    });
});

describe('InteractiveExtractor — boundary algorithm: back-to-back interactives', function () {
    it('flip_card closes cleanly when a [carousel] follows', function () {
        var blocks = [
            paraBlock('[flip card]'),                     // 0
            paraBlock('[front] side A'),                  // 1
            paraBlock('[back] side B'),                   // 2
            paraBlock('[carousel]'),                      // 3 — next interactive-start (NOT consumed)
            paraBlock('[slide 1] first slide'),           // 4
            paraBlock('[body]')                           // 5
        ];
        var out1 = boundaryExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertEqual(out1.startBlockIndex, 0);
        assertEqual(out1.endBlockIndex, 2,
            'flip_card ends at last consumed child (before carousel)');
        assertEqual(out1.childBlocks.length, 2);

        var out2 = boundaryExtractor.processInteractive(blocks, 3, 'test.html', null, false);
        assertEqual(out2.startBlockIndex, 3);
        assertTrue(out2.childBlocks.length >= 1,
            'carousel picks up [slide 1] as a child');
    });
});

describe('InteractiveExtractor — boundary algorithm: structural closers', function () {
    it('[End page] closes the boundary without being consumed', function () {
        var blocks = [
            paraBlock('[flip card]'),        // 0
            paraBlock('[front] F'),          // 1
            paraBlock('[end page]'),         // 2 — end (not consumed)
            paraBlock('[lesson 3]')
        ];
        var out = boundaryExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertEqual(out.startBlockIndex, 0);
        assertEqual(out.endBlockIndex, 1,
            'boundary ends at the last consumed child before [end page]');
    });

    it('[alert] closes the boundary and is NOT captured into the interactive', function () {
        var blocks = [
            paraBlock('[flip card]'),            // 0
            paraBlock('[front] F'),              // 1
            paraBlock('[back] B'),               // 2
            paraBlock('[alert] warning text'),   // 3 — end (not consumed)
            paraBlock('[body]')
        ];
        var out = boundaryExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertEqual(out.endBlockIndex, 2,
            'boundary ends at [back], does not include [alert]');
        // Confirm the alert is not present among child blocks
        for (var i = 0; i < out.childBlocks.length; i++) {
            assertTrue(out.childBlocks[i].tag.normalised !== 'alert',
                '[alert] must not appear in childBlocks');
        }
    });
});
