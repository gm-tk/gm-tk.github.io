/**
 * BlockSubtagMatcher — Sub-tag normalisation for accordion tabs, flip cards,
 * carousel slides, and tab sub-tags. Owns the mutable _lastCardFrontIndex state.
 *
 * Extracted from js/block-scoper.js as part of the block-scoper refactor.
 * See docs/27-block-scoper-refactor-plan.md.
 */

'use strict';

class BlockSubtagMatcher {
    constructor(tables) {
        /** @type {BlockScoperTables} */
        this._tables = tables;

        /** @type {number|null} Last card_front index for copy-paste mismatch detection */
        this._lastCardFrontIndex = null;
    }

    /**
     * Normalise a sub-tag (ordinal accordion tab, flip card front/back, carousel slide, etc.).
     *
     * @param {string} tagText - The raw tag text
     * @param {string|null} parentBlockType - The parent block type for context
     * @param {number|null} lastIndex - The last assigned sub-element index (for auto-increment)
     * @returns {Object|null} Normalised sub-tag result or null
     */
    normaliseSubTag(tagText, parentBlockType, lastIndex) {
        if (!tagText || typeof tagText !== 'string') return null;

        var inner = tagText.replace(/^\[|\]$/g, '').trim();
        if (!inner) return null;

        var cleaned = inner.toLowerCase().trim();
        var flexCleaned = cleaned.replace(/-/g, ' ').replace(/\s+/g, ' ').trim();

        // --- Accordion tab patterns ---
        var accordionTab = this._matchAccordionTab(flexCleaned, inner, lastIndex);
        if (accordionTab) return accordionTab;

        // --- Flip card front/back patterns ---
        var flipCard = this._matchFlipCardSubTag(flexCleaned, inner, lastIndex);
        if (flipCard) return flipCard;

        // --- Carousel slide patterns ---
        var slide = this._matchCarouselSlide(flexCleaned, inner, parentBlockType, lastIndex);
        if (slide) return slide;

        // --- Tab sub-tag ---
        var tab = this._matchTabSubTag(flexCleaned, inner, lastIndex);
        if (tab) return tab;

        // --- [Inside tab] marker ---
        if (flexCleaned === 'inside tab') {
            return { subType: 'inside_tab', index: null, heading: null, headingLevel: null, isMarkerOnly: true };
        }

        // --- [New tab] / [New tab 1] ---
        if (/^new\s+tab(?:\s+\d+)?$/.test(flexCleaned)) {
            return { subType: 'tab', index: (lastIndex || 0) + 1, heading: null, headingLevel: null };
        }

        return null;
    }
    // ------------------------------------------------------------------
    // Internal: Accordion tab sub-tag matching
    // ------------------------------------------------------------------

