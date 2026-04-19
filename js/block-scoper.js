/**
 * BlockScoper — Block Scoping Engine for PageForge.
 *
 * Scans normalised content blocks and groups them into hierarchical blocks.
 * A "block" is a container element (accordion, carousel, flip cards, activity, etc.)
 * that contains child content until an explicit closing tag or implicit boundary.
 *
 * @see CLAUDE.md — Block Scoping System
 */

'use strict';

class BlockScoper {
    /**
     * Create a BlockScoper instance.
     *
     * @param {TagNormaliser} tagNormaliser - An initialised TagNormaliser instance
     */
    constructor(tagNormaliser) {
        if (!tagNormaliser) {
            throw new Error('BlockScoper requires a TagNormaliser instance');
        }

        /** @type {TagNormaliser} */
        this._normaliser = tagNormaliser;

        /** Maximum lookahead lines before auto-closing a block */
        this.LOOKAHEAD_LIMIT = 200;

        /** @type {Array<Object>} Warnings generated during scoping */
        this.warnings = [];

        this._tables = new BlockScoperTables();
        this._subtagMatcher = new BlockSubtagMatcher(this._tables);
        this._tagMatcher = new BlockTagMatcher(this._tables, this.detectWriterInstruction.bind(this));
    }

    /** Delegation shim: `_lastCardFrontIndex` lives on the sub-matcher. */
    get _lastCardFrontIndex() { return this._subtagMatcher._lastCardFrontIndex; }
    set _lastCardFrontIndex(v) { this._subtagMatcher._lastCardFrontIndex = v; }

    /**
     * Delegation shim: normalise a sub-tag via BlockSubtagMatcher.
     */
    normaliseSubTag(tagText, parentBlockType, lastIndex) {
        return this._subtagMatcher.normaliseSubTag(tagText, parentBlockType, lastIndex);
    }

    /** Delegation shim: match an opening block tag. */
    _matchOpeningTag(tags, block) {
        return this._tagMatcher._matchOpeningTag(tags, block);
    }

    /** Delegation shim: match a closing block tag. */
    _matchClosingTag(tags, blockStack) {
        return this._tagMatcher._matchClosingTag(tags, blockStack);
    }

    /** Delegation shim: detect a hard boundary tag. */
    _isHardBoundary(tags) {
        return this._tagMatcher._isHardBoundary(tags);
    }

    /** Delegation shim: extract writer notes embedded in a block-opening tag. */
    _extractWriterNotesFromTag(tagInner, blockType) {
        return this._tagMatcher._extractWriterNotesFromTag(tagInner, blockType);
    }

    /** Delegation shim: fuzzy-match a block-closing tag. */
    _fuzzyMatchCloser(lowerText) {
        return this._tagMatcher._fuzzyMatchCloser(lowerText);
    }

    // ------------------------------------------------------------------
    // Public API
    // ------------------------------------------------------------------

