/** _s34_r428_shellprobe.cjs — ROUND 428 in-memory shell probe: converts each module with the live data (or INQFALLBACK_OFF=1),
 *  and for every output page prints the inquiry shell it built (crumb labels / panel count / body class) beside the gold's
 *  shell page (its crumb labels / panel count). Writes nothing unless --save DIR. Run from reference/tests/ under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s34_r428_shellprobe.cjs CEDK401 TWHA905 …
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const saveIx = process.argv.indexOf("--save");
const saveDir = saveIx >= 0 ? process.argv[saveIx + 1] : null;
const codes = process.argv.slice(2).filter((a, k, arr) => !a.startsWith("--") && arr[k - 1] !== "--save").map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);
const shellOf = (html) => {
  const labels = [];
  const m = /<div class="crumbs"[^>]*>([\s\S]*?)<\/div>\s*(?=<div class="inquiryPanel|<div class="row|<!--)/i.exec(html);
  if (m) for (const c of m[1].matchAll(/<div[^>]*crumb="[^"]*"[^>]*>([\s\S]*?)<\/div>/gi)) labels.push(c[1].replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim());
  const panels = (html.match(/class="inquiryPanel/g) || []).length;
  const body = (/<body[^>]*class="([^"]*)"/.exec(html) || [null, ""])[1];
  return { labels, panels, body };
};
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  for (const code of codes) {
    let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { _l(`${code}: no gold dir`); continue; }
    // the gold's shell page = the html with the most inquiryPanels
    let gold = null;
    for (const f of fs.readdirSync(base).filter((f) => /\.html$/i.test(f) && !/acks/i.test(f))) {
      const s = shellOf(fs.readFileSync(path.join(base, f), "utf8"));
      if (s.panels && (!gold || s.panels > gold.panels)) gold = { file: f, ...s };
    }
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
    if (!prep.ok) { _l(`${code}: prep refused (${prep.reason})`); continue; }
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.stack || e}`); continue; }
    _l(`== ${code}  gold ${gold ? `${gold.file}: ${gold.panels} panels [${gold.labels.join(" | ")}]` : "no shell"}`);
    for (const o of run.outputs) {
      if (!/\.html$/.test(o.filename) || /acks/i.test(o.filename)) continue;
      if (saveDir) { const d = path.join(saveDir, code); fs.mkdirSync(d, { recursive: true }); fs.writeFileSync(path.join(d, o.filename), o.content); }
      const s = shellOf(o.content);
      _l(`   ${o.filename}: ${s.panels} panels [${s.labels.join(" | ")}] body="${s.body}"`);
    }
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
