/**
 * Session D — Lesson Menu Style: lesson-overview-bold (Years 7-8)
 *
 * Verifies:
 *   - Single <h4>Lesson Overview</h4> appears at the top of the menu block.
 *   - Writer "We are learning:" / "I can:" body lines become
 *     <p><b>…</b></p> (trailing colon kept inside <b>).
 *   - Lists (<ul>) still follow each bold heading.
 *   - Any intro descriptive paragraph is DROPPED.
 */

describe('Session D — lesson-overview-bold style (7-8)', function () {
    var normaliser = new TagNormaliser();
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;
    var converter = new HtmlConverter(normaliser, engine);
    var config = engine.getConfig('7-8');

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

    it('7-8 resolves menuStyle === "lesson-overview-bold"', function () {
        assert(config.moduleMenu.lessonPage.menuStyle === 'lesson-overview-bold',
            'Expected 7-8 menuStyle to be lesson-overview-bold');
    });

    it('emits single <h4>Lesson Overview</h4> at the top', function () {
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('about AI.'),
            mkPara('I can:'),
            mkBullet('explain AI.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        var h4Idx = html.indexOf('<h4>Lesson Overview</h4>');
        assert(h4Idx !== -1, 'Expected <h4>Lesson Overview</h4>');
        // Ensure only ONE occurrence.
        var lastH4 = html.lastIndexOf('<h4>Lesson Overview</h4>');
        assert(lastH4 === h4Idx, 'Only one <h4>Lesson Overview</h4> permitted');
        // Should appear before the bold body lines.
        var bIdx = html.indexOf('<p><b>');
        assert(h4Idx < bIdx, '<h4> must appear before bold paragraphs');
    });

    it('converts "We are learning:" / "I can:" body lines to <p><b>…</b></p>', function () {
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('about AI.'),
            mkPara('I can:'),
            mkBullet('explain AI.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf('<p><b>We are learning:</b></p>') !== -1,
            'Expected <p><b>We are learning:</b></p>');
        assert(html.indexOf('<p><b>I can:</b></p>') !== -1,
            'Expected <p><b>I can:</b></p>');
        assert(html.indexOf('<h5>We are learning:') === -1,
            'Should NOT promote to <h5> in overview-bold style');
    });

    it('<ul> still follows each bold heading', function () {
        var menuBlocks = [
            mkPara('We are learning:'),
            mkBullet('about AI.'),
            mkPara('I can:'),
            mkBullet('explain AI.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf('<li>about AI.</li>') !== -1, 'Learning <li> present');
        assert(html.indexOf('<li>explain AI.</li>') !== -1, 'Success <li> present');
        // Ordering: learning <p><b> → <li>about AI → success <p><b> → <li>explain AI
        var lB = html.indexOf('<p><b>We are learning:');
        var lLi = html.indexOf('<li>about AI');
        var sB = html.indexOf('<p><b>I can:');
        var sLi = html.indexOf('<li>explain AI');
        assert(lB < lLi && lLi < sB && sB < sLi,
            'Expected ordering: learning bold → bullet → success bold → bullet');
    });

    it('DROPS any intro descriptive paragraph', function () {
        var menuBlocks = [
            mkPara('This lesson introduces core AI concepts.'),
            mkPara('We are learning:'),
            mkBullet('about AI.'),
            mkPara('I can:'),
            mkBullet('explain AI.')
        ];
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, menuBlocks);
        assert(html.indexOf('This lesson introduces') === -1,
            'Descriptive intro paragraph must be dropped in overview-bold style');
        assert(html.indexOf('<h4>Lesson Overview</h4>') !== -1, '<h4> still emitted');
        assert(html.indexOf('<p><b>We are learning:</b></p>') !== -1,
            'Bold learning heading still emitted');
    });

    it('empty menu blocks still emit <h4>Lesson Overview</h4> fallback', function () {
        var html = converter._generateLessonMenuContent({ type: 'lesson' }, config, {}, []);
        assert(html.indexOf('<h4>Lesson Overview</h4>') !== -1,
            '<h4>Lesson Overview</h4> still emitted on empty fallback');
    });
});
