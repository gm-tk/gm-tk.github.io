/** SESSION 40 ROUND 11 — trace one module's [Image] items as the converter sees them (type, text, blackAfter, links, the next items),
 *  filtered by a substring. From reference/tests: node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s40_r11_trace.cjs CODE "substring" */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const [code, needle] = process.argv.slice(2);
(async () => {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const base = corpus.mdir(MODS, code);
  const run = new ConversionRun({ imageMode: "P" });
  const docs = [];
  for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
    const buf = fs.readFileSync(path.join(base, name));
    docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
  }
  const orig = MediaBuilder.image.bind(MediaBuilder); let n = 0;
  MediaBuilder.image = function (it, bodyItems, i, run) {
    const r = orig(it, bodyItems, i, run);
    const all = JSON.stringify([it.text, it.blackAfter]);
    if (n < 3 && all.includes(needle)) {
      n++;
      _l("ITEM", JSON.stringify({ type: it.type, text: it.text, blackAfter: it.blackAfter, links: it.block?.links, gathered: MediaBuilder.gatherFollowing(it, bodyItems, i) }, null, 1).slice(0, 2500));
      for (let k = 1; k <= 2; k++) { const nx = bodyItems[i + k]; if (nx) _l(`NEXT${k}`, JSON.stringify({ type: nx.type, text: nx.text, blackAfter: nx.blackAfter, consumed: nx._consumed, consumedBy: nx.consumedBy }).slice(0, 600)); }
      _l("OUT", r.join("\n").slice(0, 900));
    }
    return r;
  };
  const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
  if (prep.ok) await PageAssembler.AssembleModule(run, norm);
})().catch((e) => process.stdout.write("ERR " + e.stack + "\n"));
