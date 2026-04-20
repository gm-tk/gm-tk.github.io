/**
 * Tests for BS-R2 — Speech Bubble Leaf Conversion (adjacent-path guards).
 *
 * This file houses the Group A regression guards from the BS-R2
 * remediation: adjacent typeMap / closerTypeMap paths (accordion, tabs,
 * activity, flipcards, alert openers + [end accordion] closer) that
 * must remain unchanged by the fix. They passed both pre-fix and post-fix.
 *
 * The Group B "PRE-DELETE BEHAVIOUR" describe-block that originally
 * lived here was DELETED in the same commit that applied the fix to
 * js/block-tag-matcher.js. Its intent is now expressed by the
 * post-fix contract in tests/speechBubbleLeafPostFix.test.js.
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

})();
