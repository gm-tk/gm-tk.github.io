/**
 * ListsAndRuns.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * The black (non-writer-instruction) TEXT RENDERING PRIMITIVES, split out of
 * ContentConverter (the main content-emitting class) into their own file to
 * keep that file's size manageable. "Black text" is ordinary writer prose —
 * as opposed to the RED spans the writer used for [tags] and instructions to
 * the developer. Four statics:
 *
 *   - coalesceBlackRuns(items)           merge consecutive plain black items
 *                                        into one, so a paragraph split across
 *                                        several source blocks renders as one
 *   - hoverStitch(text)                  re-attaches a hover/rollover/definition
 *                                        marker that leaked into the final text
 *                                        as a stray literal, onto its nearest
 *                                        anchor word
 *   - renderBlackText(text, run, links)  black text -> <p> / nested <ul>/<ol>
 *   - inlineMarkup(line, links)          one line -> escaped inline HTML
 *                                        (bold/italic, infoTrigger sentinel,
 *                                        bare-URL links, hyperlink weave)
 *
 * WHY SEPARATE FILE:
 * These methods were natural candidates for their own file because none of
 * them depend on ContentConverter's own internal state (its private instance
 * fields) — they only need DataService.Data (the shared global data store,
 * same as everywhere else in the app). Being self-contained like this means
 * they can live here without any awkward back-references into
 * ContentConverter.
 *
 * WHEN TO WORK HERE:
 * Any change to how plain writer prose (not inside a table or a built
 * interactive widget) becomes paragraphs, nested bullet/numbered lists,
 * bold/italic markup, or inline links. Env toggles LISTNEST_OFF,
 * EMPTYBULLET_OFF, EMPHBULLET_OFF, BLACKTAGSTRIP_OFF, LINKWEAVE_OFF, and
 * INFOSPLIT_OFF (all explained inline below, next to the behaviour they
 * control) let each individual behaviour be reverted for A/B comparison
 * without a code change.
 * ===========================================================================
 */

class ListsAndRuns {

	/**
	 * Merges consecutive black items into one, MUTATING the `items` array in
	 * place (no return value). Only plain black neighbours merge — anything
	 * already owned by an interactive widget (marked consumedBy) or already
	 * gathered by another element (marked _consumed) stays completely
	 * untouched, so this can never accidentally steal content that belongs
	 * to a different element.
	 *
	 * @param {Array<Object>} items - the page's flat list of content items,
	 *        e.g. [ { type: "black", text: "..." }, { type: "tag", ... } ];
	 *        modified in place — adjacent black items are spliced together
	 * @returns {void}
	 */
	static coalesceBlackRuns(items) {
		for (let i = 0; i < items.length - 1; i++) {
			const a = items[i];
			const b = items[i + 1];
			if (a.type === "black" && b.type === "black"
				&& a.consumedBy === undefined && b.consumedBy === undefined) {
				a.text += `\n${b.text}`;
				// Carry the merged-in item's HYPERLINKS onto the surviving block too, so a
				// coalesced run of bullets keeps EVERY line's links — not just the first
				// bullet's. For example, if a 3-bullet list gets merged into one black run,
				// and the 2nd bullet was the one carrying a hyperlink (e.g. "Complete an
				// online contact form"), that link must not be lost just because it wasn't on
				// the first bullet. Shallow-copy the block object so other references to it
				// aren't mutated by surprise; only the links array itself is extended.
				const bLinks = b.block?.links ?? [];
				if (bLinks.length) a.block = { ...(a.block ?? {}), links: [...(a.block?.links ?? []), ...bLinks] };
				items.splice(i + 1, 1);
				i--;   // re-check the same position against the new neighbour
			}
		}
	};

