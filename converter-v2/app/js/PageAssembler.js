/**
 * PageAssembler.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * This is pipeline stage [8], the LAST stage of converting a single module —
 * the orchestrator that calls every earlier pipeline stage in the right order
 * and glues their results together into the finished output files. One
 * module (the lesson sequence built from one Writers Template .docx — the
 * source document where writers wrap content in [bracketed tags] like [H2] or
 * [Activity] — plus its companion Media List .docx) becomes one or more HTML
 * "pages" (a page is one HTML output file, either a single lesson or the
 * module overview, named {CODE}-00.html, {CODE}-01.html, … in document
 * order) plus one interactives hand-off text file. The pipeline this file
 * drives:
 *   item stream → pages → interactive bundles → converted content
 *   → acknowledgements → skeleton-wrapped HTML pages → manifest.
 * See AssembleModule's own doc comment below for the numbered, stage-by-stage
 * breakdown.
 *
 * THE KEY IDEA:
 * Everything in this file reads from, and writes onto, ONE shared object: the
 * ConversionRun (parameter name `run` throughout the codebase) — a single
 * mutable scratchpad object created fresh for each conversion job that data
 * accumulates onto as the pipeline runs (the module code, the extracted
 * pages, interactive widgets, output files, and human-readable diagnostic
 * notes added via run.AddNote so nothing is silently guessed or dropped). By
 * the time AssembleModule returns, run.pages, run.interactives, and
 * run.outputs together hold the complete result of converting this module.
 *
 * OUTPUT NAMING (locked decision, 12/06/26):
 * {CODE}-00.html, -01.html, … in document order (the brief's contract
 * form; data: Emit_Templates.output_naming). The interactives manifest is
 * {CODE}_interactives.txt.
 *
 * ACKS PLACEMENT (policy, locked):
 * The acknowledgements block goes on the FIRST page only, after #footer.
 * ===========================================================================
 */

class PageAssembler {

	/**
	 * ROUND 243 (Dev-Feedback R6 — Chris, 2026-07-31): THE ONE SOURCE OF TRUTH
	 * for page output filenames, shared by the emit loop below AND the r226
	 * choice-page tile hrefs (ContentConverter.#choicePageTiles). The library
	 * convention the developer imports against is `{code}_{lesson}_{part}.html`
	 * (SCCH302_0_0.html); every page already carries exactly that number as its
	 * lessonLabel ("0.0" overview, "N.0" lesson, "N.M" sub-page, dotted writer
	 * lessons verbatim), so the filename is the label with "." → "_". The 12/06/26
	 * dash form `{code}-{NN}.html` is kept as legacy_page_file; env PAGENAME_OFF
	 * (or a page_file template without {page}) reverts byte-for-byte. A label
	 * collision (two pages resolving the same name — measured ~nonexistent; the
	 * splitter derives distinct labels) is disambiguated deterministically with
	 * a trailing _2/_3 … and reported as a run note, so two pages can NEVER
	 * silently overwrite each other.
	 * Data: Emit_Templates.output_naming (page_file/{page} + legacy_page_file).
	 */
	static PageFileNames(run) {
		if (run._pageFileNames) return run._pageFileNames;
		const naming = DataService.Data.EmitTemplates.output_naming;
		const code = run.moduleCode ?? "MODULE";
		const legacy = (typeof process !== "undefined" && process.env && process.env.PAGENAME_OFF)
			|| !String(naming.page_file ?? "").includes("{page}");
		const used = new Set();
		run._pageFileNames = (run.pages ?? []).map((p, i) => {
			if (legacy) {
				return Utils.FillTemplate(naming.legacy_page_file ?? naming.page_file,
					{ code, NN: Utils.Pad2(i) });
			}
			const label = String(p.lessonLabel ?? (p.isOverview ? "0.0" : `${i}.0`))
				.replace(/[^\d.]/g, "") || String(i);
			let page = label.replace(/\./g, "_");
			if (used.has(page)) {
				let n = 2;
				while (used.has(`${page}_${n}`)) n++;
				page = `${page}_${n}`;
				run.AddNote("warn", "PageAssembler",
					`Two pages resolved the same lesson label "${label}" — the later file is disambiguated as _${n}; check the writer's lesson numbering.`);
			}
			used.add(page);
			return Utils.FillTemplate(naming.page_file, { code, page });
		});
		return run._pageFileNames;
	};

