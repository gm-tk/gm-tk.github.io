/** _s28_t3_dbg.cjs — convert ONE module in memory and print the resolved page-shell fields + the dialect notes + the item
 *  types around the tile markers. Usage (reference/tests, WSL): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s28_t3_dbg.cjs WJFUN106 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const code = process.argv[2];
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const tp = DataService.Data.EmitTemplates.body_region.fundamentals_panels.tile_pages;
  _l("tile_pages cfg present:", !!tp, "enabled:", tp && tp.enabled, "groups:", tp && Object.keys(tp.registry.groups));
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const base = corpus.mdir(MODS, code);
  const run = new ConversionRun({ imageMode: "P" });
  const docs = [];
  for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
    const buf = fs.readFileSync(path.join(base, name));
    const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
    docs.push({ name, doc: await DocxExtractor.Extract(zip) });
  }
  const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
  _l("prep ok:", prep.ok, "| template_phase:", run.resolvedRules?.template_phase, "| page_model:", run.resolvedRules?.page_model, "| body_class:", run.resolvedRules?.body_class, "| path:", run.resolutionPath);
  // parse a few markers directly
  for (const t of ["[Tile 1 content] ", "[Tile 2] ", "[Learning intention for tile] ", "[RHS side tab navigation: for all pages/tiles] "]) {
    const p = norm.Parse(t); _l(JSON.stringify(t), "-> folded:", JSON.stringify(p.folded), "primary:", p.primary && p.primary.tag, "directive:", p.primary && p.primary.directive);
  }
  try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l("ASSEMBLE ERROR", e && e.stack || e); }
  for (const n of run.notes) if (/dialect|tile|Tile|panel|Level/i.test(n.text)) _l(`note[${n.level}] ${n.stage}: ${n.text.slice(0, 200)}`);
  _l("outputs:", run.outputs.map((o) => o.filename).join(" "));
  if (run._levelMenu) _l("levelMenu:", JSON.stringify({ module: { li: run._levelMenu.module.li && { label: run._levelMenu.module.li.label, lead: run._levelMenu.module.li.lead, n: run._levelMenu.module.li.bullets.length, tail: run._levelMenu.module.li.tail }, sc: run._levelMenu.module.sc && { label: run._levelMenu.module.sc.label, n: run._levelMenu.module.sc.bullets.length, tail: run._levelMenu.module.sc.tail } }, levels: run._levelMenu.levels.map((l) => ({ label: l.label, li: [l.li.lead, l.li.bullets.length], sc: [l.sc.lead, l.sc.bullets.length] })) })); else _l("levelMenu: none");
  const html = (run.outputs.find((o) => /_0_0\.html$/.test(o.filename)) || {}).content || "";
  _l("fundamentalsPanel count:", (html.match(/class="fundamentalsPanel"/g) || []).length, "| phases nav:", /class="phases"/.test(html), "| phaseLink:", (html.match(/phaseLink/g) || []).length, "| tab-panes:", (html.match(/tab-pane"/g) || []).length, "| shape-n flags:", (html.match(/Orphan sub-tag \[shape n\]/g) || []).length);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
// appended: dump the captured menu buckets
const _origMain = main;
