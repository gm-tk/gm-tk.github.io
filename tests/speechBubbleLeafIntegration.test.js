/**
 * Integration tests for BS-R2 — Speech Bubble Leaf Conversion.
 *
 * Exercises the full pipeline on synthetic block sequences that mix
 * [speech bubble] tags through BlockScoper → InteractiveExtractor to
 * verify that removing js/block-tag-matcher.js:102 has no observable
 * effect on downstream output.
 *
 * Coverage split:
 *   • BlockScoper layer — speech_bubble is now a leaf; scopeBlocks must
 *     never emit a blockType: 'speech_bubble' wrapper, and any orphan
 *     [end speech bubble] falls through untouched.
 *   • InteractiveExtractor layer — IE pattern-8 (table cells) and
 *     pattern-9 (Conversation layout) both key on tagInfo.normalised
 *     (the tag-normaliser output) and are therefore insensitive to the
 *     scoper's typeMap. Per the docs/30 four-site audit, these paths
 *     are the real termination owners for speech_bubble interactives.
 *
 * Per docs/30 Cross-audit verification table, html-converter never
 * string-matches speech_bubble — it reaches the renderer via the
 * generic interactive handler in html-converter-block-renderer.js:366
 * which consumes the `referenceEntry` produced by processInteractive.
 * This file therefore exercises the HC generic-delegate posture
 * indirectly by asserting that the IE boundary output is well-formed
 * (the HC consumer reads that output verbatim).
 */

'use strict';

