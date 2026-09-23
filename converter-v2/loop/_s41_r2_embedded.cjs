"use strict";
// Session 41 Round 2 PICK — the MTK "[Activity: Embedded] <type>" tables: per Bilingual WT, each one's type text, whether it is its own
// table (first row = the tag alone) or a row inside a bigger table, what precedes it (an "Activity NX:" label table? an [H1] N.M
// keystone section?), and how many data tables follow before the next label / embedded / paragraph tag. Then the gold's
// div.activity.interactive count per module. node --require ../reference/tests/_deflate_raw_polyfill.cjs _s41_r2_embedded.cjs
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_", "Bilingual");
const CL = path.join(__dirname, "..", "..", "01-Claude_Modules_", "Bilingual");
const strip = (s) => String(s ?? "").replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "").replace(/\s+/g, " ").trim();
const EMB = /^\[\s*activity\s*:\s*embedded\s*\]/i;
const LABEL = /^\**\s*(activity|ngohe)\s*\d+\s*[a-z.]*\d*\s*\**\s*:?\s*\**$/i;
(async () => {
const tot = { emb: 0, own: 0, row: 0, afterLabel: 0, gold: 0, claudeBox: 0 };
for (const code of fs.readdirSync(GOLD).sort()) {
	const dir = path.join(GOLD, code);
	const name = fs.readdirSync(dir).find((f) => f.endsWith(".docx") && /writer/i.test(f));
	if (!name) continue;
	const buf = fs.readFileSync(path.join(dir, name));
	const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
	console.log = () => {}; const doc = await DocxExtractor.Extract(zip); console.log = _l;
	const B = doc.blocks;
	let emb = 0, own = 0, inrow = 0, afterLabel = 0; const types = [];
	let lastLabel = -99;
	B.forEach((b, i) => {
		if (b.kind !== "table") return;
		const rows = b.rows || [];
		rows.forEach((r, k) => {
			const c0 = strip(r[0]);
			if (LABEL.test(c0.replace(/\*/g, ""))) lastLabel = i;
			if (EMB.test(c0)) {
				emb++; types.push(c0.replace(EMB, "").trim().slice(0, 22));
				if (k === 0) own++; else inrow++;
				if (lastLabel >= i - 1) afterLabel++;
			}
		});
	});
	const gfiles = fs.readdirSync(dir).filter(f => f.endsWith(".html"));
	const gAct = gfiles.reduce((n, f) => n + (fs.readFileSync(path.join(dir, f), "utf8").match(/class="activity interactive"|class="interactive activity"/g) || []).length, 0);
	const cdir = path.join(CL, code);
	const cBox = fs.existsSync(cdir) ? fs.readdirSync(cdir).filter(f => f.endsWith(".html")).reduce((n, f) => n + (fs.readFileSync(path.join(cdir, f), "utf8").match(/class="cv2-interactive bilingual-unbuilt"/g) || []).length, 0) : 0;
	tot.emb += emb; tot.own += own; tot.row += inrow; tot.afterLabel += afterLabel; tot.gold += gAct; tot.claudeBox += cBox;
	console.log(`${code.padEnd(8)} embedded ${String(emb).padStart(3)} (own table ${own}, row ${inrow}, right after an Activity-NX label ${afterLabel}) | gold activity.interactive ${gAct} | Claude bilingual-unbuilt boxes ${cBox} | ${[...new Set(types)].slice(0, 5).join("; ")}`);
}
console.log("TOTAL", JSON.stringify(tot));
})().catch(e => { console.error(e); process.exit(1); });
