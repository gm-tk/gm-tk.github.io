/** _s46_items.cjs — session 46: dump the page items (pre-scan) around a text match. Run from reference/tests under WSL:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s46_items.cjs CODE "needle" [radius] */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
async function main() {
	const [code, needle, rad] = process.argv.slice(2); const R = Number(rad || 3);
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) {
		const items = page.items ?? [];
		items.forEach((it, k) => {
			const t = String(it.text ?? "") + String(it.blackAfter ?? "");
			if (!t.includes(needle)) return;
			for (let j = Math.max(0, k - R); j <= Math.min(items.length - 1, k + R); j++) {
				const x = items[j];
				_l(`${j === k ? ">>" : "  "} #${j} ${x.type} cls=${x.parse?.class ?? "-"} tag=${x.parse?.primary?.tag ?? "-"} blk=${x.block === it.block ? "same" : "diff"} text=${JSON.stringify(String(x.text ?? "").slice(0, 120))} after=${JSON.stringify(String(x.blackAfter ?? "").slice(0, 80))}`);
			}
			_l("---");
		});
		return origScan(page, n, run);
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
