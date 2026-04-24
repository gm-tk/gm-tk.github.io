/**
 * TABLE-with-inline-image rendering (Sub-bug B + C).
 *
 * A table row that pairs a bullets cell (intro sentence + bullet items)
 * with a sibling [image] cell must emit a single <div class="row">
 * containing:
 *   <div class="col-md-6 col-12 paddingR">  → alert > row > col-12 > <p>intro</p><ul><li>…</li></ul>
 *   <div class="col-md-3 col-12 paddingL">  → <img …>
 *
 * iStockPhoto URLs matching /-gm<ID>-/ must resolve to
 *   src="images/iStock-<ID>.jpg"   alt=""
 *
 * Bullets-only tables and image-only tables must retain their existing
 * single-column behaviour.
 */

'use strict';

var _twiiNorm = new TagNormaliser();
var _twiiTpl = new TemplateEngine();
_twiiTpl._data = TemplateEngine._embeddedData();
_twiiTpl._loaded = true;
var _twiiConverter = new HtmlConverter(_twiiNorm, _twiiTpl);

function _twiiMkRun(text, opts) {
    opts = opts || {};
    return {
        text: text,
        formatting: {
            bold: !!opts.bold, italic: !!opts.italic, underline: false, strikethrough: false,
            color: opts.color || null, highlight: null, isRed: !!opts.isRed
        }
    };
}

function _twiiMkPara(runs, opts) {
    opts = opts || {};
    var text = runs.map(function (r) { return r.text; }).join('');
    return {
        runs: runs,
        text: text,
        heading: null,
        listLevel: opts.listLevel !== undefined ? opts.listLevel : null,
        listNumId: opts.listNumId || null,
        listFormat: opts.listFormat || null,
        isListItem: opts.isListItem || false
    };
}

function _twiiMkText(text, opts) { return _twiiMkPara([_twiiMkRun(text)], opts); }

function _twiiMkBullet(text) {
    return _twiiMkText(text, { isListItem: true, listLevel: 0, listFormat: 'bullet' });
}

function _twiiMkImageCell(url) {
    return {
        paragraphs: [_twiiMkPara([
            _twiiMkRun('[image]', { isRed: true }),
            _twiiMkRun(url)
        ])]
    };
}

function _twiiMkTable(leftCellParas, rightCellParas) {
    return {
        type: 'table',
        data: { rows: [{ cells: [{ paragraphs: leftCellParas }, { paragraphs: rightCellParas }] }] }
    };
}

function _twiiConvert(blocks) {
    var pageData = { type: 'lesson', lessonNumber: 1, filename: 'TWII-01.html', contentBlocks: blocks };
    var config = {
        gridRules: { defaultContent: 'col-md-8 col-12' },
        imageDefaults: { class: 'img-fluid', placeholderBase: 'https://placehold.co' }
    };
    return _twiiConverter.convertPage(pageData, config);
}

var _twiiIstockUrl = 'https://www.istockphoto.com/vector/ai-technology-in-industrial-landscape-gm2206845926-624131941';

