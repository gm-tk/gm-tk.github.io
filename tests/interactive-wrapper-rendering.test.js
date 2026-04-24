/**
 * Interactive wrapper rendering — output-template fixes A–F.
 *
 * Regression-lock tests for the green-dashed TIER 1 interactive preview
 * wrapper emitted by InteractivePlaceholderRenderer. Each `it()` case
 * corresponds to one of the six output-template fixes (A–F) plus a
 * cross-type assertion that protects against hard-coding speech_bubble
 * into any of the templates.
 */

'use strict';

var iwrNormaliser = new TagNormaliser();
var iwrExtractor = new InteractiveExtractor(iwrNormaliser);

function _iwrRun(text, isRed) {
    return {
        text: text,
        formatting: {
            bold: false, italic: false, underline: false,
            strikethrough: false,
            color: isRed ? 'FF0000' : null,
            highlight: null,
            isRed: !!isRed
        }
    };
}

function _iwrPara(parts, extra) {
    var runs = [];
    for (var i = 0; i < parts.length; i++) {
        runs.push(_iwrRun(parts[i].text, parts[i].isRed));
    }
    var text = parts.map(function (p) { return p.text; }).join('');
    var block = { type: 'paragraph', data: { text: text, runs: runs } };
    if (extra) {
        for (var k in extra) {
            if (Object.prototype.hasOwnProperty.call(extra, k)) block[k] = extra[k];
        }
    }
    return block;
}

function _iwrPlain(text, extra) {
    var block = { type: 'paragraph', data: { text: text, runs: [{ text: text }] } };
    if (extra) {
        for (var k in extra) {
            if (Object.prototype.hasOwnProperty.call(extra, k)) block[k] = extra[k];
        }
    }
    return block;
}

// Fixture replicating the OSAI201-01-WT speech-bubble layout-table row:
// Cell 1: [speech bubble] (start tag only)
// Cell 2, paragraph 1: [image] URL + red-text [image] annotation
// Cell 2, paragraph 2: fully-red CS: free-text note
function _iwrSpeechBubbleFixture() {
    return [
        _iwrPara([
            { text: '[speech bubble]', isRed: true }
        ], { _layoutRowId: 'row-1' }),
        _iwrPara([
            { text: '[image]', isRed: true },
            { text: ' https://example.com/unicorn.png' }
        ], { _layoutRowId: 'row-1' }),
        _iwrPara([
            { text: 'CS: render a cross through the image', isRed: true }
        ], { _layoutRowId: 'row-1' }),
        _iwrPlain('[body]')
    ];
}

describe('Interactive wrapper rendering — Fix A (header bar no TIER 1)', function () {

    it('(A) header bar reads "🔧 INTERACTIVE: <type>" and does NOT contain "TIER 1"', function () {
        var blocks = _iwrSpeechBubbleFixture();
        var out = iwrExtractor.processInteractive(blocks, 0, 'OSAI201-01.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('🔧 INTERACTIVE: speech_bubble') !== -1,
            'header bar contains "🔧 INTERACTIVE: speech_bubble"');
        assertTrue(html.indexOf('TIER 1') === -1,
            'header bar does NOT contain substring "TIER 1"');
    });

});

