/**
 * MediaListParser.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Finds the media table in an extracted docx (standalone Media List file or
 * embedded in a combined WT+media-list doc), interprets its columns, drops
 * the non-item rows, and returns clean media item objects for AcksBuilder.
 *
 * WHY SEPARATE FILE:
 * One concern: "media table → items". It knows nothing about ack formats
 * (AcksBuilder's job) and nothing about XML (DocxExtractor's job).
 *
 * DATA THIS FILE READS:
 * Input_Doc_Rules.json media_table — column header aliases, the example-row
 * and reminder-row discard signatures, the rels-over-visible-text rule.
 * New column heading spotted in the wild = one alias added there.
 *
 * THE ONE RULE THAT BURNS PEOPLE:
 * Writer-pasted URLs live in word/_rels/document.xml.rels, NOT the visible
 * cell text (which Word truncates). DocxExtractor already resolved rels
 * into each table block's links — we ALWAYS prefer a rel target whose
 * visible text appears in the row over the bare cell text.
 * ===========================================================================
 */

class MediaListParser {

	/**
	 * Strips the red-run markers from a cell's text.
	 *
	 * WHY: in COMBINED WT+media-list templates the media table's header row
	 * (and often the cell values) are red-wrapped — writers type them in the
	 * template's red style — so the raw cell reads
	 * "🔴[RED TEXT] Item No. [/RED TEXT]🔴". Verified on ANZH205/AGH1008
	 * (12/06/26): without this strip, NO combined template's media table is
	 * ever recognised. Standalone Media List files have plain black headers.
	 */
	static #cleanCell(text) {
		return (text ?? "")
			.replace(/\u{1f534}/gu, "")
			.replace(/\[\/?RED TEXT\]/g, "")
			.replace(/\s+/g, " ")
			.trim();
	};

	/**
	 * Finds the media table among a document's blocks.
	 *
	 * HOW: a table qualifies when its first row matches at least
	 * min_header_matches of the column families (folded comparison).
	 *
	 * DATA SHAPE RETURNED:
	 * { block: tableBlock, columnMap: { item_no, wt_page, item_type,
	 *   description, source, url, ecr } }
	 * — columnMap maps each column family (Input_Doc_Rules.json
	 * media_table.columns) to the CELL INDEX it lives at in THIS table's
	 * rows; a family the header row doesn't contain is simply absent from
	 * columnMap (never a fabricated index).
	 *
	 * @param {Object[]} blocks - extracted blocks (any document)
	 * @returns {Object|null} { block, columnMap } or null when absent
	 */
	static FindMediaTable(blocks) {
		const rules = DataService.Data.InputDocRules.media_table;

		for (const block of blocks) {
			if (block.kind !== "table" || !block.rows.length) continue;
			const headerCells = block.rows[0].map((c) =>
				Utils.Fold(this.#cleanCell(c)).replace(/[.]/g, ""));

			// map column family → cell index, by alias lookup
			const columnMap = {};
			for (const [family, def] of Object.entries(rules.columns)) {
				const idx = headerCells.findIndex((cell) =>
					def.aliases.some((a) => cell === a.replace(/[.]/g, "")));
				if (idx >= 0) columnMap[family] = idx;
			}

			if (Object.keys(columnMap).length >= rules.min_header_matches) {
				return { block, columnMap };
			}
		}
		return null;
	};

	/**
	 * Parses the found media table into item objects.
	 *
	 * WHAT IT RETURNS (one per genuine row):
	 * {
	 *   itemNo: "3", wtPage: 13, itemType: "video",
	 *   description: "Being a school principal in the 80's vs today",
	 *   source: "Youtube",
	 *   url: "https://www.youtube.com/watch?v=…",   ← rel target preferred
	 *   ecr: "", rowIndex: 4
	 * }
	 *
	 * REAL SAMPLE ROW (OSAH401 Media List):
	 *   1 | 11 | video | Think Time: How does Cyberbullying… | Youtube | https://…
	 *
	 * @param {Object} found - FindMediaTable() result
	 * @returns {Object[]} items (discard rows removed)
	 */
	static ParseItems(found) {
		const rules = DataService.Data.InputDocRules.media_table;
		const { block, columnMap } = found;
		const items = [];

		// links from DocxExtractor, captured PER ROW (block.rowLinks) so a
		// row only ever sees its own hyperlinks. (An earlier pooled-links
		// version matched every iStock row to the first URL in the table —
		// the per-row capture removes the guesswork entirely.)
		const rowLinks = block.rowLinks ?? [];

		for (let r = 1; r < block.rows.length; r++) {   // r=0 is the header
			const cells = block.rows[r];

			// --- discard: merged/spanning reminder rows + reminder text ---
			if (cells.length <= 1) continue;
			const firstFolded = Utils.Fold(this.#cleanCell(cells[0]));
			if (firstFolded.startsWith("reminder")) continue;

			// --- discard: completely empty rows --------------------------
			if (cells.every((c) => !this.#cleanCell(c))) continue;

			const cell = (family) => (columnMap[family] !== undefined
				? this.#cleanCell(cells[columnMap[family]]) : "");

			// --- discard: the template's worked example row ---------------
			const itemNo = cell("item_no");
			const description = cell("description");
			const isExample = Utils.Fold(itemNo) === "example"
				|| rules.discard_rows.example_row.example_signatures.some(
					(sig) => Utils.Fold(description).includes(sig));
			if (isExample) continue;

			// --- URL: ALWAYS prefer this row's rel target over the visible
			// cell text (which Word truncates). One link in the row = it is
			// the URL; several = pick the one anchored in the URL column
			// (its visible text appears in the url cell), else the first.
			let url = cell("url");
			const ownLinks = rowLinks[r] ?? [];
			if (ownLinks.length === 1) {
				url = ownLinks[0].target;
			} else if (ownLinks.length > 1) {
				const inUrlCell = ownLinks.find((l) => l.text && url.includes(l.text.slice(0, 20)));
				url = (inUrlCell ?? ownLinks[0]).target;
			}

			items.push({
				itemNo,
				wtPage: parseInt(cell("wt_page"), 10) || null,
				itemType: cell("item_type"),
				description,
				source: cell("source"),
				url,
				ecr: cell("ecr"),
				rowIndex: r,
			});
		}
		return items;
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { MediaListParser };
