// Verify built speechBubbles against the HUMAN build, bubble by bubble.
// For each module: convert (oEmbed stubbed), capture every speechBubble HTML the
// builder produced, then extract the human file's bubbles and compare.
//
// THE GATE (revised round 247, the accordion/clickDrop A1 semantics): a REAL defect
// is an internally MALFORMED build (empty / letterless bubble text) or a PARTIAL
// text garble (overlap 0.10–0.6 with no shared image). A bubble with ~ZERO overlap
// against EVERY human bubble is the writer's own text the human SUBSTITUTED or
// omitted (MXDB302's dialogue → the gold's narrated intro + carousel) — since round
// 247's text-only branch builds the writer's tag per Chris's A1 directive, that is
// reported as "gold-subst", NOT a defect. "human-only" bubbles are EXPECTED and fine:
// they are the bubbles that correctly fell back (hover front/back, a CS-noted image,
// a video, multi-image) and were left as placeholders, so the human file still
// contains them but the builder deliberately did not.
//
// We compare the bubble TEXT (faithful-to-source is the gate) and, as a secondary
// check, the iStock image id — the wrapper CHAIN is checked by compare_structure.py.
// Clone of _verify_accordion.cjs (accHead/accContent → bubble text + image id).
// Run: node --require ./_deflate_raw_polyfill.cjs _verify_speechbubble.cjs <MOD> ...
const fs = require("fs");
const corpus = require("./corpus.cjs"); // round128 nesting-aware paths
// round 149 (phase 0c): --selftest = prove this verifier still DETECTS defects (T1 null-test).
if (process.argv.includes("--selftest")) { require("./_selftest_core.cjs").selftest(__filename); return; }
const path = require("path");
const APP = path.join(__dirname, "..", "..", "app", "js");
const DATA = path.join(__dirname, "..", "..", "data");
const MODS = process.env.CV2_MODS_ROOT || path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_"); // CV2_MODS_ROOT: selftest fixture override
const j = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
// ROUND 348 (the 16 Sept 2026 loop review, LOOP §3 step 6): the RESULT line reads ✓ AT the recorded PER-MODULE
// baseline (gate_baseline.json.speechbubble.per_module — the A/B-proven pre-existing defects: OSAI401 3, OSAH501 1 at
// r313) and ✗ ONLY above it; a module absent from the table has baseline 0. The per-module `defect N` lines and the
// TOTAL line are UNCHANGED — they are the selftest's DETECTION signal (_selftest_core.cjs sums every `defect N`).
const BASE = (() => { try { return j(path.join(__dirname, "gate_baseline.json")).speechbubble?.per_module || {}; } catch { return {}; } })();

const eng = require("./_engine_load.cjs"); // round 149 (ENGINE SPLIT phase 0b): manifest-driven loader — no hand lists
const Data = eng.loadData();
Data.AcksFormats.oembed.throttle_ms = 0;
globalThis.DataService = { Data, async FetchOembed() { return { ok: false }; } };

eng.loadEngine();

// capture built speechBubble HTML per module
let built = [];
const orig = InteractiveBuilder.Build.bind(InteractiveBuilder);
InteractiveBuilder.Build = function (args) {
	const out = orig(args);
	if (args.bundle?.type === "speechBubble" && out) built.push(out);
	return out;
};

// the bubble TEXT (the <p> inside ANY bubble-* div — left/right/basic/top/...).
// Humans put HTML comments (colour/position hints) AND an extra plain <div>
// wrapper between the bubble div and the <p>, so we skip whitespace, comments
// AND opening <div> tags before the <p>. (The builder emits the <p> immediately;
// this looseness is only needed to read the varied human gold markup.)
const TEXT_RE = /bubble-[a-z][\w-]*[^"]*"[^>]*>(?:\s|<!--[\s\S]*?-->|<div[^>]*>)*<p\b[^>]*>([\s\S]*?)<\/p>/g;
// the iStock id from a bubble (real src in Mode D / human, or the Mode-P comment).
const idOf = (html) => (html.match(/iStock-(\d{4,10})/) || [])[1] || null;
// Normalise cosmetic-only differences (entities, curly quotes, <br>, whitespace)
// so the comparison is about CONTENT, per Q1 faithful-to-source.
const decode = (s) => s
	.replace(/<br\s*\/?>/gi, " ")
	.replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
	.replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCharCode(parseInt(n, 16)))
	.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
	.replace(/&quot;/g, '"').replace(/&nbsp;/g, " ");
