/**
 * PageAssembler.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * This is pipeline stage [8], the LAST stage of converting a single module —
 * the orchestrator that calls every earlier pipeline stage in the right order
 * and glues their results together into the finished output files. One
 * module (the lesson sequence built from one Writers Template .docx — the
 * source document where writers wrap content in [bracketed tags] like [H2] or
 * [Activity] — plus its companion Media List .docx) becomes one or more HTML
 * "pages" (a page is one HTML output file, either a single lesson or the
 * module overview, named {CODE}-00.html, {CODE}-01.html, … in document
 * order) plus one interactives hand-off text file. The pipeline this file
 * drives:
 *   item stream → pages → interactive bundles → converted content
 *   → acknowledgements → skeleton-wrapped HTML pages → manifest.
 * See AssembleModule's own doc comment below for the numbered, stage-by-stage
 * breakdown.
 *
 * THE KEY IDEA:
 * Everything in this file reads from, and writes onto, ONE shared object: the
 * ConversionRun (parameter name `run` throughout the codebase) — a single
 * mutable scratchpad object created fresh for each conversion job that data
 * accumulates onto as the pipeline runs (the module code, the extracted
 * pages, interactive widgets, output files, and human-readable diagnostic
 * notes added via run.AddNote so nothing is silently guessed or dropped). By
 * the time AssembleModule returns, run.pages, run.interactives, and
 * run.outputs together hold the complete result of converting this module.
 *
 * OUTPUT NAMING:
 * {code}_{lesson}_{part}.html from each page's lesson label, or the dash
 * form {CODE}-00.html, -01.html, … in document order (legacy_page_file;
 * see PageFileNames; data: Emit_Templates.output_naming). The interactives
 * manifest is {CODE}_interactives.txt.
 *
 * ACKS PLACEMENT (policy, locked):
 * The acknowledgements block goes on the FIRST page only, after #footer.
 * ===========================================================================
 */

class PageAssembler {

	/**
	 * THE ONE SOURCE OF TRUTH for page output filenames, shared by the emit loop
	 * below AND the choice-page tile hrefs (ContentConverter.#choicePageTiles). The
	 * library convention the developer imports against is `{code}_{lesson}_{part}.html`
	 * (SCCH302_0_0.html); every page already carries exactly that number as its
	 * lessonLabel ("0.0" overview, "N.0" lesson, "N.M" sub-page, dotted writer
	 * lessons verbatim), so the filename is the label with "." → "_". The alternative
	 * dash form `{code}-{NN}.html` is kept as legacy_page_file; env PAGENAME_OFF
	 * (or a page_file template without {page}) selects it. A label collision (two
	 * pages resolving the same name — rare, since the splitter derives distinct
	 * labels) is disambiguated deterministically with
	 * a trailing _2/_3 … and reported as a run note, so two pages can NEVER
	 * silently overwrite each other.
	 * Data: Emit_Templates.output_naming (page_file/{page} + legacy_page_file).
	 */
	static PageFileNames(run) {
		if (run._pageFileNames) return run._pageFileNames;
		const naming = DataService.Data.EmitTemplates.output_naming;
		const code = run.moduleCode ?? "MODULE";
		const legacy = (typeof process !== "undefined" && process.env && process.env.PAGENAME_OFF)
			|| !String(naming.page_file ?? "").includes("{page}");
		const used = new Set();
		run._pageFileNames = (run.pages ?? []).map((p, i) => {
			if (legacy) {
				return Utils.FillTemplate(naming.legacy_page_file ?? naming.page_file,
					{ code, NN: Utils.Pad2(i) });
			}
			const label = String(p.lessonLabel ?? (p.isOverview ? "0.0" : `${i}.0`))
				.replace(/[^\d.]/g, "") || String(i);
			let page = label.replace(/\./g, "_");
			if (used.has(page)) {
				let n = 2;
				while (used.has(`${page}_${n}`)) n++;
				page = `${page}_${n}`;
				run.AddNote("warn", "PageAssembler",
					`Two pages resolved the same lesson label "${label}" — the later file is disambiguated as _${n}; check the writer's lesson numbering.`);
			}
			used.add(page);
			return Utils.FillTemplate(naming.page_file, { code, page });
		});
		return run._pageFileNames;
	};

	/**
	 * THE WRITER'S RED-BRACKET JOURNAL SENTENCE IS LEARNER TEXT, NOT AN [Activity] OPENER.
	 * `[Go to your learning journal and complete activity 2B]` (the AGH family) parses with the activity tag and its id,
	 * so read as a tag it would open a box numbered 2B, strip the ids into a garbled Writers Note ("…complete and" — a
	 * KB constraint-1 breach) and leave the box EMPTY or let it swallow the next section (AGH1002 2.0 'Soil Structure').
	 * The gold renders the sentence as the learner's instruction inside its own activity box. Here — once, before the
	 * split, the scanner and the converter read the stream — a tag item whose ONLY tag is the activity tag and whose
	 * bracket is a journal SENTENCE (the data patterns, min_words..max_words) becomes a native black item holding
	 * the writer's words, brackets stripped (a trailing '}' typo too); ContentConverter's #journalInstructionBox
	 * then gives it its box. Data activity_wrapper.journal_instruction_box.bracket_sentence; env JOURNALINSTR_OFF.
	 */
	/**
	 * THE ONE-CELL TABLE IS THE WRITER'S BOX, NOT A TABLE. A writer often puts one element in a one-row one-cell table —
	 * «[video] [media item 7] <address> / [caption] Possessive Pronoun», «[alert] Did you know …», «[audio item 1] / …» —
	 * and the table renderer cannot show such a cell's tags, so the whole table shipped raw inside a hand-off box (the MTK
	 * leak guard). The human build shows the cell's content as ordinary body every time (the video and its caption, the
	 * alert box, the audio). On the MTK path (not a bilingual module), a free-body one-row one-cell table whose red tags are
	 * all plain elements of `tags` (instruction fragments allowed) and which no bare tag line just before it may own is
	 * replaced, before the page split and the widget scanner, by the items of its cell's paragraphs.
	 * Data dual_language.mtk_leak_guard.one_cell_unfold; env ONECELLUNFOLD_OFF.
	 */
	static #oneCellUnfold(items, run, normaliser) {
		const dl = DataService.Data.EmitTemplates.elements?.dual_language;
		const lg = dl?.mtk_leak_guard, cfg = lg?.one_cell_unfold;
		if (!dl || dl.enabled === false || !lg || lg.enabled === false || !cfg || cfg.enabled === false) return;
		const env = (k) => typeof process !== "undefined" && process.env && process.env[k];
		if (env(cfg.env || "ONECELLUNFOLD_OFF") || env("MTKGUARD_OFF") || env("MTKREO_OFF")) return;
		if (!run.mtkFlag) return;
		const reo = !env("REOTRANSLATE_OFF") && (/reoTranslate/i.test(run.resolvedRules?.body_class || "") || dl.use_mtk_flag === true
			|| (dl.code_prefixes || []).some((p) => String(run.moduleCode || "").toUpperCase().startsWith(String(p).toUpperCase())));
		if (reo) return;
		const tags = new Set(cfg.tags ?? []);
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		let n = 0;
		for (let k = items.length - 1; k >= 0; k--) {
			const it = items[k];
			if (it?.type !== "table") continue;
			const b = it.block, rows = b?.rows ?? [];
			if (rows.length !== 1 || (rows[0] ?? []).length !== 1) continue;
			const cell = String(rows[0][0] ?? "");
			let ok = true, any = false, first = null;
			for (const m of cell.matchAll(RED)) {
				const p = normaliser.Parse(m[1]);
				const t = p?.primary?.tag;
				if (first === null) first = t ?? "";
				if (t) { if (!tags.has(t)) { ok = false; break; } any = true; }
				else if (p?.class !== "instruction" && p?.class !== "noise") { ok = false; break; }
			}
			// the cell opens with a media / callout element (lead_tags) — a heading or body line first is a layout the
			// writer may have meant as a box of its own
			if (!ok || !any || !(cfg.lead_tags ?? []).includes(first) || !/^\s*\u{1f534}\[RED TEXT\]/u.test(cell)) continue;
			// a bare tag line just before the table may own it (a widget's data, a callout's one-cell body)
			let j = k - 1;
			while (j >= 0 && items[j]?.type === "black" && !String(items[j].text ?? "").trim()) j--;
			const prev = items[j];
			if (prev?.type === "tag" && prev.parse?.primary && !String(prev.blackAfter ?? "").trim()) continue;
			// inside a widget's run — a widget tag before the table with no section heading, page boundary or closing tag
			// between them — the table is the widget's (the scanner captures it): left as it is
			let inWidget = false;
			for (let w = k - 1, steps = 0; w >= 0 && steps < (cfg.lookback ?? 60); w--, steps++) {
				const q = items[w];
				if (q?.type !== "tag" || !q.parse?.primary) continue;
				const d = q.parse.primary.directive, t = q.parse.primary.tag;
				if (d === "INTERACTIVE" || (d === "SUBTAG" && t !== "data marker")) { inWidget = true; break; }
				if (d === "PAGE_BOUNDARY" || d === "SECTION_MARKER" || d === "CONTAINER_CLOSE" || /^h[1-3]$/.test(String(t))) break;
			}
			if (inWidget) continue;
			// the cell's own paragraphs (the extractor's side-channel), else the whole cell as one paragraph — never a split on
			// « / », which can fall inside a red span («[Alert top / image]»); a paragraph whose red markers do not pair is left
			const own = b.cellParas?.[0]?.[0];
			const paras = Array.isArray(own) && own.length ? own : [cell];
			const paired = (t) => (String(t).match(/\u{1f534}\[RED TEXT\]/gu) ?? []).length === (String(t).match(/\[\/RED TEXT\]\u{1f534}/gu) ?? []).length;
			if (!paras.every(paired)) continue;
			const blocks = paras.filter((t) => String(t ?? "").trim())
				.map((t) => ({ kind: "para", text: String(t), links: (b.links ?? []).slice(), wtPage: b.wtPage, list: "", listLevel: 0 }));
			if (!blocks.length) continue;
			items.splice(k, 1, ...PageSplitter.BuildItemStream(blocks, normaliser));
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} one-cell table(s) unfolded into the page body (the cell's elements, not a raw hand-off table).`);
	}

