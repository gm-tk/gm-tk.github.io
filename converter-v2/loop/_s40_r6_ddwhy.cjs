/** Session 40 r449 — the multiChoiceQuiz DECLINE RECORDER (the r278 technique): a patched copy of InteractiveBuilder.js
 *  in which every `return null` inside #multiChoiceQuiz / #withMembers / #withMembersRead records its source line, loaded
 *  over the live engine; every module converts in memory and each mcq bundle prints its LAST verdict (a bundle can be
 *  built more than once): BUILT, the line that declined it, an EXCEPTION, or "no template" (the templates object handed
 *  to Build lacks multiChoiceQuiz), plus how many Build calls it had. Writes nothing to the corpus. From reference/tests:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s40_r449_mcqwhy.cjs CODES…
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);

async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const src = fs.readFileSync(path.join(eng.APP, "InteractiveBuilder.js"), "utf8").split("\n");
  const lineSrc = {};
  for (const fn of ["#dropDown", "#ddStream", "#withMembers", "#withMembersRead"]) {
    const start = src.findIndex((l) => l.startsWith(`\tstatic ${fn}(`));
    if (start < 0) continue;
    let end = start + 1;
    while (end < src.length && !/^\tstatic [#A-Za-z]/.test(src[end])) end++;
    for (let i = start; i < end; i++) {
      if (src[i].includes("return null")) {
        lineSrc[i + 1] = `${fn}: ` + src[i].trim().slice(0, 140);
        src[i] = src[i].replace(/return null;/g, `return (globalThis.__mcqWhy = ${i + 1}, null);`);
      }
    }
  }
  for (let i = 0; i < src.length; i++)
    if (src[i].includes("html = this.#dropDown({ bundle, tpl, renderInline, run, renderTable, renderBlock });"))
      src[i] = src[i].replace("html = this.#dropDown({ bundle, tpl, renderInline, run, renderTable, renderBlock });",
        "html = this.#dropDown({ bundle, tpl, renderInline, run, renderTable, renderBlock }); globalThis.__mcqRaw = html ? html.length : 0;");
  const tmp = path.join(__dirname, `_s40_r6_IB_patched_${process.pid}.cjs`);   // one per process — parallel shards raced on a shared copy
  fs.writeFileSync(tmp, src.join("\n"));
  Object.assign(globalThis, require(tmp));
  const IB = globalThis.InteractiveBuilder; const _orig = IB.Build; const last = new Map();
  IB.Build = function (args) {
    globalThis.__mcqWhy = null; globalThis.__mcqRaw = -1;
    const nn = args?.run?.notes?.length ?? 0;
    const r = _orig.call(this, args); const b = args && args.bundle;
    if (b && b.type === "dropDown") {
      const key = `${args.run && args.run.moduleCode}#${b.index}`;
      const err = (args?.run?.notes ?? []).slice(nn).find((x) => /Could not build/.test(x.text));
      let why;
      if (r) why = "BUILT";
      else if (globalThis.__mcqWhy != null) why = `L${globalThis.__mcqWhy} ${lineSrc[globalThis.__mcqWhy] ?? ""}`;
      else if (err) why = "EXCEPTION " + err.text.slice(0, 140);
      else if (!args.templates || !args.templates.dropDown) why = "no multiChoiceQuiz template in the templates handed to Build";
      else if (args.templates.dropDown.enabled === false) why = "template disabled";
      else why = `declined, no recorded site (builder returned ${globalThis.__mcqRaw === -1 ? "— not reached" : globalThis.__mcqRaw ? globalThis.__mcqRaw + " chars of html" : "a falsy value"})`;
      const prev = last.get(key);
      last.set(key, { n: (prev?.n ?? 0) + 1, act: b.activityId ?? "-", why, first: prev?.first ?? why });
    }
    return r;
  };
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
    try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR ${e && e.message}`); }
  }
  for (const [k, v] of last) _l(`DDWHY\t${k}\t${v.act}\t${v.why}\tcalls=${v.n}\tfirst=${v.first === v.why ? "=" : v.first.slice(0, 60)}`);
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
