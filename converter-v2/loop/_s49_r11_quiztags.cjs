// Session 49 Round 11 — writer quiz tags the normaliser does not know (one-word spellings) — red spans only, by module.
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const pats = { radioquiz: /\bradio\s?quiz/i, "radioquiz(one word)": /\bradioquiz\b/i, "mtk quiz+autocheck": /mtk\s*quiz[^\]]*\]?[^\[]*\[?\s*auto\s*-?\s*check/i, dropquiz: /\bdropquiz\b/i, multichoice: /\bmultichoice\b/i, "multi-choice": /\bmulti-choice\b/i };
const res = {};
for (const t of fs.readdirSync(G)) for (const m of fs.readdirSync(path.join(G, t))) {
	const d = path.join(G, t, m); if (!fs.statSync(d).isDirectory()) continue;
	for (const f of fs.readdirSync(d).filter((x) => x.endsWith("_parsed.txt") && !/^[^+]* Media List_parsed\.txt$/.test(x))) {
		for (const ln of fs.readFileSync(path.join(d, f), "utf8").split("\n")) {
			const red = [...ln.matchAll(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu)].map((x) => x[1]).join(" ");
			if (!red) continue;
			for (const [k, re] of Object.entries(pats)) if (re.test(red)) { res[k] = res[k] || { n: 0, mods: new Set() }; res[k].n++; res[k].mods.add(m); }
		}
	}
}
for (const [k, v] of Object.entries(res)) console.log(`${k}: ${v.n} tags / ${v.mods.size} modules — ${[...v.mods].slice(0, 12).join(" ")}`);
