/**
 * BilingualBuilder.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Everything to do with rendering a BILINGUAL ("reoTranslate") module's
 * body — a module whose Writers Template author wrote every piece of
 * content TWICE, once in English and once in Te Reo Māori, laid out as a
 * two-column "English | Māori" table. The finished page does NOT show two
 * separate tables side by side — it shows the content INTERLEAVED, Māori
 * element first then its English counterpart, each tagged with a `reo` or
 * `eng` language attribute so the site's front-end can style/toggle them.
 * This file is the machinery that reads the writer's raw table shape and
 * produces that interleaved output. Sixteen statics + five regex fields,
 * grouped by what they're responsible for:
 *
 *   - bilingualTable / bilingualRows / bilingualSplit / langAttr /
 *         bilingualHeader   THE CORE UNFOLD: given a 2-column
 *         English-then-Māori content table, walk it row by row and emit
 *         the Māori cell FIRST then the English cell (interleaved
 *         per-element, not per-row, when section grouping — see below — is
 *         active), with any media (image/audio/video) emitted only ONCE
 *         since it isn't language-specific. Data elements.dual_language.
 *   - bilingualSection / bilingualSectionNum / bilingualLessonNum /
 *         bilingualLessonTitleHtml / reoLessonLetter /
 *         reoActivityNumFromBlock   SECTION GROUPING: the human wraps a
 *         whole bilingual lesson section (opened either by a `[H1] N.M`
 *         decimal sub-section number, or by a `[H2] Lesson N` heading) in
 *         ONE tidy nested wrapper (row > col-md-8 > div.activity when the
 *         section holds a real interactive widget, or a plain grouped
 *         column when it's just prose/media) instead of leaving every
 *         table as its own flat, disconnected row. Data
 *         dual_language.section_grouping (env toggles REONEST_OFF /
 *         REOLESSON_OFF / REOTABLE_OFF).
 *   - bilingualContainer   CALLOUT BOXES: a bilingual table whose first
 *         cell leads with a callout tag (whakataukī / alert / supervisor
 *         note / wānanga / quote) is built as the matching container
 *         (div.whakatauki, div.alert, row.supervisor, …) with its rows
 *         unfolded reo/eng INSIDE it.
 *   - bilingualActivity / isActivityMarker / isCalloutTable   ACTIVITY
 *         GATHERING: recognises the `[Activity Embedded]` marker table
 *         plus whatever widget-spec tables follow it, and gathers them
 *         all into ONE `div.activity[number]` box.
 *   - bilingualAudioImage   PHONICS GRID: recognises a table laid out as
 *         one IMAGE row above one AUDIO row (the phonics/letter-sound
 *         teaching pattern) and builds it as a row of
 *         `col.paddingR > .audioImage` tiles instead of leaving it as raw
 *         table markup. Data dual_language.audio_image (env AUDIOIMG_OFF).
 *
 * WHY SEPARATE FILE:
 * Bilingual rendering is a genuinely self-contained sub-system: none of
 * these statics touch the main content-converter's own running state
 * (page-lesson counters, open-container stack, etc.) — they only read
 * DataService.Data (the shared data-driven config, as everywhere in this
 * codebase) and a small set of values passed in explicitly as arguments.
 * The one thing they DON'T own is the tag normaliser (the class that turns
 * a raw `[Tag]` string into a resolved, canonical tag) — that instance is
 * created and owned by ContentConverter, which passes it into every method
 * here that needs it as a trailing `norm` argument, exactly the same
 * pattern TablesAndGrids and MenuBuilder use. The overall on/off switch for
 * bilingual handling (env toggle REOTRANSLATE_OFF, which decides whether a
 * module even ENTERS "reo mode" in the first place) lives in
 * ContentConverter, not here — this file only ever runs once that decision
 * has already been made upstream.
 *
 * JARGON, EXPLAINED:
 *   - "reoTranslate" / "reo mode"  the module-wide flag meaning "this
 *     module's body content is authored bilingually and needs unfolding."
 *   - "Te Reo" / "reo"  Te Reo Māori, the indigenous language of New
 *     Zealand; many Te Kura modules are published in both English and
 *     Māori.
 *   - "unfold"  turning the writer's compact 2-column table into the
 *     site's actual interleaved HTML elements.
 *
 * WHEN TO WORK HERE:
 * - Changing how a plain bilingual content table is unfolded into
 *   interleaved reo/eng elements -> bilingualTable / bilingualRows /
 *   bilingualSplit.
 * - Changing how a whole lesson SECTION is grouped/boxed -> bilingualSection
 *   and its helper methods.
 * - Changing how a bilingual callout/activity table is built ->
 *   bilingualContainer / bilingualActivity.
 * - Changing how the image-over-audio phonics grid is built ->
 *   bilingualAudioImage.
 * ===========================================================================
 */

class BilingualBuilder {

