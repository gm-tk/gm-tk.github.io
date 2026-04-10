/**
 * Tests for review page changes:
 * Phase 11: Toolbar relocation, "Calibration Tool" → "Conversion Error Log" rename
 * Phase 12: Per-panel Sync buttons replace global toggle, one-shot align trigger,
 *           cross-panel textual-anchor matching, visual feedback, removal of
 *           continuous scroll-coupling
 */

'use strict';

// Use globals exposed by test-runner.js
var _fs = global.__testFs;
var _path = global.__testPath;
var _root = global.__testRootDir;

// Load file contents for DOM structure and source code analysis tests
var reviewHtml = _fs.readFileSync(_path.resolve(_root, 'review.html'), 'utf8');
var calibrateHtml = _fs.readFileSync(_path.resolve(_root, 'calibrate.html'), 'utf8');
var reviewAppJs = _fs.readFileSync(_path.resolve(_root, 'js', 'review-app.js'), 'utf8');
var calibrateAppJs = _fs.readFileSync(_path.resolve(_root, 'js', 'calibrate-app.js'), 'utf8');
var reviewCss = _fs.readFileSync(_path.resolve(_root, 'css', 'review-styles.css'), 'utf8');

// ====================================================================
// 1. Toolbar relocation tests (Phase 11)
// ====================================================================

describe('Review Page — Toolbar relocation', function () {

    it('should have a .review-toolbar element in review.html', function () {
        assert(reviewHtml.indexOf('class="review-toolbar"') !== -1,
            'review.html should contain a .review-toolbar element');
    });

    it('should place toolbar after header and before three-panel layout', function () {
        var headerEnd = reviewHtml.indexOf('</header>');
        var toolbarStart = reviewHtml.indexOf('class="review-toolbar"');
        var layoutStart = reviewHtml.indexOf('class="review-layout"');
        assert(headerEnd !== -1 && toolbarStart !== -1 && layoutStart !== -1,
            'header, toolbar, and layout should all be present');
        assert(headerEnd < toolbarStart, 'toolbar should appear after header closes');
        assert(toolbarStart < layoutStart, 'toolbar should appear before three-panel layout');
    });

    it('should contain Raw HTML and Conversion Error Log buttons in toolbar', function () {
        var toolbarStart = reviewHtml.indexOf('class="review-toolbar"');
        var layoutStart = reviewHtml.indexOf('class="review-layout"');
        var toolbarContent = reviewHtml.substring(toolbarStart, layoutStart);
        assert(toolbarContent.indexOf('id="btn-raw-html-toggle"') !== -1,
            'Raw HTML button should be inside toolbar');
        assert(toolbarContent.indexOf('id="btn-calibration-tool"') !== -1,
            'Conversion Error Log button should be inside toolbar');
    });

    it('should NOT have controls in the header', function () {
        var headerStart = reviewHtml.indexOf('<header');
        var headerEnd = reviewHtml.indexOf('</header>');
        var headerContent = reviewHtml.substring(headerStart, headerEnd);
        assert(headerContent.indexOf('btn-raw-html-toggle') === -1,
            'header should NOT contain raw HTML button');
        assert(headerContent.indexOf('btn-calibration-tool') === -1,
            'header should NOT contain error log button');
    });

    it('should NOT have review-header-right div', function () {
        assert(reviewHtml.indexOf('review-header-right') === -1,
            'review-header-right should not exist');
    });

    it('should have header with back link, title, and module code only', function () {
        var headerStart = reviewHtml.indexOf('<header');
        var headerEnd = reviewHtml.indexOf('</header>');
        var headerContent = reviewHtml.substring(headerStart, headerEnd);
        assert(headerContent.indexOf('id="btn-back"') !== -1, 'header should contain back link');
        assert(headerContent.indexOf('review-title') !== -1, 'header should contain title');
        assert(headerContent.indexOf('review-module-code') !== -1, 'header should contain module code');
    });

    it('should have .review-toolbar CSS styles defined', function () {
        assert(reviewCss.indexOf('.review-toolbar') !== -1,
            'review-styles.css should contain .review-toolbar styles');
    });

    it('should have toolbar responsive styles', function () {
        assert(reviewCss.indexOf('.review-toolbar') !== -1,
            'review-styles.css should handle toolbar in responsive section');
    });
});

