"use strict";
// Session 41 Round 4 PICK — LESSON MARKERS THE SPLITTER LEAVES MID-PAGE. For every module: split the WT with the live engine;
// inside each page (past its first 3 items) find an item whose text reads as a lesson opener — a black "[LESSON 4]" line, an
// "[H1]/[H2] Lesson Four: …" / "Lesson 4 …" heading, "[H1] [LESSON 1] …" — whose lesson number is HIGHER than the page's own.
// Prints one row per hit + per-module totals + the gold page count vs Claude's.
// node --require ../reference/tests/_deflate_raw_polyfill.cjs _s41_r4_midlesson.cjs [CODE …]   (no codes = every gold module)
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
DataService.Data.AcksFormats.oembed.throttle_ms = 0;
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const WORDS = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12 };
const txt = (it) => (String(it.text ?? it.block?.text ?? "") + " " + String(it.blackAfter ?? "")).replace(/🔴|\[\/?RED TEXT\]/g, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
function lessonNum(t) {
	let m = t.match(/^(?:\[\s*h[1-4]\s*\]\s*)?(?:\[\s*)?lesson\s+(\d+|[a-z]+)\s*\]?\s*(?:[:\-–—.]|$|\s)/i);
	if (!m) return null;
	const v = /^\d+$/.test(m[1]) ? parseInt(m[1], 10) : WORDS[m[1].toLowerCase()];
	return v ?? null;
}
(async () => {
const only = process.argv.slice(2);
let totHits = 0, mods = 0;
for (const t of fs.readdirSync(GOLD)) for (const code of fs.readdirSync(path.join(GOLD, t))) {
	if (only.length && !only.includes(code)) continue;
	const dir = path.join(GOLD, t, code);
	const docs = [];
	try {
		for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(dir, name));
			const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
			console.log = () => {}; docs.push({ name, doc: await DocxExtractor.Extract(zip) }); console.log = _l;
		}
	} catch (e) { console.log = _l; continue; }
	const run = new ConversionRun({ imageMode: "P", interactiveMode: "extract" });
	let pages;
	try {
		console.log = () => {};
		ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
		const items = PageSplitter.BuildItemStream(run.wtBlocks, norm);
		pages = PageSplitter.Split(items, run, norm);
		console.log = _l;
	} catch (e) { console.log = _l; continue; }
	const hits = [];
	for (const p of pages) {
		const own = parseInt(String(p.lessonNumber ?? p.lessonLabel ?? "").split(".")[0], 10);
		p.items.forEach((it, k) => {
			if (k < 3) return;
			const s = txt(it);
			if (!s || s.length > 140) return;
			const n = lessonNum(s);
			if (n == null) return;
			if (!isNaN(own) && n <= own) return;
			hits.push(`${p.lessonLabel ?? "?"}#${k} ${it.type}${it.parse?.primary?.tag ? "/" + it.parse.primary.tag : ""} "${s.slice(0, 70)}"`);
		});
	}
	if (!hits.length) continue;
	mods++; totHits += hits.length;
	const gp = fs.readdirSync(dir).filter((f) => f.endsWith(".html")).length;
	console.log(`## ${t} ${code} pages=${pages.length} gold_html=${gp} mid-page lesson openers=${hits.length}`);
	for (const h of hits.slice(0, 8)) console.log("   " + h);
}
console.log(`TOTAL modules ${mods} hits ${totHits}`);
})().catch(e => { console.error(e); process.exit(1); });
