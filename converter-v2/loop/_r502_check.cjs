// ROUND 502 — every ON page differs from disk ONLY by the lesson menu's row > col-md-8 wrapper (+ re-indent).
const fs = require("fs"), path = require("path");
const ON = path.join(__dirname, "_r502_on"), CL = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const dirOf = (m) => { for (const t of fs.readdirSync(CL)) { const p = path.join(CL, t, m); if (fs.existsSync(p)) return p; } };
const menu = (s) => { const i = s.indexOf('<div id="module-menu-content"'); const j = s.indexOf('<div id="body">'); return [i, j]; };
let ok = 0, bad = 0, empty = 0;
for (const m of fs.readdirSync(ON)) for (const f of fs.readdirSync(path.join(ON, m))) {
	const a = fs.readFileSync(path.join(dirOf(m), f), "utf8"), b = fs.readFileSync(path.join(ON, m, f), "utf8");
	if (a === b) continue;
	const [ai, aj] = menu(a), [bi, bj] = menu(b);
	const outsideSame = a.slice(0, ai) === b.slice(0, bi) && a.slice(aj) === b.slice(bj);
	const al = a.slice(ai, aj).split("\n").map((l) => l.trim()).filter(Boolean);
	const bl = b.slice(bi, bj).split("\n").map((l) => l.trim()).filter(Boolean);
	// disk: moduleMenu, row, col, ...content..., </div>(col), </div>(row), </div>(menu), </div>(header)
	const stripped = [al[0], ...al.slice(3, al.length - 4), ...al.slice(al.length - 2)];
	const same = al[1] === '<div class="row">' && al[2] === '<div class="col-md-8 col-12">' && JSON.stringify(stripped) === JSON.stringify(bl);
	if (outsideSame && same) { ok++; if (bl.length <= 3) empty++; } else { bad++; console.log("UNEXPECTED", m, f, outsideSame, same); }
}
console.log(`pages: wrapper-only ${ok} (of which empty menus ${empty}), unexpected ${bad}`);
