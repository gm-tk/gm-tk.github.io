/**
 * BlockTagMatcher — Opening/closing/boundary tag matching for BlockScoper.
 *
 * Extracted from js/block-scoper.js as part of the block-scoper refactor.
 * See docs/27-block-scoper-refactor-plan.md.
 */

'use strict';

class BlockTagMatcher {
    constructor(tables, detectWriterInstructionFn) {
        /** @type {BlockScoperTables} */
        this._tables = tables;

        /** @type {Function} Bound reference to BlockScoper.detectWriterInstruction */
        this._detectWriterInstructionFn = detectWriterInstructionFn;
    }

    // ------------------------------------------------------------------
    // Internal: Opening tag matching
    // ------------------------------------------------------------------

    /**
     * Determine if a block's tags indicate a block-opening tag.
     *
     * @param {Array<Object>} tags - Normalised tags from the block
     * @param {Object} block - The raw content block
     * @returns {Object|null} { blockType, rawTag, writerNotes, layoutModifiers }
     */
    _matchOpeningTag(tags, block) {
        if (!tags || tags.length === 0) return null;

        var text = '';
        if (block && block.data) {
            text = block.data.text || '';
        }

        for (var i = 0; i < tags.length; i++) {
            var tag = tags[i];
            var raw = tag.raw || '';
            var inner = raw.replace(/^\[|\]$/g, '').trim();
            var lower = inner.toLowerCase();
            var flexLower = lower.replace(/-/g, ' ').replace(/\s+/g, ' ').trim();

            // Check against normalised results first
            var blockType = this._getBlockTypeFromNormalised(tag);
            if (blockType) {
                var writerNotes = [];
                var layoutModifiers = {};

                // Extract writer notes from tag text
                var noteResult = this._extractWriterNotesFromTag(inner, blockType);
                writerNotes = noteResult.notes;
                layoutModifiers = noteResult.modifiers;

                // Check text after the tag for additional instructions
                var afterTag = text.substring(text.indexOf(']') + 1).trim();
                if (afterTag) {
                    var instrDetect = this._detectWriterInstructionFn(afterTag);
                    if (instrDetect.isWriterNote) {
                        writerNotes.push(afterTag);
                    }
                }

                return {
                    blockType: blockType,
                    rawTag: raw,
                    writerNotes: writerNotes,
                    layoutModifiers: layoutModifiers
                };
            }

            // Try fuzzy matching for unrecognised tags
            var fuzzyMatch = this._fuzzyMatchOpener(flexLower, inner);
            if (fuzzyMatch) {
                return {
                    blockType: fuzzyMatch.blockType,
                    rawTag: raw,
                    writerNotes: fuzzyMatch.writerNotes || [],
                    layoutModifiers: fuzzyMatch.layoutModifiers || {}
                };
            }
        }

        return null;
    }

    /**
     * Get block type from a normalised tag result.
     */
    _getBlockTypeFromNormalised(tag) {
        if (!tag || !tag.normalised) return null;

        var typeMap = {
            'accordion': 'accordion',
            'carousel': 'carousel',
            'rotating_banner': 'carousel',
            'flip_card': 'flipcards',
            'click_drop': 'clickdrop',
            'drag_and_drop': 'dragdrop',
            'tabs': 'tabs',
            'speech_bubble': 'speech_bubble',
            'activity': 'activity',
            'alert': 'alert',
            'important': 'alert'
        };

        return typeMap[tag.normalised] || null;
    }

