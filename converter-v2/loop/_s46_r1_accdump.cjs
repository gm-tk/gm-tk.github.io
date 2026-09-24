/** _s46_r1_accdump.cjs — session 46 Round 1 (the accordion vocabulary batch, WHY_UNBUILT__accordion items 1–6):
 *  every accordion bundle the builder DECLINES (Build → null → the hand-off box) on the current engine, with its
 *  opener / member items and captured table rows, so each can be classified by authoring shape. Diagnostic only.
 *  Run from reference/tests under WSL, sharded:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s46_r1_accdump.cjs --shard K N [--type accordion] [--out NAME]
 *      node ../../outputs/_s46_r1_accdump.cjs --merge N [--out NAME]
 */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const NAME = arg("--out", "_s46_r1_accdump");
const TYPE = arg("--type", "accordion");
const SHARD = (k) => path.join(OUT, `${NAME}_shard${k}.json`);
const clip = (s, n) => String(s ?? "").slice(0, n);

if (process.argv.includes("--merge")) {
	const n = parseInt(arg("--merge", "8"), 10);
	const all = [];
	for (let k = 0; k < n; k++) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8")));
	fs.writeFileSync(path.join(OUT, `${NAME}.json`), JSON.stringify(all));
	const dec = all.filter((r) => !r.built);
	console.log(`${all.length} ${TYPE} bundles, ${dec.length} declined, ${new Set(dec.map((r) => r.code)).size} modules`);
	process.exit(0);
}

const eng = require(path.join(TESTS, "_engine_load.cjs"));
function moduleDirs() {
	const out = [];
	for (const tmpl of fs.readdirSync(GOLD)) {
		const tp = path.join(GOLD, tmpl);
		if (!fs.statSync(tp).isDirectory()) continue;
		for (const code of fs.readdirSync(tp)) { const cp = path.join(tp, code); if (fs.statSync(cp).isDirectory()) out.push({ code, dir: cp, tmpl }); }
	}
	return out.sort((a, b) => a.code.localeCompare(b.code));
}
function item(m) {
	if (!m) return null;
	if (m.type === "table") return { k: "table", rows: (m.block?.rows ?? []).slice(0, 12).map((r) => (r ?? []).map((c) => clip(typeof c === "string" ? c : c?.text, 400))) };
	if (m.type === "nested") return { k: "nested", t: m.bundle?.type ?? m.type };
	if (m.type === "black") return { k: "black", text: clip(m.text, 600) };
	return { k: m.type, tag: m.parse?.primary?.tag ?? null, cls: m.parse?.class ?? null, text: clip(m.text, 300), after: clip(m.blackAfter, 400) };
}
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const recs = [];
	let curMod = "?", curPage = "?";
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, n, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		let out = null;
		try { out = origBuild(args); } catch (e) { out = null; }
		const b = args?.bundle;
		if (b?.type === TYPE) {
			recs.push({ code: curMod, page: curPage, index: b.index, built: out != null,
				opener: (b.openerItems ?? []).map(item), members: out != null ? [] : (b.memberItems ?? []).map(item),
				extraTypes: b.extraTypes ?? [], variant: b.variant ?? null });
		}
		return out;
	};
	const dirs = moduleDirs();
	const si = process.argv.indexOf("--shard");
	let list = dirs, k = 0;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = dirs.filter((_, i) => i % n === k); }
	for (const d of list) {
		curMod = d.code;
		try {
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(d.dir).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
				const buf = fs.readFileSync(path.join(d.dir, name));
				docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
			}
			const istockAcksFiles = fs.readdirSync(d.dir).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(d.dir, f), "utf8") }));
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
			if (!prep.ok) continue;
			await PageAssembler.AssembleModule(run, norm);
		} catch (e) { /* keep scanning */ }
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "records");
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
