/** _measure_r357_mcq.cjs — session 17 PICK measurement: EVERY multiChoiceQuiz bundle (built or not) dumped with the evidence the r309
 *  answer-mark channel carries — the opener wording (an ANNOUNCEMENT: "correct answers highlighted / in green / in red / in bold"?),
 *  every member's text, red-ness, block.marks (hl / green) and, for a table member, its rows with cellMarks — so the shapes of the
 *  413 un-built MCQs can be classified offline (_measure_r357_mcq.py). The r286 hook (InteractiveBuilder.Build intercepted, no disk
 *  writes). Run from reference/tests under WSL, sharded:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r357_mcq.cjs --shard K 8 CODES…
 *      node ../../outputs/_measure_r357_mcq.cjs --merge      → _r357_mcq.json
 *  Diagnostic only — never imported by the engine, never writes to the corpus. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(OUT, `_r357_mcq_shard${k}.json`);
const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
if (process.argv.includes("--merge")) {
	const all = [];
	for (let k = 0; k < 64; k++) { if (fs.existsSync(SHARD(k))) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8"))); }
	fs.writeFileSync(path.join(OUT, "_r357_mcq.json"), JSON.stringify(all));
	console.log("records ->", path.join(OUT, "_r357_mcq.json"), all.length);
	return;
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const marksOf = (blk) => (blk?.marks ?? []).map((m) => ({ k: m.kind, t: clean(m.text).slice(0, 60) }));
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
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
			if (b?.type === "multiChoiceQuiz") {
				const mem = (it) => {
					const raw = String(it?.text ?? "");
					const o = { k: it?.type ?? "?", tag: it?.tag ?? it?.parse?.primary?.tag ?? null, cls: it?.parse?.class ?? null,
						t: clean(raw.replace(/\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, " ")).slice(0, 110), red: /\[RED TEXT\]/.test(raw),
						after: clean(it?.blackAfter ?? "").slice(0, 110), marks: marksOf(it?.block), list: it?.block?.list ?? null };
					if (it?.type === "table" || it?.block?.kind === "table") {
						const blk = it.block ?? it;
						o.rows = (blk.rows ?? []).slice(0, 20).map((r, ri) => (r ?? []).map((c, ci) => ({
							t: clean(String(c ?? "").replace(/\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, " ")).slice(0, 70), red: /\[RED TEXT\]/.test(String(c ?? "")),
							marks: (blk.cellMarks?.[ri]?.[ci] ?? []).map((m) => ({ k: m.kind, t: clean(m.text).slice(0, 50) })) })));
					}
					return o;
				};
				recs.push({ code: curMod, page: curPage, index: b.index, built: out != null, extraTypes: (b.extraTypes ?? []).map(String),
					nTables: (b.tables ?? []).length, instr: (b.instructions ?? []).map((s) => clean(s).slice(0, 110)),
					openers: (b.openerItems ?? []).map(mem), members: (b.memberItems ?? []).slice(0, 80).map(mem),
					tables: (b.tables ?? []).slice(0, 4).map((t) => ({ rows: (t.rows ?? []).slice(0, 24).map((r, ri) => (r ?? []).map((c, ci) => ({
						t: clean(String(c ?? "").replace(/\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, " ")).slice(0, 70), red: /\[RED TEXT\]/.test(String(c ?? "")),
						marks: (t.cellMarks?.[ri]?.[ci] ?? []).map((m) => ({ k: m.kind, t: clean(m.text).slice(0, 50) })) }))) })) });
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
	_l("shard", k, "->", list.length, "modules,", recs.length, "mcq bundles of", seen, "builds; errors", errs, lastErr);
}
main().catch((e) => { console.error(e); process.exit(1); });
