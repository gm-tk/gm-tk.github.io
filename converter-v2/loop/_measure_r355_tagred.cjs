/** _measure_r354_tagwords.cjs — ROUND 354 PICK measurement: the words riding a built widget's INVOCATION TAG line (its blackAfter and the
 *  words after the bracket on the tag's own line) — are they on the assembled page? For every BUILT bundle (any type) the hook collects every member text run of >= 3 words (a black paragraph,
 *  the words riding a tag's line, every table cell) and, once the module's pages are assembled, checks each run against the
 *  visible text of the page that carries the widget. A run that appears nowhere on the page is LOST. Records per bundle:
 *  type, code, page, index, the number of runs, the lost runs (clipped). Run from reference/tests under WSL, sharded:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r352_widgetloss.cjs --shard K N CODES…
 *      node ../../outputs/_measure_r352_widgetloss.cjs --merge      → _r355_tagred.json
 *  Diagnostic only — never imported by the engine, never writes to the corpus. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(OUT, `_r355_tr_shard${k}.json`);
if (process.argv.includes("--merge")) {
	const all = [];
	for (let k = 0; k < 64; k++) { if (fs.existsSync(SHARD(k))) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8"))); }
	fs.writeFileSync(path.join(OUT, "_r355_tagred.json"), JSON.stringify(all));
	console.log("records ->", path.join(OUT, "_r355_tagred.json"), all.length);
	return;
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const RED = /\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu;
const norm = (s) => String(s ?? "").replace(/&[a-z#0-9]+;/gi, " ").replace(/[^\p{L}\p{N}]+/gu, " ").trim().toLowerCase();
function runs(bundle) {
	const out = [];
	const m0 = (bundle.memberItems ?? [])[0];
	if (!m0 || m0.type !== "tag") return out;
	// the RED runs on the tag line only (the writer's coloured note)
	for (const raw of [m0.text, m0.blackAfter]) for (const m of String(raw ?? "").matchAll(/\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]/g)) {
		const t = norm(m[1].replace(/\[[^\]]*\]/g, " ").replace(/https?:\/\/\S+/g, " "));
		if (t.split(" ").filter(Boolean).length >= 3) out.push(t);
	}
	return [...new Set(out)];
}
function runsOLD(bundle) {
	const out = [];
	const add = (raw) => {
		let t = norm(String(raw ?? "").replace(RED, " ").replace(/\[[^\]]*\]/g, " ").replace(/https?:\/\/\S+/g, " "));
		t = t.replace(/^(?:\d+|[a-z]|[ivx]+)\s+/, "").trim();                        // a list number / letter the renderer drops ("1. why…")
		if (t.split(" ").filter(Boolean).length >= 3) out.push(t);
	};
	for (const m of [...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])]) {
		if (!m) continue;
		if (m.type === "black") add(m.text);
		else if (m.type === "tag") add(m.blackAfter);
		else if (m.type === "table") for (const r of (m.block?.rows ?? [])) for (const c of (r ?? [])) add(c);
	}
	for (const t of (bundle.tables ?? [])) for (const r of (t.rows ?? [])) for (const c of (r ?? [])) add(c);
	return [...new Set(out)];
}
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const normaliser = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const recs = []; let curMod = "?", curPage = "?", errs = 0, lastErr = "";
	let pending = [];
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, n, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle; let out = null;
		try { out = origBuild(args); } catch (e) { out = null; }
		try { if (b && out != null && b.type) pending.push({ type: b.type, code: curMod, page: curPage, index: b.index, runs: runs(b) }); }
		catch (e) { errs++; lastErr = String(e && e.stack || e).slice(0, 300); }
		return out;
	};
	const codes = process.argv.slice(2).filter((a, i, arr) => !a.startsWith("--") && !/^\d+$/.test(a) && arr[i - 1] !== "--shard");
	const si = process.argv.indexOf("--shard"); let k = 0, list = codes;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = codes.filter((_, i) => i % n === k); }
	for (const code of list) {
		curMod = code; pending = [];
		let base; try { base = corpus.mdir(GOLD, code); fs.readdirSync(base); } catch { continue; }
		try {
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
				const buf = fs.readFileSync(path.join(base, name));
				const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
				docs.push({ name, doc: await DocxExtractor.Extract(zip) });
			}
			const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser, istockAcksFiles });
			if (!prep.ok) continue;
			await PageAssembler.AssembleModule(run, normaliser);
			// the visible text of every assembled page (comments and tags stripped)
			const pageText = {};
			for (const o of run.outputs.filter((o) => /\.html$/.test(o.filename))) {
				const html = String(o.content ?? "").replace(/<!--[\s\S]*?-->/g, " ").replace(/<script[\s\S]*?<\/script>/gi, " ");
				const attrs = [...html.matchAll(/(?:alt|title|aria-label|placeholder|data-caption)="([^"]*)"/g)].map((m) => m[1]).join(" ");   // a caption carried as an attribute is not lost
				pageText[o.filename] = norm(html.replace(/<[^>]+>/g, " ") + " " + attrs);
			}
			const allText = Object.values(pageText).join(" | ");
			for (const p of pending) {
				const lost = p.runs.filter((r) => !allText.includes(r));
				recs.push({ type: p.type, code: p.code, page: p.page, index: p.index, runs: p.runs.length, lost: lost.length, lostText: lost.slice(0, 4).map((x) => x.slice(0, 70)) });
			}
		} catch (e) { errs++; lastErr = String(e && e.stack || e).slice(0, 300); }
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "built bundles; errors", errs, lastErr);
}
main().catch((e) => { console.error(e); process.exit(1); });