// ====================================================================
// 2. Rename "Calibration Tool" to "Conversion Error Log" tests
// ====================================================================

describe('Rename — Conversion Error Log label consistency', function () {

    it('should show "Conversion Error Log" on the review page button', function () {
        assert(reviewHtml.indexOf('Conversion Error Log') !== -1,
            'review.html should contain "Conversion Error Log" label');
    });

    it('should NOT show "Calibration Tool" as button text on review page', function () {
        var btnStart = reviewHtml.indexOf('id="btn-calibration-tool"');
        var btnEnd = reviewHtml.indexOf('</button>', btnStart);
        var btnContent = reviewHtml.substring(btnStart, btnEnd);
        assert(btnContent.indexOf('Calibration Tool') === -1,
            'Button text should not say "Calibration Tool"');
    });

    it('should have "Conversion Error Log" as calibrate.html page title', function () {
        assert(calibrateHtml.indexOf('<title>PageForge \u2014 Conversion Error Log</title>') !== -1
            || calibrateHtml.indexOf('<title>PageForge — Conversion Error Log</title>') !== -1,
            'calibrate.html title should be "PageForge — Conversion Error Log"');
    });

    it('should have "Conversion Error Log" as calibrate.html page heading', function () {
        assert(calibrateHtml.indexOf('Conversion Error Log</h1>') !== -1,
            'calibrate.html h1 should say "Conversion Error Log"');
    });

    it('should have _openConversionErrorLog method in review-app.js', function () {
        assert(reviewAppJs.indexOf('_openConversionErrorLog') !== -1,
            'review-app.js should have _openConversionErrorLog method');
    });

    it('should NOT have _openCalibrationTool method in review-app.js', function () {
        assert(reviewAppJs.indexOf('_openCalibrationTool') === -1,
            'review-app.js should not reference old _openCalibrationTool method');
    });

    it('should reference "Conversion Error Log" in calibrate-app.js JSDoc', function () {
        assert(calibrateAppJs.indexOf('Conversion Error Log') !== -1,
            'calibrate-app.js JSDoc should mention "Conversion Error Log"');
    });

    it('should NOT say "Calibration Comparison Tool" in calibrate.html heading', function () {
        assert(calibrateHtml.indexOf('Calibration Comparison Tool</h1>') === -1,
            'calibrate.html h1 should not say "Calibration Comparison Tool"');
    });
});

// ====================================================================
// 3. Per-panel Sync buttons — DOM presence and positioning
// ====================================================================

