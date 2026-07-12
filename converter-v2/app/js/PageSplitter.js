/**
 * PageSplitter.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Two steps that turn extracted blocks into output-page units:
 *  1. BuildItemStream() — splits every paragraph block into an ordered
 *     stream of ITEMS: red tag spans (parsed by the TagNormaliser), black
 *     content runs, and tables. This is the stream every later stage walks.
 *  2. Split() — applies the page-boundary directives + the six validated
 *     assembly rules (Tag_Normalisation_Spec.md §Page-boundary) to group
 *     items into pages: one page per output HTML file.
 *
 * THE SIX ASSEMBLY RULES (each marked AR-n where implemented):
 *  AR-1 [MODULE INTRODUCTION] continues page -00 — never splits, even when
 *       the writer placed an [end page] before it.
 *  AR-2 Adjacent boundary tags produce ONE break — never empty pages.
 *  AR-3 No [LESSON n]/[PAGE] anywhere → single-document module: [end page]
 *       is not a file break (also forced by registry page_model).
 *  AR-4 A second literal [TITLE BAR] starts a new sub-document; the loose
 *       aliases (title/overview/introduction) mid-document are headings,
 *       never breaks (the lexicon maps those through SECTION/ELEMENT, and
 *       only the literal fragment check here opens a document).
 *  AR-5 Content after the final [end page] with no headings/interactives is
 *       writer-form boilerplate — dropped with a summary note.
 *  AR-6 A bracketless red span is never a tag (TagNormaliser classifies it
 *       content/instruction — nothing for the splitter to do, noted for
 *       completeness).
 * Plus the repair rules from Tag_Interpretation_Rules.md §5.4: implicit
 * boundary before [LESSON n] (RR-2), ignore an [end page] that would close
 * an empty segment (RR-3), and merge an orphaned headings-only opening
 * segment forward (RR-4).
 *
 * ITEM SHAPES (the stream contract):
 *  { type:"tag",   parse, text, blackAfter, block }  ← one red span + the
 *                    black text that follows it inside the same paragraph
 *  { type:"black", text, block }                     ← paragraph content
 *  { type:"table", block }                           ← a docx table
 *
 * PAGE SHAPE (the splitter's product):
 *  { items:[], isOverview, lessonNumber, lessonLabel, pageTitle,
 *    subDocument, wtPageStart }
 * ===========================================================================
 */

class PageSplitter {

	/**
	 * Splits blocks into the item stream (red spans parsed, black kept).
	 *
	 * HOW PARAGRAPHS SPLIT:
	 * "🔴[RED TEXT] [H2] [/RED TEXT]🔴**Learning Intentions**" becomes one
	 * tag item whose blackAfter = "**Learning Intentions**". A paragraph
	 * with no red span becomes one black item. Adjacent red spans with
	 * nothing between them were already merged by the extractor.
	 *
	 * @param {Object[]} blocks - trimmed content blocks (DocxExtractor)
	 * @param {TagNormaliser} normaliser - the compiled matcher
	 * @returns {Object[]} item stream
	 */
	static BuildItemStream(blocks, normaliser) {
		const items = [];
		// the corpus marker form: 🔴[RED TEXT] … [/RED TEXT]🔴
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;

		for (const block of blocks) {
			if (block.kind === "table") {
				items.push({ type: "table", block });
				continue;
			}

			const text = block.text;
			let pos = 0;
			let pendingTag = null;   // last tag item awaiting its blackAfter

			for (const m of text.matchAll(RED)) {
				// black text BEFORE this red span: belongs to the previous
				// tag in this paragraph (its content), else a standalone black
				const before = text.slice(pos, m.index);
				if (before.trim()) {
					if (pendingTag) pendingTag.blackAfter += before;
					else items.push({ type: "black", text: before, block });
				}
				// the red span itself → parse once, carry the result
				const parse = normaliser.Parse(m[1]);
				pendingTag = { type: "tag", parse, text: m[1], blackAfter: "", block };
				items.push(pendingTag);
				pos = m.index + m[0].length;
			}

			const tail = text.slice(pos);
			if (tail.trim()) {
				if (pendingTag) pendingTag.blackAfter += tail;
				else items.push({ type: "black", text: tail, block });
			}
		}
		return items;
	};

