/**
 * Tests for Tag De-Fragmentation (Phase 1 Patch — Part 1)
 * Tests the defragmentRawText() pre-processing method that stitches
 * fractured red-text boundaries and cleans bracket spacing artifacts.
 */

'use strict';

var normaliser = new TagNormaliser();

// ===================================================================
// De-fragmentation: Redundant red-text boundary stitching
// ===================================================================

describe('Defragmentation — Red-text boundary stitching', function() {
    it('should stitch a fractured tag split across two red-text regions', function() {
        var input = '\uD83D\uDD34[RED TEXT] [lin [/RED TEXT]\uD83D\uDD34\uD83D\uDD34[RED TEXT] k #1] [/RED TEXT]\uD83D\uDD34';
        var result = normaliser.defragmentRawText(input);
        // After stitching, the inner content should form [link #1]
        assert(result.indexOf('[/RED TEXT]') !== -1, 'Should still have outer red markers');
        assert(result.indexOf('[link #1]') !== -1 || result.indexOf('[lin k #1]') !== -1,
            'Should stitch the fractured boundary so inner content is continuous');
    });

    it('should stitch fractured [speech bubble] tag', function() {
        var input = '\uD83D\uDD34[RED TEXT] [speech [/RED TEXT]\uD83D\uDD34\uD83D\uDD34[RED TEXT] bubble] [/RED TEXT]\uD83D\uDD34';
        var result = normaliser.defragmentRawText(input);
        assert(result.indexOf('[speech bubble]') !== -1,
            'Should stitch to form [speech bubble], got: ' + result);
    });

    it('should stitch with whitespace between close/open markers', function() {
        var input = '\uD83D\uDD34[RED TEXT] [H [/RED TEXT]\uD83D\uDD34  \uD83D\uDD34[RED TEXT] 2] [/RED TEXT]\uD83D\uDD34';
        var result = normaliser.defragmentRawText(input);
        assert(result.indexOf('[H2]') !== -1 || result.indexOf('[H 2]') !== -1,
            'Should stitch with intervening whitespace, got: ' + result);
    });

    it('should NOT stitch non-adjacent red text regions', function() {
        var input = '\uD83D\uDD34[RED TEXT] [H2] [/RED TEXT]\uD83D\uDD34 Some body text \uD83D\uDD34[RED TEXT] [H3] [/RED TEXT]\uD83D\uDD34';
        var result = normaliser.defragmentRawText(input);
        assert(result.indexOf('[H2]') !== -1, 'Should preserve [H2]');
        assert(result.indexOf('[H3]') !== -1, 'Should preserve [H3]');
        assert(result.indexOf('Some body text') !== -1, 'Should preserve body text between');
    });

    it('should handle triple-split tag across three red-text regions', function() {
        var input = '\uD83D\uDD34[RED TEXT] [drag [/RED TEXT]\uD83D\uDD34\uD83D\uDD34[RED TEXT] and [/RED TEXT]\uD83D\uDD34\uD83D\uDD34[RED TEXT] drop] [/RED TEXT]\uD83D\uDD34';
        var result = normaliser.defragmentRawText(input);
        assert(result.indexOf('[drag and drop]') !== -1,
            'Should stitch triple-split tag, got: ' + result);
    });

    it('should return unchanged text with no red markers', function() {
        var input = 'Hello world [H2] some text';
        var result = normaliser.defragmentRawText(input);
        assertEqual(result, input);
    });

    it('should return unchanged for null/empty input', function() {
        assertNull(normaliser.defragmentRawText(null));
        assertEqual(normaliser.defragmentRawText(''), '');
    });
});

// ===================================================================
// De-fragmentation: Bracket space collapsing
// ===================================================================

describe('Defragmentation — Bracket space collapsing', function() {
    it('should collapse multiple spaces inside brackets', function() {
        var result = normaliser.defragmentRawText('[interactive   activity]');
        assertEqual(result, '[interactive activity]');
    });

    it('should collapse triple spaces inside brackets', function() {
        var result = normaliser.defragmentRawText('[drag   and   drop]');
        assertEqual(result, '[drag and drop]');
    });

    it('should not affect single-spaced brackets', function() {
        var result = normaliser.defragmentRawText('[drag and drop]');
        assertEqual(result, '[drag and drop]');
    });
});

