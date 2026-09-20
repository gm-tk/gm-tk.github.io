/** _s29_r5_shellprobe2.cjs — at which post-pass does a body-side empty `row > col` shell APPEAR? Wraps the page post-passes. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2);
const SHELL = /<div class="row">\s*<div class="col[^"]*">\s*<\/div>\s*<\/div>/g;
function count(html) { const bi = html.indexOf('<div id="body">'); let n = 0, m; SHELL.lastIndex = 0; while ((m = SHELL.exec(html))) if (m.index >= bi) n++; return n; }
function ctx(html) { const bi = html.indexOf('<div id="body">'); const out = []; let m; SHELL.lastIndex = 0; while ((m = SHELL.exec(html))) if (m.index >= bi) out.push(html.slice(Math.max(0, m.index - 160), m.index).replace(/\s+/g, " ").slice(-120)); return out; }
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  let cur = "";
  const wrap = (obj, name, label) => { const o = obj[name].bind(obj); obj[name] = function (html, ...r) { const a = count(html); const out = o(html, ...r); const b = typeof out === "string" ? count(out) : -1; if (a !== b) _l(`${cur} ${label}: shells ${a} -> ${b}`); return out; }; };
  wrap(NotesAndComments, "TidyDeveloperNotes", "TidyDeveloperNotes");
  wrap(NotesAndComments, "OmitPlaceholderResidue", "OmitPlaceholderResidue");
  wrap(ListsAndRuns, "EmojiStrip", "EmojiStrip");
  wrap(ListsAndRuns, "MergeAdjacentLists", "MergeAdjacentLists");
  wrap(ListsAndRuns, "TypedNumberList", "TypedNumberList");
  wrap(ListsAndRuns, "LinkTextDisplay", "LinkTextDisplay");
  const origIndent = HtmlFormatter.Indent.bind(HtmlFormatter);
  HtmlFormatter.Indent = function (html, ...rest) { const n = count(html); if (n) _l(`${cur} at Indent: ${n} shells :: ${JSON.stringify(ctx(html).slice(0, 3))}`); return origIndent(html, ...rest); };
  const origConv = ContentConverter.ConvertPage.bind(ContentConverter);
  ContentConverter.ConvertPage = function (...a) { const out = origConv(...a); const h = typeof out === "string" ? out : (out && out.html) || ""; const n = count(h); if (n) _l(`${cur} ConvertPage OUT: ${n} shells (type ${typeof out}) :: ${JSON.stringify(ctx(h).slice(0, 2))}`); return out; };
  for (const code of codes) {
    cur = code;
    const base = corpus.mdir(MODS, code);
    const run = new ConversionRun({ imageMode: "P" }); const docs = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
    }
    const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm }); if (!prep.ok) continue;
    await PageAssembler.AssembleModule(run, norm);
  }
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); process.exit(1); });
