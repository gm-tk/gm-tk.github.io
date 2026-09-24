/** _s43_flipdump.cjs — session 43 Round 1 debug: for the named modules, print every flipCard bundle's captured table
 *  rows (raw JSON) and the built html. Run from reference/tests under WSL:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s43_flipdump.cjs CODE [PAGE]
 *  Diagnostic only. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const normaliser = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const [code, want] = process.argv.slice(2);
	let curPage = "?";
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, n, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const out = origBuild(args); const b = args?.bundle;
		if (b?.type === "flipCard" && (!want || curPage.includes(want))) {
			_l(`=== ${code} page ${curPage} #${b.index} tables ${(b.tables ?? []).length}`);
			for (const t of (b.tables ?? [])) for (const r of (t.rows ?? [])) _l("  ROW " + JSON.stringify(r).slice(0, 900));
			_l("  OUT " + String(out ?? "null").replace(/\s+/g, " ").slice(0, 1500));
		}
		return out;
	};
	const base = corpus.mdir(GOLD, code);
	const run = new ConversionRun({ imageMode: "P" }); const docs = [];
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
		const buf = fs.readFileSync(path.join(base, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		docs.push({ name, doc: await DocxExtractor.Extract(zip) });
	}
	const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
	const prep = ModuleResolver.PrepareRun({ docs, run, normaliser, istockAcksFiles });
	if (!prep.ok) { _l("prep failed"); return; }
	await PageAssembler.AssembleModule(run, normaliser);
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
