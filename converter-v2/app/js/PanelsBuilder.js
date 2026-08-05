/**
 * PanelsBuilder.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Builds the multi-PANEL page scaffolding used by two families of module
 * templates: "Fundamentals" templates (which split a page into numbered
 * PHASES — Phase 1, Phase 2, etc — each shown as its own panel) and
 * "Inquiry" templates (which split a page into TABS/crumbs, each a numbered
 * step in an inquiry process). Four static methods:
 *
 *   - fundamentalsPanels(body, opts)  wraps a Fundamentals-template page's
 *         body HTML into a series of `div.fundamentalsPanel` blocks, cut at
 *         SENTINEL markers that ConvertPage (the caller) inserted earlier in
 *         the pipeline to mark where each phase begins. Handles three
 *         different ways writers mark up their phases across different
 *         subject families: the "HPFUN" family's [New tab] tag, the "SSFUN"
 *         family's [LESSON]-phase tag, and the "TEFUN" family's plain
 *         phase-text markers — each paired with the .phases navigation strip
 *         + .introduction wrapper the human-built pages always include. Data:
 *         body_region.fundamentals_panels. (The sentinel-insertion logic and
 *         the env toggles that gate WHICH sentinel gets used — FUNDPANEL_OFF
 *         / FUNDPHASE_OFF — stay behind in ConvertPage, since they're part of
 *         deciding whether to call this method at all, not part of building
 *         the panels once called.)
 *   - phaseNavTiles(panelSegs)  builds the phaseLink "picture tile" row (one
 *         clickable tile per phase, usually with an image) plus the .phases
 *         navigation strip that the human-built pages always pair with a
 *         Fundamentals overview page (env PHASETILES_OFF)
 *   - inquiryPanels(body, opts)  wraps an Inquiry-template page's body HTML
 *         into the tabbed scaffold used by that template family: a
 *         `div.crumbs` navigation bar plus one `div.inquiryPanel` per step.
 *         Handles three writer conventions: the "BLL" family's [Tab N] tags,
 *         the "CED" family's page-split mode (where each tab is really its
 *         own sub-page), and the "TWHA"/"TWHK" family's heading-label mode
 *         (where each panel's own first heading becomes its crumb label).
 *         Data: body_region.inquiry_tabs. (Again, the caller-side toggles
 *         that gate which mode is used — INQUIRYTABS_OFF / HEADINGLABEL_OFF —
 *         stay behind in ConvertPage.)
 *   - detectInquiryCed(page, tpl)  scans the WHOLE page's item stream (not
 *         just the body) to detect the "CED" [page N]-split inquiry
 *         sub-family and capture its crumb labels, since that family's crumb
 *         list can appear either inside the menu or inside the body
 *         depending on the module (env CEDPAGE_OFF / CEDCONSUMED_OFF)
 *
 * WHY SEPARATE FILE:
 * Panel building used to live inline inside ContentConverter, the class that
 * emits the rest of the page body. It was carved out into its own file
 * because it's a clean, self-contained unit: it has NO shared state with the
 * rest of the converter (no instance fields of its own), and the sentinel-
 * insertion machinery that decides WHEN to call these methods stays behind in
 * ContentConverter/ConvertPage, which calls the entry points above at the
 * right points during page assembly. Moving code into its own file changes
 * WHERE it lives, never WHAT it produces — every method here behaves exactly
 * as it did before the move.
 *
 * WHEN TO WORK HERE:
 * Any time a Fundamentals-template phase panel or an Inquiry-template tabbed
 * panel renders with the wrong navigation, the wrong number of panels, a
 * missing picture tile, or the wrong crumb label. The layout rules themselves
 * live in Emit_Templates.json's `body_region.fundamentals_panels` and
 * `body_region.inquiry_tabs` sections and are read by the methods above; most
 * fixes are a data change there plus the minimal method logic needed to apply
 * it.
 * ===========================================================================
 */

class PanelsBuilder {

