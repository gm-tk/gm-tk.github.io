/**
 * TagNormaliser.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * The ONLY tag-matching code in the engine. Takes one raw span of writer
 * text (a red span from the docx, or a 🔴[RED TEXT]…[/RED TEXT]🔴 span from
 * a parsed file) and resolves it into canonical tags + a classification:
 * tag span | writer instruction | numbering/noise.
 *
 * WHERE THE RULES COME FROM:
 * This is a faithful JavaScript port of the validated reference pipeline:
 *   - spec:      ../data/Tag_Normalisation_Spec.md  (the ordered rule set)
 *   - reference: ../reference/tests/normaliser.py   (the proven ~120 lines)
 * It executes Tag_Lexicon.json (82 tags / 377 aliases), Tag_Exceptions.json
 * (literal overrides — the spec's Step-3 rule 2, which the Python reference
 * omits; including it makes this port a superset), and Instruction_Cues.json
 * (the §2.3b cue list, surfaced as data).
 *
 * PROVEN COVERAGE:
 * The Python pipeline resolves 9,556/9,557 historical variations (99.99%).
 * This port is parity-tested against the same corpus fixture
 * (reference/tests/Tag_Variation_Catalogue.json) — see BUILD_CHANGELOG.md
 * for the run result. If you change ANYTHING here, re-run both harnesses.
 *
 * WHY ALL TAG KNOWLEDGE IS ELSEWHERE:
 * v1 died because tag knowledge lived in code. Here, new writer phrasing =
 * one alias appended in Tag_Lexicon.json; a bizarre one-off = one literal in
 * Tag_Exceptions.json. If a tag change seems to need an edit in THIS file,
 * stop — that is the v1 death spiral (see the extension contract in the
 * normalisation spec).
 *
 * WHEN TO WORK HERE:
 * Almost never. Only if the *generic* pipeline itself changes (a new
 * matching strategy), which is a spec change first, a code change second.
 * ===========================================================================
 */

class TagNormaliser {

	// Private state: compiled lookups built once from the data files.
	#aliasMap;        // folded alias → { canon, directive }
	#aliasOrder;      // aliases sorted longest-first (embedded matching)
	#aliasRegex;      // alias → boundary regex (embedded matching)
	#exceptions;      // folded fragment → literal resolution (Tag_Exceptions)
	#lexicon;         // raw lexicon (kept for widget_types lookups)
	#addresseeRegex;  // instruction guard (built from Instruction_Cues.json)
	#cuesRegex;       // instruction cue scan (built from Instruction_Cues.json)
	#tsNoteRe;        // media-timestamp note detector, e.g. "(to 1:00)" — compiled lazily, see #isMediaTimestampNote() below

