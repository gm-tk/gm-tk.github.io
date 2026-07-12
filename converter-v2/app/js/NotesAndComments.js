/**
 * NotesAndComments.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Everything to do with the two kinds of developer-facing note that can show
 * up in the finished HTML output:
 *
 *   1. WRITER INSTRUCTIONS / DESIGNER NOTES — a note left behind for the
 *      developer, produced whenever the writer asked a question or left a
 *      to-do in the Writers Template, or the converter itself hit
 *      something it couldn't safely resolve on its own. Since ROUND 219
 *      (the design team's Change Ledger CL-0010/CL-0013) these render as
 *      a RED + BOLD `<p>` with a SOURCE-SPECIFIC prefix:
 *        - "Writers Note:"  — the writer's own note / CS instruction
 *          (recognised via the Instruction_Cues vocabulary; kind "cs");
 *        - "Red Flag:"      — a converter-detected issue (ambiguity,
 *          missing info, unbuildable structure; kind "diagnostic");
 *        - "Designer/Developer To Do:" — a deferred piece of a known,
 *          correctly-built pattern (kind "todo"; used by the doc-14
 *          subject-parameter emissions when those go live).
 *      The pre-219 prefixes were "CS:" / "RED FLAG:" (red, not bold);
 *      env NOTESCHEME_OFF (or Emit_Templates
 *      red_flag.ledger_note_scheme.enabled:false) reverts to those
 *      legacy forms byte-for-byte.
 *   2. NATIVE WORD COMMENTS — the little "insert comment" bubbles a
 *      reviewer leaves directly in Word (stored in word/comments.xml).
 *      Only comments from a WHITELISTED set of Creative Services authors
 *      are ever shown in the output; everything else is silently dropped,
 *      and even a whitelisted author's comment is dropped if it's just
 *      repeating boilerplate copyright/permission text with nothing for
 *      the developer to act on.
 *
 * WHY SEPARATE FILE:
 * These are pure "text in, HTML-snippet out" emitters that only ever need
 * DataService.Data (the shared data-driven config) and the small per-run
 * `run` object (for note counting) — no dependency on the big page-assembly
 * state machine. Keeping them together means every rule about how a note
 * or comment is worded, prefixed, de-duplicated, whitelisted, or filtered
 * lives in ONE place instead of being scattered through the page emitter.
 *
 * WHEN TO WORK HERE:
 * - Changing how a writer instruction is worded, prefixed, or de-duplicated
 *   -> redFlag / stripCsCue / stripAddresseeCue.
 * - Changing which Word-comment authors are trusted, or how their comments
 *   are rendered -> commentAuthorDisplay / commentNoteFor / commentNotes.
 * - Changing which comments count as "just noise" and get dropped
 *   -> commentIsOmittable.
 * - Matching a Media List comment to the body element that uses the same
 *   piece of media -> mediaKeys.
 * - Changing how leftover WT template placeholder text (a prompt like
 *   "Insert brief introductory text." that the writer never replaced) is
 *   cleaned out of the final page -> OmitPlaceholderResidue.
 * - Changing how developer notes are tidied up once the WHOLE page has
 *   been assembled (relocated out of the menu, merged together, stripped
 *   of empty addressee cues) -> TidyDeveloperNotes.
 *
 * WHY THE cv2-note / cv2-comment CSS CLASSES MATTER:
 * Every note this file emits carries one of these two marker classes
 * specifically so the automated structural-comparison tooling can skip
 * over them: the human-built reference pages never contain a developer
 * note, so anything that compares Claude's output structure to the
 * human's treats a marked note as invisible on both sides. If you ever add
 * a brand-new kind of note, give it one of these classes too.
 *
 * DATA THIS FILE READS: Emit_Templates.json (the `red_flag.*` section) and
 * Comment_Authors.json (the author whitelist + the boilerplate filter).
 * ===========================================================================
 */

class NotesAndComments {

