/** _verify_typing.cjs — the TYPING-QUIZ verifier (round 449, Chris's decision D13-4).
 *
 *  Every widget round ships a verifier with a --selftest whose DETECTION channel must fire on
 *  doctored input (the r149 rail). This is the first one the typing quiz has had.
 *
 *  DEFECT criteria — a built typing quiz must be the KB 03D text-only form:
 *    - the container is div.typing with layout="standardNoBorder" and holds one div.typingContainer
 *    - every question row is a div.row holding a <p> with at least one input and some question text
 *    - every input is class="form-control" type="text" placeholder="Type here" caseSensitive="false"
 *      with a NON-EMPTY answer=
 *    - the reset / checkAnswer hidden / showAnswer hidden button row follows the container
 *    - no residual writer bracket inside the widget
 *  Compared with the human's own module where it has typing inputs: a built answer that equals one
 *  of the gold's answer= values (normalised; "a||b" alternatives split) is EXACT; otherwise it is
 *  counted as "no gold match" (the gold often builds these as a carousel or a different quiz type,
 *  so it is reported, not a defect).
 *
 *  Usage (FROM reference/tests/):
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_typing.cjs CODE...
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_typing.cjs --selftest
 */
"use strict";
const fs = require("fs"), path = require("path");
const eng = require("./_engine_load.cjs");
const GOLD = path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_");
const unesc = (s) => String(s).replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");
const norm = (s) => unesc(s).toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
function dirOf(c) { for (const t of fs.readdirSync(GOLD)) { const p = path.join(GOLD, t, c); if (fs.existsSync(p)) return p; } return null; }
/** every typing widget in a page: its opening tag, container, rows and the buttons after it */
function parse(html) {
	const out = [];
	const re = /<div class="(typing(?:\s[^"]*)?)"([^>]*)>\s*<div class="typingContainer">([\s\S]*?)<\/div>\s*<div class="row">\s*((?:<div class="activityButton[^"]*">[^<]*<\/div>\s*)+)<\/div>\s*<\/div>/g;
	let m;
	while ((m = re.exec(html))) {
		const rows = [...m[3].matchAll(/<div class="row">\s*<p>([\s\S]*?)<\/p>\s*<\/div>/g)].map((r) => r[1]);
		const rowCount = (m[3].match(/<div class="row">/g) || []).length;
		out.push({ cls: m[1], attrs: m[2], rows, rowCount, buttons: m[4], raw: m[0] });
	}
	return out;
}
/** ROUND 518 — the TABLE form (r517, InteractiveBuilder.#typingTable): div.typing layout="standard" > div.table-responsive >
 *  table (rows = <tr>, each red answer an <input>) + the button row. Each table is one quiz; its rows are the <tr>s that hold an
 *  input (a header / worked-example row holds none). */
