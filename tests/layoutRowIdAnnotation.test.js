/**
 * Tests for LayoutTableUnwrapper._layoutRowId annotation.
 *
 * Session H — Inline-Embedded Start Tag + Layout-Row Sibling Capture.
 * Confirms that every block produced from the same source table row shares
 * a non-null `_layoutRowId`, that distinct source rows (and tables) receive
 * distinct IDs, and that the annotation is not applied to blocks that did
 * not originate from a layout-table unwrap.
 */

'use strict';

// -----------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------

function mkRunH(text, isRed) {
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

function mkParaH(parts) {
    var runs = [];
    for (var i = 0; i < parts.length; i++) {
        runs.push(mkRunH(parts[i].text, parts[i].isRed));
    }
    var text = parts.map(function (p) { return p.text; }).join('');
    return { runs: runs, text: text };
}

function mkCellH(paragraphs) {
    return { paragraphs: paragraphs };
}

function mkRowH(cells) {
    return { cells: cells };
}

function mkTableBlockH(rows) {
    return { type: 'table', data: { rows: rows } };
}

// -----------------------------------------------------------------
// Tests
// -----------------------------------------------------------------

describe('Session H — layout-table _layoutRowId annotation', function () {

    it('(a) two-column layout table: both unwrapped siblings share a non-null _layoutRowId', function () {
        var normaliser = new TagNormaliser();
        var unwrapper = new LayoutTableUnwrapper(normaliser);

        var mainCell = mkCellH([
            mkParaH([
                { text: '[Activity 1A]', isRed: true }
            ]),
            mkParaH([
                { text: '[Body]', isRed: true }
            ]),
            mkParaH([{ text: 'Main body content here.' }])
        ]);
        var sidebarCell = mkCellH([
            mkParaH([{ text: '[image]', isRed: true }]),
            mkParaH([{ text: 'https://example.com/image.png' }])
        ]);

        var contentBlocks = [mkTableBlockH([mkRowH([mainCell, sidebarCell])])];
        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Find unwrapped blocks
        var rowIds = {};
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i]._unwrappedFrom === 'layout_table') {
                rowIds[contentBlocks[i]._layoutRowId] = true;
                assertNotNull(contentBlocks[i]._layoutRowId, 'block ' + i + ' should have _layoutRowId');
            }
        }
        var keys = Object.keys(rowIds);
        assertEqual(keys.length, 1, 'both siblings should share exactly one _layoutRowId');
        assertTrue(keys[0].indexOf('lrow-') === 0, 'ID should start with lrow-');
    });

    it('(b) two separate layout tables: siblings from different tables get distinct _layoutRowId values', function () {
        var normaliser = new TagNormaliser();
        var unwrapper = new LayoutTableUnwrapper(normaliser);

        function buildLayoutTable() {
            var mainCell = mkCellH([
                mkParaH([{ text: '[Activity 1A]', isRed: true }]),
                mkParaH([{ text: '[Body]', isRed: true }]),
                mkParaH([{ text: 'Body text.' }])
            ]);
            var sidebarCell = mkCellH([
                mkParaH([{ text: '[image]', isRed: true }]),
                mkParaH([{ text: 'https://example.com/i.png' }])
            ]);
            return mkTableBlockH([mkRowH([mainCell, sidebarCell])]);
        }

        var contentBlocks = [buildLayoutTable(), buildLayoutTable()];
        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        var ids = [];
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i]._unwrappedFrom === 'layout_table') {
                if (ids.indexOf(contentBlocks[i]._layoutRowId) === -1) {
                    ids.push(contentBlocks[i]._layoutRowId);
                }
            }
        }
        assertEqual(ids.length, 2, 'different tables should produce distinct _layoutRowId values');
        assertTrue(ids[0] !== ids[1], 'ids must differ');
    });

    it('(c) single-column table (not a layout table): no _layoutRowId annotation applied', function () {
        var normaliser = new TagNormaliser();
        var unwrapper = new LayoutTableUnwrapper(normaliser);

        // Simple 2-row, 1-column data table — no layout-table signature.
        var tableBlock = mkTableBlockH([
            mkRowH([mkCellH([mkParaH([{ text: 'Header' }])])]),
            mkRowH([mkCellH([mkParaH([{ text: 'Value' }])])])
        ]);
        var contentBlocks = [tableBlock];
        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Table should have been preserved, not unwrapped.
        assertEqual(contentBlocks.length, 1, 'single-column data table should not be unwrapped');
        assertEqual(contentBlocks[0].type, 'table', 'table block preserved');
        assertEqual(contentBlocks[0]._layoutRowId, undefined, 'no _layoutRowId on preserved table');
    });

    it('(d) three-row layout table: each row produces siblings sharing that row\'s _layoutRowId, distinct across rows', function () {
        var normaliser = new TagNormaliser();
        var unwrapper = new LayoutTableUnwrapper(normaliser);

        function mkRowCells(label) {
            var mainCell = mkCellH([
                mkParaH([{ text: '[Activity ' + label + ']', isRed: true }]),
                mkParaH([{ text: '[Body]', isRed: true }]),
                mkParaH([{ text: 'Body ' + label }])
            ]);
            var sidebarCell = mkCellH([
                mkParaH([{ text: '[image]', isRed: true }]),
                mkParaH([{ text: 'https://example.com/' + label + '.png' }])
            ]);
            return mkRowH([mainCell, sidebarCell]);
        }

        var tableBlock = mkTableBlockH([mkRowCells('R1'), mkRowCells('R2'), mkRowCells('R3')]);
        var contentBlocks = [tableBlock];
        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Group unwrapped blocks by their _layoutRowId and check each group
        // contains >1 block.
        var byRow = {};
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i]._unwrappedFrom === 'layout_table') {
                var id = contentBlocks[i]._layoutRowId;
                if (!byRow[id]) byRow[id] = 0;
                byRow[id]++;
            }
        }
        var groupKeys = Object.keys(byRow);
        assertEqual(groupKeys.length, 3, 'three distinct _layoutRowId groups expected');
        for (var k = 0; k < groupKeys.length; k++) {
            assertTrue(byRow[groupKeys[k]] >= 2, 'each group should have >=2 blocks');
        }
    });

    it('(e) _layoutRowId is preserved alongside existing _cellRole (regression)', function () {
        var normaliser = new TagNormaliser();
        var unwrapper = new LayoutTableUnwrapper(normaliser);

        var mainCell = mkCellH([
            mkParaH([{ text: '[Activity 1A]', isRed: true }]),
            mkParaH([{ text: '[Body]', isRed: true }]),
            mkParaH([{ text: 'Main body.' }])
        ]);
        var sidebarCell = mkCellH([
            mkParaH([{ text: '[image]', isRed: true }]),
            mkParaH([{ text: 'https://example.com/i.png' }])
        ]);

        var contentBlocks = [mkTableBlockH([mkRowH([mainCell, sidebarCell])])];
        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        var sawMain = false;
        var sawSidebarImage = false;
        for (var i = 0; i < contentBlocks.length; i++) {
            var b = contentBlocks[i];
            if (b._unwrappedFrom !== 'layout_table') continue;
            assertNotNull(b._cellRole, 'block should still have _cellRole');
            assertNotNull(b._layoutRowId, 'block should also have _layoutRowId');
            if (b._cellRole === 'main_content') sawMain = true;
            if (b._cellRole === 'sidebar_image') sawSidebarImage = true;
        }
        assertTrue(sawMain, 'main_content block seen');
        assertTrue(sawSidebarImage, 'sidebar_image block seen');
    });

    it('(f) non-table blocks interspersed after unwrapping retain no _layoutRowId', function () {
        var normaliser = new TagNormaliser();
        var unwrapper = new LayoutTableUnwrapper(normaliser);

        var standalonePara = {
            type: 'paragraph',
            data: mkParaH([{ text: 'A standalone paragraph not inside any table.' }])
        };

        var mainCell = mkCellH([
            mkParaH([{ text: '[Activity 1A]', isRed: true }]),
            mkParaH([{ text: '[Body]', isRed: true }]),
            mkParaH([{ text: 'Main body.' }])
        ]);
        var sidebarCell = mkCellH([
            mkParaH([{ text: '[image]', isRed: true }]),
            mkParaH([{ text: 'https://example.com/i.png' }])
        ]);
        var tableBlock = mkTableBlockH([mkRowH([mainCell, sidebarCell])]);

        var contentBlocks = [standalonePara, tableBlock];
        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // The standalone paragraph is still at index 0 — it must not have
        // received a _layoutRowId since it was not produced by _unwrapTable.
        assertEqual(contentBlocks[0], standalonePara, 'standalone paragraph preserved in-place');
        assertEqual(contentBlocks[0]._layoutRowId, undefined, 'standalone paragraph has no _layoutRowId');
        assertEqual(contentBlocks[0]._unwrappedFrom, undefined, 'standalone paragraph not marked as unwrapped');
    });

});