const strip = (s) => decode(s.replace(/<[^>]+>/g, " "))
	.replace(/[‘’ʼ]/g, "'").replace(/[“”]/g, '"')
	.replace(/\s+/g, " ").trim();
const texts = (html) => [...html.matchAll(TEXT_RE)].map((m) => strip(m[1])).filter(Boolean);

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

// human bubble texts + image ids from the finished file(s)
function humanData(mod) {
	const dir = corpus.mdir(MODS, mod);
	let allText = [], allHtml = "";
	for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".html"))) {
		const html = fs.readFileSync(path.join(dir, f), "utf8");
		allText.push(...texts(html));
		allHtml += html;
	}
	const ids = new Set([...allHtml.matchAll(/iStock-(\d{4,10})/g)].map((m) => m[1]));
	return { humanTexts: allText, ids };
}

// Word-set (Jaccard) overlap — so we can tell a faithful build that differs only
// by the developer's COPY-EDITS (Q1: keep the source wording, human edited it →
// high overlap, NOT a defect) from a genuine builder error (no human match → low
// overlap). Mirrors the hintSlider/accordion note "residual diffs are human edits".
const toks = (s) => new Set(String(s).toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean));
const overlap = (a, b) => {
	const A = toks(a), B = toks(b);
	if (!A.size || !B.size) return 0;
	let inter = 0; for (const t of A) if (B.has(t)) inter++;
	return inter / (A.size + B.size - inter);
};
const bestMatch = (text, humanTexts) => humanTexts.reduce((best, h) => Math.max(best, overlap(text, h)), 0);
// ROUND 276 — THE HUMAN-MERGE LANE (the round-197 label-truncation rule generalised).
// The developer routinely MERGES two adjacent writer bubbles into one longer bubble
// (TEDC402-3.0: the writer's "Nice! You're peeling back the layers…" is the opening
// sentence of a human bubble that also carries the next writer bubble's text). The
// build is complete and faithful — every word of it is in the human bubble — but the
// Jaccard overlap lands at ~0.25 and the old rule called that a partial garble.
// CONTAINMENT is the discriminator: a genuinely garbled build carries words the human
// does not have, so it can never be contained. Guarded to >= 4 tokens so a one-word
// bubble cannot be "contained" by coincidence.
const containedIn = (text, humanTexts) => {
	const A = toks(text);
	if (A.size < 4) return false;
	return humanTexts.some((h) => { const B = toks(h); for (const t of A) if (!B.has(t)) return false; return true; });
};

