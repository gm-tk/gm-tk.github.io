/** _s31_r424_attable.cjs — round 424 MEASURE + unit: over EVERY docx in the gold corpus (762), which documents the
 *  activity-table detector fires on (must be exactly the 12 XOTP Writers Templates), and for those, what PrepareRun
 *  now returns (reason / label / moduleCode). Also: PrepareRun's reason for every docx it refused BEFORE this round
 *  (the (d) list of _s31_r1_rowmarkers.out) so the change is fully enumerated.
 *  Usage (reference/tests/): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s31_r424_attable.cjs
 *  Output: outputs/_s31_r424_attable.out */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const OUT = path.join(__dirname, "_s31_r424_attable.out");
const TEMPLATES = ["Standard", "Inquiry", "Fundamentals", "Bilingual"];
const lines = [];
async function extract(p) {
  const buf = fs.readFileSync(p);
  return DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength)));
}
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  let docx = 0, fired = [];
  const perModule = new Map();
  for (const t of TEMPLATES) {
    const tdir = path.join(MODS, t); if (!fs.existsSync(tdir)) continue;
    for (const code of fs.readdirSync(tdir).sort()) {
      const base = path.join(tdir, code);
      let names; try { names = fs.readdirSync(base); } catch { continue; }
      const files = names.filter((f) => f.endsWith(".docx"));
      if (!files.length) continue;
      const docs = [];
      for (const name of files) {
        docx++;
        let doc; try { doc = await extract(path.join(base, name)); } catch (e) { lines.push(`${code}\t${name}\tEXTRACT ERROR ${e && e.message}`); continue; }
        if (DocxExtractor.IsActivityTableDoc(doc.blocks)) fired.push(`${code}\t${t}\t${name}`);
        docs.push({ name, doc });
      }
      perModule.set(code, { t, docs });
    }
  }
  lines.push(`== docx scanned ${docx}; IsActivityTableDoc fired on ${fired.length} ==`);
  lines.push(...fired);
  lines.push("\n== PrepareRun on every module with an activity-table doc or previously refused (XOTP*, PMT101, TRR115) ==");
  for (const [code, { t, docs }] of perModule) {
    if (!/^XOTP/.test(code) && !["PMT101", "TRR115"].includes(code)) continue;
    const run = new ConversionRun({ imageMode: "P" });
    let prep;
    try { prep = ModuleResolver.PrepareRun({ docs: docs.map((d) => ({ name: d.name, doc: { ...d.doc, blocks: d.doc.blocks.slice() } })), run, normaliser: norm }); }
    catch (e) { lines.push(`${code}\tPREP THREW ${e && e.message}`); continue; }
    lines.push(`${code}\t${t}\tok=${prep.ok}\treason=${prep.reason || "-"}\tcode=${run.moduleCode}\tlabel=${prep.unsupported ? prep.unsupported.label.slice(0, 60) : "-"}`);
  }
  fs.writeFileSync(OUT, lines.join("\n") + "\n");
  _l(lines.join("\n"));
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
