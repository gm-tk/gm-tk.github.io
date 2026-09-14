/**
 * OmmlToMathml — turns a Word equation (OMML) into MathML.
 *
 * WHY THIS EXISTS
 * Word stores equations as Office Math Markup (OMML): <m:oMath> (inline) and
 * <m:oMathPara> (its own line) elements that sit BESIDE the ordinary <w:r> runs
 * inside a <w:p>. DocxParser's run walk only knew about <w:r>, <w:hyperlink>,
 * <w:ins>/<w:del> and <w:sdt>, so every equation fell straight through the gap
 * and never reached the parsed .txt — the writer's formula was simply absent,
 * with no marker left behind to say something had been lost.
 *
 * OUTPUT SHAPE
 * A bare `<math xmlns="http://www.w3.org/1998/Math/MathML">…</math>`, which is
 * what the human developers hand-wrote in the finished modules: 1822 of the
 * ~2009 <math> tags across 01-Finalized_Modules_ are exactly that form (105 add
 * display="inline", 66 display="block"). Emitting it verbatim lets the
 * downstream HTML build pass the equation through untouched.
 *
 * COVERAGE
 * Measured over the 26 Writers Templates whose finished HTML carries real
 * MathML: 8 of them ship OMML (MXDB301, MXDI102, MXDI301, MXEX301, MXFU302,
 * MXFU401, PES1007, PES1008 — 315 equations). Their whole vocabulary is
 * m:r/m:t, m:f, m:d, m:sSup, m:sSub and m:rad. The rest of the OMML grammar
 * (n-ary, radicals with degrees, matrices, accents, limits, function
 * application) is implemented anyway so a future template cannot reintroduce
 * the silent-drop bug, and any element still unrecognised is recursed into as
 * an <mrow> rather than discarded.
 *
 * HEADLESS-TESTABLE
 * The walk touches only childNodes / nodeType / localName / textContent /
 * getAttribute(NS), so plain objects stand in for DOM nodes under the Node test
 * runner. No DOM API is constructed here — the output is a string.
 */

'use strict';

class OmmlToMathml {

    constructor() {
        /** MathML namespace emitted on every <math> element. */
        this.MATH_NS = 'http://www.w3.org/1998/Math/MathML';

        /** Office Math Markup namespace. */
        this.M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math';

        /** WordprocessingML namespace (tracked changes / run properties). */
        this.W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main';

        /** @type {Object} Conversion statistics (surfaced through DocxParser.stats). */
        this.stats = {
            equations: 0,
            unknownElements: {}
        };
    }

    // ------------------------------------------------------------------
    // Public API
    // ------------------------------------------------------------------

    /**
     * Convert one <m:oMath> element into a complete `<math>…</math>` string.
     * @param {Node} oMathEl
     * @returns {string}
     */
    convert(oMathEl) {
        const body = this._seq(oMathEl);
        this.stats.equations++;
        return '<math xmlns="' + this.MATH_NS + '">' + body + '</math>';
    }

    /**
     * Convert an <m:oMathPara> wrapper: it holds one or more <m:oMath>
     * children (Word puts several display equations on one line this way).
     * @param {Node} oMathParaEl
     * @returns {Array<string>} one `<math>…</math>` string per equation
     */
    convertPara(oMathParaEl) {
        const out = [];
        const kids = this._elementChildren(oMathParaEl);
        for (let i = 0; i < kids.length; i++) {
            if (kids[i].localName === 'oMath') {
                out.push(this.convert(kids[i]));
            }
        }
        return out;
    }

    /** True when the element is an OMML equation root this class handles. */
    static isMathRoot(el) {
        return !!el && (el.localName === 'oMath' || el.localName === 'oMathPara');
    }

    // ------------------------------------------------------------------
    // Internal: element dispatch
    // ------------------------------------------------------------------

