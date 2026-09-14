/**
 * Tests for Word equations (OMML) reaching the parsed output as LaTeX.
 *
 * A writer who types an equation with Word's equation editor produces
 * <m:oMath> / <m:oMathPara> elements that sit BESIDE the <w:r> runs inside the
 * paragraph, so the parser's run walk used to step straight past them and the
 * formula never appeared in the parsed .txt at all.
 *
 * LaTeX is the carrier because of how the equations get written in the first
 * place. Creative Services' instruction to writers is: screenshot the equation,
 * ask an AI to convert the image to LaTeX, paste that into Word, press Alt + =.
 * That keystroke makes Word swallow the LaTeX and store OMML, so the LaTeX
 * cannot be retained — only regenerated. Doing so here means the parsed .txt
 * carries LaTeX whether the writer pressed Alt + = or left their LaTeX sitting
 * in the paragraph as plain text, and the downstream Convertor has one job.
 *
 * These tests drive the REAL OmmlToLatex, DocxParser paragraph walk and
 * OutputFormatter, and cover:
 *   - the token rules (variables, numbers, prose, Greek, function names)
 *   - every construct the corpus actually contains (fraction, delimiter,
 *     superscript, subscript, radical) plus the defensive fallback
 *   - inline `\(…\)` vs display `\[…\]`, which Word records for us
 *   - the parser branch that turns an equation into a run
 *   - the formatter passing the LaTeX through untouched
 *   - a paragraph WITHOUT an equation staying byte-identical to the old output
 *
 * Fixtures (omXml / omRun) come from tests/omml-fixtures.js.
 */

'use strict';

function olConvert(xml) {
    return new OmmlToLatex().convert(omXml(xml));
}

/** Just the LaTeX body, without the `\(…\)` wrapper, for readable assertions. */
function olBody(xml) {
    return new OmmlToLatex().convertBody(omXml(xml));
}

describe('OMML -> LaTeX: token rules', function () {

    it('wraps an inline equation in \\( \\)', function () {
        assertEqual(olConvert('<m:oMath>' + omRun('x') + '</m:oMath>'), '\\(x\\)');
    });

    it('keeps a single letter as a bare variable', function () {
        assertEqual(olBody('<m:oMath>' + omRun('E=mc') + '</m:oMath>'), 'E=mc');
    });

    it('turns operators into their LaTeX commands', function () {
        assertEqual(olBody('<m:oMath>' + omRun('a×b÷c±d') + '</m:oMath>'),
            'a\\times b\\div c\\pm d');
    });

    it('keeps the guard space only where a command would otherwise fuse', function () {
        // \Delta T needs the space; \times4200 does not, because a digit cannot
        // extend a command name.
        assertEqual(olBody('<m:oMath>' + omRun('∆E=m×c×∆T=1.5×4200') + '</m:oMath>'),
            '\\Delta E=m\\times c\\times\\Delta T=1.5\\times4200');
    });

    it('maps both deltas to \\Delta', function () {
        // Word writes U+2206 INCREMENT; the finished modules use U+0394.
        assertEqual(olBody('<m:oMath>' + omRun('∆T') + '</m:oMath>'), '\\Delta T');
        assertEqual(olBody('<m:oMath>' + omRun('ΔT') + '</m:oMath>'), '\\Delta T');
    });

    it('names Greek letters instead of treating them as prose', function () {
        assertEqual(olBody('<m:oMath>' + omRun('θ=2π') + '</m:oMath>'), '\\theta=2\\pi');
    });

    it('puts prose inside an equation in \\text{}', function () {
        assertEqual(olBody('<m:oMath>' + omRun('specific heat capacity c=') + '</m:oMath>'),
            '\\text{specific heat capacity }c=');
    });

    it('treats a short letter run as variables, not prose', function () {
        // "mc" is m times c, not the word "mc" -- and P=VI is power = volts x amps.
        assertEqual(olBody('<m:oMath>' + omRun('E=mc') + '</m:oMath>'), 'E=mc');
        assertEqual(olBody('<m:oMath>' + omRun('P=VI') + '</m:oMath>'), 'P=VI');
    });

    it('keeps a two-letter word inside the phrase it belongs to', function () {
        // "of" is two letters, but it sits between real words, so it is prose.
        assertEqual(olBody('<m:oMath>' + omRun('amount of heat energy') + '</m:oMath>'),
            '\\text{amount of heat energy}');
    });

    it('treats the typographic spaces Word inserts as whitespace', function () {
        // Word's equation editor writes U+2008 PUNCTUATION SPACE and U+2009 THIN
        // SPACE into its runs; treating one as a letter used to leave it sitting
        // inside the LaTeX as a stray character (`\\frac{1}{2 }`).
        assertEqual(olBody('<m:oMath>' + omRun('2\u2008') + '</m:oMath>'), '2');
        assertEqual(olBody('<m:oMath>' + omRun('m\u2009') + '</m:oMath>'), 'm');
        assertEqual(olBody('<m:oMath>' + omRun('a\u00A0=\u00A0b') + '</m:oMath>'), 'a=b');
    });

    it('keeps a thousands separator inside one number', function () {
        assertEqual(olBody('<m:oMath>' + omRun('504,000') + '</m:oMath>'), '504,000');
    });

    it('keeps a decimal point inside one number', function () {
        assertEqual(olBody('<m:oMath>' + omRun('0.75×460') + '</m:oMath>'), '0.75\\times460');
    });

    it('recognises a function name as a command', function () {
        assertEqual(olBody('<m:oMath>' + omRun('sin x') + '</m:oMath>'), '\\sin x');
    });

    it('escapes characters that are special inside \\text{}', function () {
        var out = olBody('<m:oMath>' + omRun('per cent&amp;more') + '</m:oMath>');
        assert(out.indexOf('\\&') !== -1, 'an ampersand in prose must be escaped');
    });

    it('ignores the Word-only property elements', function () {
        assertEqual(olBody('<m:oMath><m:ctrlPr><w:rPr><w:i/></w:rPr></m:ctrlPr>' +
            omRun('y') + '</m:oMath>'), 'y');
    });

    it('treats an <m:nor/> run as literal text', function () {
        var xml = '<m:oMath><m:r><m:rPr><m:nor/></m:rPr><m:t>if</m:t></m:r></m:oMath>';
        assertEqual(olBody(xml), '\\text{if}');
    });
});