	// Directive precedence for picking a span's PRIMARY tag
	// (Tag_Normalisation_Spec.md Step 4). Higher number wins.
	static #PRECEDENCE = {
		INTERACTIVE: 7, ELEMENT: 6, CONTAINER_OPEN: 5,
		SUBTAG: 4, INLINE: 4, INLINE_FORMAT: 4,
		PAGE_BOUNDARY: 3, SECTION_MARKER: 3, CONTAINER_CLOSE: 3,
		DROP: 2,
	};

	// Numbering pattern: "#?digits(.digits)*letter?" — captured for ids,
	// stripped for matching (spec Step 3, rule 4d). Mirrors normaliser.py.
	static #NUMBERING = /\s*#?\d+(?:\.\d+)*[a-z]?\b\s*/g;

	// "end X" / "end of X" / "/X" prefix → generic closer (spec rule 3)
	static #CLOSE_PREFIX = /^(?:end(?: of)?|\/)\s*/;

	/**
	 * Builds the matcher from the loaded data files.
	 *
	 * WHAT THE INPUTS ARE:
	 * @param {Object} lexicon    - parsed Tag_Lexicon.json
	 * @param {Object} exceptions - parsed Tag_Exceptions.json
	 * @param {Object} cues       - parsed Instruction_Cues.json
	 */
	constructor(lexicon, exceptions, cues) {
		// guard clauses — broken data should fail loudly at startup,
		// not quietly mid-conversion
		if (!lexicon?.tags) throw new Error("TagNormaliser: Tag_Lexicon.json missing/malformed");
		if (!exceptions?.exceptions) throw new Error("TagNormaliser: Tag_Exceptions.json missing/malformed");
		if (!cues?.cue_patterns) throw new Error("TagNormaliser: Instruction_Cues.json missing/malformed");

		this.#lexicon = lexicon;

		// ---- compile the alias map -------------------------------------
		// One folded alias can only belong to one canonical tag; first
		// definition wins (mirrors Python's dict.setdefault behaviour).
		this.#aliasMap = new Map();
		for (const [canon, def] of Object.entries(lexicon.tags)) {
			for (const alias of def.aliases) {
				const folded = Utils.Fold(alias);
				if (!this.#aliasMap.has(folded)) {
					this.#aliasMap.set(folded, { canon, directive: def.directive });
				}
			}
		}

		// longest-first order so embedded matching prefers the longest hit
		this.#aliasOrder = [...this.#aliasMap.keys()].sort((a, b) => b.length - a.length);

		// pre-compile one boundary regex per alias. The boundary classes
		// mirror normaliser.py exactly: an alias counts as "embedded" only
		// when bounded by space/punctuation (so 'h1' won't match inside
		// 'h1conditioning'). Trailing class additionally allows ] # digits.
		this.#aliasRegex = new Map();
		for (const alias of this.#aliasOrder) {
			const e = Utils.RegexEscape(alias);
			this.#aliasRegex.set(alias,
				new RegExp(`(?:^|[\\s:;,.|/(\\[+-])${e}(?:$|[\\s:;,.|/)\\]#\\d+-])`));
		}

		// ---- literal exceptions ----------------------------------------
		// folded full-fragment → its hand-written resolution
		this.#exceptions = new Map();
		for (const ex of exceptions.exceptions) {
			this.#exceptions.set(Utils.Fold(ex.fragment), ex.resolution);
		}

		// ---- instruction detection (data-driven) -----------------------
		// Addressee guard: fragment OPENS with "cs:" / "dev –" / "note," …
		// Built as: ^(prefix1|prefix2|…)\b[separator]
		const prefixes = cues.addressee_prefixes.map(Utils.RegexEscape).join("|");
		const seps = Utils.RegexEscape(cues.addressee_separators);
		this.#addresseeRegex = new RegExp(`^\\s*(${prefixes})\\b[${seps}]`);

		// Cue scan: any cue anywhere in the folded span (word-bounded).
		// cue_patterns entries are regex FRAGMENTS by design (see the data
		// file's _meta) — they are joined, not escaped.
		this.#cuesRegex = new RegExp(`\\b(${cues.cue_patterns.join("|")})\\b`);
	};

	/**
	 * Looks up a widget type list for a canonical tag (used by the
	 * interactive scanner to key into the boundary bank).
	 *
	 * @param {string} canon - canonical tag name, e.g. "flip card"
	 * @returns {string[]} widget_types, e.g. ["flipCard"] (empty if none)
	 */
	GetWidgetTypes(canon) {
		return this.#lexicon.tags[canon]?.widget_types ?? [];
	};

	/**
	 * Extracts a span's EMBEDDED RENDER TEXT in its ORIGINAL case.
	 *
	 * WHY THIS EXISTS:
	 * The parse results are folded (lowercased) for matching, but §1.2 of
	 * the interpretation rules is explicit: NEVER case-fold render content.
	 * When a heading/title lives inside the red span — "[H1] INTRODUCTION",
	 * "[Insert H3: Emotion]", "[Alert Box] A Living Taonga" — the visible
	 * text must come from the RAW span, not the folded remainders.
	 *
	 * HOW IT WORKS, per bracket fragment:
	 *  - "[head: payload]" where the payload is NOT itself a tag alias →
	 *    the payload is embedded content; it replaces the bracket.
	 *    ("[Insert H3: Emotion]" → "Emotion")
	 *  - any other bracket is a keyword/marker → removed entirely.
	 * Whatever sits OUTSIDE brackets inside the span stays as-is
	 * ("[H1] INTRODUCTION" → "INTRODUCTION").
	 *
	 * @param {string} raw - the raw span text (markers tolerated)
	 * @returns {string} original-case embedded render text ("" when none)
	 */
	RenderText(raw) {
		let s = raw.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "");
		s = s.replace(/\[([^\[\]]*)\]?/g, (whole, inner) => {
			const colon = inner.indexOf(":");
			if (colon < 0) return " ";
			const payload = inner.slice(colon + 1).trim();
			// a payload that is itself a known alias is a TAG, not content
			// (covers "[insert item #103: video]")
			if (!payload || this.#aliasMap.has(Utils.Fold(payload))) return " ";
			return ` ${payload} `;
		});
		s = s.replace(/\s+/g, " ").trim();
		// DROPPING STRAY PUNCTUATION-ONLY RESIDUE.
		//
		// If, after removing all the brackets, what's LEFT OVER has no letter
		// or digit in it AT ALL (in any script/language), then it's not real
		// content — it's just a stray punctuation mark a writer accidentally
		// left glued to the outside of a tag. For example "[whakatauki]:"
		// leaves a lone ":" sitting outside the bracket once the tag itself
		// is stripped away. If we returned that ":" as if it were real render
		// text, it could leak out as a bogus visible label — e.g. a callout
		// box showing an empty "<p><b>:</b></p>". So when the leftover text
		// has no letters or digits at all, we return an empty string instead.
		// This is completely safe for te reo Māori text: macronned vowels
		// like ā/ē/ī/ō/ū still count as "letters" under the \p{L} Unicode
		// property, so genuine te reo content is never mistaken for stray
		// punctuation and dropped. Any residue with even ONE real letter or
		// digit (a genuine embedded title or label) is always kept exactly
		// as before. This rule applies generally, for every tag, everywhere
		// RenderText() is called.
		// Data flag: Input_Doc_Rules.json render_text.drop_punctuation_only
		// Env toggle: STRAYLEAD_OFF (reverts to letting the stray
		// punctuation leak through as if it were real content)
		if (s && !/[\p{L}\p{N}]/u.test(s)
			&& (typeof DataService !== "undefined")
			&& DataService.Data?.InputDocRules?.render_text?.drop_punctuation_only !== false
			&& !(typeof process !== "undefined" && process.env && process.env.STRAYLEAD_OFF)) {
			return "";
		}
		return s;
	};

	/**
	 * Single best alias match inside one folded fragment.
	 *
	 * HOW IT WORKS (spec Step 3 rule 4, mirroring normaliser.py match_one):
	 * Try candidates in order — first hit wins:
	 *   a. the whole fragment           (exact)
	 *   b. text after a colon           (payload — "[insert item #103: video]")
	 *   c. text before a colon          (head    — "[H1: Phase one]")
	 *   d. fragment with numbers gone   (denumbered — "[Activity 7]")
	 *   e. head with numbers gone       (denumbered_head)
	 * then fall back to the longest alias EMBEDDED on a word boundary,
	 * where suffix position beats prefix beats interior, and aliases
	 * shorter than 3 chars must match exactly (except h1–h5).
	 *
	 * @param {string} fragment - folded bracket-fragment text
	 * @returns {Object|null} { canon, directive, how, alias } or null
	 */
	#matchOne(fragment) {
		const f = Utils.StripChars(fragment, " .;,|-");
		if (!f) return null;

		// split on the first colon for payload/head candidates
		const colon = f.indexOf(":");
		const head = colon >= 0 ? f.slice(0, colon).trim() : f;
		const payload = colon >= 0 ? f.slice(colon + 1).trim() : "";

		// de-numbered forms (numbering captured elsewhere, stripped here)
		const denum = Utils.StripChars(
			f.replace(TagNormaliser.#NUMBERING, " ").replace(/\s+/g, " ").trim(), " .;,|-");
		const denumHead = head.replace(TagNormaliser.#NUMBERING, " ").trim();

		const candidates = [
			[f, "exact"], [payload, "payload"], [head, "head"],
			[denum, "denumbered"], [denumHead, "denumbered_head"],
		];
		for (const [cand, how] of candidates) {
			if (cand && this.#aliasMap.has(cand)) {
				const hit = this.#aliasMap.get(cand);
				return { canon: hit.canon, directive: hit.directive, how, alias: cand };
			}
		}

		// ---- embedded match: longest alias on a word boundary ----------
		// Position score: suffix (2) > prefix (1) > interior (0); compared
		// after length, exactly like the Python tuple (len, pos).
		let best = null;   // { lenPos: [len,pos], result }
		const padded = ` ${f} `;
		for (const alias of this.#aliasOrder) {
			// short aliases must match exactly (h1–h5 excepted) to stop
			// e.g. 'p' or 'h' matching inside ordinary words
			if (alias.length < 3 && !/^h\d$/.test(alias)) continue;
			if (!this.#aliasRegex.get(alias).test(padded)) continue;

			const pos = f.endsWith(alias) ? 2 : (f.startsWith(alias) ? 1 : 0);
			const lenPos = [alias.length, pos];
			const better = best === null
				|| lenPos[0] > best.lenPos[0]
				|| (lenPos[0] === best.lenPos[0] && lenPos[1] > best.lenPos[1]);
			if (better) {
				const hit = this.#aliasMap.get(alias);
				best = { lenPos, result: { canon: hit.canon, directive: hit.directive, how: "embedded", alias } };
			}
		}
		return best ? best.result : null;
	};

	/**
	 * Resolves ONE bracket fragment to its tag list.
	 *
	 * ORDER (spec Step 3 — first hit wins):
	 *  1. Instruction guard (addressee prefix) → whole fragment is a
	 *     writer instruction; never tag-matched inside.
	 *  2. Exception lookup (Tag_Exceptions.json literal).
	 *  3. Generic closer ("end X" / "/X") → CONTAINER_CLOSE of X
	 *     (or PAGE_BOUNDARY for page/lesson).
	 *  4. Alias match + multi-match: after a hit, delete the matched alias
	 *     text and retry (max 3 passes) so compounds resolve to
	 *     container + child ("[Activity 10A – Drag and Drop]" → drag and
	 *     drop + activity).
	 *
	 * @param {string} fragment - folded fragment text
	 * @returns {Object[]} tag dicts; [{instruction:true,…}] for guard hits;
	 *                     [] when nothing resolved
	 */
	#resolveFragment(fragment) {
		const f = fragment.trim();

		// 1. instruction guard — "[CS please make this pink]" etc.
		if (this.#addresseeRegex.test(f)) {
			return [{ instruction: true, fragment, remainder: "" }];
		}

		// 2. literal exception — the deliberately tiny escape hatch
		const ex = this.#exceptions.get(f);
		if (ex) {
			const tags = [];
			for (const canon of [ex.primary, ...(ex.also ?? [])]) {
				const def = this.#lexicon.tags[canon];
				if (def) tags.push({ tag: canon, directive: def.directive, how: "exception", fragment, alias: canon });
			}
			if (tags.length) { tags[tags.length - 1].remainder = ""; return tags; }
		}

		// 3. generic closer — covers every "[End Accordion]", "[/alert]" …
		const closeMatch = f.match(TagNormaliser.#CLOSE_PREFIX);
		if (closeMatch && closeMatch[0].trim() && f.length > closeMatch[0].length) {
			const inner = this.#matchOne(f.slice(closeMatch[0].length));
			if (inner) {
				return [{
					tag: `end ${inner.canon}`,
					// page/lesson closers are page boundaries, not container pops
					directive: inner.directive === "PAGE_BOUNDARY" ? "PAGE_BOUNDARY" : "CONTAINER_CLOSE",
					how: "close_prefix", fragment, remainder: "",
				}];
			}
		}

		// 3b. A SUFFIX closer form: "[Activity ends]", "[Activity end]",
		// "[Tabs end]". Here the writer puts the CONTAINER word FIRST and the
		// word "end" (or "ends") LAST — the reverse order from the PREFIX
		// closer handled just above (which only recognises "end X" or "/X").
		// Some writers naturally write "ends" as a plural, but the lexicon's
		// "end activity" alias only lists the singular "activity end", so
		// without this separate check the plural form would never match. A
		// clear "<container word> end" or "<container word> ends" closes
		// whichever container is currently open with that name.
		// This is intentionally SCOPED to only match tags that open a
		// genuine CONTAINER (like "activity", "alert", "important") — so
		// something like "[image]" or "[video]" followed by the word
		// "end(s)" is never mistaken for a closer (there's no false
		// container pop), and ordinary prose like "[... to the end]" whose
		// leading word isn't a real container name simply falls through to
		// the normal alias-matching logic below instead.
		// Data flag: Tag_Lexicon.json _meta.suffix_container_close
		// Env toggle: ACTENDS_OFF
		if ((this.#lexicon._meta?.suffix_container_close ?? true)
			&& !(typeof process !== "undefined" && process.env && process.env.ACTENDS_OFF)) {
			const sufMatch = f.match(/\s+ends?$/);
			if (sufMatch) {
				const head = f.slice(0, sufMatch.index).trim();
				const inner = head ? this.#matchOne(head) : null;
				if (inner && inner.directive === "CONTAINER_OPEN") {
					return [{
						tag: `end ${inner.canon}`,
						directive: "CONTAINER_CLOSE",
						how: "close_suffix", fragment, remainder: "",
					}];
				}
			}
		}

		// 4. alias match with multi-match (container + child compounds)
		const tags = [];
		let remaining = f;
		for (let pass = 0; pass < 3; pass++) {
			const r = this.#matchOne(remaining);
			if (!r) break;
			tags.push({ tag: r.canon, directive: r.directive, how: r.how, fragment, alias: r.alias });
			// delete the matched alias text and retry on the remainder —
			// if the alias text isn't literally present (denumbered match),
			// there is nothing left to scan: stop (mirrors normaliser.py)
			const after = remaining.replace(r.alias, " ");
			if (after === remaining) { remaining = ""; break; }
			remaining = Utils.StripChars(after.replace(/\s+/g, " ").trim(), " .;,:|-");
			if (remaining.length < 3) { remaining = ""; break; }
		}
		if (tags.length) {
			tags[tags.length - 1].remainder =
				remaining.replace(TagNormaliser.#NUMBERING, " ").trim();
		}
		return tags;
	};

	/**
	 * THE public entry point: parses one raw span.
	 *
	 * WHAT IT RETURNS (one object per span):
	 * {
	 *   tags:       [ {tag, directive, how, fragment, alias, remainder?} ],
	 *   primary:    the governing tag (highest directive precedence) | null,
	 *   class:      "tag" | "instruction" | "noise",
	 *   instructionFragment: true when an addressee-guard fragment fired,
	 *   folded:     the folded span text (for downstream cue checks),
	 *   remainders: unmatched bracket text (embedded titles live here),
	 *   hasBrackets:whether any bracket fragment was found,
	 *   numbers:    captured numbering strings, e.g. ["2a"] — activity ids
	 * }
	 *
	 * REAL SAMPLE (from OSAH401):
	 *   parse("🔴[RED TEXT] [H2]  [/RED TEXT]🔴") →
	 *   { tags:[{tag:"h2",directive:"ELEMENT",how:"exact",…}],
	 *     primary:{tag:"h2",…}, class:"tag", … }
	 *
	 * @param {string} raw - the span text (markers included or not)
	 * @returns {Object} parse result as above
	 */
	Parse(raw) {
		// Step 1 FOLD: strip red markers, then fold. Raw docx spans have no
		// markers — the strip is a no-op there (spec Step 1.1).
		let s = raw.replace(/\u{1f534}/gu, "").replace(/\[\/?RED TEXT\]/g, "");
		s = Utils.Fold(s);

		// Step 2 EXTRACT bracket fragments, with damage repair:
		//   normal [x] pairs, a dangling "[x" at the end (missing ]),
		//   and a leading "x]" at the start (missing [).
		const brackets = [...s.matchAll(/\[([^\[\]]+)\]/g)].map((m) => m[1]);
		const dangling = s.match(/\[([^\[\]]+)$/);
		if (dangling) brackets.push(dangling[1]);
		const leading = s.match(/^([^\[\]]+)\]/);
		if (leading) brackets.push(leading[1]);

		// free text = whatever sits outside brackets (kept for the
		// instruction-vs-content decision below)
		const free = s.replace(/\[[^\[\]]*\]?/g, "").trim();

		// Step 3 RESOLVE each fragment
		const tags = [];
		const remainders = [];
		const numbers = [];
		let instructionFragment = false;
		for (const frag of brackets) {
			// capture numbering BEFORE it gets stripped (activity/lesson ids)
			for (const n of frag.matchAll(/#?(\d+(?:\.\d+)*[a-z]?)\b/g)) numbers.push(n[1]);

			const resolved = this.#resolveFragment(frag);
			if (!resolved.length) {
				// unmatched fragment: its folded, de-numbered text is a
				// "remainder" — often an embedded title (kept downstream)
				remainders.push(Utils.Fold(frag).replace(TagNormaliser.#NUMBERING, " ").trim());
			}
			for (const t of resolved) {
				if (t.instruction) instructionFragment = true;
				else {
					tags.push(t);
					if (t.remainder) remainders.push(t.remainder);
				}
			}
		}

		// ACTIVITY NUMBER WRITTEN OUTSIDE THE BRACKET — e.g. "[Activity] 3A".
		//
		// Most writers put an activity's id INSIDE the tag brackets, like
		// "[Activity 3A]". But some writers instead put the id AFTER the
		// closing bracket, still within the same red-coloured span — e.g.
		// "[Activity] 3A". In that shape, the "3A" ends up in the `free` text
		// (the part of the span outside any brackets) rather than inside a
		// bracket fragment, so the `numbers` array above never picks it up,
		// and the activity box renders with NO number on it at all (measured:
		// this happened far more often in our output than in the
		// human-built pages, which almost always show a number).
		// Fix: when this span carries an [Activity] tag that OPENS a
		// container, and no number was found inside any bracket, look at the
		// very START of the free text for a short "digit(s) + one letter"
		// id, like "1a", "2c", or "10b", and treat that as the activity's
		// number too. Every part of the pipeline that reads `numbers` (the
		// activity box builder, the interactive-widget scanner's activity
		// id, and the logic that merges adjacent activity fragments
		// together) then sees the number correctly. We deliberately require
		// a LETTER after the digits, not a bare number by itself — this
		// stops something like "5 minutes" of ordinary prose from ever
		// being misread as an activity number "5".
		// Data flag: Emit_Templates.json activity_wrapper.number_from_tail.enabled
		// Env toggle: ACTNUMTAIL_OFF
		if (!numbers.length && free
			&& (typeof DataService !== "undefined")
			&& DataService.Data?.EmitTemplates?.activity_wrapper?.number_from_tail?.enabled
			&& !(typeof process !== "undefined" && process.env && process.env.ACTNUMTAIL_OFF)
			&& tags.some((t) => t.tag === "activity" && t.directive === "CONTAINER_OPEN")) {
			const fm = /^(\d{1,2}[a-z])(?=\s|$|[:.)\]–-])/.exec(free);
			if (fm) numbers.push(fm[1]);
		}

		// Step 4 CLASSIFY the span
		let primary = null;
		let cls;
		if (tags.length) {
			// the primary tag = highest directive precedence; ties keep the
			// FIRST seen (stable, mirroring Python's max())
			primary = tags.reduce((best, t) => {
				const p = TagNormaliser.#PRECEDENCE[t.directive] ?? 0;
				const bp = TagNormaliser.#PRECEDENCE[best.directive] ?? 0;
				return p > bp ? t : best;
			});
			// A "CONDITION" TAG SHOULD NEVER OUTRANK A REAL WIDGET.
			//
			// Some tags describe a CONDITION under which a widget should
			// behave a certain way (e.g. "self check" / "autocheck" resolve
			// to a "typing quiz" condition tag) rather than being an actual
			// interactive widget in their own right. If a span happens to
			// ALSO contain a genuine, different INTERACTIVE widget tag —
			// e.g. "[clickdrop quiz autocheck]" resolves to BOTH a clickDrop
			// widget AND the "typing quiz" condition — the precedence
			// reducer above might pick the condition tag as `primary` just
			// because of tie-breaking order, which is wrong: the real
			// widget should always govern. This check looks for exactly
			// that situation and, if found, swaps `primary` over to the
			// genuine widget tag instead.
			// A span where the condition tag is the ONLY tag present (e.g.
			// a standalone "[self check]" with no other widget) is
			// completely unaffected by this — there's nothing to demote it
			// in favour of.
			// Data flag: Tag_Lexicon.json _meta.condition_primary_demote
			// Env toggle: PRIMARYFIX_OFF
			const cpd = this.#lexicon?._meta?.condition_primary_demote;
			if (cpd && tags.length > 1
				&& !(typeof process !== "undefined" && process.env && process.env.PRIMARYFIX_OFF)) {
				const condAliases = new Set((cpd.aliases ?? []).map((a) => String(a).toLowerCase()));
				const isCond = (t) => t.tag === cpd.tag && condAliases.has(String(t.alias ?? "").toLowerCase());
				if (isCond(primary)) {
					const real = tags.find((t) =>
						(TagNormaliser.#PRECEDENCE[t.directive] ?? 0) === TagNormaliser.#PRECEDENCE.INTERACTIVE && !isCond(t));
					if (real) primary = real;
				}
			}
			// THE WORD "INTERACTIVE" ALONE SHOULD NOT OPEN AN ACTIVITY BOX.
			//
			// The single word "interactive" is listed as one of the ALIASES
			// for the [activity] tag (i.e. it's one of the ways a writer can
			// spell "open an activity box"). That's usually fine, but it
			// causes a real problem for QUALIFIER phrases that merely use
			// the word "interactive" as an adjective rather than meaning
			// "start an activity here" — phrases like "[Interactive Stop
			// Watch]", "[interactive tool]", "[interactive stopwatch]", or
			// even a completely bare "[Interactive]" on its own. Each of
			// these was resolving to an activity CONTAINER_OPEN tag, which
			// incorrectly opened a brand-new, NUMBERLESS activity box right
			// in the middle of what should have been ONE continuous
			// activity — splitting it into two boxes (one real example: an
			// activity's audio instructions and drag-and-drop word content
			// ended up split across two separate boxes because of a stray
			// "[Interactive Stop Watch]" qualifier phrase in the middle).
			//
			// A GENUINE activity container tag always contains the actual
			// word "activity" somewhere in it too — e.g. "[interactive
			// activity]" produces a SEPARATE, real "activity" tag alongside
			// the "interactive" one. So the fix is: if the chosen PRIMARY
			// tag is an activity CONTAINER_OPEN whose matched alias is one
			// of the known "qualifier" phrases (just "interactive" used as
			// an adjective, not the real container-opening word), and there
			// is NO OTHER genuine activity tag present in the same span,
			// then drop that qualifier-only activity tag. The span then
			// falls through to being classified as an ordinary instruction
			// or noise, and it no longer opens/splits an activity box.
			//
			// Spans where "interactive" leads to a real WIDGET (not the
			// activity container) — e.g. "[Interactive – drag and drop]",
			// which resolves to the drag-and-drop widget tag — are
			// completely unaffected by this. The widget tag always wins the
			// precedence contest over the activity container tag anyway
			// (widgets outrank containers in #PRECEDENCE), so "activity"
			// never becomes `primary` in that case to begin with.
			//
			// Data flag: Tag_Lexicon.json _meta.qualifier_alias_demote
			// Env toggle: INTERACTIVEQUAL_OFF
			const qad = this.#lexicon?._meta?.qualifier_alias_demote;
			if (qad && qad.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.INTERACTIVEQUAL_OFF)
				&& primary && primary.tag === qad.tag && primary.directive === qad.open_directive) {
				const qualAliases = new Set((qad.aliases ?? []).map((a) => String(a).toLowerCase()));
				const isQual = (t) => t.tag === qad.tag && t.directive === qad.open_directive
					&& qualAliases.has(String(t.alias ?? "").toLowerCase());
				const hasRealContainer = tags.some((t) => t.tag === qad.tag
					&& t.directive === qad.open_directive
					&& !qualAliases.has(String(t.alias ?? "").toLowerCase()));
				// IMPORTANT REFINEMENT: the rule is "the word 'interactive'
				// only opens a box when a WIDGET is actually named nearby".
				// A widget's name often appears in the FREE text (the part
				// outside any brackets) right after a bare "[Interactive]"
				// or "[interactive tool]" tag — e.g. "[Interactive] Drag and
				// drop..." or "[interactive tool] flip cards...". In cases
				// like that, the human-built page DOES show a widget box
				// there, so demoting the tag would wrongly DELETE a box that
				// should exist. So: KEEP the box whenever the span names ANY
				// widget, and only demote (drop) the tag when it's a pure
				// qualifier phrase followed by ordinary instruction/prose
				// text that names no widget at all (e.g. "[Interactive Stop
				// Watch] Placed over ... please ..." — no widget named, so
				// this one still gets demoted and the box-splitting problem
				// goes away).
				//
				// We scan the folded free text for any known INTERACTIVE
				// (widget) alias appearing anywhere as a SUBSTRING, rather
				// than requiring an exact word match — this makes the check
				// robust to small variations like plurals or stray
				// punctuation the bracket-matching logic elsewhere might
				// miss (e.g. "sliders??" still contains "slider"). We
				// require the alias to be at least 4 characters long to
				// avoid accidental matches on very short, common alias
				// fragments. If in doubt, this check errs on the side of
				// KEEPING the box (a false "yes, a widget is named" only
				// means we decline to fix a split — it never deletes real
				// content).
				const foldedFree = Utils.Fold(free || "");
				let namesWidget = false;
				if (foldedFree) {
					for (const [alias, def] of this.#aliasMap) {
						if (def.directive === "INTERACTIVE" && alias.length >= 4 && foldedFree.includes(alias)) {
							namesWidget = true; break;
						}
					}
				}
				if (isQual(primary) && !hasRealContainer && !namesWidget) {
					// ROUND 217 (Chris, boundary audit — AGH1001-01). A BARE standalone
					// "[Interactive]" — the demoted alias is the span's ONLY tag and it
					// matched the whole bracket token EXACTLY (how "exact") — is not a
					// qualifier of anything: it is the writer's generic widget INVOCATION
					// ("an interactive goes here"), typically followed by the instruction
					// line + the data table. The human builds a widget + an activity box
					// there (gold AGH1001-01 ships boxes 1A/1B/1C for exactly these);
					// dropping the tag leaked the data table as a kept <table> and boxed
					// nothing. So the bare form is RE-TAGGED as the generic INTERACTIVE
					// opener instead of dropped: the scanner then opens an (unclassified)
					// bundle that captures the instruction + table, and the round-217
					// activity_wrapper.standalone_widget_box rule wraps it in the human's
					// `activity interactive` box. The QUALIFIER forms are untouched and
					// still demote-drop: "[Interactive Stop Watch] Placed over…" matches
					// EMBEDDED (not exact) and a span with more than one tag never has
					// tags.length === 1. Measured corpus-wide: 13 bare standalone
					// [Interactive] spans / 8 modules (AGH1001 ×5).
					// Data: _meta.qualifier_alias_demote.standalone_becomes.
					// Env toggle: INTALIAS_OFF (bare form reverts to the plain demote).
					const sb = qad.standalone_becomes;
					if (sb && tags.length === 1 && primary.how === "exact"
						&& !(typeof process !== "undefined" && process.env && process.env.INTALIAS_OFF)) {
						primary.tag = String(sb);
						primary.directive = "INTERACTIVE";
					} else {
						const kept = tags.filter((t) => !isQual(t));
						tags.length = 0; tags.push(...kept);
						primary = tags.length ? tags.reduce((best, t) => {
							const p = TagNormaliser.#PRECEDENCE[t.directive] ?? 0;
							const bp = TagNormaliser.#PRECEDENCE[best.directive] ?? 0;
							return p > bp ? t : best;
						}) : null;
					}
				}
			}
			// "TAG PROMOTION" — rewriting one tag into a different, related tag.
			//
			// Occasionally a tag the writer used resolves correctly, but the
			// way the human developer actually builds the page treats it as
			// a completely DIFFERENT (usually more specific) tag/container
			// convention. Rather than hard-coding a one-off special case, we
			// support a small, DATA-DRIVEN list of "promotion" rules: when
			// tag X is seen, rewrite it to tag Y so that whatever machinery
			// already exists for handling Y fires instead.
			//
			// The one rule defined today: "[Supervisor button]" is promoted
			// to "[Supervisor note]". Writers author a supervisor's
			// side-note as a green "button" element in the Writers
			// Template, but the actual human-built page renders it as the
			// SAME collapsible reveal panel used for genuine "[Supervisor
			// note]" tags elsewhere. By rewriting the tag here, it flows
			// through all of the existing supervisor-note panel-building
			// logic elsewhere in the pipeline (which all look for
			// `primary.tag === "supervisor note"`) without that logic
			// needing to know anything about "[Supervisor button]" at all.
			//
			// Data flag: Tag_Lexicon.json _meta.tag_promote (a list of {from, to, ...} rules)
			// Env toggle: each rule can carry its own toggle name (e.g.
			// SUPBUTTON_OFF for the supervisor-button rule above) to
			// disable just that one rule
			const tpr = this.#lexicon?._meta?.tag_promote;
			if (tpr && tpr.enabled !== false && primary) {
				for (const rule of (tpr.rules ?? [])) {
					if (rule.env && typeof process !== "undefined" && process.env && process.env[rule.env]) continue;
					let changed = false;
					for (const t of tags) {
						if (t.tag === rule.from) {
							t.tag = rule.to;
							if (rule.to_directive) t.directive = rule.to_directive;
							changed = true;
						}
					}
					if (changed) {
						primary = tags.reduce((best, t) => {
							const p = TagNormaliser.#PRECEDENCE[t.directive] ?? 0;
							const bp = TagNormaliser.#PRECEDENCE[best.directive] ?? 0;
							return p > bp ? t : best;
						});
					}
				}
			}
		}
		// THE [MTKquiz] FAMILY → ONE canonical "mtk quiz" ELEMENT tag (ROUND 232 —
		// Change Ledger CL-0038).
		//
		// A writer marks a D2L quiz with an "MTK quiz" span in a dozen spellings —
		// "[MTKQuiz]", "[MTK Quiz, supports engagement, audio, video, file
		// sharing]", "[Insert MTK Quiz – trigger engagement]", "[MTK quiz; trigger
		// engagement; self-marked]", a bracket-less red line ("Activity – long
		// answer MTK quiz, Kaiako marked"), even glued onto an activity opener
		// ("[Activity 1A: MTK Quiz]"). Measured live (outputs/_detect_mtkquiz.cjs,
		// all WTs: 33 spans / 21 modules), those forms resolved INCONSISTENTLY:
		// most hit the mcq INTERACTIVE via the embedded "quiz" alias (opening an
		// un-buildable bundle that swallowed the writer's quiz content into a
		// placeholder dump), the glued "[MTKQuiz]" forms were bare instructions,
		// the "Free text box…" form mis-resolved to a text box ELEMENT and the
		// "should go to teacher dropbox" form to dropdown. The design team's rule
		// (CL-0038): every such marker renders as the "Go to quiz" button + a
		// Designer/Developer To Do note, with the writer's quiz content kept.
		//
		// This step normalises the whole family AT THE PARSE LEVEL (the round-170
		// tag_promote class, but able to fire on tag-less instruction spans too):
		// when the span's text carries the MTK-quiz head (and is not the "[End of
		// MTK Quiz content]" CLOSER — that stays a CONTAINER_CLOSE), the
		// quiz-modifier junk tags (drop_tags — the mcq/engagement/text-box/
		// dropdown/etc. resolutions of the modifier prose; "dropbox" thus never
		// attaches a wrapper, per the rule) are removed and ONE "mtk quiz" ELEMENT
		// tag is injected. The primary is recomputed SURVIVORS-FIRST: a surviving
		// structural co-tag keeps governing ([Activity 1A: MTK Quiz] still opens
		// its activity box; ARFUN04's [Activity 1H drag and drop] keeps its
		// dragAndDrop bundle) and only when the old primary was itself dropped —
		// or the span had no tags at all — does "mtk quiz" take the slot. Because
		// the result is an ELEMENT, the scanner never opens a capturing bundle for
		// it, so the writer's quiz content flows to the normal body render
		// (constraint 1). A bracket-less span must be SHORT (bracketless_max_words)
		// so a long prose note that merely mentions an MTK quiz can never retag.
		// The button/note emission lives in ContentConverter (#mtkQuizEmit) off
		// data Emit_Templates.interactive_builders.mtk_quiz.
		// Data flag: Tag_Lexicon.json _meta.mtk_quiz_retag   Env toggle: MTKQUIZ_OFF
		{
			const mqr = this.#lexicon?._meta?.mtk_quiz_retag;
			if (mqr && mqr.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.MTKQUIZ_OFF)) {
				const headRe = new RegExp(mqr.head_pattern, "i");
				const exclRe = new RegExp(mqr.exclude_pattern, "i");
				if (headRe.test(s) && !exclRe.test(s)
					&& (tags.length || brackets.length
						|| s.trim().split(/\s+/).length <= (mqr.bracketless_max_words ?? 12))) {
					const drop = new Set(mqr.drop_tags ?? []);
					const oldPrimaryDropped = !!(primary && drop.has(primary.tag));
					const kept = tags.filter((t) => !drop.has(t.tag));
					tags.length = 0; tags.push(...kept);
					const canon = String(mqr.canonical ?? "mtk quiz");
					const mt = { tag: canon, directive: "ELEMENT", how: "mtk_retag", alias: canon };
					tags.push(mt);
					if (!primary || oldPrimaryDropped) {
						// SURVIVORS-FIRST, CONTAINER-FIRST recompute. The dropped primary was
						// an INTERACTIVE (precedence 7) that outranked every survivor; the
						// span's next-best GOVERNOR is a surviving [activity] CONTAINER_OPEN
						// (precedence 5) — NOT a decorative [H3] riding in the same span
						// (ELEMENT, 6). Without this preference, "[Activity 2B] [MTK quiz,
						// autograded…][H3]" (ARFUN02) recomputed to the h3 and the activity
						// box 2B silently vanished. A surviving activity therefore wins the
						// slot outright; otherwise the standard precedence reducer runs over
						// the survivors; a survivor-less span takes the injected mtk tag.
						const act = kept.find((t) => t.tag === "activity" && t.directive === "CONTAINER_OPEN");
						primary = act ?? (kept.length ? kept.reduce((best, t) => {
							const p = TagNormaliser.#PRECEDENCE[t.directive] ?? 0;
							const bp = TagNormaliser.#PRECEDENCE[best.directive] ?? 0;
							return p > bp ? t : best;
						}) : mt);
					}
				}
			}
		}
		if (tags.length) {
			cls = "tag";
		} else if (instructionFragment || this.#cuesRegex.test(s)
			|| (free && free.split(" ").length >= 3) || brackets.length
			|| this.#isMediaTimestampNote(free)) {
			// No tag was resolved, but SOMETHING here suggests it's
			// meaningful writer instruction text rather than pure noise —
			// either an instruction signal was detected, there's a
			// substantial amount of free text, there's a bracket we
			// couldn't resolve, OR it's a wholly-timestamp media-usage note
			// like "(to 1:00)" (see #isMediaTimestampNote below). In every
			// one of these cases we classify it as a writer instruction
			// (which later becomes a visible "red flag" note in the
			// output) — NEVER silently dropped, so a developer always sees
			// it and can act on it.
			cls = "instruction";
		} else {
			// bare numbers / split-span fractions → numbering/noise
			cls = "noise";
		}

		return {
			tags, primary, class: cls, instructionFragment,
			folded: s, remainders, hasBrackets: brackets.length > 0, numbers, free,
		};
	};

	/**
	 * A SECOND OPINION for one specific situation: "is this span REALLY a
	 * tag, or is it actually just an ordinary sentence that happens to
	 * mention some tag words in passing?"
	 *
	 * WHAT PROBLEM THIS SOLVES:
	 * Parse() above will classify a span as class:"tag" as soon as it finds
	 * ANY tag-word match inside it — even if that match was only found
	 * "embedded" deep inside a sentence (see #matchOne's "embedded" match
	 * type), rather than being a clean tag that leads the bracket. A writer
	 * can easily write an ordinary instruction to the page developer that
	 * just happens to use tag vocabulary as regular English words — e.g.
	 * "...reset the BUTTON at the end of this ACTIVITY" is really an
	 * instruction about a button and an activity, not an actual [button] or
	 * [activity] TAG. Parse() alone can't always tell the difference.
	 *
	 * This method gives a more careful second opinion for that specific
	 * case: a span only counts as "really an instruction in disguise" when
	 * ALL THREE of these are true —
	 *   1. every tag that WAS matched in it was matched via the "embedded"
	 *      method (buried mid-sentence, not leading the bracket cleanly)
	 *   2. it also contains a recognised writer-instruction cue word/phrase
	 *   3. it's a substantial amount of prose (at least `minWords` words,
	 *      default 8) — a short span is more likely a genuine tag
	 *
	 * WHO USES THIS AND WHY:
	 * InteractiveScanner calls this while it's in the middle of capturing
	 * the contents of an interactive widget. Without this check, a stray
	 * instruction sentence like the "reset the BUTTON..." example above
	 * would either wrongly STOP the widget-capture walk early (because it
	 * looks like a new "activity" tag has started) or get rendered as a
	 * bogus, empty element of its own. With this check, InteractiveScanner
	 * instead swallows the whole sentence as a plain instruction MEMBER of
	 * the widget it's already capturing.
	 *
	 * NOTE: this method does NOT change what Parse() itself returns — the
	 * span's overall `class` stays "tag" everywhere else in the pipeline.
	 * This is a narrowly-scoped extra check used only by the one caller
	 * that needs it.
	 *
	 * @param {Object} parse - the result object from Parse()
	 * @param {number} minWords - minimum word count to count as "substantial prose" (default 8)
	 * @returns {boolean} true when this span should be treated as an instruction, not a tag
	 */
	IsInstructionDominant(parse, minWords = 8) {
		if (!parse || parse.class !== "tag" || !parse.tags?.length) return false;
		if (!parse.tags.every((t) => t.how === "embedded")) return false;
		if (!this.#cuesRegex.test(parse.folded || "")) return false;
		return String(parse.folded || "").split(/\s+/).filter(Boolean).length >= minWords;
	};

	/**
	 * Is this span's free text NOTHING BUT a timestamp range in
	 * parentheses — e.g. "(to 1:00)" or "(0:10-1:48)"?
	 *
	 * WHY THIS MATTERS:
	 * A writer sometimes leaves a red note like this to tell Creative
	 * Services which portion of a video/audio clip to actually use — it's a
	 * genuine, meaningful instruction, not meaningless noise, even though
	 * it's short and doesn't contain any recognisable tag word or ordinary
	 * instruction-cue phrase. Without this check, a lone timestamp note
	 * like that would otherwise be classified as "noise" and silently
	 * dropped instead of being surfaced to the developer as an instruction.
	 *
	 * The exact pattern that counts as a "timestamp note" is DATA, not
	 * hard-coded here — it lives in Emit_Templates.json under
	 * elements.media_timestamp_note.pattern, so the shape can be tuned
	 * without touching this file. The compiled regular expression is built
	 * once, lazily, on first use (cached in the private #tsNoteRe field),
	 * rather than being rebuilt on every call.
	 *
	 * @param {string} free - the free (non-bracket) text of a span
	 * @returns {boolean} true when the free text is entirely a timestamp note
	 */
	#isMediaTimestampNote(free) {
		if (!free) return false;
		if (typeof process !== "undefined" && process.env && process.env.TIMESTAMPNOTE_OFF) return false;
		const d = (typeof DataService !== "undefined")
			&& DataService.Data?.EmitTemplates?.elements?.media_timestamp_note;
		if (!d || !d.enabled || !d.pattern) return false;
		if (!this.#tsNoteRe) this.#tsNoteRe = new RegExp(d.pattern, "i");
		return this.#tsNoteRe.test(free.trim());
	};
}

// Node test-harness hook (parity tests in the sandbox); browsers ignore it.
if (typeof module !== "undefined") module.exports = { TagNormaliser };
