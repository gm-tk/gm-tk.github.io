/**
 * InteractiveDataExtractor — block-stream orchestration for interactive tags.
 *
 * Walks the sequence of content blocks after an interactive-start tag to
 * extract structured data (the 13-pattern `_extractData` flow), collect
 * numbered items, evaluate sub-tag / end-boundary predicates, and compute
 * the inclusive Session F/G boundary.
 *
 * Extracted from js/interactive-extractor.js as part of the interactive-extractor
 * refactor. See docs/28-interactive-extractor-refactor-plan.md.
 */

'use strict';

class InteractiveDataExtractor {
    constructor(tagNormaliser, tables, cellParser) {
        this._normaliser = tagNormaliser;
        this._tables = tables;
        this._cellParser = cellParser;
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

        // If the interactive tag block itself is a table (e.g., speech bubble in table row
        // with image + text), extract the table data from it directly.
        var tagBlock = blocks[startIndex];
        if (tagBlock.type === 'table' && tagBlock.data) {
            var tagTableData = this._cellParser._extractTableData(tagBlock.data);
            if (tagTableData) {
                result.tableData = tagTableData;
                result.detectedPattern = this._cellParser._detectTablePattern(tagTableData, interactiveType);
                // Extract media from the table
                var tagTableMedia = this._cellParser._extractMediaFromTable(tagBlock.data);
                result.mediaReferences = result.mediaReferences.concat(tagTableMedia);
            }
            // Extract writer instructions from table cells
            if (tagBlock.data.rows) {
                for (var tr = 0; tr < tagBlock.data.rows.length; tr++) {
                    var tRow = tagBlock.data.rows[tr];
                    for (var tc = 0; tc < tRow.cells.length; tc++) {
                        var tCell = tRow.cells[tc];
                        for (var tp = 0; tp < tCell.paragraphs.length; tp++) {
                            var tText = this._cellParser._buildFormattedText(tCell.paragraphs[tp]);
                            var tTagResult = this._normaliser.processBlock(tText);
                            if (tTagResult.redTextInstructions && tTagResult.redTextInstructions.length > 0) {
                                result.writerInstructions = result.writerInstructions.concat(tTagResult.redTextInstructions);
                            }
                        }
                    }
                }
            }
        }

        var i = startIndex + 1;

        // Determine if this interactive type expects numbered sub-tags
        var expectsSubTags = (
            (this._tables.typeToPrimaryPattern[interactiveType] >= 5 &&
             this._tables.typeToPrimaryPattern[interactiveType] <= 7) ||
            interactiveType === 'flip_card' ||
            interactiveType === 'click_drop' ||
            interactiveType === 'hint_slider'
        );

        // Special handling for dropdown_quiz_paragraph (Pattern 4) — Bug 3 fix Round 3C
        // This compound interactive spans multiple blocks: story paragraphs with inline
        // [Dropdown N] markers, an optional [story heading] sub-tag, and an options table.
        // All must be collected into a SINGLE interactive placeholder.
        if (interactiveType === 'dropdown_quiz_paragraph') {
            result.detectedPattern = 4;
            var dqpStoryParagraphs = [];
            var dqpStoryTitle = null;
            var dqpDropdownCount = 0;

            while (i < blocks.length) {
                var dqpBlock = blocks[i];

                // Tables are the options data — consume and stop scanning for story
                if (dqpBlock.type === 'table' && dqpBlock.data) {
                    var dqpTableData = this._cellParser._extractTableData(dqpBlock.data);
                    if (dqpTableData) {
                        result.tableData = dqpTableData;
                    }
                    result.blocksConsumed = i - startIndex + 1;
                    i++;
                    // After consuming the options table, stop
                    break;
                }

                if (dqpBlock.type === 'paragraph' && dqpBlock.data) {
                    var dqpTagResult = this._getBlockTagResult(dqpBlock);
                    var dqpPrimaryTag = dqpTagResult.tags && dqpTagResult.tags.length > 0 ? dqpTagResult.tags[0] : null;

                    // Stop at structural, activity, or different interactive boundaries
                    if (dqpPrimaryTag && (dqpPrimaryTag.category === 'structural' ||
                        dqpPrimaryTag.normalised === 'activity' ||
                        dqpPrimaryTag.normalised === 'end_activity')) {
                        break;
                    }
                    // Stop at different interactive types (NOT dropdown — those are inline markers)
                    if (dqpPrimaryTag && dqpPrimaryTag.category === 'interactive' &&
                        dqpPrimaryTag.normalised !== 'dropdown' &&
                        dqpPrimaryTag.normalised !== 'dropdown_quiz_paragraph') {
                        break;
                    }

                    // Collect red text instructions
                    if (dqpTagResult.redTextInstructions && dqpTagResult.redTextInstructions.length > 0) {
                        result.writerInstructions = result.writerInstructions.concat(dqpTagResult.redTextInstructions);
                    }

                    // Check for [story heading] sub-tag
                    if (dqpPrimaryTag && dqpPrimaryTag.normalised === 'static_heading') {
                        dqpStoryTitle = (dqpTagResult.cleanText || '').trim();
                        result.blocksConsumed = i - startIndex + 1;
                        i++;
                        continue;
                    }
                    // Also check for story_heading alias
                    if (dqpPrimaryTag && dqpPrimaryTag.raw &&
                        dqpPrimaryTag.raw.toLowerCase().indexOf('story heading') !== -1) {
                        dqpStoryTitle = (dqpTagResult.cleanText || '').trim();
                        result.blocksConsumed = i - startIndex + 1;
                        i++;
                        continue;
                    }

                    // Check for [Dropdown N] inline markers — count them
                    if (dqpPrimaryTag && dqpPrimaryTag.normalised === 'dropdown') {
                        dqpDropdownCount++;
                    }
                    // Also check for inline [Dropdown N] within the text (not just as primary tag)
                    if (dqpTagResult.tags) {
                        for (var ddi = 0; ddi < dqpTagResult.tags.length; ddi++) {
                            if (dqpTagResult.tags[ddi].normalised === 'dropdown' &&
                                dqpTagResult.tags[ddi] !== dqpPrimaryTag) {
                                dqpDropdownCount++;
                            }
                        }
                    }

                    // Get the text content — keep [Dropdown N] markers visible in story text
                    var dqpText = this._cellParser._buildFormattedText(dqpBlock.data);
                    // Strip red text markers but keep [Dropdown N] markers
                    dqpText = dqpText.replace(/\uD83D\uDD34\[RED TEXT\]\s*([\s\S]*?)\s*\[\/RED TEXT\]\uD83D\uDD34/g,
                        function (m, inner) {
                            // Keep [Dropdown N] tags visible, strip everything else
                            var dropdownRe = /\[(?:drop\s*down|dropdown)\s*\d+\]/gi;
                            var kept = [];
                            var dm;
                            while ((dm = dropdownRe.exec(inner)) !== null) {
                                kept.push(dm[0]);
                            }
                            return kept.length > 0 ? kept.join(' ') : '';
                        });
                    dqpText = dqpText.replace(/\s+/g, ' ').trim();

                    if (dqpText) {
                        dqpStoryParagraphs.push(dqpText);
                    }

                    result.blocksConsumed = i - startIndex + 1;
                }

                i++;
            }

            // Build numbered items from collected story data
            if (dqpStoryParagraphs.length > 0 || dqpStoryTitle) {
                var dqpItems = [];
                if (dqpStoryTitle) {
                    dqpItems.push({
                        number: 0,
                        content: dqpStoryTitle,
                        tag: 'story_heading'
                    });
                }
                for (var sp = 0; sp < dqpStoryParagraphs.length; sp++) {
                    dqpItems.push({
                        number: sp + 1,
                        content: dqpStoryParagraphs[sp],
                        tag: 'story_paragraph'
                    });
                }
                result.numberedItems = dqpItems;
            }

            return result;
        }

        // Special handling for speech_bubble with conversation layout (Pattern 9)
        if (interactiveType === 'speech_bubble') {
            var sbBlock = blocks[startIndex];
            var sbTagResult = this._getBlockTagResult(sbBlock);
            var sbModifier = '';
            if (sbTagResult.tags && sbTagResult.tags.length > 0) {
                sbModifier = (sbTagResult.tags[0].modifier || '').toLowerCase();
            }
            // Also check clean text and red text instructions for "conversation" keyword
            var sbClean = (sbTagResult.cleanText || '').toLowerCase();
            var sbIsConversation = sbModifier.indexOf('conversation') !== -1 || sbClean.indexOf('conversation') !== -1;
            // Check red text instructions (writer instruction like "Conversation layout"
            // appears here when it's inside the red text region but outside brackets)
            if (!sbIsConversation && sbTagResult.redTextInstructions) {
                for (var ri = 0; ri < sbTagResult.redTextInstructions.length; ri++) {
                    if (sbTagResult.redTextInstructions[ri].toLowerCase().indexOf('conversation') !== -1) {
                        sbIsConversation = true;
                        break;
                    }
                }
            }
            if (sbIsConversation) {
                result.detectedPattern = 9;
                var conversationItems = [];
                var convRegex = /^(prompt|ai\s*response|response|user|assistant|human|student)\s*\d*\s*:/i;
                while (i < blocks.length) {
                    var convBlock = blocks[i];
                    if (convBlock.type !== 'paragraph' || !convBlock.data) break;
                    var convTagResult = this._getBlockTagResult(convBlock);
                    var convPrimaryTag = convTagResult.tags && convTagResult.tags.length > 0 ? convTagResult.tags[0] : null;
                    // Stop on structural, interactive, heading, activity tags
                    if (convPrimaryTag && (convPrimaryTag.category === 'structural' ||
                        convPrimaryTag.category === 'interactive' ||
                        convPrimaryTag.category === 'heading' ||
                        convPrimaryTag.category === 'link' ||
                        convPrimaryTag.normalised === 'activity' ||
                        convPrimaryTag.normalised === 'end_activity' ||
                        convPrimaryTag.category === 'styling' ||
                        convPrimaryTag.category === 'media')) {
                        break;
                    }
                    // Stop on [body] tag — this signals the end of conversation
                    if (convPrimaryTag && convPrimaryTag.category === 'body') {
                        break;
                    }
                    // Get text from clean text, or from formatted text if clean is empty
                    var convText = (convTagResult.cleanText || '').trim();
                    if (!convText) {
                        // Try raw formatted text (conversation may be in non-tagged runs)
                        var rawConvText = this._cellParser._buildFormattedText(convBlock.data);
                        // Strip red text markers to get clean text
                        rawConvText = rawConvText.replace(/\uD83D\uDD34\[RED TEXT\]\s*[\s\S]*?\s*\[\/RED TEXT\]\uD83D\uDD34/g, '').trim();
                        rawConvText = rawConvText.replace(/\[([^\]]+)\]/g, '').trim();
                        if (rawConvText) {
                            convText = rawConvText;
                        }
                    }
                    if (!convText) { i++; continue; }
                    // Collect red text instructions
                    if (convTagResult.redTextInstructions && convTagResult.redTextInstructions.length > 0) {
                        result.writerInstructions = result.writerInstructions.concat(convTagResult.redTextInstructions);
                    }
                    // Check if this looks like conversation content
                    var isConvLine = convRegex.test(convText);
                    if (isConvLine) {
                        conversationItems.push(convText);
                        result.blocksConsumed = i - startIndex + 1;
                        i++;
                        continue;
                    }
                    // Consume non-tagged continuation lines that follow a conversation entry
                    // (multi-paragraph responses or plain text between prompts)
                    if (!convPrimaryTag && conversationItems.length > 0) {
                        conversationItems.push(convText);
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
                var tableData = this._cellParser._extractTableData(block.data);
                if (tableData) {
                    result.tableData = tableData;
                    result.detectedPattern = this._cellParser._detectTablePattern(tableData, interactiveType);
                    result.blocksConsumed = i - startIndex + 1;
                    // Check for media in table
                    var tableMedia = this._cellParser._extractMediaFromTable(block.data);
                    result.mediaReferences = result.mediaReferences.concat(tableMedia);
                    // Extract writer instructions from table cells
                    if (block.data.rows) {
                        for (var tblR = 0; tblR < block.data.rows.length; tblR++) {
                            var tblRow = block.data.rows[tblR];
                            for (var tblC = 0; tblC < tblRow.cells.length; tblC++) {
                                var tblCell = tblRow.cells[tblC];
                                for (var tblP = 0; tblP < tblCell.paragraphs.length; tblP++) {
                                    var tblText = this._cellParser._buildFormattedText(tblCell.paragraphs[tblP]);
                                    var tblTagRes = this._normaliser.processBlock(tblText);
                                    if (tblTagRes.redTextInstructions && tblTagRes.redTextInstructions.length > 0) {
                                        result.writerInstructions = result.writerInstructions.concat(tblTagRes.redTextInstructions);
                                    }
                                }
                            }
                        }
                    }
                }
                i++;
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

                // Check for heading/body/styling/media/link tags as boundary.
                // For types that expect sub-tags: only apply boundary check if we
                // already have table data (meaning we found data but no sub-tags —
                // stop consuming). If no data yet, skip boundary to keep looking
                // for sub-tags.
                if (primaryTag && this._isEndBoundary(primaryTag)) {
                    if (!expectsSubTags) {
                        break;
                    }
                    // For expectsSubTags with table data already: stop
                    if (result.tableData && !this._isSubTagFor(primaryTag, interactiveType)) {
                        break;
                    }
                }

                // Check for media references in body text near the interactive
                var mediaRefs = this._cellParser._extractMediaFromText(tagResult.cleanText || '');
                if (mediaRefs.length > 0) {
                    result.mediaReferences = result.mediaReferences.concat(mediaRefs);
                }

                // If this is a block with NO tag and the interactive already
                // has table data, it's probably regular body content — stop
                if (!primaryTag && result.tableData) {
                    break;
                }

                // If this is a block with NO tag and we expect sub-tags, keep
                // looking past untagged instruction text to find them
                if (!primaryTag && !result.tableData && expectsSubTags) {
                    result.blocksConsumed = i - startIndex + 1;
                    i++;
                    continue;
                }

                // For word_highlighter and similar types, capture ALL following
                // plain-text paragraphs as interactive data (Pattern 4 plain text).
                if (!primaryTag && !result.tableData &&
                    (interactiveType === 'word_highlighter' || interactiveType === 'word_select')) {
                    var plainTextContent = (tagResult.cleanText || '').trim();
                    if (plainTextContent) {
                        if (!result.numberedItems) {
                            result.numberedItems = [];
                        }
                        result.numberedItems.push({
                            number: result.numberedItems.length + 1,
                            content: plainTextContent,
                            tag: 'plain_text'
                        });
                        result.detectedPattern = 4;
                        result.blocksConsumed = i - startIndex + 1;
                        i++;
                        continue;
                    }
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

        // dropdown belongs to dropdown_quiz_paragraph (inline position markers)
        if (name === 'dropdown' && interactiveType === 'dropdown_quiz_paragraph') {
            return true;
        }

        // story_heading belongs to dropdown_quiz_paragraph
        if (name === 'story_heading' && interactiveType === 'dropdown_quiz_paragraph') {
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
                    var tableData = this._cellParser._extractTableData(block.data);
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
                var mediaRefs = this._cellParser._extractMediaFromText(content);
                if (block.type === 'paragraph' && block.data) {
                    var fullText = this._cellParser._buildFormattedText(block.data);
                    mediaRefs = mediaRefs.concat(this._cellParser._extractMediaFromText(fullText));
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


    /**
     * Extract writer instructions from a block's red text.
     *
     * @param {Object} block - Content block
     * @returns {Array<string>} Instructions
     */
    _extractBlockInstructions(block) {
        if (block.type !== 'paragraph' || !block.data) return [];
        var text = this._cellParser._buildFormattedText(block.data);
        var tagResult = this._normaliser.processBlock(text);
        return tagResult.redTextInstructions || [];
    }

    // ------------------------------------------------------------------
    // Boundary detection (Session F)
    // ------------------------------------------------------------------

    /**
     * Walk blocks from an interactive-start index and determine the inclusive
     * block range that belongs to the current interactive. Captures child
     * sub-tag blocks, conversation-style paragraphs, red-text writer notes,
     * inline media, and the primary data table — without modifying the
     * existing `_extractData()` output.
     *
     * Close signals (tag NOT consumed):
     *   • `TagNormaliser.isInteractiveEndSignal()` → `body`, H2/H3 (H4/H5
     *     at top level in Session F), `end_page`, `end_activity`, `lesson`,
     *     `alert`, `important`, `whakatauki`, `quote`.
     *   • Another interactive-start tag.
     *   • Any block that does not match a child / writer-note / inline-media /
     *     conversation-paragraph rule.
     *
     * @param {Array<Object>} blocks
     * @param {number} startIndex
     * @param {Object} [tagInfo] - The normalised interactive-start tag record.
     * @param {Object} [context] - Optional `{ inActivity: boolean }`. Threaded
     *   into `TagNormaliser.isInteractiveEndSignal()` so H4/H5 inside an
     *   activity wrapper do not close the inner interactive.
     * @returns {Object}
     */
    _consumeInteractiveBoundary(blocks, startIndex, tagInfo, context) {
        if (!tagInfo) {
            tagInfo = this._getInteractiveTag(blocks[startIndex]);
        }
        var endSignalContext = context || {};

        var result = {
            startBlockIndex: startIndex,
            endBlockIndex: startIndex,
            childBlocks: [],
            conversationEntries: [],
            writerNotes: [],
            associatedMedia: [],
            dataTable: null,
            startBlockInlineContent: null,
            layoutRowSiblings: []
        };

        if (!tagInfo) return result;

        var childTags = tagInfo.interactiveChildTags || [];
        var modifier = (tagInfo.modifier || '').toLowerCase();
        var isConversationStyle = (
            tagInfo.normalised === 'speech_bubble' &&
            modifier.indexOf('conversation') !== -1
        );

        // If the start block is itself a table (e.g., [speech bubble] inside a
        // table cell), treat the table as the primary data table.
        var startBlock = blocks[startIndex];
        if (startBlock && startBlock.type === 'table' && startBlock.data) {
            result.dataTable = startBlock.data;
        }

        // Session H — if the start tag is embedded inline inside a paragraph
        // (e.g. `[speech bubble] Kia ora I'm Ariā...`), capture the remainder
        // of that paragraph's text as part of the interactive's own body so
        // it is not silently dropped by the boundary walker.
        if (startBlock && startBlock.type === 'paragraph' && startBlock.data && tagInfo.raw) {
            var startRaw = this._cellParser._buildFormattedText(startBlock.data);
            var inline = this._stripStartTagFromText(startRaw, tagInfo.raw);
            if (inline) {
                result.startBlockInlineContent = inline;
            }
        }

        // Session H — capture the `_layoutRowId` of the start block so the
        // forward-walk loop can re-pair sibling blocks unwrapped from the
        // same source layout-table row.
        var startLayoutRowId = (startBlock && startBlock._layoutRowId) || null;

        // Track whether any non-start block has been consumed yet — the primary
        // data-table rule only applies when the table sits immediately after
        // the start tag.
        var consumedCount = 0;

        for (var i = startIndex + 1; i < blocks.length; i++) {
            var next = blocks[i];

            // Session H — layout-row sibling capture. Checked BEFORE the
            // end-signal check so a sibling block unwrapped from the same
            // source row is always threaded through the boundary even if it
            // would otherwise have triggered an end-signal (e.g. a plain
            // [image] tag in the companion cell).
            if (startLayoutRowId && next && next._layoutRowId === startLayoutRowId) {
                result.layoutRowSiblings.push({
                    index: i,
                    block: next,
                    layoutRowId: startLayoutRowId
                });
                result.endBlockIndex = i;
                consumedCount++;
                continue;
            }

            // Rule: TABLE immediately after the start-tag captures as dataTable.
            if (next.type === 'table' && consumedCount === 0 && !result.dataTable) {
                result.dataTable = next.data;
                result.endBlockIndex = i;
                consumedCount++;
                continue;
            }

            var nextTagResult = this._getBlockTagResult(next);
            var nextPrimary = (nextTagResult.tags && nextTagResult.tags.length > 0)
                ? nextTagResult.tags[0] : null;

            // Rule: red-text writer instruction — capture into writerNotes.
            // Either the block is pure red text, or it carries red-text
            // instructions alongside no structural tag of its own.
            if (nextTagResult.isRedTextOnly ||
                (nextTagResult.redTextInstructions &&
                 nextTagResult.redTextInstructions.length > 0 &&
                 !nextPrimary)) {
                for (var r = 0; r < nextTagResult.redTextInstructions.length; r++) {
                    result.writerNotes.push(nextTagResult.redTextInstructions[r]);
                }
                result.endBlockIndex = i;
                consumedCount++;
                continue;
            }

            // Rule: child sub-tag belongs inside the current interactive.
            if (nextPrimary && childTags.indexOf(nextPrimary.normalised) !== -1) {
                result.childBlocks.push({
                    index: i,
                    block: next,
                    tag: nextPrimary
                });
                result.endBlockIndex = i;
                consumedCount++;
                continue;
            }

            // Rule: explicit end signal from the normaliser. Pass the activity
            // context so H4 / H5 scaffolding inside an activity does NOT
            // close the inner interactive.
            if (nextPrimary && this._normaliser.isInteractiveEndSignal(nextPrimary, endSignalContext)) {
                break;
            }

            // Rule: another interactive-start tag closes the boundary.
            if (nextPrimary && nextPrimary.isInteractiveStart === true) {
                break;
            }

            // Rule: inline [image]/[video] inside conversation-style or whenever
            // we have already begun consuming child blocks.
            if (nextPrimary &&
                (nextPrimary.normalised === 'image' || nextPrimary.normalised === 'video') &&
                (isConversationStyle || result.childBlocks.length > 0)) {
                var url = (nextTagResult.cleanText || '').trim();
                result.associatedMedia.push({
                    type: nextPrimary.normalised,
                    url: url
                });
                result.endBlockIndex = i;
                consumedCount++;
                continue;
            }

            // Rule: conversation-style — untagged / body-category paragraph
            // (e.g. "Prompt 1: ..." / "AI response: ...") belongs inside.
            if (isConversationStyle &&
                next.type === 'paragraph' &&
                (!nextPrimary || nextPrimary.category === 'body')) {
                var convText = (nextTagResult.cleanText || '').trim();
                if (!convText) {
                    var raw = this._cellParser._buildFormattedText(next.data);
                    raw = raw.replace(
                        /\uD83D\uDD34\[RED TEXT\]\s*[\s\S]*?\s*\[\/RED TEXT\]\uD83D\uDD34/g, ''
                    ).replace(/\[[^\]]+\]/g, '').trim();
                    convText = raw;
                }
                if (convText) {
                    result.conversationEntries.push(convText);
                    result.endBlockIndex = i;
                    consumedCount++;
                    continue;
                }
            }

            // Nothing matched — close boundary at the previous consumed block.
            break;
        }

        return result;
    }

    _getInteractiveTag(block) {
        if (block.type === 'paragraph' && block.data) {
            var text = this._cellParser._buildFormattedText(block.data);
            var tagResult = this._normaliser.processBlock(text);
            if (tagResult.tags) {
                for (var i = 0; i < tagResult.tags.length; i++) {
                    if (tagResult.tags[i].category === 'interactive') {
                        return tagResult.tags[i];
                    }
                }
            }
        }
        if (block.type === 'table' && block.data) {
            var tableText = this._cellParser._buildTableText(block.data);
            var tableTagResult = this._normaliser.processBlock(tableText);
            if (tableTagResult.tags) {
                for (var j = 0; j < tableTagResult.tags.length; j++) {
                    if (tableTagResult.tags[j].category === 'interactive') {
                        return tableTagResult.tags[j];
                    }
                }
            }
        }
        return null;
    }

    _getBlockTagResult(block) {
        if (block.type === 'paragraph' && block.data) {
            var text = this._cellParser._buildFormattedText(block.data);
            return this._normaliser.processBlock(text);
        }
        if (block.type === 'table' && block.data) {
            var tableText = this._cellParser._buildTableText(block.data);
            return this._normaliser.processBlock(tableText);
        }
        return { tags: [], cleanText: '', redTextInstructions: [], isRedTextOnly: false, isWhitespaceOnly: true };
    }

    // Remove one occurrence of `tagRaw` from `rawText`, stripping surrounding
    // red-text markers so an inline-embedded start tag can be subtracted from
    // its paragraph's text even when the tag is wrapped in 🔴[RED TEXT]…🔴.
    _stripStartTagFromText(rawText, tagRaw) {
        if (!rawText || !tagRaw) return '';
        var stripped = rawText
            .replace(/🔴\[RED TEXT\]\s*/g, '')
            .replace(/\s*\[\/RED TEXT\]🔴/g, '');
        var idx = stripped.indexOf(tagRaw);
        if (idx === -1) return '';
        return (stripped.slice(0, idx) + stripped.slice(idx + tagRaw.length)).trim();
    }
}
