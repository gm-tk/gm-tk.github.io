/** _r354_probe.cjs — ROUND 354 in-memory A/B probe (the r353 probe, unchanged mechanics; toggle TAGWORDSNOTE_OFF). Converts each module exactly as batch_convert.cjs
 *  does (no disk writes), compares every output page to the page on disk (01-Claude_Modules_), and
 *  prints per module: pages identical / changed, and for each changed page a compact diff (removed
 *  lines '-' / added lines '+', clipped). Run twice from reference/tests/:
 *    TAGWORDSNOTE_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_r354_probe.cjs CODES…   (expect: all identical)
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_r354_probe.cjs CODES…                     (the round's diffs)
 *  With --quiet only the summary lines print. Writes nothing.
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const OUT = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const quiet = process.argv.includes("--quiet");
const saveIx = process.argv.indexOf("--save");
const saveDir = saveIx >= 0 ? process.argv[saveIx + 1] : null;   // write every ON page here (scratch inspection)
const codes = process.argv.slice(2).filter((a, k, arr) => !a.startsWith("--") && arr[k - 1] !== "--save")
  .map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);   // CRLF-safe when the list comes from a Windows file
const clip = (s, n = 110) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);

function diffLines(a, b) {
  // a tiny LCS-free diff: report lines only in a (removed) and only in b (added), in order, using a multiset
  const A = a.split("\n"), B = b.split("\n");
  const cnt = new Map();
  for (const l of A) cnt.set(l, (cnt.get(l) ?? 0) + 1);
  const added = [];
  for (const l of B) { const c = cnt.get(l) ?? 0; if (c > 0) cnt.set(l, c - 1); else added.push(l); }
  const cnt2 = new Map();
  for (const l of B) cnt2.set(l, (cnt2.get(l) ?? 0) + 1);
  const removed = [];
  for (const l of A) { const c = cnt2.get(l) ?? 0; if (c > 0) cnt2.set(l, c - 1); else removed.push(l); }
  return { removed, added };
}

async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  let totIdent = 0, totChanged = 0, totMissing = 0; const changedPages = [];
  for (const code of codes) {
    let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { _l(`${code}: no gold dir (mdir → ${base})`); continue; }
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
      docs.push({ name, doc: await DocxExtractor.Extract(zip) });
    }
    const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f))
      .map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
    if (!prep.ok) { _l(`${code}: prep refused (${prep.reason})`); continue; }
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.stack || e}`); continue; }
    let outDir; try { outDir = corpus.mdir(OUT, code); } catch { outDir = null; }
    let ident = 0, changed = 0, missing = 0;
    for (const o of run.outputs) {
      if (!/\.html$/.test(o.filename)) continue;
      if (saveDir) { const d = path.join(saveDir, code); fs.mkdirSync(d, { recursive: true }); fs.writeFileSync(path.join(d, o.filename), o.content); }
      const p = outDir ? path.join(outDir, o.filename) : null;
      if (!p || !fs.existsSync(p)) { missing++; continue; }
      const disk = fs.readFileSync(p, "utf8");
      if (disk === o.content) { ident++; continue; }
      changed++; changedPages.push(`${code}/${o.filename}`);
      if (!quiet) {
        const d = diffLines(disk, o.content);
        _l(`  ~ ${o.filename}: -${d.removed.length} +${d.added.length}`);
        for (const l of d.removed.slice(0, 40)) _l(`     - ${clip(l)}`);
        if (d.removed.length > 40) _l(`     - … ${d.removed.length - 40} more removed`);
        for (const l of d.added.slice(0, 20)) _l(`     + ${clip(l)}`);
        if (d.added.length > 20) _l(`     + … ${d.added.length - 20} more added`);
      }
    }
    totIdent += ident; totChanged += changed; totMissing += missing;
    _l(`${code}: identical ${ident} / changed ${changed}${missing ? ` / missing-on-disk ${missing}` : ""}`);
  }
  _l(`\nTOTAL: identical ${totIdent} / changed ${totChanged} / missing ${totMissing} over ${codes.length} modules`);
  if (changedPages.length) _l("CHANGED: " + changedPages.join(" "));
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
