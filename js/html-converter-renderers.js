/**
 * HtmlConverterRenderers — Tables, lists, layout-table, image, video, sidebar, hint-slider, flip-card.
 *
 * Extracted from js/html-converter.js as part of the html-converter refactor.
 * See docs/29-html-converter-refactor-plan.md.
 */

'use strict';

class HtmlConverterRenderers {
    constructor(contentHelpers, escContent, escAttr, coreRef) {
        this._content = contentHelpers;
        this._escContent = escContent;
        this._escAttr = escAttr;
        this._coreRef = coreRef;
    }

    _wrapInRow(content, colClass) {
        return '    <div class="row">\n' +
            '      <div class="' + colClass + '">\n' +
            content + '\n' +
            '      </div>\n' +
            '    </div>';
    }

    /**
     * Render a list (bullet or ordered) from consecutive list items.
     *
     * @param {Array<Object>} items - Processed list item blocks
     * @returns {string} HTML list
     */
    _renderList(items) {
        if (items.length === 0) return '';

        var firstItem = items[0];
        var isOrdered = firstItem.data && firstItem.data.listFormat && (
            firstItem.data.listFormat === 'decimal' ||
            firstItem.data.listFormat === 'lowerLetter' ||
            firstItem.data.listFormat === 'upperLetter' ||
            firstItem.data.listFormat === 'lowerRoman' ||
            firstItem.data.listFormat === 'upperRoman'
        );

        var listTag = isOrdered ? 'ol' : 'ul';

        return this._buildNestedList(items, 0, listTag);
    }

    /**
     * Build a nested list structure recursively.
     *
     * @param {Array<Object>} items - List items
     * @param {number} level - Current nesting level
     * @param {string} listTag - 'ul' or 'ol'
     * @returns {string} HTML list
     */
    _buildNestedList(items, level, listTag) {
        var indent = '      ' + '  '.repeat(level);
        var html = indent + '<' + listTag + '>\n';

        var i = 0;
        while (i < items.length) {
            var item = items[i];
            var itemLevel = (item.data && item.data.listLevel) ? item.data.listLevel : 0;

            if (itemLevel === level) {
                var text = item.cleanText || '';
                // Check if next items are deeper (nested)
                var children = [];
                var j = i + 1;
                while (j < items.length) {
                    var nextLevel = (items[j].data && items[j].data.listLevel) ? items[j].data.listLevel : 0;
                    if (nextLevel > level) {
                        children.push(items[j]);
                        j++;
                    } else {
                        break;
                    }
                }

                html += indent + '  <li>' + this._coreRef._convertInlineFormatting(text);
                if (children.length > 0) {
                    html += '\n' + this._buildNestedList(children, level + 1, listTag) + '\n' + indent + '  ';
                }
                html += '</li>\n';

                i = j;
            } else if (itemLevel > level) {
                // Deeper items handled by recursion above
                i++;
            } else {
                // Shallower — shouldn't happen at top level
                break;
            }
        }

        html += indent + '</' + listTag + '>';
        return html;
    }

    /**
     * Render a tagged [TABLE] as an HTML table.
     *
     * @param {Object} tableData - Table data object
     * @returns {string} HTML table
     */
    renderTable(tableData) {
        if (!tableData.rows || tableData.rows.length === 0) return '';

        var html = '    <div class="table-responsive">\n';
        html += '      <table class="table noHover tableFixed">\n';

        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            var isHeader = (r === 0);
            var cellTag = isHeader ? 'th' : 'td';

            if (isHeader) {
                html += '        <thead>\n';
                html += '          <tr class="rowSolid">\n';
            } else {
                if (r === 1) html += '        <tbody>\n';
                html += '          <tr>\n';
            }

            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                var cellContent = this.renderCellContent(cell);
                html += '            <' + cellTag + '>' + cellContent + '</' + cellTag + '>\n';
            }