    /** Convert every element child of `node` in order and join the results. */
    _seq(node) {
        const kids = this._elementChildren(node);
        let out = '';
        for (let i = 0; i < kids.length; i++) {
            out += this._element(kids[i]);
        }
        return out;
    }

    /** Convert the children of `node` wrapped in a single <mrow>. */
    _row(node) {
        return '<mrow>' + this._seq(node) + '</mrow>';
    }

    /** Convert a named child (or the empty <mrow> when it is absent). */
    _rowOf(node, name) {
        const el = this._childByName(node, name);
        return el ? this._row(el) : '<mrow></mrow>';
    }

    _element(el) {
        const name = el.localName;

        // Property elements carry formatting Word needs and MathML does not.
        if (OmmlToMathml.SKIPPED[name]) { return ''; }

        switch (name) {
            case 'r':          return this._run(el);
            case 't':          return this._tokensToMathml(this._tokenise(el.textContent || ''));
            case 'f':          return this._fraction(el);
            case 'd':          return this._delimiter(el);
            case 'sSup':       return '<msup>' + this._rowOf(el, 'e') + this._rowOf(el, 'sup') + '</msup>';
            case 'sSub':       return '<msub>' + this._rowOf(el, 'e') + this._rowOf(el, 'sub') + '</msub>';
            case 'sSubSup':    return '<msubsup>' + this._rowOf(el, 'e') + this._rowOf(el, 'sub') +
                                      this._rowOf(el, 'sup') + '</msubsup>';
            case 'sPre':       return '<mmultiscripts>' + this._rowOf(el, 'e') + '<mprescripts/>' +
                                      this._rowOf(el, 'sub') + this._rowOf(el, 'sup') + '</mmultiscripts>';
            case 'rad':        return this._radical(el);
            case 'nary':       return this._nary(el);
            case 'func':       return '<mrow>' + this._rowOf(el, 'fName') + '<mo>&#x2061;</mo>' +
                                      this._rowOf(el, 'e') + '</mrow>';
            case 'bar':        return this._bar(el);
            case 'acc':        return this._accent(el);
            case 'groupChr':   return this._groupChr(el);
            case 'limLow':     return '<munder>' + this._rowOf(el, 'e') + this._rowOf(el, 'lim') + '</munder>';
            case 'limUpp':     return '<mover>' + this._rowOf(el, 'e') + this._rowOf(el, 'lim') + '</mover>';
            case 'm':          return this._matrix(el);
            case 'eqArr':      return this._eqArray(el);
            case 'oMath':      return this._seq(el);   // nested equation: flatten
            case 'br':         return '';              // a line break inside an equation
            case 'ins':        return this._seq(el);   // tracked insertion: keep the content
            case 'del':        return '';              // tracked deletion: drop it
            case 'e':
            case 'num':
            case 'den':
            case 'lim':
            case 'sub':
            case 'sup':
            case 'deg':
            case 'fName':
            case 'box':
            case 'borderBox':
            case 'phant':
                return this._row(el);
            default:
                // Never drop content: recurse into anything unrecognised and
                // record it, so a new construct shows up in the stats instead
                // of silently disappearing the way whole equations used to.
                this.stats.unknownElements[name] = (this.stats.unknownElements[name] || 0) + 1;
                return this._row(el);
        }
    }

    // ------------------------------------------------------------------
    // Internal: individual constructs
    // ------------------------------------------------------------------

    /** <m:r> — a text run inside an equation. */
    _run(rEl) {
        let text = '';
        const kids = this._elementChildren(rEl);
        for (let i = 0; i < kids.length; i++) {
            const name = kids[i].localName;
            if (name === 't') {
                text += kids[i].textContent || '';
            } else if (name === 'br') {
                text += ' ';
            } else if (name === 'tab') {
                text += ' ';
            }
        }
        if (text === '') { return ''; }

        // <m:nor/> in the run properties means "this is literal text, not
        // mathematical notation" — Word renders it upright and unitalicised.
        const rPr = this._childByName(rEl, 'rPr');
        if (rPr && this._childByName(rPr, 'nor')) {
            return '<mtext>' + this._escapeText(text) + '</mtext>';
        }

        return this._tokensToMathml(this._tokenise(text));
    }

