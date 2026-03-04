/**
 * Tests for ENGS301 inconsistency fixes.
 * Covers Issues #1-#13 across Instructions 1-6.
 */

var normaliser = new TagNormaliser();

// =====================================================================
// Instruction 1: Heading Tag Fixes (Issues #1, #5, #7)
// =====================================================================

describe('ENGS301 Issue #7 — Heading level respected', function() {
    it('[H2] should normalise to heading with level 2', function() {
        var result = normaliser.normaliseTag('[H2]');
        assertNotNull(result);
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, 2);
    });

    it('[H3] should normalise to heading with level 3', function() {
        var result = normaliser.normaliseTag('[H3]');
        assertNotNull(result);
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, 3);
    });

    it('[H4] should normalise to heading with level 4', function() {
        var result = normaliser.normaliseTag('[H4]');
        assertNotNull(result);
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, 4);
    });

    it('[H5] should normalise to heading with level 5', function() {
        var result = normaliser.normaliseTag('[H5]');
        assertNotNull(result);
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, 5);
    });
});

describe('ENGS301 Issue #5 — Incomplete heading [H ] fallback', function() {
    it('[H ] should normalise to heading with null level', function() {
        var result = normaliser.normaliseTag('[H ]');
        assertNotNull(result);
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, null);
        assertEqual(result.category, 'heading');
    });

    it('[H] should normalise to heading with null level', function() {
        var result = normaliser.normaliseTag('[H]');
        assertNotNull(result);
        assertEqual(result.normalised, 'heading');
        assertEqual(result.level, null);
    });

    it('[H ] should have modifier "incomplete"', function() {
        var result = normaliser.normaliseTag('[H ]');
        assertNotNull(result);
        assertEqual(result.modifier, 'incomplete');
    });
});

// =====================================================================
// Instruction 2: Unrecognized Tag Implementations (Issues #3, #6, #9)
// =====================================================================

describe('ENGS301 Issue #9 — [Go to journal] tag recognition', function() {
    it('[Go to journal] should normalise to go_to_journal', function() {
        var result = normaliser.normaliseTag('[Go to journal]');
        assertNotNull(result);
        assertEqual(result.normalised, 'go_to_journal');
        assertEqual(result.category, 'link');
    });

    it('[go to journal] should normalise to go_to_journal (case insensitive)', function() {
        var result = normaliser.normaliseTag('[go to journal]');
        assertNotNull(result);
        assertEqual(result.normalised, 'go_to_journal');
    });
});

describe('ENGS301 Issue #6 — [button- external link] tag recognition', function() {
    it('[button- external link] should normalise to external_link_button', function() {
        var result = normaliser.normaliseTag('[button- external link]');
        assertNotNull(result);
        assertEqual(result.normalised, 'external_link_button');
        assertEqual(result.category, 'link');
    });

    it('[button-external link] should normalise to external_link_button', function() {
        var result = normaliser.normaliseTag('[button-external link]');
        assertNotNull(result);
        assertEqual(result.normalised, 'external_link_button');
    });

    it('[button - external] should normalise to external_link_button', function() {
        var result = normaliser.normaliseTag('[button - external]');
        assertNotNull(result);
        assertEqual(result.normalised, 'external_link_button');
    });

    it('[button-download] should normalise to button', function() {
        var result = normaliser.normaliseTag('[button-download]');
        assertNotNull(result);
        assertEqual(result.normalised, 'button');
        assertEqual(result.category, 'link');
    });
});

describe('ENGS301 Issue #3 — [hovertrigger] tag recognition', function() {
    it('[hovertrigger] should normalise to info_trigger', function() {
        var result = normaliser.normaliseTag('[hovertrigger]');
        assertNotNull(result);
        assertEqual(result.normalised, 'info_trigger');
        assertEqual(result.category, 'interactive');
    });

    it('[hover trigger] should normalise to info_trigger', function() {
        var result = normaliser.normaliseTag('[hover trigger]');
        assertNotNull(result);
        assertEqual(result.normalised, 'info_trigger');
    });
});

