/** _r519_cmp.cjs — r519: every FIB widget in _r519_on/<code>/ vs the gold module's own drag texts. Run from outputs/. */
"use strict";
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const ON = path.join(__dirname, process.argv[2] || "_r519_on");
const norm = (s) => String(s).replace(/<[^>]+>/g, " ").replace(/&[a-z]+;/g, " ").toLowerCase().replace(/\s+/g, " ").trim();
const mdir = (code) => { for (const t of fs.readdirSync(G)) { const p = path.join(G, t, code); if (fs.existsSync(p)) return p; } return null; };
let tot = 0, hit = 0, txt = 0, wid = 0;
for (const m of fs.readFileSync(path.join(__dirname, "_affected_r519.txt"), "utf8").split(/\s+/).filter(Boolean)) {
	const gd = mdir(m); if (!gd) { console.log(m, "no gold"); continue; }
	const gold = fs.readdirSync(gd).filter((x) => x.endsWith(".html")).map((f) => fs.readFileSync(path.join(gd, f), "utf8")).join(" ");
	const gdrags = new Set([...gold.matchAll(/<div class="drag[^"]*"[^>]*>([\s\S]*?)<\/div>/g)].map((x) => norm(x[1])));
	const gfib = (gold.match(/layout="FIB"/g) || []).length;
	const gtext = " " + norm(gold) + " ";
	const od = path.join(ON, m); if (!fs.existsSync(od)) { console.log(m, "no ON output"); continue; }
	for (const f of fs.readdirSync(od).filter((x) => x.endsWith(".html"))) {
		const h = fs.readFileSync(path.join(od, f), "utf8");
		for (const w of h.split('layout="FIB">').slice(1)) {
			wid++;
			const body = w.slice(0, w.indexOf("activityButton") > 0 ? w.indexOf("activityButton") : 4000);
			const drags = [...body.matchAll(/<div class="drag" option="\d+">([\s\S]*?)<\/div>/g)].map((x) => norm(x[1]));
			const drops = (body.match(/class="drop"/g) || []).length;
			const h1 = drags.filter((d) => gdrags.has(d)).length, h2 = drags.filter((d) => !gdrags.has(d) && gtext.includes(" " + d + " ")).length;
			tot += drags.length; hit += h1; txt += h2;
			console.log(m, f, "goldFIB", gfib, "drops", drops, "drags", drags.length, "= gold drag", h1, "+ in gold text", h2, "e.g.", drags.slice(0, 6).join(" | "));
		}
	}
}
console.log("TOTAL widgets", wid, "drags", tot, "= a gold drag", hit, "+ in gold text", txt);