    /** <m:f> — a fraction. */
    _fraction(fEl) {
        const type = this._propVal(fEl, 'fPr', 'type');
        const num = this._rowOf(fEl, 'num');
        const den = this._rowOf(fEl, 'den');

        if (type === 'lin') {
            return '<mrow>' + num + '<mo>/</mo>' + den + '</mrow>';
        }
        if (type === 'noBar') {
            // A "no bar" fraction is Word's binomial coefficient.
            return '<mfrac linethickness="0">' + num + den + '</mfrac>';
        }
        return '<mfrac>' + num + den + '</mfrac>';
    }

    /** <m:d> — a delimited group: brackets, absolute-value bars, and so on. */
    _delimiter(dEl) {
        const dPr = this._childByName(dEl, 'dPr');
        const beg = this._attrOr(dPr, 'begChr', '(');
        const end = this._attrOr(dPr, 'endChr', ')');
        const sep = this._attrOr(dPr, 'sepChr', ',');

        const args = this._childrenByName(dEl, 'e');
        let out = '<mrow>';
        if (beg !== '') { out += '<mo>' + this._escapeText(beg) + '</mo>'; }
        for (let i = 0; i < args.length; i++) {
            if (i > 0 && sep !== '') { out += '<mo>' + this._escapeText(sep) + '</mo>'; }
            out += this._row(args[i]);
        }
        if (end !== '') { out += '<mo>' + this._escapeText(end) + '</mo>'; }
        return out + '</mrow>';
    }

    /** <m:rad> — a square root, or an n-th root when a degree is present. */
    _radical(radEl) {
        const radPr = this._childByName(radEl, 'radPr');
        const hidden = !!(radPr && this._childByName(radPr, 'degHide'));
        const deg = this._childByName(radEl, 'deg');
        const degBody = deg ? this._seq(deg) : '';

        if (hidden || degBody === '') {
            return '<msqrt>' + this._rowOf(radEl, 'e') + '</msqrt>';
        }
        return '<mroot>' + this._rowOf(radEl, 'e') + '<mrow>' + degBody + '</mrow></mroot>';
    }

    /** <m:nary> — a summation / product / integral with optional limits. */
    _nary(naryEl) {
        const naryPr = this._childByName(naryEl, 'naryPr');
        const chr = this._attrOr(naryPr, 'chr', '∫');           // default: integral
        const subHide = !!(naryPr && this._childByName(naryPr, 'subHide'));
        const supHide = !!(naryPr && this._childByName(naryPr, 'supHide'));
        const op = '<mo>' + this._escapeText(chr) + '</mo>';

        // Integrals carry their limits beside the sign; sums and products above
        // and below it.
        const beside = '∫∬∭∮'.indexOf(chr) !== -1;
        const under = beside ? 'msub' : 'munder';
        const over = beside ? 'msup' : 'mover';
        const both = beside ? 'msubsup' : 'munderover';

        let head;
        if (subHide && supHide) {
            head = op;
        } else if (supHide) {
            head = '<' + under + '>' + op + this._rowOf(naryEl, 'sub') + '</' + under + '>';
        } else if (subHide) {
            head = '<' + over + '>' + op + this._rowOf(naryEl, 'sup') + '</' + over + '>';
        } else {
            head = '<' + both + '>' + op + this._rowOf(naryEl, 'sub') +
                this._rowOf(naryEl, 'sup') + '</' + both + '>';
        }
        return '<mrow>' + head + this._rowOf(naryEl, 'e') + '</mrow>';
    }

