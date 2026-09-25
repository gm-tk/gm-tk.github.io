// _verify_dragdrop.cjs — ROUND 350 (Chris's D10-3, the dragAndDrop build kickoff): every BUILT dragAndDrop is well-formed to KB 03B.
// ROUND 351 — the KB 03B "Column Layout" is checked too (the category-sort build): see checkColumn().
//
// For each module: converts it in memory (the batch_convert path, Mode P), harvests every `<div class="dragAndDrop …">`
// widget on the ASSEMBLED pages (the post-pass output — so the r318 lazy strip and the r240 alt rider are both seen), and
// checks the 03B "Standard Layout" form per widget:
//   1. a questionContainer / ddContainer pair; a dropContainer + a dragContainer inside the ddContainer;
//   2. questions == drops == drags (a standard layout is 1:1), and every drag `option` has a drop `option` and vice-versa;
//   3. the activityButton row (reset / undo / checkAnswer) closes the widget (03B; r350 button_row);
//   4. no raw `[tag]` in the visible text (a leak);
//   5. NO loading="lazy" on any <img> inside the widget (constraint 83);
//   6. an `images` widget: every drag holds exactly one visible <img> (the Mode-P placeholder; the comment is not counted)
//      and every question holds text; a text widget: every drag holds text.
// Per module: widgets N (images M, column C) / drags D / defect. A `layout="column"` widget (ROUND 351) is checked against
// 03B's Column Layout instead: a dropContainer of HEADED ddColumns each holding ≥ 1 drop whose option is its own column index,
// a dragContainer whose ddColumn count equals the drop ddColumn count (03B: "Empty ddColumn pads to match drop column count"),
// per column drops == drags, every drag option naming a drop column, the button row, no raw [tag], no lazy, no empty drag.
// FIB / scatter / area / venn are counted, not checked (no builder ships them). Protected criterion: defect 0 (✓ at the
// recorded baseline / ✗ above it — the r348 form).
//
// Usage:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_dragdrop.cjs BLL146 BLL112 ENFUN04 …
//         node --require ./_deflate_raw_polyfill.cjs _verify_dragdrop.cjs --selftest
// Selftest (INJECT): with CV2_SELFTEST_INJECT the verifier rewrites the first built STANDARD widget's first drag to option="99"
// (no matching drop) and puts loading="lazy" on its image, and (ROUND 351) the first built COLUMN widget's first drag to
// option="99" (no such drop column) — all must register as defects (DETECTION); the fixture module must build > 0 widgets
// (LIVENESS).
"use strict";
const fs = require("fs"), path = require("path");
const corpus = require("./corpus.cjs");
if (process.argv.includes("--selftest")) { require("./_selftest_core.cjs").selftest(__filename); return; }
const MODS = process.env.CV2_MODS_ROOT || path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_");
const eng = require("./_engine_load.cjs");
const Data = eng.loadData();
Data.AcksFormats.oembed.throttle_ms = 0;
globalThis.DataService = { Data, async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
eng.loadEngine();
const norm = new TagNormaliser(Data.TagLexicon, Data.TagExceptions, Data.InstructionCues);
const BASE = (() => { try { return JSON.parse(fs.readFileSync(path.join(__dirname, "gate_baseline.json"), "utf8")).dragdrop?.per_module || {}; } catch { return {}; } })();
const BTN = Data.EmitTemplates?.interactive_builders?.dragAndDrop?.button_row;
const BTN_ON = !!(BTN && BTN.enabled !== false && !(BTN.env && process.env[BTN.env]));

async function convertModule(mod) {
	const base = corpus.mdir(MODS, mod);
	const run = new ConversionRun({ imageMode: "P" });
	const docs = [];
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
		const buf = fs.readFileSync(path.join(base, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		docs.push({ name, doc: await DocxExtractor.Extract(zip) });
	}
	const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f))
		.map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
	const log = console.log, warn = console.warn, err = console.error;
	console.log = () => {}; console.warn = () => {}; console.error = () => {};
	try {
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
		if (!prep.ok) throw new Error(`prep refused (${prep.reason})`);
		await PageAssembler.AssembleModule(run, norm);
	} finally { console.log = log; console.warn = warn; console.error = err; }
	return run.outputs.filter((o) => /\.html$/.test(o.filename)).map((o) => ({ name: o.filename, html: String(o.content ?? "") }));
}

