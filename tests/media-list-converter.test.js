/**
 * Tests for MediaListConverter (Module Development mode).
 *
 * The Media List slot performs STRUCTURAL media-table extraction: it locates
 * the genuine media-list table by its HEADER ROW and emits ONLY that table's
 * data rows (column header once at the top, the "Example" sample row skipped,
 * cells tab-separated in column order). All boilerplate outside the table —
 * intro paragraphs, headings, the submission checklist, hyperlink guidance — is
 * excluded structurally. These tests drive the pure, synchronous
 * convertParsedResult() core (over canned DocxParser results) plus the convert()
 * entry with an injected synchronous parser, so they run headlessly — the real
 * DocxParser is never loaded by the Node test runner.
 *
 * Structural-exclusion / content-agnostic edge cases live in the sibling file
 * tests/media-list-extraction.test.js.
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

// Standard media-list column header labels (Item No. … ECR approval).
var MEDIA_HEADERS = ['Item No.', 'WTPg No.', 'Item Type', 'Description', 'Source', 'URL', 'ECR approval'];

// Build a media table: the header row, then the supplied data rows (each an
// array of cell strings in column order). Tests add an 'Example' row as needed.
function mlcMediaTable(dataRows, headers) {
    return mlcTable([headers || MEDIA_HEADERS].concat(dataRows));
}

describe('MediaListConverter — structural media-table extraction', function () {

    it('convert() reuses the injected DocxParser and extracts the media table', function () {
        var parserMock = {
            calls: 0,
            parse: function () {
                this.calls++;
                return {
                    content: [
                        mlcPara('PageForge Writer Template — Media List'),
                        mlcPara('Before starting ensure you are familiar with the guidance.'),
                        mlcMediaTable([
                            ['Example', '1', 'Image', 'A sample item', 'iStock', 'https://ex.com/s.jpg', 'Yes'],
                            ['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes'],
                            ['2', '8', 'Video', 'Intro clip', 'YouTube', 'https://youtu.be/abc', 'Pending']
                        ])
                    ],
                    metadata: {}
                };
            }
        };
        var mlc = new MediaListConverter({ parser: parserMock });
        var out = mlc.convert({ name: 'List.docx' });
        // Synchronous parser → synchronous string (not a Promise).
        assert(typeof out === 'string', 'sync parser yields a string, not a Promise');
        assert(parserMock.calls === 1, 'the injected DocxParser was reused (parse called once)');
        assert(out.indexOf('Hero image') !== -1, 'real data row extracted');
        assert(out.indexOf('Intro clip') !== -1, 'second data row extracted');
        assert(out.indexOf('Before starting') === -1, 'leading intro guidance excluded');
        assert(out.indexOf('A sample item') === -1, 'Example sample row excluded');
    });

    it('excludes all boilerplate/paragraphs that precede the table', function () {
        var content = [
            mlcPara('PageForge Writer Template'),
            mlcPara('Submission checklist'),
            mlcPara('Please supply details for ALL external media used in this module.'),
            mlcMediaTable([
                ['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']
            ])
        ];
        var out = new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
        assert(out.indexOf('Hero image') !== -1, 'the data row is emitted');
        assert(out.indexOf('Please supply details') === -1, 'the "Please supply…" paragraph is excluded');
        assert(out.indexOf('Submission checklist') === -1, 'the submission-checklist heading is excluded');
        assert(out.indexOf('PageForge Writer Template') === -1, 'the template heading is excluded');
    });

    it('emits data rows in column order with the header rendered once at the top', function () {
        var content = [
            mlcMediaTable([
                ['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']
            ])
        ];
        var out = new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
        // A distinctive header label that never recurs in the data appears once.
        var first = out.indexOf('Item Type');
        assert(first !== -1, 'the column header is rendered');
        assert(out.indexOf('Item Type', first + 1) === -1, 'the header is rendered exactly once');
        // Column order within the data row: Description < Source < URL.
        var d = out.indexOf('Hero image');
        var s = out.indexOf('iStock');
        var u = out.indexOf('https://ex.com/a.jpg');
        assert(d !== -1 && s !== -1 && u !== -1, 'all data cells present');
        assert(d < s && s < u, 'cells emitted in column order (Description, Source, URL)');
    });

    it('preserves multiple data rows in their original row order', function () {
        var content = [
            mlcMediaTable([
                ['1', '5', 'Image', 'First item', 'iStock', 'https://ex.com/1.jpg', 'Yes'],
                ['2', '8', 'Video', 'Second item', 'YouTube', 'https://youtu.be/2', 'No'],
                ['3', '9', 'Audio', 'Third item', 'Freesound', 'https://ex.com/3.mp3', 'Yes']
            ])
        ];
        var out = new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
        assert(out.indexOf('First item') < out.indexOf('Second item'), 'row 1 precedes row 2');
        assert(out.indexOf('Second item') < out.indexOf('Third item'), 'row 2 precedes row 3');
    });

    it('applies NO phase/template/HTML processing (plain text only)', function () {
        var content = [
            mlcMediaTable([
                ['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']
            ])
        ];
        var out = new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
        assert(out.indexOf('<div') === -1, 'no <div> (no HTML conversion)');
        assert(out.indexOf('class="') === -1, 'no class attributes (no template/Bootstrap grid)');
        assert(out.indexOf('<!DOCTYPE') === -1, 'no document scaffold');
        assert(out.indexOf('┌─── TABLE') === -1, 'no formatter table-box envelope (structural extraction, not a full dump)');
    });

    it('handles a single-data-row media list', function () {
        var content = [
            mlcMediaTable([
                ['1', '5', 'Image', 'Only media item', 'iStock', 'https://ex.com/only.jpg', 'Yes']
            ])
        ];
        var out = new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
        assert(out.indexOf('Only media item') !== -1, 'the single data row is emitted');
        var n = out.split('\n').length;
        assert(n === 2, 'exactly two lines: header + one data row (got ' + n + ')');
    });

    it('returns a safe empty result and surfaces an error when no media table is present', function () {
        var notes = [];
        var mlc = new MediaListConverter({ notify: function (m) { notes.push(m); } });
        var content = [mlcPara('Just some prose'), mlcBullet('A checklist item')];
        var out = mlc.convertParsedResult({ content: content, metadata: {} });
        assert(out === '', 'no table → empty-but-valid result (empty string)');
        assert(notes.length === 1, 'a user-facing error was surfaced exactly once');
        assert(/media table/i.test(notes[0]), 'the error message explains no media table was found');
    });

    it('handles malformed input gracefully (never throws)', function () {
        var mlc = new MediaListConverter();
        var cases = [null, undefined, {}, { content: 'not-an-array' }, { content: null }];
        for (var i = 0; i < cases.length; i++) {
            var out = mlc.convertParsedResult(cases[i]);
            assert(out === '', 'malformed input #' + i + ' yields an empty string, not a throw');
        }
    });
});
