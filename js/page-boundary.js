/**
 * PageBoundary — Page boundary detection and validation engine for PageForge.
 *
 * Processes the parser's content blocks using TagNormaliser to identify
 * structural tags, applies 4 validation rules, and assigns content
 * blocks to output pages (HTML files).
 *
 * @see CLAUDE.md Section 11 — Page Boundary Validation Rules
 */

'use strict';

class PageBoundary {
    /**
     * Create a PageBoundary instance.
     *
     * @param {TagNormaliser} tagNormaliser - An initialised TagNormaliser instance
     */
    constructor(tagNormaliser) {
        if (!tagNormaliser) {
            throw new Error('PageBoundary requires a TagNormaliser instance');
        }

        /** @type {TagNormaliser} */
        this._normaliser = tagNormaliser;
    }

    // ------------------------------------------------------------------
    // Public API
    // ------------------------------------------------------------------

    /**
     * Process content blocks and return page assignments.
     *
     * @param {Array<Object>} contentBlocks - The parser's this.content array
     * @param {string} moduleCode - Module code string like "OSAI201"
     * @returns {Array<Object>} Array of page objects with assigned content
     */
    assignPages(contentBlocks, moduleCode) {
        if (!contentBlocks || contentBlocks.length === 0) {
            return [];
        }

        if (!moduleCode) {
            moduleCode = 'MODULE';
        }

        // Step 1: Scan all blocks and tag them with normalised structural info
        var taggedBlocks = this._tagAllBlocks(contentBlocks);

        // Step 2: Identify raw segments (split by structural markers)
        var rawSegments = this._identifyRawSegments(taggedBlocks);

        // Step 3: Apply the 4 page boundary validation rules
        var validatedSegments = this._applyValidationRules(rawSegments);

        // Step 4: Assign pages with filenames and lesson numbers
        var pages = this._assignPageMetadata(validatedSegments, moduleCode, contentBlocks);

        return pages;
    }

    // ------------------------------------------------------------------
    // Internal: Tag all blocks
    // ------------------------------------------------------------------

    /**
     * Run the tag normaliser on every content block and annotate them
     * with structural tag information.
     *
     * @param {Array<Object>} contentBlocks - Parser content blocks
     * @returns {Array<Object>} Annotated blocks with structural tag info
     */
    _tagAllBlocks(contentBlocks) {
        var tagged = [];

        for (var i = 0; i < contentBlocks.length; i++) {
            var block = contentBlocks[i];
            var blockText = this._getBlockText(block);
            var processed = this._normaliser.processBlock(blockText);

            tagged.push({
                index: i,
                block: block,
                processed: processed,
                structuralTags: this._extractStructuralTags(processed.tags),
                hasBodyContent: this._hasBodyContent(processed)
            });
        }

        return tagged;
    }

    /**
     * Extract the text content from a content block.
     *
     * @param {Object} block - A content block {type, data}
     * @returns {string} The text content of the block
     */
    _getBlockText(block) {
        if (block.type === 'paragraph' && block.data) {
            // Use the formatted text from the formatter's perspective
            // which includes red text markers and formatting
            return this._buildParagraphText(block.data);
        }
        if (block.type === 'table' && block.data) {
            return this._buildTableText(block.data);
        }
        return '';
    }

    /**
     * Build a text representation of a paragraph's runs, preserving
     * red text markers as the formatter would produce them.
     *
     * @param {Object} para - Paragraph data object
     * @returns {string} Text representation
     */
    _buildParagraphText(para) {
        if (!para.runs || para.runs.length === 0) {
            return para.text || '';
        }

        var text = '';
        for (var i = 0; i < para.runs.length; i++) {
            var run = para.runs[i];
            if (!run.text) continue;

            var chunk = run.text;
            var fmt = run.formatting || {};

            // Red text wrapping (matching formatter output)
            if (fmt.isRed) {
                chunk = '\uD83D\uDD34[RED TEXT] ' + chunk + ' [/RED TEXT]\uD83D\uDD34';
            }

            text += chunk;
        }

        return text;
    }

