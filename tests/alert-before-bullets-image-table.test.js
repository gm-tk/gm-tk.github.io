/**
 * [alert] marker immediately followed by a bullets-plus-image TABLE.
 *
 * When an authored `[alert]` paragraph sits directly before a TABLE whose
 * left cell is an intro sentence + bullet list and whose right cell is an
 * [image] cell, the converter must recognise this pairing and emit a
 * single alert-wrapped paired layout:
 *
 *   <div class="row">
 *     <div class="col-md-6 col-12 paddingR">
 *       <div class="alert">
 *         <div class="row">
 *           <div class="col-12">
 *             <p>intro</p>
 *             <ul><li>…</li>…</ul>
 *           </div>
 *         </div>
 *       </div>
 *     </div>
 *     <div class="col-md-3 col-12 paddingL"><img …></div>
 *   </div>
 *
 * Before the new sub-branch, this writer pattern produced two defects:
 *   (1) an empty <div class="alert"> from the standalone [alert] fallback, AND
 *   (2) a separately-rendered un-alerted col-md-6/col-md-3 bullets+image row.
 *
 * The new sub-branch lives in the [alert] handler of _renderBlocks, runs
 * after the Session E layout-table pairing check (so isLayoutTable()-
 * qualifying tables still flow through Session E unchanged) and before
 * the Session F Sub-bug A preceding-body wrap.
 */

'use strict';

var _abbitNorm = new TagNormaliser();
var _abbitTpl = new TemplateEngine();
_abbitTpl._data = TemplateEngine._embeddedData();
_abbitTpl._loaded = true;
var _abbitConverter = new HtmlConverter(_abbitNorm, _abbitTpl);

function _abbitMkRun(text, opts) {
    opts = opts || {};
    return {
        text: text,
        formatting: {
            bold: !!opts.bold, italic: !!opts.italic, underline: false, strikethrough: false,
            color: opts.color || null, highlight: null, isRed: !!opts.isRed
        }
    };
}

function _abbitMkPara(runs, opts) {
    opts = opts || {};
    var text = runs.map(function (r) { return r.text; }).join('');
    return {
        runs: runs,
        text: text,
        heading: opts.heading || null,
        listLevel: opts.listLevel !== undefined ? opts.listLevel : null,
        listNumId: opts.listNumId || null,
        listFormat: opts.listFormat || null,
        isListItem: opts.isListItem || false
    };
}

function _abbitMkText(text, opts) { return _abbitMkPara([_abbitMkRun(text)], opts); }

function _abbitMkBullet(text) {
    return _abbitMkText(text, { isListItem: true, listLevel: 0, listFormat: 'bullet' });
}

function _abbitMkImageCell(url) {
    return {
        paragraphs: [_abbitMkPara([
            _abbitMkRun('[image]', { isRed: true }),
            _abbitMkRun(url)
        ])]
    };
}

function _abbitMkTable(leftCellParas, rightCellParas) {
    return {
        type: 'table',
        data: { rows: [{ cells: [{ paragraphs: leftCellParas }, { paragraphs: rightCellParas }] }] }
    };
}

function _abbitMkTaggedPara(tag, trailingText) {
    var runs = [_abbitMkRun(tag, { isRed: true })];
    if (trailingText) runs.push(_abbitMkRun(trailingText));
    return _abbitMkPara(runs);
}

function _abbitMkBlockPara(para) { return { type: 'paragraph', data: para }; }

function _abbitConvert(blocks) {
    var pageData = { type: 'lesson', lessonNumber: 1, filename: 'ABBIT-01.html', contentBlocks: blocks };
    var config = {
        gridRules: { defaultContent: 'col-md-8 col-12' },
        imageDefaults: { class: 'img-fluid', placeholderBase: 'https://placehold.co' }
    };
    return _abbitConverter.convertPage(pageData, config);
}

