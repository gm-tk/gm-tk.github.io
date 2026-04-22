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
        this._cellParser = new InteractiveCellParser(tagNormaliser);
        this._dataExtractor = new InteractiveDataExtractor(tagNormaliser, this._tables, this._cellParser);
        this._renderer = new InteractivePlaceholderRenderer(this._tables, this._cellParser);
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
        var extracted = this._dataExtractor._extractData(contentBlocks, startIndex, interactiveType);

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
        var tagBlockInstructions = this._dataExtractor._extractBlockInstructions(block);
        if (tagBlockInstructions.length > 0) {
            writerInstructions = tagBlockInstructions.concat(writerInstructions);
        }

        // Session F — compute boundary metadata (startBlockIndex / endBlockIndex
        // / childBlocks / conversationEntries / writerNotes / associatedMedia /
        // dataTable). Session G threads `insideActivity` into the boundary so
        // H4 / H5 scaffolding inside an activity does not close the inner
        // interactive. html-converter.js consumes these fields to skip
        // consumed blocks during body rendering.
        var boundary = this._dataExtractor._consumeInteractiveBoundary(
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
            associatedMedia: boundary.associatedMedia || [],
            startBlockInlineContent: boundary.startBlockInlineContent || null,
            layoutRowSiblings: boundary.layoutRowSiblings || []
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
            startBlockInlineContent: boundary.startBlockInlineContent || null,
            layoutRowSiblings: boundary.layoutRowSiblings || [],
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
            dataTable: boundary.dataTable,
            startBlockInlineContent: boundary.startBlockInlineContent || null,
            layoutRowSiblings: boundary.layoutRowSiblings || []
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
                            cbT = this._cellParser._buildFormattedText(cbE.block.data);
                        } else if (cbE.block.type === 'table' && cbE.block.data) {
                            cbT = this._cellParser._buildTableText(cbE.block.data);
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

            // Session I — inline remainder text captured from the start
            // block when the start tag is embedded in a prose paragraph
            // (e.g. `[speech bubble] Kia ora...`).
            if (typeof entry.startBlockInlineContent === 'string' &&
                entry.startBlockInlineContent.length > 0) {
                lines.push('Start-Block Content:');
                lines.push('  ' + entry.startBlockInlineContent);
                lines.push('');
            }

            // Session I — layout-row sibling blocks (companion cells
            // unwrapped from the same 2-column layout-table row). One
            // indented bullet per sibling: paragraph text, optional media
            // URL, and any red-text writer notes the sibling carried.
            if (entry.layoutRowSiblings && entry.layoutRowSiblings.length > 0) {
                lines.push('Layout-Row Siblings (' + entry.layoutRowSiblings.length + '):');
                for (var lsRI = 0; lsRI < entry.layoutRowSiblings.length; lsRI++) {
                    var lsRE = entry.layoutRowSiblings[lsRI];
                    var lsRInfo = this._cellParser._extractSiblingInfo(lsRE.block);
                    var lsRLine = '  - ' + lsRInfo.paragraphText;
                    if (lsRInfo.mediaUrl) {
                        lsRLine += (lsRInfo.paragraphText ? ' ' : '') + lsRInfo.mediaUrl;
                    }
                    lines.push(lsRLine);
                    for (var lsRN = 0; lsRN < lsRInfo.redTextNotes.length; lsRN++) {
                        lines.push('    Note: ' + lsRInfo.redTextNotes[lsRN]);
                    }
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
        // Also check table blocks — interactive tags can appear inside table cells
        // (e.g., [speech bubble] in a table with image + text)
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

    /**
     * Check if a content block has a tag of a given category.
     *
     * @param {Object} block - Content block
     * @param {string} category - Category to check
     * @returns {Object|null} First matching tag or null
     */
    _getBlockTag(block, category) {
        if (block.type === 'paragraph' && block.data) {
            var text = this._cellParser._buildFormattedText(block.data);
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
            var text = this._cellParser._buildFormattedText(block.data);
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
            var text = this._cellParser._buildFormattedText(block.data);
            return this._normaliser.processBlock(text);
        }
        if (block.type === 'table' && block.data) {
            var tableText = this._cellParser._buildTableText(block.data);
            return this._normaliser.processBlock(tableText);
        }
        return { tags: [], cleanText: '', redTextInstructions: [], isRedTextOnly: false, isWhitespaceOnly: true };
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

}
