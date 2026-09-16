/** _r351_debug.cjs — ROUND 351 diagnostic: for every 3+-column dragAndDrop table bundle of the named modules, replays the
 *  #dragAndDropColumn fences and prints which one fires (the builder itself returns null silently). Never imported. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests"), GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
  let cur = "?";
  InteractiveBuilder.Build = function (args) {
    const b = args?.bundle; let out, err = null;
    try { out = origBuild(args); } catch (e) { err = e; out = null; }
    if (b?.type === "dragAndDrop" && (b.tables || []).length === 1 && (b.tables[0].rows || []).length && Math.max(...b.tables[0].rows.map((r) => r.length)) >= (+process.env.MINW || 3)) {
      _l(`== ${cur} #${b.index} built=${out != null} err=${err ? err.message : ""} extra=${(b.extraTypes || []).length} media=${(b.media || []).length}`);
      const rows = b.tables[0].rows; const cfg = args.templates.dragAndDrop.column;
      const txt = (c) => String(c ?? "").replace(RED, "").replace(/\s+/g, " ").trim();
      const width = Math.max(...rows.map((r) => r.length)); const hdr = rows[0];
      _l("   header len", hdr.length, "width", width, hdr.map((c) => `${txt(c).split(/\s+/).length}w${/\[RED TEXT\]/.test(String(c)) ? "R" : ""}${new RegExp(cfg.header_reject_pattern, "i").test(txt(c)) ? "REJ" : ""}${/\[[^\]]*\]/.test(txt(c)) ? "TAG" : ""}`).join(" | "));
      const split = new RegExp(cfg.item_split_pattern); const cols = Array.from({ length: width }, () => []);
      for (const r of rows.slice(1)) {
        if (r.length > width) _l("   ragged wide row");
        for (let c = 0; c < r.length; c++) {
          const raw = String(r[c] ?? ""); if (/\[RED TEXT\]/.test(raw)) _l("   RED cell", c);
          const t = txt(raw); if (!t) continue;
          if (/https?:\/\//.test(t)) _l("   URL cell"); if (/\[[^\]]*\]/.test(t)) _l("   TAG cell", c, t.slice(0, 60));
          for (const p of t.split(split)) { const it = p.trim(); if (it) cols[c].push(it); }
        }
      }
      const all = cols.flat(); const dup = all.filter((x, i) => all.findIndex((y) => y.toLowerCase() === x.toLowerCase()) !== i);
      _l("   items", all.length, "cols with items", cols.filter((c) => c.length).length, "dups", JSON.stringify(dup).slice(0, 200));
      _l("   members:", (b.memberItems || []).map((m) => `${m.type}${m.tag ? ":" + m.tag : ""}${m.parse ? "<" + (m.parse.class || "") + (m.parse.instructionFragment ? "/frag" : "") + " " + (m.parse.primary?.tag || "-") + ">" : ""}${m.text && String(m.text).replace(RED, "").trim() ? "(" + String(m.text).replace(RED, "").trim().slice(0, 30) + ")" : ""}${m.blackAfter && String(m.blackAfter).trim() ? "{" + String(m.blackAfter).trim().slice(0, 30) + "}" : ""}`).join(" · "));
    }
    return out;
  };
  for (const code of process.argv.slice(2)) {
    cur = code; const base = corpus.mdir(GOLD, code);
    const run = new ConversionRun({ imageMode: "P" }); const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
    if (!prep.ok) { _l(code + " prep refused"); continue; }
    await PageAssembler.AssembleModule(run, norm);
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