function parseTable(html) {
	const out = [];
	const re = /<div class="(typing(?:\s[^"]*)?)"([^>]*)>\s*<div class="table-responsive">\s*<table\b[^>]*>([\s\S]*?)<\/table>\s*<\/div>\s*<div class="row">\s*((?:<div class="activityButton[^"]*">[^<]*<\/div>\s*)+)<\/div>\s*<\/div>/g;
	let m;
	while ((m = re.exec(html))) {
		const trs = [...m[3].matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map((r) => r[1]);
		out.push({ table: true, cls: m[1], attrs: m[2], rows: trs.filter((t) => /<input\b/.test(t)), allRows: trs, buttons: m[4], raw: m[0] });
	}
	return out;
}
function defectsTable(ws) {
	const d = [];
	for (const w of ws) {
		if (!/\blayout="standard"/.test(w.attrs)) d.push("table form lacks layout=\"standard\"");
		if (!w.rows.length) d.push("table form has no input row");
		for (const r of w.rows) for (const a of inputs(r)) {
			if (!/\bclass="form-control"/.test(a) || !/\btype="text"/.test(a)) d.push("an input is not form-control / type=text");
			if (!/\bplaceholder="Type here"/.test(a)) d.push("an input lacks placeholder=\"Type here\"");
			if (!/\bcaseSensitive="false"/.test(a)) d.push("an input lacks caseSensitive=\"false\"");
			const ans = (a.match(/\banswer="([^"]*)"/) || [])[1];
			if (!ans || !ans.trim() || /^\[|\]$/.test(ans.trim())) d.push("a table input with no (or a bracketed) answer");
		}
		for (const b of ["activityButton reset", "activityButton checkAnswer hidden", "activityButton showAnswer hidden"])
			if (!w.buttons.includes(`class="${b}"`)) d.push(`table form's button row lacks ${b}`);
		if (/\[[^\]\n]{0,120}\]/.test(w.raw.replace(/answer="[^"]*"/g, ""))) d.push("the table form still shows a writer bracket");
	}
	return d;
}
function inputs(p) { return [...p.matchAll(/<input\b([^>]*)\/?>/g)].map((x) => x[1]); }
function defects(ws) {
	const d = [];
	for (const w of ws) {
		if (!/\blayout="standardNoBorder"/.test(w.attrs)) d.push("container lacks layout=\"standardNoBorder\"");
		if (!w.rows.length) d.push("no question rows");
		if (w.rows.length !== w.rowCount) d.push(`${w.rowCount - w.rows.length} row(s) not a single <p>`);
		for (const p of w.rows) {
			const ins = inputs(p);
			const text = p.replace(/<input\b[^>]*\/?>/g, " ").replace(/<[^>]+>/g, " ").trim();
			if (!ins.length) d.push(`row "${text.slice(0, 30)}" has no input`);
			if (!text) d.push("a row with no question text");
			for (const a of ins) {
				if (!/\bclass="form-control"/.test(a) || !/\btype="text"/.test(a)) d.push("an input is not form-control / type=text");
				if (!/\bplaceholder="Type here"/.test(a)) d.push("an input lacks placeholder=\"Type here\"");
				if (!/\bcaseSensitive="false"/.test(a)) d.push("an input lacks caseSensitive=\"false\"");
				const ans = (a.match(/\banswer="([^"]*)"/) || [])[1];
				if (!ans || !ans.trim()) d.push(`row "${text.slice(0, 30)}" has an input with no answer`);
			}
		}
		for (const b of ["activityButton reset", "activityButton checkAnswer hidden", "activityButton showAnswer hidden"])
			if (!w.buttons.includes(`class="${b}"`)) d.push(`button row lacks ${b}`);
		if (/\[[^\]\n]{0,120}\]/.test(w.raw)) d.push("the widget still shows a writer bracket");
	}
	return d;
}
let norm_;
async function convert(code) {
	const d = dirOf(code); if (!d) return null;
	const run = new ConversionRun({ imageMode: "P" }); const docs = [];
	for (const n of fs.readdirSync(d).filter((f) => f.endsWith(".docx"))) {
		const b = fs.readFileSync(path.join(d, n));
		docs.push({ name: n, doc: await DocxExtractor.Extract(new ZipReader(b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength))) });
	}
	const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm_ });
	if (!prep.ok) return null;
	await PageAssembler.AssembleModule(run, norm_);
	return run;
}
(async () => {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
	eng.loadEngine();   // the engine narrates to console.log — kept silent; results print through _l
	norm_ = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);

	if (process.argv.includes("--selftest")) {
		const run = await convert("BLL244");
		const html = (run.outputs || []).filter((o) => /\.html$/.test(o.filename)).map((o) => o.content).join("\n");
		const ws = parse(html);
		let ok = true;
		const nIn = ws.reduce((n, w) => n + w.rows.reduce((k, p) => k + inputs(p).length, 0), 0);
		if (nIn < 6) { _l(`  ✗ LIVENESS: the fixture built ${nIn} typing input(s), expected >= 6`); ok = false; }
		else _l(`  ✓ LIVENESS: BLL244 builds ${ws.length} typing quiz(zes) with ${nIn} inputs`);
		if (defects(ws).length) { _l("  ✗ LIVENESS: the clean fixture reports a defect: " + defects(ws).join("; ")); ok = false; }
		else _l("  ✓ LIVENESS: the clean fixture reports defect 0");
		const cases = [
			["an answer emptied", html.replace(/ answer="[^"]*"/, ' answer=""')],
			["the layout removed", html.replace(/ layout="standardNoBorder"/, "")],
			["a writer bracket injected", html.replace(/(<div class="typingContainer">\s*<div class="row">\s*<p>)/, "$1[type the answer] ")],
			["the caseSensitive attribute dropped", html.replace(/ caseSensitive="false"/, "")],
			["the showAnswer button dropped", html.replace(/<div class="activityButton showAnswer hidden">Show<\/div>/, "")],
		];
		for (const [name, doctored] of cases) {
			const n = defects(parse(doctored)).length;
			if (n) _l(`  ✓ DETECTION: ${name} → ${n} defect(s)`);
			else { _l(`  ✗ DETECTION: ${name} was NOT caught`); ok = false; }
		}
		// ROUND 518 — the TABLE form (r517): MXFUN01's `[Type and check]` tables
		const runT = await convert("MXFUN01");
		const htmlT = (runT?.outputs || []).filter((o) => /\.html$/.test(o.filename)).map((o) => o.content).join("\n");
		const wt = parseTable(htmlT);
		const nT = wt.reduce((n, w) => n + w.rows.reduce((k, r) => k + inputs(r).length, 0), 0);
		if (nT < 20) { _l(`  ✗ LIVENESS: MXFUN01 built ${nT} table-form input(s), expected >= 20`); ok = false; }
		else _l(`  ✓ LIVENESS: MXFUN01 builds ${wt.length} table-form quiz(zes) with ${nT} inputs`);
		if (defectsTable(wt).length) { _l("  ✗ LIVENESS: the clean table fixture reports a defect: " + defectsTable(wt).join("; ")); ok = false; }
		else _l("  ✓ LIVENESS: the clean table fixture reports defect 0");
		for (const [name, doctored] of [
			["a table answer emptied", htmlT.replace(/(<div class="table-responsive">[\s\S]*?) answer="[^"]*"/, '$1 answer=""')],
			["a table answer left bracketed", htmlT.replace(/(<div class="table-responsive">[\s\S]*?) answer="([^"]*)"/, '$1 answer="[$2]"')],
			["the table form's layout removed", htmlT.replace(/(<div class="typing[^"]*") layout="standard"/, "$1")],
		]) {
			const n = defectsTable(parseTable(doctored)).length;
			if (n) _l(`  ✓ DETECTION: ${name} → ${n} defect(s)`);
			else { _l(`  ✗ DETECTION: ${name} was NOT caught`); ok = false; }
		}
		_l(ok ? "SELFTEST GREEN" : "SELFTEST FAIL"); process.exit(ok ? 0 : 1);
	}

	let W = 0, A = 0, D = 0, exact = 0, nomatch = 0, nogold = 0;
	const perMod = {};   // ROUND 501: each module's built quiz count, for the count-vs-baseline test (_verify_count.cjs)
	for (const code of process.argv.slice(2)) {
		const run = await convert(code); if (!run) continue;
		const w0 = W;
		const gd = dirOf(code);
		const gold = new Set();
		for (const f of fs.readdirSync(gd).filter((x) => /\.html?$/i.test(x))) {
			const g = fs.readFileSync(path.join(gd, f), "utf8").replace(/<!--[\s\S]*?-->/g, "");
			for (const a of g.matchAll(/<input\b[^>]*\banswer="([^"]*)"/g)) for (const x of a[1].split("||")) gold.add(norm(x));
		}
		for (const o of run.outputs || []) {
			if (!/\.html$/.test(o.filename || "")) continue;
			const w1 = parse(o.content), wt = parseTable(o.content);   // ROUND 518: + the table form (r517)
			const ws = [...w1, ...wt]; if (!ws.length) continue;
			const dd = [...defects(w1), ...defectsTable(wt)]; D += dd.length; W += ws.length;
			let n = 0, hit = 0;
			for (const w of ws) for (const p of w.rows) for (const a of inputs(p)) {
				n++; const ans = norm((a.match(/\banswer="([^"]*)"/) || [])[1] || "");
				if (!gold.size) nogold++;
				else if (gold.has(ans)) { exact++; hit++; }
				else nomatch++;
			}
			A += n;
			_l(`${code} ${o.filename}: ${ws.length} typing quiz(zes), ${n} input(s), gold-matched ${hit}${dd.length ? "  DEFECTS: " + dd.join("; ") : ""}`);
		}
		perMod[code] = W - w0;
	}
	_l(`\nTOTAL ${W} typing quiz(zes) / ${A} input(s): answer = a gold answer ${exact}, no gold match ${nomatch}, module has no gold typing ${nogold} | DEFECTS ${D}`);
	// ROUND 501 (LOOP §3 step 6): the count test — ✗ when the quiz / input count FELL against gate_baseline.json.typing.
	const C = require("./_verify_count.cjs").countTest("typing", { quizzes: W, inputs: A }, perMod, process.argv.slice(2), _l);
	_l(D !== 0 ? "RESULT: DEFECTS PRESENT"
		: C.fell ? "RESULT: the built typing-quiz count FELL against the recorded baseline ✗ — a vacuous pass (see the COUNT line)."
		: "RESULT: defect 0 ✓");
	if (D !== 0 || C.fell) process.exitCode = 1;
})().catch((e) => { console.error(e); process.exit(1); });
