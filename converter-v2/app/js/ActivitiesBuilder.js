/**
 * ActivitiesBuilder.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Builds the ACTIVITY BOX — the one container element in the whole output
 * that legitimately spans MULTIPLE writer tags at once. An `[Activity]` tag
 * in the Writers Template opens a box whose members keep flowing in (body
 * text, images, widgets, headings…) until an `[end activity]` tag or some
 * other structural terminator closes it, so — unlike almost everything
 * else this converter emits — an activity box can't be built by looking at
 * one tag in isolation; it needs to track state across a whole run of
 * content. This file is what actually builds that box: its outer wrapper
 * classes, its `number=` id attribute, and whether it gets the
 * `.interactive` CSS class that marks it as a hands-on task rather than a
 * plain read-and-do activity. Three statics, and deliberately ZERO stored
 * fields of its own:
 *
 *   - activityOpen   THE OPENER — called at the moment an `[Activity]` tag
 *         is encountered. Works out the box's modifier classes, decides
 *         whether to force the `.interactive` class on based on which
 *         widget TYPE the activity owns, renumbers a bare-digit activity
 *         id into the human's `{lessonNumber}{letter}` form (env toggle
 *         ACTLETTER_OFF), builds the special "supervisor note" box variant
 *         when a supervisor note immediately follows the opener, and
 *         promotes a standalone activity's first line of text into a real
 *         `<h#>` title heading (env toggle ACTTITLE_OFF).
 *   - activityInteractivePostpass   A DOCUMENT-LEVEL CLEAN-UP PASS that
 *         runs once the whole page's HTML has already been assembled: it
 *         finds any activity box that OWNS a genuinely interactive-task
 *         widget (as opposed to a passive display widget) but somehow
 *         didn't get the `.interactive` class at emit time, and adds it
 *         retroactively (env toggle ACTINT_OFF; data
 *         body_region.activity_interactive_postpass).
 *   - containerModifiers   THE MODIFIER-CLASS RESOLVER shared logic: reads
 *         a tag's leftover, un-recognised text and sorts each word into
 *         either "this is a documented modifier class, apply it" or "this
 *         is an undocumented note, flag it visibly at the box instead of
 *         silently dropping it." Deliberately made PUBLIC (not private) so
 *         the plain callout-box emitter elsewhere in the converter can
 *         reuse the exact same logic instead of duplicating it.
 *
 * WHY SEPARATE FILE:
 * These three methods read DataService.Data (the shared data-driven
 * config, as everywhere) and NONE of the main content-converter's own
 * running state. The one piece of state they DO need — which lesson the
 * current page belongs to, and how many activities have already been
 * numbered within that lesson (so sequential lettering A, B, C… stays
 * correct) — is deliberately kept OUTSIDE this file, as private fields on
 * the main converter (which sets them up once per page), and is simply
 * passed IN to activityOpen as two ordinary trailing arguments. Similarly,
 * the DECISION about whether to even look ahead for a supervisor note, or
 * whether a bilingual-module activity bundle should route through here at
 * all, is made by the calling code before it ever reaches this file — this
 * file only ever BUILDS the box once told to.
 *
 * JARGON, EXPLAINED:
 *   - "activity box"  the bordered container the site renders around a
 *     hands-on task or exercise, built from an `[Activity]` tag.
 *   - "supervisor note"  a short instruction aimed at whoever is
 *     supervising the learner (e.g. a parent), rendered as its own small
 *     panel that can appear attached to an activity box.
 *   - ".interactive"  the CSS class (and matching site icon) that tells the
 *     reader "this activity expects you to actually click/drag/type
 *     something," as opposed to a plain instructional activity.
 * ===========================================================================
 */

class ActivitiesBuilder {

