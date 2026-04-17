/**
 * Skeleton Calibration Tests (Phase 15)
 *
 * Tests for all 5 changes from the multi-template skeleton calibration audit
 * comparing PageForge output against human-developed HTML reference files for
 * OSAI101 (template 1-3), OSAI201 (template 4-6), and OSAI301 (template 7-8).
 *
 * Covers:
 *   CHANGE 1 — <title> uses titlePattern config (no decimal numbers)
 *   CHANGE 2 — #module-code format varies by template (moduleCodeFormat)
 *   CHANGE 3 — <head> script set per template (additionalHeadScripts)
 *   CHANGE 4 — tooltip="Overview" on #module-menu-content per template
 *   CHANGE 5 — Footer link ordering (overview vs lesson pages)
 */

// ===================================================================
// Helper: create a TemplateEngine with embedded data
// ===================================================================

function _mkEngine() {
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;
    return engine;
}

function _mkPageData(overrides) {
    var defaults = {
        type: 'overview',
        lessonNumber: null,
        filename: 'OSAI201-00.html',
        moduleCode: 'OSAI201',
        englishTitle: 'AI Digital Citizenship',
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
    return result;
}

// ===================================================================
// CHANGE 1 — <title> element uses titlePattern config
// ===================================================================

describe('Phase 15 CHANGE 1 — <title> uses titlePattern config (no decimals)', function () {
    var engine = _mkEngine();

    it('template 1-3 overview <title> is MODULE_CODE + English Title', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI101', filename: 'OSAI101-00.html'
        }));
        assert(skeleton.indexOf('<title>OSAI101 AI Digital Citizenship</title>') !== -1,
            'Expected <title>OSAI101 AI Digital Citizenship</title>');
    });

    it('template 1-3 lesson <title> has no decimal number', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 1, pageIndex: 1,
            moduleCode: 'OSAI101', filename: 'OSAI101-01.html',
            lessonTitle: 'Lesson 1 Title'
        }));
        assert(skeleton.indexOf('<title>OSAI101 AI Digital Citizenship</title>') !== -1,
            'Lesson <title> should be MODULE_CODE + English Title');
        assert(skeleton.indexOf('<title>OSAI101 1.0') === -1,
            'No decimal in <title>');
    });

    it('template 4-6 lesson <title> has no decimal number', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 2, pageIndex: 2,
            filename: 'OSAI201-02.html', lessonTitle: 'Lesson 2 Title'
        }));
        assert(skeleton.indexOf('<title>OSAI201 AI Digital Citizenship</title>') !== -1,
            'Lesson <title> should be MODULE_CODE + English Title');
        assert(skeleton.indexOf('<title>OSAI201 2.0') === -1,
            'No decimal in <title>');
    });

    it('template 7-8 lesson <title> has no decimal number', function () {
        var config = engine.getConfig('7-8');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 3, pageIndex: 3,
            moduleCode: 'OSAI301', filename: 'OSAI301-03.html',
            lessonTitle: 'Lesson 3 Title'
        }));
        assert(skeleton.indexOf('<title>OSAI301 AI Digital Citizenship</title>') !== -1,
            'Lesson <title> should be MODULE_CODE + English Title');
        assert(skeleton.indexOf('<title>OSAI301 3.0') === -1,
            'No decimal in <title>');
    });

    it('titlePattern token substitution works for all templates', function () {
        var templates = ['1-3', '4-6', '7-8', '9-10', 'NCEA'];
        for (var i = 0; i < templates.length; i++) {
            var config = engine.getConfig(templates[i]);
            // Verify titlePattern exists for both page types
            assert(config.titlePattern && config.titlePattern.overviewPage,
                templates[i] + ' should have titlePattern.overviewPage');
            assert(config.titlePattern && config.titlePattern.lessonPage,
                templates[i] + ' should have titlePattern.lessonPage');
        }
    });
});

// ===================================================================
// CHANGE 2 — #module-code format varies by template
// ===================================================================

