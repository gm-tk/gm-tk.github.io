/**
 * SubTagMatcher — Last-resort verbose/ordinal sub-tag pattern dispatcher.
 *
 * Extracted from `TagNormaliser._matchSubTag` (Session 1 of the tag-pipeline
 * audit series). Called by `TagNormaliser._normalise()` after the main
 * dispatch has exhausted the heading/structural/interactive/simple-lookup
 * branches, but before the tag is marked unrecognised.
 *
 * Covers:
 *   - `[Inside tab]`, `[New tab N]` — structural markers
 *   - Ordinal accordion tabs (`[First tab of accordion]`, `[Third accordion tab]`)
 *   - Word-numbered accordion headings (`[Accordion one: Routine]`)
 *   - Numbered accordion headings (`[Accordion 1: INCOME]`)
 *   - Ordinal flip-card subtags (`[First card, front H4 title]`)
 *   - Verbose front/back (`[Front of card]`, `[Back of flipcard/clickdrop]`)
 *   - `[Card N]`, `[Flipcard N]`, `[Tab N suffix]`
 *   - `[Slide N - video]`, `[Slide N heading]`, prefixed slide patterns
 *   - `[drop image]` click-drop single-tag variant
 *
 * @see CLAUDE.md Section 10 — Tag Taxonomy & Normalisation
 */

'use strict';

class SubTagMatcher {
    constructor(ordinalResolver) {
        this._ordinalResolver = ordinalResolver;
    }

