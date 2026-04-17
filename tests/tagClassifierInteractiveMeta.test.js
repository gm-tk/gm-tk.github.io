/**
 * Tests for Session F — tag-classifier interactive metadata.
 *
 * Covers the new fields `isInteractiveStart` and `interactiveChildTags` added
 * to `category: 'interactive'` records, plus the `isInteractiveEndSignal()`
 * method added to `TagNormaliser`.
 */

'use strict';

var tnMeta = new TagNormaliser();

describe('TagNormaliser — isInteractiveStart flag', function () {
    it('flags [hint slider] / [flip card] / [carousel] / [speech bubble] / [click drop] / [accordion] / [Table wordSelect] as interactive starts', function () {
        var samples = [
            '[hint slider]', '[flip card]', '[carousel]', '[speech bubble]',
            '[click drop]', '[accordion]', '[Table wordSelect]'
        ];
        for (var i = 0; i < samples.length; i++) {
            var tag = tnMeta.normaliseTag(samples[i]);
            assertNotNull(tag, samples[i] + ' should normalise');
            assertEqual(tag.category, 'interactive', samples[i] + ' category');
            assertTrue(tag.isInteractiveStart === true,
                samples[i] + ' should have isInteractiveStart === true');
        }
    });

    it('does NOT flag [body] / [H2] / [alert] / [image] as interactive starts', function () {
        var nonInteractive = ['[body]', '[H2]', '[alert]', '[image]'];
        for (var i = 0; i < nonInteractive.length; i++) {
            var tag = tnMeta.normaliseTag(nonInteractive[i]);
            assertNotNull(tag, nonInteractive[i] + ' should normalise');
            assertTrue(tag.category !== 'interactive',
                nonInteractive[i] + ' should not be interactive');
            assertTrue(tag.isInteractiveStart !== true,
                nonInteractive[i] + ' should not have isInteractiveStart === true');
        }
    });

    it('does NOT flag interactive sub-tags [slide 1] / [tab 2] / [hint] / [shape 1] / [end accordions] as starts', function () {
        var subTags = ['[slide 1]', '[tab 2]', '[hint]', '[shape 1]', '[end accordions]'];
        for (var i = 0; i < subTags.length; i++) {
            var tag = tnMeta.normaliseTag(subTags[i]);
            assertNotNull(tag, subTags[i] + ' should normalise');
            assertTrue(tag.isInteractiveStart !== true,
                subTags[i] + ' must not be marked as an interactive start');
        }
    });
});

describe('TagNormaliser — interactiveChildTags map', function () {
    it('flip_card exposes ["front", "back"]', function () {
        var tag = tnMeta.normaliseTag('[flip card]');
        assertDeepEqual(tag.interactiveChildTags, ['front', 'back']);
    });

    it('click_drop exposes ["front", "back"] (drop normalises to back)', function () {
        var tag = tnMeta.normaliseTag('[click drop]');
        assertDeepEqual(tag.interactiveChildTags, ['front', 'back']);
    });

    it('carousel exposes carousel_slide / tab / image children', function () {
        var tag = tnMeta.normaliseTag('[carousel]');
        assertDeepEqual(tag.interactiveChildTags, ['carousel_slide', 'tab', 'image']);
    });

    it('accordion exposes ["tab", "carousel_slide"]', function () {
        var tag = tnMeta.normaliseTag('[accordion]');
        assertDeepEqual(tag.interactiveChildTags, ['tab', 'carousel_slide']);
    });

    it('speech_bubble exposes an empty child list (conversation uses inline paragraphs)', function () {
        var tag = tnMeta.normaliseTag('[speech bubble]');
        assertDeepEqual(tag.interactiveChildTags, []);
    });
});

describe('TagNormaliser — isInteractiveEndSignal()', function () {
    it('returns true for boundary-closing structural tags', function () {
        var closers = [
            '[body]', '[H2]', '[H3]', '[end page]', '[end activity]',
            '[lesson]', '[alert]', '[important]', '[whakatauki]', '[quote]'
        ];
        for (var i = 0; i < closers.length; i++) {
            var tag = tnMeta.normaliseTag(closers[i]);
            assertNotNull(tag, closers[i] + ' should normalise');
            assertTrue(tnMeta.isInteractiveEndSignal(tag) === true,
                closers[i] + ' should close interactive boundary');
        }
    });

    it('returns false for an untagged body paragraph (no tag object)', function () {
        // A paragraph with no square-bracket tag — the extractor passes null/undefined.
        assertFalse(tnMeta.isInteractiveEndSignal(null));
        assertFalse(tnMeta.isInteractiveEndSignal(undefined));
    });

    it('returns false for interactive sub-tags [front] / [back] / [drop]', function () {
        var subs = ['[front]', '[back]', '[drop]'];
        for (var i = 0; i < subs.length; i++) {
            var tag = tnMeta.normaliseTag(subs[i]);
            assertNotNull(tag, subs[i] + ' should normalise');
            assertFalse(tnMeta.isInteractiveEndSignal(tag),
                subs[i] + ' must not close interactive boundary');
        }
    });
});
