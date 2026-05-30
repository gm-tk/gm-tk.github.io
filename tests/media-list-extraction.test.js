/**
 * Structural-extraction coverage for MediaListConverter (Module Development mode).
 *
 * The Media List .txt must contain ONLY the genuine media-list table's data
 * rows — never the per-module boilerplate that precedes them (template heading,
 * submission checklist, "Before starting…" guidance, "Please supply details…"
 * paragraph, early-copyright notes). The exclusion is content-agnostic and
 * STRUCTURAL: the target table is found by HEADER-ROW content (Item No., WTPg
 * No., Item Type, Description, Source, URL, and an optional trailing ECR
 * approval), not by string-matching intro phrases and not by table position.
 *
 * These cases complement tests/media-list-converter.test.js (which covers the
 * convert() entry + core mechanics). Self-contained `ext*` builders are used so
 * this file does not depend on the sibling file's helpers.
 */

'use strict';

// ---- Self-contained canned DocxParser content builders ---------------------

function extPara(text) {
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: {}, hyperlink: null }],
            text: text, heading: null, listLevel: 0,
            listNumId: null, listFormat: null, isListItem: false
        }
    };
}

function extBullet(text) {
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: {}, hyperlink: null }],
            text: text, heading: null, listLevel: 0,
            listNumId: '1', listFormat: 'bullet', isListItem: true
        }
    };
}

function extTable(grid) {
    return {
        type: 'table',
        data: {
            rows: grid.map(function (row) {
                return {
                    cells: row.map(function (txt) {
                        return { paragraphs: [extPara(txt).data] };
                    })
                };
            })
        }
    };
}

// Standard media-list column header labels (Item No. … ECR approval).
var EXT_HEADERS = ['Item No.', 'WTPg No.', 'Item Type', 'Description', 'Source', 'URL', 'ECR approval'];

// A media table = header row + supplied data rows. Pass custom `headers` to
// exercise tolerant matching (e.g. a missing optional ECR approval column).
function extMediaTable(dataRows, headers) {
    return extTable([headers || EXT_HEADERS].concat(dataRows));
}

function convertExt(content) {
    return new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
}

