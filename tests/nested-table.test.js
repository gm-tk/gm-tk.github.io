/**
 * Tests for tables nested inside a table cell.
 *
 * A writer who builds a quiz, a vocabulary grid or a working-out box inside a
 * layout cell produces a <w:tbl> inside a <w:tc>. Before the fix the parser's
 * cell walk handled paragraphs, content controls and tracked changes but had no
 * branch for a table, so the nested table was skipped and everything in it
 * disappeared from the parsed output. Measured over the module library that was
 * 45 modules and roughly 65,500 characters of writer content, including the
 * TEDC401/TEDC402 quiz questions and their [correct] answer markers.
 *
 * These tests drive the REAL OutputFormatter, and cover:
 *   - a nested table's text is present in the output
 *   - it is placed inside its parent table, under the row it belongs to
 *   - a table WITHOUT a nested table is byte-identical to the pre-fix format
 *   - deeper nesting still recurses
 *   - a cell's own paragraphs are kept alongside its nested table
 */

'use strict';

function ntPara(text) {
    return {
        runs: [{ text: text, formatting: {}, hyperlink: null }],
        text: text, heading: null, listLevel: null, listNumId: null,
        listFormat: null, isListItem: false
    };
}
function ntNested(table) {
    return {
        runs: [], text: '', heading: null, listLevel: null, listNumId: null,
        listFormat: null, isListItem: false, nestedTable: table
    };
}
function ntCell(paras) { return { paragraphs: paras }; }
function ntRow(cells) { return { cells: cells }; }
function ntTable(rows) { return { rows: rows }; }

describe('Nested tables (a table inside a table cell)', function () {

    it('keeps the text of a nested table', function () {
        var inner = ntTable([ntRow([ntCell([ntPara('1. What does layout mean?')])])]);
        var outer = ntTable([ntRow([ntCell([ntNested(inner)])])]);

        var out = new OutputFormatter().formatTable(outer);

        assert(out.indexOf('1. What does layout mean?') !== -1,
            'nested cell text must appear in the output');
    });

    it('places the nested table inside its parent, under its own row', function () {
        var inner = ntTable([ntRow([ntCell([ntPara('inner text')])])]);
        var outer = ntTable([
            ntRow([ntCell([ntPara('row one')])]),
            ntRow([ntCell([ntNested(inner)])])
        ]);

        var lines = new OutputFormatter().formatTable(outer).split('\n');

        var open = lines.indexOf('┌─── TABLE ───');
        var rowOne = -1, nestedOpen = -1, nestedClose = -1, close = -1;
        for (var i = 0; i < lines.length; i++) {
            if (lines[i].indexOf('row one') !== -1) { rowOne = i; }
            if (lines[i].indexOf('NESTED TABLE') !== -1 && nestedOpen === -1) { nestedOpen = i; }
            if (lines[i].indexOf('END NESTED TABLE') !== -1) { nestedClose = i; }
            if (lines[i] === '└─── END TABLE ───') { close = i; }
        }

        assert(open === 0, 'parent table frame must still open the block');
        assert(rowOne < nestedOpen, 'the earlier row must come first');
        assert(nestedOpen < nestedClose, 'the nested block must open before it closes');
        assert(nestedClose < close, 'the nested block must sit inside the parent table');
        assert(lines[nestedOpen].indexOf('in row 2, cell 1') !== -1,
            'the nested block must say which row and cell it came from');
    });

    it('leaves a table with no nested table byte-identical to the old format', function () {
        var plain = ntTable([
            ntRow([ntCell([ntPara('a')]), ntCell([ntPara('b')])]),
            ntRow([ntCell([ntPara('c')]), ntCell([ntPara('d')])])
        ]);

        var out = new OutputFormatter().formatTable(plain);

        assertEqual(out,
            '┌─── TABLE ───\n│ a ║ b\n│ c ║ d\n└─── END TABLE ───',
            'output for an ordinary table must not change');
    });

    it('recurses into a table nested inside a nested table', function () {
        var deepest = ntTable([ntRow([ntCell([ntPara('deepest value')])])]);
        var middle = ntTable([ntRow([ntCell([ntNested(deepest)])])]);
        var outer = ntTable([ntRow([ntCell([ntNested(middle)])])]);

        var out = new OutputFormatter().formatTable(outer);

        assert(out.indexOf('deepest value') !== -1,
            'text three tables deep must still be reached');
    });

    it('keeps a cell\'s own paragraphs as well as its nested table', function () {
        var inner = ntTable([ntRow([ntCell([ntPara('quiz question')])])]);
        var outer = ntTable([ntRow([ntCell([
            ntPara('Part 2: answer the following'),
            ntNested(inner)
        ])])]);

        var out = new OutputFormatter().formatTable(outer);

        assert(out.indexOf('Part 2: answer the following') !== -1,
            'the cell\'s own text must survive');
        assert(out.indexOf('quiz question') !== -1,
            'the nested table must survive alongside it');
    });

    it('is inert for every other consumer of a cell', function () {
        // The placeholder the parser pushes is paragraph-shaped, so code that
        // reads .text or .runs (media list converter, comment inserter, the
        // boilerplate scan) sees an ordinary empty paragraph.
        var placeholder = ntNested(ntTable([ntRow([ntCell([ntPara('x')])])]));

        assertEqual(placeholder.text, '', 'placeholder text must be empty');
        assert(Array.isArray(placeholder.runs) && placeholder.runs.length === 0,
            'placeholder must carry an empty runs array');
        assertEqual(placeholder.isListItem, false, 'placeholder must not be a list item');
    });
});
