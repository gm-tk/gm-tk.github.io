// ROUND 504 — which Writers Templates type the side-tab crumb LIST as BLACK `Tab N – label` lines (not red [Tab N] tags)?
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const LINE = /^\s*Tab\s*(\d+)\s*[–—:\-]\s*(\S.*)$/i, INSTR = /side\s*tabs?/i;
for (const t of fs.readdirSync(G)) for (const m of fs.readdirSync(path.join(G, t))) {
	const d = path.join(G, t, m); if (!fs.statSync(d).isDirectory()) continue;
	for (const f of fs.readdirSync(d).filter((x) => x.endsWith("_parsed.txt") && !/ Media List_parsed\.txt$/.test(x.replace("Writers Template + Media List", "WT")))) {
		const L = fs.readFileSync(path.join(d, f), "utf8").split("\n");
		const hits = L.map((l, i) => [i + 1, l]).filter(([, l]) => !/🔴/.test(l) && LINE.test(l));
		if (hits.length >= 3) {
			const instr = L.findIndex((l) => INSTR.test(l)) + 1;
			console.log(`${t}/${m}: ${hits.length} black 'Tab N –' lines (l.${hits[0][0]}–${hits[hits.length - 1][0]}), side-tabs instruction l.${instr || "none"} ${instr ? JSON.stringify(L[instr - 1].slice(0, 50)) : ""}`);
		}
	}
}
