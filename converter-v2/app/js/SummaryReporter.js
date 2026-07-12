/**
 * SummaryReporter.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Renders the conversion summary panel — the surfacing contract's last
 * mile. Everything the pipeline tallied or noted (files produced, red-flag
 * count, ACK-TODO count, interactives captured, every surfaced decision)
 * is shown HERE, in the UI, where a developer cannot miss it.
 *
 * WHY SEPARATE FILE:
 * Pure presentation (standards table: renderers never fetch, never decide).
 * It reads ConversionRun.Summary() and writes DOM — nothing else.
 * ===========================================================================
 */

class SummaryReporter {

	/**
	 * Renders the summary into the panel element.
	 *
	 * WHAT IT DOES:
	 * Reads everything the run tallied via run.Summary() (plus
	 * run.resolutionPath directly) and writes it straight into the summary
	 * panel's innerHTML: headline count cards, an identity line (module
	 * code / image mode / media list found / which rules resolved it), then
	 * every surfaced note, worst level first.
	 *
	 * DATA SHAPE CONSUMED — run.Summary(), the shape this method reads
	 * (see ConversionRun for how it's built):
	 * {
	 *   pageCount, interactiveCount, redFlagCount, ackTodoCount,   // headline numbers
	 *   moduleCode, codeSource, imageMode, mediaListFound,         // identity line
	 *   notes: [ { level: "error"|"warn"|"info", stage, text } ]   // surfaced decisions
	 * }
	 *
	 * @param {ConversionRun} run - the completed run
	 */
	static Render(run) {
		const panel = document.getElementById(Config.Selectors.SummaryPanel);
		if (!panel) return;
		const s = run.Summary();

		// COLLAPSIBLE (round 205). The whole summary is a native <details>,
		// COLLAPSED by default after a conversion. The always-visible <summary>
		// header carries a MINIFIED stat bar — the same four headline figures,
		// each still labelled, in a compact one-line form. Expanding reveals the
		// full detail body (the large stat cards + identity line + surfaced
		// decisions) exactly as before. Native <details> gives keyboard focus +
		// toggle for free; no JS state to track.

		// minified stat bar — the four headline figures, compact but labelled,
		// shown on the collapsed header. Numbers needing action carry the
		// attention class so they still stand out when collapsed.
		const miniBar = `
			<span class="summary-mini">
				<span class="summary-mini-stat">${s.pageCount} pages</span>
				<span class="summary-mini-stat">${s.interactiveCount} interactives</span>
				<span class="summary-mini-stat ${s.redFlagCount ? "count-attention" : ""}">${s.redFlagCount} red flags</span>
				<span class="summary-mini-stat ${s.ackTodoCount ? "count-attention" : ""}">${s.ackTodoCount} ack-todos</span>
			</span>`;

		// headline counts — the numbers the build gate cares about
		const counts = `
			<div class="summary-counts">
				<div class="count-card"><span class="count-number">${s.pageCount}</span><span class="count-label">HTML pages</span></div>
				<div class="count-card"><span class="count-number">${s.interactiveCount}</span><span class="count-label">interactives captured (un-built)</span></div>
				<div class="count-card ${s.redFlagCount ? "count-attention" : ""}"><span class="count-number">${s.redFlagCount}</span><span class="count-label">RED FLAG notes to action</span></div>
				<div class="count-card ${s.ackTodoCount ? "count-attention" : ""}"><span class="count-number">${s.ackTodoCount}</span><span class="count-label">ACK-TODO items to resolve</span></div>
			</div>`;

		// identity line — how the module was recognised and resolved
		const identity = `
			<p class="summary-identity">
				<strong>${s.moduleCode ?? "UNKNOWN MODULE"}</strong>
				— code from ${s.codeSource ?? "n/a"} · image mode ${s.imageMode}
				· media list ${s.mediaListFound ? "found" : "<strong>NOT FOUND</strong>"}
				· rules: ${run.resolutionPath ?? "defaults"}
			</p>`;

		// every surfaced decision, worst first — nothing is hidden
		const order = { error: 0, warn: 1, info: 2 };
		const notes = [...s.notes].sort((a, b) => order[a.level] - order[b.level]);
		const noteHtml = notes.length
			? `<ul class="summary-notes">${notes.map((n) =>
				`<li class="note-${n.level}"><span class="note-stage">[${n.stage}]</span> ${this.#escape(n.text)}</li>`).join("")}</ul>`
			: `<p class="summary-clean">No discrepancies surfaced — review the red-flag/ACK-TODO counts above before sign-off.</p>`;

		panel.innerHTML = `
			<details class="summary-details">
				<summary class="summary-summary">
					<span class="summary-title">Conversion summary</span>
					${miniBar}
				</summary>
				<div class="summary-body">
					${identity}
					${counts}
					<h3>Surfaced decisions (${notes.length})</h3>
					${noteHtml}
				</div>
			</details>`;
		panel.hidden = false;
	};

	/** Local escape (Utils.EscapeHtml exists, but renderers stay standalone-readable). */
	static #escape(s) {
		return Utils.EscapeHtml(s);
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { SummaryReporter };