    /**
     * Match verbose/ordinal sub-tag patterns that the standard normalisation
     * engine does not cover. Called as a last resort before marking a tag
     * as unrecognised.
     *
     * @param {string} flexCleaned - Lowercased, normalised tag text
     * @param {string} inner - Original inner tag text (preserves case)
     * @param {string} raw - Full raw tag with brackets
     * @returns {Object|null} Normalised tag object or null
     */
    match(flexCleaned, inner, raw) {
        // --- [Inside tab] no-op marker ---
        if (flexCleaned === 'inside tab') {
            return {
                normalised: 'inside_tab', level: null, number: null,
                id: null, category: 'subtag', modifier: null, raw: raw
            };
        }

        // --- [New tab] / [New tab 1] auto-increment marker ---
        if (/^new\s+tab(?:\s+\d+)?$/.test(flexCleaned)) {
            return {
                normalised: 'new_tab', level: null, number: null,
                id: null, category: 'subtag', modifier: null, raw: raw
            };
        }

        // --- Ordinal accordion tab: [First tab of accordion], [Third accordion tab] ---
        var ordAccMatch = flexCleaned.match(
            /^(first|second|third|forth|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+(?:tab\s+of\s+accordion|accordion\s+tab)$/
        );
        if (ordAccMatch) {
            return {
                normalised: 'accordion_tab', level: null,
                number: this._ordinalResolver.resolveOrdinalOrNumber(ordAccMatch[1]),
                id: null, category: 'subtag', modifier: null, raw: raw
            };
        }

        // --- Word-numbered accordion: [accordion one], [Accordion two: Routine] ---
        var wordAccMatch = flexCleaned.match(
            /^accordion\s+(one|two|three|four|five|six|seven|eight|nine|ten)\s*:?\s*(.*)$/
        );
        if (wordAccMatch) {
            var wordAccLabel = wordAccMatch[2] ? wordAccMatch[2].trim() : null;
            // Preserve original case for label
            if (wordAccLabel) {
                var labelStart = inner.toLowerCase().indexOf(wordAccMatch[2].trim().charAt(0));
                if (labelStart !== -1 && wordAccMatch[2].trim()) {
                    wordAccLabel = inner.substring(labelStart).trim();
                }
            }
            return {
                normalised: 'accordion_tab', level: null,
                number: this._ordinalResolver.resolveOrdinalOrNumber(wordAccMatch[1]),
                id: null, category: 'subtag', modifier: wordAccLabel || null, raw: raw
            };
        }

        // --- Accordion N with label/content: [Accordion 1: INCOME], [accordion 1 types of laws] ---
        var accNLabel = flexCleaned.match(/^accordion\s+(\d+)\s*:?\s+(.+)$/);
        if (accNLabel) {
            var accLabel = accNLabel[2].trim();
            // Preserve original case
            var accLabelStart = inner.lastIndexOf(accNLabel[2].trim().charAt(0));
            if (accLabelStart !== -1) {
                accLabel = inner.substring(accLabelStart).trim();
            }
            return {
                normalised: 'accordion_tab', level: null,
                number: parseInt(accNLabel[1], 10),
                id: null, category: 'subtag', modifier: accLabel, raw: raw
            };
        }

        // --- Ordinal flip card: [First card, front H4 title], [Forth card, front H4 title] ---
        var ordFlipMatch = flexCleaned.match(
            /^(first|second|third|forth|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+card\s*,?\s*(front|back)\s*(h\d)?\s*(title)?$/
        );
        if (ordFlipMatch) {
            var flipSide = ordFlipMatch[2] === 'front' ? 'card_front' : 'card_back';
            var flipLevel = ordFlipMatch[3] ? parseInt(ordFlipMatch[3].charAt(1), 10) : null;
            return {
                normalised: flipSide, level: flipLevel,
                number: this._ordinalResolver.resolveOrdinalOrNumber(ordFlipMatch[1]),
                id: null, category: 'subtag', modifier: null, raw: raw
            };
        }

        // --- Verbose front/back: [Front of card], [Back of the flipcard], [Back of flipcard/clickdrop] ---
        var frontOfMatch = flexCleaned.match(
            /^(front|back)\s+of\s+(?:the\s+)?(?:card|flipcard|flip\s*card)(?:\/\w+)?$/
        );
        if (frontOfMatch) {
            return {
                normalised: frontOfMatch[1] === 'front' ? 'card_front' : 'card_back',
                level: null, number: null,
                id: null, category: 'subtag', modifier: null, raw: raw
            };
        }

        // --- [front of card title & image N] / [front of card title and image N] ---
        var frontTitleImgMatch = flexCleaned.match(
            /^front\s+of\s+card\s+title\s+(?:&|and)\s+image\s+(\d+)$/
        );
        if (frontTitleImgMatch) {
            return {
                normalised: 'card_front', level: null,
                number: parseInt(frontTitleImgMatch[1], 10),
                id: null, category: 'subtag', modifier: null, raw: raw
            };
        }

        // --- [Card N] standalone ---
        var cardNMatch = flexCleaned.match(/^card\s+(\d+)$/);
        if (cardNMatch) {
            return {
                normalised: 'card_front', level: null,
                number: parseInt(cardNMatch[1], 10),
                id: null, category: 'subtag', modifier: null, raw: raw
            };
        }

        // --- [Flipcard N] (no space) ---
        var flipcardNMatch = flexCleaned.match(/^flipcard\s+(\d+)$/);
        if (flipcardNMatch) {
            return {
                normalised: 'card_front', level: null,
                number: parseInt(flipcardNMatch[1], 10),
                id: null, category: 'subtag', modifier: null, raw: raw
            };
        }

        // --- Tab N with suffix: [Tab 1 body], [TAB 1 MODULE INTRODUCTION] ---
        var tabSuffixMatch = flexCleaned.match(/^tab\s+(\d+)\s+(.+)$/);
        if (tabSuffixMatch) {
            var tabSuffix = tabSuffixMatch[2].trim();
            // Preserve original case for suffix
            var tabSufStart = inner.lastIndexOf(tabSuffixMatch[2].trim().charAt(0));
            if (tabSufStart !== -1) {
                tabSuffix = inner.substring(tabSufStart).trim();
            }
            return {
                normalised: 'tab', level: null,
                number: parseInt(tabSuffixMatch[1], 10),
                id: null, category: 'subtag', modifier: tabSuffix, raw: raw
            };
        }

        // --- Slide N with suffix: [Slide 1 - video], [Slide 1: heading] ---
        var slideSuffixMatch = flexCleaned.match(/^slide\s+(\d+)\s+[-–:]\s*(.+)$/);
        if (slideSuffixMatch) {
            return {
                normalised: 'carousel_slide', level: null,
                number: parseInt(slideSuffixMatch[1], 10),
                id: null, category: 'interactive',
                modifier: slideSuffixMatch[2].trim(), raw: raw
            };
        }

        // --- Slide N with text suffix (no separator): [Slide 1 heading] ---
        var slideTextMatch = flexCleaned.match(/^slide\s+(\d+)\s+(.+)$/);
        if (slideTextMatch) {
            return {
                normalised: 'carousel_slide', level: null,
                number: parseInt(slideTextMatch[1], 10),
                id: null, category: 'interactive',
                modifier: slideTextMatch[2].trim(), raw: raw
            };
        }

        // --- Prefixed slides: [Carousel Image N], [Expectations Slide N], [Needs Slide N] ---
        var prefixedSlideMatch = flexCleaned.match(
            /^(?:carousel\s+image|(?:\w+)\s+slide)\s+(\d+)$/
        );
        if (prefixedSlideMatch) {
            return {
                normalised: 'carousel_slide', level: null,
                number: parseInt(prefixedSlideMatch[1], 10),
                id: null, category: 'interactive', modifier: null, raw: raw
            };
        }

        // --- [drop image] as single tag (click-drop variant) ---
        if (/^drop\s+image$/i.test(flexCleaned)) {
            return {
                normalised: 'back', level: null, number: null,
                id: null, category: 'subtag', modifier: 'image', raw: raw
            };
        }

        return null;
    }
}