	/**
	 * THE instruction-note emitter — the ONE place in the whole converter
	 * that produces a "CS:" or "RED FLAG:" note, so the visual form (a bold
	 * red `<p>`) and the prefix rules can never drift between call sites.
	 *
	 * WHAT IT DOES:
	 * Turns a plain instruction string into a rendered
	 * `<p style="color:red">PREFIX: text</p>` fragment — UNLESS the text
	 * turns out to be leftover, never-replaced WT template boilerplate
	 * (e.g. "Insert brief introductory text."), in which case it is
	 * silently OMITTED (no note rendered, and it does not count towards
	 * the red-flag total) because the writer supplied no real content for
	 * it to flag.
	 *
	 * HOW THE PREFIX IS CHOSEN:
	 *   - kind "cs" = a genuine WRITER-TO-CREATIVE-SERVICES note — text the
	 *     Instruction_Cues vocabulary recognised in the writer's own red
	 *     text, a developer-directed question, or an undocumented
	 *     positional note left on a container. Renders "CS: …".
	 *   - kind "diagnostic" (the default) = a note the CONVERTER ITSELF
	 *     generated because something couldn't be safely resolved (an
	 *     empty or malformed tag, a missing URL, an orphan sub-tag, an
	 *     un-built widget, an unmatched menu/container). Renders
	 *     "RED FLAG: …".
	 * Before the "CS:" prefix is actually applied, any cue the writer's
	 * own note text already opens with ("CS:", "CS Note:", "Dev:", "Note
	 * to developer:" …) is folded away first — see stripCsCue and
	 * stripAddresseeCue below — so the note can never double up to read
	 * "CS: CS Note: …".
	 *
	 * @param {string} text - the instruction/diagnostic text to show
	 * @param {ConversionRun} run - the current run (used to count red flags)
	 * @param {string} [kind="diagnostic"] - "cs" for a writer note, "diagnostic" for a converter-generated note
	 * @returns {string} the rendered note `<p>`, or an empty `<p class="cv2-omit"></p>` marker when the text was omitted as boilerplate
	 */
	static redFlag(text, run, kind = "diagnostic") {
		// OMIT a writer instruction that is verbatim WT TEMPLATE-PLACEHOLDER text the
		// writer never replaced (e.g. "Insert brief introductory text." / "In this
		// section outline any connections…"). The writer supplied NO real content, so
		// the human build omits it entirely — it is NOT surfaced as a CS note, and it
		// does not count as a red flag. Scoped to retained writer notes (kind "cs");
		// converter diagnostics are never dropped this way. Data flag
		// red_flag.omit_placeholders (folded prefix/exact match); env toggle
		// PLACEHOLDER_OFF reverts to always surfacing the note as a CS note.
		const op = DataService.Data.EmitTemplates.red_flag?.omit_placeholders;
		if (op && op.enabled !== false && kind === "cs"
			&& !(typeof process !== "undefined" && process.env && process.env.PLACEHOLDER_OFF)) {
			const f = Utils.Fold(String(text ?? "")).replace(/^[•\-*\s]+/, "").trim();
			const hit = (op.phrases ?? []).some((p) =>
				op.match === "prefix" ? (f === p || f.startsWith(p)) : f === p);
			// Omit: emit a marker (not "") rather than nothing, so a later full-page
			// clean-up pass can still find and strip the writer's now-empty bullet
			// ("• Insert brief introductory text." would otherwise leave a bare
			// <ul><li></li></ul> behind) using the same note-adjacent-bullet logic used
			// elsewhere; OmitPlaceholderResidue (further down this file) removes both
			// the empty bullet AND the marker itself once the whole page is assembled.
			// No red flag is counted for an omitted placeholder.
			if (hit) return "<p class=\"cv2-omit\"></p>";
		}
		run.CountRedFlag();
		const rf = DataService.Data.EmitTemplates.red_flag;
		// SOURCE-split the prefix. A writer-to-Creative-Services instruction (kind
		// "cs": a retained note recognised via the Instruction_Cues vocabulary, a
		// developer-directed question, or an undocumented container-positional note)
		// renders with the "CS:" prefix; a converter-emitted TECHNICAL diagnostic
		// (kind "diagnostic", the default — empty/malformed tag, missing URL, orphan
		// sub-tag, un-built widget, unmatched menu/container) keeps "RED FLAG:".
		// Behind a data flag (red_flag.cs_relabel.enabled) + env toggle
		// (CSRELABEL_OFF): when either is off, every note reverts to always reading
		// "RED FLAG:", byte-for-byte, so the split can be safely A/B tested against
		// the plain baseline. cs_form is identical to form apart from the prefix
		// word, so choosing it never changes anything else about how the note looks
		// (still bold red, same <p> style).
		const relabel = (rf.cs_relabel?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.CSRELABEL_OFF);
		const useCs = relabel && kind === "cs" && !!rf.cs_form;
		// DEDUPE the doubled CS prefix. When the canonical "CS:" prefix is about to
		// be applied AND the writer's retained note ALREADY opens with a
		// Creative-Services-family cue ("CS:", "CS Note:", "Creative Services,", …),
		// fold that leading cue away so it reads "CS: <body>" instead of doubling up
		// to "CS: CS Note: <body>". Scoped to the cs_form path: when CSRELABEL_OFF is
		// set the prefix is always "RED FLAG:", where a leading "CS Note:" is NOT a
		// duplicate, so it is left in place there. Behind data flag
		// (red_flag.cs_dedupe.enabled) + env toggle (CSDEDUPE_OFF). NOTE:/answers:/
		// alert-note labels are NOT CS cues and are left intact; the DEV-family and
		// addressed "note to/for …" forms are folded separately, immediately below.
		let body = text;
		if (useCs) {
			const dd = rf.cs_dedupe;
			const ddOn = dd && dd.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.CSDEDUPE_OFF);
			if (ddOn) {
				const stripped = this.stripCsCue(body, dd);
				if (stripped.trim()) body = stripped;   // never strip a note down to empty
			}
			// Also fold a redundant leading ADDRESSEE cue (the DEV family "Dev:"/"Dev
			// team –"/"Developer note:", and the addressed "Note to developer:", "Note
			// to CS:", "Note for Creative Services.") so the "CS:" prefix isn't echoed
			// by who the note is addressed to. Separately reversible from the CS-cue
			// dedupe just above: data flag (red_flag.addressee_fold.enabled) + env
			// toggle (ADDRFOLD_OFF). The bare cues matched here are DEV-ONLY, so this
			// never strips a bare "CS" cue — that stays stripCsCue's job, above.
			const af = rf.addressee_fold;
			const afOn = af && af.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.ADDRFOLD_OFF);
			if (afOn) {
				const stripped = this.stripAddresseeCue(body, af);
				if (stripped.trim()) body = stripped;   // never strip a note down to empty
			}
		}
		// ROUND 219 — the LEDGER NOTE SCHEME (Change Ledger CL-0010 + CL-0013).
		// When ON (the default), the note ships the design team's source-specific
		// prefixes, red + bold: cs_form = "Writers Note:", form = "Red Flag:",
		// todo_form = "Designer/Developer To Do:" (kind "todo" — a deferred
		// asset/URL/setup of a correctly-built pattern; reserved for the doc-14
		// live-wiring rounds). When OFF (env NOTESCHEME_OFF or
		// red_flag.ledger_note_scheme.enabled:false) every note reverts to the
		// r57/r72 legacy forms ("CS:" / "RED FLAG:", red only) byte-for-byte.
		// The cv2-note gate-marker class is identical in both schemes.
		const scheme = (rf.ledger_note_scheme?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.NOTESCHEME_OFF);
		let form;
		if (useCs) form = scheme ? rf.cs_form : (rf.legacy_cs_form ?? rf.cs_form);
		else if (kind === "todo" && scheme && rf.todo_form) form = rf.todo_form;
		else form = scheme ? rf.form : (rf.legacy_form ?? rf.form);
		return Utils.FillTemplate(form, { text: Utils.EscapeHtml(body.replace(/\s+/g, " ").trim()) });
	};

	/**
	 * Strips a single leading Creative-Services-family cue from a retained
	 * CS note, so the canonical "CS:" prefix (added by redFlag, above)
	 * never ends up doubled.
	 *
	 * WHAT/HOW: entirely data-driven from red_flag.cs_dedupe — builds a
	 * regex from the `cues` list (sorted longest-first, regex-escaped,
	 * `\b`-anchored so "CSV"/"CSC" can't false-match a bare "CS"), an
	 * optional " note"/" notes" suffix, then a run of `: , . – -`
	 * delimiters and surrounding whitespace. Matches ONLY at the very
	 * front of the text, once — every other word (DEV/NOTE/answers/
	 * container labels) is left untouched because it simply isn't in the
	 * `cues` list.
	 *
	 * @param {string} text - the note text (may or may not open with a cue)
	 * @param {Object} dd - red_flag.cs_dedupe config, e.g. { cues: ["CS", "CS Note", "Creative Services"], optional_suffix: ["note", "notes"] }
	 * @returns {string} text with any leading CS-family cue removed
	 */
	static stripCsCue(text, dd) {
		const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\s+/g, "\\s+");
		const cues = (dd.cues ?? []).slice()
			.sort((a, b) => b.length - a.length).map(esc).join("|");
		if (!cues) return text;
		const sufWords = (dd.optional_suffix ?? []).map(esc).join("|");
		const sufPart = sufWords ? `(?:\\s+(?:${sufWords})\\b)?` : "";
		const re = new RegExp(`^\\s*(?:${cues})\\b${sufPart}\\s*[:,.\\u2013\\-]*\\s*`, "i");
		return text.replace(re, "");
	};

	/**
	 * Strips a single leading ADDRESSEE cue from a retained CS note, so the
	 * "CS:" prefix (added by redFlag, above) isn't echoed by WHO the note
	 * happens to be addressed to.
	 *
	 * WHAT/HOW: entirely data-driven from red_flag.addressee_fold. Tries
	 * two branches, BOTH requiring an explicit delimiter (`: , . – -`,
	 * since every real-world case carries one — requiring it keeps the
	 * dev-word strip conservative and unlikely to over-match):
	 *   - ADDRESSED — `(note to|note for) [the] <addressed_cues>`
	 *     ("Note to developer:", "Note to CS:", "Note for Creative
	 *     Services.");
	 *   - BARE — a lone `<bare_cues>` dev word ("Dev:", "Dev team –",
	 *     "Developer note:").
	 * `bare_cues` are DEV-ONLY, so a bare "CS …" cue is never touched here
	 * — that is stripCsCue's job (above), independently toggled. All
	 * alternations are sorted longest-first and `\b`-anchored (so "dev
	 * team" is tried before plain "dev", and words like "development" or
	 * "device" are never accidentally matched).
	 *
	 * @param {string} text - the note text (may or may not open with an addressee cue)
	 * @param {Object} af - red_flag.addressee_fold config, e.g. { bare_cues: ["Dev", "Developer note"], addressed_cues: ["developer", "CS"], addressed_by: ["note to", "note for"] }
	 * @returns {string} text with any leading addressee cue removed
	 */
	static stripAddresseeCue(text, af) {
		const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\s+/g, "\\s+");
		const alt = (arr) => (arr ?? []).slice().sort((a, b) => b.length - a.length).map(esc).join("|");
		const bare = alt(af.bare_cues);
		const ac = alt(af.addressed_cues);
		const by = alt(af.addressed_by);
		const sufWords = (af.optional_suffix ?? []).map(esc).join("|");
		const suf = sufWords ? `(?:\\s+(?:${sufWords})\\b)?` : "";
		const artWords = (af.optional_article ?? []).map(esc).join("|");
		const art = artWords ? `(?:(?:${artWords})\\s+)?` : "";
		const D = "[:,.\\u2013\\-]";
		const branches = [];
		if (by && ac) branches.push(`(?:${by})\\s+${art}(?:${ac})\\b${suf}\\s*${D}+\\s*`);
		if (bare)     branches.push(`(?:${bare})\\b${suf}\\s*${D}+\\s*`);
		if (!branches.length) return text;
		const re = new RegExp(`^\\s*(?:${branches.join("|")})`, "i");
		return text.replace(re, "");
	};

	/**
	 * Normalises a raw Word `w:author` string and checks it against the
	 * ENABLED whitelist of Creative Services comment authors.
	 *
	 * WHY THIS IS NEEDED: Word stores whatever the reviewer's Office
	 * display name happens to be, which can vary in case, in dot-vs-space
	 * form ("Kate.Scanlon" vs "Kate Scanlon"), and occasionally carries a
	 * trailing " [N]" disambiguator Word adds when two reviewers share a
	 * name. The `match.*` settings in Comment_Authors.json control exactly
	 * which of those variations are tolerated.
	 *
	 * @param {string} rawAuthor - the raw author string straight out of word/comments.xml
	 * @returns {string|null} the canonical DISPLAY name to render (e.g. "Kate Scanlon"), or null when the author isn't whitelisted or is disabled
	 */
	static commentAuthorDisplay(rawAuthor) {
		const cfg = DataService.Data.CommentAuthors;
		if (!cfg) return null;
		const m = cfg.match ?? {};
		const norm = (s) => {
			let t = String(s ?? "");
			if (m.strip_disambiguator !== false) t = t.replace(/\s*\[\d+\]\s*$/, "");
			t = t.toLowerCase();
			if (m.dot_space_equivalent !== false) t = t.replace(/[._]+/g, " ");
			return t.replace(/\s+/g, " ").trim();
		};
		const a = norm(rawAuthor);
		if (!a) return null;
		const aRev = (m.accept_reversed_order !== false && a.split(" ").length === 2)
			? a.split(" ").reverse().join(" ") : null;
		for (const author of (cfg.authors ?? [])) {
			if (author.enabled === false) continue;
			const forms = new Set([norm(author.display), ...((author.seen_as ?? []).map(norm))]);
			if (m.accept_reversed_order !== false) {
				for (const f of [...forms]) {
					const p = f.split(" ");
					if (p.length === 2) forms.add(p.reverse().join(" "));
				}
			}
			if (forms.has(a) || (aRev && forms.has(aRev))) return author.display;
		}
		return null;
	};

	/**
	 * Builds the set of MATCH KEYS a media URL can be found under, so a
	 * Media List row's Word comment can be linked to the body element
	 * that actually uses the same piece of media.
	 *
	 * WHY THIS EXISTS: a comment left on a row of the Media List document
	 * is anchored to that row's URL — but the body's own placeholder image
	 * (Mode P) often has NO live link at all, since it's just standing in
	 * for a real asset the developer drops in later. A plain URL-equality
	 * match would miss it entirely. Both places, though, usually carry the
	 * SAME iStock reference number or YouTube video id embedded in their
	 * URL, so extracting that id as an extra key lets the comment reach
	 * the placeholder even when there's no shared literal URL.
	 *
	 * @param {string} url - a media URL, from either the Media List row or a body link
	 * @returns {string[]} candidate match keys — always includes the exact URL, plus "istock:<id>" and/or "yt:<id>" when those patterns are found in it
	 */
	static mediaKeys(url) {
		const u = String(url ?? "");
		const keys = [u];
		const cfg = DataService.Data.CommentAuthors?.media_match;
		if (cfg && cfg.id_match === false) return keys;          // exact-URL-only fallback
		const gm = u.match(/gm-?(\d{6,})/i);
		if (gm) keys.push("istock:" + gm[1]);
		const cdn = u.match(/\/id\/(\d{4,})/i);
		if (cdn) keys.push("istock:" + cdn[1]);
		const yt = u.match(/(?:youtu\.be\/|[?&]v=|\/embed\/|\/vi?\/)([\w-]{8,})/);
		if (yt) keys.push("yt:" + yt[1]);
		return keys;
	};

	/**
	 * Renders ONE native Word comment as a red note paragraph, or returns
	 * null when it shouldn't be shown at all.
	 *
	 * WHAT IT DOES: checks the comment's author against the whitelist
	 * (commentAuthorDisplay, above), checks that its text isn't just
	 * non-actionable boilerplate (commentIsOmittable, below), and — only
	 * if it survives both checks — renders it via Comment_Authors's
	 * `render.form`: the SAME bold-red style as a CS/RED FLAG note, but
	 * PREFIXED with the author's display name (e.g. "Simon Vita: …") and
	 * carrying the cv2-comment marker class so the structural comparison
	 * gates skip over it (the human-built reference page never contains a
	 * raw Word comment, so there's nothing on that side to compare it
	 * against). Master-gated by Comment_Authors.enabled plus whichever env
	 * toggle Comment_Authors.env_toggle names (COMMENTS_OFF by default) —
	 * either one turns comment rendering off completely.
	 *
	 * @param {Object} c - one comment, e.g. { author: "Kate Scanlon", text: "Please double-check this link" }
	 * @returns {string|null} the rendered note `<p>`, or null (author not whitelisted, feature disabled, or text empty/non-actionable)
	 */
	static commentNoteFor(c) {
		const cfg = DataService.Data.CommentAuthors;
		if (!cfg || cfg.enabled === false) return null;
		const tog = cfg.env_toggle || "COMMENTS_OFF";
		if (typeof process !== "undefined" && process.env && process.env[tog]) return null;
		// ROUND 219 (Change Ledger CL-0010): the ledger scheme renders a captured
		// reviewer comment "Note from {author}: {text}" in red + bold — the author
		// and text verbatim, never reworded or author-dropped. NOTESCHEME_OFF (or
		// the ledger_note_scheme data flag) reverts to the round-72 legacy
		// "{author}: {text}" form so the whole prefix scheme A/Bs as one unit.
		const scheme = (DataService.Data.EmitTemplates.red_flag?.ledger_note_scheme?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.NOTESCHEME_OFF);
		const form = scheme ? cfg.render?.form : (cfg.render?.legacy_form ?? cfg.render?.form);
		if (!form) return null;
		const display = this.commentAuthorDisplay(c.author);
		if (!display) return null;
		const text = String(c.text ?? "").replace(/\s+/g, " ").trim();
		if (!text || this.commentIsOmittable(text)) return null;   // non-actionable commentary
		return Utils.FillTemplate(form, {
			author: Utils.EscapeHtml(display), text: Utils.EscapeHtml(text),
		});
	};

	/**
	 * Collects every renderable comment note anchored to ONE content
	 * block, in that block's comment order.
	 *
	 * @param {Object} block - a content block, e.g. { text: "...", comments: [{ author, text, rowUrl? }] }
	 * @returns {string[]} rendered note `<p>`s (may be empty)
	 */
	static commentNotes(block) {
		const out = [];
		for (const c of (block?.comments ?? [])) {
			// A comment carrying a rowUrl is anchored to a Media List TABLE ROW rather
			// than to ordinary body content, so it isn't rendered here at all — it gets
			// surfaced separately, by URL-MATCHING it against the BODY element that
			// links the same media item (see mediaKeys, above). Plain body comments
			// never carry a rowUrl, so this only ever skips Media-List-anchored ones.
			if (c.rowUrl) continue;
			const n = this.commentNoteFor(c);
			if (n) out.push(n);
		}
		return out;
	};

	// Compiled content-filter regexes, built ONCE (lazily, on first use) from
	// Comment_Authors.content_filter and cached here so every subsequent call
	// re-uses the same compiled RegExp objects instead of re-parsing the
	// pattern strings on every single comment.
	static #commentFilterRe = undefined;

	/**
	 * Is this comment NON-ACTIONABLE repetitive commentary that the
	 * designer doesn't need to do anything about?
	 *
	 * WHAT IT DOES: returns true only when the text matches an
	 * `omit_boilerplate` pattern (copyright / permission wording / "used
	 * in online learning…" / "Te Kura created" / © / attribution / "link
	 * only" …) AND matches NO `action_keep` signal. That second check
	 * matters: a MIXED note that repeats boilerplate but ALSO asks for a
	 * real action ("Replace with iStock. Used with permission.") is KEPT,
	 * because there's still something for the developer to do. Both
	 * pattern lists are data-described and matched case-insensitively;
	 * disabling the filter in data makes every comment surface.
	 *
	 * @param {string} text - the comment's own text (already trimmed/collapsed)
	 * @returns {boolean} true when the comment should be dropped as noise
	 */
	static commentIsOmittable(text) {
		const cf = DataService.Data.CommentAuthors?.content_filter;
		if (!cf || cf.enabled === false || !cf.omit_boilerplate) return false;
		if (this.#commentFilterRe === undefined) {
			this.#commentFilterRe = {
				omit: new RegExp(cf.omit_boilerplate, "i"),
				keep: cf.action_keep ? new RegExp(cf.action_keep, "i") : null,
			};
		}
		const { omit, keep } = this.#commentFilterRe;
		return omit.test(text) && !(keep && keep.test(text));
	};

	/**
	 * Strips the last visible trace of an OMITTED template-placeholder
	 * note from the finished page.
	 *
	 * WHY THIS EXISTS: redFlag (above) emits an empty
	 * `<p class="cv2-omit"></p>` marker wherever it dropped a leftover WT
	 * template placeholder, rather than simply emitting nothing — that
	 * marker is what lets THIS pass find and clean up the writer's
	 * now-empty bullet point that used to hold the placeholder text (e.g.
	 * a "• Insert brief introductory text." MODULE-INTRODUCTION bullet
	 * with nothing left inside it). Without this second pass the reader
	 * would still see a bare, empty bullet in the module-introduction
	 * list even though the note itself was correctly omitted.
	 *
	 * WHAT IT DOES: removes any run of empty single-item bullet lists
	 * that sits immediately BEFORE an omit marker, then removes every
	 * omit marker itself — so neither the placeholder note nor its empty
	 * bullet ever ships in the final HTML.
	 *
	 * Gated together with the omit behaviour in redFlag
	 * (red_flag.omit_placeholders / env toggle PLACEHOLDER_OFF): when
	 * that's off, no omit markers are ever emitted in the first place, so
	 * this whole pass is a harmless no-op. Called by PageAssembler on the
	 * FULL assembled page (body + menu + acknowledgements together), so a
	 * placeholder note that happened to land in the module menu — e.g. the
	 * overview page's "Information"/"Connections" tab — gets cleaned up
	 * too, which a body-only pass could never reach.
	 *
	 * @param {string} html - the fully assembled page HTML
	 * @returns {string} the same HTML with omit-marker residue removed
	 */
	static OmitPlaceholderResidue(html) {
		const op = DataService.Data.EmitTemplates.red_flag?.omit_placeholders;
		if (!op || op.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.PLACEHOLDER_OFF) return html;
		return html
			.replace(/(?:<ul[^>]*>\s*<li[^>]*>\s*<\/li>\s*<\/ul>\s*)+(?=<p[^>]*cv2-omit)/gi, "")
			.replace(/<p[^>]*class="cv2-omit"[^>]*>\s*<\/p>\s*/gi, "");
	}

	/**
	 * Final tidy-up pass over EVERY developer-facing cv2-note `<p>` on the
	 * WHOLE assembled page — a housekeeping pass that makes the notes
	 * easier for a real developer to actually find and read, without
	 * changing what any of them say. PageAssembler calls this after
	 * OmitPlaceholderResidue (above) and before final HTML indentation.
	 *
	 * All of this is gate-NEUTRAL: cv2-note is excluded from every
	 * structural comparison gate (see the file header), so none of these
	 * changes can affect how closely the output matches the human-built
	 * reference. Controlled by data flag red_flag.note_tidy, with THREE
	 * independent behaviours:
	 *
	 *   (a) MENU RELOCATE (env toggle MENUNOTE_OFF) — a cv2-note that
	 *       landed inside the module menu (i.e. before `<div id="body">`,
	 *       since the menu region is scoped above the body) is moved and
	 *       re-emitted as the FIRST thing inside the body, where a
	 *       developer opening the page will actually notice it — a note
	 *       hidden in the menu chrome could easily be missed.
	 *   (b) COALESCE (env toggle COALESCE_OFF) — a run of several
	 *       consecutive notes that all share the same prefix collapses
	 *       into ONE note: the first line keeps its "CS:"/"RED FLAG:"
	 *       prefix, the rest drop the (now redundant) prefix and are
	 *       joined underneath it with `<br>` line breaks, instead of
	 *       appearing as a wall of separately-prefixed paragraphs.
	 *   (c) BARE-CUE FOLD (part of the coalesce step) — a note whose ENTIRE
	 *       content is just a contentless bracketed or bare addressee cue
	 *       ("[Dev]", "Dev team", "note to developer") with nothing else
	 *       said is simply DROPPED, since it carries no information a
	 *       developer could act on.
	 *
	 * Env toggle NOTETIDY_OFF reverts the whole pass at once (all three
	 * behaviours), leaving every cv2-note exactly where and how it was
	 * originally emitted.
	 *
	 * @param {string} html - the fully assembled page HTML
	 * @returns {string} the same HTML with developer notes relocated/coalesced/cleaned
	 */
	static TidyDeveloperNotes(html) {
		const cfg = DataService.Data.EmitTemplates.red_flag?.note_tidy;
		if (!cfg || cfg.enabled === false) return html;
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		if (env.NOTETIDY_OFF) return html;
		const relocateOn = cfg.menu_relocate_enabled !== false && !env.MENUNOTE_OFF;
		const coalesceOn = cfg.coalesce_enabled !== false && !env.COALESCE_OFF;
		const prefixes = (cfg.prefixes ?? ["CS:", "RED FLAG:"]).slice().sort((a, b) => b.length - a.length);
		const bareRe = new RegExp(cfg.bare_cue_pattern ?? "^(dev|developer|cs)$", "i");
		const NOTE_ONE = /<p (class="cv2-note"[^>]*)>([\s\S]*?)<\/p>/g;

		// ---- (5a) relocate menu-region notes to the top of the body -----------
		if (relocateOn) {
			const bodyIdx = html.indexOf("<div id=\"body\"");
			if (bodyIdx >= 0) {
				let head = html.slice(0, bodyIdx);
				let body = html.slice(bodyIdx);
				const moved = [];
				head = head.replace(/[ \t]*<p class="cv2-note"[^>]*>[\s\S]*?<\/p>\n?/g, (m) => {
					moved.push(m.trim());
					return "";
				});
				if (moved.length) {
					body = body.replace(/(<div id="body"[^>]*>)/, (open) => `${open}\n${moved.join("\n")}`);
					html = head + body;
				}
			}
		}

		// ---- (5b + 4) coalesce consecutive same-prefix cv2-note runs ----------
		if (coalesceOn) {
			const coalesceRun = (runStr) => {
				const notes = [];
				let m, openTag = "class=\"cv2-note\" style=\"color: red\"";
				NOTE_ONE.lastIndex = 0;
				while ((m = NOTE_ONE.exec(runStr))) {
					openTag = m[1];
					const inner = m[2].trim();
					let prefix = "", bodyTxt = inner;
					for (const p of prefixes) {
						if (inner === p || inner.startsWith(p)) { prefix = p; bodyTxt = inner.slice(p.length).trim(); break; }
					}
					// (4) drop a contentless bracketed/bare addressee cue
					const bare = bodyTxt.replace(/^[[\s]+|[\]\s]+$/g, "").trim();
					if (bareRe.test(bare)) continue;
					if (!bodyTxt) continue;
					notes.push({ prefix, body: bodyTxt });
				}
				if (!notes.length) return "";
				const out = [];
				let i = 0;
				while (i < notes.length) {
					const pfx = notes[i].prefix;
					const lines = [];
					while (i < notes.length && notes[i].prefix === pfx) { lines.push(notes[i].body); i++; }
					out.push(`<p ${openTag}>${pfx ? pfx + " " : ""}${lines.join("<br>")}</p>`);
				}
				return out.join("\n");
			};
			// maximal runs of 1+ consecutive cv2-notes (whitespace between only)
			html = html.replace(/(?:<p class="cv2-note"[^>]*>[\s\S]*?<\/p>\s*)+/g, (run) => {
				const tidied = coalesceRun(run);
				// preserve the run's trailing whitespace so surrounding layout is unchanged
				const trail = run.match(/\s*$/)[0];
				return tidied ? tidied + trail : trail;
			});
		}
		return html;
	}
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { NotesAndComments };
