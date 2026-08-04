/**
 * PrecedenceResolver.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * This file is the live engine's implementation of the PRECEDENCE CASCADE
 * (also called the "authority cascade") — a general-purpose lookup used
 * whenever the Writers Template genuinely does not specify enough detail
 * for one small piece of a page's layout (for example: exactly how wide
 * should one column of an overview menu be?). Instead of inventing an
 * arbitrary default for that gap, the cascade asks "what did the CLOSEST
 * already-built, related module do?" and copies that.
 *
 * TWO TERMS USED EVERYWHERE BELOW:
 *   - a module "code" — the short module identifier, e.g. "ENGC102".
 *   - a "key" — a short string identifying WHICH piece of page structure is
 *     being asked about, in the form "region|tag", e.g. "menu|@h5" means
 *     "the menu region's <h5> heading". resolve(code, key) is the entry point.
 * What the cascade actually looks up and compares is a "sig" (signature) —
 * a short, comparable fingerprint string capturing one structural fact
 * about one element, e.g. the literal string "col-md-6" for a column's
 * Bootstrap width class. The cascade's whole job is to predict/copy the
 * right sig for a given (code, key) from precedent.
 *
 * THE KEY IDEA — "ask the nearest relative first, then widen the search":
 * "Closest" is a ladder of increasingly wide circles of related modules.
 * The cascade tries the narrowest, most specific circle first, and only
 * widens to the next rung when the narrower one has no confident answer:
 *
 *   1 doc14                   — a curriculum lead's explicit, human-authored
 *                                default for this whole SUBJECT (see
 *                                Subject_Global_Parameters.json below). An
 *                                OVERRIDE — outranks every rung below it,
 *                                because it is direct human instruction,
 *                                not "what other modules happened to do".
 *   2 series_template         — the nearest previously-BUILT sibling(s) in
 *                                this module's own tight SERIES (e.g. all of
 *                                "BLL24") that also share its page TEMPLATE
 *                                type. Checked nearest-built-first.
 *   3 subject_phase_template  — every module sharing this module's SUBJECT
 *                                and year-LEVEL ("phase") and TEMPLATE type.
 *   4 subject_template        — every module sharing this module's SUBJECT
 *                                and TEMPLATE type (year-level no longer
 *                                required).
 *   5 subject                 — every module sharing this module's SUBJECT
 *                                (template type no longer required either).
 *   6 corpus                  — every module in the whole library. The last
 *                                resort, consulted only once nothing more
 *                                specific gave a confident answer.
 *
 * Levels 2–6 each apply a "SOLIDIFY" confidence test before trusting their
 * own answer (see #siblingChain / #consensus): the winning value must be
 * SOLIDLY, comfortably ahead of the runner-up — not a near-tie — and backed
 * by enough comparable modules. A shaky near-tie is refused, not guessed —
 * the search simply widens to the next rung instead. This is deliberate: a
 * weak majority is about as likely to be wrong as right, so the cascade
 * would rather honestly admit "not confident here" than force a guess. If
 * NONE of the six levels is confident and doc14 is silent too, resolve()
 * ESCALATES: it returns cleanly with escalate:true, the caller keeps
 * whatever default it already had, and — only where this is actually wired
 * into real output, see SHIPPED INERT below — a visible note is left for a
 * human developer instead of a silent guess. The corpus-wide majority
 * (level 6) is deliberately the LEAST-trusted, last-resort rung — never
 * treated as if it were the default answer.
 *
 * DATA OVER CODE: this file holds NO per-module logic and no hard-coded
 * subject/series lists. Everything above is DATA, loaded once via
 * DataService.Data and cached in this class's static fields (see #load):
 *   - ../data/Module_Structure_Index.json — a pre-built lookup table of
 *     what every module actually built. Its "modules" map gives, per
 *     module code and element key, the built {sig, n} pair (see
 *     #builtSig). Its "module_meta" map gives, per module code, that
 *     module's subject / template_type / phase / series / dev_order (see
 *     #metaFor). dev_order is a stand-in for "how early this module was
 *     built relative to its siblings" — level 2 (the nearest-sibling
 *     level) is "temporal": it only ever looks at candidates with a
 *     SMALLER dev_order than the module being resolved (built earlier),
 *     never at siblings built later. The wider consensus levels (3–6) are
 *     NOT temporal — they pool every matching module regardless of build
 *     order.
 *   - ../data/Precedence_Cascade.json — the six levels themselves in
 *     order, each with its own reliability floors (min_modules, window,
 *     window_agree, solidify_share, tie_defers_up, …) — see #floor for how
 *     a floor value is actually read — plus the live engine_inherit switch
 *     (see SHIPPED INERT below).
 *   - ../data/Subject_Global_Parameters.json — the human-authored per-
 *     subject override defaults consulted at level 1 ("doc14").
 *
 * This file is a MIRROR: a parallel Python implementation
 * (granular_consensus.resolve — used by this project's own internal
 * diagnostic/testing tooling, never shipped to end users) walks the
 * identical six-level ladder over the identical data files. An automated
 * parity test (reference/tests/_verify_precedence_parity.cjs) proves this
 * file's resolve() returns byte-identical answers to the Python one across
 * a large batch of real (code, key) pairs. If the logic here ever changes,
 * the Python twin needs the matching change, or the two will start
 * disagreeing — catching that disagreement is exactly what the parity
 * harness is for.
 *
 * WHEN TO WORK HERE:
 * - a cascade level's definition or reliability floor changes → edit the
 *   DATA file, ../data/Precedence_Cascade.json — not this file.
 * - the engine needs to consult the cascade for a new kind of ambiguous
 *   element → add a resolve() / resolveWidth() call at that call site.
 *
 * SHIPPED INERT: the one place this cascade is actually wired into real
 * converter output today — inheritMenu(), applied to the overview menu's
 * curriculum column width — is gated by the data flag
 * Precedence_Cascade.json engine_inherit.enabled (default FALSE) plus the
 * env var INHERIT_OFF, so by default every real conversion is byte-
 * identical to running with the cascade absent entirely. This is
 * deliberate caution, not an unfinished feature: the cascade's LOGIC is
 * built and proven correct (the parity harness above), but its live
 * application is being turned on gradually, one validated scope at a
 * time, rather than everywhere at once. env INHERIT_ON force-enables it
 * (e.g. for A/B testing); env INHERIT_OFF always wins and force-reverts
 * it, even over a data flag or caller option asking for it on.
 * ===========================================================================
 */

