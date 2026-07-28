/**
 * App.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * The orchestrator for the BROWSER version of the converter — loaded LAST,
 * after every other engine file. This is the file that runs when a real
 * person opens index.html in their browser, drops in a Writers Template
 * (WT — the source .docx a writer fills in with [bracketed tags] like [H2]
 * or [Activity]) and usually its companion Media List (a second .docx
 * listing the URL/caption for every image, video and audio used in that
 * module), and clicks Convert. It wires up the upload UI, runs the startup
 * sequence (file:// guard → load data → compile the tag matcher), and then
 * drives one conversion per click: classify the uploads (WT / media list /
 * combined), run the shared pipeline stages in order, then hand the
 * finished output files to the download list and the summary panel.
 *
 * THIS IS ONE OF TWO ENTRY POINTS:
 * A separate, parallel entry point exists for automated/bulk conversion
 * from the command line — batch_convert.cjs, a Node.js script — which does
 * NOT load or use this file at all. Both entry points funnel their critical
 * setup (classifying the uploads, detecting the module code, resolving its
 * structural rules, parsing the Media List, trimming front-matter) through
 * the SAME shared engine method, ModuleResolver.PrepareRun (see stage [3]
 * inside #convert(), below), specifically so the browser tool and the
 * command-line tool can never silently drift apart and produce different
 * output for the same input document.
 *
 * STARTUP SEQUENCE (one big try/catch, standards §8a) — see Init():
 *   file:// guard → DataService.Init() → new TagNormaliser(...) → wire up
 *   the upload UI → ready for a click.
 *
 * CONVERSION SEQUENCE (one big try/catch, standards §8a) — see #convert(),
 * which runs once per click of the Convert button:
 *   read the upload-time option checkboxes → extract every uploaded .docx
 *   into blocks → the shared prep (ModuleResolver.PrepareRun) → build every
 *   output page (PageAssembler.AssembleModule) → render the download list
 *   and the run summary.
 *
 * WHY THE file:// GUARD:
 * The engine fetches ../data/*.json at runtime (edit a data file → reload
 * → converted output changes — the whole point). Browsers block fetch on
 * file:// pages, so double-clicking index.html cannot work; the guard
 * explains the one-command local server instead of failing silently.
 * ===========================================================================
 */

class App {

	static #normaliser = null;   // compiled matcher (built once at startup)
	static #files = [];          // uploaded .docx File objects awaiting conversion
	// ROUND 235 (Chris) — the optional verified iStock acknowledgements file
	// (*_istock-acks.txt, API-sourced via Getty Images). Kept SEPARATE from
	// #files: it is not a .docx, must not enter the docx-extraction loop, and
	// does not count toward the two-docx-per-run limit.
	static #istockAcksFile = null;

