/**
 * DocxExtractor.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Turns an unzipped Writers Template .docx into the converter's intermediate
 * form: an ordered list of content BLOCKS (paragraphs + tables), each
 * carrying (a) the marker-text string the tag pipeline reads, and (b)
 * metadata the emitters need (hyperlink targets, WT page number, list info).
 *
 * THE KEY IDEA (why this file makes everything else safe):
 * The raw docx still carries the writers' red colouring as w:color runs
 * (verified: ff0000 / ee0000 in the real corpus templates). We re-wrap red
 * runs in the exact 🔴[RED TEXT] … [/RED TEXT]🔴 markers, and tables in the
 * exact ┌─── TABLE ─── │ … ║ … └─── END TABLE ─── lines, that the validated
 * historical corpus uses. Everything downstream of this file therefore runs
 * the SAME pipeline that passed the 9,557-variation regression and the
 * 121-type e2e validation — fresh uploads and the proven corpus are
 * indistinguishable.
 *
 * WHY A HAND-ROLLED XML WALK (and not DOMParser):
 * OOXML from Word is machine-generated and extremely regular; a ~40-line
 * token walker covers everything we read (w:p, w:r, w:t, w:color, w:b,
 * w:i, w:hyperlink, w:tbl/tr/tc, w:br, w:lastRenderedPageBreak, w:numPr).
 * It also runs identically in the browser and in the sandbox test harness,
 * so the ingest layer is regression-testable end-to-end.
 *
 * DATA THIS FILE READS:
 * Input_Doc_Rules.json — red hex values, marker strings, table markers,
 * formatting markers, MTK signature, content-start rule. NO input-shape
 * knowledge is hard-coded here.
 *
 * WHEN TO WORK HERE:
 * Only if Word itself changes how it stores something. New red shade,
 * new boilerplate, new media-table heading → edit Input_Doc_Rules.json.
 * ===========================================================================
 */

/**
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
		text = OmmlMathml._foldMathAlpha(text);   // ROUND 347: U+1D465 (math italic x) -> x before any per-unit walk
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
				else { flush(); for (const c of tok.text) out += "<mi>" + this._escapeText(c) + "</mi>"; }   // ROUND 347: by code point, never by UTF-16 unit
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
	/** ROUND 347: Mathematical Alphanumeric Symbols (U+1D400-U+1D7FF - Word's italic x, bold b, bold 3 ...) fold to the plain letter /
	 *  Greek letter / digit the human pages carry (<mi>x</mi>); MathML italicises a one-letter <mi> itself. Latin: 13 styles x 52
	 *  (A-Z, a-z); Greek: 5 styles x 58 (Alpha-Omega with U+03F4 at 17, nabla, alpha-omega with final sigma at 17, then the seven
	 *  symbol variants); digits: 5 styles x 10. Walks by code point - the V1.5 port walked UTF-16 units and split every pair. */
	static _foldMathAlpha(text) {
		if (!/\uD835/.test(text)) return text;   // the whole block sits on the D835 high surrogate
		let out = "";
		for (const ch of text) {
			const cp = ch.codePointAt(0);
			if (cp >= 0x1D400 && cp <= 0x1D6A3) { const k = (cp - 0x1D400) % 52; out += String.fromCharCode(k < 26 ? 65 + k : 97 + k - 26); }
			else if (cp >= 0x1D6A8 && cp <= 0x1D7CB) { const k = (cp - 0x1D6A8) % 58; out += k === 17 ? "ϴ" : k < 25 ? String.fromCharCode(0x391 + k) : k === 25 ? "∇" : k < 51 ? String.fromCharCode(0x3B1 + k - 26) : "∂ϵϑϰϕϱϖ"[k - 51]; }
			else if (cp >= 0x1D7CE && cp <= 0x1D7FF) out += String.fromCharCode(48 + (cp - 0x1D7CE) % 10);
			else out += ch;
		}
		return out;
	}
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

