// ROUND 359 — dump the resolved module_code pattern for every module with a Claude dir (before/after the registry edit)
const fs = require("fs"), path = require("path");
const eng = require("../reference/tests/_engine_load.cjs");
const Data = eng.loadData();
globalThis.DataService = { Data, async FetchOembed() { return { ok: false }; } };
eng.loadEngine();
const CL = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const out = {};
for (const tmpl of fs.readdirSync(CL)) {
  const d = path.join(CL, tmpl); if (!fs.statSync(d).isDirectory()) continue;
  for (const code of fs.readdirSync(d)) {
    if (!fs.statSync(path.join(d, code)).isDirectory()) continue;
    const run = { moduleCode: code, notes: [], AddNote() {} };
    try { const r = ModuleResolver.Resolve(code, run); out[code] = { tmpl, module_code: r.module_code, h1_count: r.h1_count, menu_type: r.menu_type, menu_button_tooltip: r.menu_button_tooltip, footer_links: r.footer_links, footer_class: r.footer_class, body_class: r.body_class }; }
    catch (e) { out[code] = { tmpl, error: String(e) }; }
  }
}
fs.writeFileSync(process.argv[2] || path.join(__dirname, "_r336_resolved.json"), JSON.stringify(out, null, 1));
console.log("resolved", Object.keys(out).length);
