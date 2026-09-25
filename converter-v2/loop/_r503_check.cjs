// ROUND 503 — every ON page differs from disk only inside #module-menu-content (the header), never in #body.
const fs = require("fs"), path = require("path");
const ON = path.join(__dirname, "_r503_on"), CL = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const dirOf = (m) => { for (const t of fs.readdirSync(CL)) { const p = path.join(CL, t, m); if (fs.existsSync(p)) return p; } };
let ok = 0, bad = 0;
for (const m of fs.readdirSync(ON)) for (const f of fs.readdirSync(path.join(ON, m))) {
	const a = fs.readFileSync(path.join(dirOf(m), f), "utf8"), b = fs.readFileSync(path.join(ON, m, f), "utf8");
	if (a === b) continue;
	const cut = (s) => [s.slice(0, s.indexOf('<div id="module-menu-content"')), s.slice(s.indexOf('<div id="body">'))];
	const [a0, a1] = cut(a), [b0, b1] = cut(b);
	if (a0 === b0 && a1 === b1) ok++; else { bad++; console.log("OUTSIDE-MENU CHANGE", m, f); }
}
console.log(`menu-only ${ok}, other ${bad}`);
