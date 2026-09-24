/** _s44_r3_acttables.cjs — session 44 Round 3: every bilingual table whose first content row is an `Activity NX: ║ Ngohe NX:` label
 *  pair (read through bold / red / tags), in the given modules (default: the Bilingual folder, read from the DOCX — the modules with no
 *  parsed WT included): its header, its first 4 rows, its column count, and the NEXT item's kind (marker table / bundle / other).
 *  WSL, from reference/tests: STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s44_r3_acttables.cjs [CODE ...] */
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
const lab = /^(?:activity|ngohe)\s*\d+(?:\.\d+)?\s*[a-z]?\s*:?$/i;
(async () => {
	let codes = process.argv.slice(2);
	if (!codes.length) codes = fs.readdirSync(path.join(GOLD, "Bilingual"));
	const per = {};
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
			if (b.kind !== "table" || !BilingualBuilder.bilingualHeader(b)) return;
			const r1 = (b.rows || [])[1] || [];
			if (!(r1.length >= 2 && lab.test(strip(r1[0]).replace(/\[[^\]]*\]/g, "").trim()) && lab.test(strip(r1[1]).replace(/\[[^\]]*\]/g, "").trim()))) return;
			const nx = items[i + 1] || {};
			const nk = nx.block?.kind === "table" ? (BilingualBuilder.isActivityMarker(nx.block) ? "MARKER" : BilingualBuilder.bilingualHeader(nx.block) ? "BILTABLE" : "TABLE") : String(nx.type);
			const cons = nx.consumedBy !== undefined ? "+consumed" : "";
			per[code] = per[code] || { n: 0, cols: {}, next: {}, row2: {} };
			const p = per[code]; p.n++;
			p.cols[b.rows[0].length] = (p.cols[b.rows[0].length] || 0) + 1;
			p.next[nk + cons] = (p.next[nk + cons] || 0) + 1;
			const r2 = strip((b.rows[2] || []).join(" ║ ")).slice(0, 40);
			const r2k = /^\[\s*h\d/i.test(r2) ? "H" : /english|māori|maori/i.test(r2) ? "HEADER2" : "other";
			p.row2[r2k] = (p.row2[r2k] || 0) + 1;
			const tt = (c) => strip(c).replace(/\[[^\]]*\]/g, "").trim();
			process.stdout.write(`TSV\t${code}\t${tt((b.rows[2] || [])[1])}\t${tt((b.rows[2] || [])[0])}\t${nk}${cons}\n`);
			if (p.n <= 2) _l(`${code} #${i} ${b.rows.length}x${b.rows[0].length} | ${strip(b.rows[0].join(" ║ ")).slice(0, 50)} | ${strip(r1.join(" ║ ")).slice(0, 40)} | r2: ${r2} | next ${nk}${cons}`);
		});
	}
	_l("\nper module: ACT tables, header column counts, row-2 kind, next item");
	for (const [c, p] of Object.entries(per)) _l(`  ${c.padEnd(8)} ${String(p.n).padStart(3)}  cols ${JSON.stringify(p.cols)}  row2 ${JSON.stringify(p.row2)}  next ${JSON.stringify(p.next)}`);
})().catch((e) => { console.error(e); process.exit(1); });
