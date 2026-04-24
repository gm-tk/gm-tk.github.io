/**
 * HtmlConverterBlockRenderer — The single giant _renderBlocks orchestrator
 * (per-block-type dispatch).
 *
 * Extracted from js/html-converter.js as part of the html-converter refactor.
 * See docs/29-html-converter-refactor-plan.md.
 */

'use strict';

class HtmlConverterBlockRenderer {
    constructor(tagNormaliser, interactiveExtractor, contentHelpers, renderers, escContent, escAttr, coreRef) {
        this.tagNormaliser = tagNormaliser;
        this._interactiveExtractor = interactiveExtractor;
        this._content = contentHelpers;
        this._renderers = renderers;
        this._escContent = escContent;
        this._escAttr = escAttr;
        this._coreRef = coreRef;
    }

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
                    var _rawHeading = self._content._stripFullHeadingFormatting(_fbText);
                    var _lessonTitleForCmp = (pageData.lessonTitle ||
                        self._coreRef._extractLessonTitle(pageData.contentBlocks || []) || '');
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
                    var rowHtml = self._renderers._wrapInRow(pendingContent.join('\n'), colClass);
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
                    htmlParts.push(self._renderers._wrapInRow(autoClsHtml, colClass));
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
                    var prevActivityHtml = this._renderers._wrapInRow(
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
                    actHeadingText = this._content._stripFullHeadingFormatting(actHeadingText);
                    var actHeadingInner = this._content._convertInlineFormatting(actHeadingText);
                    actHeadingInner = this._content._stripHeadingInlineTags(actHeadingInner);
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
                    htmlParts.push(this._renderers._wrapInRow(activityHtml, colClass));
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
                ahText = this._content._stripFullHeadingFormatting(ahText);
                var ahLevel = primaryTag.level || 3;
                if (ahLevel < 2) ahLevel = 2;
                if (ahLevel > 5) ahLevel = 5;
                var ahTag = 'h' + ahLevel;
                var ahInner = this._content._convertInlineFormatting(ahText);
                ahInner = this._content._stripHeadingInlineTags(ahInner);
                var ahHtml = '      <' + ahTag + '>' + ahInner + '</' + ahTag + '>';
                if (inActivity) {
                    activityParts.push(ahHtml);
                } else {
                    htmlParts.push(this._renderers._wrapInRow(ahHtml, colClass));
                }
                i++;
                continue;
            }

