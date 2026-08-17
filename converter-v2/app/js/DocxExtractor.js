/**
 * DocxExtractor.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Turns an unzipped Writers Template .docx into the converter's intermediate
 * form: an ordered list of content BLOCKS (paragraphs + tables), each
 * carrying (a) the marker-text string the tag pipeline reads, and (b)
 * metadata the emitters need (hyperlink targets, WT page number, list info).
 *
 * THE KEY IDEA (why this file makes everything else safe):
 * The raw docx still carries the writers' red colouring as w:color runs
 * (verified: ff0000 / ee0000 in the real corpus templates). We re-wrap red
 * runs in the exact 🔴[RED TEXT] … [/RED TEXT]🔴 markers, and tables in the
 * exact ┌─── TABLE ─── │ … ║ … └─── END TABLE ─── lines, that the validated
 * historical corpus uses. Everything downstream of this file therefore runs
 * the SAME pipeline that passed the 9,557-variation regression and the
 * 121-type e2e validation — fresh uploads and the proven corpus are
 * indistinguishable.
 *
 * WHY A HAND-ROLLED XML WALK (and not DOMParser):
 * OOXML from Word is machine-generated and extremely regular; a ~40-line
 * token walker covers everything we read (w:p, w:r, w:t, w:color, w:b,
 * w:i, w:hyperlink, w:tbl/tr/tc, w:br, w:lastRenderedPageBreak, w:numPr).
 * It also runs identically in the browser and in the sandbox test harness,
 * so the ingest layer is regression-testable end-to-end.
 *
 * DATA THIS FILE READS:
 * Input_Doc_Rules.json — red hex values, marker strings, table markers,
 * formatting markers, MTK signature, content-start rule. NO input-shape
 * knowledge is hard-coded here.
 *
 * WHEN TO WORK HERE:
 * Only if Word itself changes how it stores something. New red shade,
 * new boilerplate, new media-table heading → edit Input_Doc_Rules.json.
 * ===========================================================================
 */

class DocxExtractor {

	/**
	 * Extracts a complete docx into blocks + metadata.
	 *
	 * WHAT IT RETURNS:
	 * {
	 *   blocks:   [ paraBlock | tableBlock … ]   (document order)
	 *   rels:     Map(rId → external URL)
	 *   mtkFlag:  true when the MTK/TRR bilingual signature was seen
	 *   hasContentStart: true when a [TITLE BAR] red tag exists
	 * }
	 *
	 * BLOCK SHAPES (the contract every later stage relies on):
	 * paraBlock = {
	 *   kind: "para",
	 *   text:  "🔴[RED TEXT] [H2] [/RED TEXT]🔴**Learning Intentions**",
	 *   links: [ { text, target } ],   // resolved hyperlinks in this para
	 *   wtPage: 3,                     // Writers Template page number
	 *   list: "bullet" | "number" | null
	 * }
	 * tableBlock = {
	 *   kind: "table",
	 *   rows: [ [ cellText, cellText ] ],   // marker-text per cell
	 *   links: [ { text, target } ],        // hyperlinks anywhere in table
	 *   wtPage: 5,
	 *   text: "┌─── TABLE ───\n│ a ║ b\n└─── END TABLE ───"
	 * }
	 *
	 * @param {ZipReader} zip - opened docx archive
	 * @returns {Promise<Object>} extraction result as above
	 */
	static async Extract(zip) {
		const rules = DataService.Data.InputDocRules;

		// --- the three parts we read ------------------------------------
		const documentXml = await zip.ReadText("word/document.xml");
		// hyperlink targets live in the rels part, NOT the visible text —
		// the single most important extraction rule for the media list
		const relsXml = zip.Has("word/_rels/document.xml.rels")
			? await zip.ReadText("word/_rels/document.xml.rels") : "";
		// numbering.xml tells bullet vs numbered lists (optional part)
		const numberingXml = zip.Has("word/numbering.xml")
			? await zip.ReadText("word/numbering.xml") : "";
		// comments.xml carries native Word editor comments left by reviewers.
		// This is an OPTIONAL part of the .docx — most, but not all, Writers
		// Templates have it. Each comment is keyed by id → {author, text}; it
		// gets anchored to a specific content block later on, in
		// #parseDocument, by matching against the document.xml
		// commentRangeStart markers. We capture EVERY comment here regardless
		// of author — deciding WHICH authors' comments are worth showing (and
		// how to render them) happens further downstream, in ContentConverter.
		const commentsXml = zip.Has("word/comments.xml")
			? await zip.ReadText("word/comments.xml") : "";

		const rels = this.#parseRels(relsXml);
		const numFormats = this.#parseNumbering(numberingXml);
		const comments = this.#parseComments(commentsXml);
		const blocks = this.#parseDocument(documentXml, rels, numFormats, rules, comments);

		// --- document-level signals ---------------------------------------
		// MTK/TRR bilingual templates follow a separate pathway (data rule).
		// IMPORTANT: this is only the RAW signature signal — the heading
		// "MTK WRITERS TEMPLATE" also appears in standard templates'
		// front-matter (verified on OSAH401), so the unsupported decision is
		// made later by ConversionRun: signature AND module-code prefix
		// (Input_Doc_Rules.unsupported_pathways.also_requires_code_prefix).
		const signatures = rules.unsupported_pathways.map((u) => u.signature);
		let mtkFlag = false;
		for (const b of blocks.slice(0, 60)) {  // signature sits in the title block
			if (b.kind !== "para") continue;
			const folded = Utils.Fold(b.text);
			if (signatures.some((sig) => folded.includes(sig))) { mtkFlag = true; break; }
		}

		// literal check only here (no normaliser at extract time) — the
		// full detection chain runs in TrimFrontMatter, which gets one
		const hasContentStart = blocks.some((b) => this.IsContentStart(b, null, rules));

		// the module-specific front-matter fields (Subject/Course/Module
		// Code/Key Contact/Date submitted) — Course backs up an English
		// title later (front_matter_metadata data rule)
		const metadata = this.#extractMetadata(blocks, rules);

		return { blocks, rels, mtkFlag, hasContentStart, metadata };
	};

	/**
	 * Is this block the content-start boundary?
	 * Detection chain per Input_Doc_Rules.content_start:
	 *  (1) LITERAL fragment ("title bar") — the standard template opener;
	 *  (2) CANONICAL resolution — Fundamentals templates open with
	 *      [Fundamental content]/[Fundamental 1 code] (canonical "lesson
	 *      content") or a bare [Title] instead (verified: ARFUN01, MXFUN03,
	 *      EXPFUN04 — one PageForge run even printed "[TITLE BAR] marker
	 *      not found"). Needs the normaliser, hence the parameter.
	 *
	 * @param {Object} block - a paraBlock
	 * @param {TagNormaliser|null} normaliser - for the canonical chain
	 * @param {Object} rules - Input_Doc_Rules.json (defaults to loaded)
	 * @returns {boolean}
	 */
	static IsContentStart(block, normaliser = null, rules = DataService.Data.InputDocRules) {
		if (block.kind !== "para") return false;
		const folded = Utils.Fold(block.text);

		// (1) the literal fragment — fast path, no normaliser needed
		if (rules.content_start.content_start_fragments.some((frag) =>
			new RegExp(`\\[\\s*${Utils.RegexEscape(frag)}\\s*\\]`).test(folded))) {
			return true;
		}

		// (2) canonical resolution of the block's RED spans only — black
		// text in front-matter tables ("Resource title" …) must never match
		if (!normaliser) return false;
		const canonicals = rules.content_start.content_start_canonicals ?? [];
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		for (const m of block.text.matchAll(RED)) {
			const primary = normaliser.Parse(m[1]).primary;
			if (primary && canonicals.includes(primary.tag)) return true;
		}
		return false;
	};

