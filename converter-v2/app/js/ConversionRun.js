/**
 * ConversionRun.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * The state object for ONE conversion (one module, one upload). Every
 * pipeline stage reads from and writes to this instance instead of passing
 * a dozen loose variables around. It is also the single tally point for
 * everything the conversion summary reports: red flags, ACK-TODOs,
 * interactives, and notes.
 *
 * WHY AN INSTANCE CLASS:
 * Standards §3b — state belongs to an instance. The services around it
 * (PageSplitter, ContentConverter, …) stay static and stateless.
 *
 * THE SURFACING CONTRACT (one of the project's core rules):
 * Nothing ambiguous is ever swallowed quietly. Anything a pipeline stage
 * cannot cleanly decide is recorded HERE via AddNote() / CountRedFlag() /
 * CountAckTodo(), so the on-screen conversion summary shows it to the
 * developer. If a stage "handles" a discrepancy without tallying it here,
 * that is a bug.
 *
 * WHEN TO WORK HERE:
 * - Adding a new field that a later pipeline stage needs to read or write.
 * - Adding a new kind of tally or note the summary panel should display.
 * Do NOT put decision-making logic in this file — it is a plain data
 * container. The actual thinking lives in the pipeline stages.
 * ===========================================================================
 */

class ConversionRun {

