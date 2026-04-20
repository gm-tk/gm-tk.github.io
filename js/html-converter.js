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

        /** @type {HtmlConverterContentHelpers} */
        this._content = new HtmlConverterContentHelpers(
            this._escContent.bind(this),
            this._escAttr.bind(this)
        );

        /** @type {HtmlConverterRenderers} */
        this._renderers = new HtmlConverterRenderers(
            this._content,
            this._escContent.bind(this),
            this._escAttr.bind(this),
            this
        );

        /** @type {HtmlConverterModuleMenu} */
        this._moduleMenu = new HtmlConverterModuleMenu(
            this._normaliser,
            this._content,
            this._renderers,
            this._escContent.bind(this),
            this._escAttr.bind(this),
            this
        );

        /** @type {HtmlConverterLessonMenu} */
        this._lessonMenu = new HtmlConverterLessonMenu(
            this._normaliser,
            this._content,
            this._escContent.bind(this),
            this._escAttr.bind(this),
            this
        );

        /** @type {HtmlConverterBlockRenderer} */
        this._blockRenderer = new HtmlConverterBlockRenderer(
            this._normaliser,
            this._interactiveExtractor,
            this._content,
            this._renderers,
            this._escContent.bind(this),
            this._escAttr.bind(this),
            this
        );

        /** @type {HtmlConverterBlockProcessor} */
        this._blockProcessor = new HtmlConverterBlockProcessor(
            this._normaliser,
            this
        );
    }

    _renderBlocks(processedBlocks, config, pageData, rawBlocks) {
        return this._blockRenderer._renderBlocks(processedBlocks, config, pageData, rawBlocks);
    }

    _processAllBlocks(blocks) {
        return this._blockProcessor._processAllBlocks(blocks);
    }

    _processBlock(block) {
        return this._blockProcessor._processBlock(block);
    }

    _buildFormattedText(para) {
        return this._blockProcessor._buildFormattedText(para);
    }

    _applyFormattingMarkers(text, fmt) {
        return this._blockProcessor._applyFormattingMarkers(text, fmt);
    }

    _buildTableTextForTags(table) {
        return this._blockProcessor._buildTableTextForTags(table);
    }

    _convertInlineFormatting(text) {
        return this._content._convertInlineFormatting(text);
    }

    _escapeContentPreservingTags(text) {
        return this._content._escapeContentPreservingTags(text);
    }

    _stripFullHeadingFormatting(text) {
        return this._content._stripFullHeadingFormatting(text);
    }

    _stripHeadingInlineTags(html) {
        return this._content._stripHeadingInlineTags(html);
    }

    _splitMultiHeadingText(pBlock) {
        return this._content._splitMultiHeadingText(pBlock);
    }

    _collectBlockContent(processedBlocks, index) {
        return this._content._collectBlockContent(processedBlocks, index);
    }

    _collectAlertContent(processedBlocks, index) {
        return this._content._collectAlertContent(processedBlocks, index);
    }

    _collectMultiLineContent(processedBlocks, index, expectedLines) {
        return this._content._collectMultiLineContent(processedBlocks, index, expectedLines);
    }

    _extractUrlFromContent(processedBlocks, index) {
        return this._content._extractUrlFromContent(processedBlocks, index);
    }

    _extractImageInfo(processedBlocks, index) {
        return this._content._extractImageInfo(processedBlocks, index);
    }

    _extractAudioFilename(processedBlocks, index) {
        return this._content._extractAudioFilename(processedBlocks, index);
    }

    _extractLinkInfo(processedBlocks, index) {
        return this._content._extractLinkInfo(processedBlocks, index);
    }

    _extractExternalLinkInfo(processedBlocks, index) {
        return this._content._extractExternalLinkInfo(processedBlocks, index);
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
