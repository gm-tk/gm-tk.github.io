/** _s28_t1_mine_sar.cjs — Session 28 / Task 1: mine the Style_Anchor page-level profile of every gold
 *  module of the September-intake prefixes with ReferenceMiner.Distil (the r263 SCCH / r265 CHFUN
 *  pattern), then aggregate per PREFIX: for each tracked field the value distribution across the
 *  prefix's gold modules (majority + deviators). Output: outputs/_s28_t1_mine_sar.json + a readable
 *  table on stdout. Read-only — writes nothing into data/.
 *  Run from reference/tests under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s28_t1_mine_sar.cjs [PREFIX …]
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const ROOT = path.join(__dirname, "..", "..");
const GOLD = path.join(ROOT, "01-Finalized_Modules_");

globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
const _l = console.log.bind(console); console.log = () => { }; console.warn = () => { };
eng.loadEngine(); console.log = _l;

const moveLog = fs.readFileSync(path.join(ROOT, "00-NEW_NEW_NEW", "_MOVE_LOG_2026-09-19.tsv"), "utf8")
  .split(/\r?\n/).filter((l) => l && !l.startsWith("#")).map((l) => l.split("\t"));
const wanted = new Set(process.argv.slice(2).filter((a) => !a.startsWith("--")));
const prefixOf = (c) => (c.match(/^[A-Z]+/) || [""])[0];
// every gold module whose prefix is one of the intake prefixes (so pre-existing siblings count too)
const intakePrefixes = new Set(moveLog.map(([c]) => prefixOf(c)));
const allGold = corpus.mods(GOLD);
const codes = allGold.filter((c) => intakePrefixes.has(prefixOf(c)) && (!wanted.size || wanted.has(prefixOf(c))));

const FIELDS = ["template_phase", "level_attr", "body_class", "idoc_host", "footer_class", "acknowledgements", "page_model",
  "module_code", "h1_count", "menu_type", "menu_button_tooltip", "footer_links"];
const per = {};      // code -> mined rules
const stub = { AddNote() { } };
for (const code of codes) {
  let dir; try { dir = corpus.mdir(GOLD, code); } catch { continue; }
  const files = fs.readdirSync(dir).filter((f) => /\.html?$/i.test(f)).sort()
    .map((f) => ({ name: f, text: fs.readFileSync(path.join(dir, f), "utf8") }));
  if (!files.length) { per[code] = { _pages: 0 }; continue; }
  const d = ReferenceMiner.Distil(files, stub);
  per[code] = { _pages: files.length, _tpl: path.basename(path.dirname(dir)), ...(d ? d.rules : {}), _unmined: d ? d.unmined : FIELDS };
}
const key = (v) => v == null ? "∅" : (typeof v === "object" ? JSON.stringify(v) : String(v));
const byPrefix = {};
for (const [code, r] of Object.entries(per)) {
  const p = prefixOf(code);
  const B = (byPrefix[p] ??= { codes: [], fields: {} });
  B.codes.push(code);
  for (const f of FIELDS) {
    const F = (B.fields[f] ??= {});
    const k = key(r[f]);
    (F[k] ??= []).push(code);
  }
}
const out = { generated: new Date().toISOString(), per_module: per, by_prefix: {} };
for (const p of Object.keys(byPrefix).sort()) {
  const B = byPrefix[p];
  _l(`\n=== ${p}  (${B.codes.length} gold modules: ${B.codes.join(" ")})`);
  const summary = {};
  for (const f of FIELDS) {
    const dist = Object.entries(B.fields[f]).sort((a, b) => b[1].length - a[1].length);
    const maj = dist[0];
    summary[f] = { majority: maj[0], n: maj[1].length, of: B.codes.length, deviators: dist.slice(1).map(([v, cs]) => ({ value: v, modules: cs })) };
    const dev = dist.slice(1).map(([v, cs]) => `${v} ×${cs.length} (${cs.slice(0, 4).join(",")}${cs.length > 4 ? "…" : ""})`).join(" | ");
    _l(`  ${f.padEnd(20)} ${maj[0]}  [${maj[1].length}/${B.codes.length}]${dev ? "   deviators: " + dev : ""}`);
  }
  out.by_prefix[p] = { codes: B.codes, fields: summary };
}
fs.writeFileSync(path.join(__dirname, "_s28_t1_mine_sar.json"), JSON.stringify(out, null, 1));
_l(`\nwrote outputs/_s28_t1_mine_sar.json (${codes.length} modules, ${Object.keys(byPrefix).length} prefixes)`);
