/**
 * Tests for MediaListConverter (Module Development mode, Session 2).
 *
 * The Media List slot is a STRAIGHT FULL conversion: the entire .docx is
 * converted to the same plain-text output format the Writer's Template pipeline
 * produces, with NO [TITLE BAR] / intro-page skipping and NO phase/template
 * processing. These tests drive the pure, synchronous convertParsedResult()
 * core (over canned DocxParser results) plus the convert() entry with an
 * injected synchronous parser, so they run headlessly — the real DocxParser is
 * never loaded by the Node test runner. The shared OutputFormatter (loaded by
 * the runner) backs the formatting, so format parity is verified for real.
 */

'use strict';

// ---- Canned DocxParser content builders ------------------------------------

function mlcPara(text, fmt) {
    fmt = fmt || {};
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: fmt, hyperlink: fmt.hyperlink || null }],
            text: text,
            heading: null,
            listLevel: 0,
            listNumId: null,
            listFormat: null,
            isListItem: false
        }
    };
}

function mlcBullet(text) {
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: {}, hyperlink: null }],
            text: text,
            heading: null,
            listLevel: 0,
            listNumId: '1',
            listFormat: 'bullet',
            isListItem: true
        }
    };
}

function mlcTable(grid) {
    return {
        type: 'table',
        data: {
            rows: grid.map(function (row) {
                return {
                    cells: row.map(function (txt) {
                        return { paragraphs: [mlcPara(txt).data] };
                    })
                };
            })
        }
    };
}

describe('MediaListConverter — straight full .docx conversion', function () {

    it('convert() reuses the injected DocxParser and converts the whole document', function () {
        var parserMock = {
            parse: function () {
                return { content: [mlcPara('Alpha'), mlcPara('Beta'), mlcPara('Gamma')], metadata: {} };
            }
        };
        var mlc = new MediaListConverter({ parser: parserMock });
        var out = mlc.convert({ name: 'List.docx' });
        // Synchronous parser → synchronous string (not a Promise).
        assert(typeof out === 'string', 'sync parser yields a string, not a Promise');
        assert(out.indexOf('Alpha') !== -1, 'first block converted');
        assert(out.indexOf('Beta') !== -1, 'middle block converted');
        assert(out.indexOf('Gamma') !== -1, 'last block converted');
    });

    it('does NOT skip any leading pages/sections (unlike the writer pipeline)', function () {
        // Block 0 is front matter; a [TITLE BAR] only appears later. The writer
        // pipeline would discard everything before it; the media list must not.
        var content = [
            mlcPara('FRONT MATTER PAGE — generic submission checklist'),
            mlcPara('More boilerplate'),
            mlcPara('[TITLE BAR] Some Module'),
            mlcPara('Module body content')
        ];
        var mlc = new MediaListConverter();
        var out = mlc.convertParsedResult({ content: content, metadata: {} });
        assert(out.indexOf('FRONT MATTER PAGE') !== -1, 'leading front matter is preserved (no skip)');
        assert(out.indexOf('More boilerplate') !== -1, 'second leading block is preserved');

        // Contrast: the existing writer pipeline starting at the [TITLE BAR]
        // (contentStartIndex = 2) discards the same leading blocks.
        var writerOut = new OutputFormatter().formatAll({
            content: content, contentStartIndex: 2, contentStartFound: true, metadata: {}
        }).full;
        assert(writerOut.indexOf('FRONT MATTER PAGE') === -1,
            'sanity: the writer pipeline DOES skip the leading front matter');
    });

    it('produces output in the exact same format as the writer converter (no-skip case)', function () {
        var content = [
            mlcPara('A red instruction', { isRed: true }),
            mlcPara('Bold body', { bold: true }),
            mlcTable([['Title', 'URL'], ['Hero image', 'https://example.com/a.jpg']])
        ];
        var meta = {};
        var mlOut = new MediaListConverter().convertParsedResult({ content: content, metadata: meta });
        // When nothing is skipped, the writer pipeline (formatAll from index 0)
        // must produce a byte-identical result — same envelope, same markers.
        var writerOut = new OutputFormatter().formatAll({
            content: content, contentStartIndex: 0, contentStartFound: true, metadata: meta
        }).full;
        assertEqual(mlOut, writerOut, 'media list output equals the writer pipeline output when nothing is skipped');
        assert(mlOut.indexOf('[RED TEXT]') !== -1, 'red-text marker present (same format)');
        assert(mlOut.indexOf('**Bold body**') !== -1, 'bold marker present (same format)');
        assert(mlOut.indexOf('┌─── TABLE') !== -1, 'table box marker present (same format)');
    });

    it('preserves multi-section list content in document order', function () {
        var content = [
            mlcPara('Section One'),
            mlcBullet('Item A'),
            mlcBullet('Item B'),
            mlcPara('Section Two'),
            mlcBullet('Item C')
        ];
        var out = new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
        assert(out.indexOf('Section One') !== -1, 'first section heading preserved');
        assert(out.indexOf('Section Two') !== -1, 'second section heading preserved');
        assert(out.indexOf('• Item A') !== -1, 'bullet A preserved');
        assert(out.indexOf('• Item B') !== -1, 'bullet B preserved');
        assert(out.indexOf('• Item C') !== -1, 'bullet C (second section) preserved');
        // Document order: Section Two appears after Item B.
        assert(out.indexOf('Item B') < out.indexOf('Section Two'), 'order preserved across sections');
    });

    it('applies NO phase/template/HTML processing (plain text only)', function () {
        var content = [mlcPara('Heading-ish line', { bold: true }), mlcBullet('A bullet')];
        var out = new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
        assert(out.indexOf('<div') === -1, 'no <div> (no HTML conversion)');
        assert(out.indexOf('class="') === -1, 'no class attributes (no template/Bootstrap grid)');
        assert(out.indexOf('<!DOCTYPE') === -1, 'no document scaffold');
        assert(out.indexOf('<h1') === -1 && out.indexOf('<p>') === -1, 'no HTML tags emitted');
    });

    it('handles a single-entry media list', function () {
        var content = [mlcPara('Only one media item')];
        var out = new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
        assert(out.indexOf('Only one media item') !== -1, 'the single entry is converted');
        assert(out.indexOf('--- CONTENT START ---') !== -1, 'output envelope still produced');
    });

    it('handles an empty document gracefully', function () {
        var out = new MediaListConverter().convertParsedResult({ content: [], metadata: {} });
        assert(typeof out === 'string', 'empty document yields a string');
        assert(out.indexOf('--- CONTENT START ---') !== -1, 'envelope produced for an empty document');
    });

    it('handles malformed input gracefully', function () {
        var mlc = new MediaListConverter();
        var cases = [null, undefined, {}, { content: 'not-an-array' }, { content: null }];
        for (var i = 0; i < cases.length; i++) {
            var out = mlc.convertParsedResult(cases[i]);
            assert(typeof out === 'string', 'malformed input #' + i + ' yields a string, not a throw');
            assert(out.indexOf('--- CONTENT START ---') !== -1, 'envelope still produced for malformed input #' + i);
        }
    });
});