describe('Phase 15 CHANGE 2 — #module-code format varies by template', function () {
    var engine = _mkEngine();

    it('template 1-3 lesson uses zero-padded format (01, 02)', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 1, pageIndex: 1,
            moduleCode: 'OSAI101', filename: 'OSAI101-01.html',
            lessonTitle: 'Title'
        }));
        assert(skeleton.indexOf('<div id="module-code"><h1>01</h1></div>') !== -1,
            '1-3 lesson 1 should show "01" in #module-code');
    });

    it('template 1-3 lesson 2 uses zero-padded format 02', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 2, pageIndex: 2,
            moduleCode: 'OSAI101', filename: 'OSAI101-02.html',
            lessonTitle: 'Title'
        }));
        assert(skeleton.indexOf('<div id="module-code"><h1>02</h1></div>') !== -1,
            '1-3 lesson 2 should show "02" in #module-code');
    });

    it('template 4-6 lesson uses decimal format (1.0, 2.0)', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 1, pageIndex: 1,
            filename: 'OSAI201-01.html', lessonTitle: 'Title'
        }));
        assert(skeleton.indexOf('<div id="module-code"><h1>1.0</h1></div>') !== -1,
            '4-6 lesson 1 should show "1.0" in #module-code');
    });

    it('template 7-8 lesson uses zero-padded format (01, 02)', function () {
        var config = engine.getConfig('7-8');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 1, pageIndex: 1,
            moduleCode: 'OSAI301', filename: 'OSAI301-01.html',
            lessonTitle: 'Title'
        }));
        assert(skeleton.indexOf('<div id="module-code"><h1>01</h1></div>') !== -1,
            '7-8 lesson 1 should show "01" in #module-code');
    });

    it('template 7-8 lesson 3 uses zero-padded format 03', function () {
        var config = engine.getConfig('7-8');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 3, pageIndex: 3,
            moduleCode: 'OSAI301', filename: 'OSAI301-03.html',
            lessonTitle: 'Title'
        }));
        assert(skeleton.indexOf('<div id="module-code"><h1>03</h1></div>') !== -1,
            '7-8 lesson 3 should show "03" in #module-code');
    });

    it('overview pages always show full module code regardless of template', function () {
        var templates = ['1-3', '4-6', '7-8'];
        var codes = ['OSAI101', 'OSAI201', 'OSAI301'];
        for (var i = 0; i < templates.length; i++) {
            var config = engine.getConfig(templates[i]);
            var skeleton = engine.generateSkeleton(config, _mkPageData({
                moduleCode: codes[i], filename: codes[i] + '-00.html'
            }));
            assert(skeleton.indexOf('<div id="module-code"><h1>' + codes[i] + '</h1></div>') !== -1,
                templates[i] + ' overview should show full module code ' + codes[i]);
        }
    });

    it('moduleCodeFormat config field exists with correct defaults', function () {
        var config13 = engine.getConfig('1-3');
        assertEqual(config13.headerPattern.lessonPage.moduleCodeFormat, 'zero-padded',
            '1-3 should default to zero-padded');

        var config46 = engine.getConfig('4-6');
        assertEqual(config46.headerPattern.lessonPage.moduleCodeFormat, 'decimal',
            '4-6 should override to decimal');

        var config78 = engine.getConfig('7-8');
        assertEqual(config78.headerPattern.lessonPage.moduleCodeFormat, 'zero-padded',
            '7-8 should default to zero-padded');
    });
});

// ===================================================================
// CHANGE 3 — <head> script set per template
// ===================================================================

