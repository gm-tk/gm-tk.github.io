/**
 * TagNormaliserTables — Static lookup data for tag normalisation.
 *
 * Extracted from `TagNormaliser` (Session 1 of the tag-pipeline audit series).
 * Owns the six read-only data structures the normaliser and boundary-detector
 * consult at runtime:
 *
 *   - simpleTable            — 1:1 flexCleaned → {normalised, category}
 *   - categoryMap            — array used by `getCategory()` lookups
 *   - interactiveTags        — full list of category:'interactive' tag names
 *   - interactiveNonStartTags — interactive tags that are sub-tags / end-markers
 *   - interactiveChildTagsMap — valid child sub-tags per interactive-start tag
 *   - interactiveEndSignalTags — tags that always close an interactive boundary
 *
 * @see CLAUDE.md Section 10 — Tag Taxonomy & Normalisation
 */

'use strict';

class TagNormaliserTables {
    constructor() {
        // Simple 1:1 mappings (flexCleaned → {normalised, category})
        this.simpleTable = {
            // Page Structure (structural)
            'title bar': { normalised: 'title_bar', category: 'structural' },
            'module introduction': { normalised: 'module_introduction', category: 'structural' },
            'lesson overview': { normalised: 'lesson_overview', category: 'structural' },
            'lesson content': { normalised: 'lesson_content', category: 'structural' },
            'end page': { normalised: 'end_page', category: 'structural' },

            // Body (body)
            'body': { normalised: 'body', category: 'body' },
            'body text': { normalised: 'body', category: 'body' },

            // Content Styling (styling)
            'alert': { normalised: 'alert', category: 'styling' },
            'important': { normalised: 'important', category: 'styling' },
            'alert wananga': { normalised: 'alert_cultural_wananga', category: 'styling' },
            'alert talanoa': { normalised: 'alert_cultural_talanoa', category: 'styling' },
            'alert combined': { normalised: 'alert_cultural_combined', category: 'styling' },
            'whakatauki': { normalised: 'whakatauki', category: 'styling' },
            'quote': { normalised: 'quote', category: 'styling' },
            'rhetorical question': { normalised: 'rhetorical_question', category: 'styling' },
            'full page translate': { normalised: 'reo_translate', category: 'styling' },
            'reo translate': { normalised: 'reo_translate', category: 'styling' },

            // Media (media)
            'image': { normalised: 'image', category: 'media' },
            'video': { normalised: 'video', category: 'media' },
            'audio': { normalised: 'audio', category: 'media' },
            'audio image': { normalised: 'audio_image', category: 'media' },
            'audioimage': { normalised: 'audio_image', category: 'media' },
            'image zoom': { normalised: 'image_zoom', category: 'media' },
            'image label': { normalised: 'image_label', category: 'media' },

            // Activity (activity)
            'end activity': { normalised: 'end_activity', category: 'activity' },
            'end of activity': { normalised: 'end_activity', category: 'activity' },

            // Link/Button (link)
            'button': { normalised: 'button', category: 'link' },
            'external link button': { normalised: 'external_link_button', category: 'link' },
            'external link': { normalised: 'external_link', category: 'link' },
            'go to journal': { normalised: 'go_to_journal', category: 'link' },
            'download journal': { normalised: 'download_journal', category: 'link' },
            'upload to dropbox': { normalised: 'upload_to_dropbox', category: 'interactive' },
            'engagement quiz button': { normalised: 'engagement_quiz_button', category: 'link' },
            'supervisor button': { normalised: 'supervisor_button', category: 'link' },
            'modal button': { normalised: 'modal_button', category: 'link' },
            'audio button': { normalised: 'audio_button', category: 'link' },

            // Interactive (interactive)
            'reorder': { normalised: 'reorder', category: 'interactive' },
            'slider chart': { normalised: 'slider_chart', category: 'interactive' },
            'slider': { normalised: 'slider', category: 'interactive' },
            'memory game': { normalised: 'memory_game', category: 'interactive' },
            'word drag': { normalised: 'word_drag', category: 'interactive' },
            'typing self check': { normalised: 'typing_quiz', category: 'interactive' },
            'typing quiz': { normalised: 'typing_quiz', category: 'interactive' },
            'self check': { normalised: 'self_check', category: 'interactive' },
            'word highlighter': { normalised: 'word_highlighter', category: 'interactive' },
            'word select': { normalised: 'word_select', category: 'interactive' },
            'radio quiz': { normalised: 'radio_quiz', category: 'interactive' },
            'true false': { normalised: 'radio_quiz', category: 'interactive' },
            'checklist': { normalised: 'checklist', category: 'interactive' },
            'venn diagram': { normalised: 'venn_diagram', category: 'interactive' },
            'timeline': { normalised: 'timeline', category: 'interactive' },
            'self reflection': { normalised: 'self_reflection', category: 'interactive' },
            'reflection slider': { normalised: 'reflection_slider', category: 'interactive' },
            'stop watch': { normalised: 'stop_watch', category: 'interactive' },
            'stopwatch': { normalised: 'stop_watch', category: 'interactive' },
            'number line': { normalised: 'number_line', category: 'interactive' },
            'crossword': { normalised: 'crossword', category: 'interactive' },
            'word find': { normalised: 'word_find', category: 'interactive' },
            'wordfind': { normalised: 'word_find', category: 'interactive' },
            'bingo': { normalised: 'bingo', category: 'interactive' },
            'clicking order': { normalised: 'clicking_order', category: 'interactive' },
            'puzzle': { normalised: 'puzzle', category: 'interactive' },
            'sketcher': { normalised: 'sketcher', category: 'interactive' },
            'glossary': { normalised: 'glossary', category: 'interactive' },
            'translate': { normalised: 'translate_section', category: 'interactive' },
            'translate section': { normalised: 'translate_section', category: 'interactive' },
            'kanji cards': { normalised: 'kanji_cards', category: 'interactive' },
            'language letter': { normalised: 'kanji_cards', category: 'interactive' },
            'embed pdf': { normalised: 'embed_pdf', category: 'interactive' },
            'embed padlet': { normalised: 'embed_padlet', category: 'interactive' },
            'embed desmos': { normalised: 'embed_desmos', category: 'interactive' },
            'desmos graph': { normalised: 'embed_desmos', category: 'interactive' },

            // Structural Sub-tags (subtag)
            'front': { normalised: 'front', category: 'subtag' },
            'back': { normalised: 'back', category: 'subtag' },
            'drop': { normalised: 'back', category: 'subtag' },
            'static heading': { normalised: 'static_heading', category: 'subtag' },
            'story heading': { normalised: 'story_heading', category: 'subtag' },
            'static column': { normalised: 'static_column', category: 'subtag' },
            'unsorted list': { normalised: 'unordered_list', category: 'subtag' },
            'unordered list': { normalised: 'unordered_list', category: 'subtag' }
        };

        // Category map for getCategory() lookups
        this.categoryMap = [
            {
                category: 'structural',
                tags: ['title_bar', 'module_introduction', 'lesson', 'lesson_overview', 'lesson_content', 'end_page']
            },
            {
                category: 'heading',
                tags: ['heading']
            },
            {
                category: 'body',
                tags: ['body']
            },
            {
                category: 'styling',
                tags: ['alert', 'important', 'alert_cultural_wananga', 'alert_cultural_talanoa',
                       'alert_cultural_combined', 'whakatauki', 'quote', 'rhetorical_question', 'reo_translate']
            },
            {
                category: 'media',
                tags: ['image', 'video', 'audio', 'audio_image', 'image_zoom', 'image_label']
            },
            {
                category: 'activity',
                tags: ['activity', 'activity_heading', 'end_activity']
            },
            {
                category: 'link',
                tags: ['button', 'external_link_button', 'external_link', 'engagement_quiz_button',
                       'supervisor_button', 'modal_button', 'audio_button', 'go_to_journal']
            },
            {
                category: 'subtag',
                tags: ['front', 'back', 'static_heading', 'story_heading', 'static_column',
                       'unordered_list', 'table', 'accordion_tab', 'card_front', 'card_back',
                       'inside_tab', 'new_tab']
            }
        ];

        // All interactive tag names for category lookup
        this.interactiveTags = [
            'drag_and_drop', 'dropdown', 'dropdown_quiz_paragraph', 'flip_card',
            'accordion', 'end_accordions', 'click_drop', 'carousel', 'rotating_banner',
            'carousel_slide', 'tabs', 'tab', 'speech_bubble', 'hint_slider', 'hint',
            'shape_hover', 'shape', 'reorder', 'slider_chart', 'slider', 'memory_game',
            'word_drag', 'typing_quiz', 'self_check', 'word_select', 'word_highlighter',
            'mcq', 'multichoice_quiz_survey', 'radio_quiz', 'checklist',
            'info_trigger', 'info_trigger_image', 'audio_trigger',
            'venn_diagram', 'timeline', 'self_reflection', 'reflection_slider',
            'stop_watch', 'number_line', 'crossword', 'word_find', 'bingo',
            'clicking_order', 'puzzle', 'sketcher', 'glossary', 'translate_section',
            'kanji_cards', 'embed_pdf', 'embed_padlet', 'embed_desmos',
            'upload_to_dropbox'
        ];

        // Interactive tags that are NOT start-of-interactive (they are sub-tags
        // or the close marker of an accordion group). Everything else listed in
        // `interactiveTags` is treated as an interactive-start tag.
        this.interactiveNonStartTags = [
            'carousel_slide', 'tab', 'shape', 'hint', 'end_accordions'
        ];

        // Child sub-tags that are structurally contained within a given
        // interactive-start tag. Used by the boundary-detection algorithm
        // (Session F, `js/interactive-extractor.js`) to decide whether a
        // following block belongs inside the current interactive boundary.
        // Values are normalised tag names. Interactive-start tags not listed
        // here default to an empty array.
        this.interactiveChildTagsMap = {
            flip_card: ['front', 'back'],
            click_drop: ['front', 'back'],
            carousel: ['carousel_slide', 'tab', 'image'],
            rotating_banner: ['carousel_slide', 'tab', 'image'],
            slide_show: ['carousel_slide', 'tab', 'image'],
            accordion: ['tab', 'carousel_slide'],
            tabs: ['tab', 'carousel_slide'],
            hint_slider: ['hint', 'carousel_slide'],
            speech_bubble: []
        };

        // Normalised tags which, when encountered after an interactive-start,
        // always close the current interactive boundary. Used by
        // `isInteractiveEndSignal()`.
        this.interactiveEndSignalTags = [
            'body', 'end_page', 'end_activity', 'lesson',
            'alert', 'alert_cultural_wananga', 'alert_cultural_talanoa',
            'alert_cultural_combined',
            'important', 'whakatauki', 'quote'
        ];
    }
}