describe('MediaListConverter — structural exclusion of boilerplate', function () {

    it('identifies the media table by its header row, not by position', function () {
        // A non-media table appears FIRST; the media table appears later. The
        // converter must pick the media table by header content, not by order.
        var decoy = extTable([
            ['Week', 'Topic', 'Reading'],
            ['1', 'Intro', 'Chapter 1'],
            ['2', 'Theory', 'Chapter 2']
        ]);
        var media = extMediaTable([
            ['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']
        ]);
        var out = convertExt([extPara('Some intro'), decoy, extPara('More prose'), media]);
        assert(out.indexOf('Hero image') !== -1, 'the media table data row is emitted');
        assert(out.indexOf('Chapter 1') === -1, 'the earlier decoy (non-media) table is NOT picked');
        assert(out.indexOf('Theory') === -1, 'no decoy-table data leaks through');
    });

    it('excludes intro paragraphs preceding the table', function () {
        var out = convertExt([
            extPara('Welcome to the media list template.'),
            extPara('Before starting ensure you are familiar with the copyright policy.'),
            extMediaTable([['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']])
        ]);
        assert(out.indexOf('Hero image') !== -1, 'data row present');
        assert(out.indexOf('Welcome to the media list') === -1, 'first intro paragraph excluded');
        assert(out.indexOf('Before starting') === -1, 'copyright-policy guidance excluded');
    });

    it('excludes the submission checklist that precedes the table', function () {
        var out = convertExt([
            extPara('Submission Checklist'),
            extBullet('I have completed all media fields'),
            extBullet('I have signed the declaration'),
            extMediaTable([['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']])
        ]);
        assert(out.indexOf('Hero image') !== -1, 'data row present');
        assert(out.indexOf('I have completed all media fields') === -1, 'checklist item 1 excluded');
        assert(out.indexOf('I have signed the declaration') === -1, 'checklist item 2 excluded');
        assert(out.indexOf('Submission Checklist') === -1, 'checklist heading excluded');
    });

    it('excludes template and section headings', function () {
        var out = convertExt([
            extPara('PageForge Media List Template — ENGS301'),
            extPara('Section A: External Media'),
            extMediaTable([['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']])
        ]);
        assert(out.indexOf('Hero image') !== -1, 'data row present');
        assert(out.indexOf('PageForge Media List Template') === -1, 'template heading excluded');
        assert(out.indexOf('Section A') === -1, 'section heading excluded');
    });

    it('skips the conventional Example sample row', function () {
        var out = convertExt([
            extMediaTable([
                ['Example', '1', 'Image', 'A worked example item', 'iStock', 'https://ex.com/ex.jpg', 'Yes'],
                ['1', '5', 'Image', 'Real hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']
            ])
        ]);
        assert(out.indexOf('Real hero image') !== -1, 'the genuine data row is emitted');
        assert(out.indexOf('A worked example item') === -1, 'the Example sample row is skipped');
    });

    it('emits each data row cell in column order, tab-separated', function () {
        var out = convertExt([
            extMediaTable([['7', '12', 'Audio', 'Birdsong clip', 'Freesound', 'https://ex.com/b.mp3', 'Pending']])
        ]);
        var line = out.split('\n').pop(); // the single data line (after the header line)
        assert(line.indexOf('\t') !== -1, 'cells are tab-separated');
        var cells = line.split('\t');
        assertEqual(cells[0], '7', 'col 0 is Item No.');
        assertEqual(cells[2], 'Audio', 'col 2 is Item Type');
        assertEqual(cells[3], 'Birdsong clip', 'col 3 is Description');
        assertEqual(cells[5], 'https://ex.com/b.mp3', 'col 5 is URL');
    });

    it('excludes DIFFERENT, unknown boilerplate before the table (content-agnostic)', function () {
        // Front matter with wording unlike any other fixture — proves nothing is
        // string-matched against known intro phrases; exclusion is structural.
        var out = convertExt([
            extPara('Kia ora! This particular paper uses a bespoke front-matter blurb.'),
            extPara('Quokkas and zephyrs: lorem ipsum dolor sit amet, consectetur.'),
            extBullet('Idiosyncratic checklist line nobody hardcoded'),
            extMediaTable([['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg', 'Yes']])
        ]);
        assert(out.indexOf('Hero image') !== -1, 'data row still extracted');
        assert(out.indexOf('Kia ora') === -1, 'bespoke intro excluded');
        assert(out.indexOf('Quokkas') === -1, 'unusual second paragraph excluded');
        assert(out.indexOf('Idiosyncratic checklist line') === -1, 'unusual checklist line excluded');
    });

    it('still parses when the optional ECR approval column is absent', function () {
        var headers = ['Item No.', 'WTPg No.', 'Item Type', 'Description', 'Source', 'URL']; // no ECR approval
        var out = convertExt([
            extMediaTable([['1', '5', 'Image', 'Hero image', 'iStock', 'https://ex.com/a.jpg']], headers)
        ]);
        assert(out.indexOf('Hero image') !== -1, 'the table is still recognised and its data emitted');
        assert(out.indexOf('Item Type') !== -1, 'the header row is rendered');
        assert(out.indexOf('ECR approval') === -1, 'no ECR approval column present (optional, omitted)');
    });

    it('yields a safe empty result (no throw) when the data table is absent', function () {
        var threw = false, out;
        try {
            out = convertExt([extPara('Only prose, no table at all'), extBullet('A bullet')]);
        } catch (e) { threw = true; }
        assert(!threw, 'no exception is thrown when the media table is absent');
        assertEqual(out, '', 'an empty-but-valid string is returned');
    });
});
