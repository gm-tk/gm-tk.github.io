/** _s50_r511_ddyellow.cjs — session 50 Round 2 (r511, D15-19 dropDown): every dropDown bundle in the given modules —
 *  does it carry a YELLOW mark (block or table cell), a GREEN one, is it built, and (for yellow, unbuilt) the first lines.
 *  In memory, no writes. Run from reference/tests/ under WSL:  node ../../outputs/_s50_r511_ddyellow.cjs CODES…  */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const TYPE = process.env.DUMP_TYPE || "dropDown";
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "";
	const tally = { bundles: 0, built: 0, yellow: 0, yellowBuilt: 0, green: 0 };
	const orig = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle; const out = orig(args);
		if (b?.type === TYPE) {
			const marks = [];
			for (const m of b.memberItems ?? []) {
				for (const x of m?.block?.marks ?? []) marks.push(x);
				for (const row of m?.block?.cellMarks ?? []) for (const cell of row ?? []) for (const x of cell ?? []) marks.push(x);
			}
			const y = marks.filter((x) => x.kind === "hl" && x.color === "yellow"), g = marks.filter((x) => x.kind === "green" || (x.kind === "hl" && x.color === "green"));
			tally.bundles++; if (out) tally.built++; if (y.length) { tally.yellow++; if (out) tally.yellowBuilt++; } if (g.length) tally.green++;
			if (y.length) {
				const first = (b.memberItems ?? []).map((m) => String(m?.text ?? "").replace(/\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, "").replace(/\s+/g, " ").trim()).filter(Boolean).slice(0, 3).join(" | ");
				_l(`${code} #${b.index} ${out ? "BUILT" : "box"} yellow ${y.length} [${y.slice(0, 3).map((x) => String(x.text).slice(0, 25)).join(" / ")}] tables ${(b.memberItems ?? []).filter((m) => m?.type === "table").length} :: ${first.slice(0, 150)}`);
			}
		}
		return out;
	};
	for (code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		const run = new ConversionRun({ imageMode: "P" });
		const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
		}
		const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
		if (!prep.ok) continue;
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR`); }
	}
	_l(`TALLY ${JSON.stringify(tally)}`);
}
main();
