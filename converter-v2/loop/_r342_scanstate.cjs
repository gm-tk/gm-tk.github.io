// _r342_scanstate.cjs — convert one module in memory, then print the POST-SCAN item states around a needle (debug; writes nothing)
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs")); const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const [code, needle] = process.argv.slice(2);
(async () => {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const captured = [];
  const orig = InteractiveScanner.ScanPage;
  InteractiveScanner.ScanPage = function (page, normaliser, run) { const b = orig.call(this, page, normaliser, run); captured.push({ page, bundles: b }); return b; };
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const base = corpus.mdir(MODS, code); const run = new ConversionRun({ imageMode: "P" }); const docs = [];
  for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
    const buf = fs.readFileSync(path.join(base, name)); const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
    docs.push({ name, doc: await DocxExtractor.Extract(zip) });
  }
  ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] });
  await PageAssembler.AssembleModule(run, norm);
  const show = (it, j) => JSON.stringify({ j, type: it.type, text: String(it.text ?? "").slice(0, 50), blackAfter: String(it.blackAfter ?? "").slice(0, 30), primary: it.parse?.primary?.tag, dir: it.parse?.primary?.directive, consumedBy: it.consumedBy, _consumed: it._consumed, links: (it.block?.links ?? []).length });
  for (const { page, bundles } of captured) {
    const items = page.items ?? [];
    for (let i = 0; i < items.length; i++) {
      const it = items[i]; const s = JSON.stringify(it.block?.text ?? "") + JSON.stringify(it.blackAfter ?? "");
      if (s.includes(needle)) {
        _l(`--- page ${page.pageTitle ?? "?"} lesson ${page.lessonLabel ?? "?"} item ${i}; bundles ${bundles.length}`);
        for (let j = Math.max(0, i - 3); j <= Math.min(items.length - 1, i + 2); j++) _l((j === i ? ">> " : "   ") + show(items[j], j));
        for (const b of bundles) { const idx = b.memberItems.map((m) => items.indexOf(m)); if (idx.some((k) => Math.abs(k - i) <= 3) || Math.abs(b.startIndex - i) <= 3) _l("   bundle", JSON.stringify({ type: b.type, start: b.startIndex, end: b.endIndex, members: idx, built: !!b.built, _mtk: b._mtkShell })); }
      }
    }
  }
})().catch((e) => process.stdout.write("ERR " + (e && e.stack || e) + "\n"));
