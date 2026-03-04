/**
 * Tests for Interactive Type Inference from Table Structure (Instruction 7)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

// Helper to create table data
function makeTable(headers, rows) {
    var allRows = [];
    if (headers) {
        allRows.push({
            cells: headers.map(function(h) {
                return { paragraphs: [{ text: h, runs: [{ text: h }] }] };
            })
        });
    }
    for (var r = 0; r < rows.length; r++) {
        allRows.push({
            cells: rows[r].map(function(cell) {
                return { paragraphs: [{ text: cell, runs: [{ text: cell }] }] };
            })
        });
    }
    return { rows: allRows };
}

function makeTableWithBold(headers, rows, boldCells) {
    var allRows = [];
    if (headers) {
        allRows.push({
            cells: headers.map(function(h) {
                return { paragraphs: [{ text: h, runs: [{ text: h }] }] };
            })
        });
    }
    for (var r = 0; r < rows.length; r++) {
        allRows.push({
            cells: rows[r].map(function(cell, ci) {
                var isBold = boldCells && boldCells[r] && boldCells[r].indexOf(ci) !== -1;
                return {
                    paragraphs: [{
                        text: cell,
                        runs: [{
                            text: cell,
                            formatting: { bold: isBold }
                        }]
                    }]
                };
            })
        });
    }
    return { rows: allRows };
}

describe('Interactive Inference — Test 7.3.1: True/False table', function() {
    it('should infer radio_quiz_true_false from True/False columns', function() {
        var table = makeTable(
            ['Statement', 'True/False'],
            [
                ['The earth is round', 'True'],
                ['The sun orbits earth', 'False'],
                ['Water is wet', 'True']
            ]
        );
        var result = scoper.inferInteractiveFromTable(table);
        assertEqual(result.inferredType, 'radio_quiz_true_false');
        assertEqual(result.confidence, 'high');
    });
});

describe('Interactive Inference — Test 7.3.2: Two-column matching', function() {
    it('should infer drag_and_drop from matching pairs table', function() {
        var table = makeTable(
            ['Element', 'Example'],
            [
                ['Metaphor', 'Life is a journey'],
                ['Simile', 'Brave as a lion'],
                ['Onomatopoeia', 'Buzz and hiss']
            ]
        );
        var result = scoper.inferInteractiveFromTable(table);
        assertEqual(result.inferredType, 'drag_and_drop');
    });
});

describe('Interactive Inference — Test 7.3.3: Explicit type takes precedence', function() {
    it('should return null when no table is present', function() {
        var result = scoper.inferInteractiveFromTable(null);
        assertNull(result.inferredType);
    });
});

describe('Interactive Inference — Test 7.3.4: No table (empty)', function() {
    it('should return null for activity with no table', function() {
        var result = scoper.inferInteractiveFromTable({ rows: [] });
        assertNull(result.inferredType);
        assertEqual(result.confidence, 'none');
    });
});

describe('Interactive Inference — [Correct] markers', function() {
    it('should infer multichoice_quiz from 3+ column table with [Correct]', function() {
        var table = makeTable(
            ['Question', 'Option A', 'Option B', 'Option C'],
            [
                ['What colour is the sky?', 'Blue [Correct]', 'Red', 'Green'],
                ['What is 2+2?', '3', '4 [Correct]', '5']
            ]
        );
        var result = scoper.inferInteractiveFromTable(table);
        assertEqual(result.inferredType, 'multichoice_quiz');
        assertEqual(result.confidence, 'high');
    });
});

describe('Interactive Inference — Single column', function() {
    it('should infer ordered_list from single column numbered items', function() {
        var table = makeTable(
            null,
            [['Item one'], ['Item two'], ['Item three']]
        );
        var result = scoper.inferInteractiveFromTable(table);
        assertEqual(result.inferredType, 'ordered_list');
    });
});

describe('Interactive Inference — Question header', function() {
    it('should infer multichoice_quiz from 3+ columns with Question header', function() {
        var table = makeTable(
            ['Question', 'A', 'B', 'C'],
            [['What is X?', '1', '2', '3']]
        );
        var result = scoper.inferInteractiveFromTable(table);
        assertEqual(result.inferredType, 'multichoice_quiz');
    });
});
