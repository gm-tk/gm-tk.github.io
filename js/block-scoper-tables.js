/**
 * BlockScoperTables — Static lookup tables used by BlockScoper and its helpers.
 *
 * Fields:
 *  - ordinalMap: ordinal/number word → integer
 *  - blockTypeKeywords: first significant keyword → canonical blockType
 *  - closerTypeMap: closing-tag keyword → canonical blockType
 *  - hardBoundaryTags: normalised tag names that terminate all open blocks
 *  - blockOpenPrefixStrip: prefix words stripped before keyword matching
 *
 * Extracted from js/block-scoper.js as part of the block-scoper refactor.
 * See docs/27-block-scoper-refactor-plan.md.
 */

'use strict';

class BlockScoperTables {
    constructor() {
        // Ordinal word → number lookup map
        this.ordinalMap = {
            'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'forth': 4,
            'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10,
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        };

        // Keywords that signal block-opening tags (after stripping prefix words)
        this.blockOpenPrefixStrip = ['insert', 'interactive', 'tool', 'activity', 'visual', 'add'];

        // Block type mapping: first significant word → blockType
        this.blockTypeKeywords = {
            'accordion': 'accordion',
            'accordian': 'accordion',  // misspelling
            'accordions': 'accordion',
            'carousel': 'carousel',
            'slideshow': 'carousel',
            'slide show': 'carousel',
            'rotating banner': 'carousel',
            'flip': 'flipcards',
            'flipcard': 'flipcards',
            'flipcards': 'flipcards',
            'click drop': 'clickdrop',
            'clickdrop': 'clickdrop',
            'drop click': 'clickdrop',
            'drag': 'dragdrop',
            'alert': 'alert',
            'box': 'alert',
            'important': 'alert',
            'thought bubble': 'alert',
            'supervisor': 'alert',
            'coloured box': 'alert',
            'tabs': 'tabs',
            'tab nav': 'tabs',
            'tab layout': 'tabs',
            'tab organisation': 'tabs',
            'side tabs': 'tabs',
            'modal': 'modal',
            'activity': 'activity',
            'activities': 'activity'
        };

        // Closing tag keywords mapping
        this.closerTypeMap = {
            'accordion': 'accordion',
            'accordions': 'accordion',
            'accordian': 'accordion',
            'carousel': 'carousel',
            'slideshow': 'carousel',
            'slide show': 'carousel',
            'flipcards': 'flipcards',
            'flip cards': 'flipcards',
            'flip card': 'flipcards',
            'click drop': 'clickdrop',
            'clickdrop': 'clickdrop',
            'click drops': 'clickdrop',
            'drag and drop': 'dragdrop',
            'alert': 'alert',
            'alert box': 'alert',
            'important box': 'alert',
            'box': 'alert',
            'box out to right': 'alert',
            'box out to the right': 'alert',
            'coloured box': 'alert',
            'purple coloured box': 'alert',
            'tab': 'tabs',
            'tabs': 'tabs',
            'modal': 'modal',
            'modals': 'modal',
            'activity': 'activity',
            'interactive': '_generic',
            'interactive activity': '_generic',
            'interactive tool': '_generic',
            'quiz': '_generic',
            'quizzes in tabs': '_generic'
        };

        // Hard boundary normalised tag names
        this.hardBoundaryTags = [
            'end_page', 'lesson', 'lesson_overview'
        ];
    }
}