    /**
     * Scan content blocks and produce hierarchical block scope data.
     *
     * @param {Array<Object>} contentBlocks - The parser's content array
     * @returns {Array<Object>} Array of block scope objects plus unscoped content
     */
    scopeBlocks(contentBlocks) {
        if (!contentBlocks || contentBlocks.length === 0) {
            return [];
        }

        this.warnings = [];
        this._lastCardFrontIndex = null;
        var result = [];
        var blockStack = []; // stack of currently open blocks
        var i = 0;

        while (i < contentBlocks.length) {
            var block = contentBlocks[i];
            var tagInfo = this._getBlockTags(block);

            // Check if this is a closing tag for an open block
            var closerMatch = this._matchClosingTag(tagInfo, blockStack);
            if (closerMatch) {
                // Close the matching block
                var closedBlock = this._closeBlock(closerMatch.block, i, block, false, null);
                // Remove from stack
                var stackIdx = blockStack.indexOf(closerMatch.block);
                if (stackIdx !== -1) {
                    blockStack.splice(stackIdx, 1);
                }
                // If this block was nested, add it as a child of the parent
                if (blockStack.length > 0) {
                    blockStack[blockStack.length - 1].children.push(closedBlock);
                } else {
                    result.push(closedBlock);
                }
                i++;
                continue;
            }

            // Check if this is a block-opening tag
            var openerInfo = this._matchOpeningTag(tagInfo, block);
            if (openerInfo) {
                // Check if opening same type → implicit close of previous
                for (var s = blockStack.length - 1; s >= 0; s--) {
                    if (blockStack[s].blockType === openerInfo.blockType &&
                        blockStack[s].blockType !== 'activity') {
                        // Implicit close: same type reopen
                        var implicitClosed = this._closeBlock(
                            blockStack[s], i, null, true, 'same_type_reopen'
                        );
                        blockStack.splice(s, 1);
                        if (blockStack.length > 0) {
                            blockStack[blockStack.length - 1].children.push(implicitClosed);
                        } else {
                            result.push(implicitClosed);
                        }
                        break;
                    }
                }

                // Check for implicit boundary closures (activity closes preceding interactive)
                if (openerInfo.blockType === 'activity') {
                    for (var a = blockStack.length - 1; a >= 0; a--) {
                        if (blockStack[a].blockType !== 'activity') {
                            var activityClosed = this._closeBlock(
                                blockStack[a], i, null, true, 'next_activity'
                            );
                            blockStack.splice(a, 1);
                            if (blockStack.length > 0) {
                                blockStack[blockStack.length - 1].children.push(activityClosed);
                            } else {
                                result.push(activityClosed);
                            }
                        }
                    }
                }

                // Open new block
                var newBlock = {
                    blockType: openerInfo.blockType,
                    openingTag: openerInfo.rawTag,
                    closingTag: null,
                    implicitClose: false,
                    implicitCloseReason: null,
                    writerNotes: openerInfo.writerNotes || [],
                    layoutModifiers: openerInfo.layoutModifiers || {},
                    lineStart: i,
                    lineEnd: null,
                    children: [],
                    _contentItems: [] // internal: raw content within block
                };

                blockStack.push(newBlock);
                i++;
                continue;
            }

            // Check for hard boundary (end page, lesson, etc.)
            var isHardBoundary = this._isHardBoundary(tagInfo);
            if (isHardBoundary && blockStack.length > 0) {
                // Close ALL open blocks
                while (blockStack.length > 0) {
                    var lastBlock = blockStack.pop();
                    var hardClosed = this._closeBlock(
                        lastBlock, i, block, true, isHardBoundary
                    );
                    if (blockStack.length > 0) {
                        blockStack[blockStack.length - 1].children.push(hardClosed);
                    } else {
                        result.push(hardClosed);
                    }
                }
                // The boundary block itself is unscoped content
                result.push({ type: 'unscoped', blockIndex: i, block: block });
                i++;
                continue;
            }

            // Check for sub-element markers within current block
            if (blockStack.length > 0) {
                var currentBlock = blockStack[blockStack.length - 1];
                var subElement = this._matchSubElement(tagInfo, currentBlock, block);
                if (subElement) {
                    currentBlock.children.push(subElement);
                    i++;
                    continue;
                }

                // Regular content within a block
                currentBlock._contentItems.push({ blockIndex: i, block: block });

                // Check lookahead limit
                var linesSinceOpen = i - currentBlock.lineStart;
                if (linesSinceOpen >= this.LOOKAHEAD_LIMIT) {
                    this.warnings.push(
                        'Block \'' + currentBlock.blockType + '\' opened at line ' +
                        currentBlock.lineStart + ' has no closing tag — auto-closed after 200-line lookahead limit'
                    );
                    var limitClosed = this._closeBlock(
                        currentBlock, i, null, true, 'lookahead_limit'
                    );
                    blockStack.pop();
                    if (blockStack.length > 0) {
                        blockStack[blockStack.length - 1].children.push(limitClosed);
                    } else {
                        result.push(limitClosed);
                    }
                }
            } else {
                // Unscoped content
                result.push({ type: 'unscoped', blockIndex: i, block: block });
            }

            i++;
        }

        // Close any remaining open blocks at end of document
        while (blockStack.length > 0) {
            var remaining = blockStack.pop();
            this.warnings.push(
                'Block \'' + remaining.blockType + '\' opened at line ' +
                remaining.lineStart + ' has no closing tag — auto-closed at end of document'
            );
            var endClosed = this._closeBlock(
                remaining, contentBlocks.length - 1, null, true, 'end_of_document'
            );
            if (blockStack.length > 0) {
                blockStack[blockStack.length - 1].children.push(endClosed);
            } else {
                result.push(endClosed);
            }
        }

        return result;
    }


