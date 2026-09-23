/** SESSION 40 ROUND 11 — the STOCK-CAPTION census: every MediaBuilder.image call whose picture is identified by a STOCK link
 *  (iStock / Getty / Shutterstock — the item's own hyperlink or the gathered URL) and whose output still carries a caption <p>
 *  built from the item's own words; prints the caption, its word count, whether it equals the link's anchor, and whether the
 *  module's gold ships those words (tags / comments stripped). Writes nothing. From reference/tests:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s40_r11_stockcap.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const STOCK = /istockphoto\.com|gettyimages|shutterstock/i;
const norm = (s) => String(s ?? "").replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ").replace(/&[a-z#0-9]+;/gi, " ")
  .replace(/[’‘]/g, "'").replace(/\s+/g, " ").trim().toLowerCase();
(async () => {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const tn = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  let cur = null, gold = "";
  const orig = MediaBuilder.image.bind(MediaBuilder);
  MediaBuilder.image = function (it, bodyItems, i, run) {
    const r = orig(it, bodyItems, i, run);
    try {
      const gathered = MediaBuilder.gatherFollowing(it, bodyItems, i);
      const url = it.block?.links?.[0]?.target ?? (gathered.match(/https?:\/\/[^\s\]\)"<>]+/)?.[0] ?? "");
      if (STOCK.test(url)) {
        const ps = r.filter((h) => /^<p[ >]/.test(h)).map(norm).filter(Boolean);
        for (const p of ps) {
          const anchor = norm(it.block?.links?.[0]?.text ?? "");
          _l(`STOCKCAP\t${cur}\t${p.split(" ").length}\t${anchor && anchor.includes(p) ? "anchor" : "own"}\t${gold.includes(p) ? "gold_has" : "gold_lacks"}\t${p.slice(0, 120)}`);
        }
      }
    } catch (e) { /* keep going */ }
    return r;
  };
  for (const code of process.argv.slice(2).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean)) {
    let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
    cur = code;
    gold = fs.readdirSync(base).filter((f) => f.endsWith(".html")).map((f) => norm(fs.readFileSync(path.join(base, f), "utf8"))).join(" || ");
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: tn, istockAcksFiles });
    if (!prep.ok) continue;
    try { await PageAssembler.AssembleModule(run, tn); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.message}`); }
  }
})().catch((e) => process.stdout.write("ERR " + e.stack + "\n"));