    /**
     * Build a text representation of a table (for tag extraction).
     *
     * @param {Object} table - Table data object
     * @returns {string} Combined text from all table cells
     */
    _buildTableText(table) {
        if (!table.rows) return '';

        var texts = [];
        for (var r = 0; r < table.rows.length; r++) {
            var row = table.rows[r];
            for (var c = 0; c < row.cells.length; c++) {
                var cell = row.cells[c];
                for (var p = 0; p < cell.paragraphs.length; p++) {
                    var paraText = this._buildParagraphText(cell.paragraphs[p]);
                    if (paraText) {
                        texts.push(paraText);
                    }
                }
            }
        }

        return texts.join(' ');
    }

    /**
     * Extract structural tags from a tags array.
     *
     * @param {Array<Object>} tags - Normalised tags
     * @returns {Array<Object>} Only the structural tags
     */
    _extractStructuralTags(tags) {
        var structural = [];
        for (var i = 0; i < tags.length; i++) {
            var tag = tags[i];
            if (tag.category === 'structural') {
                structural.push(tag);
            }
        }
        return structural;
    }

    /**
     * Determine if a processed block contains meaningful body content
     * (headings, body text, media, etc. — not just structural tags).
     *
     * @param {Object} processed - Result from tagNormaliser.processBlock()
     * @returns {boolean} True if the block has body content
     */
    _hasBodyContent(processed) {
        // Check for non-structural, non-empty content
        if (processed.cleanText && processed.cleanText.trim().length > 0) {
            return true;
        }

        // Check for content-bearing tags (heading, body, styling, media, activity, link, interactive)
        for (var i = 0; i < processed.tags.length; i++) {
            var tag = processed.tags[i];
            if (tag.category && tag.category !== 'structural') {
                if (tag.category === 'heading' || tag.category === 'body' ||
                    tag.category === 'styling' || tag.category === 'media' ||
                    tag.category === 'activity' || tag.category === 'link' ||
                    tag.category === 'interactive') {
                    return true;
                }
            }
        }

        return false;
    }

    // ------------------------------------------------------------------
    // Internal: Identify raw segments
    // ------------------------------------------------------------------

    /**
     * Split tagged blocks into raw segments based on structural markers.
     * A new segment starts at [TITLE BAR] or [LESSON].
     * Segments end at [END PAGE].
     *
     * @param {Array<Object>} taggedBlocks - Annotated blocks
     * @returns {Array<Object>} Raw segments
     */
    _identifyRawSegments(taggedBlocks) {
        var segments = [];
        var currentSegment = null;

        for (var i = 0; i < taggedBlocks.length; i++) {
            var tagged = taggedBlocks[i];
            var structTags = tagged.structuralTags;

            for (var t = 0; t < structTags.length; t++) {
                var sTag = structTags[t];

                if (sTag.normalised === 'title_bar' || sTag.normalised === 'lesson') {
                    // Start a new segment
                    if (currentSegment) {
                        segments.push(currentSegment);
                    }
                    currentSegment = {
                        type: sTag.normalised === 'title_bar' ? 'overview' : 'lesson',
                        lessonNumber: sTag.number || null,
                        blocks: [],
                        startIndex: tagged.index,
                        endIndex: null,
                        hasTitleBar: sTag.normalised === 'title_bar',
                        hasModuleIntro: false,
                        hasLessonContent: false,
                        hasEndPage: false,
                        hasBodyContent: false,
                        hasHeadingOrBody: false,
                        boundaryDecisions: []
                    };
                }

                if (sTag.normalised === 'module_introduction' && currentSegment) {
                    currentSegment.hasModuleIntro = true;
                }

                if (sTag.normalised === 'lesson_content' && currentSegment) {
                    currentSegment.hasLessonContent = true;
                }

                if (sTag.normalised === 'end_page' && currentSegment) {
                    currentSegment.hasEndPage = true;
                }
            }

            // Add block to current segment
            if (currentSegment) {
                currentSegment.blocks.push(tagged);
                currentSegment.endIndex = tagged.index + 1;

                if (tagged.hasBodyContent) {
                    currentSegment.hasBodyContent = true;
                }

                // Check for heading or body tags
                for (var j = 0; j < tagged.processed.tags.length; j++) {
                    var cat = tagged.processed.tags[j].category;
                    if (cat === 'heading' || cat === 'body') {
                        currentSegment.hasHeadingOrBody = true;
                    }
                }
            }
        }

        // Push final segment
        if (currentSegment) {
            segments.push(currentSegment);
        }

        return segments;
    }

    // ------------------------------------------------------------------
    // Internal: Apply validation rules
    // ------------------------------------------------------------------

