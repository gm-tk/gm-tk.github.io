/** _r356_memberdump.cjs — dump the members of the named bundles: CODE:INDEX … (from reference/tests under WSL). Diagnostic only. */
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
  const want = new Map(process.argv.slice(2).map((a) => { const [c, i] = a.split(":"); return [c, new Set((i ?? "").split(",").map(Number))]; }));
  const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
  let cur = "?";
  InteractiveBuilder.Build = function (args) {
    const b = args?.bundle;
    if (b && want.get(cur)?.has(b.index)) {
      _l(`== ${cur} #${b.index} ${b.type} members:`);
      (b.memberItems ?? []).forEach((m, k) => _l(`  [${k}] ${m?.type} tag=${m?.parse?.primary?.tag ?? "-"} dir=${m?.parse?.primary?.directive ?? "-"} cls=${m?.parse?.class ?? "-"} text=${JSON.stringify(String(m?.text ?? "").slice(0, 90))} after=${JSON.stringify(String(m?.blackAfter ?? "").slice(0, 60))} links=${(m?.block?.links ?? []).length}`));
    }
    return origBuild(args);
  };
  const normaliser = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  for (const code of want.keys()) {
    cur = code;
    const base = corpus.mdir(GOLD, code); const run = new ConversionRun({ imageMode: "P" }); const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
      const buf = fs.readFileSync(path.join(base, name)); const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
      docs.push({ name, doc: await DocxExtractor.Extract(zip) });
    }
    const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser, istockAcksFiles }); if (!prep.ok) continue;
    await PageAssembler.AssembleModule(run, normaliser);
  }
}
main().catch((e) => { console.error(e); process.exit(1); });
