/**
 * TablesAndGrids.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * The TABLE and GRID rendering primitives, split out of ContentConverter
 * (the main content-emitting class) into their own file to keep that file's
 * size manageable. Eight statics (placeholderLinkTargets writes a hand-off
 * table's link addresses after their words, BOXLINK_OFF):
 *
 *   - contentTable(block, run, insidePlaceholder, norm)  THE table emitter — a
 *         writer table -> the kept <table> HTML (header/data rows, with
 *         structural cell-tag inline rendering), after first offering the
 *         layout-grid path below
 *   - mergedCellPlan(rows, spans)  the writer's Word merges -> each kept
 *         cell's colspan / rowspan / omitted continuation cell (TBLMERGE_OFF)
 *   - renderCellInline(cell, run, isHeader, norm)  a structural [tag] inside a
 *         KEPT data-table cell, rendered inline with its marker stripped
 *         (CELLTAG_OFF)
 *   - layoutTableGrid(rows, run, insidePlaceholder, norm)  a LAYOUT table of
 *         tagged mini-document cells -> the recursive row>col grid
 *         (LTABLE_OFF; carries a multi-row all-cells-tagged guard)
 *   - cellParts(cell)  split one cell into its "/"-separated parts
 *   - renderCellParts(cell, run, norm)  render a grid cell's parts as body
 *         elements (headings / images / grouped black text)
 *   - cellImage(text, run)  an image reference inside a cell -> the Mode-P/D
 *         placeholder markup (iStock id -> asset filename)
 *   - cellImageRefs(cell, run, cfg, links) / fillImageRefs(html, imgs)  the
 *         writer's red «Image: iStock: …:» label + address in a cell -> a
 *         token, rendered back as the cell's image (CELLIMGREF_OFF)
 *
 * WHY SEPARATE FILE:
 * These six methods were natural candidates for their own file because none
 * of them depend on ContentConverter's own internal state (its private
 * instance fields) — they only need DataService.Data (the shared global data
 * store, same as everywhere else in the app) plus one extra piece of
 * information the caller must supply explicitly: `norm`, the tag-normaliser
 * instance. `norm` is threaded through as the LAST parameter of every method
 * that needs it (three readers, plus contentTable, which simply passes it
 * through to layoutTableGrid/renderCellInline). Being self-contained like
 * this means they can live here without any awkward back-references into
 * ContentConverter.
 *
 * WHEN TO WORK HERE:
 * Any change to how a KEPT <table> is rendered, how a layout table becomes a
 * row/col grid, or how an in-cell image resolves to its placeholder markup.
 * Env toggles LTABLE_OFF and CELLTAG_OFF (both explained inline below) let
 * either behaviour be reverted for A/B comparison without a code change.
 * ===========================================================================
 */

class TablesAndGrids {

