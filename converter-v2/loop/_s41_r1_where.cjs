"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const isTB = (s) => [...String(s).matchAll(RED)].some(m => norm.Parse(m[1]).primary?.tag === "title bar");
const N = (s) => String(s).toLowerCase().replace(/🔴|\[\/?red text\]|\[[^\]]{0,40}\]/g, " ").replace(/[‘’“”'"`*_]/g, "").replace(/[^0-9a-zāēīōū]+/g, " ").replace(/\s+/g, " ").trim();
const SH = (s, k = 5) => { const w = s.split(" ").filter(Boolean); const o = new Set(); for (let i = 0; i + k <= w.length; i++) o.add(w.slice(i, i + k).join(" ")); return o; };
const btext = (b) => b.kind === "table" ? (b.rows || []).map(r => r.join(" ")).join(" ") : String(b.text || "");
(async () => {
for (const code of process.argv.slice(2)) {
	let dir; for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) dir = d; }
	const pages = fs.readdirSync(dir).filter(f => f.endsWith(".html"));
	const psh = Object.fromEntries(pages.map(f => [f, SH(N(fs.readFileSync(path.join(dir, f), "utf8").replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, " ").replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")))]));
	const name = fs.readdirSync(dir).find((f) => f.endsWith(".docx") && /writer/i.test(f));
	const buf = fs.readFileSync(path.join(dir, name));
	const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
	console.log = () => {}; const doc = await DocxExtractor.Extract(zip); console.log = _l;
	const ttb = doc.blocks.findIndex((b) => b.kind === "table" && (b.rows || []).some(r => r.some(c => isTB(c))));
	const kept = DocxExtractor.TrimFrontMatter(doc.blocks, norm, null);
	const start = doc.blocks.length - kept.length;
	console.log(`=== ${code} gold pages: ${pages.join(" ")}`);
	for (let i = ttb; i < start; i++) {
		const sh = SH(N(btext(doc.blocks[i])));
		if (!sh.size) { console.log(`  ${i} (no text) ${btext(doc.blocks[i]).replace(/\s+/g," ").slice(0,60)}`); continue; }
		const best = pages.map(f => [f, [...sh].filter(x => psh[f].has(x)).length / sh.size]).sort((a, b) => b[1] - a[1]).slice(0, 2);
		console.log(`  ${i} ${doc.blocks[i].kind} sh=${sh.size} → ${best.map(([f, v]) => f + ":" + v.toFixed(2)).join(" ")} | ${btext(doc.blocks[i]).replace(/🔴\[RED TEXT\]|\[\/RED TEXT\]🔴/g, "").replace(/\s+/g, " ").slice(0, 80)}`);
	}
}
})().catch(e => { console.error(e); process.exit(1); });
