"use strict";
// Session 41 Round 1 — THE OPENER FALLBACK'S TRIM: for every module whose WT has no standard content start, how many
// blocks TrimFrontMatter drops, what they are, and how much of the dropped text the human's gold pages carry.
// node --require ../reference/tests/_deflate_raw_polyfill.cjs _s41_r1_trim.cjs <CODE> …   (under WSL)
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
DataService.Data.AcksFormats.oembed.throttle_ms = 0;
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const N = (s) => String(s).toLowerCase().replace(/🔴|\[\/?red text\]/g, " ").replace(/[‘’“”'"`*_]/g, "").replace(/[^0-9a-zāēīōū]+/g, " ").replace(/\s+/g, " ").trim();
const SH = (s, k = 6) => { const w = s.split(" ").filter(Boolean); const o = new Set(); for (let i = 0; i + k <= w.length; i++) o.add(w.slice(i, i + k).join(" ")); return o; };
const btext = (b) => b.kind === "table" ? (b.rows || []).map(r => r.join(" ")).join(" ") : String(b.text || "");
(async () => {
for (const code of process.argv.slice(2)) {
	let dir; for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) dir = d; }
	const gtext = N(fs.readdirSync(dir).filter(f => f.endsWith(".html")).map(f => fs.readFileSync(path.join(dir, f), "utf8")
		.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, " ").replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ")
		.replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")).join(" "));
	const gsh = SH(gtext);
	for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
		const buf = fs.readFileSync(path.join(dir, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		console.log = () => {}; const doc = await DocxExtractor.Extract(zip); console.log = _l;
		if (!DocxExtractor.LooksLikeWritersTemplate(doc.blocks, norm)) continue;
		const std = doc.blocks.findIndex((b) => DocxExtractor.IsContentStart(b, norm));
		const run = new ConversionRun({});
		console.log = () => {}; const kept = DocxExtractor.TrimFrontMatter(doc.blocks, norm, run); console.log = _l;
		const cut = doc.blocks.length - kept.length;
		const dropped = doc.blocks.slice(0, cut);
		const dsh = SH(N(dropped.map(btext).join(" ")));
		let inGold = 0; for (const x of dsh) if (gsh.has(x)) inGold++;
		console.log(`\n=== ${code} ${name}: blocks ${doc.blocks.length}, standard start ${std}, TRIMMED ${cut} (tables ${dropped.filter(b => b.kind === "table").length}); dropped shingles ${dsh.size}, in gold ${inGold} (${dsh.size ? (inGold / dsh.size).toFixed(2) : "-"})`);
		dropped.slice(0, 6).forEach((b, i) => console.log(`   ${String(i).padStart(3)} ${b.kind.padEnd(5)} | ${btext(b).replace(/\s+/g, " ").slice(0, 140)}`));
		if (cut > 6) console.log(`   … last: ${btext(dropped[cut - 1]).replace(/\s+/g, " ").slice(0, 120)}`);
		console.log(`   first kept: ${btext(kept[0] || {}).replace(/\s+/g, " ").slice(0, 120)}`);
	}
}
})().catch(e => { console.error(e); process.exit(1); });