	/**
	 * Wraps a Fundamentals-template page's body HTML into
	 * `div.fundamentalsPanel phase="N"` panels, cut at the sentinel markers
	 * that ConvertPage inserted earlier in the pipeline (in fundamentals
	 * mode). Which sentinel is present in the body tells this method WHICH
	 * of three writer conventions it's dealing with (see the three branches
	 * inside the method body below — the [New tab] HPFUN family, the
	 * [LESSON]-phase SSFUN family, or the plain-text-marker TEFUN family) —
	 * each is handled by its own code path further down.
	 *
	 * For the [New tab] (HPFUN) convention specifically: the first non-empty
	 * segment becomes the introduction panel (using the `intro_class` CSS
	 * class), and the rest become numbered content panels (using
	 * `panel_class`), numbered phase 1..N.
	 *
	 * AUTO-SCOPED: a page body containing NONE of the three sentinels (e.g.
	 * the SSFUN activity-group family, the XFUN [H1] family, or any ordinary
	 * non-fundamentals page) is returned completely unchanged. Whichever
	 * sentinel IS found is ALWAYS consumed during processing (either
	 * split-and-rewrapped into panels, or split-and-rejoined) so a sentinel
	 * marker can never leak out into the final rendered HTML by accident.
	 *
	 * @param {string} body - the page's already-rendered body HTML,
	 *   containing zero or more sentinel markers
	 * @param {Object} opts
	 * @param {boolean} opts.on - whether fundamentals-panel mode is active
	 *   for this page at all (decided by the caller; when false, this method
	 *   just strips any stray sentinels and returns the body as-is)
	 * @param {string} [opts.sentinel] - the HPFUN [New tab] sentinel string
	 * @param {string} [opts.lessonSentinel] - the SSFUN [LESSON]-phase
	 *   sentinel string
	 * @param {string} [opts.phaseTextSentinel] - the TEFUN plain phase-text
	 *   sentinel string
	 * @param {Object} [opts.run] - the conversion run context
	 * @returns {string} the body HTML, now wrapped into panels (or
	 *   unchanged, if no sentinel was found)
	 *
	 * Data: body_region.fundamentals_panels. Env FUNDPANEL_OFF (checked by
	 * the caller before even calling this method, via the `on` flag above).
	 */
	static fundamentalsPanels(body, { on, sentinel, lessonSentinel, phaseTextSentinel, run, levelRow, levelLabels } = {}) {
		const cfg = DataService.Data.EmitTemplates.body_region.fundamentals_panels;
		const sent = sentinel || (cfg && cfg.sentinel) || "<!--CV2_FUNDPANEL-->";
		const lsent = lessonSentinel || (cfg && cfg.lesson_sentinel) || "<!--CV2_FUNDPHASE-->";
		const ptsent = phaseTextSentinel
			|| (cfg && cfg.phase_text && cfg.phase_text.sentinel) || "<!--CV2_FUNDPHASETEXT-->";
		const strip = (s) => s.split(sent).join("").split(lsent).join("").split(ptsent).join("");
		if (!on || !cfg || cfg.enabled === false) return strip(body);

		// THE "TEFUN" PHASE-TEXT CONVENTION: this family marks phase boundaries with
		// plain phase-text markers rather than a bracketed [tag]. Builds a
		// div.phases navigation strip (one tile per phase) + a div.introduction
		// wrapping the pre-phase content + one plain div.fundamentalsPanel per
		// phase — with NO generated heading, since the writer's own [H3] heading
		// (e.g. "Plan it!") already serves as the phase's title. segs[0] is the
		// introduction content; every later segment is one phase. This is a
		// DIFFERENT shape than the HPFUN convention below (which turns the intro
		// into its own numbered panel) and the SSFUN convention below (which
		// prepends a generated "<h3>Phase N</h3>" heading to each panel).
		if (body.includes(ptsent)) {
			const pc = cfg.phase_text || {};
			const segs = body.split(ptsent);
			const intro = segs[0].trim();
			const panelSegs = segs.slice(1).map((s) => s.trim()).filter((s) => s.length);
			if (!panelSegs.length) return strip(body);
			const n = panelSegs.length;
			// SOME modules in this family author their phases as an accordion widget
			// instead of plain phase-text markers — the writer's [Accordion]/
			// [Accordion N] tags become the phase boundaries there instead. When this
			// module has a matching row in the accordion_delimiter registry (see
			// #phaseTextDialectRow below), use the ACCORDION-AS-PHASES nav/tile variant
			// instead of the plain nav/tiles built below: nav labels come from each
			// panel's own FIRST heading (a writer's short heading may be their own
			// abbreviation of a longer body sentence — that's a faithful reproduction
			// of an editorial choice, not something to "fix"), and the tile row shows
			// ALL phases together in ONE row of `col-md-4 col-6` phaseLink tiles inside
			// a `row phaseContainer noPhase` container, each tile using `alt="Phase N"`.
			// This is a DIFFERENT tile/nav shape than both phaseNavTiles() and
			// newTabNav() below. A module with NO matching registry row takes the
			// plain phase-text path immediately below instead, completely unchanged.
			// Data: fundamentals_panels.phase_text.accordion_delimiter.
			// Env FUNPANACC_OFF disables this accordion-as-phases variant.
			const accRow = this.#phaseTextDialectRow(run);
			let nav, tilesRow;
			// LEVEL-PAGE dialect (ROUND 265 — the CHFUN "[PAGE N Novice]" family):
			// the caller (ContentConverter's level-pages pre-pass) supplies the
			// LEVEL names as the nav/tile labels and the matched registry row's
			// own tile templates. Data: fundamentals_panels.level_pages.
			// Env LEVELPAGE_OFF (the caller never passes levelRow when set).
			if (levelRow) {
				({ nav, tilesRow } = this.#levelPagesNav(panelSegs, levelRow, pc, levelLabels));
			} else if (accRow) {
				({ nav, tilesRow } = this.#phaseTextDialect(panelSegs, intro, accRow, pc));
			} else {
				nav = (pc.phases_nav_open || "<div class=\"phases\">") + "\n";
				for (let i = 1; i <= n; i++)
					nav += Utils.FillTemplate(pc.phases_nav_item || "<div phase=\"{n}\">\n<p>Phase {n}</p>\n</div>",
						{ n: String(i) }) + "\n";
				nav += (pc.phases_nav_close || "</div>");
				// Append the phaseLink picture-tile row inside .introduction — the
				// human-built pages always pair these phase panels with a picture-tile
				// row like this. Env PHASETILES_OFF makes phaseNavTiles() return an
				// empty tilesRow, so introBlock below falls back to its plain form
				// (just the intro content, no tile row).
				({ tilesRow } = this.phaseNavTiles(panelSegs));
			}
			// ROUND 265 (level-pages): the human nests the phaseLink tile row
			// INSIDE the introduction's own content column (not as a sibling
			// row after it) — when the registry row asks for that and the intro
			// actually ends with a closed row>col pair, tuck the tile row in
			// just before those two closing tags. Any other shape falls back to
			// the plain "tiles after the intro" form below.
			let introInner;
			if (levelRow && levelRow.tiles_inside_col !== false && tilesRow
				&& /<\/div>\s*<\/div>\s*$/.test(intro)) {
				introInner = intro.replace(/(<\/div>\s*<\/div>\s*)$/, tilesRow + "\n$1");
			} else {
				introInner = [intro, tilesRow].filter(Boolean).join("\n");
			}
			const introBlock = introInner
				? (pc.intro_open || "<div class=\"introduction\">") + "\n" + introInner + "\n" + (pc.intro_close || "</div>")
				: "";
			const panels = panelSegs.map((seg, i) =>
				Utils.FillTemplate(pc.panel_open || "<div class=\"fundamentalsPanel\" phase=\"{phase}\">",
					{ phase: i + 1 }) + "\n" + seg + "\n" + (pc.panel_close || "</div>"));
			// Run strip() over the WHOLE assembled output, not just the individual
			// panels: a module that mixes BOTH the [New tab] sentinel AND the plain
			// phase-text marker in the same document (e.g. modules MXFUN02/03) can
			// leave a leftover [New tab] sentinel sitting in segs[0] (the
			// pre-"Phase N" introduction), which would otherwise leak out as an
			// invisible HTML comment nobody notices — real junk in the output, even
			// though it's harmless to any visible rendering. Calling strip() on the
			// full assembled string is a safe no-op for a page that has nothing left
			// to strip (like a pure TEFUN-only page), so doing it unconditionally
			// here is both safe and simpler than tracking which case applies.
			return strip(nav + "\n" + (introBlock ? introBlock + "\n" : "") + panels.join("\n"));
		}

		// SSFUN [LESSON]-PHASE family: each segment after a phase sentinel is a plain
		// fundamentalsPanel (NO introduction) led by a generated "<h3>Phase N</h3>"
		// heading (the human's heading). The pre-content (overview) stays before them.
		if (body.includes(lsent)) {
			const pc = cfg.phase_text || {};
			const segs = body.split(lsent);
			const pre = segs[0].trim();
			const panelSegs = segs.slice(1).map((s) => s.trim()).filter((s) => s.length);
			if (!panelSegs.length) return strip(body);
			const panels = panelSegs.map((seg, i) =>
				Utils.FillTemplate(cfg.panel_open, { cls: cfg.panel_class, phase: i + 1 }) + "\n"
				+ Utils.FillTemplate(cfg.phase_heading || "<h3>Phase {n}</h3>", { n: String(i + 1) }) + "\n"
				+ seg + "\n" + cfg.panel_close);
			// Pair these panels with the .phases navigation strip and the
			// .introduction wrapper (holding the pre-content plus the phaseLink
			// tiles) that the human-built pages always ship alongside them. This is
			// self-scoping (keyed directly on panelSegs, so it only fires when there
			// actually are phase panels); env PHASETILES_OFF makes phaseNavTiles()
			// return empty strings for both, so the output below falls back to its
			// plain original form (no nav, no tile row).
			const { nav, tilesRow } = this.phaseNavTiles(panelSegs);
			if (nav || tilesRow) {
				const introInner = [pre, tilesRow].filter(Boolean).join("\n");
				const introBlock = introInner
					? (pc.intro_open || "<div class=\"introduction\">") + "\n" + introInner + "\n" + (pc.intro_close || "</div>")
					: "";
				return strip((nav ? nav + "\n" : "") + (introBlock ? introBlock + "\n" : "") + panels.join("\n"));
			}
			return strip((pre ? pre + "\n" : "") + panels.join("\n"));
		}

		// THE "HPFUN" [New tab] CONVENTION: segs[0] is the overview/menu content the
		// writer left above the [Fundamental content] marker (this is NOT a panel —
		// it's ordinary overview content); the PANELS are the segments AFTER each
		// [New tab] marker, with the first of them treated as the introduction panel.
		if (!body.includes(sent)) return strip(body);
		const segs = body.split(sent);
		const pre = segs[0].trim();
		const panelSegs = segs.slice(1).map((s) => s.trim()).filter((s) => s.length);
		if (!panelSegs.length) return strip(body);
		// Pair the .phases nav + phaseLink tile grid with these [New tab] panels too
		// (see module HPFUN903 for an example) — the same kind of nav/tile pairing
		// the TEFUN/SSFUN conventions get above, but built by a dedicated
		// newTabNav() method (below) since this family's tile layout differs
		// slightly. Nav labels come from each panel's own first heading; tiles
		// cover the CONTENT phases only, and get appended INSIDE the intro panel,
		// after its own content (matching where the human-built pages put them).
		// This is scoped to a registry of known-good subject families — a module
		// with no matching registry row (e.g. one whose panels don't cleanly map
		// to real phases) is left completely unchanged, using the original plain
		// form built above. Data: fundamentals_panels.new_tab_nav.
		// Env FUNNAV_OFF disables this nav/tile pairing.
		const nt = this.newTabNav(panelSegs, run);
		const panels = panelSegs.map((seg, i) =>
			Utils.FillTemplate(cfg.panel_open, { cls: i === 0 ? cfg.intro_class : cfg.panel_class, phase: i + 1 })
			+ "\n" + (i === 0 && nt.tilesRows ? seg + "\n" + nt.tilesRows : seg) + "\n" + cfg.panel_close);
		return (nt.nav ? nt.nav + "\n" : "") + (pre ? pre + "\n" : "") + panels.join("\n");
	};

	/**
	 * Looks up the accordion_delimiter registry row for this module, or
	 * null if none exists. Uses the same specific-to-general lookup pattern
	 * used across the converter: this exact module's series override →
	 * its subject|template_phase group (with the phase value normalised
	 * through skeleton.template_attr_map first).
	 *
	 * This is what gates the phase-text branch's accordion-as-phases
	 * nav/tile variant above — a module with no matching row (e.g. the
	 * TEFUN/SCFUN/ARFUN/ENFUN families, which don't use the accordion
	 * convention) falls through to the plain phase-text nav/tile form
	 * instead, completely unaffected by this method.
	 *
	 * @param {Object} run - the conversion run context
	 * @returns {Object|null} the registry row, or null
	 *
	 * Env FUNPANACC_OFF or FUNDPHASE_OFF both disable this lookup (either
	 * one alone is enough to force a null return).
	 */
	static #phaseTextDialectRow(run) {
		const acc = DataService.Data.EmitTemplates.body_region.fundamentals_panels?.phase_text?.accordion_delimiter;
		if (!acc || acc.enabled === false || !run) return null;
		if (typeof process !== "undefined" && process.env
			&& (process.env.FUNPANACC_OFF || process.env.FUNDPHASE_OFF)) return null;
		const reg = acc.registry || {};
		if (reg.series && reg.series[run.moduleCode]) return reg.series[run.moduleCode];
		const subj = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const rawPhase = run.resolvedRules?.template_phase ?? "";
		const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
		const lk = `${subj}|${phase}`.toLowerCase();
		const hit = Object.keys(reg.groups || {}).find((k) => k.toLowerCase() === lk);
		return hit ? reg.groups[hit] : null;
	};

	/**
	 * Builds the accordion-as-phases nav/tile variant (the THIRD distinct
	 * nav/tile layout in this file, alongside phaseNavTiles() and
	 * newTabNav() below — see module XFUN01 for an example that uses this
	 * exact form):
	 *   - nav: one `<div phase=N><p>{label}</p>` entry per PANEL, where the
	 *     label is taken from each panel's FIRST heading (using only the
	 *     English half, before any ' | ' separator; falls back to a plain
	 *     "Phase {n}" string if the panel has no heading)
	 *   - tiles: ALL phases (including phase 1) shown together in ONE
	 *     `row phaseContainer noPhase` row of `col-md-4 col-6` phaseLink
	 *     tiles, each using `alt="Phase N"` (NOT the heading label)
	 *
	 * Each tile's image comes from that panel's own first content <img> src,
	 * falling back to any other panel's first image, and finally to the
	 * introduction's first image if nothing else is found — every human-
	 * built tile carries SOME image, even though the exact image chosen for
	 * a given tile is an editorial decision made when the page was first
	 * built (not something derivable from the Writers Template), so this
	 * fallback chain just avoids ever rendering a tile with no image at all.
	 * All of the HTML shapes involved (the nav item template, the tile
	 * template, etc) come from the matched registry row, passed in as `row`.
	 *
	 * @param {string[]} panelSegs - the rendered HTML for each phase panel
	 * @param {string} intro - the rendered HTML for the introduction segment
	 * @param {Object} row - the matched accordion_delimiter registry row
	 * @param {Object} pc - the phase_text config block (for the shared nav
	 *   open/close template strings)
	 * @returns {{nav: string, tilesRow: string}}
	 */
	static #phaseTextDialect(panelSegs, intro, row, pc) {
		const n = panelSegs.length;
		const firstHeading = (html) => {
			const m = /<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/i.exec(html || "");
			if (!m) return "";
			const txt = m[1].replace(/<[^>]+>/g, "").trim();
			return txt.split(/\s*\|\s*/)[0].trim();
		};
		const labels = panelSegs.map((s, i) => {
			if (row.label_mode === "heading") {
				const h = firstHeading(s);
				if (h) return h;
			}
			return Utils.FillTemplate(row.label_fallback || "Phase {n}", { n: String(i + 1) });
		});
		let nav = (pc.phases_nav_open || "<div class=\"phases\">") + "\n";
		for (let i = 0; i < n; i++)
			nav += Utils.FillTemplate(row.phases_nav_item || "<div phase=\"{n}\">\n<p>{label}</p>\n</div>",
				{ n: String(i + 1), label: labels[i] }) + "\n";
		nav += (pc.phases_nav_close || "</div>");
		let fallbackImg = "";
		for (const s of [...panelSegs, intro || ""]) {
			const fm = /<img\b[^>]*\bsrc="([^"]*)"/i.exec(s || "");
			if (fm) { fallbackImg = fm[1]; break; }
		}
		const tiles = [];
		for (let i = 0; i < n; i++) {
			const num = String(i + 1);
			const m = /<img\b[^>]*\bsrc="([^"]*)"/i.exec(panelSegs[i] || "");
			const src = m ? m[1] : fallbackImg;
			let tile = Utils.FillTemplate(
				row.tile_open || "<div class=\"col-md-4 col-6\">\n<div class=\"phaseLink\" phase=\"{n}\">\n<h3>{label}</h3>",
				{ n: num, label: labels[i] });
			if (src) tile += "\n" + Utils.FillTemplate(
				row.tile_img || "<img class=\"phaseImg\" src=\"{src}\" alt=\"Phase {n}\">",
				{ src, label: labels[i], n: num });
			tile += "\n" + (row.tile_close || "</div>\n</div>");
			tiles.push(tile);
		}
		const tilesRow = tiles.length
			? (row.tiles_open || "<div class=\"row phaseContainer noPhase\">") + "\n"
				+ tiles.join("\n") + "\n" + (row.tiles_close || "</div>")
			: "";
		return { nav, tilesRow };
	};

	/**
	 * Builds the LEVEL-PAGES nav/tile variant (ROUND 265 — the CHFUN
	 * "[PAGE N Novice]" family; the FOURTH distinct nav/tile layout in this
	 * file). The labels are the writers' own LEVEL NAMES ("Novice",
	 * "Emergent", …), captured by ContentConverter's level-pages pre-pass and
	 * passed straight in — they are NOT derived from panel headings here.
	 * Tiles show ALL levels in one row; each tile's image is that level
	 * panel's own first content <img> (keeping that image's own alt text —
	 * the human's tiles reuse the source image's alt); a panel with no image
	 * ships a text-only tile (which exact image belongs on which tile is an
	 * editorial decision, so nothing is invented).
	 *
	 * All HTML shapes come from the matched level_pages registry row.
	 *
	 * @param {string[]} panelSegs - the rendered HTML for each level panel
	 * @param {Object} row - the matched level_pages registry row
	 * @param {Object} pc - the phase_text config block (shared nav open/close)
	 * @param {string[]} [labels] - the level names, in panel order
	 * @returns {{nav: string, tilesRow: string}}
	 *
	 * Data: fundamentals_panels.level_pages. Env LEVELPAGE_OFF (the caller
	 * never reaches this method when set).
	 */
	static #levelPagesNav(panelSegs, row, pc, labels) {
		const n = panelSegs.length;
		const lab = (i) => (labels && labels[i]) || `Phase ${i + 1}`;
		let nav = (pc.phases_nav_open || "<div class=\"phases\">") + "\n";
		for (let i = 0; i < n; i++)
			nav += Utils.FillTemplate(row.phases_nav_item || "<div phase=\"{n}\">\n<p>{label}</p>\n</div>",
				{ n: String(i + 1), label: lab(i) }) + "\n";
		nav += (pc.phases_nav_close || "</div>");
		// fallback image: the first content <img> anywhere in the module's
		// panels, so every tile carries SOME image whenever the module has any
		// (which image belongs on which tile is an editorial choice, so a
		// panel's OWN first image always wins when it has one)
		let fallback = null;
		for (const s of panelSegs) {
			const fm = /<img\b[^>]*>/i.exec(s || "");
			if (fm) { fallback = fm[0]; break; }
		}
		const tiles = [];
		for (let i = 0; i < n; i++) {
			const num = String(i + 1);
			const m = /<img\b[^>]*>/i.exec(panelSegs[i] || "") ?? (fallback ? [fallback] : null);
			const src = m ? (/\bsrc="([^"]*)"/i.exec(m[0])?.[1] ?? "") : "";
			const alt = m ? (/\balt="([^"]*)"/i.exec(m[0])?.[1] || lab(i)) : lab(i);
			let tile = Utils.FillTemplate(
				row.tile_open || "<div class=\"col-6\">\n<div class=\"phaseLink\" phase=\"{n}\">\n<h3>{label}</h3>",
				{ n: num, label: lab(i) });
			if (src) tile += "\n" + Utils.FillTemplate(
				row.tile_img || "<img class=\"phaseImg margB0\" src=\"{src}\" alt=\"{alt}\">",
				{ src, alt, n: num, label: lab(i) });
			tile += "\n" + (row.tile_close || "</div>\n</div>");
			tiles.push(tile);
		}
		const tilesRow = tiles.length
			? (row.tiles_open || "<div class=\"row phaseContainer noPhase margB2\">") + "\n"
				+ tiles.join("\n") + "\n" + (row.tiles_close || "</div>")
			: "";
		return { nav, tilesRow };
	};

	/**
	 * Builds the .phases navigation strip + phaseLink tile grid for the HPFUN
	 * [New tab] family specifically (see module HPFUN903 for an example) —
	 * this is a SEPARATE method from phaseNavTiles() below because this
	 * family's conventions differ in several specific ways:
	 *   - labels come from each panel's own FIRST heading (using only the
	 *     English half, before any ' | ' separator; falls back to a plain
	 *     "Phase N" string when a panel has no heading)
	 *   - tiles cover the CONTENT phases only (phase 2 through N — the
	 *     introduction panel, phase 1, does not get its own tile) and sit
	 *     INSIDE the intro panel itself (the caller appends the returned
	 *     tilesRows onto the end of segment 0)
	 *   - tiles chunk into multiple rows of `tiles_per_row` tiles each, once
	 *     the tile count exceeds `tiles_split_over` (e.g. 4 tiles fit on one
	 *     row, but 5 tiles split into a row of 3 plus a row of 2)
	 *   - a tile's `alt` attribute is the label text itself (rather than a
	 *     generic "Phase N" string); the tile's image comes from that
	 *     phase's own first content <img> src, falling back to any other
	 *     phase's first image if this one has none
	 *
	 * SCOPED by a registry row lookup (this module's series → its
	 * subject|template_phase group) — a module with no matching row (e.g.
	 * one whose panels don't cleanly map to real phases) returns
	 * { nav: "", tilesRows: "" }, so the caller's plain HPFUN form (built
	 * without any nav or tiles) stays completely unaffected.
	 *
	 * @param {string[]} panelSegs - the rendered HTML for each phase panel
	 * @param {Object} run - the conversion run context
	 * @returns {{nav: string, tilesRows: string}}
	 *
	 * Data: fundamentals_panels.new_tab_nav. Env FUNNAV_OFF disables this
	 * whole method (always returns the empty { nav: "", tilesRows: "" }).
	 */
	static newTabNav(panelSegs, run) {
		const cfg = DataService.Data.EmitTemplates.body_region.fundamentals_panels;
		const nt = cfg && cfg.new_tab_nav;
		const off = { nav: "", tilesRows: "" };
		if (!nt || nt.enabled === false || !run) return off;
		if (typeof process !== "undefined" && process.env && process.env.FUNNAV_OFF) return off;
		const n = (panelSegs || []).length;
		if (n < (nt.min_phases || 2)) return off;
		// Registry row lookup: this exact module's series override → its
		// subject|template_phase group (case-tolerant, with the phase value
		// normalised through skeleton.template_attr_map first).
		const subj = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const rawPhase = run.resolvedRules?.template_phase ?? "";
		const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
		const reg = nt.registry ?? {};
		let row = reg.series?.[run.moduleCode] ?? reg.groups?.[`${subj}|${phase}`];
		if (!row && reg.groups) {
			const lk = `${subj}|${phase}`.toLowerCase();
			const hit = Object.keys(reg.groups).find((k) => k.toLowerCase() === lk);
			if (hit) row = reg.groups[hit];
		}
		if (!row) return off;
		// labels: each panel's FIRST heading (tags stripped, English half before ' | ')
		const firstHeading = (html) => {
			const m = /<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/i.exec(html || "");
			if (!m) return "";
			const txt = m[1].replace(/<[^>]+>/g, "").trim();
			return txt.split(/\s*\|\s*/)[0].trim();
		};
		const labels = panelSegs.map((s, i) => {
			if (row.label_mode === "heading") {
				const h = firstHeading(s);
				if (h) return h;
			}
			return Utils.FillTemplate(nt.label_fallback || "Phase {n}", { n: String(i + 1) });
		});
		// the .phases nav — one entry per PANEL, intro included (gold ships all 7 on HPFUN903)
		const pc = cfg.phase_text || {};
		let nav = (pc.phases_nav_open || "<div class=\"phases\">") + "\n";
		for (let i = 0; i < n; i++)
			nav += Utils.FillTemplate(nt.phases_nav_item || "<div phase=\"{n}\">\n<p>{label}</p>\n</div>",
				{ n: String(i + 1), label: labels[i] }) + "\n";
		nav += (pc.phases_nav_close || "</div>");
		// the tile grid — CONTENT phases only (2..N), one tile per panel
		let fallbackImg = "";
		for (const s of panelSegs) { const fm = /<img\b[^>]*\bsrc="([^"]*)"/i.exec(s || ""); if (fm) { fallbackImg = fm[1]; break; } }
		const tiles = [];
		for (let i = 1; i < n; i++) {
			const num = String(i + 1);
			const m = /<img\b[^>]*\bsrc="([^"]*)"/i.exec(panelSegs[i] || "");
			const src = m ? m[1] : fallbackImg;
			let tile = Utils.FillTemplate(
				nt.tile_open || "<div class=\"col-md-3 col-6\">\n<div class=\"phaseLink\" phase=\"{n}\">\n<h3>{label}</h3>",
				{ n: num, label: labels[i] });
			if (src) tile += "\n" + Utils.FillTemplate(
				nt.tile_img || "<img src=\"{src}\" alt=\"{label}\" class=\"phaseImg\">",
				{ src, label: labels[i], n: num });
			tile += "\n" + (nt.tile_close || "</div>\n</div>");
			tiles.push(tile);
		}
		if (!tiles.length) return { nav, tilesRows: "" };
		const per = tiles.length > (nt.tiles_split_over ?? 4) ? (nt.tiles_per_row ?? 3) : tiles.length;
		const rows = [];
		for (let i = 0; i < tiles.length; i += per) {
			rows.push((nt.tiles_open || "<div class=\"row phaseContainer\">") + "\n"
				+ tiles.slice(i, i + per).join("\n") + "\n" + (nt.tiles_close || "</div>"));
		}
		return { nav, tilesRows: rows.join("\n") };
	};

	/**
	 * Builds the phaseLink picture-tile NAV row (plus the .phases navigation
	 * strip) that the human-built pages always pair with a Fundamentals
	 * overview page. Returns { nav, tilesRow } (both HTML strings), or a
	 * pair of empty strings when this feature is switched off, or when
	 * there are fewer than `min_phases` panels (a single phase doesn't need
	 * its own navigation).
	 *
	 * Self-scoping: only fundamentalsPanels() above calls this (i.e. only on
	 * a page already detected as using the Fundamentals template), keyed on
	 * that build's own set of phase panels. Tile labels are always the
	 * derivable "Phase N" string; each tile's image is an editorial choice
	 * that isn't written anywhere in the Writers Template, so it's hoisted
	 * from that phase segment's own first content <img src> instead — a
	 * phase with no image of its own simply gets a text-only (h3-only) tile.
	 *
	 * @param {string[]} panelSegs - the rendered HTML for each phase panel
	 * @returns {{nav: string, tilesRow: string}}
	 *
	 * Data: fundamentals_panels.phase_nav_tiles. Env PHASETILES_OFF disables
	 * this (always returns empty strings).
	 */
	static phaseNavTiles(panelSegs) {
		const cfg = DataService.Data.EmitTemplates.body_region.fundamentals_panels;
		const pnt = cfg && cfg.phase_nav_tiles;
		if (!pnt || pnt.enabled === false) return { nav: "", tilesRow: "" };
		if (typeof process !== "undefined" && process.env && process.env.PHASETILES_OFF) return { nav: "", tilesRow: "" };
		const n = (panelSegs || []).length;
		if (n < (pnt.min_phases || 2)) return { nav: "", tilesRow: "" };
		const pc = cfg.phase_text || {};
		let nav = (pc.phases_nav_open || "<div class=\"phases\">") + "\n";
		for (let i = 1; i <= n; i++)
			nav += Utils.FillTemplate(pc.phases_nav_item || "<div phase=\"{n}\">\n<p>Phase {n}</p>\n</div>", { n: String(i) }) + "\n";
		nav += (pc.phases_nav_close || "</div>");
		// The fallback tile image is the module's FIRST phase-content image, so
		// every tile ends up with SOME <img> node even when a particular phase
		// opens without its own image (which image belongs on which tile is an
		// editorial choice, not something written in the Writers Template). Only
		// when the WHOLE module has no images anywhere do tiles fall back to
		// text-only (h3-only).
		let fallbackImg = "";
		for (const s of panelSegs) { const fm = /<img\b[^>]*\bsrc="([^"]*)"/i.exec(s || ""); if (fm) { fallbackImg = fm[1]; break; } }
		let tiles = (pnt.tiles_open || "<div class=\"row phaseContainer\">") + "\n";
		for (let i = 0; i < n; i++) {
			const num = String(i + 1);
			const m = /<img\b[^>]*\bsrc="([^"]*)"/i.exec(panelSegs[i] || "");
			const src = m ? m[1] : fallbackImg;
			let tile = Utils.FillTemplate(pnt.tile_open || "<div class=\"col-md-3 col-6\">\n<div class=\"phaseLink\" phase=\"{n}\">\n<h3>Phase {n}</h3>", { n: num });
			if (src) tile += "\n" + Utils.FillTemplate(pnt.tile_img || "<img class=\"phaseImg\" src=\"{src}\" alt=\"Phase {n}\">", { src, n: num });
			tile += "\n" + (pnt.tile_close || "</div>\n</div>");
			tiles += tile + "\n";
		}
		tiles += (pnt.tiles_close || "</div>");
		return { nav, tilesRow: tiles };
	};

	/**
	 * Wraps an Inquiry-template page's body HTML into the tabbed scaffold
	 * used by that template family: a `div.crumbs` navigation bar (an
	 * "Introduction" crumb, plus one crumb per `[Tab N]` tag — with labels
	 * captured from each `[Tab N] <label>` list item), followed by
	 * `div.inquiryPanel` panels (an intro panel holding the content before
	 * the first `[Tab N]`, then one panel per opener tag). The sentinel
	 * marker is always consumed, whichever branch below handles it; the body
	 * is returned completely unchanged when no sentinel is found at all.
	 *
	 * This base [Tab N] form (the "BLL" family's convention) is just the
	 * DEFAULT — two OTHER writer conventions are handled by dedicated
	 * branches inside the method body, selected via the `cedMode` and
	 * `headingLabel` options:
	 *   - CED PAGE-SPLIT mode (cedMode): used by the "CED" subject family,
	 *     where the FIRST tab already IS the introduction (rather than a
	 *     separate lead-in before tab 1) — so the crumbs are UNIFIED (N
	 *     labels produce N crumbs total, with no separate "Introduction"
	 *     crumb), and there are N panels to match. Uses the page_split
	 *     config block's own crumb_item/panel_open templates (with the
	 *     first crumb/panel marked as "showing").
	 *   - HEADING-LABEL mode (headingLabel): used by the "TWHA"/"TWHK"
	 *     subject family, where the writer never labelled their `[Tab N]`
	 *     tags at all — instead, each panel's OWN first heading becomes its
	 *     crumb label automatically.
	 *
	 * @param {string} body - the page's already-rendered body HTML
	 * @param {Object} opts
	 * @param {boolean} opts.on - whether the base [Tab N] mode is active for
	 *   this page (decided by the caller)
	 * @param {string} [opts.sentinel] - the sentinel marker string
	 * @param {Object} [opts.labels] - captured crumb labels, keyed by tab
	 *   number, for the base [Tab N] mode
	 * @param {boolean} [opts.cedMode] - activates the CED page-split branch
	 * @param {string[]} [opts.cedLabels] - the crumb labels for CED mode
	 * @param {boolean} [opts.headingLabel] - activates the heading-label
	 *   branch
	 * @returns {string} the body HTML, now wrapped into the crumbs+panels
	 *   scaffold (or unchanged, if no sentinel was found)
	 *
	 * Data: body_region.inquiry_tabs.
	 */
	static inquiryPanels(body, { on, sentinel, labels, cedMode, cedLabels, headingLabel } = {}) {
		const cfg = DataService.Data.EmitTemplates.body_region.inquiry_tabs;
		const sent = sentinel || (cfg && cfg.sentinel) || "<!--CV2_INQPANEL-->";
		if (!(on || cedMode) || !cfg || cfg.enabled === false || !body.includes(sent)) return body.split(sent).join("");
		const segs = body.split(sent);
		const intro = segs[0].trim();
		const panelSegs = segs.slice(1).map((s) => s.trim());
		// HEADING-LABEL mode (the "TWHA"/"TWHK" subject family): builds N UNIFIED
		// panels (rel="1".."N", the first one marked "showing"); crumb 1 is always
		// the fixed label "Introduction", and crumbs 2..N are each taken from that
		// panel's own FIRST heading (using only the English part, before any
		// ' | ' separator). Any body content that appeared BEFORE the first
		// `[Tab N]` tag (segs[0] — usually empty, since the overview content is
		// normally routed to the menu instead) gets merged into panel 1, so
		// nothing written by the author is ever lost.
		if (headingLabel) {
			const ps = cfg.page_split || {};
			const hl = cfg.heading_label || {};
			const allSegs = panelSegs.length
				? [(intro ? intro + "\n" : "") + panelSegs[0], ...panelSegs.slice(1)]
				: (intro ? [intro] : []);
			const nPanels = allSegs.length;
			const firstHeading = (html) => {
				const m = /<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/i.exec(html || "");
				if (!m) return "";
				const txt = m[1].replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").trim();
				return txt.split(/\s*\|\s*/)[0].trim();   // English part before ' | '
			};
			const crumbs = [cfg.crumbs_open];
			for (let i = 0; i < nPanels; i++) {
				const label = i === 0 ? (hl.intro_label || cfg.intro_label || "Introduction") : firstHeading(allSegs[i]);
				crumbs.push(Utils.FillTemplate(ps.crumb_item || cfg.crumb_item, {
					n: String(i + 1), label, showing: i === 0 ? " class=\"showing\"" : "" }));
			}
			crumbs.push(cfg.crumbs_close);
			const panels = [];
			for (let i = 0; i < nPanels; i++)
				panels.push(Utils.FillTemplate(ps.panel_open || cfg.panel_open, { n: String(i + 1), showing: i === 0 ? " showing" : "" }) + "\n" + allSegs[i] + "\n" + cfg.panel_close);
			return crumbs.join("\n") + "\n" + panels.join("\n");
		}
		// CED PAGE-SPLIT mode (the "CED" subject family): N unified crumbs + N
		// panels, since the first tab already IS the introduction.
		if (cedMode) {
			const ps = cfg.page_split || {};
			const clab = cedLabels || [];
			// When there is NO leading content before the first `[page N]` tag (the
			// CONSUMED-list variant of this family — e.g. module CEDO102, where the
			// very first `[page N]` tag directly opens the "Introduction" panel),
			// segs[0] is empty, so the panels are simply the sentinel-split segments
			// 1:1 (e.g. 6 panels, not 7). When there IS leading introduction content
			// (the ORPHAN variant of this family — e.g. module CEDK101), that
			// content becomes the first panel instead — `allSegs` ends up as
			// [intro, ...panelSegs], the same result as the simpler
			// `panelSegs.length + 1` calculation this replaced.
			const allSegs = intro === "" ? panelSegs : [intro, ...panelSegs];
			const nPanels = allSegs.length;
			const crumbs = [cfg.crumbs_open];
			for (let i = 0; i < nPanels; i++)
				crumbs.push(Utils.FillTemplate(ps.crumb_item, {
					n: String(i + 1), label: clab[i] || "", showing: i === 0 ? " class=\"showing\"" : "" }));
			crumbs.push(cfg.crumbs_close);
			const panels = [];
			for (let i = 0; i < nPanels; i++)
				panels.push(Utils.FillTemplate(ps.panel_open, { n: String(i + 1), showing: i === 0 ? " showing" : "" }) + "\n" + allSegs[i] + "\n" + cfg.panel_close);
			return crumbs.join("\n") + "\n" + panels.join("\n");
		}
		const lab = labels || {};
		const crumbs = [cfg.crumbs_open, Utils.FillTemplate(cfg.crumb_intro, { label: cfg.intro_label || "Introduction" })];
		for (let i = 0; i < panelSegs.length; i++)
			crumbs.push(Utils.FillTemplate(cfg.crumb_item, { n: String(i + 1), label: lab[i + 1] || "" }));
		crumbs.push(cfg.crumbs_close);
		const panels = [cfg.panel_intro_open + "\n" + intro + "\n" + cfg.panel_close];
		for (let i = 0; i < panelSegs.length; i++)
			panels.push(Utils.FillTemplate(cfg.panel_open, { n: String(i + 1) }) + "\n" + panelSegs[i] + "\n" + cfg.panel_close);
		return crumbs.join("\n") + "\n" + panels.join("\n");
	};

	/**
	 * Detects the CED [page N]-SPLIT inquiry sub-family (the ORPHAN
	 * crumb-list variant — see #inquiryPanels' cedMode above) and captures
	 * its crumb labels, ahead of time, before the body is even rendered.
	 *
	 * Scans the FULL page item stream — not just the body content — because
	 * the labelled `[Tab N]` crumb-list can land in EITHER the MENU
	 * partition (e.g. module CEDK101) or the BODY partition (e.g. module
	 * CEDT404) depending on the module, so this method runs on `page.items`
	 * (the whole, un-partitioned item stream) rather than the post-partition
	 * body items used elsewhere.
	 *
	 * FIRES only when ALL of these conservative conditions hold (chosen to
	 * avoid ever mis-detecting an ordinary [Tab N] widget as this family):
	 *   - a PURE labelled `[Tab N]` crumb-list: a consecutive run of at
	 *     least 3 items that EQUALS the module's total `[Tab N]` count, with
	 *     every single entry labelled and ZERO empty openers (this rules out
	 *     the BLL family's [Tab N] tags, which are often left unlabelled,
	 *     and any stray widget-owned `[Tab N]` tag)
	 *   - at least 2 `[page N]` PAGE_BOUNDARY opener tags appearing directly
	 *     in the item stream (a single-file module keeps these in-stream;
	 *     every genuine `[tabs]`-widget module has ZERO in-stream `[page N]`
	 *     tags, so this excludes them automatically)
	 *   - the panel count (openers + 1) matches the crumb count (labels) —
	 *     i.e. the structure lines up cleanly
	 *
	 * On a match, this FLAGS each crumb-list item `_inquiryCrumb` (both the
	 * menu builder and the body-rendering loop then skip over these items,
	 * since their content becomes the crumb labels instead) and returns the
	 * labels in document order. Otherwise returns { on: false, labels: [] }.
	 *
	 * @param {Object} page - the page being built (reads page.items, the
	 *   full un-partitioned item stream)
	 * @param {Object} tpl - the Emit_Templates data object
	 * @returns {{on: boolean, labels: string[], suppressBundles?: Set}}
	 *
	 * Env CEDPAGE_OFF disables this whole detector.
	 */
	static detectInquiryCed(page, tpl) {
		const cfg = tpl?.body_region?.inquiry_tabs?.page_split;
		if (!cfg || cfg.enabled === false) return { on: false, labels: [] };
		if (typeof process !== "undefined" && process.env && process.env.CEDPAGE_OFF) return { on: false, labels: [] };
		const items = page.items || [];
		const isTabItem = (it) => it.type === "tag"
			&& (/^\s*tab\s*\d/i.test(String(it.text || "")) || /\btab\b/i.test(it.parse?.primary?.tag || ""));
		const isPageOpener = (it) => it.type === "tag"
			&& it.parse?.primary?.directive === "PAGE_BOUNDARY" && it.parse?.primary?.tag === "page";
		// the crumb-list = the longest consecutive run of `[Tab N]` items (≤1 non-tab gap
		// tolerated for an intervening [Module Introduction]/instruction line).
		let totalTabs = 0, emptyTabs = 0, run = [], best = [], gap = 0;
		for (const it of items) {
			if (isTabItem(it)) {
				totalTabs++;
				const label = (it.blackAfter || "").replace(/\*/g, "").trim();
				if (!label) emptyTabs++;
				run.push({ it, label });
				gap = 0;
				if (run.length > best.length) best = run.slice();
			} else { gap++; if (gap > 1) run = []; }
		}
		const pageOpeners = items.filter(isPageOpener).length;
		const pure = best.length >= 3 && best.length === totalTabs
			&& emptyTabs === 0 && best.every((r) => r.label);
		// A SECOND variant of this same family also exists: the `[Tab N]`
		// crumb-list can be CONSUMED by a `[tabs]` widget bundle instead of
		// sitting as its own free-standing item run, with the first `[page N]`
		// tag opening the first ("Introduction") panel directly — so in this
		// variant, panel count == opener count == label count, with NO separate
		// pre-page introduction segment (e.g. module CEDO102: 6 labels / 6
		// `[page N]` tags / 6 panels, all equal). The check above only accepts
		// the ORPHAN-list variant, where (openers + 1) == labels; this ALSO
		// accepts the openers == labels alignment, behind
		// page_split.consumed_crumb_list (env CEDCONSUMED_OFF) — and, when the
		// crumb-list turns out to have been consumed by a widget bundle, records
		// that bundle's index so the body-rendering loop SUPPRESSES it (its
		// labels already became the crumbs, so it must not ALSO render as a
		// widget). The strict "pure crumb-list" check plus the "at least 2
		// `[page N]` tags" check above are both still required, so a module whose
		// opener count doesn't match its label count, and every genuine
		// `[tabs]`-widget module (which has no in-stream `[page N]` tags at
		// all), correctly never fires this detector.
		const consumedOn = cfg.consumed_crumb_list !== false
			&& !(typeof process !== "undefined" && process.env && process.env.CEDCONSUMED_OFF);
		const aligned = (pageOpeners + 1) === best.length
			|| (consumedOn && pageOpeners === best.length);
		const on = pure && pageOpeners >= 2 && aligned;
		if (!on) return { on: false, labels: [] };
		const labels = [];
		const suppressBundles = new Set();
		for (const r of best) {
			r.it._inquiryCrumb = true;
			labels.push(r.label);
			if (consumedOn && r.it.consumedBy !== undefined) suppressBundles.add(r.it.consumedBy);
		}
		return { on: true, labels, suppressBundles };
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { PanelsBuilder };
