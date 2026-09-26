/** _s52_items_dump.cjs — session 52 Round 2: dump every module's page item stream (after PageAssembler's passes, as
 *  InteractiveScanner.ScanPage sees it) to outputs/_s52_items/<CODE>.tsv — page, idx, type, tag, directive, bold-lead flag,
 *  the tag's payload and the black text (clipped). In memory; writes only the TSVs. From reference/tests/ under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s52_items_dump.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const OUT = path.join(__dirname, "_s52_items"); fs.mkdirSync(OUT, { recursive: true });
const clip = (s, n) => String(s ?? "").replace(/[\t\r\n]+/g, " ").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let rows = [], pg = 0;
	const orig = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		const items = page.items ?? [];
		for (let k = 0; k < items.length; k++) {
			const it = items[k];
			const p = it.parse?.primary;
			const txt = it.type === "black" ? it.text : (it.type === "table" ? "[TABLE]" : "");
			rows.push([pg, k, it.type, p?.tag ?? "", p?.directive ?? "", /^\s*\*\*/.test(it.type === "black" ? it.text : (it.blackAfter ?? "")) ? "B" : "",
				clip(it.type === "tag" ? it.text : "", 60), clip(it.type === "tag" ? it.blackAfter : "", 300), clip(txt, 400)].join("\t"));
		}
		pg++;
		return orig(page, normaliser, run);
	};
	for (const code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		rows = []; pg = 0;
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
		fs.writeFileSync(path.join(OUT, code + ".tsv"), rows.join("\n") + "\n");
	}
	_l("done");
}
main();
