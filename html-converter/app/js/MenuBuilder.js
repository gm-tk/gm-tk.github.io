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
 *         Menu_Scaffold_Registry (env MENUREG_OFF reads its cruder
 *         legacy_groups/legacy_series rows instead; MENUNONE_OFF disables
 *         the "sibling page-type already says none" fallback rule)
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
 * ContentConverter emits the rest of the page body; keeping menu building
 * here makes "how the module menu renders" a self-contained, easy-to-find
 * unit instead of burying it among thousands of unrelated lines.
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
	 * WHAT/HOW: menu shape is not invented by this code — it is DERIVED from
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
	/**
	 * The INQUIRY overview-menu family (KB 06 §3.4): this page is an OVERVIEW of an Inquiry-template module (the module
	 * index's template_type — a module the index does not know keeps the ordinary path) whose subject is not excluded (the
	 * BLL parents' own gold is the banner form). Returns the family config or null. Data menu.two_col_li.inquiry_family; env
	 * INQFAMILY_OFF (INQMENU_OFF is the inquiry-tab rule's own toggle).
	 */
	/**
	 * KB constraint 75 ("inline → anchor") IN THE MODULE MENU.
	 * The menu's text buffers render through ListsAndRuns.renderBlackText, which does not see the items' hyperlinks, so
	 * without this every writer inline link in a menu pane would lose its href; the gold keeps the NCEA standard-page
	 * links in the Standards / Information tabs (AGH1009, COM1002, HIS1004, MXS1004, PES1001–1004 / 1008 …) and drops
	 * others (named overrides of c75). With the flag on, each buffer carries
	 * its items' block.links into the free-body weave (exact phrase, first occurrence per line, never inside an <a>).
	 * Data menu.inline_links {enabled, env MENULINKS_OFF}.
	 */
	static #menuLinksOn() {
		const cfg = DataService.Data.EmitTemplates.menu?.inline_links;
		if (!cfg || cfg.enabled === false) return false;
		return !(typeof process !== "undefined" && process.env && process.env[cfg.env ?? "MENULINKS_OFF"]);
	}

	static #inquiryFamilyFor(run, page) {
		const cfg = DataService.Data.EmitTemplates?.menu?.two_col_li?.inquiry_family;
		if (!cfg || cfg.enabled === false || !page?.isOverview) return null;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "INQFAMILY_OFF"]) return null;
		const code = String(run?.moduleCode || "");
		const tt = DataService.Data.ModuleStructureIndex?.module_meta?.[code]?.template_type;
		if (!tt || tt !== (cfg.template_type ?? "Inquiry")) return null;
		const subj = code.match(/^[A-Za-z]+/)?.[0] ?? "";
		if ((cfg.exclude_subjects ?? []).some((p) => subj.toUpperCase().startsWith(String(p).toUpperCase()))) return null;
		return cfg;
	}

	/** The public face of #inquiryFamilyFor (ContentConverter's overview partition asks it for the colon label match). */
	static inquiryFamilyFor(run, page) {
		return this.#inquiryFamilyFor(run, page);
	}

	/**
	 * The two-column FAMILY for this page: the Inquiry family (overviews of Inquiry-template modules), else the ITEM
	 * family — a module whose code starts with one of menu.two_col_li.item_family.code_prefixes, on EVERY page
	 * (the XOTP activity-table modules have no overview page; their lesson menu is the same two-column form: `col-md-6
	 * col-sm-12 > div.item` columns, `h3><span` labels, the trailing prose in the right column). A family carries its
	 * own shell / heading templates / left_match; the composer treats both alike.
	 */
	static #familyFor(run, page) {
		const inq = this.#inquiryFamilyFor(run, page);
		if (inq) return inq;
		const cfg = DataService.Data.EmitTemplates?.menu?.two_col_li?.item_family;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "ITEMMENU_OFF"]) return null;
		const code = String(run?.moduleCode || "").toUpperCase();
		if (!(cfg.code_prefixes ?? []).some((p) => code.startsWith(String(p).toUpperCase()))) return null;
		return cfg;
	}

	static menuTypeFor(page, run) {
		const base = this.#menuTypeForBase(page, run);
		// An Inquiry overview always carries its menu (KB 06 §3.4) — a registry 'none' verdict (CEDW101 / CEDW201 /
		// CEDR204's no-evidence value) becomes the family's none_becomes ('simplified'); tabs and simplified pass through.
		const inq = this.#inquiryFamilyFor(run, page);
		if (inq && base === "none") { if (page) page._inqMenuFromNone = true; return inq.none_becomes ?? "simplified"; }
		return base;
	}

	static #menuTypeForBase(page, run) {
		const scope = page.isOverview ? "overview" : "lesson";
		// PRIMARY: menu_type derived from the human-built modules per subject×phase
		// (the Group Majority — data/Menu_Scaffold_Registry.json, keyed by
		// run.groupKey "subjectLetters|template_phase"). It overrides the
		// Style-Anchor menu_type where the two disagree (e.g. a lesson menu the
		// Style-Anchor would suppress, or one it would add where the human has none).
		// Cascade: audited group value → Style-Anchor value → global default.
		// key = subject letters of the module code + resolved template_phase, the
		// same shape the registry rows use (e.g. "MXFL|4-6").
		const subj = run.moduleCode?.match(/^[A-Za-z]+/)?.[0] ?? "";
		const phase = run.resolvedRules?.template_phase ?? "";
		const ms = DataService.Data.MenuScaffold;
		// The registry rows are PAGE-ROLE-AWARE: lesson evidence comes only from
		// each module's FIRST lesson page, so a family with mostly-empty "1.1,
		// 1.2, ..." continuation pages doesn't get diluted down to a false "none"
		// verdict just because most of its pages are blank continuations (e.g. a
		// module whose lesson pages 1.0-6.0 all carry a Learning-Intentions menu
		// must not be miscounted as menu-less). Env MENUREG_OFF=1 reads the cruder
		// legacy_groups/legacy_series rows instead.
		const legacyReg = typeof process !== "undefined" && process.env && process.env.MENUREG_OFF;
		const regGroups = (legacyReg && ms?.legacy_groups) ? ms.legacy_groups : ms?.groups;
		const regSeries = (legacyReg && ms?.legacy_series) ? ms.legacy_series : ms?.series;
		// Cascade: Series Anchor (this module's own code) → Group Majority
		// (subject×phase) → Style-Anchor → global default.
		const grp = regGroups?.[`${subj}|${phase}`];
		const fromAudit = regSeries?.[run.moduleCode]?.[scope] ?? grp?.[scope];
		if (fromAudit) return ["tabs", "simplified"].includes(fromAudit) ? fromAudit : "none";
		// MENU-LESS FAMILY FALLTHROUGH: if THIS scope (overview or lesson) has no
		// recorded evidence for the module's group, but the OTHER scope's recorded
		// value is an explicit "none", treat the whole family as menu-less rather
		// than falling through to the generic Style-Anchor default below and
		// fabricating a menu the human developers never build. Example: a
		// fundamentals-template subject whose LESSON pages are recorded "none" but
		// whose OVERVIEW page has no recorded value — without this rule the converter
		// would wrongly bolt an extra list menu onto that overview page. This check
		// is deliberately narrow: it only fires when the sibling scope is an
		// EXPLICIT "none", so a family that genuinely does have a menu on one scope
		// (but no recorded value on the other) is left untouched.
		// Data: menu.none_family_fallthrough. Env: MENUNONE_OFF disables this rule.
		const nf = DataService.Data.EmitTemplates?.menu?.none_family_fallthrough;
		if (nf !== false && !(typeof process !== "undefined" && process.env && process.env.MENUNONE_OFF)
			&& grp && (grp[scope] === null || grp[scope] === undefined)) {
			const other = scope === "overview" ? "lesson" : "overview";
			if (grp[other] === "none") return "none";
		}
		const value = (run.resolvedRules?.menu_type ?? {})[scope];
		// "—" / "n/a" / missing = absent by design (as in the ConnectED rows)
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
		// THE TILE-PAGE DIALECT: the level / tile menu is composed from
		// run._levelMenu, which the BODY pre-pass fills — a WJFUN overview's whole
		// LI/SC block sits in the body ([Introduction content] is not a menu
		// boundary), so menuItems is EMPTY here and the early return below would
		// ship the bare two-pane shell. Compose the level tabs first whenever the
		// pre-pass captured them (CHFUN's menuItems are never empty, so its
		// level-pages path is the same branch, reached a few lines earlier).
		if (menuType !== "none" && page?.isOverview && run._levelMenu && !menuItems.length) {
			const lm0 = this.#levelTabs(run._levelMenu);
			if (lm0) {
				run.AddNote("info", "MenuBuilder",
					`Overview menu composed as level tabs (Overview + ${run._levelMenu.levels.map((l) => l.label).join(", ")}; fundamentals_panels.level_pages / tile_pages).`);
				return { kind: menuType, archetype: "writer_tabs", wtNav: lm0.nav, wtPanes: lm0.panes, wtShell: lm0.shell,
					tab1: "", tab2: "", content: "", left: "", right: "" };
			}
		}
		if (menuType === "none" || !menuItems.length) {
			// An Inquiry overview with nothing to put in the menu ships NO menu (ENGFUN02) — menuTypeFor's
			// none_becomes only serves a page that has menu content; an empty shell is never emitted.
			const kind = (!menuItems.length && page?._inqMenuFromNone) ? "none" : menuType;   // only a none→simplified conversion falls back to none; a registry 'simplified' keeps its (empty) shell
			return { kind, tab1: "", tab2: "", content: "", left: "", right: "" };
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
				tpl.fundamentals_overview_li ?? {}, menuType);
			// An in_tabs form (the FRFUN tabs overview) fills the tabs shell's first pane (tabs_two_col)
			if (funCols && funCols.inTabs && menuType === "tabs") {
				// Its Information tab is empty by construction: constraint 67 drops it (menu.info_tab_omission)
				return { kind: menuType, archetype: "tabs", tab1Cols: funCols.slice(), tab2Cols: null,
					dropTab2: this.#infoTabOmitOn(page),
					tab1: "", tab2: "", content: "", left: "", right: "" };
			}
			if (funCols) {
				return { kind: menuType, archetype: "fundamentals_li", funLiCols: funCols,
					tab1: "", tab2: "", content: "", left: "", right: "" };
			}
		}

		// LEVEL-PAGE FUNDAMENTALS TABS (the CHFUN "[PAGE N Novice]"
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
				return { kind: menuType, archetype: "writer_tabs", wtNav: lm.nav, wtPanes: lm.panes, wtShell: lm.shell,
					tab1: "", tab2: "", content: "", left: "", right: "" };
			}
		}

		// MTK DROP-DOWN-MENU BILINGUAL TABS (the PNR101/102/104 family).
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
			// no [TABn] rows: the drop-down tables are the overview-table form — one tab per role heading
			// (dropdown_menu.overview_fallback; env REODROPOVFALL_OFF)
			const ofb = ddCfg.overview_fallback;
			if (ofb && ofb.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[ofb.env ?? "REODROPOVFALL_OFF"])) {
				const tbls = menuItems.filter((it) => it._reoDropdown && it.type === "table").map((t) => ({ ...t, _reoOverviewTab: true }));
				if (tbls.length) {
					const otCfg = DataService.Data.EmitTemplates.elements?.dual_language?.overview_table_tabs ?? {};
					const ot = this.#reoOverviewTabs(tbls, run, norm, otCfg);
					if (ot.count > 1) {
						run.AddNote("info", "MenuBuilder",
							`MTK drop-down menu with no [TABn] rows composed from its tables (${ot.count} tabs: ${ot.labels.join(" | ")}).`);
						return { kind: menuType, archetype: "reo_tabs", reoNav: ot.nav, reoPanes: ot.panes,
							tab1: "", tab2: "", content: "", left: "", right: "" };
					}
				}
			}
		}

		// MTK OVERVIEW-TABLE TABS (the TRR family; KB 07A §4 + 07D §19.1).
		// ContentConverter's #partitionItems captured the writer's overview tables
		// (the table-cell [TITLE BAR] table + one table per menu role) as
		// "_reoOverviewTab"; compose them into the KB's bilingual tabs menu on the
		// same reo_tabs shell the drop-down menu uses. Never declines once tables were captured.
		// Data: elements.dual_language.overview_table_tabs. Env toggle: REOOVTABS_OFF
		// (disables the upstream capture, so this branch is never reached when set).
		if (menuItems.some((it) => it._reoOverviewTab)) {
			const otCfg = DataService.Data.EmitTemplates.elements?.dual_language?.overview_table_tabs ?? {};
			const ot = this.#reoOverviewTabs(menuItems, run, norm, otCfg);
			run.AddNote("info", "MenuBuilder",
				`MTK overview menu composed from the writer's overview tables (${ot.count} tabs: ${ot.labels.join(" | ")}; KB 07A §4).`);
			return { kind: menuType, archetype: "reo_tabs", reoNav: ot.nav, reoPanes: ot.panes,
				tab1: "", tab2: "", content: "", left: "", right: "" };
		}

		// WRITER-AUTHORED MENU TAB PARTITION (as in module ENGJ403).
		// Newer Writers Templates author the overview menu's tab layout
		// EXPLICITLY: a "[please set up as two tabs …][tab 1 – please title as
		// appropriate]" set-up instruction, then the tab-1 sections, "[close tab]",
		// "[tab 2 – …]", the tab-2 sections, "[close tab]" — all BEFORE [MODULE
		// INTRODUCTION]. The human developer builds EXACTLY that partition (ENGJ403:
		// tab 1 = LI/SC + Planning/Get-started/Connections/Assessment in two
		// side-by-side columns under a "Tirohanga Whānui | Overview" banner; tab 2 =
		// Knowledge/Practices in two columns) — but the fold-vocabulary tab_map
		// routing below knows nothing about the markers, so it would re-shuffle
		// sections into the wrong tabs and drop the banner. When the markers are
		// present, honour the writer's own partition instead of the vocabulary routing.
		// The gate (a real [MODULE INTRODUCTION]-bounded menu region + the tabs SET-UP
		// instruction + >=1 [close tab]) is narrow: CEDK101's six bare [tab N] crumbs
		// (no set-up, no closers — the inquiry crumb list, handled via _inquiryCrumb)
		// decline BY CONSTRUCTION.
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
		let archetype = menuType === "tabs" ? "tabs"
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
		// Env MENUCURRIC_OFF turns this whole ENG-family layout off (the plain
		// BLL-shaped output).
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
		let bannerFamily = archetype === "two_col_li"
			&& !engFamily
			&& bannerCfg && bannerCfg.enabled !== false
			&& convention?.banner_h4_span === true
			&& !(typeof process !== "undefined" && process.env && process.env.BANNERMENU_OFF);
		// THE INQUIRY FAMILY (KB 06 §3.4; menu.two_col_li.inquiry_family; env INQFAMILY_OFF): an Inquiry-template
		// OVERVIEW outside the excluded subjects renders the two-column form — the archetype is FORCED to two_col_li (TWHA's
		// 'flat' convention would give it one col-md-8 column), the banner family is off (ConnectED|1-3's mined banner_h4_span),
		// the left headings are h4>span and the shell is two_col_inquiry (paddingR | paddingL, no banner). The ENG offset
		// family and a tabs menu are untouched. See #inquiryFamilyFor.
		const inqCfg = this.#familyFor(run, page);   // the Inquiry family OR the item family
		const inqFamily = !!inqCfg && !engFamily && archetype !== "tabs";
		if (inqFamily) { archetype = "two_col_li"; bannerFamily = false; }
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

		const out = { kind: menuType, archetype, engFamily, bannerFamily, inquiryFamily: inqFamily, familyShell: (inqFamily && inqCfg.shell) || null, bannerLabel: "", tab1: "", tab2: "", content: "", left: "", right: "", tab1Cols: null, tab2Cols: null };

		// OVERVIEW TABS-MENU PANE-1 TWO-COLUMN LAYOUT (e.g. module ENGJ402). The
		// two-column transforms above are all gated to archetype === "two_col_li",
		// so none of them runs inside a "tabs" shell — left alone, pane 1 of a tabs
		// menu would accumulate everything into ONE long column, where the human-built
		// version splits it into TWO columns. When this flag is on, tab-1
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

		// INFORMATION-PANE NATIVE TWO-COLUMN (as in AGH1002). The human lays some
		// groups' Information/Learning pane out in TWO columns (AGH1002: LI + SC +
		// year-planner LEFT | Planning your time + get-started RIGHT) rather than one
		// col-md-8. The column count is a per-subject|phase house style whose
		// within-group discriminator is LI/SC PRESENCE in the pane (AGH's li-carrying
		// panes are two-column, its li-less ones one column; MXEO's li-carrying
		// Learning panes stay ONE column — hence registry-gated, never a global
		// rule). Tab-2 content is recorded here as kind-tagged RUNS (the t1Runs
		// pattern) so the composer below (menu.tab2_cols) can split them into the
		// group's registered column pair. Env INFOCOLS_OFF disables (single
		// accumulated column).
		const t2cfgRaw = tpl.tab2_cols;
		const t2cfg = archetype === "tabs" && page.isOverview
			&& t2cfgRaw && t2cfgRaw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.INFOCOLS_OFF)
			&& !this.isReoModule(run) ? t2cfgRaw : null;
		const t2Runs = [];

		// EXTRA MODULE-MENU TABS (as in module AGH1001's "[Module menu tab rules]").
		// The human-built pages promote SOME overview-menu sections to their OWN
		// nav tabs — AGH1001 ships FOUR tabs (Overview | Information | Connections |
		// Assessment for Learning) where a two-tab shell would dump the Connections
		// + Assessment sections into the Information pane as <h5> subsections. Which
		// sections promote, and what the tab is CALLED, is a per-subject-group
		// house style mined from the
		// human library into menu.extra_tabs.registry (e.g. most NCEA subjects
		// call the assessment tab "Standards" — a word that never appears in the
		// Writers Template). When a tab2-routed heading matches a registered
		// section for this module's group, the walk below opens a NEW pane and
		// the section's content flows into it instead of tab 2.
		// Data: menu.extra_tabs. Env EXTRATABS_OFF disables (sections stay in
		// the Information pane).
		const xtRaw = tpl.extra_tabs;
		const xtCfg = archetype === "tabs" && page.isOverview
			&& xtRaw && xtRaw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.EXTRATABS_OFF)
			&& !this.isReoModule(run) ? xtRaw : null;
		const xtRow = xtCfg ? this.#extraTabRow(run, xtCfg) : null;
		out.extraTabs = null;
		// KB constraint 67 / CL-0040 (data
		// menu.extra_tabs.curriculum_tabs.kb_canonical; env KPTABS_OFF): in the
		// TABBED archetype the Knowledge / Practices sections are ALWAYS their own
		// nav tabs (the canonical Overview → Knowledge → Practices → Information →
		// Standards set) — not only for a registry row that names them (such as
		// SCCH|7-8). A heading qualifies only when its folded text IS the section
		// heading (kb_canonical.heading_pattern), and the subjects the KB leaves on
		// their own archetype (exclude_subjects) keep the registry-only behaviour.
		const kpCfg = xtCfg && xtCfg.curriculum_tabs?.enabled !== false ? xtCfg.curriculum_tabs?.kb_canonical : null;
		const kpSubj = ((run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "").toUpperCase();
		// The BLL2xx readmit (data kb_canonical.readmit; env BLLKPTABS_OFF): a module whose code matches
		// readmit.code_pattern (the BLL2xx series) is taken off exclude_subjects — its tabbed overview gets the
		// canonical Knowledge / Practices tabs like every other subject.
		const kpReadmit = kpCfg?.readmit;
		const kpReadmitted = !!kpReadmit && kpReadmit.enabled !== false && !!kpReadmit.code_pattern
			&& !(kpReadmit.env && typeof process !== "undefined" && process.env && process.env[kpReadmit.env])
			&& new RegExp(kpReadmit.code_pattern, "i").test(String(run.moduleCode || ""));
		const kpRe = kpCfg && kpCfg.enabled !== false && kpCfg.heading_pattern
			&& !(typeof process !== "undefined" && process.env
				&& (process.env[kpCfg.env ?? "KPTABS_OFF"] || process.env.XTABCURRIC_OFF))
			&& (kpReadmitted || !(kpCfg.exclude_subjects ?? []).some((x) => String(x).toUpperCase() === kpSubj))
			? new RegExp(kpCfg.heading_pattern, "i") : null;
		let kpPromoted = false;
		// KB constraint 67 / 01B (data
		// menu.extra_tabs.curriculum_tabs.kb_canonical.standards; env STDTAB_OFF):
		// the TABBED overview's assessment section is the canonical Standards tab
		// even where the registry has no row for this module's subject|phase (a
		// row still decides its own label). Independent of KPTABS_OFF.
		const stdRaw = kpCfg?.standards;
		const stdCfg = stdRaw && stdRaw.enabled !== false
			&& !(typeof process !== "undefined" && process.env
				&& (process.env[stdRaw.env ?? "STDTAB_OFF"] || process.env.XTABCURRIC_OFF))
			&& !(stdRaw.exclude_subjects ?? []).some((x) => String(x).toUpperCase() === kpSubj)
			? stdRaw : null;
		let stdPromoted = false;

		// GENERAL BILINGUAL MENU-HEADING REDUCE. The writer types menu subsection
		// headings bilingually ("Whakamaheretia tō wā | Planning your time"), while
		// most human-built menus keep only the ENGLISH half. The choice is a
		// per-subject-group house style (most groups reduce; a coherent KEEP family
		// — the OSAH/OSOH/OSSC "Online @ home" subjects and a few others — keeps the
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
		let famLastLabel = false;   // the item family — set once the LAST left label (Do) has opened; trailing prose then goes right
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
		// KB c75 "inline → anchor" (data menu.inline_links; env MENULINKS_OFF): the buffered items'
		// own hyperlinks (block.links) travel with their text, so the free-body weave links the writer's phrase in
		// the menu too — AGH1009's Standards tab "Agricultural and Horticultural Science 1.4" → its NCEA page.
		const linksOn = MenuBuilder.#menuLinksOn();
		let linkBuf = [];
		const bufLinks = (it) => { if (linksOn) for (const l of (it?.block?.links ?? [])) if (l?.text && l?.target) linkBuf.push(l); };
		const flushText = () => {
			if (!textBuf.length) return;
			for (const piece of ListsAndRuns.renderBlackText(textBuf.join("\n"), run, linksOn ? linkBuf : [])) push(piece);
			textBuf = [];
			linkBuf = [];
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

		// The family's bare `[Tab N] <label>` markers are the menu's own tab boundaries (menu.writer_tab_markers;
		// env WTABMARK_OFF): a pre-pass rewrites them into the headings the walk below already routes.
		menuItems = this.#writerTabMarkers(menuItems, run, page, tpl, archetype);

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
							// a family's own left_match (the item family's "overview") outranks the consume vocabulary
							const famLeft = (inqFamily && Array.isArray(inqCfg.left_match)) ? inqCfg.left_match : null;
							const famHit = !!famLeft && famLeft.some((m) => folded.startsWith(m));
							if (isLabel(folded) && !famHit) continue;   // section label → consumed
							const left = famHit || (famLeft ?? cfg.left_match).some((m) => folded.startsWith(m));
							const right = (cfg.right_match ?? []).some((m) => folded.includes(m));
							if (famLeft && left) famLastLabel = folded.startsWith(String(famLeft[famLeft.length - 1]));   // past the last left label?
							if (left || right) {
								flushText();   // emit the prior bucket's buffered bullets before switching column
								bucket = left ? "left" : "right";
								push(Utils.FillTemplate(
									left ? (inqFamily ? inqCfg.left_heading : cfg.left_heading) : (inqFamily ? inqCfg.right_heading : cfg.right_heading),   // the Inquiry family's own heading templates
									{ heading: Utils.EscapeHtml(label) }));
								continue;
							}
						}
						// the item family's TRAILING PROSE — a long unlabelled paragraph after the left column's
						// labels moves to the right column (the gold's `col-md-6 col-sm-12 > div.item` right pane holds
						// the Overview row's closing paragraphs; the short "I can" items stay left).
						if (inqFamily && inqCfg.trailing_prose_right && bucket === "left" && famLastLabel && line.trim()
							&& !/^\*\*/.test(line.trim())
							&& line.trim().split(/\s+/).length >= (inqCfg.trailing_prose_min_words ?? 12)) {
							flushText(); bucket = "right";
						}
						if (line.trim()) { textBuf.push(line); bufLinks(it); }   // buffer (grouped at the next label / heading / end)
					}
					continue;
				}
				if (it.text.trim()) { textBuf.push(it.text); bufLinks(it); }   // buffer (grouped at the next heading / table / end)
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
					// overview page, in one of the listed banner subjects, with no
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
					// line as its bold title ([H2] **Understand:** <prose>) would otherwise
					// render as ONE content-glued heading, which dropEmptyHeadings() then
					// deletes outright whenever the next line is another heading (the same
					// failure mode the two_col_li split above handles, in the "tabs" layout).
					// #splitTitleContent splits the bold
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
					// tab whose matched vocabulary entry is LONGEST wins. A simpler rule —
					// "tab 2 wins whenever tab 2 matches and tab 1 doesn't" — would strand a
					// heading in tab 1 just because it happens to contain a short, generic
					// tab-1 word: "What DO I need to get started?" contains the word "do", so
					// the whole get-started section would never reach tab 2 even though tab
					// 2's own much longer, more specific phrase matches exactly (the
					// human-built pages put this content in tab 2).
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
					// section's keep_heading says so (the assessment pane mostly does; the
					// connections pane drops it — the nav label already names it). Tabs
					// appear in document order.
					// CURRICULUM TABS (module SCCH302; data
					// menu.extra_tabs.curriculum_tabs; env XTABCURRIC_OFF): a section
					// whose sections entry carries any_bucket:true (Knowledge /
					// Practices — the SCCH form, whose built sibling SCCH301 ships
					// them as their own nav tabs) is checked for promotion from ANY
					// routed bucket — the tab_map routes those headings to tab 1,
					// where a tab2-only check could never see them. A section without
					// the key keeps the tab2-only behaviour, so every other registered
					// group is untouched BY CONSTRUCTION. A sections entry may also
					// carry its OWN heading_element (the SCCH panes keep an <h4><span>
					// heading; the assessment default stays <h5>).
					const curricOn = xtCfg && xtCfg.curriculum_tabs?.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env.XTABCURRIC_OFF);
					if (xtRow || kpRe || stdCfg) {
						let sec = this.#extraTabSection(hFold, xtCfg);
						let xtLabel = sec && xtRow ? xtRow[sec] : undefined;
						// The KB canonical Knowledge / Practices tab for a
						// module whose registry row does not name the section.
						let kpHit = false, stdHit = false;
						if (!xtLabel && kpRe && kpRe.test(hFold.trim())) {
							const kSec = hFold.includes("knowledge") ? "knowledge" : "practices";
							if (kpCfg.labels?.[kSec]) { sec = kSec; xtLabel = kpCfg.labels[kSec]; kpHit = true; }
						}
						// The KB canonical Standards tab (the tab-2 assessment
						// section) for a module whose registry row does not name it.
						if (!xtLabel && !kpHit && stdCfg && sec === "assessment" && bucket === "tab2") {
							xtLabel = stdCfg.label || "Standards"; stdPromoted = true; stdHit = true;
						}
						if (sec && xtLabel
							&& (bucket === "tab2" || (curricOn && xtCfg.sections?.[sec]?.any_bucket))) {
							if (!out.extraTabs) out.extraTabs = [];
							// A KB-canonical tab LEADS (the c67 order puts
							// Knowledge → Practices BEFORE Information — SkeletonBuilder).
							out.extraTabs.push(kpHit ? { label: xtLabel, html: "", lead: true } : { label: xtLabel, html: "" });
							bucket = "extra:" + (out.extraTabs.length - 1);
							if (kpHit) kpPromoted = true;
							if (xtCfg.sections[sec]?.keep_heading !== false) {
								// A KB-canonical tab titles its pane by CANON (KB c67
								// "label by canon"), never the writer's "Knowledge:" wording.
								const engl = kpHit ? xtLabel
									: (hText.includes("|") ? hText.split("|").pop() : hText).trim();
								push(Utils.FillTemplate(
									(curricOn && xtCfg.sections?.[sec]?.heading_element)
										? xtCfg.sections[sec].heading_element
										: (xtCfg.heading_element ?? "<h5>{heading}</h5>"),
									{ heading: Utils.EscapeHtml(engl) }));
							}
							if (split) for (const p of split.pieces) push(p);
							run.AddNote("info", "MenuBuilder",
								kpHit ? `Menu section "${hText}" promoted to its own "${xtLabel}" nav tab (KB c67 canonical tab set; curriculum_tabs.kb_canonical).`
									: stdHit ? `Menu section "${hText}" promoted to its own "${xtLabel}" nav tab (KB c67 canonical Standards tab; curriculum_tabs.kb_canonical.standards).`
									: `Menu section "${hText}" promoted to its own "${xtLabel}" nav tab (menu.extra_tabs registry).`);
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
							// supplies the <p>. Without it ENGC102's Understand/Know/Do headings would
							// absorb their text and be removed by #dropEmptyHeadings.
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
							// EMPTY left column, as with module CEDO102's Understand/Know/Do
							// heading). This mirrors the eng_family split above, just applied to
							// every other two_col_li family.
							bucket = "left";
							const raw = (it.blackAfter && it.blackAfter.trim()) ? it.blackAfter : headingText;
							const mb = raw.match(/^\s*\*\*([^*]+?)\*\*\s*([\s\S]*)$/);
							// the label keeps the writer's colon in a family whose gold keeps it (menu.two_col_li.label_colon;
							// env LABELCOLON_OFF): typed inside the bold, or as its own bold run right after the label
							const lcCfg = cfg.label_colon;
							const keepColon = !!lcCfg && lcCfg.enabled !== false && !!lcCfg.code_pattern
								&& !(typeof process !== "undefined" && process.env && process.env[lcCfg.env ?? "LABELCOLON_OFF"])
								&& new RegExp(lcCfg.code_pattern, "i").test(String(run?.moduleCode || ""));
							let label, rest = "", typed = false;
							if (mb) {
								typed = /:\s*$/.test(mb[1]);
								label = mb[1].replace(/:\s*$/, "").trim(); rest = mb[2];
								if (keepColon && !typed && /^\s*(?:\*\*)?\s*:/.test(rest)) { typed = true; rest = rest.replace(/^\s*(?:\*\*)?\s*:\s*(?:\*\*)?/, ""); }
							}
							else {
								const ci = headingText.indexOf(":");
								if (ci >= 0 && headingText.slice(ci + 1).trim()) {
									label = headingText.slice(0, ci).trim(); rest = headingText.slice(ci + 1); typed = true;
								} else { typed = /:\s*$/.test(headingText); label = headingText.replace(/:\s*$/, "").trim(); }
							}
							if (keepColon && typed && label) label += ":";
							push(Utils.FillTemplate((inqFamily ? inqCfg.left_heading : cfg.left_heading), { heading: Utils.EscapeHtml(label) }));   // the Inquiry family's h4>span
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
							// menus would otherwise ship "Whāinga Ako | Learning Intentions"
							// piped where the human keeps only the English half) — right bucket
							// only: the piped headings there are all LI/SC/planning (right); the
							// human KEEPS piped left-column curriculum strands where they occur
							// (MXFL202 gold), so the left column is never touched.
							const htext = (((bannerFamily && bannerCfg.reduce_bilingual) || bhr)
								&& bucket === "right" && headingText.includes("|"))
								? headingText.split("|").pop().trim() : headingText;
							push(Utils.FillTemplate(
								bucket === "left" ? (inqFamily ? inqCfg.left_heading : cfg.left_heading) : (inqFamily ? inqCfg.right_heading : cfg.right_heading),   // the Inquiry family's own heading templates
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
				if (it.blackAfter.trim()) { textBuf.push(it.blackAfter); bufLinks(it); }
				continue;
			}

			// anything else: render its black content in place
			const text = it.blackAfter ?? "";
			if (text.trim()) { textBuf.push(text); bufLinks(it); }
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
		// only the Understand/Know/Do curriculum. The two-tab Overview|Learning
		// form belongs to ENGS102 + the MXEO overviews (both phase groups);
		// SSOG301's four-tab Learning INSERT is a one-module form with no
		// registry row. The golds also DELETE the writer's planning/connections/
		// assessment sections — that deletion has no WT discriminator
		// (byte-similar sections are KEPT by other subjects' golds), so the
		// writer's info content is RETAINED below the moved LI/SC. When the
		// pane-1 partition already moved the LI/SC to tab 2 (ENGS102's
		// curric_split) only the label changes; otherwise the LI/SC runs are
		// extracted from pane 1 here, re-emitted at the pane-1 row's li_level
		// (the gold-matched <h5>).
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
		// t2cfg declaration above for the rule). Runs LAST of the tab-2
		// shapers, and only when nothing already composed columns (the
		// moved-LI/SC two-col path and the learning-tab path win first —
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
		// FIRES only when the pane holds >=1 li/sc-family group (the
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
		// GENERAL MENU ITALIC STRIP. The human strips <i>/<em> from module-menu
		// items almost always — a clean rule that holds specifically for the MENU
		// region (body/activity/table content is stripped inconsistently, and
		// acknowledgements content always keeps it — so this rule is deliberately
		// scoped to menus only). The family-specific strips above only cover the
		// ENG/banner curriculum PANES; this generalises the same cleanup to EVERY
		// pane in EVERY family. Text content is always preserved — only the
		// wrapper tags are removed. Font-Awesome icon markup (<i class="fa...">)
		// is never touched. EXCLUDES reo/bilingual modules (TRR/PNR prefix, or
		// reoTranslate body class) — there the human KEEPS italic styling on BOTH
		// panes (the Māori line AND its English translation).
		// Data: menu.strip_italic_all. Env MENUITALIC_OFF limits this to the
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
		// before the next heading/end is omitted (the human developers almost
		// never keep one; menu_empty_heading_rule). Applies to every bucket/archetype.
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
		// CURRICULUM TABS (module SCCH302; env XTABCURRIC_OFF): a registry row
		// carrying _drop_empty_tab2 drops the shell's Information nav item + pane
		// when every routed section promoted away and no tab-2 content remains —
		// the built sibling SCCH301's gold nav is Overview | Knowledge | Practices,
		// with NO Information tab. ROW-scoped: a group without the flag keeps its
		// Information tab through the {tab2Nav}/{tab2Pane} shell slots' defaults in
		// SkeletonBuilder.
		// THE INFORMATION TAB IS NEVER DROPPED WHILE IT HOLDS THE MOVED LEARNING INTENTIONS. A `curric_split`
		// row moves the overview's LI / SC to tab 2 as `tab2Cols`; the three drops below read `out.tab2` only, so once the
		// tab's native section is promoted away (MXFL401's Assessment → Standards) the LI / SC would be dropped with the tab
		// (constraint 1; KB c67's omission rule removes an ABSENT pane). Data menu.extra_tabs.tab2_moved_guard; env T2KEEP_OFF.
		const t2g = xtCfg?.tab2_moved_guard;
		const t2ColsHeld = !!t2g && t2g.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[t2g.env ?? "T2KEEP_OFF"])
			&& Array.isArray(out.tab2Cols) && out.tab2Cols.some((c) => c && c.html && c.html.trim());
		if (t2ColsHeld && out.extraTabs) run.AddNote("info", "MenuBuilder",
			"Information tab kept — it holds the overview's moved learning intentions / success criteria (menu.extra_tabs.tab2_moved_guard).");
		if (out.extraTabs && !t2ColsHeld && xtRow && xtRow._drop_empty_tab2
			&& xtCfg.curriculum_tabs?.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.XTABCURRIC_OFF)
			&& !(out.tab2 && out.tab2.trim())) {
			out.dropTab2 = true;
			run.AddNote("info", "MenuBuilder",
				"Empty Information tab dropped — every menu section promoted to its own tab (menu.extra_tabs registry, _drop_empty_tab2).");
		} else if (out.extraTabs && !t2ColsHeld && kpPromoted && kpCfg.drop_empty_tab2
			&& !(out.tab2 && out.tab2.trim())) {
			// KB c67 omission rule — absent content → remove BOTH the <li> and the
			// pane (env KPTABS_OFF): the Information tab the canonical Knowledge /
			// Practices promotions emptied is dropped, as for the registry rows above.
			out.dropTab2 = true;
			run.AddNote("info", "MenuBuilder",
				"Empty Information tab dropped — the KB c67 omission rule after the canonical Knowledge / Practices promotions (curriculum_tabs.kb_canonical).");
		} else if (out.extraTabs && !t2ColsHeld && stdPromoted && stdCfg.drop_empty_tab2
			&& !(out.tab2 && out.tab2.trim())) {
			// KB c67 omission rule (env STDTAB_OFF): the Information tab
			// the canonical Standards promotion emptied is dropped.
			out.dropTab2 = true;
			run.AddNote("info", "MenuBuilder",
				"Empty Information tab dropped — the KB c67 omission rule after the canonical Standards promotion (curriculum_tabs.kb_canonical.standards).");
		}
		// Constraint 67's omission rule (data menu.info_tab_omission; env INFOTABOMIT_OFF): an Information tab that
		// was EMPTY to begin with (no promotion emptied it) is dropped too — the nav <li> and the pane both go.
		if (!out.dropTab2 && menuType === "tabs" && !t2ColsHeld && this.#infoTabOmitOn(page)
			&& this.#paneBlank(out.tab2) && !(Array.isArray(out.tab2Cols) && out.tab2Cols.some((c) => !this.#paneBlank(c?.html)))) {
			out.dropTab2 = true;
			run.AddNote("info", "MenuBuilder",
				"Empty Information tab dropped — the KB c67 omission rule: the Writers Template supplies no content for it (menu.info_tab_omission).");
		}
		// LESSON-MENU "Learning intentions" LABEL (as in module ENGJ403). The human
		// developers open a LESSON page's simplified menu with a GENERATED "Learning
		// intentions" label heading (`<h5>Learning intentions</h5>` before the "We
		// are learning:" lead) in specific subject|phase families — the label is NOT
		// in the Writers Template (ENGJ403's lesson regions carry only the WALT/I-can
		// lines), so this is a registry-driven generated label, like the fundamentals
		// funLi label. A registry row exists where the gold lesson menus of a
		// subject|phase group (grouped by the ENGINE-resolved subject|phase)
		// consistently carry the label AND the lesson menu type is "simplified" (the
		// h3-form families MXDB/MXFUN/SSCI build their menus through different
		// machinery and have no row). GUARDS: lesson pages only, non-empty composed
		// menu, and never when the menu already carries a "learning intention"
		// heading (double-emission-safe by construction, whatever path produced it).
		// Data: menu.lesson_li_label (registry + per-row element/label).
		// Env toggle: MENULILABEL_OFF.
		{
			const llCfg = tpl.lesson_li_label;
			const llOn = llCfg && llCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.MENULILABEL_OFF)
				&& !page.isOverview && out.content && out.content.trim();
			if (llOn) {
				// THE FIRST-IN-SERIES DEFAULT ROW (as in module SCCH302). A brand-new
				// subject has no gold-built sibling, so no group row can ever exist for
				// it — but its lesson menu still needs the label the design team uses for
				// new subjects, in the MODERN form <h4><span>Learning Intentions</span></h4>.
				// The default row fires ONLY when no registry row matched AND the resolver
				// set run.registryDefaultsApplied (the universal-field evidence floor's
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
	/**
	 * THE WRITER'S BARE TAB MARKERS (a family dialect; data menu.writer_tab_markers.families; env WTABMARK_OFF).
	 * On a tabbed overview menu of a family with a row, rewrites the item list before the walk:
	 *  - `[Tab 1] <label>`: the label names the pane and is consumed; an LI label (li_label_pattern) with no heading right
	 *    after it becomes that heading (heading_tag) — the pane's Learning Intentions label;
	 *  - `[Tab N≥2] <label>`: an assessment heading typed right after it promotes the section itself (the marker is
	 *    consumed); otherwise a label or first line that reads as the Assessment-for-Learning section (assessment_pattern /
	 *    assessment_cue_pattern — KB 01B's phrasings) becomes the canonical heading, which the Standards-tab rule promotes;
	 *    any other tab marker is left as it was;
	 *  - a table right after an item matching placeholder_note_pattern (the template's own placeholder box) is dropped.
	 * @returns {Array} the (possibly rewritten) menu items
	 */
	static #writerTabMarkers(menuItems, run, page, tpl, archetype) {
		const cfg = tpl.writer_tab_markers;
		if (!cfg || cfg.enabled === false || archetype !== "tabs" || !page.isOverview) return menuItems;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "WTABMARK_OFF"]) return menuItems;
		const subj = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const fam = cfg.families?.[subj];
		if (!fam) return menuItems;
		const fold = (s) => Utils.Fold(String(s ?? "")).replace(/[*_]/g, "").replace(/\s+/g, " ").trim();
		const isHeading = (x) => x?.type === "tag" && ["h1", "h2", "h3", "h4", "h5", "heading"].includes(x.parse?.primary?.tag);
		const liRe = new RegExp(fam.li_label_pattern ?? "^learning intentions?$", "i");
		const asRe = new RegExp(fam.assessment_pattern ?? "^(?:standards?|assessment)\\b", "i");
		const cueRe = fam.assessment_cue_pattern ? new RegExp(fam.assessment_cue_pattern, "i") : null;
		const phRe = fam.placeholder_note_pattern ? new RegExp(fam.placeholder_note_pattern, "i") : null;
		const nextOf = (i) => {
			for (let j = i + 1; j < menuItems.length; j++) {
				const x = menuItems[j];
				if (x.type === "black" && !String(x.text ?? "").trim()) continue;
				return j;
			}
			return -1;
		};
		const hTag = fam.heading_tag ?? "h3";
		const asHeading = (src, text) => ({ ...src, text: "", blackAfter: text,
			parse: { ...(src.parse ?? {}), class: "tag", remainders: [], instructionFragment: null,
				primary: { ...(src.parse?.primary ?? {}), tag: hTag, fragment: hTag } } });
		const out = [];
		let dropAt = -1, n = 0;
		for (let i = 0; i < menuItems.length; i++) {
			const it = menuItems[i];
			if (i === dropAt) { n++; continue; }
			if (phRe && it.type === "tag" && phRe.test(`${it.text ?? ""} ${it.blackAfter ?? ""}`)) {
				const j = nextOf(i);
				if (j > 0 && menuItems[j].type === "table") dropAt = j;
				out.push(it);
				continue;
			}
			if (it.type !== "tag" || it.parse?.primary?.tag !== "tab n") { out.push(it); continue; }
			const num = parseInt(String(it.parse.primary.fragment ?? "").match(/\d+/)?.[0] ?? "1", 10);
			const label = fold(it.blackAfter);
			const j = nextOf(i);
			const nx = j >= 0 ? menuItems[j] : null;
			n++;
			if (num <= 1) {
				if (label && liRe.test(label) && !isHeading(nx)) out.push(asHeading(it, String(it.blackAfter).replace(/\*/g, "").trim()));
				continue;
			}
			if (isHeading(nx) && asRe.test(fold(nx.blackAfter || (nx.parse?.remainders ?? []).join(" ")))) continue;
			const nxText = nx ? fold(nx.type === "black" ? nx.text : nx.blackAfter) : "";
			if ((label && asRe.test(label)) || (cueRe && cueRe.test(nxText))) {
				out.push(asHeading(it, fam.assessment_heading ?? "Assessment for Learning"));
				continue;
			}
			n--;
			out.push(it);
		}
		if (n) run.AddNote("info", "MenuBuilder", `${n} writer tab marker(s) / placeholder box read as the menu's own tab boundaries (menu.writer_tab_markers).`);
		return out;
	}

	/**
	 * Is constraint 67's Information-tab omission rule on for this page
	 * (data menu.info_tab_omission: enabled, page_types; env INFOTABOMIT_OFF)?
	 */
	static #infoTabOmitOn(page) {
		const c = DataService.Data.EmitTemplates.menu?.info_tab_omission;
		if (!c || c.enabled === false) return false;
		if (typeof process !== "undefined" && process.env && process.env[c.env ?? "INFOTABOMIT_OFF"]) return false;
		return (c.page_types ?? ["overview"]).includes(page.isOverview ? "overview" : "lesson");
	}

	/**
	 * A menu pane with no content: no text once tags are stripped, and no
	 * image, iframe or table (a pane holding only media is content).
	 */
	static #paneBlank(html) {
		const h = String(html ?? "");
		if (/<(img|iframe|table|video|audio)\b/i.test(h)) return false;
		return !h.replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").trim();
	}

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
			// A row may name its own LI / SC heading form (the PWY|NCEA row: h4 > span)
			return Utils.FillTemplate(row.li_sc_heading ?? cfg.li_sc_heading ?? "<h{level}>{heading}</h{level}>",
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
	 *     (an "Understand, Know | Do" split is the dominant shape)
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
		// A row may carry its own env (the PWY|NCEA family row turns off with WTABMARK_OFF)
		if (row.env && typeof process !== "undefined" && process.env && process.env[row.env]) return null;

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
		// menu.tab2_cols composer, which interleaves the moved LI/SC
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
	static fundamentalsLiRow(run, cfg, menuType) {
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
		// A block_capture row (the FRFUN family) carries one form per menu type (by_menu_type: cols of 1 or 2,
		// lead_tag, optional labels, in_tabs); it declines when fundamentals_overview_li.block_capture is off (env FUNBLOCK_OFF)
		// or the page's menu type has no form — the plain two-column behaviour for that module.
		if (row && row.block_capture) {
			const bc = cfg?.block_capture;
			if (!bc || bc.enabled === false
				|| (typeof process !== "undefined" && process.env && process.env[bc.env ?? "FUNBLOCK_OFF"])) return null;
			const form = row.by_menu_type?.[menuType];
			if (!form || !Array.isArray(form.cols) || (form.cols.length !== 1 && form.cols.length !== 2)) return null;
			return { ...row, ...form, block_capture: true };
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
	static #fundamentalsOverviewLi(menuItems, run, page, norm, cfg, menuType) {
		if (!page.isOverview || this.isReoModule(run)) return null;
		const row = this.fundamentalsLiRow(run, cfg, menuType);
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
			// A LABEL heading (fundamentals_overview_li.label_headings) opens its column and renders nothing itself
			// (the registry's generated heading is the label); that column keeps its lines verbatim (see build below)
			if (it._funLiLabel) {
				side = it._funLiLabel;
				if (side === "sc") sawSc = true; else sawWalt = true;
				sides[side].labelled = true;
				continue;
			}
			if (it.type === "black") { takeLines(it.text); continue; }
			if (it.type !== "tag") continue;
			const p = it.parse?.primary;
			if (!p || it.parse?.class === "instruction" || it.parse?.class === "noise") {
				// non-structural red: an instruction surfaces as the standard CS note in its
				// column (never silently stripped); a noise span renders nothing itself
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
		// A block_capture form (the FRFUN family): each side is its lead line as row.lead_tag (<h5>) + its
		// bullets, an optional generated label first; one col holds both sides, two cols split them LI | SC
		if (row.block_capture) {
			const side = (key, labelHtml) => {
				const lines = sides[key].lines.slice();
				if (!lines.length) return null;
				let lead = lines[0].replace(/[*_]/g, "").replace(/[\p{So}️]/gu, "").trim();
				if (cfg.lead_colon_normalise !== false) lead = lead.replace(/[\s.:…]+$/u, "").trim() + ":";
				const tag = row.lead_tag || "h5";
				const rest = lines.length > 1 ? ListsAndRuns.renderBlackText(lines.slice(1).join("\n"), run) : [];
				if (!rest.length) return null;
				// the general menu italic strip + the empty-heading guard on the side's own lines; the generated label is
				// prepended after it (a label directly above the <h5> lead is the gold's form, not an empty section)
				const body = this.dropEmptyHeadings(this.stripTextItalic(
					[`<${tag}>${Utils.EscapeHtml(lead)}</${tag}>`, ...rest, ...sides[key].flags].join("\n")), run);
				if (!body.trim()) return null;
				return [labelHtml, body].filter(Boolean).join("\n");
			};
			const li = side("li", row.li_heading || "");
			const sc = side("sc", row.sc_heading || "");
			if (!li || !sc) return null;
			run.AddNote("info", "MenuBuilder",
				"Fundamentals [Overview] WALT / I-can block routed to the module menu (menu.fundamentals_overview_li.block_capture).");
			const out = row.cols.length === 1
				? [{ cls: row.cols[0], html: li + "\n" + sc }]
				: [{ cls: row.cols[0], html: li }, { cls: row.cols[1], html: sc }];
			if (row.in_tabs) out.inTabs = true;
			return out;
		}
		const build = (key, labelHtml) => {
			let lines = sides[key].lines.slice();
			if (cfg.lead_colon_normalise !== false && lines.length && !sides[key].labelled) {   // a labelled column has no lead line
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
	 * body class, OR the TRR/PNR module-code prefixes (covers every
	 * bilingual module in the library).
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
	 * drop-down-menu table (the PNR101/102/104 family).
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
	 *  - a [TITLE BAR] row is skipped (its payload is empty in these templates;
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

			// [TITLE BAR] row — payload empty in these templates; skipped
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
	 * Reads one MTK overview table's ROLE (the TRR family). Walks the
	 * rows (English = column 1, Māori = column 2; the PR1 / PR2 review columns are
	 * ignored, KB 07A §2), skipping the "English | Māori" divider row, notes a
	 * [TITLE BAR] row, and matches the FIRST heading row's text (English, then
	 * Māori) against overview_table_tabs.roles (Overview / Strand / Dispositions /
	 * Key objectives / Critical Point / Learning Intentions / Information).
	 *
	 * @param {Object} tbl - a table item (tbl.block.rows)
	 * @param {TagNormaliser} norm - unused (kept for the call shape)
	 * @param {Object} cfg - the overview_table_tabs data block
	 * @returns {{titleBar: boolean, role: string|null, def: Object|null}|null}
	 *   null = not an overview table at all (no title bar, first content row not a role heading)
	 */
	static reoOverviewTableRole(tbl, norm, cfg) {
		const rows = tbl?.block?.rows ?? [];
		let titleBar = false;
		for (const row of rows) {
			if (!Array.isArray(row) || !row.length) continue;
			const E = this.#mtkLead(row[0]), R = this.#mtkLead(row[1]);
			const tags = [...E.tags, ...R.tags].map((t) => this.#mtkFold(t));
			if (tags.includes("title bar")) { titleBar = true; continue; }
			if (this.#mtkDivider(E, R)) continue;
			if (!E.text && !R.text && !tags.length) continue;
			const lvl = this.#mtkLevel(tags);
			const def = lvl !== null ? this.#mtkRole(E.text, R.text, cfg)
				: (!tags.length ? this.#mtkUntaggedRole(E.text, R.text, cfg) : null);
			if (def) return { titleBar, role: def.role, def };
			// no role: report the first heading's folded text (the [H1] TRR900 introduction table)
			const first = lvl !== null ? this.#mtkFold(TablesAndGrids.cellParts(E.text || R.text)[0] ?? "") : null;
			return (titleBar || first !== null) ? { titleBar, role: null, def: null, first } : null;
		}
		return titleBar ? { titleBar, role: null, def: null } : null;
	};

	// ---- the MTK overview-table helpers --------------------------------------
	static #mtkLead(cell) {
		let t = String(cell ?? "").replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "").trim();
		const tags = [];
		let m;
		// leading [tags], and a leading "/" line separator between them ("[H3] / [Body] In the first …", TRR103)
		while ((m = t.match(/^(?:\[([^\]]*)\]|\/)\s*/))) { if (m[1] !== undefined) tags.push(m[1].trim()); t = t.slice(m[0].length); }
		return { tags, text: t.trim(), raw: String(cell ?? "") };
	};
	static #mtkFold(s) {
		return Utils.Fold(String(s ?? "").replace(/\*/g, " ")).replace(/\s+/g, " ").trim();
	};
	static #mtkLevel(foldedTags) {
		for (const t of foldedTags) { const m = t.match(/^h\s*(\d)$/); if (m) return parseInt(m[1], 10); }
		return null;
	};
	static #mtkDivider(E, R) {
		const e = this.#mtkFold(E.text), r = this.#mtkFold(R.text);
		return !E.tags.length && !R.tags.length && (e || r)
			&& (e === "english" || e === "") && (r === "maori" || r === "te reo maori" || r === "");
	};
	static #mtkRole(engText, reoText, cfg) {
		const first = (s) => this.#mtkFold(TablesAndGrids.cellParts(s)[0] ?? "");
		const e = first(engText), r = first(reoText);
		for (const def of cfg.roles ?? []) {
			const re = new RegExp(def.match, "i");
			if ((e && re.test(e)) || (r && re.test(r))) return def;
		}
		return null;
	};
	// an UNTAGGED label row may name only the untagged_roles (TRR304 types "Ngā Whenu Ngā Toi
	// Mokopuna Ngā Whāinga Matua / Strands Dispositions" with no [H] tag) — never Overview /
	// Information, whose words open ordinary prose too
	static #mtkUntaggedRole(engText, reoText, cfg) {
		const def = this.#mtkRole(engText, reoText, cfg);
		return def && (cfg.untagged_roles ?? []).includes(def.role) ? def : null;
	};

	/**
	 * Composes the MTK overview menu from the writer's overview TABLES (the TRR
	 * family; KB 07A §4 "Module Menu Tabs" + the 07D §19.1 skeleton).
	 *
	 * ONE TAB PER ROLE, in the writer's order:
	 *  - a table's first heading row names its role and is the tab's nav label only
	 *    (the role's KB label when overview_table_tabs.roles gives one, else the
	 *    writer's own heading) — it is NOT repeated inside the pane, except for a
	 *    role with render_heading (Learning Intentions: the KB's `<h4><span>`);
	 *    the label row's later "/"-lines ("Learning focuses on") render as body;
	 *  - the KB's 5-TAB DEFAULT: a Critical Point table directly after the Key
	 *    objectives pane continues THAT pane (its heading not rendered; its [H2]s
	 *    are the pane's h5s) — merge_critical_into_previous;
	 *  - inside the Overview (title-bar) table a later role heading opens its own
	 *    pane (TRR112 types Key objectives / LI / SC inside the title-bar table);
	 *  - every other heading row → a reo/eng PAIR: section_heading_match (Learning
	 *    Intentions / Success Criteria) → heading_section `<h4><span>`, else
	 *    heading_lead `<h5>` — the Overview pane keeps the writer's bold (`<h5><b>`,
	 *    KB), the other panes plain text;
	 *  - body rows → BilingualBuilder.bilingualSplit pairs, Māori first; a
	 *    "[Checklist]" token is dropped and ☒ / ☐ lines become bullets (the human
	 *    keeps both — TRR114);
	 *  - a pane holding any two_column_match heading is the KB's two-column
	 *    Learning-Intentions layout (col_pane paddingR | col_split paddingL), split
	 *    at the first column_split_match heading once the left column has content;
	 *    every other pane is col_single.
	 *
	 * @returns {{nav: string, panes: string, count: number, labels: string[]}}
	 */
	static #reoOverviewTabs(menuItems, run, norm, cfg) {
		const tables = menuItems.filter((it) => it._reoOverviewTab);
		const sectionRe = new RegExp(cfg.section_heading_match ?? "^(learning intentions|success criteria)\\b", "i");
		const splitRe = new RegExp(cfg.column_split_match ?? "^(planning your time|what do i need)", "i");
		const twoColRe = new RegExp(cfg.two_column_match ?? "^(learning intentions|success criteria|planning your time)", "i");
		const clean = (s) => String(s ?? "").replace(/\*\*/g, "").replace(/^\*+|\*+$/g, "").trim();
		const firstPart = (s) => TablesAndGrids.cellParts(s)[0] ?? "";
		const restParts = (s) => TablesAndGrids.cellParts(s).slice(1).join(" / ");
		const pre = (cell) => {
			let c = String(cell ?? "");
			for (const tok of cfg.drop_tokens ?? []) c = c.split(tok).join("");
			return c.replace(/[☒☐]\s*/gu, "• ");
		};
		const panes = [];
		let pane = null, col = null;
		const newPane = (role, label) => {
			pane = { role, label, cols: [[]], twoCol: false };
			col = pane.cols[0];
			panes.push(pane);
		};
		const pushPair = (reoHtml, engHtml) => {
			if (reoHtml) col.push(BilingualBuilder.langAttr(reoHtml, "reo"));
			if (engHtml) col.push(BilingualBuilder.langAttr(engHtml, "eng"));
		};
		const pushBody = (reoCell, engCell) => {
			const Rr = BilingualBuilder.bilingualSplit(pre(reoCell), run, norm);
			const Ee = BilingualBuilder.bilingualSplit(pre(engCell), run, norm);
			const n = Math.max(Rr.text.length, Ee.text.length);
			for (let k = 0; k < n; k++) pushPair(Rr.text[k], Ee.text[k]);
			for (const m of (Rr.media.length ? Rr.media : Ee.media)) col.push(m);
		};
		const pushHeading = (E, R) => {
			const eT = firstPart(E.text), rT = firstPart(R.text);
			const eF = this.#mtkFold(eT), rF = this.#mtkFold(rT);
			if (twoColRe.test(eF) || twoColRe.test(rF)) pane.twoCol = true;
			if (pane.cols.length === 1 && col.length && (splitRe.test(eF) || splitRe.test(rF))) {
				pane.cols.push([]);
				col = pane.cols[1];
			}
			const tpl = (sectionRe.test(eF) || sectionRe.test(rF))
				? (cfg.heading_section ?? "<h4><span>{text}</span></h4>")
				: (cfg.heading_lead ?? "<h5>{text}</h5>");
			const txt = (s) => (pane.role === "overview" && cfg.overview_heading_inline !== false)
				? ListsAndRuns.inlineMarkup(String(s).trim())
				: Utils.EscapeHtml(clean(s));
			pushPair(rT ? Utils.FillTemplate(tpl, { text: txt(rT) }) : "", eT ? Utils.FillTemplate(tpl, { text: txt(eT) }) : "");
			const eRest = restParts(E.text), rRest = restParts(R.text);
			if (eRest || rRest) pushBody(rRest, eRest);
		};
		const labelOf = (def, E, R) => def?.label
			? { eng: def.label.eng, reo: def.label.reo }
			: { eng: clean(firstPart(E.text)).replace(/:\s*$/, ""), reo: clean(firstPart(R.text)).replace(/:\s*$/, "") };

		for (const tbl of tables) {
			let tableLabelSeen = false;
			for (const row of tbl.block?.rows ?? []) {
				if (!Array.isArray(row) || !row.length) continue;
				const E = this.#mtkLead(row[0]), R = this.#mtkLead(row[1]);
				const tags = [...E.tags, ...R.tags].map((t) => this.#mtkFold(t));
				if (tags.includes("title bar")) continue;
				if (this.#mtkDivider(E, R)) continue;
				const lvl = this.#mtkLevel(tags);
				const isHeading = lvl !== null && (E.text || R.text);
				// the table's first content row may be an UNTAGGED role label (TRR304): it opens the
				// pane like a heading does; its later "/"-parts are the writer's label text, not body
				const untagged = !isHeading && !tableLabelSeen && !tags.length && (E.text || R.text)
					? this.#mtkUntaggedRole(E.text, R.text, cfg) : null;
				if (untagged) {
					tableLabelSeen = true;
					newPane(untagged.role, labelOf(untagged, E, R));
					continue;
				}
				if (isHeading) {
					const def = (!tableLabelSeen || pane?.role === "overview") ? this.#mtkRole(E.text, R.text, cfg) : null;
					const opening = def && (!tableLabelSeen || def.role !== "overview");
					tableLabelSeen = true;
					if (opening) {
						if (def.role === "critical" && cfg.merge_critical_into_previous !== false
							&& pane && pane.role === "key_objectives") {
							const eRest = restParts(E.text), rRest = restParts(R.text);
							if (eRest || rRest) pushBody(rRest, eRest);
							continue;   // KB 5-tab: Critical Point continues the Key objectives pane
						}
						newPane(def.role, labelOf(def, E, R));
						if (def.render_heading) pushHeading(E, R);
						else {
							const eRest = restParts(E.text), rRest = restParts(R.text);
							if (eRest || rRest) pushBody(rRest, eRest);
						}
						continue;
					}
					if (!pane) newPane("overview", cfg.overview_label ?? { eng: "Overview", reo: "Tirohanga whānui" });
					pushHeading(E, R);
					continue;
				}
				if (!E.text && !R.text) continue;
				if (!pane) newPane("overview", cfg.overview_label ?? { eng: "Overview", reo: "Tirohanga whānui" });
				pushBody(row.length > 1 ? row[1] : "", row[0]);
			}
		}
		if (!panes.length) newPane("overview", cfg.overview_label ?? { eng: "Overview", reo: "Tirohanga whānui" });

		const colTpl = cfg.col_template ?? "<div class=\"{cls}\">\n{content}\n</div>";
		const nav = panes.map((p) => Utils.FillTemplate(
			cfg.nav_item ?? "\n<li><a><span reo>{reo}</span><span eng>{eng}</span></a></li>",
			{ reo: Utils.EscapeHtml(p.label.reo ?? ""), eng: Utils.EscapeHtml(p.label.eng ?? "") })).join("");
		const panesHtml = panes.map((p) => {
			const colsHtml = p.cols.map((c, ci) => Utils.FillTemplate(colTpl, {
				cls: !p.twoCol ? (cfg.col_single ?? "col-md-8 col-12")
					: (ci === 0 ? (cfg.col_pane ?? "col-md-6 offset-md-0 col-12 paddingR")
						: (cfg.col_split ?? "col-md-6 offset-md-0 col-12 paddingL")),
				content: c.join("\n"),
			})).join("\n");
			return Utils.FillTemplate(
				cfg.pane_template ?? "\n<div class=\"tab-pane\">\n<div class=\"row\">\n{cols}\n</div>\n</div>",
				{ cols: colsHtml });
		}).join("");
		return { nav, panes: panesHtml, count: panes.length, labels: panes.map((p) => p.label.eng) };
	};

	/**
	 * WRITER-AUTHORED MENU TAB PARTITION (as in module ENGJ403; see the
	 * buildMenu branch that calls this). Detects newer Writers Templates' explicit
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
	 *   two kinds as the tab2_cols registry, here decided by pane;
	 * - a short WALT/I-can lead line directly under an LI/SC heading renders
	 *   via lead_element (<h5>, the ENGJ403 human form) instead of a <p>;
	 * - piped bilingual headings are kept WHOLE (keep_bilingual_headings —
	 *   the human keeps "Whakamaheretia tō wā | Planning your time");
	 * - a heading BEFORE the set-up item becomes the pane-1 BANNER
	 *   ("Tirohanga Whānui | Overview" as <h3><span> in a full-width col);
	 * - an instruction span still flags/omits via NotesAndComments.redFlag
	 *   (so the "In this section outline any connections…" template prompt
	 *   is dropped by the omit list, matching the human);
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
	 * Composes the LEVEL-PAGE fundamentals menu (the CHFUN
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
		// The tile-page dialect: the Overview pane may take its own column
		// set (the gold's WJFUN Overview pane is the two-column Knowledge | Practices
		// form while its tile panes are ONE column) — registry row `menu_cols_overview`.
		const ovCols = row.menu_cols_overview || cols;
		const listHtml = (bucket) => {
			const parts = [];
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
			// A bucket's trailing paragraph(s) after its list (the tile
			// dialect's "Learning Intentions and Success criteria are included in
			// each tile." line under the Practices bullets)
			for (const t of (bucket && bucket.tail) || []) if (t) parts.push(`<p>${Utils.EscapeHtml(t)}</p>`);
			return parts;
		};
		const colHtml = (bucket, label) =>
			[Utils.FillTemplate(mc.heading_template || "<h5>{label}</h5>", { label: Utils.EscapeHtml(label) }), ...listHtml(bucket)].join("\n");
		const colT = mc.col_template || "<div class=\"{cls}\">\n{content}\n</div>";
		const pane = (li, sc, c) =>
			(mc.pane_open || "\n<div class=\"tab-pane\">\n<div class=\"row\">") + "\n"
			+ Utils.FillTemplate(colT, { cls: c[0], content: colHtml(li, liLabel) }) + "\n"
			+ Utils.FillTemplate(colT, { cls: c[1] ?? c[0], content: colHtml(sc, scLabel) })
			+ (mc.pane_close || "\n</div>\n</div>");
		// menu.pane_form "single_col": a level / tile pane is ONE column
		// holding the LI heading, the LI lead + bullets, then the SC lead + bullets
		// (the gold's WJFUN tile pane: <h5>Learning Intentions</h5><p>We are
		// learning:</p><ul>…</ul><p>I can:</p><ul>…</ul>). The Overview pane keeps
		// the two-column form under its own labels.
		const paneSingle = (li, sc, c) =>
			(mc.pane_open || "\n<div class=\"tab-pane\">\n<div class=\"row\">") + "\n"
			+ Utils.FillTemplate(colT, { cls: c[0], content: [
				Utils.FillTemplate(mc.heading_template || "<h5>{label}</h5>", { label: Utils.EscapeHtml(mc.li_label_default || "Learning Intentions") }),
				...listHtml(li), ...listHtml(sc)].join("\n") })
			+ (mc.pane_close || "\n</div>\n</div>");
		const levelPane = mc.pane_form === "single_col" ? paneSingle : pane;
		const navItem = (label) => Utils.FillTemplate(mc.nav_item || "\n<li><a>{label}</a></li>",
			{ label: Utils.EscapeHtml(label) });
		// A registry row with menu_omit_empty_overview (the JPFUN family) ships NO Overview tab when the module has no
		// LI / SC of its own — the gold's menu is the level tabs alone (level_pages.level_menu_tabs; env LEVELMENUTABS_OFF)
		const omitOv = row.menu_omit_empty_overview === true && !hasContent(mod.li) && !hasContent(mod.sc)
			&& levels.some((l) => hasContent(l.li) || hasContent(l.sc))
			&& !(typeof process !== "undefined" && process.env && process.env[(cfg.level_menu_tabs && cfg.level_menu_tabs.env) || "LEVELMENUTABS_OFF"]);
		let nav = omitOv ? "" : navItem(mc.overview_label || "Overview");
		let panes = omitOv ? "" : pane(mod.li, mod.sc, ovCols);
		for (const l of levels) {
			nav += navItem(l.label);
			panes += levelPane(l.li, l.sc, cols);
		}
		// menu.shell_row: a dialect whose gold wraps the tabs in the corpus
		// ROW+COL form (moduleMenu > div.row > div.tabs.col-12 — the WJFUN gold
		// and most of the corpus's tabs menus) names its shell here and
		// SkeletonBuilder selects it through content.menu.wtShell; a cfg without
		// the block (the CHFUN level pages — CHFUN's gold IS bare) keeps the bare
		// writer_tabs shell. Env TILEMENUROW_OFF.
		const sr = mc.shell_row;
		const shellOff = typeof process !== "undefined" && process.env && process.env[(sr && sr.env) || "TILEMENUROW_OFF"];
		const shell = (sr && sr.enabled !== false && sr.shell && !shellOff) ? sr.shell : undefined;
		return { nav, panes, shell };
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
		// opener stays with the most recent pane — defensive).
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
		// The tab pane's items carry their hyperlinks into the weave (menu.inline_links; env MENULINKS_OFF)
		const linksOn = MenuBuilder.#menuLinksOn();
		let linkBuf = [];
		const bufLinks = (it) => { if (linksOn) for (const l of (it?.block?.links ?? [])) if (l?.text && l?.target) linkBuf.push(l); };
		const flush = () => {
			if (!textBuf.length) return;
			const sec = sections[sections.length - 1];
			for (const piece of ListsAndRuns.renderBlackText(textBuf.join("\n"), run, linksOn ? linkBuf : [])) sec.pieces.push(piece);
			textBuf = [];
			linkBuf = [];
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
			if (it.type === "black") { pushLines(it.text); bufLinks(it); continue; }
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
				if ((it.blackAfter || "").trim()) { pushLines(it.blackAfter); bufLinks(it); }
				continue;
			}
			if ((it.blackAfter || "").trim()) { pushLines(it.blackAfter); bufLinks(it); }
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
	 * THE STANDARD ENTRY IS ONE PARAGRAPH, THE TITLE LINKED (KB 01B, the Standards / Assessment tab): the Writers Template's
	 * standard block, one paragraph per line, is composed into <p><b>standard</b><br><a>title</a><br>level<br>credits</p>
	 * wherever it landed in the built menu — every pane string of buildMenu's result (the core buckets, the column and
	 * promoted-tab panes, the writer-tab panes), walked once after the build. Data menu.standard_entry; env STDENTRY_OFF.
	 */
	static composeStandardEntries(menu, run) {
		const cfg = DataService.Data.EmitTemplates.menu?.standard_entry;
		if (!menu || !cfg || cfg.enabled === false || !cfg.std_pattern) return menu;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "STDENTRY_OFF"]) return menu;
		let n = 0;
		const walk = (v, depth) => {
			if (typeof v === "string") {
				if (!v.includes("<p")) return v;
				const r = this.#composeStandardEntries(v, cfg);
				n += r.n;
				return r.html;
			}
			if (depth > 3 || !v || typeof v !== "object") return v;
			if (Array.isArray(v)) { for (let k = 0; k < v.length; k++) v[k] = walk(v[k], depth + 1); return v; }
			for (const k of Object.keys(v)) v[k] = walk(v[k], depth + 1);
			return v;
		};
		walk(menu, 0);
		if (n) run?.AddNote?.("info", "MenuBuilder", `${n} standard entr${n === 1 ? "y" : "ies"} composed in the KB 01B form (menu.standard_entry).`);
		return menu;
	}

	/**
	 * A BOLD STRAND LINE IN THE KNOW / DO MENU IS THE STRAND'S HEADING. In every pane string of buildMenu's result, inside a
	 * section headed (<h4>) Know / Do / Understand, a short paragraph whose whole content is one bold run, followed by more of the
	 * section, becomes the strand's <h5> (the human build's form, 0.95). Data menu.strand_heading; env STRANDH5_OFF.
	 */
	static strandHeadings(menu, run) {
		const cfg = DataService.Data.EmitTemplates.menu?.strand_heading;
		if (!menu || !cfg || cfg.enabled === false || !cfg.section_pattern) return menu;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "STRANDH5_OFF"]) return menu;
		const secRe = new RegExp(cfg.section_pattern, "iu");
		const maxW = cfg.max_words ?? 12;
		const reqRe = cfg.require_pattern ? new RegExp(cfg.require_pattern, "u") : null;
		const textOf = (s) => String(s).replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();
		let n = 0;
		const fix = (h) => {
			if (typeof h !== "string" || !/<h4\b/i.test(h)) return h;
			return h.replace(/(<h4\b[^>]*>([\s\S]*?)<\/h4>)([\s\S]*?)(?=<h4\b|$)/gi, (all, head, headInner, sec) => {
				if (!secRe.test(textOf(headInner))) return all;
				const out = sec.replace(/<p>\s*<(b|strong)>([^<]+)<\/\1>\s*<\/p>(?=\s*<(?:p|ul|ol|div)\b)/g, (pAll, _t, inner) => {
					const t = inner.replace(/\s+/g, " ").trim();
					if (!t || t.split(" ").length > maxW || /[.!?:]$/.test(t) || (reqRe && !reqRe.test(t))) return pAll;
					n++;
					return Utils.FillTemplate(cfg.template ?? "<h5>{text}</h5>", { text: t });
				});
				return head + out;
			});
		};
		for (const k of ["tab1", "tab2", "content", "left", "right"]) if (typeof menu[k] === "string") menu[k] = fix(menu[k]);
		for (const cols of [menu.tab1Cols, menu.tab2Cols, menu.extraTabs]) if (Array.isArray(cols)) for (const c of cols) if (c && typeof c.html === "string") c.html = fix(c.html);
		if (n) run?.AddNote?.("info", "MenuBuilder", `${n} bold strand line${n === 1 ? "" : "s"} in a Know / Do pane headed as <h5> (menu.strand_heading).`);
		return menu;
	}

	/**
	 * THE UNFILLED STANDARDS TEMPLATE NEVER SHIPS. In every pane of buildMenu's result that holds the template's sentinel
	 * («Level #, External/Internal», «# credits», «Module code Standard (# credits) – Name/Title»), the paragraphs and list
	 * items that are template lines go, an emptied list goes, a lead left with nothing after it goes (back to front), the
	 * emptied heading goes; a promoted tab left with no content of its own is dropped (KB c67's omission rule).
	 * Data menu.unfilled_standard_template; env STDTEMPLATE_OFF.
	 */
	static omitUnfilledStandards(menu, run) {
		const cfg = DataService.Data.EmitTemplates.menu?.unfilled_standard_template;
		if (!menu || !cfg || cfg.enabled === false || !cfg.sentinel_pattern) return menu;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "STDTEMPLATE_OFF"]) return menu;
		const fold = (x) => String(x).replace(/<[^>]+>/g, " ").replace(/&nbsp;|&#160;/g, " ").replace(/&amp;/g, "&")
			.replace(/\s+/g, " ").trim().toLowerCase();
		const sentRe = new RegExp(cfg.sentinel_pattern, "i");
		const blockRes = (cfg.block_patterns ?? []).map((p) => new RegExp(p, "i"));
		const leadRes = (cfg.lead_patterns ?? []).map((p) => new RegExp(p, "i"));
		const own = (h) => [...String(h).matchAll(/<(p|li|h[1-6])\b([^>]*)>([\s\S]*?)<\/\1>/g)].some((b) => !/cv2-/.test(b[2]) && !/^h/.test(b[1]) && fold(b[3]))
			|| /<(?:img|table|iframe|a)\b/i.test(String(h).replace(/<p\b[^>]*cv2-[^>]*>[\s\S]*?<\/p>/g, ""));
		let n = 0;
		const clean = (h) => {
			if (typeof h !== "string" || !h.includes("<")) return h;
			if (![...h.matchAll(/<(p|li)\b([^>]*)>([\s\S]*?)<\/\1>/g)].some((b) => sentRe.test(fold(b[3])))) return h;
			let s = h.replace(/\s*<(p|li)\b([^>]*)>([\s\S]*?)<\/\1>/g, (all, tag, attrs, inner) =>
				(!/cv2-/.test(attrs) && blockRes.some((r) => r.test(fold(inner))) ? "" : all));
			s = s.replace(/\s*<(ul|ol)\b[^>]*>\s*<\/\1>/g, "");
			// a lead with nothing after it in its pane (only closing tags or the end) goes; repeated, so a chain goes back to front
			for (let guard = 0; guard < 8; guard++) {
				const ps = [...s.matchAll(/<p\b([^>]*)>([\s\S]*?)<\/p>/g)].filter((b) => !/cv2-/.test(b[1]) && leadRes.some((r) => r.test(fold(b[2]))));
				const last = ps.reverse().find((b) => !s.slice(b.index + b[0].length).replace(/<p\b[^>]*cv2-[^>]*>[\s\S]*?<\/p>/g, "").replace(/<\/[a-z0-9]+>/gi, "").trim());
				if (!last) break;
				s = s.slice(0, last.index).replace(/\s+$/, "") + s.slice(last.index + last[0].length);
			}
			s = this.dropEmptyHeadings(s, run);
			n++;
			return s;
		};
		for (const k of ["tab1", "tab2", "content", "left", "right"]) if (typeof menu[k] === "string") menu[k] = clean(menu[k]);
		for (const cols of [menu.tab1Cols, menu.tab2Cols]) if (Array.isArray(cols)) for (const c of cols) if (c && typeof c.html === "string") c.html = clean(c.html);
		if (Array.isArray(menu.extraTabs)) {
			for (const t of menu.extraTabs) if (t && typeof t.html === "string") t.html = clean(t.html);
			const kept = menu.extraTabs.filter((t) => t && own(t.html));
			if (kept.length !== menu.extraTabs.length) {
				// a dropped tab's developer notes pass through to the first pane, where the note relocation still finds them
				const notes = menu.extraTabs.filter((t) => t && !own(t.html))
					.flatMap((t) => [...String(t.html).matchAll(/<p\b[^>]*cv2-[^>]*>[\s\S]*?<\/p>/g)].map((x) => x[0]));
				const col = Array.isArray(menu.tab1Cols) ? [...menu.tab1Cols].reverse().find((c) => c && typeof c.html === "string") : null;
				const host = ["tab1", "content", "left", "tab2", "right"].find((k) => typeof menu[k] === "string" && menu[k].trim());
				if (notes.length && col) col.html += "\n" + notes.join("\n");
				else if (notes.length && host) menu[host] += "\n" + notes.join("\n");
				run?.AddNote?.("info", "MenuBuilder", `${menu.extraTabs.length - kept.length} promoted tab(s) left empty by the unfilled standards template dropped (KB c67 omission rule; menu.unfilled_standard_template).`);
				menu.extraTabs = kept.length ? kept : null;
			}
		}
		if (n) run?.AddNote?.("info", "MenuBuilder", `${n} menu pane(s): the unfilled standards template omitted (menu.unfilled_standard_template).`);
		return menu;
	}

	/**
	 * THE STANDARD ENTRY (KB 01B, the Standards / Assessment tab). Reads a menu pane's paragraphs in order; a run that opens
	 * with a standard line (cfg.std_pattern) and continues — paragraph after paragraph, nothing but white space between —
	 * with the entry's own lines (the address, '(Version N)', the title, the level, the credits; the template's unfilled
	 * placeholders) becomes ONE paragraph: <b>standard (Version N)</b><br><a href target=_blank>title</a><br>level<br>credits.
	 * A run with neither a level nor a credits line is left as it is. Returns { html, n } (n = entries composed).
	 */
	static #composeStandardEntries(html, cfg) {
		const src = String(html ?? "");
		const stdRe = new RegExp(cfg.std_pattern, "i"), verRe = new RegExp(cfg.version_pattern, "i");
		const phRe = new RegExp(cfg.placeholder_pattern, "i"), titleLabelRe = new RegExp(cfg.title_label_pattern, "i");
		const levelRe = new RegExp(cfg.level_pattern, "i"), creditsRe = new RegExp(cfg.credits_pattern, "i");
		const maxParts = cfg.max_parts ?? 7;
		// the entry's other writer forms (standard_entry.more_forms; env STDENTRYMORE_OFF): a bare number as the standard line,
		// «URL: <address>» typed as text, the standard's own address repeated as a link line
		const mf = cfg.more_forms;
		const mfOn = !!mf && mf.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[mf.env ?? "STDENTRYMORE_OFF"]);
		const bareStdRe = mfOn && mf.bare_std_pattern ? new RegExp(mf.bare_std_pattern) : null;
		const urlTextRe = mfOn && mf.url_text_pattern ? new RegExp(mf.url_text_pattern, "i") : null;
		const urlLabelRe = mfOn && mf.url_label_pattern ? new RegExp(mf.url_label_pattern, "i") : null;
		const isStd = (t) => stdRe.test(t) || (!!bareStdRe && bareStdRe.test(t));
		const textOf = (s) => String(s).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
		const isUrl = (s) => /^(?:https?:\/\/|www\.)\S+$/i.test(String(s).trim());
		const linkRe = /<a\b[^>]*\bhref="([^"]*)"[^>]*>([\s\S]*?)<\/a>/i;
		const paras = [];
		const pRe = /<p(\s[^>]*)?>([\s\S]*?)<\/p>/g;
		let m;
		while ((m = pRe.exec(src))) paras.push({ start: m.index, end: m.index + m[0].length, attrs: m[1] ?? "", inner: m[2] });
		const out = [];
		let pos = 0, n = 0;
		for (let i = 0; i < paras.length; i++) {
			const p0 = paras[i];
			const l0 = p0.inner.match(linkRe);
			// the standard line: its own words (a link on it is the address; the link's words are the standard when they
			// read as one, the title when they do not)
			let stdText = textOf(l0 ? p0.inner.replace(linkRe, " ") : p0.inner);
			let href = null, linkText = null, title = null, version = null, level = null, credits = null, stdLink = null;
			if (l0) {
				href = l0[1];
				const lt = textOf(l0[2]);
				// the writer linked the standard's own words: with no title to carry it, the link stays on them
				if (stdRe.test(lt) && !stdRe.test(stdText)) { stdLink = { words: lt, rest: stdText }; stdText = (lt + " " + stdText).trim(); }
				else linkText = lt;
			}
			if (!isStd(stdText)) continue;
			const vIn = stdText.match(/\(\s*version\s*#?\s*[\d.]*\s*\)/i);
			if (vIn) { stdText = stdText.replace(vIn[0], " ").replace(/\s+/g, " ").trim(); if (/\d/.test(vIn[0])) version = vIn[0]; }
			let j = i + 1;
			const notes = [];   // a developer note inside the entry («(from NZQA document)») passes through, after the entry
			for (; j < paras.length && j - i <= maxParts; j++) {
				if (src.slice(paras[j - 1].end, paras[j].start).trim()) break;
				if (/\bcv2-note\b/.test(paras[j].attrs)) { notes.push(src.slice(paras[j].start, paras[j].end)); continue; }
				const inner = paras[j].inner;
				const lk = inner.match(linkRe);
				const rest = textOf(lk ? inner.replace(linkRe, " ") : inner);
				const t = textOf(inner);
				if (isStd(t)) break;
				if (lk && !href && (!rest || phRe.test(rest) || verRe.test(rest) || (!!urlLabelRe && urlLabelRe.test(rest)))) {
					href = lk[1]; const lt = textOf(lk[2]); linkText = lt;
					if (verRe.test(rest) && /\d/.test(rest)) version = version ?? rest;
					continue;
				}
				if (lk && href && mfOn && lk[1] === href && (!rest || phRe.test(rest))) continue;   // the same address again
				if (lk) break;
				const um = !href && urlTextRe ? t.match(urlTextRe) : null;
				if (um) { href = um[1]; linkText = um[1]; continue; }
				if (phRe.test(t)) continue;
				if (verRe.test(t)) { if (/\d/.test(t)) version = version ?? t; continue; }
				if (levelRe.test(t) && !level) { level = t; continue; }
				if (creditsRe.test(t) && !credits) { credits = t; if (level) { j++; break; } continue; }
				if (titleLabelRe.test(t) && !title) { title = t.replace(titleLabelRe, "").trim(); continue; }
				if (!title && !level && !credits && t.split(/\s+/).length >= 2 && !/:\s*$/.test(t)) { title = t; continue; }
				break;
			}
			if (!level && !credits) continue;
			const nrm = (s) => String(s ?? "").toLowerCase().replace(/[^a-z0-9ā-ū]+/g, " ").trim();
			const keepStdLink = !!stdLink && !title && !linkText;
			const lines = [keepStdLink
				? `<b><a href="${href}" target="_blank">${stdLink.words}</a>${stdLink.rest ? " " + stdLink.rest : ""}${version ? " " + version : ""}</b>`
				: `<b>${stdText}${version ? " " + version : ""}</b>`];
			if (href && !keepStdLink) {
				if (title && linkText && !isUrl(linkText) && !nrm(linkText).includes(nrm(title))) {
					lines.push(`<a href="${href}" target="_blank">${linkText}</a>`, title);
				} else {
					lines.push(`<a href="${href}" target="_blank">${title || linkText || href}</a>`);
				}
			} else if (title) lines.push(title);
			if (level) lines.push(level);
			if (credits) lines.push(credits);
			out.push(src.slice(pos, p0.start), `<p>${lines.join("<br>")}</p>`, ...notes.map((x) => "\n" + x));
			pos = paras[j - 1].end;
			i = j - 1;
			n++;
		}
		out.push(src.slice(pos));
		return { html: n ? out.join("") : src, n };
	}

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
	 * looks up the dominant level recorded for that combination.
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

// Node export hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { MenuBuilder };
