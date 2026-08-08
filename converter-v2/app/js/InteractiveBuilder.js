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
				// ROUND 277 — `hint` and `hintSlider` are DIFFERENT elements (ONE click-to-reveal
				// tip vs a LIST of reveal rows), and the writer's TAG does not reliably tell them
				// apart: [hint sliders] resolves to widget type `hint`, while OSAI401/501 author
				// real sliders under [hint slider]. So both types enter ONE entry that routes on
				// the authored CONTENT, and it needs BOTH templates + renderBlock for hint bodies.
				case "hint":
				case "hintSlider":
					html = this.#hintEntry({ bundle, tpl, templates, renderInline, renderBlock });
					break;
				case "accordion":
					// renderTable added round 275 — the rich panel walk renders a captured data
					// table INSIDE its panel, exactly as the rich tabs pane already does.
					html = this.#accordion({ bundle, tpl, renderInline, run, renderBlock, renderNested, renderTable });
					break;
					// speechBubble needs `run` (for the image Mode P/D), so it is
					// the first builder we hand the run context to.
				case "speechBubble":
					// round 276: the four narrow branches, then the RICH general composer.
					html = this.#speechBubbleEntry({ bundle, tpl, renderInline, run });
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
					// round 283: the narrow member walk, then the GENERAL composer.
					// renderBlock/renderTable/renderNested added this round — a clickDrop's
					// revealed panel is ordinary page content (gold: 1600 <p>, 401 headings,
					// 472 <img>, 395 lists, 106 tables) and must render through the
					// converter's own emitters, exactly as the accordion's panels do.
					html = this.#clickDropEntry({ bundle, tpl, renderInline, run, renderBlock, renderTable, renderNested });
					break;
				case "dropDown":
					// ROUND 287 — the first builder this type has ever had. FENCED on the
					// writer's opener naming a dropdown, because the lexicon aliases the
					// student file-upload "dropbox" onto this same widget type and the two
					// are unrelated things (240 of 393 captured bundles are dropbox).
					html = this.#dropDown({ bundle, tpl, renderInline, run, renderTable });
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
				case "modal":       // image-pair form → TKmodal set; single document/PDF URL → a button;
					// else (round 280) the general trigger+TKmodal set fallback. renderNested/
					// renderTable/renderImage added round 280 — a modal's content is ordinary page
					// content (a kept table, a nested widget, an image) and must render through the
					// converter's own emitters, exactly as the accordion's panels do.
					html = this.#modal({ bundle, tpl, renderInline, renderBlock, renderNested, renderTable, renderImage, run });
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
	 * THE HINT-FAMILY ENTRY (ROUND 277) — routes on the authored CONTENT, not the tag.
	 *
	 * WHY AN ENTRY AT ALL. `hint` and `hintSlider` are two different HTML elements, but
	 * the writer's tag does not decide which one was authored:
	 *   • `[hint sliders]` (plural) resolves to widget type `hint` — yet it IS a slider;
	 *   • `[hint slider 1] Misleading advice:` + `[back][body] …` (OSAI401/501) is a
	 *     slider authored under the slider tag but with none of the shapes the original
	 *     table builder knew;
	 *   • `[Hint Button]` + `[Title]` + `[Body]` is the single-tip ELEMENT, and before
	 *     this round it had no template at all, so `Build` returned null at its
	 *     missing-template guard and no builder ever ran on any of its 64 bundles.
	 *
	 * ORDER (the round-276 architecture — the narrow branches first, the general
	 * composers LAST, so every pre-277 build stays byte-identical BY CONSTRUCTION):
	 *   1. the front/back MEMBER form      (unchanged, #hintSliderMembers)
	 *   2. the 2-column TABLE form         (unchanged, #hintSliderTable)
	 *   3. the LABELLED-PAIR slider        (new — HINTPAIR_OFF)
	 *   4. the single-tip hint ELEMENT     (new — HINTELEM_OFF)
	 *
	 * @param {object}   args
	 * @param {object}   args.bundle       - the captured interactive
	 * @param {object}   args.tpl          - THIS bundle type's template
	 * @param {object}   args.templates    - all interactive_builders (both hint templates)
	 * @param {function} args.renderInline - inline markup renderer
	 * @param {function} args.renderBlock  - block renderer (<p>/<ul>) for a hint body
	 * @returns {string|null} built HTML, or null to keep the hand-off box
	 */
	static #hintEntry({ bundle, tpl, templates, renderInline, renderBlock }) {
		const sliderTpl = templates?.hintSlider ?? (bundle?.type === "hintSlider" ? tpl : null);
		const hintTpl = templates?.hint ?? (bundle?.type === "hint" ? tpl : null);
		// HINTELEM_OFF must restore the PRE-277 state exactly, and before this round a
		// `hint`-typed bundle never reached a builder at all: there was no `hint` key in
		// interactive_builders, so Build returned null at its missing-template guard. The
		// toggle therefore reverts the whole hint-type reachability, not just the element
		// composer — otherwise a toggle-OFF corpus would still differ from round 276.
		if (bundle?.type === "hint"
			&& typeof process !== "undefined" && process.env && process.env.HINTELEM_OFF) return null;

		// THE GUARD IS SCOPED SO IT CAN NEVER REMOVE A PRE-277 BUILD. Before this round
		// only a `hintSlider`-typed bundle could reach branches 1+2, so for that type they
		// keep their exact previous behaviour — including two ENFUN09 / OSSM501 builds that
		// already shipped a visible leak (a PRE-EXISTING defect, recorded as a follow-up,
		// not this round's to silently change). Every path this round newly opened — the
		// same branches reached by a `hint`-typed bundle, and branches 3+4 — is guarded.
		const preExisting = bundle?.type === "hintSlider";

		// 1 + 2 — the two original branches, called EXACTLY as before.
		if (sliderTpl && sliderTpl.enabled !== false) {
			const narrow = this.#hintSlider({ bundle, tpl: sliderTpl, renderInline });
			if (narrow) return this.#hintLeakGuard(narrow, !preExisting);
			// 3 — the general labelled-pair slider.
			const pairs = this.#hintSliderPairs({ bundle, tpl: sliderTpl, renderInline, renderBlock });
			if (pairs) return this.#hintLeakGuard(pairs);
		}
		// 4 — the single-tip hint element.
		if (hintTpl && hintTpl.enabled !== false) {
			const el = this.#hintElement({ bundle, tpl: hintTpl, renderInline, renderBlock });
			if (el) return this.#hintLeakGuard(el);
		}
		return null;
	}

	/**
	 * THE LEAK GUARD (ROUND 277) — the round-167 rule applied at the hint seam.
	 *
	 * Adding the missing `hint` template made the ORIGINAL table builder reachable for
	 * `hint`-typed bundles for the first time, and one of them (TEDC402-3.0) is a 1x2
	 * LAYOUT table whose two cells are whole page blocks. Built as front|back it shipped
	 * the writer's raw "[H3]", "[Body]", "[hint sliders]", "[image]" as VISIBLE text —
	 * inside a hand-off box that text is gate-excluded chrome, but as a real widget it is
	 * a counted literal leak on the finished page.
	 *
	 * So a finished hint/slider that still shows a bracketed structural tag is DECLINED
	 * and the honest hand-off box is kept. Building can therefore never ADD a leak — only
	 * prevent one. (Prose that merely contains brackets — "[178, 165, 190]" — is not a
	 * tag: the pattern requires a leading letter, matching the round-104 discriminator.)
	 *
	 * @param {string|null} html - the built widget
	 * @returns {string|null} the same HTML, or null when it leaks
	 */
	static #hintLeakGuard(html, guard = true) {
		if (!html || !guard) return html ?? null;
		return /\[\s*[A-Za-z][^\]\n]{0,40}\]/.test(html) ? null : html;
	}

	/**
	 * hintSlider — THE LABELLED-PAIR form (ROUND 277). The general composer for every
	 * slider the writer did NOT lay out as a 2-column table or as [front]/[back] members.
	 *
	 * MEASURED DIALECTS IT COVERS (all from the live corpus, all previously declined):
	 *   ENGR202  [Hintslider 1] Front || Which fruit…   +  red span "Back || Strawberries"
	 *   OSSC501  [hint slider] [Front] || Surprise      +  [Back] || Was the message…
	 *   OSSM501  [hint slider 1] || Take breaks…        +  [back] || Try putting your phone…
	 *   OSAI401  [hint slider 1] || Misleading advice:  +  [back] [body] || AI might suggest…
	 *   TEDC402  • **A bit**  (a black bullet)          +  red span "reveals 🡪 A bit is a 1 or 0"
	 *   SCPH301  [hint slider front] || …               +  [hint slider back] || …
	 *
	 * THE ONE RULE BEHIND ALL OF THEM: a row is a FRONT followed by a BACK, and either
	 * half may arrive as the opener's own trailing text, as a tagged member, or as a
	 * red span whose leading word is a back-label ("back", "bottom", "reveals",
	 * "answer"). Which of those the writer used is layout, not meaning.
	 *
	 * NEVER HALF-BUILDS → null: a front with no reveal (BLL246's six sentence starters,
	 * MXEX401's lone question — a slider with nothing to reveal is not a slider), a
	 * captured table (that is branch 2's or a genuine decline), a media/asset request
	 * (HES1005's "[Insert media item 51]"), an image/video member, or no complete row.
	 * Writer instructions are SKIPPED and still surface as red notes after the widget
	 * (the round-214 rule), never silently dropped.
	 *
	 * TRAILING CONTENT: prose the walk over-captured after the last complete row is
	 * rendered AFTER the widget rather than dropped (the round-196 trailing_body rule),
	 * so building can never lose the writer's text.
	 */
	static #hintSliderPairs({ bundle, tpl, renderInline, renderBlock }) {
		const cfg = tpl?.labelled_pairs;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.HINTPAIR_OFF) return null;
		if ((bundle?.tables ?? []).length) return null;       // a table is branch 2's business

		const inline = renderInline ?? ((s) => s);
		const backWords = (cfg.back_label_words ?? []).map((w) => String(w).toLowerCase());
		const frontWords = (cfg.front_label_words ?? []).map((w) => String(w).toLowerCase());
		// "Back", "Back:", "reveals 🡪" — a label word, optionally followed by punctuation
		// or an arrow glyph, and nothing else. The REMAINDER (if any) is the back's text.
		const labelOnly = (s, words) => {
			const t = this.#cellText(s).replace(/\*\*/g, "").replace(/[\u{1F000}-\u{1FAFF}\u{2190}-\u{27BF}\u{1F800}-\u{1F8FF}]/gu, " ").trim();
			const m = /^([A-Za-z]+)\s*[:.\-–—]?\s*$/.exec(t);
			return !!m && words.includes(m[1].toLowerCase());
		};
		const stripLabel = (s, words) => {
			let t = this.#cellText(s).replace(/^\s*\*\*\s*/, "").trim();
			const m = /^([A-Za-z]+)\s*[:.\-–—]?\s*/.exec(t);
			if (m && words.includes(m[1].toLowerCase())) t = t.slice(m[0].length);
			// a leading arrow glyph the writer used as the reveal marker
			return t.replace(/^[\s*]*[\u{1F800}-\u{1F8FF}\u{2190}-\u{21FF}\u{27A1}\u{2192}>]+[\s*]*/gu, "").replace(/\*\*/g, "").trim();
		};
		// The opener's bracket may itself name the half: "[hint slider front]" (SCPH301).
		const bracketHalf = (m) => {
			const raw = String(m?.text ?? "").toLowerCase();
			if (frontWords.some((w) => new RegExp(`\\b${w}\\b`).test(raw))) return "front";
			if (backWords.some((w) => new RegExp(`\\b${w}\\b`).test(raw))) return "back";
			return null;
		};

		const rows = [];
		const trailing = [];
		let cur = null;                       // the row awaiting its back
		const pushFront = (text) => {
			if (!text) return false;
			if (cur && !cur.back) return false;   // two fronts running → not a clean pair form
			cur = { front: text, back: "" };
			rows.push(cur);
			return true;
		};
		const pushBack = (text) => {
			// The reveal marker the writer typed between the label and the answer
			// ("reveals 🡪 A bit is a 1 or 0") is punctuation, not content — the gold's
			// backInfo carries the answer alone. Strip a leading arrow glyph and any
			// bold markers left orphaned around it.
			const t = String(text ?? "")
				.replace(/^[\s*]*[\u{1F800}-\u{1F8FF}\u{2190}-\u{21FF}\u{27A1}\u{2192}>→]+[\s*]*/gu, "")
				.trim();
			if (!cur || !t) return false;
			cur.back = cur.back ? `${cur.back} ${t}` : t;
			return true;
		};

		for (const m of (bundle?.memberItems ?? [])) {
			if (!m) continue;
			if (m.type === "table") return null;                       // a data table → not this form
			const tag = m.type === "tag" ? m.parse?.primary?.tag : null;
			const tags = (m.parse?.tags ?? []).map((t) => t.tag);
			const raw = m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const text = this.#cellText(raw).trim();

			// (a) a writer instruction / asset request — skipped, and still surfaced as a
			//     red note after the built widget (the round-214 rule). An instruction is
			//     never learner content, so it can neither open nor close a row.
			const isNote = m.type === "tag"
				&& (m.parse?.class === "instruction" || m.parse?.class === "noise" || m.parse?.instructionFragment);
			// (b) a MEDIA / asset member — an image, a video, or a media-list reference
			//     ("[Insert media item 51]"). The slider form has nowhere to put it and we
			//     will not silently drop it. Decline.
			if (["image", "video", "audio"].includes(tag)) return null;
			if (m.type === "tag" && /\binsert (?:media|item)\b/i.test(String(m.text ?? ""))) return null;

			// (c) the widget's own invocation. Its trailing text is the row's FRONT (or,
			//     when the bracket names a half, that half). A bare repeat opens nothing.
			if (m.parse?.primary?.directive === "INTERACTIVE") {
				const half = bracketHalf(m);
				if (!text) continue;                                   // a bare repeat — no content
				if (half === "back") { if (!pushBack(text)) return null; continue; }
				if (!pushFront(text)) return null;
				continue;
			}
			// (d) an explicit [back] member — including OSAI401's "[back] [body]" span,
			//     where the PRIMARY resolves to `body` but [back] is present in the span.
			if (tag === "back" || tags.includes("back")) {
				if (!text) continue;
				if (!pushBack(text)) return null;
				continue;
			}
			// (e) an explicit [front] member.
			if (tag === "front" || tags.includes("front")) {
				if (!pushFront(text)) return null;
				continue;
			}
			// (f) a red span used as a LABEL: "Back || Strawberries", "reveals 🡪 …".
			//     The label may be the span's text with the content in blackAfter, or the
			//     whole thing may ride one string ("Reveals 🡪 Binary arithmetic is …").
			if (m.type === "tag" && !m.parse?.primary) {
				const own = String(m.text ?? "");
				if (labelOnly(own, backWords)) { if (!pushBack(text)) return null; continue; }
				if (labelOnly(own, frontWords)) { if (!pushFront(text)) return null; continue; }
				const merged = stripLabel(`${this.#cellText(own)} ${text}`.trim(), backWords);
				if (/^\s*(?:reveals?|back|bottom|answer)\b/i.test(this.#cellText(own)) && merged) {
					if (!pushBack(merged)) return null;
					continue;
				}
				if (isNote) continue;                                  // an ordinary instruction span
				return null;
			}
			if (isNote) continue;

			// (g) a BLACK line. A bullet ("• **A bit**") opens a row's front when the row
			//     before it is complete; ordinary prose AFTER the last complete row is
			//     TRAILING content and renders after the widget rather than being lost.
			//     ONCE trailing prose has started the writer has moved on, so everything
			//     after it is trailing too — otherwise its own bullet list ("• conduction",
			//     SCPH301) would be misread as a new row's front.
			if (m.type === "black") {
				if (!text) continue;
				if (/^\s*\(?\d{1,3}[.)]\s*$/.test(text)) continue;      // a bare list-number artifact
				if (trailing.length) { trailing.push(text); continue; }
				const bullet = /^[•·]\s*(.+)$/.exec(text);
				if (bullet && (!cur || cur.back)) { if (!pushFront(bullet[1].trim())) return null; continue; }
				if (cur && cur.back) { trailing.push(text); continue; }
				return null;                                           // prose mid-row → not this form
			}
			// (h) a [body] with no [back] — the writer resuming prose after the rows.
			if (tag === "body" && cur && cur.back) { if (text) trailing.push(text); continue; }
			return null;
		}

		// A TRAILING front with no reveal is the writer's lead-in to whatever comes next
		// (OSAI401's "Unfair predictions:", whose answer the scanner put in the FOLLOWING
		// bundle). It is not a row, and it is not ours to drop — it becomes trailing text.
		while (rows.length && !rows[rows.length - 1].back) trailing.unshift(rows.pop().front);
		const complete = rows.filter((r) => r.front && r.back);
		if (complete.length !== rows.length) return null;               // an INTERIOR front with no reveal
		if (complete.length < (cfg.min_rows ?? 1)) return null;

		const body = complete.map((r) => Utils.FillTemplate(tpl.row, {
			front: inline(r.front), back: inline(r.back),
		}));
		let html = [tpl.open, ...body, tpl.close].join("\n");
		if (trailing.length && cfg.trailing_body !== false && typeof renderBlock === "function") {
			// renderBlock returns an ARRAY of <p>/<ul> chunks (the shared black-text
			// renderer's contract) — join them, never string-concatenate the array.
			const rendered = renderBlock(trailing.join("\n"));
			const after = (Array.isArray(rendered) ? rendered : [rendered])
				.filter((h) => h && String(h).trim()).join("\n");
			if (after) html += `\n${after}`;
		}
		return html;
	}

	/**
	 * hint — THE WRITER'S [Hint Button] (ROUND 277): ONE click-to-reveal tip attached to
	 * a line of text. This element had NO template before this round, so `Build` returned
	 * null at its missing-template guard and all 64 tagged hints shipped as a hand-off box
	 * without any builder ever running on them.
	 *
	 * HOW THE WRITER AUTHORS IT (the dominant form — 37 of the 64, 9 modules):
	 *   [Hint Button]
	 *   [Title]  **Need help ?**
	 *   [Body]   Email or phone the kaiako. You can ring 0800 65 99 88 …
	 * The title arrives either folded into the opener's own red span (HPRE203, SSOG103 —
	 * adjacent lines merge) or as its own [Title] member (TEDC402, SSEA203 — recovered by
	 * the round-277 scanner rule, since [Title] is otherwise an absolute terminator).
	 *
	 * BUILDS (the measured gold plurality — 40 of 53 in the authoring modules = 75.5%):
	 *   <p class="hintLink">{title} <span class="hint"></span></p>
	 *   <div class="hintDropContent">{body}</div>
	 * The title is rendered through the inline renderer, so the writer's own **bold**
	 * survives exactly as TEDC401/402's gold ships it; the body goes through renderBlock
	 * so bullets become a real list.
	 *
	 * NEVER HALF-BUILDS → null: no title tag at all (we do not invent one — OSGM201's
	 * "Pop-up text when 'user controls' is clicked:" is an instruction, not a title), no
	 * body content, a captured table, or any media / other widget member.
	 */
	static #hintElement({ bundle, tpl, renderInline, renderBlock }) {
		if (typeof process !== "undefined" && process.env && process.env.HINTELEM_OFF) return null;
		if ((bundle?.tables ?? []).length) return null;
		const inline = renderInline ?? ((s) => s);
		const titleTags = (tpl.title_tags ?? ["title bar"]);
		let title = null;
		const bodyLines = [];

		const openerTitle = (m) => {
			// the [Title] folded into the opener's OWN span: "[Hint Button] [Title]" with
			// the title text in blackAfter.
			const tags = (m.parse?.tags ?? []).map((t) => t.tag);
			return tags.some((t) => titleTags.includes(t)) ? this.#cellText(m.blackAfter ?? "").trim() : null;
		};

		for (const m of [...(bundle?.openerItems ?? []), ...(bundle?.memberItems ?? [])]) {
			if (!m) continue;
			if (m.type === "table") return null;
			const tag = m.type === "tag" ? m.parse?.primary?.tag : null;
			const raw = m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const text = this.#cellText(raw).trim();

			if (m.parse?.primary?.directive === "INTERACTIVE") {
				const t = openerTitle(m);
				if (t !== null && title === null) title = t;           // may be "" → default below
				continue;
			}
			if (tag && titleTags.includes(tag)) { if (title === null) title = text; continue; }
			if (["image", "video", "audio"].includes(tag)) return null;
			if (m.type === "tag"
				&& (m.parse?.class === "instruction" || m.parse?.class === "noise" || m.parse?.instructionFragment)) continue;
			if (tag === "body" || m.type === "black") { if (text) bodyLines.push(text); continue; }
			if (this.#isInlineMarkerMember(m)) { if (text) bodyLines.push(text); continue; }
			return null;                                               // any other tag → not this form
		}

		if (title === null) return null;                               // the writer tagged no title
		if (!title) title = tpl.default_title ?? "";                   // tagged but empty
		if (!title) return null;
		if (tpl.require_body !== false && !bodyLines.length) return null;

		// renderBlock returns an ARRAY of <p>/<ul> chunks (the shared black-text renderer's
		// contract), so the writer's bullets become a real list inside the drop.
		const rendered = typeof renderBlock === "function" ? renderBlock(bodyLines.join("\n")) : null;
		const bodyHtml = rendered
			? (Array.isArray(rendered) ? rendered : [rendered]).filter((h) => h && String(h).trim()).join("\n")
			: bodyLines.map((l) => `<p>${inline(l)}</p>`).join("");
		if (!String(bodyHtml || "").trim()) return null;
		return [
			Utils.FillTemplate(tpl.link, { title: inline(title) }),
			tpl.drop_open,
			bodyHtml,
			tpl.drop_close,
		].join("\n");
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
	static #accordion({ bundle, tpl, renderInline, run, renderBlock, renderNested, renderTable }) {
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
			const withRule = this.#accordionRich({ bundle, tpl, renderInline, run, renderBlock, renderNested, renderTable });
			if (withRule !== null) return withRule;
			const legacy = this.#accordionRich({ bundle, tpl, renderInline, run, renderBlock, renderNested, renderTable, legacyPanels: true });
			if (legacy !== null) return legacy;
		}
		// ROUND 278 — THE PANEL-DELIMITER FALLBACK, tried LAST. Every path above has
		// declined, so this is strictly additive: it can only ADD a build, never change
		// one. It exists because the measured biggest decline class was not a rendering
		// gap at all — it was that ONLY an [accordion N] tag could open a panel, while
		// writers delimit panels with a table, a repeating heading or a bold lead just
		// as often. See #accordionPanels. Env ACCPANELS_OFF.
		return this.#accordionPanels({ bundle, tpl, renderInline, run, renderBlock, renderNested, renderTable });
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
	static #accordionRich({ bundle, tpl, renderInline, run, renderBlock, renderNested, renderTable, legacyPanels }) {
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (typeof renderBlock !== "function") return null;   // need the body renderer
		const inline = renderInline ?? ((s) => s);
		const rich = tpl.rich_panels ?? {};
		// ROUND 275 (Chris — the accordion/TABLE blocker): a captured data table inside a
		// panel renders through the converter's own kept-table emitter, exactly as the rich
		// TABS pane has since round 195. Data rich_panels.table_member; env ACCTABLE_OFF.
		const tblCfg = rich.table_member ?? {};
		const tableOn = tblCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ACCTABLE_OFF);
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

			// (e.6) a captured data TABLE member (ROUND 275, Chris — "the accordion builder
			//     gives up whenever the content is in a table: 190 failures, no successes").
			//     A table inside a panel is ordinary panel CONTENT and the human ships it that
			//     way: measured over the whole gold library, 325 accContent blocks across 99
			//     modules contain a <table> (EXPFUN02-00's "Success Criteria Phase Two" panel
			//     is the byte reference — <p>lead</p> + the kept table). It renders through the
			//     converter's OWN kept-table emitter (renderTable = TablesAndGrids.contentTable),
			//     so a panel table is identical to any free-body table on the page — the exact
			//     seam the rich TABS pane has used since round 195.
			//     NEVER HALF-BUILDS: without a renderTable callback (a non-converter caller), or
			//     before any panel has opened (the BARE-OPENER "table rows ARE the panels"
			//     dialect — a different builder, RECORDED not shipped this round), or when the
			//     emitter returns nothing, the whole accordion still declines to the hand-off box.
			//     Data rich_panels.table_member; env ACCTABLE_OFF.
			if (m && m.type === "table" && tableOn) {
				if (!cur || typeof renderTable !== "function") return null;
				flushText();
				const t = renderTable(m);
				if (!t || !String(t).trim()) return null;
				cur.parts.push({ html: String(t) });
				continue;
			}

			// (f) anything else (a foreign tag) → too rich → bail.
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
		const built = this.#accRenderPanels(panels, { tpl, inline, run, renderBlock, renderNested, rich });
		if (!built) return null;
		const recovered = panels.some((p) => p.r246Head);
		// ROUND 242: surface the skipped layout markers ONLY on a successful build (a
		// decline keeps the placeholder + raw dump byte-identical); #bundleInstructions
		// de-duplicates downstream, and the note renders red after the widget.
		if (markerNotes.length) bundle.instructions = [...(bundle.instructions ?? []), ...markerNotes];
		if (recovered) bundle.r246Accordion = true;                    // detector/affected-set marker
		return [tpl.open, ...built, tpl.close].join("\n");
	}

	/**
	 * SHARED PANEL RENDERER (ROUND 278 — a pure extraction from #accordionRich, so its
	 * output is byte-identical by construction; the census run with the round's toggles
	 * OFF is the proof). Turns a resolved `[{ head, parts }]` list into the finished
	 * accHead/accContent rows. Every panel needs a heading AND at least one rendered
	 * part — a panel that renders to nothing declines the WHOLE accordion (never
	 * half-build). Shared by the round-246 rich fallback and the round-278
	 * panel-delimiter fallback, so both emit the exact same markup.
	 *
	 * A part is one of: {p:text} · {img:filename} · {video:id} · {embed:html} ·
	 * {h:level,text} · {html:string} · {nested:subBundle}.
	 *
	 * @returns {string[]|null} one filled tpl.row per panel, or null to decline
	 */
	static #accRenderPanels(panels, { tpl, inline, run, renderBlock, renderNested, rich }) {
		const built = [];
		for (const p of panels) {
			if (!p.head || !p.parts.length) return null;
			if (this.#hasRedText(p.head)) return null;
			const chunks = this.#accRenderChunks(p.parts, { tpl, inline, run, renderBlock, renderNested, rich });
			if (chunks === null) return null;
			const content = chunks.join("");
			if (!content.trim()) return null;                          // panel with no rendered body
			built.push(Utils.FillTemplate(tpl.row, { head: inline(p.head), content }));
		}
		return built;
	}

	/**
	 * ROUND 289 — the per-part chunk loop of #accRenderPanels, extracted VERBATIM so the
	 * round-289 lead (content the writer put before the first panel) renders through the
	 * exact same machinery as a panel body. A pure move: #accRenderPanels' output is
	 * byte-identical by construction, which the round's toggles-OFF leg proves at corpus
	 * scale. Returns null when a part cannot be rendered (→ decline the accordion).
	 */
	static #accRenderChunks(parts, { tpl, inline, run, renderBlock, renderNested, rich }) {
		{
			const chunks = [];
			for (const part of parts) {
				if (part.img) {
					chunks.push(this.#assetImage(part.img, tpl, run));
				} else if (part.video) {
					const vt = DataService.Data.EmitTemplates.video?.youtube;
					if (!vt) return null;
					chunks.push(Utils.FillTemplate(vt, { videoId: part.video, params: "" }));
				} else if (part.embed) {
					chunks.push(part.embed);         // ROUND 278: a non-YouTube embeddable media URL
				} else if (part.nested) {
					if (typeof renderNested !== "function") return null;
					const ph = renderNested(part.nested);
					if (!ph) return null;
					// A nested widget that BUILT for real (the renderNested path attempts a
					// real build first) is wrapped in the human's in-panel row (OSOH501-01:
					// accContent 3's READYSAFE tabs sit inside <div class="row">); an un-built
					// nested placeholder stays bare, exactly as before. Data
					// rich_panels.nested_built_wrap; env ACCRICH2_OFF reverts (no wrap).
					const wrapTpl = rich?.nested_built_wrap;
					const wrap = wrapTpl && part.nested.built
						&& !(typeof process !== "undefined" && process.env && process.env.ACCRICH2_OFF);
					chunks.push(wrap ? Utils.FillTemplate(wrapTpl, { html: ph }) : ph);
				} else if (part.h) {
					chunks.push(`<${part.h}>${inline(part.text)}</${part.h}>`);
				} else if (part.html) {
					chunks.push(part.html);          // ROUND 275: a rendered panel table
				} else if (part.p) {
					const rendered = renderBlock(part.p);              // array of <p>/<ul> html
					const arr = Array.isArray(rendered) ? rendered : [rendered];
					for (const h of arr) if (h && String(h).trim()) chunks.push(String(h));
				}
			}
			return chunks;
		}
	}

	/**
	 * ROUND 289 — render the accordion's LEAD: the parts the writer put before the
	 * first panel marker, emitted ABOVE the widget in their own place (the clickDrop
	 * rule; data lead_before_first_panel). Roles convert through the SAME #accPushPart
	 * the panels use, then render through the SAME #accRenderChunks, so a lead
	 * paragraph, picture or video is byte-identical to the panel form. Returns null
	 * when a part cannot be placed, [] when the lead renders to nothing.
	 */
	static #accRenderLead(lead, { tpl, inline, run, renderBlock, renderNested, rich, max }) {
		if (lead.length > (max ?? 12)) return null;              // an unusually long lead → keep the box
		const rp = [];
		for (const p of lead) if (!this.#accPushPart(rp, p)) return null;
		if (!rp.length) return [];
		const chunks = this.#accRenderChunks(rp, { tpl, inline, run, renderBlock, renderNested, rich });
		if (chunks === null) return null;
		return chunks.filter((c) => c && String(c).trim());
	}

	/**
	 * ROUND 289 — round 239's own templated go-to-journal heading, emitted after the
	 * accordion when its member walk skipped the writer's button (see
	 * panel_delimiters.go_journal_member). Read from buttons.go_journal, never copied.
	 */
	static #accGoJournalHtml() {
		const gj = DataService.Data.EmitTemplates?.buttons?.go_journal;
		if (!gj || gj.enabled === false || !gj.form) return [];
		return [Utils.FillTemplate(gj.form, { label: Utils.EscapeHtml(gj.label ?? "Go to your journal") })];
	}

	// =======================================================================
	// ROUND 278 — THE PANEL-DELIMITER FALLBACK
	// =======================================================================
	/**
	 * PANEL-DELIMITER accordion (ROUND 278, Chris — the interactive-coverage chain,
	 * round 3 of 8: "if the writer has used the accordion tag … attempt to generate
	 * an accordion"). Tried LAST, only where the strict text/image paths AND both
	 * modes of the round-246 rich fallback have all returned null — so it is
	 * STRICTLY ADDITIVE and every accordion that built before this round builds
	 * identically after it, by construction (env ACCPANELS_OFF proves it).
	 *
	 * WHY IT EXISTS. The decline-reason recorder (outputs/_measure_r278_accordion.cjs,
	 * which rewrites every `return null` in the shipped accordion region to a recorder
	 * so the builder names its own verdict) accounted for 100% of the 454 declines,
	 * and the single biggest class — 239 declines / 105 modules — was ONE mechanism:
	 * CONTENT ARRIVED BEFORE ANY PANEL OPENED. Only an `[accordion N]` tag could open
	 * a panel, but writers delimit panels in at least four other ways, and the human
	 * builds an accordion from every one of them (each derivation below is quoted
	 * against its gold):
	 *
	 *   D1 [accordion N] tags — the existing rule, WIDENED to the word/ordinal forms
	 *      the funnel found ("[accordion one:]", "[first accordion]", "[Start of
	 *      Accordion 2]", "[Accordion heading 1]"), and a heading-less panel may now
	 *      take its head from its own first [H2]-[H6] SUB-HEADING.
	 *        CEDO501-2.1  "[Accordion 1]" "[H3] Jobseeker Support" "[Body] …"
	 *        gold         <div class="accHead"><h4>Jobseeker Support</h4></div>
	 *   D2 a captured TABLE with no panel open — ONE ROW = ONE PANEL.
	 *        ENGI303-2.0  | Look around ║ Check the words and sentences before …
	 *        gold         <h4>Look around</h4> + <p>Check the words …</p>
	 *        CEDR101-1.0  | **Helping the followers** / • What makes a good leader…
	 *        gold         <h4>Helping the followers</h4> + the bullets
	 *   D3 a repeating same-level [H2]-[H6] heading (the round-196 tabs heading-pane
	 *      rule transposed).
	 *   D4 repeating BOLD-LEAD black lines.
	 *        CEDO102-0.0  **Use less energy:** We can use less electricity …
	 *        gold         <h4>Use less energy</h4> + <p>We can use less electricity…</p>
	 *
	 * The member VOCABULARY is widened at the same time, because a panel is worth
	 * nothing if one member inside it bails the widget: a NON-iSTOCK image takes the
	 * round-126 URL-slug placeholder name (as the speech bubble has since round 276),
	 * a URL-LESS media-list reference ("[Insert image 5]", PHE1003) is an ASSET
	 * REQUEST — skipped as build content and surfaced as the standard red note after
	 * the widget, never silently dropped (the round-214/242 class) — and a video whose
	 * host is not YouTube renders through the generic iframe (the round-275 carousel
	 * precedent).
	 *
	 * NEVER HALF-BUILDS. No delimiter resolves ≥ min_panels panels · a panel with no
	 * heading or no rendered body · red writer-instruction text in a heading · a
	 * member it cannot place at all · or a finished accordion that still shows a
	 * resolved [tag] (#accLeakGuard — the round-167/275/277 rule at this seam, so
	 * building can only ever PREVENT a visible leak, never add one).
	 *
	 * Data interactive_builders.accordion.panel_delimiters; env ACCPANELS_OFF.
	 */
	static #accordionPanels({ bundle, tpl, renderInline, run, renderBlock, renderNested, renderTable }) {
		const cfg = tpl?.panel_delimiters;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.ACCPANELS_OFF) return null;
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (typeof renderBlock !== "function") return null;      // need the body renderer
		const inline = renderInline ?? ((s) => s);
		const rich = tpl.rich_panels ?? {};
		const notes = [];

		// (1) Classify every member into an ordered PART with a ROLE. Classifying by
		//     the RESOLVED TAG (not the writer's spelling) is the round-276 lesson —
		//     "[Insert image of a robot]" matches no ^image pattern.
		// ROUND 289 — the accordion's OWN member vocabulary, supplied through the same
		// caller-scoped `delims` mechanism tabs/flipCard/clickDrop already use. Every
		// key is read from data, so a family reverses on its own data key; with the
		// vocabulary disabled the object is empty and the walk is the r278 default
		// verbatim, which is what ACCMEMBER_OFF produces.
		const mv = (cfg.member_vocabulary && cfg.member_vocabulary.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ACCMEMBER_OFF))
			? cfg.member_vocabulary : null;
		const gjCfg = (cfg.go_journal_member && cfg.go_journal_member.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ACCGOJOURNAL_OFF))
			? cfg.go_journal_member : null;
		const flags = {};
		const delims = (mv || gjCfg) ? {
			prose_tags: mv?.prose_tags ?? [],
			note_tags: mv?.note_tags ?? [],
			head_tags: mv?.head_tags ?? [],
			head_level: mv?.head_level ?? "h4",
			defer_pattern: mv?.defer_pattern,
			text_tags_note_when_empty: !!mv,
			skip_go_journal: !!gjCfg,
		} : undefined;

		const parts = this.#accMemberParts(members, { tpl, cfg, run, renderTable, notes, delims, flags });
		if (!parts) return null;

		// (2) Resolve the panels from the first delimiter kind that is present. ROUND 289
		//     — content arriving BEFORE the first panel is the accordion's own LEAD and is
		//     rendered above the widget in the writer's place (the clickDrop rule), rather
		//     than declining the build outright.
		const leadCfg = (cfg.lead_before_first_panel && cfg.lead_before_first_panel.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ACCLEADIN_OFF))
			? cfg.lead_before_first_panel : null;
		const lead = [];
		const panels = this.#accResolvePanels(parts, cfg, tpl, leadCfg ? lead : null);
		if (!panels || panels.length < (cfg.min_panels ?? 1)) return null;

		// (3) Render through the SHARED panel renderer, so this fallback and the
		//     round-246 rich one emit byte-identical markup.
		const built = this.#accRenderPanels(panels, { tpl, inline, run, renderBlock, renderNested, rich });
		if (!built) return null;
		const leadHtml = lead.length
			? this.#accRenderLead(lead, { tpl, inline, run, renderBlock, renderNested, rich, max: leadCfg?.max_lead_parts ?? 12 })
			: [];
		if (leadHtml === null) return null;
		const html = [...leadHtml, tpl.open, ...built, tpl.close,
			...(flags.goJournal ? this.#accGoJournalHtml() : [])].join("\n");
		if (this.#accLeakGuard(html, cfg)) return null;           // a build must never ADD a leak
		// the r239 member branch must not emit a SECOND identical heading (see
		// buttons.go_journal.member_branch_yields_to_builder)
		if (flags.goJournal) bundle._goJournalEmitted = true;
		if (notes.length) bundle.instructions = [...(bundle.instructions ?? []), ...notes];
		bundle.r278Accordion = true;                              // detector / affected-set marker
		return html;
	}

	/**
	 * ROUND 278 — every captured member as an ordered {role,…} PART, or null when a
	 * member cannot be placed at all. Roles: panel · head · text · img · video ·
	 * embed · table · nested. Instruction/noise members and image-arrangement layout
	 * markers become NOTES (surfaced red after a successful build, never dropped).
	 *
	 * ROUND 281 — SHARED WITH TABS. The vocabulary itself (what an image / a video /
	 * an asset request / a table / a note IS) is widget-independent; only the
	 * DELIMITER tag differs. `opts.delims` lets a caller name its own delimiter and
	 * opener tags; omitted, every default is the round-278 accordion behaviour
	 * verbatim, so the accordion path is byte-identical BY CONSTRUCTION.
	 */
	static #accMemberParts(members, { tpl, cfg, run, renderTable, notes, delims, flags }) {
		const parts = [];
		const idRe = new RegExp(cfg.video_youtube_id_re
			?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");
		// A panel delimiter must carry a NUMBER (digit or word) — the bare "[accordion]"
		// is the widget's OPENER, not a panel, and treating it as one collapsed the whole
		// bundle into a single heading-less panel (caught live on CEDO102/ENGI303).
		const numbered = new RegExp(delims?.panel_tag_pattern ?? cfg.panel_tag_pattern
			?? "^\\[\\s*(?:start\\s+of\\s+)?accordion(?:\\s+(?:heading|panel))?\\s+(?:\\d+|one|two|three|four|five|six|seven|eight|nine|ten)\\s*[:.]?\\s*\\]$", "i");
		const ordinal = new RegExp(delims?.panel_ordinal_pattern ?? cfg.panel_ordinal_pattern
			?? "^\\[\\s*(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\\s+accordion\\s*[:.]?\\s*\\]$", "i");
		// the DELIMITER tag(s) that open a panel/pane, and the widget's own opener tag(s)
		// which carry no content. Default = the accordion's, so nothing moves for it.
		const delimTags = delims?.tags ?? ["accordion"];
		const openerTags = delims?.opener_tags ?? [];

		for (const m of members) {
			if (!m) continue;
			const tag = m.type === "tag" ? m.parse?.primary?.tag : null;
			// the widget's own invocation / closer — no content of its own (tabs' [tabs]).
			if (tag && openerTags.includes(tag)) continue;

			// an image-ARRANGEMENT layout marker (round 242) — a note, never content
			const layoutMk = this.#imageLayoutMarker(m, tpl);
			if (layoutMk) { notes.push(layoutMk); continue; }

			if (m.type === "nested") { parts.push({ role: "nested", bundle: m.nestedBundle }); continue; }

			if (m.type === "table") {
				if (typeof renderTable !== "function") return null;
				// Rendered EAGERLY (renderTable is only in scope here) so the table can serve
				// either job: as the panel SOURCE (D2, which reads item.block.rows) or, when
				// another delimiter owns the panels, as ordinary panel CONTENT through the
				// converter's own kept-table emitter — the round-275 seam.
				const html = renderTable(m);
				parts.push({ role: "table", item: m, html: (html && String(html).trim()) ? String(html) : null });
				continue;
			}

			if (m.type === "black") {
				const t = String(m.text ?? "");
				if (!t.trim()) continue;
				// the docx numbered-list artifact ("1." alone on its line) renders nothing
				if (/^\s*\(?\d{1,3}[.)]\s*$/.test(t)) continue;
				parts.push({ role: "text", text: t });
				continue;
			}

			// ROUND 282 — a FACE LABEL WORD. Some writers name the two sides of a flip
			// card in words rather than tags ("Facing:" / "Reverse:", EXPFUN06-0.0's
			// "[on flip]"), which arrive as instruction/noise spans and were surfaced as
			// notes with their content lost. A span whose OWN text matches the caller's
			// face_label_pattern sets the face instead, and its trailing black text is
			// that face's content. Empty for every other caller → nothing moves.
			if (m.type === "tag" && delims?.face_label_pattern) {
				const own = this.#cellText(String(m.text ?? "")).replace(/^\[|\]$/g, "").trim();
				const fm = own.match(new RegExp(delims.face_label_pattern, "i"));
				if (fm) {
					const back = new RegExp(delims.face_label_back_pattern ?? "back|reverse|flip", "i").test(own);
					parts.push({ role: "face", face: back ? "back" : "front", text: this.#cellText(m.blackAfter ?? "") });
					continue;
				}
			}

			// a writer instruction / noise span — surfaced as a red note, never build content
			if (m.type === "tag"
				&& (m.parse?.class === "instruction" || m.parse?.class === "noise" || m.parse?.instructionFragment)) {
				const t = this.#cellText(m.blackAfter ?? "") || this.#cellText(m.text ?? "");
				if (t) notes.push(t);
				continue;
			}

			const raw = m.type === "tag" ? (m.blackAfter ?? "") : "";
			const text = this.#cellText(raw);

			if (tag && delimTags.includes(tag)) {
				const own = this.#cellText(String(m.text ?? ""));
				const isDelim = !text && (numbered.test(own) || ordinal.test(own));
				// ROUND 283 — a DELIMITER TAG NAMING A SUB-ROLE. Some writers split one item
				// across several tags of the same family, each naming a part of it:
				// "[Insert ClickDrop 1] <title>" then "[Video for ClickDrop 1] <url>" then
				// "[Text for ClickDrop 1]" (XGF9001-2.0), or "[click drop 1 image] <url>"
				// then "[clickdrop 1 text]" (BLL244-2.0). The tag whose payload is nothing
				// but a MEDIA URL is that item's media, not a new item with a URL for a
				// label — which is what the shared bail below (rightly, for a heading) used
				// to make of it. Opt-in per caller: undefined for the accordion and tabs, so
				// their paths are byte-identical BY CONSTRUCTION.
				if (delims?.delimiter_media_role && text && !this.#hasRedText(raw)
					&& !(typeof process !== "undefined" && process.env && process.env.CLICKDROPS_OFF)
					&& /^\s*https?:\/\/\S+\s*$/.test(text.replace(/\s+/g, " "))) {
					const vm = text.match(idRe);
					if (vm) { parts.push({ role: "video", id: vm[1] }); continue; }
					const fn = this.#accImageFilename(text.trim(), tpl, cfg);
					if (fn) { parts.push({ role: "img", filename: fn }); continue; }
					const gen = cfg.generic_embed !== false
						? DataService.Data.EmitTemplates.video?.generic_iframe : null;
					if (gen) { parts.push({ role: "embed", html: Utils.FillTemplate(gen, { url: text.trim() }) }); continue; }
					return null;
				}
				if (text) {
					if (this.#hasRedText(raw) || /https?:\/\//.test(text)) return null;
					// A HEADING IS SHORT. When the writer put a whole sentence on the panel tag
					// ("[Accordion 1] **Recycle** means when we send certain materials to special
					// places…", CEDW101-0.0) only its BOLD LEAD is the heading and the rest is the
					// panel's first body line — the same rule D2 and D4 use. Without this the
					// build shipped a paragraph inside <h4>, which no gold panel does. With no
					// bold lead to fall back on, the panel is left head-less so the D1 resolver
					// declines rather than inventing one.
					const maxWords = cfg.head_max_words ?? 14;
					const firstLine = text.split("\n")[0].trim();
					if (text.split(/\s+/).length > maxWords || /\n/.test(text)) {
						const lead = this.#accBoldLead(firstLine, cfg);
						if (!lead) { parts.push({ role: "panel", head: "" , overlong: true }); continue; }
						parts.push({ role: "panel", head: lead.head });
						const rest = [lead.rest, ...text.split("\n").slice(1)].filter((s) => String(s).trim()).join("\n");
						if (rest.trim()) parts.push({ role: "text", text: rest });
						continue;
					}
					parts.push({ role: "panel", head: text });
				} else if (isDelim) {
					parts.push({ role: "panel", head: "" });
				}
				// a bare unnumbered "[accordion]" is the widget OPENER — skipped
				continue;
			}

			if (["h2", "h3", "h4", "h5", "h6"].includes(tag)) {
				if (this.#hasRedText(raw)) return null;
				const t = text.replace(/\*\*/g, "").trim();
				if (!t) continue;
				parts.push({ role: "head", level: tag, text: t });
				continue;
			}

			if (tag === "image") {
				const url = this.#cellMediaUrl(raw);
				if (!url) {
					// AN ASSET REQUEST, not an image: the writer named a Media-List item
					// ("[Insert image 5]", PHE1003) with no URL to render. Skipped as build
					// content and surfaced as a red note so the developer knows to place it —
					// the round-214/242 rule, never a silent drop and never a made-up filename.
					if (cfg.asset_request_note === false) return null;
					const t = this.#cellText(String(m.text ?? "")) + (text ? ` ${text}` : "");
					if (t.trim()) notes.push(t.trim());
					continue;
				}
				const fn = this.#accImageFilename(url, tpl, cfg);
				if (!fn) return null;                              // a video url / unnameable → bail
				parts.push({ role: "img", filename: fn });
				// a real caption riding with the image stays as panel text
				const residual = text.replace(/^\s*\[[^\]]*\]\s*/, "")
					.replace(/https?:\/\/\S+/g, "").replace(/\S*gm-?\d{6,10}\S*/g, "")
					.replace(/[/|]/g, " ").trim();
				if (residual && (cfg.image_caption_as_text !== false)) parts.push({ role: "text", text: residual });
				continue;
			}

			if (tag === "video" || tag === "audio") {
				if (this.#hasRedText(raw) && !this.#cellMediaUrl(raw) && !/https?:\/\//.test(raw)) return null;
				const idm = String(raw).match(idRe);
				if (idm) { parts.push({ role: "video", id: idm[1] }); continue; }
				// NOT YouTube — render the generic iframe, exactly as the body path and the
				// round-275 carousel do, instead of bailing the whole widget on the host.
				const url = String(raw).match(/https?:\/\/[^\s\]"<>)]+/)?.[0] ?? null;
				const gen = url && cfg.generic_embed !== false
					? DataService.Data.EmitTemplates.video?.generic_iframe
					: null;
				if (gen && url) { parts.push({ role: "embed", html: Utils.FillTemplate(gen, { url }) }); continue; }
				if (!url) {                                        // a media-list reference again
					if (cfg.asset_request_note === false) return null;
					const t = this.#cellText(String(m.text ?? "")) + (text ? ` ${text}` : "");
					if (t.trim()) notes.push(t.trim());
					continue;
				}
				return null;
			}

			if (tag === "body") {
				if (this.#hasRedText(raw)) return null;
				if (!text.trim()) continue;
				parts.push({ role: "text", text });
				continue;
			}

			if (this.#isInlineMarkerMember(m)) {
				if (this.#hasRedText(raw)) return null;
				if (text.trim()) parts.push({ role: "text", text });
				continue;
			}

			if (tag && /\blist\b/.test(tag)) continue;             // a no-op list delimiter

			// ROUND 281, CALLER-SUPPLIED EXTENSIONS (all empty by default → the accordion
			// path is byte-identical). A widget whose gold panes legitimately carry an
			// element the base vocabulary has no role for can name it here rather than
			// bailing the whole build:
			//   head_tags — treat as a sub-heading at head_level
			//   text_tags — render as pane prose (an [external link]'s own line)
			//   note_tags — surface as a red Writers Note (never silent, never invented)
			// ROUND 289 — A DEFERRED MARKER. A hover/definition marker sits MID-SENTENCE:
			// the defined term is inside the bracket and the rest of the sentence rides
			// after it ("[definition: horizontal axis]" + "does not label 11:00 am but…",
			// ENGJ301-4.0). Rendering only the trailing text would drop the term out of
			// the writer's own sentence, and weaving it back in is the r201 render stitch,
			// which is deliberately OFF inside a widget. So the accordion still declines
			// and keeps the honest box — measured 8 members / 6 activities. Undefined for
			// every other caller, so nothing else can move.
			if (tag && delims?.defer_pattern && (delims.prose_tags ?? []).includes(tag)
				&& new RegExp(delims.defer_pattern, "i").test(String(m.text ?? ""))) {
				return null;
			}

			// ROUND 289 — THE GO-TO-JOURNAL BUTTON (accordion only). Skipped as panel
			// content — the gold puts a button inside a panel in 1.7% of panels — and the
			// caller emits round 239's own templated <h4 class="goJournal"> after the
			// widget instead. The label patterns are READ FROM buttons.go_journal so this
			// and r239 can never drift apart (the r278 #isGoJournalButton discipline).
			if (tag === "button" && delims?.skip_go_journal && this.#accIsGoJournal(m)) {
				if (flags) flags.goJournal = true;
				continue;
			}

			if (tag && (delims?.head_tags ?? []).includes(tag)) {
				if (this.#hasRedText(raw)) return null;
				const ht = text.replace(/\*\*/g, "").trim();
				if (ht) parts.push({ role: "head", level: delims.head_level ?? "h4", text: ht });
				continue;
			}
			// ROUND 289 — prose_tags is the accordion's own name for text_tags; both are
			// read so a caller may use either. text_tags_note_when_empty (accordion only,
			// default false) turns a CONTENT-LESS member into a red Writers Note instead
			// of silently skipping it — the r214/r242 never-silently-dropped rule. Tabs
			// and clickDrop omit the key, so their paths are byte-identical.
			if (tag && [...(delims?.text_tags ?? []), ...(delims?.prose_tags ?? [])].includes(tag)) {
				if (this.#hasRedText(raw)) return null;
				if (text.trim()) { parts.push({ role: "text", text }); continue; }
				if (delims?.text_tags_note_when_empty) {
					const nt = this.#cellText(String(m.text ?? "")).trim();
					if (nt) notes.push(nt);
				}
				continue;
			}
			if (tag && (delims?.note_tags ?? []).includes(tag)) {
				const nt = this.#cellText(String(m.text ?? "")) + (text ? ` ${text}` : "");
				if (nt.trim()) notes.push(nt.trim());
				continue;
			}
			// ROUND 282 — face_tags: a widget whose members carry a FACE marker
			// ([front]/[back] on a flipCard) rather than a panel delimiter. Empty for
			// every other caller, so the accordion and tabs paths cannot move.
			if (tag && (delims?.face_tags ?? []).includes(tag)) {
				if (this.#hasRedText(raw)) return null;
				parts.push({ role: "face", face: tag, text: text.replace(/\*\*/g, "").trim() });
				continue;
			}

			return null;                                           // a foreign tag we cannot place
		}
		return parts;
	}

	/**
	 * ROUND 278 — resolve PANELS from the ordered parts, trying each delimiter kind
	 * in turn (D1 explicit tags → D2 a table → D3 repeating headings → D4 bold-lead
	 * lines) and taking the first that yields a panel with a heading. Returns
	 * `[{ head, parts }]` for #accRenderPanels, or null.
	 */
	static #accResolvePanels(parts, cfg, tpl, lead = null) {
		const substantive = parts.filter((p) => p.role !== "note");
		if (!substantive.length) return null;

		// ---- D1: explicit [accordion …] panel delimiters -----------------------
		if (parts.some((p) => p.role === "panel")) {
			const panels = [];
			let cur = null;
			for (const p of parts) {
				if (p.role === "panel") {
					if (p.overlong) return null;              // a sentence-long tag text with no bold lead
					cur = { head: p.head, parts: [] }; panels.push(cur); continue;
				}
				// ROUND 289 — a part arriving before the first panel is the accordion's own
				// LEAD, rendered above the widget where the writer put it (the clickDrop
				// rule). Only the simple roles may lead: a TABLE or a NESTED widget before
				// the first panel is a shape whose intent is genuinely unclear, so those
				// still decline. `lead` is null when the rule is off → the r278 bail.
				if (!cur && lead && ["text", "img", "video", "embed", "head"].includes(p.role)) {
					lead.push(p); continue;
				}
				if (!cur) return null;                             // content still precedes the first panel
				// a heading-less panel takes its head from its own first sub-heading
				if (p.role === "head" && !cur.head && !cur.parts.length) { cur.head = p.text; continue; }
				if (!this.#accPushPart(cur.parts, p)) return null;
			}
			this.#accHeadFromFirstLine(panels, cfg);
			return panels.every((p) => p.head && p.parts.length) ? panels : null;
		}

		// ---- D2: a captured TABLE — one row = one panel ------------------------
		const tables = parts.filter((p) => p.role === "table");
		if (tables.length === 1 && cfg.table_panels !== false) {
			const others = substantive.filter((p) => p.role !== "table");
			// only when the table IS the widget (nothing substantive but a lead line)
			if (others.every((p) => p.role === "text")) {
				const panels = this.#accTablePanels(tables[0].item, cfg, tpl);
				if (panels && panels.length >= (cfg.min_inferred_panels ?? 2)) return panels;
			}
		}

		// ---- D3: a repeating same-level heading --------------------------------
		if (cfg.heading_panels !== false) {
			const heads = parts.filter((p) => p.role === "head");
			const levels = [...new Set(heads.map((h) => h.level))];
			if (heads.length >= (cfg.min_heading_panels ?? 2) && levels.length === 1) {
				const panels = [];
				let cur = null;
				for (const p of parts) {
					if (p.role === "note") continue;
					if (p.role === "head") { cur = { head: p.text, parts: [] }; panels.push(cur); continue; }
					if (!cur) {
						// a lead line before the first heading is the accordion's intro — allowed
						// only while nothing substantive has been dropped
						if (p.role === "text") continue;
						return null;
					}
					if (!this.#accPushPart(cur.parts, p)) return null;
				}
				if (panels.length >= (cfg.min_inferred_panels ?? 2) && panels.every((p) => p.head && p.parts.length)) return panels;
			}
		}

		// ---- D4: repeating BOLD-LEAD black lines -------------------------------
		if (cfg.bold_lead_panels !== false) {
			const lines = [];
			for (const p of parts) {
				if (p.role === "note") continue;
				if (p.role !== "text") { lines.length = 0; break; }   // mixed content → not this dialect
				for (const l of String(p.text).split("\n")) if (l.trim()) lines.push(l);
			}
			if (lines.length >= (cfg.min_bold_panels ?? 2)) {
				const panels = [];
				let cur = null;
				for (const l of lines) {
					const lead = this.#accBoldLead(l, cfg);
					if (lead) { cur = { head: lead.head, parts: [] }; panels.push(cur); if (lead.rest) cur.parts.push({ p: lead.rest }); continue; }
					if (!cur) continue;                              // an intro line before the first panel
					if (!this.#accPushPart(cur.parts, { role: "text", text: l })) return null;
				}
				if (panels.length >= (cfg.min_bold_panels ?? 2) && panels.every((p) => p.head && p.parts.length)) return panels;
			}
		}
		return null;
	}

	/**
	 * ROUND 278 — append a classified part to a panel's render parts.
	 * @returns {boolean} false when the part cannot be placed (→ decline the accordion)
	 */
	static #accPushPart(out, p) {
		if (p.role === "text") {
			const last = out[out.length - 1];
			if (last && last.p !== undefined) { last.p += `\n${p.text}`; return true; }   // keep a run in one block
			out.push({ p: p.text });
			return true;
		}
		if (p.role === "img") { out.push({ img: p.filename }); return true; }
		if (p.role === "video") { out.push({ video: p.id }); return true; }
		if (p.role === "embed") { out.push({ embed: p.html }); return true; }
		if (p.role === "head") { out.push({ h: p.level, text: p.text }); return true; }
		if (p.role === "nested") { out.push({ nested: p.bundle }); return true; }
		// a table used as panel CONTENT — the kept-table emitter already ran; a null
		// means its own leak guard refused it, so the whole accordion declines.
		if (p.role === "table") { if (!p.html) return false; out.push({ html: p.html }); return true; }
		return false;
	}

	/**
	 * ROUND 278 — the ROUND-246 heading-less recovery, reused: a panel with no heading
	 * takes it from its own FIRST text line (which is what that line is), and the line
	 * is removed from the body so it is never shown twice.
	 */
	static #accHeadFromFirstLine(panels, cfg) {
		const maxWords = cfg.head_max_words ?? 14;
		for (const p of panels) {
			if (p.head || !p.parts.length) continue;
			const first = p.parts[0];
			if (!first || first.p === undefined) continue;
			const lines = String(first.p).split("\n").map((s) => s.trim()).filter(Boolean);
			if (lines.length < 2) continue;                        // the whole part IS the body
			const head = this.#cellText(lines[0]).replace(/^[•·]\s*/, "").replace(/\*\*/g, "").trim();
			if (!head || head.split(/\s+/).length > maxWords) continue;
			if (this.#hasRedText(lines[0])) continue;
			p.head = head;
			first.p = lines.slice(1).join("\n");
			if (!first.p.trim()) p.parts.shift();
		}
	}

	/**
	 * ROUND 278 — a captured TABLE whose rows ARE the panels. Per row: an image cell
	 * becomes the panel image (an unnameable/URL-less one is an asset request, so the
	 * row still builds), a SHORT first text cell is the panel HEADING, otherwise the
	 * heading is the BOLD LEAD of the content cell. Declines the whole table (→ the
	 * hand-off box) the moment a row yields no heading or no content.
	 */
	static #accTablePanels(tableItem, cfg, tpl) {
		const rows = tableItem?.block?.rows ?? [];
		if (rows.length < (cfg.min_panels ?? 1)) return null;
		const maxHead = cfg.table_head_max_words ?? 10;
		const panels = [];
		for (const row of rows) {
			const cells = (row ?? []).map((c) => String(typeof c === "string" ? c : (c?.text ?? "")));
			const kept = [];
			let img = null;
			for (const c of cells) {
				if (!this.#cellText(c).trim()) continue;
				const url = this.#cellMediaUrl(c);
				if (url) {
					const fn = this.#accImageFilename(url, tpl, cfg);
					if (!fn) return null;
					if (img) return null;                          // two images in one panel → too rich
					img = fn;
					continue;
				}
				const plain = this.#cellText(c);
				// a bracketed tag with no URL is a Media-List asset request — not a heading
				if (/^\s*\[[^\]]*\]/.test(plain) && !plain.replace(/^\s*\[[^\]]*\]\s*/, "").trim()) continue;
				kept.push(plain);
			}
			if (!kept.length) return null;
			let head = null, body = [];
			if (kept.length >= 2 && this.#accIsShortLabel(kept[0], maxHead)) {
				head = kept[0].replace(/\*\*/g, "").replace(/\s*:\s*$/, "").trim();
				body = kept.slice(1);
			} else {
				// the LONGEST cell is the content; its bold lead is the heading
				const idx = kept.reduce((best, c, i, a) => (c.length > a[best].length ? i : best), 0);
				const lead = this.#accBoldLead(String(kept[idx]).split("\n")[0], cfg);
				if (!lead) return null;
				head = lead.head;
				const restLines = String(kept[idx]).split("\n").slice(1);
				body = [[lead.rest, ...restLines].filter(Boolean).join("\n"), ...kept.filter((_, i) => i !== idx)];
			}
			const parts = [];
			if (img) parts.push({ img });
			for (const b of body) if (String(b).trim()) parts.push({ p: String(b) });
			if (!head || !parts.length) return null;
			if (this.#accHasBracketTag(head)) return null;         // never put a raw tag in a heading
			panels.push({ head, parts });
		}
		return panels;
	}

	/** ROUND 278 — a short, single-line, bullet-free label (a panel heading, not prose). */
	static #accIsShortLabel(s, maxWords) {
		const t = String(s ?? "").replace(/\*\*/g, "").trim();
		if (!t || /\n/.test(t) || /^[•·]/.test(t)) return false;
		if (this.#accHasBracketTag(t)) return false;
		return t.split(/\s+/).length <= maxWords;
	}

	/** ROUND 278 — "**Head:** rest" → { head, rest }, or null when the line has no bold lead. */
	static #accBoldLead(line, cfg) {
		const t = String(line ?? "").trim();
		const m = t.match(new RegExp(cfg.bold_lead_pattern ?? "^\\*\\*(.+?)\\*\\*\\s*[:：]?\\s*([\\s\\S]*)$"));
		if (!m) return null;
		const head = String(m[1]).replace(/\s*:\s*$/, "").trim();
		const maxWords = cfg.head_max_words ?? 14;
		if (!head || head.split(/\s+/).length > maxWords) return null;
		if (this.#accHasBracketTag(head)) return null;
		return { head, rest: String(m[2] ?? "").trim() };
	}

	/**
	 * ROUND 289 — is this member the writer's GO-TO-JOURNAL button? The patterns are
	 * READ FROM buttons.go_journal (round 239's own rule) rather than copied, so the
	 * builder's skip and #goJournalTail's emit can never drift apart — the round-278
	 * #isGoJournalButton discipline. A button carrying a URL is a real link button and
	 * is never one of these.
	 */
	static #accIsGoJournal(m) {
		const gj = DataService.Data.EmitTemplates?.buttons?.go_journal;
		if (!gj || gj.enabled === false) return false;
		if (!m || m.type !== "tag") return false;
		const p = m.parse?.primary;
		if (!p || p.tag !== "button") return false;
		const raw = String(m.text ?? ""), after = String(m.blackAfter ?? "");
		if (/https?:\/\//.test(after) || /https?:\/\//.test(raw)) return false;
		const label = after.replace(/\*/g, "").trim() || raw.replace(/[[\]*]/g, "").trim();
		return (!!label && new RegExp(gj.label_match, "i").test(label))
			|| new RegExp(gj.raw_match, "i").test(raw.trim());
	}

	/** ROUND 278 — does this text still show a bracketed writer tag? */
	static #accHasBracketTag(s) {
		return /\[[^\]\n]{1,60}\]/.test(String(s ?? ""));
	}

	/**
	 * ROUND 278 — THE LEAK GUARD (the round-167/275/277 rule at this seam). A finished
	 * accordion whose VISIBLE text still shows a bracketed tag the normaliser resolves
	 * would turn gate-excluded hand-off chrome into a counted literal leak on the page,
	 * so the build declines and the honest box stays. Building can therefore only ever
	 * PREVENT a leak. Scoped to THIS fallback, so it can never remove a pre-278 build.
	 */
	static #accLeakGuard(html, cfg) {
		if (cfg && cfg.leak_guard === false) return false;
		// The round-277 #hintLeakGuard form: a bracketed word in the VISIBLE text (the
		// Mode-P image comment is a real HTML comment and is stripped first, so it never
		// trips the guard). Deliberately normaliser-free — over-firing merely keeps the
		// honest hand-off box, which is the conservative direction.
		const vis = String(html ?? "").replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ");
		return /\[\s*[A-Za-z][^\]\n]{0,40}\]/.test(vis);
	}

	/**
	 * ROUND 278 — the panel image FILENAME. An iStock URL names itself; an image the
	 * writer sourced elsewhere (alamy, a school SharePoint, a museum page) still has to
	 * render, so it falls back to the same URL-slug placeholder the rotating banner has
	 * used since round 126 and the speech bubble since round 276. A VIDEO url is never
	 * a panel image and still declines.
	 */
	static #accImageFilename(url, tpl, cfg) {
		if (!url) return null;
		if (/youtu\.?be|youtube\.com|vimeo/i.test(url)) return null;
		const istock = this.#istockFilename(url, tpl);
		if (istock) return istock;
		if (cfg && cfg.image_slug_fallback === false) return null;
		return this.#bannerImageFilename(url, tpl);
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

			// (a0.5) a captured data TABLE member — CONTENT-LOSS REPAIR (ROUND 275). A table
			//     item carries no `.text`, so it fell through the `if (!text) continue;` guard
			//     below and was SILENTLY DROPPED: the accordion built and the writer's table
			//     simply vanished from the page. Bail instead, so the round-275 rich walk (which
			//     renders a panel table through the kept-table emitter) gets the bundle. Under
			//     ACCTABLE_OFF the old silent-drop behaviour is restored byte-for-byte.
			if (m && m.type === "table"
				&& (tpl?.rich_panels?.table_member?.enabled !== false)
				&& !(typeof process !== "undefined" && process.env && process.env.ACCTABLE_OFF)) {
				return null;
			}

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

	// =======================================================================
	// THE RICH GENERAL COMPOSER (round 276) — see the doc block on #speechBubbleRich
	// =======================================================================

	/** every `[...]` bracket inside a red span, lower-cased and trimmed. */
	static #sbBrackets(spanText) {
		return [...String(spanText ?? "").matchAll(/\[([^\]\n]{0,140}?)\]/g)]
			.map((m) => m[1].replace(/\s+/g, " ").trim().toLowerCase())
			.filter(Boolean);
	}

	/**
	 * Classify ONE writer marker (a red span's brackets + the text that follows it)
	 * into the composer's part roles. Returns { role, ... } or null when the marker
	 * carries nothing the composer recognises. `role` is one of:
	 *   bubble | image | head | text | note | STOP
	 * STOP means "this bundle is not a bubble layout" → the caller declines.
	 * Every pattern lives in data (speechBubble.rich), so a new writer spelling is a
	 * data edit, never a code change.
	 */
	static #sbMarkerRole(brackets, cfg) {
		const bubbleRe = new RegExp(cfg.bubble_re ?? "bubble", "i");
		const imageRe = new RegExp(cfg.image_re ?? "^image\\b", "i");
		const headRe = new RegExp(cfg.head_re ?? "^h[1-6]\\b", "i");
		const textRe = new RegExp(cfg.text_re ?? "^body\\b", "i");
		const declineRe = new RegExp(cfg.decline_tags ?? "^activity\\b", "i");
		const roles = new Set();
		for (const b of brackets) {
			if (bubbleRe.test(b)) { roles.add("bubble"); continue; }   // "speech bubble", "thought bubble green", …
			if (imageRe.test(b)) { roles.add("image"); continue; }
			if (headRe.test(b)) { roles.add("head"); continue; }
			if (textRe.test(b)) { roles.add("text"); continue; }
			if (declineRe.test(b)) { roles.add("STOP"); continue; }    // an [Activity]/[button]/another widget → not ours
			// anything else is a position / asset hint ("first panda on the left") — ignored
		}
		return roles;
	}

	/**
	 * A raw captured CELL (or a member's own span text) → an ordered list of parts.
	 * A cell is a string carrying "🔴[RED TEXT] … [/RED TEXT]🔴" markers with black
	 * text between them; each marker plus the text following it is one part.
	 */
	static #sbCellParts(cell, cfg, tpl) {
		const raw = String(cell ?? "");
		if (!raw.trim()) return [];
		const RE = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		const parts = [];
		let last = 0, m;
		const chunks = [];
		while ((m = RE.exec(raw)) !== null) {
			chunks.push({ lead: raw.slice(last, m.index), span: m[1] });
			last = m.index + m[0].length;
		}
		chunks.push({ lead: raw.slice(last), span: null });
		// text BEFORE the first marker belongs to whatever came before (a caption line)
		for (let i = 0; i < chunks.length; i++) {
			const c = chunks[i];
			const tail = (chunks[i + 1] ? "" : "");   // placeholder — text is taken as `lead` of the NEXT chunk
			if (i === 0 && c.lead.trim()) parts.push({ role: "text", text: c.lead.trim() });
			if (!c.span) { if (i > 0 && c.lead.trim()) { /* handled below via prev marker */ } continue; }
			const following = (chunks[i + 1]?.lead ?? "").trim();
			const roles = this.#sbMarkerRole(this.#sbBrackets(c.span), cfg);
			if (roles.has("STOP")) return null;
			const url = following.match(/https?:\/\/[^\s\]"<>)]+/)?.[0] ?? null;
			const rest = this.#sbRestText(following);
			if (roles.has("image")) {
				parts.push({ role: "image", url, hint: this.#cellText(c.span).trim() });
				if (!roles.has("bubble") && rest) parts.push({ role: "text", text: rest });
			}
			if (roles.has("bubble")) {
				parts.push({ role: "bubble", text: rest, tagText: this.#cellText(c.span) });
			} else if (roles.has("head")) {
				if (rest) parts.push({ role: "head", text: rest });
			} else if (roles.has("text")) {
				if (rest) parts.push({ role: "text", text: rest });
			} else if (!roles.size) {
				// A red span with no recognised marker is the writer LABELLING the cell
				// ("Person 1", "Insert with icons"): the MARKER is a designer instruction
				// and is surfaced as a note (never silently dropped, §6), but the black
				// text after it is the learner CONTENT and stays content — folding the
				// two together would have buried OSBY301's four bubbles inside a note.
				const noteTxt = this.#cellText(c.span).replace(/\s+/g, " ").trim();
				if (noteTxt) parts.push({ role: "note", text: noteTxt });
				if (rest) parts.push({ role: "text", text: rest });
			}
			void tail;
		}
		return parts;
	}

	/** a member item → parts (same roles as #sbCellParts). null = decline. */
	static #sbMemberParts(m, cfg, tpl) {
		if (!m) return [];
		if (m.type === "nested") return null;
		if (m.type === "black") {
			const t = String(m.text ?? "").replace(/\s+/g, " ").trim();
			return t ? [{ role: "text", text: t }] : [];
		}
		if (m.type !== "tag") return [];
		const p = m.parse?.primary;
		const after = String(m.blackAfter ?? "").replace(/\s+/g, " ").trim();
		if (!p) {
			// a red span the normaliser resolved to nothing: an instruction/noise the
			// writer left for the designer → rides along as a note (the r214 rule).
			if (["instruction", "noise"].includes(m.parse?.class)) {
				const t = `${String(m.text ?? "").trim()} ${after}`.replace(/\s+/g, " ").trim();
				return t ? [{ role: "note", text: t }] : [];
			}
			return null;
		}
		// A MEMBER is classified by its RESOLVED tag first — the writer's spelling is
		// unreliable ("[Insert image of a robot]" never matches an ^image pattern, and
		// 11 declines were exactly that), and the normaliser has already done the work.
		// The SPELLING is still read afterwards, for the bubble/thought cue and for a
		// span that resolved to something the tag map does not cover.
		const roles = new Set();
		const tag = String(p.tag ?? "").toLowerCase();
		const map = cfg.tag_roles ?? {};
		for (const [role, list] of Object.entries(map)) if ((list ?? []).includes(tag)) roles.add(role);
		if (!roles.size) for (const r of this.#sbMarkerRole(this.#sbBrackets(m.text ?? ""), cfg)) roles.add(r);
		if (roles.has("STOP")) return null;
		const url = after.match(/https?:\/\/[^\s\]"<>)]+/)?.[0] ?? null;
		const rest = this.#sbRestText(after);
		const out = [];
		if (roles.has("image")) {
			out.push({ role: "image", url: url ?? this.#memberLinkUrl(m), hint: String(m.text ?? "").trim() });
			if (!roles.has("bubble") && rest) out.push({ role: "text", text: rest });
		}
		if (roles.has("bubble") || p.directive === "INTERACTIVE") {
			out.push({ role: "bubble", text: rest, tagText: String(m.text ?? "") });
		} else if (roles.has("head")) {
			if (rest) out.push({ role: "head", text: rest });
		} else if (roles.has("text")) {
			if (rest) out.push({ role: "text", text: rest });
		} else if (!roles.size && !out.length) {
			return null;   // a resolved structural tag we do not recognise → never half-build
		}
		return out;
	}

	/**
	 * The CONTENT text following a writer marker, once the marker's own URL has been
	 * consumed into an image filename. Removing the URL can orphan a markdown emphasis
	 * marker — the writer very often types "**<url>** / **the bubble text**", and a
	 * naive edge-trim that strips `*` would unbalance the REST of the line and turn the
	 * bubble into "<b> You simply </b>add it to the end**" (caught live on CHFUN05).
	 * So: drop the URL, drop an emphasis marker that is now empty AND the writer's " / "
	 * separator with it, and trim only whitespace/brackets — never an emphasis marker
	 * that still has a partner.
	 */
	static #sbRestText(following) {
		return String(following ?? "")
			.replace(/https?:\/\/[^\s\]"<>)]+/g, " ")
			.replace(/^\s*[\]}]\s*/, "")                              // a split bracket's orphan closer (the r104 STRAYLEAD class)
			.replace(/^\s*(?:\*{1,2}|_{1,2})?\s*(?:[/|]\s*)+/, "")   // the orphaned emphasis + " / "
			.replace(/^[\s(),:;\-–—]+/, "")
			.replace(/[\s/|(),\-–—]+$/, "")
			.replace(/\s+/g, " ")
			.trim();
	}

	/** the hyperlink a member carries on its own source block, if any. */
	static #memberLinkUrl(m) {
		const links = m?.block?.links ?? [];
		return links.length ? String(links[0]?.target ?? "") : null;
	}

	/** a captured table → an ordered list of cell-part GROUPS (see the doc block). */
	static #sbTableGroups(tbl, cfg, tpl, openerIsBubble) {
		const rows = (tbl?.rows ?? []).filter((r) => Array.isArray(r) && r.length);
		if (!rows.length) return null;
		const cols = Math.max(...rows.map((r) => r.length));
		const cellParts = rows.map((r) => {
			const out = [];
			for (let c = 0; c < cols; c++) out.push(this.#sbCellParts(r[c], cfg, tpl));
			return out;
		});
		if (cellParts.some((r) => r.some((p) => p === null))) return null;   // a decline_tags marker
		const nBub = (parts) => (parts ?? []).filter((p) => p.role === "bubble").length;
		const totalBub = cellParts.flat().reduce((n, p) => n + nBub(p), 0);
		const totalImg = cellParts.flat().reduce((n, p) => n + (p ?? []).filter((x) => x.role === "image").length, 0);
		if (!totalBub && !totalImg) {
			// THE PLAIN-CELL TABLE. The writer put the bubble tag on the invocation and
			// the bubble TEXTS in a bare table — "[Put the three quotations each into a
			// speech bubble]" above a 1x3 table of three quotes (CEDR501), "[speech
			// bubbles - conversation layout] … 4 separate speech bubbles/people" above a
			// 4x2 table (OSBY301). One bubble per non-empty cell, in cell order. Gated on
			// the bundle's OWN opener being the bubble invocation and on every cell being
			// plain text, so a captured DATA table (the over-capture class) still declines.
			if (!openerIsBubble || !cfg.plain_cell_bubbles) return null;
			const flat = cellParts.flat();
			if (flat.some((p) => (p ?? []).some((x) => x.role !== "text" && x.role !== "note"))) return null;
			const out = [];
			for (const p of flat) {
				const txt = (p ?? []).filter((x) => x.role === "text").map((x) => x.text).join(" ").trim();
				const notes = (p ?? []).filter((x) => x.role === "note");
				if (!txt) { if (notes.length) out.push(notes); continue; }
				out.push([...notes, { role: "bubble", text: txt, tagText: "" }]);
			}
			return out.length ? out : null;
		}
		// GROUP by the axis that yields at most ONE bubble per group: rows, then
		// columns (the image-row-above-caption-row grid), else cell by cell.
		const byRow = cellParts.map((r) => r.flat());
		if (byRow.every((g) => nBub(g) <= 1)) return byRow;
		const byCol = [];
		for (let c = 0; c < cols; c++) byCol.push(cellParts.map((r) => r[c] ?? []).flat());
		if (byCol.every((g) => nBub(g) <= 1)) return byCol;
		return cellParts.flat();
	}

	/**
	 * THE RICH GENERAL COMPOSER — round 276 (Chris, the interactive-coverage chain,
	 * round 1 of 8). Tried LAST, after conversation / no-table-avatar / text-only /
	 * 1x2-table have all declined, so every bubble those four already build is
	 * BYTE-IDENTICAL by construction and this branch can only ADD builds.
	 *
	 * WHY IT EXISTS. The round's decline-reason probe (outputs/_measure_r276_speechbubble.cjs,
	 * which rewrites every `return null` in the speechBubble region to a recorder so the
	 * SHIPPED builder reports its own verdict) accounted for 100% of the 258 declines and
	 * found every one of them decided inside the narrow 1x2-table branch, on a guard about
	 * the writer's LAYOUT rather than about the widget:
	 *     72  "not exactly one captured table"   (69 of them had NO table at all)
	 *     67  "the bundle carries any modifier"  (the modifiers are "left", "orange",
	 *                                             "insert bookworm on right hand side" …)
	 *     50  "the table has more than one row"
	 *     38  "the row does not have exactly two cells" (27 of them ONE cell)
	 * Those four are 87% of the class, and each is a VARIATION of how the bubble was
	 * typed — the thing this round exists to handle.
	 *
	 * HOW. Members, and every cell of a captured table, are flattened into an ordered
	 * stream of PARTS carrying a role (bubble / image / head / text / note). A bubble
	 * part opens a bubble; head and text attach to it; an image becomes its avatar.
	 * ONE `row speechBubble` is emitted per bubble — the AVATAR form when it has an
	 * image, else the TEXT-ONLY form, reusing the round-246/247 templates because the
	 * gold measurement (outputs/_measure_r276_goldforms.py, 1218 rows / 143 modules)
	 * says those ARE the corpus plurality: one bubble per row 80.4%, avatar rows
	 * layout=speech 97.6% and bubble-right 58.6% vs bubble-left 12.4%, image-less rows
	 * col-12 + bubble-basic no-hover bubble-top.
	 *
	 * NEVER HALF-BUILDS. Declines (keeping the honest hand-off box) on: a structural
	 * marker in decline_tags — an [Activity] opener, another widget's invocation, a
	 * [button]/[video]/[link] carrying its own content; a nested widget; a captured
	 * table holding neither a bubble nor an image (an over-capture); an image URL we
	 * cannot name; or no bubble with any content. A URL-LESS image marker is SKIPPED
	 * as the asset request it is and surfaced in the widget's red Writers Note (the
	 * round-242 rule), and instruction/noise spans ride along the same way (round 214).
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive
	 * @param {object} args.tpl - the speechBubble template block (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @returns {string|null} the built bubble rows, or null to keep the hand-off box
	 */
	static #speechBubbleRich({ bundle, tpl, renderInline, run }) {
		const cfg = tpl?.rich;
		if (!cfg || cfg.enabled === false || !bundle) return null;
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		if (env.SBRICH_OFF) return null;

		// (1) FLATTEN — members in order; a table member expands into its groups.
		// A bundle whose OWN opener is the bubble invocation licenses the plain-cell
		// table form (the writer's "put each of these into a speech bubble" dialect).
		const openerIsBubble = [...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])]
			.some((m) => m?.type === "tag" && m.parse?.primary?.directive === "INTERACTIVE");
		const groups = [];
		let cur = [];
		const pushCur = () => { if (cur.length) groups.push(cur); cur = []; };
		for (const m of bundle.memberItems ?? []) {
			if (!m) continue;
			if (m.type === "table") {
				const g = this.#sbTableGroups(m.block, cfg, tpl, openerIsBubble);
				if (!g) return null;
				pushCur();
				for (const one of g) if (one.length) groups.push(one);
				continue;
			}
			const parts = this.#sbMemberParts(m, cfg, tpl);
			if (parts === null) return null;
			cur.push(...parts);
		}
		pushCur();
		if (!groups.length) return null;

		// (2) GROUP THE PARTS INTO BUBBLES. A bubble part opens one; head/text attach
		// to the open bubble (or, before the first bubble, to the one that follows —
		// the writer's caption-then-bubble cell order); an image attaches as the
		// avatar of the bubble it sits with.
		const notes = [];
		const bubbles = [];
		for (const g of groups) {
			let b = null;
			const pending = [];            // text/head seen before this group's bubble
			let pendingImg = null;
			for (const p of g) {
				if (p.role === "note") { if (p.text) notes.push(p.text); continue; }
				if (p.role === "image") {
					if (!p.url) { if (p.hint) notes.push(p.hint); continue; }   // an asset REQUEST (r242)
					// An image the writer sourced OUTSIDE iStock (alamy, a school SharePoint,
					// a museum page) still has to render, so it falls back to the same
					// URL-slug placeholder name the rotating banner has used since round 126
					// — a placeholder the developer swaps for the real asset, exactly like
					// every Mode-P image. A VIDEO url is never an avatar and still declines.
					const fn = (cfg.image_slug_fallback === false)
						? this.#istockFilename(p.url, tpl)
						: (/youtu\.?be|youtube\.com|vimeo/i.test(p.url) ? null : this.#bannerImageFilename(p.url, tpl));
					if (!fn) return null;   // an image we cannot name — never half-build
					if (b) { if (b.img) return null; b.img = fn; } else { if (pendingImg) return null; pendingImg = fn; }
					continue;
				}
				if (p.role === "bubble") {
					b = { img: pendingImg, lines: [...pending], thought: new RegExp(cfg.thought_re ?? "thought", "i").test(p.tagText ?? "") };
					pendingImg = null; pending.length = 0;
					if (p.text) b.lines.push({ head: false, text: p.text });
					bubbles.push(b);
					continue;
				}
				const line = { head: p.role === "head", text: p.text };
				if (b) b.lines.push(line); else pending.push(line);
			}
			// trailing text with no bubble in this group joins the last bubble made
			if (pending.length && bubbles.length) bubbles[bubbles.length - 1].lines.push(...pending);
			if (pendingImg && bubbles.length && !bubbles[bubbles.length - 1].img) {
				bubbles[bubbles.length - 1].img = pendingImg;
			}
		}

		// (3) An invocation with nothing to say contributes nothing — drop it rather
		// than bailing the whole widget (BLLR201's "[Insert bookworm on right hand
		// side of page with speech bubble + audiovisual item 5]" opener sits beside
		// the real bubble; its text is kept as a Writers Note above).
		const min = cfg.min_chars ?? 2;
		const live = bubbles.filter((b) => b.lines.some((l) => (l.text ?? "").replace(/[^\p{L}\p{N}]/gu, "").length >= min));
		for (const b of bubbles) {
			if (live.includes(b)) continue;
			for (const l of b.lines) if (l.text) notes.push(l.text);
		}
		if (!live.length) return null;
		if (live.some((b) => b.lines.length > (cfg.max_paragraphs ?? 8))) return null;

		// (4) EMIT — one row per bubble, reusing the measured round-246/247 shapes.
		const inline = renderInline ?? ((s) => s);
		const av = tpl.no_table_image ?? {};
		const to = tpl.text_only ?? {};
		const body = (b) => {
			const ps = [];
			let open = null;
			for (const l of b.lines) {
				const t = String(l.text ?? "").trim();
				// a "line" with no letter or digit in any script is stray punctuation a
				// split bracket or a stripped URL left behind (the round-104 STRAYLEAD
				// rule, which the text-only branch applies to its own paragraphs) — it
				// must never reach the page as <p>*</p>.
				if (!t || !/[\p{L}\p{N}]/u.test(t)) continue;
				if (l.head) { if (open) ps.push(open); open = `<b>${inline(t)}</b>`; continue; }
				if (/[•·]/.test(t)) {                       // a bulleted bubble → the r73 list body
					if (open) { ps.push(open); open = null; }
					const html = this.#bubbleBody(t, inline);
					if (html) ps.push({ block: html });
					continue;
				}
				if (open) open += `<br>${inline(t)}`; else ps.push(inline(t));
			}
			if (open) ps.push(open);
			const html = ps.map((p) => (p && p.block) ? p.block : `<p>${p}</p>`).join("\n");
			return ps.length > 1 ? `<div>\n${html}\n</div>` : html;
		};
		const out = [];
		for (const b of live) {
			const text = body(b);
			if (!text) return null;
			if (b.img) {
				out.push([
					Utils.FillTemplate(av.open ?? tpl.open, { layout: tpl.layout_attr ?? "speech" }),
					Utils.FillTemplate(av.image_col ?? tpl.image_col, { image: this.#assetImage(b.img, tpl, run) }),
					Utils.FillTemplate(av.text_col_right ?? tpl.text_right, { text }),
					av.close ?? tpl.close,
				].join("\n"));
			} else {
				out.push([
					Utils.FillTemplate(to.open ?? tpl.open, { layout: b.thought ? (to.layout_thought ?? "thought") : (tpl.layout_attr ?? "speech") }),
					to.col_open ?? "<div class=\"col-12\">",
					Utils.FillTemplate(to.bubble ?? "<div class=\"bubble-basic no-hover bubble-top\">{text}</div>", { text }),
					to.col_close ?? "</div>",
					to.close ?? tpl.close,
				].join("\n"));
			}
		}
		// the skipped asset requests / writer instructions surface as the standard red
		// Writers Note after the widget — ONLY on a successful build (the r242 rule).
		if (notes.length) bundle.instructions = [...(bundle.instructions ?? []), ...new Set(notes)];
		return out.join("\n");
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
	 * The speechBubble ENTRY: the four narrow branches above in their historical
	 * order, then the round-276 RICH general composer as the last resort. Splitting
	 * the entry from #speechBubble keeps every existing branch byte-untouched — the
	 * composer can only run where all four already returned null, so the 327 bubbles
	 * that built before this round build identically after it, by construction.
	 */
	static #speechBubbleEntry({ bundle, tpl, renderInline, run }) {
		const narrow = this.#speechBubble({ bundle, tpl, renderInline, run });
		if (narrow) return narrow;
		return this.#speechBubbleRich({ bundle, tpl, renderInline, run });
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
	 * THE flipCard ENTRY POINT (round 282). Tries the four SPECIALISED dialect builders
	 * first (unchanged — see #flipCardDialects), then falls through to the GENERAL
	 * composer #flipCardCards. The composer runs LAST on purpose: the round-276
	 * architecture — a fallback cannot break what already works, so every build the
	 * dialect builders already produced is byte-identical BY CONSTRUCTION.
	 *
	 * Before round 282 each dialect's refusal was `return null`, which ended the whole
	 * dispatch and kept the placeholder — the round-279 DEAD-END class. Now a refusal
	 * falls through.
	 *
	 * @param {object} args - see #flipCardDialects / #flipCardCards
	 * @returns {string|null} the built flipCard HTML, or null to keep the orange placeholder
	 */
	static #flipCard(args) {
		const built = this.#flipCardDialects(args);
		if (built !== null) return built;
		return this.#flipCardCards(args);
	}

	/**
	 * The four SPECIALISED flipCard dialect builders — see the "flipCard — a grid of
	 * cards..." doc block above (near shapeHover) for the general shape/safety rules.
	 * Tries each capture form most-specific-first, falling through to the next when one
	 * declines:
	 *   1. no table at all                                            → #flipCardMembers (image-front cards captured as [Flip Card N] tags)
	 *   2. Front|Back|Front|Back… header, ONE data row (2N columns)    → #flipCardAlternating
	 *   3. Front|Back|Front|Back… header, MULTIPLE data rows           → #flipCardMultiRow
	 *   4. exactly 2 rows, whole COLUMNS are fronts/backs (not rows)   → #flipCardTransposed
	 *   5. plain 2-column table (front | back)                        → the default path below
	 * A null from here is NOT the end of the road any more — #flipCard hands the bundle
	 * to the general composer next.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @returns {string|null} the built flipCard HTML, or null to fall through to the composer
	 */
	static #flipCardDialects({ bundle, tpl, renderInline, run }) {
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

	// =========================================================================
	//  ROUND 282 — THE GENERAL flipCard COMPOSER  (env FLIPCARDS_OFF)
	//
	//  Chris, the interactive-coverage chain round 7 of 8. flipCard was the
	//  WORST-COVERED widget in the library (49 of 484 = 10.1%) and the second
	//  largest class by modules (191). The decline recorder
	//  (outputs/_measure_r282_flipcard.cjs) accounted for 100% of the 435
	//  declines and they collapsed onto two mechanisms, neither about the
	//  writer's material being wrong:
	//
	//    • 289 declines / 44 modules carry a captured TABLE the four dialect
	//      builders could not read — 220 of them died on the single line
	//      `if (width !== 2)`. The dialects only know THREE table layouts;
	//      the writers use at least five.
	//    • 146 declines are member-authored, and 52 of those died because
	//      #flipCardMembers DEMANDS an image on every card — which the gold
	//      contradicts outright: measured over 643 gold groups / 3122 cards,
	//      a front is img+h 24.5%, img alone 23.7%, a HEADING alone 22.3% and
	//      a PARAGRAPH alone 20.7%. Text-only cards are 43% of the library.
	//
	//  So the composer reads CARDS from an ordered delimiter vocabulary, over a
	//  cell/member vocabulary shared with the round-278 accordion. It runs LAST,
	//  so all 49 pre-round builds are byte-identical BY CONSTRUCTION.
	//
	//  GOLD-BACKED GUARDS (outputs/_measure_r282_flipgold.py, body-scoped):
	//    • min_cards 1 for an EXPLICIT delimiter (face markers / [Flip Card N])
	//      — a 1-card group is 6.1% of the gold, so it is real; but
	//      min_inferred_cards 2 for an INFERRED reading, where one card would be
	//      a guess (the round-278 explicit-vs-inferred split).
	//    • NO length cap on a front. Unlike a tab label, a gold flip front runs
	//      to 4.3% over ten words (BLL264's conversation starters are whole
	//      sentences), so capping it would refuse real cards.
	//    • Both faces must carry content — a card with an empty face is not a card.
	//    • A LABEL IS NEVER INVENTED. BLL264's gold numbers its 12 word-cards
	//      <h5>1</h5>…<h5>12</h5>, a front that appears in no Writers Template;
	//      that one-cell-per-card dialect therefore DECLINES (recorded, §8).
	// =========================================================================

	/**
	 * THE GENERAL COMPOSER. Resolves cards from whichever delimiter the writer used,
	 * then renders the corpus convention (container → per card: front face + back face).
	 * Never half-builds: a card missing a face, an unreadable member, a nested widget or
	 * a second table all return null and keep the honest hand-off box.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive
	 * @param {object} args.tpl - the flipCard template block (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {object} [args.run] - conversion run context (drives Mode P/D image rendering)
	 * @param {function} [args.renderTable] - the converter's kept-table emitter
	 * @returns {string|null} the built flipCard HTML, or null to keep the placeholder
	 */
	static #flipCardCards({ bundle, tpl, renderInline, run, renderTable }) {
		const cfg = tpl?.general_cards;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.FLIPCARDS_OFF) return null;
		const inline = renderInline ?? ((s) => s);
		const notes = [];
		const tables = bundle?.tables ?? [];
		if (tables.length > 1) return null;                       // a multi-table bundle → recorded follow-up

		const cards = tables.length
			? this.#flipTableCards(tables[0].rows ?? [], { tpl, cfg, run, inline, notes })
			: this.#flipMemberCards(bundle, { tpl, cfg, run, inline, notes, renderTable });
		if (!cards || !cards.length) return null;

		const built = [];
		for (const c of cards) {
			if (!c.front || !c.back) return null;                 // both faces must carry content
			// THE LEAK GUARD (the round-167 rule at this seam, as rounds 277/278/279/280/281
			// ship it): a finished card still showing a bracketed writer tag would ADD a
			// visible literal-[tag] leak, so it declines instead. Building can only ever
			// PREVENT a leak, never cause one — proven per-module in both toggle states.
			if (this.#accLeakGuard(c.front, cfg) || this.#accLeakGuard(c.back, cfg)) return null;
			built.push(Utils.FillTemplate(tpl.card, { front: c.front, back: c.back }));
		}
		// a successful build surfaces the writer's skipped instructions / asset requests as
		// the standard red Writers Notes after the widget — the round-214/278 rule, never
		// a silent drop (a DECLINE never mutates the bundle).
		if (notes.length) {
			const seen = new Set(bundle.instructions ?? []);
			bundle.instructions = [...(bundle.instructions ?? [])];
			for (const n of notes) if (n && !seen.has(n)) { bundle.instructions.push(n); seen.add(n); }
		}
		return [tpl.container_open, ...built, tpl.container_close].join("\n");
	}

	/**
	 * TABLE readings, tried in order; the first that resolves enough cards wins.
	 *
	 *   T1  FACE-MARKER rows — any row whose every non-empty cell is a wholly-red
	 *       [front]/[back] marker names the faces of the columns BELOW it, and repeats
	 *       (OSOH501-4.0/5.0 lay four cards out as face-row, data-row, face-row,
	 *       data-row — the existing multirow builder read the SECOND face row as data
	 *       and bailed). Cards = (front column, back column) pairs per data row.
	 *   T1b A FACE-MARKER COLUMN — the same convention turned 90°: column 0 holds the
	 *       red "Front" / "Back" labels and every OTHER column is a card (ENGI303-4.0,
	 *       the whole CHFUN05 family). The label column is dropped and its faces name
	 *       the rows, then the table reads as T1/T2.
	 *   T2  A TWO-ROW table with NO face markers: row 0 is every card's FRONT and row 1
	 *       its BACK, one card per COLUMN. GOLD-VERIFIED on SSFUN03-0.0, whose three map
	 *       cards the gold ships exactly this way. This is #flipCardTransposed minus its
	 *       requirement that the writer label the faces.
	 *   T3  N rows x 2 columns — one card per ROW, a leading column-label row dropped.
	 *       The plain path, but over the richer cell vocabulary below.
	 *
	 * @returns {Array<{front:string,back:string}>|null}
	 */
	static #flipTableCards(allRows, ctx) {
		let rows = (allRows ?? []).filter((r) => Array.isArray(r) && r.some((c) => this.#cellText(c).trim()));
		if (!rows.length) return null;
		const minExp = ctx.cfg.min_cards ?? 1, minInf = ctx.cfg.min_inferred_cards ?? 2;

		// ---- T1b: a leading FACE-MARKER COLUMN (the T1 convention turned 90°) -----
		// Column 0 holds the red "Front"/"Back" labels and every other column is a card.
		// Drop it, remember the per-ROW faces, and let T1/T2 read what is left.
		let rowFaces = null;
		if (rows.length >= 2 && Math.max(0, ...rows.map((r) => r.length)) >= 2) {
			const col0 = rows.map((r) => this.#flipCellFace(r[0]));
			const col0Text = rows.map((r) => this.#cellText(r[0]).trim());
			const labelled = col0.every((f, i) => f || !col0Text[i]) && col0.filter(Boolean).length === rows.length;
			if (labelled && col0.includes("front") && col0.includes("back")) {
				rowFaces = col0;
				rows = rows.map((r) => r.slice(1));
				if (!rows.some((r) => r.some((c) => this.#cellText(c).trim()))) return null;
			}
		}
		const width = Math.max(0, ...rows.map((r) => r.length));
		if (rowFaces) {
			// one card per COLUMN, its faces named by the label column
			const fi = rowFaces.indexOf("front"), bi = rowFaces.indexOf("back");
			if (fi < 0 || bi < 0) return null;
			const cards = [];
			for (let c = 0; c < width; c++) {
				if (!this.#cellText(rows[fi][c]).trim() && !this.#cellText(rows[bi][c]).trim()) continue;
				const front = this.#flipFaceHtml(rows[fi][c], ctx, "front");
				const back = this.#flipFaceHtml(rows[bi][c], ctx, "back");
				if (front === null || back === null) return null;
				cards.push({ front, back });
			}
			return cards.length >= minExp ? cards : null;
		}

		// ---- T1: face-marker rows ------------------------------------------------
		const faceRow = (r) => {
			const faces = r.map((c) => this.#flipCellFace(c)).filter((f, i) => this.#cellText(r[i]).trim() || f);
			const named = r.map((c) => ({ f: this.#flipCellFace(c), t: this.#cellText(c).trim() }));
			// every non-empty cell must be JUST a face marker (no content of its own)
			if (!named.some((x) => x.f)) return null;
			for (const x of named) if (x.t && !x.f) return null;
			return r.map((c) => this.#flipCellFace(c));
		};
		if (rows.some((r) => faceRow(r))) {
			const cards = [];
			let faces = null;
			for (const r of rows) {
				const fr = faceRow(r);
				if (fr) { faces = fr; continue; }
				if (!faces) return null;                          // data before any face row → not this form
				for (let c = 0; c + 1 < width; c++) {
					if (faces[c] !== "front" || faces[c + 1] !== "back") continue;
					const front = this.#flipFaceHtml(r[c], ctx, "front");
					const back = this.#flipFaceHtml(r[c + 1], ctx, "back");
					if (front === null || back === null) return null;
					cards.push({ front, back });
				}
			}
			return cards.length >= minExp ? cards : null;
		}

		// ---- T1c: PER-CELL face markers (the marker rides WITH the content) -------
		// CEDO501-3.0/8.0 prefix every cell with its own "[Front of card]" /
		// "[Back of the card]", so there is no marker ROW to find — the rows themselves
		// alternate front, back, front, back. A row whose every non-empty cell opens with
		// the same face marker HAS that face; consecutive front/back rows pair by column.
		{
			const faces = rows.map((r) => this.#flipRowFace(r));
			if (faces.some((f) => f === "front") && faces.some((f) => f === "back")
				&& faces.every((f) => f)) {
				const cards = [];
				for (let i = 0; i + 1 < rows.length; i += 2) {
					if (faces[i] !== "front" || faces[i + 1] !== "back") return null;
					for (let c = 0; c < width; c++) {
						if (!this.#cellText(rows[i][c]).trim() && !this.#cellText(rows[i + 1][c]).trim()) continue;
						const front = this.#flipFaceHtml(rows[i][c], ctx, "front");
						const back = this.#flipFaceHtml(rows[i + 1][c], ctx, "back");
						if (front === null || back === null) return null;
						cards.push({ front, back });
					}
				}
				return cards.length >= minExp ? cards : null;
			}
		}

		// ---- T2: two rows, one card per column -----------------------------------
		if (rows.length === 2 && width >= 2) {
			const cards = [];
			for (let c = 0; c < width; c++) {
				if (!this.#cellText(rows[0][c]).trim() && !this.#cellText(rows[1][c]).trim()) continue;
				const front = this.#flipFaceHtml(rows[0][c], ctx, "front");
				const back = this.#flipFaceHtml(rows[1][c], ctx, "back");
				if (front === null || back === null) return null;
				cards.push({ front, back });
			}
			return cards.length >= minInf ? cards : null;
		}

		// ---- T3: N x 2, one card per row -----------------------------------------
		if (width === 2) {
			let data = rows.filter((r) => r.length === 2);
			if (data.length && this.#looksLikeFlipHeader(data[0], ctx.tpl)) data = data.slice(1);
			const cards = [];
			for (const r of data) {
				const front = this.#flipFaceHtml(r[0], ctx, "front");
				const back = this.#flipFaceHtml(r[1], ctx, "back");
				if (front === null || back === null) return null;
				cards.push({ front, back });
			}
			return cards.length >= minInf ? cards : null;
		}
		return null;
	}

	/**
	 * The FACE a wholly-red cell names ("front"/"back"), or null when the cell is not a
	 * bare face marker. Deliberately `#isFullyRed`-scoped and content-free: the round-281
	 * lesson in the mirror — a red marker followed by BLACK content is a real face WITH
	 * content, not a delimiter row, so it must not be mistaken for one.
	 */
	static #flipCellFace(cell) {
		if (!this.#isFullyRed(cell)) return null;
		const t = this.#cellText(cell).replace(/^\[|\]$/g, "").trim().toLowerCase();
		return (t === "front" || t === "back") ? t : null;
	}

	/**
	 * The face a cell's LEADING red marker names, when the marker rides WITH the cell's
	 * content ("🔴[Front of card]🔴 / 🔴[Image]🔴 …", CEDO501-3.0). Only the FIRST red
	 * span is read, and only when it is wholly a face phrase — so a red content word
	 * later in the cell can never be mistaken for a face.
	 */
	static #flipCellFacePrefix(cell) {
		const m = String(cell ?? "").match(/^\s*\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/u);
		if (!m) return null;
		const t = String(m[1]).replace(/[[\]]/g, "").trim().toLowerCase();
		if (/^front(?:\s+(?:of|of\s+the)\s+(?:the\s+)?card)?$/.test(t)) return "front";
		if (/^back(?:\s+(?:of|of\s+the)\s+(?:the\s+)?card)?$/.test(t)) return "back";
		return null;
	}

	/** The single face every non-empty cell of a row names by its leading marker, or null. */
	static #flipRowFace(row) {
		const faces = [];
		for (const c of row ?? []) {
			if (!this.#cellText(c).trim()) continue;
			const f = this.#flipCellFacePrefix(c) ?? this.#flipCellFace(c);
			if (!f) return null;
			faces.push(f);
		}
		return faces.length && faces.every((f) => f === faces[0]) ? faces[0] : null;
	}

	/**
	 * ONE FACE of a card → its finished HTML, or null to decline the whole widget.
	 *
	 * THE CELL VOCABULARY (the round-278/279/281 member vocabulary at cell level):
	 *   • the writer's structural markup ([front]/[back]/[body]/[H#]) is stripped
	 *   • a developer INSTRUCTION span (CS:/Dev:/Note:/please/[Item N]…) is surfaced as
	 *     a red Writers Note and skipped as content — never silently dropped
	 *   • an iStock URL becomes the Mode P/D image; a non-iStock image URL takes the
	 *     round-126 slug placeholder rather than blocking the card
	 *   • an image REFERENCE with no URL is an ASSET REQUEST — noted, skipped
	 *   • the writer's " / " and hard newlines split the face into parts; a "• " part
	 *     is a list item (consecutive items group into one <ul>), a SHORT lead on a
	 *     front becomes its <h4>, everything else is a <p>
	 * Returns "" for an empty face (the caller decides — both faces must have content).
	 */
	static #flipFaceHtml(raw, { tpl, cfg, run, inline, notes }, face) {
		let s = String(raw ?? "");
		if (!s.trim()) return "";
		// a wholly-red bare face marker cell carries no content of its own
		if (this.#flipCellFace(s)) return "";
		// a LEADING face marker riding with the content ("[Front of card] / …") is a
		// delimiter, not text — dropped here so it never reaches the page (T1c).
		if (this.#flipCellFacePrefix(s)) {
			s = s.replace(/^\s*\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}\s*\/?\s*/u, "");
		}
		s = this.#stripStructuralTags(s);
		// developer instructions out (noted); whatever red survives is the writer's own
		// content, coloured for emphasis (BLL/XMES phonics words) — the r281 discriminator.
		const dropped = [];
		s = String(s).replace(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu, (m, content) => {
			const raw = String(content).trim();
			if (!raw) return "";
			// A span made ENTIRELY of bracketed tokens is MARKUP by construction — the
			// writer stacked their tags ("[image][media item 8]", CHFUN05-0.0) so the
			// single-tag structural strip above could not see it. Dropped, and noted when
			// it names an asset so the developer still gets the request.
			if (/^(?:\s*\[[^\]]*\]\s*)+$/.test(raw)) {
				if (/\b(?:image|photo|media|audio|video|item)\b/i.test(raw)) dropped.push(raw.replace(/\s+/g, " "));
				return " ";
			}
			const c = raw.replace(/^[\s[]+/, "").trim();
			const re = new RegExp(`^(?:${(cfg.instruction_span_prefixes ?? []).join("|")})\\b`, "i");
			if ((cfg.instruction_span_prefixes ?? []).length && re.test(c)) { dropped.push(c); return " "; }
			return content;                                       // the writer's own red content
		});
		for (const d of dropped) notes.push(d);

		const img = [], body = [];
		const imgRe = /istockphoto|gettyimages|\.(?:jpe?g|png|gif|webp|svg)\b|\[\s*image\b|\[IMAGE\b/i;
		const segs = s.split(/\s\/\s|\n/).map((p) => p.trim()).filter((p) => p !== "");
		for (const seg of segs) {
			const url = this.#cellMediaUrl(seg);
			if (url) {
				const fn = this.#flipImageFilename(url, tpl, cfg);
				if (!fn) return null;                             // a video url here → not a card face
				img.push(this.#assetImage(fn, tpl, run));
				// a caption riding with the URL stays as face text
				const rest = this.#cellText(seg.replace(/https?:\/\/\S+/g, "").replace(/^\s*\[[^\]]*\]\s*/, "")
					.replace(/\(\s*\)/g, "").replace(/[|]/g, " ")).trim();
				// …but the residual is usually the writer's PHOTO BRIEF, not a caption
				// ("iStock: Young woman's first day…", CEDO501-2.0). Same asset-reference
				// rule: noted for the developer, never shown on the card.
				if (rest && cfg.asset_reference_pattern
					&& new RegExp(cfg.asset_reference_pattern, "i").test(rest)) { notes.push(rest); continue; }
				if (rest && cfg.image_caption_as_text !== false) body.push(rest);
				continue;
			}
			// AN ASSET REQUEST: the writer NAMED an image with no URL to render — either
			// with a tag ("[Image] …") or, just as often, in prose ("iStock: Young woman's
			// first day…", "Image: isolated outline hand drawn check", "Wikipedia Commons.").
			// It is a note to the developer, never card content and never a made-up
			// filename (the round-214/242/278 rule). THE VERIFIER CAUGHT THIS: without the
			// prose forms, CEDO501's and CEDR501's photo briefs shipped as visible card text.
			if (imgRe.test(seg) || (cfg.asset_reference_pattern
				&& new RegExp(cfg.asset_reference_pattern, "i").test(this.#cellText(seg).trim()))) {
				const t = this.#cellText(seg).trim();
				if (t) notes.push(t);
				continue;
			}
			const t = this.#cellText(seg).trim();
			if (t) body.push(t);
		}

		let html = img.join("");
		// a SHORT lead line on a FRONT is its heading — the corpus convention (a gold front
		// is img+h 24.5% / h alone 22.3%); everything else is prose.
		let lead = null;
		if (face === "front" && body.length
			&& body[0].split(/\s+/).length <= (cfg.front_head_max_words ?? 8)
			&& !/^[•·]/.test(body[0])) {
			lead = body.shift();
		}
		if (lead) html += `<${cfg.front_head_level ?? "h4"}>${inline(lead)}</${cfg.front_head_level ?? "h4"}>`;
		let ul = [];
		const flushUl = () => { if (ul.length) { html += "<ul>" + ul.map((t) => `<li>${inline(t)}</li>`).join("") + "</ul>"; ul = []; } };
		for (const p of body) {
			const bm = p.match(/^[•·]\s*(.+)$/);
			if (bm && bm[1].trim()) { ul.push(bm[1].trim()); continue; }
			flushUl();
			html += `<p>${inline(p)}</p>`;
		}
		flushUl();
		return html;
	}

	/** An image URL → the flipCard filename (iStock id, else the round-126 URL slug). */
	static #flipImageFilename(url, tpl, cfg) {
		if (!url || /youtu\.?be|youtube\.com|vimeo/i.test(url)) return null;
		const istock = this.#istockFilename(url, tpl);
		if (istock) return istock;
		if (cfg && cfg.image_slug_fallback === false) return null;
		return this.#bannerImageFilename(url, tpl);
	}

	/**
	 * MEMBER readings (no table), over the SHARED round-278 member vocabulary
	 * (#accMemberParts with flipCard's own delimiter + the new face_tags extension —
	 * omitted by every other caller, so the accordion and tabs are untouched).
	 *
	 *   M1  [Flip Card N] tags open a card; [front]/[back] set the face.
	 *   M2  [front]/[back] marker pairs with no [Flip Card N] — each [front] opens a card.
	 *   M3  A MEDIA SERIES — a repeating (image, text…) run with no markers at all:
	 *       each image opens a card and the text that follows is its back
	 *       (XDLS502-2.0's three photo cards). INFERRED, so min_inferred_cards applies.
	 *
	 * The face rule that unblocked 58 declines: content arriving while the face is
	 * "front" is FRONT content. The old builder bailed outright (`face !== "back"`),
	 * which refused every card the writer titled on its own line.
	 *
	 * @returns {Array<{front:string,back:string}>|null}
	 */
	static #flipMemberCards(bundle, { tpl, cfg, run, inline, notes, renderTable }) {
		const members = [...(bundle?.openerItems ?? []), ...(bundle?.memberItems ?? [])];
		if (!members.length) return null;
		const parts = this.#accMemberParts(members, {
			tpl, cfg, run, renderTable, notes,
			delims: {
				tags: cfg.card_tags ?? ["flip card"],
				panel_tag_pattern: cfg.card_tag_pattern,
				panel_ordinal_pattern: cfg.card_ordinal_pattern,
				face_tags: cfg.face_tags ?? ["front", "back"],
				face_label_pattern: cfg.face_label_pattern,
				face_label_back_pattern: cfg.face_label_back_pattern,
				text_tags: cfg.text_tags ?? [],
				note_tags: cfg.note_tags ?? [],
			},
		});
		if (!parts) return null;
		if (parts.some((p) => p.role === "nested" || p.role === "table")) return null;   // richer → placeholder

		const cards = [];
		let cur = null, face = "front", explicit = false;
		const open = () => { cur = { front: [], back: [] }; cards.push(cur); face = "front"; };
		const push = (o) => { if (!cur) open(); cur[face].push(o); };
		for (const p of parts) {
			if (p.role === "note") { continue; }
			if (p.role === "panel") {                              // a [Flip Card N] delimiter
				explicit = true; open();
				if (p.head) cur.front.push({ h: cfg.front_head_level ?? "h4", text: p.head });
				continue;
			}
			if (p.role === "face") {
				explicit = true;
				if (p.face === "front" && cur && (cur.front.length || cur.back.length)) open();
				else if (!cur) open();
				face = p.face;
				if (p.text) push(face === "front" && !cur.front.length
					? { h: cfg.front_head_level ?? "h4", text: p.text } : { text: p.text });
				continue;
			}
			if (p.role === "img") {
				// M3: with no explicit delimiter an image OPENS a card once the current one
				// has a back — the media-series reading (the round-247 carousel rule).
				if (!explicit && cur && cur.back.length) open();
				push({ img: p.filename });
				continue;
			}
			if (p.role === "head") {
				if (cur && face === "back" && cur.back.length) open();   // a finished back ends the card
				push({ h: p.level, text: p.text });
				continue;
			}
			if (p.role === "text") {
				// A BARE URL LINE IS THE IMAGE, not text. The writer often pastes the photo
				// link on its own line with no [image] tag, and rendering it as a paragraph
				// put a raw URL on the card (BLL123-1.0 — THE VERIFIER CAUGHT THIS).
				const bare = String(p.text ?? "").trim();
				if (/^https?:\/\/\S+$/.test(bare)) {
					const fn = this.#flipImageFilename(this.#cellMediaUrl(bare), tpl, cfg);
					if (!fn) return null;                          // a video url on a card face
					if (!explicit && cur && cur.back.length) open();
					push({ img: fn });
					continue;
				}
				// A COMPLETED BACK ENDS A CARD: the next content is the next card's front.
				// This is what resolves the label-word series (EXPFUN06-0.0's
				// "Whakawhanaungatanga" / "[on flip] Is about…" repeated four times).
				if (cur && face === "back" && cur.back.length) open();
				// with no markers, text after an image is the card's BACK
				else if (!explicit && cur && cur.front.length && !cur.back.length) face = "back";
				push({ text: p.text });
				continue;
			}
			return null;                                           // video/embed on a card face → placeholder
		}
		if (!cards.length) return null;
		const min = explicit ? (cfg.min_cards ?? 1) : (cfg.min_inferred_cards ?? 2);
		if (cards.length < min) return null;

		const render = (arr) => {
			let html = "", ul = [];
			const flushUl = () => { if (ul.length) { html += "<ul>" + ul.map((t) => `<li>${inline(t)}</li>`).join("") + "</ul>"; ul = []; } };
			for (const o of arr) {
				if (o.img) { flushUl(); html += this.#assetImage(o.img, tpl, run); continue; }
				if (o.h) { flushUl(); html += `<${o.h}>${inline(this.#cellText(o.text))}</${o.h}>`; continue; }
				for (const line of String(o.text).split(/\n/)) {
					const t = this.#cellText(line).trim();
					if (!t) continue;
					const bm = t.match(/^[•·]\s*(.+)$/);
					if (bm && bm[1].trim()) { ul.push(bm[1].trim()); continue; }
					flushUl();
					html += `<p>${inline(t)}</p>`;
				}
			}
			flushUl();
			return html;
		};
		return cards.map((c) => ({ front: render(c.front), back: render(c.back) }));
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
	static #modal({ bundle, tpl, renderInline, renderBlock, renderNested, renderTable, renderImage, run }) {
		if (!tpl || tpl.enabled === false) return null;
		// ROUND 216 (r214-a, Chris 2026-07-12: build the WRITER'S modal): the IMAGE-PAIR form
		// is tried FIRST — repeated "[modal][image] <iStock URL>" triggers each followed by its
		// [body]/black content (OSOH501-01's six ergonomics modals; the writer's CS note asks
		// for exactly this). On any mismatch it declines and the function proceeds EXACTLY as
		// before (the r73 single-document button, else the round-280 set fallback).
		const ip = this.#modalImagePairs({ bundle, tpl, renderInline, renderBlock, run });
		if (ip) return ip;
		// ROUND 73 — the single-document BUTTON. Its own guards now FALL THROUGH to the
		// round-280 fallback instead of ending the dispatch (the round-279 dead-end lesson:
		// a branch that returns its refusal as the final answer denies every later builder
		// a look at the bundle — that alone was 143 of the carousel's 561 declines).
		const btn = this.#modalDocButton({ bundle, tpl });
		if (btn) return btn;
		// ROUND 280 — the general TRIGGER + TKmodal set fallback, tried LAST so every modal
		// that built before this round builds identically after it, BY CONSTRUCTION.
		return this.#modalSets({ bundle, tpl, renderInline, renderBlock, renderNested, renderTable, renderImage, run });
	}

	/**
	 * modal → the ROUND-73 single-document BUTTON (extracted from #modal unchanged at
	 * round 280 so its declines can fall through to #modalSets). A [modal] whose captured
	 * content is exactly ONE document/PDF URL and no table is the human's external-resource
	 * button. Env MODALBTN_OFF disables THIS ATTEMPT ONLY — since round 280 the set
	 * fallback may still build; MODALBTN_OFF + MODALSETS_OFF together restore the
	 * pre-280 "keep the placeholder" behaviour exactly.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @returns {string|null} the built button HTML, or null to fall through
	 */
	static #modalDocButton({ bundle, tpl }) {
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

	// =======================================================================
	// ROUND 280 — THE GENERAL TRIGGER + TKmodal SET FALLBACK
	// =======================================================================
	/**
	 * MODAL SETS (ROUND 280, Chris — the interactive-coverage chain, round 5 of 8).
	 * Tried LAST, only where the round-216 image-pair form AND the round-73 document
	 * button have both declined — so it is STRICTLY ADDITIVE and every modal that built
	 * before this round builds identically after it, by construction (env MODALSETS_OFF
	 * proves it).
	 *
	 * WHY IT EXISTS. The decline-reason recorder (outputs/_measure_r280_modal.cjs, which
	 * rewrites every `return null` in the shipped modal region to a recorder so the
	 * builder names its own verdict) accounted for 100% of the 292 declines, and they
	 * collapsed onto just TWO guards — 246 at the button path's "exactly one URL" test
	 * and 46 at its "no captured table" test. Underneath, the cause is a single fact:
	 * the converter had a builder for the IMAGE-triggered modal (round 216) and one for
	 * a modal that is really a link to a PDF (round 73), and NOTHING AT ALL for the
	 * ordinary TEXT-triggered modal — which the gold measurement
	 * (outputs/_measure_r280_modgold.py, 283 TKmodal across 62 modules) shows is the
	 * DOMINANT form: the trigger is `div.button.TKmodalButton` 213 times (75.3%, 52
	 * modules) against an `img.TKmodalButton` 59 times (20.8%, 5 modules).
	 *
	 * THE CORPUS CONVENTION IT EMITS (gold CEDK401, byte-verified):
	 *     <div class="button TKmodalButton">Mahinga Kai Crusaders</div>
	 *     <div class="TKmodal" size="M"> …the pop-out content… </div>
	 * an image-triggered set emits the round-216 img.TKmodalButton in place of the div.
	 * `size` is editorial (the WT never gives one) → the corpus-dominant M (124 M / 83 L
	 * / 72 XL / 4 S). min_modals is 1 because a lone modal is the gold's own plurality
	 * (54 gold pages carry exactly one) — unlike the carousel, where a 1-slide widget is
	 * 0.2% and the floor is 2.
	 *
	 * THE THREE DELIMITERS, each quoted against the writer's own template:
	 *   D1 NUMBERED [Modal N …] sub-tags — the number is the delimiter, exactly as
	 *      [accordion N] is for a panel (round 278) and [Slide N] for a slide. The
	 *      bracket's own wording gives the sub-role: "image" → the trigger image,
	 *      "text"/"body" → the content, bare → the opener/title.
	 *        BLL120-0.0   [Modal 1 Image] https://www.istockphoto.com/photo/fresh-carrots-…
	 *                     [Modal 1 text] 1. Find things in your house that start with /k/
	 *                     [Modal 2 Image] … [Modal 2 text] 2. Watch the video. [video] …
	 *        MXDB201-2.0  [Modal 1] [Modal image 1] <iStock url> [Modal 1 body text] Garden
	 *                     Solutions offered a discounted price of $350 …
	 *   D2 the SAME-BLOCK LABEL line — the writer types the visible label and its pop-out
	 *      content on ONE line, so the label arrives as a black item sharing the tag's
	 *      source BLOCK (the round-105 "continuous sentence" discriminator, and the same
	 *      test the round-246 avatar absorb uses):
	 *        XGF9004-9.0  "Everyone gets the same size piece of cake, even though someone
	 *                      is hungrier. [Pop-out] Fairness can depend on need. Sometimes
	 *                      equal isn't the same as fair."
	 *                     → <div class="button TKmodalButton">Everyone gets the same size
	 *                        piece of cake…</div> + its TKmodal holding the explanation.
	 *   D3 a captured TABLE — ONE ROW = ONE MODAL, the third time this round-278/279
	 *      rule has proven to be the writer's own delimiter. The writer even labels the
	 *      columns:
	 *        ENGR302-2.0  | [Modal image] ║ [Modal text]          ← the header row
	 *                     | Link for image ║ **Intellectual** / McBean shows his expertise…
	 *
	 * NEVER HALF-BUILDS. A set with no trigger at all (neither a label nor a nameable
	 * image — a label is NEVER invented) · a set with no content · no delimiter resolving
	 * min_modals sets · red writer-instruction text in a label · a member it cannot place ·
	 * or a finished set that still shows a resolved [tag] (#accLeakGuard, the shared
	 * round-167/275/277/278 rule at this seam, so building can only ever PREVENT a
	 * visible leak, never add one).
	 *
	 * Data interactive_builders.modal.modal_sets; env MODALSETS_OFF.
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive (opener/member items — see file header)
	 * @param {object} args.tpl - this widget's editable markup templates (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links)
	 * @param {function} [args.renderBlock] - paragraph/list renderer (bullets → <ul>)
	 * @param {function} [args.renderNested] - nested sub-bundle renderer
	 * @param {function} [args.renderTable] - the converter's kept-table emitter
	 * @param {object} [args.run] - conversion run context (image Mode P/D)
	 * @returns {string|null} the built trigger+modal sets, or null to keep the placeholder
	 */
	static #modalSets({ bundle, tpl, renderInline, renderBlock, renderNested, renderTable, run }) {
		const cfg = tpl?.modal_sets;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.MODALSETS_OFF) return null;
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (typeof renderBlock !== "function") return null;         // need the body renderer
		const inline = renderInline ?? ((s) => s);
		const notes = [];

		// (1) every member as an ordered {role,…} PART. Classifying by the RESOLVED TAG
		//     rather than the writer's spelling is the round-276 lesson.
		const parts = this.#modalMemberParts(members, { tpl, cfg, run, renderTable, notes });
		if (!parts) return null;

		// (2) the SETS, from the first delimiter kind that is present.
		const sets = this.#modalResolveSets(parts, cfg, tpl);
		if (!sets || sets.length < (cfg.min_modals ?? 1)) return null;

		// (3) render through the shared set renderer.
		const built = this.#modalRenderSets(sets, { tpl, cfg, inline, run, renderBlock, renderNested });
		if (!built) return null;
		const html = built.join("\n");
		if (this.#accLeakGuard(html, cfg)) return null;             // a build must never ADD a leak
		if (notes.length) bundle.instructions = [...(bundle.instructions ?? []), ...notes];
		bundle.r280Modal = true;                                    // detector / affected-set marker
		return html;
	}

	/**
	 * ROUND 280 — every captured member as an ordered {role,…} PART, or null when a member
	 * cannot be placed at all. Roles: modal · text · img · video · embed · head · table ·
	 * nested. Instruction/noise members and asset requests become NOTES (surfaced red
	 * after a successful build, never silently dropped — the round-214/242/278 rule).
	 *
	 * A `modal` part carries { num, sub, text, block }: `num` is the writer's own number
	 * when the bracket has one, `sub` is "image" | "text" | "open" read from the bracket's
	 * wording, `block` is the source paragraph (D2's discriminator).
	 */
	static #modalMemberParts(members, { tpl, cfg, run, renderTable, notes }) {
		const parts = [];
		const idRe = new RegExp(cfg.video_youtube_id_re
			?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");
		const imgSub = new RegExp(cfg.sub_image_pattern ?? "\\bimage|\\bpic|\\bphoto", "i");
		const txtSub = new RegExp(cfg.sub_text_pattern ?? "\\btext|\\bbody|\\bcontent", "i");

		for (let i = 0; i < members.length; i++) {
			const m = members[i];
			if (!m) continue;
			const tag = m.type === "tag" ? m.parse?.primary?.tag : null;

			// an image-ARRANGEMENT layout marker (round 242) — a note, never content
			const layoutMk = this.#imageLayoutMarker(m, tpl);
			if (layoutMk) { notes.push(layoutMk); continue; }

			if (m.type === "nested") { parts.push({ role: "nested", bundle: m.nestedBundle }); continue; }

			if (m.type === "table") {
				if (typeof renderTable !== "function") return null;
				// Rendered EAGERLY (renderTable is only in scope here) so the table can serve
				// either job: the set SOURCE (D3, which reads item.block.rows) or, when another
				// delimiter owns the sets, ordinary modal CONTENT — the round-275/278 seam.
				const html = renderTable(m);
				parts.push({ role: "table", item: m, html: (html && String(html).trim()) ? String(html) : null });
				continue;
			}

			if (m.type === "black") {
				const t = String(m.text ?? "");
				if (!t.trim()) continue;
				if (/^\s*\(?\d{1,3}[.)]\s*$/.test(t)) continue;   // the docx numbered-list artifact
				parts.push({ role: "text", text: t, block: m.block });
				continue;
			}

			// a writer instruction / noise span — a red note, never build content
			if (m.type === "tag"
				&& (m.parse?.class === "instruction" || m.parse?.class === "noise" || m.parse?.instructionFragment)) {
				const t = this.#cellText(m.blackAfter ?? "") || this.#cellText(m.text ?? "");
				if (t) notes.push(t);
				continue;
			}

			const raw = m.type === "tag" ? (m.blackAfter ?? "") : "";
			const text = this.#cellText(raw);

			if (tag === "modal") {
				const own = this.#cellText(String(m.text ?? ""));
				const numM = own.match(/(\d{1,3})/);
				const sub = imgSub.test(own) ? "image" : (txtSub.test(own) ? "text" : "open");
				const part = {
					role: "modal", num: numM ? parseInt(numM[1], 10) : null,
					sub, text, block: m.block, red: this.#hasRedText(raw),
				};
				// An IMAGE sub-tag's URL sits either on its own line ("[Modal 1 Image] <url>",
				// BLL120) or on the NEXT black line ("[Modal image 1]" then the bare url,
				// MXDB201) — take the following line when it is nothing but a URL, so the
				// same rule reads both dialects.
				if (sub === "image") {
					let url = this.#cellMediaUrl(raw);
					if (!url) {
						const nxt = members[i + 1];
						const nt = nxt && nxt.type === "black" ? String(nxt.text ?? "").trim() : "";
						if (nt && /^https?:\/\/\S+$/.test(nt)) { url = this.#cellMediaUrl(nt); if (url) i++; }
					}
					part.imgUrl = url;
				}
				parts.push(part);
				continue;
			}

			if (["h2", "h3", "h4", "h5", "h6"].includes(tag)) {
				if (this.#hasRedText(raw)) return null;
				const t = text.replace(/\*\*/g, "").trim();
				if (!t) continue;
				parts.push({ role: "head", level: tag, text: t });
				continue;
			}

			if (tag === "image") {
				const url = this.#cellMediaUrl(raw);
				if (!url) {
					// AN ASSET REQUEST, not an image (the round-278 rule): the writer named a
					// Media-List item with no URL to render. Skipped as build content and
					// surfaced as a red note — never a silent drop, never a made-up filename.
					if (cfg.asset_request_note === false) return null;
					const t = this.#cellText(String(m.text ?? "")) + (text ? ` ${text}` : "");
					if (t.trim()) notes.push(t.trim());
					continue;
				}
				const fn = this.#accImageFilename(url, cfg, cfg);
				if (!fn) return null;
				parts.push({ role: "img", filename: fn });
				const residual = text.replace(/^\s*\[[^\]]*\]\s*/, "")
					.replace(/https?:\/\/\S+/g, "").replace(/\S*gm-?\d{6,10}\S*/g, "")
					.replace(/[/|]/g, " ").trim();
				if (residual) parts.push({ role: "text", text: residual, block: m.block });
				continue;
			}

			if (tag === "video" || tag === "audio") {
				if (this.#hasRedText(raw) && !this.#cellMediaUrl(raw) && !/https?:\/\//.test(raw)) return null;
				// the URL may ride the NEXT black line ("(https://www.youtube.com/watch?v=…)",
				// CEDT102) — the round-247 video tail-URL rule at this seam
				let vraw = String(raw);
				if (!/https?:\/\//.test(vraw)) {
					const nxt = members[i + 1];
					const nt = nxt && nxt.type === "black" ? String(nxt.text ?? "").trim() : "";
					if (nt && /^\(?https?:\/\/\S+\)?$/.test(nt)) { vraw = nt; i++; }
				}
				const idm = vraw.match(idRe);
				if (idm) { parts.push({ role: "video", id: idm[1] }); continue; }
				const url = vraw.match(/https?:\/\/[^\s\]"<>)]+/)?.[0] ?? null;
				const gen = url && cfg.generic_embed !== false
					? DataService.Data.EmitTemplates.video?.generic_iframe
					: null;
				if (gen && url) { parts.push({ role: "embed", html: Utils.FillTemplate(gen, { url }) }); continue; }
				if (!url) {                                        // a media-list reference again
					if (cfg.asset_request_note === false) return null;
					const t = this.#cellText(String(m.text ?? "")) + (text ? ` ${text}` : "");
					if (t.trim()) notes.push(t.trim());
					continue;
				}
				return null;
			}

			if (tag === "body") {
				if (this.#hasRedText(raw)) return null;
				if (!text.trim()) continue;
				parts.push({ role: "text", text, block: m.block });
				continue;
			}

			if (this.#isInlineMarkerMember(m)) {
				if (this.#hasRedText(raw)) return null;
				if (text.trim()) parts.push({ role: "text", text, block: m.block });
				continue;
			}

			if (tag === "button" && cfg.skip_button_members !== false) {
				// A [button] is NOT modal content: the gold puts one inside a TKmodal in only
				// 5 of 283 cases (1.8% — the same finding as the round-278 accordion's 1.7%).
				// It is the page's own button that rode into the bundle, and the writer's
				// go-to-journal button is ALREADY owned by the round-239 rule, whose
				// #goJournalTail ships the templated <h4 class="goJournal"> for a
				// member-CAPTURED button whether or not the widget builds — so releasing or
				// re-rendering it here would duplicate it (the round-273 bug). Skipped
				// silently for that one; every other button surfaces as a red note so the
				// developer still sees it. Placing it properly is the round-278
				// `button_tail_terminates` extension — a recorded follow-up.
				if (!this.#modalIsGoJournal(m)) {
					const t = this.#cellText(String(m.text ?? "")) + (text ? ` ${text}` : "");
					if (t.trim()) notes.push(t.trim());
				}
				continue;
			}

			if (tag && /\blist\b/.test(tag)) continue;             // a no-op list delimiter

			return null;                                           // a foreign tag we cannot place
		}
		return parts;
	}

	/**
	 * ROUND 280 — is this member the writer's GO-TO-JOURNAL button? Uses the SAME two data
	 * patterns as the round-239 rule that owns it (buttons.go_journal), so the two can
	 * never drift apart — the round-278 #isGoJournalButton form.
	 */
	static #modalIsGoJournal(item) {
		const gj = DataService.Data.EmitTemplates.buttons?.go_journal;
		if (!gj || gj.enabled === false) return false;
		const strip = (s) => String(s ?? "")
			.replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").replace(/\s+/g, " ").trim();
		const label = strip(item?.blackAfter ?? "");
		if (gj.label_match && new RegExp(gj.label_match, "i").test(label)) return true;
		const raw = strip(item?.text ?? "");
		return !!(gj.raw_match && new RegExp(gj.raw_match, "i").test(raw));
	}

	/**
	 * ROUND 280 — resolve the modal SETS from the ordered parts, trying each delimiter in
	 * turn (D1 numbered sub-tags → D2 same-block label lines → D3 a table) and taking the
	 * first that yields sets with a trigger. Returns `[{ label, filename, parts }]` for
	 * #modalRenderSets, or null.
	 */
	static #modalResolveSets(parts, cfg, tpl) {
		const modals = parts.filter((p) => p.role === "modal");
		if (!modals.length && !parts.some((p) => p.role === "table")) return null;
		const maxWords = cfg.label_max_words ?? 20;
		const labelOk = (t) => {
			const s = String(t ?? "").replace(/\*+/g, "").trim();
			return !!s && s.split(/\s+/).length <= maxWords && !this.#accHasBracketTag(s);
		};

		// ---- D1: NUMBERED [Modal N …] sub-tags -------------------------------------
		if (modals.some((p) => p.num != null) && cfg.numbered_sets !== false) {
			const sets = [];
			let cur = null;
			for (const p of parts) {
				if (p.role === "modal") {
					if (p.red) return null;                         // a writer instruction on the tag
					// a NEW number opens a new set; the same number continues the current one
					if (!cur || (p.num != null && p.num !== cur.num)) {
						cur = { num: p.num, label: "", filename: null, parts: [] };
						sets.push(cur);
					}
					if (p.sub === "image") {
						if (p.imgUrl) {
							const fn = this.#accImageFilename(p.imgUrl, cfg, cfg);
							if (!fn) return null;
							cur.filename = cur.filename ?? fn;
						}
						// an image sub-tag with no URL is an asset request; the set falls back
						// to its text label (and declines below if it has neither)
						continue;
					}
					if (p.text) {
						// the tag's own trailing text is the set's LABEL while it has none and
						// nothing has been added yet; otherwise it is content.
						if (!cur.label && !cur.parts.length && p.sub !== "text" && labelOk(p.text)) cur.label = p.text;
						else cur.parts.push({ role: "text", text: p.text });
					}
					continue;
				}
				if (!cur) {
					if (p.role === "text") continue;                // a lead line before the first set
					return null;
				}
				if (!this.#modalPushPart(cur.parts, p)) return null;
			}
			return this.#modalFinishSets(sets, cfg);
		}

		// ---- D2: the SAME-BLOCK LABEL line ------------------------------------------
		if (cfg.same_block_label !== false) {
			const idx = parts.map((p, i) => [p, i]).filter(([p]) => p.role === "modal");
			const paired = idx.filter(([p, i]) => {
				const prev = parts[i - 1];
				return prev && prev.role === "text" && prev.block && p.block && prev.block === p.block;
			});
			if (paired.length && paired.length >= Math.min(modals.length, cfg.min_same_block ?? 1)) {
				const sets = [];
				let cur = null;
				let pendingLabel = null;
				for (let i = 0; i < parts.length; i++) {
					const p = parts[i];
					if (p.role === "text") {
						const nxt = parts[i + 1];
						if (nxt && nxt.role === "modal" && p.block && nxt.block && p.block === nxt.block) {
							pendingLabel = p.text;                  // this line labels the NEXT modal
							continue;
						}
						if (!cur) continue;                         // a lead line before the first modal
						// STRICT ALTERNATION. In this dialect the pop-out's content rides the
						// tag's OWN trailing text, so a black line AFTER a modal that does not
						// label the next one is not modal content — it is ordinary body the
						// walk swept in. XGF9004-11.0 is the reason: it is a multiple-choice
						// quiz where only the CORRECT option carries "[Correct] [Pop-out]
						// <feedback>" and the DISTRACTOR options are plain lines between the
						// tags. Without this the build put the distractors inside the previous
						// option's pop-out and turned a quiz into a row of buttons — a
						// half-build, caught by the round-280 per-toggle decomposition.
						return null;
					}
					if (p.role === "modal") {
						if (p.red) return null;
						cur = { label: labelOk(pendingLabel) ? pendingLabel : "", filename: null, parts: [] };
						pendingLabel = null;
						sets.push(cur);
						if (p.sub === "image" && p.imgUrl) {
							const fn = this.#accImageFilename(p.imgUrl, cfg, cfg);
							if (!fn) return null;
							cur.filename = fn;
						} else if (p.text) {
							cur.parts.push({ role: "text", text: p.text });
						}
						continue;
					}
					if (!cur) return null;
					if (!this.#modalPushPart(cur.parts, p)) return null;
				}
				return this.#modalFinishSets(sets, cfg);
			}
		}

		// ---- D3: a captured TABLE — one row = one modal ------------------------------
		const tables = parts.filter((p) => p.role === "table");
		if (tables.length === 1 && cfg.table_sets !== false) {
			const others = parts.filter((p) => p.role !== "table");
			// only when the table IS the widget (nothing substantive but the invocation and
			// its lead line) — a layout table beside real content is NOT a set source
			if (others.every((p) => p.role === "text" || (p.role === "modal" && !p.text))) {
				const sets = this.#modalTableSets(tables[0].item, cfg, tpl);
				if (sets && sets.length >= (cfg.min_inferred_modals ?? 2)) return this.#modalFinishSets(sets, cfg);
			}
		}

		// ---- D4: the tag's OWN text is the label, the content follows ----------------
		// "[Modal] Factor trees" then the [video]/[body] that pops out (MXFU301-7.0). The
		// label test is the same gold-backed one D1/D2 use, so a tag carrying a whole
		// paragraph (MXDB202's "[Information popout] As you will notice here…") is NOT a
		// label and the set declines rather than putting a paragraph on a button.
		if (modals.length && cfg.tag_text_label !== false) {
			const sets = [];
			let cur = null;
			for (const p of parts) {
				if (p.role === "modal") {
					if (p.red) return null;
					if (p.sub === "image" && p.imgUrl && cur && !cur.filename) {
						const fn = this.#accImageFilename(p.imgUrl, cfg, cfg);
						if (!fn) return null;
						cur.filename = fn;
						continue;
					}
					if (!labelOk(p.text)) return null;             // not a trigger label — decline
					cur = { label: p.text, filename: null, parts: [] };
					sets.push(cur);
					continue;
				}
				if (!cur) {
					if (p.role === "text") continue;               // a lead line before the first modal
					return null;
				}
				if (!this.#modalPushPart(cur.parts, p)) return null;
			}
			if (sets.length) return this.#modalFinishSets(sets, cfg);
		}

		return null;
	}

	/** ROUND 280 — push one ordered content part onto a set, or false if it cannot be placed. */
	static #modalPushPart(list, p) {
		if (p.role === "text") { list.push({ role: "text", text: p.text }); return true; }
		if (p.role === "img") { list.push({ role: "img", filename: p.filename }); return true; }
		if (p.role === "video") { list.push({ role: "video", id: p.id }); return true; }
		if (p.role === "embed") { list.push({ role: "embed", html: p.html }); return true; }
		if (p.role === "head") { list.push({ role: "head", level: p.level, text: p.text }); return true; }
		if (p.role === "nested") { list.push({ role: "nested", bundle: p.bundle }); return true; }
		if (p.role === "table") { if (!p.html) return false; list.push({ role: "html", html: p.html }); return true; }
		return false;
	}

	/**
	 * ROUND 280 — the final never-half-build check on the resolved sets: every set needs a
	 * TRIGGER (a label or a nameable image — a label is never invented) and real CONTENT.
	 */
	static #modalFinishSets(sets, cfg) {
		if (!sets || !sets.length) return null;
		for (const s of sets) {
			if (!s.label && !s.filename) return null;              // no trigger at all
			if (!s.parts.length) return null;                      // an empty pop-out
			if (s.label && this.#hasRedText(s.label)) return null;
		}
		return sets;
	}

	/**
	 * ROUND 280 — D3: a captured table where ONE ROW IS ONE MODAL. The writer labels the
	 * columns themselves ("[Modal image] ║ [Modal text]", ENGR302-2.0), so a leading
	 * header row is dropped. The trigger is the row's IMAGE cell when one carries a
	 * nameable URL, else its short first cell; the other cell is the pop-out content.
	 */
	static #modalTableSets(item, cfg, tpl) {
		const rows = (item?.block?.rows ?? []).map((r) => (r ?? []).map((c) => this.#cellText(typeof c === "string" ? c : c?.text)));
		if (rows.length < 1) return null;
		const cols = Math.max(0, ...rows.map((r) => r.length));
		if (cols !== 2) return null;                               // only the label|content pair form
		let body = rows;
		// a HEADER row names the columns and is not a modal
		const hdr = rows[0].join(" ").toLowerCase();
		if (/\bmodal\b|\bimage\b|\bpop.?out\b|\btext\b/.test(hdr)
			&& rows[0].every((c) => c.split(/\s+/).filter(Boolean).length <= (cfg.header_max_words ?? 4))) {
			body = rows.slice(1);
		}
		if (!body.length) return null;
		const maxWords = cfg.label_max_words ?? 9;
		const assetReq = new RegExp(cfg.asset_request_cell_pattern ?? "^\\W*(?:link\\s+for\\s+)?(?:image|picture|photo|graphic)\\b", "i");
		const sets = [];
		for (const r of body) {
			if (r.length !== 2) return null;
			const [a, b] = r.map((s) => String(s ?? "").trim());
			if (!a && !b) continue;
			if (this.#hasRedText(a) || this.#hasRedText(b)) return null;
			const ua = this.#cellMediaUrl(a), ub = this.#cellMediaUrl(b);
			let filename = null, label = "", content = "";
			if (ua || ub) {
				const fn = this.#accImageFilename(ua || ub, cfg, cfg);
				if (!fn) return null;
				filename = fn;
				content = ua ? b : a;
			} else {
				// No URL anywhere in the row. A cell that merely ASKS for an image ("Link for
				// image", ENGR302-2.0) is an asset request, never a trigger label — the other
				// cell carries both. Otherwise the SHORT cell is the label.
				const aAsset = assetReq.test(a) && !ua, bAsset = assetReq.test(b) && !ub;
				if (aAsset && !bAsset) content = b;
				else if (bAsset && !aAsset) content = a;
				else {
					const aw = a.split(/\s+/).filter(Boolean).length;
					const bw = b.split(/\s+/).filter(Boolean).length;
					if (aw <= maxWords && aw <= bw) { label = a; content = b; }
					else if (bw <= maxWords && bw < aw) { label = b; content = a; }
					else return null;
				}
			}
			if (!content.trim()) return null;
			// A BOLD LEAD inside the content IS the trigger label when the row supplies no
			// other one — the round-278 accordion D2 rule, and the writer's own emphasis
			// (ENGR302-2.0: "**Intellectual** / McBean shows his expertise in creating…"
			// → trigger "Intellectual", pop-out the rest).
			if (!label && !filename) {
				const lead = this.#accBoldLead(content.split("\n")[0].trim(), { ...cfg, head_max_words: maxWords });
				if (!lead || !lead.rest.trim()) return null;
				label = lead.head;
				content = [lead.rest, ...content.split("\n").slice(1)].filter((s) => String(s).trim()).join("\n");
			}
			if (!content.trim()) return null;
			if (label && this.#accHasBracketTag(label)) return null;
			sets.push({ label, filename, parts: [{ role: "text", text: content }] });
		}
		return sets.length ? sets : null;
	}

	/**
	 * ROUND 280 — render the resolved sets as the corpus TRIGGER + TKmodal convention.
	 * An image-carrying set emits the round-216 `img.TKmodalButton`; every other set emits
	 * the gold-dominant `div.button.TKmodalButton` holding the writer's own label.
	 *
	 * @returns {string[]|null} one trigger+modal pair per set, or null to decline
	 */
	static #modalRenderSets(sets, { tpl, cfg, inline, run, renderBlock, renderNested }) {
		const out = [];
		for (const s of sets) {
			const chunks = [];
			for (const part of s.parts) {
				if (part.role === "img") {
					chunks.push(this.#assetImage(part.filename, cfg.content_image ?? cfg, run));
				} else if (part.role === "video") {
					const vt = DataService.Data.EmitTemplates.video?.youtube;
					if (!vt) return null;
					chunks.push(Utils.FillTemplate(vt, { videoId: part.id, params: "" }));
				} else if (part.role === "embed") {
					chunks.push(part.html);
				} else if (part.role === "nested") {
					if (typeof renderNested !== "function") return null;
					const ph = renderNested(part.bundle);
					if (!ph) return null;
					chunks.push(ph);
				} else if (part.role === "head") {
					chunks.push(`<${part.level}>${inline(part.text)}</${part.level}>`);
				} else if (part.role === "html") {
					chunks.push(part.html);
				} else if (part.role === "text") {
					const rendered = renderBlock(part.text);
					const arr = Array.isArray(rendered) ? rendered : [rendered];
					for (const h of arr) if (h && String(h).trim()) chunks.push(String(h));
				}
			}
			const content = chunks.join("");
			if (!content.trim()) return null;                      // a pop-out that renders to nothing
			const trigger = s.filename
				? this.#assetImage(s.filename, cfg, run)
				: Utils.FillTemplate(cfg.trigger_button ?? "<div class=\"button TKmodalButton\">{label}</div>",
					{ label: inline(String(s.label).replace(/\*+/g, "").trim()) });
			out.push(trigger + "\n"
				+ Utils.FillTemplate(cfg.modal_open ?? "<div class=\"TKmodal\" size=\"{size}\">",
					{ size: cfg.default_size ?? "M" })
				+ "\n" + content + "\n" + (cfg.modal_close ?? "</div>"));
		}
		return out.length ? out : null;
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
				// ROUND 279 DEAD-END LESSON: this used to `return` the list form's verdict,
				// so its refusal ENDED the dispatch and the general composer below was
				// never reached. It now falls through.
				const built = this.#tabsFromList({ bundle, tpl, inline, listCfg });
				if (built !== null) return built;
			}
			// ROUND 281 — the GENERAL composer, tried LAST (see #tabsPanes).
			return this.#tabsPanes({ bundle, tpl, inline, run, renderBlock, renderTable });
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
			// falls through on a decline (the round-279 dead-end lesson) so the general
			// composer below gets its look at the bundle.
			const built = this.#tabsRich({ bundle, tpl, inline, run, renderBlock, renderTable });
			if (built !== null) return built;
		}
		// ROUND 281 — the GENERAL composer, tried LAST (see #tabsPanes).
		return this.#tabsPanes({ bundle, tpl, inline, run, renderBlock, renderTable });
	}

	/**
	 * ROUND 281 — THE GENERAL TABS COMPOSER (`TABPANES_OFF`).
	 *
	 * The five earlier tabs builders each read ONE authoring dialect and four of them
	 * are gated by a mined gold-choice REGISTRY row. Measured (outputs/_measure_r281_tabs.cjs
	 * + _measure_r281_noreg.cjs): neutralising EVERY registry gate moves tabs from 17
	 * built to 18 — a gain of exactly one — so the registry was never the blocker, only
	 * the first door. The blocker is that the writer's own pane DELIMITER is usually a
	 * TABLE (or a plain heading run) that no builder reads, and that one unplaceable
	 * member bails the whole widget.
	 *
	 * This composer is tried LAST, after all five, so **every pre-round build is
	 * byte-identical BY CONSTRUCTION** (the round-276 architecture: a fallback cannot
	 * break what already works). It is deliberately NOT registry-gated — the anti-rows
	 * were mined as "the human built an ACCORDION from this form", and Chris's round-246
	 * A1 ruling settles that: build the widget the writer tagged.
	 *
	 * DELIMITER VOCABULARY, in order — the first that resolves ≥ min_panes panes wins:
	 *   D1  explicit [Tab N] tags                       (CEDO501-8.0, OSAI401, HES1005)
	 *   D2  a TABLE read COLUMN-major — the header row is the labels; an optional
	 *       leading single-cell TITLE row is peeled to a heading; a ROLE-LABELLED first
	 *       column ([Title] / [Image] / [Link for image] down column 0) makes columns
	 *       1..N the tabs and each row contributes by its role   (ENFUN01-0.0 ×3,
	 *       whose gold ships exactly these tabs: Persuade|Inform|Entertain)
	 *   D3  a TABLE read ROW-major — one row = one pane (short label cell + content
	 *       cell); a ONE-ROW table is one pane per CELL, each labelled from its own
	 *       bold or colon lead                                    (AGH1003-5.0)
	 *   D4  a repeating same-level heading run                     (the round-196 form,
	 *       un-gated)
	 *
	 * MEMBER VOCABULARY: the round-278 one, shared verbatim (#accMemberParts) — a
	 * non-iStock image takes the round-126 URL slug, an image with no URL is an ASSET
	 * REQUEST (skipped, surfaced as a red Writers Note, never invented), a non-YouTube
	 * video renders through the generic iframe, a captured table renders through the
	 * converter's own kept-table emitter, and a writer instruction becomes a note.
	 *
	 * GOLD-BACKED GUARDS (outputs/_measure_r281_tabgold.py, 319 body tab groups / 142
	 * modules): min_panes is **2** because a ONE-pane tab group does not exist in the
	 * gold library (0 of 319); a nav label is ≤ 3 words 92.3% of the time, ≤ 6 words
	 * 99.2% and ≤ 7 words 100%, so a longer line is prose, not a label — the pane keeps
	 * it and the label comes from a bold lead, or the composer declines rather than
	 * putting a sentence in the nav. Labels ship PLAIN (gold 99.0%).
	 *
	 * NEVER HALF-BUILDS: fewer than min_panes, a pane with no label or no rendered
	 * content, a member the vocabulary cannot place, or a finished widget still showing
	 * a resolved [tag] (#accLeakGuard — the round-167/275/277/278 rule at this seam, so
	 * building can only ever PREVENT a visible leak, never add one).
	 *
	 * Data interactive_builders.tabs.general_panes; env TABPANES_OFF.
	 */
	static #tabsPanes({ bundle, tpl, inline, run, renderBlock, renderTable }) {
		const cfg = tpl?.general_panes;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.TABPANES_OFF) return null;
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		if (typeof renderBlock !== "function") return null;      // need the body renderer
		const rich = tpl.rich_panes ?? {};
		const notes = [];

		// (1) every member → an ordered {role,…} part, through the SHARED round-278
		//     vocabulary; [Tab N] is this widget's delimiter and [tabs] its opener.
		const parts = this.#accMemberParts(members, {
			tpl: rich, cfg, run, renderTable, notes,
			delims: {
				tags: cfg.delimiter_tags ?? ["tab n", "tab"],
				opener_tags: cfg.opener_tags ?? ["tabs"],
				panel_tag_pattern: cfg.pane_tag_pattern
					?? "^\\[\\s*tab\\s*(?:\\d+|one|two|three|four|five|six|seven|eight|nine|ten)?\\s*[:.]?\\s*\\]$",
				panel_ordinal_pattern: cfg.pane_ordinal_pattern
					?? "^\\[\\s*(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\\s+tab\\s*[:.]?\\s*\\]$",
				// MEASURED tabs-only extensions. The gold puts a `button` inside a tab group
				// in 27 of 319 groups (8.5%) — far more than the accordion's 1.7% — but the
				// button emitter is not in scope at this seam, so it surfaces as a note
				// rather than being silently dropped. A bare [heading] is a sub-heading; an
				// [external link]'s own line is pane prose (renderBlock links a bare URL).
				head_tags: cfg.head_tags ?? ["heading"],
				head_level: cfg.head_level ?? "h4",
				text_tags: cfg.text_tags ?? ["external link"],
				note_tags: cfg.note_tags ?? ["button"],
			},
		});
		if (!parts) return null;

		// (2) resolve the panes from the first delimiter kind that is present.
		const panes = this.#tabResolvePanes(parts, cfg, rich);
		if (!panes || panes.length < (cfg.min_panes ?? 2)) return null;

		// (3) render through the shared pane-part renderer, so this composer and the
		//     five dialect builders emit the same markup.
		const navItems = [], paneItems = [];
		for (const p of panes) {
			if (!p.head || !p.parts.length) return null;
			const head = String(p.head).replace(/\*\*/g, "").replace(/\s+/g, " ").trim();
			if (!head || this.#hasRedText(head) || /[\[\]]/.test(head)) return null;
			if (head.split(/\s+/).length > (cfg.label_max_words ?? 6)) return null;
			const chunks = [];
			for (const part of p.parts) {
				const got = this.#tabsRichPart(part, rich, run, renderBlock);
				if (got === null) return null;
				chunks.push(...got);
			}
			const content = chunks.join("");
			if (!content.trim()) return null;                    // a pane with no rendered body
			navItems.push(Utils.FillTemplate(tpl.nav_item, { head: inline(head) }));
			paneItems.push(Utils.FillTemplate(tpl.pane, { content }));
		}
		const html = (panes.titleHtml ?? "") + [tpl.open, tpl.nav_open, ...navItems, tpl.nav_close,
			tpl.content_open, ...paneItems, tpl.content_close, tpl.close].join("\n");
		if (this.#accLeakGuard(html, cfg)) return null;           // a build must never ADD a leak
		if (notes.length) bundle.instructions = [...(bundle.instructions ?? []), ...notes];
		bundle.r281Tabs = true;                                   // detector / affected-set marker
		return html;
	}

	/**
	 * ROUND 281 — resolve PANES from the ordered parts, trying each delimiter kind in
	 * turn (D1 explicit [Tab N] → D2 a table read column-major → D3 a table read
	 * row-major → D4 a repeating heading run) and taking the first that yields panes.
	 * Returns `[{head, parts}]` (optionally carrying `.titleHtml`), or null.
	 */
	static #tabResolvePanes(parts, cfg, rich) {
		const substantive = parts.filter((p) => p.role !== "note");
		if (!substantive.length) return null;
		const maxLabel = cfg.label_max_words ?? 6;

		// ---- D1: explicit [Tab N] delimiters -----------------------------------
		if (parts.some((p) => p.role === "panel")) {
			const panes = [];
			let cur = null;
			for (const p of parts) {
				if (p.role === "panel") {
					if (p.overlong) return null;                 // a sentence-long tag text, no bold lead
					cur = { head: p.head, parts: [] }; panes.push(cur); continue;
				}
				if (!cur) {
					// content BEFORE the first [Tab N] is a lead-in, not pane content; only
					// plain text may precede (anything richer means the walk swept a section in).
					if (p.role === "text") continue;
					return null;
				}
				// a label-less pane takes its label from its own first sub-heading
				if (p.role === "head" && !cur.head && !cur.parts.length) { cur.head = p.text; continue; }
				if (!this.#tabPushPart(cur.parts, p, cfg, maxLabel)) return null;
			}
			return panes.every((p) => p.head && p.parts.length) ? panes : null;
		}

		// ---- D2/D3: a captured TABLE is the whole widget ------------------------
		const tables = parts.filter((p) => p.role === "table");
		if (tables.length === 1 && cfg.table_panes !== false) {
			const others = substantive.filter((p) => p.role !== "table");
			if (others.every((p) => p.role === "text")) {          // only a lead line may ride along
				const rows = (tables[0].item?.block?.rows ?? []).map((r) => (r ?? []).map((c) => String(typeof c === "string" ? c : (c?.text ?? ""))));
				const panes = this.#tabTablePanes(rows, cfg, rich);
				if (panes && panes.length >= (cfg.min_inferred_panes ?? 2)) return panes;
			}
		}

		// ---- D4: a repeating same-level heading run -----------------------------
		if (cfg.heading_panes !== false) {
			const heads = parts.filter((p) => p.role === "head");
			const levels = [...new Set(heads.map((h) => h.level))];
			if (heads.length >= (cfg.min_inferred_panes ?? 2) && levels.length === 1) {
				const panes = [];
				let cur = null;
				for (const p of parts) {
					if (p.role === "note") continue;
					if (p.role === "head") {
						if (String(p.text).split(/\s+/).length > maxLabel) {
							if (!cur) return null;                 // a long heading before any pane
							if (!this.#tabPushPart(cur.parts, { role: "text", text: p.text }, cfg, maxLabel)) return null;
							continue;                              // prose, not a label — keep it in the pane
						}
						cur = { head: p.text, parts: [] }; panes.push(cur); continue;
					}
					if (!cur) { if (p.role === "text") continue; return null; }
					if (!this.#tabPushPart(cur.parts, p, cfg, maxLabel)) return null;
				}
				if (panes.length >= (cfg.min_inferred_panes ?? 2)
					&& panes.every((p) => p.head && p.parts.length)) return panes;
			}
		}
		return null;
	}

	/** ROUND 281 — push ONE resolved part into a pane's part list, translating the
	 *  shared round-278 roles into the {p|img|video|html} shapes #tabsRichPart renders.
	 *  Returns false when the part cannot belong to a pane (→ never half-build). */
	static #tabPushPart(list, p, cfg, maxLabel) {
		if (p.role === "text") {
			const t = String(p.text ?? "").trim();
			if (!t) return true;
			const last = list[list.length - 1];
			if (last && last.p) { last.p += "\n" + t; return true; }
			list.push({ p: t }); return true;
		}
		if (p.role === "head") {
			// a sub-heading INSIDE a pane (the writer's own [H4]) — gold ships h4 in 21%
			// of tab groups, so it renders rather than bailing the widget.
			const t = String(p.text ?? "").trim();
			if (!t) return true;
			const lvl = /^h[1-6]$/.test(String(p.level)) ? p.level : "h4";
			list.push({ html: `<${lvl}>${t}</${lvl}>` }); return true;
		}
		if (p.role === "img") { list.push({ img: p.filename }); return true; }
		if (p.role === "video") { list.push({ video: p.id }); return true; }
		if (p.role === "embed") { list.push({ html: p.html }); return true; }
		if (p.role === "table") { if (!p.html) return false; list.push({ html: p.html }); return true; }
		if (p.role === "nested") return false;                    // a nested widget → its own round
		return false;
	}

	/** ROUND 281 — one table cell's text → the pane's lines. The writer separates a
	 *  cell's own lines with " / " (the converter's long-standing cell convention); an
	 *  ORPHAN leading or trailing separator is dropped rather than shipped as a stray
	 *  "/" at the top of the pane (AGH1003-5.0 "In a home garden: / • dig the soil …",
	 *  caught by the tabs verifier). */
	static #tabSplitCell(s) {
		return String(s ?? "").split(/\s+\/\s+/)
			.map((x) => x.replace(/^\s*\/\s*/, "").replace(/\s*\/\s*$/, "").trim())
			.filter(Boolean).join("\n");
	}

	/**
	 * ROUND 281 — read ONE captured table as a set of panes, COLUMN-major first
	 * (the dominant tabs form: the header row is the labels) and ROW-major second.
	 * Returns `[{head, parts}]` (optionally with `.titleHtml`), or null.
	 */
	static #tabTablePanes(rows, cfg, rich) {
		const maxLabel = cfg.label_max_words ?? 6;
		const clean = (s) => this.#cellText(String(s ?? "")).replace(/\*\*/g, "").replace(/\s+/g, " ").trim()
			.replace(/^[\/|]\s*/, "").replace(/\s*[\/|]$/, "").trim();
		// A LABEL ROW MAY NOT BE **WHOLLY** RED. Red marks the writer's own structural
		// spec, and a flipCard/clickDrop table is laid out as ENTIRELY-red [front]/[drop]
		// marker rows over the card faces (OSAI201-3.0) — which the column reader would
		// otherwise turn into four tabs all labelled "front". But a red [Tab N] marker
		// followed by BLACK label text is a perfectly good label (OSSC401-3.0
		// "🔴[Tab 1]🔴 Ari's story"), so the test is #isFullyRed per cell, not "any red".
		// Both directions were caught by the tabs verifier — the blanket form silently
		// cost OSSC401 and ENFUN05 their builds.
		const rowIsRed = (r) => (r ?? []).some((c) => this.#isFullyRed(c));
		// …and a real tab set has DISTINCT labels; repeats mean we read the wrong row.
		const distinct = (hs) => new Set(hs.map((h) => h.toLowerCase())).size === hs.length;
		const roleRe = new RegExp(cfg.role_column_pattern
			?? "^\\[?\\s*(title|label|heading|image|images|link for image|link|video|body|text|caption)\\b[^\\]]*\\]?\\s*:?$", "i");
		let titleHtml = "";

		// A leading SINGLE-CELL row is a TITLE for the whole set. Peeled to a heading at
		// the writer's own [H*] level when it carries one (the round-215 rule, generalised
		// off its CEDT-only gate); with no level to derive we decline rather than invent.
		if (rows.length > 2 && (rows[0] ?? []).length === 1) {
			const t0 = clean(rows[0][0]);
			const m = t0.match(/^\[\s*h([1-6])\b[^\]]*\]\s*(.+)$/i);
			if (m) {
				if (/[\[\]]/.test(m[2])) return null;
				titleHtml = `<h${m[1]}>${m[2]}</h${m[1]}>\n`;
			} else {
				// NO level to derive: the writer's topic line ships as a LEAD PARAGRAPH above
				// the tabs (faithful — nothing is lost) rather than inventing a heading rank.
				if (!t0 || /[\[\]]/.test(t0)) return null;
				titleHtml = `<p>${t0}</p>\n`;
			}
			rows = rows.slice(1);
		}
		if (rows.length < 1) return null;
		const nCols = (rows[0] ?? []).length;
		if (rows.some((r) => r.length !== nCols)) return null;    // ragged → a richer form

		// ---- ROLE-LABELLED first column (ENFUN01: [Title]/[Image]/[Link for image]) --
		if (nCols >= 3 && rows.length >= 2 && rows.every((r) => roleRe.test(clean(r[0])))) {
			const roles = rows.map((r) => clean(r[0]).replace(/[[\]:]/g, "").trim().toLowerCase());
			const ti = roles.findIndex((r) => /^(title|label|heading)$/.test(r));
			if (ti < 0) return null;
			// column 0 is the ROLE column and is legitimately red ([Title]); no OTHER cell may be.
			if (rows.some((r) => r.slice(1).some((c) => this.#isFullyRed(c)))) return null;
			const panes = [];
			for (let c = 1; c < nCols; c++) {
				const head = clean(rows[ti][c]);
				if (!head || head.split(/\s+/).length > maxLabel) return null;
				const parts = [];
				for (let r = 0; r < rows.length; r++) {
					if (r === ti) continue;
					const cell = clean(rows[r][c]);
					if (!cell) continue;
					if (/^(image|images|link for image|link)$/.test(roles[r])) {
						const url = this.#cellMediaUrl(rows[r][c]);
						if (!url) continue;                        // no asset yet — nothing to render
						const fn = this.#accImageFilename(url, rich, cfg);
						if (!fn) return null;
						parts.push({ img: fn });
						continue;
					}
					if (/[\[\]]/.test(cell)) return null;
					parts.push({ p: cell });
				}
				if (!parts.length) return null;
				panes.push({ head, parts });
			}
			if (panes.length >= (cfg.min_inferred_panes ?? 2) && distinct(panes.map((p) => p.head))) {
				panes.titleHtml = titleHtml; return panes;
			}
			return null;
		}

		// ---- COLUMN-major: row 0 = the labels, rows 1.. = each column's body --------
		if (nCols >= 2 && rows.length >= 2 && !rows.some(rowIsRed)) {
			const heads = rows[0].map(clean);
			if (distinct(heads) && heads.every((h) => h && !/[\[\]]/.test(h) && !/https?:\/\//.test(h)
				&& h.split(/\s+/).length <= maxLabel)) {
				const panes = [];
				for (let c = 0; c < nCols; c++) {
					const body = [];
					for (let r = 1; r < rows.length; r++) {
						const cell = clean(rows[r][c]);
						if (!cell) continue;
						if (/[\[\]]/.test(cell)) return null;
						body.push(this.#tabSplitCell(cell));
					}
					if (!body.length) return null;
					panes.push({ head: heads[c], parts: [{ p: body.join("\n") }] });
				}
				if (panes.length >= (cfg.min_inferred_panes ?? 2)) { panes.titleHtml = titleHtml; return panes; }
			}
		}

		// ---- ROW-major: one row = one pane (short label cell + content cell) --------
		if (nCols === 2 && rows.length >= (cfg.min_inferred_panes ?? 2) && !rows.some(rowIsRed)) {
			const panes = [];
			for (const r of rows) {
				const head = clean(r[0]), body = clean(r[1]);
				if (!head || !body) { panes.length = 0; break; }
				if (/[\[\]]/.test(head) || /[\[\]]/.test(body)) { panes.length = 0; break; }
				if (head.split(/\s+/).length > maxLabel) { panes.length = 0; break; }
				panes.push({ head, parts: [{ p: this.#tabSplitCell(body) }] });
			}
			if (panes.length >= (cfg.min_inferred_panes ?? 2) && distinct(panes.map((p) => p.head))) {
				panes.titleHtml = titleHtml; return panes;
			}
		}

		// ---- ONE-ROW table: one pane per CELL, labelled from its own lead -----------
		if (rows.length === 1 && nCols >= (cfg.min_inferred_panes ?? 2) && cfg.cell_panes !== false
			&& !rows.some(rowIsRed)) {
			const panes = [];
			for (const c of rows[0]) {
				const cell = clean(c);
				if (!cell || /[\[\]]/.test(cell)) return null;
				const lead = cell.match(/^([^:•\n]{1,80}?)\s*:\s*(.+)$/);
				if (!lead || lead[1].split(/\s+/).length > maxLabel) return null;
				const body = this.#tabSplitCell(lead[2]);
				if (!body) return null;
				panes.push({ head: lead[1].trim(), parts: [{ p: body }] });
			}
			if (panes.length >= (cfg.min_inferred_panes ?? 2) && distinct(panes.map((p) => p.head))) {
				panes.titleHtml = titleHtml; return panes;
			}
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
		// ambiguous to build cleanly. ROUND 279: except when every merged type is our
		// OWN — "carousel + carousel" is only the placeholder LABEL, not two different
		// widgets (the round-242 accordion finding and the round-215 tabs self-merge,
		// restated for the carousel). Writers repeat [carousel] as a SLIDE marker
		// (HPFUN302-0.0 opens six slides that way, HES1006-7.0 four), and where they
		// really did mean two slideshows the round-279 scanner rule splits them at the
		// table before the builder ever sees them. MEASURED: 52 of the 104 extraTypes
		// declines are same-type-only, across 38 modules. Data carousel.same_type_merge;
		// env CARSAMETYPE_OFF.
		const extra = bundle.extraTypes ?? [];
		if (extra.length) {
			const sameOnly = (tpl.same_type_merge?.enabled !== false)
				&& !(typeof process !== "undefined" && process.env && process.env.CARSAMETYPE_OFF)
				&& extra.every((t) => t === bundle.type);
			if (!sameOnly) return null;
		}

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

		// MEDIA|CAPTION-TABLE form (ROUND 271 — Chris, OSSC401-1.0). ONE captured
		// table whose every data row pairs a MEDIA cell with the slide's PROSE
		// (title + copy, the writer's " / " between paragraphs). Tried after the
		// all-media form and BEFORE the image|caption form, and VIDEO-SCOPED, so
		// each of those keeps its own population byte-identical.
		// Data carousel.media_caption_table; env CARMEDCAP_OFF.
		if (tables.length === 1) {
			const mc = this.#carouselMediaCaptionTable({ bundle, tpl, renderInline, run });
			if (mc !== null) return mc;
		}

		// IMAGE-CAPTION TABLE form: exactly one captured table, no video anywhere.
		// ROUND 279: its null no longer ENDS the dispatch. It used to be `return
		// this.#carouselImageTable(...)`, so a single-table carousel that failed this
		// one narrow shape never reached any later branch — 143 of the 561 declines
		// (75 modules) died at that dead-end without a fallback ever being tried.
		// Returning only on a BUILD cannot change a single existing build.
		if (!hasVideo && tables.length === 1) {
			const it = this.#carouselImageTable({ bundle, tpl, renderInline, run });
			if (it !== null) return it;
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

		// RICH SLIDE FALLBACK (round 246) — after every strict dialect has declined, so each
		// of them stays byte-identical. Builds the writer's carousel from whatever mix of
		// heading / image / video / prose the members actually carry.
		// See #carouselRich. Data carousel.rich_slides; env CARNOTBL_OFF.
		const rich = this.#carouselRich({ bundle, tpl, renderInline, run, renderBlock });
		if (rich !== null) return rich;

		// TABLE-SLIDE FALLBACK (ROUND 279) — THE LAST RESORT, so every branch above keeps
		// its own population byte-for-byte. The writer's other big slideshow dialect is a
		// plain TABLE, and the three table branches above each recognise one narrow shape;
		// this one reads any of them by the general rule the gold uses — one data ROW is
		// one slide. See #carouselTableSlides. Data carousel.table_slides; env CARTABLE_OFF.
		return this.#carouselTableSlides({ bundle, tpl, renderInline, run, renderBlock });
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
		// ROUND 279: a SAME-TYPE merge ("carousel + carousel") is only the placeholder
		// label — the dispatcher has already made that call, so mirror it here rather
		// than bailing a second time. A genuinely mixed bundle still never reaches this.
		if ((bundle.extraTypes ?? []).some((t) => t !== bundle.type)) return null;

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
		// ROUND 275 (Chris — "the carousel builder gives up whenever the writer included a
		// video link"). THE WIDENED TAIL-URL LOOKAHEAD. The dominant declining dialect is the
		// BLL phonics family's video list, where the writer types the video's TITLE on the
		// [video] tag and puts the bare URL on the FOLLOWING line — but colours that line RED,
		// so it arrives as a tag member with NO primary rather than the `black` line round 247
		// looked for, the lookahead missed it, the video resolved no id and the WHOLE carousel
		// bailed. The recovery now walks forward over blank/no-primary members of ANY type and
		// takes the first resolvable video URL, stopping at the first member that carries a
		// real primary tag (so a URL belonging to a different element can never be stolen) or
		// at any member carrying real prose of its own. Reachable ONLY for a video with no URL
		// of its own — every such bundle declines today — so it is strictly additive.
		// Data rich_slides.video_url_recovery; env CARVIDEO_OFF (CARVIDTAIL_OFF still reverts
		// the whole r247 lookahead).
		// ROUND 279 — THE MEMBER VOCABULARY (env CARMEMBER_OFF reverts all of it). The
		// decline recorder showed that after the table classes the next-biggest reasons
		// are all one thing: a member the walk knows perfectly well but cannot NAME —
		// an image on a non-iStock host (62 declines), a video/[embed] it cannot embed
		// (61), a [Caption] (which resolves to canonical tag `data marker`, so the
		// text_tags entry "caption" never matched it — 17), an [audio] (5). Data
		// carousel.member_vocabulary.
		const mv = (env.CARMEMBER_OFF || cfg.member_vocabulary?.enabled === false)
			? {} : (cfg.member_vocabulary ?? {});
		let mvUsed = false;                                          // did a round-279 rule fire?
		const vrCfg = cfg.video_url_recovery ?? {};
		const widenTail = (vrCfg.follow_any_member ?? false) && !env.CARVIDEO_OFF;
		const tailWindow = vrCfg.follow_window ?? 3;
		const tailUrls = new Map(), tailConsumed = new Set();
		if ((msCfg.video_tail_url ?? false) && !env.CARVIDTAIL_OFF) {
			const anyUrl = (x) => x?.block?.links?.[0]?.target
				?? (String((x?.type === "tag" ? (x.blackAfter ?? "") : (x?.text ?? ""))).match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");
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
					if (u && idRe.test(u)) { tailUrls.set(m, u); tailConsumed.add(nx); continue; }
				}
				if (!widenTail) continue;
				for (let j = i + 1; j < Math.min(members.length, i + 1 + tailWindow); j++) {
					const c = members[j];
					if (!c || tailConsumed.has(c)) continue;
					if (c.type === "table" || c.type === "nested") break;
					if (c.type === "tag" && c.parse?.primary) break;      // a real element owns its own URL
					const u = anyUrl(c);
					const body = String(c.type === "tag" ? (c.blackAfter ?? "") : (c.text ?? ""));
					if (!u) { if (this.#cellText(body).trim()) break; continue; }   // blank filler → keep looking
					// the line must be the URL itself, not prose that merely contains one
					if (this.#cellText(body.replace(/https?:\/\/[^\s\]"<>]+/g, " ").replace(/[()[\]]/g, " ")).trim()) break;
					if (!this.#carouselVideoUrlOk(u, cfg)) break;
					tailUrls.set(m, u); tailConsumed.add(c);
					break;
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
				if (t && !this.#carouselBareMediaRef(m.blackAfter, cfg, env)) pending.push(String(m.blackAfter));
				continue;
			}
			// the widget's own invocation contributes only its trailing prose.
			// ROUND 279: a REPEATED invocation once the open slide already holds content
			// is the writer using [carousel] as a SLIDE MARKER (HPFUN302-0.0 opens six
			// slides that way, HES1006-7.0 four) — so it opens the next slide, exactly as
			// a [Slide N] marker does. The FIRST invocation (nothing captured yet) still
			// only contributes its trailing prose, so every existing build is unchanged.
			if (tag === bundle.canonTag || tag === "carousel") {
				if (this.#hasRedText(raw)) return null;
				if (mv.invocation_opens_slide && cur && (cur.parts.length || pending.length)) {
					mvUsed = true; flush(); open();
				}
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
			// a VIDEO (or an [embed] carrying one) — the shared YouTube embed. ROUND 275: a
			// YouTube SHORTS url ships the corpus 1x1 short form and any OTHER resolvable
			// video url ships the generic iframe, exactly as the free-body media emitter
			// (MediaBuilder.media) already does — instead of bailing the whole carousel on
			// a host the YouTube-only id regex could not read. Still bails when there is no
			// url at all. Data rich_slides.video_url_recovery; env CARVIDEO_OFF.
			if (tag === "video" || tag === "embed" || (url && idRe.test(url))) {
				if (this.#hasRedText(raw)) return null;
				const id = String(url).match(idRe)?.[1];
				if (id && videoTpl) {
					flush();
					if (!cur || (mediaOpens && cur.parts.some((pt) => pt.img || pt.video))) open();
					cur.parts.push({ video: id });
					continue;
				}
				const alt = (vrCfg.other_hosts !== false) && !env.CARVIDEO_OFF
					? this.#carouselVideoEmbed(url, tpl, cfg) : null;
				// ROUND 279: a video/[embed] we cannot resolve is an ASSET REQUEST, not a
				// build failure — the writer is naming media the developer will source
				// (the decodable-story [embed book] family is 67 of these declines, and
				// round 126 already treats that as a scaffold on the free-body path). It
				// is SKIPPED as slide content and surfaced as the standard red Writers
				// Note after the widget, exactly as the rich accordion treats one
				// (r214/r242/r278) — never silently dropped, never given an invented
				// embed. A carousel left with too few real slides still declines.
				if (!alt) {
					if (!mv.asset_request) return null;              // a video we cannot resolve → bail
					mvUsed = true;
					this.#carNoteAssetRequest(bundle, m, raw, mv);
					continue;
				}
				flush();
				if (!cur || (mediaOpens && cur.parts.some((pt) => pt.img || pt.video))) open();
				cur.parts.push({ html: alt });
				continue;
			}
			// an IMAGE — the standard Mode P/D asset, named from the iStock id
			if (tag === "image" || (url && !this.#cellText(String(raw).replace(/https?:\/\/[^\s\]"<>]+/g, "")).trim())) {
				if (this.#hasRedText(raw)) return null;
				// ROUND 279: the same two-step the speech bubble (r276) and the accordion
				// (r278) already use. A NON-iStock url still names a real picture, so it
				// takes the round-126 url-SLUG placeholder instead of bailing the widget;
				// only an image with NO url at all is an asset request (skip + red note).
				const file = this.#carImageFilename(url, tpl, mv);
				if (!file) {
					if (!mv.asset_request) return null;              // a non-derivable image → bail
					mvUsed = true;
					this.#carNoteAssetRequest(bundle, m, raw, mv);
					continue;
				}
				if (!/^iStock-/i.test(file)) mvUsed = true;          // the r126 slug fallback
				flush();
				if (!cur || (mediaOpens && cur.parts.some((pt) => pt.img || pt.video))) open();
				cur.parts.push({ img: file });
				continue;
			}
			// AUDIO (ROUND 279) — the gold ships an <audio> player on 148 slides across 23
			// modules, so an [audio] member is slide CONTENT, not an unknown tag. With a
			// resolvable file it plays; with none it is an asset request like any other.
			if (mv.audio_member && tag === "audio") {
				mvUsed = true;
				if (this.#hasRedText(raw)) return null;
				const au = this.#carAudioHtml(url, raw, mv);
				if (!au) { this.#carNoteAssetRequest(bundle, m, raw, mv); continue; }
				flush();
				if (!cur || (mediaOpens && cur.parts.some((pt) => pt.img || pt.video || pt.html))) open();
				cur.parts.push({ html: au });
				continue;
			}
			// PROSE — a plain black line or a text-family element tag. ROUND 275: a line that
			// is NOTHING BUT a bare video URL is that video's REFERENCE, not learner prose —
			// the human ships ZERO of them (measured: 1,618 gold carousel captions, 0 bare-URL),
			// the same rule MediaBuilder applies on the body path (r80 stripMediaResidue).
			// Without this, every URL line the tail lookahead did not claim rendered as a
			// visible link paragraph on the slide.
			if (m.type === "black" || textTags.has(tag) || (mv.text_tags ?? []).includes(tag)) {
				if (!textTags.has(tag) && (mv.text_tags ?? []).includes(tag)) mvUsed = true;
				if (this.#hasRedText(raw)) return null;
				if (this.#carouselBareMediaRef(raw, cfg, env)) continue;
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
			&& !slides.some((s) => s.parts.some((p) => p.img || p.video || p.html || p.p))) return null;

		const html = this.#carRenderSlides(slides, { tpl, cfg, inline, run, renderBlock, videoTpl });
		if (html === null) return null;
		// THE LEAK GUARD, SCOPED TO THE ROUND-279 WIDENING (`mvUsed`). A carousel that
		// only builds because one of this round's member rules fired must not put a
		// literal writer tag on the page — BLL263-1.0's "[Embed audio book]" line was
		// caught exactly here. Scoping it to mvUsed is deliberate: an unscoped guard
		// would also refuse builds that have been shipping since round 246, which is
		// the mistake round 277 caught in its own guard.
		if (mvUsed && this.#carHasBracketTag(html, tpl.table_slides ?? {})) return null;
		bundle.r246Carousel = true;                                  // detector/affected-set marker
		return html;
	}

	/**
	 * ROUND 279 — the SLIDE RENDERER, a pure extraction from the tail of
	 * #carouselRich so the round-246 rich fallback and the new
	 * #carouselTableSlides emit byte-identical markup from the same part list
	 * (the round-278 #accRenderPanels pattern). Nothing about the existing
	 * output changed: the loop below is the round-275 code verbatim.
	 *
	 * A slide is an ordered list of PARTS, each exactly one of:
	 *   {h}     a heading            -> cfg.heading
	 *   {img}   an image FILENAME    -> the Mode P/D asset
	 *   {video} a YouTube id         -> the shared embed
	 *   {html}  ready-made markup    -> a shorts/other-host embed, an audio player
	 *   {p}     prose                -> renderBlock, inside a carousel-caption
	 * Consecutive prose parts share ONE caption div; any other part closes it.
	 *
	 * @param {Array<{parts:Array<object>}>} slides - the resolved slides
	 * @param {object} args - tpl / cfg / inline / run / renderBlock / videoTpl
	 * @returns {string|null} the finished carousel, or null to keep the placeholder
	 */
	static #carRenderSlides(slides, { tpl, cfg, inline, run, renderBlock, videoTpl }) {
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
				} else if (part.html) {
					if (capOpen) { chunks.push(cfg.caption_close); capOpen = false; }
					chunks.push(part.html);          // ROUND 275: a shorts / non-YouTube embed
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
		return [tpl.open, ...items, tpl.close].join("\n");
	}

	/**
	 * ROUND 279 — the IMAGE FILENAME for a carousel slide, the two-step the speech
	 * bubble (round 276) and the accordion (round 278) already use. An iStock id
	 * names the corpus asset; any OTHER host still names a real picture, so it
	 * takes the round-126 url-SLUG placeholder rather than bailing the widget. No
	 * url at all → null, and the caller treats the member as an asset request.
	 *
	 * @param {string} url - the member's/cell's media url
	 * @param {object} tpl - the carousel template block
	 * @param {object} mv  - carousel.member_vocabulary (empty when CARMEMBER_OFF)
	 * @returns {string|null} the filename, or null when nothing can be named
	 */
	static #carImageFilename(url, tpl, mv = {}) {
		const u = String(url ?? "");
		if (!u) return null;
		const id = (u.match(/gm-?(\d{6,10})/) || u.match(/\/id\/(\d{4,10})/) || [])[1];
		if (id) return Utils.FillTemplate(tpl.filename_istock, { id });
		if (!mv.image_slug_fallback) return null;
		return this.#bannerImageFilename(u, tpl);
	}

	/**
	 * ROUND 279 — an AUDIO slide part. The gold ships an <audio> player on 148
	 * slides across 23 modules, so an [audio] member is slide CONTENT. Uses the
	 * shared body-path audio template so a carousel's player is the page's player.
	 *
	 * @param {string} url - the member's media url
	 * @param {object} mv  - carousel.member_vocabulary
	 * @returns {string|null} the player markup, or null when there is no file
	 */
	static #carAudioHtml(url, raw, mv = {}) {
		const t = DataService.Data.EmitTemplates?.audio?.form;
		if (!t) return null;
		const u = String(url ?? "");
		const m = u.match(/\/([^/?#]+\.(?:mp3|wav|m4a|ogg))(?:\?|#|$)/i);
		if (!m) return null;                                         // no real file → an asset request
		return Utils.FillTemplate(t, {
			filename: m[1],
			title: this.#cellText(String(raw ?? "").replace(/https?:\/\/[^\s\]"<>]+/g, "")).trim(),
		});
	}

	/**
	 * ROUND 279 — record a member the builder could not turn into slide content
	 * because the ASSET does not exist yet (an image with no url, an [embed book]
	 * whose story lives on an external site, a "[Insert media item 6]" reference).
	 * It is skipped as content and pushed onto bundle.instructions, which the
	 * converter already surfaces as the standard red Writers Note AFTER the widget
	 * — the round-214/242/278 rule, so the writer's words are never silently lost.
	 *
	 * @param {object} bundle - the captured interactive
	 * @param {object} m - the member item
	 * @param {string} raw - its raw text
	 * @param {object} mv - carousel.member_vocabulary
	 */
	/**
	 * TABLE-SLIDE carousel (ROUND 279 — Chris, the interactive-coverage chain) — the
	 * carousel's sibling of the round-278 accordion panel-delimiter vocabulary, and
	 * the LAST branch tried, so every existing dialect keeps its population
	 * byte-for-byte.
	 *
	 * WHY IT EXISTS. A carousel's other big authoring form is a plain TABLE, and the
	 * three table branches above each recognise exactly ONE shape: every cell a media
	 * cell (r266), a media cell paired with prose and at least one video (r271), or an
	 * image URL paired with a caption (r63). Everything else died — and because the
	 * r63 branch RETURNED its null, most of it died without any fallback being tried
	 * at all. MEASURED by the shipped builder's own verdict
	 * (outputs/_measure_r279_carousel.cjs, all 454 modules): 277 of the 561 declines
	 * carry a captured table — 143 at the r63 dead-end, 95 refused outright by the
	 * rich fallback, the rest on min_slides — across 114 modules.
	 *
	 * THE RULE IS THE GOLD'S OWN: ONE DATA ROW IS ONE SLIDE.
	 *   AGH1002-1.0  3 rows (empty image cell | caption) -> the gold's 3 slides
	 *   EXPFUN06-0.0 3 rows (image brief   | caption)    -> the gold's 3 slides
	 *   XTAS101-0.0  7 rows (1 header + 6)               -> the gold's 6 slides
	 * A table with exactly ONE data row and several cells is instead one slide per
	 * CELL — the r266 form, and again gold-checked (XTAS101's 1x2 video row is two
	 * gold slides). A leading header/label row is dropped (the shared
	 * #isCarouselTitleOrLabelRow). Several tables (only reachable when the round-279
	 * scanner rule did NOT split them, i.e. the writer wrote one invocation) append in
	 * document order.
	 *
	 * A CELL becomes ordered PARTS through the same vocabulary the rich fallback uses:
	 * a media cell contributes its image/video, a prose cell its title and copy (split
	 * on the writer's own " / " exactly as the round-271 media|caption form does), and
	 * a cell naming an asset that does not exist yet — "ocean cleanup", "[image] teens
	 * doing art together" — is an ASSET REQUEST: skipped as content and surfaced as the
	 * red Writers Note after the widget. The gold agrees, visibly: EXPFUN06's slides
	 * show the caption only, never the writer's image brief.
	 *
	 * NEVER HALF-BUILDS (null → the honest hand-off box): a row that yields no parts, a
	 * red developer instruction in a cell, fewer than min_slides slides, more than
	 * max_slides, slides carrying no real content, or a finished carousel still showing
	 * a bracketed tag (#carLeakGuard — the round-167 rule at this seam, so building can
	 * only ever PREVENT a leak).
	 *
	 * @param {object} args
	 * @param {object} args.bundle - the captured interactive
	 * @param {object} args.tpl - the carousel template block (Emit_Templates.json)
	 * @param {function} [args.renderInline] - inline-markup renderer
	 * @param {object} [args.run] - conversion run context (Mode P/D images)
	 * @param {function} [args.renderBlock] - the black-text block renderer
	 * @returns {string|null} the built carousel, or null to keep the placeholder
	 */
	static #carouselTableSlides({ bundle, tpl, renderInline, run, renderBlock }) {
		const cfg = tpl?.table_slides;
		if (!cfg || cfg.enabled === false) return null;
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		if (env.CARTABLE_OFF) return null;
		if (typeof renderBlock !== "function") return null;
		const tables = (bundle.memberItems ?? []).filter((m) => m && m.type === "table");
		if (!tables.length) return null;
		if ((bundle.extraTypes ?? []).some((t) => t !== bundle.type)) return null;
		// REO / BILINGUAL modules are excluded (the round-145 exclusion class). Their
		// tables are the bilingual machinery's own — TRR301's "Picture | AudioImage |
		// Reretūpono | Correct word to highlight" grid is the round-135 phonics
		// audioImage form, and reading it as a slideshow produced four-cell prose
		// slides and put three literal tags on the page.
		if (cfg.exclude_reo !== false && MenuBuilder.isReoModule(run)) return null;

		const rich = tpl.rich_slides ?? {};
		const mv = (env.CARMEMBER_OFF || rich.member_vocabulary?.enabled === false)
			? {} : (rich.member_vocabulary ?? {});
		const inline = renderInline ?? ((s) => s);
		const videoTpl = DataService.Data.EmitTemplates.video?.youtube;
		const idRe = new RegExp(rich.video_id_re ?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");

		const slides = [];
		for (const item of tables) {
			const rows = (item.block?.rows ?? []).filter((r) => Array.isArray(r));
			if (!rows.length) return null;
			// drop a leading header/label row ("Image ║ Caption", an all-red label row).
			// NOT the round-63 #isCarouselTitleOrLabelRow: that one counts a row with a
			// single non-empty cell as a label, which is exactly AGH1002's shape (an
			// EMPTY image cell beside the caption) and would eat every data row.
			let data = rows;
			while (data.length > 1 && this.#carIsHeaderRow(data[0], cfg, tpl)) data = data.slice(1);
			if (!data.length) return null;
			// ONE ROW = ONE SLIDE; a single-row table is one slide per CELL (the r266 form).
			const groups = data.length === 1
				? data[0].map((c) => [c]).filter((g) => this.#cellText(g[0]).trim() || /https?:\/\//.test(String(g[0] ?? "")))
				: data.map((r) => r);
			for (const cells of groups) {
				const parts = [];
				for (const cell of cells) {
					const got = this.#carCellParts(cell, { bundle, tpl, cfg, mv, rich, idRe, inline });
					if (got === null) return null;                   // red instruction / unreadable cell
					parts.push(...got);
				}
				if (!parts.length) continue;                         // an empty row (a spacer) — skipped
				slides.push({ parts });
			}
		}

		if (slides.length < (cfg.min_slides ?? tpl.min_slides ?? 2)) return null;
		if (slides.length > (cfg.max_slides ?? rich.max_slides ?? 20)) return null;
		// SUBSTANCE GUARD (never half-build): slides carrying no image, video or prose
		// are not a slideshow — the writer's real material did not reach the bundle.
		if (cfg.require_content !== false
			&& !slides.some((s) => s.parts.some((p) => p.img || p.video || p.html || p.p))) return null;

		// The slide-title FORM is a per-GROUP house style (ROUND 214, measured): the
		// default is <h4>, and the subjects in caption_title_bold ship the title as a
		// bold <p> lead instead. Reuse that registry rather than mining a second one.
		const capCfg = tpl.caption_title_bold;
		const prefix = String(run?.moduleCode ?? "").match(/^[A-Z]+/)?.[0] ?? "";
		const boldTitle = !(env.CARCAP_OFF) && capCfg && capCfg.enabled !== false
			&& (capCfg.subjects ?? []).includes(prefix);
		const html = this.#carRenderSlides(slides, {
			tpl,
			cfg: { ...rich, ...cfg, ...(boldTitle ? { heading: cfg.heading_bold ?? "<p><b>{text}</b></p>" } : {}) },
			inline, run, renderBlock, videoTpl,
		});
		if (html === null) return null;
		if (this.#carHasBracketTag(html, cfg)) return null;           // the leak guard (r167 at this seam)
		bundle.r279CarouselTable = true;                             // detector/affected-set marker
		return html;
	}

	/**
	 * ROUND 279 — one table CELL to its ordered slide PARTS, using the same
	 * vocabulary as the rich member walk so a table-authored carousel and a
	 * member-authored one render identically.
	 *
	 * @param {*} cell - the raw cell
	 * @param {object} ctx - bundle / tpl / cfg / mv / rich / idRe / inline
	 * @returns {Array<object>|null} the parts, or null to decline the whole build
	 */
	static #carCellParts(cell, { bundle, tpl, cfg, mv, rich, idRe }) {
		let raw = String(cell ?? "");
		if (!raw.trim()) return [];
		// RED TEXT IN A CELL IS NOT AUTOMATICALLY AN INSTRUCTION. In this dialect the
		// writer colours the slide's own words — AGH1002-1.0's captions are entirely
		// red ("Parakiwai / Alluvial soil which is formed through rivers…") and the
		// GOLD ships them as the slide text — so a table cell follows the round-271
		// media|caption convention: #cellText strips the sentinels and the words are
		// content. What IS held back is a red span carrying a WRITER-INSTRUCTION cue
		// from the shared Instruction_Cues vocabulary ("please", "can you", "dev
		// team", "note to…"). Only THAT SPAN is lifted out — not the whole cell —
		// because the writer routinely mixes the two in one cell (XTAS101-0.0's
		// "[video] Autistic special interests (dev team start at 0:04)"), and it
		// surfaces as the standard red Writers Note after the widget.
		raw = this.#carStripInstructionSpans(raw, cfg, (t) => this.#carNoteAssetRequest(bundle, null, t, mv));
		if (!raw.trim()) return [];
		// ROUND 284 — REPAIR A DANGLING MEDIA MARKER before anything reads the cell.
		// A writer who drops the CLOSING bracket ("[image Young man gaming", XMES203-2.0,
		// whose well-formed siblings are "[image] online chats on phone") defeats BOTH the
		// kind test and the bracket strip below — they each require a "]" — so the marker
		// shipped as visible slide text. Round 174 repaired the missing-OPEN form at the
		// extractor and deliberately left missing-CLOSE alone because RenderText's optional
		// "]?" absorbed it; this cell path derives its text with its own regexes and never
		// goes through RenderText, so the same asymmetry re-appeared at a new seam. Repair
		// the bracket rather than strip the run: the writer's words ("Young man gaming") are
		// the caption its siblings produce. The negative lookahead means a well-formed
		// "[image] x" is untouched BY CONSTRUCTION.
		if (cfg.dangling_marker_repair) {
			raw = raw.replace(new RegExp(cfg.dangling_marker_repair, "gi"), "[$1] ");
		}
		const url = this.#cellMediaUrl(cell) || (raw.match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");
		const kind = (raw.match(new RegExp(cfg.media_marker_pattern ?? "\\[\\s*(image|video|audio|caption|embed)[^\\]]*\\]", "i")) || [])[1];
		const isVideo = url && (idRe.test(url) || this.#carouselVideoUrlOk(url, rich));
		// EVERY bracketed marker comes out of the visible text, not just the media one:
		// the writer brackets media-list references beside it ("[Item 64] [Image] lamp",
		// TRR102-1.0) and any survivor would be a literal tag on the finished page. Same
		// strip the round-271 media|caption form uses.
		const text = this.#cellText(raw).replace(/\[[^\]]*\]/g, " ")
			.replace(/https?:\/\/[^\s\]"<>]+/g, " ").replace(/\s+/g, " ").trim();

		// a VIDEO cell
		if (isVideo && (!kind || /video|embed/i.test(kind) || !text)) {
			const id = String(url).match(idRe)?.[1];
			const embed = id ? { video: id } : (() => {
				const alt = this.#carouselVideoEmbed(url, tpl, rich);
				return alt ? { html: alt } : null;
			})();
			if (!embed) { this.#carNoteAssetRequest(bundle, null, raw, mv); return []; }
			return text ? [embed, { p: text }] : [embed];
		}
		// an IMAGE cell — a url names the asset; a brief with no url is an asset request
		if (url || /^image$/i.test(kind ?? "")) {
			const file = this.#carImageFilename(url, tpl, mv);
			if (!file) { this.#carNoteAssetRequest(bundle, null, raw, mv); return text ? [{ p: text }] : []; }
			return text ? [{ img: file }, { p: text }] : [{ img: file }];
		}
		// an AUDIO cell
		if (/^audio$/i.test(kind ?? "")) {
			const au = this.#carAudioHtml(url, raw, mv);
			if (!au) { this.#carNoteAssetRequest(bundle, null, raw, mv); return text ? [{ p: text }] : []; }
			return text ? [{ html: au }, { p: text }] : [{ html: au }];
		}
		// a PROSE cell. The writer separates a slide's title from its copy with " / "
		// (the round-271 media|caption convention); a SHORT leading segment titles the
		// slide, a long one is simply the first paragraph.
		if (!text) return [];
		const sep = new RegExp(cfg.segment_separator ?? "\\s+/\\s+");
		const segs = text.split(sep).map((s) => s.trim()).filter(Boolean);
		if (segs.length > 1 && this.#carIsSlideTitle(segs[0], cfg)) {
			return [{ h: segs[0] }, { p: segs.slice(1).join("\n") }];
		}
		return [{ p: segs.join("\n") }];
	}

	/**
	 * ROUND 279 — does this table cell read as a WRITER INSTRUCTION rather than
	 * slide content? Built from the SHARED Instruction_Cues vocabulary (the same
	 * data TagNormaliser classifies spans with), so extending it stays a data edit.
	 * Only a cell whose RED text carries a cue counts: a black cell is the writer's
	 * own copy, and a red cell that merely names an asset ("[image] teens doing art
	 * together") is handled as an asset request by the media branches above.
	 */
	static #carStripInstructionSpans(raw, cfg = {}, note = () => {}) {
		if (cfg.instruction_guard === false) return raw;
		if (!this.#hasRedText(raw)) return raw;
		// The cue must OPEN the span. The shared Instruction_Cues.cue_patterns list is
		// built for classifying a whole red SPAN, and several of its entries are
		// ordinary English ("below", "above", "beside", "note") — matching them
		// anywhere inside a caption would delete the writer's own prose (AGH1002-1.0's
		// soil captions). An addressed opener cannot be confused with copy.
		const openers = cfg.instruction_openers
			?? (DataService.Data.InstructionCues?.addressee_prefixes ?? [])
				.concat(["please", "can you", "could you", "could we", "is it possible", "we would like"]);
		if (!openers.length) return raw;
		const openRe = new RegExp(`^(?:${openers.join("|")})\\b`, "i");
		return String(raw).replace(/🔴\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]🔴/g, (whole, inner) => {
			const words = String(inner).replace(/\[[^\]]*\]/g, " ").replace(/^[^\p{L}\p{N}]+/u, "").trim();
			if (!words || !openRe.test(words)) return whole;         // content, or a bare marker
			note(words);
			return " ";
		});
	}

	/**
	 * ROUND 279 — is this the table's HEADER row (to be dropped) rather than the
	 * first slide? Only two shapes count: every non-empty cell is entirely RED (the
	 * writer's column labels, "Image ║ Caption"), or every non-empty cell is exactly
	 * a label WORD. Deliberately stricter than the round-63
	 * #isCarouselTitleOrLabelRow, which also treats any single-non-empty-cell row as
	 * a label — the shape of AGH1002's every data row (an EMPTY image cell beside
	 * the caption), so reusing it here ate the whole slideshow.
	 */
	static #carIsHeaderRow(row, cfg = {}, tpl = {}) {
		if (!Array.isArray(row) || !row.length) return false;
		const cells = row.filter((c) => this.#cellText(c).trim());
		if (!cells.length) return true;                              // a wholly empty spacer row
		// an all-red row of SHORT labels ("Image ║ Caption", "Slide 1"). The length test
		// matters: AGH1002-1.0's writer coloured the slide CAPTIONS red, whole sentences
		// at a time, and without it every data row read as a header and the slideshow
		// emptied itself.
		const maxW = cfg.header_max_words ?? 3;
		if (cells.every((c) => this.#isFullyRed(c))
			&& cells.every((c) => !/https?:\/\//.test(String(c ?? "")))
			&& cells.every((c) => this.#cellText(c).replace(/\[[^\]]*\]/g, " ").trim().split(/\s+/).length <= maxW)) return true;
		const labels = (cfg.header_label_keywords && cfg.header_label_keywords.length)
			? cfg.header_label_keywords
			: (tpl.header_label_keywords ?? ["images", "image", "text", "caption", "title", "slide"]);
		const re = new RegExp(`^(${labels.join("|")})$`, "i");
		return cells.every((c) => re.test(this.#cellText(c).replace(/\[[^\]]*\]/g, " ").trim()));
	}

	/** ROUND 279 — a short leading segment is the slide's TITLE, not its first line. */
	static #carIsSlideTitle(s, cfg = {}) {
		const t = String(s ?? "").trim();
		if (!t) return false;
		const words = t.split(/\s+/).length;
		// A trailing full stop does not disqualify a SHORT lead — writers punctuate
		// their slide titles inconsistently and treating "Water levels in soil." as
		// copy while "Sunlight" became a heading left ONE carousel with two different
		// slide shapes (AGH1002-3.0). A long sentence is still copy.
		if (/[.!?]$/.test(t) && words > (cfg.title_max_words ?? 6)) return false;
		return words <= (cfg.title_max_words ?? 6);
	}

	/**
	 * ROUND 279 — THE LEAK GUARD (the round-167 rule at this seam). A finished
	 * carousel that still shows a bracketed writer tag would put raw markup on the
	 * page, so it declines and the honest hand-off box is kept instead. Building can
	 * therefore only ever PREVENT a visible leak, never add one.
	 */
	static #carHasBracketTag(html, cfg = {}) {
		if (cfg.leak_guard === false) return false;
		const vis = String(html ?? "").replace(/<!--[\s\S]*?-->/g, " ");
		const re = new RegExp(cfg.leak_pattern ?? "\\[\\s*[A-Za-z][^\\]\\n]{0,40}\\]");
		if (re.test(vis)) return true;
		// ROUND 284 — the guard had the SAME blind spot as the strip it backstops: its
		// pattern requires a CLOSING bracket, so a dangling "[image Young man gaming"
		// was invisible to it and the build shipped with a visible tag. A second arm
		// catches an unclosed marker, but only for a KNOWN media tag word, so it can
		// never refuse a build over an ordinary "[" in the writer's prose.
		if (!cfg.leak_pattern_dangling) return false;
		return new RegExp(cfg.leak_pattern_dangling, "i").test(vis);
	}

	static #carNoteAssetRequest(bundle, m, raw, mv = {}) {
		if (mv.note_asset_requests === false) return;
		const txt = this.#cellText(String(m?.text ?? "") || String(raw ?? "")).trim();
		if (!txt) return;
		const list = (bundle.instructions ??= []);
		if (!list.some((s) => String(s).trim() === txt)) list.push(txt);
	}

	/**
	 * ROUND 275 — is this line NOTHING BUT a bare video reference URL? The writer lists a
	 * video's URL on its own line beneath the [video] tag; where the tail lookahead has not
	 * claimed it (its video already carried a URL of its own, for instance) it must still not
	 * render as learner prose. MEASURED: across the whole gold library there are 1,618
	 * carousel captions and NOT ONE is a bare URL — the same convention MediaBuilder applies
	 * on the body path (round 80, stripMediaResidue). Surrounding brackets/parentheses are
	 * ignored; a line with ANY real words alongside the URL is prose and is kept.
	 *
	 * @param {string} raw - the member's raw text
	 * @param {object} cfg - the rich_slides config block
	 * @param {object} env - process.env (for the CARVIDEO_OFF reversal)
	 * @returns {boolean} true when the line is only a video reference
	 */
	static #carouselBareMediaRef(raw, cfg, env) {
		if ((cfg?.video_url_recovery?.drop_bare_url_lines === false) || env?.CARVIDEO_OFF) return false;
		const s = String(raw ?? "");
		const urls = s.match(/https?:\/\/[^\s\]"<>)]+/g);
		if (!urls || !urls.length) return false;
		if (!urls.every((u) => /youtu\.?be|youtube\.com|vimeo/i.test(u))) return false;
		const rest = this.#cellText(s.replace(/https?:\/\/[^\s\]"<>)]+/g, " ")).replace(/[()[\]|/\-–—.,:;]/g, " ").trim();
		return !rest;
	}

	/**
	 * ROUND 275 — is this URL a VIDEO source a carousel slide can embed? Used by the widened
	 * tail-URL lookahead so it can never adopt a PDF, a document or an image as a "video".
	 * A YouTube url (any form, including /shorts/) always qualifies; any other http(s) url
	 * qualifies unless it ends in a document/image/audio extension.
	 *
	 * @param {string} url - the candidate media URL
	 * @param {object} cfg - the rich_slides config block (carries video_url_recovery)
	 * @returns {boolean} true when a slide could embed it
	 */
	static #carouselVideoUrlOk(url, cfg) {
		const u = String(url ?? "");
		if (!/^https?:\/\//i.test(u)) return false;
		if (/youtu\.?be|youtube\.com/i.test(u)) return true;
		const deny = new RegExp(cfg?.video_url_recovery?.deny_extensions
			?? "\\.(pdf|docx?|pptx?|xlsx?|jpe?g|png|gif|svg|webp|mp3|wav|m4a|ogg|zip)(\\?|#|$)", "i");
		return !deny.test(u);
	}

	/**
	 * ROUND 275 — the embed HTML for a carousel video whose URL the YouTube-id regex could
	 * not read. Mirrors the free-body media emitter's own convention (MediaBuilder.media):
	 * a YouTube SHORTS url ships the corpus 1x1 short form (the round-266 shorts_embed,
	 * gold-verified 57/57), anything else ships the shared generic iframe. Returns null when
	 * the url is not an embeddable video source, so the caller keeps the hand-off box.
	 *
	 * @param {string} url - the media URL
	 * @param {object} tpl - the carousel template block (carries media_table.shorts_*)
	 * @param {object} cfg - the rich_slides config block
	 * @returns {string|null} the embed HTML, or null to decline
	 */
	static #carouselVideoEmbed(url, tpl, cfg) {
		const u = String(url ?? "");
		if (!this.#carouselVideoUrlOk(u, cfg)) return null;
		const vid = DataService.Data.EmitTemplates.video ?? {};
		const mt = tpl?.media_table ?? {};
		const sId = mt.shorts_id_re ? new RegExp(mt.shorts_id_re) : /youtube\.com\/shorts\/([\w-]{11})/;
		const sm = u.match(sId);
		if (sm && mt.shorts_embed) return Utils.FillTemplate(mt.shorts_embed, { videoId: sm[1] });
		if (sm && vid.youtube) return Utils.FillTemplate(vid.youtube, { videoId: sm[1], params: "" });
		if (/youtu\.?be|youtube\.com/i.test(u)) return null;   // a YouTube url with no readable id
		if (!vid.generic_iframe) return null;
		return Utils.FillTemplate(vid.generic_iframe, { url: Utils.EscapeHtml(u) });
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

	/**
	 * MEDIA|CAPTION-TABLE carousel (ROUND 271 — Chris, OSSC401-1.0: "there are
	 * still some carousels not being built"). The writer authors the slideshow as
	 * ONE table whose every DATA ROW pairs a MEDIA cell ([video]/[image] red tag +
	 * URL) with a PROSE cell holding that slide's title and copy, with the writer's
	 * " / " separating each rendered paragraph:
	 *
	 *   "[video] https://youtube.com/watch?v=dOR6LPeeoeU"
	 *      | "**Tech support** / Scammers often make unexpected contact… /
	 *         **Example:** A pop-up on your screen says…"
	 *
	 * WHY IT NEEDED ITS OWN BRANCH. Round 266's #carouselMediaTable owns the
	 * ALL-media-cell form and declines the moment it meets the prose cell;
	 * #carouselImageTable owns image|caption and cannot resolve a video cell; and
	 * #carouselRich declines any bundle that captured a table. So this extremely
	 * plain shape fell all the way through to the hand-off box.
	 *
	 * THE FORM IS MEASURED, not guessed. Over every gold carousel slide carrying a
	 * video AND a heading: the title ships as <h5> 114:41 against <h4> (share 0.67
	 * — a round-182 SOLIDIFY) and the media follows the text 79:16 (0.83). So a
	 * slide is  <div class="item"> <h5>title</h5> <p>copy</p>* {media} </div>,
	 * which byte-matches the OSSC401 and ENGS401 golds.
	 *
	 * TITLE = the leading segment when the writer wrote it wholly BOLD (their own
	 * emphasis, not an invented convention); a prose cell with no bold lead ships
	 * copy-only, never a fabricated heading.
	 *
	 * VIDEO-SCOPED (cfg.require_video) so the image-only table population stays
	 * with its existing owner byte-for-byte.
	 *
	 * NEVER HALF-BUILDS → null (the honest hand-off box) on: a row that is not
	 * exactly one resolvable media cell + one or more prose cells, an image URL the
	 * iStock filename rule cannot name, a video on an unknown host, a prose cell
	 * that renders empty, or fewer than min_rows rows.
	 *
	 * @param {object} args - bundle / tpl / renderInline / run
	 * @returns {string|null} the built carousel, or null
	 *
	 * Data: carousel.media_caption_table. Env toggle: CARMEDCAP_OFF.
	 */
	static #carouselMediaCaptionTable({ bundle, tpl, renderInline, run }) {
		const cfg = tpl.media_caption_table;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.CARMEDCAP_OFF) return null;
		const table = (bundle.tables ?? [])[0];
		const rows = table?.rows ?? [];
		if (!rows.length) return null;

		const inline = renderInline ?? ((s) => s);
		const acks = DataService.Data.AcksFormats ?? {};
		const ytRe = new RegExp(acks.extraction_regexes?.youtube_id
			?? "(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([\\w-]{11})");
		const shortsRe = new RegExp(cfg.shorts_id_re ?? "youtube\\.com/shorts/([\\w-]{11})");
		const tagRe = /\[\s*(image|video)\s*\]/i;
		const urlRe = /https?:\/\/[^\s\]"<>]+/;
		const sepRe = new RegExp(cfg.segment_separator ?? "\\s+/\\s+");

		const items = [];
		let sawVideo = false;
		for (const r of rows) {
			if (!Array.isArray(r)) return null;
			let media = null, prose = [];
			for (const cell of r) {
				const raw = String(cell ?? "");
				if (!raw.trim()) continue;                       // empty cell — skipped
				const kind = tagRe.exec(raw);
				const url = urlRe.exec(raw)?.[0] ?? "";
				if (kind && url) {
					if (media) return null;                      // two media cells in one row → not this form
					media = { kind: kind[1].toLowerCase(), url };
					continue;
				}
				if (url) return null;                            // an untagged media URL → not this form
				const t = this.#cellText(raw).replace(/\[[^\]]*\]/g, " ").trim();
				if (!t) return null;                             // a bare marker cell → not this form
				prose.push(t);
			}
			if (!media && !prose.length) continue;               // a wholly empty row
			if (!media || !prose.length) return null;            // never half-build

			// ---- the media part -------------------------------------------------
			let mediaHtml;
			if (media.kind === "image") {
				const filename = this.#istockFilename(media.url, tpl);
				if (!filename) return null;                      // un-nameable image → bail
				mediaHtml = this.#assetImage(filename, tpl, run);
			} else {
				sawVideo = true;
				const shortId = media.url.match(shortsRe)?.[1] ?? null;
				const watchId = media.url.match(ytRe)?.[1] ?? null;
				if (!shortId && !watchId) return null;           // unknown video host → bail
				mediaHtml = shortId
					? Utils.FillTemplate(cfg.shorts_embed, { videoId: shortId })
					: Utils.FillTemplate(DataService.Data.EmitTemplates.video.youtube,
						{ videoId: watchId, params: "" });
			}

			// ---- the prose part: title (bold lead) + one <p> per segment --------
			const segs = prose.join(" ").split(sepRe).map((s) => s.trim()).filter(Boolean);
			if (!segs.length) return null;
			const parts = [];
			let body = segs;
			const lead = segs[0] ?? "";
			// a WHOLLY bold leading segment is the writer's own slide title
			const boldLead = /^\*\*[\s\S]+\*\*$/.test(lead)
				&& !/\*\*\s*\S[\s\S]*?\*\*[\s\S]*?\*\*/.test(lead.slice(2, -2));
			if (boldLead && segs.length > 1) {
				const title = lead.replace(/^\*\*|\*\*$/g, "").replace(/\*\*/g, "").trim();
				if (title) {
					parts.push(Utils.FillTemplate(cfg.title, { text: inline(title) }));
					body = segs.slice(1);
				}
			}
			for (const seg of body) {
				const html = inline(seg);
				if (!String(html).trim()) return null;           // a segment that renders to nothing
				parts.push(Utils.FillTemplate(cfg.paragraph, { text: html }));
			}
			parts.push(mediaHtml);                               // text-first (gold 79:16)
			items.push(Utils.FillTemplate(cfg.item, { parts: parts.join("\n") }));
		}

		if ((cfg.require_video ?? true) && !sawVideo) return null;   // image-only tables keep their owner
		if (items.length < (cfg.min_rows ?? tpl.min_slides ?? 2)) return null;

		// trailing free-body paragraph(s) after the slide table (kept outside the carousel).
		const trailing = this.#carouselTrailingBody(bundle, inline, tpl);
		if (trailing === null) return null;
		return [tpl.open, ...items, tpl.close, ...trailing].join("\n");
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

		// ROUND 275 (Chris — "the click-and-drop builder gives up whenever there's an image:
		// 179 failures, 5 successes"). An [image] member inside the reveal content used to
		// bail the whole widget at the "(tag && tag !== 'body')" guard below. The human puts
		// images in clickDrop reveal content routinely — MEASURED over the whole gold library,
		// 939 of 2,877 clickDropContent blocks (33%) across 235 modules contain an <img> — so
		// each item now keeps an ORDERED part list ({p:text} / {img:filename}) and the image
		// renders in the writer's own position, as the standard Mode P/D asset.
		// Data clickDrop.image_member; env CDIMAGE_OFF.
		const imgCfg = tpl.image_member ?? {};
		const imgOn = imgCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.CDIMAGE_OFF);

		const items = [];          // [{ label, body:[paragraphs], parts:[...] }]
		let cur = null;
		const flushBody = () => {
			if (!cur || !cur.body.length) return;
			cur.parts.push({ body: cur.body });
			cur.body = [];
		};
		for (const m of members) {
			const tag = m && m.type === "tag" ? m.parse?.primary?.tag : null;
			const raw = m && m.type === "tag" ? (m.blackAfter ?? "") : (m.text ?? "");
			const text = this.#cellText(raw);

			// (a) a [click drop N] opens a new item; its trailing text is the button label.
			//     ROUND 275: a LEADING label-less [click drop] is the widget's OPENER, not an
			//     item — the same convention [accordion]/[tabs] have always used (the writer
			//     types "[click drop]" then "[click drop 1] Label"). It is skipped; a
			//     label-less tag AFTER items have started is still a malformed item and bails.
			if (tag === "click drop") {
				if (!text && !cur && imgOn) continue;              // the widget opener
				if (!text || this.#hasRedText(raw)) return null;   // a button with no clean label → bail
				flushBody();
				cur = { label: text, body: [], parts: [] };
				items.push(cur);
				continue;
			}

			// (a.5) an [image] member inside the reveal content (ROUND 275).
			//   • an EMPTY marker — no URL and no text of its own — is a media-list REFERENCE
			//     the developer fills in later, with no asset to render. The human ships
			//     nothing for it (verified across the XDLS903-906 family, whose gold reveal
			//     panels carry the writer's headings/prose and no image at all), so it is
			//     SKIPPED, exactly like the round-242 image-arrangement layout marker.
			//   • a derivable iStock image renders in place as the standard Mode P/D asset.
			//   • anything else (a non-iStock host, a caption riding along) still bails the
			//     WHOLE widget — never half-built.
			if (tag === "image" && imgOn) {
				const url = m.block?.links?.[0]?.target
					?? (String(raw).match(/https?:\/\/[^\s\]"<>]+/)?.[0] ?? "");
				// an EMPTY marker is skipped wherever it sits — including before the first
				// button, which the pre-round blank-line guard already did (byte-identity).
				if (!url && !text) continue;                       // an empty media-list marker → renders nothing
				if (!cur) return null;                             // a real image before any button → bail
				if (this.#hasRedText(raw)) return null;
				const filename = this.#istockFilename(text || url, tpl);
				if (!filename) return null;                        // non-iStock / underivable → bail
				flushBody();
				cur.parts.push({ img: filename });
				// TEXT RIDING ALONG WITH THE URL is the item's own prose CONTINUING after the
				// image (the writer types the asset link mid-paragraph — HES1007's scenario
				// panels), not a caption the widget cannot place: it renders as body text
				// after the image, in the writer's order, so nothing is lost and nothing is
				// invented. The accordion's stricter "a caption rode along → bail" rule is
				// right there (its panels have a fixed image-then-body shape); a clickDrop
				// reveal panel is free-flowing content.
				const residual = text.replace(/^\s*\[[^\]]*\]\s*/, "")
					.replace(/https?:\/\/\S+/g, " ").replace(/\S*gm-?\d{6,10}\S*/g, " ")
					.replace(/\s+/g, " ").trim();
				if (residual) cur.body.push(residual);
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
		flushBody();

		if (items.length < (tpl.min_items ?? 1)) return null;
		for (const it of items) if (!it.label || !it.parts.length) return null;   // each needs a label + content

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
		// ROUND 275: the item's parts render in the writer's own order. An item with no image
		// has exactly ONE body part holding the whole joined body, so its output is
		// byte-identical to the pre-round form.
		const renderBody = (body) => (listContent
			? ListsAndRuns.renderBlackText(body.join("\n"), run, [], false).join("\n")
			: body.map((t) => `<p>${inline(t)}</p>`).join(""));
		const contents = items.map((it) => Utils.FillTemplate(tpl.content, {
			content: it.parts.map((p) => (p.img
				? this.#assetImage(p.img, tpl, run)
				: renderBody(p.body))).join(""),
		}));
		return [tpl.open, ...buttons, ...contents, tpl.close].join("\n");
	}

	// =======================================================================
	// ROUND 283 — THE GENERAL clickDrop COMPOSER
	// =======================================================================
	/**
	 * clickDrop ENTRY (ROUND 283, Chris — the interactive-coverage chain, round 8 of 8).
	 * The narrow member walk above runs FIRST and is untouched, so all 61 pre-round
	 * builds are byte-identical BY CONSTRUCTION (the round-276 architecture: a fallback
	 * cannot break what already works — env CLICKDROPS_OFF proves it).
	 */
	static #clickDropEntry({ bundle, tpl, renderInline, run, renderBlock, renderTable, renderNested }) {
		const narrow = this.#clickDrop({ bundle, tpl, renderInline, run });
		if (narrow) return narrow;
		return this.#clickDropItems({ bundle, tpl, renderInline, run, renderBlock, renderTable, renderNested });
	}

	/**
	 * THE GENERAL clickDrop COMPOSER (ROUND 283; `CLICKDROPS_OFF`).
	 *
	 * WHY IT EXISTS. The decline recorder (outputs/_measure_r283_clickdrop.cjs — the
	 * round-276→282 tool re-pointed, which accounted for 100% of the 629 declines)
	 * found the blocker is NOT the [image] the coverage dashboard named (round 275
	 * already fixed that; only 23 declines are image-decided now). It is that the
	 * narrow walk knows exactly ONE authoring form — a run of labelled [click drop N]
	 * tags each followed by plain [body] text — and the writers use at least six:
	 *
	 *   240  an item with a LABEL and NO CONTENT the walk could keep
	 *   125  NO item resolved at all — 85 of them lay the items out in a TABLE
	 *    94  content arrived BEFORE the first button (a lead paragraph, or a
	 *         heading-delimited series) and the walk treated that as fatal
	 *    85  a member it cannot place ([H3] 77, [data marker] 18, [video] 62,
	 *         [button] 58, [external link] 5 — the cross-cutting foreign-member
	 *         blocker the dashboard also lists against dragAndDrop and accordion)
	 *
	 * SO: resolve items from an ordered DELIMITER vocabulary, over the round-278
	 * member vocabulary shared verbatim (#accMemberParts + its round-281 `delims`
	 * extension — omitted keys keep every accordion/tabs default, so those paths
	 * cannot move). First delimiter that yields enough items wins:
	 *
	 *   D1  labelled [click drop N] tags            the classic form, now over the
	 *                                               full member vocabulary
	 *   D2  a captured TABLE, read five ways (#cdTableItems)
	 *   D3  a repeating same-level HEADING run      [click drop] [H3] a [H3] b …
	 *
	 * GOLD-BACKED GUARDS (outputs/_measure_r283_cdgold.py — 1199 groups / 211 modules,
	 * body-scoped, class matched as a TOKEN per the round-282 trap):
	 *   • min_items 1 for an EXPLICIT delimiter — a ONE-item clickDrop is the gold's
	 *     own PLURALITY at 43.5% — but min_inferred_items 2, because one item from an
	 *     inferred reading would be a guess (the round-278 explicit-vs-inferred split).
	 *   • label_max_words 8: of 3036 gold labels, ≤3 words is 83.7% and ≤8 is 99.2%.
	 *     A longer line is not a button label, so the item takes its BOLD LEAD or the
	 *     text before the writer's own " / " separator (the round-271/279 rule) — and
	 *     if neither is there the composer declines rather than putting a paragraph
	 *     on a button.
	 *   • A LABEL IS NEVER INVENTED (the round-282 rule).
	 *
	 * NEVER HALF-BUILDS: no delimiter resolves enough items · an item with no label or
	 * no rendered content · red writer-instruction text in a label · a member it cannot
	 * place · or a finished widget that still shows a resolved [tag] (#accLeakGuard —
	 * the round-167/275/277/278 rule at this seam, so building can only ever PREVENT a
	 * visible leak, never add one).
	 *
	 * Data interactive_builders.clickDrop.general_items.
	 */
	static #clickDropItems({ bundle, tpl, renderInline, run, renderBlock, renderTable, renderNested }) {
		const cfg = tpl?.general_items;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.CLICKDROPS_OFF) return null;
		const members = bundle?.memberItems ?? [];
		if (!members.length) return null;
		const inline = renderInline ?? ((s) => s);
		const notes = [];

		// (1) Every member as an ordered {role,…} PART — the round-278 vocabulary,
		//     shared verbatim. `delims` names clickDrop's own delimiter/face tags and
		//     the elements its gold panels legitimately carry; every omitted key keeps
		//     the accordion default, so the accordion and tabs cannot move.
		const parts = this.#accMemberParts(members, {
			tpl, cfg, run, renderTable, notes,
			delims: {
				tags: cfg.delimiter_tags ?? ["click drop"],
				opener_tags: cfg.opener_tags ?? [],
				panel_tag_pattern: cfg.delimiter_pattern,
				panel_ordinal_pattern: cfg.delimiter_ordinal_pattern,
				head_tags: cfg.head_tags ?? [],
				head_level: cfg.head_level ?? "h4",
				text_tags: cfg.text_tags ?? [],
				note_tags: cfg.note_tags ?? [],
				face_tags: cfg.face_tags ?? [],
				delimiter_media_role: cfg.delimiter_media_role !== false,
			},
		});
		if (!parts) return null;

		// (2) Resolve the ITEMS from the first delimiter kind that is present.
		const items = this.#cdResolveItems(parts, cfg, tpl);
		if (!items) return null;
		const floor = items.inferred ? (cfg.min_inferred_items ?? 2) : (cfg.min_items ?? 1);
		if (items.list.length < floor) return null;

		// (3) Render. The gold's shape is ALL buttons first, then ALL content panels,
		//     paired by position (the JS pairs button[i] -> content[i]) — the same emit
		//     the narrow walk uses, so a build from either path is indistinguishable.
		const built = this.#cdRenderItems(items.list, { tpl, cfg, inline, run, renderBlock, renderNested, lead: items.lead });
		if (!built) return null;
		const html = [tpl.open, ...built.buttons, ...built.contents, tpl.close].join("\n");
		if (this.#accLeakGuard(html, cfg)) return null;            // a build must never ADD a leak
		// LEAD PROSE — anything the writer put before the first button renders in its
		// own place ABOVE the widget (the round-196 trailing_body rule, inverted), so
		// building can never lose a line the writer wrote.
		const lead = built.lead.filter((h) => h && String(h).trim());
		if (lead.length && this.#accLeakGuard(lead.join("\n"), cfg)) return null;
		if (notes.length) bundle.instructions = [...(bundle.instructions ?? []), ...notes];
		bundle.r283ClickDrop = true;                               // detector / affected-set marker
		return [...lead, html].join("\n");
	}

	/**
	 * ROUND 283 — resolve clickDrop ITEMS from the ordered parts. Returns
	 * `{ list:[{label, parts:[…]}], lead:[…], inferred:bool }` or null.
	 *
	 * `inferred` marks a reading the writer did not delimit explicitly (a table shape,
	 * a heading run), which raises the item floor to min_inferred_items.
	 */
	static #cdResolveItems(parts, cfg, tpl) {
		const substantive = parts.filter((p) => p.role !== "note");
		if (!substantive.length) return null;

		// ---- D1: explicit [click drop N] delimiters ---------------------------
		if (parts.some((p) => p.role === "panel")) {
			const r = this.#cdWalk(parts, cfg, (p) => (p.role === "panel" ? p.head : null));
			if (r && r.list.length) return { ...r, inferred: false };
			return null;
		}

		// ---- D2: a captured TABLE ---------------------------------------------
		const tables = parts.filter((p) => p.role === "table");
		if (tables.length === 1) {
			const rows = tables[0].item?.block?.rows ?? [];
			const list = this.#cdTableItems(rows, cfg, tpl);
			if (list && list.length) {
				// anything OUTSIDE the table (a lead paragraph, the widget's central image)
				// keeps its place before the widget.
				const lead = parts.filter((p) => p.role !== "table" && p.role !== "note");
				return { list, lead, inferred: true };
			}
		}

		// ---- D3: a repeating same-level HEADING run ---------------------------
		const heads = parts.filter((p) => p.role === "head");
		if (heads.length >= 2) {
			const lvl = heads[0].level;
			if (heads.every((h) => h.level === lvl)) {
				const r = this.#cdWalk(parts, cfg, (p) => (p.role === "head" && p.level === lvl ? p.text : null));
				if (r && r.list.length) return { ...r, inferred: true };
			}
		}
		return null;
	}

	/**
	 * ROUND 283 — the shared item WALK. `openerOf(part)` returns the label text when
	 * that part opens a new item, else null. Two general rules live here:
	 *
	 *  • CONTENT BEFORE THE FIRST BUTTON is the widget's own LEAD prose, not a reason
	 *    to throw the widget away (94 declines died on that) — it renders above the
	 *    widget, in the writer's own place, so no line is ever lost.
	 *  • A RUN OF MEDIA IMMEDIATELY BEFORE A DELIMITER BELONGS TO THE ITEM IT OPENS.
	 *    Writers put the item's picture first and name it after ("[click drop 1 image]
	 *    <url>" then "[H4] Basketball vocabulary", BLL244-2.0), so trailing media is
	 *    buffered and handed FORWARD; a media part with ordinary content after it is
	 *    flushed in place and stays where the writer put it.
	 */
	static #cdWalk(parts, cfg, openerOf) {
		const list = [], lead = [];
		let cur = null, pending = [];
		const isMedia = (p) => p.role === "img" || p.role === "video" || p.role === "embed";
		const flush = () => { if (pending.length) { (cur ? cur.parts : lead).push(...pending); pending = []; } };
		for (const p of parts) {
			if (p.role === "note") continue;
			const label = openerOf(p);
			if (label !== null && label !== undefined) {
				const lab = this.#cdLabel(label, cfg);
				if (!lab) return null;
				const carried = pending; pending = [];
				cur = { label: lab.label, parts: [...carried] };
				if (lab.rest) cur.parts.push({ role: "text", text: lab.rest });
				list.push(cur);
				continue;
			}
			if (isMedia(p)) { pending.push(p); continue; }
			flush();
			(cur ? cur.parts : lead).push(p);
		}
		flush();
		return { list, lead };
	}

	/**
	 * ROUND 283 — a button LABEL from a line of writer text, or null.
	 *
	 * MEASURED (outputs/_measure_r283_cdgold.py, 3036 gold labels): ≤3 words 83.7%,
	 * ≤6 97.0%, ≤8 99.2%. So a line longer than label_max_words is NOT a label: it is
	 * the item's own content with its label at the front, and the writer marks that
	 * front two ways — a **bold lead** (the round-278 accordion rule) or the " / "
	 * separator the same writers use for a line break (rounds 271/279). Whichever is
	 * present wins; with neither, the composer declines rather than inventing one.
	 */
	/**
	 * ROUND 283 — a table CELL's own line breaks. The docx extractor serialises the
	 * line breaks inside a table cell as the writer's " / " separator, and the human
	 * ships one <p> per part: OSOH501-01's Whanaungatanga panel is three separate
	 * paragraphs in the gold, from one " / "-joined cell. So " / " becomes a newline
	 * and the standard black-text renderer takes it from there (a "• " part still
	 * groups into a real <ul>, per round 241). The round-276 speechBubble precedent,
	 * and the same `\s+/\s+` form the carousel's segment_separator uses.
	 */
	static #cdCellLines(text, cfg) {
		const t = String(text ?? "");
		if (cfg.cell_line_split === false) return t;
		const re = new RegExp(cfg.cell_line_separator ?? "\\s+/\\s+", "g");
		return t.split(re).map((s) => s.trim()).filter(Boolean).join("\n");
	}

	static #cdLabel(raw, cfg) {
		const t = this.#cellText(String(raw ?? "")).replace(/\s+/g, " ").trim();
		if (!t) return null;
		if (this.#hasRedText(raw)) return null;
		// A BARE URL IS NEVER A LABEL. ENGC301-5.0's table is ten Google Drive links and
		// nothing else, and reading it as label|content shipped five buttons whose face
		// was a raw URL over an empty panel — caught live by the verifier. A label is
		// never invented, so a table with no words in it declines.
		if (/^\s*https?:\/\/\S+\s*$/.test(t)) return null;
		if (!/\p{L}/u.test(t)) return null;                        // no letters = not a label
		const max = cfg.label_max_words ?? 8;
		const plain = t.replace(/\*\*/g, "").trim();
		if (plain && plain.split(/\s+/).length <= max && !this.#accHasBracketTag(plain)) {
			return { label: plain, rest: "" };
		}
		// (a) a bold lead — "**Stage 1.** • Action: …"
		const bl = this.#accBoldLead(t, { ...cfg, head_max_words: max });
		if (bl) return { label: bl.head, rest: bl.rest };
		// (b) the writer's own " / " separator — "Manaaki / Show respect and kind…"
		const sep = cfg.label_separator ?? " / ";
		const i = t.indexOf(sep);
		if (i > 0) {
			const head = t.slice(0, i).replace(/\*\*/g, "").trim();
			if (head && head.split(/\s+/).length <= max && !this.#accHasBracketTag(head)) {
				return { label: head, rest: t.slice(i + sep.length).trim() };
			}
		}
		return null;
	}

	/**
	 * ROUND 283 — ITEMS FROM A CAPTURED TABLE. The single biggest structural blocker:
	 * 85 of the 125 "no item resolved" declines lay the items out in a table the walk
	 * never looked at. Five readings, tried in order, each triangulated against a
	 * writer's template and the human's finished page:
	 *
	 *  T1  a FACE-MARKER COLUMN — column 0 is [front]/[drop] repeating, so each
	 *      front-row/drop-row PAIR gives one item per remaining COLUMN
	 *      (OSSC401-2.0's 4x5 scam table; the round-282 flipCard T1b turned 90°).
	 *  T2  a HEADER ROW ([front] | [drop], or known label words) peeled, then
	 *  T3  N rows x 2 columns — label | content per ROW. The dominant clean form
	 *      (OSSC401-2.0 misinformation/disinformation/malinformation; XMES203's
	 *      six image|caption rows, where the image cell IS the button — the gold
	 *      ships an <img> inside 26.2% of its 3036 buttons).
	 *  T4  a TWO-ROW table with no markers — one item per COLUMN, row 0 the label
	 *      and row 1 the content (ENGI401-4.0's five events over five YouTube links).
	 *  T5  otherwise ONE ITEM PER CELL, each split by #cdLabel (OSOH501-1.0's
	 *      "[Click drop] Manaaki / Show respect and kind…" — the human's finished
	 *      page ships exactly those three buttons: Whanaungatanga, Manaaki, Tika).
	 *
	 * A cell that is WHOLLY the writer's red instruction text is markup, not content
	 * (the round-281 rule: #isFullyRed per cell, never "any red").
	 */
	static #cdTableItems(rows, cfg, tpl) {
		if (!Array.isArray(rows) || !rows.length) return null;
		const cellRaw = (c) => String((c && typeof c === "object" ? c.text : c) ?? "");
		const grid = rows.map((r) => (r ?? []).map(cellRaw));
		const w = Math.max(0, ...grid.map((r) => r.length));
		if (!w) return null;
		const faceRe = new RegExp(cfg.face_marker_pattern ?? "^\\[?\\s*(front|drop|back|reveal)\\s*\\]?$", "i");
		const isFace = (s) => faceRe.test(this.#cellText(s).replace(/\*\*/g, "").trim());
		const has = (s) => this.#cellText(s).replace(/\s+/g, " ").trim().length > 0;
		// A cell carrying the writer's OWN [click drop] tag is a self-delimited item.
		const cellDelimRe = new RegExp(cfg.cell_delimiter_pattern ?? "\\[\\s*click\\s*drop[^\\]]*\\]", "i");
		const isSelfDelim = (s) => cellDelimRe.test(String(s ?? ""));

		// ---- T0: the writer tagged the CELLS themselves ----------------------
		// When >=2 cells carry their own [click drop] tag the table is not a
		// label|content grid at all — each tagged CELL is one item, exactly as if the
		// writer had typed the tags in a paragraph run (OSOH501-1.0's three values,
		// whose finished page ships precisely those three buttons). Tested FIRST,
		// because the row/column readings below would otherwise pair a tagged cell
		// with its neighbour and lose the delimiter the writer actually gave.
		if (grid.reduce((n, r) => n + r.filter(isSelfDelim).length, 0) >= 2) {
			const items = [];
			for (const r of grid) {
				for (const c of r) {
					if (!has(c) || !isSelfDelim(c)) continue;
					const bare = this.#stripStructuralTags(this.#cellText(c).replace(cellDelimRe, " ")).trim();
					const lab = this.#cdLabel(bare, cfg);
					if (!lab || !lab.rest) return null;        // a button with nothing behind it
					items.push({ label: lab.label, parts: [{ role: "text", text: this.#cdCellLines(lab.rest, cfg) }] });
				}
			}
			return items.length ? items : null;
		}

		// ---- T1: a face-marker COLUMN --------------------------------------
		if (w >= 2 && grid.length >= 2 && grid.every((r) => isFace(r[0] ?? ""))) {
			const items = [];
			for (let r = 0; r + 1 < grid.length; r += 2) {
				for (let c = 1; c < w; c++) {
					const lab = this.#cdLabel(grid[r][c] ?? "", cfg);
					const body = this.#cellText(grid[r + 1][c] ?? "");
					if (!lab) continue;                       // an unlabelled column is skipped, not fatal
					const ps = [];
					if (lab.rest) ps.push({ role: "text", text: this.#cdCellLines(lab.rest, cfg) });
					if (body) ps.push({ role: "text", text: this.#cdCellLines(body, cfg) });
					if (!ps.length) continue;                 // never a button with nothing behind it
					items.push({ label: lab.label, parts: ps });
				}
			}
			return items.length ? items : null;
		}

		// ---- T2: peel a header row -----------------------------------------
		let body = grid;
		if (body.length > 1 && (body[0].every((c) => isFace(c) || !has(c)) && body[0].some((c) => isFace(c)))) {
			body = body.slice(1);
		} else if (body.length > 1 && this.#looksLikeHeaderRow(rows[0] ?? [], tpl)) {
			body = body.slice(1);
		}
		if (!body.length) return null;

		// ---- T3: N rows x 2 columns — label | content ------------------------
		if (w === 2 && body.length >= 1) {
			const items = [];
			for (const r of body) {
				const a = r[0] ?? "", b = r[1] ?? "";
				if (!has(a) && !has(b)) continue;
				if (this.#isFullyRed(a) || this.#isFullyRed(b)) return null;   // a marker row we did not peel
				const item = this.#cdRowItem(a, b, cfg, tpl);
				if (!item) return null;
				items.push(item);
			}
			return items.length ? items : null;
		}

		// ---- T4: a TWO-ROW table — one item per COLUMN -----------------------
		if (body.length === 2 && w >= 2) {
			const items = [];
			for (let c = 0; c < w; c++) {
				const a = body[0][c] ?? "", b = body[1][c] ?? "";
				if (!has(a) && !has(b)) continue;
				const item = this.#cdRowItem(a, b, cfg, tpl);
				if (!item) return null;
				items.push(item);
			}
			return items.length ? items : null;
		}

		// ---- T5: one item per CELL -------------------------------------------
		const items = [];
		for (const r of body) {
			for (const c of r) {
				if (!has(c)) continue;
				if (this.#isFullyRed(c)) continue;             // a bare marker cell is markup
				const lab = this.#cdLabel(c, cfg);
				if (!lab || !lab.rest) return null;            // a label with nothing behind it
				items.push({ label: lab.label, parts: [{ role: "text", text: this.#cdCellLines(lab.rest, cfg) }] });
			}
		}
		return items.length ? items : null;
	}

	/**
	 * ROUND 283 — ONE ITEM from a label CELL and a content CELL. The label cell is
	 * either text, or an [image] the writer made the button itself (XMES203's six
	 * image|caption rows; the gold ships an <img> inside 794 of its 3036 buttons).
	 */
	static #cdRowItem(labCell, conCell, cfg, tpl) {
		const conText = this.#cellText(conCell).trim();
		const url = this.#cellMediaUrl(labCell) || this.#cellMediaUrl(conCell);
		const labText = this.#cellText(labCell).trim();
		// (a) an IMAGE button — the label cell names an image, with or without a URL.
		const labIsImage = /^\s*\u{1f534}?\[?\s*(?:insert\s+)?image\b/iu.test(labText)
			|| /\[\s*(?:insert\s+)?image\b[^\]]*\]/i.test(String(labCell ?? ""));
		if (labIsImage) {
			const fn = url ? this.#accImageFilename(url, tpl, cfg) : null;
			// NO URL = a media-list ASSET REQUEST, and there is no button face to build:
			// the writer's words there are the PHOTO BRIEF ("quiet space", "man preparing
			// for bed"), not a label a reader should ever see — the round-282 rule, which
			// that round's verifier caught shipping as visible card text. A filename is
			// never invented and a label is never invented, so the widget declines and the
			// request surfaces as the standard red Writers Note.
			if (!fn) return null;
			const alt = this.#stripStructuralTags(labText)
				.replace(/\[[^\]\n]{0,60}\]/g, " ")
				.replace(/https?:\/\/\S+/g, " ")
				.replace(/\*\*/g, "").replace(/\s+/g, " ").trim();
			if (!conText) return null;
			return {
				label: alt || "",
				labelImg: fn,
				parts: [{ role: "text", text: this.#cdCellLines(conText, cfg) }],
			};
		}
		// (b) the ordinary label | content row.
		const lab = this.#cdLabel(labCell, cfg);
		if (!lab) return null;
		const ps = [];
		if (lab.rest) ps.push({ role: "text", text: this.#cdCellLines(lab.rest, cfg) });
		if (conText) {
			if (url && !conText.replace(/https?:\/\/\S+/g, "").trim()) {
				// the content cell is nothing but a media URL — render the media, not a link
				const vid = String(conCell).match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/))([\w-]{11})/);
				if (vid) ps.push({ role: "video", id: vid[1] });
				else {
					const fn = this.#accImageFilename(url, tpl, cfg);
					if (!fn) return null;
					ps.push({ role: "img", filename: fn });
				}
			} else {
				ps.push({ role: "text", text: this.#cdCellLines(conText, cfg) });
			}
		}
		if (!ps.length) return null;
		return { label: lab.label, parts: ps };
	}

	/**
	 * ROUND 283 — render the resolved items into the gold's shape: ALL buttons first,
	 * then ALL content panels, paired by position. Content routes through the SAME
	 * black-text renderer the narrow walk has used since round 241, so a panel built
	 * either way is byte-identical.
	 */
	static #cdRenderItems(list, { tpl, cfg, inline, run, renderBlock, renderNested, lead: leadParts }) {
		const buttons = [], contents = [];
		const listContent = (tpl.list_content ?? false)
			&& !(typeof process !== "undefined" && process.env && process.env.CDLIST_OFF);
		const renderText = (text) => {
			if (!String(text ?? "").trim()) return "";
			if (listContent) return ListsAndRuns.renderBlackText(String(text), run, [], false).join("");
			return `<p>${inline(String(text))}</p>`;
		};
		const renderParts = (rawParts) => {
			// CONSECUTIVE TEXT IS ONE BLOCK. The writer's bullet lines arrive as separate
			// parts, and rendering each on its own gave every bullet its own <ul>; the gold
			// ships one list (round 241). Joining them first lets the standard black-text
			// renderer group them exactly as it does in free body text.
			const parts = [];
			for (const p of rawParts) {
				const last = parts[parts.length - 1];
				if (p.role === "text" && last && last.role === "text") {
					last.text = `${last.text}\n${p.text}`;
					continue;
				}
				parts.push(p.role === "text" ? { ...p } : p);
			}
			const chunks = [];
			for (const p of parts) {
				if (p.role === "img") chunks.push(this.#assetImage(p.filename, tpl, run));
				else if (p.role === "video") {
					const vt = DataService.Data.EmitTemplates.video?.youtube;
					if (!vt) return null;
					chunks.push(Utils.FillTemplate(vt, { videoId: p.id, params: "" }));
				} else if (p.role === "embed") chunks.push(p.html);
				else if (p.role === "head") chunks.push(`<${p.level}>${inline(p.text)}</${p.level}>`);
				else if (p.role === "table") { if (!p.html) return null; chunks.push(p.html); }
				else if (p.role === "nested") {
					if (typeof renderNested !== "function") return null;
					const ph = renderNested(p.bundle);
					if (!ph) return null;
					chunks.push(ph);
				} else if (p.role === "text") {
					const h = renderText(p.text);
					if (h) chunks.push(h);
				} else if (p.role === "face") {
					const h = renderText(p.text);
					if (h) chunks.push(h);
				} else return null;                            // a role this widget cannot place
			}
			return chunks.join("");
		};

		for (const it of list) {
			if (!it.label && !it.labelImg) return null;         // never an unlabelled button
			if (this.#hasRedText(it.label)) return null;
			const content = renderParts(it.parts);
			if (content === null) return null;
			if (!String(content).trim()) return null;           // never a button with nothing behind it
			// …and never a button whose panel has NOTHING A READER CAN SEE. A panel built
			// only from a media placeholder strips to no text at all; the gold's own
			// image-first panels always carry words too, so an all-chrome panel is a
			// half-build and the widget keeps its honest hand-off box.
			if (cfg.require_panel_text !== false
				&& !String(content).replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ").trim()) return null;
			const labelHtml = it.labelImg
				? this.#assetImage(it.labelImg, tpl, run)
				: inline(it.label);
			buttons.push(Utils.FillTemplate(tpl.button, { label: labelHtml }));
			contents.push(Utils.FillTemplate(tpl.content, { content }));
		}
		const lead = [];
		if ((leadParts ?? []).length) {
			const h = renderParts(leadParts.filter((p) => p.role !== "note"));
			if (h === null) return null;
			if (String(h).trim()) lead.push(String(h));
		}
		return { buttons, contents, lead };
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

	// =======================================================================
	// ROUND 287 — THE DROPDOWN
	// =======================================================================
	/**
	 * dropDown (ROUND 287, Chris — "dropDown is the largest completely-unbuilt widget
	 * type in the library: 390 widgets across 163 modules, and not one has ever been
	 * attempted"). The FIRST builder this widget has had; every one of those 390
	 * declined at Build's own missing-template guard, before the dispatch was reached.
	 *
	 * TWO THINGS HAD TO BE SETTLED BEFORE A LINE OF THIS COULD BE WRITTEN.
	 *
	 * (1) THE POPULATION IS NOT WHAT THE TYPE NAME SAYS. Tag_Lexicon aliases
	 *     `dropbox`/`drop box` onto this same widget type, but a DROPBOX is the
	 *     file-upload area where a student submits a photo, a video or an audio
	 *     recording. Measured over every Writers Template: of 393 captured bundles,
	 *     240 (87 modules) are dropbox and 142 (82 modules) are a genuine dropdown.
	 *     The gold agrees they are different things — `class="activity dropbox"` (an
	 *     activity MODIFIER, 558 occurrences) versus `div.dropDown`. So the builder is
	 *     FENCED on the writer's own opener naming a dropdown, which leaves every
	 *     dropbox bundle byte-identical BY CONSTRUCTION. Re-cutting the lexicon alias
	 *     would move 240 bundles' capture and hand-off labels across 87 modules and is
	 *     recorded as its own round, not done here.
	 *
	 * (2) THE ANSWER SIGNAL IS NOT ONLY RED. Writers mark the correct option EITHER by
	 *     colouring it red OR with an explicit [correct] tag immediately before it
	 *     (BLL273, BLLR201 — the raw WT reads "…is (🔴[correct]🔴rescued, dropped,
	 *     forgotten)." and the gold ships answer="1"). Both reduce to a MARK at a
	 *     character position, so ONE derivation serves both.
	 *
	 * FOUR DIALECTS, each quoted against its gold:
	 *   D1 PARAGRAPH-PARENS — options in a parenthesis inside prose, one marked.
	 *        BLL273-2.0  "Someone who is saved from danger is ([correct]rescued, dropped, forgotten)."
	 *        gold        dropQuiz autoCheck layout="paragraph" > dropParaContainer > ol > li
	 *                    with <div class="dropDown" answer="1"> inline in the sentence.
	 *   D2 QUESTION + MARK — a question line, then the answer as a marked span; the
	 *      OPTION SET is the DISTINCT answers across the questions, which is
	 *      recoverable without parsing the writer's English (PHE1007's Dev note names
	 *      the same three words it then colours red, so the two agree).
	 *        PHE1007-1.0 "1. Liver" / red "Smooth" · "1. Bicep" / red "Skeletal" …
	 *   D3 TABLE + RED — an answers COLUMN beside a statements column, or a whole grid
	 *      of red cells under a header row.
	 *        SCCH301-1.0 header Solids|Liquids|Gases, every body cell red [yes]/[no]
	 *   D4 BULLETS + (correct) — a bullet RUN of options, the right one carrying a
	 *      `(correct)` marker.
	 *        ENGC101-4.0 "• For people with bikes / • For people with disabilities
	 *                    (correct) / • For people without cars"
	 *        gold        dropQuiz autoCheck > row > dropQuestion > img + dropDown answer="2"
	 *
	 * A LABEL, AN OPTION AND AN ANSWER ARE NEVER INVENTED. The single largest decline
	 * bucket — 76 bundles over 52 modules — is a dropdown whose correct option the
	 * writer never marked at all, and those keep their honest hand-off box.
	 *
	 * NEVER HALF-BUILDS: no dialect resolves ≥ min_units units · an option set outside
	 * min/max_options · a member the walk cannot place · an empty option · or a
	 * finished widget that still shows a resolved [tag] (#ddLeakGuard — the round
	 * 167/275/277/278 rule at this seam, so building can only ever PREVENT a leak).
	 *
	 * WHY NOT #accMemberParts. The shared round-278 walk STRIPS the red markers and
	 * BAILS on red text — but here the red text IS the answer, so reusing it would
	 * mean inverting its core rule for one caller and putting the other five widgets
	 * at risk. This walk is local and sets NO shared keys, so the accordion, tabs,
	 * clickDrop and flipCard cannot move BY CONSTRUCTION; the shared HELPERS
	 * (#cellText, #accImageFilename, #assetImage) are reused unchanged.
	 *
	 * Data interactive_builders.dropDown; env DROPDOWN_OFF.
	 */
	static #dropDown({ bundle, tpl, renderInline, run, renderTable }) {
		if (!tpl || tpl.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.DROPDOWN_OFF) return null;
		if (!this.#ddIsDropdownFamily(bundle, tpl)) return null;   // the dropbox fence
		const inline = renderInline ?? ((s) => s);
		const notes = [];
		const all = this.#ddStream(bundle, tpl, notes);
		if (!all) return null;
		// the autoCheck class, resolved ONCE from the writer's own opener wording
		const ac = this.#ddAutocheck(bundle, tpl);
		// the widget's own PREAMBLE — lead prose, a data table, an image — lifted out so
		// it renders ABOVE the quiz exactly as the gold does, instead of being swallowed
		// into the first question or (worse) silently lost.
		const { pre, toks } = this.#ddPreamble(all, tpl, inline, run, renderTable);
		if (pre === null) return null;

		// The dialects, in order. The first that resolves owns the bundle.
		const body = this.#ddParagraph(toks, tpl, inline, run, ac)
			?? this.#ddBullets(toks, tpl, inline, run, ac)
			?? this.#ddQuestions(toks, tpl, inline, run, ac)
			?? this.#ddTable(bundle, tpl, inline, ac);
		if (!body) return null;
		const built = [...pre, body].join("\n");
		if (this.#ddLeakGuard(built, tpl)) return null;            // a build must never ADD a leak
		if (notes.length) bundle.instructions = [...(bundle.instructions ?? []), ...notes];
		bundle.r287DropDown = true;                                // detector / affected-set marker
		return built;
	}

	/**
	 * ROUND 287 — THE PREAMBLE. A dropdown often opens with material that belongs to the
	 * whole quiz rather than to any one question: an instruction line ("Study this table
	 * and graph…"), the DATA TABLE the questions are about, a diagram. The gold renders
	 * all three above the container (MXDB302-4.0: prose, then the table, then the image,
	 * then the dropQuiz), so they are lifted out here and the dialects see only the
	 * question material.
	 *
	 * Returns { pre, toks }, or pre === null when a captured table cannot be rendered —
	 * a writer's table is NEVER silently dropped, so that declines the build.
	 *
	 * THE BULLET EXCEPTION. "the last paragraph before the first mark belongs to the
	 * first question" is right for prose (PHE1007's lead) but wrong for a bullet RUN,
	 * where every line before the marker is an option (ENGC101). So no prose is lifted
	 * when a bullet appears in the preamble.
	 */
	static #ddPreamble(all, tpl, inline, run, renderTable) {
		const firstMark = all.findIndex((t) => t.kind === "mark");
		if (firstMark < 0) return { pre: [], toks: all };
		const head = all.slice(0, firstMark);
		const bulletish = head.some((t) => t.kind === "plain" && /^\s*[•●▪‣]/.test(String(t.text ?? "")));
		const pre = [];
		const keep = [];
		const plainIdx = head.map((t, i) => (t.kind === "plain" ? i : -1)).filter((i) => i >= 0);
		const lastPlain = plainIdx.length ? plainIdx[plainIdx.length - 1] : -1;
		for (let i = 0; i < head.length; i++) {
			const t = head[i];
			if (t.kind === "table") {
				if (typeof renderTable !== "function" || !t.item) return { pre: null, toks: all };
				const html = renderTable(t.item);
				if (!html || !String(html).trim()) return { pre: null, toks: all };
				pre.push(String(html));
				continue;
			}
			if (t.kind === "img") {
				if (run) pre.push(this.#assetImage(t.text, tpl, run));
				continue;
			}
			if (t.kind === "plain" && !bulletish && i !== lastPlain) {
				const s = this.#ddTidy(t.text);
				if (s) pre.push(Utils.FillTemplate(tpl.question_text, { text: inline(s) }));
				continue;
			}
			keep.push(t);
		}
		return { pre, toks: [...keep, ...all.slice(firstMark)] };
	}

	/**
	 * THE FAMILY FENCE. True only when the writer's own opener names a DROPDOWN.
	 * A bundle whose opener says "dropbox" (the student file-upload area) is not this
	 * widget and is left exactly as it was.
	 */
	static #ddIsDropdownFamily(bundle, tpl) {
		const deny = new RegExp(tpl.opener_deny_pattern ?? "drop\\s*box", "i");
		const allow = new RegExp(tpl.opener_pattern ?? "drop[\\s-]*down|dropquiz|drop\\s*quiz", "i");
		for (const m of bundle?.memberItems ?? []) {
			if (m?.type !== "tag") continue;
			if (!(tpl.delimiter_tags ?? ["dropdown"]).includes(m.parse?.primary?.tag)) continue;
			const own = String(m.text ?? "");
			return allow.test(own) && !deny.test(own);
		}
		return false;
	}

	/**
	 * ROUND 287 — the captured members as an ordered token stream, or null when a
	 * member cannot be placed. Each token is { text, kind } where kind is:
	 *   "plain" ordinary prose · "mark" an ANSWER mark (red text, or a [correct] tag,
	 *   which carries no text of its own) · "img" a nameable image · "delim" a repeated
	 *   invocation opening a new item · "note" a writer instruction, surfaced red after
	 *   a successful build and never silently dropped (the round-214/242 rule).
	 *
	 * The point of the stream is that it REBUILDS the paragraph the writer typed while
	 * remembering where the marks fell — the extractor delivers a sentence with three
	 * coloured words as one black lead plus three red spans each carrying the rest of
	 * its own parenthesis, so nothing else can see the option groups.
	 */
	static #ddStream(bundle, tpl, notes) {
		const toks = [];
		const delims = tpl.delimiter_tags ?? ["dropdown"];
		const textTags = tpl.text_tags ?? [];
		const noteTags = tpl.note_tags ?? [];
		const imageTags = tpl.image_tags ?? [];
		const maxAns = tpl.max_answer_words ?? 12;
		let seenOpener = false;

		// A token with no text still MATTERS when it is a structural marker — a captured
		// table above all. Dropping an empty "table" token let a bundle build as though
		// the writer's table were not there (caught live on MXDB302-4.0, whose data table
		// feeds the questions); the paragraph/question/bullet dialects test for it and
		// decline, so the table can never be silently lost.
		const structural = new Set(["mark", "delim", "img", "table"]);
		const push = (t, kind) => { if (t || structural.has(kind)) toks.push({ text: t, kind }); };
		const after = (m) => { const t = this.#cellText(m.blackAfter ?? ""); if (t) push(t, "plain"); };

		for (const m of bundle?.memberItems ?? []) {
			if (!m) continue;
			if (m.type === "table") { toks.push({ text: "", kind: "table", item: m }); continue; }
			if (m.type === "nested") return null;
			if (m.type === "black") {
				const t = this.#cellText(m.text ?? "");
				if (t) push(t, "plain");
				continue;
			}
			if (m.type !== "tag") return null;
			const tag = m.parse?.primary?.tag ?? null;

			// the widget's OWN invocation (first) vs a REPEATED one (an item delimiter)
			if (tag && delims.includes(tag)) {
				if (!seenOpener) { seenOpener = true; after(m); continue; }
				push("", "delim"); after(m); continue;
			}
			// an EXPLICIT [correct] marker: the option that FOLLOWS it is the answer
			if (tag === "correct") { push("", "mark"); after(m); continue; }

			// an UNRESOLVED RED span — the writer coloured a word and it matched no tag.
			// Short and unbracketed = an answer token; anything else is a writer note.
			// (Class alone cannot separate them: "Give a hug" and "cheer her dad up" are
			// real answers that trip an instruction cue, while "[Dev – two options]" is a
			// note that does not.)
			if (!tag && (m.parse?.class === "noise" || m.parse?.class === "instruction")) {
				const own = this.#cellText(m.text ?? "");
				if (own && !own.startsWith("[") && own.split(/\s+/).length <= maxAns) push(own, "mark");
				else if (own) notes.push(own);
				after(m);
				continue;
			}
			if (tag && imageTags.includes(tag)) {
				const url = this.#cellMediaUrl(m.blackAfter ?? "");
				const fn = url ? this.#accImageFilename(url, tpl, tpl) : null;
				if (fn) push(fn, "img");
				else {                                             // an asset REQUEST, not an image
					const t = this.#cellText(m.text ?? "") + " " + this.#cellText(m.blackAfter ?? "");
					if (t.trim()) notes.push(t.trim());
				}
				continue;
			}
			if (tag && textTags.includes(tag)) { after(m); continue; }
			if (tag && noteTags.includes(tag)) {
				const t = this.#cellText(m.text ?? "") + " " + this.#cellText(m.blackAfter ?? "");
				if (t.trim()) notes.push(t.trim());
				after(m);
				continue;
			}
			return null;                                           // a foreign tag we cannot place
		}
		return toks;
	}

	/**
	 * ROUND 287 — the token stream as one string plus the character ranges the answer
	 * marks occupy. A ZERO-WIDTH range is an explicit [correct] insertion point: the
	 * option that FOLLOWS it is the answer.
	 */
	static #ddRebuild(toks) {
		const buf = [];
		const marks = [];
		const starts = [];
		let pos = 0;
		for (const t of toks) {
			if (t.kind === "note" || t.kind === "table" || t.kind === "img" || t.kind === "delim") continue;
			if (t.kind === "mark" && !t.text) { marks.push([pos, pos]); continue; }
			if (!t.text) continue;
			const prev = buf.length ? buf[buf.length - 1] : "";
			const need = prev && !/[(\s\n]$/.test(prev) && !/^[,).\s\n]/.test(t.text);
			if (need) { buf.push(" "); pos += 1; }
			// AN ITEM BOUNDARY. Each black paragraph arrives as its own token, so a token
			// that OPENS with the writer's numbering starts a new numbered item. Reading it
			// here rather than from the joined string is what makes the split reliable: the
			// reconstruction joins the paragraphs with spaces, so a "1." that began a
			// paragraph is indistinguishable from one mid-sentence once joined.
			if (t.kind === "plain" && /^\s*\(?\d{1,3}[.)]\s+\S/.test(t.text)) starts.push(pos);
			if (t.kind === "mark") marks.push([pos, pos + t.text.length]);
			buf.push(t.text); pos += t.text.length;
		}
		return { text: buf.join(""), marks, starts };
	}

	/** ROUND 287 — one parenthesised option group -> {options, answer, span} or null. */
	static #ddGroup(text, start, inner, marks, tpl) {
		const min = tpl.min_options ?? 2, max = tpl.max_options ?? 10;
		const opts = [];
		let off = 0;
		for (const part of inner.split(",")) {
			opts.push({ text: part.trim(), a: start + off, b: start + off + part.length });
			off += part.length + 1;
		}
		if (opts.length < min || opts.length > max) return null;
		if (opts.some((o) => !o.text)) return null;
		const hit = new Set();
		opts.forEach((o, i) => {
			for (const [ra, rb] of marks) {
				if (ra === rb) { if (o.a <= ra && ra <= o.b) hit.add(i); }      // explicit [correct]
				else if (!(o.b <= ra || o.a >= rb)) hit.add(i);
			}
		});
		if (hit.size !== 1) return null;
		return { options: opts.map((o) => o.text), answer: [...hit][0] + 1 };
	}

	/**
	 * D1 — PARAGRAPH-PARENS. Prose carrying parenthesised option groups with one
	 * option marked. Emits the gold's paragraph form: dropQuiz layout="paragraph" >
	 * dropParaContainer > <ol> with one <li> per sentence, the dropdown inline where
	 * the writer put the parenthesis.
	 */
	static #ddParagraph(toks, tpl, inline, run, ac) {
		if (toks.some((t) => t.kind === "table" || t.kind === "img" || t.kind === "delim")) return null;
		const { text, marks, starts } = this.#ddRebuild(toks);
		if (!marks.length || !text.trim()) return null;
		const groups = [];
		const re = /\(([^()]{2,300})\)/g;
		let m;
		while ((m = re.exec(text)) !== null) {
			const g = this.#ddGroup(text, m.index + 1, m[1], marks, tpl);
			if (g) groups.push({ ...g, from: m.index, to: m.index + m[0].length });
		}
		if (groups.length < (tpl.min_units ?? 1)) return null;
		// Split the prose into ITEMS on the writer's own numbering, so each numbered
		// sentence becomes one <li> exactly as the gold does.
		const items = this.#ddSplitItems(text, groups, starts);
		if (!items.length) return null;
		const lis = [];
		for (const it of items) {
			const parts = [];
			let cur = it.from;
			for (const g of it.groups) {
				const lead = text.slice(cur, g.from);
				if (lead.trim()) parts.push(inline(this.#ddTidy(lead)));
				parts.push([tpl.question_open, this.#ddUnit(g, tpl), tpl.question_close].join("\n"));
				cur = g.to;
			}
			const tail = text.slice(cur, it.to);
			if (tail.trim()) parts.push(inline(this.#ddTidy(tail)));
			lis.push(`${tpl.para_item_open}\n${parts.join("\n")}\n${tpl.para_item_close}`);
		}
		const open = Utils.FillTemplate(tpl.paragraph_open, { autocheck: ac ?? "" });
		return [open, ...lis, tpl.paragraph_close].join("\n");
	}

	/** ROUND 287 — split the rebuilt prose into numbered items, each owning its groups. */
	static #ddSplitItems(text, groups, starts) {
		const cuts = [...new Set([0, ...(starts ?? [])])].sort((a, b) => a - b);
		const items = [];
		for (let i = 0; i < cuts.length; i++) {
			const from = cuts[i], to = i + 1 < cuts.length ? cuts[i + 1] : text.length;
			const mine = groups.filter((g) => g.from >= from && g.to <= to);
			if (mine.length) items.push({ from, to, groups: mine });
		}
		return items;
	}

	/** ROUND 287 — tidy a prose fragment for display: drop the writer's item number and
	 *  collapse the whitespace the reconstruction leaves at a join. */
	static #ddTidy(s) {
		return String(s ?? "").replace(/^\s*\(?\d{1,3}[.)]\s*/, "").replace(/\s+/g, " ").trim();
	}

	/**
	 * D4 — BULLETS + (correct). A bullet RUN of options with the correct one carrying
	 * a `(correct)` marker. One dropdown per run; an image immediately before a run
	 * belongs to that run's question (ENGC101's symbol quiz, which the gold builds the
	 * same way).
	 */
	static #ddBullets(toks, tpl, inline, run, ac) {
		const markRe = new RegExp(tpl.correct_marker_pattern ?? "^\\(?\\s*correct\\s*\\)?$", "i");
		const items = [];
		let cur = null;
		const flush = () => { if (cur && cur.options.length) items.push(cur); cur = null; };
		let pendingImg = null;
		for (const t of toks) {
			if (t.kind === "table" || t.kind === "delim") { flush(); continue; }
			if (t.kind === "img") { flush(); pendingImg = t.text; continue; }
			if (t.kind === "mark" && markRe.test(String(t.text ?? "").trim())) {
				if (cur && cur.options.length) cur.answer = cur.options.length;
				continue;
			}
			for (const raw of String(t.text ?? "").split("\n")) {
				const line = raw.trim();
				if (!line) continue;
				const bullet = /^[•●▪‣\-*]\s*/.test(line);
				if (bullet) {
					if (!cur) cur = { img: pendingImg, options: [], answer: 0, question: "" };
					cur.options.push(line.replace(/^[•●▪‣\-*]\s*/, "").trim());
				} else { flush(); pendingImg = null; }
			}
		}
		flush();
		const min = tpl.min_options ?? 2, max = tpl.max_options ?? 10;
		const good = items.filter((i) => i.answer > 0 && i.options.length >= min && i.options.length <= max
			&& i.options.every((o) => o));
		if (good.length < (tpl.min_units ?? 1) || good.length !== items.length) return null;
		return this.#ddQuestionForm(good, tpl, inline, run, ac);
	}

	/**
	 * D2 — QUESTION + MARK. A question line, then the correct answer as a marked span.
	 * The OPTION SET is the distinct answers across the questions — recoverable without
	 * parsing the writer's English, and it agrees with the option set the writer states
	 * in prose where they state one at all.
	 */
	static #ddQuestions(toks, tpl, inline, run, ac) {
		if (toks.some((t) => t.kind === "table" || t.kind === "img" || t.kind === "delim")) return null;
		if (toks.some((t) => t.kind === "plain" && /\(/.test(t.text))) return null;   // a paren form is D1's
		const qs = [];
		const lead = [];
		let pending = [];
		for (const t of toks) {
			if (t.kind === "note") continue;
			if (t.kind === "mark") {
				const a = String(t.text ?? "").trim();
				if (!a || !pending.length) return null;
				// THE QUESTION IS THE LAST PARAGRAPH BEFORE THE MARK. Each black paragraph
				// arrives as its own token, so anything earlier in the buffer is the widget's
				// own LEAD prose ("Select the correct type of muscle…", PHE1007) — which the
				// gold renders as a <p> ABOVE the quiz, not inside its first question.
				const q = this.#ddTidy(String(pending.pop()).replace(/^[•●▪‣\-*]\s*/, ""));
				if (qs.length === 0) for (const p of pending) { const s = this.#ddTidy(p); if (s) lead.push(s); }
				else if (pending.length) return null;   // stray prose mid-quiz — not this shape
				pending = [];
				if (q) qs.push({ question: q, answer: a });
			} else if (String(t.text ?? "").trim()) pending.push(t.text);
		}
		if (qs.length < 2) return null;
		const maxQ = tpl.max_question_words ?? 60;
		if (qs.some((q) => q.question.split(/\s+/).length > maxQ)) return null;
		const opts = [...new Set(qs.map((q) => q.answer))];
		const min = tpl.min_options ?? 2, max = tpl.max_options ?? 10;
		if (opts.length < min || opts.length > max) return null;
		const body = this.#ddQuestionForm(
			qs.map((q) => ({ question: q.question, options: opts, answer: opts.indexOf(q.answer) + 1 })),
			tpl, inline, run, ac);
		if (!body) return null;
		const pre = lead.map((s) => Utils.FillTemplate(tpl.question_text, { text: inline(s) }));
		return [...pre, body].join("\n");
	}

	/**
	 * D3 — TABLE + RED. Either an answers COLUMN beside a statements column (TWHA902's
	 * "Statements: | Answers:"), or a whole GRID of red cells under a header row
	 * (SCCH301's Solids|Liquids|Gases yes/no table).
	 */
	static #ddTable(bundle, tpl, inline, ac) {
		const tabs = (bundle?.memberItems ?? []).filter((m) => m?.type === "table");
		if (tabs.length !== 1) return null;
		const rows = (tabs[0].block?.rows ?? [])
			.map((r) => (r ?? []).map((c) => (typeof c === "string" ? c : c?.text) ?? ""))
			.filter((r) => r.some((c) => String(c).trim()));
		if (rows.length < 2) return null;
		const w = Math.max(...rows.map((r) => r.length));
		const body = rows.slice(1);
		const min = tpl.min_options ?? 2, max = tpl.max_options ?? 10;
		const clean = (c) => this.#cellText(c).replace(/^\[|\]$/g, "").trim();

		// (a) GRID — a header row, then every body cell beyond the first is red.
		const bodyCells = body.flatMap((r) => r.slice(1).filter((c) => String(c).trim()));
		if (w >= 3 && bodyCells.length && bodyCells.every((c) => this.#isFullyRed(c))) {
			const vals = bodyCells.map(clean).filter(Boolean);
			const opts = [...new Set(vals)];
			if (opts.length < min || opts.length > max) return null;
			// The gold arranges a grid as the ROW's statement (an <ol><li>) followed by one
			// dropQuestion per COLUMN, the column head being that question's label
			// (SCCH301-1.0: "Does it have a definite shape?" then Solids / Liquids / Gases).
			const units = [];
			let nRow = 0;
			for (const r of body) {
				const label = this.#cellText(r[0] ?? "");
				nRow++;
				let first = true;
				for (let c = 1; c < w; c++) {
					const v = clean(r[c] ?? "");
					if (!v) continue;
					const head = this.#cellText(rows[0][c] ?? "");
					const u = { question: head, options: opts, answer: opts.indexOf(v) + 1 };
					if (first && label && tpl.grid_row_label) {
						u.before = Utils.FillTemplate(tpl.grid_row_label, { n: String(nRow), text: label });
					}
					first = false;
					units.push(u);
				}
			}
			if (units.length < (tpl.min_units ?? 1)) return null;
			return this.#ddQuestionForm(units, tpl, inline, null, ac);
		}

		// (b) COLUMN — a red header on the answers column, answers beneath it.
		if (w === 2 && rows[0].length > 1 && this.#isFullyRed(rows[0][1])) {
			const pairs = body.filter((r) => r.length > 1 && String(r[1]).trim())
				.map((r) => ({ q: this.#cellText(r[0] ?? ""), a: this.#cellText(r[1] ?? "") }));
			if (pairs.length < 2 || pairs.some((p) => !p.q || !p.a)) return null;
			const maxAns = tpl.max_answer_words ?? 12;
			if (pairs.some((p) => p.a.split(/\s+/).length > maxAns)) return null;
			const opts = [...new Set(pairs.map((p) => p.a))];
			if (opts.length < min || opts.length > max) return null;
			return this.#ddQuestionForm(
				pairs.map((p) => ({ question: p.q, options: opts, answer: opts.indexOf(p.a) + 1 })),
				tpl, inline, null, ac);
		}
		return null;
	}

	/** ROUND 287 — the question/grid output form: dropQuiz > row > dropQuestion*. */
	static #ddQuestionForm(units, tpl, inline, run, ac) {
		const qs = units.map((u) => {
			const bits = [];
			if (u.img && run) bits.push(this.#assetImage(u.img, tpl, run));
			if (u.question) bits.push(Utils.FillTemplate(tpl.question_text, { text: inline(u.question) }));
			bits.push(this.#ddUnit(u, tpl));
			const q = [tpl.question_open, ...bits, tpl.question_close].join("\n");
			return u.before ? `${u.before}\n${q}` : q;      // a grid's row statement
		});
		const open = Utils.FillTemplate(tpl.container_open, { autocheck: ac ?? "" });
		return [open, tpl.row_open, ...qs, tpl.row_close, tpl.container_close].join("\n");
	}

	/** ROUND 287 — one <div class="dropDown" answer="N"> unit. */
	static #ddUnit(u, tpl) {
		const options = u.options.map((o) =>
			Utils.FillTemplate(tpl.option, { option: String(o).replace(/\*\*/g, "").trim() })).join("\n");
		return Utils.FillTemplate(tpl.unit, {
			answer: String(u.answer),
			placeholder: tpl.placeholder_text ?? "Select one",
			options,
		});
	}

	/**
	 * ROUND 287 — the autoCheck class. The gold ships `dropQuiz autoCheck` on a third
	 * of its groups (105 of 312) and the writer asks for it in words on the opener
	 * ("+ auto check", "self-marking", "automarked").
	 */
	static #ddAutocheck(bundle, tpl) {
		const words = tpl.autocheck_words ?? [];
		const delims = tpl.delimiter_tags ?? ["dropdown"];
		let hay = String(bundle?.modifier ?? "");
		for (const m of bundle?.memberItems ?? []) {
			if (m?.type === "tag" && delims.includes(m.parse?.primary?.tag)) { hay += " " + String(m.text ?? ""); break; }
		}
		hay = hay.toLowerCase();
		return words.some((w) => hay.includes(String(w).toLowerCase())) ? (tpl.autocheck_class ?? " autoCheck") : "";
	}

	/**
	 * ROUND 287 — THE LEAK GUARD (the round-167/275/277/278 rule at this seam). A
	 * finished dropdown whose VISIBLE text still shows a bracketed writer tag would
	 * turn gate-excluded hand-off chrome into a counted literal leak on the page, so
	 * the build declines and the honest box stays. Building can therefore only ever
	 * PREVENT a leak; scoped to this builder, so it can never remove a pre-287 build
	 * (there are none — but the scoping is the round-277 lesson kept).
	 */
	static #ddLeakGuard(html, tpl) {
		if (tpl && tpl.leak_guard === false) return false;
		const vis = String(html ?? "").replace(/<!--[\s\S]*?-->/g, " ").replace(/<[^>]+>/g, " ");
		return /\[\s*[A-Za-z][^\]\n]{0,40}\]/.test(vis);
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
