// Session 50 Round 4 PICK — every red span holding a [bracket] whose parse has NO primary tag and is not a writer instruction,
// grouped by its folded first bracket (the lexicon's blind spots). Run from reference/tests/ under WSL (plain node).
const fs = require("fs"), path = require("path");
const eng = require(path.join(__dirname, "..", "reference", "tests", "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine();
const D = DataService.Data, n = new TagNormaliser(D.TagLexicon, D.TagExceptions, D.InstructionCues);
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const excl = new Set(fs.readFileSync(path.join(__dirname, "..", "reference", "tests", "compare_exclusions.txt"), "utf8").split(/\s+/).filter((x) => /^[A-Z]/.test(x)));
const res = {}; let tot = 0, all = 0; const mods = new Set();
for (const t of fs.readdirSync(G)) for (const m of fs.readdirSync(path.join(G, t))) {
	if (excl.has(m)) continue;
	const d = path.join(G, t, m); if (!fs.statSync(d).isDirectory()) continue;
	for (const f of fs.readdirSync(d).filter((x) => x.endsWith("_parsed.txt") && !/^[^+]* Media List_parsed\.txt$/.test(x))) {
		for (const ln of fs.readFileSync(path.join(d, f), "utf8").split("\n")) {
			for (const x of ln.matchAll(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu)) {
				const red = x[1]; const br = red.match(/\[([^\]]{1,80})\]/); if (!br) continue;
				all++;
				let r; try { r = n.Parse(red); } catch { continue; }
				if (r.primary || (r.tags || []).length) continue; if (br[1].split(/s+/).length > 4) continue;
				const k = br[1].toLowerCase().replace(/\d+/g, "#").replace(/\s+/g, " ").trim().slice(0, 45);
				(res[k] = res[k] || { n: 0, mods: new Set(), ex: red.replace(/\s+/g, " ").trim().slice(0, 90) }).n++;
				res[k].mods.add(m); tot++; mods.add(m);
			}
		}
	}
}
_l(`red spans with a bracket: ${all}; resolving to NO tag: ${tot} in ${mods.size} modules`);
for (const [k, v] of Object.entries(res).sort((a, b) => b[1].mods.size - a[1].mods.size || b[1].n - a[1].n).slice(0, 60))
	_l(`  ${String(v.n).padStart(4)} ${String(v.mods.size).padStart(3)}m  [${k}]   e.g. ${v.ex}`);
