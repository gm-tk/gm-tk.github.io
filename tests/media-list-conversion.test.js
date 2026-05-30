/**
 * Media List table-conversion defect coverage (Module Development mode).
 *
 * The Media List `.docx` → `_media_list.txt` path must emit a tab-delimited
 * seven-column table — `Item No.`, `WTPg No.`, `Item Type`, `Description`,
 * `Source`, `URL`, `ECR approval` — drawn ONLY from the document's single media
 * table. These cases lock in the defect fixes layered on top of the structural
 * extraction already covered by tests/media-list-converter.test.js and
 * tests/media-list-extraction.test.js:
 *
 *   1. the header row is always emitted first (never dropped);
 *   2. the conventional `Example` (cheetah stock-photo) sample row is excluded;
 *   3. horizontally-merged boilerplate rows (e.g. the "Reminder: …" note that
 *      spans the table width) are dropped — by structure, not by phrase;
 *   4. the auto-numbered `Item No.` column (a Word <w:numPr> list number, so its
 *      literal text is empty) is reconstructed as a sequential `1.`, `2.`, `3.`…;
 *   5. all pre-table body content is excluded;
 *   6. the tab-delimited seven-column structure — incl. the trailing (usually
 *      empty) `ECR approval` column — is preserved on every data row.
 *
 * Self-contained `mlcv*` builders are used so this file shares no helpers with
 * the sibling media-list test files. The pure, synchronous convertParsedResult()
 * core is exercised over canned DocxParser results, so it runs headlessly (the
 * real DocxParser is never loaded by the Node test runner).
 */

'use strict';

// ---- Self-contained canned DocxParser content builders ---------------------

// The canonical media-list column labels, in order.
var MLCV_HEADERS = ['Item No.', 'WTPg No.', 'Item Type', 'Description', 'Source', 'URL', 'ECR approval'];

// The merged boilerplate line that currently leaks into output; it spans the
// whole table width as a single grid-merged cell and is NOT a data row.
var MLCV_REMINDER = 'Reminder: List all external platforms recommended to the student in the module for copyright review (old and new links)';

// A non-table body paragraph.
function mlcvPara(text) {
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: {}, hyperlink: null }],
            text: text, heading: null, listLevel: 0,
            listNumId: null, listFormat: null, isListItem: false
        }
    };
}

// A bullet (submission-checklist) paragraph.
function mlcvBullet(text) {
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: {}, hyperlink: null }],
            text: text, heading: null, listLevel: 0,
            listNumId: '7', listFormat: 'bullet', isListItem: true
        }
    };
}

// A plain table cell carrying a single paragraph of literal text.
function mlcvCell(text) {
    return { paragraphs: [mlcvPara(text).data] };
}

// An AUTO-NUMBERED Item No. cell: the displayed "1./2./3." comes from a Word
// <w:numPr> list number, so the literal run text is EMPTY — exactly what plain
// text extraction sees. The converter must re-derive the ordinal from row order.
function mlcvNumberedCell() {
    return {
        paragraphs: [{
            runs: [], text: '', heading: null, listLevel: 0,
            listNumId: '3', listFormat: 'decimal', isListItem: true
        }]
    };
}

// A genuine data row: an auto-numbered (empty) Item No. cell followed by the
// remaining six column texts [WTPg No., Item Type, Description, Source, URL, ECR].
function mlcvDataRow(rest) {
    return { cells: [mlcvNumberedCell()].concat(rest.map(mlcvCell)) };
}

// The literal header row (one cell per canonical label).
function mlcvHeaderRow() {
    return { cells: MLCV_HEADERS.map(mlcvCell) };
}

// The conventional "Example" sample row (literal "Example" in the Item No. col).
function mlcvExampleRow() {
    return {
        cells: ['Example', '1', 'Image', 'Cheetah running across the savannah',
            'iStock', 'https://www.istockphoto.com/photo/cheetah-123', 'Yes'].map(mlcvCell)
    };
}

