/** _s51_r2_jactid.cjs — session 51 Round 2 PICK: every red tag item whose text is a JOURNAL instruction naming an activity id
 *  ("[Go to your learning journal and complete activity 2B]") — how TagNormaliser parsed it (primary tag, class, numbers) and
 *  the next non-empty item after it (the section the phantom activity box would wrap). In memory. Run from reference/tests/
 *  under WSL:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s51_r2_jactid.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 90) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const RE = new RegExp(process.env.JRE || "journal[\\s\\S]*activit(?:y|ies)\\s*\\d|activit(?:y|ies)\\s*\\d[\\s\\S]*journal", "i");
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
			if (it.type !== "tag" || !RE.test(String(it.text ?? ""))) continue;
			let j = k + 1; while (j < items.length && !String(items[j].text ?? "").trim() && !String(items[j].blackAfter ?? "").trim()) j++;
			const nx = items[j];
			const p = it.parse ?? {};
			_l(`JACT\t${code}\t${page.lessonLabel ?? "?"}\tprimary=${p.primary?.tag ?? "-"}\tcls=${p.class ?? "-"}\tnums=${JSON.stringify(p.numbers ?? [])}\ttags=${JSON.stringify((p.tags ?? []).map((t) => t.tag))}\t${clip(it.text, 80)}\t|after=${clip(it.blackAfter, 40)}\t| next ${nx ? nx.type + ":" + (nx.parse?.primary?.tag ?? "") + ":" + clip(nx.type === "black" ? nx.text : nx.blackAfter || nx.text, 50) : "-"}`);
		}
		return orig(page, normaliser, run);
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
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}\tASSEMBLE ERROR`); }
	}
}
main();