	/**
	 * @param {Object} options
	 * @param {string} options.imageMode - "P" (placeholder) or "D" (direct)
	 * @param {string} options.interactiveMode - How to handle an interactive
	 *   widget the converter has NOT yet learned to build:
	 *     "inline"  (default) — draw a dashed placeholder box where the widget
	 *                belongs, so the page still shows its position.
	 *     "extract" — do NOT draw the box; instead drop a single loud reference
	 *                code at that spot and hand the captured widget content off in
	 *                a separate file, {CODE}_interactives.txt (a to-do list for
	 *                the human developer). This is the "hand-off" mode.
	 *   The choice is uniform across the whole module (just like imageMode).
	 *   ROUND 235 (Chris): the hand-off is now the DEFAULT — when the option is
	 *   omitted, BOTH entries (browser + batch) resolve it from the data flag
	 *   Emit_Templates.interactive_placeholder.extract.default_mode via
	 *   DefaultInteractiveMode() below (shared code, so entry parity holds by
	 *   construction). The former UI switch is gone; env INTCOLLAPSE_OFF reverts
	 *   the default to "inline" (the pre-round behaviour), and the legacy
	 *   INTEXTRACT_ON force is still honoured for A/B harness runs.
	 */
	constructor({ imageMode = "P", interactiveMode = null } = {}) {
		if (interactiveMode == null) interactiveMode = ConversionRun.DefaultInteractiveMode();
		if (imageMode !== "P" && imageMode !== "D") {
			throw new Error(`ConversionRun: imageMode must be "P" or "D", got "${imageMode}"`);
		}
		if (interactiveMode !== "inline" && interactiveMode !== "extract") {
			throw new Error(`ConversionRun: interactiveMode must be "inline" or "extract", got "${interactiveMode}"`);
		}

		// --- upload-time choice (uniform across the whole run — brief §8.1)
		this.imageMode = imageMode;
		this.interactiveMode = interactiveMode;
		// per-page running counter for the extract-mode reference codes
		// ({CODE}-{NN}-{seq}); keyed by page index, only touched in "extract" mode.
		this.extractCounters = new Map();
		// OPTIONAL progress callback — only the browser ever sets this. Shape:
		//   (stage, done, total) => void
		//   e.g. onProgress("pages", 3, 12)  // "finished 3 of 12 pages"
		// The browser entry point (App.js) sets it to drive the Convert-panel
		// progress bar. The command-line/batch test harness NEVER sets it, so
		// every place the engine calls it is a safe no-op during batch runs.
		// This is display-only machinery: nothing here changes a single byte of
		// the HTML the converter produces.
		this.onProgress = null;

		// --- module identity (filled in later by ModuleResolver) -----------
		this.moduleCode = null;       // the module's code, e.g. "OSAH401"
		this.codeSource = null;       // note on where the code was found (shown in the summary)
		// The "rules" describing how THIS module should be built (page layout,
		// menu style, heading levels, …), worked out by ModuleResolver. It is a
		// plain object, e.g.:
		//   { body_class: "standard", page_model: "multi-file",
		//     menu_type: "tabs", template_phase: "9-10", ... }
		this.resolvedRules = null;
		this.resolutionPath = null;   // which rule sources supplied each value (shown in the summary)
		// ROUND 249 — the REFERENCE-MODULE choices (both null unless the person
		// explicitly chose one in the upload UI; the batch harness never sets
		// them, so the default path is byte-identical to the pre-round engine):
		// referenceCode = a library module code chosen to inherit page structure
		// from instead of this module's own registry home; referenceDistilled =
		// the ReferenceMiner.Distil result when reference HTML pages were
		// uploaded (its .file object also ships as {CODE}_reference-template.json).
		this.referenceCode = null;
		this.referenceDistilled = null;
		this.englishTitle = "";       // English title from the [TITLE BAR] line, e.g. "Staying safe online"
		this.teReoTitle = "";         // te reo Māori title, if the module has one
		// Some families (e.g. the "BLL" phonics modules) prefix their title bar
		// with "Module N - ...". When we strip that prefix we remember it here so
		// later stages render it exactly like the human developer does.
		// false = this module has no such prefix.
		this.modulePrefix = false;
		// The information table from the top of the Writers Template. A plain
		// object, e.g.: { Subject: "English", Course: "...", "Contact person": "..." }
		this.metadata = {};

		// --- inputs (filled by App / the ingest step) ----------------------
		// The Writers Template content, split into "blocks" (paragraphs, tables,
		// images, lists, …) AFTER the front-matter has been trimmed off. Each
		// block is an object built by DocxExtractor, e.g.:
		//   { type: "paragraph", text: "Welcome", runs: [ ... ] }
		this.wtBlocks = [];
		// The parsed Media List — one entry per media item, e.g.:
		//   [ { number: 1, kind: "image", url: "https://...", caption: "..." }, ... ]
		this.mediaItems = [];
		this.mediaListFound = false;    // did we actually find a Media List document? true / false
		// ROUND 235 (Chris) — the optional VERIFIED iStock acknowledgements file
		// (*_istock-acks.txt, sourced from the iStock API via Getty Images). Parsed
		// by AcksBuilder.ParseIstockAcks in ModuleResolver.PrepareRun into a Map of
		// asset id → { title, line }; null when no file was supplied (or the
		// feature is off — data Acks_Formats.istock_acks_file / env ISTOCKACKS_OFF).
		this.istockAcks = null;
		// ROUND 236 (Chris) — sourcing honesty for iStock TITLES.
		// istockAcksSupplied: was an acknowledgements file supplied AT ALL? (A
		// file that covers nothing still counts — "no file" and "file that
		// misses this asset" are different messages to the designer.)
		// istockUnverified: the asset ids whose titles had to be derived from
		// the image URL instead of verified against the iStock API. Each such
		// line ships the ❗ marker and the acks block carries one red note.
		// Data Acks_Formats.istock_unverified · env ISTOCKUNVERIFIED_OFF.
		this.istockAcksSupplied = false;
		this.istockUnverified = [];
		// Does the Writers Template's own page numbering look trustworthy enough
		// to split the module into pages by? Decided by a data rule. true / false.
		this.pageRecordsUsable = false;

		// --- pipeline products (built up as the conversion runs) -----------
		// The module split into pages / lessons by PageSplitter. Each page is an
		// object carrying its items, title, number, etc. (see PageSplitter.js).
		this.pages = [];
		// Every interactive widget we captured — whether or not we could build
		// it. Used to write the {CODE}_interactives.txt hand-off list. e.g.:
		//   [ { type: "flipCard", members: [ ... ], pageIndex: 2 }, ... ]
		this.interactives = [];
		// The finished files this run hands back. Each entry looks like:
		//   { filename: "OSAH401-01.html", content: "<!DOCTYPE ...>", kind: "page" }
		// kind is "page" for a lesson page, or another label for support files.
		this.outputs = [];

		// --- the tallies the summary panel reports -------------------------
		this.redFlagCount = 0;        // how many red "RED FLAG" paragraphs we emitted
		this.ackTodoCount = 0;        // how many "❗" acknowledgement-to-do lines we emitted
		// Decisions/warnings surfaced for the summary panel, e.g.:
		//   [ { level: "warn", stage: "PageSplitter", text: "Adjacent tags merged" }, ... ]
		// level is one of: "info" | "warn" | "error".
		this.notes = [];
	};