    /**
     * Fuzzy match an opener tag that wasn't caught by standard normalisation.
     */
    _fuzzyMatchOpener(flexLower, originalInner) {
        // Strip common prefix words
        var stripped = flexLower;
        var prefixes = ['insert', 'interactive', 'interactive:', 'interactive tool',
                       'interactive activity', 'visual interactive', 'add'];
        for (var p = 0; p < prefixes.length; p++) {
            if (stripped.indexOf(prefixes[p]) === 0) {
                stripped = stripped.substring(prefixes[p].length).trim();
                // Remove leading hyphen/dash/colon
                stripped = stripped.replace(/^[\s\-–:]+/, '').trim();
            }
        }

        // Now check first significant word(s) against block type keywords
        for (var keyword in this._tables.blockTypeKeywords) {
            if (this._tables.blockTypeKeywords.hasOwnProperty(keyword)) {
                if (stripped.indexOf(keyword) === 0) {
                    var afterKeyword = stripped.substring(keyword.length).trim();
                    var writerNotes = [];
                    var layoutModifiers = {};

                    // Extract notes from remaining text
                    if (afterKeyword) {
                        var noteInfo = this._extractWriterNotesFromTag(
                            originalInner, this._tables.blockTypeKeywords[keyword]
                        );
                        writerNotes = noteInfo.notes;
                        layoutModifiers = noteInfo.modifiers;
                    }

                    return {
                        blockType: this._tables.blockTypeKeywords[keyword],
                        writerNotes: writerNotes,
                        layoutModifiers: layoutModifiers
                    };
                }
            }
        }

        // Special: "Make these draggable" or similar
        if (flexLower.match(/\bdraggable\b/) || flexLower.match(/\bdrag\s+and\s+drop\b/)) {
            return { blockType: 'dragdrop', writerNotes: [originalInner], layoutModifiers: {} };
        }

        return null;
    }

    /**
     * Extract writer notes and layout modifiers from a tag's text.
     */
    _extractWriterNotesFromTag(tagInner, blockType) {
        var notes = [];
        var modifiers = {};
        var lower = tagInner.toLowerCase();

        // Layout modifiers
        if (lower.indexOf('side by side') !== -1) {
            modifiers.layout = 'side_by_side';
        }
        if (lower.match(/two\s+rows\s+of\s+four/)) {
            modifiers.layout = 'two_rows_of_four';
        }
        if (lower.indexOf('with images') !== -1) {
            modifiers.images = true;
        }
        if (lower.indexOf('with captions') !== -1) {
            modifiers.captions = true;
        }
        if (lower.match(/external\s+nav/)) {
            modifiers.navigation = 'external';
        }
        if (lower.match(/show\s+text\s+on\s+image/)) {
            modifiers.textOnImage = true;
        }

        // Multiplier: x2, x4, x10
        var multMatch = lower.match(/x(\d+)/);
        if (multMatch) {
            modifiers.multiplier = parseInt(multMatch[1], 10);
        }

        // Writer notes: text after core keyword that's instructional
        // Look for CS notes, parenthetical notes, etc.
        var csMatch = tagInner.match(/CS[,\s\-–:]+(.+)/i);
        if (csMatch) {
            notes.push('CS: ' + csMatch[1].trim());
        }

        var parenMatch = tagInner.match(/\(([^)]+)\)/);
        if (parenMatch) {
            notes.push(parenMatch[1].trim());
        }

        // Long descriptive text after the block keyword, or text containing "Please"
        var afterKeyword = this._getTextAfterBlockKeyword(tagInner, blockType);
        if (afterKeyword && (afterKeyword.split(/\s+/).length > 5 ||
            afterKeyword.toLowerCase().indexOf('please') !== -1)) {
            // Only add if not already captured as CS note or parenthetical
            if (!csMatch && !parenMatch) {
                notes.push(afterKeyword);
            }
        }

