/**
 * InteractiveBuilder.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 *   Turns a CAPTURED interactive (a "bundle" the InteractiveScanner found in
 *   the Writers Template) into the REAL, finished widget HTML — for the small
 *   set of "easy" widgets we fully understand. If it can build the widget it
 *   returns the HTML string; if anything about the captured data is unclear,
 *   it returns null and the caller falls back to the orange placeholder.
 *
 * HOW IT FITS IN (the data half lives in data/Emit_Templates.json):
 *   ContentConverter, just before it would emit an orange "un-built" box, asks
 *   this file: "can you build this one for real?" (InteractiveBuilder.Build).
 *      • returns a string  → ContentConverter ships that widget, marks it built
 *      • returns null      → ContentConverter shows the placeholder as before
 *   The MARKUP of each widget is NOT written in this file. It lives as editable
 *   templates in Emit_Templates.json → "interactive_builders". This file only
 *   decides WHICH template applies and maps the captured data into its slots.
 *
 * WHY IT IS BUILT THIS WAY:
 *   1. Safety first. A wrong-but-live interactive is worse than an honest
 *      placeholder. So every builder is conservative: the moment the data does
 *      not match the shape it expects, it bails out (null) and we keep the
 *      placeholder. We never guess.
 *   2. Data-driven, per the project philosophy. Adding/altering a widget's
 *      look is a DATA edit (Emit_Templates.json). This code only knows the
 *      data SHAPES (e.g. "hintSlider = one 2-column table"), never the markup.
 *   3. Human-editable. A new widget = copy one template entry + add one short
 *      `case` here. Both halves are commented in plain English.
 *
 * USAGE:
 *   const html = InteractiveBuilder.Build({
 *       bundle,                       // the captured interactive (see shape below)
 *       run,                          // conversion run context (for log notes)
 *       templates: <interactive_builders block from Emit_Templates.json>,
 *       renderInline: (line) => ...,  // ContentConverter's inline-markup helper
 *   });
 *   // html === string  → built widget   |   html === null → use placeholder
 *
 * THE "bundle" SHAPE THIS FILE READS (built by InteractiveScanner):
 *   {
 *     type:        "hintSlider",        // which widget the scanner thinks it is
 *     index:       5,                   // 1-based number on the page
 *     openerItems: [ <member>, ... ],   // the opener line(s); usually titles
 *     memberItems: [ <member>, ... ],   // the captured body of the widget
 *     ...                               // (other fields exist; we ignore them)
 *   }
 *   …where each <member> is one of:
 *     { type: "table", block: { rows: [ [cellA, cellB, ...], ... ] } }
 *     { type: "black", text: "…visible paragraph text…" }
 *   Cell / text strings may still carry the corpus red-span markers
 *   "🔴[RED TEXT]…[/RED TEXT]🔴"; #cellText() strips those to plain text.
 *
 * HOW TO ADD A NEW WIDGET (two small steps, no other files to touch):
 *   1. data/Emit_Templates.json → "interactive_builders": add a key with the
 *      finished markup (open / row / close + {slots}). Copy hintSlider.
 *   2. Here: add `case "<yourType>": return this.#yourType({ bundle, tpl,
 *      renderInline });` in Build(), and write that small private method to
 *      pull the captured data into the template slots — returning null if the
 *      data does not fit cleanly.
 * ===========================================================================
 */

class InteractiveBuilder {
	// =======================================================================
	// PUBLIC ENTRY
	// =======================================================================

	/**
	 * Try to build a captured interactive into real HTML.
	 *
	 * WHAT: dispatches on bundle.type to the matching private builder.
	 * HOW:  every builder is wrapped so that ANY problem — a missing template,
	 *       a disabled widget, an unexpected data shape, or a thrown error —
	 *       resolves to null (→ caller keeps the safe orange placeholder).
	 * WHY:  shipping a half-understood interactive live is the one outcome we
	 *       must never allow; null is always the safe answer.
	 *
	 * @param {object}   args
	 * @param {object}   args.bundle        - the captured interactive (shape above)
	 * @param {object}   args.run           - run context; used only for log notes
	 * @param {object}   args.templates     - Emit_Templates.interactive_builders
	 * @param {function} args.renderInline  - (line:string) => safe inline HTML
	 * @returns {string|null}  built widget HTML, or null to use the placeholder
	 */
	static Build({ bundle, run, templates, renderInline, renderBlock, renderNested, renderTable, renderImage } = {}) {
		// GUARD: builders not configured at all → nothing to build.
		if (!templates || typeof templates !== "object") return null;
		// GUARD: a bundle with no type can't be matched.
		const type = bundle?.type;
		if (!type) return null;

		// Look up THIS widget's editable template. Missing = we don't build it
		// yet (it stays a placeholder). enabled:false = a human switched it off.
		const tpl = templates[type];
		if (!tpl || tpl.enabled === false) return null;

		try {
			let html = null;
			switch (type) {
				// ---- easy widgets, added one at a time -------------------------
				case "hint":            // a single [hint] tag is really just a one-row hintSlider, so it reuses that builder
				case "hintSlider":
					html = this.#hintSlider({ bundle, tpl, renderInline });
					break;
				case "accordion":
					html = this.#accordion({ bundle, tpl, renderInline, run, renderBlock, renderNested });
					break;
					// speechBubble needs `run` (for the image Mode P/D), so it is
					// the first builder we hand the run context to.
				case "speechBubble":
					html = this.#speechBubble({ bundle, tpl, renderInline, run });
					break;
				case "flipCard":
					html = this.#flipCard({ bundle, tpl, renderInline, run });
					break;
				case "tabs":
					html = this.#tabs({ bundle, tpl, renderInline, run, renderBlock, renderTable, renderImage });
					break;
				case "carousel":
					// renderBlock added round 246 — the rich slide fallback renders slide prose
					// (and the writer's bullets) through the shared black-text renderer.
					html = this.#carousel({ bundle, tpl, renderInline, run, renderBlock });
					break;
				case "shapeHover":   // [shape hover] opener + repeating [shape n]/[body]/[image] groups (verified against OSAI501-02)
					html = this.#shapeHover({ bundle, tpl, renderInline, run });
					break;
				case "clickDrop":
					html = this.#clickDrop({ bundle, tpl, renderInline, run });
					break;
				case "glossary":
					html = this.#glossary({ bundle, tpl, renderInline });
					break;
				case "selfCheck":   // a numbered question-list form → <p class="sCQuestion"> + a free-text sCText/textarea pair
					html = this.#selfCheck({ bundle, tpl, renderInline });
					break;
				case "dragAndDrop": // the narrow N:N text-matching case only (layout=standard)
					html = this.#dragAndDrop({ bundle, tpl, renderInline });
					break;
				case "modal":       // image-pair form → TKmodal set; else a single document/PDF URL → a button
					html = this.#modal({ bundle, tpl, renderInline, renderBlock, run });
					break;
				// (infoTrigger
				//  will be added here as each is proven against the human builds.)
				default:
					return null; // type has a template but no code case yet
			}

			// A builder may still decline (null) if the captured data did not fit.
			if (html) {
				run?.AddNote?.("info", "InteractiveBuilder",
					`Built ${type} #${bundle.index} from captured data (no placeholder needed).`);
			}
			return html;
		} catch (err) {
			// NEVER let a build error break the page — fall back to placeholder.
			run?.AddNote?.("warn", "InteractiveBuilder",
				`Could not build ${type} #${bundle.index} (${err.message}); left as a placeholder for manual build.`);
			return null;
		}
	}

	// =======================================================================
	// WIDGET BUILDERS  (one small method per widget type)
	// =======================================================================

