/** _s44_r3_embrows.cjs — session 44 Round 3: every `[Activity: Embedded]` marker table in the given modules (default: the Bilingual
 *  folder), row by row — the cell count, which cells carry text, and a clip of each — so the widget-DATA rows (the ones bilingualActivity
 *  unfolds into loose paragraphs) can be told from the instruction rows. Summary: rows by shape across every marker table.
 *  WSL, from reference/tests: STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s44_r3_embrows.cjs [--quiet] [CODE ...] */
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
	const args = process.argv.slice(2); const quiet = args.includes("--quiet");
	let codes = args.filter((a) => !a.startsWith("--"));
	if (!codes.length) codes = fs.readdirSync(path.join(GOLD, "Bilingual"));
	const shape = {}; let tables = 0;
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
		try { ModuleResolver.PrepareRun({ docs, run, normaliser: norm }); } catch (e) { console.log = _l; continue; }
		const items = PageSplitter.BuildItemStream(run.wtBlocks, norm);
		console.log = _l;
		items.forEach((it, i) => {
			const b = it.block || {};
			if (b.kind !== "table" || !BilingualBuilder.isActivityMarker(b)) return;
			tables++;
			if (!quiet) _l(`${code} #${i} marker table ${b.rows.length} rows`);
			b.rows.forEach((r, k) => {
				const cells = (r || []).map(strip);
				const filled = cells.map((c) => (c ? 1 : 0)).join("");
				const lead = /\[\s*activity\s*:?\s*embedded/i.test(cells.join(" ")) ? "MARKER" : /^\[?\s*h\d\s*\]?/i.test(cells[0] || cells[1] || "") ? "HEAD" : /^\[?\s*body/i.test(cells[0] || cells[1] || "") ? "BODY" : "OTHER";
				const key = `${cells.length}c:${filled}:${lead}`;
				shape[key] = (shape[key] || 0) + 1;
				if (!quiet) _l(`   r${k} ${key.padEnd(18)} ${cells.map((c) => c.slice(0, 55)).join(" ║ ")}`);
			});
		});
	}
	_l(`marker tables: ${tables}`);
	for (const [k, v] of Object.entries(shape).sort((a, b) => b[1] - a[1])) _l(`  ${k.padEnd(20)} ${v}`);
})().catch((e) => { console.error(e); process.exit(1); });
