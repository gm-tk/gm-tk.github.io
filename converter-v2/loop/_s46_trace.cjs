/** _s46_trace.cjs — session 46: WHY does a widget bundle decline? Rewrites every `return null` in InteractiveBuilder.js
 *  (at require time, in memory — the file on disk is never touched) to record its source line, then converts ONE module
 *  and prints, for each bundle of TYPE on pages matching PAGE, the chain of nulls it hit (last = the deciding guard).
 *  Run from reference/tests under WSL:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s46_trace.cjs CODE [PAGE] [TYPE]
 */
"use strict";
const fs = require("fs"), path = require("path"), Module = require("module");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
let TRACE = [];
globalThis.__S46T = (ln, v) => { TRACE.push(v === undefined ? ln : `${ln} «${String(v).slice(0, 120)}»`); return null; };
const _tv = process.env.TRACE_VAR || ""; const TV = _tv ? [_tv.slice(0, _tv.indexOf(":")), _tv.slice(_tv.indexOf(":") + 1)] : [];
const SRC = path.join(eng.APP, "InteractiveBuilder.js");
const srcLines = fs.readFileSync(SRC, "utf8").split("\n");
const origCompile = Module.prototype._compile;
Module.prototype._compile = function (content, filename) {
	if (fs.realpathSync(filename) === fs.realpathSync(SRC)) {
		content = content.split("\n").map((l, i) => l.replace(/\breturn null;/g,
			(TV[0] && Number(TV[0]) === i + 1) ? `return __S46T(${i + 1}, ${TV[1]});` : `return __S46T(${i + 1});`)).join("\n");
		// TRACE_INJECT="LINE:expr" — record expr's value just BEFORE source line LINE runs (diagnostic only)
		const _ti = process.env.TRACE_INJECT || "";
		if (_ti) {
			const ln = Number(_ti.slice(0, _ti.indexOf(":"))), ex = _ti.slice(_ti.indexOf(":") + 1);
			const ls = content.split("\n"); ls[ln - 1] = `__S46T(${ln}, ${ex}); ` + ls[ln - 1]; content = ls.join("\n");
		}
	}
	return origCompile.call(this, content, filename);
};
async function main() {
	const [code, want, type] = process.argv.slice(2);
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	let curPage = "?";
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, n, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		TRACE = [];
		const out = origBuild(args); const b = args?.bundle;
		if (b?.type === (type || "accordion") && (!want || curPage === want || curPage.includes(want))) {
			_l(`=== ${code} page ${curPage} #${b.index} built=${out != null}`);
			const seen = TRACE.slice(-(Number(process.env.TRACE_N) || 4));
			for (const ln of seen) _l(`   ${String(ln).padStart(6)}  ${srcLines[parseInt(ln, 10) - 1].trim().slice(0, 110)}`);
			if (out) _l("   OUT " + String(out).replace(/\s+/g, " ").slice(0, 700));
		}
		return out;
	};
	const base = corpus.mdir(GOLD, code);
	const run = new ConversionRun({ imageMode: "P" }); const docs = [];
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
		const buf = fs.readFileSync(path.join(base, name));
		docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
	}
	const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
	const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
	if (!prep.ok) { _l("prep failed"); return; }
	await PageAssembler.AssembleModule(run, norm);
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
