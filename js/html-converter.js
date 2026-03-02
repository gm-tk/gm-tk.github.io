/**
 * HtmlConverter — Core HTML conversion engine for ParseMaster.
 *
 * Transforms parsed content blocks into fully marked-up HTML for
 * non-interactive content. Interactive components are rendered as
 * temporary red placeholder text (Phase 4 will refine these).
 *
 * @see CLAUDE.md Section 11 — HTML Conversion Rules
 * @see CLAUDE.md Section 13 — Future Architecture
 */

'use strict';

class HtmlConverter {
    /**
     * Create an HtmlConverter instance.
     *
     * @param {TagNormaliser} tagNormaliser - An initialised TagNormaliser instance
     * @param {TemplateEngine} templateEngine - An initialised TemplateEngine instance
     */
    constructor(tagNormaliser, templateEngine) {
        if (!tagNormaliser) {
            throw new Error('HtmlConverter requires a TagNormaliser instance');
        }
        if (!templateEngine) {
            throw new Error('HtmlConverter requires a TemplateEngine instance');
        }

        /** @type {TagNormaliser} */
        this._normaliser = tagNormaliser;

        /** @type {TemplateEngine} */
        this._templateEngine = templateEngine;
    }

    // ------------------------------------------------------------------
    // Public API
    // ------------------------------------------------------------------

    /**
     * Convert a single page's content blocks into the body HTML.
     *
     * @param {Object} pageData - Page object from PageBoundary.assignPages()
     * @param {Object} config - Resolved template config from TemplateEngine.getConfig()
     * @returns {string} HTML string for the body content area
     */
    convertPage(pageData, config) {
        var blocks = pageData.contentBlocks || [];
        var processedBlocks = this._processAllBlocks(blocks);
        var bodyHtml = this._renderBlocks(processedBlocks, config, pageData);
        return bodyHtml;
    }

    /**
     * Assemble a complete HTML file (skeleton + body content + module menu).
     *
     * @param {Object} pageData - Page object from PageBoundary with extra fields
     * @param {Object} config - Resolved template config
     * @param {Object} moduleInfo - Module-level information
     * @param {string} moduleInfo.moduleCode
     * @param {string} moduleInfo.englishTitle
     * @param {string|null} moduleInfo.tereoTitle
     * @param {number} moduleInfo.totalPages
     * @param {Object|null} moduleInfo.overviewContent
     * @returns {string} Complete standalone HTML string
     */
    assemblePage(pageData, config, moduleInfo) {
        var skeletonData = {
            type: pageData.type,
            lessonNumber: pageData.lessonNumber,
            filename: pageData.filename,
            moduleCode: moduleInfo.moduleCode,
            englishTitle: moduleInfo.englishTitle || '',
            tereoTitle: moduleInfo.tereoTitle || null,
            totalPages: moduleInfo.totalPages,
            pageIndex: pageData.type === 'overview' ? 0 : pageData.lessonNumber
        };

        var skeleton = this._templateEngine.generateSkeleton(config, skeletonData);
        var bodyHtml = this.convertPage(pageData, config);

        // Replace content placeholder
        var html = skeleton.replace('    <!-- CONTENT_PLACEHOLDER -->', bodyHtml);

        // Generate and replace module menu content
        html = this._replaceModuleMenuContent(html, pageData, config, moduleInfo);

        return html;
    }

    // ------------------------------------------------------------------
    // Internal: Block processing
    // ------------------------------------------------------------------

    /**
     * Process all content blocks through the tag normaliser, building
     * a structured representation for rendering.
     *
     * @param {Array<Object>} blocks - Raw content blocks from PageBoundary
     * @returns {Array<Object>} Processed blocks with tag info and formatted text
     */
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
            var tagResult = this._normaliser.processBlock(text);

