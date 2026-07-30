/**
 * HtmlFormatter.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Indents a finished HTML page with tabs so the output is debuggable by eye
 * — matching how the human-developed modules are formatted, and plain good
 * practice for files developers will hand-edit.
 *
 * HOW IT WORKS:
 * The emitters produce one tag (or one text-bearing element) per line, so
 * indentation is a line-level walk: a line that CLOSES a block steps the
 * depth out before printing; a line that OPENS one steps it in after.
 * Self-contained lines (<p>text</p>), void elements (<img>, <meta>, …),
 * comments, and the doctype never change depth.
 *
 * WHY A SEPARATE FILE:
 * Pure presentation polish, one concern: string in → string out. It never
 * parses meaning and never reorders content — a malformed balance simply
 * clamps at depth 0 rather than throwing mid-conversion.
 *
 * ROUND 243 (Dev-Feedback R6, E4) — BLOCK-LEVEL LINE BREAKING:
 * The emitters glue structural runs onto one line (an activity open is
 * `<div class="activity"…><div class="row"><div class="col-12">`; a table row
 * is `<tr><td>…</td><td>…</td></tr>`). The human gold breaks every MIXED
 * div/table-structural glued boundary onto its own line (measured broken-share
 * 0.88–1.00 across the gold library) and keeps ONLY the empty-element
 * one-liners glued (`<div></div>` 0.018 broken, `<td></td>` 0.010,
 * `<th></th>` 0.000). #breakBlocks therefore splits a ZERO-WHITESPACE `><`
 * boundary when BOTH tags are in the data list, EXCEPT an open tag immediately
 * followed by its own close. The inserted character is a newline BETWEEN tags
 * — never inside a text node — so the change is semantically byte-inert
 * (normalising `>\s*<` to `><` reproduces the un-split page exactly).
 * Data: Emit_Templates.formatter.block_line_breaks · env LINEBREAK_OFF.
 * ===========================================================================
 */

class HtmlFormatter {

	// elements that never have a closing tag — they must not change depth
	static #VOID = new Set(["img", "br", "meta", "link", "input", "hr",
		"source", "wbr", "area", "base", "col", "embed", "track"]);

	// one full tag (open or close, quoted attrs skipped) that is IMMEDIATELY
	// followed by another tag — the glued `><` boundary #breakBlocks splits
	static #GLUED = /(<(\/?)([a-zA-Z][\w-]*)(?:"[^"]*"|'[^']*'|[^>"'])*>)(?=<(\/?)([a-zA-Z][\w-]*))/g;

	/**
	 * Round 243 (E4): the block-tag set to break between, or null when the
	 * feature is off (data flag disabled, env LINEBREAK_OFF, or no data).
	 */
	static #breakSet() {
		if (typeof process !== "undefined" && process.env && process.env.LINEBREAK_OFF) return null;
		try {
			const cfg = DataService.Data.EmitTemplates.formatter?.block_line_breaks;
			if (!cfg || !cfg.enabled || !Array.isArray(cfg.tags)) return null;
			return new Set(cfg.tags);
		} catch (e) { return null; }
	};

	/**
	 * Round 243 (E4): splits glued block-tag boundaries in one emitter line.
	 * A boundary qualifies when BOTH tags are in `set`; an OPEN tag glued to
	 * its OWN close (`<div></div>`, `<td></td>`) stays a one-liner — the
	 * measured gold empty-element convention.
	 */
	static #breakBlocks(line, set) {
		return line.replace(HtmlFormatter.#GLUED, (whole, tag, lClose, lName, rClose, rName) => {
			const l = lName.toLowerCase(), r = rName.toLowerCase();
			if (!set.has(l) || !set.has(r)) return whole;          // outside the block set
			if (lClose === "" && rClose === "/" && l === r) return whole; // empty element
			return tag + "\n";
		});
	};

	/**
	 * Re-indents an HTML document with tabs.
	 *
	 * USAGE: HtmlFormatter.Indent(html) → indented html
	 *
	 * @param {string} html - emitter output (one element per line)
	 * @returns {string} tab-indented document
	 */
	static Indent(html) {
		const out = [];
		let depth = 0;

		// round 243 (E4): break glued block-tag runs onto their own lines
		// BEFORE the depth walk, so each new line indents like gold's.
		const breakSet = HtmlFormatter.#breakSet();
		if (breakSet) {
			html = html.split("\n")
				.map((l) => HtmlFormatter.#breakBlocks(l, breakSet))
				.join("\n");
		}

		for (const raw of html.split("\n")) {
			const line = raw.trim();
			if (!line) continue;   // emitter blank lines carry no meaning

			const opens = [...line.matchAll(/<([a-zA-Z][\w-]*)(?=[\s>])/g)]
				.map((m) => m[1].toLowerCase())
				.filter((t) => !HtmlFormatter.#VOID.has(t));
			const closes = [...line.matchAll(/<\/([a-zA-Z][\w-]*)>/g)].length;

			// net depth change AFTER this line; a pure-closing line outdents
			// BEFORE printing so the close aligns with its opener
			const net = opens.length - closes;
			if (net < 0) depth = Math.max(0, depth + net);

			out.push("\t".repeat(depth) + line);

			if (net > 0) depth += net;
		}
		return out.join("\n");
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { HtmlFormatter };
