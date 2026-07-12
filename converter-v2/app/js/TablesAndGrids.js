/**
 * TablesAndGrids.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * The TABLE and GRID rendering primitives, split out of ContentConverter
 * (the main content-emitting class) into their own file to keep that file's
 * size manageable. Six statics:
 *
 *   - contentTable(block, run, insidePlaceholder, norm)  THE table emitter — a
 *         writer table -> the kept <table> HTML (header/data rows, with
 *         structural cell-tag inline rendering), after first offering the
 *         layout-grid path below
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
		const grid = this.layoutTableGrid(rows, run, insidePlaceholder, norm);
		if (grid) return grid;

		const html = [t.open];
		rows.forEach((cells, r) => {
			const cellTpl = r === 0 ? t.header_cell : t.cell;
			html.push(t.row_open
				+ cells.map((c) => {
					// CELL-TAG rendering: a structural [tag] inside a KEPT free-body table cell
					// is rendered INLINE (its marker stripped) instead of leaking literally into
					// the page. FREE-BODY ONLY (insidePlaceholder=false) — a table INSIDE an
					// un-built interactive-widget placeholder shows the raw WT [tag] data BY
					// DESIGN (a developer reference), so its markers must NOT be stripped there.
					// Returns null when the cell doesn't match this case, so the caller falls
					// through to the plain-text rendering below.
					const inline = insidePlaceholder ? null : this.renderCellInline(c, run, r === 0, norm);
					const content = inline !== null ? inline
						// red spans inside table cells: keep their text visible,
						// marked — they are usually interactive data labels
						: ListsAndRuns.inlineMarkup(c.replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, ""), [], !insidePlaceholder);   // only weave hover/definition markers into a FREE-BODY cell, never a placeholder dump
					return Utils.FillTemplate(cellTpl, { content });
				}).join("")
				+ t.row_close);
		});
		html.push(t.close);
		return html.join("\n");
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
	static renderCellInline(cell, run, isHeader, norm) {
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
				let inner = ListsAndRuns.inlineMarkup(String(s.text).trim());
				const wantBold = s.bold && !isHeader && (cfg.bold_in_data_cells_only !== false);
				if (wantBold && !/^<(?:b|strong)>[\s\S]*<\/(?:b|strong)>$/.test(inner)) inner = `<b>${inner}</b>`;
				return inner;
			}).join(cfg.label_join ?? " ");
		}
		// image-only cell → render the in-cell image(s)
		const out = images.map((tx) => this.cellImage(tx, run).join("")).filter(Boolean);
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
	static layoutTableGrid(rows, run, insidePlaceholder, norm) {
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
		for (const r of rows) {
			const cells = (r || []).filter((c) => String(c ?? "").trim() !== "");
			if (!cells.length) continue;
			const colClass = cfg.col_class_by_count?.[String(cells.length)] || cfg.col_class_default;
			const cols = cells.map((c) => {
				const inner = this.renderCellParts(c, run, norm).filter(Boolean);
				return `${cfg.col_open.replace("{colClass}", colClass)}\n${inner.join("\n")}\n${cfg.col_close}`;
			});
			out.push(`${cfg.row_open}\n${cols.join("\n")}\n${cfg.row_close}`);
		}
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
	static cellParts(cell) {
		return String(cell ?? "")
			.replace(/\u{1f534}\[RED TEXT\]/gu, "").replace(/\[\/RED TEXT\]\u{1f534}/gu, "")
			.split(/\s+\/\s+/).map((p) => p.trim()).filter(Boolean);
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
	static renderCellParts(cell, run, norm) {
		const tpl = DataService.Data.EmitTemplates;
		const skipRe = new RegExp(tpl.body_region.layout_table_grid.skip_part_pattern ?? "^[=\\s]*$");
		const out = [];
		let buf = [];
		const flush = () => { if (buf.length) { out.push(...ListsAndRuns.renderBlackText(buf.join("\n"), run)); buf = []; } };
		for (const part of this.cellParts(cell)) {
			const m = part.match(/^\[([^\]]+)\]\s*([\s\S]*)$/);
			let canon = null, rest = part;
			if (m) {
				try { canon = norm.Parse(`[${m[1]}]`)?.primary?.tag ?? null; } catch { canon = null; }
				rest = m[2];
			}
			if (canon && /^(?:h[1-5]|heading|activity heading)$/.test(canon)) {
				flush();
				const digit = /^h\d$/.test(canon) ? parseInt(canon[1], 10) : 2;
				const shifted = Math.min(Math.max(digit + tpl.elements.heading.logical_to_element.body_shift, 2), 5);
				const text = (rest.trim() || norm.RenderText(part) || "").replace(/\*/g, "").trim();
				if (text) out.push(`<h${shifted}>${ListsAndRuns.inlineMarkup(text)}</h${shifted}>`);
			} else if (canon === "image") {
				flush();
				out.push(...this.cellImage(rest, run));
			} else {
				const content = canon ? rest : part;
				if (content.trim() && !skipRe.test(content.trim())) buf.push(content);
			}
		}
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
	static cellImage(text, run) {
		const tpl = DataService.Data.EmitTemplates.image;
		const url = text.match(/https?:\/\/[^\s\]\)"<>]+/)?.[0] ?? "";
		const istockId = url.match(/gm-?(\d{6,10})/)?.[1] ?? null;
		const filename = istockId
			? Utils.FillTemplate(tpl.filename_rules.istock, { id: istockId })
			: `${Utils.Slugify(text.replace(/https?:\/\/\S+/g, "").replace(/^\s*istock[.:]?/i, "").trim() || "image") || "image"}.jpg`;
		const label = istockId ? `iStock-${istockId}` : "image";
		if (run.imageMode === "P") {
			return [Utils.FillTemplate(tpl.mode_P.visible, { label }), Utils.FillTemplate(tpl.mode_P.comment, { filename })];
		}
		return [Utils.FillTemplate(tpl.mode_D.visible, { filename })];
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { TablesAndGrids };