// A horizontally-merged boilerplate row: a SINGLE grid-spanning cell across the
// table width (the shared parser surfaces a <w:gridSpan> <w:tc> as ONE cell).
function mlcvMergedRow(text) {
    return { cells: [mlcvCell(text)] };
}

function mlcvTable(rows) {
    return { type: 'table', data: { rows: rows } };
}

function mlcvConvert(content) {
    return new MediaListConverter().convertParsedResult({ content: content, metadata: {} });
}

// A representative Media List document: the full per-module pre-table boilerplate
// (template title, submission checklist + bullets, the MEDIA LIST heading, the
// instructional paragraphs), then the single media table — header, the Example
// sample, three auto-numbered data rows, and the merged Reminder boilerplate row.
function mlcvFixtureContent() {
    return [
        mlcvPara('MEDIA LIST TEMPLATE'),
        mlcvPara('SUBMISSION CHECKLIST'),
        mlcvBullet('I have listed every external media item'),
        mlcvBullet('I have signed the copyright declaration'),
        mlcvPara('MEDIA LIST'),
        mlcvPara('Before starting ensure you are familiar with the copyright policy.'),
        mlcvPara('Please supply details for ALL external media used in this module.'),
        mlcvPara('If a specific third-party item/image is crucial, flag it for early review.'),
        mlcvTable([
            mlcvHeaderRow(),
            mlcvExampleRow(),
            mlcvDataRow(['5', 'Image', 'Hero banner', 'iStock', 'https://ex.com/a.jpg', '']),
            mlcvDataRow(['8', 'Video', 'Intro clip', 'YouTube', 'https://youtu.be/abc', '']),
            mlcvDataRow(['12', 'Audio', 'Birdsong', 'Freesound', 'https://ex.com/b.mp3', '']),
            mlcvMergedRow(MLCV_REMINDER)
        ])
    ];
}

