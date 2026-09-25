/** _s46_trace_cc.cjs — session 46: which `return null` inside ContentConverter.js lines FROM..TO fires, per page, for one module (the
 *  file is rewritten in memory only). Run from reference/tests under WSL:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s46_trace_cc.cjs CODE FROM TO [LINE:expr] */
"use strict";
const fs = require("fs"), path = require("path"), Module = require("module");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const [code, FROM, TO, VAR] = process.argv.slice(2);
const HITS = []; let curPage = "?";
globalThis.__S46C = (ln, v) => { HITS.push(`${curPage} L${ln}${v !== undefined ? " «" + String(v).slice(0, 140) + "»" : ""}`); return null; };
const SRC = path.join(eng.APP, "ContentConverter.js");
const origCompile = Module.prototype._compile;
Module.prototype._compile = function (content, filename) {
	if (fs.realpathSync(filename) === fs.realpathSync(SRC)) {
		const vl = VAR ? Number(VAR.slice(0, VAR.indexOf(":"))) : -1, vx = VAR ? VAR.slice(VAR.indexOf(":") + 1) : "";
		content = content.split("\n").map((l, i) => (i + 1 >= Number(FROM) && i + 1 <= Number(TO))
			? l.replace(/\breturn null;/g, i + 1 === vl ? `return __S46C(${i + 1}, (() => { try { return ${vx}; } catch (e) { return "ERR"; } })());` : `return __S46C(${i + 1});`) : l).join("\n");
	}
	return origCompile.call(this, content, filename);
};
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, n, run); };
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
	for (const h of HITS) _l(h);
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