        return { notes: notes, modifiers: modifiers };
    }

    /**
     * Get text after the block type keyword in a tag.
     */
    _getTextAfterBlockKeyword(tagInner, blockType) {
        var lower = tagInner.toLowerCase();
        var keywordMap = {
            'accordion': /accordion\s*/i,
            'carousel': /(?:carousel|slideshow|slide\s+show)\s*/i,
            'flipcards': /(?:flip\s*cards?|flipcards?)\s*/i,
            'clickdrop': /(?:click\s*drop|drop\s*click|clickdrop)\s*/i,
            'dragdrop': /(?:drag\s+and\s+drop)\s*/i,
            'alert': /(?:alert|box|important)\s*/i,
            'tabs': /tabs?\s*/i,
            'modal': /modal\s*/i,
            'activity': /activit(?:y|ies)\s*/i
        };

        var pattern = keywordMap[blockType];
        if (!pattern) return '';

        var match = tagInner.match(pattern);
        if (!match) return '';

        var afterIdx = match.index + match[0].length;
        return tagInner.substring(afterIdx).trim();
    }

    // ------------------------------------------------------------------
    // Internal: Closing tag matching
    // ------------------------------------------------------------------

    /**
     * Check if any of the block's tags are closing tags for an open block.
     *
     * @param {Array<Object>} tags - Tags from the current block
     * @param {Array<Object>} blockStack - Currently open blocks
     * @returns {Object|null} { block: matchedOpenBlock, tag: closingTag }
     */
    _matchClosingTag(tags, blockStack) {
        if (!tags || tags.length === 0 || blockStack.length === 0) return null;

        for (var t = 0; t < tags.length; t++) {
            var tag = tags[t];
            var raw = tag.raw || '';
            var inner = raw.replace(/^\[|\]$/g, '').trim();
            var lower = inner.toLowerCase();

            // Check for normalised closing tags
            if (tag.normalised === 'end_activity') {
                // Find innermost activity
                for (var s = blockStack.length - 1; s >= 0; s--) {
                    if (blockStack[s].blockType === 'activity') {
                        return { block: blockStack[s], tag: raw };
                    }
                }
            }
            if (tag.normalised === 'end_accordions') {
                for (var sa = blockStack.length - 1; sa >= 0; sa--) {
                    if (blockStack[sa].blockType === 'accordion') {
                        return { block: blockStack[sa], tag: raw };
                    }
                }
            }

            // Fuzzy closer matching
            var closerType = this._fuzzyMatchCloser(lower);
            if (closerType) {
                if (closerType === '_generic') {
                    // Close innermost interactive block
                    for (var g = blockStack.length - 1; g >= 0; g--) {
                        if (blockStack[g].blockType !== 'activity') {
                            return { block: blockStack[g], tag: raw };
                        }
                    }
                    // If only activities, close innermost
                    if (blockStack.length > 0) {
                        return { block: blockStack[blockStack.length - 1], tag: raw };
                    }
                } else {
                    // Find matching block type in stack
                    for (var m = blockStack.length - 1; m >= 0; m--) {
                        if (blockStack[m].blockType === closerType) {
                            return { block: blockStack[m], tag: raw };
                        }
                    }
                    // If no exact match, try closing innermost (fuzzy)
                    if (blockStack.length > 0) {
                        return { block: blockStack[blockStack.length - 1], tag: raw };
                    }
                }
            }
        }

        return null;
    }

    /**
     * Fuzzy match a closing tag and return the block type it closes.
     *
     * @param {string} lowerText - Lowercased tag inner text
     * @returns {string|null} Block type or '_generic' or null
     */
    _fuzzyMatchCloser(lowerText) {
        var cleaned = lowerText.trim();

        // Strip common closer prefixes
        var stripped = cleaned;
        var closerPrefixes = [
            'end of ', 'end ', 'close ', 'finish '
        ];
        for (var p = 0; p < closerPrefixes.length; p++) {
            if (stripped.indexOf(closerPrefixes[p]) === 0) {
                stripped = stripped.substring(closerPrefixes[p].length).trim();
                break; // only strip one prefix
            }
        }

        // Strip closer suffixes
        var closerSuffixes = [
            ' ends here', ' ends', ' end here', ' end'
        ];
        for (var s = 0; s < closerSuffixes.length; s++) {
            if (stripped.length > closerSuffixes[s].length &&
                stripped.indexOf(closerSuffixes[s], stripped.length - closerSuffixes[s].length) !== -1) {
                stripped = stripped.substring(0, stripped.length - closerSuffixes[s].length).trim();
                break;
            }
        }

        // Check if the prefix-stripped text was identical to original (no prefix/suffix found)
        // AND the original doesn't contain 'end' — then it's not a closer
        if (stripped === cleaned && cleaned.indexOf('end') === -1 &&
            cleaned.indexOf('close') === -1 && cleaned.indexOf('finish') === -1) {
            return null;
        }

        // Handle generic closers
        if (stripped === '' || stripped === 'end' || stripped === 'ends') {
            return '_generic';
        }

        // Strip trailing numbers
        stripped = stripped.replace(/\s*\d+\s*$/, '').trim();

        // Look up in closer type map
        if (this._tables.closerTypeMap.hasOwnProperty(stripped)) {
            return this._tables.closerTypeMap[stripped];
        }

        // Fuzzy match: try removing spaces/hyphens and matching
        var compacted = stripped.replace(/[\s-]+/g, '');
        var compactedMap = {
            'accordion': 'accordion',
            'accordions': 'accordion',
            'carousel': 'carousel',
            'slideshow': 'carousel',
            'rotatingbanner': 'carousel',
            'flipcards': 'flipcards',
            'flipcard': 'flipcards',
            'clickdrop': 'clickdrop',
            'clickdrops': 'clickdrop',
            'draganddrop': 'dragdrop',
            'alert': 'alert',
            'alertbox': 'alert',
            'importantbox': 'alert',
            'colouredbox': 'alert',
            'tab': 'tabs',
            'tabs': 'tabs',
            'modal': 'modal',
            'modals': 'modal',
            'activity': 'activity',
            'interactive': '_generic',
            'interactiveactivity': '_generic',
            'interactivetool': '_generic',
            'quiz': '_generic',
            'quizzes': '_generic'
        };

        if (compactedMap.hasOwnProperty(compacted)) {
            return compactedMap[compacted];
        }

        // Check if text contains known block keyword anywhere
        if (stripped.indexOf('accordion') !== -1 || stripped.indexOf('accordian') !== -1) return 'accordion';
        if (stripped.indexOf('carousel') !== -1) return 'carousel';
        if (stripped.indexOf('slideshow') !== -1 || stripped.indexOf('slide show') !== -1) return 'carousel';
        if (stripped.indexOf('rotating banner') !== -1 || stripped.indexOf('rotatingbanner') !== -1) return 'carousel';
        if (stripped.indexOf('flip') !== -1) return 'flipcards';
        if (stripped.indexOf('clickdrop') !== -1 || stripped.indexOf('click drop') !== -1) return 'clickdrop';
        if (stripped.indexOf('drag') !== -1 && stripped.indexOf('drop') !== -1) return 'dragdrop';
        if (stripped.indexOf('box') !== -1 || stripped.indexOf('alert') !== -1) return 'alert';
        if (stripped.indexOf('tab') !== -1) return 'tabs';
        if (stripped.indexOf('modal') !== -1) return 'modal';
        if (stripped.indexOf('activity') !== -1) return 'activity';
        if (stripped.indexOf('interactive') !== -1) return '_generic';
        if (stripped.indexOf('quiz') !== -1) return '_generic';

        return null;
    }

    // ------------------------------------------------------------------
    // Internal: Boundary detection
    // ------------------------------------------------------------------

    /**
     * Determine if a block's tags indicate a hard structural boundary.
     *
     * @param {Array<Object>} tags - Tags from the block
     * @returns {string|false} Boundary reason string or false
     */
    _isHardBoundary(tags) {
        if (!tags || tags.length === 0) return false;

        for (var i = 0; i < tags.length; i++) {
            var tag = tags[i];
            if (!tag.normalised) {
                // Check raw text for unrecognised boundary patterns
                var raw = (tag.raw || '').replace(/^\[|\]$/g, '').toLowerCase().trim();
                if (raw.match(/^end\s*(of\s+)?page$/i) || raw.match(/^new\s+page$/i) ||
                    raw.match(/^insert\s+page\s+break$/i)) {
                    return 'page_break';
                }
                if (raw.match(/^end\s*(of\s+)?lesson/i)) return 'end_lesson';
                if (raw.match(/^end\s*(of\s+)?module/i)) return 'end_module';
                continue;
            }

            if (tag.normalised === 'end_page') return 'page_break';
            if (tag.normalised === 'lesson') return 'next_lesson';
            if (tag.normalised === 'lesson_overview') return 'lesson_overview';
        }

        return false;
    }
}
