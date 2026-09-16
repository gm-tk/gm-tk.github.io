/**
 * batch_convert.cjs
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Mass-converts real modules with the actual app classes: for every module
 * in module_type_representatives.json + module_type_holdout.json (the
 * most-recent + second-most-recent module of EVERY series×level type —
 * "two per type, or one if that's all there is"), it converts the Writers
 * Template + Media List docx from 01-Finalized_Modules_/<CODE>/ and writes
 * the outputs to 01-Claude_Modules_/<CODE>/.
 *
 * RESUME + AUDIT:
 * Each finished module writes 01-Claude_Modules_/<CODE>/_run.json (summary,
 * notes, error if any). Re-running skips modules that already have one —
 * delete the folder (or pass --force) to redo. Progress is appended to
 * batch_progress.log next to this script; the rolled-up results land in
 * batch_results.json.
 *
 * USAGE:
 *   node batch_convert.cjs            convert everything not yet done
 *   node batch_convert.cjs CODE …     convert specific modules only
 *   node batch_convert.cjs --force    redo everything
 * ===========================================================================
 */
"use strict";

const fs = require("fs");
const corpus = require("./corpus.cjs"); // round128 nesting-aware paths
const path = require("path");
const APP = path.join(__dirname, "..", "..", "app", "js");
const DATA = path.join(__dirname, "..", "..", "data");
const MODS = path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_");
const OUT = path.join(__dirname, "..", "..", "..", "01-Claude_Modules_");
const LOG = path.join(__dirname, "batch_progress.log");
const RESULTS = path.join(__dirname, "batch_results.json");
const j = (p) => JSON.parse(fs.readFileSync(p, "utf8"));

// ---- load the app classes (browser globals via the node hook) -------------
// ROUND 149 (ENGINE SPLIT phase 0b): the ordered engine list + the canonical data map
// live in app/js/_modules.json, loaded through the ONE shared loader (_engine_load.cjs).
// No more hand-maintained per-harness lists (the r97-104 vacuous-verifier failure mode).
const eng = require("./_engine_load.cjs");

const Data = eng.loadData();

// batch-friendly oEmbed: cached across ALL modules AND across chunked runs
// (the cache persists to oembed_cache.json so resumed batches never re-fetch)
Data.AcksFormats.oembed.throttle_ms = 40;
const CACHE_FILE = path.join(__dirname, "oembed_cache.json");
// ROUND 348: parallel workers (the _r341+ full-regeneration runners, 4 at a time) SHARE this file. The old save was a
// plain writeFileSync (truncate + write) that EVERY worker ran at exit — even under STUB_OEMBED, when the cache is never
// consulted and nothing had changed — so a worker starting up read a torn file and died in JSON.parse before converting
// anything (≈ 3 of 36 batches on every full regeneration r341–r347, each re-run singly). Now: the read tolerates a
// torn / corrupt file (warn, start empty — it is only a cache); the save is skipped when nothing changed, merges the
// file's current entries (a parallel worker's fetches are not lost), and is ATOMIC — a .pid.tmp renamed over the target,
// so a concurrent reader sees the old file or the new one, never a torn one.
const readCache = () => { if (!fs.existsSync(CACHE_FILE)) return {}; try { return j(CACHE_FILE); } catch (e) { console.error(`oembed cache unreadable (${e.message}) — starting empty`); return {}; } };
const oembedCache = new Map(Object.entries(readCache()));
let cacheDirty = 0;
const saveCache = () => {
	if (!cacheDirty) return;
	const merged = { ...readCache(), ...Object.fromEntries(oembedCache) };
	const tmp = `${CACHE_FILE}.${process.pid}.tmp`;
	fs.writeFileSync(tmp, JSON.stringify(merged));
	fs.renameSync(tmp, CACHE_FILE);
	cacheDirty = 0;
};
globalThis.DataService = {
	Data,
	async FetchOembed(url, id) {
		if (process.env.STUB_OEMBED) return { ok: false, reason: "stubbed" };   // fast structure-gate re-batch (acks excluded from compare_structure)
		if (oembedCache.has(id)) return oembedCache.get(id);
		let r;
		try {
			const res = await fetch(`https://www.youtube.com/oembed?url=${encodeURIComponent(url)}&format=json`,
				{ signal: AbortSignal.timeout(3500) });
			const t = res.ok ? await res.text() : "";
			r = t ? { ok: true, title: JSON.parse(t).title, channel: JSON.parse(t).author_name }
				: { ok: false, reason: "unavailable" };
		} catch { r = { ok: false, reason: "error" }; }
		oembedCache.set(id, r);
		if (++cacheDirty % 20 === 0) saveCache();
		return r;
	},
};

eng.loadEngine();
const norm = new TagNormaliser(Data.TagLexicon, Data.TagExceptions, Data.InstructionCues);

const log = (line) => {
	fs.appendFileSync(LOG, `${new Date().toISOString().slice(11, 19)} ${line}\n`);
};

/**
 * Converts one module folder exactly the way App.js does — LITERALLY, since
 * ROUND 185: both entries call the ONE shared prep sequence
 * (ModuleResolver.PrepareRun — the D0 parity fix; the entries had drifted and
 * produced different output for the same module, HPFUN903). This function
 * keeps only what is genuinely batch-specific: reading the .docx bytes from
 * disk, and throwing on a refusal (App renders the summary instead).
 * `_verify_entry_parity.cjs` guards the contract.
 */