describe('OMML -> LaTeX: the constructs the corpus contains', function () {

    it('converts a fraction to \\frac', function () {
        assertEqual(olBody('<m:oMath><m:f><m:fPr><m:ctrlPr/></m:fPr>' +
            '<m:num>' + omRun('∆E') + '</m:num>' +
            '<m:den>' + omRun('m×∆T') + '</m:den></m:f></m:oMath>'),
            '\\frac{\\Delta E}{m\\times\\Delta T}');
    });

    it('reproduces the PES1008 specific-heat-capacity equation', function () {
        var xml = '<m:oMath>' + omRun('c=') +
            '<m:f><m:fPr><m:ctrlPr/></m:fPr>' +
            '<m:num>' + omRun('∆E') + '</m:num>' +
            '<m:den>' + omRun('m×∆T') + '</m:den></m:f></m:oMath>';
        assertEqual(olBody(xml), 'c=\\frac{\\Delta E}{m\\times\\Delta T}');
    });

    it('converts a superscript', function () {
        assertEqual(olBody('<m:oMath><m:sSup><m:sSupPr><m:ctrlPr/></m:sSupPr>' +
            '<m:e>' + omRun('v') + '</m:e><m:sup>' + omRun('2') + '</m:sup></m:sSup></m:oMath>'),
            '{v}^{2}');
    });

    it('converts a subscript', function () {
        assertEqual(olBody('<m:oMath><m:sSub><m:sSubPr><m:ctrlPr/></m:sSubPr>' +
            '<m:e>' + omRun('E') + '</m:e><m:sub>' + omRun('k') + '</m:sub></m:sSub></m:oMath>'),
            '{E}_{k}');
    });

    it('converts a combined sub and superscript', function () {
        assertEqual(olBody('<m:oMath><m:sSubSup><m:sSubSupPr/><m:e>' + omRun('x') + '</m:e>' +
            '<m:sub>' + omRun('i') + '</m:sub><m:sup>' + omRun('2') + '</m:sup>' +
            '</m:sSubSup></m:oMath>'), '{x}_{i}^{2}');
    });

    it('wraps a delimiter group in \\left( \\right)', function () {
        assertEqual(olBody('<m:oMath><m:d><m:dPr><m:ctrlPr/></m:dPr>' +
            '<m:e>' + omRun('100-20') + '</m:e></m:d></m:oMath>'),
            '\\left(100-20\\right)');
    });

    it('honours the writer\'s own bracket characters', function () {
        assertEqual(olBody('<m:oMath><m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr>' +
            '<m:e>' + omRun('n') + '</m:e></m:d></m:oMath>'),
            '\\left[n\\right]');
    });

    it('uses a full stop where the writer suppressed a bracket', function () {
        // \left and \right each need SOMETHING; "." is LaTeX for "nothing here".
        assertEqual(olBody('<m:oMath><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val=""/></m:dPr>' +
            '<m:e>' + omRun('n') + '</m:e></m:d></m:oMath>'),
            '\\left|n\\right.');
    });

    it('escapes curly braces used as delimiters', function () {
        assertEqual(olBody('<m:oMath><m:d><m:dPr><m:begChr m:val="{"/><m:endChr m:val="}"/></m:dPr>' +
            '<m:e>' + omRun('n') + '</m:e></m:d></m:oMath>'),
            '\\left\\{n\\right\\}');
    });

    it('converts a hidden-degree radical to \\sqrt', function () {
        assertEqual(olBody('<m:oMath><m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>' +
            '<m:deg/><m:e>' + omRun('16') + '</m:e></m:rad></m:oMath>'), '\\sqrt{16}');
    });

    it('converts a radical WITH a degree to \\sqrt[n]', function () {
        assertEqual(olBody('<m:oMath><m:rad><m:radPr/>' +
            '<m:deg>' + omRun('3') + '</m:deg><m:e>' + omRun('x') + '</m:e></m:rad></m:oMath>'),
            '\\sqrt[3]{x}');
    });

    it('converts an n-ary sum with both limits', function () {
        assertEqual(olBody('<m:oMath><m:nary><m:naryPr><m:chr m:val="∑"/></m:naryPr>' +
            '<m:sub>' + omRun('i=1') + '</m:sub><m:sup>' + omRun('n') + '</m:sup>' +
            '<m:e>' + omRun('x') + '</m:e></m:nary></m:oMath>'),
            '\\sum_{i=1}^{n}{x}');
    });

    it('converts a matrix', function () {
        var xml = '<m:oMath><m:m><m:mPr/>' +
            '<m:mr><m:e>' + omRun('a') + '</m:e><m:e>' + omRun('b') + '</m:e></m:mr>' +
            '<m:mr><m:e>' + omRun('c') + '</m:e><m:e>' + omRun('d') + '</m:e></m:mr>' +
            '</m:m></m:oMath>';
        assertEqual(olBody(xml), '\\begin{matrix}a & b \\\\ c & d\\end{matrix}');
    });

    it('recurses into an unrecognised construct instead of dropping it', function () {
        var out = olBody('<m:oMath><m:borderBox><m:e>' + omRun('E') + '</m:e></m:borderBox></m:oMath>');
        assert(out.indexOf('E') !== -1, 'content inside an unhandled element must still appear');
    });

    it('records an unrecognised element in the stats', function () {
        var conv = new OmmlToLatex();
        conv.convert(omXml('<m:oMath><m:notARealThing>' + omRun('E') +
            '</m:notARealThing></m:oMath>'));
        assertEqual(conv.stats.unknownElements.notARealThing, 1,
            'a new construct must surface in the stats, not disappear');
    });

    it('keeps a tracked insertion and drops a tracked deletion', function () {
        assertEqual(olBody('<m:oMath><w:ins>' + omRun('a') + '</w:ins>' +
            '<w:del>' + omRun('z') + '</w:del></m:oMath>'), 'a');
    });
});