	/**
	 * A DOCUMENT-LEVEL "catch the ones we missed" pass for the
	 * `.interactive` class on activity boxes — runs over the WHOLE
	 * assembled page's HTML text, after everything else has already been
	 * emitted.
	 *
	 * WHY THIS EXISTS: activityOpen (below) only knows to add the
	 * `.interactive` class when the activity box's OWN bundle is a widget
	 * of an interactive-task type. But sometimes the writer structures
	 * things so the interactive-task widget is captured as a SEPARATE,
	 * NESTED placeholder INSIDE a plain activity box, rather than being
	 * the activity's own bundle — in that case activityOpen has no way to
	 * know about it at the moment the box opens, and the activity would
	 * otherwise ship without the `.interactive` class even though it truly
	 * contains an interactive task.
	 *
	 * HOW IT WORKS: scans the finished HTML text for every
	 * `<div class="activity…">` that ISN'T already marked `.interactive`,
	 * finds that div's matching closing `</div>` (tracking nesting depth
	 * so it can't get confused by divs inside the activity), and checks
	 * whether anywhere inside that span there's a cv2-interactive
	 * placeholder marker declaring a widget TYPE that's in the data list
	 * activity_wrapper.interactive_widget_types (the same list activityOpen
	 * itself checks against for its own bundle) — a widget can declare
	 * MULTIPLE types at once (e.g. "carousel + modal"), and ANY one of them
	 * matching is enough. When it finds a match, it inserts the word
	 * " interactive" directly into that div's class attribute.
	 *
	 * WHY THIS IS SAFE TO ADD LATER: the structural-comparison gates that
	 * compare Claude's output shape to the human build's shape don't look
	 * at CSS class names at all for activity boxes — only the presence of
	 * the box itself matters to them — so adding this class here can only
	 * ever move the output CLOSER to matching the human build's visible
	 * styling, never change whether a structural comparison passes or
	 * fails. Data-flagged
	 * (body_region.activity_interactive_postpass.enabled); env toggle
	 * ACTINT_OFF reverts to leaving these activities without the class.
	 *
	 * @param {string} html - the fully assembled page HTML
	 * @returns {string} the same HTML with `.interactive` added to any activity box that needed it
	 */
	static activityInteractivePostpass(html) {
		const tpl = DataService.Data.EmitTemplates;
		const cfg = tpl.body_region?.activity_interactive_postpass;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.ACTINT_OFF) return html;
		const types = new Set(tpl.activity_wrapper?.interactive_widget_types ?? []);
		if (!types.size) return html;
		// The placeholder declares its widget type(s) as a fixed-format marker string; a
		// SINGLE activity can own MULTIPLE widget types glued together as
		// "TYPE_A + TYPE_B" (e.g. "carousel + modal" or "unclassified + dropDown"), so
		// capture the WHOLE type list from the marker and check EVERY declared type —
		// not just the first one — against the interactive-task type list.
		const markerRe = /INTERACTIVE \(un-built\) #\d+: ([\w +]+)/g;
		// depth-balanced end (index just past the matching </div>) of the div opened at `start`
		const divEnd = (start) => {
			const re = /<(\/?)div\b/gi; re.lastIndex = start;
			let depth = 0, mm;
			while ((mm = re.exec(html))) {
				depth += mm[1] ? -1 : 1;
				if (depth === 0) return re.lastIndex;
			}
			return html.length;
		};
		// activity-open class = "activity" + optional modifiers; the (\s[^"]*)? after the
		// exact word excludes "activityButton…" (checkAnswer/undo/reset buttons)
		const reOpen = /<div class="(activity)(\s[^"]*)?"/g;
		const inserts = [];
		let m;
		while ((m = reOpen.exec(html))) {
			if (/(^|\s)interactive(\s|$)/.test(m[2] || "")) continue;   // already interactive
			const seg = html.slice(m.index, divEnd(m.index));
			markerRe.lastIndex = 0;
			let owns = false, mk;
			while ((mk = markerRe.exec(seg))) { if (mk[1].split(/\s*\+\s*/).some((t) => types.has(t.trim()))) { owns = true; break; } }
			// insert right after the literal `activity` word so the class reads
			// "activity interactive{mods}" (the human's order): `<div class="`=12 + `activity`=8
			if (owns) inserts.push(m.index + 20);
		}
		if (!inserts.length) return html;
		let out = html;
		for (const pos of inserts.sort((a, b) => b - a)) out = out.slice(0, pos) + " interactive" + out.slice(pos);
		return out;
	};

	/**
	 * Resolves a container-opening tag's MODIFIER CLASSES from whatever
	 * leftover text the writer typed after the tag itself.
	 *
	 * WHY THIS IS NEEDED: a writer can type something like
	 * `[Activity supervisor-required]`, where "supervisor-required" is
	 * extra text beyond the plain `[Activity]` tag. This method decides,
	 * word by word, what to do with that leftover text — a TWO-TIER rule:
	 *   1. a word that matches a DOCUMENTED modifier class (looked up in
	 *      `map`) gets ACTIONED — its CSS class is appended to the box;
	 *   2. any word that ISN'T recognised is collected separately, and — if
	 *      there are enough of them to look like a genuine note rather than
	 *      noise — rendered as a visible flagged note attached to the box,
	 *      instead of being silently thrown away.
	 *
	 * @param {Object} it - the container-opening item, e.g. { parse: { tags: [{ remainder: "supervisor-required" }], primary: { tag: "activity" } } }
	 * @param {Object} map - word -> CSS-class-string lookup for documented modifiers
	 * @param {ConversionRun} run - the current run (needed to emit a flagged note)
	 * @returns {{modifiers: string, flags: string[]}} the resolved modifier CSS classes (as one appended string) and any flagged notes to render
	 */
	static containerModifiers(it, map, run) {
		const remainder = (it.parse.tags.map((t) => t.remainder ?? "").join(" ")).trim();
		let modifiers = "";
		const leftover = [];
		for (const word of remainder.split(/\s+/).filter(Boolean)) {
			const cls = map[word];
			if (typeof cls === "string") modifiers += cls;
			else leftover.push(word);
		}
		const flags = leftover.length >= 2
			? [NotesAndComments.redFlag(`${it.parse.primary.tag} note: ${leftover.join(" ")}`, run, "cs")] : [];
		return { modifiers, flags };
	};

	/**
	 * Opens the ACTIVITY BOX — the one container in the whole converter
	 * that legitimately spans MULTIPLE tags, since its members keep
	 * flowing in until an `[end activity]` tag or some other structural
	 * terminator closes it. Because of that, this method doesn't just
	 * emit a self-contained fragment and return — it also pushes a marker
	 * onto the caller's open-container `stack` so the rest of the page
	 * emitter knows an activity is currently open and can route further
	 * content into it, until something eventually closes it back off the
	 * stack.
	 *
	 * WHAT IT DOES, IN ORDER:
	 *   1. Resolves modifier classes from the opener's leftover text
	 *      (via containerModifiers, above).
	 *   2. Forces the `.interactive` class on when the caller says this
	 *      activity owns a widget of an interactive-task type (the
	 *      per-type convention this method's caller has already worked
	 *      out — see the class-level file header for the full type list).
	 *   3. Renumbers a bare-digit activity id into the human's
	 *      `{lessonNumber}{positional letter}` form (e.g. "3" on lesson 2
	 *      becomes "2C") — but only when the writer's own id was a BARE
	 *      digit; an id the writer already gave a letter (e.g. "6B") is
	 *      trusted and left untouched, since that can encode the
	 *      activity's true position even when this converter's own
	 *      capture of the surrounding activities is incomplete.
	 *   4. When a supervisor note immediately follows this opener, builds
	 *      the special "super-content" box variant instead of the plain
	 *      one — the note gets its own panel INSIDE the box, ahead of the
	 *      activity's own title/body.
	 *   5. When this is a STANDALONE activity (not one owned by an
	 *      interactive widget bundle) and it carries its own lead-in text,
	 *      promotes that text's first line into a real heading element
	 *      instead of leaving it as plain body text.
	 *
	 * @param {Object} it - the `[Activity]` opener item being processed
	 * @param {Object[]} stack - the page emitter's open-container stack; this method pushes the new activity frame onto it
	 * @param {ConversionRun} run - the current run
	 * @param {boolean} [renderBlack=true] - whether to render this opener's own trailing text here; an interactive-widget-owned activity passes false and lays its own lead out itself
	 * @param {string|null} [idOverride=null] - an explicit id to use instead of the one parsed from the tag (falls back to the tag's own parsed number)
	 * @param {boolean} [forceInteractive=false] - true when the caller has determined this activity owns an interactive-task-type widget, forcing the `.interactive` class on
	 * @param {Object|null} [supervisorNote=null] - a supervisor-note item immediately following this opener, if the caller found one via lookahead
	 * @param {number} [pageLessonNumber] - which lesson the current page belongs to (used for id renumbering)
	 * @param {Object} [lessonLetterMap] - a per-run, per-lesson counter object (e.g. { "2": 3 }) tracking how many activities have already been numbered in each lesson; mutated in place as activities are numbered
	 * @param {boolean} [positionalId=false] - ROUND 217: true for a SYNTHETIC standalone-widget box (no writer id at all) — it takes the NEXT positional {lessonNumber}{letter} id, advancing the same lesson counter, exactly the way the human numbers the activity boxes it invents around bare task widgets in sequence with the tagged ones
	 * @returns {string[]} the rendered HTML fragments that open this activity box (its title/lead content, if any, is appended too)
	 */
	static activityOpen(it, stack, run, renderBlack = true, idOverride = null, forceInteractive = false, supervisorNote = null, pageLessonNumber, lessonLetterMap, positionalId = false) {
		const tpl = DataService.Data.EmitTemplates;
		let { modifiers, flags } = this.containerModifiers(it, tpl.activity_wrapper.modifier_classes, run);
		// PER-TYPE .interactive (derivable): an activity that OWNS an interactive
		// widget of a type the human consistently renders as an active TASK carries
		// the .interactive class — the "circle" indicator, vs the plain triangle for
		// display widgets. The widget TYPE is the WT signal (measured per type across
		// 02-All_HTML_Files: dragAndDrop 77%, multiChoiceQuiz 79%, dropQuiz 87%,
		// radioQuiz 85%, wordDrag 91%, reorder 95%, memoryGame 90%, bingo 84%,
		// wordSelect 85%, selfCheck 76% → .interactive; flipCard 32%, carousel 25%,
		// accordion 17%, clickDrop 14%, speechBubble 9% → plain). List is data:
		// activity_wrapper.interactive_widget_types.
		if (forceInteractive && !/(^| )interactive( |$)/.test(modifiers)) {
			modifiers += tpl.activity_wrapper.modifier_classes.interactive;
		}
		const out = [...flags];
		let id = (idOverride ?? it.parse.numbers[0]?.toUpperCase()) ?? null;
		// The human build numbers an activity box as {lessonNumber}{positional letter}
		// — e.g. a lesson's 4 activities become 2A/2B/2C/2D rather than being left as
		// the writer's own bare digits (1/2/3/4) straight out of the Writers Template.
		// Only a BARE-DIGIT id gets renumbered this way; an id the writer already gave
		// a letter of its own is kept as-is (see the note above about why). The
		// lesson-number PREFIX comes from the current page's own lessonNumber (worked
		// out elsewhere, robust to the page/file count not lining up exactly); the
		// LETTER is this activity's own positional order within that lesson. The
		// counter advances for every numbered activity regardless of whether it ends
		// up bare-renumbered or kept as a writer letter, so positions stay correct even
		// when both kinds of id appear side by side in the same lesson. Data
		// activity_wrapper.lesson_letter_number; env toggle ACTLETTER_OFF reverts to
		// always keeping the writer's own bare digit.
		const llRule = tpl.activity_wrapper.lesson_letter_number;
		const llOn = llRule && llRule.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.ACTLETTER_OFF);
		if (llOn && (id || positionalId) && pageLessonNumber != null) {
			const ln = String(pageLessonNumber);
			const idx = lessonLetterMap[ln] ?? 0;
			lessonLetterMap[ln] = idx + 1;
			// ROUND 217: a synthetic standalone-widget box has NO writer id — it takes the
			// next positional letter outright (same bare-digit rule, same 26-letter cap).
			if (positionalId && !id && idx < 26) {
				id = ln + String.fromCharCode(65 + idx);
			}
			// Renumber ONLY a BARE-DIGIT id into {lessonNumber}{positional letter} form
			// (e.g. a lesson's bare [Activity 1/2/3/4] becomes 2A/2B/2C/2D). A writer id
			// that ALREADY carries a letter (whether it was originally written that way,
			// or a letter this converter itself lifted from the end of a longer id
			// elsewhere in the pipeline) is deliberately KEPT rather than renumbered —
			// it can encode the activity's TRUE position even in a page where this
			// converter's own capture of the surrounding activities is incomplete: if
			// only the 2nd and 4th activities out of an original A-D set get captured,
			// keeping their own original "B"/"D" letters still matches the human build,
			// whereas relabelling them positionally as "A"/"B" would mislabel them. The
			// counter still advances for EVERY activity (kept-letter or renumbered
			// alike), so a bare id sitting among kept letters still lands on its correct
			// positional letter (and running past the 26th activity in one lesson simply
			// keeps the writer's own id rather than running out of letters).
			if (/^\d+$/.test(id) && idx < 26) {
				id = ln + String.fromCharCode(65 + idx);
			}
		}
		// When a supervisor note immediately follows this opener, build the human's
		// special "super-content-button" box variant instead of the plain one: the
		// note gets its own panel FIRST, then a fresh row>col is opened for the
		// activity's own title+body content to flow into afterwards. Otherwise, fall
		// back to the standard heading-anchored box open.
		const scCfg = tpl.activity_wrapper.super_content;
		const withNote = supervisorNote && scCfg && scCfg.enabled !== false;
		const numAttr = id ? Utils.FillTemplate(tpl.activity_wrapper.number_attr, { activityId: id }) : "";
		if (withNote) {
			out.push(`<div class="activity${modifiers}${scCfg.activity_class}"${numAttr}>`);
			out.push(scCfg.panel_open);
			const snDef = tpl.callouts?.by_tag?.["supervisor note"];
			// In a handful of module families the human build strips writer *italic*
			// markup out entirely when it lands INSIDE a supervisor note panel — the
			// panel always ships in plain text there. This is driven by the SAME data
			// setting the ordinary (non-activity) callout-box supervisor-note panel
			// elsewhere in the converter uses: callouts.by_tag.'supervisor
			// note'.strip_italic_subjects (a list of module-code prefixes this applies
			// to); env toggle PANELITALIC_OFF reverts to keeping the italic. A
			// Font-Awesome icon `<i>` is never touched by this stripping (it isn't real
			// text formatting), handled by MenuBuilder.stripTextItalic underneath.
			const stripItal = (snDef?.strip_italic_subjects ?? []).some(
				(s) => (run.moduleCode ?? "").startsWith(s))
				&& !(typeof process !== "undefined" && process.env && process.env.PANELITALIC_OFF);
			const deItal = (seg) => stripItal ? seg.map((h) => MenuBuilder.stripTextItalic(h)) : seg;
			// IN-SPAN PAYLOAD AS CONTENT: sometimes a writer types the supervisor note's
			// ENTIRE text INSIDE the coloured (red) span itself, rather than leaving any
			// plain black text after it for this box to pick up as its body — without
			// special handling that would leave the panel with no content at all, even
			// though the writer clearly did write something. In that situation the human
			// build still shows that in-span text as the panel's own <p> content, so it
			// needs to be recovered here too. (This method has no access to the tag
			// normaliser, so the caller does the original-case text extraction itself
			// and attaches it here as `_payloadText` before calling in.) A payload that
			// was instead recognised as an ordinary writer instruction fragment keeps
			// going through the normal CS-note path rather than this one. Data
			// callouts.by_tag.'supervisor note'.long_payload_as_content; env toggle
			// SUPPAYLOAD_OFF reverts to the content-less panel + flagged-as-empty note.
			const payload = (snDef?.long_payload_as_content
				&& (supervisorNote._payloadText ?? "").trim()
				&& !supervisorNote.parse?.instructionFragment
				&& !(typeof process !== "undefined" && process.env && process.env.SUPPAYLOAD_OFF))
				? supervisorNote._payloadText.trim() : "";
			if (payload) out.push(...deItal(ListsAndRuns.renderBlackText(payload, run, supervisorNote.block?.links)));
			const noteBody = (supervisorNote.blackAfter ?? "").trim();
			if (noteBody) out.push(...deItal(ListsAndRuns.renderBlackText(noteBody, run, supervisorNote.block?.links)));
			out.push(scCfg.panel_close);
			out.push(scCfg.content_open);
		} else {
			out.push(Utils.FillTemplate(tpl.activity_wrapper.open, { modifiers, numberAttr: numAttr }));
		}
		// titledOpener records whether THIS particular opener carried its own title/lead
		// text right after the tag. An opener with EMPTY trailing text (e.g.
		// "[Activity 2A]" whose title is instead a SEPARATE [H3] heading further down)
		// is the shape the human build continues by treating a LATER bare [Activity]
		// tag as still belonging to the same box (a bare re-emphasis, not a new
		// activity). A TITLED opener (e.g. "[Activity 5C] Extra for Experts", which
		// carries its own text) instead starts a fully self-contained box, so a LATER
		// bare [Activity] tag is treated as a brand-new sibling activity and gets
		// renumbered rather than merged into this one.
		stack.push({ tag: "activity", close: tpl.activity_wrapper.close, mode: "activity",
			hasContent: false, titledOpener: (it.blackAfter ?? "").trim().length > 0, id });
		// renderBlack=false lets the activity-OWNED path lay out the lead itself
		// (first line → <h3> title); the standalone container path keeps true.
		if (renderBlack && it.blackAfter.trim()) {
			// STANDALONE activity TITLE: for an activity that ISN'T owned by an
			// interactive widget bundle (renderBlack is true here, meaning this method
			// is doing the layout itself instead of deferring to the widget's own lead
			// logic), the FIRST line of the opener's trailing text becomes a real
			// `<h{level}>` title heading, and everything else becomes ordinary body
			// text — matching the house convention the vast majority of standalone
			// activities in the human build follow. Data
			// activity_wrapper.standalone_title_heading; env toggle ACTTITLE_OFF
			// reverts to rendering the whole trailing text as plain paragraphs, with
			// no heading promoted out of it.
			const th = tpl.activity_wrapper.standalone_title_heading;
			const titleOn = th?.enabled
				&& !(typeof process !== "undefined" && process.env && process.env.ACTTITLE_OFF);
			const raw = it.blackAfter.trim();
			const nl = raw.search(/\n/);
			const title = titleOn ? (nl >= 0 ? raw.slice(0, nl) : raw).replace(/\*/g, "").trim() : "";
			if (titleOn && title) {
				out.push(`<h${th.level}>${ListsAndRuns.inlineMarkup(title)}</h${th.level}>`);
				const rest = nl >= 0 ? raw.slice(nl + 1).trim() : "";
				if (rest) out.push(...ListsAndRuns.renderBlackText(rest, run, it.block?.links));
			} else {
				out.push(...ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links));
			}
			stack[stack.length - 1].hasContent = true;
		}
		return out;
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ActivitiesBuilder };
