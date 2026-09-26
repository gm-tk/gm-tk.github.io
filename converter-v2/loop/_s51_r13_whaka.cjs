/** _s51_r13_whaka.cjs — session 51 Round 13 PICK: for every gold `div.whakatauki` box (_s51_r13_whakagold.tsv) find the WT item
 *  holding its first paragraph in the Claude item stream and print the item (type, primary tag, raw text with its ** / * marks),
 *  the two items before it and the one after — the writer's cue, if any. In memory. From reference/tests/ under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s51_r13_whaka.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 90) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const norm = (s) => String(s ?? "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/<[^>]+>|\*+|_+/g, "").replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim();
const gold = {};
for (const l of fs.readFileSync(path.join(__dirname, "_s51_r13_whakagold.tsv"), "utf8").split("\n").filter(Boolean)) {
	const [code, page, tdir, n, p1] = l.split("\t");
	(gold[code] ??= []).push({ page, key: norm(p1).slice(0, 28) });
}
const desc = (it) => it ? `${it.type}:${it.parse?.primary?.tag ?? ""}:${clip(it.type === "black" ? it.text : (it.text + " ⟶ " + (it.blackAfter ?? "")), 70)}` : "-";
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "", seen = new Set();
	const orig = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		const items = page.items ?? [];
		for (const g of gold[code] ?? []) {
			if (!g.key || seen.has(g.key)) continue;
			for (let k = 0; k < items.length; k++) {
				const it = items[k];
				const t = norm(it.type === "black" ? it.text : `${it.text} ${it.blackAfter ?? ""}`);
				if (!t.includes(g.key)) continue;
				seen.add(g.key);
				const prev = items.slice(Math.max(0, k - 2), k).filter(Boolean);
				_l(`WHAKA\t${code}\t${g.page}\t${prev.map(desc).join(" ‖ ")}\t>>> ${desc(it)} [raw ${clip(JSON.stringify(it.runs?.slice?.(0, 1) ?? it.text), 60)}]\t<<< ${desc(items[k + 1])}`);
				break;
			}
		}
		return orig(page, normaliser, run);
	};
	for (code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		seen = new Set();
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
		for (const g of gold[code] ?? []) if (g.key && !seen.has(g.key)) _l(`WHAKA\t${code}\t${g.page}\tNOT FOUND\t${g.key}`);
	}
}
main();