/** every top-level `<div class="dragAndDrop …">` subtree of a page (depth-balanced) */
function widgets(html) {
	const out = []; const re = /<div class="dragAndDrop\b[^"]*"[^>]*>/g; let m;
	while ((m = re.exec(html)) !== null) {
		const start = m.index; const dre = /<(\/?)div\b[^>]*>/g; dre.lastIndex = start; let depth = 0, d;
		while ((d = dre.exec(html)) !== null) { depth += d[1] ? -1 : 1; if (depth === 0) { out.push(html.slice(start, d.index + d[0].length)); re.lastIndex = d.index + d[0].length; break; } }
	}
	return out;
}
const visible = (s) => s.replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ");
/** the balanced inner html of the first element carrying `cls` as a class token, or null */
function sub(html, cls) {
	const m = new RegExp(`<div class="[^"]*\\b${cls}\\b[^"]*"[^>]*>`).exec(html); if (!m) return null;
	const dre = /<(\/?)div\b[^>]*>/g; dre.lastIndex = m.index; let depth = 0, d;
	while ((d = dre.exec(html)) !== null) { depth += d[1] ? -1 : 1; if (depth === 0) return html.slice(m.index + m[0].length, d.index); }
	return null;
}
const items = (inner, cls) => [...(inner ?? "").matchAll(new RegExp(`<div class="${cls}"([^>]*)>([\\s\\S]*?)</div>`, "g"))].map((x) => ({ attrs: x[1], inner: x[2] }));
const optionOf = (attrs) => /option="([^"]*)"/.exec(attrs)?.[1] ?? null;
/** ROUND 351 — every balanced `<div class="ddColumn">` subtree's inner html, in order (the 03B column layout's columns) */
function subs(html, cls) {
	const out = []; const re = new RegExp(`<div class="[^"]*\\b${cls}\\b[^"]*"[^>]*>`, "g"); let m;
	while ((m = re.exec(html ?? "")) !== null) {
		const dre = /<(\/?)div\b[^>]*>/g; dre.lastIndex = m.index; let depth = 0, d;
		while ((d = dre.exec(html)) !== null) { depth += d[1] ? -1 : 1; if (depth === 0) { out.push(html.slice(m.index + m[0].length, d.index)); re.lastIndex = d.index + d[0].length; break; } }
	}
	return out;
}

/** ROUND 351 — the KB 03B "Column Layout" (the r351 category-sort build): headed drop columns, option = the column index,
 *  drag columns padded to the drop-column count, per column drops == drags. */
