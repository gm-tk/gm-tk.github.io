/**
 * HtmlConverter — Core HTML conversion engine for PageForge.
 *
 * Transforms parsed content blocks into fully marked-up HTML for
 * non-interactive content. Interactive components are rendered as
 * structured placeholders with data extraction via InteractiveExtractor.
 *
 * @see CLAUDE.md Section 11 — HTML Conversion Rules
 * @see CLAUDE.md Section 12 — Interactive Components
 */

'use strict';

class HtmlConverter {
    /**
     * Create an HtmlConverter instance.
     *
     * @param {TagNormaliser} tagNormaliser - An initialised TagNormaliser instance
     * @param {TemplateEngine} templateEngine - An initialised TemplateEngine instance
     * @param {InteractiveExtractor} [interactiveExtractor] - An optional InteractiveExtractor instance
     */
    constructor(tagNormaliser, templateEngine, interactiveExtractor) {
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

        /** @type {InteractiveExtractor|null} */
        this._interactiveExtractor = interactiveExtractor || null;

        /** @type {Array<Object>} Collected interactive reference entries from the last conversion run */
        this.collectedInteractives = [];
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
        var bodyHtml = this._renderBlocks(processedBlocks, config, pageData, blocks);
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
        // For overview pages, split content at [MODULE INTRODUCTION]
        // For lesson pages, split content at [LESSON OVERVIEW] / [LESSON CONTENT]
        var bodyPageData = pageData;
        var menuContentBlocks = null;

        if (pageData.type === 'overview') {
            var splitResult = this._splitOverviewContent(pageData);
            bodyPageData = {
                type: pageData.type,
                lessonNumber: pageData.lessonNumber,
                filename: pageData.filename,
                contentBlocks: splitResult.bodyBlocks
            };
            menuContentBlocks = splitResult.menuBlocks;
        } else if (pageData.type === 'lesson') {
            var lessonSplit = this._splitLessonContent(pageData);
            bodyPageData = {
                type: pageData.type,
                lessonNumber: pageData.lessonNumber,
                filename: pageData.filename,
                contentBlocks: lessonSplit.bodyBlocks
            };
            menuContentBlocks = lessonSplit.menuBlocks;
        }

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
        var bodyHtml = this.convertPage(bodyPageData, config);

        // Replace content placeholder
        var html = skeleton.replace('    <!-- CONTENT_PLACEHOLDER -->', bodyHtml);

        // Generate and replace module menu content
        html = this._replaceModuleMenuContent(html, pageData, config, moduleInfo, menuContentBlocks);

        return html;
    }

    /**
     * Split overview page content blocks into menu content and body content
     * at the [MODULE INTRODUCTION] tag boundary.
     *
     * @param {Object} pageData - Page data with contentBlocks
     * @returns {Object} { menuBlocks: Array, bodyBlocks: Array }
     */
    _splitOverviewContent(pageData) {
        var blocks = pageData.contentBlocks || [];
        var moduleIntroIndex = -1;

        // Find the [MODULE INTRODUCTION] tag
        for (var i = 0; i < blocks.length; i++) {
            var block = blocks[i];
            if (block.type === 'paragraph' && block.data) {
                var text = this._buildFormattedText(block.data);
                var tagResult = this._normaliser.processBlock(text);
                for (var t = 0; t < tagResult.tags.length; t++) {
                    if (tagResult.tags[t].normalised === 'module_introduction') {
                        moduleIntroIndex = i;
                        break;
                    }
                }
                if (moduleIntroIndex !== -1) break;
            }
        }

        if (moduleIntroIndex === -1) {
            // No MODULE INTRODUCTION found — all content goes to body
            return { menuBlocks: [], bodyBlocks: blocks };
        }

        // Menu blocks: everything before MODULE INTRODUCTION (after TITLE BAR)
        var menuBlocks = blocks.slice(0, moduleIntroIndex);
        // Body blocks: everything after MODULE INTRODUCTION (skip the tag itself)
        var bodyBlocks = blocks.slice(moduleIntroIndex + 1);

        return { menuBlocks: menuBlocks, bodyBlocks: bodyBlocks };
    }

