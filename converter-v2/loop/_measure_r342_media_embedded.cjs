// _measure_r342_media_embedded.cjs — corpus-wide: FREE-BODY media ELEMENT items ([audio]/[video]/[embed]-family) whose words ride the
// bracket line (embedded lead) — text MediaBuilder.media never renders. One toggle state per process. Usage: node … <shard> <n> [out.json]
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const [shardS, nS, outFile] = process.argv.slice(2); const shard = +shardS, n = +nS;
const MEDIA = new Set(["audio", "video", "embed", "audio button", "audio image"]);
(async () => {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const codes = corpus.mods(MODS).sort().filter((_, i) => i % n === shard);
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
      for (const { page } of captured) for (const it of (page.items ?? [])) {
        if (it.type !== "tag" || it.consumedBy !== undefined || it._consumed) continue;
        const prim = it.parse?.primary; if (!prim || prim.directive !== "ELEMENT" || !MEDIA.has(prim.tag)) continue;
        if (it.parse.class !== "tag" || it.parse.instructionFragment) continue;
        let lead = ""; try { lead = norm.RenderText(it.text) || ""; } catch {}
        if (!lead.trim()) continue;
        const url = it.block?.links?.[0]?.target || (String(it.text ?? "") + " " + String(it.blackAfter ?? "")).match(/https?:\/\/\S+/)?.[0] || "";
        rows.push({ code, page: page.lessonLabel, tag: prim.tag, lead: lead.trim().slice(0, 70), blackAfter: String(it.blackAfter ?? "").trim().slice(0, 30), url: url.slice(0, 40), raw: String(it.text ?? "").trim().slice(0, 80) });
      }
    } catch (e) { rows.push({ code, err: String(e && e.message || e).slice(0, 80) }); }
    finally { InteractiveScanner.ScanPage = orig; }
  }
  if (outFile) fs.writeFileSync(outFile, JSON.stringify(rows));
  _l(`shard ${shard}/${n}: ${codes.length} modules, ${rows.length} free-body media elements with embedded lead text`);
})().catch((e) => process.stdout.write("ERR " + (e && e.stack || e) + "\n"));
