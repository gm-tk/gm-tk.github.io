/** _s46_whynull.cjs — session 46: corpus-wide, WHY does each declined bundle of TYPE decline? Rewrites InteractiveBuilder.js's
 *  `return null;` at the source lines named in WHY_LINES (in memory — the file on disk is untouched) to record the value of an
 *  expression evaluated there, then converts every module (sharded) and writes, per declined bundle, the values captured.
 *  Run from reference/tests under WSL (through _s46_shardrun.sh):
 *      WHY_TYPE=accordion WHY_LINES='2843:tag + " | " + String(m.text).slice(0,80)' bash ../../outputs/_s46_shardrun.sh _s46_whynull.cjs 8
 *      node ../../outputs/_s46_whynull.cjs --merge 8
 *  WHY_LINES: one or more `LINE:expr` joined by ` ;; `. Diagnostic only. */
"use strict";
const fs = require("fs"), path = require("path"), Module = require("module");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const NAME = process.env.WHY_OUT || "_s46_whynull";
const SHARD = (k) => path.join(OUT, `${NAME}_shard${k}.json`);
if (process.argv.includes("--merge")) {
	const n = parseInt(arg("--merge", "8"), 10); const all = [];
	for (let k = 0; k < n; k++) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8")));
	fs.writeFileSync(path.join(OUT, `${NAME}.json`), JSON.stringify(all));
	console.log(`${all.length} declined bundles`); process.exit(0);
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
let HITS = [];
globalThis.__S46W = (ln, v) => { try { HITS.push([ln, String(v)]); } catch (e) { HITS.push([ln, "?"]); } return null; };
const WL = (process.env.WHY_LINES || "").split(" ;; ").filter(Boolean).map((s) => [Number(s.slice(0, s.indexOf(":"))), s.slice(s.indexOf(":") + 1)]);
const SRC = path.join(eng.APP, "InteractiveBuilder.js");
const origCompile = Module.prototype._compile;
Module.prototype._compile = function (content, filename) {
	if (fs.realpathSync(filename) === fs.realpathSync(SRC)) {
		const ls = content.split("\n");
		for (const [ln, ex] of WL) ls[ln - 1] = ls[ln - 1].replace(/\breturn null;/, `return __S46W(${ln}, (() => { try { return ${ex}; } catch (e) { return "ERR"; } })());`);
		// WHY_INJECT="LINE:expr ;; …" — record expr just BEFORE line LINE runs (for a decline that is not a literal `return null;`)
		for (const s of (process.env.WHY_INJECT || "").split(" ;; ").filter(Boolean)) {
			const ln = Number(s.slice(0, s.indexOf(":"))), ex = s.slice(s.indexOf(":") + 1);
			ls[ln - 1] = `__S46W(${ln}, (() => { try { return ${ex}; } catch (e) { return "ERR"; } })()); ` + ls[ln - 1];
		}
		content = ls.join("\n");
	}
	return origCompile.call(this, content, filename);
};
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
	const TYPE = process.env.WHY_TYPE || "accordion";
	const recs = []; let curMod = "?", curPage = "?";
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, n, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		HITS = []; let out = null;
		try { out = origBuild(args); } catch (e) { out = null; }
		const b = args?.bundle;
		if (b?.type === TYPE && out == null) recs.push({ code: curMod, page: curPage, index: b.index, hits: HITS.slice(-6) });
		return out;
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
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "declined");
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
