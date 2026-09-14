/** _measure_r322_mtkquiz.cjs — ROUND 322 PROBE (KB constraint 65 / CL-0082: the [MTKquiz] shell
 *  without the quiz content). For every module the r232 detector lists (outputs/_affected_mtkquiz.txt,
 *  every Writers Template corpus-wide), split its pages with the LIVE engine, scan the bundles, and for
 *  every item carrying the "mtk quiz" tag dump the ACTIVITY WINDOW around it: from the enclosing
 *  [Activity] opener (or up to 12 items back) to the activity's close / the next opener / a section or
 *  page boundary / an explicit MTK closer. Each item is classified so the corpus-wide SHAPE of the
 *  writer's quiz block can be measured before any code is written (LOOP §3 step 3).
 *  Diagnostic only; writes outputs/_r322_mtkquiz_windows.json + prints a per-marker summary line.
 *  Run from reference/tests/:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r322_mtkquiz.cjs [CODE…]
 */
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
const clip = (s, n = 90) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const fold = (s) => String(s ?? "").toLowerCase().replace(/\s+/g, " ").trim();

const hasMtk = (it) => it.type === "tag" && (it.parse?.tags ?? []).some((t) => t.tag === "mtk quiz");
const isActOpen = (it) => it.type === "tag" && (it.parse?.tags ?? []).some((t) => t.tag === "activity" && t.directive === "CONTAINER_OPEN");
const primDir = (it) => it.type === "tag" ? (it.parse?.primary?.directive ?? "-") : "-";
const primTag = (it) => it.type === "tag" ? (it.parse?.primary?.tag ?? "-") : "-";
const isClose = (it) => primDir(it) === "CONTAINER_CLOSE";
const isBoundary = (it) => ["PAGE_BOUNDARY", "SECTION_MARKER"].includes(primDir(it));
const isMtkCloser = (it) => it.type === "tag" && /^\s*\[?\s*end\b.*mtk/i.test(String(it.text ?? ""));

// classify one item in the window
function classify(it) {
  if (it.type === "table") return "TABLE";
  if (it.type === "tag") {
    const t = String(it.text ?? "");
    const f = fold(t);
    if (hasMtk(it)) return isActOpen(it) ? "MTK+ACTOPEN" : "MTK";
    if (isMtkCloser(it)) return "MTKCLOSER";
    if (isActOpen(it)) return "ACTOPEN";
    if (isClose(it)) return "CLOSE";
    if (isBoundary(it)) return "BOUNDARY";
    if (/\[\s*(correct|answer|answers|answer guide|model answer|type answer|type the answer|1 mark|\d+ marks?)\b/i.test(t) || /^\s*\[?\s*(correct|answer)/i.test(f)) return "ANSMARK";
    if (/button/i.test(primTag(it)) || /\[\s*button/i.test(t)) return "BUTTON";
    if (/^\s*\[\s*h[2-5]\s*\]/i.test(t) || /^h[2-5]$/.test(primTag(it))) return "HEADTAG";
    if (/^\s*\[\s*body\s*\]/i.test(t)) return "BODYTAG";
    return "TAG:" + primTag(it) + "/" + primDir(it);
  }
  const t = String(it.text ?? "").replace(/\*/g, "").trim();
  if (!t) return "BLANK";
  if (/^\(?\d{1,2}[.)]\s*(\(?[a-z][.)]\s*)?\S/.test(t)) return "QNUM";
  if (/^\(?[a-h][.)]\s+\S/i.test(t)) return "OPTION";
  if (/^(true|false)\b/i.test(t) && t.length < 12) return "OPTION";
  if (it.block?.type === "heading" || it.block?.style?.match?.(/heading/i)) return "HEADING";
  return "PROSE";
}
function blackText(it) { return it.type === "tag" ? String(it.blackAfter ?? "") : String(it.text ?? ""); }

async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  let codes = process.argv.slice(2);
  if (!codes.length) codes = fs.readFileSync(path.join(__dirname, "_affected_mtkquiz.txt"), "utf8").split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
  const out = [];
  for (const code of codes) {
    const dir = goldDir(code);
    if (!dir) { _l(`${code}: no gold dir`); continue; }
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(dir, name));
      const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
      docs.push({ name, doc: await DocxExtractor.Extract(zip) });
    }
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
    if (!prep.ok) { _l(`${code}: prep refused: ${prep.reason}`); continue; }
    ConventionResolver.Resolve(run);
    const stream = PageSplitter.BuildItemStream(run.wtBlocks, norm);
    const pages = PageSplitter.Split(stream, run, norm);
    for (const page of pages) {
      const label = String(page.lessonLabel ?? page.number ?? "?");
      const items = page.items ?? [];
      let bundles = [];
      try { bundles = InteractiveScanner.ScanPage(page, norm, run); } catch (e) { bundles = []; }
      for (let i = 0; i < items.length; i++) {
        const it = items[i];
        if (!hasMtk(it)) continue;
        // back to the enclosing activity opener (stop at a close/boundary/another opener)
        let s = i, openerIdx = -1;
        if (isActOpen(it)) { openerIdx = i; }
        else {
          for (let k = i - 1, seen = 0; k >= 0 && seen < 40; k--) {
            const c = items[k];
            if (isActOpen(c)) { openerIdx = k; s = k; break; }
            if (isClose(c) || isBoundary(c)) { s = k + 1; break; }
            s = k; seen++;
          }
        }
        // forward to the activity close / next opener / boundary / mtk closer
        let e = i, endKind = "EOP";
        for (let k = i + 1; k < items.length; k++) {
          const c = items[k];
          if (isMtkCloser(c)) { e = k; endKind = "MTKCLOSER"; break; }
          if (isClose(c)) { e = k; endKind = "CLOSE:" + primTag(c); break; }
          if (isActOpen(c)) { e = k - 1; endKind = "NEXTACT"; break; }
          if (isBoundary(c)) { e = k - 1; endKind = "BOUNDARY:" + primDir(c); break; }
          if (hasMtk(c)) { e = k - 1; endKind = "NEXTMTK"; break; }
          e = k;
        }
        const win = [];
        const counts = {};
        for (let k = s; k <= e; k++) {
          const c = items[k];
          const cls = classify(c);
          const side = k < i ? "B" : (k === i ? "M" : "A");
          const key = side + ":" + cls.split(":")[0];
          counts[key] = (counts[key] ?? 0) + 1;
          win.push({ idx: k, side, cls, consumedBy: c.consumedBy ?? null, red: c.type === "tag" ? clip(c.text, 80) : null, black: clip(blackText(c), 80) });
        }
        // bundle facts for a consumed marker (Path 2)
        let bund = null;
        if (it.consumedBy !== undefined && bundles[it.consumedBy]) {
          const b = bundles[it.consumedBy];
          const op = b.openerItems ?? [], mem = b.memberItems ?? [];
          const role = op.includes(it) ? "OPENER" : (mem.includes(it) ? "MEMBER" : "SPAN?");
          const memIdx = mem.map((m) => items.indexOf(m));
          const memBefore = memIdx.filter((k) => k < i).length, memAfter = memIdx.filter((k) => k > i).length;
          const ownIdx = b.activityOwner ? items.indexOf(b.activityOwner) : -1;
          bund = { id: it.consumedBy, type: b.type, extra: b.extraTypes ?? [], canonTag: b.canonTag ?? null, role, nOpener: op.length, nMember: mem.length, memBefore, memAfter, activityOwner: ownIdx >= 0 ? clip(b.activityOwner.text, 40) : null, activityId: b.activityId ?? null, built: b.built ?? null };
        }
        const rec = { code, page: label, markerIdx: i, bundle: bund, opener: openerIdx >= 0 ? clip(items[openerIdx].text, 60) : null, openerIsMarker: openerIdx === i, endKind, consumedBy: it.consumedBy ?? null, marker: clip(it.text, 100), counts, window: win };
        out.push(rec);
        const after = Object.entries(counts).filter(([k]) => k.startsWith("A:")).map(([k, v]) => k.slice(2) + "=" + v).join(" ");
        const before = Object.entries(counts).filter(([k]) => k.startsWith("B:")).map(([k, v]) => k.slice(2) + "=" + v).join(" ");
        if (bund) _l(`   BUNDLE #${bund.id} type=${bund.type}+${JSON.stringify(bund.extra)} canon=${bund.canonTag} role=${bund.role} openers=${bund.nOpener} members=${bund.nMember} (before ${bund.memBefore} / after ${bund.memAfter}) owner=${bund.activityOwner ?? "-"} actId=${JSON.stringify(bund.activityId)}`);
        _l(`${code} p${label} i${i} opener=${rec.opener === null ? "NONE" : (rec.openerIsMarker ? "SELF" : "«" + rec.opener + "»")} end=${endKind} consumed=${rec.consumedBy ?? "-"} | BEFORE ${before || "-"} | AFTER ${after || "-"} | «${clip(it.text, 60)}»`);
      }
    }
  }
  fs.writeFileSync(path.join(__dirname, "_r322_mtkquiz_windows.json"), JSON.stringify(out, null, 1));
  _l(`\n${out.length} markers written to outputs/_r322_mtkquiz_windows.json`);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