	/**
	 * THE BILINGUAL reo/eng UNFOLD — turns a plain 2-column (or 4-column,
	 * with the two extra columns used for proofreading marks) "English |
	 * Māori" content table into the site's actual interleaved output.
	 *
	 * WHAT/HOW: for each row, emits the MĀORI cell (column 2) FIRST as a
	 * `<tag reo>` element, then the ENGLISH cell (column 1) SECOND as a
	 * `<tag eng>` element, all inside ONE shared `row > col-md-8` wrapper;
	 * any media in the row (image/audio/video) is emitted only ONCE since
	 * it isn't language-specific and doesn't need a reo/eng pair. Returns
	 * null when the table isn't actually an English|Māori bilingual table
	 * at all (its header row doesn't say so) — that lets a front-matter,
	 * widget-spec, or plain data table safely fall through to the normal,
	 * non-bilingual rendering paths instead.
	 *
	 * @param {Object} block - a table block, e.g. { rows: [["English","Māori"], ["Hello","Kia ora"]] }
	 * @param {ConversionRun} run - the current run
	 * @param {TagNormaliser} norm - resolves any `[Tag]` markers found inside cells
	 * @returns {string|null} the rendered wrapper HTML, or null when this isn't a bilingual table
	 */
	static bilingualTable(block, run, norm, forceNoHeader = false) {
		const cfg = DataService.Data.EmitTemplates.elements?.dual_language;
		if (!cfg || cfg.enabled === false) return null;
		const rows = block.rows ?? [];
		if (rows.length < 2 || !Array.isArray(rows[0]) || rows[0].length < 2) return null;
		// requires an English|Māori header row — EXCEPT for the table the
		// [MODULE CONTENT: PAGE n] marker introduced (ROUND 212, the MTK
		// drop-down-menu template): PNR102/PNR104 open that table with
		// "Module Introduction | Kōwae Ako Whakataki" instead of the header,
		// but the column orientation is the same English|Māori as everywhere
		// else in the template (the caller passes forceNoHeader=true for it).
		if (!forceNoHeader && !this.bilingualHeader(block)) return null;
		const out = this.bilingualRows(block, run, undefined, norm);
		if (!out.length) return null;
		let html = `${cfg.wrapper_open}\n${out.join("\n")}\n${cfg.wrapper_close}`;
		// Sometimes the content table EMBEDS a widget reference (the writer wrote
		// `[Interactive] [Flipcard]`/`[Carousel]`/… INLINE in the middle of the body
		// text); the human build shows that widget SEPARATELY, after the intro prose,
		// rather than swallowing the whole table into the widget itself. The
		// over-capture guard elsewhere correctly stops the WHOLE table being captured
		// as that widget — but that means the WIDGET placeholder marker the human
		// build ships is otherwise lost entirely (the module-structure comparison
		// tooling then dips on modules that never got a placeholder box at all, e.g.
		// TRR113). So here we append ONE extra cv2 placeholder box after the unfolded
		// prose (it collapses to the same generic "un-built widget" marker the
		// comparison tooling recognises) so the unfolded prose KEEPS a visible trace
		// of its widget. Only fires for an actual bracketed widget invocation — never
		// for ordinary [H#]/[Body]/[Item]/[Image]/[Audio] content markers. Gated by
		// content_table_guard.
		const guard = cfg.content_table_guard;
		if (guard && guard.enabled !== false
			&& /\[\s*(?:interactive|flip\s?cards?|carousel|audio\s?hover|drop\s?down|multi(?:ple)?\s?choice|word\s?(?:find|select)|memory\s?game|radio\s?button|sketcher|drag\s?and\s?drop|word\s?drag|reorder|crossword)\b/i.test(block.text || "")) {
			html += `\n<div class="cv2-interactive bilingual-unbuilt">\n<p style="color: #d9480f; font-weight: bold">⚙ INTERACTIVE (un-built) — bilingual widget embedded in the content table; develop from the source table.</p>\n</div>`;
		}
		return html;
	};

	// Matches a bilingual content cell that REFERENCES an interactive widget inline
	// (e.g. the writer wrote "[Interactive] [Flipcard]" or "[Carousel]" as part of
	// the cell's own text) rather than the widget having its own separate table.
	// The human build renders that widget SEPARATELY from the unfolded prose.
	// Shared by bilingualTable (which appends the placeholder-box guard) and
	// bilingualSection (which uses it to spot a section's embedded-widget marker).
	static embeddedWidgetRe = /\[\s*(?:interactive|flip\s?cards?|carousel|audio\s?hover|drop\s?down|multi(?:ple)?\s?choice|word\s?(?:find|select)|memory\s?game|radio\s?button|sketcher|drag\s?and\s?drop|word\s?drag|reorder|crossword)\b/i;
	// Matches a bilingual SECTION-opening tag: a [H1] tag whose text is a decimal
	// sub-section number like "1.1", "1.2", "2.1" — this is what tells bilingualSection
	// a new lesson section is starting.
	static sectionNumRe = /\[\s*h1\s*\]\s*(\d+\.\d+)/i;
	// Matches a standalone "Activity NX:" / "Ngohe NX:" label line on its own (e.g.
	// "Activity 1A:") — the human LIFTS this number up onto the activity box's own
	// number= attribute instead of ever rendering it as ordinary body prose, so
	// wherever this matches, the line itself gets dropped from the rendered output.
	// Matched against the element's text with any [tag] markers already stripped out.
	static actLabelRe = /^\s*(?:activity|ngohe)\s*\d+\s*[a-z]?\s*:?\s*$/i;

	/**
	 * Pulls the activity number (e.g. "1A") out of a block's own
	 * "Activity NX:" / "Ngohe NX:" text, if it has one.
	 *
	 * @param {Object} block - a content block
	 * @returns {string|null} the upper-cased, whitespace-free number (e.g. "1A"), or null when the block carries no such label
	 */
	static reoActivityNumFromBlock(block) {
		const m = /\b(?:activity|ngohe)\s*([0-9]+\s*[a-z]?)\s*:/i.exec(block?.text || "");
		return m ? m[1].replace(/\s+/g, "").toUpperCase() : null;
	};

	/**
	 * The INNER-rows half of the bilingual unfold, factored out of
	 * bilingualTable so bilingualSection (below) can also call it and nest
	 * the result inside its own section wrapper.
	 *
	 * WHAT IT DOES: returns the interleaved
	 * `<tag reo>{Māori}</tag><tag eng>{English}</tag>` elements plus a
	 * separate media array, for a 2-column (or 4-column, with proofing
	 * columns) bilingual table — WITHOUT the outer `row > col-md-8`
	 * wrapper bilingualTable adds, so a caller that wants to nest this
	 * content inside a bigger structure (a lesson section box) can do so
	 * freely. Skips the `English|Māori` header row when the table has one;
	 * a header-less section table's leading `[H1]/[H2]/[Body]` rows are
	 * treated as ordinary content instead.
	 *
	 * @param {Object} block - a bilingual table block
	 * @param {ConversionRun} run - the current run
	 * @param {number} [fromRow] - row index to start from (used by a `[H2] Lesson N` opener to skip its own title row, which is rendered separately); when omitted, the default header-skip rule applies
	 * @param {TagNormaliser} norm - resolves any `[Tag]` markers found inside cells
	 * @returns {string[]} rendered, interleaved reo/eng element and media HTML fragments, in emission order
	 */
	static bilingualRows(block, run, fromRow, norm) {
		const rows = block?.rows ?? [];
		if (!rows.length || !Array.isArray(rows[0]) || rows[0].length < 2) return [];
		// A [H2] Lesson N opener passes fromRow explicitly to SKIP its own title row
		// (that row is rendered separately, as a bare col-md-8 <h2>, by
		// bilingualLessonTitleHtml below); every other caller just uses the default
		// header-skip rule — skip row 0 when it's the English|Māori header, else start
		// from row 0.
		const start = (fromRow !== undefined) ? fromRow : (this.bilingualHeader(block) ? 1 : 0);
		// When section grouping (the "keystone" holistic-nesting feature — see
		// bilingualSection below) is ON, INTERLEAVE reo/eng PER ELEMENT instead of per
		// row (Māori then English for each parallel paragraph — reo, eng, reo, eng —
		// matching the human build's own element order) and STRIP the standalone
		// "Activity NX:" label line (its number is lifted onto the box's own number=
		// attribute instead). This whole per-element interleave is gated behind
		// section_grouping being enabled, so bilingualTable's plain standalone unfold
		// (used when there's no section grouping at all) stays exactly as it was
		// before section grouping existed, whenever section grouping is switched off.
		const scfg = DataService.Data.EmitTemplates.elements?.dual_language?.section_grouping;
		const interleave = !!scfg && scfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.REONEST_OFF);
		const out = [];
		for (let r = start; r < rows.length; r++) {
			const reoCell = rows[r][1], engCell = rows[r][0];   // col-2 = Māori, col-1 = English
			const R = this.bilingualSplit(reoCell, run, norm);
			const E = this.bilingualSplit(engCell, run, norm);
			if (interleave) {
				const strip = (arr) => arr.filter((h) => !this.actLabelRe.test(String(h).replace(/<[^>]+>/g, "").trim()));
				const Rt = strip(R.text), Et = strip(E.text);
				const n = Math.max(Rt.length, Et.length);
				for (let k = 0; k < n; k++) {
					if (k < Rt.length) out.push(this.langAttr(Rt[k], "reo"));   // Māori element FIRST
					if (k < Et.length) out.push(this.langAttr(Et[k], "eng"));   // English element SECOND
				}
			} else {
				for (const p of R.text) out.push(this.langAttr(p, "reo"));   // Māori text FIRST
				for (const p of E.text) out.push(this.langAttr(p, "eng"));   // English text SECOND
			}
			const media = R.media.length ? R.media : E.media;             // media ONCE (un-paired)
			for (const m of media) out.push(m);
		}
		return out;
	};

	/**
	 * Reads the `[H1] N.M` decimal section number out of a table, if this
	 * table is the one that OPENS a bilingual lesson section.
	 *
	 * HOW: robust to the writer's `**bold**` / red-text cell markers; the
	 * number sits in the first content row (right after an English|Māori
	 * header row, if there is one), so only the leading few rows are
	 * scanned rather than the whole table.
	 *
	 * @param {Object} block - a table block
	 * @returns {string|null} the section number (e.g. "1.2"), or null when this table doesn't open a section
	 */
	static bilingualSectionNum(block) {
		const rows = block?.rows ?? [];
		if (!rows.length || !Array.isArray(rows[0]) || rows[0].length < 2) return null;
		const strip = (s) => String(s ?? "").replace(/🔴|\[\/?RED TEXT\]/g, "").replace(/\*/g, "");
		for (let r = 0; r < Math.min(rows.length, 3); r++) {
			for (const c of (rows[r] || [])) {
				const m = strip(c).match(this.sectionNumRe);
				if (m) return m[1];
			}
		}
		return null;
	};

	/**
	 * Reads the lesson number out of a table, if this table OPENS a
	 * `[H2] (Lesson|Hei Mahi|Ngohe) N` lesson activity (an alternative
	 * section-opener style used by some bilingual module families,
	 * alongside the `[H1] N.M` style bilingualSectionNum reads above).
	 *
	 * HOW: the lesson heading sits in the FIRST content row (right after
	 * an English|Māori header row, if there is one) — ONLY that row is
	 * scanned, so a "Lesson N" mention appearing somewhere DEEPER inside
	 * the table can never be mistaken for a real section opener. Robust
	 * to the writer's `**bold**` / red-text cell markers. Data
	 * section_grouping.lesson_heading.pattern.
	 *
	 * @param {Object} block - a table block
	 * @returns {number|null} the lesson number, or null when this table doesn't open a lesson (or the lesson_heading feature is disabled)
	 */
	static bilingualLessonNum(block) {
		const lcfg = DataService.Data.EmitTemplates.elements?.dual_language?.section_grouping?.lesson_heading;
		if (!lcfg || lcfg.enabled === false) return null;
		const rows = block?.rows ?? [];
		if (!rows.length || !Array.isArray(rows[0]) || rows[0].length < 2) return null;
		const re = new RegExp(lcfg.pattern || "\\[\\s*h2\\s*\\]\\s*(?:lesson|hei\\s*mahi|ngohe)\\s+(\\d+)", "i");
		const strip = (s) => String(s ?? "").replace(/🔴|\[\/?RED TEXT\]/g, "").replace(/\*/g, "");
		const start = this.bilingualHeader(block) ? 1 : 0;
		for (const c of (rows[start] || [])) {
			const m = strip(c).match(re);
			if (m) return parseInt(m[1], 10);
		}
		return null;
	};

	/**
	 * Renders a `[H2] Lesson N` opener's TITLE row as a bare
	 * `row > col-md-8 > <h2 reo>{Māori}</h2><h2 eng>{English}</h2>`, kept
	 * OUTSIDE the activity box that follows it — the human build keeps the
	 * lesson title ungrouped, at its own configured heading level, rather
	 * than nesting it inside the section's box.
	 *
	 * HOW: the heading level is FORCED onto the rendered `<h#>` tags so
	 * that the site-wide automatic heading re-levelling pass (which can
	 * otherwise demote headings based on document structure) can never
	 * push this title below the human's expected `<h2>`.
	 *
	 * @param {Object} block - the table block that opens the lesson
	 * @param {number} rowIdx - which row holds the title (the header row is already skipped by the caller)
	 * @param {ConversionRun} run - the current run
	 * @param {TagNormaliser} norm - resolves any `[Tag]` markers in the title cells
	 * @returns {string} the rendered title wrapper HTML, or "" when the row is empty
	 */
	static bilingualLessonTitleHtml(block, rowIdx, run, norm) {
		const row = (block?.rows ?? [])[rowIdx];
		if (!Array.isArray(row) || row.length < 2) return "";
		const lvl = DataService.Data.EmitTemplates.elements?.dual_language?.section_grouping?.lesson_heading?.title_level || 2;
		const force = (h) => String(h)
			.replace(/^(\s*<)h[1-6]\b/i, `$1h${lvl}`)
			.replace(/<\/h[1-6]>(\s*)$/i, `</h${lvl}>$1`);
		const R = this.bilingualSplit(row[1], run, norm), E = this.bilingualSplit(row[0], run, norm);
		const out = [];
		for (const p of R.text) out.push(this.langAttr(force(p), "reo"));   // Māori FIRST
		for (const p of E.text) out.push(this.langAttr(force(p), "eng"));   // English SECOND
		if (!out.length) return "";
		return `<div class="row">\n<div class="col-md-8 col-12">\n${out.join("\n")}\n</div>\n</div>`;
	};

	/**
	 * Returns the next RESEQUENCED activity letter (A, B, C, D…) for a box
	 * in lesson `lessonNum`.
	 *
	 * WHY: the human build numbers a lesson's activities sequentially
	 * WITHIN that lesson (1st activity = A, 2nd = B, …), discarding
	 * whatever irregular letters the writer originally used in the
	 * Writers Template (a writer might jump from "1A" straight to "1E" to
	 * "1H"). This keeps a running counter per (run, lessonNum) pair so
	 * repeated calls for the same lesson keep advancing through the
	 * alphabet correctly.
	 *
	 * @param {ConversionRun} run - the current run (the counter is stored on it)
	 * @param {number} lessonNum - which lesson this activity belongs to
	 * @returns {string} the next letter, "A" through "Z" (capped at Z past the 26th activity in one lesson)
	 */
	static reoLessonLetter(run, lessonNum) {
		if (!run._reoLessonSeq) run._reoLessonSeq = {};
		const n = run._reoLessonSeq[lessonNum] = (run._reoLessonSeq[lessonNum] || 0) + 1;
		return String.fromCharCode(64 + Math.min(n, 26));   // 1->A, 2->B, …
	};

	/**
	 * BILINGUAL SECTION GROUPING — the "keystone" holistic-nesting build
	 * that turns a run of separate, disconnected bilingual tables into ONE
	 * properly nested lesson-section box, matching how the human build
	 * structures a Te Reo lesson.
	 *
	 * WHY THIS EXISTS: the human build wraps every Te Reo lesson SECTION
	 * (opened either by a `[H1] N.M` decimal sub-section number, or by a
	 * `[H2] Lesson N` heading — see below) in ONE consistent nested
	 * structure:
	 *   `row > col-md-8 col-12 > div.activity > row > col-12 >
	 *    { heading + reo/eng prose + audioImage grid + the widget }`
	 * Rendering each table in a section as its own flat, standalone row
	 * (the naive approach) produces the right CONTENT but the wrong SHAPE
	 * — everything ends up at the wrong nesting depth compared to the
	 * human build. This method is what assembles the correct nested shape.
	 *
	 * HOW IT WORKS: once triggered by a section-opening table, it GATHERS
	 * every following item that belongs to the same section — bilingual
	 * content tables (unfolded via bilingualRows), audioImage phonics
	 * grids, a captured interactive-widget bundle (folded down to ONE cv2
	 * placeholder marker, and the normal widget-bundle rendering path is
	 * told to skip it so it doesn't ALSO get rendered separately), and
	 * plain black prose — STOPPING as soon as it hits the next section
	 * opener, a standalone callout box (which gets its own box instead),
	 * a phase break, or any item type it doesn't recognise. Once gathering
	 * stops, the FLAT list of gathered content is wrapped in the human's
	 * nesting: a section that ended up holding a real interactive widget
	 * becomes `div.activity interactive`; a section that's just prose/media
	 * becomes a bare grouped `col-md-8` column instead (no activity box at
	 * all, since the human build only boxes sections that need one).
	 *
	 * TWO WAYS A SECTION CAN OPEN:
	 *   1. A `[H1] N.M` decimal sub-section number (the original,
	 *      most-common trigger).
	 *   2. (When section_grouping.lesson_heading is enabled, env toggle
	 *      REOLESSON_OFF) A `[H2] Lesson N` heading, used by a different
	 *      family of bilingual modules that structures lessons this way
	 *      instead. In this case the lesson TITLE is split out and
	 *      rendered as a bare, ungrouped `col-md-8 <h2>` (via
	 *      bilingualLessonTitleHtml above); the activity content gathers
	 *      into the box starting from the row AFTER the title; the box's
	 *      number= attribute is resequenced as `{lessonNum}{A,B,C…}` (via
	 *      reoLessonLetter above); and gathering also stops at the NEXT
	 *      `[H2] Lesson N` heading, so a trailing alert/"Finished" section
	 *      correctly falls outside the box rather than being swallowed
	 *      into it.
	 * The two trigger styles are mutually exclusive by construction (a
	 * table can't match both patterns), so there's never any ambiguity
	 * about which family a given module belongs to.
	 *
	 * @param {Object[]} bodyItems - the page's flat list of parsed body items
	 * @param {number} i - index of the candidate section-opening item
	 * @param {ConversionRun} run - the current run
	 * @param {Object[]} bundles - captured interactive-widget bundles (indexed by consumedBy)
	 * @param {TagNormaliser} norm - resolves any `[Tag]` markers found in cells
	 * @returns {{html: string, next: number}|null} the rendered section HTML plus the index to resume scanning from, or null when item `i` doesn't open a section (or the feature is disabled)
	 */
	static bilingualSection(bodyItems, i, run, bundles, norm) {
		const cfg = DataService.Data.EmitTemplates.elements?.dual_language;
		const scfg = cfg && cfg.section_grouping;
		if (!scfg || scfg.enabled === false
			|| (typeof process !== "undefined" && process.env && process.env.REONEST_OFF)) return null;
		const it0 = bodyItems[i];
		if (!it0 || it0.type !== "table") return null;
		// This table can open a section in EITHER of two ways: the original [H1] N.M
		// keystone style, or (only when lesson_heading is enabled and there's no
		// [H1] N.M match) the [H2] Lesson N lesson-activity style used by a different
		// family of bilingual modules. The two opener markers are disjoint, so a
		// table can never be mistaken for both at once.
		const lessonOn = scfg.lesson_heading && scfg.lesson_heading.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.REOLESSON_OFF);
		const isH1 = this.bilingualSectionNum(it0.block) !== null;
		const lessonNum = (lessonOn && !isH1) ? this.bilingualLessonNum(it0.block) : null;
		const openedByLesson = lessonNum !== null;
		if (!isH1 && !openedByLesson) return null;
		const guardOn = cfg.content_table_guard && cfg.content_table_guard.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.REOTABLE_OFF);
		// A [H2] Lesson N opener renders its TITLE as a bare col-md-8 <h2>, OUTSIDE
		// the activity box (see bilingualLessonTitleHtml above); the activity content
		// itself is gathered starting from the row AFTER the title row (openerFromRow).
		let titleHtml = "", openerFromRow;
		if (openedByLesson) {
			const tstart = this.bilingualHeader(it0.block) ? 1 : 0;
			titleHtml = this.bilingualLessonTitleHtml(it0.block, tstart, run, norm);
			openerFromRow = tstart + 1;
		}
		const inner = [];
		let hasWidget = false;   // a TRUE interactive widget → the section is a div.activity (selective)
		let number = null;       // the "Activity NX:" number → the box's number= attr
		let j = i;
		for (; j < bodyItems.length; j++) {
			const nx = bodyItems[j];
			if (j > i) {   // a section never stops on its own opener row
				if (nx.type === "phasebreak") break;
				// A [H2] Lesson N box ends at the lesson's own closing callout (e.g. a
				// "Remember" alert box, which arrives as a CONTAINER_OPEN tag rather than
				// a table), so that alert plus any "Finished" tail content that follows it
				// render OUTSIDE the activity box, matching the human build. This check is
				// scoped to the lesson-heading style only — the original [H1] N.M keystone
				// style is untouched by it.
				if (openedByLesson && nx.type === "tag" && nx.consumedBy === undefined
					&& nx.parse?.primary?.directive === "CONTAINER_OPEN") break;
				// Also stop at the next section opener of EITHER style — another [H1] N.M
				// table, a standalone callout table (which gets its own box instead), or
				// (when the lesson-heading style is on) the next [H2] Lesson N table.
				if (nx.type === "table" && nx.consumedBy === undefined
					&& (this.bilingualSectionNum(nx.block) || this.isCalloutTable(nx.block, norm)
						|| (lessonOn && this.bilingualLessonNum(nx.block) !== null))) break;
			}
			// capture the activity NUMBER ("1A") from the first "Activity NX:"/"Ngohe NX:" the section carries
			// (the [H1] N.M keystone path only — a [H2] Lesson N box gets its resequenced number below)
			if (!openedByLesson && number === null && nx.block) { const an = this.reoActivityNumFromBlock(nx.block); if (an) number = an; }
			// a consumed widget bundle → ONE cv2 marker; the section IS a true activity (box it);
			// suppress the bundle (the bundle path skips it)
			if (nx.consumedBy !== undefined) {
				const b = bundles && bundles[nx.consumedBy];
				if (b && !b._emitted) {
					b._emitted = true;
					inner.push(`<div class="cv2-interactive bilingual-unbuilt">\n${TablesAndGrids.contentTable(nx.block, run, true, norm)}\n</div>`);
					hasWidget = true;
				}
				continue;   // a member of an already-emitted bundle renders nothing here
			}
			if (nx.type === "table") {
				// An audioImage PHONICS GRID is rendered, but does NOT by itself make the
				// section into a boxed "activity" — the human build leaves an
				// audioImage-only or prose-only section as a BARE col-md-8 column with no
				// box around it. This is the SELECTIVE boxing rule: only a section that
				// genuinely holds a real interactive widget gets the div.activity treatment.
				const aimg = this.bilingualAudioImage(nx.block);
				if (aimg) { inner.push(aimg); continue; }
				// The [H2] Lesson N opener style skips its own title row here (that row was
				// already rendered separately, as the bare <h2> built above).
				const r = this.bilingualRows(nx.block, run, (j === i) ? openerFromRow : undefined, norm);
				if (r.length) {
					inner.push(...r);
					// a content table that REFERENCES an interactive inline → keep a cv2 marker AND box
					// the section (the human builds that widget inside the div.activity).
					if (guardOn && this.embeddedWidgetRe.test(nx.block.text || "")) {
						inner.push(`<div class="cv2-interactive bilingual-unbuilt">\n<p style="color: #d9480f; font-weight: bold">⚙ INTERACTIVE (un-built) — bilingual widget embedded in the content table; develop from the source table.</p>\n</div>`);
						hasWidget = true;
					}
					continue;
				}
				// a non-bilingual DATA table (audio-item list, word bank) → a cv2 marker; on its own it does
				// NOT box the section (it is a widget's data, normally captured with its bundle).
				inner.push(`<div class="cv2-interactive bilingual-unbuilt">\n${TablesAndGrids.contentTable(nx.block, run, true, norm)}\n</div>`);
				continue;
			}
			if (nx.type === "black") {
				if (String(nx.text || "").trim())
					for (const h of ListsAndRuns.renderBlackText(nx.text, run, nx.block?.links)) inner.push(h);
				continue;
			}
			if (nx.type === "tag") {
				// an interior tag (e.g. an [Activity: Embedded] X opener the scanner did NOT consume):
				// suppress the marker (it would leak) but keep its trailing black prose.
				if (String(nx.blackAfter || "").trim())
					for (const h of ListsAndRuns.renderBlackText(nx.blackAfter, run, nx.block?.links)) inner.push(h);
				continue;
			}
			break;   // an unrecognised item ends the section (never silently swallow it)
		}
		if (!inner.length && !titleHtml) return null;
		// belt-and-braces: mark every absorbed NON-consumed item handled (the caller also jumps i)
		for (let k = i; k < j; k++) if (bodyItems[k] && bodyItems[k].consumedBy === undefined) bodyItems[k]._consumed = true;
		const innerHtml = inner.join("\n");
		// A [H2] Lesson N box RESEQUENCES its activity letter (A, B, C… — see
		// reoLessonLetter above) within each lesson, discarding the writer's own
		// irregular letters; only assigned when a box is actually going to be emitted.
		if (openedByLesson && hasWidget) number = `${lessonNum}${this.reoLessonLetter(run, lessonNum)}`;
		// SELECTIVE boxing: a section that holds a real interactive widget becomes the
		// human's div.activity box (carrying its number= attribute when the WT gave it
		// an "Activity NX:" number); a section that's just prose/media becomes a bare
		// grouped col-md-8 column with no box at all, matching how the human build
		// leaves a meaningful share of lesson sections un-boxed.
		let body = "";
		if (inner.length) body = hasWidget
			? `<div class="row">\n<div class="col-md-8 col-12">\n<div class="activity interactive"${number ? ` number="${number}"` : ""}>\n<div class="row">\n<div class="col-12">\n${innerHtml}\n</div>\n</div>\n</div>\n</div>\n</div>`
			: `<div class="row">\n<div class="col-md-8 col-12">\n${innerHtml}\n</div>\n</div>`;
		// A [H2] Lesson N opener prepends its bare-col <h2> title BEFORE the box (or
		// bare body) that was just built.
		const html = titleHtml ? (body ? `${titleHtml}\n${body}` : titleHtml) : body;
		return { html, next: j };
	};

	/**
	 * Builds the bilingual audioImage PHONICS GRID — one of the most
	 * common bilingual widget shapes: a table laid out as a
	 * column-aligned IMAGE row directly above an AUDIO row
	 * (`[Item N] [Image] {desc}` over `[Item N] [Audio] {name}`, one
	 * column per letter/sound being taught).
	 *
	 * WHAT IT DOES: builds the human's
	 * `<div class="row"> <div class="col paddingR"> <div class="audioImage">
	 * <div id="{audio name}" class="audioImageOption">
	 * <img class="img-fluid" src="images/{desc}.jpg" alt="{desc}"> …`
	 * structure, one column per image/audio pair. Note there is
	 * deliberately NO `<audio>` element in the output — the image's `id`
	 * attribute IS the audio clip name, and the site's own front-end
	 * JavaScript uses that id to play the matching sound when the image is
	 * clicked.
	 *
	 * WHY IT'S CONSERVATIVE: only builds when it finds an unambiguous IMAGE
	 * row immediately followed by an AUDIO row with at least 2 columns —
	 * the exact image file extension and column widths are left to
	 * whatever the site's own styling does with them (not something this
	 * converter can know), but the overall STRUCTURE is safely derivable
	 * from the table shape alone. Data dual_language.audio_image; env
	 * toggle AUDIOIMG_OFF.
	 *
	 * @param {Object} block - a table block
	 * @returns {string|null} the rendered grid HTML, or null when the table isn't a clean image-over-audio grid (falls back to the generic cv2 placeholder elsewhere)
	 */
	static bilingualAudioImage(block) {
		const cfg = DataService.Data.EmitTemplates?.elements?.dual_language?.audio_image;
		if (!cfg || cfg.enabled === false
			|| (typeof process !== "undefined" && process.env && process.env.AUDIOIMG_OFF)) return null;
		const rows = block?.rows ?? [];
		if (rows.length < 2) return null;
		const isImg = (c) => /\[\s*(?:image|photo)\s*\]/i.test(String(c ?? ""));
		const isAud = (c) => /\[\s*audio[^\]]*\]/i.test(String(c ?? ""));
		const clean = (c) => String(c ?? "")
			.replace(/\u{1f534}|\[\/?RED TEXT\]/gu, "")
			.replace(/\[\s*item[^\]]*\]/ig, "")
			.replace(/\[\s*(?:image|photo|audio[^\]]*)\s*\]/ig, "")
			.replace(/\*/g, "").replace(/\s+/g, " ").trim();
		// the FIRST image row, then the NEXT audio row (column-aligned phonics grid)
		let imgRow = -1, audRow = -1;
		for (let r = 0; r < rows.length; r++) {
			const cells = Array.isArray(rows[r]) ? rows[r] : [];
			const imgN = cells.filter(isImg).length, audN = cells.filter(isAud).length;
			if (imgRow < 0 && imgN >= 2 && imgN >= audN) imgRow = r;
			else if (imgRow >= 0 && audRow < 0 && audN >= 2) { audRow = r; break; }
		}
		if (imgRow < 0 || audRow < 0) return null;
		const imgs = rows[imgRow], auds = rows[audRow];
		const n = Math.min(imgs.length, auds.length);
		const cols = [];
		for (let i = 0; i < n; i++) {
			if (!isImg(imgs[i]) && !isAud(auds[i])) continue;
			const desc = clean(imgs[i]), name = clean(auds[i]) || desc;
			cols.push(`<div class="col paddingR">\n<div class="audioImage">\n<div id="${Utils.EscapeHtml(name)}" class="audioImageOption">\n<img class="img-fluid" src="images/${Utils.EscapeHtml(desc)}.jpg" alt="${Utils.EscapeHtml(desc)}">\n</div>\n</div>\n</div>`);
		}
		if (cols.length < 2) return null;
		return `<div class="row">\n${cols.join("\n")}\n</div>`;
	};

	/**
	 * Builds a BILINGUAL CALLOUT CONTAINER. When a bilingual table's very
	 * first cell carries a callout tag — `[Alert]` / `[Alert Solid]`
	 * (renders as the "important" style) / `[Whakataukī]` / `[Supervisors
	 * note]` / `[Wananga]` / `[Quote]`, matched against the shared
	 * Emit_Templates.callouts catalogue used everywhere else in the
	 * converter — this builds the matching human container (`div.whakatauki`
	 * / `div.alert` / `div.alert.solid` / `row.supervisor` / …) with its
	 * rows unfolded reo/eng INSIDE it, instead of falling back to the
	 * generic cv2-interactive placeholder box. (The multi-item ACTIVITY
	 * container that wraps several tables/widgets together is a different,
	 * separate concern — see bilingualActivity below.)
	 *
	 * @param {Object} block - a table block whose first cell may open a callout
	 * @param {ConversionRun} run - the current run
	 * @param {TagNormaliser} norm - resolves the leading `[Tag]` to find out which callout it is
	 * @returns {string|null} the rendered container HTML, or null when the first cell doesn't lead with a recognised callout tag
	 */
	static bilingualContainer(block, run, norm) {
		const cfg = DataService.Data.EmitTemplates.elements?.dual_language;
		if (!cfg || cfg.enabled === false) return null;
		const rows = block.rows ?? [];
		if (!rows.length || !Array.isArray(rows[0])) return null;
		const callouts = DataService.Data.EmitTemplates.callouts || {};
		let canon = null, def = null;
		for (const c of [rows[0][0], rows[0][1]]) {
			const m = String(c ?? "").match(/^\s*\[([^\]]+)\]/);
			if (!m) continue;
			let t = null; try { t = norm.Parse(`[${m[1]}]`)?.primary?.tag ?? null; } catch { t = null; }
			if (t && callouts[t] && t !== "side alert") { canon = t; def = callouts[t]; break; }
		}
		if (!def || !def.open) return null;
		const out = [];
		for (let r = 0; r < rows.length; r++) {
			const R = this.bilingualSplit(rows[r][1], run, norm), E = this.bilingualSplit(rows[r][0], run, norm);
			for (const p of R.text) out.push(this.langAttr(p, "reo"));
			for (const p of E.text) out.push(this.langAttr(p, "eng"));
			for (const m of (R.media.length ? R.media : E.media)) out.push(m);
		}
		if (!out.length) return null;
		const open = Utils.FillTemplate(def.open, { modifiers: "" }), inner = out.join("\n"), close = def.close;
		if (def.own_row) return `${open}\n${inner}\n${close}`;                                   // supervisor
		if (canon === "whakatauki" || canon === "quote" || canon === "wananga")                  // bare box, col-md-12
			return `<div class="row">\n<div class="col-md-12 col-12">\n${open}\n${inner}\n${close}\n</div>\n</div>`;
		return `<div class="row">\n<div class="col-md-8 col-12">\n${open}\n<div class="row">\n<div class="col-12">\n${inner}\n</div>\n</div>\n${close}\n</div>\n</div>`;  // alert / important
	};

	// --- Bilingual ACTIVITY grouping helpers ---
	// Matches the standalone "[Activity: Embedded]" / "[Activity Embedded]" marker some
	// writers use to flag a table as the start of a bilingual activity.
	static activityMarkerRe = /^\s*\[\s*activity[:\s]*embedded\s*\]/i;
	// Matches a standalone "Activity NA:" / "Ngohe NA:" label (e.g. "Activity 1A:") on a
	// line of its own — the same shape actLabelRe (above) matches, kept separate here
	// because this one is also used to extract the captured number, not just detect it.
	static activityNumRe = /^\s*(?:activity|ngohe)\s+([0-9]+[A-Za-z]?)\s*:?\s*$/i;

	/**
	 * Is this table's header row an "English | Māori" bilingual content
	 * table header?
	 *
	 * @param {Object} block - a table block
	 * @returns {boolean} true when row 0 folds to English in column 1 and Māori in column 2
	 */
	static bilingualHeader(block) {
		const cfg = DataService.Data.EmitTemplates.elements?.dual_language;
		const rows = block?.rows ?? [];
		if (!rows.length || !Array.isArray(rows[0]) || rows[0].length < 2) return false;
		const fold = (s) => Utils.Fold(String(s ?? "")).trim();
		return new RegExp(cfg?.header_english || "english", "i").test(fold(rows[0][0]))
			&& new RegExp(cfg?.header_maori || "māori|maori|te reo", "i").test(fold(rows[0][1]));
	};

	/**
	 * Does this table carry an `[Activity Embedded]` marker, or an
	 * "Activity NA:" / "Ngohe NA:" row, anywhere in it?
	 *
	 * @param {Object} block - a table block
	 * @returns {boolean} true when any cell matches either pattern
	 */
	static isActivityMarker(block) {
		for (const row of (block?.rows ?? [])) for (const c of row) {
			const s = String(c ?? "");
			if (this.activityMarkerRe.test(s) || this.activityNumRe.test(s.trim())) return true;
		}
		return false;
	};

	/**
	 * Does this table's first cell lead with a recognised callout tag?
	 * Used by bilingualSection (above) to know when a table should STOP a
	 * section gather and get its own callout box instead of being folded
	 * into the section.
	 *
	 * @param {Object} block - a table block
	 * @param {TagNormaliser} norm - resolves the leading `[Tag]` to a canonical tag
	 * @returns {boolean} true when the first cell opens with a callout tag (other than "side alert", which is handled elsewhere)
	 */
	static isCalloutTable(block, norm) {
		const callouts = DataService.Data.EmitTemplates.callouts || {};
		for (const c of [block?.rows?.[0]?.[0], block?.rows?.[0]?.[1]]) {
			const m = String(c ?? "").match(/^\s*\[([^\]]+)\]/);
			if (!m) continue;
			let t = null; try { t = norm.Parse(`[${m[1]}]`)?.primary?.tag ?? null; } catch { t = null; }
			if (t && callouts[t] && t !== "side alert") return true;
		}
		return false;
	};

	/**
	 * Builds a BILINGUAL ACTIVITY container from a set of blocks the
	 * caller has already gathered together — the `[Activity Embedded]`
	 * marker table plus whatever widget-spec / content tables followed it.
	 *
	 * WHAT IT DOES: produces
	 * `<div class="activity interactive" number="NA"><div class="row">
	 * <div class="col-12"> … </div></div></div>`, where the inner content
	 * comes from each gathered block in turn: an English|Māori bilingual
	 * table or the marker table itself gets unfolded reo/eng (with its
	 * marker/number/header rows stripped out first, since those are
	 * structural, not content); a widget-spec table (data for an
	 * interactive widget the converter doesn't build yet) becomes a
	 * cv2-interactive placeholder instead. The activity's number=
	 * attribute is read from whichever block carries an "Activity NA:"
	 * row.
	 *
	 * @param {Object[]} blocks - the gathered blocks that make up this activity
	 * @param {ConversionRun} run - the current run
	 * @param {TagNormaliser} norm - resolves `[Tag]` markers found in cells
	 * @returns {string|null} the rendered activity container HTML, or null when there's nothing to render
	 */
	static bilingualActivity(blocks, run, norm) {
		const cfg = DataService.Data.EmitTemplates.elements?.dual_language;
		if (!cfg || cfg.enabled === false || !blocks || !blocks.length) return null;
		const mRe = this.activityMarkerRe, nRe = this.activityNumRe;
		let number = "";
		const out = [];
		for (const block of blocks) {
			const rows = block?.rows ?? [];
			for (const row of rows) for (const c of row) { const nm = String(c ?? "").match(nRe); if (nm && !number) number = nm[1]; }
			if (this.bilingualHeader(block) || this.isActivityMarker(block)) {
				for (const row of rows) {
					const c0 = String(row[0] ?? ""), c1 = String(row[1] ?? "");
					if (nRe.test(c0.trim()) || /^english$/i.test(Utils.Fold(c0).trim())) continue;
					const R = this.bilingualSplit(c1.replace(mRe, "").replace(/^\s*\[[^\]]*\]\s*$/, ""), run, norm);
					const E = this.bilingualSplit(c0.replace(mRe, "").replace(/^\s*\[[^\]]*\]\s*$/, ""), run, norm);
					for (const p of R.text) out.push(this.langAttr(p, "reo"));
					for (const p of E.text) out.push(this.langAttr(p, "eng"));
					for (const m of (R.media.length ? R.media : E.media)) out.push(m);
				}
			} else {
				out.push(`<div class="cv2-interactive bilingual-unbuilt">\n${TablesAndGrids.contentTable(block, run, true, norm)}\n</div>`);
			}
		}
		if (!out.length) return null;
		const num = number ? ` number="${number}"` : "";
		return `<div class="activity interactive"${num}>\n<div class="row">\n<div class="col-12">\n${out.join("\n")}\n</div>\n</div>\n</div>`;
	};

	/**
	 * Splits ONE bilingual table cell (which may mix ordinary text with
	 * `[Item]`/`[Image]`/`[Audio]`/`[video]` markers) into two separate
	 * output streams: rendered TEXT elements and rendered MEDIA embeds.
	 *
	 * HOW: text goes through ListsAndRuns.renderBlackText (the same
	 * shared headings/body/list rendering logic used everywhere else, so
	 * a `[H#]`/`[Body]` tag inside the cell is handled identically to how
	 * it would be outside a bilingual table); media markers become their
	 * placeholder embeds directly, specifically so an `[Item]`/`[Audio]`/
	 * `[video]` tag can never leak into the page as raw, unrendered text.
	 *
	 * @param {string} cell - the raw cell text (English or Māori)
	 * @param {ConversionRun} run - the current run
	 * @param {TagNormaliser} norm - resolves any `[Tag]` markers found in the cell
	 * @returns {{text: string[], media: string[]}} the rendered text elements and media embeds, each in source order
	 */
	static bilingualSplit(cell, run, norm) {
		const text = [], media = [], buf = [];
		const flush = () => { if (buf.length) { for (const h of ListsAndRuns.renderBlackText(buf.join("\n"), run)) text.push(h); buf.length = 0; } };
		for (const part of TablesAndGrids.cellParts(cell)) {
			const low = part.toLowerCase();
			const m = part.match(/^\[([^\]]+)\]\s*([\s\S]*)$/);
			let canon = null, rest = part;
			if (m) { try { canon = norm.Parse(`[${m[1]}]`)?.primary?.tag ?? null; } catch { canon = null; } rest = m[2]; }
			if (/\[\s*(?:item[^\]]*\]\s*\[\s*)?(?:image|photo)\s*\]/.test(low)) {
				flush(); for (const x of TablesAndGrids.cellImage(part, run)) media.push(x);
			} else if (/\[\s*(?:item[^\]]*\]\s*\[\s*)?audio[^\]]*\]/.test(low)) {
				flush(); media.push('<audio preload="none" class="audioPlayer icon"></audio>');
			} else if (/\[\s*(?:item[^\]]*\]\s*\[\s*)?video[^\]]*\]/.test(low)) {
				flush(); media.push('<div class="videoSection ratio ratio-16x9">\n<iframe></iframe>\n</div>');
			} else if (canon && /^(?:h[1-6]|heading|activity heading)$/.test(canon)) {
				flush();
				const digit = /^h\d$/.test(canon) ? parseInt(canon[1], 10) : 2;
				const lvl = Math.min(Math.max(digit, 2), 5);
				const t = (norm.RenderText(part) || rest.trim() || "").replace(/\*/g, "").trim();
				if (t) text.push(`<h${lvl}>${ListsAndRuns.inlineMarkup(t)}</h${lvl}>`);
			} else {
				// Strip every leading non-media [tag] so none of them can leak into the
				// rendered text — not just the FIRST one, but a whole run of CONSECUTIVE
				// leading tags. This matters because, when the over-capture guard lets a
				// content table unfold as ordinary bilingual prose, the writer's own inline
				// widget reference (e.g. "[Interactive] [Flipcard]/[Carousel]", usually its
				// own " / "-separated part of the cell) would otherwise leak its SECOND tag
				// even after the cell's normal leading prefix tag was already stripped. So
				// the cell's own prefix tag AND any inline widget-reference tag are both
				// stripped here, one after another; the surrounding prose text itself is
				// always kept. (A widget tag that shows up mid-sentence rather than at the
				// very start is handled separately, by ListsAndRuns.renderBlackText.)
				let t = canon ? rest : part;
				let mm;
				while ((mm = t.match(/^\s*\[[^\]]+\]\s*/))) t = t.slice(mm[0].length);
				buf.push(t);
			}
		}
		flush();
		return { text, media };
	};

	/**
	 * Stamps a `reo` or `eng` boolean attribute onto the FIRST (outermost)
	 * tag of an already-rendered HTML element string, so the site's
	 * front-end can tell which language a given element belongs to.
	 *
	 * USAGE: BilingualBuilder.langAttr("<p>Kia ora</p>", "reo") -> "<p reo>Kia ora</p>"
	 *
	 * @param {string} html - a rendered element, e.g. "<p>...</p>"
	 * @param {string} lang - "reo" or "eng"
	 * @returns {string} the same HTML with the language attribute added to its opening tag
	 */
	static langAttr(html, lang) {
		return String(html).replace(/^(\s*<)([a-zA-Z][a-zA-Z0-9]*)(?=[\s>])/, `$1$2 ${lang}`);
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { BilingualBuilder };
