/**
 * Tests for Ordinal-to-Number Sub-Tag Normalization (Instruction 2)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

describe('Ordinal Normalization — Test 2.6.1: ENGJ402 accordion tab variants', function() {
    it('should normalise [First tab of accordion] to index 1', function() {
        var result = scoper.normaliseSubTag('[First tab of accordion]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 1);
    });

    it('should normalise [Second tab of accordion] to index 2', function() {
        var result = scoper.normaliseSubTag('[Second tab of accordion]', 'accordion', 1);
        assertNotNull(result);
        assertEqual(result.index, 2);
    });

    it('should normalise [Third accordion tab] to index 3', function() {
        var result = scoper.normaliseSubTag('[Third accordion tab]', 'accordion', 2);
        assertNotNull(result);
        assertEqual(result.index, 3);
    });

    it('should normalise [Forth accordion tab] to index 4 (misspelling)', function() {
        var result = scoper.normaliseSubTag('[Forth accordion tab]', 'accordion', 3);
        assertNotNull(result);
        assertEqual(result.index, 4);
    });

    it('should normalise [Fifth accordion tab] to index 5', function() {
        var result = scoper.normaliseSubTag('[Fifth accordion tab]', 'accordion', 4);
        assertNotNull(result);
        assertEqual(result.index, 5);
    });

    it('should normalise [Sixth accordion tab] to index 6', function() {
        var result = scoper.normaliseSubTag('[Sixth accordion tab]', 'accordion', 5);
        assertNotNull(result);
        assertEqual(result.index, 6);
    });
});

describe('Ordinal Normalization — Test 2.6.2: Word-numbered accordion tabs', function() {
    it('should normalise [accordion one] to index 1', function() {
        var result = scoper.normaliseSubTag('[accordion one]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });

    it('should normalise [Accordion two:] to index 2', function() {
        var result = scoper.normaliseSubTag('[Accordion two:]', 'accordion', 1);
        assertNotNull(result);
        assertEqual(result.index, 2);
    });

    it('should normalise [Accordion three: Routine] to index 3 with heading', function() {
        var result = scoper.normaliseSubTag('[Accordion three: Routine]', 'accordion', 2);
        assertNotNull(result);
        assertEqual(result.index, 3);
        assertNotNull(result.heading, 'Should have a heading');
        assert(result.heading.indexOf('Routine') !== -1 || result.heading.indexOf('routine') !== -1,
            'Heading should contain Routine');
    });
});

describe('Ordinal Normalization — Test 2.6.3: Flip card ordinals', function() {
    it('should normalise [First card, front H4 title] to card_front index 1 with H4', function() {
        var result = scoper.normaliseSubTag('[First card, front H4 title]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
        assertEqual(result.index, 1);
        assertEqual(result.headingLevel, 'H4');
    });

    it('should normalise [First card,back H4 title] to card_back index 1 with H4', function() {
        var result = scoper.normaliseSubTag('[First card,back H4 title]', 'flipcards', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'card_back');
        assertEqual(result.index, 1);
        assertEqual(result.headingLevel, 'H4');
    });
});

describe('Ordinal Normalization — Test 2.6.4: "Forth" misspelling', function() {
    it('should normalise [Forth accordion tab] to index 4', function() {
        var result = scoper.normaliseSubTag('[Forth accordion tab]', 'accordion', 3);
        assertNotNull(result);
        assertEqual(result.index, 4);
    });

    it('should normalise [Forth card, front H4 title] to index 4', function() {
        var result = scoper.normaliseSubTag('[Forth card, front H4 title]', 'flipcards', 3);
        assertNotNull(result);
        assertEqual(result.index, 4);
    });
});

describe('Ordinal Normalization — Test 2.6.6: Bare numbers as carousel slides', function() {
    it('should normalise [1] as slide index 1 within carousel scope', function() {
        var result = scoper.normaliseSubTag('[1]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 1);
    });

    it('should normalise [2] as slide index 2 within carousel scope', function() {
        var result = scoper.normaliseSubTag('[2]', 'carousel', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 2);
    });
});

describe('Ordinal Normalization — Test 2.6.7: Bare numbers outside carousel scope', function() {
    it('should NOT interpret [1] as slide outside carousel', function() {
        var result = scoper.normaliseSubTag('[1]', null, 0);
        assertNull(result, 'Should return null outside carousel scope');
    });
});

describe('Ordinal Normalization — Numeric accordion/tab markers', function() {
    it('should normalise [Tab 1] to tab index 1', function() {
        var result = scoper.normaliseSubTag('[Tab 1]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 1);
    });

    it('should normalise [Accordion tab 1] to tab index 1', function() {
        var result = scoper.normaliseSubTag('[Accordion tab 1]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 1);
    });

    it('should normalise [Accordion 1: INCOME] to tab index 1 with heading', function() {
        var result = scoper.normaliseSubTag('[Accordion 1: INCOME]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 1);
    });

    it('should normalise [New tab] to auto-incremented index', function() {
        var result = scoper.normaliseSubTag('[New tab]', 'accordion', 3);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 4, 'Should auto-increment from last index 3');
    });
});

describe('Ordinal Normalization — Slide markers', function() {
    it('should normalise [Slide 1] to slide index 1', function() {
        var result = scoper.normaliseSubTag('[Slide 1]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 1);
    });

    it('should normalise [Carousel Image 1] to slide index 1', function() {
        var result = scoper.normaliseSubTag('[Carousel Image 1]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 1);
    });
});

describe('Ordinal Normalization — [Inside tab] marker', function() {
    it('should recognise [Inside tab] as a no-op marker', function() {
        var result = scoper.normaliseSubTag('[Inside tab]', 'accordion', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'inside_tab');
        assertTrue(result.isMarkerOnly, 'Should be marker only');
    });
});

describe('Ordinal Normalization — Front/Back sub-tags', function() {
    it('should normalise [Front] to card_front', function() {
        var result = scoper.normaliseSubTag('[Front]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
    });

    it('should normalise [Back] to card_back', function() {
        var result = scoper.normaliseSubTag('[Back]', 'flipcards', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'card_back');
    });

    it('should normalise [Front of card] to card_front', function() {
        var result = scoper.normaliseSubTag('[Front of card]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
    });

    it('should normalise [Back of the card] to card_back', function() {
        var result = scoper.normaliseSubTag('[Back of the card]', 'flipcards', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'card_back');
    });

    it('should normalise [Flip card 1] to card_front index 1', function() {
        var result = scoper.normaliseSubTag('[Flip card 1]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
        assertEqual(result.index, 1);
    });
});
