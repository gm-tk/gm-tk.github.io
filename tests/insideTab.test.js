/**
 * Tests for [Inside tab] Marker Handling (Instruction 10)
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

describe('[Inside tab] — Test 10.3.1: Content grouped under tab 1', function() {
    it('should NOT create a new tab for [Inside tab]', function() {
        var blocks = [
            redPara('[Accordion]'),
            redPara('[First tab of accordion]'),
            para('Heading text'),
            redPara('[Inside tab]'),
            para('Body text inside tab'),
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
        // Should NOT have 2 tabs — [Inside tab] should not create a new one
        var tabCount = 0;
        for (var j = 0; j < accBlock.children.length; j++) {
            if (accBlock.children[j].subType === 'tab') {
                tabCount++;
            }
        }
        assertEqual(tabCount, 1, 'Should have only 1 tab (Inside tab is a no-op)');
    });
});

describe('[Inside tab] — Recognition as marker', function() {
    it('should return isMarkerOnly for [Inside tab]', function() {
        var result = scoper.normaliseSubTag('[Inside tab]', 'accordion', 1);
        assertNotNull(result);
        assertTrue(result.isMarkerOnly, 'Should be a marker-only tag');
        assertEqual(result.subType, 'inside_tab');
    });
});
