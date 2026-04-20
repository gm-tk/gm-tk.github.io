/**
 * InteractiveCellParser — paragraph/run → formatted text conversion,
 * table/cell text extraction, inline media extraction, and table-pattern
 * classification used by the interactive extractor.
 *
 * Extracted from js/interactive-extractor.js as part of the interactive-extractor
 * refactor. See docs/28-interactive-extractor-refactor-plan.md.
 */

'use strict';

class InteractiveCellParser {
    constructor(tagNormaliser) {
        this._normaliser = tagNormaliser;
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
}
