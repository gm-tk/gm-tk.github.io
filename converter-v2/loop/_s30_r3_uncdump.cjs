/** _s30_r3_uncdump.cjs — Session 30 Round 3 PICK: every UNCLASSIFIED (generic-tag) widget bundle that holds exactly one table,
 *  through the LIVE scanner: code, page, the invocation text, the table dims, the first row's cells and the first data row's cells
 *  (TSV) — so the gold's widget for the same cells can be looked up. Usage (reference/tests/):
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s30_r3_uncdump.cjs CODES… > out.tsv */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);
const TYPES = new Set((process.env.UNC_TYPES || "unclassified,interactive").split(","));
const clip = (s, n = 60) => String(s ?? "").replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "").replace(/\s+/g, " ").trim().slice(0, n);
const out = [];
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
      if (!TYPES.has(b.type)) continue;
      const tables = b.tables || [];
      if (tables.length !== 1) continue;
      const rows = (tables[0].rows || []).filter((r) => Array.isArray(r));
      const w = Math.max(0, ...rows.map((r) => r.length));
      const inv = (b.openerItems && b.openerItems[0]) || (b.memberItems && b.memberItems[0]);
      const r0 = (rows[0] || []).map((c) => clip(c, 40)).join(" | ");
      const r1 = (rows[1] || []).map((c) => clip(c, 40)).join(" | ");
      const red = rows.reduce((n, r) => n + r.filter((c) => /\[RED TEXT\]/.test(String(c))).length, 0);
      const urls = rows.reduce((n, r) => n + r.filter((c) => /https?:\/\//.test(String(c))).length, 0);
      const redRows = rows.map((r, i) => (r.some((c) => /\[RED TEXT\]/.test(String(c))) ? i : -1)).filter((i) => i >= 0).join(",");
      const stripRed = (c) => String(c ?? "").replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "").trim();
      const boldRow0 = (rows[0] || []).length && (rows[0] || []).every((c) => !stripRed(c) || /^\*\*[\s\S]*\*\*$/.test(stripRed(c))) ? "bold0" : "";
      // the r69 text form's other tests on the data rows (rows after a header row): distinct answers, no url / red
      const dataRows = rows.slice(1).filter((r) => r.length === 2 && stripRed(r[0]) && stripRed(r[1]));
      const distinct = new Set(dataRows.map((r) => stripRed(r[1]).toLowerCase())).size === dataRows.length ? "distinct" : "dupes";
      out.push([curCode, label, b.type, `${rows.length}x${w}`, red, urls, clip(inv && inv.text, 50), clip(inv && inv.blackAfter, 50), r0, r1, (b.memberItems || []).length, JSON.stringify(b.extraTypes || []), redRows, boldRow0, distinct, dataRows.length].join("\t"));
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
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { out.push(`${code}\tASSEMBLE ERROR ${e && e.message}`); }
  }
  for (const l of out) _l(l);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
