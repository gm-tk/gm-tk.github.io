/**
 * Tests for Session H — inline-embedded start tag + layout-row sibling
 * capture plumbing added to
 * `InteractiveDataExtractor._consumeInteractiveBoundary()` and threaded
 * through `InteractiveExtractor.processInteractive()`.
 *
 * Covered fields (additive — all prior fields unchanged):
 *   - `startBlockInlineContent: string | null`
 *   - `layoutRowSiblings: Array<{ index, block, layoutRowId }>`
 *
 * Placeholder / reference-doc surfacing of the two new captures is
 * deferred to a follow-up session; these tests only exercise the
 * boundary-result plumbing.
 */

'use strict';

var sessionHNormaliser = new TagNormaliser();
var sessionHExtractor = new InteractiveExtractor(sessionHNormaliser);

// ------------------------------------------------------------------
// Helpers
// ------------------------------------------------------------------

function mkRun(text, isRed) {
    return {
        text: text,
        formatting: {
            bold: false, italic: false, underline: false,
            strikethrough: false,
            color: isRed ? 'FF0000' : null,
            highlight: null,
            isRed: !!isRed
        }
    };
}

// Build a paragraph block with alternating red / plain runs.
// Each part is { text, isRed? }.
function paraFromRuns(parts, extra) {
    var runs = [];
    for (var i = 0; i < parts.length; i++) {
        runs.push(mkRun(parts[i].text, parts[i].isRed));
    }
    var text = parts.map(function (p) { return p.text; }).join('');
    var block = { type: 'paragraph', data: { text: text, runs: runs } };
    if (extra) {
        for (var k in extra) {
            if (Object.prototype.hasOwnProperty.call(extra, k)) block[k] = extra[k];
        }
    }
    return block;
}

// Simple end-signal paragraph block (plain `[body]`).
function plainBlock(text, extra) {
    var block = {
        type: 'paragraph',
        data: { text: text, runs: [{ text: text }] }
    };
    if (extra) {
        for (var k in extra) {
            if (Object.prototype.hasOwnProperty.call(extra, k)) block[k] = extra[k];
        }
    }
    return block;
}

// Red-text-only tag block (e.g. `[body]`).
function redTagBlock(tagText, extra) {
    return paraFromRuns([{ text: tagText, isRed: true }], extra);
}

// ------------------------------------------------------------------
// Tests
// ------------------------------------------------------------------

describe('Session H — inline-embedded start tag captures', function () {

    it('(a) [speech bubble] Kia ora... → startBlockInlineContent contains trimmed remainder', function () {
        var blocks = [
            paraFromRuns([
                { text: '[speech bubble]', isRed: true },
                { text: " Kia ora I'm Ariā." }
            ]),
            plainBlock('[body]')
        ];
        var out = sessionHExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out, 'processInteractive returns a record');
        assertEqual(out.startBlockInlineContent, "Kia ora I'm Ariā.");
    });

    it('(b) [speech bubble] as sole text → startBlockInlineContent === null', function () {
        var blocks = [
            paraFromRuns([{ text: '[speech bubble]', isRed: true }]),
            plainBlock('[body]')
        ];
        var out = sessionHExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        assertEqual(out.startBlockInlineContent, null);
    });

});

describe('Session H — layout-row sibling capture', function () {

    it('(c) start block + sibling share _layoutRowId=L1 → sibling captured, endBlockIndex advances', function () {
        var blocks = [
            paraFromRuns([{ text: '[speech bubble]', isRed: true }], { _layoutRowId: 'L1' }),
            paraFromRuns([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/img.png' }
            ], { _layoutRowId: 'L1' }),
            plainBlock('[body]')
        ];
        var out = sessionHExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        assertEqual(out.layoutRowSiblings.length, 1);
        assertEqual(out.layoutRowSiblings[0].index, 1);
        assertEqual(out.layoutRowSiblings[0].layoutRowId, 'L1');
        assertEqual(out.endBlockIndex, 1);
    });

    it('(d) start _layoutRowId=L1 and sibling _layoutRowId=L2 → sibling NOT captured', function () {
        var blocks = [
            paraFromRuns([{ text: '[speech bubble]', isRed: true }], { _layoutRowId: 'L1' }),
            paraFromRuns([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/img.png' }
            ], { _layoutRowId: 'L2' }),
            plainBlock('[body]')
        ];
        var out = sessionHExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        assertEqual(out.layoutRowSiblings.length, 0);
    });

    it('(e) start block with no _layoutRowId → layoutRowSiblings === [] regardless of surroundings', function () {
        var blocks = [
            paraFromRuns([{ text: '[speech bubble]', isRed: true }]),  // no _layoutRowId
            paraFromRuns([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/img.png' }
            ], { _layoutRowId: 'L1' }),
            plainBlock('[body]')
        ];
        var out = sessionHExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        assertDeepEqual(out.layoutRowSiblings, []);
    });

    it('(f) boundary still closes at [body] when a layout-row sibling precedes the closer', function () {
        var blocks = [
            paraFromRuns([{ text: '[speech bubble]', isRed: true }], { _layoutRowId: 'L1' }),
            paraFromRuns([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/img.png' }
            ], { _layoutRowId: 'L1' }),
            plainBlock('[body]'),
            plainBlock('Body content after the interactive.')
        ];
        var out = sessionHExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        // Sibling at index 1 is captured. `[body]` at index 2 fires the
        // end-signal rule and is NOT consumed. endBlockIndex stops at 1.
        assertEqual(out.layoutRowSiblings.length, 1);
        assertEqual(out.endBlockIndex, 1);
    });

});

describe('Session H — referenceEntry surfaces new fields', function () {

    it('(g) referenceEntry contains both startBlockInlineContent and layoutRowSiblings populated from the boundary', function () {
        var blocks = [
            paraFromRuns([
                { text: '[speech bubble]', isRed: true },
                { text: " Kia ora I'm Ariā." }
            ], { _layoutRowId: 'L7' }),
            paraFromRuns([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/aria.png' }
            ], { _layoutRowId: 'L7' }),
            plainBlock('[body]')
        ];
        var out = sessionHExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        assertNotNull(out.referenceEntry, 'referenceEntry present');
        assertEqual(out.referenceEntry.startBlockInlineContent, "Kia ora I'm Ariā.");
        assertEqual(out.referenceEntry.layoutRowSiblings.length, 1);
        assertEqual(out.referenceEntry.layoutRowSiblings[0].index, 1);
        assertEqual(out.referenceEntry.layoutRowSiblings[0].layoutRowId, 'L7');
    });

});
