// _verify_menulabels.cjs — ROUND 349 (Chris's D10-9): the lesson-menu label form (KB constraint 23 / 01B).
//
// For each module: converts it in memory (the batch_convert path) and, inside every page's #module-menu-content, checks
//   1. every learning / success LABEL (the data role_lexicon; ≤ label_max_words; colon / ellipsis or a list after it) is <h5>,
//   2. every label ends with a colon (the KB form) — when colon_form is on,
//   3. (REPORTED, not a defect) under a "We are learning:" label, items that still start with a capitalised bare verb
//      (constraint 24 wants "to …"; the writer's own "We are learning:" lists are left as written — only the normalised
//      "to"-family lists are rewritten by the engine, so this counter is information for the KB session),
//   4. on a LESSON page no section TITLE (title_lexicon) sits immediately above a label (01B line 223),
//   5. no <p> sits between an <h5> label and its list (constraint 23 "NOT intermediate <p> elements").
// A constraint-70 sentence lead-in ("Ākonga will learn …", longer than label_max_words) is not a label and is never a defect.
// Per module: labels, the five counters, defect (the sum of 1, 2, 4, 5).
//
// Usage:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_menulabels.cjs AGH1002 ENGC401 MXFL201 …
//         node --require ./_deflate_raw_polyfill.cjs _verify_menulabels.cjs --selftest
// Selftest (INJECT): with CV2_SELFTEST_INJECT the verifier turns the first <h5> label of the first menu page back into a
// <p> — the not-<h5> rule must register a defect (DETECTION); the fixture must build > 0 labels (LIVENESS).
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
const CFG = Data.EmitTemplates?.menu?.lesson_label_form || {};
const LEVEL = CFG.level ?? 5, MAXW = CFG.label_max_words ?? 8;
const LEARN = new RegExp(CFG.role_lexicon?.learning ?? "^(we are learning|learning intentions?)\\b", "i");
const SUCC = new RegExp(CFG.role_lexicon?.success ?? "^(i can|you will show your understanding|success criteria|how will i know)\\b", "i");
const TITLES = new Set((CFG.title_lexicon ?? []).map((t) => String(t).toLowerCase()));
const LEARN_LABEL = String(CFG.learning_label ?? "We are learning:");
const BASE = (() => { try { return JSON.parse(fs.readFileSync(path.join(__dirname, "gate_baseline.json"), "utf8")).menulabels?.per_module || {}; } catch { return {}; } })();
const fold = (t) => t.replace(/<[^>]+>/g, " ").replace(/&nbsp;/gi, " ").replace(/&[a-z]+;/gi, " ")
	.toLowerCase().replace(/[‘’`´]/g, "'").replace(/[^a-z0-9'āēīōū ]+/gi, " ").replace(/\s+/g, " ").trim();
const text = (inner) => inner.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();

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

/** the #module-menu-content subtree of a page (depth-balanced), or "" */
function menuOf(html) {
	const i = html.indexOf('id="module-menu-content"'); if (i < 0) return "";
	const start = html.lastIndexOf("<div", i);
	const re = /<(\/?)div\b[^>]*>/gi; re.lastIndex = start; let depth = 0, m;
	while ((m = re.exec(html)) !== null) { depth += m[1] ? -1 : 1; if (depth === 0) return html.slice(start, m.index + m[0].length); }
	return html.slice(start);
}
/** the menu's block sequence: {kind:"blk", tag, inner, f, words, role, title, colon} | {kind:"list", raw} */
function blocks(menu) {
	const els = []; const re = /<(p|h[1-6])\b[^>]*>([\s\S]*?)<\/\1>|<(ul|ol)\b[^>]*>[\s\S]*?<\/\3>/gi; let m;
	while ((m = re.exec(menu)) !== null) {
		if (m[3]) { els.push({ kind: "list", raw: m[0] }); continue; }
		const f = fold(m[2]), t = text(m[2]);
		els.push({ kind: "blk", tag: m[1].toLowerCase(), inner: m[2], f, words: f ? f.split(" ").length : 0,
			role: SUCC.test(f) ? "success" : (LEARN.test(f) ? "learning" : null),
			title: TITLES.has(f) || TITLES.has(f.replace(/\s*:$/, "")), colon: /:\s*$/.test(t), ellipsis: /(\.\.\.|…)\s*$/.test(t) });
	}
	return els;
}
const isLabel = (els, i) => { const e = els[i]; return !!(e && e.kind === "blk" && e.role && !e.title && e.words <= MAXW && (e.colon || e.ellipsis || (els[i + 1] && els[i + 1].kind === "list"))); };

(async () => {
	let totLabels = 0, totDefect = 0, totAbove = 0, mods = 0, improved = false, injected = false;
	for (const mod of process.argv.slice(2)) {
		let pages;
		try { pages = await convertModule(mod); } catch (e) { console.log(`${mod}: ERROR ${e.message}`); continue; }
		mods++;
		let labels = 0, notH5 = 0, noColon = 0, badItems = 0, titleAbove = 0, pBetween = 0;
		for (const p of pages) {
			let menu = menuOf(p.html); if (!menu) continue;
			const overview = /_0_0\.html$/i.test(p.name);
			if (process.env.CV2_SELFTEST_INJECT && !injected) {
				const k = menu.search(new RegExp(`<h${LEVEL}>[^<]*:</h${LEVEL}>`));
				if (k >= 0) { menu = menu.slice(0, k) + menu.slice(k).replace(new RegExp(`<h${LEVEL}>([^<]*:)</h${LEVEL}>`), "<p>$1</p>"); injected = true; }
			}
			const els = blocks(menu);
			for (let i = 0; i < els.length; i++) {
				const e = els[i];
				if (e.kind !== "blk") continue;
				if (!overview && e.title && isLabel(els, i + 1)) { titleAbove++; continue; }   // rule 4
				if (!isLabel(els, i)) continue;
				labels++;
				if (e.tag !== `h${LEVEL}`) notH5++;                                            // rule 1
				if (CFG.colon_form !== false && !e.colon) noColon++;                           // rule 2
				const nxt = els[i + 1];
				if (nxt && nxt.kind === "blk" && nxt.tag === "p" && els[i + 2] && els[i + 2].kind === "list" && !nxt.role) pBetween++;   // rule 5
				if (CFG.learning_to_normalise !== false && text(e.inner) === LEARN_LABEL && nxt && nxt.kind === "list") {   // rule 3
					for (const li of nxt.raw.matchAll(/<li\b[^>]*>([\s\S]*?)<\/li>/gi)) { const t = text(li[1]); if (/^[A-Z][a-z]+\b/.test(t) && !/^To\b/.test(t)) badItems++; }
				}
			}
		}
		const defect = notH5 + noColon + titleAbove + pBetween;   // badItems is reported only
		const base = +(BASE[mod] || 0);
		if (defect > base) totAbove += defect - base;
		if (defect && defect < base) improved = true;
		totLabels += labels; totDefect += defect;
		console.log(`${mod}: labels ${labels}; not-h${LEVEL} ${notH5}; no-colon ${noColon}; bare-verb items ${badItems}; title-above-label ${titleAbove}; p-between ${pBetween}; defect ${defect}${defect > base ? ` ✗ (above the recorded baseline ${base})` : defect ? ` ✓ (at the recorded baseline ${base})` : " ✓"}`);
	}
	console.log(`TOTAL: ${totLabels} label(s) across ${mods} module(s); defect ${totDefect}.`);
	console.log(totAbove ? "RESULT: defects ABOVE the recorded baseline ✗ — fix before proceeding (gate_baseline.json.menulabels.per_module)."
		: totDefect ? `RESULT: every lesson-menu label is the KB's <h${LEVEL}> form or at its recorded baseline ✓ (${totDefect} recorded in gate_baseline.json.menulabels${improved ? " — IMPROVED below baseline: refresh it" : ""})`
		: `RESULT: every lesson-menu label is the KB's <h${LEVEL}> form ✓`);
	process.exit(totAbove ? 1 : 0);
})();