(function() {
    var _normaliser = new TagNormaliser();
    var _scoper = new BlockScoper(_normaliser);
    var _extractor = new InteractiveExtractor(_normaliser);

    function _intPara(text, opts) {
        opts = opts || {};
        var run = { text: text };
        if (opts.isRed) run.formatting = { isRed: true };
        return { type: 'paragraph', data: { text: text, runs: [run] } };
    }

    function _redPara(text) {
        return {
            type: 'paragraph',
            data: {
                text: '\uD83D\uDD34[RED TEXT] ' + text + ' [/RED TEXT]\uD83D\uDD34',
                runs: [{ text: text }]
            }
        };
    }

    function _intTable(headers, rows) {
        var allRows = [];
        if (headers) {
            allRows.push({
                cells: headers.map(function(h) {
                    return { paragraphs: [{ text: h, runs: [{ text: h }] }] };
                })
            });
        }
        for (var r = 0; r < rows.length; r++) {
            allRows.push({
                cells: rows[r].map(function(cell) {
                    return { paragraphs: [{ text: cell, runs: [{ text: cell }] }] };
                })
            });
        }
        return { type: 'table', data: { rows: allRows } };
    }

    describe('BS-R2 integration — BlockScoper produces NO speech_bubble-typed scope', function() {
        it('two [speech bubble] tags in the same page do NOT implicit-close each other (no scoper wrap at all)', function() {
            // Pre-fix this fixture would have produced two same-type openers and
            // implicit-closed the first at the second. Post-fix, neither tag
            // opens a block — they are leaves handed off to the IE layer.
            var blocks = [
                _redPara('[speech bubble]'),
                _intPara('First bubble body'),
                _redPara('[speech bubble]'),
                _intPara('Second bubble body')
            ];
            var result = _scoper.scopeBlocks(blocks);
            for (var i = 0; i < result.length; i++) {
                assertEqual(result[i].type, 'unscoped',
                    'entry ' + i + ' must be unscoped — scoper no longer opens speech_bubble blocks');
                assert(!result[i].blockType,
                    'no entry may carry a blockType — speech_bubble is a leaf');
            }
        });
    });

    describe('BS-R2 integration — InteractiveExtractor termination is unaffected', function() {
        it('pattern-9 Conversation layout: processInteractive captures all Prompt/Response entries', function() {
            // Mirrors the existing Session G fixture at
            // tests/interactiveBoundaryIntegration.test.js:73. After BS-R2 the
            // scoper no longer claims speech_bubble as a block, but the IE
            // pattern-9 path (data-extractor.js:217, :722) still reads
            // tag.normalised and owns termination via isInteractiveEndSignal.
            var blocks = [
                _intPara('[speech bubble Conversation layout]'),
                _intPara('Prompt 1: What is a leaf tag?'),
                _intPara('AI response: A tag the block-scoper never opens.'),
                _intPara('Prompt 2: Why remove it from typeMap?'),
                _intPara('AI response: Because no consumer reads its blockType.'),
                _intPara('[body]')
            ];
            var out = _extractor.processInteractive(blocks, 0, 'osai401.html', '1', false);
            assertNotNull(out, 'processInteractive must return a placeholder record');
            assertEqual(out.interactiveType, 'speech_bubble',
                'interactiveType must come from tagInfo.normalised — unaffected by BS-R2');
            assertEqual(out.conversationEntries.length, 4,
                'all four Prompt/Response entries must be captured');
            assertEqual(out.conversationEntries[0], 'Prompt 1: What is a leaf tag?');
            assertEqual(out.conversationEntries[3], 'AI response: Because no consumer reads its blockType.');
        });

        it('pattern-8 table: [speech bubble] with an associated table routes to dataPattern 8', function() {
            // Mirrors interactive-cell-parser.js:212 and
            // interactive-extractor-tables.js:53. Pattern 8 is the fallback
            // primary pattern for speech_bubble when no Conversation modifier
            // is present and a data table is attached.
            var blocks = [
                _intPara('[speech bubble]'),
                _intTable(
                    ['Speaker', 'Line'],
                    [
                        ['Alice', 'Hello there.'],
                        ['Bob', 'General Kenobi.']
                    ]
                ),
                _intPara('[body]')
            ];
            var out = _extractor.processInteractive(blocks, 0, 'osai201.html', '2', false);
            assertNotNull(out, 'processInteractive must return a placeholder record');
            assertEqual(out.interactiveType, 'speech_bubble',
                'interactiveType still derived from tag.normalised');
            assertEqual(out.dataPattern, 8,
                'pattern-8 classification must hold post-BS-R2 (cell-parser.js:212 + tables.js:53)');
            assertNotNull(out.referenceEntry,
                'referenceEntry must populate — this is the payload the html-converter generic delegate consumes');
            assertEqual(out.referenceEntry.type, 'speech_bubble',
                'referenceEntry.type must be speech_bubble so the generic interactive handler dispatches correctly');
        });

        it('[speech bubble] followed by H2 terminates at the H2 via isInteractiveEndSignal', function() {
            // The IE boundary walker owns speech_bubble termination. BS-R2
            // removes the scoper's silent-dead-code opener; the walker's
            // isInteractiveEndSignal logic (keyed on heading tags,
            // activity-wrapper, body marker) remains the termination source.
            var blocks = [
                _intPara('[speech bubble]'),
                _intPara('Bubble body line'),
                _intPara('[H2] The next section heading')
            ];
            var out = _extractor.processInteractive(blocks, 0, 'test.html', null, false);
            assertNotNull(out, 'processInteractive must return a record');
            // Boundary must stop before the H2 block (index 2).
            assert(out.endBlockIndex < 2,
                'IE walker must terminate before the H2 — endBlockIndex ' + out.endBlockIndex + ' expected < 2');
        });

        it('referenceEntry for speech_bubble is well-formed — HC generic delegate has no reason to string-match', function() {
            // Negative-confirmation integration test. The html-converter
            // generic interactive handler at html-converter-block-renderer.js:
            // 366-395 consumes `referenceEntry` without string-matching the
            // type. This test exercises the IE side of that contract: the
            // referenceEntry must carry a non-null type, tier, dataPattern,
            // and placeholderHtml — the four fields the handler reads.
            var blocks = [
                _intPara('[speech bubble]'),
                _intPara('A short character line.'),
                _intPara('[body]')
            ];
            var out = _extractor.processInteractive(blocks, 0, 'test.html', null, false);
            assertNotNull(out, 'processInteractive must return a record');
            assertEqual(out.referenceEntry.type, 'speech_bubble');
            assertEqual(out.referenceEntry.tier, 1,
                'speech_bubble is a Tier-1 interactive per TIER_1_TYPES at interactive-extractor-tables.js:19');
            assertNotNull(out.referenceEntry.dataPattern);
            assert(typeof out.placeholderHtml === 'string' && out.placeholderHtml.length > 0,
                'placeholderHtml must be non-empty — HC consumes it via the generic delegate');
        });
    });

})();