describe('Interactive wrapper rendering — Fix B (header wrapper div after <hr>)', function () {

    it('(B) <p style="font-weight: bold;"><em>INTERACTIVE: <type></em></p> wrapper is emitted as a sibling between <hr> and the main content div', function () {
        var blocks = _iwrSpeechBubbleFixture();
        var out = iwrExtractor.processInteractive(blocks, 0, 'OSAI201-01.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;

        // Header wrapper paragraph is emitted exactly once.
        var headerWrapperMark = '<p style="font-weight: bold;"><em>INTERACTIVE: speech_bubble</em></p>';
        assertTrue(html.indexOf(headerWrapperMark) !== -1,
            'header wrapper paragraph is present');

        // Verify ordering: <hr> → header-wrapper div → main content wrapper div.
        var hrIdx = html.indexOf('<hr style="margin: 0; border-color: green;" />');
        assertTrue(hrIdx !== -1, '<hr> separator is present');
        var headerWrapperIdx = html.indexOf(headerWrapperMark);
        assertTrue(headerWrapperIdx > hrIdx,
            'header wrapper paragraph appears AFTER the <hr>');

        // The two content divs must both be siblings — the header wrapper div
        // first, then the main content wrapper div.
        var firstContentDivIdx = html.indexOf(
            '<div style="padding: 10px 12px; font-size: 0.85em; color: #333; background: #fafafa;">'
        );
        var lastContentDivIdx = html.lastIndexOf(
            '<div style="padding: 10px 12px; font-size: 0.85em; color: #333; background: #fafafa;">'
        );
        assertTrue(firstContentDivIdx !== -1 && lastContentDivIdx !== -1,
            'two content wrapper divs exist');
        assertTrue(firstContentDivIdx < lastContentDivIdx,
            'header wrapper div is emitted BEFORE the main content wrapper div');
        assertTrue(firstContentDivIdx > hrIdx,
            'header wrapper div is the first content div AFTER the <hr>');
        assertTrue(headerWrapperIdx > firstContentDivIdx && headerWrapperIdx < lastContentDivIdx,
            'header wrapper paragraph sits INSIDE the first (header) wrapper div');
    });

});

describe('Interactive wrapper rendering — Fix C (diagnostic text suppressed)', function () {

    it('(C) "No structured data detected" diagnostic paragraph is suppressed; <p><em></em></p> empty element still emitted', function () {
        var blocks = _iwrSpeechBubbleFixture();
        var out = iwrExtractor.processInteractive(blocks, 0, 'OSAI201-01.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        // The diagnostic paragraph (not the preserved <!-- Data Summary -->
        // comment) must no longer render visible text.
        assertTrue(html.indexOf('<p><em>No structured data detected') === -1,
            'diagnostic <p><em>No structured data detected…</em></p> is NOT rendered');
        assertTrue(html.indexOf('check InteractiveExtractor boundary detection') === -1,
            'diagnostic follow-up text is NOT in the rendered HTML');
        assertTrue(html.indexOf('<p><em></em></p>') !== -1,
            'empty <p><em></em></p> element still emitted in its place');
    });

});

describe('Interactive wrapper rendering — Fix D (Layout-Row Siblings label suppressed)', function () {

    it('(D) literal "Layout-Row Siblings:" label text is suppressed, but its paragraph element is retained', function () {
        var blocks = _iwrSpeechBubbleFixture();
        var out = iwrExtractor.processInteractive(blocks, 0, 'OSAI201-01.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Layout-Row Siblings:') === -1,
            '"Layout-Row Siblings:" label text is NOT in the rendered HTML');
        assertTrue(html.indexOf('<p style="font-weight: bold; margin: 4px 0;"></p>') !== -1,
            'empty bold paragraph element is still emitted (label paragraph retained)');
    });

});

describe('Interactive wrapper rendering — Fix E (siblings children reordered)', function () {

    it('(E) Note: [tag] annotation paragraph is emitted BEFORE the URL paragraph it annotates', function () {
        var blocks = _iwrSpeechBubbleFixture();
        var out = iwrExtractor.processInteractive(blocks, 0, 'OSAI201-01.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        var notePos = html.indexOf('Note: [image]');
        var urlPos = html.indexOf('https://example.com/unicorn.png');
        assertTrue(notePos !== -1, 'Note: [image] annotation paragraph is present');
        assertTrue(urlPos !== -1, 'URL paragraph is present');
        assertTrue(notePos < urlPos,
            'Note: [image] annotation is emitted BEFORE the URL paragraph it annotates');
    });

});

describe('Interactive wrapper rendering — Fix F (trailing empty paragraph)', function () {

    it('(F) Layout-Row Siblings section\'s final child is <p style="margin: 2px 0;"></p>', function () {
        var blocks = _iwrSpeechBubbleFixture();
        var out = iwrExtractor.processInteractive(blocks, 0, 'OSAI201-01.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;

        // Locate the Layout-Row Siblings section — it's the dashed-top div
        // that contains the empty bold label paragraph emitted by Fix D.
        var labelMark = '<p style="font-weight: bold; margin: 4px 0;"></p>';
        var labelIdx = html.indexOf(labelMark);
        assertTrue(labelIdx !== -1, 'siblings section label paragraph located');

        // Take everything from the label paragraph up to the next closing
        // </div> — that's the siblings section body.
        var sectionTail = html.substring(labelIdx);
        var closeIdx = sectionTail.indexOf('</div>');
        assertTrue(closeIdx !== -1, 'siblings section closes with </div>');
        var sectionBody = sectionTail.substring(0, closeIdx);

        // The final <p>...</p> element inside the siblings section must
        // be the trailing empty paragraph.
        var lastPIdx = sectionBody.lastIndexOf('<p style="margin: 2px 0;">');
        assertTrue(lastPIdx !== -1, 'at least one <p style="margin: 2px 0;"> in siblings section');
        var trailingFragment = sectionBody.substring(lastPIdx).trim();
        assertEqual(trailingFragment, '<p style="margin: 2px 0;"></p>',
            'final child of siblings section is <p style="margin: 2px 0;"></p>');
    });

});

describe('Interactive wrapper rendering — cross-type (Fixes A–C applied to non-speech_bubble interactive)', function () {

    it('(X) a flip_card interactive receives the same header-bar, header-wrapper, and empty-diagnostic fixes', function () {
        var blocks = [
            _iwrPlain('[flip card]'),
            _iwrPara([{ text: '[body]' }])
        ];
        var out = iwrExtractor.processInteractive(blocks, 0, 'OSAI201-02.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;

        // Fix A: header bar reads "🔧 INTERACTIVE: flip_card" (no TIER 1).
        assertTrue(html.indexOf('🔧 INTERACTIVE: flip_card') !== -1,
            'flip_card header bar reads "🔧 INTERACTIVE: flip_card"');
        assertTrue(html.indexOf('TIER 1') === -1,
            'flip_card header bar does NOT contain "TIER 1"');

        // Fix B: header wrapper paragraph is emitted for flip_card.
        assertTrue(html.indexOf('<p style="font-weight: bold;"><em>INTERACTIVE: flip_card</em></p>') !== -1,
            'flip_card header wrapper paragraph is present');

        // Fix C: "No structured data detected" diagnostic paragraph is suppressed
        // (the preserved <!-- Data Summary --> comment is allowed to retain the string).
        assertTrue(html.indexOf('<p><em>No structured data detected') === -1,
            'diagnostic <p><em>No structured data detected…</em></p> is NOT in flip_card output');
        assertTrue(html.indexOf('<p><em></em></p>') !== -1,
            'empty <p><em></em></p> element still emitted for flip_card');
    });

});