    /**
     * Apply all 4 page boundary validation rules to the raw segments.
     *
     * @param {Array<Object>} segments - Raw segments from _identifyRawSegments
     * @returns {Array<Object>} Validated and potentially merged segments
     */
    _applyValidationRules(segments) {
        var result = segments.slice(); // shallow copy

        // Rule 1: Pre-MODULE-INTRODUCTION End Page → DISREGARD
        result = this._applyRule1(result);

        // Rule 2: Missing End Page Between Lessons → INSERT
        result = this._applyRule2(result);

        // Rule 3: Empty Lesson Segment → DISREGARD End Page
        result = this._applyRule3(result);

        // Rule 4: Orphaned Title Bar → MERGE
        result = this._applyRule4(result);

        return result;
    }

    /**
     * Rule 1: If [End page] appears between [TITLE BAR] and [MODULE INTRODUCTION],
     * disregard it. Title bar + module introduction combine into single -00 page.
     *
     * @param {Array<Object>} segments - Current segments
     * @returns {Array<Object>} Updated segments
     */
    _applyRule1(segments) {
        // Look for overview segments with end_page but before module_introduction
        // If there's a title_bar segment followed by a module_introduction segment,
        // and the title_bar segment has an end_page, merge them.
        for (var i = 0; i < segments.length; i++) {
            var seg = segments[i];

            if (seg.type === 'overview' && seg.hasTitleBar && seg.hasEndPage && !seg.hasModuleIntro) {
                // Check if next segment has MODULE INTRODUCTION
                if (i + 1 < segments.length && segments[i + 1].type === 'overview' &&
                    segments[i + 1].hasModuleIntro) {
                    // Merge: combine this segment with the next
                    var nextSeg = segments[i + 1];
                    seg.blocks = seg.blocks.concat(nextSeg.blocks);
                    seg.endIndex = nextSeg.endIndex;
                    seg.hasModuleIntro = true;
                    seg.hasEndPage = nextSeg.hasEndPage;
                    seg.hasBodyContent = seg.hasBodyContent || nextSeg.hasBodyContent;
                    seg.hasHeadingOrBody = seg.hasHeadingOrBody || nextSeg.hasHeadingOrBody;
                    seg.hasLessonContent = seg.hasLessonContent || nextSeg.hasLessonContent;
                    seg.boundaryDecisions.push({
                        rule: 1,
                        action: 'disregard_end_page',
                        reason: 'End page before MODULE INTRODUCTION — merged with next segment'
                    });

                    // Remove the next segment
                    segments.splice(i + 1, 1);
                }
            }

            // Also handle the case where end_page is within the same segment
            // before module_introduction appears
            if (seg.type === 'overview' && seg.hasTitleBar && seg.hasEndPage && seg.hasModuleIntro) {
                // The end_page between title_bar and module_introduction should be ignored
                // This is already handled by being in the same segment
                seg.boundaryDecisions.push({
                    rule: 1,
                    action: 'disregard_end_page',
                    reason: 'End page within title bar + module introduction segment'
                });
            }
        }

        return segments;
    }

    /**
     * Rule 2: If [LESSON n] appears without a preceding [End page] since
     * the previous lesson, insert an implicit boundary.
     * (Already handled by segment splitting — each LESSON starts a new segment)
     *
     * @param {Array<Object>} segments - Current segments
     * @returns {Array<Object>} Updated segments
     */
    _applyRule2(segments) {
        // Since _identifyRawSegments already splits at each [LESSON], this rule
        // is automatically satisfied. We just need to detect when a previous
        // lesson segment didn't have an [End page] and note the implicit boundary.
        for (var i = 1; i < segments.length; i++) {
            var prevSeg = segments[i - 1];
            var currSeg = segments[i];

            if (currSeg.type === 'lesson' && prevSeg.type === 'lesson' && !prevSeg.hasEndPage) {
                prevSeg.boundaryDecisions.push({
                    rule: 2,
                    action: 'insert_boundary',
                    reason: 'Missing End page before lesson — implicit boundary inserted'
                });
            }
        }

        return segments;
    }

