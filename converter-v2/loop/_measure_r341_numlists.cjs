/** _measure_r341_numlists.cjs — ROUND 341 PICK probe: every WORD-NUMBERED list (w:numFmt decimal…) in every WT (live extractor, all 454
 *  modules), grouped by context (the nearest preceding heading / tag text: learning intentions / success criteria vs other), paired to the
 *  gold by the first item's text; the gold's form (ol / ul / not-a-list / absent) per group and per template. Writes _r341_numlists.json. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const norm = (s) => String(s ?? "").replace(/<[^>]+>/g, " ").replace(/&[a-z#0-9]+;/g, " ").replace(/[*_]/g, "").replace(/\s+/g, " ").trim().toLowerCase();
const LI = /learning intention|success criteria|you will show|we are learning|learning outcome|by the end of|in this (lesson|module) you|you will be able|will learn|learning objectives|i can/i;
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const idx = DataService.Data.ModuleStructureIndex?.module_meta ?? {};
  const rows = [];
  for (const code of corpus.mods(MODS)) {
    let base; try { base = corpus.mdir(MODS, code); } catch { continue; }
    const docx = fs.readdirSync(base).filter((f) => f.endsWith(".docx")); if (!docx.length) continue;
    const golds = fs.readdirSync(base).filter((f) => f.endsWith(".html")).map((f) => fs.readFileSync(path.join(base, f), "utf8"));
    const goldLists = []; for (const g of golds) for (const m of g.matchAll(/<(ul|ol)[^>]*>([\s\S]*?)<\/\1>/g)) goldLists.push([m[1], norm(m[2])]);
    const goldText = norm(golds.join(" "));
    const blocks = [];
    for (const name of docx) {
      const buf = fs.readFileSync(path.join(base, name));
      const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
      const doc = await DocxExtractor.Extract(zip); for (const b of (doc.blocks ?? [])) blocks.push(b);
    }
    const meta = idx[code] ?? {};
    for (let i = 0; i < blocks.length; i++) {
      if (blocks[i].list !== "number") continue;
      let j = i; while (j + 1 < blocks.length && blocks[j + 1].list === "number") j++;
      const n = j - i + 1;
      // context: nearest preceding non-list block text
      let ctx = ""; for (let k = i - 1; k >= 0 && k >= i - 3; k--) { if (blocks[k].list) continue; ctx = String(blocks[k].text ?? ""); if (ctx.trim()) break; }
      const isLI = LI.test(ctx) || LI.test(String(blocks[i].text)) ;
      const key = norm(blocks[i].text).replace(/^\d+[.)]\s*/, "").slice(0, 30);
      let gold = "absent";
      if (key.length >= 8) { const hit = goldLists.find(([k, t]) => t.includes(key)); gold = hit ? hit[0] : (goldText.includes(key) ? "not-a-list" : "absent"); }
      rows.push({ code, template: meta.template_type ?? path.basename(path.dirname(base)), subject: meta.subject ?? "?", n, ctx: ctx.replace(/\s+/g, " ").slice(0, 60), isLI, gold, first: key });
      i = j;
    }
  }
  fs.writeFileSync(path.join(__dirname, "_r341_numlists.json"), JSON.stringify({ generated: new Date().toISOString(), rows }, null, 1));
  const tally = (label, rs) => { const c = {}; for (const r of rs) c[r.gold] = (c[r.gold] ?? 0) + 1; const f = (c.ol ?? 0) + (c.ul ?? 0); _l(`${label.padEnd(44)} n=${String(rs.length).padStart(4)} mods=${String(new Set(rs.map((r) => r.code)).size).padStart(3)} | gold ${JSON.stringify(c)} ol/found ${f ? ((c.ol ?? 0) / f).toFixed(2) : "-"}`); };
  _l(`WORD-NUMBERED lists in the WTs: ${rows.length} in ${new Set(rows.map((r) => r.code)).size} modules`);
  tally("ALL", rows);
  tally("  learning-intention context", rows.filter((r) => r.isLI)); tally("  other context", rows.filter((r) => !r.isLI));
  for (const t of ["Standard", "Bilingual", "Fundamentals", "Inquiry"]) { tally(`  ${t} — LI context`, rows.filter((r) => r.template === t && r.isLI)); tally(`  ${t} — other`, rows.filter((r) => r.template === t && !r.isLI)); }
  const subj = {}; for (const r of rows.filter((r) => r.isLI)) (subj[r.subject] ??= []).push(r);
  _l("\nLI-context by subject (n >= 3):"); for (const [s, rs] of Object.entries(subj).sort((a, b) => b[1].length - a[1].length)) if (rs.length >= 3) tally(`  ${s}`, rs);
  const ulLI = rows.filter((r) => r.isLI && r.gold === "ul"); _l(`\nLI-context gold=ul pages: ${ulLI.length} lists in ${new Set(ulLI.map((r) => r.code)).size} modules: ${[...new Set(ulLI.map((r) => r.code))].join(" ")}`);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); });
