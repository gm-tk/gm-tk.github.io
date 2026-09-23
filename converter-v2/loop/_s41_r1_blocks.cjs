"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const btext = (b) => b.kind === "table" ? "T" + (b.rows||[]).length + "x" + ((b.rows||[])[0]||[]).length + " " + (b.rows || []).map(r => r.join(" ║ ")).join(" ┃ ") : String(b.text || "");
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
(async () => {
const code = process.argv[2], a = +(process.argv[3]||0), z = +(process.argv[4]||40);
let dir; for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) dir = d; }
for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx") && /writer/i.test(f))) {
	const buf = fs.readFileSync(path.join(dir, name));
	const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
	console.log = () => {}; const doc = await DocxExtractor.Extract(zip); console.log = _l;
	doc.blocks.slice(a, z).forEach((b, i) => {
		const dirs = [...btext(b).matchAll(RED)].map(m => norm.Parse(m[1]).primary).filter(Boolean).map(p => (p.directive||"-") + "/" + (p.tag||"-")).slice(0, 4).join(",");
		console.log(String(a + i).padStart(4), b.kind.padEnd(5), dirs.padEnd(40).slice(0, 40), "|", btext(b).replace(/\s+/g, " ").slice(0, 120));
	});
}
})().catch(e => { console.error(e); process.exit(1); });
