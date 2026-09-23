"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
(async () => {
const code = process.argv[2], a = +process.argv[3], z = +process.argv[4];
let dir; for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) dir = d; }
const name = fs.readdirSync(dir).find((f) => f.endsWith(".docx") && /writer/i.test(f));
const buf = fs.readFileSync(path.join(dir, name));
const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
console.log = () => {}; const doc = await DocxExtractor.Extract(zip); console.log = _l;
for (let i = a; i <= z; i++) {
	const b = doc.blocks[i];
	if (b.kind !== "table") { console.log(`${i} PARA | ${String(b.text).replace(/🔴\[RED TEXT\]|\[\/RED TEXT\]🔴/g, "").slice(0, 120)}`); continue; }
	console.log(`${i} TABLE ${b.rows.length} rows`);
	b.rows.forEach((r, k) => console.log(`   r${k}: ` + r.map(c => String(c).replace(/🔴\[RED TEXT\]|\[\/RED TEXT\]🔴/g, "").replace(/\s+/g, " ").slice(0, 70)).join("  ║  ")));
}
})().catch(e => { console.error(e); process.exit(1); });
