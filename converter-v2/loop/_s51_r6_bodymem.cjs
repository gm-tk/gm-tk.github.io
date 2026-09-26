/** _s51_r6_bodymem.cjs — session 51 Round 6 PICK: every [Body]-tagged MEMBER of every widget bundle (in memory, the scanner's
 *  own bundles): its bundle type, whether it comes after the bundle's first table / list / widget content ("after content"),
 *  and its text. Prints one TSV line per member: BM \t code \t type \t pos \t afterContent \t built \t text. The gold placement
 *  is joined by _s51_r6_bodymem_join.py. Run from reference/tests/ under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s51_r6_bodymem.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 120) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "", all = [];
	const orig = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		const out = orig(page, normaliser, run);
		for (const b of out ?? []) all.push(b);
		return out;
	};
	for (code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		all = [];
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
		for (const b of all) {
			const mem = b.memberItems ?? [];
			let content = false;
			for (let k = 0; k < mem.length; k++) {
				const m = mem[k];
				if (m?.type === "table" || (m?.type === "black" && /^\s*(?:[•\-–*]|\d+[.)])\s/.test(String(m.text ?? ""))) || (m?.type === "tag" && m.parse?.primary?.directive === "INTERACTIVE" && k > 0)) content = true;
				if (m?.type === "tag" && ["body", "body text"].includes(String(m.parse?.primary?.tag ?? ""))) {
					const t = String(m.blackAfter ?? "").trim();
					if (t.split(/\s+/).length >= 4) _l(`BM\t${code}\t${b.type}\t${k}/${mem.length}\t${content ? 1 : 0}\t${b.built ? 1 : 0}\t${clip(t)}`);
				}
			}
		}
	}
}
main();
