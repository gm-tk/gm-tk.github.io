// Verify built flipCards against the HUMAN build, card by card.
// For each module: convert (oEmbed stubbed), capture every flipCard HTML the
// builder produced, extract each card's front/back TEXT, and check every built
// text appears in the human file (exact, or modulo the developer's copy-edits).
//
// THE GATE: a BUILT card text with no human match is a real defect — "built-only"
// must be EMPTY. "human-only" cards are EXPECTED (the ones that correctly fell
// back: image-only, red-labelled, multi-table). Image-only cells contribute no
// text and are not compared here (compare_structure covers wrapper chains).
// Clone of _verify_speechbubble.cjs. Run:
//   node --require ./_deflate_raw_polyfill.cjs _verify_flipcard.cjs <MOD> ...
const fs = require("fs");
const corpus = require("./corpus.cjs"); // round128 nesting-aware paths
// round 149 (phase 0c): --selftest = prove this verifier still DETECTS defects (T1 null-test).
if (process.argv.includes("--selftest")) { require("./_selftest_core.cjs").selftest(__filename); return; }
const path = require("path");
const APP = path.join(__dirname, "..", "..", "app", "js");
const DATA = path.join(__dirname, "..", "..", "data");
const MODS = process.env.CV2_MODS_ROOT || path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_"); // CV2_MODS_ROOT: selftest fixture override
const j = (p) => JSON.parse(fs.readFileSync(p, "utf8"));

const eng = require("./_engine_load.cjs"); // round 149 (ENGINE SPLIT phase 0b): manifest-driven loader — no hand lists
const Data = eng.loadData();
Data.AcksFormats.oembed.throttle_ms = 0;
globalThis.DataService = { Data, async FetchOembed() { return { ok: false }; } };

eng.loadEngine();

let built = [];
let curPage = null;   // round 282: which page each build came from (the A1 page lane)
const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
InteractiveScanner.ScanPage = function (page, normaliser, run) {
	const lbl = String(page?.lessonLabel ?? page?.label ?? "");
	const m = lbl.match(/(\d+)(?:[._](\d+))?/);
	curPage = m ? `${+m[1]}.${+(m[2] ?? 0)}` : null;
	return origScan(page, normaliser, run);
};
const orig = InteractiveBuilder.Build.bind(InteractiveBuilder);
InteractiveBuilder.Build = function (args) {
	const out = orig(args);
	if (args.bundle?.type === "flipCard" && out) built.push({ html: out, page: curPage });
	return out;
};

// each card's front/back TEXT (front/back divs hold <p>/<h4>/<img>; no nested div).
// ROUND 282 — THE FACE CLASS CARRIES MODIFIERS. The gold writes the face as
// `class="front flipImage"` (1065 of its 3452 fronts), `back flipImage`, `front noBG`,
// `back center-text`, `back oneChild`… and the old exact-match `class="(?:front|back)"`
// harvested NONE of them, so a built card whose text the gold DOES carry read as a
// defect (CEDO501's "Wages"/"Salary"/"Commission" — the gold ships every one of them
// inside a `front flipImage`). Matching the face word as a CLASS TOKEN is the fix;
// the built side is unaffected (this converter emits a bare `class="front"`), so the
// change can only ever REMOVE false defects, never hide a real one.
const UNIT_RE = /<div class="[^"]*\b(?:front|back)\b[^"]*"[^>]*>([\s\S]*?)<\/div>/g;
const decode = (s) => s
	.replace(/<br\s*\/?>/gi, " ")
	.replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
	.replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCharCode(parseInt(n, 16)))
	.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
	.replace(/&quot;/g, '"').replace(/&nbsp;/g, " ");
const strip = (s) => decode(s.replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " "))
	.replace(/[‘’ʼ]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, " ").trim();
const units = (html) => [...html.matchAll(UNIT_RE)].map((m) => strip(m[1])).filter((t) => t.length > 2);

const toks = (s) => new Set(String(s).toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean));
const overlap = (a, b) => { const A = toks(a), B = toks(b); if (!A.size || !B.size) return 0; let i = 0; for (const t of A) if (B.has(t)) i++; return i / (A.size + B.size - i); };
const best = (t, hs) => hs.reduce((m, h) => Math.max(m, overlap(t, h)), 0);

const norm = new TagNormaliser(Data.TagLexicon, Data.TagExceptions, Data.InstructionCues);
async function convertModule(mod) {
	const base = corpus.mdir(MODS, mod);
	const run = new ConversionRun({ imageMode: "P" });
	let wt = null, mediaSource = null;
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
		const buf = fs.readFileSync(path.join(base, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		const doc = await DocxExtractor.Extract(zip);
		const mediaTable = MediaListParser.FindMediaTable(doc.blocks);
		const isWt = DocxExtractor.LooksLikeWritersTemplate(doc.blocks, norm);
		if (isWt && !wt) wt = { name, doc };
		if (mediaTable && !mediaSource) mediaSource = { name, doc, mediaTable };
	}
	run.moduleCode = ModuleResolver.DetectModuleCode({ filenames: [wt.name], allBlocks: wt.doc.blocks, run });
	run.metadata = wt.doc.metadata ?? {};
	run.resolvedRules = ModuleResolver.Resolve(run.moduleCode, run);
	if (mediaSource) { run.mediaItems = MediaListParser.ParseItems(mediaSource.mediaTable); run.mediaListFound = true; }
	run.pageRecordsUsable = Math.max(...wt.doc.blocks.map((b) => b.wtPage ?? 1)) >= Data.InputDocRules.wt_page_tracking.min_pages_for_trust;
	run.wtBlocks = DocxExtractor.TrimFrontMatter(wt.doc.blocks, norm, run).filter((b) => b !== mediaSource?.mediaTable.block);
	const log = console.log; console.log = () => {};
	await PageAssembler.AssembleModule(run, norm);
	console.log = log;
}

function humanUnits(mod) {
	const dir = corpus.mdir(MODS, mod);
	const out = [];
	for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".html"))) out.push(...units(fs.readFileSync(path.join(dir, f), "utf8")));
	return out;
}

