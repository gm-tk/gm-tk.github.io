/**
 * Session D — Lesson Menu Styles: baseline + promote-to-h5
 *
 * Verifies:
 *   - The baseline "synthesise-headings" style (4-6) still emits
 *     <h5>Learning Intentions</h5> / <h5>How will I know if I've learned it?</h5>
 *     above writer intro <p> elements (Phase 13 behaviour preserved).
 *   - The new "promote-to-h5" style (1-3 / 9-10 / NCEA) promotes the writer's
 *     "We are learning:" / "I can:" body lines directly to <h5>, does NOT
 *     synthesise parent section headings, and keeps any preceding descriptive
 *     paragraph as <p>.
 */

describe('Session D — baseline synthesise-headings (4-6) unchanged', function () {
    var normaliser = new TagNormaliser();
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;
    var converter = new HtmlConverter(normaliser, engine);
    var config = engine.getConfig('4-6');

    function mkPara(text) {
        return {
            type: 'paragraph',
            data: { runs: [{ text: text, formatting: {} }], text: text }
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

    it('4-6 emits synthesised <h5>Learning Intentions</h5> before writer intro <p>', function () {
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('what AI is.'),
            mkPara('I can:'),
            mkBullet('explain AI.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf('<h5>Learning Intentions</h5>') !== -1,
            'Expected synthesised <h5>Learning Intentions</h5> for 4-6');
        assert(html.indexOf('<p>We are learning:</p>') !== -1,
            'Expected <p>We are learning:</p> writer intro');
        var hIdx = html.indexOf('Learning Intentions');
        var pIdx = html.indexOf('We are learning:');
        assert(hIdx < pIdx, 'Synthesised heading must appear before writer intro');
    });

    it('4-6 menuStyle is explicitly "synthesise-headings"', function () {
        assert(config.moduleMenu.lessonPage.menuStyle === 'synthesise-headings',
            'Expected 4-6 menuStyle to be synthesise-headings');
    });
});

describe('Session D — promote-to-h5 style (1-3 / 9-10 / NCEA)', function () {
    var normaliser = new TagNormaliser();
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;
    var converter = new HtmlConverter(normaliser, engine);

    function mkPara(text) {
        return {
            type: 'paragraph',
            data: { runs: [{ text: text, formatting: {} }], text: text }
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

    it('1-3 / 9-10 / NCEA all resolve menuStyle === "promote-to-h5"', function () {
        ['1-3', '9-10', 'NCEA'].forEach(function (id) {
            var cfg = engine.getConfig(id);
            assert(cfg.moduleMenu.lessonPage.menuStyle === 'promote-to-h5',
                id + ' menuStyle should be promote-to-h5');
        });
    });

    it('promotes "We are learning:" + "I can:" body lines to <h5> (no intro paragraph)', function () {
        var cfg = engine.getConfig('1-3');
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('what AI is.'),
            mkPara('I can:'),
            mkBullet('explain AI.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, cfg, {}, menuBlocks);
        assert(html.indexOf('<h5>We are learning:</h5>') !== -1,
            'Expected <h5>We are learning:</h5>');
        assert(html.indexOf('<h5>I can:</h5>') !== -1 ||
               html.indexOf('<h5>You will show your understanding by:</h5>') !== -1,
            'Expected a success <h5> heading promoted from body');
        assert(html.indexOf('Learning Intentions') === -1,
            'No synthesised Learning Intentions heading should appear');
        assert(html.indexOf("How will I know if I've learned it?") === -1,
            'No synthesised success heading should appear');
        assert(html.indexOf('<li>what AI is.</li>') !== -1, '<ul><li> should follow learning <h5>');
    });

    it('keeps preceding descriptive intro paragraph as <p>', function () {
        var cfg = engine.getConfig('1-3');
        var menuBlocks = [
            mkPara('In this lesson we explore AI.'),
            mkPara('We are learning:'),
            mkBullet('what AI is.'),
            mkPara('I can:'),
            mkBullet('explain AI.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, cfg, {}, menuBlocks);
        assert(html.indexOf('<p>In this lesson we explore AI.</p>') !== -1,
            'Intro descriptive <p> should be preserved');
        var descIdx = html.indexOf('In this lesson');
        var h5Idx = html.indexOf('<h5>We are learning:');
        assert(descIdx < h5Idx, 'Intro <p> should appear before promoted <h5>');
    });

    it('promote-to-h5 without intro paragraph still emits both <h5> with <ul>', function () {
        var cfg = engine.getConfig('NCEA');
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('a.'),
            mkBullet('b.'),
            mkPara('I can:'),
            mkBullet('c.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, cfg, {}, menuBlocks);
        assert(html.indexOf('<h5>We are learning:</h5>') !== -1, 'learning <h5> emitted');
        assert(html.indexOf('<h5>I can:</h5>') !== -1, 'success <h5> emitted');
        assert(html.indexOf('<ul>') !== -1, '<ul> emitted');
        assert(html.indexOf('Learning Intentions') === -1, 'No synthesised parent heading');
    });

    it('promote-to-h5 keeps trailing colon inside <h5>', function () {
        var cfg = engine.getConfig('9-10');
        var menuBlocks = [mkPara('We are learning:'), mkBullet('x.')];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, cfg, {}, menuBlocks);
        assert(html.indexOf('<h5>We are learning:</h5>') !== -1,
            'Trailing colon must be kept inside <h5>');
    });
});
