/**
 * Dropdown quiz paragraph — raw-content preservation fallback tests.
 *
 * Locks in the invariant: when a dropdown_quiz_paragraph interactive cannot
 * be rendered into its structured `<div class="dropQuiz" layout="paragraph">`
 * form, the placeholder body must contain the raw source content (story
 * heading + prose paragraphs with inline [Dropdown N] markers + complete
 * options table). Empty `Writer note: .` lines must never replace real
 * source content.
 *
 * Synthetic block-stream fixtures (no .docx).
 */

'use strict';

var dqpNormaliser = new TagNormaliser();
var dqpExtractor = new InteractiveExtractor(dqpNormaliser);

function _dqpPara(text, opts) {
    opts = opts || {};
    var run = { text: text };
    if (opts.isRed) run.formatting = { isRed: true };
    return { type: 'paragraph', data: { text: text, runs: [run] } };
}
function _dqpTable(headers, rows) {
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

function _dqpBuildFixture() {
    // [Activity 1] wrapping a [multi choice dropdown quiz paragraph] with one
    // [story heading], five prose paragraphs containing inline [Dropdown N]
    // markers, and a 5-column options table where each cell contains three
    // slash-separated options. Followed by [end of activity], [body], a
    // post-activity paragraph, and an unrelated [flip card] interactive.
    return [
        _dqpPara('[Activity 1] Reading practice'),                              // 0
        _dqpPara('[multi choice dropdown quiz paragraph]'),                     // 1
        _dqpPara('[story heading] The Mystery of the Missing Map'),            // 2
        _dqpPara('In the village of Aotea the children had [Dropdown 1] for weeks.'),       // 3
        _dqpPara('Aroha and Tama would [Dropdown 2] near the old totara tree.'),            // 4
        _dqpPara('The waka had been [Dropdown 3] in the rushing current.'),                 // 5
        _dqpPara('Every chimney was [Dropdown 4] with woodsmoke from the fires.'),          // 6
        _dqpPara('The missing map was [Dropdown 5] under a large flat stone.'),             // 7
        _dqpTable(null, [
            ['waited / longed / hoped',
             'sleep / lie / rest',
             'caught / trapped / stuck',
             'rising / smoking / blowing',
             'hidden / placed / found']
        ]),                                                                     // 8
        _dqpPara('[end of activity]'),                                          // 9
        _dqpPara('[body]'),                                                     // 10
        _dqpPara('After the activity, the children shared what they had learned.'), // 11
        _dqpPara('[flip card]'),                                                // 12
        _dqpPara('[front] Front of card'),                                      // 13
        _dqpPara('[back] Back of card'),                                        // 14
        _dqpPara('[body]')                                                      // 15
    ];
}

describe('Dropdown quiz paragraph — placeholder identification', function () {
    it('detects dropdown_quiz_paragraph subtype and emits placeholder with subtype label and activity number', function () {
        var blocks = _dqpBuildFixture();
        var out = dqpExtractor.processInteractive(blocks, 1, 'OSAI201-01.html', '1', true);
        assertNotNull(out);
        assertEqual(out.interactiveType, 'dropdown_quiz_paragraph');
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('INTERACTIVE PLACEHOLDER: dropdown_quiz_paragraph') !== -1,
            'placeholder header carries the dropdown_quiz_paragraph subtype label');
        assertTrue(html.indexOf('Activity 1') !== -1,
            'placeholder header carries the activity number');
    });
});

describe('Dropdown quiz paragraph — story heading preservation', function () {
    it('preserves the [story heading] content inside the placeholder body', function () {
        var blocks = _dqpBuildFixture();
        var out = dqpExtractor.processInteractive(blocks, 1, 'OSAI201-01.html', '1', true);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Story heading:') !== -1,
            'placeholder body labels the story heading');
        assertTrue(html.indexOf('The Mystery of the Missing Map') !== -1,
            'story heading title appears verbatim in placeholder body');
    });
});

