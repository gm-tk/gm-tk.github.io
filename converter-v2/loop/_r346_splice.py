#!/usr/bin/env python3
"""_r346_splice.py — ROUND 346 (Chris's D10-7: Word equations → MathML). The V1.5 `pageforge-site/js/omml-to-mathml.js`
converter ported into DocxExtractor.js over a plain-object XML tree (V2's extractor is regex-based; the V1.5 class only
touches childNodes / nodeType / localName / textContent / getAttribute); an `m:oMath` beside a paragraph's runs becomes a
synthetic black run carrying a private-use sentinel (U+E010 id U+E011) that flows through every text path unchanged and is
swapped for the `<math>` markup by a full-page post-pass in PageAssembler (then the page gains the `mathJax` body class);
the hand-off .txt gets the same swap. Idempotent; LF-safe; never json.dumps. Run: python3 _r346_splice.py [--check]"""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2"))
DX = os.path.join(ROOT, "app", "js", "DocxExtractor.js")
PA = os.path.join(ROOT, "app", "js", "PageAssembler.js")
MB = os.path.join(ROOT, "app", "js", "ManifestBuilder.js")
IR = os.path.join(ROOT, "data", "Input_Doc_Rules.json")
CHECK = "--check" in sys.argv
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    if not CHECK: io.open(p, "w", encoding="utf-8", newline="").write(s)
def once(s, a, w): n = s.count(a); assert n == 1, f"{w}: anchor found {n}x: {a[:80]!r}"

