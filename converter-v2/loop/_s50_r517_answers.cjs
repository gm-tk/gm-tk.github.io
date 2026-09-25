// Session 50 Round 9 (r517) — every TABLE-form typing quiz Claude built (div.typing layout="standard" > table): its inputs' answers
// against the module's gold typing answers (any <input … answer="…">). Also: malformed units (empty answer, no input). Plain node, from outputs/.
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_"), C = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const norm = (s) => String(s).replace(/&amp;/g, "&").replace(/&[a-z]+;/g, " ").toLowerCase().replace(/[\s ]+/g, " ").replace(/[.,;:!?]+$/, "").trim();
const mods = fs.readFileSync(path.join(__dirname, process.argv[2] || "_affected_r517.txt"), "utf8").split(/\s+/).filter(Boolean);
let quizzes = 0, inputs = 0, hit = 0, noGold = 0, bad = 0;
for (const m of mods) {
	const cd = fs.readdirSync(C).map((t) => path.join(C, t, m)).find((x) => fs.existsSync(x));
	const gd = fs.readdirSync(G).map((t) => path.join(G, t, m)).find((x) => fs.existsSync(x));
	if (!cd || !gd) continue;
	const gold = new Set();
	for (const f of fs.readdirSync(gd).filter((x) => x.endsWith(".html")))
		for (const a of fs.readFileSync(path.join(gd, f), "utf8").replace(/<!--[\s\S]*?-->/g, "").matchAll(/<input[^>]*\banswer="([^"]*)"/g))
			for (const alt of a[1].split("||")) gold.add(norm(alt));
	let mq = 0, mi = 0, mh = 0;
	for (const f of fs.readdirSync(cd).filter((x) => x.endsWith(".html"))) {
		const h = fs.readFileSync(path.join(cd, f), "utf8");
		for (const q of h.matchAll(/<div class="typing[^"]*" layout="standard">\s*<div class="table-responsive">([\s\S]*?)<\/table>/g)) {
			mq++; const ans = [...q[1].matchAll(/<input[^>]*\banswer="([^"]*)"/g)].map((x) => x[1]);
			if (!ans.length || ans.some((a) => !a.trim())) bad++;
			for (const a of ans) { mi++; if (gold.has(norm(a))) mh++; }
		}
	}
	if (!mq) continue;
	quizzes += mq; inputs += mi; hit += mh; if (!gold.size) noGold += mi;
	console.log(`${m}: ${mq} table quiz(zes), ${mi} inputs, ${mh} = a gold answer${gold.size ? "" : " (module has NO gold typing input)"}`);
}
console.log(`TOTAL ${quizzes} table quizzes / ${inputs} inputs: ${hit} = a gold answer (${(100 * hit / Math.max(1, inputs)).toFixed(0)} %), ${noGold} in modules with no gold typing; malformed ${bad}`);
