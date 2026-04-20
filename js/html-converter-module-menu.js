/**
 * HtmlConverterModuleMenu — Module-page menu (overview/info tabs) + menu helpers.
 *
 * Extracted from js/html-converter.js as part of the html-converter refactor.
 * See docs/29-html-converter-refactor-plan.md.
 */

'use strict';

class HtmlConverterModuleMenu {
    constructor(tagNormaliser, contentHelpers, renderers, escContent, escAttr, coreRef) {
        this.tagNormaliser = tagNormaliser;
        this._content = contentHelpers;
        this._renderers = renderers;
        this._escContent = escContent;
        this._escAttr = escAttr;
        this._coreRef = coreRef;
    }

    replaceModuleMenuContent(html, pageData, config, moduleInfo, menuContentBlocks) {
        if (pageData.type === 'overview') {
            // Split menu content into Overview and Information tabs
            var tabContent = this.splitMenuContentIntoTabs(menuContentBlocks || [], config);

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
            var lessonMenu = this._coreRef._generateLessonMenuContent(pageData, config, moduleInfo, menuContentBlocks);
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
    splitMenuContentIntoTabs(blocks, config) {
        var processedBlocks = this._coreRef._processAllBlocks(blocks);
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
        return this.renderModuleMenuBlocks(blocks, config, indent, true);
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
        return this.renderModuleMenuBlocks(blocks, config, indent, false, true);
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
    renderModuleMenuBlocks(blocks, config, indent, isOverviewTab, isInfoTab) {
        var processedBlocks = this._coreRef._processAllBlocks(blocks);
        var parts = [];
        var isFirstHeading = true;
        var successCriteriaHeading = (config.moduleMenu && config.moduleMenu.overviewPage &&
            config.moduleMenu.overviewPage.successCriteriaHeading)
            ? config.moduleMenu.overviewPage.successCriteriaHeading
            : 'How will I know if I\'ve learned it?';
        var stripInfoTabTereoPrefix = !!(config.moduleMenu && config.moduleMenu.overviewPage &&
            config.moduleMenu.overviewPage.stripInfoTabTereoPrefix);
        // Strip "Tereo | " prefix (info tab only) — leaves text unchanged when no ' | ' exists.
        function stripTereoPrefix(text) {
            if (!text) return text;
            var idx = text.indexOf(' | ');
            return idx !== -1 ? text.substring(idx + 3).trim() : text;
        }
        // Information tab uses h5 headings; Overview tab uses h4
        var menuHeadingTag = isInfoTab ? 'h5' : 'h4';
        var overviewCfg = (config.moduleMenu && config.moduleMenu.overviewPage) || {};
        var overviewHeadingLevel = overviewCfg.overviewTabHeadingLevel || 'h4';
        var wrapAllOverviewSpan = overviewCfg.wrapAllOverviewHeadingsInSpan === true;
        // Information tab uses h5 headings; Overview tab uses configured level
        var menuHeadingTag = isInfoTab ? 'h5' : overviewHeadingLevel;
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
                    var menuHeadingTexts = this._coreRef._splitMultiHeadingText(pBlock);
                    for (var mhti = 0; mhti < menuHeadingTags.length; mhti++) {
                        var mhMenuText = menuHeadingTexts[mhti] || '';
                        mhMenuText = this._coreRef._stripFullHeadingFormatting(mhMenuText);
                        if (isInfoTab && stripInfoTabTereoPrefix) {
                            mhMenuText = stripTereoPrefix(mhMenuText);
                        }
                        mhMenuText = this._normaliseMenuHeading(mhMenuText, successCriteriaHeading);
                        var mhMenuInner = this._coreRef._convertInlineFormatting(mhMenuText);
                        mhMenuInner = this._coreRef._stripHeadingInlineTags(mhMenuInner);
                        if (mhMenuInner.trim()) {
                            if (isOverviewTab && wrapAllOverviewSpan) {
                                parts.push(indent + '<' + menuHeadingTag + '><span>' + mhMenuInner + '</span></' + menuHeadingTag + '>');
                            } else {
                                parts.push(indent + '<' + menuHeadingTag + '>' + mhMenuInner + '</' + menuHeadingTag + '>');
                            }
                        }
                    }
                    isFirstHeading = false;
                    i++;
                    continue;
                }

                var headingText = pBlock.cleanText || '';
                headingText = this._coreRef._stripFullHeadingFormatting(headingText);
                if (isInfoTab && stripInfoTabTereoPrefix) {
                    headingText = stripTereoPrefix(headingText);
                }

                // If this is H1 in overview tab, split heading from description
                if (primaryTag.level === 1 && isOverviewTab && isFirstHeading) {
                    var h1Parts = this._splitH1HeadingAndDescription(pBlock);
                    var titleBehaviour = (config.moduleMenu && config.moduleMenu.overviewPage &&
                        config.moduleMenu.overviewPage.overviewTitleHeadingBehaviour)
                        ? config.moduleMenu.overviewPage.overviewTitleHeadingBehaviour
                        : 'keep';
                    var h1HeadingText = h1Parts.heading;
                    if (titleBehaviour === 'strip-tereo') {
                        var pipeIdx = h1HeadingText.indexOf(' | ');
                        if (pipeIdx !== -1) {
                            h1HeadingText = h1HeadingText.substring(pipeIdx + 3).trim();
                        }
                    }
                    // Heading with span (overview tab primary title), unless suppressed
                    if (titleBehaviour !== 'suppress' && h1HeadingText) {
                        parts.push(indent + '<' + menuHeadingTag + '><span>' + this._escContent(h1HeadingText) + '</span></' + menuHeadingTag + '>');
                    }
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
                var headingInner = this._coreRef._convertInlineFormatting(normalisedHeading);
                headingInner = this._coreRef._stripHeadingInlineTags(headingInner);

                if (isOverviewTab && (isFirstHeading || wrapAllOverviewSpan)) {
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
                var bodyInner = this._coreRef._convertInlineFormatting(bodyText);
                // Strip remaining italic tags from module menu content
                bodyInner = bodyInner.replace(/<\/?i>/g, '');
                parts.push(indent + '<p>' + bodyInner + '</p>');
            }

            i++;
        }

        // Change 8 — Empty heading suppression. Drop a heading if it is immediately
        // followed by another heading or by end-of-list, OR if its text is empty
        // after any earlier normalisation/stripping.
        function isHeadingPart(s) {
            return /^\s*<h[1-6][^>]*>/.test(s);
        }
        function headingHasContent(s) {
            var m = s.match(/<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/);
            if (!m) return true;
            return m[1].replace(/<\/?span[^>]*>/g, '').replace(/\s+/g, '') !== '';
        }
        var filteredParts = [];
        for (var fp = 0; fp < parts.length; fp++) {
            var cur = parts[fp];
            if (isHeadingPart(cur)) {
                if (!headingHasContent(cur)) continue;
                var nxt = parts[fp + 1];
                if (!nxt || isHeadingPart(nxt)) continue;
            }
            filteredParts.push(cur);
        }
        parts = filteredParts;

        if (parts.length === 0) {
            return indent + '<!-- No content -->';
        }

        // Wrap in row + col grid. Overview tab column class is config-driven
        // (moduleMenu.overviewPage.overviewTabColumnClass); Info tab stays fixed.
        var gridIndent = indent;
        var colClass = isOverviewTab ? (overviewCfg.overviewTabColumnClass || 'col-md-8 col-12') : 'col-md-8 col-12';
        var wrapped = gridIndent + '<div class="row">\n';
        wrapped += gridIndent + '  <div class="' + colClass + '">\n';
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
        definition = this.formatInfoTriggerDefinition(definition);

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
    formatInfoTriggerDefinition(definition) {
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
            var triggerWordFormatted = this._coreRef._convertInlineFormatting(trigger.triggerWord);
            var formattedDef = this.formatInfoTriggerDefinition(trigger.definition);
            var infoSpan = '<span class="infoTrigger" info="' +
                this._escAttr(formattedDef) + '">' +
                triggerWordFormatted + '</span>';

            result = beforePart + infoSpan + afterPart;
        }

        // Clean up: remove red text markers, tags, and format the remaining text
        result = result.replace(/\uD83D\uDD34\[RED TEXT\]\s*[\s\S]*?\s*\[\/RED TEXT\]\uD83D\uDD34/g, '');
        result = result.replace(/\[([^\]]*)\]/g, '');
        result = result.replace(/\s+/g, ' ').trim();
        result = this._coreRef._convertInlineFormatting(result);

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
                var itemInner = this._coreRef._convertInlineFormatting(text);
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
}
