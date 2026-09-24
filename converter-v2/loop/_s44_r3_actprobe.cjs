/** _s44_r3_actprobe.cjs — session 44 Round 3: convert the given modules (default: the Bilingual folder) in memory with
 *  BilingualBuilder.bilingualActivity wrapped, and record every call: the module, the page, the gathered blocks, each block's rows by
 *  shape (cells / filled / HEAD-BODY-MARKER-OTHER) and how many elements the box emitted. Also counts the keystone bilingualSection calls
 *  whose gather holds a marker table. WSL, from reference/tests:
 *  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s44_r3_actprobe.cjs [--rows] [CODE ...] */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const strip = (s) => String(s ?? "").replace(/🔴|\[\/?RED TEXT\]/g, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
const shapeOf = (r) => {
	const cells = (r || []).map(strip);
	const lead = /\[\s*activity\s*:?\s*embedded/i.test(cells.join(" ")) ? "MARKER" : /^\[\s*h\d\s*\]/i.test(cells[0] || cells[1] || "") ? "HEAD"
		: /^\[\s*body/i.test(cells[0] || cells[1] || "") ? "BODY" : "OTHER";
	return `${cells.length}c:${cells.map((c) => (c ? 1 : 0)).join("")}:${lead}`;
};
(async () => {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const args = process.argv.slice(2), showRows = args.includes("--rows");
	let codes = args.filter((a) => !a.startsWith("--"));
	if (!codes.length) codes = fs.readdirSync(path.join(MODS, "Bilingual"));
	let cur = "";
	const calls = [], shapes = {};
	const orig = BilingualBuilder.bilingualActivity.bind(BilingualBuilder);
	BilingualBuilder.bilingualActivity = function (blocks, run, n) {
		const html = orig(blocks, run, n);
		const rec = { code: cur, blocks: blocks.length, rows: [], els: (String(html || "").match(/<(p|h\d|li)\b/g) || []).length };
		for (const b of blocks) for (const r of (b.rows || [])) { const s = shapeOf(r); rec.rows.push(s); shapes[s] = (shapes[s] || 0) + 1; }
		calls.push(rec); return html;
	};
	for (const code of codes) {
		cur = code;
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		const run = new ConversionRun({ imageMode: "P" });
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
			docs.push({ name, doc: await DocxExtractor.Extract(zip) });
		}
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
		if (!prep.ok) continue;
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { continue; }
	}
	const byMod = {};
	for (const c of calls) { byMod[c.code] = byMod[c.code] || { calls: 0, rows: 0, els: 0 }; byMod[c.code].calls++; byMod[c.code].rows += c.rows.length; byMod[c.code].els += c.els; }
	_l("bilingualActivity calls by module:", JSON.stringify(byMod));
	_l("row shapes across every call:"); for (const [k, v] of Object.entries(shapes).sort((a, b) => b[1] - a[1])) _l(`  ${k.padEnd(20)} ${v}`);
	if (showRows) for (const c of calls) _l(`${c.code} blocks=${c.blocks} els=${c.els} rows: ${c.rows.join(" ")}`);
})().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
