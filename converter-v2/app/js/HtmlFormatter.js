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
 * ===========================================================================
 */

class HtmlFormatter {

	// elements that never have a closing tag — they must not change depth
	static #VOID = new Set(["img", "br", "meta", "link", "input", "hr",
		"source", "wbr", "area", "base", "col", "embed", "track"]);

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