    /** <m:bar> — an overbar or underbar. */
    _bar(barEl) {
        const pos = this._propVal(barEl, 'barPr', 'pos');
        if (pos === 'top') {
            return '<mover accent="true">' + this._rowOf(barEl, 'e') + '<mo>&#xAF;</mo></mover>';
        }
        return '<munder accentunder="true">' + this._rowOf(barEl, 'e') + '<mo>&#x5F;</mo></munder>';
    }

    /** <m:acc> — an accent (hat, tilde, vector arrow, …). */
    _accent(accEl) {
        const chr = this._attrOr(this._childByName(accEl, 'accPr'), 'chr', '̂');
        return '<mover accent="true">' + this._rowOf(accEl, 'e') +
            '<mo>' + this._escapeText(chr) + '</mo></mover>';
    }

    /** <m:groupChr> — a brace or arrow grouping the expression. */
    _groupChr(gEl) {
        const gPr = this._childByName(gEl, 'groupChrPr');
        const chr = this._attrOr(gPr, 'chr', '⏟');
        const pos = this._propVal(gEl, 'groupChrPr', 'pos');
        const tag = pos === 'top' ? 'mover' : 'munder';
        return '<' + tag + '>' + this._rowOf(gEl, 'e') +
            '<mo>' + this._escapeText(chr) + '</mo></' + tag + '>';
    }

    /** <m:m> — a matrix. */
    _matrix(mEl) {
        const rows = this._childrenByName(mEl, 'mr');
        let out = '<mtable>';
        for (let i = 0; i < rows.length; i++) {
            const cells = this._childrenByName(rows[i], 'e');
            out += '<mtr>';
            for (let c = 0; c < cells.length; c++) {
                out += '<mtd>' + this._seq(cells[c]) + '</mtd>';
            }
            out += '</mtr>';
        }
        return out + '</mtable>';
    }

    /** <m:eqArr> — a stack of aligned equations. */
    _eqArray(eqEl) {
        const rows = this._childrenByName(eqEl, 'e');
        let out = '<mtable>';
        for (let i = 0; i < rows.length; i++) {
            out += '<mtr><mtd>' + this._seq(rows[i]) + '</mtd></mtr>';
        }
        return out + '</mtable>';
    }

    // ------------------------------------------------------------------
    // Internal: run text -> MathML tokens
    // ------------------------------------------------------------------

    /**
     * Split a run's text into number / operator / word / space tokens.
     * A number keeps its internal decimal point and thousands commas
     * ("504,000" and "1.5" are one token each, not three).
     */
    _tokenise(text) {
        const out = [];
        let i = 0;
        while (i < text.length) {
            const ch = text.charAt(i);

            if (OmmlToMathml._isSpace(ch)) {
                out.push({ kind: 'space', text: ch });
                i++;
            } else if (OmmlToMathml._isDigit(ch)) {
                let j = i + 1;
                while (j < text.length) {
                    if (OmmlToMathml._isDigit(text.charAt(j))) { j++; continue; }
                    const sep = text.charAt(j);
                    if ((sep === '.' || sep === ',') && OmmlToMathml._isDigit(text.charAt(j + 1))) {
                        j += 2;
                        continue;
                    }
                    break;
                }
                out.push({ kind: 'number', text: text.slice(i, j) });
                i = j;
            } else if (OmmlToMathml.OPERATORS.indexOf(ch) !== -1) {
                out.push({ kind: 'op', text: ch });
                i++;
            } else {
                let j = i;
                while (j < text.length) {
                    const c = text.charAt(j);
                    if (OmmlToMathml._isSpace(c) || OmmlToMathml._isDigit(c) ||
                        OmmlToMathml.OPERATORS.indexOf(c) !== -1) { break; }
                    j++;
                }
                out.push({ kind: 'word', text: text.slice(i, j) });
                i = j;
            }
        }
        return out;
    }

