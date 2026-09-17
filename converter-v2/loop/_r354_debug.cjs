/** _r352_debug.cjs — ROUND 352 diagnostic: for every carousel bundle of the named modules, prints the members with their parse
 *  directive / class / blackAfter and whether the build succeeded, so the members rule's verdict can be traced. Never imported. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests"), GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
  let cur = "?";
  InteractiveBuilder.Build = function (args) {
    const b = args?.bundle; let out, err = null;
    const notesBefore = (args.run?.notes ?? args.run?._notes ?? []).length;
    try { out = origBuild(args); } catch (e) { err = e; out = null; }
    if (["accordion", "hintSlider", "flipCard"].includes(b?.type) && out != null) {
      const notes = args.run?.notes ?? args.run?._notes ?? [];
      for (const n of notes.slice(notesBefore)) _l("   NOTE:", JSON.stringify(n).slice(0, 300));
      _l(`== ${cur} #${b.index} built=${out != null} err=${err ? err.message : ""} tables=${(b.tables || []).length} extra=${(b.extraTypes || []).length} r279=${!!b.r279CarouselTable}`);
      (b.memberItems || []).slice(0, 2).forEach((m, i) => _l(`   [${i}] ${m.type} tag=${m.parse?.primary?.tag ?? m.tag ?? "-"} dir=${m.parse?.primary?.directive ?? "-"} cls=${m.parse?.class ?? "-"} text=${String(m.text ?? "").replace(RED, "").trim().slice(0, 40)} after=${String(m.blackAfter ?? "").replace(RED, "").trim().slice(0, 40)}`));
      _l("   INSTR:", JSON.stringify(b.instructions || []).slice(0, 200));
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
