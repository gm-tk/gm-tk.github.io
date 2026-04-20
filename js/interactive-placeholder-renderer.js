/**
 * InteractivePlaceholderRenderer — builds the dashed-border HTML placeholder
 * emitted for each detected interactive component.
 *
 * Handles column-class selection, data summary string, content preview body,
 * and the content escaping helper.
 *
 * Extracted from js/interactive-extractor.js as part of the interactive-extractor
 * refactor. See docs/28-interactive-extractor-refactor-plan.md.
 */

'use strict';

class InteractivePlaceholderRenderer {
    constructor(tables, cellParser) {
        this._tables = tables;
        this._cellParser = cellParser;
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
        var tableData = opts.tableData;
        var numberedItems = opts.numberedItems;
        // Session G — additive fields captured by the boundary algorithm.
        // Visual shell (dashed border, tier colours, data table preview) is
        // unchanged; these surface in extra sub-sections only when populated.
        var childBlocks = opts.childBlocks || [];
        var conversationEntries = opts.conversationEntries || [];
        var boundaryWriterNotes = opts.boundaryWriterNotes || [];
        var associatedMedia = opts.associatedMedia || [];

        var typeLabel = type + (modifier ? ' (' + modifier + ')' : '');
        var activityLabel = activityId || 'inline';

        // Colour scheme based on tier
        var borderColor = tier === 1 ? 'green' : 'red';
        var bgColor = tier === 1 ? '#e6f9e6' : '#fde8e8';
        var textColor = tier === 1 ? '#1a7a1a' : '#c0392b';
        var icon = tier === 1 ? '\uD83D\uDD27' : '\u26A0\uFE0F';
        var tierLabel = tier === 1 ? 'TIER 1 INTERACTIVE' : 'INTERACTIVE PLACEHOLDER';

        var lines = [];

        // Opening HTML comment
        lines.push('<!-- ========== INTERACTIVE: ' + typeLabel +
            ' | Activity: ' + activityLabel +
            ' | File: ' + filename + ' ========== -->');

        // Row/col wrapper only when NOT inside an activity
        if (!insideActivity) {
            lines.push('<div class="row">');
            lines.push('  <div class="' + colClass + '">');
        }

        // Container with dashed border
        lines.push('    <div style="border: 2px dashed ' + borderColor + '; padding: 0; margin: 10px 0;">');

        // Header bar
        lines.push('      <div style="background: ' + bgColor + '; color: ' + textColor +
            '; padding: 8px 12px; font-weight: bold; font-size: 0.9em;">');
        lines.push('        ' + icon + ' ' + tierLabel + ': ' + this._escContent(type) +
            ' \u2014 Activity ' + this._escContent(activityLabel));
        lines.push('      </div>');

        // Separator
        lines.push('      <hr style="margin: 0; border-color: ' + borderColor + ';" />');

        // Hidden comment block for data reference
        lines.push('      <!-- INTERACTIVE_START: ' + type + ' -->');
        lines.push('      <!-- Data Pattern: ' + dataPattern + ' -->');
        lines.push('      <!-- Data Summary: ' + dataSummary + ' -->');

        // Content preview body
        lines.push('      <div style="padding: 10px 12px; font-size: 0.85em; color: #333; background: #fafafa;">');

        // Generate content preview based on data pattern and extracted data
        var previewHtml = this._generateContentPreview(dataPattern, tableData, numberedItems, type);
        lines.push(previewHtml);

        // Writer instructions (legacy — extracted by _extractData)
        if (writerInstructions && writerInstructions.length > 0) {
            for (var wi = 0; wi < writerInstructions.length; wi++) {
                lines.push('        <p style="color: #666; font-style: italic; margin-top: 8px;">Writer note: ' +
                    this._escContent(writerInstructions[wi]) + '</p>');
            }
        }

        // Session G — child sub-tag blocks (e.g. flip card [front] / [back]).
        // Render below the table preview to preserve every captured block.
        if (childBlocks.length > 0) {
            lines.push('        <div style="margin-top: 8px; padding-top: 6px; border-top: 1px dashed #ccc;">');
            lines.push('          <p style="font-weight: bold; margin: 4px 0;">Child blocks:</p>');
            for (var cbi = 0; cbi < childBlocks.length; cbi++) {
                var cbEntry = childBlocks[cbi];
                var cbTagName = (cbEntry.tag && cbEntry.tag.normalised) || 'item';
                var cbBlock = cbEntry.block;
                var cbText = '';
                if (cbBlock) {
                    if (cbBlock.type === 'paragraph' && cbBlock.data) {
                        cbText = this._cellParser._buildFormattedText(cbBlock.data);
                    } else if (cbBlock.type === 'table' && cbBlock.data) {
                        cbText = this._cellParser._buildTableText(cbBlock.data);
                    }
                }
                cbText = (cbText || '').replace(
                    /\uD83D\uDD34\[RED TEXT\]\s*[\s\S]*?\s*\[\/RED TEXT\]\uD83D\uDD34/g, ''
                ).replace(/\[[^\]]+\]/g, '').trim();
                lines.push('          <p style="margin: 2px 0;"><strong>[' +
                    this._escContent(cbTagName) + ']</strong> ' +
                    this._escContent(cbText) + '</p>');
            }
            lines.push('        </div>');
        }

