"use strict";
// the blocks between the TABLE-CELL title bar and where TrimFrontMatter actually starts: count, kinds, directives, gold overlap
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
for (const t of fs.readdirSync(GOLD)) for (const code of fs.readdirSync(path.join(GOLD, t))) {
	if (!process.argv.slice(2).some(p => code.startsWith(p))) continue;
	const dir = path.join(GOLD, t, code);
	const pages = fs.readdirSync(dir).filter(f => f.endsWith(".html"));
	const g0 = pages.find(f => /_0_0\.html$/.test(f));
	const gtxt = (fs_) => N(fs_.map(f => fs.readFileSync(path.join(dir, f), "utf8").replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, " ").replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")).join(" "));
	const gall = SH(gtxt(pages)), gov = g0 ? SH(gtxt([g0])) : new Set();
	for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
		const buf = fs.readFileSync(path.join(dir, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		console.log = () => {}; const doc = await DocxExtractor.Extract(zip); console.log = _l;
		if (!DocxExtractor.LooksLikeWritersTemplate(doc.blocks, norm)) continue;
		const ttb = doc.blocks.findIndex((b) => b.kind === "table" && (b.rows || []).some(r => r.some(c => isTB(c))));
		const run = new ConversionRun({});
		console.log = () => {}; const kept = DocxExtractor.TrimFrontMatter(doc.blocks, norm, run); console.log = _l;
		const start = doc.blocks.length - kept.length;
		const gap = ttb >= 0 && ttb < start ? doc.blocks.slice(ttb, start) : [];
		const sh = SH(N(gap.map(btext).join(" ")));
		let a = 0, o = 0; for (const x of sh) { if (gall.has(x)) a++; if (gov.has(x)) o++; }
		console.log([code, "blocks=" + doc.blocks.length, "tableTB=" + ttb, "start=" + start, "gap=" + gap.length + "(" + gap.filter(b => b.kind === "table").length + "T)",
			"shingles=" + sh.size, "inGold=" + (sh.size ? (a / sh.size).toFixed(2) : "-"), "inGold0_0=" + (sh.size ? (o / sh.size).toFixed(2) : "-"),
			"startsAt: " + btext(doc.blocks[start] || {}).replace(/\s+/g, " ").slice(0, 70)].join("  "));
	}
}
})().catch(e => { console.error(e); process.exit(1); });
