/**
 * ContentConverter.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Pipeline stage [6] — THE CORE. Walks one page's item stream and emits its
 * body HTML: every non-interactive tag becomes its correct element, writer
 * instructions become visible red flags, interactive ranges (already marked
 * by InteractiveScanner) become one distinct un-built placeholder each, and
 * the overview/lesson menu content is split out for the skeleton.
 *
 * HOW IT IS ORGANISED (mirrors Tag_Interpretation_Rules.md Part 7):
 *  - ONE dispatcher keyed by directive class — eight outcomes cover ~70 tags
 *  - ONE instruction emitter (NotesAndComments.redFlag) — the only place the RED FLAG form
 *    is produced (changing it later is one data edit in Emit_Templates)
 *  - per-family behaviour comes from Emit_Templates.json, never from
 *    per-module branches. If you are about to write
 *    `if (moduleCode === …)` here — STOP. That knowledge belongs in data.
 *
 * WHAT IT RETURNS (per page):
 *  { bodyHtml, menu: {kind:"tabs",tab1,tab2} | {kind:"simplified",content}
 *    | {kind:"none"} , titleBar: {english, teReo} }
 *
 * CONTENT-LOCATION MODEL (Part 3 of the rules — one rule, four cases):
 * try the bracket's embedded payload, then the following black text; a
 * marker may legitimately have neither. MediaBuilder.gatherFollowing implements the
 * "following black text up to the next marker" capture.
 * ===========================================================================
 */

class ContentConverter {

	// the matcher for the current ConvertPage call — used by RenderText
	// lookups (original-case embedded titles; §1.2: never fold render text)
	static #norm = null;
	// the current page's English title — lets a mid-doc [Title] that merely
	// repeats the module name be consumed instead of duplicated as a body
	// heading (the human gold standard never repeats it; verified BLL146-0.0)
	static #pageEnglishTitle = "";
	// The RAW [TITLE BAR] payload BEFORE any prefix-stripping, e.g. "Module 2 - oe, ow, …".
	// Some modules (the BLL phonics family) put a "Module N - " prefix in front of the real
	// title, and #pageEnglishTitle above has already had that prefix stripped off. If a later
	// [Title]-style alias in the body repeats the title, it needs to be recognised as a repeat
	// of EITHER the stripped OR the un-stripped wording — otherwise a duplicate heading like
	// "<h3>Module 2 - oe…</h3>" would leak into the page body (seen on module BLL232).
	static #pageRawTitle = "";
	// the current LESSON page's title (from page.pageTitle, harvested by
	// PageSplitter into the header <h1>). The FIRST body heading that repeats
	// it is consumed — the human shows the lesson title ONCE, in the header
	// (measured: 723 human lesson pages do NOT repeat it in the body vs 35 that
	// do). Without this the same "[H2] Lesson N: <title>" rendered TWICE
	// (header h1 + body h3) on 683/887 Claude lesson pages.
	static #pageLessonTitle = "";
	static #firstBodyHeadingSeen = false;
	// The current lesson page's number (set from PageSplitter's page.lessonNumber) plus a
	// per-lesson activity-letter counter, used together to build "{lessonNumber}{letter}"
	// activity numbers such as "3A", "3B" (see data activity_wrapper.lesson_letter_number).
	// #lessonLetterMap is keyed BY lessonNumber so the lettering CONTINUES correctly across
	// several sub-pages that belong to the same lesson (A, B on page one, then C, D on page
	// two of the same lesson) instead of restarting at A on every page. #lettersModule tracks
	// which module was last lettered, so the whole map resets whenever a new module starts.
	static #pageLessonNumber = null;
	static #lessonLetterMap = {};
	static #lettersModule = null;

	/**
	 * Looks up the "accordion delimiter" registry row for this module, or returns null
	 * when this module isn't in the registry.
	 *
	 * WHAT THIS IS FOR:
	 * A few modules author their page's "phases" as a single accordion widget with
	 * numbered sections ([Accordion 1], [Accordion 2] …) instead of any of the other
	 * phase-marking conventions handled elsewhere in this file. Before those numbered
	 * accordion sections can be treated as phase boundaries, we need to confirm that THIS
	 * particular module is actually meant to be read that way — that's what this registry
	 * row confirms.
	 *
	 * HOW THE LOOKUP WORKS (the same lookup shape used by several other per-module
	 * registries in this codebase): try an exact override for this specific module code
	 * first (`registry.series`); if there isn't one, fall back to a group keyed by
	 * "SUBJECT|template_phase" — the subject-code prefix of the module code, combined with
	 * its template phase (normalised through skeleton.template_attr_map so phases that mean
	 * the same thing but are labelled differently still line up).
	 *
	 * WHY IT'S SHARED: this exact same registry row is also read independently, elsewhere
	 * in the engine, by InteractiveScanner (to decide whether it should suppress its normal
	 * accordion-bundling behaviour on this page) and by PanelsBuilder (to decide which
	 * nav/tile layout to build). Both of those other files read the ONE data row defined
	 * here, so the "is this module in accordion-as-phases mode?" decision can never
	 * disagree between them.
	 *
	 * @param {Object} acc - the accordion_delimiter config block from Emit_Templates.json
	 * @param {ConversionRun} run - the current run (reads run.resolvedRules, run.moduleCode)
	 * @returns {Object|null} the matching registry row, or null when this module isn't in it
	 */
	static #accordionPhaseRow(acc, run) {
		if (!/(^|\s)fundamentals(\s|$)/.test(run?.resolvedRules?.body_class || "")) return null;
		if (run?.resolvedRules?.page_model !== "single-file") return null;
		const reg = acc.registry || {};
		if (reg.series && reg.series[run?.moduleCode]) return reg.series[run.moduleCode];
		const subj = (run?.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const rawPhase = run?.resolvedRules?.template_phase ?? "";
		const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
		const lk = `${subj}|${phase}`.toLowerCase();
		const hit = Object.keys(reg.groups || {}).find((k) => k.toLowerCase() === lk);
		return hit ? reg.groups[hit] : null;
	};

	/**
	 * LEVEL-PAGE FUNDAMENTALS PRE-PASS (ROUND 265 — the CHFUN "[PAGE N Novice]"
	 * dialect, module CHFUN01).
	 *
	 * The Languages Fundamentals family writes ONE single-file module as a
	 * sequence of "[PAGE N <Level>]" sections, grouped by named proficiency
	 * LEVEL (Novice, Emergent, …). The human-built page turns that into the
	 * standard fundamentals phase chrome, with the LEVELS as the phases:
	 *   - each LEVEL becomes ONE fundamentalsPanel holding ALL of its pages
	 *     (a phasebreak fires only when the level CHANGES);
	 *   - every page keeps its own title (the marker's trailing text) as a
	 *     section heading inside the panel — synthesized here as a writer-level
	 *     [H1] item so the ordinary re-levelling machinery ranks it at the top
	 *     of the page outline (h3), pushing the writer's [H2] section headings
	 *     down to h4 exactly as the human ships them;
	 *   - each page's "[Page Overview]" learning-intentions block (a bare
	 *     "We are learning:" + bullets + "I can:" + bullets run) is captured
	 *     and AGGREGATED BY LEVEL into the module menu's per-level tab panes;
	 *   - the module's own [Overview] section: its [H3]-labelled LI/SC blocks
	 *     go to the menu's Overview pane, its introduction prose STAYS in the
	 *     body (it becomes the .introduction content), and the bare [Overview]
	 *     marker itself renders nothing;
	 *   - the "[Page content]" marker and the "[End of <X> Content]" /
	 *     "[Start of <X>]" level separators are structural no-ops, consumed.
	 *
	 * Registry-gated (level_pages.registry — the CHFUN|combo group) AND
	 * single-file page model, so no other module family can enter this path;
	 * the "[page N]"-style markers used by the CED/XDLS families never match
	 * the marker pattern (it requires a LEVEL WORD after the digit).
	 *
	 * @param {Object[]} bodyItems - the page's body items (mutated in place)
	 * @param {ConversionRun} run - the conversion run (gains run._levelMenu)
	 * @param {boolean} fundPanelMode - fundamentals mode is on for this page
	 * @param {boolean} singleFilePage - registry page_model is "single-file"
	 * @returns {{labels: string[], row: Object}|null} the level labels (in
	 *   first-seen order) + the matched registry row, or null when the dialect
	 *   does not apply
	 *
	 * Data: body_region.fundamentals_panels.level_pages.
	 * Env toggle: LEVELPAGE_OFF (reverts the whole dialect).
	 */
	static #levelPagesPrepass(bodyItems, run, fundPanelMode, singleFilePage) {
		const cfg = DataService.Data.EmitTemplates.body_region.fundamentals_panels?.level_pages;
		if (!cfg || cfg.enabled === false || !fundPanelMode || !singleFilePage) return null;
		if (typeof process !== "undefined" && process.env && process.env.LEVELPAGE_OFF) return null;
		// registry row: this module's series override → its subject|template_phase group
		const reg = cfg.registry || {};
		let row = reg.series?.[run?.moduleCode] ?? null;
		if (!row) {
			const subj = (run?.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
			const rawPhase = run?.resolvedRules?.template_phase ?? "";
			const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
			const lk = `${subj}|${phase}`.toLowerCase();
			const hit = Object.keys(reg.groups || {}).find((k) => k.toLowerCase() === lk);
			row = hit ? reg.groups[hit] : null;
		}
		if (!row) return null;
		const folded = (it) => (it.parse?.folded ?? "").trim();
		const markerRe = new RegExp(cfg.marker_pattern || "^\\[page \\d+ \\p{L}+\\]$", "iu");
		const isMarker = (it) => it.type === "tag" && it.consumedBy === undefined
			&& it.parse?.primary?.directive === "PAGE_BOUNDARY" && it.parse?.primary?.tag === "page"
			&& markerRe.test(folded(it));
		if (bodyItems.filter(isMarker).length < (cfg.min_markers ?? 2)) return null;

		const pageContentRe = new RegExp(cfg.page_content_pattern || "^\\[page content\\]$", "i");
		const pageOvRe = new RegExp(cfg.page_overview_pattern || "^\\[page overview\\]$", "i");
		const ovAliasRe = new RegExp(cfg.overview_alias_pattern || "^\\[overview\\]$", "i");
		const noopRes = (cfg.noop_patterns || ["^\\[end of [^\\]]+ content\\]$", "^\\[start of [^\\]]+\\]$"])
			.map((r) => new RegExp(r, "i"));
		const liHeadRe = new RegExp(cfg.menu_li_heading_pattern || "learning intention", "i");
		const scHeadRe = new RegExp(cfg.menu_sc_heading_pattern || "how will i know|success criteria", "i");
		const stripRed = (s) => String(s || "").replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "");

		const moduleMenu = { li: null, sc: null };
		const menuLevels = [];
		const levelIdx = new Map();
		let curLevel = null;
		const out = [];
		for (let i = 0; i < bodyItems.length; i++) {
			const it = bodyItems[i];
			// ---- "[PAGE N <Level>]" — a level page opens ------------------
			if (isMarker(it)) {
				// original-case level word from the raw block text (folded is lowercased)
				const raw = stripRed(String(it.block?.text ?? it.text ?? ""));
				const m = raw.match(/\[\s*page\s+\d+\s+([^\]]+?)\s*\]/i);
				const label = (m ? m[1] : "").replace(/\s+/g, " ").trim() || `Phase ${menuLevels.length + 1}`;
				const key = label.toLowerCase();
				if (!levelIdx.has(key)) {
					levelIdx.set(key, menuLevels.length);
					menuLevels.push({ label, li: { lead: "", bullets: [] }, sc: { lead: "", bullets: [] } });
					out.push({ type: "phasebreak" });
				}
				curLevel = levelIdx.get(key);
				// the marker's trailing text is the page's own section title —
				// synthesized as a writer-level heading so #relevelHeadings ranks
				// it at the top of the outline (data: title_writer_level)
				const title = String(it.blackAfter || "").trim();
				if (title) {
					const wl = cfg.title_writer_level ?? 1;
					out.push({ type: "tag", text: `[H${wl}]`, parse: this.#norm.Parse(`[H${wl}] `),
						blackAfter: title, block: it.block });
				}
				continue;
			}
			if (it.type === "tag" && it.consumedBy === undefined) {
				const f = folded(it);
				// ---- "[Page content]" + level separators — structural no-ops -
				if (pageContentRe.test(f) || noopRes.some((re) => re.test(f))) {
					if ((it.blackAfter || "").trim()) out.push({ type: "black", text: it.blackAfter, block: it.block });
					continue;
				}
				// ---- "[Page Overview]" — capture the LI/SC run BY LEVEL ------
				if (curLevel !== null && pageOvRe.test(f)) {
					const lines = [];
					if ((it.blackAfter || "").trim()) lines.push(...String(it.blackAfter).split("\n"));
					let j = i + 1;
					while (j < bodyItems.length && bodyItems[j].type === "black"
						&& bodyItems[j].consumedBy === undefined) {
						lines.push(...String(bodyItems[j].text || "").split("\n"));
						j++;
					}
					i = j - 1;
					this.#levelMenuAbsorb(menuLevels[curLevel], lines, cfg);
					continue;
				}
				// ---- the module's [Title] alias → the introduction heading ----
				// (synthesized at the same writer level as the page titles, so
				// the re-leveller ranks it h3 alongside them — the human's form)
				if (curLevel === null && it.parse?.primary?.tag === "title bar"
					&& new RegExp(cfg.title_alias_pattern || "^\\[title\\]$", "i").test(f)
					&& (it.blackAfter || "").trim()) {
					const wl = cfg.title_writer_level ?? 1;
					out.push({ type: "tag", text: `[H${wl}]`, parse: this.#norm.Parse(`[H${wl}] `),
						blackAfter: it.blackAfter, block: it.block });
					continue;
				}
				// ---- the module's own [Overview] marker — renders nothing ----
				if (curLevel === null && it.parse?.primary?.tag === "title bar" && ovAliasRe.test(f)) {
					if ((it.blackAfter || "").trim()) out.push({ type: "black", text: it.blackAfter, block: it.block });
					continue;
				}
				// ---- module-overview [H3]-labelled LI/SC block → menu --------
				if (curLevel === null && /^h[1-6]$/.test(it.parse?.primary?.tag || "")
					&& (liHeadRe.test(Utils.Fold(it.blackAfter || "")) || scHeadRe.test(Utils.Fold(it.blackAfter || "")))) {
					const side = liHeadRe.test(Utils.Fold(it.blackAfter || "")) ? "li" : "sc";
					const label = String(it.blackAfter || "").replace(/\*+/g, "").trim();
					const lines = [];
					let j = i + 1;
					if (j < bodyItems.length && bodyItems[j].type === "tag"
						&& bodyItems[j].consumedBy === undefined
						&& bodyItems[j].parse?.primary?.tag === "body") {
						if ((bodyItems[j].blackAfter || "").trim()) lines.push(...String(bodyItems[j].blackAfter).split("\n"));
						j++;
					}
					while (j < bodyItems.length && bodyItems[j].type === "black"
						&& bodyItems[j].consumedBy === undefined) {
						lines.push(...String(bodyItems[j].text || "").split("\n"));
						j++;
					}
					i = j - 1;
					const bucket = { label, lead: "", bullets: [] };
					this.#levelMenuLines(bucket, lines, cfg);
					moduleMenu[side] = bucket;
					continue;
				}
			}
			out.push(it);
		}
		bodyItems.splice(0, bodyItems.length, ...out);
		run._levelMenu = { module: moduleMenu, levels: menuLevels, row, cfg };
		run.AddNote("info", "ContentConverter",
			`Level-page fundamentals dialect: ${menuLevels.length} levels (${menuLevels.map((l) => l.label).join(", ")}) — panels grouped by level, [Page Overview] blocks routed to the module menu (fundamentals_panels.level_pages).`);
		return { labels: menuLevels.map((l) => l.label), row };
	};

	/**
	 * Absorbs one "[Page Overview]" run of lines into a LEVEL's menu bucket:
	 * the run splits at the SC lead line ("I can:" …) into the LI side and the
	 * SC side; each side's first non-bullet line becomes the lead (kept only
	 * from the FIRST page of the level), and its bullet lines append to the
	 * level's aggregated bullet list. (Part of the ROUND 265 level-pages
	 * dialect above.)
	 *
	 * @param {Object} level - the level bucket { label, li: {lead, bullets},
	 *   sc: {lead, bullets} }
	 * @param {string[]} lines - the captured raw lines
	 * @param {Object} cfg - the level_pages config block
	 */
	static #levelMenuAbsorb(level, lines, cfg) {
		const scLeadRe = new RegExp(cfg.sc_lead_pattern || "^i can\\b", "i");
		const liLeadRe = new RegExp(cfg.li_lead_pattern || "^we (are|'re) learning", "i");
		const liLines = [], scLines = [];
		let side = liLines;
		for (const ln of lines) {
			const t = ln.trim();
			if (!t) continue;
			if (side === liLines && scLeadRe.test(t.replace(/^[•◦▪\-\s]+/, ""))) side = scLines;
			side.push(t);
		}
		const absorb = (bucket, ls, leadRe) => {
			for (const t of ls) {
				const bare = t.replace(/^[•◦▪]\s*/, "");
				if (bare !== t || /^[-–]\s/.test(t)) bucket.bullets.push(this.#levelBullet(bare));
				else if (!bucket.lead) bucket.lead = bare;
				// a LATER page of the same level repeats the lead line ("We are
				// learning:" …) — the human's aggregated pane keeps ONE lead and
				// lists all the bullets under it, so a repeat is simply dropped
				else if (leadRe.test(bare)) continue;
				else bucket.bullets.push(this.#levelBullet(bare));
			}
		};
		absorb(level.li, liLines, liLeadRe);
		absorb(level.sc, scLines, scLeadRe);
	};

	/**
	 * Fills one module-overview menu bucket from its captured lines (the
	 * [Body] lead + bullet run under an [H3] LI/SC label). (Part of the
	 * ROUND 265 level-pages dialect above.)
	 *
	 * @param {Object} bucket - { label, lead, bullets }
	 * @param {string[]} lines - the captured raw lines
	 * @param {Object} cfg - the level_pages config block
	 */
	static #levelMenuLines(bucket, lines, cfg) {
		for (const ln of lines) {
			const t = ln.trim();
			if (!t) continue;
			const bare = t.replace(/^[•◦▪]\s*/, "");
			if (bare !== t) bucket.bullets.push(this.#levelBullet(bare));
			else if (!bucket.lead) bucket.lead = bare;
			else bucket.bullets.push(this.#levelBullet(bare));
		}
	};

	/**
	 * Normalises one menu bullet: markdown-bold markers stripped, a single
	 * trailing comma dropped (the human's panes list bullets bare, with only
	 * the final one keeping its full stop). (Part of the ROUND 265
	 * level-pages dialect above.)
	 *
	 * @param {string} s - the raw bullet text
	 * @returns {string}
	 */
	static #levelBullet(s) {
		return String(s || "").replace(/\*+/g, "").trim().replace(/,$/, "");
	};

	/**
	 * Converts one page.
	 *
	 * @param {Object} page - PageSplitter page (items carry parse results +
	 *                        consumedBy marks from InteractiveScanner)
	 * @param {Object[]} bundles - this page's interactive bundles
	 * @param {ConversionRun} run - rules, tallies, notes
	 * @param {TagNormaliser} normaliser - for original-case embedded text
	 * @returns {Object} { bodyHtml, menu, titleBar }
	 */
	static ConvertPage(page, bundles, run, normaliser) {
		this.#norm = normaliser;
		const tpl = DataService.Data.EmitTemplates;
		const menuType = MenuBuilder.menuTypeFor(page, run);

		// ---- split the stream: what feeds the MENU vs the BODY -----------
		const { titleBar, menuItems, bodyItems } =
			this.#partitionItems(page, menuType, run);
		this.#pageEnglishTitle = titleBar.english || run.englishTitle || "";
		this.#pageRawTitle = titleBar.rawEnglish || "";   // the full title before prefix-stripping
		// LESSON-TITLE DE-DUP: the title that PageSplitter already promoted up into the page
		// header's <h1> (page.pageTitle) must not ALSO show up a second time as the very
		// first heading inside the body — that would repeat the same words twice on the page.
		//
		// The OVERVIEW page used to be left out of this de-dup entirely (its lessonTitle was
		// forced to an empty string), which meant a module's own [MODULE INTRODUCTION] [H1]
		// heading — which usually just repeats the module's title — leaked through as a
		// redundant heading in the body (seen on module ENGC102, where the title "Keeping it
		// real" appeared twice). The overview page DOES have a title of its own — the
		// module's English title, shown in the page header — so the first body heading is now
		// de-duped against THAT, the exact same way a lesson page de-dups against its own
		// lesson title. The match must be EXACT (not a partial/fuzzy match): measured against
		// real human-built modules, an exact match is dropped 100% of the time, so this can
		// never accidentally strip a heading that only happens to look similar.
		// Data flag: body_region.lesson_title_dedup.overview   Env toggle: OVDEDUP_OFF
		const _ovDedupOn = (tpl.body_region?.lesson_title_dedup?.overview?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.OVDEDUP_OFF);
		this.#pageLessonTitle = page.isOverview
			? (_ovDedupOn ? this.#pageEnglishTitle : "")
			: (page.pageTitle || "");
		this.#firstBodyHeadingSeen = false;
		// LESSON-LETTER ACTIVITY NUMBERING CONTEXT: lessonNumber stays null on the overview
		// page (there is no "{lessonNumber}{letter}" activity renumbering there). The
		// per-lesson letter counter is reset whenever the module changes; WITHIN one module it
		// persists across pages, so a lesson that is split over several sub-pages keeps
		// counting its letters onward (A, B on the first sub-page, then C, D on the next)
		// instead of restarting at A each time.
		this.#pageLessonNumber = page.isOverview ? null : (page.lessonNumber ?? null);
		if (this.#lettersModule !== run.moduleCode) {
			this.#lettersModule = run.moduleCode;
			this.#lessonLetterMap = {};
		}

		// coalesce runs of consecutive black items (each docx paragraph is
		// its own block, so a bullet list arrives as N separate items —
		// joining them lets the list builder group "• …" lines into ONE
		// <ul> instead of N single-item lists)
		ListsAndRuns.coalesceBlackRuns(menuItems);
		ListsAndRuns.coalesceBlackRuns(bodyItems);

		// ---- body --------------------------------------------------------
		// THE ROW MANAGER — one structure per row, the dominant gold-standard
		// convention (51% of all human rows hold exactly one direct child,
		// measured across 2,045 pages; Emit_Templates body_region.row_rule).
		// The one grouping exception: a heading keeps its immediately-
		// following text run in the same row. Inside an open container or
		// activity, no row breaks ever happen.
		const rowCfg = tpl.body_region.row_breaks;
		const parts = [];
		let rowOpen = false;
		// FUNDAMENTALS PANELS: the "Fundamentals" family of modules present their content as a
		// set of numbered "phase" panels rather than one continuous scroll. The HPFUN subject
		// group marks where each phase begins with a writer tag "[New tab]" — if nothing
		// special were done with it, that tag would otherwise be left over as an orphaned
		// "[tab n]" red-flag warning in the output, because nothing else knows what to do with
		// it. In fundamentals mode we instead DROP that warning and push an internal
		// {sentinel} marker into the item stream at every "[New tab]"; a later post-processing
		// step, PanelsBuilder.fundamentalsPanels, reads those sentinels and wraps the relevant
		// stretches of body content into "div.fundamentalsPanel" blocks. This whole mechanism
		// is automatically scoped to modules that actually use the [New tab] family of markers
		// — subject groups like SSFUN/XFUN that don't use it are completely unaffected (the
		// sentinel is simply never inserted).
		// Data flag: body_region.fundamentals_panels   Env toggle: FUNDPANEL_OFF
		const fundCfg = tpl.body_region.fundamentals_panels;
		const fundPanelMode = !!fundCfg && fundCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FUNDPANEL_OFF)
			&& /(^|\s)fundamentals(\s|$)/.test(run.resolvedRules?.body_class || "");
		// BILINGUAL "reoTranslate" MODE: a reoTranslate module writes its content as
		// English|Māori side-by-side tables in the Writers Template; this mode "unfolds" those
		// tables into interleaved same-language chunks in the output — a Māori paragraph
		// tagged <... reo> immediately followed by its English counterpart tagged <... eng> —
		// instead of leaving them stuck together as a raw two-column table.
		// Data flag: elements.dual_language   Env toggle: REOTRANSLATE_OFF (reverts to the
		// non-bilingual rendering, useful for comparing the two output shapes side by side)
		const dlCfg = tpl.elements?.dual_language;
		// THE "MTK HOUSE HEADER" IS NOT, BY ITSELF, PROOF OF A BILINGUAL MODULE (see
		// PageSplitter for the full story): almost every Writers Template — bilingual or not —
		// carries the "MTK WRITERS TEMPLATE" house-style header, so treating that header alone
		// as a signal for "this module needs bilingual/reoMode handling" over-fires on a huge
		// number of ordinary, non-bilingual modules. Because of that, the mtkFlag is only
		// honoured as a reoMode trigger when explicitly turned back on via the data flag
		// `use_mtk_flag:true`, or by setting env MTKREO_OFF=1 (which restores the OLDER,
		// over-eager behaviour — useful for comparing old vs. new output side by side).
		const _mtkArm = (!!dlCfg && dlCfg.use_mtk_flag === true)
			|| !!(typeof process !== "undefined" && process.env && process.env.MTKREO_OFF);
		const reoMode = !!dlCfg && dlCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.REOTRANSLATE_OFF)
			&& (/reoTranslate/i.test(run.resolvedRules?.body_class || "") || (_mtkArm && !!run.mtkFlag)
				|| (dlCfg.code_prefixes || []).some((p) => String(run.moduleCode || "").toUpperCase().startsWith(String(p).toUpperCase())));
		const FUND_SENTINEL = (fundCfg && fundCfg.sentinel) || "<!--CV2_FUNDPANEL-->";
		// The SSFUN fundamentals subject group marks its phase boundaries differently from
		// HPFUN above — instead of "[New tab]", it uses a "[LESSON] FUNdamental Phase N"
		// marker (a PAGE_BOUNDARY tag that stays in the item stream when the whole module
		// lives on one file/page). Because the marker is different, it needs its own,
		// separate sentinel to drive the same phase-panel-wrapping behaviour.
		const FUND_LESSON_SENTINEL = (fundCfg && fundCfg.lesson_sentinel) || "<!--CV2_FUNDPHASE-->";
		// The TEFUN fundamentals subject group marks each phase boundary with an even plainer
		// convention still: a line of completely ordinary black body text that just says
		// "Phase N" — no writer tag at all. Neither the HPFUN "[New tab]" handling above, nor
		// the SSFUN "[LESSON]" handling, recognises this shape, so without special-casing it
		// the body was never split into panels and each "Phase N" line leaked straight through
		// into the output as a meaningless "<p>Phase N</p>".
		//
		// This is detected when a SINGLE page contains at least `min_delimiters` standalone
		// "Phase N" black paragraphs AND has none of the other tag-based page/phase delimiters
		// ("[New tab]" / "[LESSON]" / "[Page N]"). When that fires, each "Phase N" line is
		// consumed and replaced with a panel sentinel; the phase_text branch of
		// PanelsBuilder.fundamentalsPanels then builds the ".phases" navigation strip, the
		// ".introduction" wrapper, and one "fundamentalsPanel" per phase from those sentinels.
		//
		// The ">=2 lines on the page" + "no other tag-based delimiter" combination scopes this
		// narrowly to the clean, single-page, 4-phase TEFUN01 through TEFUN08 family, and
		// correctly EXCLUDES a module like MXFUN01, which spreads its phases 1/2/4 across a
		// deep, multi-file "[Page N]"/"[Lesson]" structure instead.
		// Data flag: fundamentals_panels.phase_text   Env toggle: FUNDPHASE_OFF
		const fundPhaseCfg = fundCfg && fundCfg.phase_text;
		const FUND_PHASETEXT_SENTINEL = (fundPhaseCfg && fundPhaseCfg.sentinel) || "<!--CV2_FUNDPHASETEXT-->";
		const phaseTextRe = new RegExp((fundPhaseCfg && fundPhaseCfg.delimiter_pattern) || "^phase\\s+\\d+$", "i");
		// The ENFUN fundamentals subject group uses yet another way of marking phase
		// boundaries: a standalone span of RED text reading "Phase N", with no square
		// brackets around it at all — so the tag-classifier treats it as plain unstructured
		// "noise" with no resolvable tag, and it renders nothing by itself. This is the
		// red-coloured cousin of the plain black "Phase N" line the TEFUN group uses above, but
		// because it carries no brackets, the black-line-only handling above never recognised
		// it, so these 8 ENFUN modules' whole phase navigation/panel layout was shipping
		// completely flat (unstructured) instead of split into phases.
		//
		// This class was measured across every Writers Template in the corpus
		// (outputs/_measure_funpanred.cjs): it is EXACTLY 8 modules, all in the single-file
		// ENFUN subject|template group, each numbering its phases [1, 2, 3, 4]. The very first
		// "Phase 1" span sits BEFORE the page's [Overview] section marker, so it is routed to
		// the body (not the menu) by #partitionItems — it renders nothing in the menu either
		// way. 24 other, longer mentions of the words "Phase N" inside ordinary prose are
		// correctly left alone, because the rule only fires when the ENTIRE folded text of the
		// span is nothing but "Phase N"; one lone matching span on module MXFUN02 falls below
		// the minimum-delimiter-count threshold and so doesn't trigger this path either.
		//
		// InteractiveScanner (a different file) also knows about this exact same red-span
		// pattern and treats it as a hard stopping point when capturing the members of an
		// interactive widget — without that, 3 of these 4 spans across three ENFUN modules
		// would otherwise get accidentally swallowed as if they were part of a widget instead
		// of a phase boundary.
		// Data flag: fundamentals_panels.phase_text.red_delimiter
		// Env toggle: FUNPANRED_OFF (reverts ALL THREE pieces of this mechanism at once — the
		// detection here, the routing in #partitionItems, and the scanner's hard stop)
		const redDelimCfg = fundPhaseCfg && fundPhaseCfg.red_delimiter;
		const redDelimOn = !!redDelimCfg && redDelimCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FUNPANRED_OFF);
		const isRedPhaseItem = (it) => redDelimOn && it.type === "tag" && !it.parse?.primary
			&& (it.parse?.class === "noise" || it.parse?.class === "instruction")
			&& it.consumedBy === undefined
			&& phaseTextRe.test((it.parse?.folded ?? "").trim());
		// The ARFUN fundamentals subject group marks phase boundaries with BRACKETED red
		// instruction spans — a third distinct convention, different from both TEFUN's plain
		// black "Phase N" line and ENFUN's bare (bracket-less) red span handled above.
		// OPENERS look like "[Phase one content begins]" or "[Start of phase two content]"
		// (classified as an unresolved instruction with no primary tag — its folded text
		// keeps the brackets, so without this handling it would just render as a retained,
		// visible developer note). CLOSERS look like "[End of Phase One]" or "[End of phase
		// two content]" (these DO resolve to a primary tag, "end other", with a
		// CONTAINER_CLOSE directive — the different "[End page and …]" PAGE_BOUNDARY phrasing
		// never reaches this code at all). Both openers and closers become phase-break markers.
		//
		// ARFUN02 has one phase boundary (phase 4) marked ONLY by a closer, with no matching
		// opener at all — which is why closers are accepted as break points in the first
		// place. To stop this from misfiring elsewhere, a closer is only ever accepted on a
		// page that already has at least one accepted OPENER. This guard specifically protects
		// 7 other modules that use closer-only phrasing for a different reason entirely (the
		// TEFUN family's own "[end phase N]" markers, which are already handled by the plain
		// black "Phase N" convention above — accepting them again here would double up their
		// phase breaks), and it protects ARFUN04, a multi-file module whose similar-looking
		// "beginning of/begin" phrasing is a deliberately different, unrelated pattern.
		//
		// A closer immediately followed by an opener, or a trailing break with nothing after
		// it, is harmless — the panel-building code that consumes these markers simply trims
		// and discards any empty segments. This class was measured against every Writers
		// Template in the corpus (outputs/_measure_funpanbracket.cjs) and is EXACTLY modules
		// ARFUN01, ARFUN02, ARFUN03 and ARFUN05.
		// Data flag: fundamentals_panels.phase_text.bracketed_delimiter
		// Env toggle: FUNPANBRACKET_OFF
		const brCfg = fundPhaseCfg && fundPhaseCfg.bracketed_delimiter;
		const brOn = !!brCfg && brCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FUNPANBRACKET_OFF);
		const brOpenRe = brOn && brCfg.opener_pattern ? new RegExp(brCfg.opener_pattern, "i") : null;
		const brCloseRe = brOn && brCfg.closer_pattern ? new RegExp(brCfg.closer_pattern, "i") : null;
		const brCloserDirs = (brCfg && brCfg.closer_primary_directives) || ["PAGE_BOUNDARY", "CONTAINER_CLOSE"];
		const isBracketOpener = (it) => !!brOpenRe && it.type === "tag" && !it.parse?.primary
			&& (it.parse?.class === "noise" || it.parse?.class === "instruction")
			&& it.consumedBy === undefined
			&& brOpenRe.test((it.parse?.folded ?? "").trim());
		// opener count FIRST (page-level) — the closer fence keys on it
		const bracketOpenerCount = brOpenRe ? bodyItems.reduce((n, it) => n + (isBracketOpener(it) ? 1 : 0), 0) : 0;
		const brCloserOk = !!brCloseRe && (brCfg.closer_requires_opener === false || bracketOpenerCount >= 1);
		const isBracketCloser = (it) => brCloserOk && it.type === "tag"
			&& it.consumedBy === undefined
			&& (!it.parse?.primary || brCloserDirs.includes(it.parse?.primary?.directive))
			&& brCloseRe.test((it.parse?.folded ?? "").trim());
		// Two more modules, SCFUN01 and SSFUN03, use yet another phase-marking convention:
		// the word "Phase N" is attached as the TRAILING TEXT of an otherwise-ordinary writer
		// tag, rather than standing alone. SCFUN01 writes "[TILE N] Phase N" (the tag itself
		// resolves to a "shape n" sub-tag; one of its tiles is typed in plain black rather than
		// red, which is handled by a separate black_line_pattern check). SSFUN03 writes
		// "[Fundamental content] SSFUN03 **PHASE N**" (the tag resolves to a "lesson content"
		// section-marker; the SSFUN03 module code itself appears inline in the text, matched
		// via a {code} placeholder that gets filled in with the running module's own code).
		//
		// Because these two modules render their phases differently in the human-built output,
		// the `eligible_tags` config maps each tag to which BREAK KIND it should produce:
		// "phase_text" (SCFUN01's human version has no generated phase heading, matching the
		// TEFUN style) or "lesson" (SSFUN03's human version DOES get a generated
		// "<h3>Phase N</h3>" heading, matching the rest of its SSFUN sibling modules). The
		// match requires the ENTIRE cleaned trailing text to be exactly "Phase N" (after
		// stripping bold-markdown and punctuation), so nothing is ever silently swallowed by
		// accident.
		//
		// Measured against every Writers Template in the corpus
		// (outputs/_measure_funpantag.cjs), this class is EXACTLY these 2 modules; a similar-
		// looking but different tag family ("[Title] Phase N" on modules EXPFUN02-05) is
		// correctly excluded because it isn't in the eligible-tags list. Every matching item
		// here is one that no interactive widget had already claimed, so no matching change was
		// needed over in InteractiveScanner for this particular dialect.
		// Data flag: fundamentals_panels.phase_text.tag_anchored_delimiter
		// Env toggle: FUNPANTAG_OFF (FUNDPHASE_OFF reverts the entire phase-panel mechanism,
		// including this one)
		const taCfg = fundPhaseCfg && fundPhaseCfg.tag_anchored_delimiter;
		const taOn = !!taCfg && taCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FUNPANTAG_OFF);
		const taTags = (taOn && taCfg.eligible_tags) || {};
		const taClean = (s) => String(s || "").replace(/\*\*/g, " ")
			.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, "").replace(/\s+/g, " ").trim().toLowerCase();
		const taBaRe = taOn ? new RegExp((taCfg.blackafter_pattern || "^(?:{code}\\s*)?phase\\s+\\d+$")
			.replace("{code}", String(run.moduleCode || "").toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))) : null;
		const taKindOf = (it) => {
			if (!taOn || it.type !== "tag" || it.consumedBy !== undefined) return null;
			const kind = taTags[it.parse?.primary?.tag];
			return (kind && taBaRe.test(taClean(it.blackAfter))) ? kind : null;
		};
		// the BLACK-typed twin (a tile line the writer never made red — keeps its brackets)
		const taLineRe = taOn && taCfg.black_line_pattern ? new RegExp(taCfg.black_line_pattern, "i") : null;
		const taLineClean = (s) => String(s || "").replace(/\*\*/g, " ")
			.replace(/^[^\p{L}\p{N}\[\]]+|[^\p{L}\p{N}\[\]]+$/gu, "").replace(/\s+/g, " ").trim();
		const isTaLine = (ln) => !!taLineRe && taLineRe.test(taLineClean(ln));
		// ACCORDION-AS-PHASES: module XFUN01 authors its phases as ONE single [Accordion]
		// widget containing nine numbered sections, [Accordion 1] through [Accordion 9] — but
		// the human-built version of this module does NOT build an actual accordion widget at
		// all. Instead it builds the same phase-navigation chrome used elsewhere in this file,
		// mapping accordion section 1 to phase 1, section 2 to phase 2, and so on, one-to-one
		// by number.
		//
		// This required a genuinely new kind of phase-delimiter handling, because normally the
		// numbered [Accordion N] tags would simply get scooped up (bundle-consumed) by
		// InteractiveScanner as members of one big accordion interactive widget, long before
		// this code ever sees them. To prevent that, InteractiveScanner checks the same
		// registry row this file reads (see #accordionPhaseRow above — the row for group
		// "XFUN|combo") and SUPPRESSES its normal accordion-bundling behaviour on any page that
		// registry row applies to (numbered accordions are otherwise the completely standard,
		// ordinary way to build a real accordion widget on about 60 other, non-fundamentals
		// modules, so this suppression is narrowly scoped and measured to have essentially no
		// effect outside this one gated case).
		//
		// With bundling suppressed, the accordion-related items reach this code unconsumed,
		// and each shape is handled: a NUMBERED invocation like "[Accordion 3]" becomes a
		// phase-break marker (each resulting panel keeps its own writer-authored [H3]/[H4]
		// heading, rather than one being generated); the bare, un-numbered "[accordion]"
		// opening tag and the "[End accordion section]" closing tags (in both their bracketed
		// and bracket-less forms) are simply consumed and produce nothing; a "[link to …
		// section]" cross-reference tag is dissolved back into ordinary prose text (the
		// human-built version keeps the surrounding sentence but drops the link itself, which
		// also gets rid of what used to be a confusing "orphaned sub-tag" warning); and any
		// leftover, split-bracket black "[" residue left over from the above is simply dropped.
		// Data flag: fundamentals_panels.phase_text.accordion_delimiter
		// Env toggle: FUNPANACC_OFF (FUNDPHASE_OFF reverts the entire phase-panel mechanism,
		// including this one)
		const accCfg = fundPhaseCfg && fundPhaseCfg.accordion_delimiter;
		const accOn = !!accCfg && accCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FUNPANACC_OFF);
		const accRow = accOn ? ContentConverter.#accordionPhaseRow(accCfg, run) : null;
		const accNumRe = accRow ? new RegExp(accCfg.numbered_pattern || "^\\[accordion\\s+\\d+\\]$", "i") : null;
		const accNoopRes = accRow ? [
			new RegExp(accCfg.bare_pattern || "^\\[accordion\\]$", "i"),
			...((accCfg.noop_patterns || ["^\\[?end accordion section\\]?$"]).map((r) => new RegExp(r, "i"))),
		] : [];
		const accNoopTags = (accCfg && accCfg.noop_tags) || ["accordion", "end accordion"];
		const accLinkRe = accRow && accCfg.link_dissolve_pattern ? new RegExp(accCfg.link_dissolve_pattern, "i") : null;
		const accResidueRe = accRow && accCfg.black_residue_pattern ? new RegExp(accCfg.black_residue_pattern) : null;
		const isAccBreak = (it) => !!accNumRe && it.type === "tag" && it.consumedBy === undefined
			&& it.parse?.primary?.tag === (accCfg.tag || "accordion")
			&& accNumRe.test((it.parse?.folded ?? "").trim());
		const isAccNoop = (it) => !!accNoopRes.length && it.type === "tag" && it.consumedBy === undefined
			&& (!it.parse?.primary || accNoopTags.includes(it.parse?.primary?.tag))
			&& accNoopRes.some((re) => re.test((it.parse?.folded ?? "").trim()));
		const isAccLink = (it) => !!accLinkRe && it.type === "tag" && it.consumedBy === undefined
			&& accLinkRe.test((it.parse?.folded ?? "").trim());
		// Count "Phase N" delimiter LINES across the UNCONSUMED black items. This has to be
		// robust to text having been merged together (coalesced) earlier in the pipeline — a
		// "Phase N" line can end up sitting at the start, middle, or end of a merged run of
		// black text (on TEFUN02, "Phase 1" trails the introduction's body text; on TEFUN05, the
		// phase lines land in the middle of a merged run). A line that some OTHER interactive
		// widget has already captured (consumedBy is set) stays inside that widget and is not
		// counted here. The red-span delimiter form (the ENFUN dialect, above) counts toward
		// this same total too — both forms share one page-level "at least min_delimiters"
		// threshold; no module in the corpus has been found to use both forms at once.
		const phaseLineCount = bodyItems.reduce((n, it) =>
			(it.type === "black" && it.consumedBy === undefined)
				? n + String(it.text || "").split("\n").filter((ln) => phaseTextRe.test(ln.trim()) || isTaLine(ln)).length
				: n + ((isRedPhaseItem(it) || isBracketOpener(it) || isBracketCloser(it) || taKindOf(it) || isAccBreak(it)) ? 1 : 0), 0);
		// SCOPE to the SINGLE-FILE fundamentals page model (the phase-panel template is single-file:
		// the whole module — all phases — on one page). MXFUN01 is multi-file (page_model "multi-file",
		// 19 pages) → excluded, matching the human; every TEFUN level is single-file. (phaseLineCount>=2
		// already excludes MXFUN01 — its phase lines never surface as >=2 unconsumed black lines on a
		// single page — so the page-model test is belt-and-braces against a future multi-file case.)
		const singleFilePage = run.resolvedRules?.page_model === "single-file";
		const phaseTextMode = fundPanelMode && !!fundPhaseCfg && fundPhaseCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FUNDPHASE_OFF)
			&& singleFilePage
			&& phaseLineCount >= ((fundPhaseCfg && fundPhaseCfg.min_delimiters) || 2);
		// PHASE-TEXT PRE-PASS: walk through the body items and split apart every black-text item
		// wherever it contains a "Phase N" delimiter LINE, replacing that line with a
		// NON-black {type:"phasebreak"} marker item. Making the marker non-black matters: both
		// MediaBuilder.gatherFollowing (which stops gathering text as soon as it hits a
		// non-black item) and the earlier black-run-merging step would otherwise have happily
		// swallowed a bare "Phase N" line into whatever [Body]/[image] element sits next to it,
		// hiding the delimiter. This only touches UNCONSUMED items — a phase line already
		// captured inside some other interactive widget is left exactly where it is. The loop
		// walks the item list BACKWARDS, so that splicing an item out never shifts the index of
		// an item that hasn't been visited yet.
		if (phaseTextMode) {
			for (let k = bodyItems.length - 1; k >= 0; k--) {
				const bi = bodyItems[k];
				// The RED-span delimiter form (ENFUN): replace the whole span with a phasebreak
				// marker; if it happens to carry any trailing (blackAfter) text, that text
				// survives as its own separate black item (measured: none of the 8 ENFUN
				// modules actually carry any such trailing text, but this is kept as a safety
				// net). The BRACKETED opener/closer forms (ARFUN) take exactly the same path
				// (and likewise, none of the 4 ARFUN modules carry trailing text either — same
				// safety net).
				if (isRedPhaseItem(bi) || isBracketOpener(bi) || isBracketCloser(bi)) {
					const repl = [{ type: "phasebreak" }];
					if (bi.blackAfter && bi.blackAfter.trim()) repl.push({ type: "black", text: bi.blackAfter, block: bi.block });
					bodyItems.splice(k, 1, ...repl);
					continue;
				}
				// The ACCORDION-INVOCATION forms (XFUN01; only reached because the registry gate
				// told InteractiveScanner to leave them unconsumed): a numbered "[Accordion N]"
				// becomes a phasebreak; the bare opener and the closer tags become no-ops
				// (produce nothing); a "[link to … section]" cross-reference dissolves into its
				// trailing prose text; any leftover split-bracket black "[" residue is dropped
				// entirely. Any trailing (blackAfter) text is preserved everywhere it could
				// occur, even though none of the measured numbered/bare/closer cases actually
				// carry any — again, a safety net rather than an observed requirement.
				if (isAccBreak(bi)) {
					const repl = [{ type: "phasebreak" }];
					if (bi.blackAfter && bi.blackAfter.trim()) repl.push({ type: "black", text: bi.blackAfter, block: bi.block });
					bodyItems.splice(k, 1, ...repl);
					continue;
				}
				if (isAccNoop(bi) || isAccLink(bi)) {
					const repl = [];
					if (bi.blackAfter && bi.blackAfter.trim()) repl.push({ type: "black", text: bi.blackAfter, block: bi.block });
					bodyItems.splice(k, 1, ...repl);
					continue;
				}
				if (accResidueRe && bi.type === "black" && bi.consumedBy === undefined
					&& accResidueRe.test(String(bi.text || "").trim())) {
					bodyItems.splice(k, 1);
					continue;
				}
				// The TAG-ANCHORED forms (SCFUN01/SSFUN03): the whole item — the tag plus its
				// trailing "Phase N" text — collapses into ONE phasebreak marker, tagged with a
				// "kind" so the emitter downstream knows which panel style to build. Because the
				// match rule requires the ENTIRE cleaned trailing text to be nothing but "Phase
				// N", there is guaranteed to be no leftover prose that could be silently lost.
				// The "kind" selects which sentinel gets emitted: "lesson" routes to the SSFUN
				// generated-heading style, anything else routes to the plain phase_text style.
				{
					const taKind = taKindOf(bi);
					if (taKind) { bodyItems.splice(k, 1, { type: "phasebreak", kind: taKind }); continue; }
				}
				if (bi.type !== "black" || bi.consumedBy !== undefined) continue;
				const lines = String(bi.text || "").split("\n");
				if (!lines.some((ln) => phaseTextRe.test(ln.trim()) || isTaLine(ln))) continue;
				const repl = []; let buf = [];
				const flush = () => { if (buf.join("\n").trim()) repl.push({ type: "black", text: buf.join("\n"), block: bi.block }); buf = []; };
				for (const ln of lines) {
					// A BLACK-typed "[Tile N] Phase N" line (one the writer forgot to colour red —
					// SCFUN01's tile 2 is like this) still counts as a break, exactly like a plain
					// black "Phase N" line does.
					if (phaseTextRe.test(ln.trim()) || isTaLine(ln)) { flush(); repl.push({ type: "phasebreak" }); }
					else buf.push(ln);
				}
				flush();
				bodyItems.splice(k, 1, ...repl);
			}
		}

		// LEVEL-PAGE FUNDAMENTALS (ROUND 265 — the CHFUN "[PAGE N Novice]" dialect,
		// module CHFUN01). The Languages Fundamentals family authors ONE single-file
		// module as a sequence of "[PAGE N <Level>]" sections grouped by proficiency
		// LEVEL (Novice, Emergent, …): each level becomes ONE fundamentalsPanel (all
		// of its pages joined, each page keeping its own title as a section heading),
		// the phases nav + phaseLink tiles are labelled with the LEVEL names, and the
		// per-page "[Page Overview]" learning-intentions blocks are aggregated BY
		// LEVEL into the module menu's per-level tab panes (the module's own
		// [Overview] section's [H3]-labelled LI/SC blocks become the menu's Overview
		// pane, while its introduction prose stays in the body's introduction).
		// Registry-gated (fundamentals_panels.level_pages.registry — the CHFUN|combo
		// group) + single-file page model, so no other module family can enter this
		// path. Data: body_region.fundamentals_panels.level_pages.
		// Env toggle: LEVELPAGE_OFF (reverts the whole dialect).
		const lvInfo = this.#levelPagesPrepass(bodyItems, run, fundPanelMode, singleFilePage);

		// INQUIRY TABBED TEMPLATE (the BLL "[Tab N] label-list" family): some modules present
		// their content as a set of navigable "inquiry" panels labelled by a crumb-trail of
		// [Tab N] tags, rather than as one continuous page. To avoid mistaking this for the
		// UNRELATED "[tabs]" interactive WIDGET (which also uses [Tab N] sub-tags, but is a
		// single self-contained widget, not a whole-page navigation structure — modules like
		// BLL232, BLL236, OSAI501, and ENGJ402 use that instead), this only fires on a
		// deliberately conservative combination of signals: a writer instruction mentioning
		// "side tabs" AND at least 2 [Tab N] sub-tags present. A "[Tab N] <label>" list entry
		// with text after it captures a crumb-trail label; an EMPTY "[Tab N]" (no label text)
		// opens a new panel (marked with a sentinel).
		// Data flag: body_region.inquiry_tabs   Env toggle: INQUIRYTABS_OFF
		const inqCfg = tpl.body_region.inquiry_tabs;
		const inquiryLabels = {};
		const isTabItem = (it) => it.type === "tag"
			&& (/^\s*tab\s*\d/i.test(String(it.text || "")) || /\btab\b/i.test(it.parse?.primary?.tag || ""));
		// FIRE when ≥2 orphan top-level `[Tab N]` (widget `[tabs]` members are consumed by
		// the scanner, so they never reach here) AND a confirming signal: a `[Tab N] <label>`
		// crumb-list (≥3 labelled) OR a "side tabs" instruction. The label-list is the robust
		// primary signal (the instruction text is classified as a CS note and is awkward to read).
		const _tabItems = bodyItems.filter(isTabItem);
		const _labeledTabs = _tabItems.filter((it) => (it.blackAfter || "").trim().length > 0).length;
		// EMPTY `[Tab N]` openers are the inquiry PANEL openers; a mis-captured `[tabs]`
		// WIDGET's orphan tabs carry CONTENT (labelled), so requiring ≥2 EMPTY openers
		// excludes them (MXDB202) while the BLL inquiry pages (6-7 empty openers) fire.
		const _emptyOpeners = _tabItems.filter((it) => !(it.blackAfter || "").trim()).length;
		const _sideTabsInstr = bodyItems.some((it) => /side\s*tabs?/i.test(`${it.text || ""} ${it.blackAfter || ""}`));
		// A `[page N]`-DELIMITED PANEL variant: the BLL phonics subject group writes a labelled
		// `[Tab N]` crumb-list (at least 3 entries) but then opens its FIRST panel with an empty
		// `[Tab 1]` and every panel AFTER that with a labelled `[page N]` marker instead. That
		// means the page has only ONE empty `[Tab N]` opener overall, which is not enough to
		// trigger the "at least 2 empty openers" rule above, but it also isn't a pure
		// heading-labelled page either (it does have labelled tabs). This block detects that
		// specific in-between shape and fires `_bllInquiry` for it too, so the SAME
		// `bll_page_split` panel-building logic further down handles it — no separate build
		// code is needed. Requiring at least 3 top-level `[page N]` markers is what tells this
		// apart from the UNRELATED "[tabs]" interactive widget family (modules like MXDB202,
		// XGF9003, and MXFL301 have labelled, orphaned `[Tab N]` tags but zero `[page N]`
		// openers) — measured against every "[Tab N]"-using module in the corpus, this never
		// misfires (outputs/_measure_bllpage_widen.cjs).
		// Data flag: inquiry_tabs.page_opener_fire
		// Env toggle: BLLPAGEOPENER_OFF (independent of INQUIRYTABS_OFF, which controls the
		// simpler empty-opener form above)
		const _pageOpeners = bodyItems.filter((it) => it.type === "tag"
			&& it.consumedBy === undefined
			&& it.parse?.primary?.directive === "PAGE_BOUNDARY"
			&& /\bpage\b/i.test(it.parse?.primary?.tag || "")).length;
		const _pgCfg = inqCfg && inqCfg.page_opener_fire;
		const _pageDelimited = !!_pgCfg && _pgCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.BLLPAGEOPENER_OFF)
			&& _labeledTabs >= (_pgCfg.min_labeled ?? 3)
			&& _emptyOpeners >= (_pgCfg.min_empty ?? 1)
			&& _pageOpeners >= (_pgCfg.min_page_openers ?? 3);
		const _bllInquiry = !!inqCfg && inqCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.INQUIRYTABS_OFF)
			&& ((_emptyOpeners >= 2 && (_labeledTabs >= 3 || _sideTabsInstr)) || _pageDelimited);
		// The TWHA/TWHK HEADING-LABEL family is a third shape again: EMPTY [Tab N] openers with
		// NO labelled crumb-list at all and NO "side tabs" writer instruction — instead, each
		// panel's crumb label is taken from that panel's own FIRST heading. This fires when
		// there are zero labelled tabs (_labeledTabs === 0) AND at least `min_openers` empty
		// openers. That threshold was tuned by measurement to 6, which cleanly separates the
		// real modules that use this shape (TWHA901 has 17, TWHK903 has 17, TWHA906 has 13,
		// TWHA903 has 8) from every module that merely LOOKS similar but has 4 or fewer (a
		// "[End tab]" CONTAINER_CLOSE closer tag also gets counted as an "empty opener" by the
		// raw count, which inflates the number, but a closer never actually opens a new panel).
		// This reuses ALL of the SAME panel-splitting machinery as the other inquiry-mode
		// variants above (pushing sentinels, suppressing orphaned tags, recovering labels) by
		// simply being OR'd into the same `inquiryMode` flag; the only difference is which BUILD
		// form gets used, chosen by a `headingLabel` flag passed through to
		// PanelsBuilder.inquiryPanels.
		// Data flag: inquiry_tabs.heading_label   Env toggle: HEADINGLABEL_OFF
		// TRUE openers = empty [Tab N] that are NOT a [End tab] CONTAINER_CLOSE closer (the closers
		// inflate _emptyOpeners). Requiring ≥ min_true_openers EXCLUDES the EX `[Section N]`/`[New side
		// tab]` family (EXPFUN04: 1 opener + 7 closers = _emptyOpeners 8 but only 1 panel) which would
		// otherwise fire and build a 1-panel page where the human has 7. The PANEL SPLIT pushes a
		// sentinel per true opener, so this is also the real panel-count signal.
		const _trueOpeners = _tabItems.filter((it) => !(it.blackAfter || "").trim()
			&& it.parse?.primary?.directive !== "CONTAINER_CLOSE").length;
		// SINGLE-FILE scope guard: the TWHA/TWHK heading-label template above is meant for a
		// one-page inquiry "landing" module. A completely different family — the EX subject
		// group's "[New side tab]" markers (seen on EXIP901/EXBP901) — happens to parse into
		// the SAME empty "[Tab N]" opener shape, but those modules are spread across several
		// files/pages (page_model "multi-file") and are a different, deliberately not-yet-
		// handled structure. Without this guard, the heading-label logic above would wrongly
		// fire on those EX lesson pages too, mis-building 6 to 8 panels per module. This guard
		// only EXCLUDES a page when it is explicitly marked multi-file — everything else
		// defaults to firing, matching the same "default to yes unless proven multi-file"
		// approach used for the fundamentals single-page detection earlier in this file.
		const _singleFile = run?.resolvedRules?.page_model !== "multi-file";
		const _hlCfg = inqCfg && inqCfg.heading_label;
		const _headingLabelOn = !!inqCfg && inqCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.INQUIRYTABS_OFF)
			&& !!_hlCfg && _hlCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.HEADINGLABEL_OFF)
			&& _singleFile
			&& _labeledTabs === 0
			&& _emptyOpeners >= (_hlCfg.min_openers ?? 6)
			&& _trueOpeners >= (_hlCfg.min_true_openers ?? 2);
		const inquiryMode = _bllInquiry || _headingLabelOn;
		const INQ_SENTINEL = (inqCfg && inqCfg.sentinel) || "<!--CV2_INQPANEL-->";
		// The CED subject group has its own INQUIRY [Page N]-SPLIT variant (modules CEDK101,
		// CEDT404): these carry a PURE labelled `[Tab N]` crumb-list (with NO empty openers at
		// all — every tab already has a label) and instead split their panels wherever an
		// in-stream `[page N]` PAGE_BOUNDARY marker appears, all on one file/page. Because the
		// label list can appear either inside the menu region or the body region of the page,
		// `PanelsBuilder.detectInquiryCed` scans the WHOLE page stream (not just one partition)
		// to find and capture the labels, then flags each label item with `_inquiryCrumb` so
		// that BOTH the menu-building code and the body loop below know to skip over them. It
		// only fires on a deliberately conservative combination — a pure label list, at least 2
		// in-stream `[page N]` markers, and the panel count matching the crumb count — which
		// means the genuinely different `[tabs]`-WIDGET modules (which carry zero in-stream
		// `[page N]` markers) never trigger it by accident (verified with
		// `outputs/_probe_cedpage.cjs`). This is mutually exclusive with the BLL `inquiryMode`
		// above, because that one specifically requires EMPTY openers, and CED has none.
		// Data flag: body_region.inquiry_tabs.page_split   Env toggle: CEDPAGE_OFF
		const cedInq = PanelsBuilder.detectInquiryCed(page, tpl);
		const cedInquiryMode = cedInq.on;
		// SIDE-ALERT PAIRING: in the human-built output, a RIGHT-positioned alert box sits
		// side-by-side with the content that follows it, sharing one row (an 8-column content
		// block next to a 4-column alert block), rather than sitting in its own separate row
		// above or below. To reproduce that, a right-positioned alert is DEFERRED instead of
		// emitted immediately (`pendingSideAlert` holds its col-md-4 HTML) and only attached —
		// as the right sibling of the FOLLOWING content's col-md-8 column — once that following
		// row actually closes. `sideAlertSawMedia` delays that row-close until AFTER any
		// introductory media (a video or image) has flowed in, so that a film-title heading
		// plus its video both end up gathered together inside the same col-md-8 column as the
		// alert's partner. Both of these stay null/false in every other, ordinary case.
		let pendingSideAlert = null;
		let sideAlertSawMedia = false;
		// true right after a heading was emitted — lets ONE text run join
		// the heading's row (rowCfg.heading_keeps_next_black_run)
		let headingHold = false;
		// THE [page N]-LABEL FOLD: holds onto the label text of the MOST RECENT `[page N]` panel
		// opener, for as long as that panel is still completely EMPTY (i.e. the very last thing
		// pushed so far is still just the INQ_SENTINEL marker with nothing inside it yet). This
		// lets a supervisor-note callout that opens a new section derive its own heading text
		// from that held label — matching the human-built version's in-panel "<h2>" heading
		// (seen on modules BLL140 pages 2-7, BLL150 page 5, BLL160 page 5; measured with
		// outputs/_measure_pagelabel_fold.py). The held value is overwritten the moment the
		// NEXT `[page N]` opener arrives, and cleared out entirely by an empty-`[Tab N]` opener,
		// by the CED page-split logic, or once it has actually been used.
		// Data flag: callouts.by_tag.'supervisor note'.fold_page_label
		// Env toggle: PAGEFOLD_OFF
		let pageLabelHold = "";
		// THE XDLS900 CHOICE-PAGE TILE NAVIGATION (ROUND 226 — Chris's XDLS900 screenshot
		// triage): once the "[LESSON Choice page]" opener has been seen on this page, this
		// holds the build state ({ cfg, labels }) — the labels harvested from the writer's
		// [Tab Nav Layout] one-column category table — until the end of the page, where the
		// tile grid renders as the page's LAST body row (the human-built pages place the
		// choicePage row after all the introduction content). Stays null on every page that
		// has no choice-page opener.
		// Data flag: body_region.choice_page_tiles   Env toggle: CHOICETILES_OFF
		let choiceTiles = null;
		// CHILD-DICTATES-ANCESTOR RULE: when an activity box contains a supervisor note inside
		// it, the outer content ROW that wraps that activity needs to carry an extra
		// '.supervisor' CSS class — the frontend's "reveal" JavaScript specifically looks for a
		// "div.row.supervisor" element, and without that class the note would render as plain
		// inline text instead of the intended pop-up icon/modal (this was seen going wrong on
		// module BLL241, pages 2A and 2C). Since the row is opened BEFORE it's known what's
		// inside the activity, the activity-opening code sets `nextRowClass` in advance; the
		// `emit` function below applies whatever class is waiting there to the row it's about
		// to open, then resets it back to empty.
		// Data flag: body_region.content_row_open, the '{rowClass}' template slot
		let nextRowClass = "";
		const emit = (...html) => {
			// lazy row opening — a row only exists once REAL content arrives, so an
			// emit() with nothing to push (e.g. a de-duped lesson-title heading that
			// returns []) can never produce an empty, useless "row > col" pair.
			const content = html.filter(Boolean);
			if (!content.length) return;
			if (!rowOpen) {
				parts.push(Utils.FillTemplate(tpl.body_region.content_row_open,
					{ contentColClass: tpl.body_region.content_col_class_default, rowClass: nextRowClass }));
				rowOpen = true; nextRowClass = "";
			}
			parts.push(...content);
		};
		const breakRow = () => {
			if (rowOpen) {
				if (pendingSideAlert) {
					// SIDE-ALERT PAIRING (see the field declaration above): close the col-md-8 main
					// column, append the held col-md-4 alert as its right sibling, then close the row —
					// reproducing the human-built version's shared-row layout.
					parts.push("</div>");           // close the col-md-8 main column
					parts.push(pendingSideAlert);   // the held col-md-4 > alert.top box
					parts.push("</div>");           // close the row
					pendingSideAlert = null; sideAlertSawMedia = false;
				} else {
					parts.push(tpl.body_region.content_row_close);
				}
				rowOpen = false;
			}
		};
		/**
		 * Row decision for the next root-level block, per its kind:
		 *  "heading"  → new row; the next text run may join it
		 *  "textRun"  → joins a heading's row once, else its own row
		 *  anything else ("block": media/table/callout/widget/…) → own row
		 * No-op while a container is open (stack non-empty).
		 */
		const rowFor = (kind) => {
			if (stack.length) return;
			// GROUPED ROWS (data: body_region.row_breaks.group_content) — matches
			// the human, where 86% of rows hold 2+ content children. Text and lists
			// FLOW into the current row; a heading starts a fresh row (the text
			// after it flows in); a hard block (media/table/callout/widget) takes
			// its own row. Replaces the legacy one-block-per-row over-counting.
			if (rowCfg.group_content) {
				// ROW GROUPING: measured against the human-built corpus (via _wt_human_align.py),
				// a human developer only opens a brand-new, top-level "div.row" at four kinds of
				// moment — a HEADING (24% of the time), an ACTIVITY (18%), the very start of the
				// page or a quote (14%), or a CALLOUT box (2%) — and simply FLOWS everything else
				// (media, tables, widgets, lists, ordinary body text) into whichever section row is
				// already open. An earlier, simpler rule gave every single piece of media or widget
				// its OWN row, which produced roughly twice as many rows as the human version and a
				// visibly "wall-to-wall" stack of extra "div.row" wrappers (first noticed comparing
				// against module OSAI401).
				const flowBlocks = rowCfg.flow_blocks
					&& !(typeof process !== "undefined" && process.env && process.env.ROWGROUP_OFF);
				if (kind === "heading" || kind === "section") {
					// SIDE-ALERT PAIRING: while a right-positioned alert is still waiting to be
					// paired and its intro media hasn't flowed in yet, GATHER this heading into the
					// alert's shared col-md-8 column instead of breaking into a new row — the
					// human-built version keeps a heading like "Under the Skin" inside that same
					// paired column rather than starting a fresh row for it.
					if (pendingSideAlert && !sideAlertSawMedia) return;
					breakRow(); return;
				}   // open a new section row
				if (flowBlocks) return;             // media/table/widget FLOW into the current section row
				if (kind === "textRun") return;     // (legacy) only text/lists flow
				breakRow();                          // (legacy) media/table/callout/widget → own row
				return;
			}
			// LEGACY per-block behaviour (a heading keeps one following text run).
			if (kind === "heading") {
				breakRow();
				headingHold = rowCfg.heading_keeps_next_black_run === true;
				return;
			}
			if (kind === "textRun" && headingHold) { headingHold = false; return; }
			headingHold = false;
			breakRow();
		};

		const stack = [];   // open containers (activities / SPANNING callouts)
		// ACTIVITY-REGION BOLD STRIP (full explanation on #activityBoldStripper below; does
		// nothing when the feature is switched off). Built ONCE per page, wrapped around the
		// LIVE `stack` array above: every time it is called, it looks at whatever container is
		// CURRENTLY on top of that stack, and only strips bold formatting while that top
		// container is an ACTIVITY box — if the top of the stack is instead a callout (an alert
		// box, which is handled separately and keeps its bold text) or the stack is empty, it
		// leaves the text completely unchanged.
		// Env toggle: ACTBOLD_OFF
		const actDeBold = this.#activityBoldStripper(stack, run);
		// Tracks which source blocks' whitelisted native Word comments have already been shown
		// to the reader (one source block can produce several output items — e.g. a paragraph
		// that becomes both a heading and a following text run — so its comment must be shown
		// only once, attached to the FIRST of those items, not repeated on every one).
		const commentedBlocks = new Set();
		// MEDIA-LIST COMMENTS: a whitelisted Word comment can also be anchored to a row of the
		// separate Media List document (rather than to the Writers Template body directly). When
		// that row carries a URL (`rowUrl`), the comment should be surfaced right BEFORE
		// whichever body element ends up linking that same piece of media — not stuck inside the
		// raw media-list table where nobody reading the finished page would ever see it. A
		// lookup of URL → [comment] is built from all such row-anchored comments, then each
		// content block's own link URLs are matched against that lookup. This is controlled by
		// the media_match data flag and the MEDIAMATCH_OFF environment toggle; the media-list
		// row itself (the comment's own anchor block) is excluded from the matching so a comment
		// never doubles up on its own anchor, and each matched comment is only ever shown once,
		// attached to the FIRST content element found that links it.
		const mmCfg = DataService.Data.CommentAuthors?.media_match;
		const mediaMatchOn = mmCfg && mmCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.MEDIAMATCH_OFF);
		// Matching is done by MEDIA KEY, not just the raw URL — a media key is either the exact
		// URL itself, OR (when the URL is a recognisable iStock/YouTube link) the extracted
		// iStock/YouTube reference number on its own. This matters because a body IMAGE is often
		// shown only as an un-built ("Mode-P") placeholder that has no clickable link at all —
		// its only remaining trace of the original URL is that same iStock reference id. Using
		// both forms of the key lets a Media List comment still reach that placeholder image.
		// This id-matching approach was verified against real modules (every id matched between
		// the body and the media list on MXDI202, 18 out of 18, and on MXFL301, 76 out of 76).
		// The plain exact-URL key continues to cover ordinary videos and pasted links as before.
		const urlComments = new Map();
		const emittedMedia = new Set();
		if (mediaMatchOn) {
			const seenMC = new Set();
			for (const bi of bodyItems) {
				for (const c of (bi.block?.comments ?? [])) {
					if (!c.rowUrl) continue;
					const dk = `${c.author}||${c.text}||${c.rowUrl}`;
					if (seenMC.has(dk)) continue;
					seenMC.add(dk);
					const entry = { c, anchorBlock: bi.block };
					for (const k of NotesAndComments.mediaKeys(c.rowUrl)) {
						if (!urlComments.has(k)) urlComments.set(k, []);
						urlComments.get(k).push(entry);
					}
				}
			}
		}
		// the media keys an item (or its whole bundle, on the bundle's first item) carries
		const itemMatchKeys = (it) => {
			if (!mediaMatchOn || !urlComments.size) return [];
			const urls = [];
			if (it.consumedBy !== undefined) {
				const b = bundles[it.consumedBy];
				if (b && !b._emitted) {
					for (const tb of (b.tables ?? [])) for (const l of (tb.links ?? [])) if (l?.target) urls.push(l.target);
					for (const m of [...(b.openerItems ?? []), ...(b.memberItems ?? [])])
						for (const l of (m.block?.links ?? [])) if (l?.target) urls.push(l.target);
				}
			} else {
				for (const l of (it.block?.links ?? [])) if (l?.target) urls.push(l.target);
			}
			return urls.flatMap((u) => NotesAndComments.mediaKeys(u));
		};
		const emitMediaComments = (it) => {
			for (const k of itemMatchKeys(it)) {
				for (const entry of (urlComments.get(k) ?? [])) {
					if (entry.anchorBlock === it.block || emittedMedia.has(entry)) continue;
					emittedMedia.add(entry);
					const note = NotesAndComments.commentNoteFor(entry.c);
					if (note) { breakRow(); parts.push(note); }
				}
			}
		};
		// marks the open container as holding content — used by the
		// activity auto-close heuristics
		const markContent = () => {
			if (stack.length) stack[stack.length - 1].hasContent = true;
		};

		// rendered heading level for a tag item (null when not a heading)
		const renderedHeading = (primary) => {
			if (!primary) return null;
			if (!["h1", "h2", "h3", "h4", "h5", "heading", "activity heading"].includes(primary.tag)) return null;
			const digit = /^h\d$/.test(primary.tag) ? parseInt(primary.tag[1], 10) : 2;
			return Math.min(Math.max(digit + tpl.elements.heading.logical_to_element.body_shift, 2), 5);
		};

		/**
		 * Auto-closes open containers that must not swallow this item.
		 * Two modes (Emit_Templates):
		 *  - "activity": container_auto_close.activity_close_before —
		 *    heading/section heuristics (activities have no reliable end tag)
		 *  - "span": a callout the writer EXPLICITLY closes later — only a
		 *    section marker / page boundary force-closes early
		 *    (callouts.containment.span_close_before); the writer's [end X]
		 *    is otherwise authoritative.
		 * STRICT callouts never sit on this stack at all — they are emitted
		 * complete by #calloutStrict (the anti-over-nesting rule).
		 */
		const autoClose = (it) => {
			const primary = it.type === "tag" ? it.parse.primary : null;
			while (stack.length) {
				const top = stack[stack.length - 1];
				let hit;
				if (top.mode === "span" || top.mode === "span-wrap") {
					const spanCfg = tpl.callouts.containment.span_close_before;
					hit = primary && spanCfg.directives.includes(primary.directive);
					// a STRUCTURED-CONTENT wrap (no explicit [end X] — the callout wraps a
					// following table/widget) ALSO closes at a heading: the table is the
					// callout's content, so a heading after it begins a new section. This
					// bounds the wrap so it can't over-capture (an explicit [end X] span,
					// mode "span", trusts the writer and does NOT close at a heading).
					if (top.mode === "span-wrap") {
						const h = renderedHeading(primary);
						hit = hit || (h !== null && h <= (tpl.callouts.containment.wrap_close_heading_max ?? 3));
					}
				} else {
					const cfg = DataService.Data.EmitTemplates.container_auto_close.activity_close_before;
					// An activity's OWN TITLE heading belongs INSIDE the box and must NOT close it.
					// (a) an [activity heading] is ALWAYS the title (title_heading_tags) → never closes;
					// (b) a plain section heading (H2-H5 ≤ rendered_heading_max) is the title when it is
					//     the FIRST thing after the [Activity N] opener (top.hasContent === false) → stays
					//     inside; only AFTER the activity has content is such a heading a section break
					//     that closes it (heading_closes_only_after_content). Fixes the empty-activity-box
					//     spill (ENGC201-01 1B + 246 boxes/59 modules): a separate [Activity heading]/[H3]
					//     title right after the opener no longer auto-closes the box empty.
					const titleTags = cfg.title_heading_tags ?? [];
					const isTitleHeading = primary && titleTags.includes(primary.tag);
					const h = isTitleHeading ? null : renderedHeading(primary);
					// A writer's own [H3] SECTION heading closes the current activity box (the
					// threshold rendered_heading_max = 4 covers logical [H1]/[H2]/[H3] headings;
					// [H4]/[H5] sub-headings render at level >4 and stay INSIDE the activity instead of
					// closing it). Env toggle ACTHEAD_OFF reverts to an earlier, stricter threshold (3)
					// for side-by-side comparison of the two behaviours.
					const actHeadMax = (typeof process !== "undefined" && process.env && process.env.ACTHEAD_OFF)
						? (cfg.rendered_heading_max_legacy ?? 3)
						: cfg.rendered_heading_max;
					const headingCloses = h !== null && h <= actHeadMax
						&& (!cfg.heading_closes_only_after_content || top.hasContent);
					hit = headingCloses
						|| (primary && cfg.directives.includes(primary.directive))
						|| (primary && cfg.tags.includes(primary.tag));
				}
				if (!hit) return;
				emit(top.close);
				stack.pop();
				run.AddNote("info", "ContentConverter",
					`Page ${page.lessonLabel}: [${top.tag}] auto-closed before the next ${primary?.tag ?? it.type}.`);
				if (!stack.length) breakRow();
			}
		};

		// SECTION PRE-PASS for "[all external links]": when a writer's instruction says
		// "[all external links]", it declares that every [video] item in that section should
		// be treated as an external link rather than an embedded video — the human-built
		// version renders those as link-BUTTONS instead of video embeds (first seen on module
		// OSBY201, page 03). This pre-pass walks the body once, marking each governed [video]
		// item so that #element (below) knows to render it as a button; "governance" resets
		// automatically at the next heading or page boundary, so it can never leak past the
		// section the writer intended. This is driven entirely by the writer's own instruction
		// text — it is a general rule, not a special case tied to any one module code.
		// Env toggle: ALLEXTVID_OFF
		const aevTpl = tpl.elements.all_external_links_videos;
		const aevOn = aevTpl && aevTpl.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ALLEXTVID_OFF);
		if (aevOn) {
			let govern = false;
			for (const bi of bodyItems) {
				if (bi.type !== "tag") continue;
				const bp = bi.parse?.primary;
				if (renderedHeading(bp) !== null || bp?.directive === "PAGE_BOUNDARY"
					|| bp?.directive === "SECTION_MARKER") { govern = false; continue; }
				if (/all\s+external\s+links?/i.test(String(bi.text ?? ""))) { govern = true; continue; }
				if (govern && (bp?.tag === "video" || bp?.tag === "audio")) bi._extLinkButton = true;
			}
		}

		// WITHIN-ACTIVITY SUPERVISOR-NOTE SCAN, shared by the two different ways an activity box
		// can be opened (the ordinary CONTAINER_OPEN opener tag, and the case where an activity
		// is owned by a bundled interactive widget instead — the latter never had this
		// lookahead at all before this was added). Starting from item index `from`, this walks
		// FORWARD through the body items looking for a supervisor note that belongs inside THIS
		// activity, stopping at the activity's natural boundary. "Natural boundary" mirrors the
		// exact same rules `autoClose` uses elsewhere in this file: a section heading after some
		// content has already been seen, any of the configured activity_close_before directives
		// or tags, a closing tag, or a section marker. Items already claimed by some OTHER
		// bundled interactive widget are skipped over rather than treated as a boundary — a
		// supervisor note that comes after an embedded interactive still belongs to the
		// enclosing activity box (measured against the corpus: 50 such "mid-activity" notes vs.
		// 69 notes that sit directly after the activity opener with nothing in between — see
		// outputs/_measure_supervisor_boxgap.py). Returns the found note item, or null when there
		// isn't one; the caller consumes it immediately, in place, so the main loop below simply
		// skips over it when it reaches that position naturally.
		// Data flag: activity_wrapper.super_content.scan_within_activity
		// Env toggle: SUPSCAN_OFF (reverts to an earlier, narrower lookahead that only checked
		// the position IMMEDIATELY after the activity opener; SUPNOTE_OFF switches off the whole
		// supervisor-note-inside-activity mechanism, including this scan)
		const scanSupNote = (from) => {
			const scCfg = tpl.activity_wrapper.super_content;
			const scanCfg = scCfg?.scan_within_activity;
			if (!scCfg || scCfg.enabled === false || !scanCfg || scanCfg.enabled === false) return null;
			if (typeof process !== "undefined" && process.env
				&& (process.env.SUPNOTE_OFF || process.env.SUPSCAN_OFF)) return null;
			const ccfg = tpl.container_auto_close.activity_close_before;
			const hMax = (typeof process !== "undefined" && process.env && process.env.ACTHEAD_OFF)
				? (ccfg.rendered_heading_max_legacy ?? 3) : ccfg.rendered_heading_max;
			let seenContent = false;
			for (let k = from; k < bodyItems.length; k++) {
				const cand = bodyItems[k];
				if (cand.type === "black") {
					if ((cand.text ?? "").trim()) seenContent = true;
					continue;
				}
				if (cand.consumedBy !== undefined || cand._consumed) continue;
				if (cand.type !== "tag") { seenContent = true; continue; }
				const cp = cand.parse?.primary;
				if (cp?.tag === "supervisor note") return cand;
				const isTitle = (ccfg.title_heading_tags ?? []).includes(cp?.tag);
				const hh = isTitle ? null : renderedHeading(cp);
				if (hh !== null && hh <= hMax
					&& (!ccfg.heading_closes_only_after_content || seenContent)) return null;
				if (cp && (ccfg.directives.includes(cp.directive) || ccfg.tags.includes(cp.tag))) return null;
				if (cp?.directive === "CONTAINER_CLOSE" || cp?.directive === "PAGE_BOUNDARY"
					|| cp?.directive === "SECTION_MARKER") return null;
				seenContent = true;
			}
			return null;
		};

		// BLL PAIRING PRE-PASS: different writers order their intro supervisor note differently
		// relative to its section heading — sometimes BEFORE the heading (module BLL225 writes
		// "[supervisor note][Introduction][body]") and sometimes AFTER it (module BLL111 writes
		// "[Introduction][supervisor note][body]"). Whichever order the writer used, the
		// human-built output looks IDENTICAL either way: the heading gets its own row, followed
		// by a "row.supervisor" containing the note panel next to a paragraph. To make both
		// writer orderings converge on that same output, this pre-pass detects a note that comes
		// BEFORE its heading and swaps it to come AFTER instead, so the later pairing code
		// (further down, where items are actually emitted) only ever has to handle the
		// "heading-then-note" order.
		//
		// A "qualifying" heading here is either a rendered [H1]-[H3] (within
		// `max_heading_level`), or a mid-page [title bar]-family section marker such as the
		// "[Introduction]" alias (listed in `swap_heading_tags`). `firstActivityIdx` limits both
		// this pre-pass AND the later pairing logic to the part of the page BEFORE the first
		// activity box opens — a supervisor note that appears INSIDE an activity is handled by
		// entirely separate logic (`scanSupNote`, above). This shares its scope, its data flag,
		// and its environment toggle with the pairing logic itself:
		// Data flag: callouts.by_tag.'supervisor note'.pair_with_content
		// Env toggle: SUPPAIR_OFF
		let firstActivityIdx = -1;
		for (let k = 0; k < bodyItems.length; k++) {
			const p = bodyItems[k].type === "tag" ? bodyItems[k].parse?.primary : null;
			if (p?.tag === "activity" && p?.directive === "CONTAINER_OPEN") { firstActivityIdx = k; break; }
		}
		const pcPre = tpl.callouts.by_tag["supervisor note"]?.pair_with_content;
		const pairPreOn = pcPre && pcPre.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.SUPPAIR_OFF)
			&& (pcPre.subjects ?? []).some((s) => (run.moduleCode ?? "").startsWith(s));
		if (pairPreOn) {
			const end = firstActivityIdx < 0 ? bodyItems.length : firstActivityIdx;
			for (let k = 0; k < end; k++) {
				const s = bodyItems[k];
				if (s.type !== "tag" || s.parse?.primary?.tag !== "supervisor note"
					|| s.consumedBy !== undefined || s._consumed) continue;
				let a = k + 1;
				while (a < end && bodyItems[a].type === "black"
					&& !(bodyItems[a].text ?? "").trim()) a++;
				const H = a < end ? bodyItems[a] : null;
				const hp = H?.type === "tag" ? H.parse?.primary : null;
				const hLvl = renderedHeading(hp);
				const isSwapHeading = hp && (
					(hLvl !== null && hLvl <= (pcPre.max_heading_level ?? 3))
					|| ((pcPre.swap_heading_tags ?? []).includes(hp.tag)
						&& hp.directive === "SECTION_MARKER"));
				if (!isSwapHeading) continue;
				let b = a + 1;
				while (b < end && bodyItems[b].type === "black"
					&& !(bodyItems[b].text ?? "").trim()) b++;
				const B2 = b < end ? bodyItems[b] : null;
				if (!(B2 && B2.type === "tag" && B2.consumedBy === undefined && !B2._consumed
					&& (pcPre.body_tags ?? ["body"]).includes(B2.parse?.primary?.tag))) continue;
				bodyItems.splice(a, 1);      // lift the heading out …
				bodyItems.splice(k, 0, H);   // … and re-insert it before the note
				run.AddNote("info", "ContentConverter",
					`Page ${page.lessonLabel}: supervisor note swapped after its section heading (BLL pairing pre-pass).`);
				k = a;
			}
		}

		// [MTKquiz] ADJACENT WRITER-BUTTON ABSORB pre-pass (ROUND 232 — CL-0038):
		// pairs each mtk-quiz marker with the writer's own quiz button in its
		// neighbourhood so exactly ONE canonical button ships per quiz (gold's
		// form). See #mtkQuizPrepass below for the full story.
		this.#mtkQuizPrepass(bodyItems, bundles, tpl);

		for (let i = 0; i < bodyItems.length; i++) {
			const it = bodyItems[i];

			// A fundamentals PHASE boundary (produced earlier by the phase-text pre-pass): close
			// anything that messy quiz markup left open, then push the panel sentinel — read
			// later by the phase_text branch of PanelsBuilder.fundamentalsPanels, which wraps the
			// body into panels at each sentinel. A KINDED break (see the tag-anchored delimiter
			// handling above) picks which sentinel to push: kind "lesson" pushes the SSFUN
			// [LESSON]-style sentinel (which generates its own "<h3>Phase N</h3>" heading —
			// matching the SSFUN family's human-built form); anything else pushes the plain
			// phase_text sentinel (no generated heading).
			if (it.type === "phasebreak") {
				while (stack.length) emit(stack.pop().close);
				breakRow();
				// ROUND 266 (the level-pages dialect): the LEVEL ordinal becomes the
				// page's activity-number prefix — the human numbers the boxes it
				// invents around this family's task widgets 1A/1B/1C within the
				// first level (the r217 "fundamentals number by PHASE" follow-up,
				// derivable here because the level markers are explicit). Only the
				// level-pages dialect sets run._levelMenu, so every other
				// fundamentals family keeps its numberless pages exactly.
				if (run._levelMenu) {
					this.#pageLessonNumber = (typeof this.#pageLessonNumber === "number")
						? this.#pageLessonNumber + 1 : 1;
				}
				parts.push(it.kind === "lesson" ? FUND_LESSON_SENTINEL : FUND_PHASETEXT_SENTINEL);
				continue;
			}

			// INQUIRY CED: a captured `[Tab N]` crumb-list entry (flagged by
			// PanelsBuilder.detectInquiryCed) renders NOTHING in the body — its label text has
			// already been captured for the crumb-trail navigation instead. (On module CEDT404
			// this list sits in the body partition of the page; on CEDK101 it sits in the menu.)
			if (it._inquiryCrumb) continue;

			// ---- whitelisted Word comments → red note JUST BEFORE the element ----
			// Surface each anchored Creative-Services comment as a direct child of the body
			// content region, immediately before the element it is anchored to. One source block
			// can split into several output items, so a block's comments are only emitted once —
			// on the FIRST of those items that reaches this point.
			if (it.block && !commentedBlocks.has(it.block)) {
				commentedBlocks.add(it.block);
				const notes = NotesAndComments.commentNotes(it.block);
				if (notes.length) { breakRow(); for (const n of notes) parts.push(n); }
			}
			// Surface a Media List comment before the content element that links the same media
			// item (matched by URL, per the media-key matching set up above); placed at body
			// level, immediately before the box that displays that media.
			emitMediaComments(it);

			// ---- interactive ranges → ONE placeholder at range start -----
			if (it.consumedBy !== undefined) {
				// A supervisor note that was already hoisted into its activity's panel at the
				// moment the activity was OPENED (by super_content.scan_within_activity, above) has
				// already been fully rendered as part of that opening; simply skip over its own
				// turn in this loop (the older, simpler "note immediately follows the opener" case
				// jumps the loop index `i` past it and never reaches this branch at all).
				if (it.consumedBy === "activity-super-content") continue;
				// A "mode" opener (see activity_wrapper.mode_opener_merge, further down) has
				// already claimed this numbered opener and merged the two into one activity box:
				// the box is already OPEN, carrying this opener's number, with its title heading
				// already inside. So this opener does NOT open a second box and does NOT
				// auto-close anything — it only contributes its own lead text into the box that's
				// already open.
				if (it.consumedBy === "activity-mode-merge") {
					if (it.blackAfter && it.blackAfter.trim()) {
						emit(...actDeBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links)));
						markContent();
					}
					continue;
				}
				const bundle = bundles[it.consumedBy];
				// CED CONSUMED crumb-list: a `[tabs]` bundle whose `[Tab N]` members were claimed
				// as inquiry CRUMBS (by PanelsBuilder.detectInquiryCed) is suppressed entirely — it
				// should never render as its own widget. Its OPENER item reaches this point in the
				// loop BEFORE its members do (the members get dropped by the `_inquiryCrumb` skip
				// above), so this guard catches the opener here: mark the bundle as already
				// emitted and skip it, leaving only the "div.crumbs" navigation behind. Setting
				// env CEDCONSUMED_OFF empties out `suppressBundles`, so the widget renders exactly
				// as it would have without any of this CED handling.
				if (bundle && cedInq.suppressBundles && cedInq.suppressBundles.has(it.consumedBy)) {
					bundle._emitted = true;
					continue;
				}
				if (bundle && !bundle._emitted) {
					bundle._emitted = true;
					autoClose(it);
					// a new activity-owned (or numbered) bundle closes any
					// still-open activity first (bank's "(new [Activity N])"
					// absolute terminator; stops BLL146's 1E nesting in 1D)
					const isNewActivity = bundle.canonTag === "activity"
						|| bundle.activityOwner !== undefined
						|| bundle.activityId !== null;
					while (isNewActivity && stack.length
						&& stack[stack.length - 1].tag === "activity") {
						emit(stack.pop().close);
						run.AddNote("info", "ContentConverter",
							`Page ${page.lessonLabel}: open [activity] closed by the next activity's widget bundle.`);
						if (!stack.length) breakRow();
					}

					// Sometimes an interactive widget's OWN tag carries an activity number and type
					// together, e.g. "[Activity 1A drag and drop]" — that gives it an activityId, but
					// NO separate activity-opener tag of its own (there's no plain "[Activity 1A]"
					// elsewhere for it to be owned by). Even so, the human-built version still wraps
					// it in a numbered activity container. To reproduce that, this treats the
					// interactive tag ITSELF as the activity's owner; its title/instructions/data
					// stay INSIDE the un-built placeholder as usual.
					// Data flag: activity_wrapper.embedded_interactive_activity
					// Env toggle: EMBACT_OFF (reverts to a bare placeholder with no activity wrapper
					// around it at all)
					const eiaCfg = tpl.activity_wrapper.embedded_interactive_activity;
					const embeddedAct = !bundle.activityOwner && bundle.activityId != null
						&& eiaCfg && eiaCfg.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env.EMBACT_OFF)
						&& it.type === "tag" && it.parse?.tags?.some((t) => t.tag === "activity");
					// BILINGUAL bundle activity (module TRR102): in bilingual (reoMode) modules, the
					// scanner pass that reads the English|Māori tables tags this bundle with the
					// "Activity NX:"/"Ngohe NX:" row number it found (bundle.reoActivity) — but there
					// is NO real "[Activity]" tag item to point back to as its owner, because the
					// number came from a table row, not a writer tag. This is wrapped the same way
					// as the embedded-interactive case just above, using a SYNTHETIC (made-up) owner
					// object instead of a real one: it has no parsed tag data (so it contributes no
					// style modifiers), and — importantly — it produces NO lead text, because in the
					// human-built version the bilingual introduction heading/body renders as its OWN
					// separate section OUTSIDE the activity box, not as lead text inside it. The
					// ".interactive" CSS class is still forced on, based on the widget's TYPE, by the
					// same rule ActivitiesBuilder.activityOpen always applies for interactive widget
					// types.
					// Data flag: activity_wrapper.reo_bundle_activity   Env toggle: REOACT_OFF
					const reoActCfg = tpl.activity_wrapper.reo_bundle_activity;
					const reoAct = reoMode && bundle.reoActivity === true && bundle.activityId != null
						&& reoActCfg && reoActCfg.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env.REOACT_OFF);
					const reoOwner = reoAct
						? { type: "tag", parse: { tags: [], numbers: [], primary: null }, blackAfter: "" }
						: null;
					// STANDALONE TASK-WIDGET ACTIVITY BOX (round 217 — Chris's boundary audit,
					// 2026-07-12). A TASK-type interactive the writer authored with NO [Activity]
					// tag at all (AGH1001-01: "[Interactive] Drag and drop the products…" + the
					// data table) is still boxed by the human developer — an invented
					// `<div class="activity interactive" number="1B">` wrapping the instruction +
					// widget, numbered in the lesson's normal letter sequence. MEASURED corpus-wide
					// (outputs/_measure_standalone_boxing.py, gold-vs-Claude block containment):
					// standalone bundles whose content the gold puts inside an activity box —
					// dragAndDrop 0.97 (n=73 decided), unclassified 0.88 (163), multiChoiceQuiz
					// 0.89 (38), radioQuiz 0.88 (8), selfCheck 0.83 (6); the DISPLAY types
					// (accordion/carousel/speechBubble/flipCard/clickDrop/tabs/modal/hintSlider…)
					// measure 0.08–0.16 and stay bare. The ambiguous band (dropDown 0.57,
					// selectionBox 0.78, typing 0.60, slider, reorder) is deliberately NOT listed —
					// recorded as a follow-up needing a finer (group-level) discriminator. The box
					// takes the human's `activity interactive` form (force_interactive) and the
					// NEXT positional lesson letter (ActivitiesBuilder.activityOpen positionalId —
					// the gold NUMBERS its invented boxes in sequence with the tagged ones, which
					// is also why Claude's letters used to drift on such pages). The gold's own
					// box TITLE heading is human-authored (in no WT) — recorded C, not invented.
					// reoMode is excluded (bilingual bundles have their own reo_bundle_activity
					// path + placeholder surface). Data: activity_wrapper.standalone_widget_box
					// (enabled + types[] + force_interactive). Env toggle: ACTWRAP_OFF.
					const saCfg = tpl.activity_wrapper.standalone_widget_box;
					const saOn = saCfg && saCfg.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env.ACTWRAP_OFF)
						&& !reoMode && !bundle.activityOwner && bundle.activityId == null
						&& !embeddedAct && !reoAct
						// NUMBERED-LESSON pages only: the human NUMBERS every box it invents,
						// and on a page with no lesson number (single-file fundamentals /
						// overviews) the human numbers by PHASE (HPFUN201 1A/1B/2A/2B…) —
						// which this converter cannot yet derive. A numberless box is a shape
						// the gold never ships and it MIS-PAIRS against gold's numbered boxes
						// (the skeleton keeps the number attr; measured −15..−17pp on the
						// HPFUN overviews). Phase-scoped numbering = the recorded follow-up;
						// until then the rule asserts only where the number is derivable.
						&& this.#pageLessonNumber != null
						&& (saCfg.types ?? []).includes(bundle.type);
					const saOwner = saOn
						? { type: "tag", parse: { tags: [], numbers: [], primary: null }, blackAfter: "" }
						: null;
					// LEVEL-PAGES ID-LED TASK BUNDLE → ACTIVITY BOX (ROUND 266 — CHFUN01,
					// Chris's screenshot: "SEPARATE UNBUILT INTERACTIVE THAT IS INSIDE AN
					// ACTIVITY CONTAINER"). In the level-pages dialect the writer leads each
					// task widget with its own activity id + title ("[dropquiz] … 1A Check
					// your understanding"); the human wraps the widget in
					// `<div class="activity interactive" number="1A">` with the title as the
					// box's h3, renumbering the writer's ids (1A/3A/4A → 1A/1B/1C) in the
					// level's own letter sequence — the phase ordinal set at the phasebreak
					// above is the number prefix. Only run._levelMenu pages (the registry-
					// gated dialect) can enter this branch; rides LEVELPAGE_OFF.
					// Data: fundamentals_panels.level_pages.activity_box.
					const lvCfgBox = run._levelMenu ? (run._levelMenu.cfg?.activity_box ?? {}) : null;
					const lvLead = (lvCfgBox && lvCfgBox.enabled !== false
						&& !reoMode && !bundle.activityOwner && bundle.activityId == null
						&& !embeddedAct && !reoAct
						&& this.#pageLessonNumber != null)
						? String(it.blackAfter ?? "").trim()
							.match(new RegExp(lvCfgBox.id_lead_pattern ?? "^(\\d+[A-Z])\\s+(\\S.*)$"))
						: null;
					const lvOwner = lvLead
						? { type: "tag", parse: { tags: [], numbers: [], primary: null }, blackAfter: "" }
						: null;
					// lvOwner OUTRANKS the r217 generic box: both wrap the widget in the
					// same numbered `activity interactive` form, but the dialect's box
					// also carries the writer's OWN title heading (a task type like
					// radioQuiz can qualify for both — the titled form is the human's).
					const actOwner = bundle.activityOwner ?? (embeddedAct ? it : (reoOwner ?? lvOwner ?? saOwner));
					rowFor(actOwner ? "section" : "block");   // activity = own section row; inline widget flows
					if (actOwner) {
						// OSAI301 1A shape: render a REAL activity wrapper, its
						// title + lead [body] as activity-level content, then
						// the cv2 box (widget + data ONLY) nested inside — the
						// pre-activity body/video stayed as their own rows.
						// .interactive is forced when the bundle's widget type(s) are
						// in the measured "interactive task" set (data-driven; fixes the
						// circle-vs-triangle indicator — ENGS301 1A dragAndDrop).
						const interactiveTypes = new Set(tpl.activity_wrapper.interactive_widget_types ?? []);
						const forceInt = [bundle.type, ...(bundle.extraTypes ?? [])]
							.some((t) => interactiveTypes.has(t))
							// a round-217 SYNTHETIC standalone box is `activity interactive` by
							// construction — the box only exists because of the widget it wraps
							|| (actOwner === saOwner && saCfg?.force_interactive !== false)
							// … and so is a round-266 level-pages id-led box
							|| (actOwner === lvOwner && lvCfgBox?.force_interactive !== false);
						// A BUNDLE-OWNED activity (module BLL124, activities 2C/2D — the "interactive
						// captured right after the opener" case) used to have NO lookahead for a
						// supervisor note at all (its supervisorNote argument was hardcoded to null),
						// so any note attached to it — whether directly after the opener or further
						// inside — would auto-close the activity box early and end up rendered
						// standalone underneath it instead of inside the panel. This reuses the same
						// shared scan used elsewhere in this file (any member the scan finds is
						// marked consumedBy and skipped when the main loop later reaches it); bundles
						// owned by a bilingual (reo) activity are excluded, since bilingual notes
						// belong to their own separate handling.
						// Data flag: activity_wrapper.super_content.scan_within_activity
						// Env toggle: SUPSCAN_OFF
						const bSupNote = (bundle.activityOwner || embeddedAct) ? scanSupNote(i + 1) : null;
						if (bSupNote) nextRowClass = tpl.activity_wrapper.super_content.row_class ?? " supervisor";
						// A supervisor note's IN-SPAN payload (its own text, written directly inside
						// the red span rather than as separate black text after it) is rendered here,
						// in its original letter-casing, for the activity panel to use — because
						// ActivitiesBuilder itself has no access to the normaliser (#norm) needed to do
						// this rendering (see long_payload_as_content for the fuller explanation).
						if (bSupNote) bSupNote._payloadText = this.#norm.RenderText(bSupNote.text ?? "");
						emit(...ActivitiesBuilder.activityOpen(actOwner, stack, run, false, bundle.activityId, forceInt, bSupNote, this.#pageLessonNumber, this.#lessonLetterMap, actOwner === saOwner || actOwner === lvOwner));
						if (bSupNote) bSupNote.consumedBy = "activity-super-content";
						// ROUND 266 (level-pages id-led box): the writer's own lead title —
						// "1A Check your understanding" minus the id — is the box's heading
						// (the human's h3), emitted as the box's first content.
						if (actOwner === lvOwner && lvLead) {
							emit(Utils.FillTemplate(lvCfgBox.title_heading ?? "<h3>{title}</h3>",
								{ title: Utils.EscapeHtml(String(lvLead[2]).replace(/\*+/g, "").trim()) }));
						}
						// ROUND 229: actProse records whether this activity box emitted any PROSE
						// content (title heading / lead body / lead table) ahead of its widget —
						// the prose_interactive_rows split below only fires on a prose-carrying
						// box (a widget-only box keeps the single-col form, gold's own shape).
						let actProse = false;
						if (bundle.activityOwner) {
						// Lead content: the FIRST heading/text LINE is the activity title (<h3>);
						// the REST is BUFFERED and rendered as ONE ListsAndRuns.renderBlackText block so
						// consecutive bullets group into a single <ul> (OSAI501-02 Activity 2A:
						// the Benefit/Risk/Managing instruction list was splitting into THREE
						// separate <ul> — one per bullet — because each lead item rendered alone).
						// Joining is paragraph-safe: ListsAndRuns.renderBlackText re-splits on newlines, so
						// non-bullet paragraphs still emit as separate <p> exactly as before.
						let titleDone = false;
						let leadBuf = [];
						const flushLead = () => {
							// actDeBold is applied here because the bundle-owned activity's LEAD text (the
							// writer's own instruction block that comes BEFORE the un-built widget box —
							// this is the single biggest source of such text, 56 nodes on module ARFUN04
							// alone) counts as ordinary activity-region body text, and so is subject to the
							// same bold-stripping rule as any other activity body text. The widget box's
							// own internal member dump (#interactivePlaceholder) is a completely different,
							// deliberately raw, un-touched hand-off area, and is NOT run through actDeBold.
							if (leadBuf.length) { emit(...actDeBold(ListsAndRuns.renderBlackText(leadBuf.join("\n"), run))); leadBuf = []; actProse = true; }
						};
						const addLead = (raw) => {
							const text = (raw ?? "").trim();
							if (!text) return;
							if (!titleDone) {
								const nl = text.search(/\n/);
								const title = (nl >= 0 ? text.slice(0, nl) : text).replace(/\*/g, "").trim();
								const rest = nl >= 0 ? text.slice(nl + 1).trim() : "";
								if (title) { emit(`<h3>${ListsAndRuns.inlineMarkup(title)}</h3>`); titleDone = true; actProse = true; }
								if (rest) leadBuf.push(rest);
							} else {
								leadBuf.push(text);
							}
						};
						// the title can ride on the [activity] tag itself or the lead items
						const leadStream = [];
						if (bundle.activityOwner.blackAfter?.trim()) {
							leadStream.push({ type: "black", text: bundle.activityOwner.blackAfter });
						}
						for (const l of (bundle.activityLeadItems ?? [])) leadStream.push(l);
						for (const lead of leadStream) {
							if (lead.type === "table") { flushLead(); emit(TablesAndGrids.contentTable(lead.block, run, false, this.#norm)); titleDone = true; actProse = true; continue; }
							if (lead.type === "black") { addLead(lead.text); continue; }
							const lp = lead.parse.primary;
							if (lp && ["h1", "h2", "h3", "h4", "h5", "heading", "activity heading"].includes(lp.tag)) {
								addLead(this.#norm.RenderText(lead.text) || lead.blackAfter || "");
							} else if (lead.blackAfter?.trim()) {
								addLead(lead.blackAfter);
							}
						}
						flushLead();
						}
						// PROSE | INTERACTIVE INNER ROWS (ROUND 229 — Change Ledger CL-0048/CL-0036,
						// constraint 63; Chris's activity-pair kickoff). In the registry-listed
						// families the human closes the activity's PROSE row and gives the widget
						// its OWN inner row at the group's measured width (ENFUN gold, 77/96 boxes:
						// activity > row > col-12 [prose] + row > col-md-12 col-12 [widget] — the
						// exact ENFUN02 1D form). Fires only on a prose-carrying box (actProse) in
						// a module whose code starts with a registry prefix; everywhere else the
						// single-col flow is the gold-dominant same_col form (75.4%) and is kept
						// BY CONSTRUCTION. The registry is GENERATED, never hand-typed
						// (outputs/_measure_activity_inner_rows.py --gen). Data
						// activity_wrapper.prose_interactive_rows; env toggle ACTROWS_OFF reverts
						// to the single-col flow.
						const pirCfg = tpl.activity_wrapper.prose_interactive_rows;
						const pirKey = (pirCfg && pirCfg.enabled !== false && actProse
							&& !(typeof process !== "undefined" && process.env && process.env.ACTROWS_OFF))
							? (Object.keys(pirCfg.registry ?? {}).find((p) => (run.moduleCode ?? "").startsWith(p)) ?? null)
							: null;
						if (pirKey) {
							emit(pirCfg.prose_close);
							emit(Utils.FillTemplate(pirCfg.widget_row_open, { widgetCol: pirCfg.registry[pirKey].widget_col }));
						}
						// A bundle the CL-0038 pre-pass claimed as the quiz BUTTON and that holds
						// no real content skips its empty placeholder box — the canonical button
						// (emitted by the tail just below) replaces it (ROUND 232; see
						// #mtkQuizBundleThin).
						if (!this.#mtkQuizBundleThin(bundle)) emit(this.#interactivePlaceholder(bundle, run));
						// [MTKquiz] markers riding this bundle (captured member or opener co-tag)
						// ship their button + To Do note here, inside the still-open box
						// (ROUND 232 — CL-0038; see #mtkQuizBundleTail).
						emit(...this.#mtkQuizBundleTail(bundle, run, it));
						// A writer's go-to-journal [button] directly after the widget belongs
						// INSIDE this activity box (ROUND 239 — Dev-Feedback R2, B4; the
						// human's h4.goJournal sits inside the box; see #goJournalTail).
						emit(...this.#goJournalTail(bodyItems, i, run, bundle));
						// close the activity at the bundle's end (the
						// terminator that ended the widget — e.g. the [H3])
						emit(stack.pop().close);
						breakRow();
					} else {
						// An inline widget FLOWS into the current section row, per the row-grouping
						// rule set up earlier in this method; only the older, non-grouping rule gave it
						// its own row (via rowCfg.after) when row-grouping wasn't in effect.
						if (!this.#mtkQuizBundleThin(bundle)) emit(this.#interactivePlaceholder(bundle, run));
						emit(...this.#mtkQuizBundleTail(bundle, run, it));   // ROUND 232 — CL-0038 (see above)
						if (!rowCfg.flow_blocks && !stack.length && rowCfg.after.includes("interactive_placeholder")) breakRow();
					}
					// INQUIRY consumed-opener RECOVERY. Empty `[Tab N]` PANEL OPENERS that come
					// right after some other widget are often SWALLOWED by that widget's own
					// member-capturing scan, instead of being left alone to open a new panel — for
					// example, a trailing `[Tab N]` absorbed as the LAST member of an activity's
					// final modal on modules BLL150/BLL160/BLL170/BLL210, or absorbed by a carousel
					// on TWHA902. When that happens, the page never actually splits into the right
					// number of panels (it might build 2 panels instead of the human's 6-9). This
					// only runs once inquiry mode has been CONFIRMED (`inquiryMode` is computed
					// earlier, before this scanning step, so this doesn't change WHETHER inquiry mode
					// fires — only what happens once it has). For a NON-`[tabs]` bundle whose TRAILING
					// members are empty `[Tab N]` tags, this closes any open activity and pushes one
					// panel sentinel per swallowed opener — restoring the panel boundary the widget's
					// scan swallowed, WITHOUT un-claiming the tag from that widget (so nothing leaks)
					// and WITHOUT needing any change to the scanning code itself. A genuine `[tabs]`
					// widget is left alone (its `[Tab N]` members are legitimate parts of that widget
					// — modules ENGJ301 and XGF9003 are untouched by this); a module that never
					// triggers this recovery in the first place reaches this code unchanged (module
					// ENGJ402 is byte-identical with or without this).
					// Data flag: inquiry_tabs.recover_consumed_openers   Env toggle: INQRECOVER_OFF
					if (inquiryMode && bundle.type !== "tabs"
						&& inqCfg.recover_consumed_openers !== false
						&& !(typeof process !== "undefined" && process.env && process.env.INQRECOVER_OFF)) {
						let trailingOpeners = 0;
						const _mem = bundle.memberItems || [];
						for (let mi = _mem.length - 1; mi >= 0; mi--) {
							const _m = _mem[mi];
							if (isTabItem(_m) && !(_m.blackAfter || "").trim()) { trailingOpeners++; continue; }
							break;   // stop at the first non-(empty-tab) trailing member
						}
						if (trailingOpeners > 0) {
							// close any open activity at the panel boundary (mirrors the new-activity close)
							while (stack.length && stack[stack.length - 1].tag === "activity") {
								emit(stack.pop().close);
								if (!stack.length) breakRow();
							}
							breakRow();
							for (let t = 0; t < trailingOpeners; t++) parts.push(INQ_SENTINEL);
							pageLabelHold = "";   // a recovered TAB-opened panel carries no [page N] label to hold
						}
					}
				}
				this.#closeSpanWrap(stack, emit, breakRow);   // a span-wrap callout holds EXACTLY this widget — close it now
				continue;   // every other item in the range is inside the bundle
			}

			if (it.type === "table") {
				// THE XDLS900 NAV-LAYOUT TABLES (ROUND 226). A table claimed by the choice-page
				// tile build (_choiceLabelTable — the [Tab Nav Layout] one-column category list)
				// contributes its category names as the tile labels and renders nothing itself.
				// A nav-layout table that is NOT feeding a tile build (_tabNavTable on XDLS908's
				// standalone form; _stickyNavTable — the cross-module sticky-nav link list,
				// flagged by PageSplitter) is a site-navigation set-up spec, not page content:
				// the human drops it entirely (the sticky nav is a js/stickyNav.js include), so
				// it surfaces as ONE Designer/Developer To Do note instead of a raw dumped table.
				// Data flag: body_region.choice_page_tiles   Env toggle: TABNAVDROP_OFF
				// (the flags are only ever set while the feature is on, so no re-check needed)
				const _navClean = (c) => String(c ?? "")
					.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "")
					.replace(/\*\*/g, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
				if (it._choiceLabelTable && choiceTiles) {
					for (const row of (it.block.rows ?? [])) {
						const cell = (row ?? []).map(_navClean).find((c) => c);
						if (cell) choiceTiles.labels.push(cell);
					}
					continue;   // realised as the tile grid at the end of the page
				}
				if (it._tabNavTable || it._stickyNavTable) {
					const cpCfg = tpl.body_region.choice_page_tiles ?? {};
					const rows = (it.block.rows ?? [])
						.map((row) => (row ?? []).map(_navClean).filter(Boolean).join(" "))
						.filter(Boolean);
					emit(NotesAndComments.redFlag(Utils.FillTemplate(
						(it._stickyNavTable ? cpCfg.sticky_todo : cpCfg.tabnav_todo) ?? "Navigation set-up table: {items}",
						{ items: rows.join(" · "), labels: rows.join(", ") }), run, "todo"));
					continue;
				}
				autoClose(it);
				// A side ALERT box can be authored as a 1-cell (1x1) TABLE whose single cell leads with
				// a positional "[Alert box on right hand side]" tag; the human-built version turns
				// that into a proper "col > alert" callout, rather than letting it fall through to
				// the ordinary (and here, incorrect) leaking layout-grid table handling.
				// Data flag: body_region.alert_table   Env toggle: ALERTTBL_OFF
				const alertBox = stack.length ? null : this.#alertTable(it.block.rows ?? [], run);
				if (alertBox) {
					const atCfg = tpl.body_region.alert_table ?? {};
					const sidePairOn = (atCfg.side_pair ?? false) && alertBox.side
						&& !(typeof process !== "undefined" && process.env && process.env.ALERTPAIR_OFF);
					breakRow();
					if (sidePairOn) {
						// DEFER the positional alert — pair it as the col-md-4 right sibling of the
						// FOLLOWING content's col-md-8 row (the human-built version's same-row layout),
						// only actually attaching it once that following row closes (see breakRow above).
						// This gathers everything from the introduction through to the video into that
						// shared row before pairing happens.
						pendingSideAlert = alertBox.col; sideAlertSawMedia = false;
					} else {
						parts.push(alertBox.html); markContent();   // the alert renders in its own row
					}
					this.#closeSpanWrap(stack, emit, breakRow); continue;
				}
				// A LAYOUT-TABLE grid IS its own "row > col" structure already, so at the body
				// top level it is emitted DIRECTLY — not nested inside the default
				// "row > col-md-8" content wrapper — matching the human-built version's bare
				// "row > col" grid with no extra nesting level.
				//
				// BILINGUAL unfold: a reoTranslate English|Māori content table is unfolded into
				// interleaved <tag reo>/<tag eng> elements, inside one "row > col-md-8" wrapper of
				// its own (its OWN row, just like a plain grid), with any shared media emitted only
				// once. This falls through (returns null) for an ordinary, non-bilingual table.
				if (reoMode && !stack.length) {
					// KEYSTONE section grouping: a "[H1] N.M" opener groups the WHOLE section —
					// heading, reo/eng prose, the audioImage grid, and the widget together — into ONE
					// "row > col-md-8 > div.activity > row > col-12" nesting, matching the
					// human-built version's nesting exactly. This runs FIRST (before the other
					// per-table handlers below get a chance to fire) so the section can absorb its
					// own content tables and widget bundles as a whole.
					// Data flag: dual_language.section_grouping   Env toggle: REONEST_OFF
					const sec = BilingualBuilder.bilingualSection(bodyItems, i, run, bundles, this.#norm);
					if (sec) { breakRow(); parts.push(sec.html); markContent(); this.#closeSpanWrap(stack, emit, breakRow); i = sec.next - 1; continue; }
					const bil = BilingualBuilder.bilingualTable(it.block, run, this.#norm,
						it._reoModuleContent === true);
					if (bil) { breakRow(); parts.push(bil); markContent(); this.#closeSpanWrap(stack, emit, breakRow); continue; }
					// A bilingual CALLOUT container (whakataukī / alert / supervisor-note box).
					const cont = BilingualBuilder.bilingualContainer(it.block, run, this.#norm);
					if (cont) { breakRow(); parts.push(cont); markContent(); this.#closeSpanWrap(stack, emit, breakRow); continue; }
					// A bilingual ACTIVITY: GATHER the activity's marker table together with any
					// widget-spec/content tables that follow it (stopping at the next activity
					// marker, a bilingual content table, a callout, an item already claimed by some
					// other widget, or any non-table item) into ONE "div.activity[number]" — with
					// the unfolded reo/eng introduction plus any widget placeholders nested inside it.
					if (BilingualBuilder.isActivityMarker(it.block)) {
						const blocks = [it.block];
						let j = i + 1;
						while (j < bodyItems.length) {
							const nx = bodyItems[j];
							if (nx.type !== "table" || nx.consumedBy !== undefined || nx._consumed) break;
							if (BilingualBuilder.isActivityMarker(nx.block) || BilingualBuilder.bilingualHeader(nx.block) || BilingualBuilder.isCalloutTable(nx.block, this.#norm)) break;
							blocks.push(nx.block); nx._consumed = true; j++;
						}
						const act = BilingualBuilder.bilingualActivity(blocks, run, this.#norm);
						if (act) { breakRow(); parts.push(act); markContent(); this.#closeSpanWrap(stack, emit, breakRow); i = j - 1; continue; }
					}
					// A column-aligned IMAGE-row + AUDIO-row table is the phonics "audioImage" grid
					// (287 human-built divs of this exact shape were found in the corpus); build the
					// human's `row > col.paddingR > audioImage` structure directly, instead of an
					// un-built placeholder box (this structure is NOT collapsed down to a single
					// generic marker by the skeleton comparison tooling, so building the REAL
					// structure here genuinely improves the match, where a single placeholder would
					// not have).
					// Data flag: dual_language.audio_image   Env toggle: AUDIOIMG_OFF
					const aimg = BilingualBuilder.bilingualAudioImage(it.block);
					if (aimg) { breakRow(); parts.push(aimg); markContent(); this.#closeSpanWrap(stack, emit, breakRow); continue; }
					// A reoMode (bilingual) module's free-body table that all of the bilingual
					// handlers above have declined to handle is USUALLY genuinely an un-built
					// widget/spec table, which correctly falls through to the safe, un-built
					// "cv2-interactive" placeholder box below. BUT a CLEAN STRUCTURAL LAYOUT table
					// (an ordinary image|body side-by-side layout, where every cell simply leads with
					// a plain "[tag]") is NOT actually a widget at all — the human-built version
					// renders it as a plain "row > col" GRID, exactly like the ordinary (non-bilingual)
					// layout-table handling elsewhere in this file. Bilingual mode used to skip that
					// grid-building path entirely, so a module like ENGS201, page 01 — whose "Origin
					// stories" image|body table is just an ordinary layout table — ended up shipping
					// as the un-built placeholder box, LEAKING the literal text "[body]"/"[image]"
					// where real content should have been. This tries building the grid FIRST (using
					// the exact same detector the ordinary, non-bilingual path uses — it only accepts
					// a single-row, fully-tagged table, and bails out on anything that looks like a
					// real widget/spec/data table); if it isn't a clean layout table, this returns
					// null and the un-built placeholder is used as before.
					// Data flag: dual_language.reo_layout_table_grid   Env toggle: REOLTABLE_OFF
					breakRow();
					const reoGridOn = (dlCfg.reo_layout_table_grid?.enabled !== false)
						&& !(typeof process !== "undefined" && process.env && process.env.REOLTABLE_OFF);
					const reoGrid = reoGridOn ? TablesAndGrids.layoutTableGrid(it.block.rows ?? [], run, false, this.#norm, it.block.links ?? null) : null;
					// LEAK-SAFE: use the grid ONLY when it is clean. A grid cell whose text carries a
					// resolved [tag] somewhere in the MIDDLE of its text (the cell renderer only strips
					// a LEADING tag, not one buried mid-sentence) would leak that raw tag as VISIBLE
					// text on the page — whereas the un-built placeholder box is exempt from the
					// "leaked tag" detection used elsewhere, so it hid the same problem. So a grid that
					// still shows a resolved tag anywhere in it falls BACK to the placeholder instead:
					// this whole feature can therefore never make a leak WORSE, only fix one.
					if (reoGrid && !this.#htmlLeaksResolvedTag(reoGrid)) parts.push(reoGrid);
					else parts.push(`<div class="cv2-interactive bilingual-unbuilt">\n${TablesAndGrids.contentTable(it.block, run, true, this.#norm)}\n</div>`);
					markContent(); this.#closeSpanWrap(stack, emit, breakRow); continue;
				}
				// LEAK GUARD, generalising the SAME "never let the grid leak a raw tag" safety check
				// used just above for reoMode to the ORDINARY (non-bilingual) path too: a module can
				// carry the MTK house header WITHOUT actually being routed into bilingual/reoMode
				// handling (see the earlier note about the mtkFlag not being reliable proof of a
				// bilingual module on its own). On such a module, a free-body table whose rendered
				// HTML — whether a kept plain <table> OR a layout GRID — still shows a resolved [tag]
				// (a widget/media/structural cell tag the cell renderer had to leave as literal text,
				// including one buried in the MIDDLE of a cell that the cell renderer can't strip)
				// falls back to the EXACT SAME un-built placeholder form that would have been used had
				// the module gone through the bilingual/reoMode path — so this guard can never make an
				// existing leak worse, it can only prevent a new one from appearing (measured: this
				// single table/grid class accounts for the entire +84-occurrence inventory that this
				// guard un-masks).
				// Data flag: dual_language.mtk_leak_guard   Env toggle: MTKGUARD_OFF
				// (MTKREO_OFF reverts the entire mtkFlag-demotion mechanism this guard belongs to)
				const _lgCfg = dlCfg?.mtk_leak_guard;
				const _lgOn = !!run.mtkFlag && !reoMode && !!_lgCfg && _lgCfg.enabled !== false
					&& !(typeof process !== "undefined" && process.env
						&& (process.env.MTKGUARD_OFF || process.env.MTKREO_OFF));
				const _lgFallback = () => {
					breakRow();
					parts.push(`<div class="cv2-interactive bilingual-unbuilt">\n${TablesAndGrids.contentTable(it.block, run, true, this.#norm)}\n</div>`);
				};
				const grid = stack.length ? null : TablesAndGrids.layoutTableGrid(it.block.rows ?? [], run, false, this.#norm, it.block.links ?? null);
				if (grid) {
					if (_lgOn && this.#htmlLeaksResolvedTag(grid)) {
						_lgFallback();
					} else {
						breakRow();
						parts.push(grid);
					}
				} else {
					const tbl = TablesAndGrids.contentTable(it.block, run, false, this.#norm);
					if (_lgOn && this.#htmlLeaksResolvedTag(tbl)) {
						_lgFallback();
					} else {
						rowFor("block");
						emit(tbl);
					}
				}
				markContent();
				this.#closeSpanWrap(stack, emit, breakRow);   // a span-wrap callout holds EXACTLY this table — close it now
				continue;
			}

			if (it.type === "black") {
				rowFor("textRun");
				emit(...actDeBold(ListsAndRuns.renderBlackText(it.text, run, it.block?.links)));
				markContent();
				continue;
			}

			// ---- tag item: dispatch by directive class --------------------
			const parse = it.parse;
			const primary = parse.primary;

			// whole-span writer instruction (§5.16) — the entire red span is
			// the developer note; any black text after it is real content.
			// Red flags ride with their neighbouring content — never a break.
			if (!primary) {
				if (parse.class === "instruction") emit(NotesAndComments.redFlag(it.text, run, "cs"));
				if (it.blackAfter.trim()) { emit(...actDeBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links))); markContent(); }
				continue;
			}

			// BARE [Activity] RE-EMPHASIS MERGE: sometimes a bare "[Activity]" tag with no
			// number arrives while a NUMBERED activity is already open and already has content,
			// and its own opener tail was EMPTY — this is the writer simply re-marking, inside
			// prose, where the interactive widget sits within that SAME activity (seen on module
			// ENGC101, activity 2A: "...Tick the describing words"). Without special handling,
			// this would incorrectly produce a SECOND, numberless activity box, whereas the
			// human-built version keeps everything in the ONE numbered box. So this flows the
			// bare tag's lead text into the already-open box and suppresses the opener entirely
			// — this check MUST run before autoClose, because autoClose would otherwise close
			// the already-open activity as soon as it sees this new "[activity]" tag. The
			// `titledOpener` check below protects a DIFFERENT, unrelated case — a writer
			// deliberately starting a fresh, separately-titled activity (like "Dropbox",
			// "Reflection", or "Pick-a-task" sections) — from being wrongly merged in; the
			// keyword-exclusion list is an extra safety net on top of that check.
			// Data flag: activity_wrapper.bare_reemphasis_merge   Env toggle: REEMPH_OFF
			if (primary.tag === "activity" && primary.directive === "CONTAINER_OPEN"
				&& !it.parse.numbers[0] && it.consumedBy === undefined
				&& !((primary.remainder ?? "").trim()) && it.parse.tags.length === 1
				&& !((it.parse.free ?? "").trim())) {
				// TRULY-BARE [Activity] only — the red span is EXACTLY "[Activity]" with NO
				// text after the bracket (free empty), its lead carried as BLACK text
				// (ENGC101 "[Activity]🔴Which words..."). EXCLUDES a descriptive-label opener
				// whose label sits in the RED free text ("[activity] short answer box" /
				// "[activity] memory card game" — PHE1005) — those are interactive-TYPE
				// activities the human keeps as their own box, not a re-emphasis. Also
				// excludes bracket-remainder labels and multi-tag spans.
				const remCfg = tpl.activity_wrapper.bare_reemphasis_merge;
				const remOn = remCfg?.enabled
					&& !(typeof process !== "undefined" && process.env && process.env.REEMPH_OFF);
				const top = stack[stack.length - 1];
				// merge ONLY into a NUMBERED open activity with an empty-tail opener (ENGC101
				// 2A). top.id excludes a NUMBERLESS open box (ENGI203's bare-[Activity] chains,
				// which the human RENUMBERS as siblings, not merges); !top.titledOpener excludes
				// a self-titled opener (CEDO102 "[Activity 5C] Extra for Experts" -> Dropbox is a
				// new sibling, renumbered).
				const openAct = top && top.tag === "activity" && top.id && top.hasContent && !top.titledOpener;
				const lead = (it.blackAfter ?? "").trim().toLowerCase();
				const excluded = (remCfg?.exclude_keywords ?? []).some((k) => lead.startsWith(k));
				if (remOn && openAct && !excluded) {
					if (it.blackAfter.trim()) emit(...actDeBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links)));
					markContent();
					run.AddNote("info", "ContentConverter",
						`Page ${page.lessonLabel}: bare [activity] re-emphasis merged into the open numbered activity (no new box).`);
					continue;
				}
			}

			autoClose(it);

			switch (primary.directive) {
				case "ELEMENT": {
					// row kind: headings start (and may share) a row; plain
					// text-family elements behave as text runs; media and
					// everything else stand alone (data: body_region.row_rule)
					const h = renderedHeading(primary);
					// mid-doc [Title]/[Introduction] renders as a section
					// heading, so it row-groups like one
					rowFor(h !== null || primary.tag === "title bar" ? "heading"
						: (["body", "table", "list"].includes(primary.tag) ? "textRun" : "block"));
					// actDeBold is applied here because an element's own ATTACHED text (a media or
					// image item's blackAfter text, or gathered follower text like module ARFUN04's
					// "[Insert item #6]" class of caption) counts as ACTIVITY-region body text
					// whenever an activity box is currently open, so it goes through the same
					// bold-stripping rule as other activity content. The SEPARATE #element call
					// sites used by callout rendering (boxParts / same-block button absorption)
					// deliberately stay UN-wrapped by actDeBold — those live inside an alert-style
					// callout, which is allowed to keep its bold formatting.
					emit(...actDeBold(this.#element(it, bodyItems, i, stack, run)));
					// An mtk-quiz CO-TAG riding some other element ([H3]-primary etc. —
					// possible when a glued span's dropped primary recomputed to a
					// non-activity survivor) still ships its button + To Do note right
					// after that element (ROUND 232 — CL-0038; #mtkQuizEmit is
					// once-per-item, so an mtk-PRIMARY item already emitted above is a
					// no-op here).
					if ((it.parse?.tags ?? []).some((t) => t.tag === "mtk quiz")) {
						emit(...this.#mtkQuizEmit(it, run));
					}
					markContent();
					// SIDE-ALERT PAIRING: the intro media (video/image) flowing into the pending
					// alert's col-md-8 column COMPLETES that column — the next heading break will
					// then close the row with the alert attached (the human-built version stops the
					// col-md-8 column right after the intro video).
					if (pendingSideAlert && ["image", "video", "audio", "embed"].includes(primary.tag)) sideAlertSawMedia = true;
					// #element may have consumed following black items —
					// skip them (they were marked)
					while (bodyItems[i + 1]?._consumed) i++;
					break;
				}

				case "CONTAINER_OPEN": {
					if (primary.tag === "activity") {
						// CONSECUTIVE ACTIVITY OPENERS describe ONE box, not two. Writers pair a
						// layout/mode NOTE tag with the real numbered tag — HIS1008 "[Activity
						// Individual]" + "[Activity 1A] …", or the inverse CEDK "[Activity 1B]" +
						// "[Activity body] …". Both canonicalise to tag "activity", so the first opens
						// an EMPTY box that the second immediately auto-closes (CONTAINER_OPEN is a
						// close-before directive), spilling the content. Fix: when this opener has NO
						// content of its own AND the next non-blank item is ALSO an [activity] opener,
						// SUPPRESS this (note) half — the other opener makes the box; hand it this
						// opener's activity NUMBER if it is the one that carries it (so the box stays
						// numbered). Robust to either order and to the layout-word spelling.
						let j = i + 1;
						while (j < bodyItems.length && bodyItems[j].type === "black"
							&& !(bodyItems[j].text ?? "").trim()) j++;
						const nxt = bodyItems[j];
						const nextIsActivityOpener = nxt?.type === "tag"
							&& nxt.parse?.primary?.tag === "activity"
							&& nxt.parse?.primary?.directive === "CONTAINER_OPEN"
							&& nxt.consumedBy === undefined;
						const myId = it.parse.numbers[0]?.toUpperCase() ?? null;
						const nextId = nextIsActivityOpener ? (nxt.parse.numbers[0]?.toUpperCase() ?? null) : null;
						const myContent = (it.blackAfter ?? "").trim().length > 0;
						if (nextIsActivityOpener && !myContent && it.consumedBy === undefined && (myId || nextId)) {
							if (myId && !nextId) nxt._activityIdOverride = myId;   // carry the number forward
							run.AddNote("info", "ContentConverter",
								`Page ${page.lessonLabel}: layout-note [activity] opener merged into the adjacent numbered activity (no empty box).`);
							break;   // suppress this opener's box
						}
						// MODE-OPENER FORWARD MERGE (module HIS1004's family): an un-numbered activity
						// opener with no content of its own — a "[Activity individual]", "[Activity
						// embedded]", "[Activity body]", or bare "[Activity]" tag — is really just a
						// LAYOUT/MODE annotation describing the NUMBERED activity that comes after it,
						// even when the box's OWN title heading sits in between the two (HIS1004 writes
						// "[Activity individual] [H3] Which rights [Activity 1A]" — meaning ONE box,
						// numbered 1A, with the H3 as its title). The immediate re-emphasis merge above
						// only skips over BLANK lines when looking for what comes next; this extends
						// that same idea to also skip over the title heading(s) in between and adopt
						// the later numbered opener's id, opening ONE box right HERE so the heading ends
						// up inside it. The numbered opener that gets merged in is marked as consumed
						// ("activity-mode-merge") — it still contributes its own lead text into the
						// already-open box, but it does not open a second box and does not auto-close
						// anything. A DIFFERENT, unrelated writer convention — the XDLS family's
						// "[Activity]" tag with its number written as plain black text — is
						// automatically EXCLUDED from this merge, because its number ends up inside
						// `blackAfter`, which makes `myContent` true.
						// Data flag: activity_wrapper.mode_opener_merge   Env toggle: ACTMODEMERGE_OFF
						const momCfg = tpl.activity_wrapper.mode_opener_merge;
						const momOn = momCfg && momCfg.enabled !== false
							&& !(typeof process !== "undefined" && process.env && process.env.ACTMODEMERGE_OFF);
						if (momOn && !myId && !myContent && it.consumedBy === undefined) {
							const maxH = momCfg.max_intervening_headings ?? 1;
							const titleTags = tpl.container_auto_close.activity_close_before.title_heading_tags ?? [];
							let k = i + 1, headings = 0, target = null;
							while (k < bodyItems.length) {
								const c = bodyItems[k];
								if (c.type === "black") {
									if (!(c.text ?? "").trim()) { k++; continue; }
									break;   // real body text between the openers -> not a clean mode->title->numbered trio
								}
								if (c.type !== "tag" || c.consumedBy !== undefined) break;
								const cp = c.parse?.primary;
								if (!cp) break;
								// a NUMBERED activity opener -> the merge target
								if (cp.tag === "activity" && cp.directive === "CONTAINER_OPEN" && c.parse.numbers[0]) {
									target = c; break;
								}
								// the box's own title heading (rendered H1-H5 / [activity heading]) -> skip
								const isTitleH = titleTags.includes(cp.tag) || renderedHeading(cp) !== null;
								if (isTitleH && headings < maxH) { headings++; k++; continue; }
								break;   // anything else (interactive/section marker/another opener) ends the trio
							}
							if (target) {
								it._activityIdOverride = target.parse.numbers[0].toUpperCase();
								target.consumedBy = "activity-mode-merge";
								run.AddNote("info", "ContentConverter",
									`Page ${page.lessonLabel}: mode [activity] opener merged forward into numbered activity ${it._activityIdOverride} (title heading kept inside; no empty box).`);
							}
						}
						// A "[Supervisor note]" that appears immediately after this opener NESTS as the
						// activity's own super-content panel (matching the human-built version's
						// "activity super-content-button" box), instead of being treated as an ordinary
						// CONTAINER_OPEN directive that would auto-close the activity box early and
						// spill the following body text/image out into a loose, disconnected row below
						// it (this went wrong on module BLL241, page 2A).
						// Data flag: activity_wrapper.super_content   Env toggle: SUPNOTE_OFF
						const scCfg = tpl.activity_wrapper.super_content;
						let supNote = null, supNoteIdx = -1;
						if (scCfg && scCfg.enabled !== false
							&& !(typeof process !== "undefined" && process.env && process.env.SUPNOTE_OFF)) {
							let k2 = i + 1;
							while (k2 < bodyItems.length && bodyItems[k2].type === "black"
								&& !(bodyItems[k2].text ?? "").trim()) k2++;
							const nn = bodyItems[k2];
							if (nn && nn.type === "tag" && nn.parse?.primary?.tag === "supervisor note"
								&& nn.consumedBy === undefined) { supNote = nn; supNoteIdx = k2; }
							// EXTENDED WITHIN-ACTIVITY SCAN (module BLL225, page 2E): a writer will
							// sometimes place the supervisor note MID-activity instead of right at the
							// start — e.g. "[Activity][body][supervisor note][video][end activity]" — and
							// even then, the human-built version STILL hoists that note into the box's
							// panel as the FIRST child. The note found this way is consumed IN PLACE (the
							// loop index `i` is left unchanged, because the ordinary content sitting
							// between the opener and the note still needs to render normally); the main
							// loop simply skips over the note when it naturally arrives at it. This
							// reuses the same shared `scanSupNote` helper documented earlier in this
							// method, above the pre-passes.
							// Env toggle: SUPSCAN_OFF
							if (!supNote) supNote = scanSupNote(k2);
						}
						rowFor("section");   // an [Activity] opens its own section row
						// The row wrapping a supervisor-note activity carries the '.supervisor' class
						// (per the child-dictates-ancestor rule explained earlier — the frontend's
						// "reveal" JavaScript specifically looks for ".row.supervisor").
						if (supNote && scCfg) nextRowClass = scCfg.row_class ?? " supervisor";
						// The note's IN-SPAN payload (its own text, written directly inside the red
						// span) is rendered in its original letter-casing for the activity panel —
						// ActivitiesBuilder has no access to the normaliser (#norm) needed to do this
						// itself; see long_payload_as_content for the fuller explanation.
						if (supNote) supNote._payloadText = this.#norm.RenderText(supNote.text ?? "");
						emit(...ActivitiesBuilder.activityOpen(it, stack, run, true, it._activityIdOverride ?? null, false, supNote, this.#pageLessonNumber, this.#lessonLetterMap));
						// When the note sits immediately next to the opener, the loop index jumps
						// past it right away; when it was instead found by the lookahead scan
						// further down the item stream, the loop index is left in place and the
						// note is simply skipped over once the main loop naturally reaches it.
						if (supNote) { supNote.consumedBy = "activity-super-content"; if (supNoteIdx >= 0) i = supNoteIdx; }
						// An [Activity …] opener CARRYING the mtk-quiz co-tag ("[Activity 3C]
						// [MTKQuiz] [Tagged to …]", HPRE301; "[Activity 1A: MTK Quiz]", ARFUN02)
						// ships its quiz button + To Do note INSIDE the box it just opened
						// (ROUND 232 — CL-0038; suppressed to the note alone when the pre-pass
						// found the writer's own button/marker further into the box — the gold
						// position). See #mtkQuizEmit.
						if ((it.parse?.tags ?? []).some((t) => t.tag === "mtk quiz")) {
							emit(...this.#mtkQuizEmit(it, run));
						}
						break;
					}

					// own_row callouts (supervisor note) carry their OWN
					// row/col wrappers — they bypass the standard row
					// entirely (always strict; emitted complete)
					const defOwn = tpl.callouts.by_tag[primary.tag];
					if (defOwn?.own_row && !stack.length) {
						breakRow();
						headingHold = false;
						const boxParts = this.#calloutOpen(it, bodyItems, i, stack, run, false).filter(Boolean);
						// BLL-family SIDE-BY-SIDE PAIRING (module BLL225): the human-built version
						// anchors a non-activity supervisor note directly to the section paragraph it
						// annotates — ONE "row.supervisor" holding the note panel column FIRST, then the
						// content column second (measured against the corpus: 99 out of 101 paired
						// human-built sites belong to the BLL subject group; every other subject ships
						// the note as its own standalone row — a control comparison on module MXFL101,
						// which has the IDENTICAL Writers Template context, confirms it stays
						// standalone there). This is scoped to the BLL subject-code prefix, only applies
						// BEFORE the page's first "[Activity]" opener, and needs a "companion" — the
						// next unclaimed "[body]" element (if a bare black-text follower was already
						// gathered INTO the note's own panel by #calloutOpen, then there's no separate
						// companion to pair with, and this pairing correctly declines — nothing changes
						// in that case). When it fires, the box's closing HTML is re-opened back up to
						// the row level, and the companion paragraph is rendered as the sibling content
						// column (using a column CSS class that varies per subject series — e.g. BLL2
						// uses "paddingR").
						// Data flag: callouts.by_tag.<tag>.pair_with_content
						// Env toggle: SUPPAIR_OFF (reverts to the standalone row form)
						const pcCfg = defOwn.pair_with_content;
						const pairOn = pcCfg && pcCfg.enabled !== false
							&& !(typeof process !== "undefined" && process.env && process.env.SUPPAIR_OFF)
							&& (pcCfg.subjects ?? []).some((s) => (run.moduleCode ?? "").startsWith(s))
							&& (firstActivityIdx < 0 || i < firstActivityIdx);
						let pairedFwd = false;
						if (pairOn) {
							let j = i + 1;
							while (j < bodyItems.length && bodyItems[j].type === "black"
								&& !(bodyItems[j].text ?? "").trim()) j++;
							const comp = bodyItems[j];
							if (comp && comp.type === "tag" && comp.consumedBy === undefined
								&& !comp._consumed
								&& (pcCfg.body_tags ?? ["body"]).includes(comp.parse?.primary?.tag)) {
								const closeStr = boxParts.pop();
								const cut = closeStr.lastIndexOf("</div>");
								boxParts.push(closeStr.slice(0, cut).replace(/\s+$/, ""));
								const ser = ((run.moduleCode ?? "").match(/^[A-Z]+\d/) ?? [""])[0];
								boxParts.push((pcCfg.content_col_open_by_series ?? {})[ser]
									?? pcCfg.content_col_open);
								boxParts.push(...this.#element(comp, bodyItems, j, stack, run).filter(Boolean));
								boxParts.push(pcCfg.content_col_close ?? "</div>");
								boxParts.push(pcCfg.row_close ?? "</div>");
								comp._consumed = true;
								pairedFwd = true;
								run.AddNote("info", "ContentConverter",
									`Page ${page.lessonLabel}: supervisor note paired with its section paragraph (BLL family convention).`);
							}
						}
						// BLL1 h2-INSIDE pairing: on the BLL1 single-file phonics parent modules
						// (BLL130 through BLL160), each letter-team section opens with "[H1/H2] →
						// [Supervisor note] → [Activity]" and has NO companion "[body]" paragraph at
						// all — so the side-by-side pairing above declines (there's no companion to pair
						// with). In this shape, the human-built version instead pairs the note with the
						// section HEADING itself: ONE "row.supervisor" holding the panel column FIRST,
						// then a "paddingR" column holding ONLY the section heading (measured against the
						// corpus: 20 out of 20 of these "heading-inside" human sites belong to the BLL1
						// parent modules specifically; module BLL210, which belongs to the sibling BLL2
						// group, has 2 heading-preceded notes that the human instead leaves standalone —
						// so this is scoped to a specific list of series, not to the whole BLL family).
						// Because the heading's own row was already emitted just before the note broke
						// the row, `parts` at this point ends with exactly three entries — the row-open,
						// the heading element, and the row-close — so those three are popped back off and
						// the heading is re-emitted inside the pairing's content column instead (reusing
						// the same "un-close and re-open the row" trick used by the side-alert pairing
						// elsewhere in this file).
						// Data flag: callouts.by_tag.'supervisor note'.pair_with_heading
						// Env toggle: SUPPAIRH2_OFF
						const phCfg = defOwn.pair_with_heading;
						let foldedHeading = false;   // guards against the [page N]-label fold below double-applying on top of this heading fold
						const phOn = !pairedFwd && phCfg && phCfg.enabled !== false
							&& !(typeof process !== "undefined" && process.env && process.env.SUPPAIRH2_OFF)
							&& (phCfg.series ?? []).some((s) => (run.moduleCode ?? "").startsWith(s));
						if (phOn && parts.length >= 3
							&& parts[parts.length - 1] === tpl.body_region.content_row_close) {
							const hd = parts[parts.length - 2];
							const hm = /^<h([1-6])[\s>]/.exec(hd ?? "");
							const rowOpenStr = Utils.FillTemplate(tpl.body_region.content_row_open,
								{ contentColClass: tpl.body_region.content_col_class_default, rowClass: "" });
							if (hm && +hm[1] <= (phCfg.max_rendered_level ?? 3)
								&& new RegExp(`</h${hm[1]}>\\s*$`).test(hd)
								&& parts[parts.length - 3] === rowOpenStr) {
								parts.pop();                       // the heading row's close
								const headingHtml = parts.pop();   // the heading itself
								parts.pop();                       // the heading row's open
								const closeStr = boxParts.pop();
								const cut = closeStr.lastIndexOf("</div>");
								boxParts.push(closeStr.slice(0, cut).replace(/\s+$/, ""));
								boxParts.push(phCfg.content_col_open);
								boxParts.push(headingHtml);
								boxParts.push(phCfg.content_col_close ?? "</div>");
								boxParts.push(phCfg.row_close ?? "</div>");
								run.AddNote("info", "ContentConverter",
									`Page ${page.lessonLabel}: supervisor note paired with its section heading (BLL1 h2-inside convention).`);
								foldedHeading = true;
							}
						}
						// The [page N]-LABEL fold: on the BLL1 modules whose inquiry pages are
						// delimited by "[page N]" markers, a letter-team section can open with
						// "[page N] <label>" → "[Supervisor note]" → "[Activity]", with NO separate
						// heading ITEM at all (the crumb-trail label lives only in the page's separate
						// "[Tab N]" list) — so the heading fold just above has no heading row available
						// to pop. In this shape, the human-built version instead DERIVES its fold
						// heading from the page's own label: ONE "row.supervisor" holding the panel
						// column, plus a "paddingR" column holding that label rendered as a heading.
						// Measured against the corpus (outputs/_measure_pagelabel_fold.py): there are 9
						// labelled "[page N]+note" sites in total, all belonging to BLL1 modules; the
						// human renders the label as an in-panel heading on all 9 of them (its PRESENCE
						// is completely consistent), though only 7 of the 9 actually FOLD it into the
						// row this way (the other 2, on modules BLL140 page 2 and BLL170 page 4, have no
						// site-level difference in their Writers Template that would explain why they're
						// different, so they're folded through the same way as the rest for consistency
						// — a small, accepted, one-off editorial deviation). This only fires when BOTH
						// of the pairing attempts above have declined AND the very end of `parts` is
						// EXACTLY the still-empty panel sentinel (meaning the note would be the panel's
						// very first piece of content). The heading level is fixed at `writer_level: 2`
						// — meaning it enters the heading-emitting pipeline exactly as if the writer had
						// typed a genuine "[H2]" tag (going through the same digit + body-shift +
						// re-levelling logic as any other heading), so it lands at the SAME level as the
						// other, similarly-folded headings nearby and can never accidentally shift the
						// rank of some other, unrelated heading on the page.
						// Data flag: callouts.by_tag.'supervisor note'.fold_page_label
						// Env toggle: PAGEFOLD_OFF
						const plCfg = defOwn.fold_page_label;
						const plOn = !pairedFwd && !foldedHeading && plCfg && plCfg.enabled !== false
							&& !(typeof process !== "undefined" && process.env && process.env.PAGEFOLD_OFF)
							&& (plCfg.series ?? []).some((s) => (run.moduleCode ?? "").startsWith(s))
							&& !!pageLabelHold
							&& parts.length > 0 && parts[parts.length - 1] === INQ_SENTINEL;
						if (plOn) {
							const l2e = tpl.elements.heading.logical_to_element;
							const plReOn = (tpl.body_region?.heading_relevel?.enabled !== false)
								&& !(typeof process !== "undefined" && process.env && process.env.RELEVEL_OFF);
							const lvl = Math.min(Math.max((plCfg.writer_level ?? 2) + l2e.body_shift, 2),
								plReOn ? (l2e.relevel_headroom ?? 6) : 5);
							const closeStr = boxParts.pop();
							const cut = closeStr.lastIndexOf("</div>");
							boxParts.push(closeStr.slice(0, cut).replace(/\s+$/, ""));
							boxParts.push(plCfg.content_col_open);
							boxParts.push(Utils.FillTemplate(plCfg.heading_template ?? "<h{level}>{label}</h{level}>",
								{ level: lvl, label: ListsAndRuns.inlineMarkup(pageLabelHold) }));
							boxParts.push(plCfg.content_col_close ?? "</div>");
							boxParts.push(plCfg.row_close ?? "</div>");
							pageLabelHold = "";
							run.AddNote("info", "ContentConverter",
								`Page ${page.lessonLabel}: supervisor note paired with its [page N] label heading (BLL1 fold_page_label).`);
						}
						parts.push(...boxParts);
						while (bodyItems[i + 1]?._consumed) i++;
						break;
					}

					// FLOWING callouts (quote/thought): the human-built version renders these as plain,
					// specially-classed paragraphs INSIDE the surrounding section row (a page-opening
					// quote opens the row, and the introduction that follows simply FLOWS into it), NOT
					// as a self-contained box that gets its own row, the way an alert or important-note
					// callout does.
					const flowingCallout = (tpl.callouts.flowing_tags ?? ["quote", "thought"]).includes(primary.tag);
					rowFor(flowingCallout ? "block" : "section");   // boxed callout = own section row; quote flows
					// SIDE-ALERT SIDE-BY-SIDE BACKWARD PAIRING: the human-built version pairs a
					// side_column callout (an "alertActivity" box) as the RIGHT sibling of the content
					// column that immediately PRECEDES it, sharing ONE row — measured against the
					// corpus: 99 out of 100 sites across the 43 modules that use "[side alert]" pair
					// this way. `rowFor("section")` just above has already closed that preceding
					// content row, so at this point `parts` ends with the row's closing HTML (closing
					// both the col-md-8 column and the row itself). This code un-does that closing,
					// appends the alert's column as a sibling of the content column, and then re-closes
					// the row — the default col-md-8 content column already matches the human-built
					// version exactly, with no changes needed there. If there is no preceding content
					// row to pair with at all (e.g. the alert sits at the very start of the page, or two
					// alerts appear back-to-back), this falls back to giving the alert its own separate
					// row instead.
					// Data flag: callouts.side_column_backward_pair
					// Env toggle: SIDEPAIR_OFF (independent of SIDEALERT_OFF, which reverts the
					// side-column alert CLASS entirely, not just its pairing behaviour)
					const _sideDef = tpl.callouts.by_tag[primary.tag];
					const _sideAlertOff = typeof process !== "undefined" && process.env && process.env.SIDEALERT_OFF;
					const _sidePairOff = typeof process !== "undefined" && process.env && process.env.SIDEPAIR_OFF;
					const _sidePairOn = _sideDef && _sideDef.side_column
						&& (tpl.callouts.side_column_backward_pair ?? false)
						&& !_sidePairOff
						&& !(primary.tag === "side alert" && _sideAlertOff)
						&& !stack.length;
					if (_sidePairOn && parts.length
						&& parts[parts.length - 1] === tpl.body_region.content_row_close) {
						parts.pop();                                   // un-close the preceding content row
						parts.push("</div>");                          // re-close just the col-md-8 main column
						parts.push(this.#sideAlertCol(it, bodyItems, i, run, _sideDef));   // alert as right sibling
						parts.push("</div>");                          // close the shared row
						rowOpen = false;
						while (bodyItems[i + 1]?._consumed) i++;       // its strict text run was consumed
						break;
					}
					// callouts: STRICT by default (the callout holds only its
					// own content run — the OSAI201 over-nesting fix); a
					// writer's explicit [end X] ahead switches to SPAN mode.
					// STRUCTURED-CONTENT WRAP: a callout with no black text whose
					// content is a following TABLE/widget (the strict text-gather
					// would leave it EMPTY) spans to CONTAIN that content, bounded
					// at the next heading/section/page (OSGM501: [Alert] + a 2-col
					// image|text table). Measured: 18 modules have callout-then-table.
					const wrapStructured = this.#calloutWrapsStructured(it, bodyItems, i);
					const spans = this.#explicitCloseAhead(bodyItems, i, primary.tag) || wrapStructured;
					emit(...this.#calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured));
					if (!spans) {
						// strict BOXED callout: the box is already complete — fresh row next.
						// A FLOWING callout (quote/thought) does NOT break — the intro flows into its row.
						if (!flowingCallout && !stack.length) breakRow();
						// its following text run was consumed into the box
						while (bodyItems[i + 1]?._consumed) i++;
					}
					break;
				}

				case "CONTAINER_CLOSE": {
					if (stack.length) {
						const top = stack.pop();
						// EMPTY SPAN-WRAP KILL (ROUND 239 — Dev-Feedback R2, B1 part 2). A
						// span-mode callout opens its inner row>col-12 wrapper EAGERLY (the
						// content normally arrives via later items); when the writer's whole
						// content rode the span's own lead paragraph and the [end X] follows
						// immediately, that wrapper is still the LAST thing emitted — an
						// empty row>col-12 pair the human never ships (measured: Claude 70
						// pairs / 28 modules, gold 2). Detected exactly: the last emitted
						// part IS the remembered wrap-open string, so nothing ever flowed
						// in. The wrap open is popped and its close is stripped off the
						// box's close string; a box with ANY flowed content is untouched.
						// Data flag: callouts.drop_empty_span_wrap   Env toggle: EMPTYWRAP_OFF
						const _ewCfg = tpl.callouts.drop_empty_span_wrap;
						if (top.wrapOpen && _ewCfg && _ewCfg.enabled !== false
							&& !(typeof process !== "undefined" && process.env && process.env.EMPTYWRAP_OFF)
							&& parts.length && parts[parts.length - 1] === top.wrapOpen
							&& top.close.startsWith(top.wrapClose + "\n")) {
							parts.pop();
							emit(top.close.slice((top.wrapClose + "\n").length));
						} else {
							emit(top.close);
						}
						// content after a closed callout/activity starts a
						// fresh row (corpus convention — data knob)
						if (!stack.length && rowCfg.after.includes(
							top.tag === "activity" ? "activity_close" : "callout_close")) breakRow();
					} else {
						// close without an open: ignore gracefully + surface
						// (§5.15 — the writer omitted the opener, or a page
						// boundary already closed it)
						run.AddNote("info", "ContentConverter",
							`Page ${page.lessonLabel}: [${primary.tag}] had no open container — ignored.`);
					}
					if (it.blackAfter.trim()) emit(...actDeBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links)));
					break;
				}

				case "SECTION_MARKER": {
					// MID-document title-bar aliases ([Title]/[Introduction])
					// are headings, never section breaks (page-boundary rule
					// 4) — and a [Title] that only repeats the module name is
					// CONSUMED (the header h1 already shows it; gold standard
					// BLL146-0.0 renders just <h3>Introduction</h3>)
					if (primary.tag === "title bar") {
						let text = (this.#norm.RenderText(it.text) || it.blackAfter)
							.replace(/\*/g, "").trim();
						const foldT = (s) => Utils.Fold(s).replace(/\s+/g, "");
						const ftext = text ? foldT(text) : "";
						const repeatsTitle = ftext && (
							(this.#pageEnglishTitle && ftext === foldT(this.#pageEnglishTitle))
							// Also match the RAW, pre-prefix-strip "Module N - …" version of the title
							// (see #pageRawTitle above), so a mid-document alias that repeats THAT
							// wording still gets recognised and consumed, even after the "Module N -"
							// prefix has been stripped off the main title.
							|| (this.#pageRawTitle && ftext === foldT(this.#pageRawTitle)));
						if (repeatsTitle) break;   // consumed — already in the header
						if (!text) {
							const word = (primary.fragment ?? "").trim();
							text = word ? word.charAt(0).toUpperCase() + word.slice(1) : "";
						}
						if (text) {
							rowFor("heading");
							emit(`<h3>${ListsAndRuns.inlineMarkup(text)}</h3>`);
						}
						break;
					}
					// other region labels emit nothing themselves (no
					// comments — not a permitted use); content simply follows
					rowFor("block");
					if (it.blackAfter.trim()) emit(...actDeBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links)));
					break;
				}

				case "PAGE_BOUNDARY":
					// SSFUN fundamentals: a "[LESSON] FUNdamental Phase N" marker (kept in the item
					// stream when the whole module lives on one file/page) is actually a PANEL
					// boundary, not just an ordinary section break — push the phase sentinel here
					// (PanelsBuilder.fundamentalsPanels wraps the body into panels at each one).
					if (fundPanelMode && !stack.length && primary?.tag === "lesson") {
						breakRow();
						parts.push(FUND_LESSON_SENTINEL);
						break;
					}
					// INQUIRY CED [Page N]-split: a top-level `[page N]` opener is a PANEL boundary.
					// Close any still-open activity first (writers put the next panel's `[page N]`
					// directly after the previous panel's last activity, which has no explicit end
					// tag of its own — the same idiom seen in the empty-[Tab N]-opener recovery
					// elsewhere in this file), then push the panel sentinel (read by
					// PanelsBuilder.inquiryPanels in its page_split mode, which wraps the body into
					// panels at each one). A "[end page]" closer tag falls through to the ordinary
					// section-break path below instead.
					// Env toggle: CEDPAGE_OFF
					if (cedInquiryMode && primary?.tag === "page") {
						while (stack.length && stack[stack.length - 1].tag === "activity") {
							emit(stack.pop().close);
							if (!stack.length) breakRow();
						}
						if (!stack.length) {
							breakRow();
							parts.push(INQ_SENTINEL);
							pageLabelHold = "";   // CED panels never label-fold (they are not BLL1 modules)
							headingHold = false;
							break;
						}
					}
					// _bllInquiry HYBRID [page N] panel split (module BLL210): the BLL phonics
					// subject group usually authors each section as `[Tab N][Page N][H#]` together,
					// but SOME sections open on a `[Page N]` marker ALONE, with no empty `[Tab N]`
					// alongside it (seen on BLL210's "Long vowels"/"Silent e" sections). The ordinary
					// `_bllInquiry` panel split only reacted to `[Tab N]` (plus the consumed-opener
					// recovery elsewhere in this file), so a `[page N]`-alone section used to get
					// MERGED into the previous panel instead of starting its own, which then shifted
					// every LATER crumb label out of alignment too. Now a top-level `[page N]` ALSO
					// opens a panel on its own, with de-duplication so it can never double-split
					// either a `[Tab N][page N]` pair (already handled together) or a `[page N]` that
					// was already consumed by the opener-recovery logic: this skips whenever the
					// PREVIOUS body item was itself a tab-family opener or another page boundary.
					// Data flag: inquiry_tabs.bll_page_split   Env toggle: BLLPAGE_OFF
					// (the CED-family [Page N]-split is a separate, related mechanism, handled just
					// above this one)
					if (_bllInquiry && !cedInquiryMode && primary?.tag === "page"
						&& (inqCfg.bll_page_split?.enabled !== false)
						&& !(typeof process !== "undefined" && process.env && process.env.BLLPAGE_OFF)) {
						const _prev = bodyItems[i - 1];
						const _prevIsBoundary = !!_prev && _prev.type === "tag"
							&& (isTabItem(_prev)
								|| (_prev.parse?.primary?.directive === "PAGE_BOUNDARY" && /\bpage\b/i.test(_prev.parse?.primary?.tag || "")));
						if (!_prevIsBoundary) {
							while (stack.length && stack[stack.length - 1].tag === "activity") {
								emit(stack.pop().close);
								if (!stack.length) breakRow();
							}
							if (!stack.length) {
								breakRow();
								parts.push(INQ_SENTINEL);
								// Hold onto the [page N] LABEL for the fold_page_label branch further
								// up this method (a BLL1 section-opening supervisor note derives its
								// fold heading from this held value while the panel is still empty).
								pageLabelHold = (it.blackAfter || "").replace(/\*/g, "").trim();
								headingHold = false;
								break;
							}
						}
					}
					// single-file modules keep boundary tags in-stream as
					// section separations — a fresh row reads as the break
					breakRow();
					headingHold = false;
					break;

				case "INLINE":
					rowFor("textRun");
					emit(...this.#inline(it, run));
					markContent();
					break;

				case "SUBTAG":
					// THE XDLS900 CHOICE-PAGE + NAV-LAYOUT MARKERS (ROUND 226 — Chris's XDLS900
					// screenshot triage; population = EXACTLY XDLS902-906 + XDLS908, measured over
					// ALL 431 dirs by outputs/_detect_choicetiles.cjs). Three folded-text-gated
					// handlers, checked FIRST so the generic orphan-sub-tag red flag below never
					// fires for them:
					// (1) "[LESSON Choice page]" (parses primary "option" — the word Choice aliases
					//     to the option sub-tag) OPENS the tile build: the following [Tab Nav
					//     Layout …] marker + its ONE-column category table are claimed as the tile
					//     labels, and the grid renders at the end of the page (see #choicePageTiles).
					//     The opener's own label text is a navigation-page label the human drops
					//     (the r143/r163 page-label class), noted, never body content.
					// (2) A STANDALONE "[Tab Nav Layout …]" (no choice page — XDLS908's form) is a
					//     site-navigation set-up instruction: the marker is consumed and its table
					//     becomes a Designer/Developer To Do note (the human drops both).
					// (3) A bare "[Tab Nav]" repeat marker (re-leaked an "Orphan sub-tag [tab n]"
					//     flag on ~every XDLS90x page) is consumed — a layout REPEAT directive, not
					//     content; its bare [Sticky Nav] twin already parses to DROP. Matched on the
					//     span's own folded text, so a real orphaned [tab 1] sub-tag still flags.
					// Data flag: body_region.choice_page_tiles
					// Env toggles: CHOICETILES_OFF (1), TABNAVDROP_OFF (2 + 3)
					{
						const cpCfg = tpl.body_region.choice_page_tiles;
						if (cpCfg && cpCfg.enabled !== false) {
							const cpFold = (it.parse?.folded ?? "").trim();
							const tilesOn = !(typeof process !== "undefined" && process.env && process.env.CHOICETILES_OFF);
							const navDropOn = !(typeof process !== "undefined" && process.env && process.env.TABNAVDROP_OFF);
							if (it._choiceNavSpan) break;   // already claimed by the tile build
							if (tilesOn && new RegExp(cpCfg.opener_pattern ?? "^\\[\\s*lesson choice page\\s*\\]", "i").test(cpFold)) {
								choiceTiles = { cfg: cpCfg, labels: [] };
								// claim the [Tab Nav Layout …] marker + its label table (both directly
								// follow the opener; only genuinely BLANK items are skipped, so the
								// no-table dialect — XDLS902 — safely finds nothing and falls back to
								// the lesson titles)
								for (let j = i + 1; j < bodyItems.length; j++) {
									const nx = bodyItems[j];
									if (nx.type === "black" && !String(nx.text ?? "").trim()) continue;
									if (nx.type === "tag" && new RegExp(cpCfg.tab_layout_pattern ?? "^\\[\\s*tab nav layout\\b", "i")
										.test((nx.parse?.folded ?? "").trim())) {
										nx._choiceNavSpan = true;
										for (let t = j + 1; t < bodyItems.length; t++) {
											const nt = bodyItems[t];
											if (nt.type === "black" && !String(nt.text ?? "").trim()) continue;
											if (nt.type === "table") nt._choiceLabelTable = true;
											break;   // first non-blank item either IS the table or ends the claim
										}
									}
									break;   // judge by the first non-blank item only
								}
								if ((it.blackAfter || "").trim()) run.AddNote("info", "ContentConverter",
									`[LESSON Choice page] label "${it.blackAfter.trim()}" is a navigation-page label — dropped (the human-built pages never show it); the tile grid renders at the end of this page.`);
								break;
							}
							if (navDropOn && new RegExp(cpCfg.tab_layout_pattern ?? "^\\[\\s*tab nav layout\\b", "i").test(cpFold)) {
								// standalone nav-layout marker (XDLS908): consume + To-Do its table
								for (let t = i + 1; t < bodyItems.length; t++) {
									const nt = bodyItems[t];
									if (nt.type === "black" && !String(nt.text ?? "").trim()) continue;
									if (nt.type === "table") nt._tabNavTable = true;
									break;
								}
								break;
							}
							if (navDropOn && !(it.blackAfter || "").trim()
								&& (cpCfg.bare_marker_patterns ?? []).some((p) => new RegExp(p, "i").test(cpFold))) {
								break;   // bare [Tab Nav] repeat marker — consumed, renders nothing
							}
						}
					}
					// In FUNDAMENTALS mode, a top-level "[New tab]" sub-tag is actually a PANEL
					// boundary, not an orphaned, mis-structured tag: drop the usual RED FLAG
					// warning and push a top-level sentinel instead (the
					// PanelsBuilder.fundamentalsPanels post-pass splits the body into panels at
					// each one). This only applies at the TOP level (never inside an already-open
					// container), and uses a word-bounded "\btab\b" match so unrelated sub-tags
					// like "data table" never match by accident. Neither "[End tab]" nor
					// "[End FUNdamental]" ever reach this code path (verified against the corpus),
					// so only "[New tab]" itself opens a panel this way.
					if (fundPanelMode && !stack.length && /\btab\b/i.test(primary.tag || "")) {
						breakRow();
						parts.push(FUND_SENTINEL);
						if (it.blackAfter.trim()) emit(...actDeBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links)));
						break;
					}
					// A top-level INQUIRY EMPTY `[Tab N]` panel opener that is reached while an
					// ACTIVITY is still open closes that activity FIRST — writers put the next
					// panel's opener directly after the previous panel's last activity, which has no
					// explicit end tag of its own — so the opener correctly SPLITS the panel instead
					// of getting trapped inside the still-open activity (where the `!stack.length`
					// check below would otherwise be false) and leaking out as a spurious "orphan
					// tag" warning (seen on module BLL210's trailing opener, and on TWHA902's
					// heading-label panels). This only applies to EMPTY openers (a labelled
					// crumb-list entry is captured as a label regardless of what's on the stack), and
					// only ever closes an ACTIVITY (never a real container or callout box). Uses the
					// same `inquiryMode` gate and INQRECOVER_OFF toggle as the related recovery logic
					// elsewhere in this file.
					if (inquiryMode && isTabItem(it) && !(it.blackAfter || "").trim()
						&& inqCfg.recover_consumed_openers !== false
						&& !(typeof process !== "undefined" && process.env && process.env.INQRECOVER_OFF)
						&& stack.length && stack[stack.length - 1].tag === "activity") {
						while (stack.length && stack[stack.length - 1].tag === "activity") {
							emit(stack.pop().close);
							if (!stack.length) breakRow();
						}
					}
					// INQUIRY: a `[Tab N] <label>` list entry (one that also carries a label) simply
					// CAPTURES the crumb-trail label and renders nothing further; an EMPTY `[Tab N]`
					// (no label text) instead OPENS a new panel (a sentinel is pushed for it).
					if (inquiryMode && !stack.length && isTabItem(it)) {
						const n = (String(it.text).match(/tab\s*(\d+)/i) || [])[1];
						const label = (it.blackAfter || "").replace(/\*/g, "").trim();
						if (label) { if (n) inquiryLabels[n] = label; break; }
						// SYMMETRIC de-duplication for the BLL hybrid `[Tab N]`/`[page N]` boundary
						// (modules BLL210 and BLL130): writers order the pair EITHER as
						// `[Tab N][page N]` (BLL210's order) OR as `[page N][Tab N]` (BLL130's
						// order). The `[page N]` split handled above already opened the panel in
						// either case, so an empty `[Tab N]` immediately FOLLOWING a `[page N]`
						// boundary is redundant and must be treated as a no-op — without this check
						// the pair would double-split the panel (as seen on BLL130: 7 panels became
						// 13). Scoped to the `_bllInquiry` family and its own data flag.
						if (_bllInquiry && (inqCfg.bll_page_split?.enabled !== false)
							&& !(typeof process !== "undefined" && process.env && process.env.BLLPAGE_OFF)) {
							const _prevP = bodyItems[i - 1];
							if (_prevP && _prevP.type === "tag"
								&& _prevP.parse?.primary?.directive === "PAGE_BOUNDARY"
								&& /\bpage\b/i.test(_prevP.parse?.primary?.tag || "")) break;
						}
						breakRow();
						parts.push(INQ_SENTINEL);
						pageLabelHold = "";   // a tab-opened panel has no [page N] label to hold onto
						break;
					}
					// FREE-BODY [caption] → the human's captionText paragraph (ROUND 239 —
					// Dev-Feedback R2, B2; SCCH302-02's blood-under-the-microscope caption).
					// "caption" is an alias of the data-marker SUBTAG (its meaning INSIDE a
					// widget bundle — carousel/flipCard captions — is untouched: bundle
					// members never reach this orphan branch). A free-body [caption] is the
					// writer's image caption, which the human ships as
					// <p class="captionText">…</p> (gold ×545) — not an orphan-structure
					// red flag. The match is the EXACT bare bracket, so a caption marker
					// carrying extra instruction text still surfaces as a flag below.
					// Data flag: elements.caption_text   Env toggle: CAPTIONTEXT_OFF
					{
						const _capCfg = tpl.elements?.caption_text;
						if (_capCfg && _capCfg.enabled !== false
							&& !(typeof process !== "undefined" && process.env && process.env.CAPTIONTEXT_OFF)
							&& primary.tag === "data marker"
							&& new RegExp(_capCfg.match ?? "^\\[\\s*caption\\s*\\]\\s*$", "i")
								.test((it.parse?.folded ?? Utils.Fold(String(it.text ?? ""))).trim())
							&& it.blackAfter.trim()) {
							emit(...actDeBold([Utils.FillTemplate(_capCfg.template,
								{ text: ListsAndRuns.inlineMarkup(it.blackAfter.replace(/\*/g, "").trim()) })]));
							break;
						}
					}
					// a sub-tag outside any interactive = mis-structured
					// source: render its content, flag the orphan (surface,
					// never absorb)
					emit(NotesAndComments.redFlag(
						`Orphan sub-tag [${primary.tag}] outside an interactive — content kept below; check the source structure.`, run));
					if (it.blackAfter.trim()) emit(...actDeBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links)));
					break;

				case "INTERACTIVE":
					// defensive only — the scanner owns these ranges
					emit(NotesAndComments.redFlag(
						`Interactive [${primary.tag}] reached the converter unbundled — captured as a bare placeholder; report this case.`, run));
					break;

				case "DROP":
					// deliberate exclusions (sticky nav) — never emitted
					break;

				case "INLINE_FORMAT":
				default:
					if (it.blackAfter.trim()) emit(...actDeBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links)));
					break;
			}
		}

		// unclosed containers at page end: close them and say so
		while (stack.length) {
			const open = stack.pop();
			emit(open.close);
			run.AddNote("warn", "ContentConverter",
				`Page ${page.lessonLabel}: [${open.tag}] was never closed — closed at page end.`);
		}
		breakRow();
		// SIDE-ALERT PAIRING: if the page ended with a right-positioned alert STILL waiting to
		// be paired (no following content ever opened a row it could be attached to), emit it
		// as its own row instead, so it is never silently dropped from the output — this falls
		// back to the same plain "own-row alert" form used elsewhere for an alert that isn't
		// being paired with a content column.
		if (pendingSideAlert) { parts.push("<div class=\"row\">\n" + pendingSideAlert + "\n</div>"); pendingSideAlert = null; }
		// THE XDLS900 CHOICE-PAGE TILE GRID (ROUND 226): renders as the page's LAST body row
		// — the human-built pages place the choicePage row after all the introduction content
		// (verified XDLS902/903/906 golds). One tile per lesson, linking to that lesson's
		// GENERATED HTML file; iconType ships empty with one To Do note listing the tiles
		// (icon choice is editorial — gold itself carries "CS: review iconType" comments).
		if (choiceTiles) {
			const built = this.#choicePageTiles(run, choiceTiles);
			if (built) {
				parts.push(NotesAndComments.redFlag(Utils.FillTemplate(
					choiceTiles.cfg.icon_todo ?? "Choice-page tiles built with an empty iconType: {labels}",
					{ labels: built.labels.join(", ") }), run, "todo"));
				parts.push(built.html);
				markContent();
			}
			choiceTiles = null;
		}
		const body = parts;

		// ---- menu --------------------------------------------------------
		// The learning-design headers ("We are learning to:", "WALT", "I can:", and similar)
		// most often actually live inside #module-menu-content (the menu scaffold), not the body
		// — e.g. module AGH1004 renders "We are learning to:" as an "<h5>" inside the menu on
		// every lesson page — so the named-heading promotion (see #promoteNamedHeadings below)
		// also runs across the menu's HTML-string fields, not just the body
		// (MenuBuilder.buildMenu returns an OBJECT whose values are strings of pane HTML).
		const menu = MenuBuilder.buildMenu(menuItems, menuType, run, page, this.#norm);
		// The ENG-family two_col OVERVIEW menu deliberately keeps "We are learning:"/"I can:"
		// as plain "<p>" lead-in text (it does NOT promote them to headings), so the
		// named-heading promotion above is skipped for it entirely.
		const twoColCfg = DataService.Data.EmitTemplates.menu.two_col_li;
		const skipMenuPromo = (menu.engFamily && twoColCfg?.eng_family?.skip_named_promotion)
			|| (menu.bannerFamily && twoColCfg?.banner_family?.skip_named_promotion);
		if (!skipMenuPromo) {
			for (const k of ["tab1", "tab2", "content", "left", "right"]) {
				if (typeof menu[k] === "string" && menu[k]) menu[k] = this.#promoteNamedHeadings(menu[k], true);
			}
		}

		// LESSON-MENU REPEAT. A small, measured set of modules repeat the OVERVIEW curriculum
		// (Understand/Know/Do) menu VERBATIM on every lesson page's #module-menu-content;
		// without this, the converter only builds that menu once, on the overview, and leaves
		// every lesson page's menu EMPTY. For a module on the FLAGGED list below: stash the
		// overview's already-built menu (onto run.overviewMenu) and reuse it wherever a lesson
		// page's own menu would otherwise be empty. This has to be a PER-MODULE list because it
		// was proven NON-DERIVABLE from the source alone — module MXFL201 repeats the menu on
		// its lessons, but MXFL204 (which shares the same subject, phase, and "simplified"
		// menu-type, with input Writers Templates that look indistinguishable by any structural
		// rule) does NOT — so the only reliable signal is the human developer's own per-module
		// choice, recorded here as data rather than guessed at by the code. This can never
		// over-fire: it only acts on the modules explicitly listed, only when the lesson menu is
		// ALREADY empty, and never on a page whose menu type is "none".
		// Data flag: Emit_Templates.menu.lesson_repeats_overview {enabled, modules}
		// Env toggle: MENUREPEAT_OFF
		const lro = DataService.Data.EmitTemplates.menu?.lesson_repeats_overview;
		const menuRepeatOn = lro && lro.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.MENUREPEAT_OFF)
			&& Array.isArray(lro.modules) && lro.modules.includes(run.moduleCode);
		if (menuRepeatOn && menuType !== "none") {
			const paneKeys = ["tab1", "tab2", "content", "left", "right"];
			const isEmpty = (m) => !paneKeys.some((k) => typeof m[k] === "string" && m[k].trim());
			if (page.isOverview) {
				if (!isEmpty(menu)) run.overviewMenu = JSON.parse(JSON.stringify(menu));
			} else if (isEmpty(menu) && run.overviewMenu) {
				Object.assign(menu, JSON.parse(JSON.stringify(run.overviewMenu)));
			}
		}

		// THE 6-LEVEL PRECEDENCE CASCADE — live engine application. This lets a module's
		// overview menu inherit structural width decisions from the nearest previously-developed
		// SIBLING module (walking a 6-level fallback chain: doc-14 override, then series, phase,
		// subject-and-template, subject, then finally the whole corpus as a last resort) instead
		// of always using one hard-coded default. It is currently SHIPPED INERT — the data flag
		// "Precedence_Cascade.engine_inherit.enabled" is false, so the call below is a complete
		// no-op, meaning the output corpus is byte-for-byte identical whether or not this code
		// exists, and every protected quality gate holds automatically as a result (the same safe
		// "ship it turned off first" pattern used for the subject-parameters mechanism). Once
		// switched on (planned to happen gradually, one proven scope at a time), the overview
		// menu's curriculum column WIDTH would be GENERATED from that nearest sibling
		// (PrecedenceResolver, reading Module_Structure_Index.json) instead of the current
		// registry default; if no level of the cascade can decide, the current default is kept
		// and a gate-neutral advisory note (class "cv2-note") is added instead. The env toggle
		// INHERIT_OFF force-reverts this even if the data flag is somehow on. Measured impact if
		// enabled (see outputs/_measure_cascade_engine.py): +29 fixes / −4 regressions = +25 net
		// improvement on the skeleton-structure gate; because the menu region is scoped to the
		// page's "#header" section, ONLY that one gate is affected either way.
		// Data flag: Precedence_Cascade.engine_inherit
		if (page.isOverview && typeof PrecedenceResolver !== "undefined") {
			PrecedenceResolver.inheritMenu(menu, run.moduleCode);
		}

		// DOCUMENT-LEVEL heading re-levelling: the writer's own "[H?]" digit is essentially
		// noise — the human developer re-bases every page's body-heading outline to a
		// consistent "h3-at-the-top" hierarchy regardless of what number the writer typed.
		// Re-level the assembled body's FREE-BODY headings as a post-pass to match that.
		// THEN promote the named learning-design headers ("We are learning to", "Success
		// criteria", and similar fixed phrases) from plain "<p>" text up to a FIXED "<h5>"
		// heading level — this has to run AFTER re-levelling, so that fixed level survives the
		// rank-normalising step above instead of being renumbered along with everything else.
		// #dropNoteResidueBullets runs OUTERMOST (i.e. last, wrapping everything else): an
		// element that sits between an empty bullet and its attached developer note (e.g. a
		// heading that gets dropped or promoted by one of the passes below) can be removed by
		// those passes, so the empty-bullet/note adjacency this method looks for only fully
		// forms AFTER all of them have already run (seen on module ENGR301-03).
		// PanelsBuilder.fundamentalsPanels also runs OUTERMOST: it wraps the fully-assembled body
		// into "div.fundamentalsPanel" elements at each "[New tab]" sentinel position (or, if the
		// feature is switched off or there was nothing to split, it just strips any stray
		// sentinel back out — a sentinel marker itself must never leak into the final HTML).
		// #stripCloserResidue also runs OUTERMOST: it drops a leaked "[end X]" closer tag that
		// survived rendering as a lone, empty "<p>" (a closer directive renders nothing by
		// design, so any visible trace of one is residue, not content). This runs before
		// PanelsBuilder.inquiryPanels so that the inquiryActive check below (which compares
		// finalBody against bodyHtml) stays purely about whether the inquiry wrapping changed
		// anything, uncontaminated by unrelated residue-stripping.
		const bodyHtml = this.#stripCloserResidue(PanelsBuilder.fundamentalsPanels(
			this.#dropNoteResidueBullets(this.#alertTitleHeading(ActivitiesBuilder.activityInteractivePostpass(this.#promoteNamedHeadings(
				this.#relevelHeadings(body.filter(Boolean).join("\n")))))),
			{ on: fundPanelMode, sentinel: FUND_SENTINEL, lessonSentinel: FUND_LESSON_SENTINEL,
				phaseTextSentinel: FUND_PHASETEXT_SENTINEL, run,
				// ROUND 265: the level-pages dialect's nav/tile labels + registry row
				// (fundamentals_panels.level_pages; env LEVELPAGE_OFF)
				levelRow: lvInfo?.row, levelLabels: lvInfo?.labels }));   // "run" is passed through for the newTabNav registry lookup
		// INQUIRY-mode wrapping also runs OUTERMOST: it turns the assembled body into
		// "div.crumbs" + "div.inquiryPanel" elements at each "[Tab N]" sentinel position.
		// inquiryActive then tells SkeletonBuilder whether to emit the inquiry page's body
		// class and footer.
		const finalBody = PanelsBuilder.inquiryPanels(bodyHtml,
			{ on: inquiryMode, sentinel: INQ_SENTINEL, labels: inquiryLabels,
				cedMode: cedInquiryMode, cedLabels: cedInq.labels, headingLabel: _headingLabelOn });
		const inquiryActive = (inquiryMode || cedInquiryMode) && finalBody !== bodyHtml;
		// CED firing flags the fixed inquiry footer-nav shell (a single-file CED page has no
		// registry footer links of its own, so SkeletonBuilder would otherwise emit an empty
		// #footer). Scoped specifically to CED so the BLL family's footers stay byte-unchanged.
		return { bodyHtml: finalBody, menu, titleBar, inquiryActive,
			cedInquiry: cedInquiryMode && finalBody !== bodyHtml };
	};

	/**
	 * NAMED LEARNING-DESIGN HEADING promotion — a post-pass run on the assembled body
	 * HTML, AFTER #relevelHeadings has already run.
	 *
	 * WHAT IT DOES:
	 * Te Kura's own learning-design phrases — "We are learning to", "You will show your
	 * understanding by", "Success criteria", "Learning intentions", "How will I know if
	 * I've learned it?" — form a CLOSED, recognisable vocabulary that the human developer
	 * always renders as a HEADING, even when the writer left them as plain, untagged black
	 * text in the source document (which the converter would otherwise just render as an
	 * ordinary "<p>" paragraph). This method promotes any FREE-BODY "<p>" (one that is NOT
	 * inside an interactive-widget subtree) whose folded text EXACTLY matches one of these
	 * known phrases up to a "<h{level}>" heading.
	 *
	 * WHY IT'S SAFE (AND WHY A GENERIC VERSION WAS REJECTED):
	 * A generic "any bold line becomes a heading" rule was tried and rejected, because
	 * which arbitrary phrases get bolded-into-a-heading varies by individual human
	 * developer — there's no reliable pattern to that. But THESE named phrases are
	 * different: they are a fixed, closed list that is consistently rendered as a heading
	 * across the whole corpus, so promoting them is a genuinely derivable rule rather than
	 * a guess. The match requires the folded text of the WHOLE paragraph to equal a known
	 * phrase exactly (not just contain it), which avoids the earlier false-positive problem
	 * of an ordinary body sentence that merely happens to start with similar wording.
	 * Measured net effect across matched pairs: 142 wins (human uses a heading, Claude was
	 * using a plain paragraph) vs 26 losses (human actually kept it as a paragraph) = a net
	 * +116 improvement.
	 *
	 * GATE SAFETY: changing a tag from "<p>" to "<h*>" never alters the surrounding
	 * row/column/activity wrapper structure, so this change is invisible to the structural
	 * comparison gates and only affects the more detailed skeleton-match gate.
	 *
	 * Data flag: body_region.named_headings
	 * Env toggle: NAMEDH_OFF (for A/B comparison against the pre-promotion behaviour)
	 */
	static #promoteNamedHeadings(html, isMenu = false) {
		const cfg = DataService.Data.EmitTemplates.body_region?.named_headings;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.NAMEDH_OFF) return html;
		const level = cfg.level ?? 5;
		const phrases = new Set(cfg.phrases ?? []);
		// MENU LEAD-IN CONDITIONAL promotion. The lesson-menu lead-in labels ("We are
		// learning:" / "I can:" / "We are learning about:") fold down to "we are learning" or
		// "i can" — NOT "we are learning TO" — so they never matched the exact phrase list
		// above, and Claude was emitting a plain "<p>" where the human developer uses a
		// heading ("<h5>"). However, the human actually KEEPS these as plain "<p>" text when
		// they appear as a SECONDARY lead-in directly UNDER a learning-design PARENT heading
		// (for example "Learning Intentions" as the heading, followed by "We are learning:" as
		// its lead-in line) — only the first, standalone case should be promoted. The
		// discriminator below (measured against real human output) is: promote a lead-in
		// UNLESS it is immediately preceded by another learning-design label with no bullet
		// list in between (in that case it's the second half of a heading-plus-lead-in pair,
		// and stays "<p>"). This whole lead-in promotion is MENU-ONLY — in the body, these same
		// phrases are ordinary page content and are never promoted — and the ENG-family
		// two_col menus already skip this promotion entirely (handled elsewhere).
		const lcfg = DataService.Data.EmitTemplates.body_region?.menu_lead_in_headings;
		const leadOn = isMenu && lcfg && lcfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.MENULEADIN_OFF);
		const leadPhrases = leadOn ? new Set(lcfg.phrases ?? []) : new Set();
		const ldLabels = leadOn ? new Set(lcfg.ld_labels ?? []) : new Set();
		const leadLevel = lcfg?.level ?? level;
		if (!phrases.size && !leadPhrases.size) return html;
		const skip = new Set(cfg.skip_classes
			?? DataService.Data.EmitTemplates.body_region?.heading_relevel?.skip_classes ?? []);
		const fold = (s) => s.replace(/<[^>]+>/g, " ").replace(/&[a-z]+;/gi, " ")
			.toLowerCase().replace(/[‘’]/g, "'")
			.replace(/[^a-z0-9' ]+/g, " ").replace(/\s+/g, " ").trim();
		const widget = this.#widgetRanges(html, skip);
		const inWidget = (pos) => widget.some(([a, b]) => pos >= a && pos < b);
		// a conditional lead-in is a SUB-lead-in (keep <p>) iff the nearest preceding <h*>/<p>
		// element is itself an LD label AND no bullet list intervenes (bullets = a fresh group).
		const precededByLabel = (off) => {
			const before = html.slice(0, off);
			let last = null, re = /<(h[1-6]|p)\b[^>]*>([\s\S]*?)<\/\1>/gi, mm;
			while ((mm = re.exec(before)) !== null) last = mm;
			if (!last) return false;
			const tail = before.slice(last.index + last[0].length);
			if (/<li\b|<\/li>|<ul\b|<\/ul>/i.test(tail)) return false;   // bullets → fresh group
			return ldLabels.has(fold(last[2]));
		};
		return html.replace(/<p\b[^>]*>([\s\S]*?)<\/p>/gi, (m, inner, off) => {
			if (inWidget(off)) return m;
			const f = fold(inner);
			if (phrases.has(f)) return `<h${level}>${inner}</h${level}>`;
			if (leadPhrases.has(f) && !precededByLabel(off)) return `<h${leadLevel}>${inner}</h${leadLevel}>`;
			return m;
		});
	};

	/**
	 * ALERT-TITLE heading. An "[alert]" callout box whose FIRST content line is a SHORT TITLE
	 * (for example "Safety message" or "Key points from today's lesson:") followed by more
	 * body text underneath it is rendered by the human developer as an inner HEADING
	 * ("<h4>"), but the converter used to just leave it as an ordinary "<p>" paragraph. This
	 * is a post-pass (run AFTER heading re-levelling, the same way #promoteNamedHeadings is):
	 * it promotes the FIRST "<p>" found inside a ".alert" box up to "<h{level}>" whenever its
	 * text is short enough (at or under max_title_chars characters) AND there is a FOLLOWING
	 * block of content after it (the "<[^/]" pattern below checks for that — an alert box
	 * containing only ONE paragraph and nothing else is just ordinary body text, so it is
	 * left untouched). Measured net effect: +592 improvement (650 wins vs 58 losses) across
	 * the 2,190 human-built alert boxes measured, with "<h4>" being the dominant level used
	 * (752 of them). This is GATE-SAFE — changing a "<p>" to an "<h4>" never alters the
	 * surrounding row/column wrapper structure, so the structural-comparison gates are
	 * unaffected by it.
	 * Data flag: body_region.alert_title_heading
	 * Env toggle: ALERTH_OFF
	 */
	static #alertTitleHeading(html) {
		const cfg = DataService.Data.EmitTemplates.body_region?.alert_title_heading;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.ALERTH_OFF) return html;
		const level = cfg.level ?? 4;
		const maxLen = cfg.max_title_chars ?? 45;
		// first <p> inside a .alert (optionally inside its row>col), promoted ONLY when a
		// following block tag exists after it (`\s*<[^/]` — a closing </div> = the only block).
		const re = /(<div class="alert[^"]*">\s*(?:<div class="row">\s*<div class="col[^"]*">\s*)?)<p\b[^>]*>([\s\S]*?)<\/p>(\s*<[^/])/gi;
		return html.replace(re, (full, pre, inner, after) => {
			const text = inner.replace(/<[^>]+>/g, " ").replace(/&[a-z]+;/gi, " ").trim();
			if (!text || text.length > maxLen) return full;
			return `${pre}<h${level}>${inner}</h${level}>${after}`;
		});
	};

	/**
	 * Char ranges [start,end] of every widget-subtree div (a div/section whose
	 * class is in `skip`), depth-balanced. Shared by the named-heading promotion
	 * to keep its <p>→heading rewrite OUT of built-widget subtrees (same protection
	 * the #relevelHeadings walk applies to free-body headings).
	 */
	static #widgetRanges(html, skip) {
		const ranges = [];
		const re = /<(\/?)(?:div|section)\b([^>]*)>/gi;
		let depth = 0;
		const stack = [];
		let m;
		while ((m = re.exec(html))) {
			if (m[1] === "/") {
				if (stack.length && stack[stack.length - 1].depth === depth) {
					ranges.push([stack.pop().start, m.index + m[0].length]);
				}
				depth--;
			} else {
				depth++;
				const cls = (m[2].match(/class="([^"]*)"/i)?.[1] ?? "").split(/\s+/);
				if (cls.some((c) => skip.has(c))) stack.push({ depth, start: m.index });
			}
		}
		return ranges;
	};

	/**
	 * DOCUMENT-LEVEL heading re-levelling — a post-pass on the assembled #body HTML.
	 *
	 * THE FINDING: human developers largely ignore the writer's own "[H?]" digit and
	 * instead re-base EVERY page's body-heading outline to a consistent, page-relative
	 * hierarchy that starts at h3 (measured: 71% of human pages start their body at h3, with
	 * body headings collapsing down to a h3 > h4 > h5 structure). In other words, the
	 * writer's heading-level TAG in the source document is unreliable noise — what actually
	 * matters is the human's consistent OUTPUT convention, which is invisible if you look at
	 * headings one at a time but becomes clear once you look at a whole document's heading
	 * OUTLINE together. So this method re-levels by the page's heading outline rather than by
	 * the writer's tag: it takes the page's DISTINCT free-body heading levels, sorts them, and
	 * maps them onto base_level, base_level+1, base_level+2, and so on (clamped at
	 * max_level) — essentially a rank normalisation of whatever levels are actually present.
	 * Measured improvement: matching just "writer's level + 1" got 46.2% of text-matched
	 * headings right; this rank-based approach gets 57.5% right.
	 *
	 * SCOPE: this only touches FREE-BODY headings (h2 through h5) — any heading that sits
	 * INSIDE an interactive-widget subtree (see skip_classes: the un-built placeholder class
	 * plus every built-widget's own class) is deliberately left untouched, so that the widget
	 * verifiers and each widget's own internal heading conventions stay protected from this
	 * page-wide re-levelling. This is GATE-SAFE — changing a heading's LEVEL never changes the
	 * surrounding row/column/activity wrapper structure, so the structural-comparison gates
	 * are unaffected; only the more detailed heading-level-match measurement improves.
	 * Data flag: body_region.heading_relevel.enabled
	 * Env toggle: RELEVEL_OFF (for A/B comparison)
	 */
	static #relevelHeadings(html) {
		const cfg = DataService.Data.EmitTemplates.body_region?.heading_relevel;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.RELEVEL_OFF) return html;
		const base = cfg.base_level ?? 3;
		const maxL = cfg.max_level ?? 5;
		const skip = new Set(cfg.skip_classes ?? []);
		// ACTIVITY-ANCHOR EXCLUSION. An activity's own title heading is always emitted at a
		// FIXED level (h3 — the top content-section level), whereas an ordinary free-body
		// "[H#]" heading gets its level from the writer's digit plus a body-wide shift. This
		// creates a problem: a writer's "[H3]" SECTION heading that is meant to be a PEER of
		// the activities (sitting alongside them, not inside them) would end up rendered one
		// level too deep — for example, module OSAI401-01: the human renders "[H3] Types of
		// AI" at h3 (a peer of the activity titles) and "[H4]" at h4, but without this
		// exclusion the converter would push them down to h4/h5, because the activity's fixed
		// h3 was occupying the base rank in the re-level pool ahead of them. The fix is to
		// treat activity subtrees the same way widget subtrees are treated here (excluded from
		// both the pool-building and the rewrite), so the free-body "[H#]" outline ranks from
		// the base level entirely on its own — the activity titles keep their fixed h3, and
		// the page's top-level "[H#]" heading aligns alongside it as intended. This is
		// SELF-SCOPING: it only changes a page's output when an activity heading would
		// otherwise have been the SHALLOWEST anchor in the pool; if a genuine free-body h3
		// (or a "[H2]" that already maps to h3) already holds the base rank, nothing changes.
		// Env toggle: RELEVELACT_OFF (reverts to the un-excluded behaviour)
		if (!(typeof process !== "undefined" && process.env && process.env.RELEVELACT_OFF))
			for (const c of (cfg.activity_anchor_classes ?? [])) skip.add(c);
		// SUPERVISOR-NOTE ANCHOR EXCLUSION. The supervisor-note callout box carries its own
		// fixed "<h3>Supervisor note</h3>" label inside its "super-content-button" wrapper.
		// That label is not really a free-body section heading, but without this exclusion it
		// would still PIN the re-level base rank at h3, which meant the page's genuine "[H3]"
		// section headings (writer digit plus the usual body shift) could no longer normalise
		// back down to h3 as they should (seen on module ENGC101-02's "Conversations"
		// heading). The fix is the same as the activity-anchor exclusion above: skip this box
		// entirely, the same way a widget subtree is skipped.
		// Env toggle: SUPHEAD_OFF (reverts to the un-excluded behaviour)
		if (!(typeof process !== "undefined" && process.env && process.env.SUPHEAD_OFF))
			for (const c of (cfg.supervisor_skip_classes ?? [])) skip.add(c);
		// h[2-6]: a writer [H5] is emitted at the intermediate h6 when re-levelling is active
		// (one extra level of headroom so [H4] vs [H5] stay DISTINCT through the body clamp);
		// the rank below normalises every level back into base..max_level (h3..h5).
		// FIXED-LEVEL HEADING CLASSES (ROUND 245 — Chris, the SCCH302 developer
		// error log, "goJournal heading level is inconsistent").
		//
		// A few headings are TEMPLATED chrome rather than part of the writer's
		// document outline: the converter emits them at a fixed level with a
		// fixed class. `<h4 class="goJournal">Go to your journal</h4>` is the
		// clearest case — the human gold ships it at h4 **568 times out of 568,
		// 100%**, whether it sits inside an activity box or stands alone. But
		// because it looked like an ordinary free-body heading it joined the
		// re-level POOL and then got RE-RANKED with everything else, so Claude
		// shipped 110 at h3 and 8 at h5 (of 835). Being in the pool is doubly
		// wrong: it also displaced the writer's real headings around it.
		//
		// A heading whose OWN class is listed here is excluded from BOTH the
		// pool and the rewrite — the same treatment the activity-anchor and
		// supervisor-note exclusions above already get, but keyed on the
		// heading's own class rather than an ancestor div (headings never nest,
		// so a simple open/close latch is enough).
		// Data: body_region.heading_relevel.fixed_level_classes.
		// Env toggle: FIXEDHEAD_OFF (reverts to re-levelling them with the rest).
		const fixedCls = new Set(
			(typeof process !== "undefined" && process.env && process.env.FIXEDHEAD_OFF)
				? [] : (cfg.fixed_level_classes ?? []));
		const fixedLevelHeading = (attrs) => fixedCls.size > 0
			&& (String(attrs ?? "").match(/class="([^"]*)"/i)?.[1] ?? "")
				.split(/\s+/).some((c) => fixedCls.has(c));
		const tagRe = /<(\/?)(div|section|h[2-6])\b([^>]*)>/gi;
		// shared tag-walk that tracks div nesting + which spans are inside a widget subtree
		const walk = (onFreeHeadingOpen) => {
			let depth = 0;
			const wstack = [];   // div-depths at which a widget container opened
			let m;
			tagRe.lastIndex = 0;
			while ((m = tagRe.exec(html))) {
				const isClose = m[1] === "/";
				const tag = m[2].toLowerCase();
				if (tag === "div" || tag === "section") {
					if (isClose) {
						if (wstack.length && wstack[wstack.length - 1] === depth) wstack.pop();
						depth--;
					} else {
						depth++;
						const cls = (m[3].match(/class="([^"]*)"/i)?.[1] ?? "").split(/\s+/);
						if (cls.some((c) => skip.has(c))) wstack.push(depth);
					}
				} else if (!isClose && wstack.length === 0) {
					if (fixedLevelHeading(m[3])) continue;   // a fixed-level heading never joins the pool
					onFreeHeadingOpen(parseInt(tag[1], 10));
				}
			}
		};
		// SAFETY CLAMP: the h6 emission headroom is an INTERMEDIATE artifact only the re-leveller
		// understands. A free-body [H5]→h6 is ranked back into range below, but an [H5]→h6 that sits
		// INSIDE a skip subtree (widget / activity) is left untouched by the walk — so any h6 that
		// survives is clamped to max_level (h5, its normal body-clamped level). Applied to EVERY
		// active return so no h6 ever reaches the output.
		const clamp6 = (s) => s.replace(/(<\/?)h6\b([^>]*>)/gi, `$1h${maxL}$2`);
		// PASS 1 — collect the page's free-body heading outline
		const levels = [];
		walk((lv) => levels.push(lv));
		if (!levels.length) return clamp6(html);
		const distinct = [...new Set(levels)].sort((a, b) => a - b);
		const rank = new Map(distinct.map((lv, i) => [lv, Math.min(base + i, maxL)]));
		if (distinct.every((lv) => rank.get(lv) === lv)) return clamp6(html);   // already an h3-top outline → no level change
		// PASS 2 — rewrite free-body heading open + close tags (re-running the same walk state)
		let depth = 0;
		const wstack = [];
		let fixedOpen = false;   // latch: the OPEN fixed-level heading's close tag must be left alone too
		return clamp6(html.replace(tagRe, (full, slash, tg, attrs) => {
			const isClose = slash === "/";
			const tag = tg.toLowerCase();
			if (tag !== "div" && tag !== "section") {
				if (!isClose && fixedLevelHeading(attrs)) { fixedOpen = true; return full; }
				if (isClose && fixedOpen) { fixedOpen = false; return full; }
			}
			if (tag === "div" || tag === "section") {
				if (isClose) {
					if (wstack.length && wstack[wstack.length - 1] === depth) wstack.pop();
					depth--;
				} else {
					depth++;
					const cls = (attrs.match(/class="([^"]*)"/i)?.[1] ?? "").split(/\s+/);
					if (cls.some((c) => skip.has(c))) wstack.push(depth);
				}
				return full;
			}
			if (wstack.length > 0) return full;                 // inside a widget — leave it
			const newLv = rank.get(parseInt(tag[1], 10));
			if (!newLv || newLv === parseInt(tag[1], 10)) return full;
			return isClose ? `</h${newLv}>` : `<h${newLv}${attrs}>`;
		}));
	};

	// =======================================================================
	// PARTITIONING (what feeds the menu vs the body)
	// =======================================================================

	/**
	 * Title casing for the header <h1><span> title(s).
	 *
	 * WHY: human developers virtually never ship an ALL-CAPS header title — the
	 * corpus audit found 2 of ~2,200. They normalise it (mostly to sentence case).
	 * So if the writer typed the title in ALL CAPS we sentence-case it (first
	 * letter up, the rest down). Titles already in mixed/sentence/title case are
	 * left EXACTLY as written — editorial casing (proper nouns, acronyms) can't be
	 * reconstructed and isn't ours to invent.
	 *
	 * USAGE: #normaliseTitleCase("ROARS AND WHISPERS") → "Roars and whispers"
	 *        #normaliseTitleCase("AI Digital Citizenship") → unchanged
	 *
	 * @param {string} s
	 * @returns {string}
	 */
	static #normaliseTitleCase(s) {
		const t = String(s ?? "");
		const letters = t.replace(/[^A-Za-zĀĒĪŌŪāēīōū]/g, "");
		// not all-caps (or no letters) → leave the writer's casing untouched
		if (!letters || letters !== letters.toUpperCase()) return t;
		// all-caps → sentence case: lowercase everything, capitalise the first letter
		return t.toLowerCase().replace(/[A-Za-zĀĒĪŌŪāēīōū]/, (c) => c.toUpperCase());
	};

	/**
	 * Bilingual PARALLEL-TITLE split — the WT signal for a two-language title
	 * that carries NO pipe / line-break / 2+space separator (so the standard
	 * chain would merge both languages into one <h1>, and the lone "single"
	 * title then wrongly triggers the Course backup into the other <h1>).
	 *
	 * THE SIGNAL (derivable from the WT alone): the payload is TWO phrases each
	 * ending in the SAME sentence-terminal punctuation (! !, . ., or ? ?) AND
	 * exactly ONE half carries a Te Reo macron (āēīōū) — i.e. the English!/Te-Reo!
	 * pattern. Verified across all 370 human title bars: 2 correct splits
	 * (ENGS301 "PICTURE THIS! WHAKAAHUATIA TĒNEI!", ENGC202 "Ready, Set,
	 * Instruct! Takatū, Whakaritea, Tohutohu!") and ZERO false splits — it never
	 * breaks a single-language title (no single-title payload matches both
	 * guards). Source order is preserved (English-first in both gold cases).
	 *
	 * The 147 OTHER no-separator two-title modules use editorial signals not
	 * present in the raw payload (colon, slash, dash, or pure bilingual
	 * knowledge) — those stay a single title (the documented non-derivable
	 * limitation; see Scaffolding/Human_Translation audits).
	 *
	 * @param {string} payload  the code-stripped [TITLE BAR] payload
	 * @returns {string[]|null} [first, second] or null when the signal is absent
	 */
	static #bilingualPunctSplit(payload) {
		const cfg = DataService.Data.EmitTemplates.header.title_split ?? {};
		if (!cfg.bilingual_punct_split) return null;
		const m = payload.match(/^(.+?[.!?])\s+(.+[.!?])$/);
		if (!m) return null;
		const a = m[1].trim();
		const b = m[2].trim();
		if (a.slice(-1) !== b.slice(-1)) return null;        // same terminal punct on BOTH halves
		const macron = /[āēīōūĀĒĪŌŪ]/;
		if (macron.test(a) === macron.test(b)) return null;  // exactly ONE half is Te Reo (macron)
		return [a, b];
	};

	/**
	 * Splits a bilingual "[TITLE BAR]" on a SINGLE spaced dash ( – / — / - ) into its Te Reo
	 * and English halves (module CEDW501's title was the original example of this shape).
	 *
	 * WHY THIS IS TIGHTLY GUARDED:
	 * It must ONLY fire on the clean "X – Y" bilingual-title shape, and must never accidentally
	 * fire on a single-language title that just happens to contain internal punctuation. The
	 * guards are: no pipe/slash/double-space present (those are handled earlier in the split
	 * chain, or signal a different structure entirely), EXACTLY ONE spaced dash present, both
	 * resulting halves are non-empty, EXACTLY ONE half carries a macron (a Māori accent mark —
	 * the signal that it's the Te Reo half), and NEITHER half is unfinished template-placeholder
	 * boilerplate text. Measured 3 clean splits across the whole corpus with 0 false splits
	 * (see outputs/_measure_dashtitle.py).
	 *
	 * Data flag: header.title_split.bilingual_dash_split
	 * Env toggle: DASHTITLE_OFF
	 * @returns {?string[]} [a, b] in the payload's original order, or null if it doesn't apply
	 */
	static #bilingualDashSplit(payload) {
		const cfg = DataService.Data.EmitTemplates.header.title_split ?? {};
		if (!cfg.bilingual_dash_split) return null;
		if (typeof process !== "undefined" && process.env && process.env.DASHTITLE_OFF) return null;
		if (/[|/]/.test(payload) || /\n/.test(payload) || /\S {2,}\S/.test(payload)) return null;
		const dashes = payload.match(/\s[–—-]\s/g);
		if (!dashes || dashes.length !== 1) return null;      // exactly ONE spaced dash
		const parts = payload.split(/\s[–—-]\s/).map((s) => s.trim());
		if (parts.length !== 2 || !parts[0] || !parts[1]) return null;
		const macron = /[āēīōūĀĒĪŌŪ]/;
		if (macron.test(parts[0]) === macron.test(parts[1])) return null;   // exactly ONE half Te Reo
		const boiler = /(module title|insert|awaiting|translation)/i;
		if (boiler.test(parts[0]) || boiler.test(parts[1])) return null;     // an incomplete/placeholder title
		return parts;
	};

	/**
	 * Handles two more bilingual "[TITLE BAR]" boundary shapes that the dash/punctuation
	 * splitters above still miss (found via a screenshot review of module OSAH301-0.0, whose
	 * English and Te Reo titles weren't being separated). BOTH shapes below reuse the SAME
	 * macron-based guard as the dash splitter (#bilingualTwoLangGuard: EXACTLY one half must
	 * carry a macron/āēīōū accent mark, and neither half may be unfinished placeholder
	 * boilerplate), so neither one can accidentally fire on a single-language title or on a
	 * title shape already handled elsewhere. Both run AFTER the punctuation/dash splitters in
	 * the overall split chain, so they only ever see titles those earlier splitters rejected.
	 *
	 * COLON shape: the two halves are separated by a single ':' character — for example
	 * module CEDO501's "TE WHAI MŌNI: YOUR MONEY" or TWHK903's "Digital Citizenship:
	 * Tāurungi Matihiko".
	 *
	 * CASE-TRANSITION shape: an ALL-CAPS English half is glued directly onto a non-caps Te
	 * Reo half, because the writer's original visual boundary (a checkmark emoji or similar)
	 * was dropped somewhere upstream in the document-parsing pipeline and collapsed down to
	 * a single space — for example module OSAH301's "ONLINE ABUSE AND HARASSMENT Tūkinotanga
	 * ā-ipurangi…". The split point is found by taking the longest leading run of ALL-CAPS
	 * words as the English half, with everything non-capitalised after it as the Te Reo half
	 * (the all-caps English half is then automatically fixed up to normal title casing by
	 * #normaliseTitleCase elsewhere). Measured 4 clean splits with 0 false positives (see
	 * outputs/_measure_title_markersplit.py).
	 *
	 * Data flag: header.title_split.bilingual_marker_split
	 * Env toggle: BILINGUALMARK_OFF
	 */
	static #bilingualTwoLangGuard(parts) {
		if (!Array.isArray(parts) || parts.length !== 2 || !parts[0] || !parts[1]) return null;
		const macron = /[āēīōūĀĒĪŌŪ]/;
		if (macron.test(parts[0]) === macron.test(parts[1])) return null;   // exactly ONE half Te Reo
		const boiler = /(module title|insert|awaiting|translation)/i;
		if (boiler.test(parts[0]) || boiler.test(parts[1])) return null;
		return parts;
	};

	// other separators are handled EARLIER in the chain (or are ambiguous) — bail if present
	static #titleHasOtherSep(payload) {
		return /[|/]/.test(payload) || /\s[–—-]\s/.test(payload) || /\n/.test(payload) || /\S {2,}\S/.test(payload);
	};

	/**
	 * THE GENERAL single-character bilingual title splitter (found via module ENGS401-00).
	 *
	 * BACKGROUND — why this exists as a general mechanism rather than another one-off case:
	 * title separators used to be handled ASYMMETRICALLY. The slash character '/' was only
	 * ever recognised DEFENSIVELY — both #titleHasOtherSep and #bilingualDashSplit would BAIL
	 * OUT when they saw a slash present, correctly recognising "this isn't my separator" — but
	 * no splitter ever actually ACTED on a slash to perform a split. The result: a
	 * slash-separated bilingual "[TITLE BAR]" like "Responding to Texts / Te whakautu i ngā
	 * kuputuhi" (module ENGS401) fell all the way through every splitter and ended up
	 * rendered as one single combined "<h1>", even though the human developer always ships
	 * it as two separate headings. The general fix: every single-character "soft" separator
	 * now lives in ONE ordered DATA list
	 * (header.title_split.bilingual_marker_split.char_separators), and THIS method is the
	 * ONLY splitter that walks that list — the FIRST separator in the list that occurs
	 * EXACTLY once in the title AND yields a guarded, valid bilingual pair wins. Because it's
	 * now purely data-driven, adding a future single-character title separator is just a DATA
	 * edit — the old defensive-but-not-offensive asymmetry that caused this whole bug class
	 * cannot happen again.
	 *
	 * Each entry in the list has the shape { sep, flag (its own data on/off key), off (its
	 * own env A/B toggle), bail_other_sep? (optional) }. The colon separator folds into this
	 * list unchanged from its earlier dedicated handling (flag "colon", env
	 * BILINGUALMARK_OFF, bail_other_sep:true — meaning it keeps its original "if any OTHER
	 * separator is present, this one isn't mine to handle" bail-out rule). The slash
	 * separator (flag "slash", env TITLESLASH_OFF) is ordered FIRST in the list (so it
	 * outranks the colon) and deliberately does NOT set bail_other_sep, so a slash-separated
	 * title that also happens to contain an internal spaced dash (module ENGI201) still
	 * splits correctly on the top-level slash. The same macron-based guard used by the dash
	 * splitter (#bilingualTwoLangGuard) is applied to every entry, which means none of them
	 * can ever falsely split a genuine single-language title. Measured (see
	 * outputs/_measure_title_separators.py): the slash rule splits 8 modules correctly with
	 * 0 false splits; folding the colon rule into this same list produces byte-identical
	 * output to its old dedicated handling (no module in the corpus contains both '/' and
	 * ':' in its title, so there's no overlap to worry about).
	 */
	static #bilingualCharSplit(payload) {
		const cfg = DataService.Data.EmitTemplates.header.title_split ?? {};
		const ms = cfg.bilingual_marker_split ?? {};
		const envOff = (v) => typeof process !== "undefined" && process.env && v && process.env[v];
		for (const e of (ms.char_separators ?? [])) {
			if (!e || !e.sep) continue;
			if (e.flag && !ms[e.flag]) continue;                              // per-separator DATA flag
			if (envOff(e.off)) continue;                                      // per-separator env A/B toggle
			if (e.bail_other_sep && this.#titleHasOtherSep(payload)) continue; // the colon rule keeps its own "bail if any other separator is present" rule
			if ((payload.split(e.sep).length - 1) !== 1) continue;            // EXACTLY one occurrence
			const idx = payload.indexOf(e.sep);
			const parts = [payload.slice(0, idx).trim(), payload.slice(idx + 1).trim()];
			const guarded = this.#bilingualTwoLangGuard(parts);
			if (guarded) return guarded;
		}
		return null;
	};

	static #bilingualCaseSplit(payload) {
		const cfg = DataService.Data.EmitTemplates.header.title_split ?? {};
		if (!cfg.bilingual_marker_split?.case_transition) return null;
		if (typeof process !== "undefined" && process.env && process.env.BILINGUALMARK_OFF) return null;
		if (this.#titleHasOtherSep(payload) || /:/.test(payload)) return null;   // colon is the colon-split's domain
		const words = payload.split(/\s+/);
		if (words.length < 2) return null;
		const isCaps = (w) => /[A-ZĀĒĪŌŪ]/.test(w) && !/[a-zāēīōū]/.test(w);
		let k = 0;
		while (k < words.length && isCaps(words[k])) k++;
		if (k < 1 || k >= words.length) return null;   // need ≥1 ALL-CAPS word AND ≥1 non-caps remainder
		const parts = [words.slice(0, k).join(" ").trim(), words.slice(k).join(" ").trim()];
		return this.#bilingualTwoLangGuard(parts);
	};

	/**
	 * Splits a page's items three ways:
	 *  - titleBar: the [TITLE BAR] payload → header titles (English | Te Reo)
	 *  - menuItems: overview pre-introduction section, or the lesson's
	 *    [Lesson Overview] section — IF the page has a menu (else body)
	 *  - bodyItems: everything else
	 *
	 * WHY: the overview's Learning-Intentions/Success-Criteria headings are
	 * CONSUMED into the module-menu (they emit no body element) — the one
	 * heading outcome that isn't an element (Tag_Interpretation_Rules §5.1).
	 */
	static #partitionItems(page, menuType, run) {
		const items = page.items;
		const titleBar = { english: "", teReo: "" };
		const menuItems = [];
		const bodyItems = [];

		// find the boundary markers.
		// The menu/body boundary on the overview is [MODULE INTRODUCTION] —
		// or, in the BLL-family templates that never use it, the first
		// MID-document title-bar alias ([Title]/[Introduction] resolving to
		// the "title bar" canonical AFTER the real opener): everything
		// before it is the menu block (verified against BLL146-0.0, whose
		// human menu holds the Understand/Know/Do region).
		let introIdx = items.findIndex((it) => it.type === "tag"
			&& it.parse.primary?.tag === "module introduction");
		if (introIdx < 0 && page.isOverview) {
			let seenOpener = false;
			introIdx = items.findIndex((it) => {
				if (it.type !== "tag" || it.parse.primary?.tag !== "title bar") return false;
				if (!seenOpener) { seenOpener = true; return false; }   // the page opener itself
				return true;                                            // first MID-doc alias
			});
		}
		// FUNDAMENTALS front-matter [Overview] WALT/I-can block routing to the MODULE MENU
		// (module HPFUN903 is the reference example for this). When the menu/body boundary
		// found above is a mid-document title-bar alias whose variant word folds to a known
		// entry in alias_words (specifically "overview" — the "[Title]"/"[Introduction]"
		// alias forms never carry this block, measured 0 times across the whole 427-module
		// corpus), and the forward region after it (black text plus "safe" tags plus
		// non-structural red spans, stopping at the first STRUCTURAL tag) holds BOTH a WALT
		// lead-in line ("We are learning…") AND a Success-Criteria lead-in line ("I can:" /
		// "You will show…"), and a matching row exists in the
		// menu.fundamentals_overview_li registry for this subject-and-phase group — then the
		// whole region becomes MENU source content (its items are marked "_funLi" so
		// MenuBuilder knows to compose them into the menu) and the alias tag itself is
		// CONSUMED entirely (the human developer's gold output ships no "<h3>Overview</h3>"
		// body heading at all here — their body simply opens straight at the phases
		// navigation). Measured across ALL 427 Writers Templates (see
		// outputs/_measure_funmenu.cjs): this applies to exactly 20 modules (7 ENFUN, 12
		// HPFUN, and XFUN01), all of which are single-page overviews using the "simplified"
		// menu type; a further 7 modules that have the alias but lack the required lead-in
		// lines (EXPFUN02 through 05, SCFUN01, SSFUN03, TEDC401) correctly decline to apply
		// this rule. The env toggle below reverts the ENTIRE mechanism at this one single
		// choke point — with it off, no region is captured, the alias renders as a plain
		// "<h3>Overview</h3>" body heading, the WALT/SC block stays as ordinary body content,
		// and the menu is left in its earlier, less complete form.
		// Env toggle: FUNMENU_OFF
		let funIdxSet = null, funAliasIdx = -1;
		const funCfg = DataService.Data.EmitTemplates.menu?.fundamentals_overview_li;
		const funOn = funCfg && funCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FUNMENU_OFF);
		if (funOn && page.isOverview && menuType !== "none" && introIdx > 0
			&& items[introIdx]?.type === "tag"
			&& items[introIdx]?.parse?.primary?.tag === "title bar"
			&& (funCfg.alias_words ?? []).includes(items[introIdx].parse.primary.fragment ?? "")
			&& MenuBuilder.fundamentalsLiRow(run, funCfg)) {
			const funSafe = new Set(funCfg.menu_section_safe_tags ?? ["body", "list", "sub head"]);
			const funTextish = (x) => {
				if (x.type === "black") return true;
				if (x.type !== "tag") return false;
				const p = x.parse?.primary;
				if (!p) return true;                                       // unresolved red span
				if (x.parse?.class === "instruction" || x.parse?.class === "noise") return true;
				return funSafe.has(p.tag);
			};
			const funIdx = new Set();
			const funLines = [];
			for (let j = introIdx + 1; j < items.length; j++) {
				const x = items[j];
				if (!funTextish(x)) break;                                 // a structural tag ends the region
				funIdx.add(j);
				if (x.type === "black") funLines.push(x.text);
				else if (x.blackAfter && x.blackAfter.trim()) funLines.push(x.blackAfter);
			}
			const funMaxW = funCfg.lead_max_words ?? 10;
			const funFold = (s) => Utils.Fold(String(s)).replace(/[*_]/g, "").replace(/\s+/g, " ").trim();
			const funHasLead = (list) => funLines.join("\n").split(/\n+/).some((ln) => {
				const f = funFold(ln);
				if (!f || /^[•\-–—]/.test(f) || f.split(/\s+/).length > funMaxW) return false;
				return (list ?? []).some((m) => f === m || f.startsWith(m + " ")
					|| f.startsWith(m + ":") || f.startsWith(m + "…") || f.startsWith(m + "."));
			});
			if (funIdx.size && funHasLead(funCfg.walt_match) && funHasLead(funCfg.sc_match)) {
				funIdxSet = funIdx;
				funAliasIdx = introIdx;
			}
		}
		// The ENFUN subject group's Phase-1 RED delimiter span sits BEFORE the "[Overview]"
		// alias on every one of the 8 measured modules that use this pattern — that is, on
		// the MENU side of the menu/body boundary — where the pre-intro menu-source rule
		// above would otherwise consume it as menu content, meaning the phase-text pre-pass
		// (elsewhere in this file) would never get to see the complete set of phase
		// delimiters for the page. The fix routes a matching delimiter span to the BODY side
		// instead: this is safe because the span renders NOTHING in the menu anyway (it's
		// classified as noise, with no resolved primary tag), so moving it doesn't change any
		// menu bytes — it only affects WHERE the item lives in the internal item list, the
		// same "position-only" pattern used for the bracket-less "Lesson overview" lead
		// elsewhere in this file. This uses the same gating conditions as the phase-text
		// pre-pass itself (the data flag, the page's fundamentals body_class, the single-file
		// page model, and a minimum count of standalone delimiter spans page-wide).
		// Data flag: fundamentals_panels.phase_text.red_delimiter
		// Env toggle: FUNPANRED_OFF
		let redPhaseToBody = null;
		{
			const fpCfg = DataService.Data.EmitTemplates.body_region?.fundamentals_panels?.phase_text;
			const rdCfg = fpCfg && fpCfg.red_delimiter;
			const rdOn = !!rdCfg && rdCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.FUNPANRED_OFF)
				&& !(typeof process !== "undefined" && process.env && process.env.FUNDPHASE_OFF)
				&& /(^|\s)fundamentals(\s|$)/.test(run.resolvedRules?.body_class || "")
				&& run.resolvedRules?.page_model === "single-file";
			if (rdOn) {
				const rdRe = new RegExp((fpCfg && fpCfg.delimiter_pattern) || "^phase\\s+\\d+$", "i");
				const rdIdx = [];
				for (let i2 = 0; i2 < items.length; i2++) {
					const x = items[i2];
					if (x.type === "tag" && !x.parse?.primary
						&& (x.parse?.class === "noise" || x.parse?.class === "instruction")
						&& rdRe.test((x.parse?.folded ?? "").trim())) rdIdx.push(i2);
				}
				if (rdIdx.length >= ((fpCfg && fpCfg.min_delimiters) || 2)) redPhaseToBody = new Set(rdIdx);
			}
		}
		// Content-based fallback: combined-doc overviews (e.g. ENGJ302) have NO
		// [MODULE INTRODUCTION], no mid-doc title-bar alias, and no in-page [End page]
		// to mark where the menu ends. Recognise the overview's MENU SECTIONS by their
		// headings (Understand/Know/Do, Learning Intentions, Success Criteria, Planning,
		// Connections, Assessment, Overview…) and route those heading-led blocks into
		// the menu; everything else stays body. Driven by data: menu.overview_section_labels.
		const overviewMenuIdx = new Set();
		if (introIdx < 0 && page.isOverview && menuType !== "none") {
			const labels = DataService.Data.EmitTemplates.menu.overview_section_labels ?? [];
			const matchesLabel = (f) => labels.some((l) =>
				f === l || f.startsWith(l + " ") || f.endsWith(" " + l) || f.includes(" " + l + " "));
			// An inquiry-mode `[Tab N]` opener ENDS the overview menu region: the inquiry
			// panels that follow it are body content, not menu content. Without this check,
			// the LAST menu-section heading found would leave the inMenu flag stuck at true,
			// which would then SWALLOW the following `[Tab 1]`/`[Tab 2]` openers into the menu
			// too (since they aren't themselves headings, nothing would ever flip inMenu back
			// off) — right up until the next non-menu inquiry heading was reached. That meant
			// those tab openers never reached the #body section and never got a panel
			// sentinel of their own, causing separate panels to visually collapse into one
			// (seen on module TWHA901, where "Introduction" and "Agency" merged into a single
			// panel). With this fix, once the first tab-family opener is seen, everything
			// from that point onward on the page is treated as body content.
			// Data flag: menu.inquiry_tab_ends_overview_menu
			// Env toggle: INQMENU_OFF
			// (this only applies within this content-based fallback path; an overview with no
			// `[Tab N]` tags at all is completely unaffected — the check only ever fires where
			// a tab-family tag actually exists, i.e. only on inquiry-style modules)
			const _inqEndsMenu = (DataService.Data.EmitTemplates.menu.inquiry_tab_ends_overview_menu?.enabled !== false)
				&& !(typeof process !== "undefined" && process.env && process.env.INQMENU_OFF);
			const _isTabTag = (it2) => it2.type === "tag"
				&& (/^\s*tab\s*\d/i.test(String(it2.text || "")) || /\btab\b/i.test(it2.parse?.primary?.tag || ""));
			let inMenu = false;
			let pastFirstTab = false;
			for (let k = 0; k < items.length; k++) {
				const it2 = items[k];
				if (_inqEndsMenu && _isTabTag(it2)) { pastFirstTab = true; inMenu = false; }
				if (pastFirstTab) continue;   // inquiry panels are body — never menu
				if (it2.type === "tag" && it2.parse.primary?.tag === "title bar") { inMenu = false; continue; }
				if (it2.type === "tag" && ["h1", "h2", "h3", "h4", "h5", "heading"].includes(it2.parse.primary?.tag)) {
					const htext = ((it2.blackAfter || "").replace(/[*_]/g, "").trim()) || this.#norm.RenderText(it2.text) || "";
					inMenu = matchesLabel(Utils.Fold(htext));   // start/continue a menu section?
				}
				if (inMenu) overviewMenuIdx.add(k);   // this item belongs to a menu section
			}
		}
		let overviewIdx = items.findIndex((it) => it.type === "tag"
			&& it.parse.primary?.tag === "lesson overview");
		// THE BRACKET-LESS red "Lesson overview" lead (found on modules EXIP901,
		// EXBP901, and ENGS302). Sometimes a writer types the words "Lesson overview" as
		// ordinary red-coloured TEXT rather than as a proper bracketed tag — with no
		// brackets, no "[Lesson Overview]" tag ever resolves (it's classified as plain
		// noise, with no resolved primary tag), so the menu-building logic above never
		// fires for it, and the WALT/intentions content that should have gone into the menu
		// stays stuck in the ordinary body instead — even though the human developer puts
		// it in the menu on every page shaped like this. Measured across the whole corpus:
		// 3 modules / 11 such spans, with ZERO occurrences of the same phrase appearing as
		// ordinary black (non-red) text — which means a rule that only matches an EXACT,
		// whole-span red-text match can never accidentally over-fire on ordinary prose (see
		// outputs/_measure_bareoverview.py for the full measurement). So: when NO bracketed
		// "[Lesson Overview]"-style tag exists anywhere on the page, this code accepts a red
		// noise/instruction span whose ENTIRE folded text matches the configured pattern as
		// standing in for the overview MARKER instead. This only affects WHERE the item
		// sits in the internal item list — the span itself still renders nothing either way,
		// so it's a position-only fix.
		// Data flag: menu.lesson_overview_bare_lead
		// Env toggle: BARELEAD_OFF
		const bareCfg = DataService.Data.EmitTemplates.menu?.lesson_overview_bare_lead;
		const bareOn = bareCfg && bareCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.BARELEAD_OFF);
		if (bareOn && overviewIdx < 0) {
			const barePat = new RegExp(bareCfg.pattern ?? "^lesson overview:?$", "i");
			overviewIdx = items.findIndex((it) => it.type === "tag" && !it.parse?.primary
				&& (it.parse?.class === "noise" || it.parse?.class === "instruction")
				&& barePat.test((it.parse?.folded ?? "").trim()));
		}
		const contentIdx = items.findIndex((it) => it.type === "tag"
			&& it.parse.primary?.tag === "lesson content");

		// Where does the lesson menu END? The [Lesson Overview] block ("We are
		// learning:" / "I can:" + bullets) is bounded by [Lesson content] WHEN the
		// writer includes it. But MANY lessons omit [Lesson content] and go straight
		// from [Lesson Overview] to the lesson's first heading / lesson-title — in
		// that case the menu ends at that first heading. Without this, the menu
		// block leaks into #body and #module-menu-content is left EMPTY (verified
		// bug: OSBY301 Lesson 2, which has no [Lesson content], only [H2]).
		// The lesson body always begins at one of these tags, so they bound the menu:
		//
		// The "[Lesson content]" marker actually OPENS the "We are learning:" / "I can:"
		// sub-region (found on module OSAH501-03) — and the human developer ALSO routes
		// that sub-region into #module-menu-content, meaning "[Lesson content]" is NOT
		// really the end of the menu at all. The converter used to set lessonMenuEnd
		// directly to contentIdx (the position of the "[Lesson content]" marker itself),
		// which caused the WALT/I-can intentions block that follows it to leak out into the
		// ordinary body instead of the menu. With the menu.lesson_content_in_menu flag on,
		// the menu instead ends at the first genuine HEADING or title-bar tag that follows
		// (skipping straight past the "[Lesson content]" marker itself), so the learning
		// intentions correctly reach the menu the same way the human's version does
		// (measured across 442 lesson pages: 98.9% match, with 0 genuine over-fires — the 5
		// apparent body-exceptions turned out to simply be menu-less pages; see
		// outputs/_measure_lessonmenu.py for the full measurement).
		// Env toggle: LESSONINTENT_OFF (reverts to ending the menu right at the marker)
		const intentCfg = DataService.Data.EmitTemplates.menu.lesson_content_in_menu;
		const intentOn = intentCfg && intentCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.LESSONINTENT_OFF);
		const lessonMenuEndTags = new Set(intentOn
			? ["title bar", "h1", "h2", "h3", "h4", "h5", "heading"]
			: ["lesson content", "title bar", "h1", "h2", "h3", "h4", "h5", "heading"]);
		let lessonMenuEnd = intentOn ? -1 : contentIdx;
		if (lessonMenuEnd < 0 && overviewIdx >= 0) {
			lessonMenuEnd = items.findIndex((it, idx) => idx > overviewIdx
				&& it.type === "tag" && lessonMenuEndTags.has(it.parse.primary?.tag));
		}
		// guard: extending past [Lesson content] but finding NO heading (a lesson with
		// no title after the intentions) falls back to ending at the marker, so the
		// intro is still captured — never regress to an empty menu.
		if (intentOn && lessonMenuEnd < 0 && contentIdx >= 0) lessonMenuEnd = contentIdx;

		// SECTION-STOP menu capture. The simple region described above (from overviewIdx
		// through to the first heading) absorbs EVERYTHING in between as menu content — but
		// the CED NCEA subject family writes its lesson pages as "[Lesson Overview]" →
		// "[alert.top]" printable-resources box + "[Button]"s → "[Lesson content]" →
		// WALT/I-can → "[H2]", and the human developer's version keeps the alert box and
		// buttons in the ordinary #body, putting ONLY the WALT/intentions content into the
		// menu. So this section-stop logic makes the menu instead absorb two SEPARATE,
		// CONTIGUOUS text-only sections: (A) the "[Lesson Overview]" tag's own intro run,
		// and (B) the "[Lesson content]" section — each one running only over black text
		// and a small set of menu-safe tags (menu_section_safe_tags, defaulting to
		// body/list/sub-heading); ANY other kind of tag (an alert, a button, an image, an
		// interactive widget, a heading, and so on) immediately ends that section. Pages
		// whose whole region was already pure text to begin with (the simpler pattern:
		// Lesson-Overview → Lesson-content → WALT → heading, with nothing else mixed in)
		// produce byte-identical output either way, by construction.
		// Data flag: menu.lesson_menu_section_stop
		// Env toggle: MENUSTOP_OFF (reverts to the simple, non-section-stopping range)
		const stopCfg = DataService.Data.EmitTemplates.menu?.lesson_menu_section_stop;
		const stopOn = intentOn && stopCfg && stopCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.MENUSTOP_OFF);
		let menuIdxSet = null;
		if (stopOn && overviewIdx >= 0 && lessonMenuEnd > overviewIdx) {
			const safe = new Set(stopCfg.menu_section_safe_tags ?? ["body", "list", "sub head"]);
			// "Menu-safe" means: black text, a tag from the safe list, OR a NON-STRUCTURAL
			// red item — a writer's own instruction/noise span (for example module ENGC302
			// leaves the template prompt "Depending on the size and complexity…" sitting
			// between "[Lesson Overview]" and the WALT text) or an unresolved red span with
			// no primary tag. None of these carry any real structure, and the earlier,
			// simpler region logic already absorbed them into the menu region, so treating
			// them as "skip over, don't stop for" here keeps that existing behaviour
			// byte-identical. Only a genuinely STRUCTURAL tag (an alert, a button, an image,
			// an interactive widget, a heading, and so on) actually ends a section.
			const textish = (x) => {
				if (x.type === "black") return true;
				if (x.type !== "tag") return false;                       // image/table blocks stop
				const p = x.parse?.primary;
				if (!p) return true;                                       // unresolved red span
				if (x.parse?.class === "instruction" || x.parse?.class === "noise") return true;
				return safe.has(p.tag);
			};
			menuIdxSet = new Set();
			for (let j = overviewIdx + 1; j < lessonMenuEnd; j++) {     // section A: the LO intro
				if (j === contentIdx) break;                            // LC opens its own section
				if (!textish(items[j])) break;                          // a structural tag ends it
				menuIdxSet.add(j);
			}
			if (contentIdx > overviewIdx && contentIdx < lessonMenuEnd) {
				for (let j = contentIdx + 1; j < lessonMenuEnd; j++) {  // section B: [Lesson content]
					if (!textish(items[j])) break;
					menuIdxSet.add(j);
				}
			}
		}

		// Tracks items that the TITLE-BAR branch below absorbed as extra title sources — for
		// example an adjacent Te Reo black text line, or a pipe-separated-half red sibling
		// span. Once absorbed, an item is marked "consumed" here so it stops being rendered
		// a second time as ordinary body or menu text (the same capture-then-mark-consumed
		// pattern used by the bracket-less overview lead and the fundamentals overview menu
		// logic above).
		const tbConsumed = new Set();

		// MTK DROP-DOWN-MENU CAPTURE (ROUND 212 — the PNR101/102/104 bilingual family).
		// The new "Te Aka Taumatua" template authors the WHOLE module menu as one
		// English|Māori two-column table between a "[Content for DROP DOWN MENU]"
		// opener and an "[END OF DROP-DOWN MENU]" closer (PNR102 types the closer
		// without the hyphen). On a bilingual overview page, everything from the
		// opener to the closer is routed to the MENU side here: the table itself is
		// flagged "_reoDropdown" so MenuBuilder.#reoDropdownTabs composes it into the
		// human's bilingual tabs menu, and the opener/closer marker tags are consumed
		// (they render nothing). Everything after the closer stays ordinary body
		// content (the [MODULE CONTENT: PAGE 1] introduction table).
		// Data: elements.dual_language.dropdown_menu. Env toggle: REODROPMENU_OFF.
		let ddIdxSet = null;
		{
			const ddCfg = DataService.Data.EmitTemplates.elements?.dual_language?.dropdown_menu;
			const ddOn = ddCfg && ddCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF)
				&& page.isOverview && menuType !== "none" && MenuBuilder.isReoModule(run);
			if (ddOn) {
				const opRe = new RegExp(ddCfg.opener_pattern ?? "^\\[content for drop[ -]?down menu\\]$", "i");
				const clRe = new RegExp(ddCfg.closer_pattern ?? "^\\[end of drop[ -]?down menu\\]$", "i");
				const oi = items.findIndex((x) => x.type === "tag"
					&& opRe.test((x.parse?.folded ?? "").trim()));
				// the PNR TABLE shape only: the opener must be DIRECTLY followed by
				// the menu table (the paragraph-form TRR203/TRR301 siblings author
				// their menu as loose paragraphs — a separate follow-up class; they
				// keep their existing behaviour, byte-identical)
				if (oi >= 0 && items[oi + 1]?.type === "table") {
					ddIdxSet = new Set([oi]);
					for (let j = oi + 1; j < items.length; j++) {
						const x = items[j];
						if (x.type === "tag" && clRe.test((x.parse?.folded ?? "").trim())) {
							ddIdxSet.add(j);   // the closer marker itself
							break;
						}
						// defensive stop: a page boundary means the writer never
						// closed the section — leave the rest to the body
						if (x.type === "tag" && x.parse?.primary?.directive === "PAGE_BOUNDARY") break;
						if (x.type === "table") {
							x._reoDropdown = true;
							menuItems.push(x);
						}
						ddIdxSet.add(j);   // markers/blank items inside the section are consumed
					}
				}
			}
		}

		for (let i = 0; i < items.length; i++) {
			const it = items[i];

			// items captured by the MTK drop-down-menu section above (ROUND 212):
			// the table is already on the menu side; the markers render nothing
			if (ddIdxSet && ddIdxSet.has(i)) continue;

			// The fundamentals "[Overview]" alias tag is CONSUMED (skipped entirely) once its
			// WALT/I-can region has already been captured for the menu above — the human
			// developer's gold output never shows a "<h3>Overview</h3>" body heading in this
			// case; their body content simply opens straight at the phases navigation. This
			// check runs BEFORE the title-bar branch below so that a placeholder-titled opener
			// can never accidentally re-purpose this already-consumed alias as the page's
			// header title.
			if (i === funAliasIdx) continue;
			if (tbConsumed.has(i)) continue;   // already absorbed into the header title above

			// ---- the title bar feeds the header, never the body ----------
			if (it.type === "tag" && it.parse.primary?.tag === "title bar"
				&& titleBar.english === "") {
				// payload → header titles, per Emit_Templates header.title_split:
				// strip a leading module-code token (writers prepend it), then
				// split English | Te Reo on a pipe, else a line break, else a
				// run of 2+ spaces (the OSAI201 gold separator)
				// strip a leading module-code token (writers prepend the full code
				// "OSAI201" OR just the series letters "OSAI") from one side
				const stripCode = (s) => {
					if (!s || !run.moduleCode) return s;
					const letters = run.moduleCode.match(/^[A-Za-z]+/)?.[0] ?? run.moduleCode;
					return s
						.replace(new RegExp(`^\\s*${Utils.RegexEscape(run.moduleCode)}\\b[\\s:–-]*`, "i"), "")
						.replace(new RegExp(`^\\s*${Utils.RegexEscape(letters)}\\b[\\s:–-]+(?=\\S)`, ""), "");
				};
				// The placeholder list (folded for comparison) is computed once here — this
				// catches unfilled template boilerplate text like 'MODULE TITLE TE REO',
				// 'MODULE TITLE', or 'TE REO' that a writer sometimes forgets to replace.
				const tsCfg = DataService.Data.EmitTemplates.header.title_split;
				const phRuleOn = (tsCfg.placeholder_title_rule?.enabled !== false)
					&& !(typeof process !== "undefined" && process.env && process.env.TITLEPH_OFF);
				const ph = [
					...(tsCfg.placeholder_titles ?? []),
					...(phRuleOn ? (tsCfg.placeholder_title_rule?.extra_placeholders ?? []) : []),
				].map((s) => Utils.Fold(s).replace(/\s+/g, ""));
				const isPlaceholder = (s) => ph.includes(Utils.Fold(s).replace(/[\[\]\s|]+/g, ""));
				// A module's title can live in either the RED "[TITLE BAR]" span itself (the
				// "embedded" text) OR in the black text that follows it. When the BLACK side is
				// either missing entirely or is just an unfilled placeholder, fall back to using
				// the red span's own English title instead, so it doesn't get lost (seen on
				// module CEDO202, whose title was 'Moving through the seasons' in the red span
				// alongside a black 'MODULE TITLE TE REO' placeholder; module ANZH401 has the
				// same shape). Ordinary black-only titles (the large majority of modules) and
				// messy multi-span titles (modules XMES103/HIS1008) still just use the black
				// text after the tag as their payload, unaffected by this fallback.
				// Env toggle: TITLEPH_OFF (reverts to always using the black-text payload)
				let payload;
				let payloadJoined = false;   // tracks whether a payload split across multiple spans was re-joined below
				if (phRuleOn) {
					const embeddedTitle = stripCode((this.#norm.RenderText(it.text) || "").replace(/\*/g, "").trim());
					const blackTitle = stripCode(it.blackAfter.replace(/\*/g, "").trim());
					payload = ((!blackTitle || isPlaceholder(blackTitle)) && embeddedTitle)
						? embeddedTitle : (blackTitle || embeddedTitle);
					// Sometimes a writer authors ONE bilingual title but ends up SPLITTING it
					// across two separate spans by accident: the Te Reo half ends up in the RED
					// span (the "embedded" text), while the black text left after the tag is just
					// a bare pipe-prefixed HALF of the title, like "| Thinking creatively" (seen
					// on module TEFUN03). The black-text-preferred fallback logic above would
					// otherwise just ship that half-title as-is and silently lose the embedded
					// Te Reo language entirely. So: when the black side STARTS with a pipe
					// character and the embedded (red-span) side looks like a real title (not a
					// placeholder), re-join the two together — the combined payload then splits
					// cleanly on the pipe just like any other normal bilingual title would.
					// Measured across all 430 Writers Templates: this applies to exactly TEFUN03
					// and ANZH401 (ANZH401's pipe-half turned out to be unfilled placeholder
					// boilerplate, so it gets dropped further downstream anyway and its output is
					// unaffected either way).
					// Data flag: header.title_split.split_payload_join.pipe_lead_black
					// Env toggle: TITLESPANJOIN_OFF
					const sjCfg = tsCfg.split_payload_join;
					const sjOn = sjCfg && sjCfg.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env.TITLESPANJOIN_OFF);
					if (sjOn && sjCfg.pipe_lead_black !== false && embeddedTitle && blackTitle
						&& /^\|/.test(blackTitle) && !isPlaceholder(embeddedTitle)) {
						payload = `${embeddedTitle} ${blackTitle}`.trim();
						payloadJoined = true;
					}
					// Another shape (seen on modules ANZH101 and MXFL104): the pipe-separated half
					// of the title lives in a completely SEPARATE red span (one with no resolved
					// primary tag) that sits DIRECTLY after the title-bar tag. On ANZH101 the
					// span's own text IS that half ("| Tangata Whenua Pūrākau"); on MXFL104 the
					// span is just a bare red '|' separator character, with the actual Te Reo half
					// carried in that span's OWN blackAfter text instead (this happens because
					// the span sits mid-paragraph, so the black text following it gets attached
					// to the span rather than to the title bar). Both the span's own text AND its
					// blackAfter are absorbed into the payload, and the span itself is marked
					// consumed. Without this, that half of the title would otherwise leak out
					// as either a stray body line or a retained developer note, when the human
					// developer's gold output ships it properly as the second-language "<h1>".
					// Data flag: header.title_split.split_payload_join.pipe_sibling
					//
					// There are two separate measured cases here, both boiling down to "a pipe
					// character separates the two title halves": either the SEPARATE SPAN leads
					// with '|' (ANZH101's "| Tangata Whenua Pūrākau", or MXFL104's bare red '|'
					// whose blackAfter carries the actual half), OR the PAYLOAD already collected
					// so far dangles a trailing '|' and the separate span holds the other half
					// (module OSOH301: "ONLINE @HOME |" plus a red span "Ngā whakahaeretanga
					// ā-ipurangi i te kāinga" — the human ships both halves together). Each case
					// was measured against every title-bar line across the whole corpus and
					// confirmed to apply to exactly the named modules.
					if (sjOn && sjCfg.pipe_sibling !== false) {
						for (let j = i + 1; j < items.length; j++) {
							const nx = items[j];
							if (nx.type === "black" && !String(nx.text ?? "").trim()) continue;
							const spanText = String(nx.text ?? "").trim();
							if (nx.type === "tag" && !nx.parse?.primary
								&& (nx.parse?.class === "instruction" || nx.parse?.class === "noise")
								&& (/^\|/.test(spanText) || /\|\s*$/.test(payload))
								// an awaiting-translation note span is never the title half
								&& !/(awaiting|translation|insert|module title)/i.test(spanText)) {
								const spanHalf = `${spanText.replace(/\*/g, "").trim()} ${String(nx.blackAfter ?? "").replace(/\*/g, "").trim()}`.trim();
								payload = `${payload} ${spanHalf}`.trim();
								payloadJoined = true;
								tbConsumed.add(j);
							}
							break;   // only the IMMEDIATE non-empty item
						}
					}
				} else {
					payload = stripCode((it.blackAfter.trim() || this.#norm.RenderText(it.text)).replace(/\*/g, "").trim());
				}
				// The BLL phonics subject group writes its title bars in the shape "Module N -
				// <letter teams>" (found on module BLL232) — the human developer strips the
				// "Module N" prefix out and moves it into the overview page's #module-code chip
				// instead, keeping only the remainder (lower-cased) as the visible title. This
				// strips that prefix here; the titleBar.modulePrefix flag set below drives both
				// the chip text and the lowercase styling span over in SkeletonBuilder. Measured
				// against the corpus: applies to 49 out of 49 BLL modules, 0 non-BLL modules, and
				// 0 over-fires (see outputs/_measure_module_prefix.py).
				// Data flag: header.title_split.module_prefix_split
				// Env toggle: MODPREFIX_OFF (reverts to a generic "Module" chip and an un-split title)
				const mpCfg = tsCfg.module_prefix_split;
				const mpOn = mpCfg && mpCfg.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.MODPREFIX_OFF);
				if (mpOn && mpCfg.pattern) {
					const mp = payload.match(new RegExp(mpCfg.pattern, "i"));
					if (mp) {
						titleBar.rawEnglish = payload;   // keep the full title so a mid-doc alias still de-dups
						payload = mp[1].trim();          // the remainder becomes the title
						titleBar.modulePrefix = true;    // overview chip "Module N" + lowercase span
					}
				}
					// The BLL phonics subject group's OVERVIEW (i.e. parent) title bar has yet
					// another distinct shape: "LEARNING/TEACHING THE SOUNDS – <letter teams>"
					// (found on module BLL210 — this is a different shape from the lesson-level
					// "Module N - ..." prefix handled just above). The human developer de-capitalises
					// the leading phrase (turning "LEARNING THE SOUNDS" into "Learning the
					// sounds") and wraps ONLY the letter-teams that follow the dash in a
					// lowercase-styled span. The general #normaliseTitleCase helper elsewhere
					// skips this string entirely, because the already-lowercase phonics tail
					// makes the whole string fail the "is this wholly upper-case" check it uses.
					// So this splits the title explicitly into a de-capitalised lead, the
					// separator, and the tail; the titleBar.phonics* fields set below drive
					// SkeletonBuilder's dedicated phonics title rendering and its
					// chip-derived-from-module-code behaviour.
					// Data flag: header.title_split.phonics_overview_split
					// Env toggle: PHONICSTITLE_OFF
					const poCfg = tsCfg.phonics_overview_split;
					const poOn = poCfg && poCfg.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env.PHONICSTITLE_OFF);
					if (poOn && poCfg.pattern && !titleBar.modulePrefix && !payload.includes("|")) {
						const po = payload.match(new RegExp(poCfg.pattern, "i"));
						if (po) {
							titleBar.rawEnglish = payload;
							titleBar.phonicsLead = this.#normaliseTitleCase(po[1].trim());
							titleBar.phonicsSep = po[2].trim();
							titleBar.phonicsTail = po[3].trim();
							titleBar.english = `${titleBar.phonicsLead} ${titleBar.phonicsSep} ${titleBar.phonicsTail}`;
							titleBar.teReo = "";
							titleBar.single = true;
							continue;                        // skip the normal split/normalise for this payload
						}
					}
				let parts;
				if (payload.includes("|")) parts = payload.split("|");
				else if (/\n/.test(payload)) parts = payload.split(/\n+/);
				else if (/\S {2,}\S/.test(payload)) parts = payload.split(/ {2,}/);
				else parts = this.#bilingualPunctSplit(payload) ?? this.#bilingualDashSplit(payload)
					?? this.#bilingualCharSplit(payload) ?? this.#bilingualCaseSplit(payload) ?? [payload];
				parts = parts.map((s) => s.trim()).filter(Boolean);
				// Sometimes a writer leaves the template's own boilerplate prompt text
				// ('MODULE TITLE TE REO' or 'MODULE TITLE') GLUED directly onto the title
				// payload, with the real Te Reo title typed immediately after it (for example
				// module XMES103: 'My Family – Who I live with MODULE TITLE TE REO: Taku
				// Whānau'). The placeholder filter further below only knows how to drop a
				// marker that occupies an ENTIRE split part on its own (like module OSGM501's
				// 'GAMING SAFELY | MODULE TITLE TE REO'); a marker that's glued onto the
				// MIDDLE or END of a real piece of text never reaches that filter and would
				// otherwise leak straight into one combined "<h1>". This EXPLODES each split
				// part at any glued boilerplate marker found inside it (dropping the marker
				// text itself), then reuses the normal English/Te-Reo two-heading assignment
				// logic. Two guards protect this: (a) the payload must NOT START with a marker
				// (a marker at the very start signals a Te-Reo-first title instead, a
				// different, recorded case — module CEDT104); (b) a part that is a marker in
				// its ENTIRETY is left alone for the placeholder filter below to handle
				// normally, so that filter's own drop-tracking flag and warning stay
				// unaffected (module OSGM501's output is unchanged by this). The markers
				// matched come from the extra_placeholders data list (with the bare word 'te
				// reo' deliberately excluded, since that can be a genuine Te Reo word in a
				// real title — see module CEDW201), matched longest-match-first. Measured
				// across all 430 module directories (see outputs/_measure_titlemarker.cjs):
				// fixes exactly 12 modules (11 of which were being actively tracked), with 0
				// over-fires.
				// Data flag: header.title_split.marker_glue_split
				// Env toggle: TITLEMARKSPLIT_OFF
				const mgCfg = tsCfg.marker_glue_split;
				const mgOn = mgCfg && mgCfg.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.TITLEMARKSPLIT_OFF);
				if (mgOn && !payloadJoined && parts.length) {
					const glue = (tsCfg.placeholder_title_rule?.extra_placeholders ?? [])
						.map((s) => Utils.Fold(s).replace(/\s+/g, " ").trim())
						.filter(Boolean).sort((a, b) => b.length - a.length);
					const foldPay = Utils.Fold(payload).replace(/\s+/g, " ").replace(/^[[\]\s]+/, "").trim();
					const startsMk = glue.some((mk) => foldPay.startsWith(mk));
					if (glue.length && !startsMk) {
						const glueChars = mgCfg.trailing_glue_chars ?? ":：–—-|";
						const cls = glueChars.replace(/[\\\]^-]/g, "\\$&");
						const alt = glue.map((mk) => mk.split(" ").map((w) => Utils.RegexEscape(w)).join("\\s+")).join("|");
						const mkRe = new RegExp(`\\s*(?:${alt})\\s*[${cls}]*\\s*`, "giu");
						const edge = new RegExp(`^[\\s${cls}]+|[\\s${cls}]+$`, "g");
						const isWhole = (p) => glue.includes(Utils.Fold(p).replace(/[[\]|]+/g, "").replace(/\s+/g, " ").trim());
						const exploded = [];
						let fired = false;
						for (const p of parts) {
							if (isWhole(p)) { exploded.push(p); continue; }   // a whole-marker part is left for the placeholder filter below to handle
							mkRe.lastIndex = 0;
							if (!mkRe.test(p)) { exploded.push(p); continue; }
							mkRe.lastIndex = 0;
							const segs = p.split(mkRe).map((s) => s.replace(edge, "").trim()).filter(Boolean);
							if (segs.length) { exploded.push(...segs); fired = true; }
							else exploded.push(p);
						}
						if (fired) { parts = exploded; titleBar.markerGlueSplit = true; }
					}
				}
				// Strips an ORPHAN boundary separator: this handles the case where a writer
				// typed a "soft" separator character ALONGSIDE a "hard" one that already got
				// split on earlier (for example "Visual Literacy /  Mātau Reo Ataata", from
				// modules SSFUN05/08 — the double-space branch above splits on the double-space
				// first, leaving the '/' character orphaned as a stray leading/trailing
				// character on one half). The human developer never ships a title "<h1>" with a
				// leading or trailing separator character (measured: 0 out of 405 human
				// titles), so trimming an orphaned one off at a half's boundary is provably
				// matching human behaviour. This is scoped to only the characters listed in the
				// strip_boundary_separators data ('/' by default; an orphaned dash or colon are
				// separate, still-deferred cases). The trimming regex only ever touches a
				// LEADING or TRAILING separator character — never one that's internal to a
				// half — so it safely applies to single-title payloads too (for example module
				// ENGI401's "A Moment in Time /", whose Te Reo half turned out to be an
				// unfilled placeholder living in a separate span) without ever disturbing a
				// single-language title's own intentional internal punctuation (a title like
				// "TV / Radio" correctly keeps its slash).
				// Env toggle: TITLESEPTRIM_OFF
				const sbsCfg = tsCfg.strip_boundary_separators;
				const sbsOn = sbsCfg && !(typeof process !== "undefined" && process.env && process.env.TITLESEPTRIM_OFF);
				if (sbsOn && parts.length) {
					const cls = String(sbsCfg).replace(/[\\\]^-]/g, "\\$&");   // escape for a char class
					const edge = new RegExp(`^[\\s${cls}]+|[\\s${cls}]+$`, "g");
					parts = parts.map((s) => s.replace(edge, "").trim()).filter(Boolean);
				}
				// PLACEHOLDER title-half: writers sometimes leave the second title as a
				// literal LABEL ("Te Reo" — i.e. "the language", meaning "Te Reo
				// translation goes here"), which the human replaces with the real
				// translation (XGF9001: WT "My Inner Compass | Te Reo" → human
				// "My Inner Compass" + "Te Takinga o taku wairua"). The real title is
				// NOT in the WT, so we must not SHIP the placeholder as an <h1>: drop it
				// and surface a red flag. Data list: header.title_split.placeholder_titles.
				// The placeholder list is extended with the 'MODULE TITLE TE REO'/'MODULE
				// TITLE' template boilerplate strings (found on module OSBY201) — a writer who
				// never replaced this boilerplate text has effectively NOT supplied that
				// title, so it needs to be dropped the same way any other placeholder is.
				// Data flag: header.title_split.placeholder_title_rule
				// Env toggle: TITLEPH_OFF (reverts to the smaller, original placeholder list,
				// and to always restoring a title rather than allowing an empty result)
				const before = parts.length;
				const kept = parts.filter((p) => {
					if (ph.includes(Utils.Fold(p).replace(/[\[\]\s]+/g, ""))) {
						run.AddNote("warn", "ContentConverter",
							`[TITLE BAR] title half is the placeholder "${p}" — the real title is not in the WT; dropped, not shipped as an <h1>. Add the title to the source.`);
						run.CountRedFlag();
						return false;
					}
					return true;
				});
				// record that at least one placeholder was dropped so PageAssembler does
				// NOT mis-promote a surviving REAL title to the Te Reo slot (the Course
				// backup's "lone title = Te Reo" assumption only holds when nothing was dropped)
				titleBar.droppedPlaceholder = phRuleOn && kept.length < before;
				if (kept.length) parts = kept;
				else if (phRuleOn && before) parts = [];   // ALL placeholders were dropped → empty → the Course-name backup supplies the English title instead
				// When the placeholder rule is switched off, this never allows the title list to
				// end up empty — it always restores something rather than shipping nothing.
				// Human developers virtually never ship an ALL-CAPS header title (measured: only
				// 2 out of roughly 2,200 in the whole corpus) — they normalise it to ordinary
				// sentence case. So sentence-case a title the writer typed in all caps; leave a
				// title that already has normal mixed casing untouched.
				// When a payload was JOINED together from separate spans above and split into
				// exactly 2 parts, with exactly ONE of them being Māori-lettered (using the
				// same Māori-alphabet-letters test used elsewhere in this file), this assigns
				// ENGLISH FIRST regardless of which order the parts came in — the human
				// developer's gold output ships English-first on modules TEFUN03 and ANZH101,
				// and doing so also keeps #pageEnglishTitle set to the actual English text, so
				// the overview heading de-duplication logic elsewhere still correctly recognises
				// the English title. This is SCOPED to joined payloads only — the ordinary
				// dash-split and character-split paths keep the payload's original order as-is
				// (module CEDW501's gold output ships the Te Reo half first there, so reordering
				// would be wrong for that case).
				const maoriHalf = (s) => {
					const L = String(s ?? "").replace(/[^A-Za-zĀĒĪŌŪāēīōū]/g, "");
					return !!L && !/[bcdfjlqsvxyz]/i.test(L);
				};
				if (payloadJoined && parts.length === 2 && maoriHalf(parts[0]) !== maoriHalf(parts[1])) {
					titleBar.english = this.#normaliseTitleCase(parts[maoriHalf(parts[0]) ? 1 : 0]);
					titleBar.teReo = this.#normaliseTitleCase(parts[maoriHalf(parts[0]) ? 0 : 1]);
				} else {
					titleBar.english = this.#normaliseTitleCase(parts[0] ?? "");
					titleBar.teReo = this.#normaliseTitleCase(parts.slice(1).join(" ").trim());
				}
				// flag a SINGLE-title payload (0 or 1 real title) so PageAssembler can decide
				// whether the lone title is actually Te Reo (no English pair)
				// and pull the English from the front-matter Course
				titleBar.single = parts.length <= 1;
				// A Māori-language BLACK text line found DIRECTLY following the "[TITLE BAR]"
				// payload is recognised as the module's Te Reo title, which the human developer
				// ships as an additional header "<h1>" (or a pair of them) — module AGH1006's
				// gold output splits its colon-separated pair into TWO separate h1 lines ('Te
				// whakatō tipu kākāriki' / 'Te whakahaere hātepe ahumāra'). This only fires
				// when the title-bar payload itself yielded just a single (English-only) title;
				// the candidate line must be the FIRST non-empty item found after the title bar,
				// must pass the Māori-alphabet-letters test used elsewhere in this file
				// (deliberately NOT the broader mtkFlag signal, which over-fires on
				// non-bilingual modules), and must be a plausible title length. The matched line
				// is CONSUMED so it stops being separately rendered as ordinary body or menu
				// text. Measured across all 430 module directories through the live pipeline
				// (see outputs/_measure_titleh1.cjs): this pattern applies to EXACTLY two
				// modules, AGH1005 and AGH1006, with zero over-fires anywhere else.
				// Data flag: header.title_split.te_reo_line
				// Env toggle: TEREOLINE_OFF
				const trlCfg = tsCfg.te_reo_line;
				const trlOn = trlCfg && trlCfg.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.TEREOLINE_OFF);
				if (trlOn && parts.length <= 1 && !titleBar.teReo) {
					const nonMaori = new RegExp(trlCfg.non_maori_letters ?? "[bcdfjlqsvxyz]", "i");
					for (let j = i + 1; j < items.length; j++) {
						const nx = items[j];
						if (tbConsumed.has(j)) continue;
						if (nx.type === "black" && !String(nx.text ?? "").trim()) continue;
						if (nx.type === "black") {
							const clean = String(nx.text).replace(/\*\*?/g, "").trim();
							const letters = clean.replace(/[^A-Za-zĀĒĪŌŪāēīōū]/g, "");
							const words = clean.split(/\s+/).filter(Boolean).length;
							if (letters && !nonMaori.test(letters) && words <= (trlCfg.max_words ?? 20)) {
								let lines = [clean];
								if (trlCfg.pair_split !== false && (clean.match(/[:：]/g) || []).length === 1) {
									const cp = clean.split(/\s*[:：]\s*/).map((s) => s.trim()).filter(Boolean);
									if (cp.length === 2) lines = cp;
								}
								titleBar.teReoLines = lines.map((s) => this.#normaliseTitleCase(s));
								titleBar.teReo = titleBar.teReoLines[0];
								titleBar.single = false;   // two languages are genuinely present
								tbConsumed.add(j);
							}
						}
						break;   // only the IMMEDIATE non-empty item; anything else ends the look-ahead
					}
				}
				continue;
			}

			// ---- overview: everything between title bar and [MODULE
			//      INTRODUCTION] is menu source (when a menu exists) --------
			// The captured fundamentals "[Overview]" region (see the funIdxSet logic above)
			// also joins the menu source here, with its items marked "_funLi" so MenuBuilder
			// knows to compose them into its two-column Learning-Intentions/Success-Criteria
			// layout.
			if (page.isOverview && menuType !== "none"
				&& ((introIdx > 0 && i < introIdx) || overviewMenuIdx.has(i)
					|| (funIdxSet && funIdxSet.has(i)))) {
				// A standalone red "Phase N" delimiter span belongs to the BODY-side phase
				// machinery, never to the menu (it renders nothing if placed in the menu
				// anyway); see the gating logic set up further above for this.
				if (redPhaseToBody && redPhaseToBody.has(i)) { bodyItems.push(it); continue; }
				if (funIdxSet && funIdxSet.has(i)) it._funLi = true;
				menuItems.push(it);
				continue;
			}

			// ---- lesson: the [Lesson Overview] section is the menu -------
			// menu region = (overviewIdx .. lessonMenuEnd), computed above:
			// ends at [Lesson content] when present, else the first heading.
			// With the lesson_menu_section_stop flag on, menu membership is decided by the
			// SECTION-STOP set built above (the text runs making up the Lesson-Overview intro
			// plus the Lesson-Content section) — a structural element like an alert, button,
			// or image sitting mid-region correctly stays in the ordinary body instead (the
			// CED subject family's shape, described above).
			if (!page.isOverview && menuType !== "none" && overviewIdx >= 0
				&& i >= overviewIdx
				&& (lessonMenuEnd < 0 ? false : i < lessonMenuEnd)) {
				// Section marker tags carry no render content of their own (also skip the
				// "[Lesson content]" marker itself here, now that the menu region extends
				// past it)
				if (i === overviewIdx || (intentOn && i === contentIdx)) continue;
				if (menuIdxSet && !menuIdxSet.has(i)) { bodyItems.push(it); continue; }
				menuItems.push(it);
				continue;
			}

			bodyItems.push(it);
		}
		return { titleBar, menuItems, bodyItems };
	};

	// =======================================================================
	// EMITTERS (one per concern; all forms come from Emit_Templates.json)
	// =======================================================================

	/**
	 * Finds the documented writer INSTRUCTIONS embedded inside a widget bundle so they
	 * can be RETAINED and rendered instead of silently discarded, and generalises across
	 * EVERY interactive-widget type: the writer's note-to-developer can ride inside a TABLE
	 * cell (for example a speechBubble's image cell might carry a Creative Services note), a
	 * captured member item, or the widget's own opener tag. This harvests every red
	 * text span that the shared normaliser classifies as an instruction (using the same
	 * Instruction_Cues.json vocabulary the whole app already shares — cue words like
	 * "cs", "dev", "note", "please", "can you", and similar), plus any instructions the
	 * interactive-scanner already found on its own (bundle.instructions), de-duplicates
	 * them, and the caller then renders them as a red "<p>" note placed after the widget.
	 * This is CAPTURE-NEUTRAL: it only READS the bundle and never mutates it, so widget
	 * builds and the bundle's captured ranges are completely unaffected — this purely
	 * SURFACES writer instructions that would previously have been silently dropped.
	 */
	static #bundleInstructions(bundle) {
		const seen = new Set();
		const out = [];
		const add = (t) => {
			const s = String(t ?? "").replace(/\s+/g, " ").trim();
			if (s && !seen.has(s)) { seen.add(s); out.push(s); }
		};
		for (const t of (bundle.instructions ?? [])) add(t);
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		const scan = (text) => {
			for (const m of String(text ?? "").matchAll(RED)) {
				let parse;
				try { parse = this.#norm.Parse(m[1]); } catch { parse = null; }
				if (parse && (parse.class === "instruction" || parse.instructionFragment)) {
					add(m[1].replace(/^[\s[]+|[\s\]]+$/g, ""));
				}
			}
		};
		for (const tbl of (bundle.tables ?? [])) {
			for (const row of (tbl.rows ?? [])) for (const cell of row) scan(cell);
		}
		for (const it of [...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])]) {
			scan(it?.text);
			scan(it?.blackAfter);
		}
		return out;
	};

	/**
	 * [MTKquiz] — the "Go to quiz" button family (ROUND 232 — Change Ledger
	 * CL-0038, 16 Jul; Chris). Four small pieces, all gated by the SAME data
	 * flag + env toggle as the TagNormaliser retag that feeds them
	 * (Tag_Lexicon._meta.mtk_quiz_retag / MTKQUIZ_OFF — with the retag off no
	 * item ever carries the "mtk quiz" tag, so every one of these is dormant
	 * and the corpus is byte-identical).
	 *
	 * #mtkQuizPrepass — THE ADJACENT WRITER-BUTTON ABSORB (the dedup rule).
	 * At most of the measured sites the writer typed their OWN quiz button
	 * next to the MTK marker — "[button] Go to quiz" directly above it
	 * (TEFUN02/TEFUN03), "[Button] Quiz" above (TEFUN06/07/08), "[Button] Go
	 * to quiz." after the box's heading + lead (ARFUN02/ARFUN04), or a
	 * standalone "[Go to quiz]" red span inside the same activity (HPRE301,
	 * where that span otherwise becomes an empty mcq placeholder bundle). The
	 * human ships exactly ONE anchored button per quiz, at the writer's
	 * button position. So: for each item carrying the "mtk quiz" tag, walk a
	 * small window (window_back items up, window_forward down, skipping blank
	 * lines, STOPPING at another mtk item / an [Activity] opener / any
	 * section-page-closer boundary so the scan can never leak across
	 * activities) looking for a writer quiz button — a [button]-family
	 * ELEMENT whose label folds into button_label_pattern, or a span whose
	 * whole folded text matches marker_span_pattern. When found, the button
	 * item (or its thin bundle) is flagged to render as the CANONICAL CL-0038
	 * anchored button (_mtkQuizAnchor / bundle._mtkQuizBtn) and the mtk item
	 * is flagged _mtkButtonAbsorbed so it ships its To Do note WITHOUT a
	 * second button. A [go to quiz] span OUTSIDE any mtk window is untouched
	 * (the corpus-wide standalone class, ~40 modules, is a recorded
	 * follow-up, NOT this rule).
	 */
	static #mtkQuizPrepass(bodyItems, bundles, tpl) {
		const cfg = tpl.interactive_builders?.mtk_quiz;
		if (!cfg || cfg.enabled === false) return;
		if (typeof process !== "undefined" && process.env && process.env.MTKQUIZ_OFF) return;
		const hasMtk = (c) => c.type === "tag" && (c.parse?.tags ?? []).some((t) => t.tag === "mtk quiz");
		const lblRe = new RegExp(cfg.button_label_pattern, "i");
		const mrkRe = new RegExp(cfg.marker_span_pattern, "i");
		const isBoundary = (c) => hasMtk(c)
			|| (c.parse?.tags ?? []).some((t) => t.tag === "activity" && t.directive === "CONTAINER_OPEN")
			|| ["PAGE_BOUNDARY", "SECTION_MARKER", "CONTAINER_CLOSE"].includes(c.parse?.primary?.directive);
		const isBtnItem = (c) => {
			if (c.type !== "tag" || !c.parse?.primary) return false;
			if (c.parse.primary.directive !== "ELEMENT" || !(c.parse.primary.tag || "").includes("button")) return false;
			const label = ((this.#norm?.RenderText(c.text) || "") + " " + (c.blackAfter || ""))
				.replace(/\*/g, "").replace(/\s+/g, " ").trim();
			return lblRe.test(label);
		};
		const isMarkerSpan = (c) => c.type === "tag"
			&& mrkRe.test(String(c.parse?.folded ?? "").trim());
		const claim = (c) => {
			// A [button] item swallowed into some widget's bundle never reaches the
			// element dispatcher, so an upgrade flag on it would LOSE the button
			// entirely (caught live on TEFUN03, where the writer's buttons ride the
			// same bundle as the MTK marker) — only an UNCONSUMED button item can be
			// claimed; otherwise the mtk marker keeps emitting its own button.
			if (isBtnItem(c) && c.consumedBy === undefined && !c._consumed) { c._mtkQuizAnchor = true; return true; }
			if (isMarkerSpan(c)) {
				if (c.consumedBy !== undefined && bundles[c.consumedBy]) bundles[c.consumedBy]._mtkQuizBtn = true;
				else if (c.consumedBy === undefined && !c._consumed) c._mtkQuizAnchor = true;
				else return false;
				return true;
			}
			return false;
		};
		// One window step. Blank lines are free; boundaries stop the walk; an
		// item already CONSUMED into some widget's bundle is INVISIBLE to the
		// window (it lives inside that widget's box, not between the marker and
		// its button — without this, the members a bundle captured between an
		// opener-riding marker and the writer's button exhausted the window,
		// ARFUN04-1H) — except that a consumed [Go to quiz] MARKER span still
		// claims its own bundle as the button.
		const step = (c, state) => {
			if (c.type === "black" && !(c.text ?? "").trim()) return "skip";
			if (isBoundary(c)) return "stop";
			if (c.consumedBy !== undefined || c._consumed) {
				if (isMarkerSpan(c) && c.consumedBy !== undefined && bundles[c.consumedBy]) {
					bundles[c.consumedBy]._mtkQuizBtn = true;
					return "found";
				}
				return "skip";
			}
			state.seen++;
			return claim(c) ? "found" : "next";
		};
		for (let i = 0; i < bodyItems.length; i++) {
			const it = bodyItems[i];
			if (!hasMtk(it)) continue;
			let found = false;
			const st = { seen: 0 };
			for (let k = i - 1; k >= 0 && st.seen < (cfg.window_back ?? 2); k--) {
				const r = step(bodyItems[k], st);
				if (r === "stop") break;
				if (r === "found") { found = true; break; }
			}
			if (!found) {
				st.seen = 0;
				for (let k = i + 1; k < bodyItems.length && st.seen < (cfg.window_forward ?? 5); k++) {
					const r = step(bodyItems[k], st);
					if (r === "stop") break;
					if (r === "found") { found = true; break; }
				}
			}
			if (found) it._mtkButtonAbsorbed = true;
		}
	}

	/**
	 * #mtkQuizEmit — the marker's own rendering: the canonical anchored
	 * button (href="#", target=_blank — the dev wires the D2L quicklink at
	 * publish time; gold's populated quickLink hrefs ARE that wiring, so the
	 * blank href is an INTENTIONAL pre-publish divergence) followed by ONE
	 * Designer/Developer To Do note (kind "todo", class cv2-note =
	 * gate-excluded) carrying the writer's raw quiz spec — the span's own
	 * text, so modifier prose like "supports engagement, audio, video, file
	 * sharing" or "should go to teacher dropbox" (which per the rule does NOT
	 * attach a dropbox wrapper) is never silently stripped (the round-43
	 * principle). When the pre-pass absorbed the button into a writer button
	 * nearby, only the note ships here.
	 */
	static #mtkQuizEmit(it, run) {
		const cfg = DataService.Data.EmitTemplates.interactive_builders?.mtk_quiz;
		if (!cfg || cfg.enabled === false) return [];
		if (typeof process !== "undefined" && process.env && process.env.MTKQUIZ_OFF) return [];
		if (it._mtkQuizEmitted) return [];
		it._mtkQuizEmitted = true;
		const out = [];
		const spec = String(it.text ?? "")
			.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "")
			.replace(/\s+/g, " ").trim();
		if (!it._mtkButtonAbsorbed) out.push(cfg.button_html);
		out.push(NotesAndComments.redFlag(Utils.FillTemplate(cfg.todo_note,
			{ spec: spec || "(no further spec given)" }), run, "todo"));
		return out;
	}

	/**
	 * #mtkQuizBundleTail — the bundle-side hook. An mtk marker can be
	 * CAPTURED into a neighbouring widget's bundle (TEFUN03/06/07/08: the
	 * "[Quiz]- triggers engagement" opener's member walk swallows the
	 * following MTK span; ARFUN04: the marker rides the dragAndDrop opener
	 * span itself), in which case the item never reaches the main loop. At
	 * the bundle's emit, every mtk-carrying opener/member ships its
	 * button+note straight after the widget box; a bundle the pre-pass
	 * claimed as the quiz BUTTON ([Go to quiz]-span bundles) additionally
	 * ships the canonical button (and, when THIN — no content members — its
	 * empty placeholder box is suppressed entirely via #mtkQuizBundleThin:
	 * the box would have held nothing but the marker's own raw line).
	 */
	static #mtkQuizBundleTail(bundle, run, openerIt = null) {
		const cfg = DataService.Data.EmitTemplates.interactive_builders?.mtk_quiz;
		if (!cfg || cfg.enabled === false) return [];
		if (typeof process !== "undefined" && process.env && process.env.MTKQUIZ_OFF) return [];
		const out = [];
		// openerIt = the loop item whose consumedBy triggered this bundle's emit —
		// the bundle's OPENING span itself, which sits in neither openerItems nor
		// memberItems (ARFUN04-1H's dragAndDrop opener carries the mtk co-tag).
		for (const m of [openerIt, ...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])]) {
			if (m && m.type === "tag" && (m.parse?.tags ?? []).some((t) => t.tag === "mtk quiz")) {
				out.push(...this.#mtkQuizEmit(m, run));
			}
		}
		if (bundle._mtkQuizBtn && !bundle._mtkQuizBtnEmitted) {
			bundle._mtkQuizBtnEmitted = true;
			out.push(cfg.button_html);
		}
		return out;
	}

	/**
	 * GO-TO-JOURNAL TAIL ABSORB (ROUND 239 — Dev-Feedback R2, B4; SCCH302-03
	 * activity 3D / 4A). A bundle-owned activity box closes at its widget's end,
	 * so a writer's "[button] Go to Journal" sitting AFTER the widget's own end
	 * tag but still BEFORE [end activity] used to escape into its own row below
	 * the closed box. The human ships the templated <h4 class="goJournal"> INSIDE
	 * the activity. Called at the bundle-owned close site (the r232
	 * mtkQuizBundleTail placement class): walks forward from the bundle's opening
	 * item, skipping bundle-consumed items, blank lines and a stray non-activity
	 * CONTAINER_CLOSE (the widget's own unconsumed end tag); if the FIRST real
	 * item is a go-to-journal [button] (the same discriminator as the buttons
	 * branch — explicit label or the anchored alias span, no URL), it is
	 * consumed here and the h4 returns for emission inside the still-open box.
	 * Anything else stops the walk — a following activity's own button is never
	 * reached (its opener is a CONTAINER_OPEN, which stops the walk first).
	 * Data flag: buttons.go_journal.absorb_into_activity   Env toggle: GOJOURNAL_OFF
	 */
	static #goJournalTail(bodyItems, i, run, bundle = null) {
		const gjCfg = DataService.Data.EmitTemplates.buttons?.go_journal;
		if (!gjCfg || gjCfg.enabled === false || gjCfg.absorb_into_activity === false) return [];
		if (typeof process !== "undefined" && process.env && process.env.GOJOURNAL_OFF) return [];
		const lblRe = new RegExp(gjCfg.label_match, "i");
		const aliasRe = new RegExp(gjCfg.raw_match, "i");
		const h4 = () => [Utils.FillTemplate(gjCfg.form,
			{ label: Utils.EscapeHtml(gjCfg.label ?? "Go to your journal") })];
		const isGoJournal = (c) => {
			const p = c.type === "tag" ? c.parse?.primary : null;
			if (!p || p.directive !== "ELEMENT" || p.tag !== "button") return false;
			const url = c.block?.links?.[0]?.target
				?? ((c.blackAfter ?? "").match(/https?:\/\/[^\s\]]+/)?.[0] ?? "");
			if (url) return false;
			const explicit = (this.#norm.RenderText(c.text) || "").replace(/\*/g, "").trim()
				|| (c.blackAfter || "").replace(/\*/g, "").trim();
			return (explicit && lblRe.test(explicit))
				|| aliasRe.test(Utils.Fold(String(c.text ?? "")).trim());
		};
		// A go-to-journal [button] the widget's member walk CAPTURED as a trailing
		// member (a writer's 4A shape: no [end click and drop], so the button rode
		// into the bundle like an Undo/Reset control) still ships its h4 inside the
		// box — the r232 mtkQuizBundleTail pattern: the member stays verbatim in the
		// raw hand-off dump, the canonical form emits in the live rendering.
		if (bundle) {
			for (const m of (bundle.memberItems ?? [])) {
				if (m && isGoJournal(m)) return h4();
			}
		}
		for (let j = i + 1; j < bodyItems.length && j <= i + 120; j++) {
			const c = bodyItems[j];
			if (!c) break;
			if (c._consumed || c.consumedBy !== undefined && c.consumedBy !== null) continue;
			if (c.type === "black" && !String(c.text ?? "").trim()) continue;
			const p = c.type === "tag" ? c.parse?.primary : null;
			// a stray unconsumed widget end tag ([end click and drop]) — already closed
			if (p && p.directive === "CONTAINER_CLOSE" && p.tag !== "end activity"
				&& !/\bactivity\b/i.test(p.tag ?? "")) continue;
			if (p && p.directive === "ELEMENT" && p.tag === "button" && isGoJournal(c)) {
				c._consumed = true;
				return h4();
			}
			break;   // the first real item was not a go-to-journal button — stop
		}
		return [];
	}

	/** A pre-pass-claimed BUTTON bundle with no real content members — its
	 *  placeholder box is suppressed (the canonical button replaces it). */
	static #mtkQuizBundleThin(bundle) {
		if (!bundle._mtkQuizBtn) return false;
		if (typeof process !== "undefined" && process.env && process.env.MTKQUIZ_OFF) return false;
		return (bundle.memberItems ?? []).every((m) =>
			m.type !== "table"
			&& !(m.blackAfter ?? "").trim()
			&& !(m.type === "black" && (m.text ?? "").trim()));
	}

	/**
	 * ELEMENT dispatcher: headings, body, image, video/audio, buttons,
	 * tables, embeds, inputs — content gathered embedded-then-following.
	 *
	 * RETURNS an array of HTML strings. May mark following black items
	 * _consumed when the element's content spans paragraphs.
	 */
	static #element(it, bodyItems, i, stack, run) {
		const tpl = DataService.Data.EmitTemplates;
		const tag = it.parse.primary.tag;
		const out = [];

		// instruction fragments riding in the same span flag first, in place
		if (it.parse.instructionFragment) {
			out.push(NotesAndComments.redFlag(it.text, run, "cs"));
		}

		// ---- [MTKquiz] → the canonical "Go to quiz" button + To Do note ----
		// (ROUND 232 — CL-0038; see #mtkQuizEmit above. The retag made this an
		// ELEMENT precisely so the writer's quiz content after it flows to the
		// normal body render instead of being swallowed into a bundle dump.)
		if (tag === "mtk quiz") {
			out.push(...this.#mtkQuizEmit(it, run));
			return out;
		}

		// ---- headings ----------------------------------------------------
		if (["h1", "h2", "h3", "h4", "h5", "heading", "activity heading"].includes(tag)) {
			const digit = /^h\d$/.test(tag) ? parseInt(tag[1], 10) : 2;
			// In body context, the writer's own heading digit drifts DOWN by one level (this
			// is the ground-truthed convention documented in the tag-interpretation rules),
			// clamped to stay within the valid body heading range. CEILING: this is normally
			// h5, but when the page re-leveller (#relevelHeadings) is active, it goes on to
			// RANK the page's distinct heading levels back down into the h3–h5 range anyway —
			// so this gives it ONE extra intermediate level of headroom (h6) to work with
			// first. Without that headroom, a writer's "[H5]" heading would clamp to h5 the
			// same as a "[H4]" heading, making them indistinguishable; with the extra h6
			// level, a 3-level "[H3]"/"[H4]"/"[H5]" page correctly re-levels to h3/h4/h5
			// instead of incorrectly collapsing "[H5]" up into "h4" (seen on module
			// OSAI401-04). #relevelHeadings always normalises any leftover h6 back down to a
			// valid level afterwards; when re-levelling is switched off entirely, the ceiling
			// stays at h5 so an h6 tag never leaks into the final output.
			const l2e = tpl.elements.heading.logical_to_element;
			const reOn = (tpl.body_region?.heading_relevel?.enabled !== false)
				&& !(typeof process !== "undefined" && process.env && process.env.RELEVEL_OFF);
			const shifted = Math.min(Math.max(digit + l2e.body_shift, 2), reOn ? (l2e.relevel_headroom ?? 6) : 5);

			// content: embedded payload first (ORIGINAL case via RenderText —
			// "[Insert H3: Emotion]" → "Emotion"), then the following text
			const embedded = this.#norm.RenderText(it.text);
			// PRESERVE inline **bold**/*italic* markup INSIDE the heading text itself (module
			// OSBY201-02's "What to do if **you bully** online?" is the example that
			// established this — the human developer keeps that inline bold). The raw markup
			// is kept for rendering via ListsAndRuns.inlineMarkup; a separate PLAIN copy (with
			// the markers stripped out) is used
			// only for the empty-check and the lesson-title de-duplication comparison below.
			// Env toggle: HEADINLINE_OFF (reverts to the older, asterisk-stripped/un-bolded heading)
			let raw = (embedded || it.blackAfter).trim();
			// the lesson-first "[H2] Lesson N: …" prefix strips — the number
			// already lives in the header/module-code
			raw = raw.replace(/^lesson\s+#?\d+(?:\.\d+)?[a-z]?\s*[:.\-–—]?\s*/i, "") || raw;
			let text = raw.replace(/\*/g, "").trim();
			if (!text.trim()) {
				out.push(NotesAndComments.redFlag(`Empty [${tag.toUpperCase()}] — the writer left a heading placeholder with no text.`, run));
				return out;
			}
			// LESSON-TITLE DE-DUP: the FIRST body heading that repeats the lesson
			// title (already promoted to the header <h1> by PageSplitter) is
			// CONSUMED — the human shows the lesson title once, in the header (723
			// human lesson pages don't repeat it in the body vs 35 that do). Only
			// the first body heading is a candidate, so a deeper repeat is untouched.
			if (!this.#firstBodyHeadingSeen && tag !== "activity heading") {
				this.#firstBodyHeadingSeen = true;
				// The body's lesson heading often arrives wrapped WHOLE in *italic* markers —
				// for example "[H2] *Lesson 3: Be kind online*" (found on module OSBY201-03) —
				// which means the leading "Lesson N:" strip earlier in this method (which is
				// anchored to match only at the very start of the string, "^lesson") misses it,
				// because the string actually starts with an asterisk character instead. That
				// left the "Lesson N:" prefix surviving into the `text` variable, which then
				// prevented the de-duplication check below from ever matching against the
				// already-prefix-free page title shown in the header "<h1>" — resulting in a
				// DUPLICATE title appearing in the body (measured across 310 pages in the
				// corpus; the human developer keeps a duplicate on only 7 of them). The fix
				// strips a leading "Lesson N:" prefix from BOTH sides of the comparison below
				// (the header's page title is already prefix-free, so this makes the comparison
				// fair). This only affects the de-duplication TEST — the actual rendered output
				// of a kept heading is completely unchanged either way.
				// Data flag: body_region.lesson_title_dedup.strip_lesson_prefix
				// Env toggle: LESSONPFX_OFF
				const _ddCfg = tpl.body_region?.lesson_title_dedup;
				const _pfxOn = (_ddCfg?.strip_lesson_prefix !== false)
					&& !(typeof process !== "undefined" && process.env && process.env.LESSONPFX_OFF);
				const _stripLessonPfx = (s) => _pfxOn
					? (String(s).replace(/^lesson\s+#?\d+(?:\.\d+)?[a-z]?\s*[:.\-–—]?\s*/i, "") || String(s))
					: String(s);
				if (this.#pageLessonTitle
					&& Utils.Fold(_stripLessonPfx(text)).replace(/\s+/g, "") === Utils.Fold(_stripLessonPfx(this.#pageLessonTitle)).replace(/\s+/g, "")) {
					// keep any genuinely-following body text (Part-3 "BOTH" case)
					if (embedded && it.blackAfter.trim()) out.push(...ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links));
					return out;   // the heading itself is in the header already
				}
			}
			// Keep a PARTIAL inline bold (a single bolded KEYWORD within the heading, as in
			// module OSBY201's "**you bully**") but FLATTEN a WHOLE-heading bold (a writer's
			// "**Learning Intentions**" style heading, which the human developer renders as
			// plain, non-bold text) — bolding every single "**"-wrapped heading would add a
			// "<b>" tag the human's version doesn't have, which regresses the skeleton
			// structure-matching gate. Env toggle: HEADINLINE_OFF (reverts to always
			// rendering the heading as plain, un-bolded text)
			const tTrim = raw.trim();
			// WHOLE-bold = removing every **bold** run leaves only separators (|, /, -, :) —
			// covers a single "**X**" AND a bilingual "**te reo |****English**" (both bold).
			const wholeBold = /\*\*/.test(tTrim)
				&& /^[\s|/\-–—:•]*$/.test(tTrim.replace(/\*\*[\s\S]*?\*\*/g, ""));
			const headInline = ((typeof process !== "undefined" && process.env && process.env.HEADINLINE_OFF) || wholeBold)
				? text : raw;
			// Strips whole or partial *italic* markup from a BODY heading (the human developer
			// ships body headings as plain text 99.5% of the time), excluding the ENG-reading
			// subject families (which keep italic for book/story titles) and bilingual/reo
			// modules. See #stripHeadingItalic below for the full explanation.
			out.push(this.#stripHeadingItalic(`<h${shifted}>${ListsAndRuns.inlineMarkup(headInline)}</h${shifted}>`, run));
			// Part-3 "BOTH" case: an embedded heading whose span is followed
			// by body text — the following text is the NEXT element's body
			if (embedded && it.blackAfter.trim()) {
				out.push(...ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links));
			}
			return out;
		}

		// ---- CAPTION mis-resolve guard (found on module ENGS302-00) --------
		// Tags like "[Insert caption with video]" / "[caption with image]" / "[Caption text
		// for image]" resolve to the EMBEDDED media word ("video" or "image") via the
		// longest-matching-suffix rule the tag normaliser uses, so without this guard the
		// media-handling branches below would try to build (or red-flag) a media element out
		// of what is actually just a CAPTION (this produced a spurious 'RED FLAG: [video]
		// with no URL found' warning on module ENGS302-00). When a media-resolved tag's RAW
		// text contains the word "caption", it really IS a caption, not a media reference: so
		// this renders its own text as ordinary body content instead, never attempting to
		// build a media embed or raise a red flag for it. The separate, bare
		// "[Caption]"/"[Insert caption]" data-marker sub-tag (used by the image-caption
		// widget) is a different code path and never reaches this guard.
		// Data flag: elements.caption_not_media
		// Env toggle: CAPTIONMEDIA_OFF
		if (["image", "video", "audio", "embed"].includes(tag)
			&& (tpl.elements?.caption_not_media?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.CAPTIONMEDIA_OFF)
			&& /\bcaption\b/i.test(it.text || "")) {
			const cap = (it.blackAfter && it.blackAfter.trim())
				? it.blackAfter : MediaBuilder.gatherFollowing(it, bodyItems, i);
			if (cap.trim()) out.push(...ListsAndRuns.renderBlackText(cap, run, it.block?.links));
			return out;
		}

		// ---- image (Mode P / Mode D — uniform per run) ---------------------
		if (tag === "image") {
			return out.concat(MediaBuilder.image(it, bodyItems, i, run));
		}

		// ---- video / audio --------------------------------------------------
		if (tag === "video" || tag === "audio") {
			// A "[video]" tag that is governed by a writer's "[all external links]"
			// instruction (found on module OSBY201-03) renders as an external-link BUTTON
			// instead of an embedded video player (its label comes from the video's own
			// italic title) — this is flagged ahead of time by a section-wide pre-pass.
			// Data flag: elements.all_external_links_videos
			// Env toggle: ALLEXTVID_OFF
			if (it._extLinkButton) {
				const ba = it.blackAfter ?? "";
				const vurl = it.block?.links?.[0]?.target ?? (ba.match(/https?:\/\/[^\s\]]+/)?.[0] ?? "");
				const vlabel = ba.replace(/https?:\/\/[^\s\]]+/g, "").replace(/\*/g, "").trim();
				if (vurl) {
					const eb = tpl.buttons["external link button"];
					out.push(Utils.FillTemplate(eb.form, {
						url: Utils.EscapeHtml(vurl),
						label: Utils.EscapeHtml(vlabel || eb.video_label || "Go to video"),
					}));
					return out;
				}
			}
			return out.concat(MediaBuilder.media(it, bodyItems, i, tag, run));
		}

		// ---- standalone content table marker --------------------------------
		if (tag === "table") {
			// the actual table block follows; it renders when reached
			if (it.blackAfter.trim()) out.push(...ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links));
			return out;
		}

		// ---- list marker -----------------------------------------------------
		if (tag === "list") {
			if (it.blackAfter.trim()) out.push(...ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links));
			return out;
		}

		// ---- buttons ---------------------------------------------------------
		if (tag.includes("button")) {
			// THE WRITER'S OWN QUIZ BUTTON at an [MTKquiz] site (ROUND 232 — CL-0038).
			// The pre-pass (#mtkQuizPrepass) flagged this [button] as the quiz's
			// button — "[Button] Go to quiz." (ARFUN02/ARFUN04) or "[Button] Quiz"
			// (TEFUN06/07/08) adjacent to the MTK marker. It renders as the CANONICAL
			// anchored CL-0038 form (label normalised to "Go to quiz", href="#"
			// blank for the dev's D2L quicklink) instead of the plain green
			// `<div class="button">` with the writer's ad-hoc label — the human ships
			// exactly this anchored form at every measured site. The MTK marker's own
			// emit was suppressed by the same pre-pass, so ONE button ships per quiz.
			if (it._mtkQuizAnchor) {
				const mq = tpl.interactive_builders?.mtk_quiz;
				if (mq && mq.enabled !== false) { out.push(mq.button_html); return out; }
			}
			const key = tpl.buttons[tag] ? tag : "button";
			const btn = tpl.buttons[key];
			let url = it.block?.links?.[0]?.target
				?? (it.blackAfter.match(/https?:\/\/[^\s\]]+/)?.[0] ?? "");
			// EXTERNAL LINK BUTTON handling: writers often drop this marker INLINE in the
			// middle of an ordinary body sentence, so the text that follows the URL is really
			// just running prose continuing that sentence, NOT a button label. This uses a
			// SHORT trailing phrase as the label when one looks plausible, falling back to a
			// sensible default label otherwise; any leftover running prose is re-emitted as
			// ordinary body text rather than being swallowed into the button.
			let label = (this.#norm.RenderText(it.text) || "").replace(/\*/g, "").trim();
			let trailing = "";
			if (tag === "external link button" && url) {
				const after = it.blackAfter.replace(/https?:\/\/[^\s\]]+/, "").replace(/\*/g, "").trim();
				if (!label) {
					const short = after && after.split(/\s+/).length <= (btn.label_max_words ?? 4) && !/[.!?]$/.test(after);
					if (short) { label = after; }
					else {
						label = /youtu|vimeo|\bvideo\b/i.test(url) ? (btn.video_label ?? "Go to video") : (btn.default_label ?? "Go to website");
						trailing = after;   // running prose after the URL → body, not the label
					}
				}
			}
			if (!label) label = (it.blackAfter || "").replace(/\*/g, "").replace(/https?:\/\/[^\s\]]+/, "").trim()
				|| tpl.buttons.journal_label_default;
			// DOWNLOAD-JOURNAL TEMPLATED SCAFFOLD (ROUND 239 — Dev-Feedback R2, B5;
			// SCCH302-02 activity 2B). The writer's "[button to download journal with
			// standard instructions]" ships the design team's templated download scaffold
			// (docs/{CODE} Journal.docx anchor + downloadButton + hint + hintDropContent)
			// plus ONE Designer/Developer To Do note that the journal document itself must
			// be created. The discriminator (download+journal+"standard instructions", or
			// the "button to download journal" head) has a measured corpus population of
			// ZERO — the 15 existing download-journal bracket forms keep their existing
			// routes (incl. the round-96 button_download rule) byte-identically. The
			// writer's own label text is consumed (it IS the button's label, replaced by
			// the templated "Download journal").
			// Data flag: buttons.download_journal   Env toggle: DLJOURNAL_OFF
			const djCfg = tpl.buttons.download_journal;
			if (djCfg && djCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.DLJOURNAL_OFF)
				&& new RegExp(djCfg.match, "i").test(Utils.Fold(String(it.text ?? "")))) {
				out.push(NotesAndComments.redFlag(
					Utils.FillTemplate(djCfg.note, { code: run.moduleCode ?? "" }), run, "todo"));
				out.push(Utils.FillTemplate(djCfg.scaffold, { code: run.moduleCode ?? "" }));
				return out;
			}
			// GO-TO-JOURNAL H4 (ROUND 239 — Dev-Feedback R2, B4; SCCH302-03 activity 3D).
			// A [button] whose EXPLICIT label folds to "go to (your) journal" — or the
			// alias-typed [go to journal]/[journal button] span — ships the design team's
			// templated <h4 class="goJournal">Go to your journal</h4> instead of a green
			// button. Fires only on an EXPLICIT writer label (a bare [Button] whose label
			// came from journal_label_default is untouched) and never when a URL is
			// present (gold's h4 carries no link). The gold library is era-MIXED
			// (h4 ×568 vs button ×1,052, mixed within most subjects) — the developer's
			// feedback names the h4 as the design team's CURRENT convention, so this is a
			// FORWARD-LOOKING overrides-gold rule (captured in
			// Subject_Global_Parameters._universal_conventions.r239_go_journal_h4).
			// Data flag: buttons.go_journal   Env toggle: GOJOURNAL_OFF
			const gjCfg = tpl.buttons.go_journal;
			if (gjCfg && gjCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.GOJOURNAL_OFF)
				&& key === "button" && !url) {
				const _lblRe = new RegExp(gjCfg.label_match, "i");
				const _explicitLbl = (this.#norm.RenderText(it.text) || "").replace(/\*/g, "").trim()
					|| (it.blackAfter || "").replace(/\*/g, "").replace(/https?:\/\/[^\s\]]+/, "").trim();
				const _aliasSpan = new RegExp(gjCfg.raw_match, "i")
					.test(Utils.Fold(String(it.text ?? "")).trim());
				if ((_explicitLbl && _lblRe.test(_explicitLbl)) || _aliasSpan) {
					out.push(Utils.FillTemplate(gjCfg.form,
						{ label: Utils.EscapeHtml(gjCfg.label ?? "Go to your journal") }));
					// never silently strip: an alias-typed span carrying REAL trailing prose
					// (not just its own "Go to journal"-ish label duplicate) keeps that prose
					// as ordinary body text after the heading
					const _tail = (it.blackAfter || "").replace(/\*/g, "").trim();
					if (_aliasSpan && _tail && !_lblRe.test(_tail)) {
						out.push(...ListsAndRuns.renderBlackText(_tail, run, it.block?.links));
					}
					return out;
				}
			}
			// BLL SUBJECT HOUSE STYLE: a plain "[button]" whose label is a dropbox
			// upload/visit renders ORANGE (buttonD) in the Blended-Literacy subject family,
			// GREEN elsewhere — a per-module-prefix convention (the SAME label is both
			// colours corpus-wide, so it is NOT a per-button CTA rule). Data:
			// buttons.dropbox_orange_house_style; env DROPBOXD_OFF. Colour only — the
			// per-module D2L dropbox link/rcode is not in the WT/Media List.
			let form = btn.form;
			const dox = tpl.buttons.dropbox_orange_house_style;
			let dropboxFired = false;
			if (key === "button" && dox?.enabled
				&& !(typeof process !== "undefined" && process.env && process.env.DROPBOXD_OFF)) {
				const prefix = run.moduleCode?.match(/^[A-Za-z]+/)?.[0] ?? "";
				if (new RegExp(dox.label_match, "i").test(label)
					&& (dox.module_prefixes ?? []).includes(prefix)) {
					form = tpl.buttons.button_dropbox.form;
					dropboxFired = true;
				}
			}
			// A plain "[Button]" tag whose URL actually sits on the IMMEDIATELY-FOLLOWING
			// standalone bare-URL paragraph (rather than inside the button tag itself) is the
			// human developer's LINKED button — this loads that URL onto the button as its
			// href, and drops the now-redundant bare-URL "<p>" that would otherwise render
			// separately underneath it (verified against modules ENGI302, ENGJ202, SSOG301,
			// and MXDI301). This is deliberately TIGHT: it only fires when the next body
			// item's WHOLE content is a single http(s) URL and nothing else (the same "a bare
			// URL and nothing else" discriminator used for the standalone external-link
			// button elsewhere), the item is not itself a structural tag, and it hasn't
			// already been consumed by something else; it also never fires on the
			// dropbox-orange button variant. The consumed URL paragraph is then skipped over
			// by the main loop's usual "_consumed" check.
			// Data flags: buttons.absorb_following_url, buttons.button_linked
			// Env toggle: BTNURL_OFF
			const auRule = tpl.buttons.absorb_following_url;
			const auOn = auRule && auRule.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.BTNURL_OFF);
			if (auOn && key === "button" && !dropboxFired && !url) {
				const nxt = bodyItems[i + 1];
				if (nxt && !nxt._consumed && nxt.consumedBy === undefined) {
					const nraw = String(nxt.blackAfter ?? "").replace(/\*/g, "").trim();
					const nlink = nxt.block?.links?.[0];
					const nDir = nxt.parse?.primary?.directive;
					const nIsStruct = nDir && ["CONTAINER_OPEN", "CONTAINER_CLOSE",
						"PAGE_BOUNDARY", "SECTION_MARKER", "INTERACTIVE"].includes(nDir);
					const nurl = /^https?:\/\/\S+$/.test(nraw) ? nraw
						: (nlink?.target && /^https?:\/\//.test(nlink.target)
							&& (nraw === "" || nraw === nlink.target) ? nlink.target : "");
					if (nurl && !nIsStruct) {
						url = nurl;
						form = tpl.buttons.button_linked.form;
						nxt._consumed = true;
					}
				}
			}
			// A "[button]" tag whose RAW in-bracket text contains the word "download" (for
			// example "[Download learning journal button]", found on module ENGS302-01) is
			// the human developer's DOWNLOAD button variant — an orange
			// "<div class="button downloadButton">" using the writer's own descriptive text
			// as the label ("Download learning journal"), rather than the plain default
			// "<div class="button">Go to your journal</div>" form. This is SCOPED to an
			// explicit "download" word appearing in the tag text itself (a bare "[Button]"
			// tag that a human developer separately chose to style as a download button, with
			// its own editorially-invented label and class, is left completely untouched —
			// this was measured and found to be genuinely non-derivable from the source, see
			// outputs/_measure_dropbox.py); the parent activity's own "dropbox" CSS class is
			// similarly left alone as non-derivable. This rule takes priority over the
			// default/dropbox/linked button forms above when it matches.
			// Data flag: buttons.button_download
			// Env toggle: DLBTN_OFF
			const dlCfg = tpl.buttons.button_download;
			if (dlCfg && dlCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.DLBTN_OFF)
				&& /\bdownload\b/i.test(String(it.text ?? ""))) {
				const dlLabel = String(it.text ?? "")
					.replace(/^[\s\[]+|[\s\]]+$/g, "")        // strip the surrounding brackets/space
					.replace(/\s*\bbuttons?\b\s*$/i, "")      // strip the trailing "button(s)" word
					.replace(/\*/g, "").replace(/\s+/g, " ").trim();
				if (dlLabel) { label = dlLabel; form = dlCfg.form; }
			}
			out.push(Utils.FillTemplate(form, {
				label: Utils.EscapeHtml(label), url: Utils.EscapeHtml(url),
			}));
			if (trailing) out.push(...ListsAndRuns.renderBlackText(trailing, run));
			return out;
		}

		// ---- embeds & inputs -------------------------------------------------
		if (tag === "embed") {
			// EMBED STORY → CAROUSEL SCAFFOLD. An [embed story] /
			// [Embed pdf text of story] / [Embed School Journal story] embeds a decodable/journal
			// story whose pages live on an external site (SPELD/School Journal). A bare <iframe> of
			// that site renders as a broken grey box; the human builds a CAROUSEL of the story's
			// page images (measured 63/64 [embed story] modules). Those pages are sourced manually
			// post-conversion (not in the WT/Media List), so emit the carousel SCAFFOLD with one
			// Mode-P/D placeholder slide. Keyed on 'story' in the tag remainder, EXCLUDING 'audio'
			// (the lone '[Embed audio recording of this story]' is an audio). Data
			// elements.embed_story_carousel; env EMBEDSTORY_OFF.
			const _esc = tpl.elements?.embed_story_carousel;
			const _escOn = _esc && _esc.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.EMBEDSTORY_OFF);
			// Fire on a data-driven trigger word ('story'|'book') in the [embed] tag's own bracket,
			// excluding 'audio'. 'story' also folds to the "story heading" SUBTAG (it.parse.tags), so
			// that is checked too; 'book' only appears in the raw bracket. Whole-word match so
			// 'audiobook'/'booklet' never trip it.
			const _firstBracket = (String(it.text || "").match(/\[[^\]]*\]/)?.[0] ?? "").toLowerCase();
			const _embTags = it.parse?.tags ?? [];
			const _trigRe = new RegExp(`\\b(?:${_esc?.trigger_words ?? "story|book"})\\b`);
			const _exclRe = new RegExp(`\\b(?:${_esc?.exclude_words ?? "audio"})\\b`);
			const _isStory = (_trigRe.test(_firstBracket) || _embTags.some((t) => t.tag === "story heading"))
				&& !_exclRe.test(_firstBracket) && !_embTags.some((t) => t.tag === "audio");
			if (_escOn && _isStory) {
				const label = _esc.placeholder_label ?? "story";
				const fname = _esc.placeholder_filename ?? "story.jpg";
				const img = run.imageMode === "P"
					? Utils.FillTemplate(tpl.image.mode_P.visible, { label })
						+ Utils.FillTemplate(tpl.image.mode_P.comment, { filename: fname })
					: Utils.FillTemplate(tpl.image.mode_D.visible, { filename: fname });
				out.push([_esc.open, Utils.FillTemplate(_esc.item, { image: img }), _esc.close].join("\n"));
				return out;
			}
			// A URL the writer typed INSIDE the tag's red span (e.g.
			// "[Embed film] edit to start at 3 seconds https://youtu…") is in it.text, not blackAfter /
			// a hyperlink / a following black item, so the old gatherFollowing search missed it →
			// 'RED FLAG: [embed] with no URL found'. Probe links → blackAfter → it.text (last resort).
			// Data elements.media_url_in_text; env MEDIAURLTEXT_OFF.
			const _urlInTextOn = (tpl.elements?.media_url_in_text?.enabled !== false)
				&& !(typeof process !== "undefined" && process.env && process.env.MEDIAURLTEXT_OFF);
			const _re = /https?:\/\/[^\s\]\)"<>]+/;
			const probe = it.block?.links?.[0]?.target
				?? (it.blackAfter || "").match(_re)?.[0]
				?? (_urlInTextOn ? String(it.text || "").match(_re)?.[0] : undefined)
				?? "";
			// a YouTube/Vimeo "[Embed film]"/"[Imbed film]" is the human's VIDEO embed (videoSection,
			// ENGS302-01 verified), NOT a bare iframe — route it through MediaBuilder.media so it builds the same
			// videoSection as "[Embed video]" (which already resolves to the video tag).
			if (probe && /youtu\.?be|youtube|vimeo/i.test(probe)) {
				return out.concat(MediaBuilder.media(it, bodyItems, i, "video", run));
			}
			const url = probe
				|| (MediaBuilder.gatherFollowing(it, bodyItems, i).match(/https?:\/\/[^\s\]]+/)?.[0] ?? "");
			if (!url) {
				out.push(NotesAndComments.redFlag("[embed] with no URL found — add the embed source.", run));
				return out;
			}
			out.push(Utils.FillTemplate(tpl.embeds.iframe, { url: Utils.EscapeHtml(url) }));
			return out;
		}
		if (tag === "text box") {
			const placeholder = (it.blackAfter || "").replace(/\*/g, "").trim();
			out.push(Utils.FillTemplate(tpl.embeds.text_box, { placeholder: Utils.EscapeHtml(placeholder) }));
			return out;
		}

		// ---- title bar resolved as ELEMENT mid-document (a heading) -----------
		if (tag === "title bar") {
			let text = (this.#norm.RenderText(it.text) || it.blackAfter).replace(/\*/g, "").trim();
			// a [Title] that merely repeats the module title is CONSUMED —
			// the header h1 already shows it (gold standard: BLL146-0.0)
			if (text && this.#pageEnglishTitle
				&& Utils.Fold(text).replace(/\s+/g, "") ===
					Utils.Fold(this.#pageEnglishTitle).replace(/\s+/g, "")) {
				return out;
			}
			if (!text) {
				// a bare [Introduction]/[Title] mid-document: the alias WORD
				// itself is the heading (human BLL146-0.0 renders
				// <h3>Introduction</h3> from exactly this form)
				const word = (it.parse.primary.fragment ?? "").trim();
				text = word ? word.charAt(0).toUpperCase() + word.slice(1) : "";
			}
			if (text) out.push(`<h3>${ListsAndRuns.inlineMarkup(text)}</h3>`);
			return out;
		}

		// ---- body / default ELEMENT: paragraphs of the following content ------
		const gathered = MediaBuilder.gatherFollowing(it, bodyItems, i);
		if (gathered.trim()) out.push(...ListsAndRuns.renderBlackText(gathered, run));
		return out;
	};

	/**
	 * CALLOUT emitter — the OSAI201 over-nesting fix.
	 *
	 * STRICT (default): the box holds ONLY its own content run — embedded
	 * payload + the black text following its marker (including directly
	 * following black items, which get marked _consumed) — and is emitted
	 * COMPLETE, never touching the stack. The next [body]/[video]/heading
	 * tag can therefore never end up inside it. This is the project's core
	 * marker model (§1.1) applied to containers, backed by the corpus:
	 * .whakatauki holds only its proverb <p>s in all 181 human instances.
	 *
	 * SPAN (writer-explicit): when a matching [end X] exists ahead, the box
	 * deliberately spans — it opens on the stack and runs until that close.
	 *
	 * Pipe-split: whakataukī arrive as "reo | english" on one line; the
	 * house form is two <p>s (179/181) — data flag split_payload_on_pipe.
	 */
	/**
	 * The human developer strips a writer's "**bold**" markup that lands INSIDE an
	 * alert-family callout box (any of the "alert", "alert solid", "alert top", or
	 * "alertActivity" classes) across a measured set of 16 subject families.
	 *
	 * HOW THIS WAS MEASURED: live measurement against the whole corpus (see
	 * outputs/_measure_alertbold.py) found the human strips bold in this context 1103 times
	 * out of 1153 (96% of the time) within the applicable scope — consistently so per
	 * subject (90–100%) and per box sub-class (94–100%, meaning there's no meaningfully
	 * different sub-convention by box type). The small remaining "kept bold" minority turned
	 * out to be span-level key-vocabulary editorial choices (for example the HIS subject's
	 * "mana"/"apartheid" definition terms) with no reliable discriminating rule available —
	 * so this is treated as a NET-POSITIVE rendering normalisation: applying the strip
	 * overall matches the human far more often than it doesn't, even though a few individual
	 * cases won't match. Some subject families are excluded because they were measured as
	 * genuinely inconsistent fragments (ANZH 86%, ART 79%, BLL 77% — not reliable enough to
	 * include), and bilingual/reo modules are excluded entirely since they keep bold far less
	 * consistently there (TRR strips only 40% of the time) — handled via the shared
	 * MenuBuilder.isReoModule check (deliberately never the broader mtkFlag signal).
	 *
	 * REGION SCOPING: this only strips bold within the box's OWN lead/payload/content
	 * renders — it checks the callout definition's own emitted opening HTML against a class
	 * pattern, so whakataukī boxes, quote boxes, wānanga boxes, and supervisor-note panels
	 * never match this pattern and are correctly left untouched (those were measured
	 * separately, as their own distinct buckets). Nested tables and widgets inside the box
	 * are rendered via entirely different code paths and are therefore untouched by
	 * construction, not by any special-casing here.
	 *
	 * @returns {Function} a mapper function to apply to a segment array (identity/no-op when
	 *   this feature is inactive)
	 * Data flag: callouts.strip_bold
	 * Env toggle: ALERTBOLD_OFF (reverts to keeping the writer's original bold markup)
	 */
	static #alertBoldStripper(def, run) {
		const cfg = DataService.Data.EmitTemplates.callouts?.strip_bold;
		const off = typeof process !== "undefined" && process.env && process.env.ALERTBOLD_OFF;
		const on = cfg && cfg.enabled !== false && !off && def?.open
			&& new RegExp(cfg.class_pattern || "class=\"(alert|important)").test(def.open)
			&& (cfg.subjects ?? []).some((s) => (run.moduleCode ?? "").startsWith(s))
			&& !(cfg.exclude_reo !== false && MenuBuilder.isReoModule(run));
		return on ? (seg) => seg.map((h) => MenuBuilder.stripTextBold(h)) : (seg) => seg;
	}

	/**
	 * The human developer strips a writer's "**bold**" markup that lands in an ACTIVITY
	 * box's own body text, in the subject families that make up the "strong" side of the
	 * Fundamentals template group.
	 *
	 * HOW THIS WAS MEASURED: live measurement against the corpus (see
	 * outputs/_measure_actbold.py, which separates out alert-box content so it isn't
	 * double-counted with #alertBoldStripper above) found the human strips bold here 846
	 * times out of 892 (95% of the time) within the applicable subjects — ARFUN 95%, ENFUN
	 * 91%, HPFUN 100%, MXFUN 97%, XFUN 100%. Other subject families are excluded because
	 * they were measured as genuinely inconsistent: TEFUN is a real 49/51 mixed case, SSFUN
	 * sits at 75%, SCFUN has too few samples (7) to be reliable, and non-Fundamentals
	 * template types generally sit at 75–87% (this whole rule is scoped to Fundamentals
	 * only). Bilingual/reo modules are excluded via the shared MenuBuilder.isReoModule check
	 * (again, deliberately never the broader mtkFlag signal). The small remaining "kept
	 * bold" minority (46 instances, heavily clustered in module ARFUN04's "Instructions:"
	 * and "Goal:" lead-in lines plus other key vocabulary) has no reliable discriminating
	 * rule available — a rule based on whether the bold text follows a colon was tried and
	 * found NOT to separate the cases well (within ARFUN04 itself, the keep-rate is 14% for
	 * colon-led text vs 2% for plain text — not a clean enough split) — so, as with the
	 * alert-box version above, this is treated as a NET-POSITIVE rendering normalisation
	 * (65 genuinely fixable cases against 18 acceptable side-effect losses, net +47 correct
	 * matches).
	 *
	 * REGION SCOPING: rather than checking a callout definition's class (as the alert
	 * version does), this checks the LIVE container stack at render time — the returned
	 * mapper function only strips bold while the TOP of the stack is an open ACTIVITY
	 * (mode === "activity"). If a callout box sits on top of the stack instead (the alert
	 * case handled by #alertBoldStripper, which keeps bold in these particular subjects), or
	 * if the stack is empty, this is a no-op. Strict callouts, kept tables, widgets,
	 * headings, and media all render via entirely different code paths, so they are
	 * untouched BY CONSTRUCTION rather than by any special-casing here. This is applied at
	 * ConvertPage's main black-text emit sites in the processing loop.
	 *
	 * @returns {Function} a mapper function to apply to a segment array (identity/no-op when
	 *   this feature is inactive)
	 * Data flag: activity_wrapper.strip_bold
	 * Env toggle: ACTBOLD_OFF (reverts to keeping the writer's original bold markup)
	 */
	static #activityBoldStripper(stack, run) {
		const cfg = DataService.Data.EmitTemplates.activity_wrapper?.strip_bold;
		const off = typeof process !== "undefined" && process.env && process.env.ACTBOLD_OFF;
		const on = cfg && cfg.enabled !== false && !off
			&& (cfg.subjects ?? []).some((s) => (run.moduleCode ?? "").startsWith(s))
			&& !(cfg.exclude_reo !== false && MenuBuilder.isReoModule(run));
		if (!on) return (seg) => seg;
		return (seg) => {
			const top = stack[stack.length - 1];
			return top && top.mode === "activity"
				? seg.map((h) => MenuBuilder.stripTextBold(h)) : seg;
		};
	}

	/**
	 * The human developer ships BODY headings as PLAIN text 99.5% of the time (found via a
	 * screenshot review of module OSAH301-1.0, where the italics "should be stripped" but
	 * weren't) — without this, the converter would keep a whole-heading "*italic*" style the
	 * writer typed, for example a section heading like "[H3] *What is online harassment or
	 * abuse?*" rendering as "<h3><i>…</i></h3>" instead of plain "<h3>…</h3>".
	 *
	 * HOW THIS WAS MEASURED: live measurement (see outputs/_measure_heading_italic.py) found
	 * the human strips heading italics 99.5% of the time overall, across every template and
	 * roughly 50 different subjects (including OSAH). The one meaningful exception is the
	 * ENGLISH-READING subject families (ENGS 95%, ENGC 94%, ENGR 96%, ENGJ 98%, ENGI 99%),
	 * where the italic text that gets kept is actually a NAMED WORK — a book or story title
	 * — with no reliable way to tell it apart from an ordinary section heading, so those
	 * subjects are excluded from this strip entirely (the same "no discriminating rule
	 * available, so exclude the whole family" pattern used by the bold-stripping methods
	 * above). Bilingual/reo modules are also excluded, via the shared
	 * MenuBuilder.isReoModule check.
	 *
	 * WHY THIS IS SAFE FOR THE GATES: the structural-skeleton comparison gate KEEPS "<i>"
	 * nodes in its comparison (it only drops script/style-type elements), so stripping the
	 * italic here where the human's version also has it stripped actually REMOVES a
	 * spurious "<i>" node that was causing a mismatch — a net-POSITIVE change for that gate.
	 * The other structural-comparison gates are unaffected either way, because an "<i>" tag
	 * is not a structural container and the heading's inner text content is unchanged by
	 * removing it.
	 *
	 * Strips via the shared MenuBuilder.stripTextItalic helper (which guards against
	 * touching Font-Awesome icon markup).
	 * Data flag: elements.heading.strip_italic
	 * Env toggle: HEADITALIC_OFF (reverts to keeping the writer's original italic markup)
	 */
	static #stripHeadingItalic(html, run) {
		const cfg = DataService.Data.EmitTemplates.elements?.heading?.strip_italic;
		const off = typeof process !== "undefined" && process.env && process.env.HEADITALIC_OFF;
		const on = cfg && cfg.enabled !== false && !off
			&& !(cfg.exclude_subjects ?? []).some((s) => (run.moduleCode ?? "").startsWith(s))
			&& !(cfg.exclude_reo !== false && MenuBuilder.isReoModule(run));
		return on ? MenuBuilder.stripTextItalic(html) : html;
	}

	/**
	 * Builds the SIDE column for a "side_column" callout (a "[Side alert]" tag, which
	 * renders as an "alertActivity" box). Returns just the
	 * `<div class="{side_column}"> … </div>` column on its own (with no outer row wrapper),
	 * so that the calling emit site is free to either wrap it in its own standalone row, OR
	 * splice it in as the right-hand sibling of the immediately preceding "col-md-8" content
	 * column within one shared row (this second, side-by-side form is the human developer's
	 * actual convention, measured to match 99 times out of 100 in the corpus — it looks much
	 * better visually than always stacking the alert underneath its content).
	 * MediaBuilder.gatherFollowing marks the strict text run it consumes — this method must
	 * be called EXACTLY ONCE per side-alert (the calling emit site is responsible for
	 * guaranteeing that).
	 */
	static #sideAlertCol(it, bodyItems, i, run, def) {
		const inner = [];
		const following = MediaBuilder.gatherFollowing(it, bodyItems, i);
		const _txt = following.trim() ? following : (it.blackAfter || "").trim();
		const deBold = this.#alertBoldStripper(def, run);   // the alertActivity box class is one of the measured alert-family buckets, so bold gets stripped here too
		if (_txt) inner.push(...deBold(ListsAndRuns.renderBlackText(_txt, run, it.block?.links)));
		const box = `${def.open}\n${inner.join("\n")}\n${def.close}`;
		return `<div class="${def.side_column}">\n${box}\n</div>`;
	}

	static #calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured = false) {
		const tpl = DataService.Data.EmitTemplates;
		const tag = it.parse.primary.tag;
		// With the SIDEALERT_OFF env toggle set, a "[side alert]" tag reverts to being treated
		// as a plain "[alert]" box (an older, simple substring-match behaviour, found on
		// module BLL210); otherwise it keeps its own dedicated callout definition.
		const _sideAlertOff = typeof process !== "undefined" && process.env && process.env.SIDEALERT_OFF;
		let def = (tag === "side alert" && _sideAlertOff) ? tpl.callouts.by_tag.alert : tpl.callouts.by_tag[tag];
		// INNER PANEL ROW (found on module BLL225-0.0): the human developer wraps the
		// supervisor-note panel's two "col-12" columns in an ADDITIONAL inner row
		// ("super-content row" > inner "row" > columns) — measured at 215 out of 215 human
		// non-activity supervisor-note sites, versus the converter's 0 out of 214 before this
		// fix; the original template definition had simply under-copied its own reference
		// example (the same class of gap as the activity-panel's own inner row elsewhere in
		// this file, which the frontend's reveal JavaScript specifically looks for). A
		// callout definition carrying an inner_row configuration swaps to that
		// open/close pair instead of the flat, non-wrapped legacy form.
		// Data flag: callouts.by_tag.<tag>.inner_row
		// Env toggle: SUPINROW_OFF (reverts to the flat, non-inner-row legacy panel)
		const _irCfg = def?.inner_row;
		if (_irCfg && _irCfg.enabled !== false && _irCfg.open
			&& !(typeof process !== "undefined" && process.env && process.env.SUPINROW_OFF)) {
			def = Object.assign({}, def, { open: _irCfg.open, close: _irCfg.close });
		}
		if (!def) {
			return [NotesAndComments.redFlag(
				`Unknown container [${tag}] — content kept below without a wrapper; add it to Emit_Templates callouts.`, run)];
		}
		// A "[side alert]" tag renders as an alertActivity box sitting in a SIDE column
		// (found on module BLL210): it has no "alert" CSS class, no inner "row>col-12" wrap,
		// and no h4-styled lead line — its content is just direct "<p>" elements inside the
		// alertActivity box, itself wrapped in "row>{side_column}". The strict following text
		// run is gathered and marked consumed, so the main processing loop skips over it.
		// The exact column width and whether it sits side-by-side with other content are
		// editorial details, handled separately (see the "SIDE-BY-SIDE backward pairing"
		// note below).
		// Data flag: callouts.by_tag.'side alert'
		// Env toggle: SIDEALERT_OFF
		if (def.side_column) {
			// This is the OWN-ROW form. The SIDE-BY-SIDE backward pairing (placing this
			// column as the right-hand sibling of the preceding content column instead) is
			// handled separately at the emit site, which calls #sideAlertCol directly to get
			// just the column HTML for that purpose.
			return [`<div class="row">\n${this.#sideAlertCol(it, bodyItems, i, run, def)}\n</div>`];
		}

		const { modifiers, flags } = ActivitiesBuilder.containerModifiers(it, tpl.callouts.modifier_classes, run);
		const out = [...flags];
		out.push(Utils.FillTemplate(def.open, { modifiers }));

		// embedded payload (e.g. "[Alert Box] A Living Taonga") — original
		// case via RenderText (§1.2: matching folds, render content never)
		const embedded = this.#norm.RenderText(it.text);
		const lead = embedded && embedded.split(" ").length <= 12 && !it.parse.instructionFragment
			? embedded : "";

		// the lead's element: alerts/importants use an h4 (corpus-dominant),
		// refined by the module's GROUP convention where measured
		// (Html_Convention_Registry callout_lead); others keep a bold <p>
		const leadEl = def.lead_element
			? (run.conventions?.calloutLead || def.lead_element) : null;
		const leadHtml = (text) => leadEl
			? `<${leadEl}>${ListsAndRuns.inlineMarkup(text)}</${leadEl}>`
			: `<p><b>${ListsAndRuns.inlineMarkup(text)}</b></p>`;

		// Alert-region bold strip (see #alertBoldStripper above for the full explanation; it
		// is a no-op mapper when the feature is inactive). This applies to the box's OWN
		// rendered content in BOTH of the modes below (the span mode's lead/first-paragraph,
		// and the strict mode's lead/payload/content). A span-mode box's LATER items handled
		// separately by the main processing loop are a small, separately-logged residue that
		// this doesn't reach (measured to be small — worth re-measuring before spending
		// effort chasing it further).
		// Env toggle: ALERTBOLD_OFF
		const deBold = this.#alertBoldStripper(def, run);

		if (spans) {
			// SPAN mode: open stays on the stack; later items nest inside until the
			// terminator (writer's [end X] for an explicit span; the next
			// heading/section/page for a STRUCTURED-CONTENT wrap).
			if (lead) out.push(...deBold([leadHtml(lead)]));
			if (it.blackAfter.trim()) out.push(...deBold(ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links)));
			// alert/important wrap their content in row>col-12; for a SPAN the content
			// arrives later (the main loop), so open the wrap NOW and close it with the box.
			const wrap = def.wrap_content ? tpl.callouts.content_wrap : null;
			if (wrap) out.push(wrap.open);
			const closeHtml = (wrap ? wrap.close + "\n" : "") + def.close;
			// ROUND 239 (Dev-Feedback R2, B1 part 2): remember the wrap open/close strings on
			// the stack entry, so the CONTAINER_CLOSE site can detect a box whose inner
			// row>col-12 stayed EMPTY (the writer put all the content in the span's own lead
			// paragraph and closed the box immediately — SCCH302-01's [right-hand alert]/
			// [end alert] shape) and drop the useless empty wrapper pair. Measured: the
			// converted corpus ships 70 such empty row>col-12 pairs / 28 modules; the human
			// gold ships 2 (both one-off outliers) — the human never keeps the empty wrap.
			// Data flag: callouts.drop_empty_span_wrap   Env toggle: EMPTYWRAP_OFF
			stack.push({ tag, close: closeHtml,
				mode: wrapStructured ? "span-wrap" : "span", hasContent: out.length > 1,
				wrapOpen: wrap ? wrap.open : null, wrapClose: wrap ? wrap.close : null });
			run.AddNote("info", "ContentConverter", wrapStructured
				? `[${tag}] wraps the following table/widget as its content (no [end ${tag}]) — closes at the next heading/section/page.`
				: `[${tag}] spans to an explicit end tag (writer-authored box).`);
			return out;
		}

		// STRICT mode: gather the box's own content run and close it NOW.
		// PROVERB callouts (whakataukī) hold ONLY the proverb — the leading SHORT
		// line(s) — never the commentary that follows. The human keeps the proverb
		// in .whakatauki (median 2 <p>s = reo + english) and the explanation as FREE
		// body (measured 137/147). #gatherProverb stops at the first long/commentary
		// paragraph and leaves it un-consumed so it renders as body. Other callouts
		// keep the full following-run gather.
		let content = def.proverb_only
			? this.#gatherProverb(it, bodyItems, i, def)
			: MediaBuilder.gatherFollowing(it, bodyItems, i);
		if (def.split_payload_on_pipe) {
			// split "reo SEP english" into separate lines → separate <p>s, where SEP is
			// any of | – — (pipe / en-dash / em-dash, ALWAYS spaced so hyphenated words
			// and number ranges are never split). Writers vary the separator (corpus:
			// pipe 23, spaced-dash among the rest); the human splits them either way.
			// Never split a line carrying a URL.
			content = content.split("\n").map((line) =>
				line.includes("http") ? line : line.replace(/\s+[|–—]\s+/, "\n")).join("\n");
		}
		// PROVERB NORMALISE — SPLIT step (round 225; Chris's XDLS905/906 whakataukī
		// screenshots). A writer authors the proverb as a bold reo line, a SOFT line
		// break (w:br), then the English translation — the docx extractor drops soft
		// breaks, so the two lines arrive GLUED into one ("…ana”Through perseverance…")
		// and ship as ONE <p>. The human house form is TWO separate plain <p>s
		// (measured 213/215 gold .whakatauki boxes; tool outputs/_measure_whakatauki.py).
		// The lost break is still visible in the raw text as a BOUNDARY — a leading
		// **bold**/*italic* group directly abutting more text, a closing quote followed
		// by prose, a space-before pipe with no space after, or a trailing
		// "(translation)" — so the split re-derives the writer's own line structure.
		// Splits run on the RAW text (the markers ARE the signal); the bold/italic/
		// quote STRIPS happen at the rendered-segment level below (deProv).
		// Data flag: callouts.by_tag.<tag>.proverb_normalise
		// Env toggle: PROVERBNORM_OFF (reverts split AND strips)
		if (def.proverb_normalise) content = this.#proverbSplit(content, def.proverb_normalise);
		// the human wraps an alert/important's content in a row>col-12 (data:
		// callouts.by_tag.<tag>.wrap_content + callouts.content_wrap). whakataukī /
		// quote keep their direct <p>s (no wrap_content key).
		const wrap = def.wrap_content ? tpl.callouts.content_wrap : null;
		if (wrap) out.push(wrap.open);
		// The human developer strips a writer's *italic* markup that lands INSIDE the
		// supervisor-note super-content panel, in the MXDI and XDLS subject families
		// specifically (measured: all 29 out of 29 source-document spans there get stripped —
		// the human panels carry ZERO "<i>"/"<em>" elements; the converter used to keep 13 of
		// them on module MXDI103). The BLL subject family is a genuine MIXED case (book/story
		// titles there are deliberately KEPT italic), and the bilingual/reo families keep
		// their reo italic too — so this is scoped to an explicit subject list rather than
		// applied everywhere (the same "list only where it was actually measured to be
		// consistent" pattern used elsewhere in this file). Font-Awesome icon markup is left
		// untouched by the shared MenuBuilder.stripTextItalic helper.
		// Data flag: callouts.by_tag.<tag>.strip_italic_subjects
		// Env toggle: PANELITALIC_OFF
		const stripItal = (def.strip_italic_subjects ?? []).some(
			(s) => (run.moduleCode ?? "").startsWith(s))
			&& !(typeof process !== "undefined" && process.env && process.env.PANELITALIC_OFF);
		const deItal = (seg) => stripItal ? seg.map((h) => MenuBuilder.stripTextItalic(h)) : seg;
		// PROVERB NORMALISE — STRIP step: the human ships proverb <p>s PLAIN — bold
		// stripped (gold keeps <b> in only 2/215 boxes), italic stripped (5/215),
		// wrapping curly/straight quotes stripped (9/215) — the site CSS supplies the
		// bold/italic styling. Segment-level so the shared strip helpers handle even a
		// mangled ***triple-marker*** run (XLP03). The tiny gold keep-minority has no
		// discriminator → NET-POSITIVE class (the r164 precedent).
		// Data flag: callouts.by_tag.<tag>.proverb_normalise  Env: PROVERBNORM_OFF
		const pnCfg = def.proverb_normalise;
		const pnOn = pnCfg && pnCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.PROVERBNORM_OFF);
		const deProv = (seg) => pnOn ? seg.map((h) => ContentConverter.#proverbStripSeg(h, pnCfg)) : seg;
		if (lead) out.push(...deProv(deBold(deItal([leadHtml(lead)]))));
		// LONG IN-SPAN PAYLOAD AS CONTENT (found on module BLL111): when a writer types the
		// WHOLE note text INSIDE the red span itself (for example "[Supervisor note] The
		// decodable book(s) … [/RED TEXT]"), it's too long to pass the "12 words or fewer"
		// lead-line rule, and the strict content-gathering logic only ever collects ordinary
		// BLACK text — so without this fix, the panel would render with no content at all,
		// plus a spurious "Empty [tag]" red-flag warning, even though the human developer
		// ships that writer's prose directly as the panel's own "<p>" content (measured: 10
		// sites across 8 modules, ALL BLL-family supervisor notes, all genuine note prose;
		// module BLL111-01's human version also weaves in the payload's own bare URL as a
		// link, which is why this renders through the full renderBlackText helper rather than
		// as a bare, unprocessed "<p>"). A payload that's actually an instruction fragment
		// keeps using the separate CS-note handling path, untouched by this.
		// Data flag: callouts.by_tag.<tag>.long_payload_as_content
		// Env toggle: SUPPAYLOAD_OFF (reverts to the dropped-payload-plus-red-flag behaviour)
		const longPayload = def.long_payload_as_content && !lead && embedded
			&& !it.parse.instructionFragment
			&& !(typeof process !== "undefined" && process.env && process.env.SUPPAYLOAD_OFF)
			? embedded : "";
		if (longPayload) out.push(...deBold(deItal(ListsAndRuns.renderBlackText(longPayload, run, it.block?.links))));
		if (content.trim()) out.push(...deProv(deBold(deItal(ListsAndRuns.renderBlackText(content, run, it.block?.links)))));

		// SAME-BLOCK BUTTON/LINK ABSORB (found on module OSAH501-01). An "[external link
		// button]"/"[Button]" ELEMENT tag, or an "[external link]" INLINE tag, that sits in
		// the SAME source-document paragraph (the same underlying "block") as the callout
		// tag is genuinely part of the box's own CONTINUOUS sentence, not a separate section
		// starting after it — the human developer renders it INSIDE the alert/important box's
		// "row>col-12" wrapper (measured across the corpus: modules OSAH501, OSAH301,
		// OSGM101, OSAH401, ANZH404, XGF9006, and MXEO401 all nest it this way; 13 sites
		// across roughly 9 modules total). A button that appears a whole PARAGRAPH later
		// (i.e. belongs to a different "block") is deliberately left UNTOUCHED and stays in
		// its own separate row (this is the shape used by the CED subject family's
		// "[alert.top]" boxes — 36 different-block cases measured). The same-block
		// continuation check walks a contiguous run of TAG items right after the callout tag
		// (the document-parsing step always attaches a paragraph's black text to whichever
		// tag precedes it, so any same-block follower will always itself be a tag) — this
		// means it can never collide with MediaBuilder.gatherFollowing, which only ever walks
		// BLACK items and stops as soon as it hits a tag. The require_url check only absorbs
		// an item that has a genuinely resolvable http(s) URL target, so a writer instruction
		// that merely mentions the word "button" without an actual link (for example
		// "[please add a button to link to SSFUN07…]", found on module SSFUN01) is correctly
		// NOT absorbed. The walk STOPS as soon as it hits a different block, a non-button/
		// non-link item, or an item with no URL — so it can never accidentally over-capture
		// content that doesn't belong to the box.
		// Data flag: callouts.inline_continuation
		// Env toggle: CALLOUTBTN_OFF
		let absorbedInline = false;
		const icCfg = tpl.callouts.inline_continuation;
		const icOn = wrap && icCfg && icCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.CALLOUTBTN_OFF);
		if (icOn) {
			for (let j = i + 1; j < bodyItems.length; j++) {
				const nx = bodyItems[j];
				if (!nx || nx.type !== "tag" || nx.block !== it.block
					|| nx._consumed || nx.consumedBy !== undefined) break;
				const np = nx.parse?.primary;
				const isBtn = (icCfg.absorb_button_element !== false)
					&& np?.directive === "ELEMENT" && (np.tag || "").includes("button");
				const isExt = (icCfg.absorb_external_link_inline !== false)
					&& np?.tag === "external link";
				if (!isBtn && !isExt) break;
				if (icCfg.require_url !== false) {
					const url = ((nx.block?.links || []).map((l) => l?.target)
							.find((t) => /^https?:\/\//i.test(t || "")))
						|| (String(nx.blackAfter || "").match(/https?:\/\/[^\s\]]+/)?.[0])
						|| (String(nx.text || "").match(/https?:\/\/[^\s\]]+/)?.[0]) || "";
					if (!url) break;
				}
				out.push(...(np.directive === "INLINE"
					? this.#inline(nx, run)
					: this.#element(nx, bodyItems, j, stack, run)).filter(Boolean));
				nx._consumed = true;
				absorbedInline = true;
			}
		}

		if (!lead && !longPayload && !content.trim() && !absorbedInline) {
			out.push(NotesAndComments.redFlag(`Empty [${tag}] — the writer left a callout with no content.`, run));
		}
		if (wrap) out.push(wrap.close);
		out.push(def.close);
		return out;
	};

	/**
	 * Should this callout SPAN to WRAP a following TABLE as its content?
	 *
	 * THE BREAKDOWN it fixes (OSGM501): the writer put `[Alert]` then a 2-column
	 * table (image | speech-bubble text) — the alert's CONTENT is the table. The
	 * strict text-gather only collects black TEXT, so the alert rendered EMPTY and
	 * the table was lifted out as a separate widget. The human renders the table
	 * INSIDE the alert. Measured: 18 modules have a callout immediately followed by
	 * a table.
	 *
	 * THE ROBUST RULE (generalises, not one-off): a CONTENT callout (one with
	 * wrap_content — alert/important) that has NO black text of its own and is
	 * immediately followed by a TABLE wraps that table (and any widget the scanner
	 * built from it) as its content, in "span-wrap" mode bounded at the next
	 * heading/section/page so it can never over-capture. Proverb callouts
	 * (whakataukī) and text callouts are unaffected.
	 *
	 * @returns {boolean}
	 */
	static #calloutWrapsStructured(it, bodyItems, i) {
		const def = DataService.Data.EmitTemplates.callouts.by_tag[it.parse.primary?.tag];
		if (!def || !def.wrap_content) return false;        // only content callouts wrap
		if ((it.blackAfter ?? "").trim()) return false;     // it has its own text → strict
		const next = bodyItems[i + 1];
		return !!next && next.type === "table";             // its content is a following table
	};

	/**
	 * Closes an open "span-wrap" callout the instant its ONE table/widget has been
	 * rendered. A span-wrap (callout wrapping a following table) holds EXACTLY that
	 * content — closing it here (rather than letting autoClose wait for the next
	 * heading) is what keeps it from over-capturing the free body that follows.
	 * emit/breakRow are passed in because they are ConvertPage-local closures.
	 */
	/**
	 * Checks whether this rendered HTML still shows a resolved "[tag]" as plain visible
	 * text — that is, a residual bracket whose text, if re-parsed through the normaliser,
	 * would resolve to a real primary tag (a structural, widget, container, or marker tag —
	 * as opposed to ordinary prose, an instruction cue, or noise text, all of which resolve
	 * to a null primary tag and are therefore NOT considered a leak). This is used to keep
	 * the bilingual (reoMode) layout-table grid rendering safe: if converting a table to a
	 * grid layout would end up leaking a resolved tag from inside one of its cells as plain
	 * text, the code falls back to the safer, un-built placeholder form instead (which is
	 * deliberately excluded from the leak-detection gate, since its raw text is an
	 * intentional developer hand-off, not a bug). This mirrors the same leak-scanning logic
	 * used by the separate structural-defect audit tool.
	 */
	static #htmlLeaksResolvedTag(html) {
		const vis = String(html ?? "").replace(/<[^>]+>/g, " ");
		for (const m of vis.matchAll(/\[([^\]\n]{1,60})\]/g)) {
			let prim = null;
			try { prim = this.#norm.Parse(`[${m[1]}]`)?.primary?.tag ?? null; } catch { prim = null; }
			if (prim) return true;
		}
		return false;
	};

	static #closeSpanWrap(stack, emit, breakRow) {
		if (stack.length && stack[stack.length - 1].mode === "span-wrap") {
			emit(stack.pop().close);
			if (!stack.length) breakRow();
		}
	};

	/**
	 * Does a matching explicit close lie ahead for this callout?
	 * Scans forward until a section marker / page boundary / another
	 * callout opening (whichever comes first) — within that window, a
	 * CONTAINER_CLOSE of the same family (or the generic [end]) means the
	 * writer authored a spanning box.
	 */
	static #explicitCloseAhead(bodyItems, i, canonTag) {
		// ONLY the specific family close counts as span evidence — the
		// generic [end]/[End Phase N] forms resolve to "end other" and are
		// far too weak (TEFUN07's [End Phase 1] section markers wrongly
		// spanned an [Alert RHS] across a whole phase before this guard).
		const family = new Set([`end ${canonTag}`]);
		// alert/important share close phrasing in the wild
		if (canonTag === "important") family.add("end alert");
		if (canonTag === "alert") family.add("end important");

		for (let j = i + 1; j < bodyItems.length; j++) {
			const it2 = bodyItems[j];
			if (it2.type !== "tag") continue;
			const p = it2.parse.primary;
			if (!p) continue;
			if (p.directive === "PAGE_BOUNDARY" || p.directive === "SECTION_MARKER") return false;
			if (p.directive === "CONTAINER_OPEN" && p.tag !== "activity") return false;
			if (it2.parse.tags.some((t) => t.directive === "CONTAINER_CLOSE" && family.has(t.tag))) return true;
		}
		return false;
	};

	/**
	 * INLINE emitter — external links woven into the text flow.
	 * (Inline INTERACTIVE triggers are bundled by the scanner; only the
	 * non-interactive inline family lands here.)
	 */
	static #inline(it, run) {
		const tpl = DataService.Data.EmitTemplates;
		const out = [];
		const text = (it.blackAfter ?? "").trim();
		const link0 = it.block?.links?.[0];
		// When the "[external link]" tag MODIFIES a descriptive-phrase hyperlink (meaning the
		// link's visible text is a readable phrase, not just the bare URL) and carries no
		// trailing black text of its own, that phrase is rendered as the actual link by the
		// separate black-text item instead (via ListsAndRuns.inlineMarkup's hyperlink
		// weaving) — the tag itself is really just an "this link opens externally" modifier
		// in that case, so this emits NOTHING here, avoiding a duplicate, redundant bare-URL
		// "<p>". The STANDALONE form (a bare URL with no descriptive phrase attached to it at
		// all) still emits its own link below, as normal.
		// Env toggle: LINKWEAVE_OFF (reverts to leaving the phrase plain and emitting this bare URL too)
		const hw = DataService.Data.EmitTemplates.elements.hyperlink_weave;
		const weaveOn = hw && hw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.LINKWEAVE_OFF);
		if (weaveOn && !text && link0 && link0.target
			&& String(link0.text ?? "").trim()
			&& !/^https?:\/\//i.test(String(link0.text).trim())
			&& String(link0.text).trim() !== String(link0.target).trim()) {
			return out;
		}
		const url = link0?.target ?? (text.match(/https?:\/\/[^\s\]]+/)?.[0] ?? "");
		if (url) {
			// A STANDALONE "[external link]" tag whose item is ONLY a bare URL, with no
			// descriptive label text at all (found on module OSBY201-03), is the human
			// developer's externalButton form — the same visual treatment used by the
			// dedicated "[external link button]" tag elsewhere. A labelled form (one that
			// does have descriptive text) keeps the ordinary inline link treatment instead.
			// Data flag: elements.external_link_button_standalone
			// Env toggle: EXTBTN_OFF
			const labelText = text.replace(/https?:\/\/[^\s\]]+/g, "").replace(/\*/g, "").trim();
			const sbRule = tpl.elements.external_link_button_standalone;
			const sbOn = sbRule && sbRule.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.EXTBTN_OFF);
			const isExtLink = it.parse?.primary?.tag === "external link"
				|| (it.parse?.tags ?? []).some((t) => t.tag === "external link");
			// A LEADING "[external link]" tag (meaning it's the paragraph's PRIMARY tag —
			// the tag governs the whole paragraph, in the shape "[external link] __Phrase__
			// [LINK:url]", found on module ENGI302-02) that renders a short, descriptive
			// resource title is the human developer's externalButton form, rather than the
			// ordinary inline "<p><a>" hyperlink weave used elsewhere. The discriminator here
			// is the tag's POSITION within the paragraph (measured, see
			// outputs/_measure_extlink_position.py): a LEADING tag position means "render as
			// a button" (seen on modules ENGI302, ENGI303, ENGJ201), while a TRAILING tag
			// position means "render inline" (seen on modules OSBY201 and OSAH401 — measured
			// zero button-form cases anywhere in the corpus for trailing position). A
			// trailing-position form is already caught by the earlier "!text" early-return
			// above, so only a leading-position tag ever reaches this code; the short-label
			// guard below then keeps a leading external-link tag that happens to govern a
			// long, ordinary prose sentence from being turned into one giant, awkward button.
			const isLeadingExtLink = it.parse?.primary?.tag === "external link";
			const lbRule = tpl.elements.external_link_button_labelled;
			const lbOn = lbRule && lbRule.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.EXTBTNLABEL_OFF);
			const lbWords = labelText ? labelText.split(/\s+/).length : 0;
			const lbShort = labelText && lbWords <= (lbRule?.label_max_words ?? 10) && !/[.!?:]$/.test(labelText);
			if (sbOn && isExtLink && !labelText) {
				const eb = tpl.buttons["external link button"];
				const label = /youtu\.?be|youtube|vimeo|\bvideo\b/i.test(url)
					? (eb.video_label ?? "Go to video") : (eb.default_label ?? "Go to website");
				out.push(Utils.FillTemplate(eb.form, {
					url: Utils.EscapeHtml(url), label: Utils.EscapeHtml(label),
				}));
			} else if (lbOn && isLeadingExtLink && url && lbShort) {
				out.push(Utils.FillTemplate(lbRule.form, {
					url: Utils.EscapeHtml(url), text: Utils.EscapeHtml(labelText),
				}));
			} else {
				const label = labelText || url;
				out.push(`<p>${Utils.FillTemplate(tpl.elements.external_link_inline.form, {
					url: Utils.EscapeHtml(url), text: Utils.EscapeHtml(label),
				})}</p>`);
			}
		} else if (text) {
			out.push(...ListsAndRuns.renderBlackText(text, run, it.block?.links));
		}
		return out;
	};

	/**
	 * The interactive placeholder — visually and structurally distinct from
	 * every MTK style, pairing the page position to its manifest entry by
	 * index. Captured members render readably inside (un-built); writer
	 * instructions inside the bundle flag in red. NEVER an answer-bearing
	 * comment.
	 */
	static #interactivePlaceholder(bundle, run) {
		// FIRST: can we build this interactive for REAL? The InteractiveBuilder
		// handles the small set of "easy" widgets we fully understand. It returns
		// finished HTML, or null when the captured data is ambiguous — in which
		// case we fall straight through to the honest orange placeholder below.
		// (Markup lives in data/Emit_Templates.json → interactive_builders.)
		const built = InteractiveBuilder.Build({
			bundle,
			run,
			templates: DataService.Data.EmitTemplates.interactive_builders,
			renderInline: (line) => ListsAndRuns.inlineMarkup(line, [], false),   // built-widget internals are deliberately outside the free-body hover-definition weaving scope (see hoverStitch)
			// The rich-accordion fallback renders panel bodies with the converter's OWN body
			// machinery so they stay identical to the rest of the page — renderBlock =
			// ListsAndRuns.renderBlackText (bullets become "<ul>", paragraphs become "<p>");
			// renderNested = #interactivePlaceholder for an absorbed nested sub-bundle (for
			// example a shapeHover widget nested inside another one falls back to its own
			// honest cv2-interactive placeholder, addressed by its own index).
			renderBlock: (text) => ListsAndRuns.renderBlackText(text, run, undefined, false),   // built-widget internals are deliberately outside the free-body hover-definition weaving scope
			renderNested: (sub) => this.#interactivePlaceholder(sub, run),
			// The rich-tabs pane renderer needs the kept-table emitter for a captured
			// data-table member (for example the BLL subject family's letter mats), so the
			// pane's table renders IDENTICALLY to an ordinary free-body kept table.
			renderTable: (tblItem) => TablesAndGrids.contentTable(tblItem.block, run, false, this.#norm),
			// A URL-less trailing "[image]" member (for example "[insert item 3]", found on
			// module PHE1005 — the human ships the actual image AFTER the widget) renders
			// through the NORMAL body-path image emitter, so it carries the same standard
			// Mode P/D placeholder-image and caption conventions as any other body image.
			renderImage: (imgItem) => MediaBuilder.image(imgItem, [imgItem], 0, run).join("\n"),
		});
		if (built !== null) {
			bundle.built = true;            // flag for the manifest (built vs un-built)
			// RETAIN embedded writer instructions rather than silently discarding them.
			// A documented CS:/Dev:/Note:/please… note the writer coloured red inside a
			// widget cell/member is stripped from the BUILD (so it never corrupts the
			// widget), but it is NOT learner content to discard — the human designer needs
			// it. Surface each as a red <p> AFTER the built widget. For an activity-OWNED
			// widget the caller emits this return value BEFORE the activity close, so the
			// notes land bottom-but-inside the activity container — exactly the house rule.
			const notes = this.#bundleInstructions(bundle);
			return built + notes.map((t) => NotesAndComments.redFlag(t, run, "cs")).join("");
		}

		// EMPTY-BUNDLE GUARD (body-breakdown #2): an interactive invocation that
		// captured NO content — no member text, no table, no media, no heading —
		// must NOT render a big empty placeholder box. These are inline markers
		// ([highlight text] inside a sentence), stray end markers ([X ends here]),
		// or a data-less invocation. Emit a compact red flag instead, so the marker
		// is still surfaced (and the manifest still lists it) without littering the
		// page with empty interactive shells. (The full placeholder is reserved for
		// bundles that actually carry un-built content.)
		const hasText = (it) => String(it.type === "black" ? it.text : (it.blackAfter ?? "")).trim().length > 0;
		const hasContent = !!(bundle.headingText?.trim())
			|| bundle.instructions.length > 0
			|| (bundle.tables?.length > 0)
			|| (bundle.media?.length > 0)
			|| [...bundle.openerItems, ...bundle.memberItems].some(hasText);
		if (!hasContent) {
			bundle.built = false;
			const label = [bundle.type, ...(bundle.extraTypes ?? [])].join(" + ");
			return NotesAndComments.redFlag(
				`Un-built [${label}] marker — no content captured (an inline marker, a stray end tag, or a writer instruction); see ${run.moduleCode ?? "MODULE"}_interactives.txt.`,
				run);
		}

		const tpl = DataService.Data.EmitTemplates.interactive_placeholder;
		// A writer instruction EMBEDDED inside the interactive is moved to JUST BEFORE the
		// placeholder box: notesBefore prepends the bundle's instructions at the return point
		// instead of nesting them inside the dashed placeholder box itself.
		// Data flag: interactive_placeholder.instructions_before
		// Env toggle: NOTEBEFORE_OFF (reverts to placing the notes INSIDE the box instead)
		// (Notes that were already positioned AFTER an element in the source stay put either way.)
		const notesBefore = (tpl.instructions_before !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.NOTEBEFORE_OFF);
		// EMPTY-BOX GUARD: if the only content the box would RENDER (besides the banner) is
		// the instruction(s), moving them before the box leaves an empty placeholder — so
		// render JUST the notes (no box), mirroring the empty-bundle guard above. The box
		// renders heading + tables + text-bearing members; it does NOT render bundle.media,
		// so media must NOT count here (else a media+instruction bundle becomes a text-empty
		// box once the instruction moves out — body_compare's empty-interactive flag).
		const hasRenderedNonInstr = !!(bundle.headingText?.trim())
			|| (bundle.tables?.length > 0)
			|| [...bundle.openerItems, ...bundle.memberItems].some(hasText);
		if (notesBefore && bundle.instructions.length > 0 && !hasRenderedNonInstr) {
			return bundle.instructions.map((i) => NotesAndComments.redFlag(i, run, "cs")).join("\n");
		}

		// INTERACTIVE EXTRACT (developer HAND-OFF) MODE. When the run is in "extract" mode
		// (turned on either via the UI switch or the env toggle below, applied uniformly
		// across the whole conversion run the same way image mode is), an un-built
		// interactive widget that WOULD normally render the dashed placeholder box below is
		// INSTEAD replaced by a single, prominent, unique REFERENCE CODE marking its exact
		// position on the page; the actual captured content for a developer to work from is
		// handed off separately via the "{CODE}_interactives.txt" file (built by
		// ManifestBuilder), headed by that SAME reference code so the two can be matched up.
		// The default "inline" mode never enters this branch at all, so output with this
		// feature off is byte-identical to before it existed. Only the box-rendering path is
		// diverted here — the empty-marker and instruction-only guard checks above still keep
		// their own normal inline rendering, so no documented writer note ever gets silently
		// dropped from the page just because extract mode is on.
		// ROUND 235 (Chris) — the hand-off is now the DEFAULT, and the marker box
		// CONTAINS the raw content: when extract.collapse is enabled (the shipped
		// default), this branch no longer returns the bare marker. It computes the
		// reference code exactly as before (same id/label, same bundle stash for the
		// .txt cross-reference), then FALLS THROUGH to the normal inline box build
		// below and wraps that byte-exact inline rendering inside the marker box,
		// collapsed by default behind the animated ▼/▲ toggle (extractWrap carries
		// the computed code down to the wrap at the return point). With collapse off
		// (env INTCOLLAPSE_OFF — which also flips the DEFAULT mode back to inline —
		// or data collapse.enabled:false), the branch returns the r138/r159 bare
		// marker unchanged, so INTEXTRACT_ON + INTCOLLAPSE_OFF reproduces the legacy
		// extract output byte-for-byte.
		// Data flag: interactive_placeholder.extract (+ .default_mode, .collapse)
		// Env toggles: INTEXTRACT_ON (legacy force), INTCOLLAPSE_OFF (revert round)
		const ex = tpl.extract;
		let extractWrap = null;
		if (run.interactiveMode === "extract" && ex && ex.enabled !== false) {
			bundle.built = false;                          // an un-built, EXTRACTED placeholder
			const pageIdx = run.pages.indexOf(bundle.page);
			const nn = Utils.Pad2(pageIdx < 0 ? 0 : pageIdx);   // the page's document-order index. ROUND 243: the
			// output FILES now use the library _L_S names (PageAssembler.PageFileNames); the extract
			// REFERENCE code deliberately keeps this stable index form — it is the search-by-code
			// contract between the page marker and {CODE}_interactives.txt (whose File: line carries
			// the real filename), not a filename.
			const seqN = (run.extractCounters.get(pageIdx) || 0) + 1;
			run.extractCounters.set(pageIdx, seqN);        // per-page running number, document order
			// ROUND 205 (Chris) — the reference code is now plain + hyphenated with INT
			// after the module code (e.g. MXDI202-INT-01-01-accordion), and uses ONLY the
			// FIRST widget type (no "+ accordion + accordion" repeats). The old glyph form
			// ⟦INT · MXDI202-01-01 · accordion + …⟧ is reverted by editing ref_format/
			// label_format back in data (they are inherently reversible format strings).
			const code = run.moduleCode ?? "MODULE";
			const seq = Utils.Pad2(seqN);
			const type = bundle.type;                       // first type only (drop extraTypes)
			const id = Utils.FillTemplate(ex.id_format, { code, NN: nn, seq });
			const ref = Utils.FillTemplate(ex.ref_format, { id, code, NN: nn, seq, type });
			const label = Utils.FillTemplate(ex.label_format, { ref, id, code, NN: nn, seq, type });
			// stash on the bundle so ManifestBuilder heads its .txt block with the same code
			bundle.extractRef = ref;
			bundle.extractLabel = label;
			bundle.extractId = id;
			// The reference marker is styled LOUD (a rainbow border and stripes), rather than
			// the site's usual calm blue — the intent is that a developer scanning the page
			// visually cannot possibly miss the hand-off spot. This is a STYLE-ONLY change —
			// the CSS class, the data- attributes, and the {label} text (which is the actual
			// search-by-code contract a developer relies on) are all identical either way.
			// Data flag: extract.marker_loud
			// Env toggle: INTLOUD_OFF (reverts to the plain calm-blue marker style)
			const loudOn = ex.marker_loud_enabled !== false && !!ex.marker_loud
				&& !(typeof process !== "undefined" && process.env && process.env.INTLOUD_OFF);
			const col = ex.collapse;
			const collapseOn = col && col.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.INTCOLLAPSE_OFF);
			if (!collapseOn) {
				// legacy bare-marker extract (r138/r159 byte-exact — no content on page)
				return Utils.FillTemplate(loudOn ? ex.marker_loud : ex.marker, { index: bundle.index, id, ref, label });
			}
			extractWrap = { index: bundle.index, id, ref, label, col };
			// fall through: build the normal inline rendering below, then wrap it
		}

		const parts = [];
		// The un-built placeholder box scrolls horizontally instead of overflowing the page
		// layout, for whenever the raw member dump inside it (especially wide captured
		// tables) is wider than the box itself: "overflow-x: auto" means a scrollbar
		// appears exactly and only when there's actually an overflow, applied on the OUTER
		// dashed box so its frame stays visually fixed in place while just the content inside
		// it scrolls.
		// Data flags: interactive_placeholder.scroll_x, interactive_placeholder.block_open_scroll
		// Env toggle: INTSCROLLX_OFF (reverts to the earlier box style, without the scroll behaviour)
		const scrollOn = tpl.scroll_x?.enabled !== false && !!tpl.block_open_scroll
			&& !(typeof process !== "undefined" && process.env && process.env.INTSCROLLX_OFF);
		parts.push(Utils.FillTemplate(scrollOn ? tpl.block_open_scroll : tpl.block_open, { index: bundle.index }));
		parts.push(Utils.FillTemplate(tpl.block_banner, {
			index: bundle.index,
			// multi-widget activities show every absorbed type (BLL155 1A:
			// "carousel + selfCheck" — ONE activity, one placeholder)
			type: [bundle.type, ...(bundle.extraTypes ?? [])].join(" + "),
			modifierLabel: bundle.modifier ? Utils.FillTemplate(tpl.modifier_label, { modifier: bundle.modifier }) : "",
			activityId: bundle.activityId ?? tpl.no_activity_label,
			manifestFile: `${run.moduleCode ?? "MODULE"}_interactives.txt`,
		}));
		parts.push(tpl.member_dump_open);

		if (bundle.headingText) parts.push(`<h4>${Utils.EscapeHtml(bundle.headingText)}</h4>`);
		if (!notesBefore) for (const instr of bundle.instructions) parts.push(NotesAndComments.redFlag(instr, run, "cs"));

		// member dump: text members render TOGETHER (so the writer's
		// numbered/bulleted option lists group into one list, not N
		// single-item lists); tables render at their position.
		// OPENER items render FIRST — they carry the activity's own title
		// and instruction lines, which are part of the captured bundle
		// (without this, BLL146's Activity 1E lost its heading text).
		let textRun = [];
		const flushText = () => {
			if (textRun.length) parts.push(...ListsAndRuns.renderBlackText(textRun.join("\n"), run, undefined, false));   // this raw cv2 placeholder dump is a developer hand-off, not free-body text — the hover-definition weaving (hoverStitch) is deliberately skipped here
			textRun = [];
		};
		// openerItems are only populated for inline (non-activity) bundles;
		// activity-owned bundles render their openers as activity content
		// OUTSIDE the box, so the box holds members only
		for (const m of [...bundle.openerItems, ...bundle.memberItems]) {
			if (m.type === "table") { flushText(); parts.push(TablesAndGrids.contentTable(m.block, run, true, this.#norm)); continue; }
			const text = m.type === "black" ? m.text : (m.blackAfter ?? "");
			// don't repeat the line already shown as the bundle heading
			if (text.trim() && text.trim() !== bundle.headingText.trim()) textRun.push(text);
		}
		flushText();

		parts.push(tpl.member_dump_close);
		parts.push(tpl.block_close);
		const lead = notesBefore
			? bundle.instructions.map((i) => NotesAndComments.redFlag(i, run, "cs")).join("\n")
			: "";
		const inlineHtml = (lead ? lead + "\n" : "") + parts.join("\n");
		// ROUND 235 (Chris) — the default hand-off wrap: the byte-exact inline
		// rendering above (retained notes + the dashed box) goes INSIDE the loud
		// reference-code marker box, collapsed by default behind the animated
		// arrow toggle. The wrapper carries BOTH classes — cv2-interactive (so
		// every gate exclusion and verbatim-zone walk treats the whole box exactly
		// like the old placeholder) and cv2-int-ref (the Page Stitcher's
		// search-by-code contract: replacing the wrapper by data-cv2-ref swaps the
		// hidden raw content out together with the marker).
		if (extractWrap) {
			const c = extractWrap.col;
			return [
				Utils.FillTemplate(c.wrapper_open, { index: extractWrap.index, id: extractWrap.id, ref: extractWrap.ref }),
				Utils.FillTemplate(c.label_row, { label: extractWrap.label }),
				c.content_open,
				inlineHtml,
				c.content_close,
				c.wrapper_close,
			].join("\n");
		}
		return inlineHtml;
	};

	// =======================================================================
	// TEXT RENDERING HELPERS
	// =======================================================================

	/**
	 * Drops NOTE-RESIDUE empty bullets — a LONE empty "<ul><li></li></ul>" left behind by a
	 * writer's bulleted instruction once its text has already been lifted out into a
	 * cv2-note instead (found on modules MXDI202-00 and BLL126-01). This is a post-pass over
	 * the fully assembled body, following the same general pattern as
	 * MediaBuilder.stripMediaResidue: the measured signature to look for is a SINGLE empty
	 * "<li>" list immediately FOLLOWED by a cv2-note paragraph — this needs to be a
	 * post-pass rather than handled at emit time, because it also needs to correctly handle
	 * a RUN of several consecutive bulleted instructions where the bullet and its
	 * corresponding note aren't directly adjacent to each other at the moment each one is
	 * individually emitted (an earlier attempt to strip this at emit time missed 7 of the 63
	 * measured occurrences for exactly that reason). Measured (see
	 * outputs/_measure_loneempty.py): 63 occurrences across 25 modules in the converter's
	 * output; the human developer ships zero of these. A genuinely populated list, a
	 * multi-blank worksheet scaffold (2 or more empty "<li>" items — a deliberate blank
	 * template for the learner to fill in), and a deliberate lone blank bullet that is NOT
	 * followed by a note are all correctly left intact by this.
	 * Data flag: body_region.list_nesting.drop_note_residue_bullet
	 * Env toggle: NOTEBULLET_OFF
	 */
	static #dropNoteResidueBullets(html) {
		const cfg = DataService.Data.EmitTemplates.body_region?.list_nesting ?? {};
		if (!(cfg.drop_note_residue_bullet ?? true)) return html;
		if (typeof process !== "undefined" && process.env && process.env.NOTEBULLET_OFF) return html;
		// a RUN of one-or-more consecutive single-item empty lists ending at a cv2-note: each is a
		// bulleted instruction whose text was lifted to the note (HIS1003-07 / XGF9003-00 stack 3).
		return html.replace(/(?:<ul[^>]*>\s*<li[^>]*>\s*<\/li>\s*<\/ul>\s*)+(?=<p[^>]*cv2-note)/gi, "");
	}

	/**
	 * Drops a leaked CLOSER directive's residue (the "[end X] leftover-leak" problem). A
	 * writer's closing tag — "[End page]" / "[End of important box]" / "[End interactive]" /
	 * "[End of task]" and similar — is a DIRECTIVE that is supposed to render nothing at
	 * all, but in a handful of rendering contexts (inside a black-text run, a coalesced run
	 * of text, or a flowing quote box) it ended up surviving as a LONE, visible
	 * "<p>[tag]</p>" instead of being fully suppressed. This post-pass removes such a "<p>"
	 * whenever the bracket text (a) carries the standalone word "end" or "ends", AND (b)
	 * actually resolves, via the real tag normaliser, to a genuine CONTAINER_CLOSE or
	 * PAGE_BOUNDARY directive (i.e. it's classified as a real tag, not just red-coloured
	 * prose).
	 *  - The "end" word-guard is the precision floor here: it EXCLUDES a heading that
	 *    happens to mis-resolve to something else ("[Lesson Summary]" resolves as a
	 *    lesson/PAGE_BOUNDARY tag, but contains no "end" word) AND excludes the "[next
	 *    page]" page-break OPENER tags.
	 *  - The tag-resolver guard EXCLUDES genuine content that happens to contain the word
	 *    "end" (for example "[… near the end of a book]" resolves as an OPENER tag, not a
	 *    closer, so it's correctly left alone).
	 *  - A bracket that carries embedded CONTENT alongside it (for example "[Lesson 2] THE
	 *    WORLD COURT") is never rendered as a LONE, empty "<p>" to begin with, so it's
	 *    naturally untouched by this — only a "<p>[ … ]</p>" containing nothing but the
	 *    bracket itself can ever match this pattern.
	 * The general "[end X]" closer CONVENTION itself is already fully built and working
	 * (97.9% of such tags resolve correctly on their own) — this method only cleans up the
	 * small amount of leftover leaked residue downstream of that. Measured: 21 occurrences
	 * across 6 modules in the converter's output; the human developer ships zero of these.
	 * Data flag: body_region.closer_residue_strip
	 * Env toggle: ENDCLOSER_OFF
	 */
	static #stripCloserResidue(html) {
		const cfg = DataService.Data.EmitTemplates.body_region?.closer_residue_strip;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.ENDCLOSER_OFF) return html;
		if (!this.#norm) return html;
		return html.replace(/<p>\s*(\[[^\]<]*\])\s*<\/p>\s*/gi, (whole, bracket) => {
			if (!/\bends?\b/i.test(bracket)) return whole;          // must carry the 'end' closer word
			let parse; try { parse = this.#norm.Parse(bracket); } catch { return whole; }
			const p = parse && parse.primary;
			const isCloser = parse && parse.class === "tag" && p
				&& (p.directive === "CONTAINER_CLOSE" || p.directive === "PAGE_BOUNDARY");
			return isCloser ? "" : whole;                           // a recognised end-closer renders nothing
		});
	}

	/**
	 * THE XDLS900 CHOICE-PAGE TILE GRID (ROUND 226 — Chris's XDLS900 screenshot triage;
	 * population = EXACTLY XDLS902-906, measured over ALL 431 dirs by
	 * outputs/_detect_choicetiles.cjs). Builds the human's icon-tile navigation row
	 * ("row > col-12.choicePage… > div.choice.col-md-3.col-6" per tile) from the writer's
	 * own material: ONE tile per LESSON (the first page of each distinct writer lesson
	 * number, in document order), labelled with the writer's [Tab Nav Layout] category for
	 * that position (state.labels, harvested from the one-column table — XDLS906's gold
	 * uses them verbatim) or, when the writer authored no category table (XDLS902), the
	 * lesson's own TITLE (which IS what that module's gold shows). Each tile links to the
	 * lesson's GENERATED HTML file (Chris's decision 2026-07-15 — the gold's online MTK
	 * quickLink rcodes exist nowhere in the WT), resolved deterministically from the page's
	 * index in run.pages exactly the way PageAssembler names the output files. iconType
	 * ships EMPTY (icon choice is editorial — the gold pages carry their own "CS: review
	 * iconType" comments); the caller surfaces one To Do note listing the tiles.
	 * Returns { html, labels } or null when the module has no lesson pages.
	 * Data flag: body_region.choice_page_tiles   Env toggle: CHOICETILES_OFF
	 */
	static #choicePageTiles(run, state) {
		const cfg = state.cfg;
		const naming = DataService.Data.EmitTemplates.output_naming;
		const code = run.moduleCode ?? "MODULE";
		const lessons = [];
		const seen = new Set();
		(run.pages ?? []).forEach((p, idx) => {
			if (p.isOverview || p.lessonNumber == null) return;
			const n = String(p.lessonNumber);
			if (seen.has(n)) return;   // only the FIRST page of a multi-file lesson is linked
			seen.add(n);
			lessons.push({ idx, n, title: String(p.pageTitle ?? "").replace(/\*/g, "").trim() });
		});
		if (!lessons.length) return null;
		// NO-TABLE dialect (XDLS902): the tile labels are the lesson TITLES, so only TITLED
		// lessons are tiled — an untitled page is a continuation fragment (XDLS902's
		// pre-existing "2.0" lesson-tail over-split), not a learning area; its gold ships
		// exactly the 7 titled lessons as tiles. With a category table the writer's own
		// list drives the count and maps positionally.
		const tiled = state.labels.length ? lessons : lessons.filter((l) => l.title);
		if (!tiled.length) return null;
		const labels = [];
		const tiles = tiled.map((l, k) => {
			const label = String(state.labels[k] ?? "").trim() || l.title || `Lesson ${l.n}`;
			labels.push(label);
			return Utils.FillTemplate(cfg.tile, {
				// ROUND 243: through the shared filename source of truth, so a tile
				// href ALWAYS matches the emitted file (library _L_S form or legacy).
				href: PageAssembler.PageFileNames(run)[l.idx],
				target: cfg.link_target ?? "_self",
				label: Utils.EscapeHtml(label),
			});
		});
		if (state.labels.length > tiled.length) run.AddNote("warn", "ContentConverter",
			`Choice page: ${state.labels.length} tab-nav categories but only ${tiled.length} lessons — the extra categories were not tiled.`);
		return { html: Utils.FillTemplate(cfg.shell, { tiles: tiles.join("\n") }), labels };
	}

	/** A standalone content table → a real <table> (header row = <th>). */
	// Renders a side-alert box that the writer AUTHORED as a single-cell TABLE, where that
	// cell leads with a positional tag like "[Alert box on right hand side]" (found on
	// module ENGS302-01) — this matches the human developer's
	// "<col><div class="alert top">…</div></col>" output. Without this, the ordinary
	// layout-table-to-grid conversion would drop the "[alert]" tag entirely and leak its raw
	// content as plain text instead. Returns null unless the table's leading tag is a
	// recognised positional "[alert]" variant.
	// Data flag: body_region.alert_table
	// Env toggle: ALERTTBL_OFF
	static #alertTable(rows, run) {
		const cfg = DataService.Data.EmitTemplates.body_region?.alert_table;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.ALERTTBL_OFF) return null;
		if (!rows?.length || rows.length !== 1) return null;
		const cells = (rows[0] || []).filter((c) => String(c ?? "").trim() !== "");
		if (cells.length !== 1) return null;
		const parts = TablesAndGrids.cellParts(cells[0]);
		if (!parts.length) return null;
		const lead = parts[0].match(/^\[([^\]]+)\]/);
		if (!lead) return null;
		let canon = null;
		try { canon = this.#norm.Parse(`[${lead[1]}]`)?.primary?.tag ?? null; } catch { canon = null; }
		if (!(cfg.alert_tags ?? ["alert", "important"]).includes(canon)) return null;
		const phrase = lead[1].toLowerCase();
		let colClass = cfg.default_col ?? "col-12";
		let modifiers = canon === "important" ? " solid" : "";
		let positioned = false;
		for (const pos of (cfg.positional ?? [])) {
			if (new RegExp(pos.match, "i").test(phrase)) { colClass = pos.col; modifiers += pos.modifiers ?? ""; positioned = true; break; }
		}
		if (cfg.positional_only && !positioned) return null;
		for (const [kw, cls] of Object.entries(cfg.extra_modifier_keywords ?? {})) {
			if (new RegExp(`\\b${kw}\\b`, "i").test(phrase) && !modifiers.includes(cls.trim())) modifiers += cls;
		}
		const inner = TablesAndGrids.renderCellParts(parts.slice(1).join(" / "), run, this.#norm).filter(Boolean);
		if (!inner.length) return null;
		const open = Utils.FillTemplate(cfg.wrap_open, { colClass, modifiers });
		const html = open + "\n" + inner.join("\n") + "\n" + cfg.wrap_close;
		// Also exposes the COL-ONLY portion (just the column plus the alert box inside it,
		// with NO outer row wrapper) so that the converter can PAIR a right-positioned alert
		// as the "col-md-4" right-hand sibling of the FOLLOWING content's "col-md-8" column,
		// both sharing one row — matching the human developer's same-row layout. The `side`
		// flag returned below is true only for a genuinely positioned alert (one that got a
		// real, specific column class assigned, not just the generic default column).
		// Data flag: body_region.alert_table.side_pair
		const colOpen = Utils.FillTemplate(cfg.side_col_open ?? "<div class=\"{colClass}\">\n<div class=\"alert{modifiers}\">", { colClass, modifiers });
		const col = colOpen + "\n" + inner.join("\n") + "\n" + (cfg.side_col_close ?? "</div>\n</div>");
		return { html, col, side: positioned && colClass !== (cfg.default_col ?? "col-12") };
	};

	/**
	 * Gathers ONLY a PROVERB's lines for a proverb callout (whakataukī) — the
	 * leading SHORT line(s), stopping BEFORE the commentary so it is NOT consumed
	 * and renders as free body. Robust to the variations the corpus shows:
	 *  - reo SEP english on ONE line (the marker's own paragraph): held as the
	 *    single proverb line (later split on the separator → 2 <p>s). A following
	 *    short line is NOT also pulled in, because the english is already present.
	 *  - reo on the marker line, english on the NEXT line (no separator on line 1):
	 *    the next SHORT line is pulled in as the english; a long paragraph stops it.
	 *  - proverb with no commentary: the next item is a marker → stops anyway.
	 * The "short vs long" test is the signal that generalises (a proverb line is a
	 * phrase; commentary is explanatory prose) — measured 137/147 human whakataukī
	 * hold exactly the 2 proverb <p>s, only 4 hold a long paragraph.
	 *
	 * @param {Object} def - the callout def (proverb_max_chars / proverb_max_paragraphs)
	 * @returns {string} the proverb text (newline-joined); commentary left un-consumed
	 */
	/**
	 * PROVERB NORMALISE — the SPLIT half (round 225; the strip half is
	 * #proverbStripSeg). Re-derives the writer's own two proverb lines (reo +
	 * English) when they arrive GLUED into one, which happens because the docx
	 * extractor drops a paragraph-internal SOFT line break (w:br) — the writer's
	 * break is gone but its position is still visible as a boundary in the raw
	 * text. Four measured boundary shapes, first match wins, at most ONE split
	 * per line (a proverb is reo + English, never more):
	 *  - markup boundary: a leading bold or italic marker group (inner ≥10 chars, so
	 *    a mangled ***“*** fragment like XLP03's can never split mid-proverb)
	 *    directly followed by more text — XDLS903/905/906/912, XMES203, CEDW501, XLP01;
	 *  - quote boundary: a leading “quoted” phrase, then whitespace + prose — CEDO301;
	 *  - loose pipe: whitespace BEFORE a pipe, none required after ("riri |*Well
	 *    done…*", OSBY301 — the strict spaced-pipe rule above requires both sides);
	 *  - paren translation: a full-tail "(english translation)" (≥6 chars each
	 *    side) — ENGR102; the parentheses are dropped, matching gold.
	 * A line carrying a URL is never touched. The no-marker language-boundary glue
	 * (CEDT501-12 "kōrero. The food…", CEDO105) has NO derivable split point —
	 * measured decline, left as-is.
	 * Data flag: callouts.by_tag.<tag>.proverb_normalise
	 * Env toggle: PROVERBNORM_OFF
	 *
	 * @param {string} content - the gathered proverb text (newline-joined)
	 * @param {Object} cfg - the def's proverb_normalise object
	 * @returns {string} the content with re-derived line breaks
	 */
	static #proverbSplit(content, cfg) {
		if (cfg.enabled === false) return content;
		if (typeof process !== "undefined" && process.env && process.env.PROVERBNORM_OFF) return content;
		const out = [];
		for (const raw of content.split("\n")) {
			const line = raw.trim();
			if (!line || line.includes("http")) { out.push(raw); continue; }
			let m = null;
			if (cfg.split_markup_boundary !== false) {
				// EXACT marker pairs (** with **, * with *) — an alternation, never a
				// {1,2} quantifier: backtracking on \*{1,2} let the closing ** DONATE
				// an asterisk to the tail, splitting off a junk "*" line (XDLS904,
				// XTAS101 — caught on the round-225 A/B). Optional whitespace before
				// the tail; the tail must carry REAL text (a letter/digit once its own
				// markers are removed), so a lone leftover marker can never split.
				m = line.match(/^(\*\*[^*]{10,}\*\*|\*[^*]{10,}\*)\s*(\S.*)$/);
				if (m && !/[\p{L}\p{N}]/u.test(m[2].replace(/\*/g, ""))) m = null;
			}
			if (!m && cfg.split_quote_boundary !== false)
				m = line.match(/^([“”"][^“”"]{6,}[“”"])\s+(\S.*)$/);
			if (!m && cfg.split_pipe_loose !== false && /\s\|/.test(line)) {
				const p = line.split(/\s+\|\s*/);
				if (p.length >= 2 && p[0] && p[1]) m = [line, p[0], p.slice(1).join(" ")];
			}
			if (!m && cfg.split_paren_translation !== false)
				m = line.match(/^([^()]{6,}?)\s+\(([^()]{6,})\)$/);
			out.push(m ? m[1].trim() + "\n" + m[2].trim() : raw);
		}
		return out.join("\n");
	};

	/**
	 * PROVERB NORMALISE — the STRIP half (round 225). The human ships proverb
	 * <p>s PLAIN: bold stripped (gold keeps <b> in only 2/215 .whakatauki boxes),
	 * italic stripped (5/215), wrapping curly/straight quotes stripped (9/215) —
	 * the site CSS supplies the bold/italic proverb styling, so a kept <b> both
	 * mismatches gold AND double-styles in the browser. Runs on the RENDERED
	 * segment (after renderBlackText) so the shared MenuBuilder strip helpers
	 * resolve even a mangled ***triple-marker*** run cleanly; quote/asterisk
	 * strips are EDGE-anchored to the <p> tags so an interior quote in prose is
	 * never touched. The tiny gold keep-minority has no discriminator →
	 * NET-POSITIVE class (the r164 precedent).
	 *
	 * @param {string} h - one rendered HTML segment
	 * @param {Object} cfg - the def's proverb_normalise object
	 * @returns {string} the normalised segment
	 */
	static #proverbStripSeg(h, cfg) {
		let s = h;
		if (cfg.strip_bold !== false) s = MenuBuilder.stripTextBold(s);
		if (cfg.strip_italic !== false) s = MenuBuilder.stripTextItalic(s);
		if (cfg.strip_wrapping_quotes !== false)
			s = s.replace(/(<p[^>]*>)\s*(?:[“”"]|&quot;)+\s*/g, "$1")
				.replace(/\s*(?:[“”"]|&quot;)+\s*(<\/p>)/g, "$1")
				.replace(/(<p[^>]*>)\s*\*+\s*/g, "$1")
				.replace(/\s*\*+\s*(<\/p>)/g, "$1")
				// an ORPHAN edge pipe — the writer typed the reo|english separator
				// INSIDE the bold group ("**…rangatahi |**", OSSM301), so the pipe
				// split never saw it and it survives as a dangling boundary char;
				// the human ships 0 proverb lines edged with a separator (the r177
				// title boundary-separator class)
				.replace(/(<p[^>]*>)\s*\|\s*/g, "$1")
				.replace(/\s*\|\s*(<\/p>)/g, "$1");
		return s;
	};

	static #gatherProverb(it, bodyItems, i, def) {
		const maxChars = def.proverb_max_chars ?? 200;
		const maxPara = def.proverb_max_paragraphs ?? 2;
		const sepRe = /\s[|–—]\s/;                 // reo|english separator on one line
		const first = (it.blackAfter ?? "").trim();
		const parts = first ? [first] : [];
		// only look for the english on a SEPARATE line when it is not already on the
		// first line (i.e. the first line carries no reo|english separator)
		if (!sepRe.test(first)) {
			for (let j = i + 1; j < bodyItems.length && parts.length < maxPara; j++) {
				const next = bodyItems[j];
				if (next.type !== "black" || next.consumedBy !== undefined) break;
				if ((next.text ?? "").trim().length > maxChars) break;   // commentary → free body
				parts.push(next.text.trim());
				next._consumed = true;
			}
		}
		return parts.join("\n");
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ContentConverter };