	/**
	 * THE table emitter: turns one writer-authored table block into either a
	 * kept <table> element (the normal case) or, when the table turns out to
	 * actually be a side-by-side LAYOUT rather than real tabular data, a
	 * row>col grid instead (see layoutTableGrid below).
	 *
	 * HOW: first offers the whole table to layoutTableGrid, which decides
	 * whether this is really a layout table in disguise; if it declines
	 * (returns null), falls through to the normal <table> rendering path,
	 * cell by cell.
	 *
	 * @param {Object} block - the table content block, e.g.
	 *        { rows: [ ["Header A", "Header B"], ["cell 1", "cell 2"] ] }
	 * @param {ConversionRun} run - the current conversion run (image mode, etc.)
	 * @param {boolean} [insidePlaceholder] - true when this table sits inside
	 *        an un-built interactive-widget placeholder box, where the raw
	 *        writer [tag] text must be shown as-is (a developer reference)
	 *        rather than cleaned up
	 * @param {TagNormaliser} norm - resolves a bracketed [tag] to its
	 *        canonical name; needed to detect structural tags inside cells
	 * @returns {string} the rendered <table> (or row>col grid) HTML
	 */
	static contentTable(block, run, insidePlaceholder = false, norm) {
		const t = DataService.Data.EmitTemplates.elements.table;
		const rows = block.rows ?? [];

		// LAYOUT-TABLE -> GRID. A FREE-BODY content table whose cells each embed a
		// tagged mini-document ([H3]+[Image]+[Body]+list, "/"-separated parts) is really a
		// side-by-side LAYOUT that should render as a row>col grid, not as a genuine data
		// table. Render each cell's parts back through the element renderer. Conservative:
		// SINGLE-ROW only (a 1-row table is never an MCQ/comparison DATA table);
		// placeholder/widget tables stay raw (insidePlaceholder); a widget-member tag in
		// any cell bails out of the grid path (a mis-captured flipCard/carousel stays raw).
		// Data flag: body_region.layout_table_grid. Env toggle: LTABLE_OFF (disables the
		// grid conversion, so a layout table renders as a plain <table> instead).
		// The table block's own hyperlinks travel down
		// both cell paths (grid + kept-table), so a title-anchored image cell can
		// resolve its URL exactly like its free-body counterpart (see cellImage below).
		const links = block.links ?? null;
		const grid = this.layoutTableGrid(rows, run, insidePlaceholder, norm, links, block);
		if (grid) return grid;

		// KB 05D: every content table carries the KB class form —
		// `table table-bordered` by default; a two-column COMPARISON table (every row exactly
		// two cells AND a header pair from the contrast lexicon) takes `table tableFixed` when
		// kb_class_form.comparison is enabled. The wrapper and the th header rule are unchanged.
		// Data flag: elements.table.kb_class_form. Env toggle: TBLBORDER_OFF (bare `table`).
		const cf = t.kb_class_form;
		const cfOn = !!cf && cf.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[cf.env ?? "TBLBORDER_OFF"]);
		let open = t.open;
		if (cfOn) {
			let cls = cf.default_class || "table table-bordered";
			const cmp = cf.comparison;
			// the comparison form has its own env (comparison.env = TBLCOMPARE_OFF)
			const cmpOn = cmp && cmp.enabled === true && !(typeof process !== "undefined" && process.env && process.env[cmp.env || "TBLCOMPARE_OFF"]);
			if (cmpOn && Array.isArray(cmp.lexicon) && rows.length && rows.every((cells) => cells.length === 2)) {
				const fold = (c) => Utils.Fold(String(c ?? "").replace(/<[^>]+>/g, "").replace(/\[[^\]]*\]/g, "").replace(/\*/g, "")).replace(/[^\p{L}' ]+/gu, " ").trim();
				const [a, b] = rows[0].map(fold);
				// a WHOLE-WORD match (plural 's' allowed), so "do" does not match "don't touch" (XTAS102)
				const w = (h, x) => h === x || h.startsWith(x + " ") || h === x + "s" || h.startsWith(x + "s ");
				if (cmp.lexicon.some(([x, y]) => (w(a, x) && w(b, y)) || (w(a, y) && w(b, x)))) cls = cmp.class || "table tableFixed";
			}
			open = open.replace(/<table class="table">/, `<table class="${cls}">`);
		}
		const html = [open];
		// The first row is the header row (<th>, KB 05D's column-label form) UNLESS one of its
		// cells runs to first_row_header.data_row_min_words words — a sentence is not a label, and the human
		// build treats such a row as data (every shorter row stays th). The word
		// count strips the red-run markers and the ** / __ emphasis. Env TBLHEADLONG_OFF = every first row th.
		const frh = t.first_row_header;
		const frhOn = !!frh && frh.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[frh.env ?? "TBLHEADLONG_OFF"]);
		// The VISIBLE words: the red-run markers, then any bracketed [tag] / [hover: definition] marker, then the ** / __
		// emphasis are stripped before counting (ENGJ403's one-column heading row carries two hover definitions inside
		// its brackets — seven visible words). A first row whose every non-empty cell is WHOLLY bold is the writer's own
		// header cue and stays th whatever its length (gold th 0.86 on the matched bold rows).
		const plainOf = (c) => String(c ?? "").replace(/\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu, " ").trim();
		const wordsOf = (c) => plainOf(c).replace(/\[[^\]]*\]?/g, " ").replace(/\*\*|__/g, " ").trim().split(/\s+/).filter(Boolean).length;
		const wholeBold = (c) => /^(?:\*\*|__)[\s\S]*(?:\*\*|__)$/.test(plainOf(c));
		// FREE-BODY tables only: a table inside an un-built widget's hand-off dump keeps its raw first-row form
		// (the placeholder containment — a developer reference, not page content).
		// A first row LED by the writer's red [word] beside its word (a dictionary row, cell_audio_word) is a data row.
		const awCfg = insidePlaceholder ? null : this.cellAudioWordConfig();
		const firstIsHeader = (insidePlaceholder || !frhOn || !rows.length
			|| rows[0].filter((c) => plainOf(c)).every((c) => wholeBold(c)) && rows[0].some((c) => plainOf(c))
			|| !rows[0].some((c) => wordsOf(c) >= (frh.data_row_min_words ?? 9)))
			&& !(awCfg && rows.length && this.cellAudioWord(rows[0], 0, awCfg));
		// MERGED CELLS: the writer's Word merges (the extractor's cellSpans side-channel) — a cell merged across
		// columns carries colspan, a cell merged down rows carries rowspan and its EMPTY continuation cells are
		// omitted. FREE-BODY tables only; null (the plain form) when the side-channel does not line up with these rows.
		// Data elements.table.merged_cells; env TBLMERGE_OFF.
		const mc = t.merged_cells;
		// The vertical half has its own flag (elements.table.merged_cells.rows; env TBLMERGEROWS_OFF).
		const envOn = (cfg, name) => !!cfg && cfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[cfg.env ?? name]);
		const plan = !insidePlaceholder && envOn(mc, "TBLMERGE_OFF")
			? this.mergedCellPlan(rows, block.cellSpans, envOn(mc.rows, "TBLMERGEROWS_OFF")) : null;
		// A hand-off box's raw table keeps the writer's link addresses (placeholderLinkTargets; the free body weaves its own).
		const shown = insidePlaceholder ? this.placeholderLinkTargets(rows, block.links) : rows;
		// A FIRST ROW HOLDING A PICTURE IS A DATA ROW: a header row one of whose rendered cells holds an <img> is re-tagged
		// with the data-cell form (KB 05D: a header cell is a column label). FREE-BODY only.
		// Data elements.table.first_row_header.image_row; env TBLHEADIMG_OFF.
		const imgRowOn = !insidePlaceholder && frhOn && envOn(frh.image_row, "TBLHEADIMG_OFF");
		shown.forEach((cells, r) => {
			const isHdr = r === 0 && firstIsHeader;
			const baseTpl = isHdr ? t.header_cell : t.cell;
			const rowHtml = cells.map((c, ci) => {
					const p = plan ? plan[r][ci] : null;
					if (p && p.hidden) return "";
					const attrs = !p ? ""
						: (p.colspan > 1 ? Utils.FillTemplate(mc.colspan_attr, { n: p.colspan }) : "")
						+ (p.rowspan > 1 ? Utils.FillTemplate(mc.rowspan_attr, { n: p.rowspan }) : "");
					const cellTpl = attrs ? baseTpl.replace(/^<(t[hd])\b/, `<$1${attrs}`) : baseTpl;
					// THE WRITER'S RED [word] BESIDE ITS WORD renders as the word's audio button (cellAudioWord). FREE-BODY only.
					// Data elements.table.cell_audio_word; env CELLAUDIOWORD_OFF.
					const aw = awCfg ? this.cellAudioWord(cells, ci, awCfg) : null;
					if (aw) return Utils.FillTemplate(cellTpl, { content: aw });
					// THE WRITER'S IMAGE REFERENCE IN A KEPT CELL: a red «Image: iStock: …:» label and its address render as the
					// cell's image in place (cellImageRefs); the cell is rendered from its tokenised text through the usual
					// branches below and the images are put back after. FREE-BODY only. When the cell has its paragraphs
					// (cellParagraphs), they are tokenised as paragraphs so the line form survives.
					// Data elements.table.cell_image_reference; env CELLIMGREF_OFF.
					// THE WRITER'S RED REQUEST IN A KEPT CELL («Please insert the image on page 6») renders as a Writers Note in
					// place the same way (cellRedRequests, after the image references). Data elements.table.cell_red_request;
					// env CELLREDREQ_OFF.
					const irCfg = insidePlaceholder ? null : this.cellImageRefConfig(false);
					let cc = c, irImgs = null, irParas = null, rqNotes = null, rqLinks = [];
					if (!insidePlaceholder) {
						const P0 = this.cellParagraphs(block, rows, r, ci, c);
						const SEP = "\n\u0001\n";   // whitespace on both sides: an address typed before it ends there
						let work = P0 ? P0.join(SEP) : c, changed = false;
						const ir = irCfg ? this.cellImageRefs(work, run, irCfg, norm, links, P0 ? SEP : null) : null;
						if (ir) { irImgs = ir.imgs; work = ir.text; changed = true; }
						const rq = this.cellRedRequests(work, run, norm, P0 ? SEP : null, links);
						if (rq) { rqNotes = rq.notes; rqLinks = rq.links ?? []; work = rq.text; changed = true; }
						if (changed) {
							if (P0) {
								irParas = work.split(SEP).map((x) => x.trim()).filter(Boolean);
								cc = irParas.join(DataService.Data.InputDocRules?.table_markers?.in_cell_line_break ?? " / ");
							} else cc = work;
						}
					}
					// CELL-TAG rendering: a structural [tag] inside a KEPT free-body table cell
					// is rendered INLINE (its marker stripped) instead of leaking literally into
					// the page. FREE-BODY ONLY (insidePlaceholder=false) — a table INSIDE an
					// un-built interactive-widget placeholder shows the raw WT [tag] data BY
					// DESIGN (a developer reference), so its markers must NOT be stripped there.
					// Returns null when the cell doesn't match this case, so the caller falls
					// through to the plain-text rendering below.
					const inline = insidePlaceholder ? null : this.renderCellInline(cc, run, isHdr, norm, links);
					// A FREE-BODY cell renderCellInline declines whose ' / '-joined lines include a '• '
					// bullet renders through the body's own paragraph + list machinery (a lead line → <p>, a bullet
					// run → <ul><li>) instead of the raw joined string. It weaves the same links as every other free-body cell
					// (cellLinks: web addresses only), so an asset name inside a writer's bracket stays plain text and the
					// bracket still lifts into a Writers Note. Data elements.table.cell_bullets; env TBLCELLLIST_OFF.
					const blOn = !insidePlaceholder && inline === null && !!t.cell_bullets && t.cell_bullets.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env[t.cell_bullets.env ?? "TBLCELLLIST_OFF"]);
					const blParts = blOn ? this.cellParts(cc) : [];
					const blHit = blParts.some((p) => /^•\s*\S/.test(p));
					// A FREE-BODY cell of two or more writer paragraphs (the extractor's cellParas side-channel) renders them
					// as lines joined by cell_paragraphs.joiner instead of the in-cell « / » marker; null when not that case.
					const paras = insidePlaceholder || inline !== null || blHit ? null
						: irParas ? (irParas.length >= 2 ? irParas : null)
						: this.cellParagraphs(block, rows, r, ci, c);
					const unred = (x) => x.replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "");
					const content = this.fillImageRefs(this.fillImageRefs(blHit ? ListsAndRuns.renderBlackText(this.cellNumberedParts(block, rows, r, ci, blParts).join("\n"), run, this.cellLinks(links).concat(rqLinks), true).join("")
						: inline !== null ? inline
						: paras ? paras.map((p) => ListsAndRuns.inlineMarkup(unred(p), this.cellLinks(links).concat(rqLinks), true)).join(t.cell_paragraphs.joiner)
						// red spans inside table cells: keep their text visible,
						// marked — they are usually interactive data labels
						: ListsAndRuns.inlineMarkup(unred(cc),
							insidePlaceholder ? [] : this.cellLinks(links).concat(rqLinks), !insidePlaceholder), irImgs), rqNotes, null, "CV2NOTE");   // only weave hover/definition markers (and the cell's own hyperlinks) into a FREE-BODY cell, never a placeholder dump
					// A HEADER CELL IS PLAIN: the human's <th> is almost never wholly bold (KB 05D's
					// <tr><th>Header 1</th> form), while a writer-bold header row would render <th><b>…</b></th>.
					// A header cell whose rendered content is exactly ONE <b>/<strong> span
					// (no other bold inside) drops the wrapper; <td> cells keep theirs. Free-body only.
					// Data elements.table.header_cell_plain; env THPLAIN_OFF (keeps the bold wrapper).
					let _cell = content;
					const _thp = t.header_cell_plain;
					if (isHdr && !insidePlaceholder && _thp && _thp.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env[_thp.env ?? "THPLAIN_OFF"])) {
						const _m = String(_cell).match(/^\s*<(b|strong)>([\s\S]*)<\/\1>\s*$/);
						if (_m && !/<\/?(?:b|strong)\b/.test(_m[2])) _cell = _m[2];
					}
					return Utils.FillTemplate(cellTpl, { content: _cell });
				}).join("");
			html.push(t.row_open
				+ (isHdr && imgRowOn && /<img\b/i.test(rowHtml) ? rowHtml.replace(/<th\b/g, "<td").replace(/<\/th>/g, "</td>") : rowHtml)
				+ t.row_close);
		});
		html.push(t.close);
		return html.join("\n");
	};

	/**
	 * The MERGED-CELL plan for one kept table: per cell { colspan, rowspan, hidden }, from the extractor's
	 * cellSpans side-channel (each cell's Word span width, vertical-merge state and grid column).
	 *   - span > 1                         -> colspan = span
	 *   - vmerge "continue" with NO text   -> hidden; the nearest visible cell above it at the same grid
	 *                                         column that is part of the merge gains one rowspan
	 *   - a continuation cell that carries text stays a visible cell (it is content, not a merge filler)
	 * Returns null when there is nothing to merge or when the side-channel's shape does not match the rows
	 * exactly (a caller that re-cut the rows keeps the plain form).
	 *
	 * @param {string[][]} rows - the table's cell texts
	 * @param {Object[][]} [spans] - block.cellSpans, rows-aligned { span, vmerge, col }
	 * @param {boolean} [mergeRows] - apply the vertical merges too (rowspan + omitted continuation cells)
	 * @returns {Object[][]|null}
	 */
	static mergedCellPlan(rows, spans, mergeRows = true) {
		if (!Array.isArray(spans) || spans.length !== rows.length
			|| rows.some((cells, r) => !Array.isArray(cells) || !Array.isArray(spans[r]) || spans[r].length !== cells.length)) return null;
		const plan = rows.map((cells) => cells.map(() => ({ colspan: 1, rowspan: 1, hidden: false })));
		let any = false;
		rows.forEach((cells, r) => cells.forEach((c, i) => {
			const s = spans[r][i] || {};
			if (s.span > 1) { plan[r][i].colspan = s.span; any = true; }
			if (!mergeRows || s.vmerge !== "continue" || String(c ?? "").trim()) return;
			for (let u = r - 1; u >= 0; u--) {
				const k = spans[u].findIndex((x) => x && x.col === s.col);
				if (k < 0 || !spans[u][k].vmerge) return;
				if (plan[u][k].hidden) continue;
				plan[u][k].rowspan += 1;
				plan[r][i].hidden = true;
				any = true;
				return;
			}
		}));
		return any ? plan : null;
	};

	/**
	 * DATA-TABLE CELL-TAG rendering. A structural [tag] inside a cell of a KEPT
	 * <table> (one that layoutTableGrid decided NOT to turn into a grid) is
	 * rendered INLINE — with its bracket marker stripped out — instead of
	 * leaking into the page as literal "[H2] Some text" text. Matches the
	 * reference developer's own rendering convention:
	 *   • [H1-6] / [Body, bold] text -> <b>text</b> in a DATA cell (<td>); PLAIN
	 *     text in a HEADER cell (<th> — already bold by default in the site's
	 *     CSS, so no extra <b> is needed there). For example, a matrix table's
	 *     [H2]-tagged first-column label becomes <td><b>Organisation</b></td>,
	 *     while that same tag used as an actual column header becomes plain
	 *     <th>Executive function skill</th>; a [Body, bold] cell whose text is
	 *     already wrapped in **asterisks** becomes <th><b>Line</b></th> (the
	 *     ** markdown itself supplies the bold).
	 *   • [Body] / [Text] / [list] text -> just the text (no bold).
	 *   • an image-only cell -> the in-cell <img> (via cellImage). A cell that
	 *     carries BOTH a text label AND a decorative [Image] renders only the
	 *     label and drops the image.
	 * SCOPE = STRUCTURAL tags only (an explicit allow-list in the data file). A
	 * cell whose LEADING tag is actually a widget-member tag (e.g. [front],
	 * [Card N], [Item N], [Tab N]) or a non-tag bracket (like "[tick]", or
	 * ordinary bracketed prose) is LEFT COMPLETELY ALONE — this method returns
	 * null, and the caller then renders the cell's literal text unchanged — so
	 * a genuine data table whose cells happen to contain bracketed prose can
	 * never be mis-rendered by this rule. Does NOT touch layoutTableGrid's own
	 * keep-vs-grid decision (that runs first, separately).
	 *
	 * @param {string} cell - the raw cell text (may contain a leading [tag])
	 * @param {ConversionRun} run - the current conversion run
	 * @param {boolean} isHeader - true when this cell is in the table's first
	 *        (header) row — controls the bold/plain distinction above
	 * @param {TagNormaliser} norm - resolves a bracketed [tag] to its canonical name
	 * @returns {string|null} the cell's inner HTML, or null when this cell
	 *        isn't a case this method handles (the caller should fall back to
	 *        its own literal-text rendering)
	 * Data flag: body_region.data_table_cell_tags.
	 * Env toggle: CELLTAG_OFF (disables this whole method, so every structural
	 * tag in a data-table cell leaks as literal bracketed text instead).
	 */
	static renderCellInline(cell, run, isHeader, norm, links = null) {
		const cfg = DataService.Data.EmitTemplates.body_region?.data_table_cell_tags;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.CELLTAG_OFF) return null;
		const parts = this.cellParts(cell);
		if (!parts.length) return null;
		const struct = new Set(cfg.structural_tags);
		const headingRe = new RegExp(cfg.heading_pattern ?? "^(?:h[1-6]|heading|activity heading)$");
		const canonOf = (bracket) => {
			try { return norm.Parse(`[${bracket}]`)?.primary?.tag ?? null; } catch { return null; }
		};
		// ACTIVATE only when the LEADING part is a structural [tag] (the allow-list).
		const lead = parts[0].match(/^\[([^\]]+)\]/);
		const leadCanon = lead ? canonOf(lead[1]) : null;
		if (!leadCanon || !struct.has(leadCanon)) return null;

		const labelSegs = [];   // { bold, text }
		const images = [];      // raw text for #cellImage
		for (const part of parts) {
			const m = part.match(/^\[([^\]]+)\]\s*([\s\S]*)$/);
			const bracket = m ? m[1] : "";
			const rest = m ? m[2] : part;
			const canon = m ? canonOf(bracket) : null;
			if (canon && headingRe.test(canon)) {
				labelSegs.push({ bold: true, text: (rest.trim() || norm.RenderText(part) || "") });
			} else if (canon === "body" || canon === "list") {
				labelSegs.push({ bold: /\bbold\b/i.test(bracket), text: rest });
			} else if (canon === "image") {
				images.push(rest || part);
			} else if (canon && struct.has(canon)) {
				labelSegs.push({ bold: false, text: rest });
			} else if (!canon && /^https?:\/\/\S+$/.test(part.trim())) {
				images.push(part);   // a bare-URL continuation → image adjunct (dropped when a label exists)
			} else {
				labelSegs.push({ bold: false, text: part });   // plain continuation text
			}
		}

		const labels = labelSegs.filter((s) => String(s.text).trim() !== "");
		if (labels.length) {
			// a TEXT label is present → render it; decorative [Image] parts are DROPPED.
			return labels.map((s) => {
				let inner = ListsAndRuns.inlineMarkup(String(s.text).trim(), this.cellLinks(links));   // the cell's own hyperlinks
				const wantBold = s.bold && !isHeader && (cfg.bold_in_data_cells_only !== false);
				if (wantBold && !/^<(?:b|strong)>[\s\S]*<\/(?:b|strong)>$/.test(inner)) inner = `<b>${inner}</b>`;
				return inner;
			}).join(cfg.label_join ?? " ");
		}
		// image-only cell → render the in-cell image(s)
		const out = images.map((tx) => this.cellImage(tx, run, links).join("")).filter(Boolean);
		return out.length ? out.join("") : null;
	};

	/**
	 * LAYOUT-TABLE -> GRID. Some writer tables aren't really tabular DATA at
	 * all — they're being used as a quick way to lay two or three things out
	 * side by side (e.g. an image next to a paragraph, in a single-row
	 * table). The reference developer renders those as a row>col grid of
	 * normal body elements, not as an actual <table>. This method detects
	 * that shape and, when it matches, BUILDS the grid HTML; otherwise it
	 * returns null and the caller renders a normal <table> instead.
	 *
	 * WHAT COUNTS AS A "LAYOUT" TABLE: every non-empty cell needs to open
	 * with a recognised structural [tag] (see the DETECT step below) — a
	 * genuine data table's cells are just plain data, with no tags.
	 *
	 * @param {Array<Array<string>>} rows - the table's cells, row by row, e.g.
	 *        [ ["[Image] https://...", "[Body] Some descriptive text"] ]
	 * @param {ConversionRun} run - the current conversion run
	 * @param {boolean} insidePlaceholder - true when this table sits inside an
	 *        un-built interactive-widget placeholder; layout conversion is
	 *        skipped there (the raw tag text must show through unchanged)
	 * @param {TagNormaliser} norm - resolves a bracketed [tag] to its canonical name
	 * @returns {string|null} the row>col grid HTML, or null when `rows` isn't
	 *        recognised as a layout table (the caller should render a plain
	 *        <table> instead)
	 * See Emit_Templates.body_region.layout_table_grid for the full data
	 * shape. Env toggle: LTABLE_OFF (disables this method entirely, so every
	 * table — layout or data — renders as a plain <table>).
	 */
	static layoutTableGrid(rows, run, insidePlaceholder, norm, links = null, block = null) {
		const cfg = DataService.Data.EmitTemplates.body_region?.layout_table_grid;
		if (!cfg || cfg.enabled === false || insidePlaceholder || !rows?.length) return null;
		if (typeof process !== "undefined" && process.env && process.env.LTABLE_OFF) return null;
		// DETECT: structural [tag] cells; a widget-member tag bails (mis-captured widget → raw);
		// track whether EVERY non-empty cell is a tagged mini-document (the clean-panel signal).
		const struct = new Set(cfg.structural_tags);
		let hasStruct = false, allTagged = true;
		for (const r of rows) {
			for (const cell of (r || [])) {
				if (!String(cell ?? "").trim()) continue;   // empty cells don't disqualify
				let cellTagged = false;
				for (const part of this.cellParts(cell)) {
					const m = part.match(/^\[([^\]]+)\]/);
					if (!m) continue;
					let canon = null;
					try { canon = norm.Parse(`[${m[1]}]`)?.primary?.tag ?? null; } catch { canon = null; }
					if (!canon) continue;
					if (norm.GetWidgetTypes(canon).length) return null;   // mis-captured widget → raw
					if (struct.has(canon)) { hasStruct = true; cellTagged = true; }
				}
				if (!cellTagged) allTagged = false;
			}
		}
		if (!hasStruct) return null;
		// MULTI-ROW GUARD: a 1-row table is always treated as a side-by-side panel set (see
		// above). A MULTI-ROW table, on the other hand, is only converted to a grid when
		// EVERY non-empty cell is itself a tagged mini-document — the "clean panel" case,
		// e.g. a grid of food-item cards, each cell fully tagged with its own heading/image/body.
		// A multi-row table with ANY plain, untagged cell is instead a genuine DATA table (for
		// example, a tagged header row sitting above plain data rows, or a tagged first-column
		// label next to plain data columns) and MUST stay a real <table> so its tabular
		// structure is preserved. Data flag: layout_table_grid.multi_row_requires_all_cells_tagged.
		if (rows.length !== 1 && (cfg.multi_row_requires_all_cells_tagged ?? true) && !allTagged) return null;
		// BUILD: each row → a div.row; each non-empty cell → a col rendered from its parts.
		const out = [];
		rows.forEach((r, ri) => {
			// each non-empty cell with its original column index (the cellNumbered record is rows-aligned)
			const cells = (r || []).map((c, ci) => ({ c, ci })).filter((x) => String(x.c ?? "").trim() !== "");
			if (!cells.length) return;
			const colClass = cfg.col_class_by_count?.[String(cells.length)] || cfg.col_class_default;
			const cols = cells.map(({ c, ci }) => {
				const inner = this.renderCellParts(c, run, norm, links, this.gridCellNumbered(block, rows, ri, ci)).filter(Boolean);
				return `${cfg.col_open.replace("{colClass}", colClass)}\n${inner.join("\n")}\n${cfg.col_close}`;
			});
			out.push(`${cfg.row_open}\n${cols.join("\n")}\n${cfg.row_close}`);
		});
		return out.length ? out.join("\n") : null;
	};

	/**
	 * Splits a table cell into its "/"-separated parts, with any red-span
	 * marker wrappers stripped out first. Writers combine several tagged
	 * mini-elements inside one cell by separating them with " / ", e.g. a
	 * cell reading "[H3] Wheels / [Image] https://... / [Body] Some text"
	 * splits into three parts: "[H3] Wheels", "[Image] https://...", and
	 * "[Body] Some text". Empty parts are dropped.
	 *
	 * @param {string} cell - the raw cell text
	 * @returns {string[]} the trimmed, non-empty "/"-separated parts
	 */
	/**
	 * THE WRITER'S HYPERLINK IN A TABLE CELL. The free body weaves a
	 * Writers-Template hyperlink onto its phrase (ListsAndRuns.inlineMarkup's `links`, the hyperlink_weave rule), and a
	 * free-body table cell does the same with the table block's own links, so `Email __help@netsafe.org.nz__`
	 * (mailto) or `__www.youthline.co.nz__` keeps its link as the human build does. Returns the links to weave, or [] when
	 * the rule is off. Callers only use it for FREE-BODY
	 * cells (a hand-off box's raw table dump stays untouched). Data elements.hyperlink_weave.table_cells; env CELLLINKWEAVE_OFF.
	 *
	 * @param {Array<Object>|null} links - the table block's hyperlinks [{text, target}]
	 * @returns {Array<Object>} the links to weave (possibly empty)
	 */
	/**
	 * THE HAND-OFF TABLE KEEPS ITS LINKS. A table dumped raw into a hand-off box (an un-built widget's table, the
	 * Bilingual builder's unbuilt rows) shows the writer's text for the developer, but a cell's hyperlink lives
	 * beside the text (block.links), so the image / audio file the writer linked would be lost from the box. Each
	 * link is written after its own words in the cell that holds them, in the hand-off form (`page_form`,
	 * «words [LINK: url]»): links are taken in reading order, each one's words found in the next cell that holds
	 * them, consecutive runs of one address joined into one span; a link whose words are themselves an address is
	 * already visible and stays as it is, and one whose words are in no cell is skipped. The rows are returned
	 * unchanged when there is nothing to place. Data interactive_placeholder.manifest_link_targets.page_form;
	 * env BOXLINK_OFF.
	 *
	 * @param {string[][]} rows - the table's cell texts
	 * @param {Array<Object>|null} links - the table block's hyperlinks [{text, target}], in reading order
	 * @returns {string[][]} the rows, with each placed link's address after its words
	 */
	/**
	 * A TABLE CELL'S PARAGRAPHS ARE LINES, NOT SLASHES. The extractor joins a cell's paragraphs with the in-cell
	 * marker (« / ») and records the paragraphs themselves beside the rows (block.cellParas). A writer may also type
	 * « / » inside ONE paragraph («Whenu / Strand»), so the marker alone cannot be split on: this returns the cell's
	 * own paragraphs only when the side-channel lines up with the rows and the cell string is still exactly those
	 * paragraphs joined by the marker (a cell a caller rewrote keeps its single-line form). Data
	 * elements.table.cell_paragraphs; env CELLBR_OFF.
	 *
	 * @param {Object} block - the table block (its cellParas)
	 * @param {string[][]} rows - the rows being rendered
	 * @param {number} r - row index
	 * @param {number} ci - cell index
	 * @param {string} c - the cell string being rendered
	 * @returns {string[]|null} the cell's paragraphs, or null
	 */
	static cellParagraphs(block, rows, r, ci, c) {
		const cfg = DataService.Data.EmitTemplates.elements?.table?.cell_paragraphs;
		if (!cfg || cfg.enabled === false || !cfg.joiner) return null;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "CELLBR_OFF"]) return null;
		const all = block?.cellParas;
		if (!Array.isArray(all) || all.length !== rows.length || !Array.isArray(all[r]) || all[r].length !== (rows[r]?.length ?? -1)) return null;
		const pa = all[r][ci];
		if (!Array.isArray(pa) || pa.length < 2) return null;
		const marker = DataService.Data.InputDocRules?.table_markers?.in_cell_line_break ?? " / ";
		return pa.join(marker) === String(c ?? "") ? pa : null;
	};

	/**
	 * A kept cell's Word-NUMBERED list items. The extractor gives every list paragraph in a cell the bullet prefix «• »
	 * (a cell paragraph is parsed without the numbering map) and records, beside the rows, the text of each paragraph whose
	 * Word list is numbered (block.cellNumbered). On the list path those items read «1. text», so renderBlackText builds an
	 * <ol> — the human's form for a writer's numbered cell list, where a bulleted one stays <ul>. Matched by the item's own
	 * text, so a re-cut row or a writer's « / » inside a paragraph can never number the wrong item.
	 * Data elements.table.cell_bullets.numbered; env TBLCELLOL_OFF.
	 *
	 * @param {Object} block - the table block (its cellNumbered)
	 * @param {string[][]} rows - the rows being rendered
	 * @param {number} r - row index
	 * @param {number} ci - cell index
	 * @param {string[]} parts - the cell's lines (cellParts)
	 * @returns {string[]} the lines, a numbered item's «• » turned into «1. »
	 */
	static cellNumberedParts(block, rows, r, ci, parts) {
		const cfg = DataService.Data.EmitTemplates.elements?.table?.cell_bullets?.numbered;
		if (!cfg || cfg.enabled === false) return parts;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "TBLCELLOL_OFF"]) return parts;
		const all = block?.cellNumbered;
		if (!Array.isArray(all) || all.length !== rows.length || !Array.isArray(all[r]) || all[r].length !== (rows[r]?.length ?? -1)) return parts;
		const nums = all[r][ci];
		if (!Array.isArray(nums) || !nums.length) return parts;
		const unred = (x) => String(x ?? "").replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "").trim();
		const set = new Set(nums.map(unred));
		return parts.map((p) => (set.has(p) ? p.replace(/^•\s+/, "1. ") : p));
	};

	/**
	 * A LAYOUT-GRID cell's Word-numbered list items (layoutTableGrid → renderCellParts): the cell's cellNumbered record as a
	 * set of item texts (red markers stripped, «• » prefix kept — the form renderCellParts compares), or null when the rule
	 * is off or the record does not line up with the rows. Data elements.table.cell_bullets.numbered.grid; env
	 * GRIDCELLOL_OFF (and TBLCELLOL_OFF).
	 *
	 * @param {Object|null} block - the table block (its cellNumbered)
	 * @param {string[][]} rows - the rows being rendered
	 * @param {number} r - row index
	 * @param {number} ci - cell index (in the row's own cells, empty ones included)
	 * @returns {Set<string>|null}
	 */
	static gridCellNumbered(block, rows, r, ci) {
		const num = DataService.Data.EmitTemplates.elements?.table?.cell_bullets?.numbered;
		const on = (c, name) => !!c && c.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[c.env ?? name]);
		if (!on(num, "TBLCELLOL_OFF") || !on(num.grid, "GRIDCELLOL_OFF")) return null;
		const all = block?.cellNumbered;
		if (!Array.isArray(all) || all.length !== rows.length || !Array.isArray(all[r]) || all[r].length !== (rows[r]?.length ?? -1)) return null;
		const nums = all[r][ci];
		if (!Array.isArray(nums) || !nums.length) return null;
		const unred = (x) => String(x ?? "").replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "").trim();
		// a numbered paragraph with a soft line break inside it («• Prototype → Sketch a possible solution / create a first
		// draft») reaches renderCellParts as two parts: its first segment is the list item
		const marker = DataService.Data.InputDocRules?.table_markers?.in_cell_line_break ?? " / ";
		const set = new Set();
		for (const n of nums.map(unred)) { set.add(n); set.add(n.split(marker)[0].trim()); }
		return set;
	};

	static placeholderLinkTargets(rows, links) {
		const cfg = DataService.Data.EmitTemplates.interactive_placeholder?.manifest_link_targets;
		if (!cfg || cfg.enabled === false || !cfg.page_form || !Array.isArray(links) || !links.length) return rows;
		if (typeof process !== "undefined" && process.env && process.env[cfg.page_env ?? "BOXLINK_OFF"]) return rows;
		const addressRe = new RegExp(cfg.address_text_pattern ?? "^(?:https?://|www\\.)\\S+$", "i");
		const text = rows.map((cells) => (Array.isArray(cells) ? cells.map((c) => String(c ?? "")) : cells));
		const refs = [];
		text.forEach((cells, r) => { if (Array.isArray(cells)) cells.forEach((_, ci) => refs.push([r, ci])); });
		const spans = new Map();   // "r,ci" → [{start, end, url}]
		const keep = (s) => { const k = `${s.r},${s.ci}`; if (!spans.has(k)) spans.set(k, []); spans.get(k).push(s); };
		let at = 0, off = 0, cur = null;
		for (const l of links) {
			const url = String(l?.target ?? "").trim();
			const words = String(l?.text ?? "");
			if (!/^https?:\/\//i.test(url) || !/[\p{L}\p{N}]/u.test(words) || addressRe.test(words.trim())) continue;
			if (cur && cur.url === url) {   // the next run of the open link
				const t = text[cur.r][cur.ci];
				const p = t.indexOf(words, cur.end);
				if (p >= 0 && /^[\s*_]*$/.test(t.slice(cur.end, p))) { cur.end = p + words.length; off = cur.end; continue; }
			}
			if (cur) { keep(cur); cur = null; }
			for (let k = at; k < refs.length; k++) {
				const [r, ci] = refs[k];
				const p = text[r][ci].indexOf(words, k === at ? off : 0);
				if (p < 0) continue;
				at = k; off = p + words.length;
				cur = { r, ci, start: p, end: off, url };
				break;
			}
		}
		if (cur) keep(cur);
		if (!spans.size) return rows;
		return text.map((cells, r) => (Array.isArray(cells) ? cells.map((t, ci) => {
			const list = (spans.get(`${r},${ci}`) ?? []).sort((a, b) => b.start - a.start);
			let s = t, floor = Infinity;
			for (const sp of list) {
				if (sp.end > floor) continue;   // overlapping span: keep the later one
				s = s.slice(0, sp.start) + Utils.FillTemplate(cfg.page_form, { text: s.slice(sp.start, sp.end), url: sp.url }) + s.slice(sp.end);
				floor = sp.start;
			}
			return s;
		}) : cells));
	};

	static cellLinks(links) {
		const c = DataService.Data.EmitTemplates.elements?.hyperlink_weave?.table_cells;
		if (!c || c.enabled === false || !Array.isArray(links) || !links.length) return [];
		if (typeof process !== "undefined" && process.env && process.env[c.env ?? "CELLLINKWEAVE_OFF"]) return [];
		// only a link whose VISIBLE text is itself a web / email address (the block's list also carries image, file and video
		// asset references and phrases that recur elsewhere in the table — data anchor_pattern, explained in its note)
		if (!c.anchor_pattern) return links;
		const re = new RegExp(c.anchor_pattern, "i");
		// an anchor that ends in a file extension (`Tukutuku.jpg`) is a file
		// name, not an address — data exclude_pattern
		const ex = c.exclude_pattern ? new RegExp(c.exclude_pattern, "i") : null;
		// a phrase link to an ordinary web page («online contact form» → netsafe.org.nz/report) is woven too
		// (table_cells.phrase_links; env CELLPHRASELINK_OFF): not an asset host, not a file
		const pl = c.phrase_links;
		const plOn = !!pl && pl.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[pl.env ?? "CELLPHRASELINK_OFF"]);
		const hostRe = plOn && pl.asset_host_pattern ? new RegExp(pl.asset_host_pattern, "i") : null;
		const phrase = (l, t) => {
			if (!plOn) return false;
			const target = String(l?.target ?? "").trim();
			if (!/^https?:\/\//i.test(target) || (hostRe && hostRe.test(target)) || (ex && (ex.test(t) || ex.test(target.replace(/[?#].*$/, ""))))) return false;
			return t.split(/\s+/).filter((w) => /[\p{L}\p{N}]/u.test(w)).length >= (pl.min_words ?? 2);
		};
		return links.filter((l) => { const t = String(l?.text ?? "").trim(); return (re.test(t) && !(ex && ex.test(t))) || phrase(l, t); });
	};

	static cellParts(cell) {
		// a run of line-break markers (an emptied line between them) is one break, so no marker is left on the next line
		// (soft_break_lead.cell_parts; env CELLSLASH_OFF)
		const cp = DataService.Data.EmitTemplates?.elements?.soft_break_lead?.cell_parts;
		const run = !!cp && cp.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[cp.env || "CELLSLASH_OFF"]);
		// red letters typed INSIDE a word («t🔴ea🔴ch») keep the word whole: a marker touching a letter outside it loses the
		// extractor's padding space on that side (inline_red_words.cell_glue; env CELLREDGLUE_OFF)
		const gl = DataService.Data.EmitTemplates?.elements?.inline_red_words?.cell_glue;
		const glue = !!gl && gl.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[gl.env || "CELLREDGLUE_OFF"]);
		let s = String(cell ?? "");
		if (glue) s = s.replace(/(\p{L})?\u{1f534}\[RED TEXT\] (\p{L}{1,5}) \[\/RED TEXT\]\u{1f534}(\p{L})?/gu, (m, pre, red, post) => (!pre && !post) ? m
			: (pre ?? "") + "\u{1f534}[RED TEXT]" + (pre ? "" : " ") + red + (post ? "" : " ") + "[/RED TEXT]\u{1f534}" + (post ?? ""));
		return s
			.replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "")
			.split(run ? /\s+\/(?:\s+\/)*\s+/ : /\s+\/\s+/).map((p) => p.trim()).filter(Boolean);
	};

	/**
	 * Renders one layout-table cell as a sequence of body elements: each
	 * "/"-separated [tag] part (see cellParts above) is dispatched exactly
	 * like a free-standing body element would be —
	 *   - a heading tag becomes <hN> (the writer's own heading digit, shifted
	 *     by the standard body_shift amount; the page-wide heading
	 *     re-leveller normalises it further afterwards)
	 *   - an [image] tag goes through the image emitter (cellImage)
	 *   - body/list/bullet/plain text goes through
	 *     ListsAndRuns.renderBlackText, so consecutive "• " bullet parts
	 *     group together into one <ul> instead of becoming separate
	 *     paragraphs
	 * Stray divider tokens a writer sometimes leaves between parts (a bare
	 * "=" or an em dash "—" with nothing else on it) are skipped entirely.
	 *
	 * @param {string} cell - the raw cell text
	 * @param {ConversionRun} run - the current conversion run
	 * @param {TagNormaliser} norm - resolves a bracketed [tag] to its canonical name
	 * @returns {string[]} the rendered HTML for each element found in the cell
	 */
	static renderCellParts(cell, run, norm, links = null, numbered = null) {
		// THE WRITER'S IMAGE REFERENCE IN A LAYOUT-GRID CELL: a red «Image: iStock: …:» label and its address render as the
		// image in place (cellImageRefs), before the red-note rule below could print a wholly red reference as a Writers
		// Note. Data elements.table.cell_image_reference.grid; env GRIDIMGREF_OFF (and CELLIMGREF_OFF).
		const irCfg = this.cellImageRefConfig(true);
		const ir = irCfg ? this.cellImageRefs(cell, run, irCfg, norm, links) : null;
		if (ir) {
			// the tokens are black text now, so the second pass renders the cell's parts as usual; each image goes back
			// where its token landed, and one the rendering lost goes after the cell's parts
			const placed = new Set();
			const out = this.renderCellParts(ir.text, run, norm, links, numbered).map((h) => this.fillImageRefs(h, ir.imgs, placed));
			ir.imgs.forEach((img, i) => { if (!placed.has(i)) out.push(img); });
			return out;
		}
		const tpl = DataService.Data.EmitTemplates;
		const skipRe = new RegExp(tpl.body_region.layout_table_grid.skip_part_pattern ?? "^[=\\s]*$");
		const out = [];
		let buf = [];
		// the cell's text and headings weave the table block's own hyperlinks (see cellLinks)
		const cl = this.cellLinks(links);
		const flush = () => { if (buf.length) { out.push(...ListsAndRuns.renderBlackText(buf.join("\n"), run, cl)); buf = []; } };
		// THE RED NOTE IN A LAYOUT CELL. cellParts strips the red markers, so a
		// part the writer typed wholly in RED with no [tag] of its own — a note to the developer beside the picture ("please
		// add eyes, mouth and license plate", "[Image like this – kombi van parked in Auckland", ENGS202) — would render as a
		// learner paragraph. Such a part renders as the writer's red note instead, the free body's own form
		// (NotesAndComments.redFlag kind "cs"). The raw cell is split the same way; any mismatch keeps the plain rendering.
		// Data body_region.layout_table_grid.red_part_note; env CELLREDNOTE_OFF (and TABLEHOVER_OFF, the master toggle).
		const rpn = tpl.body_region.layout_table_grid.red_part_note;
		const rpnOn = rpn && rpn.enabled !== false
			&& !(typeof process !== "undefined" && process.env && (process.env[rpn.env ?? "CELLREDNOTE_OFF"] || process.env.TABLEHOVER_OFF));
		const parts = this.cellParts(cell);
		let redOnly = null;
		if (rpnOn) {
			const raw = String(cell ?? "").split(/\s+\/\s+/).map((p) => p.trim()).filter((p) =>
				p.replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "").trim());
			if (raw.length === parts.length) {
				redOnly = raw.map((p) => /\u{1f534}\[RED TEXT\]/u.test(p)
					&& !p.replace(/\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu, "").trim());
			}
		}
		parts.forEach((part, pi) => {
			const m = part.match(/^\[([^\]]+)\]\s*([\s\S]*)$/);
			let canon = null, rest = part;
			if (m) {
				try { canon = norm.Parse(`[${m[1]}]`)?.primary?.tag ?? null; } catch { canon = null; }
				rest = m[2];
			}
			if (!canon && redOnly && redOnly[pi] && /\p{L}/u.test(part)) {
				flush();
				out.push(NotesAndComments.redFlag(part.trim(), run, "cs"));
				return;
			}
			if (canon && /^(?:h[1-5]|heading|activity heading)$/.test(canon)) {
				flush();
				const digit = /^h\d$/.test(canon) ? parseInt(canon[1], 10) : 2;
				const shifted = Math.min(Math.max(digit + tpl.elements.heading.logical_to_element.body_shift, 2), 5);
				const text = (rest.trim() || norm.RenderText(part) || "").replace(/\*/g, "").trim();
				if (text) out.push(`<h${shifted}>${ListsAndRuns.inlineMarkup(text, cl)}</h${shifted}>`);
			} else if (canon === "image") {
				flush();
				out.push(...this.cellImage(rest, run, links));
			} else {
				let content = canon ? rest : part;
				// a Word-numbered item reads «1. » so its run is an <ol> (gridCellNumbered; cell_bullets.numbered.grid)
				if (numbered && numbered.has(content.trim())) content = content.trim().replace(/^•\s+/, "1. ");
				if (content.trim() && !skipRe.test(content.trim())) buf.push(content);
			}
		});
		flush();
		return out;
	};

	/**
	 * Renders an image reference found inside a layout-table cell. The cell
	 * text is typically a pasted asset reference such as
	 * "iStock. https://www.istockphoto.com/photo/...-gm1234567890-...jpg" —
	 * that whole description is the asset REFERENCE the writer pasted in, not
	 * text meant for the learner to read, so it is consumed here and never
	 * shown as visible page text. When the URL contains a recognisable iStock
	 * id, the filename is derived from it; otherwise a filename is slugified
	 * from whatever descriptive text remains. See MediaBuilder.image for the
	 * same Mode P (visible placeholder) / Mode D (direct image) split applied
	 * to a normal, free-body [image] tag.
	 *
	 * @param {string} text - the cell's raw text (expected to contain a URL)
	 * @param {ConversionRun} run - the current conversion run (drives imageMode)
	 * @returns {string[]} one or two HTML fragments — the placeholder/image
	 *          markup (and, in Mode P, a second commented-out real reference)
	 */
	static cellImage(text, run, links = null) {
		const tpl = DataService.Data.EmitTemplates.image;
		let url = text.match(/https?:\/\/[^\s\]\)"<>]+/)?.[0] ?? "";
		// TITLE-ANCHORED CELL IMAGE. A writer often
		// authors a table-cell image BY TITLE: the cell text is the asset's title, and
		// the URL lives only in the docx hyperlink's TARGET (which the extractor stores
		// on the table BLOCK, not in the cell text). Free-body images already resolve
		// this form through it.block.links; without this step the cell path would slugify
		// the title into a wrong filename (SCCH302's Solutions/Suspensions table:
		// "clear-yellow-liquid-is-poured-into-beake.jpg" instead of
		// iStock-1321097020.jpg). When the cell text holds NO URL, find the table
		// block's hyperlink whose folded anchor TEXT sits inside the folded cell text
		// (longest anchor wins, so two image cells in one row each find their own
		// link) and use its target. Data flag: body_region.cell_image_link_match.
		// Env toggle: CELLIMGLINK_OFF (title-anchored cells fall back to slug filenames).
		if (!url && links && links.length) {
			const cfg = DataService.Data.EmitTemplates.body_region?.cell_image_link_match;
			const on = cfg && cfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.CELLIMGLINK_OFF);
			if (on) {
				const fold = (s) => String(s ?? "").toLowerCase().replace(/\s+/g, " ").trim();
				const ft = fold(text);
				let best = null;
				for (const l of links) {
					const a = fold(l.text);
					if (!l.target || /^https?:\/\//i.test(String(l.text ?? "").trim())) continue;
					if (a.length < (cfg.min_anchor_length ?? 8)) continue;
					if (ft.includes(a) && (!best || a.length > best.len)) best = { len: a.length, target: l.target };
				}
				if (best) url = best.target;
			}
		}
		const istockId = url.match(/gm-?(\d{6,10})/)?.[1] ?? null;
		const filename = istockId
			? Utils.FillTemplate(tpl.filename_rules.istock, { id: istockId })
			: `${Utils.Slugify(text.replace(/https?:\/\/\S+/g, "").replace(/^\s*istock[.:]?/i, "").trim() || "image") || "image"}.jpg`;
		const label = istockId ? `iStock-${istockId}` : "image";
		if (run.imageMode === "P") {
			return [MediaBuilder.FinishImg(Utils.FillTemplate(tpl.mode_P.visible, { label }), url, istockId, run),
				MediaBuilder.FinishImg(Utils.FillTemplate(tpl.mode_P.comment, { filename }), url, istockId, run)];
		}
		return [MediaBuilder.FinishImg(Utils.FillTemplate(tpl.mode_D.visible, { filename }), url, istockId, run)];
	};

	/**
	 * Is the cell image-reference rule on for this caller? The kept-table cell reads
	 * elements.table.cell_image_reference (env CELLIMGREF_OFF); the layout-grid cell also needs its grid block
	 * (env GRIDIMGREF_OFF).
	 *
	 * @param {boolean} grid - true for the layout-grid caller (renderCellParts)
	 * @returns {Object|null} the data block when on, else null
	 */
	static cellImageRefConfig(grid) {
		const cfg = DataService.Data.EmitTemplates.elements?.table?.cell_image_reference;
		const on = (c, name) => !!c && c.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[c.env ?? name]);
		if (!on(cfg, "CELLIMGREF_OFF")) return null;
		if (grid && !on(cfg.grid, "GRIDIMGREF_OFF")) return null;
		return cfg;
	};

	/**
	 * THE WRITER'S IMAGE REFERENCE IN A TABLE CELL. A writer types the picture a cell should hold as a red label with no
	 * bracket («Image: iStock: symbol on speech bubble:», «Image RHS: iStock: …:») and the stock or source address after it.
	 * Each such red run (consecutive red spans read as one), together with its address — inside the run, typed right after
	 * it on the same line, on the cell's next line, or, with no address typed, the table link whose words sit inside the run
	 * (or make up the rest of its line) — is replaced by a token; the token's image is the cell's own image emitter
	 * (cellImage). The caller renders the tokenised cell through its usual path and puts the images in with fillImageRefs.
	 * Text after the address on the same line stays. A run with a bracket, or with no resolvable address, is left alone,
	 * and so is a cell that carries the writer's own [image] tag (that tag's path renders the cell's image).
	 * Data elements.table.cell_image_reference {label_pattern, address_pattern}.
	 *
	 * @param {string} cell - the raw cell text (red markers in)
	 * @param {ConversionRun} run - the current conversion run (image mode)
	 * @param {Object} cfg - the data block (cellImageRefConfig)
	 * @param {TagNormaliser} norm - resolves a bracketed [tag] to its canonical name
	 * @param {Array<Object>|null} [links] - the table block's hyperlinks [{text, target}]
	 * @param {string|null} [sep] - the separator the caller joined the cell's paragraphs with (default the « / » marker);
	 *        it must hold whitespace on both sides so an address typed before it ends there
	 * @returns {{text: string, imgs: string[]}|null} the tokenised cell and one image per token, or null when none
	 */
	static cellImageRefs(cell, run, cfg, norm, links = null, sep = null) {
		const s = String(cell ?? "");
		if (!cfg || !/\u{1f534}\[RED TEXT\]/u.test(s)) return null;
		if (this.cellHasImageTag(s, norm, sep)) return null;
		// the semicolon form of the label (cell_image_reference.semicolon_label; env IMGLABELSEMI_OFF)
		const semi = cfg.semicolon_label;
		const semiOn = !!semi && semi.enabled !== false && !!semi.label_pattern
			&& !(typeof process !== "undefined" && process.env && process.env[semi.env ?? "IMGLABELSEMI_OFF"]);
		const labelRe = new RegExp(semiOn ? semi.label_pattern : cfg.label_pattern, "i");
		const addr = cfg.address_pattern ?? "https?://[^\\s<>\"\\]\\[]+";
		const addrRe = new RegExp(addr, "i");
		const esc = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
		const sepRe = sep ? esc(sep) : "\\s\\/";
		const sameLine = new RegExp(`^[ \\t]*(${addr})`, "i");
		const nextLine = new RegExp(`^\\s*${sep ? esc(sep) : "\\/"}\\s*(${addr})[ \\t]*(?=${sepRe}|\\n|$)`, "i");
		const fold = (x) => String(x ?? "").toLowerCase().replace(/\s+/g, " ").trim();
		const webLinks = (links ?? []).filter((l) => /^https?:\/\//i.test(String(l?.target ?? "")));
		const runRe = /(?:\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534})+/gu;
		const hits = [];
		for (const m of s.matchAll(runRe)) {
			const inner = m[0].replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "");
			if (/[[\]]/.test(inner) || !labelRe.test(inner)) continue;
			let end = m.index + m[0].length;
			let url = inner.match(addrRe)?.[0] ?? null;
			const after = s.slice(end);
			if (!url) {
				const a = after.match(sameLine) ?? after.match(nextLine);
				if (a) { url = a[1]; end += a[0].length; }
			}
			if (!url && webLinks.length) {
				// a title-anchored reference: the link's words inside the run, or the rest of the run's line made of link words
				const fi = fold(inner);
				let best = null;
				for (const l of webLinks) {
					const t = fold(l.text);
					if (t.length >= 8 && fi.includes(t) && (!best || t.length > best.len)) best = { len: t.length, target: l.target };
				}
				if (best) url = best.target;
				else {
					const lineEnd = after.search(sep ? new RegExp(`${esc(sep)}|\\n`) : /\s\/\s|\n/);
					const line = lineEnd < 0 ? after : after.slice(0, lineEnd);
					let rest = line, first = null;
					for (const l of webLinks.slice().sort((x, y) => String(y.text ?? "").length - String(x.text ?? "").length)) {
						const t = String(l.text ?? "").trim();
						if (t.length < 2 || !rest.includes(t)) continue;
						if (!first && t.length >= 8) first = l.target;
						rest = rest.split(t).join(" ");
					}
					if (first && !/[\p{L}\p{N}]/u.test(rest)) { url = first; end += line.length; }
				}
			}
			if (!url) continue;
			const desc = inner.replace(new RegExp(addr, "gi"), " ").replace(labelRe, " ")
				.replace(/^\s*(?:i?stock|getty\s*images?|shutterstock)\b[^:;]{0,30}[:;]\s*/i, " ").replace(/[\s:;]+$/, "").replace(/\s+/g, " ").trim();
			let img = this.cellImage(`${desc} ${url}`, run, links).join("");
			// THE NOTE ABOUT THE PICTURE: the cell's next line wholly red, no bracket («(image needs to be flipped vertically as
			// above)») is the writer's note on this picture — it renders as a Writers Note beside the image (the layout cell's
			// red-note form, NotesAndComments.redFlag kind "cs"). Data cell_image_reference.trailing_note.
			if (cfg.trailing_note !== false) {
				const tn = s.slice(end).match(new RegExp(`^\\s*${sep ? esc(sep) : "\\/"}\\s*((?:\\u{1f534}\\[RED TEXT\\][\\s\\S]*?\\[\\/RED TEXT\\]\\u{1f534})+)[ \\t]*(?=${sepRe}|\\n|$)`, "u"));
				const note = tn ? tn[1].replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "").trim() : "";
				if (note && !/[[\]]/.test(note) && /\p{L}/u.test(note)) {
					img += NotesAndComments.redFlag(note, run, "cs");
					end += tn[0].length;
				}
			}
			hits.push({ start: m.index, end, img });
		}
		if (!hits.length) return null;
		let text = "", at = 0;
		hits.forEach((h, i) => { text += s.slice(at, h.start) + `⟦CV2IMG${i}⟧`; at = h.end; });
		text += s.slice(at);
		return { text, imgs: hits.map((h) => h.img) };
	};

	/**
	 * Puts the images of cellImageRefs back into a rendered cell: a token alone in a paragraph replaces the paragraph,
	 * any other token is replaced where it stands, and a token the rendering lost is added at the end (the image is never
	 * dropped).
	 *
	 * @param {string} html - the rendered cell content
	 * @param {string[]|null} imgs - the images, by token number
	 * @param {Set<number>|null} [placed] - for a caller that renders a cell in several fragments: records each token put
	 *        back, and a token not in this fragment is NOT added at the end (the caller adds the lost ones once)
	 * @param {string} [prefix] - the token family (CV2IMG for cellImageRefs, CV2NOTE for cellRedRequests)
	 * @returns {string}
	 */
	static fillImageRefs(html, imgs, placed = null, prefix = "CV2IMG") {
		if (!imgs || !imgs.length) return html;
		let out = String(html ?? "");
		imgs.forEach((img, i) => {
			const tok = `⟦${prefix}${i}⟧`;
			const alone = new RegExp(`<p>\\s*${tok}\\s*</p>`);
			if (alone.test(out)) out = out.replace(alone, img);
			else if (out.includes(tok)) out = out.split(tok).join(img);
			else { if (!placed) out += img; return; }
			if (placed) placed.add(i);
		});
		return out;
	};

	/**
	 * Does the cell carry the writer's own [image] tag (a line that opens with a bracket resolving to "image")? That tag's
	 * path builds the cell's picture from the cell text, so the cell-token rules (cellImageRefs, cellRedRequests) stand aside.
	 *
	 * @param {string} cell - the cell text
	 * @param {TagNormaliser} norm
	 * @param {string|null} [sep] - the paragraph separator the caller joined the cell with (default the « / » marker)
	 * @returns {boolean}
	 */
	static cellHasImageTag(cell, norm, sep = null) {
		const s = String(cell ?? "");
		return this.cellParts(sep ? s.split(sep).join(" / ") : s).some((p) => {
			const m = p.match(/^\[([^\]]+)\]/);
			if (!m) return false;
			try { return norm?.Parse(`[${m[1]}]`)?.primary?.tag === "image"; } catch { return false; }
		});
	};

	/**
	 * The cell_audio_word block when it is on (null when off or absent). Env CELLAUDIOWORD_OFF.
	 *
	 * @returns {Object|null}
	 */
	static cellAudioWordConfig() {
		const cfg = DataService.Data.EmitTemplates?.elements?.table?.cell_audio_word;
		return cfg && cfg.enabled !== false && cfg.form
			&& !(typeof process !== "undefined" && process.env && process.env[cfg.env ?? "CELLAUDIOWORD_OFF"]) ? cfg : null;
	}

	/**
	 * THE WRITER'S RED [word] BESIDE ITS WORD (a te reo dictionary row: «[kuia]» | «kuia» | its meaning). The cell is wholly
	 * red and only a bracketed word; the next cell is plain text folding to the same word (within max_edit letters — the
	 * writer's «[teketeko]» beside «tekoteko»). Returns the audio button named from the VISIBLE word (folded, its words
	 * joined by name_joiner), or null when the cell is not that case. Data elements.table.cell_audio_word.
	 *
	 * @param {string[]} cells - the row's raw cell texts (red markers in)
	 * @param {number} ci - the cell's column
	 * @param {Object|null} cfg - cellAudioWordConfig()
	 * @returns {string|null}
	 */
	static cellAudioWord(cells, ci, cfg) {
		if (!cfg || ci + 1 >= cells.length) return null;
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		const raw = String(cells[ci] ?? "");
		if (!raw.includes("\u{1f534}") || raw.replace(RED, "").trim()) return null;
		const m = raw.replace(RED, "$1").replace(/\s+/g, " ").trim().match(/^\[\s*([^\[\]]+?)\s*\]$/);
		if (!m) return null;
		const next = String(cells[ci + 1] ?? "");
		if (/\u{1f534}|[\[\]]/u.test(next)) return null;
		const word = next.replace(/\*\*|__/g, "").replace(/\s+/g, " ").trim();
		const max = cfg.max_words ?? 4, count = (x) => x.split(" ").filter(Boolean).length;
		if (!word || count(word) > max || count(m[1]) > max) return null;
		const key = (x) => Utils.Fold(x).toLowerCase().replace(/[^a-z0-9]+/g, "");
		const a = key(m[1]), b = key(word);
		if (!a || !b) return null;
		// letters apart (Levenshtein), allowed at most max_edit and a quarter of the shorter word
		const d = Array.from({ length: b.length + 1 }, (_, j) => j);
		for (let i = 1; i <= a.length; i++) {
			let prev = d[0]; d[0] = i;
			for (let j = 1; j <= b.length; j++) {
				const tmp = d[j];
				d[j] = Math.min(d[j] + 1, d[j - 1] + 1, prev + (a[i - 1] === b[j - 1] ? 0 : 1));
				prev = tmp;
			}
		}
		if (d[b.length] > Math.min(cfg.max_edit ?? 2, Math.floor(Math.min(a.length, b.length) / 4))) return null;
		const name = Utils.Fold(word).toLowerCase().replace(/[^a-z0-9]+/g, " ").trim().split(" ").join(cfg.name_joiner ?? "-");
		return Utils.FillTemplate(cfg.form, { name });
	}

	/**
	 * THE WRITER'S RED REQUEST IN A TABLE CELL. Each red run (consecutive red spans read as one) with no bracket, at least
	 * min_words words and an instruction cue (the free body's own test, norm.HasInstructionCue) is replaced by a token whose
	 * fragment is the Writers Note (NotesAndComments.redFlag kind "cs"); the caller renders the tokenised cell and puts the
	 * notes back with fillImageRefs(…, "CV2NOTE"). A red run with no cue stays as it is (a data label the learner reads).
	 * Data elements.table.cell_red_request; env CELLREDREQ_OFF.
	 *
	 * @param {string} cell - the cell text (red markers in; image references already tokenised)
	 * @param {ConversionRun} run
	 * @param {TagNormaliser} norm
	 * @returns {{text: string, notes: string[]}|null}
	 */
	static cellRedRequests(cell, run, norm, sep = null, links = null) {
		const cfg = DataService.Data.EmitTemplates.elements?.table?.cell_red_request;
		if (!cfg || cfg.enabled === false || !norm) return null;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "CELLREDREQ_OFF"]) return null;
		let s = String(cell ?? "");
		if (!/\u{1f534}\[RED TEXT\]/u.test(s)) return null;
		// a cell that carries the writer's own [image] tag builds its picture from the cell text: left alone
		if (this.cellHasImageTag(s, norm, sep)) return null;
		// a red link request whose address is the following word's own hyperlink («[Link 2, to https://…/kiekie/] kiekie», the
		// word linked to the same address in the table's links) is redundant: removed before the requests are read, and that
		// link is handed back (links) for the cell's weave. Data cell_red_request.redundant_link; env CELLREDLINK_OFF.
		const woven = [];
		const rl = cfg.redundant_link;
		if (rl && rl.enabled !== false && rl.pattern && Array.isArray(links) && links.length
			&& !(typeof process !== "undefined" && process.env && process.env[rl.env ?? "CELLREDLINK_OFF"])) {
			const rlRe = new RegExp(rl.pattern, "i");
			const addr = (u) => String(u ?? "").trim().replace(/[)\].,]+$/, "").replace(/\/$/, "").toLowerCase();
			s = s.replace(/(?:\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534})+/gu, (run, at) => {
				const inner = run.replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").replace(/\s+/g, " ").trim();
				const m = inner.match(rlRe);
				if (!m) return run;
				const after = s.slice(at + run.length, at + run.length + (rl.lookahead_chars ?? 160)).trimStart();
				const lk = links.find((l) => {
					const t = String(l?.text ?? "").trim();
					return t && after.startsWith(t) && !/\p{L}/u.test(after.charAt(t.length)) && addr(l?.target) === addr(m[1]);
				});
				if (!lk) return run;
				woven.push(lk);
				return " ";
			});
			if (woven.length && !/\u{1f534}\[RED TEXT\]/u.test(s)) return { text: s, notes: [], links: woven };
		}
		const minW = cfg.min_words ?? 3;
		// THE BRACKETED FORM: a red run that is exactly one bracketed request of at least bracketed.min_words letter-words
		// and no web address («[students type here]») — the bracket is the writer's instruction mark, no cue word needed.
		// Data elements.table.cell_red_request.bracketed; env CELLREDBRACKET_OFF.
		const bk = cfg.bracketed;
		const RUNS = /(?:\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534})+/gu;
		const innerOf = (r) => r.replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "").replace(/\s+/g, " ").trim();
		const bkFits = (inner) => /^\[[^[\]]+\]$/.test(inner) && !/https?:\/\/|www\./i.test(inner)
			&& !(bk.exclude_pattern && new RegExp(bk.exclude_pattern, "i").test(inner))
			&& !(bk.skip_resolved_tags !== false && (() => { try { return !!norm.Parse(inner)?.primary; } catch { return true; } })())
			&& inner.slice(1, -1).split(" ").filter((w) => /\p{L}/u.test(w)).length >= (bk.min_words ?? 2);
		// only a cell whose every bracketed red run qualifies and whose other text holds no bracket the tag vocabulary
		// resolves: a cell that also carries a real tag, red or black («[insert audio]» typed as a link), is left to the
		// cell's own handling
		const restResolves = () => {
			const rest = s.replace(RUNS, (r) => (bkFits(innerOf(r)) ? " " : r)).replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, " ");
			for (const t of rest.matchAll(/\[([^\]\n]{1,60})\]/g)) {
				try { if (norm.Parse(`[${t[1]}]`)?.primary) return true; } catch { return true; }
			}
			return false;
		};
		const bkOn = !!bk && bk.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[bk.env ?? "CELLREDBRACKET_OFF"])
			&& [...s.matchAll(RUNS)].map((m) => innerOf(m[0])).every((inner) => !/[[\]]/.test(inner) || bkFits(inner))
			&& !restResolves();
		const hits = [];
		for (const m of s.matchAll(RUNS)) {
			const inner = innerOf(m[0]);
			if (!inner) continue;
			if (bkOn && bkFits(inner)) {
				// a bracket with the writer's words still to come in its paragraph («The artist worked [phrase highlighter]
				// in a bright …») puts its note at the paragraph's end, so the note never splits the sentence
				const stop = sep && s.indexOf(sep, m.index + m[0].length) >= 0 ? s.indexOf(sep, m.index + m[0].length) : s.length;
				const after = s.slice(m.index + m[0].length, stop).replace(RUNS, " ");
				hits.push({ start: m.index, end: m.index + m[0].length, note: NotesAndComments.redFlag(inner, run, "cs"),
					at: /[\p{L}\p{N}]/u.test(after) ? stop : null });
				continue;
			}
			if (/[[\]]/.test(inner)) continue;
			if (inner.split(" ").filter((w) => /[\p{L}\p{N}]/u.test(w)).length < minW) continue;
			if (!norm.HasInstructionCue(inner)) continue;
			hits.push({ start: m.index, end: m.index + m[0].length, note: NotesAndComments.redFlag(inner, run, "cs") });
		}
		if (!hits.length) return woven.length ? { text: s, notes: [], links: woven } : null;
		// a space on each side: a web address typed right before the run must end before the token (the link weave)
		const edits = [];
		hits.forEach((h, i) => {
			const tok = ` ⟦CV2NOTE${i}⟧ `;
			if (h.at == null) edits.push({ from: h.start, to: h.end, put: tok });
			else { edits.push({ from: h.start, to: h.end, put: " " }); edits.push({ from: h.at, to: h.at, put: tok }); }
		});
		edits.sort((a, b) => a.from - b.from || a.to - b.to);
		let text = "", at = 0;
		for (const e of edits) { text += s.slice(at, e.from) + e.put; at = Math.max(at, e.to); }
		text += s.slice(at);
		return { text, notes: hits.map((h) => h.note), links: woven };
	};
}

// Node export hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { TablesAndGrids };
