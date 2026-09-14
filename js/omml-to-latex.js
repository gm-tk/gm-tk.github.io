/**
 * OmmlToLatex — turns a Word equation (OMML) into LaTeX.
 *
 * WHY LATEX AND NOT MATHML
 * Creative Services' instruction to writers (Persephone Samuels, 26 Aug 2026) is:
 * screenshot the equation, ask an AI to "convert the equation in this image to
 * latex for word", paste the LaTeX into Word, then press Alt + = so Word turns
 * it into a real equation. That last keystroke CONSUMES the LaTeX — Word stores
 * OMML and keeps no copy of what was typed, so the writer's LaTeX cannot be
 * "retained", only regenerated. Regenerating it here gives the parsed .txt a
 * single carrier for maths: LaTeX, whether the writer pressed Alt + = or left
 * their LaTeX sitting in the paragraph as plain text. The downstream Convertor
 * project then has exactly one job — LaTeX to the page's maths markup — which is
 * what its COMP_12 "MathJax / Equations" rule already describes.
 *
 * OUTPUT SHAPE
 * `\(…\)` for an equation sitting inline in a sentence (<m:oMath>) and `\[…\]`
 * for one the writer put on its own line (<m:oMathPara>) — the delimiters the
 * Convertor knowledge base already specifies. Word records which of the two the
 * writer chose, so we do not have to guess.
 *
 * A symbol command is always emitted with a trailing space (`\times 4200`,
 * `\Delta E`) because `\DeltaE` would read as one unknown command. Runs of
 * spaces are collapsed and the result trimmed, so the spacing stays tidy.
 *
 * COVERAGE
 * Same vocabulary as the MathML converter: measured across the 8 Writers
 * Templates that actually ship OMML (MXDB301, MXDI102, MXDI301, MXEX301,
 * MXFU302, MXFU401, PES1007, PES1008 — 315 equations), the whole grammar in use
 * is m:r/m:t, m:f, m:d, m:sSup, m:sSub and m:rad. The rest of the common OMML
 * grammar is implemented anyway, and anything still unrecognised is recursed
 * into rather than dropped — a silent drop is the bug this exists to prevent.
 *
 * HEADLESS-TESTABLE
 * The walk touches only childNodes / nodeType / localName / textContent /
 * getAttribute(NS), so plain objects stand in for DOM nodes under the Node test
 * runner. The output is a string; no DOM is constructed.
 */

'use strict';

class OmmlToLatex {