    _matchAccordionTab(flexCleaned, originalInner, lastIndex) {
        // Ordinal accordion tabs: [First tab of accordion], [Third accordion tab]
        var ordAccMatch = flexCleaned.match(
            /^(first|second|third|forth|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+(?:tab\s+of\s+accordion|accordion\s+tab)$/
        );
        if (ordAccMatch) {
            var idx = this._tables.ordinalMap[ordAccMatch[1]];
            return { subType: 'tab', index: idx, heading: null, headingLevel: null };
        }

        // Word-numbered accordion: [accordion one], [Accordion two: Routine]
        var wordAccMatch = flexCleaned.match(
            /^accordion\s+(one|two|three|four|five|six|seven|eight|nine|ten)\s*:?\s*(.*)$/
        );
        if (wordAccMatch) {
            var wordIdx = this._tables.ordinalMap[wordAccMatch[1]];
            var subHeading = wordAccMatch[2] ? wordAccMatch[2].trim() : null;
            // Preserve original case for heading
            if (subHeading) {
                var headingStart = originalInner.toLowerCase().indexOf(wordAccMatch[2]);
                if (headingStart !== -1) {
                    subHeading = originalInner.substring(headingStart).trim();
                }
            }
            return { subType: 'tab', index: wordIdx, heading: subHeading || null, headingLevel: null };
        }

        // Numeric accordion/tab: [accordion 1], [Tab 1], [Accordion tab 1]
        var numAccMatch = flexCleaned.match(
            /^(?:accordion\s+tab|accordion|tab)\s+(\d+)\s*:?\s*(.*)$/
        );
        if (numAccMatch) {
            var numIdx = parseInt(numAccMatch[1], 10);
            var numSuffix = numAccMatch[2] ? numAccMatch[2].trim() : null;
            var numContentHint = null;
            var numHeading = null;
            if (numSuffix) {
                // Distinguish content hints from headings
                if (/^(body|content|image|video|heading|tab)$/i.test(numSuffix)) {
                    numContentHint = numSuffix.toLowerCase();
                } else {
                    // Preserve original case using position offset
                    var numSuffixPos = flexCleaned.indexOf(numAccMatch[2]);
                    if (numSuffixPos !== -1 && numSuffixPos < originalInner.length) {
                        numHeading = originalInner.substring(numSuffixPos).trim();
                    } else {
                        numHeading = numSuffix;
                    }
                }
            }
            return { subType: 'tab', index: numIdx, heading: numHeading || null,
                     headingLevel: null, contentHint: numContentHint };
        }

        // [accordion N content] / [accordion N types of laws]
        var accContentMatch = flexCleaned.match(/^accordion\s+(\d+)\s+(.+)$/);
        if (accContentMatch) {
            var accIdx = parseInt(accContentMatch[1], 10);
            var accSuffix = accContentMatch[2].trim();
            var accContentHint = null;
            var accHeading = null;
            if (/^(body|content|image|video|heading|tab)$/i.test(accSuffix)) {
                accContentHint = accSuffix.toLowerCase();
            } else {
                accHeading = accSuffix;
            }
            return { subType: 'tab', index: accIdx, heading: accHeading,
                     headingLevel: null, contentHint: accContentHint };
        }

        // [TAB N MODULE INTRODUCTION] etc.
        var tabModMatch = flexCleaned.match(/^tab\s+(\d+)\s+(.+)$/);
        if (tabModMatch) {
            var tabIdx = parseInt(tabModMatch[1], 10);
            var tabSuffix = tabModMatch[2].trim();
            var tabContentHint = null;
            var tabHeading = null;
            if (/^(body|content|image|video|heading|tab)$/i.test(tabSuffix)) {
                tabContentHint = tabSuffix.toLowerCase();
            } else {
                // Preserve original case by finding suffix position in flexCleaned
                // then using same offset in originalInner
                var suffixPos = flexCleaned.indexOf(tabModMatch[2]);
                if (suffixPos !== -1 && suffixPos < originalInner.length) {
                    tabHeading = originalInner.substring(suffixPos).trim();
                } else {
                    tabHeading = tabSuffix;
                }
            }
            return { subType: 'tab', index: tabIdx, heading: tabHeading,
                     headingLevel: null, contentHint: tabContentHint };
        }

        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Flip card sub-tag matching
    // ------------------------------------------------------------------

    _matchFlipCardSubTag(flexCleaned, originalInner, lastIndex) {
        // Ordinal flip cards: [First card, front H4 title]
        var ordFlipMatch = flexCleaned.match(
            /^(first|second|third|forth|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+card\s*,?\s*(front|back)\s*(h\d)?\s*(title)?$/
        );
        if (ordFlipMatch) {
            var idx = this._tables.ordinalMap[ordFlipMatch[1]];
            var side = ordFlipMatch[2] === 'front' ? 'card_front' : 'card_back';
            var hLevel = ordFlipMatch[3] ? ordFlipMatch[3].toUpperCase() : null;

            // Copy-paste mismatch detection for card_back:
            // If writer copy-pasted and forgot to update ordinal (e.g., "Third card, back"
            // when the preceding card_front was index 4), use the preceding front's index.
            if (side === 'card_back' && this._lastCardFrontIndex !== null &&
                this._lastCardFrontIndex !== undefined && idx !== this._lastCardFrontIndex) {
                console.warn(
                    'Card back ordinal mismatch: tag says \'' + ordFlipMatch[1] +
                    '\' (index ' + idx + ') but preceding card_front was index ' +
                    this._lastCardFrontIndex + ' — using index ' + this._lastCardFrontIndex
                );
                idx = this._lastCardFrontIndex;
            }

            // Track last card_front index for mismatch detection
            if (side === 'card_front') {
                this._lastCardFrontIndex = idx;
            }

            return { subType: side, index: idx, heading: null, headingLevel: hLevel };
        }

        // [Front], [Back], [front], [back]
        if (flexCleaned === 'front' || flexCleaned === 'front of card' ||
            flexCleaned === 'front of the flipcard' || flexCleaned === 'front of the card') {
            var frontIdx = (lastIndex || 0) + 1;
            this._lastCardFrontIndex = frontIdx;
            return { subType: 'card_front', index: frontIdx, heading: null, headingLevel: null };
        }
        if (flexCleaned === 'back' || flexCleaned === 'back of card' || flexCleaned === 'back of the card' ||
            flexCleaned === 'back of flipcard' || flexCleaned.match(/^back\s+of\s+flipcard/)) {
            return { subType: 'card_back', index: lastIndex || 1, heading: null, headingLevel: null };
        }

        // [drop] - click-drop variant of front
        if (flexCleaned === 'drop' || flexCleaned.match(/^drop\s+image/)) {
            var dropIdx = (lastIndex || 0) + 1;
            this._lastCardFrontIndex = dropIdx;
            return { subType: 'card_front', index: dropIdx, heading: null, headingLevel: null };
        }

        // [Card N] [Front] — often split into compound, but if standalone:
        var cardNMatch = flexCleaned.match(/^card\s+(\d+)$/);
        if (cardNMatch) {
            var cardIdx = parseInt(cardNMatch[1], 10);
            this._lastCardFrontIndex = cardIdx;
            return { subType: 'card_front', index: cardIdx, heading: null, headingLevel: null };
        }

        // [Flip card 1], [Flipcard 1], [flip Card 1]
        var flipN = flexCleaned.match(/^flip\s*card\s+(\d+)$/);
        if (flipN) {
            var flipIdx = parseInt(flipN[1], 10);
            this._lastCardFrontIndex = flipIdx;
            return { subType: 'card_front', index: flipIdx, heading: null, headingLevel: null };
        }

        // [front of card title & image 1] / [front of card title and image 1]
        var frontTitleMatch = flexCleaned.match(/^front\s+of\s+card\s+(?:title\s+(?:&|and)\s+image\s+)?(\d+)$/);
        if (frontTitleMatch) {
            var ftIdx = parseInt(frontTitleMatch[1], 10);
            this._lastCardFrontIndex = ftIdx;
            return { subType: 'card_front', index: ftIdx, heading: null, headingLevel: null };
        }

        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Carousel slide sub-tag matching
    // ------------------------------------------------------------------

    _matchCarouselSlide(flexCleaned, originalInner, parentBlockType, lastIndex) {
        // [Slide N], [slide N]
        var slideMatch = flexCleaned.match(/^slide\s+(\d+)\s*[-–:]?\s*(.*)$/);
        if (slideMatch) {
            var idx = parseInt(slideMatch[1], 10);
            var note = slideMatch[2] ? slideMatch[2].trim() : null;
            return { subType: 'slide', index: idx, heading: null, headingLevel: null, contentHint: note || null };
        }

        // [Carousel Image N]
        var carImgMatch = flexCleaned.match(/^carousel\s+image\s+(\d+)$/);
        if (carImgMatch) {
            return { subType: 'slide', index: parseInt(carImgMatch[1], 10), heading: null, headingLevel: null };
        }

        // [Expectations Slide N], [Needs Slide N]
        var namedSlideMatch = flexCleaned.match(/^(?:\w+)\s+slide\s+(\d+)$/);
        if (namedSlideMatch) {
            return { subType: 'slide', index: parseInt(namedSlideMatch[1], 10), heading: null, headingLevel: null };
        }

        // Bare number [1], [2] etc. — ONLY within carousel scope
        if (parentBlockType === 'carousel') {
            var bareNum = flexCleaned.match(/^(\d+)$/);
            if (bareNum) {
                return { subType: 'slide', index: parseInt(bareNum[1], 10), heading: null, headingLevel: null };
            }
        }

        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Tab sub-tag matching
    // ------------------------------------------------------------------

    _matchTabSubTag(flexCleaned, originalInner, lastIndex) {
        // [Tab N]
        var tabMatch = flexCleaned.match(/^tab\s+(\d+)\s*:?\s*(.*)$/);
        if (tabMatch) {
            var heading = tabMatch[2] ? tabMatch[2].trim() : null;
            return { subType: 'tab', index: parseInt(tabMatch[1], 10), heading: heading, headingLevel: null };
        }

        return null;
    }
}
