/** _s28_t1_convdiff.cjs — per-group diff of the Html_Convention_Registry dominants (pre snapshot vs rebuilt). */
"use strict";
const fs = require("fs"), path = require("path");
const a = JSON.parse(fs.readFileSync(path.join(__dirname, "_s28_t1_pre", "Html_Convention_Registry.json"), "utf8")).groups;
const b = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "pageforge-site", "converter-v2", "data", "Html_Convention_Registry.json"), "utf8")).groups;
const flat = (g, pre = "", out = {}) => {
  for (const [k, v] of Object.entries(g || {})) {
    if (k === "members" || k === "series_deviations") continue;
    if (v && typeof v === "object" && !Array.isArray(v)) flat(v, pre + k + ".", out); else out[pre + k] = JSON.stringify(v);
  }
  return out;
};
for (const k of Object.keys(a).sort()) {
  if (!b[k]) { console.log(`- ${k} REMOVED`); continue; }
  const fa = flat(a[k]), fb = flat(b[k]);
  const lines = [];
  for (const f of new Set([...Object.keys(fa), ...Object.keys(fb)])) if (fa[f] !== fb[f] && !/share$/.test(f)) lines.push(`${f}: ${fa[f] ?? "∅"} → ${fb[f] ?? "∅"}` + (fb[f.replace(/dominant.*$|element$|host$/, "share")] ? ` (share ${fb[f.replace(/\.(dominant\..*|element|host)$/, ".share")] ?? ""})` : ""));
  const ma = (a[k].members || []).length, mb = (b[k].members || []).length;
  const da = Object.keys(a[k].series_deviations || {}).sort().join(","), db = Object.keys(b[k].series_deviations || {}).sort().join(",");
  if (lines.length || da !== db) console.log(`~ ${k} (members ${ma} → ${mb})\n    ${lines.join("\n    ")}${da !== db ? `\n    series_deviations: [${da}] → [${db}]` : ""}`);
}
for (const k of Object.keys(b).sort()) if (!a[k]) console.log(`+ ${k} NEW (members ${(b[k].members || []).length}): ${Object.entries(flat(b[k])).filter(([f]) => /dominant|element$|host$/.test(f)).map(([f, v]) => `${f}=${v}`).join(" ")}`);
