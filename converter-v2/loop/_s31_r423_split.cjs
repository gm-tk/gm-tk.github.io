/** _s31_r423_split.cjs — trace the page splitter for a module: the boundary items in the stream and the pages produced.
 *  Usage (reference/tests/): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s31_r423_split.cjs PMT101 PNR107 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 60) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const origSplit = PageSplitter.Split.bind(PageSplitter);
  PageSplitter.Split = function (items, run, normaliser) {
    _l(`--- item stream: ${items.length} items; body_class=${run.resolvedRules && run.resolvedRules.body_class}; page_model=${run.resolvedRules && run.resolvedRules.page_model}; mtkFlag=${run.mtkFlag}`);
    items.forEach((it, i) => {
      if (it.type === "tag") {
        const p = it.parse && it.parse.primary;
        if (p && ["PAGE_BOUNDARY", "SECTION_MARKER", "CONTAINER_CLOSE"].includes(p.directive))
          _l(`${i}\ttag\t${p.tag}\t${p.directive}\tnums=${JSON.stringify(it.parse.numbers || [])}\t«${clip(it.text, 50)}»\tafter«${clip(it.blackAfter, 30)}»\twtPage=${it.block && it.block.wtPage}`);
      } else if (it.type === "table") {
        const rows = (it.block && it.block.rows) || [];
        _l(`${i}\ttable\t${rows.length}x${Math.max(0, ...rows.map((r) => (r || []).length))}\t«${clip((rows[0] || []).join(" | "), 60)}»`);
      }
    });
    const pages = origSplit(items, run, normaliser);
    _l(`--- pages: ${pages.length}`);
    for (const p of pages) _l(`  ${p.lessonLabel}\tisOverview=${p.isOverview}\titems=${p.items.length}\ttitle=«${clip(p.pageTitle, 40)}»`);
    return pages;
  };
  for (const code of process.argv.slice(2)) {
    const base = corpus.mdir(MODS, code);
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    _l(`=== ${code}`);
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
    if (!prep.ok) { _l(`${code}: PREP FAILED ${prep.reason}`); continue; }
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.message}`); }
    for (const n of (run.notes || [])) { const t = n.text || n.message || ""; if (/PageSplitter|end page|LESSON|single-file|page_model/i.test(t)) _l(`  note: ${clip(t, 160)}`); }
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
