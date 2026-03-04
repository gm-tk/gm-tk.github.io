/**
 * Tests for Video Tag Normalization Enhancement (Instruction 8)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

describe('Video Normalization — Test 8.4.1: [embed video]', function() {
    it('should normalise to video', function() {
        var result = normaliser.normaliseTag('[embed video]');
        assertNotNull(result);
        assertEqual(result.normalised, 'video');
        assertEqual(result.category, 'media');
    });
});

describe('Video Normalization — Test 8.4.2: [imbed video] misspelling', function() {
    it('should normalise misspelled imbed to video', function() {
        var result = normaliser.normaliseTag('[imbed video]');
        assertNotNull(result);
        assertEqual(result.normalised, 'video');
    });
});

describe('Video Normalization — Test 8.4.3: Video with start time', function() {
    it('should extract start time from instruction text', function() {
        var result = scoper.extractVideoTiming('edit to start at 0:14 seconds');
        assertNotNull(result.startTime);
        assertEqual(result.startTime, '0:14');
    });
});

describe('Video Normalization — Test 8.4.4: Video with start and end time', function() {
    it('should extract both start and end time', function() {
        var result = scoper.extractVideoTiming(
            'edit to start playing at :53 minutes. Edit to finish playing at 2:09 minutes'
        );
        assertNotNull(result.startTime);
        assertNotNull(result.endTime);
        assertEqual(result.startTime, '0:53');
        assertEqual(result.endTime, '2:09');
    });
});

describe('Video Normalization — Test 8.4.5: Start and finish with "and"', function() {
    it('should extract start and end from combined instruction', function() {
        var result = scoper.extractVideoTiming(
            'edit to start at :58 seconds and finish at 1:48 minutes'
        );
        assertNotNull(result.startTime);
        assertNotNull(result.endTime);
        assertEqual(result.startTime, '0:58');
        assertEqual(result.endTime, '1:48');
    });
});

describe('Video Normalization — Test 8.4.6: Interactive: Video with title', function() {
    it('should normalise [Interactive: Video: Sustainable Development Goals]', function() {
        var result = normaliser.normaliseTag('[Interactive: Video: Sustainable Development Goals]');
        assertNotNull(result);
        assertEqual(result.normalised, 'video');
        // Title captured as modifier
        assertNotNull(result.modifier, 'Should have modifier/title');
    });
});

describe('Video Normalization — [Insert video]', function() {
    it('should normalise [Insert video] to video', function() {
        var result = normaliser.normaliseTag('[Insert video]');
        assertNotNull(result);
        assertEqual(result.normalised, 'video');
    });
});

describe('Video Normalization — [embed film]', function() {
    it('should normalise [embed film] to video', function() {
        var result = normaliser.normaliseTag('[embed film]');
        assertNotNull(result);
        assertEqual(result.normalised, 'video');
    });
});

describe('Video Normalization — [imbed film]', function() {
    it('should normalise [imbed film] to video', function() {
        var result = normaliser.normaliseTag('[imbed film]');
        assertNotNull(result);
        assertEqual(result.normalised, 'video');
    });
});

describe('Video Normalization — Video normalise method', function() {
    it('should detect [embed video] as video type', function() {
        var result = scoper.normaliseVideoTag('embed video');
        assertNotNull(result);
        assertEqual(result.type, 'video');
    });

    it('should detect [imbed video] as video type', function() {
        var result = scoper.normaliseVideoTag('imbed video');
        assertNotNull(result);
        assertEqual(result.type, 'video');
    });

    it('should detect [Interactive: Video: Title] with title', function() {
        var result = scoper.normaliseVideoTag('Interactive: Video: Sustainable Development Goals');
        assertNotNull(result);
        assertEqual(result.type, 'video');
        assertEqual(result.title, 'Sustainable Development Goals');
    });

    it('should return null for non-video tags', function() {
        var result = scoper.normaliseVideoTag('image');
        assertNull(result);
    });
});