	/**
	 * Groups the item stream into pages.
	 *
	 * @param {Object[]} items - BuildItemStream() output
	 * @param {ConversionRun} run - rules + note surface
	 * @param {TagNormaliser|null} normaliser - for original-case embedded
	 *                  lesson titles ("[LESSON 2] Cook's First Voyage")
	 * @returns {Object[]} pages
	 */
	static Split(items, run, normaliser = null) {
		// AR-3: single-document modules never split. THE REGISTRY DECIDES
		// (its page_model is validated per level): 'single-file' = one file
		// regardless of page tags; 'multi-file' = [LESSON]/[PAGE]/[end page]
		// boundaries each produce a file — INCLUDING [end page] alone
		// (verified on XGF9001: no [LESSON] tags at all, 15 real files split
		// purely by [End page]). The no-LESSON/PAGE-tags heuristic is only
		// the fallback for a silent registry.
		const hasLessonOrPage = items.some((it) => it.type === "tag"
			&& it.parse.primary?.directive === "PAGE_BOUNDARY"
			&& ["lesson", "page"].includes(it.parse.primary.tag));
		const pageModel = run.resolvedRules?.page_model;
		const singleFile = pageModel === "single-file"
			|| (pageModel === undefined && !hasLessonOrPage);
		if (pageModel === "single-file" && hasLessonOrPage) {
			run.AddNote("info", "PageSplitter",
				"Registry says single-file but lesson/page tags exist — keeping ONE file; the tags become in-page breaks (registry rule).");
		}

		// BILINGUAL (reoMode) PAGE-SPLIT SUPPORT.
		//
		// A bilingual "reoTranslate" module's Writers Template marks the start
		// of each lesson with a `[LESSON N CONTENT]` tag. That tag classifies
		// as a SECTION_MARKER, not a PAGE_BOUNDARY, so the ordinary
		// page-splitting logic further down never treated it as a place to
		// start a new page — lesson 1's content fell onto the overview page
		// instead of getting its own page, and every lesson after it ended up
		// numbered one lower than it should be (the item stream here starts
		// right at lesson 1, because the overview's own body text was already
		// trimmed off earlier in the pipeline).
		// This mirrors the SAME "is this a bilingual module?" test that
		// ContentConverter uses elsewhere: the body carries the reoTranslate
		// CSS class, OR the Writers Template carried the bilingual house-style
		// signature (mtkFlag), OR the module code starts with "TRR" or "PNR".
		// Data flag: Emit_Templates.json elements.dual_language.page_split
		// Env toggle: REOPAGE_OFF
		const _dlCfg = (typeof DataService !== "undefined")
			&& DataService.Data?.EmitTemplates?.elements?.dual_language;
		// THE "mtkFlag" IS NOT A RELIABLE BILINGUAL SIGNAL.
		//
		// Every Writers Template built from the standard house template
		// carries a "MTK WRITERS TEMPLATE" heading in its front matter — that
		// is just the NAME of the template file, not a sign that the module
		// is bilingual. The vast majority of Writers Templates (measured: 374
		// out of 390) carry this heading, yet only a small number of modules
		// are genuinely bilingual. So mtkFlag being true is treated as WEAK
		// evidence, and is only trusted when explicitly turned on via a data
		// flag or the MTKREO_OFF env var. Genuine bilingual detection comes
		// from the OTHER two signals below and is unaffected: the module's
		// body carries the reoTranslate CSS class, or its module code starts
		// with "TRR" or "PNR".
		// Data flag: Emit_Templates.json elements.dual_language.use_mtk_flag
		// Env toggle: MTKREO_OFF (set to re-enable mtkFlag as a bilingual
		// signal, restoring the older, more permissive behaviour)
		const _mtkArm = (!!_dlCfg && _dlCfg.use_mtk_flag === true)
			|| !!(typeof process !== "undefined" && process.env && process.env.MTKREO_OFF);
		const _reoMode = !!_dlCfg && _dlCfg.enabled !== false
			&& (/reoTranslate/i.test(run.resolvedRules?.body_class || "") || (_mtkArm && !!run.mtkFlag)
				|| (_dlCfg.code_prefixes || []).some((p) => String(run.moduleCode || "").toUpperCase().startsWith(String(p).toUpperCase())));
		const reoPage = _reoMode && (_dlCfg.page_split?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.REOPAGE_OFF);
		// A SECOND bilingual page-split convention: a `[H2] Lesson N` (or the
		// te reo equivalent, `[H2] Ngohe N`) heading that sits at the top of a
		// TABLE ROW starts a new lesson page — but only when its number is
		// HIGHER than the lesson we're already on. Writers repeat the exact
		// same `[H2] Lesson N` heading at the top of every sub-activity table
		// within that lesson, so if we opened a new page every time we saw
		// the heading at all, we'd get a separate page per activity instead
		// of per lesson. Watching for the number to actually INCREMENT is
		// what tells us "this is a genuinely new lesson" rather than "this is
		// the same lesson's next table".
		// Data flag: page_split.lesson_table_boundary
		// Env toggle: REOPAGE2_OFF (independent of REOPAGE_OFF above)
		const reoPage2 = reoPage && (_dlCfg.page_split?.lesson_table_boundary?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.REOPAGE2_OFF);

		// TWO GENERAL RULES FOR "AR-4" (see the file header banner above —
		// AR-4 is the rule that a second literal [TITLE BAR] starts a
		// brand-new sub-document). These matter for modules that are NOT
		// bilingual: once mtkFlag stopped being trusted as a bilingual signal
		// on its own (see above), some non-bilingual modules that used to be
		// routed through the more forgiving bilingual page-split path started
		// hitting AR-4's "new sub-document" behaviour on a mid-document title
		// bar that was never meant to start a new document. These two rules
		// cover that situation generally, for any module.
		// Data flag: Emit_Templates.json page_split_rules
		// Env toggle: MTKPAGE_OFF disables both rules below (MTKREO_OFF also
		// disables them, as a side effect of turning mtkFlag back into a
		// trusted bilingual signal — with it on, reoPage handles mid-doc
		// title bars itself and this branch is never reached)
		const _psRules = ((typeof DataService !== "undefined")
			&& DataService.Data?.EmitTemplates?.page_split_rules) || null;
		const _psRulesOff = (typeof process !== "undefined" && process.env
			&& (process.env.MTKPAGE_OFF || process.env.MTKREO_OFF));
		// Rule 1 — a module whose registry page_model says "single-file"
		// (i.e. it should always produce exactly one output file, no matter
		// what page tags appear in the source) should NEVER be split into a
		// sub-document by AR-4 either. A second [TITLE BAR] in a single-file
		// module just becomes an in-page heading, the same way [LESSON] and
		// [PAGE] tags already do for single-file modules elsewhere in this
		// function.
		const _sfSuppress = !!_psRules && _psRules.single_file_subdocument_suppress !== false
			&& !_psRulesOff && run.resolvedRules?.page_model === "single-file";
		// Rule 2 — if a SECOND [TITLE BAR] has EXACTLY the same text as the
		// one before it (once both are case/whitespace-folded), it is almost
		// always a writer's copy-paste duplicate rather than a genuinely new
		// document, so it's treated as an in-page duplicate instead of
		// opening a new sub-document. (Some modules DO legitimately have two
		// different [TITLE BAR]s with different text — e.g. an
		// English-language document paired with its Te Reo twin — and those
		// are untouched by this rule because their text differs.)
		const _dupInpage = !!_psRules && _psRules.duplicate_titlebar_inpage !== false && !_psRulesOff;
		let _lastTitleBarFold = null;

		const pages = [];
		let current = null;
		let lessonOrdinal = 0;      // bare [LESSON] tags number themselves 1,2,3…
		let pageWithinLesson = 0;   // [PAGE] sub-numbering → labels 3.0, 3.1, …
		let seenIntro = false;      // AR-1 latch
		let subDocument = 0;        // AR-4 counter

		/** Opens a new page and makes it current. */
		const open = (props) => {
			current = {
				items: [], isOverview: false, lessonNumber: null,
				lessonLabel: null, pageTitle: "", subDocument, ...props,
			};
			pages.push(current);
		};

		/**
		 * RR-3/AR-2: a page is "empty" when it has no black content, no
		 * table, and no rendering tag — closing it would emit a blank file.
		 */
		const currentIsEmpty = () => current && !current.items.some((it) =>
			it.type === "table"
			|| (it.type === "black" && it.text.trim())
			|| (it.type === "tag" && (it.blackAfter.trim()
				|| ["ELEMENT", "INTERACTIVE", "CONTAINER_OPEN", "INLINE"].includes(it.parse.primary?.directive))));

		let closed = false;   // true between an [end page] and the next opener

		// Tracks whether this document's stream carried the STANDALONE
		// "[Content for DROP DOWN MENU]" opener (ROUND 212 — the MTK bilingual
		// template's PNR shape). Only such a document treats a later "[MODULE
		// CONTENT: PAGE n]" marker as overview content rather than a page break.
		let _ddSeenOpener = false;
		const _ddOpenerRe = (_dlCfg?.dropdown_menu && _dlCfg.dropdown_menu.enabled !== false)
			? new RegExp(_dlCfg.dropdown_menu.opener_pattern ?? "^\\[content for drop[ -]?down menu\\]$", "i")
			: null;

		for (let i = 0; i < items.length; i++) {
			const it = items[i];
			const primary = it.type === "tag" ? it.parse.primary : null;
			if (_ddOpenerRe && !_ddSeenOpener && it.type === "tag"
				&& _ddOpenerRe.test((it.parse?.folded ?? "").trim())) _ddSeenOpener = true;

			// ---- document opener: the literal [TITLE BAR] ----------------
			// (AR-4: only the literal fragment opens a (sub)document)
			const isTitleBar = it.type === "tag"
				&& it.parse.tags.some((t) => t.tag === "title bar" && t.fragment.trim() === "title bar");
			if (isTitleBar) {
				const _tbFold = Utils.Fold(String(it.block?.text || ""));
				const _tbIsDup = _lastTitleBarFold !== null && _tbFold === _lastTitleBarFold;
				_lastTitleBarFold = _tbFold;
				if (!current) {
					open({ isOverview: true, lessonLabel: "0.0", wtPageStart: it.block.wtPage });
				} else if (reoPage) {
					// In a bilingual (reoMode) module, a [Title Bar] tag
					// appearing partway through the document is a LESSON
					// TITLE, not the start of a new sub-document — some
					// writers use [Title Bar] instead of [H1] for an
					// individual lesson's heading. Keep it on the CURRENT
					// lesson page instead of treating it as AR-4's "second
					// title bar means a new document" signal, so we don't
					// relabel pages unnecessarily.
					current.items.push(it);
					closed = false;
					continue;
				} else if (_sfSuppress || (_dupInpage && _tbIsDup)) {
					// Rule 1 (single-file modules): a mid-document [TITLE BAR]
					// stays in-page, because AR-4 now respects the registry's
					// page_model the same way it already respects
					// [LESSON]/[PAGE] tags for single-file modules elsewhere
					// in this function.
					// Rule 2 (duplicate title bars): a second [TITLE BAR] with
					// exactly the same text as the one before it is a
					// writer's copy-paste duplicate, kept in-page rather than
					// treated as a new document.
					// Both cases use the SAME "keep it on the current page"
					// handling as the reoMode branch just above.
					run.AddNote("info", "PageSplitter",
						_sfSuppress
							? "Second [TITLE BAR] kept in-page — registry page_model is single-file."
							: "Second [TITLE BAR] is a same-text duplicate of the previous one — kept in-page, not a sub-document.");
					current.items.push(it);
					closed = false;
					continue;
				} else {
					// AR-4: a SECOND literal [TITLE BAR] → new sub-document
					subDocument++;
					run.AddNote("warn", "PageSplitter",
						`Second [TITLE BAR] found — starting sub-document ${subDocument} (e.g. a reading-record twin set). Files continue the same numbering; review the split.`);
					open({ isOverview: true, lessonLabel: "0.0", subDocument, wtPageStart: it.block.wtPage });
				}
				closed = false;
				seenIntro = false;
				current.items.push(it);   // title bar carries the page titles
				continue;
			}

			// no page open yet and this isn't a literal [TITLE BAR]:
			// Fundamentals-style templates open with [Fundamental content] /
			// [Title] instead — the front-matter trim already anchored us at
			// the right block, so open the overview here implicitly
			if (!current) {
				open({ isOverview: true, lessonLabel: "0.0", wtPageStart: it.block?.wtPage });
				run.AddNote("info", "PageSplitter",
					"Document opens without a literal [TITLE BAR] — overview page opened at the first content tag (Fundamentals-style template).");
			}

			// ---- AR-1: [MODULE INTRODUCTION] continues -00 ----------------
			if (primary?.tag === "module introduction") {
				seenIntro = true;
				if (closed) {
					// the writer put [end page] before the intro — disregard
					// that break (repair rule 1): same overview page continues
					closed = false;
					run.AddNote("info", "PageSplitter",
						"[end page] before [MODULE INTRODUCTION] disregarded — the introduction stays on the overview page (AR-1).");
				}
				current.items.push(it);
				continue;
			}

			// ---- reoMode: [LESSON N CONTENT] section-marker → lesson page -----
			// In a bilingual module a numbered `[LESSON N CONTENT]` marker opens lesson
			// page N.0 (it parses as a SECTION_MARKER, so the PAGE_BOUNDARY block below
			// never sees it). The overview (0.0) is whatever precedes the FIRST one — for
			// most TRR the stream starts at lesson 1, so the just-opened implicit overview
			// stays EMPTY and becomes the menu page (RR-4 is guarded below to keep it).
			if (reoPage && primary?.tag === "lesson content" && it.parse.numbers.length) {
				const num = it.parse.numbers[0];
				// AR-2: a stray empty page before this boundary is reused, not duplicated
				if (current && currentIsEmpty() && !current.isOverview) {
					pages.pop();
					current = pages[pages.length - 1] ?? null;
				}
				lessonOrdinal = parseInt(num, 10) || (lessonOrdinal + 1);
				pageWithinLesson = 0;
				open({
					lessonNumber: num,
					lessonLabel: `${num}.0`,
					pageTitle: it.blackAfter.trim() || (normaliser ? normaliser.RenderText(it.text) : ""),
					wtPageStart: it.block?.wtPage,
				});
				closed = false;
				continue;   // the marker itself is not body content
			}

			// ---- reoMode CONVENTION 2: a [H2] Lesson N / Ngohe N TABLE-ROW heading -----
			// opens a lesson page when the lesson NUMBER increments. The writer repeats the
			// same `[H2] Lesson N` at the top of each sub-activity table (TRR114: Lesson 1 ×3,
			// 2 ×3, 3 ×3 → human pages 1.0/2.0/3.0); split ONLY on a NEW (higher) number so the
			// repeats stay in-page. The `[H2] Lesson N` form is self-discriminating (the overview
			// headings are "Overview"/"Key Objectives"/… never "Lesson N"). reoMode-gated → standard
			// untouched. The dipthong-tail lessons (no `[H2] Lesson N`, e.g. TRR114 pp 4-5) are a
			// separate follow-up; this banks the clean lesson-numbered pages.
			if (reoPage2 && it.type === "table" && Array.isArray(it.block?.rows)) {
				let lnum = null;
				const rows = it.block.rows;
				for (let r = 0; r < Math.min(rows.length, 3) && lnum === null; r++) {
					for (const c of (rows[r] || [])) {
						const m = String(c ?? "").replace(/\u{1f534}|\[\/?RED TEXT\]|\*/gu, "")
							.match(/\[\s*h2\s*\]\s*(?:lesson|ngohe)\s+(\d+)/i);
						if (m) { lnum = parseInt(m[1], 10); break; }
					}
				}
				if (lnum !== null && lnum > lessonOrdinal) {
					// AR-2: reuse a stray empty page before this boundary
					if (current && currentIsEmpty() && !current.isOverview) {
						pages.pop(); current = pages[pages.length - 1] ?? null;
					}
					lessonOrdinal = lnum;
					pageWithinLesson = 0;
					open({ lessonNumber: String(lnum), lessonLabel: `${lnum}.0`,
						pageTitle: "", wtPageStart: it.block?.wtPage });
					closed = false;
					current.items.push(it);   // the [H2] Lesson N table is the page's heading content
					continue;
				}
			}

			// ---- page boundaries ------------------------------------------
			if (primary?.directive === "PAGE_BOUNDARY") {
				const tag = primary.tag;

				// The MTK "Te Aka Taumatua" bilingual template's "[MODULE CONTENT:
				// PAGE 1]" marker (ROUND 212 — the PNR101/102/104 family) parses as
				// a "page" PAGE_BOUNDARY, but it does NOT start a new page: it
				// introduces the OVERVIEW page's own body content (the module
				// introduction that follows the drop-down-menu section). The human
				// developer's 0.0 page = the drop-down menu + this module content,
				// so the marker is consumed here and the content simply continues on
				// the page that is already open. Without this, the generic "page"
				// handling below would have opened a new "page-as-lesson" file and
				// the overview would ship without its introduction. SCOPED to a
				// document whose stream carried the STANDALONE "[Content for DROP
				// DOWN MENU]" opener earlier (_ddSeenOpener — the PNR shape): the
				// TRR203/TRR301 siblings glue this marker onto their drop-down
				// CLOSER inside one red span (so the anchored pattern never matches
				// them anyway), and TRR304 has no drop-down opener at all — all
				// three keep their existing pagination, byte-identical.
				// Data: elements.dual_language.dropdown_menu.module_content_pattern.
				// Env toggle: REODROPMENU_OFF.
				if (tag === "page" && reoPage && _ddSeenOpener
					&& _dlCfg?.dropdown_menu && _dlCfg.dropdown_menu.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF)
					&& new RegExp(_dlCfg.dropdown_menu.module_content_pattern ?? "^\\[module content\\b", "i")
						.test((it.parse?.folded ?? "").trim())) {
					run.AddNote("info", "PageSplitter",
						"[MODULE CONTENT: PAGE n] marker — its content stays on the overview page (MTK drop-down-menu template).");
					// Mark the marker's content tables so the bilingual unfold accepts
					// them even without an "English|Māori" header row (PNR102/PNR104
					// open theirs with "Module Introduction | Kōwae Ako Whakataki"
					// instead; the column orientation is the same English|Māori as
					// everywhere else in this template).
					// ROUND 220 (Chris, the PNR104-00 raw-dump screenshot): flag EVERY
					// table in the module-content REGION, not just the first. PNR104's
					// writer split the same logical content into TWO tables (whakataukī
					// table + "Module Introduction" table — PNR101 has them as ONE);
					// the old first-table-only walk left the second table unflagged, it
					// failed bilingualTable's header requirement, and the whole module
					// introduction shipped as a raw cv2 "bilingual-unbuilt" dump. The
					// region ends at the next structural red marker ([END OF PAGE] /
					// [LESSON N CONTENT] — the first "tag" item), same stop as before.
					// Data: dropdown_menu.module_content_all_tables.
					// Env toggle: REOMODCONTENT_OFF (first-table-only legacy walk).
					const _mcAllTables = _dlCfg.dropdown_menu.module_content_all_tables !== false
						&& !(typeof process !== "undefined" && process.env && process.env.REOMODCONTENT_OFF);
					for (let j = i + 1; j < items.length; j++) {
						if (items[j].type === "table") {
							items[j]._reoModuleContent = true;
							if (!_mcAllTables) break;   // legacy: only a DIRECTLY-following table
							continue;                    // ROUND 220: every region table
						}
						if (items[j].type === "tag") break;   // the next structural marker ends the region
					}
					closed = false;
					continue;
				}

				if (tag === "lesson" || tag === "page") {
					if (singleFile) {
						// AR-3: in-page section break only — keep the item so
						// the converter can render a section separation
						current.items.push(it);
						closed = false;
						continue;
					}
					// AR-2: adjacent boundary tags = one break (an unclosed
					// empty current page is REUSED, not duplicated)
					if (current && currentIsEmpty() && !current.isOverview) {
						run.AddNote("info", "PageSplitter",
							"Adjacent page boundaries merged — no empty page emitted (AR-2).");
						pages.pop();
						current = pages[pages.length - 1] ?? null;
					}

					if (tag === "lesson") {
						// RR-2 happens implicitly: opening a lesson page closes
						// the previous page whether or not [end page] appeared
						lessonOrdinal++;
						pageWithinLesson = 0;
						// the writer's own number wins when present ([LESSON 3]);
						// bare [LESSON] tags fall back to the running ordinal
						const num = it.parse.numbers.length
							? it.parse.numbers[0] : String(lessonOrdinal);
						open({
							lessonNumber: num,
							lessonLabel: `${num}.0`,
							// following text first; embedded payload (in its
							// ORIGINAL case — render text never folds) second
							pageTitle: it.blackAfter.trim()
								|| (normaliser ? normaliser.RenderText(it.text) : ""),
							wtPageStart: it.block.wtPage,
						});
					} else if (current?.lessonNumber === null || current?.isOverview
						|| current?.openedBy === "page-as-lesson") {
						// [PAGE] straight after the overview — or after another
						// page-as-lesson — is the BLL pattern: the writer uses
						// [PAGE] where others use [LESSON], so these files ARE
						// successive lessons (corpus: BLL233-0.0 / -1.0 / -2.0)
						lessonOrdinal++;
						pageWithinLesson = 0;
						open({
							lessonNumber: String(lessonOrdinal),
							lessonLabel: `${lessonOrdinal}.0`,
							pageTitle: "",
							wtPageStart: it.block.wtPage,
							openedBy: "page-as-lesson",
						});
					} else {
						// [PAGE] within a lesson: a new file in the SAME
						// lesson → x.1, x.2 … (spec §5.4 sub-numbering)
						pageWithinLesson++;
						const base = current.lessonNumber;
						open({
							lessonNumber: base,
							lessonLabel: `${base}.${pageWithinLesson}`,
							pageTitle: "",
							wtPageStart: it.block.wtPage,
						});
					}
					closed = false;
					continue;
				}

				// [end page] / [end lesson]
				if (singleFile) { closed = false; continue; }   // AR-3
				if (currentIsEmpty() && !current.isOverview) {
					// RR-3: an [end page] that would close an empty segment is
					// disregarded — the previous page simply continues
					run.AddNote("info", "PageSplitter",
						"[end page] closing an empty segment disregarded (RR-3).");
					continue;
				}
				// AR-1 guard: an [end page] before the intro has appeared on
				// the overview is held open until we know (handled above when
				// the intro arrives; if no intro ever comes, the close stands)
				closed = true;
				continue;
			}

			// ---- ordinary item --------------------------------------------
			if (closed) {
				// content AFTER an [end page]…
				// AR-5: if everything remaining is flat boilerplate (no
				// headings, no interactives), drop it with one note
				const rest = items.slice(i);
				const hasSubstance = rest.some((r) => r.type === "tag"
					&& ["ELEMENT", "INTERACTIVE", "CONTAINER_OPEN"].includes(r.parse.primary?.directive)
					&& r.parse.primary?.tag !== "body");
				if (!hasSubstance) {
					run.AddNote("info", "PageSplitter",
						`Content after the final [end page] (${rest.length} blocks) is writer-form boilerplate — not emitted (AR-5).`);
					break;
				}

				// AR-1 (generalised, PRECISE form): a stray [end page] on the
				// OVERVIEW is disregarded ONLY when what follows is clearly
				// still introduction material — i.e. the next tag span is an
				// introduction-cluster marker: a MID-doc title-bar alias
				// ([Title]/[Introduction]), [module introduction], or
				// [supervisor note]. That is the BLL-family pattern
				// (verified BLL146). ANY other follower (plain headings,
				// body, widgets) means the break is REAL — maths modules
				// open lessons with plain topic headings (MXEX401 collapsed
				// to one page under a looser version of this rule).
				if (current?.isOverview) {
					const INTRO_TAGS = new Set(["title bar", "module introduction", "supervisor note"]);
					let introNext = false;
					for (let k = i; k < Math.min(i + 4, items.length); k++) {
						const peek = items[k];
						if (peek.type !== "tag") continue;
						introNext = INTRO_TAGS.has(peek.parse.primary?.tag);
						break;   // judge by the FIRST tag span only
					}
					if (introNext) {
						run.AddNote("info", "PageSplitter",
							"[end page] on the overview disregarded — an introduction-cluster marker follows ([Title]/[Introduction]/[supervisor note]; AR-1 generalised).");
						closed = false;
						current.items.push(it);
						continue;
					}
				}
				// substance without a [LESSON]/[PAGE] tag: a NORMAL writer
				// pattern (verified on ANZH205 — five of its seven lessons
				// open with just "[end page]" then "[H2] Lesson N: …").
				// The new page is implied; harvest its number/title from the
				// heading that opens it when one is there.
				const heading = it.type === "tag"
					&& ["h1", "h2", "h3", "h4", "h5", "heading"].includes(primary?.tag)
					? (it.blackAfter || it.parse.remainders.join(" ")).trim() : "";
				// "Lesson 4: My Rohe" → number "4", title "My Rohe"
				const lm = heading.match(/^\**\s*lesson\s+(\d+(?:\.\d+)?[a-z]?)\s*[:.\-–—]?\s*(.*)$/i);
				lessonOrdinal = lm ? parseInt(lm[1], 10) : lessonOrdinal + 1;
				pageWithinLesson = 0;
				open({
					lessonNumber: lm ? lm[1] : String(lessonOrdinal),
					lessonLabel: `${lm ? lm[1] : lessonOrdinal}.0`,
					pageTitle: lm ? lm[2].replace(/\**$/, "").trim() : "",
					wtPageStart: it.block.wtPage,
				});
				run.AddNote("info", "PageSplitter",
					`Implicit page break: content continues after [end page] without a [LESSON] tag — opened page ${current.lessonLabel}${lm ? ` ("${current.pageTitle}")` : ""}.`);
				closed = false;
			}
			current.items.push(it);
		}