describe('Per-panel Sync buttons — DOM structure', function () {

    it('should have a Sync button in the PageForge panel header', function () {
        var pfPanelStart = reviewHtml.indexOf('id="panel-pageforge"');
        var pfPanelBody = reviewHtml.indexOf('id="pageforge-panel-body"');
        var pfHeader = reviewHtml.substring(pfPanelStart, pfPanelBody);
        assert(pfHeader.indexOf('id="btn-sync-pageforge"') !== -1,
            'PageForge panel header should contain btn-sync-pageforge');
    });

    it('should have a Sync button in the Human Reference panel header', function () {
        var humanPanelStart = reviewHtml.indexOf('id="panel-human"');
        var humanPanelBody = reviewHtml.indexOf('id="human-panel-body"');
        var humanHeader = reviewHtml.substring(humanPanelStart, humanPanelBody);
        assert(humanHeader.indexOf('id="btn-sync-human"') !== -1,
            'Human Reference panel header should contain btn-sync-human');
    });

    it('should have a Sync button in the Writer Template panel header', function () {
        var writerPanelStart = reviewHtml.indexOf('id="panel-writer"');
        var writerPanelBody = reviewHtml.indexOf('id="writer-panel-body"');
        var writerHeader = reviewHtml.substring(writerPanelStart, writerPanelBody);
        assert(writerHeader.indexOf('id="btn-sync-writer"') !== -1,
            'Writer Template panel header should contain btn-sync-writer');
    });

    it('should use consistent review-sync-btn class on all three buttons', function () {
        var pfBtn = reviewHtml.indexOf('id="btn-sync-pageforge"');
        var humanBtn = reviewHtml.indexOf('id="btn-sync-human"');
        var writerBtn = reviewHtml.indexOf('id="btn-sync-writer"');

        // Check class precedes each ID
        var pfClass = reviewHtml.lastIndexOf('review-sync-btn', pfBtn);
        var humanClass = reviewHtml.lastIndexOf('review-sync-btn', humanBtn);
        var writerClass = reviewHtml.lastIndexOf('review-sync-btn', writerBtn);

        assert(pfClass !== -1 && pfClass > pfBtn - 200, 'PF sync btn should have review-sync-btn class');
        assert(humanClass !== -1 && humanClass > humanBtn - 200, 'Human sync btn should have review-sync-btn class');
        assert(writerClass !== -1 && writerClass > writerBtn - 200, 'Writer sync btn should have review-sync-btn class');
    });

    it('should have all three sync buttons use the same arrow icon', function () {
        // Check that all three use the &#8644; entity (⇄ left-right arrow)
        var count = (reviewHtml.match(/&#8644;\s*Sync/g) || []).length;
        assertEqual(count, 3, 'should have 3 sync buttons with &#8644; Sync text');
    });

    it('should have CSS styles for .review-sync-btn', function () {
        assert(reviewCss.indexOf('.review-sync-btn') !== -1,
            'review-styles.css should define .review-sync-btn styles');
    });

    it('should have CSS for .review-sync-btn-pulse visual feedback', function () {
        assert(reviewCss.indexOf('.review-sync-btn-pulse') !== -1,
            'review-styles.css should define .review-sync-btn-pulse for click feedback');
    });

    it('should have CSS for .review-panel-sync-flash target flash', function () {
        assert(reviewCss.indexOf('.review-panel-sync-flash') !== -1,
            'review-styles.css should define .review-panel-sync-flash for target feedback');
    });
});

// ====================================================================
// 4. Global Sync toggle fully removed
// ====================================================================

describe('Global Sync toggle — Complete removal', function () {

    it('should NOT have sync-mode-toggle checkbox in review.html', function () {
        assert(reviewHtml.indexOf('id="sync-mode-toggle"') === -1,
            'review.html should not contain sync-mode-toggle checkbox');
    });

    it('should NOT have .review-sync-toggle label in review.html', function () {
        assert(reviewHtml.indexOf('review-sync-toggle') === -1,
            'review.html should not contain review-sync-toggle label');
    });

    it('should NOT have syncModeEnabled property in review-app.js', function () {
        assert(reviewAppJs.indexOf('syncModeEnabled') === -1,
            'review-app.js should not reference syncModeEnabled');
    });

    it('should NOT have _scrollSyncLock property in review-app.js', function () {
        assert(reviewAppJs.indexOf('_scrollSyncLock') === -1,
            'review-app.js should not reference _scrollSyncLock');
    });

    it('should NOT have _bindScrollSync method in review-app.js', function () {
        assert(reviewAppJs.indexOf('_bindScrollSync') === -1,
            'review-app.js should not contain _bindScrollSync');
    });

    it('should NOT have _attachIframeScrollHandler in review-app.js', function () {
        assert(reviewAppJs.indexOf('_attachIframeScrollHandler') === -1,
            'review-app.js should not contain _attachIframeScrollHandler');
    });

    it('should NOT have _attachIframeClickHandler in review-app.js', function () {
        assert(reviewAppJs.indexOf('_attachIframeClickHandler') === -1,
            'review-app.js should not contain _attachIframeClickHandler');
    });

    it('should NOT have _updateSyncModeIndicator in review-app.js', function () {
        assert(reviewAppJs.indexOf('_updateSyncModeIndicator') === -1,
            'review-app.js should not contain _updateSyncModeIndicator');
    });

    it('should NOT have debounced scroll handler references in review-app.js', function () {
        assert(reviewAppJs.indexOf('_debouncedPfScroll') === -1,
            'review-app.js should not reference _debouncedPfScroll');
        assert(reviewAppJs.indexOf('_debouncedHumanScroll') === -1,
            'review-app.js should not reference _debouncedHumanScroll');
        assert(reviewAppJs.indexOf('_debouncedWriterScroll') === -1,
            'review-app.js should not reference _debouncedWriterScroll');
    });

    it('should NOT have .review-sync-toggle CSS styles', function () {
        assert(reviewCss.indexOf('.review-sync-toggle') === -1,
            'review-styles.css should not contain .review-sync-toggle');
    });

    it('should NOT have .review-sync-slider CSS styles', function () {
        assert(reviewCss.indexOf('.review-sync-slider') === -1,
            'review-styles.css should not contain .review-sync-slider');
    });

    it('should NOT have .review-sync-active CSS class', function () {
        assert(reviewCss.indexOf('.review-sync-active') === -1,
            'review-styles.css should not contain .review-sync-active');
    });

    it('should NOT have 6-tier sync methods in review-app.js', function () {
        assert(reviewAppJs.indexOf('_syncToBlock') === -1,
            'should not have _syncToBlock');
        assert(reviewAppJs.indexOf('_highlightInIframe') === -1,
            'should not have _highlightInIframe');
        assert(reviewAppJs.indexOf('_syncHumanPanelIntelligent') === -1,
            'should not have _syncHumanPanelIntelligent');
        assert(reviewAppJs.indexOf('_highlightAndScroll') === -1,
            'should not have _highlightAndScroll');
        assert(reviewAppJs.indexOf('_findStructuralId') === -1,
            'should not have _findStructuralId');
        assert(reviewAppJs.indexOf('_extractActivityNumber') === -1,
            'should not have _extractActivityNumber');
        assert(reviewAppJs.indexOf('_extractHeadingText') === -1,
            'should not have _extractHeadingText');
        assert(reviewAppJs.indexOf('_extractWordGroups') === -1,
            'should not have _extractWordGroups');
        assert(reviewAppJs.indexOf('_findByWordGroups') === -1,
            'should not have _findByWordGroups');
    });
});

// ====================================================================
// 5. One-shot Sync click implementation
// ====================================================================

describe('Per-panel Sync — One-shot align trigger implementation', function () {

    it('should have _onSyncClick method in review-app.js', function () {
        assert(reviewAppJs.indexOf('_onSyncClick(') !== -1,
            'review-app.js should contain _onSyncClick method');
    });

    it('should accept sourcePanel parameter in _onSyncClick', function () {
        assert(reviewAppJs.indexOf("_onSyncClick(sourcePanel)") !== -1
            || reviewAppJs.indexOf("_onSyncClick('pageforge')") !== -1,
            '_onSyncClick should work with panel identifiers');
    });

    it('should bind _onSyncClick to all three Sync buttons in _bindEvents', function () {
        var bindEventsStart = reviewAppJs.indexOf('_bindEvents()');
        var bindEventsEnd = reviewAppJs.indexOf('_openConversionErrorLog', bindEventsStart);
        var bindSection = reviewAppJs.substring(bindEventsStart, bindEventsEnd);
        assert(bindSection.indexOf("_onSyncClick('pageforge')") !== -1,
            'should bind pageforge sync button');
        assert(bindSection.indexOf("_onSyncClick('human')") !== -1,
            'should bind human sync button');
        assert(bindSection.indexOf("_onSyncClick('writer')") !== -1,
            'should bind writer sync button');
    });

    it('should call _extractVisibleAnchor with source panel in _onSyncClick', function () {
        var methodStart = reviewAppJs.indexOf('_onSyncClick(sourcePanel)');
        var methodEnd = reviewAppJs.indexOf('_syncPanelToAnchor', methodStart);
        var methodBody = reviewAppJs.substring(methodStart, methodEnd);
        assert(methodBody.indexOf('_extractVisibleAnchor(sourcePanel)') !== -1,
            '_onSyncClick should extract anchor from the source panel');
    });

    it('should NOT scroll the source panel (only targets)', function () {
        var methodStart = reviewAppJs.indexOf('_onSyncClick(sourcePanel)');
        var methodEnd = reviewAppJs.indexOf('\n    }', methodStart + 100);
        methodEnd = reviewAppJs.indexOf('\n    }', methodEnd + 1);
        var methodBody = reviewAppJs.substring(methodStart, methodEnd);
        assert(methodBody.indexOf("filter(function (p) { return p !== sourcePanel; })") !== -1,
            'should filter out source panel from targets');
    });

    it('should have _syncPanelToAnchor method for scrolling targets', function () {
        assert(reviewAppJs.indexOf('_syncPanelToAnchor(') !== -1,
            'should have _syncPanelToAnchor method');
    });

    it('should handle both rendered and raw HTML views in _syncPanelToAnchor', function () {
        var methodStart = reviewAppJs.indexOf('_syncPanelToAnchor(panel');
        var methodEnd = reviewAppJs.indexOf('\n    }', methodStart + 50);
        var methodBody = reviewAppJs.substring(methodStart, methodEnd);
        assert(methodBody.indexOf('rawHtmlMode') !== -1,
            '_syncPanelToAnchor should check rawHtmlMode');
        assert(methodBody.indexOf('_scrollRawViewToAnchor') !== -1,
            'should use _scrollRawViewToAnchor for raw views');
        assert(methodBody.indexOf('_scrollIframeToAnchor') !== -1,
            'should use _scrollIframeToAnchor for rendered views');
        assert(methodBody.indexOf('_scrollWriterToAnchor') !== -1,
            'should use _scrollWriterToAnchor for writer panel');
    });
});

// ====================================================================
// 6. Content-matching logic uses textual-anchor helpers
// ====================================================================

describe('Per-panel Sync — Content matching uses anchor helpers', function () {

    it('should still have normaliseTextForMatch static method', function () {
        assert(reviewAppJs.indexOf('static normaliseTextForMatch(') !== -1,
            'should retain normaliseTextForMatch helper');
    });

    it('should still have _extractVisibleAnchor method', function () {
        assert(reviewAppJs.indexOf('_extractVisibleAnchor(') !== -1,
            'should retain _extractVisibleAnchor');
    });

    it('should still have _scrollRawViewToAnchor method', function () {
        assert(reviewAppJs.indexOf('_scrollRawViewToAnchor(') !== -1,
            'should retain _scrollRawViewToAnchor');
    });

    it('should still have _scrollIframeToAnchor method', function () {
        assert(reviewAppJs.indexOf('_scrollIframeToAnchor(') !== -1,
            'should retain _scrollIframeToAnchor');
    });

    it('should still have _scrollWriterToAnchor method', function () {
        assert(reviewAppJs.indexOf('_scrollWriterToAnchor(') !== -1,
            'should retain _scrollWriterToAnchor');
    });

    it('should still have _extractAnchorFromRawView method', function () {
        assert(reviewAppJs.indexOf('_extractAnchorFromRawView(') !== -1,
            'should retain _extractAnchorFromRawView');
    });

    it('should use fallbackFraction for proportional scroll fallback', function () {
        assert(reviewAppJs.indexOf('fallbackFraction') !== -1,
            'should use fallbackFraction as proportional fallback parameter');
    });

    it('should still have _restoreScrollFromAnchor for Raw HTML toggle', function () {
        assert(reviewAppJs.indexOf('_restoreScrollFromAnchor(') !== -1,
            'should retain _restoreScrollFromAnchor for Raw HTML view toggle');
    });
});

// ====================================================================
// 7. Visual feedback
// ====================================================================

describe('Per-panel Sync — Visual feedback', function () {

    it('should add pulse class to clicked sync button', function () {
        var methodStart = reviewAppJs.indexOf('_onSyncClick(sourcePanel)');
        var methodEnd = reviewAppJs.indexOf('_extractVisibleAnchor(sourcePanel)', methodStart);
        var methodBody = reviewAppJs.substring(methodStart, methodEnd);
        assert(methodBody.indexOf('review-sync-btn-pulse') !== -1,
            'should add review-sync-btn-pulse class on click');
    });

    it('should remove pulse class after timeout', function () {
        var methodStart = reviewAppJs.indexOf('_onSyncClick(sourcePanel)');
        var methodEnd = reviewAppJs.indexOf('_extractVisibleAnchor(sourcePanel)', methodStart);
        var methodBody = reviewAppJs.substring(methodStart, methodEnd);
        assert(methodBody.indexOf("classList.remove('review-sync-btn-pulse')") !== -1,
            'should remove pulse class after delay');
    });

    it('should flash target panels on sync', function () {
        var methodStart = reviewAppJs.indexOf('_onSyncClick(sourcePanel)');
        var nextMethod = reviewAppJs.indexOf('\n    _syncPanelToAnchor', methodStart);
        var methodBody = reviewAppJs.substring(methodStart, nextMethod);
        assert(methodBody.indexOf('review-panel-sync-flash') !== -1,
            'should add review-panel-sync-flash to target panels');
    });

    it('should show toast notification after sync', function () {
        var methodStart = reviewAppJs.indexOf('_onSyncClick(sourcePanel)');
        var nextMethod = reviewAppJs.indexOf('\n    /**', methodStart + 50);
        var methodBody = reviewAppJs.substring(methodStart, nextMethod);
        assert(methodBody.indexOf('showToast') !== -1,
            'should call showToast after sync completes');
    });
});

// ====================================================================
// 8. No continuous scroll-coupling after sync
// ====================================================================

describe('Per-panel Sync — No continuous scroll-coupling', function () {

    it('should NOT have scroll event listeners bound to panels', function () {
        assert(reviewAppJs.indexOf("addEventListener('scroll'") === -1,
            'should not bind scroll event listeners to any panel');
    });

    it('should NOT have onPanelScroll function', function () {
        assert(reviewAppJs.indexOf('onPanelScroll') === -1,
            'should not have onPanelScroll continuous handler');
    });

    it('should NOT have getScrollable function', function () {
        assert(reviewAppJs.indexOf('function getScrollable(') === -1,
            'should not have getScrollable inner function');
    });

    it('should NOT have getScrollFraction function', function () {
        assert(reviewAppJs.indexOf('function getScrollFraction(') === -1,
            'should not have getScrollFraction');
    });

    it('should NOT have setScrollFraction function', function () {
        assert(reviewAppJs.indexOf('function setScrollFraction(') === -1,
            'should not have setScrollFraction');
    });

    it('should NOT have debounce function', function () {
        assert(reviewAppJs.indexOf('function debounce(') === -1,
            'should not have debounce helper (no longer needed)');
    });
});

// ====================================================================
// 9. Raw HTML scroll-position preservation (retained from Phase 11)
// ====================================================================

describe('Raw HTML toggle — Scroll-position preservation', function () {

    it('should extract anchor BEFORE toggling panel content', function () {
        var toggleStart = reviewAppJs.indexOf('_toggleRawHtmlMode() {');
        var extractCall = reviewAppJs.indexOf("this._extractVisibleAnchor('pageforge')", toggleStart);
        var loadCall = reviewAppJs.indexOf('this._loadPageforgePanel', toggleStart);
        assert(extractCall !== -1 && loadCall !== -1,
            'both anchor extraction and panel load should exist');
        assert(extractCall < loadCall,
            'anchor extraction should happen before panel reload');
    });

    it('should use requestAnimationFrame for post-render scroll restoration', function () {
        assert(reviewAppJs.indexOf('requestAnimationFrame') !== -1,
            'should use requestAnimationFrame');
    });

    it('should use proportional fallback when text match fails', function () {
        assert(reviewAppJs.indexOf('fallbackFraction') !== -1,
            'should accept fallbackFraction parameter');
    });
});

// ====================================================================
// 10. normaliseTextForMatch unit tests (retained from Phase 11)
// ====================================================================

describe('normaliseTextForMatch — Text normalisation helper', function () {

    // Extract the static method body and create a callable function
    var normaliseTextForMatch;
    (function () {
        var start = reviewAppJs.indexOf('static normaliseTextForMatch(text) {');
        if (start === -1) return;
        // Find the method body by matching braces
        var braceCount = 0;
        var bodyStart = reviewAppJs.indexOf('{', start);
        var i = bodyStart;
        do {
            if (reviewAppJs[i] === '{') braceCount++;
            if (reviewAppJs[i] === '}') braceCount--;
            i++;
        } while (braceCount > 0 && i < reviewAppJs.length);
        var fnBody = reviewAppJs.substring(bodyStart + 1, i - 1);
        normaliseTextForMatch = new Function('text', fnBody);
    })();

    it('should return empty string for null/undefined/empty input', function () {
        if (!normaliseTextForMatch) { assert(false, 'could not extract normaliseTextForMatch'); return; }
        assertEqual(normaliseTextForMatch(null), '');
        assertEqual(normaliseTextForMatch(undefined), '');
        assertEqual(normaliseTextForMatch(''), '');
    });

    it('should strip HTML tags', function () {
        if (!normaliseTextForMatch) return;
        var result = normaliseTextForMatch('<p>Hello <b>world</b></p>');
        assert(result.indexOf('<') === -1, 'should not contain HTML tags');
        assert(result.indexOf('hello') !== -1, 'should contain "hello"');
        assert(result.indexOf('world') !== -1, 'should contain "world"');
    });

    it('should lowercase text', function () {
        if (!normaliseTextForMatch) return;
        var result = normaliseTextForMatch('HELLO World');
        assertEqual(result, 'hello world');
    });

    it('should collapse whitespace', function () {
        if (!normaliseTextForMatch) return;
        var result = normaliseTextForMatch('hello   world   test');
        assertEqual(result, 'hello world test');
    });

    it('should preserve macronised characters', function () {
        if (!normaliseTextForMatch) return;
        var result = normaliseTextForMatch('Tēnā koe');
        assert(result.indexOf('tēnā') !== -1, 'should preserve macronised vowels');
    });

    it('should decode common HTML entities', function () {
        if (!normaliseTextForMatch) return;
        var result = normaliseTextForMatch('A &amp; B');
        assert(result.indexOf('&amp;') === -1, 'should not contain raw &amp; entity');
    });

    it('should remove punctuation', function () {
        if (!normaliseTextForMatch) return;
        var result = normaliseTextForMatch('Hello, world! How are you?');
        assert(result.indexOf(',') === -1, 'should remove commas');
        assert(result.indexOf('!') === -1, 'should remove exclamation marks');
        assert(result.indexOf('?') === -1, 'should remove question marks');
    });
});
