/**
 * HtmlConverterLessonMenu — Lesson-page menu generation (three style variants).
 *
 * Extracted from js/html-converter.js as part of the html-converter refactor.
 * See docs/29-html-converter-refactor-plan.md.
 */

'use strict';

class HtmlConverterLessonMenu {
    constructor(tagNormaliser, contentHelpers, escContent, escAttr, coreRef) {
        this.tagNormaliser = tagNormaliser;
        this._content = contentHelpers;
        this._escContent = escContent;
        this._escAttr = escAttr;
        this._coreRef = coreRef;
    }

    generateLessonMenuContent(pageData, config, moduleInfo, menuContentBlocks) {
        var menuCfg = (config.moduleMenu && config.moduleMenu.lessonPage) || {};
        var sectionHeadings = menuCfg.sectionHeadings || {
            learning: 'Learning Intentions',
            success: "How will I know if I've learned it?"
        };
        // Legacy "labels" (e.g., "We are learning:" / "I can:") are retained in
        // templates.json as fallback text for the intro paragraph when the
        // writer did not provide one — Phase 13 behaviour prefers the writer's
        // own intro text verbatim.
        var fallbackLabels = menuCfg.labels || {
            learning: 'We are learning:',
            success: 'I can:'
        };
        var indent = '          ';

        var menuStyle = menuCfg.menuStyle || 'synthesise-headings';
        if (menuStyle === 'promote-to-h5') {
            return this._generateLessonMenuPromoteToH5(menuContentBlocks, fallbackLabels, indent);
        }
        if (menuStyle === 'lesson-overview-bold') {
            return this._generateLessonMenuOverviewBold(menuContentBlocks, fallbackLabels, indent);
        }
        // Fall through: "synthesise-headings" (baseline behaviour).

        if (!menuContentBlocks || menuContentBlocks.length === 0) {
            // No content — emit section headings with placeholder comments
            var html = '';
            html += indent + '<h5>' + this._escContent(sectionHeadings.learning) + '</h5>\n';
            html += indent + '<!-- Learning intentions content -->\n';
            html += indent + '<h5>' + this._escContent(sectionHeadings.success) + '</h5>\n';
            html += indent + '<!-- Success criteria content -->';
            return html;
        }

        // Process the menu content blocks to find description, learning, and success sections
        var processedBlocks = this._coreRef._processAllBlocks(menuContentBlocks);
        var descriptionParts = [];
        // Writer's intro paragraph text for each section (verbatim, Phase 13).
        var learningIntroText = null;
        var successIntroText = null;
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

            // Detect section boundaries by matching label-like text.
            // Phase 13 — preserve the writer's exact intro text as the <p> for
            // that section (rather than substituting a config label).
            if (cleanText) {
                var lowerText = cleanText.toLowerCase().replace(/[*_]/g, '');
                if (lowerText.indexOf('we are learning') !== -1 ||
                    lowerText.indexOf('learning intention') !== -1) {
                    currentSection = 'learning';
                    if (learningIntroText === null) learningIntroText = cleanText;
                    i++;
                    continue;
                }
                if (lowerText.indexOf('i can') !== -1 ||
                    lowerText.indexOf('success criteria') !== -1 ||
                    lowerText.indexOf('you will show') !== -1 ||
                    lowerText.indexOf('how will i know') !== -1) {
                    currentSection = 'success';
                    if (successIntroText === null) successIntroText = cleanText;
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
                    if (learningIntroText === null) learningIntroText = cleanText;
                    i++;
                    continue;
                }
                if (lowerHeading.indexOf('i can') !== -1 ||
                    lowerHeading.indexOf('success criteria') !== -1 ||
                    lowerHeading.indexOf('you will show') !== -1 ||
                    lowerHeading.indexOf('how will i know') !== -1) {
                    currentSection = 'success';
                    if (successIntroText === null) successIntroText = cleanText;
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
            descText = this._coreRef._stripFullItalic(descText);
            var descInner = this._coreRef._convertInlineFormatting(descText);
            descInner = descInner.replace(/<\/?i>/g, '');
            result.push(indent + '<p>' + descInner + '</p>');
        }

        // Phase 13 — new two-tier structure:
        //   <h5>{sectionHeading}</h5>       (from template config)
        //   <p>{writer's intro text}</p>    (verbatim, or config fallback)
        //   <ul>{list items}</ul>
        var self = this;
        function renderIntroParagraph(text, fallback) {
            var introText = (text && text.trim()) ? text.trim() : fallback;
            if (!introText) return null;
            introText = self._coreRef._stripFullItalic(introText);
            var inner = self._coreRef._convertInlineFormatting(introText);
            inner = inner.replace(/<\/?i>/g, '');
            return indent + '<p>' + inner + '</p>';
        }

        function sectionHasAnyContent(intro, items) {
            return (intro && intro.trim()) || (items && items.length > 0);
        }

        // Learning section
        if (sectionHasAnyContent(learningIntroText, learningItems)) {
            result.push(indent + '<h5>' + this._escContent(sectionHeadings.learning) + '</h5>');
            var learningIntroHtml = renderIntroParagraph(learningIntroText, fallbackLabels.learning);
            if (learningIntroHtml) result.push(learningIntroHtml);
            if (learningItems.length > 0) {
                result.push(this._coreRef._renderMenuList(learningItems, indent));
            }
        }

        // Success section
        if (sectionHasAnyContent(successIntroText, successItems)) {
            result.push(indent + '<h5>' + this._escContent(sectionHeadings.success) + '</h5>');
            var successIntroHtml = renderIntroParagraph(successIntroText, fallbackLabels.success);
            if (successIntroHtml) result.push(successIntroHtml);
            if (successItems.length > 0) {
                result.push(this._coreRef._renderMenuList(successItems, indent));
            }
        }

        return result.join('\n');
    }

    /**
     * Session D — "promote-to-h5" menu style for 1-3 / 9-10 / NCEA lesson pages.
     * Promotes the writer's "We are learning:" / "I can:" body lines directly
     * to <h5> (trailing colon kept); preserves any preceding descriptive
     * paragraph as <p>; does NOT synthesise parent section headings.
     */
    _generateLessonMenuPromoteToH5(menuContentBlocks, fallbackLabels, indent) {
        if (!menuContentBlocks || menuContentBlocks.length === 0) {
            var h = '';
            h += indent + '<h5>' + this._escContent(fallbackLabels.learning) + '</h5>\n';
            h += indent + '<!-- Learning intentions content -->\n';
            h += indent + '<h5>' + this._escContent(fallbackLabels.success) + '</h5>\n';
            h += indent + '<!-- Success criteria content -->';
            return h;
        }
        var processedBlocks = this._coreRef._processAllBlocks(menuContentBlocks);
        var result = [];
        var currentSection = 'description';
        var i = 0;
        while (i < processedBlocks.length) {
            var pBlock = processedBlocks[i];
            var tags = pBlock.tagResult ? pBlock.tagResult.tags : [];
            var primaryTag = tags.length > 0 ? tags[0] : null;
            var category = primaryTag ? primaryTag.category : null;
            if (category === 'structural') { i++; continue; }
            if (pBlock.tagResult && pBlock.tagResult.isWhitespaceOnly) { i++; continue; }
            if (pBlock.tagResult && pBlock.tagResult.isRedTextOnly && tags.length === 0 && !pBlock.cleanText) { i++; continue; }
            var cleanText = (pBlock.cleanText || '').trim();
            var lowerText = cleanText ? cleanText.toLowerCase().replace(/[*_]/g, '') : '';
            var learnLabel = (fallbackLabels.learning || '').toLowerCase().replace(/[*_:]/g, '').trim();
            var succLabel = (fallbackLabels.success || '').toLowerCase().replace(/[*_:]/g, '').trim();
            var isLearning = cleanText && (
                (learnLabel && lowerText.indexOf(learnLabel) !== -1) ||
                lowerText.indexOf('we are learning') !== -1 ||
                lowerText.indexOf('learning intention') !== -1 ||
                lowerText.indexOf('i will be able to') !== -1
            );
            var isSuccess = cleanText && !isLearning && (
                (succLabel && lowerText.indexOf(succLabel) !== -1) ||
                lowerText.indexOf('i can') !== -1 ||
                lowerText.indexOf('success criteria') !== -1 ||
                lowerText.indexOf('you will show') !== -1 ||
                lowerText.indexOf('how will i know') !== -1
            );
            if (isLearning) {
                currentSection = 'learning';
                var lh = this._coreRef._stripFullItalic(cleanText);
                result.push(indent + '<h5>' + this._escContent(lh) + '</h5>');
                i++; continue;
            }
            if (isSuccess) {
                currentSection = 'success';
                var sh = this._coreRef._stripFullItalic(cleanText);
                result.push(indent + '<h5>' + this._escContent(sh) + '</h5>');
                i++; continue;
            }
            if (pBlock.data && pBlock.data.isListItem) {
                var listItems = [];
                while (i < processedBlocks.length) {
                    var lb = processedBlocks[i];
                    if (lb.data && lb.data.isListItem) {
                        var listFmt = lb.data.listFormat || 'bullet';
                        if ((currentSection === 'success' || currentSection === 'learning') && listFmt !== 'bullet') {
                            break;
                        }
                        listItems.push(lb);
                        i++;
                    } else {
                        break;
                    }
                }
                if (listItems.length > 0) {
                    result.push(this._coreRef._renderMenuList(listItems, indent));
                }
                continue;
            }
            if (currentSection === 'description' && cleanText) {
                var descText = this._coreRef._stripFullItalic(cleanText);
                var descInner = this._coreRef._convertInlineFormatting(descText);
                descInner = descInner.replace(/<\/?i>/g, '');
                result.push(indent + '<p>' + descInner + '</p>');
            }
            i++;
        }
        return result.join('\n');
    }

    /**
     * Session D — "lesson-overview-bold" menu style for 7-8 lesson pages.
     * Emits a single <h4>Lesson Overview</h4> at the top. Writer's
     * "We are learning:" / "I can:" body lines become <p><b>…</b></p>.
     * Any intro descriptive paragraph is DROPPED. Lists remain <ul>.
     */
    _generateLessonMenuOverviewBold(menuContentBlocks, fallbackLabels, indent) {
        var result = [];
        result.push(indent + '<h4>Lesson Overview</h4>');
        if (!menuContentBlocks || menuContentBlocks.length === 0) {
            result.push(indent + '<p><b>' + this._escContent(fallbackLabels.learning) + '</b></p>');
            result.push(indent + '<!-- Learning intentions content -->');
            result.push(indent + '<p><b>' + this._escContent(fallbackLabels.success) + '</b></p>');
            result.push(indent + '<!-- Success criteria content -->');
            return result.join('\n');
        }
        var processedBlocks = this._coreRef._processAllBlocks(menuContentBlocks);
        var currentSection = 'description';
        var i = 0;
        while (i < processedBlocks.length) {
            var pBlock = processedBlocks[i];
            var tags = pBlock.tagResult ? pBlock.tagResult.tags : [];
            var primaryTag = tags.length > 0 ? tags[0] : null;
            var category = primaryTag ? primaryTag.category : null;
            if (category === 'structural') { i++; continue; }
            if (pBlock.tagResult && pBlock.tagResult.isWhitespaceOnly) { i++; continue; }
            if (pBlock.tagResult && pBlock.tagResult.isRedTextOnly && tags.length === 0 && !pBlock.cleanText) { i++; continue; }
            var cleanText = (pBlock.cleanText || '').trim();
            var lowerText = cleanText ? cleanText.toLowerCase().replace(/[*_]/g, '') : '';
            var learnLabel = (fallbackLabels.learning || '').toLowerCase().replace(/[*_:]/g, '').trim();
            var succLabel = (fallbackLabels.success || '').toLowerCase().replace(/[*_:]/g, '').trim();
            var isLearning = cleanText && (
                (learnLabel && lowerText.indexOf(learnLabel) !== -1) ||
                lowerText.indexOf('we are learning') !== -1 ||
                lowerText.indexOf('learning intention') !== -1 ||
                lowerText.indexOf('i will be able to') !== -1
            );
            var isSuccess = cleanText && !isLearning && (
                (succLabel && lowerText.indexOf(succLabel) !== -1) ||
                lowerText.indexOf('i can') !== -1 ||
                lowerText.indexOf('success criteria') !== -1 ||
                lowerText.indexOf('you will show') !== -1 ||
                lowerText.indexOf('how will i know') !== -1
            );
            if (isLearning) {
                currentSection = 'learning';
                var lh = this._coreRef._stripFullItalic(cleanText);
                result.push(indent + '<p><b>' + this._escContent(lh) + '</b></p>');
                i++; continue;
            }
            if (isSuccess) {
                currentSection = 'success';
                var sh = this._coreRef._stripFullItalic(cleanText);
                result.push(indent + '<p><b>' + this._escContent(sh) + '</b></p>');
                i++; continue;
            }
            if (pBlock.data && pBlock.data.isListItem) {
                var listItems = [];
                while (i < processedBlocks.length) {
                    var lb = processedBlocks[i];
                    if (lb.data && lb.data.isListItem) {
                        var listFmt = lb.data.listFormat || 'bullet';
                        if ((currentSection === 'success' || currentSection === 'learning') && listFmt !== 'bullet') {
                            break;
                        }
                        listItems.push(lb);
                        i++;
                    } else {
                        break;
                    }
                }
                if (listItems.length > 0) {
                    result.push(this._coreRef._renderMenuList(listItems, indent));
                }
                continue;
            }
            // Descriptive paragraph intentionally DROPPED for overview-bold style.
            i++;
        }
        return result.join('\n');
    }

}