        // Session G — conversation entries (speech_bubble Conversation layout).
        if (conversationEntries.length > 0) {
            lines.push('        <div style="margin-top: 8px; padding-top: 6px; border-top: 1px dashed #ccc;">');
            lines.push('          <p style="font-weight: bold; margin: 4px 0;">Conversation entries:</p>');
            for (var cei = 0; cei < conversationEntries.length; cei++) {
                var ceEntry = conversationEntries[cei];
                var ceLabelMatch = (ceEntry || '').match(
                    /^((?:Prompt|AI\s*response|Response|User|Assistant|Human|Student)\s*\d*\s*:)\s*([\s\S]*)/i
                );
                if (ceLabelMatch) {
                    lines.push('          <p style="margin: 2px 0;"><strong>' +
                        this._escContent(ceLabelMatch[1]) + '</strong> ' +
                        this._escContent(ceLabelMatch[2]) + '</p>');
                } else {
                    lines.push('          <p style="margin: 2px 0;">' +
                        this._escContent(ceEntry) + '</p>');
                }
            }
            lines.push('        </div>');
        }

        // Session G — writer notes captured INSIDE the boundary (red text).
        // De-duplicated against the legacy writerInstructions list above so the
        // same note isn't repeated.
        if (boundaryWriterNotes.length > 0) {
            var seenNotes = {};
            if (writerInstructions) {
                for (var swi = 0; swi < writerInstructions.length; swi++) {
                    seenNotes[(writerInstructions[swi] || '').trim()] = true;
                }
            }
            var pendingNotes = [];
            for (var bwn = 0; bwn < boundaryWriterNotes.length; bwn++) {
                var bwnText = (boundaryWriterNotes[bwn] || '').trim();
                if (!bwnText || seenNotes[bwnText]) continue;
                seenNotes[bwnText] = true;
                pendingNotes.push(bwnText);
            }
            for (var pwn = 0; pwn < pendingNotes.length; pwn++) {
                lines.push('        <p style="color: #666; font-style: italic; margin-top: 8px;">Writer note: ' +
                    this._escContent(pendingNotes[pwn]) + '</p>');
            }
        }

        // Session G — associated media URLs (inline [image] / [video]).
        if (associatedMedia.length > 0) {
            lines.push('        <div style="margin-top: 8px; padding-top: 6px; border-top: 1px dashed #ccc;">');
            lines.push('          <p style="font-weight: bold; margin: 4px 0;">Associated media:</p>');
            for (var ami = 0; ami < associatedMedia.length; ami++) {
                var amEntry = associatedMedia[ami];
                lines.push('          <p style="margin: 2px 0;">' +
                    this._escContent(amEntry.type) + ': ' +
                    this._escContent(amEntry.url) + '</p>');
            }
            lines.push('        </div>');
        }

        lines.push('      </div>');
        lines.push('      <!-- INTERACTIVE_END: ' + type + ' -->');
        lines.push('    </div>');

        if (!insideActivity) {
            lines.push('  </div>');
            lines.push('</div>');
        }

        // Closing HTML comment
        lines.push('<!-- ========== END INTERACTIVE: ' + type + ' ========== -->');

