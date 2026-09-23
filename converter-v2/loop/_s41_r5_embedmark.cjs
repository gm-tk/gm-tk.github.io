"use strict";
// Session 41 Round 5 PICK — THE EMBEDDED LESSON-BOUNDARY MARKERS: every page the live splitter opens at a "lesson"/"page"
// PAGE_BOUNDARY span that matched how:'embedded' (the r245 pool — "[Lesson Summary]", "[lesson title]", "[Next Page]" …), per
// module, with the marker text, the page's item count, and the module's gold / Claude page counts.
// node --require ../reference/tests/_deflate_raw_polyfill.cjs _s41_r5_embedmark.cjs [CODE …]
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
(async () => {
const only = process.argv.slice(2);
const byMarker = new Map();
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
	let items, pages;
	const run = new ConversionRun({ imageMode: "P", interactiveMode: "extract" });
	try {
		console.log = () => {};
		ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
		items = PageSplitter.BuildItemStream(run.wtBlocks, norm);
		pages = PageSplitter.Split(items, run, norm);
		console.log = _l;
	} catch (e) { console.log = _l; continue; }
	// which items are embedded lesson/page boundaries?
	const emb = new Set(items.filter((it) => it.type === "tag" && it.parse?.primary?.directive === "PAGE_BOUNDARY"
		&& ["lesson", "page"].includes(it.parse.primary.tag) && it.parse.primary.how === "embedded"));
	if (!emb.size) continue;
	const gp = fs.readdirSync(dir).filter((f) => f.endsWith(".html") && !/glossary|claude/i.test(f)).length;
	const hits = [];
	for (const it of emb) {
		const pg = pages.find((p) => p.items[0] === it || p.items.includes(it));
		const opened = pages.find((p) => p.items[0] === it) || null;
		const txt = String(it.text ?? "").replace(/\s+/g, " ").trim().slice(0, 50);
		const key = String(it.parse?.folded ?? txt).toLowerCase().replace(/\d+/g, "N").replace(/\s+/g, " ").trim().slice(0, 40);
		hits.push(`${txt}${opened ? ` → opens ${opened.lessonLabel} (${opened.items.length})` : " (no page)"}`);
		if (!byMarker.has(key)) byMarker.set(key, { n: 0, mods: new Set(), opens: 0 });
		const b = byMarker.get(key); b.n++; b.mods.add(code); if (opened) b.opens++;
	}
	console.log(`## ${t} ${code} gold_html=${gp} claude_pages=${pages.length} embedded=${emb.size}`);
	for (const h of hits.slice(0, 6)) console.log("   " + h);
}
console.log("\nBY MARKER (folded, digits→N):");
for (const [k, v] of [...byMarker.entries()].sort((a, b) => b[1].n - a[1].n)) console.log(`  ${String(v.n).padStart(3)} spans / ${String(v.mods.size).padStart(2)} modules / opens ${v.opens}: ${k}  [${[...v.mods].slice(0, 6).join(" ")}]`);
})().catch(e => { console.error(e); process.exit(1); });
