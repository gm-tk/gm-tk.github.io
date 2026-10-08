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
	static hoverStitch(text, report = null) {
		// `report` (optional) receives [start, end] — in `text`'s own coordinates — of every marker this pass
		// WEAVES, so InteractiveScanner.#interactiveInTable can tell an inline cell hover from a widget invocation
		// (data hover_definition_inline.table_cell_release; env TABLEHOVER_OFF). Omitted = the output is unchanged.
		const s0 = String(text ?? "");
		if (s0.indexOf("[") < 0) return s0;
		const tpl = DataService.Data.EmitTemplates;
		const cfg = tpl.elements?.hover_definition_inline?.render_stitch;
		if (!cfg || cfg.enabled === false) return s0;
		if (typeof process !== "undefined" && process.env && process.env.INFOSPLIT_OFF) return s0;
		const IT0 = String.fromCharCode(0xE000), IT1 = String.fromCharCode(0xE001);
		// The define_heads data block (the scanner-weave's sibling extension) contributes
		// its stitch_heads ("define") to the render-stitch head vocabulary too, unless
		// toggled off, alongside "definition".
		// Data flag: elements.hover_definition_inline.define_heads   Env toggle: DEFINEHEAD_OFF
		const _dh = tpl.elements?.hover_definition_inline?.define_heads;
		const _dhHeads = (_dh && _dh.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.DEFINEHEAD_OFF))
			? (_dh.stitch_heads ?? []) : [];
		// THE TRIGGER-WORDED HEAD WITH A COLON DEF (`nouns [hovertrigger: Person, place or thing.]`,
		// `intern [hover trigger: An intern is…]`): the paragraph path weaves it in InteractiveScanner (the single-bracket
		// inline trigger), but in a table cell it reaches this pass, where the "trigger" rule below would decline it, so a
		// released layout-table cell would show it as literal text. With the flag ON those heads join the alternation FIRST
		// and a marker whose trigger head is followed straight by a separator is taken for the word. A trigger marker
		// with no separator ("[Info Trigger] on blue", "[hover trigger over image + captions…]") is untouched. Data
		// render_stitch.trigger_heads; env HOVERTRIGSTITCH_OFF (and TABLEHOVER_OFF, with table_cell_release).
		const _th = cfg.trigger_heads;
		const _thOn = _th && _th.enabled !== false && Array.isArray(_th.heads) && _th.heads.length
			&& !(typeof process !== "undefined" && process.env && (process.env[_th.env ?? "HOVERTRIGSTITCH_OFF"] || process.env.TABLEHOVER_OFF));
		// THE BOLD / ITALIC ANCHOR: the last-word fallback below also takes a closing **bold** / *italic* run
		// (`**visual storytelling** [hovertrigger: …]` — inlineMarkup then wraps the whole run, the paragraph path's own form).
		// Data render_stitch.bold_anchor; env HOVERBOLDSTITCH_OFF (and TABLEHOVER_OFF, the master toggle).
		const _ba = cfg.bold_anchor;
		const _baOn = _ba && _ba.enabled !== false
			&& !(typeof process !== "undefined" && process.env && (process.env[_ba.env ?? "HOVERBOLDSTITCH_OFF"] || process.env.TABLEHOVER_OFF));
		const trigHeads = _thOn ? _th.heads.map((w) => String(w).trim().replace(/[-\s]+/g, "[-\\s]?")) : [];
		const heads = trigHeads.concat((cfg.head_words ?? ["hover", "rollover", "mouseover", "definition"])
			.concat(_dhHeads)
			.map((w) => String(w).trim().replace(/[-\s]+/g, "[-\\s]?")));
		const seps = cfg.separators ?? ":=–—";
		const sepEsc = seps.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
		const trigSepRe = _thOn ? new RegExp("^\\[\\s*(?:" + trigHeads.join("|") + ")\\s*[" + sepEsc + "]", "iu") : null;
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
			const decline = (trigRe.test(full) && !(trigSepRe && trigSepRe.test(full))) || !def || !/\p{L}/u.test(def)
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
			// QUOTED NAMED ANCHOR (the ENGJ403 "hover info ‘X’:" idiom in kept
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
				const wm = tb.match(/([\p{L}\p{M}\p{N}][\p{L}\p{M}\p{N}'’\-]*)$/u)
					|| (_baOn ? tb.match(/(\*\*[^*\n]*[\p{L}\p{N}][^*\n]*\*\*|(?<!\*)\*[^*\n]*[\p{L}\p{N}][^*\n]*\*)$/u) : null)
					// …and a word / run closed by 1–2 punctuation marks (`**landmarks**. [hovertrigger: …]`): the sentinel
					// follows the punctuation and inlineMarkup's punctuation-anchor pass wraps the run or word before it
					// (or drops the sentinel under that pass's own guards)
					|| (_baOn ? tb.match(/(?:[\p{L}\p{M}\p{N}]|\*)[.?!,;:)]{1,2}$/u) : null);
				if (wm) { out += tb + sentinel; last = end; woven = true; }
			}
			if (woven && report) report.push([start, end]);
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
		// MEDIA-REFERENCE LINE DROP at the free-body text point. The primary drop
		// lives in MediaBuilder.image (an image's OWN anchor-text reference line), but
		// a reference title can also reach plain black-text rendering when its [image]
		// marker was consumed elsewhere (e.g. an un-built quiz's flushed lead text —
		// SCCH302's "Metal Bucket … Stock Photo – Download Image Now – iStock" lines).
		// The iStock reference form is unmistakable ("… Stock Photo – Download Image
		// Now – iStock") and the gold library never ships such lines as visible text,
		// so a whole LINE matching the data-driven form is dropped here too. Same
		// `stitch` containment as the hover re-stitch: FALSE for cv2 placeholder dumps /
		// built-widget content (the raw hand-off keeps every reference line), so only
		// genuine free-body text is cleaned. Shares the image drop's data flag + env
		// toggle: elements.image_reference_title_drop / IMGREFTITLE_OFF.
		const _refCfg = DataService.Data.EmitTemplates.elements?.image_reference_title_drop;
		if (stitch && _refCfg && _refCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.IMGREFTITLE_OFF)) {
			const lineRe = new RegExp(_refCfg.line_pattern
				?? "download image now|stock (?:photo|illustration|vector)\\b[^\\n]*[\\u2013\\u2014-]\\s*istock\\s*$", "i");
			text = String(text ?? "").split("\n").filter((l) => !(l.trim() && lineRe.test(l.trim()))).join("\n");
		}
		// SENTINEL-PAIR ATOMICITY. A hover/infoTrigger definition woven into the raw text
		// as a U+E000…U+E001 sentinel pair must never be CUT by the per-line split below —
		// a definition whose text spans a soft line break (a real "\n", e.g. MXDI202-09's
		// Vertex/Face/Edge hover block) would otherwise leave an unpaired sentinel
		// character leaking into each half. Any newline INSIDE a pair collapses to a
		// space, so the woven definition stays one atomic span on one line; text outside
		// the pairs keeps its line structure.
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
		let lines = text.split(/\n+/).filter((l) => l.trim());
		// GLYPH-ONLY LINE DROP. A free-body line whose whole content is ONE punctuation
		// glyph (a writer's stray "." / ",", a text-box bracket "[" / "]" left behind after an image,
		// a broken equation's "+" "=" "–", PNR102's "✔" ticks) would ship as <p>.</p>; the gold
		// never keeps one. The line — with its * emphasis
		// markers removed — must be exactly one character that is not a letter, not a digit, not "_"
		// and not a kept glyph ("•" stays for the bullet path's own empty-item rule). Free-body text
		// only (stitch true): the placeholder / built-widget dumps stay a faithful hand-off.
		// Data flag: body_region.drop_glyph_only_lines. Env toggle: GLYPHLINE_OFF.
		const _glyphCfg = tpl.body_region?.drop_glyph_only_lines;
		if (stitch && _glyphCfg && _glyphCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_glyphCfg.env ?? "GLYPHLINE_OFF"])) {
			const keep = new Set((_glyphCfg.keep ?? ["•"]).map(String));
			lines = lines.filter((l) => {
				const g = l.trim(), t = g.replace(/\*/g, "").trim() || g;   // a lone "*" is itself the glyph
				return !([...t].length === 1 && !/[\p{L}\p{N}_]/u.test(t) && !keep.has(t));
			});
		}
		const indentPer = cfg.indent_spaces_per_level ?? 2;
		// Sometimes a writer accidentally types a structural tag (e.g. "[body]") in ordinary
		// BLACK text instead of colouring it red — since only RED text is scanned for [tags],
		// a black one like this is invisible to the tag detector and LEAKS through as literal
		// content (e.g. a line literally starting with the text "[body] A trusted adult…").
		// Strip a leading tag like this before rendering. Data flag:
		// body_region.black_leading_tag_strip. Env toggle: BLACKTAGSTRIP_OFF.
		// body_region.black_leading_tag_strip_more {tags, env BLACKBODYTEXT_OFF}: more tags on their own toggle.
		const _more = tpl.body_region?.black_leading_tag_strip_more;
		const stripTags = cfg && [...(tpl.body_region?.black_leading_tag_strip ?? []),
			...((_more && _more.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[_more.env ?? "BLACKBODYTEXT_OFF"]))
				? (_more.tags ?? []) : [])];
		const blackTagRe = (stripTags && stripTags.length
			&& !(typeof process !== "undefined" && process.env && process.env.BLACKTAGSTRIP_OFF))
			? new RegExp(`^\\[(?:${stripTags.map((t) => String(t).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})\\]\\s*`, "i")
			: null;
		// a writer's TYPED bullet glyph («› text») is a bullet line like «• text» (body_region.typed_bullet_glyphs; env TYPEDBULLET_OFF)
		const _tbg = tpl.body_region?.typed_bullet_glyphs;
		const typedBulletRe = _tbg && _tbg.enabled !== false && (_tbg.glyphs ?? []).length
			&& !(typeof process !== "undefined" && process.env && process.env[_tbg.env ?? "TYPEDBULLET_OFF"])
			? new RegExp(`^[${_tbg.glyphs.map((g) => String(g).replace(/[\]\\^-]/g, "\\$&")).join("")}]\\s+(.*)$`, "u") : null;
		// the writer's typed hyphen bullets («- item» / «– item»), only inside a run of min_run or more such lines (blank lines
		// between allowed), never before a digit (body_region.typed_bullet_glyphs.dash_runs; env DASHBULLET_OFF)
		const _dr = _tbg?.dash_runs;
		const dashRe = _dr && _dr.enabled !== false && (_dr.glyphs ?? []).length
			&& !(typeof process !== "undefined" && process.env && process.env[_dr.env ?? "DASHBULLET_OFF"])
			? new RegExp(`^[${_dr.glyphs.map((g) => String(g).replace(/[\]\\^-]/g, "\\$&")).join("")}]\\s+(?!\\d)(\\S.*)$`, "u") : null;
		const dashRun = new Set();
		if (dashRe) {
			const idx = lines.map((l, k) => (l.trim() ? k : -1)).filter((k) => k >= 0);
			let run0 = [];
			const close = () => { if (run0.length >= (_dr.min_run ?? 2)) for (const k of run0) dashRun.add(k); run0 = []; };
			for (const k of idx) { if (dashRe.test(lines[k].trim())) run0.push(k); else close(); }
			close();
		}
		const nodes = lines.map((raw, li) => {
			const indent = nestOff ? 0 : (raw.match(/^[ \t]+/)?.[0].length ?? 0);
			const level = Math.floor(indent / indentPer);
			let line = raw.trim();
			if (blackTagRe) line = line.replace(blackTagRe, "").trim();
			// MANUAL BULLET. The plain "• text" path is unchanged; when emphBulletOn, ALSO match a
			// bullet after a leading run of *,_ emphasis markers ("*•text*") and, if the glyph sat
			// inside an emphasis WRAPPER, drop the now-dangling closing marker so the content stays
			// clean. A plain "• text" can't match this (it needs a leading *,_), so the non-emphasis
			// path is unaffected — this only ADDS <li> for the emphasis-led form.
			let bullet = null;
			const emphB = emphBulletOn ? line.match(/^([*_]{1,2})[ \t]*•[ \t]*([\s\S]*)$/) : null;
			if (emphB) {
				let c = emphB[2];
				if (c.endsWith(emphB[1])) c = c.slice(0, -emphB[1].length);
				bullet = [line, c.trim()];
			} else {
				bullet = line.match(/^•\s*(.*)$/) ?? (typedBulletRe ? line.match(typedBulletRe) : null)
					?? (dashRun.has(li) ? line.match(dashRe) : null);
			}
			const numbered = line.match(/^(\d+)[.)]\s+(.*)$/);
			if (bullet) return { kind: "ul", level, content: bullet[1] };
			if (numbered) return { kind: "ol", level, content: numbered[2], num: parseInt(numbered[1], 10) };
			return { kind: "p", level: 0, content: line };
		});
		// THE WRITER'S TYPED ASTERISK BULLET. A "* text" line (asterisk + space) is the writer's own manual
		// bullet — the extractor's Word numbering always renders "• ", and the italic marker "*text*" never opens with a
		// space — so it is a list item, never a literal "<p>* …</p>": one level under a directly preceding list item, at
		// the level of a directly preceding "* " line, else a flat top-level item (BLL240's "Decoding … involves:"
		// sub-points; ARFUN02's clap pattern). Data body_region.list_nesting.asterisk_bullet; env STARBULLET_OFF.
		// A LONE "* " line after prose is a FOOTNOTE (HIS1006's "* hori = …", MXEO201's "* squared" — the gold keeps
		// the asterisk paragraph), and a line holding another lone "*" is an italic span ("* NEW * Telling…"): so a
		// line converts only directly after a list item or inside a run of two or more such lines.
		const _star = cfg.asterisk_bullet;
		if (_star && _star.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_star.env ?? "STARBULLET_OFF"])) {
			const starOf = (nd) => {
				if (!nd || nd.kind !== "p") return null;
				const m = /^\*[ \t]+(\S[\s\S]*)$/.exec(nd.content);
				return m && !/(^|[^*])\*([^*]|$)/.test(m[1]) ? m[1] : null;
			};
			const cand = nodes.map(starOf);
			for (let k = 0; k < nodes.length; k++) {
				if (cand[k] == null) continue;
				const prev = k > 0 ? nodes[k - 1] : null;
				const inRun = (k > 0 && cand[k - 1] != null) || (k + 1 < nodes.length && cand[k + 1] != null);
				if (!(prev && prev.kind !== "p") && !prev?._star && !inRun) continue;
				const level = prev?._star ? prev.level : (prev && prev.kind !== "p" ? prev.level + 1 : 0);
				nodes[k] = { kind: "ul", level, content: cand[k], _star: true };
			}
		}
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
				items.push({ content: cur.content, childHtml, num: cur.num });
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
			let open = listKind === "ul" ? L.unordered_open : L.ordered_open;
			const close = listKind === "ul" ? L.unordered_close : L.ordered_close;
			// A CONTINUED NUMBERED LIST KEEPS ITS NUMBERS (KB constraint 42): a numbered run whose first
			// item is N > 1 (Word's own number from the extractor, or the writer's typed digit) opens
			// <ol start="N">, so a list interrupted by a sentence, an image or a note does not restart at 1.
			// Data body_region.list_nesting.ol_start; env OLNUM_OFF.
			const _ols = cfg.ol_start;
			if (listKind === "ol" && nodes[start].kind === "ol" && _ols && _ols.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[_ols.env ?? "OLNUM_OFF"])) {
				const n0 = kept.length ? kept[0].num : null;
				if (Number.isInteger(n0) && n0 > 1) open = open.replace(/^<ol\b/, "<ol" + Utils.FillTemplate(_ols.start_attr, { n: n0 }));
			}
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
	 * convention (the human-built pages use <b>/<i> almost
	 * exclusively), not an oversight here.
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
		// semantic <strong>/<em> (the human-built pages use <b>/<i>
		// almost exclusively). A function replacer avoids $-escaping in content.
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
		// THE HOVER DEFINITION'S OWN TEXT, at emission: every weave path hands its definition
		// over in the sentinel, and some keep the writer's separator (`: the number of seeds that germinate`, `– prayer/chant`)
		// or nothing but the sentence's punctuation (`.`). The gold's `info` is the bare definition (it almost never starts
		// with punctuation). A leading separator run is stripped when a letter or digit remains after it (a definition that is
		// only punctuation keeps its span — the skeleton and the gold both have the span). Data hover_definition_inline.def_clean;
		// env HOVERDEFCLEAN_OFF.
		const _dc = DataService.Data.EmitTemplates.elements?.hover_definition_inline?.def_clean;
		if (_dc && _dc.enabled !== false && s.includes(_it0)
			&& !(typeof process !== "undefined" && process.env && process.env[_dc.env ?? "HOVERDEFCLEAN_OFF"])) {
			const lead = new RegExp("^(?:" + (_dc.lead_pattern ?? "[\\s:;,=\\-–—]+") + ")", "u");
			s = s.replace(new RegExp(`${_it0}([^${_it0}${_it1}]*)${_it1}`, "g"), (m, d) => {
				const c = d.replace(lead, "");
				return _it0 + (/[\p{L}\p{N}]/u.test(c) ? c : d) + _it1;
			});
		}
		const fmtIt = fmt.info_trigger ?? '<span class="infoTrigger" info="{info}">{anchor}</span>';
		// A LONG RUN IS NOT THE ANCHOR: a bold / italic run of more than long_run.max_words words, or one that opens with
		// punctuation («*…across the world. Theories of socialism*», «*, stemming from the teachings of Marxism*»), is the
		// writer's quotation or sentence, not the term — its last word is the anchor, inside the writer's formatting.
		// Data elements.info_trigger_anchor.long_run; env HOVERLONGRUN_OFF.
		const _lr = DataService.Data.EmitTemplates.elements?.info_trigger_anchor?.long_run;
		const _lrOn = !!_lr && _lr.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[_lr.env ?? "HOVERLONGRUN_OFF"]);
		s = s.replace(new RegExp(`<(b|i)>([^<]*)</\\1>${_it0}([^${_it0}${_it1}]*)${_it1}`, "g"),
			(m, tag, inner, def) => {
				if (_lrOn && !(_lr.skip_def_pattern && new RegExp(_lr.skip_def_pattern, "u").test(def))) {
					const n = inner.trim().split(/\s+/).filter((w) => /[\p{L}\p{N}]/u.test(w)).length;
					if (n > (_lr.max_words ?? 12) || (_lr.lead_punct_pattern && new RegExp(_lr.lead_punct_pattern, "u").test(inner))) {
						const mm = inner.match(/^([\s\S]*?)([\p{L}\p{M}\p{N}][\p{L}\p{M}\p{N}'’\-]*)([^\p{L}\p{M}\p{N}]*)$/u);
						if (mm && mm[1].trim()) return `<${tag}>${mm[1]}${fmtIt.replace("{info}", def.trim()).replace("{anchor}", mm[2])}${mm[3]}</${tag}>`;
					}
				}
				return fmtIt.replace("{info}", def.trim()).replace("{anchor}", inner);
			});
		// THE HOVER'S ANCHOR IS THE WRITER'S WHOLE TERM: a te reo term's lead word (reo_lead.words: «hoa ako», «te reo»,
		// «Mātauranga Māori», «tino rangatiratanga», «Ngāti Tūwharetoa» …) binds to the word before the definition.
		// Data elements.info_trigger_anchor.reo_lead; env HOVERREOLEAD_OFF.
		const _ia = DataService.Data.EmitTemplates.elements?.info_trigger_anchor;
		if (_ia && s.includes(_it0)) {
			const W = "[\\p{L}\\p{M}\\p{N}'’\\-]";
			const rl = _ia.reo_lead;
			if (rl && rl.enabled !== false && Array.isArray(rl.words) && rl.words.length
				&& !(typeof process !== "undefined" && process.env && process.env[rl.env ?? "HOVERREOLEAD_OFF"])) {
				s = s.replace(new RegExp(`(^|[^\\p{L}\\p{M}\\p{N}'’\\-])((?:${rl.words.join("|")})\\s+[\\p{L}\\p{M}\\p{N}]${W}*)${_it0}([^${_it0}${_it1}]*)${_it1}`, "giu"),
					(m, pre, term, def) => pre + fmtIt.replace("{info}", def.trim()).replace("{anchor}", term));
			}
		}
		// NON-BOLD anchor: wrap the single WORD immediately before the sentinel. Most of the
		// human's infoTrigger anchors are ONE word ("contempt", "whānau", "kōrero", "onomatopoeia",
		// "stanzas", "decisions"…). A multi-word non-bold anchor gets its LAST word wrapped — the
		// definition stays correct on a partial anchor (still far better than dropping it). Word chars
		// include macrons/diacritics, digits, hyphens and apostrophes; a leading non-letter (e.g. a
		// writer ✅ marker) is left outside the span.
		s = s.replace(new RegExp(`([\\p{L}\\p{M}\\p{N}][\\p{L}\\p{M}\\p{N}'’\\-]*)${_it0}([^${_it0}${_it1}]*)${_it1}`, "gu"),
			(m, word, def) => fmtIt.replace("{info}", def.trim()).replace("{anchor}", word));
		// THE HOVER DEFINITION AFTER THE FULL STOP. A writer who types the marker after the sentence's punctuation
		// (`…the addition of organic matter. [hover definition: material that has come from…]`, AGH1002) leaves no word right
		// before the sentinel, so the definition would be dropped, where the gold builds it.
		// Before the drop: the bold / italic run, the quoted phrase, or (for a definition of min_def_words+) the last word right
		// before 1–2 punctuation marks becomes the anchor; the punctuation stays after the span. A writer NOTE riding the same
		// path (`on ‘Fibre’`, `colour 3`, `over Māori boy`, `production – the process…`, a file name) matches note_pattern
		// and is still dropped. Data elements.info_trigger_punct_anchor; env HOVERPUNCT_OFF.
		const _pa = DataService.Data.EmitTemplates.elements?.info_trigger_punct_anchor;
		if (_pa && _pa.enabled !== false && s.includes(_it0)
			&& !(typeof process !== "undefined" && process.env && process.env[_pa.env ?? "HOVERPUNCT_OFF"])) {
			const noteRe = _pa.note_pattern ? new RegExp(_pa.note_pattern, "iu") : null;
			const P = `(${_pa.punct_class ?? "[.?!,;:)]"}{1,2})\\s*${_it0}([^${_it0}${_it1}]*)${_it1}`;
			const words = (d) => d.replace(/<[^>]+>/g, " ").trim().split(/\s+/).filter(Boolean).length;
			const okDef = (d, min) => words(d) >= min && /\p{L}/u.test(d) && !(noteRe && noteRe.test(d.replace(/<[^>]+>/g, "").trim()));
			const wrap = (anchor, def, p) => fmtIt.replace("{info}", def.trim()).replace("{anchor}", anchor) + p;
			// the line's FIRST SENTENCE is the term (`setting.` as a list item, `Ka rawe tō mahi! You have now completed…` as a
			// paragraph): the gold wraps all of it, punctuation inside — `<span …>setting.</span>` (ARFUN05), `<span …>Ka rawe tō
			// mahi!</span> You have…` (BLL272)
			const wl = _pa.whole_line_max_words ?? 8;
			s = s.replace(new RegExp(`^(\\s*)([^<${_it0}${_it1}]*?\\p{L}[^<${_it0}${_it1}]*?)${P.replace(_pa.punct_class ?? "[.?!,;:)]", _pa.whole_line_punct ?? "[.?!]")}`, "u"),
				(m, lead, term, p, def) => (words(term) <= wl && okDef(def, 1))
					? lead + wrap(term.trim() + p, def, "") : m);
			s = s.replace(new RegExp(`<(b|i)>([^<]*)</\\1>${P}`, "gu"), (m, tag, inner, p, def) => okDef(def, 1) ? wrap(inner, def, p) : m);
			s = s.replace(new RegExp(`(“[^“”<]{1,60}”)${P.replace("{1,2}", "{0,2}")}`, "gu"), (m, q, p, def) => okDef(def, 1) ? wrap(q, def, p) : m);
			// the last-word anchor only for a CAPITALISED definition (last_word_upper): a lower-case one mostly glosses a term
			// named earlier in the sentence (HIS1006 `the belief that…` = stereotype); a capitalised one mostly defines the last word
			const upperOk = (d) => _pa.last_word_upper === false || /^\p{Lu}/u.test(d.replace(/<[^>]+>/g, "").trim());
			s = s.replace(new RegExp(`([\\p{L}\\p{M}\\p{N}][\\p{L}\\p{M}\\p{N}'’\\-]*)${P}`, "gu"),
				(m, word, p, def) => okDef(def, _pa.min_def_words ?? 2) && upperOk(def) ? wrap(word, def, p) : m);
		}
		if (typeof process !== "undefined" && process.env && process.env.TRACE_ITDROP) for (const _m of s.matchAll(new RegExp(`${_it0}([^${_it0}${_it1}]*)${_it1}`, "g"))) process.stderr.write(`ITDROP\t${JSON.stringify(s.slice(Math.max(0, _m.index - 40), _m.index))}\t${JSON.stringify(_m[1].slice(0, 40))}\n`);
		s = s.replace(new RegExp(`${_it0}[^${_it0}${_it1}]*${_it1}`, "g"), "");   // still no clean anchor → drop the sentinel (plain text)
		// THE SPACE BEFORE PUNCTUATION AFTER A HOVER SPAN: the removed marker's padding space
		// would sit between the built span and the sentence's punctuation (`components</span> . We…`,
		// `style</span> , <span…`), which the gold almost never has. Drop it. Data
		// hover_definition_inline.def_clean.tight_after_span; env HOVERTIGHT_OFF.
		if (_dc && _dc.enabled !== false && _dc.tight_after_span !== false && s.includes('class="infoTrigger"')
			&& !(typeof process !== "undefined" && process.env && process.env[_dc.tight_after_span_env ?? "HOVERTIGHT_OFF"])) {
			s = s.replace(/(<span class="infoTrigger"[^>]*>[^<]*<\/span>)[ \t]+(?=[,.;:!?)])/g, "$1");
		}
		// bare URLs become real links (target=_blank, corpus convention); the text is escaped by now, so a query string's
		// ampersand is «&amp;» and stays inside the address (elements.bare_url_link.query_string; env URLQUERY_OFF)
		const _bu = DataService.Data.EmitTemplates.elements?.bare_url_link;
		const _buQuery = !!_bu && _bu.enabled !== false && _bu.query_string !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_bu.env || "URLQUERY_OFF"]);
		const _buRe = _buQuery ? /(https?:\/\/(?:[^\s<>&"]|&amp;)+)/g : /(https?:\/\/[^\s<>&"]+)/g;
		// the address ends where the URL ends: closing sentence punctuation (never an entity's own «;») and a «)» with no
		// «(» to match inside the address go back to the sentence (elements.bare_url_link.trailing_punctuation; env URLTRIM_OFF)
		const _bt = _bu?.trailing_punctuation;
		const _btOn = !!_bt && _bt.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[_bt.env || "URLTRIM_OFF"]);
		if (_btOn) {
			const marks = String(_bt.chars ?? ".,;:!?");
			const count = (u, c) => u.split(c).length - 1;
			// a «]» with no «[» inside the address closes the marker typed round it («[LINK: …]» / «[URL: …]»)
			// (elements.bare_url_link.trailing_punctuation.unmatched_bracket; env URLBRACKET_OFF)
			const _ub = _bt.unmatched_bracket;
			const _ubOn = !!_ub && _ub.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[_ub.env || "URLBRACKET_OFF"]);
			s = s.replace(_buRe, (whole) => {
				let u = whole, tail = "";
				for (;;) {
					const last = u.slice(-1);
					if (last && marks.includes(last) && !(last === ";" && /&(?:[a-z]+|#\d+);$/i.test(u))) { tail = last + tail; u = u.slice(0, -1); continue; }
					if (last === ")" && count(u, ")") > count(u, "(")) { tail = last + tail; u = u.slice(0, -1); continue; }
					if (_ubOn && last === "]" && count(u, "]") > count(u, "[")) { tail = last + tail; u = u.slice(0, -1); continue; }
					break;
				}
				return `<a href="${u}" target="_blank">${u}</a>${tail}`;
			});
		} else s = s.replace(_buRe, '<a href="$1" target="_blank">$1</a>');
		// the writer's typed «[URL: <address>]» marker round a linked address: the link stays, the marker goes
		// (elements.bare_url_link.url_marker; env URLMARKER_OFF)
		const _um = _bu?.url_marker;
		if (_um && _um.enabled !== false && _um.pattern && /url/i.test(s)
			&& !(typeof process !== "undefined" && process.env && process.env[_um.env || "URLMARKER_OFF"])) {
			s = s.replace(new RegExp(_um.pattern, "gi"), "$1");
		}
		// an ORPHAN «]» right after the line's last link closes a red writer instruction whose «[» went to a note
		// («[Developer, please copy … from» + «https://…]»): with no «[» left in the visible text, it goes
		// (elements.bare_url_link.url_marker.orphan_close; env URLMARKER_OFF)
		if (_um && _um.enabled !== false && _um.orphan_close !== false && s.includes("</a>]")
			&& !(typeof process !== "undefined" && process.env && process.env[_um.env || "URLMARKER_OFF"])) {
			const vis = s.replace(/<[^>]+>/g, "");
			if (vis.split("]").length > vis.split("[").length) s = s.replace(/(<\/a>)\](\s*)$/, "$1$2");
		}
		// Weave the Writers Template's own HYPERLINK phrases (block.links {text,target}) onto their
		// DESCRIPTIVE text as <a href=target>phrase</a> — the human convention. Conservative: exact
		// phrase text, FIRST occurrence, skip if the text is itself a URL (bare-URL rule already linked
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
	 * DOMAIN LINK-TEXT DISPLAY (as in the BLL241 supervisor note). For the
	 * domains listed in Emit_Templates.json →
	 * elements.link_text_display.domains, a link whose VISIBLE TEXT is itself a
	 * URL on that domain renders that text as the domain's canonical display
	 * form ("https://speldsa.org.au") while the href keeps the writer's FULL
	 * deep URL — exactly what the human developers ship in the page BODY
	 * (their acknowledgements keep the full URL
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
	 * NO-EMOJI RULE (Change Ledger CL-0051, an exception to CL-0001
	 * permitting deletion of writer characters). Strips emoji from
	 * the rendered page as a FULL-PAGE post-pass (the LinkTextDisplay seam:
	 * after the note tidy, before Indent, caller stops at the acks block) —
	 * post-pass placement means the tag machinery, the ✅-glued title fences,
	 * the tile delimiters and the 🔴 red-run sentinels are untouchable
	 * by construction. Scope = Extended_Pictographic grapheme CLUSTERS minus
	 * the data exempt list (ticks & crosses verbatim + the listed maths
	 * operators); EP arrow emoji map to PLAIN arrows (gold's own TEDC402
	 * treatment); a keycap digit keeps its digit. The ledger's clauses: a run
	 * of 2+ consecutive plain <p> lines PREFIXED by a would-be-deleted
	 * cluster becomes one <ul>/<li>; a lone one stays a <p>; in-prose
	 * removals get spacing normalised; a <p> the strip emptied is dropped.
	 * ONE disclosure note per affected page at the first removal (via the
	 * caller's noteFactory → NotesAndComments.redFlag, so the note scheme +
	 * NOTESCHEME_OFF apply to it like any note); a header/menu first-removal
	 * relocates the note to the body top. VERBATIM zones are
	 * copied through untouched: cv2-interactive subtrees (the developer
	 * hand-off), cv2-note/cv2-comment payloads, <script>/<style>, and every
	 * tag (attributes never touched). Data: Input_Doc_Rules.emoji_strip;
	 * env EMOJISTRIP_OFF turns the whole pass off.
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
		// a header/menu first-removal relocates to the body top
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

	/**
	 * TYPED-NUMBER RUNS → A SEMANTIC <ol> (KB constraint 42, Universal).
	 * A writer who TYPES the step numbers ("1. Pull the plunger…", "2. …") gives the
	 * extractor plain paragraphs, not a Word numbered list, so LISTNEST never sees a
	 * list and the page would ship one <p> per line with the digit inside it — the KB
	 * says numbered steps / sub-questions are <ol><li> (start="N" when the run does
	 * not begin at 1), NEVER manual numbering, and the human developers build the
	 * <ol> (as in BLL212 / SCCH301 / ENGR101).
	 *
	 * A full-page post-pass at the EmojiStrip seam (PageAssembler, body only): a
	 * run of >= min_run CONSECUTIVE bare <p> elements (nothing but whitespace
	 * between one </p> and the next <p>) whose text opens with SEQUENTIAL typed
	 * numbers (n, n+1, …; a restart or a gap ends the group) becomes one <ol> of
	 * <li>s, the lead removed from the paragraph's first text node (a lead inside
	 * a leading <b>/<i> is removed there, the inline tag kept).
	 *
	 * VERBATIM zones are copied through untouched, exactly as EmojiStrip carves
	 * them (cv2-interactive hand-off boxes, cv2-note / cv2-comment, script, style)
	 * PLUS every built-widget subtree whose class opens with one of the data-listed
	 * verbatim_widget_classes: a flipCard face keeps its typed number as the card
	 * title, a dragAndDrop question stays a plain <p>, a carousel caption a <p> —
	 * those widgets own their inner shape. Accordion
	 * panels, activity boxes and free body are LIVE.
	 * The paragraph-content pattern is guarded so it can never cross a </p>.
	 * Data: Emit_Templates body_region.typed_number_list;
	 * env TYPEDOL_OFF.
	 *
	 * @param {string} html - one finished page's HTML (before the acks block)
	 * @returns {string}
	 */
	/**
	 * ORPHAN PUNCTUATION. A block (p / h1–h6 / li, from body_region.orphan_punctuation.elements) whose whole text is
	 * one sentence mark (merge_pattern: a lone . , ; : ! ?) or a mark that carries no wording (drop_pattern: a lone
	 * dash / bullet glyph, a bare `**` run, the cell line-break marker «/» on its own) is what is left when a widget
	 * capture, a fill-in answer span, a URL line or a moved definition took the words around it. A merge-mark joins the
	 * end of the text block that closes right before it (a p / li / heading, through a list close) — the writer's mark is
	 * kept (constraint 1); with no text block right before it, and for a drop-mark, the block is removed, together with
	 * a list it leaves empty. A pre-acks page post-pass; the verbatim zones (hand-off boxes, developer notes and
	 * comments, built widgets on the typed-number list's verbatim list, scripts, styles) are skipped.
	 * Data: Emit_Templates.body_region.orphan_punctuation   Env toggle: ORPHANPUNCT_OFF
	 *
	 * @param {string} html - one page's HTML (before the acks block)
	 * @returns {string} the HTML with orphan punctuation blocks merged / removed
	 */
	static OrphanPunctuation(html) {
		const cfg = DataService.Data.EmitTemplates?.body_region?.orphan_punctuation;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "ORPHANPUNCT_OFF"]) return html;
		const src = String(html);
		const els = (cfg.elements ?? ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li"]).filter((t) => /^[a-z0-9]+$/.test(t));
		if (!els.length) return src;
		// a candidate block holds text only, or text inside one inline wrapper (<p><b>.</b></p>)
		const blockRe = new RegExp("<(" + els.join("|") + ")(?:\\s[^>]*)?>\\s*(?:<(b|strong|i|em)>)?([^<]*)(?:</\\2>)?\\s*</\\1>", "g");
		const mergeRe = new RegExp(cfg.merge_pattern ?? "^[.,;:!?]{1,2}$", "u");
		const dropRe = new RegExp(cfg.drop_pattern ?? "^(?:[•·▪◦\\-–—]|(?:\\*\\*\\s*)+|/(?:\\s*/)*)$", "u");
		const textOf = (s) => String(s).replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();
		// the text block that closes right before a position: </p> / </li> / </hN>, optionally followed by a list close
		const tailRe = /(<\/(?:p|li|h[1-6])>)((?:\s*<\/(?:ul|ol)>)?\s*)$/;
		const endsInText = /(?:[^>\s]|<\/(?:a|b|i|u|em|strong|span|sup|sub)>)\s*$/;
		const fix = (s, dropOnly = false) => {
			let out = "", last = 0, m, hit = false;
			blockRe.lastIndex = 0;
			while ((m = blockRe.exec(s))) {
				const t = textOf(m[3]);
				if (!t) continue;
				const merge = !dropOnly && mergeRe.test(t);
				if (!merge && !dropRe.test(t)) continue;
				hit = true;
				let head = out + s.slice(last, m.index);
				let tail = s.slice(m.index + m[0].length);
				const tm = merge ? head.match(tailRe) : null;
				if (tm && endsInText.test(head.slice(0, head.length - tm[0].length))) {
					const cut = head.length - tm[0].length;
					head = head.slice(0, cut) + t + tm[1] + tm[2];
				} else if (m[1] === "li") {
					// a removed <li> that was its list's only item takes the list with it
					const om = head.match(/<(ul|ol)(?:\s[^>]*)?>\s*$/);
					const cm = tail.match(/^\s*<\/(ul|ol)>/);
					if (om && cm && om[1] === cm[1]) {
						head = head.slice(0, head.length - om[0].length);
						s = s.slice(0, m.index + m[0].length) + tail.slice(cm[0].length);
					}
				}
				out = head.replace(/[ \t]+$/, "");
				last = m.index + m[0].length;
				blockRe.lastIndex = last;
			}
			return hit ? out + s.slice(last) : s;
		};
		// carve the page into LIVE and VERBATIM zones — built widgets are LIVE too when inside_built_widgets is on (a lone
		// mark is never a widget's shape); hand-off boxes, notes, scripts and styles stay verbatim. Data
		// orphan_punctuation.inside_built_widgets; env ORPHANWIDGET_OFF.
		const ibw = cfg.inside_built_widgets;
		const ibwOn = !!ibw && ibw.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[ibw.env ?? "ORPHANWIDGET_OFF"]);
		const tnl = DataService.Data.EmitTemplates?.body_region?.typed_number_list;
		const widgets = (tnl?.verbatim_widget_classes ?? []).map((c) => String(c).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
		const carve = (src, withWidgets) => {
		const openRe = new RegExp("<div class=\"(?:cv2-interactive" + (withWidgets && widgets.length ? "|" + widgets.join("|") : "")
			+ ")|<p class=\"cv2-(?:note|comment)\"|<script\\b|<style\\b", "g");
		const pieces = [];
		let i = 0, om;
		while ((om = openRe.exec(src))) {
			const j = om.index;
			let end;
			if (om[0].startsWith("<div")) {
				const re = /<div\b|<\/div>/g;
				re.lastIndex = j; let depth = 0, mm; end = src.length;
				while ((mm = re.exec(src))) {
					depth += mm[0] === "</div>" ? -1 : 1;
					if (depth === 0) { end = re.lastIndex; break; }
				}
			} else if (om[0].startsWith("<p")) {
				const k = src.indexOf("</p>", j); end = k < 0 ? src.length : k + 4;
			} else {
				const close = om[0].startsWith("<script") ? "</script>" : "</style>";
				const k = src.indexOf(close, j); end = k < 0 ? src.length : k + close.length;
			}
			if (j > i) pieces.push({ live: true, s: src.slice(i, j) });
			// a built widget (not a hand-off box, a note, a script or a style) is its own zone
			pieces.push({ live: false, widget: om[0].startsWith("<div") && !/cv2-interactive/.test(om[0]), s: src.slice(j, end) });
			i = end; openRe.lastIndex = end;
		}
		if (i < src.length) pieces.push({ live: true, s: src.slice(i) });
		return pieces;
		};
		// THE MARK THAT LEADS A BLOCK. A p / li that OPENS with a lone sentence mark — «. These smell when they decompose…»
		// (an accordion head lifted from «**Meat and fat**.»), «<b>: Capturing movement</b>» (a heading lifted from «**Give it a
		// try**:»), «<b>.</b> It can be felt…» (the full stop of the paragraph before, split at a hover tag) — gives the mark
		// to the p / li that closes right before it when that one ends in words without a mark of its own; after a heading,
		// an accordion head, a closed question or nothing, the mark is dropped. The block keeps its words and an inline
		// wrapper that still holds some. Data orphan_punctuation.leading; env ORPHANLEAD_OFF.
		const ld = cfg.leading;
		const ldOn = !!ld && ld.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[ld.env ?? "ORPHANLEAD_OFF"]);
		const lels = (ld?.elements ?? ["p", "li"]).filter((t) => /^[a-z0-9]+$/.test(t));
		const marks = String(ld?.marks ?? ".,;:!?").replace(/[\]\\^-]/g, "\\$&");
		const leadOpenRe = new RegExp("<(" + lels.join("|") + ")(?:\\s[^>]*)?>", "g");
		const leadRe = new RegExp("^(\\s*)(?:<(b|strong|i|em)>)?\\s*([" + marks + "])(\\s*</(?:b|strong|i|em)>)?(\\s+)(?=[^\\s<" + marks + "])", "u");
		const prevTextRe = /(<\/(p|li)>)((?:\s*<\/(?:ul|ol)>)?\s*)$/;
		const markEnd = new RegExp("[" + marks + "]\\s*(?:</(?:a|b|i|u|em|strong|span|sup|sub)>\\s*)*$", "u");
		const leadFix = (s) => {
			if (!ldOn || !lels.length) return s;
			let out = "", last = 0, m;
			leadOpenRe.lastIndex = 0;
			while ((m = leadOpenRe.exec(s))) {
				const at = m.index + m[0].length;
				const mm = s.slice(at, at + 60).match(leadRe);
				if (!mm) continue;
				const wrapOpen = !!mm[2], wrapClosed = !!mm[4];
				// the block without its mark: «<b>:</b> words» loses the emptied wrapper, «<b>: words</b>» keeps it
				const keep = (wrapOpen && !wrapClosed) ? `${mm[1]}<${mm[2]}>` : mm[1];
				let head = out + s.slice(last, at);
				const before = head.slice(0, head.length - m[0].length);
				const pm = before.match(prevTextRe);
				if (pm) {
					const body = before.slice(0, before.length - pm[0].length);
					if (endsInText.test(body) && !markEnd.test(body)) head = body + mm[3] + pm[1] + pm[3] + m[0];
				}
				out = head + keep;
				last = at + mm[0].length;
				leadOpenRe.lastIndex = last;
			}
			return out + s.slice(last);
		};
		// inside a built widget only a DROP mark goes (a lone dash / bullet / slash — no wording): a sentence mark there may
		// be the widget's own content (a flip card's «?» front) and stays; the widget's own hand-off boxes and notes are verbatim
		const inWidget = (w) => carve(w, false).map((p) => (p.live ? leadFix(fix(p.s, true)) : p.s)).join("");
		return carve(src, true).map((p) => (p.live ? leadFix(fix(p.s)) : (p.widget && ibwOn ? inWidget(p.s) : p.s))).join("");
	};

	/**
	 * ADJACENT SIBLING LISTS → ONE LIST. A writer's bullet run split into two
	 * sibling <ul>s by an item that rendered nothing (a bullet's trailing inline [link to X]
	 * marker, a consumed item, an image between bullets) is one list in the gold. A full-page
	 * post-pass at the TypedNumberList seam (body only, the same verbatim zones): a bare
	 * </ul> followed only by whitespace and a bare <ul> joins. Only the data-listed tags
	 * (ul — an <ol> restart is a new numbered list). Data body_region.merge_adjacent_lists;
	 * env ULMERGE_OFF.
	 * @param {string} html - one finished page's HTML (before the acks block)
	 * @returns {string}
	 */
	static MergeAdjacentLists(html) {
		const cfg = DataService.Data.EmitTemplates?.body_region?.merge_adjacent_lists;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "ULMERGE_OFF"]) return html;
		const src = String(html);
		const tags = (cfg.tags ?? ["ul"]).map((t) => String(t).toLowerCase()).filter((t) => /^[a-z]+$/.test(t));
		if (!tags.length) return src;
		const joinRe = new RegExp("</(" + tags.join("|") + ")>(\\s*)<\\1>", "g");
		if (!joinRe.test(src)) return src;
		joinRe.lastIndex = 0;
		const tnl = DataService.Data.EmitTemplates?.body_region?.typed_number_list;
		const widgets = ((cfg.verbatim_widget_classes ?? tnl?.verbatim_widget_classes) ?? []).map((c) => String(c).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
		const openRe = new RegExp("<div class=\"(?:cv2-interactive|" + widgets.join("|")
			+ ")|<p class=\"cv2-(?:note|comment)\"|<script\\b|<style\\b", "g");
		const pieces = [];
		{
			let i = 0, m;
			while ((m = openRe.exec(src))) {
				const j = m.index;
				let end;
				if (m[0].startsWith("<div")) {
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
		return pieces.map((p) => (p.live ? p.s.replace(joinRe, "$2") : p.s)).join("");
	};

	/**
	 * A LIST NUMBER NEVER STANDS ALONE. A bare <p> whose whole text is a list number («1.», «12)» —
	 * optionally inside one bold / italic wrapper) is left behind when a Word-numbered paragraph's
	 * content goes elsewhere: a wholly red item lifted into a Writers Note (an answer key «1. C»,
	 * a developer instruction), or an item whose leading [body] tag opened a block of its own. It
	 * carries nothing for the learner, and the human build never has one, so it leaves the page.
	 * A full-page post-pass at the TypedNumberList seam, after the containers are decided — LIVE
	 * zones only: hand-off boxes, notes and the data-listed built widgets keep their text verbatim.
	 * Data body_region.lone_list_number; env LONENUM_OFF.
	 * @param {string} html - one finished page's HTML (before the acks block)
	 * @returns {string}
	 */
	static LoneListNumbers(html) {
		const cfg = DataService.Data.EmitTemplates?.body_region?.lone_list_number;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "LONENUM_OFF"]) return html;
		const src = String(html);
		const lone = new RegExp(cfg.pattern || "[ \\t]*<p>\\s*(?:<(b|strong|i|em)>)?\\s*\\d{1,2}\\s*[.)]\\s*(?:<\\/\\1>)?\\s*<\\/p>[ \\t]*\\n?", "g");
		if (!lone.test(src)) return src;
		lone.lastIndex = 0;
		const tnl = DataService.Data.EmitTemplates?.body_region?.typed_number_list;
		const widgets = ((cfg.verbatim_widget_classes ?? tnl?.verbatim_widget_classes) ?? []).map((c) => String(c).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
		const openRe = new RegExp("<div class=\"(?:cv2-interactive|" + widgets.join("|")
			+ ")|<p class=\"cv2-(?:note|comment)\"|<script\\b|<style\\b", "g");
		const pieces = [];
		{
			let i = 0, m;
			while ((m = openRe.exec(src))) {
				const j = m.index;
				let end;
				if (m[0].startsWith("<div")) {
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
		return pieces.map((p) => (p.live ? p.s.replace(lone, "") : p.s)).join("");
	};

	/**
	 * A RUN OF TYPED DASH LINES → A SEMANTIC <ul> (the typed-number list's sibling, KB constraint 42's semantic-list principle).
	 * A writer who types «- » at the head of each line gives the extractor plain paragraphs; a run of >= min_run consecutive bare
	 * <p> (nothing but whitespace between one </p> and the next <p>) whose text opens with lead_pattern becomes one <ul> of <li>s,
	 * the dash removed from the paragraph's first text node (a dash bolded on its own goes with its emptied inline tag). The
	 * verbatim zones are the typed-number list's own (hand-off boxes, notes and comments, scripts, styles, the listed built
	 * widgets). Data: Emit_Templates body_region.typed_dash_list; env TYPEDUL_OFF.
	 * The en dash «– » is the same typed bullet, never before a digit (typed_dash_list.en_dash; env TYPEDULENDASH_OFF). A run
	 * whose every gap holds one or more writer notes keeps its paragraphs and loses the typed dash (typed_dash_list.note_gaps;
	 * env TYPEDULNOTEGAP_OFF).
	 *
	 * @param {string} html - one finished page's HTML (before the acks block)
	 * @returns {string}
	 */
	static TypedDashList(html) {
		const cfg = DataService.Data.EmitTemplates?.body_region?.typed_dash_list;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "TYPEDUL_OFF"]) return html;
		const src = String(html);
		const envOff = (c, d) => typeof process !== "undefined" && process.env && process.env[c.env || d];
		const _en = cfg.en_dash;
		const enG = _en && _en.enabled !== false && (_en.glyphs ?? []).length && !envOff(_en, "TYPEDULENDASH_OFF")
			? _en.glyphs.map((g) => String(g).replace(/[\]\\^-]/g, "\\$&")).join("") : "";
		const G = enG ? "[-" + enG + "]" : "-";
		if (!new RegExp("<p>\\s*(?:<[^>]+>\\s*)*" + G, "u").test(src)) return src;   // no candidate at all
		const leadRe = new RegExp(cfg.lead_pattern || "^\\s*-\\s+");
		const enRe = enG ? new RegExp("^\\s*[" + enG + "]\\s+(?!\\d)\\S", "u") : null;
		const _ng = cfg.note_gaps;
		const noteGaps = !!_ng && _ng.enabled !== false && !envOff(_ng, "TYPEDULNOTEGAP_OFF");
		const minRun = Math.max(2, cfg.min_run ?? 2);
		const tnl = DataService.Data.EmitTemplates?.body_region?.typed_number_list;
		const widgets = (tnl?.verbatim_widget_classes ?? []).map((c) => String(c).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
		const openRe = new RegExp("<div class=\"(?:cv2-interactive" + (widgets.length ? "|" + widgets.join("|") : "")
			+ ")|<p class=\"cv2-(?:note|comment)\"|<script\\b|<style\\b", "g");
		const pieces = [];
		{
			let i = 0, m;
			while ((m = openRe.exec(src))) {
				const j = m.index;
				let end;
				if (m[0].startsWith("<div")) {
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
		const P_INNER = "(?:(?!<\\/p>)[^])*";
		const RUN_RE = new RegExp("<p>" + P_INNER + "<\\/p>(?:\\s*<p>" + P_INNER + "<\\/p>)+", "g");
		const ITEM_RE = () => new RegExp("(<p>(" + P_INNER + ")<\\/p>)(\\s*)", "g");
		const LEAD_HTML = enG ? new RegExp("^((?:\\s*<[^>]+>)*)\\s*" + G + "(?:\\s+|(\\s*<\\/(b|i|strong|em|u)>)\\s*)", "u")
			: /^((?:\s*<[^>]+>)*)\s*-(?:\s+|(\s*<\/(b|i|strong|em|u)>)\s*)/;
		const stripLead = (inner) => inner.replace(LEAD_HTML, (all, open, closeTag, closeName) => {
			if (!closeTag) return open;
			const re = new RegExp("(\\s*<" + closeName + "(?:\\s[^>]*)?>)(?![\\s\\S]*<" + closeName + "(?:\\s[^>]*)?>)");
			return open.replace(re, "");
		}).replace(/^[ \t ]+/, "");
		const isDash = (inner) => {
			const t = inner.replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ");
			return (leadRe.test(t) || (!!enRe && enRe.test(t))) && LEAD_HTML.test(inner);
		};
		// A dash run the writer's notes break up: every gap between two dash paragraphs holds one or more notes and nothing
		// else, and no dash paragraph touches the chain from outside — each keeps its <p> and loses the typed dash.
		if (noteGaps) {
			const units = [];
			pieces.forEach((p, k) => {
				if (!p.live) { units.push({ type: p.s.startsWith("<p class=\"cv2-note\"") ? "note" : "other" }); return; }
				const re = /<p>((?:(?!<\/p>)[^])*)<\/p>/g; let last = 0, mm;
				while ((mm = re.exec(p.s))) {
					if (p.s.slice(last, mm.index).trim()) units.push({ type: "other" });
					units.push({ type: isDash(mm[1]) ? "dash" : "p", k, start: mm.index, end: re.lastIndex, inner: mm[1] });
					last = re.lastIndex;
				}
				if (p.s.slice(last).trim()) units.push({ type: "other" });
			});
			const edits = [];
			for (let i = 0; i < units.length; i++) {
				if (units[i].type !== "dash" || (i > 0 && units[i - 1].type === "dash")) continue;
				const chain = [i]; let j = i + 1;
				for (;;) {
					let n = 0;
					while (j < units.length && units[j].type === "note") { n++; j++; }
					if (n && j < units.length && units[j].type === "dash") { chain.push(j); j++; continue; }
					break;
				}
				const lastIx = chain[chain.length - 1];
				if (chain.length >= minRun && !(lastIx + 1 < units.length && units[lastIx + 1].type === "dash")) edits.push(...chain.map((c) => units[c]));
				i = lastIx;
			}
			for (const u of edits.sort((a, b) => b.k - a.k || b.start - a.start)) {
				const s = pieces[u.k].s;
				pieces[u.k].s = s.slice(0, u.start) + "<p>" + stripLead(u.inner) + "</p>" + s.slice(u.end);
			}
		}
		const listify = (chunk) => chunk.replace(RUN_RE, (run) => {
			const items = [];
			const re = ITEM_RE(); let mm;
			while ((mm = re.exec(run))) items.push({ html: mm[1], inner: mm[2], ws: mm[3], dash: isDash(mm[2]) });
			let out = "", group = [];
			const flush = () => {
				if (group.length >= minRun) out += "<ul>\n" + group.map((g) => "<li>" + stripLead(g.inner) + "</li>").join("\n") + "\n</ul>\n";
				else for (const g of group) out += g.html + g.ws;
				group = [];
			};
			for (const it of items) {
				if (it.dash) { group.push(it); continue; }
				flush();
				out += it.html + it.ws;
			}
			flush();
			return out;
		});
		return pieces.map((p) => (p.live ? listify(p.s) : p.s)).join("");
	};

	static TypedNumberList(html) {
		const cfg = DataService.Data.EmitTemplates?.body_region?.typed_number_list;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "TYPEDOL_OFF"]) return html;
		const src = String(html);
		if (!/<p>\s*(?:<[^>]+>\s*)*\d/.test(src)) return src;   // no candidate at all
		const leadRe = new RegExp(cfg.lead_pattern || "^\\s*(\\d{1,2})\\s*[.)]\\s+");
		const minRun = Math.max(2, cfg.min_run ?? 2);
		const widgets = (cfg.verbatim_widget_classes ?? []).map((c) => String(c).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));

		// ---- carve the page into LIVE zones and VERBATIM zones ---------------
		const openRe = new RegExp("<div class=\"(?:cv2-interactive|" + widgets.join("|")
			+ ")|<p class=\"cv2-(?:note|comment)\"|<script\\b|<style\\b", "g");
		const pieces = [];
		{
			let i = 0, m;
			while ((m = openRe.exec(src))) {
				const j = m.index;
				let end;
				if (m[0].startsWith("<div")) {           // subtree by <div> depth
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

		// ---- 2+ consecutive sequentially-numbered plain <p>s → one <ol> --------
		const P_INNER = "(?:(?!<\\/p>)[^])*";
		const RUN_RE = new RegExp("<p>" + P_INNER + "<\\/p>(?:\\s*<p>" + P_INNER + "<\\/p>)+", "g");
		const ITEM_RE = () => new RegExp("(<p>(" + P_INNER + ")<\\/p>)(\\s*)", "g");
		// the lead sits in the FIRST text node: optional leading inline tags, then the number,
		// then EITHER the whitespace before the text OR a closing inline tag when the writer
		// bolded the number on its own ("<b>1.</b> Play …" → "Play …", the emptied <b> dropped)
		const LEAD_HTML = new RegExp("^((?:\\s*<[^>]+>)*)\\s*\\d{1,2}\\s*[.)](?:\\s+|(\\s*<\\/(b|i|strong|em|u)>)\\s*)");
		const stripLead = (inner) => inner.replace(LEAD_HTML, (all, open, closeTag, closeName) => {
			if (!closeTag) return open;
			// drop the LAST opening tag of the same name from the leading tag run (it wrapped only the number)
			const re = new RegExp("(\\s*<" + closeName + "(?:\\s[^>]*)?>)(?![\\s\\S]*<" + closeName + "(?:\\s[^>]*)?>)");
			return open.replace(re, "");
		}).replace(/^[ \t ]+/, "");
		const numberOf = (inner) => {
			const m = inner.replace(/<[^>]+>/g, "").match(leadRe);
			return m ? parseInt(m[1], 10) : null;
		};
		const listify = (chunk) => chunk.replace(RUN_RE, (run) => {
			const items = [];
			const re = ITEM_RE(); let mm;
			while ((mm = re.exec(run))) items.push({ html: mm[1], inner: mm[2], ws: mm[3], n: numberOf(mm[2]) });
			let out = "", group = [];
			const flush = () => {
				if (group.length >= minRun) {
					const lis = group.map((g) => "<li>" + stripLead(g.inner) + "</li>");
					const start = cfg.start_attr !== false && group[0].n !== 1 ? ` start="${group[0].n}"` : "";
					out += "<ol" + start + ">\n" + lis.join("\n") + "\n</ol>\n";
				} else for (const g of group) out += g.html + g.ws;
				group = [];
			};
			for (const it of items) {
				// SEQUENTIAL = the writer's typed count (n, n+1, …) OR the extractor's Word-numbered-list
				// marker, which prefixes EVERY item with "1." (DocxExtractor never counts) — a run whose
				// numbers are all the same is that marker form and is one <ol> too (marker_form_all_equal).
				const last = group.length ? group[group.length - 1].n : null;
				const allEqual = group.length > 0 && group.every((g) => g.n === group[0].n);
				const seq = it.n !== null && (group.length === 0 || cfg.sequential === false
					|| it.n === last + 1
					|| (cfg.marker_form_all_equal !== false && allEqual && it.n === group[0].n));
				if (it.n !== null && seq) group.push(it);
				else if (it.n !== null) { flush(); group.push(it); }   // a restart opens a new group
				else { flush(); out += it.html + it.ws; }
			}
			flush();
			return out;
		});
		return pieces.map((p) => (p.live ? listify(p.s) : p.s)).join("");
	};

	/**
	 * THE LANGUAGE-FONT WRAP (KB constraint 92 / CL-0093: the language-font classes
	 * `jp-text` / `ch-text` / `pinyin` are MANDATORY on
	 * every occurrence, and the conversion applies them — not the designer afterwards).
	 * This is the CJK half: every RUN of Chinese / Japanese text on the page is wrapped
	 * `<span class="ch-text">…</span>` / `<span class="jp-text">…</span>`. A full-page
	 * post-pass at the LinkTextDisplay seam (the caller stops at the acks block — the
	 * gold leaves its acknowledgement credits bare), so every emitter is covered at one
	 * seam: the header <h1> title span (the KB's nested form), the module menu, prose,
	 * lists, table cells, callouts, built widgets and the hand-off boxes alike.
	 *   - a RUN = blocks of CJK characters (Han, kana, CJK punctuation, fullwidth forms)
	 *     joined by internal whitespace and by the ASCII brackets / slashes / stops that
	 *     sit BETWEEN two CJK blocks (the KB's `他(她)是我的(哥哥/弟弟/姐姐/妹妹`),
	 *     starting and ending on a CJK character, and holding at least one Han or kana
	 *     character — a punctuation-only stretch is never a run (the gold's
	 *     spans almost always start and end on a CJK character);
	 *   - the CLASS: a run holding any kana is Japanese regardless of the module; a
	 *     Han-only run takes the MODULE's language (data module_language, longest
	 *     code-prefix match); a Han-only run in a module with no language is left bare
	 *     (the KB says raise a Red Flag rather than guess — that half is not built);
	 *   - VERBATIM: <script> / <style> / <title> and the cv2-note / cv2-comment
	 *     developer quotes (data skip_zones); a text segment already inside an element
	 *     carrying one of the three classes is never re-wrapped (idempotent).
	 * Only the TEXT between tags is ever touched — attributes, tags and entities are
	 * copied through. Data Emit_Templates.body_region.language_fonts; env LANGFONT_OFF.
	 *
	 * @param {string} html - one finished page's HTML (before the acks block)
	 * @param {object} run  - the conversion run (run.moduleCode decides the language)
	 * @returns {string} the HTML with every CJK run wrapped in its language class
	 */
	static LanguageFontWrap(html, run) {
		const cfg = DataService.Data.EmitTemplates?.body_region?.language_fonts;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "LANGFONT_OFF"]) return html;
		const s = String(html ?? "");
		if (!s) return s;
		const classes = cfg.classes ?? { ch: "ch-text", jp: "jp-text", pinyin: "pinyin" };
		const CJK = cfg.cjk_chars ?? "\\u3040-\\u30ff\\u3400-\\u4dbf\\u4e00-\\u9fff\\uf900-\\ufaff\\uff00-\\uffef\\u3000-\\u303f";
		const HAN = cfg.han_chars ?? "\\u3400-\\u4dbf\\u4e00-\\u9fff\\uf900-\\ufaff";
		const KANA = cfg.kana_chars ?? "\\u3040-\\u30ff";
		const JOIN = cfg.internal_joiners ?? "\\s\\u00a0()\\[\\]/.,:;!?…\\-";
		// cheap gate: no Han / kana on the page → nothing to do (the fullwidth / CJK
		// punctuation ranges alone never make a run)
		const anyRe = new RegExp("[" + HAN + KANA + "]", "u");
		if (!anyRe.test(s)) return s;
		// a run: CJK block (joiners CJK block)* — the joiners are consumed only when a
		// CJK block follows, so a run never ends on a space or an ASCII stop
		const runRe = new RegExp("[" + CJK + "]+(?:[" + JOIN + "]+[" + CJK + "]+)*", "gu");
		const hanRe = new RegExp("[" + HAN + "]", "u");
		const kanaRe = new RegExp("[" + KANA + "]", "u");
		// the module's language (longest code-prefix match)
		const code = String(run?.moduleCode ?? "").toUpperCase();
		let modLang = null, best = -1;
		for (const [p, lang] of Object.entries(cfg.module_language ?? {})) {
			const P = String(p).toUpperCase();
			if (code.startsWith(P) && P.length > best) { best = P.length; modLang = lang; }
		}
		const kanaJp = cfg.kana_is_japanese !== false;
		const hanNeedsMod = cfg.han_needs_module_language !== false;
		const wrapper = cfg.wrapper || "span";
		const langOf = (runText) => {
			if (kanaJp && kanaRe.test(runText)) return "jp";
			if (modLang) return modLang;
			return hanNeedsMod ? null : "ch";
		};
		// a run STARTS on a Han / kana character or an opening bracket / quote — a leading
		// CJK colon / comma / stop / tilde belongs to the text before it (the gold's spans
		// start on a character 4,331 : 64; `Sachiko： かず` keeps the colon outside)
		const openers = cfg.lead_open_chars ?? "「『（【〈《〔［｛“‘";
		const headRe = new RegExp("^[^" + HAN + KANA + openers.replace(/[\]\\^-]/g, "\\$&") + "]+", "u");
		const wrapSeg = (seg) => seg.replace(runRe, (m) => {
			if (!hanRe.test(m) && !kanaRe.test(m)) return m;     // punctuation-only stretch
			const lang = langOf(m);
			if (!lang || !classes[lang]) return m;
			const hm = headRe.exec(m);
			const lead = hm ? hm[0] : "", body = hm ? m.slice(hm[0].length) : m;
			if (!body) return m;
			return `${lead}<${wrapper} class="${classes[lang]}">${body}</${wrapper}>`;
		});
		// ---- walk the page: tags copied through, text segments wrapped -------------
		const zones = (cfg.skip_zones ?? []).map(([o, c]) => ({ open: new RegExp(o), close: String(c) }));
		const langCls = new Set(Object.values(classes));
		const tagRe = /<[^>]*>/g;
		let out = "", i = 0, m;
		let inLang = null;            // { tag, depth } while inside an element carrying a language class
		while ((m = tagRe.exec(s))) {
			const j = m.index, tag = m[0];
			if (j > i) out += inLang ? s.slice(i, j) : wrapSeg(s.slice(i, j));
			// a verbatim zone opens here → copy through to its closer
			const z = zones.find((zz) => zz.open.test(tag) && tag.search(zz.open) === 0);
			if (z && !inLang) {
				const k = s.indexOf(z.close, j + tag.length);
				const end = k < 0 ? s.length : k + z.close.length;
				out += s.slice(j, end);
				i = end; tagRe.lastIndex = end;
				continue;
			}
			out += tag;
			i = j + tag.length;
			// track an element that already carries a language class (never re-wrap inside it)
			const tm = /^<(\/?)([a-zA-Z][a-zA-Z0-9-]*)/.exec(tag);
			if (tm) {
				const closing = tm[1] === "/", name = tm[2].toLowerCase();
				const selfClosing = /\/\s*>$/.test(tag) || /^(?:br|img|hr|input|meta|link|source|wbr|area|base|col)$/.test(name);
				if (inLang) {
					if (name === inLang.tag && !selfClosing) {
						inLang.depth += closing ? -1 : 1;
						if (inLang.depth === 0) inLang = null;
					}
				} else if (!closing && !selfClosing) {
					const cm = /\sclass="([^"]*)"/.exec(tag);
					if (cm && cm[1].split(/\s+/).some((c) => langCls.has(c))) inLang = { tag: name, depth: 1 };
				}
			}
		}
		if (i < s.length) out += inLang ? s.slice(i) : wrapSeg(s.slice(i));
		return out;
	};

	/**
	 * THE WRITER'S TYPED FRACTION IN A LEVEL 3–4
	 * MATHS MODULE SHIPS AS MathML. In a module whose run.groupKey is listed in
	 * Input_Doc_Rules.math.typed_fractions.groups, every typed `a/b` (slash_pattern) and every vulgar
	 * fraction (½ ¼ …, `vulgar`) in a TEXT segment becomes a bare-<mn> MathML fraction (KB 05A's form).
	 * Tags are copied through; skip_zones are copied verbatim to their closer; an element carrying a
	 * skip_class_tokens class (the hand-off box) is copied verbatim to its matching close tag. Only the
	 * fraction's typography changes — every other character of the text is kept. Env TYPEDFRAC_OFF.
	 */
	static TypedFractions(html, run) {
		const cfg = DataService.Data.InputDocRules?.math?.typed_fractions;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "TYPEDFRAC_OFF"]) return html;
		const s = String(html ?? "");
		if (!s) return s;
		if (!(cfg.groups ?? []).includes(run?.groupKey)) return s;
		const vulgar = cfg.vulgar ?? {};
		const vKeys = Object.keys(vulgar);
		const esc = (c) => c.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
		const slashSrc = cfg.slash_pattern ?? "(?<![\\d/:.\\w$%-])(\\d{1,4})/(\\d{1,4})(?![\\d/\\w])";
		const fracRe = new RegExp(slashSrc + (vKeys.length ? "|(" + vKeys.map(esc).join("|") + ")" : ""), "gu");
		const NS = "http://www.w3.org/1998/Math/MathML";
		const mfrac = (a, b) => `<math xmlns="${NS}"><mfrac><mn>${a}</mn><mn>${b}</mn></mfrac></math>`;
		// the replacer reads the vulgar group only when the pattern HAS one (an empty `vulgar` map leaves two
		// groups, and the third argument would then be the match offset)
		const conv = (seg) => seg.replace(fracRe, (m, a, b, ...rest) => {
			const v = vKeys.length ? rest[0] : undefined;
			if (typeof v === "string" && v) { const p = vulgar[v]; return Array.isArray(p) && p.length === 2 ? mfrac(p[0], p[1]) : m; }
			return a !== undefined && b !== undefined ? mfrac(a, b) : m;
		});
		const zones = (cfg.skip_zones ?? []).map(([o, c]) => ({ open: new RegExp(o), close: String(c) }));
		const skipCls = new Set(cfg.skip_class_tokens ?? []);
		const tagRe = /<[^>]*>/g;
		let out = "", i = 0, m;
		let inSkip = null;            // { tag, depth } while inside an element carrying a skip class
		while ((m = tagRe.exec(s))) {
			const j = m.index, tag = m[0];
			if (j > i) out += inSkip ? s.slice(i, j) : conv(s.slice(i, j));
			const z = !inSkip && zones.find((zz) => tag.search(zz.open) === 0);
			if (z) {
				const k = s.indexOf(z.close, j + tag.length);
				const end = k < 0 ? s.length : k + z.close.length;
				out += s.slice(j, end);
				i = end; tagRe.lastIndex = end;
				continue;
			}
			out += tag;
			i = j + tag.length;
			const tm = /^<(\/?)([a-zA-Z][a-zA-Z0-9-]*)/.exec(tag);
			if (tm) {
				const closing = tm[1] === "/", name = tm[2].toLowerCase();
				const selfClosing = /\/\s*>$/.test(tag) || /^(?:br|img|hr|input|meta|link|source|wbr|area|base|col)$/.test(name);
				if (inSkip) {
					if (name === inSkip.tag && !selfClosing) {
						inSkip.depth += closing ? -1 : 1;
						if (inSkip.depth === 0) inSkip = null;
					}
				} else if (!closing && !selfClosing) {
					const cm = /\sclass="([^"]*)"/.exec(tag);
					if (cm && cm[1].split(/\s+/).some((c) => skipCls.has(c))) inSkip = { tag: name, depth: 1 };
				}
			}
		}
		if (i < s.length) out += inSkip ? s.slice(i) : conv(s.slice(i));
		return out;
	};
}

// Node module export; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ListsAndRuns };
