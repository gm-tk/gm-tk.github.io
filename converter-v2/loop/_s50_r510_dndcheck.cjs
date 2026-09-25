// Session 50 Round 1 (r510) — each NEW dragAndDrop / dropQuiz build (disk, r510 ON) vs the OFF probe (_r510_offfinal):
// its drag texts found among the module's GOLD page texts? Run from outputs/ (plain node).
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_"), CL = path.join(__dirname, "..", "..", "01-Claude_Modules_"), OFF = path.join(__dirname, "_r510_offfinal");
const norm = (s) => String(s).replace(/<[^>]+>/g, " ").replace(/&[a-z]+;/g, " ").toLowerCase().replace(/[^a-z0-9ā-ū]+/g, " ").trim();
const drags = (h) => [...h.matchAll(/<div class="drag"[^>]*>([\s\S]*?)<\/div>/g)].map((m) => norm(m[1])).filter(Boolean);
let pages = 0, tot = 0, hitAll = 0;
for (const m of fs.readdirSync(OFF)) {
	const cd = fs.readdirSync(CL).map((t) => path.join(CL, t, m)).find((x) => fs.existsSync(x)); if (!cd) continue;
	const gd = fs.readdirSync(G).map((t) => path.join(G, t, m)).find((x) => fs.existsSync(x));
	const gold = fs.readdirSync(gd).filter((x) => x.endsWith(".html")).map((x) => norm(fs.readFileSync(path.join(gd, x), "utf8").replace(/<!--[\s\S]*?-->/g, ""))).join(" ");
	for (const f of fs.readdirSync(path.join(OFF, m)).filter((x) => x.endsWith(".html"))) {
		const before = drags(fs.readFileSync(path.join(OFF, m, f), "utf8")), after = drags(fs.readFileSync(path.join(cd, f), "utf8"));
		const neu = after.filter((d) => !before.includes(d)); if (!neu.length) continue;
		const hit = neu.filter((d) => gold.includes(d)).length; pages++; tot += neu.length; hitAll += hit;
		console.log(`${m}/${f}: new drags ${neu.length}, in the gold ${hit} (${(100 * hit / neu.length).toFixed(0)} %)`);
	}
}
console.log(`TOTAL: ${pages} pages, ${tot} new drags, ${hitAll} in the gold (${(100 * hitAll / Math.max(1, tot)).toFixed(0)} %)`);
