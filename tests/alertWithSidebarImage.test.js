/**
 * Session E — Change 1: alert + layout-table sidebar-image pairing.
 *
 * When writer uses `[alert]` followed by a layout table whose main cell
 * contains bullets/paragraphs and whose sidebar cell contains an image,
 * the alert must consume the main cell as its body content and pair
 * side-by-side with the sidebar image. Column widths:
 *   - alert: col-md-6 col-12 paddingR
 *   - image: col-md-3 col-12 paddingL
 *
 * Regression: previously this produced an EMPTY <div class="alert">
 * with the bullet list lost.
 */

'use strict';

var _normForAlertSB = new TagNormaliser();
var _unwrapperForAlertSB = new LayoutTableUnwrapper(_normForAlertSB);
var _templateEngineForAlertSB = new TemplateEngine();
_templateEngineForAlertSB._data = TemplateEngine._embeddedData();
_templateEngineForAlertSB._loaded = true;
var _converterForAlertSB = new HtmlConverter(_normForAlertSB, _templateEngineForAlertSB);

function _asbMkPara(text, opts) {
    opts = opts || {};
    return {
        runs: [{
            text: text,
            formatting: { bold: false, italic: false, underline: false, strikethrough: false, color: null, highlight: null, isRed: false }
        }],
        text: text,
        heading: null,
        listLevel: opts.listLevel !== undefined ? opts.listLevel : null,
        listNumId: opts.listNumId || null,
        listFormat: opts.listFormat || null,
        isListItem: opts.isListItem || false
    };
}

function _asbMkBlockPara(text, opts) {
    return { type: 'paragraph', data: _asbMkPara(text, opts) };
}

function _asbMkTable(leftParas, rightParas) {
    return {
        type: 'table',
        data: {
            rows: [{
                cells: [
                    { paragraphs: leftParas },
                    { paragraphs: rightParas }
                ]
            }]
        }
    };
}

function _asbBuildFixture() {
    // [body] lead-in.  then  [alert]  then  layout table with:
    //   main cell: 4 bullet items
    //   sidebar cell: [image] + URL
    var body = _asbMkBlockPara('[body] AI uses a lot of power.');
    var alert = _asbMkBlockPara('[alert]');
    // Layout-table detection requires 2+ structural tags across 1+ cells.
    // Two [body] tags in the main cell supply the needed threshold; the
    // sidebar [image] doesn't itself count toward structuralCount.
    var table = _asbMkTable(
        [
            _asbMkPara('[body] AI is not safe for our environment due to:'),
            _asbMkPara('high energy consumption and CO\u2082 gas', { isListItem: true, listLevel: 0, listFormat: 'bullet' }),
            _asbMkPara('water use for cooling data centres', { isListItem: true, listLevel: 0, listFormat: 'bullet' }),
            _asbMkPara('electronic waste from old hardware', { isListItem: true, listLevel: 0, listFormat: 'bullet' }),
            _asbMkPara('rare-earth mining impact', { isListItem: true, listLevel: 0, listFormat: 'bullet' }),
            _asbMkPara('[body] These costs add up quickly.')
        ],
        [
            _asbMkPara('[image] https://www.istockphoto.com/photo/something-gm2206845926')
        ]
    );
    return [body, alert, table];
}

function _asbConvert(blocks) {
    _unwrapperForAlertSB.unwrapLayoutTables(blocks, 0);
    var pageData = { type: 'lesson', lessonNumber: 1, filename: 'TEST-01.html', contentBlocks: blocks };
    var config = { gridRules: { defaultContent: 'col-md-8 col-12' }, imageDefaults: { class: 'img-fluid', placeholderBase: 'https://placehold.co' } };
    return _converterForAlertSB.convertPage(pageData, config);
}

describe('Session E Change 1 — alert + layout-table sidebar pairing', function () {

    it('should place bullet-list content inside the alert', function () {
        var html = _asbConvert(_asbBuildFixture());
        assertTrue(html.indexOf('<div class="alert">') !== -1,
            'alert div should be present');
        assertTrue(html.indexOf('<ul>') !== -1,
            'bullet list from main cell should render as <ul>');
        assertTrue(html.indexOf('high energy consumption') !== -1,
            'first bullet text should be inside the alert');
    });

    it('should pair the alert side-by-side with the sidebar image', function () {
        var html = _asbConvert(_asbBuildFixture());
        var alertIdx = html.indexOf('<div class="alert">');
        var imgIdx = html.indexOf('<img');
        assertTrue(alertIdx !== -1 && imgIdx !== -1,
            'both alert and image should render');
        assertTrue(alertIdx < imgIdx,
            'alert should appear before image in paired layout');
    });

    it('should use col-md-6 paddingR for the alert column', function () {
        var html = _asbConvert(_asbBuildFixture());
        assertTrue(html.indexOf('col-md-6 col-12 paddingR') !== -1,
            'alert column should be col-md-6 col-12 paddingR');
    });

    it('should use col-md-3 paddingL for the image column', function () {
        var html = _asbConvert(_asbBuildFixture());
        assertTrue(html.indexOf('col-md-3 col-12 paddingL') !== -1,
            'image column should be col-md-3 col-12 paddingL');
    });

    it('should NOT emit an empty alert div (regression guard)', function () {
        var html = _asbConvert(_asbBuildFixture());
        // Match an empty alert: opening tag followed only by whitespace + closing
        var emptyAlert = /<div class="alert">\s*<div class="row">\s*<div class="col-12">\s*<\/div>\s*<\/div>\s*<\/div>/;
        assertFalse(emptyAlert.test(html),
            'alert div should not be empty');
    });

    it('should fall through to the existing render when no sidebar is present', function () {
        // Alert with plain body content, no layout table
        var blocks = [
            _asbMkBlockPara('[alert]'),
            _asbMkBlockPara('This is an important notice.')
        ];
        var pageData = { type: 'lesson', lessonNumber: 1, filename: 'TEST-01.html', contentBlocks: blocks };
        var config = { gridRules: { defaultContent: 'col-md-8 col-12' } };
        var html = _converterForAlertSB.convertPage(pageData, config);
        assertTrue(html.indexOf('<div class="alert">') !== -1,
            'alert should still render without layout-table pairing');
        assertTrue(html.indexOf('This is an important notice.') !== -1,
            'alert content from untagged paragraph should still be consumed');
        assertTrue(html.indexOf('col-md-3 col-12 paddingL') === -1,
            'should NOT apply paired column widths when no sidebar present');
    });

});
