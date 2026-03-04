/**
 * Tests for Layout Direction Extraction (Instruction 4)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

describe('Layout Direction — Test 4.5.1: Image embedded left', function() {
    it('should extract image position left', function() {
        var result = scoper.extractLayoutDirection('image embedded to the left with text to the right');
        assertNotNull(result);
        assertEqual(result.coreType, 'image');
        assertEqual(result.position, 'left');
    });
});

describe('Layout Direction — Test 4.5.2: Image right', function() {
    it('should extract image position right', function() {
        var result = scoper.extractLayoutDirection('image right');
        assertNotNull(result);
        assertEqual(result.coreType, 'image');
        assertEqual(result.position, 'right');
    });
});

describe('Layout Direction — Test 4.5.3: Body left', function() {
    it('should extract body position left', function() {
        var result = scoper.extractLayoutDirection('Body left');
        assertNotNull(result);
        assertEqual(result.coreType, 'body');
        assertEqual(result.position, 'left');
    });
});

describe('Layout Direction — Test 4.5.4: Body right', function() {
    it('should extract body position right', function() {
        var result = scoper.extractLayoutDirection('Body right');
        assertNotNull(result);
        assertEqual(result.coreType, 'body');
        assertEqual(result.position, 'right');
    });
});

describe('Layout Direction — Test 4.5.5: Body bold', function() {
    it('should extract body with bold style', function() {
        var result = scoper.extractLayoutDirection('Body, bold');
        assertNotNull(result);
        assertEqual(result.coreType, 'body');
        assertEqual(result.style, 'bold');
    });
});

describe('Layout Direction — Test 4.5.6: Layout pair detection', function() {
    it('should detect image right + body left as layout pair', function() {
        var blocks = [
            { layoutInfo: { coreType: 'image', position: 'right', description: null, style: null } },
            { layoutInfo: { coreType: 'body', position: 'left', description: null, style: null } }
        ];
        var result = scoper.detectLayoutPairs(blocks);
        assertEqual(result.length, 1);
        assertEqual(result[0].type, 'layout_pair');
        assertEqual(result[0].columns.length, 2);
        assertEqual(result[0].columns[0].contentType, 'image');
        assertEqual(result[0].columns[1].contentType, 'body');
    });
});

describe('Layout Direction — Image embedded right', function() {
    it('should extract image position right from long form', function() {
        var result = scoper.extractLayoutDirection('image embedded to the right with text to the left');
        assertNotNull(result);
        assertEqual(result.coreType, 'image');
        assertEqual(result.position, 'right');
    });
});

describe('Layout Direction — Body bullet points', function() {
    it('should extract body with bullet style', function() {
        var result = scoper.extractLayoutDirection('Body, bullet points');
        assertNotNull(result);
        assertEqual(result.coreType, 'body');
        assertEqual(result.style, 'bullet');
    });
});

describe('Layout Direction — Flip card image', function() {
    it('should recognise flip card image tag', function() {
        var result = scoper.extractLayoutDirection('Flip card image');
        assertNotNull(result);
        assertEqual(result.coreType, 'image');
        assertEqual(result.style, 'flip_card');
    });
});
