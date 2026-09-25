"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
(async () => {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
	eng.loadEngine();
	const [code, idx] = [process.argv[2], +process.argv[3]];
	const orig = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (a) { const b = a?.bundle; if (b?.index === idx && b.type === "dragAndDrop") {
		_l("opener", JSON.stringify((b.openerItems ?? []).map((m) => [m.type, String(m.text ?? "").slice(0, 60), String(m.blackAfter ?? "").slice(0, 40), m.block?.id ?? m.block?.list ?? ""])));
		for (const m of (b.memberItems ?? []).slice(0, 6)) _l(JSON.stringify([m.type, m.parse?.class, String(m.text ?? "").slice(0, 60), String(m.blackAfter ?? "").slice(0, 40), m.block?.list ?? "", m.block === (b.memberItems[0]?.block)]));
		_l("prevItemText", JSON.stringify(b.prevItemText)); }
		return orig(a); };
	const base = corpus.mdir(MODS, code); const run = new ConversionRun({ imageMode: "P" });
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const docs = []; for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) { const buf = fs.readFileSync(path.join(base, name)); docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) }); }
	const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] }); if (prep.ok) await PageAssembler.AssembleModule(run, norm);
})();
