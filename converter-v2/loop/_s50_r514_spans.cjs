// Session 50 Round 6 (r514) — every red span whose parse CHANGES when the toggled aliases are on (SPELLALIAS_OFF off),
// grouped by the tags it gains. Run from reference/tests/ under WSL.
const fs = require("fs"), path = require("path");
const eng = require(path.join(__dirname, "..", "reference", "tests", "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine();
const D = DataService.Data;
process.env.SPELLALIAS_OFF = "1"; const nOff = new TagNormaliser(D.TagLexicon, D.TagExceptions, D.InstructionCues); delete process.env.SPELLALIAS_OFF;
const nOn = new TagNormaliser(D.TagLexicon, D.TagExceptions, D.InstructionCues);
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const key = (r) => (r.tags || []).map((t) => t.tag).join("+") + "|" + (r.class ?? "");
const byTag = {}; let tot = 0; const mods = new Set();
for (const t of fs.readdirSync(G)) for (const m of fs.readdirSync(path.join(G, t))) {
	const d = path.join(G, t, m); if (!fs.statSync(d).isDirectory()) continue;
	for (const f of fs.readdirSync(d).filter((x) => x.endsWith("_parsed.txt") && !/^[^+]* Media List_parsed\.txt$/.test(x))) {
		for (const ln of fs.readFileSync(path.join(d, f), "utf8").split("\n")) {
			for (const x of ln.matchAll(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu)) {
				const red = x[1]; if (!/\[/.test(red)) continue;
				const off = nOff.Parse(red), on = nOn.Parse(red);
				if (key(off) === key(on)) continue;
				const w = `${key(off)} → ${key(on)}`;
				tot++; mods.add(m); (byTag[w] = byTag[w] || []).push(`${m}: ${red.replace(/\s+/g, " ").trim().slice(0, 130)}`);
			}
		}
	}
}
_l(`spans changed by r514: ${tot} in ${mods.size} modules`);
for (const [k, v] of Object.entries(byTag).sort((a, b) => b[1].length - a[1].length)) { _l(`== ${k} (${v.length})`); for (const s of v.slice(0, 6)) _l("   " + s); }
