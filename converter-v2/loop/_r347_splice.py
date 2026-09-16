#!/usr/bin/env python3
"""_r347_splice.py — ROUND 347 (Chris's D10-5: the KB 05D table form). Idempotent; run under WSL from anywhere.
Data: Emit_Templates.json elements.table gains kb_class_form {enabled, env TBLBORDER_OFF, default_class "table table-bordered",
      comparison {enabled false, class "table tableFixed", lexicon}} — surgical text insertion (tab-indented file, never json.dumps).
Engine: TablesAndGrids.contentTable swaps the <table class="table"> opener for the KB class form when the flag is on.
Carried fix (r346's own defect, found by the r347 OFF probe): Unicode math-italic letters (U+1D400–U+1D7FF, e.g. U+1D465) were
walked by UTF-16 unit in the OMML port, so each shipped as two <mi>U+FFFD</mi> (MXDB301_3_0, MXFU401_2_0: 34 of them); the gold
ships <mi>x</mi>. Fold the block to its plain letter and walk letters by code point; the math verifier counts a U+FFFD / lone
surrogate inside <math> as malformed. Every JS text below is a RAW string: what you read is what lands in the file."""
import io, os
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2"
TESTS = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    data = s.encode("utf-8")                      # encode BEFORE opening: a bad string can never truncate the file
    with io.open(p, "wb") as f: f.write(data)
def splice(p, anchor, new, marker, label):
    s = rd(p)
    if marker in s: print(f"{label}: already present"); return
    assert s.count(anchor) == 1, f"{label}: anchor count {s.count(anchor)}"
    wr(p, s.replace(anchor, new)); print(f"{label}: spliced")

# ---- data ---------------------------------------------------------------------------------------------------------
T = "\t"
cell = T*3 + '"cell": "<td>{content}</td>",\n'
lex = ('[["can", "cannot"], ["can", "can\'t"], ["pros", "cons"], ["advantages", "disadvantages"], ["advantage", "disadvantage"], '
       '["before", "after"], ["do", "don\'t"], ["dos", "don\'ts"], ["true", "false"], ["similarities", "differences"], ["fact", "opinion"], '
       '["facts", "opinions"], ["strengths", "weaknesses"], ["positive", "negative"], ["positives", "negatives"], ["cause", "effect"], '
       '["causes", "effects"], ["then", "now"], ["past", "present"], ["benefits", "risks"], ["benefits", "costs"], ["for", "against"], '
       '["agree", "disagree"], ["wants", "needs"], ["living", "non-living"], ["renewable", "non-renewable"], ["input", "output"], '
       '["problem", "solution"], ["question", "answer"], ["english", "te reo"], ["english", "maori"]]')
block = "\n".join([
    T*3 + '"kb_class_form": {',
    T*4 + '"enabled": true,',
    T*4 + '"env": "TBLBORDER_OFF",',
    T*4 + '"default_class": "table table-bordered",',
    T*4 + '"comparison": {',
    T*5 + '"enabled": false,',
    T*5 + '"class": "table tableFixed",',
    T*5 + '"lexicon": ' + lex + ',',
    T*5 + '"note": "ROUND 347: shipped OFF. The gold\'s two-column contrast-header tables (13 across the corpus) split four ways — plain table 4 / '
          'table-bordered 3 / bordered+tableFixed 5 / tableFixed 1 — and the gold\'s two-column tables overall are plain table 229 vs any tableFixed 85, '
          'so the KB\'s comparison-table rule has no lexicon the corpus confirms; the hook stays data-ready for a KB session that settles one."',
    T*4 + '},',
    T*4 + '"rule": "ROUND 347 (Chris\'s D10-5, KB 05D level 1): every content table ships <table class=\\"table table-bordered\\"> inside the '
          'table-responsive wrapper (the gold: bordered 1011 / 1819 tables — Standard a 0.51 tie, Inquiry 0.72, Fundamentals 0.69, Bilingual 0.86 — '
          'a NAMED override on the Standard plain-table pages). 05D\'s optional noHover / center-text are not emitted. Env TBLBORDER_OFF restores the bare table class."',
    T*3 + '},',
]) + "\n"
splice(os.path.join(ROOT, "data", "Emit_Templates.json"), cell, cell + block, "kb_class_form", "data Emit_Templates.json")

