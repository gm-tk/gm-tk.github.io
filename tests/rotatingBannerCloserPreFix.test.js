/**
 * Tests for BS-R3 — Rotating Banner Explicit Closer Path (adjacent-path guards).
 *
 * This file houses the Group A regression guards from the BS-R3 remediation:
 * adjacent closer/opener paths (carousel / accordion / flipcards / rotating
 * banner opener / orphan-closer fallthrough) that must remain unchanged by
 * the fix. They passed both pre-fix and post-fix.
 *
 * The Group B "PRE-FIX BEHAVIOUR" describe-block that originally lived here
 * was DELETED in the same commit that applied the fix. Its intent is now
 * expressed by the post-fix contract in tests/rotatingBannerCloserPostFix.test.js.
 */

'use strict';

// ---- Shared helpers (mirrors tests/blockScoping.test.js conventions) ----
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

    // ------------------------------------------------------------------
    // Group A — adjacent behaviour that must remain unchanged post-fix
    // ------------------------------------------------------------------

    describe('BS-R3 Group A — adjacent closers unaffected by the fix', function() {
        it('[end carousel] still closes a carousel block explicitly', function() {
            var blocks = [
                redPara('[Carousel]'),
                redPara('[Slide 1]'),
                para('Slide 1 content'),
                redPara('[end carousel]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var carBlock = findBlockByType(result, 'carousel');
            assertNotNull(carBlock, 'Carousel block should be found');
            assertFalse(carBlock.implicitClose,
                'Carousel must be explicitly closed by [end carousel]');
        });

        it('[end accordion] still closes an accordion block explicitly', function() {
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

        it('[end flipcards] still closes a flipcards block explicitly', function() {
            var blocks = [
                redPara('[Flip cards]'),
                redPara('[First card, front H4 title]'),
                para('Front 1'),
                redPara('[First card, back H4 title]'),
                para('Back 1'),
                redPara('[end flipcards]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var flipBlock = findBlockByType(result, 'flipcards');
            assertNotNull(flipBlock, 'Flipcards block should be found');
            assertFalse(flipBlock.implicitClose,
                'Flipcards must be explicitly closed by [end flipcards]');
        });

        it('[rotating banner] opener still opens a rotating_banner block (mapped to carousel)', function() {
            var blocks = [
                redPara('[rotating banner]'),
                redPara('[Slide 1]'),
                para('Slide 1 content'),
                redPara('[End page]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var carBlock = findBlockByType(result, 'carousel');
            assertNotNull(carBlock,
                '[rotating banner] must open a carousel-typed block (opener path is unchanged)');
        });

        it('an unrelated orphan closer ([end nonexistent-block]) returns null via _fuzzyMatchCloser', function() {
            // Orphan closers fall through every closerTypeMap / compactedMap /
            // containment branch and must return null so the block-scoper
            // does not mis-close an unrelated open block.
            var result = _matcher._fuzzyMatchCloser('end nonexistent-block');
            assertNull(result,
                'Unrelated orphan closer must not match any closer group');
        });
    });

})();
