/** _s30_r2_scdump.cjs — Session 30 Round 2 PICK: dump every selfCheck bundle (opener, members, tables, media, owner) through
 *  the LIVE scanner over the given modules — the letter-grid bingo class's authoring shape.
 *  Usage (from reference/tests/): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s30_r2_scdump.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);
const WANT = process.env.SCDUMP_TYPE || "selfCheck";
const clip = (s, n = 80) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
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
      if (b.type !== WANT) continue;
      out.push(`\n=== ${curCode} page ${label} ${b.type} #${b.index} modifier="${clip(b.modifier, 40)}" extraTypes=${JSON.stringify(b.extraTypes || [])} owner=${b.activityOwner ? clip(b.activityOwner.text, 40) : "-"}`);
      const items = [...(b.openerItems || []), ...(b.memberItems || [])];
      out.push(`  items (${items.length}): openers ${(b.openerItems || []).length} / members ${(b.memberItems || []).length}`);
      for (const m of items) {
        if (!m) continue;
        if (m.type === "tag") {
          const p = m.parse && m.parse.primary;
          out.push(`    [tag ${p ? p.tag : "?"}${p && p.directive ? "/" + p.directive : ""} cls=${m.parse && m.parse.class}] text«${clip(m.text, 70)}» after«${clip(m.blackAfter, 70)}»`);
        } else if (m.type === "table") {
          const rows = m.rows || [];
          out.push(`    [table ${rows.length}x${Math.max(0, ...rows.map((r) => (r || []).length))}] ${rows.map((r) => (r || []).map((c) => clip(typeof c === "string" ? c : (c && c.text) || JSON.stringify(c), 14)).join(" | ")).join(" // ").slice(0, 300)}`);
        } else {
          out.push(`    [${m.type}] «${clip(m.text, 90)}»`);
        }
      }
      out.push(`  tables: ${(b.tables || []).length}; media: ${JSON.stringify((b.media || []).map((x) => clip(x.target || x.text, 50)))}; instructions: ${JSON.stringify((b.instructions || []).map((x) => clip(x, 60)))}`);
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
    if (!prep.ok) { out.push(`${code}: PREP FAILED`); continue; }
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { out.push(`${code}: ASSEMBLE ERROR ${e && e.message}`); }
  }
  for (const l of out) _l(l);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
