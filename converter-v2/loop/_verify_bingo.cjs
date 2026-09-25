// _verify_bingo.cjs — verify auto-built BINGO grids (round 420 — the letter-grid form of the
// BLL family's [Self check]; KB 03E COMP_04) against the human gold.
//
// WHAT A DEFECT IS HERE. A bingo is a faithful-to-source widget (Chris's A1 ruling / D10-3:
// if the writer tagged a letter grid we build the KB's bingo, whatever the developer did on
// that page), so a MISMATCH with the human is not a bug — the developer re-typed the grid,
// re-flowed it, added the snipped alphabet audio or built something else. A REAL DEFECT is
// an INTERNALLY MALFORMED unit, the thing that would reach a learner as a broken widget:
//   • a container whose `grid` is missing / not a positive integer
//   • fewer than 4 cells, or a cell without a <p> / with empty text
//   • no cell marked value="correct" (nothing to check against)
//   • a container outside a `div.bingo` wrapper, or a wrapper without the Reset / Check row
//   • a raw writer [tag] or a red-text marker in a cell
// Those are checked on the BUILD alone, so the verifier is meaningful even where the human
// shipped no bingo at all.
//
// It also reports how each built unit compares to the human, for information:
//   exact     — a human bingo on the module with the same cell multiset and the same correct count
//   copy-edit — a human bingo with the same cell count and correct count (the developer re-typed the letters)
//   dev-edit  — the human reworded / re-flowed / omitted this one (faithful, unmatchable)
//
// Run: node --require ./_deflate_raw_polyfill.cjs _verify_bingo.cjs <MOD> ...
//      node --require ./_deflate_raw_polyfill.cjs _verify_bingo.cjs --selftest
"use strict";
const fs = require("fs"), path = require("path");
const corpus = require("./corpus.cjs");
if (process.argv.includes("--selftest")) { require("./_selftest_core.cjs").selftest(__filename); return; }
const MODS = process.env.CV2_MODS_ROOT || path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_");
const eng = require("./_engine_load.cjs");
const Data = eng.loadData();
Data.AcksFormats.oembed.throttle_ms = 0;
globalThis.DataService = { Data, async FetchOembed() { return { ok: false }; } };
eng.loadEngine();
const norm = new TagNormaliser(Data.TagLexicon, Data.TagExceptions, Data.InstructionCues);

const decode = (s) => String(s || "").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
	.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");
const strip = (s) => decode(String(s || "").replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ")).replace(/\s+/g, " ").trim();

/** BALANCED inner html for the <div> opening at `start`. */
function balancedInner(html, start) {
	const i = html.indexOf(">", start);
	if (i < 0) return "";
	let depth = 1, j = i + 1, close = -1;
	while (j < html.length && depth) {
		const nx = html.indexOf("<div", j);
		close = html.indexOf("</div", j);
		if (close < 0) break;
		if (nx >= 0 && nx < close) { depth++; j = nx + 4; } else { depth--; j = close + 5; }
	}
	return html.slice(i + 1, Math.max(i + 1, close));
}

/** Every bingo WRAPPER (div.bingo) in a page/build -> { grid, cells[], correct, hasButtons, malformed[] }.
 *  A bingoContainer with no div.bingo wrapper is reported as its own (defective) unit. */
function units(html) {
	const out = [];
	const s = String(html || "");
	const seen = new Set();
	for (const m of s.matchAll(/<div\b[^>]*class="[^"]*\bbingo\b[^"]*"[^>]*>/g)) {
		const inner = balancedInner(s, m.index);
		const cm = /<div\b[^>]*class="[^"]*\bbingoContainer\b[^"]*"([^>]*)>/.exec(inner);
		const unit = { grid: null, cells: [], correct: 0, hasButtons: /\bactivityButton\b[^"]*\breset-btn\b/.test(inner) && /\bactivityButton\b[^"]*\bcheck-btn\b/.test(inner), malformed: [] };
		if (!cm) { unit.malformed.push("no bingoContainer inside the bingo wrapper"); out.push(unit); continue; }
		seen.add(m.index + inner.indexOf(cm[0]));
		const g = /\bgrid="([^"]*)"/.exec(cm[0] + cm[1]);
		unit.grid = g ? g[1] : null;
		const cinner = balancedInner(inner, inner.indexOf(cm[0]));
		for (const c of cinner.matchAll(/<div\b[^>]*class="[^"]*\bnumber\b[^"]*"([^>]*)>/g)) {
			const ci = balancedInner(cinner, c.index);
			const p = /<p\b[^>]*>([\s\S]*?)<\/p>/.exec(ci);
			const text = p ? strip(p[1]) : null;
			const isCorrect = /\bvalue="correct"/.test(c[0]);
			unit.cells.push({ text, correct: isCorrect, hasP: !!p });
			if (isCorrect) unit.correct++;
		}
		out.push(unit);
	}
	// a stray bingoContainer with no wrapper
	for (const m of s.matchAll(/<div\b[^>]*class="[^"]*\bbingoContainer\b[^"]*"[^>]*>/g)) {
		if ([...seen].some((k) => Math.abs(k - m.index) < 4)) continue;
		const before = s.slice(Math.max(0, m.index - 400), m.index);
		if (/class="[^"]*\bbingo\b[^"]*"/.test(before)) continue;   // inside a wrapper we already read
		out.push({ grid: null, cells: [], correct: 0, hasButtons: false, malformed: ["a bingoContainer outside a div.bingo wrapper"] });
	}
	return out;
}

