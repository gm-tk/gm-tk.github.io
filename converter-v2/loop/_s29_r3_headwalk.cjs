/** _s29_r3_headwalk.cjs — Session 29 Round 3 PICK: every TASK-type widget bundle that captured NO table and no member
 *  beyond its own invocation, through the LIVE scanner over the given modules — what follows the invocation on the page?
 *  Walks page.items after the bundle's invocation: skips blanks, records the kind sequence (h = heading tag, p = black
 *  prose / [body], T = table, I = instruction span, X = another opener / marker / widget invocation, E = end) up to the
 *  first table or stop, max 8 items. The AGH1004 lesson-1 shape reads `h p T`: the writer's table sits behind a heading the
 *  member walk terminated on. Prints one line per bundle + a summary by (type, shape) and by shape.
 *  Usage (from reference/tests/): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s29_r3_headwalk.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);
const TASK = new Set(["dragAndDrop", "clickDrop", "selfCheck", "dropDown", "multiChoiceQuiz", "radioQuiz", "typing", "reorder", "selectionBox", "unclassified", "interactive", "flipCard", "carousel", "accordion", "tabs", "modal"]);
const clip = (s, n = 60) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const rows = [];
function kindOf(it) {
  if (!it) return "E";
  if (it.type === "table") return "T";
  if (it.type === "black") return String(it.text || "").trim() ? "p" : "";
  if (it.type !== "tag") return "?";
  const p = it.parse && it.parse.primary; const cls = it.parse && it.parse.class;
  if (!p) return cls === "instruction" || cls === "noise" ? "I" : "?";
  if (/^h[1-6]$/.test(p.tag) || p.tag === "heading") return "h";
  if (p.tag === "body" || p.tag === "list") return "p";
  if (p.directive === "INTERACTIVE" || p.directive === "CONTAINER_OPEN" || p.directive === "SECTION_MARKER" || p.directive === "PAGE_BOUNDARY" || p.directive === "CONTAINER_CLOSE") return "X";
  if (p.directive === "ELEMENT") return "e";
  return "?";
}
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
    const items = page.items || [];
    for (const b of (bundles || [])) {
      if (!TASK.has(b.type)) continue;
      const tables = (b.tables || []).length; const mem = (b.memberItems || []).length;
      if (tables > 0 || mem > 1 || b.activityOwner) continue;
      const inv = (b.memberItems && b.memberItems[0]) || items[b.startIndex];
      let i = items.indexOf(inv); if (i < 0) i = b.startIndex ?? -1; if (i < 0) continue;
      const seq = []; let j = i + 1, steps = 0, tableIdx = -1; let hText = "";
      while (j < items.length && steps < 8) {
        const k = kindOf(items[j]); j++;
        if (k === "") continue;
        steps++; seq.push(k);
        if (k === "h" && !hText) { const hi = items[j - 1]; hText = clip((hi.blackAfter || "").trim() || (hi.text || "").replace(/\[[^\]]*\]/g, ""), 60); }
        if (k === "T") { tableIdx = j - 1; break; }
        if (k === "X" || k === "?") break;
      }
      const shape = seq.join(" ") || "E";
      const tbl = tableIdx >= 0 ? items[tableIdx] : null;
      const cell0 = tbl && tbl.rows && tbl.rows[0] && tbl.rows[0][0] ? clip(typeof tbl.rows[0][0] === "string" ? tbl.rows[0][0] : (tbl.rows[0][0].text || JSON.stringify(tbl.rows[0][0])), 40) : "";
      const dims = tbl && tbl.rows ? `${tbl.rows.length}x${(tbl.rows[0] || []).length}` : "";
      rows.push({ code: curCode, page: label, type: b.type, shape, inv: clip(inv && inv.text, 50), after: clip(inv && inv.blackAfter, 30), dims, cell0, hText });
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
  for (const r of rows) _l(`${r.code}\t${r.page}\t${r.type}\t${r.shape}\t${r.dims}\t«${r.inv}»\tafter«${r.after}»\tcell0«${r.cell0}»\thead«${r.hText}»`);
  const by = new Map(), bs = new Map();
  for (const r of rows) { const k = r.type + " | " + r.shape; by.set(k, (by.get(k) || 0) + 1); bs.set(r.shape, (bs.get(r.shape) || 0) + 1); }
  _l(`SUMMARY empty task bundles ${rows.length} modules ${new Set(rows.map((r) => r.code)).size} pages ${new Set(rows.map((r) => r.code + "/" + r.page)).size}`);
  _l("BY SHAPE:"); for (const [k, v] of [...bs.entries()].sort((a, b) => b[1] - a[1])) _l(`  ${v}\t${k}`);
  _l("BY TYPE|SHAPE:"); for (const [k, v] of [...by.entries()].sort((a, b) => b[1] - a[1]).slice(0, 30)) _l(`  ${v}\t${k}`);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
