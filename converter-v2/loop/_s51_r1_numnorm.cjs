/** _s51_r1_numnorm.cjs — session 51 Round 1 PICK: every page_number_normalise rename note (the r369 post-pass), with the
 *  pre-normalise id list reconstructed from it. A DUPLICATE writer id (two boxes both carrying 4A) is the split-box class:
 *  the writer's one activity rendered as two boxes; the de-dupe then shifts every later id on the page by one letter.
 *  In memory, no disk writes. Run from reference/tests/ under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s51_r1_numnorm.cjs CODES…
 *  Output: code \t page \t renames */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	for (const code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		const run = new ConversionRun({ imageMode: "P" });
		const origNote = run.AddNote.bind(run);
		run.AddNote = function (lvl, src, msg) {
			const m = /^Page (.*?): activity numbers? normalised \(page_number_normalise\): (.*)\.$/.exec(String(msg ?? ""));
			if (m) _l(`${code}\t${m[1]}\t${m[2]}`);
			return origNote(lvl, src, msg);
		};
		const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
		}
		const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
		if (!prep.ok) continue;
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}\tASSEMBLE ERROR`); }
	}
}
main();