CONVERTER = r'''/**
 * ROUND 346 (the autonomous loop's session 12 — Chris's D10-7, Option A: a Word EQUATION ships
 * as MathML, the form that renders in MTK). A Word equation is not a w:r run: it lives in an
 * <m:oMath> (inline) or <m:oMathPara> (its own line) BESIDE the runs of a w:p, so the run walk
 * below never saw it and every equation silently vanished from the page (329 equations across
 * 12 Writers Templates, measured outputs/_measure_r346_omml.py). This is the V1.5 converter
 * (pageforge-site/js/omml-to-mathml.js — tested against this corpus) ported verbatim in its
 * logic over a PLAIN-OBJECT XML TREE (OmmlMathml.Tree), because V2's extractor is regex-based
 * and the V1.5 class only ever touches childNodes / nodeType / localName / textContent /
 * getAttribute. An OMML element it does not recognise is recursed into as an <mrow> and counted
 * in stats.unknownElements — never dropped (the silent-drop bug this class exists to prevent).
 * Data Input_Doc_Rules.math; env MATHML_OFF (in DocxExtractor.#parseParagraph).
 */
class OmmlMathml {
	constructor() {
		this.MATH_NS = "http://www.w3.org/1998/Math/MathML";
		this.stats = { equations: 0, unknownElements: {} };
	}

	/** Convert one <m:oMath> element (a Tree node) into a complete `<math>…</math>` string. */
	convert(oMathEl) {
		const body = this._seq(oMathEl);
		this.stats.equations++;
		return '<math xmlns="' + this.MATH_NS + '">' + body + "</math>";
	}

	/** Parse an OMML XML fragment (one <m:oMath>…</m:oMath>) into a plain-object node tree. */
	static Tree(xml) {
		const root = { nodeType: 1, localName: "#root", attrs: {}, childNodes: [], parent: null };
		let cur = root;
		const TOK = /<!--[\s\S]*?-->|<\?[\s\S]*?\?>|<\/([A-Za-z_][\w:.-]*)\s*>|<([A-Za-z_][\w:.-]*)((?:\s+[\w:.-]+\s*=\s*"[^"]*")*)\s*(\/?)>|([^<]+)/g;
		const ATTR = /([\w:.-]+)\s*=\s*"([^"]*)"/g;
		const decode = (s) => s.replace(/&(amp|lt|gt|quot|apos|#x[0-9A-Fa-f]+|#\d+);/g, (m, e) => {
			if (e === "amp") return "&"; if (e === "lt") return "<"; if (e === "gt") return ">";
			if (e === "quot") return '"'; if (e === "apos") return "'";
			return String.fromCodePoint(e[1] === "x" || e[1] === "X" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10));
		});
		const mk = (name, attrs, parent) => {
			const el = { nodeType: 1, localName: name.includes(":") ? name.slice(name.lastIndexOf(":") + 1) : name,
				attrs, childNodes: [], parent,
				getAttribute(n) { return Object.prototype.hasOwnProperty.call(this.attrs, n) ? this.attrs[n] : null; } };
			Object.defineProperty(el, "textContent", { get() {
				return this.childNodes.map((k) => k.nodeType === 3 ? k.textContent : k.textContent).join("");
			} });
			return el;
		};
		let m;
		while ((m = TOK.exec(xml)) !== null) {
			if (m[1] !== undefined) { if (cur.parent) cur = cur.parent; continue; }   // close
			if (m[2] !== undefined) {
				const attrs = {}; let a;
				while ((a = ATTR.exec(m[3] || "")) !== null) attrs[a[1]] = decode(a[2]);
				const el = mk(m[2], attrs, cur);
				cur.childNodes.push(el);
				if (!m[4]) cur = el;                                             // open (not self-closed)
				continue;
			}
			if (m[5] !== undefined) cur.childNodes.push({ nodeType: 3, textContent: decode(m[5]) });
		}
		return root;
	}

	_seq(node) {
		const kids = this._elementChildren(node); let out = "";
		for (let i = 0; i < kids.length; i++) out += this._element(kids[i]);
		return out;
	}
	_row(node) { return "<mrow>" + this._seq(node) + "</mrow>"; }
	_rowOf(node, name) { const el = this._childByName(node, name); return el ? this._row(el) : "<mrow></mrow>"; }

	_element(el) {
		const name = el.localName;
		if (OmmlMathml.SKIPPED[name]) return "";
		switch (name) {
			case "r":        return this._run(el);
			case "t":        return this._tokensToMathml(this._tokenise(el.textContent || ""));
			case "f":        return this._fraction(el);
			case "d":        return this._delimiter(el);
			case "sSup":     return "<msup>" + this._rowOf(el, "e") + this._rowOf(el, "sup") + "</msup>";
			case "sSub":     return "<msub>" + this._rowOf(el, "e") + this._rowOf(el, "sub") + "</msub>";
			case "sSubSup":  return "<msubsup>" + this._rowOf(el, "e") + this._rowOf(el, "sub") + this._rowOf(el, "sup") + "</msubsup>";
			case "sPre":     return "<mmultiscripts>" + this._rowOf(el, "e") + "<mprescripts/>" + this._rowOf(el, "sub") + this._rowOf(el, "sup") + "</mmultiscripts>";
			case "rad":      return this._radical(el);
			case "nary":     return this._nary(el);
			case "func":     return "<mrow>" + this._rowOf(el, "fName") + "<mo>&#x2061;</mo>" + this._rowOf(el, "e") + "</mrow>";
			case "bar":      return this._bar(el);
			case "acc":      return this._accent(el);
			case "groupChr": return this._groupChr(el);
			case "limLow":   return "<munder>" + this._rowOf(el, "e") + this._rowOf(el, "lim") + "</munder>";
			case "limUpp":   return "<mover>" + this._rowOf(el, "e") + this._rowOf(el, "lim") + "</mover>";
			case "m":        return this._matrix(el);
			case "eqArr":    return this._eqArray(el);
			case "oMath":    return this._seq(el);
			case "br":       return "";
			case "ins":      return this._seq(el);
			case "del":      return "";
			case "e": case "num": case "den": case "lim": case "sub": case "sup": case "deg": case "fName":
			case "box": case "borderBox": case "phant":
				return this._row(el);
			default:
				this.stats.unknownElements[name] = (this.stats.unknownElements[name] || 0) + 1;
				return this._row(el);
		}
	}

	_run(rEl) {
		let text = "";
		const kids = this._elementChildren(rEl);
		for (let i = 0; i < kids.length; i++) {
			const name = kids[i].localName;
			if (name === "t") text += kids[i].textContent || "";
			else if (name === "br" || name === "tab") text += " ";
		}
		if (text === "") return "";
		const rPr = this._childByName(rEl, "rPr");
		if (rPr && this._childByName(rPr, "nor")) return "<mtext>" + this._escapeText(text) + "</mtext>";
		return this._tokensToMathml(this._tokenise(text));
	}
	_fraction(fEl) {
		const type = this._propVal(fEl, "fPr", "type");
		const num = this._rowOf(fEl, "num"), den = this._rowOf(fEl, "den");
		if (type === "lin") return "<mrow>" + num + "<mo>/</mo>" + den + "</mrow>";
		if (type === "noBar") return '<mfrac linethickness="0">' + num + den + "</mfrac>";
		return "<mfrac>" + num + den + "</mfrac>";
	}
	_delimiter(dEl) {
		const dPr = this._childByName(dEl, "dPr");
		const beg = this._attrOr(dPr, "begChr", "("), end = this._attrOr(dPr, "endChr", ")"), sep = this._attrOr(dPr, "sepChr", ",");
		const args = this._childrenByName(dEl, "e");
		let out = "<mrow>";
		if (beg !== "") out += "<mo>" + this._escapeText(beg) + "</mo>";
		for (let i = 0; i < args.length; i++) {
			if (i > 0 && sep !== "") out += "<mo>" + this._escapeText(sep) + "</mo>";
			out += this._row(args[i]);
		}
		if (end !== "") out += "<mo>" + this._escapeText(end) + "</mo>";
		return out + "</mrow>";
	}
	_radical(radEl) {
		const radPr = this._childByName(radEl, "radPr");
		const hidden = !!(radPr && this._childByName(radPr, "degHide"));
		const deg = this._childByName(radEl, "deg");
		const degBody = deg ? this._seq(deg) : "";
		if (hidden || degBody === "") return "<msqrt>" + this._rowOf(radEl, "e") + "</msqrt>";
		return "<mroot>" + this._rowOf(radEl, "e") + "<mrow>" + degBody + "</mrow></mroot>";
	}
	_nary(naryEl) {
		const naryPr = this._childByName(naryEl, "naryPr");
		const chr = this._attrOr(naryPr, "chr", "∫");
		const subHide = !!(naryPr && this._childByName(naryPr, "subHide"));
		const supHide = !!(naryPr && this._childByName(naryPr, "supHide"));
		const op = "<mo>" + this._escapeText(chr) + "</mo>";
		const beside = "∫∬∭∮".indexOf(chr) !== -1;
		const under = beside ? "msub" : "munder", over = beside ? "msup" : "mover", both = beside ? "msubsup" : "munderover";
		let head;
		if (subHide && supHide) head = op;
		else if (supHide) head = "<" + under + ">" + op + this._rowOf(naryEl, "sub") + "</" + under + ">";
		else if (subHide) head = "<" + over + ">" + op + this._rowOf(naryEl, "sup") + "</" + over + ">";
		else head = "<" + both + ">" + op + this._rowOf(naryEl, "sub") + this._rowOf(naryEl, "sup") + "</" + both + ">";
		return "<mrow>" + head + this._rowOf(naryEl, "e") + "</mrow>";
	}
	_bar(barEl) {
		const pos = this._propVal(barEl, "barPr", "pos");
		if (pos === "top") return '<mover accent="true">' + this._rowOf(barEl, "e") + "<mo>&#xAF;</mo></mover>";
		return '<munder accentunder="true">' + this._rowOf(barEl, "e") + "<mo>&#x5F;</mo></munder>";
	}
	_accent(accEl) {
		const chr = this._attrOr(this._childByName(accEl, "accPr"), "chr", "̂");
		return '<mover accent="true">' + this._rowOf(accEl, "e") + "<mo>" + this._escapeText(chr) + "</mo></mover>";
	}
	_groupChr(gEl) {
		const gPr = this._childByName(gEl, "groupChrPr");
		const chr = this._attrOr(gPr, "chr", "⏟");
		const pos = this._propVal(gEl, "groupChrPr", "pos");
		const tag = pos === "top" ? "mover" : "munder";
		return "<" + tag + ">" + this._rowOf(gEl, "e") + "<mo>" + this._escapeText(chr) + "</mo></" + tag + ">";
	}
	_matrix(mEl) {
		const rows = this._childrenByName(mEl, "mr"); let out = "<mtable>";
		for (let i = 0; i < rows.length; i++) {
			const cells = this._childrenByName(rows[i], "e"); out += "<mtr>";
			for (let c = 0; c < cells.length; c++) out += "<mtd>" + this._seq(cells[c]) + "</mtd>";
			out += "</mtr>";
		}
		return out + "</mtable>";
	}
	_eqArray(eqEl) {
		const rows = this._childrenByName(eqEl, "e"); let out = "<mtable>";
		for (let i = 0; i < rows.length; i++) out += "<mtr><mtd>" + this._seq(rows[i]) + "</mtd></mtr>";
		return out + "</mtable>";
	}

	/** Split a run's text into number / operator / word / space tokens (a number keeps its decimal point and thousands commas). */
	_tokenise(text) {
		const out = []; let i = 0;
		while (i < text.length) {
			const ch = text.charAt(i);
			if (OmmlMathml._isSpace(ch)) { out.push({ kind: "space", text: ch }); i++; }
			else if (OmmlMathml._isDigit(ch)) {
				let j = i + 1;
				while (j < text.length) {
					if (OmmlMathml._isDigit(text.charAt(j))) { j++; continue; }
					const sep = text.charAt(j);
					if ((sep === "." || sep === ",") && OmmlMathml._isDigit(text.charAt(j + 1))) { j += 2; continue; }
					break;
				}
				out.push({ kind: "number", text: text.slice(i, j) }); i = j;
			} else if (OmmlMathml.OPERATORS.indexOf(ch) !== -1) { out.push({ kind: "op", text: ch }); i++; }
			else {
				let j = i;
				while (j < text.length) {
					const c = text.charAt(j);
					if (OmmlMathml._isSpace(c) || OmmlMathml._isDigit(c) || OmmlMathml.OPERATORS.indexOf(c) !== -1) break;
					j++;
				}
				out.push({ kind: "word", text: text.slice(i, j) }); i = j;
			}
		}
		return out;
	}
	/** Tokens → MathML token elements: a single letter is a variable <mi>, a word is prose <mtext> (neighbouring words and
	 *  the spaces between them kept together), digits are <mn>, everything else <mo> — the human developers' convention. */
	_tokensToMathml(tokens) {
		const isProse = this._classifyWords(tokens); let out = "", buffer = "";
		const flush = () => { if (buffer !== "") { out += "<mtext>" + this._escapeText(this._protectEdgeSpaces(buffer)) + "</mtext>"; buffer = ""; } };
		for (let i = 0; i < tokens.length; i++) {
			const tok = tokens[i];
			if (tok.kind === "space") { if (buffer !== "") buffer += " "; }
			else if (tok.kind === "word") {
				if (isProse[i]) buffer += tok.text;
				else { flush(); for (let c = 0; c < tok.text.length; c++) out += "<mi>" + this._escapeText(tok.text.charAt(c)) + "</mi>"; }
			} else if (tok.kind === "number") { flush(); out += "<mn>" + this._escapeText(tok.text) + "</mn>"; }
			else { flush(); out += "<mo>" + this._escapeText(tok.text) + "</mo>"; }
		}
		flush();
		return out;
	}
	/** one letter → a variable; 3+ → prose; exactly two → a variable pair unless a 3+-letter word sits one space away. */
	_classifyWords(tokens) {
		const prose = [];
		for (let i = 0; i < tokens.length; i++) {
			const tok = tokens[i];
			if (tok.kind !== "word") { prose.push(false); continue; }
			if (tok.text.length === 1) { prose.push(false); continue; }
			if (tok.text.length >= 3) { prose.push(true); continue; }
			prose.push(this._hasPhraseNeighbour(tokens, i));
		}
		return prose;
	}
	_hasPhraseNeighbour(tokens, i) {
		const long = (t) => t && t.kind === "word" && t.text.length >= 3;
		const before = i >= 2 && tokens[i - 1].kind === "space" && long(tokens[i - 2]);
		const after = i + 2 < tokens.length && tokens[i + 1].kind === "space" && long(tokens[i + 2]);
		return before || after;
	}
	_elementChildren(node) {
		const out = []; const kids = (node && node.childNodes) ? node.childNodes : [];
		for (let i = 0; i < kids.length; i++) if (kids[i] && kids[i].nodeType === 1) out.push(kids[i]);
		return out;
	}
	_childByName(node, name) { const kids = this._elementChildren(node); for (let i = 0; i < kids.length; i++) if (kids[i].localName === name) return kids[i]; return null; }
	_childrenByName(node, name) { const kids = this._elementChildren(node), out = []; for (let i = 0; i < kids.length; i++) if (kids[i].localName === name) out.push(kids[i]); return out; }
	_val(el) {
		if (!el) return null;
		const raw = el.getAttribute("m:val") ?? el.getAttribute("w:val") ?? el.getAttribute("val");
		return (raw === null || raw === undefined || raw === "") ? null : raw;
	}
	_attrOr(propsEl, childName, fallback) {
		const child = this._childByName(propsEl, childName);
		if (!child) return fallback;
		const v = this._val(child);
		return (v === null || v === undefined) ? "" : v;
	}
	_propVal(el, propsName, childName) { const props = this._childByName(el, propsName); if (!props) return null; return this._val(this._childByName(props, childName)); }
	_protectEdgeSpaces(text) {
		return text.replace(/^ +/, (m) => " ".repeat(m.length)).replace(/ +$/, (m) => " ".repeat(m.length));
	}
	_escapeText(text) {
		return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/ /g, "&#xA0;");
	}
	static _isDigit(ch) { return ch >= "0" && ch <= "9"; }
	/** Whitespace as Word writes it inside an equation (U+2008 / U+2009 / U+00A0 included via \s); U+200B is the only gap. */
	static _isSpace(ch) { return /\s/.test(ch) || ch === "​"; }
}
/** Characters that become <mo>; everything else non-digit / non-space is a letter (Greek, macrons, ℃ come through as <mi>). */
OmmlMathml.OPERATORS = "=+-−±×÷*/<>≤≥≠≈∝" + "→←↔⇒⇔"
	+ "·∙∘∅∆Δ∂" + "()[]{}|,;:!?%^~′″";
/** Word-only property elements: formatting MathML does not carry. */
OmmlMathml.SKIPPED = {
	ctrlPr: true, rPr: true, fPr: true, dPr: true, sSupPr: true, sSubPr: true, sSubSupPr: true, sPrePr: true, radPr: true,
	naryPr: true, funcPr: true, barPr: true, accPr: true, limLowPr: true, limUppPr: true, groupChrPr: true, mPr: true,
	mrPr: true, eqArrPr: true, boxPr: true, borderBoxPr: true, phantPr: true, argPr: true, oMathParaPr: true,
	bookmarkStart: true, bookmarkEnd: true, proofErr: true, lastRenderedPageBreak: true,
};

'''

