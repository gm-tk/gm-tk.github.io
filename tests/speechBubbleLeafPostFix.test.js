/**
 * Tests for BS-R2 — Speech Bubble Leaf Conversion (POST-FIX contract).
 *
 * Asserts the target behaviour after the BS-R2 fix removes line 102
 * ('speech_bubble': 'speech_bubble') from the typeMap inside
 * BlockTagMatcher._getBlockTypeFromNormalised.
 *
 * Expected post-fix:
 *   • BlockTagMatcher no longer returns a block-type for speech_bubble.
 *   • BlockScoper emits unscoped entries for [speech bubble] — never a
 *     block-wrapper with blockType: 'speech_bubble'.
 *   • The tag-normaliser still emits tagInfo.normalised === 'speech_bubble'
 *     (classifier unaffected — leaf conversion is orthogonal).
 *   • The interactive-extractor still classifies pattern-8 / pattern-9
 *     via tag.normalised (IE owns termination semantics).
 *   • Orphan [end speech bubble] remains side-effect-free.
 *
 * This file is expected to FAIL before the fix lands in
 * js/block-tag-matcher.js:102 (the _matchOpeningTag assertions, the
 * _getBlockTypeFromNormalised assertion, and the scopeBlocks assertion
 * will fail), and to pass after.
 */

'use strict';

(function() {
    var _norm = new TagNormaliser();
    var _scoper = new BlockScoper(_norm);
    var _tables = new BlockScoperTables();
    var _matcher = new BlockTagMatcher(_tables, function() { return false; });
    var _ieTables = new InteractiveExtractorTables();
    var _cellParser = new InteractiveCellParser(_norm);

    function para(text) {
        return { type: 'paragraph', data: { text: text, runs: [{ text: text }] } };
    }

    function redPara(text) {
        return {
            type: 'paragraph',
            data: {
                text: '\uD83D\uDD34[RED TEXT] ' + text + ' [/RED TEXT]\uD83D\uDD34',
                runs: [{ text: text }]
            }
        };
    }

    function findBlockByType(blocks, blockType) {
        for (var i = 0; i < blocks.length; i++) {
            if (blocks[i].blockType === blockType) return blocks[i];
        }
        return null;
    }

    function tagsFor(tagText) {
        var processed = _norm.processBlock(
            '\uD83D\uDD34[RED TEXT] ' + tagText + ' [/RED TEXT]\uD83D\uDD34'
        );
        return processed.tags || [];
    }

    describe('BS-R2 post-fix — speech_bubble is a leaf (no block-scoper opener path)', function() {
        it('_matchOpeningTag on [speech bubble] returns null (no scope opened)', function() {
            var tags = tagsFor('[speech bubble]');
            var result = _matcher._matchOpeningTag(tags, redPara('[speech bubble]'));
            assertNull(result,
                'POST-FIX: speech_bubble opener path is removed; _matchOpeningTag must fall through to null');
        });

        it('_getBlockTypeFromNormalised({normalised:"speech_bubble"}) returns null', function() {
            var result = _matcher._getBlockTypeFromNormalised({ normalised: 'speech_bubble' });
            assertNull(result,
                'POST-FIX: typeMap no longer contains the speech_bubble entry; lookup must return null');
        });

        it('scopeBlocks on [speech bubble]...[end speech bubble] emits NO speech_bubble scope — both blocks unscoped', function() {
            var blocks = [
                redPara('[speech bubble]'),
                para('Character says something'),
                redPara('[end speech bubble]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var sbBlock = findBlockByType(result, 'speech_bubble');
            assertNull(sbBlock,
                'POST-FIX: no block with blockType "speech_bubble" may appear in the scoper output');
            // Both the start and the orphan end must emit as top-level unscoped entries.
            var unscopedCount = 0;
            for (var i = 0; i < result.length; i++) {
                if (!result[i].blockType && result[i].type === 'unscoped') {
                    unscopedCount++;
                }
            }
            assertEqual(unscopedCount, 3,
                'POST-FIX: all three paragraphs must be emitted as unscoped entries');
        });

        it('tag-normaliser still produces tagInfo.normalised === "speech_bubble" (classifier unaffected)', function() {
            var tags = tagsFor('[speech bubble]');
            assertTrue(tags.length > 0, 'tag-normaliser must still parse the tag');
            assertEqual(tags[0].normalised, 'speech_bubble',
                'POST-FIX: tag-normaliser classifier is orthogonal to block-scoper typeMap — normalised name must still be "speech_bubble"');
        });

        it('IE pattern-8 table path: cell-parser._detectTablePattern still returns 8 for speech_bubble', function() {
            // Mirrors the call site at js/interactive-cell-parser.js:212 — IE layer
            // classifies pattern-8 via the interactiveType string, which is derived
            // from tag.normalised (tag-normaliser output), not scoper blockType.
            // Leaf conversion must not disturb this path.
            var dummyTableData = { rows: [], headerRow: null, bodyRows: [] };
            var pattern = _cellParser._detectTablePattern(dummyTableData, 'speech_bubble');
            assertEqual(pattern, 8,
                'POST-FIX: pattern-8 classification is keyed on normalised tag name — unchanged');
        });

        it('IE pattern-8 lookup table (typeToPrimaryPattern) still carries the "speech_bubble": 8 entry', function() {
            // Mirrors the static-lookup site at js/interactive-extractor-tables.js:53.
            // This is the fallback dispatch used by interactive-extractor.js:63 when
            // `extracted.detectedPattern` is not set. Leaf conversion must not
            // disturb it (no scoper dependency).
            assertEqual(_ieTables.typeToPrimaryPattern['speech_bubble'], 8,
                'POST-FIX: typeToPrimaryPattern static table must still map speech_bubble → 8');
        });

        it('orphan [end speech bubble] closer path still returns null (unrecognised closer, unchanged)', function() {
            // Pre-fix and post-fix both: _fuzzyMatchCloser has no entry for
            // speech_bubble and never did. Leaf conversion does not introduce
            // one — the orphan closer remains side-effect-free.
            var result = _matcher._fuzzyMatchCloser('end speech bubble');
            assertNull(result,
                'POST-FIX: [end speech bubble] remains an unrecognised closer — no scoper group matches');
        });
    });

})();
