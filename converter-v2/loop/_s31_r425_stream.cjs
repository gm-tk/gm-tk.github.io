/** _s31_r425_stream.cjs — round 425: print the synthetic tag stream the adapter emits for an XOTP module, then the pages
 *  the splitter makes of it. Usage (reference/tests/):
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s31_r425_stream.cjs XOTPB09 XOTPG04 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const clip = (s, n = 110) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const origSplit = PageSplitter.Split.bind(PageSplitter);
  PageSplitter.Split = function (items, run, normaliser) {
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
    if (!prep.ok) { _l(`${code}: PREP ${prep.reason} ${prep.unsupported ? prep.unsupported.label : ""}`); continue; }
    _l(`--- adapted stream: ${prep.wt.doc.blocks.length} blocks (title «${clip(run.title || "", 60)}»)`);
    prep.wt.doc.blocks.forEach((b, i) => _l(`${i}\t${b.kind}\t${clip(b.text, 120)}`));
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.stack}`); }
    for (const n of (run.notes || [])) { const t = n.text || n.message || ""; if (/round 425|Activity-table|PageSplitter|end page|LESSON|menu/i.test(t)) _l(`  note[${n.level}]: ${clip(t, 200)}`); }
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
