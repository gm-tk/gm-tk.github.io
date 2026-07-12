/**
 * Utils.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Pure, reusable utility functions shared across the converter: text folding,
 * escaping, date stamping, template filling, and small string helpers.
 *
 * WHY SEPARATE FILE:
 * Per the coding standards, pure helpers live apart from DOM/fetch/business
 * logic so they can be reasoned about (and tested) in isolation.
 *
 * RULES:
 * - All functions here are PURE (same input = same output)
 * - No DOM manipulation here
 * - No data fetching, no globals
 * ===========================================================================
 */

class Utils {

	// =======================================================================
	// TEXT FOLDING (matching the reference normaliser's fold() exactly)
	// =======================================================================

	/**
	 * Folds a string for case/diacritic/whitespace-insensitive MATCHING.
	 *
	 * WHAT IT DOES:
	 * Strips diacritics (whakataukī → whakatauki), straightens curly quotes,
	 * turns en/em dashes into "-", collapses whitespace runs to single
	 * spaces, trims, lowercases.
	 *
	 * WHY IT MATTERS:
	 * This is THE comparability step from Tag_Normalisation_Spec.md Step 1.
	 * Every alias match, cue match, and heading lookup folds first, so a
	 * variation that differs only by case/spacing/diacritics never needs a
	 * rule of its own. It mirrors reference/tests/normaliser.py fold()
	 * exactly — parity with the Python harness depends on it.
	 *
	 * NOTE: NEVER fold render content — folding is for matching only.
	 *
	 * @param {string} s - raw text
	 * @returns {string} folded text
	 */
	static Fold(s) {
		// normalize("NFKD") splits letters from their accent marks,
		// then \p{M} (Unicode "Mark") removes the accents
		let out = s.normalize("NFKD").replace(/\p{M}/gu, "");
		// curly quotes → straight; non-breaking space → space
		out = out.replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/ /g, " ");
		// en dash / em dash → hyphen (instruction cues rely on this)
		out = out.replace(/[–—]/g, "-");
		// collapse all whitespace runs to single spaces, trim, lowercase
		return out.replace(/\s+/g, " ").trim().toLowerCase();
	};

	/**
	 * Strips a set of characters from both ends of a string.
	 * (JS has no direct equivalent of Python's str.strip("chars") — the
	 * normaliser port needs one for fragment tidying like ' .;,|-'.)
	 *
	 * @param {string} s - input
	 * @param {string} chars - the characters to remove from the ends
	 * @returns {string}
	 */
	static StripChars(s, chars) {
		let start = 0;
		let end = s.length;
		while (start < end && chars.includes(s[start])) start++;
		while (end > start && chars.includes(s[end - 1])) end--;
		return s.slice(start, end);
	};

	// =======================================================================
	// HTML HELPERS
	// =======================================================================

	/**
	 * Escapes the five HTML-special characters so writer text renders as
	 * text, never as markup.
	 *
	 * USAGE: Utils.EscapeHtml('AT&T <ltd>') → 'AT&amp;T &lt;ltd&gt;'
	 *
	 * @param {string} s
	 * @returns {string}
	 */
	static EscapeHtml(s) {
		return String(s)
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/"/g, "&quot;")
			.replace(/'/g, "&#39;");
	};

	/**
	 * Fills {placeholder} tokens in a template string from a values object.
	 *
	 * WHAT IT DOES:
	 * "Hello {name}" + {name: "Chris"} → "Hello Chris". Unknown tokens are
	 * left in place (visible), because silently emitting an empty string
	 * would hide a template/data mismatch — surfacing beats absorbing.
	 *
	 * USAGE:
	 * Utils.FillTemplate(tpl.red_flag.form, { text: "CS — fix me" })
	 *
	 * @param {string} template - text containing {tokens}
	 * @param {Object} values - token → replacement
	 * @returns {string}
	 */
	static FillTemplate(template, values) {
		return template.replace(/\{(\w+)\}/g, (whole, key) =>
			// ?? keeps the literal token when no value was supplied —
			// a visible signal that something didn't line up
			values[key] ?? whole
		);
	};

	// =======================================================================
	// TEXT FORMATTING
	// =======================================================================

	/**
	 * Title Cases a list of words with the acks slug rules applied:
	 * special tokens get their official casing (3d → 3D), small words stay
	 * lowercase unless first.
	 *
	 * WHY IT EXISTS:
	 * The iStock slug → official title derivation (Acks_Formats.json
	 * istock_slug_title, 98% verified) needs consistent casing.
	 *
	 * @param {string[]} words - lowercased slug words
	 * @param {Object} specialTokens - folded token → official casing
	 * @param {string[]} smallWords - words kept lowercase mid-title
	 * @returns {string}
	 */
	static TitleCaseWords(words, specialTokens = {}, smallWords = []) {
		return words.map((w, i) => {
			if (specialTokens[w]) return specialTokens[w];
			if (i > 0 && smallWords.includes(w)) return w;
			return w.charAt(0).toUpperCase() + w.slice(1);
		}).join(" ");
	};

	/**
	 * Today's date as dd/mm/yy — the acks "retrieved" stamp format
	 * (Acks_Formats.json oembed.retrieved_date_format).
	 *
	 * @returns {string} e.g. "12/06/26"
	 */
	static TodayStamp() {
		const now = new Date();
		// ternary-free zero pad: "0" + n, keep last two chars
		const pad = (n) => String(n).padStart(2, "0");
		return `${pad(now.getDate())}/${pad(now.getMonth() + 1)}/${String(now.getFullYear()).slice(-2)}`;
	};

	/**
	 * Zero-pads a lesson/page number to two digits ("1" → "01").
	 * Used by output filenames ({code}-01.html) and padded module codes.
	 *
	 * @param {number|string} n
	 * @returns {string}
	 */
	static Pad2(n) {
		return String(n).padStart(2, "0");
	};

	/**
	 * Makes a short URL-safe slug from free text (for Mode-P placeholder
	 * labels and fallback image filenames).
	 *
	 * USAGE: Utils.Slugify("Fun bulldog!") → "fun-bulldog"
	 *
	 * @param {string} s
	 * @param {number} maxLen - cap the slug length (default 40)
	 * @returns {string}
	 */
	static Slugify(s, maxLen = 40) {
		return Utils.Fold(s)
			.replace(/[^a-z0-9]+/g, "-")   // anything non-alphanumeric → dash
			.replace(/^-+|-+$/g, "")        // no leading/trailing dashes
			.slice(0, maxLen)
			.replace(/-+$/g, "");           // re-trim if the cut landed on a dash
	};

	/**
	 * Escapes a string for safe use inside a RegExp.
	 * (Same job as Python's re.escape — the normaliser port builds alias
	 * regexes from data, so every alias must be escaped first.)
	 *
	 * @param {string} s
	 * @returns {string}
	 */
	static RegexEscape(s) {
		return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
	};

	/**
	 * Sequential async mapping — the team's standard mapSeries (standards
	 * §7c). Used for rate-limit-friendly work like oEmbed fetches.
	 *
	 * @param {Array} iterable
	 * @param {Function} action - async (item, index, total) => result
	 * @returns {Promise<Array>} results in order
	 */
	static async MapSeries(iterable, action) {
		const results = [];
		for (const [index, item] of iterable.entries()) {
			results.push(await action(item, index, iterable.length));
		}
		return results;
	};
}

// Node test-harness hook: the browser ignores this (module is undefined);
// the sandbox parity tests require() these classes. Not used by the app.
if (typeof module !== "undefined") module.exports = { Utils };