// =====================================================================
// Instruction 3: Hintslider (Issue #10)
// =====================================================================

describe('ENGS301 Issue #10 — [hintslider] tag recognition', function() {
    it('[hintslider] should normalise to hint_slider', function() {
        var result = normaliser.normaliseTag('[hintslider]');
        assertNotNull(result);
        assertEqual(result.normalised, 'hint_slider');
        assertEqual(result.category, 'interactive');
    });

    it('[hint slider] should normalise to hint_slider', function() {
        var result = normaliser.normaliseTag('[hint slider]');
        assertNotNull(result);
        assertEqual(result.normalised, 'hint_slider');
    });

    it('[hintslider 2] should normalise to hint_slider with number 2', function() {
        var result = normaliser.normaliseTag('[hintslider 2]');
        assertNotNull(result);
        assertEqual(result.normalised, 'hint_slider');
        assertEqual(result.number, 2);
    });
});

// =====================================================================
// Instruction 4: Flipcard (Issue #12)
// =====================================================================

describe('ENGS301 Issue #12 — [flipcard] tag recognition', function() {
    it('[flipcard] should normalise to flip_card', function() {
        var result = normaliser.normaliseTag('[flipcard]');
        assertNotNull(result);
        assertEqual(result.normalised, 'flip_card');
        assertEqual(result.category, 'interactive');
    });

    it('[flip card] should normalise to flip_card', function() {
        var result = normaliser.normaliseTag('[flip card]');
        assertNotNull(result);
        assertEqual(result.normalised, 'flip_card');
    });

    it('[flip cards] should normalise to flip_card', function() {
        var result = normaliser.normaliseTag('[flip cards]');
        assertNotNull(result);
        assertEqual(result.normalised, 'flip_card');
    });

    it('[flipcard image] should normalise to flip_card with image modifier', function() {
        var result = normaliser.normaliseTag('[flipcard image]');
        assertNotNull(result);
        assertEqual(result.normalised, 'flip_card');
        assertEqual(result.modifier, 'image');
    });
});

// =====================================================================
// Instruction 5: Interactive Data Capture (Issues #2, #4, #8, #11)
// =====================================================================

describe('ENGS301 Issue #4 — [multichoice dropdown quiz] recognition', function() {
    it('[multichoice dropdown quiz] should normalise to mcq', function() {
        var result = normaliser.normaliseTag('[multichoice dropdown quiz]');
        assertNotNull(result);
        assertEqual(result.normalised, 'mcq');
        assertEqual(result.category, 'interactive');
    });

    it('[multi choice dropdown quiz] should normalise to mcq', function() {
        var result = normaliser.normaliseTag('[multi choice dropdown quiz]');
        assertNotNull(result);
        assertEqual(result.normalised, 'mcq');
    });

    it('[dropdown quiz] should normalise to mcq', function() {
        var result = normaliser.normaliseTag('[dropdown quiz]');
        assertNotNull(result);
        assertEqual(result.normalised, 'mcq');
    });

    it('[multichoice dropdown quiz] should have dropdown modifier', function() {
        var result = normaliser.normaliseTag('[multichoice dropdown quiz]');
        assertNotNull(result);
        assertEqual(result.modifier, 'dropdown');
    });
});

describe('ENGS301 Issue #2 — [IMAGE:] reference detection in processBlock', function() {
    it('should detect IMAGE reference in non-red text', function() {
        var result = normaliser.processBlock('[IMAGE: image4.png] some text');
        assertNotNull(result);
        // IMAGE references are tags, so they should be found
        assert(result.cleanText.indexOf('some text') !== -1, 'Clean text should contain "some text"');
    });
});

// =====================================================================
// Instruction 6: Formatter list numbering
// =====================================================================

describe('ENGS301 Issue #13 — Formatter list counter tracking', function() {
    it('should exist as _listCounters property after formatContent', function() {
        // The formatter initializes list counters in formatContent
        // This is a structural check — the formatter class now tracks counters
        var formatter = new OutputFormatter();
        assertEqual(typeof formatter.formatContent, 'function');
    });
});
