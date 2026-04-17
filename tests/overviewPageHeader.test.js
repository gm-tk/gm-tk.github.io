/**
 * Session A — overview-page header calibration tests.
 *
 * Covers Change 1: dual <h1> emission in _generateHeader + pipe separator.
 */

function _oh_mkEngine() {
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;
    return engine;
}

function _oh_mkPageData(overrides) {
    var defaults = {
        type: 'overview',
        lessonNumber: null,
        filename: 'OSAI401-00.html',
        moduleCode: 'OSAI401',
        englishTitle: 'Smart Homes',
        tereoTitle: null,
        lessonTitle: null,
        totalPages: 4,
        pageIndex: 0
    };
    var result = {};
    var keys = Object.keys(defaults);
    for (var i = 0; i < keys.length; i++) {
        result[keys[i]] = overrides && overrides.hasOwnProperty(keys[i])
            ? overrides[keys[i]]
            : defaults[keys[i]];
    }
    if (overrides) {
        var extraKeys = Object.keys(overrides);
        for (var j = 0; j < extraKeys.length; j++) {
            if (!result.hasOwnProperty(extraKeys[j])) {
                result[extraKeys[j]] = overrides[extraKeys[j]];
            }
        }
    }
    return result;
}

function _oh_countH1Spans(html) {
    var matches = html.match(/<h1><span>[^<]*<\/span><\/h1>/g);
    return matches ? matches.length : 0;
}

describe('Session A — overview header dual H1', function () {
    var engine = _oh_mkEngine();

    it('9-10 overview emits two <h1><span>...</span></h1> when both titles provided', function () {
        var config = engine.getConfig('9-10');
        var skeleton = engine.generateSkeleton(config, _oh_mkPageData({
            englishTitle: 'Smart Homes',
            tereoTitle: 'Ngā Kāinga Atamai'
        }));
        assertEqual(_oh_countH1Spans(skeleton), 2, 'Expected 2 H1 span headings');
        assert(skeleton.indexOf('<h1><span>Smart Homes</span></h1>') !== -1, 'English H1 present');
        assert(skeleton.indexOf('<h1><span>Ngā Kāinga Atamai</span></h1>') !== -1, 'Tereo H1 present');
    });

    it('9-10 overview default order is English first, Tereo second', function () {
        var config = engine.getConfig('9-10');
        var skeleton = engine.generateSkeleton(config, _oh_mkPageData({
            englishTitle: 'Smart Homes',
            tereoTitle: 'Ngā Kāinga Atamai'
        }));
        var engIdx = skeleton.indexOf('<h1><span>Smart Homes</span></h1>');
        var reoIdx = skeleton.indexOf('<h1><span>Ngā Kāinga Atamai</span></h1>');
        assert(engIdx !== -1 && reoIdx !== -1, 'Both H1s present');
        assert(engIdx < reoIdx, 'English H1 should precede Tereo H1 by default');
    });

    it('titleOrder "tereo-first" reverses order on overview page', function () {
        var config = engine.getConfig('9-10');
        var skeleton = engine.generateSkeleton(config, _oh_mkPageData({
            englishTitle: 'Smart Homes',
            tereoTitle: 'Ngā Kāinga Atamai',
            titleOrder: 'tereo-first'
        }));
        var engIdx = skeleton.indexOf('<h1><span>Smart Homes</span></h1>');
        var reoIdx = skeleton.indexOf('<h1><span>Ngā Kāinga Atamai</span></h1>');
        assert(engIdx !== -1 && reoIdx !== -1, 'Both H1s present');
        assert(reoIdx < engIdx, 'Tereo H1 should precede English H1 when titleOrder=tereo-first');
    });

    it('single H1 fallback: 1-3 overview emits exactly one <h1><span>...</span></h1>', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _oh_mkPageData({
            moduleCode: 'OSAI101',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null
        }));
        assertEqual(_oh_countH1Spans(skeleton), 1, 'Expected 1 H1 span heading');
        assert(skeleton.indexOf('<h1><span>AI Digital Citizenship</span></h1>') !== -1,
            'English H1 present');
    });

    it('single H1 preserved on 1-3 even when tereoTitle provided (titles array = [english])', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _oh_mkPageData({
            moduleCode: 'OSAI101',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: 'Hinengaro Miihini'
        }));
        assertEqual(_oh_countH1Spans(skeleton), 1,
            '1-3 titles array is ["english"] — tereo H1 suppressed');
    });

    it('pipe separator splits English/Tereo title when double-space not present', function () {
        // Replicates the app.js regex /  +| \| / to assert pipe behaviour.
        var re = /  +| \| /;
        var parts = 'Smart Homes | Ngā Kāinga Atamai'.split(re);
        assertEqual(parts.length, 2, 'Should split on space-pipe-space');
        assertEqual(parts[0].trim(), 'Smart Homes', 'English half');
        assertEqual(parts[1].trim(), 'Ngā Kāinga Atamai', 'Tereo half');
    });

    it('pipe-separated title flows through _generateHeader to produce dual H1 on 9-10', function () {
        // When the caller passes a pipe-separated englishTitle and no tereoTitle,
        // the template engine's internal split must populate the second H1.
        var config = engine.getConfig('9-10');
        var skeleton = engine.generateSkeleton(config, _oh_mkPageData({
            englishTitle: 'Smart Homes | Ngā Kāinga Atamai',
            tereoTitle: null
        }));
        assertEqual(_oh_countH1Spans(skeleton), 2, 'Expected 2 H1 spans from pipe-split title');
        assert(skeleton.indexOf('<h1><span>Smart Homes</span></h1>') !== -1, 'English H1 present');
        assert(skeleton.indexOf('<h1><span>Ngā Kāinga Atamai</span></h1>') !== -1, 'Tereo H1 present');
    });
});
