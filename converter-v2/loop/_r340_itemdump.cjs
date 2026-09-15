/** _r340_itemdump.cjs — dump the item stream around a video id for a module (debug; writes nothing). */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const [code, needle] = process.argv.slice(2);
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const base = corpus.mdir(MODS, code);
  const run = new ConversionRun({ imageMode: "P" }); const docs = [];
  for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
    const buf = fs.readFileSync(path.join(base, name));
    const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
    docs.push({ name, doc: await DocxExtractor.Extract(zip) });
  }
  const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
  if (!prep.ok) { _l("prep refused", prep.reason); return; }
  const items0 = PageSplitter.BuildItemStream(run.wtBlocks, norm);
  const pages = [{ pageTitle: "STREAM", items: items0 }];
  const show = (it) => JSON.stringify({ type: it.type, tag: it.text?.slice(0, 40), primary: it.parse?.primary?.tag, directive: it.parse?.primary?.directive, tags: (it.parse?.tags ?? []).map((t) => t.tag), blackAfter: String(it.blackAfter ?? it.text ?? "").slice(0, 80), links: (it.block?.links ?? []).map((l) => [l.text?.slice(0, 30), l.target?.slice(0, 60)]), consumed: it._consumed, consumedBy: it.consumedBy, bundled: it.bundled, interactive: it.interactive ? "yes" : undefined }, null, 0);
  const keysOfRun = Object.keys(run).filter((k) => Array.isArray(run[k])).map((k) => `${k}[${run[k].length}]`);
  _l("run arrays:", keysOfRun.join(" "));
  for (const pg of pages) {
    const items = pg.items ?? [];
    for (let i = 0; i < items.length; i++) {
      const it = items[i]; const s = JSON.stringify(it.block?.text ?? "") + JSON.stringify(it.blackAfter ?? "") + JSON.stringify(it.block?.links ?? []);
      if (s.includes(needle)) {
        _l(`--- page ${pg.pageTitle ?? "?"} item ${i}`);
        for (let j = Math.max(0, i - 3); j <= Math.min(items.length - 1, i + 2); j++) _l((j === i ? ">> " : "   ") + show(items[j]));
      }
    }
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); });
