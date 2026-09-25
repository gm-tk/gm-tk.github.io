/** _s50_r16_actnums.cjs — session 50 Round 16 PICK: per module, the activity NUMBERS the gold carries (`class="activity…"
 *  number="4C"`) that no Claude page carries, and whether the writer's template text names them ('Activity 4C' / '4C'
 *  in the Claude page's text or its interactives file). Output-only census. Run from outputs/. */
"use strict";
const fs = require("fs"), path = require("path");
const G = path.join(__dirname, "..", "..", "01-Finalized_Modules_"), C = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const dirs = (root) => { const m = new Map(); for (const t of fs.readdirSync(root)) { const td = path.join(root, t); if (!fs.statSync(td).isDirectory()) continue; for (const d of fs.readdirSync(td)) { const p = path.join(td, d); if (fs.statSync(p).isDirectory()) m.set(d, p); } } return m; };
const gd = dirs(G), cd = dirs(C);
const nums = (dir, re) => { const s = new Set(); let text = ""; for (const f of fs.readdirSync(dir).filter((x) => re.test(x))) { const h = fs.readFileSync(path.join(dir, f), "utf8"); text += h; for (const m of h.matchAll(/class="activity[^"]*"[^>]*\bnumber="([^"]+)"/g)) s.add(m[1].trim().toUpperCase()); } return { s, text }; };
let totMissing = 0, modsWith = 0; const rows = []; const byFam = {};
for (const [code, gp] of gd) {
	const cp = cd.get(code); if (!cp) continue;
	const g = nums(gp, /\.html$/i), c = nums(cp, /_\d+(_\d+)*\.html$/);
	let itx = ""; try { itx = fs.readFileSync(path.join(cp, `${code}_interactives.txt`), "utf8"); } catch {}
	const miss = [...g.s].filter((n) => !c.s.has(n) && /^\d{1,2}[A-Z]$/.test(n));
	if (!miss.length) continue;
	const named = miss.filter((n) => new RegExp(`Activity\\s*:?\\s*${n}\\b`, "i").test(c.text + itx));
	totMissing += miss.length; modsWith++;
	const fam = code.replace(/\d+$/, ""); byFam[fam] = (byFam[fam] ?? 0) + miss.length;
	rows.push([miss.length, code, miss.slice(0, 12).join(","), named.length, named.slice(0, 8).join(",")]);
}
rows.sort((a, b) => b[0] - a[0]);
console.log(`gold activity numbers with no Claude activity: ${totMissing} over ${modsWith} modules`);
console.log("by family:", Object.entries(byFam).sort((a, b) => b[1] - a[1]).slice(0, 12).map(([k, v]) => `${k} ${v}`).join(" · "));
console.log(`named in Claude's own text (the writer typed 'Activity N'): ${rows.reduce((n, r) => n + r[3], 0)}`);
for (const r of rows.slice(0, 25)) console.log(`  ${r[1]}: missing ${r[0]} [${r[2]}] · named in Claude text ${r[3]} [${r[4]}]`);
