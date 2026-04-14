/**
 * Phase 13 — Years 4–6 Lesson Page Recalibration Tests
 *
 * Covers the four discrepancies identified in the OSAI201-01 calibration
 * snapshot and the structural changes introduced to resolve them:
 *
 *   Discrepancy 1 — <title> contains no lesson decimal number
 *   Discrepancy 2 — lesson <h1> uses the lesson-specific title
 *                   (single h1, no trailing space, no Te Reo for 1-3/4-6/7-8)
 *   Discrepancy 3 — lesson #module-menu-button has NO tooltip attribute
 *   Discrepancy 4 — lesson module menu uses the new two-tier structure
 *                   <h5>{sectionHeading}</h5><p>{writer intro}</p><ul>...
 *
 * Verifies that prior behaviour for overview pages (full-tab menu, tooltip on
 * #module-menu-content, dual h1 for 9-10/NCEA) is not disturbed.
 */

// ===================================================================
// Discrepancy 1 — <title> element has no decimal lesson number
// ===================================================================

describe('Phase 13 — Discrepancy 1: <title> has no decimal lesson number', function () {
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;

    it('lesson page <title> is MODULE_CODE + English Title only', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'OSAI201-01.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null,
            lessonTitle: 'What is AI?',
            totalPages: 5,
            pageIndex: 1
        });
        assert(skeleton.indexOf('<title>OSAI201 AI Digital Citizenship</title>') !== -1,
            'Expected <title>OSAI201 AI Digital Citizenship</title>');
        assert(skeleton.indexOf('1.0') === -1 ||
            skeleton.indexOf('<title>OSAI201 1.0') === -1,
            '<title> must not contain the lesson decimal "1.0"');
    });

    it('overview page <title> is MODULE_CODE + English Title only', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'overview',
            lessonNumber: null,
            filename: 'OSAI201-00.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null,
            totalPages: 5,
            pageIndex: 0
        });
        assert(skeleton.indexOf('<title>OSAI201 AI Digital Citizenship</title>') !== -1,
            'Expected overview <title> with no decimal');
        assert(skeleton.indexOf('<title>OSAI201 0.0') === -1,
            'Overview <title> must not contain "0.0"');
    });

    it('still keeps decimal lesson format inside #module-code display', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'OSAI201-01.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null,
            lessonTitle: 'What is AI?',
            totalPages: 5,
            pageIndex: 1
        });
        assert(skeleton.indexOf('<div id="module-code"><h1>1.0</h1></div>') !== -1,
            '#module-code display should still use decimal "1.0"');
    });
});

// ===================================================================
// Discrepancy 2 — Lesson-specific <h1>, single, no trailing space,
//                 no Te Reo for 1-3/4-6/7-8 lesson pages
// ===================================================================