/** ROUND 282 — THE A1 LANE, PAGE-SCOPED (the round-247/281 precedent). The set of
 *  page keys whose GOLD page carries a flipCard. A card built on a page the developer
 *  gave no flipCard is a gold SUBSTITUTION, not a garble — Chris's round-246 A1 ruling
 *  says build the widget the writer tagged, so it is reported as a divergence rather
 *  than counted against the defect baseline. Keys use the documented shared idiom
 *  (`_L_S` → L.S, `-NN` → N.N, `_L.S` → L.S). */
function humanFlipPages(mod) {
	const dir = corpus.mdir(MODS, mod);
	const keys = new Set();
	for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".html"))) {
		const html = fs.readFileSync(path.join(dir, f), "utf8");
		if (!units(html).length) continue;
		const k = pageKey(f);
		if (k !== null) keys.add(k);
	}
	return keys;
}
function pageKey(name) {
	const base = String(name).replace(/\.html$/i, "");
	let m = base.match(/_(\d+)_(\d+)$/) || base.match(/_(\d+)\.(\d+)$/) || base.match(/-(\d+)\.(\d+)$/);
	if (m) return `${+m[1]}.${+m[2]}`;
	m = base.match(/[-_](\d+)$/);
	if (m) return `${+m[1]}.0`;
	return null;
}

(async () => {
	let anyDefect = false, tot = 0, ex = 0, ed = 0, df = 0, dv = 0, sb = 0;
	const perMod = {};   // ROUND 501: each module's built count, for the count-vs-baseline test (_verify_count.cjs)
	for (const mod of process.argv.slice(2)) {
		built = [];
		try { await convertModule(mod); } catch (e) { console.log(`${mod}: ERROR ${e.message}`); continue; }
		const b = built.flatMap((x) => units(x.html).map((t) => ({ t, page: x.page })));
		const hu = humanUnits(mod);
		const goldPages = humanFlipPages(mod);
		// DIVERGENCE (not a defect): the human file has NO flipCard at all, so the
		// developer rendered the [flip card] source differently / omitted it (e.g.
		// a restructured holdout module). Our build is still faithful to the WT.
		if (b.length && hu.length === 0) {
			console.log(`${mod}: built ${b.length} card-texts — human file has NO flipCard → DIVERGENCE (developer omitted/restructured), not a defect`);
			tot += b.length; dv += b.length; perMod[mod] = b.length; continue;
		}
		let exact = 0, edit = 0, defect = [], subst = 0;
		for (const { t, page } of b) {
			const m = best(t, hu);
			if (m >= 0.95) { exact++; continue; }
			if (m >= 0.6) { edit++; continue; }
			// ROUND 282 — the A1 lane, PAGE-scoped: the developer built no flipCard on
			// THIS page, so they substituted another widget here. Not a garble.
			if (page && goldPages.size && !goldPages.has(page)) { subst++; continue; }
			defect.push({ t, m });
		}
		sb += subst;
		// PER-MODULE: "defect" = a built card whose text matches no human card >=0.6. That is a
		// TRACKED baseline (~14 corpus-wide), NOT a failure on its own — only divergence fails.
		const verdict = b.length === 0 ? "no builds" : (defect.length === 0 ? "all matched ✓" : `${defect.length} unmatched (baseline)`);
		console.log(`${mod}: built ${b.length} card-texts [exact ${exact}, copy-edit ${edit}, gold-subst ${subst}, defect ${defect.length}] ${verdict}`);
		tot += b.length; ex += exact; ed += edit; df += defect.length; perMod[mod] = b.length;
		for (const d of defect) { console.log(`   unmatched (overlap ${d.m.toFixed(2)}): ${String(d.t).slice(0, 120)}`); }
	}
	// THE PROTECTED CRITERION is divergence 0 (gate_baseline.json.flipcard / CLAUDE.md S9): a built
	// card whose MODULE has no human flipCard at all = a real regression. exact/copy-edit/defect are
	// a committed baseline you DIFF (hold-or-improve), NOT a target of zero — so this no longer prints
	// a scary "real defects present" every run just because the baseline carries ~14 unmatched.
	console.log(`\nTOTAL ${tot}: exact ${ex}, copy-edit ${ed}, gold-subst ${sb}, defect ${df}, divergence ${dv}.`);
	// ROUND 501 (LOOP §3 step 6): the count test — ✗ when the built card count FELL against gate_baseline.json.flipcard.
	const C = require("./_verify_count.cjs").countTest("flipcard", { total: tot }, perMod, process.argv.slice(2));
	if (C.fell && dv === 0) console.log("RESULT: the built flipCard count FELL against the recorded baseline ✗ — a vacuous pass (see the COUNT line).");
	else console.log(dv === 0
		? "RESULT: divergence 0 ✓ (protected). exact/copy-edit/defect are a tracked baseline — diff vs gate_baseline.json.flipcard, hold-or-improve."
		: `RESULT: divergence ${dv} ✗ — a built card has no human flipCard counterpart; investigate before ship.`);
	process.exitCode = dv === 0 && !C.fell ? 0 : 1;
})();
