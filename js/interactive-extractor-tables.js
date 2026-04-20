/**
 * InteractiveExtractorTables — pure data tables used by the interactive extractor.
 *
 * Holds tier membership, pattern names, type→pattern mapping, sub-tag type list,
 * and wide-column types. No behaviour.
 *
 * Extracted from js/interactive-extractor.js as part of the interactive-extractor
 * refactor. See docs/28-interactive-extractor-refactor-plan.md.
 */

'use strict';

class InteractiveExtractorTables {
    constructor() {
        /**
         * Tier 1 — PageForge renders full HTML (Phase 7).
         * Simple, static HTML structures with no complex JS logic.
         */
        this.TIER_1_TYPES = ['accordion', 'flip_card', 'speech_bubble', 'tabs'];

        /**
         * Data pattern names keyed by pattern number.
         */
        this.patternNames = {
            1: 'Single Data Table',
            2: 'Front/Back Table Rows',
            3: 'Hint/Slide Table',
            4: 'Numbered Items (Paragraph)',
            5: 'Numbered Slides',
            6: 'Numbered Shapes/Tabs',
            7: 'Numbered Accordions',
            8: 'Speech Bubble in Table Row',
            9: 'Conversation Layout',
            10: 'Word Select Table',
            11: 'Axis Labels',
            12: 'Info Trigger Image',
            13: 'Self-Assessment/Survey Table'
        };

        /**
         * Map interactive types to their most common data patterns.
         */
        this.typeToPrimaryPattern = {
            'drag_and_drop': 1,
            'dropdown': 1,
            'dropdown_quiz_paragraph': 4,
            'flip_card': 2,
            'accordion': 7,
            'click_drop': 2,
            'carousel': 5,
            'rotating_banner': 5,
            'tabs': 6,
            'speech_bubble': 8,
            'hint_slider': 3,
            'shape_hover': 6,
            'reorder': 1,
            'slider_chart': 11,
            'memory_game': 1,
            'word_drag': 1,
            'typing_quiz': 1,
            'self_check': 1,
            'word_select': 10,
            'word_highlighter': 10,
            'mcq': 1,
            'multichoice_quiz_survey': 13,
            'radio_quiz': 1,
            'checklist': 1,
            'info_trigger': 1,
            'info_trigger_image': 12,
            'audio_trigger': 1,
            'venn_diagram': 1,
            'timeline': 1,
            'self_reflection': 1,
            'reflection_slider': 1,
            'stop_watch': 1,
            'number_line': 1,
            'crossword': 1,
            'word_find': 1,
            'bingo': 1,
            'clicking_order': 1,
            'puzzle': 1,
            'sketcher': 1,
            'glossary': 1,
            'embed_pdf': 1,
            'embed_padlet': 1,
            'embed_desmos': 1,
            'slider': 1,
            'translate_section': 1,
            'kanji_cards': 1
        };

        /**
         * Interactive types that are sub-tags — these mark data within an
         * interactive, not standalone interactives themselves.
         */
        this.subTagTypes = [
            'carousel_slide', 'tab', 'shape', 'hint',
            'end_accordions'
        ];

        /**
         * Interactive types that use wide column class.
         */
        this.wideColTypes = ['drag_and_drop', 'info_trigger_image'];
    }
}