class DocxExtractor {
	// ROUND 346 — the equation registry: every converted <m:oMath> is stored here and its
	// index rides through the text stream as the sentinel U+E010 <id> U+E011 (a private-use
	// pair, like the r75 hover sentinels U+E000/E001); PageAssembler / ManifestBuilder swap it
	// for the markup at the very end. Process-wide (a run never reads another run's ids).
	static #math = [];
	static MathRegister(html) { this.#math.push(String(html)); return this.#math.length - 1; }
	static MathSentinel(id) { return String.fromCharCode(0xE010) + id + String.fromCharCode(0xE011); }
	static MathReplace(text) {
		if (text == null) return text;
		const s = String(text);
		if (s.indexOf(String.fromCharCode(0xE010)) < 0) return s;
		return s.replace(/\uE010(\d+)\uE011/g, (m, id) => DocxExtractor.#math[+id] ?? "");
	}
	static MathRegistered() { return this.#math.length; }

	/**
	 * Extracts a complete docx into blocks + metadata.
	 *
	 * WHAT IT RETURNS:
	 * {
	 *   blocks:   [ paraBlock | tableBlock … ]   (document order)
	 *   rels:     Map(rId → external URL)
	 *   mtkFlag:  true when the MTK/TRR bilingual signature was seen
	 *   hasContentStart: true when a [TITLE BAR] red tag exists
	 * }
	 *
	 * BLOCK SHAPES (the contract every later stage relies on):
	 * paraBlock = {
	 *   kind: "para",
	 *   text:  "🔴[RED TEXT] [H2] [/RED TEXT]🔴**Learning Intentions**",
	 *   links: [ { text, target } ],   // resolved hyperlinks in this para
	 *   wtPage: 3,                     // Writers Template page number
	 *   list: "bullet" | "number" | null
	 * }
	 * tableBlock = {
	 *   kind: "table",
	 *   rows: [ [ cellText, cellText ] ],   // marker-text per cell
	 *   links: [ { text, target } ],        // hyperlinks anywhere in table
	 *   wtPage: 5,
	 *   text: "┌─── TABLE ───\n│ a ║ b\n└─── END TABLE ───"
	 * }
	 *
	 * @param {ZipReader} zip - opened docx archive
	 * @returns {Promise<Object>} extraction result as above
	 */
	static async Extract(zip) {
		const rules = DataService.Data.InputDocRules;

		// --- the three parts we read ------------------------------------
		const documentXml = await zip.ReadText("word/document.xml");
		// hyperlink targets live in the rels part, NOT the visible text —
		// the single most important extraction rule for the media list
		const relsXml = zip.Has("word/_rels/document.xml.rels")
			? await zip.ReadText("word/_rels/document.xml.rels") : "";
		// numbering.xml tells bullet vs numbered lists (optional part)
		const numberingXml = zip.Has("word/numbering.xml")
			? await zip.ReadText("word/numbering.xml") : "";
		// comments.xml carries native Word editor comments left by reviewers.
		// This is an OPTIONAL part of the .docx — most, but not all, Writers
		// Templates have it. Each comment is keyed by id → {author, text}; it
		// gets anchored to a specific content block later on, in
		// #parseDocument, by matching against the document.xml
		// commentRangeStart markers. We capture EVERY comment here regardless
		// of author — deciding WHICH authors' comments are worth showing (and
		// how to render them) happens further downstream, in ContentConverter.
		const commentsXml = zip.Has("word/comments.xml")
			? await zip.ReadText("word/comments.xml") : "";

		const rels = this.#parseRels(relsXml);
		const numFormats = this.#parseNumbering(numberingXml);
		const comments = this.#parseComments(commentsXml);
		const blocks = this.#parseDocument(documentXml, rels, numFormats, rules, comments);

		// --- document-level signals ---------------------------------------
		// MTK/TRR bilingual templates follow a separate pathway (data rule).
		// IMPORTANT: this is only the RAW signature signal — the heading
		// "MTK WRITERS TEMPLATE" also appears in standard templates'
		// front-matter (verified on OSAH401), so the unsupported decision is
		// made later by ConversionRun: signature AND module-code prefix
		// (Input_Doc_Rules.unsupported_pathways.also_requires_code_prefix).
		const signatures = rules.unsupported_pathways.map((u) => u.signature);
		let mtkFlag = false;
		for (const b of blocks.slice(0, 60)) {  // signature sits in the title block
			if (b.kind !== "para") continue;
			const folded = Utils.Fold(b.text);
			if (signatures.some((sig) => folded.includes(sig))) { mtkFlag = true; break; }
		}

		// literal check only here (no normaliser at extract time) — the
		// full detection chain runs in TrimFrontMatter, which gets one
		const hasContentStart = blocks.some((b) => this.IsContentStart(b, null, rules));

		// the module-specific front-matter fields (Subject/Course/Module
		// Code/Key Contact/Date submitted) — Course backs up an English
		// title later (front_matter_metadata data rule)
		const metadata = this.#extractMetadata(blocks, rules);

		return { blocks, rels, mtkFlag, hasContentStart, metadata };
	};

	/**
	 * Is this block the content-start boundary?
	 * Detection chain per Input_Doc_Rules.content_start:
	 *  (1) LITERAL fragment ("title bar") — the standard template opener;
	 *  (2) CANONICAL resolution — Fundamentals templates open with
	 *      [Fundamental content]/[Fundamental 1 code] (canonical "lesson
	 *      content") or a bare [Title] instead (verified: ARFUN01, MXFUN03,
	 *      EXPFUN04 — one PageForge run even printed "[TITLE BAR] marker
	 *      not found"). Needs the normaliser, hence the parameter.
	 *
	 * @param {Object} block - a paraBlock
	 * @param {TagNormaliser|null} normaliser - for the canonical chain
	 * @param {Object} rules - Input_Doc_Rules.json (defaults to loaded)
	 * @returns {boolean}
	 */
	static IsContentStart(block, normaliser = null, rules = DataService.Data.InputDocRules) {
		if (block.kind !== "para") return false;
		const folded = Utils.Fold(block.text);

		// (1) the literal fragment — fast path, no normaliser needed
		if (rules.content_start.content_start_fragments.some((frag) =>
			new RegExp(`\\[\\s*${Utils.RegexEscape(frag)}\\s*\\]`).test(folded))) {
			return true;
		}

		// (2) canonical resolution of the block's RED spans only — black
		// text in front-matter tables ("Resource title" …) must never match
		if (!normaliser) return false;
		const canonicals = rules.content_start.content_start_canonicals ?? [];
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		for (const m of block.text.matchAll(RED)) {
			const primary = normaliser.Parse(m[1]).primary;
			if (primary && canonicals.includes(primary.tag)) return true;
		}
		return false;
	};

	/**
	 * Captures the FILLED module-specific front-matter fields from the gray
	 * info table ('Label: value' paragraphs), per front_matter_metadata.
	 * A bare 'Label:' (blank template row) is skipped.
	 *
	 * @param {Object[]} blocks
	 * @param {Object} rules - Input_Doc_Rules.json
	 * @returns {Object} { subject, course, moduleCode, keyContact, dateSubmitted } (only filled keys)
	 */
	static #extractMetadata(blocks, rules) {
		const cfg = rules.front_matter_metadata;
		if (!cfg) return {};
		const out = {};
		// labels checked longest-first so "key contact (name, email…)" wins
		// over a bare "key contact"
		const fieldByLabel = [];
		for (const [field, def] of Object.entries(cfg.fields)) {
			for (const label of def.labels) fieldByLabel.push([Utils.Fold(label), field]);
		}
		fieldByLabel.sort((a, b) => b[0].length - a[0].length);

		for (const b of blocks) {
			if (b.kind !== "para") continue;
			// the raw paragraph text without red markers / markdown
			const text = b.text.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "")
				.replace(/\*\*/g, "").trim();
			const colon = text.indexOf(":");
			if (colon < 0) continue;
			const labelFolded = Utils.Fold(text.slice(0, colon));
			const value = text.slice(colon + 1).trim();
			if (!value) continue;   // blank template row
			const hit = fieldByLabel.find(([l]) => labelFolded === l);
			if (hit && !out[hit[1]]) out[hit[1]] = value;
		}

		// TABLE-ROW metadata (ROUND 212 — the PNR family's MTK "Te Aka Taumatua"
		// template): its front matter carries the module info as a TABLE
		// ("Module Name | Ngā tau: 1 | Numbers: 1"), not "Label: value"
		// paragraphs, so the paragraph walk above never captured it. Only the
		// fields listed in table_row_fields are read from table rows —
		// deliberately NOT course/moduleCode, so the "Course is the title
		// backup" path can never start firing on modules where it never fired
		// before. The captured moduleName is the bilingual title source when
		// the module has no [TITLE BAR] payload (see PageAssembler).
		// Env toggle: REODROPMENU_OFF.
		const tableFields = new Set(cfg.table_row_fields ?? []);
		if (tableFields.size
			&& !(typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF)) {
			const clean = (s) => String(s ?? "")
				.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "")
				.replace(/\*\*/g, "").trim();
			for (const b of blocks) {
				if (b.kind !== "table") continue;
				for (const row of (b.rows ?? [])) {
					if (!Array.isArray(row) || row.length < 2) continue;
					const labelFolded = Utils.Fold(clean(row[0]));
					const hit = fieldByLabel.find(([l, f]) => labelFolded === l && tableFields.has(f));
					if (!hit) continue;
					const value = clean(row[1]);
					if (value && !out[hit[1]]) out[hit[1]] = value;
				}
			}
		}
		// ROUND 321 (the MTK title source): the TRR1xx table has NO Module Name row — the
		// Module Code cell carries the title after the code ("TRR108: Ngā Orokati Tuarua –
		// Final Consonants"). Keep that remainder as metadata.moduleCodeTitle for the
		// PageAssembler fallback. Data front_matter_metadata.title_in_code_cell; env MTKTITLES_OFF.
		const tic = cfg.title_in_code_cell;
		if (tic && tic.enabled !== false && Array.isArray(tic.labels)
			&& !(typeof process !== "undefined" && process.env && process.env.MTKTITLES_OFF)) {
			const clean2 = (s) => String(s ?? "").replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "").replace(/\*\*/g, "").trim();
			const want = new Set(tic.labels.map((l) => Utils.Fold(l)));
			for (const b of blocks) {
				if (b.kind !== "table" || out[tic.field ?? "moduleCodeTitle"]) continue;
				for (const row of (b.rows ?? [])) {
					if (!Array.isArray(row) || row.length < 2 || !want.has(Utils.Fold(clean2(row[0])))) continue;
					const m = /^\s*[A-Za-z]{2,8}\d{2,5}[A-Za-z]?\s*[:\u2013\u2014\-]?\s*(.+)$/.exec(clean2(row[1]));
					if (m && m[1].trim()) { out[tic.field ?? "moduleCodeTitle"] = m[1].trim(); break; }
				}
			}
		}
		return out;
	};

	/**
	 * ROUND 423 (session 31) — PAGE-BOUNDARY MARKERS TYPED AS TABLE ROWS ARE
	 * PARAGRAPHS (PMT101, the MTK "Te Aka Taumatua" template written as ONE
	 * table).
	 *
	 * WHY: PNR107 and the other MTK bilingual modules carry [MODULE CONTENT:
	 * PAGE 1] / [END OF PAGE] / [LESSON N CONTENT] / [END OF DROP DOWN MENU]
	 * as paragraphs BETWEEN one English ║ Māori table per page. PMT101's
	 * writer kept the whole module in one table and typed those markers as
	 * rows (the red span alone in the left cell, the right cell empty), so
	 * IsContentStart — paragraphs only — never saw a content start and the
	 * module was refused as "no Writers Template". Splitting the table at
	 * each such row and emitting the marker as a paraBlock turns PMT101's
	 * block stream into exactly PNR107's shape; recognition, the trim, the
	 * r212 drop-down rescue, the page splitter and the bilingual handlers
	 * then run unchanged.
	 *
	 * SCOPE (measured, outputs/_s31_r1_rowmarkers.cjs, all 545 docx-bearing
	 * gold modules): a row qualifies only when EVERY non-empty cell is
	 * exactly one red span resolving to a promote_tags canonical and nothing
	 * else. That fires on PMT101 alone (9 rows). The [TITLE BAR] ║ [TITLE BAR]
	 * rows of the 19 MTK modules are content rows and "title bar" is not a
	 * promote tag; a marker beside other cell text (ENGS202's page-opener
	 * table) never qualifies. Every untouched document gets the SAME array
	 * back — a no-op by construction.
	 *
	 * Data: Input_Doc_Rules.content_start.table_row_boundary_markers.
	 * Env: ROWMARKER_OFF.
	 *
	 * @param {Object[]} blocks - extracted blocks (tables carry .rows / .rowLinks)
	 * @param {TagNormaliser|null} normaliser - resolves the cell spans (required)
	 * @param {ConversionRun|null} run - note surfacing
	 * @returns {Object[]} the same array when nothing qualifies, else a new list
	 */
	static PromoteTableRowMarkers(blocks, normaliser, run = null) {
		const cfg = DataService?.Data?.InputDocRules?.content_start?.table_row_boundary_markers;
		if (!normaliser || !cfg || cfg.enabled === false || !Array.isArray(blocks)) return blocks;
		const envKey = cfg.env || "ROWMARKER_OFF";
		if (typeof process !== "undefined" && process.env && process.env[envKey]) return blocks;
		const tags = new Set(cfg.promote_tags ?? []);
		if (!tags.size || !blocks.some((b) => b && b.kind === "table")) return blocks;
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		const tm = DataService.Data.InputDocRules.table_markers;
		// the marker text of a qualifying row, else null
		const markerOf = (cells) => {
			let text = null;
			for (const c of cells) {
				const s = String(c ?? "").trim();
				if (!s) continue;
				const spans = [...s.matchAll(RED)];
				if (spans.length !== 1 || s.replace(RED, "").replace(/[\s*_]/g, "")) return null;
				const primary = normaliser.Parse(spans[0][1]).primary;
				if (!primary || !tags.has(primary.tag)) return null;
				text = text ?? s;
			}
			return text;
		};
		// a slice of the table between two markers; null when every row in the
		// slice is blank (the writer's spacer rows around a marker are not
		// content — emitted as a table they would stand between an [END OF
		// PAGE] and the next [LESSON N CONTENT] and trip the splitter's AR-5)
		const subTable = (src, from, to) => {
			const rows = src.rows.slice(from, to);
			if (!rows.some((cells) => (cells ?? []).some((c) => String(c ?? "").trim()))) return null;
			const rowLinks = (src.rowLinks ?? []).slice(from, to);
			const blk = {
				kind: "table", rows, rowLinks, links: rowLinks.flat(), wtPage: src.wtPage,
				text: [tm.open, ...rows.map((cells) => `${tm.row_prefix}${cells.join(tm.column_separator)}`), tm.close].join("\n"),
			};
			if (src.cellMarks) blk.cellMarks = src.cellMarks.slice(from, to);
			return blk;
		};
		let promoted = 0;
		const out = [];
		for (const b of blocks) {
			if (!b || b.kind !== "table" || !Array.isArray(b.rows)) { out.push(b); continue; }
			const cuts = [];
			b.rows.forEach((cells, i) => {
				const text = Array.isArray(cells) ? markerOf(cells) : null;
				if (text) cuts.push([i, text]);
			});
			if (!cuts.length) { out.push(b); continue; }
			let from = 0;
			const push = (blk) => { if (blk) out.push(blk); };
			for (const [i, text] of cuts) {
				if (i > from) push(subTable(b, from, i));
				out.push({ kind: "para", text, links: [], wtPage: b.wtPage, list: "", listLevel: 0 });
				from = i + 1;
				promoted++;
			}
			if (from < b.rows.length) push(subTable(b, from, b.rows.length));
		}
		if (!promoted) return blocks;
		run?.AddNote("info", "DocxExtractor",
			`${promoted} page-boundary marker(s) typed as table rows promoted to paragraphs — the one-table MTK template (round 423; env ${envKey} reverts).`);
		return out;
	};

	/**
	 * ROUND 424 (session 31) — IS THIS DOCUMENT THE ACTIVITY-TABLE DIALECT?
	 * The XOTP reader family carries no red tags at all: its structure is one
	 * two-column table whose header row reads "Section heading | Text/Activity"
	 * (the table opens with a merged title row, so the header may be the second
	 * row — `scan_rows`). True when any table's first `scan_rows` rows hold a
	 * row whose first two non-empty cells fold to that header pair. Measured
	 * over all 762 corpus docx: exactly the 12 XOTP Writers Templates.
	 * Same test as the parsed-text tab's OutputFormatter.ACTIVITY_TABLE_NOTICE
	 * (round 409). Data: Input_Doc_Rules.input_shapes.activity_table.
	 * Env: ACTTABLE_OFF.
	 *
	 * @param {Object[]} blocks
	 * @param {Object} rules - Input_Doc_Rules.json (defaults to loaded)
	 * @returns {boolean}
	 */
	static IsActivityTableDoc(blocks, rules = DataService.Data.InputDocRules) {
		const cfg = rules?.input_shapes?.activity_table;
		if (!cfg || cfg.enabled === false || !Array.isArray(blocks)) return false;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "ACTTABLE_OFF"]) return false;
		const want = (cfg.header ?? []).map((h) => Utils.Fold(h).replace(/[*_]/g, "").replace(/\s+/g, " ").trim());
		if (want.length < 2) return false;
		const scan = Math.max(1, cfg.scan_rows ?? 3);
		const fold = (c) => Utils.Fold(String(c ?? "")).replace(/[*_]/g, "").replace(/\s+/g, " ").trim();
		return blocks.some((b) => b && b.kind === "table" && Array.isArray(b.rows)
			&& b.rows.slice(0, scan).some((row) => {
				const cells = (Array.isArray(row) ? row : []).map(fold).filter((c) => c.length);
				return cells.length >= 2 && cells[0] === want[0] && cells[1] === want[1];
			}));
	};

	/**
	 * ROUND 425 (session 31) — THE ACTIVITY-TABLE ADAPTER: turns the XOTP
	 * reader family's "Section heading | Text/Activity" table into the
	 * synthetic red-tag paragraph stream the whole existing pipeline already
	 * speaks, so no builder, menu shell or page-splitter rule is new. The
	 * mapping is DATA (Input_Doc_Rules.input_shapes.activity_table.adapter):
	 *   - the title row → [TITLE BAR] + the title;
	 *   - the Overview row → each lesson page's [Lesson Overview] block (the
	 *     writer's "(dropdown at top right)" IS the lesson-page module menu;
	 *     the gold has no overview page);
	 *   - Introduction → [H2] + [Body]; Online book → [Carousel] (+ the story
	 *     questions when the writer put them in the same row); Questions →
	 *     [alert] [H3] + the numbered lines (the r337 <ol>);
	 *   - a numbered row → [Activity N] (lettered) / a bare [Activity] (the
	 *     r400 positional letter), the section heading as [H2] when the row
	 *     also carries its own title, [H3], the instruction line, the widget
	 *     invocation the section's words name (widget_hints — the heading
	 *     decides, a CS: line only confirms), then the payload;
	 *   - Share with your kaiako → [Activity] [H3] + the two [button]s (the
	 *     r305 dropbox post-pass adds the class token);
	 *   - Quiz + the nested "I can" table → nothing (the D2L self-assessment
	 *     quiz, spec §3.2), recorded in a note;
	 *   - the page break: lettered labels break where the lesson digit
	 *     changes, bare numbers after the data-declared row (spec §3.3).
	 * A wholly parenthetical line is the writer's instruction to the
	 * developer — emitted as a red bracket-less span (an instruction to the
	 * normaliser, a Writers Note on the page, gate-invisible); a CS: line stays
	 * a plain paragraph for the r219 addressee-prefix scheme. The reader book
	 * (carousel images, matching sentences, credits) is in none of the
	 * documents: those widgets ship as the standard hand-off placeholders.
	 * Called from ModuleResolver.PrepareRun for a document IsActivityTableDoc
	 * accepted; every other document never reaches it. Env: ACTTABLEADAPT_OFF.
	 *
	 * @param {Object[]} blocks - the extracted blocks (one table carries the module)
	 * @param {TagNormaliser|null} normaliser - unused today (the stream is literal)
	 * @param {ConversionRun|null} run - note surfacing
	 * @returns {Object[]} the adapted block list (the same array when nothing applies)
	 */
	static AdaptActivityTable(blocks, normaliser, run = null) {
		const rules = DataService?.Data?.InputDocRules;
		const cfg = rules?.input_shapes?.activity_table;
		const ad = cfg?.adapter;
		if (!cfg || !ad || ad.enabled !== true || !Array.isArray(blocks)) return blocks;
		if (typeof process !== "undefined" && process.env && process.env[ad.env || "ACTTABLEADAPT_OFF"]) return blocks;
		const ti = blocks.findIndex((b) => b && b.kind === "table" && this.IsActivityTableDoc([b], rules));
		if (ti < 0) return blocks;
		const tbl = blocks[ti];
		const brk = rules.table_markers?.in_cell_line_break ?? " / ";
		const RED = (s) => `\u{1f534}[RED TEXT] ${s} [/RED TEXT]\u{1f534}`;
		const TAG = (t) => RED(`[${t}]`);
		const fold = (s) => Utils.Fold(String(s ?? "")).replace(/[*_]/g, "").replace(/\s+/g, " ").trim();
		const plain = (s) => String(s ?? "").replace(/\*\*|__/g, "").replace(/\s+/g, " ").trim();
		const lines = (cell) => String(cell ?? "").split(brk).map((s) => s.trim()).filter(Boolean);
		const re = (p, f = "i") => new RegExp(p, f);
		const sep = ad.heading_pair_separator ?? " | ";
		const titleReject = re(ad.title_line_reject ?? "^(cs:|to cs:|instruction|\\()");
		const titleMaxW = ad.title_line_max_words ?? 6;
		const stripPrefixes = (ad.strip_line_prefixes ?? ["instruction:"]).map((p) => fold(p));
		const paren = (s) => /^\(.*\)$/.test(plain(s));
		const isCs = (s) => re(ad.cs_line_pattern ?? "^(to\\s+)?cs\\s*:").test(plain(s));
		const isImage = (s) => /^\[IMAGE:/i.test(String(s).trim());
		const instructionLine = (s) => stripPrefixes.some((p) => fold(s).startsWith(p));
		const stripInstruction = (s) => {
			const f = fold(s); const p = stripPrefixes.find((x) => f.startsWith(x));
			if (!p) return s;
			return String(s).replace(re("^\\s*(\\*\\*)?" + p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\s*(\\*\\*)?\\s*"), "").trim();
		};
		const isTitleLine = (s, maxW = titleMaxW) => {
			const t = plain(s);
			if (!t || titleReject.test(fold(t)) || isImage(t)) return false;
			if (/[.:;]$/.test(t)) return false;
			return t.split(/\s+/).length <= maxW;
		};
		const leftInstr = re(ad.instruction_line_pattern ?? "^(insert|create|reproduce|please)\\b");
		// ---- the rows ---------------------------------------------------------
		const rows = tbl.rows ?? [];
		const want = (cfg.header ?? []).map((h) => fold(h));
		const hdr = rows.findIndex((r) => { const c = (r ?? []).map(fold).filter(Boolean); return c.length >= 2 && c[0] === want[0] && c[1] === want[1]; });
		if (hdr < 0) return blocks;
		let title = "";
		for (let r = 0; r < hdr && !title; r++) {
			const t = plain((rows[r] ?? []).filter((c) => String(c ?? "").trim()).join(" "));
			for (const p of (ad.title_patterns ?? [])) { const m = re(p).exec(t); if (m && m[2]) { title = m[2].trim(); break; } }
			if (!title && t) title = t;
		}
		const out = [];
		const push = (text, links) => out.push({ kind: "para", text, links: (links ?? []).slice(), wtPage: tbl.wtPage, list: "", listLevel: 0 });
		push(TAG("TITLE BAR") + (title ? `**${title}**` : ""), tbl.links);
		let overview = [], overviewLinks = [];
		let lessonNo = 0, bareCount = 0, skipped = 0, activities = 0, pageOpen = false;
		const breakAfter = ad.page_break?.bare_numbers_break_after ?? 3;
		const openLesson = (n, links) => {
			if (pageOpen) push(TAG("End page"), []);
			lessonNo = n; pageOpen = true;
			push(TAG(`LESSON ${n}`), []);
			if (overview.length) {
				push(TAG(ad.lesson_overview_tag ?? "Lesson Overview"), overviewLinks);
				for (const l of overview) push(l, overviewLinks);
			}
		};
		const ensurePage = (links) => { if (!pageOpen) openLesson(1, links); };
		const emitBody = (ls, links, first = true) => {
			for (const l of ls) {
				if (fold(l) === "instruction:" || fold(l) === "instruction") continue;
				if (paren(l) && ad.parenthetical_as_instruction !== false) { push(RED(plain(l)), links); continue; }
				const s = stripInstruction(l);
				if (!s) continue;
				// a `CS:` / `To CS:` line is the writer's note to Creative Services — a RED span, so the
				// standard instruction path renders it as the Writers Note (data cs_lines_as_instruction)
				if (isCs(s) && ad.cs_lines_as_instruction !== false) { push(RED(plain(s)), links); continue; }
				if (first && !isImage(s) && !isCs(s)) { push(TAG("Body") + s, links); first = false; }
				else push(s, links);
			}
			return first;
		};
		const emitQuestions = (ls, links) => {
			const qs = ls.filter((l) => !/^instruction:?$/.test(fold(l)));
			let t = ad.questions_title_default ?? "Story questions";
			if (qs.length && isTitleLine(qs[0], ad.questions_title_max_words ?? 4)) t = plain(qs.shift());
			// the title rides the alert tag as its embedded lead (the callout's own lead element — the family's
			// alert variant fixes it at h3) unless questions_title_as_lead is false; the extractor marks every
			// cell list "• " (a cell carries no numFmt), so questions_list "numbered" restores the writer's
			// decimal list (verified in the docx: numId → decimal) and renderBlackText builds the <ol>
			const asLead = ad.questions_title_as_lead !== false;
			push(asLead ? RED(`[${ad.alert_tag ?? "alert"}] ${t}`) : TAG(ad.alert_tag ?? "alert"), links);   // the lead INSIDE the span
			if (!asLead) push(TAG("H3") + t, links);
			const numbered = ad.questions_list === "numbered";
			emitBody(numbered ? qs.map((l) => String(l).replace(/^\s*\u2022\s+/, "1. ")) : qs, links);
			push(TAG("End alert"), links);
		};
		const hintFor = (text) => {
			const f = fold(text);
			for (const h of (ad.widget_hints ?? [])) if (re(h.match).test(f)) return h.tag;
			return null;
		};
		for (let r = hdr + 1; r < rows.length; r++) {
			const cells = (rows[r] ?? []).map((c) => String(c ?? ""));
			const nonEmpty = cells.filter((c) => c.trim());
			if (!nonEmpty.length) continue;
			const links = tbl.rowLinks?.[r] ?? [];
			const left = cells.length >= 2 ? cells[0] : "";
			const right = cells.length >= 2 ? cells.slice(1).join(brk) : cells[0];
			const leftLines = lines(left).filter((l) => !paren(l));
			const leftFold = leftLines.map(fold).join(" / ");
			let sec = null;
			for (const s of (ad.sections ?? [])) { if (re(s.match).test(leftFold)) { sec = s; break; } }
			const role = sec?.role ?? null;
			if (role === "skip") {
				skipped++;
				if (sec.terminal) { skipped += rows.length - r - 1; break; }   // the nested "I can" rows follow the Quiz row
				continue;
			}
			const rightLines = lines(right);
			if (role === "overview") {
				overview = rightLines.slice(); overviewLinks = links;
				// the row's own left-cell label ("Overview") leads the menu as a bold label (the gold's first
				// `<h3><span>Overview</span></h3>`, 24 / 24 pages) — data overview_label_from_cell
				const lab = ad.overview_label_from_cell !== false ? plain(leftLines[0] ?? "") : "";
				if (lab && !/^\*\*/.test(String(overview[0] ?? "").trim())) overview.unshift(`**${lab}**`);
				continue;
			}
			ensurePage(links);
			if (role === "introduction") {
				push(TAG("H2") + leftLines.map(plain).join(sep), links);
				emitBody(rightLines, links);
				continue;
			}
			if (role === "online_book") {
				const splitRe = re(ad.online_book_questions_split ?? "^instruction");
				const k = rightLines.findIndex((l) => splitRe.test(fold(l)));
				const before = k < 0 ? rightLines : rightLines.slice(0, k);
				const after = k < 0 ? [] : rightLines.slice(k);
				push(TAG("Carousel"), links);
				for (const l of before) push(paren(l) ? RED(plain(l)) : l, links);
				if (after.length) emitQuestions(after, links);
				continue;
			}
			if (role === "questions") { emitQuestions(rightLines, links); continue; }
			if (role === "share") {
				push(TAG("Activity"), links);
				push(TAG("H3") + leftLines.map(plain).join(sep), links);
				const btnRe = re(ad.button_line_pattern ?? "\\bbutton\\b");
				const body = [], buttons = [];
				for (const l of rightLines) {
					const t = String(l).replace(/\*\*|__|\*/g, "").trim();
					if (btnRe.test(t)) {
						// "Upload to dropbox button   Go to assessment quiz button" → one [button] per label
						for (const part of t.split(re(ad.button_split ?? "\\bbutton\\b", "i"))) {
							const lab = part.replace(/\s+/g, " ").trim();
							if (lab) buttons.push(lab);
						}
					} else body.push(l);
				}
				emitBody(body, links);
				for (const b of buttons) push(TAG("button") + " " + b, links);
				continue;
			}
			// ---- an activity row (numbered, or a section heading with no role) ----
			const labelLine = leftLines.find((l) => /^\d+[a-z]?$/i.test(plain(l)));
			let label = labelLine ? plain(labelLine).toUpperCase() : null;
			if (!label) { const m = /^(\d+[a-z]?)\b/i.exec(plain(leftLines[0] ?? "")); if (m) label = m[1].toUpperCase(); }
			const headingLines = leftLines.filter((l) => l !== labelLine && !/^\d+[a-z]?\b\s*$/i.test(plain(l)) && !leftInstr.test(fold(l)));
			const leftInstrLines = leftLines.filter((l) => leftInstr.test(fold(l)));
			const leftHeading = headingLines.map((l) => plain(l).replace(/^\d+[a-z]?\s+/i, "")).filter(Boolean).join(sep);
			const lettered = !!label && /[a-z]$/i.test(label);
			if (lettered) {
				const digit = parseInt(label, 10);
				if (digit > lessonNo) openLesson(digit, links);
			} else if (label) {
				bareCount++;
				if (bareCount === breakAfter + 1) openLesson(lessonNo + 1, links);
			}
			const rest = rightLines.slice();
			let rightTitle = null;
			if (rest.length && isTitleLine(rest[0])) rightTitle = plain(rest.shift());
			let h3 = null;
			if (leftHeading && rightTitle) { push(TAG("H2") + leftHeading, links); h3 = rightTitle; }
			else h3 = rightTitle || leftHeading || null;
			push(lettered ? TAG(`Activity ${label}`) : TAG("Activity"), links);
			activities++;
			if (h3) push(TAG("H3") + h3, links);
			for (const l of leftInstrLines) push(RED(plain(l)), links);
			const widget = hintFor(left + brk + right);
			const instr = rest.filter((l) => instructionLine(l));
			const payload = rest.filter((l) => !instructionLine(l));
			let first = emitBody(instr, links, true);
			if (widget) push(TAG(widget), links);
			emitBody(payload, links, first && !widget);
		}
		if (!pageOpen) {
			run?.AddNote("warn", "DocxExtractor", "Activity-table template: no body row recognised — the document was left as extracted.");
			return blocks;
		}
		push(TAG("End page"), []);
		run?.AddNote("info", "DocxExtractor",
			`Activity-table template adapted (round 425): ${activities} activity box(es) over ${lessonNo} page(s), the Overview row as each page's menu, `
			+ `${skipped} row(s) not emitted (the Quiz / 'I can' self-assessment rows are the D2L quiz, never a page); the reader book's images and matching `
			+ `sentences are not in the document — those widgets ship as hand-off boxes. Env ${ad.env || "ACTTABLEADAPT_OFF"} reverts.`);
		return [...blocks.slice(0, ti), ...out, ...blocks.slice(ti + 1)];
	};

	/**
	 * Is this document a Writers Template at all? True when any block is a
	 * recognised content start, OR the fallback applies (a red span
	 * resolving to a structural directive — bare-[H1] openers).
	 * Used by the upload classifier; TrimFrontMatter then finds the spot.
	 *
	 * @param {Object[]} blocks
	 * @param {TagNormaliser} normaliser
	 * @returns {boolean}
	 */
	static LooksLikeWritersTemplate(blocks, normaliser) {
		if (blocks.some((b) => this.IsContentStart(b, normaliser))) return true;
		const fallback = DataService.Data.InputDocRules.content_start
			.content_start_fallback_directives ?? [];
		if (!normaliser || !fallback.length) return false;
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		return blocks.some((b) => b.kind === "para"
			&& [...b.text.matchAll(RED)].some((m) =>
				fallback.includes(normaliser.Parse(m[1]).primary?.directive)));
	};

	/**
	 * Drops everything before the first content-start block.
	 *
	 * WHY: everything before the opener is generic template front-matter
	 * (submission checklist, LOT tags, Section A/B…) — out of scope by rule:
	 * not interpreted, not converted, not flagged.
	 *
	 * FALLBACK (chain step 3): when no opener exists at all, ALL blocks are
	 * returned and the caller must surface a loud warning — PageForge's own
	 * behaviour for these rare templates.
	 *
	 * @param {Object[]} blocks - all extracted blocks
	 * @param {TagNormaliser|null} normaliser - for the canonical chain
	 * @param {ConversionRun|null} run - surfacing
	 * @returns {Object[]} blocks from the boundary onward
	 */
	static TrimFrontMatter(blocks, normaliser = null, run = null) {
		let result = null;
		let start = blocks.findIndex((b) => this.IsContentStart(b, normaliser));

		// DROP-DOWN-MENU OPENER RESCUE (ROUND 212 — the MTK "Te Aka Taumatua"
		// bilingual template, the PNR101/102/104 family). That template has NO
		// paragraph-level [TITLE BAR] at all (its [TITLE BAR] tags live inside
		// TABLE cells, which the standard chain never sees), so the first
		// standard content-start found is the [LESSON 1 CONTENT] marker — and
		// everything before it (the "[Content for DROP DOWN MENU]" module-menu
		// section + the [MODULE CONTENT: PAGE 1] introduction) was silently
		// trimmed away as front matter: the module shipped an EMPTY overview.
		// RESCUE: when the standard start is a LESSON-CONTENT start (NOT a
		// title-bar one) and a "[Content for DROP DOWN MENU]" paragraph exists
		// EARLIER, the document opens there instead. Scoping matters: a module
		// whose standard start IS a [TITLE BAR] paragraph (the TRR203/TRR301
		// shape — same marker family, but their title bar is already visible to
		// the standard chain) is left completely unchanged.
		// Data: content_start.content_start_fragments_dropdown.
		// Env toggle: REODROPMENU_OFF.
		if (start >= 0
			&& !(typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF)) {
			const rules = DataService.Data.InputDocRules;
			const ddFrags = rules.content_start.content_start_fragments_dropdown ?? [];
			if (ddFrags.length) {
				const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
				// is the found standard start a TITLE-BAR start? (literal fragment
				// or a red span resolving to the "title bar" canonical)
				const sb = blocks[start];
				const sbFolded = Utils.Fold(sb.text);
				let titleBarStart = /\[\s*title bar\s*\]/.test(sbFolded);
				if (!titleBarStart && normaliser) {
					titleBarStart = [...sb.text.matchAll(RED)].some((m) =>
						normaliser.Parse(m[1]).primary?.tag === "title bar");
				}
				if (!titleBarStart) {
					const dd = blocks.findIndex((b) => b.kind === "para"
						&& ddFrags.some((frag) =>
							new RegExp(`\\[\\s*${Utils.RegexEscape(frag)}\\s*\\]`).test(Utils.Fold(b.text))));
					if (dd >= 0 && dd < start) {
						run?.AddNote("info", "DocxExtractor",
							"Content opened at the [Content for DROP DOWN MENU] marker — the MTK drop-down-menu bilingual template (its overview lives before the first [LESSON N CONTENT]).");
						start = dd;
					}
				}
			}
		}
		if (start >= 0) result = blocks.slice(start);

		// last chance (data rule content_start_fallback_directives): the
		// first red span resolving to a structural directive opens the
		// document — some templates begin at a bare [H1] (EXPFUN06).
		if (result === null) {
			const rules = DataService.Data.InputDocRules;
			const fallback = rules.content_start.content_start_fallback_directives ?? [];
			if (normaliser && fallback.length) {
				const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
				const idx = blocks.findIndex((b) => b.kind === "para"
					&& [...b.text.matchAll(RED)].some((m) =>
						fallback.includes(normaliser.Parse(m[1]).primary?.directive)));
				if (idx >= 0) {
					run?.AddNote("warn", "DocxExtractor",
						"No [TITLE BAR]/[Fundamental content] opener — content started at the first structural tag instead; check the first page for stray front-matter.");
					result = blocks.slice(idx);
				}
			}
		}

		if (result === null) {
			run?.AddNote("warn", "DocxExtractor",
				"No content-start tag found at all — converting ALL blocks; front-matter may leak into the output. Review the source template.");
			result = blocks;
		}

		// ROUND 306 — a PAGE-LAYOUT table that traps a speech bubble beside an
		// [Activity] dissolves into ordinary stacked blocks (the human's own
		// answer). Runs BEFORE the bracket repair below, so a dissolved cell's
		// "Activity]" typo is repaired like any other paragraph's.
		result = this.DissolveBubbleLayoutTables(result, normaliser, run);

		// Some writers accidentally drop the opening square bracket off a tag
		// — e.g. typing "H2] Know:" instead of "[H2] Know:". Repair that here,
		// once, before any other part of the pipeline reads these blocks.
		return this.RepairContentTags(result, normaliser, run);
	};

	/**
	 * ROUND 370 — DROPS THE MEDIA-LIST PREAMBLE OF A COMBINED DOCUMENT.
	 *
	 * WHY: in a combined "Writers Template + Media List" docx the media-list
	 * section opens after the last content page with a red "MEDIA LIST"
	 * heading, the red "Please supply details for ALL external media …"
	 * instruction and a plain-text copyright-clearance bullet ("If a specific
	 * third-party item/image is crucial to your writing, then please submit
	 * this for early copyright clearance …" with its sharepoint link), and
	 * only then the media TABLE. PrepareRun excluded the table alone, so the
	 * preamble flowed into the last lesson page: the two red runs became
	 * Writers Notes and the bullet rendered as learner-facing body text on
	 * 136 pages / 134 modules. The human gold ships it on 0 pages.
	 *
	 * HOW: walking BACKWARDS from the media table, a paragraph block that is
	 * blank, whose folded text (red markers stripped) equals a phrases_exact
	 * entry, or contains a phrases_contains entry, is part of the preamble;
	 * the walk stops at the first block matching none, and at max_blocks.
	 * The preamble and the table are removed together; at least one phrase
	 * hit is required (blank lines alone never trigger it). A separate Media
	 * List docx is untouched by construction: its table is not among the
	 * Writers Template's own blocks, so the walk never starts.
	 *
	 * The TAIL: the template's SUBMISSION CHECKLIST ("Have you: ☐ Completed
	 * Section A …") follows the table on 81 of the 277 combined WTs and rendered
	 * as learner-facing text on 22 pages (gold 0). It is dropped with the table
	 * when the first non-blank block after the table opens with a
	 * tail_start_phrases entry AND every block to the end of the document is a
	 * paragraph carrying no red span that resolves to a structural tag other
	 * than [body] — the PageSplitter AR-5 substance test — so a media table
	 * placed MID-document (MXFUN01/02/03: Phase 2 content follows it) keeps its
	 * tail by construction.
	 *
	 * Data: Input_Doc_Rules.media_list_preamble   Env toggle: MLPREAMBLE_OFF
	 *
	 * @param {Object[]} blocks - the WT's blocks (after TrimFrontMatter)
	 * @param {Object|null} tableBlock - the media table block, if any
	 * @param {ConversionRun|null} run - surfacing
	 * @param {TagNormaliser|null} normaliser - for the tail's substance test
	 * @param {Object|null} legacyTable - the pre-r370 exclusion (the mediaSource's
	 *        table block, whichever document it came from); the OFF path drops
	 *        exactly that and nothing else, so the toggle reverts byte-for-byte
	 * @returns {Object[]} blocks minus the table, its preamble and its tail
	 */
	static TrimMediaListPreamble(blocks, tableBlock, run = null, normaliser = null, legacyTable = tableBlock) {
		const cfg = DataService.Data.InputDocRules.media_list_preamble;
		const on = cfg && cfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.MLPREAMBLE_OFF);
		if (!on) return blocks.filter((b) => b !== legacyTable);
		const withoutTable = blocks.filter((b) => b !== tableBlock && b !== legacyTable);
		const idx = tableBlock ? blocks.indexOf(tableBlock) : -1;
		const exact = (cfg.phrases_exact ?? []).map((p) => Utils.Fold(String(p)));
		const contains = (cfg.phrases_contains ?? []).map((p) => Utils.Fold(String(p)));
		const maxBack = cfg.max_blocks ?? 8;
		const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
		const REDSPAN = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		// red markers and the extractor's **bold** / *italic* / __link__ markers are
		// not words — "**SUBMISSION CHECKLIST**" must read as "submission checklist"
		const folded = (b) => Utils.Fold(String(b.text ?? "").replace(RED, " ").replace(/[*_]+/g, ""));
		const isPhrase = (b) => {
			if (b.kind !== "para") return false;
			const t = folded(b);
			return !!t && (exact.includes(t) || contains.some((p) => t.includes(p)));
		};
		const isBlank = (b) => b.kind === "para" && !folded(b);
		const isPreamble = (b) => isBlank(b) || isPhrase(b);
		// A writer's OWN note to the designer inside the media-list section ("Designer
		// and Copyright: many of the requested images are taken as a still shot …",
		// TWHK901; "Note- I have added the twinkl resource links …", ENGI401) is a block
		// made only of red spans that resolve to no structural tag: the walk passes
		// OVER it (so the boilerplate before it is still found) but KEEPS it — it is
		// the writer's instruction, which renders as the standing Writers Note.
		const structuralAny = new Set(["ELEMENT", "INTERACTIVE", "CONTAINER_OPEN", "CONTAINER_CLOSE", "PAGE_BOUNDARY", "SECTION_MARKER"]);
		const isRedNote = (b) => {
			if (!normaliser || b.kind !== "para") return false;
			const raw = String(b.text ?? "");
			if (!raw.trim() || raw.replace(REDSPAN, "").trim()) return false;   // black words → not a pure note
			for (const m of raw.matchAll(REDSPAN)) {
				const p = normaliser.Parse(m[1]).primary;
				if (p && structuralAny.has(p.directive)) return false;
			}
			return true;
		};
		// A short plain LABEL the writer puts on a media table ("Phase 1" / "Phase 2",
		// MXFUN03) is part of the media-list section: passed over BETWEEN the table and
		// the preamble (never above the preamble — a short line there is content).
		const labelMax = cfg.label_max_words ?? 3;
		const isShortLabel = (b) => {
			if (b.kind !== "para" || isPreamble(b)) return false;
			const n = folded(b).split(" ").filter(Boolean).length;
			return n > 0 && n <= labelMax && !/\u{1f534}/u.test(String(b.text ?? ""));
		};
		// a SECOND media table (the writer split the list by phase) is recognised by
		// the same column test the media-list parser uses
		const isMediaTable = (b) => b.kind === "table" && typeof MediaListParser !== "undefined"
			&& !!MediaListParser.FindMediaTable([b]);
		const keep = new Set();   // pass-through red notes inside the walked range
		let start, end, tailFrom, nExtra = 0, headed = false;
		if (idx >= 0) {
			// ---- the preamble: walk backwards from the table ----------------------
			start = idx;
			let seenPhrase = false;
			while (start > 0 && idx - start < maxBack) {
				const b = blocks[start - 1];
				if (isPhrase(b)) { seenPhrase = true; start--; continue; }
				if (isBlank(b)) { start--; continue; }
				if (isRedNote(b)) { keep.add(b); start--; continue; }
				if (!seenPhrase && isShortLabel(b)) { start--; continue; }
				break;
			}
			// a run of blank lines / labels / notes alone is never a preamble — one phrase hit is required
			if (!blocks.slice(start, idx).some(isPhrase)) { start = idx; keep.clear(); }
			end = idx;
			// ---- further media tables directly after the first ---------------------
			if (cfg.tail_extra_media_tables !== false) {
				let k = idx + 1, last = idx;
				while (k < blocks.length && (isBlank(blocks[k]) || isShortLabel(blocks[k]) || isMediaTable(blocks[k]))) {
					if (isMediaTable(blocks[k])) last = k;
					k++;
				}
				if (last > idx) { nExtra = last - idx; end = last; }
			}
			tailFrom = end + 1;
		} else {
			// ---- no media table in this document: the heading + preamble alone -----
			// (the table is in a separate Media List docx — the CHFUN family; the WT
			// still carries the template's 'MEDIA LIST' heading and its instructions)
			if (cfg.no_table_heading === false) return withoutTable;
			const h = blocks.findIndex((b) => b.kind === "para" && exact.includes(folded(b)));
			if (h < 0) return withoutTable;
			let e = h;
			while (e + 1 < blocks.length && e - h < maxBack) {
				const b = blocks[e + 1];
				if (isPreamble(b)) { e++; continue; }
				if (isRedNote(b)) { keep.add(b); e++; continue; }
				break;
			}
			// the heading alone is not enough — a boilerplate phrase must follow it
			if (!blocks.slice(h + 1, e + 1).some((b) => !keep.has(b) && isPhrase(b) && contains.some((p) => folded(b).includes(p)))) return withoutTable;
			start = h; end = e; tailFrom = e + 1; headed = true;
		}
		// ---- the tail: the submission checklist to the end of the document ----
		let nTail = 0;
		if (cfg.tail_drop !== false && normaliser) {
			const tailStarts = (cfg.tail_start_phrases ?? []).map((p) => Utils.Fold(String(p)));
			const structural = new Set(cfg.tail_structural_directives
				?? ["ELEMENT", "INTERACTIVE", "CONTAINER_OPEN", "CONTAINER_CLOSE", "PAGE_BOUNDARY", "SECTION_MARKER"]);
			const tail = blocks.slice(tailFrom);
			const firstText = tail.map(folded).find((t) => t) ?? "";
			const opensTail = tailStarts.some((p) => firstText.startsWith(p));
			const hasSubstance = (b) => {
				if (b.kind !== "para") return true;
				for (const m of String(b.text ?? "").matchAll(REDSPAN)) {
					const p = normaliser.Parse(m[1]).primary;
					if (p && structural.has(p.directive) && p.tag !== "body") return true;
				}
				return false;
			};
			if (opensTail && tail.length && !tail.some(hasSubstance)) { nTail = blocks.length - tailFrom; end = blocks.length - 1; }
		}
		if (!headed && start >= idx && end <= idx) return withoutTable;
		const nPre = headed ? (end - start + 1 - nTail - keep.size) : (idx - start - keep.size);
		const plural = (n) => `${n} block${n === 1 ? "" : "s"}`;
		run?.AddNote("info", "DocxExtractor",
			`Media-list boilerplate dropped: ${plural(nPre)} `
			+ (headed ? "of the media-list heading and preamble (no media table recognised in this document)" : "before the media table")
			+ (nExtra ? ` and ${plural(nExtra)} after it (a second media table)` : "")
			+ (nTail ? ` and ${plural(nTail)} after it (the submission checklist)` : "")
			+ (keep.size ? `; ${keep.size} writer note${keep.size === 1 ? "" : "s"} in that section kept` : "")
			+ ` — the template's own instructions, not content.`);
		return blocks.filter((b, k) => b !== tableBlock && b !== legacyTable && (keep.has(b) || k < start || k > end));
	};

	/**
	 * ROUND 306 — DISSOLVES A PAGE-LAYOUT TABLE THAT TRAPS A SPEECH BUBBLE.
	 *
	 * WHAT PROBLEM THIS SOLVES:
	 * One writer family (measured: EXACTLY TEDC402, 12 tables corpus-wide) lays a
	 * whole lesson activity out inside a two-column table — the [Activity] with its
	 * heading/instructions in one cell, the character picture + [speech bubble] in
	 * the other. The bubble's collector took the whole table, met the [Activity]
	 * marker, and correctly concluded "not a bubble layout" — so BOTH cells shipped
	 * inside a developer hand-off box. The human developer's own answer is to THROW
	 * THE TABLE AWAY: the finished page ships the two cells as two ordinary stacked
	 * blocks in reading order — a normal activity box, then a normal bubble row
	 * (TEDC402-1.0, byte-verified in the round-306 brief).
	 *
	 * HOW: a qualifying table's cells become ordinary paragraph blocks, one block
	 * per cell in reading order, with the in-cell line-break marker restored to a
	 * plain newline (the round-227 soft-break form every downstream reader already
	 * handles). Every existing mechanism then does the rest: the [Activity] opener
	 * opens its box, and the [Image]+[speech bubble] cell is EXACTLY the one-
	 * paragraph avatar dialect round 246's no-table bubble builder already builds
	 * on this very module's free-body pages.
	 *
	 * THE FENCE IS MEASURED, NOT GUESSED (outputs/_measure_r306_layouttables.cjs,
	 * all 454 modules): a table dissolves ONLY when its red spans resolve to BOTH
	 * an ACTIVITY-family CONTAINER_OPEN marker AND a speech-bubble INTERACTIVE
	 * invocation. "Activity marker alone" would have fired on ~120 tables across
	 * ~20 modules — the bilingual TRR embedded-activity tables, the fundamentals
	 * accordion/slide tables, CEDO501's round-305 quiz tables — every one of which
	 * must STAY a table. Both-markers fires on 12 tables, ALL TEDC402. A table
	 * carrying any PAGE_BOUNDARY / SECTION_MARKER span never dissolves (exposing an
	 * in-cell [End page] to the page splitter would churn pagination — the ENGS202
	 * page-opener class stays exactly as it is).
	 *
	 * ROUND 313 adds the SECOND qualifying shape, and it needs no proxy at all: a
	 * ONE-ROW ONE-CELL table has no second cell for data to sit in, so an activity
	 * marker inside one is a box the writer drew, not widget data. Measured over all
	 * 454 WTs that shape is 7 tables / 5 modules; the 3 reo ones are excluded (the
	 * r145/r167 class — reoMode routes tables through the bilingual handlers) leaving
	 * ENGI400 x2, HPFUN903 and TEDC402, every one gold-verified to ship no table.
	 * The other generalisation — "any INTERACTIVE invocation, not just a bubble" —
	 * was measured and DECLINED: it fires on 35 tables and 23 of those are genuine
	 * DATA tables (CEDO501's r305 quiz grids, flipCard front/back tables, drag-and-drop
	 * option grids, the TRR English|Te Reo pairs). The tag is not the discriminator.
	 *
	 * Data: Input_Doc_Rules.tables.bubble_layout_dissolve (+ .single_cell).
	 * Env: SBLAYOUT_OFF (whole rule) / SBSINGLECELL_OFF (the r313 arm alone).
	 *
	 * @param {Object[]} blocks - content blocks (tables carry .rows / .rowLinks)
	 * @param {TagNormaliser|null} normaliser - resolves the cell spans (required)
	 * @param {ConversionRun|null} run - note surfacing
	 * @returns {Object[]} a new block list with qualifying tables dissolved
	 */
	static DissolveBubbleLayoutTables(blocks, normaliser, run = null) {
		const cfg = DataService?.Data?.InputDocRules?.tables?.bubble_layout_dissolve;
		if (!normaliser || !cfg || cfg.enabled === false) return blocks;
		if (typeof process !== "undefined" && process.env && process.env.SBLAYOUT_OFF) return blocks;
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		const needTags = new Set(cfg.interactive_tags ?? ["speech bubble"]);
		const brk = DataService.Data.InputDocRules?.table_markers?.in_cell_line_break ?? " / ";
		/* ROUND 313 — the single-cell arm, independently reversible. */
		const scCfg = cfg.single_cell;
		const scOn = !!scCfg && scCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.SBSINGLECELL_OFF)
			&& !(scCfg.exclude_code_prefixes ?? []).some((p) => String(run?.moduleCode ?? "").startsWith(p));
		const out = [];
		for (const b of blocks) {
			if (!b || b.kind !== "table" || !Array.isArray(b.rows)) { out.push(b); continue; }
			let hasAct = false, hasBubble = false, hasBoundary = false, hasPlainAct = false;
			for (const m of String(b.text ?? "").matchAll(RED)) {
				let p; try { p = normaliser.Parse(m[1]); } catch { continue; }
				const pr = p && p.primary;
				if (!pr) continue;
				if (pr.tag === "activity" && pr.directive === "CONTAINER_OPEN") {
					hasAct = true;
					/* Is it an EXPLICIT activity opener the writer typed ("[Activity 2A]"),
					 * or a widget request that merely ALIASES to one ("[interactive tool]
					 * quiz — tick box yes or no DEV: answers will vary")?  Only the first
					 * qualifies the single-cell arm — see scOpener below. */
					if (/^\s*\[?\s*activity\b/i.test(String(m[1] ?? ""))) hasPlainAct = true;
				}
				else if (pr.directive === "INTERACTIVE" && needTags.has(pr.tag)) hasBubble = true;
				else if (pr.directive === "PAGE_BOUNDARY" || pr.directive === "SECTION_MARKER") hasBoundary = true;
			}
			/* THE SINGLE-CELL ARM. `scOpener` is the fence the round's own word-loss
			 * check forced: HPFUN903's one-cell table has no explicit opener at all —
			 * what makes it "an activity" is the WIDGET REQUEST "[interactive tool]
			 * quiz — tick box yes or no DEV: answers will vary", which aliases to the
			 * activity tag. Dissolving that hands a widget spec to the body path, and
			 * measured live it (a) dropped the writer's "DEV:" instruction from the
			 * page — a §6 violation — and (b) promoted the first bullet to the box's
			 * <h3> (the gold ships ZERO bullet headings in 2,385 files). Requiring a
			 * bracket the writer opened with the word "activity" separates that case
			 * from ENGI400's "[Activity 2A]" and TEDC402's "Activity] 1D" cleanly and
			 * for a structural reason, not a per-module one. */
			const scOpener = scCfg?.require_explicit_activity_opener === false || hasPlainAct;
			const singleCell = scOn && scOpener
				&& b.rows.length === 1 && (b.rows[0]?.length ?? 0) === 1;
			if (!hasAct || hasBoundary || !(hasBubble || singleCell)) { out.push(b); continue; }
			let made = 0;
			for (let r = 0; r < b.rows.length; r++) {
				for (const cell of (b.rows[r] ?? [])) {
					const text = String(cell ?? "").split(brk).join("\n").trim();
					if (!text) continue;
					out.push({
						kind: "para", text,
						links: (b.rowLinks?.[r] ?? b.links ?? []).slice(),
						wtPage: b.wtPage, list: "", listLevel: 0,
					});
					made++;
				}
			}
			run?.AddNote("info", "DocxExtractor", hasBubble
				? `Page-layout table dissolved into ${made} stacked blocks (an [Activity] and a [speech bubble] shared one table — the finished page stacks them; round 306).`
				: `Single-cell page-layout table dissolved into ${made} stacked blocks (a one-cell table holding an [Activity] is a box the writer drew, not widget data; round 313).`);
		}
		return out;
	};

	/**
	 * REPAIRS A TAG THAT IS MISSING ITS OPENING SQUARE BRACKET.
	 *
	 * WHAT PROBLEM THIS SOLVES:
	 * A writer will sometimes forget to colour the opening "[" of a tag red,
	 * so what should have been a red span reading "[H2] Know:" instead
	 * arrives as "H2] Know:" (missing the "["). TagNormaliser.Parse already
	 * tolerates this for CLASSIFICATION purposes — it can still work out
	 * that "H2] Know:" MEANS the [H2] tag — but roughly ten OTHER places in
	 * the pipeline (RenderText, the overview-menu splitter, the black-tag
	 * stripper, InteractiveScanner…) read the raw bracket characters
	 * directly and don't know that trick. They see a stray "H2]" with no
	 * matching "[" and leak it into the page as literal text (one real
	 * example: a "Know" heading disappeared entirely and the literal text
	 * "<h5>H2]</h5>" showed up in the HTML instead).
	 *
	 * HOW IT WORKS:
	 * For every red ("content") span, look at the text right before its
	 * first "]". If that text is a single word/phrase that resolves to a
	 * KNOWN tag by a clean, WHOLE match — not a tag word that just happens
	 * to appear buried inside an ordinary sentence, see clean_hows below —
	 * insert the missing "[" at the start of that word. Every downstream
	 * reader then sees a normal, complete "[H2]" tag. The original
	 * letter-casing is preserved, because RenderText needs it to show
	 * headings/titles with correct capitalisation.
	 *
	 * WHAT THIS DOES NOT TOUCH:
	 * A tag that is missing its CLOSING bracket instead (e.g. "[hover
	 * trigger: some text" with no "]" at the end) is deliberately left
	 * alone — TagNormaliser.Parse and RenderText already have their own
	 * tolerant handling for that shape, and fully fixing it needs more work
	 * that hasn't been done yet (tracked separately as a "split-bracket
	 * infoTrigger" follow-up).
	 *
	 * DATA DRIVEN: which match types count as "clean enough to repair"
	 * lives in Input_Doc_Rules.json under
	 * red_runs.repair_missing_bracket.clean_hows (e.g. "exact",
	 * "denumbered", "denumbered_head" — NOT "embedded", which means the tag
	 * word was found buried inside ordinary prose rather than leading the
	 * phrase).
	 *
	 * @param {Object[]} blocks - content blocks (block.text carries the red markers)
	 * @param {TagNormaliser|null} normaliser - resolves the token (required)
	 * @param {ConversionRun|null} run - surfacing hook (not used today; kept for future warnings)
	 * @returns {Object[]} the same array, with block.text repaired in place
	 */
	static RepairContentTags(blocks, normaliser, run = null) {
		const cfg = DataService?.Data?.InputDocRules?.red_runs?.repair_missing_bracket;
		if (!normaliser || !cfg || cfg.enabled === false) return blocks;
		if (typeof process !== "undefined" && process.env && process.env.BRACKETFIX_OFF) return blocks;
		const cleanHows = new Set(cfg.clean_hows ?? ["exact", "denumbered", "denumbered_head"]);
		const excludeTags = new Set(cfg.exclude_tags ?? []);
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		for (const b of blocks) {
			if (b.kind !== "para" || !b.text || b.text.indexOf("]") < 0) continue;
			b.text = b.text.replace(RED, (whole, inner) => {
				const fixed = this.#repairLeadingBracket(inner, normaliser, cleanHows, excludeTags);
				return fixed === null ? whole : "\u{1f534}[RED TEXT]" + fixed + "[/RED TEXT]\u{1f534}";
			});
		}
		return blocks;
	};

	/**
	 * Inserts a missing OPENING bracket into one red-span's inner text when the
	 * span opens with a lone "token]" whose token is WHOLLY a known tag. Returns
	 * the repaired inner string, or null when nothing should change (the guard).
	 */
	static #repairLeadingBracket(inner, normaliser, cleanHows, excludeTags) {
		const closeIdx = inner.indexOf("]");
		if (closeIdx < 0) return null;                        // no ] at all
		const openIdx = inner.indexOf("[");
		if (openIdx >= 0 && openIdx < closeIdx) return null;  // a "[" already opens before this "]" → well-formed pair
		const before = inner.slice(0, closeIdx);              // token region incl. leading whitespace
		const token = before.trim();
		if (!token) return null;                              // bare "]"
		let parsed;
		try { parsed = normaliser.Parse("[" + token + "]"); } catch { return null; }
		const prim = parsed && parsed.primary;
		// WHOLE-token match only (clean_hows) — a tag word embedded in prose is how="embedded" and skipped.
		if (!prim || !cleanHows.has(prim.how) || excludeTags.has(prim.tag)) return null;
		const lead = before.length - before.trimStart().length;
		return inner.slice(0, lead) + "[" + inner.slice(lead);
	};

	// =======================================================================
	// XML PARSING (private)
	// =======================================================================

	/**
	 * Reads word/_rels/document.xml.rels into rId → external target URL.
	 *
	 * DATA SHAPE (real sample from OSAH401 Media List.docx):
	 * <Relationship Id="rId8" Type=".../hyperlink"
	 *   Target="https://www.istockphoto.com/photo/fun-dog-…" TargetMode="External"/>
	 *
	 * @param {string} xml
	 * @returns {Map<string,string>}
	 */
	static #parseRels(xml) {
		const rels = new Map();
		// one regex per Relationship element; attribute order can vary, so
		// capture the whole tag then pick attributes out of it
		for (const m of xml.matchAll(/<Relationship\b[^>]*>/g)) {
			const tag = m[0];
			if (!/TargetMode="External"/.test(tag)) continue;
			const id = tag.match(/\bId="([^"]+)"/)?.[1];
			const target = tag.match(/\bTarget="([^"]+)"/)?.[1];
			if (id && target) rels.set(id, this.#decodeXml(target));
		}
		return rels;
	};

	/**
	 * Reads word/numbering.xml just deeply enough to answer one question
	 * per numId: bullet list or numbered list?
	 *
	 * HOW: numId → abstractNumId → the ilvl-0 numFmt ("bullet"/"decimal"/…).
	 *
	 * @param {string} xml
	 * @returns {Map<string,string>} numId → "bullet" | "number"
	 */
	static #parseNumbering(xml) {
		const formats = new Map();
		if (!xml) return formats;

		// abstractNumId → first numFmt val
		const abstractFmt = new Map();
		for (const m of xml.matchAll(/<w:abstractNum w:abstractNumId="(\d+)"[\s\S]*?(?=<w:abstractNum |<\/w:numbering>)/g)) {
			const fmt = m[0].match(/<w:numFmt w:val="(\w+)"/)?.[1];
			abstractFmt.set(m[1], fmt === "bullet" ? "bullet" : "number");
		}
		// numId → abstractNumId
		for (const m of xml.matchAll(/<w:num w:numId="(\d+)"[^>]*>\s*<w:abstractNumId w:val="(\d+)"/g)) {
			formats.set(m[1], abstractFmt.get(m[2]) ?? "bullet");
		}
		return formats;
	};

	/**
	 * Parses word/comments.xml into id → { author, text }.
	 *
	 * Word stores each comment as <w:comment w:id="N" w:author="…" w:date="…"
	 * w:initials="…"> … <w:p><w:r><w:t>text</w:t></w:r></w:p> … </w:comment>.
	 * Comments never nest, so the close tag is unambiguous. We keep the author
	 * (the Office display name — the same name later checked against the
	 * author whitelist) and the joined run text; the
	 * anchor (WHICH content the comment is attached to) comes from the
	 * commentRangeStart markers in document.xml, matched by id in #parseDocument.
	 *
	 * @param {string} xml - word/comments.xml content ("" when the part is absent)
	 * @returns {Map<string,{author:string,text:string}>}
	 */
	static #parseComments(xml) {
		const map = new Map();
		if (!xml) return map;
		const re = /<w:comment\b([^>]*)>([\s\S]*?)<\/w:comment>/g;
		for (const m of xml.matchAll(re)) {
			const id = m[1].match(/\bw:id="([^"]*)"/)?.[1];
			if (id === undefined) continue;
			const author = this.#decodeXml(m[1].match(/\bw:author="([^"]*)"/)?.[1] ?? "");
			const text = [...m[2].matchAll(/<w:t\b[^>]*>([\s\S]*?)<\/w:t>/g)]
				.map((t) => this.#decodeXml(t[1])).join("");
			map.set(id, { author, text: text.replace(/\s+/g, " ").trim() });
		}
		return map;
	};

	/**
	 * The main walk: document.xml → ordered blocks.
	 *
	 * HOW IT WORKS:
	 * Word nests tables inside w:tbl and paragraphs inside w:p. We split the
	 * body into top-level chunks by scanning for w:p / w:tbl at depth 0 of
	 * the body, then parse each chunk. (Nested tables inside cells are rare
	 * in writers templates; a nested table's text simply joins its cell.)
	 *
	 * @param {string} xml - word/document.xml content
	 * @param {Map} rels - rId → URL
	 * @param {Map} numFormats - numId → bullet|number
	 * @param {Object} rules - Input_Doc_Rules.json
	 * @returns {Object[]} blocks
	 */
	static #parseDocument(xml, rels, numFormats, rules, comments = new Map()) {
		const blocks = [];
		// COMMENT ANCHORING: a <w:commentRangeStart> marker inside a chunk of
		// XML tells us which block a Word comment belongs to; we surface that
		// note JUST BEFORE the block it's anchored to. A comment anchored
		// inside an EMPTY paragraph (e.g. a comment left on an embedded image
		// with no text of its own) would otherwise be silently lost once that
		// empty block gets dropped, so instead we CARRY such comments forward
		// and attach them to the next block that actually survives — the
		// nearest real element after the anchor point.
		let pendingComments = [];
		const findComments = (chunkXml, isTable = false) => {
			const found = [];
			if (!comments.size) return found;
			const seen = new Set();
			for (const cm of chunkXml.matchAll(/<w:commentRangeStart\b[^>]*\bw:id="([^"]*)"/g)) {
				const id = cm[1];
				if (seen.has(id)) continue;
				seen.add(id);
				const c = comments.get(id);
				if (!c) continue;
				// When a comment is anchored inside a TABLE row (this happens
				// on the Media List document), also capture that row's
				// hyperlink URL. Later on, this lets us match the comment to
				// whichever BODY element links the same piece of media, so the
				// note appears next to the media itself instead of being
				// stuck inside the raw media-list table.
				let rowUrl = null;
				if (isTable) {
					const s = chunkXml.lastIndexOf("<w:tr", cm.index);
					const e = s >= 0 ? chunkXml.indexOf("</w:tr>", cm.index) : -1;
					if (s >= 0 && e > s) {
						const rid = chunkXml.slice(s, e).match(/r:id="([^"]+)"/)?.[1];
						if (rid && rels && rels.get(rid)) rowUrl = rels.get(rid);
					}
				}
				found.push(rowUrl ? { ...c, rowUrl } : { ...c });
			}
			return found;
		};
		// page counter (Writers Template pagination) — bumped by Word's own
		// w:lastRenderedPageBreak records + explicit page breaks; feeds the
		// media list's WTPg No. → lesson mapping for acks grouping
		const page = { current: rules.wt_page_tracking.first_page_number };

		// body = everything inside <w:body> … </w:body>
		const body = xml.slice(xml.indexOf("<w:body>") + 8, xml.lastIndexOf("</w:body>"));

		// walk top-level elements: tables first (they contain paragraphs,
		// so we must not double-read their inner w:p as body paragraphs)
		let pos = 0;
		while (pos < body.length) {
			const nextP = body.indexOf("<w:p ", pos);
			const nextP2 = body.indexOf("<w:p>", pos);
			const nextTbl = body.indexOf("<w:tbl>", pos);
			// earliest of the three markers (-1 = not found → Infinity)
			const candidates = [
				[nextP < 0 ? Infinity : nextP, "p"],
				[nextP2 < 0 ? Infinity : nextP2, "p"],
				[nextTbl < 0 ? Infinity : nextTbl, "tbl"],
			].sort((a, b) => a[0] - b[0]);
			const [at, kind] = candidates[0];
			if (at === Infinity) break;

			// ROUND 265 (CHFUN01): a SELF-CLOSED empty paragraph
			// (<w:p w14:paraId=".."/> — Word's shorthand for an empty
			// paragraph) has no </w:p> at all. It carries no content, so as a
			// top-level block it is simply skipped; letting it fall through to
			// #findClose would mis-count it as an OPEN with no CLOSE (see the
			// matching fix there). Data: paragraph.self_closed_skip.
			// Env toggle: SELFCLOSEP_OFF.
			if (kind === "p" && this.#selfClosedSkipOn(rules)) {
				const gt = body.indexOf(">", at);
				if (gt > 0 && body[gt - 1] === "/") { pos = gt + 1; continue; }
			}

			if (kind === "tbl") {
				const end = this.#findClose(body, at, "w:tbl");
				const tableXml = body.slice(at, end);
				const tblBlock = this.#parseTable(tableXml, rels, page, rules);
				const found = findComments(tableXml, true);
				const all = pendingComments.length ? [...pendingComments, ...found] : found;
				pendingComments = [];
				if (all.length) tblBlock.comments = all;
				blocks.push(tblBlock);
				pos = end;
			} else {
				const end = this.#findClose(body, at, "w:p");
				const paraXml = body.slice(at, end);
				const block = this.#parseParagraph(paraXml, rels, numFormats, page, rules);
				const found = findComments(paraXml);
				// keep empty paragraphs out — they carry no content and the
				// corpus form separates blocks with blank lines anyway
				if (block.text.trim()) {
					const all = pendingComments.length ? [...pendingComments, ...found] : found;
					pendingComments = [];
					if (all.length) block.comments = all;
					blocks.push(block);
				} else if (found.length) {
					// anchor sits in an empty (e.g. image-only) paragraph that is dropped —
					// carry its comments to the next kept block (nearest real element after).
					pendingComments.push(...found);
				}
				pos = end;
			}
		}
		// any comments whose anchor trailed the last real content attach to the last block
		if (pendingComments.length && blocks.length) {
			const last = blocks[blocks.length - 1];
			last.comments = last.comments ? [...last.comments, ...pendingComments] : pendingComments;
		}
		return blocks;
	};

	/**
	 * Finds the index just past the matching close tag, handling nesting
	 * (tables nest tables; paragraphs never nest paragraphs but the same
	 * scanner serves both).
	 *
	 * @param {string} xml - the text being scanned
	 * @param {number} start - index of the opening tag
	 * @param {string} tag - element name, e.g. "w:tbl"
	 * @returns {number} index just after the close tag
	 */
	static #findClose(xml, start, tag) {
		const open = `<${tag}`;
		const close = `</${tag}>`;
		const scSkip = this.#selfClosedSkipOn();
		let depth = 0;
		let i = start;
		while (i < xml.length) {
			const nextOpen = xml.indexOf(open, i);
			const nextClose = xml.indexOf(close, i);
			if (nextClose < 0) return xml.length;
			// an opening tag like <w:tblPr would false-match <w:tbl —
			// require the next char to close the name (space or >)
			if (nextOpen >= 0 && nextOpen < nextClose
				&& (xml[nextOpen + open.length] === ">" || xml[nextOpen + open.length] === " ")) {
				// ROUND 265 (CHFUN01): a SELF-CLOSED element (<w:p .../> —
				// Word's empty-paragraph shorthand, common in table cells)
				// has NO matching close tag. Counting it as an open ratchets
				// the depth up one for ever, so a textbox-carrying paragraph
				// whose scan passes one NEVER finds its close and swallows
				// the rest of the document into ONE giant block (CHFUN01
				// lost every paragraph boundary in the module this way; the
				// TRR203 "mega-paragraph" was the same bug). A self-closed
				// open contributes NOTHING to depth — skip past it.
				// Data: Input_Doc_Rules.paragraph.self_closed_skip.
				// Env toggle: SELFCLOSEP_OFF (reverts to the ratchet).
				if (scSkip) {
					const gt = xml.indexOf(">", nextOpen);
					if (gt > 0 && xml[gt - 1] === "/") { i = gt + 1; continue; }
				}
				depth++;
				i = nextOpen + open.length;
			} else {
				depth--;
				i = nextClose + close.length;
				if (depth === 0) return i;
			}
		}
		return xml.length;
	};

	/**
	 * ROUND 265: is the self-closed-paragraph skip active? (data flag AND
	 * not reverted by the SELFCLOSEP_OFF env toggle).
	 *
	 * @param {Object} [rules] - Input_Doc_Rules.json (defaults to DataService)
	 * @returns {boolean}
	 */
	static #selfClosedSkipOn(rules = null) {
		if (typeof process !== "undefined" && process.env && process.env.SELFCLOSEP_OFF) return false;
		const r = rules ?? ((typeof DataService !== "undefined") ? DataService.Data?.InputDocRules : null);
		return (r?.paragraph?.self_closed_skip?.enabled ?? true) !== false;
	};

	/**
	 * Parses ONE paragraph into a paraBlock (the heart of the extractor).
	 *
	 * RUN HANDLING:
	 * - red runs (w:color in red_hex_values) merge into ONE red span,
	 *   wrapped in the corpus markers
	 * - black bold/italic runs get the markdown markers (corpus convention)
	 * - hyperlinked runs resolve their rId target into block.links
	 * - w:lastRenderedPageBreak / w:br type="page" bump the WT page counter
	 *
	 * @returns {Object} paraBlock
	 */
	static #parseParagraph(xml, rels, numFormats, page, rules) {
		// page bump BEFORE assigning: Word records the break at the start
		// of the first paragraph of the new page.
		// CAUTION (verified on OSAH401): Google-Docs exports write
		// <w:pageBreakBefore w:val="0"/> on nearly EVERY paragraph, meaning
		// "no break" — only a bare element or val="1"/"true" is a real break.
		const breaks = (xml.match(/<w:lastRenderedPageBreak\s*\/>/g) ?? []).length
			+ (xml.match(/<w:br w:type="page"\s*\/>/g) ?? []).length
			+ (xml.match(/<w:pageBreakBefore(?: w:val="(?:1|true)")?\s*\/>/g) ?? []).length;
		if (breaks > 0) page.current += breaks;

		// list detection from the paragraph properties
		let list = null;
		const numId = xml.match(/<w:numId w:val="(\d+)"/)?.[1];
		if (numId) list = numFormats.get(numId) ?? "bullet";
		// NESTING LEVEL: <w:ilvl> is Word's own list-indentation level (0 =
		// top level, 1 = indented one level, and so on). We capture it here
		// and encode it as leading 2-space indentation on the bullet/number
		// prefix text, so the list-rendering code further downstream
		// (#renderBlackText) can rebuild proper NESTED <ul>/<ol> HTML — for
		// example, a bold top-level bullet at ilvl 0 with indented sub-points
		// underneath it at ilvl 1. Stays 0 for an ordinary, non-nested list,
		// or for a paragraph that isn't a list item at all.
		const listLevel = parseInt(xml.match(/<w:ilvl w:val="(\d+)"/)?.[1] ?? "0", 10);

		const links = [];
		// pieces: [{ text, red, bold, italic }] in order — grouped later
		const pieces = [];
		// ROUND 341: the near-red BRACKET DEPTH left open by earlier near-red runs of this
		// paragraph — a bracket-less near-red run INSIDE an open tag (Word split the tag
		// across runs) stays red, exactly as a standard-red run would; a black run with
		// real text ends the context. Measured 51 such split sites (HIS1002 32).
		let nearOpen = 0;

		// hyperlink spans first: record target + remember their range so
		// runs inside know their link. We process by replacing hyperlink
		// wrappers with their inner runs, tagging them.
		// Simplest robust approach: walk all runs in order; track whether
		// the run sits inside a w:hyperlink by pre-splitting the XML.
		// ROUND 346 (Chris's D10-7): a Word EQUATION lives in an <m:oMath> BESIDE the runs, so the
		// run walk below never saw it. Each one is converted to MathML now (OmmlMathml) and
		// replaced in place by a synthetic black run carrying its registry sentinel, so the
		// equation keeps its exact position inside the paragraph's text. Data Input_Doc_Rules.math;
		// env MATHML_OFF (the equation vanishes again, as before this round).
		const _mathCfg = rules.math;
		if (_mathCfg && _mathCfg.enabled !== false && xml.indexOf("<m:oMath") >= 0
			&& !(typeof process !== "undefined" && process.env && process.env[_mathCfg.env ?? "MATHML_OFF"])) {
			const conv = new OmmlMathml();
			xml = xml.replace(/<m:oMath\b[^>]*>[\s\S]*?<\/m:oMath>/g, (frag) => {
				const tree = OmmlMathml.Tree(frag);
				const el = tree.childNodes.find((k) => k.nodeType === 1 && k.localName === "oMath");
				const html = el ? conv.convert(el) : "";
				if (!html) return "";
				return "<w:r><w:t xml:space=\"preserve\">" + DocxExtractor.MathSentinel(DocxExtractor.MathRegister(html)) + "</w:t></w:r>";
			});
		}
		const segments = xml.split(/(<w:hyperlink [^>]*>|<\/w:hyperlink>)/);
		let currentLink = null;
		for (const seg of segments) {
			const openLink = seg.match(/^<w:hyperlink ([^>]*)>$/);
			if (openLink) {
				const rId = openLink[1].match(/r:id="([^"]+)"/)?.[1];
				currentLink = rId ? (rels.get(rId) ?? null) : null;
				continue;
			}
			if (seg === "</w:hyperlink>") { currentLink = null; continue; }

			// runs inside this segment
			for (const rm of seg.matchAll(/<w:r\b[\s\S]*?<\/w:r>/g)) {
				const run = rm[0];
				// run text: all w:t contents + tabs as spaces — PLUS soft line breaks.
				// THE DROPPED SOFT LINE BREAK (ROUND 227 — the r225 recorded lever, measured
				// 5,999 <w:br> across 357 of 429 WTs). When a writer presses Shift+Enter, Word
				// stores a <w:br/> INSIDE the paragraph; the old w:t-only extraction silently
				// deleted it, GLUING the text on either side with no separator at all
				// ("…ana”Through perseverance…" — corrupted text, corpus-wide; the round-225
				// whakataukī fix patched the symptom inside proverb boxes only). A <w:br/>
				// WITHOUT type="page|column" now contributes "\n" at its own position — the
				// truthful representation of what the writer authored (a line break); the
				// downstream machinery already handles multi-line text (renderBlackText emits
				// one <p>/<li> per line — the majority gold form for soft-broken paragraphs,
				// measured outputs/_measure_softbreak.py; Utils.Fold collapses \s+ so tag
				// CLASSIFICATION is unchanged). The page-break counter above keeps reading
				// type="page" breaks exactly as before.
				// Data: Input_Doc_Rules.paragraph.soft_break_newline   Env toggle: SOFTBR_OFF
				const softBr = rules.paragraph?.soft_break_newline !== false
					&& !(typeof process !== "undefined" && process.env && process.env.SOFTBR_OFF);
				let text = "";
				for (const t of run.matchAll(/<w:t(?: [^>]*)?>([\s\S]*?)<\/w:t>|<w:br(?:\s+[^>]*)?\/>/g)) {
					if (t[0].startsWith("<w:br")) {
						if (softBr && !/w:type="(?:page|column)"/.test(t[0])) text += "\n";
					} else text += this.#decodeXml(t[1]);
				}
				if (/<w:tab\/>/.test(run)) text = ` ${text}`;
				// INVISIBLE-WHITESPACE NORMALISE (ROUND 241 — Dev-Feedback R4, E1: the
				// SCCH302 "AI marker" NBSP; the same extractor seam as the r227 soft-break
				// fix, and table cells arrive through this same paragraph walk). A writer's
				// Word file carries invisible characters that were never intended as page
				// content: the NON-BREAKING SPACE U+00A0 (autocorrect/paste residue —
				// measured 15,198 across 416 of 429 WTs; 2,108 survived into the shipped
				// corpus while the gold library ships effectively none) becomes a plain
				// space, and the ZERO-WIDTH characters U+200B/U+200C/U+200D/U+FEFF
				// (124 occurrences / 22 WTs) are deleted. GRANULARITY SAFETY (the r227
				// red-run trap): an NBSP-only run stays a non-empty whitespace piece
				// (trim()/Fold treat U+00A0 as whitespace before AND after), so red-span
				// merging is untouched; a run the zero-width strip empties drops out like
				// an always-empty run — the tags gate (9557/9557 spans) is the authoritative
				// granularity detector, proven unchanged in the round's probes. Tag
				// classification is inert by construction (Utils.Fold collapses \s+, which
				// already matches U+00A0). Data: Input_Doc_Rules.text_normalise.
				// Env toggle: NBSP_OFF (reverts the whole normalisation).
				const tn = rules.text_normalise;
				if (tn && tn.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.NBSP_OFF)) {
					if (tn.nbsp_to_space !== false) text = text.replace(/\u00A0/g, " ");
					if (tn.strip_zero_width !== false) text = text.replace(/[\u200B\u200C\u200D\uFEFF]/g, "");
				}
				if (!text) continue;

				const color = run.match(/<w:color w:val="([0-9A-Fa-f]{6})"/)?.[1]?.toLowerCase();
				// THE NEAR-RED TAG RUN (ROUND 341 — the autonomous loop, session 9). Only a
				// run whose colour is on red_hex_values was ever scanned for tags, so a
				// writer whose red is ed0000 (the HIS NCEA1 writer), fa0000 (ENGFUN02) or
				// Word's standard "Dark Red" c00000 (OS* / CED / ARFUN / TEFUN) shipped
				// "[H3] Using browser controls…" as a literal paragraph — 598 tag brackets
				// on 30 modules, the bulk of the literal-tag-leak gate. A run in the hue
				// band (r >= min_r, g <= max_g, b <= max_b) counts as red ONLY when it
				// carries a bracket (require_bracket): c00000 is ALSO used for content
				// ("+ 5 = 9", "tone", "pace"), and a blanket rule would strip it as an
				// instruction. Strictly additive — a run that is red today is unchanged
				// and a bracket-less run is unchanged. The exact list stays primary.
				// Data: Input_Doc_Rules.red_runs.near_red_tag_runs   Env toggle: NEARRED_OFF
				const nr = rules.red_runs.near_red_tag_runs;
				const nearRedOn = nr && nr.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.NEARRED_OFF);
				const listRed = rules.red_runs.red_hex_values.includes(color);
				const nearRed = !listRed && nearRedOn && !!color && this.#nearRed(color, nr)
					&& (!nr.require_bracket || nearOpen > 0 || /[\[\]]/.test(text));
				// THE HYPERLINKED MEDIA TAG (ROUND 342 — the autonomous loop, session 9). The BLL
				// phonics writers type "[audio 1]" AS A HYPERLINK to the sound file (the run is the
				// hyperlink blue or black), so it never counted as red and shipped as literal text.
				// A run inside a w:hyperlink whose bracket OPENS with a data-listed media head word
				// counts as red. Fenced to the head list because the same writers hyperlink every
				// WORD of a phonics word list ("[scissors]" -> its sound) — content, never a tag.
				// Data: Input_Doc_Rules.red_runs.hyperlinked_tag_runs   Env toggle: HYPERTAG_OFF
				const ht = rules.red_runs.hyperlinked_tag_runs;
				const hyperTagOn = ht && ht.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.HYPERTAG_OFF);
				// Session 11: the link TARGET must be a media-file carrier (data link_target_match —
				// the drive / sharepoint / istock / youtube hosts or a media file extension); a
				// curriculum resource PAGE (BLL262's tahurangi School-Journal link) is a reference
				// to the resource, never the media file, and stays the black link line.
				const hyperTarget = !currentLink || !ht?.link_target_match
					|| new RegExp(ht.link_target_match, "i").test(String(currentLink));
				const hyperRed = !listRed && !nearRed && hyperTagOn && !!currentLink && hyperTarget
					&& (nearOpen > 0 || this.#hyperlinkedTagHead(text, ht.head_words || [], ht.exclude_words || []));
				const red = listRed || nearRed || hyperRed;
				if (nearRed || hyperRed) nearOpen = Math.max(0, nearOpen + (text.match(/\[/g) || []).length - (text.match(/\]/g) || []).length);
				else if (!listRed && text.trim()) nearOpen = 0;
				// <w:b/> means bold on; <w:b w:val="0"/> means explicitly off
				const bold = /<w:b\/>|<w:b w:val="(?:1|true)"\/>/.test(run);
				const italic = /<w:i\/>|<w:i w:val="(?:1|true)"\/>/.test(run);

				// ANSWER MARKS (ROUND 309 — reasons 4+5 of the dropDown catalogue). A writer
				// marks a quiz's correct answer with a yellow HIGHLIGHTER (<w:highlight>,
				// never read before this round) or with GREEN text (00b050 — the writer's
				// answer green; the template's guidance green 316757 stays ignored). The
				// mark is recorded on a SIDE-CHANNEL (block.marks below) and NEVER touches
				// the serialised text, so red-span granularity and every downstream byte
				// are identical by construction — the tags gate (9557/9557) is the canary.
				// A consumer must bring its own fence (round 309's dropDown reading needs
				// the writer's own "Correct answers highlighted / in green" announcement).
				// Data: Input_Doc_Rules.answer_marks   Env toggle: ANSMARK_OFF
				const am = rules.answer_marks;
				const amOn = am && am.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.ANSMARK_OFF);
				let mark = null;
				if (amOn) {
					const hl = run.match(/<w:highlight w:val="([^"]+)"/)?.[1];
					if (hl && !(am.exclude_highlight_values ?? ["none", "white"]).includes(hl)) mark = "hl";
					else if ((am.green_hex_values ?? ["00b050"]).includes(color)) mark = "green";
				}

				if (currentLink) links.push({ text, target: currentLink });
				pieces.push({ text, red, bold, italic, mark, hyper: hyperRed });
			}
		}

		// ---- serialise the pieces into the corpus marker-text form ------
		let out = "";
		let i = 0;
		while (i < pieces.length) {
			if (pieces[i].red) {
				// Merge a run of consecutive red runs into ONE marker span.
				//
				// We also BRIDGE a stray NON-RED whitespace run that sits in
				// the MIDDLE of a tag, between two red runs. Word sometimes
				// splits what the writer typed as a single, uniformly-red
				// "[tag]" into several separate XML runs, and in the process
				// can lose the red colour on just the interior space
				// character — which fragments one tag into two separate
				// marker spans. A real example of the broken shape this
				// produces: a tag like
				// "[Please embed this journal story (as in ANZHFUN01 phase 2]"
				// arriving as two pieces — "...phase 2" coloured red, then a
				// single space that lost its colour, then "]" coloured red
				// again.
				// The bridge only fires when ALL of these are true:
				//   - the red text collected SO FAR is mid-tag (it has an
				//     unmatched "[" that hasn't been closed by a "]" yet)
				//   - the non-red gap run is pure whitespace (nothing else)
				//   - the very NEXT run after the gap is red again
				// That combination means it's safe to re-glue the two red
				// pieces back into one tag — it can never accidentally pull
				// in real black body text, and it can never merge two
				// separate, complete tags into one.
				// (The ordinary case — Word splitting same-colour text into
				// multiple runs, e.g. "[Tab 1: I" + "ntroduction" + "]" —
				// is already handled by the consecutive-red merge loop
				// below; this bridge only covers the case where the colour
				// itself gets dropped on one small gap.)
				// Data flag: Input_Doc_Rules.json red_runs.bridge_split_tag
				// Env toggle: REDBRIDGE_OFF (disables the bridge, so the tag
				// stays fragmented into two marker spans)
				const bridgeOn = rules.red_runs.bridge_split_tag
					&& !(typeof process !== "undefined" && process.env && process.env.REDBRIDGE_OFF);
				let redText = "";
				while (i < pieces.length) {
					if (pieces[i].red) { redText += pieces[i].text; i++; continue; }
					// SOFT-BREAK-ONLY GAP (ROUND 227, part of the w:br→\n fix). A soft line
					// break often lives in a COLOURLESS run of its own between two red runs
					// ("[Overview]" ⏎ "[H3] Knowledge" — one paragraph, the tags on separate
					// lines). Before the fix that run carried NO text at all, so it was
					// INVISIBLE here and the two red runs merged into ONE marker span; the
					// "\n" it now contributes must therefore also merge INTO the span —
					// otherwise it would SPLIT the span in two and change tag GRANULARITY
					// corpus-wide (caught live on SSOG103: the standalone "[Overview]" alias
					// flipped the whole lesson-menu partition). Utils.Fold collapses the \n,
					// so the merged span parses byte-identically to the pre-fix glued form
					// (proven: primary/tags/RenderText identical). ONLY a pure-newline piece
					// bridges this way — a piece with any other character (even a plain
					// space) was already a visible separator before the fix and keeps its
					// existing two-span behaviour.
					if (pieces[i].text && /^\n+$/.test(pieces[i].text)
						&& i + 1 < pieces.length && pieces[i + 1].red) {
						redText += pieces[i].text; i++; continue;
					}
					const opens = (redText.match(/\[/g) || []).length;
					const closes = (redText.match(/\]/g) || []).length;
					if (bridgeOn && opens > closes && pieces[i].text.trim() === ""
						&& i + 1 < pieces.length && pieces[i + 1].red) {
						redText += pieces[i].text; i++; continue;   // bridge the whitespace gap mid-tag
					}
					break;
				}
				// A WHITESPACE-ONLY red span: sometimes a writer accidentally
				// colours just a single space or tab character red, with no
				// real text in it. If we wrapped that lone space in a
				// [RED TEXT] marker like any other red span, PageSplitter
				// would treat it as a standalone tag-like item and FRAGMENT
				// the paragraph in two at that point — e.g. "**Banter is**
				// like other things..." would get chopped into two separate
				// <p> elements right at the accidentally-red space. Instead,
				// when the collected red text is NOTHING BUT whitespace, we
				// just emit a single plain space character (no marker at
				// all) so the paragraph stays in one piece. This only ever
				// fires when the red run is PURE whitespace — any real
				// [tag] or written instruction (anything with actual
				// non-whitespace content) always keeps its marker and is
				// never dropped.
				// Data flag: Input_Doc_Rules.json red_runs.collapse_whitespace_only
				// Env toggle: REDWS_OFF (reverts to wrapping the whitespace
				// in a marker and letting the paragraph fragment)
				const collapseRedWs = rules.red_runs.collapse_whitespace_only
					&& !(typeof process !== "undefined" && process.env && process.env.REDWS_OFF);
				if (collapseRedWs && redText.trim() === "") out += " ";
				else out += `${rules.red_runs.marker_open}${redText}${rules.red_runs.marker_close}`;
			} else {
				// merge consecutive black runs sharing the same bold/italic
				const { bold, italic } = pieces[i];
				let blackText = "";
				while (i < pieces.length && !pieces[i].red
					&& pieces[i].bold === bold && pieces[i].italic === italic) {
					blackText += pieces[i].text; i++;
				}
				// markdown markers only when the text has substance —
				// never wrap pure whitespace (it renders as stray asterisks)
				if (blackText.trim()) {
					// PRESERVING THE SPACE BEFORE A BOLD/ITALIC WORD: trim()
					// removes whitespace from BOTH ends, but Word often stores
					// the space BETWEEN two words as the LEADING character of
					// the next styled run rather than as the TRAILING
					// character of the previous run. For example, the plain
					// run might contain "...their" (no trailing space) while
					// the very next bold run contains " wellbeing or hauora"
					// (WITH a leading space). If we simply trim() that bold
					// run's text, we lose the leading space and the two words
					// get glued together with no gap: "their<b>wellbeing...".
					// So we restore the leading space SYMMETRICALLY with the
					// trailing space — but ONLY when the original run actually
					// started with a space, so a case where the words were
					// genuinely meant to run together (no leading space in the
					// source) is left exactly as it was.
					// Data flag: Input_Doc_Rules.json formatting_markers.preserve_leading_space
					// Env toggle: BOLDSPACE_OFF (reverts to only restoring the
					// trailing space, not the leading one)
					const keepLead = rules.formatting_markers.preserve_leading_space
						&& !(typeof process !== "undefined" && process.env && process.env.BOLDSPACE_OFF);
					const lead = (keepLead && blackText.startsWith(" ")) ? " " : "";
					const tail = blackText.endsWith(" ") ? " " : "";
					if (bold) blackText = `${lead}${rules.formatting_markers.bold}${blackText.trim()}${rules.formatting_markers.bold}${tail}`;
					else if (italic) blackText = `${lead}${rules.formatting_markers.italic}${blackText.trim()}${rules.formatting_markers.italic}${tail}`;
				}
				out += blackText;
			}
		}

		// bullet / number prefix so the downstream list builder sees the corpus form.
		// LEADING INDENT encodes the nesting level (2 spaces per ilvl) — #renderBlackText
		// reads it to build nested <ul>/<ol>; a flat (ilvl 0) list is unchanged.
		const indent = "  ".repeat(Math.max(0, listLevel));
		if (list === "bullet" && out.trim()) out = `${indent}${rules.formatting_markers.bullet_prefix}${out}`;
		if (list === "number" && out.trim() && !/^\s*\d+[.)]/.test(out)) out = `${indent}1. ${out}`;

		// ANSWER-MARK side-channel (ROUND 309): merge consecutive same-kind marked
		// pieces (Word fragments one highlighted phrase into several runs; a pure
		// whitespace gap between two same-kind marked pieces bridges — the red-merge
		// convention). block.text is untouched — the marks travel beside it.
		const marks = [];
		{
			let cur = null;
			const flush = () => { if (cur && cur.text.trim()) marks.push({ text: cur.text.trim(), kind: cur.kind }); cur = null; };
			for (const p of pieces) {
				if (p.mark) {
					if (cur && cur.kind === p.mark) { cur.text += p.text; continue; }
					flush(); cur = { text: p.text, kind: p.mark };
				} else if (cur && /^\s*$/.test(p.text)) cur.text += p.text;
				else flush();
			}
			flush();
		}

		const blk = { kind: "para", text: out, links, wtPage: page.current, list, listLevel };
		if (marks.length) blk.marks = marks;
		// ROUND 342 (session 11) — a paragraph whose tag span came from a HYPERLINKED run is
		// marked on a side-channel (never in the text, so red-span granularity and every
		// downstream byte are identical by construction): MediaBuilder.media reads it to
		// render the words the writer typed inside the same hyperlink as the tag.
		if (pieces.some((p) => p.hyper)) blk.hyperTag = true;
		return blk;
	};

	/**
	 * Parses ONE table into a tableBlock, serialising each cell with the
	 * same paragraph logic (so red tags INSIDE tables keep their markers —
	 * interactives' data tables depend on this).
	 *
	 * @returns {Object} tableBlock
	 */
	static #parseTable(xml, rels, page, rules) {
		const links = [];
		const rows = [];
		const rowLinks = [];   // hyperlinks per ROW — the media list parser
		                       // must never guess which row a URL belongs to
		// table page = page at the point the table starts; cell-level breaks
		// also bump the global counter as they're encountered
		const tablePage = page.current;

		let anyCellMark = false;
		const cellMarks = [];   // rows-aligned: cellMarks[r][c] = [{text,kind}] (ROUND 309)
		for (const rowMatch of xml.matchAll(/<w:tr\b[\s\S]*?<\/w:tr>/g)) {
			const cells = [];
			const thisRowLinks = [];
			const thisRowMarks = [];
			for (const cellMatch of rowMatch[0].matchAll(/<w:tc\b[\s\S]*?<\/w:tc>/g)) {
				// every paragraph in the cell, joined with the in-cell
				// line-break marker (phase-4 convention: " / ")
				const paras = [];
				const cm = [];
				for (const pm of cellMatch[0].matchAll(/<w:p[ >][\s\S]*?<\/w:p>/g)) {
					const block = this.#parseParagraph(pm[0], rels, new Map(), page, rules);
					if (block.text.trim()) paras.push(block.text.trim());
					links.push(...block.links);
					thisRowLinks.push(...block.links);
					if (block.marks) cm.push(...block.marks);   // the r309 answer-mark side-channel
				}
				cells.push(paras.join(rules.table_markers.in_cell_line_break));
				thisRowMarks.push(cm);
				if (cm.length) anyCellMark = true;
			}
			rows.push(cells);
			rowLinks.push(thisRowLinks);
			cellMarks.push(thisRowMarks);
		}

		// the corpus text form — what the tag pipeline scans
		const tm = rules.table_markers;
		const text = [
			tm.open,
			...rows.map((cells) => `${tm.row_prefix}${cells.join(tm.column_separator)}`),
			tm.close,
		].join("\n");

		const blk = { kind: "table", rows, rowLinks, links, wtPage: tablePage, text };
		if (anyCellMark) blk.cellMarks = cellMarks;   // ROUND 309 answer-mark side-channel
		return blk;
	};

	/**
	 * Decodes the five XML entities Word writes into text content.
	 * @param {string} s
	 * @returns {string}
	 */
	/**
	 * ROUND 341 — is a w:color hex a NEAR-RED (a shade the writer used AS red but
	 * red_hex_values does not name)? Pure arithmetic on the six hex digits against
	 * the data band; a non-hex value is never near-red.
	 */
	/**
	 * ROUND 342 — does a run's text open a bracket whose FIRST WORD is one of the data-listed
	 * media heads ("[audio 1]", "[Audio button]", "[Video link]")? Case-folded; a multi-word
	 * head ("audio button") is matched as a prefix of the bracket's words. A bracket whose
	 * remaining words carry an EXCLUDED word ("[Audio Animation 1: …]" — a CS-animation
	 * brief, not a sound file; session 11) is never a media tag.
	 */
	static #hyperlinkedTagHead(text, heads, excludes = []) {
		const m = String(text).match(/\[\s*([^\]]{1,60})/);
		if (!m) return false;
		const inner = m[1].toLowerCase().replace(/[^a-z ]+/g, " ").replace(/\s+/g, " ").trim();
		if (!inner) return false;
		if (excludes.length && inner.split(" ").some((w) => excludes.includes(w))) return false;
		return heads.some((h) => inner === h || inner.startsWith(h + " "));
	}

	static #nearRed(hex, nr) {
		if (!/^[0-9a-f]{6}$/.test(hex)) return false;
		const r = parseInt(hex.slice(0, 2), 16), g = parseInt(hex.slice(2, 4), 16), b = parseInt(hex.slice(4, 6), 16);
		return r >= (nr.min_r ?? 176) && g <= (nr.max_g ?? 64) && b <= (nr.max_b ?? 64);
	}

	static #decodeXml(s) {
		return s
			.replace(/&lt;/g, "<").replace(/&gt;/g, ">")
			.replace(/&quot;/g, '"').replace(/&apos;/g, "'")
			.replace(/&amp;/g, "&");
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { DocxExtractor, OmmlMathml };