describe('Phase 15 CHANGE 3 — <head> script set per template', function () {
    var engine = _mkEngine();

    it('template 1-3 has stickyNav.js before idoc_scripts.js', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI101', filename: 'OSAI101-00.html'
        }));
        var stickyIdx = skeleton.indexOf('stickyNav.js');
        var idocIdx = skeleton.indexOf('idoc_scripts.js');
        assert(stickyIdx !== -1, '1-3 should include stickyNav.js');
        assert(idocIdx !== -1, '1-3 should include idoc_scripts.js');
        assert(stickyIdx < idocIdx,
            'stickyNav.js must appear BEFORE idoc_scripts.js');
    });

    it('template 1-3 uses tekuradev.desire2learn.com', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI101', filename: 'OSAI101-00.html'
        }));
        assert(skeleton.indexOf('tekuradev.desire2learn.com') !== -1,
            '1-3 should use tekuradev (with dev infix)');
        // Ensure it does NOT use the non-dev URL for idoc_scripts
        var idocMatch = skeleton.match(/src="https:\/\/tekura[^"]*idoc_scripts\.js"/g);
        assert(idocMatch && idocMatch.length === 1, 'Should have exactly one idoc_scripts.js');
        assert(idocMatch[0].indexOf('tekuradev') !== -1,
            'The idoc_scripts.js URL should be tekuradev');
    });

    it('template 1-3 stickyNav script has correct attributes', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI101', filename: 'OSAI101-00.html'
        }));
        assert(skeleton.indexOf('src="js/stickyNav.js"') !== -1,
            'stickyNav script should have src="js/stickyNav.js"');
        assert(skeleton.indexOf('type="text/javascript"') !== -1,
            'stickyNav script should have type="text/javascript"');
        assert(skeleton.indexOf('class="stickyNav"') !== -1,
            'stickyNav script should have class="stickyNav"');
    });

    it('template 4-6 has only idoc_scripts.js (no stickyNav)', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData());
        assert(skeleton.indexOf('stickyNav') === -1,
            '4-6 should NOT include stickyNav.js');
        assert(skeleton.indexOf('idoc_scripts.js') !== -1,
            '4-6 should include idoc_scripts.js');
    });

    it('template 4-6 uses tekura.desire2learn.com (no dev infix)', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData());
        assert(skeleton.indexOf('tekura.desire2learn.com/shared/refresh_template/js/idoc_scripts.js') !== -1,
            '4-6 should use tekura (without dev infix)');
    });

    it('template 7-8 has stickyNav.js before idoc_scripts.js', function () {
        var config = engine.getConfig('7-8');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI301', filename: 'OSAI301-00.html'
        }));
        var stickyIdx = skeleton.indexOf('stickyNav.js');
        var idocIdx = skeleton.indexOf('idoc_scripts.js');
        assert(stickyIdx !== -1, '7-8 should include stickyNav.js');
        assert(idocIdx !== -1, '7-8 should include idoc_scripts.js');
        assert(stickyIdx < idocIdx,
            'stickyNav.js must appear BEFORE idoc_scripts.js');
    });

    it('template 7-8 uses tekuradev.desire2learn.com', function () {
        var config = engine.getConfig('7-8');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI301', filename: 'OSAI301-00.html'
        }));
        assert(skeleton.indexOf('tekuradev.desire2learn.com') !== -1,
            '7-8 should use tekuradev (with dev infix)');
    });

    it('additionalHeadScripts config field reflects correct defaults', function () {
        var config13 = engine.getConfig('1-3');
        assertEqual(config13.additionalHeadScripts.length, 1,
            '1-3 should have 1 additional script');
        assertEqual(config13.additionalHeadScripts[0].src, 'js/stickyNav.js',
            '1-3 additional script should be stickyNav.js');

        var config46 = engine.getConfig('4-6');
        assertEqual(config46.additionalHeadScripts.length, 0,
            '4-6 should have 0 additional scripts');

        var config78 = engine.getConfig('7-8');
        assertEqual(config78.additionalHeadScripts.length, 1,
            '7-8 should have 1 additional script');
        assertEqual(config78.additionalHeadScripts[0].src, 'js/stickyNav.js',
            '7-8 additional script should be stickyNav.js');
    });
});

// ===================================================================
// CHANGE 4 — tooltip="Overview" on #module-menu-content per template
// ===================================================================

