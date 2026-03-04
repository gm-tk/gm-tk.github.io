/**
 * Regression tests for existing TagNormaliser functionality.
 * Ensures new changes don't break pre-existing tag normalization.
 */

'use strict';

var normaliser = new TagNormaliser();

describe('TagNormaliser Regression — Structural tags', function() {
    it('should normalise [title bar]', function() {
        var result = normaliser.normaliseTag('[title bar]');
        assertEqual(result.normalised, 'title_bar');
        assertEqual(result.category, 'structural');
    });

    it('should normalise [module introduction]', function() {
        var result = normaliser.normaliseTag('[module introduction]');
        assertEqual(result.normalised, 'module_introduction');
    });

    it('should normalise [lesson overview]', function() {
        var result = normaliser.normaliseTag('[lesson overview]');
        assertEqual(result.normalised, 'lesson_overview');
    });

    it('should normalise [lesson content]', function() {
        var result = normaliser.normaliseTag('[lesson content]');
        assertEqual(result.normalised, 'lesson_content');
    });

    it('should normalise [end page]', function() {
        var result = normaliser.normaliseTag('[end page]');
        assertEqual(result.normalised, 'end_page');
    });

    it('should normalise [lesson 3]', function() {
        var result = normaliser.normaliseTag('[lesson 3]');
        assertEqual(result.normalised, 'lesson');
        assertEqual(result.number, 3);
    });
});

describe('TagNormaliser Regression — Heading tags', function() {
    it('should normalise [H1] to heading level 1', function() {
        var result = normaliser.normaliseTag('[H1]');
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, 1);
    });

    it('should normalise [H2] to heading level 2', function() {
        var result = normaliser.normaliseTag('[H2]');
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, 2);
    });

    it('should normalise [h5] to heading level 5', function() {
        var result = normaliser.normaliseTag('[h5]');
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, 5);
    });
});

describe('TagNormaliser Regression — Body tags', function() {
    it('should normalise [body]', function() {
        var result = normaliser.normaliseTag('[body]');
        assertEqual(result.normalised, 'body');
    });

    it('should normalise [body text]', function() {
        var result = normaliser.normaliseTag('[body text]');
        assertEqual(result.normalised, 'body');
    });
});

describe('TagNormaliser Regression — Activity tags', function() {
    it('should normalise [Activity 1A]', function() {
        var result = normaliser.normaliseTag('[Activity 1A]');
        assertEqual(result.normalised, 'activity');
        assertEqual(result.id, '1A');
    });

    it('should normalise [activity]', function() {
        var result = normaliser.normaliseTag('[activity]');
        assertEqual(result.normalised, 'activity');
    });

    it('should normalise [end activity]', function() {
        var result = normaliser.normaliseTag('[end activity]');
        assertEqual(result.normalised, 'end_activity');
    });

    it('should normalise [activity heading H3]', function() {
        var result = normaliser.normaliseTag('[activity heading H3]');
        assertEqual(result.normalised, 'activity_heading');
        assertEqual(result.level, 3);
    });
});

describe('TagNormaliser Regression — Interactive tags', function() {
    it('should normalise [drag and drop]', function() {
        var result = normaliser.normaliseTag('[drag and drop]');
        assertEqual(result.normalised, 'drag_and_drop');
    });

    it('should normalise [drag and drop column autocheck]', function() {
        var result = normaliser.normaliseTag('[drag and drop column autocheck]');
        assertEqual(result.normalised, 'drag_and_drop');
        assertNotNull(result.modifier);
    });

    it('should normalise [flip card]', function() {
        var result = normaliser.normaliseTag('[flip card]');
        assertEqual(result.normalised, 'flip_card');
    });

    it('should normalise [accordion]', function() {
        var result = normaliser.normaliseTag('[accordion]');
        assertEqual(result.normalised, 'accordion');
    });

    it('should normalise [click drop]', function() {
        var result = normaliser.normaliseTag('[click drop]');
        assertEqual(result.normalised, 'click_drop');
    });

    it('should normalise [carousel]', function() {
        var result = normaliser.normaliseTag('[carousel]');
        assertEqual(result.normalised, 'carousel');
    });

    it('should normalise [slide show]', function() {
        var result = normaliser.normaliseTag('[slide show]');
        assertEqual(result.normalised, 'carousel');
    });

    it('should normalise [speech bubble]', function() {
        var result = normaliser.normaliseTag('[speech bubble]');
        assertEqual(result.normalised, 'speech_bubble');
    });

    it('should normalise [tabs]', function() {
        var result = normaliser.normaliseTag('[tabs]');
        assertEqual(result.normalised, 'tabs');
    });

    it('should normalise [mcq]', function() {
        var result = normaliser.normaliseTag('[mcq]');
        assertEqual(result.normalised, 'mcq');
    });

    it('should normalise [radio quiz]', function() {
        var result = normaliser.normaliseTag('[radio quiz]');
        assertEqual(result.normalised, 'radio_quiz');
    });

    it('should normalise [true false]', function() {
        var result = normaliser.normaliseTag('[true false]');
        assertEqual(result.normalised, 'radio_quiz');
    });

    it('should normalise [info trigger]', function() {
        var result = normaliser.normaliseTag('[info trigger]');
        assertEqual(result.normalised, 'info_trigger');
    });

    it('should normalise [info trigger image]', function() {
        var result = normaliser.normaliseTag('[info trigger image]');
        assertEqual(result.normalised, 'info_trigger_image');
    });
});

