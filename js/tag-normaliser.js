/**
 * TagNormaliser — Tag taxonomy and normalisation engine for ParseMaster.
 *
 * Processes raw content block text to extract square-bracket tags,
 * red text markers, and writer instructions. Maps all tag variants
 * to canonical normalised forms with category classification.
 *
 * @see CLAUDE.md Section 10 — Tag Taxonomy & Normalisation
 */

'use strict';

class TagNormaliser {
    constructor() {
        /**
         * Red text marker pattern.
         * Matches: 🔴[RED TEXT] ... [/RED TEXT]🔴
         */
        this._redTextPattern = /\uD83D\uDD34\[RED TEXT\]\s*([\s\S]*?)\s*\[\/RED TEXT\]\uD83D\uDD34/g;

        /**
         * Square bracket tag pattern.
         * Matches: [anything inside brackets]
         */
        this._tagPattern = /\[([^\]]+)\]/g;

        this._buildNormalisationTable();
    }

    // ------------------------------------------------------------------
    // Public API
    // ------------------------------------------------------------------

    /**
     * Process a single content block's text, returning extracted tags,
     * clean text, and red text instructions.
     *
     * @param {string} textContent - The raw text content of a block
     * @returns {Object} Processed result with tags, cleanText, redTextInstructions, flags
     */
    processBlock(textContent) {
        if (!textContent || typeof textContent !== 'string') {
            return {
                tags: [],
                cleanText: '',
                redTextInstructions: [],
                isRedTextOnly: false,
                isWhitespaceOnly: true
            };
        }

        var tags = [];
        var redTextInstructions = [];
        var remainingText = textContent;
        var hasNonRedContent = false;

        // Step 1: Extract all red text regions
        var redRegions = this._extractRedTextRegions(textContent);

        // Step 2: Process each red text region for tags and instructions
        for (var i = 0; i < redRegions.length; i++) {
            var region = redRegions[i];
            var innerContent = region.content;

            // Check if whitespace-only red text
            if (!innerContent || innerContent.trim() === '') {
                continue;
            }

            // Look for square bracket tags within this red text region
            var regionTags = this._extractTagsFromText(innerContent);

            if (regionTags.length > 0) {
                // Add all found tags
                for (var t = 0; t < regionTags.length; t++) {
                    tags.push(regionTags[t]);
                }

                // Check for instruction text after removing tags
                var instructionText = innerContent;
                // Remove all tag occurrences
                instructionText = instructionText.replace(this._tagPattern, '').trim();
                if (instructionText.length > 0) {
                    redTextInstructions.push(instructionText);
                }
            } else {
                // Pure instruction — no square bracket tags
                redTextInstructions.push(innerContent.trim());
            }
        }

        // Step 3: Build text without red text markers
        var textWithoutRed = textContent.replace(this._redTextPattern, '');

        // Step 4: Check for tags in the non-red text portion
        var nonRedTags = this._extractTagsFromText(textWithoutRed);
        for (var j = 0; j < nonRedTags.length; j++) {
            tags.push(nonRedTags[j]);
        }

        // Step 5: Build clean text — remove all red text markers AND all square bracket tags
        var cleanText = textContent;
        // Remove red text regions entirely
        cleanText = cleanText.replace(this._redTextPattern, '');
        // Remove square bracket tags
        cleanText = cleanText.replace(this._tagPattern, '');
        // Collapse multiple spaces to single
        cleanText = cleanText.replace(/  +/g, ' ').trim();

        // Step 6: Determine flags
        hasNonRedContent = textWithoutRed.replace(this._tagPattern, '').trim().length > 0;

        var hasRedContent = redRegions.length > 0;
        var allRedContentEmpty = redRegions.length > 0 &&
            redRegions.every(function (r) { return !r.content || r.content.trim() === ''; });

        var isWhitespaceOnly = cleanText === '' && tags.length === 0 &&
            redTextInstructions.length === 0;

        // If all red text regions were whitespace, it's whitespace-only
        if (hasRedContent && allRedContentEmpty && !hasNonRedContent) {
            isWhitespaceOnly = true;
        }

        var isRedTextOnly = hasRedContent && !hasNonRedContent && !isWhitespaceOnly;

        // Post-process: handle info trigger image special case
        tags = this._handleInfoTriggerImageMerge(tags);

        return {
            tags: tags,
            cleanText: cleanText,
            redTextInstructions: redTextInstructions,
            isRedTextOnly: isRedTextOnly,
            isWhitespaceOnly: isWhitespaceOnly
        };
    }

    /**
     * Normalise a single tag string (without red text wrapping).
     *
     * @param {string} tagText - Tag text with or without brackets, e.g. "[H2]" or "drag and drop column"
     * @returns {Object} Normalised tag result
     */
    normaliseTag(tagText) {
        if (!tagText || typeof tagText !== 'string') {
            return null;
        }

        // Strip brackets if present
        var inner = tagText.replace(/^\[|\]$/g, '').trim();
        if (!inner) {
            return null;
        }

        var raw = tagText.indexOf('[') === 0 ? tagText : '[' + inner + ']';

        return this._normalise(inner, raw);
    }

    /**
     * Classify what category a normalised tag belongs to.
     *
     * @param {string} normalisedName - The normalised tag name
     * @returns {string|null} Category name or null if not found
     */
    getCategory(normalisedName) {
        if (!normalisedName) return null;

        for (var i = 0; i < this._categoryMap.length; i++) {
            var entry = this._categoryMap[i];
            if (entry.tags.indexOf(normalisedName) !== -1) {
                return entry.category;
            }
        }

        // Check interactive — large set
        if (this._interactiveTags.indexOf(normalisedName) !== -1) {
            return 'interactive';
        }

        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Red text extraction
    // ------------------------------------------------------------------

    /**
     * Extract all red text regions from input text.
     *
     * @param {string} text - Raw text content
     * @returns {Array<{content: string, start: number, end: number}>}
     */
    _extractRedTextRegions(text) {
        var regions = [];
        var regex = new RegExp(this._redTextPattern.source, 'g');
        var match;

        while ((match = regex.exec(text)) !== null) {
            regions.push({
                content: match[1],
                start: match.index,
                end: match.index + match[0].length,
                fullMatch: match[0]
            });
        }

        return regions;
    }

    // ------------------------------------------------------------------
    // Internal: Tag extraction from text
    // ------------------------------------------------------------------

    /**
     * Extract and normalise all square bracket tags from a text string.
     *
     * @param {string} text - Text potentially containing [tags]
     * @returns {Array<Object>} Array of normalised tag objects
     */
    _extractTagsFromText(text) {
        var tags = [];
        var regex = new RegExp(this._tagPattern.source, 'g');
        var match;

        while ((match = regex.exec(text)) !== null) {
            var inner = match[1].trim();
            if (!inner) continue;

            // Skip RED TEXT / /RED TEXT markers themselves
            if (inner === 'RED TEXT' || inner === '/RED TEXT') continue;

            var raw = match[0];
            var normalised = this._normalise(inner, raw);

            if (normalised) {
                tags.push(normalised);
            }
        }

        return tags;
    }

    // ------------------------------------------------------------------
    // Internal: Normalisation engine
    // ------------------------------------------------------------------

    /**
     * Core normalisation: takes inner tag content and returns a normalised object.
     *
     * @param {string} inner - Tag content without brackets
     * @param {string} raw - Original tag text with brackets
     * @returns {Object} Normalised tag object
     */
    _normalise(inner, raw) {
        var normalised = null;
        var level = null;
        var number = null;
        var id = null;
        var category = null;
        var modifier = null;

        // Lowercase and clean for matching
        var cleaned = inner.toLowerCase().trim();
        // Normalise hyphens to spaces for flexible matching
        var flexCleaned = cleaned.replace(/-/g, ' ').replace(/\s+/g, ' ').trim();

        // --- Heading tags: h1-h5 ---
        var headingMatch = flexCleaned.match(/^h\s*([1-5])$/);
        if (headingMatch) {
            return {
                normalised: 'heading',
                level: parseInt(headingMatch[1], 10),
                number: null,
                id: null,
                category: 'heading',
                modifier: null,
                raw: raw
            };
        }

        // --- Lesson with number ---
        var lessonMatch = flexCleaned.match(/^lesson\s+(\d+)$/);
        if (lessonMatch) {
            return {
                normalised: 'lesson',
                level: null,
                number: parseInt(lessonMatch[1], 10),
                id: null,
                category: 'structural',
                modifier: null,
                raw: raw
            };
        }

        // --- Lesson (no number) ---
        if (flexCleaned === 'lesson') {
            return {
                normalised: 'lesson',
                level: null,
                number: null,
                id: null,
                category: 'structural',
                modifier: null,
                raw: raw
            };
        }

        // --- Activity with ID ---
        var activityMatch = flexCleaned.match(/^activity\s+(\d+[a-z]?)$/i);
        if (activityMatch) {
            return {
                normalised: 'activity',
                level: null,
                number: null,
                id: activityMatch[1].toUpperCase(),
                category: 'activity',
                modifier: null,
                raw: raw
            };
        }

        // --- Activity heading / activity title ---
        if (flexCleaned === 'activity heading' || flexCleaned === 'activity title') {
            return {
                normalised: 'activity_heading',
                level: null,
                number: null,
                id: null,
                category: 'activity',
                modifier: null,
                raw: raw
            };
        }

        // --- Activity (no ID) ---
        if (flexCleaned === 'activity') {
            return {
                normalised: 'activity',
                level: null,
                number: null,
                id: null,
                category: 'activity',
                modifier: null,
                raw: raw
            };
        }

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
            flexCleaned === 'multi choice dropdown quiz paragraph') {
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

        // --- Flip card variants ---
        var flipCardMatch = flexCleaned.match(/^flip\s+cards?(?:\s+(\d+))?(?:\s+image)?$/);
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

        // --- Carousel / slide show ---
        if (flexCleaned === 'carousel' || flexCleaned === 'slide show') {
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

        // --- Hint slider with optional number ---
        var hintSliderMatch = flexCleaned.match(/^hint\s+slider\s*(\d+)?$/);
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

        // --- Image with optional number (must come BEFORE simple lookup) ---
        var imageMatch = flexCleaned.match(/^image\s+(\d+)$/);
        if (imageMatch) {
            return {
                normalised: 'image',
                level: null,
                number: parseInt(imageMatch[1], 10),
                id: null,
                category: 'media',
                modifier: null,
                raw: raw
            };
        }

        // --- Table with optional number or qualifier ---
        var tableMatch = flexCleaned.match(/^table(?:\s+(\S+))?$/);
        if (tableMatch && flexCleaned.indexOf('table') === 0) {
            var tableQualifier = tableMatch[1] || null;
            var tableNumber = null;
            if (tableQualifier && /^\d+$/.test(tableQualifier)) {
                tableNumber = parseInt(tableQualifier, 10);
                tableQualifier = null;
            }
            modifier = tableQualifier;
            return {
                normalised: 'table',
                level: null,
                number: tableNumber,
                id: null,
                category: 'subtag',
                modifier: modifier,
                raw: raw
            };
        }

        // --- Simple lookup table ---
        var lookupResult = this._lookupSimple(flexCleaned);
        if (lookupResult) {
            return {
                normalised: lookupResult.normalised,
                level: lookupResult.level || null,
                number: null,
                id: null,
                category: lookupResult.category,
                modifier: null,
                raw: raw
            };
        }

        // --- Unrecognised tag ---
        return {
            normalised: null,
            level: null,
            number: null,
            id: null,
            category: null,
            modifier: null,
            raw: raw
        };
    }

    // ------------------------------------------------------------------
    // Internal: Simple lookup table
    // ------------------------------------------------------------------

    /**
     * Look up a cleaned tag string in the simple normalisation table.
     *
     * @param {string} flexCleaned - Lowercased tag with hyphens→spaces
     * @returns {Object|null} { normalised, category, level? } or null
     */
    _lookupSimple(flexCleaned) {
        if (this._simpleTable.hasOwnProperty(flexCleaned)) {
            return this._simpleTable[flexCleaned];
        }
        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Build normalisation table
    // ------------------------------------------------------------------

    /**
     * Construct the complete normalisation lookup table and category map.
     */
    _buildNormalisationTable() {
        // Simple 1:1 mappings (flexCleaned → {normalised, category})
        this._simpleTable = {
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
            'static heading': { normalised: 'static_heading', category: 'subtag' },
            'static column': { normalised: 'static_column', category: 'subtag' },
            'unsorted list': { normalised: 'unordered_list', category: 'subtag' },
            'unordered list': { normalised: 'unordered_list', category: 'subtag' }
        };

        // Category map for getCategory() lookups
        this._categoryMap = [
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
                       'supervisor_button', 'modal_button', 'audio_button']
            },
            {
                category: 'subtag',
                tags: ['front', 'back', 'static_heading', 'static_column', 'unordered_list', 'table']
            }
        ];

        // All interactive tag names for category lookup
        this._interactiveTags = [
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
            'kanji_cards', 'embed_pdf', 'embed_padlet', 'embed_desmos'
        ];
    }

    // ------------------------------------------------------------------
    // Internal: Info trigger image merge special case
    // ------------------------------------------------------------------

    /**
     * Handle the special case where [info trigger] is immediately followed
     * by [image] (adjacent tags that should merge into info_trigger_image).
     *
     * @param {Array<Object>} tags - Array of normalised tag objects
     * @returns {Array<Object>} Updated tags array
     */
    _handleInfoTriggerImageMerge(tags) {
        if (tags.length < 2) return tags;

        var result = [];
        var i = 0;

        while (i < tags.length) {
            if (i < tags.length - 1 &&
                tags[i].normalised === 'info_trigger' &&
                tags[i + 1].normalised === 'image') {
                // Merge into info_trigger_image
                result.push({
                    normalised: 'info_trigger_image',
                    level: null,
                    number: null,
                    id: null,
                    category: 'interactive',
                    modifier: null,
                    raw: tags[i].raw + ' ' + tags[i + 1].raw
                });
                i += 2;
            } else {
                result.push(tags[i]);
                i++;
            }
        }

        return result;
    }
}
