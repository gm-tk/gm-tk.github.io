/** _s50_r1_bundledump.cjs — session 50 Round 1 (r510): dump the opener items of every dragAndDrop bundle the
 *  builder sees for the given codes (in memory, no disk writes). Run from reference/tests/ under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s50_r1_bundledump.cjs HPFUN101
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const TYPE = process.env.DUMP_TYPE || "dragAndDrop";
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const orig = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle;
		const out = orig(args);
		if (b?.type === TYPE) {
			_l(`--- ${b.type} #${b.index} modifier=${JSON.stringify(b.modifier)} built=${out ? "yes" : "no"}`);
			_l(`  keys=${Object.keys(b).join(",")} opener=${JSON.stringify(b.opener ?? b.openerItem ?? null)?.slice(0,300)}`);
			for (const m of (b.memberItems ?? []).slice(0,3)) _l(`  member ${m.type}: text=${JSON.stringify(String(m.text ?? "").slice(0, 160))}`);
			for (const m of b.openerItems ?? []) _l(`  opener ${m.type}: text=${JSON.stringify(String(m.text ?? "").slice(0, 160))} free=${JSON.stringify(String(m.parse?.free ?? "").slice(0, 120))} keys=${Object.keys(m).join(",")}`);
		}
		return out;
	};
	for (const code of process.argv.slice(2).filter((a) => !a.startsWith("--"))) {
		const base = corpus.mdir(MODS, code);
		const run = new ConversionRun({ imageMode: "P" });
		const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
			docs.push({ name, doc: await DocxExtractor.Extract(zip) });
		}
		const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
		_l(`== ${code} prep ${prep.ok}`);
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l("convert error: " + e.message); }
	}
}
main();
