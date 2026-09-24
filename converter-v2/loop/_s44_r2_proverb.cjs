/** _s44_r2_proverb.cjs — session 44 Round 2: every Writers Template TABLE (all modules given, default the Bilingual folder) whose
 *  first content rows name a PROVERB / WHAKATAUKĪ heading, with its shape (columns, rows, the heading cells, the tag on the heading
 *  row), and whether a [Whakatauki] callout tag is present anywhere in it. WSL, from reference/tests:
 *  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s44_r2_proverb.cjs [CODE ...] */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
DataService.Data.AcksFormats.oembed.throttle_ms = 0;
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine(); console.log = _l;
globalThis.norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const strip = (s) => String(s ?? "").replace(/🔴|\[\/?RED TEXT\]/g, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
(async () => {
	let codes = process.argv.slice(2);
	if (!codes.length) codes = fs.readdirSync(path.join(GOLD, "Bilingual"));
	for (const code of codes) {
		let dir; for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) dir = d; }
		if (!dir) continue;
		const run = new ConversionRun({ imageMode: "P", interactiveMode: "extract" });
		const docs = [];
		for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(dir, name));
			const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
			console.log = () => {}; docs.push({ name, doc: await DocxExtractor.Extract(zip) }); console.log = _l;
		}
		console.log = () => {};
		try { ModuleResolver.PrepareRun({ docs, run, normaliser: norm }); } catch (e) { console.log = _l; _l(code, "PREPARE FAIL", e.message); continue; }
		const items = PageSplitter.BuildItemStream(run.wtBlocks, norm);
		console.log = _l;
		let hits = 0;
		items.forEach((it, i) => {
			const b = it.block || {};
			if (b.kind !== "table") {
				const t = strip(it.text || b.text || "");
				if (/\bwhakatauk|\bproverb\b/i.test(t) && t.length < 160) _l(`${code} #${i} ${it.type} ${String(it.parse?.primary?.tag || "")} | ${t.slice(0, 130)}`);
				return;
			}
			const rows = b.rows || [];
			const head = rows.slice(0, 3).map((r) => (r || []).map(strip).join(" ║ ")).join(" ┃ ");
			if (!/\bwhakatauk|\bproverb\b/i.test(head)) return;
			hits++;
			_l(`${code} #${i} TABLE ${rows.length}x${rows[0]?.length} | ${head.slice(0, 230)}`);
			for (const r of rows.slice(0, 5)) _l("     row: " + (r || []).map((c) => strip(c).slice(0, 60)).join(" ║ "));
		});
		if (!hits) _l(`${code} — no proverb table`);
	}
})().catch((e) => { console.error(e); process.exit(1); });
