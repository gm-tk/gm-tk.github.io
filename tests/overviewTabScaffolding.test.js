/**
 * Session A — overview tab scaffolding calibration tests.
 *
 * Covers Changes 2–4: config-driven overviewTabColumnClass,
 * overviewTabHeadingLevel, and wrapAllOverviewHeadingsInSpan.
 */

function _ots_mkEngine() {
    var engine = new TemplateEngine();
    engine._data = TemplateEngine._embeddedData();
    engine._loaded = true;
    return engine;
}

function _ots_render(templateId, isOverviewTab, blocks) {
    var engine = _ots_mkEngine();
    var config = engine.getConfig(templateId);
    var normaliser = new TagNormaliser();
    var converter = new HtmlConverter(normaliser, engine);
    if (isOverviewTab) {
        return converter._renderModuleMenuBlocks(blocks, config, '      ', true, false);
    }
    return converter._renderModuleMenuBlocks(blocks, config, '      ', false, true);
}

// Build paragraph blocks in the shape _processAllBlocks() expects.
function _ots_para(text) {
    return {
        type: 'paragraph',
        data: {
            runs: [{ text: text, formatting: {} }],
            text: text
        }
    };
}
function _ots_blocks() {
    return [
        _ots_para('[H2] Overview'),
        _ots_para('Intro sentence.'),
        _ots_para('[H2] Success Criteria'),
        _ots_para('Second section.')
    ];
}

describe('Session A — overview tab column class (Change 2)', function () {
    it('4-6 uses baseConfig default col-md-8 col-12', function () {
        var out = _ots_render('4-6', true, _ots_blocks());
        assert(out.indexOf('<div class="col-md-8 col-12">') !== -1,
            'Expected col-md-8 col-12 for 4-6 overview tab');
    });

    it('1-3 override applies col-md-12 col-12', function () {
        var out = _ots_render('1-3', true, _ots_blocks());
        assert(out.indexOf('<div class="col-md-12 col-12">') !== -1,
            'Expected col-md-12 col-12 for 1-3 overview tab');
    });

    it('7-8 override applies col-md-12 col-12', function () {
        var out = _ots_render('7-8', true, _ots_blocks());
        assert(out.indexOf('<div class="col-md-12 col-12">') !== -1,
            'Expected col-md-12 col-12 for 7-8 overview tab');
    });

    it('9-10 override applies col-md-12 col-12', function () {
        var out = _ots_render('9-10', true, _ots_blocks());
        assert(out.indexOf('<div class="col-md-12 col-12">') !== -1,
            'Expected col-md-12 col-12 for 9-10 overview tab');
    });

    it('Info tab ignores overviewTabColumnClass override (stays col-md-8 col-12)', function () {
        var out = _ots_render('1-3', false, _ots_blocks());
        assert(out.indexOf('<div class="col-md-8 col-12">') !== -1,
            'Info tab must stay col-md-8 col-12 even when 1-3 overrides overview');
        assert(out.indexOf('col-md-12 col-12') === -1,
            'Info tab must not receive col-md-12 col-12');
    });
});

describe('Session A — overview tab heading level (Change 3)', function () {
    it('4-6 overview tab headings default to h4', function () {
        var out = _ots_render('4-6', true, _ots_blocks());
        assert(out.indexOf('<h4>') !== -1 || out.indexOf('<h4><span>') !== -1,
            'Expected h4 heading tag in 4-6 overview tab');
        assert(out.indexOf('<h5>') === -1, 'h5 must not appear in 4-6 overview tab');
    });

    it('NCEA overview tab uses h5 per override', function () {
        var out = _ots_render('NCEA', true, _ots_blocks());
        assert(out.indexOf('<h5>') !== -1 || out.indexOf('<h5><span>') !== -1,
            'Expected h5 heading tag in NCEA overview tab');
    });
});

describe('Session A — wrapAllOverviewHeadingsInSpan (Change 4)', function () {
    it('4-6 default wraps only the first overview heading in <span>', function () {
        var out = _ots_render('4-6', true, _ots_blocks());
        var spans = out.match(/<h4><span>[^<]*<\/span><\/h4>/g) || [];
        assertEqual(spans.length, 1, 'Exactly one h4 span wrap expected on 4-6');
    });

    it('1-3 wraps every overview heading in <span>', function () {
        var out = _ots_render('1-3', true, _ots_blocks());
        var spans = out.match(/<h4><span>[^<]*<\/span><\/h4>/g) || [];
        assertEqual(spans.length, 2, 'Both headings wrapped in span on 1-3');
    });

    it('7-8 wraps every overview heading in <span>', function () {
        var out = _ots_render('7-8', true, _ots_blocks());
        var spans = out.match(/<h4><span>[^<]*<\/span><\/h4>/g) || [];
        assertEqual(spans.length, 2, 'Both headings wrapped in span on 7-8');
    });

    it('9-10 wraps every overview heading in <span>', function () {
        var out = _ots_render('9-10', true, _ots_blocks());
        var spans = out.match(/<h4><span>[^<]*<\/span><\/h4>/g) || [];
        assertEqual(spans.length, 2, 'Both headings wrapped in span on 9-10');
    });
});
