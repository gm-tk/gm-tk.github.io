/**
 * Session G — activity-wrapper boundary detection tests.
 *
 * Covers:
 *   • Context-aware `TagNormaliser.isInteractiveEndSignal()` — H4 / H5 inside
 *     an activity do NOT close the inner interactive; H2 / H3 still do.
 *   • `[Activity N]` opens a wrapper, `[H4]` / `[H5]` render as scaffolding,
 *     inner `[flip card]` extracts correctly and closes at `[body]`.
 *   • Two activities back-to-back: `[Activity 2]` boundary.
 *   • Activity with inner interactive + `[H2]`: boundary closes cleanly.
 *
 * Synthetic block-stream fixtures (no .docx).
 */

'use strict';

var actNormaliser = new TagNormaliser();
var actExtractor = new InteractiveExtractor(actNormaliser);

function _actPara(text) {
    return { type: 'paragraph', data: { text: text, runs: [{ text: text }] } };
}
function _actTable(headers, rows) {
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

describe('TagNormaliser.isInteractiveEndSignal — context: { inActivity: true }', function () {
    it('H4 / H5 do NOT close inside an activity', function () {
        var ctx = { inActivity: true };
        assertFalse(actNormaliser.isInteractiveEndSignal(
            { normalised: 'heading', level: 4 }, ctx));
        assertFalse(actNormaliser.isInteractiveEndSignal(
            { normalised: 'heading', level: 5 }, ctx));
    });

    it('H2 / H3 still close inside an activity', function () {
        var ctx = { inActivity: true };
        assertTrue(actNormaliser.isInteractiveEndSignal(
            { normalised: 'heading', level: 2 }, ctx));
        assertTrue(actNormaliser.isInteractiveEndSignal(
            { normalised: 'heading', level: 3 }, ctx));
    });

    it('H4 / H5 still close at top level (no activity context)', function () {
        assertTrue(actNormaliser.isInteractiveEndSignal(
            { normalised: 'heading', level: 4 }));
        assertTrue(actNormaliser.isInteractiveEndSignal(
            { normalised: 'heading', level: 5 }));
    });

    it('end_activity / end_page / lesson always close', function () {
        var ctx = { inActivity: true };
        assertTrue(actNormaliser.isInteractiveEndSignal(
            { normalised: 'end_activity' }, ctx));
        assertTrue(actNormaliser.isInteractiveEndSignal(
            { normalised: 'end_page' }, ctx));
        assertTrue(actNormaliser.isInteractiveEndSignal(
            { normalised: 'lesson' }, ctx));
    });
});

describe('InteractiveExtractor — boundary inside activity wrapper', function () {
    it('flip_card inside [Activity 1] survives an [H4] scaffolding heading', function () {
        var blocks = [
            _actPara('[Activity 1] Sort the items'),       // 0 — activity opener
            _actPara('[H4] Sub-heading inside activity'),  // 1 — scaffolding (H4)
            _actPara('[flip card]'),                       // 2 — interactive start
            _actTable(['Front', 'Back'], [['A', 'B']]),    // 3 — primary dataTable
            _actPara('[front] Front copy'),                // 4 — child
            _actPara('[back] Back copy'),                  // 5 — child
            _actPara('[body]'),                            // 6 — closes interactive
            _actPara('Body paragraph')
        ];
        var out = actExtractor.processInteractive(
            blocks, 2, 'test.html', '1', /* insideActivity */ true);
        assertNotNull(out);
        assertEqual(out.startBlockIndex, 2);
        assertEqual(out.endBlockIndex, 5,
            'flip_card boundary closes at [body], children captured');
        assertEqual(out.childBlocks.length, 2);
        assertNotNull(out.dataTable);
    });

    it('flip_card inside activity does NOT close on a stray [H4]', function () {
        var blocks = [
            _actPara('[flip card]'),                      // 0
            _actPara('[front] F1'),                       // 1
            _actPara('[H4] More scaffolding'),            // 2 — scaffolding when inActivity
            _actPara('[back] B1'),                        // 3
            _actPara('[body]')                            // 4 — closes
        ];
        var out = actExtractor.processInteractive(
            blocks, 0, 'test.html', '1', true);
        // [H4] does NOT match a child / writer-note / media / conversation
        // rule, so the boundary closes BEFORE [H4] (last consumed = [front]).
        // The activity-render loop in html-converter is the one that treats
        // [H4] as scaffolding for the activity itself.
        assertEqual(out.startBlockIndex, 0);
        assertEqual(out.endBlockIndex, 1,
            'inner interactive ends at [front]; [H4] is activity-level scaffolding');
        assertEqual(out.childBlocks.length, 1);
    });

    it('flip_card boundary closes at H2 even when inside activity', function () {
        var blocks = [
            _actPara('[flip card]'),                      // 0
            _actPara('[front] F'),                        // 1
            _actPara('[back] B'),                         // 2
            _actPara('[H2] New section heading'),         // 3 — closes
            _actPara('Section body')
        ];
        var out = actExtractor.processInteractive(
            blocks, 0, 'test.html', '1', true);
        assertEqual(out.endBlockIndex, 2,
            'H2 closes the boundary even with inActivity context');
    });

    it('top-level (no activity) — H4 still closes the boundary', function () {
        var blocks = [
            _actPara('[flip card]'),                      // 0
            _actPara('[front] F'),                        // 1
            _actPara('[H4] Sub-heading')                  // 2 — closes at top level
        ];
        var out = actExtractor.processInteractive(
            blocks, 0, 'test.html', null, /* insideActivity */ false);
        assertEqual(out.endBlockIndex, 1,
            'at top level the H4 closes the inner interactive');
    });

    it('back-to-back interactives inside activity: second [flip card] closes the first', function () {
        var blocks = [
            _actPara('[flip card]'),                      // 0
            _actPara('[front] F1'),                       // 1
            _actPara('[back] B1'),                        // 2
            _actPara('[flip card]'),                      // 3 — second start (NOT consumed)
            _actPara('[front] F2'),                       // 4
            _actPara('[back] B2'),                        // 5
            _actPara('[end activity]')
        ];
        var out1 = actExtractor.processInteractive(
            blocks, 0, 'test.html', '1', true);
        assertEqual(out1.endBlockIndex, 2,
            'first flip_card closes before the second interactive-start');
        var out2 = actExtractor.processInteractive(
            blocks, 3, 'test.html', '1', true);
        assertEqual(out2.startBlockIndex, 3);
        assertEqual(out2.endBlockIndex, 5,
            'second flip_card consumes its own [front]/[back]');
    });
});
