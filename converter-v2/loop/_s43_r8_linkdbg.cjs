/** _s43_r8_linkdbg.cjs — session 43 Round 8 debug: convert one module and print every ListsAndRuns.inlineMarkup / renderBlackText
 *  call whose text contains the given phrase, with the links it received and a short stack (which emitter called it).
 *  WSL, from reference/tests: STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s43_r8_linkdbg.cjs CODE "phrase" */
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
	const [code, phrase] = process.argv.slice(2);
	const normaliser = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	for (const fn of ["inlineMarkup", "renderBlackText"]) {
		const orig = ListsAndRuns[fn].bind(ListsAndRuns);
		ListsAndRuns[fn] = function (text, ...rest) {
			if (String(text).includes(phrase)) {
				const links = fn === "inlineMarkup" ? rest[0] : rest[1];
				const st = (new Error().stack || "").split("\n").slice(2, 6).map((s) => s.trim().replace(/\(.*[\\/]/, "(")).join(" <- ");
				_l(`${fn}: links=${JSON.stringify((links || []).map((l) => l.text).slice(0, 4))} :: ${String(text).slice(0, 90).replace(/\n/g, "⏎")}\n    ${st}`);
			}
			return orig(text, ...rest);
		};
	}
	const base = corpus.mdir(GOLD, code);
	const run = new ConversionRun({ imageMode: "P" }); const docs = [];
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
		const buf = fs.readFileSync(path.join(base, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		docs.push({ name, doc: await DocxExtractor.Extract(zip) });
	}
	for (const b of docs.flatMap((d) => d.doc.blocks)) {
		const t = JSON.stringify(b);
		if (t.includes(phrase)) _l("BLOCK links:", JSON.stringify(b.links ?? b.block?.links ?? null).slice(0, 300));
	}
	const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
	const prep = ModuleResolver.PrepareRun({ docs, run, normaliser, istockAcksFiles });
	if (!prep.ok) { _l("prep failed"); return; }
	await PageAssembler.AssembleModule(run, normaliser);
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