        return lines.join('\n');
    }

    /**
     * Generate content preview HTML for the placeholder body.
     *
     * @param {number} dataPattern - Data pattern number
     * @param {Object|null} tableData - Extracted table data
     * @param {Array|null} numberedItems - Extracted numbered items
     * @param {string} type - Interactive type
     * @returns {string} HTML preview content
     */
    _generateContentPreview(dataPattern, tableData, numberedItems, type) {
        var lines = [];

        // Dropdown quiz paragraph: show story text + table together
        if (type === 'dropdown_quiz_paragraph' && numberedItems && numberedItems.length > 0) {
            // Delegate to the numbered items branch which handles pattern 4 + tableData
            // Fall through intentionally (skip the tableData-only branch)
        } else if (tableData) {
            // Table-based data patterns (1, 2, 3, 8, 10, 11, 12, 13)
            var dims = tableData.dimensions || 'unknown';
            if (dataPattern === 2) {
                lines.push('        <p><em>Data: Front/Back (' + dims + ')</em></p>');
            } else if (dataPattern === 3) {
                lines.push('        <p><em>Data: Hint Slider (' + dims + ')</em></p>');
            } else if (dataPattern === 8) {
                lines.push('        <p><em>Data: Speech Bubble (character + image)</em></p>');
            } else if (dataPattern === 10) {
                lines.push('        <p><em>Data: Word Select (' + dims + ')</em></p>');
            } else {
                lines.push('        <p><em>Data: Table (' + dims + ')</em></p>');
            }

            // Render table preview (max 5 rows)
            lines.push('        <table style="width:100%; border-collapse: collapse; font-size: 0.85em; margin-top: 6px;">');
            if (tableData.headers && tableData.headers.length > 0) {
                lines.push('          <tr>');
                for (var h = 0; h < tableData.headers.length; h++) {
                    lines.push('            <td style="border:1px solid #ccc; padding:4px; font-weight:bold;">' +
                        this._escContent(tableData.headers[h]) + '</td>');
                }
                lines.push('          </tr>');
            }
            if (tableData.rows) {
                var maxRows = Math.min(tableData.rows.length, 5);
                for (var r = 0; r < maxRows; r++) {
                    lines.push('          <tr>');
                    for (var c = 0; c < tableData.rows[r].length; c++) {
                        lines.push('            <td style="border:1px solid #ccc; padding:4px;">' +
                            this._escContent(tableData.rows[r][c]) + '</td>');
                    }
                    lines.push('          </tr>');
                }
                if (tableData.rows.length > 5) {
                    lines.push('          <tr><td colspan="' + (tableData.headers ? tableData.headers.length : 1) +
                        '" style="border:1px solid #ccc; padding:4px; text-align:center; font-style:italic;">... and ' +
                        (tableData.rows.length - 5) + ' more rows</td></tr>');
                }
            }
            lines.push('        </table>');
        } else if (numberedItems && numberedItems.length > 0) {
            // Numbered items patterns (4, 5, 6, 7, 9)
            // Dropdown quiz paragraph (Pattern 4) — special compound preview
            if (dataPattern === 4 && type === 'dropdown_quiz_paragraph') {
                var dqpDropdowns = 0;
                for (var di = 0; di < numberedItems.length; di++) {
                    var dItem = numberedItems[di];
                    var ddMatches = (dItem.content || '').match(/\[(?:drop\s*down|dropdown)\s*\d+\]/gi);
                    if (ddMatches) dqpDropdowns += ddMatches.length;
                }
                lines.push('        <p><em>Data: Dropdown Quiz Paragraph (' + dqpDropdowns + ' dropdowns)</em></p>');
                for (var dpi = 0; dpi < numberedItems.length; dpi++) {
                    var dpItem = numberedItems[dpi];
                    if (dpItem.tag === 'story_heading') {
                        lines.push('        <p><strong>Title:</strong> <em>' +
                            this._escContent(dpItem.content) + '</em></p>');
                    } else {
                        // Render story paragraph with [Dropdown N] markers bolded
                        var storyText = this._escContent(dpItem.content);
                        storyText = storyText.replace(/\[(?:drop\s*down|dropdown)\s*(\d+)\]/gi,
                            '<strong>[Dropdown $1]</strong>');
                        lines.push('        <p>' + storyText + '</p>');
                    }
                }
                // Also show table data if available
                if (tableData) {
                    lines.push('        <hr style="margin: 8px 0; border-color: #ddd;" />');
                    lines.push('        <p><em>Dropdown options:</em></p>');
                    lines.push('        <table style="width:100%; border-collapse: collapse; font-size: 0.85em;">');
                    if (tableData.headers && tableData.headers.length > 0) {
                        lines.push('          <tr>');
                        for (var dh = 0; dh < tableData.headers.length; dh++) {
                            lines.push('            <td style="border:1px solid #ccc; padding:4px; font-weight:bold;">' +
                                this._escContent(tableData.headers[dh]) + '</td>');
                        }
                        lines.push('          </tr>');
                    }
                    if (tableData.rows) {
                        for (var dr = 0; dr < tableData.rows.length; dr++) {
                            lines.push('          <tr>');
                            for (var dc = 0; dc < tableData.rows[dr].length; dc++) {
                                lines.push('            <td style="border:1px solid #ccc; padding:4px;">' +
                                    this._escContent(tableData.rows[dr][dc]) + '</td>');
                            }
                            lines.push('          </tr>');
                        }
                    }
                    lines.push('        </table>');
                }
            } else if (dataPattern === 9) {
                lines.push('        <p><em>Data: Conversation layout (' + numberedItems.length + ' entries)</em></p>');
                lines.push('        <table style="width:100%; border-collapse: collapse; font-size: 0.85em; margin-top: 6px;">');
                for (var ci = 0; ci < numberedItems.length; ci++) {
                    var convItem = numberedItems[ci];
                    var convContent = convItem.content || '';
                    // Try to split "Prompt N: text" and "AI response: text" for label/content columns
                    var convLabelMatch = convContent.match(/^((?:Prompt|AI\s*response|Response|User|Assistant|Human|Student)\s*\d*\s*:)\s*([\s\S]*)/i);
                    if (convLabelMatch) {
                        lines.push('          <tr>');
                        lines.push('            <td style="border:1px solid #ccc; padding:4px; font-weight:bold; white-space:nowrap; vertical-align:top;">' +
                            this._escContent(convLabelMatch[1]) + '</td>');
                        lines.push('            <td style="border:1px solid #ccc; padding:4px;">' +
                            this._escContent(convLabelMatch[2]) + '</td>');
                        lines.push('          </tr>');
                    } else {
                        lines.push('          <tr>');
                        lines.push('            <td colspan="2" style="border:1px solid #ccc; padding:4px;">' +
                            this._escContent(convContent) + '</td>');
                        lines.push('          </tr>');
                    }
                }
                lines.push('        </table>');
            } else if (dataPattern === 2) {
                // Front/back numbered items (flip cards, click drops)
                var cardCount = 0;
                for (var fi = 0; fi < numberedItems.length; fi++) {
                    if (numberedItems[fi].tag === 'flip_card' || numberedItems[fi].tag === 'carousel_slide') {
                        cardCount++;
                    }
                }
                if (cardCount === 0) cardCount = Math.ceil(numberedItems.length / 3);
                lines.push('        <p><em>Data: ' + cardCount + ' cards \u2014 Front/Back</em></p>');
                for (var ni = 0; ni < numberedItems.length; ni++) {
                    var nItem = numberedItems[ni];
                    var itemLabel = nItem.tag || 'Item';
                    var itemNum = nItem.number || (ni + 1);
                    var itemText = (nItem.content || '').substring(0, 150);
                    lines.push('        <p><strong>' + this._escContent(itemLabel) + ' ' + itemNum +
                        ':</strong> ' + this._escContent(itemText) + '</p>');
                }
            } else {
                var patternLabel = this._tables.patternNames[dataPattern] || 'items';
                lines.push('        <p><em>Data: ' + numberedItems.length + ' ' + patternLabel.toLowerCase() + '</em></p>');
                for (var pi = 0; pi < numberedItems.length; pi++) {
                    var pItem = numberedItems[pi];
                    var pLabel = pItem.tag || 'Item';
                    var pNum = pItem.number || (pi + 1);
                    var pText = (pItem.content || '').substring(0, 150);
                    lines.push('        <p><strong>' + this._escContent(pLabel) + ' ' + pNum +
                        ':</strong> ' + this._escContent(pText) + '</p>');
                }
            }
        } else {
            lines.push('        <p><em>No structured data detected \u2014 check InteractiveExtractor boundary detection</em></p>');
        }

        return lines.join('\n');
    }

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
}