# ---------------------------------------------------------------- Input_Doc_Rules.json
ir = rd(IR)
if '"math": {' in ir:
    print("Input_Doc_Rules: math block already present")
else:
    anchor = '\t"text_normalise": {\n'
    once(ir, anchor, "Input_Doc_Rules")
    block = ('\t"math": {\n'
             '\t\t"enabled": true,\n'
             '\t\t"env": "MATHML_OFF",\n'
             '\t\t"body_class_token": "mathJax",\n'
             '\t\t"rule": "ROUND 346 (the autonomous loop\'s session 12, 2026-09-16 — Chris\'s D10-7, Option A: MathML, the gold\'s form and the one that renders in MTK; KB delta: 05A \'MathJax / Equations\' → MathML is the shipped form). A Word equation is not a w:r run — it lives in an <m:oMath> beside the runs of a w:p (329 equations across 12 Writers Templates, every one inline beside runs; not one <m:oMathPara> in the corpus — outputs/_measure_r346_omml.py), so the run walk never saw it and every equation silently vanished from the page. Now each <m:oMath> is converted by OmmlMathml (the V1.5 pageforge-site/js/omml-to-mathml.js port; vocabulary r/t, f, sSup, sSub, d, rad = the corpus\'s whole OMML vocabulary, the rest of the grammar implemented anyway and an unknown element recursed as <mrow>, never dropped) and replaced IN PLACE by a synthetic black run carrying a private-use sentinel (U+E010 <id> U+E011) that flows through every text path — tag classification, coalescing, the emoji strip, the hover sentinels U+E000/E001, the typed-number list — unchanged; PageAssembler\'s final post-pass swaps the sentinel for the <math xmlns=…> markup (bare — the gold\'s 1873 : 105 inline : 70 block majority; MathJax renders it either way) and adds body_class_token to the <body> class of every page that carries a <math> (the gold\'s per-page form, 0.92 precision); the hand-off .txt gets the same swap. Verifier reference/tests/_verify_math.cjs: per module, the docx <m:oMath> count == the pages\' <math> count, every <math> page carries mathJax, no sentinel leaks (defect 0). Env MATHML_OFF reverts byte-for-byte (the equations vanish again)."\n'
             '\t},\n')
    ir = ir.replace(anchor, block + anchor, 1); wr(IR, ir); print("Input_Doc_Rules: math block inserted")

