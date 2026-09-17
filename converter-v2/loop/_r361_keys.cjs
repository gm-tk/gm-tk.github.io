"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
(async () => {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const code = process.argv[2]; const base = corpus.mdir(MODS, code); const run = new ConversionRun({ imageMode: "P" }); const docs = [];
  for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) { const buf = fs.readFileSync(path.join(base, name)); const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength)); docs.push({ name, doc: await DocxExtractor.Extract(zip) }); }
  ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] }); await PageAssembler.AssembleModule(run, norm);
  const items = run.pages[0].items;
  for (const i of [14, 15, 21]) { const it = items[i]; _l(i, Object.keys(it).join(","), "| text:", JSON.stringify(String(it.text).slice(0, 60)), "| block.lines:", it.block?.lines?.length, "| block.text:", JSON.stringify(String(it.block?.text ?? "").slice(0, 50))); }
})();
