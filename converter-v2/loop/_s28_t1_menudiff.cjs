/** _s28_t1_menudiff.cjs — diff the re-mined Menu_Scaffold_Registry against the pre-rebuild snapshot:
 *  groups added / removed / value-changed, series added / removed / value-changed, legacy tiers identical? */
"use strict";
const fs = require("fs"), path = require("path");
const DATA = path.join(__dirname, "..", "..", "pageforge-site", "converter-v2", "data");
const pre = JSON.parse(fs.readFileSync(path.join(__dirname, "_s28_t1_pre", "Menu_Scaffold_Registry.json"), "utf8"));
const post = JSON.parse(fs.readFileSync(path.join(DATA, "Menu_Scaffold_Registry.json"), "utf8"));
const val = (g) => g ? `${g.overview}/${g.lesson}` : "∅";
function diffTier(name, a, b) {
  const added = [], removed = [], changed = [];
  for (const k of Object.keys(b)) if (!(k in a)) added.push(`${k}=${val(b[k])}`);
  for (const k of Object.keys(a)) if (!(k in b)) removed.push(`${k}=${val(a[k])}`);
  for (const k of Object.keys(a)) if (k in b && val(a[k]) !== val(b[k])) changed.push(`${k}: ${val(a[k])} → ${val(b[k])}` + (b[k]._evidence ? `  ev ov=${JSON.stringify(b[k]._evidence.overview)} le=${JSON.stringify(b[k]._evidence.lesson)}` : ""));
  console.log(`\n== ${name}: pre ${Object.keys(a).length} / post ${Object.keys(b).length} — added ${added.length}, removed ${removed.length}, CHANGED ${changed.length}`);
  if (changed.length) console.log("  CHANGED:\n   " + changed.join("\n   "));
  if (removed.length) console.log("  removed: " + removed.join(", "));
  if (added.length) console.log("  added: " + added.join(", "));
}
diffTier("groups", pre.groups, post.groups);
diffTier("series", pre.series, post.series);
console.log("\nlegacy_groups identical:", JSON.stringify(pre.legacy_groups) === JSON.stringify(post.legacy_groups),
  " legacy_series identical:", JSON.stringify(pre.legacy_series) === JSON.stringify(post.legacy_series),
  " global_default identical:", JSON.stringify(pre.global_default) === JSON.stringify(post.global_default));
