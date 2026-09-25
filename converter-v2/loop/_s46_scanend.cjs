/** _s46_scanend.cjs — session 46: where does the scanner END each bundle of TYPE on a page, and on what item? Prints each bundle's
 *  last members and the terminator item (page.items[endIndex]). Run from reference/tests under WSL:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s46_scanend.cjs CODE PAGE [TYPE] */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const brief = (it) => !it ? "(end of page)" : `${it.type}${it.type === "tag" ? " [" + (it.parse?.primary?.tag ?? it.parse?.class ?? "?") + "]" : ""} ${JSON.stringify(String(it.text ?? it.block?.rows?.[0] ?? "").slice(0, 90))}${it.blackAfter ? " + " + JSON.stringify(String(it.blackAfter).slice(0, 60)) : ""}`;
async function main() {
	const [code, want, type] = process.argv.slice(2);
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) {
		const res = origScan(page, n, run);
		const label = String(page?.lessonLabel ?? page?.label ?? "?");
		if (!want || label === want || label.startsWith(want)) {
			const bundles = Array.isArray(res) ? res : (res?.bundles ?? []);
			for (const b of bundles) {
				if (type !== "*" && b?.type !== (type || "accordion")) continue;
				_l(`=== ${code} ${label} #${b.index} [${b.type}] owner=${b.activityOwner ? "Y" : "-"} start ${b.startIndex} end ${b.endIndex} members ${(b.memberItems ?? []).length}`);
				for (const m of (b.memberItems ?? []).slice(process.env.ALLM ? 0 : -3)) _l("   last member: " + brief(m));
				_l("   TERMINATOR: " + brief(page.items[b.endIndex]));
				_l("   then:       " + brief(page.items[b.endIndex + 1]));
			}
		}
		return res;
	};
	const base = corpus.mdir(GOLD, code);
	const run = new ConversionRun({ imageMode: "P" }); const docs = [];
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
		const buf = fs.readFileSync(path.join(base, name));
		docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
	}
	const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
	const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
	if (!prep.ok) { _l("prep failed"); return; }
	await PageAssembler.AssembleModule(run, norm);
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
