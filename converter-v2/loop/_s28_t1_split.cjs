/** _s28_t1_split.cjs — the population split for the decomposable gates after the Task-1 scoped regeneration:
 *  per-module compare_structure / body_compare rows, the 19-Sept fast-loop baseline vs the live run, split into the
 *  103 affected modules and the rest (which must be EXACT). Run under WSL from anywhere. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const BASE = path.join(__dirname, "_fastloop_baseline");
const affected = new Set(fs.readFileSync(path.join(__dirname, "_s28_t1_affected.txt"), "utf8").split(/\r?\n/).map((s) => s.trim()).filter(Boolean));
const csB = JSON.parse(fs.readFileSync(path.join(BASE, "structural_comparison.json"), "utf8"));
const csL = JSON.parse(fs.readFileSync(path.join(TESTS, "structural_comparison.json"), "utf8"));
const F = ["matched", "exact_chain", "claude_extra_container", "claude_missing_container", "row_wrap_missing"];
const byMod = (rows) => Object.fromEntries(rows.map((r) => [r.module, r]));
const B = byMod(csB), L = byMod(csL);
const sum = (rows, f) => rows.reduce((a, r) => a + (r[f] || 0), 0);
console.log("== compare_structure: baseline (19 Sept) vs live");
for (const f of F) console.log(`  ${f.padEnd(26)} ${String(sum(csB, f)).padStart(6)} → ${String(sum(csL, f)).padStart(6)}   (${sum(csL, f) - sum(csB, f) >= 0 ? "+" : ""}${sum(csL, f) - sum(csB, f)})`);
let unaffDiff = [], affDelta = {};
for (const f of F) affDelta[f] = 0;
for (const m of new Set([...Object.keys(B), ...Object.keys(L)])) {
  const b = B[m] || {}, l = L[m] || {};
  const diff = F.filter((f) => (b[f] || 0) !== (l[f] || 0));
  if (!diff.length) continue;
  if (affected.has(m)) { for (const f of F) affDelta[f] += (l[f] || 0) - (b[f] || 0); }
  else unaffDiff.push(`${m}: ${diff.map((f) => `${f} ${b[f] || 0}→${l[f] || 0}`).join(", ")}`);
}
console.log(`  UNAFFECTED modules with any moved row: ${unaffDiff.length}${unaffDiff.length ? "\n    " + unaffDiff.join("\n    ") : "  (EXACT)"}`);
console.log(`  AFFECTED modules account for: ${F.map((f) => `${f} ${affDelta[f] >= 0 ? "+" : ""}${affDelta[f]}`).join(", ")}`);
// per affected module, the EXTRA / MISSING movers
const movers = [];
for (const m of affected) { const b = B[m] || {}, l = L[m] || {}; const de = (l.claude_extra_container || 0) - (b.claude_extra_container || 0), dm = (l.claude_missing_container || 0) - (b.claude_missing_container || 0), dx = (l.exact_chain || 0) - (b.exact_chain || 0); if (de || dm) movers.push(`${m} EXTRA ${de >= 0 ? "+" : ""}${de} MISSING ${dm >= 0 ? "+" : ""}${dm} exact ${dx >= 0 ? "+" : ""}${dx}`); }
console.log("  EXTRA/MISSING movers (affected): " + (movers.join(" | ") || "none"));

// body_compare: {idx: {module, page, flags...}} shape — count per module the flagged pages
const bcB = JSON.parse(fs.readFileSync(path.join(BASE, "body_compare.json"), "utf8"));
const bcL = JSON.parse(fs.readFileSync(path.join(TESTS, "body_compare.json"), "utf8"));
const rows = (o) => Array.isArray(o) ? o : Object.values(o);
const sample = rows(bcL)[0]; console.log("\n== body_compare row keys:", Object.keys(sample || {}).join(", "));
const flagsOf = (r) => ["over_capture", "runaway", "empty_container", "empty", "overcapture", "any"].filter((k) => r[k]);
const tally = (o) => { const t = {}; for (const r of rows(o)) { const m = r.module || String(r.page || r.file || "").split(/[_./]/)[0]; const f = flagsOf(r); if (!f.length) continue; (t[m] ??= { pages: 0 }).pages++; for (const k of f) t[m][k] = (t[m][k] || 0) + 1; } return t; };
const tb = tally(bcB), tl = tally(bcL);
const un = [], af = [];
for (const m of new Set([...Object.keys(tb), ...Object.keys(tl)])) { const a = JSON.stringify(tb[m] || {}), b = JSON.stringify(tl[m] || {}); if (a === b) continue; (affected.has(m) ? af : un).push(`${m}: ${a} → ${b}`); }
console.log(`  body_compare UNAFFECTED modules moved: ${un.length}${un.length ? "\n    " + un.join("\n    ") : " (EXACT)"}`);
console.log(`  body_compare AFFECTED modules moved: ${af.length}\n    ${af.join("\n    ")}`);
