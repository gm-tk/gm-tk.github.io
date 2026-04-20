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

        this._tables = new InteractiveExtractorTables();
        this._renderer = new InteractivePlaceholderRenderer(this._tables, this);
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
        var tier = this._tables.TIER_1_TYPES.indexOf(interactiveType) !== -1 ? 1 : 2;

        // Look ahead to extract associated data
        var extracted = this._extractData(contentBlocks, startIndex, interactiveType);

        // Determine data pattern
        var dataPattern = extracted.detectedPattern ||
            this._tables.typeToPrimaryPattern[interactiveType] || 1;
        var dataPatternName = this._tables.patternNames[dataPattern] || 'Unknown';

        // Build position context
        var positionContext = this._buildPositionContext(contentBlocks, startIndex);

        // Determine column class
        var colClass = this._renderer._getColumnClass(interactiveType, modifier, extracted);

        // Build data summary string
        var dataSummary = this._renderer._buildDataSummary(extracted);

        // Collect writer instructions
        var writerInstructions = extracted.writerInstructions || [];
        // Also check the tag block itself for instructions
        var tagBlockInstructions = this._extractBlockInstructions(block);
        if (tagBlockInstructions.length > 0) {
            writerInstructions = tagBlockInstructions.concat(writerInstructions);
        }

        // Session F — compute boundary metadata (startBlockIndex / endBlockIndex
        // / childBlocks / conversationEntries / writerNotes / associatedMedia /
        // dataTable). Session G threads `insideActivity` into the boundary so
        // H4 / H5 scaffolding inside an activity does not close the inner
        // interactive. html-converter.js consumes these fields to skip
        // consumed blocks during body rendering.
        var boundary = this._consumeInteractiveBoundary(
            contentBlocks, startIndex, tagInfo, { inActivity: insideActivity === true }
        );

        // Build placeholder HTML (with data preview — Part B redesign).
        // Session G — placeholder fidelity: thread captured childBlocks /
        // conversationEntries / writerNotes / associatedMedia / dataTable
        // from the boundary into the renderer so every consumed block
        // appears INSIDE the placeholder shell (visual shell unchanged).
        var placeholderHtml = this._renderer._generatePlaceholderHtml({
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
            insideActivity: insideActivity,
            tableData: extracted.tableData || boundary.dataTable || null,
            numberedItems: extracted.numberedItems || null,
            childBlocks: boundary.childBlocks || [],
            conversationEntries: boundary.conversationEntries || [],
            boundaryWriterNotes: boundary.writerNotes || [],
            associatedMedia: boundary.associatedMedia || []
        });

        // Build reference entry. Session G — surface the new boundary
        // captures so generateReferenceDocument() can include them.
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
            tableData: extracted.tableData || boundary.dataTable || null,
            listData: extracted.listData || null,
            numberedItems: extracted.numberedItems || null,
            activityHeading: extracted.activityHeading || null,
            activityInstructions: extracted.activityInstructions || null,
            writerInstructions: writerInstructions,
            mediaReferences: extracted.mediaReferences || [],
            redFlags: extracted.redFlags || [],
            childBlocks: boundary.childBlocks || [],
            conversationEntries: boundary.conversationEntries || [],
            boundaryWriterNotes: boundary.writerNotes || [],
            associatedMedia: boundary.associatedMedia || [],
            notes: ''
        };

        return {
            placeholderHtml: placeholderHtml,
            referenceEntry: referenceEntry,
            blocksConsumed: extracted.blocksConsumed,
            interactiveType: interactiveType,
            dataPattern: dataPattern,
            startBlockIndex: boundary.startBlockIndex,
            endBlockIndex: boundary.endBlockIndex,
            childBlocks: boundary.childBlocks,
            conversationEntries: boundary.conversationEntries,
            writerNotes: boundary.writerNotes,
            associatedMedia: boundary.associatedMedia,
            dataTable: boundary.dataTable
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
        lines.push('Generated by PageForge');
        lines.push('=====================================');
        lines.push('');
        lines.push('TOTAL INTERACTIVES: ' + total);
        lines.push('  Tier 1 (rendered by PageForge): ' + tier1Count +
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
                (entry.tier === 1 ? 'Rendered by PageForge' : 'Requires implementation'));
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

            // Media references — combine legacy mediaReferences with the
            // Session G boundary-captured `associatedMedia` list, dedup by
            // type+url. Section header is preserved for downstream parsers.
            var mediaKeys = {};
            var mediaCombined = [];
            if (entry.mediaReferences) {
                for (var mr = 0; mr < entry.mediaReferences.length; mr++) {
                    var mref = entry.mediaReferences[mr];
                    var mk = (mref.type || '') + '::' + (mref.url || '');
                    if (mediaKeys[mk]) continue;
                    mediaKeys[mk] = true;
                    mediaCombined.push(mref);
                }
            }
            if (entry.associatedMedia) {
                for (var am = 0; am < entry.associatedMedia.length; am++) {
                    var amref = entry.associatedMedia[am];
                    var amk = (amref.type || '') + '::' + (amref.url || '');
                    if (mediaKeys[amk]) continue;
                    mediaKeys[amk] = true;
                    mediaCombined.push(amref);
                }
            }
            if (mediaCombined.length > 0) {
                lines.push('Associated Media:');
                for (var mi = 0; mi < mediaCombined.length; mi++) {
                    var media = mediaCombined[mi];
                    lines.push('  ' + media.type + ': ' + media.url);
                }
            } else {
                lines.push('Associated Media: None');
            }
            lines.push('');

            // Session G — child sub-tag blocks captured by the boundary
            // (e.g. flip card [front] / [back] entries). Additive sub-section
            // inside the existing entry block; top-level structure unchanged.
            if (entry.childBlocks && entry.childBlocks.length > 0) {
                lines.push('Child Blocks (' + entry.childBlocks.length + '):');
                for (var cbI = 0; cbI < entry.childBlocks.length; cbI++) {
                    var cbE = entry.childBlocks[cbI];
                    var cbN = (cbE.tag && cbE.tag.normalised) || 'item';
                    var cbT = '';
                    if (cbE.block) {
                        if (cbE.block.type === 'paragraph' && cbE.block.data) {
                            cbT = this._buildFormattedText(cbE.block.data);
                        } else if (cbE.block.type === 'table' && cbE.block.data) {
                            cbT = this._buildTableText(cbE.block.data);
                        }
                    }
                    cbT = (cbT || '').replace(
                        /\uD83D\uDD34\[RED TEXT\]\s*[\s\S]*?\s*\[\/RED TEXT\]\uD83D\uDD34/g, ''
                    ).replace(/\[[^\]]+\]/g, '').trim();
                    lines.push('  [' + cbN + '] ' + cbT);
                }
                lines.push('');
            }

            // Session G — conversation entries (speech_bubble Conversation
            // layout) preserved in order with speaker labels intact.
            if (entry.conversationEntries && entry.conversationEntries.length > 0) {
                lines.push('Conversation Entries (' + entry.conversationEntries.length + '):');
                for (var ceI = 0; ceI < entry.conversationEntries.length; ceI++) {
                    lines.push('  ' + (ceI + 1) + '. ' + entry.conversationEntries[ceI]);
                }
                lines.push('');
            }

            // Session G — boundary writer notes (red-text instructions
            // captured INSIDE the interactive boundary). Dedup against the
            // legacy Writer Instructions section above.
            if (entry.boundaryWriterNotes && entry.boundaryWriterNotes.length > 0) {
                var seenWN = {};
                if (entry.writerInstructions) {
                    for (var swI = 0; swI < entry.writerInstructions.length; swI++) {
                        seenWN[(entry.writerInstructions[swI] || '').trim()] = true;
                    }
                }
                var freshWN = [];
                for (var bwI = 0; bwI < entry.boundaryWriterNotes.length; bwI++) {
                    var bwT = (entry.boundaryWriterNotes[bwI] || '').trim();
                    if (!bwT || seenWN[bwT]) continue;
                    seenWN[bwT] = true;
                    freshWN.push(bwT);
                }
                if (freshWN.length > 0) {
                    lines.push('Boundary Writer Notes:');
                    for (var fwI = 0; fwI < freshWN.length; fwI++) {
                        lines.push('  - ' + freshWN[fwI]);
                    }
                    lines.push('');
                }
            }

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
        // Also check table blocks — interactive tags can appear inside table cells
        // (e.g., [speech bubble] in a table with image + text)
        if (block.type === 'table' && block.data) {
            var tableText = this._buildTableText(block.data);
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

        // If the interactive tag block itself is a table (e.g., speech bubble in table row
        // with image + text), extract the table data from it directly.
        var tagBlock = blocks[startIndex];
        if (tagBlock.type === 'table' && tagBlock.data) {
            var tagTableData = this._extractTableData(tagBlock.data);
            if (tagTableData) {
                result.tableData = tagTableData;
                result.detectedPattern = this._detectTablePattern(tagTableData, interactiveType);
                // Extract media from the table
                var tagTableMedia = this._extractMediaFromTable(tagBlock.data);
                result.mediaReferences = result.mediaReferences.concat(tagTableMedia);
            }
            // Extract writer instructions from table cells
            if (tagBlock.data.rows) {
                for (var tr = 0; tr < tagBlock.data.rows.length; tr++) {
                    var tRow = tagBlock.data.rows[tr];
                    for (var tc = 0; tc < tRow.cells.length; tc++) {
                        var tCell = tRow.cells[tc];
                        for (var tp = 0; tp < tCell.paragraphs.length; tp++) {
                            var tText = this._buildFormattedText(tCell.paragraphs[tp]);
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
                    var dqpTableData = this._extractTableData(dqpBlock.data);
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
                    var dqpText = this._buildFormattedText(dqpBlock.data);
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
                        var rawConvText = this._buildFormattedText(convBlock.data);
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
                var tableData = this._extractTableData(block.data);
                if (tableData) {
                    result.tableData = tableData;
                    result.detectedPattern = this._detectTablePattern(tableData, interactiveType);
                    result.blocksConsumed = i - startIndex + 1;
                    // Check for media in table
                    var tableMedia = this._extractMediaFromTable(block.data);
                    result.mediaReferences = result.mediaReferences.concat(tableMedia);
                    // Extract writer instructions from table cells
                    if (block.data.rows) {
                        for (var tblR = 0; tblR < block.data.rows.length; tblR++) {
                            var tblRow = block.data.rows[tblR];
                            for (var tblC = 0; tblC < tblRow.cells.length; tblC++) {
                                var tblCell = tblRow.cells[tblC];
                                for (var tblP = 0; tblP < tblCell.paragraphs.length; tblP++) {
                                    var tblText = this._buildFormattedText(tblCell.paragraphs[tblP]);
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
                var mediaRefs = this._extractMediaFromText(tagResult.cleanText || '');
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

            // Preserve [IMAGE: filename] references that were stripped by cleanText
            var imageRefs = text.match(/\[IMAGE:\s*[^\]]+\]/gi);
            if (imageRefs) {
                var imageRefStr = imageRefs.join(' ');
                clean = clean ? imageRefStr + ' ' + clean : imageRefStr;
            }

            // Preserve short red-text content descriptors (1-5 words) that are
            // NOT writer instructions. These are content labels like "Blue paint
            // swatch" used in drag-and-drop targets.
            if (!clean.trim() && tagResult.redTextInstructions && tagResult.redTextInstructions.length > 0) {
                for (var ri = 0; ri < tagResult.redTextInstructions.length; ri++) {
                    var instruction = tagResult.redTextInstructions[ri].trim();
                    // Remove any square bracket tags from the instruction
                    instruction = instruction.replace(/\[[^\]]*\]/g, '').trim();
                    if (!instruction) continue;
                    var wordCount = instruction.split(/\s+/).length;
                    // Short phrases (1-5 words) without instruction verbs are content labels
                    var isInstruction = /\b(please|can you|make|add|use|have|ensure|note|check|verify|remove|delete|insert|should|must|need)\b/i.test(instruction);
                    if (wordCount <= 5 && !isInstruction) {
                        clean = instruction;
                        break;
                    }
                }
            }

            if (clean.trim()) {
                parts.push(clean.trim());
            }
        }

        return parts.join(' / ');
    }

    /**
     * Extract text from a table cell with extra noise filtering.
     * Strips CS instructions, tag markers, and formatting artifacts,
     * keeping only meaningful body text and URLs.
     *
     * Used for speech bubble and similar interactives where cells may
     * contain extra writer notes alongside actual content.
     *
     * @param {Object} cell - Cell data
     * @returns {Object} { text, urls, hasImageTag, hasSpeechBubbleTag }
     */
    _extractCellContentClean(cell) {
        if (!cell.paragraphs || cell.paragraphs.length === 0) {
            return { text: '', urls: [], hasImageTag: false, hasSpeechBubbleTag: false };
        }

        var textParts = [];
        var urls = [];
        var hasImageTag = false;
        var hasSpeechBubbleTag = false;

        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            var rawText = this._buildFormattedText(para);
            var tagResult = this._normaliser.processBlock(rawText);

            // Check for image/speech bubble tags
            if (tagResult.tags) {
                for (var t = 0; t < tagResult.tags.length; t++) {
                    if (tagResult.tags[t].normalised === 'image') hasImageTag = true;
                    if (tagResult.tags[t].normalised === 'speech_bubble') hasSpeechBubbleTag = true;
                }
            }

            // Extract URLs from the full text (before stripping)
            var urlRegex = /https?:\/\/[^\s\]]+/g;
            var urlMatch;
            while ((urlMatch = urlRegex.exec(rawText)) !== null) {
                urls.push(urlMatch[0]);
            }

            // Keep clean text (with tags and red text stripped)
            var clean = (tagResult.cleanText || '').trim();
            // Also strip URLs from clean text (we track them separately)
            clean = clean.replace(/https?:\/\/[^\s]+/g, '').trim();
            if (clean) {
                textParts.push(clean);
            }
        }

        return {
            text: textParts.join(' / '),
            urls: urls,
            hasImageTag: hasImageTag,
            hasSpeechBubbleTag: hasSpeechBubbleTag
        };
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

        // Reassemble fragmented red-text tags (Bug 1 fix — Round 3C)
        text = this._normaliser.reassembleFragmentedTags(text);

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
            var patternLabel = this._tables.patternNames[entry.dataPattern] || 'items';
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
            dataTable: null
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

        // Track whether any non-start block has been consumed yet — the primary
        // data-table rule only applies when the table sits immediately after
        // the start tag.
        var consumedCount = 0;

        for (var i = startIndex + 1; i < blocks.length; i++) {
            var next = blocks[i];

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
                    var raw = this._buildFormattedText(next.data);
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
}