# ---------------------------------------------------------------- DocxExtractor.js
dx = rd(DX)
if "class OmmlMathml" in dx:
    print("DocxExtractor: OmmlMathml already present")
else:
    a0 = "class DocxExtractor {\n"
    once(dx, a0, "DocxExtractor class head")
    dx = dx.replace(a0, CONVERTER + a0, 1)
    # registry statics right after the class opens
    a1 = "class DocxExtractor {\n"
    reg = ("class DocxExtractor {\n"
           "\t// ROUND 346 — the equation registry: every converted <m:oMath> is stored here and its\n"
           "\t// index rides through the text stream as the sentinel U+E010 <id> U+E011 (a private-use\n"
           "\t// pair, like the r75 hover sentinels U+E000/E001); PageAssembler / ManifestBuilder swap it\n"
           "\t// for the markup at the very end. Process-wide (a run never reads another run's ids).\n"
           "\tstatic #math = [];\n"
           "\tstatic MathRegister(html) { this.#math.push(String(html)); return this.#math.length - 1; }\n"
           "\tstatic MathSentinel(id) { return String.fromCharCode(0xE010) + id + String.fromCharCode(0xE011); }\n"
           "\tstatic MathReplace(text) {\n"
           "\t\tif (text == null) return text;\n"
           "\t\tconst s = String(text);\n"
           "\t\tif (s.indexOf(String.fromCharCode(0xE010)) < 0) return s;\n"
           "\t\treturn s.replace(/\\uE010(\\d+)\\uE011/g, (m, id) => DocxExtractor.#math[+id] ?? \"\");\n"
           "\t}\n"
           "\tstatic MathRegistered() { return this.#math.length; }\n")
    dx = dx.replace(a1, reg, 1)
    # the paragraph hook: before the hyperlink split
    a2 = ("\t\tconst segments = xml.split(/(<w:hyperlink [^>]*>|<\\/w:hyperlink>)/);\n"
          "\t\tlet currentLink = null;\n")
    once(dx, a2, "parseParagraph segments")
    hook = ("\t\t// ROUND 346 (Chris's D10-7): a Word EQUATION lives in an <m:oMath> BESIDE the runs, so the\n"
            "\t\t// run walk below never saw it. Each one is converted to MathML now (OmmlMathml) and\n"
            "\t\t// replaced in place by a synthetic black run carrying its registry sentinel, so the\n"
            "\t\t// equation keeps its exact position inside the paragraph's text. Data Input_Doc_Rules.math;\n"
            "\t\t// env MATHML_OFF (the equation vanishes again, as before this round).\n"
            "\t\tconst _mathCfg = rules.math;\n"
            "\t\tif (_mathCfg && _mathCfg.enabled !== false && xml.indexOf(\"<m:oMath\") >= 0\n"
            "\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[_mathCfg.env ?? \"MATHML_OFF\"])) {\n"
            "\t\t\tconst conv = new OmmlMathml();\n"
            "\t\t\txml = xml.replace(/<m:oMath\\b[^>]*>[\\s\\S]*?<\\/m:oMath>/g, (frag) => {\n"
            "\t\t\t\tconst tree = OmmlMathml.Tree(frag);\n"
            "\t\t\t\tconst el = tree.childNodes.find((k) => k.nodeType === 1 && k.localName === \"oMath\");\n"
            "\t\t\t\tconst html = el ? conv.convert(el) : \"\";\n"
            "\t\t\t\tif (!html) return \"\";\n"
            "\t\t\t\treturn \"<w:r><w:t xml:space=\\\"preserve\\\">\" + DocxExtractor.MathSentinel(DocxExtractor.MathRegister(html)) + \"</w:t></w:r>\";\n"
            "\t\t\t});\n"
            "\t\t}\n")
    dx = dx.replace(a2, hook + a2, 1)
    a3 = "if (typeof module !== \"undefined\") module.exports = { DocxExtractor };"
    once(dx, a3, "exports")
    dx = dx.replace(a3, "if (typeof module !== \"undefined\") module.exports = { DocxExtractor, OmmlMathml };", 1)
    wr(DX, dx); print("DocxExtractor: converter + registry + hook applied")