class PrecedenceResolver {

	// ---- cached data, loaded once by #load() from DataService.Data (see the file banner) ----
	static #idx = null;      // Module_Structure_Index.json's "modules": {code: {"region|tag": {sig, n}}} — what each module ACTUALLY built, per element (see #builtSig)
	static #meta = null;     // Module_Structure_Index.json's "module_meta": {code: {subject, template_type, prefix, phase, series, dev_order}} — per-module classification (see #metaFor)
	static #casc = null;     // Precedence_Cascade.json — the six cascade levels in order + their reliability floors + the engine_inherit live-application switch
	static #doc14 = null;    // Subject_Global_Parameters.json — the human-authored per-subject override defaults consulted at cascade level 1 ("doc14")
	static #memberCache = new Map();   // memoised #members() results: "code|group" -> [sibling module codes], so repeat lookups for the same module are free

	/**
	 * Reads one entry out of DataService.Data by its DATA-SERVICE key (e.g.
	 * "ModuleStructureIndex") — NOT the same thing as an "element key" like
	 * "menu|@h5" used everywhere else in this file; this `key` just names
	 * which whole JSON data file to fetch. Falls back to `fallback` when
	 * DataService itself isn't loaded/available (e.g. a bare unit test) or
	 * the key is missing. Every load in #load() goes through this one
	 * guarded read so a missing data file degrades to an empty/safe shape
	 * instead of throwing — worst case, the cascade simply finds no
	 * evidence anywhere and ESCALATEs, rather than crashing the converter.
	 *
	 * @param {string} key - the DataService.Data key, e.g. "PrecedenceCascade"
	 * @param {*} fallback - returned when DataService/the key is unavailable
	 * @returns {*} the loaded data, or `fallback`
	 */
	static #D(key, fallback) {
		return (typeof DataService !== "undefined" && DataService.Data && DataService.Data[key]) || fallback;
	}

	/**
	 * Lazily loads + caches the three data files this whole class runs on
	 * (see the file banner's DATA OVER CODE section). Every public method
	 * below calls this first; after the first call it's a no-op (guarded
	 * by `this.#idx === null`), so the JSON is only pulled out of
	 * DataService.Data once per page/session no matter how many resolve()
	 * calls follow. Call _reset() to force the next call to reload from
	 * scratch (the parity harness does this between test fixtures).
	 *
	 * @returns {void} populates #idx / #meta / #casc / #doc14 as a side effect
	 */
	static #load() {
		if (this.#idx === null) {
			const d = this.#D("ModuleStructureIndex", { modules: {}, module_meta: {} });
			this.#idx = d.modules || {};
			this.#meta = d.module_meta || {};
			this.#casc = this.#D("PrecedenceCascade", { _meta: { reliability_defaults: {} }, levels: [], confidence_by_level: {} });
			this.#doc14 = this.#D("SubjectParameters", { families: [] });
		}
	}

	// ---- MODULE METADATA — classify a code into subject/template/phase/series/dev_order (mirrors meta_for) ----
	/**
	 * Splits a module code into its letter PREFIX and digit SUFFIX, e.g.
	 * "ENGC102" → ["ENGC", "102"]. This is the FALLBACK path used only when
	 * a code has no entry in Module_Structure_Index.json's module_meta (see
	 * #metaFor) — it derives a rough phase/series straight from the digits
	 * (first digit = phase, first two digits = series) so a brand-new or
	 * otherwise-unindexed module can still be classified well enough to
	 * try the cascade, instead of the whole lookup silently failing.
	 *
	 * @param {string} code - a module code, e.g. "ENGC102"
	 * @returns {[string, string]} [prefix, digits], e.g. ["ENGC", "102"];
	 *   falls back to [code, ""] when the code doesn't start with letters
	 */
	static #splitCode(code) {
		const m = /^([A-Za-z]+)(\d*)/.exec(code || "");
		return m ? [m[1], m[2]] : [code, ""];
	}

	/**
	 * Looks up (or, failing that, DERIVES) a module's classification —
	 * subject, template_type, phase, series, dev_order — the exact fields
	 * every group-membership check (#members) and group label
	 * (#groupLabel) reads. This is the engine mirror of the Python
	 * meta_for().
	 *
	 * The preferred path is a direct hit in Module_Structure_Index.json's
	 * module_meta — e.g. for "AGH1001" the index holds:
	 *   { subject: "NCEA1", template_type: "Standard", prefix: "AGH",
	 *     phase: "AGH1", series: "AGH10", dev_order: 1001 }
	 * ("phase" = prefix + the first digit, roughly the year-level; "series"
	 * = prefix + the first two digits, the tight sibling group used by
	 * cascade level 2; dev_order here is literally the code's own digits,
	 * standing in for build order).
	 *
	 * When the code isn't in the index at all (an unindexed/new module),
	 * this FALLS BACK to #splitCode and derives a best-effort phase/
	 * series/dev_order from the code's own digits, leaving subject and
	 * template_type null — so any group check keyed on subject or
	 * template_type will simply find no match and move on, rather than
	 * the lookup throwing.
	 *
	 * @param {string} code - a module code, e.g. "AGH1001"
	 * @returns {{subject: ?string, template_type: ?string, prefix: string,
	 *   phase: ?string, series: ?string, dev_order: ?number}}
	 */
	static #metaFor(code) {
		this.#load();
		if (this.#meta[code]) return this.#meta[code];
		const [pre, digits] = this.#splitCode(code);
		return {
			subject: null, template_type: null, prefix: pre,
			phase: digits ? pre + digits.slice(0, 1) : null,
			series: digits.length >= 2 ? pre + digits.slice(0, 2) : (digits ? pre + digits : null),
			dev_order: digits ? parseInt(digits, 10) : null,
		};
	}

	/**
	 * Reads one RELIABILITY-FLOOR threshold for a cascade level — e.g.
	 * "min_modules" or "solidify_share", the tunable numbers that decide
	 * how much evidence, and how solid an agreement, is required before a
	 * level is allowed to answer at all. Falls back through three tiers:
	 * (1) the level's OWN override in Precedence_Cascade.json (e.g. level 3
	 * sets its own min_modules:3), else (2) the file's shared
	 * `_meta.reliability_defaults` block (the same value re-used by every
	 * level that doesn't override it, e.g. solidify_share defaults to
	 * 0.60 everywhere), else (3) the hard-coded `dflt` passed in by the
	 * caller, a last-ditch safety net for when the data file is missing
	 * entirely.
	 *
	 * @param {Object} level - one entry from Precedence_Cascade.json's levels[]
	 * @param {string} name - the floor's name, e.g. "min_modules", "window",
	 *   "window_agree", "solidify_share", "majority_share"
	 * @param {number} dflt - hard-coded fallback if neither data source has it
	 * @returns {number} the effective threshold to use
	 */
	static #floor(level, name, dflt) {
		if (level[name] !== undefined && level[name] !== null) return level[name];
		const rd = (this.#casc._meta && this.#casc._meta.reliability_defaults) || {};
		return rd[name] !== undefined ? rd[name] : dflt;
	}

	/**
	 * Looks up what a specific module ACTUALLY built for a specific
	 * element key — the raw fact every cascade level compares against.
	 * Reads straight out of the cached Module_Structure_Index.json (#idx):
	 * e.g. `#builtSig("AGH1001", "menu|@h5")` finds the index entry
	 * `{ sig: "h5@row>col=col-md-8", n: 10 }` and returns just the `sig`
	 * string, "h5@row>col=col-md-8". Returns null when the module has no
	 * record at all for that key (it never built that element, or isn't
	 * in the index) — callers treat null as "no evidence from this
	 * module", not as an error.
	 *
	 * @param {string} code - a module code, e.g. "AGH1001"
	 * @param {string} key - an element key, "region|tag", e.g. "menu|@h5"
	 * @returns {?string} the built signature string, or null if unknown
	 */
	static #builtSig(code, key) {
		const m = this.#idx[code];
		return m && m[key] ? m[key].sig : null;
	}

	// ---- GROUP MEMBERSHIP — "which other modules count as my series/subject/etc relatives?" (mirrors group_members) ----
	/**
	 * Finds every OTHER module that belongs to a named comparison GROUP
	 * for `code` — the pool of "relatives" one cascade level is allowed to
	 * look at. This is the engine mirror of the Python group_members(),
	 * and it is what actually implements the ladder's five non-override
	 * groups (levels 2–6); level 1, doc14, doesn't use group membership at
	 * all — see #doc14Governance for that instead.
	 *
	 * WHAT COUNTS AS "BELONGING", per group:
	 *   - "series" / "phase"        — same series / same phase as `code`
	 *                                 (a generic single-field match, kept
	 *                                 here for parity with the Python
	 *                                 helper's more general signature; not
	 *                                 used by any of the six SHIPPED
	 *                                 cascade levels today — level 2 uses
	 *                                 "series_template" below, not bare
	 *                                 "series").
	 *   - "series_template"         — LEVEL 2: same series AND same
	 *                                 template_type as `code`.
	 *   - "subject_phase_template"  — LEVEL 3: same subject, same phase's
	 *                                 year-digit, and same template_type.
	 *   - "subject_template"        — LEVEL 4: same subject and
	 *                                 template_type.
	 *   - "subject"                 — LEVEL 5: same subject.
	 *   - "corpus"                  — LEVEL 6: every module, unfiltered.
	 *
	 * `code` itself is always excluded from its own group. For the groups
	 * flagged "temporal" in Precedence_Cascade.json ("series"/"phase" and
	 * "series_template" — i.e. LEVEL 2), a candidate is ALSO excluded
	 * unless its dev_order is strictly smaller than `code`'s own dev_order
	 * — only previously-BUILT relatives count, never ones built later.
	 * The wider consensus groups (subject_phase_template / subject_template
	 * / subject / corpus) are NOT temporal: they pool every matching
	 * module regardless of build order.
	 *
	 * Results are memoised per (code, group) pair in #memberCache, since
	 * the same module/group combination is often re-asked for many
	 * different element keys within one batch of resolve() calls.
	 *
	 * @param {string} code - the module being resolved for, e.g. "ENGC102"
	 * @param {string} group - one of "series" | "phase" | "series_template"
	 *   | "subject_phase_template" | "subject_template" | "subject" | "corpus"
	 * @returns {string[]} module codes belonging to that group (`code` excluded)
	 */
	static #members(code, group) {
		const ck = code + "|" + group;
		if (this.#memberCache.has(ck)) return this.#memberCache.get(ck);
		const me = this.#metaFor(code);
		const myDo = me.dev_order;
		const out = [];
		for (const c in this.#idx) {
			if (c === code) continue;
			const m = this.#meta[c] || this.#metaFor(c);
			if (group === "series" || group === "phase") {
				if (me[group] == null || m[group] !== me[group]) continue;
				if (myDo != null && (m.dev_order == null || m.dev_order >= myDo)) continue;
			} else if (group === "series_template") {
				// LEVEL 2 — nearest previously-built sibling(s): SAME series AND SAME template (temporal — see the dev_order filter below)
				if (me.series == null || m.series !== me.series) continue;
				if (!me.template_type || m.template_type !== me.template_type) continue;
				if (myDo != null && (m.dev_order == null || m.dev_order >= myDo)) continue;
			} else if (group === "subject_phase_template") {
				// LEVEL 3 — same SUBJECT (pooled across its sibling prefixes) + same year-LEVEL + same TEMPLATE (NOT temporal — build order doesn't matter here)
				if (!me.subject || m.subject !== me.subject) continue;
				if (!me.template_type || m.template_type !== me.template_type) continue;
				const myd = (me.phase || "").slice(-1);
				if (!myd || (m.phase || "").slice(-1) !== myd) continue;
			} else if (group === "subject_template") {
				if (!me.subject || m.subject !== me.subject) continue;
				if (!me.template_type || m.template_type !== me.template_type) continue;
			} else if (group === "subject") {
				if (!me.subject || m.subject !== me.subject) continue;
			} else if (group === "corpus") {
				/* all */
			} else continue;
			out.push(c);
		}
		this.#memberCache.set(ck, out);
		return out;
	}

	/**
	 * Renders a short, HUMAN-READABLE label for a comparison group, e.g.
	 * "NCEA1 · level 1 · Standard" for a subject_phase_template group, or
	 * "AGH10 · Standard" for a series_template group. Used purely for
	 * DISPLAY/DIAGNOSTICS — it becomes the `reference` field of a
	 * #consensus-decided resolve() result (see resolve()'s return shape),
	 * so a developer reading a resolution can see at a glance which pool
	 * of modules an answer came from, without re-deriving it themselves.
	 * (A #siblingChain result uses an actual module code as `reference`
	 * instead — a single sibling, not a labelled group — so this function
	 * is only ever called for the four "consensus" groups.)
	 *
	 * @param {string} code - the module being resolved for
	 * @param {string} group - the comparison group name (see #members)
	 * @returns {string} a short display label for that group
	 */
	static #groupLabel(code, group) {
		const m = this.#metaFor(code);
		if (group === "series") return m.series || "?";
		if (group === "series_template") return `${m.series} · ${m.template_type}`;
		if (group === "phase") return m.phase || "?";
		if (group === "subject_phase_template") return `${m.subject} · level ${(m.phase || "?").slice(-1)} · ${m.template_type}`;
		if (group === "subject_template") return `${m.subject} / ${m.template_type}`;
		if (group === "subject") return m.subject || "?";
		return "corpus";
	}

	// ---- LEVEL DECIDERS — the two ways a level can reach a confident answer (mirrors _sibling_chain / _consensus) ----
	/**
	 * LEVEL 2's decider — "do my nearest-built siblings agree?" Only the
	 * series_template level uses this (the one "sibling_chain"-kind level
	 * in Precedence_Cascade.json); every other level uses #consensus.
	 *
	 * HOW IT DECIDES:
	 *  1. Collect every sibling in `level.group` (via #members) that has a
	 *     built sig for this `key` (via #builtSig), each tagged with its
	 *     own dev_order.
	 *  2. Sort NEAREST-BUILT-FIRST — the highest dev_order (built latest,
	 *     but still earlier than `code`, since #members already excluded
	 *     later siblings) comes first; ties break on code then sig, purely
	 *     so this sort matches the Python implementation's byte-for-byte.
	 *  3. Keep only the nearest WINDOW of siblings (how many is
	 *     `level.window`, default 5 — see #floor), deliberately NOT the
	 *     whole series: a value from 10 modules ago is a much weaker
	 *     signal than one from the module built immediately before.
	 *  4. Within that window, find the most-common sig. If it's shared by
	 *     at least `window_agree` (default 0.75, i.e. 75%) of the window,
	 *     that's a CLEAN decision; otherwise the window is too "mixed" to
	 *     trust and this level is skipped (the cascade widens to level 3).
	 *
	 * @param {string} code - the module being resolved for
	 * @param {string} key - the element key being resolved, e.g. "menu|@h5"
	 * @param {Object} level - the series_template level definition from
	 *   Precedence_Cascade.json (reads .group, .window, .window_agree)
	 * @returns {[?Object, string]} a [decision, reason] pair. On success,
	 *   decision looks like { reference: "AGH1005", reference_sig:
	 *   "col-md-8", n_modules: 3, majority_share: 1.0, window: [{code,
	 *   sig}, …] } and reason is "clean". On failure decision is null and
	 *   reason explains why: "empty" (no siblings had any built sig for
	 *   this key) or "mixed" (the window didn't solidly agree).
	 */
	static #siblingChain(code, key, level) {
		const preds = [];
		for (const c of this.#members(code, level.group)) {
			const sig = this.#builtSig(c, key);
			if (sig == null) continue;
			const m = this.#meta[c] || this.#metaFor(c);
			preds.push([m.dev_order == null ? -1 : m.dev_order, c, sig]);
		}
		if (!preds.length) return [null, "empty"];
		// nearest-lower first; mirror Python's reverse tuple sort (dev_order, code, sig) exactly
		preds.sort((a, b) => (b[0] - a[0])
			|| (a[1] < b[1] ? 1 : a[1] > b[1] ? -1 : 0)
			|| (a[2] < b[2] ? 1 : a[2] > b[2] ? -1 : 0));
		const W = Math.trunc(this.#floor(level, "window", 5));
		const thr = Number(this.#floor(level, "window_agree", 0.75));
		const win = preds.slice(0, W);
		const cnt = new Map();
		for (const [, , s] of win) cnt.set(s, (cnt.get(s) || 0) + 1);
		let topSig = null, topN = -1;
		for (const [s, n] of cnt) if (n > topN) { topSig = s; topN = n; }
		if (topN / win.length < thr) return [null, "mixed"];
		const refCode = win.find(([, , s]) => s === topSig)[1];
		return [{
			reference: refCode, reference_sig: topSig, n_modules: preds.length,
			majority_share: Math.round((topN / win.length) * 1000) / 1000,
			window: win.map(([, c, s]) => ({ code: c, sig: s })),
		}, "clean"];
	}

	/**
	 * LEVELS 3–6's decider — "does this WHOLE group solidly agree?" Used
	 * by every level whose Precedence_Cascade.json entry has
	 * kind:"consensus" (subject_phase_template, subject_template,
	 * subject, corpus). Unlike #siblingChain, there's no window and no
	 * build-order weighting here — every module in the group gets an
	 * equal vote.
	 *
	 * HOW IT DECIDES:
	 *  1. Collect the built sig (via #builtSig) from every member of
	 *     `level.group` (via #members) that has one for this `key`.
	 *  2. Tally how many modules built each distinct sig, and rank the
	 *     tallies highest-first (ties keep first-seen order, purely to
	 *     match the Python Counter.most_common() tie-break exactly).
	 *  3. Refuse to answer at all ("thin") if fewer than `min_modules`
	 *     comparable modules exist — too small a sample to trust, no
	 *     matter how unanimous it looks.
	 *  4. Otherwise apply the level's confidence rule, `level.decision`:
	 *       - "solidify" (used by every consensus level shipped today):
	 *         accept a majority value here only when it is SOLIDLY ahead
	 *         of the runner-up (its share of all votes must be at or
	 *         above `solidify_share`, default 0.60 — "at least 60% of
	 *         comparable modules agree, clearly ahead of second place")
	 *         AND it isn't tied with the runner-up (unless the level sets
	 *         tie_defers_up:false). Anything short of that is an
	 *         ambiguous split: OMIT an answer at this level and let the
	 *         cascade defer to the next, wider level instead of guessing.
	 *       - "plurality": only the tie check applies (whoever has the
	 *         most votes wins, ties excepted) — a looser rule kept for
	 *         completeness/parity with the Python side; not used by any
	 *         level shipped today.
	 *       - anything else (the "majority" default): a plain
	 *         top-share-vs-`majority_share` cutoff, no tie handling.
	 *
	 * @param {string} code - the module being resolved for
	 * @param {string} key - the element key being resolved, e.g. "menu|@h5"
	 * @param {Object} level - the level definition from
	 *   Precedence_Cascade.json (reads .group, .decision, .min_modules,
	 *   .solidify_share / .majority_share, .tie_defers_up)
	 * @returns {[?Object, string]} a [decision, reason] pair. On success,
	 *   decision looks like { reference: "NCEA1 · level 1 · Standard",
	 *   reference_sig: "col-md-8", n_modules: 27, majority_share: 0.89,
	 *   variants: 2 } and reason is "clean". On failure decision is null
	 *   and reason is "empty" (no evidence), "thin" (below min_modules),
	 *   "tie", "unsolid" (solidify_share not met), or "mixed" (majority_share
	 *   not met).
	 */
	static #consensus(code, key, level) {
		const sigs = [];
		for (const c of this.#members(code, level.group)) {
			const s = this.#builtSig(c, key);
			if (s != null) sigs.push(s);
		}
		if (!sigs.length) return [null, "empty"];
		const cnt = new Map();
		for (const s of sigs) cnt.set(s, (cnt.get(s) || 0) + 1);
		// count desc, ties keep first-seen order (stable sort) -> mirrors Python Counter.most_common
		const ranked = [...cnt.entries()].sort((a, b) => b[1] - a[1]);
		const [topSig, topN] = ranked[0];
		const n = sigs.length;
		if (n < Math.trunc(this.#floor(level, "min_modules", 5))) return [null, "thin"];
		const dec = level.decision || "majority";
		if (dec === "solidify") {
			// a SOLID dominant value only: a tie (see tie_defers_up), or a top-share below the
			// solidify_share floor, is an ambiguous split -> OMIT an answer here + defer up to the next, wider level
			if ((level.tie_defers_up !== false) && ranked.length > 1 && ranked[1][1] === topN) return [null, "tie"];
			if ((topN / n) < Number(this.#floor(level, "solidify_share", 0.60))) return [null, "unsolid"];
		} else if (dec === "plurality") {
			if ((level.tie_defers_up !== false) && ranked.length > 1 && ranked[1][1] === topN) return [null, "tie"];
		} else if ((topN / n) < Number(this.#floor(level, "majority_share", 0.60))) {
			return [null, "mixed"];
		}
		return [{
			reference: this.#groupLabel(code, level.group), reference_sig: topSig,
			n_modules: n, majority_share: Math.round((topN / n) * 1000) / 1000, variants: ranked.length,
		}, "clean"];
	}

	// ---- SUBJECT-WIDE OVERRIDES (cascade level 1) — human-authored defaults that outrank the rest of the ladder (mirrors doc14_governance) ----
	/**
	 * Finds which subject-wide parameter FAMILIES (from
	 * Subject_Global_Parameters.json) apply to `code` at all — before even
	 * asking whether any of their conventions actually govern the element
	 * being resolved (that part is #doc14Governance). A family is IN SCOPE
	 * for `code` when: it is marked `active`, `code` starts with one of
	 * its `scope.prefixes` / `scope.cohort_prefixes` (case-insensitive — a
	 * family can cover several related prefixes together, e.g. one family
	 * covers HES/PHE/PES/HPE as a single cohort), and — if the family
	 * restricts itself to one year-level via `scope.level` — the digit
	 * right after `code`'s prefix matches that level.
	 *
	 * @param {string} code - a module code, e.g. "BLL241"
	 * @returns {Object[]} the matching, active family objects from
	 *   Subject_Global_Parameters.json (usually 0 or 1; a code could in
	 *   theory match more than one family)
	 */
	static #scopeMatch(code) {
		this.#load();
		const [pre, digits] = this.#splitCode(code);
		const level = digits ? digits[0] : null;
		const out = [];
		for (const fam of (this.#doc14.families || [])) {
			if (!fam.active) continue;
			const sc = fam.scope || {};
			// r218: a scope's exclude_prefixes carves a LONGER sibling prefix OUT of a
			// shorter one's reach (doc-14 §14.9/§14.11 — BLLR is a distinct series BLL must
			// NOT bind; PHEFUN/HPFUN belong to §14.5, not the §14.8 content cohort).
			// Mirrors subject_parameters.scope_match exactly (parity contract).
			if ((sc.exclude_prefixes || []).some((x) => code.toUpperCase().startsWith(x.toUpperCase()))) continue;
			const prefixes = [...(sc.prefixes || []), ...(sc.cohort_prefixes || [])];
			if (!prefixes.some((p) => code.toUpperCase().startsWith(p.toUpperCase()))) continue;
			if (sc.level != null && String(level) !== String(sc.level)) continue;
			out.push(fam);
		}
		return out;
	}

	/**
	 * LEVEL 1's decider — does a human-authored subject-wide default
	 * actually GOVERN this specific element key? #scopeMatch has already
	 * narrowed things down to the subject families that cover `code` at
	 * all; this walks each matching family's `conventions[]` looking for
	 * one whose `registry_check` names exactly this element (region + tag)
	 * and states what value it expects there (`expect_contains`, matched
	 * loosely — see resolve()'s `match: "contains"` handling for level 1).
	 * Not every convention even HAS a `registry_check` — many are
	 * prose-only guidance meant for a human, not a code-checkable
	 * structural claim — those are silently skipped, since there's
	 * nothing for the cascade to automatically apply.
	 *
	 * Matches BOTH the plain-tag form of a key ("body|activity") and the
	 * rendered-HTML-tag form ("menu|@h5"), since `expect_contains`
	 * conventions are written against either shape depending on the family.
	 *
	 * @param {string} code - a module code, e.g. "BLL241"
	 * @param {string} key - the element key being resolved, e.g. "body|activity"
	 * @returns {?{family: string, convention: string, token: string}} the
	 *   governing family id + convention name + expected token, or null
	 *   when no active family's convention governs this key
	 */
	static #doc14Governance(code, key) {
		for (const fam of this.#scopeMatch(code)) {
			for (const conv of (fam.conventions || [])) {
				const rc = conv.registry_check || {};
				const { region, tag, expect_contains: token } = rc;
				if (region && tag && token && (key === `${region}|${tag}` || key === `${region}|@${tag}`)) {
					// r218: overrides_gold = the family is a FORWARD-LOOKING directive that also
					// outranks the module's own human gold (the gold may predate the rule) —
					// carried through so resolve()'s answer is self-describing for stocktakes.
					return { family: fam.id, convention: conv.name, token, overrides_gold: !!fam.overrides_gold };
				}
			}
		}
		return null;
	}

	// ---- THE CASCADE ITSELF — walk all six levels in order, return on the first clean answer (mirrors granular_consensus.resolve) ----
	/**
	 * THE ENTRY POINT of the whole file — walks the precedence cascade for
	 * one (module, element) pair and returns what to inherit, or a clean
	 * instruction to escalate instead of guessing. This is the JavaScript
	 * twin of the Python granular_consensus.resolve(); see the file
	 * banner's MIRROR paragraph for the parity guarantee between them.
	 *
	 * HOW IT WALKS THE LADDER:
	 * Reads the ordered `levels` array straight out of
	 * Precedence_Cascade.json (see the file banner for what the six
	 * shipped levels are) and tries them in order, RETURNING IMMEDIATELY
	 * on the first one that produces a confident answer:
	 *   - the "override" level (doc14) asks #doc14Governance whether a
	 *     human-authored subject default governs this exact key; if so,
	 *     that wins outright and nothing below it is even considered;
	 *   - a "sibling_chain" level (only level 2 today) asks #siblingChain;
	 *   - every other ("consensus") level asks #consensus.
	 * Whichever function answers, its `[decision, reason]` pair is
	 * unpacked (see #siblingChain / #consensus for what the reason codes
	 * mean) — a non-null decision returns immediately; a null decision is
	 * recorded in `tried` (e.g. "series_template:mixed") and the loop
	 * moves on to the next, WIDER level. If every level comes back
	 * empty-handed, the final return has `escalate: true` — see
	 * escalateNote() for how that actually surfaces to a human developer
	 * once this is wired into live output.
	 *
	 * EXAMPLE — a clean level-2 decision (a nearby sibling settles it):
	 *   PrecedenceResolver.resolve("AGH1006", "menu|@h5")
	 *   // => {
	 *   //   escalate: false, level: 2, authority: "series_template_precedence",
	 *   //   reference: "AGH1005", reference_sig: "col-md-8",
	 *   //   match: "equals", majority_share: 1, n_modules: 1,
	 *   //   confidence: "high", window: [{ code: "AGH1005", sig: "col-md-8" }],
	 *   //   tried: [],
	 *   // }
	 *   // i.e. "AGH1006 should inherit col-md-8 for its menu <h5>, because
	 *   // its nearest built sibling AGH1005 built col-md-8 there."
	 *
	 * EXAMPLE — nothing in the whole cascade was confident (ESCALATE):
	 *   PrecedenceResolver.resolve("BLL244", "menu|@h5")
	 *   // => {
	 *   //   escalate: true, level: null, authority: "none",
	 *   //   reference: null, reference_sig: null, match: null,
	 *   //   majority_share: null, n_modules: null, confidence: "none",
	 *   //   tried: ["doc14:silent", "series_template:mixed",
	 *   //           "subject_phase_template:unsolid", …, "corpus:unsolid"],
	 *   //   note: "no cascade level yielded a clean answer and doc-14 is "
	 *   //         + "silent — keep the default.",
	 *   // }
	 *   // i.e. every level was tried and logged in `tried`, none could
	 *   // solidly confirm a value, so the caller should keep its existing
	 *   // default rather than have the cascade invent one.
	 *
	 * @param {string} code - the module code being resolved for, e.g. "AGH1006"
	 * @param {string} key - the element key, "region|tag", e.g. "menu|@h5"
	 * @returns {Object} a resolution object. Always carries `escalate`
	 *   (boolean) and `tried` (string[] of "levelId:reason" entries for
	 *   every level that did NOT decide). When `escalate` is false it also
	 *   carries `level` (which of the six levels answered, 1–6),
	 *   `authority` (that level's authority name), `reference` (the
	 *   sibling code or group label the answer came from), `reference_sig`
	 *   (the sig/value to inherit), `match` ("equals" or "contains" — how
	 *   strictly a caller should compare against `reference_sig`),
	 *   `majority_share`, `n_modules`, `confidence` (a human-readable label
	 *   from confidence_by_level), and — level-1 only — `convention`, or —
	 *   level-2 only — `window`. When `escalate` is true it also carries a
	 *   `note` string meant to be shown to a developer.
	 */
	static resolve(code, key) {
		this.#load();
		const conf = this.#casc.confidence_by_level || {};
		const tried = [];
		for (const level of (this.#casc.levels || [])) {
			const lid = level.id;
			if (level.kind === "override" || lid === "doc14") {
				const g = this.#doc14Governance(code, key);
				if (g) {
					return {
						escalate: false, level: level.n || 1, authority: "doc14",
						reference: g.family, reference_sig: g.token, match: "contains",
						majority_share: null, n_modules: null,
						confidence: conf[String(level.n || 1)] || "authoritative",
						convention: g.convention, doc14_override: !!g.overrides_gold,
						tried: tried.slice(),
					};
				}
				tried.push("doc14:silent");
				continue;
			}
			const [d, reason] = level.kind === "sibling_chain"
				? this.#siblingChain(code, key, level)
				: this.#consensus(code, key, level);
			if (d) {
				return {
					escalate: false, level: level.n, authority: level.authority,
					reference: d.reference, reference_sig: d.reference_sig,
					match: level.match || "equals", majority_share: d.majority_share,
					n_modules: d.n_modules, confidence: conf[String(level.n)] || "medium",
					window: d.window, tried: tried.slice(),
				};
			}
			tried.push(`${lid}:${reason}`);
		}
		return {
			escalate: true, level: null, authority: "none", reference: null,
			reference_sig: null, match: null, majority_share: null, n_modules: null,
			confidence: "none", tried,
			note: "no cascade level yielded a clean answer and doc-14 is silent — keep the default.",
		};
	}

	// ---- ENGINE HELPERS — turning a raw resolve() answer into something ContentConverter/MenuBuilder can actually apply ----
	/**
	 * Convenience wrapper around resolve() for the one concrete use case
	 * this file actually ships today: "what Bootstrap column-width class
	 * (col-md-N) does the cascade authorise for this key?" Calls
	 * resolve() and, only when it returned a clean "equals"-match answer
	 * (a level-1 "contains" answer doesn't qualify — a doc14 token isn't
	 * guaranteed to BE a width class — and neither does an escalation,
	 * which has no reference_sig at all), extracts the col-md-N token
	 * from `reference_sig`. If the winning sig isn't actually a
	 * column-width string (e.g. it's a tag/wrapper signature for some
	 * other kind of element), `width` comes back null even though
	 * `resolution.escalate` is false — callers must check `width`, not
	 * just `!resolution.escalate`.
	 *
	 * @param {string} code - the module code being resolved for
	 * @param {string} key - the element key, e.g. "menu|@h5"
	 * @returns {{width: ?string, resolution: Object}} `width` is a string
	 *   like "col-md-8", or null when the cascade escalated, matched via
	 *   "contains", or its answer wasn't a column-width sig. `resolution`
	 *   is always the full resolve() object, so a caller can still build
	 *   an escalateNote()-style advisory even when width is null.
	 */
	static resolveWidth(code, key) {
		const r = this.resolve(code, key);
		if (r.escalate || r.match !== "equals") return { width: null, resolution: r };
		const m = /col-md-\d+/.exec(r.reference_sig || "");
		return { width: m ? m[0] : null, resolution: r };
	}

	/**
	 * Decides whether inheritMenu()'s LIVE application should actually run
	 * for this call — see the file banner's SHIPPED INERT section for why
	 * this defaults to off. Checked in this priority order, highest wins:
	 *   1. env INHERIT_OFF — force-revert; always wins, even over an
	 *      explicit opts.enabled:true.
	 *   2. env INHERIT_ON  — force-enable (used for A/B-testing a batch
	 *      conversion with the cascade switched on, without editing the
	 *      data file).
	 *   3. opts.enabled    — an explicit caller override (used by the
	 *      parity/A-B test harness to flip the mechanism on for a single
	 *      call without touching env vars or the data file).
	 *   4. the data flag   — Precedence_Cascade.json
	 *      engine_inherit.enabled, the SHIPPED default (false).
	 *
	 * @param {{enabled?: boolean}} [opts] - optional caller override; only
	 *   consulted when neither env var is set
	 * @returns {boolean} true only when the live application should run
	 */
	static inheritEnabled(opts) {
		opts = opts || {};
		const cfg = (this.#D("PrecedenceCascade", {}).engine_inherit) || {};
		const env = (typeof process !== "undefined" && process.env) || {};
		if (env.INHERIT_OFF) return false;          // force-revert (A/B), outranks everything
		if (env.INHERIT_ON) return true;            // force-on (A/B / scoped-ship of the ON state)
		return opts.enabled != null ? !!opts.enabled : !!cfg.enabled;
	}

	/**
	 * THE LIVE APPLICATION of the whole cascade to real converter output —
	 * and the SHIPPED-INERT mechanism described in the file banner: with
	 * the default data flag (engine_inherit.enabled:false),
	 * inheritEnabled() returns false and this function returns `menu`
	 * completely UNCHANGED on its very first line, so real conversions
	 * are byte-identical to the cascade not existing at all, and every
	 * protected output gate holds by construction.
	 *
	 * WHEN ENABLED: the overview menu's CURRICULUM column width is
	 * GENERATED by asking the cascade (resolveWidth — "what did the
	 * nearest previously-developed relative build here?") instead of
	 * coming from MenuBuilder's static per-template registry default, so
	 * a module can automatically pick up its nearest sibling's width
	 * rather than a one-size-fits-all fallback. On ESCALATE (the cascade
	 * had no confident answer anywhere), the existing default width is
	 * KEPT untouched and a visible, gate-neutral cv2-note developer
	 * advisory (escalateNote) is prepended to the menu instead — visible
	 * to a human reviewer, never a silent guess.
	 *
	 * `menu` is the plain object of HTML-pane strings (and/or structured
	 * column arrays) that MenuBuilder.buildMenu() builds; this function
	 * mutates + returns that SAME object (not a copy).
	 *
	 * @param {Object} menu - MenuBuilder.buildMenu()'s output object, e.g.
	 *   { tab1: "<div…", tab2Cols: [{cls, html}, …], … }
	 * @param {string} code - the module code the menu belongs to
	 * @param {{enabled?: boolean}} [opts] - forwarded to inheritEnabled()
	 * @returns {Object} the same `menu` object, mutated in place when the
	 *   cascade was enabled and had something to apply
	 */
	static inheritMenu(menu, code, opts) {
		if (!menu || !this.inheritEnabled(opts)) return menu;      // INERT default → byte-identical
		const cfg = (this.#D("PrecedenceCascade", {}).engine_inherit) || {};
		const key = cfg.menu_curric_key || "menu|@h5";
		const panes = ["tab1", "tab2", "content", "left", "right"];
		const { width, resolution } = this.resolveWidth(code, key);
		if (resolution.escalate) {                                  // keep the default + a visible advisory
			const note = this.escalateNote(code, key, resolution);
			for (const k of panes) {
				if (typeof menu[k] === "string" && menu[k].trim()) { menu[k] = note + "\n" + menu[k]; break; }
			}
			return menu;
		}
		if (!width) return menu;                                    // cascade sig isn't a plain col-md width
		// TARGET the CURRICULUM column only — the col carrying an <h5> heading — so a legitimate
		// multi-column layout (e.g. a col-md-12 band + curriculum col) is preserved, not collapsed.
		// The STRUCTURED cols (menu.tab1Cols/tab2Cols, rendered by SkeletonBuilder) carry
		// the width in .cls; the flat string panes carry it inline. Both handled, curriculum-scoped.
		const setCurric = (cols) => Array.isArray(cols) ? cols.map((c) =>
			(c && typeof c.cls === "string" && typeof c.html === "string" && /<h[45]/i.test(c.html))
				? Object.assign({}, c, { cls: c.cls.replace(/\bcol-md-(?:6|8|12)\b/, width) }) : c) : cols;
		if (menu.tab1Cols) menu.tab1Cols = setCurric(menu.tab1Cols);
		if (menu.tab2Cols) menu.tab2Cols = setCurric(menu.tab2Cols);
		// flat-pane form: swap only inside a curriculum column div that carries an <h5>
		for (const k of panes) {
			if (typeof menu[k] === "string" && /<h[45]/i.test(menu[k])) {
				menu[k] = menu[k].replace(/(<div class="[^"]*?)\bcol-md-(?:6|8|12)\b([^"]*"[^>]*>(?:(?!<\/div>)[\s\S])*?<h[45])/gi,
					(m, a, b) => a + width + b);
			}
		}
		return menu;
	}

	/**
	 * Builds the visible developer advisory shown when the cascade
	 * ESCALATES (see resolve()) — the "give up cleanly and leave a note"
	 * half of the escalate behaviour described in the file banner.
	 * Renders as a `cv2-note`-classed paragraph, the same CSS class this
	 * codebase uses for every other developer-facing retained note/
	 * red-flag, which is why it's "gate-neutral": every protected
	 * output-comparison gate already knows to ignore `cv2-note` content
	 * when judging a match to the human-built reference HTML, so this
	 * advisory can be shown without ever being mistaken for real page
	 * content. It lists every level that was tried and why each declined
	 * (`resolution.tried`, e.g. "series_template:mixed"), so a developer
	 * can see at a glance which rungs of the ladder were considered
	 * before the cascade gave up.
	 *
	 * @param {string} code - the module code (not referenced in the
	 *   rendered text below; kept for a consistent call signature with
	 *   the other resolve-adjacent helpers)
	 * @param {string} key - the element key that couldn't be resolved,
	 *   e.g. "menu|@h5"
	 * @param {Object} resolution - the escalated resolve() return value
	 *   (reads resolution.tried)
	 * @returns {string} an HTML `<p class="cv2-note">…</p>` string
	 */
	static escalateNote(code, key, resolution) {
		const t = (resolution && resolution.tried) ? resolution.tried.join(", ") : "";
		return `<p class="cv2-note" style="color:red;font-weight:bold;">RED FLAG: no inherited `
			+ `structure for ${key} — the precedence cascade found no clean precedent `
			+ `(${t}); kept the default (developer: confirm against doc 14 / the series predecessor).</p>`;
	}

	/**
	 * REFERENCE-MODULE SUGGESTION (ROUND 249 — the HTML Generator's
	 * "Reference module" panel). Names the nearest already-built module a
	 * new conversion would most naturally inherit from — the same "ask the
	 * nearest relative first, then widen" idea as the cascade above, but
	 * answering the coarser, person-facing question "WHICH ONE module is
	 * my reference?" rather than resolving one element key. Display-only:
	 * nothing in the conversion reads this — the actual inheritance stays
	 * with ModuleResolver.Resolve / this cascade, and only an EXPLICIT
	 * user override (PrepareRun's referenceCode option) changes anything.
	 *
	 * HOW IT CHOOSES (Gavin's two-tier rule, round 250 — deliberately NO
	 * wider fallback):
	 *   1. SAME MODULE SERIES — same code prefix + same leading digit
	 *      (OSAI502 → the OSAI5xx family → OSAI501 first and foremost);
	 *   2. SAME SUBJECT AT THE SAME PHASE — a different prefix in the same
	 *      subject whose leading digit matches (no OSAI5xx on record →
	 *      an Online Safety 5xx sibling: OSOH501 / OSBY501 / …). For a
	 *      code the index has never seen, the subject is borrowed from any
	 *      indexed module sharing its prefix.
	 * Inside a tier, prefer the nearest EARLIER-built module (dev_order
	 * below this code's own — the "module this one continues from"),
	 * falling back to the nearest later one when nothing earlier exists.
	 * When NEITHER tier holds a module, return null — the UI then demands
	 * an explicit choice ("Please select a reference module") or a
	 * reference-HTML upload before converting.
	 *
	 * @param {string} code - the module being converted, e.g. "OSAI502"
	 * @returns {?{code: string, group: string, why: string, meta: Object}}
	 *   the suggested reference module, or null when neither tier holds
	 *   a relative (a brand-new subject/series)
	 */
	static SuggestReference(code) {
		this.#load();
		if (!code) return null;
		const me = this.#metaFor(code);
		const mine = me.dev_order ?? Infinity;
		// the subject may be unknown for a brand-new code — borrow it from
		// any indexed module sharing the letter prefix (OSAI → Online Safety)
		let subject = me.subject;
		if (!subject && me.prefix) {
			for (const c in this.#meta) {
				if (this.#meta[c].prefix === me.prefix) { subject = this.#meta[c].subject; break; }
			}
		}
		const digit = (me.phase || "").slice(-1);
		const nearest = (list) => {
			if (!list.length) return null;
			const earlier = list.filter(([, m]) => m.dev_order != null && m.dev_order < mine);
			const pool = earlier.length ? earlier : list;
			pool.sort((a, b) =>
				Math.abs((a[1].dev_order ?? 0) - mine) - Math.abs((b[1].dev_order ?? 0) - mine)
				|| (a[0] < b[0] ? -1 : 1));
			return pool[0][0];
		};
		const circles = [
			["series", (m) => me.phase && m.phase === me.phase,
				"the nearest already-built module in the same module series"],
			["subject_phase", (m) => subject && m.subject === subject
				&& digit && (m.phase || "").slice(-1) === digit,
				"the nearest already-built module in the same subject at the same phase"],
		];
		const cands = [];
		for (const c in this.#meta) {
			if (c !== code) cands.push([c, this.#meta[c]]);
		}
		for (const [group, test, why] of circles) {
			const hit = nearest(cands.filter(([, m]) => test(m)));
			if (hit) return { code: hit, group, why, meta: this.#meta[hit] };
		}
		return null;
	}

	/**
	 * TEST-ONLY hook: clears every cached/memoised field (#idx, #meta,
	 * #casc, #doc14, #memberCache) so the NEXT call to #load() re-reads
	 * DataService.Data from scratch instead of reusing whatever was
	 * cached from a previous test's fixture data. Production code never
	 * needs to call this — #load()'s cache is meant to live for the whole
	 * page/session. The parity harness
	 * (reference/tests/_verify_precedence_parity.cjs) calls it between
	 * test fixtures so each one starts from a clean slate.
	 *
	 * @returns {void}
	 */
	static _reset() { this.#idx = null; this.#meta = null; this.#casc = null; this.#doc14 = null; this.#memberCache.clear(); }
}

// Node test-harness hook: the browser ignores this (module is undefined); the parity
// harness (reference/tests/_verify_precedence_parity.cjs) and other node test scripts
// require() this class from here. Not used by the shipped browser app.
if (typeof module !== "undefined") module.exports = { PrecedenceResolver };
