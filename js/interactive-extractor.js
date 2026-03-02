/**
 * InteractiveExtractor — Detects interactive components, extracts their data,
 * generates structured placeholder HTML, and produces a reference document.
 *
 * @see CLAUDE.md Section 12 — Interactive Components
 */

'use strict';

class InteractiveExtractor {
    /**
     * Create an InteractiveExtractor instance.
     *
     * @param {TagNormaliser} tagNormaliser - An initialised TagNormaliser instance
     */
    constructor(tagNormaliser) {
        if (!tagNormaliser) {
            throw new Error('InteractiveExtractor requires a TagNormaliser instance');
        }

        /** @type {TagNormaliser} */
        this._normaliser = tagNormaliser;

        /**
         * Tier 1 — ParseMaster renders full HTML (Phase 7).
         * Simple, static HTML structures with no complex JS logic.
         */
        this.TIER_1_TYPES = ['accordion', 'flip_card', 'speech_bubble', 'tabs'];

        /**
         * Data pattern names keyed by pattern number.
         */
        this._patternNames = {
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
        this._typeToPrimaryPattern = {
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
        this._subTagTypes = [
            'carousel_slide', 'tab', 'shape', 'hint',
            'end_accordions'
        ];

        /**
         * Interactive types that use wide column class.
         */
        this._wideColTypes = ['drag_and_drop', 'info_trigger_image'];
    }

    // ------------------------------------------------------------------
    // Public API
    // ------------------------------------------------------------------

    /**
     * Process a sequence of content blocks starting from an interactive tag.
     * Returns the placeholder HTML and extracted data, plus how many blocks
     * were consumed.
     *
     * @param {Array<Object>} contentBlocks - All content blocks (raw, from page)
     * @param {number} startIndex - Index of the interactive tag block
     * @param {string} pageFilename - Filename of the HTML page being generated
     * @param {string|null} activityId - Activity number/ID if inside an activity wrapper
     * @param {boolean} insideActivity - Whether the interactive is inside an [activity] wrapper
     * @returns {Object} { placeholderHtml, referenceEntry, blocksConsumed, interactiveType, dataPattern }
     */
    processInteractive(contentBlocks, startIndex, pageFilename, activityId, insideActivity) {
        var block = contentBlocks[startIndex];
        var tagInfo = this._getInteractiveTag(block);

        if (!tagInfo) {
            return null;
        }

        var interactiveType = tagInfo.normalised;
        var modifier = tagInfo.modifier || null;
        var tier = this.TIER_1_TYPES.indexOf(interactiveType) !== -1 ? 1 : 2;

        // Look ahead to extract associated data
        var extracted = this._extractData(contentBlocks, startIndex, interactiveType);

        // Determine data pattern
        var dataPattern = extracted.detectedPattern ||
            this._typeToPrimaryPattern[interactiveType] || 1;
        var dataPatternName = this._patternNames[dataPattern] || 'Unknown';

        // Build position context
        var positionContext = this._buildPositionContext(contentBlocks, startIndex);

        // Determine column class
        var colClass = this._getColumnClass(interactiveType, modifier, extracted);

        // Build data summary string
        var dataSummary = this._buildDataSummary(extracted);

        // Collect writer instructions
        var writerInstructions = extracted.writerInstructions || [];
        // Also check the tag block itself for instructions
        var tagBlockInstructions = this._extractBlockInstructions(block);
        if (tagBlockInstructions.length > 0) {
            writerInstructions = tagBlockInstructions.concat(writerInstructions);
        }

        // Build placeholder HTML
        var placeholderHtml = this._generatePlaceholderHtml({
            interactiveType: interactiveType,
            modifier: modifier,
            activityId: activityId,
            pageFilename: pageFilename,
            colClass: colClass,
            tier: tier,
            dataPattern: dataPattern,
            dataSummary: dataSummary,
            writerInstructions: writerInstructions,
            activityHeading: extracted.activityHeading || null,
            activityInstructions: extracted.activityInstructions || null,
            insideActivity: insideActivity
        });

        // Build reference entry
        var referenceEntry = {
            index: 0,
            filename: pageFilename,
            activityId: activityId || null,
            type: interactiveType,
            modifier: modifier,
            tier: tier,
            dataPattern: dataPattern,
            dataPatternName: dataPatternName,
            positionContext: positionContext,
            tableData: extracted.tableData || null,
            listData: extracted.listData || null,
            numberedItems: extracted.numberedItems || null,
            activityHeading: extracted.activityHeading || null,
            activityInstructions: extracted.activityInstructions || null,
            writerInstructions: writerInstructions,
            mediaReferences: extracted.mediaReferences || [],
            redFlags: extracted.redFlags || [],
            notes: ''
        };

        return {
            placeholderHtml: placeholderHtml,
            referenceEntry: referenceEntry,
            blocksConsumed: extracted.blocksConsumed,
            interactiveType: interactiveType,
            dataPattern: dataPattern
        };
    }

    /**
     * Generate the complete interactive reference document for a module.
     *
     * @param {Array<Object>} allInteractives - Array of referenceEntry objects
     * @param {string} moduleCode - Module code
     * @returns {string} Plain text reference document
     */
    generateReferenceDocument(allInteractives, moduleCode) {
        if (!allInteractives || allInteractives.length === 0) {
            return '';
        }

        var total = allInteractives.length;
        var tier1Count = 0;
        var tier2Count = 0;
        var filesSet = {};

        for (var i = 0; i < allInteractives.length; i++) {
            allInteractives[i].index = i + 1;
            if (allInteractives[i].tier === 1) {
                tier1Count++;
            } else {
                tier2Count++;
            }
            filesSet[allInteractives[i].filename] = true;
        }

        var files = Object.keys(filesSet).sort();

        var lines = [];
        lines.push('=====================================');
        lines.push('INTERACTIVE REFERENCE \u2014 ' + moduleCode);
        lines.push('Generated by ParseMaster');
        lines.push('=====================================');
        lines.push('');
        lines.push('TOTAL INTERACTIVES: ' + total);
        lines.push('  Tier 1 (rendered by ParseMaster): ' + tier1Count +
            ' \u2014 accordion, flip_card, speech_bubble, tabs');
        lines.push('  Tier 2 (requires implementation): ' + tier2Count);
        lines.push('FILES: ' + files.join(', '));
        lines.push('');
        lines.push('=====================================');

        for (var j = 0; j < allInteractives.length; j++) {
            var entry = allInteractives[j];
            lines.push('');
            lines.push('INTERACTIVE ' + entry.index + ' of ' + total);
            lines.push('-------------------------------------');
            lines.push('File: ' + entry.filename);
            lines.push('Activity: ' + (entry.activityId || '(none \u2014 inline component)'));
            lines.push('Type: ' + entry.type);
            lines.push('Modifier: ' + (entry.modifier || 'none'));
            lines.push('Tier: ' + entry.tier + ' \u2014 ' +
                (entry.tier === 1 ? 'Rendered by ParseMaster' : 'Requires implementation'));
            lines.push('Data Pattern: ' + entry.dataPattern + ' \u2014 ' + entry.dataPatternName);
            lines.push('Position: ' + (entry.positionContext || 'Unknown'));
            lines.push('');

            if (entry.activityHeading) {
                lines.push('Activity Heading: ' + entry.activityHeading);
            }
            if (entry.activityInstructions) {
                lines.push('Activity Instructions: ' + entry.activityInstructions);
            }
            if (entry.activityHeading || entry.activityInstructions) {
                lines.push('');
            }

            // Data section
            lines.push(this._formatReferenceData(entry));

            // Writer instructions
            if (entry.writerInstructions && entry.writerInstructions.length > 0) {
                lines.push('Writer Instructions:');
                for (var wi = 0; wi < entry.writerInstructions.length; wi++) {
                    lines.push('  - ' + entry.writerInstructions[wi]);
                }
            } else {
                lines.push('Writer Instructions: None');
            }
            lines.push('');

            // Media references
            if (entry.mediaReferences && entry.mediaReferences.length > 0) {
                lines.push('Associated Media:');
                for (var mi = 0; mi < entry.mediaReferences.length; mi++) {
                    var media = entry.mediaReferences[mi];
                    lines.push('  ' + media.type + ': ' + media.url);
                }
            } else {
                lines.push('Associated Media: None');
            }
            lines.push('');

            // Red flags
            if (entry.redFlags && entry.redFlags.length > 0) {
                lines.push('Red Flags:');
                for (var rf = 0; rf < entry.redFlags.length; rf++) {
                    lines.push('  - ' + entry.redFlags[rf]);
                }
            } else {
                lines.push('Red Flags: None');
            }

            lines.push('');
            lines.push('-------------------------------------');
        }

        return lines.join('\n');
    }

    // ------------------------------------------------------------------
    // Internal: Tag detection
    // ------------------------------------------------------------------

    /**
     * Get the interactive tag from a content block.
     *
     * @param {Object} block - Content block
     * @returns {Object|null} Tag info or null
     */
    _getInteractiveTag(block) {
        if (block.type === 'paragraph' && block.data) {
            var text = this._buildFormattedText(block.data);
            var tagResult = this._normaliser.processBlock(text);
            if (tagResult.tags) {
                for (var i = 0; i < tagResult.tags.length; i++) {
                    if (tagResult.tags[i].category === 'interactive') {
                        return tagResult.tags[i];
                    }
                }
            }
        }
        return null;
    }

    /**
     * Check if a content block has a tag of a given category.
     *
     * @param {Object} block - Content block
     * @param {string} category - Category to check
     * @returns {Object|null} First matching tag or null
     */
    _getBlockTag(block, category) {
        if (block.type === 'paragraph' && block.data) {
            var text = this._buildFormattedText(block.data);
            var tagResult = this._normaliser.processBlock(text);
            if (tagResult.tags) {
                for (var i = 0; i < tagResult.tags.length; i++) {
                    if (category && tagResult.tags[i].category === category) {
                        return tagResult.tags[i];
                    }
                }
            }
        }
        return null;
    }

    /**
     * Get the primary tag from a content block.
     *
     * @param {Object} block - Content block
     * @returns {Object|null} Primary tag result or null
     */
    _getBlockPrimaryTag(block) {
        if (block.type === 'paragraph' && block.data) {
            var text = this._buildFormattedText(block.data);
            var tagResult = this._normaliser.processBlock(text);
            if (tagResult.tags && tagResult.tags.length > 0) {
                return tagResult.tags[0];
            }
        }
        return null;
    }

    /**
     * Get the full tag result for a block.
     *
     * @param {Object} block - Content block
     * @returns {Object} Tag result
     */
    _getBlockTagResult(block) {
        if (block.type === 'paragraph' && block.data) {
            var text = this._buildFormattedText(block.data);
            return this._normaliser.processBlock(text);
        }
        if (block.type === 'table' && block.data) {
            var tableText = this._buildTableText(block.data);
            return this._normaliser.processBlock(tableText);
        }
        return { tags: [], cleanText: '', redTextInstructions: [], isRedTextOnly: false, isWhitespaceOnly: true };
    }

    // ------------------------------------------------------------------
    // Internal: Data extraction
    // ------------------------------------------------------------------

    /**
     * Extract all associated data for an interactive component by looking ahead
     * from the interactive tag block.
     *
     * @param {Array<Object>} blocks - All content blocks
     * @param {number} startIndex - Index of the interactive tag block
     * @param {string} interactiveType - Normalised interactive type
     * @returns {Object} Extracted data
     */
    _extractData(blocks, startIndex, interactiveType) {
        var result = {
            blocksConsumed: 1, // at minimum, consume the interactive tag itself
            tableData: null,
            listData: null,
            numberedItems: null,
            writerInstructions: [],
            mediaReferences: [],
            activityHeading: null,
            activityInstructions: null,
            detectedPattern: null,
            redFlags: []
        };

        var i = startIndex + 1;

        // Special handling for speech_bubble with conversation layout (Pattern 9)
        if (interactiveType === 'speech_bubble') {
            var tagBlock = blocks[startIndex];
            var sbTagResult = this._getBlockTagResult(tagBlock);
            var sbModifier = '';
            if (sbTagResult.tags && sbTagResult.tags.length > 0) {
                sbModifier = (sbTagResult.tags[0].modifier || '').toLowerCase();
            }
            // Also check clean text for "conversation" keyword
            var sbClean = (sbTagResult.cleanText || '').toLowerCase();
            if (sbModifier.indexOf('conversation') !== -1 || sbClean.indexOf('conversation') !== -1) {
                result.detectedPattern = 9;
                var conversationItems = [];
                while (i < blocks.length) {
                    var convBlock = blocks[i];
                    if (convBlock.type !== 'paragraph' || !convBlock.data) break;
                    var convTagResult = this._getBlockTagResult(convBlock);
                    var convPrimaryTag = convTagResult.tags && convTagResult.tags.length > 0 ? convTagResult.tags[0] : null;
                    // Stop on any tagged block (structural, interactive, heading, activity, etc.)
                    if (convPrimaryTag && (convPrimaryTag.category === 'structural' ||
                        convPrimaryTag.category === 'interactive' ||
                        convPrimaryTag.category === 'heading' ||
                        convPrimaryTag.normalised === 'activity' ||
                        convPrimaryTag.normalised === 'end_activity' ||
                        convPrimaryTag.category === 'styling' ||
                        convPrimaryTag.category === 'media')) {
                        break;
                    }
                    var convText = (convTagResult.cleanText || '').trim();
                    if (!convText) { i++; continue; }
                    // Check if this looks like conversation content
                    var isConvLine = /^(prompt|ai\s*response|response|user|assistant|human|student)\s*\d*\s*:/i.test(convText);
                    // Also consume any non-tagged paragraph that follows the pattern
                    if (isConvLine || (!convPrimaryTag && conversationItems.length > 0)) {
                        conversationItems.push(convText);
                        if (convTagResult.redTextInstructions && convTagResult.redTextInstructions.length > 0) {
                            result.writerInstructions = result.writerInstructions.concat(convTagResult.redTextInstructions);
                        }
                        result.blocksConsumed = i - startIndex + 1;
                        i++;
                        continue;
                    }
                    break;
                }
                if (conversationItems.length > 0) {
                    result.numberedItems = conversationItems.map(function (text, idx) {
                        return { number: idx + 1, content: text, tag: 'conversation_line' };
                    });
                    return result;
                }
            }
        }

        // Look ahead to find associated data blocks
        while (i < blocks.length) {
            var block = blocks[i];

            // Check what this block is
            if (block.type === 'table') {
                // Tables immediately following an interactive are interactive data
                var tableData = this._extractTableData(block.data);
                if (tableData) {
                    result.tableData = tableData;
                    result.detectedPattern = this._detectTablePattern(tableData, interactiveType);
                    result.blocksConsumed = i - startIndex + 1;
                    // Check for media in table
                    var tableMedia = this._extractMediaFromTable(block.data);
                    result.mediaReferences = result.mediaReferences.concat(tableMedia);
                }
                i++;

                // After consuming a table, check if the NEXT block is also
                // interactive data (for patterns with multiple tables or
                // continuation). But be conservative — stop if it looks like
                // regular body content.
                continue;
            }

            if (block.type === 'paragraph' && block.data) {
                var tagResult = this._getBlockTagResult(block);
                var primaryTag = tagResult.tags && tagResult.tags.length > 0 ? tagResult.tags[0] : null;

                // Collect red text instructions from within the interactive scope
                if (tagResult.redTextInstructions && tagResult.redTextInstructions.length > 0) {
                    result.writerInstructions = result.writerInstructions.concat(tagResult.redTextInstructions);
                }

                // Check for sub-tags that belong to this interactive
                if (primaryTag && this._isSubTagFor(primaryTag, interactiveType)) {
                    // This is a sub-tag (e.g., [slide 1], [tab 1], [accordion 1])
                    var numberedData = this._collectNumberedItems(blocks, i, interactiveType);
                    result.numberedItems = numberedData.items;
                    result.detectedPattern = numberedData.detectedPattern;
                    result.blocksConsumed = numberedData.lastIndex - startIndex + 1;
                    i = numberedData.lastIndex + 1;
                    continue;
                }

                // Check for end markers
                if (primaryTag && (primaryTag.normalised === 'end_accordions' ||
                    primaryTag.normalised === 'end_activity')) {
                    // End marker: include it if it's end_accordions (part of interactive)
                    if (primaryTag.normalised === 'end_accordions') {
                        result.blocksConsumed = i - startIndex + 1;
                    }
                    break;
                }

                // Check for structural/activity tags that signal end of interactive
                if (primaryTag && (primaryTag.category === 'structural' ||
                    primaryTag.normalised === 'activity' ||
                    primaryTag.normalised === 'end_activity')) {
                    break;
                }

                // Check for a DIFFERENT interactive type (not a sub-tag of this parent)
                if (primaryTag && primaryTag.category === 'interactive' &&
                    !this._isSubTagFor(primaryTag, interactiveType) &&
                    primaryTag.normalised !== interactiveType) {
                    break;
                }

                // Check for heading/body/styling/media/link tags as boundary
                // ONLY if we are not expecting sub-tags (types that use numbered patterns)
                var expectsSubTags = this._typeToPrimaryPattern[interactiveType] >= 5 &&
                    this._typeToPrimaryPattern[interactiveType] <= 7;
                if (primaryTag && this._isEndBoundary(primaryTag) && !expectsSubTags) {
                    break;
                }

                // Check for media references in body text near the interactive
                var mediaRefs = this._extractMediaFromText(tagResult.cleanText || '');
                if (mediaRefs.length > 0) {
                    result.mediaReferences = result.mediaReferences.concat(mediaRefs);
                }

                // If this is a block with NO tag and the interactive already
                // has table data, it's probably regular body content — stop
                if (!primaryTag && result.tableData) {
                    break;
                }

                // If this is a block with NO tag and no table data yet, it might
                // be instruction text for the interactive. Consume conservatively:
                // only consume one tagless paragraph after the interactive tag
                if (!primaryTag && !result.tableData && result.blocksConsumed === 1) {
                    // This could be instructions/context text
                    result.blocksConsumed = i - startIndex + 1;
                    i++;
                    continue;
                }

                // If we already consumed extra paragraphs, stop
                if (!primaryTag) {
                    break;
                }
            }

            // If block is a page break or unknown type, stop
            if (block.type === 'pageBreak') {
                break;
            }

            i++;
        }

        return result;
    }

    /**
     * Check if a tag is a sub-tag that belongs to the given interactive type.
     *
     * @param {Object} tag - Tag object
     * @param {string} interactiveType - Parent interactive type
     * @returns {boolean}
     */
    _isSubTagFor(tag, interactiveType) {
        var name = tag.normalised;

        // carousel_slide belongs to carousel or rotating_banner
        if (name === 'carousel_slide' && (interactiveType === 'carousel' || interactiveType === 'rotating_banner')) {
            return true;
        }

        // tab belongs to tabs
        if (name === 'tab' && interactiveType === 'tabs') {
            return true;
        }

        // shape belongs to shape_hover
        if (name === 'shape' && interactiveType === 'shape_hover') {
            return true;
        }

        // hint belongs to hint_slider
        if (name === 'hint' && interactiveType === 'hint_slider') {
            return true;
        }

        // accordion (numbered) belongs to accordion
        if (name === 'accordion' && interactiveType === 'accordion') {
            return true;
        }

        // flip_card (numbered) belongs to flip_card
        if (name === 'flip_card' && interactiveType === 'flip_card') {
            return true;
        }

        // front/back sub-tags
        if ((name === 'front' || name === 'back') &&
            (interactiveType === 'flip_card' || interactiveType === 'click_drop')) {
            return true;
        }

        return false;
    }

    /**
     * Check if a tag signals the end of interactive data.
     *
     * @param {Object} tag - Tag object
     * @returns {boolean}
     */
    _isEndBoundary(tag) {
        var cat = tag.category;
        var name = tag.normalised;

        // Structural, heading, and activity tags are boundaries
        if (cat === 'structural') return true;
        if (cat === 'heading') return true;
        if (name === 'activity' || name === 'end_activity') return true;

        // Body, styling, media tags are boundaries
        if (cat === 'body') return true;
        if (cat === 'styling') return true;
        if (cat === 'media') return true;
        if (cat === 'link') return true;

        return false;
    }

    /**
     * Collect numbered items (slides, shapes, tabs, accordions) starting from
     * a sub-tag block.
     *
     * @param {Array<Object>} blocks - All content blocks
     * @param {number} startIndex - Index of the first sub-tag
     * @param {string} interactiveType - Parent interactive type
     * @returns {Object} { items, lastIndex, detectedPattern }
     */
    _collectNumberedItems(blocks, startIndex, interactiveType) {
        var items = [];
        var i = startIndex;
        var lastIndex = startIndex;
        var detectedPattern = null;

        // Map type to expected pattern
        if (interactiveType === 'carousel' || interactiveType === 'rotating_banner') {
            detectedPattern = 5;
        } else if (interactiveType === 'shape_hover' || interactiveType === 'tabs') {
            detectedPattern = 6;
        } else if (interactiveType === 'accordion') {
            detectedPattern = 7;
        } else if (interactiveType === 'flip_card' || interactiveType === 'click_drop') {
            detectedPattern = 2;
        } else if (interactiveType === 'hint_slider') {
            detectedPattern = 3;
        }

        while (i < blocks.length) {
            var block = blocks[i];
            var tagResult = this._getBlockTagResult(block);
            var primaryTag = tagResult.tags && tagResult.tags.length > 0 ? tagResult.tags[0] : null;

            // Check for end markers
            if (primaryTag && primaryTag.normalised === 'end_accordions') {
                lastIndex = i;
                break;
            }

            // Only break on true structural boundaries within numbered items:
            // structural tags (lesson, title_bar, etc.), activity/end_activity,
            // or a DIFFERENT interactive type that isn't a sub-tag of this parent
            if (primaryTag) {
                var cat = primaryTag.category;
                var name = primaryTag.normalised;

                // Structural tags and activity boundaries always break
                if (cat === 'structural') break;
                if (name === 'activity' || name === 'end_activity') break;

                // A different interactive type that isn't a sub-tag of this parent breaks
                if (cat === 'interactive' &&
                    !this._isSubTagFor(primaryTag, interactiveType) &&
                    name !== interactiveType) {
                    break;
                }
            }

            // If it's a sub-tag or a table or content within a sub-tag scope, collect it
            if (primaryTag && this._isSubTagFor(primaryTag, interactiveType)) {
                // Start a new numbered item
                var itemContent = tagResult.cleanText || '';
                var itemNumber = primaryTag.number || primaryTag.id || (items.length + 1);
                items.push({
                    number: itemNumber,
                    content: itemContent,
                    tag: primaryTag.normalised
                });
                lastIndex = i;
            } else if (block.type === 'table') {
                // Table within numbered items scope
                if (items.length > 0) {
                    var lastItem = items[items.length - 1];
                    var tableData = this._extractTableData(block.data);
                    if (tableData) {
                        lastItem.tableData = tableData;
                    }
                }
                lastIndex = i;
            } else if (items.length > 0) {
                // Content block (heading, body, media, etc.) within the current numbered item
                // These are data belonging to the last sub-tag
                var content = tagResult.cleanText || '';
                if (content.trim()) {
                    var currentItem = items[items.length - 1];
                    currentItem.content += (currentItem.content ? '\n' : '') + content;
                }
                // Also capture media references
                var mediaRefs = this._extractMediaFromText(content);
                if (block.type === 'paragraph' && block.data) {
                    var fullText = this._buildFormattedText(block.data);
                    mediaRefs = mediaRefs.concat(this._extractMediaFromText(fullText));
                }
                lastIndex = i;
            } else if (!primaryTag && items.length === 0) {
                // No items started yet, and no tag — this is regular body content
                break;
            }

            i++;
        }

        return {
            items: items.length > 0 ? items : null,
            lastIndex: lastIndex,
            detectedPattern: detectedPattern
        };
    }

    // ------------------------------------------------------------------
    // Internal: Table data extraction
    // ------------------------------------------------------------------

    /**
     * Extract structured table data from a table block.
     *
     * @param {Object} tableData - Table data object from parser
     * @returns {Object|null} Extracted table data
     */
    _extractTableData(tableData) {
        if (!tableData || !tableData.rows || tableData.rows.length === 0) {
            return null;
        }

        var headers = [];
        var rows = [];

        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            var rowData = [];

            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                var cellText = this._extractCellText(cell);
                rowData.push(cellText);
            }

            if (r === 0) {
                headers = rowData;
            } else {
                rows.push(rowData);
            }
        }

        var numCols = headers.length;
        var numRows = tableData.rows.length;

        return {
            headers: headers,
            rows: rows,
            dimensions: numRows + ' rows \u00D7 ' + numCols + ' columns'
        };
    }