(async () => {
	let anyDefect = false, anyAbove = false, improved = false, totBuilt = 0, totExact = 0, totEdit = 0, totDefect = 0, totDiverge = 0, totSubst = 0, idMiss = 0;
	for (const mod of process.argv.slice(2)) {
		built = [];
		try { await convertModule(mod); } catch (e) { console.log(`${mod}: ERROR ${e.message}`); continue; }
		// T1 null-test (round 247, the accordion inject pattern): a MALFORMED sample the
		// malformation rule MUST flag — mangled gold is the wrong probe now that a
		// zero-overlap writer-faithful bubble is the tolerated gold-subst lane.
		if (process.env.CV2_SELFTEST_INJECT) built.push('<div class="bubble-basic no-hover"><p>?!?</p></div>');
		// ROUND 306 — HARVEST CORRECTION (the r283 clickDrop precedent: a fuller read can
		// only REMOVE false defects; the DETECTION channel is unchanged). The old read took
		// texts(h)[0] — the FIRST <p> of the whole Build output — so (a) a LABEL-FIRST
		// multi-paragraph bubble was judged on its 2-word label alone (ENGI202's faithful
		// "Kaitiakitanga | Guardianship" + whakataukī + translation scored 0.13 against the
		// human's identical one-<p> form and read as a garble), and (b) a multi-ROW build
		// counted as ONE bubble. Harvest PER BUBBLE ROW, all its <p>s joined — the honest
		// comparison unit either way.
		const builtBubbles = built.flatMap((h) => {
			const rows = h.split(/(?=<div class="row speechBubble)/).filter((s) => /bubble-[a-z]/.test(s));
			const units = rows.length ? rows : [h];
			return units.map((rowHtml) => {
				const bi = rowHtml.search(/bubble-[a-z]/);
				const seg = bi >= 0 ? rowHtml.slice(bi) : rowHtml;
				const ps = [...seg.matchAll(/<p\b[^>]*>([\s\S]*?)<\/p>/g)].map((m) => strip(m[1])).filter(Boolean);
				return { text: ps.join(" ").replace(/\s+/g, " ").trim(), id: idOf(rowHtml) };
			});
		});
		const { humanTexts, ids } = humanData(mod);
		let exact = 0, edit = 0, diverge = 0, subst = 0, defect = [];
		const malformed = (t) => !/[\p{L}\p{N}]/u.test(String(t ?? ""));
		for (const b of builtBubbles) {
			const m = bestMatch(b.text, humanTexts);
			if (malformed(b.text)) defect.push({ ...b, m, why: "malformed" });   // empty/letterless build → always a real defect
			else if (m >= 0.95) exact++;
			else if (m >= 0.6) edit++;           // faithful build; human copy-edited
			else if (b.id && ids.has(b.id)) diverge++;   // SAME image in the human, text reworded → developer rewrote the bubble (faithful build, Q1) — not a defect
			else if (containedIn(b.text, humanTexts)) edit++;   // round 276: every word of the build is inside one human bubble → the human MERGED writer bubbles, not a garble
			else if (m < 0.10) subst++;          // ~ZERO overlap with every human bubble → the human substituted/omitted the writer's bubble (A1, round 247) — reported, not a defect
			else defect.push({ ...b, m });               // partial garble: some overlap, no image → real concern
		}
		const idMisses = builtBubbles.filter((b) => b.id && !ids.has(b.id));
		const base = +(BASE[mod] || 0);   // ROUND 348: this module's recorded baseline (0 when unrecorded)
		const verdict = builtBubbles.length === 0 ? "no builds"
			: defect.length === 0 ? "OK ✓ (built⊆human, modulo copy-edits / dev-rewrites / gold-subst)"
			: defect.length <= base ? `OK ✓ (at the recorded baseline ${base}${defect.length < base ? " — IMPROVED, refresh gate_baseline.json" : ""})`
			: `DEFECT ✗ (above the recorded baseline ${base})`;
		if (defect.length > base) anyAbove = true;
		if (defect.length && defect.length < base) improved = true;
		console.log(`${mod}: built ${builtBubbles.length} [exact ${exact}, copy-edit ${edit}, dev-edit ${diverge}, gold-subst ${subst}, defect ${defect.length}] ${verdict}${idMisses.length ? ` | image-id miss ${idMisses.length}` : ""}`);
		totBuilt += builtBubbles.length; totExact += exact; totEdit += edit; totDefect += defect.length; totDiverge += diverge; totSubst += subst;
		for (const d of defect) { anyDefect = true; console.log(`   DEFECT (overlap ${d.m.toFixed(2)}${d.why ? ", " + d.why : ""}): ${d.text.slice(0, 120)}`); }
		if (idMisses.length) { idMiss += idMisses.length; for (const b of idMisses) console.log(`   image-id not in human file: iStock-${b.id}`); }
	}
	console.log(`\nTOTAL built ${totBuilt}: exact ${totExact}, copy-edit ${totEdit}, dev-edit ${totDiverge}, gold-subst ${totSubst}, defect ${totDefect}; image-id misses ${idMiss}.`);
	// ROUND 348: ✓ at the recorded baseline, ✗ only above it (LOOP §3 step 6). anyDefect still says whether ANY defect
	// exists at all (the pre-r348 wording is kept as a parenthetical so a reader sees the baseline is not zero).
	console.log(anyAbove ? "RESULT: defects ABOVE the recorded baseline ✗ — fix before proceeding (gate_baseline.json.speechbubble.per_module)."
		: anyDefect ? `RESULT: every built bubble is human-matched, writer-faithful (gold-subst) or at its recorded baseline ✓ (${totDefect} recorded in gate_baseline.json.speechbubble${improved ? " — IMPROVED below baseline: refresh it" : ""})`
		: "RESULT: every built bubble is human-matched or writer-faithful (gold-subst) ✓");
	process.exitCode = anyAbove ? 1 : 0;
})();
