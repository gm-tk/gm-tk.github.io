/**
 * OrdinalResolver — Ordinal/cardinal word → number resolution.
 *
 * Extracted from `TagNormaliser` (Session 1 of the tag-pipeline audit series).
 * Handles three input classes:
 *   1. Word ordinals/cardinals ("first", "forth", "one", "two", ..., "tenth")
 *   2. Numeric strings with ordinal suffixes ("1st", "2nd", "3rd", "4th")
 *   3. Plain numeric strings ("5", "10", "21")
 *
 * @see CLAUDE.md Section 10 — Tag Taxonomy & Normalisation
 * @see docs/18-tag-normalisation-patch.md (ordinal suffix stripping — Phase 1 Patch)
 */

'use strict';

class OrdinalResolver {
    constructor() {
        this._ordinalMap = {
            'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'forth': 4,
            'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10,
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        };
    }

    /**
     * Resolve an ordinal word, cardinal word, or numeric string to its number.
     *
     * @param {string} word - e.g. "first", "Forth", "one", "10"
     * @returns {number|null} The numeric value, or null if unrecognised
     */
    resolveOrdinalOrNumber(word) {
        if (!word) return null;
        var lower = word.toLowerCase().trim();
        // Direct lookup in ordinal/cardinal map
        if (this._ordinalMap.hasOwnProperty(lower)) return this._ordinalMap[lower];
        // Strip trailing ordinal suffixes (1st, 2nd, 3rd, 4th, etc.)
        var stripped = lower.replace(/(st|nd|rd|th)$/, '');
        if (stripped !== lower) {
            var suffixParsed = parseInt(stripped, 10);
            if (!isNaN(suffixParsed)) return suffixParsed;
        }
        // Plain numeric string
        var parsed = parseInt(lower, 10);
        return isNaN(parsed) ? null : parsed;
    }
}