    /**
     * Rule 3: If a segment has [LESSON] but NO body tags AND NO [Lesson content],
     * disregard the closing [End page].
     *
     * @param {Array<Object>} segments - Current segments
     * @returns {Array<Object>} Updated segments
     */
    _applyRule3(segments) {
        var result = [];

        for (var i = 0; i < segments.length; i++) {
            var seg = segments[i];

            if (seg.type === 'lesson' && !seg.hasHeadingOrBody && !seg.hasLessonContent && seg.hasEndPage) {
                // Empty lesson — merge with next segment if possible
                seg.boundaryDecisions.push({
                    rule: 3,
                    action: 'disregard_end_page',
                    reason: 'Empty lesson segment (no body tags or lesson content) — end page disregarded'
                });

                if (i + 1 < segments.length) {
                    // Merge blocks into next segment
                    var nextSeg = segments[i + 1];
                    nextSeg.blocks = seg.blocks.concat(nextSeg.blocks);
                    nextSeg.startIndex = seg.startIndex;
                    nextSeg.boundaryDecisions = seg.boundaryDecisions.concat(nextSeg.boundaryDecisions);
                } else {
                    // No next segment — just discard the empty segment
                    result.push(seg);
                }
                continue;
            }

            result.push(seg);
        }

        return result;
    }

    /**
     * Rule 4: If a segment contains ONLY [TITLE BAR] + headings + [End page]
     * with no body content, merge it with the following segment.
     *
     * @param {Array<Object>} segments - Current segments
     * @returns {Array<Object>} Updated segments
     */
    _applyRule4(segments) {
        var result = [];

        for (var i = 0; i < segments.length; i++) {
            var seg = segments[i];

            if (seg.hasTitleBar && !seg.hasModuleIntro && !seg.hasBodyContent && seg.hasEndPage) {
                // Orphaned title bar — merge with next segment
                seg.boundaryDecisions.push({
                    rule: 4,
                    action: 'merge_with_next',
                    reason: 'Orphaned title bar (no module introduction, no body content) — merged with next segment'
                });

                if (i + 1 < segments.length) {
                    var nextSeg = segments[i + 1];
                    nextSeg.blocks = seg.blocks.concat(nextSeg.blocks);
                    nextSeg.startIndex = seg.startIndex;
                    nextSeg.hasTitleBar = true;
                    nextSeg.boundaryDecisions = seg.boundaryDecisions.concat(nextSeg.boundaryDecisions);

                    // If the next segment is a lesson, it becomes overview
                    if (nextSeg.type === 'lesson') {
                        nextSeg.type = 'overview';
                    }
                } else {
                    // No next segment — keep it as-is
                    result.push(seg);
                }
                continue;
            }

            result.push(seg);
        }

        return result;
    }

    // ------------------------------------------------------------------
    // Internal: Assign page metadata
    // ------------------------------------------------------------------

    /**
     * Assign filenames, lesson numbers, and types to validated segments.
     *
     * @param {Array<Object>} segments - Validated segments
     * @param {string} moduleCode - Module code string
     * @param {Array<Object>} contentBlocks - Original content blocks array
     * @returns {Array<Object>} Page objects with full metadata
     */
    _assignPageMetadata(segments, moduleCode, contentBlocks) {
        var pages = [];
        var lessonCounter = 0;

        for (var i = 0; i < segments.length; i++) {
            var seg = segments[i];
            var page = {};

            if (seg.type === 'overview') {
                page.type = 'overview';
                page.lessonNumber = null;
                page.filename = moduleCode + '-00.html';
            } else {
                lessonCounter++;
                var lessonNum = seg.lessonNumber || lessonCounter;
                // If explicit lesson number was provided, sync counter
                if (seg.lessonNumber) {
                    lessonCounter = seg.lessonNumber;
                    lessonNum = seg.lessonNumber;
                }

                page.type = 'lesson';
                page.lessonNumber = lessonNum;
                page.filename = moduleCode + '-' + this._zeroPad(lessonNum) + '.html';
            }

            page.contentBlocks = [];
            page.startIndex = seg.startIndex;
            page.endIndex = seg.endIndex;
            page.boundaryDecisions = seg.boundaryDecisions;

            // Collect actual content blocks for this page
            for (var b = 0; b < seg.blocks.length; b++) {
                var blockIndex = seg.blocks[b].index;
                if (blockIndex < contentBlocks.length) {
                    page.contentBlocks.push(contentBlocks[blockIndex]);
                }
            }

            pages.push(page);
        }

        return pages;
    }

    /**
     * Zero-pad a number to 2 digits.
     *
     * @param {number} num - Number to pad
     * @returns {string} Zero-padded string
     */
    _zeroPad(num) {
        return num < 10 ? '0' + num : '' + num;
    }
}
