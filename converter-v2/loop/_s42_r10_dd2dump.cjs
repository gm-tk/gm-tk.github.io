/** Session 42 Round 10 — dump every dragAndDrop bundle that does NOT build and holds exactly ONE two-column table: module, page label,
 *  bundle index, the table's rows (cell text, red spans kept as «…»), the bundle's other member lines (the writer's instruction).
 *  Run from CONVERTER_V2/reference/tests under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s42_r10_dd2dump.cjs CODE…  > ../../outputs/_s42_r10_dd2dump.json */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);
const clean = (s) => String(s ?? "").replace(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu, "«$1»").replace(/\*\*|__|\*/g, "").replace(/\s+/g, " ").trim();
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const out = []; let cur = "?", page = "?";
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (p, n, r) { page = String(p?.lessonLabel ?? p?.label ?? "?"); return origScan(p, n, r); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle; let res = null;
		try { res = origBuild(args); } catch (e) { res = null; }
		try {
			const t = b?.tables ?? [];
			if (b?.type === "dragAndDrop" && res == null && t.length === 1) {
				const rows = (t[0].rows ?? []).map((r) => r.map(clean));
				if (rows.length && Math.max(...rows.map((r) => r.length)) === 2) {
					const lines = [];
					for (const m of b.memberItems ?? []) {
						if (!m || m.type === "table") continue;
						const s = clean(m.type === "black" ? m.text : ((m.text ?? "") + " " + (m.blackAfter ?? "")));
						if (s) lines.push(s.slice(0, 200));
					}
					out.push({ code: cur, page, index: b.index, rows, lines, extra: b.extraTypes ?? [], media: (b.media ?? []).length });
				}
			}
		} catch (e) { /* keep going */ }
		return res;
	};
	for (const code of codes) {
		cur = code;
		let dir; try { dir = corpus.mdir(MODS, code); fs.readdirSync(dir); } catch { continue; }
		try {
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
				const buf = fs.readFileSync(path.join(dir, name));
				docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
			}
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
			if (!prep.ok) continue;
			await PageAssembler.AssembleModule(run, norm);
		} catch (e) { /* keep going */ }
	}
	_l(JSON.stringify(out, null, 1));
}
main().catch((e) => { console.error(e); process.exit(1); });