	/**
	 * STARTUP. Runs once, when the page finishes loading (wired up at the
	 * very bottom of this file via a DOMContentLoaded listener). Everything
	 * the app needs before a person can click "Convert" happens here, in
	 * order, inside one try/catch (standards §8a) — so a startup failure is
	 * caught and shown loudly instead of leaving a half-initialised page
	 * that looks fine but silently doesn't work.
	 *
	 * THE STARTUP SEQUENCE, STEP BY STEP:
	 *   1. file:// GUARD — if this page was opened by double-clicking
	 *      index.html (protocol "file:") instead of being served over
	 *      http://, hide the whole app UI, show the file:// warning panel
	 *      instead, and return early — nothing else below is safe to run
	 *      yet (see "WHY THE file:// GUARD" at the top of this file).
	 *   2. DataService.Init() — fetches and parses every runtime
	 *      configuration/data JSON file the engine needs (the tag lexicon,
	 *      tag exceptions, instruction-cue vocabulary, and every other
	 *      data-driven rule file under data/*.json). This is awaited
	 *      because nothing below — or later, during a conversion — can run
	 *      correctly until it has finished.
	 *   3. Build the TagNormaliser — the compiled matcher that recognises
	 *      and classifies every [bracketed tag] a writer used in their
	 *      Writers Template (e.g. working out that "[h2]", "[H2]" and a
	 *      stray "[Heading 2]" all mean the same tag). It is built ONCE
	 *      here, from the lexicon/exceptions/instruction-cue data just
	 *      loaded, and then reused for every conversion click for the rest
	 *      of this browser session — it is never rebuilt per conversion.
	 *   4. Stamp the build version onto the page (a small "build …" label)
	 *      purely so a developer looking at the running page can tell at a
	 *      glance whether the code they just edited is actually the code
	 *      that's live.
	 *   5. #wireUi() — attach every click/drag/drop event listener the
	 *      upload UI and the Convert button need.
	 *   6. Log "ready to convert" and stop. The app now just waits for a
	 *      person to drop in files and click Convert, which is handled
	 *      entirely separately by #convert() (see CONVERSION SEQUENCE at
	 *      the top of this file, and #convert()'s own JSDoc below).
	 *
	 * @returns {Promise<void>} resolves once the app is ready for a click —
	 *   or once the file:// guard has shown its message and returned early
	 */
	static async Init() {
		try {
			// ---- file:// guard ------------------------------------------
			if (location.protocol === "file:") {
				document.getElementById(Config.Selectors.FileGuard).hidden = false;
				document.getElementById(Config.Selectors.AppRoot).hidden = true;
				return;
			}

			// ---- load every runtime data file, compile the matcher -------
			await DataService.Init();
			this.#normaliser = new TagNormaliser(
				DataService.Data.TagLexicon,
				DataService.Data.TagExceptions,
				DataService.Data.InstructionCues,
			);

			// stamp the build version on the page so a developer can see at
			// a glance that new code is live (YYMMDD + iteration)
			const vEl = document.getElementById("app-version");
			if (vEl) vEl.textContent = `build ${Config.AppVersion}`;

			this.#wireUi();
			this.#log(Config.Strings.ReadyToConvert);
			console.log(`🟢 HTML Generator V2 ready (v${Config.AppVersion})`);
		} catch (error) {
			console.error("🔴 App initialization error:", error);
			Config.FULL_BREAK(`Startup failed: ${error.message}`);
		}
	};

	// =======================================================================
	// UI WIRING (delegated events, CSS-class state — standards §8)
	// =======================================================================

	/**
	 * Wires up every event listener the upload UI and the Convert button
	 * need. Called once from Init(), after the tag matcher is ready — never
	 * called again, so these listeners live for the whole page session.
	 *
	 * WHAT IT WIRES:
	 * - the drop zone: clicking it opens the native file picker; dragging
	 *   files over it highlights it (adds the "active" CSS class); dropping
	 *   files onto it adds them via #addFiles()
	 * - the hidden file <input>: its "change" event fires after a person
	 *   picks files through the native picker it opens
	 * - the Convert button: starts one conversion by calling #convert()
	 * - the file list: ONE delegated click listener on the whole <ul>,
	 *   rather than a listener per row (see WHY, below)
	 *
	 * WHY A DELEGATED LISTENER ON THE FILE LIST (not one "remove" listener
	 * per row): #renderFileList() throws away and rebuilds the list's whole
	 * innerHTML every time a file is added or removed, which would destroy
	 * any listener attached directly to an individual row's remove button.
	 * Listening on the parent <ul> instead means the listener survives every
	 * re-render — it inspects e.target when a click happens to work out
	 * which row was clicked, using e.target.closest("[data-remove]") to find
	 * the nearest remove button (and read its data-remove index) even if the
	 * actual click landed on a child element of that button, like an icon.
	 *
	 * @returns {void}
	 */
	static #wireUi() {
		const dropZone = document.getElementById(Config.Selectors.DropZone);
		const fileInput = document.getElementById(Config.Selectors.FileInput);

		// drop zone: click opens the picker; drag-and-drop adds files
		dropZone.addEventListener("click", () => fileInput.click());
		dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("active"); });
		dropZone.addEventListener("dragleave", () => dropZone.classList.remove("active"));
		dropZone.addEventListener("drop", (e) => {
			e.preventDefault();
			dropZone.classList.remove("active");
			this.#addFiles([...e.dataTransfer.files]);
		});
		fileInput.addEventListener("change", () => {
			this.#addFiles([...fileInput.files]);
			fileInput.value = "";   // same file can be re-picked after a fix
		});

		document.getElementById(Config.Selectors.ConvertButton)
			.addEventListener("click", () => this.#convert());

		// the "clear everything & convert another module" reset button — resets
		// the converter to its fresh state in place (see #resetPage()).
		const resetBtn = document.getElementById(Config.Selectors.ResetButton);
		if (resetBtn) resetBtn.addEventListener("click", () => this.#resetPage());

		// delegated remove buttons on the file list (rows are re-rendered)
		document.getElementById(Config.Selectors.FileList)
			.addEventListener("click", (e) => {
				const btn = e.target.closest("[data-remove]");
				if (!btn) return;
				// "acks" removes the optional _istock-acks.txt row; a number
				// removes the docx at that index (see #renderFileList)
				if (btn.dataset.remove === "acks") this.#istockAcksFile = null;
				else this.#files.splice(Number(btn.dataset.remove), 1);
				this.#renderFileList();
			});
	};

	/**
	 * Adds newly-picked or dropped files to the pending upload list (the
	 * shared #files array), validating them first. Called from both upload
	 * paths wired up in #wireUi() — the drop-zone's "drop" event and the
	 * file <input>'s "change" event — so this is the ONE place file
	 * validation happens, no matter how a person chose their files.
	 *
	 * WHAT IT VALIDATES:
	 * - extension: only files ending in ".docx" are kept. Anything else (a
	 *   stray .pdf, .doc, a screenshot, …) is rejected immediately with a
	 *   visible log message — never silently dropped without explanation.
	 * - count: this tool converts ONE module per run, which needs at most
	 *   two files — the Writers Template (WT) and its companion Media List
	 *   — or a single combined .docx that serves as both. A third file is
	 *   refused, the list is trimmed back to the first two, and a log
	 *   message explains why.
	 *
	 * WHAT IT DOES NOT DO: work out WHICH of the (up to two) accepted files
	 * is the WT and which is the Media List — that classification happens
	 * later, inside ModuleResolver.PrepareRun, once the files have actually
	 * been unzipped and their content read (see #convert() stage [3]).
	 *
	 * @param {File[]} files - newly-picked or dropped browser File objects
	 * @returns {void}
	 */
	static #addFiles(files) {
		// .docx inputs, plus the ONE optional *_istock-acks.txt (ROUND 235 —
		// the API-sourced verified iStock acknowledgements); anything else is
		// surfaced immediately
		for (const f of files) {
			if (f.name.toLowerCase().endsWith(".docx")) this.#files.push(f);
			else if (/istock-acks\.txt$/i.test(f.name)) {
				if (this.#istockAcksFile) this.#log(`⚠ "${this.#istockAcksFile.name}" replaced by "${f.name}" — one iStock acknowledgements file per run.`);
				this.#istockAcksFile = f;
				this.#log(`✓ "${f.name}" — verified iStock acknowledgements loaded; its titles will be used for iStock acks.`);
			}
			else this.#log(`⚠ "${f.name}" is not a .docx (or an _istock-acks.txt) — ignored.`);
		}
		// one module per run: a WT + its media list (or one combined file)
		if (this.#files.length > 2) {
			this.#log("⚠ More than two .docx files — Phase 1 converts ONE module per run (WT + media list, or one combined docx). Extra files removed.");
			this.#files = this.#files.slice(0, 2);
		}
		this.#renderFileList();
	};

	/**
	 * Redraws the visible list of pending uploaded files from the current
	 * #files array, and enables/disables the Convert button to match — it
	 * only becomes clickable once at least one file has been added.
	 *
	 * WHY REBUILD THE WHOLE LIST (rather than patch individual rows): the
	 * list is always short (at most two files — see #addFiles()), so simply
	 * re-rendering the whole <ul> from #files on every change keeps this
	 * file's in-memory state and the visible DOM impossible to get out of
	 * sync — #files is the one source of truth, and the DOM is always just
	 * a direct reflection of it. Each row's "remove" button carries its own
	 * array index in a data-remove="i" attribute, which the delegated click
	 * listener wired in #wireUi() reads to know which file to splice out.
	 *
	 * Called after every change to #files: when files are added, and when
	 * one is removed via its row's "remove" button.
	 *
	 * @returns {void}
	 */
	static #renderFileList() {
		const list = document.getElementById(Config.Selectors.FileList);
		const rows = this.#files.map((f, i) =>
			`<li>${Utils.EscapeHtml(f.name)} <button type="button" data-remove="${i}" title="Remove">✕</button></li>`);
		// the optional verified iStock acknowledgements file renders as its own
		// row (data-remove="acks" — see the delegated click handler in #wireUi)
		if (this.#istockAcksFile) rows.push(
			`<li>${Utils.EscapeHtml(this.#istockAcksFile.name)} <em>(verified iStock acks)</em> <button type="button" data-remove="acks" title="Remove">✕</button></li>`);
		list.innerHTML = rows.join("");
		document.getElementById(Config.Selectors.ConvertButton).disabled = this.#files.length === 0;
	};

	// =======================================================================
	// THE CONVERSION PROGRESS BAR (Convert panel)
	// =======================================================================
	// Stage-weighted determinate bar: each stage owns a fixed slice of the
	// 0–100% bar, and advances by done/total INSIDE that slice — so the bar
	// is MONOTONIC (it only ever moves forward; it never jumps backward or
	// resets mid-run) without needing to know every stage's total item count
	// up front (page counts, media counts, etc. only exist once the run is
	// actually under way). The extract and prep stages are reported directly
	// by #convert(); the pages and acks stages arrive through
	// run.onProgress — an OPTIONAL callback that ONLY this browser entry
	// point ever sets. The command-line batch-conversion tool
	// (batch_convert.cjs) never sets run.onProgress, so the engine's guarded
	// call sites that report progress are harmless no-ops when running in
	// batch — this is purely display machinery bolted onto the browser UI,
	// not a change to the shared conversion logic itself, so it can never
	// make the browser tool and the batch tool produce different output.
	// The acks slice is the widest because building the acknowledgements
	// section is the genuinely slow phase in the browser: it does a real
	// oEmbed fetch (a web standard some sites, like YouTube, support for
	// looking up a resource's title/author from its URL alone) for each
	// media item, with a throttle of at least 250ms between fetches.

	/**
	 * The stage table the progress bar is built from. Each stage owns a
	 * fixed slice of the 0–100% bar: "start" is the percentage where that
	 * slice begins, and "span" is how many percentage points wide it is.
	 * The four spans (15 + 5 + 35 + 40 = 95) deliberately leave the last 5
	 * points unused — #progressDone() jumps straight to a clean 100% rather
	 * than trying to land exactly on 95+span. "label" names the entry in
	 * Config.Strings used as that stage's visible text label.
	 */
	static #ProgressStages = {
		extract: { start: 0,  span: 15, label: "ProgressExtract" },
		prep:    { start: 15, span: 5,  label: "ProgressPrep" },
		pages:   { start: 20, span: 35, label: "ProgressPages" },
		acks:    { start: 55, span: 40, label: "ProgressAcks" },
	};

	/**
	 * Shows the progress bar at 0% and clears any leftover error styling
	 * left over from a previous failed run. Called at the very start of
	 * every #convert() click, before any real conversion work happens.
	 * @returns {void}
	 */
	static #progressStart() {
		const bar = document.getElementById(Config.Selectors.ProgressBar);
		if (!bar) return;                    // older index.html — degrade silently
		bar.classList.remove("error");
		bar.hidden = false;
		this.#progressSet("extract", 0, Math.max(this.#files.length, 1));
	};

	/**
	 * Moves the bar's fill to a position INSIDE one stage's fixed slice,
	 * based on how far through that stage the work has got (done out of
	 * total). For example, #progressSet("pages", 3, 10) with pages'
	 * {start: 20, span: 35} lands the fill at 20 + 35*(3/10) = 30.5%,
	 * rounded. Also updates the bar's visible text label and its
	 * aria-valuenow attribute (used by screen readers).
	 *
	 * @param {string} stage - one of the keys in #ProgressStages: "extract" | "prep" | "pages" | "acks"
	 * @param {number} done - units completed so far within this stage
	 * @param {number} total - the total number of units this stage will process
	 * @returns {void}
	 */
	static #progressSet(stage, done, total) {
		const bar = document.getElementById(Config.Selectors.ProgressBar);
		const s = this.#ProgressStages[stage];
		if (!bar || bar.hidden || !s) return;
		const frac = total > 0 ? Math.min(done / total, 1) : 1;
		const pct = Math.round(s.start + s.span * frac);
		document.getElementById(Config.Selectors.ProgressBarFill).style.width = `${pct}%`;
		bar.setAttribute("aria-valuenow", String(pct));
		const detail = total > 1 ? ` ${Math.min(done, total)}/${total}` : "";
		document.getElementById(Config.Selectors.ProgressBarLabel).textContent =
			`${Config.Strings[s.label] ?? stage}${detail} — ${pct}%`;
	};

	/**
	 * Fills the bar the rest of the way to a full 100% and switches its
	 * label to "Done" (the bar itself stays visible, it doesn't hide).
	 * Called once, immediately after a conversion finishes successfully.
	 * @returns {void}
	 */
	static #progressDone() {
		const bar = document.getElementById(Config.Selectors.ProgressBar);
		if (!bar || bar.hidden) return;
		document.getElementById(Config.Selectors.ProgressBarFill).style.width = "100%";
		bar.setAttribute("aria-valuenow", "100");
		document.getElementById(Config.Selectors.ProgressBarLabel).textContent =
			`${Config.Strings.ProgressDone} — 100%`;
	};

	/**
	 * Puts the bar into its error state: the fill FREEZES exactly where it
	 * was when the failure happened (it does not reset to 0% or jump to
	 * 100%) and turns red, so a person can see roughly how far the
	 * conversion got before it broke. Called from #convert()'s catch block.
	 * @returns {void}
	 */
	static #progressError() {
		const bar = document.getElementById(Config.Selectors.ProgressBar);
		if (!bar || bar.hidden) return;
		bar.classList.add("error");
		document.getElementById(Config.Selectors.ProgressBarLabel).textContent =
			Config.Strings.ProgressFailed;
	};

	/**
	 * Hides the progress bar and resets its fill back to 0%, ready for the
	 * next click. Used by #convert()'s early-return paths — an upload that
	 * gets refused before real conversion work starts (e.g. no Writers
	 * Template found among the uploads) never moved the bar to a
	 * meaningful position, so hiding it is clearer than leaving a stalled,
	 * near-empty bar on screen.
	 * @returns {void}
	 */
	static #progressHide() {
		const bar = document.getElementById(Config.Selectors.ProgressBar);
		if (!bar) return;
		bar.hidden = true;
		bar.classList.remove("error");
		document.getElementById(Config.Selectors.ProgressBarFill).style.width = "0%";
		bar.setAttribute("aria-valuenow", "0");
	};

	// =======================================================================
	// THE CONVERSION (one run per click)
	// =======================================================================

	/**
	 * Runs ONE complete conversion: everything that happens between a person
	 * clicking the Convert button and the finished HTML pages appearing in
	 * the download list. Wrapped in one big try/catch (standards §8a) so any
	 * failure — anywhere in the whole pipeline — is caught, logged to both
	 * the browser console and the on-page log, and shown as a frozen red
	 * progress bar, rather than leaving the button disabled forever or
	 * failing in a way nobody can see.
	 *
	 * THE CONVERSION SEQUENCE, STEP BY STEP:
	 *   [1] Read the upload-time option checkboxes (image mode P/D, and the
	 *       interactive hand-off mode inline/extract) and use them to
	 *       construct a fresh ConversionRun — the "run" object: one mutable
	 *       scratchpad object created for THIS conversion only, that every
	 *       later stage reads from and writes onto (the detected module
	 *       code, the resolved rules, the finished pages, warning/error
	 *       notes, the output files, …).
	 *   [2] Extract every uploaded .docx file into this engine's internal
	 *       block representation (see ZipReader + DocxExtractor.Extract).
	 *       Neither uploaded file is known yet to be the Writers Template or
	 *       the Media List at this point — see stage [3] for that.
	 *   [3] Run the ONE shared prep sequence, ModuleResolver.PrepareRun:
	 *       classify the extracted files, detect the module code, resolve
	 *       its structural rules, parse the Media List, and trim the WT's
	 *       front-matter. This is the SAME sequence the separate
	 *       command-line batch tool calls (see the note near the top of
	 *       this file) — see stage [3]'s own comment, below, for why that
	 *       matters. PrepareRun can signal that conversion cannot continue
	 *       (prep.ok === false): either no Writers Template was found among
	 *       the uploads at all (prep.reason === "no-wt"), or the module uses
	 *       a pathway this converter doesn't support yet (prep.reason ===
	 *       "unsupported", e.g. certain bilingual templates) — either way,
	 *       #convert() logs why, re-enables the Convert button, and returns
	 *       early without attempting to build any pages.
	 *   [4] Wire up run.onProgress (see THE CONVERSION PROGRESS BAR, above)
	 *       so the engine can report page-by-page and acknowledgement-by-
	 *       acknowledgement progress back to this browser UI as it works.
	 *   [5]–[8] Hand the fully-prepared run to PageAssembler.AssembleModule,
	 *       which runs the rest of the pipeline (page splitting, interactive
	 *       widget scanning + content conversion, acknowledgements, and
	 *       final HTML assembly) and fills in run.pages / run.interactives /
	 *       run.outputs. See stage [5]–[8]'s own comment, below.
	 *   Finally: render the finished output files into the download list
	 *       (#renderOutputs) and the run summary panel (SummaryReporter),
	 *       mark the progress bar 100% Done, and log a one-line result.
	 *
	 * @returns {Promise<void>} resolves once conversion has finished (or
	 *   failed, or been refused) and the button has been re-enabled
	 */
	static async #convert() {
		const button = document.getElementById(Config.Selectors.ConvertButton);
		button.disabled = true;
		this.#clearOutputs();
		this.#progressStart();
		this.#log(Config.Strings.Converting);

		try {
			// ---- [1] upload-time choices ------------------------------------
			// imageMode ("P" or "D"): which of two placeholder-image rendering
			// styles to use for an image the converter can't fetch a real
			// asset for yet. Purely a user choice, carried on the run object.
			const imageMode = document.getElementById(Config.Selectors.ModeP).checked ? "P" : "D";
			// ROUND 235 (Chris) — the interactive HAND-OFF is now the DEFAULT and
			// its UI switch is gone: interactiveMode is resolved by the run itself
			// (ConversionRun.DefaultInteractiveMode — the same shared, data-driven
			// decision the batch harness uses, so the two entries cannot drift).
			// Every un-built interactive renders as its reference-code box with
			// the raw captured content collapsed inside it, and the same codes
			// head the {CODE}_interactives.txt blocks.
			const run = new ConversionRun({ imageMode });

			// ---- [2] extract every uploaded docx into blocks ----------------
			// A .docx file IS a zip archive internally (that's Word's own
			// format), so ZipReader opens it as one, and
			// DocxExtractor.Extract(zip) reads the zip's XML parts and turns
			// them into this engine's internal representation: an ordered
			// list of paragraph/table "blocks" that the rest of the pipeline
			// works with (see DocxExtractor.js for the full block shape).
			// This runs for EVERY uploaded file (there are at most two — see
			// #addFiles()) — at this point neither file is known yet to be
			// the Writers Template or the Media List; that classification
			// happens next, in stage [3].
			//
			// `docs` ends up shaped like:
			//   [
			//     { name: "OSAH401 Writers Template.docx", doc: { blocks, rels, mtkFlag, hasContentStart, metadata } },
			//     { name: "OSAH401 Media List.docx",        doc: { blocks, rels, mtkFlag, hasContentStart, metadata } },
			//   ]
			const docs = [];
			for (const file of this.#files) {
				const zip = new ZipReader(await file.arrayBuffer());
				const doc = await DocxExtractor.Extract(zip);
				docs.push({ name: file.name, doc });
				this.#log(`Extracted ${file.name}: ${doc.blocks.length} blocks, ${doc.rels.size} links.`);
				this.#progressSet("extract", docs.length, this.#files.length);
			}

			// ---- [3] THE SHARED PREP ----------------------------------------
			// Classification (working out which uploaded file is the WT and
			// which is the Media List), module-code detection, structural
			// rule resolution, setting run.mtkFlag, the unsupported-pathway
			// refusal check, media-item parsing, and trimming the WT's
			// front-matter ALL live in ONE method: ModuleResolver.PrepareRun.
			// This browser app and batch_convert.cjs (the separate,
			// command-line entry point used for bulk/automated conversion —
			// see the note near the top of this file) BOTH call this exact
			// same method for their setup, so they can never silently drift
			// apart again. They used to each run their own separate copy of
			// this logic, and those two copies quietly grew out of sync over
			// time — this app, for instance, used to forget to set
			// run.mtkFlag and ran an older, since-relaxed refusal rule — so
			// the SAME module could produce DIFFERENT HTML depending on
			// which tool converted it (a real example this was fixed for:
			// the module HPFUN903 converted differently through the browser
			// than through the batch tool). The automated test
			// `_verify_entry_parity.cjs` exists specifically to keep proving
			// the two entry points stay calling this one shared sequence.
			// ROUND 235 (Chris) — the optional verified iStock acknowledgements
			// file rides into the ONE shared prep sequence as plain text; parsing
			// lives inside PrepareRun/AcksBuilder (never here — entry parity).
			const istockAcksText = this.#istockAcksFile ? await this.#istockAcksFile.text() : null;
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: this.#normaliser, istockAcksText });
			if (!prep.ok && prep.reason === "no-wt") {
				this.#log("🔴 No Writers Template found among the uploads (no [TITLE BAR]/[Fundamental content] opener). Nothing converted.");
				this.#progressHide();
				button.disabled = false;
				return;
			}
			if (!prep.ok && prep.reason === "unsupported") {
				run.AddNote("error", "App", `${prep.unsupported.label}: ${prep.unsupported.action}`);
				SummaryReporter.Render(run);
				this.#progressHide();
				button.disabled = false;
				return;
			}
			if (prep.mediaSource) this.#log(`Media list: ${run.mediaItems.length} items.`);
			this.#progressSet("prep", 1, 1);

			// The browser-only progress hook: pages + acks progress reports flow
			// from the engine's guarded call sites inside the pipeline below.
			// batch_convert.cjs never sets run.onProgress, so those same call
			// sites are harmless no-ops when running in batch — see THE
			// CONVERSION PROGRESS BAR section, above, for the full explanation.
			run.onProgress = (stage, done, total) => this.#progressSet(stage, done, total);

			// ---- [5]-[8]: the page-building pipeline ------------------------
			// App.js's own stage numbering picks back up here at [5]. Stages
			// [5] through [8] all happen INSIDE this one call, entirely inside
			// PageAssembler.AssembleModule: split the prepared module into
			// pages, scan each page for interactive widgets and convert its
			// content to HTML, build the acknowledgements section, and wrap
			// every finished page in its page skeleton plus write the
			// interactives hand-off manifest. This file deliberately doesn't
			// need those details to stay correct — see PageAssembler.js if you
			// need to trace further in.
			await PageAssembler.AssembleModule(run, this.#normaliser);

			// ---- outputs + summary ------------------------------------------
			// Conversion succeeded: hand the finished files to the download
			// list (#renderOutputs) and the human-readable run summary
			// (SummaryReporter.Render), then mark the progress bar 100% Done.
			this.#renderOutputs(run);
			SummaryReporter.Render(run);
			this.#progressDone();
			this.#log(`${Config.Strings.Done} ${run.outputs.length} files for ${run.moduleCode ?? "module"}.`);

			// ---- post-success UI (ROUND 205) -------------------------------
			// The module is converted, so:
			//  (R3) HIDE the Convert button — the current module is done; a
			//       fresh conversion goes through the reset button below. We
			//       hide (not destroy) the node so the reset can restore it.
			//  (R5) SHOW the "clear everything & convert another module" reset
			//       button, which is meaningless before a conversion exists.
			//  (R2) SCROLL to the VERY BOTTOM so the "Download all as .zip"
			//       button is guaranteed visible — when a module produces many
			//       HTML files their filenames can push that button off-screen,
			//       so landing on it (block:"end") is what Chris wants, not the
			//       top of the Output files section. We scroll the button itself
			//       into view (robust inside the embedded iframe); a full-height
			//       window.scrollTo is the equivalent when the button is absent.
			//       All three fire ONLY on success — never on refusal/error.
			button.hidden = true;
			const resetPanel = document.getElementById(Config.Selectors.ResetPanel);
			if (resetPanel) resetPanel.hidden = false;
			const downloadAll = document.getElementById(Config.Selectors.DownloadAll);
			if (downloadAll && !downloadAll.hidden) {
				downloadAll.scrollIntoView({ behavior: "smooth", block: "end" });
			} else {
				window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
			}
		} catch (error) {
			console.error("🔴 Conversion error:", error);
			this.#progressError();
			this.#log(`🔴 Conversion failed: ${error.message} (see the browser console for the stack).`);
		}
		button.disabled = false;
	};

	// =======================================================================
	// OUTPUT PRESENTATION
	// =======================================================================

	/**
	 * Renders the results of a successful conversion into the Outputs
	 * panel: a "module details" summary card, one downloadable link per
	 * output file, and a "download all as zip" button. Called once, right
	 * after PageAssembler.AssembleModule finishes inside #convert().
	 *
	 * WHAT IT BUILDS:
	 * - the module-details card: the captured front-matter fields (module
	 *   code, subject, course, English/Te Reo titles, key contact, date
	 *   submitted) plus the two upload-time choices (image mode,
	 *   interactive hand-off mode), read from run.Summary().metadata and
	 *   the run object itself. Blank fields are filtered out rather than
	 *   shown empty.
	 * - one <li> per file in run.outputs: each finished HTML page, plus the
	 *   interactives hand-off manifest file when one was produced (see the
	 *   "extract" interactive mode). Each becomes a real downloadable link
	 *   by wrapping its text content in a Blob and pointing an <a> at an
	 *   object URL for that blob — the whole file lives in memory, there is
	 *   no server to fetch it from.
	 * - the "download all" button, wired to zip every output together
	 *   (ZipWriter.Build) on click, built lazily rather than up front since
	 *   most conversions are only ever inspected file-by-file.
	 *
	 * @param {ConversionRun} run - the completed run (run.outputs, run.Summary(), etc.)
	 * @returns {void}
	 */
	static #renderOutputs(run) {
		const list = document.getElementById(Config.Selectors.OutputList);
		list.innerHTML = "";

		// module-identity card beside the downloads — the captured
		// front-matter fields + resolved titles, kept for future use
		const md = run.Summary().metadata;
		const metaEl = document.getElementById("output-metadata");
		if (metaEl) {
			const rows = [
				["Module code", run.moduleCode],
				["Subject", md.subject],
				["Course", md.course],
				["English title", md.englishTitle],
				["Te Reo title", md.teReoTitle],
				["Key contact", md.keyContact],
				["Date submitted", md.dateSubmitted],
				["Image mode", run.imageMode],
				["Interactive mode", run.interactiveMode === "extract" ? "hand-off (raw content collapsed in-page, expandable)" : "inline (legacy)"],
				["iStock acks file", run.istockAcks ? `${run.istockAcks.size} verified titles` : null],
			].filter(([, v]) => v);
			metaEl.innerHTML = `<h3>Module details</h3><dl class="meta-list">${
				rows.map(([k, v]) => `<dt>${Utils.EscapeHtml(k)}</dt><dd>${Utils.EscapeHtml(String(v))}</dd>`).join("")
			}</dl>`;
			metaEl.hidden = false;
		}

		for (const out of run.outputs) {
			const blob = new Blob([out.content],
				{ type: out.kind === "manifest" ? "text/plain" : "text/html" });
			const a = document.createElement("a");
			a.href = URL.createObjectURL(blob);
			a.download = out.filename;
			a.textContent = out.filename;
			const li = document.createElement("li");
			li.appendChild(a);
			li.insertAdjacentHTML("beforeend",
				` <span class="output-kind">${out.kind === "manifest" ? "interactives manifest" : "page"}</span>`);
			list.appendChild(li);
		}

		// download-all zip
		const all = document.getElementById(Config.Selectors.DownloadAll);
		all.hidden = run.outputs.length === 0;
		all.onclick = () => {
			const blob = ZipWriter.Build(run.outputs);
			const a = document.createElement("a");
			a.href = URL.createObjectURL(blob);
			a.download = `${run.moduleCode ?? "module"}_converted.zip`;
			a.click();
			URL.revokeObjectURL(a.href);
		};
	};

	/**
	 * Wipes every leftover output from a previous conversion — the file
	 * download list, the module-details card, the "download all" button,
	 * and the run-summary panel — back to their empty/hidden starting
	 * state. Called at the very start of every #convert() click, before any
	 * new conversion work begins, so a failed or refused conversion can
	 * never leave a STALE previous run's outputs visible alongside (or
	 * instead of) whatever the new click actually produced.
	 *
	 * @returns {void}
	 */
	static #clearOutputs() {
		document.getElementById(Config.Selectors.OutputList).innerHTML = "";
		document.getElementById(Config.Selectors.DownloadAll).hidden = true;
		const meta = document.getElementById("output-metadata");
		if (meta) { meta.hidden = true; meta.innerHTML = ""; }
		const panel = document.getElementById(Config.Selectors.SummaryPanel);
		panel.hidden = true;
		panel.innerHTML = "";
	};

	/**
	 * Resets the whole converter back to its fresh, first-load state IN PLACE
	 * — WITHOUT reloading the page. Wired to the "clear everything & convert
	 * another module" reset button (shown only after a conversion completes).
	 *
	 * WHY NOT location.reload(): the converter runs inside an <iframe> in the
	 * PageForge site shell (under "HTML Generator" mode). A full reload would
	 * navigate the iframe back to the site's default "Module Development"
	 * landing page, dropping the user out of the converter entirely. So the
	 * reset rebuilds the fresh state by hand instead: it returns the SAME view
	 * to "new-page state without navigating away".
	 *
	 * WHAT IT CLEARS/RESTORES:
	 *  - the pending uploads (#files) + the (now empty) file list
	 *  - all outputs: the download list, module-details card, download-all
	 *    button, and the summary panel (via #clearOutputs)
	 *  - the progress bar (hidden, back to 0%) + the progress log
	 *  - the Convert button: shown again + disabled-until-a-file-is-added
	 *  - the image-mode radios back to Mode P (default)
	 *  - hides this reset button again (meaningless with no conversion)
	 *  - scrolls back to the top (section 1 · Upload)
	 *
	 * @returns {void}
	 */
	static #resetPage() {
		// pending uploads + file list (incl. the optional _istock-acks.txt)
		this.#files = [];
		this.#istockAcksFile = null;
		this.#renderFileList();          // also disables the Convert button (0 files)

		// outputs, module-details card, download-all, summary panel
		this.#clearOutputs();

		// progress bar + log
		this.#progressHide();
		const log = document.getElementById(Config.Selectors.ProgressLog);
		if (log) log.innerHTML = "";

		// Convert button: bring it back (R3 hid it on success) — #renderFileList
		// has already set its disabled state to match the now-empty file list.
		const button = document.getElementById(Config.Selectors.ConvertButton);
		if (button) button.hidden = false;

		// upload-time choices back to their defaults (the extract checkbox is
		// GONE since round 235 — the hand-off is the default, nothing to reset)
		const modeP = document.getElementById(Config.Selectors.ModeP);
		if (modeP) modeP.checked = true;
		const modeD = document.getElementById(Config.Selectors.ModeD);
		if (modeD) modeD.checked = false;

		// hide the reset button again + scroll to the top (section 1 · Upload)
		const resetPanel = document.getElementById(Config.Selectors.ResetPanel);
		if (resetPanel) resetPanel.hidden = true;
		window.scrollTo({ top: 0, behavior: "smooth" });
	};

	/**
	 * Appends one line of plain text to the visible, scrolling progress log
	 * panel (newest line last, at the bottom). Used throughout Init() and
	 * #convert() to narrate what's happening — file validation warnings,
	 * per-file extraction results, refusal reasons, the final result line,
	 * and so on — so a person watching the page can follow along without
	 * opening the browser's developer console.
	 *
	 * WHY textContent (not innerHTML): the text passed in can include a
	 * writer's own filename or error message, which must never be
	 * interpreted as HTML markup — textContent always renders it as
	 * literal text, so there's no need to separately escape it here.
	 *
	 * @param {string} text - the line to append (plain text, not HTML)
	 * @returns {void}
	 */
	static #log(text) {
		const log = document.getElementById(Config.Selectors.ProgressLog);
		const line = document.createElement("p");
		line.textContent = text;
		log.appendChild(line);
		log.scrollTop = log.scrollHeight;
	};
}

// the single bootstrap (standards §8a)
document.addEventListener("DOMContentLoaded", () => {
	App.Init();
});
