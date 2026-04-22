/**
 * Session I — end-to-end integration test for the OSAI201-01-WT
 * speech-bubble-in-a-layout-table pattern.
 *
 * Synthetic fixture (no .docx): a 2-column layout-table row where
 *   Cell 1: `[speech bubble]` + inline bubble text (Kia ora...),
 *   Cell 2: `[image]` + image URL + fully-red `CS:` writer note,
 * followed by a standalone `[body]` paragraph and a body paragraph.
 *
 * Pipeline: LayoutTableUnwrapper.unwrapLayoutTables() →
 *           InteractiveExtractor.processInteractive() →
 *           InteractiveExtractor.generateReferenceDocument()
 *
 * Expected captures surfaced INSIDE the placeholder:
 *   - Start-Block Content: bubble text
 *   - Layout-Row Siblings: image URL (<em>), CS note (Note: line)
 *
 * Outside the placeholder: the `[body]` paragraph is NOT duplicated
 * inside the placeholder HTML.
 */

'use strict';

var sbiNormaliser = new TagNormaliser();
var sbiUnwrapper = new LayoutTableUnwrapper(sbiNormaliser);
var sbiExtractor = new InteractiveExtractor(sbiNormaliser);

// ------------------------------------------------------------------
// Helpers (mirrors tests/layoutTableUnwrapper.test.js mkPara/mkTable)
// ------------------------------------------------------------------

function _sbiRun(text, isRed) {
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

function _sbiPara(parts) {
    var runs = [];
    for (var i = 0; i < parts.length; i++) {
        runs.push(_sbiRun(parts[i].text, parts[i].isRed));
    }
    var text = parts.map(function (p) { return p.text; }).join('');
    return {
        runs: runs, text: text,
        heading: null, listLevel: null, listNumId: null,
        listFormat: null, isListItem: false
    };
}

// One table cell = array of paragraphs (each built from _sbiPara).
function _sbiCell(paragraphs) {
    return { paragraphs: paragraphs };
}

// Layout-table fixture matching OSAI201-01-WT speech-bubble pattern.
function _buildSpeechBubbleLayoutFixture() {
    var cell1 = _sbiCell([
        _sbiPara([
            { text: '[speech bubble]', isRed: true },
            { text: " Kia ora I'm Ariā." }
        ])
    ]);
    var cell2 = _sbiCell([
        _sbiPara([
            { text: '[image]', isRed: true },
            { text: ' https://example.com/aria-avatar.png' }
        ]),
        _sbiPara([
            { text: 'CS: render the Ariā avatar at 120px square', isRed: true }
        ])
    ]);
    var table = {
        type: 'table',
        data: {
            rows: [{ cells: [cell1, cell2] }]
        }
    };
    return [
        table,
        {
            type: 'paragraph',
            data: _sbiPara([{ text: '[body]', isRed: true }])
        },
        {
            type: 'paragraph',
            data: _sbiPara([{ text: 'Subsequent body paragraph after the layout table.' }])
        }
    ];
}

function _processSpeechBubbleFixture() {
    var blocks = _buildSpeechBubbleLayoutFixture();
    sbiUnwrapper.unwrapLayoutTables(blocks, 0);
    // Find the unwrapped speech bubble start block (carries the [speech bubble]
    // tag). After unwrapping, cell-1 main content is at some index — find it.
    var startIndex = -1;
    for (var i = 0; i < blocks.length; i++) {
        var b = blocks[i];
        if (b.type !== 'paragraph' || !b.data || !b.data.text) continue;
        if (b.data.text.indexOf('[speech bubble]') !== -1) {
            startIndex = i;
            break;
        }
    }
    assertTrue(startIndex !== -1, 'start block located after unwrap');
    var out = sbiExtractor.processInteractive(blocks, startIndex, 'OSAI201-01.html', null, false);
    return { blocks: blocks, startIndex: startIndex, out: out };
}

// ------------------------------------------------------------------
// Tests
// ------------------------------------------------------------------

describe('Session I — speech-bubble layout-table integration', function () {

    it('(a) placeholder HTML contains the bubble text (Kia ora...)', function () {
        var ctx = _processSpeechBubbleFixture();
        assertNotNull(ctx.out);
        var html = ctx.out.placeholderHtml;
        assertTrue(html.indexOf('Start-Block Content:') !== -1,
            'Start-Block Content section rendered');
        assertTrue(html.indexOf("Kia ora I'm Ariā.") !== -1,
            'bubble text surfaced inside placeholder');
    });

    it('(b) placeholder HTML contains the image URL', function () {
        var ctx = _processSpeechBubbleFixture();
        assertNotNull(ctx.out);
        var html = ctx.out.placeholderHtml;
        assertTrue(html.indexOf('Layout-Row Siblings:') !== -1,
            'Layout-Row Siblings section rendered');
        assertTrue(html.indexOf('https://example.com/aria-avatar.png') !== -1,
            'image URL surfaced inside placeholder');
    });

    it('(c) placeholder HTML contains the CS red-text note', function () {
        var ctx = _processSpeechBubbleFixture();
        assertNotNull(ctx.out);
        var html = ctx.out.placeholderHtml;
        assertTrue(html.indexOf('Note: CS: render the Ariā avatar at 120px square') !== -1,
            'CS red-text note surfaced with Note: prefix');
    });

    it('(d) the body paragraph after the [body] tag is NOT duplicated inside the placeholder', function () {
        var ctx = _processSpeechBubbleFixture();
        assertNotNull(ctx.out);
        var html = ctx.out.placeholderHtml;
        // The post-[body] narrative paragraph must render outside the
        // placeholder and must NOT be duplicated inside it.
        assertTrue(html.indexOf('Subsequent body paragraph after the layout table.') === -1,
            'post-[body] body paragraph text absent from placeholder');
        // Boundary must stop at or before the plain post-body paragraph;
        // its index must be strictly greater than endBlockIndex so the
        // html-converter skip loop leaves it visible as body content.
        var bodyParaIdx = -1;
        for (var i = ctx.startIndex + 1; i < ctx.blocks.length; i++) {
            var b = ctx.blocks[i];
            if (b.type === 'paragraph' && b.data && b.data.text &&
                b.data.text.indexOf('Subsequent body paragraph') !== -1) {
                bodyParaIdx = i;
                break;
            }
        }
        assertTrue(bodyParaIdx !== -1, 'post-[body] paragraph exists in stream');
        assertTrue(ctx.out.endBlockIndex < bodyParaIdx,
            'endBlockIndex stops before the post-[body] narrative paragraph');
    });

    it('(e) generateReferenceDocument() surfaces bubble text + URL + note for the speech-bubble entry', function () {
        var ctx = _processSpeechBubbleFixture();
        assertNotNull(ctx.out);
        var refDoc = sbiExtractor.generateReferenceDocument(
            [ctx.out.referenceEntry], 'OSAI201'
        );
        assertTrue(refDoc.indexOf('Start-Block Content:') !== -1,
            'reference doc includes Start-Block Content section');
        assertTrue(refDoc.indexOf("Kia ora I'm Ariā.") !== -1,
            'bubble text present in reference doc');
        assertTrue(refDoc.indexOf('Layout-Row Siblings') !== -1,
            'reference doc includes Layout-Row Siblings section');
        assertTrue(refDoc.indexOf('https://example.com/aria-avatar.png') !== -1,
            'image URL present in reference doc');
        assertTrue(refDoc.indexOf('CS: render the Ariā avatar at 120px square') !== -1,
            'CS red-text note present in reference doc');
    });

});
