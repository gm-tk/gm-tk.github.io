/**
 * MenuBuilder.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Builds the MODULE MENU — the tabbed or "simplified" navigation block that
 * sits near the top of a converted page, surfacing things like the module's
 * Learning Intentions / Success Criteria, curriculum headings (Understand /
 * Know / Do), and lesson links, laid out however that subject and page type
 * (module overview page vs. an inner lesson page) is supposed to look. Six
 * static methods:
 *
 *   - menuTypeFor(page, run)  decides the menu's SHAPE for this page —
 *         "tabs", "simplified", or "none" (some subjects show no menu at
 *         all) — by looking up rows in the page-role-aware
 *         Menu_Scaffold_Registry (env MENUREG_OFF reverts to an older,
 *         cruder set of preserved rows; MENUNONE_OFF disables the
 *         "sibling page-type already says none" fallback rule)
 *   - buildMenu(menuItems, menuType, run, page, norm)  THE menu emitter —
 *         turns the captured menu items into rendered HTML panes. Covers
 *         the plain tabs/simplified case plus several subject-family
 *         layouts: the two-column curriculum split used by the "ENG"
 *         subject family (env MENUCURRIC_OFF), the "banner" family layout
 *         (env BANNERMENU_OFF), a curriculum split-all variant
 *         (env CURRICSPLIT_OFF), and a general italic-strip cleanup pass
 *         applied to every pane (env MENUITALIC_OFF)
 *   - isReoModule(run)  true for bilingual (te reo Māori / English) modules
 *         — those menus KEEP italic styling on BOTH the Māori line and its
 *         English translation, so the general italic strip above must skip
 *         them (detected via the TRR/PNR module-code prefix or the
 *         reoTranslate body class)
 *   - stripTextItalic(html)  strips <i>/<em> wrapper tags out of a menu
 *         pane's HTML while keeping the inner text, and while leaving any
 *         Font-Awesome icon markup (<i class="fa...">) untouched
 *   - stripTextBold(html)  the bold-stripping sibling of stripTextItalic;
 *         also reused by ContentConverter's alert-box bold strip
 *         (env ALERTBOLD_OFF)
 *   - curriculumLevel(run, engCfg)  picks which heading level (h1..h6) the
 *         Understand/Know/Do curriculum heading should render at — this
 *         varies by subject and by school phase (year group) in the
 *         two-column menu families
 *   - dropEmptyHeadings(html, run)  removes a menu heading that has no
 *         content underneath it before the next heading — an empty
 *         placeholder heading nobody actually wants rendered
 *
 * WHY SEPARATE FILE:
 * Menu building used to live inline inside ContentConverter, the class that
 * emits the rest of the page body. It was carved out into its own file so
 * that "how the module menu renders" is a self-contained, easy-to-find unit
 * instead of buried among thousands of unrelated lines. Moving code into its
 * own file changes WHERE it lives, never WHAT it produces — every method
 * here behaves exactly as it did before the move.
 *
 * A NOTE ON THE `norm` PARAMETER: this class has no instance state of its
 * own — like every file in this app, it reads shared configuration off the
 * global DataService.Data object. The one thing it does NOT own is the tag
 * normaliser (the object that resolves a writer's `[tag]` markers into
 * structured data): that instance belongs to the caller (ContentConverter)
 * and is simply passed in as the `norm` argument to buildMenu, which uses it
 * for exactly two things — one pass-through call into
 * TablesAndGrids.contentTable, and one direct call to norm.RenderText().
 * Two closely related behaviours are deliberately NOT in this file and still
 * live in ContentConverter: deciding which page items even count as "menu
 * items" in the first place (env MENUSTOP_OFF / BARELEAD_OFF), and promoting
 * certain named headings ahead of the menu (env MENULEADIN_OFF).
 *
 * WHEN TO WORK HERE:
 * Any time the module menu — the tabbed/simplified block near the top of a
 * page — renders the wrong shape, puts content in the wrong column, uses the
 * wrong heading level, or keeps/strips italic or bold styling incorrectly
 * for a given subject or page type. The layout rules themselves live in
 * Emit_Templates.json's `menu` section and are read by the methods above;
 * most fixes are a data change there plus the minimal method logic needed to
 * apply it.
 * ===========================================================================
 */

class MenuBuilder {

	/**
	 * Decides the menu SHAPE for this page: "tabs", "simplified", or "none".
	 *
	 * WHAT/HOW: menu shape is not invented by this code — it is MEASURED from
	 * the library of already human-built modules (which subjects, phases, and
	 * page types actually carry a tabs menu, a simplified list, or no menu at
	 * all) and stored in data/Menu_Scaffold_Registry.json. This method looks
	 * up that recorded value using a cascade from most-specific to
	 * most-general, returning the first match found:
	 *   1. Series Anchor  — this EXACT module code has its own recorded value
	 *   2. Group Majority — the majority value recorded for this subject +
	 *      school phase combination (e.g. key "MXFL|4-6" = subject letters
	 *      "MXFL", phase "4-6")
	 *   3. Style-Anchor / global default — a generic fallback value
	 *
	 * @param {Object} page - the page being built; page.isOverview tells us
	 *   whether this is the module's overview (landing) page or an inner
	 *   lesson page, since the two can use different menu shapes
	 * @param {Object} run - the conversion run context (module code,
	 *   resolved rules, etc.)
	 * @returns {"tabs"|"simplified"|"none"}
	 */
	static menuTypeFor(page, run) {
		const scope = page.isOverview ? "overview" : "lesson";
		// PRIMARY: menu_type measured from the human corpus per subject×phase
		// (the Group Majority — data/Menu_Scaffold_Registry.json, keyed by
		// run.groupKey "subjectLetters|template_phase"). This corrects the
		// Style-Anchor menu_type where it disagreed with the human (e.g. a lesson
		// menu wrongly suppressed, or one added where the human has none).
		// Cascade: audited group value → Style-Anchor value → global default.
		// key = subject letters of the module code + resolved template_phase, the
		// SAME shape derive_menu_type.cjs writes (e.g. "MXFL|4-6").
		const subj = run.moduleCode?.match(/^[A-Za-z]+/)?.[0] ?? "";
		const phase = run.resolvedRules?.template_phase ?? "";
		const ms = DataService.Data.MenuScaffold;
		// The registry rows are mined PAGE-ROLE-AWARE by derive_menu_type.cjs: lesson
		// evidence is taken only from each module's FIRST lesson page, so a family
		// with mostly-empty "1.1, 1.2, ..." continuation pages doesn't get diluted
		// down to a false "none" verdict just because most of its pages are blank
		// continuations (e.g. a module whose lesson pages 1.0-6.0 all carry a
		// Learning-Intentions menu must not be miscounted as menu-less). The miner
		// also correctly parses module codes/filenames that are heavy with digits
		// instead of tripping over them. Env MENUREG_OFF=1 reverts to an older,
		// cruder set of mined rows (legacy_groups/legacy_series) for comparison.
		const legacyReg = typeof process !== "undefined" && process.env && process.env.MENUREG_OFF;
		const regGroups = (legacyReg && ms?.legacy_groups) ? ms.legacy_groups : ms?.groups;
		const regSeries = (legacyReg && ms?.legacy_series) ? ms.legacy_series : ms?.series;
		// Cascade: Series Anchor (this module's own code) → Group Majority
		// (subject×phase) → Style-Anchor → global default.
		const grp = regGroups?.[`${subj}|${phase}`];
		const fromAudit = regSeries?.[run.moduleCode]?.[scope] ?? grp?.[scope];
		if (fromAudit) return ["tabs", "simplified"].includes(fromAudit) ? fromAudit : "none";
		// MENU-LESS FAMILY FALLTHROUGH: if THIS scope (overview or lesson) has no
		// measured evidence for the module's group, but the OTHER scope's measured
		// value is an explicit "none", treat the whole family as menu-less rather
		// than falling through to the generic Style-Anchor default below and
		// fabricating a menu the human developers never build. Example: a
		// fundamentals-template subject whose LESSON pages are measured "none" but
		// whose OVERVIEW page was never measured — without this rule the converter
		// would wrongly bolt an extra list menu onto that overview page. This check
		// is deliberately narrow: it only fires when the sibling scope is an
		// EXPLICIT "none", so a family that genuinely does have a menu on one scope
		// (but just hasn't been measured yet on the other) is left untouched.
		// Data: menu.none_family_fallthrough. Env: MENUNONE_OFF disables this rule.
		const nf = DataService.Data.EmitTemplates?.menu?.none_family_fallthrough;
		if (nf !== false && !(typeof process !== "undefined" && process.env && process.env.MENUNONE_OFF)
			&& grp && (grp[scope] === null || grp[scope] === undefined)) {
			const other = scope === "overview" ? "lesson" : "overview";
			if (grp[other] === "none") return "none";
		}
		const value = (run.resolvedRules?.menu_type ?? {})[scope];
		// "—" / "n/a" / missing = absent by design (ConnectED finding)
		return ["tabs", "simplified"].includes(value) ? value : "none";
	};

	/**
	 * Builds the module menu's rendered HTML from its captured source items
	 * (the headings/paragraphs/tables that were identified upstream as
	 * belonging to the menu region of the page, in document order).
	 *
	 * WHAT/HOW (the two base shapes; several subject-family variations are
	 * layered on top of these further down in the method body):
	 *   - "tabs":       each heading routes its following content into EITHER
	 *                   tab 1 or tab 2, decided by matching the heading text
	 *                   against Emit_Templates menu.tab_map (case/diacritic-
	 *                   folded match). A heading matching neither list still
	 *                   goes into tab 1, but gets a visible red note attached
	 *                   — an unrecognised heading is SURFACED, never silently
	 *                   absorbed, so a gap in tab_map's vocabulary is easy to
	 *                   notice and fix.
	 *   - "simplified": every heading becomes a plain <h5>; all content stays
	 *                   in its original document order underneath.
	 *
	 * @param {Array} menuItems - the page items captured as menu content, in
	 *   document order (headings, plain-text paragraphs, tables, ...)
	 * @param {"tabs"|"simplified"|"none"} menuType - the shape decided by
	 *   menuTypeFor()
	 * @param {Object} run - the conversion run context
	 * @param {Object} page - the page being built (page.isOverview matters
	 *   for several of the layout variants below)
	 * @param {TagNormaliser} norm - the tag-normaliser instance, owned by the
	 *   caller and passed in for the two spots that need it (see the file
	 *   header note on `norm`)
	 * @returns {Object} e.g. for a simplified menu:
	 *   { kind: "simplified", archetype: "flat", content: "<h5>...</h5>...",
	 *     tab1: "", tab2: "", left: "", right: "" }
	 *   ...or for a tabs menu: { kind: "tabs", archetype: "tabs",
	 *     tab1: "<h5>...</h5>", tab2: "<h5>...</h5>", content: "", ... }
	 *   Some subject families additionally fill tab1Cols / tab2Cols (an array
	 *   of { cls, html } column objects) or funLiCols (see
	 *   #fundamentalsOverviewLi) instead of, or alongside, the plain strings.
	 */
	static buildMenu(menuItems, menuType, run, page, norm) {
		if (menuType === "none" || !menuItems.length) {
			return { kind: menuType, tab1: "", tab2: "", content: "", left: "", right: "" };
		}
		const tpl = DataService.Data.EmitTemplates.menu;

		// FUNDAMENTALS OVERVIEW LI/SC MENU: some "Fundamentals"-template modules put
		// their Learning-Intentions / Success-Criteria block in the front matter under
		// an [Overview] marker rather than as ordinary body headings. Upstream (in
		// ContentConverter's #partitionItems), those captured items get flagged
		// `_funLi` — but ONLY when a matching registry row exists for this module's
		// subject/phase, so this branch and that earlier capture step can never
		// disagree about whether this menu shape applies. When flagged items are
		// present, compose them into the two registry-defined columns (see
		// #fundamentalsOverviewLi below) and return immediately — a leftover
		// front-matter "code" line (e.g. a bare "<p>HPFUN903</p>") is intentionally
		// dropped, matching what the human-built pages do. If the compose step
		// declines (returns null, meaning this module doesn't cleanly fit the
		// pattern), we fall through to the generic walk below instead. Env
		// FUNMENU_OFF disables the upstream CAPTURE step (the one choke point that
		// controls this), so this whole branch is simply never reached when that
		// toggle is set.
		if (menuItems.some((it) => it._funLi)) {
			const funCols = this.#fundamentalsOverviewLi(menuItems, run, page, norm,
				tpl.fundamentals_overview_li ?? {});
			if (funCols) {
				return { kind: menuType, archetype: "fundamentals_li", funLiCols: funCols,
					tab1: "", tab2: "", content: "", left: "", right: "" };
			}
		}

		// LEVEL-PAGE FUNDAMENTALS TABS (ROUND 265 — the CHFUN "[PAGE N Novice]"
		// dialect, module CHFUN01). ContentConverter's level-pages pre-pass
		// captured the module's [Overview]-section LI/SC blocks plus every
		// "[Page Overview]" learning-intentions block (aggregated BY LEVEL)
		// onto run._levelMenu; compose them here into the human's tabbed menu —
		// one "Overview" tab + one tab per LEVEL (Novice, Emergent, …), each
		// pane a two-column LI | SC row — rendered through the same bare
		// div.tabs shell the writer-authored tab partition uses (writer_tabs).
		// Data: body_region.fundamentals_panels.level_pages.
		// Env toggle: LEVELPAGE_OFF (the upstream pre-pass never sets
		// run._levelMenu when it is off, so this branch is never reached).
		if (run._levelMenu) {
			const lm = this.#levelTabs(run._levelMenu);
			if (lm) {
				run.AddNote("info", "MenuBuilder",
					`Overview menu composed as level tabs (Overview + ${run._levelMenu.levels.map((l) => l.label).join(", ")}; fundamentals_panels.level_pages).`);
				return { kind: menuType, archetype: "writer_tabs", wtNav: lm.nav, wtPanes: lm.panes,
					tab1: "", tab2: "", content: "", left: "", right: "" };
			}
		}

		// MTK DROP-DOWN-MENU BILINGUAL TABS (ROUND 212 — the PNR101/102/104 family).
		// ContentConverter's #partitionItems flagged the "[Content for DROP DOWN
		// MENU]" section's English|Māori table "_reoDropdown"; compose it here into
		// the human's bilingual tabs menu (nav <span reo>/<span eng> labels, one
		// tab-pane per [TABn] row, reo/eng element pairs inside). If the compose
		// declines (no [TABn] rows found), fall through to the generic walk below.
		// Data: elements.dual_language.dropdown_menu. Env toggle: REODROPMENU_OFF
		// (that toggle disables the upstream capture, so this branch is never
		// reached when it is set).
		if (menuItems.some((it) => it._reoDropdown)) {
			const ddCfg = DataService.Data.EmitTemplates.elements?.dual_language?.dropdown_menu ?? {};
			const dd = this.#reoDropdownTabs(menuItems, run, norm, ddCfg);
			if (dd) {
				return { kind: menuType, archetype: "reo_tabs", reoNav: dd.nav, reoPanes: dd.panes,
					tab1: "", tab2: "", content: "", left: "", right: "" };
			}
		}

