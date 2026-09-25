// ROUND 507 — every question the yellow-tick build made, checked against the module's GOLD quizzes (all gold pages):
// the gold question with the most similar text; does its value="correct" option equal ours?
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const ON = path.join(__dirname, "_r507_on"), CL = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const norm = (s) => String(s).replace(/&quot;/g, '"').replace(/&amp;/g, "&").replace(/<[^>]+>/g, " ").toLowerCase().replace(/[^a-z0-9ā-ū]+/g, " ").trim();
const words = (s) => new Set(norm(s).split(" ").filter((w) => w.length > 2));
const sim = (a, b) => { const A = words(a), B = words(b); if (!A.size || !B.size) return 0; let n = 0; for (const w of A) if (B.has(w)) n++; return n / Math.max(A.size, B.size); };
function quizzes(html) {
	const out = [];
	for (const q of html.split(/(?=<(?:p|li) class="mcqQuestionText")/).slice(1)) {
		const qt = (q.match(/<(?:p|li) class="mcqQuestionText">([\s\S]*?)<\/(?:p|li)>/) || [])[1] || "";
		const opts = [...q.matchAll(/<p class="mcqOption"\s*([^>]*)>([\s\S]*?)<\/p>/g)].map((m) => ({ t: m[2], ok: /value="correct"/.test(m[1]) }));
		out.push({ qt, opts });
	}
	return out;
}
let tot = 0, exact = 0, wrong = 0, nog = 0;
for (const m of fs.readdirSync(ON)) {
	const gd = fs.readdirSync(G).map((t) => path.join(G, t, m)).find((p) => fs.existsSync(p));
	const gq = fs.readdirSync(gd).filter((f) => f.endsWith(".html")).flatMap((f) => quizzes(fs.readFileSync(path.join(gd, f), "utf8").replace(/<!--[\s\S]*?-->/g, "")));
	const cd = fs.readdirSync(CL).map((t) => path.join(CL, t, m)).find((p) => fs.existsSync(p));
	for (const f of fs.readdirSync(path.join(ON, m)).filter((f) => f.endsWith(".html"))) {
		const on = quizzes(fs.readFileSync(path.join(ON, m, f), "utf8"));
		const off = fs.existsSync(path.join(cd, f)) ? quizzes(fs.readFileSync(path.join(cd, f), "utf8")) : [];
		const offKeys = new Set(off.map((q) => norm(q.qt)));
		for (const q of on) {
			if (offKeys.has(norm(q.qt))) continue;   // built before this round
			tot++;
			let best = null, bs = 0;
			for (const g of gq) { const s = Math.max(sim(q.qt, g.qt), sim(q.opts.map((o) => o.t).join(" "), g.opts.map((o) => o.t).join(" "))); if (s > bs) { bs = s; best = g; } }
			const mine = q.opts.find((o) => o.ok)?.t || "";
			if (!best || bs < 0.5) { nog++; console.log(`  no-gold  ${m} ${f}: ${norm(q.qt).slice(0, 60)}`); continue; }
			const gold = best.opts.filter((o) => o.ok).map((o) => norm(o.t));
			if (gold.includes(norm(mine)) || gold.some((g) => sim(g, mine) >= 0.8)) exact++;
			else { wrong++; console.log(`  DIFFERS  ${m} ${f}: Q "${norm(q.qt).slice(0, 50)}" ours "${norm(mine).slice(0, 40)}" gold "${gold.join(" | ").slice(0, 40)}" (sim ${bs.toFixed(2)})`); }
		}
	}
}
console.log(`NEW questions ${tot}: answer = the gold's ${exact}, differs ${wrong}, no gold quiz found ${nog}`);