describe('OMML -> LaTeX: inline vs display', function () {

    it('wraps a display equation in \\[ \\]', function () {
        var list = new OmmlToLatex().convertPara(omXml(
            '<m:oMathPara><m:oMathParaPr/><m:oMath>' + omRun('P=VI') + '</m:oMath></m:oMathPara>'));
        assertDeepEqual(list, ['\\[P=VI\\]']);
    });

    it('splits an <m:oMathPara> holding two equations', function () {
        var list = new OmmlToLatex().convertPara(omXml(
            '<m:oMathPara><m:oMathParaPr/>' +
            '<m:oMath>' + omRun('a') + '</m:oMath>' +
            '<m:oMath>' + omRun('b') + '</m:oMath></m:oMathPara>'));
        assertDeepEqual(list, ['\\[a\\]', '\\[b\\]']);
    });

    it('counts each equation once', function () {
        var conv = new OmmlToLatex();
        conv.convert(omXml('<m:oMath>' + omRun('a') + '</m:oMath>'));
        conv.convertPara(omXml('<m:oMathPara><m:oMath>' + omRun('b') + '</m:oMath>' +
            '<m:oMath>' + omRun('c') + '</m:oMath></m:oMathPara>'));
        assertEqual(conv.stats.equations, 3);
    });
});

