/** _s46_r2_scanend_all.cjs — session 46 Round 2: corpus-wide, every bundle the scanner closes on a [Body] / heading while it already
 *  holds a table (the member_rule.body_terminates_after_table section break), with its LAST captured member — the class where the
 *  last member is the widget's own panel / pane / item DELIMITER (the writer opened a new panel after the table and the [Body] is its
 *  content). Sharded (run through _s46_shardrun.sh), --merge N writes _s46_r2_scanend.json. Diagnostic only. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const NAME = "_s46_r2_scanend"; const SHARD = (k) => path.join(OUT, `${NAME}_shard${k}.json`);
if (process.argv.includes("--merge")) {
	const n = parseInt(arg("--merge", "8"), 10); const all = [];
	for (let k = 0; k < n; k++) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8")));
	fs.writeFileSync(path.join(OUT, `${NAME}.json`), JSON.stringify(all)); console.log(`${all.length} records`); process.exit(0);
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const tagOf = (it) => it?.type === "tag" ? (it.parse?.primary?.tag ?? `(${it.parse?.class ?? "?"})`) : it?.type ?? "(end)";
function moduleDirs() {
	const out = [];
	for (const tmpl of fs.readdirSync(GOLD)) {
		const tp = path.join(GOLD, tmpl); if (!fs.statSync(tp).isDirectory()) continue;
		for (const code of fs.readdirSync(tp)) { const cp = path.join(tp, code); if (fs.statSync(cp).isDirectory()) out.push({ code, dir: cp }); }
	}
	return out.sort((a, b) => a.code.localeCompare(b.code));
}
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const recs = []; let curMod = "?";
	const built = new Map();
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) { const out = origBuild(args); if (args?.bundle) built.set(args.bundle, out != null); return out; };
	const pending = [];
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) {
		const res = origScan(page, n, run);
		const label = String(page?.lessonLabel ?? page?.label ?? "?");
		const bundles = Array.isArray(res) ? res : (res?.bundles ?? []);
		for (const b of bundles) {
			if (!b || !(b.tables ?? []).length) continue;
			const term = page.items[b.endIndex];
			const tt = tagOf(term);
			if (!(tt === "body" || /^h[2-5]$/.test(tt))) continue;
			const mem = b.memberItems ?? [];
			const last = mem[mem.length - 1];
			const lastTableIdx = mem.map((m) => m?.type).lastIndexOf("table");
			pending.push({ b, rec: { code: curMod, page: label, type: b.type, term: tt, termText: String(term?.blackAfter ?? term?.text ?? "").slice(0, 60),
				last: tagOf(last), lastText: String(last?.text ?? "").replace(/\s+/g, " ").slice(0, 50) + " " + String(last?.blackAfter ?? "").slice(0, 40),
				membersAfterTable: mem.length - 1 - lastTableIdx } });
		}
		return res;
	};
	const dirs = moduleDirs(); const si = process.argv.indexOf("--shard");
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
		for (const p of pending.splice(0)) recs.push({ ...p.rec, built: built.get(p.b) ?? null });
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "records");
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
