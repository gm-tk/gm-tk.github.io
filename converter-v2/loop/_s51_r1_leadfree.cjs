/** _s51_r1_leadfree.cjs — session 51 Round 1 PICK: every firing of the r366 rule (activity_wrapper.lead_free_after_tag —
 *  the first black member's first paragraph freed as the activity's lead above the box) and what it freed. Flags:
 *    LIST  — the freed paragraph is a numbered / lettered / bulleted list item ("1. The bus", "a) …", "• …")
 *    FRAG  — the freed member's block continues with a RED member (the answer typed inside the same sentence)
 *  In memory, no disk writes. Run from reference/tests/ under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s51_r1_leadfree.cjs CODES…
 *  Output: one TSV line per firing: code  type  flags  words  freed-text  |  next-member */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 90) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const LIST = /^\s*(?:\(?\d{1,2}[.)]|\(?[a-hA-H][.)]|[•\-–*·▪◦])\s+/;
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "", seen = [];
	const orig = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		const out = orig(page, normaliser, run);
		for (const b of out ?? []) seen.push({ b, mem: [...(b.memberItems ?? [])] });
		return out;
	};
	for (code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		seen = [];
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
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}\tASSEMBLE ERROR`); continue; }
		for (const { b, mem } of seen) {
			for (let k = 0; k < mem.length; k++) {
				const m = mem[k];
				const freed = m._leadFree ? String(m.text ?? "") : (m._leadFreed ?? null);
				if (freed == null) continue;
				const nx = mem[k + 1];
				const flags = [];
				if (LIST.test(freed)) flags.push("LIST");
				if (nx && nx.block && nx.block === m.block && nx.type === "tag") flags.push("FRAG");
				if (!/[.?!:;)"'”’]\s*$/.test(freed.trim())) flags.push("NOSTOP");
				_l(`${code}\t${b.type}\t${flags.join(",") || "-"}\t${freed.trim().split(/\s+/).length}\t${clip(freed)}\t|\t${nx ? nx.type + ":" + clip(nx.type === "black" ? nx.text : (nx.text + " » " + (nx.blackAfter ?? "")), 60) : "-"}`);
			}
		}
	}
}
main();