    /**
     * Turn tokens into MathML token elements, following the convention the
     * human developers used in the finished modules: a single letter is a
     * variable (<mi>), a word is prose (<mtext>, with neighbouring words and
     * the spaces between them kept in one element), digits are <mn> and
     * everything else is an operator (<mo>).
     */
    _tokensToMathml(tokens) {
        const isProse = this._classifyWords(tokens);
        let out = '';
        let buffer = '';

        const flush = () => {
            if (buffer !== '') {
                out += '<mtext>' + this._escapeText(this._protectEdgeSpaces(buffer)) + '</mtext>';
                buffer = '';
            }
        };

        for (let i = 0; i < tokens.length; i++) {
            const tok = tokens[i];

            if (tok.kind === 'space') {
                // A space only survives as part of the prose it sits inside.
                if (buffer !== '') { buffer += ' '; }
            } else if (tok.kind === 'word') {
                if (isProse[i]) {
                    buffer += tok.text;
                } else {
                    // A run of variables: each letter is its own <mi>.
                    flush();
                    for (let c = 0; c < tok.text.length; c++) {
                        out += '<mi>' + this._escapeText(tok.text.charAt(c)) + '</mi>';
                    }
                }
            } else if (tok.kind === 'number') {
                flush();
                out += '<mn>' + this._escapeText(tok.text) + '</mn>';
            } else {
                flush();
                out += '<mo>' + this._escapeText(tok.text) + '</mo>';
            }
        }
        flush();
        return out;
    }


    /**
     * Decide, for each token, whether a word is PROSE or a run of VARIABLES.
     * Word gives us no signal — "specific heat capacity" and "mc" are both just
     * letters in an equation run — so this is the rule:
     *
     *   - one letter  -> always a variable ("c", "J", "x")
     *   - 3 or more   -> prose ("mass", "Temperature", "specific")
     *   - exactly two -> a variable pair ("mc", "VI", "IR", "Pt") UNLESS it sits
     *                    a single space away from a word of 3+ letters, which
     *                    makes it part of a phrase ("amount OF heat energy")
     *
     * Measured against the equations in PES1007/PES1008/MXFU401: it puts every
     * phrase in prose and every variable product in maths.
     */
    _classifyWords(tokens) {
        const prose = [];
        for (let i = 0; i < tokens.length; i++) {
            const tok = tokens[i];
            if (tok.kind !== 'word') { prose.push(false); continue; }
            if (tok.text.length === 1) { prose.push(false); continue; }
            if (tok.text.length >= 3) { prose.push(true); continue; }
            prose.push(this._hasPhraseNeighbour(tokens, i));
        }
        return prose;
    }

    /** True when a word of 3+ letters sits one space away, either side. */
    _hasPhraseNeighbour(tokens, i) {
        const long = function (t) { return t && t.kind === 'word' && t.text.length >= 3; };
        const before = i >= 2 && tokens[i - 1].kind === 'space' && long(tokens[i - 2]);
        const after = i + 2 < tokens.length && tokens[i + 1].kind === 'space' && long(tokens[i + 2]);
        return before || after;
    }

    // ------------------------------------------------------------------
    // Internal: node + attribute helpers (DOM-shaped, but duck-typed so the
    // headless test runner can pass plain objects)
    // ------------------------------------------------------------------

    _elementChildren(node) {
        const out = [];
        const kids = (node && node.childNodes) ? node.childNodes : [];
        for (let i = 0; i < kids.length; i++) {
            if (kids[i] && kids[i].nodeType === 1) { out.push(kids[i]); }
        }
        return out;
    }

    _childByName(node, name) {
        const kids = this._elementChildren(node);
        for (let i = 0; i < kids.length; i++) {
            if (kids[i].localName === name) { return kids[i]; }
        }
        return null;
    }

    _childrenByName(node, name) {
        const kids = this._elementChildren(node);
        const out = [];
        for (let i = 0; i < kids.length; i++) {
            if (kids[i].localName === name) { out.push(kids[i]); }
        }
        return out;
    }

