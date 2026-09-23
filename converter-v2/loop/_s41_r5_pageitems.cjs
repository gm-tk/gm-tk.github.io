"use strict";
// print the items of the named pages (all pages with <= maxItems items) for a module — node … _s41_r5_pageitems.cjs CODE [maxItems]
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
(async () => {
const code = process.argv[2], max = +(process.argv[3] || 12);
let dir; for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) dir = d; }
const docs = [];
for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
	const buf = fs.readFileSync(path.join(dir, name));
	const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
	console.log = () => {}; docs.push({ name, doc: await DocxExtractor.Extract(zip) }); console.log = _l;
}
const run = new ConversionRun({ imageMode: "P", interactiveMode: "extract" });
console.log = () => {};
ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
const items = PageSplitter.BuildItemStream(run.wtBlocks, norm);
const pages = PageSplitter.Split(items, run, norm);
console.log = _l;
pages.forEach((p, pi) => {
	if (p.items.length > max) { console.log(`-- ${p.lessonLabel} (${p.items.length} items) first: ${String(p.items[0]?.text ?? "").replace(/\s+/g, " ").slice(0, 80)}`); return; }
	console.log(`== ${p.lessonLabel} (${p.items.length} items) title="${p.pageTitle}"`);
	p.items.forEach((it) => console.log(`     ${it.type.padEnd(6)} ${String(it.parse?.primary?.tag ?? "").padEnd(14)} | ${(String(it.text ?? it.block?.text ?? "") + " " + String(it.blackAfter ?? "")).replace(/\s+/g, " ").slice(0, 110)}`));
});
})().catch(e => { console.error(e); process.exit(1); });
