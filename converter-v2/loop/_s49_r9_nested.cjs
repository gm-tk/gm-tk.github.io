// Session 49 Round 9 — every NESTED red bracket `[a [b] c]` in the Writers Templates (parsed text), by inner / outer words.
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const RE = /\[([^\[\]]*)\[([^\[\]]*)\]([^\[\]]*)\]/g;
const byInner = {}, byOuterFirst = {}; let n = 0; const mods = new Set(); const ex = [];
for (const t of fs.readdirSync(G)) for (const m of fs.readdirSync(path.join(G, t))) {
	const d = path.join(G, t, m); if (!fs.statSync(d).isDirectory()) continue;
	for (const f of fs.readdirSync(d).filter((x) => x.endsWith("_parsed.txt") && !/\] Media List_parsed|^[^+]* Media List_parsed\.txt$/.test(x))) {
		const L = fs.readFileSync(path.join(d, f), "utf8").split("\n");
		L.forEach((ln, i) => {
			const red = [...ln.matchAll(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu)].map((x) => x[1]).join(" ");
			for (const mm of red.matchAll(RE)) {
				n++; mods.add(m);
				const inner = mm[2].trim().toLowerCase(), outer = (mm[1] + " " + mm[3]).trim().toLowerCase();
				byInner[inner] = (byInner[inner] || 0) + 1;
				const o = outer.split(/\s+/).slice(0, 3).join(" ");
				byOuterFirst[o] = (byOuterFirst[o] || 0) + 1;
				if (ex.length < 12) ex.push(`${m} l.${i + 1}: ${mm[0].slice(0, 70)}`);
			}
		});
	}
}
console.log(`nested red brackets: ${n} in ${mods.size} modules`);
console.log("by inner:", Object.entries(byInner).sort((a, b) => b[1] - a[1]).slice(0, 15).map(([k, v]) => `${k} ${v}`).join(" | "));
console.log("by outer (first 3 words):", Object.entries(byOuterFirst).sort((a, b) => b[1] - a[1]).slice(0, 20).map(([k, v]) => `${k} ${v}`).join(" | "));
console.log(ex.join("\n"));