function checkColumn(w, r) {
	const dropC = sub(w, "dropContainer"), dragC = sub(w, "dragContainer");
	if (dropC === null || dragC === null) { r.defects.push("no dropContainer / dragContainer pair"); return r; }
	const cols = subs(dropC, "ddColumn"), dcols = subs(dragC, "ddColumn");
	if (!cols.length) { r.defects.push("no drop ddColumn"); return r; }
	const perCol = new Map(), anyCol = new Set();
	cols.forEach((c, i) => {
		const drops = items(c, "drop"); const key = String(i + 1);
		if (!visible(c.replace(/<div class="drop"[^>]*><\/div>/g, " ")).trim() && !/<img\b/.test(c)) r.defects.push(`drop column ${key} has no heading`);
		if (!drops.length) r.defects.push(`drop column ${key} has no drop`);
		for (const d of drops) { const o = optionOf(d.attrs); if (o === "any") anyCol.add(key); else if (o !== key) r.defects.push(`drop option ${o} sits in column ${key}`); }
		perCol.set(key, drops.length);
	});
	const drags = items(dragC, "drag"); r.drags = drags.length;
	const dragCount = new Map();
	for (const d of drags) {
		const o = optionOf(d.attrs); dragCount.set(o, (dragCount.get(o) ?? 0) + 1);
		if (!perCol.has(o)) r.defects.push(`drag option ${o} has no drop column`);
		if (!visible(d.inner).trim() && !/<img\b/.test(d.inner.replace(/<!--[\s\S]*?-->/g, " "))) r.defects.push("an empty drag");
	}
	for (const [o, n] of perCol) if (!anyCol.has(o) && (dragCount.get(o) ?? 0) !== n) r.defects.push(`column ${o}: drops ${n} / drags ${dragCount.get(o) ?? 0}`);
	if (dcols.length !== cols.length) r.defects.push(`drag ddColumns ${dcols.length} / drop ddColumns ${cols.length} (03B pads to match)`);
	if (BTN_ON && !btnOk(w)) r.defects.push("no activityButton row");
	if (/\[\s*[A-Za-z][^\]\n]{0,40}\]/.test(visible(w))) r.defects.push("raw [tag] in the visible text");
	if (/loading="lazy"/.test(w)) r.defects.push('loading="lazy" inside the widget (c83)');
	return r;
}

// ROUND 483 (KB 03B "With autoCheck"; c38 on the 1-3 / 4-6 / ECH templates): an autoCheck widget keeps ONLY the Reset button;
// every other widget keeps the reset / undo hidden / checkAnswer hidden row
function btnOk(w) {
	if (/<div class="dragAndDrop[^"]*\bautoCheck\b/.test(w))
		return /activityButton reset/.test(w) && !/activityButton undo/.test(w) && !/activityButton checkAnswer/.test(w);
	return /activityButton reset/.test(w) && /activityButton undo hidden/.test(w) && /activityButton checkAnswer hidden/.test(w);
}

function check(w) {
	const layout = /layout="([^"]*)"/.exec(w)?.[1] ?? "";
	const images = /<div class="dragAndDrop[^"]*\bimages\b/.test(w);
	const r = { layout, images, drags: 0, defects: [] };
	if (layout === "column") return checkColumn(w, r);   // ROUND 351 — the category-sort build
	if (layout !== "standard") return r;   // FIB / scatter / area / venn are not built by any builder — counted only
	const q = sub(w, "questionContainer"), dd = sub(w, "ddContainer");
	if (q === null || dd === null) { r.defects.push("no questionContainer / ddContainer pair"); return r; }
	const dropC = sub(dd, "dropContainer"), dragC = sub(dd, "dragContainer");
	if (dropC === null || dragC === null) { r.defects.push("no dropContainer / dragContainer pair"); return r; }
	const qs = items(q, "question"), drops = items(dropC, "drop"), drags = items(dragC, "drag");
	r.drags = drags.length;
	if (!(qs.length && qs.length === drops.length && drops.length === drags.length)) r.defects.push(`counts differ: questions ${qs.length} / drops ${drops.length} / drags ${drags.length}`);
	const dropOpts = new Set(drops.map((d) => optionOf(d.attrs))), dragOpts = new Set(drags.map((d) => optionOf(d.attrs)));
	for (const o of dragOpts) if (!dropOpts.has(o)) r.defects.push(`drag option ${o} has no drop`);
	for (const o of dropOpts) if (!dragOpts.has(o)) r.defects.push(`drop option ${o} has no drag`);
	if (BTN_ON && !btnOk(w)) r.defects.push("no activityButton row");
	if (/\[\s*[A-Za-z][^\]\n]{0,40}\]/.test(visible(w))) r.defects.push("raw [tag] in the visible text");
	if (/loading="lazy"/.test(w)) r.defects.push('loading="lazy" inside the widget (c83)');
	for (const qq of qs) if (!visible(qq.inner).trim()) r.defects.push("an empty question");
	for (const d of drags) {
		const vis = d.inner.replace(/<!--[\s\S]*?-->/g, " ");
		const nImg = (vis.match(/<img\b/g) || []).length;
		if (images) { if (nImg !== 1) r.defects.push(`an images drag with ${nImg} visible <img>`); }
		else if (!visible(d.inner).trim()) r.defects.push("an empty text drag");
	}
	return r;
}

