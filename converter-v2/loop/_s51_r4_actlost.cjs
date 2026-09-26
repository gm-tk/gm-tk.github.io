/** _s51_r4_actlost.cjs — session 51 Round 4 PICK: every red span whose tags include the activity tag but whose PRIMARY is some
 *  other tag (after r523), grouped by the winning tag + directive and the other tags. In memory (the item stream only — no
 *  conversion). Run from reference/tests/ under WSL:  node ../../outputs/_s51_r4_actlost.cjs CODES…
 *  Output: ACT \t code \t primary(directive) \t tags \t numbers \t text */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 90) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	for (const code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
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
		const items = PageSplitter.BuildItemStream(run.wtBlocks, norm);
		for (const it of items) {
			if (it.type !== "tag" || !it.parse) continue;
			const tags = it.parse.tags ?? [];
			if (!tags.some((t) => t.tag === "activity") || it.parse.primary?.tag === "activity") continue;
			const p = it.parse.primary;
			_l(`ACT\t${code}\t${p ? p.tag + "(" + p.directive + ")" : "-"}\t${tags.map((t) => t.tag).join("+")}\t${JSON.stringify(it.parse.numbers)}\t${clip(it.text, 70)} » ${clip(it.blackAfter, 40)}`);
		}
	}
}
main();