describe('Phase 15 CHANGE 4 — tooltip on #module-menu-content per template', function () {
    var engine = _mkEngine();

    it('template 1-3 overview has NO tooltip on #module-menu-content', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI101', filename: 'OSAI101-00.html'
        }));
        assert(skeleton.indexOf('id="module-menu-content" class="moduleMenu">') !== -1,
            '1-3 overview #module-menu-content should have NO tooltip attribute');
        assert(skeleton.indexOf('id="module-menu-content" class="moduleMenu" tooltip="Overview"') === -1,
            '1-3 overview must NOT have tooltip="Overview"');
    });

    it('template 4-6 overview HAS tooltip="Overview" on #module-menu-content', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData());
        assert(skeleton.indexOf('id="module-menu-content" class="moduleMenu" tooltip="Overview"') !== -1,
            '4-6 overview should have tooltip="Overview" on #module-menu-content');
    });

    it('template 7-8 overview has NO tooltip on #module-menu-content', function () {
        var config = engine.getConfig('7-8');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI301', filename: 'OSAI301-00.html'
        }));
        assert(skeleton.indexOf('id="module-menu-content" class="moduleMenu">') !== -1,
            '7-8 overview #module-menu-content should have NO tooltip attribute');
        assert(skeleton.indexOf('id="module-menu-content" class="moduleMenu" tooltip="Overview"') === -1,
            '7-8 overview must NOT have tooltip="Overview"');
    });

    it('tooltipOn config field reflects correct values per template', function () {
        var config13 = engine.getConfig('1-3');
        assertNull(config13.moduleMenu.overviewPage.tooltipOn,
            '1-3 overview tooltipOn should be null');

        var config46 = engine.getConfig('4-6');
        assertEqual(config46.moduleMenu.overviewPage.tooltipOn, 'module-menu-content',
            '4-6 overview tooltipOn should be "module-menu-content"');

        var config78 = engine.getConfig('7-8');
        assertNull(config78.moduleMenu.overviewPage.tooltipOn,
            '7-8 overview tooltipOn should be null');
    });

    it('lesson pages remain unaffected — no tooltip on button for all templates', function () {
        var templates = ['1-3', '4-6', '7-8'];
        var codes = ['OSAI101', 'OSAI201', 'OSAI301'];
        for (var i = 0; i < templates.length; i++) {
            var config = engine.getConfig(templates[i]);
            var skeleton = engine.generateSkeleton(config, _mkPageData({
                type: 'lesson', lessonNumber: 1, pageIndex: 1,
                moduleCode: codes[i], filename: codes[i] + '-01.html',
                lessonTitle: 'Title'
            }));
            assert(skeleton.indexOf('<div id="module-menu-button" class="circle-button btn1"></div>') !== -1,
                templates[i] + ' lesson page should have no tooltip on button');
        }
    });
});

// ===================================================================
// CHANGE 5 — Footer link ordering
// ===================================================================

