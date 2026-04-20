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

        /** @type {HtmlConverterRenderers} */
        this._renderers = new HtmlConverterRenderers(
            null,
            this._escContent.bind(this),
            this._escAttr.bind(this),
            this
        );

        /** @type {HtmlConverterModuleMenu} */
        this._moduleMenu = new HtmlConverterModuleMenu(
            this._normaliser,
            null,
            this._renderers,
            this._escContent.bind(this),
            this._escAttr.bind(this),
            this
        );

        /** @type {HtmlConverterLessonMenu} */
        this._lessonMenu = new HtmlConverterLessonMenu(
            this._normaliser,
            null,
            this._escContent.bind(this),
            this._escAttr.bind(this),
            this
        );
    }

    _generateLessonMenuContent(pageData, config, moduleInfo, menuContentBlocks) {
        return this._lessonMenu.generateLessonMenuContent(pageData, config, moduleInfo, menuContentBlocks);
    }

    _replaceModuleMenuContent(html, pageData, config, moduleInfo, menuContentBlocks) {
        return this._moduleMenu.replaceModuleMenuContent(html, pageData, config, moduleInfo, menuContentBlocks);
    }

    _splitMenuContentIntoTabs(blocks, config) {
        return this._moduleMenu.splitMenuContentIntoTabs(blocks, config);
    }

    _renderModuleMenuBlocks(blocks, config, indent, isOverviewTab, isInfoTab) {
        return this._moduleMenu.renderModuleMenuBlocks(blocks, config, indent, isOverviewTab, isInfoTab);
    }

    _formatInfoTriggerDefinition(definition) {
        return this._moduleMenu.formatInfoTriggerDefinition(definition);
    }

    _stripFullItalic(text) {
        return this._moduleMenu._stripFullItalic(text);
    }

    _renderMenuList(items, indent) {
        return this._moduleMenu._renderMenuList(items, indent);
    }

    _extractHovertriggerData(formattedText, paraData) {
        return this._moduleMenu._extractHovertriggerData(formattedText, paraData);
    }

    _extractInfoTriggerData(pBlock) {
        return this._moduleMenu._extractInfoTriggerData(pBlock);
    }

    _renderHovertriggerParagraph(pBlock) {
        return this._moduleMenu._renderHovertriggerParagraph(pBlock);
    }

    _splitQuoteAttribution(text) {
        return this._moduleMenu._splitQuoteAttribution(text);
    }

    _renderTable(tableData) {
        return this._renderers.renderTable(tableData);
    }

    _renderCellContent(cell) {
        return this._renderers.renderCellContent(cell);
    }

    _renderTableAsGrid(tableData) {
        return this._renderers._renderTableAsGrid(tableData);
    }

    _detectLayoutTable(tableData) {
        return this._renderers._detectLayoutTable(tableData);
    }

    _renderLayoutTable(layoutInfo, config) {
        return this._renderers._renderLayoutTable(layoutInfo, config);
    }

    _renderImagePlaceholder(imageRef, config) {
        return this._renderers.renderImagePlaceholder(imageRef, config);
    }

    _renderImage(imgInfo, config) {
        return this._renderers.renderImage(imgInfo, config);
    }

    _renderVideo(url, config) {
        return this._renderers.renderVideo(url, config);
    }

    _renderSidebarBlock(pBlock, config) {
        return this._renderers._renderSidebarBlock(pBlock, config);
    }

    _renderList(items) {
        return this._renderers._renderList(items);
    }

    _wrapInRow(content, colClass) {
        return this._renderers._wrapInRow(content, colClass);
    }

    _wrapSideBySide(mainHtml, sidebarHtml, mainColClass, sidebarColClass) {
        return this._renderers._wrapSideBySide(mainHtml, sidebarHtml, mainColClass, sidebarColClass);
    }

    _hasTableTag(pBlock) {
        return this._renderers._hasTableTag(pBlock);
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

        // Phase 13: For lesson pages, extract the lesson-specific title from the
        // first [H2] heading in the body content (the lesson's own title). Strip
        // "Lesson N:" prefix for display. Passed to the skeleton so the header
        // <h1> uses the lesson title rather than the module title.
        var lessonTitle = null;
        if (pageData.type === 'lesson') {
            lessonTitle = this._extractLessonTitle(bodyPageData.contentBlocks);
        }

        var skeletonData = {
            type: pageData.type,
            lessonNumber: pageData.lessonNumber,
            filename: pageData.filename,
            moduleCode: moduleInfo.moduleCode,
            englishTitle: moduleInfo.englishTitle || '',
            tereoTitle: moduleInfo.tereoTitle || null,
            lessonTitle: lessonTitle,
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

    /**
     * Extract the lesson-specific title from body content blocks.
     *
     * Phase 13: Lesson pages display the lesson's own title (the first [H2]
     * heading following [Lesson Content]) in the header <h1>, not the module
     * title. The "Lesson N:" prefix is stripped here (via TemplateEngine
     * helper) when the skeleton is generated.
     *
     * @param {Array<Object>} bodyBlocks - Body content blocks for the lesson
     * @returns {string|null} Raw heading text of the first [H2], or null if none found
     */
    _extractLessonTitle(bodyBlocks) {
        if (!bodyBlocks || bodyBlocks.length === 0) return null;

        for (var i = 0; i < bodyBlocks.length; i++) {
            var block = bodyBlocks[i];
            if (block.type !== 'paragraph' || !block.data) continue;
            var text = this._buildFormattedText(block.data);
            var tagResult = this._normaliser.processBlock(text);
            var tags = tagResult.tags || [];
            for (var t = 0; t < tags.length; t++) {
                var tag = tags[t];
                // First [H1] or [H2] heading tag in the body is the lesson title.
                if (tag.category === 'heading' && (tag.level === 1 || tag.level === 2)) {
                    var clean = (tagResult.cleanText || '').trim();
                    if (clean) {
                        // Strip wrapping bold/italic artefacts from .docx output
                        clean = this._stripFullHeadingFormatting(clean);
                        return clean;
                    }
                }
            }
        }
        return null;
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

        // Change 2: suppressDuplicateLessonTitleH2 flag. When enabled on a
        // lesson page, skip the first body block if it is an [H2] whose text
        // matches the extracted lesson title (after stripping leading
        // "Lesson N:" / "Lesson N -" / "Lesson N." prefixes and italic/bold
        // markers). Default OFF — no behaviour change unless opted in.
        var _skipDuplicateLessonH2Index = -1;
        if (config && config.contentRules &&
            config.contentRules.suppressDuplicateLessonTitleH2 === true &&
            pageData && pageData.type === 'lesson') {
            for (var _fi = 0; _fi < processedBlocks.length; _fi++) {
                var _fb = processedBlocks[_fi];
                if (!_fb) continue;
                var _fbTags = _fb.tagResult ? _fb.tagResult.tags : [];
                var _fbTag = _fbTags.length > 0 ? _fbTags[0] : null;
                var _fbText = (_fb.cleanText || '').trim();
                if (!_fbTag && !_fbText) continue;
                if (_fbTag && _fbTag.normalised === 'heading' &&
                    (_fbTag.level === 1 || _fbTag.level === 2)) {
                    var _rawHeading = self._stripFullHeadingFormatting(_fbText);
                    var _lessonTitleForCmp = (pageData.lessonTitle ||
                        self._extractLessonTitle(pageData.contentBlocks || []) || '');
                    var _norm = function (s) {
                        return (s || '').replace(/\*+/g, '')
                            .replace(/^Lesson\s+\d+\s*[:.\-]\s*/i, '')
                            .trim().toLowerCase();
                    };
                    var _nh = _norm(_rawHeading);
                    var _nl = _norm(_lessonTitleForCmp);
                    if (_nh && _nl && _nh === _nl) {
                        _skipDuplicateLessonH2Index = _fi;
                    }
                }
                break;
            }
        }

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
            if (i === _skipDuplicateLessonH2Index) {
                i++;
                continue;
            }
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
                    // Session G — `inActivity` is threaded into processInteractive so
                    // the Session F boundary algorithm can apply activity-aware
                    // close rules (H4 / H5 scaffolding inside an activity does
                    // NOT close the inner interactive). Activity-level wrap
                    // (open / close on [Activity N], [end activity], H2, etc.)
                    // remains owned by this loop's `inActivity` flag below.
                    var extractResult = self._interactiveExtractor.processInteractive(
                        rawBlocks, rawIdx, pageFilename, currentActivityId, inActivity
                    );

                    if (extractResult) {
                        // Collect reference entry
                        self.collectedInteractives.push(extractResult.referenceEntry);

                        // Mark raw blocks as consumed so we skip their processed equivalents.
                        // Session G — also consume the boundary range computed by the
                        // Session F algorithm so any blocks captured by the boundary
                        // (childBlocks, conversation entries, writer notes, inline
                        // media, primary data table) are not duplicated as body
                        // content outside the placeholder.
                        var consumedStart = rawIdx + 1; // the tag block itself is processed normally
                        var consumedEnd = rawIdx + extractResult.blocksConsumed;
                        for (var ci = consumedStart; ci < consumedEnd; ci++) {
                            consumedRawIndices[ci] = true;
                        }
                        if (typeof extractResult.endBlockIndex === 'number' &&
                            extractResult.endBlockIndex > rawIdx) {
                            for (var bi = rawIdx + 1; bi <= extractResult.endBlockIndex; bi++) {
                                consumedRawIndices[bi] = true;
                            }
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

                // Layout-table pairing: when the immediately-following blocks
                // carry _unwrappedFrom: 'layout_table' metadata, consume the
                // main-content cell paragraphs as the alert's body content and
                // pair an adjacent sidebar block (image/alert) side-by-side.
                var ltMainStart = i + 1;
                var ltMainEnd = ltMainStart;
                while (ltMainEnd < processedBlocks.length) {
                    var ltb = processedBlocks[ltMainEnd];
                    if (ltb && ltb._unwrappedFrom === 'layout_table' && ltb._cellRole === 'main_content') {
                        ltMainEnd++;
                    } else {
                        break;
                    }
                }
                var ltHasMain = (ltMainEnd > ltMainStart);
                var ltSidebarBlock = null;
                if (ltHasMain && ltMainEnd < processedBlocks.length) {
                    var ltSb = processedBlocks[ltMainEnd];
                    if (ltSb && (ltSb._cellRole === 'sidebar_image' || ltSb._cellRole === 'sidebar_alert') &&
                        (ltSb._sidebarImageUrl !== undefined || ltSb._sidebarAlertContent !== undefined)) {
                        ltSidebarBlock = ltSb;
                    }
                }

                if (ltHasMain) {
                    var ltInnerHtml = '';
                    var ltTagText = (pBlock.cleanText || '').trim();
                    if (ltTagText) {
                        ltInnerHtml += '          <p>' + this._convertInlineFormatting(ltTagText) + '</p>\n';
                    }
                    var ltk = ltMainStart;
                    while (ltk < ltMainEnd) {
                        var ltMblk = processedBlocks[ltk];
                        if (ltMblk.data && ltMblk.data.isListItem) {
                            var ltListItems = [];
                            while (ltk < ltMainEnd && processedBlocks[ltk].data && processedBlocks[ltk].data.isListItem) {
                                ltListItems.push(processedBlocks[ltk]);
                                ltk++;
                            }
                            ltInnerHtml += this._renderList(ltListItems) + '\n';
                        } else {
                            var ltT = (ltMblk.cleanText || '').trim();
                            if (ltT) {
                                ltInnerHtml += '          <p>' + this._convertInlineFormatting(ltT) + '</p>\n';
                            }
                            ltk++;
                        }
                    }
                    var ltAlertHtml = '    <div class="alert">\n' +
                        '      <div class="row">\n' +
                        '        <div class="col-12">\n' +
                        ltInnerHtml +
                        '        </div>\n' +
                        '      </div>\n' +
                        '    </div>';
                    var ltBlocksConsumed = ltMainEnd - i;
                    if (ltSidebarBlock) {
                        var ltSidebarInner;
                        if (ltSidebarBlock._cellRole === 'sidebar_image') {
                            ltSidebarInner = '      ' + this._renderImagePlaceholder(ltSidebarBlock._sidebarImageUrl || '', config);
                        } else {
                            ltSidebarInner = this._renderSidebarBlock(ltSidebarBlock, config);
                        }
                        var ltPairedHtml = this._wrapSideBySide(
                            ltAlertHtml,
                            ltSidebarInner,
                            'col-md-6 col-12 paddingR',
                            'col-md-3 col-12 paddingL'
                        );
                        if (inActivity) {
                            activityParts.push(ltPairedHtml);
                        } else {
                            htmlParts.push(ltPairedHtml);
                        }
                        ltBlocksConsumed += 1;
                    } else {
                        if (inActivity) {
                            activityParts.push(ltAlertHtml);
                        } else {
                            htmlParts.push(this._wrapInRow(ltAlertHtml, colClass));
                        }
                    }
                    i += ltBlocksConsumed;
                    continue;
                }

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