    /**
     * Split compound tag text into individual tag instructions.
     *
     * @param {string} text - Text potentially containing multiple bracket pairs
     * @returns {Array<Object>} Array of split tag results
     */
    splitCompoundTags(text) {
        if (!text || typeof text !== 'string') return [];

        // Find all bracket pairs
        var bracketPairs = [];
        var bracketRegex = /\[([^\]]+)\]/g;
        var match;
        var lastEnd = 0;

        while ((match = bracketRegex.exec(text)) !== null) {
            bracketPairs.push({
                full: match[0],
                inner: match[1].trim(),
                start: match.index,
                end: match.index + match[0].length
            });
            lastEnd = match.index + match[0].length;
        }

        if (bracketPairs.length === 0) return [];
        if (bracketPairs.length === 1) {
            // Single tag — check for "image of X and HN" pattern
            var entry = { tag: bracketPairs[0].full, inner: bracketPairs[0].inner };
            var imageOfMatch = bracketPairs[0].inner.match(
                /^image\s+of\s+(.+?)\s+and\s+(H\d)$/i
            );
            if (imageOfMatch) {
                entry.imageDescription = imageOfMatch[1];
                entry.headingLevel = imageOfMatch[2].toUpperCase();
            }
            // Check for trailing text
            var trailing = text.substring(lastEnd).trim();
            if (trailing) {
                entry.trailingText = trailing;
            }
            return [entry];
        }

        // Multiple bracket pairs — split them
        var results = [];
        for (var i = 0; i < bracketPairs.length; i++) {
            var entry = { tag: bracketPairs[i].full, inner: bracketPairs[i].inner };

            // Check for "image of X and HN" pattern
            var imageOfMatch = bracketPairs[i].inner.match(
                /^image\s+of\s+(.+?)\s+and\s+(H\d)$/i
            );
            if (imageOfMatch) {
                entry.imageDescription = imageOfMatch[1];
                entry.headingLevel = imageOfMatch[2].toUpperCase();
            }

            results.push(entry);
        }

        // Trailing text after last bracket
        var trailingText = text.substring(lastEnd).trim();
        if (trailingText) {
            results[results.length - 1].trailingText = trailingText;
        }