	/**
	 * THE TEMPLATE'S FRONT-MATTER FIELDS ARE NEVER LEARNER TEXT. A writer's front-matter block typed after the content
	 * start shipped its «Label: value» lines as body paragraphs («Module code: TEFUN02», «Key contacts: <name> <email>»,
	 * «Date submitted: 2024», «Curriculum Level: …»); the human build shows none of them. A free black paragraph whose text
	 * opens with one of the field labels is dropped. Data front_matter_metadata.body_strip; env FRONTMATTERBODY_OFF.
	 */
	static #frontMatterBody(items, run) {
		const cfg = DataService.Data.InputDocRules?.front_matter_metadata?.body_strip;
		if (!cfg || cfg.enabled === false || !cfg.pattern) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "FRONTMATTERBODY_OFF"]) return;
		const re = new RegExp(cfg.pattern, "i");
		let n = 0;
		for (let k = items.length - 1; k >= 0; k--) {
			const it = items[k];
			if (it?.type !== "black" || !re.test(String(it.text ?? ""))) continue;
			items.splice(k, 1);
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} front-matter field line(s) left out of the body (template metadata, not learner text).`);
	}

	static #journalBracketSentence(items, run) {
		const cfg = DataService.Data.EmitTemplates?.activity_wrapper?.journal_instruction_box;
		if (!cfg || cfg.enabled === false || cfg.bracket_sentence === false) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "JOURNALINSTR_OFF"]) return;
		const jRe = new RegExp(cfg.journal_pattern, "i"), vRe = new RegExp(cfg.verb_pattern, "i"), idRe = new RegExp(cfg.id_pattern, "i");
		// the writer's placeholder id («complete activity X.» / «XY.» / «XX.») — a journal sentence too (placeholder; env JOURNALPH_OFF)
		const ph = cfg.placeholder;
		const phRe = ph && ph.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[ph.env || "JOURNALPH_OFF"])
			? new RegExp(ph.id_pattern) : null;
		const stopOn = !!cfg.outer_stop && cfg.outer_stop.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[cfg.outer_stop.env || "JOURNALSTOP_OFF"]);
		let n = 0;
		for (const it of items) {
			if (!it || it.type !== "tag" || it.parse?.primary?.tag !== "activity" || (it.parse.tags ?? []).length !== 1) continue;
			// the sentence's own stop typed after the closing bracket («… activity 2A].» — outer_stop; env JOURNALSTOP_OFF)
			let raw = String(it.text ?? ""), stop = "";
			const os = stopOn ? /[\]}]\s*([.!?])\s*$/.exec(raw) : null;
			if (os) { stop = os[1]; raw = raw.slice(0, os.index + 1); }
			let inner = raw.replace(/^\s*\[/, "").replace(/[\]}]\s*$/, "").trim();
			if (stop && !/[.!?]$/.test(inner)) inner += stop;
			if (/[[\]{}]/.test(inner)) continue;   // a second bracket inside: not one sentence
			const words = inner.split(/\s+/).filter(Boolean).length;
			if (words < (cfg.min_words ?? 5) || words > (cfg.max_words ?? 40)) continue;
			if (!jRe.test(inner) || !vRe.test(inner) || !(idRe.test(inner) || (phRe && phRe.test(inner)))) continue;
			const tail = String(it.blackAfter ?? "");
			it.type = "black";
			it.text = inner + (tail.trim() ? (/^\s*[.,;:!?]/.test(tail) ? tail.trim() : " " + tail.trim()) : "");
			delete it.parse; delete it.blackAfter;
			it._journalSentence = true;
			// the post-pass moves ONLY these sentences out of a box numbered with another id (a writer's black journal line
			// inside her own activity box stays there — the HES form, already the gold's)
			(run._journalTexts ??= new Set()).add(it.text.replace(/[*_]/g, "").replace(/\s+/g, " ").trim().toLowerCase());
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler",
			`${n} red-bracket journal instruction${n > 1 ? "s" : ""} read as the learner's sentence, not an [Activity] opener (journal_instruction_box.bracket_sentence).`);
	}

	/**
	 * THE UNTAGGED WHAKATAUKĪ (KB 07B §7; the gold boxes it where its text survives). A free black
	 * paragraph whose every word is Māori-phonotactic, followed by an English paragraph, is a proverb + translation the writer
	 * typed without the [Whakatauki] tag: the reo item is re-typed as that tag with the reo line as its payload, so the
	 * existing proverb-only callout (reo + english, bold / italic stripped) builds the box. A pair already under a whakatauki
	 * tag and a greeting are left alone. Data callouts.untagged_proverb; env UNTAGPROVERB_OFF.
	 * Refinements: (1) the English line is handed to the box HERE as the
	 * writer's `reo | english` one-line form (split_payload_on_pipe makes it two <p>s) and its own item emptied — by emit time
	 * a later pass has merged it with the paragraphs after it (PHE1005), so the proverb gather would take it for
	 * commentary and leave it out; an "English" line over max_english_chars is commentary and stays free (reo-only box);
	 * (2) a proverb that is a widget's or a strict callout's content (the item before it is an INTERACTIVE directive —
	 * ANZH301 / 302's `[interactive]` — or an owner_tags callout with a payload or more content) is left to it, while a
	 * payload-free owner_tags callout whose whole content is the pair is REPLACED by the whakatauki (AGH1002 / CBI1004 /
	 * CEDT207 / CEDT301 / XDLS901's `[Important]` + proverb — the gold ships the whakatauki alone); (3) the later lines of a writer-TAGGED proverb (a whakatauki tag within
	 * tagged_lookback short lines before it — ENGC204's four-line box) are left to that tag; (4) the writer's bare label
	 * line just before the pair (`Whakataukī`, `[Whakataukī]`, `Whakatauki:`) and an inline `Whakatauki:` prefix are dropped,
	 * as the gold drops them (label_pattern / label_prefix_pattern).
	 */
	/**
	 * THE BLACK-TYPED MEDIA TAG, AFTER THE SCAN. The extractor re-marks a black [H1]–[H6] at a
	 * paragraph head red; a black `[Image …]` / `[Video …]` promoted there would become a widget MEMBER when it
	 * followed an open widget (swallowing the next section). So media tags wait until the page's
	 * widget scan has run: an UNCONSUMED black item that OPENS its paragraph with a bracket the normaliser resolves to a
	 * listed media tag becomes the tag item a red tag builds (`{type: "tag", parse, text, blackAfter, block}` — PageSplitter's
	 * shape), and ContentConverter renders it through the image / video emitter. Data InputDocRules.red_runs.black_lead_tag.
	 * media_after_scan {enabled, env, tags}; env BLACKLEADMEDIA_OFF.
	 */
	static #blackLeadMedia(page, normaliser, run) {
		const cfg = DataService.Data.InputDocRules?.red_runs?.black_lead_tag?.media_after_scan;
		if (!cfg || cfg.enabled === false || !normaliser) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "BLACKLEADMEDIA_OFF"]) return;
		const allow = new Set((cfg.tags ?? ["image", "video"]).map((t) => String(t).toLowerCase()));
		const re = /^(\s*)(\*\*|__)?\[([^\[\]\u{1f534}]{1,200})\]/u;
		const items = page?.items ?? [];
		let n = 0;
		for (let i = 0; i < items.length; i++) {
			const it = items[i];
			if (!it || it.type !== "black" || it.consumedBy !== undefined) continue;
			if (i > 0 && items[i - 1]?.block === it.block) continue;            // not the head of its paragraph
			const m = String(it.text ?? "").match(re);
			if (!m) continue;
			let parse = null;
			try { parse = normaliser.Parse("[" + m[3] + "]"); } catch { parse = null; }
			const tag = parse?.primary?.tag;
			if (!tag || !allow.has(String(tag).toLowerCase())) continue;
			// the CALLOUT fence: a callout box ([alert] / [important] / …) gathers the black text (and headings) after its tag and
			// a tag item ends it — a media line inside that reach stays black (HIS1005 6.0's `[Image Link]` inside an [alert]
			// emptied the box on the first probe). Walk back over black items and heading tags to the nearest other tag.
			if (cfg.callout_fence !== false) {
				const callouts = DataService.Data.EmitTemplates?.callouts?.by_tag ?? {};
				const passTags = new Set(cfg.callout_walk_pass_tags ?? ["body"]);
				let h = i - 1;
				while (h >= 0 && items[h] && (items[h].type === "black"
					|| (items[h].type === "tag" && (/^h[1-6]$/.test(String(items[h].parse?.primary?.tag ?? ""))
						|| passTags.has(String(items[h].parse?.primary?.tag ?? "")) || items[h].parse?.class === "instruction")))) h--;
				const prevTag = h >= 0 && items[h]?.type === "tag" ? String(items[h].parse?.primary?.tag ?? "") : "";
				if (prevTag && Object.prototype.hasOwnProperty.call(callouts, prevTag)) continue;
			}
			items[i] = { type: "tag", parse, text: " [" + m[3] + "] ", blackAfter: (m[2] ?? "") + String(it.text).slice(m[0].length),
				block: it.block, blackLeadMedia: true };
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} media tag(s) typed in black at a paragraph head read as the writer's red tag, after the widget scan.`);
	};

	/**
	 * THE BLACK DEVELOPER NOTE IS A WRITERS NOTE. A writer's note to the developer typed in BLACK ("Note to CS – Please use
	 * Sassoon font.", "DEV: Colour code for phase 2:", "Can we make something like this please?") would ship as learner text; the
	 * human build drops these lines. A black item whose plain text matches red_flag.black_developer_note.pattern — or a heading
	 * tag (heading_tags) whose whole payload does — becomes the writer-instruction item the normaliser already makes of that text
	 * (Parse → class "instruction", no tag), so ContentConverter's instruction path prints the red Writers Note in its place. A
	 * parse that is not a pure instruction is left alone. Data red_flag.black_developer_note; env BLACKDEVNOTE_OFF.
	 *
	 * @param {Object[]} items - the module's body items (mutated in place)
	 * @param {ConversionRun} run
	 * @param {TagNormaliser} normaliser
	 */
	static #blackDeveloperNote(items, run, normaliser) {
		const cfg = DataService.Data.EmitTemplates?.red_flag?.black_developer_note;
		if (!cfg || cfg.enabled === false || !normaliser || !cfg.pattern) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "BLACKDEVNOTE_OFF"]) return;
		const re = new RegExp(cfg.pattern, "i");
		const plain = (s) => String(s ?? "").replace(/<[^>]+>|\*+/g, "").replace(/\s+/g, " ").trim();
		const heads = new Set(cfg.heading_tags ?? []);
		// a black line inside a widget's capture (the nearest tag before it, over black lines only, is a widget tag) is the
		// widget's own content — the hand-off box keeps it as the writer typed it (cfg.inside_widget: false)
		const inWidget = (i) => {
			if (cfg.inside_widget !== false) return false;
			let h = i - 1;
			while (h >= 0 && items[h] && items[h].type === "black") h--;
			const tag = h >= 0 && items[h]?.type === "tag" ? items[h].parse?.primary?.tag : null;
			try { return !!tag && normaliser.GetWidgetTypes(tag).length > 0; } catch { return false; }
		};
		let n = 0;
		for (const [i, it] of items.entries()) {
			if (!it) continue;
			let text = null;
			if (it.type === "black" && !inWidget(i)) text = plain(it.text);
			else if (it.type === "tag" && heads.has(it.parse?.primary?.tag) && !String(it.text ?? "").replace(/\[[^\]]*\]|\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, "").trim())
				text = plain(it.blackAfter);   // a heading tag whose whole payload is the note
			if (!text || !re.test(text)) continue;
			const p = normaliser.Parse(text);
			if (p?.class !== "instruction" || p.primary) continue;
			it.type = "tag"; it.parse = p; it.text = text; it.blackAfter = "";
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} black developer note${n > 1 ? "s" : ""} read as the Writers Note, not learner text (red_flag.black_developer_note).`);
	};

	/**
	 * A HIGHLIGHT REQUEST INSIDE A SENTENCE NO LONGER CUTS IT. The writer types a red highlight request in the middle of
	 * a sentence — «Māori perspectives value [highlight text] **mana (personal …)** as key aspects», «Being [highlight text]
	 * **gifted** means …», «[emphasise / highlight text]», «[end highlight]» — and the tag item cut the sentence into two
	 * paragraphs wherever it stood: in the free body, in an accordion pane, on a flip card's back, in an activity box.
	 * «[highlight]» and «[highlight text]» are also the word-select widget's tag names, so the scanner took the request
	 * for a widget inside its host's capture. The human keeps the sentence whole and marks the words in different ways
	 * from page to page (a highlight span, bold or plain), so — once, before the split and the scanner read the stream — a
	 * tag item whose whole text is one such request (the data bare_pattern), standing in the same paragraph between text
	 * that does not end a sentence and text that continues it, is taken out and the two halves joined; the writer's own
	 * marks stay and no mark is guessed. The word / letter / phrase highlighter quiz is never matched.
	 * Data: Emit_Templates.elements.inline_format_request.highlight_forms   Env toggle: FMTREQHILITE_OFF (a word closed by its mark before the request: marked_before, FMTREQMARKED_OFF)
	 */
	static #highlightRequestInSentence(items, run) {
		const base = DataService.Data.EmitTemplates?.elements?.inline_format_request;
		const cfg = base?.highlight_forms;
		if (!cfg || cfg.enabled === false || !cfg.bare_pattern || !Array.isArray(items)) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "FMTREQHILITE_OFF"]) return;
		const reqRe = new RegExp(cfg.bare_pattern, "iu");
		// the text before may end in the writer's own closing mark («**and** [bold] listen») — the sentence still runs
		const mb = base.marked_before;
		const mbOn = !!mb && mb.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[mb.env || "FMTREQMARKED_OFF"]);
		const beforeRe = new RegExp((mbOn && mb.before_pattern) || (cfg.before_pattern ?? base.before_pattern ?? "[\\p{L}\\p{N},’'\")]\\s*$"), "u");
		const afterRe = new RegExp((mbOn && mb.after_pattern) || (cfg.after_pattern ?? base.more_forms?.after_pattern ?? "^\\s*(?:\\*{1,2}[\\p{L}\\p{N}]|[.,;:!?)’'\"]|\\p{Ll})"), "u");
		const innerOf = (x) => String(x?.text ?? "").replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").trim();
		// the bare bold / italic vocabulary joins on the same terms (stream_bare); a pair's opener and a named request do not
		const sb = base.stream_bare;
		const sbOn = !!sb && sb.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[sb.env || "FMTREQSTREAM_OFF"]);
		const sbRes = sbOn ? [base.bare_request_pattern, base.more_forms?.bare_pattern, mbOn ? mb.bare_pattern : null].filter(Boolean).map((p) => new RegExp(p, "iu")) : [];
		const endRe = sbOn && base.more_forms?.end_pattern ? new RegExp(base.more_forms.end_pattern, "iu") : null;
		const openRe = sbOn && base.bare_request_pattern ? new RegExp(base.bare_request_pattern, "iu") : null;
		const isReq = (x, i) => {
			const t = innerOf(x);
			if (reqRe.test(t)) return true;
			if (!sbRes.some((r) => r.test(t))) return false;
			if (!endRe) return true;
			// the pair «[bold] words [end bold]» is the later pass's: neither its opener nor its closer joins here
			const nx = items[i + 1], pv = items[i - 1];
			if (!endRe.test(t)) return !(nx && nx.type === "tag" && nx.block === x.block && endRe.test(innerOf(nx)));
			return !(openRe && pv && pv.type === "tag" && pv.block === x.block && openRe.test(innerOf(pv)));
		};
		let n = 0;
		for (let i = 1; i < items.length; i++) {
			const it = items[i];
			if (!it || it.type !== "tag" || !isReq(it, i)) continue;
			// the sentence's first half: the item before, or — when that is a request already joined — the item it joined
			let prev = items[i - 1];
			if (prev?._sentenceHost) prev = prev._sentenceHost;
			if (!prev || prev.block !== it.block || (prev.type !== "black" && prev.type !== "tag")) continue;
			const key = prev.type === "black" ? "text" : "blackAfter";
			const before = String(prev[key] ?? ""), after = String(it.blackAfter ?? "");
			if (!before.trim() || !beforeRe.test(before) || !afterRe.test(after)) continue;
			const a = after.replace(/^\s+/, "");
			// «**as**» + «**.** It helps» → «**as.** It helps»: two runs in the same mark meet at a stop
			const b = before.replace(/\s+$/, ""), mm = mbOn ? /^([*_]+)[.,;:!?)’'"]/.exec(a) : null;
			if (mm && b.endsWith(mm[1])) prev[key] = b.slice(0, -mm[1].length) + a.slice(mm[1].length);
			else prev[key] = b + (/^[.,;:!?)’'"]/.test(a) ? "" : " ") + a;
			// the request item stays where it stands, its words moved: the scanner and every later pass see the same items
			it.blackAfter = "";
			it._sentenceHost = prev;
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} highlight / formatting request${n === 1 ? "" : "s"} inside a sentence taken out, the sentence kept whole (inline_format_request.highlight_forms / stream_bare).`);
	}

	/**
	 * AN AUDIO-ANIMATION REQUEST TYPED IN BLACK IS THE ANIMATION VIDEO. A writer who typed «[Audio Animation 1:» in black
	 * (bold-underlined, linked to the module's audio-script document) and closed the bracket in a red note left a paragraph
	 * the red-tag rule (elements.audio_animation) never sees, so the bracket shipped as learner text. Before the split and
	 * the scanner, such a paragraph — an unclosed bracket naming an audio animation — becomes that tag item (its words, its
	 * paragraph's links), and MediaBuilder builds the animation's video frame and To Do with the writer's link.
	 * Data elements.audio_animation.black_opener   Env toggle: AUDIOANIMBLACK_OFF
	 */
	static #blackAudioAnimation(items, run, normaliser) {
		const aa = DataService.Data.EmitTemplates?.elements?.audio_animation;
		const cfg = aa?.black_opener;
		if (!cfg || cfg.enabled === false || aa.enabled === false || !cfg.pattern || !normaliser || !Array.isArray(items)) return;
		if (typeof process !== "undefined" && process.env && (process.env[cfg.env || "AUDIOANIMBLACK_OFF"] || process.env[aa.env || "AUDIOANIM_OFF"])) return;
		const re = new RegExp(cfg.pattern, "i");
		let n = 0;
		for (const it of items) {
			if (!it || it.type !== "black") continue;
			const t = String(it.text ?? "").replace(/[*_]/g, "").replace(/\s+/g, " ").trim();
			if (!re.test(t)) continue;
			const text = "[" + t.replace(/^\[\s*/, "").replace(/[\s:;,–-]+$/, "") + "]";
			let p = null;
			try { p = normaliser.Parse(text + " "); } catch { p = null; }
			if (!p?.primary) continue;
			it.type = "tag"; it.parse = p; it.text = " " + text + " "; it.blackAfter = "";
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} audio-animation request${n > 1 ? "s" : ""} typed in black read as the animation tag (audio_animation.black_opener).`);
	}

	static #untaggedProverb(items, run, normaliser) {
		const cfg = DataService.Data.EmitTemplates?.callouts?.untagged_proverb;
		if (!cfg || cfg.enabled === false || !normaliser) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "UNTAGPROVERB_OFF"]) return;
		const syl = new RegExp(cfg.syllable_pattern, "i"), punct = new RegExp(cfg.word_strip_pattern, "g");
		const excl = cfg.exclude_pattern ? new RegExp(cfg.exclude_pattern, "i") : null;
		const labelRe = cfg.label_pattern ? new RegExp(cfg.label_pattern, "i") : null;
		const prefixRe = cfg.label_prefix_pattern ? new RegExp(cfg.label_prefix_pattern, "i") : null;
		const sepRe = /\s[|–—]\s/;
		const plain = (s) => String(s ?? "").replace(/<[^>]+>|\*+/g, "").replace(/(?<![A-Za-z])_+|_+(?![A-Za-z])/g, "").normalize("NFC").replace(/\s+/g, " ").trim();
		const words = (s) => plain(s).replace(punct, " ").split(/\s+/).filter(Boolean);
		const empty = (it) => !String(it?.text ?? "").trim() && !String(it?.blackAfter ?? "").trim();
		const maxReo = cfg.max_reo_chars ?? 200;
		const eng0 = (x) => String(x?.text ?? "").trim();
		// The overview's MODULE MENU region — from a `[TITLE BAR]` section marker to the next section marker — is
		// built by the menu builder, not the callout emitter; a proverb there stays as the writer typed it (ENGI202's Understand
		// block). The skip applies to the payload pass only. Data
		// callouts.untagged_proverb.payload_forms.skip_menu_region; env WHKFORMS_OFF.
		const pfc = cfg.payload_forms;
		const menuGuard = !!pfc && pfc.enabled !== false && pfc.skip_menu_region === true
			&& !(typeof process !== "undefined" && process.env && process.env[pfc.env || "WHKFORMS_OFF"]);
		const inMenu = new Set();
		if (menuGuard) {
			let on = false;
			for (let k = 0; k < items.length; k++) {
				const p = items[k]?.type === "tag" ? items[k].parse?.primary : null;
				if (p?.directive === "SECTION_MARKER" || p?.directive === "PAGE_BOUNDARY") { on = p.tag === "title bar"; continue; }
				if (on) inMenu.add(k);
			}
		}
		let n = 0, nOwn = 0;
		for (let k = 0; k < items.length; k++) {
			const it = items[k];
			if (!it || it.type !== "black") continue;
			const reo = plain(it.text);
			if (!reo || reo.length > maxReo || (excl && excl.test(reo))) continue;
			const w = words(it.text);
			if (w.length < (cfg.min_reo_words ?? 4) || !w.every((x) => syl.test(x))) continue;
			let j = k + 1; while (j < items.length && items[j]?.type === "black" && empty(items[j])) j++;
			const nx = items[j];
			if (!nx || nx.type !== "black") continue;
			const ew = words(nx.text).filter((x) => /^[A-Za-zāēīōūĀĒĪŌŪ]+$/.test(x));
			if (ew.length < (cfg.min_english_words ?? 3) || ew.filter((x) => syl.test(x)).length / ew.length >= (cfg.max_english_reo_share ?? 0.5)) continue;
			// (2) / (3): walk back over empties and up to tagged_lookback short black lines — a whakatauki tag there owns
			// this line; the nearest non-empty item an INTERACTIVE tag owns it as its widget's content
			let p = k - 1; while (p >= 0 && items[p]?.type !== "table" && empty(items[p])) p--;
			if (items[p]?.type === "tag" && items[p].parse?.primary?.directive === "INTERACTIVE") continue;
			let owner = null;
			if (items[p]?.type === "tag" && (cfg.owner_tags ?? []).includes(items[p].parse?.primary?.tag)) {
				// a payload-free callout whose WHOLE content is the pair (a tag / the end follows the English) is the writer's
				// proverb box under another name — the gold ships the whakatauki alone (AGH1002, CBI1004, CEDT207, CEDT301,
				// XDLS901); any other owned line stays with its callout
				let e = j + 1; while (e < items.length && items[e]?.type === "black" && empty(items[e])) e++;
				if (String(items[p].blackAfter ?? "").trim() || (e < items.length && items[e]?.type !== "tag")) continue;
				owner = items[p];
			}
			let q = p, back = 0, owned = false;
			while (q >= 0 && back <= (cfg.tagged_lookback ?? 2)) {
				const b = items[q];
				if (b?.type === "tag") { owned = b.parse?.primary?.tag === "whakatauki"; break; }
				if (b?.type !== "black") break;
				if (!empty(b)) { if (plain(b.text).length > maxReo) break; back++; }
				q--;
			}
			if (owned) continue;
			const parse = normaliser.Parse(cfg.retag_as);
			if (parse?.primary?.tag !== "whakatauki") continue;
			if (owner && plain(eng0(nx)).length > (cfg.max_english_chars ?? 200)) continue;
			if (owner) { owner.type = "black"; delete owner.parse; owner.text = ""; owner.blackAfter = ""; nOwn++; }
			// (4) the bare label line before the pair
			if (labelRe && items[p]?.type === "black" && labelRe.test(plain(items[p].text))) { items[p].text = ""; items[p].blackAfter = ""; }
			let payload = String(it.text).trim();
			if (prefixRe) payload = payload.replace(prefixRe, "");
			// (1) the English joins the payload as the writer's one-line `reo | english` form, unless it is commentary
			const eng = eng0(nx);
			if (plain(eng).length <= (cfg.max_english_chars ?? 200) && !sepRe.test(payload) && !sepRe.test(eng)) {
				payload = `${payload} | ${eng}`;
				nx.text = ""; nx.blackAfter = "";
			}
			it.type = "tag"; it.parse = parse; it.blackAfter = payload; it.text = cfg.retag_as;
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} untagged proverb${n > 1 ? "s" : ""} (a reo line + its English) read as ${cfg.retag_as}${nOwn ? ` (${nOwn} in place of a payload-free callout that held only the pair)` : ""} (callouts.untagged_proverb).`);
		// THE PROVERB AS A TAG'S PAYLOAD:
		// the reo line typed on the tag's own line — `[Body] *Tuku iho, he tapu te upoko.*` (PHE1007, BLLR201) or a callout whose
		// whole content is the pair, `[Alert] *Kō ngā tahu ā ō tapuwai inanahi…*` + the English (ANZH105 / 205, SSOG101, XDLS501's
		// `[Important Statement]`) — is the same proverb box; the gold ships div.whakatauki on every one. The tag is re-typed as the
		// whakatauki with `reo | english` as its payload. Data callouts.untagged_proverb.payload_forms; env WHKFORMS_OFF.
		const pf = cfg.payload_forms;
		if (!pf || pf.enabled === false || (typeof process !== "undefined" && process.env && process.env[pf.env || "WHKFORMS_OFF"])) return;
		let n2 = 0;
		for (let k = 0; k < items.length; k++) {
			const it = items[k];
			const tag = it?.type === "tag" ? it.parse?.primary?.tag : null;
			if (!tag || !(pf.tags ?? []).includes(tag) || inMenu.has(k)) continue;
			let pay = String(it.blackAfter ?? "").trim();
			if (prefixRe) pay = pay.replace(prefixRe, "");
			const reo = plain(pay);
			if (!reo || reo.length > maxReo || (excl && excl.test(reo))) continue;
			const w = words(pay);
			if (w.length < (cfg.min_reo_words ?? 4) || !w.every((x) => syl.test(x))) continue;
			let j = k + 1; while (j < items.length && items[j]?.type === "black" && empty(items[j])) j++;
			const nx = items[j];
			if (!nx || nx.type !== "black") continue;
			const ew = words(nx.text).filter((x) => /^[A-Za-zāēīōūĀĒĪŌŪ]+$/.test(x));
			if (ew.length < (cfg.min_english_words ?? 3) || ew.filter((x) => syl.test(x)).length / ew.length >= (cfg.max_english_reo_share ?? 0.5)) continue;
			const eng = eng0(nx);
			if (plain(eng).length > (cfg.max_english_chars ?? 200)) continue;
			if ((pf.whole_content_tags ?? []).includes(tag)) {
				let e = j + 1; while (e < items.length && items[e]?.type === "black" && empty(items[e])) e++;
				if (e < items.length && items[e]?.type !== "tag") continue;   // the callout holds more than the pair: it stays
			}
			const parse = normaliser.Parse(cfg.retag_as);
			if (parse?.primary?.tag !== "whakatauki") continue;
			it.parse = parse; it.text = cfg.retag_as;
			it.blackAfter = !sepRe.test(pay) && !sepRe.test(eng) ? `${pay} | ${eng}` : pay;
			if (it.blackAfter !== pay) { nx.text = ""; nx.blackAfter = ""; }
			n2++;
		}
		if (n2) run.AddNote("info", "PageAssembler", `${n2} proverb${n2 > 1 ? "s" : ""} typed as a tag's payload read as ${cfg.retag_as} (callouts.untagged_proverb.payload_forms).`);
	}

	/**
	 * THE BOLD ACTIVITY ID AFTER A WIDGET TAG (the FRNO family's form): `[Reorder autocheck]]
	 * **2C****Put the conversation together**` — the id and title typed in bold black after the widget tag, so no box would open and
	 * both would ship inside the hand-off box; the gold boxes each as div.activity[number=2C] titled by the bold words. The widget tag
	 * is re-parsed with an `[Activity 2C]` co-tag (the activity + widget span, which opens the numbered box) and the bold id
	 * leaves the tail. A stray bracket span between them (`[Wordfind autocheck] ] **1E**…`, a noise item) hands the tail's id to the
	 * widget tag just before it on the same paragraph. Data Tag_Lexicon _meta.bold_id_widget_activity; env BOLDIDACT_OFF.
	 */
	static #boldIdWidgetActivity(items, run, normaliser) {
		const cfg = DataService.Data.TagLexicon?._meta?.bold_id_widget_activity;
		if (!cfg || cfg.enabled === false || !normaliser) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "BOLDIDACT_OFF"]) return;
		const re = new RegExp(cfg.id_pattern);
		let n = 0;
		for (let i = 0; i < items.length; i++) {
			const it = items[i];
			if (it?.type !== "tag") continue;
			const m = re.exec(String(it.blackAfter ?? ""));
			if (!m) continue;
			let w = it;
			if (!it.parse?.primary && i > 0 && items[i - 1]?.type === "tag" && items[i - 1].block === it.block) w = items[i - 1];
			const p = w.parse?.primary;
			if (!p || p.directive !== "INTERACTIVE" || (w.parse.tags ?? []).some((t) => t.tag === "activity")) continue;
			// the typed form `[Activity 2C – <widget words>]`, so the bold title after the id becomes the box's <h3>
			// (activity_wrapper.embedded_interactive_activity.typed_tag_title); the widget words keep resolving the widget
			const inner = String(w.text ?? "").replace(/[[\]]/g, " ").replace(/\s+/g, " ").trim();
			const text = `[Activity ${m[1]} – ${inner}]`;
			const np = normaliser.Parse(text);
			if (!np?.primary || np.primary.directive !== "INTERACTIVE" || !(np.tags ?? []).some((t) => t.tag === "activity")) continue;
			w.parse = np; w.text = text;
			const tail = String(it.blackAfter).slice(m[0].length);
			if (w !== it) { w.blackAfter = String(w.blackAfter ?? "") + tail; it.blackAfter = ""; }   // the stray bracket's tail moves to its widget
			else it.blackAfter = tail;
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} widget tag${n > 1 ? "s" : ""} followed by a bold activity id read as the activity + widget span (bold_id_widget_activity).`);
	}

	/**
	 * THE CO-TAG'S DUPLICATE-ID GUARD. TagNormaliser gives an `[Activity 2] [H3] Title` span the activity's
	 * primary slot (Tag_Lexicon _meta.activity_heading_cotag); but when the SAME id opens another activity later on the same
	 * page, the writer put the id on a section heading AND on the real activity (MXEX202 lesson 2: `[Activity 2] [H3] Double
	 * or Half` … `[Activity 2] [H3] Fun Water Challenge`; HES1002 2.0) — the gold boxes only the later one and keeps the
	 * first a free heading, while a box on the first shifts every later id by the id de-dupe. Such a span hands the primary
	 * slot back to its heading (the plain parse). Data activity_heading_cotag.duplicate_id_guard; env ACTHDCOTAG_OFF.
	 */
	static #cotagDuplicateId(items, run) {
		const cfg = DataService.Data.TagLexicon?._meta?.activity_heading_cotag;
		if (!cfg || cfg.enabled === false || cfg.duplicate_id_guard === false) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "ACTHDCOTAG_OFF"]) return;
		const idOf = (x) => String(x?.parse?.numbers?.[0] ?? "").toUpperCase();
		let n = 0;
		for (let i = 0; i < items.length; i++) {
			const it = items[i];
			if (it?.type !== "tag" || !it.parse?.cotagHeading || it.parse.primary?.tag !== "activity" || !idOf(it)) continue;
			for (let j = i + 1; j < items.length; j++) {
				const x = items[j];
				if (x?.type !== "tag" || !x.parse?.primary) continue;
				if (x.parse.primary.directive === "PAGE_BOUNDARY") break;
				if (x.parse.primary.tag === "activity" && idOf(x) === idOf(it)) {
					it.parse.primary = it.parse.cotagHeading; n++;
					break;
				}
			}
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} [Activity] + heading co-tag${n > 1 ? "s" : ""} kept as a heading: the same id opens a later activity (activity_heading_cotag.duplicate_id_guard).`);
	}

	/**
	 * THE WRITER'S BARE [Summary] IS AN ALERT BOX TITLED 'Summary' (the AGH family's own tag; the gold boxes the whole
	 * run as `div.alert` headed `<h4>Summary</h4>`). The span resolves to no tag, so left alone it would ship as a Writers
	 * Note with the bullets free. Here it is re-parsed as the data's retag_as (the
	 * plain alert callout) with the tag word as its first content line: the ordinary strict alert path gathers the run and
	 * #alertTitleHeading lifts that short first line to the h4. Data callouts.bare_summary_alert; env SUMMARYALERT_OFF.
	 */
	static #bareSummaryAlert(items, run, normaliser) {
		const cfg = DataService.Data.EmitTemplates?.callouts?.bare_summary_alert;
		if (!cfg || cfg.enabled === false || !normaliser) return;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "SUMMARYALERT_OFF"]) return;
		const re = new RegExp(cfg.pattern, "i");
		let n = 0;
		for (const it of items) {
			if (!it || it.type !== "tag" || it.parse?.primary || !re.test(String(it.text ?? ""))) continue;
			const parse = normaliser.Parse(cfg.retag_as);
			if (!parse?.primary) continue;
			it.parse = parse; it.text = cfg.retag_as;
			it.blackAfter = cfg.title + (String(it.blackAfter ?? "").trim() ? " " + String(it.blackAfter).trim() : "");
			n++;
		}
		if (n) run.AddNote("info", "PageAssembler", `${n} bare [Summary] tag${n > 1 ? "s" : ""} read as an alert titled '${cfg.title}' (callouts.bare_summary_alert).`);
	}

	/**
	 * Converts ONE module end-to-end: the single entry point that turns an
	 * already-extracted Writers Template (run.wtBlocks, parsed by an earlier
	 * pipeline stage) into finished, ready-to-save HTML pages plus the
	 * interactives hand-off manifest. Fills in run.pages, run.interactives, and
	 * run.outputs on the ConversionRun object passed in.
	 *
	 * THE STAGES, IN ORDER:
	 *   1. Resolve this module's HTML rendering conventions (ConventionResolver)
	 *      — must run after ModuleResolver has already set run.groupKey.
	 *   2. Split the Writers Template's content into an ordered "item stream",
	 *      then split that into pages — one entry in run.pages per lesson or
	 *      overview (PageSplitter).
	 *   3. For each page: scan it for "interactive bundles" (clusters of writer
	 *      content that should become one interactive widget, e.g. a flip-card
	 *      set) BEFORE converting the page's content, so the converter knows
	 *      where to place each widget's placeholder or built-out HTML
	 *      (InteractiveScanner) — then convert the page's content to HTML
	 *      (ContentConverter).
	 *   4. Work out the module's English / Te Reo Māori title, including the
	 *      fallback rules for when the Writers Template's own [TITLE BAR] tag
	 *      was incomplete, ambiguous, or left as unfilled placeholder text.
	 *   5. Build the acknowledgements section (AcksBuilder) — generated for
	 *      every module, whether or not any media actually needs crediting.
	 *   6. Wrap each page's converted content in the shared page chrome
	 *      ("skeleton" HTML — the header/menu/footer common to every page;
	 *      SkeletonBuilder), chaining each page's prev/next footer links to its
	 *      sibling output files, and push the finished HTML onto run.outputs.
	 *   7. Build the {CODE}_interactives.txt hand-off manifest — a plain-text
	 *      worklist of every interactive widget the converter could not fully
	 *      build automatically (ManifestBuilder) — and push it onto
	 *      run.outputs too.
	 *
	 * DATA SHAPES:
	 * A `pageProducts` entry (built internally below, one per page) looks like:
	 *   { page: <the PageSplitter page object>,
	 *     content: <ContentConverter's { html, titleBar, … } result for that page> }
	 * A `run.outputs` entry (this method's final result) looks like:
	 *   { filename: "CODE-00.html", content: "<...finished HTML string...>", kind: "page" }
	 *   { filename: "CODE_interactives.txt", content: "<...manifest text...>", kind: "manifest" }
	 *
	 * @param {ConversionRun} run - the shared scratchpad object for this
	 *   conversion job; must already be prepared with run.wtBlocks (the
	 *   extracted Writers Template content) and run.mediaItems (the parsed
	 *   Media List) before this is called
	 * @param {TagNormaliser} normaliser - the compiled [bracketed tag] matcher
	 *   used throughout the pipeline to recognise and classify writer tags
	 * @returns {Promise<void>} nothing is returned directly — every result is
	 *   written onto the `run` object's pages / interactives / outputs arrays
	 */
	static async AssembleModule(run, normaliser) {
		const naming = DataService.Data.EmitTemplates.output_naming;

		// HTML conventions via the group cascade (series → subject×phase →
		// global) — must run after ModuleResolver set run.groupKey
		ConventionResolver.Resolve(run);

		// ---- [5] split into pages -----------------------------------------
		const items = PageSplitter.BuildItemStream(run.wtBlocks, normaliser);
		PageAssembler.#journalBracketSentence(items, run);   // before the split, the scanner and the converter all read the item
		PageAssembler.#bareSummaryAlert(items, run, normaliser);   // SUMMARYALERT_OFF
		PageAssembler.#cotagDuplicateId(items, run);   // ACTHDCOTAG_OFF — the co-tag rule's own guard
		PageAssembler.#boldIdWidgetActivity(items, run, normaliser);   // BOLDIDACT_OFF
		PageAssembler.#untaggedProverb(items, run, normaliser);   // UNTAGPROVERB_OFF
		PageAssembler.#blackDeveloperNote(items, run, normaliser);   // BLACKDEVNOTE_OFF
		PageAssembler.#highlightRequestInSentence(items, run);   // FMTREQHILITE_OFF — before the scanner reads the request as a widget tag
		PageAssembler.#blackAudioAnimation(items, run, normaliser);   // AUDIOANIMBLACK_OFF
		PageAssembler.#oneCellUnfold(items, run, normaliser);   // ONECELLUNFOLD_OFF — before the split and the scanner
		PageAssembler.#frontMatterBody(items, run);   // FRONTMATTERBODY_OFF
		run.pages = PageSplitter.Split(items, run, normaliser);
		if (!run.pages.length) {
			run.AddNote("error", "PageAssembler",
				"No pages could be assembled from this document — nothing to output.");
			return;
		}

		// ---- [6] scan interactives + convert content ------------------------
		// (scan first so converted pages can place the placeholders; bundle
		// indexes are run-wide and 1-based so the manifest reads naturally)
		const pageProducts = [];
		for (const page of run.pages) {
			const bundles = InteractiveScanner.ScanPage(page, normaliser, run);
			PageAssembler.#blackLeadMedia(page, normaliser, run);   // AFTER the scan (BLACKLEADMEDIA_OFF)
			for (const b of bundles) {
				b.index = run.interactives.length + 1;
				b.page = page;
				run.interactives.push(b);
				// A NESTED sub-bundle absorbed into a host widget (e.g. an accordion
				// panel that swallows a shapeHover widget inside it) is registered right
				// after its host so it gets its own run-wide cv2-index + manifest entry,
				// and so the host's builder can render its honest placeholder by index.
				// The host has already consumed the nested items' range while scanning,
				// so they must never be independently re-scanned as their own bundle.
				for (const nb of (b.nestedBundles ?? [])) {
					nb.index = run.interactives.length + 1;
					nb.page = page;
					run.interactives.push(nb);
				}
			}
			const content = ContentConverter.ConvertPage(page, bundles, run, normaliser);
			pageProducts.push({ page, content });
			// Browser-only progress reporting + a repaint yield. This whole per-page
			// loop runs SYNCHRONOUSLY, so without help the browser's Convert-panel
			// progress bar would never get a chance to redraw until the entire module
			// had finished converting. When (and only when) the browser entry point set
			// run.onProgress, report the page that just finished, then yield one
			// "macrotask" — `await new Promise((resolve) => setTimeout(resolve, 0))`
			// hands control back to the browser's event loop for a single tick so it
			// can repaint the bar — before continuing to the next page. The node
			// command-line entry point never sets run.onProgress, so this whole block is a
			// no-op there: no report, no yield, no change to the batch conversion path
			// (this is display machinery only, not conversion prep).
			if (run.onProgress) {
				run.onProgress("pages", pageProducts.length, run.pages.length);
				await new Promise((resolve) => setTimeout(resolve, 0));
			}
		}

		// The overview page's title bar (its [TITLE BAR]-tagged content in the Writers
		// Template, holding the English title and, for bilingual modules, the Te Reo
		// Māori title) feeds every lesson page's fallback title.
		const overviewProduct = pageProducts.find((p) => p.page.isOverview) ?? pageProducts[0];
		run.englishTitle = overviewProduct?.content.titleBar.english ?? "";
		run.teReoTitle = overviewProduct?.content.titleBar.teReo ?? "";
		// The overview page is where the BLL "Module N -" title-prefix family gets
		// decided (see the title-bar handling further down this file). Remember that
		// decision on the run itself so every OTHER page in this module — not just
		// the overview — also renders its own title h1 with the same lowercase span.
		run.modulePrefix = overviewProduct?.content.titleBar.modulePrefix === true;

		// "MODULE NAME" METADATA TITLE (the PNR101/102/104 MTK
		// "Te Aka Taumatua" bilingual family). This template has NO [TITLE BAR]
		// payload anywhere (the drop-down-menu table's [TITLE BAR] row is left
		// empty); the module's bilingual title lives in the front-matter metadata
		// table's "Module Name" row instead ("Ngā tau: 1 | Numbers: 1"). When no
		// title was derived at all, pipe-split that value and ship its halves in
		// PAYLOAD ORDER (Te Reo first in the gold — the same positional
		// slot convention the ordinary title splits use; see the CEDW501 note in
		// ContentConverter). This runs BEFORE the Course backup below so a course
		// CODE ("PNR9000") can never become the title.
		// Data: elements.dual_language.dropdown_menu.title_from_module_name +
		// front_matter_metadata.table_row_fields. Env toggle: REODROPMENU_OFF
		// (the metadata capture is also disabled by it, so this never fires).
		{
			const ddCfg = DataService.Data.EmitTemplates.elements?.dual_language?.dropdown_menu;
			const ddOn = ddCfg && ddCfg.enabled !== false && ddCfg.title_from_module_name !== false
				&& !(typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF);
			const modName = run.metadata?.moduleName;
			if (ddOn && modName && !run.englishTitle && !run.teReoTitle) {
				const parts = String(modName).split(/\s*\|\s*/).map((s) => s.trim()).filter(Boolean);
				if (parts.length) {
					run.englishTitle = parts[0];
					run.teReoTitle = parts.slice(1).join(" | ");
					run.AddNote("info", "PageAssembler",
						`No [TITLE BAR] title — using the front-matter "Module Name" metadata "${modName}" as the module title (MTK drop-down-menu template).`);
				}
			}
		}

		// The title typed as a front-matter instruction ("[Insert title H1: What the arts have in common]",
		// ARFUN01 — no [TITLE BAR] anywhere) is the module title when nothing else gave one. Data
		// header.title_split.title_instruction (ModuleResolver captures it); env TITLEINSTR_OFF.
		if (!run.englishTitle && !run.teReoTitle && run.metadata?.titleInstruction
			&& !(typeof process !== "undefined" && process.env && process.env.TITLEINSTR_OFF)) {
			run.englishTitle = run.metadata.titleInstruction;
			run.AddNote("info", "PageAssembler",
				`No [TITLE BAR] title — using the writer's title instruction "${run.metadata.titleInstruction}" from the front matter (title_split.title_instruction).`);
		}

		// English-title BACKUP: the module must never ship with a Te-Reo-only
		// title. When the [TITLE BAR] gave a SINGLE title that does NOT match
		// the front-matter Course (i.e. it's the Te Reo name), promote that
		// lone title to the Te Reo slot and use Course as the English title
		// (front_matter_metadata.course_is_english_title_backup; as in
		// OSAI301, whose payload is only "Kirirarautanga Matihiko AI").
		// The MTK / Te Reo Rangatira title source: the TRR1xx docx leaves its
		// [TITLE BAR] rows empty and has no Module
		// Name row, so both run titles are still empty here. Sources, in order: the first
		// [H1] / [Title Bar] item anywhere whose text carries a pipe (the per-page
		// "TRR102 The vowels: Aa | Ngā Oropuare: Aa" repetition, code stripped, halves in
		// payload order), else the Module Code cell's remainder (metadata.moduleCodeTitle:
		// a pipe, or one spaced dash with a macron on exactly one side, splits it). The
		// skeleton orders the pair Māori-first for these modules (header.mtk_titles).
		{
			const mtk = DataService.Data.EmitTemplates.header?.mtk_titles;
			const mtkOn = mtk && mtk.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[mtk.env ?? "MTKTITLES_OFF"])
				&& new RegExp(mtk.body_class ?? "reoTranslate", "i").test(String(run.resolvedRules?.body_class || ""));
			if (mtkOn && !run.englishTitle && !run.teReoTitle) {
				const code = String(run.moduleCode || "");
				const esc = code.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
				const stripCode = (s) => code ? String(s).replace(new RegExp("^\\s*" + esc + "\\s*[:\\-\u2013\u2014]?\\s*", "i"), "") : String(s);
				const tidy = (s) => String(s ?? "").replace(/\*+/g, "").replace(/^[\s:\-\u2013\u2014|]+|[\s:\-\u2013\u2014|]+$/g, "").replace(/\s+/g, " ").trim();
				let parts = null, src = "";
				const tags = new Set(mtk.repetition_tags ?? ["h1", "title bar"]);
				outer: for (const p of run.pages) {
					for (const it of (p.items ?? [])) {
						if (it.type !== "tag" || !tags.has(it.parse?.primary?.tag)) continue;
						const txt = tidy(stripCode(tidy(it.blackAfter || "")));
						if (!txt.includes("|")) continue;
						const h = txt.split("|").map(tidy).filter(Boolean);
						if (h.length >= 2) { parts = h.slice(0, 2); src = `[${it.parse.primary.tag}] repetition on page ${p.lessonLabel}`; break outer; }
					}
				}
				const cell = tidy(run.metadata?.moduleCodeTitle);
				if (!parts && cell) {
					const M = /[\u0101\u0113\u012b\u014d\u016b\u0100\u0112\u012a\u014c\u016a]/;
					if (cell.includes("|")) parts = cell.split("|").map(tidy).filter(Boolean).slice(0, 2);
					else {
						const d = cell.split(/\s+[\u2013\u2014\-]\s+/);
						parts = (d.length === 2 && (M.test(d[0]) !== M.test(d[1])) && d.every((h) => tidy(h).replace(/[^A-Za-zÀ-ſ]/g, "").length >= 3)) ? d.map(tidy) : [cell];
					}
					src = "the Module Code cell";
				}
				if (parts && parts.length) {
					run.englishTitle = parts[0];
					run.teReoTitle = parts[1] ?? "";
					run.AddNote("info", "PageAssembler",
						`No [TITLE BAR] / Module Name title — MTK module title taken from ${src}: "${parts.join(" | ")}".`);
				}
			}
		}
		const tb = overviewProduct?.content.titleBar;
		const course = run.metadata?.course;
		const titlePhOn = (DataService.Data.EmitTemplates.header.title_split.placeholder_title_rule?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.TITLEPH_OFF);
		if (titlePhOn && course && !run.englishTitle) {
			// Sometimes EVERY half of the [TITLE BAR] tag was left as unreplaced
			// template placeholder text (e.g. the writer never filled in 'MODULE TITLE
			// TE REO') — meaning there is NO real title anywhere in the Writers
			// Template. In that case, fall back to the front-matter Course field as the
			// SINGLE English title and ship NO Te Reo title at all (we only ever show
			// both languages when both are genuinely present in the source document;
			// we never invent the missing one). Env toggle TITLEPH_OFF reverts this
			// whole rule, falling back instead to a narrower check for what
			// counts as "placeholder text".
			// Before the Course, the front matter's own title fields: the Module code
			// value's words after the code, or the Subject under a programme-banner
			// Course (placeholder_title_rule.front_matter_titles; env FMTITLE_OFF).
			const fmt = PageAssembler.#frontMatterTitle(run);
			if (fmt) {
				run.englishTitle = fmt.parts[0];
				run.teReoTitle = fmt.parts[1] ?? "";
				run.AddNote("info", "PageAssembler",
					`[TITLE BAR] held only placeholder text — using the front-matter ${fmt.src} "${fmt.parts.join(" | ")}" as the module title (not the Course "${course}").`);
			} else {
				run.englishTitle = course;
				run.teReoTitle = "";
				run.AddNote("info", "PageAssembler",
					`[TITLE BAR] held only placeholder text — using the front-matter Course "${course}" as the English title; no Te Reo title (the real one is not in the WT).`);
			}
		} else if (tb?.single && course
			// a REAL title left after dropping a placeholder half (mixed bar) is the
			// English title — NOT Te Reo — so don't run the lone-title promotion on it
			&& !(titlePhOn && tb?.droppedPlaceholder)
			// The lone-title → Te Reo promotion below assumes that when the Writers
			// Template's [TITLE BAR] gives just ONE title, and that title differs from
			// the front-matter Course field, the lone title must be the Te Reo name
			// (this rule exists to handle a module like OSAI301, whose only title text
			// is "Kirirarautanga matihiko AI"). That assumption MISFIRES when the lone
			// title is actually the ENGLISH module title and the Course field just
			// happens to hold a broader subject name instead: a WT title of
			// "*KEEPING IT REAL*" with Course "Communication" (ENGC102) would ship
			// <h1>Communication</h1> as the English title (wrong — that's just the
			// subject name) with "Keeping it real" shoved into the Te Reo slot; a
			// Māori Course name ("Te Ara Hou", ENGS302) could even land in the
			// ENGLISH slot. GUARD:
			// only promote the lone title to the Te Reo slot when it is ACTUALLY
			// written in Te Reo Māori (the Māori alphabet never uses the letters
			// b c d f j l q s v x y z; it only uses g/h/k/m/n/p/r/t/w plus vowels +
			// macrons, including the ng/wh digraphs). An English lone title is left as
			// the English title, with no Te Reo title invented out of nothing (the
			// real Te Reo title, if this module has one, simply isn't present anywhere
			// in this WT, so we don't guess at it). OSAI301 is still promoted.
			// Data flag: header.title_split.lone_title_maori_guard; env: LONETITLE_OFF.
			&& this.#loneTitleIsTeReo(run.englishTitle)
			&& Utils.Fold(run.englishTitle).replace(/\s+/g, "")
				!== Utils.Fold(course).replace(/\s+/g, "")) {
			run.teReoTitle = run.englishTitle;   // the lone WT title was Te Reo
			run.englishTitle = course;
			run.AddNote("info", "PageAssembler",
				`[TITLE BAR] held only "${run.teReoTitle}" (no English) — using the front-matter Course "${course}" as the English title; Te Reo kept as the second title.`);
		}
		// the skeleton reads the run-level titles; refresh the overview
		// product's titleBar so the header h1s reflect the backup
		if (overviewProduct) {
			overviewProduct.content.titleBar.english = run.englishTitle;
			overviewProduct.content.titleBar.teReo = run.teReoTitle;
		}

		// ---- [6b] acknowledgements — ALWAYS generated (policy) --------------
		const acksHtml = await AcksBuilder.Build(run);

		// ---- [7]+[8] skeleton wrap + emit -----------------------------------
		const code = run.moduleCode ?? "MODULE";
		// page filenames are deterministic — compute them all first so each
		// page's footer can link to its prev/next siblings (page chaining).
		// Through the shared PageFileNames helper (the library
		// {code}_{lesson}_{part}.html form; env PAGENAME_OFF = the dash form).
		const filenames = PageAssembler.PageFileNames(run);
		// Change Ledger CL-0044 (constraint 71): footer nav
		// hrefs ship EMPTY — prev/next/home alike; D2L wires the real links at
		// publish time. The gold library's hrefs are empty too (the populated
		// few are the publish-time D2L quickLink wiring itself), so this
		// matches both the design-team directive AND the gold. The per-position
		// <li> composition (value_map) is unchanged — only the href fill.
		// Data footer.nav_links_empty.enabled; env FOOTEREMPTY_OFF restores
		// sibling chaining.
		const footerEmpty = (DataService.Data.EmitTemplates.footer?.nav_links_empty?.enabled === true)
			&& !(typeof process !== "undefined" && process.env && process.env.FOOTEREMPTY_OFF);
		pageProducts.forEach(({ page, content }, i) => {
			const html = SkeletonBuilder.BuildPage({
				page, content, run,
				// first page carries the acks block (after #footer);
				// historical last-page placement is superseded — never copy it
				acksHtml: i === 0 ? acksHtml : "",
				isFinal: i === pageProducts.length - 1 && pageProducts.length > 1,
				// CL-0044: hrefs empty by default; FOOTEREMPTY_OFF restores chaining
				prevHref: footerEmpty ? "" : (i > 0 ? filenames[i - 1] : ""),
				nextHref: footerEmpty ? "" : (i < pageProducts.length - 1 ? filenames[i + 1] : ""),
			});
			run.outputs.push({
				filename: filenames[i],
				// tab-indented for hand-editing/debugging, matching the human-developed
				// modules' formatting. Before formatting, two clean-up passes run over
				// the finished page HTML, in this order: OmitPlaceholderResidue strips
				// the left-over debris of an omitted, unfilled template prompt (an empty
				// bullet point plus its internal cv2-omit marker) from anywhere on the
				// page — the menu and the acknowledgements section included, not just
				// the main body. TidyDeveloperNotes then cleans up developer-facing
				// comment notes: it relocates any comment note that ended up inside the
				// module menu out into the body instead, merges ("coalesces") runs of
				// consecutive same-prefix notes into one, and drops bare addressee cues
				// that carry no actual content.
				// THE ORDER MATTERS: OmitPlaceholderResidue must run BEFORE
				// TidyDeveloperNotes, so an already-omitted placeholder prompt can never
				// be accidentally relocated or merged back in by the tidy-up pass.
				// DOMAIN LINK-TEXT DISPLAY (as in the BLL241 supervisor note): a
				// link on a configured domain whose visible text
				// is itself a URL shows the domain's canonical display form
				// ("https://speldsa.org.au") while the href keeps the full deep URL.
				// Applied to the page BEFORE the acknowledgements block only — the
				// human developers keep the FULL URL text in their acknowledgements
				// and canonicalise it in the body.
				// Data: Emit_Templates elements.link_text_display; env LINKTEXT_OFF.
				// NO-EMOJI RULE (Change Ledger CL-0051): after the note
				// tidy and BEFORE the link-text pass, EmojiStrip removes emoji from
				// the rendered writer content (Extended_Pictographic clusters minus
				// the ledger's exempt ticks & crosses; arrows become plain arrows;
				// 2+ consecutive emoji-prefixed lines become a <ul>; ONE red
				// disclosure note per affected page, built through the standard
				// NotesAndComments.redFlag machinery so the note scheme and
				// NOTESCHEME_OFF apply to it like any other note). Applied to the
				// page BEFORE the acknowledgements block only — the acks keep
				// their verbatim oEmbed titles and the converter's own ❗ ack-todo
				// markers. Verbatim zones (cv2-interactive hand-off boxes,
				// cv2-note / cv2-comment quotes) are skipped inside the pass.
				// Data: Input_Doc_Rules.emoji_strip; env EMOJISTRIP_OFF.
				// TYPED-NUMBER RUNS → <ol> (KB constraint 42): after the
				// emoji pass and BEFORE the link-text pass, TypedNumberList turns a
				// run of consecutive plain <p>s whose text opens with sequential typed
				// numbers ("1. …", "2. …") into one semantic <ol> (start="N" when the
				// run does not begin at 1), the typed number stripped. Body only; the
				// same verbatim zones as EmojiStrip plus the built widgets that own
				// their inner shape (flipCard / dragAndDrop / carousel / …).
				// Data: Emit_Templates body_region.typed_number_list; env TYPEDOL_OFF.
				content: HtmlFormatter.Indent(
					(() => {
						// the unfilled Connections sample leaves the page (NotesAndComments.OmitTemplateSample;
						// red_flag.omit_template_sample; env TEMPLATESAMPLE_OFF) — beside the placeholder-residue pass.
						const tidied = NotesAndComments.TidyDeveloperNotes(
							NotesAndComments.OmitTemplateSample(NotesAndComments.OmitPlaceholderResidue(html)));
						// Adjacent sibling lists join into one (body_region.merge_adjacent_lists; env ULMERGE_OFF) — after TypedNumberList, before the link-text pass.
						// A bare list-number paragraph leaves the page (body_region.lone_list_number; env LONENUM_OFF) — after TypedNumberList.
						// An orphan punctuation block merges onto the text before it or leaves (ListsAndRuns.OrphanPunctuation;
						// body_region.orphan_punctuation; env ORPHANPUNCT_OFF) — after the emoji pass, before TypedNumberList.
						// The Writers Template's own hint line («Learning outcome/intentions for the lesson») leaves the page
						// (ListsAndRuns.TemplateHintLine; body_region.template_hint_line; env HINTLINE_OFF) — after OrphanPunctuation.
						// A run of typed «- » lines becomes a <ul> (ListsAndRuns.TypedDashList; body_region.typed_dash_list; env
						// TYPEDUL_OFF) — beside TypedNumberList, before the adjacent-list join.
						const deEmoji = (seg) => ListsAndRuns.MergeAdjacentLists(ListsAndRuns.LoneListNumbers(ListsAndRuns.TypedDashList(ListsAndRuns.TypedNumberList(ListsAndRuns.TemplateHintLine(ListsAndRuns.OrphanPunctuation(ListsAndRuns.EmojiStrip(seg, () =>
							NotesAndComments.redFlag(
								DataService.Data.InputDocRules?.emoji_strip?.disclosure ?? "",
								run, "diagnostic"))))))));
						const ai = tidied.indexOf("<div class=\"acks");
						// KB constraint 92 / CL-0093: every CJK run takes its language-font class
						// (ListsAndRuns.LanguageFontWrap; data body_region.language_fonts; env LANGFONT_OFF) —
						// after the link-text pass, the pre-acks slice only (the gold's acks credits stay bare).
						const langWrap = (seg) => ListsAndRuns.LanguageFontWrap(ListsAndRuns.LinkTextDisplay(seg), run);
						// A level 3–4 Maths module's typed fractions become MathML (ListsAndRuns.TypedFractions;
						// data Input_Doc_Rules.math.typed_fractions; env TYPEDFRAC_OFF) — the pre-acks slice, after every
						// other text pass, before the equation sentinels are swapped.
						const preFrac = ai < 0 ? langWrap(deEmoji(tidied)) : langWrap(deEmoji(tidied.slice(0, ai)));
						const fracd = ListsAndRuns.TypedFractions(preFrac, run);
						const passed = ai < 0 ? fracd : fracd + tidied.slice(ai);
						// The equation sentinels become their MathML LAST, after every
						// text pass (none of them may touch the markup), and a page that now carries a <math>
						// gains the mathJax body class (the gold's per-page form). Data Input_Doc_Rules.math.
						const _mathCfg = DataService.Data.InputDocRules?.math;
						let withMath = DocxExtractor.MathReplace(passed);
						if (_mathCfg && _mathCfg.enabled !== false && (withMath !== passed || fracd !== preFrac) && /<math\b/.test(withMath)) {
							const tok = _mathCfg.body_class_token || "mathJax";
							withMath = withMath.replace(/<body class="([^"]*)"/, (m, cls) =>
								new RegExp("(^|\\s)" + tok + "(\\s|$)").test(cls) ? m : "<body class=\"" + cls + " " + tok + "\"");
						}
						// The superscript / subscript sentinels become <sup> / <sub> (the
						// whole-phrase guard inside); data Input_Doc_Rules.formatting_markers.vert_align; env VERTALIGN_OFF.
						withMath = DocxExtractor.VertReplace(withMath, false, DataService.Data.InputDocRules?.formatting_markers?.vert_align);
						// The writer's in-sentence underline sentinels become <u> (plain inside headings, attributes and the
						// <title>); data Input_Doc_Rules.formatting_markers.underline; env UNDERLINE_OFF (no sentinels are made).
						withMath = DocxExtractor.UnderReplace(withMath, false, DataService.Data.InputDocRules?.formatting_markers?.underline);
						// KB c52: every derivable iStock image alt, LAST (MediaBuilder.FillWidgetAlts;
						// data elements.image_attrs.widget_alt_postpass; env WIDGETALT_OFF).
						return MediaBuilder.FillWidgetAlts(withMath, run);
					})()),
				kind: "page",
			});
		});

		// ---- [8] the interactives manifest -----------------------------------
		// filenames are known now, so manifest entries can point at them
		run.interactives.forEach((b) => {
			const pageIndex = run.pages.indexOf(b.page);
			b.targetFile = run.outputs[pageIndex]?.filename ?? run.outputs[0]?.filename;
		});
		run.outputs.push({
			filename: Utils.FillTemplate(naming.manifest_file, { code }),
			content: DocxExtractor.UnderReplace(DocxExtractor.VertReplace(DocxExtractor.MathReplace(ManifestBuilder.Build(run)), true), true),   // equation sentinels → MathML in the hand-off too; sup / sub and underline sentinels stripped to plain text
			kind: "manifest",
		});

		// ---- the distilled reference template --------------------------------
		// When the person uploaded reference HTML pages at conversion time (see
		// ModuleResolver.PrepareRun's reference-module block), the mined
		// structural profile ships as its own JSON output — the file needed
		// to add that reference module to PageForge's templated modules.
		// Named after the REFERENCE module's code (that's what the file
		// describes), falling back to this module's code when the uploaded
		// pages carried no recognisable code in their filenames.
		if (run.referenceDistilled?.file) {
			const refName = run.referenceDistilled.referenceCode ?? code;
			run.outputs.push({
				filename: `${refName}_reference-template.json`,
				content: JSON.stringify(run.referenceDistilled.file, null, "\t") + "\n",
				kind: "reference-template",
			});
		}
	};

	/**
	 * The module's own title from the front matter, for a [TITLE BAR] that holds only
	 * placeholder text (or nothing). Two fields can carry it: the Module code value's
	 * words after the code token ("ENGC302 Email Me | Īmēra Mai"; a "|" splits English |
	 * Te Reo), and the Subject when the Course is a programme banner (data pattern) rather
	 * than a title. A value with no space, or nothing left after the code, is not a title.
	 * Data header.title_split.placeholder_title_rule.front_matter_titles; env FMTITLE_OFF.
	 *
	 * @param {ConversionRun} run - the run whose metadata holds the front-matter fields
	 * @returns {{parts: string[], src: string}|null} the title halves and their source
	 */
	static #frontMatterTitle(run) {
		const cfg = DataService.Data.EmitTemplates.header?.title_split?.placeholder_title_rule?.front_matter_titles;
		if (!cfg || cfg.enabled === false
			|| (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "FMTITLE_OFF"])) return null;
		const md = run.metadata ?? {};
		const tidy = (s) => String(s ?? "").replace(/\u{1f534}/gu, "").replace(/\*+/g, "").replace(/\s+/g, " ").trim();
		const isTitle = (s) => /\s/.test(s) && /[A-Za-zÀ-ſ]{3}/.test(s);
		if (cfg.module_code_field && md.moduleCode) {
			const rest = tidy(tidy(md.moduleCode).replace(new RegExp(cfg.code_token ?? "^\\s*[A-Za-z]{2,8}\\d{2,5}\\s*"), ""));
			if (isTitle(rest)) {
				const parts = rest.split(/\s*\|\s*/).map(tidy).filter(Boolean).slice(0, 2);
				if (parts.length) return { parts, src: "Module code" };
			}
		}
		if (cfg.subject_when_course && md.subject && new RegExp(cfg.subject_when_course, "i").test(tidy(md.course))) {
			const subj = tidy(md.subject);
			if (isTitle(subj)) return { parts: [subj], src: "Subject" };
		}
		return null;
	}

	/**
	 * Decides whether a LONE [TITLE BAR] title — the Writers Template gave only one
	 * title, with no separate Te Reo half — is written in Te Reo Māori (in which case
	 * the Course-backup logic above should promote it into the Te Reo title slot), or
	 * whether it is actually English (in which case it IS the English title and
	 * should ship alone, with no Te Reo title invented).
	 *
	 * HOW: Te Reo Māori uses only the letters a e h i k m n o p r t u w (plus the
	 * macrons ā ē ī ō ū) and the ng/wh digraphs — it NEVER uses b c d f j l q s v x y
	 * z. So a title containing any of those non-Māori letters must be English.
	 *
	 * WHY THIS GUARD EXISTS: see the caller's comment above for two real modules
	 * (ENGC102, ENGS302) whose English titles were once wrongly promoted into the Te
	 * Reo slot before this check was added.
	 *
	 * @param {string} title - the lone WT title text to classify
	 * @returns {boolean} true when the title should be treated as Te Reo Māori; also
	 *   true when the guard itself is switched off (via the data flag or env
	 *   LONETITLE_OFF), which preserves the original always-promote behavior from
	 *   before this guard existed
	 */
	static #loneTitleIsTeReo(title) {
		const cfg = DataService.Data.EmitTemplates.header?.title_split?.lone_title_maori_guard;
		const on = (cfg?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.LONETITLE_OFF);
		if (!on) return true;                          // guard off → original (always promote)
		const nonMaori = new RegExp(cfg?.non_maori_letters ?? "[bcdfjlqsvxyz]", "i");
		return !nonMaori.test(String(title ?? ""));    // no non-Māori letter → Te Reo
	}
}

// Node module export; browsers ignore it.
if (typeof module !== "undefined") module.exports = { PageAssembler };
