/** _s51_r13_proverb.cjs — session 51 Round 13 MEASURE: every UNTAGGED proverb-shaped pair in the WT item stream — a black paragraph
 *  of ≥ 4 words, EVERY word Māori-phonotactic (open syllables over the Māori alphabet), followed by a black English paragraph — with
 *  the item before it (the cue) and the table flag. Prints PROV rows for _s51_r13_provgold.py to look up in the gold. In memory.
 *  From reference/tests/ under WSL:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s51_r13_proverb.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 90) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const strip = (s) => String(s ?? "").replace(/<[^>]+>|\*+|(?<![a-z])_+|_+(?![a-z])/gi, "").replace(/\s+/g, " ").trim();
const SYL = /^(?:(?:[hkmnprtw]|ng|wh)?[aeiouāēīōū])+$/i;
const words = (s) => strip(s).normalize("NFC").replace(/[‘’'"“”.,;:!?()\-–—…]/g, " ").split(/\s+/).filter(Boolean);
const isReo = (s) => { const w = words(s); return w.length >= 4 && w.every((x) => SYL.test(x)); };
const isEng = (s) => { const w = words(s); return w.length >= 3 && w.filter((x) => SYL.test(x)).length / w.length < 0.5; };
const textOf = (it) => it ? (it.type === "black" ? it.text : "") : "";
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "";
	const orig = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		const items = page.items ?? [];
		for (let k = 0; k < items.length; k++) {
			const it = items[k];
			if (it.type !== "black" || !isReo(it.text)) continue;
			let j = k + 1; while (j < items.length && !String(textOf(items[j]) || items[j].text || "").trim()) j++;
			const nx = items[j];
			if (!nx || nx.type !== "black" || !isEng(nx.text)) continue;
			let p = k - 1; while (p >= 0 && !String(items[p].text ?? "").trim() && !String(items[p].blackAfter ?? "").trim()) p--;
			const pv = items[p];
			const cue = pv ? `${pv.type}:${pv.parse?.primary?.tag ?? ""}` : "-";
			const bold = /^\s*\*\*/.test(it.text) ? "bold" : /^\s*\*/.test(it.text) || /^\s*_/.test(it.text) ? "ital" : "plain";
			_l(`PROV\t${code}\t${page.lessonLabel ?? "?"}\t${cue}\t${bold}\t${it.inTable || it.table ? "table" : "free"}\t${clip(strip(it.text), 80)}\t${clip(strip(nx.text), 60)}`);
		}
		return orig(page, normaliser, run);
	};
	for (code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		const run = new ConversionRun({ imageMode: "P" });
		const nm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
		}
		const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: nm, istockAcksFiles });
		if (!prep.ok) continue;
		try { await PageAssembler.AssembleModule(run, nm); } catch (e) { _l(`${code}\tASSEMBLE ERROR`); }
	}
}
main();
