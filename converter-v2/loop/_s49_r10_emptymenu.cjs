// Session 49 Round 10 — every Claude page whose #module-menu-content holds no text at all (KB 10 §5: an empty lesson menu must
// carry a visible red flag asking the designer to supply the copy). By module / prefix; lesson vs overview.
const fs = require("fs"), path = require("path");
const CL = path.join(__dirname, "..", "..", "01-Claude_Modules_");
let n = 0, ov = 0, flagged = 0; const mods = {}, pref = {};
for (const t of fs.readdirSync(CL)) for (const m of fs.readdirSync(path.join(CL, t))) {
	const d = path.join(CL, t, m); if (!fs.statSync(d).isDirectory()) continue;
	for (const f of fs.readdirSync(d).filter((x) => x.endsWith(".html"))) {
		const s = fs.readFileSync(path.join(d, f), "utf8");
		const i = s.indexOf('<div id="module-menu-content"'); if (i < 0) continue;
		const j = s.indexOf('<div id="body"', i); const menu = s.slice(i, j < 0 ? undefined : j);
		const txt = menu.replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").trim();
		if (txt) continue;
		n++; if (/_0_0\.html$/.test(f)) ov++;
		mods[m] = (mods[m] || 0) + 1; const p = m.replace(/\d.*$/, ""); pref[p] = (pref[p] || 0) + 1;
	}
}
console.log(`pages with an EMPTY module menu: ${n} (overview-named ${ov}) in ${Object.keys(mods).length} modules`);
console.log("by prefix:", Object.entries(pref).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(", "));
console.log("modules:", Object.entries(mods).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(", "));
