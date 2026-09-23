"use strict";
// Session 41 Round 7 PICK — THE MODULE INTRODUCTION SPLIT OFF THE OVERVIEW. For every module: split with the live engine; report
// the first lesson page when (a) any of its first 3 items reads "module introduction" / "introduction" (tag or black, any bracket,
// any case), or (b) it is tiny (<= 15 items) and the module's gold overview carries >= 50 % of its text. Prints the item forms.
// node --require ../reference/tests/_deflate_raw_polyfill.cjs _s41_r7_intro.cjs [CODE …]
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const N = (s) => String(s).toLowerCase().replace(/🔴|\[\/?red text\]|\[[^\]]{0,40}\]/g, " ").replace(/[‘’“”'"`*_]/g, "").replace(/[^0-9a-zāēīōū]+/g, " ").replace(/\s+/g, " ").trim();
const SH = (s, k = 5) => { const w = s.split(" ").filter(Boolean); const o = new Set(); for (let i = 0; i + k <= w.length; i++) o.add(w.slice(i, i + k).join(" ")); return o; };
const itext = (it) => String(it.text ?? it.block?.text ?? "") + " " + String(it.blackAfter ?? "");
(async () => {
const only = process.argv.slice(2);
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
	let pages;
	const run = new ConversionRun({ imageMode: "P", interactiveMode: "extract" });
	try {
		console.log = () => {};
		ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
		pages = PageSplitter.Split(PageSplitter.BuildItemStream(run.wtBlocks, norm), run, norm);
		console.log = _l;
	} catch (e) { console.log = _l; continue; }
	if (pages.length < 2 || !pages[0].isOverview) continue;
	const p1 = pages[1];
	const head = p1.items.slice(0, 3).map(itext).join(" | ").replace(/\s+/g, " ");
	const introWord = /\bmodule introduction\b|\bintroduction\b/i.test(head.replace(/🔴|\[\/?RED TEXT\]/g, ""));
	const g0 = fs.readdirSync(dir).find((f) => /^[A-Z]+\d+[_\-.]0+[._]0\.html$|_0_0\.html$|[-_]00\.0\.html$|_0\.0\.html$|-0\.0\.html$/i.test(f));
	let share = null;
	if (g0) {
		const gs = SH(N(fs.readFileSync(path.join(dir, g0), "utf8").replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, " ").replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")));
		const ps = SH(N(p1.items.map(itext).join(" ")));
		if (ps.size) share = [...ps].filter((x) => gs.has(x)).length / ps.size;
	}
	if (!(introWord || (p1.items.length <= 15 && share != null && share >= 0.5))) continue;
	console.log(`## ${t} ${code} p1=${p1.lessonLabel} items=${p1.items.length} inGoldOverview=${share == null ? "-" : share.toFixed(2)} introWord=${introWord}`);
	console.log(`   ${p1.items.slice(0, 3).map((it) => it.type + (it.parse?.primary?.tag ? "/" + it.parse.primary.tag : "") + ": " + itext(it).replace(/\s+/g, " ").trim().slice(0, 60)).join("  ||  ")}`);
}
})().catch(e => { console.error(e); process.exit(1); });
