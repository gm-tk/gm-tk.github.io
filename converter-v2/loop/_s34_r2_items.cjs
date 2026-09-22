/** _s34_r2_items.cjs — dump a module's page item stream (type / primary tag / directive / class / text / blackAfter / consumedBy)
 *  for the pages whose label matches ITEMS_PAGE (default "1"). Usage (reference/tests/):
 *    ITEMS_PAGE=1.0 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s34_r2_items.cjs FRFUN06 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const WANT = process.env.ITEMS_PAGE || "1";
const clip = (s, n = 70) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const out = [];
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
  InteractiveScanner.ScanPage = function (page, normaliser, run) {
    const bundles = origScan(page, normaliser, run);
    const label = String(page?.lessonLabel ?? page?.label ?? "?");
    if (WANT === "*" || String(label).startsWith(WANT)) {
      out.push(`=== page ${label} isOverview=${page.isOverview} items ${(page.items || []).length}`);
      (page.items || []).forEach((it, i) => {
        if (it.type === "tag") {
          const p = it.parse && it.parse.primary;
          out.push(`${i}\ttag\t${p ? p.tag : "?"}\t${p ? p.directive : ""}\t${it.parse && it.parse.class}\t«${clip(it.text, 60)}»\tafter«${clip(it.blackAfter, 40)}»\tconsumed=${it.consumedBy !== undefined}`);
        } else if (it.type === "table") {
          const rows = (it.block && it.block.rows) || it.rows || [];
          out.push(`${i}\ttable\t${rows.length}x${Math.max(0, ...rows.map((r) => (r || []).length))}\t«${rows.slice(0, 3).map((r) => (r || []).map((c) => clip(c, 14)).join("|")).join(" // ")}»\tconsumed=${it.consumedBy !== undefined}`);
        } else {
          out.push(`${i}\t${it.type}\t«${clip(it.text, 70)}»\tconsumed=${it.consumedBy !== undefined}`);
        }
      });
    }
    return bundles;
  };
  for (const code of codes) {
    let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
    if (!prep.ok) { out.push(`${code}: PREP FAILED`); continue; }
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { out.push(`${code}: ASSEMBLE ERROR ${e && e.message}`); }
  }
  for (const l of out) _l(l);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
