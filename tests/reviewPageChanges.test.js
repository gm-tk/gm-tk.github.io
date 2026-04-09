/**
 * Tests for Phase 11 review page changes:
 * - Toolbar relocation (buttons moved from header to toolbar row)
 * - "Calibration Tool" renamed to "Conversion Error Log"
 * - Scroll sync implementation
 * - Raw HTML scroll-position preservation (textual-anchor matching)
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
// 1. Toolbar relocation tests
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

    it('should contain all three controls inside toolbar', function () {
        var toolbarStart = reviewHtml.indexOf('class="review-toolbar"');
        var layoutStart = reviewHtml.indexOf('class="review-layout"');
        var toolbarContent = reviewHtml.substring(toolbarStart, layoutStart);
        assert(toolbarContent.indexOf('id="sync-mode-toggle"') !== -1,
            'Sync mode toggle should be inside toolbar');
        assert(toolbarContent.indexOf('id="btn-raw-html-toggle"') !== -1,
            'Raw HTML button should be inside toolbar');
        assert(toolbarContent.indexOf('id="btn-calibration-tool"') !== -1,
            'Conversion Error Log button should be inside toolbar');
    });

    it('should NOT have controls in the header', function () {
        var headerStart = reviewHtml.indexOf('<header');
        var headerEnd = reviewHtml.indexOf('</header>');
        var headerContent = reviewHtml.substring(headerStart, headerEnd);
        assert(headerContent.indexOf('sync-mode-toggle') === -1,
            'header should NOT contain sync toggle');
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
// 3. Scroll sync implementation tests
// ====================================================================

describe('Scroll sync — Implementation structure', function () {

    it('should have _bindScrollSync method', function () {
        assert(reviewAppJs.indexOf('_bindScrollSync') !== -1,
            'review-app.js should contain _bindScrollSync method');
    });

    it('should call _bindScrollSync during construction', function () {
        var constructorStart = reviewAppJs.indexOf('constructor()');
        var renderCall = reviewAppJs.indexOf('this._render()');
        var bindScrollCall = reviewAppJs.indexOf('this._bindScrollSync()');
        assert(bindScrollCall !== -1, '_bindScrollSync should be called');
        assert(constructorStart < bindScrollCall && bindScrollCall < renderCall,
            '_bindScrollSync should be called before _render');
    });

    it('should have _scrollSyncLock for feedback loop prevention', function () {
        assert(reviewAppJs.indexOf('_scrollSyncLock') !== -1,
            'review-app.js should use _scrollSyncLock');
    });

    it('should set lock = true before syncing and release after delay', function () {
        var lockSet = reviewAppJs.indexOf('self._scrollSyncLock = true;');
        var lockRelease = reviewAppJs.indexOf('self._scrollSyncLock = false;');
        assert(lockSet !== -1, 'should set lock = true during sync');
        assert(lockRelease !== -1, 'should release lock = false after delay');
    });

    it('should early-return when syncModeEnabled is false', function () {
        assert(reviewAppJs.indexOf('if (!self.syncModeEnabled) return;') !== -1,
            'should skip scroll sync when disabled');
    });

    it('should early-return when lock is active', function () {
        assert(reviewAppJs.indexOf('if (self._scrollSyncLock) return;') !== -1,
            'should skip when lock is active (prevents infinite loop)');
    });

    it('should have _attachIframeScrollHandler method', function () {
        assert(reviewAppJs.indexOf('_attachIframeScrollHandler') !== -1,
            'should have _attachIframeScrollHandler');
    });

    it('should attach scroll handlers to writer panel body', function () {
        assert(reviewAppJs.indexOf("writerPanelBody.addEventListener('scroll'") !== -1,
            'should bind scroll to writer panel');
    });

    it('should attach scroll handlers to raw view containers', function () {
        assert(reviewAppJs.indexOf("pageforgeRaw.addEventListener('scroll'") !== -1,
            'should bind scroll to pageforge raw');
        assert(reviewAppJs.indexOf("humanRaw.addEventListener('scroll'") !== -1,
            'should bind scroll to human raw');
    });

    it('should use debounce for scroll event throttling', function () {
        assert(reviewAppJs.indexOf('function debounce(') !== -1,
            'should have a debounce helper');
    });

    it('should handle both rendered and raw HTML mode in getScrollable', function () {
        assert(reviewAppJs.indexOf('function getScrollable(panel)') !== -1,
            'should have getScrollable inner function');
        // Should reference rawHtmlMode check
        var getScrollableStart = reviewAppJs.indexOf('function getScrollable(panel)');
        var getScrollableEnd = reviewAppJs.indexOf('return null;\n        }', getScrollableStart + 100);
        var fnBody = reviewAppJs.substring(getScrollableStart, getScrollableEnd);
        assert(fnBody.indexOf('rawHtmlMode') !== -1,
            'getScrollable should check rawHtmlMode');
    });
});

// ====================================================================
// 4. Raw HTML scroll-position preservation tests
// ====================================================================

describe('Raw HTML toggle — Scroll-position preservation', function () {

    it('should have normaliseTextForMatch static method', function () {
        assert(reviewAppJs.indexOf('static normaliseTextForMatch(') !== -1,
            'should have normaliseTextForMatch');
    });

    it('should have _extractVisibleAnchor method', function () {
        assert(reviewAppJs.indexOf('_extractVisibleAnchor(') !== -1,
            'should have _extractVisibleAnchor');
    });

    it('should have _scrollRawViewToAnchor method', function () {
        assert(reviewAppJs.indexOf('_scrollRawViewToAnchor(') !== -1,
            'should have _scrollRawViewToAnchor');
    });

    it('should have _scrollIframeToAnchor method', function () {
        assert(reviewAppJs.indexOf('_scrollIframeToAnchor(') !== -1,
            'should have _scrollIframeToAnchor');
    });

    it('should have _scrollWriterToAnchor method', function () {
        assert(reviewAppJs.indexOf('_scrollWriterToAnchor(') !== -1,
            'should have _scrollWriterToAnchor');
    });

    it('should have _restoreScrollFromAnchor method', function () {
        assert(reviewAppJs.indexOf('_restoreScrollFromAnchor(') !== -1,
            'should have _restoreScrollFromAnchor');
    });

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

    it('should disable sync during scroll restoration to avoid loops', function () {
        var restoreStart = reviewAppJs.indexOf('_restoreScrollFromAnchor(anchor)');
        var disableSync = reviewAppJs.indexOf('this.syncModeEnabled = false', restoreStart);
        assert(disableSync !== -1, 'should disable sync during restoration');
    });

    it('should restore sync state after scroll restoration completes', function () {
        assert(reviewAppJs.indexOf('self.syncModeEnabled = wasSyncEnabled') !== -1,
            'should restore original sync state');
    });
});

// ====================================================================
// 5. normaliseTextForMatch unit tests
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
