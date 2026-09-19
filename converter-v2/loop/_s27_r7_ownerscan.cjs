/** _s27_r7_ownerscan.cjs — Session 27 Round 7: every bundle whose activityOwner span's PRIMARY tag is not `activity`
 *  (the [interactive: video] class), through the LIVE scanner over the given modules. Prints one line per such
 *  bundle: module / page / bundle type / owner primary tag+directive / the activity tag's alias word + how / the
 *  owner's text / whether the owner span is ALSO the bundle's own invocation (i.e. the widget tag itself carries the
 *  alias — never an owner problem) / the lead-item count; then a summary by (primary, alias).
 *  Usage (from reference/tests/): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s27_r7_ownerscan.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);
const clip = (s, n = 70) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const rows = [];
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  let curCode = "";
  const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
  InteractiveScanner.ScanPage = function (page, normaliser, run) {
    const label = String(page?.lessonLabel ?? page?.label ?? "?");
    const bundles = origScan(page, normaliser, run);
    for (const b of (bundles || [])) {
      const o = b.activityOwner; if (!o || o.type !== "tag" || !o.parse) continue;
      const prim = o.parse.primary; const pt = prim ? prim.tag : "null";
      if (pt === "activity") continue;
      const at = (o.parse.tags || []).find((t) => t.tag === "activity");
      const self = b.memberItems && b.memberItems.includes(o) || (b.startIndex != null && page.items && page.items[b.startIndex] === o && (b.activityLeadItems || []).length === 0 && !prim);
      rows.push({ code: curCode, page: label, type: b.type, prim: pt + "/" + (prim ? prim.directive : "-"), alias: at ? (at.raw || at.alias || "?") + "/" + at.how : "?",
        text: clip(o.text), after: clip(o.blackAfter, 40), lead: (b.activityLeadItems || []).length, id: b.activityId || "", members: (b.memberItems || []).length, tables: (b.tables || []).length });
    }
    return bundles;
  };
  for (const code of codes) {
    curCode = code;
    let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
    if (!prep.ok) continue;
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.message}`); }
  }
  for (const r of rows) _l(`${r.code}\t${r.page}\t${r.type}\t${r.prim}\t${r.alias}\tlead=${r.lead}\tid=${r.id}\tmem=${r.members}\ttbl=${r.tables}\t«${r.text}»\tafter«${r.after}»`);
  const by = new Map();
  for (const r of rows) { const k = r.prim + " | " + r.alias; by.set(k, (by.get(k) || 0) + 1); }
  _l(`SUMMARY rows ${rows.length} modules ${new Set(rows.map((r) => r.code)).size} pages ${new Set(rows.map((r) => r.code + "/" + r.page)).size}`);
  for (const [k, v] of [...by.entries()].sort((a, b) => b[1] - a[1])) _l(`  ${v}\t${k}`);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