    /**
     * Extract text content from a table cell, preserving formatting markers.
     *
     * @param {Object} cell - Cell data
     * @returns {string} Cell text
     */
    _extractCellText(cell) {
        if (!cell.paragraphs || cell.paragraphs.length === 0) return '';

        var parts = [];
        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            var text = this._buildFormattedText(para);
            // Strip red text markers but keep the content for reference
            var tagResult = this._normaliser.processBlock(text);
            var clean = tagResult.cleanText || '';
            if (clean.trim()) {
                parts.push(clean.trim());
            }
        }

        return parts.join(' / ');
    }

    /**
     * Detect which table data pattern matches for an interactive type.
     *
     * @param {Object} tableData - Extracted table data
     * @param {string} interactiveType - Interactive type
     * @returns {number} Pattern number
     */
    _detectTablePattern(tableData, interactiveType) {
        if (!tableData) return 1;

        // Check for front/back pattern (Pattern 2)
        if (interactiveType === 'flip_card' || interactiveType === 'click_drop') {
            return 2;
        }

        // Check for hint/slide pattern (Pattern 3)
        if (interactiveType === 'hint_slider') {
            return 3;
        }

        // Check for word select pattern (Pattern 10)
        if (interactiveType === 'word_select' || interactiveType === 'word_highlighter') {
            return 10;
        }

        // Check for axis labels (Pattern 11)
        if (interactiveType === 'slider_chart') {
            return 11;
        }

        // Check for info trigger image (Pattern 12)
        if (interactiveType === 'info_trigger_image') {
            return 12;
        }

        // Check for survey/self-assessment (Pattern 13)
        if (interactiveType === 'multichoice_quiz_survey') {
            return 13;
        }

        // Check for speech bubble pattern (Pattern 8)
        if (interactiveType === 'speech_bubble') {
            return 8;
        }

        // Default: single data table (Pattern 1)
        return 1;
    }

    /**
     * Extract media references from table data.
     *
     * @param {Object} tableData - Raw table data from parser
     * @returns {Array<Object>} Media references
     */
    _extractMediaFromTable(tableData) {
        var media = [];
        if (!tableData || !tableData.rows) return media;

        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                for (var p = 0; p < cell.paragraphs.length; p++) {
                    var para = cell.paragraphs[p];
                    var text = this._buildFormattedText(para);
                    var refs = this._extractMediaFromText(text);
                    media = media.concat(refs);
                }
            }
        }

        return media;
    }

    // ------------------------------------------------------------------
    // Internal: Text building helpers
    // ------------------------------------------------------------------

    /**
     * Build formatted text from paragraph runs (mirrors HtmlConverter logic).
     *
     * @param {Object} para - Paragraph data object
     * @returns {string} Formatted text
     */
    _buildFormattedText(para) {
        if (!para.runs || para.runs.length === 0) {
            return para.text || '';
        }

        var text = '';
        for (var i = 0; i < para.runs.length; i++) {
            var run = para.runs[i];
            if (!run.text) continue;

            var chunk = run.text;
            var fmt = run.formatting || {};

            if (fmt.isRed) {
                chunk = '\uD83D\uDD34[RED TEXT] ' + chunk + ' [/RED TEXT]\uD83D\uDD34';
            } else {
                chunk = this._applyFormattingMarkers(chunk, fmt);
            }

            if (run.hyperlink && !fmt.isRed) {
                var linkText = run.text.trim();
                if (linkText === run.hyperlink || linkText.replace(/\s/g, '') === run.hyperlink) {
                    chunk = run.hyperlink;
                } else {
                    chunk = chunk + ' [LINK: ' + run.hyperlink + ']';
                }
            }

            text += chunk;
        }

        return text;
    }

    /**
     * Apply formatting markers to text.
     *
     * @param {string} text - Raw text
     * @param {Object} fmt - Formatting object
     * @returns {string} Text with formatting markers
     */
    _applyFormattingMarkers(text, fmt) {
        if (!text.trim()) return text;

        var leadMatch = text.match(/^(\s*)/);
        var trailMatch = text.match(/(\s*)$/);
        var leading = leadMatch ? leadMatch[1] : '';
        var trailing = trailMatch ? trailMatch[1] : '';
        var inner = text.trim();

        if (!inner) return text;

        var result = inner;

        if (fmt.bold && fmt.italic) {
            result = '***' + result + '***';
        } else if (fmt.bold) {
            result = '**' + result + '**';
        } else if (fmt.italic) {
            result = '*' + result + '*';
        }

        if (fmt.underline) {
            result = '__' + result + '__';
        }

        return leading + result + trailing;
    }

    /**
     * Build combined text from a table for tag extraction.
     *
     * @param {Object} table - Table data
     * @returns {string}
     */
    _buildTableText(table) {
        if (!table.rows) return '';
        var texts = [];
        for (var r = 0; r < table.rows.length; r++) {
            var row = table.rows[r];
            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                for (var p = 0; p < cell.paragraphs.length; p++) {
                    var paraText = this._buildFormattedText(cell.paragraphs[p]);
                    if (paraText) texts.push(paraText);
                }
            }
        }
        return texts.join(' ');
    }

    // ------------------------------------------------------------------
    // Internal: Media extraction
    // ------------------------------------------------------------------

    /**
     * Extract media references from text content.
     *
     * @param {string} text - Text content
     * @returns {Array<Object>} Media references
     */
    _extractMediaFromText(text) {
        var media = [];
        if (!text) return media;

        // iStock URLs
        var istockRegex = /https?:\/\/(?:www\.)?istockphoto\.com\/[^\s\]]+/g;
        var istockMatch;
        while ((istockMatch = istockRegex.exec(text)) !== null) {
            media.push({ type: 'image', url: istockMatch[0] });
        }

        // Audio files
        var audioRegex = /([^\s/]+\.mp3)/gi;
        var audioMatch;
        while ((audioMatch = audioRegex.exec(text)) !== null) {
            media.push({ type: 'audio', url: audioMatch[1] });
        }

        // Generic image URLs (not iStock)
        var imgRegex = /https?:\/\/[^\s\]]+\.(?:jpg|jpeg|png|gif|webp|svg)/gi;
        var imgMatch;
        while ((imgMatch = imgRegex.exec(text)) !== null) {
            // Avoid duplicates with iStock
            var alreadyCaptured = false;
            for (var m = 0; m < media.length; m++) {
                if (media[m].url === imgMatch[0]) {
                    alreadyCaptured = true;
                    break;
                }
            }
            if (!alreadyCaptured) {
                media.push({ type: 'image', url: imgMatch[0] });
            }
        }

        return media;
    }

    /**
     * Extract writer instructions from a block's red text.
     *
     * @param {Object} block - Content block
     * @returns {Array<string>} Instructions
     */
    _extractBlockInstructions(block) {
        if (block.type !== 'paragraph' || !block.data) return [];
        var text = this._buildFormattedText(block.data);
        var tagResult = this._normaliser.processBlock(text);
        return tagResult.redTextInstructions || [];
    }

    // ------------------------------------------------------------------
    // Internal: Context and summary helpers
    // ------------------------------------------------------------------

    /**
     * Build position context string describing what comes before this interactive.
     *
     * @param {Array<Object>} blocks - Content blocks
     * @param {number} index - Current block index
     * @returns {string} Context description
     */
    _buildPositionContext(blocks, index) {
        // Look backwards for the nearest heading or notable content
        for (var i = index - 1; i >= Math.max(0, index - 5); i--) {
            var block = blocks[i];
            if (block.type === 'paragraph' && block.data) {
                var tagResult = this._getBlockTagResult(block);
                var primaryTag = tagResult.tags && tagResult.tags.length > 0 ? tagResult.tags[0] : null;

                if (primaryTag && primaryTag.normalised === 'heading') {
                    var headingText = tagResult.cleanText || '';
                    if (headingText.trim()) {
                        return 'After heading "' + headingText.trim().substring(0, 60) + '"';
                    }
                }

                if (primaryTag && primaryTag.normalised === 'activity_heading') {
                    var ahText = tagResult.cleanText || '';
                    if (ahText.trim()) {
                        return 'Activity heading: "' + ahText.trim().substring(0, 60) + '"';
                    }
                }

                if (!primaryTag && tagResult.cleanText && tagResult.cleanText.trim()) {
                    return 'After paragraph "' + tagResult.cleanText.trim().substring(0, 60) + '..."';
                }
            }
        }

        return 'Start of content section';
    }

    /**
     * Build a brief data summary string.
     *
     * @param {Object} extracted - Extracted data
     * @returns {string} Summary string
     */
    _buildDataSummary(extracted) {
        if (extracted.tableData) {
            return 'Table (' + extracted.tableData.dimensions + ')';
        }
        if (extracted.numberedItems && extracted.numberedItems.length > 0) {
            return extracted.numberedItems.length + ' numbered items';
        }
        return 'No structured data detected';
    }

    /**
     * Determine the correct column class for the interactive placeholder.
     *
     * @param {string} type - Interactive type
     * @param {string|null} modifier - Modifier string
     * @param {Object} extracted - Extracted data
     * @returns {string} Column class
     */
    _getColumnClass(type, modifier, extracted) {
        // D&D with column modifier
        if (type === 'drag_and_drop' && modifier && modifier.indexOf('column') !== -1) {
            // Check for many images (6+ items)
            if (extracted.tableData && extracted.tableData.rows &&
                extracted.tableData.rows.length >= 6) {
                return 'col-md-10 col-12';
            }
            return 'col-md-12 col-12';
        }

        // Info trigger image
        if (type === 'info_trigger_image') {
            return 'col-md-12 col-12';
        }

        // All carousel types and everything else
        return 'col-md-8 col-12';
    }

    // ------------------------------------------------------------------
    // Internal: Placeholder HTML generation
    // ------------------------------------------------------------------

    /**
     * Generate the placeholder HTML for an interactive component.
     *
     * @param {Object} opts - Options for placeholder generation
     * @returns {string} HTML string
     */
    _generatePlaceholderHtml(opts) {
        var type = opts.interactiveType;
        var modifier = opts.modifier;
        var activityId = opts.activityId;
        var filename = opts.pageFilename;
        var colClass = opts.colClass;
        var tier = opts.tier;
        var dataPattern = opts.dataPattern;
        var dataSummary = opts.dataSummary;
        var writerInstructions = opts.writerInstructions;
        var insideActivity = opts.insideActivity;

        var typeLabel = type + (modifier ? ' (' + modifier + ')' : '');
        var activityLabel = activityId || 'inline';

        var lines = [];

        // Opening HTML comment
        lines.push('<!-- ========== INTERACTIVE: ' + typeLabel +
            ' | Activity: ' + activityLabel +
            ' | File: ' + filename + ' ========== -->');

        // Only generate the activity wrapper if we have a named activity ID
        // and we're not already inside an activity wrapper.
        // Inline interactives (no activity ID, not inside [activity] block) get no wrapper.
        var needsActivityWrapper = !insideActivity && activityId;
        if (needsActivityWrapper) {
            lines.push('<div class="activity interactive" number="' + this._escAttr(activityId) + '">');
        }

        lines.push('  <div class="row">');
        lines.push('    <div class="' + colClass + '">');

        // Data comment block
        lines.push('      <!-- INTERACTIVE_START: ' + type + ' -->');
        lines.push('      <!-- Data Pattern: ' + dataPattern + ' -->');
        lines.push('      <!-- Data Summary: ' + dataSummary + ' -->');

        if (writerInstructions && writerInstructions.length > 0) {
            for (var wi = 0; wi < writerInstructions.length; wi++) {
                lines.push('      <!-- Writer Instructions: ' +
                    this._escContent(writerInstructions[wi]) + ' -->');
            }
        }

        // Visible placeholder indicator
        if (tier === 1) {
            lines.push('      <p style="color: green; border: 2px dashed green; padding: 10px; text-align: center;">');
            lines.push('        \uD83D\uDD27 TIER 1 INTERACTIVE: ' + this._escContent(type) + '<br />');
            lines.push('        Activity ' + this._escContent(activityLabel) +
                ' \u2014 ParseMaster will render this component (Phase 7)');
            lines.push('      </p>');
        } else {
            lines.push('      <p style="color: red; border: 2px dashed red; padding: 10px; text-align: center;">');
            lines.push('        \u26A0\uFE0F INTERACTIVE PLACEHOLDER: ' + this._escContent(type) + '<br />');
            lines.push('        Activity ' + this._escContent(activityLabel) +
                ' \u2014 see Interactive Reference Document for full data');
            lines.push('      </p>');
        }

        lines.push('      <!-- INTERACTIVE_END: ' + type + ' -->');
        lines.push('    </div>');
        lines.push('  </div>');

        if (needsActivityWrapper) {
            lines.push('</div>');
        }

        // Closing HTML comment
        lines.push('<!-- ========== END INTERACTIVE: ' + type + ' ========== -->');

        return lines.join('\n');
    }

    // ------------------------------------------------------------------
    // Internal: Reference document data formatting
    // ------------------------------------------------------------------

    /**
     * Format data for a reference document entry.
     *
     * @param {Object} entry - Reference entry
     * @returns {string} Formatted data text
     */
    _formatReferenceData(entry) {
        var lines = [];

        if (entry.tableData) {
            lines.push('Data (Table \u2014 ' + entry.tableData.dimensions + '):');
            if (entry.tableData.headers && entry.tableData.headers.length > 0) {
                lines.push('  Headers: ' + entry.tableData.headers.join(' | '));
            }
            if (entry.tableData.rows) {
                for (var r = 0; r < entry.tableData.rows.length; r++) {
                    lines.push('  Row ' + (r + 1) + ': ' + entry.tableData.rows[r].join(' | '));
                }
            }
            lines.push('');
        } else if (entry.numberedItems && entry.numberedItems.length > 0) {
            var patternLabel = this._patternNames[entry.dataPattern] || 'items';
            lines.push('Data (' + entry.numberedItems.length + ' ' + patternLabel.toLowerCase() + '):');
            for (var n = 0; n < entry.numberedItems.length; n++) {
                var item = entry.numberedItems[n];
                var prefix = item.tag ? item.tag : 'Item';
                lines.push('  ' + prefix + ' ' + item.number + ': ' +
                    (item.content || '').substring(0, 200));
                if (item.tableData) {
                    lines.push('    [Table: ' + item.tableData.dimensions + ']');
                }
            }
            lines.push('');
        } else {
            lines.push('Data: No structured data extracted');
            lines.push('');
        }

        return lines.join('\n');
    }

    // ------------------------------------------------------------------
    // Internal: HTML escaping helpers
    // ------------------------------------------------------------------

    /**
     * Escape HTML content text.
     *
     * @param {string} text
     * @returns {string}
     */
    _escContent(text) {
        if (!text) return '';
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    /**
     * Escape for HTML attributes.
     *
     * @param {string} text
     * @returns {string}
     */
    _escAttr(text) {
        if (!text) return '';
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }
}