async function convertModule(mod) {
	const base = corpus.mdir(MODS, mod);
	// ROUND 235 (Chris) — interactiveMode is no longer forced per-entry: the run
	// resolves its own default (ConversionRun.DefaultInteractiveMode — the data-driven
	// hand-off default, shared with the browser app so the entries cannot drift).
	// The legacy env INTEXTRACT_ON force and the round-reverting INTCOLLAPSE_OFF are
	// both honoured INSIDE that shared resolver.
	const run = new ConversionRun({ imageMode: "P" });

	const docs = [];
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
		const buf = fs.readFileSync(path.join(base, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		docs.push({ name, doc: await DocxExtractor.Extract(zip) });
	}
	// ROUND 235 (Chris) — the optional verified iStock acknowledgements file
	// alongside the module's .docx inputs; parsed inside PrepareRun (shared
	// prep — entry parity), inert when absent (the corpus module folders carry
	// none).
	// ROUND 236 — hand in EVERY .txt in the folder rather than name-matching
	// one: AcksBuilder.PickIstockAcks decides from the CONTENTS, exactly as it
	// does for the browser's uploads. Measured safe here — all 559 .txt files
	// beside the corpus .docx inputs are "*_parsed.txt" WT dumps and not one
	// contains a single acknowledgement line, so none can be mistaken for the
	// acks file.
	const istockAcksFiles = fs.readdirSync(base)
		.filter((f) => /\.txt$/i.test(f))
		.map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));

	const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
	if (!prep.ok && prep.reason === "no-wt") throw new Error("no Writers Template (no content opener found)");
	if (!prep.ok && prep.reason === "unsupported") throw new Error(`refused by design: ${prep.unsupported.label}`);

	await PageAssembler.AssembleModule(run, norm);
	return run;
}

(async () => {
	const args = process.argv.slice(2);
	const force = args.includes("--force");
	const picked = args.filter((a) => !a.startsWith("--"));

	// the chosen set, in priority order:
	//   1. explicit CODE args, else
	//   2. compare_set.txt — the reconciled list Chris signed off (round 43): EXACTLY
	//      the modules that live in 01-Claude_Modules_, all developed in the last 18
	//      months. This is the canonical default so a no-arg regen can never re-create
	//      deleted (out-of-list) folders. Edit that file to change the set.
	//   3. (fallback) every representative + holdout, deduped — the legacy auto-set.
	const csPath = path.join(__dirname, "compare_set.txt");
	let modules;
	if (picked.length) {
		modules = picked;
	} else if (fs.existsSync(csPath)) {
		modules = fs.readFileSync(csPath, "utf8").split(/\r?\n/).map((s) => s.trim()).filter(Boolean).sort();
	} else {
		const reps = j(path.join(__dirname, "module_type_representatives.json"));
		const hold = j(path.join(__dirname, "module_type_holdout.json"));
		modules = [...new Set([...Object.values(reps), ...Object.values(hold)])].sort();
	}

	fs.mkdirSync(OUT, { recursive: true });
	// ROUND 349: batch_results.json is the SECOND file the parallel workers race on (the r348 fix covered the oembed cache):
	// a torn-tolerant read (it is a diagnostic ledger — warn and start empty) and, below, an atomic MERGED write.
	const readResults = () => { if (!fs.existsSync(RESULTS)) return {}; try { return j(RESULTS); } catch (e) { console.error(`batch_results.json unreadable (${e.message}) — starting empty`); return {}; } };
	const results = readResults();
	const saveResults = () => {
		const merged = { ...readResults(), ...results };   // another worker's rows are kept; this worker's rows win
		const tmp = `${RESULTS}.${process.pid}.tmp`;
		fs.writeFileSync(tmp, JSON.stringify(merged, null, 1));
		fs.renameSync(tmp, RESULTS);
	};

	log(`BATCH START — ${modules.length} modules`);
	let done = 0;
	for (const mod of modules) {
		const outDir = corpus.mdir(OUT, mod);
		const marker = path.join(outDir, "_run.json");
		if (!force && fs.existsSync(marker)) { done++; continue; }   // resume
		if (!fs.existsSync(corpus.mdir(MODS, mod))) {
			results[mod] = { error: "module folder missing" };
			log(`SKIP ${mod}: folder missing`);
			continue;
		}

		// mute the pipeline's console narration during batch (everything it
		// says is captured in the run summary notes anyway)
		const orig = console.log;
		console.log = () => {};
		let entry;
		try {
			const run = await convertModule(mod);
			fs.rmSync(outDir, { recursive: true, force: true });
			fs.mkdirSync(outDir, { recursive: true });
			for (const o of run.outputs) fs.writeFileSync(path.join(outDir, o.filename), o.content);
			entry = { ...run.Summary(), error: null };
		} catch (e) {
			fs.mkdirSync(outDir, { recursive: true });
			entry = { moduleCode: mod, error: e.message };
		} finally {
			console.log = orig;
		}
		fs.writeFileSync(marker, JSON.stringify(entry, null, 1));
		results[mod] = entry;
		saveResults();
		done++;
		log(`${done}/${modules.length} ${mod} ${entry.error ? `ERROR: ${entry.error}` : `ok (${entry.pageCount} pages, ${entry.interactiveCount} interactives, ${entry.redFlagCount} flags, ${entry.ackTodoCount} ackTodos)`}`);
	}
	saveCache();
	log(`BATCH COMPLETE — ${done}/${modules.length}`);
})().catch((e) => { saveCache(); log(`BATCH FATAL: ${e.stack ?? e}`); process.exit(1); });
