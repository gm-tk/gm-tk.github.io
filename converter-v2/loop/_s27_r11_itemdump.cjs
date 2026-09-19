/** _s27_r11_itemdump.cjs — dump every page item of ONE module whose text matches a regex (env MATCH), with its type / parse class / primary / tag count.
 *  Usage (from reference/tests/): MATCH="activity 4|understanding" STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s27_r11_itemdump.cjs CODE */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
const code = process.argv[2]; const rx = new RegExp(process.env.MATCH || "activity 4", "i");
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
	eng.loadEngine(); console.log = _l;
	globalThis.norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	let dir = null;
	for (const t of fs.readdirSync(GOLD)) { const d = path.join(GOLD, t, code); if (fs.existsSync(d)) dir = d; }
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		const label = String(page?.lessonLabel ?? page?.label ?? "?");
		for (const [ix, x] of (page.items || []).entries()) {
			const t = clean(x.text) + " | " + clean(x.blackAfter);
			if (!rx.test(t)) continue;
			_l(`ITEM[${label}#${ix}] type=${x.type} class=${x.parse?.class} prim=${x.parse?.primary?.tag ?? "null"} tags=${(x.parse?.tags || []).length} consumed=${x.consumedBy} «${t.slice(0, 110)}»`);
		}
		return origScan(page, normaliser, run);
	};
	const run = new ConversionRun({ imageMode: "P" }); const docs = [];
	for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
		const buf = fs.readFileSync(path.join(dir, name));
		docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
	}
	const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm }); if (!prep.ok) { _l("prep failed"); return; }
	await PageAssembler.AssembleModule(run, norm);
}
main().catch((e) => { console.error(e); process.exit(1); });
