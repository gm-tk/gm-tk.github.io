// _r342_notes.cjs — convert one module in memory and print run notes matching a needle (debug; writes nothing)
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const [code, needle] = process.argv.slice(2);
(async () => {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const base = corpus.mdir(MODS, code); const run = new ConversionRun({ imageMode: "P" }); const docs = [];
  for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
    const buf = fs.readFileSync(path.join(base, name)); const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
    docs.push({ name, doc: await DocxExtractor.Extract(zip) });
  }
  const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
  await PageAssembler.AssembleModule(run, norm);
  const notes = (run.notes || []).filter((n) => JSON.stringify(n).toLowerCase().includes(needle.toLowerCase()));
  _l(`${notes.length} note(s) matching '${needle}':`); for (const n of notes) _l("  " + JSON.stringify(n).slice(0, 300));
})().catch((e) => process.stdout.write("ERR " + (e && e.stack || e) + "\n"));