		// ---- post-pass: fill gaps from the pages' own headings ------------
		// Writers often title lessons only via their first heading ("[H2]
		// Lesson 2: …"); bare [LESSON] tags then leave number/title empty.
		for (const p of pages) {
			if (p.isOverview) continue;
			// HARVESTING A LESSON'S TITLE FROM ITS FIRST HEADING — but only a
			// GENUINE title, not just any heading that happens to appear
			// first. A heading that appears BEFORE the page's first
			// [Activity] box (or an explicit "Lesson N: ..." heading anywhere)
			// really is the lesson's title. But a heading that appears AFTER
			// an activity has already started is usually content belonging to
			// a widget/section INSIDE that activity (for example, a small
			// heading used purely as a label on one panel of a click-and-drag
			// widget) — not the page's title. Using such a heading as the
			// page title would produce titles that the human-built version of
			// the page never actually uses.
			// Data flag: body_region.lesson_title_dedup.harvest_before_activity_only
			// Env toggle: LESSONTITLE_OFF
			const _btaOn = (DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup
				?.harvest_before_activity_only !== false)
				&& !(typeof process !== "undefined" && process.env && process.env.LESSONTITLE_OFF);
			let firstHeading = null;
			for (const it2 of p.items) {
				if (it2.type !== "tag") continue;
				const pt2 = it2.parse.primary?.tag;
				const ht2 = (it2.blackAfter || it2.parse.remainders.join(" ")).replace(/\*/g, "").trim();
				if (_btaOn && pt2 === "activity" && !/^lesson\s+\d/i.test(ht2)) break;   // stop at 1st activity
				if (["h1", "h2", "h3", "h4", "h5", "heading"].includes(pt2)
					&& (it2.blackAfter.trim() || it2.parse.remainders.length)) { firstHeading = it2; break; }
			}
			if (!firstHeading) continue;
			const text = (firstHeading.blackAfter || firstHeading.parse.remainders.join(" "))
				.replace(/\*/g, "").trim();
			const lm = text.match(/^lesson\s+(\d+(?:\.\d+)?[a-z]?)\s*[:.\-–—]?\s*(.*)$/i);
			// FILLING IN A BARE-NUMBER PAGE TITLE FROM THE FIRST HEADING.
			//
			// Sometimes a "[LESSON] N" tag's ONLY payload is the digit itself
			// (e.g. just "1"), which used to leave p.pageTitle set to that
			// bare number. The header would then literally show "1" as the
			// lesson's name instead of a real title like "Plot Structure" —
			// and the code below that fills in a title from the page's first
			// heading only ran when pageTitle was completely EMPTY, so a
			// bare-number title slipped through untouched. Now this ALSO
			// overwrites a pageTitle that is nothing but a bare lesson
			// number/label, filling it in from the first heading exactly the
			// same way the "totally empty" case already worked.
			// This has a knock-on benefit: once the real lesson name is in
			// the page header, the logic elsewhere (in ContentConverter) that
			// removes a repeated lesson-title heading from the page BODY can
			// recognise the match — so a duplicate body heading like
			// "[H2] Lesson 1: Plot Structure" gets correctly removed instead
			// of appearing twice on the page.
			// SAFE TO ALWAYS APPLY: none of the human-built lesson pages we
			// measured (0 out of 555) ever use a bare number as the visible
			// header title, so this change can only make things better or
			// leave them unchanged.
			// Data flag: lesson_title_dedup.lesson_name_from_heading
			// Env toggle: LESSONNAME_OFF (reverts to leaving a bare-number
			// title in place, in which case the body heading is no longer
			// de-duplicated either)
			const _lnCfg = (typeof DataService !== "undefined"
				&& DataService.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.lesson_name_from_heading);
			const _lnOn = (_lnCfg?.enabled !== false)
				&& !(typeof process !== "undefined" && process.env && process.env.LESSONNAME_OFF);
			const _bareNum = /^\s*\d+(?:\.\d+)?[a-z]?\s*$/i.test(String(p.pageTitle ?? "").trim());
			const _newTitle = (lm ? lm[2] : text).trim();
			if (!p.pageTitle) p.pageTitle = _newTitle;
			else if (_lnOn && _bareNum && _newTitle) p.pageTitle = _newTitle;
			if (lm && p.lessonNumber !== lm[1]) {
				// the writer's own heading number wins over our ordinal —
				// but a disagreement is worth a summary line
				if (p.lessonNumber && p.lessonNumber !== lm[1]) {
					run.AddNote("info", "PageSplitter",
						`Page ${p.lessonLabel}: heading says "Lesson ${lm[1]}" — using the heading's number.`);
				}
				p.lessonNumber = lm[1];
				p.lessonLabel = `${lm[1]}.0`;
			}
		}

