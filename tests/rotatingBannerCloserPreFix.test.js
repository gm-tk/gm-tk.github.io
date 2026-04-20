/**
 * Tests for BS-R3 — Rotating Banner Explicit Closer Path (PRE-FIX baseline).
 *
 * This file locks the closer-path baseline for rotating_banner / rotatingbanner
 * *before* the BS-R3 fix lands. It has two clearly-labelled groups:
 *
 *   Group A — adjacent behaviour that must remain unchanged post-fix.
 *             These tests pass both before and after the BS-R3 fix and stay
 *             in place as permanent regression guards for the surrounding
 *             closer paths (carousel / accordion / flipcards / orphan-closer
 *             fallthrough / rotating banner opener).
 *
 *   Group B — PRE-FIX BEHAVIOUR that the BS-R3 fix will deliberately invert.
 *             These tests document the current (broken) return value so the
 *             regression is visible before the fix. Once the fix lands their
 *             intent is fully expressed by the post-fix companion file
 *             (tests/rotatingBannerCloserPostFix.test.js) — the Group B
 *             `describe(...)` block below will be DELETED (not commented out)
 *             in that same commit.
 *
 * Do not rely on the Group B assertions as forward-compatible contracts.
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

    // ------------------------------------------------------------------
    // Group B — PRE-FIX BEHAVIOUR (will be DELETED post-fix)
    // ------------------------------------------------------------------

    describe('BS-R3 Group B — PRE-FIX BEHAVIOUR (will be inverted in post-fix file)', function() {
        it('PRE-FIX: _fuzzyMatchCloser("end rotating banner") returns null (no carousel-group match)', function() {
            // Pre-fix: the space-separated form does not appear in closerTypeMap,
            // compactedMap, or any containment branch, so the closer falls
            // through to null. Post-fix this will return "carousel".
            var result = _matcher._fuzzyMatchCloser('end rotating banner');
            assertNull(result,
                'Pre-fix: [end rotating banner] currently has no closer path (falls through to null)');
        });

        it('PRE-FIX: _fuzzyMatchCloser("end rotatingbanner") returns null (no carousel-group match)', function() {
            // Pre-fix: the compacted form is absent from compactedMap and
            // no containment branch recognises "rotatingbanner". Post-fix
            // this will return "carousel".
            var result = _matcher._fuzzyMatchCloser('end rotatingbanner');
            assertNull(result,
                'Pre-fix: [end rotatingbanner] currently has no closer path (falls through to null)');
        });

        it('PRE-FIX: a [rotating banner] ... [end rotating banner] pair closes implicitly, not explicitly', function() {
            // Pre-fix: [end rotating banner] is not recognised as a closer, so
            // the block only terminates via an implicit mechanism (hard
            // boundary / same-type reopen / end-of-document / IE boundary).
            // Here the terminator is an [End page] hard boundary that
            // follows the (unrecognised) [end rotating banner] tag.
            var blocks = [
                redPara('[rotating banner]'),
                redPara('[Slide 1]'),
                para('Slide 1 content'),
                redPara('[Slide 2]'),
                para('Slide 2 content'),
                redPara('[end rotating banner]'),
                redPara('[End page]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var carBlock = findBlockByType(result, 'carousel');
            assertNotNull(carBlock, 'Carousel-typed block must still be found');
            assertTrue(carBlock.implicitClose,
                'Pre-fix: rotating_banner block is implicitly closed (no explicit closer match)');
        });
    });
})();
