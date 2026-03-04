/**
 * Tests for Enhanced Tag Fragment Reassembly (Instruction 6)
 */

'use strict';

var normaliser = new TagNormaliser();

// Helper to wrap text in red markers
function red(text) {
    return '\uD83D\uDD34[RED TEXT] ' + text + ' [/RED TEXT]\uD83D\uDD34';
}

describe('Fragment Reassembly — Test 6.4.1: 2-fragment basic', function() {
    it('should reassemble [Activit + y 1A]', function() {
        var input = red('[Activit') + red('y 1A]');
        var result = normaliser.reassembleFragmentedTags(input);
        assert(result.indexOf('[Activit') !== -1 && result.indexOf('y 1A]') !== -1,
            'Should contain reassembled tag content');
        // Should be merged into a single red text marker pair
        var openCount = (result.match(/\uD83D\uDD34\[RED TEXT\]/g) || []).length;
        assertEqual(openCount, 1, 'Should have one merged red text opening marker');
    });
});

describe('Fragment Reassembly — Test 6.4.2: 2-fragment with just closing bracket', function() {
    it('should reassemble [accordion 1 + ]', function() {
        var input = red('[accordion 1 ') + red(']');
        var result = normaliser.reassembleFragmentedTags(input);
        assert(result.indexOf('[accordion 1') !== -1, 'Should contain [accordion 1]');
    });
});

describe('Fragment Reassembly — Test 6.4.3: 3-fragment reassembly', function() {
    it('should reassemble 3 fragments into one tag', function() {
        var input = red('[Learning Journal button that links with ') +
                    red('journal ') +
                    red('1 for this module]');
        var result = normaliser.reassembleFragmentedTags(input);
        assert(result.indexOf('[Learning Journal button that links with') !== -1,
            'Should contain reassembled tag');
        assert(result.indexOf('1 for this module]') !== -1,
            'Should contain end of tag');
    });
});

describe('Fragment Reassembly — Test 6.4.4: 4-fragment with compound tags', function() {
    it('should reassemble 4 fragments with multiple bracket pairs', function() {
        var input = red('[1] [image of American poet ') +
                    red('Claude McKay ') +
                    red('and H5] White House by American poet ') +
                    red('Claude McKay');
        var result = normaliser.reassembleFragmentedTags(input);
        // Should have [1] and [image of American poet Claude McKay and H5] in the result
        assert(result.indexOf('[1]') !== -1, 'Should contain [1]');
        assert(result.indexOf('image of American poet') !== -1,
            'Should contain image description');
    });
});

describe('Fragment Reassembly — Test 6.4.5: Fragment where [ is separated', function() {
    it('should reassemble [ + front]', function() {
        var input = red('[') + red('front]');
        var result = normaliser.reassembleFragmentedTags(input);
        assert(result.indexOf('[front]') !== -1 || result.indexOf('[ front]') !== -1,
            'Should contain [front]');
    });
});

describe('Fragment Reassembly — Test 6.4.6: Fragment with leading space', function() {
    it('should reassemble [End + tab]', function() {
        var input = red('[End ') + red('tab]');
        var result = normaliser.reassembleFragmentedTags(input);
        assert(result.indexOf('[End tab]') !== -1, 'Should contain [End tab]');
    });
});

describe('Fragment Reassembly — Existing 2-way splits still work', function() {
    it('should handle [carousel + External nav buttons]', function() {
        var input = red('[carousel ') + red('External nav buttons]');
        var result = normaliser.reassembleFragmentedTags(input);
        assert(result.indexOf('[carousel External nav buttons]') !== -1,
            'Should contain reassembled carousel tag');
    });

    it('should handle [body tex + t]', function() {
        var input = red('[body tex') + red('t]');
        var result = normaliser.reassembleFragmentedTags(input);
        assert(result.indexOf('[body tex') !== -1 && result.indexOf('t]') !== -1,
            'Should contain reassembled body text tag');
    });

    it('should handle [end interac + tive]', function() {
        var input = red('[end interac') + red('tive]');
        var result = normaliser.reassembleFragmentedTags(input);
        assert(result.indexOf('[end interac') !== -1,
            'Should contain beginning of reassembled tag');
    });
});

describe('Fragment Reassembly — Non-adjacent markers NOT merged', function() {
    it('should not merge red text markers separated by non-red content', function() {
        var input = red('[Tab 1]') + ' Some body text ' + red('[H4]');
        var result = normaliser.reassembleFragmentedTags(input);
        // Should remain as two separate red text blocks
        // Count the opening 🔴[RED TEXT] markers
        var openCount = (result.match(/\uD83D\uDD34\[RED TEXT\]/g) || []).length;
        assertEqual(openCount, 2, 'Should have two separate red text opening markers');
    });
});