            return {
                type: 'paragraph',
                data: block.data,
                formattedText: text,
                tagResult: tagResult,
                cleanText: tagResult.cleanText
            };
        }

        if (block.type === 'table' && block.data) {
            var tableText = this._buildTableTextForTags(block.data);
            var tableTagResult = this._normaliser.processBlock(tableText);

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

    // ------------------------------------------------------------------
    // Internal: Block rendering
    // ------------------------------------------------------------------

    /**
     * Render all processed blocks into HTML.
     *
     * @param {Array<Object>} processedBlocks - Processed blocks
     * @param {Object} config - Template config
     * @param {Object} pageData - Page data
     * @returns {string} Combined HTML string
     */
    _renderBlocks(processedBlocks, config, pageData) {
        var htmlParts = [];
        var i = 0;
        var inActivity = false;
        var activityHasInteractive = false;
        var activityParts = [];
        var colClass = config.gridRules ? config.gridRules.defaultContent : 'col-md-8 col-12';

        // Collect consecutive body content for grouping in rows
        var pendingContent = [];

        var self = this;

        function flushPending() {
            if (pendingContent.length > 0) {
                var rowHtml = self._wrapInRow(pendingContent.join('\n'), colClass);
                if (inActivity) {
                    activityParts.push(rowHtml);
                } else {
                    htmlParts.push(rowHtml);
                }
                pendingContent = [];
            }
        }

        while (i < processedBlocks.length) {
            var pBlock = processedBlocks[i];
            var tags = pBlock.tagResult ? pBlock.tagResult.tags : [];
            var primaryTag = tags.length > 0 ? tags[0] : null;
            var tagName = primaryTag ? primaryTag.normalised : null;
            var category = primaryTag ? primaryTag.category : null;

            // Handle red text instructions as HTML comments
            if (pBlock.tagResult && pBlock.tagResult.redTextInstructions) {
                for (var ri = 0; ri < pBlock.tagResult.redTextInstructions.length; ri++) {
                    var instruction = pBlock.tagResult.redTextInstructions[ri];
                    if (instruction.trim()) {
                        var comment = '    <!-- CS: ' + this._escContent(instruction.trim()) + ' -->';
                        if (inActivity) {
                            activityParts.push(comment);
                        } else {
                            htmlParts.push(comment);
                        }
                    }
                }
            }

            // Skip structural tags that don't produce visible HTML
            if (category === 'structural') {
                // These are handled at page level, not block level
                i++;
                continue;
            }

            // Skip whitespace-only blocks
            if (pBlock.tagResult && pBlock.tagResult.isWhitespaceOnly) {
                i++;
                continue;
            }

            // Skip blocks that are red-text-only with no tags and no clean text
            if (pBlock.tagResult && pBlock.tagResult.isRedTextOnly &&
                tags.length === 0 && !pBlock.cleanText) {
                i++;
                continue;
            }

            // --- Activity wrapper ---
            if (tagName === 'activity') {
                flushPending();
                inActivity = true;
                activityHasInteractive = false;
                activityParts = [];
                var activityId = primaryTag.id || '';
                // Store activity info for closing
                this._currentActivityId = activityId;
                i++;
                continue;
            }

            if (tagName === 'end_activity') {
                flushPending();
                if (inActivity) {
                    var activityClass = activityHasInteractive
                        ? 'activity interactive'
                        : 'activity alertPadding';
                    var activityNum = this._currentActivityId || '';
                    var activityHtml = '    <div class="' + activityClass + '"' +
                        (activityNum ? ' number="' + this._escAttr(activityNum) + '"' : '') + '>\n';
                    activityHtml += activityParts.join('\n') + '\n';
                    activityHtml += '    </div>';
                    htmlParts.push(activityHtml);
                    inActivity = false;
                    activityParts = [];
                }
                i++;
                continue;
            }

            // --- Activity heading ---
            if (tagName === 'activity_heading') {
                flushPending();
                var ahText = pBlock.cleanText || '';
                var ahHtml = '      <h3>' + this._convertInlineFormatting(ahText) + '</h3>';
                if (inActivity) {
                    activityParts.push(ahHtml);
                } else {
                    htmlParts.push(this._wrapInRow(ahHtml, colClass));
                }
                i++;
                continue;
            }

            // --- Interactive components (temporary placeholder) ---
            if (category === 'interactive') {
                flushPending();
                activityHasInteractive = true;
                var interactiveName = tagName || 'unknown';
                var placeholderHtml = '      <p style="color: red; font-weight: bold;">' +
                    '\u26A0\uFE0F INTERACTIVE: ' + this._escContent(interactiveName) +
                    ' \u2014 placeholder (to be developed)</p>';
                if (inActivity) {
                    activityParts.push(placeholderHtml);
                } else {
                    htmlParts.push(this._wrapInRow(placeholderHtml, colClass));
                }
                i++;
                continue;
            }

            // --- Headings ---
            if (tagName === 'heading') {
                flushPending();
                var headingLevel = primaryTag.level || 2;
                var headingText = pBlock.cleanText || '';

                // [H1] in body context renders as <h2>
                if (headingLevel === 1) {
                    headingLevel = 2;
                }

                // Strip full-heading italic wrapping
                headingText = this._stripFullHeadingItalic(headingText);

                // First "Lesson N" heading rule for lesson pages
                if (pageData.type === 'lesson' && headingLevel === 2) {
                    var lessonPrefixMatch = headingText.match(/^Lesson\s+\d+\s+/i);
                    if (lessonPrefixMatch) {
                        headingText = headingText.substring(lessonPrefixMatch[0].length);
                        headingLevel = 3;
                    }
                }

                // Clamp heading level to 2-5
                if (headingLevel < 2) headingLevel = 2;
                if (headingLevel > 5) headingLevel = 5;

                var hTag = 'h' + headingLevel;
                var headingHtml = '      <' + hTag + '>' +
                    this._convertInlineFormatting(headingText) +
                    '</' + hTag + '>';

                if (inActivity) {
                    activityParts.push(headingHtml);
                } else {
                    htmlParts.push(this._wrapInRow(headingHtml, colClass));
                }
                i++;
                continue;
            }

            // --- Body text ---
            if (tagName === 'body' || (category === null && !tagName && pBlock.cleanText)) {
                var bodyText = pBlock.cleanText || '';
                if (bodyText.trim()) {
                    // Check if it's a list item from the original paragraph
                    if (pBlock.data && pBlock.data.isListItem) {
                        // Collect consecutive list items
                        var listItems = [];
                        var listStartI = i;
                        while (i < processedBlocks.length) {
                            var lb = processedBlocks[i];
                            if (lb.data && lb.data.isListItem) {
                                listItems.push(lb);
                                i++;
                            } else {
                                break;
                            }
                        }
                        var listHtml = this._renderList(listItems);
                        pendingContent.push(listHtml);
                        continue;
                    }

                    var pHtml = '      <p>' + this._convertInlineFormatting(bodyText) + '</p>';
                    pendingContent.push(pHtml);
                }
                i++;
                continue;
            }

            // --- Alert ---
            if (tagName === 'alert') {
                flushPending();
                var alertContent = this._collectBlockContent(processedBlocks, i);
                var alertHtml = '    <div class="alert">\n' +
                    '      <div class="row">\n' +
                    '        <div class="col-12">\n' +
                    '          <p>' + this._convertInlineFormatting(alertContent) + '</p>\n' +
                    '        </div>\n' +
                    '      </div>\n' +
                    '    </div>';
                alertHtml = this._wrapInRow(alertHtml, colClass);
                if (inActivity) {
                    activityParts.push(alertHtml);
                } else {
                    htmlParts.push(alertHtml);
                }
                i++;
                continue;
            }

            // --- Important ---
            if (tagName === 'important') {
                flushPending();
                var impContent = this._collectBlockContent(processedBlocks, i);
                var impHtml = '    <div class="alert solid">\n' +
                    '      <div class="row">\n' +
                    '        <div class="col-12">\n' +
                    '          <p>' + this._convertInlineFormatting(impContent) + '</p>\n' +
                    '        </div>\n' +
                    '      </div>\n' +
                    '    </div>';
                impHtml = this._wrapInRow(impHtml, colClass);
                if (inActivity) {
                    activityParts.push(impHtml);
                } else {
                    htmlParts.push(impHtml);
                }
                i++;
                continue;
            }

            // --- Cultural alerts ---
            if (tagName === 'alert_cultural_wananga' ||
                tagName === 'alert_cultural_talanoa' ||
                tagName === 'alert_cultural_combined') {
                flushPending();
                var layout = tagName.replace('alert_cultural_', '');
                var cultContent = this._collectBlockContent(processedBlocks, i);
                var cultHtml = '    <div class="alert cultural" layout="' + layout + '">\n' +
                    '      <div class="row">\n' +
                    '        <div class="col-12">\n' +
                    '          <p>' + this._convertInlineFormatting(cultContent) + '</p>\n' +
                    '        </div>\n' +
                    '      </div>\n' +
                    '    </div>';
                cultHtml = this._wrapInRow(cultHtml, colClass);
                if (inActivity) {
                    activityParts.push(cultHtml);
                } else {
                    htmlParts.push(cultHtml);
                }
                i++;
                continue;
            }

            // --- Whakatauki ---
            if (tagName === 'whakatauki') {
                flushPending();
                var whakContent = this._collectMultiLineContent(processedBlocks, i, 2);
                var whakHtml = '    <div class="whakatauki">\n';
                for (var w = 0; w < whakContent.length; w++) {
                    whakHtml += '      <p>' + this._convertInlineFormatting(whakContent[w]) + '</p>\n';
                }
                whakHtml += '    </div>';
                whakHtml = this._wrapInRow(whakHtml, colClass);
                if (inActivity) {
                    activityParts.push(whakHtml);
                } else {
                    htmlParts.push(whakHtml);
                }
                i++;
                continue;
            }

            // --- Quote ---
            if (tagName === 'quote') {
                flushPending();
                var quoteLines = this._collectMultiLineContent(processedBlocks, i, 2);
                var quoteText = quoteLines[0] || '';
                var quoteAck = quoteLines.length > 1 ? quoteLines[1] : '';

                // Add quotes if not already present
                if (quoteText && !quoteText.startsWith('"') && !quoteText.startsWith('\u201C')) {
                    quoteText = '\u201C' + quoteText + '\u201D';
                }

                var quoteHtml = '      <p class="quoteText">' +
                    this._convertInlineFormatting(quoteText) + '</p>';
                if (quoteAck) {
                    quoteHtml += '\n      <p class="quoteAck">' +
                        this._convertInlineFormatting(quoteAck) + '</p>';
                }
                quoteHtml = this._wrapInRow(quoteHtml, colClass);
                if (inActivity) {
                    activityParts.push(quoteHtml);
                } else {
                    htmlParts.push(quoteHtml);
                }
                i++;
                continue;
            }

            // --- Rhetorical question ---
            if (tagName === 'rhetorical_question') {
                flushPending();
                var rqContent = this._collectBlockContent(processedBlocks, i);
                var rqHtml = '    <div class="rhetoricalQuestion">\n' +
                    '      <p>' + this._convertInlineFormatting(rqContent) + '</p>\n' +
                    '    </div>';
                rqHtml = this._wrapInRow(rqHtml, colClass);
                if (inActivity) {
                    activityParts.push(rqHtml);
                } else {
                    htmlParts.push(rqHtml);
                }
                i++;
                continue;
            }

            // --- Video ---
            if (tagName === 'video') {
                flushPending();
                var videoUrl = this._extractUrlFromContent(processedBlocks, i);
                var videoHtml = this._renderVideo(videoUrl, config);
                videoHtml = this._wrapInRow(videoHtml, colClass);
                if (inActivity) {
                    activityParts.push(videoHtml);
                } else {
                    htmlParts.push(videoHtml);
                }
                i++;
                continue;
            }

            // --- Image ---
            if (tagName === 'image') {
                flushPending();
                var imgInfo = this._extractImageInfo(processedBlocks, i);
                var imgHtml = this._renderImage(imgInfo, config);
                imgHtml = this._wrapInRow(imgHtml, colClass);
                if (inActivity) {
                    activityParts.push(imgHtml);
                } else {
                    htmlParts.push(imgHtml);
                }
                i++;
                continue;
            }

            // --- Audio ---
            if (tagName === 'audio') {
                flushPending();
                var audioFile = this._extractAudioFilename(processedBlocks, i);
                var audioHtml = '      <audio preload="none" src="audio/' +
                    this._escAttr(audioFile) + '" class="audioPlayer icon" title="max-width:300px"></audio>';
                audioHtml = this._wrapInRow(audioHtml, colClass);
                if (inActivity) {
                    activityParts.push(audioHtml);
                } else {
                    htmlParts.push(audioHtml);
                }
                i++;
                continue;
            }

            // --- Button ---
            if (tagName === 'button') {
                flushPending();
                var btnInfo = this._extractLinkInfo(processedBlocks, i);
                var btnHtml = '      <a href="' + this._escAttr(btnInfo.url) +
                    '" target="_blank"><div class="button">' +
                    this._convertInlineFormatting(btnInfo.text) + '</div></a>';
                btnHtml = this._wrapInRow(btnHtml, colClass);
                if (inActivity) {
                    activityParts.push(btnHtml);
                } else {
                    htmlParts.push(btnHtml);
                }
                i++;
                continue;
            }

            // --- External link button ---
            if (tagName === 'external_link_button') {
                flushPending();
                var elbInfo = this._extractLinkInfo(processedBlocks, i);
                var elbHtml = '      <a href="' + this._escAttr(elbInfo.url) +
                    '" target="_blank"><div class="externalButton">' +
                    this._convertInlineFormatting(elbInfo.text) + '</div></a>';
                elbHtml = this._wrapInRow(elbHtml, colClass);
                if (inActivity) {
                    activityParts.push(elbHtml);
                } else {
                    htmlParts.push(elbHtml);
                }
                i++;
                continue;
            }

            // --- External link ---
            if (tagName === 'external_link') {
                flushPending();
                var elInfo = this._extractLinkInfo(processedBlocks, i);
                var elHtml = '      <a href="' + this._escAttr(elInfo.url) +
                    '" target="_blank">' + this._convertInlineFormatting(elInfo.text) + '</a>';
                elHtml = this._wrapInRow(elHtml, colClass);
                if (inActivity) {
                    activityParts.push(elHtml);
                } else {
                    htmlParts.push(elHtml);
                }
                i++;
                continue;
            }

            // --- Supervisor button ---
            if (tagName === 'supervisor_button') {
                flushPending();
                var supContent = this._collectBlockContent(processedBlocks, i);
                var supHtml = '    <div class="supervisorContainer">\n' +
                    '      <div class="supervisorButton"></div>\n' +
                    '      <div class="supervisorContent">\n' +
                    '        <p>' + this._convertInlineFormatting(supContent) + '</p>\n' +
                    '      </div>\n' +
                    '    </div>';
                supHtml = this._wrapInRow(supHtml, colClass);
                if (inActivity) {
                    activityParts.push(supHtml);
                } else {
                    htmlParts.push(supHtml);
                }
                i++;
                continue;
            }

            // --- Table (tagged as [TABLE]) ---
            if (pBlock.type === 'table' && this._hasTableTag(pBlock)) {
                flushPending();
                var tableHtml = this._renderTable(pBlock.data);
                tableHtml = this._wrapInRow(tableHtml, colClass);
                if (inActivity) {
                    activityParts.push(tableHtml);
                } else {
                    htmlParts.push(tableHtml);
                }
                i++;
                continue;
            }

            // --- Untagged table → grid layout ---
            if (pBlock.type === 'table' && !this._hasTableTag(pBlock)) {
                flushPending();
                var gridTableHtml = this._renderTableAsGrid(pBlock.data);
                if (inActivity) {
                    activityParts.push(gridTableHtml);
                } else {
                    htmlParts.push(gridTableHtml);
                }
                i++;
                continue;
            }

            // --- Subtag (front, back, static_heading, etc.) ---
            if (category === 'subtag') {
                // Sub-tags are typically part of interactive data; render as plain text
                if (pBlock.cleanText && pBlock.cleanText.trim()) {
                    var subHtml = '      <p>' + this._convertInlineFormatting(pBlock.cleanText) + '</p>';
                    pendingContent.push(subHtml);
                }
                i++;
                continue;
            }

            // --- Link category (misc buttons) ---
            if (category === 'link') {
                flushPending();
                var linkInfo = this._extractLinkInfo(processedBlocks, i);
                var linkHtml = '      <a href="' + this._escAttr(linkInfo.url) +
                    '" target="_blank">' + this._convertInlineFormatting(linkInfo.text) + '</a>';
                linkHtml = this._wrapInRow(linkHtml, colClass);
                if (inActivity) {
                    activityParts.push(linkHtml);
                } else {
                    htmlParts.push(linkHtml);
                }
                i++;
                continue;
            }

            // --- Reo translate ---
            if (tagName === 'reo_translate') {
                // Structural styling tag — content continues; skip the tag itself
                i++;
                continue;
            }

            // --- Default: render as paragraph if there's clean text ---
            if (pBlock.cleanText && pBlock.cleanText.trim()) {
                // Check if this is a list item
                if (pBlock.data && pBlock.data.isListItem) {
                    var defListItems = [];
                    var defListStart = i;
                    while (i < processedBlocks.length) {
                        var dlb = processedBlocks[i];
                        if (dlb.data && dlb.data.isListItem) {
                            defListItems.push(dlb);
                            i++;
                        } else {
                            break;
                        }
                    }
                    var defListHtml = this._renderList(defListItems);
                    pendingContent.push(defListHtml);
                    continue;
                }

                var defHtml = '      <p>' + this._convertInlineFormatting(pBlock.cleanText) + '</p>';
                pendingContent.push(defHtml);
            }

            i++;
        }

        // Flush any remaining pending content
        flushPending();

        // Close any open activity
        if (inActivity) {
            var finalActivityClass = activityHasInteractive
                ? 'activity interactive'
                : 'activity alertPadding';
            var finalActivityNum = this._currentActivityId || '';
            var finalActivityHtml = '    <div class="' + finalActivityClass + '"' +
                (finalActivityNum ? ' number="' + this._escAttr(finalActivityNum) + '"' : '') + '>\n';
            finalActivityHtml += activityParts.join('\n') + '\n';
            finalActivityHtml += '    </div>';
            htmlParts.push(finalActivityHtml);
        }

        return htmlParts.join('\n');
    }

    // ------------------------------------------------------------------
    // Internal: Inline formatting conversion
    // ------------------------------------------------------------------

    /**
     * Convert ParseMaster formatting markers to HTML.
     * Also handles hyperlink conversion and HTML escaping.
     *
     * @param {string} text - Text with formatting markers
     * @returns {string} HTML string
     */
    _convertInlineFormatting(text) {
        if (!text) return '';

        // First, handle hyperlinks: __link text__ [LINK: URL]
        text = text.replace(/__([^_]+)__\s*\[LINK:\s*([^\]]+)\]/g, function (match, linkText, url) {
            return '<a href="' + url.trim() + '" target="_blank">' + linkText + '</a>';
        });

        // Also handle [LINK: URL] without underline markers (bare link references)
        text = text.replace(/\[LINK:\s*([^\]]+)\]/g, function (match, url) {
            return '<a href="' + url.trim() + '" target="_blank">' + url.trim() + '</a>';
        });

        // HTML-escape content text (but NOT the already-inserted HTML tags)
        // We need to be careful: escape < > & only in non-HTML-tag portions
        text = this._escapeContentPreservingTags(text);

        // Convert formatting markers (order matters: *** before ** before *)
        // Bold+Italic: ***text***
        text = text.replace(/\*\*\*([^*]+)\*\*\*/g, '<b><i>$1</i></b>');

        // Bold: **text**
        text = text.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');

        // Italic: *text*  (but not inside URLs or already processed)
        text = text.replace(/(?<![/\w])\*([^*]+)\*(?![/\w])/g, '<i>$1</i>');

        // Underline: __text__ (but not those already consumed by hyperlinks)
        text = text.replace(/__([^_]+)__/g, '<u>$1</u>');

        return text;
    }

    /**
     * HTML-escape content while preserving already-inserted HTML tags.
     *
     * @param {string} text - Text potentially containing HTML tags and raw content
     * @returns {string} Text with content escaped but tags preserved
     */
    _escapeContentPreservingTags(text) {
        // Split on HTML tags (preserve them), escape everything else
        var parts = text.split(/(<[^>]+>)/);
        var result = '';

        for (var i = 0; i < parts.length; i++) {
            if (parts[i].charAt(0) === '<' && parts[i].charAt(parts[i].length - 1) === '>') {
                // This is an HTML tag — preserve as-is
                result += parts[i];
            } else {
                // This is content — escape it
                result += parts[i]
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
            }
        }

        return result;
    }

    /**
     * Strip italic wrapping from an entire heading.
     * If the whole heading is wrapped in *...*, remove it.
     * If only part is italic, preserve it.
     *
     * @param {string} text - Heading text
     * @returns {string} Text with full-heading italic stripped
     */
    _stripFullHeadingItalic(text) {
        if (!text) return '';
        var trimmed = text.trim();

        // Check for full wrapping: starts with * and ends with *
        // but not ** (bold) — single italic markers only
        if (trimmed.charAt(0) === '*' && trimmed.charAt(trimmed.length - 1) === '*') {
            // Check it's not bold markers
            if (trimmed.charAt(1) !== '*' && trimmed.charAt(trimmed.length - 2) !== '*') {
                // Full italic wrapping — strip it
                return trimmed.substring(1, trimmed.length - 1);
            }
        }

        return text;
    }

    // ------------------------------------------------------------------
    // Internal: Content collection helpers
    // ------------------------------------------------------------------

    /**
     * Collect the clean text from the current block (content after the tag).
     *
     * @param {Array<Object>} processedBlocks - All processed blocks
     * @param {number} index - Current block index
     * @returns {string} Clean text content
     */
    _collectBlockContent(processedBlocks, index) {
        var block = processedBlocks[index];
        return (block && block.cleanText) ? block.cleanText : '';
    }

    /**
     * Collect content from the current block, expecting multiple lines.
     *
     * @param {Array<Object>} processedBlocks - All processed blocks
     * @param {number} index - Current block index
     * @param {number} expectedLines - Number of lines expected
     * @returns {Array<string>} Array of text lines
     */
    _collectMultiLineContent(processedBlocks, index, expectedLines) {
        var block = processedBlocks[index];
        var text = (block && block.cleanText) ? block.cleanText : '';

        // Split on newlines or use as single line
        var lines = text.split(/\n/).filter(function (l) { return l.trim(); });

        if (lines.length < expectedLines) {
            // Try to collect from subsequent blocks
            var j = index + 1;
            while (lines.length < expectedLines && j < processedBlocks.length) {
                var nextBlock = processedBlocks[j];
                if (nextBlock && nextBlock.cleanText && nextBlock.cleanText.trim()) {
                    var nextTags = nextBlock.tagResult ? nextBlock.tagResult.tags : [];
                    // Stop if next block has its own tag
                    if (nextTags.length > 0 && nextTags[0].normalised) break;
                    lines.push(nextBlock.cleanText.trim());
                }
                j++;
            }
        }

        return lines;
    }

    /**
     * Extract a URL from the content following a tag (e.g., video URL).
     *
     * @param {Array<Object>} processedBlocks - All processed blocks
     * @param {number} index - Current block index
     * @returns {string} URL or empty string
     */
    _extractUrlFromContent(processedBlocks, index) {
        var block = processedBlocks[index];
        var text = (block && block.cleanText) ? block.cleanText : '';

        // Check clean text for URL
        var urlMatch = text.match(/https?:\/\/[^\s]+/);
        if (urlMatch) return urlMatch[0];

        // Check formatted text for URL
        var fText = (block && block.formattedText) ? block.formattedText : '';
        urlMatch = fText.match(/https?:\/\/[^\s\]]+/);
        if (urlMatch) return urlMatch[0];

        // Look in next block for URL
        if (index + 1 < processedBlocks.length) {
            var nextBlock = processedBlocks[index + 1];
            if (nextBlock) {
                var nextText = nextBlock.cleanText || nextBlock.formattedText || '';
                urlMatch = nextText.match(/https?:\/\/[^\s\]]+/);
                if (urlMatch) return urlMatch[0];
            }
        }

        return '';
    }

    /**
     * Extract image information from content around an [image] tag.
     *
     * @param {Array<Object>} processedBlocks - All processed blocks
     * @param {number} index - Current block index
     * @returns {Object} Image info {istockUrl, istockId, alt, dimensions}
     */
    _extractImageInfo(processedBlocks, index) {
        var block = processedBlocks[index];
        var text = (block && block.formattedText) ? block.formattedText : '';
        var cleanText = (block && block.cleanText) ? block.cleanText : '';
        var combined = text + ' ' + cleanText;

        // Check next block too
        if (index + 1 < processedBlocks.length) {
            var next = processedBlocks[index + 1];
            if (next && next.cleanText) {
                combined += ' ' + next.cleanText;
            }
            if (next && next.formattedText) {
                combined += ' ' + next.formattedText;
            }
        }

        var istockUrl = '';
        var istockId = '';
        var istockMatch = combined.match(/https?:\/\/(?:www\.)?istockphoto\.com\/[^\s\]]+/);
        if (istockMatch) {
            istockUrl = istockMatch[0];
            var gmMatch = istockUrl.match(/gm(\d+)/);
            if (gmMatch) {
                istockId = 'iStock-' + gmMatch[1];
            }
        }

        return {
            istockUrl: istockUrl,
            istockId: istockId,
            alt: '',
            dimensions: '600x400'
        };
    }

    /**
     * Extract audio filename from content.
     *
     * @param {Array<Object>} processedBlocks - All processed blocks
     * @param {number} index - Current block index
     * @returns {string} Audio filename
     */
    _extractAudioFilename(processedBlocks, index) {
        var block = processedBlocks[index];
        var text = (block && block.cleanText) ? block.cleanText : '';

        // Look for a filename pattern
        var fileMatch = text.match(/([^\s/]+\.mp3)/i);
        if (fileMatch) {
            return fileMatch[1].replace(/\s/g, '_');
        }

        // Try next block
        if (index + 1 < processedBlocks.length) {
            var next = processedBlocks[index + 1];
            if (next && next.cleanText) {
                fileMatch = next.cleanText.match(/([^\s/]+\.mp3)/i);
                if (fileMatch) {
                    return fileMatch[1].replace(/\s/g, '_');
                }
            }
        }

        return 'audio_placeholder.mp3';
    }

    /**
     * Extract link text and URL from content.
     *
     * @param {Array<Object>} processedBlocks - All processed blocks
     * @param {number} index - Current block index
     * @returns {Object} {text, url}
     */
    _extractLinkInfo(processedBlocks, index) {
        var block = processedBlocks[index];
        var formattedText = (block && block.formattedText) ? block.formattedText : '';
        var cleanText = (block && block.cleanText) ? block.cleanText : '';

        // Check for [LINK: URL] pattern
        var linkMatch = formattedText.match(/\[LINK:\s*([^\]]+)\]/);
        var url = linkMatch ? linkMatch[1].trim() : '';

        // If no link found in formatted text, look for bare URL
        if (!url) {
            var urlMatch = cleanText.match(/https?:\/\/[^\s]+/);
            if (urlMatch) url = urlMatch[0];
        }

        // Get link text (clean text minus URLs)
        var text = cleanText.replace(/https?:\/\/[^\s]+/g, '').trim();
        if (!text) text = url;

        return { text: text, url: url || '#' };
    }

    // ------------------------------------------------------------------
    // Internal: Rendering helpers
    // ------------------------------------------------------------------

    /**
     * Wrap content in a Bootstrap grid row.
     *
     * @param {string} content - HTML content
     * @param {string} colClass - Column class
     * @returns {string} Wrapped HTML
     */
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

                html += indent + '  <li>' + this._convertInlineFormatting(text);
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
    _renderTable(tableData) {
        if (!tableData.rows || tableData.rows.length === 0) return '';

        var html = '    <div class="table-responsive">\n';
        html += '      <table class="table noHover tableFixed">\n';
        html += '        <tbody>\n';

        for (var r = 0; r < tableData.rows.length; r++) {
            var row = tableData.rows[r];
            html += '          <tr>\n';
            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                var cellContent = this._renderCellContent(cell);
                html += '            <td>' + cellContent + '</td>\n';
            }
            html += '          </tr>\n';
        }

        html += '        </tbody>\n';
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
    _renderCellContent(cell) {
        if (!cell.paragraphs || cell.paragraphs.length === 0) return '';

        var parts = [];
        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            var text = this._buildFormattedText(para);
            // Process through tag normaliser to strip tags
            var processed = this._normaliser.processBlock(text);
            var clean = processed.cleanText || '';
            if (clean.trim()) {
                parts.push(this._convertInlineFormatting(clean));
            }
        }

        return parts.join('<br />');
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
                var cellContent = this._renderCellContent(cell);
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
    _renderVideo(url, config) {
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
    _renderImage(imgInfo, config) {
        var dimensions = imgInfo.dimensions || '600x400';
        var placeholderBase = (config.imageDefaults && config.imageDefaults.placeholderBase)
            ? config.imageDefaults.placeholderBase
            : 'https://placehold.co';

        var html = '      <img class="img-fluid" loading="lazy" src="' +
            placeholderBase + '/' + dimensions + '?text=Image+Placeholder" alt="" />';

        if (imgInfo.istockId) {
            html += '\n      <!-- <img class="img-fluid" loading="lazy" src="images/' +
                this._escAttr(imgInfo.istockId) + '.jpg" alt="' +
                this._escAttr(imgInfo.istockUrl) + '" /> -->';
        }

        return html;
    }

    // ------------------------------------------------------------------
    // Internal: Module menu content
    // ------------------------------------------------------------------

    /**
     * Replace module menu placeholders with actual content.
     *
     * @param {string} html - Full HTML string with placeholders
     * @param {Object} pageData - Page data
     * @param {Object} config - Template config
     * @param {Object} moduleInfo - Module info
     * @returns {string} HTML with module menu populated
     */
    _replaceModuleMenuContent(html, pageData, config, moduleInfo) {
        if (pageData.type === 'overview') {
            // Overview page: populate tab content
            var overviewTab = this._generateOverviewTabContent(pageData, config, moduleInfo);
            var infoTab = this._generateInfoTabContent(pageData, config, moduleInfo);

            html = html.replace(
                '            <!-- MODULE_MENU_CONTENT: Overview -->',
                overviewTab
            );
            html = html.replace(
                '            <!-- MODULE_MENU_CONTENT: Information -->',
                infoTab
            );

            // Handle Standards tab (NCEA)
            if (html.indexOf('<!-- MODULE_MENU_CONTENT: Standards -->') !== -1) {
                html = html.replace(
                    '            <!-- MODULE_MENU_CONTENT: Standards -->',
                    '            <!-- Standards content to be added -->'
                );
            }
        } else {
            // Lesson page: simplified menu
            var lessonMenu = this._generateLessonMenuContent(pageData, config, moduleInfo);
            html = html.replace(
                '          <!-- MODULE_MENU_CONTENT -->',
                lessonMenu
            );
        }

        return html;
    }

    /**
     * Generate Overview tab content for overview page module menu.
     *
     * @param {Object} pageData - Page data
     * @param {Object} config - Template config
     * @param {Object} moduleInfo - Module info
     * @returns {string} HTML content
     */
    _generateOverviewTabContent(pageData, config, moduleInfo) {
        var html = '';
        var title = moduleInfo.englishTitle || 'Module Overview';

        // Overview title with h4>span
        html += '            <h4><span>Tirohanga Wh\u0101nui | Overview</span></h4>\n';
        html += '            <!-- Overview content from module -->';

        return html;
    }

    /**
     * Generate Information tab content.
     *
     * @param {Object} pageData - Page data
     * @param {Object} config - Template config
     * @param {Object} moduleInfo - Module info
     * @returns {string} HTML content
     */
    _generateInfoTabContent(pageData, config, moduleInfo) {
        return '            <!-- Information tab content -->';
    }

    /**
     * Generate lesson page module menu content.
     *
     * @param {Object} pageData - Page data
     * @param {Object} config - Template config
     * @param {Object} moduleInfo - Module info
     * @returns {string} HTML content
     */
    _generateLessonMenuContent(pageData, config, moduleInfo) {
        var labels = (config.moduleMenu && config.moduleMenu.lessonPage && config.moduleMenu.lessonPage.labels)
            ? config.moduleMenu.lessonPage.labels
            : { learning: 'We are learning:', success: 'I can:' };

        var html = '';
        html += '          <h5>' + this._escContent(labels.learning) + '</h5>\n';
        html += '          <!-- Learning intentions content -->\n';
        html += '          <h5>' + this._escContent(labels.success) + '</h5>\n';
        html += '          <!-- Success criteria content -->';

        return html;
    }

    // ------------------------------------------------------------------
    // Internal: Utility methods
    // ------------------------------------------------------------------

    /**
     * Escape text for HTML content (not for use inside tags).
     *
     * @param {string} str - Raw text
     * @returns {string} Escaped text
     */
    _escContent(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    /**
     * Escape text for use in HTML attributes.
     *
     * @param {string} str - Raw text
     * @returns {string} Escaped text
     */
    _escAttr(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }
}
