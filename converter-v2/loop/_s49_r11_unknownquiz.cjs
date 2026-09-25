// Session 49 Round 11 — red brackets naming a quiz / interactive the normaliser resolves to NO widget tag (run from reference/tests).
const fs = require("fs"), path = require("path");
const eng = require(path.join(__dirname, "..", "reference", "tests", "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine();
const D = DataService.Data, n = new TagNormaliser(D.TagLexicon, D.TagExceptions, D.InstructionCues);
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const WORD = /\b(quiz|radio|multichoice|multi-choice|drag|drop|reorder|typing|self\s?check|auto\s?check|flip|click\s?drop|sorting|matching)\b/i;
const res = {}; let tot = 0; const mods = new Set();
for (const t of fs.readdirSync(G)) for (const m of fs.readdirSync(path.join(G, t))) {
	const d = path.join(G, t, m); if (!fs.statSync(d).isDirectory()) continue;
	for (const f of fs.readdirSync(d).filter((x) => x.endsWith("_parsed.txt") && !/^[^+]* Media List_parsed\.txt$/.test(x))) {
		for (const ln of fs.readFileSync(path.join(d, f), "utf8").split("\n")) {
			for (const x of ln.matchAll(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu)) {
				const red = x[1]; if (!/\[/.test(red) || !WORD.test(red)) continue;
				const r = n.Parse(red);
				const hasWidget = (r.tags || []).some((tg) => tg.directive === "INTERACTIVE" || /quiz|drag|drop|reorder|flip|click|typing|mcq|radio|select|sort|match|memory|word/i.test(tg.tag));
				if (hasWidget) continue;
				const k = red.replace(/\s+/g, " ").trim().toLowerCase().slice(0, 50);
				res[k] = res[k] || { n: 0, mods: new Set() }; res[k].n++; res[k].mods.add(m); tot++; mods.add(m);
			}
		}
	}
}
_l(`unresolved quiz-like red brackets: ${tot} in ${mods.size} modules`);
for (const [k, v] of Object.entries(res).sort((a, b) => b[1].n - a[1].n).slice(0, 30)) _l(`  ${String(v.n).padStart(3)} ${String(v.mods.size).padStart(3)}m  ${k}`);
