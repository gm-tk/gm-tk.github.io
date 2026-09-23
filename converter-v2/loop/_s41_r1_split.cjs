"use strict";
// Session 41 Round 1 PICK — the splitter's pages and every lesson/page-ish item for the named modules.
// node --require ../reference/tests/_deflate_raw_polyfill.cjs _s41_r1_split.cjs <CODE> [<CODE> …]
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false, reason:"stubbed" }; } };
DataService.Data.AcksFormats.oembed.throttle_ms = 0;
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
globalThis.norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
function find(code) {
	for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) return d; }
	return null;
}
(async () => {
for (const code of process.argv.slice(2)) {
	const dir = find(code);
	const run = new ConversionRun({ imageMode: "P", interactiveMode: "extract" });
	const docs = [];
	for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
		const buf = fs.readFileSync(path.join(dir, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		console.log = () => {};
		docs.push({ name, doc: await DocxExtractor.Extract(zip) });
		console.log = _l;
	}
	console.log = () => {};
	ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
	const items = PageSplitter.BuildItemStream(run.wtBlocks, norm);
	const pages = PageSplitter.Split(items, run, norm);
	console.log = _l;
	console.log(`\n=== ${code} reoMode=${!!run.reoMode} mtk=${!!run.mtkFlag} pages=${pages.length}: ` + pages.map(p => `${p.lessonLabel ?? "?"}(${p.items.length})`).join(" "));
	items.forEach((it, i) => {
		const txt = String(it.text || it.block?.text || "").replace(/\s+/g, " ");
		const tag = it.parse?.primary?.tag || "";
		if ((it.type === "tag" && /lesson|page/.test(tag)) || /\[\s*(lesson|end ?page|page)\b/i.test(txt) || /^\W*(lesson|ngohe)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b/i.test(txt.replace(/🔴|\[\/?RED TEXT\]|\[[^\]]*\]|\*/g, "").trim()))
			console.log(String(i).padStart(4), it.type.padEnd(6), String(tag).padEnd(16), JSON.stringify(it.parse?.numbers ?? []).padEnd(8), "|", txt.slice(0, 100));
	});
	for (const n of run.notes ?? []) if (n.stage === "PageSplitter") console.log("   note:", String(n.text).slice(0, 200));
}
})().catch(e => { console.error(e); process.exit(1); });
