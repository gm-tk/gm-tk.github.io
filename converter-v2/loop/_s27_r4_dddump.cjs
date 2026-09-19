/** _s27_r4_dddump.cjs — dump every dragAndDrop bundle of ONE module: members, tables, start/end, the items around it.
 *  Usage (from reference/tests/): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s27_r4_dddump.cjs CODE [page] */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
const code = process.argv[2], onlyPage = process.argv[3] || null;
function itemStr(it) {
	if (!it) return "∅";
	if (it.type === "table") { const rows = it.block?.rows ?? []; return `TABLE ${rows.length}x${Math.max(0, ...rows.map((r) => (r || []).length))}${it._consumed ? " (consumed)" : ""}`; }
	if (it.type === "black") return `black «${clean(it.text).slice(0, 60)}»${it._consumed ? " (consumed)" : ""}`;
	const p = it.parse?.primary; return `tag[${p?.tag ?? "?"}/${p?.directive ?? "?"}/${it.parse?.class ?? "?"}] «${clean(it.text).slice(0, 50)}» after«${clean(it.blackAfter).slice(0, 50)}»${it._consumed ? " (consumed)" : ""}${it.consumedBy ? " by=" + it.consumedBy : ""}`;
}
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
		const bundles = origScan(page, normaliser, run);
		if (onlyPage && label !== onlyPage) return bundles;
		const items = page.items || [];
		for (const b of (bundles || [])) {
			if (b.type !== "dragAndDrop") continue;
			_l(`\n=== ${code}/${label} bundle#${b.index} type=${b.type} start=${b.startIndex} end=${b.endIndex} tables=${(b.tables || []).length} extra=${JSON.stringify(b.extraTypes || [])} owner=${b.activityOwner ? "yes" : "no"} variant=${b.variant ?? ""}`);
			_l("  members:"); for (const m of (b.memberItems || [])) _l("    " + itemStr(m));
			_l("  items around:"); for (let i = Math.max(0, b.startIndex - 2); i < Math.min(items.length, b.endIndex + 8); i++) _l(`    [${i}]${i >= b.startIndex && i < b.endIndex ? "*" : " "} ` + itemStr(items[i]));
		}
		return bundles;
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
