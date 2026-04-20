/**
 * Tests for BS-R3 — Rotating Banner Explicit Closer Path (POST-FIX contract).
 *
 * These tests assert the target behaviour of the BS-R3 fix:
 *   • [end rotating banner] closes a rotating_banner block explicitly.
 *   • [end rotatingbanner]  (no space) closes it explicitly.
 *   • Case normalisation still works (mixed case matches).
 *   • The closer routes to the carousel group (matching the opener).
 *   • Orphan closers remain side-effect-free.
 *   • The explicit closer wins over the hard-boundary LOOKAHEAD fallback.
 *
 * This file is expected to FAIL before the fix lands in
 * js/block-scoper-tables.js + js/block-tag-matcher.js, and to pass after.
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

    describe('BS-R3 post-fix — explicit closer for rotating banner', function() {
        it('[end rotating banner] closes a rotating_banner block explicitly', function() {
            var blocks = [
                redPara('[rotating banner]'),
                redPara('[Slide 1]'),
                para('Slide 1 content'),
                redPara('[end rotating banner]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var carBlock = findBlockByType(result, 'carousel');
            assertNotNull(carBlock, 'carousel-typed block must be found');
            assertFalse(carBlock.implicitClose,
                '[end rotating banner] must close the block explicitly, not via implicit fallback');
        });

        it('[end rotatingbanner] (no space) also closes a rotating_banner block explicitly', function() {
            var blocks = [
                redPara('[rotating banner]'),
                redPara('[Slide 1]'),
                para('Slide 1 content'),
                redPara('[end rotatingbanner]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var carBlock = findBlockByType(result, 'carousel');
            assertNotNull(carBlock, 'carousel-typed block must be found');
            assertFalse(carBlock.implicitClose,
                '[end rotatingbanner] (no-space form) must close the block explicitly');
        });

        it('[End Rotating Banner] mixed case still closes (normalisation-consistent)', function() {
            var blocks = [
                redPara('[rotating banner]'),
                redPara('[Slide 1]'),
                para('Slide 1 content'),
                redPara('[End Rotating Banner]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var carBlock = findBlockByType(result, 'carousel');
            assertNotNull(carBlock, 'carousel-typed block must be found');
            assertFalse(carBlock.implicitClose,
                'Mixed-case [End Rotating Banner] must close the block explicitly');
        });

        it('_fuzzyMatchCloser routes "end rotating banner" and "end rotatingbanner" to the carousel group', function() {
            // Mirrors the convention used by existing sibling closers:
            //   _fuzzyMatchCloser("end carousel")   → "carousel"
            //   _fuzzyMatchCloser("end slideshow")  → "carousel"
            // Post-fix, both rotating banner forms must yield the same closer type.
            assertEqual(_matcher._fuzzyMatchCloser('end rotating banner'), 'carousel',
                '[end rotating banner] must map to the "carousel" closer group');
            assertEqual(_matcher._fuzzyMatchCloser('end rotatingbanner'), 'carousel',
                '[end rotatingbanner] must map to the "carousel" closer group');
        });

        it('orphan [end rotating banner] outside any active block does not crash or mis-close', function() {
            // With an empty block stack, _matchClosingTag() returns null at its guard
            // regardless of closer-type resolution. This test exercises the scoper's
            // top-level behaviour: an orphan rotating-banner closer must not cause a
            // crash and must not invent / mis-close any unrelated block.
            var blocks = [
                para('Some ordinary paragraph'),
                redPara('[end rotating banner]'),
                para('More paragraph')
            ];
            var result = _scoper.scopeBlocks(blocks);
            // No block-scoped wrapper should have appeared.
            for (var i = 0; i < result.length; i++) {
                assert(result[i].blockType !== 'carousel',
                    'Orphan [end rotating banner] must not conjure a carousel block');
                assert(result[i].blockType !== 'rotating_banner',
                    'Orphan [end rotating banner] must not conjure a rotating_banner block');
            }
        });

        it('explicit [end rotating banner] wins over the hard-boundary LOOKAHEAD fallback', function() {
            // Pre-fix this block would have closed only at the trailing [End page]
            // hard boundary. Post-fix the explicit closer must terminate the block,
            // so the body of content AFTER [end rotating banner] (and before
            // [End page]) must NOT be absorbed into the carousel block's contents.
            var blocks = [
                redPara('[rotating banner]'),
                redPara('[Slide 1]'),
                para('Slide 1 content'),
                redPara('[Slide 2]'),
                para('Slide 2 content'),
                redPara('[end rotating banner]'),
                para('Content after the banner'),
                redPara('[End page]')
            ];
            var result = _scoper.scopeBlocks(blocks);
            var carBlock = findBlockByType(result, 'carousel');
            assertNotNull(carBlock, 'carousel-typed block must be found');
            assertFalse(carBlock.implicitClose,
                'Explicit closer must take precedence over LOOKAHEAD / hard-boundary fallback');
            // The "Content after the banner" paragraph must live OUTSIDE the carousel block.
            // Top-level content that was not absorbed by any scoped block is emitted
            // as { type: 'unscoped', block: {...} } by BlockScoper.scopeBlocks().
            var outsideFound = false;
            for (var i = 0; i < result.length; i++) {
                var b = result[i];
                if (b.blockType) continue; // skip scoped wrappers
                var inner = b.block && b.block.data ? b.block.data.text : '';
                if (inner && inner.indexOf('Content after the banner') !== -1) {
                    outsideFound = true;
                    break;
                }
            }
            assertTrue(outsideFound,
                '"Content after the banner" must be emitted as a top-level unscoped block, not absorbed into the carousel');
        });
    });
})();
