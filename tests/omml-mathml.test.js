/**
 * Tests for OmmlToMathml — Word equations (OMML) converted to MathML.
 *
 * This converter is NOT in the parse path: the parser emits LaTeX (see
 * tests/omml-latex.test.js and js/omml-to-latex.js), because Creative Services
 * asks writers to author their equations as LaTeX in the first place. MathML is
 * kept as the deterministic alternative for the day the downstream LaTeX ->
 * markup step needs replacing with code, so it stays covered.
 *
 * Fixtures (omXml / omRun) come from tests/omml-fixtures.js.
 */

'use strict';

function omConvert(xml) {
    return new OmmlToMathml().convert(omXml(xml));
}

var OM_MATH_OPEN = '<math xmlns="http://www.w3.org/1998/Math/MathML">';

describe('OMML -> MathML: token conventions', function () {

    it('emits a bare <math> element with the MathML namespace', function () {
        var out = omConvert('<m:oMath>' + omRun('x') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<mi>x</mi></math>',
            'the wrapper must match the form the finished modules use');
    });

    it('splits a run into variables, numbers and operators', function () {
        var out = omConvert('<m:oMath>' + omRun('∆E=m×c×∆T') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN +
            '<mo>∆</mo><mi>E</mi><mo>=</mo><mi>m</mi><mo>×</mo><mi>c</mi><mo>×</mo>' +
            '<mo>∆</mo><mi>T</mi></math>');
    });

    it('keeps prose inside an equation as one <mtext>', function () {
        // The trailing space becomes a non-breaking space because a MathML
        // renderer collapses a plain one at the edge of an <mtext> -- the same
        // thing the human developers wrote by hand in PES1008.
        var out = omConvert('<m:oMath>' + omRun('specific heat capacity c=') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN +
            '<mtext>specific heat capacity&#xA0;</mtext><mi>c</mi><mo>=</mo></math>');
    });

    it('treats a short letter run as variables, not prose', function () {
        var out = omConvert('<m:oMath>' + omRun('E=mc') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<mi>E</mi><mo>=</mo><mi>m</mi><mi>c</mi></math>',
            '"mc" is m times c, not the word "mc"');
    });

    it('keeps a two-letter word inside the phrase it belongs to', function () {
        var out = omConvert('<m:oMath>' + omRun('amount of heat energy') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<mtext>amount of heat energy</mtext></math>');
    });

    it('treats the typographic spaces Word inserts as whitespace', function () {
        var out = omConvert('<m:oMath>' + omRun('2\u2008') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<mn>2</mn></math>',
            "Word's U+2008 punctuation space is whitespace, not a character");
    });

    it('keeps a thousands separator inside one number', function () {
        var out = omConvert('<m:oMath>' + omRun('504,000') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<mn>504,000</mn></math>');
    });

    it('keeps a decimal point inside one number', function () {
        var out = omConvert('<m:oMath>' + omRun('1.5×4200') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<mn>1.5</mn><mo>×</mo><mn>4200</mn></math>');
    });

    it('escapes characters that would otherwise break the markup', function () {
        var out = omConvert('<m:oMath>' + omRun('a&amp;b &lt;c&gt;') + '</m:oMath>');
        assert(out.indexOf('&amp;') !== -1, 'the ampersand must stay escaped');
        assert(out.indexOf('<mo>&lt;</mo>') !== -1 && out.indexOf('<mo>&gt;</mo>') !== -1,
            'a less-than / greater-than sign must become an escaped operator');
        assert(!/&(?!amp;|lt;|gt;|#xA0;)/.test(out),
            'no raw ampersand may survive into the markup');
    });

    it('ignores the Word-only property elements', function () {
        var out = omConvert('<m:oMath><m:ctrlPr><w:rPr><w:i/></w:rPr></m:ctrlPr>' +
            omRun('y') + '</m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<mi>y</mi></math>',
            'ctrlPr / rPr carry Word formatting MathML does not have');
    });
});

describe('OMML -> MathML: the constructs the corpus contains', function () {

    it('converts a fraction to <mfrac>', function () {
        var out = omConvert('<m:oMath><m:f><m:fPr><m:ctrlPr/></m:fPr>' +
            '<m:num>' + omRun('∆E') + '</m:num>' +
            '<m:den>' + omRun('m×∆T') + '</m:den></m:f></m:oMath>');
        assertEqual(out, OM_MATH_OPEN +
            '<mfrac><mrow><mo>∆</mo><mi>E</mi></mrow>' +
            '<mrow><mi>m</mi><mo>×</mo><mo>∆</mo><mi>T</mi></mrow></mfrac></math>');
    });

    it('converts a superscript to <msup>', function () {
        var out = omConvert('<m:oMath><m:sSup><m:sSupPr><m:ctrlPr/></m:sSupPr>' +
            '<m:e>' + omRun('v') + '</m:e><m:sup>' + omRun('2') + '</m:sup></m:sSup></m:oMath>');
        assertEqual(out, OM_MATH_OPEN +
            '<msup><mrow><mi>v</mi></mrow><mrow><mn>2</mn></mrow></msup></math>');
    });

    it('converts a subscript to <msub>', function () {
        var out = omConvert('<m:oMath><m:sSub><m:sSubPr><m:ctrlPr/></m:sSubPr>' +
            '<m:e>' + omRun('E') + '</m:e><m:sub>' + omRun('k') + '</m:sub></m:sSub></m:oMath>');
        assertEqual(out, OM_MATH_OPEN +
            '<msub><mrow><mi>E</mi></mrow><mrow><mi>k</mi></mrow></msub></math>');
    });

    it('wraps a delimiter group in round brackets by default', function () {
        var out = omConvert('<m:oMath><m:d><m:dPr><m:ctrlPr/></m:dPr>' +
            '<m:e>' + omRun('100-20') + '</m:e></m:d></m:oMath>');
        assertEqual(out, OM_MATH_OPEN +
            '<mrow><mo>(</mo><mrow><mn>100</mn><mo>-</mo><mn>20</mn></mrow><mo>)</mo></mrow></math>');
    });

    it('honours the writer\'s own bracket characters', function () {
        var out = omConvert('<m:oMath><m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr>' +
            '<m:e>' + omRun('n') + '</m:e></m:d></m:oMath>');
        assert(out.indexOf('<mo>[</mo>') !== -1, 'the opening bracket must be the one Word stored');
        assert(out.indexOf('<mo>]</mo>') !== -1);
    });

    it('emits no bracket when the writer suppressed one', function () {
        var out = omConvert('<m:oMath><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val=""/></m:dPr>' +
            '<m:e>' + omRun('n') + '</m:e></m:d></m:oMath>');
        assert(out.indexOf('<mo>|</mo>') !== -1);
        assert(out.indexOf('<mo></mo>') === -1, 'an empty end character must produce no <mo>');
    });

    it('converts a hidden-degree radical to <msqrt>', function () {
        var out = omConvert('<m:oMath><m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>' +
            '<m:deg/><m:e>' + omRun('16') + '</m:e></m:rad></m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<msqrt><mrow><mn>16</mn></mrow></msqrt></math>');
    });

    it('converts a radical WITH a degree to <mroot>', function () {
        var out = omConvert('<m:oMath><m:rad><m:radPr/>' +
            '<m:deg>' + omRun('3') + '</m:deg><m:e>' + omRun('x') + '</m:e></m:rad></m:oMath>');
        assertEqual(out, OM_MATH_OPEN +
            '<mroot><mrow><mi>x</mi></mrow><mrow><mn>3</mn></mrow></mroot></math>');
    });

    it('converts an n-ary sum with both limits', function () {
        var out = omConvert('<m:oMath><m:nary><m:naryPr><m:chr m:val="∑"/></m:naryPr>' +
            '<m:sub>' + omRun('i=1') + '</m:sub><m:sup>' + omRun('n') + '</m:sup>' +
            '<m:e>' + omRun('x') + '</m:e></m:nary></m:oMath>');
        assert(out.indexOf('<munderover><mo>∑</mo>') !== -1,
            'a sum carries its limits above and below the sign');
    });

    it('recurses into an unrecognised construct instead of dropping it', function () {
        var out = omConvert('<m:oMath><m:borderBox><m:e>' + omRun('E') + '</m:e></m:borderBox></m:oMath>');
        assert(out.indexOf('<mi>E</mi>') !== -1,
            'content inside an unhandled element must still reach the output');
    });

    it('records an unrecognised element in the stats', function () {
        var conv = new OmmlToMathml();
        conv.convert(omXml('<m:oMath><m:notARealThing>' + omRun('E') +
            '</m:notARealThing></m:oMath>'));
        assertEqual(conv.stats.unknownElements.notARealThing, 1,
            'a new construct must surface in the stats, not disappear');
    });

    it('splits an <m:oMathPara> holding two equations', function () {
        var list = new OmmlToMathml().convertPara(omXml(
            '<m:oMathPara><m:oMathParaPr/>' +
            '<m:oMath>' + omRun('a') + '</m:oMath>' +
            '<m:oMath>' + omRun('b') + '</m:oMath></m:oMathPara>'));
        assertEqual(list.length, 2);
        assertEqual(list[0], OM_MATH_OPEN + '<mi>a</mi></math>');
        assertEqual(list[1], OM_MATH_OPEN + '<mi>b</mi></math>');
    });

    it('keeps a tracked insertion and drops a tracked deletion', function () {
        var out = omConvert('<m:oMath><w:ins>' + omRun('a') + '</w:ins>' +
            '<w:del>' + omRun('z') + '</w:del></m:oMath>');
        assertEqual(out, OM_MATH_OPEN + '<mi>a</mi></math>');
    });
});