# ---- engine: the table class form -------------------------------------------------------------------------------------
open_anchor = T*2 + "const html = [t.open];\n"
open_code = r'''		// ROUND 347 (Chris's D10-5, KB 05D): every content table ships the KB class form —
		// `table table-bordered` by default; a two-column COMPARISON table (every row exactly
		// two cells AND a header pair from the contrast lexicon) ships `table tableFixed` when
		// kb_class_form.comparison is enabled (shipped OFF: the gold's contrast tables split
		// four ways, measured r347). The wrapper and the th header rule are unchanged.
		// Data flag: elements.table.kb_class_form. Env toggle: TBLBORDER_OFF (bare `table`).
		const cf = t.kb_class_form;
		const cfOn = !!cf && cf.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[cf.env ?? "TBLBORDER_OFF"]);
		let open = t.open;
		if (cfOn) {
			let cls = cf.default_class || "table table-bordered";
			const cmp = cf.comparison;
			if (cmp && cmp.enabled === true && Array.isArray(cmp.lexicon) && rows.length && rows.every((cells) => cells.length === 2)) {
				const fold = (c) => Utils.Fold(String(c ?? "").replace(/<[^>]+>/g, "").replace(/\[[^\]]*\]/g, "").replace(/\*/g, "")).replace(/[^\p{L}' ]+/gu, " ").trim();
				const [a, b] = rows[0].map(fold);
				if (cmp.lexicon.some(([x, y]) => (a.startsWith(x) && b.startsWith(y)) || (a.startsWith(y) && b.startsWith(x)))) cls = cmp.class || "table tableFixed";
			}
			open = open.replace(/<table class="table">/, `<table class="${cls}">`);
		}
		const html = [open];
'''
splice(os.path.join(ROOT, "app", "js", "TablesAndGrids.js"), open_anchor, open_code, "kb_class_form", "engine TablesAndGrids.js")

# ---- engine: the carried math-alpha fix -----------------------------------------------------------------------------
p = os.path.join(ROOT, "app", "js", "DocxExtractor.js")
a1 = "\t_tokenise(text) {\n\t\tconst out = []; let i = 0;\n"
n1 = "\t_tokenise(text) {\n\t\ttext = OmmlMathml._foldMathAlpha(text);   // ROUND 347: U+1D465 (math italic x) -> x before any per-unit walk\n\t\tconst out = []; let i = 0;\n"
splice(p, a1, n1, "_foldMathAlpha(text)", "engine DocxExtractor.js tokenise")
a2 = r'''else { flush(); for (let c = 0; c < tok.text.length; c++) out += "<mi>" + this._escapeText(tok.text.charAt(c)) + "</mi>"; }'''
n2 = r'''else { flush(); for (const c of tok.text) out += "<mi>" + this._escapeText(c) + "</mi>"; }   // ROUND 347: by code point, never by UTF-16 unit'''
splice(p, a2, n2, "for (const c of tok.text)", "engine DocxExtractor.js mi loop")
a3 = '\tstatic _isDigit(ch) { return ch >= "0" && ch <= "9"; }\n'
fold = r'''	/** ROUND 347: Mathematical Alphanumeric Symbols (U+1D400-U+1D7FF - Word's italic x, bold b, bold 3 ...) fold to the plain letter /
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
'''
splice(p, a3, a3 + fold, "static _foldMathAlpha", "engine DocxExtractor.js fold")

# ---- the math verifier (gate tool + its loop/ mirror) ---------------------------------------------------------------
va = r'''	if (!/^<math xmlns="http:\/\/www\.w3\.org\/1998\/Math\/MathML"/.test(mathHtml)) return false;
'''
vn = va + r'''	if (/�|\p{Cs}/u.test(mathHtml)) return false;   // ROUND 347: a replacement char or a lone surrogate = a lost letter
'''
for d in (TESTS, os.path.join(ROOT, "loop")):
    splice(os.path.join(d, "_verify_math.cjs"), va, vn, r"\p{Cs}", "verifier " + d.split("/")[-1])