    constructor() {
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

    /** Convert one <m:oMath> into an inline `\(…\)` equation. */
    convert(oMathEl) {
        this.stats.equations++;
        return '\\(' + this.convertBody(oMathEl) + '\\)';
    }

    /**
     * Convert an <m:oMathPara> wrapper into display `\[…\]` equations. Word puts
     * several display equations on one line this way, so this returns a list.
     * @returns {Array<string>}
     */
    convertPara(oMathParaEl) {
        const out = [];
        const kids = this._elementChildren(oMathParaEl);
        for (let i = 0; i < kids.length; i++) {
            if (kids[i].localName !== 'oMath') { continue; }
            this.stats.equations++;
            out.push('\\[' + this.convertBody(kids[i]) + '\\]');
        }
        return out;
    }

    /** The LaTeX for an equation's contents, without delimiters. */
    convertBody(oMathEl) {
        return this._tidy(this._seq(oMathEl));
    }

    /** True when the element is an OMML equation root this class handles. */
    static isMathRoot(el) {
        return !!el && (el.localName === 'oMath' || el.localName === 'oMathPara');
    }

    // ------------------------------------------------------------------
    // Internal: element dispatch
    // ------------------------------------------------------------------

    _seq(node) {
        const kids = this._elementChildren(node);
        let out = '';
        for (let i = 0; i < kids.length; i++) {
            out += this._element(kids[i]);
        }
        return out;
    }

    /** Convert a named child into a `{…}` LaTeX group. */
    _group(node, name) {
        const el = this._childByName(node, name);
        return '{' + (el ? this._tidy(this._seq(el)) : '') + '}';
    }

    _element(el) {
        const name = el.localName;

        if (OmmlToLatex.SKIPPED[name]) { return ''; }

        switch (name) {
            case 'r':          return this._run(el);
            case 't':          return this._tokensToLatex(this._tokenise(el.textContent || ''));
            case 'f':          return this._fraction(el);
            case 'd':          return this._delimiter(el);
            case 'sSup':       return this._group(el, 'e') + '^' + this._group(el, 'sup');
            case 'sSub':       return this._group(el, 'e') + '_' + this._group(el, 'sub');
            case 'sSubSup':    return this._group(el, 'e') + '_' + this._group(el, 'sub') +
                                      '^' + this._group(el, 'sup');
            case 'sPre':       return '{}_' + this._group(el, 'sub') + '^' + this._group(el, 'sup') +
                                      this._group(el, 'e');
            case 'rad':        return this._radical(el);
            case 'nary':       return this._nary(el);
            case 'func':       return this._function(el);
            case 'bar':        return (this._propVal(el, 'barPr', 'pos') === 'top' ? '\\overline' :
                                      '\\underline') + this._group(el, 'e');
            case 'acc':        return this._accent(el);
            case 'groupChr':   return (this._propVal(el, 'groupChrPr', 'pos') === 'top' ?
                                      '\\overbrace' : '\\underbrace') + this._group(el, 'e');
            case 'limLow':     return '\\underset' + this._group(el, 'lim') + this._group(el, 'e');
            case 'limUpp':     return '\\overset' + this._group(el, 'lim') + this._group(el, 'e');
            case 'm':          return this._matrix(el);
            case 'eqArr':      return this._eqArray(el);
            case 'oMath':      return this._seq(el);   // nested equation: flatten
            case 'br':         return ' ';
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
                return this._seq(el);
            default:
                // Never drop content: recurse into anything unrecognised and
                // record it, so a new construct shows up in the stats instead
                // of silently disappearing the way whole equations used to.
                this.stats.unknownElements[name] = (this.stats.unknownElements[name] || 0) + 1;
                return this._seq(el);
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
            if (name === 't') { text += kids[i].textContent || ''; }
            else if (name === 'br' || name === 'tab') { text += ' '; }
        }
        if (text === '') { return ''; }

        // <m:nor/> means "literal text, not mathematical notation".
        const rPr = this._childByName(rEl, 'rPr');
        if (rPr && this._childByName(rPr, 'nor')) {
            return '\\text{' + this._escapeText(text) + '}';
        }
        return this._tokensToLatex(this._tokenise(text));
    }

    _fraction(fEl) {
        const type = this._propVal(fEl, 'fPr', 'type');
        const num = this._group(fEl, 'num');
        const den = this._group(fEl, 'den');
        if (type === 'lin') { return num + '/' + den; }
        if (type === 'noBar') { return '\\binom' + num + den; }
        return '\\frac' + num + den;
    }

    /** <m:d> — a delimited group: brackets, absolute-value bars, and so on. */
    _delimiter(dEl) {
        const dPr = this._childByName(dEl, 'dPr');
        const beg = this._attrOr(dPr, 'begChr', '(');
        const end = this._attrOr(dPr, 'endChr', ')');
        const sep = this._attrOr(dPr, 'sepChr', ',');

        const args = this._childrenByName(dEl, 'e');
        let out = '\\left' + this._delimChar(beg);
        for (let i = 0; i < args.length; i++) {
            if (i > 0 && sep !== '') { out += this._delimSeparator(sep); }
            out += this._tidy(this._seq(args[i]));
        }
        return out + '\\right' + this._delimChar(end);
    }

    /** A \left / \right needs a delimiter; an omitted one becomes a full stop. */
    _delimChar(ch) {
        if (ch === '') { return '.'; }
        if (ch === '{' || ch === '}') { return '\\' + ch; }
        if (ch === '|' || ch === '(' || ch === ')' || ch === '[' || ch === ']' ||
            ch === '/' || ch === '.') { return ch; }
        if (Object.prototype.hasOwnProperty.call(OmmlToLatex.SYMBOLS, ch)) {
            return OmmlToLatex.SYMBOLS[ch];
        }
        return ch;
    }

    _delimSeparator(sep) {
        if (sep === '|') { return '\\mid '; }
        return this._delimChar(sep);
    }

    _radical(radEl) {
        const radPr = this._childByName(radEl, 'radPr');
        const hidden = !!(radPr && this._childByName(radPr, 'degHide'));
        const deg = this._childByName(radEl, 'deg');
        const degBody = deg ? this._tidy(this._seq(deg)) : '';

        if (hidden || degBody === '') { return '\\sqrt' + this._group(radEl, 'e'); }
        return '\\sqrt[' + degBody + ']' + this._group(radEl, 'e');
    }

    /** <m:nary> — a summation / product / integral with optional limits. */
    _nary(naryEl) {
        const naryPr = this._childByName(naryEl, 'naryPr');
        const chr = this._attrOr(naryPr, 'chr', '∫');
        const subHide = !!(naryPr && this._childByName(naryPr, 'subHide'));
        const supHide = !!(naryPr && this._childByName(naryPr, 'supHide'));

        let out = this._symbol(chr);
        if (!subHide) { out += '_' + this._group(naryEl, 'sub'); }
        if (!supHide) { out += '^' + this._group(naryEl, 'sup'); }
        return out + this._group(naryEl, 'e');
    }

    /** <m:func> — function application, e.g. sin(x). */
    _function(funcEl) {
        const nameEl = this._childByName(funcEl, 'fName');
        const name = nameEl ? this._tidy(this._seq(nameEl)) : '';
        return (name === '' ? '' : name + ' ') + this._group(funcEl, 'e');
    }

    _accent(accEl) {
        const chr = this._attrOr(this._childByName(accEl, 'accPr'), 'chr', '̂');
        const cmd = Object.prototype.hasOwnProperty.call(OmmlToLatex.ACCENTS, chr)
            ? OmmlToLatex.ACCENTS[chr] : '\\hat';
        return cmd + this._group(accEl, 'e');
    }

    _matrix(mEl) {
        const rows = this._childrenByName(mEl, 'mr');
        const lines = [];
        for (let i = 0; i < rows.length; i++) {
            const cells = this._childrenByName(rows[i], 'e');
            const parts = [];
            for (let c = 0; c < cells.length; c++) { parts.push(this._tidy(this._seq(cells[c]))); }
            lines.push(parts.join(' & '));
        }
        return '\\begin{matrix}' + lines.join(' \\\\ ') + '\\end{matrix}';
    }

    _eqArray(eqEl) {
        const rows = this._childrenByName(eqEl, 'e');
        const lines = [];
        for (let i = 0; i < rows.length; i++) { lines.push(this._tidy(this._seq(rows[i]))); }
        return '\\begin{aligned}' + lines.join(' \\\\ ') + '\\end{aligned}';
    }

    // ------------------------------------------------------------------
    // Internal: run text -> LaTeX
    // ------------------------------------------------------------------

    /**
     * Split a run's text into number / operator / word / space tokens. A number
     * keeps its internal decimal point and thousands commas ("504,000" and
     * "1.5" are one token each, not three).
     */
    _tokenise(text) {
        const out = [];
        let i = 0;
        while (i < text.length) {
            const ch = text.charAt(i);

            if (OmmlToLatex._isSpace(ch)) {
                out.push({ kind: 'space', text: ' ' });
                i++;
            } else if (OmmlToLatex._isDigit(ch)) {
                let j = i + 1;
                while (j < text.length) {
                    if (OmmlToLatex._isDigit(text.charAt(j))) { j++; continue; }
                    const sep = text.charAt(j);
                    if ((sep === '.' || sep === ',') && OmmlToLatex._isDigit(text.charAt(j + 1))) {
                        j += 2;
                        continue;
                    }
                    break;
                }
                out.push({ kind: 'number', text: text.slice(i, j) });
                i = j;
            } else if (OmmlToLatex.OPERATORS.indexOf(ch) !== -1) {
                out.push({ kind: 'op', text: ch });
                i++;
            } else {
                let j = i;
                while (j < text.length) {
                    const c = text.charAt(j);
                    if (OmmlToLatex._isSpace(c) || OmmlToLatex._isDigit(c) ||
                        OmmlToLatex.OPERATORS.indexOf(c) !== -1) { break; }
                    j++;
                }
                out.push({ kind: 'word', text: text.slice(i, j) });
                i = j;
            }
        }
        return out;
    }

    /**
     * Turn tokens into LaTeX. A single letter is a variable and stays bare; a
     * Greek letter becomes its command; a known function name becomes `\sin`
     * and friends; any other word is prose and goes in `\text{…}` together with
     * the words beside it; digits stay bare; everything else is a symbol.
     */
    _tokensToLatex(tokens) {
        const isProse = this._classifyWords(tokens);
        let out = '';
        let buffer = '';

        const flush = () => {
            if (buffer !== '') {
                out += '\\text{' + this._escapeText(buffer) + '}';
                buffer = '';
            }
        };

        for (let i = 0; i < tokens.length; i++) {
            const tok = tokens[i];

            if (tok.kind === 'space') {
                if (buffer !== '') { buffer += ' '; }
            } else if (tok.kind === 'word') {
                const fn = OmmlToLatex.FUNCTIONS[tok.text.toLowerCase()];
                if (fn) {
                    flush();
                    out += fn + ' ';
                } else if (isProse[i]) {
                    buffer += tok.text;
                } else {
                    // A run of variables: each letter stands on its own.
                    flush();
                    for (let c = 0; c < tok.text.length; c++) {
                        out += this._symbol(tok.text.charAt(c));
                    }
                }
            } else if (tok.kind === 'number') {
                flush();
                out += tok.text;
            } else {
                flush();
                out += this._symbol(tok.text);
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

    /**
     * One character as LaTeX. A command always carries a trailing space, so
     * `\Delta` followed by `E` cannot fuse into `\DeltaE`.
     */
    _symbol(ch) {
        if (Object.prototype.hasOwnProperty.call(OmmlToLatex.SYMBOLS, ch)) {
            return OmmlToLatex.SYMBOLS[ch] + ' ';
        }
        if (Object.prototype.hasOwnProperty.call(OmmlToLatex.GREEK, ch)) {
            return OmmlToLatex.GREEK[ch] + ' ';
        }
        if (ch === '{' || ch === '}' || ch === '$' || ch === '&' ||
            ch === '#' || ch === '%' || ch === '_') { return '\\' + ch; }
        return ch;
    }

    /**
     * Collapse the spacing the symbol rule introduces and trim the ends. The
     * guard space after a command is only NEEDED when a letter follows, because
     * a LaTeX command name is letters only — so `\Delta T` keeps its space while
     * `\times 4200` tightens to `\times4200`, which is how the writers' own AI
     * output is shaped (`\frac{8\times15}{2\times3}`).
     */
    _tidy(latex) {
        return latex
            .replace(/ {2,}/g, ' ')
            .replace(/(\\[a-zA-Z]+) +([^a-zA-Z])/g, '$1$2')
            .replace(/^ +| +$/g, '');
    }

    /** Escape the characters that are special inside `\text{…}`. */
    _escapeText(text) {
        return String(text)
            .replace(/\\/g, '\\textbackslash{}')
            .replace(/([{}$&#%_])/g, '\\$1')
            .replace(/\^/g, '\\^{}')
            .replace(/~/g, '\\~{}');
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

    _attrOr(propsEl, childName, fallback) {
        const child = this._childByName(propsEl, childName);
        if (!child) { return fallback; }
        const v = this._val(child);
        return (v === null || v === undefined) ? '' : v;
    }

    _propVal(el, propsName, childName) {
        const props = this._childByName(el, propsName);
        if (!props) { return null; }
        return this._val(this._childByName(props, childName));
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
 * Characters treated as operators by the tokeniser. Everything not in here, not
 * a digit and not whitespace is a letter, so Greek variables, macronised vowels
 * and unit symbols come through without needing a Unicode property escape.
 */
OmmlToLatex.OPERATORS =
    '=+-−±×÷*/<>≤≥≠≈∝' +
    '→←↔⇒⇔' +
    '·∙∘∅∆Δ∂' +
    '()[]{}|,;:!?%^~′″';

/** Operator and symbol characters that have a LaTeX command. */
OmmlToLatex.SYMBOLS = {
    '−': '-', '×': '\\times', '÷': '\\div',
    '±': '\\pm', '∓': '\\mp',
    '≤': '\\leq', '≥': '\\geq', '≠': '\\neq',
    '≈': '\\approx', '∝': '\\propto',
    '≡': '\\equiv', '∞': '\\infty',
    '→': '\\to', '←': '\\leftarrow', '↔': '\\leftrightarrow',
    '⇒': '\\Rightarrow', '⇔': '\\Leftrightarrow',
    '·': '\\cdot', '∙': '\\cdot', '∘': '\\circ', '∅': '\\emptyset',
    '∂': '\\partial', '∑': '\\sum', '∏': '\\prod',
    '∫': '\\int', '∬': '\\iint', '∭': '\\iiint', '∮': '\\oint',
    '√': '\\surd', '∈': '\\in', '∉': '\\notin',
    '⊂': '\\subset', '⊆': '\\subseteq',
    '∪': '\\cup', '∩': '\\cap',
    '∀': '\\forall', '∃': '\\exists', '¬': '\\neg',
    '°': '^\\circ',
    // Word writes U+2206 INCREMENT; the finished modules use U+0394 GREEK
    // CAPITAL DELTA. Both are the same "change in" delta to a reader.
    '∆': '\\Delta', 'Δ': '\\Delta',
    '′': "'", '″': "''"
};

/** Greek letters, so a variable keeps its identity instead of becoming prose. */
OmmlToLatex.GREEK = {
    'α': '\\alpha', 'β': '\\beta', 'γ': '\\gamma', 'δ': '\\delta',
    'ε': '\\epsilon', 'ζ': '\\zeta', 'η': '\\eta', 'θ': '\\theta',
    'ι': '\\iota', 'κ': '\\kappa', 'λ': '\\lambda', 'μ': '\\mu',
    'ν': '\\nu', 'ξ': '\\xi', 'π': '\\pi', 'ρ': '\\rho',
    'σ': '\\sigma', 'τ': '\\tau', 'υ': '\\upsilon', 'φ': '\\phi',
    'χ': '\\chi', 'ψ': '\\psi', 'ω': '\\omega',
    'Γ': '\\Gamma', 'Θ': '\\Theta', 'Λ': '\\Lambda', 'Ξ': '\\Xi',
    'Π': '\\Pi', 'Σ': '\\Sigma', 'Υ': '\\Upsilon', 'Φ': '\\Phi',
    'Ψ': '\\Psi', 'Ω': '\\Omega'
};

/** Function names that are commands in LaTeX rather than prose. */
OmmlToLatex.FUNCTIONS = (function () {
    const names = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'sinh', 'cosh', 'tanh',
        'arcsin', 'arccos', 'arctan', 'log', 'ln', 'lg', 'exp', 'lim', 'max', 'min',
        'det', 'gcd', 'dim', 'ker'];
    const map = {};
    for (let i = 0; i < names.length; i++) { map[names[i]] = '\\' + names[i]; }
    return map;
}());

/** Accent characters Word stores, and the LaTeX command for each. */
OmmlToLatex.ACCENTS = {
    '̂': '\\hat', '̃': '\\tilde', '̄': '\\bar', '̅': '\\overline',
    '̇': '\\dot', '̈': '\\ddot', '̌': '\\check', '̆': '\\breve',
    '⃗': '\\vec', '→': '\\vec'
};

/** Word-only property elements: they describe formatting LaTeX does not carry. */
OmmlToLatex.SKIPPED = {
    ctrlPr: true, rPr: true, fPr: true, dPr: true, sSupPr: true, sSubPr: true,
    sSubSupPr: true, sPrePr: true, radPr: true, naryPr: true, funcPr: true,
    barPr: true, accPr: true, limLowPr: true, limUppPr: true, groupChrPr: true,
    mPr: true, mrPr: true, eqArrPr: true, boxPr: true, borderBoxPr: true,
    phantPr: true, argPr: true, oMathParaPr: true, bookmarkStart: true,
    bookmarkEnd: true, proofErr: true, lastRenderedPageBreak: true
};

// Node (test runner) export; harmless in the browser.
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OmmlToLatex;
}
