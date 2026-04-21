/**
 * Session I — placeholder surfacing tests for the two Session H boundary
 * captures (`startBlockInlineContent`, `layoutRowSiblings`).
 *
 * The visual shell (dashed border + tier colours + header bar) must stay
 * byte-for-byte identical; the new sub-sections are additive and only
 * fire when their inputs are non-empty. Shared existing sub-sections
 * (Child blocks / Conversation entries / Writer note / Associated media)
 * must continue to render unchanged when the new sections also fire.
 */

'use strict';

var pirNormaliser = new TagNormaliser();
var pirExtractor = new InteractiveExtractor(pirNormaliser);

function _pirRun(text, isRed) {
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

function _pirPara(parts, extra) {
    var runs = [];
    for (var i = 0; i < parts.length; i++) {
        runs.push(_pirRun(parts[i].text, parts[i].isRed));
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

function _pirPlain(text, extra) {
    var block = { type: 'paragraph', data: { text: text, runs: [{ text: text }] } };
    if (extra) {
        for (var k in extra) {
            if (Object.prototype.hasOwnProperty.call(extra, k)) block[k] = extra[k];
        }
    }
    return block;
}

describe('Session I — placeholder surfaces startBlockInlineContent', function () {

    it('(a) Start-Block Content section rendered when inline remainder is non-empty', function () {
        var blocks = [
            _pirPara([
                { text: '[speech bubble]', isRed: true },
                { text: " Kia ora I'm Ariā." }
            ]),
            _pirPlain('[body]')
        ];
        var out = pirExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Start-Block Content:') !== -1,
            'Start-Block Content: header present');
        assertTrue(html.indexOf("Kia ora I'm Ariā.") !== -1,
            'inline remainder text surfaced');
    });

    it('(b) Start-Block Content section NOT rendered when inline remainder is empty', function () {
        var blocks = [
            _pirPara([{ text: '[speech bubble]', isRed: true }]),
            _pirPlain('[body]')
        ];
        var out = pirExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertEqual(out.startBlockInlineContent, null,
            'boundary capture is null');
        assertTrue(html.indexOf('Start-Block Content:') === -1,
            'no Start-Block Content: header in rendered HTML');
    });

});

describe('Session I — placeholder surfaces layoutRowSiblings', function () {

    it('(c) Layout-Row Siblings section rendered when the list is non-empty', function () {
        var blocks = [
            _pirPara([{ text: '[speech bubble]', isRed: true }], { _layoutRowId: 'L1' }),
            _pirPara([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/img.png' }
            ], { _layoutRowId: 'L1' }),
            _pirPlain('[body]')
        ];
        var out = pirExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Layout-Row Siblings:') !== -1,
            'Layout-Row Siblings: header present');
    });

    it('(d) each sibling surfaces paragraph text, media URL in <em>, and red-text Note: line', function () {
        var blocks = [
            _pirPara([{ text: '[speech bubble]', isRed: true }], { _layoutRowId: 'L1' }),
            _pirPara([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/img.png ' },
                { text: 'CS: render the Ariā avatar', isRed: true }
            ], { _layoutRowId: 'L1' }),
            _pirPlain('[body]')
        ];
        var out = pirExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Layout-Row Siblings:') !== -1,
            'header present');
        assertTrue(html.indexOf('https://example.com/img.png') !== -1,
            'image URL surfaced');
        assertTrue(html.indexOf('<em>https://example.com/img.png</em>') !== -1,
            'URL wrapped in <em>');
        assertTrue(html.indexOf('Note: CS: render the Ariā avatar') !== -1,
            'red-text note surfaced with Note: prefix');
        assertTrue(html.indexOf('font-style: italic') !== -1,
            'note line uses italic style');
    });

});

describe('Session I — existing sub-sections continue to render (regression)', function () {

    it('(e) Child Blocks / Conversation Entries / Writer note / Associated media all coexist with Start-Block Content + Layout-Row Siblings', function () {
        var blocks = [
            _pirPara([
                { text: '[speech bubble Conversation layout]', isRed: true },
                { text: " Kia ora I'm Ariā." }
            ], { _layoutRowId: 'L2' }),
            _pirPara([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/sibling.png' }
            ], { _layoutRowId: 'L2' }),
            _pirPlain('Prompt 1: First question'),
            _pirPara([
                { text: '[image]', isRed: true },
                { text: ' https://example.com/inline.png' }
            ]),
            _pirPlain('AI response: First answer'),
            _pirPara([
                { text: '🔴[RED TEXT]', isRed: false },
                { text: 'CS: tone should be friendly', isRed: true },
                { text: '[/RED TEXT]🔴', isRed: false }
            ]),
            _pirPlain('[body]')
        ];
        var out = pirExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('Conversation entries:') !== -1,
            'Conversation entries section present');
        assertTrue(html.indexOf('First question') !== -1, 'Prompt 1 text present');
        assertTrue(html.indexOf('First answer') !== -1, 'AI response text present');
        assertTrue(html.indexOf('Associated media:') !== -1,
            'Associated media section present');
        assertTrue(html.indexOf('https://example.com/inline.png') !== -1,
            'inline image URL in associated media');
        assertTrue(html.indexOf('Writer note:') !== -1,
            'boundary writer note line present');
        assertTrue(html.indexOf('tone should be friendly') !== -1,
            'writer note text present');
        assertTrue(html.indexOf('Start-Block Content:') !== -1,
            'Start-Block Content header present');
        assertTrue(html.indexOf("Kia ora I'm Ariā.") !== -1,
            'start block inline content present');
        assertTrue(html.indexOf('Layout-Row Siblings:') !== -1,
            'Layout-Row Siblings header present');
        assertTrue(html.indexOf('https://example.com/sibling.png') !== -1,
            'sibling image URL present');
    });

});

describe('Session I — placeholder shell is byte-for-byte unchanged when new sections do not fire', function () {

    it('(f) Tier 1 dashed border, green colour class, TIER 1 INTERACTIVE label, and header bar all preserved; no new section headers emitted', function () {
        var blocks = [
            _pirPlain('[flip card]'),
            _pirPara([
                { text: '[front] Front One' }
            ]),
            _pirPara([
                { text: '[back] Back One' }
            ]),
            _pirPlain('[body]')
        ];
        var out = pirExtractor.processInteractive(blocks, 0, 'test.html', null, false);
        assertNotNull(out);
        var html = out.placeholderHtml;
        assertTrue(html.indexOf('border: 2px dashed green') !== -1,
            'tier 1 green dashed border preserved');
        assertTrue(html.indexOf('TIER 1 INTERACTIVE') !== -1,
            'tier 1 label preserved');
        assertTrue(html.indexOf('background: #e6f9e6') !== -1,
            'tier 1 background colour preserved');
        assertTrue(html.indexOf('INTERACTIVE_START: flip_card') !== -1,
            'data-reference comment preserved');
        assertTrue(html.indexOf('INTERACTIVE_END: flip_card') !== -1,
            'data-end comment preserved');
        assertTrue(html.indexOf('Start-Block Content:') === -1,
            'no Start-Block Content: header when inline remainder is null');
        assertTrue(html.indexOf('Layout-Row Siblings:') === -1,
            'no Layout-Row Siblings: header when list is empty');
    });

});
