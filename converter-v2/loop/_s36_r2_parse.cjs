/** _s36_r2_parse.cjs — parse a few red-span strings through the live TagNormaliser (session 36 Round 2 PICK). reference/tests: node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s36_r2_parse.cjs */
"use strict";
const path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine();
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
for (const s of ["[Title: Dance and Movement]", "[Title: Puoro me te Oro| Music and Sound]", "[Title: Puoro me te Oro | Music and Sound]", "[Title: Phase one] Emoji for thumb nail 🎸", "[Title: Visual Arts]", "[ARFUN02]"]) {
  const p = norm.Parse(s);
  _l(JSON.stringify(s), "->", JSON.stringify({ primary: p.primary && { tag: p.primary.tag, directive: p.primary.directive, fragment: p.primary.fragment }, cls: p.class, folded: p.folded }));
}
