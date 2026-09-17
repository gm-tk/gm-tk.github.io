/** _r361_items.cjs — ROUND 361 PICK instrumentation: the POST-SCANNER item stream of the EXPlore "Navigation with N sections"
 *  family (EXPFUN02–05). Converts each module in memory exactly as batch_convert.cjs does, then prints for every page the items
 *  whose text matches the dialect's markers (type, primary tag / directive, text, blackAfter, consumedBy, stack depth hints).
 *  Run from reference/tests/:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_r361_items.cjs CODES…  */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const all = process.argv.includes("--all");
const RX = /activity heading|[heading]|which sound|roll and record|what do you think about/i;
const clip = (s, n = 80) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  for (const code of codes) {
    const base = corpus.mdir(MODS, code);
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
      docs.push({ name, doc: await DocxExtractor.Extract(zip) });
    }
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
    if (!prep.ok) { _l(`${code}: prep refused (${prep.reason})`); continue; }
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.stack || e}`); continue; }
    _l(`\n===== ${code}: pages=${run.pages.length} page_model=${run.resolvedRules?.page_model} =====`);
    run.pages.forEach((page, pi) => {
      const items = page.items || [];
      _l(`-- page ${pi} items=${items.length} isOverview=${page.isOverview}`);
      items.forEach((it, i) => {
        const txt = `${it.text || ""} ${it.blackAfter || ""}`;
        if (!all && !RX.test(txt)) return;
        const p = it.parse?.primary;
        _l(`  [${String(i).padStart(4)}] ${String(it.type).padEnd(10)} tag=${clip(p?.tag, 14).padEnd(14)} dir=${clip(p?.directive, 16).padEnd(16)} cb=${it.consumedBy ?? "-"} links=${JSON.stringify(it.block?.links ?? []).slice(0, 110)} f=${it._inqSection ?? "-"}/${it._inqSectionConsume ? "c" : "-"} | ${clip(it.text, 70)} ‖ ${clip(it.blackAfter, 40)}`);
      });
    });
  }
}
main().catch((e) => { console.error(e); process.exit(1); });
