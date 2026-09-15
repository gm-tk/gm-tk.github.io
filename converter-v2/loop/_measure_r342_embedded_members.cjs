// _measure_r342_embedded_members.cjs — corpus-wide: un-built bundles whose TAG members carry EMBEDDED text (words on the bracket line, blackAfter empty)
// that the inline hand-off box never dumps. Runs the real conversion in memory (one toggle state per process). Usage: node … <shard> <nshards> [out.json]
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const [shardS, nS, outFile] = process.argv.slice(2); const shard = +shardS, n = +nS;
(async () => {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const codes = corpus.mods(MODS).map((m) => (typeof m === "string" ? m : m.code)).sort().filter((_, i) => i % n === shard);
  const rows = [];
  for (const code of codes) {
    let base; try { base = corpus.mdir(MODS, code); } catch { continue; }
    const docxs = fs.readdirSync(base).filter((f) => f.endsWith(".docx")); if (!docxs.length) continue;
    const captured = []; const orig = InteractiveScanner.ScanPage;
    InteractiveScanner.ScanPage = function (page, nm, run) { const b = orig.call(this, page, nm, run); captured.push({ page, bundles: b }); return b; };
    try {
      const run = new ConversionRun({ imageMode: "P" }); const docs = [];
      for (const name of docxs) { const buf = fs.readFileSync(path.join(base, name)); const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength)); docs.push({ name, doc: await DocxExtractor.Extract(zip) }); }
      const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] }); if (!prep.ok) continue;
      await PageAssembler.AssembleModule(run, norm);
      for (const { page, bundles } of captured) for (const b of bundles) {
        if (b.built) continue;
        const hasText = (it) => String(it.type === "black" ? it.text : (it.blackAfter ?? "")).trim().length > 0;
        const members = [...(b.openerItems ?? []), ...(b.memberItems ?? [])];
        const emb = [];
        for (const m of members) {
          if (!m || m.type !== "tag" || !m.parse?.primary || m.parse.class !== "tag") continue;
          if (String(m.blackAfter ?? "").trim()) continue;
          let t = ""; try { t = norm.RenderText(m.text) || ""; } catch {}
          if (t.trim()) emb.push({ tag: m.parse.primary.tag, dir: m.parse.primary.directive, text: t.trim().slice(0, 60) });
        }
        if (!emb.length) continue;
        const nonInstr = !!(b.headingText?.trim()) || (b.tables?.length > 0) || members.some(hasText);
        rows.push({ code, page: page.lessonLabel, type: b.type, suppressed: !nonInstr, instr: (b.instructions ?? []).length, emb });
      }
    } catch (e) { rows.push({ code, err: String(e && e.message || e).slice(0, 80) }); }
    finally { InteractiveScanner.ScanPage = orig; }
  }
  if (outFile) fs.writeFileSync(outFile, JSON.stringify(rows));
  _l(`shard ${shard}/${n}: ${codes.length} modules, ${rows.length} bundles with embedded-text tag members, ${rows.filter((r) => r.suppressed).length} of them box-suppressed`);
})().catch((e) => process.stdout.write("ERR " + (e && e.stack || e) + "\n"));
