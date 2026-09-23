/** SESSION 40 ROUND 9 (24 Sept 2026) — the JOURNAL-DEFAULT RECORDER (the r278 technique): a patched copy of ContentConverter.js
 *  in which the one line that gives a label-less button `buttons.journal_label_default` ("Go to your journal") also records the
 *  item — module, page, the tag's key, the bracket text the writer typed, its black tail and the next item's text — loaded over
 *  the live engine; every named module converts in memory. Writes nothing to the corpus. From reference/tests:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s40_r9_jdefault.cjs CODES…
 *  Prints one JDEF line per defaulted button (tab-separated).
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);
const LINE = "label = this.#buttonCanonicalLabel(label, key, run, tpl);";

async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const src = fs.readFileSync(path.join(eng.APP, "ContentConverter.js"), "utf8");
  if (src.split(LINE).length !== 2) { _l("ERR the journal-default line is not unique"); process.exit(2); }
  const rec = "if (labelDefaulted) { (globalThis.__jd = globalThis.__jd || []).push({ code: run.moduleCode, key, text: String(it.text ?? \"\"), black: String(it.blackAfter ?? \"\"), next: String(bodyItems?.[i + 1]?.text ?? bodyItems?.[i + 1]?.blackAfter ?? \"\"), nextType: bodyItems?.[i + 1]?.type ?? \"\", label, url, form: String(form).slice(0, 40), page: (typeof page !== \"undefined\" ? run.pages.indexOf(page) : -1) }); } ";
  const patched = src.replace(LINE, LINE + " " + rec);
  const tmp = path.join(__dirname, `_s40_r9_CC_patched_${process.pid}.cjs`);
  fs.writeFileSync(tmp, patched);
  Object.assign(globalThis, require(tmp));
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  for (const code of codes) {
    let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
    const run = new ConversionRun({ imageMode: "P" });
    const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
      docs.push({ name, doc: await DocxExtractor.Extract(zip) });
    }
    const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
    if (!prep.ok) continue;
    globalThis.__jd = [];
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.message}`); }
    const clip = (s) => s.replace(/\s+/g, " ").trim().slice(0, 120);
    for (const r of globalThis.__jd) _l(`JDEF\t${code}\t${r.page}\t${r.key}|${r.label}|${r.url ? "URL" : "-"}|${String(r.form ?? "").slice(0, 30)}\t${clip(r.text)}\t${clip(r.black)}\t${r.nextType}:${clip(r.next)}`);
  }
  try { fs.unlinkSync(tmp); } catch { /* keep going */ }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
