// ROUND 510 — each NEW dragAndDrop / dropQuiz build: its drag / option texts found among the module's GOLD widget texts?
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_"), CL = path.join(__dirname, "..", "..", "01-Claude_Modules_"), ON = path.join(__dirname, "_r510_on");
const norm = (s) => String(s).replace(/<[^>]+>/g, " ").replace(/&[a-z]+;/g, " ").toLowerCase().replace(/[^a-z0-9ā-ū]+/g, " ").trim();
const drags = (h) => [...h.matchAll(/<div class="drag"[^>]*>([\s\S]*?)<\/div>/g)].map((m) => norm(m[1])).filter(Boolean);
for (const p of fs.readFileSync(path.join(__dirname, "_r510_ON_pages.txt"), "utf8").split("\n").filter((x) => x.endsWith(".html"))) {
	const [m, f] = p.split("/");
	const cd = fs.readdirSync(CL).map((t) => path.join(CL, t, m)).find((x) => fs.existsSync(x));
	const before = drags(fs.readFileSync(path.join(cd, f), "utf8")), after = drags(fs.readFileSync(path.join(ON, m, f), "utf8"));
	const neu = after.filter((d) => !before.includes(d)); if (!neu.length) continue;
	const gd = fs.readdirSync(G).map((t) => path.join(G, t, m)).find((x) => fs.existsSync(x));
	const gold = fs.readdirSync(gd).filter((x) => x.endsWith(".html")).map((x) => norm(fs.readFileSync(path.join(gd, x), "utf8").replace(/<!--[\s\S]*?-->/g, ""))).join(" ");
	const hit = neu.filter((d) => gold.includes(d)).length;
	console.log(`${p}: new drags ${neu.length}, found in the gold ${hit} (${(100 * hit / neu.length).toFixed(0)} %) e.g. "${neu[0].slice(0, 50)}"`);
}
