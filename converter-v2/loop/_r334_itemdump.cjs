/** _r334_itemdump.cjs — ROUND 334 DIAGNOSTIC: dump a module's page item stream (type / primary tag / directive /
 *  consumedBy / text) so the inquiry-cycle delimiter shape can be read off the LIVE extractor. Writes nothing. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
function goldDir(code) {
  for (const tmpl of fs.readdirSync(GOLD)) { const tp = path.join(GOLD, tmpl, code); try { if (fs.statSync(tp).isDirectory()) return tp; } catch (e) {} }
  return null;
}
const clip = (s, n = 90) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const code = process.argv[2]; const filt = process.argv[3] ? new RegExp(process.argv[3], "i") : null;
  const dir = goldDir(code);
  const run = new ConversionRun({ imageMode: "P" });
  const docs = [];
  for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
    const buf = fs.readFileSync(path.join(dir, name));
    const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
    docs.push({ name, doc: await DocxExtractor.Extract(zip) });
  }
  const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
  if (!prep.ok) { _l("prep refused: " + prep.reason); return; }
  ConventionResolver.Resolve(run);
  const stream = PageSplitter.BuildItemStream(run.wtBlocks, norm);
  const pages = PageSplitter.Split(stream, run, norm);
  _l(`RUN code=${run.moduleCode} bodyClass=<<${run.resolvedRules?.body_class}>> pageModel=<<${run.resolvedRules?.page_model}>> pages=${pages.length}`);
  for (const page of pages) {
    const items = page.items ?? [];
    _l(`\n##### PAGE ${page.lessonLabel ?? page.number} -- ${items.length} items`);
    items.forEach((it, i) => {
      const t = String(it.text ?? "");
      if (filt && !filt.test(t) && !filt.test(String(it.blackAfter ?? ""))) return;
      const p = it.parse?.primary;
      _l(`  ${String(i).padStart(3)} ${it.type.padEnd(6)} tag=${(p?.tag ?? "-").padEnd(16)} dir=${(p?.directive ?? "-").padEnd(14)} cls=${it.parse?.class ?? "-"} consumed=${it.consumedBy ?? "-"} «${clip(t)}»${it.blackAfter ? ` after=«${clip(it.blackAfter, 60)}»` : ""}`);
    });
  }
}
main().catch((e) => { console.error(e); process.exit(1); });
