/** _s29_r4_dbg.cjs — why did #headingTableOwner not fire on an OWNED empty bundle? Prints the fields the rule tests. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2);
const clip = (s, n = 50) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
  let cur = "";
  InteractiveScanner.ScanPage = function (page, normaliser, run) {
    const bundles = origScan(page, normaliser, run); const items = page.items || [];
    for (const b of bundles || []) {
      if (!["dragAndDrop", "multiChoiceQuiz", "reorder", "selectionBox"].includes(b.type)) continue;
      if ((b.tables || []).length) continue;
      const inv = b.memberItems && b.memberItems[0];
      const o = b.activityOwner;
      const nxt = items[b.endIndex];
      const seq = items.slice(b.endIndex, b.endIndex + 6).map((x) => x.type === "tag" ? (x.parse?.primary ? x.parse.primary.tag + "/" + x.parse.primary.directive : "noprim:" + x.parse?.class) + (x.consumedBy !== undefined ? "!" : "") : x.type + (x.type === "black" && !String(x.text || "").trim() ? "(blank)" : "") + (x.consumedBy !== undefined ? "!" : "")).join(" > ");
      _l(`${cur} ${page.lessonLabel} ${b.type} inv«${clip(inv && inv.text)}» members=${(b.memberItems || []).length} extra=${JSON.stringify(b.extraTypes || [])} owner=${o ? "«" + clip(o.text || "(syn)") + "» tail«" + clip(o.blackAfter) + "» id=" + b.activityId : "none"} lead=[${(b.activityLeadItems || []).map((x) => x.type === "tag" ? (x.parse?.primary?.tag || "?") : x.type).join(",")}] seq=${seq} next=${nxt ? nxt.type + ":" + (nxt.parse?.primary?.tag || "") + (nxt.consumedBy !== undefined ? "!" : "") : "END"}`);
    }
    return bundles;
  };
  for (const code of codes) {
    cur = code;
    const base = corpus.mdir(MODS, code);
    const run = new ConversionRun({ imageMode: "P" }); const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm }); if (!prep.ok) continue;
    await PageAssembler.AssembleModule(run, norm);
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
