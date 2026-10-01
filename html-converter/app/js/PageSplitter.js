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
		// page-splitting logic further down never treats it as a place to
		// start a new page — without this, lesson 1's content would fall onto
		// the overview page instead of getting its own page, and every lesson
		// after it would be numbered one lower than it should be (the item
		// stream here starts right at lesson 1, because the overview's own body
		// text was already trimmed off earlier in the pipeline).
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
		// is bilingual. The vast majority of Writers Templates carry this
		// heading, yet only a small number of modules
		// are genuinely bilingual. So mtkFlag being true is treated as WEAK
		// evidence, and is only trusted when explicitly turned on via a data
		// flag or the MTKREO_OFF env var. Genuine bilingual detection comes
		// from the OTHER two signals below and is unaffected: the module's
		// body carries the reoTranslate CSS class, or its module code starts
		// with "TRR" or "PNR".
		// Data flag: Emit_Templates.json elements.dual_language.use_mtk_flag
		// Env toggle: MTKREO_OFF (set it to trust mtkFlag as a bilingual
		// signal — the more permissive behaviour)
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
		// bilingual: with mtkFlag not trusted as a bilingual signal on its
		// own (see above), a non-bilingual module can hit AR-4's "new
		// sub-document" behaviour on a mid-document title bar that was never
		// meant to start a new document. These two rules cover that situation
		// generally, for any module.
		// Data flag: Emit_Templates.json page_split_rules
		// Env toggle: MTKPAGE_OFF disables both rules below (MTKREO_OFF also
		// disables them, as a side effect of making mtkFlag a trusted
		// bilingual signal — with it on, reoPage handles mid-doc title bars
		// itself and this branch is never reached)
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
		// Rule 4 — an EMPTY [TITLE BAR] on the still-open overview is the writer's section marker, never AR-4's twin
		// document (data page_split_rules.empty_titlebar_inpage; env EMPTYTB_OFF)
		const _etb = _psRules?.empty_titlebar_inpage;
		const _etbOn = !!_etb && _etb.enabled !== false && !_psRulesOff
			&& !(typeof process !== "undefined" && process.env && process.env[_etb.env ?? "EMPTYTB_OFF"]);
		// Rule 3 — a [TITLE BAR] on a freshly opened LESSON page is that lesson's title (data
		// page_split_rules.lesson_titlebar_inpage; env LESSONTB_OFF)
		const _ltb = _psRules?.lesson_titlebar_inpage;
		const _ltbOn = !!_ltb && _ltb.enabled !== false && !_psRulesOff
			&& !(typeof process !== "undefined" && process.env && process.env[_ltb.env ?? "LESSONTB_OFF"]);
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
		// THE MID-PAGE LESSON HEADING OPENS ITS LESSON PAGE. The implicit-page-break branch below
		// harvests a "Lesson N: …" heading only right after an [end page]; a writer who opens a lesson
		// with the heading alone ("[H1] Lesson Four: Creating movement…" DAN1004, "[H2] Lesson 2 The
		// Negative Powers of 10" MXDI301, "[H1] Lesson 3 Carbon Compounds" CBI1008) or with a black
		// "[LESSON 5]" / "LESSON 3" line (MXS1004, GEO1004 / 1006 — the marker typed without the red
		// style) would otherwise have that lesson merged into the page before it; the human starts a
		// page there. PRE-SCAN: candidate items = an h1–h3 heading whose
		// words open "Lesson <N>" (digits or a number word), or a black line that is exactly
		// "[LESSON N]" / an upper-case "LESSON N …"; a candidate needs min_items_after items before the
		// next candidate or page boundary (a lesson LIST on one page is not a set of openers). At run
		// time it opens page N.0 only on a lesson page (never the overview), off single-file / reoMode
		// modules, when N is HIGHER than the lesson in effect; the black marker line is consumed.
		// Data: page_split.mid_page_lesson_heading. Env toggle: MIDLESSON_OFF.
		const _mlh = DataService.Data.EmitTemplates.page_split?.mid_page_lesson_heading;
		const _mlhOn = !!_mlh && _mlh.enabled !== false && !singleFile && !reoPage
			&& !(typeof process !== "undefined" && process.env && process.env[_mlh.env ?? "MIDLESSON_OFF"]);
		const _midOpeners = new Map();
		let _bac = null, _bacRe = null;   // black_marker_any_case (read by the implicit page break too)
		if (_mlhOn) {
			const WORDS = _mlh.number_words ?? {};
			const num = (w) => /^\d+$/.test(w) ? parseInt(w, 10) : (WORDS[String(w).toLowerCase()] ?? null);
			const headRe = new RegExp(_mlh.heading_pattern ?? "^lesson\\s+(\\d+|[a-z]+)\\b\\s*[:.\\-–—]?\\s*(.*)$", "i");
			const blackRe = new RegExp(_mlh.black_pattern ?? "^(?:\\[\\s*lesson\\s+(\\d+)\\s*\\]|LESSON\\s+(\\d+)\\b.*)$");
			// A black '[LESSON N]' in ANY case is a candidate too (black_pattern has no i flag, so GEO1006's
			// upper-case markers need this). Data mid_page_lesson_heading.black_marker_any_case; env BLACKLESSON_OFF.
			_bac = _mlh.black_marker_any_case ?? null;
			_bacRe = _bac && _bac.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[_bac.env ?? "BLACKLESSON_OFF"])
				? new RegExp(_bac.pattern ?? "^\\[\\s*lesson\\s+(\\d+)\\s*\\]$", _bac.flags ?? "i") : null;
			const _sn = _mlh.span_number;
			const _snRe = _sn && _sn.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[_sn.env ?? "SPANLESSON_OFF"])
				? new RegExp(_sn.pattern ?? "^lesson\\s+(\\d+|[a-z]+)\\s*[:.\\-–—]?$", "i") : null;
			const _sf = _sn?.split_form;
			const _sfOn = !!_snRe && !!_sf && _sf.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[_sf.env ?? "SPLITLESSON_OFF"]);
			const cands = [];
			// A numbered «N.0 TITLE» lesson title (GER1002's `[title] 2.0 …`, its red «4.0» + black title) is a
			// candidate too (mid_page_lesson_heading.title_form; env TITLENUM_OFF)
			const _tf = _mlh.title_form;
			const _tfOn = !!_tf && _tf.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[_tf.env ?? "TITLENUM_OFF"]);
			const _tfRe = _tfOn ? new RegExp(_tf.pattern ?? "^(\\d+)\\.0\\s+(\\S.*)$") : null;
			const _tfSpanRe = _tfOn && _tf.number_span_pattern ? new RegExp(_tf.number_span_pattern) : null;
			items.forEach((it, idx) => {
				if (_tfOn && it.type === "tag") {
					const own = String(it.blackAfter || "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
					const red = String(it.text ?? "").replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
					if ((_tf.tags ?? ["title bar"]).includes(it.parse?.primary?.tag)) {
						const m = own.match(_tfRe);
						if (m) { cands.push({ idx, n: parseInt(m[1], 10), title: m[2].trim(), consume: false }); return; }
					} else if (_tfSpanRe && !it.parse?.primary?.tag && own && _tfSpanRe.test(red)) {
						cands.push({ idx, n: parseInt(red.match(_tfSpanRe)[1], 10), title: own, consume: false });
						return;
					}
				}
				if (it.type === "tag" && (_mlh.heading_tags ?? ["h1", "h2", "h3"]).includes(it.parse?.primary?.tag)) {
					const h = String(it.blackAfter || (it.parse?.remainders ?? []).join(" ")).replace(/\*/g, "").replace(/\s+/g, " ").trim();
					const m = h.match(headRe);
					if (m && num(m[1]) != null) cands.push({ idx, n: num(m[1]), title: (m[2] ?? "").trim(), consume: false });
					else if (_snRe) {
						// «Lesson N» typed INSIDE the red heading span, the black text its title (CBI1009's
						// `[H2] Lesson 2` + «Solubility Rules»). Data mid_page_lesson_heading.span_number; env SPANLESSON_OFF.
						const f = String(it.parse?.free ?? "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
						const m2 = f.match(_snRe);
						if (m2 && num(m2[1]) != null) cands.push({ idx, n: num(m2[1]), title: h, consume: false });
						else if (_sfOn && new RegExp(_sf.word_pattern ?? "^lesson\\s*[:.\\-–—]?$", "i").test(f)) {
							// The split form: a red «Lesson» + a black «N Title» (CBI1008's `[H1] Lesson` + «4 The Law of
							// Conservation of Mass»). Data span_number.split_form; env SPLITLESSON_OFF.
							const m3 = h.match(new RegExp(_sf.black_pattern ?? "^(\\d+)\\b\\s*[:.\\-–—]?\\s*(.*)$"));
							if (m3) cands.push({ idx, n: parseInt(m3[1], 10), title: (m3[2] ?? "").trim(), consume: false });
						}
					}
				} else if (it.type === "black") {
					const t = String(it.text ?? "").replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
					const m = t.match(blackRe);
					if (m) cands.push({ idx, n: parseInt(m[1] ?? m[2], 10), title: "", consume: true });
					else if (_bacRe) {
						const m2 = t.match(_bacRe);
						if (m2) cands.push({ idx, n: parseInt(m2[1], 10), title: "", consume: true, anyCase: true });
					}
				}
			});
			const minAfter = _mlh.min_items_after ?? 3;
			cands.forEach((c, k) => {
				// the next candidate with a DIFFERENT number (a "[LESSON 4]" line and its "[H2] Lesson 4 …" echo are one opener)
				const nx = cands.slice(k + 1).find((d) => d.n !== c.n);
				let end = nx ? nx.idx : items.length;
				for (let q = c.idx + 1; q < end; q++) {
					if (items[q].type === "tag" && items[q].parse?.primary?.directive === "PAGE_BOUNDARY") { end = q; break; }
				}
				if (end - c.idx - 1 >= minAfter) _midOpeners.set(c.idx, c);
			});
		}

		const currentIsEmpty = () => current && !current.items.some((it) =>
			it.type === "table"
			|| (it.type === "black" && it.text.trim())
			|| (it.type === "tag" && (it.blackAfter.trim()
				|| ["ELEMENT", "INTERACTIVE", "CONTAINER_OPEN", "INLINE"].includes(it.parse.primary?.directive))));

		// THE FRONT-MATTER-ONLY LESSON PAGE. A lesson page (not the overview) whose items are ONLY its front
		// matter — section markers ([Lesson Overview] / [Lesson content] / a title-bar alias), ≤ max_headings headings,
		// writer instructions / noise, black text that is blank or made only of WALT / SC lead or list lines, and a body /
		// sub-head tag carrying only such lines — is not ended by the writer's next [end page], bare
		// [LESSON] or [PAGE]: the content after it continues on it (the gold's one page; MXFU301 lesson 4, XLP02 lesson 3).
		// Data page_split.lesson_boundary_guard.front_matter_fold; env FRONTFOLD_OFF.
		const _ffCfg = DataService.Data.EmitTemplates.page_split?.lesson_boundary_guard?.front_matter_fold;
		const _ffOn = !!_ffCfg && _ffCfg.enabled !== false
			&& DataService.Data.EmitTemplates.page_split?.lesson_boundary_guard?.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_ffCfg.env || "FRONTFOLD_OFF"]);
		const _ffMarkers = new Set(_ffOn ? (_ffCfg.markers ?? ["end page", "bare lesson", "page"]) : []);
		// A DOTTED lesson number read from a "Lesson N.M:" heading (the implicit-page opener, the
		// post-pass number override) is the page label verbatim, as for a dotted [LESSON N.M] tag —
		// never "1.2.0" (PWY1001 / 1002 / 1008 / 1009, MXEX301, MXEO301: the gold's 1.2). Data
		// page_split.writer_lesson_numbers.dotted_heading_verbatim; env DOTHEAD_OFF.
		const _dhOn = DataService.Data.EmitTemplates.page_split?.writer_lesson_numbers?.dotted_heading_verbatim === true
			&& !(typeof process !== "undefined" && process.env && process.env.DOTHEAD_OFF);
		// The writer's [PAGE N] opens its own lesson page (see the [PAGE] branch).
		// Data page_split.page_marker_as_lesson; env PAGELESSON_OFF.
		const _pml = DataService.Data.EmitTemplates.page_split?.page_marker_as_lesson;
		const _pmlOn = !!_pml && _pml.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_pml.env || "PAGELESSON_OFF"]);
		const _ffLead = new RegExp(DataService.Data.EmitTemplates.menu?.lesson_overview_implicit?.lead_pattern
			?? "^(we are learning|learning intentions?|you will show|how will i know|i can\\b|success criteria)", "i");
		const _ffList = /^\s*(?:[•\-–—*·o]|\d+[.)]|[a-z][.)])\s+/i;
		const _ffLine = (l) => _ffList.test(l) || _ffLead.test(Utils.Fold(l).replace(/[*_]/g, "").trim());
		const _ffLines = (s) => String(s || "").split(/\n/).map((l) => l.trim()).filter(Boolean);
		const frontMatterOnly = () => {
			if (!_ffOn || !current || current.isOverview || current.lessonNumber === null || !current.items.length) return false;
			// black prose is content even inside the [Lesson Overview] block: SPA1004 lesson 2 runs from its LO lines
			// straight into the lesson's own paragraphs with no marker or heading between them
			let heads = 0;
			for (const x of current.items) {
				if (x.type === "black") {
					if (_ffLines(x.text).every(_ffLine)) continue;
					return false;
				}
				if (x.type !== "tag") return false;                          // a table / image block is content
				const p = x.parse?.primary;
				if (!p) continue;                                            // a writer instruction / noise / unresolved red span
				if (p.directive === "SECTION_MARKER") continue;
				if (/^h[1-6]$/.test(p.tag) || p.tag === "heading") {
					if (++heads > (_ffCfg.max_headings ?? 2)) return false;
					continue;
				}
				if ((p.tag === "body" || p.tag === "sub head") && _ffLines(x.blackAfter).every(_ffLine)) continue;
				return false;
			}
			return true;
		};

		let closed = false;   // true between an [end page] and the next opener

		// Tracks whether this document's stream carried the STANDALONE
		// "[Content for DROP DOWN MENU]" opener (the MTK bilingual
		// template's PNR shape). Only such a document treats a later "[MODULE
		// CONTENT: PAGE n]" marker as overview content rather than a page break.
		let _ddSeenOpener = false;
		const _ddOpenerRe = (_dlCfg?.dropdown_menu && _dlCfg.dropdown_menu.enabled !== false)
			? new RegExp(_dlCfg.dropdown_menu.opener_pattern ?? "^\\[content for drop[ -]?down menu\\]$", "i")
			: null;

		// KB 01D «explicit numbers preserved»: every explicit integer [LESSON N] tag's position, so an
		// implicit page break can tell whether the writer's next number is still to come (see the
		// implicit-break opener below). Data page_split.implicit_break_sub_page; env IMPLSUB_OFF.
		const _ibs = DataService.Data.EmitTemplates.page_split?.implicit_break_sub_page;
		const _ibsOn = !!_ibs && _ibs.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_ibs.env ?? "IMPLSUB_OFF"]);
		const _explicitLessonAt = [];
		if (_ibsOn) items.forEach((x, k) => {   // every [LESSON] tag; a bare or dotted one records n = null (it blocks the rule)
			if (x.type === "tag" && x.parse?.primary?.tag === "lesson")
				_explicitLessonAt.push({ k, n: x.parse.numbers?.length && /^\d+$/.test(String(x.parse.numbers[0])) ? parseInt(x.parse.numbers[0], 10) : null });
		});

		// The FRFUN multi-file levels overview: a level-first title marker met on the overview opens the
		// first level page (see the branch before «ordinary item» below).
		// Data body_region.fundamentals_panels.level_overview; env LEVELOV_OFF.
		const _lvOv = DataService.Data.EmitTemplates.body_region?.fundamentals_panels?.level_overview;
		const _lvOvRe = (_lvOv && _lvOv.enabled !== false && _lvOv.split_overview_at_marker === true
			&& run?.resolvedRules?.level_overview === "multi-file"
			&& !(typeof process !== "undefined" && process.env && process.env[_lvOv.env ?? "LEVELOV_OFF"]))
			? new RegExp(_lvOv.marker_pattern, "iu") : null;

		// The open side tab (page_split.side_tab_end_page; env SIDETABEND_OFF)
		const _ste = DataService.Data.EmitTemplates.page_split?.side_tab_end_page;
		const _steOn = !!_ste && _ste.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_ste.env ?? "SIDETABEND_OFF"]);
		const _steOpenRe = _steOn ? new RegExp(_ste.opener_text_pattern ?? "side\\s*tab", "i") : null;
		const _steCloseRe = _steOn ? new RegExp(_ste.closer_pattern ?? "^\\[\\s*end(?:\\s+of)?\\s+tab\\b", "i") : null;
		const _steStageRes = _steOn ? (_ste.stage_marker_patterns ?? []).map((p) => new RegExp(p, "i")) : [];
		let _openSideTab = null;
		let _dupOpeningSkip = -1;   // the repeated heading of a pasted-twice opening (duplicate_opening_drop)
		// The EXPlore stage header opens its own page (page_split.stage_opener_break; env STAGEBREAK_OFF):
		// the break index of each bare «Lesson overview:» label, walked back over the stage's header run
		const _sob = DataService.Data.EmitTemplates.page_split?.stage_opener_break;
		const _sobOn = !!_sob && _sob.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_sob.env ?? "STAGEBREAK_OFF"]);
		const _stageBreakAt = new Set();
		let _stageDialect = false;
		if (_sob && _sob.enabled !== false) {
			const _sobClean = (s) => String(s ?? "").replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").replace(/\s+/g, " ").trim();
			const _sobLabRe = new RegExp(_sob.label_pattern ?? "^lesson overview\\s*:?$", "i");
			const _sobLabs = [];
			items.forEach((x, k) => { if (x.type === "tag" && !x.parse?.primary?.tag && _sobLabRe.test(_sobClean(x.text))) _sobLabs.push(k); });
			// the module's stage dialect (ContentConverter's template_fallback.stage_dialect reads it; its own env)
			_stageDialect = _sobLabs.length >= (_sob.min_labels ?? 2);
			if (_sobOn && _stageDialect) {
				for (const L of _sobLabs) {
					let b = L, steps = 0;
					for (let k = L - 1; k >= 0 && steps < (_sob.lead_max ?? 4); k--) {
						const x = items[k];
						if (x.type === "black" && !String(x.text ?? "").trim()) continue;
						const bt = x.type === "black" ? _sobClean(x.text) : "";
						const isInstr = x.type === "tag" && x.parse?.class === "instruction" && !x.parse?.primary?.tag;
						const isBoldTitle = x.type === "black" && /^\*\*[^*]+\*\*$/.test(bt)
							&& bt.replace(/\*/g, "").trim().split(/\s+/).length <= (_sob.lead_bold_max_words ?? 8);
						if (!isInstr && !isBoldTitle) break;
						b = k; steps++;
					}
					_stageBreakAt.add(b);
				}
			}
		}
		for (let i = 0; i < items.length; i++) {
			const it = items[i];
			const primary = it.type === "tag" ? it.parse.primary : null;
			if (_ddOpenerRe && !_ddSeenOpener && it.type === "tag"
				&& _ddOpenerRe.test((it.parse?.folded ?? "").trim())) _ddSeenOpener = true;
			if (i === _dupOpeningSkip) continue;   // the pasted-twice opening's repeated heading
			if (_steOn && it.type === "tag") {
				const _f = (it.parse?.folded ?? "").trim();
				if (primary?.tag === "tab n" && _steOpenRe.test(_f)) {
					_openSideTab = (_f.replace(/^\[\s*new\s+side\s+tab\s*/i, "").replace(/\]\s*$/, "").trim()
						|| String(it.blackAfter ?? "").replace(/\*+/g, "").trim()).toLowerCase() || null;
				} else if (_steCloseRe.test(_f)) _openSideTab = null;
			}
			if (_stageBreakAt.has(i) && !closed && current && !currentIsEmpty()) {
				closed = true;
				run.AddNote("info", "PageSplitter",
					`The stage header "${String(it.text ?? "").replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").replace(/\s+/g, " ").trim().slice(0, 60)}" opens its own page (page_split.stage_opener_break).`);
			}

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
				} else if (_ltbOn && !current.isOverview && current.items.every((x) => (x.type === "black" && !String(x.text || "").trim())
					|| (x.type === "tag" && x.parse?.primary?.directive === "PAGE_BOUNDARY"))) {
					// A [TITLE BAR] arriving on a FRESH lesson page (only its opener tag so far) is that
					// lesson's title, never AR-4's twin document (page_split_rules.lesson_titlebar_inpage; LESSONTB_OFF)
					run.AddNote("info", "PageSplitter",
						`[TITLE BAR] on the freshly opened lesson page ${current.lessonLabel ?? ""} kept in-page as the lesson's title (page_split_rules.lesson_titlebar_inpage).`);
					// the lesson has no title of its own yet: the title bar's text names it (its leading "1.0" label stripped)
					if (!current.pageTitle) {
						const _t = String(it.blackAfter || "").replace(/\*+/g, "").replace(/^\s*\d+(?:\.\d+)*\s*[:–—-]?\s*/, "").trim();
						if (_t) current.pageTitle = _t;
					}
					current.items.push(it);
					closed = false;
					continue;
				} else if (_etbOn && current.isOverview && !closed && !String(it.blackAfter || "").trim()
					&& !String(it.text || "").replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").replace(/\[[^\]]*\]/g, "").trim()) {
					// An empty [TITLE BAR] on the open overview stays in-page (page_split_rules.empty_titlebar_inpage)
					run.AddNote("info", "PageSplitter",
						"An empty second [TITLE BAR] on the open overview kept in-page — a section marker, not a twin document (page_split_rules.empty_titlebar_inpage).");
					// the block it heads is the overview: remembered, so the page's close can put it before the introduction
					if (current._etbAt == null) current._etbAt = current.items.length;
					current.items.push(it);
					closed = false;
					continue;
				} else if (_dupInpage && _tbIsDup && _psRules?.duplicate_opening_drop?.enabled !== false && !!_psRules?.duplicate_opening_drop
					&& !(typeof process !== "undefined" && process.env && process.env[_psRules.duplicate_opening_drop.env ?? "DUPOPEN_OFF"])
					&& (() => {
						// The opening [TITLE BAR] + heading pasted twice (BLL124): the repeat is dropped with its heading
						const _hFold = (x) => Utils.Fold(String(x?.blackAfter || "").replace(/\*/g, "")).trim();
						const _isH = (x) => x?.type === "tag" && /^h[1-6]$/.test(String(x.parse?.primary?.tag || ""));
						let a = current.items.length - 1;
						while (a >= 0 && current.items[a].type === "black" && !String(current.items[a].text ?? "").trim()) a--;
						let b = i + 1;
						while (b < items.length && items[b].type === "black" && !String(items[b].text ?? "").trim()) b++;
						if (a < 0 || !_isH(current.items[a]) || !_isH(items[b]) || !_hFold(items[b]) || _hFold(items[b]) !== _hFold(current.items[a])) return false;
						_dupOpeningSkip = b;
						return true;
					})()) {
					run.AddNote("info", "PageSplitter",
						"A pasted-twice opening [TITLE BAR] + heading dropped — one opening (page_split_rules.duplicate_opening_drop).");
					closed = false;
					continue;
				} else if (_sfSuppress || (_dupInpage && _tbIsDup)) {
					// Rule 1 (single-file modules): a mid-document [TITLE BAR]
					// stays in-page, because AR-4 respects the registry's
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
			// untouched. The diphthong-tail lessons (no `[H2] Lesson N`, e.g. TRR114 pp 4-5) are not
			// split by this rule.
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

				// An [Intro Page] span typed right after [MODULE INTRODUCTION] is the introduction's own label, never a
				// page (XLP05): consumed with its label, the page continues. Data page_split.intro_cluster_forms.intro_page_label;
				// env INTROPAGE_OFF.
				{
					const _ipl = DataService.Data.EmitTemplates.page_split?.intro_cluster_forms?.intro_page_label;
					if (_ipl && _ipl.enabled !== false && _ipl.pattern
						&& !(typeof process !== "undefined" && process.env && process.env[_ipl.env ?? "INTROPAGE_OFF"])
						&& new RegExp(_ipl.pattern, "i").test((it.parse?.folded ?? "").trim())) {
						let q = i - 1;
						while (q >= 0 && items[q].type === "black" && !String(items[q].text ?? "").trim()) q--;
						if (q >= 0 && items[q].type === "tag" && items[q].parse?.primary?.tag === "module introduction") {
							run.AddNote("info", "PageSplitter",
								`"${(it.parse?.folded ?? "").trim()}" right after [MODULE INTRODUCTION] is the introduction's label — no new page (intro_cluster_forms.intro_page_label).`);
							continue;
						}
					}
				}

				// The MTK "Te Aka Taumatua" bilingual template's "[MODULE CONTENT:
				// PAGE 1]" marker (the PNR101/102/104 family) parses as
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
				// three keep their own pagination.
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
					// Flag EVERY table in the module-content REGION, not just the first. A
					// writer may split the same logical content into TWO tables (PNR104: a
					// whakataukī table + a "Module Introduction" table — PNR101 has them as
					// ONE); a first-table-only walk would leave the second table unflagged, it
					// would fail bilingualTable's header requirement, and the whole module
					// introduction would ship as a raw cv2 "bilingual-unbuilt" dump. The
					// region ends at the next structural red marker ([END OF PAGE] /
					// [LESSON N CONTENT] — the first "tag" item).
					// Data: dropdown_menu.module_content_all_tables.
					// Env toggle: REOMODCONTENT_OFF (first table only).
					const _mcAllTables = _dlCfg.dropdown_menu.module_content_all_tables !== false
						&& !(typeof process !== "undefined" && process.env && process.env.REOMODCONTENT_OFF);
					for (let j = i + 1; j < items.length; j++) {
						if (items[j].type === "table") {
							items[j]._reoModuleContent = true;
							if (!_mcAllTables) break;   // toggle off: only a DIRECTLY-following table
							continue;                    // every region table
						}
						if (items[j].type === "tag") break;   // the next structural marker ends the region
					}
					closed = false;
					continue;
				}

				// The XDLS900 "[Sticky Nav Layout with the following … repeat on EVERY
				// PAGE]" marker (the XDLS902-906/908 family) parses as a
				// "page" PAGE_BOUNDARY only because the word PAGE appears inside its
				// bracket text — it is NOT a page break at all, it's the writer's
				// set-up instruction for the site's sticky-navigation include
				// (js/stickyNav.js in the human-built pages). Treating it as a
				// boundary would fragment the modules (XDLS906's choice page split in
				// two; XDLS908's lesson 1 split mid-content). The marker is consumed
				// here, and the ONE-column link table that directly follows it is
				// flagged _stickyNavTable so ContentConverter can surface it as a
				// Designer/Developer To Do note instead of a raw dumped table (the
				// human drops the table entirely — its content lives in the online
				// sticky-nav configuration, not the page). Scoped by the span's own
				// "sticky nav" tag + the anchored folded-text pattern, so ordinary
				// [PAGE] boundaries are untouched by construction.
				// Data: body_region.choice_page_tiles.sticky_layout_pattern.
				// Env toggle: TABNAVDROP_OFF (off = the page-boundary split + the
				// raw table dump).
				const _cpCfg = DataService.Data.EmitTemplates.body_region?.choice_page_tiles;
				if (tag === "page" && _cpCfg && _cpCfg.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.TABNAVDROP_OFF)
					&& it.parse.tags.some((t) => t.tag === "sticky nav")
					&& new RegExp(_cpCfg.sticky_layout_pattern ?? "^\\[\\s*sticky nav layout\\b", "i")
						.test((it.parse?.folded ?? "").trim())) {
					run.AddNote("info", "PageSplitter",
						"[Sticky Nav Layout …] marker — a navigation set-up instruction, not a page break; its link table becomes a To Do note.");
					for (let j = i + 1; j < items.length; j++) {
						if (items[j].type === "table") { items[j]._stickyNavTable = true; break; }
						if (items[j].type === "tag") break;   // the next structural marker ends the search
					}
					closed = false;
					continue;
				}

				// THE BURIED-MARKER GUARD (as in ENGS404). A span becomes a lesson/page
				// boundary merely because the word "lesson"/"page" turns up inside writer
				// prose: "[insert lesson from ENO511 …]" would invent a page numbered 511,
				// "[Designer note: Please insert old lesson from here…]" another, and
				// "[Rollover for mana: … complete History fundamental lesson 7 …]" — a hover
				// definition — one in three HIS modules. None of them is a page break.
				//
				// THE CONTAINMENT STATEMENT: the primary must have matched
				// how:"embedded" (the clean_hows distinction — the tag word buried
				// mid-bracket rather than matched as a whole token). Boundaries that
				// matched exact/denumbered/denumbered_head are UNTOUCHABLE BY
				// CONSTRUCTION; only the embedded pool reaches this guard.
				//
				// Within that pool the marker is disregarded when EITHER the span
				// is instruction-dominant by the EXISTING TagNormaliser predicate
				// (every tag embedded + a recognised writer-instruction cue +
				// >= min_words of prose), OR the bracket text BEFORE the marker
				// word carries a deny token (a leading instruction verb, or a
				// FOREIGN module code like "PHO1032" — the cross-module "copy that
				// lesson" reference form). FAIL-OPEN: an unrecognised embedded
				// form stays a boundary, so every genuine embedded marker
				// survives ([Lesson summary], [lesson title], [Final Page], [Next Page],
				// [Intro page], [Page N of diary], [page ends] …).
				//
				// The span is NOT dropped — it simply stops being a page break, so
				// its own content still renders wherever it sits (constraint 1:
				// never silently strip a documented instruction).
				// Data: page_split.lesson_boundary_guard.instruction_guard.
				// Env toggle: LESSONGUARD_OFF.
				const _lbgCfg = DataService.Data.EmitTemplates.page_split?.lesson_boundary_guard;
				const _lbgOn = _lbgCfg && _lbgCfg.enabled !== false;
				// A REVISION NOTE THAT POINTS AT A LESSON. (b) an `end lesson` closer whose bracket names ANOTHER
				// module ("[End - From Lesson 3 in old ENO304 module]", ENGC206) ends a block copied from that module, not this
				// module's lesson; (a) below: the preposition lead also denies an embedded `lesson` span ("[Found in Lesson 3
				// of old module]"). Data lesson_boundary_guard.reference_forms.lesson_notes; env REFLESSON_OFF.
				const _ln = _lbgCfg?.reference_forms?.lesson_notes;
				const _lnOn = !!_lbgOn && !!_ln && _ln.enabled !== false && _lbgCfg.reference_forms.enabled !== false
					&& !(typeof process !== "undefined" && process.env
						&& (process.env[_ln.env ?? "REFLESSON_OFF"] || process.env[_lbgCfg.reference_forms.env ?? "REFMARK_OFF"]));
				if (_lnOn && (_ln.foreign_code_close_tags ?? []).includes(tag) && _lbgCfg.foreign_code_pattern) {
					const _own = String(run.moduleCode || "").toUpperCase();
					let _fc = false;
					for (const m of String(it.text ?? "").toUpperCase().matchAll(new RegExp(_lbgCfg.foreign_code_pattern, "g"))) {
						if (m[0] !== _own) { _fc = true; break; }
					}
					if (_fc) {
						run.AddNote("info", "PageSplitter",
							`"${String(it.parse?.folded ?? "").trim().slice(0, 60)}" closes a block copied from another module — not a page boundary (lesson_boundary_guard.reference_forms.lesson_notes).`);
						it._boundaryDenied = "note";
						current?.items.push(it);
						closed = false;
						continue;
					}
				}
				if (_lbgOn && _lbgCfg.instruction_guard !== false
					&& (tag === "lesson" || tag === "page")
					&& primary.how === "embedded"
					&& !(typeof process !== "undefined" && process.env && process.env.LESSONGUARD_OFF)) {
					const _folded = String(it.parse?.folded ?? "");
					let _deny = false;
					if (normaliser && typeof normaliser.IsInstructionDominant === "function"
						&& normaliser.IsInstructionDominant(it.parse,
							_lbgCfg.instruction_dominant_min_words ?? 8)) _deny = true;
					const _raw = String(it.text ?? "");
					// A CROSS-MODULE REFERENCE. "[insert lesson from ENO511 …]",
					// "[Copy PHO1032 lesson 8]", "[PHO1011 lesson 5.1-5.3]" name
					// ANOTHER module's lesson for the developer to copy in. A
					// foreign module code in the bracket settles it: whatever the
					// span is, it is not THIS module's page boundary. The run's own
					// code is excluded so a writer who names their own module in a
					// genuine marker is untouched.
					if (!_deny && _lbgCfg.foreign_code_pattern) {
						const _own = String(run.moduleCode || "").toUpperCase();
						for (const m of _raw.toUpperCase().matchAll(new RegExp(_lbgCfg.foreign_code_pattern, "g"))) {
							if (m[0] !== _own) { _deny = true; break; }
						}
					}
					// A HOVER/ROLLOVER DEFINITION. "[Rollover for mana: … complete
					// History fundamental lesson 7 …]" is a hover trigger whose
					// definition happens to mention a lesson — vocabulary, not
					// structure. Tested on the text BEFORE the marker word so a
					// genuine marker can never match.
					if (!_deny && _lbgCfg.deny_lead_pattern) {
						const _at = _raw.toLowerCase().indexOf(tag);
						const _lead = _at > 0 ? _raw.slice(0, _at) : "";
						if (_lead && new RegExp(_lbgCfg.deny_lead_pattern, "i").test(_lead)) _deny = true;
					}
					// A SECTION LABEL. The writer's "[Lesson Summary]" (HIS1002, MXFU402 — a red label before
					// the lesson's own "[H3] Lesson Summary" heading) and the inline "[lesson title]" (PES1008 —
					// "[H2] *Lesson 2* [lesson title] *Heat Capacity Calculations*") name a PART of the lesson,
					// not a new one; the human keeps both on the lesson page. Data
					// lesson_boundary_guard.deny_marker_pattern; env LABELMARK_OFF.
					// A PLACEMENT NOTE. "[Kōwhai Avatar – right hand side of the page]", "[Insert bookworm on
					// right side of page …]" (BLLR201–203), "[Create two new colour boxes to go on the side of …]"
					// (ART1006) say WHERE on the page something goes — 'page' is a position, not a boundary. Data
					// lesson_boundary_guard.deny_position_pattern; env POSNOTE_OFF.
					if (!_deny && _lbgCfg.deny_position_pattern
						&& !(typeof process !== "undefined" && process.env && process.env.POSNOTE_OFF)
						&& new RegExp(_lbgCfg.deny_position_pattern, "i").test(_folded)) _deny = true;
					// A REFERENCE. A preposition (+ determiners) before the
					// marker word means the note POINTS AT a page or lesson ("… repeat on EVERY PAGE", "navigate forward to lesson 5",
					// "from this page", "on student page", "rewrite of lesson 1 …") — a genuine marker puts the word first or after a
					// label word. Data lesson_boundary_guard.reference_forms.lead_pattern; env REFMARK_OFF.
					const _rf = _lbgCfg.reference_forms;
					if (!_deny && _rf && _rf.enabled !== false && _rf.lead_pattern
						&& [...(_rf.lead_tags ?? ["page"]), ...(_lnOn && !closed ? (_ln.lead_tags_extra ?? []) : [])].includes(tag)
						&& !(typeof process !== "undefined" && process.env && process.env[_rf.env ?? "REFMARK_OFF"])) {
						const _low = _raw.toLowerCase();
						const _at2 = _low.indexOf(tag);
						const _lead2 = _at2 > 0 ? _low.slice(0, _at2).split("[").pop() : "";
						if (_lead2.trim() && new RegExp(_rf.lead_pattern, "i").test(_lead2)) _deny = true;
					}
					const _lmOn = !(typeof process !== "undefined" && process.env && process.env.LABELMARK_OFF);
					const _noteDeny = _deny;   // every denial above is a writer NOTE; the two below are section LABELS
					if (!_deny && _lmOn && _lbgCfg.deny_marker_pattern
						&& new RegExp(_lbgCfg.deny_marker_pattern, "i").test(_folded.trim())) _deny = true;
					// the summary label is a boundary only when a whole run of content follows it (HIS1002's
					// first "[Lesson Summary]" is where lesson 2 — typed with no marker of its own — begins);
					// before a short summary and the next marker it is part of the lesson
					if (!_deny && _lmOn && _lbgCfg.deny_short_marker_pattern
						&& new RegExp(_lbgCfg.deny_short_marker_pattern, "i").test(_folded.trim())) {
						const _max = _lbgCfg.deny_short_marker_max_items ?? 12;
						let _n = 0, _hit = false;
						for (let q = i + 1; q < items.length && _n <= _max; q++, _n++) {
							const x = items[q];
							if (x.type === "tag" && x.parse?.primary?.directive === "PAGE_BOUNDARY") { _hit = true; break; }
						}
						if (_hit || _n < _max) _deny = true;
					}
					if (_deny) {
						run.AddNote("info", "PageSplitter",
							`"${_folded.trim().slice(0, 60)}" mentions ${tag} inside a writer instruction — not a page boundary (lesson_boundary_guard).`);
						it._boundaryDenied = _noteDeny ? "note" : "label";   // read by ContentConverter (denied_note)
						current?.items.push(it);
						closed = false;
						continue;
					}
				}

				// A PAGE REFERENCE INTO A LINKED DOCUMENT. A numbered
				// "[page 21]" typed straight after a document's name or link ("… Audiovisual Request Template RAP 2026.docx
				// [page 21]", GENO901 ×15) names a page OF THAT DOCUMENT, not a page of this module. Data
				// lesson_boundary_guard.reference_forms.doc_ref_pattern; env REFMARK_OFF.
				{
					const _lbg2 = DataService.Data.EmitTemplates.page_split?.lesson_boundary_guard;
					const _rf2 = _lbg2?.reference_forms;
					if (_lbg2 && _lbg2.enabled !== false && _rf2 && _rf2.enabled !== false && _rf2.doc_ref_pattern
						&& (_rf2.doc_ref_tags ?? ["page"]).includes(tag) && (it.parse?.numbers ?? []).length
						&& !(typeof process !== "undefined" && process.env && process.env[_rf2.env ?? "REFMARK_OFF"])) {
						let _pv = null;
						for (let q = i - 1; q >= 0; q--) {
							const x = items[q];
							if (x.type === "black" && !String(x.text ?? "").trim()) continue;
							_pv = x; break;
						}
						const _pt = _pv ? String(_pv.type === "black" ? _pv.text : (_pv.blackAfter ?? "")).replace(/[*_]+/g, "").trim() : "";
						if (_pt && new RegExp(_rf2.doc_ref_pattern, "i").test(_pt)) {
							run.AddNote("info", "PageSplitter",
								`"${String(it.parse?.folded ?? "").trim().slice(0, 40)}" follows a linked document's name — a page reference into that document, not a page boundary (lesson_boundary_guard.reference_forms).`);
							it._boundaryDenied = "docref";   // a fragment of the note before it, never its own Writers Note
							current?.items.push(it);
							closed = false;
							continue;
						}
					}
				}

				if (tag === "lesson" || tag === "page") {
					if (singleFile) {
						// AR-3: in-page section break only — keep the item so
						// the converter can render a section separation
						current.items.push(it);
						closed = false;
						continue;
					}
					// OVERVIEW-NUMBERED "[Lesson 0.0]" (as in module ENGJ403). Newer
					// Writers Templates number the module introduction as its own "lesson":
					// "[MODULE INTRODUCTION]" → "[Lesson 0.0]" → the introduction content.
					// Lesson number 0/0.0 IS the overview page's own number, so opening a
					// new page here would ship the overview EMPTY (all its body content moved
					// to a spurious "0.0.0" file) while the human keeps the introduction ON
					// the 0.0 page. When the current page is the overview and the writer's
					// lesson number matches the overview pattern, the marker is consumed and
					// the content simply continues on the overview.
					// Data: page_split.writer_lesson_numbers.overview_zero_pattern.
					// Env toggle: ZEROLESSON_OFF.
					const wlnCfg = DataService.Data.EmitTemplates.page_split?.writer_lesson_numbers;
					const wlnOn = wlnCfg && wlnCfg.enabled !== false;
					if (tag === "lesson" && wlnOn && current?.isOverview
						&& !(typeof process !== "undefined" && process.env && process.env.ZEROLESSON_OFF)
						&& it.parse.numbers.length
						&& new RegExp(wlnCfg.overview_zero_pattern ?? "^0(\\.0)?$")
							.test(String(it.parse.numbers[0]))) {
						run.AddNote("info", "PageSplitter",
							`[Lesson ${it.parse.numbers[0]}] is the overview's own number — the introduction stays on the 0.0 page (writer_lesson_numbers).`);
						closed = false;
						continue;
					}
					// THE DIVIDER-BANNER MERGE (as in ENGS404).
					//
					// A Writers Template house convention writes the lesson number
					// TWICE. The divider page between lessons carries "[End page]"
					// then an all-caps banner "[LESSON 1.0]"; the lesson proper
					// then opens with the titled "[Lesson 1.0] Elements of
					// narrative". Between the two sits ONLY the lesson-menu region
					// — the [Lesson Overview] marker and its black "We are
					// learning:" / "I can:" run.
					//
					// AR-2 below cannot merge them because that menu text makes
					// currentIsEmpty() false, so the banner would open a file of its
					// own (header + footer, no body) and the duplicate-label
					// relabeller would then renumber EVERY later lesson — one writer
					// convention cascading into the whole module's pagination.
					//
					// THE RULE: a [Lesson N] marker whose number equals the OPEN
					// lesson page's number does not open a new page when that page
					// has received no BODY content yet — it is the same lesson.
					// The open page keeps its identity and adopts whichever of
					// title/number the second marker supplies that it lacks.
					//
					// "Body content" = a table, or a tag whose directive is
					// ELEMENT / INTERACTIVE / CONTAINER_OPEN / INLINE. The menu
					// region's SECTION_MARKERs and black text deliberately do NOT
					// count: that material belongs to the same lesson page either
					// way. That distinction is what keeps the rule off the writers
					// who genuinely reuse a number across real content (CEDO501, HES1005,
					// AGH1006 and HIS1007 carry body items between their same-number pairs).
					// Data: page_split.lesson_boundary_guard.duplicate_number_merge.
					// Env toggle: LESSONDUP_OFF.
					// A bare [LESSON] (or one repeating the open lesson's number) or a [PAGE] after a
					// front-matter-only lesson page does not open a new page (front_matter_fold; env FRONTFOLD_OFF)
					if (frontMatterOnly() && ((tag === "page" && _ffMarkers.has("page"))
						|| (tag === "lesson" && _ffMarkers.has("bare lesson") && (!it.parse.numbers.length
							|| String(it.parse.numbers[0]).replace(/\.0+$/, "") === String(current.lessonNumber).replace(/\.0+$/, ""))))) {
						const _t = String(it.blackAfter || "").trim();
						if (!current.pageTitle && _t) current.pageTitle = _t;
						run.AddNote("info", "PageSplitter",
							`[${tag}] after a page holding only the lesson's front matter — the lesson continues on page ${current.lessonLabel}, no empty page emitted (front_matter_fold).`);
						closed = false;
						continue;
					}
					// A DOTTED SUB-lesson N.M (M ≥ 1) of the open lesson N ("[Lesson 1]" + "[Lesson Overview]" … then
					// "[LESSON 1.1] Timeliness", PWY1001) after a page holding only that lesson's front matter continues the
					// page and gives it the sub-lesson's number + title, as the gold's 1.1 carries that menu (no empty 1.0
					// page). The plain front-matter fold keeps precedence. Data
					// lesson_boundary_guard.front_matter_fold.dotted_sub_lesson; env FRONTFOLDDOT_OFF.
					if (tag === "lesson" && _ffOn && _ffCfg.dotted_sub_lesson === true
						&& !(typeof process !== "undefined" && process.env && process.env.FRONTFOLDDOT_OFF)
						&& current && !current.isOverview && current.lessonNumber !== null
						&& it.parse.numbers.length && /^\d+\.[1-9]\d*$/.test(String(it.parse.numbers[0]))
						&& String(it.parse.numbers[0]).split(".")[0] === String(current.lessonNumber).replace(/\.0+$/, "")
						&& frontMatterOnly()) {
						lessonOrdinal++;
						pageWithinLesson = 0;
						// the page keeps its lesson NUMBER; the label (N.M) and the title become the sub-lesson's, and it stays
						// the lesson's MENU SOURCE (ContentConverter's lesson_continuation_inherits registers a menu only on N.0)
						current.lessonLabel = String(it.parse.numbers[0]);
						current._lessonMenuSource = true;
						const _dt = String(it.blackAfter || "").trim() || (normaliser ? normaliser.RenderText(it.text) : "");
						if (_dt) current.pageTitle = _dt;
						run.AddNote("info", "PageSplitter",
							`[LESSON ${it.parse.numbers[0]}] after a page holding only its lesson's front matter — the page continues as ${current.lessonLabel}, no empty page emitted (front_matter_fold.dotted_sub_lesson).`);
						closed = false;
						continue;
					}
					if (tag === "lesson" && _lbgOn && _lbgCfg.duplicate_number_merge !== false
						&& !(typeof process !== "undefined" && process.env && process.env.LESSONDUP_OFF)
						&& current && !current.isOverview && current.lessonNumber !== null
						&& it.parse.numbers.length
						// Compare NUMERICALLY, not as strings: the divider banner
						// and the titled opener routinely spell the same lesson two
						// ways ("[LESSON 4.0]" then "[Lesson 4]", ENGS404 ×3). Only
						// a trailing ".0" is folded away, so "3.1" can never equal
						// "3" and a genuine sub-lesson still opens its own page.
						&& String(it.parse.numbers[0]).replace(/\.0+$/, "")
							=== String(current.lessonNumber).replace(/\.0+$/, "")
						&& !current.items.some((x) => x.type === "table"
							|| (x.type === "tag" && ["ELEMENT", "INTERACTIVE", "CONTAINER_OPEN", "INLINE"]
								.includes(x.parse.primary?.directive)))) {
						const _title = it.blackAfter.trim()
							|| (normaliser ? normaliser.RenderText(it.text) : "");
						if (!current.pageTitle && _title) current.pageTitle = _title;
						run.AddNote("info", "PageSplitter",
							`[Lesson ${it.parse.numbers[0]}] repeats the open lesson's number with no body content between — merged, no empty page emitted (lesson_boundary_guard).`);
						closed = false;
						continue;
					}

					// AR-2: adjacent boundary tags = one break (an unclosed
					// empty current page is REUSED, not duplicated)
					if (current && currentIsEmpty() && !current.isOverview) {
						run.AddNote("info", "PageSplitter",
							"Adjacent page boundaries merged — no empty page emitted (AR-2).");
						// The popped page's own ordinal bump is undone — a [PAGE] that opened lesson N followed at once by a
						// [LESSON] tag would otherwise number that lesson N+1 (CEDO301 2.0 … 6.0 for the gold's 1.0 …). Data
						// page_split.page_marker_as_lesson.ar2_restores_ordinal; env AR2ORD_OFF.
						if (current._prevOrdinal !== undefined && _pml?.ar2_restores_ordinal === true
							&& !(typeof process !== "undefined" && process.env && process.env.AR2ORD_OFF)) {
							lessonOrdinal = current._prevOrdinal;
						}
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
						// DOTTED WRITER LESSON NUMBERS (ENGJ403, the CED NCEA family,
						// XMES202). Newer Writers Templates number lessons ALREADY DOTTED
						// ("[Lesson 1.0]", "[Lesson 2.1]"); appending the usual ".0" would
						// produce "1.0.0"/"2.1.0" page labels + chips where the human ships
						// "1.0"/"2.1" (gold CEDO501/CEDT501/CEDK501 pages are the same
						// "2.1"-style). A dotted number is used VERBATIM as the label;
						// un-dotted "[Lesson 4]" keeps the ".0" suffix.
						// Data: page_split.writer_lesson_numbers.dotted_label_verbatim.
						// Env toggle: DOTLESSON_OFF.
						const dotVerbatim = wlnOn && wlnCfg.dotted_label_verbatim !== false
							&& !(typeof process !== "undefined" && process.env && process.env.DOTLESSON_OFF)
							&& String(num).includes(".");
						open({
							lessonNumber: num,
							lessonLabel: dotVerbatim ? String(num) : `${num}.0`,
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
							_prevOrdinal: lessonOrdinal - 1,   // AR-2 restores it when this page pops empty
						});
					} else if (_pmlOn && current
						// not when the tag itself names a dotted sub-lesson ("[page 3] Lesson 2.1", XTAS103)
						&& !new RegExp(_pml.deny_text_pattern ?? "\\b\\d+\\.\\d+\\b").test(`${it.text ?? ""} ${it.blackAfter ?? ""}`)
						// not when a [LESSON] tag opens the page next (BLL261 "[page 2]" → "[Lesson Two]", CEDO301) —
						// that tag opens the lesson itself and AR-2 folds the empty [PAGE] page away
						&& !(() => {
							for (let q = i + 1; q < items.length; q++) {
								const nx = items[q];
								if (nx.type === "black" && !String(nx.text ?? "").trim()) continue;
								return nx.type === "tag" && nx.parse?.primary?.directive === "PAGE_BOUNDARY"
									&& nx.parse.primary.tag === "lesson";
							}
							return false;
						})()
						&& (
						(_pml.after_implicit !== false && current.openedBy === "implicit")
						|| (_pml.writer_next_number !== false && pageWithinLesson === 0
							&& it.parse.numbers.length && /^\d+$/.test(String(it.parse.numbers[0]))
							&& /^\d+(?:\.0+)?$/.test(String(current.lessonNumber))
							&& parseInt(it.parse.numbers[0], 10) === parseInt(current.lessonNumber, 10) + 1))) {
						// THE WRITER'S [PAGE N] OPENS ITS OWN LESSON PAGE. The page-as-lesson rule above fires only
						// after the overview or another page-as-lesson; a [PAGE] after a lesson page opened
						// IMPLICITLY (content after [end page], no "Lesson N" heading — MXFL101 / 103, XGF9003,
						// BLL175) or carrying the NEXT lesson's number after [LESSON N-1] (ENGI101 "[LESSON 1]" →
						// "[Page 2]"; MXFL204 "[Lesson 3]" → "[page 4]") would otherwise fall to the sub-page branch
						// below, shipping x.1, x.2 … where the gold ships lesson N (MXFL103's gold runs 0.0 … 7.0).
						// An implicit page counts on sequentially (the writer's number is not trusted there —
						// MXFL101 writes "[page 1]" for its second lesson); the next-number form takes the writer's
						// number. Data page_split.page_marker_as_lesson; env PAGELESSON_OFF.
						lessonOrdinal = current.openedBy === "implicit"
							? lessonOrdinal + 1 : parseInt(it.parse.numbers[0], 10);
						pageWithinLesson = 0;
						open({
							lessonNumber: String(lessonOrdinal),
							lessonLabel: `${lessonOrdinal}.0`,
							pageTitle: "",
							wtPageStart: it.block.wtPage,
							openedBy: "page-as-lesson",
						});
						run.AddNote("info", "PageSplitter",
							`[PAGE] opens lesson page ${lessonOrdinal}.0, not a sub-page (page_marker_as_lesson).`);
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
				// TILE-LESSON CLOSERS (as in module ENGJ403 lesson 5). The writer's
				// "[end tile lesson navigate back to lesson 5]" closes a TILE
				// sub-structure INSIDE the lesson, not the page — but it parses as an
				// "end lesson" PAGE_BOUNDARY, so it would split lesson 5 into three files
				// where the human ships ONE 5.0 page. A closer whose own text matches the
				// tile pattern is consumed and the page simply continues. The form is
				// specific to ENGJ403.
				// Data: page_split.writer_lesson_numbers.tile_closer_pattern.
				// Env toggle: TILECLOSER_OFF.
				{
					const wln2 = DataService.Data.EmitTemplates.page_split?.writer_lesson_numbers;
					if (wln2 && wln2.enabled !== false && tag === "end lesson"
						&& !(typeof process !== "undefined" && process.env && process.env.TILECLOSER_OFF)
						&& new RegExp(wln2.tile_closer_pattern ?? "tile\\s+lesson|navigate back to lesson", "i")
							.test((it.parse?.folded ?? "").trim())) {
						run.AddNote("info", "PageSplitter",
							"Tile-lesson closer — an in-page tile structure, not a page boundary; the lesson page continues (writer_lesson_numbers).");
						closed = false;
						continue;
					}
				}
				// AN [END PAGE <TAB>] THAT NAMES THE OPEN SIDE TAB CLOSES THE TAB, NOT THE PAGE (EXIP901 / EXBP901's
				// "[End page intro]"): when more side-tab content follows before the next page boundary or stage marker, the
				// span becomes an [End of tab] closer and the page continues. Data page_split.side_tab_end_page; env SIDETABEND_OFF.
				if (_steOn && tag === "end page" && _openSideTab) {
					const _rest = (it.parse?.folded ?? "").trim().replace(/^\[\s*end\s+page\s*/i, "").replace(/\]\s*$/, "").trim().toLowerCase();
					if (_rest && (_rest === _openSideTab || _openSideTab.startsWith(_rest))) {
						let _tabFollows = false;
						for (let q = i + 1; q < Math.min(items.length, i + 1 + (_ste.lookahead ?? 400)); q++) {
							const x = items[q];
							const fx = String(x.type === "tag" ? (x.parse?.folded ?? "") : "").trim();
							if (x.type !== "tag") continue;
							if (_steCloseRe.test(fx) || (x.parse?.primary?.tag === "tab n" && _steOpenRe.test(fx))) { _tabFollows = true; break; }
							if (x.parse?.primary?.directive === "PAGE_BOUNDARY" || _steStageRes.some((re) => re.test(fx))) break;
						}
						if (_tabFollows) {
							const _closer = normaliser
								? { ...it, text: "\u{1f534}[RED TEXT] [End of tab] [/RED TEXT]\u{1f534}", parse: normaliser.Parse("[End of tab]") }
								: it;
							current?.items.push(_closer);
							run.AddNote("info", "PageSplitter",
								`"${(it.parse?.folded ?? "").trim()}" names the open side tab — it closes that tab, not the page (side_tab_end_page).`);
							_openSideTab = null;
							closed = false;
							continue;
						}
					}
				}
				// In a stage-dialect module an [end page] typed directly before the next tab opener closes the
				// open tab, not the page (EXBP901's Share It: "[End page]" → "[Next tab] Preparing for your showcase") — the
				// stage is the page. Data page_split.stage_opener_break.tab_end_page; env STAGEBREAK_OFF.
				if (_sobOn && _stageDialect && _sob.tab_end_page !== false && tag === "end page") {
					let q = i + 1;
					while (q < items.length && items[q].type === "black" && !String(items[q].text ?? "").trim()) q++;
					const nx = items[q];
					if (nx && nx.type === "tag" && nx.parse?.primary?.tag === "tab n" && nx.parse?.primary?.directive === "SUBTAG") {
						const _closer = normaliser
							? { ...it, text: "\u{1f534}[RED TEXT] [End of tab] [/RED TEXT]\u{1f534}", parse: normaliser.Parse("[End of tab]") }
							: it;
						current?.items.push(_closer);
						run.AddNote("info", "PageSplitter",
							`"${(it.parse?.folded ?? "").trim()}" directly before a tab opener closes the tab, not the page (stage_opener_break.tab_end_page).`);
						closed = false;
						continue;
					}
				}
				if (_ffMarkers.has("end page") && frontMatterOnly()) {
					// An [end page] closing a page that holds only the lesson's front matter is
					// disregarded: the lesson's content continues on it (front_matter_fold; env FRONTFOLD_OFF)
					run.AddNote("info", "PageSplitter",
						`[end page] after a page holding only the lesson's front matter disregarded — page ${current.lessonLabel} continues (front_matter_fold).`);
					continue;
				}
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

			// ---- a mid-page lesson heading / black [LESSON N] line opens its page ----
			if (!closed && _midOpeners.has(i) && current && (!current.isOverview || current._introMerged)) {
				const c = _midOpeners.get(i);
				if (c.n > lessonOrdinal) {
					// AR-2 FOR THE MID-PAGE OPENER. A "[New page]" typed right before "[H2] Lesson Five: …" (DAN1006) opens
					// sub-page 4.1, and this opener would then open 5.0 beside it, leaving 4.1 empty (the gold: 4.0 → 5.0). An
					// empty current page is reused, as the [LESSON] branch's AR-2 already does.
					// Data page_split.mid_page_lesson_heading.empty_page_merge; env MIDEMPTY_OFF.
					if (_mlh.empty_page_merge === true
						&& !(typeof process !== "undefined" && process.env && process.env.MIDEMPTY_OFF)
						&& currentIsEmpty() && !current.isOverview) {
						run.AddNote("info", "PageSplitter",
							`An empty page ${current.lessonLabel} before the mid-page lesson opener merged — no empty page emitted (AR-2).`);
						pages.pop();
						current = pages[pages.length - 1] ?? null;
					}
					lessonOrdinal = c.n;
					pageWithinLesson = 0;
					open({ lessonNumber: String(c.n), lessonLabel: `${c.n}.0`, pageTitle: c.title, wtPageStart: it.block?.wtPage });
					run.AddNote("info", "PageSplitter",
						`Mid-page lesson opener — "${c.consume ? String(it.text ?? "").trim() : "Lesson " + c.n + (c.title ? ": " + c.title : "")}" opened page ${c.n}.0 (page_split.mid_page_lesson_heading).`);
					if (c.consume) continue;
					current.items.push(it);
					continue;
				}
			}

			// ---- a level-first title marker on the overview opens the first level page ----
			// FRFUN06 types `[Title] [H1] [Novice Page 1] 1. The main vowel sounds` straight after its overview with no
			// [End page], so without this the level page (and its eight side tabs) would ride on the overview; every FRFUN
			// gold ships it as its own file. Only a registry row saying level_overview "multi-file" enters (the FRFUN row).
			if (_lvOvRe && current?.isOverview && !closed && it.type === "tag"
				&& _lvOvRe.test(String(it.block?.text ?? it.text ?? "").replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, ""))) {
				lessonOrdinal++;
				pageWithinLesson = 0;
				open({ lessonNumber: String(lessonOrdinal), lessonLabel: `${lessonOrdinal}.0`, pageTitle: "", wtPageStart: it.block?.wtPage });
				run.AddNote("info", "PageSplitter",
					`A level page marker on the overview opened page ${current.lessonLabel} (fundamentals_panels.level_overview.split_overview_at_marker).`);
				current.items.push(it);
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
				// open lessons with plain topic headings (a looser rule would
				// collapse MXEX401 to one page).
				if (current?.isOverview) {
					const INTRO_TAGS = new Set(["title bar", "module introduction", "supervisor note"]);
					let introNext = false;
					let choiceNext = false;
					// CHOICE-PAGE MERGE (the XDLS900 family). The human merges the
					// "[LESSON Choice page]" tile-navigation section INTO page 00 (every
					// gold ships 00 = introduction + the choice tiles, then one page per
					// lesson), so the writer's [end page] directly before the choice opener
					// is disregarded exactly like the introduction-cluster rule above. The
					// opener form belongs to XDLS902-906, which all follow this same
					// [End page] → [LESSON Choice page] shape.
					// Data: body_region.choice_page_tiles.merge_into_overview.
					// Env toggle: CHOICEMERGE_OFF (the choice section then gets its
					// own implicit "1.0" page).
					const _cpm = DataService.Data.EmitTemplates.body_region?.choice_page_tiles;
					const _cpmOn = _cpm && _cpm.enabled !== false && _cpm.merge_into_overview !== false
						&& !(typeof process !== "undefined" && process.env && process.env.CHOICEMERGE_OFF);
					// THE INTRODUCTION'S OTHER WRITER FORMS: a BLACK "**[MODULE INTRODUCTION]**" line (HIS1002,
					// ART1006, PES1005), the marker glued to another tag ("[MODULE INTRODUCTION] [insert image]"
					// GEO1004, MUS1004), a CS / unresolved instruction tag in front of it (ENGR102), and the heading
					// form ("[H2] Introduction", "[H1] **INTRODUCTION**", "[H3] **MODULE INTRODUCTION**" — CBI1009,
					// COM1005 / 1006, DAN1003 / 1004, MXDI101). The human keeps the introduction on 0.0 in every
					// one (its page 1 is lesson 1). Data page_split.intro_cluster_forms; env INTROFORM_OFF.
					const _icf = DataService.Data.EmitTemplates.page_split?.intro_cluster_forms;
					const _icfOn = !!_icf && _icf.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env[_icf.env ?? "INTROFORM_OFF"]);
					const _icfClean = (s) => String(s ?? "").replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
					for (let k = i; k < Math.min(i + 4, items.length); k++) {
						const peek = items[k];
						if (peek.type !== "tag") {
							if (_icfOn && peek.type === "black" && new RegExp(_icf.black_pattern, "i").test(_icfClean(peek.text))) { introNext = true; break; }
							continue;
						}
						// A red LABEL naming the introduction ("Splash Page - Intro", EXBP901 / EXIP901) is itself an
						// introduction-cluster marker (data intro_cluster_forms.label_form; env INTROLABEL_OFF)
						const _lf = _icf?.label_form;
						if (_icfOn && _lf && _lf.enabled !== false && _lf.pattern && !peek.parse?.primary?.tag
							&& !(typeof process !== "undefined" && process.env && process.env[_lf.env ?? "INTROLABEL_OFF"])
							&& new RegExp(_lf.pattern, "i").test(_icfClean(peek.text))) { introNext = true; break; }
						if (_icfOn && _icf.skip_unresolved_tags !== false
							&& (!peek.parse?.primary?.tag || peek.parse?.class === "instruction")) continue;
						introNext = INTRO_TAGS.has(peek.parse.primary?.tag)
							|| (_icfOn && new RegExp(_icf.embedded_pattern, "i").test(String(peek.text ?? "")))
							|| (_icfOn && (_icf.heading_tags ?? ["h1", "h2", "h3"]).includes(peek.parse.primary?.tag)
								&& new RegExp(_icf.heading_pattern, "i").test(_icfClean(peek.blackAfter || (peek.parse?.remainders ?? []).join(" "))));
						choiceNext = _cpmOn && new RegExp(_cpm.opener_pattern
							?? "^\\[\\s*lesson choice page\\s*\\]", "i")
							.test((peek.parse?.folded ?? "").trim());
						break;   // judge by the FIRST tag span only
					}
					if (introNext || choiceNext) {
						run.AddNote("info", "PageSplitter", choiceNext
							? "[end page] on the overview disregarded — the [LESSON Choice page] tile navigation stays on page 0.0 (choice_page_tiles.merge_into_overview)."
							: "[end page] on the overview disregarded — an introduction-cluster marker follows ([Title]/[Introduction]/[supervisor note]; AR-1 generalised).");
						// The overview holds a merged introduction: a lesson heading after it
						// (DAN1004's "[H1] Lesson One: …" with no [End page] between) opens its lesson page
						// (the mid-page opener, allowed on this overview only)
						if (_icfOn && introNext) current._introMerged = true;
						// The introduction's first item is marked, so the overview's menu / body boundary
						// (ContentConverter) can end the menu there for every form this rule recognises — not only the red
						// [MODULE INTRODUCTION] tag. Data intro_cluster_forms.menu_boundary; env INTROMENU_OFF.
						if (introNext && _icf?.menu_boundary === true
							&& !(typeof process !== "undefined" && process.env && process.env.INTROMENU_OFF)) it._introStart = true;
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
				// A black [LESSON N] / LESSON N marker line (a mid-page opener candidate) as the first item after an
				// [end page] is consumed, as the mid-page opener consumes it (otherwise GEO1006 2.0 / 3.0 would show a red
				// "Writers Note: [LESSON 3]", MXS1004 a bare <p>LESSON 6</p>); the page keeps the running ordinal (MXS1004's
				// writer skips 3 and 8 — the gold numbers its pages in sequence). Data black_marker_any_case.implicit_break_consume.
				const _bm = (_bacRe && _bac.implicit_break_consume !== false && it.type === "black") ? _midOpeners.get(i) : null;
				const _bmN = _bm && _bm.consume ? _bm.n : null;
				// KB 01D «explicit numbers preserved»: inside a lesson page N whose writer still has an explicit
				// [LESSON N+1] ahead, the implied page is lesson N's CONTINUATION — sub-page N.k, the gold's form
				// (CEDR501 1.1 «Roles») — not lesson N+1, which would collide with the writer's [LESSON N+1] and
				// shift every later lesson by one (the «Duplicate lesson label … relabelled» cascade). It keeps the
				// lesson's number, so it inherits the lesson's menu.
				// The NEXT [LESSON] tag must be exactly [LESSON N+1] (a writer who reuses a number — HES1005's second
				// [LESSON 3] — or a bare / dotted tag keeps the running ordinal).
				// A segment holding only the NEXT lesson's front matter (its [Lesson Overview] typed before its own
				// [LESSON N+1] tag — as in OSGM401) belongs to that lesson: the running-ordinal page + the front-matter fold keep it.
				const _curN = current && !current.isOverview ? String(current.lessonNumber ?? "") : "";
				const _nextLesson = _ibsOn ? _explicitLessonAt.find((e) => e.k > i) : null;
				const _segFrontMatter = (from, to) => {
					let heads = 0;
					for (let q = from; q < to; q++) {
						const x = items[q];
						if (x.type === "black") { if (_ffLines(x.text).every(_ffLine)) continue; return false; }
						if (x.type !== "tag") return false;
						const p = x.parse?.primary;
						if (!p || p.directive === "SECTION_MARKER") continue;
						if (/^h[1-6]$/.test(p.tag) || p.tag === "heading") { if (++heads > 2) return false; continue; }
						if ((p.tag === "body" || p.tag === "sub head") && _ffLines(x.blackAfter).every(_ffLine)) continue;
						return false;
					}
					return true;
				};
				if (!lm && _bmN == null && _ibsOn && /^\d+$/.test(_curN) && _nextLesson && _nextLesson.n === parseInt(_curN, 10) + 1
					&& !_segFrontMatter(i, _nextLesson.k)) {
					pageWithinLesson++;
					open({
						lessonNumber: _curN,
						lessonLabel: `${_curN}.${pageWithinLesson}`,
						pageTitle: "",
						wtPageStart: it.block.wtPage,
						openedBy: "implicit-sub",
					});
					run.AddNote("info", "PageSplitter",
						`Implicit page break inside lesson ${_curN} — the writer's [LESSON ${parseInt(_curN, 10) + 1}] is still to come, so the page is its continuation ${current.lessonLabel} (implicit_break_sub_page, KB 01D).`);
					closed = false;
					current.items.push(it);
					continue;
				}
				lessonOrdinal = lm ? parseInt(lm[1], 10) : lessonOrdinal + 1;
				pageWithinLesson = 0;
				open({
					lessonNumber: lm ? lm[1] : String(lessonOrdinal),
					// A dotted number from the opening "Lesson N.M:" heading is the label verbatim
					lessonLabel: (lm && _dhOn && String(lm[1]).includes(".")) ? String(lm[1]) : `${lm ? lm[1] : lessonOrdinal}.0`,
					pageTitle: lm ? lm[2].replace(/\**$/, "").trim() : "",
					wtPageStart: it.block.wtPage,
					// Marks the plain implicit page for page_marker_as_lesson
					...(_pmlOn && !lm ? { openedBy: "implicit" } : {}),
				});
				if (_bmN != null) {
					run.AddNote("info", "PageSplitter",
						`The writer's black "${String(it.text ?? "").trim()}" after [end page] opened page ${current.lessonLabel} — the marker line consumed (mid_page_lesson_heading.black_marker_any_case).`);
					closed = false;
					continue;
				}
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
			// The activity-table adapter: the adapted stream's pages carry the MODULE title as
			// their own — the gold's lesson h1 repeats the module title on every XOTP page — so the
			// heading harvest is skipped and the SkeletonBuilder fallback applies. Set by ModuleResolver
			// from `input_shapes.activity_table.adapter.page_title === "module"`; env ACTTABLEADAPT_OFF.
			if (run && run.pageTitleFromModule) continue;
			// KB c79 hygiene: a header title never carries a writer's
			// markdown marker. Strip every `*` from the [LESSON] payload BEFORE the label /
			// bare-number tests below (so `**3**` reads as the bare number it is and takes the
			// lesson's own name from its first heading) and collapse whitespace; a title left with
			// no letter or digit is emptied so the module-title fallback applies. Fires only on a
			// title that carries a `*`. Data body_region.lesson_title_dedup.title_markers;
			// env TITLEMARK_OFF.
			const _tmCfg = DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.title_markers;
			if (_tmCfg && _tmCfg.enabled !== false && p.pageTitle && /\*/.test(String(p.pageTitle))
				&& !(typeof process !== "undefined" && process.env && process.env[_tmCfg.env ?? "TITLEMARK_OFF"])) {
				const _t = String(p.pageTitle).replace(/\*/g, "").replace(/\s+/g, " ").trim();
				p.pageTitle = /[\p{L}\p{N}]/u.test(_t) ? _t : "";
			}
			// A heading tag typed in black at the head of the [LESSON] payload (MUS1004's "**[H1] Lesson One. …**")
			// is not part of the title (title_markers.tag_prefix; env TITLETAG_OFF)
			const _tpCfg = _tmCfg?.tag_prefix;
			if (_tpCfg && _tpCfg.enabled !== false && _tmCfg.enabled !== false && p.pageTitle
				&& !(typeof process !== "undefined" && process.env && process.env[_tpCfg.env ?? "TITLETAG_OFF"])) {
				const _tpRe = new RegExp(_tpCfg.pattern ?? "^\\s*\\[\\s*h[1-6]\\s*\\]\\s*", "i");
				const _raw = String(p.pageTitle);
				const _lead = _raw.replace(/^\s*\**\s*/, "");
				if (_tpRe.test(_lead)) p.pageTitle = _lead.replace(_tpRe, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
			}
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
			// KB constraint 79 (the `Lesson N` LABEL titles): a title that is nothing but a
			// lesson label ("Lesson One", "Lesson #3", "Lesson 5 continued") is no title — the first REAL
			// heading names the page (label-only headings skipped, the label stripped from a prefixed one).
			// Data body_region.lesson_title_dedup.lesson_label_titles; env LESSONLABEL_OFF.
			const _llCfg = DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.lesson_label_titles;
			const _llOn = !!_llCfg && _llCfg.enabled !== false && !!_llCfg.label_pattern
				&& !(typeof process !== "undefined" && process.env && process.env[_llCfg.env ?? "LESSONLABEL_OFF"]);
			const _llRe = _llOn ? new RegExp(_llCfg.label_pattern, "i") : null;
			const _llMatch = (s) => (_llRe ? _llRe.exec(String(s ?? "").replace(/\*/g, "").trim()) : null);
			const _labelOnly = (s) => { const m = _llMatch(s); return !!m && !String(m[3] ?? "").trim(); };
			const _stripLabel = (s) => { const m = _llMatch(s); const rest = m ? String(m[3] ?? "").trim() : ""; return rest || String(s ?? "").trim(); };
			let firstHeading = null;
			// KB c79: a heading whose words are typed INSIDE its red span ("🔴[H2] Missionaries and Māori🔴", ANZH304)
			// has no black text and no parse remainders, so the harvest would skip it and the module title stand in
			// as the lesson's h1 — while the body renders that very heading. Its embedded render text
			// (TagNormaliser.RenderText, the body's own source) names the page.
			// Data body_region.lesson_title_dedup.embedded_heading_title; env EMBHEADTITLE_OFF.
			const _ehCfg = DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.embedded_heading_title;
			const _ehOn = !!_ehCfg && _ehCfg.enabled !== false && !!normaliser
				&& !(typeof process !== "undefined" && process.env && process.env[_ehCfg.env ?? "EMBHEADTITLE_OFF"]);
			// KB c79: a remainder that sits inside the heading's own tag bracket (the level word of FRFUN07's red
			// `[Title] [H1] [Emergent Page 3] Change of shape`) never names the page when the writer typed the title in
			// the red span — the embedded words (below) win.
			// Data embedded_heading_title.bracket_remainder_yields; env BRACKETREM_OFF.
			const _bracketRem = (x) => {
				if (!_ehOn || _ehCfg.bracket_remainder_yields !== true
					|| (typeof process !== "undefined" && process.env && process.env[_ehCfg.bracket_remainder_env ?? "BRACKETREM_OFF"])) return false;
				const rem = (x.parse?.remainders ?? []).map((r) => String(r).toLowerCase().trim()).filter(Boolean);
				const frags = (x.parse?.tags ?? []).map((t) => String(t.fragment ?? "").toLowerCase());
				return rem.length > 0 && rem.every((r) => frags.some((f) => f.includes(r)));
			};
			const _embText = (x) => (_ehOn && !String(x.blackAfter ?? "").trim() && (!(x.parse?.remainders ?? []).length || _bracketRem(x))
				? String(normaliser.RenderText(String(x.text ?? "")) ?? "").replace(/\*/g, "").trim() : "");
			// the heading's own words: black text, else its remainders — unless they are bracket words and red words exist
			const _remText = (x) => ((_bracketRem(x) && _embText(x)) ? "" : (x.parse?.remainders ?? []).join(" "));
			let firstHeadingText = "";
			for (const it2 of p.items) {
				if (it2.type !== "tag") continue;
				const pt2 = it2.parse.primary?.tag;
				const ht2 = (it2.blackAfter || _remText(it2) || _embText(it2)).replace(/\*/g, "").trim();
				// a heading that is only a lesson label never names the page — keep scanning
				if (_llOn && ["h1", "h2", "h3", "h4", "h5", "heading"].includes(pt2) && ht2 && _labelOnly(ht2)) continue;
				if (_btaOn && pt2 === "activity" && !/^lesson\s+\d/i.test(ht2)) break;   // stop at 1st activity
				// The MTK title source: a reoTranslate page has no [Activity] tag to stop the harvest, so a
				// body [H3] ("Finished!") would become the page title; only the writer's [H1] title repetition
				// may name the page there — else the module titles (SkeletonBuilder). Data
				// header.mtk_titles.harvest_heading_tags; env MTKTITLES_OFF.
				const _mtk = DataService?.Data?.EmitTemplates?.header?.mtk_titles;
				const _mtkOn = _mtk && _mtk.enabled !== false && Array.isArray(_mtk.harvest_heading_tags)
					&& !(typeof process !== "undefined" && process.env && process.env[_mtk.env ?? "MTKTITLES_OFF"])
					&& new RegExp(_mtk.body_class ?? "reoTranslate", "i").test(String(run?.resolvedRules?.body_class || ""));
				const _hTags = _mtkOn ? _mtk.harvest_heading_tags : ["h1", "h2", "h3", "h4", "h5", "heading"];
				if (_hTags.includes(pt2)
					&& (it2.blackAfter.trim() || (it2.parse.remainders.length && !(_bracketRem(it2) && _embText(it2))))) { firstHeading = it2; break; }
				// The heading's words inside its red span (also past a bracket-word remainder)
				if (_hTags.includes(pt2) && _embText(it2)) { firstHeading = it2; firstHeadingText = _embText(it2); break; }
			}
			if (!firstHeading) continue;
			const text = (firstHeading.blackAfter || _remText(firstHeading) || firstHeadingText)
				.replace(/\*/g, "").trim();
			const lm = text.match(/^lesson\s+(\d+(?:\.\d+)?[a-z]?)\s*[:.\-–—]?\s*(.*)$/i);
			// FILLING IN A BARE-NUMBER PAGE TITLE FROM THE FIRST HEADING.
			//
			// Sometimes a "[LESSON] N" tag's ONLY payload is the digit itself
			// (e.g. just "1"), which would leave p.pageTitle set to that bare
			// number, and the header would literally show "1" as the lesson's
			// name instead of a real title like "Plot Structure". So a pageTitle
			// that is nothing but a bare lesson number/label is filled in from
			// the first heading exactly the same way as an empty one.
			// This has a knock-on benefit: once the real lesson name is in
			// the page header, the logic elsewhere (in ContentConverter) that
			// removes a repeated lesson-title heading from the page BODY can
			// recognise the match — so a duplicate body heading like
			// "[H2] Lesson 1: Plot Structure" gets correctly removed instead
			// of appearing twice on the page.
			// SAFE TO ALWAYS APPLY: the human-built lesson pages never use a
			// bare number as the visible header title.
			// Data flag: lesson_title_dedup.lesson_name_from_heading
			// Env toggle: LESSONNAME_OFF (leaves a bare-number title in place,
			// in which case the body heading is not de-duplicated either)
			const _lnCfg = (typeof DataService !== "undefined"
				&& DataService.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.lesson_name_from_heading);
			const _lnOn = (_lnCfg?.enabled !== false)
				&& !(typeof process !== "undefined" && process.env && process.env.LESSONNAME_OFF);
			const _bareNum = /^\s*\d+(?:\.\d+)?[a-z]?\s*$/i.test(String(p.pageTitle ?? "").trim());
			// The harvested heading loses its own label ("Lesson #3 Opening Doors…" → "Opening Doors…")
			const _newTitle = (_llOn ? _stripLabel(lm ? lm[2] : text) : (lm ? lm[2] : text)).trim();
			if (!p.pageTitle) p.pageTitle = _newTitle;
			else if (_lnOn && _bareNum && _newTitle) p.pageTitle = _newTitle;
			// A label-only title ("Lesson One") is replaced by the first real heading; a
			// label-prefixed one ("Lesson One – The Ode") keeps its own words
			else if (_llOn && _labelOnly(p.pageTitle) && !(_llMatch(p.pageTitle)?.[2]) && _newTitle && !_labelOnly(_newTitle)) p.pageTitle = _newTitle;   // a "continued" sub-page inherits instead (below)
			else if (_llOn && _llCfg.strip_existing_title !== false && _stripLabel(p.pageTitle) !== String(p.pageTitle).trim()) p.pageTitle = _stripLabel(p.pageTitle);
			if (lm && p.lessonNumber !== lm[1]) {
				// the writer's own heading number wins over our ordinal —
				// but a disagreement is worth a summary line
				if (p.lessonNumber && p.lessonNumber !== lm[1]) {
					run.AddNote("info", "PageSplitter",
						`Page ${p.lessonLabel}: heading says "Lesson ${lm[1]}" — using the heading's number.`);
				}
				p.lessonNumber = lm[1];
				// A DOTTED number read from a red-embedded heading ("Lesson 1.0: …", MXEO102 / MXFL104) is the
				// label verbatim (the dotted_label_verbatim rule), never "1.0.0" (embedded_heading_title.dotted_label_verbatim);
				// the same for a black heading's dotted number (page_split.writer_lesson_numbers
				// .dotted_heading_verbatim; env DOTHEAD_OFF)
				p.lessonLabel = (String(lm[1]).includes(".")
					&& ((firstHeadingText && _ehCfg?.dotted_label_verbatim !== false) || (!firstHeadingText && _dhOn)))
					? String(lm[1]) : `${lm[1]}.0`;
			}
		}

		// KB constraint 79: a page whose title is STILL only a lesson label after the harvest
		// (no heading of its own) — a sub-page (N.M, M > 0) inherits its parent lesson's title
		// (CEDT501 5.1 "Lesson 5 continued" → "Speaking up"); a label-PREFIXED title with no heading
		// still loses its label. Data lesson_title_dedup.lesson_label_titles; env LESSONLABEL_OFF.
		{
			const _llCfg = DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.lesson_label_titles;
			const _llOn = !!_llCfg && _llCfg.enabled !== false && !!_llCfg.label_pattern
				&& !(typeof process !== "undefined" && process.env && process.env[_llCfg.env ?? "LESSONLABEL_OFF"]);
			if (_llOn) {
				const _llRe = new RegExp(_llCfg.label_pattern, "i");
				const _m = (s) => _llRe.exec(String(s ?? "").replace(/\*/g, "").trim());
				const _only = (s) => { const m = _m(s); return !!m && !String(m[3] ?? "").trim(); };
				const _strip = (s) => { const m = _m(s); const r = m ? String(m[3] ?? "").trim() : ""; return r || String(s ?? "").trim(); };
				const _byLabel = new Map(pages.filter((q) => q.lessonLabel).map((q) => [String(q.lessonLabel), q]));
				for (const p of pages) {
					if (p.isOverview || !p.pageTitle) continue;
					if (_only(p.pageTitle)) {
						if (_llCfg.inherit_parent_on_subpage === false) continue;
						const lab = String(p.lessonLabel ?? "");
						const mm = /^(\d+)\.(\d+)$/.exec(lab);
						if (!mm || mm[2] === "0") continue;
						const parent = _byLabel.get(`${mm[1]}.0`);
						if (parent && parent.pageTitle && !_only(parent.pageTitle)) p.pageTitle = parent.pageTitle;
					} else if (_llCfg.strip_existing_title !== false && _strip(p.pageTitle) !== String(p.pageTitle).trim()) {
						p.pageTitle = _strip(p.pageTitle);
					}
				}
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
				if (run.noOverviewPage) {
					// A module that ships NO overview page (the
					// activity-table family: the writer's Overview row is the
					// lesson-page menu, and the gold's first file is 1_0). The
					// title-bar-only opening segment folds into lesson 1 AS A
					// LESSON page — its own label and chrome kept, the title-bar
					// item riding along so the header title still resolves
					// (PageAssembler reads pageProducts[0] when no overview exists).
					// Set only by the adapter path (Input_Doc_Rules
					// input_shapes.activity_table.adapter.no_overview_page); env
					// ACTTABLEADAPT_OFF turns it off with the rest of the adapter.
					run.AddNote("info", "PageSplitter",
						"Title-bar-only opening segment folded into lesson 1 as a lesson page — this module has no overview page.");
					pages[1].items = [...first.items, ...pages[1].items];
					pages.shift();
				} else {
					run.AddNote("warn", "PageSplitter",
						"Overview segment had headings only — merged forward into the first lesson page (RR-4).");
					pages[1].items = [...first.items, ...pages[1].items];
					pages[1].isOverview = true;
					pages[1].lessonLabel = first.lessonLabel ?? pages[1].lessonLabel;
					pages.shift();
				}
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
		// Every page of a stage-dialect module carries the flag ContentConverter's template_fallback.stage_dialect reads.
		// An overview whose writer typed the introduction BEFORE an empty [TITLE BAR] + the overview section: the
		// overview block moves ahead of the introduction (the Writers Template's own order — overview, then [MODULE INTRODUCTION]),
		// and the payload-less title bar is dropped (page_split_rules.empty_titlebar_inpage; env EMPTYTB_OFF)
		for (const p of pages) {
			if (p._etbAt == null) continue;
			const im = p.items.findIndex((x, k) => k < p._etbAt && x.type === "tag" && x.parse?.primary?.tag === "module introduction");
			if (im < 0) continue;
			p.items = [...p.items.slice(0, im), ...p.items.slice(p._etbAt + 1), ...p.items.slice(im, p._etbAt)];
			run.AddNote("info", "PageSplitter",
				"The overview block the empty [TITLE BAR] heads moved ahead of the introduction typed before it (page_split_rules.empty_titlebar_inpage).");
		}
		// (and each tab opener on them `_stageOpener` — InteractiveScanner's capture stop reads it)
		if (_stageDialect) for (const p of pages) {
			p._stageDialect = true;
			for (const x of p.items) if (x.type === "tag" && x.parse?.primary?.tag === "tab n" && x.parse?.primary?.directive === "SUBTAG") x._stageOpener = true;
		}

		return pages;
	};
}

// Node export hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { PageSplitter };