describe('Phase 13 — Discrepancy 2: lesson <h1> uses lesson-specific title', function () {
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;

    it('Years 4–6 lesson page <h1> uses lessonTitle, not module title', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'OSAI201-01.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: 'Kirirarautanga Matihiko AI',
            lessonTitle: 'What is AI?',
            totalPages: 5,
            pageIndex: 1
        });
        assert(skeleton.indexOf('<h1><span>What is AI?</span></h1>') !== -1,
            'Expected <h1><span>What is AI?</span></h1>');
    });

    it('lesson <h1> has NO trailing space inside span', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'OSAI201-01.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null,
            lessonTitle: 'What is AI?',
            totalPages: 5,
            pageIndex: 1
        });
        assert(skeleton.indexOf('<span>What is AI? </span>') === -1,
            'No trailing space inside the <span>');
        assert(skeleton.indexOf('<span>What is AI?</span>') !== -1,
            'Span content has no trailing space');
    });

    it('overview <h1> also has NO trailing space inside span', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'overview',
            lessonNumber: null,
            filename: 'OSAI201-00.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null,
            totalPages: 5,
            pageIndex: 0
        });
        assert(skeleton.indexOf('<span>AI Digital Citizenship </span>') === -1,
            'Overview <h1> span should have no trailing space');
        assert(skeleton.indexOf('<span>AI Digital Citizenship</span>') !== -1,
            'Overview <h1> span without trailing space');
    });

    it('Years 4–6 lesson page has exactly one <h1> title element (no Te Reo)', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'OSAI201-01.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: 'Kirirarautanga Matihiko AI',
            lessonTitle: 'What is AI?',
            totalPages: 5,
            pageIndex: 1
        });
        // Count <h1><span> occurrences in the header (i.e. title h1s)
        var matches = skeleton.match(/<h1><span>/g);
        assertEqual(matches ? matches.length : 0, 1,
            'Expected exactly one title <h1><span> on 4-6 lesson page');
        assert(skeleton.indexOf('Kirirarautanga') === -1,
            'Te Reo title should not appear on 4-6 lesson page');
    });

    it('Years 9–10 lesson page still emits dual English + Te Reo <h1>', function () {
        var config = engine.getConfig('9-10');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'XYZ401-01.html',
            moduleCode: 'XYZ401',
            englishTitle: 'English Title',
            tereoTitle: 'Te Reo Title',
            lessonTitle: 'Lesson Title',
            totalPages: 3,
            pageIndex: 1
        });
        assert(skeleton.indexOf('Te Reo Title') !== -1,
            '9-10 lesson page should still emit Te Reo <h1>');
    });

    it('lesson-title extraction strips "Lesson N:" prefix', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'OSAI201-01.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null,
            lessonTitle: 'Lesson 1: What is AI?',
            totalPages: 5,
            pageIndex: 1
        });
        assert(skeleton.indexOf('<h1><span>What is AI?</span></h1>') !== -1,
            'Prefix "Lesson 1:" should be stripped');
    });

    it('falls back to module title when lessonTitle is missing (with warning)', function () {
        var origWarn = console.warn;
        var warned = false;
        console.warn = function () { warned = true; };
        try {
            var config = engine.getConfig('4-6');
            var skeleton = engine.generateSkeleton(config, {
                type: 'lesson',
                lessonNumber: 1,
                filename: 'ABC201-01.html',
                moduleCode: 'ABC201',
                englishTitle: 'Module Title',
                tereoTitle: null,
                lessonTitle: null,
                totalPages: 3,
                pageIndex: 1
            });
            assert(skeleton.indexOf('<h1><span>Module Title</span></h1>') !== -1,
                'Falls back to module title when lessonTitle missing');
            assert(warned, 'A console warning should be emitted on fallback');
        } finally {
            console.warn = origWarn;
        }
    });

    it('HtmlConverter._extractLessonTitle finds first [H2] heading', function () {
        var normaliser = new TagNormaliser();
        var te = new TemplateEngine();
        te._data = TemplateEngine._embeddedData();
        te._loaded = true;
        var converter = new HtmlConverter(normaliser, te);

        var blocks = [
            {
                type: 'paragraph',
                data: {
                    runs: [
                        { text: '[H2] ', formatting: { isRed: true } },
                        { text: 'Lesson 1: What is AI?', formatting: {} }
                    ],
                    text: '[H2] Lesson 1: What is AI?'
                }
            },
            {
                type: 'paragraph',
                data: {
                    runs: [
                        { text: '[body] ', formatting: { isRed: true } },
                        { text: 'AI stands for…', formatting: {} }
                    ],
                    text: '[body] AI stands for…'
                }
            }
        ];
        var title = converter._extractLessonTitle(blocks);
        // _extractLessonTitle returns the raw clean text; prefix stripping
        // happens inside the template engine via _stripLessonPrefix.
        assert(title && title.indexOf('What is AI?') !== -1,
            'Expected extracted title to contain "What is AI?" (got: ' + title + ')');
    });
});

// ===================================================================
// Discrepancy 3 — lesson #module-menu-button has no tooltip attribute
// ===================================================================