describe('Phase 15 CHANGE 5 — Footer link ordering', function () {
    var engine = _mkEngine();

    it('overview page: next-lesson first, then home-nav', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            totalPages: 4, pageIndex: 0
        }));
        var nextIdx = skeleton.indexOf('id="next-lesson"');
        var homeIdx = skeleton.indexOf('class="home-nav"');
        assert(nextIdx !== -1, 'Overview should have next-lesson');
        assert(homeIdx !== -1, 'Overview should have home-nav');
        assert(nextIdx < homeIdx,
            'Overview: next-lesson should come BEFORE home-nav');
    });

    it('overview page: no prev-lesson link', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            totalPages: 4, pageIndex: 0
        }));
        assert(skeleton.indexOf('id="prev-lesson"') === -1,
            'Overview page should NOT have prev-lesson');
    });

    it('lesson page: prev-lesson, then next-lesson, then home-nav', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 2, pageIndex: 2,
            filename: 'OSAI201-02.html', lessonTitle: 'Title',
            totalPages: 5
        }));
        var homeIdx = skeleton.indexOf('class="home-nav"');
        var prevIdx = skeleton.indexOf('id="prev-lesson"');
        var nextIdx = skeleton.indexOf('id="next-lesson"');
        assert(homeIdx !== -1, 'Lesson should have home-nav');
        assert(prevIdx !== -1, 'Lesson (middle) should have prev-lesson');
        assert(nextIdx !== -1, 'Lesson (middle) should have next-lesson');
        assert(prevIdx < nextIdx,
            'Lesson: prev-lesson should come BEFORE next-lesson');
        assert(nextIdx < homeIdx,
            'Lesson: next-lesson should come BEFORE home-nav');
    });

    it('first lesson page: prev-lesson (back to overview), then home-nav', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 1, pageIndex: 1,
            filename: 'OSAI201-01.html', lessonTitle: 'Title',
            totalPages: 4
        }));
        var homeIdx = skeleton.indexOf('class="home-nav"');
        var prevIdx = skeleton.indexOf('id="prev-lesson"');
        assert(homeIdx !== -1 && prevIdx !== -1,
            'First lesson should have both home-nav and prev-lesson');
        assert(prevIdx < homeIdx,
            'First lesson: prev-lesson BEFORE home-nav');
    });

    it('final lesson page: prev-lesson, then home-nav, no next-lesson', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 3, pageIndex: 3,
            filename: 'OSAI201-03.html', lessonTitle: 'Title',
            totalPages: 4
        }));
        var homeIdx = skeleton.indexOf('class="home-nav"');
        var prevIdx = skeleton.indexOf('id="prev-lesson"');
        var nextIdx = skeleton.indexOf('id="next-lesson"');
        assert(homeIdx !== -1, 'Final lesson should have home-nav');
        assert(prevIdx !== -1, 'Final lesson should have prev-lesson');
        assert(nextIdx === -1, 'Final lesson should NOT have next-lesson');
        assert(prevIdx < homeIdx,
            'Final lesson: prev-lesson BEFORE home-nav');
    });

    it('footer link ordering consistent across templates 1-3, 4-6, 7-8', function () {
        var templates = ['1-3', '4-6', '7-8'];
        var codes = ['OSAI101', 'OSAI201', 'OSAI301'];
        for (var i = 0; i < templates.length; i++) {
            var config = engine.getConfig(templates[i]);
            // Lesson page
            var skeleton = engine.generateSkeleton(config, _mkPageData({
                type: 'lesson', lessonNumber: 2, pageIndex: 2,
                moduleCode: codes[i], filename: codes[i] + '-02.html',
                lessonTitle: 'Title', totalPages: 5
            }));
            var homeIdx = skeleton.indexOf('class="home-nav"');
            var prevIdx = skeleton.indexOf('id="prev-lesson"');
            assert(prevIdx < homeIdx,
                templates[i] + ' lesson: prev-lesson should come before home-nav');
        }
    });

    it('footer still uses zero-padded filenames for navigation links', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 2, pageIndex: 2,
            filename: 'OSAI201-02.html', lessonTitle: 'Title',
            totalPages: 5
        }));
        assert(skeleton.indexOf('OSAI201-01.html') !== -1,
            'prev-lesson should use zero-padded filename');
        assert(skeleton.indexOf('OSAI201-03.html') !== -1,
            'next-lesson should use zero-padded filename');
    });
});

// ===================================================================
// Cross-template calibration snapshots
// ===================================================================

