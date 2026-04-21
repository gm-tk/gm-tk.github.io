/**
 * LayoutTableUnwrapper — Detects and unwraps layout tables in the content stream.
 *
 * Writers frequently use Word tables as two-column layout grids (e.g., main content
 * in one column, companion image in the other). When parsed, these tables trap
 * structural content (activities, body text, interactives) inside table cells,
 * preventing the main pipeline from processing them.
 *
 * This module detects layout tables and unwraps them: extracting the cell content
 * and re-inserting it into the main content stream at the table's original position.
 * Sidebar content (images, alerts) is annotated for the HTML converter.
 *
 * Must run BEFORE: tag normalisation, block scoping, page boundary, HTML conversion.
 *
 * @see CLAUDE.md Section 13 — Future Architecture
 */

'use strict';

class LayoutTableUnwrapper {
    /**
     * Create a LayoutTableUnwrapper instance.
     *
     * @param {TagNormaliser} tagNormaliser - An initialised TagNormaliser instance
     */
    constructor(tagNormaliser) {
        if (!tagNormaliser) {
            throw new Error('LayoutTableUnwrapper requires a TagNormaliser instance');
        }

        /** @type {TagNormaliser} */
        this._normaliser = tagNormaliser;

        /** @type {number} Number of layout tables unwrapped in last run */
        this.unwrappedCount = 0;

        /** @type {number} Number of data tables preserved in last run */
        this.preservedCount = 0;
        this._counter = 0;
    }

    // ------------------------------------------------------------------
    // Public API
    // ------------------------------------------------------------------

    /**
     * Process the content array, detecting and unwrapping layout tables.
     * Modifies the content array in-place.
     *
     * @param {Array<Object>} contentBlocks - The content blocks array from DocxParser
     * @param {number} [startIndex=0] - Index to start processing from (e.g., contentStartIndex)
     * @returns {Array<Object>} The modified content array (same reference, modified in-place)
     */
    unwrapLayoutTables(contentBlocks, startIndex) {
        startIndex = startIndex || 0;
        this.unwrappedCount = 0;
        this.preservedCount = 0;

        var i = startIndex;
        while (i < contentBlocks.length) {
            var block = contentBlocks[i];

            if (block.type !== 'table' || !block.data) {
                i++;
                continue;
            }

            // Check contextual override: is this table preceded by an interactive type tag?
            if (this._shouldOverrideAsDataTable(contentBlocks, i)) {
                this.preservedCount++;
                i++;
                continue;
            }

            // Run layout table detection
            if (this.isLayoutTable(block.data)) {
                // Unwrap: extract cell content and replace the table in the stream
                var replacement = this._unwrapTable(block.data);

                // Splice: remove the table, insert the replacement blocks
                var args = [i, 1].concat(replacement);
                Array.prototype.splice.apply(contentBlocks, args);

                this.unwrappedCount++;

                // Advance past the inserted blocks
                i += replacement.length;
            } else {
                this.preservedCount++;
                i++;
            }
        }

        return contentBlocks;
    }

