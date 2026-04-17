/**
 * Footer Link Ordering Tests (Session C)
 *
 * Validates the corrected footer link ordering across all 5 templates:
 *
 *   Lesson pages (pageIndex > 0) — UNIFORM across all templates:
 *     Middle pages: prev-lesson, next-lesson, home-nav
 *     Final page:   prev-lesson, home-nav (no next-lesson)
 *
 *   Overview pages (pageIndex === 0) — VARIES by template:
 *     Templates 1-3, 7-8, NCEA: home-nav, next-lesson
 *     Templates 4-6, 9-10:      next-lesson, home-nav
 *
 * This corrects an incorrect lesson-page ordering applied in an earlier
 * session and introduces config-driven overview ordering via the new
 * config field `footerPattern.overviewPage.linkOrder`.
 */

(function () {
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

    function _overviewSkeleton(engine, templateKey, moduleCode, totalPages) {
        var config = engine.getConfig(templateKey);
        return engine.generateSkeleton(config, _mkPageData({
            type: 'overview', pageIndex: 0,
            moduleCode: moduleCode,
            filename: moduleCode + '-00.html',
            totalPages: totalPages
        }));
    }

    function _lessonSkeleton(engine, templateKey, moduleCode, pageIndex, totalPages) {
        var config = engine.getConfig(templateKey);
        var pad = String(pageIndex).padStart(2, '0');
        return engine.generateSkeleton(config, _mkPageData({
            type: 'lesson',
            lessonNumber: pageIndex,
            pageIndex: pageIndex,
            moduleCode: moduleCode,
            filename: moduleCode + '-' + pad + '.html',
            lessonTitle: 'Lesson ' + pageIndex,
            totalPages: totalPages
        }));
    }

    // ===================================================================
    // Overview page — baseConfig default (next-lesson, home-nav)
    // ===================================================================

    describe('Session C — Overview page: baseConfig default (next-lesson, home-nav)', function () {
        var engine = _mkEngine();

        it('template 4-6 overview renders next-lesson before home-nav', function () {
            var skeleton = _overviewSkeleton(engine, '4-6', 'OSAI201', 4);
            var nextIdx = skeleton.indexOf('id="next-lesson"');
            var homeIdx = skeleton.indexOf('class="home-nav"');
            assert(nextIdx !== -1, '4-6 overview should have next-lesson');
            assert(homeIdx !== -1, '4-6 overview should have home-nav');
            assert(nextIdx < homeIdx,
                '4-6 overview: next-lesson BEFORE home-nav');
        });

        it('template 9-10 overview renders next-lesson before home-nav', function () {
            var skeleton = _overviewSkeleton(engine, '9-10', 'ENGS901', 4);
            var nextIdx = skeleton.indexOf('id="next-lesson"');
            var homeIdx = skeleton.indexOf('class="home-nav"');
            assert(nextIdx !== -1, '9-10 overview should have next-lesson');
            assert(homeIdx !== -1, '9-10 overview should have home-nav');
            assert(nextIdx < homeIdx,
                '9-10 overview: next-lesson BEFORE home-nav');
        });
    });

    // ===================================================================
    // Overview page — template override (home-nav, next-lesson)
    // ===================================================================

    describe('Session C — Overview page: 1-3 / 7-8 / NCEA override (home-nav, next-lesson)', function () {
        var engine = _mkEngine();

        it('template 1-3 overview renders home-nav before next-lesson', function () {
            var skeleton = _overviewSkeleton(engine, '1-3', 'OSAI101', 4);
            var nextIdx = skeleton.indexOf('id="next-lesson"');
            var homeIdx = skeleton.indexOf('class="home-nav"');
            assert(nextIdx !== -1, '1-3 overview should have next-lesson');
            assert(homeIdx !== -1, '1-3 overview should have home-nav');
            assert(homeIdx < nextIdx,
                '1-3 overview: home-nav BEFORE next-lesson');
        });

        it('template 7-8 overview renders home-nav before next-lesson', function () {
            var skeleton = _overviewSkeleton(engine, '7-8', 'OSAI301', 4);
            var nextIdx = skeleton.indexOf('id="next-lesson"');
            var homeIdx = skeleton.indexOf('class="home-nav"');
            assert(nextIdx !== -1, '7-8 overview should have next-lesson');
            assert(homeIdx !== -1, '7-8 overview should have home-nav');
            assert(homeIdx < nextIdx,
                '7-8 overview: home-nav BEFORE next-lesson');
        });

        it('template NCEA overview renders home-nav before next-lesson', function () {
            var skeleton = _overviewSkeleton(engine, 'NCEA', 'ENGS301', 4);
            var nextIdx = skeleton.indexOf('id="next-lesson"');
            var homeIdx = skeleton.indexOf('class="home-nav"');
            assert(nextIdx !== -1, 'NCEA overview should have next-lesson');
            assert(homeIdx !== -1, 'NCEA overview should have home-nav');
            assert(homeIdx < nextIdx,
                'NCEA overview: home-nav BEFORE next-lesson');
        });
    });

    // ===================================================================
    // Overview page — single-page module suppresses next-lesson
    // ===================================================================

    describe('Session C — Overview page: single-page module omits next-lesson', function () {
        var engine = _mkEngine();

        it('totalPages === 1 omits next-lesson even when override orders it first', function () {
            var skeleton = _overviewSkeleton(engine, '1-3', 'OSAI101', 1);
            assert(skeleton.indexOf('id="next-lesson"') === -1,
                'Single-page 1-3 overview should NOT emit next-lesson');
            assert(skeleton.indexOf('class="home-nav"') !== -1,
                'Single-page 1-3 overview should still emit home-nav');
        });

        it('totalPages === 1 on default-order template also omits next-lesson', function () {
            var skeleton = _overviewSkeleton(engine, '4-6', 'OSAI201', 1);
            assert(skeleton.indexOf('id="next-lesson"') === -1,
                'Single-page 4-6 overview should NOT emit next-lesson');
            assert(skeleton.indexOf('class="home-nav"') !== -1,
                'Single-page 4-6 overview should still emit home-nav');
        });
    });

    // ===================================================================
    // Lesson page — middle page: prev-lesson, next-lesson, home-nav
    // (uniform across all 5 templates — one test per template)
    // ===================================================================

    describe('Session C — Lesson page middle: prev, next, home (uniform across templates)', function () {
        var engine = _mkEngine();

        function _assertMiddleOrder(templateKey, moduleCode) {
            var skeleton = _lessonSkeleton(engine, templateKey, moduleCode, 2, 5);
            var prevIdx = skeleton.indexOf('id="prev-lesson"');
            var nextIdx = skeleton.indexOf('id="next-lesson"');
            var homeIdx = skeleton.indexOf('class="home-nav"');
            assert(prevIdx !== -1, templateKey + ' middle: has prev-lesson');
            assert(nextIdx !== -1, templateKey + ' middle: has next-lesson');
            assert(homeIdx !== -1, templateKey + ' middle: has home-nav');
            assert(prevIdx < nextIdx,
                templateKey + ' middle: prev-lesson BEFORE next-lesson');
            assert(nextIdx < homeIdx,
                templateKey + ' middle: next-lesson BEFORE home-nav');
        }

        it('template 1-3 middle lesson renders prev, next, home', function () {
            _assertMiddleOrder('1-3', 'OSAI101');
        });

        it('template 4-6 middle lesson renders prev, next, home', function () {
            _assertMiddleOrder('4-6', 'OSAI201');
        });

        it('template 7-8 middle lesson renders prev, next, home', function () {
            _assertMiddleOrder('7-8', 'OSAI301');
        });

        it('template 9-10 middle lesson renders prev, next, home', function () {
            _assertMiddleOrder('9-10', 'ENGS901');
        });

        it('template NCEA middle lesson renders prev, next, home', function () {
            _assertMiddleOrder('NCEA', 'ENGS301');
        });
    });

    // ===================================================================
    // Lesson page — final page: prev-lesson, home-nav (no next-lesson)
    // (order identical across all 5 templates — one collective test)
    // ===================================================================

    describe('Session C — Lesson page final: prev, home (no next-lesson) — all templates', function () {
        var engine = _mkEngine();

        it('final lesson page: prev-lesson before home-nav, no next-lesson, across all 5 templates', function () {
            var templates = [
                { key: '1-3',  code: 'OSAI101' },
                { key: '4-6',  code: 'OSAI201' },
                { key: '7-8',  code: 'OSAI301' },
                { key: '9-10', code: 'ENGS901' },
                { key: 'NCEA', code: 'ENGS301' }
            ];
            for (var i = 0; i < templates.length; i++) {
                var t = templates[i];
                var skeleton = _lessonSkeleton(engine, t.key, t.code, 3, 4);
                var prevIdx = skeleton.indexOf('id="prev-lesson"');
                var nextIdx = skeleton.indexOf('id="next-lesson"');
                var homeIdx = skeleton.indexOf('class="home-nav"');
                assert(prevIdx !== -1, t.key + ' final: has prev-lesson');
                assert(homeIdx !== -1, t.key + ' final: has home-nav');
                assert(nextIdx === -1,
                    t.key + ' final: should NOT have next-lesson');
                assert(prevIdx < homeIdx,
                    t.key + ' final: prev-lesson BEFORE home-nav');
            }
        });
    });

    // ===================================================================
    // Regression guard — no lesson page renders home-nav before prev-lesson
    // ===================================================================

    describe('Session C — Regression guard: lesson pages never order home-nav before prev-lesson', function () {
        var engine = _mkEngine();

        it('no template emits home-nav BEFORE prev-lesson on any lesson page', function () {
            var templates = [
                { key: '1-3',  code: 'OSAI101' },
                { key: '4-6',  code: 'OSAI201' },
                { key: '7-8',  code: 'OSAI301' },
                { key: '9-10', code: 'ENGS901' },
                { key: 'NCEA', code: 'ENGS301' }
            ];
            for (var i = 0; i < templates.length; i++) {
                var t = templates[i];
                // Check both middle and final lesson pages
                var middle = _lessonSkeleton(engine, t.key, t.code, 2, 5);
                var final = _lessonSkeleton(engine, t.key, t.code, 3, 4);
                var mPrev = middle.indexOf('id="prev-lesson"');
                var mHome = middle.indexOf('class="home-nav"');
                var fPrev = final.indexOf('id="prev-lesson"');
                var fHome = final.indexOf('class="home-nav"');
                assert(mPrev < mHome,
                    t.key + ' middle: prev-lesson must precede home-nav');
                assert(fPrev < fHome,
                    t.key + ' final: prev-lesson must precede home-nav');
            }
        });
    });
}());