		// RR-4: an opening segment that is only headings (no body content)
		// merges forward into the next page rather than shipping a stub
		if (pages.length >= 2) {
			const first = pages[0];
			const hasBody = first.items.some((it) =>
				(it.type === "black" && it.text.trim())
				|| it.type === "table"
				|| (it.type === "tag" && it.blackAfter.trim() && it.parse.primary?.tag !== "title bar"));
			// EXCEPTION for bilingual (reoMode) modules: their overview page
			// (0.0) is DELIBERATELY empty of body content — it's just the
			// module's menu page, and the menu itself lives in the page
			// header (#header), not in the body content this check is
			// looking at. So an empty reoMode overview must NOT be merged
			// forward into lesson 1; it needs to stay as its own separate
			// page even though it has no items of its own.
			if (!hasBody && !seenIntro && !(reoPage && first.isOverview)) {
				run.AddNote("warn", "PageSplitter",
					"Overview segment had headings only — merged forward into the first lesson page (RR-4).");
				pages[1].items = [...first.items, ...pages[1].items];
				pages[1].isOverview = true;
				pages[1].lessonLabel = first.lessonLabel ?? pages[1].lessonLabel;
				pages.shift();
			}
		}

		// ---- label uniqueness pass ----------------------------------------
		// Writers sometimes reuse "Lesson N" headings (observed in NCEA
		// templates), which would duplicate lesson labels (acks groups +
		// module-code numbering). Output FILENAMES are sequential and never
		// collide; labels are deduped here, with each collision surfaced.
		const seen = new Set();
		for (const p of pages) {
			if (!p.lessonLabel) continue;
			if (seen.has(p.lessonLabel)) {
				const original = p.lessonLabel;
				// bump to the next free integer label
				let n = Math.floor(parseFloat(original)) + 1;
				while (seen.has(`${n}.0`)) n++;
				p.lessonNumber = String(n);
				p.lessonLabel = `${n}.0`;
				run.AddNote("warn", "PageSplitter",
					`Duplicate lesson label ${original} (writers reused the number) — relabelled to ${p.lessonLabel}; check the source numbering.`);
			}
			seen.add(p.lessonLabel);
		}

		return pages;
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { PageSplitter };
