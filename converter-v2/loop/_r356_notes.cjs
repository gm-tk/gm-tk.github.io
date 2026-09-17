/** _r356_notes.cjs — print the members-rule decline notes for the given modules (from reference/tests under WSL). Diagnostic only. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs")), corpus = require(path.join(TESTS, "corpus.cjs"));
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const normaliser = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  for (const code of process.argv.slice(2)) {
    const base = corpus.mdir(GOLD, code); const run = new ConversionRun({ imageMode: "P" }); const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
      const buf = fs.readFileSync(path.join(base, name)); const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
      docs.push({ name, doc: await DocxExtractor.Extract(zip) });
    }
    const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser, istockAcksFiles }); if (!prep.ok) { _l(code, "prep failed"); continue; }
    await PageAssembler.AssembleModule(run, normaliser);
    for (const n of (run.notes ?? [])) if (/Members rule/.test(n.message ?? n.text ?? JSON.stringify(n))) _l(code, "|", n.message ?? n.text ?? JSON.stringify(n));
  }
}
main().catch((e) => { console.error(e); process.exit(1); });
