// _verify_math.cjs — ROUND 346 (Chris's D10-7): Word equations ship as MathML.
//
// For each module: converts it in memory (the batch_convert path), counts the <m:oMath>
// equations in the writer's docx and the <math> elements on the built pages, and checks
//   1. counts agree (every equation reaches a page; none invented),
//   2. every page carrying a <math> carries the mathJax body class,
//   3. no equation sentinel (U+E010 / U+E011) leaks into a page or the hand-off .txt,
//   4. every <math> is well-formed at the MathML level: namespace present, balanced tags.
// Per module: equations, math, defect (count mismatch + mathJax misses + leaks + malformed).
//
// Usage:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_math.cjs MXDI301 PES1008 …
//         node --require ./_deflate_raw_polyfill.cjs _verify_math.cjs --selftest
// Selftest (INJECT): with CV2_SELFTEST_INJECT the verifier strips one <math> from the first
// built math page — the count mismatch must register as a defect (DETECTION), and the
// fixture modules must build > 0 equations (LIVENESS).
"use strict";
const fs = require("fs"), path = require("path");
const corpus = require("./corpus.cjs");
if (process.argv.includes("--selftest")) { require("./_selftest_core.cjs").selftest(__filename); return; }
const MODS = process.env.CV2_MODS_ROOT || path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_");
const eng = require("./_engine_load.cjs");
const Data = eng.loadData();
Data.AcksFormats.oembed.throttle_ms = 0;
globalThis.DataService = { Data, async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
eng.loadEngine();
const norm = new TagNormaliser(Data.TagLexicon, Data.TagExceptions, Data.InstructionCues);
const TOKEN = Data.InputDocRules?.math?.body_class_token || "mathJax";
const SENT = /[\uE010\uE011]/;

async function convertModule(mod) {
	const base = corpus.mdir(MODS, mod);
	const run = new ConversionRun({ imageMode: "P" });
	const docs = []; let omath = 0;
	const before = DocxExtractor.MathRegistered();
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
		const buf = fs.readFileSync(path.join(base, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		docs.push({ name, doc: await DocxExtractor.Extract(zip) });
		// the docx equation count, read straight from the XML the way the measurement tool does
		const xml = zip.Has("word/document.xml") ? await zip.ReadText("word/document.xml") : "";
		omath += (xml.match(/<m:oMath\b[^>]*>/g) || []).length;
	}
	const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f))
		.map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
	const log = console.log, warn = console.warn, err = console.error;
	console.log = () => {}; console.warn = () => {}; console.error = () => {};
	try {
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
		if (!prep.ok) throw new Error(`prep refused (${prep.reason})`);
		await PageAssembler.AssembleModule(run, norm);
	} finally { console.log = log; console.warn = warn; console.error = err; }
	const registered = DocxExtractor.MathRegistered() - before;
	return { pages: run.outputs.filter((o) => /\.html$/.test(o.filename)).map((o) => ({ name: o.filename, html: String(o.content ?? "") })),
		txt: run.outputs.filter((o) => /\.txt$/.test(o.filename)).map((o) => String(o.content ?? "")).join("\n"),
		omath, registered };
}

function wellFormed(mathHtml) {
	if (!/^<math xmlns="http:\/\/www\.w3\.org\/1998\/Math\/MathML"/.test(mathHtml)) return false;
	if (/\uFFFD|\p{Cs}/u.test(mathHtml)) return false;   // ROUND 347: a replacement char or a lone surrogate = a lost letter
	const stack = [];
	for (const m of mathHtml.matchAll(/<(\/?)([a-z]+)\b[^>]*?(\/?)>/g)) {
		if (m[3] === "/") continue;
		if (m[1] === "/") { if (stack.pop() !== m[2]) return false; }
		else stack.push(m[2]);
	}
	return stack.length === 0;
}

(async () => {
	let totEq = 0, totMath = 0, totDefect = 0, mods = 0;
	for (const mod of process.argv.slice(2)) {
		let r;
		try { r = await convertModule(mod); } catch (e) { console.log(`${mod}: ERROR ${e.message}`); continue; }
		mods++;
		if (process.env.CV2_SELFTEST_INJECT) {
			const p = r.pages.find((x) => /<math\b/.test(x.html));
			if (p) p.html = p.html.replace(/<math\b[\s\S]*?<\/math>/, "");   // one equation lost — must be caught
		}
		let math = 0, mathPages = 0, noJax = 0, leaks = 0, bad = 0;
		for (const p of r.pages) {
			const ms = p.html.match(/<math\b[\s\S]*?<\/math>/g) || [];
			math += ms.length;
			if (ms.length) {
				mathPages++;
				if (!new RegExp(`<body class="[^"]*(^|\\s)${TOKEN}(\\s|")`).test(p.html)) noJax++;
				for (const m of ms) if (!wellFormed(m.replace(/\s+/g, " "))) bad++;
			}
			if (SENT.test(p.html)) leaks++;
		}
		if (SENT.test(r.txt)) leaks++;
		const mismatch = Math.abs(r.omath - math);
		const defect = mismatch + noJax + leaks + bad;
		totEq += r.omath; totMath += math; totDefect += defect;
		console.log(`${mod}: equations ${r.omath} (registered ${r.registered}) / <math> ${math} on ${mathPages} page(s); ${TOKEN} missing ${noJax}; sentinel leaks ${leaks}; malformed ${bad}; defect ${defect}${defect ? " ✗" : " ✓"}`);
	}
	console.log(`TOTAL: ${totEq} equation(s) across ${mods} module(s); <math> ${totMath}; defect ${totDefect}.`);
	console.log(totDefect ? "RESULT: real defects present ✗ — fix before proceeding." : "RESULT: every Word equation ships as MathML ✓");
	process.exit(totDefect ? 1 : 0);
})();