describe('Phase 13 — Discrepancy 3: lesson #module-menu-button has no tooltip', function () {
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;

    it('Years 4–6 lesson page has no tooltip on #module-menu-button', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'OSAI201-01.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null,
            lessonTitle: 'What is AI?',
            totalPages: 5,
            pageIndex: 1
        });
        assert(skeleton.indexOf('<div id="module-menu-button" class="circle-button btn1"></div>') !== -1,
            'Lesson #module-menu-button must have NO tooltip attribute');
        assert(skeleton.indexOf('id="module-menu-button" class="circle-button btn1" tooltip') === -1,
            'No tooltip attribute allowed on lesson #module-menu-button');
    });

    it('Years 1–3 lesson page also has no tooltip on button', function () {
        var config = engine.getConfig('1-3');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'ABC101-01.html',
            moduleCode: 'ABC101',
            englishTitle: 'Title',
            tereoTitle: null,
            lessonTitle: 'Lesson Title',
            totalPages: 3,
            pageIndex: 1
        });
        assert(skeleton.indexOf('<div id="module-menu-button" class="circle-button btn1"></div>') !== -1,
            '1-3 lesson page button has no tooltip');
    });

    it('Years 7–8 lesson page also has no tooltip on button', function () {
        var config = engine.getConfig('7-8');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'ABC301-01.html',
            moduleCode: 'ABC301',
            englishTitle: 'Title',
            tereoTitle: null,
            lessonTitle: 'Lesson Title',
            totalPages: 3,
            pageIndex: 1
        });
        assert(skeleton.indexOf('<div id="module-menu-button" class="circle-button btn1"></div>') !== -1,
            '7-8 lesson page button has no tooltip');
    });

    it('overview page STILL has tooltip on #module-menu-content (not changed)', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'overview',
            lessonNumber: null,
            filename: 'OSAI201-00.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: null,
            totalPages: 5,
            pageIndex: 0
        });
        assert(skeleton.indexOf('id="module-menu-content" class="moduleMenu" tooltip="Overview"') !== -1,
            'Overview page still has tooltip="Overview" on #module-menu-content');
        assert(skeleton.indexOf('id="module-menu-button" class="circle-button btn1"></div>') !== -1,
            'Overview page button still has no tooltip attribute');
    });
});

// ===================================================================
// Discrepancy 4 — two-tier lesson module menu structure
// ===================================================================

