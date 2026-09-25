/** _s50_r9_typtable.cjs — session 50 Round 9 PICK: every typing / selfCheck bundle holding exactly ONE table with red cells
 *  (the writer's answers) — built? media? the opener words; per module. In memory. Run from reference/tests/ under WSL. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const cellText = (c) => String(typeof c === "string" ? c : c?.text ?? "");
const isRed = (c) => { const s = cellText(c).trim(); return !!s && s.replace(RED, "").replace(/[\s|/•·,.;:–-]+/g, "") === "" && RED.test(s); };
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "";
	const orig = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle; const out = orig(args);
		if (b && (b.type === "typing" || b.type === "selfCheck")) {
			const tabs = (b.memberItems ?? []).filter((m) => m?.type === "table");
			if (tabs.length === 1) {
				const rows = tabs[0].block?.rows ?? [];
				let red = 0, black = 0, mixedRows = 0;
				for (const r of rows) { let rr = 0, bb = 0; for (const c of r ?? []) { if (!cellText(c).trim()) continue; RED.lastIndex = 0; if (isRed(c)) rr++; else bb++; } red += rr; black += bb; if (rr && bb) mixedRows++; }
				const opener = (b.memberItems ?? []).filter((m) => m?.type === "tag").map((m) => cellText(m.text).replace(RED, "$1")).join(" ").replace(/\s+/g, " ").slice(0, 110);
				const media = (b.media ?? []).length || rows.some((r) => (r ?? []).some((c) => /https?:\/\/|\[image|\[photo/i.test(cellText(c))));
				_l(`${code}\t#${b.index}\t${b.type}\t${out ? "BUILT" : "box"}\trows ${rows.length}\tred ${red}\tblack ${black}\tmixedRows ${mixedRows}\tmedia ${media ? 1 : 0}\t${opener}`);
			}
		}
		return out;
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
