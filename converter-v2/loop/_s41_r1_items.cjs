"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
DataService.Data.AcksFormats.oembed.throttle_ms = 0;
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
globalThis.norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
(async () => {
const code = process.argv[2], lim = +(process.argv[3] || 40);
let dir; for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) dir = d; }
const run = new ConversionRun({ imageMode: "P", interactiveMode: "extract" });
const docs = [];
for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
	const buf = fs.readFileSync(path.join(dir, name));
	const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
	console.log = () => {}; docs.push({ name, doc: await DocxExtractor.Extract(zip) }); console.log = _l;
}
const raw = docs.map(d => `${d.name}: ${d.doc.blocks.length} blocks`).join("; ");
console.log = () => {};
ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
const items = PageSplitter.BuildItemStream(run.wtBlocks, norm);
console.log = _l;
console.log(raw, "| wtBlocks", run.wtBlocks.length, "| items", items.length);
items.slice(0, lim).forEach((it, i) => {
	const b = it.block || {};
	const txt = b.kind === "table" ? `TABLE ${b.rows?.length}x${b.rows?.[0]?.length} ` + JSON.stringify((b.rows||[]).slice(0,2)).slice(0, 110) : String(it.text || b.text || "");
	console.log(String(i).padStart(4), String(it.type).padEnd(6), String(it.parse?.primary?.tag || "").padEnd(14), "|", txt.replace(/\s+/g, " ").slice(0, 150));
});
})().catch(e => { console.error(e); process.exit(1); });
