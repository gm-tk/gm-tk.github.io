/** _s50_r14_headfrag.cjs — session 50 Round 14 PICK: every hand-off box (cv2-int-ref) or built widget whose PREVIOUS
 *  element is a short text fragment with no terminal punctuation (BLL247's `<li>The bus</li>` — a sentence head the scanner
 *  left outside the capture). Output-only census over 01-Claude_Modules_. Run from outputs/. */
"use strict";
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const vis = (s) => s.replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();
let n = 0; const mods = new Set(), pages = new Set(); const ex = [];
for (const t of fs.readdirSync(ROOT)) {
	const td = path.join(ROOT, t); if (!fs.statSync(td).isDirectory()) continue;
	for (const m of fs.readdirSync(td)) {
		const md = path.join(td, m); if (!fs.statSync(md).isDirectory()) continue;
		for (const f of fs.readdirSync(md).filter((x) => /_\d+(_\d+)*\.html$/.test(x))) {
			const h = fs.readFileSync(path.join(md, f), "utf8");
			const re = /<div class="cv2-interactive cv2-int-ref"|<div class="(?:dragAndDrop|typing|dropDown|multiChoiceQuiz)\b/g; let x;
			while ((x = re.exec(h)) !== null) {
				const before = h.slice(Math.max(0, x.index - 600), x.index);
				const mm = /<(li|p)\b[^>]*>((?:(?!<\/?(?:li|p)\b)[\s\S])*?)<\/\1>\s*(?:<\/(?:ol|ul)>\s*)?$/.exec(before);
				if (!mm) continue;
				const txt = vis(mm[2]);
				if (!txt || txt.length > 70 || /[.?!:;)"'”’…]$/.test(txt) || /^\[|^[A-Z0-9 ]+$/.test(txt)) continue;
				if (txt.split(" ").length > 8) continue;
				n++; mods.add(m); pages.add(m + "/" + f);
				if (ex.length < 40) ex.push(`${m}/${f} <${mm[1]}> "${txt}" → ${h.slice(x.index, x.index + 40).includes("cv2") ? "BOX" : "WIDGET"}`);
			}
		}
	}
}
console.log(`fragments before a box/widget: ${n} / pages ${pages.size} / modules ${mods.size}`);
for (const e of ex) console.log("  " + e);
