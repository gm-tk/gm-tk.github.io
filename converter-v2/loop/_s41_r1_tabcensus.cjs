"use strict";
// TRR overview tables (table-cell title bar → first page boundary): per table its [H1]/[H2] rows (English); vs the gold 0.0's nav labels + pane classes
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok:false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const strip = (s) => String(s ?? "").replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "");
const lead = (s) => { let t = strip(s).trim(); const tags = []; let m; while ((m = t.match(/^\[([^\]]*)\]\s*/))) { tags.push(m[1].trim().toLowerCase()); t = t.slice(m[0].length); } return { tags, text: t.replace(/\*/g, "").replace(/\s+/g, " ").trim() }; };
(async () => {
for (const code of process.argv.slice(2)) {
	const dir = path.join(GOLD, "Bilingual", code);
	const name = fs.readdirSync(dir).find((f) => f.endsWith(".docx") && /writer/i.test(f));
	const buf = fs.readFileSync(path.join(dir, name));
	const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
	console.log = () => {}; const doc = await DocxExtractor.Extract(zip); console.log = _l;
	const B = doc.blocks;
	const ttb = B.findIndex((b) => b.kind === "table" && b.rows.some(r => r.some(c => [...String(c).matchAll(RED)].some(m => norm.Parse(m[1]).primary?.tag === "title bar"))));
	const out = [];
	for (let i = ttb; i >= 0 && i < B.length; i++) {
		const b = B[i];
		if (b.kind !== "table") {
			const t = strip(b.text).trim();
			if (!t) continue;
			out.push(`P:${t.slice(0, 40)}`);
			if (/\[\s*(end page|end of page|lesson|module content|end of drop)/i.test(t)) break;
			continue;
		}
		const hs = b.rows.map(r => lead(r[0] || "")).filter(x => x.tags.some(t => /^(h\d|title bar)$/.test(t))).map(x => `${x.tags.find(t => /^(h\d|title bar)$/.test(t))}:${x.text.slice(0, 26)}`);
		out.push(`T[${hs.join(" · ")}]`);
	}
	const gf = fs.readdirSync(dir).find(f => /_0[._]0/.test(f) && f.endsWith(".html"));
	const g = fs.readFileSync(path.join(dir, gf), "utf8");
	const menu = (g.split('id="module-menu-content"')[1] || "").split('id="body"')[0];
	const labels = [...menu.matchAll(/<li><a>([\s\S]*?)<\/a><\/li>/g)].map(m => (m[1].match(/<span eng>([^<]*)/) || [, m[1].replace(/<[^>]+>/g, "")])[1]);
	const panes = menu.split('class="tab-pane').slice(1).map(p => { const cols = [...p.matchAll(/<div class="(col-[^"]*)"/g)].map(m => m[1].replace("col-md-", "").replace(" col-12", "").replace("offset-md-0 ", "")); const hs = [...p.matchAll(/<(h\d)[^>]*\beng\b[^>]*>(?:<span>|<b>)*([^<]{0,22})/g)].map(m => m[1] + ":" + m[2]); return `(${cols.join("|")}) ${hs.slice(0, 6).join(" · ")}`; });
	console.log(`\n=== ${code}\n  WT: ${out.join("\n      ")}\n  GOLD tabs: ${labels.join(" | ")}`);
	panes.forEach((p, k) => console.log(`   pane${k + 1}: ${p}`));
}
})().catch(e => { console.error(e); process.exit(1); });