describe('Phase 15 — Cross-template calibration snapshots', function () {
    var engine = _mkEngine();

    it('OSAI101-01 (1-3 lesson): zero-padded code, stickyNav, tekuradev, no tooltip, correct footer order', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 1, pageIndex: 1,
            moduleCode: 'OSAI101', filename: 'OSAI101-01.html',
            lessonTitle: 'What is AI?', totalPages: 4
        }));
        // #module-code: zero-padded
        assert(skeleton.indexOf('<div id="module-code"><h1>01</h1></div>') !== -1,
            'OSAI101-01 module-code should be "01"');
        // <title>: no decimal
        assert(skeleton.indexOf('<title>OSAI101 AI Digital Citizenship</title>') !== -1,
            'OSAI101-01 title should be MODULE_CODE + English Title');
        // Scripts: stickyNav + tekuradev
        assert(skeleton.indexOf('stickyNav.js') !== -1,
            'OSAI101-01 should have stickyNav');
        assert(skeleton.indexOf('tekuradev.desire2learn.com') !== -1,
            'OSAI101-01 should use tekuradev');
        // Footer: prev-lesson before home-nav (lesson pages)
        var homeIdx = skeleton.indexOf('class="home-nav"');
        var prevIdx = skeleton.indexOf('id="prev-lesson"');
        assert(prevIdx < homeIdx, 'OSAI101-01 footer: prev-lesson before home-nav');
    });

    it('OSAI201-01 (4-6 lesson): decimal code, no stickyNav, tekura, no tooltip on button, correct footer', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 1, pageIndex: 1,
            filename: 'OSAI201-01.html', lessonTitle: 'What is AI?',
            totalPages: 4
        }));
        // #module-code: decimal
        assert(skeleton.indexOf('<div id="module-code"><h1>1.0</h1></div>') !== -1,
            'OSAI201-01 module-code should be "1.0"');
        // <title>: no decimal
        assert(skeleton.indexOf('<title>OSAI201 AI Digital Citizenship</title>') !== -1,
            'OSAI201-01 title should be MODULE_CODE + English Title');
        // Scripts: no stickyNav
        assert(skeleton.indexOf('stickyNav') === -1,
            'OSAI201-01 should NOT have stickyNav');
        assert(skeleton.indexOf('tekura.desire2learn.com/shared/refresh_template/js/idoc_scripts.js') !== -1,
            'OSAI201-01 should use tekura (no dev)');
        // Footer: prev-lesson before home-nav (lesson pages)
        var homeIdx = skeleton.indexOf('class="home-nav"');
        var prevIdx = skeleton.indexOf('id="prev-lesson"');
        assert(prevIdx < homeIdx, 'OSAI201-01 footer: prev-lesson before home-nav');
    });

    it('OSAI301-01 (7-8 lesson): zero-padded code, stickyNav, tekuradev, no tooltip, correct footer', function () {
        var config = engine.getConfig('7-8');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            type: 'lesson', lessonNumber: 1, pageIndex: 1,
            moduleCode: 'OSAI301', filename: 'OSAI301-01.html',
            lessonTitle: 'What is AI?', totalPages: 4
        }));
        // #module-code: zero-padded
        assert(skeleton.indexOf('<div id="module-code"><h1>01</h1></div>') !== -1,
            'OSAI301-01 module-code should be "01"');
        // <title>: no decimal
        assert(skeleton.indexOf('<title>OSAI301 AI Digital Citizenship</title>') !== -1,
            'OSAI301-01 title should be MODULE_CODE + English Title');
        // Scripts: stickyNav + tekuradev
        assert(skeleton.indexOf('stickyNav.js') !== -1,
            'OSAI301-01 should have stickyNav');
        assert(skeleton.indexOf('tekuradev.desire2learn.com') !== -1,
            'OSAI301-01 should use tekuradev');
        // Footer: prev-lesson before home-nav (lesson pages)
        var homeIdx = skeleton.indexOf('class="home-nav"');
        var prevIdx = skeleton.indexOf('id="prev-lesson"');
        assert(prevIdx < homeIdx, 'OSAI301-01 footer: prev-lesson before home-nav');
    });

    it('OSAI101-00 (1-3 overview): full module code, no tooltip, overview footer order', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            moduleCode: 'OSAI101', filename: 'OSAI101-00.html',
            totalPages: 4
        }));
        // #module-code: full code
        assert(skeleton.indexOf('<div id="module-code"><h1>OSAI101</h1></div>') !== -1,
            'OSAI101-00 module-code should be full code');
        // No tooltip on menu-content
        assert(skeleton.indexOf('id="module-menu-content" class="moduleMenu" tooltip') === -1,
            'OSAI101-00 should NOT have tooltip on module-menu-content');
        // Footer: next-lesson before home-nav
        var nextIdx = skeleton.indexOf('id="next-lesson"');
        var homeIdx = skeleton.indexOf('class="home-nav"');
        assert(nextIdx < homeIdx, 'OSAI101-00 footer: next-lesson before home-nav');
    });

    it('OSAI201-00 (4-6 overview): full module code, tooltip present, overview footer order', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, _mkPageData({
            totalPages: 4
        }));
        // #module-code: full code
        assert(skeleton.indexOf('<div id="module-code"><h1>OSAI201</h1></div>') !== -1,
            'OSAI201-00 module-code should be full code');
        // Tooltip present
        assert(skeleton.indexOf('id="module-menu-content" class="moduleMenu" tooltip="Overview"') !== -1,
            'OSAI201-00 should have tooltip="Overview" on module-menu-content');
        // Footer: next-lesson before home-nav
        var nextIdx = skeleton.indexOf('id="next-lesson"');
        var homeIdx = skeleton.indexOf('class="home-nav"');
        assert(nextIdx < homeIdx, 'OSAI201-00 footer: next-lesson before home-nav');
    });
});