describe('TagNormaliser Regression — Media tags', function() {
    it('should normalise [image]', function() {
        var result = normaliser.normaliseTag('[image]');
        assertEqual(result.normalised, 'image');
        assertEqual(result.category, 'media');
    });

    it('should normalise [video]', function() {
        var result = normaliser.normaliseTag('[video]');
        assertEqual(result.normalised, 'video');
        assertEqual(result.category, 'media');
    });

    it('should normalise [image 1]', function() {
        var result = normaliser.normaliseTag('[image 1]');
        assertEqual(result.normalised, 'image');
        assertEqual(result.number, 1);
    });
});

describe('TagNormaliser Regression — Link tags', function() {
    it('should normalise [button]', function() {
        var result = normaliser.normaliseTag('[button]');
        assertEqual(result.normalised, 'button');
        assertEqual(result.category, 'link');
    });

    it('should normalise [external link]', function() {
        var result = normaliser.normaliseTag('[external link]');
        assertEqual(result.normalised, 'external_link');
    });

    it('should normalise [external link button]', function() {
        var result = normaliser.normaliseTag('[external link button]');
        assertEqual(result.normalised, 'external_link_button');
    });
});

describe('TagNormaliser Regression — Styling tags', function() {
    it('should normalise [alert]', function() {
        var result = normaliser.normaliseTag('[alert]');
        assertEqual(result.normalised, 'alert');
        assertEqual(result.category, 'styling');
    });

    it('should normalise [important]', function() {
        var result = normaliser.normaliseTag('[important]');
        assertEqual(result.normalised, 'important');
    });

    it('should normalise [quote]', function() {
        var result = normaliser.normaliseTag('[quote]');
        assertEqual(result.normalised, 'quote');
    });

    it('should normalise [whakatauki]', function() {
        var result = normaliser.normaliseTag('[whakatauki]');
        assertEqual(result.normalised, 'whakatauki');
    });
});

describe('TagNormaliser Regression — Sub-tags', function() {
    it('should normalise [front]', function() {
        var result = normaliser.normaliseTag('[front]');
        assertEqual(result.normalised, 'front');
        assertEqual(result.category, 'subtag');
    });

    it('should normalise [back]', function() {
        var result = normaliser.normaliseTag('[back]');
        assertEqual(result.normalised, 'back');
    });

    it('should normalise [drop]', function() {
        var result = normaliser.normaliseTag('[drop]');
        assertEqual(result.normalised, 'back');
    });

    it('should normalise [Table wordSelect] to word_select', function() {
        var result = normaliser.normaliseTag('[Table wordSelect]');
        assertEqual(result.normalised, 'word_select');
    });
});

describe('TagNormaliser Regression — Red text processing', function() {
    it('should extract tags from red text', function() {
        var result = normaliser.processBlock('\uD83D\uDD34[RED TEXT] [H2] [/RED TEXT]\uD83D\uDD34');
        assert(result.tags.length > 0, 'Should find tags');
        assertEqual(result.tags[0].normalised, 'heading');
        assertEqual(result.tags[0].level, 2);
    });

    it('should extract instructions from red text', function() {
        var result = normaliser.processBlock(
            '\uD83D\uDD34[RED TEXT] [drag and drop column autocheck] They are in correct place [/RED TEXT]\uD83D\uDD34'
        );
        assert(result.tags.length > 0);
        assertEqual(result.tags[0].normalised, 'drag_and_drop');
        assert(result.redTextInstructions.length > 0, 'Should have instructions');
    });

    it('should handle whitespace-only red text', function() {
        var result = normaliser.processBlock('\uD83D\uDD34[RED TEXT]   [/RED TEXT]\uD83D\uDD34');
        assertTrue(result.isWhitespaceOnly);
    });
});

describe('TagNormaliser Regression — Video tag variants (new)', function() {
    it('should normalise [embed video]', function() {
        var result = normaliser.normaliseTag('[embed video]');
        assertEqual(result.normalised, 'video');
        assertEqual(result.category, 'media');
    });

    it('should normalise [imbed video]', function() {
        var result = normaliser.normaliseTag('[imbed video]');
        assertEqual(result.normalised, 'video');
    });

    it('should normalise [Insert video]', function() {
        var result = normaliser.normaliseTag('[Insert video]');
        assertEqual(result.normalised, 'video');
    });

    it('should normalise [embed film]', function() {
        var result = normaliser.normaliseTag('[embed film]');
        assertEqual(result.normalised, 'video');
    });

    it('should normalise [slideshow] to carousel', function() {
        var result = normaliser.normaliseTag('[slideshow]');
        assertEqual(result.normalised, 'carousel');
    });
});

describe('TagNormaliser Regression — Category lookup', function() {
    it('should return structural for title_bar', function() {
        assertEqual(normaliser.getCategory('title_bar'), 'structural');
    });

    it('should return heading for heading', function() {
        assertEqual(normaliser.getCategory('heading'), 'heading');
    });

    it('should return interactive for drag_and_drop', function() {
        assertEqual(normaliser.getCategory('drag_and_drop'), 'interactive');
    });

    it('should return media for video', function() {
        assertEqual(normaliser.getCategory('video'), 'media');
    });

    it('should return null for unknown', function() {
        assertNull(normaliser.getCategory('nonexistent_tag'));
    });
});
