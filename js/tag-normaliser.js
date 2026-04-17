/**
 * TagNormaliser — Tag taxonomy and normalisation engine for PageForge.
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
        this._buildOrdinalMap();
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

        // Step 0: Pre-process — de-fragment fractured red text boundaries
        textContent = this.defragmentRawText(textContent);

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

        return this._annotateInteractive(this._normalise(inner, raw));
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

    /**
     * Pre-process raw text to de-fragment fractured red-text boundaries
     * caused by Microsoft Word splitting a single tag across multiple
     * XML formatting runs.
     *
     * Handles three classes of artifact:
     * 1. Redundant close/re-open boundaries:
     *    `[/RED TEXT]🔴` + whitespace + `🔴[RED TEXT]` → stripped
     * 2. Multiple spaces inside square brackets: collapsed to single space
     * 3. Leading/trailing spaces inside square brackets: trimmed
     *
     * @param {string} text - Raw text content potentially with fractured markers
     * @returns {string} Cleaned text with fractured boundaries stitched
     */
    defragmentRawText(text) {
        if (!text || typeof text !== 'string') return text;

        // 1. Stitch fractured red-text boundaries:
        //    [/RED TEXT]🔴 <whitespace> 🔴[RED TEXT] → removed
        text = text.replace(
            /\[\/RED TEXT\]\uD83D\uDD34\s*\uD83D\uDD34\[RED TEXT\]/g,
            ''
        );

        // 2. Collapse multiple spaces inside square brackets to single space
        text = text.replace(/\[([^\]]+)\]/g, function(match, inner) {
            var cleaned = inner.replace(/\s{2,}/g, ' ');
            return '[' + cleaned + ']';
        });

        // 3. Trim leading/trailing whitespace inside square brackets
        //    e.g. [ tags ] → [tags], [ H2 ] → [H2]
        text = text.replace(/\[\s+([^\]]*?)\s*\]/g, function(match, inner) {
            return '[' + inner.trim() + ']';
        });
        // Also handle trailing-only: [tags ] → [tags]
        text = text.replace(/\[([^\]]*?)\s+\]/g, function(match, inner) {
            return '[' + inner.trim() + ']';
        });

        return text;
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
            var normalised = this._annotateInteractive(this._normalise(inner, raw));

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

        // --- Video tag variants (embed video, imbed video, insert video, etc.) ---
        var videoResult = this._matchVideoTag(flexCleaned, inner, raw);
        if (videoResult) {
            return videoResult;
        }

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

        // --- Incomplete heading tag [H ] or [H] (no digit) — fallback heading ---
        var incompleteHeadingMatch = flexCleaned.match(/^h\s*$/);
        if (incompleteHeadingMatch) {
            return {
                normalised: 'heading',
                level: null,
                number: null,
                id: null,
                category: 'heading',
                modifier: 'incomplete',
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

        // --- Activity heading / activity title (with optional heading level) ---
        var actHeadingMatch = flexCleaned.match(/^activity\s+(?:heading|title)(?:\s+h?\s*([2-5]))?$/);
        if (actHeadingMatch) {
            return {
                normalised: 'activity_heading',
                level: actHeadingMatch[1] ? parseInt(actHeadingMatch[1], 10) : 3,
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

        // --- [Table wordSelect] / [Table word select] → word_select interactive ---
        if (flexCleaned === 'table wordselect' || flexCleaned === 'table word select') {
            return {
                normalised: 'word_select',
                level: null,
                number: null,
                id: null,
                category: 'interactive',
                modifier: 'table',
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

        // --- Button with descriptive suffix: [button- external link], [button-download], etc. ---
        var buttonSuffixMatch = flexCleaned.match(/^button\s*[\u2013\u2014-]?\s*(external\s*link|external|link|download)$/);
        if (buttonSuffixMatch) {
            var btnSuffix = buttonSuffixMatch[1].replace(/\s+/g, '_');
            var btnNormalised = 'external_link_button';
            if (btnSuffix === 'download') btnNormalised = 'button';
            return {
                normalised: btnNormalised,
                level: null,
                number: null,
                id: null,
                category: 'link',
                modifier: btnSuffix,
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

        // --- Ordinal & verbose sub-tag matching (last resort before unrecognised) ---
        var subTagResult = this._matchSubTag(flexCleaned, inner, raw);
        if (subTagResult) {
            return subTagResult;
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
            'kanji_cards', 'embed_pdf', 'embed_padlet', 'embed_desmos',
            'upload_to_dropbox'
        ];

        // Interactive tags that are NOT start-of-interactive (they are sub-tags
        // or the close marker of an accordion group). Everything else listed in
        // `_interactiveTags` is treated as an interactive-start tag.
        this._interactiveNonStartTags = [
            'carousel_slide', 'tab', 'shape', 'hint', 'end_accordions'
        ];

        // Child sub-tags that are structurally contained within a given
        // interactive-start tag. Used by the boundary-detection algorithm
        // (Session F, `js/interactive-extractor.js`) to decide whether a
        // following block belongs inside the current interactive boundary.
        // Values are normalised tag names. Interactive-start tags not listed
        // here default to an empty array.
        this._interactiveChildTagsMap = {
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
        this._interactiveEndSignalTags = [
            'body', 'end_page', 'end_activity', 'lesson',
            'alert', 'alert_cultural_wananga', 'alert_cultural_talanoa',
            'alert_cultural_combined',
            'important', 'whakatauki', 'quote'
        ];
    }

    /**
     * Annotate a normalised tag object with interactive-boundary metadata.
     * Adds `isInteractiveStart` (boolean) and `interactiveChildTags` (array of
     * normalised sub-tag names) to every `category: 'interactive'` record so
     * the downstream boundary-detection algorithm in
     * `js/interactive-extractor.js` can iterate without re-computing these
     * classifications.
     *
     * @param {Object|null} tagObj - Normalised tag record (or null).
     * @returns {Object|null} Same record with added metadata, or null.
     */
    _annotateInteractive(tagObj) {
        if (!tagObj || tagObj.category !== 'interactive') return tagObj;
        var name = tagObj.normalised;
        tagObj.isInteractiveStart = (this._interactiveNonStartTags.indexOf(name) === -1);
        tagObj.interactiveChildTags = this._interactiveChildTagsMap[name] || [];
        return tagObj;
    }

    // ------------------------------------------------------------------
    // Public: Red-text fragment reassembly
    // ------------------------------------------------------------------

    /**
     * Reassemble fragmented red-text tags that were split across multiple
     * Word formatting runs.
     *
     * When a writer types [speech bubble] in red but Word splits it across
     * two XML runs (e.g., one with italic, one without), the parser outputs:
     *   🔴[RED TEXT] [ [/RED TEXT]🔴🔴[RED TEXT] speech bubble] [/RED TEXT]🔴
     * This method detects such adjacent markers and merges them when their
     * combined content forms a valid [tag] pattern.
     *
     * @param {string} text - Text with red-text markers
     * @returns {string} Text with fragmented tags reassembled
     */
    reassembleFragmentedTags(text) {
        if (!text || typeof text !== 'string') return text;

        // Use a non-trimming regex to preserve inner whitespace for reassembly
        var redMarkerRe = /\uD83D\uDD34\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\uD83D\uDD34/g;

        // Collect all red-text markers and their positions
        var markers = [];
        var match;
        while ((match = redMarkerRe.exec(text)) !== null) {
            markers.push({
                fullMatch: match[0],
                innerContent: match[1],  // preserves original whitespace
                innerTrimmed: match[1].trim(),
                startIndex: match.index,
                endIndex: match.index + match[0].length
            });
        }

        if (markers.length < 2) return text;

        // Scan for consecutive markers that should be merged
        var merges = [];

        for (var i = 0; i < markers.length - 1; i++) {
            // Skip markers already consumed by a merge
            var alreadyConsumed = false;
            for (var mc = 0; mc < merges.length; mc++) {
                if (i >= merges[mc].startIdx && i <= merges[mc].endIdx) {
                    alreadyConsumed = true;
                    break;
                }
            }
            if (alreadyConsumed) continue;

            // Try merging N consecutive markers (4, 3, 2) — longest match first
            var maxLookahead = Math.min(markers.length - i, 6); // up to 6-way merge

            var merged = false;
            for (var span = maxLookahead; span >= 2; span--) {
                if (i + span - 1 >= markers.length) continue;

                // Check all gaps between markers are empty
                var allGapsEmpty = true;
                for (var g = 0; g < span - 1; g++) {
                    var gap = text.substring(markers[i + g].endIndex, markers[i + g + 1].startIndex).trim();
                    if (gap !== '') {
                        allGapsEmpty = false;
                        break;
                    }
                }

                if (!allGapsEmpty) continue;

                // Concatenate all inner contents preserving original whitespace
                var parts = [];
                for (var c = 0; c < span; c++) {
                    parts.push(markers[i + c].innerContent);
                }
                // Direct concatenation preserves original spacing
                // (e.g., "[End " + "tab]" = "[End tab]")
                // Then normalise multiple spaces to single
                var combined = parts.join('').replace(/\s+/g, ' ').trim();

                // Check if combined text contains or forms a valid tag
                var tagMatch = combined.match(/\[([^\]]+)\]/);
                // Also check if it contains an incomplete bracket that would complete
                var hasOpenBracket = combined.indexOf('[') !== -1;
                var hasCloseBracket = combined.indexOf(']') !== -1;

                if (tagMatch || (hasOpenBracket && hasCloseBracket)) {
                    merges.push({
                        startIdx: i,
                        endIdx: i + span - 1,
                        replacement: '\uD83D\uDD34[RED TEXT] ' + combined + ' [/RED TEXT]\uD83D\uDD34'
                    });
                    merged = true;
                    break;
                }
            }

            // If no multi-way merge worked, skip to next marker
        }

        // Apply merges in reverse order so indices don't shift
        for (var m = merges.length - 1; m >= 0; m--) {
            var merge = merges[m];
            var startPos = markers[merge.startIdx].startIndex;
            var endPos = markers[merge.endIdx].endIndex;
            text = text.substring(0, startPos) + merge.replacement + text.substring(endPos);
        }

        return text;
    }

    // ------------------------------------------------------------------
    // Internal: Video tag matching
    // ------------------------------------------------------------------

    /**
     * Match video tag variants including embed/imbed/insert video/film patterns.
     *
     * @param {string} flexCleaned - Lowercased, normalised tag text
     * @param {string} inner - Original inner tag text
     * @param {string} raw - Full raw tag with brackets
     * @returns {Object|null} Normalised video tag or null
     */
    _matchVideoTag(flexCleaned, inner, raw) {
        // Core video patterns
        var videoPatterns = [
            /^embed\s+video$/,
            /^imbed\s+video$/,
            /^insert\s+video$/,
            /^embed\s+film$/,
            /^imbed\s+film$/
        ];

        for (var p = 0; p < videoPatterns.length; p++) {
            if (flexCleaned.match(videoPatterns[p])) {
                return {
                    normalised: 'video',
                    level: null,
                    number: null,
                    id: null,
                    category: 'media',
                    modifier: null,
                    raw: raw
                };
            }
        }

        // [interactive: video] or [interactive: video: title]
        var interVideoMatch = flexCleaned.match(/^interactive\s*:\s*video(?:\s*:\s*(.+))?$/);
        if (interVideoMatch) {
            return {
                normalised: 'video',
                level: null,
                number: null,
                id: null,
                category: 'media',
                modifier: interVideoMatch[1] ? interVideoMatch[1].trim() : null,
                raw: raw
            };
        }

        // [insert Audio animation Video N (...)]
        if (flexCleaned.match(/audio\s+animation\s+video/)) {
            return {
                normalised: 'video',
                level: null,
                number: null,
                id: null,
                category: 'media',
                modifier: 'audio_animation',
                raw: raw
            };
        }

        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Ordinal map
    // ------------------------------------------------------------------

    /**
     * Build the ordinal/cardinal word → number lookup map.
     */
    _buildOrdinalMap() {
        this._ordinalMap = {
            'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'forth': 4,
            'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10,
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        };
    }

    // ------------------------------------------------------------------
    // Internal: Verbose sub-tag matching
    // ------------------------------------------------------------------

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
    _matchSubTag(flexCleaned, inner, raw) {
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
                number: this.resolveOrdinalOrNumber(ordAccMatch[1]),
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
                number: this.resolveOrdinalOrNumber(wordAccMatch[1]),
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
                number: this.resolveOrdinalOrNumber(ordFlipMatch[1]),
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

    /**
     * Decide whether a normalised tag closes the current interactive boundary.
     * Consumed by the interactive-extractor's boundary-detection algorithm.
     *
     * @param {Object|string} normalisedTag - Either a normalised tag record
     *   (with at least `.normalised` and optional `.level`/`.category`) or a
     *   plain normalised tag name string.
     * @param {Object} [context] - Optional context; `{ inActivity: boolean }`
     *   is accepted for forward compatibility (refined in Session G).
     * @returns {boolean} True if this tag closes the current interactive.
     */
    isInteractiveEndSignal(normalisedTag, context) {
        if (!normalisedTag) return false;
        var name = typeof normalisedTag === 'string'
            ? normalisedTag
            : normalisedTag.normalised;
        if (!name) return false;

        if (this._interactiveEndSignalTags.indexOf(name) !== -1) return true;

        // Headings: H2 / H3 always close. H4 / H5 close at top level (Session F);
        // Session G refines the H4/H5 rule when `context.inActivity` is true.
        if (name === 'heading') {
            var level = typeof normalisedTag === 'object' ? normalisedTag.level : null;
            if (level === 2 || level === 3) return true;
            if (level === 4 || level === 5) {
                var inActivity = context && context.inActivity === true;
                // Session F: top-level H4/H5 close; inside activity left to Session G.
                return !inActivity;
            }
        }

        return false;
    }
}