var _abbitIstockUrl = 'https://www.istockphoto.com/vector/ai-technology-in-industrial-landscape-gm2206845926-624131941';

function _abbitBuildAlertThenBulletsImageTable(imageUrl) {
    return [
        _abbitMkBlockPara(_abbitMkTaggedPara('[alert]', '')),
        _abbitMkTable(
            [
                _abbitMkText('AI is not safe for our environment due to:'),
                _abbitMkBullet('high energy consumption and CO₂ gas'),
                _abbitMkBullet('AI data centres use large amounts of water for cooling'),
                _abbitMkBullet('pollution and e-waste'),
                _abbitMkBullet('mining for rare earth materials to build AI equipment.')
            ],
            [_abbitMkImageCell(imageUrl).paragraphs[0]]
        )
    ];
}

describe('[alert] marker preceding bullets+image TABLE — alert-wrapped paired layout', function () {

    it('emits exactly one <div class="alert"> and the alert wraps the bullets column only', function () {
        var html = _abbitConvert(_abbitBuildAlertThenBulletsImageTable(_abbitIstockUrl));
        var openRe = /<div class="alert">/g;
        var matches = html.match(openRe);
        assertTrue(matches !== null && matches.length === 1,
            'exactly one <div class="alert"> must appear (got ' + (matches ? matches.length : 0) + ')');
        // The alert must live inside the paddingR (bullets) column, not paddingL (image)
        var alertIdx = html.indexOf('<div class="alert">');
        var paddingRIdx = html.indexOf('<div class="col-md-6 col-12 paddingR">');
        var paddingLIdx = html.indexOf('<div class="col-md-3 col-12 paddingL">');
        assertTrue(paddingRIdx !== -1 && paddingLIdx !== -1, 'paired columns must render');
        assertTrue(paddingRIdx < alertIdx && alertIdx < paddingLIdx,
            'alert must sit inside the paddingR column (before paddingL opens)');
    });

    it('paired row uses col-md-6 col-12 paddingR for alert/bullets and col-md-3 col-12 paddingL for image', function () {
        var html = _abbitConvert(_abbitBuildAlertThenBulletsImageTable(_abbitIstockUrl));
        assertTrue(html.indexOf('<div class="col-md-6 col-12 paddingR">') !== -1,
            'col-md-6 col-12 paddingR column must render');
        assertTrue(html.indexOf('<div class="col-md-3 col-12 paddingL">') !== -1,
            'col-md-3 col-12 paddingL column must render');
    });

    it('intro sentence renders as <p>…</p> and bullets as <ul><li>…</li>…</ul> inside the alert inner col-12', function () {
        var html = _abbitConvert(_abbitBuildAlertThenBulletsImageTable(_abbitIstockUrl));
        var alertIdx = html.indexOf('<div class="alert">');
        assertTrue(alertIdx !== -1, 'alert must render');
        var afterAlert = html.slice(alertIdx);
        var innerRowRel = afterAlert.indexOf('<div class="row">');
        var innerColRel = afterAlert.indexOf('<div class="col-12">');
        var pRel = afterAlert.indexOf('<p>AI is not safe for our environment due to:</p>');
        var ulRel = afterAlert.indexOf('<ul>');
        var liRel = afterAlert.indexOf('<li>high energy consumption and CO₂ gas</li>');
        assertTrue(innerRowRel !== -1 && innerColRel !== -1,
            'alert must wrap an inner <div class="row"><div class="col-12">…</div></div>');
        assertTrue(innerRowRel < innerColRel && innerColRel < pRel,
            'inner row/col-12 must open before the intro <p>');
        assertTrue(pRel !== -1 && ulRel !== -1 && liRel !== -1,
            'intro <p> and bullet <ul><li> must render inside the alert');
        assertTrue(pRel < ulRel && ulRel < liRel,
            'intro <p> must precede bullet <ul> which must precede <li>');
    });

    it('iStockPhoto URL with -gm<ID>- in the image cell resolves to src="images/iStock-<ID>.jpg" with alt=""', function () {
        var html = _abbitConvert(_abbitBuildAlertThenBulletsImageTable(_abbitIstockUrl));
        assertTrue(html.indexOf('src="images/iStock-2206845926.jpg"') !== -1,
            'iStock URL must map to images/iStock-<NUMERIC_ID>.jpg');
        assertTrue(html.indexOf('alt=""') !== -1, 'img alt must be empty');
        assertTrue(html.indexOf('placehold.co') === -1,
            'no placehold.co placeholder for a valid iStock URL');
    });

    it('non-iStockPhoto URL keeps placehold.co placeholder (no false-positive iStock mapping)', function () {
        var html = _abbitConvert(_abbitBuildAlertThenBulletsImageTable('https://example.com/assets/photo.jpg'));
        assertTrue(html.indexOf('src="images/iStock-') === -1,
            'non-iStock URL must not map to images/iStock-<ID>.jpg');
        assertTrue(html.indexOf('placehold.co') !== -1,
            'non-iStock URL must retain the placehold.co placeholder');
    });

    it('emitted <img> carries class="img-fluid", loading="lazy", and uses self-closing /> style', function () {
        var html = _abbitConvert(_abbitBuildAlertThenBulletsImageTable(_abbitIstockUrl));
        var imgMatch = html.match(/<img [^>]+>/);
        assertTrue(imgMatch !== null, 'img tag must render');
        var imgTag = imgMatch[0];
        assertTrue(imgTag.indexOf('class="img-fluid"') !== -1, 'img must carry class="img-fluid"');
        assertTrue(imgTag.indexOf('loading="lazy"') !== -1, 'img must carry loading="lazy"');
        assertTrue(/\/>$/.test(imgTag), 'img must use self-closing /> style');
    });

    it('regression guard: [alert] + bullets+image TABLE produces exactly one alert and no empty-alert scaffolding', function () {
        var html = _abbitConvert(_abbitBuildAlertThenBulletsImageTable(_abbitIstockUrl));
        var openRe = /<div class="alert">/g;
        var matches = html.match(openRe);
        assertTrue(matches !== null && matches.length === 1,
            'exactly one <div class="alert"> must appear (regression guard against double-alert defect)');
        // Empty-alert scaffolding pattern (from alert-tag-preceding-body-association.test.js)
        var empty = /<div class="alert">\s*<div class="row">\s*<div class="col-12">\s*<\/div>\s*<\/div>\s*<\/div>/;
        assertFalse(empty.test(html),
            'no empty-alert scaffolding — the alert must contain the intro <p> and bullet <ul>');
    });

    it('fall-through guard: [alert] + a two-column table that is NOT bullets+image does not trigger the new sub-branch', function () {
        // Table whose right cell has no [image] marker — just plain text.
        var plainPlainTable = _abbitMkTable(
            [_abbitMkText('Left cell plain text.')],
            [_abbitMkText('Right cell plain text.')]
        );
        var html = _abbitConvert([
            _abbitMkBlockPara(_abbitMkTaggedPara('[alert]', '')),
            plainPlainTable
        ]);
        // The new sub-branch must NOT fire → no paired col-md-6/col-md-3 row
        assertTrue(html.indexOf('col-md-6 col-12 paddingR') === -1,
            'plain-text two-column table must not emit col-md-6 col-12 paddingR');
        assertTrue(html.indexOf('col-md-3 col-12 paddingL') === -1,
            'plain-text two-column table must not emit col-md-3 col-12 paddingL');
        // The plain cell text must still reach the output via whichever handler picks it up
        assertTrue(html.indexOf('Left cell plain text.') !== -1,
            'left cell text must still appear in the output');
        assertTrue(html.indexOf('Right cell plain text.') !== -1,
            'right cell text must still appear in the output');
    });

});