	/**
	 * Resolves the run's DEFAULT interactive mode (ROUND 235, Chris) — the one
	 * shared decision both entry points use when no explicit interactiveMode is
	 * passed, so the browser app and the batch harness can never drift apart on
	 * it (the r185 entry-parity principle: shared code, not per-entry logic).
	 *
	 * Resolution order (reproducing the r234 A/B matrix exactly):
	 *  1. env INTEXTRACT_ON    → "extract" (the legacy r138 explicit force —
	 *     with INTCOLLAPSE_OFF also set, the extract branch skips the collapse
	 *     wrap, i.e. the r234 bare-marker extract, byte-for-byte)
	 *  2. env INTCOLLAPSE_OFF  → "inline" (the r234 default, byte-for-byte)
	 *  3. data Emit_Templates.interactive_placeholder.extract.default_mode
	 *     ("extract" = the shipped hand-off default) when the extract feature is
	 *     enabled; anything else → "inline".
	 *
	 * @returns {string} "extract" or "inline"
	 */
	static DefaultInteractiveMode() {
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		if (env.INTEXTRACT_ON) return "extract";
		if (env.INTCOLLAPSE_OFF) return "inline";
		const ex = (typeof DataService !== "undefined" && DataService.Data)
			? DataService.Data.EmitTemplates?.interactive_placeholder?.extract : null;
		return (ex && ex.enabled !== false && ex.default_mode === "extract") ? "extract" : "inline";
	};

	/**
	 * Records a surfaced decision/discrepancy for the summary panel.
	 *
	 * USAGE:
	 * run.AddNote("warn", "PageSplitter", "Adjacent boundary tags merged …");
	 *
	 * @param {string} level - "info" | "warn" | "error"
	 * @param {string} stage - which pipeline stage is reporting
	 * @param {string} text - human-readable explanation
	 */
	AddNote(level, stage, text) {
		this.notes.push({ level, stage, text });
		// mirror to the console so a developer watching DevTools sees the
		// pipeline narrate itself (emoji convention from the standards)
		const icon = level === "error" ? "🔴" : (level === "warn" ? "🟠" : "🟢");
		console.log(`${icon} [${stage}] ${text}`);
	};

	/** Tally one emitted RED FLAG paragraph (called by the one emitter). */
	CountRedFlag() { this.redFlagCount++; };

	/** Tally one emitted ❗ ACK-TODO line (called by AcksBuilder only). */
	CountAckTodo() { this.ackTodoCount++; };

	/**
	 * The summary object the UI renders for this run.
	 * @returns {Object} plain data for SummaryReporter
	 */
	Summary() {
		return {
			moduleCode: this.moduleCode,
			codeSource: this.codeSource,
			imageMode: this.imageMode,
			interactiveMode: this.interactiveMode,
			files: this.outputs.map((o) => o.filename),
			pageCount: this.outputs.filter((o) => o.kind === "page").length,
			interactiveCount: this.interactives.length,
			redFlagCount: this.redFlagCount,
			ackTodoCount: this.ackTodoCount,
			mediaListFound: this.mediaListFound,
			notes: this.notes,
			// module-identity fields for the frontend (and future use):
			// subject/course/contact from the front-matter table, plus the
			// resolved titles
			metadata: {
				...this.metadata,
				englishTitle: this.englishTitle,
				teReoTitle: this.teReoTitle,
			},
		};
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ConversionRun };