describe('DocxParser: equations become runs', function () {

    function olParagraph(inner) {
        return omXml('<w:p><w:pPr/>' + inner + '</w:p>');
    }

    function olExtract(inner) {
        var parser = new DocxParser();
        var result = {
            runs: [], text: '', heading: null, listLevel: null,
            listNumId: null, listFormat: null, isListItem: false
        };
        parser._extractParagraphContent(olParagraph(inner), result);
        result.text = result.runs.map(function (r) { return r.text; }).join('');
        return { parser: parser, result: result };
    }

    it('picks up an equation that sits beside the ordinary runs', function () {
        var got = olExtract('<w:r><w:t>The formula is </w:t></w:r>' +
            '<m:oMath>' + omRun('E=mc') + '</m:oMath>');

        assertEqual(got.result.runs.length, 2, 'the prose run AND the equation must survive');
        assertEqual(got.result.runs[0].text, 'The formula is ');
        assertTrue(got.result.runs[1].isMath, 'the equation run must be flagged as maths');
        assertEqual(got.result.runs[1].text, '\\(E=mc\\)');
    });

    it('picks up a display equation wrapped in <m:oMathPara>', function () {
        var got = olExtract('<m:oMathPara><m:oMath>' + omRun('P=VI') + '</m:oMath></m:oMathPara>');

        assertEqual(got.result.runs.length, 1);
        assertTrue(got.result.runs[0].isMath);
        assertEqual(got.result.runs[0].text, '\\[P=VI\\]');
        assertEqual(got.parser.stats.mathEquations, 1, 'the equation must be counted');
    });

    it('counts every equation in a paragraph that holds several', function () {
        var got = olExtract('<m:oMathPara>' +
            '<m:oMath>' + omRun('a') + '</m:oMath>' +
            '<m:oMath>' + omRun('b') + '</m:oMath></m:oMathPara>' +
            '<m:oMath>' + omRun('c') + '</m:oMath>');
        assertEqual(got.parser.stats.mathEquations, 3);
        assertEqual(got.result.runs.length, 3);
        assertEqual(got.result.text, '\\[a\\]\\[b\\]\\(c\\)');
    });

    it('leaves a paragraph without an equation exactly as it was', function () {
        var got = olExtract('<w:r><w:t>ordinary prose</w:t></w:r>');
        assertEqual(got.result.runs.length, 1);
        assertEqual(got.result.runs[0].text, 'ordinary prose');
        assertEqual(got.result.runs[0].isMath, undefined,
            'a prose run must not grow a maths flag');
        assertEqual(got.parser.stats.mathEquations, 0);
    });
});

describe('OutputFormatter: the LaTeX passes through untouched', function () {

    function olMathRun(latex, fmt) {
        return { text: latex, isMath: true, formatting: fmt || {} };
    }
    function olProseRun(text, fmt) {
        return { text: text, formatting: fmt || {}, hyperlink: null };
    }
    function olPara(runs) {
        return {
            runs: runs, text: runs.map(function (r) { return r.text; }).join(''),
            heading: null, listLevel: null, listNumId: null,
            listFormat: null, isListItem: false
        };
    }

    var SAMPLE = '\\[c=\\frac{\\Delta E}{m\\times\\Delta T}\\]';

    it('emits an equation-only paragraph as the LaTeX itself', function () {
        assertEqual(new OutputFormatter().formatParagraph(olPara([olMathRun(SAMPLE)])), SAMPLE);
    });

    it('keeps the equation inline with the prose around it', function () {
        var out = new OutputFormatter().formatParagraph(olPara([
            olProseRun('so '), olMathRun('\\(E=mc\\)'), olProseRun(' follows')
        ]));
        assertEqual(out, 'so \\(E=mc\\) follows');
    });

    it('does not wrap the LaTeX in bold or italic markers', function () {
        var out = new OutputFormatter().formatParagraph(olPara([
            olMathRun(SAMPLE, { bold: true, italic: true })
        ]));
        assertEqual(out, SAMPLE, 'a ** around \\frac would corrupt the equation');
    });

    it('does not trim the backslashes or braces at the edges', function () {
        var out = new OutputFormatter().formatParagraph(olPara([olMathRun('\\(x\\)')]));
        assertEqual(out, '\\(x\\)');
    });

    it('does not add the yellow-highlight tick to an equation', function () {
        var out = new OutputFormatter().formatParagraph(olPara([
            olMathRun(SAMPLE, { highlight: 'yellow' })
        ]));
        assertEqual(out.indexOf('✅'), -1);
    });

    it('leaves a paragraph without an equation byte-identical', function () {
        var out = new OutputFormatter().formatParagraph(olPara([
            olProseRun('plain ', {}), olProseRun('bold', { bold: true })
        ]));
        assertEqual(out, 'plain **bold**');
    });

    it('carries an equation through a list item', function () {
        var para = olPara([olMathRun(SAMPLE)]);
        para.isListItem = true;
        para.listLevel = 0;
        para.listFormat = 'bullet';
        assertEqual(new OutputFormatter().formatParagraph(para), '• ' + SAMPLE);
    });
});