// ===================================================================
// De-fragmentation: Bracket whitespace trimming
// ===================================================================

describe('Defragmentation — Bracket whitespace trimming', function() {
    it('should trim leading spaces inside brackets', function() {
        var result = normaliser.defragmentRawText('[ tags ]');
        assertEqual(result, '[tags]');
    });

    it('should trim leading/trailing spaces inside brackets', function() {
        var result = normaliser.defragmentRawText('[ H2 ]');
        assertEqual(result, '[H2]');
    });

    it('should trim trailing space only', function() {
        var result = normaliser.defragmentRawText('[body ]');
        assertEqual(result, '[body]');
    });

    it('should trim leading space only', function() {
        var result = normaliser.defragmentRawText('[ body]');
        assertEqual(result, '[body]');
    });

    it('should handle both space collapsing and trimming together', function() {
        var result = normaliser.defragmentRawText('[  drag   and  drop  ]');
        assertEqual(result, '[drag and drop]');
    });
});

// ===================================================================
// De-fragmentation: Integration with processBlock
// ===================================================================

describe('Defragmentation — processBlock integration', function() {
    it('should correctly extract a tag from stitched red-text', function() {
        var input = '\uD83D\uDD34[RED TEXT] [H [/RED TEXT]\uD83D\uDD34\uD83D\uDD34[RED TEXT] 2] [/RED TEXT]\uD83D\uDD34';
        var result = normaliser.processBlock(input);
        assert(result.tags.length > 0, 'Should find tags after stitching');
        assertEqual(result.tags[0].normalised, 'heading');
    });

    it('should correctly extract [activity] from spaced brackets', function() {
        var input = '\uD83D\uDD34[RED TEXT] [ activity ] [/RED TEXT]\uD83D\uDD34';
        var result = normaliser.processBlock(input);
        assert(result.tags.length > 0, 'Should find activity tag');
        assertEqual(result.tags[0].normalised, 'activity');
    });

    it('should correctly extract multi-space tag', function() {
        var input = '\uD83D\uDD34[RED TEXT] [drag   and   drop] [/RED TEXT]\uD83D\uDD34';
        var result = normaliser.processBlock(input);
        assert(result.tags.length > 0, 'Should find tag');
        assertEqual(result.tags[0].normalised, 'drag_and_drop');
    });
});

// ===================================================================
// resolveOrdinalOrNumber: Suffix stripping
// ===================================================================

describe('resolveOrdinalOrNumber — Ordinal suffix stripping', function() {
    it('should resolve "1st" to 1', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('1st'), 1);
    });

    it('should resolve "2nd" to 2', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('2nd'), 2);
    });

    it('should resolve "3rd" to 3', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('3rd'), 3);
    });

    it('should resolve "4th" to 4', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('4th'), 4);
    });

    it('should resolve "10th" to 10', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('10th'), 10);
    });

    it('should still resolve word ordinals', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('first'), 1);
        assertEqual(normaliser.resolveOrdinalOrNumber('Third'), 3);
        assertEqual(normaliser.resolveOrdinalOrNumber('forth'), 4);
    });

    it('should still resolve cardinal words', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('one'), 1);
        assertEqual(normaliser.resolveOrdinalOrNumber('Ten'), 10);
    });

    it('should still resolve plain numbers', function() {
        assertEqual(normaliser.resolveOrdinalOrNumber('5'), 5);
        assertEqual(normaliser.resolveOrdinalOrNumber('12'), 12);
    });

    it('should return null for unrecognised input', function() {
        assertNull(normaliser.resolveOrdinalOrNumber('banana'));
        assertNull(normaliser.resolveOrdinalOrNumber(null));
        assertNull(normaliser.resolveOrdinalOrNumber(''));
    });
});