            // --- Inline info trigger → render as <span class="infoTrigger"> ---
            if (tagName === 'info_trigger' && category === 'interactive') {
                // Info triggers (not info_trigger_image) are inline elements
                // Extract the trigger word and definition from the block
                var itResult = this._coreRef._extractInfoTriggerData(pBlock);
                if (itResult) {
                    var itHtml = '      <p>' + this._content._convertInlineFormatting(itResult.beforeText) +
                        '<span class="infoTrigger" info="' + this._escAttr(itResult.definition) + '">' +
                        this._escContent(itResult.triggerWord) + '</span>' +
                        this._content._convertInlineFormatting(itResult.afterText) + '</p>';
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
                var hsHtml = self._renderers._renderHintSlider(processedBlocks, i, rawBlocks, procToRawMap, consumedRawIndices);
                if (hsHtml) {
                    if (inActivity) {
                        activityParts.push(hsHtml.html);
                    } else {
                        htmlParts.push(self._renderers._wrapInRow(hsHtml.html, colClass));
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
                var fcHtml = self._renderers._renderFlipCard(processedBlocks, i, rawBlocks, procToRawMap, consumedRawIndices);
                if (fcHtml) {
                    if (inActivity) {
                        activityParts.push(fcHtml.html);
                    } else {
                        htmlParts.push(self._renderers._wrapInRow(fcHtml.html, colClass));
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
                        self._coreRef.collectedInteractives.push(extractResult.referenceEntry);

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
                    htmlParts.push(this._renderers._wrapInRow(placeholderHtml, colClass));
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
                    var headingTexts = this._content._splitMultiHeadingText(pBlock);
                    for (var hti = 0; hti < headingTags.length; hti++) {
                        var mhLevel = headingTags[hti].level || 2;
                        var mhText = headingTexts[hti] || '';
                        if (mhLevel === 1) mhLevel = 2;
                        mhText = this._content._stripFullHeadingFormatting(mhText);
                        if (mhLevel < 2) mhLevel = 2;
                        if (mhLevel > 5) mhLevel = 5;
                        var mhTag = 'h' + mhLevel;
                        var mhInner = this._content._convertInlineFormatting(mhText);
                        mhInner = this._content._stripHeadingInlineTags(mhInner);
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
                headingText = this._content._stripFullHeadingFormatting(headingText);

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

                var headingInner = this._content._convertInlineFormatting(headingText);
                headingInner = this._content._stripHeadingInlineTags(headingInner);
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
                var htHtml = this._coreRef._renderHovertriggerParagraph(pBlock);
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
                        var listHtml = this._renderers._renderList(listItems);
                        pendingContent.push(listHtml);
                        continue;
                    }

                    var pHtml = '      <p>' + this._content._convertInlineFormatting(bodyText) + '</p>';
                    pendingContent.push(pHtml);
                }
                i++;
                continue;
            }

            // --- Alert ---
            if (tagName === 'alert') {
                // NOTE: flushPending() is deferred until a sub-branch has
                // decided whether to consume the last pendingContent entry
                // as the alert's wrapped preceding-body paragraph.

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
                    flushPending();
                    var ltInnerHtml = '';
                    var ltTagText = (pBlock.cleanText || '').trim();
                    if (ltTagText) {
                        ltInnerHtml += '          <p>' + this._content._convertInlineFormatting(ltTagText) + '</p>\n';
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
                            ltInnerHtml += this._renderers._renderList(ltListItems) + '\n';
                        } else {
                            var ltT = (ltMblk.cleanText || '').trim();
                            if (ltT) {
                                ltInnerHtml += '          <p>' + this._content._convertInlineFormatting(ltT) + '</p>\n';
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
                            ltSidebarInner = '      ' + this._renderers.renderImagePlaceholder(ltSidebarBlock._sidebarImageUrl || '', config);
                        } else {
                            ltSidebarInner = this._renderers._renderSidebarBlock(ltSidebarBlock, config);
                        }
                        var ltPairedHtml = this._renderers._wrapSideBySide(
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
                            htmlParts.push(this._renderers._wrapInRow(ltAlertHtml, colClass));
                        }
                    }
                    i += ltBlocksConsumed;
                    continue;
                }

                // Bullets+image TABLE pairing: when the [alert] marker is
                // immediately followed by a TABLE block matching the bullets+
                // image detector, consume both blocks together and render the
                // paired layout with the alert wrapper enabled. Runs after
                // the Session E layout-table pairing check (which claims
                // isLayoutTable()-qualifying tables first) and before the
                // Session F Sub-bug A preceding-body wrap. If the detector
                // returns null, or the next block is not a table, fall
                // through to the existing sub-branches unchanged.
                if (i + 1 < processedBlocks.length) {
                    var nextBlock = processedBlocks[i + 1];
                    if (nextBlock && nextBlock.type === 'table' && !this._renderers._hasTableTag(nextBlock)) {
                        var abiLayout = this._renderers._detectBulletsAndImageTable(nextBlock.data);
                        if (abiLayout) {
                            flushPending();
                            var abiHtml = this._renderers._renderBulletsAndImageTable(abiLayout, config, { alertWrap: true });
                            if (inActivity) {
                                activityParts.push(abiHtml);
                            } else {
                                htmlParts.push(abiHtml);
                            }
                            i += 2;
                            continue;
                        }
                    }
                }

                var alertResult = this._content._collectAlertContent(processedBlocks, i);

                // Preceding-body wrap: when the alert marker is standalone
                // (no content of its own AND nothing collected from following
                // untagged paragraphs) AND the immediately-preceding processed
                // block was a [body] (or an untagged paragraph), wrap that
                // preceding body content inside the alert's inner col-12.
                if (alertResult.paragraphs.length === 0 && !inActivity &&
                    pendingContent.length > 0 && i > 0) {
                    var prevBlock = processedBlocks[i - 1];
                    var prevTags = (prevBlock && prevBlock.tagResult && prevBlock.tagResult.tags) || [];
                    var prevName = prevTags.length > 0 ? prevTags[0].normalised : null;
                    var prevIsBody = prevBlock && prevBlock.type === 'paragraph' &&
                        !(prevBlock.data && prevBlock.data.isListItem) &&
                        (prevName === 'body' || (prevTags.length === 0 && (prevBlock.cleanText || '').trim()));
                    if (prevIsBody) {
                        var poppedHtml = pendingContent.pop();
                        // Re-indent the popped `      <p>...</p>` to fit the
                        // alert's `          <p>...</p>` inner-col-12 depth.
                        var poppedInner = poppedHtml.replace(/^ {6}/gm, '          ');
                        var wrappedAlertHtml = '    <div class="alert">\n' +
                            '      <div class="row">\n' +
                            '        <div class="col-12">\n' +
                            poppedInner + '\n' +
                            '        </div>\n' +
                            '      </div>\n' +
                            '    </div>';
                        flushPending();
                        htmlParts.push(this._renderers._wrapInRow(wrappedAlertHtml, colClass));
                        i += alertResult.blocksConsumed;
                        continue;
                    }
                }

                flushPending();
                var alertInnerHtml = '';
                for (var ai = 0; ai < alertResult.paragraphs.length; ai++) {
                    alertInnerHtml += '          <p>' + this._content._convertInlineFormatting(alertResult.paragraphs[ai]) + '</p>\n';
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
                    htmlParts.push(this._renderers._wrapInRow(alertHtml, colClass));
                }
                i += alertResult.blocksConsumed;
                continue;
            }

            // --- Important ---
            if (tagName === 'important') {
                flushPending();
                var impResult = this._content._collectAlertContent(processedBlocks, i);
                var impInnerHtml = '';
                for (var ii = 0; ii < impResult.paragraphs.length; ii++) {
                    impInnerHtml += '          <p>' + this._content._convertInlineFormatting(impResult.paragraphs[ii]) + '</p>\n';
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
                    htmlParts.push(this._renderers._wrapInRow(impHtml, colClass));
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
                var cultResult = this._content._collectAlertContent(processedBlocks, i);
                var cultInnerHtml = '';
                for (var ci2 = 0; ci2 < cultResult.paragraphs.length; ci2++) {
                    cultInnerHtml += '          <p>' + this._content._convertInlineFormatting(cultResult.paragraphs[ci2]) + '</p>\n';
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
                    htmlParts.push(this._renderers._wrapInRow(cultHtml, colClass));
                }
                i += cultResult.blocksConsumed;
                continue;
            }

            // --- Whakatauki ---
            if (tagName === 'whakatauki') {
                var whakContent = this._content._collectMultiLineContent(processedBlocks, i, 3);
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
                    whakHtml += '      <p>' + this._content._convertInlineFormatting(whakContent[w]) + '</p>\n';
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
                var quoteLines = this._content._collectMultiLineContent(processedBlocks, i, 2);
                var quoteText = quoteLines[0] || '';
                var quoteAck = quoteLines.length > 1 ? quoteLines[1] : '';

                // If only one line, try splitting on attribution pattern (Issue 6)
                if (!quoteAck && quoteText) {
                    var ackSplit = this._coreRef._splitQuoteAttribution(quoteText);
                    quoteText = ackSplit.quote;
                    quoteAck = ackSplit.attribution;
                }

                // Strip italic wrapping from quote text (docx artefact — CSS handles styling).
                // Handles both *text* and "*text*" and "* text"* patterns.
                quoteText = this._coreRef._stripFullItalic(quoteText);
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

                var quoteConvertedText = this._content._convertInlineFormatting(quoteText);
                var quoteHtml = '      <p class="quoteText">' + quoteConvertedText + '</p>';
                if (quoteAck) {
                    quoteHtml += '\n      <p class="quoteAck">' +
                        this._content._convertInlineFormatting(quoteAck) + '</p>';
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
                var rqContent = this._content._collectBlockContent(processedBlocks, i);
                var rqHtml = '    <div class="rhetoricalQuestion">\n' +
                    '      <p>' + this._content._convertInlineFormatting(rqContent) + '</p>\n' +
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
                var videoUrl = this._content._extractUrlFromContent(processedBlocks, i);
                var videoHtml = this._renderers.renderVideo(videoUrl, config);
                if (inActivity) {
                    activityParts.push(videoHtml);
                } else {
                    pendingContent.push(videoHtml);
                }
                i++;
                continue;
            }

            // --- Bullets + [image] table pattern ---
            // When a table pairs a bullet-list cell with an [image] cell, we
            // render it as a paired col-md-6 paddingR alert + col-md-3 paddingL
            // image row rather than letting the table fall through to the
            // generic [image] branch (which would silently drop the bullet
            // content because a table block carries no _cellText/_cleanText
            // on its own). Bullets-only and image-only tables fall through
            // to the existing single-column handlers by returning null.
            if (pBlock.type === 'table' && !this._renderers._hasTableTag(pBlock)) {
                var biLayout = this._renderers._detectBulletsAndImageTable(pBlock.data);
                if (biLayout) {
                    flushPending();
                    var biHtml = this._renderers._renderBulletsAndImageTable(biLayout, config, { alertWrap: false });
                    if (inActivity) {
                        activityParts.push(biHtml);
                    } else {
                        htmlParts.push(biHtml);
                    }
                    i++;
                    continue;
                }
            }

            // --- Image ---
            if (tagName === 'image' && pBlock.type !== 'table') {
                var imgInfo = this._content._extractImageInfo(processedBlocks, i);
                var imgHtml = this._renderers.renderImage(imgInfo, config);
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
                var audioFile = this._content._extractAudioFilename(processedBlocks, i);
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
                var btnInfo = this._content._extractLinkInfo(processedBlocks, i);
                var btnHtml = '      <a href="' + this._escAttr(btnInfo.url) +
                    '" target="_blank"><div class="button">' +
                    this._content._convertInlineFormatting(btnInfo.text) + '</div></a>';
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
                var elbInfo = this._content._extractLinkInfo(processedBlocks, i);
                var elbHtml = '      <a href="' + this._escAttr(elbInfo.url) +
                    '" target="_blank"><div class="externalButton">' +
                    this._content._convertInlineFormatting(elbInfo.text) + '</div></a>';
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
                var elInfo = this._content._extractExternalLinkInfo(processedBlocks, i);
                var elHtml;
                if (elInfo.beforeText && elInfo.beforeText.trim()) {
                    // Paragraph text before the tag + inline URL link
                    elHtml = '      <p>' + this._content._convertInlineFormatting(elInfo.beforeText) +
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
                var supContent = this._content._collectBlockContent(processedBlocks, i);
                var supHtml = '    <div class="supervisorContainer">\n' +
                    '      <div class="supervisorButton"></div>\n' +
                    '      <div class="supervisorContent">\n' +
                    '        <p>' + this._content._convertInlineFormatting(supContent) + '</p>\n' +
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
                var sidebarHtml = self._renderers._renderSidebarBlock(pBlock, config);
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
                        var sideRowHtml = self._renderers._wrapSideBySide(mainContent, sidebarHtml);
                        activityParts.push(sideRowHtml);
                    } else {
                        var sideMainContent = pendingContent.join('\n');
                        pendingContent = [];
                        var sideLayout = self._renderers._wrapSideBySide(sideMainContent, sidebarHtml);
                        htmlParts.push(sideLayout);
                    }
                }
                i++;
                continue;
            }

            // --- Table (tagged as [TABLE]) ---
            if (pBlock.type === 'table' && this._renderers._hasTableTag(pBlock)) {
                var tableHtml = this._renderers.renderTable(pBlock.data);
                if (inActivity) {
                    activityParts.push(tableHtml);
                } else {
                    pendingContent.push(tableHtml);
                }
                i++;
                continue;
            }

            // --- Layout table: body text + image side by side ---
            if (pBlock.type === 'table' && !this._renderers._hasTableTag(pBlock)) {
                var layoutInfo = this._renderers._detectLayoutTable(pBlock.data);
                if (layoutInfo) {
                    flushPending();
                    var layoutHtml = this._renderers._renderLayoutTable(layoutInfo, config);
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
            if (pBlock.type === 'table' && !this._renderers._hasTableTag(pBlock)) {
                // Grid tables have their own row structure, so flush first
                flushPending();
                var gridTableHtml = this._renderers._renderTableAsGrid(pBlock.data);
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
                    var subHtml = '      <p>' + this._content._convertInlineFormatting(pBlock.cleanText) + '</p>';
                    pendingContent.push(subHtml);
                }
                i++;
                continue;
            }

            // --- Link category (misc buttons) ---
            if (category === 'link') {
                var linkInfo = this._content._extractLinkInfo(processedBlocks, i);
                var linkHtml = '      <a href="' + this._escAttr(linkInfo.url) +
                    '" target="_blank">' + this._content._convertInlineFormatting(linkInfo.text) + '</a>';
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
                    var defListHtml = this._renderers._renderList(defListItems);
                    pendingContent.push(defListHtml);
                    continue;
                }

                var defHtml = '      <p>' + this._content._convertInlineFormatting(pBlock.cleanText) + '</p>';
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
            htmlParts.push(this._renderers._wrapInRow(finalActivityHtml, colClass));
        }

        return htmlParts.join('\n');
    }
}