describe('MediaListConverter — Media List table conversion defects', function () {

    it('emits the header row as the first output line with all seven column labels', function () {
        var out = mlcvConvert(mlcvFixtureContent());
        var firstLine = out.split('\n')[0];
        assertEqual(firstLine, MLCV_HEADERS.join('\t'), 'first line is the literal seven-column header');
        var cols = firstLine.split('\t');
        assertEqual(cols.length, 7, 'header carries seven tab-separated columns');
        assertEqual(cols[0], 'Item No.', 'header keeps its literal Item No. label (not numbered)');
        assertEqual(cols[6], 'ECR approval', 'header keeps the trailing ECR approval label');
    });

    it('excludes the conventional Example (cheetah stock-photo) sample row', function () {
        var out = mlcvConvert(mlcvFixtureContent());
        assert(out.indexOf('Cheetah') === -1, 'the Example row description is not emitted');
        assert(out.toLowerCase().indexOf('example') === -1, 'no Example label leaks into output');
        assert(out.indexOf('istockphoto.com/photo/cheetah') === -1, 'the Example row URL is not emitted');
    });

    it('excludes the horizontally-merged "Reminder" boilerplate row', function () {
        var out = mlcvConvert(mlcvFixtureContent());
        assert(out.indexOf('Reminder: List all external platforms') === -1, 'the merged Reminder row is dropped');
        assert(out.indexOf('copyright review') === -1, 'no merged-row text leaks through');
    });

    it('reconstructs the Item No. column as sequential 1., 2., 3. across retained data rows', function () {
        var out = mlcvConvert(mlcvFixtureContent());
        var dataLines = out.split('\n').slice(1); // drop the header line
        assertEqual(dataLines.length, 3, 'three retained data rows');
        assertEqual(dataLines[0].split('\t')[0], '1.', 'first data row Item No. is 1.');
        assertEqual(dataLines[1].split('\t')[0], '2.', 'second data row Item No. is 2.');
        assertEqual(dataLines[2].split('\t')[0], '3.', 'third data row Item No. is 3.');
    });

    it('retains exactly the genuine data rows (Example + merged row excluded from the count)', function () {
        var out = mlcvConvert(mlcvFixtureContent());
        var lines = out.split('\n');
        assertEqual(lines.length, 4, 'one header line + exactly three data lines');
        assert(out.indexOf('Hero banner') !== -1, 'data row 1 retained');
        assert(out.indexOf('Intro clip') !== -1, 'data row 2 retained');
        assert(out.indexOf('Birdsong') !== -1, 'data row 3 retained');
    });

    it('excludes every pre-table paragraph (title, checklist, heading, instructions)', function () {
        var out = mlcvConvert(mlcvFixtureContent());
        assert(out.indexOf('MEDIA LIST TEMPLATE') === -1, 'the template title is excluded');
        assert(out.indexOf('SUBMISSION CHECKLIST') === -1, 'the submission-checklist heading is excluded');
        assert(out.indexOf('I have listed every external media item') === -1, 'a checklist bullet is excluded');
        assert(out.indexOf('Before starting') === -1, 'the "Before starting…" instruction is excluded');
        assert(out.indexOf('Please supply details') === -1, 'the "Please supply details…" instruction is excluded');
        assert(out.indexOf('If a specific third-party') === -1, 'the early-review instruction is excluded');
    });

    it('preserves the tab-delimited seven-column structure on every line', function () {
        var out = mlcvConvert(mlcvFixtureContent());
        var lines = out.split('\n');
        for (var i = 0; i < lines.length; i++) {
            assertEqual(lines[i].split('\t').length, 7, 'line ' + i + ' has seven tab-separated columns');
        }
        // Spot-check column order on the first data row.
        var d0 = lines[1].split('\t');
        assertEqual(d0[0], '1.', 'col 0 is the reconstructed Item No.');
        assertEqual(d0[1], '5', 'col 1 is WTPg No.');
        assertEqual(d0[2], 'Image', 'col 2 is Item Type');
        assertEqual(d0[3], 'Hero banner', 'col 3 is Description');
        assertEqual(d0[4], 'iStock', 'col 4 is Source');
        assertEqual(d0[5], 'https://ex.com/a.jpg', 'col 5 is URL');
    });

    it('keeps the trailing (empty) ECR approval column present on data rows', function () {
        var out = mlcvConvert(mlcvFixtureContent());
        var dataLine = out.split('\n')[1];
        var cells = dataLine.split('\t');
        assertEqual(cells.length, 7, 'the data row carries all seven columns');
        assertEqual(cells[6], '', 'the trailing ECR approval column is present and empty');
        // A trailing empty field means the line ends on the ECR-approval tab boundary.
        assertEqual(dataLine.charAt(dataLine.length - 1), '\t', 'line ends with the ECR-approval tab boundary');
    });

    it('also drops a merged boilerplate row whose spanned cells repeat the same text', function () {
        // Some inputs surface a horizontal merge as the SAME text repeated across
        // every spanned column rather than one collapsed cell — both are non-data.
        var content = [
            mlcvPara('Before starting ensure you are familiar with the policy.'),
            mlcvTable([
                mlcvHeaderRow(),
                mlcvDataRow(['5', 'Image', 'Hero banner', 'iStock', 'https://ex.com/a.jpg', '']),
                { cells: MLCV_HEADERS.map(function () { return mlcvCell(MLCV_REMINDER); }) }
            ])
        ];
        var out = mlcvConvert(content);
        assert(out.indexOf('Reminder: List all external platforms') === -1, 'the repeated-text merged row is dropped');
        var lines = out.split('\n');
        assertEqual(lines.length, 2, 'only the header line + one genuine data row remain');
        assertEqual(lines[1].split('\t')[0], '1.', 'the single data row is numbered 1.');
    });
});
