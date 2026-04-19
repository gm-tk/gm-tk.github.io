/**
 * InteractiveTagMatcher — Interactive-category pattern dispatcher.
 *
 * Extracted from `TagNormaliser._normalise()` (Session 1 of the tag-pipeline
 * audit series). Owns the long regex ladder that classifies interactive
 * components: drag_and_drop, dropdown, flip_card, accordion, click_drop,
 * carousel, rotating_banner, carousel_slide, tabs, tab, speech_bubble,
 * hint_slider, hint, shape_hover, shape, info_trigger, info_trigger_image,
 * audio_trigger, multichoice_quiz_survey, mcq.
 *
 * Called from `TagNormaliser._normalise()` after the heading/structural/
 * lesson/activity branches, and before the image/table/button branches.
 * Dispatch order within this matcher is significant — for example
 * `info_trigger_image` must match before `info_trigger`.
 *
 * @see CLAUDE.md Section 10 — Tag Taxonomy & Normalisation
 * @see docs/16-engs301-fixes.md (hovertrigger, flipcard/hintslider one-word,
 *      multichoice dropdown quiz — ENGS301 additions)
 */

'use strict';

class InteractiveTagMatcher {
    /**
     * Match any interactive-category tag pattern.
     *
     * @param {string} flexCleaned - Lowercased, hyphen-normalised tag text
     * @param {string} inner - Original inner tag text (preserves case)
     * @param {string} raw - Full raw tag with brackets
     * @returns {Object|null} Normalised tag object or null if no pattern matched
     */
    match(flexCleaned, inner, raw) {
        var modifier = null;

        // --- Drag and drop (with modifiers) ---
        var dndMatch = flexCleaned.match(/^drag\s+and\s+drop\s*(.*)$/);
        if (dndMatch) {
            modifier = dndMatch[1] ? dndMatch[1].replace(/\s+/g, '_').trim() : null;
            if (modifier === '') modifier = null;
            return {
                normalised: 'drag_and_drop',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: modifier,
                raw: raw
            };
        }

        // --- Dropdown quiz paragraph / dropquiz variants ---
        if (flexCleaned === 'dropdown quiz paragraph' ||
            flexCleaned === 'drop down quiz paragraph' ||
            flexCleaned === 'drop down paragraph quiz' ||
            flexCleaned === 'dropquiz' ||
            flexCleaned === 'multi choice dropdown quiz paragraph' ||
            flexCleaned === 'multichoice dropdown quiz paragraph') {
            return {
                normalised: 'dropdown_quiz_paragraph',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Dropdown / drop down with optional number ---
        var dropdownMatch = flexCleaned.match(/^drop\s*down\s*(\d+)?$/);
        if (dropdownMatch) {
            return {
                normalised: 'dropdown',
                level: null,
                number: dropdownMatch[1] ? parseInt(dropdownMatch[1], 10) : null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Flip card variants (flipcard, flip card, flip cards) ---
        // Note: "flipcard N" (single word + number) is a sub-tag reference to a numbered card,
        // so the standalone "flipcard" match must either have a space or no trailing number.
        var flipCardMatch = flexCleaned.match(/^flip\s+cards?(?:\s+(\d+))?(?:\s+image)?$/) ||
            (flexCleaned === 'flipcard' || flexCleaned === 'flipcards' ||
             flexCleaned === 'flipcard image' || flexCleaned === 'flipcards image'
                ? [flexCleaned] : null);
        if (flipCardMatch) {
            modifier = flexCleaned.indexOf('image') !== -1 ? 'image' : null;
            return {
                normalised: 'flip_card',
                level: null,
                number: flipCardMatch[1] ? parseInt(flipCardMatch[1], 10) : null,
                id: null,
                category: 'interactive',
                modifier: modifier,
                raw: raw
            };
        }

        // --- End accordions ---
        if (flexCleaned === 'end accordions') {
            return {
                normalised: 'end_accordions',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Accordion with optional number ---
        var accordionMatch = flexCleaned.match(/^accordion\s*(\d+)?$/);
        if (accordionMatch) {
            return {
                normalised: 'accordion',
                level: null,
                number: accordionMatch[1] ? parseInt(accordionMatch[1], 10) : null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Click drop / clickdrop / drop click with optional number ---
        var clickDropMatch = flexCleaned.match(/^(?:click\s*drop|drop\s*click|clickdrop)\s*(\d+)?$/);
        if (clickDropMatch) {
            return {
                normalised: 'click_drop',
                level: null,
                number: clickDropMatch[1] ? parseInt(clickDropMatch[1], 10) : null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Carousel / slide show / slideshow ---
        if (flexCleaned === 'carousel' || flexCleaned === 'slide show' || flexCleaned === 'slideshow') {
            return {
                normalised: 'carousel',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Rotating banner ---
        if (flexCleaned === 'rotating banner') {
            return {
                normalised: 'rotating_banner',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Slide N ---
        var slideMatch = flexCleaned.match(/^slide\s+(\d+)$/);
        if (slideMatch) {
            return {
                normalised: 'carousel_slide',
                level: null,
                number: parseInt(slideMatch[1], 10),
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Tabs ---
        if (flexCleaned === 'tabs') {
            return {
                normalised: 'tabs',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Tab N ---
        var tabMatch = flexCleaned.match(/^tab\s+(\d+)$/);
        if (tabMatch) {
            return {
                normalised: 'tab',
                level: null,
                number: parseInt(tabMatch[1], 10),
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Speech bubble + suffix ---
        var speechMatch = flexCleaned.match(/^speech\s+bubble\s*(.*)$/);
        if (speechMatch) {
            modifier = speechMatch[1] ? speechMatch[1].replace(/\s+/g, '_').trim() : null;
            if (modifier === '') modifier = null;
            return {
                normalised: 'speech_bubble',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: modifier,
                raw: raw
            };
        }

        // --- Hint slider / hintslider with optional number ---
        var hintSliderMatch = flexCleaned.match(/^hint\s*slider\s*(\d+)?$/);
        if (hintSliderMatch) {
            return {
                normalised: 'hint_slider',
                level: null,
                number: hintSliderMatch[1] ? parseInt(hintSliderMatch[1], 10) : null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Hint (standalone) ---
        if (flexCleaned === 'hint') {
            return {
                normalised: 'hint',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Shape hover (with optional "with image") ---
        if (flexCleaned === 'shape hover' || flexCleaned === 'shape hover with image') {
            modifier = flexCleaned === 'shape hover with image' ? 'with_image' : null;
            return {
                normalised: 'shape_hover',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: modifier,
                raw: raw
            };
        }

        // --- Shape N ---
        var shapeMatch = flexCleaned.match(/^shape\s+(\d+)$/);
        if (shapeMatch) {
            return {
                normalised: 'shape',
                level: null,
                number: parseInt(shapeMatch[1], 10),
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Hovertrigger / hover trigger → info_trigger ---
        var hovertriggerMatch = flexCleaned.match(/^hover\s*trigger(?:\s*:\s*(.*))?$/);
        if (hovertriggerMatch) {
            modifier = hovertriggerMatch[1] ? hovertriggerMatch[1].trim() : null;
            return {
                normalised: 'info_trigger',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: modifier,
                raw: raw
            };
        }

        // --- Info trigger image (special case — must come before info trigger) ---
        if (flexCleaned === 'info trigger image' ||
            flexCleaned === 'infotrigger image' ||
            flexCleaned === 'info trigger] image' ||
            flexCleaned === 'info trigger] [image') {
            return {
                normalised: 'info_trigger_image',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Info audio trigger / audio trigger ---
        if (flexCleaned === 'info audio trigger' ||
            flexCleaned === 'audio trigger' ||
            flexCleaned === 'audio triggers') {
            return {
                normalised: 'audio_trigger',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Info trigger (NOT followed by "image") ---
        var infoTriggerMatch = flexCleaned.match(/^info\s*trigger(?:\s+(.+))?$/);
        if (infoTriggerMatch) {
            var suffix = infoTriggerMatch[1] || '';
            if (suffix && suffix.trim().toLowerCase() === 'image') {
                return {
                    normalised: 'info_trigger_image',
                    level: null,
                    number: null,
                    id: null,
                    category: 'interactive',
                    modifier: null,
                    raw: raw
                };
            }
            modifier = suffix ? suffix.replace(/\s+/g, '_').trim() : null;
            if (modifier === '') modifier = null;
            return {
                normalised: 'info_trigger',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: modifier,
                raw: raw
            };
        }

        // --- Multi choice quiz survey / multichoice quiz survey ---
        if (flexCleaned === 'multi choice quiz survey' ||
            flexCleaned === 'multichoice quiz survey') {
            return {
                normalised: 'multichoice_quiz_survey',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        // --- Multichoice dropdown quiz → mcq (dropdown variant) ---
        if (flexCleaned === 'multichoice dropdown quiz' ||
            flexCleaned === 'multi choice dropdown quiz' ||
            flexCleaned === 'dropdown quiz') {
            return {
                normalised: 'mcq',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: 'dropdown',
                raw: raw
            };
        }

        // --- MCQ / multi choice quiz / multichoice quiz / multi choice ---
        if (flexCleaned === 'mcq' ||
            flexCleaned === 'multi choice quiz' ||
            flexCleaned === 'multichoice quiz' ||
            flexCleaned === 'multi choice') {
            return {
                normalised: 'mcq',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: null,
                raw: raw
            };
        }

        return null;
    }
}