    /**
     * Detect whether a table is a layout table (used by writers as a two-column
     * design grid containing structural/instructional tags).
     *
     * @param {Object} tableData - Raw table data { rows: [{ cells: [{ paragraphs: [...] }] }] }
     * @returns {boolean} True if the table is a layout table
     */
    isLayoutTable(tableData) {
        if (!tableData || !tableData.rows || tableData.rows.length === 0) {
            return false;
        }

        var hasActivityTag = false;
        var hasInteractiveTypeTag = false;
        var cellsWithStructuralTags = 0;
        var totalStructuralTagCount = 0;

        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            if (!row.cells) continue;

            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                var cellTags = this._getCellStructuralTags(cell);

                if (cellTags.hasActivity) {
                    hasActivityTag = true;
                }
                if (cellTags.hasInteractive) {
                    hasInteractiveTypeTag = true;
                }
                if (cellTags.structuralCount > 0) {
                    cellsWithStructuralTags++;
                    totalStructuralTagCount += cellTags.structuralCount;
                }
            }
        }

        // Immediate: any activity or interactive type tag = layout table
        if (hasActivityTag || hasInteractiveTypeTag) {
            return true;
        }

        // Threshold: at least 1 cell with structural tags and 2+ total structural tags
        if (cellsWithStructuralTags >= 1 && totalStructuralTagCount >= 2) {
            return true;
        }

        return false;
    }

    // ------------------------------------------------------------------
    // Internal: Structural tag detection in cells
    // ------------------------------------------------------------------

    /**
     * Analyse a table cell for structural tags.
     *
     * @param {Object} cell - Cell data { paragraphs: [...] }
     * @returns {Object} { hasActivity, hasInteractive, hasContent, hasUI, structuralCount }
     */
    _getCellStructuralTags(cell) {
        var result = {
            hasActivity: false,
            hasInteractive: false,
            hasContent: false,
            hasUI: false,
            structuralCount: 0
        };

        if (!cell || !cell.paragraphs) return result;

        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            var text = this._buildFormattedText(para);
            var tags = this._extractTagsFromText(text);

            for (var t = 0; t < tags.length; t++) {
                var tag = tags[t];

                // Activity & structural tags (high confidence)
                if (/^activity\s/i.test(tag) || /^activity$/i.test(tag) ||
                    /^activity\s*heading/i.test(tag) || /^activity\s*title/i.test(tag)) {
                    result.hasActivity = true;
                    result.structuralCount++;
                    continue;
                }

                // End page / end lesson / lesson content / lesson
                if (/^end\s*page$/i.test(tag) || /^end\s*lesson$/i.test(tag) ||
                    /^lesson\s*content$/i.test(tag) || /^lesson$/i.test(tag) ||
                    /^lesson\s+\d/i.test(tag)) {
                    result.hasActivity = true; // Treat as high-confidence structural
                    result.structuralCount++;
                    continue;
                }

                // Interactive type tags (high confidence)
                if (/^multichoice/i.test(tag) || /^multi\s*choice/i.test(tag) ||
                    /^drag\s*and\s*drop/i.test(tag) || /^drag\s*&\s*drop/i.test(tag) ||
                    /^word\s*(?:highlighter|select)/i.test(tag) ||
                    /^flip\s*card/i.test(tag) || /^flipcard/i.test(tag) ||
                    /^accordion/i.test(tag) ||
                    /^hint\s*slider/i.test(tag) || /^hintslider/i.test(tag) ||
                    /^carousel/i.test(tag) || /^slide\s*show/i.test(tag) || /^slideshow/i.test(tag) ||
                    /^click\s*drop/i.test(tag) || /^clickdrop/i.test(tag) ||
                    /^drop\s*down\s*quiz/i.test(tag) || /^dropdown\s*quiz/i.test(tag) || /^dropquiz/i.test(tag) ||
                    /^speech\s*bubble/i.test(tag) ||
                    /^tabs$/i.test(tag) ||
                    /^typing\s*(?:self[- ]check|quiz)/i.test(tag) ||
                    /^self[- ]?check$/i.test(tag) ||
                    /^mcq$/i.test(tag) ||
                    /^radio\s*quiz/i.test(tag) || /^true\s*false/i.test(tag) ||
                    /^reorder$/i.test(tag) ||
                    /^memory\s*game/i.test(tag) ||
                    /^word\s*drag/i.test(tag) ||
                    /^checklist$/i.test(tag) ||
                    /^timeline$/i.test(tag) ||
                    /^crossword$/i.test(tag) ||
                    /^puzzle$/i.test(tag) ||
                    /^bingo$/i.test(tag)) {
                    result.hasInteractive = true;
                    result.structuralCount++;
                    continue;
                }

                // Body & heading tags (medium confidence)
                if (/^body$/i.test(tag) || /^body\s+text$/i.test(tag) ||
                    /^H[2-5]$/i.test(tag)) {
                    result.hasContent = true;
                    result.structuralCount++;
                    continue;
                }

                // UI element tags (medium confidence)
                if (/^button$/i.test(tag) ||
                    /^modal$/i.test(tag) || /^modal\s*button$/i.test(tag) ||
                    /^alert$/i.test(tag) || /^important$/i.test(tag) ||
                    /^go\s*to\s*journal$/i.test(tag) ||
                    /^upload\s*to\s*dropbox$/i.test(tag) ||
                    /^external\s*link/i.test(tag) ||
                    /^engagement\s*quiz\s*button$/i.test(tag) ||
                    /^supervisor\s*button$/i.test(tag)) {
                    result.hasUI = true;
                    result.structuralCount++;
                    continue;
                }
            }
        }

        return result;
    }

    /**
     * Extract square-bracket tag names from formatted text (inside red text markers).
     *
     * @param {string} text - Formatted text possibly containing red text markers
     * @returns {Array<string>} Tag names found (without brackets)
     */
    _extractTagsFromText(text) {
        if (!text) return [];

        var tags = [];
        // Match tags inside red text markers: 🔴[RED TEXT] [tag name] [/RED TEXT]🔴
        var redTextPattern = /\uD83D\uDD34\[RED TEXT\]\s*(.*?)\s*\[\/RED TEXT\]\uD83D\uDD34/g;
        var match;

        while ((match = redTextPattern.exec(text)) !== null) {
            var content = match[1];
            // Extract square-bracket tags from the red text content
            var tagPattern = /\[([^\]]+)\]/g;
            var tagMatch;
            while ((tagMatch = tagPattern.exec(content)) !== null) {
                var tagName = tagMatch[1].trim();
                if (tagName && tagName !== '/RED TEXT' && tagName !== 'RED TEXT') {
                    tags.push(tagName);
                }
            }
        }

        // Also check for square-bracket tags in non-red text (some writers don't use red)
        var plainTagPattern = /\[([^\]]+)\]/g;
        while ((match = plainTagPattern.exec(text)) !== null) {
            var plainTag = match[1].trim();
            // Skip red text marker fragments
            if (plainTag === 'RED TEXT' || plainTag === '/RED TEXT') continue;
            // Skip if already found in red text
            if (tags.indexOf(plainTag) === -1) {
                tags.push(plainTag);
            }
        }

        return tags;
    }

    // ------------------------------------------------------------------
    // Internal: Contextual override (data tables following interactive tags)
    // ------------------------------------------------------------------

    /**
     * Check whether a table should be overridden as a data table because it
     * immediately follows an interactive type tag (outside the table).
     *
     * @param {Array<Object>} contentBlocks - Full content array
     * @param {number} tableIndex - Index of the table in the array
     * @returns {boolean} True if the table should be treated as a data table
     */
    _shouldOverrideAsDataTable(contentBlocks, tableIndex) {
        // Look back 1-5 blocks before the table for interactive type tags
        var lookbackLimit = Math.max(0, tableIndex - 5);

        for (var i = tableIndex - 1; i >= lookbackLimit; i--) {
            var block = contentBlocks[i];
            if (block.type !== 'paragraph' || !block.data) continue;

            var text = this._buildFormattedText(block.data);
            var tags = this._extractTagsFromText(text);

            for (var t = 0; t < tags.length; t++) {
                var tag = tags[t];
                if (/^flip\s*card/i.test(tag) || /^flipcard/i.test(tag) ||
                    /^drag\s*and\s*drop/i.test(tag) || /^drag\s*&\s*drop/i.test(tag) ||
                    /^hint\s*slider/i.test(tag) || /^hintslider/i.test(tag) ||
                    /^carousel/i.test(tag) || /^slide\s*show/i.test(tag) || /^slideshow/i.test(tag) ||
                    /^accordion/i.test(tag) ||
                    /^click\s*drop/i.test(tag) || /^clickdrop/i.test(tag) ||
                    /^word\s*(?:highlighter|select)/i.test(tag) ||
                    /^speech\s*bubble/i.test(tag) ||
                    /^tabs$/i.test(tag) ||
                    /^memory\s*game/i.test(tag) ||
                    /^reorder$/i.test(tag) ||
                    /^typing\s*(?:self[- ]check|quiz)/i.test(tag) ||
                    /^mcq$/i.test(tag) ||
                    /^radio\s*quiz/i.test(tag) || /^true\s*false/i.test(tag)) {

                    // Override UNLESS the table contains an [Activity] tag
                    // (which overrides everything)
                    var tableTags = this._getTableAllTags(contentBlocks[tableIndex].data);
                    var hasActivity = tableTags.some(function (tg) {
                        return /^activity\s/i.test(tg) || /^activity$/i.test(tg);
                    });
                    return !hasActivity;
                }
            }
        }

        return false;
    }

    /**
     * Get all tags from all cells in a table.
     *
     * @param {Object} tableData - Table data
     * @returns {Array<string>} All tag names
     */
    _getTableAllTags(tableData) {
        var tags = [];
        if (!tableData || !tableData.rows) return tags;

        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            if (!row.cells) continue;
            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                if (!cell || !cell.paragraphs) continue;
                for (var p = 0; p < cell.paragraphs.length; p++) {
                    var text = this._buildFormattedText(cell.paragraphs[p]);
                    var cellTags = this._extractTagsFromText(text);
                    tags = tags.concat(cellTags);
                }
            }
        }
        return tags;
    }

    // ------------------------------------------------------------------
    // Internal: Layout table unwrapping
    // ------------------------------------------------------------------

    /**
     * Unwrap a layout table into content blocks.
     * Each row is processed: main content cells become paragraph blocks,
     * sidebar cells (images, alerts) become annotated paragraph blocks.
     *
     * @param {Object} tableData - The layout table data
     * @returns {Array<Object>} Replacement content blocks
     */
    _unwrapTable(tableData) {
        var blocks = [];
        var counter = ++this._counter;

        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            if (!row.cells || row.cells.length === 0) continue;
            var layoutRowId = 'lrow-' + counter + '-' + r;
            var roles = this._assignColumnRoles(row);

            var mainCells = [];
            var sidebarCells = [];

            for (var c = 0; c < row.cells.length; c++) {
                if (roles[c] === 'main_content' || roles[c] === 'content') {
                    mainCells.push(row.cells[c]);
                } else {
                    sidebarCells.push({ cell: row.cells[c], role: roles[c] });
                }
            }

            // Extract main content cell paragraphs into the stream
            for (var mc = 0; mc < mainCells.length; mc++) {
                var cell = mainCells[mc];
                if (!cell.paragraphs) continue;
                for (var p = 0; p < cell.paragraphs.length; p++) {
                    var para = cell.paragraphs[p];
                    // Skip empty paragraphs
                    if (!para.text && (!para.runs || para.runs.length === 0)) continue;
                    blocks.push({
                        type: 'paragraph',
                        data: para,
                        _unwrappedFrom: 'layout_table',
                        _cellRole: 'main_content',
                        _layoutRowId: layoutRowId
                    });
                }
            }

            // Extract sidebar cells as annotated blocks. _createSidebarBlock
            // may return a single block OR an array (sidebar + trailing
            // writer-instruction paragraphs not absorbed into the synthetic
            // image/alert block).
            for (var sc = 0; sc < sidebarCells.length; sc++) {
                var sidebar = sidebarCells[sc];
                var sidebarResult = this._createSidebarBlock(sidebar.cell, sidebar.role);
                if (!sidebarResult) continue;
                var sidebarBlocks = Array.isArray(sidebarResult) ? sidebarResult : [sidebarResult];
                for (var sr = 0; sr < sidebarBlocks.length; sr++) {
                    sidebarBlocks[sr]._layoutRowId = layoutRowId;
                    blocks.push(sidebarBlocks[sr]);
                }
            }
        }

        return blocks;
    }

    /**
     * Assign roles to each column in a layout table row.
     *
     * @param {Object} row - Table row { cells: [...] }
     * @returns {Array<string>} Role for each column: 'main_content', 'sidebar_image', 'sidebar_alert', or 'content'
     */
    _assignColumnRoles(row) {
        var roles = [];

        for (var c = 0; c < row.cells.length; c++) {
            var cell = row.cells[c];
            var tags = [];
            var cellText = '';

            if (cell && cell.paragraphs) {
                for (var p = 0; p < cell.paragraphs.length; p++) {
                    var text = this._buildFormattedText(cell.paragraphs[p]);
                    cellText += text + ' ';
                    var cellTags = this._extractTagsFromText(text);
                    tags = tags.concat(cellTags);
                }
            }

            var hasActivityOrBody = tags.some(function (t) {
                return /^activity/i.test(t) || /^body$/i.test(t) || /^body\s+text$/i.test(t) ||
                    /^H[2-5]$/i.test(t) || /^multichoice/i.test(t) || /^multi\s*choice/i.test(t) ||
                    /^drag/i.test(t) || /^word/i.test(t) ||
                    /^button$/i.test(t) || /^modal/i.test(t) ||
                    /^upload\s*to\s*dropbox$/i.test(t) || /^go\s*to\s*journal$/i.test(t) ||
                    /^end\s*page$/i.test(t) || /^end\s*lesson$/i.test(t) ||
                    /^lesson/i.test(t) || /^accordion/i.test(t) ||
                    /^flip\s*card/i.test(t) || /^flipcard/i.test(t) ||
                    /^carousel/i.test(t) || /^hint\s*slider/i.test(t) ||
                    /^click\s*drop/i.test(t) || /^clickdrop/i.test(t) ||
                    /^speech\s*bubble/i.test(t) || /^tabs$/i.test(t) ||
                    /^supervisor/i.test(t) || /^engagement/i.test(t) ||
                    /^external\s*link/i.test(t);
            });

            var hasOnlyImage = tags.length > 0 && tags.every(function (t) {
                return /^image/i.test(t);
            });

            var hasOnlyAlert = tags.length > 0 && tags.every(function (t) {
                return /^alert$/i.test(t) || /^important$/i.test(t) ||
                    /^alert[- ]/i.test(t);
            });

            // Check for plain image URL (no tags but URL with image extension or istock)
            var isPlainImageURL = tags.length === 0 &&
                /https?:\/\/.*\.(jpg|jpeg|png|gif|webp|svg)|istockphoto/i.test(cellText);

            if (hasActivityOrBody) {
                roles.push('main_content');
            } else if (hasOnlyImage || isPlainImageURL) {
                roles.push('sidebar_image');
            } else if (hasOnlyAlert) {
                roles.push('sidebar_alert');
            } else if (tags.length === 0 && cellText.trim()) {
                // No tags but has content — treat as general content
                roles.push('content');
            } else {
                roles.push('content');
            }
        }

        return roles;
    }

    /**
     * Create a sidebar content block from a sidebar cell.
     *
     * Returns either:
     *   - A single annotated block (for simple image/alert cells), or
     *   - An array of blocks: the annotated sidebar block followed by any
     *     additional paragraphs from the cell that carry meaningful content
     *     beyond the image/alert (e.g., writer/CS instructions). This
     *     preserves otherwise-lost text (Defect 3) and keeps it available
     *     for downstream writer-instruction detection.
     *
     * @param {Object} cell - Cell data
     * @param {string} role - 'sidebar_image' or 'sidebar_alert'
     * @returns {Object|Array<Object>|null} Annotated content block(s) or null
     */
    _createSidebarBlock(cell, role) {
        if (!cell || !cell.paragraphs || cell.paragraphs.length === 0) return null;

        var imageUrl = '';
        var alertText = [];
        // Classify each paragraph: the "image" paragraph (carries the URL or
        // the [image] tag) is absorbed into the synthetic image block; any
        // other paragraph is preserved as a standalone block.
        var imageParaIndices = {};

        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            var text = this._buildFormattedText(para);

            // URL extraction — exclude whitespace, `]`, `[` and the high
            // surrogate of the 🔴 red-text-marker emoji (U+1F534 =
            // \uD83D\uDD34). Without the `\uD83D` exclusion the regex
            // greedily swallows the opening of the next red-text marker
            // (e.g. "https://...URL🔴[RED") when a red-space run follows
            // the hyperlink — see Defect 2.
            var urlMatch = text.match(/(https?:\/\/[^\s\[\]\uD83D]+)/);
            if (urlMatch && !imageUrl) {
                imageUrl = urlMatch[1];
                imageParaIndices[p] = true;
            }

            // Tag-based classification: paragraphs whose only structural
            // tag is [image] (or whose content is exclusively the URL) are
            // treated as the image paragraph.
            var tagResult = this._normaliser.processBlock(text);
            var clean = (tagResult.cleanText || '').trim();

            var paraTags = this._extractTagsFromText(text);
            var hasImageTag = paraTags.some(function (t) { return /^image/i.test(t); });
            var hasAlertTag = paraTags.some(function (t) {
                return /^alert$/i.test(t) || /^important$/i.test(t) || /^alert[- ]/i.test(t);
            });

            if (role === 'sidebar_image' && (hasImageTag || urlMatch)) {
                imageParaIndices[p] = true;
            }
            if (role === 'sidebar_alert' && (hasAlertTag || clean)) {
                if (clean) alertText.push(clean);
                imageParaIndices[p] = true;
            }
        }

        // Build list of "extra" paragraphs (those NOT absorbed into the
        // synthetic block). These are preserved as standalone paragraph
        // blocks so their content (e.g., fully-red CS writer instructions)
        // is never dropped — Defect 3.
        var extras = [];
        for (var ep = 0; ep < cell.paragraphs.length; ep++) {
            if (imageParaIndices[ep]) continue;
            var extraPara = cell.paragraphs[ep];
            // Skip paragraphs with no meaningful content
            if (!extraPara.text || !extraPara.text.trim()) continue;
            if ((!extraPara.runs || extraPara.runs.length === 0) && !extraPara.text) continue;
            extras.push({
                type: 'paragraph',
                data: extraPara,
                _unwrappedFrom: 'layout_table',
                _cellRole: 'sidebar_extra'
            });
        }

        if (role === 'sidebar_image') {
            // Synthesise a paragraph that preserves the [image] tag as a
            // red-coloured run and the resolved URL as a plain run. This
            // keeps the [image] marker visible in the text stream (Defect 2)
            // while leaving _sidebarImageUrl as the canonical URL source
            // for the HTML converter.
            var runs = [
                {
                    text: '[image]',
                    formatting: { bold: false, italic: false, underline: false, strikethrough: false, color: 'FF0000', highlight: null, isRed: true }
                }
            ];
            if (imageUrl) {
                runs.push({
                    text: ' ',
                    formatting: { bold: false, italic: false, underline: false, strikethrough: false, color: null, highlight: null, isRed: false }
                });
                runs.push({
                    text: imageUrl,
                    formatting: { bold: false, italic: false, underline: false, strikethrough: false, color: null, highlight: null, isRed: false },
                    hyperlink: imageUrl
                });
            }
            var imgParaText = imageUrl ? ('[image] ' + imageUrl) : '[image]';
            var imgPara = {
                runs: runs,
                text: imgParaText,
                heading: null,
                listLevel: null,
                listNumId: null,
                listFormat: null,
                isListItem: false
            };
            var imgBlock = {
                type: 'paragraph',
                data: imgPara,
                _unwrappedFrom: 'layout_table',
                _cellRole: 'sidebar_image',
                _sidebarImageUrl: imageUrl,
                _sidebarParagraphs: cell.paragraphs
            };
            if (extras.length === 0) return imgBlock;
            return [imgBlock].concat(extras);
        }

        if (role === 'sidebar_alert') {
            var alertPara = {
                runs: [{
                    text: alertText.join(' '),
                    formatting: { bold: false, italic: false, underline: false, strikethrough: false, color: null, highlight: null, isRed: false }
                }],
                text: alertText.join(' '),
                heading: null,
                listLevel: null,
                listNumId: null,
                listFormat: null,
                isListItem: false
            };
            var alertBlock = {
                type: 'paragraph',
                data: alertPara,
                _unwrappedFrom: 'layout_table',
                _cellRole: 'sidebar_alert',
                _sidebarAlertContent: alertText,
                _sidebarParagraphs: cell.paragraphs
            };
            if (extras.length === 0) return alertBlock;
            return [alertBlock].concat(extras);
        }

        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Text building (mirrors HtmlConverter._buildFormattedText)
    // ------------------------------------------------------------------

    /**
     * Build formatted text from a paragraph's runs.
     * Mirrors the same logic used by HtmlConverter._buildFormattedText()
     * to produce consistent red text markers and formatting.
     *
     * @param {Object} para - Paragraph data object
     * @returns {string} Formatted text with red text markers
     */
    _buildFormattedText(para) {
        if (!para) return '';
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
            }

            text += chunk;
        }

        return text;
    }
}
