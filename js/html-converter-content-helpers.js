/**
 * HtmlConverterContentHelpers — Inline formatting + content-collection helpers
 * (URL/image/audio/link extraction).
 *
 * Extracted from js/html-converter.js as part of the html-converter refactor.
 * See docs/29-html-converter-refactor-plan.md.
 */

'use strict';

class HtmlConverterContentHelpers {
    constructor(escContent, escAttr) {
        this._escContent = escContent;
        this._escAttr = escAttr;
    }

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
}
