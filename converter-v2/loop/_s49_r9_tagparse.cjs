// Session 49 Round 9 — how TagNormaliser reads the nested / compound autocheck forms. Run from reference/tests.
const path = require("path");
const eng = require(path.join(__dirname, "..", "reference", "tests", "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine();
const D = DataService.Data;
const n = new TagNormaliser(D.TagLexicon, D.TagExceptions, D.InstructionCues);
for (const s of process.argv.slice(2)) {
	const r = n.Normalise ? n.Normalise(s) : (n.Parse ? n.Parse(s) : null);
	_l(JSON.stringify(s), "=>", JSON.stringify({ primary: r?.primary?.tag, tags: (r?.tags || []).map((t) => t.tag), cls: r?.class }));
}
