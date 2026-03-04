/**
 * Tests for Block Scoping System (Instruction 1)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

// Helper to create mock paragraph content blocks
function para(text) {
    return { type: 'paragraph', data: { text: text, runs: [{ text: text }] } };
}

function redPara(text) {
    return { type: 'paragraph', data: { text: '\uD83D\uDD34[RED TEXT] ' + text + ' [/RED TEXT]\uD83D\uDD34', runs: [{ text: text }] } };
}

function table(rows) {
    return {
        type: 'table',
        data: {
            rows: rows.map(function(row) {
                return {
                    cells: row.map(function(cell) {
                        return { paragraphs: [{ text: cell, runs: [{ text: cell }] }] };
                    })
                };
            })
        }
    };
}

describe('Block Scoping — Test 1.7.1: Accordion with explicit close', function() {
    it('should create accordion block with 6 tabs and explicit close', function() {
        var blocks = [
            redPara('[Accordion]'),
            redPara('[Tab 1]'),
            para('Tab 1 content'),
            redPara('[Tab 2]'),
            para('Tab 2 content'),
            redPara('[Tab 3]'),
            para('Tab 3 content'),
            redPara('[Tab 4]'),
            para('Tab 4 content'),
            redPara('[Tab 5]'),
            para('Tab 5 content'),
            redPara('[Tab 6]'),
            para('Tab 6 content'),
            redPara('[end of accordion]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var accBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'accordion') {
                accBlock = result[i];
                break;
            }
        }

        assertNotNull(accBlock, 'Accordion block should be found');
        assertEqual(accBlock.blockType, 'accordion');
        assertFalse(accBlock.implicitClose, 'Should not be implicitly closed');
    });
});

describe('Block Scoping — Test 1.7.2: Carousel with explicit close', function() {
    it('should create carousel block with 2 slides', function() {
        var blocks = [
            redPara('[Carousel]'),
            redPara('[Slide 1]'),
            para('Slide 1 content'),
            redPara('[Slide 2]'),
            para('Slide 2 content'),
            redPara('[end carousel]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var carBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'carousel') {
                carBlock = result[i];
                break;
            }
        }

        assertNotNull(carBlock, 'Carousel block should be found');
        assertEqual(carBlock.blockType, 'carousel');
        assertFalse(carBlock.implicitClose, 'Should not be implicitly closed');
    });
});

describe('Block Scoping — Test 1.7.3: Flip cards with explicit close', function() {
    it('should create flipcards block', function() {
        var blocks = [
            redPara('[Flip cards]'),
            redPara('[First card, front H4 title]'),
            para('Front 1'),
            redPara('[First card, back H4 title]'),
            para('Back 1'),
            redPara('[Second card, front H4 title]'),
            para('Front 2'),
            redPara('[Second card, back H4 title]'),
            para('Back 2'),
            redPara('[End of flipcards]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var flipBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'flipcards') {
                flipBlock = result[i];
                break;
            }
        }

        assertNotNull(flipBlock, 'Flipcards block should be found');
        assertEqual(flipBlock.blockType, 'flipcards');
        assertFalse(flipBlock.implicitClose, 'Should not be implicitly closed');
    });
});

describe('Block Scoping — Test 1.7.4: Drag and drop with implicit close at page boundary', function() {
    it('should create dragdrop block closed at [End page]', function() {
        var blocks = [
            redPara('[Drag and drop activity with correct answers]'),
            table([['Category A', 'Category B'], ['Item 1', 'Item 2']]),
            para('Some body text'),
            redPara('[End page]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var ddBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'dragdrop') {
                ddBlock = result[i];
                break;
            }
        }

        assertNotNull(ddBlock, 'Dragdrop block should be found');
        assertTrue(ddBlock.implicitClose, 'Should be implicitly closed');
        assertEqual(ddBlock.implicitCloseReason, 'page_break', 'Should be closed by page break');
    });
});

describe('Block Scoping — Test 1.7.5: Drag and drop implicit close at next activity', function() {
    it('should close dragdrop before next activity', function() {
        var blocks = [
            redPara('[Drag and drop]'),
            table([['A', 'B'], ['C', 'D']]),
            redPara('[Activity 3B]'),
            para('Activity content')
        ];

        var result = scoper.scopeBlocks(blocks);
        var ddBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'dragdrop') {
                ddBlock = result[i];
                break;
            }
        }

        assertNotNull(ddBlock, 'Dragdrop block should be found');
        assertTrue(ddBlock.implicitClose, 'Should be implicitly closed');
        assertEqual(ddBlock.implicitCloseReason, 'next_activity', 'Should be closed by next activity');
    });
});

describe('Block Scoping — Test 1.7.6: Nested blocks (activity containing interactive)', function() {
    it('should create nested structure', function() {
        var blocks = [
            redPara('[Activity 2A]'),
            para('Activity heading'),
            redPara('[Drag and drop]'),
            table([['X', 'Y']]),
            redPara('[End drag and drop]'),
            redPara('[End activity]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var actBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'activity') {
                actBlock = result[i];
                break;
            }
        }

        assertNotNull(actBlock, 'Activity block should be found');
        assertEqual(actBlock.blockType, 'activity');
        assertFalse(actBlock.implicitClose);

        // Check for nested dragdrop
        var hasDragDrop = false;
        for (var j = 0; j < actBlock.children.length; j++) {
            if (actBlock.children[j].blockType === 'dragdrop') {
                hasDragDrop = true;
            }
        }
        assertTrue(hasDragDrop, 'Should have nested dragdrop block');
    });
});

describe('Block Scoping — Test 1.7.7: Mismatched closer spelling', function() {
    it('should match closer despite spelling difference', function() {
        var blocks = [
            redPara('[Flip cards]'),
            para('Content'),
            redPara('[End of flipcards]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var flipBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'flipcards') {
                flipBlock = result[i];
                break;
            }
        }

        assertNotNull(flipBlock, 'Flipcards block should be found');
        assertFalse(flipBlock.implicitClose, 'Should be explicitly closed despite spelling diff');
    });
});

describe('Block Scoping — Test 1.7.8: Generic closer', function() {
    it('should close accordion with [end interactive]', function() {
        var blocks = [
            redPara('[Accordion]'),
            para('Content'),
            redPara('[end interactive]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var accBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'accordion') {
                accBlock = result[i];
                break;
            }
        }

        assertNotNull(accBlock, 'Accordion block should be found');
        assertFalse(accBlock.implicitClose, 'Should be explicitly closed by generic closer');
    });
});

describe('Block Scoping — Test 1.7.9: Boxout with closing tag', function() {
    it('should create alert block for [Box out to the right]', function() {
        var blocks = [
            redPara('[Box out to the right]'),
            para('Box content'),
            redPara('[End of box out to right]')
        ];

        var result = scoper.scopeBlocks(blocks);
        var alertBlock = null;
        for (var i = 0; i < result.length; i++) {
            if (result[i].blockType === 'alert') {
                alertBlock = result[i];
                break;
            }
        }

        assertNotNull(alertBlock, 'Alert block should be found');
        assertFalse(alertBlock.implicitClose);
    });
});

describe('Block Scoping — Test 1.7.10: Lookahead limit', function() {
    it('should auto-close after 200-line lookahead limit', function() {
        var blocks = [redPara('[Carousel]')];
        // Add 250 body paragraphs
        for (var i = 0; i < 250; i++) {
            blocks.push(para('Body text line ' + i));
        }

        var result = scoper.scopeBlocks(blocks);
        var carBlock = null;
        for (var j = 0; j < result.length; j++) {
            if (result[j].blockType === 'carousel') {
                carBlock = result[j];
                break;
            }
        }

        assertNotNull(carBlock, 'Carousel block should be found');
        assertTrue(carBlock.implicitClose, 'Should be implicitly closed');
        assertEqual(carBlock.implicitCloseReason, 'lookahead_limit', 'Reason should be lookahead_limit');

        // Check warning was generated
        assertTrue(scoper.warnings.length > 0, 'Should have generated a warning');
        assert(scoper.warnings[0].indexOf('lookahead') !== -1, 'Warning should mention lookahead');
    });
});
