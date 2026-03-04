/**
 * Tests for Ordinal & Verbose Sub-Tag Normalization
 *
 * Covers:
 *   Instruction 1: ORDINAL_MAP and resolveOrdinalOrNumber()
 *   Instruction 2: Accordion tab sub-tag normalization (Patterns A–E)
 *   Instruction 3: Flip card front/back sub-tag normalization (Patterns F–H)
 *   Instruction 4: Carousel slide sub-tag normalization (Patterns I–K)
 *   Instruction 5: TagNormaliser recognition (prevents "unrecognised" reports)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

// Helper to create mock paragraph content blocks
function mkPara(text) {
    return { type: 'paragraph', data: { text: text, runs: [{ text: text }] } };
}

function mkRedPara(text) {
    return { type: 'paragraph', data: { text: '\uD83D\uDD34[RED TEXT] ' + text + ' [/RED TEXT]\uD83D\uDD34', runs: [{ text: text }] } };
}

// ==========================================================================
// INSTRUCTION 1: ORDINAL_MAP and resolveOrdinalOrNumber()
// ==========================================================================

describe('Instruction 1 — resolveOrdinalOrNumber utility', function() {
    it('Test 1.3.1: should resolve ordinal words to numbers', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('first'), 1);
        assertEqual(normaliser.resolveOrdinalOrNumber('second'), 2);
        assertEqual(normaliser.resolveOrdinalOrNumber('third'), 3);
        assertEqual(normaliser.resolveOrdinalOrNumber('fourth'), 4);
        assertEqual(normaliser.resolveOrdinalOrNumber('fifth'), 5);
        assertEqual(normaliser.resolveOrdinalOrNumber('sixth'), 6);
        assertEqual(normaliser.resolveOrdinalOrNumber('seventh'), 7);
        assertEqual(normaliser.resolveOrdinalOrNumber('eighth'), 8);
        assertEqual(normaliser.resolveOrdinalOrNumber('ninth'), 9);
        assertEqual(normaliser.resolveOrdinalOrNumber('tenth'), 10);
    });

    it('should resolve "Forth" misspelling to 4', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('Forth'), 4);
        assertEqual(normaliser.resolveOrdinalOrNumber('forth'), 4);
    });

    it('should resolve cardinal words to numbers', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('one'), 1);
        assertEqual(normaliser.resolveOrdinalOrNumber('two'), 2);
        assertEqual(normaliser.resolveOrdinalOrNumber('three'), 3);
        assertEqual(normaliser.resolveOrdinalOrNumber('four'), 4);
        assertEqual(normaliser.resolveOrdinalOrNumber('five'), 5);
    });

    it('should be case-insensitive', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('SIXTH'), 6);
        assertEqual(normaliser.resolveOrdinalOrNumber('First'), 1);
        assertEqual(normaliser.resolveOrdinalOrNumber('FORTH'), 4);
    });

    it('should resolve numeric strings', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('10'), 10);
        assertEqual(normaliser.resolveOrdinalOrNumber('1'), 1);
        assertEqual(normaliser.resolveOrdinalOrNumber('42'), 42);
    });

    it('should return null for unrecognised words', function() {
        assertNull(normaliser.resolveOrdinalOrNumber('banana'));
        assertNull(normaliser.resolveOrdinalOrNumber(''));
        assertNull(normaliser.resolveOrdinalOrNumber(null));
    });
});

// ==========================================================================
// INSTRUCTION 2: ACCORDION TAB SUB-TAG NORMALIZATION
// ==========================================================================

describe('Instruction 2 — Test 2.8.1: ENGJ402 Lesson 1 verbose ordinal accordion tabs', function() {
    it('should normalise all 6 verbose ordinal tabs from ENGJ402 lines 146–210', function() {
        var tags = [
            { input: '[First tab of accordion]',  expectedIndex: 1 },
            { input: '[Second tab of accordion]', expectedIndex: 2 },
            { input: '[Third accordion tab]',     expectedIndex: 3 },
            { input: '[Forth accordion tab]',     expectedIndex: 4 },
            { input: '[Fifth accordion tab]',     expectedIndex: 5 },
            { input: '[Sixth accordion tab]',     expectedIndex: 6 }
        ];

        for (var i = 0; i < tags.length; i++) {
            var result = scoper.normaliseSubTag(tags[i].input, 'accordion', i);
            assertNotNull(result, 'Should match: ' + tags[i].input);
            assertEqual(result.subType, 'tab', 'subType for: ' + tags[i].input);
            assertEqual(result.index, tags[i].expectedIndex, 'index for: ' + tags[i].input);
        }
    });

    it('[Forth accordion tab] should map to index 4 despite misspelling', function() {
        var result = scoper.normaliseSubTag('[Forth accordion tab]', 'accordion', 3);
        assertNotNull(result);
        assertEqual(result.index, 4);
    });
});

describe('Instruction 2 — Test 2.8.2: Word-numbered accordion tabs', function() {
    it('should normalise [accordion one] to index 1 with no heading', function() {
        var result = scoper.normaliseSubTag('[accordion one]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 1);
        assertNull(result.heading);
    });

    it('should normalise [Accordion two:] to index 2', function() {
        var result = scoper.normaliseSubTag('[Accordion two:]', 'accordion', 1);
        assertNotNull(result);
        assertEqual(result.index, 2);
    });

    it('should normalise [Accordion three: Routine] to index 3 with heading "Routine"', function() {
        var result = scoper.normaliseSubTag('[Accordion three: Routine]', 'accordion', 2);
        assertNotNull(result);
        assertEqual(result.index, 3);
        assertNotNull(result.heading);
        assert(result.heading.indexOf('Routine') !== -1, 'Heading should contain Routine, got: ' + result.heading);
    });

    it('should normalise [accordion four] to index 4', function() {
        var result = scoper.normaliseSubTag('[accordion four]', 'accordion', 3);
        assertNotNull(result);
        assertEqual(result.index, 4);
    });
});

describe('Instruction 2 — Test 2.8.3: Numeric tab patterns (regression check)', function() {
    it('[Tab 1] should return tab index 1', function() {
        var result = scoper.normaliseSubTag('[Tab 1]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 1);
    });

    it('[tab 1] should return tab index 1 (lowercase)', function() {
        var result = scoper.normaliseSubTag('[tab 1]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });

    it('[TAB 1] should return tab index 1 (uppercase)', function() {
        var result = scoper.normaliseSubTag('[TAB 1]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });
});

describe('Instruction 2 — Test 2.8.4: Tab with suffixes/labels', function() {
    it('[Tab 1 body] should return contentHint "body"', function() {
        var result = scoper.normaliseSubTag('[Tab 1 body]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 1);
        assertEqual(result.contentHint, 'body');
        assertNull(result.heading);
    });

    it('[TAB 1 MODULE INTRODUCTION] should return heading', function() {
        var result = scoper.normaliseSubTag('[TAB 1 MODULE INTRODUCTION]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
        assertNotNull(result.heading);
        assert(result.heading.indexOf('MODULE INTRODUCTION') !== -1,
            'Heading should contain MODULE INTRODUCTION, got: ' + result.heading);
    });

    it('[Accordion 1: INCOME] should return heading "INCOME"', function() {
        var result = scoper.normaliseSubTag('[Accordion 1: INCOME]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
        assertNotNull(result.heading);
        assert(result.heading.indexOf('INCOME') !== -1,
            'Heading should contain INCOME, got: ' + result.heading);
    });

    it('[accordion 1 types of laws] should return heading', function() {
        var result = scoper.normaliseSubTag('[accordion 1 types of laws]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
        assertNotNull(result.heading);
    });

    it('[accordion 1 content] should return contentHint "content"', function() {
        var result = scoper.normaliseSubTag('[accordion 1 content]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
        assertEqual(result.contentHint, 'content');
    });
});

describe('Instruction 2 — Test 2.8.5: [New tab] auto-increment', function() {
    it('should auto-increment from lastIndex 3 to 4', function() {
        var result = scoper.normaliseSubTag('[New tab]', 'accordion', 3);
        assertNotNull(result);
        assertEqual(result.subType, 'tab');
        assertEqual(result.index, 4);
    });

    it('[new tab] lowercase should also auto-increment', function() {
        var result = scoper.normaliseSubTag('[new tab]', 'accordion', 3);
        assertNotNull(result);
        assertEqual(result.index, 4);
    });

    it('should start at 1 when lastIndex is 0', function() {
        var result = scoper.normaliseSubTag('[New tab]', 'accordion', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });

    it('[New tab] 1 variant with trailing number should auto-increment', function() {
        var result = scoper.normaliseSubTag('[New tab 1]', 'accordion', 2);
        assertNotNull(result);
        assertEqual(result.index, 3);
    });
});

describe('Instruction 2 — Test 2.8.6: [Inside tab] no-op', function() {
    it('should return a marker-only result (not a new tab)', function() {
        var result = scoper.normaliseSubTag('[Inside tab]', 'accordion', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'inside_tab');
        assertTrue(result.isMarkerOnly);
    });

    it('should be case-insensitive', function() {
        var result = scoper.normaliseSubTag('[inside tab]', 'accordion', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'inside_tab');
    });
});

// ==========================================================================
// INSTRUCTION 3: FLIP CARD FRONT/BACK SUB-TAG NORMALIZATION
// ==========================================================================

describe('Instruction 3 — Test 3.6.1: ENGJ402 Lesson 5 ordinal flip card tags', function() {
    it('should normalise all 8 flip card tags from ENGJ402 lines 990–1024', function() {
        // Reset mismatch tracking state
        scoper._lastCardFrontIndex = null;

        var tags = [
            { input: '[First card, front H4 title]',  subType: 'card_front', index: 1, hl: 'H4' },
            { input: '[First card,back H4 title]',    subType: 'card_back',  index: 1, hl: 'H4' },
            { input: '[Second card, front H4 title]', subType: 'card_front', index: 2, hl: 'H4' },
            { input: '[Second card, back H4 title]',  subType: 'card_back',  index: 2, hl: 'H4' },
            { input: '[Third card, front H4 title]',  subType: 'card_front', index: 3, hl: 'H4' },
            { input: '[Third card, back H4 title]',   subType: 'card_back',  index: 3, hl: 'H4' },
            { input: '[Forth card, front H4 title]',  subType: 'card_front', index: 4, hl: 'H4' },
            { input: '[Third card, back H4 title]',   subType: 'card_back',  index: 4, hl: 'H4' } // MISMATCH: says Third but should be 4
        ];

        for (var i = 0; i < tags.length; i++) {
            var result = scoper.normaliseSubTag(tags[i].input, 'flipcards', i);
            assertNotNull(result, 'Should match: ' + tags[i].input);
            assertEqual(result.subType, tags[i].subType, 'subType for tag ' + (i + 1) + ': ' + tags[i].input);
            assertEqual(result.index, tags[i].index, 'index for tag ' + (i + 1) + ': ' + tags[i].input);
            assertEqual(result.headingLevel, tags[i].hl, 'headingLevel for tag ' + (i + 1) + ': ' + tags[i].input);
        }
    });

    it('[Forth card, front H4 title] should be index 4 despite misspelling', function() {
        scoper._lastCardFrontIndex = null;
        var result = scoper.normaliseSubTag('[Forth card, front H4 title]', 'flipcards', 3);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
        assertEqual(result.index, 4);
        assertEqual(result.headingLevel, 'H4');
    });

    it('[First card,back H4 title] should handle no space after comma', function() {
        scoper._lastCardFrontIndex = 1;
        var result = scoper.normaliseSubTag('[First card,back H4 title]', 'flipcards', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'card_back');
        assertEqual(result.index, 1);
    });
});

describe('Instruction 3 — Copy-paste mismatch detection', function() {
    it('should correct card_back index when ordinal mismatches preceding card_front', function() {
        scoper._lastCardFrontIndex = null;

        // First, process card_front with index 4
        var front = scoper.normaliseSubTag('[Forth card, front H4 title]', 'flipcards', 3);
        assertEqual(front.index, 4);

        // Then, process card_back that says "Third" (index 3) — should be corrected to 4
        var back = scoper.normaliseSubTag('[Third card, back H4 title]', 'flipcards', 4);
        assertEqual(back.index, 4, 'Should use corrected index from preceding card_front');
    });
});

describe('Instruction 3 — Test 3.6.2: Simple [Front]/[Back] with auto-increment', function() {
    it('should auto-increment card index for sequential Front/Back pairs', function() {
        var front1 = scoper.normaliseSubTag('[Front]', 'flipcards', 0);
        assertEqual(front1.subType, 'card_front');
        assertEqual(front1.index, 1);

        var back1 = scoper.normaliseSubTag('[Back]', 'flipcards', 1);
        assertEqual(back1.subType, 'card_back');
        assertEqual(back1.index, 1);

        var front2 = scoper.normaliseSubTag('[Front]', 'flipcards', 1);
        assertEqual(front2.subType, 'card_front');
        assertEqual(front2.index, 2);

        var back2 = scoper.normaliseSubTag('[Back]', 'flipcards', 2);
        assertEqual(back2.subType, 'card_back');
        assertEqual(back2.index, 2);
    });
});

describe('Instruction 3 — Test 3.6.4: Verbose "of card" patterns', function() {
    it('[Front of card] should normalise to card_front', function() {
        var result = scoper.normaliseSubTag('[Front of card]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
    });

    it('[Back of the card] should normalise to card_back', function() {
        var result = scoper.normaliseSubTag('[Back of the card]', 'flipcards', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'card_back');
    });

    it('[Front of the flipcard] should normalise to card_front', function() {
        var result = scoper.normaliseSubTag('[Front of the flipcard]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
    });

    it('[Back of flipcard/clickdrop] should normalise to card_back', function() {
        var result = scoper.normaliseSubTag('[Back of flipcard/clickdrop]', 'flipcards', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'card_back');
    });
});

describe('Instruction 3 — Test 3.6.5: Numbered card markers', function() {
    it('[Flip Card 1] should normalise to card_front index 1', function() {
        var result = scoper.normaliseSubTag('[Flip Card 1]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
        assertEqual(result.index, 1);
    });

    it('[flip card 1] should normalise (lowercase)', function() {
        var result = scoper.normaliseSubTag('[flip card 1]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });

    it('[Flipcard 1] should normalise (no space)', function() {
        var result = scoper.normaliseSubTag('[Flipcard 1]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });

    it('[Card 1] should normalise to card_front index 1', function() {
        var result = scoper.normaliseSubTag('[Card 1]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
        assertEqual(result.index, 1);
    });
});

describe('Instruction 3 — Test 3.6.6: [drop] click-drop variant', function() {
    it('[drop] should normalise to card_front', function() {
        var result = scoper.normaliseSubTag('[drop]', 'clickdrop', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
    });

    it('[drop image] should normalise to card_front', function() {
        var result = scoper.normaliseSubTag('[drop image]', 'clickdrop', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
    });
});

describe('Instruction 3 — [front of card title and image N] patterns', function() {
    it('should handle [front of card title & image 1]', function() {
        var result = scoper.normaliseSubTag('[front of card title & image 1]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
        assertEqual(result.index, 1);
    });

    it('should handle [front of card title and image 1]', function() {
        var result = scoper.normaliseSubTag('[front of card title and image 1]', 'flipcards', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'card_front');
        assertEqual(result.index, 1);
    });
});

// ==========================================================================
// INSTRUCTION 4: CAROUSEL SLIDE SUB-TAG NORMALIZATION
// ==========================================================================

describe('Instruction 4 — Test 4.6.1: Bare numbers inside carousel scope', function() {
    it('[1] should be slide index 1 within carousel', function() {
        var result = scoper.normaliseSubTag('[1]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 1);
    });

    it('[2] should be slide index 2 within carousel', function() {
        var result = scoper.normaliseSubTag('[2]', 'carousel', 1);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 2);
    });

    it('[10] should be slide index 10 within carousel', function() {
        var result = scoper.normaliseSubTag('[10]', 'carousel', 9);
        assertNotNull(result);
        assertEqual(result.index, 10);
    });
});

describe('Instruction 4 — Test 4.6.2: Bare numbers OUTSIDE carousel scope', function() {
    it('[1] should return null outside carousel scope', function() {
        var result = scoper.normaliseSubTag('[1]', null, 0);
        assertNull(result);
    });

    it('[2] should return null outside carousel scope', function() {
        var result = scoper.normaliseSubTag('[2]', 'accordion', 0);
        assertNull(result);
    });
});

describe('Instruction 4 — Test 4.6.3: Slide with suffix', function() {
    it('[Slide 1] should normalise to slide index 1', function() {
        var result = scoper.normaliseSubTag('[Slide 1]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 1);
    });

    it('[Slide 1 - video] should include contentHint', function() {
        var result = scoper.normaliseSubTag('[Slide 1 - video]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 1);
        assertNotNull(result.contentHint);
    });

    it('[Slide 1: video] should handle colon separator', function() {
        var result = scoper.normaliseSubTag('[Slide 1: video]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });

    it('[Slide 1 heading] should handle text suffix', function() {
        var result = scoper.normaliseSubTag('[Slide 1 heading]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });
});

describe('Instruction 4 — Test 4.6.4: Prefixed slides', function() {
    it('[Carousel Image 1] should normalise to slide index 1', function() {
        var result = scoper.normaliseSubTag('[Carousel Image 1]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.subType, 'slide');
        assertEqual(result.index, 1);
    });

    it('[Expectations Slide 1] should normalise to slide index 1', function() {
        var result = scoper.normaliseSubTag('[Expectations Slide 1]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });

    it('[Needs Slide 1] should normalise to slide index 1', function() {
        var result = scoper.normaliseSubTag('[Needs Slide 1]', 'carousel', 0);
        assertNotNull(result);
        assertEqual(result.index, 1);
    });
});

// ==========================================================================
// INSTRUCTION 5: TAG NORMALISER RECOGNITION (prevents "unrecognised" reports)
// ==========================================================================

describe('Instruction 5 — TagNormaliser recognises ordinal accordion tabs', function() {
    it('[First tab of accordion] should NOT be unrecognised', function() {
        var result = normaliser.normaliseTag('[First tab of accordion]');
        assertNotNull(result);
        assertNotNull(result.normalised, 'Should have a normalised name');
        assertEqual(result.normalised, 'accordion_tab');
        assertEqual(result.number, 1);
        assertEqual(result.category, 'subtag');
    });

    it('[Sixth accordion tab] should NOT be unrecognised', function() {
        var result = normaliser.normaliseTag('[Sixth accordion tab]');
        assertNotNull(result);
        assertEqual(result.normalised, 'accordion_tab');
        assertEqual(result.number, 6);
    });

    it('[Forth accordion tab] misspelling should NOT be unrecognised', function() {
        var result = normaliser.normaliseTag('[Forth accordion tab]');
        assertNotNull(result);
        assertEqual(result.normalised, 'accordion_tab');
        assertEqual(result.number, 4);
    });
});

describe('Instruction 5 — TagNormaliser recognises word-numbered accordion', function() {
    it('[accordion one] should be recognised', function() {
        var result = normaliser.normaliseTag('[accordion one]');
        assertNotNull(result);
        assertEqual(result.normalised, 'accordion_tab');
        assertEqual(result.number, 1);
    });

    it('[Accordion three: Routine] should be recognised with modifier', function() {
        var result = normaliser.normaliseTag('[Accordion three: Routine]');
        assertNotNull(result);
        assertEqual(result.normalised, 'accordion_tab');
        assertEqual(result.number, 3);
        assertNotNull(result.modifier);
    });
});

describe('Instruction 5 — TagNormaliser recognises accordion N with label', function() {
    it('[Accordion 1: INCOME] should be recognised', function() {
        var result = normaliser.normaliseTag('[Accordion 1: INCOME]');
        assertNotNull(result);
        assertEqual(result.normalised, 'accordion_tab');
        assertEqual(result.number, 1);
    });

    it('[accordion 1 types of laws] should be recognised', function() {
        var result = normaliser.normaliseTag('[accordion 1 types of laws]');
        assertNotNull(result);
        assertEqual(result.normalised, 'accordion_tab');
    });
});

describe('Instruction 5 — TagNormaliser recognises ordinal flip card tags', function() {
    it('[First card, front H4 title] should be recognised as card_front', function() {
        var result = normaliser.normaliseTag('[First card, front H4 title]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_front');
        assertEqual(result.number, 1);
        assertEqual(result.level, 4);
        assertEqual(result.category, 'subtag');
    });

    it('[Forth card, front H4 title] misspelling should be recognised', function() {
        var result = normaliser.normaliseTag('[Forth card, front H4 title]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_front');
        assertEqual(result.number, 4);
    });

    it('[Second card, back H4 title] should be recognised as card_back', function() {
        var result = normaliser.normaliseTag('[Second card, back H4 title]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_back');
        assertEqual(result.number, 2);
        assertEqual(result.level, 4);
    });
});

describe('Instruction 5 — TagNormaliser recognises verbose front/back', function() {
    it('[Front of card] should be recognised', function() {
        var result = normaliser.normaliseTag('[Front of card]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_front');
        assertEqual(result.category, 'subtag');
    });

    it('[Back of the card] should be recognised', function() {
        var result = normaliser.normaliseTag('[Back of the card]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_back');
    });

    it('[Front of the flipcard] should be recognised', function() {
        var result = normaliser.normaliseTag('[Front of the flipcard]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_front');
    });

    it('[Back of flipcard/clickdrop] should be recognised', function() {
        var result = normaliser.normaliseTag('[Back of flipcard/clickdrop]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_back');
    });
});

describe('Instruction 5 — TagNormaliser recognises [Inside tab] and [New tab]', function() {
    it('[Inside tab] should be recognised as inside_tab subtag', function() {
        var result = normaliser.normaliseTag('[Inside tab]');
        assertNotNull(result);
        assertEqual(result.normalised, 'inside_tab');
        assertEqual(result.category, 'subtag');
    });

    it('[New tab] should be recognised as new_tab subtag', function() {
        var result = normaliser.normaliseTag('[New tab]');
        assertNotNull(result);
        assertEqual(result.normalised, 'new_tab');
        assertEqual(result.category, 'subtag');
    });

    it('[New tab 1] should be recognised', function() {
        var result = normaliser.normaliseTag('[New tab 1]');
        assertNotNull(result);
        assertEqual(result.normalised, 'new_tab');
    });
});

describe('Instruction 5 — TagNormaliser recognises extended slide patterns', function() {
    it('[Slide 1 - video] should be recognised', function() {
        var result = normaliser.normaliseTag('[Slide 1 - video]');
        assertNotNull(result);
        assertEqual(result.normalised, 'carousel_slide');
        assertEqual(result.number, 1);
    });

    it('[Slide 1 heading] should be recognised', function() {
        var result = normaliser.normaliseTag('[Slide 1 heading]');
        assertNotNull(result);
        assertEqual(result.normalised, 'carousel_slide');
        assertEqual(result.number, 1);
    });

    it('[Carousel Image 1] should be recognised', function() {
        var result = normaliser.normaliseTag('[Carousel Image 1]');
        assertNotNull(result);
        assertEqual(result.normalised, 'carousel_slide');
        assertEqual(result.number, 1);
    });

    it('[Expectations Slide 1] should be recognised', function() {
        var result = normaliser.normaliseTag('[Expectations Slide 1]');
        assertNotNull(result);
        assertEqual(result.normalised, 'carousel_slide');
    });
});

describe('Instruction 5 — TagNormaliser recognises numbered card/flipcard', function() {
    it('[Card 1] should be recognised as card_front', function() {
        var result = normaliser.normaliseTag('[Card 1]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_front');
        assertEqual(result.number, 1);
    });

    it('[Flipcard 1] should be recognised', function() {
        var result = normaliser.normaliseTag('[Flipcard 1]');
        assertNotNull(result);
        assertEqual(result.normalised, 'card_front');
        assertEqual(result.number, 1);
    });
});

describe('Instruction 5 — TagNormaliser recognises tab N with suffix', function() {
    it('[Tab 1 body] should be recognised', function() {
        var result = normaliser.normaliseTag('[Tab 1 body]');
        assertNotNull(result);
        assertEqual(result.normalised, 'tab');
        assertEqual(result.number, 1);
    });

    it('[TAB 1 MODULE INTRODUCTION] should be recognised', function() {
        var result = normaliser.normaliseTag('[TAB 1 MODULE INTRODUCTION]');
        assertNotNull(result);
        assertEqual(result.normalised, 'tab');
        assertEqual(result.number, 1);
    });
});

describe('Instruction 5 — Category lookup for new subtag names', function() {
    it('accordion_tab should be in subtag category', function() {
        assertEqual(normaliser.getCategory('accordion_tab'), 'subtag');
    });

    it('card_front should be in subtag category', function() {
        assertEqual(normaliser.getCategory('card_front'), 'subtag');
    });

    it('card_back should be in subtag category', function() {
        assertEqual(normaliser.getCategory('card_back'), 'subtag');
    });

    it('inside_tab should be in subtag category', function() {
        assertEqual(normaliser.getCategory('inside_tab'), 'subtag');
    });

    it('new_tab should be in subtag category', function() {
        assertEqual(normaliser.getCategory('new_tab'), 'subtag');
    });
});

describe('Instruction 5 — Existing patterns still work (regression)', function() {
    it('[Tab 1] should still normalise to tab (existing pattern)', function() {
        var result = normaliser.normaliseTag('[Tab 1]');
        assertNotNull(result);
        assertEqual(result.normalised, 'tab');
        assertEqual(result.number, 1);
        assertEqual(result.category, 'interactive');
    });

    it('[Slide 1] should still normalise to carousel_slide', function() {
        var result = normaliser.normaliseTag('[Slide 1]');
        assertNotNull(result);
        assertEqual(result.normalised, 'carousel_slide');
        assertEqual(result.number, 1);
    });

    it('[Accordion] should still normalise to accordion', function() {
        var result = normaliser.normaliseTag('[Accordion]');
        assertNotNull(result);
        assertEqual(result.normalised, 'accordion');
        assertEqual(result.category, 'interactive');
    });

    it('[Accordion 1] should still normalise to accordion with number', function() {
        var result = normaliser.normaliseTag('[Accordion 1]');
        assertNotNull(result);
        assertEqual(result.normalised, 'accordion');
        assertEqual(result.number, 1);
    });

    it('[Flip card] should still normalise to flip_card', function() {
        var result = normaliser.normaliseTag('[Flip card]');
        assertNotNull(result);
        assertEqual(result.normalised, 'flip_card');
    });

    it('[front] should still normalise via simple table', function() {
        var result = normaliser.normaliseTag('[front]');
        assertNotNull(result);
        assertEqual(result.normalised, 'front');
        assertEqual(result.category, 'subtag');
    });

    it('[back] should still normalise via simple table', function() {
        var result = normaliser.normaliseTag('[back]');
        assertNotNull(result);
        assertEqual(result.normalised, 'back');
    });

    it('[drop] should still normalise to back', function() {
        var result = normaliser.normaliseTag('[drop]');
        assertNotNull(result);
        assertEqual(result.normalised, 'back');
    });
});

// ==========================================================================
// INTEGRATION: Block scoping with ordinal sub-tags
// ==========================================================================

describe('Integration — Accordion with verbose ordinal tabs in block scoping', function() {
    it('should produce 6 tabs from verbose ordinal tags', function() {
        var blocks = [
            mkRedPara('[Accordion]'),
            mkRedPara('[First tab of accordion]'),
            mkPara('Content for tab 1'),
            mkRedPara('[Second tab of accordion]'),
            mkPara('Content for tab 2'),
            mkRedPara('[Third accordion tab]'),
            mkPara('Content for tab 3'),
            mkRedPara('[Forth accordion tab]'),
            mkPara('Content for tab 4'),
            mkRedPara('[Fifth accordion tab]'),
            mkPara('Content for tab 5'),
            mkRedPara('[Sixth accordion tab]'),
            mkPara('Content for tab 6'),
            mkRedPara('[end of accordion]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var accBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'accordion') {
                accBlock = result[i];
                break;
            }
        }

        assertNotNull(accBlock, 'Accordion block should be found');
        // Count tab children
        var tabCount = 0;
        for (var j = 0; j < accBlock.children.length; j++) {
            if (accBlock.children[j].subType === 'tab') {
                tabCount++;
            }
        }
        assertEqual(tabCount, 6, 'Should have 6 tabs from ordinal sub-tags');
        assert(!accBlock.implicitClose, 'Should have explicit close');
    });
});

describe('Integration — [Inside tab] does not create extra tabs in block scoping', function() {
    it('should skip [Inside tab] and keep correct tab count', function() {
        var blocks = [
            mkRedPara('[Accordion]'),
            mkRedPara('[First tab of accordion]'),
            mkPara('Tab 1 heading'),
            mkRedPara('[Inside tab]'),
            mkPara('Tab 1 body content'),
            mkRedPara('[Second tab of accordion]'),
            mkPara('Tab 2 content'),
            mkRedPara('[end accordion]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var accBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'accordion') {
                accBlock = result[i];
                break;
            }
        }

        assertNotNull(accBlock);
        var tabCount = 0;
        for (var j = 0; j < accBlock.children.length; j++) {
            if (accBlock.children[j].subType === 'tab') {
                tabCount++;
            }
        }
        assertEqual(tabCount, 2, 'Should have exactly 2 tabs (Inside tab is no-op)');
    });
});