(async () => {
	let totW = 0, totImg = 0, totCol = 0, totDrags = 0, totDefect = 0, totAbove = 0, mods = 0, improved = false, injected = false, injectedCol = false;
	const perMod = {};   // ROUND 501: each module's built count, for the count-vs-baseline test (_verify_count.cjs)
	for (const mod of process.argv.slice(2)) {
		let pages;
		try { pages = await convertModule(mod); } catch (e) { console.log(`${mod}: ERROR ${e.message}`); continue; }
		mods++;
		let n = 0, nImg = 0, nCol = 0, drags = 0, defect = 0; const notes = [];
		for (const p of pages) {
			for (let w of widgets(p.html)) {
				if (process.env.CV2_SELFTEST_INJECT && !injected && /layout="standard"/.test(w) && /<div class="drag" option="1">/.test(w)) {
					w = w.replace('<div class="drag" option="1">', '<div class="drag" option="99">').replace(/<img class="img-fluid/, '<img loading="lazy" class="img-fluid');
					injected = true;
				}
				if (process.env.CV2_SELFTEST_INJECT && !injectedCol && /layout="column"/.test(w) && /<div class="drag" option="1">/.test(w)) {
					w = w.replace('<div class="drag" option="1">', '<div class="drag" option="99">');   // ROUND 351 — no such drop column
					injectedCol = true;
				}
				const r = check(w); n++; if (r.images) nImg++; if (r.layout === "column") nCol++; drags += r.drags;
				if (r.defects.length) { defect += r.defects.length; notes.push(`   ${p.name}: ${r.defects.join("; ")}`); }
			}
		}
		const base = +(BASE[mod] || 0);
		if (defect > base) totAbove += defect - base;
		if (defect && defect < base) improved = true;
		totW += n; totImg += nImg; totCol += nCol; totDrags += drags; totDefect += defect; perMod[mod] = n;
		console.log(`${mod}: widgets ${n} (images ${nImg}, column ${nCol}); drags ${drags}; defect ${defect}${defect > base ? ` ✗ (above the recorded baseline ${base})` : defect ? ` ✓ (at the recorded baseline ${base})` : " ✓"}`);
		for (const l of notes.slice(0, 12)) console.log(l);
	}
	console.log(`TOTAL: ${totW} widget(s) across ${mods} module(s); images ${totImg}; column ${totCol}; drags ${totDrags}; defect ${totDefect}.`);
	// ROUND 501 (LOOP §3 step 6): the count test — ✗ when the widget count FELL against gate_baseline.json.dragdrop.
	const C = require("./_verify_count.cjs").countTest("dragdrop", { widgets: totW }, perMod, process.argv.slice(2));
	console.log(totAbove ? "RESULT: defects ABOVE the recorded baseline ✗ — fix before proceeding (gate_baseline.json.dragdrop.per_module)."
		: C.fell ? "RESULT: the built dragAndDrop count FELL against the recorded baseline ✗ — a vacuous pass (see the COUNT line)."
		: totDefect ? `RESULT: every built dragAndDrop is the KB 03B form or at its recorded baseline ✓ (${totDefect} recorded in gate_baseline.json.dragdrop${improved ? " — IMPROVED below baseline: refresh it" : ""})`
		: "RESULT: every built dragAndDrop is the KB 03B form ✓");
	process.exit(totAbove || C.fell ? 1 : 0);
})();