    /**
     * Split lesson page content blocks into menu content (between [LESSON OVERVIEW]
     * and [LESSON CONTENT]) and body content (after [LESSON CONTENT]).
     *
     * @param {Object} pageData - Page data with contentBlocks
     * @returns {Object} { menuBlocks: Array, bodyBlocks: Array }
     */
    _splitLessonContent(pageData) {
        var blocks = pageData.contentBlocks || [];
        var overviewIndex = -1;
        var contentIndex = -1;

        for (var i = 0; i < blocks.length; i++) {
            var block = blocks[i];
            if (block.type === 'paragraph' && block.data) {
                var text = this._buildFormattedText(block.data);
                var tagResult = this._normaliser.processBlock(text);
                for (var t = 0; t < tagResult.tags.length; t++) {
                    var tagName = tagResult.tags[t].normalised;
                    if (tagName === 'lesson_overview' && overviewIndex === -1) {
                        overviewIndex = i;
                    }
                    if (tagName === 'lesson_content' && contentIndex === -1) {
                        contentIndex = i;
                    }
                }
            }
            if (overviewIndex !== -1 && contentIndex !== -1) break;
        }

        // If no lesson overview/content tags found, all goes to body
        if (overviewIndex === -1 && contentIndex === -1) {
            return { menuBlocks: [], bodyBlocks: blocks };
        }

        // If only lesson_content found (no overview), all before it is menu, after is body
        if (overviewIndex === -1 && contentIndex !== -1) {
            return {
                menuBlocks: blocks.slice(0, contentIndex),
                bodyBlocks: blocks.slice(contentIndex + 1)
            };
        }

        // If lesson_overview found but lesson_content is missing, use a heuristic:
        // The menu content (learning/success criteria) ends at the first heading (H2+),
        // activity tag, or interactive tag after the lesson overview section.
        // This prevents ALL content from being routed to the menu, leaving body empty.
        if (overviewIndex !== -1 && contentIndex === -1) {
            var heuristicEnd = blocks.length;
            for (var h = overviewIndex + 1; h < blocks.length; h++) {
                var hBlock = blocks[h];
                if (hBlock.type !== 'paragraph' || !hBlock.data) {
                    // Table blocks after some menu items likely signal body content
                    if (hBlock.type === 'table' && h > overviewIndex + 3) {
                        heuristicEnd = h;
                        break;
                    }
                    continue;
                }
                var hText = this._buildFormattedText(hBlock.data);
                var hTagResult = this._normaliser.processBlock(hText);
                for (var ht = 0; ht < hTagResult.tags.length; ht++) {
                    var hTag = hTagResult.tags[ht];
                    // Heading tags (H2, H3, etc.) signal start of body content
                    if (hTag.category === 'heading' && hTag.level && hTag.level <= 3) {
                        heuristicEnd = h;
                        break;
                    }
                    // Activity tags signal start of body content
                    if (hTag.normalised === 'activity' || hTag.normalised === 'end_activity') {
                        heuristicEnd = h;
                        break;
                    }
                    // Interactive tags signal start of body content
                    if (hTag.category === 'interactive') {
                        heuristicEnd = h;
                        break;
                    }
                    // Styling tags (alert, important, etc.) signal body content
                    if (hTag.category === 'styling') {
                        heuristicEnd = h;
                        break;
                    }
                }
                if (heuristicEnd !== blocks.length) break;
            }
            return {
                menuBlocks: blocks.slice(overviewIndex + 1, heuristicEnd),
                bodyBlocks: blocks.slice(heuristicEnd)
            };
        }

        // Normal case: both tags found
        // Menu blocks: between lesson_overview and lesson_content (exclusive of both tags)
        var menuStart = overviewIndex + 1;
        var menuEnd = contentIndex;
        var menuBlocks = blocks.slice(menuStart, menuEnd);

        // Body blocks: after lesson_content tag
        var bodyBlocks = blocks.slice(contentIndex + 1);

        return { menuBlocks: menuBlocks, bodyBlocks: bodyBlocks };
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

            // Detect hovertrigger pattern in formatted text:
            // 🔴[RED TEXT] [hovertrigger: [/RED TEXT]🔴 definition 🔴[RED TEXT] ] [/RED TEXT]🔴
            var hovertriggerData = this._extractHovertriggerData(text, block.data);

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

    // ------------------------------------------------------------------
    // Internal: Block rendering
    // ------------------------------------------------------------------

    /**
     * Render all processed blocks into HTML.
     *
     * @param {Array<Object>} processedBlocks - Processed blocks
     * @param {Object} config - Template config
     * @param {Object} pageData - Page data
     * @param {Array<Object>} [rawBlocks] - Original raw content blocks (for interactive extraction)
     * @returns {string} Combined HTML string
     */
    _renderBlocks(processedBlocks, config, pageData, rawBlocks) {
        var htmlParts = [];
        var i = 0;
        var inActivity = false;
        var activityHasInteractive = false;
        var activityHasSidebar = false;
        var activityHasDropbox = false;
        var activityParts = [];
        var colClass = config.gridRules ? config.gridRules.defaultContent : 'col-md-8 col-12';

        // Collect consecutive body content for grouping in rows
        var pendingContent = [];

        var self = this;

        // Build a mapping from processed block index to raw block index.
        // _processAllBlocks filters out pageBreaks and empty blocks, so
        // the indices diverge. We need the raw index for interactive extraction.
        var procToRawMap = [];
        if (rawBlocks) {
            var procIdx = 0;
            for (var ri = 0; ri < rawBlocks.length; ri++) {
                var rb = rawBlocks[ri];
                if (rb.type === 'pageBreak') continue;
                if ((rb.type === 'paragraph' && rb.data) || (rb.type === 'table' && rb.data)) {
                    if (procIdx < processedBlocks.length) {
                        procToRawMap[procIdx] = ri;
                        procIdx++;
                    }
                }
            }
        }

        // Track the set of raw block indices already consumed by interactives
        // so we skip processed blocks that correspond to consumed raw blocks.
        var consumedRawIndices = {};

        function flushPending() {
            if (pendingContent.length > 0) {
                if (inActivity) {
                    // Inside activities, push raw content — the activity wrapper
                    // provides its own inner row/col-12 structure
                    for (var fp = 0; fp < pendingContent.length; fp++) {
                        activityParts.push(pendingContent[fp]);
                    }
                } else {
                    var rowHtml = self._wrapInRow(pendingContent.join('\n'), colClass);
                    htmlParts.push(rowHtml);
                }
                pendingContent = [];
            }
        }

        while (i < processedBlocks.length) {
            // Skip blocks whose raw counterpart was consumed by interactive extraction
            if (procToRawMap[i] !== undefined && consumedRawIndices[procToRawMap[i]]) {
                i++;
                continue;
            }

            var pBlock = processedBlocks[i];
            var tags = pBlock.tagResult ? pBlock.tagResult.tags : [];
            var primaryTag = tags.length > 0 ? tags[0] : null;
            var tagName = primaryTag ? primaryTag.normalised : null;
            var category = primaryTag ? primaryTag.category : null;

            // Red text instructions are internal workflow annotations (CS notes).
            // They are captured by InteractiveExtractor for reference document
            // entries but are NOT rendered in the output HTML.

            // --- Auto-close activity at structural boundaries ---
            // Activities own all content until a clear section boundary.
            // H4/H5 are sub-headings WITHIN activities, so they do NOT close.
            // H2/H3 are section-level headings that signal a new section OUTSIDE.
            // [image], [video], [button], [alert] tags are content WITHIN activities.
            // 'activity', 'end_activity', and 'interactive' tags are handled
            // by their dedicated code blocks below — don't auto-close for those.
            if (inActivity) {
                var shouldAutoClose = false;

                // Section-level headings (H2, H3) always close an activity
                // (but NOT H4/H5, and NOT [Activity heading])
                if (category === 'heading' && tagName === 'heading' &&
                    primaryTag.level !== null && primaryTag.level <= 3) {
                    shouldAutoClose = true;
                }

                // Structural tags always close
                if (category === 'structural') {
                    shouldAutoClose = true;
                }

                // [body] tag only closes activity AFTER interactive was consumed
                // (before that, body text is instruction text within the activity)
                if (category === 'body' && tagName === 'body' && activityHasInteractive) {
                    shouldAutoClose = true;
                }

                // Non-interactive activities with content: also close at section headings
                if (!activityHasInteractive && activityParts.length > 0) {
                    if (category === 'heading' && tagName !== 'activity_heading' &&
                        primaryTag.level !== null && primaryTag.level <= 3) {
                        shouldAutoClose = true;
                    }
                }

                if (shouldAutoClose) {
                    flushPending();
                    var autoClsClass = activityHasDropbox
                        ? 'activity dropbox'
                        : (activityHasInteractive ? 'activity interactive' : 'activity');
                    if (activityHasSidebar) autoClsClass += ' alertPadding';
                    var autoClsNum = self._currentActivityId || '';
                    var autoClsHtml = '    <div class="' + autoClsClass + '"' +
                        (autoClsNum ? ' number="' + self._escAttr(autoClsNum) + '"' : '') + '>\n' +
                        '      <div class="row">\n        <div class="col-12">\n' +
                        activityParts.join('\n') + '\n' +
                        '        </div>\n      </div>\n' +
                        '    </div>';
                    htmlParts.push(self._wrapInRow(autoClsHtml, colClass));
                    inActivity = false;
                    activityHasInteractive = false;
                    activityHasSidebar = false;
                    activityHasDropbox = false;
                    activityParts = [];
                    // Don't increment i — re-process this block as body content
                    continue;
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
                // If already inside an activity (previous one not closed with [end activity]),
                // flush the previous activity to htmlParts before starting the new one.
                // This prevents content loss when writers omit [end activity] tags.
                if (inActivity && activityParts.length > 0) {
                    var prevActivityClass = activityHasDropbox
                        ? 'activity dropbox'
                        : (activityHasInteractive ? 'activity interactive' : 'activity');
                    if (activityHasSidebar) prevActivityClass += ' alertPadding';
                    var prevActivityNum = this._currentActivityId || '';
                    var prevActivityHtml = this._wrapInRow(
                        '    <div class="' + prevActivityClass + '"' +
                        (prevActivityNum ? ' number="' + this._escAttr(prevActivityNum) + '"' : '') + '>\n' +
                        '      <div class="row">\n        <div class="col-12">\n' +
                        activityParts.join('\n') + '\n' +
                        '        </div>\n      </div>\n' +
                        '    </div>', colClass);
                    htmlParts.push(prevActivityHtml);
                }
                inActivity = true;
                activityHasInteractive = false;
                activityHasSidebar = false;
                activityHasDropbox = false;
                activityParts = [];
                var activityId = primaryTag.id || '';
                // Store activity info for closing
                this._currentActivityId = activityId;

                // Bug 6 fix: Extract heading text from [Activity N] Heading text
                var actHeadingText = (pBlock.cleanText || '').trim();
                if (actHeadingText) {
                    actHeadingText = this._stripFullHeadingFormatting(actHeadingText);
                    var actHeadingInner = this._convertInlineFormatting(actHeadingText);
                    actHeadingInner = this._stripHeadingInlineTags(actHeadingInner);
                    if (actHeadingInner.trim()) {
                        activityParts.push('      <h3>' + actHeadingInner + '</h3>');
                    }
                }

                i++;
                continue;
            }

            if (tagName === 'end_activity') {
                flushPending();
                if (inActivity) {
                    var activityClass = activityHasDropbox
                        ? 'activity dropbox'
                        : (activityHasInteractive ? 'activity interactive' : 'activity');
                    if (activityHasSidebar) activityClass += ' alertPadding';
                    var activityNum = this._currentActivityId || '';
                    // Activity wrapper: outer row → col → activity div → inner row → col-12 → content
                    var activityHtml = '    <div class="' + activityClass + '"' +
                        (activityNum ? ' number="' + this._escAttr(activityNum) + '"' : '') + '>\n' +
                        '      <div class="row">\n        <div class="col-12">\n' +
                        activityParts.join('\n') + '\n' +
                        '        </div>\n      </div>\n' +
                        '    </div>';
                    // Wrap the activity div in an outer Bootstrap grid row
                    htmlParts.push(this._wrapInRow(activityHtml, colClass));
                    inActivity = false;
                    activityHasSidebar = false;
                    activityHasDropbox = false;
                    activityParts = [];
                }
                i++;
                continue;
            }

            // --- Activity heading ---
            if (tagName === 'activity_heading') {
                flushPending();
                var ahText = pBlock.cleanText || '';
                ahText = this._stripFullHeadingFormatting(ahText);
                var ahLevel = primaryTag.level || 3;
                if (ahLevel < 2) ahLevel = 2;
                if (ahLevel > 5) ahLevel = 5;
                var ahTag = 'h' + ahLevel;
                var ahInner = this._convertInlineFormatting(ahText);
                ahInner = this._stripHeadingInlineTags(ahInner);
                var ahHtml = '      <' + ahTag + '>' + ahInner + '</' + ahTag + '>';
                if (inActivity) {
                    activityParts.push(ahHtml);
                } else {
                    htmlParts.push(this._wrapInRow(ahHtml, colClass));
                }
                i++;
                continue;
            }

            // --- Inline info trigger → render as <span class="infoTrigger"> ---
            if (tagName === 'info_trigger' && category === 'interactive') {
                // Info triggers (not info_trigger_image) are inline elements
                // Extract the trigger word and definition from the block
                var itResult = this._extractInfoTriggerData(pBlock);
                if (itResult) {
                    var itHtml = '      <p>' + this._convertInlineFormatting(itResult.beforeText) +
                        '<span class="infoTrigger" info="' + this._escAttr(itResult.definition) + '">' +
                        this._escContent(itResult.triggerWord) + '</span>' +
                        this._convertInlineFormatting(itResult.afterText) + '</p>';
                    if (inActivity) {
                        activityParts.push(itHtml);
                    } else {
                        pendingContent.push(itHtml);
                    }
                    i++;
                    continue;
                }
                // Fall through to interactive handler if extraction fails
            }

            // --- Hintslider rendering (Tier 1) ---
            if (tagName === 'hint_slider' && category === 'interactive') {
                flushPending();
                activityHasInteractive = true;
                var hsHtml = self._renderHintSlider(processedBlocks, i, rawBlocks, procToRawMap, consumedRawIndices);
                if (hsHtml) {
                    if (inActivity) {
                        activityParts.push(hsHtml.html);
                    } else {
                        htmlParts.push(self._wrapInRow(hsHtml.html, colClass));
                    }
                    // Mark consumed blocks
                    for (var hsci = 0; hsci < hsHtml.consumedRawIndices.length; hsci++) {
                        consumedRawIndices[hsHtml.consumedRawIndices[hsci]] = true;
                    }
                    i++;
                    continue;
                }
                // Fall through to generic interactive handler if rendering fails
            }

            // --- Flipcard rendering (Tier 1) ---
            if (tagName === 'flip_card' && category === 'interactive') {
                flushPending();
                activityHasInteractive = true;
                var fcHtml = self._renderFlipCard(processedBlocks, i, rawBlocks, procToRawMap, consumedRawIndices);
                if (fcHtml) {
                    if (inActivity) {
                        activityParts.push(fcHtml.html);
                    } else {
                        htmlParts.push(self._wrapInRow(fcHtml.html, colClass));
                    }
                    for (var fcci = 0; fcci < fcHtml.consumedRawIndices.length; fcci++) {
                        consumedRawIndices[fcHtml.consumedRawIndices[fcci]] = true;
                    }
                    i++;
                    continue;
                }
            }

            // --- Interactive components ---
            if (category === 'interactive') {
                flushPending();
                activityHasInteractive = true;
                // Track upload_to_dropbox interactives for activity class
                if (tagName === 'upload_to_dropbox') {
                    activityHasDropbox = true;
                }

                // Use InteractiveExtractor if available and we have raw blocks
                if (self._interactiveExtractor && rawBlocks && procToRawMap[i] !== undefined) {
                    var rawIdx = procToRawMap[i];
                    var pageFilename = pageData.filename || '';
                    var currentActivityId = inActivity ? (self._currentActivityId || null) : null;
                    var extractResult = self._interactiveExtractor.processInteractive(
                        rawBlocks, rawIdx, pageFilename, currentActivityId, inActivity
                    );

                    if (extractResult) {
                        // Collect reference entry
                        self.collectedInteractives.push(extractResult.referenceEntry);

                        // Mark raw blocks as consumed so we skip their processed equivalents
                        var consumedStart = rawIdx + 1; // the tag block itself is processed normally
                        var consumedEnd = rawIdx + extractResult.blocksConsumed;
                        for (var ci = consumedStart; ci < consumedEnd; ci++) {
                            consumedRawIndices[ci] = true;
                        }

                        if (inActivity) {
                            activityParts.push(extractResult.placeholderHtml);
                        } else {
                            htmlParts.push(extractResult.placeholderHtml);
                        }

                        i++;
                        continue;
                    }
                }

                // Fallback: simple placeholder if no extractor
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
                // Handle multiple heading tags in one block
                var headingTags = [];
                for (var ht = 0; ht < tags.length; ht++) {
                    if (tags[ht].normalised === 'heading') {
                        headingTags.push(tags[ht]);
                    }
                }

                if (headingTags.length > 1) {
                    var headingTexts = this._splitMultiHeadingText(pBlock);
                    for (var hti = 0; hti < headingTags.length; hti++) {
                        var mhLevel = headingTags[hti].level || 2;
                        var mhText = headingTexts[hti] || '';
                        if (mhLevel === 1) mhLevel = 2;
                        mhText = this._stripFullHeadingFormatting(mhText);
                        if (mhLevel < 2) mhLevel = 2;
                        if (mhLevel > 5) mhLevel = 5;
                        var mhTag = 'h' + mhLevel;
                        var mhInner = this._convertInlineFormatting(mhText);
                        mhInner = this._stripHeadingInlineTags(mhInner);
                        if (mhInner.trim()) {
                            var mhHtml = '      <' + mhTag + '>' + mhInner + '</' + mhTag + '>';
                            if (inActivity) {
                                activityParts.push(mhHtml);
                            } else {
                                pendingContent.push(mhHtml);
                            }
                        }
                    }
                    i++;
                    continue;
                }

                var headingLevel = primaryTag.level || null;
                var headingText = pBlock.cleanText || '';
                var isIncompleteHeading = !headingLevel;

                // Fallback for incomplete heading tags [H ] with no level
                if (isIncompleteHeading) {
                    headingLevel = self._lastHeadingLevel || 3;
                }

                // [H1] in body context renders as <h2>
                if (headingLevel === 1) {
                    headingLevel = 2;
                }

                // Strip full-heading bold/italic wrapping (docx artefact)
                headingText = this._stripFullHeadingFormatting(headingText);

                // "Lesson N" prefix rule for lesson pages:
                // Strip the "Lesson N" prefix from heading text for clean display.
                // The heading level is preserved as the writer specified it.
                if (pageData.type === 'lesson') {
                    var lessonPrefixMatch = headingText.match(/^Lesson\s+\d+\s+/i);
                    if (lessonPrefixMatch) {
                        headingText = headingText.substring(lessonPrefixMatch[0].length);
                    }
                }

                // Clamp heading level to 2-5
                if (headingLevel < 2) headingLevel = 2;
                if (headingLevel > 5) headingLevel = 5;

                // Track last heading level for incomplete heading fallback
                self._lastHeadingLevel = headingLevel;

                var hTag = 'h' + headingLevel;

                // Conservative ALL-CAPS detection for H2-H5 headings
                var allCapsWarning = false;
                if (headingText && headingLevel >= 2) {
                    var letters = headingText.replace(/[^a-zA-Z]/g, '');
                    var upperCount = headingText.replace(/[^A-Z]/g, '').length;
                    if (letters.length > 3 && upperCount / letters.length > 0.6) {
                        allCapsWarning = true;
                    }
                }

                var headingInner = this._convertInlineFormatting(headingText);
                headingInner = this._stripHeadingInlineTags(headingInner);
                var headingHtml = '';
                if (isIncompleteHeading) {
                    headingHtml += '      <!-- \u26A0\uFE0F DEV CHECK: Writer used [H ] with no level \u2014 defaulted to ' + hTag + ' -->\n';
                }
                if (allCapsWarning) {
                    headingHtml += '      <!-- \u26A0\uFE0F DEV CHECK: Heading appears to be ALL CAPS \u2014 should be Sentence case -->\n';
                }
                headingHtml += '      <' + hTag + '>' + headingInner + '</' + hTag + '>';

                if (inActivity) {
                    activityParts.push(headingHtml);
                } else {
                    pendingContent.push(headingHtml);
                }
                i++;
                continue;
            }

            // --- Hovertrigger inline rendering ---
            if (pBlock._hovertriggers && pBlock._hovertriggers.length > 0) {
                var htHtml = this._renderHovertriggerParagraph(pBlock);
                if (htHtml) {
                    if (inActivity) {
                        activityParts.push(htHtml);
                    } else {
                        pendingContent.push(htHtml);
                    }
                    i++;
                    continue;
                }
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
                var alertResult = this._collectAlertContent(processedBlocks, i);
                var alertInnerHtml = '';
                for (var ai = 0; ai < alertResult.paragraphs.length; ai++) {
                    alertInnerHtml += '          <p>' + this._convertInlineFormatting(alertResult.paragraphs[ai]) + '</p>\n';
                }
                var alertHtml = '    <div class="alert">\n' +
                    '      <div class="row">\n' +
                    '        <div class="col-12">\n' +
                    alertInnerHtml +
                    '        </div>\n' +
                    '      </div>\n' +
                    '    </div>';
                if (inActivity) {
                    activityParts.push(alertHtml);
                } else {
                    htmlParts.push(this._wrapInRow(alertHtml, colClass));
                }
                i += alertResult.blocksConsumed;
                continue;
            }

            // --- Important ---
            if (tagName === 'important') {
                flushPending();
                var impResult = this._collectAlertContent(processedBlocks, i);
                var impInnerHtml = '';
                for (var ii = 0; ii < impResult.paragraphs.length; ii++) {
                    impInnerHtml += '          <p>' + this._convertInlineFormatting(impResult.paragraphs[ii]) + '</p>\n';
                }
                var impHtml = '    <div class="alert solid">\n' +
                    '      <div class="row">\n' +
                    '        <div class="col-12">\n' +
                    impInnerHtml +
                    '        </div>\n' +
                    '      </div>\n' +
                    '    </div>';
                if (inActivity) {
                    activityParts.push(impHtml);
                } else {
                    htmlParts.push(this._wrapInRow(impHtml, colClass));
                }
                i += impResult.blocksConsumed;
                continue;
            }

            // --- Cultural alerts ---
            if (tagName === 'alert_cultural_wananga' ||
                tagName === 'alert_cultural_talanoa' ||
                tagName === 'alert_cultural_combined') {
                flushPending();
                var layout = tagName.replace('alert_cultural_', '');
                var cultResult = this._collectAlertContent(processedBlocks, i);
                var cultInnerHtml = '';
                for (var ci2 = 0; ci2 < cultResult.paragraphs.length; ci2++) {
                    cultInnerHtml += '          <p>' + this._convertInlineFormatting(cultResult.paragraphs[ci2]) + '</p>\n';
                }
                var cultHtml = '    <div class="alert cultural" layout="' + layout + '">\n' +
                    '      <div class="row">\n' +
                    '        <div class="col-12">\n' +
                    cultInnerHtml +
                    '        </div>\n' +
                    '      </div>\n' +
                    '    </div>';
                if (inActivity) {
                    activityParts.push(cultHtml);
                } else {
                    htmlParts.push(this._wrapInRow(cultHtml, colClass));
                }
                i += cultResult.blocksConsumed;
                continue;
            }

            // --- Whakatauki ---
            if (tagName === 'whakatauki') {
                var whakContent = this._collectMultiLineContent(processedBlocks, i, 3);
                // If there's only one line, try splitting on pipe separator
                if (whakContent.length === 1 && whakContent[0].indexOf(' | ') !== -1) {
                    var pipeParts = whakContent[0].split(' | ');
                    whakContent = [];
                    for (var pp = 0; pp < pipeParts.length; pp++) {
                        if (pipeParts[pp].trim()) whakContent.push(pipeParts[pp].trim());
                    }
                }
                var whakHtml = '    <div class="whakatauki">\n';
                for (var w = 0; w < whakContent.length; w++) {
                    whakHtml += '      <p>' + this._convertInlineFormatting(whakContent[w]) + '</p>\n';
                }
                whakHtml += '    </div>';
                if (inActivity) {
                    activityParts.push(whakHtml);
                } else {
                    pendingContent.push(whakHtml);
                }
                i++;
                continue;
            }

            // --- Quote ---
            if (tagName === 'quote') {
                var quoteLines = this._collectMultiLineContent(processedBlocks, i, 2);
                var quoteText = quoteLines[0] || '';
                var quoteAck = quoteLines.length > 1 ? quoteLines[1] : '';

                // If only one line, try splitting on attribution pattern (Issue 6)
                if (!quoteAck && quoteText) {
                    var ackSplit = this._splitQuoteAttribution(quoteText);
                    quoteText = ackSplit.quote;
                    quoteAck = ackSplit.attribution;
                }

                // Strip italic wrapping from quote text (docx artefact — CSS handles styling).
                // Handles both *text* and "*text*" and "* text"* patterns.
                quoteText = this._stripFullItalic(quoteText);
                // Also strip italic markers inside or around quote marks:
                // "*text"* → "text", *"text"* → "text"
                quoteText = quoteText
                    .replace(/^([""\u201C])\*/, '$1')    // "*text → "text
                    .replace(/\*([""\u201D])$/, '$1')    // text"* → text"
                    .replace(/^\*([""\u201C])/, '$1')    // *"text → "text
                    .replace(/([""\u201D])\*$/, '$1');   // text*" → text"

                // Add quotes if not already present
                if (quoteText && !quoteText.startsWith('"') && !quoteText.startsWith('\u201C')) {
                    quoteText = '\u201C' + quoteText + '\u201D';
                }

                var quoteConvertedText = this._convertInlineFormatting(quoteText);
                var quoteHtml = '      <p class="quoteText">' + quoteConvertedText + '</p>';
                if (quoteAck) {
                    quoteHtml += '\n      <p class="quoteAck">' +
                        this._convertInlineFormatting(quoteAck) + '</p>';
                }
                if (inActivity) {
                    activityParts.push(quoteHtml);
                } else {
                    pendingContent.push(quoteHtml);
                }
                i++;
                continue;
            }

            // --- Rhetorical question ---
            if (tagName === 'rhetorical_question') {
                var rqContent = this._collectBlockContent(processedBlocks, i);
                var rqHtml = '    <div class="rhetoricalQuestion">\n' +
                    '      <p>' + this._convertInlineFormatting(rqContent) + '</p>\n' +
                    '    </div>';
                if (inActivity) {
                    activityParts.push(rqHtml);
                } else {
                    pendingContent.push(rqHtml);
                }
                i++;
                continue;
            }

            // --- Video ---
            if (tagName === 'video') {
                var videoUrl = this._extractUrlFromContent(processedBlocks, i);
                var videoHtml = this._renderVideo(videoUrl, config);
                if (inActivity) {
                    activityParts.push(videoHtml);
                } else {
                    pendingContent.push(videoHtml);
                }
                i++;
                continue;
            }

            // --- Image ---
            if (tagName === 'image') {
                var imgInfo = this._extractImageInfo(processedBlocks, i);
                var imgHtml = this._renderImage(imgInfo, config);
                if (inActivity) {
                    activityParts.push(imgHtml);
                } else {
                    pendingContent.push(imgHtml);
                }
                i++;
                continue;
            }

            // --- Audio ---
            if (tagName === 'audio') {
                var audioFile = this._extractAudioFilename(processedBlocks, i);
                var audioHtml = '      <audio preload="none" src="audio/' +
                    this._escAttr(audioFile) + '" class="audioPlayer icon" title="max-width:300px"></audio>';
                if (inActivity) {
                    activityParts.push(audioHtml);
                } else {
                    pendingContent.push(audioHtml);
                }
                i++;
                continue;
            }

            // --- Button ---
            if (tagName === 'button') {
                var btnInfo = this._extractLinkInfo(processedBlocks, i);
                var btnHtml = '      <a href="' + this._escAttr(btnInfo.url) +
                    '" target="_blank"><div class="button">' +
                    this._convertInlineFormatting(btnInfo.text) + '</div></a>';
                if (inActivity) {
                    activityParts.push(btnHtml);
                } else {
                    pendingContent.push(btnHtml);
                }
                i++;
                continue;
            }

            // --- External link button ---
            if (tagName === 'external_link_button') {
                var elbInfo = this._extractLinkInfo(processedBlocks, i);
                var elbHtml = '      <a href="' + this._escAttr(elbInfo.url) +
                    '" target="_blank"><div class="externalButton">' +
                    this._convertInlineFormatting(elbInfo.text) + '</div></a>';
                if (inActivity) {
                    activityParts.push(elbHtml);
                } else {
                    pendingContent.push(elbHtml);
                }
                i++;
                continue;
            }

            // --- External link ---
            // [external link] renders the URL as a visible inline link within paragraph text.
            // The text before the tag is regular paragraph content; the URL after is the link.
            // This is different from [external link button] which creates a styled button.
            if (tagName === 'external_link') {
                var elInfo = this._extractExternalLinkInfo(processedBlocks, i);
                var elHtml;
                if (elInfo.beforeText && elInfo.beforeText.trim()) {
                    // Paragraph text before the tag + inline URL link
                    elHtml = '      <p>' + this._convertInlineFormatting(elInfo.beforeText) +
                        ' <a href="' + this._escAttr(elInfo.url) + '" target="_blank">' +
                        this._escContent(elInfo.url) + '</a>' +
                        (elInfo.afterPunctuation ? this._escContent(elInfo.afterPunctuation) : '') +
                        '</p>';
                } else {
                    // No preceding text — just the link
                    elHtml = '      <p><a href="' + this._escAttr(elInfo.url) + '" target="_blank">' +
                        this._escContent(elInfo.url) + '</a></p>';
                }
                if (inActivity) {
                    activityParts.push(elHtml);
                } else {
                    pendingContent.push(elHtml);
                }
                i++;
                continue;
            }

            // --- Go to journal ---
            if (tagName === 'go_to_journal') {
                var gojHtml = '      <h4 class="goJournal">Go to your journal</h4>';
                if (inActivity) {
                    activityParts.push(gojHtml);
                } else {
                    pendingContent.push(gojHtml);
                }
                i++;
                continue;
            }

            // --- Download journal ---
            if (tagName === 'download_journal') {
                var djModuleCode = pageData.moduleCode || 'MODULE';
                var djHtml = '      <a href="docs/' + this._escAttr(djModuleCode) +
                    ' Journal.docx" target="_blank"><div class="button downloadButton">Download journal</div></a>\n' +
                    '      <div class="hint"></div>\n' +
                    '      <div class="hintDropContent" hintType="oneDrive"></div>';
                if (inActivity) {
                    activityParts.push(djHtml);
                } else {
                    pendingContent.push(djHtml);
                }
                i++;
                continue;
            }

            // --- Supervisor button ---
            if (tagName === 'supervisor_button') {
                var supContent = this._collectBlockContent(processedBlocks, i);
                var supHtml = '    <div class="supervisorContainer">\n' +
                    '      <div class="supervisorButton"></div>\n' +
                    '      <div class="supervisorContent">\n' +
                    '        <p>' + this._convertInlineFormatting(supContent) + '</p>\n' +
                    '      </div>\n' +
                    '    </div>';
                if (inActivity) {
                    activityParts.push(supHtml);
                } else {
                    pendingContent.push(supHtml);
                }
                i++;
                continue;
            }

            // --- Sidebar blocks from layout table unwrapping ---
            if (pBlock._cellRole === 'sidebar_image' || pBlock._cellRole === 'sidebar_alert') {
                // Sidebar content from unwrapped layout tables.
                // Flush current pending content and create a side-by-side layout:
                // the pending content goes in col-md-8, the sidebar goes in col-md-4.
                var sidebarHtml = self._renderSidebarBlock(pBlock, config);
                if (sidebarHtml) {
                    if (inActivity) {
                        // Inside an activity, pair with recent activity content
                        activityHasSidebar = true;
                        var mainContent = '';
                        if (pendingContent.length > 0) {
                            mainContent = pendingContent.join('\n');
                            pendingContent = [];
                        } else if (activityParts.length > 0) {
                            // Use the last few activity parts as the main column
                            mainContent = activityParts.pop();
                        }
                        var sideRowHtml = self._wrapSideBySide(mainContent, sidebarHtml);
                        activityParts.push(sideRowHtml);
                    } else {
                        var sideMainContent = pendingContent.join('\n');
                        pendingContent = [];
                        var sideLayout = self._wrapSideBySide(sideMainContent, sidebarHtml);
                        htmlParts.push(sideLayout);
                    }
                }
                i++;
                continue;
            }

            // --- Table (tagged as [TABLE]) ---
            if (pBlock.type === 'table' && this._hasTableTag(pBlock)) {
                var tableHtml = this._renderTable(pBlock.data);
                if (inActivity) {
                    activityParts.push(tableHtml);
                } else {
                    pendingContent.push(tableHtml);
                }
                i++;
                continue;
            }

            // --- Layout table: body text + image side by side ---
            if (pBlock.type === 'table' && !this._hasTableTag(pBlock)) {
                var layoutInfo = this._detectLayoutTable(pBlock.data);
                if (layoutInfo) {
                    flushPending();
                    var layoutHtml = this._renderLayoutTable(layoutInfo, config);
                    if (inActivity) {
                        activityParts.push(layoutHtml);
                    } else {
                        htmlParts.push(layoutHtml);
                    }
                    i++;
                    continue;
                }
            }

            // --- Untagged table → grid layout ---
            if (pBlock.type === 'table' && !this._hasTableTag(pBlock)) {
                // Grid tables have their own row structure, so flush first
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
                var linkInfo = this._extractLinkInfo(processedBlocks, i);
                var linkHtml = '      <a href="' + this._escAttr(linkInfo.url) +
                    '" target="_blank">' + this._convertInlineFormatting(linkInfo.text) + '</a>';
                if (inActivity) {
                    activityParts.push(linkHtml);
                } else {
                    pendingContent.push(linkHtml);
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
            var finalActivityClass = activityHasDropbox
                ? 'activity dropbox'
                : (activityHasInteractive ? 'activity interactive' : 'activity');
            if (activityHasSidebar) finalActivityClass += ' alertPadding';
            var finalActivityNum = this._currentActivityId || '';
            var finalActivityHtml = '    <div class="' + finalActivityClass + '"' +
                (finalActivityNum ? ' number="' + this._escAttr(finalActivityNum) + '"' : '') + '>\n' +
                '      <div class="row">\n        <div class="col-12">\n' +
                activityParts.join('\n') + '\n' +
                '        </div>\n      </div>\n' +
                '    </div>';
            htmlParts.push(this._wrapInRow(finalActivityHtml, colClass));
        }

        return htmlParts.join('\n');
    }

    // ------------------------------------------------------------------
    // Internal: Inline formatting conversion
    // ------------------------------------------------------------------

    /**
     * Convert PageForge formatting markers to HTML.
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
     * Strip bold/italic formatting markers from heading text.
     * Headings should never have full-heading bold or italic wrapping
     * (these are .docx formatting artefacts).
     * Also merges consecutive bold segments into one clean heading.
     *
     * @param {string} text - Heading text with formatting markers
     * @returns {string} Text with heading-level formatting stripped
     */
    _stripFullHeadingFormatting(text) {
        if (!text) return '';
        var trimmed = text.trim();

        // Strip all bold markers ** from the heading
        // This handles: **text**, **part1** **part2**, etc.
        trimmed = trimmed.replace(/\*\*\*/g, ''); // strip *** (bold+italic) markers first
        trimmed = trimmed.replace(/\*\*/g, '');    // strip ** (bold) markers

        // Strip full-heading italic wrapping: *entire text*
        // Check if entire remaining text is wrapped in single *...*
        var innerTrimmed = trimmed.trim();
        if (innerTrimmed.charAt(0) === '*' && innerTrimmed.charAt(innerTrimmed.length - 1) === '*' &&
            innerTrimmed.charAt(1) !== '*' && innerTrimmed.charAt(innerTrimmed.length - 2) !== '*') {
            // Check if there's only one pair of * markers (full wrap, not partial italic)
            var starCount = 0;
            for (var j = 0; j < innerTrimmed.length; j++) {
                if (innerTrimmed.charAt(j) === '*') starCount++;
            }
            if (starCount === 2) {
                innerTrimmed = innerTrimmed.substring(1, innerTrimmed.length - 1);
            }
        }

        // Also strip any remaining single * markers that wrap the entire text
        // (handles cases where italic markers survive)
        innerTrimmed = innerTrimmed.replace(/^\*|\*$/g, '');

        // Collapse multiple spaces from marker removal
        innerTrimmed = innerTrimmed.replace(/\s{2,}/g, ' ').trim();

        return innerTrimmed;
    }

    /**
     * Strip <b> and <i> tags from heading HTML output.
     * Headings should never have inline bold/italic wrapping.
     *
     * @param {string} html - Heading inner HTML
     * @returns {string} HTML with <b>, </b>, <i>, </i> stripped
     */
    _stripHeadingInlineTags(html) {
        if (!html) return '';
        return html
            .replace(/<\/?b>/g, '')
            .replace(/<\/?i>/g, '')
            .replace(/\s{2,}/g, ' ')
            .trim();
    }

    /**
     * Split clean text from a block with multiple heading tags into
     * separate texts, one per heading tag.
     *
     * @param {Object} pBlock - Processed block with multiple heading tags
     * @returns {Array<string>} Array of heading text strings
     */
    _splitMultiHeadingText(pBlock) {
        var formattedText = pBlock.formattedText || '';
        var cleanText = pBlock.cleanText || '';

        // Try to split on the boundary between bold segments
        // Pattern: **heading1** **heading2** or **heading1** \n **heading2**
        var boldSegments = [];
        var boldRegex = /\*\*([^*]+)\*\*/g;
        var match;
        while ((match = boldRegex.exec(cleanText)) !== null) {
            boldSegments.push(match[1].trim());
        }

        if (boldSegments.length > 1) {
            return boldSegments;
        }

        // Fallback: try splitting on newline
        var lines = cleanText.split(/\n/).filter(function (l) { return l.trim(); });
        if (lines.length > 1) {
            return lines;
        }

        // Last resort: return as single text
        return [cleanText];
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
     * Collect all content paragraphs belonging to an alert/important block.
     * Consumes the tag block plus all following body-content paragraphs until
     * a structural boundary (heading, activity, interactive, styling, media,
     * or another tagged element).
     *
     * @param {Array<Object>} processedBlocks - All processed blocks
     * @param {number} index - Index of the alert tag block
     * @returns {Object} { paragraphs: Array<string>, blocksConsumed: number }
     */
    _collectAlertContent(processedBlocks, index) {
        var paragraphs = [];
        var block = processedBlocks[index];
        var tagBlockText = (block && block.cleanText) ? block.cleanText : '';
        if (tagBlockText.trim()) {
            paragraphs.push(tagBlockText);
        }

        var j = index + 1;
        while (j < processedBlocks.length) {
            var nextBlock = processedBlocks[j];
            var nextTags = nextBlock.tagResult ? nextBlock.tagResult.tags : [];
            var nextTag = nextTags.length > 0 ? nextTags[0] : null;

            // Stop at any tagged block (except body tag with no other structural meaning)
            if (nextTag) {
                var nextCat = nextTag.category;
                var nextName = nextTag.normalised;
                // Body tag means the next paragraph is regular body content — stop
                if (nextCat === 'body' || nextCat === 'heading' || nextCat === 'structural' ||
                    nextCat === 'interactive' || nextCat === 'styling' || nextCat === 'media' ||
                    nextCat === 'link' || nextCat === 'activity' ||
                    nextName === 'activity' || nextName === 'end_activity' ||
                    nextName === 'alert' || nextName === 'important' ||
                    nextName === 'alert_cultural_wananga' ||
                    nextName === 'alert_cultural_talanoa' ||
                    nextName === 'alert_cultural_combined') {
                    break;
                }
            }

            // Stop at table blocks
            if (nextBlock.type === 'table') break;

            // Consume untagged paragraphs (continuation of alert content)
            var nextText = (nextBlock.cleanText || '').trim();
            if (nextText) {
                paragraphs.push(nextText);
            }
            j++;
        }

        return { paragraphs: paragraphs, blocksConsumed: j - index };
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

    /**
     * Extract external link info: preceding paragraph text, URL, and trailing punctuation.
     * [external link] renders the URL as a visible inline link — the text before the tag
     * is regular paragraph content, not link text.
     *
     * @param {Array<Object>} processedBlocks - All processed blocks
     * @param {number} index - Current block index
     * @returns {Object} {beforeText, url, afterPunctuation}
     */
    _extractExternalLinkInfo(processedBlocks, index) {
        var block = processedBlocks[index];
        var formattedText = (block && block.formattedText) ? block.formattedText : '';
        var cleanText = (block && block.cleanText) ? block.cleanText : '';

        // Extract URL from formatted text or clean text
        var url = '';

        // Check for [LINK: URL] pattern
        var linkMatch = formattedText.match(/\[LINK:\s*([^\]]+)\]/);
        if (linkMatch) {
            url = linkMatch[1].trim();
        }

        // If no LINK marker, look for bare URL in clean text
        if (!url) {
            var urlMatch = cleanText.match(/https?:\/\/[^\s]+/);
            if (urlMatch) url = urlMatch[0];
        }

        // If no URL in this block, check next block
        if (!url && index + 1 < processedBlocks.length) {
            var nextBlock = processedBlocks[index + 1];
            if (nextBlock) {
                var nextClean = nextBlock.cleanText || '';
                var nextFormatted = nextBlock.formattedText || '';
                var nextUrlMatch = nextClean.match(/https?:\/\/[^\s]+/) ||
                    nextFormatted.match(/https?:\/\/[^\s\]]+/);
                if (nextUrlMatch) url = nextUrlMatch[0];
            }
        }

        // The text BEFORE the [external link] tag is the paragraph content
        var beforeText = cleanText.replace(/https?:\/\/[^\s]+/g, '').trim();

        // Extract trailing punctuation from the block (e.g., the "." between tag and URL)
        var afterPunctuation = '';
        // Check if cleanText has punctuation right after removing URLs
        var punctMatch = cleanText.match(/https?:\/\/[^\s]+([.!?,;:])/);
        if (!punctMatch) {
            // Check for punctuation in the formatted text between the tag and URL
            var fmtPunctMatch = formattedText.match(/\[external\s+link\]\s*\[\/RED TEXT\][^.!?,;:]*([.!?,;:])/i);
            if (fmtPunctMatch) {
                afterPunctuation = fmtPunctMatch[1];
            }
            // Also check for punctuation as a separate red text marker (e.g., 🔴[RED TEXT] . [/RED TEXT]🔴)
            var redPunctMatch = formattedText.match(/\[external\s+link\][\s\S]*?\[\/RED TEXT\]\uD83D\uDD34\s*\uD83D\uDD34\[RED TEXT\]\s*([.!?,;:])\s*\[\/RED TEXT\]\uD83D\uDD34/i);
            if (redPunctMatch) {
                afterPunctuation = redPunctMatch[1];
                // Remove the punctuation from beforeText if it leaked there
                if (beforeText.endsWith(afterPunctuation)) {
                    beforeText = beforeText.slice(0, -afterPunctuation.length).trim();
                }
            }
        }

        // Clean up trailing punctuation from beforeText
        // (The punctuation between tag and URL sometimes ends up in cleanText)
        if (afterPunctuation && beforeText.endsWith(afterPunctuation)) {
            beforeText = beforeText.slice(0, -afterPunctuation.length).trim();
        }

        return { beforeText: beforeText, url: url || '#', afterPunctuation: afterPunctuation };
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
                var cellContent = this._renderCellContent(cell);
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
                var pText = this._buildFormattedText(textCell.paragraphs[p]);
                var pTagResult = this._normaliser.processBlock(pText);
                var clean = (pTagResult.cleanText || '').trim();
                if (clean) textParagraphs.push(clean);
            }

            // Image cell
            var imgCell = row.cells[imageColIdx];
            for (var ip = 0; ip < imgCell.paragraphs.length; ip++) {
                var iPText = this._buildFormattedText(imgCell.paragraphs[ip]);
                var iTagResult = this._normaliser.processBlock(iPText);
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
     * Get all tags from a table cell's paragraphs.
     *
     * @param {Object} cell - Table cell data
     * @returns {Array<Object>} Tags found
     */
    _getTableCellTags(cell) {
        var tags = [];
        if (!cell || !cell.paragraphs) return tags;
        for (var p = 0; p < cell.paragraphs.length; p++) {
            var text = this._buildFormattedText(cell.paragraphs[p]);
            var tagResult = this._normaliser.processBlock(text);
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
                html += '        <p>' + this._convertInlineFormatting(layoutInfo.textParagraphs[t]) + '</p>\n';
            }
            html += '      </div>\n';
            html += '      <div class="' + imgColClass + '">\n';
            html += '        ' + this._renderImagePlaceholder(layoutInfo.imageRef, config) + '\n';
            html += '      </div>\n';
        } else {
            // Image left, text right
            html += '      <div class="' + imgColClass + '">\n';
            html += '        ' + this._renderImagePlaceholder(layoutInfo.imageRef, config) + '\n';
            html += '      </div>\n';
            html += '      <div class="' + textColClass + '">\n';
            for (var t2 = 0; t2 < layoutInfo.textParagraphs.length; t2++) {
                html += '        <p>' + this._convertInlineFormatting(layoutInfo.textParagraphs[t2]) + '</p>\n';
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
    _renderImagePlaceholder(imageRef, config) {
        var placeholderBase = (config.imageDefaults && config.imageDefaults.placeholderBase)
            ? config.imageDefaults.placeholderBase : 'https://placehold.co';
        var imgClass = (config.imageDefaults && config.imageDefaults.class)
            ? config.imageDefaults.class : 'img-fluid';

        // Extract iStock number for alt text if available
        var altText = '';
        if (imageRef) {
            var gmMatch = imageRef.match(/gm(\d+)/);
            if (gmMatch) {
                altText = 'iStock-' + gmMatch[1];
            }
        }

        var html = '<img class="' + imgClass + '" loading="lazy" src="' +
            placeholderBase + '/400x300?text=Image" alt="' + this._escAttr(altText) + '" />';

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
                '          ' + this._renderImagePlaceholder(imageUrl, config) + '\n' +
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
                    alertHtml += '          <h4>' + this._convertInlineFormatting(alertContent[ac]) + '</h4>\n';
                } else {
                    alertHtml += '          <p>' + this._convertInlineFormatting(alertContent[ac]) + '</p>\n';
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
    _wrapSideBySide(mainHtml, sidebarHtml) {
        var html = '    <div class="row">\n';
        html += '      <div class="col-md-8 col-12">\n';
        if (mainHtml && mainHtml.trim()) {
            html += mainHtml + '\n';
        }
        html += '      </div>\n';
        html += '      <div class="col-md-4 offset-md-0 col-12">\n';
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
            html += '            <p>' + this._convertInlineFormatting(hintRows[h].front) + '</p>\n';
            html += '          </div>\n';
            html += '          <div class="backInfo">\n';
            html += '            <p>' + this._convertInlineFormatting(hintRows[h].back) + '</p>\n';
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
                html += '            <h5>' + this._convertInlineFormatting(card.heading) + '</h5>\n';
            }
            if (card.image) {
                html += '            <img class="img-fluid" loading="lazy" src="images/' +
                    this._escAttr(card.image) + '" alt="Flipcard image" />\n';
            }
            html += '          </div>\n';
            html += '          <div class="back">\n';
            if (card.back) {
                html += '            <p>' + this._convertInlineFormatting(card.back) + '</p>\n';
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
            texts.push(this._buildFormattedText(cell.paragraphs[p]));
        }
        return texts.join(' / ');
    }

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

        // Use iStock number as alt text if available
        var altText = imgInfo.istockId || '';

        var html = '      <img class="img-fluid" loading="lazy" src="' +
            placeholderBase + '/' + dimensions + '?text=Image+Placeholder" alt="' +
            this._escAttr(altText) + '" />';

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
     * @param {Array|null} menuContentBlocks - Content blocks for menu tabs (overview only)
     * @returns {string} HTML with module menu populated
     */
    _replaceModuleMenuContent(html, pageData, config, moduleInfo, menuContentBlocks) {
        if (pageData.type === 'overview') {
            // Split menu content into Overview and Information tabs
            var tabContent = this._splitMenuContentIntoTabs(menuContentBlocks || [], config);

            // Overview page: populate tab content
            var overviewTab = this._generateOverviewTabContent(tabContent.overviewBlocks, config, moduleInfo);
            var infoTab = this._generateInfoTabContent(tabContent.infoBlocks, config, moduleInfo);

            html = html.replace(
                '              <!-- MODULE_MENU_CONTENT: Overview -->',
                overviewTab
            );
            html = html.replace(
                '              <!-- MODULE_MENU_CONTENT: Information -->',
                infoTab
            );

            // Handle Standards tab (NCEA)
            if (html.indexOf('<!-- MODULE_MENU_CONTENT: Standards -->') !== -1) {
                html = html.replace(
                    '              <!-- MODULE_MENU_CONTENT: Standards -->',
                    '              <!-- Standards content to be added -->'
                );
            }
        } else {
            // Lesson page: simplified menu with actual content from [Lesson Overview]
            var lessonMenu = this._generateLessonMenuContent(pageData, config, moduleInfo, menuContentBlocks);
            html = html.replace(
                '          <!-- MODULE_MENU_CONTENT -->',
                lessonMenu
            );
        }

        return html;
    }

    /**
     * Split menu content blocks into Overview tab and Information tab content.
     * Overview tab: H1 title + description, first two H2 sections (Learning Intentions + Success Criteria)
     * Information tab: Everything from the third H2 onwards
     *
     * @param {Array} blocks - Content blocks before MODULE INTRODUCTION
     * @param {Object} config - Template config
     * @returns {Object} { overviewBlocks: Array, infoBlocks: Array }
     */
    _splitMenuContentIntoTabs(blocks, config) {
        var processedBlocks = this._processAllBlocks(blocks);
        var h2Count = 0;
        var splitIndex = processedBlocks.length; // default: everything in overview

        for (var i = 0; i < processedBlocks.length; i++) {
            var pBlock = processedBlocks[i];
            var tags = pBlock.tagResult ? pBlock.tagResult.tags : [];
            for (var t = 0; t < tags.length; t++) {
                // Count H2 headings (skip H1 — that's the overview title, not a section)
                if (tags[t].normalised === 'heading' && tags[t].level === 2) {
                    h2Count++;
                    // Third H2 and beyond → Information tab
                    if (h2Count === 3) {
                        splitIndex = i;
                        break;
                    }
                }
            }
            if (splitIndex !== processedBlocks.length) break;
        }

        // Map processed blocks back to original blocks
        var overviewOrigBlocks = blocks.slice(0, splitIndex < processedBlocks.length ? this._getOriginalBlockIndex(blocks, processedBlocks, splitIndex) : blocks.length);
        var infoOrigBlocks = splitIndex < processedBlocks.length ? blocks.slice(this._getOriginalBlockIndex(blocks, processedBlocks, splitIndex)) : [];

        return {
            overviewBlocks: overviewOrigBlocks,
            infoBlocks: infoOrigBlocks
        };
    }

    /**
     * Map from processed block index back to original block index.
     *
     * @param {Array} originalBlocks - Original content blocks
     * @param {Array} processedBlocks - Processed blocks (some may be filtered)
     * @param {number} processedIndex - Index in processed blocks
     * @returns {number} Index in original blocks
     */
    _getOriginalBlockIndex(originalBlocks, processedBlocks, processedIndex) {
        if (processedIndex >= processedBlocks.length) return originalBlocks.length;
        // Count non-null blocks up to the target
        var origIdx = 0;
        var procCount = 0;
        for (var i = 0; i < originalBlocks.length; i++) {
            var block = originalBlocks[i];
            if (block.type === 'pageBreak') continue;
            if (block.type === 'paragraph' && block.data) {
                if (procCount === processedIndex) return i;
                procCount++;
            } else if (block.type === 'table' && block.data) {
                if (procCount === processedIndex) return i;
                procCount++;
            }
        }
        return originalBlocks.length;
    }

    /**
     * Generate Overview tab content for overview page module menu.
     * Contains: H1 overview title + description, Learning Intentions, Success Criteria
     *
     * @param {Array} blocks - Content blocks for overview tab
     * @param {Object} config - Template config
     * @param {Object} moduleInfo - Module info
     * @returns {string} HTML content
     */
    _generateOverviewTabContent(blocks, config, moduleInfo) {
        var indent = '              ';
        return this._renderModuleMenuBlocks(blocks, config, indent, true);
    }

    /**
     * Generate Information tab content.
     * Contains: Planning time, What do I need, Connections, etc.
     *
     * @param {Array} blocks - Content blocks for information tab
     * @param {Object} config - Template config
     * @param {Object} moduleInfo - Module info
     * @returns {string} HTML content
     */
    _generateInfoTabContent(blocks, config, moduleInfo) {
        var indent = '              ';
        if (!blocks || blocks.length === 0) {
            return indent + '<!-- Information tab content -->';
        }
        return this._renderModuleMenuBlocks(blocks, config, indent, false, true);
    }

    /**
     * Render content blocks for module menu tabs.
     * Uses h4 headings, strips italic from list items and body text,
     * normalises Success Criteria label.
     *
     * @param {Array} blocks - Raw content blocks
     * @param {Object} config - Template config
     * @param {string} indent - Base indentation string
     * @param {boolean} isOverviewTab - Whether this is the Overview tab (first h4 gets span)
     * @param {boolean} [isInfoTab] - Whether this is the Information tab (uses h5 headings)
     * @returns {string} HTML content for the tab
     */
    _renderModuleMenuBlocks(blocks, config, indent, isOverviewTab, isInfoTab) {
        var processedBlocks = this._processAllBlocks(blocks);
        var parts = [];
        var isFirstHeading = true;
        var successCriteriaHeading = (config.moduleMenu && config.moduleMenu.overviewPage &&
            config.moduleMenu.overviewPage.successCriteriaHeading)
            ? config.moduleMenu.overviewPage.successCriteriaHeading
            : 'How will I know if I\'ve learned it?';
        // Information tab uses h5 headings; Overview tab uses h4
        var menuHeadingTag = isInfoTab ? 'h5' : 'h4';
        var i = 0;
        var self = this;

        while (i < processedBlocks.length) {
            var pBlock = processedBlocks[i];
            var tags = pBlock.tagResult ? pBlock.tagResult.tags : [];
            var primaryTag = tags.length > 0 ? tags[0] : null;
            var tagName = primaryTag ? primaryTag.normalised : null;
            var category = primaryTag ? primaryTag.category : null;

            // Skip structural tags, whitespace-only, red-text-only with no content
            if (category === 'structural') { i++; continue; }
            if (pBlock.tagResult && pBlock.tagResult.isWhitespaceOnly) { i++; continue; }
            if (pBlock.tagResult && pBlock.tagResult.isRedTextOnly && tags.length === 0 && !pBlock.cleanText) { i++; continue; }

            // Headings → h4 (Bug 5)
            if (tagName === 'heading') {
                // Bug 9: Handle multiple heading tags in one block
                var menuHeadingTags = [];
                for (var mht = 0; mht < tags.length; mht++) {
                    if (tags[mht].normalised === 'heading') {
                        menuHeadingTags.push(tags[mht]);
                    }
                }

                if (menuHeadingTags.length > 1) {
                    // Multiple heading tags — split text and render each
                    var menuHeadingTexts = this._splitMultiHeadingText(pBlock);
                    for (var mhti = 0; mhti < menuHeadingTags.length; mhti++) {
                        var mhMenuText = menuHeadingTexts[mhti] || '';
                        mhMenuText = this._stripFullHeadingFormatting(mhMenuText);
                        mhMenuText = this._normaliseMenuHeading(mhMenuText, successCriteriaHeading);
                        var mhMenuInner = this._convertInlineFormatting(mhMenuText);
                        mhMenuInner = this._stripHeadingInlineTags(mhMenuInner);
                        if (mhMenuInner.trim()) {
                            parts.push(indent + '<' + menuHeadingTag + '>' + mhMenuInner + '</' + menuHeadingTag + '>');
                        }
                    }
                    isFirstHeading = false;
                    i++;
                    continue;
                }

                var headingText = pBlock.cleanText || '';
                headingText = this._stripFullHeadingFormatting(headingText);

                // If this is H1 in overview tab, split heading from description
                if (primaryTag.level === 1 && isOverviewTab && isFirstHeading) {
                    var h1Parts = this._splitH1HeadingAndDescription(pBlock);
                    // Heading with span (overview tab primary title)
                    parts.push(indent + '<' + menuHeadingTag + '><span>' + this._escContent(h1Parts.heading) + '</span></' + menuHeadingTag + '>');
                    if (h1Parts.description) {
                        parts.push(indent + '<p>' + this._escContent(h1Parts.description) + '</p>');
                    }
                    isFirstHeading = false;
                    i++;
                    continue;
                }

                // Normalise "Success Criteria" heading
                var normalisedHeading = this._normaliseMenuHeading(headingText, successCriteriaHeading);

                // Convert and strip inline formatting from headings
                var headingInner = this._convertInlineFormatting(normalisedHeading);
                headingInner = this._stripHeadingInlineTags(headingInner);

                if (isOverviewTab && isFirstHeading) {
                    parts.push(indent + '<' + menuHeadingTag + '><span>' + headingInner + '</span></' + menuHeadingTag + '>');
                } else {
                    parts.push(indent + '<' + menuHeadingTag + '>' + headingInner + '</' + menuHeadingTag + '>');
                }
                isFirstHeading = false;
                i++;
                continue;
            }

            // List items → strip italic (Bug 8)
            if (pBlock.data && pBlock.data.isListItem) {
                var listItems = [];
                while (i < processedBlocks.length) {
                    var lb = processedBlocks[i];
                    if (lb.data && lb.data.isListItem) {
                        listItems.push(lb);
                        i++;
                    } else {
                        break;
                    }
                }
                var listHtml = this._renderMenuList(listItems, indent);
                parts.push(listHtml);
                continue;
            }

            // Body text / paragraphs → strip italic (Bug 8)
            if (pBlock.cleanText && pBlock.cleanText.trim()) {
                var bodyText = pBlock.cleanText;
                // Strip full-paragraph italic wrapping from module menu content
                bodyText = this._stripFullItalic(bodyText);
                var bodyInner = this._convertInlineFormatting(bodyText);
                // Strip remaining italic tags from module menu content
                bodyInner = bodyInner.replace(/<\/?i>/g, '');
                parts.push(indent + '<p>' + bodyInner + '</p>');
            }

            i++;
        }

        if (parts.length === 0) {
            return indent + '<!-- No content -->';
        }

        // Wrap in row + col grid
        var gridIndent = indent;
        var wrapped = gridIndent + '<div class="row">\n';
        wrapped += gridIndent + '  <div class="col-md-8 col-12">\n';
        wrapped += parts.join('\n') + '\n';
        wrapped += gridIndent + '  </div>\n';
        wrapped += gridIndent + '</div>';

        return wrapped;
    }

    /**
     * Split an H1 heading block into heading text and description.
     * The bold portion is the heading, the italic portion is the description.
     *
     * @param {Object} pBlock - Processed block
     * @returns {Object} { heading: string, description: string }
     */
    _splitH1HeadingAndDescription(pBlock) {
        var formattedText = pBlock.formattedText || '';

        // Remove red text markers and tags
        var cleaned = formattedText.replace(/\uD83D\uDD34\[RED TEXT\]\s*[\s\S]*?\s*\[\/RED TEXT\]\uD83D\uDD34/g, '');
        cleaned = cleaned.replace(/\[([^\]]+)\]/g, '').trim();

        // Try to split bold heading from italic description
        // Pattern: **heading text***description text*
        // or: **heading text** *description text*
        var boldMatch = cleaned.match(/^\*\*([^*]+)\*\*\s*\*?([^*]*)\*?$/);
        if (boldMatch) {
            var heading = boldMatch[1].trim();
            var desc = boldMatch[2].trim();
            // Strip leading/trailing * from description
            desc = desc.replace(/^\*+|\*+$/g, '').trim();
            return { heading: heading, description: desc };
        }

        // Fallback: try splitting on the boundary between bold and italic markers
        var boldEndIdx = cleaned.indexOf('***');
        if (boldEndIdx !== -1) {
            // Pattern like: **heading***description*
            var beforeTriple = cleaned.substring(0, boldEndIdx).replace(/^\*\*/, '').trim();
            var afterTriple = cleaned.substring(boldEndIdx + 3).replace(/\*$/, '').trim();
            return { heading: beforeTriple, description: afterTriple };
        }

        // If no split possible, use clean text
        return { heading: pBlock.cleanText || '', description: '' };
    }

    /**
     * Normalise module menu heading text.
     * Replaces "Success Criteria" with the normalised version.
     *
     * @param {string} text - Heading text
     * @param {string} successCriteriaHeading - Normalised heading text
     * @returns {string} Normalised heading text
     */
    _normaliseMenuHeading(text, successCriteriaHeading) {
        if (!text) return '';
        var lower = text.toLowerCase().trim();
        if (lower === 'success criteria' || lower.indexOf('success criteria') === 0) {
            return successCriteriaHeading;
        }
        return text;
    }

    /**
     * Extract info trigger data from a processed block.
     * Looks for patterns where the clean text has a word followed by a definition
     * from the red text instructions.
     *
     * @param {Object} pBlock - Processed block
     * @returns {Object|null} { triggerWord, definition, beforeText, afterText } or null
     */
    _extractInfoTriggerData(pBlock) {
        var cleanText = (pBlock.cleanText || '').trim();
        var instructions = (pBlock.tagResult && pBlock.tagResult.redTextInstructions)
            ? pBlock.tagResult.redTextInstructions
            : [];

        // The definition is typically in the red text instruction
        var definition = instructions.length > 0 ? instructions[0].trim() : '';

        // Format multi-word definitions: capitalise first letter and add trailing period
        definition = this._formatInfoTriggerDefinition(definition);

        // The trigger word is the clean text (the visible word the reader clicks)
        if (cleanText && definition) {
            return {
                triggerWord: cleanText,
                definition: definition,
                beforeText: '',
                afterText: ''
            };
        }

        // If clean text has content but no definition, it might still be
        // an inline trigger where the definition comes from context
        if (cleanText && !definition) {
            return null; // Fall through to interactive handler
        }

        return null;
    }

    /**
     * Format an info trigger definition for the `info` attribute.
     * Single-word definitions are left as-is. Multi-word definitions
     * get a capitalised first letter and a trailing period.
     *
     * @param {string} definition - Raw definition text
     * @returns {string} Formatted definition
     */
    _formatInfoTriggerDefinition(definition) {
        if (!definition || typeof definition !== 'string') return definition || '';
        var trimmed = definition.trim();
        if (!trimmed) return trimmed;

        // Check if multi-word (more than one word)
        var words = trimmed.split(/\s+/);
        if (words.length <= 1) return trimmed;

        // Capitalise first letter
        var formatted = trimmed.charAt(0).toUpperCase() + trimmed.slice(1);

        // Add trailing period if not already present
        var lastChar = formatted.charAt(formatted.length - 1);
        if (lastChar !== '.' && lastChar !== '!' && lastChar !== '?') {
            formatted += '.';
        }

        return formatted;
    }

    /**
     * Render a paragraph containing hovertrigger(s) as <p> with infoTrigger spans.
     *
     * @param {Object} pBlock - Processed block with _hovertriggers data
     * @returns {string} HTML paragraph with infoTrigger spans
     */
    _renderHovertriggerParagraph(pBlock) {
        var formattedText = pBlock.formattedText || '';
        var triggers = pBlock._hovertriggers;

        // Process from last to first to preserve indices
        var result = formattedText;
        for (var t = triggers.length - 1; t >= 0; t--) {
            var trigger = triggers[t];
            // Replace the trigger word + hovertrigger pattern with infoTrigger span
            // The trigger word raw form (with formatting markers) is right before the red text block
            var beforePart = trigger.beforeText;
            var afterPart = trigger.afterText;
            var triggerWordFormatted = this._convertInlineFormatting(trigger.triggerWord);
            var formattedDef = this._formatInfoTriggerDefinition(trigger.definition);
            var infoSpan = '<span class="infoTrigger" info="' +
                this._escAttr(formattedDef) + '">' +
                triggerWordFormatted + '</span>';

            result = beforePart + infoSpan + afterPart;
        }

        // Clean up: remove red text markers, tags, and format the remaining text
        result = result.replace(/\uD83D\uDD34\[RED TEXT\]\s*[\s\S]*?\s*\[\/RED TEXT\]\uD83D\uDD34/g, '');
        result = result.replace(/\[([^\]]*)\]/g, '');
        result = result.replace(/\s+/g, ' ').trim();
        result = this._convertInlineFormatting(result);

        if (!result.trim()) return null;
        return '      <p>' + result + '</p>';
    }

    /**
     * Extract hovertrigger data from formatted text.
     * Detects the pattern: word 🔴[RED TEXT] [hovertrigger: [/RED TEXT]🔴 definition 🔴[RED TEXT] ] [/RED TEXT]🔴
     *
     * @param {string} formattedText - The formatted text with red text markers
     * @param {Object} paraData - The paragraph data with runs
     * @returns {Array|null} Array of hovertrigger objects or null
     */
    _extractHovertriggerData(formattedText, paraData) {
        if (!formattedText || formattedText.indexOf('hovertrigger') === -1) return null;

        var redTextMarker = '\uD83D\uDD34';
        // Pattern to detect hovertrigger: [hovertrigger: definition text ]
        // spread across red text boundaries
        var pattern = new RegExp(
            redTextMarker + '\\[RED TEXT\\]\\s*\\[hovertrigger\\s*:\\s*\\[/RED TEXT\\]' + redTextMarker +
            '\\s*([\\s\\S]*?)\\s*' +
            redTextMarker + '\\[RED TEXT\\]\\s*\\]\\s*\\[/RED TEXT\\]' + redTextMarker,
            'gi'
        );

        var triggers = [];
        var match;
        while ((match = pattern.exec(formattedText)) !== null) {
            var definition = match[1].trim();
            // Find the trigger word — the word(s) immediately before the hovertrigger tag
            var beforeText = formattedText.substring(0, match.index);
            // Extract last word(s) before the hovertrigger, stripping formatting markers
            var wordMatch = beforeText.match(/(\S+)\s*$/);
            var triggerWord = wordMatch ? wordMatch[1] : '';
            // Strip formatting markers from trigger word
            triggerWord = triggerWord.replace(/\*{1,3}/g, '').replace(/__/g, '');
            var beforeTrigger = beforeText.substring(0, beforeText.length - (wordMatch ? wordMatch[0].length : 0));
            var afterTrigger = formattedText.substring(match.index + match[0].length);

            triggers.push({
                triggerWord: triggerWord,
                definition: definition,
                fullMatch: match[0],
                matchIndex: match.index,
                beforeText: beforeTrigger,
                afterText: afterTrigger,
                triggerWordRaw: wordMatch ? wordMatch[1] : ''
            });
        }

        return triggers.length > 0 ? triggers : null;
    }

    /**
     * Split a quote string into quote text and attribution.
     * Looks for patterns like "quote text" By Author or "quote text" — Author
     *
     * @param {string} text - Full quote text
     * @returns {Object} { quote: string, attribution: string }
     */
    _splitQuoteAttribution(text) {
        if (!text) return { quote: '', attribution: '' };

        // Pattern 1: closing quote followed by "By" (case-insensitive)
        // Handles: "quote text" By Author, *"quote text"* By Author, etc.
        var byMatch = text.match(/^([\s\S]*?["\u201D\*])\s+(By\s+[\s\S]+)$/i);
        if (byMatch) {
            return { quote: byMatch[1].trim(), attribution: byMatch[2].trim() };
        }

        // Pattern 2: em dash separator
        var dashMatch = text.match(/^([\s\S]*?["\u201D\*])\s+[\u2014\u2013\-]{1,3}\s+([\s\S]+)$/);
        if (dashMatch) {
            return { quote: dashMatch[1].trim(), attribution: dashMatch[2].trim() };
        }

        // Pattern 3: Look for last sentence starting with "By " after any kind of quote mark
        var lastByIdx = text.lastIndexOf(' By ');
        if (lastByIdx === -1) lastByIdx = text.lastIndexOf(' by ');
        if (lastByIdx > 0) {
            var beforeBy = text.substring(0, lastByIdx).trim();
            // Only split if the "By" comes after a quote-ending character
            var lastChar = beforeBy.charAt(beforeBy.length - 1);
            if (lastChar === '"' || lastChar === '\u201D' || lastChar === '*' || lastChar === '.') {
                return {
                    quote: beforeBy,
                    attribution: text.substring(lastByIdx + 1).trim()
                };
            }
        }

        return { quote: text, attribution: '' };
    }

    /**
     * Strip italic markers from entire text (module menu content).
     *
     * @param {string} text - Text with formatting markers
     * @returns {string} Text with full-italic stripped
     */
    _stripFullItalic(text) {
        if (!text) return '';
        var trimmed = text.trim();
        // Strip wrapping * markers
        if (trimmed.charAt(0) === '*' && trimmed.charAt(trimmed.length - 1) === '*' &&
            trimmed.charAt(1) !== '*' && trimmed.charAt(trimmed.length - 2) !== '*') {
            return trimmed.substring(1, trimmed.length - 1);
        }
        return text;
    }

    /**
     * Render list items for module menu tabs (with italic stripping).
     *
     * @param {Array} items - Processed list item blocks
     * @param {string} indent - Base indentation
     * @returns {string} HTML list
     */
    _renderMenuList(items, indent) {
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

        return this._buildMenuNestedList(items, 0, listTag, indent);
    }

    /**
     * Build nested list for module menu (strips italic from items).
     *
     * @param {Array} items - List items
     * @param {number} level - Nesting level
     * @param {string} listTag - 'ul' or 'ol'
     * @param {string} indent - Base indentation
     * @returns {string} HTML list
     */
    _buildMenuNestedList(items, level, listTag, indent) {
        var levelIndent = indent + '  '.repeat(level);
        var html = levelIndent + '<' + listTag + '>\n';

        var i = 0;
        while (i < items.length) {
            var item = items[i];
            var itemLevel = (item.data && item.data.listLevel) ? item.data.listLevel : 0;

            if (itemLevel === level) {
                var text = item.cleanText || '';
                // Strip italic from list items in module menu (Bug 8)
                text = this._stripFullItalic(text);
                var itemInner = this._convertInlineFormatting(text);
                // Strip remaining italic tags
                itemInner = itemInner.replace(/<\/?i>/g, '');

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

                html += levelIndent + '  <li>' + itemInner;
                if (children.length > 0) {
                    html += '\n' + this._buildMenuNestedList(children, level + 1, listTag, indent) + '\n' + levelIndent + '  ';
                }
                html += '</li>\n';

                i = j;
            } else if (itemLevel > level) {
                i++;
            } else {
                break;
            }
        }

        html += levelIndent + '</' + listTag + '>';
        return html;
    }

    /**
     * Generate lesson page module menu content.
     * Routes [Lesson Overview] content into the menu with template config labels.
     *
     * @param {Object} pageData - Page data
     * @param {Object} config - Template config
     * @param {Object} moduleInfo - Module info
     * @param {Array|null} menuContentBlocks - Content blocks from [Lesson Overview]
     * @returns {string} HTML content
     */
    _generateLessonMenuContent(pageData, config, moduleInfo, menuContentBlocks) {
        var labels = (config.moduleMenu && config.moduleMenu.lessonPage && config.moduleMenu.lessonPage.labels)
            ? config.moduleMenu.lessonPage.labels
            : { learning: 'We are learning:', success: 'I can:' };
        var indent = '          ';

        if (!menuContentBlocks || menuContentBlocks.length === 0) {
            // No content — use empty placeholders
            var html = '';
            html += indent + '<h5>' + this._escContent(labels.learning) + '</h5>\n';
            html += indent + '<!-- Learning intentions content -->\n';
            html += indent + '<h5>' + this._escContent(labels.success) + '</h5>\n';
            html += indent + '<!-- Success criteria content -->';
            return html;
        }

        // Process the menu content blocks to find description, learning, and success sections
        var processedBlocks = this._processAllBlocks(menuContentBlocks);
        var parts = [];
        var descriptionParts = [];
        var learningItems = [];
        var successItems = [];
        var currentSection = 'description'; // before any recognised heading
        var i = 0;

        while (i < processedBlocks.length) {
            var pBlock = processedBlocks[i];
            var tags = pBlock.tagResult ? pBlock.tagResult.tags : [];
            var primaryTag = tags.length > 0 ? tags[0] : null;
            var category = primaryTag ? primaryTag.category : null;

            // Skip structural tags and whitespace
            if (category === 'structural') { i++; continue; }
            if (pBlock.tagResult && pBlock.tagResult.isWhitespaceOnly) { i++; continue; }
            if (pBlock.tagResult && pBlock.tagResult.isRedTextOnly && tags.length === 0 && !pBlock.cleanText) { i++; continue; }

            var cleanText = (pBlock.cleanText || '').trim();

            // Detect section boundaries by matching label-like text
            if (cleanText) {
                var lowerText = cleanText.toLowerCase().replace(/[*_]/g, '');
                if (lowerText.indexOf('we are learning') !== -1 ||
                    lowerText.indexOf('learning intention') !== -1) {
                    currentSection = 'learning';
                    i++;
                    continue;
                }
                if (lowerText.indexOf('i can') !== -1 ||
                    lowerText.indexOf('success criteria') !== -1 ||
                    lowerText.indexOf('you will show') !== -1 ||
                    lowerText.indexOf('how will i know') !== -1) {
                    currentSection = 'success';
                    i++;
                    continue;
                }
            }

            // Also check heading tags for section detection
            if (primaryTag && primaryTag.normalised === 'heading' && cleanText) {
                var lowerHeading = cleanText.toLowerCase().replace(/[*_]/g, '');
                if (lowerHeading.indexOf('we are learning') !== -1 ||
                    lowerHeading.indexOf('learning intention') !== -1) {
                    currentSection = 'learning';
                    i++;
                    continue;
                }
                if (lowerHeading.indexOf('i can') !== -1 ||
                    lowerHeading.indexOf('success criteria') !== -1 ||
                    lowerHeading.indexOf('you will show') !== -1 ||
                    lowerHeading.indexOf('how will i know') !== -1) {
                    currentSection = 'success';
                    i++;
                    continue;
                }
            }

            // Collect list items for menu sections.
            // Only collect bullet items for learning/success sections.
            // Ordered (numbered) list items are activity questions — stop consuming.
            if (pBlock.data && pBlock.data.isListItem) {
                var listItems = [];
                while (i < processedBlocks.length) {
                    var lb = processedBlocks[i];
                    if (lb.data && lb.data.isListItem) {
                        // Stop if this is an ordered (numbered) list item in success section
                        // — numbered items are activity questions, not success criteria
                        var listFmt = lb.data.listFormat || 'bullet';
                        if ((currentSection === 'success' || currentSection === 'learning') &&
                            listFmt !== 'bullet' && listItems.length > 0) {
                            break;
                        }
                        // Only include bullet items for learning/success sections
                        if ((currentSection === 'success' || currentSection === 'learning') &&
                            listFmt !== 'bullet') {
                            break;
                        }
                        listItems.push(lb);
                        i++;
                    } else {
                        break;
                    }
                }
                if (currentSection === 'learning') {
                    learningItems = learningItems.concat(listItems);
                } else if (currentSection === 'success') {
                    successItems = successItems.concat(listItems);
                }
                continue;
            }

            // Collect description paragraphs (before any heading section)
            if (currentSection === 'description' && cleanText) {
                descriptionParts.push(pBlock);
            }

            i++;
        }

        // Build HTML output
        var result = [];

        // Description paragraph(s)
        for (var d = 0; d < descriptionParts.length; d++) {
            var descText = descriptionParts[d].cleanText || '';
            descText = this._stripFullItalic(descText);
            var descInner = this._convertInlineFormatting(descText);
            descInner = descInner.replace(/<\/?i>/g, '');
            result.push(indent + '<p>' + descInner + '</p>');
        }

        // "We are learning:" heading + list
        result.push(indent + '<h5>' + this._escContent(labels.learning) + '</h5>');
        if (learningItems.length > 0) {
            result.push(this._renderMenuList(learningItems, indent));
        }

        // "I can:" / "You will show..." heading + list
        result.push(indent + '<h5>' + this._escContent(labels.success) + '</h5>');
        if (successItems.length > 0) {
            result.push(this._renderMenuList(successItems, indent));
        }

        return result.join('\n');
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