        return results;
    }

    /**
     * Extract layout direction from a tag.
     *
     * @param {string} tagText - The raw tag text (inner, without brackets)
     * @returns {Object|null} Layout info { coreType, position, description, style }
     */
    extractLayoutDirection(tagText) {
        if (!tagText || typeof tagText !== 'string') return null;

        var cleaned = tagText.toLowerCase().trim();
        var original = tagText.trim();

        // --- Image layout patterns ---

        // [image embedded to the left with text to the right]
        var embeddedMatch = cleaned.match(
            /^image\s+embedded\s+to\s+the\s+(left|right)\s+with\s+text\s+to\s+the\s+(left|right)$/
        );
        if (embeddedMatch) {
            return { coreType: 'image', position: embeddedMatch[1], description: null, style: null };
        }

        // [image right] / [image left]
        var imgPosMatch = cleaned.match(/^image\s+(right|left)$/);
        if (imgPosMatch) {
            return { coreType: 'image', position: imgPosMatch[1], description: null, style: null };
        }

        // [image] of / [image] description
        var imgDescMatch = cleaned.match(/^image\]?\s+(?:of\s+)?(.+)/i);
        if (imgDescMatch && !cleaned.match(/^image\s+(right|left|zoom|label|hover|embedded)/)) {
            return { coreType: 'image', position: 'default', description: imgDescMatch[1], style: null };
        }

        // [insert image hover with captions]
        if (cleaned.match(/insert\s+image\s+hover/)) {
            return { coreType: 'image', position: 'hover', description: null, style: null };
        }

        // [insert images and captions side by side]
        if (cleaned.match(/insert\s+images?\s+.*side\s+by\s+side/)) {
            return { coreType: 'image', position: 'side-by-side', description: null, style: null };
        }

        // [Flip card image]
        if (cleaned.match(/^flip\s+card\s+image/)) {
            return { coreType: 'image', position: 'default', description: null, style: 'flip_card' };
        }

        // --- Body layout patterns ---

        // [Body left] / [Body right]
        var bodyPosMatch = cleaned.match(/^body\s+(left|right)$/);
        if (bodyPosMatch) {
            return { coreType: 'body', position: bodyPosMatch[1], description: null, style: null };
        }

        // [Body, bold]
        if (cleaned.match(/^body\s*,\s*bold/)) {
            return { coreType: 'body', position: 'default', description: null, style: 'bold' };
        }

        // [Body, bullet points]
        if (cleaned.match(/^body\s*,\s*bullet/)) {
            return { coreType: 'body', position: 'default', description: null, style: 'bullet' };
        }

        // [Body – please emphasise...]
        if (cleaned.match(/^body\s+[\u2013\-–]+\s+please/)) {
            return { coreType: 'body', position: 'default', description: null, style: 'bold' };
        }

        // [Body text after Activity N]
        if (cleaned.match(/^body\s+text\s+after/)) {
            return { coreType: 'body', position: 'default', description: null, style: null };
        }

        return null;
    }

    /**
     * Detect layout pairs (image+body side-by-side grouping).
     *
     * @param {Array<Object>} blocks - Processed blocks with layout info
     * @returns {Array<Object>} Blocks with layout pairs grouped
     */
    detectLayoutPairs(blocks) {
        if (!blocks || blocks.length < 2) return blocks;

        var result = [];
        var i = 0;

        while (i < blocks.length) {
            if (i + 1 < blocks.length) {
                var current = blocks[i].layoutInfo;
                var next = blocks[i + 1].layoutInfo;

                if (current && next &&
                    current.position !== 'default' && next.position !== 'default' &&
                    current.coreType !== next.coreType &&
                    ((current.coreType === 'image' && next.coreType === 'body') ||
                     (current.coreType === 'body' && next.coreType === 'image'))) {
                    result.push({
                        type: 'layout_pair',
                        columns: [
                            { position: current.position, contentType: current.coreType, content: blocks[i] },
                            { position: next.position, contentType: next.coreType, content: blocks[i + 1] }
                        ]
                    });
                    i += 2;
                    continue;
                }
            }
            result.push(blocks[i]);
            i++;
        }

        return result;
    }

    /**
     * Detect whether a tag is a writer instruction / developer note.
     *
     * @param {string} tagText - The raw tag text (inner, without brackets)
     * @returns {Object} { isWriterNote, isButtonLabel, label, noteText }
     */
    detectWriterInstruction(tagText) {
        if (!tagText || typeof tagText !== 'string') {
            return { isWriterNote: false, isButtonLabel: false, label: null, noteText: null };
        }

        var cleaned = tagText.trim();
        var lower = cleaned.toLowerCase();

        // Rule D: [Button] followed by short label vs long instruction
        var buttonMatch = lower.match(/^button\]?\s+(.+)$/);
        if (buttonMatch || lower === 'button') {
            if (buttonMatch) {
                var afterButton = cleaned.substring(cleaned.toLowerCase().indexOf(buttonMatch[1].charAt(0)));
                // Recapture from original to preserve case
                afterButton = cleaned.replace(/^button\]?\s+/i, '').trim();
                var wordCount = afterButton.split(/\s+/).length;
                if (wordCount <= 3) {
                    return { isWriterNote: false, isButtonLabel: true, label: afterButton, noteText: null };
                } else {
                    return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
                }
            }
            return { isWriterNote: false, isButtonLabel: false, label: null, noteText: null };
        }

        // Rule C: Button tags that are instructions
        if (lower.match(/^self[\s-]marking\s+button/)) {
            return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
        }
        if (lower.match(/^reset\s+button\s+to/)) {
            return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
        }
        if (lower.match(/^learning\s+journal\s+button/)) {
            return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
        }

        // Rule A: Known instruction prefixes
        var instructionPrefixes = [
            /^cs\s*[\u2013\-–,:]/, /^cs\s/,
            /^dev\b/i, /^dev\s*[\u2013\-–,:]/, /^dev\s+team/,
            /^please\s+(create|make|find|put|insert|display|provide)/,
            /^create\s+(a|clipart|two|three)/,
            /^note\s*[:\s]/, /^note\s+for/,
            /^if\s+correct\b/,
            /^all\s+images\s+in\s+this/,
            /^add\s+a\s+(button|picture|visual)/,
            /^add\s+visuals/,
            /^checks\s+should\s+align/,
            /^include\s+only/,
            /^these\s+buttons\s+were/,
            /^students\s+to\s+select/
        ];

        for (var p = 0; p < instructionPrefixes.length; p++) {
            if (lower.match(instructionPrefixes[p])) {
                return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
            }
        }

        // Rule B: Contains known instruction-only patterns
        if (lower.indexOf('dev team') !== -1 || lower.indexOf('creative services') !== -1) {
            return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
        }
        if (lower.indexOf('copyright') !== -1 || lower.indexOf('permission') !== -1) {
            return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
        }

        // Full sentence detection (>15 words, no recognizable tag keyword at start)
        var words = cleaned.split(/\s+/);
        if (words.length > 15) {
            var firstWord = lower.split(/\s+/)[0];
            var tagKeywords = [
                'image', 'body', 'video', 'accordion', 'carousel', 'flip',
                'drag', 'drop', 'tab', 'slide', 'activity', 'alert',
                'button', 'h1', 'h2', 'h3', 'h4', 'h5', 'heading',
                'lesson', 'title', 'front', 'back', 'modal', 'speech',
                'important', 'quote', 'embed', 'audio', 'mcq', 'radio',
                'checklist', 'reorder', 'dropdown', 'end'
            ];
            if (tagKeywords.indexOf(firstWord) === -1) {
                return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
            }
        }

        // "please" in text but not starting with known element tag
        if (lower.indexOf('please') !== -1) {
            var firstSigWord = lower.split(/\s+/)[0];
            var elementTagWords = [
                'image', 'body', 'video', 'accordion', 'carousel', 'flip',
                'drag', 'tab', 'slide', 'activity', 'alert', 'button',
                'h1', 'h2', 'h3', 'h4', 'h5', 'front', 'back', 'modal',
                'embed', 'insert'
            ];
            if (elementTagWords.indexOf(firstSigWord) === -1) {
                return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
            }
        }

        // Conditional instructions
        if (lower.match(/^if\s+(they|the|correct|clicking)/)) {
            return { isWriterNote: true, isButtonLabel: false, label: null, noteText: cleaned };
        }

        return { isWriterNote: false, isButtonLabel: false, label: null, noteText: null };
    }

    /**
     * Infer interactive type from table structure when no explicit tag is present.
     *
     * @param {Object} tableData - Table data object from parser
     * @returns {Object} { inferredType, confidence }
     */
    inferInteractiveFromTable(tableData) {
        if (!tableData || !tableData.rows || tableData.rows.length === 0) {
            return { inferredType: null, confidence: 'none' };
        }

        var rows = tableData.rows;
        var numCols = rows[0].cells ? rows[0].cells.length : 0;

        if (numCols === 0) {
            return { inferredType: null, confidence: 'none' };
        }

        // Check for True/False pattern
        if (numCols === 2) {
            var tfCount = 0;
            var correctMarkers = 0;
            for (var r = 0; r < rows.length; r++) {
                if (rows[r].cells && rows[r].cells.length >= 2) {
                    var cellText = this._getCellText(rows[r].cells[1]).toLowerCase().trim();
                    if (cellText === 'true' || cellText === 'false' ||
                        cellText === 'true/false' || cellText === 'true or false') {
                        tfCount++;
                    }
                    // Check for bold markers
                    if (this._cellHasBold(rows[r].cells[1])) {
                        correctMarkers++;
                    }
                }
            }
            // If more than half rows have T/F values
            if (tfCount > rows.length * 0.5) {
                return { inferredType: 'radio_quiz_true_false', confidence: 'high' };
            }
        }

        // Check for [Correct] markers in cells
        for (var cr = 0; cr < rows.length; cr++) {
            if (rows[cr].cells) {
                for (var cc = 0; cc < rows[cr].cells.length; cc++) {
                    var cellContent = this._getCellText(rows[cr].cells[cc]);
                    if (cellContent.match(/\[correct\]/i)) {
                        if (numCols >= 3) {
                            return { inferredType: 'multichoice_quiz', confidence: 'high' };
                        }
                        return { inferredType: 'radio_quiz', confidence: 'medium' };
                    }
                }
            }
        }

        // Check for Question header with 3+ columns
        if (numCols >= 3 && rows.length > 0 && rows[0].cells) {
            var headerText = this._getCellText(rows[0].cells[0]).toLowerCase();
            if (headerText.match(/question/)) {
                return { inferredType: 'multichoice_quiz', confidence: 'medium' };
            }
        }

        // Check for 2-column matching pairs (drag and drop)
        if (numCols === 2 && rows.length >= 2) {
            return { inferredType: 'drag_and_drop', confidence: 'low' };
        }

        // Single column numbered items
        if (numCols === 1 && rows.length >= 2) {
            return { inferredType: 'ordered_list', confidence: 'low' };
        }

        return { inferredType: null, confidence: 'none' };
    }

    /**
     * Normalise video tags with timing instruction extraction.
     *
     * @param {string} tagText - The raw tag/instruction text
     * @returns {Object|null} { type: "video", startTime, endTime, title, variant, note }
     */
    normaliseVideoTag(tagText) {
        if (!tagText || typeof tagText !== 'string') return null;

        var cleaned = tagText.toLowerCase().trim();
        var original = tagText.trim();

        // Check if it's a video tag
        var videoPatterns = [
            /^embed\s+video/i,
            /^imbed\s+video/i,
            /^insert\s+video/i,
            /^video$/i,
            /^embed\s+film/i,
            /^imbed\s+film/i,
            /^interactive\s*:\s*video/i
        ];

        var isVideo = false;
        for (var p = 0; p < videoPatterns.length; p++) {
            if (cleaned.match(videoPatterns[p])) {
                isVideo = true;
                break;
            }
        }

        // [insert Audio animation Video ...]
        if (!isVideo && cleaned.match(/audio\s+animation\s+video/i)) {
            isVideo = true;
        }

        if (!isVideo) return null;

        var result = { type: 'video', startTime: null, endTime: null, title: null, variant: null, note: null };

        // Extract title from [Interactive: Video: Title]
        var titleMatch = original.match(/interactive\s*:\s*video\s*:\s*(.+)/i);
        if (titleMatch) {
            result.title = titleMatch[1].trim();
        }

        // Extract variant for audio animation video
        if (cleaned.match(/audio\s+animation\s+video/i)) {
            result.variant = 'audio_animation';
            var noteMatch = original.match(/\(([^)]+)\)/);
            if (noteMatch) {
                result.note = noteMatch[1].trim();
            }
        }

        return result;
    }

    /**
     * Extract video timing instructions from text following a video tag.
     *
     * @param {string} text - Text after the video tag
     * @returns {Object} { startTime, endTime }
     */
    extractVideoTiming(text) {
        if (!text || typeof text !== 'string') return { startTime: null, endTime: null };

        var result = { startTime: null, endTime: null };

        // Start time patterns — handle both :53 (seconds only) and 1:05 (min:sec)
        var startPatterns = [
            /(?:edit\s+to\s+)?(?:start|begin)\s+(?:at|playing\s+(?:at|from))\s+:?(\d*[:.]\d+)\s*(?:seconds?|minutes?)?/i,
            /start\s+(?:at|from)\s+:?(\d*[:.]\d+)/i,
            /start\s+playing\s+(?:at|from)\s+:?(\d*[:.]\d+)/i
        ];

        for (var s = 0; s < startPatterns.length; s++) {
            var startMatch = text.match(startPatterns[s]);
            if (startMatch) {
                result.startTime = this._normaliseTimestamp(startMatch[1]);
                break;
            }
        }

        // End time patterns
        var endPatterns = [
            /(?:edit\s+to\s+)?(?:finish|end|stop)\s+(?:at|playing\s+at)\s+:?(\d*[:.]\d+)\s*(?:seconds?|minutes?)?/i,
            /(?:finish|end)\s+playing\s+at\s+:?(\d*[:.]\d+)\s*(?:seconds?|minutes?)?/i,
            /(?:and\s+)?(?:finish|end)\s+(?:at)\s+:?(\d*[:.]\d+)/i
        ];

        for (var e = 0; e < endPatterns.length; e++) {
            var endMatch = text.match(endPatterns[e]);
            if (endMatch) {
                result.endTime = this._normaliseTimestamp(endMatch[1]);
                break;
            }
        }

        return result;
    }

    /**
     * Normalise alert/boxout tags to structured form.
     *
     * @param {string} tagText - The raw tag inner text
     * @returns {Object|null} { type: "alert", variant, colour }
     */
    normaliseAlertTag(tagText) {
        if (!tagText || typeof tagText !== 'string') return null;

        var cleaned = tagText.toLowerCase().trim();
        var flexCleaned = cleaned.replace(/-/g, ' ').replace(/\s+/g, ' ');

        // Already handled by standard normaliser for basic alert/important
        // This method handles extended variants

        if (flexCleaned === 'alert' || flexCleaned === 'alert box') {
            return { type: 'alert', variant: 'default', colour: null };
        }

        if (flexCleaned.match(/^alert\s*\.?\s*top\.?$/)) {
            return { type: 'alert', variant: 'top', colour: null };
        }

        if (flexCleaned === 'important' || flexCleaned === 'important note') {
            return { type: 'alert', variant: 'important', colour: null };
        }

        if (flexCleaned.match(/^alert\s*\/\s*summary\s+box$/)) {
            return { type: 'alert', variant: 'summary', colour: null };
        }

        // Box variants
        if (flexCleaned.match(/^box\s+out\s+to\s+the\s+right/)) {
            return { type: 'alert', variant: 'box_right', colour: null };
        }
        if (flexCleaned.match(/^box\s+to\s+the\s+right\s+with\s+an?\s+exemplar/)) {
            return { type: 'alert', variant: 'box_right_exemplar', colour: null };
        }
        if (flexCleaned.match(/^box\s*\d*$/)) {
            return { type: 'alert', variant: 'box', colour: null };
        }
        if (flexCleaned.match(/^right\s+hand\s+side\s+alert/)) {
            return { type: 'alert', variant: 'alert_right', colour: null };
        }

        // Coloured box
        var colouredMatch = flexCleaned.match(/(?:in\s+a?\s+)?(?:pale\s+)?(\w+)\s+coloured\s+box/);
        if (colouredMatch) {
            return { type: 'alert', variant: 'coloured_box', colour: colouredMatch[1] };
        }
        if (flexCleaned === 'coloured box') {
            return { type: 'alert', variant: 'coloured_box', colour: null };
        }

        // Thought bubble
        var thoughtMatch = flexCleaned.match(/^thought\s+bubble\s*(.*)?$/);
        if (thoughtMatch) {
            var tbColour = null;
            if (thoughtMatch[1]) {
                var tbColorMatch = thoughtMatch[1].match(/^(\w+)/);
                if (tbColorMatch) tbColour = tbColorMatch[1];
            }
            return { type: 'alert', variant: 'thought_bubble', colour: tbColour || null };
        }

        // Supervisor note
        if (flexCleaned.match(/^supervisor'?s?\s+note/)) {
            return { type: 'alert', variant: 'supervisor_note', colour: null };
        }

        // Wānanga/Talanoa box
        if (flexCleaned.match(/wananga|talanoa/)) {
            return { type: 'alert', variant: 'cultural', colour: null };
        }

        // Definition
        if (flexCleaned.match(/^definition/)) {
            return { type: 'alert', variant: 'definition', colour: null };
        }

        // Equation
        if (flexCleaned === 'equation') {
            return { type: 'alert', variant: 'equation', colour: null };
        }

        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Building patterns and maps
    // ------------------------------------------------------------------

    // ------------------------------------------------------------------
    // Internal: Tag extraction helpers
    // ------------------------------------------------------------------

    /**
     * Get all normalised tags from a content block.
     *
     * @param {Object} block - A content block from the parser
     * @returns {Array<Object>} Array of tag objects with normalised info
     */
    _getBlockTags(block) {
        if (!block) return [];

        var text = '';
        if (block.type === 'paragraph' && block.data) {
            text = block.data.text || '';
        } else if (block.type === 'table') {
            // Check table cells for tags
            return this._getTableTags(block);
        }

        if (!text) return [];

        var processed = this._normaliser.processBlock(text);
        return processed.tags || [];
    }

    /**
     * Get tags from table cells.
     */
    _getTableTags(block) {
        if (!block.data || !block.data.rows) return [];

        var tags = [];
        var rows = block.data.rows;
        for (var r = 0; r < rows.length && r < 3; r++) { // check first 3 rows
            if (rows[r].cells) {
                for (var c = 0; c < rows[r].cells.length; c++) {
                    var cell = rows[r].cells[c];
                    if (cell.paragraphs) {
                        for (var p = 0; p < cell.paragraphs.length; p++) {
                            var cellText = cell.paragraphs[p].text || '';
                            var processed = this._normaliser.processBlock(cellText);
                            if (processed.tags) {
                                tags = tags.concat(processed.tags);
                            }
                        }
                    }
                }
            }
        }
        return tags;
    }


    // ------------------------------------------------------------------
    // Internal: Sub-element matching
    // ------------------------------------------------------------------

    /**
     * Match a sub-element tag within an open block.
     */
    _matchSubElement(tags, parentBlock, block) {
        if (!tags || tags.length === 0) return null;

        for (var i = 0; i < tags.length; i++) {
            var tag = tags[i];
            var raw = tag.raw || '';
            var inner = raw.replace(/^\[|\]$/g, '').trim();

            var subTag = this.normaliseSubTag(inner, parentBlock.blockType,
                this._getLastChildIndex(parentBlock));

            if (subTag && !subTag.isMarkerOnly) {
                return {
                    subType: subTag.subType,
                    index: subTag.index,
                    heading: subTag.heading || null,
                    headingLevel: subTag.headingLevel || null,
                    content: [{ blockIndex: block, raw: raw }]
                };
            }
        }

        return null;
    }

    /**
     * Get the last child index from a block's children.
     */
    _getLastChildIndex(block) {
        if (!block.children || block.children.length === 0) return 0;
        var lastChild = block.children[block.children.length - 1];
        return lastChild.index || 0;
    }


    // ------------------------------------------------------------------
    // Internal: Block closing helper
    // ------------------------------------------------------------------

    /**
     * Close a block and produce the final scope object.
     */
    _closeBlock(block, lineEnd, closingBlock, implicit, reason) {
        block.lineEnd = lineEnd;
        block.implicitClose = implicit;
        block.implicitCloseReason = reason || null;
        if (closingBlock && !implicit) {
            block.closingTag = closingBlock.data ? closingBlock.data.text : (closingBlock.raw || null);
        }
        // Clean up internal items
        delete block._contentItems;
        return block;
    }

    // ------------------------------------------------------------------
    // Internal: Table helpers for interactive inference
    // ------------------------------------------------------------------

    _getCellText(cell) {
        if (!cell) return '';
        if (cell.paragraphs) {
            return cell.paragraphs.map(function(p) { return p.text || ''; }).join(' ');
        }
        if (typeof cell === 'string') return cell;
        return '';
    }

    _cellHasBold(cell) {
        if (!cell || !cell.paragraphs) return false;
        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            if (para.runs) {
                for (var r = 0; r < para.runs.length; r++) {
                    if (para.runs[r].formatting && para.runs[r].formatting.bold) return true;
                }
            }
        }
        return false;
    }

    // ------------------------------------------------------------------
    // Internal: Timestamp normalisation
    // ------------------------------------------------------------------

    _normaliseTimestamp(raw) {
        if (!raw) return null;
        // Handle both : and . separators
        var parts = raw.split(/[:.]/);
        if (parts.length === 2) {
            var min = parseInt(parts[0], 10) || 0;
            var sec = parseInt(parts[1], 10) || 0;
            return min + ':' + (sec < 10 ? '0' + sec : sec);
        }
        // Single number — treat as seconds
        if (parts.length === 1) {
            var secs = parseInt(parts[0], 10) || 0;
            return '0:' + (secs < 10 ? '0' + secs : secs);
        }
        return raw;
    }
}