describe('Sub-bug B + C — table with bullets + inline [image] renders paired layout', function () {

    it('emits a single row with col-md-6 paddingR alert and col-md-3 paddingL image', function () {
        var table = _twiiMkTable(
            [
                _twiiMkText('**AI is not safe for our environment due to:**'),
                _twiiMkBullet('high energy consumption and CO₂ gas'),
                _twiiMkBullet('AI data centres use large amounts of water for cooling'),
                _twiiMkBullet('pollution and e-waste'),
                _twiiMkBullet('mining for rare earth materials to build AI equipment.')
            ],
            [_twiiMkImageCell(_twiiIstockUrl).paragraphs[0]]
        );
        var html = _twiiConvert([table]);
        assertTrue(html.indexOf('col-md-6 col-12 paddingR') !== -1,
            'row should contain col-md-6 col-12 paddingR column');
        assertTrue(html.indexOf('col-md-3 col-12 paddingL') !== -1,
            'row should contain col-md-3 col-12 paddingL column');
        assertTrue(html.indexOf('<div class="alert">') !== -1,
            'paddingR column should wrap an alert div');
        var ulIdx = html.indexOf('<ul>');
        var liIdx = html.indexOf('<li>');
        assertTrue(ulIdx !== -1 && liIdx !== -1, 'bullet list should render inside the alert');
    });

    it('strips **bold** markdown from the intro sentence — renders plain <p>', function () {
        var table = _twiiMkTable(
            [
                _twiiMkText('**AI is not safe for our environment due to:**'),
                _twiiMkBullet('cost'),
                _twiiMkBullet('carbon')
            ],
            [_twiiMkImageCell(_twiiIstockUrl).paragraphs[0]]
        );
        var html = _twiiConvert([table]);
        assertTrue(html.indexOf('<p>AI is not safe for our environment due to:</p>') !== -1,
            'intro should render as plain <p>…</p> with ** markers stripped');
        // No <b> wrapping the intro
        assertTrue(html.indexOf('<p><b>AI is not safe') === -1,
            'intro <p> should not be wrapped in <b>');
    });

    it('renders bullet items as <li> elements verbatim (no leading • character)', function () {
        var table = _twiiMkTable(
            [
                _twiiMkText('Intro text.'),
                _twiiMkBullet('• pre-bulleted item'),
                _twiiMkBullet('regular item')
            ],
            [_twiiMkImageCell(_twiiIstockUrl).paragraphs[0]]
        );
        var html = _twiiConvert([table]);
        assertTrue(html.indexOf('<li>pre-bulleted item</li>') !== -1,
            'leading • character should be stripped from bullet list items');
        assertTrue(html.indexOf('<li>regular item</li>') !== -1,
            'regular bullet item should render verbatim');
    });

    it('maps iStockPhoto URL with -gm<ID>- to src="images/iStock-<ID>.jpg"', function () {
        var table = _twiiMkTable(
            [_twiiMkText('intro'), _twiiMkBullet('item')],
            [_twiiMkImageCell(_twiiIstockUrl).paragraphs[0]]
        );
        var html = _twiiConvert([table]);
        assertTrue(html.indexOf('src="images/iStock-2206845926.jpg"') !== -1,
            'iStock URL should map to images/iStock-<ID>.jpg');
        assertTrue(html.indexOf('placehold.co') === -1,
            'no placehold.co placeholder should appear for iStock URL');
        assertTrue(html.indexOf('alt=""') !== -1, 'alt should be empty');
    });

    it('non-iStockPhoto URL keeps placehold.co placeholder path (no iStock mapping)', function () {
        var table = _twiiMkTable(
            [_twiiMkText('intro'), _twiiMkBullet('item')],
            [_twiiMkImageCell('https://example.com/assets/photo.jpg').paragraphs[0]]
        );
        var html = _twiiConvert([table]);
        assertTrue(html.indexOf('src="images/iStock-') === -1,
            'non-iStock URL should not map to images/iStock-<ID>.jpg');
        assertTrue(html.indexOf('placehold.co') !== -1,
            'non-iStock URL should retain the placehold.co placeholder');
    });

    it('<img …> carries class="img-fluid" loading="lazy" and alt=""', function () {
        var table = _twiiMkTable(
            [_twiiMkText('intro'), _twiiMkBullet('item')],
            [_twiiMkImageCell(_twiiIstockUrl).paragraphs[0]]
        );
        var html = _twiiConvert([table]);
        var imgMatch = html.match(/<img [^>]+>/);
        assertTrue(imgMatch !== null, 'img tag should render');
        var imgTag = imgMatch[0];
        assertTrue(imgTag.indexOf('class="img-fluid"') !== -1, 'img should carry class="img-fluid"');
        assertTrue(imgTag.indexOf('loading="lazy"') !== -1, 'img should carry loading="lazy"');
        assertTrue(imgTag.indexOf('alt=""') !== -1, 'img should carry alt=""');
    });

    it('bullets-only table (no image cell) retains existing single-column grid behaviour', function () {
        var table = _twiiMkTable(
            [_twiiMkText('intro'), _twiiMkBullet('one'), _twiiMkBullet('two')],
            [_twiiMkText('second column plain text')]
        );
        var html = _twiiConvert([table]);
        // Should NOT emit the paired col-md-6 / col-md-3 layout
        assertTrue(html.indexOf('col-md-6 col-12 paddingR') === -1,
            'bullets-only table should not emit col-md-6 paddingR');
        assertTrue(html.indexOf('col-md-3 col-12 paddingL') === -1,
            'bullets-only table should not emit col-md-3 paddingL');
    });

    it('image-only table (no bullets cell) retains existing single-column handling', function () {
        var table = _twiiMkTable(
            [_twiiMkText('plain caption')],
            [_twiiMkImageCell(_twiiIstockUrl).paragraphs[0]]
        );
        var html = _twiiConvert([table]);
        assertTrue(html.indexOf('col-md-6 col-12 paddingR') === -1,
            'image-only table (no bullets) should not emit the paired col-md-6 paddingR layout');
    });

    it('integrates with a [body] + [alert] + TABLE + [body] stream from the reference test case', function () {
        function mkRed(tag, trail) {
            var runs = [_twiiMkRun(tag, { isRed: true })];
            if (trail) runs.push(_twiiMkRun(trail));
            return _twiiMkPara(runs);
        }
        var blocks = [
            { type: 'paragraph', data: mkRed('[body]', 'The building and running of AI is a big strain on our already struggling environment.') },
            { type: 'paragraph', data: mkRed('[alert]', '') },
            _twiiMkTable(
                [
                    _twiiMkText('**AI is not safe for our environment due to:**'),
                    _twiiMkBullet('high energy consumption and CO₂ gas'),
                    _twiiMkBullet('AI data centres use large amounts of water for cooling'),
                    _twiiMkBullet('pollution and e-waste'),
                    _twiiMkBullet('mining for rare earth materials to build AI equipment.')
                ],
                [_twiiMkImageCell(_twiiIstockUrl).paragraphs[0]]
            ),
            { type: 'paragraph', data: mkRed('[body]', 'Sometimes AI makes mistakes that are obvious.') }
        ];
        var html = _twiiConvert(blocks);
        // The first alert should wrap the first body paragraph
        var firstAlertIdx = html.indexOf('<div class="alert">');
        assertTrue(firstAlertIdx !== -1, 'first alert should render');
        assertTrue(html.slice(firstAlertIdx, firstAlertIdx + 600).indexOf('The building and running of AI') !== -1,
            'first alert should wrap the first body paragraph');
        // The paired row follows
        assertTrue(html.indexOf('col-md-6 col-12 paddingR') !== -1,
            'paired alert+image row should emit col-md-6 paddingR');
        assertTrue(html.indexOf('src="images/iStock-2206845926.jpg"') !== -1,
            'iStock URL should resolve to images/iStock-2206845926.jpg');
        // Trailing body renders in col-md-8
        assertTrue(html.indexOf('<p>Sometimes AI makes mistakes that are obvious.</p>') !== -1,
            'trailing body paragraph should render after the paired row');
    });

});