describe('Dropdown quiz paragraph — prose paragraph preservation', function () {
    it('preserves all five prose paragraphs with inline [Dropdown N] markers visible verbatim', function () {
        var blocks = _dqpBuildFixture();
        var out = dqpExtractor.processInteractive(blocks, 1, 'OSAI201-01.html', '1', true);
        var html = out.placeholderHtml;
        for (var n = 1; n <= 5; n++) {
            assertTrue(html.indexOf('[Dropdown ' + n + ']') !== -1,
                '[Dropdown ' + n + '] marker visible verbatim in placeholder body');
        }
        assertTrue(html.indexOf('village of Aotea') !== -1, 'paragraph 1 prose preserved');
        assertTrue(html.indexOf('Aroha and Tama') !== -1, 'paragraph 2 prose preserved');
        assertTrue(html.indexOf('rushing current') !== -1, 'paragraph 3 prose preserved');
        assertTrue(html.indexOf('woodsmoke') !== -1, 'paragraph 4 prose preserved');
        assertTrue(html.indexOf('large flat stone') !== -1, 'paragraph 5 prose preserved');
    });
});

describe('Dropdown quiz paragraph — options table preservation', function () {
    it('preserves all five options-table columns with all three options per column (15 strings) intact', function () {
        var blocks = _dqpBuildFixture();
        var out = dqpExtractor.processInteractive(blocks, 1, 'OSAI201-01.html', '1', true);
        var html = out.placeholderHtml;
        var allOptions = [
            'waited', 'longed', 'hoped',
            'sleep', 'lie', 'rest',
            'caught', 'trapped', 'stuck',
            'rising', 'smoking', 'blowing',
            'hidden', 'placed', 'found'
        ];
        for (var i = 0; i < allOptions.length; i++) {
            assertTrue(html.indexOf(allOptions[i]) !== -1,
                'option string "' + allOptions[i] + '" present in placeholder body');
        }
        assertTrue(html.indexOf('<table') !== -1,
            'options preserved as an HTML <table> inside the placeholder body');
    });
});

describe('Dropdown quiz paragraph — Writer note suppression', function () {
    it('does not emit any empty Writer note: . entries for this subtype', function () {
        var blocks = _dqpBuildFixture();
        var out = dqpExtractor.processInteractive(blocks, 1, 'OSAI201-01.html', '1', true);
        var html = out.placeholderHtml;
        assertEqual(html.indexOf('Writer note: .'), -1,
            'no "Writer note: ." artifact emitted for dropdown_quiz_paragraph');
        assertEqual(html.indexOf('>Writer note:</'), -1,
            'no entirely empty "Writer note:" entry emitted for dropdown_quiz_paragraph');
    });
});

describe('Dropdown quiz paragraph — surrounding content not swallowed', function () {
    it('the [body] paragraph after [end of activity] renders outside the placeholder, in its normal post-activity position', function () {
        var blocks = _dqpBuildFixture();
        var out = dqpExtractor.processInteractive(blocks, 1, 'OSAI201-01.html', '1', true);
        // Consumed blocks span from the [multi choice dropdown quiz paragraph]
        // start (index 1) up to and including the options table (index 8).
        // The [end of activity] (9), [body] (10), and post-activity paragraph
        // (11) must all remain unconsumed and therefore render externally.
        assertEqual(out.blocksConsumed, 8,
            'blocksConsumed stops at the options table; post-activity content not swallowed');
        var html = out.placeholderHtml;
        assertEqual(html.indexOf('After the activity, the children shared'), -1,
            'post-activity body paragraph not embedded inside the placeholder');
        assertEqual(html.indexOf('[end of activity]'), -1,
            '[end of activity] marker not embedded inside the placeholder');
    });
});

describe('Dropdown quiz paragraph — non-paragraph interactive elsewhere unaffected', function () {
    it('a flip_card sibling in the same fixture still produces its expected child-block output', function () {
        var blocks = _dqpBuildFixture();
        var out = dqpExtractor.processInteractive(blocks, 12, 'OSAI201-01.html', null, false);
        assertNotNull(out);
        assertEqual(out.interactiveType, 'flip_card');
        var html = out.placeholderHtml;
        // Mirrors the assertion shape used by interactivePlaceholderFidelity.test.js
        // for flip_card: tier 1 green dashed border + child blocks section
        // listing the captured [front] / [back] entries.
        assertTrue(html.indexOf('border: 2px dashed green') !== -1,
            'flip_card retains tier 1 green dashed border');
        assertTrue(html.indexOf('Child blocks:') !== -1,
            'flip_card placeholder still surfaces Child blocks section');
        assertTrue(html.indexOf('Front of card') !== -1, '[front] content preserved');
        assertTrue(html.indexOf('Back of card') !== -1, '[back] content preserved');
    });
});