            html += '          </tr>\n';
            if (isHeader) {
                html += '        </thead>\n';
            }
        }

        if (tableData.rows.length > 1) {
            html += '        </tbody>\n';
        }
        html += '      </table>\n';
        html += '    </div>';

        return html;
    }

    /**
     * Render table cell content, preserving formatting.
     *
     * @param {Object} cell - Cell data
     * @returns {string} HTML content for the cell
     */
    renderCellContent(cell) {
        if (!cell.paragraphs || cell.paragraphs.length === 0) return '';

        var parts = [];
        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            var text = this._coreRef._buildFormattedText(para);
            // Process through tag normaliser to strip tags
            var processed = this._coreRef._normaliser.processBlock(text);
            var clean = processed.cleanText || '';
            if (clean.trim()) {
                parts.push(this._coreRef._convertInlineFormatting(clean));
            }
        }

        if (parts.length === 1) {
            return parts[0];
        }
        return parts.map(function(p) { return '<p>' + p + '</p>'; }).join('');
    }

    /**
     * Render an untagged table as Bootstrap grid layout.
     *
     * @param {Object} tableData - Table data
     * @returns {string} HTML grid
     */
    _renderTableAsGrid(tableData) {
        if (!tableData.rows || tableData.rows.length === 0) return '';

        var html = '';
        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            html += '    <div class="row">\n';
            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                var cellContent = this.renderCellContent(cell);
                var colSize = Math.floor(12 / row.cells.length);
                html += '      <div class="col-md-' + colSize + ' col-12">\n';
                if (cellContent) {
                    html += '        <p>' + cellContent + '</p>\n';
                }
                html += '      </div>\n';
            }
            html += '    </div>\n';
        }

        return html;
    }

    /**
     * Detect if a table is a layout table (body text + image side-by-side).
     * A layout table has exactly 2 columns where one contains [body] tagged text
     * and the other contains [image] tagged content with no interactive tags.
     *
     * @param {Object} tableData - Raw table data
     * @returns {Object|null} Layout info { textCol, imageCol, textContent, imageRef } or null
     */
    _detectLayoutTable(tableData) {
        if (!tableData || !tableData.rows || tableData.rows.length === 0) return null;

        // Check first row has exactly 2 cells
        var firstRow = tableData.rows[0];
        if (!firstRow.cells || firstRow.cells.length !== 2) return null;

        var col0Tags = this._getTableCellTags(firstRow.cells[0]);
        var col1Tags = this._getTableCellTags(firstRow.cells[1]);

        // Check if one column has [body] and the other has [image]
        var col0HasBody = col0Tags.some(function (t) { return t.normalised === 'body'; });
        var col0HasImage = col0Tags.some(function (t) { return t.normalised === 'image'; });
        var col1HasBody = col1Tags.some(function (t) { return t.normalised === 'body'; });
        var col1HasImage = col1Tags.some(function (t) { return t.normalised === 'image'; });

        // Check no interactive tags
        var allTags = col0Tags.concat(col1Tags);
        var hasInteractive = allTags.some(function (t) { return t.category === 'interactive'; });
        if (hasInteractive) return null;

        var textColIdx = -1;
        var imageColIdx = -1;

        if (col0HasBody && col1HasImage) {
            textColIdx = 0;
            imageColIdx = 1;
        } else if (col1HasBody && col0HasImage) {
            textColIdx = 1;
            imageColIdx = 0;
        } else {
            return null;
        }

        // Extract text content from body cell (all rows)
        var textParagraphs = [];
        var imageRef = '';
        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            if (!row.cells || row.cells.length !== 2) continue;

            // Text cell
            var textCell = row.cells[textColIdx];
            for (var p = 0; p < textCell.paragraphs.length; p++) {
                var pText = this._coreRef._buildFormattedText(textCell.paragraphs[p]);
                var pTagResult = this._coreRef._normaliser.processBlock(pText);
                var clean = (pTagResult.cleanText || '').trim();
                if (clean) textParagraphs.push(clean);
            }

            // Image cell
            var imgCell = row.cells[imageColIdx];
            for (var ip = 0; ip < imgCell.paragraphs.length; ip++) {
                var iPText = this._coreRef._buildFormattedText(imgCell.paragraphs[ip]);
                var iTagResult = this._coreRef._normaliser.processBlock(iPText);
                var iClean = (iTagResult.cleanText || '').trim();
                // Check for URL in clean text
                if (iClean && /https?:\/\//.test(iClean)) {
                    var urlMatch = iClean.match(/(https?:\/\/[^\s]+)/);
                    if (urlMatch) imageRef = urlMatch[1];
                }
                // Also check the full text for URLs
                if (!imageRef) {
                    var urlInFull = iPText.match(/(https?:\/\/[^\s\]]+)/);
                    if (urlInFull) imageRef = urlInFull[1];
                }
            }
        }

        if (textParagraphs.length === 0) return null;

        return {
            textColIdx: textColIdx,
            imageColIdx: imageColIdx,
            textParagraphs: textParagraphs,
            imageRef: imageRef
        };
    }

    /**
     * Detect the "bullets + [image]" two-column table pattern.
     * One cell has bullet-list paragraphs (plus an optional leading intro
     * paragraph) and the sibling cell has an [image] marker + URL. Returns
     * a layout descriptor, or null when either half of the pattern is
     * missing — so bullets-only tables and image-only tables fall through
     * to their existing single-column handlers.
     *
     * @param {Object} tableData - Raw table data
     * @returns {Object|null} { bulletsColIdx, imageColIdx, introText, bulletItems, imageRef } or null
     */
    _detectBulletsAndImageTable(tableData) {
        if (!tableData || !tableData.rows || tableData.rows.length === 0) return null;
        var firstRow = tableData.rows[0];
        if (!firstRow.cells || firstRow.cells.length !== 2) return null;

        var self = this;
        function analyseCell(cell) {
            var bulletItems = [];
            var introText = '';
            var hasImageTag = false;
            var imageRef = '';
            if (!cell || !cell.paragraphs) {
                return { bulletItems: bulletItems, introText: introText, hasImageTag: hasImageTag, imageRef: imageRef };
            }
            for (var p = 0; p < cell.paragraphs.length; p++) {
                var para = cell.paragraphs[p];
                var text = self._coreRef._buildFormattedText(para);
                var tagResult = self._coreRef._normaliser.processBlock(text);
                var clean = (tagResult.cleanText || '').trim();
                var isImage = tagResult.tags && tagResult.tags.some(function (t) { return t.normalised === 'image'; });
                if (isImage) {
                    hasImageTag = true;
                    var urlMatch = clean.match(/(https?:\/\/[^\s]+)/);
                    if (urlMatch) imageRef = urlMatch[1];
                    continue;
                }
                if (para && para.isListItem) {
                    // Bullet item — strip any leading bullet character.
                    bulletItems.push(clean.replace(/^[•◦⁃\-\*]\s*/, ''));
                    continue;
                }
                if (clean) {
                    if (!introText) introText = clean;
                }
            }
            return { bulletItems: bulletItems, introText: introText, hasImageTag: hasImageTag, imageRef: imageRef };
        }

        var cell0 = analyseCell(firstRow.cells[0]);
        var cell1 = analyseCell(firstRow.cells[1]);

        var bulletsColIdx = -1, imageColIdx = -1;
        if (cell0.bulletItems.length > 0 && cell1.hasImageTag) {
            bulletsColIdx = 0; imageColIdx = 1;
        } else if (cell1.bulletItems.length > 0 && cell0.hasImageTag) {
            bulletsColIdx = 1; imageColIdx = 0;
        } else {
            return null;
        }

        var bulletsCell = bulletsColIdx === 0 ? cell0 : cell1;
        var imageCell = imageColIdx === 0 ? cell0 : cell1;

        return {
            bulletsColIdx: bulletsColIdx,
            imageColIdx: imageColIdx,
            introText: bulletsCell.introText,
            bulletItems: bulletsCell.bulletItems,
            imageRef: imageCell.imageRef
        };
    }

    /**
     * Strip leading/trailing *, **, *** markdown from a sentence. Used for
     * the intro paragraph in a bullets+image table where writers often
     * bold the intro (e.g. **AI is not safe…:**) but the rendered output
     * should emit a plain <p> without <b>/<i> wrapping.
     *
     * @param {string} text
     * @returns {string}
     */
    _stripBoldItalicMarkdown(text) {
        if (!text) return '';
        return text
            .replace(/\*{3}([\s\S]+?)\*{3}/g, '$1')
            .replace(/\*{2}([\s\S]+?)\*{2}/g, '$1')
            .replace(/\*([^\*\n]+)\*/g, '$1');
    }

    /**
     * Render a bullets+image table as a paired two-column row:
     *   col-md-6 col-12 paddingR  — alert wrapping intro <p> + bullet <ul>
     *   col-md-3 col-12 paddingL  — img
     *
     * @param {Object} layoutInfo - From _detectBulletsAndImageTable
     * @param {Object} config - Template config
     * @param {Object} [options] - Rendering options
     * @param {boolean} [options.alertWrap=false] - When true, the bullets column is wrapped in <div class="alert">. Default false.
     * @returns {string} HTML row
     */
    _renderBulletsAndImageTable(layoutInfo, config, options) {
        options = options || {};
        var alertWrap = options.alertWrap === true;
        var innerHtml = '';
        if (layoutInfo.introText) {
            var intro = this._stripBoldItalicMarkdown(layoutInfo.introText);
            innerHtml += '          <p>' + this._coreRef._convertInlineFormatting(intro) + '</p>\n';
        }
        if (layoutInfo.bulletItems.length > 0) {
            innerHtml += '          <ul>\n';
            for (var b = 0; b < layoutInfo.bulletItems.length; b++) {
                innerHtml += '            <li>' + this._coreRef._convertInlineFormatting(layoutInfo.bulletItems[b]) + '</li>\n';
            }
            innerHtml += '          </ul>\n';
        }

        var bulletsColumnInner;
        if (alertWrap) {
            bulletsColumnInner = '    <div class="alert">\n' +
                '      <div class="row">\n' +
                '        <div class="col-12">\n' +
                innerHtml +
                '        </div>\n' +
                '      </div>\n' +
                '    </div>';
        } else {
            bulletsColumnInner = '    <div class="row">\n' +
                '      <div class="col-12">\n' +
                innerHtml +
                '      </div>\n' +
                '    </div>';
        }

        var imgHtml = this.renderImagePlaceholder(layoutInfo.imageRef || '', config);

        return '    <div class="row">\n' +
            '      <div class="col-md-6 col-12 paddingR">\n' +
            bulletsColumnInner + '\n' +
            '      </div>\n' +
            '      <div class="col-md-3 col-12 paddingL">\n' +
            '        ' + imgHtml + '\n' +
            '      </div>\n' +
            '    </div>';
    }

    /**
     * Get all tags from a table cell's paragraphs.
     *
     * @param {Object} cell - Table cell data
     * @returns {Array<Object>} Tags found
     */
    _getTableCellTags(cell) {
        var tags = [];
        if (!cell || !cell.paragraphs) return tags;
        for (var p = 0; p < cell.paragraphs.length; p++) {
            var text = this._coreRef._buildFormattedText(cell.paragraphs[p]);
            var tagResult = this._coreRef._normaliser.processBlock(text);
            if (tagResult.tags) {
                tags = tags.concat(tagResult.tags);
            }
        }
        return tags;
    }

    /**
     * Render a layout table as Bootstrap side-by-side columns.
     *
     * @param {Object} layoutInfo - From _detectLayoutTable
     * @param {Object} config - Template config
     * @returns {string} HTML
     */
    _renderLayoutTable(layoutInfo, config) {
        var textColClass = 'col-md-8 col-12';
        var imgColClass = 'col-md-4 offset-md-0 col-12';

        var html = '    <div class="row">\n';

        // Render in document order (text col first or image col first)
        if (layoutInfo.textColIdx < layoutInfo.imageColIdx) {
            // Text left, image right
            html += '      <div class="' + textColClass + '">\n';
            for (var t = 0; t < layoutInfo.textParagraphs.length; t++) {
                html += '        <p>' + this._coreRef._convertInlineFormatting(layoutInfo.textParagraphs[t]) + '</p>\n';
            }
            html += '      </div>\n';
            html += '      <div class="' + imgColClass + '">\n';
            html += '        ' + this.renderImagePlaceholder(layoutInfo.imageRef, config) + '\n';
            html += '      </div>\n';
        } else {
            // Image left, text right
            html += '      <div class="' + imgColClass + '">\n';
            html += '        ' + this.renderImagePlaceholder(layoutInfo.imageRef, config) + '\n';
            html += '      </div>\n';
            html += '      <div class="' + textColClass + '">\n';
            for (var t2 = 0; t2 < layoutInfo.textParagraphs.length; t2++) {
                html += '        <p>' + this._coreRef._convertInlineFormatting(layoutInfo.textParagraphs[t2]) + '</p>\n';
            }
            html += '      </div>\n';
        }

        html += '    </div>';
        return html;
    }

    /**
     * Render an image placeholder tag (for layout tables).
     *
     * @param {string} imageRef - Image URL or reference
     * @param {Object} config - Template config
     * @returns {string} HTML img tag
     */
    renderImagePlaceholder(imageRef, config) {
        var imgClass = (config.imageDefaults && config.imageDefaults.class)
            ? config.imageDefaults.class : 'img-fluid';

        // iStockPhoto URLs matching /-gm<NUMERIC_ID>-/ resolve directly to
        // a local images/iStock-<ID>.jpg asset. alt="" is kept empty —
        // writers do not author alt text in the .docx template.
        if (imageRef) {
            var istockGmMatch = imageRef.match(/^https?:\/\/(?:www\.)?istockphoto\.com\/[^\s]*?-gm(\d+)(?:[-?\/][^\s]*)?$/);
            if (istockGmMatch) {
                return '<img class="' + imgClass + '" loading="lazy" src="images/iStock-' +
                    this._escAttr(istockGmMatch[1]) + '.jpg" alt="" />';
            }
        }

        var placeholderBase = (config.imageDefaults && config.imageDefaults.placeholderBase)
            ? config.imageDefaults.placeholderBase : 'https://placehold.co';

        var html = '<img class="' + imgClass + '" loading="lazy" src="' +
            placeholderBase + '/400x300?text=Image" alt="" />';

        if (imageRef) {
            html += '\n        <!-- Reference: ' + this._escContent(imageRef) + ' -->';
        }

        return html;
    }

    /**
     * Render a sidebar block (from layout table unwrapping) as HTML.
     *
     * @param {Object} pBlock - Processed block with _cellRole metadata
     * @param {Object} config - Template config
     * @returns {string} Sidebar HTML
     */
    _renderSidebarBlock(pBlock, config) {
        if (pBlock._cellRole === 'sidebar_image') {
            var imageUrl = pBlock._sidebarImageUrl || '';
            var imgHtml = '    <div class="alertImage">\n' +
                '      <div class="row">\n' +
                '        <div class="col-12">\n' +
                '          ' + this.renderImagePlaceholder(imageUrl, config) + '\n' +
                '        </div>\n' +
                '      </div>\n' +
                '    </div>';
            return imgHtml;
        }

        if (pBlock._cellRole === 'sidebar_alert') {
            var alertContent = pBlock._sidebarAlertContent || [];
            var alertHtml = '    <div class="alert top">\n' +
                '      <div class="row">\n' +
                '        <div class="col-12">\n';

            for (var ac = 0; ac < alertContent.length; ac++) {
                if (ac === 0 && alertContent.length > 1) {
                    // First item could be a heading
                    alertHtml += '          <h4>' + this._coreRef._convertInlineFormatting(alertContent[ac]) + '</h4>\n';
                } else {
                    alertHtml += '          <p>' + this._coreRef._convertInlineFormatting(alertContent[ac]) + '</p>\n';
                }
            }

            alertHtml += '        </div>\n' +
                '      </div>\n' +
                '    </div>';
            return alertHtml;
        }

        return '';
    }

    /**
     * Wrap main content and sidebar content in a side-by-side row layout.
     * Main content goes in col-md-8, sidebar goes in col-md-4.
     *
     * @param {string} mainHtml - HTML for the main content column
     * @param {string} sidebarHtml - HTML for the sidebar column
     * @returns {string} Combined row HTML
     */
    _wrapSideBySide(mainHtml, sidebarHtml, mainColClass, sidebarColClass) {
        var mainCol = mainColClass || 'col-md-8 col-12';
        var sideCol = sidebarColClass || 'col-md-4 offset-md-0 col-12';
        var html = '    <div class="row">\n';
        html += '      <div class="' + mainCol + '">\n';
        if (mainHtml && mainHtml.trim()) {
            html += mainHtml + '\n';
        }
        html += '      </div>\n';
        html += '      <div class="' + sideCol + '">\n';
        html += sidebarHtml + '\n';
        html += '      </div>\n';
        html += '    </div>';
        return html;
    }

    /**
     * Check if a processed table block has a [TABLE] tag.
     *
     * @param {Object} pBlock - Processed block
     * @returns {boolean}
     */
    _hasTableTag(pBlock) {
        if (!pBlock.tagResult || !pBlock.tagResult.tags) return false;
        for (var i = 0; i < pBlock.tagResult.tags.length; i++) {
            if (pBlock.tagResult.tags[i].normalised === 'table') {
                return true;
            }
        }
        return false;
    }

    /**
     * Render a video embed.
     *
     * @param {string} url - Video URL
     * @param {Object} config - Template config
     * @returns {string} HTML video embed
     */
    /**
     * Render a hintSlider interactive from the data table following the tag.
     *
     * @param {Array} processedBlocks - All processed blocks
     * @param {number} tagIndex - Index of the hint_slider tag block
     * @param {Array} rawBlocks - Raw content blocks
     * @param {Array} procToRawMap - Mapping from processed to raw indices
     * @param {Object} consumedRawIndices - Set of consumed raw indices
     * @returns {Object|null} { html, consumedRawIndices } or null
     */
    _renderHintSlider(processedBlocks, tagIndex, rawBlocks, procToRawMap, consumedRawIndices) {
        // Find the next table block after the tag
        var tableBlock = null;
        var tableRawIdx = -1;
        var consumed = [];

        if (rawBlocks && procToRawMap[tagIndex] !== undefined) {
            var startRaw = procToRawMap[tagIndex] + 1;
            for (var ri = startRaw; ri < rawBlocks.length && ri < startRaw + 5; ri++) {
                if (rawBlocks[ri].type === 'table' && rawBlocks[ri].data) {
                    tableBlock = rawBlocks[ri].data;
                    tableRawIdx = ri;
                    consumed.push(ri);
                    break;
                }
            }
        }

        // Also check processed blocks
        if (!tableBlock) {
            for (var pi = tagIndex + 1; pi < processedBlocks.length && pi < tagIndex + 5; pi++) {
                if (processedBlocks[pi].type === 'table' && processedBlocks[pi].data) {
                    tableBlock = processedBlocks[pi].data;
                    if (procToRawMap[pi] !== undefined) {
                        consumed.push(procToRawMap[pi]);
                    }
                    break;
                }
            }
        }

        if (!tableBlock || !tableBlock.rows || tableBlock.rows.length < 2) {
            return null;
        }

        // Parse the table: skip header row, extract front/back pairs from columns 2 & 3
        // (or columns 1 & 2 if only 2 columns)
        var rows = tableBlock.rows;
        var dataStartRow = 1; // Skip header row
        var frontCol, backCol;

        // Determine column layout
        if (rows[0].cells.length >= 3) {
            frontCol = 1;
            backCol = 2;
        } else {
            frontCol = 0;
            backCol = 1;
        }

        var hintRows = [];
        for (var r = dataStartRow; r < rows.length; r++) {
            var row = rows[r];
            if (!row.cells || row.cells.length <= backCol) continue;
            var frontText = this._getCellPlainText(row.cells[frontCol]);
            var backText = this._getCellPlainText(row.cells[backCol]);
            if (frontText.trim() || backText.trim()) {
                hintRows.push({ front: frontText.trim(), back: backText.trim() });
            }
        }

        if (hintRows.length === 0) return null;

        // Build HTML
        var html = '    <div class="hintSlider" hintCssFile="standard">\n';
        for (var h = 0; h < hintRows.length; h++) {
            html += '      <div class="hintRow dark">\n';
            html += '        <div class="infoContainer">\n';
            html += '          <div class="frontInfo">\n';
            html += '            <p>' + this._coreRef._convertInlineFormatting(hintRows[h].front) + '</p>\n';
            html += '          </div>\n';
            html += '          <div class="backInfo">\n';
            html += '            <p>' + this._coreRef._convertInlineFormatting(hintRows[h].back) + '</p>\n';
            html += '          </div>\n';
            html += '        </div>\n';
            html += '      </div>\n';
        }
        html += '    </div>';

        return { html: html, consumedRawIndices: consumed };
    }

    /**
     * Render a flipCard interactive from the data table following the tag.
     *
     * @param {Array} processedBlocks - All processed blocks
     * @param {number} tagIndex - Index of the flip_card tag block
     * @param {Array} rawBlocks - Raw content blocks
     * @param {Array} procToRawMap - Mapping from processed to raw indices
     * @param {Object} consumedRawIndices - Set of consumed raw indices
     * @returns {Object|null} { html, consumedRawIndices } or null
     */
    _renderFlipCard(processedBlocks, tagIndex, rawBlocks, procToRawMap, consumedRawIndices) {
        // Find the next table block after the tag
        var tableBlock = null;
        var consumed = [];

        if (rawBlocks && procToRawMap[tagIndex] !== undefined) {
            var startRaw = procToRawMap[tagIndex] + 1;
            for (var ri = startRaw; ri < rawBlocks.length && ri < startRaw + 5; ri++) {
                if (rawBlocks[ri].type === 'table' && rawBlocks[ri].data) {
                    tableBlock = rawBlocks[ri].data;
                    consumed.push(ri);
                    break;
                }
            }
        }

        if (!tableBlock) {
            for (var pi = tagIndex + 1; pi < processedBlocks.length && pi < tagIndex + 5; pi++) {
                if (processedBlocks[pi].type === 'table' && processedBlocks[pi].data) {
                    tableBlock = processedBlocks[pi].data;
                    if (procToRawMap[pi] !== undefined) {
                        consumed.push(procToRawMap[pi]);
                    }
                    break;
                }
            }
        }

        if (!tableBlock || !tableBlock.rows || tableBlock.rows.length < 2) {
            return null;
        }

        // Flipcard table: columns = cards, row 1 = fronts, row 2 = backs
        var rows = tableBlock.rows;
        var cardCount = rows[0].cells.length;
        var cards = [];

        for (var c = 0; c < cardCount; c++) {
            var frontCell = rows[0].cells[c];
            var backCell = rows.length > 1 ? rows[1].cells[c] : null;

            // Parse front: extract heading and image
            var frontText = this._getCellFormattedText(frontCell);
            var frontHeading = '';
            var frontImage = '';

            // Look for [H5] or [h5] heading tag
            var hMatch = frontText.match(/\[H\s*(\d)\]\s*/i);
            if (hMatch) {
                frontText = frontText.replace(/\[H\s*\d\]\s*/i, '');
            }
            // Look for [IMAGE: filename]
            var imgMatch = frontText.match(/\[IMAGE:\s*(\S+)\]/i);
            if (imgMatch) {
                frontImage = imgMatch[1];
                frontText = frontText.replace(/\[IMAGE:\s*\S+\]/i, '');
            }
            // Clean up the heading text
            frontText = frontText.replace(/\uD83D\uDD34\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\uD83D\uDD34/g, '');
            frontText = frontText.replace(/\[([^\]]*)\]/g, '');
            frontText = frontText.replace(/\s*\/\s*/g, '').trim(); // Remove cell separators
            frontHeading = frontText.trim();

            // Parse back
            var backText = '';
            if (backCell) {
                backText = this._getCellPlainText(backCell);
                // Strip [body] tag
                backText = backText.replace(/\[body\]\s*/gi, '').trim();
            }

            if (frontHeading || backText) {
                cards.push({
                    heading: frontHeading,
                    image: frontImage,
                    back: backText
                });
            }
        }

        if (cards.length === 0) return null;

        // Determine column width
        var colWidth = Math.floor(12 / Math.min(cards.length, 4));
        var colClass = 'col-md-' + colWidth + ' col-12';

        // Build HTML
        var html = '    <div class="row flipCardsContainer">\n';
        for (var fc = 0; fc < cards.length; fc++) {
            var card = cards[fc];
            html += '      <div class="' + colClass + ' paddingLR">\n';
            html += '        <div class="flipCard">\n';
            html += '          <div class="front">\n';
            if (card.heading) {
                html += '            <h5>' + this._coreRef._convertInlineFormatting(card.heading) + '</h5>\n';
            }
            if (card.image) {
                html += '            <img class="img-fluid" loading="lazy" src="images/' +
                    this._escAttr(card.image) + '" alt="Flipcard image" />\n';
            }
            html += '          </div>\n';
            html += '          <div class="back">\n';
            if (card.back) {
                html += '            <p>' + this._coreRef._convertInlineFormatting(card.back) + '</p>\n';
            }
            html += '          </div>\n';
            html += '        </div>\n';
            html += '      </div>\n';
        }
        html += '    </div>';

        return { html: html, consumedRawIndices: consumed };
    }

    /**
     * Get plain text from a table cell (all paragraphs concatenated).
     *
     * @param {Object} cell - Table cell with paragraphs
     * @returns {string} Plain text
     */
    _getCellPlainText(cell) {
        if (!cell || !cell.paragraphs) return '';
        var texts = [];
        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            var text = '';
            if (para.runs) {
                for (var r = 0; r < para.runs.length; r++) {
                    if (para.runs[r].text && !(para.runs[r].formatting && para.runs[r].formatting.isRed)) {
                        text += para.runs[r].text;
                    }
                }
            } else {
                text = para.text || '';
            }
            if (text.trim()) texts.push(text.trim());
        }
        return texts.join(' ');
    }

    /**
     * Get formatted text from a table cell (including formatting markers).
     *
     * @param {Object} cell - Table cell with paragraphs
     * @returns {string} Formatted text
     */
    _getCellFormattedText(cell) {
        if (!cell || !cell.paragraphs) return '';
        var texts = [];
        for (var p = 0; p < cell.paragraphs.length; p++) {
            texts.push(this._coreRef._buildFormattedText(cell.paragraphs[p]));
        }
        return texts.join(' / ');
    }

    renderVideo(url, config) {
        if (!url) {
            return '      <!-- Video URL not found -->';
        }

        // YouTube Shorts
        var shortsMatch = url.match(/youtube\.com\/shorts\/([a-zA-Z0-9_-]+)/);
        if (shortsMatch) {
            return '    <div class="videoSection youtubeShort ratio ratio-1x1">\n' +
                '      <iframe src="https://www.youtube.com/embed/' + this._escAttr(shortsMatch[1]) +
                '" frameborder="0" title="YouTube video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>\n' +
                '    </div>';
        }

        // YouTube standard
        var ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]+)/);
        if (ytMatch) {
            return '    <div class="videoSection ratio ratio-16x9">\n' +
                '      <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/' +
                this._escAttr(ytMatch[1]) +
                '" loading="lazy" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n' +
                '    </div>';
        }

        // Vimeo
        var vimeoMatch = url.match(/(?:vimeo\.com\/|player\.vimeo\.com\/video\/)(\d+)/);
        if (vimeoMatch) {
            return '    <div class="videoSection ratio ratio-16x9">\n' +
                '      <iframe src="https://player.vimeo.com/video/' + this._escAttr(vimeoMatch[1]) +
                '" frameborder="0" allowfullscreen></iframe>\n' +
                '    </div>';
        }

        // Unknown video URL — embed as-is
        return '    <div class="videoSection ratio ratio-16x9">\n' +
            '      <iframe src="' + this._escAttr(url) +
            '" frameborder="0" allowfullscreen></iframe>\n' +
            '    </div>';
    }

    /**
     * Render an image placeholder with commented-out iStock reference.
     *
     * @param {Object} imgInfo - Image info object
     * @param {Object} config - Template config
     * @returns {string} HTML image
     */
    renderImage(imgInfo, config) {
        // iStockPhoto URLs with a -gm<ID>- segment resolve to a local
        // images/iStock-<ID>.jpg asset. alt="" stays empty — writers do
        // not author alt text in the .docx template.
        if (imgInfo.istockId) {
            return '      <img class="img-fluid" loading="lazy" src="images/' +
                this._escAttr(imgInfo.istockId) + '.jpg" alt="" />';
        }

        var dimensions = imgInfo.dimensions || '600x400';
        var placeholderBase = (config.imageDefaults && config.imageDefaults.placeholderBase)
            ? config.imageDefaults.placeholderBase
            : 'https://placehold.co';

        return '      <img class="img-fluid" loading="lazy" src="' +
            placeholderBase + '/' + dimensions + '?text=Image+Placeholder" alt="" />';
    }

}
