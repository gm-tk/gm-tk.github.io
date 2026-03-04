/**
 * Tests for Compound Tag Splitting (Instruction 3)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

describe('Compound Tag Splitting — Test 3.3.1: Multiple brackets', function() {
    it('should split [Body] [LESSON] 6 into 2 tags', function() {
        var result = scoper.splitCompoundTags('[Body] [LESSON] 6');
        assert(result.length >= 2, 'Should produce at least 2 results');
        assertEqual(result[0].inner, 'Body');
        assertEqual(result[1].inner, 'LESSON');
    });
});

describe('Compound Tag Splitting — Test 3.3.2: Tag + heading level', function() {
    it('should split [Tab 1] [H4] into tab + heading', function() {
        var result = scoper.splitCompoundTags('[Tab 1] [H4]');
        assertEqual(result.length, 2);
        assertEqual(result[0].inner, 'Tab 1');
        assertEqual(result[1].inner, 'H4');
    });
});

describe('Compound Tag Splitting — Test 3.3.3: "image of X and HN"', function() {
    it('should split [image of Elizabeth Barrett Browning and H5]', function() {
        var result = scoper.splitCompoundTags('[image of Elizabeth Barrett Browning and H5]');
        assertEqual(result.length, 1);
        assertEqual(result[0].imageDescription, 'Elizabeth Barrett Browning');
        assertEqual(result[0].headingLevel, 'H5');
    });
});

describe('Compound Tag Splitting — Test 3.3.4: No-space brackets', function() {
    it('should split [Front][H3] into front + H3', function() {
        var result = scoper.splitCompoundTags('[Front][H3]');
        assertEqual(result.length, 2);
        assertEqual(result[0].inner, 'Front');
        assertEqual(result[1].inner, 'H3');
    });
});

describe('Compound Tag Splitting — Test 3.3.5: Triple brackets', function() {
    it('should split [Card 1] [Front] [H3] into 3 parts', function() {
        var result = scoper.splitCompoundTags('[Card 1] [Front] [H3]');
        assertEqual(result.length, 3);
        assertEqual(result[0].inner, 'Card 1');
        assertEqual(result[1].inner, 'Front');
        assertEqual(result[2].inner, 'H3');
    });
});

describe('Compound Tag Splitting — Test 3.3.6: Bracket + trailing text', function() {
    it('should capture trailing text after last bracket', function() {
        var result = scoper.splitCompoundTags('[1] [image of American poet Claude McKay and H5] White House by American poet Claude McKay');
        assert(result.length >= 2, 'Should have at least 2 tags');
        assertEqual(result[0].inner, '1');
        // Last entry should have trailing text
        var last = result[result.length - 1];
        assertNotNull(last.trailingText, 'Should have trailing text');
        assert(last.trailingText.indexOf('White House') !== -1, 'Trailing should contain White House');
    });
});

describe('Compound Tag Splitting — Single tag with trailing text', function() {
    it('should handle single tag with trailing text', function() {
        var result = scoper.splitCompoundTags('[Accordion] x4 DEV override');
        assertEqual(result.length, 1);
        assertEqual(result[0].inner, 'Accordion');
        assertEqual(result[0].trailingText, 'x4 DEV override');
    });
});

describe('Compound Tag Splitting — Activity + heading', function() {
    it('should split [Activity 1A] [heading] into 2 tags', function() {
        var result = scoper.splitCompoundTags('[Activity 1A] [heading]');
        assertEqual(result.length, 2);
        assertEqual(result[0].inner, 'Activity 1A');
        assertEqual(result[1].inner, 'heading');
    });

    it('should split [Multichoice quiz] [body] into 2 tags', function() {
        var result = scoper.splitCompoundTags('[Multichoice quiz] [body]');
        assertEqual(result.length, 2);
        assertEqual(result[0].inner, 'Multichoice quiz');
        assertEqual(result[1].inner, 'body');
    });
});
