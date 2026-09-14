/** _r321_titledump.cjs — ROUND 314 DIAGNOSTIC. For a module, dump every page's bundles with the
 *  fields ContentConverter reads when it decides to CLOSE the open activity before emitting a
 *  widget bundle (isNewActivity = canonTag==='activity' || activityOwner!==undefined || activityId!==null),
 *  plus the item stream around each dropbox bundle. Diagnostic only; writes nothing. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
function goldDir(code) {
  for (const tmpl of fs.readdirSync(GOLD)) {
    const tp = path.join(GOLD, tmpl, code);
    try { if (fs.statSync(tp).isDirectory()) return tp; } catch (e) {}
  }
  return null;
}
const clip = (s, n = 70) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const code = process.argv[2]; const onlyPage = process.argv[3];
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
  _l(`RUN englishTitle=<<${run.englishTitle}>> teReoTitle=<<${run.teReoTitle}>> mtkFlag=${run.mtkFlag} bodyClass=<<${run.resolvedRules?.body_class}>>`);
  for (const page of pages) {
    const label = String(page.lessonLabel ?? page.number ?? "?");
    if (onlyPage && label !== onlyPage) continue;
    const items = page.items ?? [];
    _l(`
##### ${code} PAGE ${label} pageTitle=<<${page.pageTitle}>> -- ${items.length} items`);
    items.slice(0, 9).forEach((it, i) => { const p = it.parse?.primary; _l(`    item ${i} type=${it.type} tag=${p?.tag ?? "-"} dir=${p?.directive ?? "-"} <<${clip(String(it.text ?? ""), 80)}>> black=<<${clip(String(it.blackAfter ?? ""), 50)}>>`); });
    continue;
    const bundles = InteractiveScanner.ScanPage(page, norm, run);
    _l(`\n##### ${code} PAGE ${label} — ${items.length} items, ${bundles.length} bundles`);
    for (const b of bundles) {
      const op = b.openerItems?.[0] ?? b.memberItems?.[0];
      const opIdx = items.indexOf(op);
      const ownIdx = b.activityOwner ? items.indexOf(b.activityOwner) : -1;
      _l(`  BUNDLE type=${b.type} extra=${JSON.stringify(b.extraTypes ?? [])} canonTag=${b.canonTag} activityId=${JSON.stringify(b.activityId)} activityOwner=${b.activityOwner === undefined ? "undefined" : (ownIdx + " «" + clip(b.activityOwner.text, 40) + "»")} openerIdx=${opIdx} opener=«${clip(op?.text, 60)}» nMem=${(b.memberItems ?? []).length}`);
    }
    // item stream around dropbox-ish items
    items.forEach((it, i) => {
      const t = String(it.text ?? "");
      if (/drop\s?box|\[\s*activity|end page|end activity/i.test(t) || it.parse?.primary?.tag === "activity") {
        const p = it.parse?.primary;
        _l(`    item ${i} type=${it.type} tag=${p?.tag ?? "-"} dir=${p?.directive ?? "-"} consumedBy=${it.consumedBy ?? "-"} «${clip(t, 90)}» black=«${clip(it.blackAfter, 40)}»`);
      }
    });
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
