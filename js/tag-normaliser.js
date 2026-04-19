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

        this._ordinalResolver = new OrdinalResolver();
        this._tables = new TagNormaliserTables();
        this._defragmenter = new TagDefragmenter();
        this._subTagMatcher = new SubTagMatcher(this._ordinalResolver);
        this._interactiveMatcher = new InteractiveTagMatcher();

        // Expose table data as own-properties so existing internal code
        // (_lookupSimple, getCategory, _annotateInteractive,
        // isInteractiveEndSignal) continues to reference these names.
        this._simpleTable              = this._tables.simpleTable;
        this._categoryMap              = this._tables.categoryMap;
        this._interactiveTags          = this._tables.interactiveTags;
        this._interactiveNonStartTags  = this._tables.interactiveNonStartTags;
        this._interactiveChildTagsMap  = this._tables.interactiveChildTagsMap;
        this._interactiveEndSignalTags = this._tables.interactiveEndSignalTags;
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
        return this._ordinalResolver.resolveOrdinalOrNumber(word);
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
        return this._defragmenter.defragmentRawText(text);
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


        // --- Interactive-category patterns (drag_and_drop through mcq) ---
        var interactiveResult = this._interactiveMatcher.match(flexCleaned, inner, raw);
        if (interactiveResult) return interactiveResult;

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
        var subTagResult = this._subTagMatcher.match(flexCleaned, inner, raw);
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
        return this._defragmenter.reassembleFragmentedTags(text);
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
     *   refines heading-level handling so H4 / H5 inside an activity wrapper
     *   are treated as activity scaffolding (do NOT close the inner
     *   interactive) while H2 / H3 still close.
     * @returns {boolean} True if this tag closes the current interactive.
     */
    isInteractiveEndSignal(normalisedTag, context) {
        if (!normalisedTag) return false;
        var name = typeof normalisedTag === 'string'
            ? normalisedTag
            : normalisedTag.normalised;
        if (!name) return false;

        if (this._interactiveEndSignalTags.indexOf(name) !== -1) return true;

        // Headings:
        //   • H2 / H3 always close (section boundary).
        //   • H4 / H5 close at top level, but inside an activity wrapper they
        //     are scaffolding for the activity itself and do NOT close the
        //     inner interactive (Session G refinement).
        if (name === 'heading') {
            var level = typeof normalisedTag === 'object' ? normalisedTag.level : null;
            if (level === 2 || level === 3) return true;
            if (level === 4 || level === 5) {
                var inActivity = context && context.inActivity === true;
                return !inActivity;
            }
        }

        return false;
    }
}