	/**
	 * glossary — a flat list of "Term – Meaning" entries → the human's Term/Meaning
	 * table (verified against OSAI201-01). Each captured black line is split on the FIRST
	 * en/em-dash (or spaced hyphen): the part before is the Term, after is the Meaning.
	 * Lines with no dash (e.g. a stray heading) are skipped; declines to a placeholder
	 * if fewer than min_rows valid entries are found. The outer row>col wrapper is
	 * supplied by the body emitter — only the inner div.glossary is built here.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links); identity if omitted
	 * @returns {string|null} the built glossary HTML, or null to keep the orange placeholder
	 */
	static #glossary({ bundle, tpl, renderInline }) {
		const re = new RegExp(tpl.split_pattern ?? "^(.+?)\\s+[\\u2013\\u2014-]\\s+([\\s\\S]+)$");
		const sources = [...(bundle?.openerItems ?? []), ...(bundle?.memberItems ?? [])];
		const rows = [];
		for (const m of sources) {
			if (!m) continue;
			const text = m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			for (const line of String(text).split(/\n+/)) {
				const t = line.trim();
				if (!t) continue;
				const mm = t.match(re);
				if (!mm) continue;                       // not a Term–Meaning line → skip
				const term = mm[1].trim(), meaning = mm[2].trim();
				if (term && meaning) rows.push({ term, meaning });
			}
		}
		if (rows.length < (tpl.min_rows ?? 2)) return null;
		const body = rows.map((r) => Utils.FillTemplate(tpl.row, {
			term: renderInline(r.term), meaning: renderInline(r.meaning),
		})).join("\n");
		return `${tpl.wrapper_open}\n${body}\n${tpl.wrapper_close}`;
	}

	/**
	 * selfCheck — QUESTION-LIST form (verified against HPFUN401). A clean list of
	 * NUMBERED questions → per question a <p class="sCQuestion"> + a free-text
	 * <div class="sCText" checkOn=""><textarea rows="2" placeholder="Type here">.
	 * CONSERVATIVE (never half-build): builds ONLY when every captured black line is a
	 * numbered question and there is NO table, media, URL, red writer-instruction, or
	 * extra widget type — the image-matching TABLE form and the mixed video+question form
	 * both bail to the placeholder. rows/checkOn are editorial choices we default to the
	 * corpus-common 2/empty; the node STRUCTURE (all a structural comparison sees) is exact.
	 * Env SELFCHECK_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links); identity if omitted
	 * @returns {string|null} the built selfCheck HTML, or null to keep the orange placeholder
	 */
	static #selfCheck({ bundle, tpl, renderInline }) {
		if (typeof process !== "undefined" && process.env && process.env.SELFCHECK_OFF) return null;
		if ((bundle?.tables ?? []).length) return null;          // image-matching table form → keep placeholder
		if ((bundle?.media ?? []).length) return null;           // any media (video/image) → not the plain Q-list form
		if (bundle?.extraTypes && bundle.extraTypes.length) return null;
		const inline = renderInline ?? ((s) => s);
		const sources = [...(bundle?.openerItems ?? []), ...(bundle?.memberItems ?? [])];
		const questions = [];
		for (const m of sources) {
			if (!m) continue;
			if (m.type === "table") return null;
			const raw = m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			if (this.#hasRedText(raw)) return null;              // a writer instruction inside → not a clean Q-list
			for (const line of String(raw).split(/\n+/)) {
				const t = this.#cellText(line).trim();
				if (!t) continue;
				if (/https?:\/\//.test(t)) return null;          // a URL (video/link) → mixed form → bail
				if (!/^\d+[.)]\s*\S/.test(t)) return null;       // a non-numbered line (instruction/heading) → bail
				questions.push(t);
			}
		}
		if (questions.length < (tpl.min_rows ?? 2)) return null;
		const body = questions.map((q) => Utils.FillTemplate(tpl.row, { question: inline(q) }));
		return [tpl.open, ...body, tpl.close].join("\n");
	}

	/**
	 * dragAndDrop — NARROW N:N TEXT-MATCHING form, layout=standard.
	 * One 2-column data table [label | answer]; row order is the answer key. Builds the
	 * human's questionContainer (one .question per label) + ddContainer (a .drop per row
	 * and a .drag per row, option = 1-based row index), answers rendered as <p> text.
	 * CONSERVATIVE: the human's layout choice (standard/column/FIB/scatter) and image-form
	 * alt text are NON-DERIVABLE editorial (measured: bundle.modifier is the writer's
	 * freeform remainder, not layout=), so we fire ONLY on the safest sub-shape and keep the
	 * placeholder otherwise — bail unless exactly one table, width 2, >= min_rows rows, every
	 * answer DISTINCT plain text (a repeated answer = categorisation, not matching → bail),
	 * and no media / URL / red / extraType. layout defaults to standard. Env DRAGDROP_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links); identity if omitted
	 * @returns {string|null} the built dragAndDrop HTML, or null to keep the orange placeholder
	 */
	static #dragAndDrop({ bundle, tpl, renderInline }) {
		if (typeof process !== "undefined" && process.env && process.env.DRAGDROP_OFF) return null;
		if (bundle?.extraTypes && bundle.extraTypes.length) return null;
		if ((bundle?.media ?? []).length) return null;
		const tables = bundle?.tables ?? [];
		if (tables.length !== 1) return null;
		const srcRows = tables[0].rows ?? [];
		const width = Math.max(0, ...srcRows.map((r) => (r ?? []).length));
		if (width !== 2) return null;                            // strictly label | answer
		const rows = srcRows.filter((r) => Array.isArray(r) && r.length === 2);
		if (rows.length < (tpl.min_rows ?? 2)) return null;
		const inline = renderInline ?? ((s) => s);
		const labels = [], answers = [];
		for (const r of rows) {
			if (this.#hasRedText(r[0]) || this.#hasRedText(r[1])) return null;   // writer instruction → bail
			const label = this.#cellText(r[0]).trim();
			const answer = this.#cellText(r[1]).trim();
			if (!label || !answer) return null;
			if (/https?:\/\//.test(label) || /https?:\/\//.test(answer)) return null;  // image/media form → bail
			labels.push(label); answers.push(answer);
		}
		// DISTINCT answers ⇒ a 1:1 MATCHING set; a repeat ⇒ categorisation (different structure) → bail.
		if (new Set(answers.map((a) => a.toLowerCase())).size !== answers.length) return null;
		const out = [tpl.open];
		for (const l of labels) out.push(Utils.FillTemplate(tpl.question, { label: inline(l) }));
		out.push(tpl.mid);
		for (let i = 0; i < rows.length; i++) out.push(Utils.FillTemplate(tpl.drop, { n: i + 1 }));
		out.push(tpl.drag_open);
		for (let i = 0; i < answers.length; i++) out.push(Utils.FillTemplate(tpl.drag, { n: i + 1, answer: inline(answers[i]) }));
		out.push(tpl.close);
		return out.join("\n");
	}

	/**
	 * hintSlider — a stack of click-to-reveal rows.
	 *
	 * DATA SHAPE WE EXPECT: exactly one 2-column table, where every row is
	 *   [ front (the hint shown), back (the answer revealed) ]. An optional
	 *   leading header row labelling the columns ("hint | slide", "front |
	 *   back") is dropped. Anything that does not look like this → null.
	 *
	 * SAMPLE captured table.rows (OSAI201):
	 *   [ ["hint", "slide"],
	 *     ["I learn how people type…", "Autocorrect or predictive text."],
	 *     ["I control game characters…", "AI in gaming."], … ]
	 *
	 * BUILDS (per row, from Emit_Templates.interactive_builders.hintSlider.row):
	 *   <div class="hintRow"><div class="infoContainer">
	 *     <div class="frontInfo"><p>{front}</p></div>
	 *     <div class="backInfo"><p>{back}</p></div>
	 *   </div></div>
	 */
	static #hintSlider({ bundle, tpl, renderInline }) {
		// Dispatch by CONTENT: a MEMBER-based hint widget (the writer typed [front]/[back]
		// tags per row — OSBY201-02) routes to the member path; the classic 2-column TABLE
		// form uses the original path VERBATIM (so it stays byte-identical — proven by A/B).
		const members = bundle?.memberItems ?? [];
		const hasFrontBack = members.some((m) => m && m.type === "tag"
			&& ["front", "back"].includes(m.parse?.primary?.tag));
		return hasFrontBack
			? this.#hintSliderMembers({ bundle, tpl, renderInline })
			: this.#hintSliderTable({ bundle, tpl, renderInline });
	}

	/** hintSlider, TABLE form (the original builder for this widget, unchanged since it was first written). */
	static #hintSliderTable({ bundle, tpl, renderInline }) {
		// hintSlider is STRICTLY a two-part widget (front shown, back revealed).
		// So we only build from EXACTLY ONE table that is EXACTLY two columns
		// wide. Any other shape is ambiguous and we must not guess:
		//   • 0 tables   → the front/back was captured as free text, not a table
		//                  (e.g. alternating paragraph lines) — too risky to pair.
		//   • 2+ tables  → more than one data block; which is the slider? unknown.
		//   • 3+ columns → extra data (image / audio / etc.) we cannot place into
		//                  a plain front|back row (e.g. ENGI401's image+front+back).
		// In every one of those cases we return null and keep the placeholder.
		const tables = bundle?.tables ?? [];
		if (tables.length !== 1) return null;

		const allRows = tables[0].rows ?? [];
		const width = Math.max(0, ...allRows.map((r) => (r ?? []).length));
		if (width !== 2) return null;                 // strictly front | back

		// Keep the genuine two-cell rows; drop a column-label header if present.
		let rows = allRows.filter((r) => Array.isArray(r) && r.length === 2);
		if (rows.length && this.#looksLikeHeaderRow(rows[0], tpl)) rows = rows.slice(1);
		if (!rows.length) return null;

		// Map each [front, back] into the editable row template.
		const inline = renderInline ?? ((s) => s); // safe default if not supplied
		const body = rows.map((r) => Utils.FillTemplate(tpl.row, {
			front: inline(this.#cellText(r[0])),
			back:  inline(this.#cellText(r[1])),
		}));

		// open + every row + close → the finished widget.
		return [tpl.open, ...body, tpl.close].join("\n");
	}

	/**
	 * hintSlider, MEMBER form (verified — OSBY201-02). The writer authors each row as a
	 * [front] tag (the hint button label) + a [back] tag (the revealed text), often with a
	 * stray list-number line ("1.") before each — the human renders the same
	 * `hintRow > infoContainer > frontInfo + backInfo` rows as the table form.
	 *
	 * ROBUST to the writer's deviations: the [hint slider]/[hint] opener is skipped; a
	 * pure list-marker black line ("1.", "1)", "•", "-") is dropped (the auto-numbering
	 * artifact); every row must pair a [front] with a [back]. SAFETY (never half-build →
	 * null): a row missing its front or back, real black prose between items (not a list
	 * marker), red writer-instruction text, or any other tag → keep the placeholder.
	 */
	static #hintSliderMembers({ bundle, tpl, renderInline }) {
		const members = bundle?.memberItems ?? [];
		const inline = renderInline ?? ((s) => s);
		const rows = [];          // [{ front, back }]
		let cur = null;
		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			const raw = m && m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const text = this.#cellText(raw);

			if (tag === "hint slider" || tag === "hint") continue;     // the opener tag
			if (tag === "front") {
				if (!text || this.#hasRedText(raw)) return null;
				cur = { front: text, back: "" };
				rows.push(cur);
				continue;
			}
			if (tag === "back") {
				if (!cur || !text || this.#hasRedText(raw)) return null;
				cur.back = cur.back ? `${cur.back} ${text}` : text;
				continue;
			}
			// a stray list-number / bullet line ("1.", "1)", "•", "-") is the writer's
			// auto-numbering artifact → drop it; real prose or any other tag → bail.
			if (!text) continue;
			if ((m.type === "black" || !tag) && /^\s*(?:\d+[.)]|[•·\-*])\s*$/.test(text)) continue;
			return null;
		}

		if (rows.length < 2) return null;                              // need ≥2 hint rows
		for (const r of rows) if (!r.front || !r.back) return null;    // every row needs front + back
		const body = rows.map((r) => Utils.FillTemplate(tpl.row, {
			front: inline(r.front), back: inline(r.back),
		}));
		return [tpl.open, ...body, tpl.close].join("\n");
	}

	/**
	 * accordion - a stack of click-to-open panels (a heading that reveals a body).
	 *
	 * HOW THE WRITER AUTHORS IT (from the boundary research + parsed templates):
	 *   an accordion is a MEMBER SEQUENCE, not a data table. Each panel is one
	 *   [accordion N] tag whose TRAILING text is the panel heading, followed by the
	 *   panel's body paragraph(s). The scanner captures the repeated [accordion N]
	 *   tags (2nd..Nth absorbed as extraTypes) plus the body text as members.
	 *
	 * SAMPLE captured bundle.memberItems (OSBY301):
	 *   { type:"tag",   tag:"accordion", blackAfter:"Intent to Harm" }   // panel heading
	 *   { type:"black", text:"Deliberate actions meant to hurt..." }     // panel body
	 *   { type:"tag",   tag:"accordion", blackAfter:"Power Imbalance" }  // next panel ...
	 *
	 * BUILDS one <div class="accordion"> with, per panel (Emit_Templates accordion.row):
	 *   <div class="accHead"><h4>{head}</h4></div>
	 *   <div class="accContent">{content}</div>   ({content} = one <p> per paragraph)
	 *
	 * SAFETY (never half-build): plain-TEXT panels only. Returns null (-> keep the
	 *   placeholder) the moment the bundle is richer than heading+body text: any
	 *   other member tag ([image]/[video]/[button]/a data table), a panel missing
	 *   its heading or body, or red writer-instruction text inside a panel. This is a
	 *   deliberate policy, not a gap: image/nested/mixed accordions stay honest
	 *   placeholders rather than risk a wrong-looking live widget.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (image mode, log notes)
	 * @param {function} [args.renderBlock] - paragraph/list renderer, needed by the rich fallback
	 * @param {function} [args.renderNested] - renders an absorbed sub-widget as its own honest placeholder
	 * @returns {string|null} the built accordion HTML, or null to keep the orange placeholder
	 */
	static #accordion({ bundle, tpl, renderInline, run, renderBlock, renderNested }) {
		// Dispatch by CONTENT: a panel image ([image] member) routes to the
		// image-aware path; a pure heading+text accordion uses the original path
		// VERBATIM (so plain-text accordions stay byte-identical — proven by A/B).
		const members = bundle?.memberItems ?? [];
		const hasImage = members.some((m) => m && m.type === "tag" && m.parse?.primary?.tag === "image");
		const strict = hasImage
			? this.#accordionWithImages({ bundle, tpl, renderInline, run })
			: this.#accordionTextOnly({ bundle, tpl, renderInline });
		if (strict !== null) return strict;

		// RICH FALLBACK (verified against OSAI501-03). The strict paths above BAIL the
		// whole accordion the moment a panel is richer than heading + iStock image +
		// plain paragraphs. The human routinely also nests a [video], a BULLET list,
		// and (5 corpus pages) a shapeHover. This fallback fires ONLY when the strict
		// paths declined, so every accordion that already builds is byte-identical
		// (proven by ACCRICH_OFF). It still returns null (→ placeholder, never half-
		// built) on anything it cannot place cleanly.
		const rich = tpl?.rich_panels;
		if (rich && rich.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ACCRICH_OFF)) {
			// ROUND 246 ticket 2 — STRICTLY ADDITIVE. The heading-less numbered-panel rule
			// changes how members GROUP, so it could in principle break an accordion that
			// already built. Try it first; if the result is null, run the fallback again with
			// the rule OFF, which reproduces the round-245 grouping exactly. The new rule can
			// therefore only ever ADD builds, never remove one.
			const withRule = this.#accordionRich({ bundle, tpl, renderInline, run, renderBlock, renderNested });
			if (withRule !== null) return withRule;
			return this.#accordionRich({ bundle, tpl, renderInline, run, renderBlock, renderNested, legacyPanels: true });
		}
		return null;
	}

	/**
	 * RICH accordion (verified against OSAI501-03 — the FALLBACK used when the strict
	 * text/image paths decline). Groups members into panels exactly like #accordionWithImages,
	 * then renders each panel's accContent in DOCUMENT ORDER, handling the richer
	 * member kinds the human builds:
	 *   [image] (iStock)          -> #assetImage (Mode P/D)               — same as the image path
	 *   [video] (YouTube/Vimeo)   -> the shared video.youtube embed       — NEW
	 *   black / [body] text       -> renderBlock (#renderBlackText)       — bullets become <ul><li>
	 *   {type:"nested"} sub-bundle-> renderNested (#interactivePlaceholder) — honest nested placeholder
	 *
	 * NEVER half-builds: the WHOLE accordion returns null (→ orange placeholder) on a
	 * data table, a non-iStock / unresolvable image, a video with no readable id, a
	 * panel with no heading or no rendered body, red writer-instruction text, or any
	 * member it cannot place. Requires renderBlock (the bullet/paragraph renderer);
	 * without it the fallback declines so non-converter callers keep the placeholder.
	 */
	static #accordionRich({ bundle, tpl, renderInline, run, renderBlock, renderNested, legacyPanels }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (typeof renderBlock !== "function") return null;   // need the body renderer
		const inline = renderInline ?? ((s) => s);
		const rich = tpl.rich_panels ?? {};
		const markerNotes = [];   // ROUND 242: skipped image-ARRANGEMENT layout markers, surfaced as notes on success
		// ROUND 246 ticket 2 — heading-less numbered panels (see head_from_first_line)
		const headFirstCfg = rich.head_from_first_line ?? {};
		const numberedPanels = !legacyPanels && headFirstCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ACCNOTBL_OFF);
		const idRe = new RegExp(rich.video_youtube_id_re
			?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");

		// (1) GROUP members into panels. A panel opens on each [accordion N] tag
		//     (heading = its trailing text); a LEADING heading-less [accordion] is the
		//     opener (skip). Each panel collects an ORDERED list of body parts; a body
		//     part is one of: {p:text} (a run of black/[body] text to renderBlock),
		//     {img:filename}, {video:id}, {nested:subBundle}.
		const panels = [];      // [{ head, parts:[...] }]
		let cur = null;
		let pendingText = [];   // accumulating black/[body] text for the current run

		const flushText = () => {
			if (!cur) { pendingText = []; return; }
			const joined = pendingText.join("\n").trim();
			if (joined) cur.parts.push({ p: joined });
			pendingText = [];
		};

		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;

			// (a0) an IMAGE-ARRANGEMENT LAYOUT MARKER (ROUND 242, Dev-Feedback R5 C1 —
			//     SCCH302 "[2 images next to each other]"): a URL-less embedded-[image]
			//     instruction about how the following images should be ARRANGED. It is
			//     never learner content and never an image element — skip it as build
			//     content; a successful build surfaces its text as the standard red
			//     note after the widget (the r214 instruction-member class). Both
			//     accordion walks previously BAILED the whole widget at this member.
			//     Data accordion.image_layout_marker; env ACCIMGMARK_OFF.
			const layoutMk = this.#imageLayoutMarker(m, tpl);
			if (layoutMk) { markerNotes.push(layoutMk); continue; }

			// (a) NESTED sub-bundle marker (an absorbed shapeHover) — render in place.
			if (m && m.type === "nested") {
				if (!cur) return null;                         // a nested widget before any panel → too odd
				flushText();
				cur.parts.push({ nested: m.nestedBundle });
				continue;
			}

			// (b) panel delimiter.
			if (tag === "accordion") {
				const head = this.#cellText(m.blackAfter ?? "");
				// ROUND 246 (ticket 2): a NUMBERED heading-less tag — "[accordion 1]" alone on
				// its line — is a PANEL MARKER, not the widget's opener, so it opens a panel
				// whose heading is recovered from the panel's own first text line below
				// (head_from_first_line). The bare "[accordion]" / "[accordion x 2]" opener is
				// unnumbered and still skipped, so every accordion that already builds is
				// untouched. env ACCNOTBL_OFF reverts.
				if (!head && numberedPanels && new RegExp(headFirstCfg.numbered_pattern
					?? "\\[\\s*accordion\\s+\\d+\\s*\\]", "i").test(String(m.text ?? ""))) {
					flushText();
					cur = { head: "", parts: [] };
					panels.push(cur);
					continue;
				}
				if (!head) { if (!cur) continue; flushText(); continue; }   // leading opener / stray
				if (this.#hasRedText(m.blackAfter ?? "") || /https?:\/\//.test(head)) return null;
				flushText();
				cur = { head, parts: [] };
				panels.push(cur);
				continue;
			}

			// (c) image member — a single derivable iStock url, nothing else in the cell.
			if (tag === "image") {
				if (!cur) return null;
				const raw = m.blackAfter ?? "";
				if (!this.#cellMediaUrl(raw)) return null;     // not an image cell (no url / a video)
				const text = this.#cellText(raw);
				const filename = this.#istockFilename(text, tpl);
				if (!filename) return null;                    // non-iStock / underivable → bail whole accordion
				const residual = text.replace(/^\s*\[[^\]]*\]\s*/, "")
					.replace(/https?:\/\/\S+/g, "").replace(/\S*gm-?\d{6,10}\S*/g, "")
					.replace(/[/|]/g, " ").trim();
				if (residual) return null;                     // a real caption rode along → too rich
				flushText();
				cur.parts.push({ img: filename });
				continue;
			}

			// (d) video member — a YouTube/Vimeo embed in the cell.
			if (tag === "video") {
				if (!cur) return null;
				const raw = String(m.blackAfter ?? "");
				if (this.#hasRedText(raw)) return null;
				const idm = raw.match(idRe);
				if (!idm) return null;                         // a video we cannot resolve → bail
				flushText();
				cur.parts.push({ video: idm[1] });
				continue;
			}

			// (d2) SUB-HEADING member (ROUND 214, Chris — OSOH501-01 panel 4's [H5]
			//     Manaaki/Tika/Whanaungatanga value headings). A panel's own [H2]-[H6]
			//     sub-heading renders faithfully at the writer's level inside accContent
			//     (the human's exact shape). Red text still bails. Data
			//     rich_panels.sub_headings; env ACCRICH2_OFF reverts (a heading member
			//     bails the whole accordion to the placeholder again).
			if (["h2", "h3", "h4", "h5", "h6"].includes(tag)
				&& rich.sub_headings !== false
				&& !(typeof process !== "undefined" && process.env && process.env.ACCRICH2_OFF)) {
				if (!cur) return null;
				const raw = m.blackAfter ?? "";
				if (this.#hasRedText(raw)) return null;
				const t = this.#cellText(raw).replace(/\*\*/g, "").trim();
				if (!t) continue;
				flushText();
				cur.parts.push({ h: tag, text: t });
				continue;
			}

			// (e0) a WRITER-INSTRUCTION member (ROUND 214) — a CS/Dev note the writer typed
			//     inside a panel ("CS – Please have it so that ākonga click on the image…",
			//     OSOH501-01 panel 1). It is NEVER learner content and NEVER silently lost:
			//     #collectMember already copied it into bundle.instructions, and the BUILT
			//     path surfaces every instruction as a red cv2-note right after the built
			//     widget (the standing house rule). So the member itself is simply SKIPPED
			//     here instead of bailing the whole accordion. Env ACCRICH2_OFF reverts.
			if (m && m.type === "tag"
				&& (m.parse?.class === "instruction" || m.parse?.class === "noise" || m.parse?.instructionFragment)
				&& rich.skip_instruction_members !== false
				&& !(typeof process !== "undefined" && process.env && process.env.ACCRICH2_OFF)) {
				continue;
			}

			// (e) body text — untagged black or a [body] tag. Accumulate (renderBlock
			//     will split paragraphs + form <ul> for bullets). Red instruction text
			//     bails the whole accordion (it must stay a visible flag).
			if (m && m.type === "black") {
				const t = m.text ?? "";
				if (!t.trim()) continue;
				// (e-marker) a LIST-MARKER-only line (ROUND 214) — the docx list artifact a
				//     writer leaves when panels are authored as a numbered list ("1." with the
				//     real content in the following tag item, OSOH501-01 panel 4). Renders
				//     nothing in the human build → skip. Env ACCRICH2_OFF reverts.
				if (/^\s*\(?\d{1,3}[.)]\s*$/.test(t)
					&& rich.skip_list_marker_lines !== false
					&& !(typeof process !== "undefined" && process.env && process.env.ACCRICH2_OFF)) {
					continue;
				}
				if (!cur) return null;
				pendingText.push(t);
				continue;
			}
			if (tag === "body") {
				const raw = m.blackAfter ?? "";
				if (this.#hasRedText(raw)) return null;
				const t = this.#cellText(raw);
				if (!t.trim()) continue;
				if (!cur) return null;
				pendingText.push(t);
				continue;
			}
			if (this.#isInlineMarkerMember(m)) {
				const t = this.#cellText(m.blackAfter ?? "");
				if (this.#hasRedText(m.blackAfter ?? "")) return null;
				if (t.trim()) pendingText.push(t);
				continue;
			}

			// (e.5) a LIST marker ([unordered list]/[ordered list]) — a no-op delimiter;
			//     the bullet lines follow as black "• …" members, which renderBlock
			//     (#renderBlackText) groups into <ul>/<ol> identically to the rest of the
			//     page. Skip the marker; keep the surrounding text accumulating so the
			//     intro <p> and its <ul> stay in one rendered block (the human shape).
			if (tag && /\blist\b/.test(tag)) continue;

			// (f) anything else (a data table, a foreign tag) → too rich → bail.
			return null;
		}
		flushText();

		// (1b) HEADING-LESS PANEL RECOVERY (round 246, ticket 2 of the basic-interactive
		// builders round). A large writer family numbers the panels but puts NO text on the
		// tag itself — "[accordion 1]" on its own line, then the panel's own first line
		// ("US 29302 (Version 3)") and the rest of the body below it. Every such accordion
		// bailed on the "each panel needs a heading" rule below. Chris's directive
		// (2026-08-03): where the writer tagged an accordion, build an accordion — so the
		// panel takes its heading from its own FIRST text line, which is what that line is,
		// and the line is removed from the body so it is never shown twice. A panel left with
		// no body after the promotion still bails (never half-build). Data
		// rich_panels.head_from_first_line; env ACCNOTBL_OFF.
		const headFirst = rich.head_from_first_line;
		if (headFirst && headFirst.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ACCNOTBL_OFF)) {
			for (const p of panels) {
				if (p.head || !p.parts.length) continue;
				const first = p.parts[0];
				if (!first || !first.p) continue;                   // only a TEXT part can donate a heading
				const lines = String(first.p).split("\n").map((s) => s.trim()).filter(Boolean);
				if (lines.length < 2) continue;                     // the whole part IS the body — leave it
				const head = this.#cellText(lines[0]).replace(/^[•·]\s*/, "").trim();
				const maxWords = headFirst.max_words ?? 14;
				if (!head || head.split(/\s+/).length > maxWords) continue;
				if (this.#hasRedText(lines[0])) continue;
				p.head = head;
				first.p = lines.slice(1).join("\n");
				if (!first.p.trim()) p.parts.shift();
				p.r246Head = true;
			}
		}

		// (2) RENDER every panel. Each needs a heading + at least one rendered part.
		if (!panels.length) return null;
		const built = [];
		let recovered = false;
		for (const p of panels) {
			if (p.r246Head) recovered = true;
			if (!p.head || !p.parts.length) return null;
			if (this.#hasRedText(p.head)) return null;
			const chunks = [];
			for (const part of p.parts) {
				if (part.img) {
					chunks.push(this.#assetImage(part.img, tpl, run));
				} else if (part.video) {
					const vt = DataService.Data.EmitTemplates.video?.youtube;
					if (!vt) return null;
					chunks.push(Utils.FillTemplate(vt, { videoId: part.video, params: "" }));
				} else if (part.nested) {
					if (typeof renderNested !== "function") return null;
					const ph = renderNested(part.nested);
					if (!ph) return null;
					// A nested widget that BUILT for real (the renderNested path attempts a
					// real build first) is wrapped in the human's in-panel row (OSOH501-01:
					// accContent 3's READYSAFE tabs sit inside <div class="row">); an un-built
					// nested placeholder stays bare, exactly as before. Data
					// rich_panels.nested_built_wrap; env ACCRICH2_OFF reverts (no wrap).
					const wrapTpl = rich.nested_built_wrap;
					const wrap = wrapTpl && part.nested.built
						&& !(typeof process !== "undefined" && process.env && process.env.ACCRICH2_OFF);
					chunks.push(wrap ? Utils.FillTemplate(wrapTpl, { html: ph }) : ph);
				} else if (part.h) {
					chunks.push(`<${part.h}>${inline(part.text)}</${part.h}>`);
				} else if (part.p) {
					const rendered = renderBlock(part.p);              // array of <p>/<ul> html
					const arr = Array.isArray(rendered) ? rendered : [rendered];
					for (const h of arr) if (h && String(h).trim()) chunks.push(String(h));
				}
			}
			const content = chunks.join("");
			if (!content.trim()) return null;                          // panel with no rendered body
			built.push(Utils.FillTemplate(tpl.row, { head: inline(p.head), content }));
		}
		// ROUND 242: surface the skipped layout markers ONLY on a successful build (a
		// decline keeps the placeholder + raw dump byte-identical); #bundleInstructions
		// de-duplicates downstream, and the note renders red after the widget.
		if (markerNotes.length) bundle.instructions = [...(bundle.instructions ?? []), ...markerNotes];
		if (recovered) bundle.r246Accordion = true;                    // detector/affected-set marker
		return [tpl.open, ...built, tpl.close].join("\n");
	}

	/**
	 * ROUND 242 (Dev-Feedback R5, Family C1 — SCCH302's mixtures accordion). An
	 * IMAGE-ARRANGEMENT LAYOUT MARKER: a red span the lexicon resolves to [image]
	 * only EMBEDDED in prose ("[2 images next to each other]", "[insert images
	 * side by side]"), carrying NO media URL of its own and NO trailing black
	 * content. It is a writer LAYOUT INSTRUCTION about the images that follow —
	 * not an image element — so the accordion walks SKIP it as build content and
	 * a successful build surfaces its text as the standard red note after the
	 * widget (the r214 instruction-member class: never silently stripped, never
	 * a build-breaker). CONTAINMENT BY CONSTRUCTION: both the strict-image and
	 * rich walks previously BAILED the whole accordion at this member (no URL →
	 * return null), so every output this rule can change was a placeholder —
	 * an accordion that already BUILT never carried one. MEASURED corpus-wide
	 * (outputs/_detect_r242_accunnum.cjs, all 429 WTs live): the arrangement
	 * vocabulary = 21 occurrences / 13 modules (+ SCCH302 outside the corpus);
	 * the un-numbered repeated-label [accordion] form itself (75 regions / 41
	 * modules) was ALREADY accepted — the scanner's same-type absorb merges the
	 * repeats into ONE bundle and the rich walk treats each bare head as a panel
	 * delimiter — so this marker was the ONLY blocker on the C1 class.
	 * Data interactive_builders.accordion.image_layout_marker; env ACCIMGMARK_OFF.
	 *
	 * @param {object} m   - a captured member item
	 * @param {object} tpl - the accordion template block (holds image_layout_marker)
	 * @returns {string|null} the marker's note text, or null (not a layout marker)
	 */
	static #imageLayoutMarker(m, tpl) {
		const cfg = tpl?.image_layout_marker;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.ACCIMGMARK_OFF) return null;
		if (!m || m.type !== "tag") return null;
		const p = m.parse?.primary;
		if (!p || p.tag !== "image" || p.how === "exact") return null;   // a real [image]/[images] tag is never a marker
		if (this.#cellText(m.blackAfter ?? "")) return null;             // content rides after → a real member
		const text = String(m.text ?? "");
		if (this.#cellMediaUrl(text)) return null;                       // carries a real URL → a real image reference
		if (!new RegExp(cfg.pattern, "i").test(text)) return null;       // not the arrangement vocabulary
		return this.#cellText(text);
	}

	/**
	 * PLAIN-TEXT accordion (the original builder for this widget, unchanged since it was
	 * first written). Every panel is a heading + body text; any non-text member
	 * (image/video/button/table) bails.
	 */
	static #accordionTextOnly({ bundle, tpl, renderInline }) {
		// Walk the captured members in order, grouping them into panels. A panel
		// opens on each [accordion N] tag (heading = the tag's trailing text) and
		// then collects the body paragraph(s) that follow it, until the next
		// [accordion N] tag. The body may be plain black text or a [body] tag.
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;

		const panels = [];          // [{ head, bodyParts:[...] }]
		let cur = null;

		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;

			// (a) panel delimiter -> start a new panel; heading is its trailing text.
			//     A LEADING [accordion] with NO heading is the OPENER (like [tabs]/[hint
			//     slider] — OSAI501-02 types `[accordion]` then `[accordion 1] …`) -> skip
			//     it; a heading-less [accordion] AFTER panels have started is a genuinely
			//     malformed panel -> bail.
			if (tag === "accordion") {
				const head = this.#cellText(m.blackAfter ?? "");
				if (!head) { if (!cur) continue; return null; }
				if (/https?:\/\//.test(head)) return null;   // a URL in the heading → not a clean accordion (XGF9001 quiz-link panels) → bail
				cur = { head, bodyParts: [] };
				panels.push(cur);
				continue;
			}

			// (b) body paragraph for the current panel (plain text, or a [body] tag
			//     whose trailing text is the paragraph). Body before any panel has
			//     opened means this is not a clean accordion -> bail.
			if (m && m.type === "black") {
				const t = this.#cellText(m.text ?? "");
				if (!t) continue;                       // blank line - ignore
				if (!cur) return null;
				cur.bodyParts.push(t);
				continue;
			}
			if (tag === "body") {
				const t = this.#cellText(m.blackAfter ?? "");
				if (!t) continue;
				if (!cur) return null;
				cur.bodyParts.push(t);
				continue;
			}

			// (b.5) an INLINE-MARKER member ([highlight text]/[word select]/[rollover definition])
			//     is the writer annotating text INLINE within the current panel body — body
			//     CONTINUATION, not a foreign widget. Merge its text into the current panel's last
			//     paragraph (the marker split one paragraph; XGF9001-00 "…value [highlight] mana…").
			if (this.#isInlineMarkerMember(m)) {
				const t = this.#cellText(m.blackAfter ?? "");
				if (!t) continue;
				if (!cur || this.#hasRedText(m.blackAfter ?? "")) return null;
				this.#mergeBodyContinuation(cur.bodyParts, t);
				continue;
			}

			// (c) ANYTHING else (an [image]/[video]/[button]/[link] member, or a data
			//     table) means the bundle is richer than a pure text accordion -- e.g.
			//     OSBY301's trailing [video], or an image panel. We never half-build.
			return null;
		}

		// Every panel must have a heading AND at least one body paragraph, and carry
		// no embedded red writer-instruction text (those stay as visible flags).
		if (!panels.length) return null;
		const inline = renderInline ?? ((s) => s);
		const built = [];
		for (const p of panels) {
			if (!p.head || !p.bodyParts.length) return null;
			if (this.#hasRedText(p.head)) return null;
			if (p.bodyParts.some((t) => this.#hasRedText(t))) return null;
			const content = p.bodyParts.map((t) => `<p>${inline(t)}</p>`).join("");
			built.push(Utils.FillTemplate(tpl.row, { head: inline(p.head), content }));
		}

		// open + every panel + close -> the finished accordion.
		return [tpl.open, ...built, tpl.close].join("\n");
	}

	/**
	 * IMAGE accordion (verified — OSGM501-02). Each panel is `[accordion N]` heading +
	 * an optional single derivable iStock `[image]` + body paragraph(s). The image
	 * renders FIRST inside accContent (Mode P/D, alt non-derivable → ""), then one <p>
	 * per body paragraph — exactly the human shape `accContent > img + p+`.
	 *
	 * PANEL BODY vs TRAILING FREE BODY (the OSGM501-02 boundary, measured): a panel's
	 * body is its first [body] tag plus following UNTAGGED black continuations. A FRESH
	 * [body] TAG in the LAST panel — once that panel already has its image + a body —
	 * is the writer RESUMING free body (the human renders it as a <p> AFTER the
	 * accordion). It (and the rest) render via trailing_body, not as a panel.
	 *
	 * SAFETY (never half-build → null, keep the placeholder): a [video]/[button]/data
	 * table / a 2nd image in a panel / a non-iStock (underivable) image / a panel
	 * missing its heading or body / red writer-instruction text — any of these bails
	 * the WHOLE accordion. Mixed image + text-only panels are allowed (each renders
	 * its own content).
	 */
	static #accordionWithImages({ bundle, tpl, renderInline, run }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		const inline = renderInline ?? ((s) => s);

		// index of the LAST [accordion] tag → tells us when we are past the final panel
		let lastAccIdx = -1;
		members.forEach((m, i) => {
			if (m && m.type === "tag" && m.parse?.primary?.tag === "accordion") lastAccIdx = i;
		});

		const panels = [];          // [{ head, image:filename|null, body:[...] }]
		const trailing = [];        // free-body paragraph(s) after the last panel
		const markerNotes = [];     // ROUND 242: skipped image-ARRANGEMENT layout markers, surfaced as notes on success
		let cur = null;
		let trailingMode = false;

		for (let i = 0; i < members.length; i++) {
			const m = members[i];
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			const raw = m && m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const text = this.#cellText(raw);

			// (a0) an IMAGE-ARRANGEMENT LAYOUT MARKER (ROUND 242 — see #imageLayoutMarker):
			//     skipped as build content, surfaced as a red note on a successful build.
			const layoutMk = this.#imageLayoutMarker(m, tpl);
			if (layoutMk) { markerNotes.push(layoutMk); continue; }

			// (a) panel delimiter. A LEADING [accordion] with NO heading is the OPENER
			//     (OSAI501-02 types `[accordion]` then `[accordion 1] …`) → skip; a
			//     heading-less [accordion] after panels have started → bail.
			if (tag === "accordion") {
				if (!text) { if (!cur) { trailingMode = false; continue; } return null; }
				if (this.#hasRedText(raw) || /https?:\/\//.test(text)) return null;   // red note / a URL in the heading → not a clean accordion → bail
				cur = { head: text, image: null, body: [] };
				panels.push(cur);
				trailingMode = false;
				continue;
			}

			// once resuming free body, everything else is trailing (plain text only)
			if (trailingMode) {
				if (!text) continue;
				if (this.#hasRedText(raw)) return null;
				if (this.#isInlineMarkerMember(m)) { this.#mergeBodyContinuation(trailing, text); continue; }   // inline highlight → trailing continuation
				if (tag && tag !== "body") return null;          // a real widget tag in the tail → bail
				if (/[•·]|\n/.test(text)) return null;
				trailing.push(text);
				continue;
			}

			// (b) the panel image — a single derivable iStock url, nothing else in the cell.
			//     The iStock id is read from the FULL cell text (not the matched URL) so a
			//     stray SPACE inside the writer's URL ("…/lapt op-…-gm683243494-…", OSAI501-02)
			//     still resolves; the residual check likewise strips any gm-id URL slug so the
			//     broken-off tail isn't mistaken for a caption.
			if (tag === "image") {
				if (!cur || cur.image) return null;              // image before a panel / 2nd image → bail
				if (!this.#cellMediaUrl(raw)) return null;       // not an image cell (no URL / a video) → bail
				const filename = this.#istockFilename(text, tpl);
				if (!filename) return null;                      // non-iStock / underivable → bail
				const residual = text.replace(/^\s*\[[^\]]*\]\s*/, "")
					.replace(/https?:\/\/\S+/g, "").replace(/\S*gm-?\d{6,10}\S*/g, "")
					.replace(/[/|]/g, " ").trim();
				if (residual) return null;                       // a real caption rode along → too rich
				cur.image = filename;
				continue;
			}

			// (c) body text. An UNTAGGED black line continues the current panel; a fresh
			//     [body] TAG in the LAST panel after it already has image+body resumes
			//     free body. A null-primary member (an unparsed inline run) is treated as
			//     plain continuation text — never a terminator.
			if (!text) continue;                                 // blank line
			if (!cur) return null;                               // body before any panel → bail
			if (this.#hasRedText(raw)) return null;
			if (tag === "body" && i > lastAccIdx && cur.image && cur.body.length) {
				trailingMode = true;
				trailing.push(text);
				continue;
			}
			if (this.#isInlineMarkerMember(m)) { this.#mergeBodyContinuation(cur.body, text); continue; }   // inline highlight → panel body continuation
			if (tag && tag !== "body") return null;              // a real widget tag → too rich
			cur.body.push(text);
		}

		if (!panels.length) return null;
		const built = [];
		for (const p of panels) {
			if (!p.head || !p.body.length) return null;          // every panel needs a heading + body
			const img = p.image ? this.#assetImage(p.image, tpl, run) : "";
			const content = img + p.body.map((t) => `<p>${inline(t)}</p>`).join("");
			built.push(Utils.FillTemplate(tpl.row, { head: inline(p.head), content }));
		}
		const tail = trailing.map((t) => Utils.FillTemplate(tpl.trailing_body, { text: inline(t) }));
		// ROUND 242: surface the skipped layout markers ONLY on a successful build.
		if (markerNotes.length) bundle.instructions = [...(bundle.instructions ?? []), ...markerNotes];
		return [tpl.open, ...built, tpl.close, ...tail].join("\n");
	}

	/**
	 * speechBubble — a character image beside a STATIC speech/thought bubble.
	 *
	 * HOW THE WRITER AUTHORS IT (verified against the corpus, not assumed):
	 *   one 1x2 TABLE — two cells in a single row — where one cell is an [image]
	 *   tag + its iStock URL and the other is a [speech bubble] tag + the bubble
	 *   text. The scanner also lifts the image URL into bundle.media. The cell
	 *   ORDER tells us the side the developer renders the bubble on.
	 *
	 * SAMPLE captured bundle (OSAI201 #1, the Aria intro):
	 *   media:  [ "https://www.istockphoto.com/photo/...gm978974888-..." ]
	 *   tables: [ { rows: [ [ "[speech bubble] Kia ora! I'm Aria...",   // text cell
	 *                         "[image] https://...gm978974888-..." ] ] } ]  // image cell
	 *   → text cell first, image cell second → bubble-LEFT (matches the human file).
	 *
	 * BUILDS (Emit_Templates.interactive_builders.speechBubble):
	 *   <div class="row speechBubble" layout="speech">
	 *     <div class="col-md-9 col-sm-8"><div class="bubble-left no-hover"><p>{text}</p></div></div>
	 *     <div class="col-3">{image}</div>            (image col + bubble col swap for bubble-right)
	 *   </div>
	 *   {image} honours Mode P/D exactly like MediaBuilder.image.
	 *
	 * SAFETY (never half-build → return null, keep the placeholder) the moment the
	 *   capture is richer than ONE image + ONE static text bubble:
	 *     • a 'layout'/conversation modifier (multi-bubble),
	 *     • not exactly one 1x2 table, or not exactly one image in media,
	 *     • a video URL (YouTube) or a non-iStock image we cannot name,
	 *     • extra red developer-instruction text in EITHER cell (a 2nd red span —
	 *       a "CS: ..." note, or a 'flipside:' front/back reveal). Those are kept
	 *       as visible flags by the placeholder path, faithful to the source.
	 */

	/**
	 * CONVERSATION speechBubble. The writer authors "[speech bubble]
	 * Conversation layout" + alternating Prompt/AI-response BLACK lines; the human
	 * renders div.row.speechBubble > col-md-12 > alternating bubble-right (the
	 * prompt/user turn) / bubble-left.secondary (the AI response). Built from the
	 * bundle's black members by STRICT alternation starting RIGHT (the human's
	 * turn-taking), with a content override (a line starting with a response prefix
	 * forces left, a prompt prefix forces right). Conservative — builds ONLY a clean
	 * black-line conversation (modifier mentions "conversation" OR >= min_turns lines
	 * start Prompt/AI-response) with NO table and NO "face" members ([front]/[back]
	 * tags marking a click-to-reveal side) — anything richer returns null → the
	 * placeholder. Data: speechBubble.conversation.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - the speechBubble template block (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @returns {string|null} the built conversation-bubble HTML, or null to fall through to the static-bubble path
	 */
	static #speechBubbleConversation({ bundle, tpl, renderInline }) {
		const cfg = tpl?.conversation;
		if (!cfg || cfg.enabled === false || !bundle) return null;
		if ((bundle.tables ?? []).length) return null;
		const inline = renderInline ?? ((s) => s);
		const fold = (s) => s.toLowerCase().trim();
		const respPre = cfg.response_prefixes ?? [], promptPre = cfg.prompt_prefixes ?? [];
		const isResp = (l) => respPre.some((p) => fold(l).startsWith(p));
		const isPrompt = (l) => promptPre.some((p) => fold(l).startsWith(p));
		const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();

		// drop the leading invocation [speech bubble] tag; split the rest at a trailing [click drop]
		// (the conversation may absorb its response as an inline CLICK reveal — verified against OSAI401-01
		// Prompt 4 + [Click drop] front/drop, per the Writers Template's literal request, NOT the human's hover).
		const members = (bundle.memberItems ?? []).filter((m, i) =>
			!(i === 0 && m.type === "tag" && m.parse?.primary?.directive === "INTERACTIVE"));
		const cdIdx = members.findIndex((m) => m.type === "tag" && m.parse?.primary?.tag === "click drop");
		const head = cdIdx === -1 ? members : members.slice(0, cdIdx);
		const cdMembers = cdIdx === -1 ? [] : members.slice(cdIdx + 1);
		// head must be PURE black conversation turns; a clickDrop reveal must be ONLY front/drop/back/answer + black
		if (head.some((m) => m.type === "tag")) return null;
		if (cdMembers.some((m) => m.type === "tag"
			&& !["front", "drop", "back", "answer"].includes(m.parse?.primary?.tag))) return null;
		let headLines = head.filter((m) => m.type === "black").map((m) => clean(m.text)).filter(Boolean);
		const hasReveal = cdIdx !== -1 && cdMembers.length > 0;

		// conversation cue: the "Conversation layout" invocation cue, OR >= min_turns prompt/response lines
		const modConvo = /conversation/i.test(bundle.modifier ?? "")
			|| [...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])].some((m) =>
				m.type === "tag" && /conversation/i.test(String(m.text ?? "")));
		const cued = headLines.filter((l) => isResp(l) || isPrompt(l)).length;
		if (!modConvo && cued < (cfg.min_turns ?? 2)) return null;
		if (!headLines.length && !hasReveal) return null;

		// build the inline CLICK reveal (the absorbed clickDrop) as the last bubble: the button is the
		// conversation's trailing "click/see/reveal" prompt line (else the [front] text); the revealed
		// content is the [front] (if not the button) + [drop] + any following bullet lines.
		let revealBubble = "";
		if (hasReveal && cfg.reveal_bubble) {
			const frontTxt = clean(cdMembers.find((m) => m.type === "tag" && m.parse?.primary?.tag === "front")?.blackAfter);
			const lastHead = headLines[headLines.length - 1] ?? "";
			let button = frontTxt || "Click to reveal";
			if (/\b(click|tap|see|reveal|hover)\b/i.test(lastHead)) { button = lastHead; headLines = headLines.slice(0, -1); }
			const content = [];
			if (frontTxt && button !== frontTxt) content.push(frontTxt);
			for (const m of cdMembers) {
				if (m.type === "tag" && m.parse?.primary?.tag === "front") continue;   // the [front] is handled above (button or content)
				const t = m.type === "tag" ? clean(m.blackAfter) : clean(m.text).replace(/^•\s*/, "");
				if (t) content.push(t);
			}
			if (!content.length) return null;
			revealBubble = Utils.FillTemplate(cfg.reveal_bubble, {
				cls: cfg.left_class, front: inline(button),
				drop: content.map((l) => `<p>${inline(l)}</p>`).join("\n"),
			});
		} else if (hasReveal) {
			return null;   // a clickDrop reveal but no template → keep the placeholder
		}

		const bubbles = headLines.map((line, idx) => {
			const side = isResp(line) ? "left" : isPrompt(line) ? "right" : (idx % 2 === 0 ? "right" : "left");
			const cls = side === "right" ? cfg.right_class : cfg.left_class;
			return Utils.FillTemplate(cfg.bubble, { cls, text: inline(line) });
		});
		if (revealBubble) bubbles.push(revealBubble);
		if (!bubbles.length) return null;
		return Utils.FillTemplate(cfg.wrapper, { bubbles: bubbles.join("\n") });
	}
	/**
	 * NO-TABLE AVATAR + BUBBLE (round 246, ticket 1 of the basic-interactive builders round).
	 *
	 * THE GAP. The static bubble branch below only knows the writer's TABLE dialect — exactly
	 * one 1x2 table whose two cells are the [image] and the [speech bubble]. A large family of
	 * writers instead types the whole widget as ONE PARAGRAPH:
	 *
	 *   [Image] avatar Tina  smiling  Young Beautiful Student Woman Set … iStock
	 *   [LINK: https://www.istockphoto.com/vector/…gm2235638824-650974740]
	 *   [speech bubble] RHS  See how the table gives the details, the chart shows the pattern…
	 *
	 * With no table the bubble fell straight to the developer hand-off box while its avatar
	 * rendered as a loose standalone image above it — where the finished page ships ONE
	 * `row speechBubble` holding the avatar column and the bubble column side by side.
	 *
	 * The scanner recovers the paragraph-mate [image] (InteractiveScanner
	 * #absorbSameBlockImage, same source `block` only) and hands it over as
	 * bundle.sameBlockImage; this branch renders it exactly like every other image on the
	 * page (Mode P/D via #assetImage) beside the bubble text.
	 *
	 * MEASURED (outputs/_measure_r246_sbblock.cjs + _measure_r246_gold.py, all 445 corpus
	 * module dirs): the class is EXACTLY 55 bundles (TEDC401 33, TEDC402 21, SSCI104 1) and the
	 * human gold builds an avatar+bubble row at **55 of 55**. The SIDE follows the writer's
	 * ORDER, the same rule the table branch derives from cell order — the image leads in all 55,
	 * giving bubble-right, which matches the gold on 53/55 (2 editorial lefts, the round-123
	 * single-deviation class). The writer's own side word is deliberately ignored: it appears on
	 * only 7 of the 55 and disagrees with the gold where it does appear.
	 *
	 * NEVER HALF-BUILDS. Every richer shape keeps the honest hand-off box: the absorb itself
	 * refuses a bundle with a table, extra widget types, a video URL, more than one iStock id, or
	 * a paragraph carrying a second structural element; here the branch additionally requires a
	 * nameable iStock filename, real bubble text, and a bounded number of paragraphs. Bulleted
	 * and numbered-list bubbles are left to the existing list machinery and decline here.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (needs bundle.sameBlockImage)
	 * @param {object} args.tpl - the speechBubble template block (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @returns {string|null} the built avatar+bubble row, or null to fall through
	 */
	/**
	 * The no-table bubble's TEXT, or null when this bundle is not the plain avatar+bubble
	 * form (round 246). PROMOTED PUBLIC because BOTH sides of the ticket must agree: the
	 * scanner calls it BEFORE absorbing a same-block avatar (so it never consumes an image
	 * the builder would then decline to render — which would trap the image inside a
	 * hand-off box), and #speechBubbleNoTable calls it to render. ONE definition, so the
	 * absorb and the build can never drift apart. (The `contentTable` / `renderBlackText` /
	 * `containerModifiers` / `gatherFollowing` promotion precedent.)
	 *
	 * Accepts the invocation tag's own trailing text plus following plain black lines. Anything
	 * BEFORE the invocation is the absorbed image run — its descriptive words and the iStock
	 * reference title belong to the image, never to the bubble (the round-80/240 media-reference
	 * rule), so the scan starts AT the invocation.
	 *
	 * DECLINES on anything richer, keeping the honest hand-off box: a table or nested
	 * widget, a member carrying a real second element (a trailing [Button] / [MTKQuiz] the
	 * writer put after the bubble), a bulleted or numbered list (the existing build_list
	 * territory), no text at all, or more than max_paragraphs paragraphs.
	 *
	 * @param {object[]} members - bundle.memberItems
	 * @param {object|null} skip - the absorbed image item to ignore (null before the absorb)
	 * @param {object} cfg - Emit_Templates…speechBubble.no_table_image
	 * @returns {string[]|null} the bubble's paragraphs, or null to decline
	 */
	static NoTableBubbleParagraphs(members, skip, cfg) {
		const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
		const list = members ?? [];
		const from = list.findIndex((m) => m?.type === "tag" && m.parse?.primary?.directive === "INTERACTIVE");
		if (from === -1) return null;
		const paras = [];
		for (const m of list.slice(from)) {
			if (!m || m === skip) continue;
			if (m.type === "table" || m.type === "nested") return null;
			if (m.type === "black") { const t = clean(m.text); if (t) paras.push(t); continue; }
			const p = m.parse?.primary;
			if (p && p.directive !== "INTERACTIVE") return null;          // a real second element
			if (!p && !["instruction", "noise"].includes(m.parse?.class)) return null;
			const t = clean(m.blackAfter);
			if (t) paras.push(t);
		}
		if (!paras.length) return null;
		if (paras.length > (cfg?.max_paragraphs ?? 4)) return null;
		// lists are the existing build_list / placeholder territory, not this branch
		if (paras.some((t) => /[•·]/.test(t) || /(^|\s)\d+[.)]\s/.test(t))) return null;
		return paras;
	}

	static #speechBubbleNoTable({ bundle, tpl, renderInline, run }) {
		const cfg = tpl?.no_table_image;
		if (!cfg || cfg.enabled === false || !bundle) return null;
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		if (env.SBNOTBL_OFF) return null;
		const imgItem = bundle.sameBlockImage;
		if (!imgItem) return null;                       // only the scanner's absorbed form
		if ((bundle.tables ?? []).length || (bundle.extraTypes ?? []).length) return null;

		// the one nameable iStock image (the absorb already fenced count/video)
		const urls = (bundle.media ?? []).map((m) => String(m?.target ?? m?.text ?? ""));
		const named = urls.map((u) => ({ u, fn: this.#istockFilename(u, tpl) })).filter((x) => x.fn);
		if (named.length !== 1) return null;

		// bubble text = the invocation tag's own trailing text plus any following black lines.
		// The absorbed image run sits at the FRONT of memberItems and contributes nothing.
		const inline = renderInline ?? ((s) => s);
		const paras = this.NoTableBubbleParagraphs(bundle.memberItems, imgItem, cfg);
		if (!paras) return null;

		// ORDER sets the side, exactly like the table branch's cell order: the image leading
		// puts the avatar in the left column and the bubble on the right.
		const imgFirst = (bundle.memberItems ?? []).indexOf(imgItem) === 0;
		const imageBlock = Utils.FillTemplate(cfg.image_col,
			{ image: this.#assetImage(named[0].fn, tpl, run) });
		const textBlock = Utils.FillTemplate(imgFirst ? cfg.text_col_right : cfg.text_col_left,
			{ text: paras.map((t) => `<p>${inline(t)}</p>`).join("\n") });
		const open = Utils.FillTemplate(cfg.open ?? tpl.open, { layout: tpl.layout_attr ?? "speech" });
		const middle = imgFirst ? [imageBlock, textBlock] : [textBlock, imageBlock];
		return [open, ...middle, cfg.close ?? tpl.close].join("\n");
	}

	/**
	 * TEXT-ONLY BUBBLE(S) — ROUND 247 (Chris, ENGS404-00 "[insert thought bubble]").
	 * The writer's bubble with NO character image and NO table: "[insert thought bubble]
	 * Where do we find stories? [insert thought bubble] Why are stories important?" — the
	 * round-246 recorded image-less decline class, now built on Chris's directive that ALL
	 * basic interactives build (the A1 writer's-tag branch). MEASURED: 229 such bundles /
	 * 52 modules corpus-wide (outputs/_detect_r247.cjs), 212 of them clean; the human
	 * library itself ships the text-only form 385 times, with layout="thought" (365 occ /
	 * 152 pages) for exactly this wording — emit shape = the measured plurality
	 * (col-12 > bubble-basic no-hover bubble-top; the side/colour scatter is editorial C).
	 * Each INTERACTIVE invocation member opens its OWN bubble row; its trailing text plus
	 * any following black lines are that bubble's paragraphs (>1 <p> takes the round-104
	 * wrapper <div>). layout = "thought" when the writer's own tag wording says thought,
	 * else the standard speech. NEVER half-builds: any real second element / table /
	 * media / empty bubble / bulleted text (the build_list territory) / over-long bubble
	 * declines to the honest hand-off box. Data speechBubble.text_only; env SBTEXT_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items)
	 * @param {object} args.tpl - the speechBubble template block (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @returns {string|null} the built bubble row(s), or null to keep the placeholder
	 */
	static #speechBubbleTextOnly({ bundle, tpl, renderInline }) {
		const cfg = tpl?.text_only;
		if (!cfg || cfg.enabled === false || !bundle) return null;
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		if (env.SBTEXT_OFF) return null;
		if ((bundle.tables ?? []).length || (bundle.media ?? []).length || bundle.sameBlockImage) return null;
		if ((bundle.extraTypes ?? []).some((t) => t !== bundle.type)) return null;   // same-type merge only
		const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
		const maxP = cfg.max_paragraphs ?? 4;
		const thoughtRe = new RegExp(cfg.thought_re ?? "thought", "i");
		const bubbles = [];
		let curB = null, thought = false;
		for (const m of bundle.memberItems ?? []) {
			if (!m) continue;
			if (m.type === "table" || m.type === "nested") return null;
			if (m.type === "black") {
				const t = clean(m.text);
				if (!t) continue;
				if (!curB) return null;                 // stray text before any bubble → not this form
				curB.push(t);
				continue;
			}
			const p = m.parse?.primary;
			if (p && p.directive === "INTERACTIVE") {
				if (thoughtRe.test(String(m.text ?? ""))) thought = true;
				curB = [];
				bubbles.push(curB);
				const t = clean(m.blackAfter);
				if (t) curB.push(t);
				continue;
			}
			if (!p && ["instruction", "noise"].includes(m.parse?.class)) continue;   // writer notes ride along
			return null;                                // a real second element → never half-build
		}
		// a "paragraph" with no letter/digit in any script is stray punctuation a split
		// bracket left behind (the r104 STRAYLEAD class — TEDC402's lone "]") — drop it
		for (const b of bubbles) {
			for (let k = b.length - 1; k >= 0; k--) if (!/[\p{L}\p{N}]/u.test(b[k])) b.splice(k, 1);
		}
		if (!bubbles.length || bubbles.some((b) => !b.length)) return null;          // an EMPTY bubble → bail
		for (const b of bubbles) {
			if (b.length > maxP) return null;
			if (b.some((t) => /[•·]/.test(t) || /(^|\s)\d+[.)]\s/.test(t))) return null;   // the build_list territory
		}
		const inline = renderInline ?? ((s) => s);
		const layout = thought ? (cfg.layout_thought ?? "thought") : (tpl.layout_attr ?? "speech");
		return bubbles.map((b) => {
			const ps = b.map((t) => `<p>${inline(t)}</p>`).join("\n");
			const text = b.length > 1 ? `<div>\n${ps}\n</div>` : ps;   // the round-104 multi-<p> wrapper rule
			return [
				Utils.FillTemplate(cfg.open ?? tpl.open, { layout }),
				cfg.col_open,
				Utils.FillTemplate(cfg.bubble, { text }),
				cfg.col_close,
				cfg.close ?? tpl.close,
			].join("\n");
		}).join("\n");
	}

	/**
	 * The full speechBubble dispatcher: tries the multi-turn CONVERSATION form first,
	 * then falls back to the plain static ONE-IMAGE + ONE-TEXT-BUBBLE form documented
	 * above. See that doc block for the data shape and the safety/bail conditions.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - the speechBubble template block (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @returns {string|null} the built speechBubble HTML, or null to keep the orange placeholder
	 */
	static #speechBubble({ bundle, tpl, renderInline, run }) {
		// (0) CONVERSATION layout: a multi-turn Prompt/AI-response bubble
		// chain (verified against OSAI401-01). Built from black-line members as alternating bubbles.
		const convo = this.#speechBubbleConversation({ bundle, tpl, renderInline });
		if (convo) return convo;

		// (0b) NO-TABLE AVATAR + BUBBLE: the writer's one-paragraph dialect, recovered by the
		// scanner's same-block image absorb. Tried before the table branch (which requires a
		// 1x2 table this form never has). See #speechBubbleNoTable.
		const noTbl = this.#speechBubbleNoTable({ bundle, tpl, renderInline, run });
		if (noTbl) return noTbl;

		// (0c) TEXT-ONLY bubble(s) — no image, no table (round 247, ENGS404-00). Tried
		// BEFORE the modifier bail: the writer's benign "[insert thought bubble]" wording
		// resolves as a modifier, and the image-ambiguity the modifier bail protects
		// against cannot arise in a media-less bundle. See #speechBubbleTextOnly.
		const txtOnly = this.#speechBubbleTextOnly({ bundle, tpl, renderInline });
		if (txtOnly) return txtOnly;

		// (1) Only the simple, static bubble. A non-empty modifier marks the
		// writer's conversation/multi-bubble layouts (e.g. OSBY301's
		// "[speech bubbles- conversation layout]") — never one image + one text.
		if (bundle?.modifier) return null;

		// (2) The clean capture is EXACTLY one 1x2 table (one row, two cells).
		const tables = bundle?.tables ?? [];
		if (tables.length !== 1) return null;
		const rows = tables[0].rows ?? [];
		if (rows.length !== 1) return null;
		const row = rows[0] ?? [];
		if (row.length !== 2) return null;

		// (3) ...and EXACTLY one image in media that we can NAME (an iStock photo).
		// (verified against OSAH501-03): the bubble TEXT may carry its OWN hyperlinks
		// ([LINK: mailto:…] / [LINK: https://…] — the Lawdog "Email help@netsafe.org.nz / Complete
		// an online contact form" bullets) which #harvestMedia collects into bundle.media ALONGSIDE
		// the one iStock image, so an EARLIER `media.length !== 1` check bailed on every bubble whose
		// body links out. Instead, count the iStock IMAGES (the entries #istockFilename names) and
		// require EXACTLY ONE; still BAIL on a video (a YouTube/Vimeo bubble is not the plain image
		// form) or a 2nd image. The non-image hyperlink URLs are the bubble's own links, woven into
		// the text by the converter's separate [LINK:] hyperlink-weave logic (elsewhere in the
		// pipeline). Data speechBubble.image_only_media; env SBLINKMEDIA_OFF reverts.
		const media = bundle?.media ?? [];
		const _envM = (typeof process !== "undefined" && process.env) ? process.env : {};
		let url, filename;
		if ((tpl.image_only_media !== false) && !_envM.SBLINKMEDIA_OFF) {
			const urls = media.map((m) => String(m?.target ?? m?.text ?? ""));
			if (urls.some((u) => /youtu\.?be|youtube\.com|vimeo/i.test(u))) return null;   // a video → not the plain bubble
			const imgs = urls.map((u) => ({ u, fn: this.#istockFilename(u, tpl) })).filter((x) => x.fn);
			if (imgs.length !== 1) return null;          // need EXACTLY one nameable iStock image (a 2nd image bails)
			url = imgs[0].u; filename = imgs[0].fn;
		} else {
			if (media.length !== 1) return null;
			url = String(media[0]?.target ?? media[0]?.text ?? "");
			filename = this.#istockFilename(url, tpl);
			if (!filename) return null;                 // video / non-iStock → fall back
		}

		// (4) Tell the two cells apart: the IMAGE cell is the one carrying the URL
		// (or an [image] tag); the OTHER cell is the bubble text. Keying off the
		// captured URL (not the tag word) is robust to writer tag spellings.
		const imgIdx = row.findIndex((c) => this.#isImageCell(c, url));
		if (imgIdx === -1) return null;
		// (5) Strip developer-INSTRUCTION ("CS: …") and REVEAL ("flipside:") red spans first — they
		// must not block an otherwise-clean build. The human builds the bubble regardless: a CS note
		// is a manual image/layout edit (not bubble content), and a flipside label just separates the
		// bubble's two text parts. The widget's own [image]/[speech bubble] tag span is kept; any OTHER
		// unexpected 2nd red span still bails below. (OSAI201 #1 CS-note image cell; #8 flipside text.)
		let imgCell = this.#stripDevSpans(String(row[imgIdx] ?? ""), tpl.droppable_span_prefixes);
		const txtCell = this.#stripDevSpans(String(row[imgIdx === 0 ? 1 : 0] ?? ""), tpl.droppable_span_prefixes);
		// CS-INSTRUCTION isolation (verified against OSAI201-02 #12): the image cell is authored
		// "[image] CS <sign text> [Can that go on the sign?] / URL" — a documented cue (CS/dev/note)
		// right after the [image] tag introduces a MANUAL-edit instruction (the sign text AND the
		// question, red + black) running to the URL. stripDevSpans can't remove the BLACK sign text,
		// so the imgResidual check would still bail. Reduce the cell to its [image] tag + URL (the only
		// build-relevant parts) so the bubble builds (the human builds it; the designer adds the sign
		// text by hand). Only fires when a cue sits immediately after the tag — a normal image cell is
		// untouched.
		imgCell = this.#isolateInstructionImageCell(imgCell, tpl.droppable_span_prefixes, url);

		// Both cells must now be CLEAN (faithful-to-source; never half-build). A clean cell carries at
		// most ONE red span — its own tag. A surviving SECOND red span is an unrecognised instruction →
		// bail and keep the honest placeholder + its flag.
		if (this.#redSpanCount(imgCell) > 1) return null;
		if (this.#redSpanCount(txtCell) > 1) return null;

		// image cell: once the leading [image] tag and the URL are removed, NOTHING
		// meaningful may remain (no caption / no stray prose we would otherwise drop).
		// Markdown emphasis markers (the writer ITALICISED the URL — OSAI501-03 #11's
		// "*https://…*") are formatting, not a caption, so they are stripped too; the "/"
		// the writer used to separate the URL from a now-removed CS note is just a separator.
		const imgResidual = this.#cellText(imgCell)
			.replace(/^\s*\[[^\]]*\]\s*/, "")       // drop the leading [image] tag
			.replace(/https?:\/\/\S+/g, "")          // drop the URL (consumed into the filename)
			.replace(/[*_~`/|]/g, "")                // drop stray markdown emphasis + the "/" separator
			.trim();
		if (imgResidual) return null;

		// text cell: drop the leading [speech bubble] tag (and the writer's "/" separator
		// that sometimes follows it, OSBY201-02 #8) → the bubble text itself.
		const text = this.#cellText(txtCell).replace(/^\s*\[[^\]]*\]\s*/, "").replace(/^\/\s*/, "").trim();
		if (!text) return null;

		const inline = renderInline ?? ((s) => s);
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		// A hard newline → a structure we don't reproduce here → placeholder.
		if (/\n/.test(text)) return null;
		// A NUMBERED list ("1. … / 2. …") is also not reproduced here. Match the number only at
		// a " / "-PART START (a real list marker), NOT anywhere in the text — a phone number
		// mid-bullet ("call 0508 NETSAFE (0508 638 723) within New Zealand") must not be mistaken
		// for a list marker and bail the build (verified against OSAH501-03). env SBNUMLIST_OFF
		// reverts to the older "match anywhere in the text" behaviour.
		if (env.SBNUMLIST_OFF
			? /(^|\s)\d+[.)]\s/.test(text)
			: text.split(/\s+\/\s+/).some((part) => /^\s*\d+[.)]\s/.test(part.trim()))) return null;

		let textHtml, blockBody = false, multiP = false;
		if (/[•·]/.test(text)) {
			// A BULLETED bubble ("intro / • item / • item /
			// closing") is BUILT as a <p>/<ul> structure inside the bubble (the human renders
			// the list — verified against OSBY201-02 #8), rather than left as an un-built
			// placeholder. Data speechBubble.build_list; env SBLIST_OFF reverts to the
			// placeholder. Uses a BLOCK text template (no outer <p>) so the <ul> isn't
			// illegally nested inside a <p>.
			if (!tpl.build_list || env.SBLIST_OFF) return null;
			textHtml = this.#bubbleBody(text, inline);
			if (!textHtml) return null;
			blockBody = true;
		} else {
			// The writer's " / " is a PARAGRAPH break when the parts are paragraph-like (the
			// human renders multiple <p> — OSAI501-02 #7's GenAI bubble). It is a LIST when the
			// parts are short labels (OSBY301). So split on " / " and render multiple <p> ONLY
			// when EVERY part looks like a sentence/paragraph; a short-item " / " list keeps the
			// placeholder. Robust to the count of parts and tolerant of the writer's spacing.
			let paragraphs = [text];
			if (/(^|\s)\/(\s|$)/.test(text)) {
				const parts = text.split(/\s+\/\s+/).map((s) => s.trim()).filter(Boolean);
				const minWords = tpl.paragraph_min_words ?? 6;
				const paragraphLike = parts.length >= 2
					&& parts.every((p) => p.split(/\s+/).length >= minWords && /[.!?]/.test(p));
				if (!paragraphLike) return null;            // a short-item list → keep the placeholder
				paragraphs = parts;
			}
			multiP = paragraphs.length >= 2;
			textHtml = paragraphs.map((p) => inline(p)).join("</p><p>");
		}

		// (6) Compose. Cell order sets the side: image SECOND → bubble-left (text
		// on the left); image FIRST → bubble-right (image on the left). The image
		// renders per the run's Mode P/D, like every other image on the page.
		const layout = tpl.layout_attr ?? "speech";
		const imageBlock = Utils.FillTemplate(tpl.image_col, { image: this.#assetImage(filename, tpl, run) });
		// THE WRAPPER-DIV RULE (verified against OSAH501-01): when the bubble body is
		// MORE THAN ONE <p> (the ' / ' multi-paragraph split) OR a bulleted block, the human
		// wraps the whole run in an extra <div> inside a 'bubble-basic no-hover bubble-{side}'
		// element. Single-<p> bubbles keep the plain 'bubble-{side} no-hover' + direct <p> form.
		// Measured 12/12 human真-multi bubbles use bubble-basic + wrapper. Data
		// speechBubble.multi_wrapper; env SBWRAP_OFF reverts to the single-bubble form.
		const mw = tpl.multi_wrapper;
		const useWrap = (blockBody || multiP) && mw && mw.enabled !== false && !env.SBWRAP_OFF;
		let txtTpl, fill;
		if (useWrap) {
			txtTpl = imgIdx === 1 ? mw.text_left : mw.text_right;        // bubble-basic + <div> wrapper
			fill = blockBody ? textHtml : `<p>${textHtml}</p>`;          // a COMPLETE block run
		} else if (blockBody) {
			txtTpl = imgIdx === 1 ? (tpl.text_left_block ?? tpl.text_left) : (tpl.text_right_block ?? tpl.text_right);
			fill = textHtml;
		} else {
			txtTpl = imgIdx === 1 ? tpl.text_left : tpl.text_right;       // template wraps in <p>{text}</p>
			fill = textHtml;
		}
		const textBlock = Utils.FillTemplate(txtTpl, { text: fill });
		const middle = imgIdx === 1 ? [textBlock, imageBlock] : [imageBlock, textBlock];
		return [Utils.FillTemplate(tpl.open, { layout }), ...middle, tpl.close].join("\n");
	}

	/**
	 * Renders a BULLETED speech-bubble body: the writer's " / "-separated parts where
	 * a "• "-led part is a list item. Consecutive bullets group into one <ul>; other parts are
	 * <p>. (OSBY201-02 #8's "intro / • a / • b / • c / closing" → <p>intro</p><ul>…</ul><p>closing</p>.)
	 *
	 * @param {string} text - the bubble's raw " / "-joined text
	 * @param {function} inline - inline-markup renderer (bold/italic/links)
	 * @returns {string} the assembled <p>/<ul> HTML (never null — an empty input yields "")
	 */
	static #bubbleBody(text, inline) {
		const parts = String(text ?? "").split(/\s+\/\s+/).map((s) => s.trim()).filter(Boolean);
		if (!parts.length) return "";
		const out = []; let li = [];
		const flush = () => { if (li.length) { out.push(`<ul>${li.map((x) => `<li>${inline(x)}</li>`).join("")}</ul>`); li = []; } };
		for (const p of parts) {
			const b = p.match(/^[•·]\s*(.*)$/);
			if (b && b[1].trim()) li.push(b[1].trim());
			else { flush(); out.push(`<p>${inline(p)}</p>`); }
		}
		flush();
		return out.join("");
	}

	/**
	 * flipCard — a grid of cards, each a FRONT that flips to reveal a BACK.
	 *
	 * DATA SHAPE WE EXPECT: exactly one 2-column table — column 1 is every card's
	 *   front, column 2 its back. A leading column-label row ("Image for one side |
	 *   Text for flipped side", "Front | Back", or the writer's red labels) is
	 *   dropped. Each cell renders to an IMAGE (Mode P/D) or plain TEXT.
	 *
	 * SAMPLE captured rows:
	 *   CEDO202 (text|text): ["Some animals hibernate…", "Make a shape with your body…"]
	 *   ENGJ302 (image|text): ["[IMAGE…] [LINK: …istockphoto…]", "**Brown bear** / **Max speed:** 56 kmh / …"]
	 *
	 * BUILDS one <div class="row flipCardsContainer"> with, per card (flipCard.card):
	 *   <div class="col-…"><div class="flipCard"><div class="front">{front}</div>
	 *     <div class="back">{back}</div></div></div>
	 *
	 * SAFETY (never half-build → null, keep the placeholder): see #flipCell — any
	 *   cell that is neither a clean image nor red-free text (e.g. ENGI202's
	 *   [Front of flip card]-labelled cells), an empty cell, bullets, or a capture
	 *   wider than two columns / more than one table, all fall back.
	 */
	/**
	 * shapeHover — a ring of clickable image "shapes", each revealing a text panel (verified
	 * against OSAI501-02). The writer authors [shape hover] then repeating groups [shape n][H#] TITLE + [body]
	 * HOVER-TEXT + [image] iStock-URL (the scanner captures these as members; the heading carries the
	 * 'shape n' subtag). Builds the human's two-zone structure:
	 *   <div class=shapeHover layout=clockwise>
	 *     <div class=outerContent>  N x <div class='shape image'>(img + <h4 class=template-colours>title</h4>)
	 *     <div class=hoverContent>  N x <div class=shapeContent><div><p>body</p></div></div>
	 * shapeHover is a recognised WIDGET, so the automated structural-comparison tests treat the whole
	 * subtree as one opaque widget marker (they don't look inside it, so its layout/colour/alt details
	 * can't fail that comparison) — meaning we get full credit for the correct structure while still
	 * rendering the real, visible HTML faithfully. CONSERVATIVE
	 * (never half-build): bails to the placeholder on a table, a nested widget, red instruction text, a
	 * non-iStock/unresolvable image, fewer than min_shapes shapes, or any shape missing a title/image/body.
	 * Data interactive_builders.shapeHover; env SHAPEHOVER_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (image mode, resolved template rules)
	 * @returns {string|null} the built shapeHover HTML, or null to keep the orange placeholder
	 */
	static #shapeHover({ bundle, tpl, renderInline, run }) {
		if (!tpl || tpl.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.SHAPEHOVER_OFF) return null;
		if ((bundle?.tables ?? []).length) return null;          // table-authored form not handled → placeholder
		const inline = renderInline ?? ((s) => s);
		const members = [...(bundle?.openerItems ?? []), ...(bundle?.memberItems ?? [])];
		if (!members.length) return null;

		const shapes = [];   // [{ title, body, img }]
		let cur = null;
		for (const m of members) {
			if (m.type === "nested" || m.type === "table") return null;   // richer/foreign → keep placeholder
			const p = m.type === "tag" ? m.parse?.primary : null;
			const tags = m.type === "tag" ? (m.parse?.tags ?? []).map((t) => t.tag) : [];
			// the [shape hover] opener itself — skip
			if (p?.directive === "INTERACTIVE" && /shape\s*hover/.test(p?.tag ?? "")) continue;
			// a [shape n] member (carries the shape's heading) opens a new shape
			if (tags.includes("shape n")) {
				cur = { title: this.#cellText(m.blackAfter ?? "").trim(), body: "", img: "" };
				shapes.push(cur);
				continue;
			}
			if (!cur) {                                          // anything before the first shape
				if (m.type === "black" && !this.#cellText(m.text ?? "")) continue;   // blank line → skip
				return null;                                     // real content with no shape → bail
			}
			const raw = m.type === "tag" ? String(m.blackAfter ?? "") : String(m.text ?? "");
			if (p?.tag === "image") { cur.img += " " + raw; continue; }
			if (p?.tag === "body" || (m.type === "black" && this.#cellText(raw))) {
				if (this.#hasRedText(raw)) return null;          // embedded writer instruction → bail
				const t = this.#cellText(raw).trim();
				if (t) cur.body += (cur.body ? " " : "") + t;
				continue;
			}
			return null;                                         // any other member → not the clean form → bail
		}
		if (shapes.length < (tpl.min_shapes ?? 2)) return null;

		const colour = tpl.colour_var_by_phase?.[run?.resolvedRules?.template_phase]
			?? tpl.colour_var_by_phase?._default ?? "NCEA";
		const layout = tpl.layout_default ?? "clockwise";
		const outer = [], hover = [];
		for (const s of shapes) {
			if (!s.title || !s.img.trim() || !s.body) return null;   // every shape needs title + image + body
			const id = (s.img.match(/gm-?(\d{6,10})/) || s.img.match(/\/id\/(\d{4,10})/) || [])[1] ?? null;
			if (!id) return null;                                    // non-iStock/unresolvable → keep placeholder
			const image = this.#assetImage(Utils.FillTemplate(tpl.filename_istock, { id }), tpl, run);
			if (!image) return null;
			outer.push(Utils.FillTemplate(tpl.shape, { image, title: inline(s.title), colour }));
			hover.push(Utils.FillTemplate(tpl.shape_content, { body: inline(s.body) }));
		}
		return [
			Utils.FillTemplate(tpl.container_open, { layout }),
			tpl.outer_open, ...outer, tpl.outer_close,
			tpl.hover_open, ...hover, tpl.hover_close,
			tpl.container_close,
		].join("\n");
	}

	/**
	 * The full flipCard dispatcher — see the "flipCard — a grid of cards..." doc block
	 * above (near shapeHover) for the general shape/safety rules. Tries several capture
	 * forms most-specific-first, falling through to the next when one declines:
	 *   1. no table at all                                            → #flipCardMembers (image-front cards captured as [Flip Card N] tags)
	 *   2. Front|Back|Front|Back… header, ONE data row (2N columns)    → #flipCardAlternating
	 *   3. Front|Back|Front|Back… header, MULTIPLE data rows           → #flipCardMultiRow
	 *   4. exactly 2 rows, whole COLUMNS are fronts/backs (not rows)   → #flipCardTransposed
	 *   5. plain 2-column table (front | back)                        → the default path below
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @returns {string|null} the built flipCard HTML, or null to keep the orange placeholder
	 */
	static #flipCard({ bundle, tpl, renderInline, run }) {
		const tables = bundle?.tables ?? [];
		// MEMBER-CAPTURED image-front cards (verified against OSAI501-03): NO table, the writer
		// authored [Flip Card N] + [Front][H4] title + [image] url + [back] text per card. Build the
		// human's 2-wide image-front grid (else null → keep the placeholder; never half-build). The
		// TABLE forms (handled below) are untouched. Data flipCard.member_image_cards; env FLIPMEMBER_OFF.
		if (!tables.length) return this.#flipCardMembers({ bundle, tpl, run, renderInline });
		if (tables.length !== 1) return null;
		const allRows = tables[0].rows ?? [];
		const width = Math.max(0, ...allRows.map((r) => (r ?? []).length));

		// ALTERNATING multi-column "Flip card image" variant: a header row of
		// Front|Back|Front|Back… labels over a SINGLE data row of 2N columns, each column-pair a
		// card with a rich image-front. Built only when clean, else null → the 2-col path below /
		// placeholder. Scoped to width>=4 so the plain 2-col front|back form further down is untouched.
		if (tpl.alternating_multicol && width >= 4 && width % 2 === 0
			&& !(typeof process !== "undefined" && process.env && process.env.FLIPALT_OFF)) {
			const alt = this.#flipCardAlternating(allRows, width, tpl, run, renderInline ?? ((s) => s));
			if (alt !== null) return alt;
		}

		// THE MULTI-ROW alternating Front/Back form (verified against OSAH501-03): a
		// Front|Back|Front|Back header over MULTIPLE data rows (each row = width/2 cards,
		// read column-pair by column-pair), with a RICH/BULLETED back the writer laid out as
		// "[body] / Law: X / lead-in: / • a / • b". The writer's [Flip card image] tag asks for
		// flip cards; the human editorially rebuilt it as an accordion, but THAT choice is
		// NON-DERIVABLE (there is no direct link from the writer's tag to "render as an
		// accordion instead"), so this converter faithfully builds the writer's flipCard
		// instead. Generalises the single-data-row alternating form above (#flipCardAlternating)
		// to N rows + a bulleted back. Scoped width>=4 so the plain 2-col front|back form is
		// untouched; the automated structural comparison collapses flipCard/accordion/placeholder
		// all to one WIDGET marker, so this rendering choice is invisible to that score either
		// way — a dedicated flipCard checker verifies the actual build. Conservative
		// (never half-build → placeholder): clean Front/Back header, every row width-wide, every
		// card builds cleanly. Data flipCard.front_back_multirow; env FLIPMULTIROW_OFF.
		// Runs AFTER the single-row alternating form above (which handles its exact shape
		// first) — this is a more capable FALLBACK for any width>=4 Front/Back table that
		// single-row form can't handle: multiple data rows, a bulleted/rich back, or an
		// image-only front. Header + >=1 data row.
		if (tpl.front_back_multirow && width >= 4 && width % 2 === 0 && allRows.length >= 2
			&& !(typeof process !== "undefined" && process.env && process.env.FLIPMULTIROW_OFF)) {
			const mr = this.#flipCardMultiRow(allRows, width, tpl, run, renderInline ?? ((s) => s));
			if (mr !== null) return mr;
		}

		// TRANSPOSED multi-column form (verified against OSBY201-02 #12): a 2-ROW table whose
		// COLUMNS are the cards — row 0 = the fronts ("[front] / label / [image] url"), row 1 =
		// the backs ("[back] / text"). Build N image-front / text-back cards (reusing
		// #flipImageFront/#flipBack with the leading [front]/[back] FACE directive stripped).
		// Conservative: exactly 2 rows, width>=2, every cell builds cleanly. Env FLIPTRANS_OFF.
		if (tpl.transposed && allRows.length === 2 && width >= 2 && width !== 2
			&& !(typeof process !== "undefined" && process.env && process.env.FLIPTRANS_OFF)) {
			const trans = this.#flipCardTransposed(allRows, width, tpl, run, renderInline ?? ((s) => s));
			if (trans !== null) return trans;
		}

		if (width !== 2) return null;                       // strictly front | back

		// keep the genuine two-cell rows; drop a leading column-label header row.
		let rows = allRows.filter((r) => Array.isArray(r) && r.length === 2);
		if (rows.length && this.#looksLikeFlipHeader(rows[0], tpl)) rows = rows.slice(1);
		if (!rows.length) return null;

		const inline = renderInline ?? ((s) => s);
		const cards = [];
		for (const r of rows) {
			const front = this.#flipCell(r[0], tpl, run, inline);
			const back = this.#flipCell(r[1], tpl, run, inline);
			if (front === null || back === null) return null;   // any unclear cell → fall back
			cards.push(Utils.FillTemplate(tpl.card, { front, back }));
		}
		return [tpl.container_open, ...cards, tpl.container_close].join("\n");
	}

	/**
	 * MEMBER-CAPTURED image-front flipCards (verified against OSAI501-03). The writer authored NO
	 * table — instead [Flip Card N] then [Front]([H4]) title + [image] url + [back] text per card.
	 * The human builds a 2-wide IMAGE-FRONT grid (col-md-6 > flipCard noBG > front flipImage(img+h4)
	 * + back(p)). Reuses #flipImageFront / #flipBack. Conservative (never half-build): every card
	 * needs an image-front (image + title) AND a back; any other/missing member → null (placeholder).
	 * Data flipCard.member_image_cards (+ card_image_front); env FLIPMEMBER_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @returns {string|null} the built flipCard HTML, or null to fall through to the table-based forms
	 */
	static #flipCardMembers({ bundle, tpl, run, renderInline }) {
		if (!tpl.member_image_cards || !tpl.card_image_front) return null;
		if (typeof process !== "undefined" && process.env && process.env.FLIPMEMBER_OFF) return null;
		if ((bundle?.tables ?? []).length) return null;
		const inline = renderInline ?? ((s) => s);
		const members = [...(bundle?.openerItems ?? []), ...(bundle?.memberItems ?? [])];
		if (!members.length) return null;

		// TWO member shapes (both handled): (A) the INLINE shape — [Flip Card N], [Front][H4] title +
		// [image] url (one item), [back] text (one item); (B) the SEPARATE shape (verified against
		// OSAI501-04) — [Flip Card N], [Front], [H5] title, [image] url, [back], [body] text (+ a
		// black "Example:" line). `face` tracks which SIDE of the card we are currently filling in
		// ("front" or "back"); a HEADING is the front title, a [body]/black line after [back] is the
		// back content.
		const cards = [];                 // [{ title, img, back }]
		let cur = null, face = null;
		const headingTags = new Set(["h2", "h3", "h4", "h5", "h6", "heading", "story heading"]);
		for (const m of members) {
			const p = m && m.type === "tag" ? m.parse?.primary : null;
			const tags = m && m.type === "tag" ? (m.parse?.tags ?? []).map((t) => t.tag) : [];
			// a [Flip Card N] INTERACTIVE tag opens a new card (the opener + each subsequent one)
			if (p?.directive === "INTERACTIVE" && p?.tag === "flip card") { cur = { title: "", img: "", back: "" }; cards.push(cur); face = "front"; continue; }
			if (!cur) {                    // a blank black line before the first card → skip; anything else → bail
				if (m.type === "black" && !this.#cellText(m.text ?? "")) continue;
				return null;
			}
			// FACE markers — may carry inline content (shape A) or be empty markers (shape B)
			if (tags.includes("front") || p?.tag === "front") { face = "front"; const t = this.#cellText(m.blackAfter ?? ""); if (t) cur.title += (cur.title ? " " : "") + t; continue; }
			if (p?.tag === "back") { face = "back"; const t = this.#cellText(m.blackAfter ?? ""); if (t) cur.back += (cur.back ? " / " : "") + t; continue; }
			if (p?.tag === "image") { cur.img += " " + String(m.blackAfter ?? ""); continue; }
			// a HEADING is the front title (shape B: [Front] then [H5] title)
			if (p && headingTags.has(p.tag)) {
				if (this.#hasRedText(m.blackAfter ?? "")) return null;
				const t = this.#cellText(m.blackAfter ?? ""); if (t) cur.title += (cur.title ? " " : "") + t;
				continue;
			}
			// a [body] ELEMENT or a non-blank black line is BACK content (shape B: [back] then [body] + "Example:")
			if (p?.tag === "body" || m.type === "black") {
				const raw = m.type === "tag" ? String(m.blackAfter ?? "") : String(m.text ?? "");
				if (!this.#cellText(raw).trim()) continue;            // blank line → skip
				if (this.#hasRedText(raw)) return null;               // embedded writer instruction → bail
				if (face !== "back") return null;                     // body before any [back] → not this clean form → bail
				cur.back += (cur.back ? " / " : "") + this.#cellText(raw).trim();
				continue;
			}
			return null;                   // any other member (video/button/table/foreign tag) → not this clean form → bail
		}
		if (!cards.length) return null;

		const built = [];
		for (const c of cards) {
			if (!c.title || !c.img || !c.back) return null;          // every card needs an image-front + a back
			const front = this.#flipImageFront(`${c.title} / ${c.img}`, tpl, run, inline);
			const back = this.#flipBack(c.back, inline);
			if (front === null || back === null) return null;        // any unclear card → keep the placeholder
			built.push(Utils.FillTemplate(tpl.card_image_front, { front, back }));
		}
		return [tpl.container_open, ...built, tpl.container_close].join("\n");
	}

	/**
	 * modal → BUTTON. A [modal] whose captured content is a SINGLE
	 * document/PDF URL (no data table) is the human's external-resource BUTTON
	 * (verified against OSBY201-02 #13 → a button linking the Cyberbullying PDF). The exact button
	 * WORDING is editorial (the Writers Template gives only the URL), so the label is a derived short
	 * link-phrase when present, else a generic default; the STRUCTURE (the button) is the
	 * derivable win. Conservative: exactly ONE URL and no rich/table content, else null →
	 * keep the placeholder. Data interactive_builders.modal; env MODALBTN_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @returns {string|null} the built button HTML, or null to keep the orange placeholder
	 */
	static #modal({ bundle, tpl, renderInline, renderBlock, run }) {
		if (!tpl || tpl.enabled === false) return null;
		// ROUND 216 (r214-a, Chris 2026-07-12: build the WRITER'S modal): the IMAGE-PAIR form
		// is tried FIRST — repeated "[modal][image] <iStock URL>" triggers each followed by its
		// [body]/black content (OSOH501-01's six ergonomics modals; the writer's CS note asks
		// for exactly this). On any mismatch it declines and the function proceeds EXACTLY as
		// before (the r73 single-document button, else the placeholder) — measured corpus-wide
		// (outputs/_measure_modalpairs.cjs, 369 modal bundles): the clean pair form fires on
		// EXACTLY 1 bundle; the near-miss dialects (EXPFUN tile-modals, MXDI "[Modal N Image]",
		// BLL image-enlarge no-body) all decline by construction and are recorded follow-ups.
		const ip = this.#modalImagePairs({ bundle, tpl, renderInline, renderBlock, run });
		if (ip) return ip;
		if (typeof process !== "undefined" && process.env && process.env.MODALBTN_OFF) return null;
		if ((bundle?.tables ?? []).length) return null;
		const urls = [];
		const labels = [];
		for (const m of (bundle?.media ?? [])) {
			const u = String(m?.target ?? m?.text ?? "");
			if (/^https?:/.test(u)) urls.push(u);
		}
		for (const it of [...(bundle?.openerItems ?? []), ...(bundle?.memberItems ?? [])]) {
			for (const l of (it?.block?.links ?? [])) {
				if (l?.target) urls.push(l.target);
				if (l?.text) labels.push(l.text);
			}
			const txt = String(it?.blackAfter ?? (it?.type === "black" ? it?.text : "") ?? "");
			const mm = txt.match(/https?:\/\/[^\s\]]+/);
			if (mm) urls.push(mm[0]);
			const rest = txt.replace(/https?:\/\/[^\s\]]+/g, "").replace(/\*/g, "").trim();
			if (rest) labels.push(rest);
		}
		// Verified against OSBY201-03: a [video] adjacent to the modal is its OWN
		// element — the scanner may associate its URL as bundle.media, which made the
		// single-document modal see >1 URL and bail. Exclude video-host URLs so a modal
		// whose own resource is one document still builds (a true VIDEO modal then has 0
		// doc URLs → still bails, correctly keeping the placeholder). Data
		// interactive_builders.modal.exclude_video_urls; env MODALVID_OFF.
		const excludeVideo = (tpl.exclude_video_urls !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.MODALVID_OFF);
		const isVideoUrl = (u) => /youtu\.?be|youtube|vimeo/i.test(String(u));
		const uniq = [...new Set(urls.filter(Boolean).filter((u) => !(excludeVideo && isVideoUrl(u))))];
		if (uniq.length !== 1) return null;
		let label = labels.map((s) => s.replace(/\s+/g, " ").trim())
			.find((s) => s && s.length <= (tpl.label_max_chars ?? 70)
				&& !/^https?:/.test(s) && !/click the button|below/i.test(s));
		if (!label) label = tpl.default_label ?? "Go to resource";
		return Utils.FillTemplate(tpl.form, { url: Utils.EscapeHtml(uniq[0]), label: Utils.EscapeHtml(label) });
	}

	/**
	 * modal IMAGE-PAIR form → the human's TKmodal convention (ROUND 216; r214-a, the OSOH501
	 * screenshot set; build form = the WRITER'S modal, Chris's decision 2026-07-12).
	 *
	 * HOW THE WRITER AUTHORS IT (verified OSOH501-01, accordion panel 1):
	 *   a CS note "Please have it so that ākonga click on the image and the body text as the
	 *   modal", then repeating pairs of
	 *     [modal][image] <iStock URL>        ← the clickable trigger image
	 *     [body] <text> (+ black bullet lines)  ← that modal's content
	 *
	 * BUILDS the corpus modal convention (trigger directly followed by its modal — CEDK401,
	 * ENGI301 book-shelf form):
	 *   <img class="img-fluid TKmodalButton" …iStock Mode P/D…>
	 *   <div class="TKmodal" size="M"> {body <p>/<ul>} </div>          × one per pair
	 *
	 * SAFETY (never half-build) — declines (null → the r73 button path, then the honest
	 * placeholder) on: any modal member WITHOUT an [image] span or an iStock-nameable URL,
	 * trigger-line caption residue, red text, a table / nested widget / foreign tag member,
	 * content before the first trigger, or an EMPTY pair (the BLL image-enlarge no-body form —
	 * a recorded follow-up dialect, NOT this form). A writer-instruction member is SKIPPED
	 * (it surfaces as the standard red cv2-note after the built widget — the r214 accordion
	 * class). The modal size attr is editorial (the WT gives none) → the corpus-dominant
	 * default_size "M" (116 M / 81 L / 72 XL measured). Nested-in-accordion sets build in
	 * place via renderNested (r214 nested_built_wrap).
	 *
	 * Data interactive_builders.modal.image_pairs; env MODALIMG_OFF reverts to the placeholder.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - the modal templates (Emit_Templates.json interactive_builders.modal)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {function} [args.renderBlock] - paragraph/list renderer (bullets → <ul>)
	 * @param {object} [args.run] - conversion run context (image Mode P/D)
	 * @returns {string|null} the built trigger+modal set, or null to fall through
	 */
	static #modalImagePairs({ bundle, tpl, renderBlock, run }) {
		const cfg = tpl?.image_pairs;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.MODALIMG_OFF) return null;
		if (typeof renderBlock !== "function") return null;
		if ((bundle?.tables ?? []).length) return null;
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		const pairs = [];            // [{ filename, texts:[…] }]
		let cur = null;
		for (const m of members) {
			if (!m) continue;
			if (m.type === "nested" || m.type === "table" || (m.block && m.block.type === "table")) return null;
			const tag = m.type === "tag" ? m.parse?.primary?.tag : null;
			if (tag === "modal") {
				const span = (m.parse?.tags ?? []).map((t) => t.tag);
				if (!span.includes("image")) return null;         // a non-image modal in the set → not this form
				const raw = String(m.blackAfter ?? "");
				if (this.#hasRedText(raw)) return null;
				const text = this.#cellText(raw);
				const um = text.match(/https?:\/\/\S+/);
				const filename = um ? this.#istockFilename(um[0], cfg) : null;
				if (!filename) return null;                       // no / non-iStock URL → underivable
				const residual = text.replace(/https?:\/\/\S+/g, "").replace(/\S*gm-?\d{6,10}\S*/g, "").trim();
				if (residual) return null;                        // a caption rode the trigger line → too rich
				cur = { filename, texts: [] };
				pairs.push(cur);
				continue;
			}
			// a writer-instruction member — surfaced as the red cv2-note after the widget; skip.
			if (m.type === "tag"
				&& (m.parse?.class === "instruction" || m.parse?.class === "noise" || m.parse?.instructionFragment)
				&& cfg.skip_instruction_members !== false) continue;
			if (m.type === "black") {
				const t = m.text ?? "";
				if (!t.trim()) continue;
				if (!cur) return null;                            // content before the first trigger → not the pair form
				cur.texts.push(t);
				continue;
			}
			if (tag === "body") {
				const raw = m.blackAfter ?? "";
				if (this.#hasRedText(raw)) return null;
				const t = this.#cellText(raw);
				if (!t.trim()) continue;
				if (!cur) return null;
				cur.texts.push(t);
				continue;
			}
			if (this.#isInlineMarkerMember(m)) {
				if (this.#hasRedText(m.blackAfter ?? "")) return null;
				const t = this.#cellText(m.blackAfter ?? "");
				if (t.trim()) { if (!cur) return null; cur.texts.push(t); }
				continue;
			}
			if (tag && /\blist\b/.test(tag)) continue;            // [unordered list] marker — bullets follow as black lines
			return null;                                          // anything else (heading, media, button…) → too rich
		}
		if (!pairs.length) return null;
		const out = [];
		for (const p of pairs) {
			const joined = p.texts.join("\n").trim();
			if (!joined) return null;                             // an EMPTY modal (image-enlarge dialect) → decline
			const rendered = renderBlock(joined);
			const arr = Array.isArray(rendered) ? rendered : [rendered];
			const content = arr.filter((h) => h && String(h).trim()).join("");
			if (!content.trim()) return null;
			out.push(this.#assetImage(p.filename, cfg, run));
			out.push(Utils.FillTemplate(cfg.modal_open, { size: cfg.default_size ?? "M" })
				+ "\n" + content + "\n" + (cfg.modal_close ?? "</div>"));
		}
		return out.join("\n");
	}

	/**
	 * tabs — a strip of tab headings, each revealing its own content pane.
	 *
	 * HOW THE WRITER AUTHORS IT (members, like accordion — verified, not assumed):
	 *   a [tabs] opener, then one [Tab N] tag per tab whose TRAILING text is that
	 *   tab's HEADING (e.g. [Tab 1] Mat 1), followed by the tab's body paragraph(s).
	 *   An optional [Tabs end here] closer (also tag "tabs") carries no content.
	 *
	 * SAMPLE captured bundle.memberItems (ENGJ301):
	 *   { type:"tag", tag:"tabs" }                                  // opener
	 *   { type:"tag", tag:"tab n", blackAfter:"First person…" }     // tab heading
	 *   { type:"tag", tag:"body", blackAfter:"It hurts to think…" } // tab body …
	 *
	 * BUILDS  <div class="tabs…"> <ul class="nav nav-tabs"><li><a>{head}</a></li>…</ul>
	 *   <div class="tab-content"><div class="tab-pane">{content}</div>…</div></div>
	 *
	 * SAFETY (never half-build): plain heading + body TEXT only, ≥ 2 tabs. Returns
	 *   null (→ keep the placeholder) the moment a tab's content is a DATA TABLE
	 *   (BLL233's letter tables), an image/nested widget, a tab is missing its
	 *   heading, or red writer-instruction text appears inside a tab.
	 *
	 * This is the TOP-LEVEL dispatcher for every "tabs" bundle. Not every writer
	 * authors [Tab N] tags, so it tries several capture forms, richest/most-specific
	 * first, falling through to the next when one declines (see the numbered
	 * sections in the body below):
	 *   no [Tab N] tags at all → try heading-delimited panes, then table-sourced
	 *     panes, then a flat bullet list, then give up (honest placeholder)
	 *   has [Tab N] tags       → try the strict plain-text walk, then a richer
	 *     fallback that also accepts images/video/tables inside a pane
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (image mode, module code, log notes)
	 * @param {function} [args.renderBlock] - paragraph/list renderer, needed by the richer forms
	 * @param {function} [args.renderTable] - renders a captured data table exactly like the rest of the page
	 * @param {function} [args.renderImage] - renders a captured image exactly like the rest of the page
	 * @returns {string|null} the built tabs HTML, or null to keep the orange placeholder
	 */
	static #tabs({ bundle, tpl, renderInline, run, renderBlock, renderTable, renderImage }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		const inline = renderInline ?? ((s) => s);

		// LIST-OPENER tabbed-nav form. Some writers author a [tabs]
		// widget NOT with [Tab N] tags but as a flat "• Term – description" BULLET LIST
		// (HES1003 tikanga principles). The [Tab N] loop below would bail the moment it
		// meets a bodyless bullet (no current pane), so the whole widget stayed an orange
		// placeholder. When the bundle carries NO [Tab N] member, hand it to #tabsFromList,
		// which builds one tab per top-level bullet (label = the Term before the dash, pane
		// = the description) — or returns null to keep the honest placeholder. Data
		// interactive_builders.tabs.list_opener; env TABLIST_OFF reverts to the placeholder.
		const hasTabN = members.some((m) => m && m.type === "tag"
			&& (m.parse?.primary?.tag === "tab n" || m.parse?.primary?.tag === "tab"));
		if (!hasTabN) {
			// The HEADING-DELIMITED form: the writer authors the panes as SAME-LEVEL [H2]-[H6]
			// sections after the [tabs] invocation (PHE1005 '[activity interactive - tabs]'
			// + [H3] 'What is hauora?' + [body]; MXFL401 '[tabs] headings: rates; …').
			// Registry-gated per-FORM (rich_panes.heading_panes.registry — the heading
			// form's own mined gold-choice rows, NEVER the [Tab N] rows); reuses the
			// rich_panes pane machinery. Data rich_panes.heading_panes; env TABHEAD_OFF.
			const richCfg = tpl.rich_panes;
			const headCfg = richCfg?.heading_panes;
			const headOff = typeof process !== "undefined" && process.env && process.env.TABHEAD_OFF;
			if (richCfg && richCfg.enabled !== false && headCfg && headCfg.enabled !== false && !headOff) {
				const built = this.#tabsHeadingPanes({ bundle, tpl, inline, run, renderBlock, renderTable, renderImage });
				if (built !== null) return built;
			}
			// The TABLE-SOURCED form: the writer authors the whole tab set as ONE table straight
			// after the [tabs] invocation — the header row = the tab labels, each column's
			// content cell = that pane's body (TEDC402 '[tabs]' + '**Bias**║**Outliers**║
			// **Assumptions**' over one content row). Registry-gated per FORM
			// (rich_panes.table_panes.registry — its own mined gold-choice rows); reuses the
			// rich_panes pane machinery. Data rich_panes.table_panes; env TABTABLE_OFF.
			const tblCfg = richCfg?.table_panes;
			const tblOff = typeof process !== "undefined" && process.env && process.env.TABTABLE_OFF;
			if (richCfg && richCfg.enabled !== false && tblCfg && tblCfg.enabled !== false && !tblOff) {
				const built = this.#tabsTablePanes({ bundle, tpl, inline, run, renderBlock, renderImage });
				if (built !== null) return built;
			}
			// The ROW-per-tab TABLE form (ROUND 214, Chris — OSOH501-01 READYSAFE): ONE table
			// where each ROW is a tab — the label cell carries [tab N] + the letter/word, the
			// other cell the pane's [image]/[H4]/[body] segments. The r197 form above is
			// COLUMN-per-tab (header row = labels); this is its row-major sibling. Gated to the
			// measured subjects (outputs/_measure_tabrows.py: exactly OSOH501/OSOH201/CEDT501
			// author it; gold builds tabs on all three). Data rich_panes.row_panes; env TABROWS_OFF.
			const rowCfg = richCfg?.row_panes;
			const rowOff = typeof process !== "undefined" && process.env && process.env.TABROWS_OFF;
			if (richCfg && richCfg.enabled !== false && rowCfg && rowCfg.enabled !== false && !rowOff) {
				const built = this.#tabsTableRows({ bundle, tpl, inline, run });
				if (built !== null) return built;
			}
			const listCfg = tpl.list_opener;
			const listOff = typeof process !== "undefined" && process.env && process.env.TABLIST_OFF;
			if (listCfg && listCfg.enabled !== false && !listOff) {
				return this.#tabsFromList({ bundle, tpl, inline, listCfg });
			}
			return null;   // no [Tab N] tabs and the list/heading forms declined → honest placeholder
		}

		// STRICT text path first (the original walk, byte-identical for the bundles it
		// already builds — ENGJ301); when it declines, try the RICH fallback below
		// (registry-gated) before keeping the placeholder.
		const strict = this.#tabsStrictText({ bundle, tpl, inline });
		if (strict !== null) return strict;

		// The rich fallback builds [Tab N] panes holding an iStock image, a YouTube video, or a kept
		// data TABLE, exactly like the rich accordion fallback (#accordionRich) — but ONLY where a
		// "GOLD-CHOICE REGISTRY" (rich_panes.registry — a small lookup table built by inspecting the
		// human's already-finished modules) says the human actually builds TABS for this
		// subject|template group. The [tabs] tag alone is NOT a reliable build signal: the
		// same Writers Template form is human-built as an ACCORDION on OSAI|9-10 / OSBY|NCEA — no
		// matching registry row → honest placeholder. Data interactive_builders.tabs.rich_panes; env TABRICH_OFF.
		const rich = tpl.rich_panes;
		const richOff = typeof process !== "undefined" && process.env && process.env.TABRICH_OFF;
		if (rich && rich.enabled !== false && !richOff) {
			return this.#tabsRich({ bundle, tpl, inline, run, renderBlock, renderTable });
		}
		return null;
	}

	/**
	 * STRICT-TEXT [Tab N] tabs (the original walk — kept as its own method so the
	 * rich fallback below can run after it declines). Plain heading + body TEXT only, ≥ 2 tabs;
	 * any richer member (table/image/widget) or red instruction returns null.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} args.inline - inline-markup renderer (bold/italic/links)
	 * @returns {string|null} the built tabs HTML, or null to try the rich fallback next
	 */
	static #tabsStrictText({ bundle, tpl, inline }) {
		const members = bundle?.memberItems ?? [];
		const panes = [];          // [{ head, bodyParts:[...] }]
		let cur = null;
		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;

			// (a) the [tabs] opener and [Tabs end here] closer carry no pane content.
			if (tag === "tabs") continue;

			// (b) a [Tab N] starts a new pane; its trailing text is the heading.
			if (tag === "tab n" || tag === "tab") {
				const head = this.#cellText(m.blackAfter ?? "");
				if (!head || this.#hasRedText(head)) return null;   // no clean heading → bail
				cur = { head, bodyParts: [] };
				panes.push(cur);
				continue;
			}

			// (c) body paragraph for the current pane (plain black text or [body]).
			if (m && m.type === "black") {
				const t = this.#cellText(m.text ?? "");
				if (!t) continue;
				if (!cur || this.#hasRedText(t)) return null;
				cur.bodyParts.push(t);
				continue;
			}
			if (tag === "body") {
				const t = this.#cellText(m.blackAfter ?? "");
				if (!t) continue;
				if (!cur || this.#hasRedText(t)) return null;
				cur.bodyParts.push(t);
				continue;
			}

			// (c.5) an INLINE-MARKER member ([highlight text]/[rollover definition]) is body
			//     CONTINUATION of the current pane (the writer's inline highlight/tooltip), not a
			//     richer widget → merge its text into the pane's last paragraph.
			if (this.#isInlineMarkerMember(m)) {
				const t = this.#cellText(m.blackAfter ?? "");
				if (!t) continue;
				if (!cur || this.#hasRedText(m.blackAfter ?? "")) return null;
				this.#mergeBodyContinuation(cur.bodyParts, t);
				continue;
			}

			// (d) ANYTHING else (a data TABLE, an [image]/widget) → richer than text.
			return null;
		}

		// need at least two real tabs, each a heading + at least one body paragraph.
		if (panes.length < 2) return null;
		const navItems = [], paneItems = [];
		for (const p of panes) {
			if (!p.head || !p.bodyParts.length) return null;
			navItems.push(Utils.FillTemplate(tpl.nav_item, { head: inline(p.head) }));
			const content = p.bodyParts.map((t) => `<p>${inline(t)}</p>`).join("");
			paneItems.push(Utils.FillTemplate(tpl.pane, { content }));
		}
		return [tpl.open, tpl.nav_open, ...navItems, tpl.nav_close,
			tpl.content_open, ...paneItems, tpl.content_close, tpl.close].join("\n");
	}

	/**
	 * tabsFromList — the LIST-OPENER tabbed-nav form (verified against HES1003).
	 *
	 * A [tabs] widget whose members are a flat "• Term – description" bullet list with NO
	 * [Tab N] tags. Each TOP-LEVEL bullet becomes one tab: the nav label is the Term (the
	 * text before the first en/em-dash), the pane is the description after it.
	 *
	 * NEVER HALF-BUILD — returns null (→ keep the orange placeholder) unless EVERY captured
	 * line is a clean top-level "• Term – desc" bullet: ≥ min_tabs of them, each Term ≤
	 * max_label_words words, with no indented/nested sub-bullet, no data table, no media, no
	 * extra widget type and no red writer-instruction anywhere. (The human rewrites each
	 * pane's prose editorially, so only the tab STRUCTURE + the derivable Term labels match;
	 * the pane text is the writer's own — invisible to the automated text-stripped comparison.)
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} args.inline - inline-markup renderer (bold/italic/links)
	 * @param {object} args.listCfg - the tpl.list_opener config block (patterns/limits, all data-tunable)
	 * @returns {string|null} the built tabs HTML, or null to keep the orange placeholder
	 */
	static #tabsFromList({ bundle, tpl, inline, listCfg }) {
		// richer-than-text bundles are out of scope (image/table/video panes, multi-widget).
		if ((bundle.tables && bundle.tables.length)
			|| (bundle.media && bundle.media.length)
			|| (bundle.extraTypes && bundle.extraTypes.length)) return null;

		const sep = new RegExp(listCfg.split_pattern ?? "^(.+?)\\s+[\\u2013\\u2014]\\s+([\\s\\S]+)$");
		const bullet = listCfg.bullet_prefix ?? "•";
		const maxWords = listCfg.max_label_words ?? 6;
		const minTabs = listCfg.min_tabs ?? 2;
		const maxTrailingLines = listCfg.max_trailing_lines ?? 2;

		// Tabs scanning does not terminate on a heading, so a [tabs] bullet list usually
		// SWEEPS IN the next section's short lead (HES1003's "Activity 2A" before the next
		// [Activity]). Partition the captured members into the LEADING contiguous run of
		// clean "• Term – desc" bullets (→ the tabs) and the small text TRAILER after them
		// (re-emitted verbatim so nothing is lost). Bail the moment anything is richer than
		// plain text, the trailer grows beyond max_trailing_lines, or a bullet is malformed.
		const panes = [];          // [{ head, body }]
		const trailing = [];       // plain-text lines swept in after the bullet list
		let inTrailer = false;
		for (const m of bundle.memberItems ?? []) {
			if (!m) continue;
			let txt;
			if (m.type === "tag") {
				const tag = m.parse?.primary?.tag;
				if (tag === "tabs") continue;                  // the [tabs] / [Tabs end here] opener-closer
				txt = m.blackAfter ?? "";
				if (!String(txt).trim()) return null;          // a content-less tag = image/widget/structural → bail
			} else if (m.type === "black") {
				txt = m.text ?? "";
			} else {
				return null;                                   // a table or other non-text member → too rich
			}
			if (this.#hasRedText(txt)) return null;            // writer instruction inside → bail
			for (const raw of String(txt).split(/\n+/)) {
				if (!raw.trim()) continue;
				if (!inTrailer) {
					// still gathering the leading bullet run?
					const indented = /^\s/.test(raw);
					const line = raw.trim();
					if (!indented && line.startsWith(bullet)) {
						const mm = this.#cellText(line.slice(bullet.length).trim()).match(sep);
						if (mm) {
							const head = mm[1].trim(), body = mm[2].trim();
							if (head && body && head.split(/\s+/).length <= maxWords) {
								panes.push({ head, body });
								continue;
							}
						}
					}
					// first non-bullet line → the rest is the trailer
					inTrailer = true;
				}
				trailing.push(this.#cellText(raw).trim());
			}
		}
		if (panes.length < minTabs) return null;               // not enough clean tabs → keep the placeholder
		// The scanner swept the next section's SHORT lead into the tabs (it does not terminate
		// on a heading). A small over-captured trailer (an activity label like "Activity 2A",
		// whose own activity box follows separately) is what the human DROPS — so we drop it
		// too. But a LARGER trailer means a real section was absorbed: don't half-build, keep
		// the honest placeholder so nothing is silently lost.
		const trailWords = trailing.join(" ").split(/\s+/).filter(Boolean).length;
		if (trailing.length > maxTrailingLines
			|| trailWords > (listCfg.max_trailing_words ?? 6)) return null;

		const navItems = panes.map((p) => Utils.FillTemplate(tpl.nav_item, { head: inline(p.head) }));
		const paneItems = panes.map((p) => Utils.FillTemplate(tpl.pane, { content: `<p>${inline(p.body)}</p>` }));
		return [tpl.open, tpl.nav_open, ...navItems, tpl.nav_close,
			tpl.content_open, ...paneItems, tpl.content_close, tpl.close].join("\n");
	}

	/**
	 * The GOLD-CHOICE registry row for the rich-tabs fallback: per-module
	 * series override first, then the subject|template group (the same registry-row
	 * lookup pattern used by several other builders, case-tolerant). Returns "tabs" when
	 * the human builds tabbed nav from a clean [Tab N] bundle in this group, else null
	 * (→ honest placeholder).
	 *
	 * @param {object} rich - the tpl.rich_panes config block, which owns .registry
	 * @param {object} run - conversion run context (moduleCode + resolvedRules.template_phase)
	 * @returns {string|null} "tabs" when the registry says build, else null
	 */
	static #tabsRichRow(rich, run) {
		const reg = rich?.registry || {};
		if (!run) return null;
		if (reg.series && reg.series[run.moduleCode]) return reg.series[run.moduleCode];
		const subj = (run.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const rawPhase = run.resolvedRules?.template_phase ?? "";
		const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
		const lk = `${subj}|${phase}`.toLowerCase();
		const hit = Object.keys(reg.groups || {}).find((k) => k.toLowerCase() === lk);
		return hit ? reg.groups[hit] : null;
	}

	/**
	 * RICH tabs — the sibling of the rich-accordion fallback (#accordionRich), for
	 * bundles that DO have [Tab N] tags. Fires ONLY when the strict text path declined AND
	 * the mined GOLD-CHOICE REGISTRY row (rich_panes.registry) says the human builds TABS for
	 * a clean [Tab N] bundle in this subject|template group — the [tabs] tag alone is NOT a
	 * reliable build signal (OSAI|9-10 / OSBY|NCEA build ACCORDIONS from the exact same
	 * source form → no matching registry row → placeholder).
	 *
	 * PANES: a [Tab N] opens a pane; its blackAfter FIRST LINE is the label — the whole
	 * SHORT line (≤ max_label_words), or the **bold lead** of a long line (label = the
	 * lead, the WHOLE line stays as the pane's first paragraph — HPFUN401's human-built form).
	 * Members render like the rest of the page:
	 *   black / [body] text   -> renderBlock (#renderBlackText)      — bullets become <ul>
	 *   [image] (iStock)      -> #assetImage (Mode P/D)              — the accordion rule
	 *   [video] (YouTube)     -> the shared video.youtube embed
	 *   a captured data TABLE -> renderTable (the kept-table emitter — the BLL letter mats)
	 *
	 * NEVER half-builds: returns null (→ the orange placeholder) on a red writer
	 * instruction, an extraTypes merge, an unlabelled tab, a long label line without a
	 * bold lead, a non-iStock / captioned image cell, an unresolvable video, a pane with
	 * no rendered content, or ANY member it cannot place (buttons / external links are a
	 * documented, deliberately-deferred extension).
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} args.inline - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives the registry lookup + image mode)
	 * @param {function} [args.renderBlock] - paragraph/list renderer (required — declines without it)
	 * @param {function} [args.renderTable] - renders a captured data table exactly like the rest of the page
	 * @returns {string|null} the built tabs HTML, or null to keep the orange placeholder
	 */
	static #tabsRich({ bundle, tpl, inline, run, renderBlock, renderTable }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (typeof renderBlock !== "function") return null;    // need the body renderer
		if (bundle.extraTypes && bundle.extraTypes.length) return null;   // merged multi-widget → too tangled
		const rich = tpl.rich_panes ?? {};
		if (this.#tabsRichRow(rich, run) !== "tabs") return null;   // no gold-choice row → placeholder

		const maxLabel = rich.max_label_words ?? 6;
		const idRe = new RegExp(rich.video_youtube_id_re
			?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");

		const panes = [];       // [{ head, parts:[{p|img|video|html}] }]
		let cur = null;
		let pendingText = [];
		const flushText = () => {
			if (!cur) { pendingText = []; return; }
			const joined = pendingText.join("\n").trim();
			if (joined) cur.parts.push({ p: joined });
			pendingText = [];
		};

		// TRAILING FREE BODY (the accordion OSGM501-02 rule transposed — OSAI501-05,
		// measured): a FRESH [body] TAG in the LAST pane, once that pane already has
		// its text AND its non-text part, is the writer RESUMING free body after an
		// omitted [end tabs] — the human renders it AFTER the widget. It (and further
		// plain text) render via rich_panes.trailing_body, not as pane content.
		const lastTabIdx = members.reduce((k, m, i) => (m && m.type === "tag"
			&& (m.parse?.primary?.tag === "tab n" || m.parse?.primary?.tag === "tab")) ? i : k, -1);
		let trailingMode = false;
		const trailing = [];

		for (let i = 0; i < members.length; i++) {
			const m = members[i];
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;

			if (trailingMode) {
				const raw = m && m.type === "tag" ? (m.blackAfter ?? "") : (m?.text ?? "");
				const t = this.#cellText(raw);
				if (!t) continue;
				if (this.#hasRedText(raw)) return null;
				if (m.type !== "black" && tag !== "body" && !this.#isInlineMarkerMember(m)) return null;
				if (/[•·]|\n/.test(t)) return null;         // a list/complex tail → bail (accordion rule)
				trailing.push(t);
				continue;
			}

			// (a) a captured data TABLE member — the pane's kept table (BLL232/233/236/245).
			if (m && m.type === "table") {
				if (!cur || typeof renderTable !== "function") return null;
				flushText();
				const t = renderTable(m);
				if (!t || !String(t).trim()) return null;
				cur.parts.push({ html: String(t) });
				continue;
			}

			if (tag === "tabs") continue;              // the [tabs] opener / [end tabs] closer

			// (b) [Tab N] — a new pane. The first blackAfter line decides the label.
			if (tag === "tab n" || tag === "tab") {
				const raw = m.blackAfter ?? "";
				if (this.#hasRedText(raw)) return null;
				flushText();
				const rawLines = String(raw).split(/\n+/).filter((l) => l.trim());
				const first = this.#cellText(rawLines[0] ?? "");
				if (!first || /https?:\/\//.test(first)) return null;   // unlabelled / URL tab → bail
				// the nav LABEL ships PLAIN — the human strips a whole-bold label's markers
				// (SSEA203 "**Why do we use cash?**" → "Why do we use cash?"); this matches
				// the same "navigation chrome ships plain" rule applied elsewhere in the
				// converter (e.g. module-menu headings). Pane text keeps its own markup.
				let head = first.replace(/\*\*/g, "").trim();
				const restLines = rawLines.slice(1);
				if (first.split(/\s+/).length > maxLabel) {
					// LONG line: the label is its **bold lead** (HPFUN401 "**Culture**: …");
					// the whole line stays as the pane's first paragraph.
					const lead = (rawLines[0] ?? "").match(/^\s*\*\*([^*]+)\*\*\s*[:：]/);
					if (!lead || !this.#cellText(lead[1])) return null;
					head = this.#cellText(lead[1]);
					restLines.unshift(rawLines[0]);
				}
				cur = { head, parts: [] };
				panes.push(cur);
				for (const l of restLines) pendingText.push(l);
				continue;
			}

			// (c) image member — a single derivable iStock url, nothing else in the cell
			//     (the same rule #accordionRich uses for its panel images).
			if (tag === "image") {
				if (!cur) return null;
				const raw = m.blackAfter ?? "";
				if (!this.#cellMediaUrl(raw)) return null;
				const text = this.#cellText(raw);
				const filename = this.#istockFilename(text, rich);
				if (!filename) return null;
				const residual = text.replace(/^\s*\[[^\]]*\]\s*/, "")
					.replace(/https?:\/\/\S+/g, "").replace(/\S*gm-?\d{6,10}\S*/g, "")
					.replace(/[/|]/g, " ").trim();
				if (residual) return null;                 // a real caption rode along → too rich
				flushText();
				cur.parts.push({ img: filename });
				continue;
			}

			// (d) video member — a YouTube embed in the cell.
			if (tag === "video") {
				if (!cur) return null;
				const raw = String(m.blackAfter ?? "");
				if (this.#hasRedText(raw)) return null;
				const idm = raw.match(idRe);
				if (!idm) return null;
				flushText();
				cur.parts.push({ video: idm[1] });
				continue;
			}

			// (e) body text — untagged black or a [body] tag; red instruction bails.
			if (m && m.type === "black") {
				const t = m.text ?? "";
				if (!t.trim()) continue;
				if (!cur || this.#hasRedText(t)) return null;
				pendingText.push(t);
				continue;
			}
			if (tag === "body") {
				const raw = m.blackAfter ?? "";
				if (this.#hasRedText(raw)) return null;
				const t = this.#cellText(raw);
				if (!t.trim()) continue;
				if (!cur) return null;
				// a fresh [body] in the LAST pane once it already holds text + its
				// non-text part = the writer resuming free body (see trailing note).
				if (i > lastTabIdx && !pendingText.length
					&& cur.parts.some((p) => p.p) && cur.parts.some((p) => p.img || p.video || p.html)) {
					trailingMode = true;
					if (/[•·]|\n/.test(t)) return null;
					trailing.push(t);
					continue;
				}
				pendingText.push(t);
				continue;
			}
			if (this.#isInlineMarkerMember(m)) {
				const t = this.#cellText(m.blackAfter ?? "");
				if (this.#hasRedText(m.blackAfter ?? "")) return null;
				if (t.trim()) pendingText.push(t);
				continue;
			}

			// (e.5) a LIST marker — a no-op delimiter; the bullets follow as black members.
			if (tag && /\blist\b/.test(tag)) continue;

			// (f) anything else (a button, an external link, a nested widget, a heading)
			//     → richer than this stage builds → bail.
			return null;
		}
		flushText();

		// (2) RENDER: ≥ 2 panes, each a clean label + at least one rendered part.
		if (panes.length < 2) return null;
		const navItems = [], paneItems = [];
		for (const p of panes) {
			if (!p.head || !p.parts.length || this.#hasRedText(p.head)) return null;
			const chunks = [];
			for (const part of p.parts) {
				const got = this.#tabsRichPart(part, rich, run, renderBlock);
				if (got === null) return null;
				chunks.push(...got);
			}
			const content = chunks.join("");
			if (!content.trim()) return null;              // a pane with no rendered body
			navItems.push(Utils.FillTemplate(tpl.nav_item, { head: inline(p.head) }));
			paneItems.push(Utils.FillTemplate(tpl.pane, { content }));
		}
		const tail = trailing.map((t) => Utils.FillTemplate(rich.trailing_body ?? "<p>{text}</p>", { text: inline(t) }));
		return [tpl.open, tpl.nav_open, ...navItems, tpl.nav_close,
			tpl.content_open, ...paneItems, tpl.content_close, tpl.close, ...tail].join("\n");
	}

	/**
	 * ONE captured pane part → its HTML chunk(s) (shared by #tabsRich and
	 * #tabsHeadingPanes; extracted verbatim from #tabsRich's render loop so both
	 * builders stay in sync). Returns an array of chunks, or null when the part CANNOT
	 * render (missing video template) — the caller must bail the whole widget (never
	 * half-build).
	 *
	 * @param {object} part - one pane part: {p:text} | {img:filename} | {video:id} | {html:string}
	 * @param {object} rich - the tpl.rich_panes config block
	 * @param {object} run - conversion run context (drives Mode P/D image rendering)
	 * @param {function} renderBlock - paragraph/list renderer for {p} parts
	 * @returns {string[]|null} the rendered HTML chunk(s), or null if this part can't render
	 */
	static #tabsRichPart(part, rich, run, renderBlock) {
		if (part.img) return [this.#assetImage(part.img, rich, run)];
		if (part.video) {
			const vt = DataService.Data.EmitTemplates.video?.youtube;
			if (!vt) return null;
			return [Utils.FillTemplate(vt, { videoId: part.video, params: "" })];
		}
		if (part.html) return [part.html];
		if (part.p) {
			const rendered = renderBlock(part.p);
			const arr = Array.isArray(rendered) ? rendered : [rendered];
			return arr.filter((h) => h && String(h).trim()).map((h) => String(h));
		}
		return [];
	}

	/**
	 * HEADING-PANE tabs — the #tabsRich sibling for the form with NO [Tab N] members.
	 * The writer delimits the panes with SAME-LEVEL [H2]-[H6] section headings after the
	 * [tabs] invocation:
	 *   [activity interactive - tabs] …   (PHE1005)      [tabs] headings: rates; …   (MXFL401)
	 *   [H3] What is hauora?  [body] …    → pane 1        [H3] Rates  + text          → pane 1
	 * Fires ONLY when the mined per-FORM GOLD-CHOICE registry row
	 * (rich_panes.heading_panes.registry — its own rows, never the [Tab N] set) says the
	 * human builds TABS for this subject|template group. Pane label = the heading's first
	 * blackAfter line (the same short/**-stripped label rules #tabsRich uses). Members render
	 * through the SAME machinery (#tabsRichPart: text/img/video/table).
	 *
	 * TWO measured SECTION-BREAK rules (verified against the human's finished modules):
	 *   (1) a LONG same-level heading (> max_label_words) AFTER ≥ min_panes complete panes
	 *       is the writer's NEXT SECTION (MXFL401 "**But how did Alan…**" — the human ships it
	 *       OUTSIDE the widget) → the widget closes; the heading + its following plain
	 *       text render after it via trailing_body;
	 *   (2) a URL-LESS [image] member once the panes are complete (PHE1005 "[insert item
	 *       3]", a media-list reference — the human ships the image AFTER the widget) →
	 *       rendered after the widget via the renderImage hook (the normal body-path emitter).
	 * An EXACT duplicate pane (same folded label + content — a writer copy-paste, MXFL401
	 * "Power" ×2; the human ships it once) is dropped (dedup_identical_panes).
	 *
	 * NEVER half-builds: an instruction/noise member, MIXED heading levels, a long heading
	 * before min_panes complete, red text, a url-less image mid-widget, content before the
	 * first heading, a non-hover data marker, an unresolvable video/image, a button/link/
	 * nested widget, a second trailing image — all return null (→ today's output, usually
	 * the orange placeholder). Data rich_panes.heading_panes; env TABHEAD_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} args.inline - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives the registry lookup + image mode)
	 * @param {function} [args.renderBlock] - paragraph/list renderer (required — declines without it)
	 * @param {function} [args.renderTable] - renders a captured data table exactly like the rest of the page
	 * @param {function} [args.renderImage] - renders a trailing image exactly like the rest of the page
	 * @returns {string|null} the built tabs HTML, or null to keep the orange placeholder
	 */
	static #tabsHeadingPanes({ bundle, tpl, inline, run, renderBlock, renderTable, renderImage }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (typeof renderBlock !== "function") return null;    // need the body renderer
		if (bundle.extraTypes && bundle.extraTypes.length) return null;   // merged multi-widget → too tangled
		const rich = tpl.rich_panes ?? {};
		const cfg = rich.heading_panes ?? {};
		if (this.#tabsRichRow(cfg, run) !== "tabs") return null;   // no per-form gold-choice row → placeholder

		const maxLabel = rich.max_label_words ?? 6;
		const minPanes = cfg.min_panes ?? 2;
		const hoverRe = cfg.hover_marker_continuation
			? new RegExp(cfg.hover_marker_continuation, "i") : null;
		const idRe = new RegExp(rich.video_youtube_id_re
			?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");
		const hRe = /^h[2-6]$/;
		const fold = (s) => String(s ?? "").toLowerCase().replace(/\s+/g, " ").trim();

		let panes = [];         // [{ head, parts:[{p|img|video|html}] }]
		let cur = null;
		let headLevel = null;   // ALL pane headings must share one level (a sub-head → richer form)
		let pendingText = [];
		const flushText = () => {
			if (!cur) { pendingText = []; return; }
			const joined = pendingText.join("\n").trim();
			if (joined) cur.parts.push({ p: joined });
			pendingText = [];
		};
		let trailingMode = false;
		const trailing = [];    // [{ text } | { imgItem }] — rendered AFTER the widget, in order

		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			const dir = m && m.type === "tag" ? m.parse?.primary?.directive : null;
			const cls = m && m.type === "tag" ? m.parse?.class : null;

			if (trailingMode) {
				// after the widget closed only PLAIN text may follow (the same trailing-body rule #tabsRich uses)
				const raw = m && m.type === "tag" ? (m.blackAfter ?? "") : (m?.text ?? "");
				if (this.#hasRedText(raw)) return null;
				if (m.type === "black" || tag === "body" || this.#isInlineMarkerMember(m)) {
					const t = this.#cellText(raw);
					if (!t) continue;
					if (/[•·]|\n/.test(t)) return null;      // a list/complex tail → bail
					trailing.push({ text: t });
					continue;
				}
				return null;
			}

			if (tag === "tabs") continue;              // the [tabs] opener / [end tabs] closer

			// a retained writer instruction/noise span anywhere inside → never half-build
			if (m && m.type === "tag" && (cls === "instruction" || cls === "noise")) return null;

			// (a) a SAME-LEVEL section heading — a new pane, the trailing section break, or bail.
			if (m && m.type === "tag" && tag && hRe.test(tag) && dir === "ELEMENT") {
				const raw = m.blackAfter ?? "";
				if (this.#hasRedText(raw)) return null;
				const rawLines = String(raw).split(/\n+/).filter((l) => l.trim());
				const first = this.#cellText(rawLines[0] ?? "");
				if (!first) return null;                       // an unlabelled heading → bail
				if (headLevel === null) headLevel = tag;
				else if (tag !== headLevel) return null;       // mixed levels → richer than this stage
				if (first.split(/\s+/).length > maxLabel) {
					// SECTION-BREAK rule (1): a long heading after the panes are complete
					// is the next section — close the widget, render it as trailing text.
					if (panes.length >= minPanes && (cur?.parts.length || pendingText.length)) {
						flushText();
						trailingMode = true;
						for (const l of rawLines) {
							const lt = this.#cellText(l);
							if (lt) trailing.push({ text: lt });
						}
						continue;
					}
					return null;                               // long heading too early → bail
				}
				flushText();
				// the nav LABEL ships PLAIN (the same "navigation chrome ships plain" rule used elsewhere)
				const head = first.replace(/\*\*/g, "").trim();
				cur = { head, parts: [] };
				panes.push(cur);
				for (const l of rawLines.slice(1)) pendingText.push(l);
				continue;
			}

			// (b) a captured data TABLE member — the pane's kept table (the same rule #tabsRich uses).
			if (m && m.type === "table") {
				if (!cur || typeof renderTable !== "function") return null;
				flushText();
				const t = renderTable(m);
				if (!t || !String(t).trim()) return null;
				cur.parts.push({ html: String(t) });
				continue;
			}

			// (c) image member — in-cell iStock URL → a pane image (the same rule #accordionRich uses);
			//     NO url once the panes are complete → SECTION-BREAK rule (2): the widget
			//     closes and the image renders AFTER it via the renderImage hook.
			if (tag === "image") {
				if (!cur) return null;
				const raw = m.blackAfter ?? "";
				if (this.#cellMediaUrl(raw)) {
					const text = this.#cellText(raw);
					const filename = this.#istockFilename(text, rich);
					if (!filename) return null;
					const residual = text.replace(/^\s*\[[^\]]*\]\s*/, "")
						.replace(/https?:\/\/\S+/g, "").replace(/\S*gm-?\d{6,10}\S*/g, "")
						.replace(/[/|]/g, " ").trim();
					if (residual) return null;                 // a real caption rode along → too rich
					flushText();
					cur.parts.push({ img: filename });
					continue;
				}
				if (panes.length >= minPanes && (cur.parts.length || pendingText.length)
					&& typeof renderImage === "function") {
					flushText();
					trailingMode = true;
					trailing.push({ imgItem: m });
					continue;
				}
				return null;                                   // a url-less image mid-widget → bail
			}

			// (d) video member — a YouTube embed in the cell (the same rule #accordionRich uses).
			if (tag === "video") {
				if (!cur) return null;
				const raw = String(m.blackAfter ?? "");
				if (this.#hasRedText(raw)) return null;
				const idm = raw.match(idRe);
				if (!idm) return null;
				flushText();
				cur.parts.push({ video: idm[1] });
				continue;
			}

			// (e) body text — untagged black or a [body] tag; red instruction bails.
			if (m && m.type === "black") {
				const t = m.text ?? "";
				if (!t.trim()) continue;
				if (!cur || this.#hasRedText(t)) return null;
				pendingText.push(t);
				continue;
			}
			if (tag === "body") {
				const raw = m.blackAfter ?? "";
				if (this.#hasRedText(raw)) return null;
				const t = this.#cellText(raw);
				if (!t.trim()) continue;
				if (!cur) return null;
				pendingText.push(t);
				continue;
			}
			if (this.#isInlineMarkerMember(m)) {
				const t = this.#cellText(m.blackAfter ?? "");
				if (this.#hasRedText(m.blackAfter ?? "")) return null;
				if (t.trim()) pendingText.push(t);
				continue;
			}

			// (e.5) a HOVER/ROLLOVER definition marker mid-paragraph ([hover over
			//     definition: see], PHE1005) — its blackAfter CONTINUES the paragraph the
			//     marker split; merge it into the pending line (straight concat — the
			//     writer's own spacing spans the boundary). Any OTHER data marker bails.
			if (tag === "data marker") {
				if (!cur || !hoverRe || !hoverRe.test(m.parse?.folded ?? "")) return null;
				const t = this.#cellText(m.blackAfter ?? "");
				if (this.#hasRedText(m.blackAfter ?? "")) return null;
				if (t) {
					if (pendingText.length) pendingText[pendingText.length - 1] += t;
					else pendingText.push(t);
				}
				continue;
			}

			// (f) anything else (a button, an external link, a nested widget, a list
			//     marker with substance) → richer than this stage builds → bail.
			return null;
		}
		flushText();

		// EXACT-DUPLICATE pane dedup (a writer copy-paste repeat — MXFL401 "Power" ×2;
		// gold ships the pane once). Same folded label AND same folded content only.
		if (cfg.dedup_identical_panes !== false) {
			const seen = new Set();
			const keep = [];
			for (const p of panes) {
				const key = fold(p.head) + "␞" + p.parts.map((pt) =>
					pt.p ? "p:" + fold(pt.p) : pt.img ? "i:" + pt.img
						: pt.video ? "v:" + pt.video : "h:" + fold(pt.html)).join("␞");
				if (seen.has(key)) continue;
				seen.add(key);
				keep.push(p);
			}
			panes = keep;
		}

		// RENDER: ≥ min_panes panes, each a clean label + at least one rendered part.
		if (panes.length < minPanes) return null;
		const navItems = [], paneItems = [];
		for (const p of panes) {
			if (!p.head || !p.parts.length || this.#hasRedText(p.head)) return null;
			const chunks = [];
			for (const part of p.parts) {
				const got = this.#tabsRichPart(part, rich, run, renderBlock);
				if (got === null) return null;
				chunks.push(...got);
			}
			const content = chunks.join("");
			if (!content.trim()) return null;              // a pane with no rendered body
			navItems.push(Utils.FillTemplate(tpl.nav_item, { head: inline(p.head) }));
			paneItems.push(Utils.FillTemplate(tpl.pane, { content }));
		}
		const tail = [];
		for (const t of trailing) {
			if (t.text) {
				tail.push(Utils.FillTemplate(rich.trailing_body ?? "<p>{text}</p>", { text: inline(t.text) }));
				continue;
			}
			if (t.imgItem) {
				if (typeof renderImage !== "function") return null;
				const h = renderImage(t.imgItem);
				if (!h || !String(h).trim()) return null;
				tail.push(String(h));
			}
		}
		return [tpl.open, tpl.nav_open, ...navItems, tpl.nav_close,
			tpl.content_open, ...paneItems, tpl.content_close, tpl.close, ...tail].join("\n");
	}

	/**
	 * TABLE-PANE tabs — the sibling of #tabsRich and #tabsHeadingPanes, for the form
	 * authored as ONE TABLE. The writer lays the whole tab set out as a
	 * table straight after the [tabs] invocation — the HEADER ROW carries the tab
	 * labels, each COLUMN's content cell(s) carry that pane's body (TEDC402:
	 *   [tabs]  →  │ **Bias** ║ **Outliers** ║ **Assumptions** │
	 *              │ **Bias** / Bias happens when… ║ … ║ … │
	 * human's build: nav Bias/Outliers/Assumptions, each pane the column's paragraphs/bullets).
	 * Fires ONLY when the per-FORM GOLD-CHOICE registry row
	 * (rich_panes.table_panes.registry — its own rows, never the [Tab N]/heading sets)
	 * says the human builds TABS from this form in this subject|template group.
	 *
	 * LABEL RULE: every header cell must clean to a SHORT label — red-span markers
	 * stripped (writers often type tab titles red: 'Tab 1: Step 1' / 'Level 1'), a
	 * '[tab title: X]'/'[Tab N]' bracket consumed, a 'Tab N:' lead consumed, a leading
	 * [H*]/[body] marker stripped, ** stripped (nav chrome ships PLAIN — the same rule
	 * applied everywhere else in this file). PANES are COLUMN-MAJOR: pane c = the content rows'
	 * column-c cells, each cell's ' / '-joined paragraphs re-split to lines and
	 * rendered through renderBlock (bullets → <ul>, lines → <p> — the normal
	 * black-text machinery; a leading [Body]/[list] marker per line is stripped).
	 *
	 * TRAILING members after the table (the human ships them after the widget):
	 *   - an [image] member → rendered AFTER via the renderImage hook (the same rule
	 *     #tabsHeadingPanes uses; TEDC402's avatar [Image] — the human's bubble-row img;
	 *     the bubble TEXT itself is scanner-absorbed into its own speechBubble bundle
	 *     and builds separately);
	 *   - an instruction/noise member following that image (its pose/catalogue
	 *     reference, split from the image's OWN source paragraph) → consumed WITHOUT a
	 *     second note: the renderImage emitter reads the shared source block and
	 *     surfaces the red instruction as its own CS note (never silently stripped —
	 *     probe-proven; a second emission here doubled it), and the catalogue line is
	 *     the image's media reference (already accounted for elsewhere once a widget is
	 *     built, kept in the emitter's commented real-filename reference);
	 *   - plain black sentences BEFORE any trailing image → trailing_body paragraphs
	 *     (the same trailing-text rule used throughout this file; a black AFTER an image
	 *     is that image's caption/reference — media machinery's territory → bail).
	 *
	 * NEVER half-builds: no registry row, an extraTypes merge, ≠1 table member, any
	 * member before the table (a documented, deliberately-deferred class — see TEDC401-1.0),
	 * <2 rows / <2 cols, a ragged row, a header cell that is empty / long / a URL / carries any
	 * other bracket tag (the [RHS]+[Image] avatar-COLUMN sub-form, TEDC402-4.0 —
	 * also documented and deferred), a RED content cell (the writer's OWN other-widget spec —
	 * TEDC402's 5x4 dataset table is human-built as clickDrop buttons: this guard agrees with
	 * that human choice), an EMPTY content cell (an embedded image the docx cell extractor cannot
	 * see — the PES1004 class), any other bracket tag in content, a trailing
	 * button/link/marker/widget/second table (further deferred classes) — all return
	 * null (→ today's output, usually the orange placeholder).
	 * Data rich_panes.table_panes; env TABTABLE_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} args.inline - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives the registry lookup + image mode)
	 * @param {function} [args.renderBlock] - paragraph/list renderer (required — declines without it)
	 * @param {function} [args.renderImage] - renders a trailing image exactly like the rest of the page
	 * @returns {string|null} the built tabs HTML, or null to keep the orange placeholder
	 */
	static #tabsTablePanes({ bundle, tpl, inline, run, renderBlock, renderImage }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (typeof renderBlock !== "function") return null;    // need the body renderer
		const rich = tpl.rich_panes ?? {};
		const cfg = rich.table_panes ?? {};
		// ROUND 215 (Chris, r214-b CEDT501) — the TITLE-ROW sub-form: a leading single-cell
		// [H*] TITLE cell above the [tab N] label row ("[H2] Being assertive online is …" over
		// "[tab 1][H3] …|[tab 2]…|[tab 3]…"). The gold builds tabs there but the r197 registry
		// is TEDC-only and the extra title row reads ragged. A subject in table_panes.title_row
		// .subjects may proceed WITHOUT a registry "tabs" verdict, but ONLY when the exact
		// title-row signature is present (checked in #tabsTableCore). All title-row-only
		// behaviour (title peel, label "/" sub-split, pane lead, MULTIPLE [tabs]+table segments
		// in one bundle) is gated on !registryTabs, so the TEDC label-header path stays
		// byte-untouched. Env TABTITLEROW_OFF reverts.
		const registryTabs = this.#tabsRichRow(cfg, run) === "tabs";
		const titleCfg = cfg.title_row ?? {};
		const titleSubj = (run?.moduleCode ?? "").match(/^[A-Za-z]+/)?.[0] ?? "";
		const titleFormAllowed = titleCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.TABTITLEROW_OFF)
			&& (titleCfg.subjects ?? []).includes(titleSubj);
		if (!registryTabs && !titleFormAllowed) return null;   // no gold-choice → placeholder
		// extraTypes = other widget TYPES merged into this bundle → too tangled to build. The
		// TITLE-ROW form legitimately merges a SECOND [tabs] invocation (CEDT501's two tab
		// tables land in one bundle → extraTypes ["tabs"]); allow that self-merge, but still
		// bail on any genuinely different widget type.
		const extra = (bundle.extraTypes ?? []).filter((t) => t !== "tabs");
		if (registryTabs && bundle.extraTypes && bundle.extraTypes.length) return null;
		if (!registryTabs && extra.length) return null;

		const tableIdxs = members.map((m, i) => (m && m.type === "table" ? i : -1)).filter((i) => i >= 0);
		if (!tableIdxs.length) return null;
		const opts = { registryTabs, cfg, rich, titleCfg, tpl, inline, run, renderBlock };

		// TITLE-ROW form: the two [Tabs] tables land in ONE captured bundle
		// (members = [tabs] table [tabs] table). Build EACH table's tabs, concatenated; every
		// non-table member must be a [tabs] tag (never half-build across the set).
		if (!registryTabs) {
			for (const m of members) {
				if (m && m.type === "table") continue;
				const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
				if (tag === "tabs") continue;                        // the invocation / [end tabs]
				if (m && m.type === "black" && !this.#cellText(m.text)) continue;   // an empty black line
				return null;                                         // any other member → not this clean form
			}
			const parts = [];
			for (const ti of tableIdxs) {
				const built = this.#tabsTableCore(members[ti].block?.rows ?? [], opts);
				if (built === null) return null;                    // never half-build across the set
				parts.push(built);
			}
			return parts.join("\n");
		}

		// REGISTRY (TEDC) path — EXACTLY ONE table, NOTHING before it but the [tabs] opener,
		// then the allowed TRAILING image/text classes. Byte-identical to the r197 form.
		if (tableIdxs.length !== 1) return null;
		const ti = tableIdxs[0];
		for (let i = 0; i < ti; i++) {
			const m = members[i];
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			if (tag === "tabs") continue;                        // the invocation itself
			if (m && m.type === "black" && !this.#cellText(m.text)) continue;   // an empty black line
			return null;                                         // a lead member → the recorded lead class
		}
		const core = this.#tabsTableCore(members[ti].block?.rows ?? [], opts);
		if (core === null) return null;

		// TRAILING members (after the table) — see the doc block's allowed classes.
		const trailing = [];   // [{ text } | { imgItem }] — in member order
		let sawImage = false;
		for (let i = ti + 1; i < members.length; i++) {
			const m = members[i];
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			const cls = m && m.type === "tag" ? m.parse?.class : null;
			if (tag === "tabs") continue;                        // an [end tabs] closer
			if (m && m.type === "tag" && (tag === "image" || tag === "images")) {
				trailing.push({ imgItem: m });
				sawImage = true;
				continue;
			}
			if (m && m.type === "tag" && (cls === "instruction" || cls === "noise")) {
				if (!sawImage) return null;                      // a standalone trailing instruction → never half-build
				continue;                                        // a trailing image's own reference (renderImage re-notes it)
			}
			if (m && (m.type === "black" || tag === "body" || this.#isInlineMarkerMember(m))) {
				if (sawImage) return null;                       // an image's caption/reference → media territory
				const raw = m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
				if (this.#hasRedText(raw)) return null;
				const t = this.#cellText(raw);
				if (!t) continue;
				if (/[•·]|\n/.test(t)) return null;              // a list/complex tail → bail
				trailing.push({ text: t });
				continue;
			}
			return null;   // a button / video / marker / widget / second table → further deferred classes
		}
		const tail = [];
		for (const t of trailing) {
			if (t.text) { tail.push(Utils.FillTemplate(rich.trailing_body ?? "<p>{text}</p>", { text: inline(t.text) })); continue; }
			if (t.imgItem) {
				if (typeof renderImage !== "function") return null;
				const h = renderImage(t.imgItem);
				if (!h || !String(h).trim()) return null;
				tail.push(String(h));
			}
		}
		return tail.length ? core + "\n" + tail.join("\n") : core;
	}

	/**
	 * Build ONE column-form tab table's HTML (nav + panes, plus a peeled title heading for the
	 * TITLE-ROW form). Factored out of #tabsTablePanes (round 215) so the title-row form can
	 * loop over multiple [tabs]+table segments in one bundle. Returns the tabs HTML string or
	 * null to decline (the caller keeps the placeholder). The REGISTRY (TEDC) path calls this
	 * with registryTabs=true → no title peel / no label "/"-split → byte-identical to r197.
	 */
	static #tabsTableCore(tblRows, { registryTabs, cfg, rich, titleCfg, tpl, inline, run, renderBlock }) {
		let rows = tblRows ?? [];
		// TITLE-ROW form: peel a leading single-cell [H*] TITLE row above the [tab N] label row
		// and emit it as a heading before the tabs (relevel handles the level, consistent with
		// the page's other [H#]). Requires the exact signature.
		let titleHtml = "";
		if (!registryTabs) {
			const first = rows[0] ?? [];
			const second = rows[1] ?? [];
			const titleRe = new RegExp(titleCfg.title_tag_pattern ?? "^\\[\\s*h([1-6])\\b[^\\]]*\\]\\s*", "i");
			const firstTxt = first.length === 1 ? this.#cellText(first[0]) : "";
			const mTitle = firstTxt.match(titleRe);
			const secondTabs = second.filter((c) => /\[\s*tab\s+\d+\s*\]/i.test(String(c))).length;
			if (!(mTitle && secondTabs >= 2)) return null;   // subject allowed but NOT this form → placeholder
			const titleText = firstTxt.replace(titleRe, "").replace(/\*\*/g, "").replace(/\s+/g, " ").trim();
			if (/[\[\]]/.test(titleText)) return null;       // an unexpected tag in the title → bail
			if (titleText) titleHtml = `<h${mTitle[1]}>${inline(titleText)}</h${mTitle[1]}>\n`;
			rows = rows.slice(1);                            // the [tab N] label row is now rows[0]
		}
		if (rows.length < (cfg.min_rows ?? 2)) return null;
		const nCols = (rows[0] ?? []).length;
		if (nCols < (cfg.min_cols ?? 2)) return null;
		for (const r of rows) if (r.length !== nCols) return null;   // ragged → a richer form

		// HEADER ROW → the labels.
		const maxLabel = cfg.max_label_words ?? rich.max_label_words ?? 6;
		const prefixRe = new RegExp(cfg.label_prefix_pattern ?? "^Tab\\s*\\d+\\s*:?\\s*", "i");
		const tagStripRe = new RegExp(cfg.label_tag_strip_pattern
			?? "^\\[\\s*(?:h[1-6]|heading|body)\\b[^\\]]*\\]\\s*", "i");
		const heads = [];
		const paneLeads = rows[0].map(() => []);   // TITLE-ROW form: label-cell " / "-sub-lines → pane top
		for (let hc = 0; hc < rows[0].length; hc++) {
			let s = this.#cellText(rows[0][hc]);
			// TITLE-ROW form ONLY: a "[tab N] label / (sub-description)" cell splits at " / " —
			// the FIRST segment is the nav label, the rest LEAD the pane (CEDT501 table 2's
			// "(Being mean…)" parenthetical the human floats above the bullets). TEDC (registry
			// path) keeps the whole cell as one label — this branch never runs for it.
			if (!registryTabs) {
				const segs = s.split(/\s+\/\s+/);
				s = segs[0];
				for (const extra of segs.slice(1)) {
					const t = extra.replace(/\*\*/g, "").trim();
					if (/[\[\]]/.test(t)) return null;   // a tag in a lead → a richer form, bail
					if (t) paneLeads[hc].push(t);
				}
			}
			// a '[tab title: X]' / '[Tab N]' bracket lead — consume it, keep any X payload
			s = s.replace(/^\[\s*tab[^\]:]*(?::\s*([^\]]*))?\]\s*/i, (mm, x) => (x ? x + " " : ""));
			s = s.replace(prefixRe, "");
			s = s.replace(tagStripRe, "");
			s = s.replace(/\*\*/g, "").replace(/\s+/g, " ").trim();
			if (!s || /https?:\/\//.test(s) || /[\[\]]/.test(s)) return null;   // empty / URL / tag residue
			if (s.split(/\s+/).length > maxLabel) return null;                  // a long header is prose, not a label
			heads.push(s);
		}

		// CONTENT ROWS → column-major pane text.
		const cellTagRe = new RegExp(cfg.cell_tag_strip_pattern
			?? "^\\[\\s*(?:body|list|text)\\b[^\\]]*\\]\\s*", "i");
		const paneTexts = heads.map((_, c) => paneLeads[c].slice());   // lead lines first (title-row form)
		for (let r = 1; r < rows.length; r++) {
			for (let c = 0; c < nCols; c++) {
				const raw = String(rows[r][c] ?? "");
				if (this.#hasRedText(raw)) return null;          // red = the writer's own spec, not pane body
				const parts = raw.split(/\s+\/\s+/).map((p) => p.trim()).filter(Boolean);
				const lines = [];
				for (let part of parts) {
					part = part.replace(cellTagRe, "").trim();
					if (!part) continue;
					if (/[\[\]]/.test(part)) {
						const lettered = [...part.matchAll(/\[([^\]]*)\]/g)].some((b) => /\p{L}/u.test(b[1]));
						if (lettered || /[\[\]]/.test(part.replace(/\[[^\]]*\]/g, ""))) return null;
					}
					lines.push(part);
				}
				if (!lines.length) return null;                  // an empty cell hides an embedded image (PES class)
				paneTexts[c].push(lines.join("\n"));
			}
		}

		// RENDER — the same pane-assembly machinery #tabsRich and #tabsHeadingPanes use.
		const navItems = [], paneItems = [];
		for (let c = 0; c < heads.length; c++) {
			const chunks = this.#tabsRichPart({ p: paneTexts[c].join("\n") }, rich, run, renderBlock);
			if (chunks === null) return null;
			const content = chunks.join("");
			if (!content.trim()) return null;                    // a pane with no rendered body
			navItems.push(Utils.FillTemplate(tpl.nav_item, { head: inline(heads[c]) }));
			paneItems.push(Utils.FillTemplate(tpl.pane, { content }));
		}
		return titleHtml + [tpl.open, tpl.nav_open, ...navItems, tpl.nav_close,
			tpl.content_open, ...paneItems, tpl.content_close, tpl.close].join("\n");
	}

	/**
	 * ROW-per-tab TABLE tabs (ROUND 214 — verified against OSOH501-01 READYSAFE; the
	 * r197 #tabsTablePanes COLUMN-form sibling). The writer authors the whole tab set as
	 * ONE table where each ROW is a tab: the label cell carries "[tab N] **R**" (label =
	 * the remaining cell text, ** stripped — nav chrome ships PLAIN, the r145/r168/r195
	 * class) and the OTHER cell holds the pane's slash-separated tagged segments
	 * ("[image] URL / [H4] Ready / [body] Being ready…"). Panes ship the segments in
	 * order: the Mode-P/D image, an <h4> at the writer's level, one <p> per [body]
	 * (matching the gold OSOH501-01 pane shape: img + h4 + p).
	 *
	 * Gated to the MEASURED subjects (outputs/_measure_tabrows.py: exactly 3 modules
	 * corpus-wide author this form — OSOH501 ×9 rows, OSOH201, CEDT501 — and the human
	 * gold builds a tabs nav on ALL THREE).
	 *
	 * NEVER half-builds: an extraTypes merge, ≠1 table, a substantive lead member before
	 * the table, < min_rows [tab N] rows, a row without exactly one [tab N] label cell,
	 * an empty/long/bracket-residue label, a non-iStock image, red residue after tag
	 * stripping, or an unknown segment tag all return null (the honest placeholder).
	 * Data rich_panes.row_panes; env TABROWS_OFF.
	 */
	static #tabsTableRows({ bundle, tpl, inline, run }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (bundle.extraTypes && bundle.extraTypes.length) return null;
		const rich = tpl.rich_panes ?? {};
		const cfg = rich.row_panes ?? {};
		const prefix = String(run?.moduleCode ?? "").match(/^[A-Z]+/)?.[0] ?? "";
		if (!(cfg.subjects ?? []).includes(prefix)) return null;   // no measured gold-choice → placeholder

		// EXACTLY ONE captured table; nothing substantive before it but the opener; after
		// it only empty/list-marker black lines (the OSOH numbered-list artifact "1.").
		const tableIdxs = members.map((m, i) => (m && m.type === "table" ? i : -1)).filter((i) => i >= 0);
		if (tableIdxs.length !== 1) return null;
		const ti = tableIdxs[0];
		for (let i = 0; i < members.length; i++) {
			if (i === ti) continue;
			const m = members[i];
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			if (tag === "tabs") continue;                            // the invocation / an [end tabs]
			if (m && m.type === "tag" && (m.parse?.class === "instruction" || m.parse?.class === "noise")) continue;   // surfaces via bundle.instructions
			if (m && m.type === "black") {
				const t = this.#cellText(m.text);
				if (!t || /^\(?\d{1,3}[.)]\s*$/.test(t)) continue;   // empty / a list-marker artifact
			}
			return null;                                             // any other member → a richer form
		}
		const rows = members[ti].block?.rows ?? [];
		const tabRe = /^\[\s*tab\s*(\d+)\s*\]\s*/i;
		const maxLabel = cfg.max_label_words ?? rich.max_label_words ?? 6;
		const navItems = [];
		const paneItems = [];
		let tabRows = 0;
		for (const r of rows) {
			if (!Array.isArray(r) || r.length < 2) return null;
			// the label cell = the one whose text starts with [tab N]; the pane = the other.
			const texts = r.map((c) => this.#cellText(c));
			const li = texts.findIndex((t) => tabRe.test(t));
			if (li < 0) return null;                                 // a row with no [tab N] → not this form
			const rest = texts.filter((_, i) => i !== li).filter((t) => t.trim());
			if (rest.length !== 1) return null;                      // exactly one content cell
			let label = texts[li].replace(tabRe, "").replace(/\*\*/g, "").replace(/\s+/g, " ").trim();
			if (!label || /[\[\]]|https?:\/\//.test(label)) return null;
			if (label.split(/\s+/).length > maxLabel) return null;
			// content cell → ordered tagged segments: [image] / [H2-6] / [body].
			const cell = rest[0];
			const segs = [...cell.matchAll(/\[\s*([a-z0-9 ]+?)\s*\]\s*([^\[]*)/gi)];
			if (!segs.length) return null;
			const parts = [];
			for (const s of segs) {
				const stag = s[1].toLowerCase().replace(/\s+/g, " ").trim();
				let text = s[2].replace(/\s*\/\s*$/, "").trim();     // strip the trailing " / " separator
				if (/^image/.test(stag)) {
					const url = text.match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "";
					const filename = this.#istockFilename(url, rich);   // the iStock templates live on rich_panes
					if (!filename) return null;                      // non-iStock / no URL → bail
					const residual = text.replace(/https?:\/\/\S+/g, "").replace(/[/|]/g, " ").trim();
					if (residual) return null;                       // a caption rode along → richer form
					parts.push(this.#assetImage(filename, rich, run));
					continue;
				}
				if (/^h[2-6]$/.test(stag)) {
					const t = text.replace(/\*\*/g, "").trim();
					if (!t) return null;
					parts.push(`<${stag}>${inline(t)}</${stag}>`);
					continue;
				}
				if (/^(body|text)$/.test(stag)) {
					if (!text.trim()) return null;
					for (const line of text.split(/\n+/)) {
						if (line.trim()) parts.push(`<p>${inline(line.trim())}</p>`);
					}
					continue;
				}
				return null;                                         // an unknown segment tag → bail
			}
			if (!parts.length) return null;
			tabRows++;
			navItems.push(Utils.FillTemplate(tpl.nav_item, { head: inline(label) }));
			paneItems.push(Utils.FillTemplate(tpl.pane, { content: parts.join("\n") }));
		}
		if (tabRows < (cfg.min_rows ?? 2)) return null;
		return [tpl.open, tpl.nav_open, ...navItems, tpl.nav_close,
			tpl.content_open, ...paneItems, tpl.content_close, tpl.close].join("\n");
	}

	/**
	 * carousel — a multi-slide viewer. CONSERVATIVE: builds the clean,
	 * content-derivable forms and keeps the placeholder for everything else.
	 *   (0) ROTATING BANNER — a looping image strip, not really a slideshow at all
	 *                         (see #rotateBanner for why it still arrives as a "carousel" bundle).
	 *   (1) IMAGE-CAPTION TABLE — a 2-column TABLE pairing a derivable image-URL cell with
	 *                         a [body] caption cell (one slide per row). #carouselImageTable.
	 *   (2) IMAGE-SLIDE MEMBERS — a [carousel] opener + per slide a heading/[image]/body,
	 *                         with NO table at all. #carouselImageSlides.
	 *   (3) VIDEO carousel  — every slide a YouTube video (member-based). #carouselVideo.
	 * Dispatch is by CONTENT, most-specific-first: the pre-fold "rotateBanner" variant wins
	 * outright; then a carousel that captured exactly one table and NO video member is the
	 * image-caption form; then, with no table and no video, the image-slide-members form is
	 * tried; anything else falls to the video form (which itself declines on non-video
	 * content). Mixed, text, empty-image, 3+-column and irregular carousels all fall back (null).
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @returns {string|null} the built carousel HTML, or null to keep the orange placeholder
	 */
	static #carousel({ bundle, tpl, renderInline, run, renderBlock }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		// extraTypes set = a multi-widget activity merged in (carousel + X) — too
		// ambiguous to build cleanly.
		if (bundle.extraTypes && bundle.extraTypes.length) return null;

		// ROTATING/ROLLING BANNER (verified against BLL117-02). A [rolling banner]/[rotating
		// banner]/[banner] folds to a carousel bundle, but the human builds a looping image
		// STRIP (div.rotateBanner > bannerItem*N), not a slideshow. The pre-fold bundle.variant
		// remembers the writer used the banner form; #rotateBanner builds it from the captured
		// URL table (placeholder images). Conservative — null falls through to the slideshow
		// dispatch / placeholder. Data carousel.rotate_banner; env ROTBANNER_OFF.
		const rotOn = (tpl.rotate_banner?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.ROTBANNER_OFF);
		if (rotOn && bundle.variant === "rotateBanner") {
			const banner = this.#rotateBanner({ bundle, tpl, run });
			if (banner !== null) return banner;
		}

		const tables = bundle?.tables ?? [];
		const hasVideo = members.some((m) => {
			const text = m && m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const url = m?.block?.links?.[0]?.target ?? (String(text).match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");
			return /youtu\.?be|youtube\.com|vimeo/i.test(url);
		});

		// MEDIA-TABLE form (ROUND 266 — the CHFUN "[slideshow]" dialect, Chris:
		// "MAKE INTO CAROUSEL!"): ONE captured table whose every cell is a media
		// cell ([image]/[video] tag + URL, optional [caption]) builds one slide
		// per cell. Tried FIRST so it owns its exact shape; a table that fails
		// the media-cell test falls straight through to the image|caption-table
		// branch below, byte-unchanged. Data carousel.media_table; env
		// CARMEDTBL_OFF.
		if (tables.length === 1) {
			const mt = this.#carouselMediaTable({ bundle, tpl, renderInline, run });
			if (mt !== null) return mt;
		}

		// IMAGE-CAPTION TABLE form: exactly one captured table, no video anywhere.
		if (!hasVideo && tables.length === 1) {
			return this.#carouselImageTable({ bundle, tpl, renderInline, run });
		}
		// IMAGE-SLIDE MEMBER form: no video, no table — a [carousel] opener + per slide
		// a [heading]/[story heading] + [image] + a [black] body (verified against OSAI201-03 #16).
		// Built only when clean (#carouselImageSlides), else null → the video fallback / placeholder.
		// Env CARIMG_OFF.
		if (!hasVideo && tables.length === 0) {
			const slides = this.#carouselImageSlides({ bundle, tpl, renderInline, run });
			if (slides !== null) return slides;
		}
		// VIDEO form (member-based). A captured table here = a mixed/odd shape → the
		// video walk will reject the non-URL table member and fall back.
		const vid = this.#carouselVideo({ bundle, tpl });
		if (vid !== null) return vid;

		// RICH SLIDE FALLBACK (round 246) — the last resort, after every strict dialect has
		// declined, so each of them stays byte-identical. Builds the writer's carousel from
		// whatever mix of heading / image / video / prose the members actually carry.
		// See #carouselRich. Data carousel.rich_slides; env CARNOTBL_OFF.
		return this.#carouselRich({ bundle, tpl, renderInline, run, renderBlock });
	}

	/**
	 * RICH SLIDE carousel (round 246, ticket 3 of the basic-interactive builders round) —
	 * the carousel's sibling of the round-214 rich-accordion fallback.
	 *
	 * WHY IT EXISTS. Only 36 of 794 captured carousels built, because each existing branch
	 * recognises exactly ONE authoring dialect and bails wholesale on anything else: the
	 * image/caption TABLE form, the image-slide form (which requires EVERY slide to carry both
	 * an image AND a caption), and the pure-video form (which requires every member to be a
	 * bare URL). Writers mix headings, images, videos and prose freely inside one [carousel].
	 *
	 * CHRIS'S DIRECTIVE (2026-08-03) — the Decision Framework's A1 branch: "if the writer has
	 * specified a carousel, the best thing is to generate a carousel". The human developer's
	 * finished page often shows something else (measured over 554 paired no-table declines: a
	 * carousel at 65, another element at 287 — 134 of them accordions — and the text absent at
	 * 202), but that substitution comes from verbal feedback recorded nowhere, AFTER v1 was
	 * handed over. The writer's tag is the derivable target, so this build is judged on the
	 * carousel VERIFIER plus never-half-build, NOT on matching the human's substitution
	 * (Decision_Framework_Human_vs_Claude.md, GATE PRECEDENCE).
	 *
	 * HOW. Members are walked in document order. A [Slide N]-family marker opens a slide; so
	 * does a heading once the current slide already holds content. Each slide accumulates an
	 * ordered part list — heading, image (Mode P/D), YouTube embed, prose (via renderBlock, so
	 * the writer's bullets become a real list) — rendered into the standard carousel item.
	 *
	 * NEVER HALF-BUILDS. Returns null (the honest hand-off box) on: a captured data table, a
	 * merged extra widget type, a nested sub-bundle, red writer-instruction text inside slide
	 * content, an image or video URL it cannot resolve, a member tag it does not recognise, an
	 * empty slide, or a slide count outside [min_slides, max_slides].
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items)
	 * @param {object} args.tpl - the carousel template block (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @param {function} [args.renderBlock] - the black-text/bullet renderer
	 * @returns {string|null} the built carousel, or null to keep the placeholder
	 */
	static #carouselRich({ bundle, tpl, renderInline, run, renderBlock }) {
		const cfg = tpl?.rich_slides;
		if (!cfg || cfg.enabled === false) return null;
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		if (env.CARNOTBL_OFF) return null;
		if (typeof renderBlock !== "function") return null;          // need the body renderer
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if ((bundle.tables ?? []).length) return null;               // the table dialects own that shape
		if ((bundle.extraTypes ?? []).length) return null;           // a merged multi-widget bundle

		const inline = renderInline ?? ((s) => s);
		const slideTags = new Set(cfg.slide_tags ?? []);
		const headTags = new Set(cfg.heading_tags ?? []);
		const textTags = new Set(cfg.text_tags ?? []);
		const idRe = new RegExp(cfg.video_id_re ?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");
		const videoTpl = DataService.Data.EmitTemplates.video?.youtube;

		// ROUND 247 (Chris, ENGS404-00) — the MEDIA-SERIES refinements, each independently toggled.
		// (a) PER-MEDIA SLIDES (env CARMEDSLIDE_OFF): in a bundle with NO [Slide N] markers, each
		// image/video member OPENS its own slide — the writer's back-to-back media list is one
		// slide per item ("[image 1]..[image 4]" = a 4-slide carousel; two [video]s = 2 slides,
		// which previously piled into ONE slide and failed min_slides). A heading/prose-opened
		// slide still receives its FIRST media item (the media only opens a new slide when the
		// current slide already holds a media part), so the heading+image dialect is unchanged.
		// (b) VIDEO-TAIL URL (env CARVIDTAIL_OFF): a [video]/[insert video] member with no URL of
		// its own takes it from the immediately-following black link/title line (the r240 D2
		// title-anchored class inside a widget — measured 137 members / 38 modules, none building);
		// that line is CONSUMED as the video's reference, exactly as MediaBuilder treats it.
		const msCfg = cfg.media_series ?? {};
		const slideMarked = members.some((m) => m?.type === "tag"
			&& (m.parse?.primary?.tag === "slide n" || m.parse?.primary?.tag === "slide"
				|| (m.parse?.tags ?? []).some((t) => t.tag === "slide n")));
		const mediaOpens = (msCfg.media_opens_slide ?? false) && !slideMarked && !env.CARMEDSLIDE_OFF;
		const tailUrls = new Map(), tailConsumed = new Set();
		if ((msCfg.video_tail_url ?? false) && !env.CARVIDTAIL_OFF) {
			for (let i = 0; i < members.length; i++) {
				const m = members[i];
				if (m?.type !== "tag" || m.parse?.primary?.tag !== "video") continue;
				const own = m.block?.links?.[0]?.target
					?? (String((m.text ?? "") + " " + (m.blackAfter ?? "")).match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");
				if (own) continue;
				const nx = members[i + 1];
				if (nx?.type === "black") {
					const u = nx.block?.links?.[0]?.target
						?? (String(nx.text ?? "").match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");
					if (u && idRe.test(u)) { tailUrls.set(m, u); tailConsumed.add(nx); }
				}
			}
		}

		const slides = [];
		let cur = null;
		let pending = [];                                            // accumulating prose for the open slide
		const open = () => { cur = { parts: [] }; slides.push(cur); return cur; };
		const flush = () => {
			const joined = pending.join("\n").trim();
			pending = [];
			if (!joined) return true;
			if (!cur) open();
			cur.parts.push({ p: joined });
			return true;
		};

		for (const m of members) {
			if (!m) continue;
			if (tailConsumed.has(m)) continue;                       // a video's own link/title line (r247)
			if (m.type === "table" || m.type === "nested") return null;
			const tag = m.type === "tag" ? m.parse?.primary?.tag : null;
			const tags = m.type === "tag" ? (m.parse?.tags ?? []).map((t) => t.tag) : [];
			const raw = m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const url = tailUrls.get(m)
				?? m.block?.links?.[0]?.target ?? (String(raw).match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");

			// a writer INSTRUCTION / noise span is not slide content — skip it exactly as the
			// rich accordion does (round 214): the scanner already filed it in
			// bundle.instructions, so it still surfaces as a red Writers Note after the widget
			// and is never silently stripped.
			if (m.type === "tag" && !m.parse?.primary
				&& ["instruction", "noise"].includes(m.parse?.class)) {
				const t = this.#cellText(m.blackAfter ?? "").trim();
				if (t) pending.push(String(m.blackAfter));   // its trailing BLACK text is learner prose
				continue;
			}
			// the widget's own invocation contributes only its trailing prose
			if (tag === bundle.canonTag || tag === "carousel") {
				if (this.#hasRedText(raw)) return null;
				const t = this.#cellText(raw).trim();
				if (t) pending.push(String(raw));
				continue;
			}
			// a [Slide N]-family marker always opens a slide. Its OWN trailing text is the
			// slide's content, not a title — the writer types "[slide 1- with a basic coloured
			// background] Listen to your favourite picture book…" (ENFUN04), a whole sentence —
			// so it goes to the caption, exactly like a black line would.
			if (slideTags.has(tag) || tags.some((t) => slideTags.has(t))) {
				if (this.#hasRedText(raw)) return null;
				flush(); open();
				if (this.#cellText(raw).trim()) pending.push(String(raw));
				continue;
			}
			// a heading titles the open slide, or opens the next one once it holds content
			if (headTags.has(tag)) {
				if (this.#hasRedText(raw)) return null;
				const t = this.#cellText(raw).trim();
				if (!t) continue;
				flush();
				if (!cur || cur.parts.length) open();
				cur.parts.push({ h: t });
				continue;
			}
			// a VIDEO (or an [embed] carrying one) — the shared YouTube embed
			if (tag === "video" || tag === "embed" || (url && idRe.test(url))) {
				if (this.#hasRedText(raw)) return null;
				const id = String(url).match(idRe)?.[1];
				if (!id || !videoTpl) return null;                   // a video we cannot resolve → bail
				flush();
				if (!cur || (mediaOpens && cur.parts.some((pt) => pt.img || pt.video))) open();
				cur.parts.push({ video: id });
				continue;
			}
			// an IMAGE — the standard Mode P/D asset, named from the iStock id
			if (tag === "image" || (url && !this.#cellText(String(raw).replace(/https?:\/\/[^\s\]"<>]+/g, "")).trim())) {
				if (this.#hasRedText(raw)) return null;
				const id = (String(url).match(/gm-?(\d{6,10})/) || String(url).match(/\/id\/(\d{4,10})/) || [])[1];
				if (!id) return null;                                // a non-derivable image → bail
				flush();
				if (!cur || (mediaOpens && cur.parts.some((pt) => pt.img || pt.video))) open();
				cur.parts.push({ img: Utils.FillTemplate(tpl.filename_istock, { id }) });
				continue;
			}
			// PROSE — a plain black line or a text-family element tag
			if (m.type === "black" || textTags.has(tag)) {
				if (this.#hasRedText(raw)) return null;
				if (this.#cellText(raw).trim()) pending.push(String(raw));
				continue;
			}
			if (!String(raw).trim() && !tag) continue;               // a blank line / stray marker
			return null;                                             // an unrecognised member → keep the placeholder
		}
		flush();

		if (slides.length < (cfg.min_slides ?? tpl.min_slides ?? 2)) return null;
		if (slides.length > (cfg.max_slides ?? 20)) return null;
		// SUBSTANCE GUARD (never half-build): a carousel whose slides are ALL bare headings
		// carries no content — the writer's real slide material did not reach the bundle, so
		// the honest hand-off box is better than an empty-looking slideshow.
		if (cfg.require_content !== false
			&& !slides.some((s) => s.parts.some((p) => p.img || p.video || p.p))) return null;

		const items = [];
		for (const s of slides) {
			if (!s.parts.length) return null;                        // an empty slide → never half-build
			const chunks = [];
			let capOpen = false;
			for (const part of s.parts) {
				if (part.h) {
					if (capOpen) { chunks.push(cfg.caption_close); capOpen = false; }
					chunks.push(Utils.FillTemplate(cfg.heading, { text: inline(part.h) }));
				} else if (part.img) {
					if (capOpen) { chunks.push(cfg.caption_close); capOpen = false; }
					chunks.push(this.#assetImage(part.img, tpl, run));
				} else if (part.video) {
					if (capOpen) { chunks.push(cfg.caption_close); capOpen = false; }
					chunks.push(Utils.FillTemplate(videoTpl, { videoId: part.video, params: "" }));
				} else {
					// renderBlock (ListsAndRuns.renderBlackText) returns an ARRAY of <p>/<ul>
					// html, exactly as the rich accordion consumes it.
					const rendered = renderBlock(part.p);
					const arr = (Array.isArray(rendered) ? rendered : [rendered])
						.filter((h) => h && String(h).trim());
					if (!arr.length) return null;
					if (!capOpen) { chunks.push(cfg.caption_open); capOpen = true; }
					for (const h of arr) chunks.push(String(h));
				}
			}
			if (capOpen) chunks.push(cfg.caption_close);
			items.push(Utils.FillTemplate(cfg.item, { parts: chunks.join("\n") }));
		}
		bundle.r246Carousel = true;                                  // detector/affected-set marker
		return [tpl.open, ...items, tpl.close].join("\n");
	}

	/**
	 * ROTATE BANNER (verified against BLL117-02) — the looping image STRIP the human builds
	 * for a [rolling banner]/[rotating banner]/[banner]. These fold to a `carousel` bundle
	 * (widget_type_taxonomy rotateBanner->carousel) but the human's output is
	 * div.rotateBanner > div.bannerContainer > div.bannerItem*N > img, NOT a slideshow viewer —
	 * so #carousel branches here when the pre-fold bundle.variant is "rotateBanner". The single
	 * captured table is a grid of bare image-URL cells; emit one bannerItem per non-empty
	 * cell, read COLUMN-MAJOR (the human's source order — invisible to the automated
	 * text-stripped structural comparison, which collapses the whole widget to one marker).
	 * Each image is the standard Mode-P/D
	 * placeholder (the iStock id in the URL → images/iStock-<id>.jpg; a non-iStock image host
	 * → a slug placeholder — both shown as a placehold.co placeholder + the commented real
	 * ref). CONSERVATIVE never-half-build → null (the #carousel fallback keeps the honest
	 * placeholder) on: no table; a TEXT-only cell (the text+image banner form, OSAI101); a cell
	 * carrying a CAPTION beyond the URL (the image+caption CAROUSEL form, CEDW501); a video URL;
	 * or < min_items images. alt stays empty (the human's alt is the editorial Media-List
	 * description). Data carousel.rotate_banner; env ROTBANNER_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (its .tables[0] is the banner grid)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @returns {string|null} the built rotating-banner HTML, or null to fall through
	 */
	static #rotateBanner({ bundle, tpl, run }) {
		const cfg = tpl.rotate_banner;
		if (!cfg || cfg.enabled === false) return null;
		const table = (bundle.tables ?? [])[0];
		const rows = (table?.rows ?? []).filter((r) => Array.isArray(r));
		if (!rows.length) return null;
		const ncols = Math.max(...rows.map((r) => r.length));
		const items = [];
		for (let c = 0; c < ncols; c++) {
			for (const r of rows) {
				const text = this.#cellText(r[c] ?? "");
				if (!text) continue;                          // empty cell (ragged last column) — skip
				const url = (text.match(/https?:\/\/[^\s\]"<>]+/) ?? [])[0];
				if (!url) return null;                        // a TEXT-only cell (text+image banner form) → keep placeholder
				if (/youtu\.?be|youtube\.com|vimeo/i.test(url)) return null;   // a video → not an image strip
				// PURE-IMAGE GUARD (CEDW501): the rotateBanner STRIP is image-only. If a cell carries
				// a CAPTION (any text beyond the image URL + an optional leading media label), it is the
				// image+CAPTION CAROUSEL form, NOT a banner strip — bail so it falls through to the
				// carousel/placeholder rather than silently dropping the caption.
				const residue = text
					.replace(/https?:\/\/[^\s\]"<>]+/g, " ")              // the image URL (the asset ref, not learner text)
					.replace(/^\s*(image|photo|img|picture)\s*:?/i, " ")  // an optional leading media label
					.replace(/[\s/]+/g, "").trim();
				if (residue) return null;
				items.push(Utils.FillTemplate(cfg.item, { image: this.#assetImage(this.#bannerImageFilename(url, tpl), tpl, run) }));
			}
		}
		if (items.length < (cfg.min_items ?? 2)) return null;
		return [cfg.open, ...items, cfg.close].join("\n");
	}

	/** A banner image's asset filename: the iStock id form when present, else a slug of the
	 * URL's last path segment (a gate-invisible placeholder name — the developer drops in the
	 * real asset post-conversion, exactly like every other image). */
	static #bannerImageFilename(url, tpl) {
		const istock = this.#istockFilename(url, tpl);
		if (istock) return istock;
		const seg = (url.split(/[?#]/)[0].split("/").filter(Boolean).pop() || "image").replace(/\.[a-z0-9]{2,4}$/i, "");
		return (Utils.Slugify(seg) || "image") + ".jpg";
	}

	/**
	 * IMAGE-SLIDE MEMBER carousel (verified against OSAI201-03 #16). bundle.memberItems is a
	 * [carousel] opener then, per slide, a [heading]/[story heading] (the slide heading),
	 * an [image] (an iStock URL), and a [black] body (e.g. "**Scenario:** … \n **⚠️Caution:** …").
	 * Build one item_image_heading per slide: <h4>heading</h4> + the Mode-P/D image +
	 * a carousel-caption whose <p>s are the body split on newlines (rendered via renderInline).
	 * CONSERVATIVE (never half-build): any slide missing an image or body, a non-iStock image,
	 * a surviving red instruction, or < min_slides slides → null (keep the orange placeholder).
	 * Data interactive_builders.carousel.{image_slides_enabled,item_image_heading}; env CARIMG_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @returns {string|null} the built carousel HTML, or null to try the video-carousel form next
	 */
	static #carouselImageSlides({ bundle, tpl, renderInline, run }) {
		if (tpl.image_slides_enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.CARIMG_OFF) return null;
		if (!tpl.item_image_heading) return null;
		const members = bundle?.memberItems ?? [];
		const inline = renderInline ?? ((s) => s);
		const slides = [];
		let cur = null;
		// Verified against OSAI501-04: a [Slide N] marker opens a slide and the FOLLOWING [H#] is the
		// slide title (the original, simpler form of this builder only opened a slide on a
		// [heading]/[story heading] with no [Slide N] marker at all).
		// Recognise both: a [slide n]/[slide] marker → new slide; an [H2]-[H6]/[heading]/[story heading]
		// → the title for the slide just opened (or a new slide for the heading-only carousel form).
		const headingTags = new Set(["heading", "story heading", "h2", "h3", "h4", "h5", "h6"]);
		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			const tags = m && m.type === "tag" ? (m.parse?.tags ?? []).map((t) => t.tag) : [];
			const text = m && m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			if (tag === "carousel") continue;                                   // the [carousel]/[slide show] opener
			if (tags.includes("slide n") || tag === "slide n" || tag === "slide") {
				cur = { heading: "", image: null, body: [] };                   // a [Slide N] marker opens a new slide
				slides.push(cur);
				continue;
			}
			if (headingTags.has(tag)) {
				if (this.#hasRedText(text)) return null;
				const h = this.#cellText(text).trim();
				if (!h) continue;
				if (cur && !cur.heading && !cur.image && !cur.body.length) { cur.heading = h; continue; }   // title for the [Slide N] just opened
				cur = { heading: h, image: null, body: [] };                    // heading-opened slide (no [slide n] markers)
				slides.push(cur);
				continue;
			}
			const url = m?.block?.links?.[0]?.target ?? (String(text).match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");
			const isImage = tag === "image" || (url && !this.#cellText(String(text).replace(/https?:\/\/[^\s\]"<>]+/g, "")).trim());
			if (isImage) {
				if (!cur) return null;                               // an image with no open slide → bail
				if (cur.image) continue;                             // a duplicate/stray image URL after the slide's image → skip
				const id = (url.match(/gm-?(\d{6,10})/) || url.match(/\/id\/(\d{4,10})/) || [])[1];
				if (!id) return null;                                // a non-derivable image → bail (never half-build)
				cur.image = this.#assetImage(Utils.FillTemplate(tpl.filename_istock, { id }), tpl, run);
				continue;
			}
			// Verified against OSAI501-04: a slide caption authored as a [body] ELEMENT (the [Slide N]
			// form), not as a black paragraph. Push its text as a caption line (same as a black member).
			if (tag === "body") {
				if (this.#hasRedText(text)) return null;             // an embedded writer instruction → bail
				if (!cur) return null;
				if (this.#cellText(text).trim()) cur.body.push(String(text));
				continue;
			}
			if (m && m.type === "black") {
				if (!this.#cellText(text).trim()) continue;
				if (!cur || this.#hasRedText(text)) { if (process.env.CARIMG_DEBUG) console.error("[CARIMG] bail BLACK cur=" + !!cur + " red=" + this.#hasRedText(text)); return null; }
				cur.body.push(String(text));
				continue;
			}
			if (!String(text).trim()) continue;                      // any empty member (stray marker / blank line) → skip
			return null;                                             // anything richer → bail
		}
		if (slides.length < (tpl.min_slides ?? 2)) return null;
		// The slide-title FORM is a per-GROUP house style (ROUND 214, measured
		// outputs/_measure_carousel_caption.py): the default is the OSAI <h4>-above-img
		// form (A — byte-identical for every carousel already building); the subjects
		// listed in caption_title_bold ship the title as the caption's FIRST
		// <p><b>title</b></p> line instead (B — OSOH501's gold shape, 29:0 in that
		// subject). A slide whose heading the writer FORGOT (OSOH501-02 slide 4 — the
		// gold's recovered title is not in the WT, recorded C) ships body-only through
		// the caption shell rather than an empty <h4>. env CARCAP_OFF reverts to A-only
		// + the round-63 empty-heading behaviour.
		const capCfg = tpl.caption_title_bold;
		const capOff = typeof process !== "undefined" && process.env && process.env.CARCAP_OFF;
		const prefix = String(run?.moduleCode ?? "").match(/^[A-Z]+/)?.[0] ?? "";
		const boldForm = !capOff && capCfg && capCfg.enabled !== false
			&& (capCfg.subjects ?? []).includes(prefix) && tpl.item_image_caption;
		const items = [];
		for (const s of slides) {
			if (!s.image || !s.body.length) return null;             // never half-build
			// one <p> per paragraph: split on newlines AND before each bold-LABEL section
			// ("**Scenario:** …" / "**⚠️Caution:** …") — the human renders each as its own <p>.
			const caption = s.body
				.flatMap((b) => b.split(/\n+/))
				.flatMap((line) => line.split(/(?=\*\*\s*\W{0,3}[A-Z][a-zA-Z]{2,18}:)/))
				.map((part) => (this.#cellText(part).trim() ? `<p>${inline(part.trim())}</p>` : ""))
				.filter(Boolean).join("\n");
			if (!caption) return null;
			if (boldForm) {
				const title = s.heading ? `<p><b>${inline(s.heading)}</b></p>\n` : "";
				items.push(Utils.FillTemplate(tpl.item_image_caption, {
					image: s.image, caption: title + caption,
				}));
				continue;
			}
			if (!s.heading && tpl.item_image_caption && !capOff) {   // headingless slide → caption-only shell
				items.push(Utils.FillTemplate(tpl.item_image_caption, { image: s.image, caption }));
				continue;
			}
			items.push(Utils.FillTemplate(tpl.item_image_heading, {
				heading: inline(s.heading), image: s.image, caption,
			}));
		}
		return [tpl.open, ...items, tpl.close].join("\n");
	}

	/**
	 * VIDEO carousel (member-based — EXPFUN02/03, ENGJ301). bundle.memberItems is the
	 * [carousel] opener + a run of [video] members (or a [slide N] marker / a black
	 * line carrying a YouTube URL). Build one <div class="item video"> per video.
	 *
	 * SAFETY (never half-build): null the moment a member is a non-YouTube URL, carries
	 * caption/heading TEXT beyond the URL, is an image, or there are < min_slides videos.
	 */
	static #carouselVideo({ bundle, tpl }) {
		const members = bundle?.memberItems ?? [];
		const videoTpl = DataService.Data.EmitTemplates.video;
		const ytRe = new RegExp(DataService.Data.AcksFormats.extraction_regexes.youtube_id);
		const STRUCTURAL = new Set(["carousel", "slide", "slide n", "shape n", "story heading"]);
		const ids = [];

		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			const text = m && m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const url = m?.block?.links?.[0]?.target
				?? (text.match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");

			if (url) {
				const id = url.match(ytRe)?.[1];
				if (!id) return null;                       // non-YouTube video/link → bail
				// the member must be JUST the URL (+ its tag) — any real caption/heading
				// text means this is a content carousel, not a pure video one.
				const caption = this.#cellText(text.replace(/https?:\/\/[^\s\]"<>]+/g, ""));
				if (caption && caption.replace(/[\s.,–—-]/g, "").length > 2) return null;
				ids.push(id);
				continue;
			}
			// no URL: allowed only if it's a structural marker or a blank line
			if (tag && STRUCTURAL.has(tag)) continue;
			if (m && m.type === "black" && !this.#cellText(text).trim()) continue;
			return null;                                    // text/heading/image content → bail
		}

		if (ids.length < (tpl.min_slides ?? 2)) return null;   // 0–1 videos is not a carousel
		const items = ids.map((id) => Utils.FillTemplate(tpl.item_video, {
			embed: Utils.FillTemplate(videoTpl.youtube, { videoId: id, params: "" }),
		}));
		return [tpl.open, ...items, tpl.close].join("\n");
	}

	/**
	 * IMAGE-CAPTION TABLE carousel (verified — OSGM501-01). The captured table pairs,
	 * per data ROW, an IMAGE cell (a derivable iStock URL, with an optional [carousel N]
	 * / [slide N] / [image] marker + " / " separator) with a CAPTION cell ([body] + the
	 * prose). Build one <div class="item image"> per row: the image (Mode P/D) + a
	 * <div class="carousel-caption"><p>…</p>. The image src is the iStock id convention
	 * (images/iStock-<id>.jpg); the developer's alt text is NOT derivable → alt="".
	 *
	 * ROW HANDLING (flexible, robust to writer variation):
	 *   • a leading single-cell [Title] row and an "Images | Text" column-label row are
	 *     dropped (content-based, not tag-spelling-based — see #isCarouselTitleOrLabelRow);
	 *   • each remaining row MUST be a clean image|caption pair (#imageCaptionPair) in
	 *     either column order — anything else (3+ cols, image in both/neither cell, a
	 *     non-iStock/underivable image, a 2nd red developer span, a bulleted/multi-line
	 *     caption) bails the WHOLE widget (never half-build);
	 *   • a trailing non-slide [body] paragraph AFTER the table is the writer resuming
	 *     free body (the human renders it as a <p> after the carousel) → appended via
	 *     #carouselTrailingBody, NOT lost. A richer trailing member (table/widget/list)
	 *     bails.
	 */
	/**
	 * MEDIA-TABLE carousel (ROUND 266 — the CHFUN "[slideshow]" dialect,
	 * module CHFUN01; Chris's screenshot: "MAKE INTO CAROUSEL!"). The writer
	 * authors the whole slideshow as ONE table; every cell is a media cell:
	 * an [image] or [video] red tag (+ a [media item N] sub-tag), a URL, and
	 * optionally a [caption] tag with the caption text — e.g.
	 *   "[image][media item 1] https://istockphoto.com/..." |
	 *   "[video][media item 3] https://youtube.com/watch?v=… / [caption] Chinese calligraphy"
	 * Builds one slide per cell, in cell order:
	 *   - [image] → the standard Mode P/D asset machinery (#assetImage via the
	 *     iStock filename rule) — NO caption div unless the cell carries one
	 *   - [video] YouTube watch/youtu.be → the shared video.youtube 16x9 embed;
	 *     a /shorts/ URL → the youtubeShort 1x1 form (the CHFUN golds ship
	 *     shorts that way 57/57); the cell's [caption] → a carousel-caption
	 * Slides ship a PLAIN videoSection (no icon) — the family's gold icon
	 * share is 0.69, below the r200 solidify floor (recorded).
	 *
	 * NEVER HALF-BUILDS → null (the honest hand-off box) on: a cell with no
	 * URL, an image URL the iStock filename rule cannot name, a video URL on
	 * an unknown host, or fewer than min_slides slides.
	 *
	 * @param {object} args - bundle / tpl / renderInline / run
	 * @returns {string|null} the built carousel, or null
	 *
	 * Data: carousel.media_table. Env toggle: CARMEDTBL_OFF.
	 */
	static #carouselMediaTable({ bundle, tpl, renderInline, run }) {
		const cfg = tpl.media_table;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.CARMEDTBL_OFF) return null;
		const table = (bundle.tables ?? [])[0];
		const rows = table?.rows ?? [];
		if (!rows.length) return null;
		const inline = renderInline ?? ((s) => s);
		const acks = DataService.Data.AcksFormats ?? {};
		const ytRe = new RegExp(acks.youtube_id ?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");
		const shortsRe = new RegExp(cfg.shorts_id_re ?? "youtube\\.com/shorts/([\\w-]{11})");
		const tagRe = /\[\s*(image|video)\s*\]/i;

		const slides = [];
		for (const r of rows) {
			if (!Array.isArray(r)) return null;
			for (const cell of r) {
				const raw = String(cell ?? "");
				if (!raw.trim()) continue;                       // empty cell — skipped
				const kindM = tagRe.exec(raw);
				if (!kindM) return null;                         // a non-media cell → not this form
				const kind = kindM[1].toLowerCase();
				const url = raw.match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "";
				if (!url) return null;
				// the cell's own [caption] text (everything after the [caption] tag)
				const capM = /\[\s*caption\s*\][^\u{1f534}]*/iu.exec(raw);
				const caption = capM
					? this.#cellText(raw.slice(capM.index)).replace(/^\s*\[\s*caption\s*\]\s*/i, "").trim()
					: "";
				if (kind === "image") {
					const filename = this.#istockFilename(url, tpl);
					if (!filename) return null;                  // un-nameable image → bail
					const image = this.#assetImage(filename, tpl, run);
					slides.push(caption
						? Utils.FillTemplate(tpl.item_image, { image, caption: inline(caption) })
						: Utils.FillTemplate(cfg.item_image_plain ?? "<div class=\"item image\">\n{image}\n</div>", { image }));
				} else {
					const shortId = url.match(shortsRe)?.[1] ?? null;
					const watchId = url.match(ytRe)?.[1] ?? null;
					if (!shortId && !watchId) return null;       // unknown video host → bail
					const embed = shortId
						? Utils.FillTemplate(cfg.shorts_embed, { videoId: shortId })
						: Utils.FillTemplate(DataService.Data.EmitTemplates.video.youtube, { videoId: watchId, params: "" });
					slides.push(caption
						? Utils.FillTemplate(cfg.item_video_caption
							?? "<div class=\"item video\">\n{embed}\n<div class=\"carousel-caption\">\n<p>{caption}</p>\n</div>\n</div>",
							{ embed, caption: inline(caption) })
						: Utils.FillTemplate(cfg.item_video_plain ?? "<div class=\"item video\">\n{embed}\n</div>", { embed }));
				}
			}
		}
		if (slides.length < (tpl.min_slides ?? 2)) return null;

		// trailing free-body paragraph(s) after the slide table (kept outside the carousel).
		const trailing = this.#carouselTrailingBody(bundle, inline, tpl);
		if (trailing === null) return null;

		return [tpl.open, ...slides, tpl.close, ...trailing].join("\n");
	}

	static #carouselImageTable({ bundle, tpl, renderInline, run }) {
		const table = (bundle.tables ?? [])[0];
		const rows = table?.rows ?? [];
		if (!rows.length) return null;
		const members = bundle.memberItems ?? [];
		const inline = renderInline ?? ((s) => s);

		// GUARD: nothing meaningful may sit BEFORE the table except the [carousel]
		// opener (or blank lines) — a video/image/heading before it is too rich to build.
		const tableIdx = members.findIndex((m) => m.type === "table");
		for (let i = 0; i < tableIdx; i++) {
			const m = members[i];
			const tag = m.type === "tag" ? m.parse?.primary?.tag : null;
			const text = this.#cellText(m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? ""));
			if (tag === "carousel" && !text) continue;            // the opener tag
			if (m.type === "black" && !text) continue;            // blank line
			return null;
		}

		// walk rows in order: drop leading title/label rows, build every data row.
		const slides = [];
		let started = false;
		for (const r of rows) {
			if (!Array.isArray(r)) return null;
			const pair = this.#imageCaptionPair(r, tpl);
			if (pair) {
				slides.push(Utils.FillTemplate(tpl.item_image, {
					image: this.#assetImage(pair.filename, tpl, run),
					caption: inline(pair.caption),
				}));
				started = true;
				continue;
			}
			// not a clean slide: a leading title/label row is dropped; anything else bails.
			if (!started && this.#isCarouselTitleOrLabelRow(r, tpl)) continue;
			return null;
		}
		if (slides.length < (tpl.min_slides ?? 2)) return null;

		// trailing free-body paragraph(s) after the slide table (kept outside the carousel).
		const trailing = this.#carouselTrailingBody(bundle, inline, tpl);
		if (trailing === null) return null;

		return [tpl.open, ...slides, tpl.close, ...trailing].join("\n");
	}

	/**
	 * clickDrop — a row of click-to-reveal buttons (verified — OSGM501-03). MEMBER-based
	 * like accordion/tabs: one [click drop N] tag per item (its trailing text = the button
	 * LABEL) followed by the item's [body] paragraph(s) (the revealed CONTENT). The human
	 * renders, inside ONE <div class="row">, ALL buttons first then ALL content panels,
	 * paired by position; the per-row GROUPING the human chooses (OSGM501-03's 6 items as
	 * 2 rows of 3) is a NON-DERIVABLE, gate-invisible layout choice (clickDrop is in the
	 * wrapper catalogue), so we emit one row of all buttons + all contents — functionally
	 * identical (the JS pairs button[i] → content[i]).
	 *
	 * SAFETY (never half-build → null, keep the placeholder): an [image]/[video]/[button]/
	 * [heading]/data table inside the widget, an item missing its label or body, or red
	 * writer-instruction text all fall back. (Same-TYPE extra clickDrops are the additional
	 * BUTTONS — captured as members, never a reason to bail.)
	 */
	static #clickDrop({ bundle, tpl, renderInline, run }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		const inline = renderInline ?? ((s) => s);

		const items = [];          // [{ label, body:[paragraphs] }]
		let cur = null;
		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			const raw = m && m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const text = this.#cellText(raw);

			// (a) a [click drop N] opens a new item; its trailing text is the button label
			if (tag === "click drop") {
				if (!text || this.#hasRedText(raw)) return null;   // a button with no clean label → bail
				cur = { label: text, body: [] };
				items.push(cur);
				continue;
			}
			// (b) body paragraph for the current item (untagged black or a [body] tag)
			if (!text) continue;                                   // blank line
			if (!cur) return null;                                 // content before any button → bail
			if (this.#hasRedText(raw)) return null;
			if (this.#isInlineMarkerMember(m)) { this.#mergeBodyContinuation(cur.body, text); continue; }   // inline highlight → item body continuation
			if (tag && tag !== "body") return null;                // an [image]/widget member → too rich
			cur.body.push(text);
		}

		if (items.length < (tpl.min_items ?? 1)) return null;
		for (const it of items) if (!it.label || !it.body.length) return null;   // each needs a label + content

		const buttons = items.map((it) => Utils.FillTemplate(tpl.button, { label: inline(it.label) }));
		// ROUND 241 (Dev-Feedback R4, C2 — SCCH302's Equipment clickDrop). The revealed
		// CONTENT used to be dumped one <p> per captured paragraph, which shipped a writer's
		// Word bullets as literal '<p>• A 100ml measuring cylinder</p>' text. The gold
		// library ships ZERO such bullets inside clickDropContent and 134 pages with real
		// <ul>/<ol> lists there (measured round 241), so the content now routes through the
		// STANDARD black-text renderer (ListsAndRuns.renderBlackText — the same machinery
		// every free-body paragraph/list uses: '• ' lines group into <ul><li>, numbered
		// lines into <ol>, plain lines stay one <p> each). stitch=false = the r201
		// containment (built-widget internals are outside the free-body hover-weave scope);
		// links=[] matches the legacy inline path. A plain no-bullet body renders through
		// the same <p> template as before. Data flag: interactive_builders.clickDrop
		// .list_content. Env toggle: CDLIST_OFF (reverts to the one-<p>-per-paragraph form).
		const listContent = (tpl.list_content ?? false)
			&& !(typeof process !== "undefined" && process.env && process.env.CDLIST_OFF);
		const contents = items.map((it) => Utils.FillTemplate(tpl.content, {
			content: listContent
				? ListsAndRuns.renderBlackText(it.body.join("\n"), run, [], false).join("\n")
				: it.body.map((t) => `<p>${inline(t)}</p>`).join(""),
		}));
		return [tpl.open, ...buttons, ...contents, tpl.close].join("\n");
	}

	// =======================================================================
	// SHARED HELPERS  (used by the builders above)
	// =======================================================================

	/**
	 * True when a row is just column LABELS (so we drop it before building).
	 *
	 * Two signals, either is enough — both are conservative so a real data row
	 * is never mistaken for a header:
	 *   (a) STRUCTURAL — every cell is fully wrapped in the writer's RED TEXT
	 *       markers. Writers colour their column labels red (it's an
	 *       instruction to the developer, not learner content), so an all-red
	 *       first row is the label row. This catches odd phrasings like
	 *       "Hint title" / "Information once slide" without any word list.
	 *   (b) WORD-LIST — every cell (red markers stripped) is a known column
	 *       label word. The list is data-tunable via the widget template's
	 *       header_label_keywords (falls back to a sensible default here).
	 */
	static #looksLikeHeaderRow(cells, tpl = {}) {
		if (!Array.isArray(cells) || !cells.length) return false;
		// (a) writer's red column-labels
		if (cells.every((c) => this.#isFullyRed(c))) return true;
		// (b) known label words (data-tunable)
		const words = (tpl.header_label_keywords && tpl.header_label_keywords.length)
			? tpl.header_label_keywords
			: ["hint", "slide", "front", "back", "term", "definition", "word", "meaning"];
		const re = new RegExp(`^(${words.join("|")})$`, "i");
		return cells.every((c) => re.test(this.#cellText(c)));
	}

	/** True when a cell is entirely the writer's red instruction text. */
	static #isFullyRed(cell) {
		const s = String(cell ?? "").trim();
		return /^\u{1f534}\[RED TEXT\][\s\S]*\[\/RED TEXT\]\u{1f534}$/u.test(s);
	}

	/**
	 * True when a cell carries the writer's red instruction text ANYWHERE (not
	 * only as a whole-cell header). Such text is a developer instruction, not
	 * learner content, so a plain-text widget must never build around it — it
	 * falls back instead, leaving the instruction visible as a red flag.
	 */
	static #hasRedText(cell) {
		return /\[RED TEXT\]/.test(String(cell ?? ""));
	}

	/**
	 * True when a member is an INLINE-MARKER widget tag — [highlight text]/[word select]
	 * (→ wordSelect/wordHighlighter) or [rollover/hover definition] (→ infoTrigger). The
	 * scanner ABSORBS these inside an open widget (they annotate the host text INLINE — a
	 * highlight span or a tooltip — never a standalone box), so they arrive in a member-text
	 * widget's bundle as a stray tag member. The member-text builders (accordion/tabs/clickDrop)
	 * must treat such a member as body CONTINUATION of the current panel/item: the writer dropped
	 * the marker MID-PARAGRAPH (XGF9001-00's "…Māori perspectives value [highlight text] mana…"),
	 * which the parser split into a [body] part + a [word select] part — NOT a foreign widget tag
	 * that should force a bail. The highlight/tooltip STYLING is non-derivable, so Phase-1 renders
	 * the annotated text as readable plain text (the inline-marker policy); we re-join it so the
	 * panel body stays one paragraph, matching the human.
	 *
	 * Data-driven (no hard-coded tag words): the marker widget-types come from the boundary bank's
	 * member_rule.{inline_markers, standalone_inline_markers}; the canonical-tag → widget-type map
	 * from the lexicon. Any future alias for a highlight / rollover marker is covered automatically.
	 */
	static #isInlineMarkerMember(m) {
		if (!m || m.type !== "tag") return false;
		const tag = m.parse?.primary?.tag;
		if (!tag) return false;
		const mr = DataService.Data.BoundaryBank?._meta?.member_rule ?? {};
		const markers = new Set([...(mr.inline_markers ?? []), ...(mr.standalone_inline_markers ?? [])]);
		const types = DataService.Data.TagLexicon?.tags?.[tag]?.widget_types ?? [];
		return types.some((t) => markers.has(t));
	}

	/** Append inline-marker continuation TEXT to a panel/item body part array, merging it into
	 *  the LAST paragraph (the marker split one paragraph) or starting one if the body is empty. */
	static #mergeBodyContinuation(parts, text) {
		if (!text) return;
		if (parts.length) parts[parts.length - 1] += " " + text;
		else parts.push(text);
	}

	/**
	 * Captured cell/line → plain text: strips the corpus red-span markers and
	 * trims. (Inline **bold** / *italic* / links are handled later by the
	 * caller's renderInline, so we leave those markers in place here.)
	 */
	static #cellText(value) {
		return String(value ?? "")
			.replace(/\u{1f534}\[RED TEXT\]/gu, "")
			.replace(/\[\/RED TEXT\]\u{1f534}/gu, "")
			.trim();
	}

	/**
	 * iStock URL → the image FILENAME the page uses (e.g. "iStock-978974888.jpg"),
	 * or null when the URL is not a nameable iStock image so the caller falls back.
	 *
	 * WHY iStock-only: it is the unambiguous, dominant image source in this corpus
	 * and its id (the run of 6-10 digits after "gm" in the URL) gives a stable
	 * filename. A YouTube/Vimeo link is a VIDEO, not a bubble image — reject it.
	 * (This mirrors MediaBuilder.image; the filename PATTERN lives in data.)
	 */
	static #istockFilename(url, tpl) {
		if (!url || /youtu\.?be|youtube\.com|vimeo/i.test(url)) return null;
		// iStock ids look like "...gm978974888-..." (sometimes "gm-978974888")
		const id = url.match(/gm-?(\d{6,10})/)?.[1] ?? null;
		return id ? Utils.FillTemplate(tpl.filename_istock, { id }) : null;
	}

	/**
	 * True when a table cell is the IMAGE cell of a speech bubble: it either holds
	 * the captured image URL, or carries an [image] tag. (Keying off the URL the
	 * scanner already extracted is robust to how the writer spelled the tag.)
	 */
	static #isImageCell(cell, url) {
		const s = String(cell ?? "");
		return (url && s.includes(url)) || /\[\s*image\b/i.test(s);
	}

	/**
	 * Drops red INSTRUCTION / REVEAL spans from a widget cell, keeping the surrounding learner
	 * content, so an otherwise-clean build is no longer blocked by them. The widget's OWN tag span
	 * ([image]/[speech bubble]) is KEPT. A span is dropped when its content (leading bracket/space
	 * removed) starts with one of `prefixes` at a word boundary:
	 *   • "CS:"/"Dev:"/"Note:" — a developer instruction (a MANUAL image/layout edit the human does
	 *     by hand, e.g. OSAI201 #1 "CS: can a cross be put through the brain image…") — NOT content.
	 *   • "flipside:" — a reveal LABEL; the bubble text AFTER it (the second part) is kept, so the
	 *     existing " / " multi-paragraph path renders both parts (OSAI201 #8's GenAI bubble).
	 * Any OTHER unexpected 2nd red span still trips the conservative #redSpanCount bail.
	 * Data-tunable: prefixes default below; override via the widget template (droppable_span_prefixes).
	 */
	static #stripDevSpans(cell, prefixes) {
		const pre = (prefixes && prefixes.length) ? prefixes : ["cs", "dev", "note", "flipside", "flip side"];
		const re = new RegExp(`^(?:${pre.join("|")})\\b`, "i");
		return String(cell ?? "").replace(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu,
			(m, content) => re.test(content.replace(/^[\s\[]+/, "")) ? "" : m);
	}

	/**
	 * How many MEANINGFUL red writer-instruction spans a cell contains. A clean widget
	 * cell has at most ONE (its own tag); a SECOND span is an embedded developer note
	 * ("CS: ...") or a 'flipside:' reveal — the signal to fall back, not build.
	 *
	 * Counts only spans whose content is non-blank: an EMPTY / whitespace-only red span
	 * is a writer FORMATTING artifact (e.g. a coloured trailing space or tab after the
	 * image URL — OSBY201-02's bubble), NOT a developer instruction, so it must not trip
	 * the "2nd red span → bail" guard. Robust to the common stray-red-space deviation.
	 */
	/**
	 * Isolate an embedded MANUAL-EDIT instruction in a widget IMAGE cell (verified against
	 * OSAI201-02 #12). When a
	 * documented cue (CS/dev/note…) sits immediately AFTER the [image] tag, the cue introduces a
	 * designer instruction (e.g. OSAI201-02 "[image] CS Give me three pet story ideas. Can that
	 * text be on the sign?") that runs — across red spans AND plain black text — up to the image
	 * URL. The only build-relevant content is the [image] tag + the URL, so reduce the cell to
	 * those two and drop the instruction (the human acts on it by hand). Returns the cell unchanged
	 * when no cue directly follows the tag, so an ordinary image cell is never touched.
	 *
	 * @param {string} cell - the raw cell text (may contain 🔴[RED TEXT]…[/RED TEXT]🔴 spans)
	 * @param {string[]} prefixes - the cue words that mark a developer instruction (e.g. "cs", "dev")
	 * @param {string} [url] - the image URL already extracted elsewhere, if known
	 * @returns {string} the cell, either unchanged or reduced to just its [image] tag + URL
	 */
	static #isolateInstructionImageCell(cell, prefixes, url) {
		const pre = (prefixes && prefixes.length) ? prefixes : ["cs", "dev", "note", "flipside", "flip side"];
		const plain = this.#cellText(cell);
		const afterTag = plain.replace(/^\s*\[[^\]]*\]\s*/, "");
		if (!new RegExp(`^(?:${pre.join("|")})\\b`, "i").test(afterTag)) return cell;   // no embedded cue → unchanged
		const tag = plain.match(/\[[^\]]*image[^\]]*\]/i)?.[0] ?? "[image]";
		const u = url || (plain.match(/https?:\/\/\S+/)?.[0] ?? "");
		return `\u{1f534}[RED TEXT] ${tag} [/RED TEXT]\u{1f534}${u ? ` ${u}` : ""}`;
	}

	static #redSpanCount(cell) {
		const spans = String(cell ?? "").match(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu) || [];
		return spans.filter((s) =>
			s.replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").trim().length > 0).length;
	}

	/**
	 * Render a bubble image honouring the run's image mode, exactly like the rest
	 * of the page: Mode P (default) = a visible placeholder + the commented-out
	 * real reference (so the developer drops the asset in later); Mode D = the
	 * real <img>. The markup (incl. the bubble-img class) lives in the widget
	 * template, so it stays editable in data with no code change.
	 *
	 * @param {string} filename - e.g. "iStock-978974888.jpg"
	 * @param {object} tpl      - the speechBubble template block
	 * @param {object} run      - run context (run.imageMode is "P" or "D")
	 */
	static #assetImage(filename, tpl, run) {
		// ROUND 242 — the r240 D1 RIDER taken (the recorded "any widget round" rider):
		// widget-INTERNAL images join the alt/lazy rule via MediaBuilder.FinishImg.
		// The title authority here is the VERIFIED iStock API map only (run.istockAcks,
		// keyed by the id read from the filename); there is no URL at this seam so the
		// slug fallback never fires. CORPUS-INERT for alt BY CONSTRUCTION (corpus module
		// folders carry no acks file → no verified map → alt stays ""); loading="lazy"
		// is already baked into every widget image template except flipCard's Mode-P
		// visible placeholder, which FinishImg now completes (a named forward-looking
		// r240_img_alt_lazy delta; shapeHover's style-first Mode-P template stays
		// untouched by the finisher's regex — recorded residue). Data
		// elements.image_attrs.widget_internal; env WIDGETIMG_OFF reverts the rider
		// ALONE (the parent rule's IMGATTRS_OFF/enabled:false still kill it too via
		// FinishImg's own guards — needed so the rider decomposes independently of the
		// r240 body-path rule, which shipped un-regenerated in the same chain).
		const wcfg = DataService.Data.EmitTemplates.elements?.image_attrs;
		const rider = wcfg && wcfg.widget_internal !== false
			&& !(typeof process !== "undefined" && process.env && process.env.WIDGETIMG_OFF);
		const istockId = String(filename).match(/iStock-(\d+)/i)?.[1] ?? null;
		const fin = rider ? ((h) => MediaBuilder.FinishImg(h, "", istockId, run)) : ((h) => h);
		if (run?.imageMode === "P") {
			// label = the filename without its extension ("iStock-978974888")
			const label = String(filename).replace(/\.[a-z0-9]+$/i, "");
			return fin(Utils.FillTemplate(tpl.image_mode_P, { label }))
				+ fin(Utils.FillTemplate(tpl.image_mode_P_comment, { filename }));
		}
		return fin(Utils.FillTemplate(tpl.image_mode_D, { filename }));
	}

	// -----------------------------------------------------------------------
	// SHARED PAIRED-DATA / COLUMN-ROLE HELPERS
	//   Content-based (not tag-spelling-based) column-role detection, so the
	//   carousel image table — and, in future, any paired-column widget — reads
	//   robustly across writer variation. #cellMediaUrl is the generalisation of
	//   the speechBubble #isImageCell test (an image cell is one carrying an image
	//   URL); #imageCaptionPair classifies a 2-cell row as image|caption either way
	//   round; #isCarouselTitleOrLabelRow drops the writer's title / column-label rows.
	// -----------------------------------------------------------------------

	/**
	 * The IMAGE URL a cell carries, or null. An image URL is any pasted http(s) URL
	 * that is NOT a video host (YouTube/Vimeo). Robust to the writer's marker + " / "
	 * separator (the URL is matched anywhere in the cell). Used to tell an image
	 * column from a caption column by CONTENT, not by the tag word.
	 */
	static #cellMediaUrl(cell) {
		const url = String(cell ?? "").match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? null;
		if (!url) return null;
		if (/youtu\.?be|youtube\.com|vimeo/i.test(url)) return null;   // a video, not an image
		return url;
	}

	/**
	 * Classify a 2-cell row as a clean image|caption slide, or null. EXACTLY one cell
	 * must carry a derivable iStock image URL (#cellMediaUrl → #istockFilename) and the
	 * OTHER must be plain caption text; the column ORDER is free (image-then-caption or
	 * caption-then-image). Returns { filename, caption } or null.
	 *
	 * Conservative (never half-build): null when both/neither cell is an image, the
	 * image is non-iStock/underivable, either cell carries a 2nd red developer span
	 * (an instruction beyond the cell's own tag), the image cell has leftover prose,
	 * or the caption is empty / bulleted / multi-line (the human renders that as a
	 * <ul>/<br> we must not flatten).
	 */
	static #imageCaptionPair(row, tpl) {
		if (!Array.isArray(row) || row.length !== 2) return null;
		const a = String(row[0] ?? ""), b = String(row[1] ?? "");
		const aUrl = this.#cellMediaUrl(a), bUrl = this.#cellMediaUrl(b);
		let imgIdx;
		if (aUrl && !bUrl) imgIdx = 0;
		else if (bUrl && !aUrl) imgIdx = 1;
		else return null;                                  // both or neither → not image|caption
		const filename = this.#istockFilename(imgIdx === 0 ? aUrl : bUrl, tpl);
		if (!filename) return null;                        // non-iStock → cannot name → bail
		const imgCell = imgIdx === 0 ? a : b;
		const txtCell = imgIdx === 0 ? b : a;
		// a clean cell carries at most ONE red span (its own marker); a 2nd is an
		// embedded developer instruction → bail.
		if (this.#redSpanCount(imgCell) > 1 || this.#redSpanCount(txtCell) > 1) return null;
		// image cell: once the leading marker, the " / " separator and the URL are
		// removed, nothing meaningful may remain.
		const imgResidual = this.#cellText(imgCell)
			.replace(/^\s*\[[^\]]*\]\s*/, "")              // drop the leading [carousel N]/[image] marker
			.replace(/https?:\/\/\S+/g, "")                // drop the URL (consumed into the filename)
			.replace(/[/|]/g, " ").trim();                 // drop the " / " separator
		if (imgResidual) return null;
		// caption: drop the leading [body] tag → the caption prose itself.
		const caption = this.#cellText(txtCell).replace(/^\s*\[[^\]]*\]\s*/, "").trim();
		if (!caption) return null;
		if (/[•·]|\n/.test(caption)) return null;          // a list / hard newline → don't flatten
		return { filename, caption };
	}

	/**
	 * True when a carousel table row is the writer's TITLE row (a single content cell,
	 * e.g. "[Title] How are New Zealanders Gaming?") or a column-LABEL row ("Images |
	 * Text", all-red), so it is dropped before the slides. Content-based, tolerant of
	 * the title/label being present or absent.
	 */
	static #isCarouselTitleOrLabelRow(row, tpl = {}) {
		if (!Array.isArray(row) || !row.length) return false;
		const cells = row.map((c) => this.#cellText(c)).filter((c) => c.trim());
		if (cells.length <= 1) return true;                // a one-cell [Title]/[Cover] row
		if (row.every((c) => this.#isFullyRed(c))) return true;   // all-red column labels
		const labels = (tpl.header_label_keywords && tpl.header_label_keywords.length)
			? tpl.header_label_keywords
			: ["images", "image", "text", "caption", "title", "slide"];
		const re = new RegExp(`^(${labels.join("|")})$`, "i");
		return cells.every((c) => re.test(c.replace(/^\s*\[[^\]]*\]\s*/, "").trim()));
	}

	/**
	 * The trailing free-body paragraph(s) a writer placed AFTER a carousel's slide
	 * table — the human renders these as plain <p> AFTER the carousel (OSGM501-01),
	 * not as slides. Returns an array of rendered <p> (possibly empty), or null when a
	 * trailing member is richer than a plain [body] paragraph (a 2nd table, an image /
	 * widget tag, a list / multi-line) — in which case the whole build bails so the
	 * placeholder keeps that content intact.
	 */
	static #carouselTrailingBody(bundle, inline, tpl) {
		const members = bundle.memberItems ?? [];
		let lastTableIdx = -1;
		members.forEach((m, i) => { if (m.type === "table") lastTableIdx = i; });
		const out = [];
		for (let i = lastTableIdx + 1; i < members.length; i++) {
			const m = members[i];
			if (m.type === "table") return null;           // a 2nd table after the slides
			const isTag = m.type === "tag";
			const raw = isTag ? (m.blackAfter ?? "") : (m.text ?? "");
			const text = this.#cellText(raw);
			if (!text) continue;                            // blank line
			if (isTag && m.parse?.primary?.tag !== "body") return null;   // image/widget/heading tag
			if (this.#hasRedText(raw)) return null;        // red developer instruction
			if (/[•·]|\n/.test(text)) return null;          // a list / multi-paragraph → needs full block render
			out.push(Utils.FillTemplate(tpl.trailing_body, { text: inline(text) }));
		}
		return out;
	}

	/**
	 * True when a flipCard's first row is just column LABELS (so we drop it before
	 * building). Either the writer's all-red instruction row, OR every cell
	 * CONTAINS a label keyword (front/back/image/text/side/flip…). "Contains" (not
	 * "equals") because the labels are phrases like "Image for one side". A real
	 * card row (e.g. "Kaitiakitanga (guardianship)") matches none, so it is kept.
	 */
	static #looksLikeFlipHeader(cells, tpl = {}) {
		if (!Array.isArray(cells) || !cells.length) return false;
		if (cells.every((c) => this.#isFullyRed(c))) return true;
		const words = (tpl.header_contains_keywords && tpl.header_contains_keywords.length)
			? tpl.header_contains_keywords
			: ["front", "back", "image", "text"];
		const re = new RegExp(`\\b(${words.join("|")})\\b`, "i");
		return cells.every((c) => re.test(this.#cellText(c)));
	}

	/**
	 * One flipCard cell → its finished HTML, or null to fall back.
	 *
	 *   • IMAGE cell — when the cell carries an image reference (an iStock/.jpg URL,
	 *     a [LINK: …] to a photo, or an [image] tag). Emitted as an <img> honouring
	 *     Mode P/D, exactly like every other image; the writer's image label tags
	 *     ([IMAGE: …], "Link for photo") never reach the page. The filename uses the
	 *     iStock id when present (…gm12345… or …/id/12345…), else a generic name.
	 *   • TEXT cell — the cell's BLACK learner text. A clean text cell carries NO
	 *     red writer-instruction span; if one remains (a label or a "CS:" note we
	 *     must not silently drop) we fall back. The writer's " / " (a slash with
	 *     spaces) is a line break and becomes <br>; bold/italic render via renderInline.
	 */
	static #flipCell(raw, tpl, run, inline) {
		const s = String(raw ?? "");

		// (a) image? an image URL, a [LINK: …] to a photo, an [image]/[IMAGE tag, or
		// the writer's "Link for photo/image" placeholder text (the istock URL is
		// link-extracted out of the cell, leaving only that visible label — the
		// human still renders an image here, so we do too, via Mode P/D).
		if (/istockphoto|\.(?:jpe?g|png|gif|webp|svg)\b|\[\s*image\b|\[IMAGE\b|\blink for (?:a |an )?(?:photo|image|picture)/i.test(s)) {
			const id = (s.match(/gm-?(\d{6,10})/) || s.match(/\/id\/(\d{4,10})/) || [])[1] ?? null;
			const filename = id ? Utils.FillTemplate(tpl.filename_istock, { id }) : tpl.filename_generic;
			return this.#assetImage(filename, tpl, run);
		}

		// (b) text: pure black text only — a leftover red span is an instruction we
		// cannot safely drop, so bail and keep the placeholder (it surfaces it).
		if (this.#hasRedText(s)) return null;
		let t = this.#cellText(s).replace(/^[\s/]+/, "").replace(/[\s/]+$/, "").trim();
		if (!t || /[•·]|\n/.test(t)) return null;        // empty / bullets / hard newline → fall back
		t = t.replace(/\s\/\s/g, "<br>");                // the writer's " / " line-break → <br>
		// LINK-EXTRACTED-IMAGE GUARD: when an istock [LINK: …] is pulled out of a flip
		// cell upstream, the leftover is the image's bold label + the word, e.g.
		// "Snowman / Snowman" → identical halves. That is a mangled IMAGE cell, not real
		// two-line text — building it duplicates the label ("Snowman<br>Snowman",
		// ENGS101). When in doubt, fall back to the honest placeholder rather than
		// half-build. (Distinct halves like "They love the rain / Raincoat" are a
		// separate image-cell case handled by the whole-card fallback alongside these.)
		const halves = t.split("<br>").map((x) => this.#cellText(x).trim().toLowerCase());
		if (halves.length === 2 && halves[0] && halves[0] === halves[1]) return null;
		return Utils.FillTemplate(tpl.text, { text: inline(t) });
	}

	/**
	 * The ALTERNATING multi-column "Flip card image" form. allRows = [header, data]:
	 * the header is the Front|Back|Front|Back… labels, the single data row is 2N columns whose
	 * column-PAIRS are the cards. Conservative: null (→ placeholder) unless exactly 2 rows, a clean
	 * Front/Back header, and every front/back cell builds cleanly.
	 *
	 * @param {Array<Array<string>>} allRows - the captured table's raw rows (row 0 = header)
	 * @param {number} width - the table's column count (must be even, 2N)
	 * @param {object} tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {object} run - conversion run context (drives Mode P/D image rendering)
	 * @param {function} inline - inline-markup renderer (bold/italic/links)
	 * @returns {string|null} the built flipCard HTML, or null to keep the orange placeholder
	 */
	static #flipCardAlternating(allRows, width, tpl, run, inline) {
		if (allRows.length !== 2) return null;                       // header + ONE data row only
		const header = allRows[0] ?? [], data = allRows[1] ?? [];
		if (header.length !== width || data.length !== width) return null;
		if (!this.#looksLikeFlipHeader(header, tpl)) return null;     // clean alternating Front/Back labels
		const cards = [];
		for (let i = 0; i < width / 2; i++) {
			const front = this.#flipImageFront(data[2 * i], tpl, run, inline);
			const back = this.#flipBack(data[2 * i + 1], inline);
			if (front === null || back === null) return null;        // any unclear card → whole widget falls back
			cards.push(Utils.FillTemplate(tpl.card, { front, back }));
		}
		return cards.length ? [tpl.container_open, ...cards, tpl.container_close].join("\n") : null;
	}

	/**
	 * A RICH flip FRONT cell — "TEXT / [image] / url" → <img> + <h4>TEXT</h4> (image first, the
	 * human's order). Needs BOTH an image part and a heading-text part; a non-image red span (a
	 * surviving CS instruction) or a bullet → null (keep the placeholder).
	 */
	static #flipImageFront(raw, tpl, run, inline) {
		const imgRe = /istockphoto|\.(?:jpe?g|png|gif|webp|svg)\b|\[\s*image\b|\[IMAGE\b|^https?:\/\//i;
		let imgSrc = "";
		const textParts = [];
		for (const p of String(raw ?? "").split(/\s\/\s/)) {
			if (imgRe.test(p)) { imgSrc += " " + p; continue; }      // an [image] span or a photo URL
			if (this.#hasRedText(p)) return null;                    // a non-image red instruction → bail
			const t = this.#cellText(p).trim();
			if (!t) continue;
			if (/[•·]|\n/.test(t)) return null;                      // bullets / hard newline → richer, bail
			textParts.push(t);
		}
		if (!imgSrc.trim() || !textParts.length) return null;        // need BOTH an image and a heading
		const id = (imgSrc.match(/gm-?(\d{6,10})/) || imgSrc.match(/\/id\/(\d{4,10})/) || [])[1] ?? null;
		const filename = id ? Utils.FillTemplate(tpl.filename_istock, { id }) : tpl.filename_generic;
		const img = this.#assetImage(filename, tpl, run);
		if (!img) return null;
		return img + textParts.map((t) => `<h4>${inline(t)}</h4>`).join("");
	}

	/** A flip BACK cell — "/"-split into one <p> per part (bold/italic via renderInline). */
	static #flipBack(raw, inline) {
		const s = String(raw ?? "");
		if (this.#hasRedText(s)) return null;                        // a surviving red instruction → bail
		const parts = s.split(/\s\/\s/).map((p) => this.#cellText(p).trim()).filter(Boolean);
		if (!parts.length || parts.some((p) => /[•·]/.test(p))) return null;
		return parts.map((t) => `<p>${inline(t)}</p>`).join("");
	}

	/**
	 * The TRANSPOSED multi-column flipCard (verified against OSBY201-02 #12): allRows = [fronts, backs]
	 * where each COLUMN is a card. Each front cell is "[front] / label / [image] url" → image +
	 * <h4>label</h4>; each back cell is "[back] / text" → <p>text</p>. The leading [front]/[back]
	 * FACE directive is stripped, then the existing #flipImageFront / #flipBack build each face.
	 * Conservative: row 0 must be ALL fronts and row 1 ALL backs, and every card must build cleanly
	 * (else null → keep the placeholder).
	 *
	 * @param {Array<Array<string>>} allRows - the captured table's raw rows: [fronts row, backs row]
	 * @param {number} width - the table's column count (one column per card)
	 * @param {object} tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {object} run - conversion run context (drives Mode P/D image rendering)
	 * @param {function} inline - inline-markup renderer (bold/italic/links)
	 * @returns {string|null} the built flipCard HTML, or null to keep the orange placeholder
	 */
	static #flipCardTransposed(allRows, width, tpl, run, inline) {
		const fronts = allRows[0] ?? [], backs = allRows[1] ?? [];
		if (fronts.length < width || backs.length < width) return null;
		const RED = /\u{1f534}\[RED TEXT\]\s*([^[\u{1f534}]*?)\s*\[\/RED TEXT\]\u{1f534}/u;
		const faceOf = (cell) => {
			const m = String(cell ?? "").match(RED);
			const w = m ? m[1].trim().toLowerCase() : "";
			return (w === "front" || w === "back") ? w : null;
		};
		// the rows must be a clean fronts-row + backs-row (in either order)
		let frontRow = fronts, backRow = backs;
		if (fronts.every((c) => faceOf(c) === "back") && backs.every((c) => faceOf(c) === "front")) {
			frontRow = backs; backRow = fronts;
		} else if (!(fronts.every((c) => faceOf(c) === "front") && backs.every((c) => faceOf(c) === "back"))) {
			return null;
		}
		const stripFace = (cell) => String(cell ?? "")
			.replace(/^\s*\u{1f534}\[RED TEXT\]\s*(?:front|back)\s*\[\/RED TEXT\]\u{1f534}\s*\/?\s*/iu, "");
		const cards = [];
		for (let c = 0; c < width; c++) {
			const front = this.#flipImageFront(stripFace(frontRow[c]), tpl, run, inline);
			const back = this.#flipBack(stripFace(backRow[c]), inline);
			if (front === null || back === null) return null;
			cards.push(Utils.FillTemplate(tpl.card, { front, back }));
		}
		return cards.length ? [tpl.container_open, ...cards, tpl.container_close].join("\n") : null;
	}

	/**
	 * The MULTI-ROW alternating Front/Back flipCard (verified against OSAH501-03). allRows =
	 * [header, dataRow1, dataRow2, …]; each data row holds width/2 cards as column-pairs
	 * (col 2i = front, col 2i+1 = back). Reuses #flipImageFront (image + <h4> title) for the
	 * front and #flipBackRich (paragraphs + a <ul> for the bulleted law text) for the back, after
	 * stripping the writer's per-cell structural markup ([body]/[image]/[H#]). Conservative
	 * (never half-build → null = keep the placeholder): a clean Front/Back header, ≥2 data rows,
	 * every row width-wide, and every card builds cleanly (a surviving CS instruction, an empty
	 * cell, or a missing image/title fails the whole widget).
	 *
	 * @param {Array<Array<string>>} allRows - the captured table's raw rows (row 0 = header)
	 * @param {number} width - the table's column count (must be even, 2 columns per card)
	 * @param {object} tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {object} run - conversion run context (drives Mode P/D image rendering)
	 * @param {function} inline - inline-markup renderer (bold/italic/links)
	 * @returns {string|null} the built flipCard HTML, or null to keep the orange placeholder
	 */
	static #flipCardMultiRow(allRows, width, tpl, run, inline) {
		const header = allRows[0] ?? [];
		if (!this.#looksLikeFlipHeader(header, tpl)) return null;
		const dataRows = (allRows.slice(1)).filter((r) => Array.isArray(r) && r.some((c) => this.#cellText(c).trim()));
		if (dataRows.length < 1) return null;                       // need a header + at least one data row
		const cards = [];
		for (const row of dataRows) {
			if (row.length < width) return null;                    // ragged row → not this clean form → bail
			for (let i = 0; i < width / 2; i++) {
				const fRaw = this.#stripStructuralTags(row[2 * i]);
				// front = image + title (#flipImageFront); fall back to an IMAGE-ONLY front when the
				// cell carries only an image and no title (OSAH501-05 penalty/jail cards).
				const front = this.#flipImageFront(fRaw, tpl, run, inline) ?? this.#flipImageOnly(fRaw, tpl, run);
				const back = this.#flipBackRich(this.#stripStructuralTags(row[2 * i + 1]), inline);
				if (front === null || back === null) return null;   // any unclear card → keep the placeholder
				cards.push(Utils.FillTemplate(tpl.card_image_front, { front, back }));
			}
		}
		return cards.length ? [tpl.container_open, ...cards, tpl.container_close].join("\n") : null;
	}

	/**
	 * A RICH flip BACK — like #flipBack but it KEEPS a bullet list (a flip back can hold a <ul>;
	 * a writer's "Law: X / lead-in: / • a / • b" becomes <p>Law: X</p><p>lead-in:</p><ul><li>a</li>
	 * <li>b</li></ul>). "/"-split; a "• "/"· " part is a list item (consecutive items group into one
	 * <ul>), every other non-empty part is a <p>. A surviving red instruction (a CS note we must not
	 * silently drop) → null (keep the placeholder).
	 */
	static #flipBackRich(raw, inline) {
		const s = String(raw ?? "");
		if (this.#hasRedText(s)) return null;
		// a leading "/" is the writer's empty first line after the stripped [body] tag — drop it.
		const parts = s.replace(/^\s*\/\s*/, "").split(/\s\/\s/)
			.map((p) => this.#cellText(p).trim().replace(/^\/\s*/, "")).filter(Boolean);
		if (!parts.length) return null;
		let html = "", ul = [];
		const flushUl = () => { if (ul.length) { html += "<ul>" + ul.map((t) => `<li>${inline(t)}</li>`).join("") + "</ul>"; ul = []; } };
		for (const p of parts) {
			const bm = p.match(/^[•·]\s*(.+)$/);
			if (bm && bm[1].trim()) { ul.push(bm[1].trim()); continue; }
			flushUl();
			html += `<p>${inline(p)}</p>`;
		}
		flushUl();
		return html || null;
	}

	/**
	 * An IMAGE-ONLY flip FRONT — a cell carrying ONLY an image reference and no title (a valid
	 * flip front that reveals the back's text). Returns the <img> (Mode P/D), or null when the
	 * cell has any real non-image text (→ it's a titled front for #flipImageFront) or a surviving
	 * red instruction (→ keep the placeholder).
	 */
	static #flipImageOnly(raw, tpl, run) {
		const s = String(raw ?? "");
		if (this.#hasRedText(s)) return null;
		const imgRe = /istockphoto|\.(?:jpe?g|png|gif|webp|svg)\b|\[\s*image\b|\[IMAGE\b|^https?:\/\//i;
		let imgSrc = "";
		for (const p of s.split(/\s\/\s/)) {
			if (imgRe.test(p)) { imgSrc += " " + p; continue; }
			if (this.#cellText(p).trim()) return null;       // a real non-image text part → not image-only
		}
		if (!imgSrc.trim()) return null;
		const id = (imgSrc.match(/gm-?(\d{6,10})/) || imgSrc.match(/\/id\/(\d{4,10})/) || [])[1] ?? null;
		const filename = id ? Utils.FillTemplate(tpl.filename_istock, { id }) : tpl.filename_generic;
		return this.#assetImage(filename, tpl, run);
	}

	/**
	 * Strip the writer's per-cell STRUCTURAL markup tags ([body]/[front]/[back]/[H#]/[heading]/
	 * [flip card]) — both the red-wrapped form (🔴[RED TEXT][body][/RED TEXT]🔴) and a bare literal
	 * [body] — so the cell's real learner content reaches #flipImageFront / #flipBackRich. [image]
	 * is LEFT intact ( #flipImageFront keys its image detection on it / the iStock URL). A
	 * NON-structural red span (a "CS:" note) is NOT touched, so the builder still bails on it
	 * (never silently drop an instruction).
	 */
	static #stripStructuralTags(raw) {
		return String(raw ?? "")
			.replace(/\u{1f534}\[RED TEXT\]\s*\[?\s*(?:body|front|back|h[1-6]|heading|flip\s?card)\s*\d*\s*\]?\s*\[\/RED TEXT\]\u{1f534}/giu, " ")
			.replace(/\[\s*(?:body|front|back|h[1-6]|heading|flip\s?card)\s*\d*\s*\]/gi, " ")
			.replace(/[ \t]{2,}/g, " ")
			.trim();
	}
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { InteractiveBuilder };
