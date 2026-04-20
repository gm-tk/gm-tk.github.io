/**
 * HtmlConverterBlockProcessor — Tag normalisation + formatted-text build for raw blocks.
 *
 * Extracted from js/html-converter.js as part of the html-converter refactor.
 * See docs/29-html-converter-refactor-plan.md.
 */

'use strict';

class HtmlConverterBlockProcessor {
    constructor(tagNormaliser, coreRef) {
        this._normaliser = tagNormaliser;
        this._coreRef = coreRef;
    }

    _processAllBlocks(blocks) {
        var result = [];

        for (var i = 0; i < blocks.length; i++) {
            var block = blocks[i];
            var processed = this._processBlock(block);
            if (processed) {
                result.push(processed);
            }
        }

        return result;
    }

    /**
     * Process a single content block.
     *
     * @param {Object} block - A content block {type, data}
     * @returns {Object|null} Processed block or null if empty
     */
    _processBlock(block) {
        if (block.type === 'pageBreak') {
            return null;
        }

        if (block.type === 'paragraph' && block.data) {
            var text = this._buildFormattedText(block.data);

            // Detect hovertrigger pattern in formatted text:
            // 🔴[RED TEXT] [hovertrigger: [/RED TEXT]🔴 definition 🔴[RED TEXT] ] [/RED TEXT]🔴
            var hovertriggerData = this._coreRef._extractHovertriggerData(text, block.data);

            var tagResult = this._normaliser.processBlock(text);

            var processed = {
                type: 'paragraph',
                data: block.data,
                formattedText: text,
                tagResult: tagResult,
                cleanText: tagResult.cleanText
            };

            // Attach hovertrigger data if detected
            if (hovertriggerData) {
                processed._hovertriggers = hovertriggerData;
            }

            // Preserve sidebar metadata from layout table unwrapping
            if (block._unwrappedFrom) {
                processed._unwrappedFrom = block._unwrappedFrom;
            }
            if (block._cellRole) {
                processed._cellRole = block._cellRole;
            }
            if (block._sidebarImageUrl !== undefined) {
                processed._sidebarImageUrl = block._sidebarImageUrl;
            }
            if (block._sidebarAlertContent) {
                processed._sidebarAlertContent = block._sidebarAlertContent;
            }
            if (block._sidebarParagraphs) {
                processed._sidebarParagraphs = block._sidebarParagraphs;
            }

            return processed;
        }

        if (block.type === 'table' && block.data) {
            var tableText = this._buildTableTextForTags(block.data);
            var tableTagResult = this._normaliser.processBlock(tableText);

            // Promote interactive tags to primary position (Bug 4 fix):
            // If a table contains an interactive tag (e.g., speech_bubble) in its
            // cells but it's not the primary tag, move it to front so the
            // interactive handler fires.
            if (tableTagResult.tags && tableTagResult.tags.length > 1) {
                var interactiveIdx = -1;
                for (var ti = 0; ti < tableTagResult.tags.length; ti++) {
                    if (tableTagResult.tags[ti].category === 'interactive') {
                        interactiveIdx = ti;
                        break;
                    }
                }
                if (interactiveIdx > 0) {
                    var iTag = tableTagResult.tags.splice(interactiveIdx, 1)[0];
                    tableTagResult.tags.unshift(iTag);
                }
            }

            // Detect implicit click_drop from front/back sub-tags (Bug 2B fix):
            // Tables containing [front] and [back/drop] sub-tags in cells are
            // click_drop interactives even without a preceding [click drop] tag.
            if (tableTagResult.tags) {
                var hasFront = false;
                var hasBack = false;
                var hasInteractive = false;
                for (var ft = 0; ft < tableTagResult.tags.length; ft++) {
                    if (tableTagResult.tags[ft].normalised === 'front') hasFront = true;
                    if (tableTagResult.tags[ft].normalised === 'back') hasBack = true;
                    if (tableTagResult.tags[ft].category === 'interactive') hasInteractive = true;
                }
                if (hasFront && hasBack && !hasInteractive) {
                    tableTagResult.tags.unshift({
                        normalised: 'click_drop',
                        level: null,
                        number: null,
                        id: null,
                        category: 'interactive',
                        modifier: null,
                        raw: '[click_drop]'
                    });
                }
            }

            return {
                type: 'table',
                data: block.data,
                tagResult: tableTagResult
            };
        }

        return null;
    }

    /**
     * Build formatted text from a paragraph's runs (matching formatter output).
     *
     * @param {Object} para - Paragraph data object
     * @returns {string} Formatted text with red text markers and formatting
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

                // Yellow highlight marker (correct answer indicator)
                if (fmt.highlight === 'yellow') {
                    chunk = '\u2705' + chunk;
                }
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
     * Apply formatting markers to text (matching OutputFormatter logic).
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
     * Build text from table for tag extraction.
     *
     * @param {Object} table - Table data object
     * @returns {string} Combined text
     */
    _buildTableTextForTags(table) {
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
}