	/**
	 * ROUND 522 (the autonomous loop's session 51 Round 2) — THE WRITER'S RED-BRACKET JOURNAL SENTENCE IS
	 * LEARNER TEXT, NOT AN [Activity] OPENER. `[Go to your learning journal and complete activity 2B]` (the AGH
	 * family, 36 spans / 6 modules) parses with the activity tag and its id, so the converter opened a box
	 * numbered 2B, stripped the ids into a garbled Writers Note ("…complete and" — a KB constraint-1 breach) and
	 * left the box EMPTY or let it swallow the next section (AGH1002 2.0 'Soil Structure'). The gold renders the
	 * sentence as the learner's instruction inside its own activity box (61 / 61 in AGH). Here — once, before the
	 * split, the scanner and the converter read the stream — a tag item whose ONLY tag is the activity tag and whose
	 * bracket is a journal SENTENCE (the data patterns, min_words..max_words) becomes a native black item holding
	 * the writer's words, brackets stripped (a trailing '}' typo too); ContentConverter's #journalInstructionBox
	 * then gives it its box. Data activity_wrapper.journal_instruction_box.bracket_sentence; env JOURNALINSTR_OFF.
	 */
	static #journalBracketSentence(items, run) {
		const cfg = DataService.Data.EmitTemplates?.activity_wrapper?.journal_instruction_box;
		if (!cfg || cfg.enabled === false || cfg.bracket_sentence === false) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "JOURNALINSTR_OFF"]) return;
		const jRe = new RegExp(cfg.journal_pattern, "i"), vRe = new RegExp(cfg.verb_pattern, "i"), idRe = new RegExp(cfg.id_pattern, "i");
		let n = 0;
		for (const it of items) {
			if (!it || it.type !== "tag" || it.parse?.primary?.tag !== "activity" || (it.parse.tags ?? []).length !== 1) continue;
			const inner = String(it.text ?? "").replace(/^\s*\[/, "").replace(/[\]}]\s*$/, "").trim();
			if (/[[\]{}]/.test(inner)) continue;   // a second bracket inside: not one sentence
			const words = inner.split(/\s+/).filter(Boolean).length;
			if (words < (cfg.min_words ?? 5) || words > (cfg.max_words ?? 40)) continue;
			if (!jRe.test(inner) || !vRe.test(inner) || !idRe.test(inner)) continue;
			const tail = String(it.blackAfter ?? "");
			it.type = "black";
			it.text = inner + (tail.trim() ? (/^\s*[.,;:!?]/.test(tail) ? tail.trim() : " " + tail.trim()) : "");
			delete it.parse; delete it.blackAfter;
			it._r522Journal = true;
			// the post-pass moves ONLY these sentences out of a box numbered with another id (a writer's black journal line
			// inside her own activity box stays there — the HES form, already the gold's)
			(run._r522JournalTexts ??= new Set()).add(it.text.replace(/[*_]/g, "").replace(/\s+/g, " ").trim().toLowerCase());
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler",
			`${n} red-bracket journal instruction${n > 1 ? "s" : ""} read as the learner's sentence, not an [Activity] opener (journal_instruction_box.bracket_sentence).`);
	}

	/**
	 * ROUND 525 — THE BOLD ACTIVITY ID AFTER A WIDGET TAG (the FRNO family's form, 50 spans): `[Reorder autocheck]]
	 * **2C****Put the conversation together**` — the id and title typed in bold black after the widget tag, so no box opened and
	 * both shipped inside the hand-off box; the gold boxes each as div.activity[number=2C] titled by the bold words. The widget tag
	 * is re-parsed with an `[Activity 2C]` co-tag (the round-92 activity + widget span, which opens the numbered box) and the bold id
	 * leaves the tail. A stray bracket span between them (`[Wordfind autocheck] ] **1E**…`, a noise item) hands the tail's id to the
	 * widget tag just before it on the same paragraph. Data Tag_Lexicon _meta.bold_id_widget_activity; env BOLDIDACT_OFF.
	 */
	static #boldIdWidgetActivity(items, run, normaliser) {
		const cfg = DataService.Data.TagLexicon?._meta?.bold_id_widget_activity;
		if (!cfg || cfg.enabled === false || !normaliser) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "BOLDIDACT_OFF"]) return;
		const re = new RegExp(cfg.id_pattern);
		let n = 0;
		for (let i = 0; i < items.length; i++) {
			const it = items[i];
			if (it?.type !== "tag") continue;
			const m = re.exec(String(it.blackAfter ?? ""));
			if (!m) continue;
			let w = it;
			if (!it.parse?.primary && i > 0 && items[i - 1]?.type === "tag" && items[i - 1].block === it.block) w = items[i - 1];
			const p = w.parse?.primary;
			if (!p || p.directive !== "INTERACTIVE" || (w.parse.tags ?? []).some((t) => t.tag === "activity")) continue;
			// the round-365 form `[Activity 2C – <widget words>]`, so the bold title after the id becomes the box's <h3>
			// (activity_wrapper.embedded_interactive_activity.typed_tag_title); the widget words keep resolving the widget
			const inner = String(w.text ?? "").replace(/[[\]]/g, " ").replace(/\s+/g, " ").trim();
			const text = `[Activity ${m[1]} – ${inner}]`;
			const np = normaliser.Parse(text);
			if (!np?.primary || np.primary.directive !== "INTERACTIVE" || !(np.tags ?? []).some((t) => t.tag === "activity")) continue;
			w.parse = np; w.text = text;
			const tail = String(it.blackAfter).slice(m[0].length);
			if (w !== it) { w.blackAfter = String(w.blackAfter ?? "") + tail; it.blackAfter = ""; }   // the stray bracket's tail moves to its widget
			else it.blackAfter = tail;
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} widget tag${n > 1 ? "s" : ""} followed by a bold activity id read as the activity + widget span (bold_id_widget_activity).`);
	}

	/**
	 * ROUND 523 — THE CO-TAG'S DUPLICATE-ID GUARD. TagNormaliser gives an `[Activity 2] [H3] Title` span the activity's
	 * primary slot (Tag_Lexicon _meta.activity_heading_cotag); but when the SAME id opens another activity later on the same
	 * page, the writer put the id on a section heading AND on the real activity (MXEX202 lesson 2: `[Activity 2] [H3] Double
	 * or Half` … `[Activity 2] [H3] Fun Water Challenge`; HES1002 2.0) — the gold boxes only the later one and keeps the
	 * first a free heading, while a box on the first shifts every later id by the r369 de-dupe. Such a span hands the primary
	 * slot back to its heading (the pre-523 parse). Data activity_heading_cotag.duplicate_id_guard; env ACTHDCOTAG_OFF.
	 */
	static #cotagDuplicateId(items, run) {
		const cfg = DataService.Data.TagLexicon?._meta?.activity_heading_cotag;
		if (!cfg || cfg.enabled === false || cfg.duplicate_id_guard === false) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "ACTHDCOTAG_OFF"]) return;
		const idOf = (x) => String(x?.parse?.numbers?.[0] ?? "").toUpperCase();
		let n = 0;
		for (let i = 0; i < items.length; i++) {
			const it = items[i];
			if (it?.type !== "tag" || !it.parse?.cotagHeading || it.parse.primary?.tag !== "activity" || !idOf(it)) continue;
			for (let j = i + 1; j < items.length; j++) {
				const x = items[j];
				if (x?.type !== "tag" || !x.parse?.primary) continue;
				if (x.parse.primary.directive === "PAGE_BOUNDARY") break;
				if (x.parse.primary.tag === "activity" && idOf(x) === idOf(it)) {
					it.parse.primary = it.parse.cotagHeading; n++;
					break;
				}
			}
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} [Activity] + heading co-tag${n > 1 ? "s" : ""} kept as a heading: the same id opens a later activity (activity_heading_cotag.duplicate_id_guard).`);
	}

	/**
	 * ROUND 522 part 2 — THE WRITER'S BARE [Summary] IS AN ALERT BOX TITLED 'Summary' (the AGH family's own tag: 31 spans,
	 * every one AGH; the gold boxes the whole run as `div.alert` headed `<h4>Summary</h4>`, 83 / 83 blocks). The span resolves
	 * to no tag, so it shipped as a Writers Note with the bullets free. Here it is re-parsed as the data's retag_as (the
	 * plain alert callout) with the tag word as its first content line: the ordinary strict alert path gathers the run and
	 * #alertTitleHeading lifts that short first line to the h4. Data callouts.bare_summary_alert; env SUMMARYALERT_OFF.
	 */
	static #bareSummaryAlert(items, run, normaliser) {
		const cfg = DataService.Data.EmitTemplates?.callouts?.bare_summary_alert;
		if (!cfg || cfg.enabled === false || !normaliser) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "SUMMARYALERT_OFF"]) return;
		const re = new RegExp(cfg.pattern, "i");
		let n = 0;
		for (const it of items) {
			if (!it || it.type !== "tag" || it.parse?.primary || !re.test(String(it.text ?? ""))) continue;
			const parse = normaliser.Parse(cfg.retag_as);
			if (!parse?.primary) continue;
			it.parse = parse; it.text = cfg.retag_as;
			it.blackAfter = cfg.title + (String(it.blackAfter ?? "").trim() ? " " + String(it.blackAfter).trim() : "");
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} bare [Summary] tag${n > 1 ? "s" : ""} read as an alert titled '${cfg.title}' (callouts.bare_summary_alert).`);
	}

	/**
	 * Converts ONE module end-to-end: the single entry point that turns an
	 * already-extracted Writers Template (run.wtBlocks, parsed by an earlier
	 * pipeline stage) into finished, ready-to-save HTML pages plus the
	 * interactives hand-off manifest. Fills in run.pages, run.interactives, and
	 * run.outputs on the ConversionRun object passed in.
	 *
	 * THE STAGES, IN ORDER:
	 *   1. Resolve this module's HTML rendering conventions (ConventionResolver)
	 *      — must run after ModuleResolver has already set run.groupKey.
	 *   2. Split the Writers Template's content into an ordered "item stream",
	 *      then split that into pages — one entry in run.pages per lesson or
	 *      overview (PageSplitter).
	 *   3. For each page: scan it for "interactive bundles" (clusters of writer
	 *      content that should become one interactive widget, e.g. a flip-card
	 *      set) BEFORE converting the page's content, so the converter knows
	 *      where to place each widget's placeholder or built-out HTML
	 *      (InteractiveScanner) — then convert the page's content to HTML
	 *      (ContentConverter).
	 *   4. Work out the module's English / Te Reo Māori title, including the
	 *      fallback rules for when the Writers Template's own [TITLE BAR] tag
	 *      was incomplete, ambiguous, or left as unfilled placeholder text.
	 *   5. Build the acknowledgements section (AcksBuilder) — generated for
	 *      every module, whether or not any media actually needs crediting.
	 *   6. Wrap each page's converted content in the shared page chrome
	 *      ("skeleton" HTML — the header/menu/footer common to every page;
	 *      SkeletonBuilder), chaining each page's prev/next footer links to its
	 *      sibling output files, and push the finished HTML onto run.outputs.
	 *   7. Build the {CODE}_interactives.txt hand-off manifest — a plain-text
	 *      worklist of every interactive widget the converter could not fully
	 *      build automatically (ManifestBuilder) — and push it onto
	 *      run.outputs too.
	 *
	 * DATA SHAPES:
	 * A `pageProducts` entry (built internally below, one per page) looks like:
	 *   { page: <the PageSplitter page object>,
	 *     content: <ContentConverter's { html, titleBar, … } result for that page> }
	 * A `run.outputs` entry (this method's final result) looks like:
	 *   { filename: "CODE-00.html", content: "<...finished HTML string...>", kind: "page" }
	 *   { filename: "CODE_interactives.txt", content: "<...manifest text...>", kind: "manifest" }
	 *
	 * @param {ConversionRun} run - the shared scratchpad object for this
	 *   conversion job; must already be prepared with run.wtBlocks (the
	 *   extracted Writers Template content) and run.mediaItems (the parsed
	 *   Media List) before this is called
	 * @param {TagNormaliser} normaliser - the compiled [bracketed tag] matcher
	 *   used throughout the pipeline to recognise and classify writer tags
	 * @returns {Promise<void>} nothing is returned directly — every result is
	 *   written onto the `run` object's pages / interactives / outputs arrays
	 */
	static async AssembleModule(run, normaliser) {
		const naming = DataService.Data.EmitTemplates.output_naming;

		// HTML conventions via the group cascade (series → subject×phase →
		// global) — must run after ModuleResolver set run.groupKey
		ConventionResolver.Resolve(run);

		// ---- [5] split into pages -----------------------------------------
		const items = PageSplitter.BuildItemStream(run.wtBlocks, normaliser);
		PageAssembler.#journalBracketSentence(items, run);   // ROUND 522 — before the split, the scanner and the converter all read the item
		PageAssembler.#bareSummaryAlert(items, run, normaliser);   // ROUND 522 part 2 (SUMMARYALERT_OFF)
		PageAssembler.#cotagDuplicateId(items, run);   // ROUND 523 (ACTHDCOTAG_OFF — the co-tag rule's own guard)
		PageAssembler.#boldIdWidgetActivity(items, run, normaliser);   // ROUND 525 (BOLDIDACT_OFF)
		run.pages = PageSplitter.Split(items, run, normaliser);
		if (!run.pages.length) {
			run.AddNote("error", "PageAssembler",
				"No pages could be assembled from this document — nothing to output.");
			return;
		}

		// ---- [6] scan interactives + convert content ------------------------
		// (scan first so converted pages can place the placeholders; bundle
		// indexes are run-wide and 1-based so the manifest reads naturally)
		const pageProducts = [];
		for (const page of run.pages) {
			const bundles = InteractiveScanner.ScanPage(page, normaliser, run);
			for (const b of bundles) {
				b.index = run.interactives.length + 1;
				b.page = page;
				run.interactives.push(b);
				// A NESTED sub-bundle absorbed into a host widget (e.g. an accordion
				// panel that swallows a shapeHover widget inside it) is registered right
				// after its host so it gets its own run-wide cv2-index + manifest entry,
				// and so the host's builder can render its honest placeholder by index.
				// The host has already consumed the nested items' range while scanning,
				// so they must never be independently re-scanned as their own bundle.
				for (const nb of (b.nestedBundles ?? [])) {
					nb.index = run.interactives.length + 1;
					nb.page = page;
					run.interactives.push(nb);
				}
			}
			const content = ContentConverter.ConvertPage(page, bundles, run, normaliser);
			pageProducts.push({ page, content });
			// Browser-only progress reporting + a repaint yield. This whole per-page
			// loop runs SYNCHRONOUSLY, so without help the browser's Convert-panel
			// progress bar would never get a chance to redraw until the entire module
			// had finished converting. When (and only when) the browser entry point set
			// run.onProgress, report the page that just finished, then yield one
			// "macrotask" — `await new Promise((resolve) => setTimeout(resolve, 0))`
			// hands control back to the browser's event loop for a single tick so it
			// can repaint the bar — before continuing to the next page. The node
			// command-line harness never sets run.onProgress, so this whole block is a
			// no-op there: no report, no yield, no change to the batch conversion path
			// (this is display machinery only, not conversion prep).
			if (run.onProgress) {
				run.onProgress("pages", pageProducts.length, run.pages.length);
				await new Promise((resolve) => setTimeout(resolve, 0));
			}
		}

		// The overview page's title bar (its [TITLE BAR]-tagged content in the Writers
		// Template, holding the English title and, for bilingual modules, the Te Reo
		// Māori title) feeds every lesson page's fallback title.
		const overviewProduct = pageProducts.find((p) => p.page.isOverview) ?? pageProducts[0];
		run.englishTitle = overviewProduct?.content.titleBar.english ?? "";
		run.teReoTitle = overviewProduct?.content.titleBar.teReo ?? "";
		// The overview page is where the BLL "Module N -" title-prefix family gets
		// decided (see the title-bar handling further down this file). Remember that
		// decision on the run itself so every OTHER page in this module — not just
		// the overview — also renders its own title h1 with the same lowercase span.
		run.modulePrefix = overviewProduct?.content.titleBar.modulePrefix === true;

		// "MODULE NAME" METADATA TITLE (ROUND 212 — the PNR101/102/104 MTK
		// "Te Aka Taumatua" bilingual family). This template has NO [TITLE BAR]
		// payload anywhere (the drop-down-menu table's [TITLE BAR] row is left
		// empty); the module's bilingual title lives in the front-matter metadata
		// table's "Module Name" row instead ("Ngā tau: 1 | Numbers: 1"). When no
		// title was derived at all, pipe-split that value and ship its halves in
		// PAYLOAD ORDER (Te Reo first on all three golds — the same positional
		// slot convention the ordinary title splits use; see the CEDW501 note in
		// ContentConverter). This runs BEFORE the Course backup below so a course
		// CODE ("PNR9000") can never become the title.
		// Data: elements.dual_language.dropdown_menu.title_from_module_name +
		// front_matter_metadata.table_row_fields. Env toggle: REODROPMENU_OFF
		// (the metadata capture is also disabled by it, so this never fires).
		{
			const ddCfg = DataService.Data.EmitTemplates.elements?.dual_language?.dropdown_menu;
			const ddOn = ddCfg && ddCfg.enabled !== false && ddCfg.title_from_module_name !== false
				&& !(typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF);
			const modName = run.metadata?.moduleName;
			if (ddOn && modName && !run.englishTitle && !run.teReoTitle) {
				const parts = String(modName).split(/\s*\|\s*/).map((s) => s.trim()).filter(Boolean);
				if (parts.length) {
					run.englishTitle = parts[0];
					run.teReoTitle = parts.slice(1).join(" | ");
					run.AddNote("info", "PageAssembler",
						`No [TITLE BAR] title — using the front-matter "Module Name" metadata "${modName}" as the module title (MTK drop-down-menu template).`);
				}
			}
		}

		// English-title BACKUP: the module must never ship with a Te-Reo-only
		// title. When the [TITLE BAR] gave a SINGLE title that does NOT match
		// the front-matter Course (i.e. it's the Te Reo name), promote that
		// lone title to the Te Reo slot and use Course as the English title
		// (front_matter_metadata.course_is_english_title_backup; verified
		// need on OSAI301: payload was only "Kirirarautanga Matihiko AI").
		// ROUND 321 (loop Round 8 — the MTK / Te Reo Rangatira title source, Chris's
		// decision 2). The TRR1xx docx leaves its [TITLE BAR] rows empty and has no Module
		// Name row, so both run titles are still empty here. Sources, in order: the first
		// [H1] / [Title Bar] item anywhere whose text carries a pipe (the per-page
		// "TRR102 The vowels: Aa | Ngā Oropuare: Aa" repetition, code stripped, halves in
		// payload order), else the Module Code cell's remainder (metadata.moduleCodeTitle:
		// a pipe, or one spaced dash with a macron on exactly one side, splits it). The
		// skeleton orders the pair Māori-first for these modules (header.mtk_titles).
		{
			const mtk = DataService.Data.EmitTemplates.header?.mtk_titles;
			const mtkOn = mtk && mtk.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[mtk.env ?? "MTKTITLES_OFF"])
				&& new RegExp(mtk.body_class ?? "reoTranslate", "i").test(String(run.resolvedRules?.body_class || ""));
			if (mtkOn && !run.englishTitle && !run.teReoTitle) {
				const code = String(run.moduleCode || "");
				const esc = code.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
				const stripCode = (s) => code ? String(s).replace(new RegExp("^\\s*" + esc + "\\s*[:\\-\u2013\u2014]?\\s*", "i"), "") : String(s);
				const tidy = (s) => String(s ?? "").replace(/\*+/g, "").replace(/^[\s:\-\u2013\u2014|]+|[\s:\-\u2013\u2014|]+$/g, "").replace(/\s+/g, " ").trim();
				let parts = null, src = "";
				const tags = new Set(mtk.repetition_tags ?? ["h1", "title bar"]);
				outer: for (const p of run.pages) {
					for (const it of (p.items ?? [])) {
						if (it.type !== "tag" || !tags.has(it.parse?.primary?.tag)) continue;
						const txt = tidy(stripCode(tidy(it.blackAfter || "")));
						if (!txt.includes("|")) continue;
						const h = txt.split("|").map(tidy).filter(Boolean);
						if (h.length >= 2) { parts = h.slice(0, 2); src = `[${it.parse.primary.tag}] repetition on page ${p.lessonLabel}`; break outer; }
					}
				}
				const cell = tidy(run.metadata?.moduleCodeTitle);
				if (!parts && cell) {
					const M = /[\u0101\u0113\u012b\u014d\u016b\u0100\u0112\u012a\u014c\u016a]/;
					if (cell.includes("|")) parts = cell.split("|").map(tidy).filter(Boolean).slice(0, 2);
					else {
						const d = cell.split(/\s+[\u2013\u2014\-]\s+/);
						parts = (d.length === 2 && (M.test(d[0]) !== M.test(d[1])) && d.every((h) => tidy(h).replace(/[^A-Za-zÀ-ſ]/g, "").length >= 3)) ? d.map(tidy) : [cell];
					}
					src = "the Module Code cell";
				}
				if (parts && parts.length) {
					run.englishTitle = parts[0];
					run.teReoTitle = parts[1] ?? "";
					run.AddNote("info", "PageAssembler",
						`No [TITLE BAR] / Module Name title — MTK module title taken from ${src}: "${parts.join(" | ")}" (round 321).`);
				}
			}
		}
		const tb = overviewProduct?.content.titleBar;
		const course = run.metadata?.course;
		const titlePhOn = (DataService.Data.EmitTemplates.header.title_split.placeholder_title_rule?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.TITLEPH_OFF);
		if (titlePhOn && course && !run.englishTitle) {
			// Sometimes EVERY half of the [TITLE BAR] tag was left as unreplaced
			// template placeholder text (e.g. the writer never filled in 'MODULE TITLE
			// TE REO') — meaning there is NO real title anywhere in the Writers
			// Template. In that case, fall back to the front-matter Course field as the
			// SINGLE English title and ship NO Te Reo title at all (we only ever show
			// both languages when both are genuinely present in the source document;
			// we never invent the missing one). Env toggle TITLEPH_OFF reverts this
			// whole rule, falling back instead to an older, narrower check for what
			// counts as "placeholder text".
			run.englishTitle = course;
			run.teReoTitle = "";
			run.AddNote("info", "PageAssembler",
				`[TITLE BAR] held only placeholder text — using the front-matter Course "${course}" as the English title; no Te Reo title (the real one is not in the WT).`);
		} else if (tb?.single && course
			// a REAL title left after dropping a placeholder half (mixed bar) is the
			// English title — NOT Te Reo — so don't run the lone-title promotion on it
			&& !(titlePhOn && tb?.droppedPlaceholder)
			// The lone-title → Te Reo promotion below assumes that when the Writers
			// Template's [TITLE BAR] gives just ONE title, and that title differs from
			// the front-matter Course field, the lone title must be the Te Reo name
			// (this rule exists to handle a module like OSAI301, whose only title text
			// was "Kirirarautanga matihiko AI"). That assumption MISFIRES when the lone
			// title is actually the ENGLISH module title and the Course field just
			// happens to hold a broader subject name instead: one module (ENGC102) had
			// WT title "*KEEPING IT REAL*" and Course "Communication", and without this
			// guard the converter shipped <h1>Communication</h1> as the English title
			// (wrong — that's just the subject name) with "Keeping it real" wrongly
			// shoved into the Te Reo slot; another module (ENGS302) went even further
			// and put its Māori Course name "Te Ara Hou" into the ENGLISH slot. GUARD:
			// only promote the lone title to the Te Reo slot when it is ACTUALLY
			// written in Te Reo Māori (the Māori alphabet never uses the letters
			// b c d f j l q s v x y z; it only uses g/h/k/m/n/p/r/t/w plus vowels +
			// macrons, including the ng/wh digraphs). An English lone title is left as
			// the English title, with no Te Reo title invented out of nothing (the
			// real Te Reo title, if this module has one, simply isn't present anywhere
			// in this WT, so we don't guess at it). This has been checked against the
			// existing library of already-built modules with no regressions (see
			// outputs/_probe_lonetitle.cjs), and OSAI301 still gets promoted correctly.
			// Data flag: header.title_split.lone_title_maori_guard; env: LONETITLE_OFF.
			&& this.#loneTitleIsTeReo(run.englishTitle)
			&& Utils.Fold(run.englishTitle).replace(/\s+/g, "")
				!== Utils.Fold(course).replace(/\s+/g, "")) {
			run.teReoTitle = run.englishTitle;   // the lone WT title was Te Reo
			run.englishTitle = course;
			run.AddNote("info", "PageAssembler",
				`[TITLE BAR] held only "${run.teReoTitle}" (no English) — using the front-matter Course "${course}" as the English title; Te Reo kept as the second title.`);
		}
		// the skeleton reads the run-level titles; refresh the overview
		// product's titleBar so the header h1s reflect the backup
		if (overviewProduct) {
			overviewProduct.content.titleBar.english = run.englishTitle;
			overviewProduct.content.titleBar.teReo = run.teReoTitle;
		}

		// ---- [6b] acknowledgements — ALWAYS generated (policy) --------------
		const acksHtml = await AcksBuilder.Build(run);

		// ---- [7]+[8] skeleton wrap + emit -----------------------------------
		const code = run.moduleCode ?? "MODULE";
		// page filenames are deterministic — compute them all first so each
		// page's footer can link to its prev/next siblings (page chaining).
		// ROUND 243: through the shared PageFileNames helper (the library
		// {code}_{lesson}_{part}.html form; env PAGENAME_OFF = the dash legacy).
		const filenames = PageAssembler.PageFileNames(run);
		// ROUND 228 (Chris — Change Ledger CL-0044, constraint 71): footer nav
		// hrefs ship EMPTY — prev/next/home alike; D2L wires the real links at
		// publish time. Measured: the gold library is 97% empty (the populated
		// remainder is the publish-time D2L quickLink wiring itself), so this
		// matches both the design-team directive AND the gold. The per-position
		// <li> composition (value_map) is unchanged — only the href fill.
		// Data footer.nav_links_empty.enabled; env FOOTEREMPTY_OFF reverts to
		// the round-8 sibling chaining.
		const footerEmpty = (DataService.Data.EmitTemplates.footer?.nav_links_empty?.enabled === true)
			&& !(typeof process !== "undefined" && process.env && process.env.FOOTEREMPTY_OFF);
		pageProducts.forEach(({ page, content }, i) => {
			const html = SkeletonBuilder.BuildPage({
				page, content, run,
				// first page carries the acks block (after #footer);
				// historical last-page placement is superseded — never copy it
				acksHtml: i === 0 ? acksHtml : "",
				isFinal: i === pageProducts.length - 1 && pageProducts.length > 1,
				// CL-0044: hrefs empty by default; FOOTEREMPTY_OFF restores chaining
				prevHref: footerEmpty ? "" : (i > 0 ? filenames[i - 1] : ""),
				nextHref: footerEmpty ? "" : (i < pageProducts.length - 1 ? filenames[i + 1] : ""),
			});
			run.outputs.push({
				filename: filenames[i],
				// tab-indented for hand-editing/debugging, matching the human-developed
				// modules' formatting. Before formatting, two clean-up passes run over
				// the finished page HTML, in this order: OmitPlaceholderResidue strips
				// the left-over debris of an omitted, unfilled template prompt (an empty
				// bullet point plus its internal cv2-omit marker) from anywhere on the
				// page — the menu and the acknowledgements section included, not just
				// the main body. TidyDeveloperNotes then cleans up developer-facing
				// comment notes: it relocates any comment note that ended up inside the
				// module menu out into the body instead, merges ("coalesces") runs of
				// consecutive same-prefix notes into one, and drops bare addressee cues
				// that carry no actual content. TidyDeveloperNotes is "gate-neutral" —
				// this clean-up cannot affect the automated regression comparisons used
				// to check the converter's output against known-good modules, because
				// developer-comment markup is excluded from those comparisons anyway.
				// THE ORDER MATTERS: OmitPlaceholderResidue must run BEFORE
				// TidyDeveloperNotes, so an already-omitted placeholder prompt can never
				// be accidentally relocated or merged back in by the tidy-up pass.
				// DOMAIN LINK-TEXT DISPLAY (ROUND 213 — Chris, the BLL241 supervisor-
				// note screenshot): a link on a configured domain whose visible text
				// is itself a URL shows the domain's canonical display form
				// ("https://speldsa.org.au") while the href keeps the full deep URL.
				// Applied to the page BEFORE the acknowledgements block only — the
				// human developers keep the FULL URL text in their acknowledgements
				// (measured), and canonicalise it in the body (67/68 sites).
				// Data: Emit_Templates elements.link_text_display; env LINKTEXT_OFF.
				// NO-EMOJI RULE (ROUND 234 — Change Ledger CL-0051): after the note
				// tidy and BEFORE the link-text pass, EmojiStrip removes emoji from
				// the rendered writer content (Extended_Pictographic clusters minus
				// the ledger's exempt ticks & crosses; arrows become plain arrows;
				// 2+ consecutive emoji-prefixed lines become a <ul>; ONE red
				// disclosure note per affected page, built through the standard
				// NotesAndComments.redFlag machinery so the r219 note scheme and
				// NOTESCHEME_OFF apply to it like any other note). Applied to the
				// page BEFORE the acknowledgements block only — the acks keep
				// their verbatim oEmbed titles and the converter's own ❗ ack-todo
				// markers. Verbatim zones (cv2-interactive hand-off boxes,
				// cv2-note / cv2-comment quotes) are skipped inside the pass.
				// Data: Input_Doc_Rules.emoji_strip; env EMOJISTRIP_OFF.
				// TYPED-NUMBER RUNS → <ol> (ROUND 337 — KB constraint 42): after the
				// emoji pass and BEFORE the link-text pass, TypedNumberList turns a
				// run of consecutive plain <p>s whose text opens with sequential typed
				// numbers ("1. …", "2. …") into one semantic <ol> (start="N" when the
				// run does not begin at 1), the typed number stripped. Body only; the
				// same verbatim zones as EmojiStrip plus the built widgets that own
				// their inner shape (flipCard / dragAndDrop / carousel / …).
				// Data: Emit_Templates body_region.typed_number_list; env TYPEDOL_OFF.
				content: HtmlFormatter.Indent(
					(() => {
						const tidied = NotesAndComments.TidyDeveloperNotes(
							NotesAndComments.OmitPlaceholderResidue(html));
						// ROUND 392: adjacent sibling lists join into one (body_region.merge_adjacent_lists; env ULMERGE_OFF) — after TypedNumberList, before the link-text pass.
						const deEmoji = (seg) => ListsAndRuns.MergeAdjacentLists(ListsAndRuns.TypedNumberList(ListsAndRuns.EmojiStrip(seg, () =>
							NotesAndComments.redFlag(
								DataService.Data.InputDocRules?.emoji_strip?.disclosure ?? "",
								run, "diagnostic"))));
						const ai = tidied.indexOf("<div class=\"acks");
						// ROUND 419 (KB constraint 92 / CL-0093): every CJK run takes its language-font class
						// (ListsAndRuns.LanguageFontWrap; data body_region.language_fonts; env LANGFONT_OFF) —
						// after the link-text pass, the pre-acks slice only (the gold's acks credits stay bare).
						const langWrap = (seg) => ListsAndRuns.LanguageFontWrap(ListsAndRuns.LinkTextDisplay(seg), run);
						const passed = ai < 0
							? langWrap(deEmoji(tidied))
							: langWrap(deEmoji(tidied.slice(0, ai))) + tidied.slice(ai);
						// ROUND 346 (Chris's D10-7): the equation sentinels become their MathML LAST, after every
						// text pass (none of them may touch the markup), and a page that now carries a <math>
						// gains the mathJax body class (the gold's per-page form). Data Input_Doc_Rules.math.
						const _mathCfg = DataService.Data.InputDocRules?.math;
						let withMath = DocxExtractor.MathReplace(passed);
						if (_mathCfg && _mathCfg.enabled !== false && withMath !== passed && /<math\b/.test(withMath)) {
							const tok = _mathCfg.body_class_token || "mathJax";
							withMath = withMath.replace(/<body class="([^"]*)"/, (m, cls) =>
								new RegExp("(^|\\s)" + tok + "(\\s|$)").test(cls) ? m : "<body class=\"" + cls + " " + tok + "\"");
						}
						// ROUND 474 (KB c52): every derivable iStock image alt, LAST (MediaBuilder.FillWidgetAlts;
						// data elements.image_attrs.widget_alt_postpass; env WIDGETALT_OFF).
						return MediaBuilder.FillWidgetAlts(withMath, run);
					})()),
				kind: "page",
			});
		});

		// ---- [8] the interactives manifest -----------------------------------
		// filenames are known now, so manifest entries can point at them
		run.interactives.forEach((b) => {
			const pageIndex = run.pages.indexOf(b.page);
			b.targetFile = run.outputs[pageIndex]?.filename ?? run.outputs[0]?.filename;
		});
		run.outputs.push({
			filename: Utils.FillTemplate(naming.manifest_file, { code }),
			content: DocxExtractor.MathReplace(ManifestBuilder.Build(run)),   // ROUND 346: equation sentinels → MathML in the hand-off too
			kind: "manifest",
		});

		// ---- the distilled reference template (ROUND 249) --------------------
		// When the person uploaded reference HTML pages at conversion time (see
		// ModuleResolver.PrepareRun's reference-module block), the mined
		// structural profile ships as its own JSON output — the file Chris
		// needs to add that reference module to PageForge's templated modules.
		// Named after the REFERENCE module's code (that's what the file
		// describes), falling back to this module's code when the uploaded
		// pages carried no recognisable code in their filenames.
		if (run.referenceDistilled?.file) {
			const refName = run.referenceDistilled.referenceCode ?? code;
			run.outputs.push({
				filename: `${refName}_reference-template.json`,
				content: JSON.stringify(run.referenceDistilled.file, null, "\t") + "\n",
				kind: "reference-template",
			});
		}
	};

	/**
	 * Decides whether a LONE [TITLE BAR] title — the Writers Template gave only one
	 * title, with no separate Te Reo half — is written in Te Reo Māori (in which case
	 * the Course-backup logic above should promote it into the Te Reo title slot), or
	 * whether it is actually English (in which case it IS the English title and
	 * should ship alone, with no Te Reo title invented).
	 *
	 * HOW: Te Reo Māori uses only the letters a e h i k m n o p r t u w (plus the
	 * macrons ā ē ī ō ū) and the ng/wh digraphs — it NEVER uses b c d f j l q s v x y
	 * z. So a title containing any of those non-Māori letters must be English.
	 *
	 * WHY THIS GUARD EXISTS: see the caller's comment above for two real modules
	 * (ENGC102, ENGS302) whose English titles were once wrongly promoted into the Te
	 * Reo slot before this check was added.
	 *
	 * @param {string} title - the lone WT title text to classify
	 * @returns {boolean} true when the title should be treated as Te Reo Māori; also
	 *   true when the guard itself is switched off (via the data flag or env
	 *   LONETITLE_OFF), which preserves the original always-promote behavior from
	 *   before this guard existed
	 */
	static #loneTitleIsTeReo(title) {
		const cfg = DataService.Data.EmitTemplates.header?.title_split?.lone_title_maori_guard;
		const on = (cfg?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.LONETITLE_OFF);
		if (!on) return true;                          // guard off → original (always promote)
		const nonMaori = new RegExp(cfg?.non_maori_letters ?? "[bcdfjlqsvxyz]", "i");
		return !nonMaori.test(String(title ?? ""));    // no non-Māori letter → Te Reo
	}
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { PageAssembler };
