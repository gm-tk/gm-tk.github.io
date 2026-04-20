/**
 * Tests for BS-R2 — Speech Bubble Leaf Conversion (pre-fix baseline).
 *
 * Houses the Group A regression guards that must remain unchanged by the
 * BS-R2 fix (adjacent typeMap / closerTypeMap entries — accordion, tabs,
 * activity, flipcards, alert) AND a Group B "PRE-DELETE BEHAVIOUR"
 * describe-block documenting the exact shape of the speech_bubble opener
 * result that the fix will remove.
 *
 * Group B will be DELETED (not commented out) in the same commit that
 * applies the fix to js/block-tag-matcher.js:102. Its intent is then
 * expressed by the inverted assertions in
 * tests/speechBubbleLeafPostFix.test.js.
 *
 * Mirrors the authoring conventions of tests/rotatingBannerCloserPreFix.test.js
 * and tests/blockScoping.test.js.
 */

'use strict';

(function() {
    var _norm = new TagNormaliser();
    var _scoper = new BlockScoper(_norm);
    var _tables = new BlockScoperTables();
    var _matcher = new BlockTagMatcher(_tables, function() { return false; });

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

    // Build a tagInfo array matching what BlockScoper._getBlockTags returns
    // for a given red-text tag — used to invoke _matchOpeningTag directly.
    function tagsFor(tagText) {
        var processed = _norm.processBlock(
            '\uD83D\uDD34[RED TEXT] ' + tagText + ' [/RED TEXT]\uD83D\uDD34'
        );
        return processed.tags || [];
    }

    // ------------------------------------------------------------------
    // Group A — adjacent typeMap / closerTypeMap entries must be unaffected
    // ------------------------------------------------------------------

    describe('BS-R2 Group A — adjacent opener/closer paths unaffected by the fix', function() {
        it('[accordion] opener still returns blockType "accordion" via typeMap', function() {
            var tags = tagsFor('[accordion]');
            var result = _matcher._matchOpeningTag(tags, redPara('[accordion]'));
            assertNotNull(result, 'accordion opener must match');
            assertEqual(result.blockType, 'accordion',
                '[accordion] must map to blockType "accordion"');
        });

        it('[tabs] opener still returns blockType "tabs" via typeMap', function() {
            var tags = tagsFor('[tabs]');
            var result = _matcher._matchOpeningTag(tags, redPara('[tabs]'));
            assertNotNull(result, 'tabs opener must match');
            assertEqual(result.blockType, 'tabs',
                '[tabs] must map to blockType "tabs"');
        });

        it('[activity] opener still returns blockType "activity" via typeMap', function() {
            var tags = tagsFor('[activity]');
            var result = _matcher._matchOpeningTag(tags, redPara('[activity]'));
            assertNotNull(result, 'activity opener must match');
            assertEqual(result.blockType, 'activity',
                '[activity] must map to blockType "activity"');
        });

        it('[flip card] opener still returns blockType "flipcards" via typeMap', function() {
            var tags = tagsFor('[flip cards]');
            var result = _matcher._matchOpeningTag(tags, redPara('[flip cards]'));
            assertNotNull(result, 'flip cards opener must match');
            assertEqual(result.blockType, 'flipcards',
                '[flip cards] must map to blockType "flipcards"');
        });

        it('[alert] opener still returns blockType "alert" via typeMap', function() {
            var tags = tagsFor('[alert]');
            var result = _matcher._matchOpeningTag(tags, redPara('[alert]'));
            assertNotNull(result, 'alert opener must match');
            assertEqual(result.blockType, 'alert',
                '[alert] must map to blockType "alert"');
        });

        it('[end accordion] closer still resolves to "accordion" via closerTypeMap', function() {
            var blocks = [
                redPara('[Accordion]'),
                redPara('[Tab 1]'),
                para('Tab 1 content'),
                redPara('[end accordion]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var accBlock = findBlockByType(result, 'accordion');
            assertNotNull(accBlock, 'Accordion block should be found');
            assertFalse(accBlock.implicitClose,
                'Accordion must be explicitly closed by [end accordion]');
        });
    });

    // ------------------------------------------------------------------
    // Group B — PRE-DELETE BEHAVIOUR (will be INVERTED by the fix)
    //
    // These two cases describe the silent dead-code state of the scoper
    // today: _matchOpeningTag returns a block-type for a speech_bubble
    // normalised tag, and scopeBlocks emits a scope with that type
    // (implicit-closed at EOF because there is no closer path).
    //
    // The same commit that removes js/block-tag-matcher.js:102 will DELETE
    // this describe-block (not comment it out). Its intent is expressed as
    // inverted assertions in tests/speechBubbleLeafPostFix.test.js.
    // ------------------------------------------------------------------

    describe('BS-R2 Group B — PRE-DELETE BEHAVIOUR (will be removed by the fix)', function() {
        it('_matchOpeningTag on a normalised speech_bubble tag returns blockType "speech_bubble"', function() {
            var tags = tagsFor('[speech bubble]');
            var result = _matcher._matchOpeningTag(tags, redPara('[speech bubble]'));
            assertNotNull(result,
                'PRE-FIX: [speech bubble] must open a scoper block via typeMap:102');
            assertEqual(result.blockType, 'speech_bubble',
                'PRE-FIX: typeMap:102 maps speech_bubble → "speech_bubble"');
        });

        it('scopeBlocks on [speech bubble]...[end speech bubble] emits a speech_bubble scope (implicit-close)', function() {
            var blocks = [
                redPara('[speech bubble]'),
                para('Character says something'),
                redPara('[end speech bubble]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var sbBlock = findBlockByType(result, 'speech_bubble');
            assertNotNull(sbBlock,
                'PRE-FIX: speech_bubble-typed block must appear in the output');
            assertTrue(sbBlock.implicitClose,
                'PRE-FIX: block implicit-closes at EOF because no closer path resolves [end speech bubble]');
        });
    });

})();