# ---------------------------------------------------------------- PageAssembler.js
pa = rd(PA)
if "ROUND 346" in pa:
    print("PageAssembler: math post-pass already present")
else:
    a4 = ("\t\t\t\t\t\tconst ai = tidied.indexOf(\"<div class=\\\"acks\");\n"
          "\t\t\t\t\t\treturn ai < 0\n"
          "\t\t\t\t\t\t\t? ListsAndRuns.LinkTextDisplay(deEmoji(tidied))\n"
          "\t\t\t\t\t\t\t: ListsAndRuns.LinkTextDisplay(deEmoji(tidied.slice(0, ai))) + tidied.slice(ai);\n")
    once(pa, a4, "PageAssembler chain")
    n4 = ("\t\t\t\t\t\tconst ai = tidied.indexOf(\"<div class=\\\"acks\");\n"
          "\t\t\t\t\t\tconst passed = ai < 0\n"
          "\t\t\t\t\t\t\t? ListsAndRuns.LinkTextDisplay(deEmoji(tidied))\n"
          "\t\t\t\t\t\t\t: ListsAndRuns.LinkTextDisplay(deEmoji(tidied.slice(0, ai))) + tidied.slice(ai);\n"
          "\t\t\t\t\t\t// ROUND 346 (Chris's D10-7): the equation sentinels become their MathML LAST, after every\n"
          "\t\t\t\t\t\t// text pass (none of them may touch the markup), and a page that now carries a <math>\n"
          "\t\t\t\t\t\t// gains the mathJax body class (the gold's per-page form). Data Input_Doc_Rules.math.\n"
          "\t\t\t\t\t\tconst _mathCfg = DataService.Data.InputDocRules?.math;\n"
          "\t\t\t\t\t\tlet withMath = DocxExtractor.MathReplace(passed);\n"
          "\t\t\t\t\t\tif (_mathCfg && _mathCfg.enabled !== false && withMath !== passed && /<math\\b/.test(withMath)) {\n"
          "\t\t\t\t\t\t\tconst tok = _mathCfg.body_class_token || \"mathJax\";\n"
          "\t\t\t\t\t\t\twithMath = withMath.replace(/<body class=\"([^\"]*)\"/, (m, cls) =>\n"
          "\t\t\t\t\t\t\t\tnew RegExp(\"(^|\\\\s)\" + tok + \"(\\\\s|$)\").test(cls) ? m : \"<body class=\\\"\" + cls + \" \" + tok + \"\\\"\");\n"
          "\t\t\t\t\t\t}\n"
          "\t\t\t\t\t\treturn withMath;\n")
    pa = pa.replace(a4, n4, 1)
    a5 = ("\t\t\tcontent: ManifestBuilder.Build(run),\n\t\t\tkind: \"manifest\",\n")
    once(pa, a5, "manifest push")
    pa = pa.replace(a5, "\t\t\tcontent: DocxExtractor.MathReplace(ManifestBuilder.Build(run)),   // ROUND 346: equation sentinels → MathML in the hand-off too\n\t\t\tkind: \"manifest\",\n", 1)
    wr(PA, pa); print("PageAssembler: math post-pass + manifest swap applied")
print("CHECK ONLY" if CHECK else "done")