	/**
	 * Finds the index of the LAST whole-word (case-insensitive) occurrence of
	 * `term` inside `hay`, pointing at the START of the term itself (not at
	 * any word-boundary character before it). Returns -1 when `term` doesn't
	 * appear as a whole word anywhere in `hay`. Used by hoverStitch below to
	 * find where an anchor word last occurs in the text seen so far.
	 *
	 * @param {string} hay - the text to search within
	 * @param {string} term - the whole word to search for
	 * @returns {number} the character index of the last match, or -1 when not found
	 */
	static #lastWordIndex(hay, term) {
		const esc = String(term).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
		let re;
		try { re = new RegExp("(?:^|[^\\p{L}\\p{N}])(" + esc + ")(?![\\p{L}\\p{N}])", "giu"); }
		catch { return -1; }
		let m, idx = -1;
		while ((m = re.exec(hay)) !== null) {
			idx = m.index + m[0].length - m[1].length;
			if (re.lastIndex === m.index) re.lastIndex++;
		}
		return idx;
	}

	/**
	 * RE-STITCHES a hover/rollover/definition marker that leaked into the
	 * page as a literal bracketed fragment, weaving it onto its nearby
	 * anchor word instead.
	 *
	 * BACKGROUND: a writer can mark up an inline "hover to see a definition"
	 * interaction directly in their prose, e.g. "word [hover: some
	 * definition]" or "[Rollover definition for TERM: some definition]".
	 * Normally this is caught earlier in the pipeline, while the marker is
	 * still a clean, self-contained red [tag], and woven into a
	 * <span class="infoTrigger"> around the anchor word. But some forms of
	 * this marker only become resolvable AFTER other processing has already
	 * run — for example when the anchor word and the bracketed definition
	 * end up split across two different source items (a black paragraph
	 * mentioning "...for TERM" on one line, with the bracketed definition
	 * itself gathered up separately), or when the marker survives as literal
	 * bracketed text inside a table cell or a tag's own trailing text. Left
	 * alone, those cases show up as ugly literal "[hover: ...]" text on the
	 * finished page. This method is the second-chance pass that catches
	 * them: it scans a whole piece of already-assembled render text for the
	 * marker pattern and, wherever it finds one, weaves the definition onto
	 * the anchor word using the same private-use-character sentinel
	 * (U+E000 ... U+E001) that inlineMarkup (below) already knows how to
	 * turn into an infoTrigger <span>.
	 *
	 * ANCHOR RESOLUTION: prefers an explicit "for TERM" / "on TERM" phrase
	 * written inside the marker itself (matching the LAST occurrence of that
	 * word anywhere earlier in the text); otherwise falls back to the single
	 * word immediately before the marker. When neither produces a safe,
	 * unambiguous anchor, the marker is left completely untouched rather
	 * than risk weaving it onto the wrong word.
	 *
	 * SAFETY: this method must only ever run over FREE-BODY text — content
	 * sitting inside an un-built interactive-widget placeholder has to show
	 * the writer's raw bracketed text unchanged (it's a developer hand-off
	 * reference, not finished page content), so it is the CALLERS of this
	 * method (renderBlackText / inlineMarkup, both below) that are
	 * responsible for skipping the call entirely on placeholder content, via
	 * their own `stitch` parameter.
	 *
	 * @param {string} text - a block of already-assembled render text to scan
	 * @returns {string} the same text with any recognised markers rewoven
	 *          onto their anchor word (any marker with no safe anchor is
	 *          left exactly as it was)
	 * Data flag: elements.hover_definition_inline.render_stitch.
	 * Env toggle: INFOSPLIT_OFF (disables this whole method, so a leaked
	 * marker renders as literal bracketed text instead of being rewoven).
	 * Reuses the same declining rules (instruction/URL definitions,
	 * "trigger" wording) as the earlier interactive-scanner weave, so both
	 * passes make the same call about what's safe to convert.
	 */
	static hoverStitch(text) {
		const s0 = String(text ?? "");
		if (s0.indexOf("[") < 0) return s0;
		const tpl = DataService.Data.EmitTemplates;
		const cfg = tpl.elements?.hover_definition_inline?.render_stitch;
		if (!cfg || cfg.enabled === false) return s0;
		if (typeof process !== "undefined" && process.env && process.env.INFOSPLIT_OFF) return s0;
		const IT0 = String.fromCharCode(0xE000), IT1 = String.fromCharCode(0xE001);
		const heads = (cfg.head_words ?? ["hover", "rollover", "mouseover", "definition"])
			.map((w) => String(w).trim().replace(/[-\s]+/g, "[-\\s]?"));
		const seps = cfg.separators ?? ":=–—";
		const sepEsc = seps.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
		const headAlt = "(?:audio[-\\s]+)?(?:info[-\\s]+)?(?:" + heads.join("|") + ")";
		let re;
		try {
			re = new RegExp("\\[\\s*(" + headAlt + ")\\b([^\\]\\[" + sepEsc + "]*?)\\s*[" + sepEsc + "]\\s*([^\\]\\[]+?)\\s*\\]", "giu");
		} catch { return s0; }
		const hyg = tpl.elements?.hover_weave_hygiene;
		const instrRe = (hyg && hyg.enabled !== false && hyg.instruction_def_guard !== false)
			? new RegExp(hyg.instruction_cue_pattern ?? "\\b(?:please|can you|could you|note to (?:dev|cs)\\b|dev team)\\b", "i") : null;
		const urlRe = (hyg && hyg.enabled !== false && hyg.url_host_skip !== false)
			? new RegExp(hyg.media_tail_pattern ?? "(?:https?:\\/\\/[^\\s<>&\"]+)", "i") : null;
		const trigRe = tpl.elements?.hover_definition_inline?.skip_if_tag_keyword
			? new RegExp(tpl.elements.hover_definition_inline.skip_if_tag_keyword, "i") : /\btrigger\b/i;
		const maxDef = cfg.max_def_len ?? 400;

		let out = "", last = 0, m;
		re.lastIndex = 0;
		while ((m = re.exec(s0)) !== null) {
			const full = m[0], between = m[2] ?? "", def = (m[3] ?? "").trim();
			const start = m.index, end = start + full.length;
			const segBefore = s0.slice(last, start);
			// DECLINE (leave the literal completely untouched) when: the marker uses the word
			// "trigger" (a different, unrelated marker form this method must not touch), the
			// "definition" text actually looks like a developer instruction or contains a URL
			// (not a real definition), or the definition is empty, has no letters at all, or is
			// suspiciously long. The rule is always: never risk a WRONG weave, and never turn a
			// harmless literal into a new kind of leak.
			const decline = trigRe.test(full) || !def || !/\p{L}/u.test(def)
				|| def.length > maxDef || /https?:\/\//i.test(def)   // a def with a URL is a "click this link" instruction, not a definition
				|| (instrRe && instrRe.test(def)) || (urlRe && urlRe.test(def));
			if (decline) { out += segBefore + full; last = end; continue; }
			const sentinel = IT0 + def + IT1;
			const nm = between.match(/\b(?:for|on)\s+([^\]]+?)\s*$/i);
			let woven = false;
			if (nm) {
				const term = nm[1].trim().replace(/[.,;:]+$/, "");
				const hay = out + segBefore;
				const idx = term && /\p{L}/u.test(term) ? ListsAndRuns.#lastWordIndex(hay, term) : -1;
				if (idx >= 0) {
					const ae = idx + term.length;
					out = hay.slice(0, ae) + sentinel + hay.slice(ae);
					last = end; woven = true;
				}
			}
			// QUOTED NAMED ANCHOR (ROUND 222c — the ENGJ403 "hover info ‘X’:" idiom in kept
			// TABLE cells, e.g. "**First Act – exposition** [hover info ‘exposition’: **Setting
			// up the story.** ]"). The writer names the hovered word in quotes between the head
			// and the separator; weave the sentinel onto that word's LAST occurrence in the
			// preceding prose. This also rescues the cells the last-word fallback below cannot
			// anchor (their prose ends in "**" bold markers, not a word character). For a
			// multi-word quoted anchor ("inciting incident") the sentinel lands after the
			// phrase and #inlineMarkup wraps its final word — exactly the human's
			// `inciting <span class="infoTrigger">incident</span>` form (gold ENGJ403 4.0).
			if (!woven) {
				const qm2 = between.match(/['‘"]([^'’"‘]+)['’"]/);
				const qterm = qm2 ? qm2[1].trim().replace(/[.,;:]+$/, "") : "";
				if (qterm && /\p{L}/u.test(qterm)) {
					const hay = out + segBefore;
					const idx = ListsAndRuns.#lastWordIndex(hay, qterm);
					if (idx >= 0) {
						const ae = idx + qterm.length;
						out = hay.slice(0, ae) + sentinel + hay.slice(ae);
						last = end; woven = true;
					}
				}
			}
			if (!woven && !nm) {
				const tb = segBefore.replace(/\s+$/, "");
				const wm = tb.match(/([\p{L}\p{M}\p{N}][\p{L}\p{M}\p{N}'’\-]*)$/u);
				if (wm) { out += tb + sentinel; last = end; woven = true; }
			}
			if (!woven) { out += segBefore + full; last = end; }   // no clean anchor → keep the literal
		}
		out += s0.slice(last);
		return out;
	}

	/**
	 * Renders a run of black (plain writer prose) text into HTML paragraphs
	 * and nested bullet/numbered lists.
	 *
	 * HANDLES: splitting on blank lines into separate <p> paragraphs, "• "
	 * lines becoming a nested <ul> (the indentation level comes from how many
	 * times the source paragraph was indented in the original Word document
	 * — see DocxExtractor for how that indent gets encoded), "1." / "2."
	 * runs becoming a nested <ol>, the **bold** / *italic* markdown-style
	 * markers, and bare URLs turning into real links.
	 *
	 * @param {string} text - the raw black text, one source line per "\n"
	 * @param {ConversionRun} run - the current conversion run
	 * @param {Array<Object>} [links] - hyperlink targets captured from the
	 *        source document, e.g. [ { text: "here", target: "https://..." } ] —
	 *        used to weave a matching phrase into a real <a> link
	 * @param {boolean} [stitch] - when true (the default), also runs
	 *        hoverStitch over this text first; pass false for content
	 *        inside an un-built widget placeholder (see hoverStitch above)
	 * @returns {string[]} the rendered HTML for each paragraph/list found
	 */
	static renderBlackText(text, run, links = [], stitch = true) {
		// Re-stitch a cross-LINE "for TERM" hover marker on the FULL text BEFORE splitting it
		// into individual lines below — this way the anchor term (which might be on one line)
		// and its marker (which might be on a different line) are still in the same string when
		// hoverStitch goes looking for them. `stitch` is FALSE for un-built-widget-placeholder /
		// built-widget content (that dump must stay a faithful, untouched raw hand-off) — only
		// genuine FREE-BODY text ever gets woven. The INFOSPLIT_OFF env toggle also disables it
		// globally (see hoverStitch above).
		if (stitch) text = this.hoverStitch(String(text ?? ""));
		// SENTINEL-PAIR ATOMICITY (ROUND 227, part of the w:br→\n fix). A hover/infoTrigger
		// definition woven into the raw text as a U+E000…U+E001 sentinel pair must never be
		// CUT by the per-line split below — a definition whose text spans a soft line break
		// (now a real "\n", e.g. MXDI202-09's Vertex/Face/Edge hover block) would otherwise
		// leave an unpaired sentinel character leaking into each half (defect class E). Any
		// newline INSIDE a pair collapses to a space, so the woven definition stays one
		// atomic span on one line; text outside the pairs keeps its line structure.
		text = String(text ?? "").replace(/[^]*/g, (m) => m.replace(/\n+/g, " "));
		const tpl = DataService.Data.EmitTemplates;
		const L = tpl.elements.list;
		const cfg = tpl.body_region?.list_nesting ?? {};
		const nestOff = typeof process !== "undefined" && process.env && process.env.LISTNEST_OFF;
		// EMPTY-ITEM artifact drop. A writer bullet whose ONLY content was a red developer
		// instruction (which gets lifted out separately into its own note) leaves an empty
		// black "• " bullet behind — this would otherwise render as an empty <li> mixed in among
		// otherwise-populated list items, which the reference site never actually ships. So: drop
		// those stray empty items — but KEEP a list that is ENTIRELY empty (a deliberate
		// blank-worksheet scaffold for the learner to fill in, which the reference site DOES
		// ship as-is). Data flag: drop_empty_items. Env toggle: EMPTYBULLET_OFF.
		const dropEmpty = (cfg.drop_empty_items ?? true)
			&& !(typeof process !== "undefined" && process.env && process.env.EMPTYBULLET_OFF);
		// EMPHASIS-LED MANUAL BULLET: a writer sometimes typed the bullet glyph "•" as their own
		// list marker but then wrapped the whole line in emphasis markup ("*•text*"), or left a
		// stray emphasis marker in front of it (" *•make…"), or separated the glyph from the text
		// with a tab instead of a space ("•\ttext"). The plain "starts with •" test just below
		// misses all of these variants, so without this extra check they would leak through as a
		// plain <p> instead of becoming a real list item. Data flag:
		// body_region.list_nesting.emphasis_led_bullet. Env toggle: EMPHBULLET_OFF.
		const emphBulletOn = (cfg.emphasis_led_bullet ?? true)
			&& !(typeof process !== "undefined" && process.env && process.env.EMPHBULLET_OFF);
		const out = [];
		// KEEP leading indentation — it encodes the Word list NESTING level (2 spaces per
		// w:ilvl, added by DocxExtractor). The extractor emits one block per paragraph,
		// joined by "\n"; bullets arrive as consecutive lines and group into nested lists.
		const lines = text.split(/\n+/).filter((l) => l.trim());
		const indentPer = cfg.indent_spaces_per_level ?? 2;
		// Sometimes a writer accidentally types a structural tag (e.g. "[body]") in ordinary
		// BLACK text instead of colouring it red — since only RED text is scanned for [tags],
		// a black one like this is invisible to the tag detector and LEAKS through as literal
		// content (e.g. a line literally starting with the text "[body] A trusted adult…").
		// Strip a leading tag like this before rendering. Data flag:
		// body_region.black_leading_tag_strip. Env toggle: BLACKTAGSTRIP_OFF.
		const stripTags = cfg && (tpl.body_region?.black_leading_tag_strip ?? []);
		const blackTagRe = (stripTags && stripTags.length
			&& !(typeof process !== "undefined" && process.env && process.env.BLACKTAGSTRIP_OFF))
			? new RegExp(`^\\[(?:${stripTags.map((t) => String(t).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})\\]\\s*`, "i")
			: null;
		const nodes = lines.map((raw) => {
			const indent = nestOff ? 0 : (raw.match(/^[ \t]+/)?.[0].length ?? 0);
			const level = Math.floor(indent / indentPer);
			let line = raw.trim();
			if (blackTagRe) line = line.replace(blackTagRe, "").trim();
			// MANUAL BULLET. The plain "• text" path is unchanged; when emphBulletOn, ALSO match a
			// bullet after a leading run of *,_ emphasis markers ("*•text*") and, if the glyph sat
			// inside an emphasis WRAPPER, drop the now-dangling closing marker so the content stays
			// clean. A plain "• text" can't match this (it needs a leading *,_), so toggle-OFF and the
			// non-emphasis path are byte-identical — the change only ADDS <li> for the emphasis-led form.
			let bullet = null;
			const emphB = emphBulletOn ? line.match(/^([*_]{1,2})[ \t]*•[ \t]*([\s\S]*)$/) : null;
			if (emphB) {
				let c = emphB[2];
				if (c.endsWith(emphB[1])) c = c.slice(0, -emphB[1].length);
				bullet = [line, c.trim()];
			} else {
				bullet = line.match(/^•\s*(.*)$/);
			}
			const numbered = line.match(/^(\d+)[.)]\s+(.*)$/);
			if (bullet) return { kind: "ul", level, content: bullet[1] };
			if (numbered) return { kind: "ol", level, content: numbered[2] };
			return { kind: "p", level: 0, content: line };
		});
		const fullyBold = (s) => /^\*\*[\s\S]+\*\*$/.test(s.trim());

		// render a contiguous run of list items at `baseLevel` into one <ul>/<ol>; deeper
		// items nest into the preceding <li>. Returns [html, nextIndex].
		const renderList = (start, baseLevel) => {
			let listKind = nodes[start].kind;
			const items = [];
			let allBold = true, allHaveChildren = true;
			let i = start;
			while (i < nodes.length && nodes[i].kind !== "p" && nodes[i].level >= baseLevel) {
				if (nodes[i].level > baseLevel) { i++; continue; }     // safety (deeper consumed below)
				if (nodes[i].kind !== listKind) break;                 // same-level kind change → new list
				const cur = nodes[i];
				i++;
				let childHtml = "";
				if (i < nodes.length && nodes[i].kind !== "p" && nodes[i].level > baseLevel) {
					const [ch, ni] = renderList(i, baseLevel + 1);
					childHtml = ch; i = ni;
				} else {
					allHaveChildren = false;
				}
				if (!fullyBold(cur.content)) allBold = false;
				items.push({ content: cur.content, childHtml });
			}
			// EMPTY-ITEM drop: a stray empty <li> inside a POPULATED list is the "• "-only
			// artifact (a writer bullet whose red instruction was lifted to a note). An ALL-empty
			// list is left intact (the deliberate blank-worksheet scaffold). The ol-override is
			// recomputed on the kept set so a dropped empty can't change it; when nothing is
			// dropped (kept === items) the kept-set values reproduce the originals exactly.
			let kept = items;
			if (dropEmpty && items.some((x) => x.content.trim() !== "")) {
				kept = items.filter((x) => x.content.trim() !== "" || x.childHtml);
			}
			// OL-OVERRIDE (human convention, OSAI201-02 "What did we learn?"): a TOP-level
			// bullet list whose every item is BOLD and carries nested sub-points renders as
			// a NUMBERED <ol> (the writer's docx bullets are an under-specification the human
			// numbers). Conservative: top level only, every item bold + parented, ≥2 items.
			const allBoldK = kept.length >= 2 && kept.every((x) => fullyBold(x.content));
			const allChildK = kept.length >= 1 && kept.every((x) => x.childHtml);
			if ((cfg.ol_bold_parents ?? true) && baseLevel === 0 && listKind === "ul"
				&& allBoldK && allChildK && kept.length >= 2) listKind = "ol";
			const open = listKind === "ul" ? L.unordered_open : L.ordered_open;
			const close = listKind === "ul" ? L.unordered_close : L.ordered_close;
			const lis = kept.map(({ content, childHtml }) =>
				Utils.FillTemplate(L.item, { content: this.inlineMarkup(content, links, stitch) + (childHtml ? `\n${childHtml}` : "") }));
			return [[open, ...lis, close].join("\n"), i];
		};

		let i = 0;
		while (i < nodes.length) {
			if (nodes[i].kind === "p") {
				out.push(Utils.FillTemplate(tpl.elements.paragraph.form, { content: this.inlineMarkup(nodes[i].content, links, stitch) }));
				i++;
			} else {
				const [html, ni] = renderList(i, nodes[i].level);
				out.push(html); i = ni;
			}
		}
		return out;
	};

	/**
	 * Converts the writer's markdown-style inline markup inside ONE line of
	 * text into safe, escaped HTML. Escapes HTML special characters FIRST,
	 * then converts the corpus's own markers (**bold**, *italic*), and
	 * finally links any bare URLs. Order matters here: escaping AFTER
	 * converting the markers would mangle the freshly-inserted HTML tags
	 * right back into visible, escaped text.
	 *
	 * NOTE ON TAGS USED: bold/italic render as plain <b>/<i>, not the more
	 * "semantic" <strong>/<em> — that is the reference site's own house
	 * convention (see the inline comment further down for the measured
	 * evidence), not an oversight here.
	 *
	 * @param {string} line - one line of already-assembled writer text
	 * @param {Array<Object>} [links] - hyperlink targets captured from the
	 *        source document, e.g. [ { text: "here", target: "https://..." } ]
	 * @param {boolean} [stitch] - when true (the default), also runs
	 *        hoverStitch over this line first; pass false for content
	 *        inside an un-built widget placeholder (see hoverStitch above)
	 * @returns {string} the escaped, markup-converted HTML for this line
	 */
	static inlineMarkup(line, links = [], stitch = true) {
		const fmt = DataService.Data.EmitTemplates.elements.inline_format;
		// Re-stitch any hover/rollover/definition marker that reached this single line as a
		// FREE-BODY literal (table cells and headings call inlineMarkup directly, without going
		// through renderBlackText above, so they need their own hoverStitch pass here too).
		// `stitch` is FALSE for un-built-widget-placeholder / built-widget content, so that raw
		// hand-off content stays untouched. This runs BEFORE EscapeHtml below, so the sentinel's
		// inserted definition text gets HTML-escaped along with everything else, exactly like the
		// self-closed marker form handled elsewhere in the pipeline.
		if (stitch) line = this.hoverStitch(String(line ?? ""));
		let s = Utils.EscapeHtml(line);
		// **bold** / *italic* use the HOUSE convention from data — <b>/<i>, not
		// semantic <strong>/<em> (measured: human <b> 11259 vs <strong> 277,
		// <i> 4822 vs <em> 144). A function replacer avoids $-escaping in content.
		s = s.replace(/\*\*([^*]+)\*\*/g, (m, g) => Utils.FillTemplate(fmt.bold, { content: g }));
		s = s.replace(/\*([^*]+)\*/g, (m, g) => Utils.FillTemplate(fmt.italic, { content: g }));
		// INFO-TRIGGER inline annotation. The scanner re-stitched a "term [hovertrigger: DEF]" marker
		// onto the line, encoding the hover DEFINITION in a private-use sentinel (U+E000 DEF U+E001)
		// RIGHT AFTER the anchor term. Wrap the immediately-preceding BOLD/ITALIC run (the anchor) in
		// <span class="infoTrigger" info="DEF"> — the human's inline definition span (ENGC201). The DEF
		// is already HTML-escaped (EscapeHtml ran first), so it is attribute-safe. When the preceding
		// token is NOT a clear bold/italic anchor, the anchor span is non-derivable, so the sentinel is
		// dropped → plain text (the hover deferred). The sentinel never occurs in ordinary text, so
		// non-infoTrigger lines are untouched.
		const _it0 = String.fromCharCode(0xE000), _it1 = String.fromCharCode(0xE001);
		const fmtIt = fmt.info_trigger ?? '<span class="infoTrigger" info="{info}">{anchor}</span>';
		s = s.replace(new RegExp(`<(b|i)>([^<]*)</\\1>${_it0}([^${_it0}${_it1}]*)${_it1}`, "g"),
			(m, tag, inner, def) => fmtIt.replace("{info}", def.trim()).replace("{anchor}", inner));
		// NON-BOLD anchor: wrap the single WORD immediately before the sentinel. Measured: 81% of the
		// human's 1,603 infoTrigger anchors are ONE word ("contempt", "whānau", "kōrero", "onomatopoeia",
		// "stanzas", "decisions"…). A multi-word non-bold anchor gets its LAST word wrapped — the
		// definition stays correct on a partial anchor (still far better than dropping it). Word chars
		// include macrons/diacritics, digits, hyphens and apostrophes; a leading non-letter (e.g. a
		// writer ✅ marker) is left outside the span.
		s = s.replace(new RegExp(`([\\p{L}\\p{M}\\p{N}][\\p{L}\\p{M}\\p{N}'’\\-]*)${_it0}([^${_it0}${_it1}]*)${_it1}`, "gu"),
			(m, word, def) => fmtIt.replace("{info}", def.trim()).replace("{anchor}", word));
		s = s.replace(new RegExp(`${_it0}[^${_it0}${_it1}]*${_it1}`, "g"), "");   // still no clean anchor → drop the sentinel (plain text)
		// bare URLs become real links (target=_blank, corpus convention)
		s = s.replace(/(https?:\/\/[^\s<>&"]+)/g, '<a href="$1" target="_blank">$1</a>');
		// Weave the Writers Template's own HYPERLINK phrases (block.links {text,target}) onto their
		// DESCRIPTIVE text as <a href=target>phrase</a> — the human convention (1011 vs
		// Claude's 131 phrase-links; an 880-link gap). Conservative: exact phrase text,
		// FIRST occurrence, skip if the text is itself a URL (bare-URL rule already linked
		// it) or already sits inside an <a>. Data: elements.hyperlink_weave; env LINKWEAVE_OFF.
		const hw = DataService.Data.EmitTemplates.elements.hyperlink_weave;
		const weaveOn = hw && hw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.LINKWEAVE_OFF);
		if (weaveOn && Array.isArray(links) && links.length) {
			for (const lk of links) {
				const t = String(lk?.text ?? "").trim();
				const href = String(lk?.target ?? "").trim();
				if (!t || !href || /^https?:\/\//i.test(t)) continue;
				const esc = Utils.EscapeHtml(t);
				const idx = s.indexOf(esc);
				if (idx < 0) continue;
				const before = s.slice(0, idx);
				if (before.lastIndexOf("<a ") > before.lastIndexOf("</a>")) continue;  // already inside a link
				s = before
					+ Utils.FillTemplate(hw.form, { url: Utils.EscapeHtml(href), text: esc })
					+ s.slice(idx + esc.length);
			}
		}
		return s;
	};

	/**
	 * DOMAIN LINK-TEXT DISPLAY (ROUND 213 — Chris, the BLL241 supervisor-note
	 * screenshot). For the domains listed in Emit_Templates.json →
	 * elements.link_text_display.domains, a link whose VISIBLE TEXT is itself a
	 * URL on that domain renders that text as the domain's canonical display
	 * form ("https://speldsa.org.au") while the href keeps the writer's FULL
	 * deep URL — exactly what the human developers ship in the page BODY
	 * (measured 67/68 body sites; their acknowledgements keep the full URL
	 * text, so the caller runs this on the pre-acknowledgements part of the
	 * page only). An anchor whose text is a descriptive PHRASE ("SPELD SA
	 * website") is never touched — only URL-shaped text is rewritten, so no
	 * meaningful wording can ever be lost. Runs as a FULL-PAGE post-pass (the
	 * OmitPlaceholderResidue / TidyDeveloperNotes pattern) so every emitter —
	 * body prose, supervisor panels, callouts, notes, future widgets — is
	 * covered uniformly, in every module.
	 * Env toggle: LINKTEXT_OFF (reverts to the raw full-URL link text).
	 *
	 * @param {string} html - one finished page's HTML (before the acks block)
	 * @returns {string} the HTML with domain link texts canonicalised
	 */
	static LinkTextDisplay(html) {
		const cfg = DataService.Data.EmitTemplates?.elements?.link_text_display;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.LINKTEXT_OFF) return html;
		const domains = Object.entries(cfg.domains ?? {});
		if (!domains.length) return html;
		const rewrite = (seg) => seg.replace(
			/<a\b([^>]*?)href="([^"]+)"([^>]*)>([^<]*)<\/a>/gi,
			(whole, pre, href, post, text) => {
				for (const [domain, display] of domains) {
					const d = domain.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
					// the href must be ON this domain (scheme + optional www., then
					// the domain as the whole host)
					if (!new RegExp(`^https?://(?:www\\.)?${d}(?:[/?#]|$)`, "i").test(href.trim())) continue;
					// the visible text must ITSELF be a URL on the same domain
					// (optionally scheme-less / www.-prefixed, any path, an optional
					// stray trailing "." the writer glued on) — a descriptive
					// phrase never matches, so it is never rewritten
					if (!new RegExp(`^(?:https?://)?(?:www\\.)?${d}(?:[/?#]\\S*)?\\.?$`, "i").test(text.trim())) continue;
					if (text.trim() === display) return whole;   // already canonical
					return `<a${pre}href="${href}"${post}>${display}</a>`;
				}
				return whole;
			});
		// An UN-BUILT widget's dashed placeholder box (class cv2-interactive) is the
		// developer's raw hand-off material — its content is preserved verbatim by
		// long-standing rule (the same containment the hover re-stitch and note
		// machinery follow), so anchors inside those boxes are NOT rewritten. Walk
		// the page, copying each cv2-interactive subtree through untouched (matching
		// close found by <div> depth counting) and rewriting only the rest.
		const s = String(html);
		let out = "", i = 0;
		for (;;) {
			const j = s.indexOf("<div class=\"cv2-interactive", i);
			if (j < 0) { out += rewrite(s.slice(i)); break; }
			out += rewrite(s.slice(i, j));
			const re = /<div\b|<\/div>/g;
			re.lastIndex = j;
			let depth = 0, end = s.length, m;
			while ((m = re.exec(s))) {
				depth += m[0] === "</div>" ? -1 : 1;
				if (depth === 0) { end = re.lastIndex; break; }
			}
			out += s.slice(j, end);
			i = end;
		}
		return out;
	};

	/**
	 * NO-EMOJI RULE (ROUND 234 — Change Ledger CL-0051, the first CL-0001
	 * exception permitting deletion of writer characters). Strips emoji from
	 * the rendered page as a FULL-PAGE post-pass (the LinkTextDisplay seam:
	 * after the note tidy, before Indent, caller stops at the acks block) —
	 * post-pass placement means the tag machinery, the ✅-glued title fences,
	 * the r192 tile delimiters and the 🔴 red-run sentinels are untouchable
	 * by construction. Scope = Extended_Pictographic grapheme CLUSTERS minus
	 * the data exempt list (ticks & crosses verbatim + the measured maths
	 * operators); EP arrow emoji map to PLAIN arrows (gold's own TEDC402
	 * treatment); a keycap digit keeps its digit. The ledger's clauses: a run
	 * of 2+ consecutive plain <p> lines PREFIXED by a would-be-deleted
	 * cluster becomes one <ul>/<li>; a lone one stays a <p>; in-prose
	 * removals get spacing normalised; a <p> the strip emptied is dropped.
	 * ONE disclosure note per affected page at the first removal (via the
	 * caller's noteFactory → NotesAndComments.redFlag, so the r219 scheme +
	 * NOTESCHEME_OFF apply to it like any note); a header/menu first-removal
	 * relocates the note to the body top (the r203 rule). VERBATIM zones are
	 * copied through untouched: cv2-interactive subtrees (the developer
	 * hand-off), cv2-note/cv2-comment payloads, <script>/<style>, and every
	 * tag (attributes never touched). Data: Input_Doc_Rules.emoji_strip;
	 * env EMOJISTRIP_OFF reverts the whole pass byte-for-byte.
	 *
	 * @param {string} html - one finished page's HTML (before the acks block)
	 * @param {function(): (string|null)} noteFactory - builds the disclosure
	 *        note html; called AT MOST ONCE, and only if something was removed
	 * @returns {string} the HTML with emoji stripped per the rule
	 */
	static EmojiStrip(html, noteFactory) {
		const cfg = DataService.Data.InputDocRules?.emoji_strip;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.EMOJISTRIP_OFF) return html;

		const exempt = new Set(
			[...(cfg.exempt ?? []), ...Object.values(cfg.exempt_extensions ?? {}).flat()]
				.map((c) => String(c).codePointAt(0)));
		const arrows = {};
		for (const [k, v] of Object.entries(cfg.arrow_map ?? {})) arrows[k.codePointAt(0)] = v;
		// one emoji grapheme cluster: an Extended_Pictographic base plus its
		// riders (VS15/16, skin tones, ZWJ-joined follow-ons, a keycap mark),
		// OR a keycap digit sequence, OR a regional-indicator flag pair. A
		// cluster is handled WHOLE, so a VS16 is never orphan-stripped off a
		// kept tick (✅️ survives intact; a stripped base takes its riders).
		const CL = "(?:\\p{Extended_Pictographic}(?:[\\u{FE0E}\\u{FE0F}\\u{1F3FB}-\\u{1F3FF}]|\\u{200D}\\p{Extended_Pictographic}[\\u{FE0E}\\u{FE0F}\\u{1F3FB}-\\u{1F3FF}]*)*\\u{20E3}?|[0-9#*]\\u{FE0F}\\u{20E3}|[\\u{1F1E6}-\\u{1F1FF}]{2})";
		const clusterRe = () => new RegExp(CL, "gu");
		const leadRe = new RegExp("^" + CL, "u");
		const SENT = "\uE0EE";                       // one-shot anchor mark (PUA)

		let removed = false;
		const stripSeg = (seg) => {                  // one inter-tag text segment
			let hit = false;
			let s = seg.replace(clusterRe(), (cl) => {
				const base = cl.codePointAt(0);
				if (exempt.has(base)) return cl;         // ticks & crosses kept whole
				hit = true;
				if (/^[0-9#*]/.test(cl)) return cl[0];   // keycap: the digit survives
				return arrows[base] ?? "";               // arrow → plain form; else gone
			});
			if (hit) {
				removed = true;
				s = s.replace(/[ \t]{2,}/g, " ").replace(/[ \t]+([.,;:!?)\]])/g, "$1");
				// a DELETED lead cluster must not leave its trailing space behind
				// as a new leading space ("⚖️ <b>Low…" → "<b>Low…", not " <b>Low…")
				if (deletedLead(seg)) s = s.replace(/^[ \t ]+/, "");
			}
			return s;
		};
		// a line lead that the strip would DELETE (exempt/arrow leads keep a
		// visible mark, so those lines are NOT checklist candidates)
		const deletedLead = (text) => {
			const m = String(text).replace(/^[\s\u00A0]+/, "").match(leadRe);
			if (!m) return null;
			const base = m[0].codePointAt(0);
			if (exempt.has(base) || arrows[base] !== undefined || /^[0-9#*]/.test(m[0])) return null;
			return m[0];
		};

		// ---- carve the page into LIVE zones and VERBATIM zones ---------------
		const src = String(html);
		const pieces = [];
		{
			const openRe = /<div class="cv2-interactive|<p class="cv2-(?:note|comment)"|<script\b|<style\b/g;
			let i = 0, m;
			while ((m = openRe.exec(src))) {
				const j = m.index;
				let end;
				if (m[0].startsWith("<div")) {           // cv2 subtree by <div> depth
					const re = /<div\b|<\/div>/g;
					re.lastIndex = j; let depth = 0, mm; end = src.length;
					while ((mm = re.exec(src))) {
						depth += mm[0] === "</div>" ? -1 : 1;
						if (depth === 0) { end = re.lastIndex; break; }
					}
				} else if (m[0].startsWith("<p")) {
					const k = src.indexOf("</p>", j); end = k < 0 ? src.length : k + 4;
				} else {
					const close = m[0].startsWith("<script") ? "</script>" : "</style>";
					const k = src.indexOf(close, j); end = k < 0 ? src.length : k + close.length;
				}
				if (j > i) pieces.push({ live: true, s: src.slice(i, j) });
				pieces.push({ live: false, s: src.slice(j, end) });
				i = end; openRe.lastIndex = end;
			}
			if (i < src.length) pieces.push({ live: true, s: src.slice(i) });
		}

		// ---- clause 1: 2+ consecutive deleted-lead plain <p>s → one <ul> -----
		// The paragraph-content pattern is GUARDED so it can never cross a
		// </p> boundary — a lazy [^]*? here would backtrack-extend across
		// paragraphs under match pressure and swallow the structure between
		// them (caught live on SCFUN01's phases nav). "Consecutive" is strict:
		// nothing but whitespace between one </p> and the next <p>.
		const P_INNER = "(?:(?!<\\/p>)[^])*";
		const RUN_RE = new RegExp("<p>" + P_INNER + "<\\/p>(?:\\s*<p>" + P_INNER + "<\\/p>)+", "g");
		const ITEM_RE = () => new RegExp("(<p>(" + P_INNER + ")<\\/p>)(\\s*)", "g");
		let marked = false;
		const listify = (chunk) => {
			if (cfg.list_runs === false) return chunk;
			return chunk.replace(RUN_RE, (run) => {
				const items = [];
				const re = ITEM_RE(); let mm;
				while ((mm = re.exec(run))) items.push({ html: mm[1], inner: mm[2], ws: mm[3] });
				let out = "", group = [];
				const flush = () => {
					if (group.length >= 2) {
						removed = true;
						const lis = group.map((g) => "<li>"
							+ g.inner.replace(g.lead, "").replace(/^[ \t\u00A0]+/, "")
							+ "</li>");
						out += (marked ? "" : SENT) + "<ul>\n" + lis.join("\n") + "\n</ul>\n";
						marked = true;
					} else if (group.length) out += group[0].html + group[0].ws;
					group = [];
				};
				for (const it of items) {
					const lead = deletedLead(it.inner.replace(/<[^>]+>/g, ""));
					if (lead) group.push({ ...it, lead });
					else { flush(); out += it.html + it.ws; }
				}
				flush();
				return out;
			});
		};

		// ---- clause 2: char strip + emptied-<p> drop + first-removal anchor --
		let out = "", anchor = -1;
		const stack = [];                            // open p/h/ul/ol/table starts
		const flow = /^<(p|h[1-6]|ul|ol|table)[\s>]/i;
		const closeOf = /^<\/(p|h[1-6]|ul|ol|table)>/i;
		for (const piece of pieces) {
			if (!piece.live) { out += piece.s; continue; }
			const chunk = listify(piece.s);
			let buf = null;                          // the open plain-or-attributed <p>
			for (const tok of chunk.split(/(<[^>]*>)/)) {
				if (!tok) continue;
				const isTag = tok[0] === "<" && tok[tok.length - 1] === ">";
				const pos = () => (buf ? buf.start : out.length);
				if (isTag) {
					if (flow.test(tok)) stack.push({ tag: tok.match(flow)[1].toLowerCase(), start: pos() });
					else if (closeOf.test(tok)) {
						const t = tok.match(closeOf)[1].toLowerCase();
						for (let k = stack.length - 1; k >= 0; k--) if (stack[k].tag === t) { stack.splice(k); break; }
					}
					if (/^<p[\s>]/i.test(tok) && !buf && cfg.drop_emptied !== false) {
						buf = { start: out.length, s: tok, changed: false }; continue;
					}
					if (buf) {
						buf.s += tok;
						if (/^<\/p>/i.test(tok)) {       // close the buffered paragraph
							const text = buf.s.replace(/<[^>]+>/g, "");
							if (buf.changed && !/\S/.test(text)) { /* emptied → dropped */ }
							else out += buf.s;
							buf = null;
						}
						continue;
					}
					out += tok; continue;
				}
				// text segment
				let seg = tok, localChange = false;
				if (seg.includes(SENT)) {                // clause-1 anchor mark
					seg = seg.split(SENT).join("");
					localChange = true;
				}
				const before = seg;
				seg = stripSeg(seg);
				if (seg !== before) localChange = true;
				if (localChange && anchor < 0) anchor = stack.length ? stack[0].start : pos();
				if (buf) { buf.s += seg; if (seg !== before) buf.changed = true; }
				else out += seg;
			}
			if (buf) out += buf.s;                   // unterminated <p> — emit as-is
		}
		if (!removed) return out;

		// ---- the disclosure note: ONE per affected page, at the first removal;
		// a header/menu first-removal relocates to the body top (the r203 rule)
		const note = typeof noteFactory === "function" ? noteFactory() : null;
		if (note) {
			const bodyAt = out.indexOf("<div id=\"body\"");
			const bodyIn = bodyAt < 0 ? 0 : out.indexOf(">", bodyAt) + 1;
			let at = anchor >= 0 ? anchor : bodyIn;
			if (bodyAt >= 0 && at <= bodyAt) at = bodyIn;
			out = out.slice(0, at) + "\n" + note + "\n" + out.slice(at);
		}
		return out;
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ListsAndRuns };
