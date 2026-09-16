/** _measure_r350_ddcolumn.cjs — ROUND 350 PICK measurement (the D10-3 dragAndDrop kickoff, shape family 1: the 3+-column table).
 *  The r286 hook (InteractiveBuilder.Build intercepted, no disk writes) — for every dragAndDrop bundle with tables, dumps the
 *  table(s): width, row count, each row's cells (cleaned, clipped), whether a cell carries red writer text, and whether the
 *  builder built it. Run from reference/tests under WSL, sharded:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r350_ddcolumn.cjs --shard K 4 [CODES…]
 *      node ../../outputs/_measure_r350_ddcolumn.cjs --merge      → _r350_ddcolumn.json
 *  Diagnostic only — never imported by the engine, never writes to the corpus. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(OUT, `_r350_dd_shard${k}.json`);
const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
if (process.argv.includes("--merge")) {
	const all = [];
	for (let k = 0; k < 64; k++) { if (fs.existsSync(SHARD(k))) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8"))); }
	fs.writeFileSync(path.join(OUT, "_r350_ddcolumn.json"), JSON.stringify(all));
	console.log("records ->", path.join(OUT, "_r350_ddcolumn.json"), all.length);
	return;
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const RED_OPEN = /\u{1f534}\[RED TEXT\]/gu, RED_CLOSE = /\[\/RED TEXT\]\u{1f534}/gu;
function cellInfo(cell) {
	// a cell is a plain STRING carrying the writer's markers (the builder reads it with #cellText / #hasRedText)
	const raw = String(cell ?? "");
	const red = /\[RED TEXT\]/.test(raw);
	const redRuns = [...raw.matchAll(/\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]/g)].map((m) => clean(m[1]).slice(0, 40));
	const text = clean(raw.replace(RED_OPEN, "").replace(RED_CLOSE, ""));
	return { t: text.slice(0, 80), red, redRuns, url: /https?:\/\//.test(raw), slashItems: text ? (text.split(" / ").length) : 0 };
}
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console), _e = console.error.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const recs = []; let curMod = "?", curPage = "?", seen = 0, errs = 0, lastErr = "";
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, normaliser, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle; let out = null;
		try { out = origBuild(args); } catch (e) { out = null; }
		try {
			seen++;
			if (b?.type === "dragAndDrop") {
				const tables = (b.tables ?? []).map((t) => (t.rows ?? []).map((r) => (r ?? []).map(cellInfo)));
				recs.push({ code: curMod, page: curPage, index: b.index, built: out != null, extraTypes: (b.extraTypes ?? []).length, media: (b.media ?? []).length,
					nTables: tables.length, width: tables.length ? Math.max(0, ...tables[0].map((r) => r.length)) : 0, tables: tables.slice(0, 3) });
			}
		} catch (e) { errs++; lastErr = String(e && e.stack || e).slice(0, 300); }
		return out;
	};
	const codes = process.argv.slice(2).filter((a, i, arr) => !a.startsWith("--") && !/^\d+$/.test(a) && arr[i - 1] !== "--shard");
	const si = process.argv.indexOf("--shard"); let k = 0, list = codes;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = codes.filter((_, i) => i % n === k); }
	for (const code of list) {
		curMod = code;
		let base; try { base = corpus.mdir(GOLD, code); fs.readdirSync(base); } catch { continue; }
		try {
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
				const buf = fs.readFileSync(path.join(base, name));
				const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
				docs.push({ name, doc: await DocxExtractor.Extract(zip) });
			}
			const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
			if (!prep.ok) continue;
			await PageAssembler.AssembleModule(run, norm);
		} catch (e) { errs++; lastErr = String(e && e.stack || e).slice(0, 300); }
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "dragAndDrop bundles of", seen, "builds; errors", errs, lastErr);
}
main().catch((e) => { console.error(e); process.exit(1); });
