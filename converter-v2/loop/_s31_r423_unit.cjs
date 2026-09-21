/** _s31_r423_unit.cjs — round 423 unit check: PromoteTableRowMarkers on PMT101 (must promote 9, recognised as a WT,
 *  block stream shaped like PNR107's) and on PNR107 / ENGS202 / TRR116 / TRR115 (must return the SAME array).
 *  Also converts PMT101 in memory and reports the pages built + their labels.
 *  Usage (reference/tests/): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s31_r423_unit.cjs */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 70) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function extractAll(code) {
  const base = corpus.mdir(MODS, code);
  const docs = [];
  for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
    const buf = fs.readFileSync(path.join(base, name));
    docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
  }
  return docs;
}
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  let fails = 0;
  for (const code of ["PNR107", "ENGS202", "TRR116", "TRR115", "TRR102"]) {
    const docs = await extractAll(code);
    for (const d of docs) {
      const before = d.doc.blocks;
      const after = DocxExtractor.PromoteTableRowMarkers(before, norm, null);
      const same = after === before;
      if (!same) fails++;
      _l(`${code}\t${d.name}\tsame-array=${same}`);
    }
  }
  const docs = await extractAll("PMT101");
  const wtDoc = docs.find((d) => /Writers Template/.test(d.name));
  const before = wtDoc.doc.blocks.length;
  const run = new ConversionRun({ imageMode: "P" });
  const beforeWt = DocxExtractor.LooksLikeWritersTemplate(wtDoc.doc.blocks, norm);
  const after = DocxExtractor.PromoteTableRowMarkers(wtDoc.doc.blocks, norm, run);
  const afterWt = DocxExtractor.LooksLikeWritersTemplate(after, norm);
  _l(`PMT101\tblocks ${before} -> ${after.length}\tWT before=${beforeWt} after=${afterWt}\tnotes=${(run.notes || []).length}`);
  const promoted = after.filter((b) => b.kind === "para" && /RED TEXT/.test(b.text) && !wtDoc.doc.blocks.includes(b));
  for (const p of promoted) _l(`  promoted: «${clip(p.text)}» wtPage=${p.wtPage}`);
  const tables = after.filter((b) => b.kind === "table").map((b) => `${b.rows.length}x${Math.max(...b.rows.map((r) => r.length))}`);
  _l(`  tables after: ${tables.join(", ")}`);
  if (!afterWt || promoted.length !== 9) fails++;
  // the run: fresh docs (PrepareRun mutates), through the shared prep + assembly
  const docs2 = await extractAll("PMT101");
  const run2 = new ConversionRun({ imageMode: "P" });
  const prep = ModuleResolver.PrepareRun({ docs: docs2, run: run2, normaliser: norm });
  _l(`PrepareRun ok=${prep.ok} reason=${prep.reason || "-"} moduleCode=${run2.moduleCode} mtkFlag=${run2.mtkFlag} reoMode=${run2.resolvedRules && run2.resolvedRules.reoMode}`);
  if (!prep.ok) { fails++; }
  else {
    try {
      await PageAssembler.AssembleModule(run2, norm);
      const pages = run2.pages || run2.outputs || [];
      _l(`assembled pages: ${pages.length}`);
      for (const p of pages) _l(`  ${p.filename || p.name || "?"}\t${(p.html || "").length} bytes\t${clip(p.title || p.label || "", 50)}`);
    } catch (e) { _l(`ASSEMBLE ERROR ${e && e.stack}`); fails++; }
  }
  _l(`notes: ${(run2.notes || []).filter((n) => /round 423|promoted/.test(n.text || n.message || "")).map((n) => n.text || n.message).join(" | ")}`);
  _l(fails ? `FAIL ${fails}` : "UNIT OK");
  process.exit(fails ? 1 : 0);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
