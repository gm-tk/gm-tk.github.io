/**
 * Alert-tag preceding-body association (Sub-bug A).
 *
 * A standalone `[alert]` marker immediately following a `[body]` block
 * must wrap that preceding body content inside the alert's inner
 *   <div class="row"><div class="col-12"><p>…</p></div></div>
 * structure, instead of emitting the body as a sibling row and an empty
 * alert as a second row.
 */

'use strict';

var _atpbNorm = new TagNormaliser();
var _atpbTpl = new TemplateEngine();
_atpbTpl._data = TemplateEngine._embeddedData();
_atpbTpl._loaded = true;
var _atpbConverter = new HtmlConverter(_atpbNorm, _atpbTpl);

function _atpbMkRun(text, opts) {
    opts = opts || {};
    return {
        text: text,
        formatting: {
            bold: !!opts.bold, italic: !!opts.italic, underline: false, strikethrough: false,
            color: opts.color || null, highlight: null, isRed: !!opts.isRed
        }
    };
}

function _atpbMkPara(runs, opts) {
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

function _atpbMkTaggedPara(tag, trailingText, opts) {
    var runs = [_atpbMkRun(tag, { isRed: true })];
    if (trailingText) runs.push(_atpbMkRun(trailingText));
    return _atpbMkPara(runs, opts || {});
}

function _atpbMkBlockPara(para) { return { type: 'paragraph', data: para }; }

function _atpbConvert(blocks) {
    var pageData = { type: 'lesson', lessonNumber: 1, filename: 'ATPB-01.html', contentBlocks: blocks };
    var config = {
        gridRules: { defaultContent: 'col-md-8 col-12' },
        imageDefaults: { class: 'img-fluid', placeholderBase: 'https://placehold.co' }
    };
    return _atpbConverter.convertPage(pageData, config);
}

describe('Sub-bug A — [alert] wraps preceding [body]', function () {

    it('wraps a single preceding body paragraph inside the alert', function () {
        var html = _atpbConvert([
            _atpbMkBlockPara(_atpbMkTaggedPara('[body]', 'The building and running of AI is a big strain.')),
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', ''))
        ]);
        var alertIdx = html.indexOf('<div class="alert">');
        var paraIdx = html.indexOf('<p>The building and running of AI is a big strain.</p>');
        assertTrue(alertIdx !== -1, 'alert div should be emitted');
        assertTrue(paraIdx !== -1, 'body paragraph should be emitted');
        assertTrue(alertIdx < paraIdx, 'alert should open before the body paragraph — wrapping it');
        // Empty alert regression guard
        var empty = /<div class="alert">\s*<div class="row">\s*<div class="col-12">\s*<\/div>\s*<\/div>\s*<\/div>/;
        assertFalse(empty.test(html), 'alert should not be empty');
    });

    it('does not wrap a preceding heading block (no body, heading-only run)', function () {
        var html = _atpbConvert([
            _atpbMkBlockPara(_atpbMkTaggedPara('[H2]', 'Section title', { heading: 2 })),
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', ''))
        ]);
        // The H2 should render as a heading OUTSIDE the alert (not inside it)
        var h2Idx = html.indexOf('<h2>');
        var alertIdx = html.indexOf('<div class="alert">');
        assertTrue(h2Idx !== -1, 'h2 should render somewhere');
        assertTrue(alertIdx !== -1, 'alert should still render');
        assertTrue(h2Idx < alertIdx, 'h2 should appear before alert — not inside it');
        // The alert should not contain the h2 tag
        var alertEndIdx = html.indexOf('</div></div></div>', alertIdx);
        if (alertEndIdx === -1) alertEndIdx = html.length;
        var alertSegment = html.slice(alertIdx, alertEndIdx + 20);
        assertTrue(alertSegment.indexOf('<h2>') === -1,
            'alert should not contain the preceding heading');
    });

    it('does not wrap a preceding body separated by an intervening heading', function () {
        var html = _atpbConvert([
            _atpbMkBlockPara(_atpbMkTaggedPara('[body]', 'Lead body paragraph.')),
            _atpbMkBlockPara(_atpbMkTaggedPara('[H3]', 'Section title', { heading: 3 })),
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', ''))
        ]);
        var alertIdx = html.indexOf('<div class="alert">');
        assertTrue(alertIdx !== -1, 'alert should render');
        // The alert should NOT contain the body paragraph (intervening heading blocks the wrap)
        var alertBlock = html.slice(alertIdx);
        assertTrue(alertBlock.indexOf('Lead body paragraph.') === -1,
            'alert should not wrap a body paragraph that has an intervening heading');
    });

    it('wraps each [body] in a body-alert-body-alert sequence into its own alert', function () {
        var html = _atpbConvert([
            _atpbMkBlockPara(_atpbMkTaggedPara('[body]', 'First body para.')),
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', '')),
            _atpbMkBlockPara(_atpbMkTaggedPara('[body]', 'Second body para.')),
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', ''))
        ]);
        // Count alert divs
        var alertCount = (html.match(/<div class="alert">/g) || []).length;
        assertEqual(alertCount, 2, 'should emit two alert divs');
        // First alert should contain the first body, second alert the second body
        var firstAlertIdx = html.indexOf('<div class="alert">');
        var secondAlertIdx = html.indexOf('<div class="alert">', firstAlertIdx + 1);
        var firstAlertSeg = html.slice(firstAlertIdx, secondAlertIdx);
        var secondAlertSeg = html.slice(secondAlertIdx);
        assertTrue(firstAlertSeg.indexOf('First body para.') !== -1,
            'first alert should wrap the first body paragraph');
        assertTrue(secondAlertSeg.indexOf('Second body para.') !== -1,
            'second alert should wrap the second body paragraph');
    });

    it('renders an alert at the start of the document as empty (nothing to wrap)', function () {
        var html = _atpbConvert([
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', '')),
            _atpbMkBlockPara(_atpbMkTaggedPara('[body]', 'Following body paragraph.'))
        ]);
        var alertIdx = html.indexOf('<div class="alert">');
        assertTrue(alertIdx !== -1, 'alert should render');
        // Inner col-12 should be empty
        var empty = /<div class="alert">\s*<div class="row">\s*<div class="col-12">\s*<\/div>\s*<\/div>\s*<\/div>/;
        assertTrue(empty.test(html),
            'alert at start of document with no preceding block should render empty');
    });

    it('wraps a preceding body containing unicode and inline punctuation', function () {
        var html = _atpbConvert([
            _atpbMkBlockPara(_atpbMkTaggedPara('[body]',
                'Mā te wā — kaitiakitanga is about care for the whenua; CO₂ matters.')),
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', ''))
        ]);
        var alertIdx = html.indexOf('<div class="alert">');
        assertTrue(alertIdx !== -1, 'alert should render');
        var alertBlock = html.slice(alertIdx);
        assertTrue(alertBlock.indexOf('Mā te wā — kaitiakitanga is about care for the whenua; CO₂ matters.') !== -1,
            'alert should wrap body text with unicode characters and inline punctuation intact');
    });

    it('emits exact nesting <div class="alert"><div class="row"><div class="col-12">…<p>…</p>…</div></div></div>', function () {
        var html = _atpbConvert([
            _atpbMkBlockPara(_atpbMkTaggedPara('[body]', 'Nested structure test paragraph.')),
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', ''))
        ]);
        // The exact nesting, whitespace-collapsed, should contain alert > row > col-12 > <p>
        var collapsed = html.replace(/\s+/g, ' ');
        var expected = /<div class="alert"> <div class="row"> <div class="col-12"> <p>Nested structure test paragraph.<\/p> <\/div> <\/div> <\/div>/;
        assertTrue(expected.test(collapsed),
            'alert should nest exactly as alert > row > col-12 > <p>body</p>');
    });

    it('falls through to existing behaviour when alert has following untagged body content', function () {
        // Alert with FOLLOWING untagged paragraph uses the pre-existing
        // _collectAlertContent path — the preceding-body wrap does not fire.
        var html = _atpbConvert([
            _atpbMkBlockPara(_atpbMkTaggedPara('[alert]', '')),
            _atpbMkBlockPara(_atpbMkPara([_atpbMkRun('Following untagged notice.')]))
        ]);
        var alertIdx = html.indexOf('<div class="alert">');
        assertTrue(alertIdx !== -1, 'alert should render');
        assertTrue(html.indexOf('Following untagged notice.') !== -1,
            'alert should still consume the following untagged paragraph as its content');
    });

});