function defects(u) {
	const d = [...u.malformed];
	const g = Number(u.grid);
	if (u.grid === null || !Number.isInteger(g) || g < 1) d.push(`grid="${u.grid}"`);
	if (u.cells.length < 4) d.push(`${u.cells.length} cell(s)`);
	if (u.cells.some((c) => !c.hasP || !c.text)) d.push("a cell without a <p> / with empty text");
	if (!u.correct) d.push("no value=\"correct\" cell");
	if (!u.hasButtons) d.push("no Reset / Check row");
	if (u.cells.some((c) => c.text && (/\[[^\]]*\]/.test(c.text) || /RED TEXT/.test(c.text)))) d.push("a raw [tag] / red marker in a cell");
	return d;
}

let built = [];
const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
InteractiveBuilder.Build = function (args) {
	const out = origBuild(args);
	if (out && args.bundle?.type === "selfCheck" && /\bbingoContainer\b/.test(out)) built.push(out);
	return out;
};

async function convertModule(mod) {
	const base = corpus.mdir(MODS, mod);
	const run = new ConversionRun({ imageMode: "P" });
	let wt = null, ms = null;
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
		const buf = fs.readFileSync(path.join(base, name));
		const doc = await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength)));
		const mt = MediaListParser.FindMediaTable(doc.blocks);
		if (DocxExtractor.LooksLikeWritersTemplate(doc.blocks, norm) && !wt) wt = { name, doc };
		if (mt && !ms) ms = { name, doc, mt };
	}
	run.moduleCode = ModuleResolver.DetectModuleCode({ filenames: [wt.name], allBlocks: wt.doc.blocks, run });
	run.metadata = wt.doc.metadata ?? {};
	run.resolvedRules = ModuleResolver.Resolve(run.moduleCode, run);
	if (ms) { run.mediaItems = MediaListParser.ParseItems(ms.mt); run.mediaListFound = true; }
	run.pageRecordsUsable = Math.max(...wt.doc.blocks.map((b) => b.wtPage ?? 1)) >= Data.InputDocRules.wt_page_tracking.min_pages_for_trust;
	run.wtBlocks = DocxExtractor.TrimFrontMatter(wt.doc.blocks, norm, run).filter((b) => b !== ms?.mt.block);
	const log = console.log; console.log = () => {};
	await PageAssembler.AssembleModule(run, norm);
	console.log = log;
}

function humanUnits(mod) {
	const dir = corpus.mdir(MODS, mod);
	const out = [];
	for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".html"))) {
		out.push(...units(fs.readFileSync(path.join(dir, f), "utf8")));
	}
	return out;
}
const multiset = (u) => u.cells.map((c) => String(c.text ?? "").toLowerCase()).sort().join("|") + "#" + u.correct;
const shape = (u) => u.cells.length + "#" + u.correct;

(async () => {
	let totalBuilt = 0, totalUnits = 0, totalCells = 0, exact = 0, copyedit = 0, diverge = 0, defect = 0, modsBuilt = 0;
	const perMod = {};   // ROUND 501: each module's built grid count, for the count-vs-baseline test (_verify_count.cjs)
	for (const mod of process.argv.slice(2)) {
		built = [];
		try { await convertModule(mod); } catch (e) { console.log(`${mod}: ERROR ${e.message}`); continue; }
		// T1 null-test: an internally MALFORMED unit the defect rule MUST flag
		// (a non-numeric grid, one empty cell, no correct cell, no button row).
		if (process.env.CV2_SELFTEST_INJECT) {
			built.push('<div class="bingo col-12"><div class="bingoContainer" grid="x"><div class="number"><p></p></div></div></div>');
		}
		if (!built.length) { console.log(`${mod}: built 0 bingos (all fell back)`); continue; }
		modsBuilt++;
		const human = humanUnits(mod);
		const hExact = new Set(human.map(multiset)), hShape = new Set(human.map(shape));
		let mE = 0, mC = 0, mV = 0, mD = 0, mUnits = 0, mCells = 0;
		for (const b of built) {
			totalBuilt++;
			for (const u of units(b)) {
				mUnits++; totalUnits++; mCells += u.cells.length; totalCells += u.cells.length;
				const d = defects(u);
				if (d.length) { mD++; console.log(`  ✗ ${mod}: ${d.join("; ")}`); continue; }
				if (hExact.has(multiset(u))) { mE++; continue; }
				if (hShape.has(shape(u))) { mC++; continue; }
				mV++;
			}
		}
		exact += mE; copyedit += mC; diverge += mV; defect += mD; perMod[mod] = mUnits;
		const verdict = mD ? `✗ ${mD} defect` : "✓ every grid well-formed";
		console.log(`${mod}: ${built.length} bingo build(s), ${mUnits} grid(s) / ${mCells} cells [exact ${mE}, copy-edit ${mC}, dev-edit ${mV}, defect ${mD}]  gold bingos ${human.length}  ${verdict}`);
	}
	console.log(`\nTOTAL: ${totalUnits} grid(s) across ${modsBuilt} module(s), ${totalCells} cells; exact ${exact}, copy-edit ${copyedit}, dev-edit ${diverge}, defect ${defect}.`);
	// ROUND 501 (LOOP §3 step 6): the count test — ✗ when the grid / cell count FELL against gate_baseline.json.bingo.
	const C = require("./_verify_count.cjs").countTest("bingo", { grids: totalUnits, cells: totalCells }, perMod, process.argv.slice(2));
	console.log(defect ? "RESULT: real defects present ✗"
		: C.fell ? "RESULT: the built bingo count FELL against the recorded baseline ✗ — a vacuous pass (see the COUNT line)."
		: "RESULT: every built bingo grid is the KB 03E form ✓");
	if (defect || C.fell) process.exitCode = 1;
})();