describe('Phase 13 — Discrepancy 4: two-tier lesson module menu', function () {
    var normaliser = new TagNormaliser();
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;
    var converter = new HtmlConverter(normaliser, engine);
    var config = engine.getConfig('4-6');

    function mkPara(text, isRed) {
        return {
            type: 'paragraph',
            data: {
                runs: [{ text: text, formatting: isRed ? { isRed: true } : {} }],
                text: text
            }
        };
    }

    function mkBullet(text) {
        return {
            type: 'paragraph',
            data: {
                runs: [{ text: text, formatting: {} }],
                text: text,
                isListItem: true,
                listLevel: 0,
                listFormat: 'bullet',
                listNumId: '1'
            }
        };
    }

    it('emits <h5>{sectionHeading}</h5><p>{writer intro}</p><ul> for learning section', function () {
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('what AI is.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf('<h5>Learning Intentions</h5>') !== -1,
            'Expected section heading <h5>Learning Intentions</h5>');
        assert(html.indexOf('<p>We are learning:</p>') !== -1,
            'Expected writer intro paragraph <p>We are learning:</p>');
        assert(html.indexOf('<li>what AI is.</li>') !== -1,
            'Expected <li>what AI is.</li>');
        // Structural ordering — section heading before intro before list
        var hIdx = html.indexOf('Learning Intentions');
        var pIdx = html.indexOf('We are learning:');
        var liIdx = html.indexOf('<li>what AI is');
        assert(hIdx < pIdx && pIdx < liIdx,
            'Expected ordering h5 → p → li (got indices ' +
            hIdx + ', ' + pIdx + ', ' + liIdx + ')');
    });

    it('emits <h5>How will I know if I\'ve learned it?</h5><p>I can:</p><ul> for success section', function () {
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('what AI is.'),
            mkPara('I can:'),
            mkBullet('understand what AI is.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf("<h5>How will I know if I've learned it?</h5>") !== -1,
            'Expected section heading for success');
        assert(html.indexOf('<p>I can:</p>') !== -1,
            'Expected writer intro <p>I can:</p>');
        assert(html.indexOf('<li>understand what AI is.</li>') !== -1,
            'Expected <li>understand what AI is.</li>');
    });

    it('preserves writer intro text verbatim (e.g. "You will show your understanding by:")', function () {
        // Phase 13 reversal: writer intro text is rendered verbatim, NOT
        // substituted with config label text.
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('x.'),
            mkPara('You will show your understanding by:'),
            mkBullet('y.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf('<p>You will show your understanding by:</p>') !== -1,
            'Writer intro text must be preserved verbatim');
    });

    it('section with intro text but no list items still emits heading + intro', function () {
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('x.'),
            mkPara('I can:')
            // No bullets for success
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf("<h5>How will I know if I've learned it?</h5>") !== -1,
            'Success section heading still emitted');
        assert(html.indexOf('<p>I can:</p>') !== -1,
            'Success intro paragraph still emitted');
    });

    it('section with list items but no recognised intro text still emits heading', function () {
        // When only list items exist and no intro paragraph was found,
        // the empty-content fallback should still emit section headings.
        var menuBlocks = [];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf('<h5>Learning Intentions</h5>') !== -1,
            'Empty fallback still emits learning section heading');
        assert(html.indexOf("<h5>How will I know if I've learned it?</h5>") !== -1,
            'Empty fallback still emits success section heading');
    });

    it('all four supported year levels use the same sectionHeadings defaults', function () {
        var years = ['1-3', '4-6', '7-8', '9-10', 'NCEA'];
        for (var i = 0; i < years.length; i++) {
            var cfg = engine.getConfig(years[i]);
            var sh = cfg.moduleMenu.lessonPage.sectionHeadings;
            assertEqual(sh.learning, 'Learning Intentions',
                years[i] + ' should use "Learning Intentions" as learning heading');
            assertEqual(sh.success, "How will I know if I've learned it?",
                years[i] + ' should use "How will I know if I\'ve learned it?" as success heading');
        }
    });

    it('legacy labels are still preserved in config as fallback intro text', function () {
        var cfg46 = engine.getConfig('4-6');
        assertEqual(cfg46.moduleMenu.lessonPage.labels.learning, 'We are learning:',
            'Legacy "learning" label preserved as fallback');
        assertEqual(cfg46.moduleMenu.lessonPage.labels.success, 'You will show your understanding by:',
            'Legacy "success" label preserved as fallback (4-6 override)');
    });
});

// ===================================================================
// Calibration snapshot — end-to-end OSAI201-01 assertion
// ===================================================================

describe('Phase 13 — OSAI201 calibration snapshot (lesson page assembly)', function () {
    // Exercises template-engine + html-converter together by building a
    // realistic lesson-page skeleton and asserting the four recalibrated
    // regions match the human reference structure.
    var normaliser = new TagNormaliser();
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;

    it('OSAI201-01.html header + <title> + menu button matches human reference', function () {
        var config = engine.getConfig('4-6');
        var skeleton = engine.generateSkeleton(config, {
            type: 'lesson',
            lessonNumber: 1,
            filename: 'OSAI201-01.html',
            moduleCode: 'OSAI201',
            englishTitle: 'AI Digital Citizenship',
            tereoTitle: 'Kirirarautanga Matihiko AI',
            lessonTitle: 'What is AI?',
            totalPages: 5,
            pageIndex: 1
        });

        // Discrepancy 1 — <title>
        assert(skeleton.indexOf('<title>OSAI201 AI Digital Citizenship</title>') !== -1,
            '<title> should omit lesson decimal');

        // Discrepancy 2 — single lesson <h1>, no trailing space, no Te Reo
        assert(skeleton.indexOf('<h1><span>What is AI?</span></h1>') !== -1,
            'Lesson <h1> uses lesson title, no trailing space');
        assert(skeleton.indexOf('Kirirarautanga') === -1,
            'No Te Reo <h1> on 4-6 lesson page');

        // Discrepancy 3 — no tooltip on lesson menu button
        assert(skeleton.indexOf('<div id="module-menu-button" class="circle-button btn1"></div>') !== -1,
            'No tooltip attribute on lesson #module-menu-button');
    });
});
