/** _s31_r1_rowmarkers.cjs — session 31 Round 1 MEASURE (the PMT101 class).
 *  Over EVERY Writers Template docx in the gold corpus (552 dirs, never compare_set):
 *   (a) how the normaliser resolves the page / lesson boundary markers (the canonical names a
 *       data rule must list);
 *   (b) every TABLE ROW whose non-empty cells are ONLY a red span resolving to such a marker
 *       ("a marker-only row") — per module: rows, the markers, whether the module has a Claude dir,
 *       whether LooksLikeWritersTemplate accepts it today;
 *   (c) the same rows split into "cell 0 only" vs "every cell" so the promotion rule can be scoped.
 *  Usage (reference/tests/):  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s31_r1_rowmarkers.cjs
 *  Output: outputs/_s31_r1_rowmarkers.out (+ stdout summary). */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const CLAUDE = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const OUT = path.join(__dirname, "_s31_r1_rowmarkers.out");
const TEMPLATES = ["Standard", "Inquiry", "Fundamentals", "Bilingual"];
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const clip = (s, n = 60) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const PROBE_TAGS = ["[MODULE CONTENT: PAGE 1]", "[MODULE CONTENT: PAGE 2]", "[END OF PAGE]", "[END PAGE]",
  "[LESSON 1 CONTENT]", "[LESSON 2 CONTENT]", "[END OF DROPDOWN MENU]", "[END OF DROP DOWN MENU]",
  "[Content for DROP DOWN MENU]", "[END OF MODULE]", "[TITLE BAR]", "[Fundamental content]", "[Fundamental 1 code]"];
const lines = [];
function claudeDirs() {
  const set = new Set();
  for (const t of TEMPLATES) {
    const d = path.join(CLAUDE, t); if (!fs.existsSync(d)) continue;
    for (const c of fs.readdirSync(d)) set.add(c);
  }
  return set;
}
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  lines.push("== (a) how the boundary markers resolve ==");
  for (const t of PROBE_TAGS) {
    const p = norm.Parse(t);
    lines.push(`${t}\t-> tag=${p.primary ? p.primary.tag : "-"}\tdirective=${p.primary ? p.primary.directive : "-"}\tclass=${p.class}`);
  }
  const have = claudeDirs();
  const perModule = [];
  let modules = 0, wtDocs = 0;
  for (const t of TEMPLATES) {
    const tdir = path.join(MODS, t); if (!fs.existsSync(tdir)) continue;
    for (const code of fs.readdirSync(tdir).sort()) {
      const base = path.join(tdir, code);
      let names; try { names = fs.readdirSync(base); } catch { continue; }
      const docx = names.filter((f) => f.endsWith(".docx"));
      if (!docx.length) continue;
      modules++;
      for (const name of docx) {
        const buf = fs.readFileSync(path.join(base, name));
        let doc; try { doc = await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))); } catch (e) { lines.push(`${code}\t${name}\tEXTRACT ERROR ${e && e.message}`); continue; }
        const isWt = DocxExtractor.LooksLikeWritersTemplate(doc.blocks, norm);
        // count marker-only rows in every table
        const rows = [];
        let tables = 0;
        for (const b of doc.blocks) {
          if (b.kind !== "table") continue;
          tables++;
          for (const row of (b.rows ?? [])) {
            if (!Array.isArray(row)) continue;
            const cells = row.map((c) => String(c ?? "").trim());
            const nonEmpty = cells.filter((c) => c.length);
            if (!nonEmpty.length) continue;
            const marks = [];
            let allMarker = true;
            for (const c of nonEmpty) {
              const ms = [...c.matchAll(RED)];
              const rest = c.replace(RED, "").replace(/[\s*_]/g, "");
              if (ms.length !== 1 || rest.length) { allMarker = false; break; }
              const p = norm.Parse(ms[0][1]).primary;
              if (!p) { allMarker = false; break; }
              marks.push(`${p.tag}/${p.directive}`);
            }
            if (allMarker) rows.push({ cells: nonEmpty.length, marks: marks.join("+"), text: clip(nonEmpty[0], 50) });
          }
        }
        if (rows.length || !isWt) {
          const isMedia = /media list/i.test(name);
          if (!isMedia) wtDocs++;
          perModule.push({ code, t, name, isWt, hasClaude: have.has(code), tables, rows });
        }
      }
    }
  }
  lines.push(`\n== (b) marker-only table rows — modules scanned ${modules} ==`);
  const byMark = new Map();
  for (const m of perModule) {
    if (!m.rows.length) continue;
    const marksCount = new Map();
    for (const r of m.rows) marksCount.set(r.marks, (marksCount.get(r.marks) || 0) + 1);
    lines.push(`${m.code}\t${m.t}\t${m.name}\tWT=${m.isWt}\tclaude=${m.hasClaude}\ttables=${m.tables}\tmarkerRows=${m.rows.length}\t${[...marksCount].map(([k, v]) => `${k}×${v}`).join(", ")}`);
    for (const r of m.rows) byMark.set(r.marks, (byMark.get(r.marks) || 0) + 1);
  }
  lines.push(`\n== (c) marker kinds over all marker-only rows ==`);
  for (const [k, v] of [...byMark].sort((a, b) => b[1] - a[1])) lines.push(`${k}\t${v}`);
  lines.push(`\n== (d) docx NOT accepted as a Writers Template today ==`);
  for (const m of perModule) if (!m.isWt) lines.push(`${m.code}\t${m.t}\t${m.name}\tclaude=${m.hasClaude}\ttables=${m.tables}\tmarkerRows=${m.rows.length}`);
  fs.writeFileSync(OUT, lines.join("\n") + "\n");
  _l(`modules ${modules}; docs with marker rows or refused ${perModule.length}; written ${OUT}`);
  _l(lines.slice(0, 16).join("\n"));
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
