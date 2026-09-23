"use strict";
// every WT: the standard content start, the first PARA title bar, the first TABLE-CELL title bar
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const isTB = (s) => [...String(s).matchAll(RED)].some(m => norm.Parse(m[1]).primary?.tag === "title bar") || /\[\s*title bar\s*\]/i.test(s);
(async () => {
const only = process.argv.slice(2);
for (const t of fs.readdirSync(GOLD)) for (const code of fs.readdirSync(path.join(GOLD, t))) {
	if (only.length && !only.some(p => code.startsWith(p))) continue;
	const dir = path.join(GOLD, t, code);
	for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
		let doc;
		try { const buf = fs.readFileSync(path.join(dir, name));
			const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
			console.log = () => {}; doc = await DocxExtractor.Extract(zip); console.log = _l; } catch (e) { console.log = _l; continue; }
		if (!DocxExtractor.LooksLikeWritersTemplate(doc.blocks, norm)) continue;
		const std = doc.blocks.findIndex((b) => DocxExtractor.IsContentStart(b, norm));
		const ptb = doc.blocks.findIndex((b) => b.kind === "para" && isTB(b.text));
		const ttb = doc.blocks.findIndex((b) => b.kind === "table" && (b.rows || []).some(r => r.some(c => isTB(c))));
		console.log([t, code, doc.blocks.length, "std=" + std, "paraTB=" + ptb, "tableTB=" + ttb].join("\t"));
	}
}
})().catch(e => { console.error(e); process.exit(1); });