	/**
	 * Captures the FILLED module-specific front-matter fields from the gray
	 * info table ('Label: value' paragraphs), per front_matter_metadata.
	 * A bare 'Label:' (blank template row) is skipped.
	 *
	 * @param {Object[]} blocks
	 * @param {Object} rules - Input_Doc_Rules.json
	 * @returns {Object} { subject, course, moduleCode, keyContact, dateSubmitted } (only filled keys)
	 */
	static #extractMetadata(blocks, rules) {
		const cfg = rules.front_matter_metadata;
		if (!cfg) return {};
		const out = {};
		// labels checked longest-first so "key contact (name, email…)" wins
		// over a bare "key contact"
		const fieldByLabel = [];
		for (const [field, def] of Object.entries(cfg.fields)) {
			for (const label of def.labels) fieldByLabel.push([Utils.Fold(label), field]);
		}
		fieldByLabel.sort((a, b) => b[0].length - a[0].length);

		for (const b of blocks) {
			if (b.kind !== "para") continue;
			// the raw paragraph text without red markers / markdown
			const text = b.text.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "")
				.replace(/\*\*/g, "").trim();
			const colon = text.indexOf(":");
			if (colon < 0) continue;
			const labelFolded = Utils.Fold(text.slice(0, colon));
			const value = text.slice(colon + 1).trim();
			if (!value) continue;   // blank template row
			const hit = fieldByLabel.find(([l]) => labelFolded === l);
			if (hit && !out[hit[1]]) out[hit[1]] = value;
		}

		// TABLE-ROW metadata (ROUND 212 — the PNR family's MTK "Te Aka Taumatua"
		// template): its front matter carries the module info as a TABLE
		// ("Module Name | Ngā tau: 1 | Numbers: 1"), not "Label: value"
		// paragraphs, so the paragraph walk above never captured it. Only the
		// fields listed in table_row_fields are read from table rows —
		// deliberately NOT course/moduleCode, so the "Course is the title
		// backup" path can never start firing on modules where it never fired
		// before. The captured moduleName is the bilingual title source when
		// the module has no [TITLE BAR] payload (see PageAssembler).
		// Env toggle: REODROPMENU_OFF.
		const tableFields = new Set(cfg.table_row_fields ?? []);
		if (tableFields.size
			&& !(typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF)) {
			const clean = (s) => String(s ?? "")
				.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "")
				.replace(/\*\*/g, "").trim();
			for (const b of blocks) {
				if (b.kind !== "table") continue;
				for (const row of (b.rows ?? [])) {
					if (!Array.isArray(row) || row.length < 2) continue;
					const labelFolded = Utils.Fold(clean(row[0]));
					const hit = fieldByLabel.find(([l, f]) => labelFolded === l && tableFields.has(f));
					if (!hit) continue;
					const value = clean(row[1]);
					if (value && !out[hit[1]]) out[hit[1]] = value;
				}
			}
		}
		return out;
	};

	/**
	 * Is this document a Writers Template at all? True when any block is a
	 * recognised content start, OR the fallback applies (a red span
	 * resolving to a structural directive — bare-[H1] openers).
	 * Used by the upload classifier; TrimFrontMatter then finds the spot.
	 *
	 * @param {Object[]} blocks
	 * @param {TagNormaliser} normaliser
	 * @returns {boolean}
	 */
	static LooksLikeWritersTemplate(blocks, normaliser) {
		if (blocks.some((b) => this.IsContentStart(b, normaliser))) return true;
		const fallback = DataService.Data.InputDocRules.content_start
			.content_start_fallback_directives ?? [];
		if (!normaliser || !fallback.length) return false;
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		return blocks.some((b) => b.kind === "para"
			&& [...b.text.matchAll(RED)].some((m) =>
				fallback.includes(normaliser.Parse(m[1]).primary?.directive)));
	};

	/**
	 * Drops everything before the first content-start block.
	 *
	 * WHY: everything before the opener is generic template front-matter
	 * (submission checklist, LOT tags, Section A/B…) — out of scope by rule:
	 * not interpreted, not converted, not flagged.
	 *
	 * FALLBACK (chain step 3): when no opener exists at all, ALL blocks are
	 * returned and the caller must surface a loud warning — PageForge's own
	 * behaviour for these rare templates.
	 *
	 * @param {Object[]} blocks - all extracted blocks
	 * @param {TagNormaliser|null} normaliser - for the canonical chain
	 * @param {ConversionRun|null} run - surfacing
	 * @returns {Object[]} blocks from the boundary onward
	 */
	static TrimFrontMatter(blocks, normaliser = null, run = null) {
		let result = null;
		let start = blocks.findIndex((b) => this.IsContentStart(b, normaliser));

		// DROP-DOWN-MENU OPENER RESCUE (ROUND 212 — the MTK "Te Aka Taumatua"
		// bilingual template, the PNR101/102/104 family). That template has NO
		// paragraph-level [TITLE BAR] at all (its [TITLE BAR] tags live inside
		// TABLE cells, which the standard chain never sees), so the first
		// standard content-start found is the [LESSON 1 CONTENT] marker — and
		// everything before it (the "[Content for DROP DOWN MENU]" module-menu
		// section + the [MODULE CONTENT: PAGE 1] introduction) was silently
		// trimmed away as front matter: the module shipped an EMPTY overview.
		// RESCUE: when the standard start is a LESSON-CONTENT start (NOT a
		// title-bar one) and a "[Content for DROP DOWN MENU]" paragraph exists
		// EARLIER, the document opens there instead. Scoping matters: a module
		// whose standard start IS a [TITLE BAR] paragraph (the TRR203/TRR301
		// shape — same marker family, but their title bar is already visible to
		// the standard chain) is left completely unchanged.
		// Data: content_start.content_start_fragments_dropdown.
		// Env toggle: REODROPMENU_OFF.
		if (start >= 0
			&& !(typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF)) {
			const rules = DataService.Data.InputDocRules;
			const ddFrags = rules.content_start.content_start_fragments_dropdown ?? [];
			if (ddFrags.length) {
				const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
				// is the found standard start a TITLE-BAR start? (literal fragment
				// or a red span resolving to the "title bar" canonical)
				const sb = blocks[start];
				const sbFolded = Utils.Fold(sb.text);
				let titleBarStart = /\[\s*title bar\s*\]/.test(sbFolded);
				if (!titleBarStart && normaliser) {
					titleBarStart = [...sb.text.matchAll(RED)].some((m) =>
						normaliser.Parse(m[1]).primary?.tag === "title bar");
				}
				if (!titleBarStart) {
					const dd = blocks.findIndex((b) => b.kind === "para"
						&& ddFrags.some((frag) =>
							new RegExp(`\\[\\s*${Utils.RegexEscape(frag)}\\s*\\]`).test(Utils.Fold(b.text))));
					if (dd >= 0 && dd < start) {
						run?.AddNote("info", "DocxExtractor",
							"Content opened at the [Content for DROP DOWN MENU] marker — the MTK drop-down-menu bilingual template (its overview lives before the first [LESSON N CONTENT]).");
						start = dd;
					}
				}
			}
		}
		if (start >= 0) result = blocks.slice(start);

		// last chance (data rule content_start_fallback_directives): the
		// first red span resolving to a structural directive opens the
		// document — some templates begin at a bare [H1] (EXPFUN06).
		if (result === null) {
			const rules = DataService.Data.InputDocRules;
			const fallback = rules.content_start.content_start_fallback_directives ?? [];
			if (normaliser && fallback.length) {
				const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
				const idx = blocks.findIndex((b) => b.kind === "para"
					&& [...b.text.matchAll(RED)].some((m) =>
						fallback.includes(normaliser.Parse(m[1]).primary?.directive)));
				if (idx >= 0) {
					run?.AddNote("warn", "DocxExtractor",
						"No [TITLE BAR]/[Fundamental content] opener — content started at the first structural tag instead; check the first page for stray front-matter.");
					result = blocks.slice(idx);
				}
			}
		}

		if (result === null) {
			run?.AddNote("warn", "DocxExtractor",
				"No content-start tag found at all — converting ALL blocks; front-matter may leak into the output. Review the source template.");
			result = blocks;
		}

		// ROUND 306 — a PAGE-LAYOUT table that traps a speech bubble beside an
		// [Activity] dissolves into ordinary stacked blocks (the human's own
		// answer). Runs BEFORE the bracket repair below, so a dissolved cell's
		// "Activity]" typo is repaired like any other paragraph's.
		result = this.DissolveBubbleLayoutTables(result, normaliser, run);

		// Some writers accidentally drop the opening square bracket off a tag
		// — e.g. typing "H2] Know:" instead of "[H2] Know:". Repair that here,
		// once, before any other part of the pipeline reads these blocks.
		return this.RepairContentTags(result, normaliser, run);
	};

	/**
	 * ROUND 306 — DISSOLVES A PAGE-LAYOUT TABLE THAT TRAPS A SPEECH BUBBLE.
	 *
	 * WHAT PROBLEM THIS SOLVES:
	 * One writer family (measured: EXACTLY TEDC402, 12 tables corpus-wide) lays a
	 * whole lesson activity out inside a two-column table — the [Activity] with its
	 * heading/instructions in one cell, the character picture + [speech bubble] in
	 * the other. The bubble's collector took the whole table, met the [Activity]
	 * marker, and correctly concluded "not a bubble layout" — so BOTH cells shipped
	 * inside a developer hand-off box. The human developer's own answer is to THROW
	 * THE TABLE AWAY: the finished page ships the two cells as two ordinary stacked
	 * blocks in reading order — a normal activity box, then a normal bubble row
	 * (TEDC402-1.0, byte-verified in the round-306 brief).
	 *
	 * HOW: a qualifying table's cells become ordinary paragraph blocks, one block
	 * per cell in reading order, with the in-cell line-break marker restored to a
	 * plain newline (the round-227 soft-break form every downstream reader already
	 * handles). Every existing mechanism then does the rest: the [Activity] opener
	 * opens its box, and the [Image]+[speech bubble] cell is EXACTLY the one-
	 * paragraph avatar dialect round 246's no-table bubble builder already builds
	 * on this very module's free-body pages.
	 *
	 * THE FENCE IS MEASURED, NOT GUESSED (outputs/_measure_r306_layouttables.cjs,
	 * all 454 modules): a table dissolves ONLY when its red spans resolve to BOTH
	 * an ACTIVITY-family CONTAINER_OPEN marker AND a speech-bubble INTERACTIVE
	 * invocation. "Activity marker alone" would have fired on ~120 tables across
	 * ~20 modules — the bilingual TRR embedded-activity tables, the fundamentals
	 * accordion/slide tables, CEDO501's round-305 quiz tables — every one of which
	 * must STAY a table. Both-markers fires on 12 tables, ALL TEDC402. A table
	 * carrying any PAGE_BOUNDARY / SECTION_MARKER span never dissolves (exposing an
	 * in-cell [End page] to the page splitter would churn pagination — the ENGS202
	 * page-opener class stays exactly as it is).
	 *
	 * ROUND 313 adds the SECOND qualifying shape, and it needs no proxy at all: a
	 * ONE-ROW ONE-CELL table has no second cell for data to sit in, so an activity
	 * marker inside one is a box the writer drew, not widget data. Measured over all
	 * 454 WTs that shape is 7 tables / 5 modules; the 3 reo ones are excluded (the
	 * r145/r167 class — reoMode routes tables through the bilingual handlers) leaving
	 * ENGI400 x2, HPFUN903 and TEDC402, every one gold-verified to ship no table.
	 * The other generalisation — "any INTERACTIVE invocation, not just a bubble" —
	 * was measured and DECLINED: it fires on 35 tables and 23 of those are genuine
	 * DATA tables (CEDO501's r305 quiz grids, flipCard front/back tables, drag-and-drop
	 * option grids, the TRR English|Te Reo pairs). The tag is not the discriminator.
	 *
	 * Data: Input_Doc_Rules.tables.bubble_layout_dissolve (+ .single_cell).
	 * Env: SBLAYOUT_OFF (whole rule) / SBSINGLECELL_OFF (the r313 arm alone).
	 *
	 * @param {Object[]} blocks - content blocks (tables carry .rows / .rowLinks)
	 * @param {TagNormaliser|null} normaliser - resolves the cell spans (required)
	 * @param {ConversionRun|null} run - note surfacing
	 * @returns {Object[]} a new block list with qualifying tables dissolved
	 */
	static DissolveBubbleLayoutTables(blocks, normaliser, run = null) {
		const cfg = DataService?.Data?.InputDocRules?.tables?.bubble_layout_dissolve;
		if (!normaliser || !cfg || cfg.enabled === false) return blocks;
		if (typeof process !== "undefined" && process.env && process.env.SBLAYOUT_OFF) return blocks;
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		const needTags = new Set(cfg.interactive_tags ?? ["speech bubble"]);
		const brk = DataService.Data.InputDocRules?.table_markers?.in_cell_line_break ?? " / ";
		/* ROUND 313 — the single-cell arm, independently reversible. */
		const scCfg = cfg.single_cell;
		const scOn = !!scCfg && scCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.SBSINGLECELL_OFF)
			&& !(scCfg.exclude_code_prefixes ?? []).some((p) => String(run?.moduleCode ?? "").startsWith(p));
		const out = [];
		for (const b of blocks) {
			if (!b || b.kind !== "table" || !Array.isArray(b.rows)) { out.push(b); continue; }
			let hasAct = false, hasBubble = false, hasBoundary = false, hasPlainAct = false;
			for (const m of String(b.text ?? "").matchAll(RED)) {
				let p; try { p = normaliser.Parse(m[1]); } catch { continue; }
				const pr = p && p.primary;
				if (!pr) continue;
				if (pr.tag === "activity" && pr.directive === "CONTAINER_OPEN") {
					hasAct = true;
					/* Is it an EXPLICIT activity opener the writer typed ("[Activity 2A]"),
					 * or a widget request that merely ALIASES to one ("[interactive tool]
					 * quiz — tick box yes or no DEV: answers will vary")?  Only the first
					 * qualifies the single-cell arm — see scOpener below. */
					if (/^\s*\[?\s*activity\b/i.test(String(m[1] ?? ""))) hasPlainAct = true;
				}
				else if (pr.directive === "INTERACTIVE" && needTags.has(pr.tag)) hasBubble = true;
				else if (pr.directive === "PAGE_BOUNDARY" || pr.directive === "SECTION_MARKER") hasBoundary = true;
			}
			/* THE SINGLE-CELL ARM. `scOpener` is the fence the round's own word-loss
			 * check forced: HPFUN903's one-cell table has no explicit opener at all —
			 * what makes it "an activity" is the WIDGET REQUEST "[interactive tool]
			 * quiz — tick box yes or no DEV: answers will vary", which aliases to the
			 * activity tag. Dissolving that hands a widget spec to the body path, and
			 * measured live it (a) dropped the writer's "DEV:" instruction from the
			 * page — a §6 violation — and (b) promoted the first bullet to the box's
			 * <h3> (the gold ships ZERO bullet headings in 2,385 files). Requiring a
			 * bracket the writer opened with the word "activity" separates that case
			 * from ENGI400's "[Activity 2A]" and TEDC402's "Activity] 1D" cleanly and
			 * for a structural reason, not a per-module one. */
			const scOpener = scCfg?.require_explicit_activity_opener === false || hasPlainAct;
			const singleCell = scOn && scOpener
				&& b.rows.length === 1 && (b.rows[0]?.length ?? 0) === 1;
			if (!hasAct || hasBoundary || !(hasBubble || singleCell)) { out.push(b); continue; }
			let made = 0;
			for (let r = 0; r < b.rows.length; r++) {
				for (const cell of (b.rows[r] ?? [])) {
					const text = String(cell ?? "").split(brk).join("\n").trim();
					if (!text) continue;
					out.push({
						kind: "para", text,
						links: (b.rowLinks?.[r] ?? b.links ?? []).slice(),
						wtPage: b.wtPage, list: "", listLevel: 0,
					});
					made++;
				}
			}
			run?.AddNote("info", "DocxExtractor", hasBubble
				? `Page-layout table dissolved into ${made} stacked blocks (an [Activity] and a [speech bubble] shared one table — the finished page stacks them; round 306).`
				: `Single-cell page-layout table dissolved into ${made} stacked blocks (a one-cell table holding an [Activity] is a box the writer drew, not widget data; round 313).`);
		}
		return out;
	};

	/**
	 * REPAIRS A TAG THAT IS MISSING ITS OPENING SQUARE BRACKET.
	 *
	 * WHAT PROBLEM THIS SOLVES:
	 * A writer will sometimes forget to colour the opening "[" of a tag red,
	 * so what should have been a red span reading "[H2] Know:" instead
	 * arrives as "H2] Know:" (missing the "["). TagNormaliser.Parse already
	 * tolerates this for CLASSIFICATION purposes — it can still work out
	 * that "H2] Know:" MEANS the [H2] tag — but roughly ten OTHER places in
	 * the pipeline (RenderText, the overview-menu splitter, the black-tag
	 * stripper, InteractiveScanner…) read the raw bracket characters
	 * directly and don't know that trick. They see a stray "H2]" with no
	 * matching "[" and leak it into the page as literal text (one real
	 * example: a "Know" heading disappeared entirely and the literal text
	 * "<h5>H2]</h5>" showed up in the HTML instead).
	 *
	 * HOW IT WORKS:
	 * For every red ("content") span, look at the text right before its
	 * first "]". If that text is a single word/phrase that resolves to a
	 * KNOWN tag by a clean, WHOLE match — not a tag word that just happens
	 * to appear buried inside an ordinary sentence, see clean_hows below —
	 * insert the missing "[" at the start of that word. Every downstream
	 * reader then sees a normal, complete "[H2]" tag. The original
	 * letter-casing is preserved, because RenderText needs it to show
	 * headings/titles with correct capitalisation.
	 *
	 * WHAT THIS DOES NOT TOUCH:
	 * A tag that is missing its CLOSING bracket instead (e.g. "[hover
	 * trigger: some text" with no "]" at the end) is deliberately left
	 * alone — TagNormaliser.Parse and RenderText already have their own
	 * tolerant handling for that shape, and fully fixing it needs more work
	 * that hasn't been done yet (tracked separately as a "split-bracket
	 * infoTrigger" follow-up).
	 *
	 * DATA DRIVEN: which match types count as "clean enough to repair"
	 * lives in Input_Doc_Rules.json under
	 * red_runs.repair_missing_bracket.clean_hows (e.g. "exact",
	 * "denumbered", "denumbered_head" — NOT "embedded", which means the tag
	 * word was found buried inside ordinary prose rather than leading the
	 * phrase).
	 *
	 * @param {Object[]} blocks - content blocks (block.text carries the red markers)
	 * @param {TagNormaliser|null} normaliser - resolves the token (required)
	 * @param {ConversionRun|null} run - surfacing hook (not used today; kept for future warnings)
	 * @returns {Object[]} the same array, with block.text repaired in place
	 */
	static RepairContentTags(blocks, normaliser, run = null) {
		const cfg = DataService?.Data?.InputDocRules?.red_runs?.repair_missing_bracket;
		if (!normaliser || !cfg || cfg.enabled === false) return blocks;
		if (typeof process !== "undefined" && process.env && process.env.BRACKETFIX_OFF) return blocks;
		const cleanHows = new Set(cfg.clean_hows ?? ["exact", "denumbered", "denumbered_head"]);
		const excludeTags = new Set(cfg.exclude_tags ?? []);
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		for (const b of blocks) {
			if (b.kind !== "para" || !b.text || b.text.indexOf("]") < 0) continue;
			b.text = b.text.replace(RED, (whole, inner) => {
				const fixed = this.#repairLeadingBracket(inner, normaliser, cleanHows, excludeTags);
				return fixed === null ? whole : "\u{1f534}[RED TEXT]" + fixed + "[/RED TEXT]\u{1f534}";
			});
		}
		return blocks;
	};

	/**
	 * Inserts a missing OPENING bracket into one red-span's inner text when the
	 * span opens with a lone "token]" whose token is WHOLLY a known tag. Returns
	 * the repaired inner string, or null when nothing should change (the guard).
	 */
	static #repairLeadingBracket(inner, normaliser, cleanHows, excludeTags) {
		const closeIdx = inner.indexOf("]");
		if (closeIdx < 0) return null;                        // no ] at all
		const openIdx = inner.indexOf("[");
		if (openIdx >= 0 && openIdx < closeIdx) return null;  // a "[" already opens before this "]" → well-formed pair
		const before = inner.slice(0, closeIdx);              // token region incl. leading whitespace
		const token = before.trim();
		if (!token) return null;                              // bare "]"
		let parsed;
		try { parsed = normaliser.Parse("[" + token + "]"); } catch { return null; }
		const prim = parsed && parsed.primary;
		// WHOLE-token match only (clean_hows) — a tag word embedded in prose is how="embedded" and skipped.
		if (!prim || !cleanHows.has(prim.how) || excludeTags.has(prim.tag)) return null;
		const lead = before.length - before.trimStart().length;
		return inner.slice(0, lead) + "[" + inner.slice(lead);
	};

	// =======================================================================
	// XML PARSING (private)
	// =======================================================================

	/**
	 * Reads word/_rels/document.xml.rels into rId → external target URL.
	 *
	 * DATA SHAPE (real sample from OSAH401 Media List.docx):
	 * <Relationship Id="rId8" Type=".../hyperlink"
	 *   Target="https://www.istockphoto.com/photo/fun-dog-…" TargetMode="External"/>
	 *
	 * @param {string} xml
	 * @returns {Map<string,string>}
	 */
	static #parseRels(xml) {
		const rels = new Map();
		// one regex per Relationship element; attribute order can vary, so
		// capture the whole tag then pick attributes out of it
		for (const m of xml.matchAll(/<Relationship\b[^>]*>/g)) {
			const tag = m[0];
			if (!/TargetMode="External"/.test(tag)) continue;
			const id = tag.match(/\bId="([^"]+)"/)?.[1];
			const target = tag.match(/\bTarget="([^"]+)"/)?.[1];
			if (id && target) rels.set(id, this.#decodeXml(target));
		}
		return rels;
	};

	/**
	 * Reads word/numbering.xml just deeply enough to answer one question
	 * per numId: bullet list or numbered list?
	 *
	 * HOW: numId → abstractNumId → the ilvl-0 numFmt ("bullet"/"decimal"/…).
	 *
	 * @param {string} xml
	 * @returns {Map<string,string>} numId → "bullet" | "number"
	 */
	static #parseNumbering(xml) {
		const formats = new Map();
		if (!xml) return formats;

		// abstractNumId → first numFmt val
		const abstractFmt = new Map();
		for (const m of xml.matchAll(/<w:abstractNum w:abstractNumId="(\d+)"[\s\S]*?(?=<w:abstractNum |<\/w:numbering>)/g)) {
			const fmt = m[0].match(/<w:numFmt w:val="(\w+)"/)?.[1];
			abstractFmt.set(m[1], fmt === "bullet" ? "bullet" : "number");
		}
		// numId → abstractNumId
		for (const m of xml.matchAll(/<w:num w:numId="(\d+)"[^>]*>\s*<w:abstractNumId w:val="(\d+)"/g)) {
			formats.set(m[1], abstractFmt.get(m[2]) ?? "bullet");
		}
		return formats;
	};

	/**
	 * Parses word/comments.xml into id → { author, text }.
	 *
	 * Word stores each comment as <w:comment w:id="N" w:author="…" w:date="…"
	 * w:initials="…"> … <w:p><w:r><w:t>text</w:t></w:r></w:p> … </w:comment>.
	 * Comments never nest, so the close tag is unambiguous. We keep the author
	 * (the Office display name — the same name later checked against the
	 * author whitelist) and the joined run text; the
	 * anchor (WHICH content the comment is attached to) comes from the
	 * commentRangeStart markers in document.xml, matched by id in #parseDocument.
	 *
	 * @param {string} xml - word/comments.xml content ("" when the part is absent)
	 * @returns {Map<string,{author:string,text:string}>}
	 */
	static #parseComments(xml) {
		const map = new Map();
		if (!xml) return map;
		const re = /<w:comment\b([^>]*)>([\s\S]*?)<\/w:comment>/g;
		for (const m of xml.matchAll(re)) {
			const id = m[1].match(/\bw:id="([^"]*)"/)?.[1];
			if (id === undefined) continue;
			const author = this.#decodeXml(m[1].match(/\bw:author="([^"]*)"/)?.[1] ?? "");
			const text = [...m[2].matchAll(/<w:t\b[^>]*>([\s\S]*?)<\/w:t>/g)]
				.map((t) => this.#decodeXml(t[1])).join("");
			map.set(id, { author, text: text.replace(/\s+/g, " ").trim() });
		}
		return map;
	};

	/**
	 * The main walk: document.xml → ordered blocks.
	 *
	 * HOW IT WORKS:
	 * Word nests tables inside w:tbl and paragraphs inside w:p. We split the
	 * body into top-level chunks by scanning for w:p / w:tbl at depth 0 of
	 * the body, then parse each chunk. (Nested tables inside cells are rare
	 * in writers templates; a nested table's text simply joins its cell.)
	 *
	 * @param {string} xml - word/document.xml content
	 * @param {Map} rels - rId → URL
	 * @param {Map} numFormats - numId → bullet|number
	 * @param {Object} rules - Input_Doc_Rules.json
	 * @returns {Object[]} blocks
	 */
	static #parseDocument(xml, rels, numFormats, rules, comments = new Map()) {
		const blocks = [];
		// COMMENT ANCHORING: a <w:commentRangeStart> marker inside a chunk of
		// XML tells us which block a Word comment belongs to; we surface that
		// note JUST BEFORE the block it's anchored to. A comment anchored
		// inside an EMPTY paragraph (e.g. a comment left on an embedded image
		// with no text of its own) would otherwise be silently lost once that
		// empty block gets dropped, so instead we CARRY such comments forward
		// and attach them to the next block that actually survives — the
		// nearest real element after the anchor point.
		let pendingComments = [];
		const findComments = (chunkXml, isTable = false) => {
			const found = [];
			if (!comments.size) return found;
			const seen = new Set();
			for (const cm of chunkXml.matchAll(/<w:commentRangeStart\b[^>]*\bw:id="([^"]*)"/g)) {
				const id = cm[1];
				if (seen.has(id)) continue;
				seen.add(id);
				const c = comments.get(id);
				if (!c) continue;
				// When a comment is anchored inside a TABLE row (this happens
				// on the Media List document), also capture that row's
				// hyperlink URL. Later on, this lets us match the comment to
				// whichever BODY element links the same piece of media, so the
				// note appears next to the media itself instead of being
				// stuck inside the raw media-list table.
				let rowUrl = null;
				if (isTable) {
					const s = chunkXml.lastIndexOf("<w:tr", cm.index);
					const e = s >= 0 ? chunkXml.indexOf("</w:tr>", cm.index) : -1;
					if (s >= 0 && e > s) {
						const rid = chunkXml.slice(s, e).match(/r:id="([^"]+)"/)?.[1];
						if (rid && rels && rels.get(rid)) rowUrl = rels.get(rid);
					}
				}
				found.push(rowUrl ? { ...c, rowUrl } : { ...c });
			}
			return found;
		};
		// page counter (Writers Template pagination) — bumped by Word's own
		// w:lastRenderedPageBreak records + explicit page breaks; feeds the
		// media list's WTPg No. → lesson mapping for acks grouping
		const page = { current: rules.wt_page_tracking.first_page_number };

		// body = everything inside <w:body> … </w:body>
		const body = xml.slice(xml.indexOf("<w:body>") + 8, xml.lastIndexOf("</w:body>"));

		// walk top-level elements: tables first (they contain paragraphs,
		// so we must not double-read their inner w:p as body paragraphs)
		let pos = 0;
		while (pos < body.length) {
			const nextP = body.indexOf("<w:p ", pos);
			const nextP2 = body.indexOf("<w:p>", pos);
			const nextTbl = body.indexOf("<w:tbl>", pos);
			// earliest of the three markers (-1 = not found → Infinity)
			const candidates = [
				[nextP < 0 ? Infinity : nextP, "p"],
				[nextP2 < 0 ? Infinity : nextP2, "p"],
				[nextTbl < 0 ? Infinity : nextTbl, "tbl"],
			].sort((a, b) => a[0] - b[0]);
			const [at, kind] = candidates[0];
			if (at === Infinity) break;

			// ROUND 265 (CHFUN01): a SELF-CLOSED empty paragraph
			// (<w:p w14:paraId=".."/> — Word's shorthand for an empty
			// paragraph) has no </w:p> at all. It carries no content, so as a
			// top-level block it is simply skipped; letting it fall through to
			// #findClose would mis-count it as an OPEN with no CLOSE (see the
			// matching fix there). Data: paragraph.self_closed_skip.
			// Env toggle: SELFCLOSEP_OFF.
			if (kind === "p" && this.#selfClosedSkipOn(rules)) {
				const gt = body.indexOf(">", at);
				if (gt > 0 && body[gt - 1] === "/") { pos = gt + 1; continue; }
			}

			if (kind === "tbl") {
				const end = this.#findClose(body, at, "w:tbl");
				const tableXml = body.slice(at, end);
				const tblBlock = this.#parseTable(tableXml, rels, page, rules);
				const found = findComments(tableXml, true);
				const all = pendingComments.length ? [...pendingComments, ...found] : found;
				pendingComments = [];
				if (all.length) tblBlock.comments = all;
				blocks.push(tblBlock);
				pos = end;
			} else {
				const end = this.#findClose(body, at, "w:p");
				const paraXml = body.slice(at, end);
				const block = this.#parseParagraph(paraXml, rels, numFormats, page, rules);
				const found = findComments(paraXml);
				// keep empty paragraphs out — they carry no content and the
				// corpus form separates blocks with blank lines anyway
				if (block.text.trim()) {
					const all = pendingComments.length ? [...pendingComments, ...found] : found;
					pendingComments = [];
					if (all.length) block.comments = all;
					blocks.push(block);
				} else if (found.length) {
					// anchor sits in an empty (e.g. image-only) paragraph that is dropped —
					// carry its comments to the next kept block (nearest real element after).
					pendingComments.push(...found);
				}
				pos = end;
			}
		}
		// any comments whose anchor trailed the last real content attach to the last block
		if (pendingComments.length && blocks.length) {
			const last = blocks[blocks.length - 1];
			last.comments = last.comments ? [...last.comments, ...pendingComments] : pendingComments;
		}
		return blocks;
	};

	/**
	 * Finds the index just past the matching close tag, handling nesting
	 * (tables nest tables; paragraphs never nest paragraphs but the same
	 * scanner serves both).
	 *
	 * @param {string} xml - the text being scanned
	 * @param {number} start - index of the opening tag
	 * @param {string} tag - element name, e.g. "w:tbl"
	 * @returns {number} index just after the close tag
	 */
	static #findClose(xml, start, tag) {
		const open = `<${tag}`;
		const close = `</${tag}>`;
		const scSkip = this.#selfClosedSkipOn();
		let depth = 0;
		let i = start;
		while (i < xml.length) {
			const nextOpen = xml.indexOf(open, i);
			const nextClose = xml.indexOf(close, i);
			if (nextClose < 0) return xml.length;
			// an opening tag like <w:tblPr would false-match <w:tbl —
			// require the next char to close the name (space or >)
			if (nextOpen >= 0 && nextOpen < nextClose
				&& (xml[nextOpen + open.length] === ">" || xml[nextOpen + open.length] === " ")) {
				// ROUND 265 (CHFUN01): a SELF-CLOSED element (<w:p .../> —
				// Word's empty-paragraph shorthand, common in table cells)
				// has NO matching close tag. Counting it as an open ratchets
				// the depth up one for ever, so a textbox-carrying paragraph
				// whose scan passes one NEVER finds its close and swallows
				// the rest of the document into ONE giant block (CHFUN01
				// lost every paragraph boundary in the module this way; the
				// TRR203 "mega-paragraph" was the same bug). A self-closed
				// open contributes NOTHING to depth — skip past it.
				// Data: Input_Doc_Rules.paragraph.self_closed_skip.
				// Env toggle: SELFCLOSEP_OFF (reverts to the ratchet).
				if (scSkip) {
					const gt = xml.indexOf(">", nextOpen);
					if (gt > 0 && xml[gt - 1] === "/") { i = gt + 1; continue; }
				}
				depth++;
				i = nextOpen + open.length;
			} else {
				depth--;
				i = nextClose + close.length;
				if (depth === 0) return i;
			}
		}
		return xml.length;
	};

	/**
	 * ROUND 265: is the self-closed-paragraph skip active? (data flag AND
	 * not reverted by the SELFCLOSEP_OFF env toggle).
	 *
	 * @param {Object} [rules] - Input_Doc_Rules.json (defaults to DataService)
	 * @returns {boolean}
	 */
	static #selfClosedSkipOn(rules = null) {
		if (typeof process !== "undefined" && process.env && process.env.SELFCLOSEP_OFF) return false;
		const r = rules ?? ((typeof DataService !== "undefined") ? DataService.Data?.InputDocRules : null);
		return (r?.paragraph?.self_closed_skip?.enabled ?? true) !== false;
	};

	/**
	 * Parses ONE paragraph into a paraBlock (the heart of the extractor).
	 *
	 * RUN HANDLING:
	 * - red runs (w:color in red_hex_values) merge into ONE red span,
	 *   wrapped in the corpus markers
	 * - black bold/italic runs get the markdown markers (corpus convention)
	 * - hyperlinked runs resolve their rId target into block.links
	 * - w:lastRenderedPageBreak / w:br type="page" bump the WT page counter
	 *
	 * @returns {Object} paraBlock
	 */
	static #parseParagraph(xml, rels, numFormats, page, rules) {
		// page bump BEFORE assigning: Word records the break at the start
		// of the first paragraph of the new page.
		// CAUTION (verified on OSAH401): Google-Docs exports write
		// <w:pageBreakBefore w:val="0"/> on nearly EVERY paragraph, meaning
		// "no break" — only a bare element or val="1"/"true" is a real break.
		const breaks = (xml.match(/<w:lastRenderedPageBreak\s*\/>/g) ?? []).length
			+ (xml.match(/<w:br w:type="page"\s*\/>/g) ?? []).length
			+ (xml.match(/<w:pageBreakBefore(?: w:val="(?:1|true)")?\s*\/>/g) ?? []).length;
		if (breaks > 0) page.current += breaks;

		// list detection from the paragraph properties
		let list = null;
		const numId = xml.match(/<w:numId w:val="(\d+)"/)?.[1];
		if (numId) list = numFormats.get(numId) ?? "bullet";
		// NESTING LEVEL: <w:ilvl> is Word's own list-indentation level (0 =
		// top level, 1 = indented one level, and so on). We capture it here
		// and encode it as leading 2-space indentation on the bullet/number
		// prefix text, so the list-rendering code further downstream
		// (#renderBlackText) can rebuild proper NESTED <ul>/<ol> HTML — for
		// example, a bold top-level bullet at ilvl 0 with indented sub-points
		// underneath it at ilvl 1. Stays 0 for an ordinary, non-nested list,
		// or for a paragraph that isn't a list item at all.
		const listLevel = parseInt(xml.match(/<w:ilvl w:val="(\d+)"/)?.[1] ?? "0", 10);

		const links = [];
		// pieces: [{ text, red, bold, italic }] in order — grouped later
		const pieces = [];

		// hyperlink spans first: record target + remember their range so
		// runs inside know their link. We process by replacing hyperlink
		// wrappers with their inner runs, tagging them.
		// Simplest robust approach: walk all runs in order; track whether
		// the run sits inside a w:hyperlink by pre-splitting the XML.
		const segments = xml.split(/(<w:hyperlink [^>]*>|<\/w:hyperlink>)/);
		let currentLink = null;
		for (const seg of segments) {
			const openLink = seg.match(/^<w:hyperlink ([^>]*)>$/);
			if (openLink) {
				const rId = openLink[1].match(/r:id="([^"]+)"/)?.[1];
				currentLink = rId ? (rels.get(rId) ?? null) : null;
				continue;
			}
			if (seg === "</w:hyperlink>") { currentLink = null; continue; }

			// runs inside this segment
			for (const rm of seg.matchAll(/<w:r\b[\s\S]*?<\/w:r>/g)) {
				const run = rm[0];
				// run text: all w:t contents + tabs as spaces — PLUS soft line breaks.
				// THE DROPPED SOFT LINE BREAK (ROUND 227 — the r225 recorded lever, measured
				// 5,999 <w:br> across 357 of 429 WTs). When a writer presses Shift+Enter, Word
				// stores a <w:br/> INSIDE the paragraph; the old w:t-only extraction silently
				// deleted it, GLUING the text on either side with no separator at all
				// ("…ana”Through perseverance…" — corrupted text, corpus-wide; the round-225
				// whakataukī fix patched the symptom inside proverb boxes only). A <w:br/>
				// WITHOUT type="page|column" now contributes "\n" at its own position — the
				// truthful representation of what the writer authored (a line break); the
				// downstream machinery already handles multi-line text (renderBlackText emits
				// one <p>/<li> per line — the majority gold form for soft-broken paragraphs,
				// measured outputs/_measure_softbreak.py; Utils.Fold collapses \s+ so tag
				// CLASSIFICATION is unchanged). The page-break counter above keeps reading
				// type="page" breaks exactly as before.
				// Data: Input_Doc_Rules.paragraph.soft_break_newline   Env toggle: SOFTBR_OFF
				const softBr = rules.paragraph?.soft_break_newline !== false
					&& !(typeof process !== "undefined" && process.env && process.env.SOFTBR_OFF);
				let text = "";
				for (const t of run.matchAll(/<w:t(?: [^>]*)?>([\s\S]*?)<\/w:t>|<w:br(?:\s+[^>]*)?\/>/g)) {
					if (t[0].startsWith("<w:br")) {
						if (softBr && !/w:type="(?:page|column)"/.test(t[0])) text += "\n";
					} else text += this.#decodeXml(t[1]);
				}
				if (/<w:tab\/>/.test(run)) text = ` ${text}`;
				// INVISIBLE-WHITESPACE NORMALISE (ROUND 241 — Dev-Feedback R4, E1: the
				// SCCH302 "AI marker" NBSP; the same extractor seam as the r227 soft-break
				// fix, and table cells arrive through this same paragraph walk). A writer's
				// Word file carries invisible characters that were never intended as page
				// content: the NON-BREAKING SPACE U+00A0 (autocorrect/paste residue —
				// measured 15,198 across 416 of 429 WTs; 2,108 survived into the shipped
				// corpus while the gold library ships effectively none) becomes a plain
				// space, and the ZERO-WIDTH characters U+200B/U+200C/U+200D/U+FEFF
				// (124 occurrences / 22 WTs) are deleted. GRANULARITY SAFETY (the r227
				// red-run trap): an NBSP-only run stays a non-empty whitespace piece
				// (trim()/Fold treat U+00A0 as whitespace before AND after), so red-span
				// merging is untouched; a run the zero-width strip empties drops out like
				// an always-empty run — the tags gate (9557/9557 spans) is the authoritative
				// granularity detector, proven unchanged in the round's probes. Tag
				// classification is inert by construction (Utils.Fold collapses \s+, which
				// already matches U+00A0). Data: Input_Doc_Rules.text_normalise.
				// Env toggle: NBSP_OFF (reverts the whole normalisation).
				const tn = rules.text_normalise;
				if (tn && tn.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.NBSP_OFF)) {
					if (tn.nbsp_to_space !== false) text = text.replace(/\u00A0/g, " ");
					if (tn.strip_zero_width !== false) text = text.replace(/[\u200B\u200C\u200D\uFEFF]/g, "");
				}
				if (!text) continue;

				const color = run.match(/<w:color w:val="([0-9A-Fa-f]{6})"/)?.[1]?.toLowerCase();
				const red = rules.red_runs.red_hex_values.includes(color);
				// <w:b/> means bold on; <w:b w:val="0"/> means explicitly off
				const bold = /<w:b\/>|<w:b w:val="(?:1|true)"\/>/.test(run);
				const italic = /<w:i\/>|<w:i w:val="(?:1|true)"\/>/.test(run);

				// ANSWER MARKS (ROUND 309 — reasons 4+5 of the dropDown catalogue). A writer
				// marks a quiz's correct answer with a yellow HIGHLIGHTER (<w:highlight>,
				// never read before this round) or with GREEN text (00b050 — the writer's
				// answer green; the template's guidance green 316757 stays ignored). The
				// mark is recorded on a SIDE-CHANNEL (block.marks below) and NEVER touches
				// the serialised text, so red-span granularity and every downstream byte
				// are identical by construction — the tags gate (9557/9557) is the canary.
				// A consumer must bring its own fence (round 309's dropDown reading needs
				// the writer's own "Correct answers highlighted / in green" announcement).
				// Data: Input_Doc_Rules.answer_marks   Env toggle: ANSMARK_OFF
				const am = rules.answer_marks;
				const amOn = am && am.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.ANSMARK_OFF);
				let mark = null;
				if (amOn) {
					const hl = run.match(/<w:highlight w:val="([^"]+)"/)?.[1];
					if (hl && !(am.exclude_highlight_values ?? ["none", "white"]).includes(hl)) mark = "hl";
					else if ((am.green_hex_values ?? ["00b050"]).includes(color)) mark = "green";
				}

				if (currentLink) links.push({ text, target: currentLink });
				pieces.push({ text, red, bold, italic, mark });
			}
		}

		// ---- serialise the pieces into the corpus marker-text form ------
		let out = "";
		let i = 0;
		while (i < pieces.length) {
			if (pieces[i].red) {
				// Merge a run of consecutive red runs into ONE marker span.
				//
				// We also BRIDGE a stray NON-RED whitespace run that sits in
				// the MIDDLE of a tag, between two red runs. Word sometimes
				// splits what the writer typed as a single, uniformly-red
				// "[tag]" into several separate XML runs, and in the process
				// can lose the red colour on just the interior space
				// character — which fragments one tag into two separate
				// marker spans. A real example of the broken shape this
				// produces: a tag like
				// "[Please embed this journal story (as in ANZHFUN01 phase 2]"
				// arriving as two pieces — "...phase 2" coloured red, then a
				// single space that lost its colour, then "]" coloured red
				// again.
				// The bridge only fires when ALL of these are true:
				//   - the red text collected SO FAR is mid-tag (it has an
				//     unmatched "[" that hasn't been closed by a "]" yet)
				//   - the non-red gap run is pure whitespace (nothing else)
				//   - the very NEXT run after the gap is red again
				// That combination means it's safe to re-glue the two red
				// pieces back into one tag — it can never accidentally pull
				// in real black body text, and it can never merge two
				// separate, complete tags into one.
				// (The ordinary case — Word splitting same-colour text into
				// multiple runs, e.g. "[Tab 1: I" + "ntroduction" + "]" —
				// is already handled by the consecutive-red merge loop
				// below; this bridge only covers the case where the colour
				// itself gets dropped on one small gap.)
				// Data flag: Input_Doc_Rules.json red_runs.bridge_split_tag
				// Env toggle: REDBRIDGE_OFF (disables the bridge, so the tag
				// stays fragmented into two marker spans)
				const bridgeOn = rules.red_runs.bridge_split_tag
					&& !(typeof process !== "undefined" && process.env && process.env.REDBRIDGE_OFF);
				let redText = "";
				while (i < pieces.length) {
					if (pieces[i].red) { redText += pieces[i].text; i++; continue; }
					// SOFT-BREAK-ONLY GAP (ROUND 227, part of the w:br→\n fix). A soft line
					// break often lives in a COLOURLESS run of its own between two red runs
					// ("[Overview]" ⏎ "[H3] Knowledge" — one paragraph, the tags on separate
					// lines). Before the fix that run carried NO text at all, so it was
					// INVISIBLE here and the two red runs merged into ONE marker span; the
					// "\n" it now contributes must therefore also merge INTO the span —
					// otherwise it would SPLIT the span in two and change tag GRANULARITY
					// corpus-wide (caught live on SSOG103: the standalone "[Overview]" alias
					// flipped the whole lesson-menu partition). Utils.Fold collapses the \n,
					// so the merged span parses byte-identically to the pre-fix glued form
					// (proven: primary/tags/RenderText identical). ONLY a pure-newline piece
					// bridges this way — a piece with any other character (even a plain
					// space) was already a visible separator before the fix and keeps its
					// existing two-span behaviour.
					if (pieces[i].text && /^\n+$/.test(pieces[i].text)
						&& i + 1 < pieces.length && pieces[i + 1].red) {
						redText += pieces[i].text; i++; continue;
					}
					const opens = (redText.match(/\[/g) || []).length;
					const closes = (redText.match(/\]/g) || []).length;
					if (bridgeOn && opens > closes && pieces[i].text.trim() === ""
						&& i + 1 < pieces.length && pieces[i + 1].red) {
						redText += pieces[i].text; i++; continue;   // bridge the whitespace gap mid-tag
					}
					break;
				}
				// A WHITESPACE-ONLY red span: sometimes a writer accidentally
				// colours just a single space or tab character red, with no
				// real text in it. If we wrapped that lone space in a
				// [RED TEXT] marker like any other red span, PageSplitter
				// would treat it as a standalone tag-like item and FRAGMENT
				// the paragraph in two at that point — e.g. "**Banter is**
				// like other things..." would get chopped into two separate
				// <p> elements right at the accidentally-red space. Instead,
				// when the collected red text is NOTHING BUT whitespace, we
				// just emit a single plain space character (no marker at
				// all) so the paragraph stays in one piece. This only ever
				// fires when the red run is PURE whitespace — any real
				// [tag] or written instruction (anything with actual
				// non-whitespace content) always keeps its marker and is
				// never dropped.
				// Data flag: Input_Doc_Rules.json red_runs.collapse_whitespace_only
				// Env toggle: REDWS_OFF (reverts to wrapping the whitespace
				// in a marker and letting the paragraph fragment)
				const collapseRedWs = rules.red_runs.collapse_whitespace_only
					&& !(typeof process !== "undefined" && process.env && process.env.REDWS_OFF);
				if (collapseRedWs && redText.trim() === "") out += " ";
				else out += `${rules.red_runs.marker_open}${redText}${rules.red_runs.marker_close}`;
			} else {
				// merge consecutive black runs sharing the same bold/italic
				const { bold, italic } = pieces[i];
				let blackText = "";
				while (i < pieces.length && !pieces[i].red
					&& pieces[i].bold === bold && pieces[i].italic === italic) {
					blackText += pieces[i].text; i++;
				}
				// markdown markers only when the text has substance —
				// never wrap pure whitespace (it renders as stray asterisks)
				if (blackText.trim()) {
					// PRESERVING THE SPACE BEFORE A BOLD/ITALIC WORD: trim()
					// removes whitespace from BOTH ends, but Word often stores
					// the space BETWEEN two words as the LEADING character of
					// the next styled run rather than as the TRAILING
					// character of the previous run. For example, the plain
					// run might contain "...their" (no trailing space) while
					// the very next bold run contains " wellbeing or hauora"
					// (WITH a leading space). If we simply trim() that bold
					// run's text, we lose the leading space and the two words
					// get glued together with no gap: "their<b>wellbeing...".
					// So we restore the leading space SYMMETRICALLY with the
					// trailing space — but ONLY when the original run actually
					// started with a space, so a case where the words were
					// genuinely meant to run together (no leading space in the
					// source) is left exactly as it was.
					// Data flag: Input_Doc_Rules.json formatting_markers.preserve_leading_space
					// Env toggle: BOLDSPACE_OFF (reverts to only restoring the
					// trailing space, not the leading one)
					const keepLead = rules.formatting_markers.preserve_leading_space
						&& !(typeof process !== "undefined" && process.env && process.env.BOLDSPACE_OFF);
					const lead = (keepLead && blackText.startsWith(" ")) ? " " : "";
					const tail = blackText.endsWith(" ") ? " " : "";
					if (bold) blackText = `${lead}${rules.formatting_markers.bold}${blackText.trim()}${rules.formatting_markers.bold}${tail}`;
					else if (italic) blackText = `${lead}${rules.formatting_markers.italic}${blackText.trim()}${rules.formatting_markers.italic}${tail}`;
				}
				out += blackText;
			}
		}

		// bullet / number prefix so the downstream list builder sees the corpus form.
		// LEADING INDENT encodes the nesting level (2 spaces per ilvl) — #renderBlackText
		// reads it to build nested <ul>/<ol>; a flat (ilvl 0) list is unchanged.
		const indent = "  ".repeat(Math.max(0, listLevel));
		if (list === "bullet" && out.trim()) out = `${indent}${rules.formatting_markers.bullet_prefix}${out}`;
		if (list === "number" && out.trim() && !/^\s*\d+[.)]/.test(out)) out = `${indent}1. ${out}`;

		// ANSWER-MARK side-channel (ROUND 309): merge consecutive same-kind marked
		// pieces (Word fragments one highlighted phrase into several runs; a pure
		// whitespace gap between two same-kind marked pieces bridges — the red-merge
		// convention). block.text is untouched — the marks travel beside it.
		const marks = [];
		{
			let cur = null;
			const flush = () => { if (cur && cur.text.trim()) marks.push({ text: cur.text.trim(), kind: cur.kind }); cur = null; };
			for (const p of pieces) {
				if (p.mark) {
					if (cur && cur.kind === p.mark) { cur.text += p.text; continue; }
					flush(); cur = { text: p.text, kind: p.mark };
				} else if (cur && /^\s*$/.test(p.text)) cur.text += p.text;
				else flush();
			}
			flush();
		}

		const blk = { kind: "para", text: out, links, wtPage: page.current, list, listLevel };
		if (marks.length) blk.marks = marks;
		return blk;
	};

	/**
	 * Parses ONE table into a tableBlock, serialising each cell with the
	 * same paragraph logic (so red tags INSIDE tables keep their markers —
	 * interactives' data tables depend on this).
	 *
	 * @returns {Object} tableBlock
	 */
	static #parseTable(xml, rels, page, rules) {
		const links = [];
		const rows = [];
		const rowLinks = [];   // hyperlinks per ROW — the media list parser
		                       // must never guess which row a URL belongs to
		// table page = page at the point the table starts; cell-level breaks
		// also bump the global counter as they're encountered
		const tablePage = page.current;

		let anyCellMark = false;
		const cellMarks = [];   // rows-aligned: cellMarks[r][c] = [{text,kind}] (ROUND 309)
		for (const rowMatch of xml.matchAll(/<w:tr\b[\s\S]*?<\/w:tr>/g)) {
			const cells = [];
			const thisRowLinks = [];
			const thisRowMarks = [];
			for (const cellMatch of rowMatch[0].matchAll(/<w:tc\b[\s\S]*?<\/w:tc>/g)) {
				// every paragraph in the cell, joined with the in-cell
				// line-break marker (phase-4 convention: " / ")
				const paras = [];
				const cm = [];
				for (const pm of cellMatch[0].matchAll(/<w:p[ >][\s\S]*?<\/w:p>/g)) {
					const block = this.#parseParagraph(pm[0], rels, new Map(), page, rules);
					if (block.text.trim()) paras.push(block.text.trim());
					links.push(...block.links);
					thisRowLinks.push(...block.links);
					if (block.marks) cm.push(...block.marks);   // the r309 answer-mark side-channel
				}
				cells.push(paras.join(rules.table_markers.in_cell_line_break));
				thisRowMarks.push(cm);
				if (cm.length) anyCellMark = true;
			}
			rows.push(cells);
			rowLinks.push(thisRowLinks);
			cellMarks.push(thisRowMarks);
		}

		// the corpus text form — what the tag pipeline scans
		const tm = rules.table_markers;
		const text = [
			tm.open,
			...rows.map((cells) => `${tm.row_prefix}${cells.join(tm.column_separator)}`),
			tm.close,
		].join("\n");

		const blk = { kind: "table", rows, rowLinks, links, wtPage: tablePage, text };
		if (anyCellMark) blk.cellMarks = cellMarks;   // ROUND 309 answer-mark side-channel
		return blk;
	};

	/**
	 * Decodes the five XML entities Word writes into text content.
	 * @param {string} s
	 * @returns {string}
	 */
	static #decodeXml(s) {
		return s
			.replace(/&lt;/g, "<").replace(/&gt;/g, ">")
			.replace(/&quot;/g, '"').replace(/&apos;/g, "'")
			.replace(/&amp;/g, "&");
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { DocxExtractor };