    /** Read the m:val attribute off an element, whatever namespace shape it has. */
    _val(el) {
        if (!el) { return null; }
        let v = null;
        if (typeof el.getAttributeNS === 'function') {
            v = el.getAttributeNS(this.M_NS, 'val');
            if (v === null || v === '') {
                const w = el.getAttributeNS(this.W_NS, 'val');
                if (w !== null && w !== '') { v = w; }
            }
        }
        if ((v === null || v === '') && typeof el.getAttribute === 'function') {
            const raw = el.getAttribute('m:val') || el.getAttribute('w:val');
            if (raw !== null && raw !== undefined && raw !== '') { v = raw; }
        }
        return v;
    }

    /**
     * Read a child's m:val, falling back to `fallback` only when the child is
     * absent. An explicitly empty value ("no bracket here") is honoured.
     */
    _attrOr(propsEl, childName, fallback) {
        const child = this._childByName(propsEl, childName);
        if (!child) { return fallback; }
        const v = this._val(child);
        return (v === null || v === undefined) ? '' : v;
    }

    /** Read `<parent><propsName><childName m:val="…"/></propsName></parent>`. */
    _propVal(el, propsName, childName) {
        const props = this._childByName(el, propsName);
        if (!props) { return null; }
        return this._val(this._childByName(props, childName));
    }

    /**
     * A leading or trailing plain space inside <mtext> is collapsed away by
     * MathML renderers, so it becomes a non-breaking space — the same thing the
     * human developers wrote by hand ("specific heat capacity&nbsp;").
     */
    _protectEdgeSpaces(text) {
        return text
            .replace(/^ +/, function (m) { return new Array(m.length + 1).join('\u00A0'); })
            .replace(/ +$/, function (m) { return new Array(m.length + 1).join('\u00A0'); });
    }

    _escapeText(text) {
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\u00A0/g, '&#xA0;');
    }

    static _isDigit(ch) { return ch >= '0' && ch <= '9'; }

    /**
     * Whitespace, as Word actually writes it inside an equation. It does not
     * stop at a plain space: the equation editor sprinkles typographic spaces
     * (U+2008 PUNCTUATION SPACE, U+2009 THIN SPACE, U+00A0 NO-BREAK SPACE) into
     * the runs it builds. `\s` covers every one of those; U+200B ZERO WIDTH
     * SPACE is the only gap it leaves.
     */
    static _isSpace(ch) {
        return /\s/.test(ch) || ch === '\u200B';
    }
}

/**
 * Characters that become <mo>. Everything not in here, not a digit and not
 * whitespace is treated as a letter, so Greek variables, macronised vowels and
 * unit symbols (℃) come through as <mi> without needing a Unicode property
 * escape. The two deltas are operators because that is what the human
 * developers wrote (45 <mo>Δ</mo> across the finished modules).
 */
OmmlToMathml.OPERATORS =
    '=+-−±×÷*/<>≤≥≠≈∝' +
    '→←↔⇒⇔' +
    '·∙∘∅∆Δ∂' +
    '()[]{}|,;:!?%^~′″';

/** Word-only property elements: they describe formatting MathML does not carry. */
OmmlToMathml.SKIPPED = {
    ctrlPr: true, rPr: true, fPr: true, dPr: true, sSupPr: true, sSubPr: true,
    sSubSupPr: true, sPrePr: true, radPr: true, naryPr: true, funcPr: true,
    barPr: true, accPr: true, limLowPr: true, limUppPr: true, groupChrPr: true,
    mPr: true, mrPr: true, eqArrPr: true, boxPr: true, borderBoxPr: true,
    phantPr: true, argPr: true, oMathParaPr: true, bookmarkStart: true,
    bookmarkEnd: true, proofErr: true, lastRenderedPageBreak: true
};

// Node (test runner) export; harmless in the browser.
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OmmlToMathml;
}
