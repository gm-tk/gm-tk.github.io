/** _r350_dump.cjs — dump every dragAndDrop bundle's raw table cells for the named modules (diagnostic; the r350 census hook, unclipped). */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests"), GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
  let cur = "?";
  InteractiveBuilder.Build = function (args) {
    const b = args?.bundle; const out = origBuild(args);
    if (b?.type === "dragAndDrop") {
      _l(`== ${cur} #${b.index} built=${out != null} extra=${(b.extraTypes||[]).length} media=${(b.media||[]).length} tables=${(b.tables||[]).length} instr=${JSON.stringify(b.instructions||[])}`);
      for (const t of (b.tables || [])) for (const r of (t.rows || [])) _l("   " + JSON.stringify(r.map((c) => String(c).slice(0, 140))));
    }
    return out;
  };
  for (const code of process.argv.slice(2)) {
    cur = code; const base = corpus.mdir(GOLD, code);
    const run = new ConversionRun({ imageMode: "P" }); const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
    if (!prep.ok) { _l(code + " prep refused"); continue; }
    await PageAssembler.AssembleModule(run, norm);
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
