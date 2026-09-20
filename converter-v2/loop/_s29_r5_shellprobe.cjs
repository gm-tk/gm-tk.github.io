/** _s29_r5_shellprobe.cjs — what RAW content sits inside a body-side empty `row > col` shell before HtmlFormatter runs? */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const codes = process.argv.slice(2);
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
  DataService.Data.AcksFormats.oembed.throttle_ms = 0;
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine(); if (process.env.CC_INSTR) Object.assign(globalThis, require(process.env.CC_INSTR));
  const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
  const origIndent = HtmlFormatter.Indent.bind(HtmlFormatter);
  let cur = "";
  HtmlFormatter.Indent = function (html, ...rest) {
    const re = /<div class="row">\s*<div class="col[^"]*">([\s\S]{0,400}?)<\/div>\s*<\/div>/g;
    let m; const bi = html.indexOf('<div id="body">');
    while ((m = re.exec(html))) {
      if (m.index < bi) continue;
      const inner = m[1];
      if (inner.replace(/<!--[\s\S]*?-->/g, "").trim() === "" || /^(\s|<p>\s*<\/p>|<!--[\s\S]*?-->)*$/.test(inner)) {
        _l(`${cur} :: RAW INNER=${JSON.stringify(inner.slice(0, 160))} :: BEFORE=${JSON.stringify(html.slice(Math.max(0, m.index - 140), m.index).replace(/\s+/g, " "))}`);
      }
    }
    return origIndent(html, ...rest);
  };
  for (const code of codes) {
    cur = code; globalThis.__probeCode = code;
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