		// WRITER-AUTHORED MENU TAB PARTITION (ROUND 221 — module ENGJ403, Chris).
		// The NEWEST Writers-Template era authors the overview menu's tab layout
		// EXPLICITLY: a "[please set up as two tabs …][tab 1 – please title as
		// appropriate]" set-up instruction, then the tab-1 sections, "[close tab]",
		// "[tab 2 – …]", the tab-2 sections, "[close tab]" — all BEFORE [MODULE
		// INTRODUCTION]. The human developer builds EXACTLY that partition (ENGJ403:
		// tab 1 = LI/SC + Planning/Get-started/Connections/Assessment in two
		// side-by-side columns under a "Tirohanga Whānui | Overview" banner; tab 2 =
		// Knowledge/Practices in two columns) — but the fold-vocabulary tab_map
		// routing below knows nothing about the markers, so it re-shuffled sections
		// into the wrong tabs and dropped the banner. When the markers are present,
		// honour the writer's own partition instead of the vocabulary routing.
		// MEASURED over ALL 428 corpus WTs (outputs/_measure_menutabtags.cjs): the
		// gate (a real [MODULE INTRODUCTION]-bounded menu region + the tabs SET-UP
		// instruction + >=1 [close tab]) fires on EXACTLY ENGJ403 today; CEDK101's
		// six bare [tab N] crumbs (no set-up, no closers — the inquiry crumb list,
		// already handled via _inquiryCrumb) decline BY CONSTRUCTION.
		// Data: menu.writer_tab_partition + menu.shells.writer_tabs.
		// Env toggle: MENUTABPART_OFF (falls back to the fold-routing walk below).
		{
			const wtCfg = tpl.writer_tab_partition;
			const wtOn = wtCfg && wtCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.MENUTABPART_OFF)
				&& menuType === "tabs" && page.isOverview;
			if (wtOn) {
				const wt = this.#writerTabPartition(menuItems, run, norm, wtCfg);
				if (wt) {
					run.AddNote("info", "MenuBuilder",
						`Overview menu composed from the writer's own [tab N]/[close tab] markers (${wt.count} tabs; menu.writer_tab_partition).`);
					return { kind: menuType, archetype: "writer_tabs", wtNav: wt.nav, wtPanes: wt.panes,
						tab1: "", tab2: "", content: "", left: "", right: "" };
				}
			}
		}

		// The menu's FORM (its archetype/layout) comes from the same specific-to-
		// general convention cascade used elsewhere in the converter: this exact
		// module's own series → its subject+phase group → a global default. The
		// aim is to never apply one blanket layout rule to every module in the
		// library — always prefer the most specific evidence available for THIS
		// particular module.
		const pageType = page.isOverview ? "overview" : "lesson";
		const convention = run.conventions?.menu?.[pageType] ?? null;
		const archetype = menuType === "tabs" ? "tabs"
			: (convention?.archetype === "two_col_li" ? "two_col_li" : "flat");

		// THE "ENG FAMILY" OFFSET TWO-COLUMN LAYOUT (convention banner_h4_span:false):
		// subjects like ENG*/MX*/ANZH/... render this menu with NO banner header,
		// using 'col-md-6 offset-md-0 col-12' Bootstrap columns; a curriculum line
		// written as '**Label:** prose' gets SPLIT into a heading + a separate <p>;
		// a bilingual LI/SC heading is reduced down to its English half; italics
		// are stripped; and WALT/I-can lead-in lines are kept as plain <p>
		// paragraphs. Subject families that use a banner header instead
		// (convention banner_h4_span:true, e.g. the "BLL" family below) are
		// untouched by this branch. Data: Emit_Templates menu.two_col_li.eng_family.
		// Env MENUCURRIC_OFF reverts this whole ENG-family layout back to the plain
		// BLL-shaped output.
		const engCfg = tpl.two_col_li?.eng_family;
		const engSubject = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const engFamily = archetype === "two_col_li"
			&& engCfg && engCfg.enabled !== false
			&& convention?.banner_h4_span === false
			&& (!engCfg.subjects || engCfg.subjects.includes(engSubject))
			&& !(typeof process !== "undefined" && process.env && process.env.MENUCURRIC_OFF);
		// THE "BANNER" FAMILY (convention banner_h4_span:true — a different family
		// than eng_family above, e.g. module BLL211 and its siblings): reuses most
		// of the same overview transforms as the ENG family — reduce a bilingual
		// LI/SC heading to its English half, strip italics on both panes, keep
		// WALT/I-can lines as <p> lead-ins — but ALSO sources the top banner text
		// from the module's actual [H1] heading (reduced to English) instead of a
		// hardcoded literal banner string. Data: menu.two_col_li.banner_family.
		// Env BANNERMENU_OFF disables this family layout.
		const bannerCfg = tpl.two_col_li?.banner_family;
		const bannerFamily = archetype === "two_col_li"
			&& !engFamily
			&& bannerCfg && bannerCfg.enabled !== false
			&& convention?.banner_h4_span === true
			&& !(typeof process !== "undefined" && process.env && process.env.BANNERMENU_OFF);
		// THE CURRICULUM-LINE SPLIT, GENERALISED TO EVERY OTHER two_col_li FAMILY
		// (the banner family plus subjects like CEDO/CEDT/XGF that aren't part of
		// the ENG family above): without this, a curriculum line written as
		// '**Label:** prose' gets absorbed whole into the heading, producing a
		// heading with no separate content underneath it — which
		// dropEmptyHeadings() then deletes outright, leaving an EMPTY left column
		// where the Understand/Know/Do heading should be. This mirrors the
		// ENG-family split above, just applied to every other two_col_li family
		// too. Data: menu.two_col_li.curriculum_split_all.
		// Env CURRICSPLIT_OFF disables it.
		const curricSplit = archetype === "two_col_li" && !engFamily
			&& tpl.two_col_li.curriculum_split_all !== false
			&& !(typeof process !== "undefined" && process.env && process.env.CURRICSPLIT_OFF);

		const out = { kind: menuType, archetype, engFamily, bannerFamily, bannerLabel: "", tab1: "", tab2: "", content: "", left: "", right: "", tab1Cols: null, tab2Cols: null };

		// OVERVIEW TABS-MENU PANE-1 TWO-COLUMN LAYOUT (e.g. module ENGJ402). The
		// two-column transforms above are all gated to archetype === "two_col_li",
		// so none of them ran inside a "tabs" shell — pane 1 of a tabs menu used to
		// just accumulate everything into ONE long column, when the human-built
		// version actually splits it into TWO columns. When this flag is on, tab-1
		// content is ALSO recorded as a sequence of kind-tagged "runs" (curric / li
		// / sc / lead / other — one run per heading plus the content that follows
		// it); #tabsPane1Partition then composes those runs into the correct
		// two-column form afterwards, using a registry of known column layouts.
		// Data: menu.tabs_pane1_two_col. Env TABTWOCOL_OFF disables this and falls
		// back to the single accumulated column.
		const t1cfgRaw = tpl.tabs_pane1_two_col;
		const t1cfg = archetype === "tabs" && t1cfgRaw && t1cfgRaw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.TABTWOCOL_OFF)
			? t1cfgRaw : null;
		const t1Runs = [];
		let t1SkipPiece = false;

		// INFORMATION-PANE NATIVE TWO-COLUMN (round 211, Chris — the AGH1002
		// screenshot). The human lays some groups' Information/Learning pane out
		// in TWO columns (AGH1002: LI + SC + year-planner LEFT | Planning your
		// time + get-started RIGHT) where this builder dumped everything into ONE
		// col-md-8. Measured across all 186 gold tabs-overviews
		// (outputs/_measure_tab2_cols.py): the column count is a per-
		// subject|phase house style whose within-group discriminator is LI/SC
		// PRESENCE in the pane (AGH li-carrying golds 2-col 3/3, li-less 0/6;
		// MXEO's li-carrying Learning panes stay ONE col 0/3 — hence registry-
		// gated, never a global rule). Tab-2 content is recorded here as
		// kind-tagged RUNS (the t1Runs pattern) so the composer below
		// (menu.tab2_cols) can split them into the group's registered column
		// pair. Env INFOCOLS_OFF disables (single accumulated column).
		const t2cfgRaw = tpl.tab2_cols;
		const t2cfg = archetype === "tabs" && page.isOverview
			&& t2cfgRaw && t2cfgRaw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.INFOCOLS_OFF)
			&& !this.isReoModule(run) ? t2cfgRaw : null;
		const t2Runs = [];

		// EXTRA MODULE-MENU TABS (module AGH1001's "[Module menu tab rules]"
		// screenshot). The human-built pages promote SOME overview-menu sections
		// to their OWN nav tabs — AGH1001 ships FOUR tabs (Overview | Information
		// | Connections | Assessment for Learning) where this builder's two-tab
		// shell used to dump the Connections + Assessment sections into the
		// Information pane as <h5> subsections. Which sections promote, and what
		// the tab is CALLED, is a per-subject-group house style mined from the
		// human library into menu.extra_tabs.registry (e.g. most NCEA subjects
		// call the assessment tab "Standards" — a word that never appears in the
		// Writers Template). When a tab2-routed heading matches a registered
		// section for this module's group, the walk below opens a NEW pane and
		// the section's content flows into it instead of tab 2.
		// Data: menu.extra_tabs. Env EXTRATABS_OFF disables (sections stay in
		// the Information pane exactly as before).
		const xtRaw = tpl.extra_tabs;
		const xtCfg = archetype === "tabs" && page.isOverview
			&& xtRaw && xtRaw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.EXTRATABS_OFF)
			&& !this.isReoModule(run) ? xtRaw : null;
		const xtRow = xtCfg ? this.#extraTabRow(run, xtCfg) : null;
		out.extraTabs = null;

		// GENERAL BILINGUAL MENU-HEADING REDUCE (the r206 follow-up). The writer
		// types menu subsection headings bilingually ("Whakamaheretia tō wā |
		// Planning your time") and this builder shipped the pipe intact, while
		// most human-built menus keep only the ENGLISH half. Measured across the
		// whole library (outputs/_measure_menuh5_reo.py): 251 of 316 decided
		// piped headings reduce, and the choice is a per-subject-group house
		// style (most groups reduce at 1.00; a coherent KEEP family — the
		// OSAH/OSOH/OSSC "Online @ home" subjects and a few others — keeps the
		// full bilingual form). Registry-gated per subject|phase group via the
		// SAME #extraTabRow lookup shape as extra_tabs, applied at RENDER only
		// (the tab_map heading fill below + the simplified <h5>) — never to the
		// routing fold (the tab vocabulary carries both languages) and never in
		// a reo module. Data menu.bilingual_heading_reduce; env MENUH5REO_OFF.
		const bhrRaw = tpl.bilingual_heading_reduce;
		const bhr = !!(bhrRaw && bhrRaw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.MENUH5REO_OFF)
			&& !this.isReoModule(run)
			&& this.#extraTabRow(run, bhrRaw));

		// walk: heading tag → bucket decision; following content joins it
		let bucket = archetype === "tabs" ? "tab1"
			: (archetype === "two_col_li" ? "right" : "content");
		const push = (html) => {
			// content routed to a PROMOTED extra tab (see extra_tabs above) —
			// it accumulates on that tab's own html, not on a core pane
			if (bucket.startsWith("extra:")) {
				const t = out.extraTabs[+bucket.slice(6)];
				t.html += (t.html ? "\n" : "") + html;
				return;
			}
			if (t1cfg && bucket === "tab1" && !t1SkipPiece) {
				if (!t1Runs.length) t1Runs.push({ kind: "lead", headingText: null, headHtml: null, pieces: [] });
				t1Runs[t1Runs.length - 1].pieces.push(html);
			}
			// mirror capture for the NATIVE tab-2 content (menu.tab2_cols): every
			// piece routed to tab 2 also lands on the current tab-2 run, so the
			// pane can be re-composed into columns after the walk. out.tab2 keeps
			// accumulating in parallel — it stays the single-column fallback.
			if (t2cfg && bucket === "tab2") {
				if (!t2Runs.length) t2Runs.push({ kind: "lead", pieces: [] });
				t2Runs[t2Runs.length - 1].pieces.push(html);
			}
			out[bucket] += (out[bucket] ? "\n" : "") + html;
		};

		// BUFFER consecutive "black" (plain-text, non-tag) content so consecutive
		// bullet lines GROUP into ONE <ul> instead of many separate ones. Menu items
		// are partitioned out of the page BEFORE ListsAndRuns.coalesceBlackRuns runs
		// (the pass that would normally merge adjacent plain-text runs together), so
		// each bullet line arrives here as its own separate item (and two_col_li
		// renders content per-LINE too). Without this buffer, calling
		// ListsAndRuns.renderBlackText() once per item/line would emit a separate
		// one-<li> <ul> for every bullet, with visible gaps between them — but the
		// human-built pages group these into a single list (e.g. a module's
		// Knowledge / Practices / Learning Intentions / Success Criteria items all
		// rendering as one <ul>). This mirrors the same buffer-then-flush pattern
		// used elsewhere in the converter for activity lead-in text. flushText()
		// renders the buffered run as ONE block into whichever bucket (column) is
		// CURRENT — it's still paragraph-safe, because
		// ListsAndRuns.renderBlackText() re-splits on newlines internally, so
		// non-bullet paragraphs still come out as separate <p> tags rather than
		// being merged together. It's called right before any heading, table,
		// bucket switch, or consumed label, and once more at the very end.
		let textBuf = [];
		const flushText = () => {
			if (!textBuf.length) return;
			for (const piece of ListsAndRuns.renderBlackText(textBuf.join("\n"), run)) push(piece);
			textBuf = [];
		};

		// The pane/section LABEL heading itself (e.g. "Learning Intentions") is
		// consumed — never re-rendered as its own item — in EVERY archetype: the
		// human-built pages never repeat this label as visible content, since it's
		// already implied by the column/tab it's sitting in.
		const isLabel = (folded) => (tpl.tab_map.consume_labels ?? []).some((l) =>
			folded === l || l.includes(folded) || folded.includes(l));

		// OVERVIEW BANNER precondition (e.g. module OSAH401). The overview page's
		// [H1] section label is kept as an <h4> "banner" heading ONLY when the
		// overview does NOT also contain an Understand/Know/Do curriculum block,
		// and only for a specific set of subjects (OSAH/OSOH/OSSC) verified against
		// the human-built pages. If a U/K/D block IS present, the human instead used
		// the two-column curriculum layout, so no separate banner is needed. This
		// scan runs once, up front, to decide which case applies.
		const ovbCfg = tpl.overview_banner_h4;
		const ovbSubject = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const ovbCurric = (ovbCfg?.curriculum_labels ?? ["understand", "know", "do"]);
		const hasCurriculumBlock = menuItems.some((it) => {
			let txt = "";
			if (it.type === "black") txt = it.text || "";
			else if (it.type === "tag" && it.parse?.primary
				&& ["h1", "h2", "h3", "h4", "h5", "heading"].includes(it.parse.primary.tag))
				txt = (norm.RenderText(it.text) || it.blackAfter || "");
			else return false;
			return txt.split(/\n+/).some((ln) => {
				const f = Utils.Fold(ln.replace(/\*/g, "").replace(/[:|].*$/, "").trim());
				return ovbCurric.some((c) => f === c);
			});
		});
		const ovbEnabled = ovbCfg && ovbCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.OVBANNER_OFF)
			&& page.isOverview && !hasCurriculumBlock
			&& (ovbCfg.subjects ?? []).includes(ovbSubject);

		for (const it of menuItems) {
			// INQUIRY-TEMPLATE "CED" PAGE-SPLIT crumb list: PanelsBuilder.detectInquiryCed()
			// scans the whole page for a `[Tab N]` crumb list and flags each entry it
			// finds with `_inquiryCrumb`. That crumb list can land inside the menu's
			// own captured item range (e.g. module CEDK101, where the list sits
			// before the [Module Introduction] marker) — so it must be suppressed
			// here too, or its labels would leak out as stray menu <p> paragraphs
			// instead of staying exclusively in the crumb navigation bar
			// PanelsBuilder builds.
			if (it._inquiryCrumb) continue;
			if (it.type === "black") {
				// two_col_li: writers mark the module LI/SC labels as BOLD
				// lines (**Whāinga Ako | Learning Intentions**) rather than
				// [H] tags — a standalone bold line matching the routing
				// lists switches the column and becomes its heading, using
				// the ENGLISH half of a piped reo|english label (the human
				// BLL155-0.0 right column shows plain-English h5s)
				if (archetype === "two_col_li") {
					const cfg = tpl.two_col_li;
					for (const line of it.text.split(/\n+/)) {
						const bold = line.trim().match(/^\*\*(.+?)\*\*:?$/);
						if (bold) {
							const label = bold[1].includes("|")
								? bold[1].split("|").pop().trim() : bold[1].trim();
							const folded = Utils.Fold(label);
							if (isLabel(folded)) continue;   // section label → consumed
							const left = cfg.left_match.some((m) => folded.startsWith(m));
							const right = (cfg.right_match ?? []).some((m) => folded.includes(m));
							if (left || right) {
								flushText();   // emit the prior bucket's buffered bullets before switching column
								bucket = left ? "left" : "right";
								push(Utils.FillTemplate(
									left ? cfg.left_heading : cfg.right_heading,
									{ heading: Utils.EscapeHtml(label) }));
								continue;
							}
						}
						if (line.trim()) textBuf.push(line);   // buffer (grouped at the next label / heading / end)
					}
					continue;
				}
				if (it.text.trim()) textBuf.push(it.text);   // buffer (grouped at the next heading / table / end)
				continue;
			}
			if (it.type === "table") { flushText(); push(TablesAndGrids.contentTable(it.block, run, false, norm)); continue; }

			const primary = it.parse.primary;
			const headingText = (norm.RenderText(it.text) || it.blackAfter)
				.replace(/\*/g, "").trim();

			if (primary && ["h1", "h2", "h3", "h4", "h5", "heading"].includes(primary.tag) && headingText) {
				flushText();   // a heading ends the current list run → flush buffered bullets first
				const folded = Utils.Fold(headingText);
				if (isLabel(folded)) {
					// The BANNER family sources its top banner text from this very [H1]
					// section label (reduced to English if it's bilingual), instead of
					// using a hardcoded literal string. GUARD: only accept a SHORT title
					// (at most banner_max_words words). A longer "Overview: <intro prose>"
					// style [H1] (seen on module CEDK101 and other Inquiry-template banner
					// modules) is NOT actually a short banner title, so we bail out and
					// fall back to the hardcoded default banner text instead of dumping a
					// whole paragraph of prose into the banner.
					if (bannerFamily && bannerCfg.banner_from_h1 && !out.bannerLabel) {
						const lbl = (headingText.includes("|")
							? headingText.split("|").pop() : headingText).trim();
						const maxW = bannerCfg.banner_max_words ?? 5;
						if (lbl && lbl.split(/\s+/).length <= maxW) out.bannerLabel = lbl;
					}
					// OVERVIEW BANNER emit: keep the overview page's [H1] section label as
					// an <h4><span> "banner" heading at the top of tab 1, instead of
					// dropping it entirely. `ovbEnabled` already confirmed we're on an
					// overview page, in one of the measured banner subjects, with no
					// curriculum block — this is a DIFFERENT code path than the
					// banner-family case just above (which re-homes the label into
					// `bannerLabel` rather than rendering it here).
					if (ovbEnabled && !bannerFamily && !engFamily) {
						push(Utils.FillTemplate(ovbCfg.element ?? "<h4><span>{heading}</span></h4>",
							{ heading: Utils.EscapeHtml(headingText) }));
						run.AddNote("info", "MenuBuilder",
							`Overview [H1] "${headingText}" kept as the tab-1 <h4> banner (overview_banner_h4).`);
						continue;
					}
					run.AddNote("info", "MenuBuilder",
						`Menu heading "${headingText}" is the section label — consumed (the menu scaffolding names it).`);
					continue;
				}

				if (archetype === "tabs") {
					// THE ONE-LINE "**Title:** content" SPLIT (e.g. module ENGR202). In an
					// OVERVIEW tabs pane, a curriculum heading whose CONTENT shares the same
					// line as its bold title ([H2] **Understand:** <prose>) used to render
					// as ONE content-glued heading, which dropEmptyHeadings() then deleted
					// outright whenever the next line was another heading (the same failure
					// mode fixed above for the two_col_li layout, but this is the "tabs"
					// layout's own copy of that bug). #splitTitleContent splits the bold
					// TITLE away from the non-bold CONTENT (title -> heading, content -> a
					// following <p>) so the heading is NEVER dropped; it returns null
					// (meaning KEEP WHOLE, unchanged) for a bilingual / ambiguous / no-clear-
					// boundary line. `hFold` (the folded text used for tab routing below)
					// is based on the TITLE only, not the content prose — so a body mention
					// of a word like "connections" or "assessment" inside the content can't
					// accidentally mis-route the whole heading into the wrong tab.
					const split = page.isOverview ? this.#splitTitleContent(it, headingText, run) : null;
					const hText = split ? split.label : headingText;
					const hFold = split ? Utils.Fold(hText) : folded;
					// SPECIFICITY routing (data tab_map.longest_match; env TABROUTE_OFF): the
					// tab whose matched vocabulary entry is LONGEST wins. The simpler rule
					// this replaced — "tab 2 wins whenever tab 2 matches and tab 1 doesn't" —
					// could strand a heading in tab 1 just because it happened to contain a
					// short, generic tab-1 word: "What DO I need to get started?" contains
					// the word "do", so the whole get-started section never reached tab 2
					// even though tab 2's own much longer, more specific phrase matched
					// exactly (the human-built pages put this content in tab 2 across many
					// modules).
					const longest = tpl.tab_map.longest_match !== false
						&& !(typeof process !== "undefined" && process.env && process.env.TABROUTE_OFF);
					const s1 = tpl.tab_map.tab1.match.reduce((a, m) => hFold.includes(m) && m.length > a ? m.length : a, 0);
					const s2 = tpl.tab_map.tab2.match.reduce((a, m) => hFold.includes(m) && m.length > a ? m.length : a, 0);
					const inTab1 = s1 > 0, inTab2 = s2 > 0;
					bucket = longest ? (s2 > s1 ? "tab2" : "tab1")
						: (inTab2 && !inTab1 ? "tab2" : "tab1");
					// PROMOTE TO AN OWN TAB (see extra_tabs above): a tab2-routed
					// section heading that matches a REGISTERED section for this
					// module's group opens a NEW nav tab + pane; the section's
					// following content flows into that pane via push(). The pane
					// keeps the section heading as an ENGLISH-reduced <h5> when the
					// section's keep_heading says so (the assessment pane does — 66
					// of 85 human golds; the connections pane drops it — the nav
					// label already names it). Tabs appear in document order.
					// ROUND 263 (curriculum tabs — module SCCH302; data
					// menu.extra_tabs.curriculum_tabs; env XTABCURRIC_OFF): a section
					// whose sections entry carries any_bucket:true (Knowledge /
					// Practices — the SCCH form, whose built sibling SCCH301 ships
					// them as their own nav tabs) is checked for promotion from ANY
					// routed bucket — the r238 tab_map routes those headings to tab 1,
					// where the original tab2-only check could never see them. A
					// section without the key keeps the exact tab2-only behaviour, so
					// every previously-registered group is untouched BY CONSTRUCTION.
					// A sections entry may also carry its OWN heading_element (the
					// SCCH panes keep an <h4><span> heading; the r206 assessment
					// default stays <h5>).
					const curricOn = xtCfg && xtCfg.curriculum_tabs?.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env.XTABCURRIC_OFF);
					if (xtRow) {
						const sec = this.#extraTabSection(hFold, xtCfg);
						if (sec && xtRow[sec]
							&& (bucket === "tab2" || (curricOn && xtCfg.sections?.[sec]?.any_bucket))) {
							if (!out.extraTabs) out.extraTabs = [];
							out.extraTabs.push({ label: xtRow[sec], html: "" });
							bucket = "extra:" + (out.extraTabs.length - 1);
							if (xtCfg.sections[sec]?.keep_heading !== false) {
								const engl = (hText.includes("|") ? hText.split("|").pop() : hText).trim();
								push(Utils.FillTemplate(
									(curricOn && xtCfg.sections?.[sec]?.heading_element)
										? xtCfg.sections[sec].heading_element
										: (xtCfg.heading_element ?? "<h5>{heading}</h5>"),
									{ heading: Utils.EscapeHtml(engl) }));
							}
							if (split) for (const p of split.pieces) push(p);
							run.AddNote("info", "MenuBuilder",
								`Menu section "${hText}" promoted to its own "${xtRow[sec]}" nav tab (menu.extra_tabs registry).`);
							continue;
						}
					}
					if (!inTab1 && !inTab2) {
						// surfaced, never absorbed: unknown menu heading
						push(NotesAndComments.redFlag(
							`Menu heading "${hText}" matched no tab rule (Emit_Templates menu.tab_map) — placed in tab 1.`, run));
					}
					const hEl = Utils.FillTemplate(tpl.tab_map[bucket].element,
						{ heading: Utils.EscapeHtml(this.#reduceBilingualHeading(hText, bhr)) });
					if (t1cfg && bucket === "tab1") {
						// start a kind-tagged run; the heading html is held OUT of pieces so
						// #tabsPane1Partition can re-level/transform it at compose time. When the split
						// fired, the heading is the TITLE and the content rides as the run's following
						// pieces (pushed into the run + out.tab1).
						t1Runs.push({ kind: this.#tabHeadKind(hFold, t1cfg), headingText: hText, headHtml: hEl, pieces: [] });
						t1SkipPiece = true; push(hEl); t1SkipPiece = false;
						if (split) for (const p of split.pieces) push(p);
					} else {
						// a tab-2-routed heading starts a NEW kind-tagged tab-2 run
						// (menu.tab2_cols): the heading html itself becomes the run's
						// first piece via push(); the kind vocabulary is shared with
						// pane 1 (tabs_pane1_two_col li_match/sc_match).
						if (t2cfg && bucket === "tab2") {
							t2Runs.push({ kind: this.#tabHeadKind(hFold, t2cfgRaw.li_match
								? t2cfgRaw : (t1cfgRaw ?? {})), pieces: [] });
						}
						push(hEl);
						if (split) for (const p of split.pieces) push(p);   // content after the heading (tab 2 / no partition)
					}
								} else if (archetype === "two_col_li") {
					// the Blended-Literacy two-column form: curriculum
					// Understand/Know/Do LEFT (h5+span), module LI/SC RIGHT
					// (h5 plain) — routing lists in Emit_Templates two_col_li
					const cfg = tpl.two_col_li;
					if (engFamily) {
						// Curriculum content goes LEFT (and gets split, see below);
						// everything else (LI/WALT/WILF/SC/I-can) goes RIGHT — this matches
						// the convention seen across the human-built library, where the
						// Learning Intentions sit on the right alongside "What I'm Looking
						// For" (WILF) content.
						const isCurric = (engCfg.curriculum_match ?? cfg.left_match).some((m) => folded.startsWith(m));
						if (isCurric) {
							// CURRICULUM split: '**Label:** prose' → the label heading (colon
							// dropped) + the prose as a following <p>. When the writer put the
							// prose in a SEPARATE paragraph (rest empty) the next black item
							// supplies the <p>. Fixes ENGC102's dropped Understand/Know/Do
							// (three text-absorbed headings nuked by #dropEmptyHeadings).
							bucket = "left";
							const raw = (it.blackAfter && it.blackAfter.trim()) ? it.blackAfter : headingText;
							const mb = raw.match(/^\s*\*\*([^*]+?)\*\*\s*([\s\S]*)$/);
							let label, rest = "";
							if (mb) { label = mb[1].replace(/:\s*$/, "").trim(); rest = mb[2]; }
							else {
								const ci = headingText.indexOf(":");
								if (ci >= 0 && headingText.slice(ci + 1).trim()) {
									label = headingText.slice(0, ci).trim(); rest = headingText.slice(ci + 1);
								} else { label = headingText.replace(/:\s*$/, "").trim(); }
							}
							push(Utils.FillTemplate(engCfg.curriculum_heading,
								{ level: this.curriculumLevel(run, engCfg), heading: Utils.EscapeHtml(label) }));
							if (rest && rest.replace(/[*\s]/g, "")) {
								for (const piece of ListsAndRuns.renderBlackText(rest.trim(), run)) push(piece);
							}
						} else {
							// LI / WALT / WILF / SC / I-can → RIGHT; h5 plain, bilingual reduced to English
							bucket = "right";
							const label = headingText.includes("|") ? headingText.split("|").pop().trim() : headingText;
							push(Utils.FillTemplate(engCfg.li_sc_heading, { heading: Utils.EscapeHtml(label) }));
						}
					} else {
						const isLeftCurric = cfg.left_match.some((m) => folded.startsWith(m));
						if (isLeftCurric && curricSplit) {
							// SPLIT '**Label:** prose' → the label heading (colon dropped) using
							// this family's OWN left_heading template, plus the prose as a
							// following <p> — so the heading is NOT left content-less (which
							// would otherwise get deleted by #dropEmptyHeadings, leaving an
							// EMPTY left column, as happened on module CEDO102's
							// Understand/Know/Do heading before this fix). This mirrors the
							// eng_family split above, just applied to every other two_col_li
							// family.
							bucket = "left";
							const raw = (it.blackAfter && it.blackAfter.trim()) ? it.blackAfter : headingText;
							const mb = raw.match(/^\s*\*\*([^*]+?)\*\*\s*([\s\S]*)$/);
							let label, rest = "";
							if (mb) { label = mb[1].replace(/:\s*$/, "").trim(); rest = mb[2]; }
							else {
								const ci = headingText.indexOf(":");
								if (ci >= 0 && headingText.slice(ci + 1).trim()) {
									label = headingText.slice(0, ci).trim(); rest = headingText.slice(ci + 1);
								} else { label = headingText.replace(/:\s*$/, "").trim(); }
							}
							push(Utils.FillTemplate(cfg.left_heading, { heading: Utils.EscapeHtml(label) }));
							if (rest && rest.replace(/[*\s]/g, "")) {
								for (const piece of ListsAndRuns.renderBlackText(rest.trim(), run)) push(piece);
							}
						} else {
							bucket = isLeftCurric ? "left" : "right";
							// The BANNER family "bilingual reduces" a piped 'reo | english'
							// RIGHT-column LI/SC heading down to just its English half (i.e.
							// drops the Māori half and keeps only the text after the "|").
							// The GENERAL registry-gated reduce (bhr, see the flag above)
							// covers the same RIGHT-column emit for every registered
							// non-banner group too (e.g. the MXFL family, whose two_col_li
							// menus shipped "Whāinga Ako | Learning Intentions" piped where
							// the human keeps only the English half) — right bucket only:
							// the measured piped population is entirely LI/SC/planning
							// (right); the human KEEPS piped left-column curriculum strands
							// where they occur (MXFL202 gold), so the left column is never
							// touched.
							const htext = (((bannerFamily && bannerCfg.reduce_bilingual) || bhr)
								&& bucket === "right" && headingText.includes("|"))
								? headingText.split("|").pop().trim() : headingText;
							push(Utils.FillTemplate(
								bucket === "left" ? cfg.left_heading : cfg.right_heading,
								{ heading: Utils.EscapeHtml(htext) }));
						}
					}
				} else {
					push(`<h5>${Utils.EscapeHtml(this.#reduceBilingualHeading(headingText, bhr))}</h5>`);
				}
				continue;
			}

			// instruction spans inside the menu still flag visibly
			if (!primary && it.parse.class === "instruction") {
				flushText();
				push(NotesAndComments.redFlag(it.text, run, "cs"));
				if (it.blackAfter.trim()) textBuf.push(it.blackAfter);
				continue;
			}

			// anything else: render its black content in place
			const text = it.blackAfter ?? "";
			if (text.trim()) textBuf.push(text);
		}
		flushText();   // emit any trailing buffered bullets

		// Compose the pane-1 registry columns from the kind-tagged runs recorded
		// above (overview tabs menus only). This DECLINES — leaving out.tab1Cols
		// null, i.e. falling back to the plain single-column pane built above — in
		// several cases: no matching registry row, a "single"-column row, a reo
		// (bilingual) module, missing required run kinds, or an empty non-band
		// column that would otherwise ship blank.
		let liscMoved = false;
		let movedRuns = [];   // the moved LI/SC as STRUCTURED runs (menu.tab2_cols)
		if (t1cfg && t1Runs.length) {
			const res = this.#tabsPane1Partition(t1Runs, run, page, t1cfg);
			if (res) {
				out.tab1Cols = res.cols;
				movedRuns = res.t2movedRuns ?? [];
				// The moved LI/SC content renders as a TWO-COLUMN tab-2 when there is
				// no native tab-2 content it would need to interleave with; otherwise
				// it's prepended as a flat block onto whatever tab-2 already has.
				if (res.tab2Cols && !(out.tab2 && out.tab2.trim())) {
					out.tab2Cols = res.tab2Cols;
					liscMoved = true;
				} else if (res.tab2Prepend) {
					out.tab2 = res.tab2Prepend + (out.tab2 ? "\n" + out.tab2 : "");
					liscMoved = true;
				}
			}
		}

		// THE "LEARNING" SECOND TAB (the MXEO/ENGS102 family). These modules'
		// human-built overviews name the SECOND tab "Learning" and home the
		// Learning-Intentions / Success-Criteria content there — tab 1 keeps
		// only the Understand/Know/Do curriculum. Measured corpus-wide
		// (outputs/_measure_learningtab.py): the two-tab Overview|Learning form
		// is EXACTLY ENGS102 + all four MXEO gold tabs-overviews (both phase
		// groups, zero counter-examples); SSOG301's four-tab Learning INSERT is
		// a one-module form (recorded C, no registry row). The golds also
		// DELETE the writer's planning/connections/assessment sections — that
		// deletion has no WT discriminator (byte-similar sections are KEPT by
		// other subjects' golds), so the writer's info content is RETAINED
		// below the moved LI/SC (recorded residual). When the r166 partition
		// already moved the LI/SC to tab 2 (ENGS102's curric_split) only the
		// label changes; otherwise the LI/SC runs are extracted from pane 1
		// here, re-emitted at the r166 row's li_level (the gold-matched <h5>).
		// ALL-OR-NOTHING per module: if the LI/SC cannot be cleanly moved
		// (e.g. pane 1 would be left with nothing), neither the move nor the
		// label ships. Data menu.learning_tab; env LEARNTAB_OFF.
		const ltRaw = tpl.learning_tab;
		const ltRow = archetype === "tabs" && page.isOverview
			&& ltRaw && ltRaw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.LEARNTAB_OFF)
			&& !this.isReoModule(run) ? this.#extraTabRow(run, ltRaw) : null;
		if (ltRow) {
			let ok = liscMoved;
			if (!ok && !out.tab1Cols
				&& t1Runs.some((r) => (r.kind === "li" || r.kind === "sc") && (r.headHtml || r.pieces.length))) {
				const p1row = this.#extraTabRow(run, t1cfgRaw ?? {}) ?? {};
				const kept = [], moved = [];
				for (const r of t1Runs) {
					if (r.kind === "li" || r.kind === "sc") {
						moved.push(this.#tabsPane1HeadHtml(r, p1row, t1cfgRaw ?? {}, run), ...r.pieces);
					} else {
						if (r.headHtml) kept.push(r.headHtml);
						kept.push(...r.pieces);
					}
				}
				const keptHtml = kept.join("\n"), movedHtml = moved.join("\n");
				if (keptHtml.trim() && movedHtml.trim()) {
					out.tab1 = keptHtml;
					out.tab2 = movedHtml + (out.tab2 && out.tab2.trim() ? "\n" + out.tab2 : "");
					ok = true;
				}
			}
			if (ok) {
				out.tab2Label = ltRaw.label ?? "Learning";
				run.AddNote("info", "MenuBuilder",
					`Second menu tab labelled "${out.tab2Label}" with the LI/SC content homed there (menu.learning_tab registry).`);
			}
		}

		// INFORMATION-PANE NATIVE TWO-COLUMN compose (menu.tab2_cols — see the
		// t2cfg declaration above for the measurement). Runs LAST of the tab-2
		// shapers, and only when nothing already composed columns (the r172
		// moved-LI/SC two-col path and the r209 learning-tab path win first —
		// their groups are not registered here anyway). Rebuilds the pane from
		// the moved LI/SC runs + the native kind-tagged tab-2 runs:
		//   1. adjacent li/li (or sc/sc) runs MERGE into one section group — an
		//      LI heading and its "We are learning to:" lead h5 are ONE section;
		//      a leading un-headed run rides the first headed group;
		//   2. kind "li_sc"  → the leading LI-family groups go LEFT, everything
		//      else RIGHT (the MX* families, whose golds ship [li]|[sc]);
		//      kind "balance" → the first ceil(G/2) groups go LEFT (AGH/ANZH/
		//      HIS/CEDO/ENGR/MXFU — the exact split point is editorial within
		//      AGH, whose three golds cut 4|1, 3|2 and 1|3; the grouped balance
		//      is the general form and matches the family arrangement).
		// FIRES only when the pane holds >=1 li/sc-family group (the measured
		// within-group discriminator — AGH's li-less panes stay one column) and
		// >=2 groups total, and both columns end up non-empty.
		if (t2cfg && !out.tab2Cols) {
			const row = this.#extraTabRow(run, t2cfg);
			if (row && Array.isArray(row.cols) && row.cols.length === 2) {
				const items = [];
				for (const m of movedRuns) if (m.html.trim()) items.push({ kind: m.kind, html: m.html });
				for (const r of t2Runs) {
					const h = r.pieces.join("\n");
					if (h.trim()) items.push({ kind: r.kind, html: h });
				}
				const groups = [];
				for (const it of items) {
					const last = groups[groups.length - 1];
					if (last && last.kind === it.kind && (it.kind === "li" || it.kind === "sc")) {
						last.html += "\n" + it.html;
					} else if (last && last.kind === "lead" && groups.length === 1) {
						last.html += "\n" + it.html; last.kind = it.kind;
					} else {
						groups.push({ kind: it.kind, html: it.html });
					}
				}
				const liGroups = groups.filter((g) => g.kind === "li" || g.kind === "sc").length;
				if (groups.length >= 2 && liGroups >= 1) {
					let L, R;
					if (row.kind === "li_sc") {
						let i = 0;
						while (i < groups.length && groups[i].kind === "li") i++;
						L = groups.slice(0, i); R = groups.slice(i);
					} else {
						const cut = Math.ceil(groups.length / 2);
						L = groups.slice(0, cut); R = groups.slice(cut);
					}
					const Lh = this.dropEmptyHeadings(L.map((g) => g.html).join("\n"), run);
					const Rh = this.dropEmptyHeadings(R.map((g) => g.html).join("\n"), run);
					if (Lh.trim() && Rh.trim()) {
						out.tab2Cols = [{ cls: row.cols[0], html: Lh }, { cls: row.cols[1], html: Rh }];
						run.AddNote("info", "MenuBuilder",
							`Information pane composed as the group's two-column form (menu.tab2_cols registry, kind "${row.kind ?? "balance"}").`);
					}
				}
			}
		}

		// Strip <i>/<em> tags from the ENG-family panes — the Writers Template
		// wraps curriculum prose and WALT/I-can lists in *italics*, but the
		// human-built menus never carry any; <b> (bold) markup is preserved.
		// The BANNER family gets the same both-pane strip.
		if ((engFamily && engCfg.strip_italics) || (bannerFamily && bannerCfg.strip_italics)) {
			for (const key of ["left", "right"]) {
				if (out[key]) out[key] = out[key].replace(/<\/?(?:i|em)>/gi, "");
			}
		}
		// Same italics strip applied to the recovered curriculum (LEFT pane) for
		// every OTHER two_col_li family too (not just ENG) — the human's
		// curriculum prose is plain there as well, even though the Writers
		// Template wraps it in *italics*.
		else if (curricSplit && out.left) {
			out.left = out.left.replace(/<\/?(?:i|em)>/gi, "");
		}
		// GENERAL MENU ITALIC STRIP. Measured across the whole human-built module
		// library (see outputs/_measure_italic_transfer.py): the human strips
		// <i>/<em> from module-menu items about 99% of the time — a clean rule
		// that holds specifically for the MENU region (compare: body/activity/
		// table content is only 43-66% stripped, which is editorial/inconsistent,
		// and acknowledgements content is 0% stripped/always kept — so this rule
		// is deliberately scoped to menus only). The family-specific strips above
		// only covered the ENG/banner curriculum PANES; this generalises the same
		// cleanup to EVERY pane in EVERY family. Text content is always preserved
		// — only the wrapper tags are removed. Font-Awesome icon markup
		// (<i class="fa...">) is never touched (no menu in the corpus uses icon
		// italics for anything else). EXCLUDES reo/bilingual modules (TRR/PNR
		// prefix, or reoTranslate body class) — there the human KEEPS italic
		// styling on BOTH panes (the Māori line AND its English translation).
		// Data: menu.strip_italic_all. Env MENUITALIC_OFF reverts to the older,
		// family-only strips above (ENG/banner panes only).
		if ((tpl.strip_italic_all ?? true) && !this.isReoModule(run)
			&& !(typeof process !== "undefined" && process.env && process.env.MENUITALIC_OFF)) {
			for (const key of ["tab1", "tab2", "content", "left", "right"]) {
				if (out[key]) out[key] = this.stripTextItalic(out[key]);
			}
			// The partitioned pane-1 columns get the same general italic strip too
			if (out.tab1Cols) for (const c of out.tab1Cols) c.html = this.stripTextItalic(c.html);
			if (out.tab2Cols) for (const c of out.tab2Cols) c.html = this.stripTextItalic(c.html);
			// ...and so do the promoted extra-tab panes
			if (out.extraTabs) for (const t of out.extraTabs) t.html = this.stripTextItalic(t.html);
		}

		// drop EMPTY preconfigured headings — a menu heading with no content
		// before the next heading/end is omitted (human devs almost never
		// keep one: 127 filled vs 3 empty for "What do I need to get started?";
		// menu_empty_heading_rule). Applies to every bucket/archetype.
		for (const key of ["tab1", "tab2", "content", "left", "right"]) {
			if (out[key]) out[key] = this.dropEmptyHeadings(out[key], run);
		}
		// Per-column empty-heading drop too (safe to run twice — running this same
		// check again after the partition step above is a no-op if it already ran)
		if (out.tab1Cols) for (const c of out.tab1Cols) c.html = this.dropEmptyHeadings(c.html, run);
		if (out.tab2Cols) for (const c of out.tab2Cols) c.html = this.dropEmptyHeadings(c.html, run);
		// A PROMOTED tab whose pane ended up with no real content (e.g. its
		// section was empty in the Writers Template, so only the optional <h5>
		// heading — which dropEmptyHeadings just removed — was ever pushed) is
		// dropped entirely: the human never ships an empty pane, and a nav tab
		// with a blank pane would look broken. Same discipline as the
		// never-ship-an-empty-column rule in #tabsPane1Partition.
		if (out.extraTabs) {
			for (const t of out.extraTabs) t.html = this.dropEmptyHeadings(t.html, run);
			out.extraTabs = out.extraTabs.filter((t) => t.html && t.html.trim());
			if (!out.extraTabs.length) out.extraTabs = null;
		}
		// ROUND 263 (curriculum tabs — module SCCH302; env XTABCURRIC_OFF): a
		// registry row carrying _drop_empty_tab2 drops the shell's Information
		// nav item + pane when every routed section promoted away and no tab-2
		// content remains — the built sibling SCCH301's gold nav is
		// Overview | Knowledge | Practices, with NO Information tab. ROW-scoped:
		// a group without the flag (every previously-registered group) keeps its
		// Information tab byte-identically through the {tab2Nav}/{tab2Pane}
		// shell slots' defaults in SkeletonBuilder.
		if (out.extraTabs && xtRow && xtRow._drop_empty_tab2
			&& xtCfg.curriculum_tabs?.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.XTABCURRIC_OFF)
			&& !(out.tab2 && out.tab2.trim())) {
			out.dropTab2 = true;
			run.AddNote("info", "MenuBuilder",
				"Empty Information tab dropped — every menu section promoted to its own tab (menu.extra_tabs registry, _drop_empty_tab2).");
		}
		// LESSON-MENU "Learning intentions" LABEL (ROUND 222 — module ENGJ403;
		// Chris's lesson-menu report). The human developers open a LESSON page's
		// simplified menu with a GENERATED "Learning intentions" label heading
		// (`<h5>Learning intentions</h5>` before the "We are learning:" lead) in
		// specific subject|phase families — the label is NOT in the Writers
		// Template (ENGJ403's lesson regions carry only the WALT/I-can lines),
		// so this is a registry-driven generated label, the round-187 funLi
		// class. MEASURED over every gold lesson-page menu (grouped by the
		// ENGINE-resolved subject|phase): rows generated where the group share
		// is ≥0.80 over ≥5 menus AND the lesson menu type is "simplified"
		// (ENGJ|4-6 is 45/45; the h3-form families MXDB/MXFUN/SSCI are recorded
		// follow-ups — their menus build through different machinery). GUARDS:
		// lesson pages only, non-empty composed menu, and never when the menu
		// already carries a "learning intention" heading (double-emission-safe
		// by construction, whatever path produced it).
		// Data: menu.lesson_li_label (registry + per-row element/label).
		// Env toggle: MENULILABEL_OFF.
		{
			const llCfg = tpl.lesson_li_label;
			const llOn = llCfg && llCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.MENULILABEL_OFF)
				&& !page.isOverview && out.content && out.content.trim();
			if (llOn) {
				// THE FIRST-IN-SERIES DEFAULT ROW (ROUND 238 — Dev-Feedback R1
				// Family A, module SCCH302). A brand-new subject has no gold-built
				// sibling on disk, so no MEASURED group row can ever exist for it —
				// but its lesson menu still needs the label the design team
				// confirmed for new subjects, in the MODERN form
				// <h4><span>Learning Intentions</span></h4>. The default row fires
				// ONLY when no measured registry row matched AND the resolver set
				// run.registryDefaultsApplied (the universal-field evidence floor's
				// first-in-series signal) — every module with real gold evidence is
				// untouched BY CONSTRUCTION. Data: menu.lesson_li_label.default_row.
				// Env toggle: MENUDEFAULT_OFF.
				const llDef = llCfg.default_row;
				const llDefOn = llDef && llDef.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.MENUDEFAULT_OFF)
					&& run.registryDefaultsApplied;
				const llRow = this.#extraTabRow(run, llCfg) ?? (llDefOn ? llDef : null);
				if (llRow && !Utils.Fold(out.content).includes("learning intention")) {
					out.content = Utils.FillTemplate(
						llRow.element ?? "<h5>{label}</h5>",
						{ label: Utils.EscapeHtml(llRow.label ?? "Learning intentions") })
						+ "\n" + out.content;
				}
			}
		}

		return out;
	};

	/**
	 * Resolves this module's EXTRA-TAB registry row (menu.extra_tabs.registry):
	 * the module's own series override → its subject|phase group (case-
	 * tolerant) — the same lookup shape #tabsPane1Partition uses for the
	 * pane-1 column registry, so the two registries can never key apart.
	 *
	 * @param {Object} run - the conversion run context
	 * @param {Object} cfg - the menu.extra_tabs config block
	 * @returns {Object|null} e.g. { assessment: "Standards", connections: "Connections" }
	 */
	static #extraTabRow(run, cfg) {
		const reg = cfg.registry ?? {};
		const subj = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const rawPhase = run.resolvedRules?.template_phase ?? "";
		const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
		let row = reg.series?.[run.moduleCode] ?? reg.groups?.[`${subj}|${phase}`];
		if (!row && reg.groups) {
			const lk = `${subj}|${phase}`.toLowerCase();
			const hit = Object.keys(reg.groups).find((k) => k.toLowerCase() === lk);
			if (hit) row = reg.groups[hit];
		}
		return row ?? null;
	}

	/**
	 * Reduces a bilingual "reo | English" menu heading to its ENGLISH (last
	 * pipe segment) half — the render-time half of the general bilingual
	 * menu-heading reduce (data menu.bilingual_heading_reduce; env
	 * MENUH5REO_OFF). Identity when the reduce is off for this module, the
	 * text carries no pipe, or the English half would be empty.
	 *
	 * @param {string} text - the heading text as routed
	 * @param {boolean} on - this module's resolved reduce flag
	 * @returns {string} the (possibly reduced) heading text
	 */
	static #reduceBilingualHeading(text, on) {
		if (!on || !text || !text.includes("|")) return text;
		const eng = text.split("|").pop().trim();
		return eng || text;
	}

	/**
	 * Which extra-tab SECTION (if any) a folded, tab2-routed menu heading
	 * belongs to — the section whose matched vocabulary phrase is LONGEST
	 * wins, the same specificity rule the tab_map routing itself uses (so a
	 * heading like "Assessment for Learning" resolves through its own full
	 * phrase, never through the bare "assessment" substring of some other
	 * section's vocabulary).
	 *
	 * @param {string} hFold - the case/diacritic-folded heading text
	 * @param {Object} cfg - the menu.extra_tabs config block
	 * @returns {string|null} a menu.extra_tabs.sections key, or null
	 */
	static #extraTabSection(hFold, cfg) {
		let best = null, len = 0;
		for (const [sec, def] of Object.entries(cfg.sections ?? {})) {
			for (const m of def.match ?? []) {
				if (m.length > len && hFold.includes(m)) { best = sec; len = m.length; }
			}
		}
		return best;
	}

	/**
	 * Classifies a tabs-menu heading into a "kind" used by the pane-1
	 * partition step below (#tabsPane1Partition): "curric" (a curriculum
	 * heading like Understand/Know/Do), "li" (Learning Intentions), "sc"
	 * (Success Criteria), or "other".
	 *
	 * HOW: the curriculum vocabulary is REUSED from two_col_li.left_match —
	 * the same list that routes the left column in the two-column menu
	 * families, never a separate parallel list. The li/sc vocabulary comes
	 * from the right_match refinement inside the tabs_pane1_two_col config
	 * (splitting "li" from "sc" is needed for the li_sc partition layout —
	 * see module CEDK501 for an example that uses it). The curriculum test
	 * matches at the WORD level against the English half of the heading: the
	 * label itself must equal or start with a known curriculum word like
	 * "do", not merely CONTAIN it as a substring — a heading like "what DO i
	 * need..." contains the letters "do" but is not a curriculum heading.
	 *
	 * @param {string} folded - the case/diacritic-folded heading text
	 * @param {Object} cfg - the tabs_pane1_two_col config block
	 * @returns {"curric"|"li"|"sc"|"other"}
	 */
	static #tabHeadKind(folded, cfg) {
		const curric = DataService.Data.EmitTemplates.menu.two_col_li?.left_match ?? [];
		const isCur = (s) => {
			const base = s.replace(/:\s*$/, "").trim();
			return curric.some((c) => base === c || base.startsWith(c + " ") || base.startsWith(c + ":"));
		};
		// Try the RAW text first — a heading whose own strand is "glued" together
		// with a pipe character (e.g. "know: mātauranga tau | number  in our..."
		// on module MXDI201) must not be mis-classified by popping off the wrong
		// half — then fall back to testing the English half of a reo|english
		// piped label (e.g. "whāinga ako | learning intentions").
		if (isCur(folded.trim())) return "curric";
		if (folded.includes("|") && isCur(folded.split("|").pop().trim())) return "curric";
		if ((cfg.li_match ?? []).some((k) => folded.includes(k))) return "li";
		if ((cfg.sc_match ?? []).some((k) => folded.includes(k))) return "sc";
		return "other";
	};

	/**
	 * Splits a one-line overview-menu heading whose bold TITLE and non-bold
	 * CONTENT share the same source line (e.g. "**Understand:** <some
	 * prose>") into { label, pieces } — so the bold part becomes the heading
	 * and the rest becomes a separate following <p> — instead of leaving one
	 * content-glued heading that #dropEmptyHeadings would delete outright as
	 * "empty".
	 *
	 * Returns null (meaning: KEEP WHOLE, don't split) unless ALL of these hold:
	 *   - there's a genuine bold-title -> non-bold-content boundary, with
	 *     REAL non-bold content after it (the primary signal a split is safe)
	 *   - it's NOT a bilingual title — no top-level '|' character, and the
	 *     trailing content isn't itself entirely bold (those are Te-Reo |
	 *     English dual-language titles, left to the bilingual-reduce logic
	 *     elsewhere in this file instead)
	 *   - we're CONFIDENT the bold run really is meant as a menu title:
	 *     either it ends with a colon (a secondary signal), OR its folded
	 *     form is a known overview-menu heading recorded in the corpus
	 *     lexicon at or above min_count (env MENUHEADINGLEX_OFF ignores this
	 *     lexicon check), OR it matches a known two_col_li.left_match
	 *     curriculum label (Understand/Know/Do)
	 *
	 * @param {Object} it - the menu item being processed
	 * @param {string} headingText - the (already tag-stripped) heading text
	 * @param {Object} run - the conversion run context
	 * @returns {{label: string, pieces: string[]}|null}
	 *
	 * Env TABCURRICSPLIT_OFF disables this split entirely (always returns
	 * null, so the heading and its glued content stay combined as one node).
	 */
	static #splitTitleContent(it, headingText, run) {
		const tpl = DataService.Data.EmitTemplates.menu;
		const cfg = tpl.tabs_pane1_curric_split;
		if (!cfg || cfg.enabled === false
			|| (typeof process !== "undefined" && process.env && process.env.TABCURRICSPLIT_OFF)) return null;
		// the RAW black text keeps the ** bold markers (headingText has them stripped)
		const raw = (it.blackAfter && it.blackAfter.trim()) ? it.blackAfter : headingText;
		if (raw.includes("|")) return null;                         // bilingual title — the reduce logic elsewhere handles this instead
		const mb = raw.match(/^\s*\*\*([^*]+?)\*\*\s*([\s\S]+)$/);   // bold TITLE then trailing content
		if (!mb) return null;
		// real NON-bold content after the title? (strip bold runs, pipes, asterisks, whitespace)
		if (mb[2].replace(/\*\*[^*]+?\*\*/g, "").replace(/[*|\s]/g, "") === "") return null;
		const rawLabel = mb[1].trim();
		const label = rawLabel.replace(/:\s*$/, "").trim();
		if (!label) return null;
		// CONFIDENCE: colon-terminated bold (secondary) OR a curriculum left_match OR a corpus
		// overview-menu heading (the lexicon database; MENUHEADINGLEX_OFF ignores it).
		const flabel = Utils.Fold(label);
		const hasColon = /:\s*$/.test(rawLabel);
		const left = (tpl.two_col_li?.left_match ?? []).some((mt) =>
			flabel === mt || flabel.startsWith(mt + " ") || flabel.startsWith(mt + ":"));
		const lex = DataService.Data.OverviewMenuHeadingLexicon;
		const inLex = lex && lex.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.MENUHEADINGLEX_OFF)
			&& lex.headings && (lex.headings[flabel] ?? 0) >= (lex.min_count ?? 3);
		if (!hasColon && !left && !inLex) return null;              // ambiguous -> keep whole (never dropped)
		const pieces = ListsAndRuns.renderBlackText(mb[2].trim(), run);
		return pieces.length ? { label, pieces } : null;
	};

	/**
	 * Builds the rendered heading HTML for one partitioned pane-1 "run" (see
	 * #tabsPane1Partition below): a "curric" run has its trailing colon
	 * stripped and renders using the registry's curric_level heading level
	 * (an <h4> with an inner <span>, by default); an "li"/"sc" run has its
	 * bilingual pipe reduced down to the English half and renders using the
	 * registry's li_level heading level (an <h5>, by default). A run of any
	 * OTHER kind — e.g. an English-first strand heading like "Measurement |
	 * Ine..." that the human keeps as-is rather than reducing — keeps its
	 * ORIGINAL heading element untouched.
	 *
	 * @param {Object} r - the run (kind, headingText, headHtml, pieces)
	 * @param {Object} row - the registry row for this module's column layout
	 * @param {Object} cfg - the tabs_pane1_two_col config block
	 * @param {Object} run - the conversion run context
	 * @returns {string} the heading's HTML
	 */
	static #tabsPane1HeadHtml(r, row, cfg, run) {
		if (r.kind === "curric") {
			let t = r.headingText, glued = "";
			if (cfg.strip_curric_colon !== false) t = t.replace(/:\s*$/, "").trim();
			// GLUE split (seen in the "MX" subject family): sometimes the writer runs
			// the whole strand's prose directly INTO the [H2] heading item itself
			// (e.g. "Know: Mātauranga tau | Number  In our number system..."), so the
			// heading arrives here as a whole paragraph's worth of text. Split
			// label|prose at the FIRST colon, but only when the remainder after the
			// colon is LONG (at least glue_split_min_words words, default 9) — a
			// SHORT remainder is a genuine strand subtitle that the human keeps
			// inside the heading itself (module ENGR302's "Know: ideas within,
			// across and beyond texts" stays whole, since splitting it would leave
			// an oddly short trailing paragraph).
			const ci = t.indexOf(":");
			if (ci > 0 && ci < 24) {
				const rest = t.slice(ci + 1).trim();
				if (rest.split(/\s+/).length >= (cfg.glue_split_min_words ?? 9)) {
					glued = rest;
					t = t.slice(0, ci).trim();
				}
			}
			const head = Utils.FillTemplate(cfg.curric_heading ?? "<h{level}><span>{heading}</span></h{level}>",
				{ level: String(row.curric_level ?? "h4").replace(/^h/i, ""), heading: Utils.EscapeHtml(t) });
			if (!glued) return head;
			return [head, ...ListsAndRuns.renderBlackText(glued, run)].join("\n");
		}
		if (r.kind === "li" || r.kind === "sc") {
			let t = r.headingText;
			if (cfg.reduce_li_bilingual !== false && t.includes("|")) t = t.split("|").pop().trim();
			return Utils.FillTemplate(cfg.li_sc_heading ?? "<h{level}>{heading}</h{level}>",
				{ level: String(row.li_level ?? "h5").replace(/^h/i, ""), heading: Utils.EscapeHtml(t) });
		}
		return r.headHtml;
	};

	/**
	 * Composes the tabs OVERVIEW menu's pane-1 registry columns from the
	 * kind-tagged runs collected during the walk in buildMenu() (e.g. module
	 * ENGJ402).
	 *
	 * REGISTRY ROW LOOKUP: this exact module's series (only recorded for
	 * modules that deviate from the rest of their group) → its subject|phase
	 * group (case-tolerant match).
	 *
	 * SPLIT KINDS (which columns exist and what goes where, read from the
	 * matched registry row):
	 *   - curric_li:    curriculum columns, with LI/SC content in the LAST
	 *                    column (module ENGJ402's shape)
	 *   - curric_split: no LI content in pane 1 at all — the captured LI/SC
	 *                    runs move over to TAB 2 instead, which is where the
	 *                    human-built pages actually put them (modules
	 *                    AGH1001/MXDI201)
	 *   - li_sc:        one column for LI, one column for SC (module CEDK501)
	 *
	 * DISTRIBUTION RULES for curriculum runs across columns:
	 *   - the LAST curriculum run always anchors the LAST curriculum column
	 *     (an "Understand, Know | Do" split is the dominant shape, seen on
	 *     11 modules)
	 *   - a col-md-12 "BAND" column (a full-width spacer row) takes the
	 *     FIRST curriculum run ONLY when exactly one other curriculum column
	 *     remains (module AGH1001's "Understand | Know, Do" shape), and
	 *     stays EMPTY when two columns remain (modules ANZH304/ANZH404's
	 *     "| Understand, Know | Do" shape — the human ships an empty spacer
	 *     div there, so we match that)
	 *   - a "lead"/"other" run (content with no heading of its own) rides
	 *     along with whichever column the previous routed run landed in —
	 *     keeping document order means content always stays with its own
	 *     section
	 *
	 * DECLINES (returns null, meaning: fall back to the plain single-column
	 * pane built earlier) on any of: a lesson page (this layout only applies
	 * to overview pages), a reo/bilingual module (see isReoModule), no
	 * matching registry row or a "single"-column row, a missing required run
	 * kind, or any non-band column that would end up empty (we never ship a
	 * visibly empty column).
	 *
	 * @param {Array} runs - the kind-tagged runs collected during the walk
	 * @param {Object} run - the conversion run context
	 * @param {Object} page - the page being built
	 * @param {Object} cfg - the tabs_pane1_two_col config block
	 * @returns {{cols: Array, tab2Prepend: string, tab2Cols: Array|null}|null}
	 */
	static #tabsPane1Partition(runs, run, page, cfg) {
		if (!page.isOverview || this.isReoModule(run)) return null;
		if (!runs.some((r) => r.headHtml)) return null;   // no headed structure to partition
		const subj = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		// the registry was mined from the human pages' template ATTRIBUTE, so a compound
		// phase band normalises through the same map the attribute does ("9-10/NCEA" →
		// "NCEA", CEDK501/ENGS401/OSAH501 — else the lookup silently misses the group row)
		const rawPhase = run.resolvedRules?.template_phase ?? "";
		const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
		const reg = cfg.registry ?? {};
		let row = reg.series?.[run.moduleCode] ?? reg.groups?.[`${subj}|${phase}`];
		if (!row && reg.groups) {
			const lk = `${subj}|${phase}`.toLowerCase();
			const hit = Object.keys(reg.groups).find((k) => k.toLowerCase() === lk);
			if (hit) row = reg.groups[hit];
		}
		if (!row || row.split === "single" || !Array.isArray(row.cols) || row.cols.length < 2) return null;

		const N = row.cols.length;
		const isBand = (i) => /\bcol-md-12\b/.test(row.cols[i] ?? "");
		const curric = runs.filter((r) => r.kind === "curric");
		const lisc = runs.filter((r) => r.kind === "li" || r.kind === "sc");
		const moveTab2 = row.split === "curric_split" && cfg.move_li_tab2_when_curric_split !== false;
		const colOf = new Map();

		if (row.split === "li_sc") {
			const firstSc = lisc.findIndex((r) => r.kind === "sc");
			if (firstSc <= 0) return null;             // need an LI run THEN an SC run to split
			lisc.forEach((r, i) => colOf.set(r, i < firstSc ? 0 : Math.min(1, N - 1)));
		} else {
			if (!curric.length) return null;
			const cols = row.split === "curric_li"
				? [...Array(N - 1).keys()] : [...Array(N).keys()];
			if (cols.length >= 2 && isBand(cols[0])) {
				const rest = cols.slice(1);
				if (rest.length === 1) {               // band + 1: band takes the FIRST run (AGH1001)
					colOf.set(curric[0], cols[0]);
					curric.slice(1).forEach((r) => colOf.set(r, rest[0]));
				} else {                               // band + 2+: band stays EMPTY (ANZH304)
					curric.forEach((r, i) => colOf.set(r,
						i === curric.length - 1 ? rest[rest.length - 1] : rest[0]));
				}
			} else if (cols.length >= 2) {             // no band: u,k | d (the 6+6 dominant)
				curric.forEach((r, i) => colOf.set(r,
					i === curric.length - 1 ? cols[cols.length - 1] : cols[0]));
			} else {
				curric.forEach((r) => colOf.set(r, cols[0]));
			}
			if (row.split === "curric_li") {
				if (!lisc.length) return null;         // registry says LI lives in pane 1; none captured
				lisc.forEach((r) => colOf.set(r, N - 1));
			}
		}

		// document-order walk: a lead/other run rides the previous routed run's col
		const colHtml = Array.from({ length: N }, () => []);
		const t2moved = [];
		// The moved LI/SC content ALSO accumulates into two buckets (LI content on
		// the left, SC content on the right) for the tab-2 two-column layout below;
		// the split point is the FIRST "sc"-kind run encountered, in document order.
		const t2Left = [], t2Right = [];
		// ... and a STRUCTURED copy (one {kind, html} per moved run) for the
		// round-211 menu.tab2_cols composer, which interleaves the moved LI/SC
		// with the pane's NATIVE content into the group's registered column pair.
		const t2movedRuns = [];
		let sawSc = false;
		let cur = 0;
		for (const r of runs) {
			if (moveTab2 && (r.kind === "li" || r.kind === "sc")) {
				const headHtml = this.#tabsPane1HeadHtml(r, row, cfg, run);
				t2moved.push(headHtml, ...r.pieces);
				t2movedRuns.push({ kind: r.kind, html: [headHtml, ...r.pieces].join("\n") });
				if (r.kind === "sc") sawSc = true;
				(sawSc ? t2Right : t2Left).push(headHtml, ...r.pieces);
				continue;
			}
			if (colOf.has(r)) cur = colOf.get(r);
			if (r.headHtml) colHtml[cur].push(this.#tabsPane1HeadHtml(r, row, cfg, run));
			colHtml[cur].push(...r.pieces);
		}
		// per-col empty-heading drop BEFORE the guard (a heading whose content was dropped
		// must not smuggle an otherwise-empty col past it)
		const html = colHtml.map((h) => this.dropEmptyHeadings(h.join("\n"), run));
		for (let i = 0; i < N; i++) {
			if (!html[i].trim() && !(i === 0 && N >= 3 && isBand(0))) return null;
		}
		// TAB-2 TWO-COLUMN LAYOUT (e.g. module ENGR202): render the moved LI/SC
		// content as two col-md-6 columns (LI on the left, SC on the right),
		// reusing the SAME pair of col-md-6 columns the registry row already
		// defines for pane 1 (the human-built pages ship exactly that
		// padding-right/padding-left pair) — instead of the flatter single-column
		// prepend used as the fallback. Guarded: requires both an LI run AND an SC
		// run present, EXACTLY two col-md-6 columns available in the registry row,
		// and both sides ending up non-empty; otherwise this stays null and the
		// caller falls back to the flat tab2Prepend form built above. A reo
		// (bilingual) module was already declined at the top of this method.
		// Env TAB2COL_OFF disables this two-column layout.
		let tab2Cols = null;
		const c6 = (row.cols || []).filter((c) => /\bcol-md-6\b/.test(c));
		if ((cfg.move_li_two_col !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.TAB2COL_OFF)
			&& t2Left.length && t2Right.length && c6.length === 2) {
			const L = this.dropEmptyHeadings(t2Left.join("\n"), run);
			const R = this.dropEmptyHeadings(t2Right.join("\n"), run);
			if (L.trim() && R.trim()) tab2Cols = [{ cls: c6[0], html: L }, { cls: c6[1], html: R }];
		}
		return {
			cols: html.map((h, i) => ({ cls: row.cols[i], html: h })),
			tab2Prepend: t2moved.length ? t2moved.join("\n") : "",
			tab2Cols,
			t2movedRuns,
		};
	};

	/**
	 * Looks up the registry row that defines the fundamentals overview LI/SC
	 * menu's column layout (data path: menu.fundamentals_overview_li.registry)
	 * for this module: this exact module's series override → its
	 * subject|template_phase group (case-tolerant, with the phase value
	 * normalised through skeleton.template_attr_map first — the same lookup
	 * shape used by #tabsPane1Partition above).
	 *
	 * This method is PUBLIC (not a private #-prefixed method) because
	 * ContentConverter's #partitionItems method also needs to consult it, at
	 * the point where menu items get CAPTURED — using the same lookup for
	 * both capture and compose means the two steps can never disagree about
	 * whether this menu layout applies to a given module.
	 *
	 * @param {Object} run - the conversion run context
	 * @param {Object} cfg - the fundamentals_overview_li config block
	 * @returns {Object|null} the registry row (with a 2-entry `cols` array),
	 *   or null if none is defined for this module
	 */
	static fundamentalsLiRow(run, cfg) {
		const subj = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const rawPhase = run.resolvedRules?.template_phase ?? "";
		const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
		const reg = cfg?.registry ?? {};
		let row = reg.series?.[run.moduleCode] ?? reg.groups?.[`${subj}|${phase}`];
		if (!row && reg.groups) {
			const lk = `${subj}|${phase}`.toLowerCase();
			const hit = Object.keys(reg.groups).find((k) => k.toLowerCase() === lk);
			if (hit) row = reg.groups[hit];
		}
		if (!row || !Array.isArray(row.cols) || row.cols.length !== 2) return null;
		return row;
	};

	/**
	 * Composes the fundamentals overview LI/SC menu's two columns from the
	 * captured front-matter [Overview] region — the items that
	 * ContentConverter's #partitionItems marked with `_funLi` (see module
	 * HPFUN903 for an example that uses this menu shape).
	 *
	 * HOW: split the region's plain-text lines at the Success-Criteria (SC)
	 * lead line into an LI column and an SC column; each column becomes the
	 * registry's GENERATED label heading followed by its lines, rendered via
	 * ListsAndRuns.renderBlackText() (a short lead-in line stays a plain <p>;
	 * consecutive bullets group into one <ul>). `lead_colon_normalise` trims
	 * a lead line's trailing ellipsis/dots (and strips any decorative emoji,
	 * e.g. module ENFUN04's checkmark symbol) down to a clean trailing ':'
	 * form; a lead line that folds identically to its own generated column
	 * label is DEDUP-DROPPED (some modules' SC lead line IS already the
	 * label text, so the human-built page ships no separate <p> for it
	 * there).
	 *
	 * Any instruction span found inside the captured region still renders as
	 * a standard red "CS:" note in its column (never silently discarded —
	 * see the "never silently strip a documented instruction" rule); a known
	 * unfilled Writers-Template placeholder prompt is already omitted
	 * upstream by the placeholder-prompt rule inside
	 * NotesAndComments.redFlag.
	 *
	 * @param {Array} menuItems - the page's menu items (only the `_funLi`
	 *   flagged ones are used)
	 * @param {Object} run - the conversion run context
	 * @param {Object} page - the page being built
	 * @param {TagNormaliser} norm - the tag-normaliser instance
	 * @param {Object} cfg - the fundamentals_overview_li config block
	 * @returns {Array|null} [{cls, html}, {cls, html}] — the two columns —
	 *   or null (DECLINE, meaning: fall back to the generic menu walk) on: a
	 *   lesson page, a reo/bilingual module, no matching registry row,
	 *   either lead line missing, or either column ending up with no real
	 *   content (we never ship a visibly empty column)
	 */
	static #fundamentalsOverviewLi(menuItems, run, page, norm, cfg) {
		if (!page.isOverview || this.isReoModule(run)) return null;
		const row = this.fundamentalsLiRow(run, cfg);
		if (!row) return null;

		const foldLine = (s) => Utils.Fold(String(s)).replace(/[*_]/g, "").replace(/\s+/g, " ").trim();
		const maxW = cfg.lead_max_words ?? 10;
		const isLead = (list) => (ln) => {
			const f = foldLine(ln);
			if (!f || /^[•\-–—]/.test(f)) return false;                    // a bullet is never a lead
			if (f.split(/\s+/).length > maxW) return false;                // lead-sized lines only
			return (list ?? []).some((m) => f === m || f.startsWith(m + " ") || f.startsWith(m + ":")
				|| f.startsWith(m + "…") || f.startsWith(m + "."));
		};
		const isWalt = isLead(cfg.walt_match);
		const isSc = isLead(cfg.sc_match);

		// document-order walk: lines accumulate into the LI side until the SC lead flips it
		const sides = { li: { lines: [], flags: [] }, sc: { lines: [], flags: [] } };
		let side = "li", sawWalt = false, sawSc = false;
		const takeLines = (text) => {
			for (const ln of String(text ?? "").split(/\n+/)) {
				if (!ln.trim()) continue;
				if (!sawSc && isSc(ln)) { side = "sc"; sawSc = true; }
				else if (!sawWalt && isWalt(ln)) sawWalt = true;
				sides[side].lines.push(ln);
			}
		};
		for (const it of menuItems) {
			if (!it._funLi) continue;
			if (it.type === "black") { takeLines(it.text); continue; }
			if (it.type !== "tag") continue;
			const p = it.parse?.primary;
			if (!p || it.parse?.class === "instruction" || it.parse?.class === "noise") {
				// non-structural red: an instruction surfaces as the standard CS note in its
				// column (never silently stripped, §6); a noise span renders nothing itself
				if (it.parse?.class === "instruction" || it.parse?.instructionFragment) {
					const flag = NotesAndComments.redFlag(it.text, run, "cs");
					if (flag) sides[side].flags.push(flag);
				}
				takeLines(it.blackAfter);
				continue;
			}
			if (it.parse?.instructionFragment) {
				const flag = NotesAndComments.redFlag(it.text, run, "cs");
				if (flag) sides[side].flags.push(flag);
			}
			takeLines(it.blackAfter);                                      // safe tags: their black content
		}
		if (!sawWalt || !sawSc) return null;
		if (!sides.li.lines.length || !sides.sc.lines.length) return null;

		const alnum = (s) => Utils.Fold(String(s)).replace(/[^\p{L}\p{N}]+/gu, "");
		const build = (key, labelHtml) => {
			let lines = sides[key].lines.slice();
			if (cfg.lead_colon_normalise !== false && lines.length) {
				// the lead line: strip italic markers + emoji marks, trim trailing …/./: → ':'
				let lead = lines[0].replace(/[*_]/g, "").replace(/[\p{So}️]/gu, "").trim();
				lead = lead.replace(/[\s.:…]+$/u, "").trim();
				if (lead) lines[0] = lead + ":";
			}
			const labelText = String(labelHtml).replace(/<[^>]+>/g, "");
			if (lines.length && alnum(lines[0]) === alnum(labelText)) lines = lines.slice(1);
			const pieces = lines.length ? ListsAndRuns.renderBlackText(lines.join("\n"), run) : [];
			if (!pieces.length) return null;                               // a label-only column never ships
			return [labelHtml, ...pieces, ...sides[key].flags].join("\n");
		};
		let li = build("li", row.li_heading ?? "<h5>Learning intentions</h5>");
		let sc = build("sc", row.sc_heading ?? "<h5>Success criteria</h5>");
		if (!li || !sc) return null;
		// Apply the general menu italic strip (a reo/bilingual module was already
		// declined above) plus the empty-heading guard.
		li = this.dropEmptyHeadings(this.stripTextItalic(li), run);
		sc = this.dropEmptyHeadings(this.stripTextItalic(sc), run);
		if (!li.trim() || !sc.trim()) return null;
		run.AddNote("info", "MenuBuilder",
			"Fundamentals [Overview] WALT/I-can block routed to the module menu as the two-col LI/SC form (menu.fundamentals_overview_li).");
		return [{ cls: row.cols[0], html: li }, { cls: row.cols[1], html: sc }];
	};

	/**
	 * Is this a BILINGUAL-TEMPLATE module (te reo Māori + English)? The
	 * general menu italic strip above is scoped OUT for these: the human
	 * KEEPS italic styling on BOTH panes of a bilingual menu — the Māori
	 * line AND its English translation (see modules TRR108/TRR301 for
	 * examples). Keyed on the dual-language TEMPLATE only: the reoTranslate
	 * body class, OR the TRR/PNR module-code prefixes (covers all 19
	 * bilingual modules in the library).
	 *
	 * We deliberately do NOT use run.mtkFlag here: mtkFlag is a much
	 * broader "does this document contain any Māori-content signature at
	 * all" flag (DocxExtractor scans the document's first 60 paragraphs for
	 * a te-reo marker), and it also fires on ordinary Standard/Inquiry
	 * modules that simply happen to include some Māori content (e.g. module
	 * CEDO102 mentions Tangaroa/Māui) — but whose menu the human DOES still
	 * strip italic from. Using mtkFlag here would wrongly suppress the
	 * italic strip on almost every reo-flavoured English menu in the
	 * library.
	 *
	 * @param {Object} run - the conversion run context
	 * @returns {boolean}
	 */
	static isReoModule(run) {
		const dl = DataService.Data.EmitTemplates.elements?.dual_language || {};
		return /reoTranslate/i.test(run.resolvedRules?.body_class || "")
			|| (dl.code_prefixes || []).some((p) =>
				String(run.moduleCode || "").toUpperCase().startsWith(String(p).toUpperCase()));
	};

	/**
	 * Composes the MTK "Te Aka Taumatua" bilingual tabs menu from the
	 * drop-down-menu table (ROUND 212 — the PNR101/102/104 family).
	 *
	 * INPUT: the English|Māori two-column table between "[Content for DROP DOWN
	 * MENU]" and "[END OF DROP-DOWN MENU]" (flagged "_reoDropdown" upstream by
	 * ContentConverter's #partitionItems). Column 1 = English, column 2 = Māori
	 * (the same orientation BilingualBuilder.bilingualRows reads).
	 *
	 * ROW GRAMMAR (verified against all three human golds):
	 *  - a row carrying a [TABn] tag opens tab-pane n; the row's own text is the
	 *    nav label ONLY (the human never repeats it inside the pane) — nav item =
	 *    <li><a><span reo>{māori}</span><span eng>{english}</span></a></li>;
	 *  - a [TITLE BAR] row is skipped (its payload is empty in every measured WT;
	 *    the module title comes from the front-matter "Module Name" metadata row
	 *    instead — see PageAssembler);
	 *  - a plain "**English** | **Māori**" divider row is skipped;
	 *  - a [Hn]-tagged heading row renders as a reo/eng PAIR: the pane's FIRST
	 *    heading and every [H2] → <h4><span> section head; any later [H1]/[H3]
	 *    → <h5> lead-in (the human's exact levels on all three golds);
	 *  - a heading whose folded text matches pane_split_labels ("Connections" /
	 *    "Ngā Hononga") starts the pane's SECOND column (paddingR | paddingL —
	 *    the human splits the Information pane there on all three golds);
	 *  - every other row is body content, rendered through
	 *    BilingualBuilder.bilingualSplit (paragraphs, • bullet lists, media) and
	 *    interleaved element-wise Māori-first — a "☐" checklist line becomes a
	 *    normal bullet first (checkbox_bullet), matching the human's <ul>.
	 *
	 * DECLINES (returns null → the generic walk runs instead): no table rows, or
	 * no [TABn] row found at all.
	 *
	 * Data: elements.dual_language.dropdown_menu. Env toggle: REODROPMENU_OFF
	 * (disables the upstream capture, so this is never reached when set).
	 *
	 * @param {Object[]} menuItems - partitioned menu items (holds the flagged table)
	 * @param {ConversionRun} run - module identity, notes
	 * @param {TagNormaliser} norm - tag resolution for cell content
	 * @param {Object} cfg - the dropdown_menu data block
	 * @returns {{nav: string, panes: string}|null}
	 */
	static #reoDropdownTabs(menuItems, run, norm, cfg) {
		const tblItem = menuItems.find((it) => it._reoDropdown);
		const rows = tblItem?.block?.rows ?? [];
		if (!rows.length) return null;

		const stripRed = (s) => String(s ?? "")
			.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "");
		// peels every leading "[tag]" token off a cell; returns the tokens + text
		const leadTags = (s) => {
			let t = stripRed(s).trim();
			const tags = [];
			let m;
			while ((m = t.match(/^\[([^\]]*)\]\s*/))) { tags.push(m[1].trim()); t = t.slice(m[0].length); }
			return { tags, text: t.trim() };
		};
		const fold = (s) => Utils.Fold(String(s ?? "").replace(/\*/g, " "))
			.replace(/\s+/g, " ").trim();
		const clean = (s) => String(s ?? "").replace(/\*\*/g, "").replace(/^\*+|\*+$/g, "").trim();
		const tabNum = (tags) => {
			for (const t of tags) { const m = fold(t).match(/^tab\s*(\d+)$/); if (m) return m[1]; }
			return null;
		};
		const headLevel = (tags) => {
			for (const t of tags) { const m = fold(t).match(/^h(\d)$/); if (m) return parseInt(m[1], 10); }
			return null;
		};
		const splitLabels = (cfg.pane_split_labels ?? []).map((l) => fold(l));

		const panes = [];
		let pane = null, col = null, paneHadHeading = false;
		const newPane = (navEng, navReo) => {
			pane = { navEng, navReo, cols: [[]] };
			col = pane.cols[0];
			paneHadHeading = false;
			panes.push(pane);
		};

		for (const row of rows) {
			if (!Array.isArray(row) || !row.length) continue;
			const engCell = row[0] ?? "";
			const reoCell = row.length > 1 ? (row[1] ?? "") : "";
			const E = leadTags(engCell), R = leadTags(reoCell);
			const eFold = fold(E.text), rFold = fold(R.text);

			// [TITLE BAR] row — payload empty in every measured WT; skipped
			if ([...E.tags, ...R.tags].some((t) => fold(t) === "title bar")) continue;
			// "**English** | **Māori**" divider row — layout scaffolding, skipped
			if (!E.tags.length && !R.tags.length
				&& (eFold === "english" || eFold === "") && (rFold === "maori" || rFold === "")
				&& (eFold || rFold)) continue;

			// a [TABn] row opens a new pane; its text is the nav label only
			const tn = tabNum(E.tags) ?? tabNum(R.tags);
			if (tn !== null) { newPane(clean(E.text), clean(R.text)); continue; }
			if (!pane) continue;   // stray content before the first [TABn] row

			const lvl = headLevel(E.tags) ?? headLevel(R.tags);
			if (lvl !== null && (E.text || R.text)) {
				// the Connections-family heading starts the pane's SECOND column
				if (pane.cols.length === 1
					&& splitLabels.some((l) => eFold === l || rFold === l)) {
					pane.cols.push([]);
					col = pane.cols[1];
				}
				const isSection = !paneHadHeading || lvl === 2;
				paneHadHeading = true;
				const tplH = isSection
					? (cfg.heading_section ?? "<h4><span>{text}</span></h4>")
					: (cfg.heading_lead ?? "<h5>{text}</h5>");
				if (R.text) col.push(BilingualBuilder.langAttr(
					Utils.FillTemplate(tplH, { text: Utils.EscapeHtml(clean(R.text)) }), "reo"));
				if (E.text) col.push(BilingualBuilder.langAttr(
					Utils.FillTemplate(tplH, { text: Utils.EscapeHtml(clean(E.text)) }), "eng"));
				continue;
			}

			// body row — reo/eng element pairs via the shared bilingual cell renderer;
			// a "☐" checklist line becomes an ordinary bullet first, so it groups
			// into the same <ul> the human ships
			const pre = (cell) => cfg.checkbox_bullet === false
				? String(cell ?? "") : String(cell ?? "").replace(/☐\s*/gu, "• ");
			const Rr = BilingualBuilder.bilingualSplit(pre(reoCell), run, norm);
			const Ee = BilingualBuilder.bilingualSplit(pre(engCell), run, norm);
			const n = Math.max(Rr.text.length, Ee.text.length);
			for (let k = 0; k < n; k++) {
				if (k < Rr.text.length) col.push(BilingualBuilder.langAttr(Rr.text[k], "reo"));
				if (k < Ee.text.length) col.push(BilingualBuilder.langAttr(Ee.text[k], "eng"));
			}
			for (const m of (Rr.media.length ? Rr.media : Ee.media)) col.push(m);
		}

		if (!panes.length) return null;   // no [TABn] rows — not this menu shape

		const colTpl = cfg.col_template ?? "<div class=\"{cls}\">\n{content}\n</div>";
		const nav = panes.map((p) => Utils.FillTemplate(
			cfg.nav_item ?? "\n<li><a><span reo>{reo}</span><span eng>{eng}</span></a></li>",
			{ reo: Utils.EscapeHtml(p.navReo), eng: Utils.EscapeHtml(p.navEng) })).join("");
		const panesHtml = panes.map((p, pi) => {
			const colsHtml = p.cols.map((c, ci) => Utils.FillTemplate(colTpl, {
				cls: pi === 0 ? (cfg.col_first_pane ?? "col-md-8 col-12")
					: (ci === 0 ? (cfg.col_pane ?? "col-md-6 offset-md-0 col-12 paddingR")
						: (cfg.col_split ?? "col-md-6 offset-md-0 col-12 paddingL")),
				content: c.join("\n"),
			})).join("\n");
			return Utils.FillTemplate(
				cfg.pane_template ?? "\n<div class=\"tab-pane\">\n<div class=\"row\">\n{cols}\n</div>\n</div>",
				{ cols: colsHtml });
		}).join("");
		return { nav, panes: panesHtml };
	};

	/**
	 * WRITER-AUTHORED MENU TAB PARTITION (ROUND 221 — module ENGJ403; see the
	 * buildMenu branch that calls this). Detects the newest WT era's explicit
	 * overview-menu tab markup — a "[please set up as … tabs]" SET-UP
	 * instruction (whose span usually also carries the glued first "[tab 1 –
	 * please title as appropriate]" opener), later "[tab N]" openers, and
	 * "[close tab]" closers — and composes one nav item + one tab-pane per
	 * writer tab, partitioned exactly where the writer put the markers.
	 *
	 * Composition per pane (all forms from menu.writer_tab_partition):
	 * - heading-led SECTIONS, kind-tagged li/sc/other via li_match/sc_match;
	 * - a pane with any LI/SC section splits LI/SC LEFT | rest RIGHT; a pane
	 *   without splits balanced (first half of the sections LEFT) — the same
	 *   two kinds as the round-211 tab2_cols registry, here decided by pane;
	 * - a short WALT/I-can lead line directly under an LI/SC heading renders
	 *   via lead_element (<h5>, the ENGJ403 human form) instead of a <p>;
	 * - piped bilingual headings are kept WHOLE (keep_bilingual_headings —
	 *   the human keeps "Whakamaheretia tō wā | Planning your time");
	 * - a heading BEFORE the set-up item becomes the pane-1 BANNER
	 *   ("Tirohanga Whānui | Overview" as <h3><span> in a full-width col);
	 * - an instruction span still flags/omits via NotesAndComments.redFlag
	 *   (so the "In this section outline any connections…" template prompt
	 *   is dropped by the round-86 omit list, matching the human);
	 * - nav labels come from the opener's own label text unless it is
	 *   template boilerplate (instruction_label_pattern), in which case the
	 *   corpus-standard default_labels (Overview/Information…) apply.
	 *
	 * NEVER HALF-BUILDS: returns null (fall back to the fold-routing walk)
	 * unless the set-up instruction, >=1 closer and >=2 non-empty panes are
	 * all present.
	 *
	 * @param {Array} menuItems - the overview menu-region items
	 * @param {ConversionRun} run
	 * @param {TagNormaliser} norm
	 * @param {Object} cfg - Emit_Templates menu.writer_tab_partition
	 * @returns {{nav:string,panes:string,count:number}|null}
	 */
	/**
	 * Composes the LEVEL-PAGE fundamentals menu (ROUND 265 — the CHFUN
	 * "[PAGE N Novice]" dialect): one "Overview" tab pane built from the
	 * module's own [Overview]-section LI/SC blocks, plus one tab pane per
	 * LEVEL (Novice, Emergent, …) built from that level's aggregated
	 * "[Page Overview]" learning-intentions blocks. Every pane is the same
	 * two-column shape the human ships: LI (heading + lead + bullets) on the
	 * left, SC on the right. The pane headings are the writer's own
	 * [H3] labels from the module's [Overview] section ("Learning
	 * Intentions" / "How will I know I have learned it?"), reused across the
	 * level panes exactly as the human does; data defaults cover a module
	 * whose writer omitted them.
	 *
	 * Returns { nav, panes } for the writer_tabs shell, or null when nothing
	 * usable was captured (the caller then falls through to the ordinary menu
	 * machinery).
	 *
	 * @param {Object} data - run._levelMenu ({ module, levels, row, cfg })
	 * @returns {{nav: string, panes: string}|null}
	 *
	 * Data: body_region.fundamentals_panels.level_pages (menu templates under
	 * its `menu` block; pane columns from the matched registry row).
	 * Env toggle: LEVELPAGE_OFF (upstream — this method is never reached).
	 */
	static #levelTabs(data) {
		const { module: mod, levels, row, cfg } = data;
		const mc = cfg.menu || {};
		const hasContent = (b) => b && (b.bullets.length || b.lead);
		if (!hasContent(mod.li) && !levels.some((l) => hasContent(l.li) || hasContent(l.sc))) return null;
		const liLabel = (mod.li && mod.li.label) || mc.li_label_default || "Learning Intentions";
		const scLabel = (mod.sc && mod.sc.label) || mc.sc_label_default || "How will I know I have learned it?";
		const cols = row.menu_cols || ["col-md-6 offset-md-0 col-12 paddingR", "col-md-6 offset-md-0 col-12 paddingL"];
		const colHtml = (bucket, label) => {
			const parts = [Utils.FillTemplate(mc.heading_template || "<h5>{label}</h5>", { label: Utils.EscapeHtml(label) })];
			if (bucket && bucket.lead) parts.push(`<p>${Utils.EscapeHtml(bucket.lead)}</p>`);
			if (bucket && bucket.bullets.length) {
				// bullet punctuation, the human's pane convention: every bullet
				// bare (its trailing comma/full-stop dropped), only the FINAL
				// one closing with a full stop
				const bs = bucket.bullets.map((b, i) => {
					let t = String(b).trim().replace(/[.,]$/, "");
					if (i === bucket.bullets.length - 1 && /[\p{L}\p{N}]$/u.test(t)) t += ".";
					return t;
				});
				parts.push("<ul>");
				for (const b of bs) parts.push(`<li>${Utils.EscapeHtml(b)}</li>`);
				parts.push("</ul>");
			}
			return parts.join("\n");
		};
		const pane = (li, sc) =>
			(mc.pane_open || "\n<div class=\"tab-pane\">\n<div class=\"row\">") + "\n"
			+ Utils.FillTemplate(mc.col_template || "<div class=\"{cls}\">\n{content}\n</div>",
				{ cls: cols[0], content: colHtml(li, liLabel) }) + "\n"
			+ Utils.FillTemplate(mc.col_template || "<div class=\"{cls}\">\n{content}\n</div>",
				{ cls: cols[1] ?? cols[0], content: colHtml(sc, scLabel) })
			+ (mc.pane_close || "\n</div>\n</div>");
		const navItem = (label) => Utils.FillTemplate(mc.nav_item || "\n<li><a>{label}</a></li>",
			{ label: Utils.EscapeHtml(label) });
		let nav = navItem(mc.overview_label || "Overview");
		let panes = pane(mod.li, mod.sc);
		for (const l of levels) {
			nav += navItem(l.label);
			panes += pane(l.li, l.sc);
		}
		return { nav, panes };
	};

	static #writerTabPartition(menuItems, run, norm, cfg) {
		const foldOf = (it) => String(it.parse?.folded ?? Utils.Fold(String(it.text || ""))).trim();
		const setupRe = new RegExp(cfg.setup_pattern ?? "set ?up as .{0,24}tabs", "i");
		const openRe = new RegExp(cfg.opener_pattern ?? "^\\[?tab\\s*(\\d+)", "i");
		const closeRe = new RegExp(cfg.closer_pattern ?? "^\\[?(?:close|end)\\s+tab", "i");

		// ---- detect the markers -------------------------------------------
		let setupIdx = -1, closers = 0;
		const openerIdx = [];
		menuItems.forEach((it, i) => {
			if (it.type !== "tag") return;
			const f = foldOf(it);
			if (setupIdx < 0 && setupRe.test(f)) { setupIdx = i; return; }
			if (closeRe.test(f)) { closers++; return; }
			if (openRe.test(f)) openerIdx.push(i);
		});
		if (setupIdx < 0 || closers < (cfg.min_closers ?? 1)) return null;

		// ---- partition the items into writer panes ------------------------
		// pane 1 opens AT the set-up item (its span carries the glued first
		// opener); each later [tab N] opener starts the next pane; [close tab]
		// closes the current one (a stray item between a close and the next
		// opener stays with the most recent pane — defensive, none measured).
		const labelFrom = (rawText) => {
			const m = String(rawText || "").match(/\[\s*tab\s*\d+\s*[-–—:]?\s*([^\]]*)\]/i);
			return (m && m[1] ? m[1] : "").trim();
		};
		const panes = [{ label: labelFrom(menuItems[setupIdx].text), items: [] }];
		const pre = menuItems.slice(0, setupIdx);
		for (let i = setupIdx + 1; i < menuItems.length; i++) {
			const it = menuItems[i];
			if (it.type === "tag") {
				const f = foldOf(it);
				if (closeRe.test(f)) continue;                       // marker — renders nothing
				const om = f.match(openRe);
				if (om) { panes.push({ label: labelFrom(it.text), items: [] }); continue; }
			}
			panes[panes.length - 1].items.push(it);
		}
		if (panes.length < 2 || panes.some((p) => !p.items.length)) return null;

		// ---- the pane-1 banner: a heading BEFORE the set-up item ----------
		let banner = "";
		for (const it of pre) {
			if (it.type !== "tag" || !it.parse?.primary) continue;
			if (!["h1", "h2", "h3", "h4", "h5", "heading"].includes(it.parse.primary.tag)) continue;
			const t = (norm.RenderText(it.text) || it.blackAfter || "").replace(/\*/g, "").trim();
			if (t) banner = Utils.FillTemplate(
				cfg.banner ?? "<div class=\"col-md-12 col-12 paddingR\">\n<h3><span>{heading}</span></h3>\n</div>",
				{ heading: Utils.EscapeHtml(t) });
		}

		// ---- render each pane ---------------------------------------------
		const navParts = [], paneParts = [];
		const instrLabelRe = new RegExp(cfg.instruction_label_pattern ?? "please|title as appropriate", "i");
		const defaults = cfg.default_labels ?? ["Overview", "Information"];
		panes.forEach((p, idx) => {
			const label = (p.label && !instrLabelRe.test(p.label))
				? p.label : (defaults[idx] ?? `Tab ${idx + 1}`);
			navParts.push(Utils.FillTemplate(cfg.nav_item ?? "\n<li><a>{label}</a></li>",
				{ label: Utils.EscapeHtml(label) }));
			let paneHtml = this.#writerTabPane(p.items, run, norm, cfg, idx === 0);
			if (!this.isReoModule(run)) paneHtml = this.stripTextItalic(paneHtml);
			paneParts.push(Utils.FillTemplate(
				cfg.pane_template ?? "\n<div class=\"tab-pane\">\n{banner}{content}\n</div>",
				{ banner: idx === 0 && banner ? banner + "\n" : "", content: paneHtml }));
		});
		return { nav: navParts.join(""), panes: paneParts.join(""), count: panes.length };
	};

	/**
	 * Renders ONE writer-authored tab pane (see #writerTabPartition): builds
	 * the heading-led sections, then splits them into the two side-by-side
	 * columns (LI/SC left | rest right when LI/SC sections exist, else a
	 * balanced split), each section rendered heading + lead + grouped text.
	 *
	 * @param {Array} items - the pane's partitioned items
	 * @param {ConversionRun} run
	 * @param {TagNormaliser} norm
	 * @param {Object} cfg - menu.writer_tab_partition
	 * @param {boolean} isFirst - pane 1 uses pane1_heading_element (plain h4)
	 * @returns {string} the pane's inner HTML (the row + columns)
	 */
	static #writerTabPane(items, run, norm, cfg, isFirst) {
		const liMatch = cfg.li_match ?? ["learning intention", "whainga ako"];
		const scMatch = cfg.sc_match ?? ["success criteria", "paearu angitu", "how will i know", "you will show"];
		const leadRe = new RegExp(cfg.lead_pattern
			?? "^(we are learning|what are we learning|i can|you will show|how will i know)", "i");
		const hEl = isFirst
			? (cfg.pane1_heading_element ?? "<h4>{heading}</h4>")
			: (cfg.heading_element ?? "<h4><span>{heading}</span></h4>");
		const sections = [{ kind: "other", pieces: [] }];   // pre-heading content bucket
		let textBuf = [];
		const flush = () => {
			if (!textBuf.length) return;
			const sec = sections[sections.length - 1];
			for (const piece of ListsAndRuns.renderBlackText(textBuf.join("\n"), run)) sec.pieces.push(piece);
			textBuf = [];
		};
		const pushLines = (text) => {
			const sec = sections[sections.length - 1];
			for (const line of String(text).split(/\n+/)) {
				if (!line.trim()) continue;
				// a short WALT/I-can lead directly under an LI/SC heading → lead_element
				if ((sec.kind === "li" || sec.kind === "sc") && !sec.leadDone && !textBuf.length
					&& leadRe.test(Utils.Fold(line).replace(/[*_]/g, "").trim())) {
					sec.leadDone = true;
					sec.pieces.push(Utils.FillTemplate(cfg.lead_element ?? "<h5>{lead}</h5>",
						{ lead: Utils.EscapeHtml(line.replace(/[*_]/g, "").trim()) }));
					continue;
				}
				textBuf.push(line);
			}
		};
		for (const it of items) {
			if (it._inquiryCrumb) continue;
			if (it.type === "black") { pushLines(it.text); continue; }
			if (it.type === "table") { flush(); sections[sections.length - 1].pieces.push(TablesAndGrids.contentTable(it.block, run, false, norm)); continue; }
			const primary = it.parse?.primary;
			const headingText = (norm.RenderText(it.text) || it.blackAfter || "").replace(/\*/g, "").trim();
			if (primary && ["h1", "h2", "h3", "h4", "h5", "heading"].includes(primary.tag) && headingText) {
				flush();
				const folded = Utils.Fold(headingText);
				const kind = liMatch.some((m) => folded.includes(m)) ? "li"
					: scMatch.some((m) => folded.includes(m)) ? "sc" : "other";
				// piped bilingual headings ship WHOLE (the ENGJ403 human keeps them)
				const shown = cfg.keep_bilingual_headings === false && headingText.includes("|")
					? headingText.split("|").pop().trim() : headingText;
				sections.push({ kind, pieces: [Utils.FillTemplate(hEl, { heading: Utils.EscapeHtml(shown) })] });
				continue;
			}
			if (!primary && it.parse?.class === "instruction") {
				flush();
				sections[sections.length - 1].pieces.push(NotesAndComments.redFlag(it.text, run, "cs"));
				if ((it.blackAfter || "").trim()) pushLines(it.blackAfter);
				continue;
			}
			if ((it.blackAfter || "").trim()) pushLines(it.blackAfter);
		}
		flush();
		const secs = sections.filter((s) => s.pieces.length);
		if (!secs.length) return "";
		// ---- the two-column split -----------------------------------------
		const pair = cfg.col_pair ?? ["col-md-6 col-12 paddingLR", "col-md-6 col-12 paddingLR"];
		let left, right;
		if (secs.some((s) => s.kind === "li" || s.kind === "sc")) {
			left = secs.filter((s) => s.kind === "li" || s.kind === "sc");
			right = secs.filter((s) => s.kind === "other");
		} else {
			left = secs.slice(0, Math.ceil(secs.length / 2));
			right = secs.slice(Math.ceil(secs.length / 2));
		}
		const colHtml = (list) => list.map((s) => s.pieces.join("\n")).join("\n");
		if (!right.length) {
			return Utils.FillTemplate(cfg.row_single ?? "\n<div class=\"row\">\n<div class=\"{cls}\">\n{content}\n</div>\n</div>",
				{ cls: pair[0], content: colHtml(left) });
		}
		return Utils.FillTemplate(cfg.row_pair
			?? "\n<div class=\"row\">\n<div class=\"{cls1}\">\n{left}\n</div>\n<div class=\"{cls2}\">\n{right}\n</div>\n</div>",
			{ cls1: pair[0], cls2: pair[1], left: colHtml(left), right: colHtml(right) });
	};

	/**
	 * Removes text-italic (<i>/<em>) wrapper tags from a chunk of HTML,
	 * KEEPING the inner text. A Font-Awesome / icon element like
	 * <i class="fa..."> is deliberately left intact (it's matched and
	 * excluded by the icon guard in the regex below), so this strip can
	 * never accidentally break an icon's markup; any other inner markup
	 * like <b>/<a> is preserved too. Used throughout buildMenu().
	 *
	 * @param {string} html
	 * @returns {string}
	 */
	static stripTextItalic(html) {
		return String(html)
			.replace(/<i\b(?![^>]*(?:fa-|fas|far|fal|fab|icon|material|glyphicon))[^>]*>([\s\S]*?)<\/i>/gi, "$1")
			.replace(/<em\b[^>]*>([\s\S]*?)<\/em>/gi, "$1");
	};

	/**
	 * The BOLD-stripping sibling of stripTextItalic: removes <b>/<strong>
	 * wrapper tags, KEEPING the inner text and any inner markup (<i>/<a>/
	 * etc). Repeats until it reaches a fixed point, so nested bold markup
	 * (e.g. <b>x <b>y</b></b>) can't leave an orphaned wrapper tag behind
	 * after just one pass. Also used by ContentConverter's alert-box bold
	 * strip (env ALERTBOLD_OFF).
	 *
	 * @param {string} html
	 * @returns {string}
	 */
	static stripTextBold(html) {
		let s = String(html), prev;
		do {
			prev = s;
			s = s.replace(/<b\b[^>]*>([\s\S]*?)<\/b>/gi, "$1")
				.replace(/<strong\b[^>]*>([\s\S]*?)<\/strong>/gi, "$1");
		} while (s !== prev);
		return s;
	};

	/**
	 * Picks the heading level (h1..h6) the curriculum (Understand/Know/Do)
	 * heading should render at, for the ENG-family two-column menu. The
	 * writer always tags this heading [H2] in the Writers Template, but the
	 * human-built page actually re-levels it — typically one, two, or three
	 * levels deeper — depending on the subject and school phase; this method
	 * looks up the MEASURED dominant level for that combination.
	 *
	 * @param {Object} run - the conversion run context
	 * @param {Object} engCfg - the two_col_li.eng_family config block, which
	 *   holds two lookup tables: curriculum_level_by_group (keyed
	 *   "subject|phase", the most specific and preferred) and
	 *   curriculum_level_by_phase (keyed just by phase, the fallback)
	 * @returns {string} the heading level as a bare digit string (e.g. "3"
	 *   for <h3>)
	 */
	static curriculumLevel(run, engCfg) {
		const subject = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const phase = run.resolvedRules?.template_phase || "_default";
		const byGroup = engCfg.curriculum_level_by_group || {};
		const byPhase = engCfg.curriculum_level_by_phase || {};
		const h = byGroup[`${subject}|${phase}`] || byPhase[phase] || byPhase._default || "h4";
		return String(h).replace(/^h/i, "");
	};

	/**
	 * Removes headings that have no content before the next heading (or the
	 * end of the block). Works on the per-line HTML the menu builder
	 * accumulates — e.g. a configured "What do I need to get started?"
	 * heading that a particular module's writer never actually filled in
	 * with any following content gets dropped entirely, instead of shipping
	 * as an empty, pointless heading.
	 *
	 * @param {string} html - newline-joined menu-column HTML
	 * @param {Object} run - the conversion run context (used to log an
	 *   informational note whenever a heading gets dropped)
	 * @returns {string} same, minus empty-scaffolding headings
	 */
	static dropEmptyHeadings(html, run) {
		const lines = html.split("\n");
		const isHeading = (l) => /^<h[1-6][ >]/.test(l.trim());
		const kept = [];
		for (let i = 0; i < lines.length; i++) {
			if (isHeading(lines[i])) {
				// look ahead: is there any non-heading content before the
				// next heading / end?
				let j = i + 1;
				let hasContent = false;
				for (; j < lines.length; j++) {
					if (isHeading(lines[j])) break;
					if (lines[j].trim()) { hasContent = true; break; }
				}
				if (!hasContent) {
					const label = lines[i].replace(/<[^>]+>/g, "").trim();
					run.AddNote("info", "MenuBuilder",
						`Menu heading "${label}" had no content beneath it — omitted (empty preconfigured scaffolding).`);
					continue;   // drop the empty heading
				}
			}
			kept.push(lines[i]);
		}
		return kept.join("\n");
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { MenuBuilder };
