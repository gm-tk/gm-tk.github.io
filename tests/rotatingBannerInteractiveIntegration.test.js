/**
 * Integration tests for BS-R3 — Rotating Banner Explicit Closer Path.
 *
 * Exercises the full pipeline on a synthetic block sequence containing
 *   [rotating banner], [Slide 1], body, [Slide 2], body, [end rotating banner]
 * (and post-content that must not be absorbed into the rotating_banner
 * region at the block-scoper layer).
 *
 * Coverage split:
 *   • BlockScoper layer — the explicit closer from BS-R3 must terminate the
 *     carousel-typed scoped block AT the closer, keeping its children array
 *     bounded to the two slides and leaving post-content unscoped.
 *   • InteractiveExtractor layer — the IE walker is independent of the
 *     block-scoper and has its own boundary-detection logic
 *     (`_isEndBoundary` + `_collectNumberedItems`). Per the docs/28 cross-
 *     audit on BS-R3, the IE walker's behaviour must remain stable (no
 *     regression) now that `_matchClosingTag` can return a non-null result
 *     for `end rotating banner`. The IE walker itself still terminates via
 *     its own structural / activity / heading / body / styling / media /
 *     link category boundaries — not via the block-scoper's closer.
 *
 * Per the docs/29 negative-confirmation cross-audit, html-converter has no
 * direct `rotating_banner` code path (routed via the generic interactive
 * handler) so no html-converter integration is exercised here.
 */

'use strict';

(function() {
    var _normaliser = new TagNormaliser();
    var _scoper = new BlockScoper(_normaliser);
    var _extractor = new InteractiveExtractor(_normaliser);

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

    // Canonical pipeline fixture used across the describe-blocks below.
    function buildFixture() {
        return [
            redPara('[rotating banner]'),     // 0 — interactive start
            redPara('[Slide 1]'),             // 1 — carousel_slide subtag
            para('Slide 1 body'),             // 2 — slide 1 content
            redPara('[Slide 2]'),             // 3 — carousel_slide subtag
            para('Slide 2 body'),             // 4 — slide 2 content
            redPara('[end rotating banner]'), // 5 — explicit closer (BS-R3)
            para('Post content'),             // 6 — must remain unscoped
            redPara('[End page]')             // 7 — hard-boundary fallback
        ];
    }

    describe('BS-R3 integration — BlockScoper side of the pipeline', function() {
        it('scoper produces exactly one carousel-typed block for the rotating banner', function() {
            var scoped = _scoper.scopeBlocks(buildFixture());
            var count = 0;
            for (var i = 0; i < scoped.length; i++) {
                if (scoped[i].blockType === 'carousel') count++;
            }
            assertEqual(count, 1,
                'Exactly one carousel-typed block must be emitted for the rotating banner');
        });

        it('scoper terminates the rotating_banner at [end rotating banner] (explicit close)', function() {
            var scoped = _scoper.scopeBlocks(buildFixture());
            var carBlock = findBlockByType(scoped, 'carousel');
            assertNotNull(carBlock, 'carousel-typed block must be found');
            assertFalse(carBlock.implicitClose,
                'BS-R3: explicit [end rotating banner] must close the block, not a fallback');
            assertEqual(carBlock.lineEnd, 5,
                'Block must terminate at the line of the explicit closer (index 5)');
        });

        it('scoper children array contains exactly the two carousel_slide subtags', function() {
            var scoped = _scoper.scopeBlocks(buildFixture());
            var carBlock = findBlockByType(scoped, 'carousel');
            assertNotNull(carBlock);
            assertEqual(carBlock.children.length, 2,
                'Carousel must contain exactly two slide children — walker terminates at the closer');
            assertEqual(carBlock.children[0].subType, 'slide');
            assertEqual(carBlock.children[1].subType, 'slide');
            assertEqual(carBlock.children[0].index, 1);
            assertEqual(carBlock.children[1].index, 2);
        });

        it('post-content after the explicit closer is NOT absorbed into the rotating banner region', function() {
            var scoped = _scoper.scopeBlocks(buildFixture());
            var postFound = false;
            for (var i = 0; i < scoped.length; i++) {
                var b = scoped[i];
                if (b.blockType) continue; // scoped wrappers cannot hold raw text
                var inner = b.block && b.block.data ? b.block.data.text : '';
                if (inner && inner.indexOf('Post content') !== -1) {
                    postFound = true;
                    break;
                }
            }
            assertTrue(postFound,
                'Post content must live as a top-level unscoped block after the rotating_banner');
        });
    });

    describe('BS-R3 integration — InteractiveExtractor side of the pipeline', function() {
        it('processInteractive generates exactly one placeholder for the rotating banner', function() {
            var fixture = buildFixture();
            var out = _extractor.processInteractive(fixture, 0, 'test.html', null, false);
            assertNotNull(out, 'processInteractive must return a placeholder record');
            assertEqual(out.interactiveType, 'rotating_banner',
                'Interactive type must be rotating_banner');
            assertEqual(out.referenceEntry.type, 'rotating_banner',
                'Reference entry type must be rotating_banner');
            // The placeholder's boundary delimiters must appear exactly once each.
            var startCount = (out.placeholderHtml.match(/INTERACTIVE_START: rotating_banner/g) || []).length;
            var endCount = (out.placeholderHtml.match(/INTERACTIVE_END: rotating_banner/g) || []).length;
            assertEqual(startCount, 1, 'Placeholder must open exactly once');
            assertEqual(endCount, 1, 'Placeholder must close exactly once');
        });

        it('IE walker routes rotating_banner to pattern 5 (numbered slides) and collects both slides', function() {
            var fixture = buildFixture();
            var out = _extractor.processInteractive(fixture, 0, 'test.html', null, false);
            assertEqual(out.dataPattern, 5,
                'rotating_banner must route to pattern 5 (numbered slides)');
            var items = out.referenceEntry.numberedItems;
            assertNotNull(items, 'Reference entry must carry numberedItems for pattern 5');
            assertEqual(items.length, 2, 'Exactly two slide items must be collected');
            assertEqual(items[0].number, 1);
            assertEqual(items[1].number, 2);
            assertEqual(items[0].tag, 'carousel_slide');
            assertEqual(items[1].tag, 'carousel_slide');
        });

        it('BS-R3 does not destabilise the IE boundary walker (no crash, placeholder well-formed)', function() {
            // docs/28 audit pointed to three sites that rely on the IE walker's
            // own termination logic (tables.js:51 pattern map; data-extractor.js:
            // 479 _isSubTagFor carousel_slide → rotating_banner; data-extractor.js:
            // 567 pattern-5 dispatch). BS-R3 did not touch any of these sites;
            // this test is a regression guard that processInteractive still
            // returns a coherent record on the full synthetic fixture.
            var fixture = buildFixture();
            var out = _extractor.processInteractive(fixture, 0, 'test.html', null, false);
            assertNotNull(out, 'processInteractive must not return null');
            assert(typeof out.placeholderHtml === 'string' && out.placeholderHtml.length > 0,
                'placeholderHtml must be a non-empty string');
            assert(out.blocksConsumed >= 1,
                'blocksConsumed must be at least 1 (the tag block itself)');
        });
    });
})();
