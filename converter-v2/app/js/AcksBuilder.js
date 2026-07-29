/**
 * AcksBuilder.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Pipeline stage [6b] — builds the acknowledgements block from the media
 * list, per the complete spec in Acks_Formats.json (the machine-readable
 * form of 00_Copyright_Acks_Formatting_Rules.md §1–8).
 *
 * THE POLICY (locked 2026-06-12, a non-decision):
 * The block is generated for EVERY module — always. There is deliberately
 * NO conditional logic around whether to emit it. A module with zero
 * external media still gets the standing items. Placement (PageAssembler):
 * bottom of the very FIRST page, div.acks AFTER #footer.
 *
 * SOURCING HONESTY (the ACK-TODO contract):
 * Anything the writer docs + the verified derivations (iStock URL slug,
 * YouTube oEmbed) cannot fill becomes a VISIBLE one-line ❗ ackTodo entry
 * with a machine-readable comment beside it — never an HTML-comment-only
 * flag, never a silent omission, never a guessed field.
 *
 * LESSON MAPPING (Input_Doc_Rules.media_item_lesson_mapping):
 * Strongest evidence first — 1 content match (the item's URL/asset id
 * appears in a lesson's content), 2 WT page records when trustworthy,
 * 3 neighbour interpolation (media lists run in page order), 4 fallback
 * to the first group. Every interpolated/fallback placement is surfaced
 * in the conversion summary.
 * ===========================================================================
 */

class AcksBuilder {

	/**
	 * Builds the complete acknowledgements block HTML for one conversion run.
	 *
	 * WHAT: turns run.mediaItems (every row of the parsed Media List) into
	 * the finished acks block — one acknowledgement (or ACK-TODO) per item,
	 * grouped under its lesson, wrapped in the fixed set of standing items
	 * (opening disclaimer, optional AI-usage statement, catch-all line, full
	 * copyright statement) the spec always requires. See the file header
	 * above for the policy (always generated, never conditional) and the
	 * ACK-TODO contract (surface a gap, never guess).
	 *
	 * HOW (three steps, each commented inline below):
	 *  1. resolve each media item into an entry (or null) via #buildEntry,
	 *     awaited one at a time (see #sleep) so YouTube oEmbed calls go out
	 *     throttled rather than all at once;
	 *  2. map the built entries to lesson groups via #groupByLesson;
	 *  3. assemble the final HTML string in the spec's fixed group order.
	 *
	 * @param {ConversionRun} run - the run: run.mediaItems (input),
	 *   run.pages (for lesson grouping), run.AddNote / run.CountAckTodo
	 *   (surfacing + tallying, per the run's surfacing contract)
	 * @returns {Promise<string>} the acks block's HTML, ready for
	 *   PageAssembler to place at the bottom of the module's first page
	 */
	static async Build(run) {
		const fmt = DataService.Data.AcksFormats;

		// ---- 1. resolve each media item into an entry (async: oEmbed) ----
		// MapSeries + throttle keeps the unauthenticated oEmbed endpoint
		// happy (rate-limit friendliness, standards §7c)
		const entries = await Utils.MapSeries(run.mediaItems, async (item, index, total) => {
			const entry = await this.#buildEntry(item, run);
			if (run.mediaItems.length > 1) await this.#sleep(fmt.oembed.throttle_ms);
			// Browser-only progress reporting. Fetching each YouTube item's
			// metadata over the network (oEmbed, in #youtubeEntry below) plus
			// the deliberate throttle pause between items (#sleep) — being a
			// good citizen of the free, unauthenticated oEmbed endpoint —
			// makes this acks walk the naturally slowest phase of a real
			// browser conversion, so this is where progress gets reported.
			// Guarded: the command-line/batch test harness never sets
			// run.onProgress (see ConversionRun.js), so this call is a
			// no-op there — it can never change the batch tool's output.
			if (run.onProgress) run.onProgress("acks", index + 1, total);
			return entry;
		});

		// ---- 2. map items to lesson groups --------------------------------
		const groups = this.#groupByLesson(entries.filter(Boolean), run);

		// ---- 3. assemble the block ----------------------------------------
		const hasAi = entries.some((e) => e?.sourceClass === "ai");
		const g = fmt.lesson_groups;
		const html = [];

		html.push(Utils.FillTemplate(fmt.container.wrapper_open, {
			acksClass: hasAi ? fmt.container.acks_class_ai_variant : fmt.container.acks_class_standard,
		}));

		// opening disclaimer (its own group, per the corpus form)
		html.push(g.group_element_open, fmt.standing_items.opening_disclaimer);
		if (hasAi) html.push(fmt.standing_items.ai_usage_statement);   // §5.1 position
		// ROUND 236 (Chris) — the unverified-iStock designer note closes the
		// opening group, which puts it at the top of the acks block and
		// directly above the ❗ lesson groups it explains. Empty string (and so
		// no output at all) whenever every iStock title was verified.
		const unverifiedNote = this.#unverifiedNote(run);
		if (unverifiedNote) html.push(unverifiedNote);
		html.push(g.group_element_close);

		// per-lesson groups, in page order — every lesson gets its group,
		// each opened with the spec-mandated lesson-label comment and
		// closed with the designer-media check line (§8: once per group)
		for (const group of groups) {
			html.push(g.group_element_open);
			html.push(Utils.FillTemplate(g.group_label_comment, { lesson: group.label }));
			// DE-DUPLICATE within the lesson group: writers often paste the SAME media
			// (URL/iStock id) across a lesson's activities and each becomes a media-list
			// row → an entry. The human acknowledges a given asset ONCE per lesson (e.g.
			// XGF9001 page 0 had iStock 1957478548 acknowledged 13×). Skip an entry whose
			// exact ack line already appeared in THIS group (an asset legitimately
			// re-appears in OTHER lessons, so dedup is per-group, not global).
			const seenLines = new Set();
			for (const e of group.entries) {
				const key = String(e.html ?? "").replace(/\s+/g, " ").trim();
				if (key && seenLines.has(key)) continue;
				if (key) seenLines.add(key);
				if (e.todoComment) html.push(e.todoComment);
				html.push(e.html);
			}
			html.push(g.group_element_close);
		}

		// catch-all + full copyright statement (fixed closing positions)
		html.push(g.group_element_open, fmt.standing_items.catch_all, g.group_element_close);
		html.push(g.group_element_open, fmt.standing_items.copyright_statement, g.group_element_close);

		html.push(fmt.container.wrapper_close);
		return html.join("\n");
	};

	// =======================================================================
	// ENTRY BUILDING (one media item → one entry / ACK-TODO)
	// =======================================================================
	// Every method in this section takes ONE media-list `item` (a row parsed
	// from the Media List .docx by MediaListParser.ParseItems) and returns
	// ONE `entry` object (or null). Documented once here so the methods
	// below can just say "returns an entry" instead of re-deriving the
	// shape every time:
	//
	// item (input) — one row of the Media List table, e.g.:
	//   { itemNo: "3", wtPage: 13, itemType: "video",
	//     description: "Being a school principal in the 80's vs today",
	//     source: "Youtube", url: "https://www.youtube.com/watch?v=…",
	//     ecr: "", rowIndex: 4 }
	//   (this file only ever reads itemNo/itemType/description/source/url/
	//   wtPage off it — ecr/rowIndex are MediaListParser's own bookkeeping)
	//
	// entry (output) — what #plain / #todo / every #...Entry method below
	// returns, and what #buildEntry ultimately hands back to Build(), e.g.:
	//   { html: "<p>Image: Two Kids Playing Soccer On Field. iStock photo
	//            ID: 1234567890.</p>",
	//     todoComment: null,       // or an "<!-- ACK-TODO[type] ... -->" string
	//     sourceClass: "istock",   // which branch built this ("todo" for an ACK-TODO)
	//     item }                   // the original item, carried through to #groupByLesson
	//   #buildEntry can also return null outright — meaning NO acknowledgement
	//   is needed at all (a lesson link, or a Te Kura item already covered by
	//   the standing catch-all line). That is different from an ACK-TODO:
	//   null means "nothing to say here", an ACK-TODO means "something is
	//   missing and a human needs to fill it in" — see the file header's
	//   ACK-TODO contract.

	/**
	 * Builds one acknowledgement entry from a media item — the per-item
	 * dispatcher that Build() calls once for each row of the Media List.
	 *
	 * HOW: classifies the item's source (#classify), then routes to the
	 * matching source-specific builder below (#istockEntry, #youtubeEntry,
	 * #pixabayEntry, #wikiEntry, #websiteEntry, or an inline template for
	 * twinkl/heygen/ai/other_stock) via the switch. Any source with no
	 * dedicated branch falls through to #websiteEntry, the generic
	 * "writer's own description + link" form. After the switch, one
	 * consistency check runs so every kind of "not enough information"
	 * line ends up visibly flagged the same way (see the "UNKNOWN ITEM
	 * TYPE" comment further down in this method).
	 *
	 * @param {Object} item - one Media List row (see the shape note above)
	 * @param {ConversionRun} run - the run (for AddNote / CountAckTodo)
	 * @returns {Promise<Object|null>} an entry (see the shape note above),
	 *   or null when NO acknowledgement is needed at all — a lesson link,
	 *   or a Te Kura-owned item already covered by the standing catch-all
	 *   line (both are scope rules from Acks_Formats.json, not something
	 *   missing)
	 */
	static async #buildEntry(item, run) {
		const fmt = DataService.Data.AcksFormats;
		const sourceClass = this.#classify(item);

		// scope rule §1: lesson links don't get acknowledgements
		if (sourceClass === "skip") {
			run.AddNote("info", "AcksBuilder",
				`Media item ${item.itemNo} ("${item.itemType}") is a lesson link — no acknowledgement (scope rule).`);
			return null;
		}
		// Te Kura items are covered by the standing catch-all line
		if (sourceClass === "tekura") return null;

		const prefix = this.#typePrefix(item, run);
		const adapted = fmt.entry_templates.adapted_keywords.some((k) =>
			Utils.Fold(`${item.description} ${item.itemType}`).includes(k))
			? fmt.entry_templates.adapted_token : "";

		let entry;
		switch (sourceClass) {
			case "istock":   entry = this.#istockEntry(item, prefix, adapted, run); break;
			case "youtube":  entry = await this.#youtubeEntry(item, run); break;
			case "pixabay":  entry = this.#pixabayEntry(item, prefix, run); break;
			case "wikicommons": entry = this.#wikiEntry(item, prefix, run); break;
			case "twinkl":
				entry = this.#plain(Utils.FillTemplate(fmt.entry_templates.twinkl, {
					Title: item.description, URL: item.url,
				}), sourceClass, item); break;
			case "heygen":
				entry = this.#plain(fmt.entry_templates.heygen, sourceClass, item); break;
			case "ai":
				entry = this.#plain(Utils.FillTemplate(fmt.entry_templates.ai_copilot, {
					Description: item.description,
				}), sourceClass, item); break;
			case "other_stock": {
				// same shape as iStock with the library named (§3.4)
				const id = item.url.match(/(\d{6,12})/)?.[1]
					?? item.description.match(/\b(\d{8,10})\b/)?.[1] ?? "";
				if (!id) { entry = this.#todo(item, "asset-id", { title: item.description }, run); break; }
				entry = this.#plain(Utils.FillTemplate(fmt.entry_templates.other_stock, {
					TypePrefix: prefix, Title: item.description, AssetId: id,
					LibraryName: item.source || "Shutterstock Images LLC", Adapted: adapted,
				}), sourceClass, item); break;
			}
			default:         entry = this.#websiteEntry(item, prefix, run);
		}

		// UNKNOWN ITEM TYPE → visible ❗ flag.
		// The bug this guards against: a writer's item type that isn't in
		// type_prefix_map (see #typePrefix below) falls back to a
		// Title-cased guess of the type string itself ("jpg"→"Jpg",
		// "text"→"Text") and only logs a background summary note — so the
		// finished line LOOKED complete (it read fine, no ❗) even though
		// "Jpg" is not a real acknowledgement prefix and information is
		// genuinely missing. That was inconsistent with every other
		// "not enough information" case (e.g. the video-meta ACK-TODO
		// built a few lines above, in the "youtube" branch of the switch),
		// which DOES show a visible ❗. The fix: re-emit the already-built
		// line as a visible ❗ ackTodo (via #todoFromEntry) so every
		// incomplete-information case flags the same way. Entries that are
		// ALREADY a TODO (asset-id/licence/video-meta, sourceClass "todo")
		// keep their own ❗ and are left alone here; skip/tekura items
		// already returned above and never reach this check. Data flag
		// ack_todo.flag_unknown_type; env ACKUNKNOWN_OFF reverts to the
		// silent-note (pre-fix) behaviour, for A/B comparison.
		if (entry && entry.sourceClass !== "todo" && this.#isUnknownType(item)
			&& fmt.ack_todo.flag_unknown_type
			&& !(typeof process !== "undefined" && process.env && process.env.ACKUNKNOWN_OFF)) {
			return this.#todoFromEntry(item, entry, run);
		}
		return entry;
	};

	/**
	 * Builds an iStock acknowledgement.
	 *
	 * WHAT: extracts the iStock asset id and, when present, a title slug
	 * from the item's URL (e.g. ".../two-kids-playing-soccer-gm1234567890-…"
	 * → id "1234567890", slug "two-kids-playing-soccer").
	 *
	 * WHY THE TITLE COMES FROM THE URL, NOT THE WRITER'S DESCRIPTION:
	 * the URL slug is iStock's own official image title (verified 98%
	 * accurate against the real corpus, per Acks_Formats.json's
	 * istock_slug_title rule) — the writer's free-text description in the
	 * Media List is not reliable enough to acknowledge by, so it is never
	 * used here even when it is present.
	 *
	 * @param {Object} item - a Media List row (see the shape note above)
	 * @param {string} prefix - the type prefix ("Image", "Video", …) from #typePrefix
	 * @param {string} adapted - the "(image adapted)"-style suffix token, or ""
	 * @param {ConversionRun} run - the run (for #todo's tallying)
	 * @returns {Object} an entry (see the shape note above) — a real
	 *   acknowledgement when both id and slug are found, an ACK-TODO
	 *   ("istock-name") when only the id is found, or an ACK-TODO
	 *   ("asset-id") when neither is found
	 */
	/**
	 * Parses the optional VERIFIED iStock acknowledgements file (ROUND 235,
	 * Chris — CL-0002 adopted into the input contract). The file
	 * (*_istock-acks.txt) holds one fully-formed acknowledgement per line —
	 *   <p>Photo: Friends dancing in the street, iStock 1422643105, Getty
	 *   Images. Used with permission.</p>
	 * — sourced from the iStock API via Getty Images, so its titles are
	 * DEFINITELY correct and outrank the URL-slug derivation (#istockEntry
	 * consults the map first). Titles may themselves contain commas/periods:
	 * the line pattern captures everything between the first ": " and the
	 * LAST ", iStock <id>," greedily, which handles that correctly.
	 *
	 * Called from ModuleResolver.PrepareRun (the ONE shared prep sequence, so
	 * the browser app and the batch harness behave identically — entry parity).
	 *
	 * Data flag: Acks_Formats.istock_acks_file (enabled / line_pattern)
	 * Env toggle: ISTOCKACKS_OFF (ignore the file entirely)
	 *
	 * @param {string|null} text - the raw file text, or null when not supplied
	 * @param {ConversionRun} run - for the loaded-count summary note
	 * @returns {Map<string,{title:string,line:string}>|null} asset id → entry,
	 *   or null when there is no file / no parseable line / the feature is off
	 */
	static ParseIstockAcks(text, run) {
		const cfg = DataService.Data.AcksFormats.istock_acks_file ?? {};
		if (cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.ISTOCKACKS_OFF) return null;
		if (!text) return null;
		const lineRe = new RegExp(cfg.line_pattern ?? "^(?:<p>)?\\s*[^:<>]{1,40}:\\s*(.*),\\s*iStock\\s+(\\d{5,12})\\s*,", "i");
		const map = new Map();
		let unparsed = 0;
		for (const raw of String(text).split(/\r?\n/)) {
			const line = raw.trim();
			if (!line) continue;
			const m = line.match(lineRe);
			if (m) map.set(m[2], { title: m[1].trim(), line });
			else unparsed++;
		}
		if (run && (map.size || unparsed)) {
			run.AddNote(unparsed ? "warn" : "info", "AcksBuilder",
				`_istock-acks.txt: ${map.size} verified iStock title${map.size === 1 ? "" : "s"} loaded`
				+ (unparsed ? ` (${unparsed} line${unparsed === 1 ? "" : "s"} not in the expected "<p>Prefix: Title, iStock ID, …" form — ignored)` : "")
				+ `; these API-sourced titles override slug-derived titles.`);
		}
		// ROUND 236 — record that a file WAS supplied, independently of whether it
		// parsed to anything. #unverifiedNote needs the distinction: "no file at
		// all" and "a file that simply does not cover this asset" are different
		// messages to the designer.
		if (run) run.istockAcksSupplied = !!String(text ?? "").trim();
		return map.size ? map : null;
	};

	/**
	 * ROUND 236 (Chris) — CONTENT-FIRST recognition of the verified iStock
	 * acknowledgements file.
	 *
	 * WHY: round 235 keyed acceptance on the FILENAME (`*istock-acks.txt`).
	 * Chris is moving to per-module names (`_istock-acks-OSAI501.txt`,
	 * `_OSAI501-istock-acks.txt`) while a large number of files already exist
	 * under the old name, so no filename rule can cover the family. His rule
	 * instead: whatever it is called, if it is a .txt holding a list of iStock
	 * acknowledgement lines AND NOTHING ELSE, that is the file — and its titles
	 * are top priority.
	 *
	 * WHAT: tests text against the same `line_pattern` the parser uses, and
	 * qualifies it on TWO thresholds from data — enough matching lines
	 * (`min_matching_lines`, so a passing mention cannot qualify) and a high
	 * enough share of the non-empty lines (`min_share_of_nonempty`, Chris's
	 * "and nothing else"). Blank lines are ignored entirely.
	 *
	 * @param {string} text - the candidate file's contents
	 * @returns {{ok: boolean, matched: number, nonEmpty: number, share: number}}
	 */
	static LooksLikeIstockAcks(text) {
		const cfg = DataService.Data.AcksFormats.istock_acks_file ?? {};
		const det = cfg.detect ?? {};
		const lineRe = new RegExp(cfg.line_pattern, "i");
		let matched = 0, nonEmpty = 0;
		for (const raw of String(text ?? "").split(/\r?\n/)) {
			const line = raw.trim();
			if (!line) continue;
			nonEmpty++;
			if (lineRe.test(line)) matched++;
		}
		const share = nonEmpty ? matched / nonEmpty : 0;
		const ok = matched >= (det.min_matching_lines ?? 3)
			&& share >= (det.min_share_of_nonempty ?? 0.8);
		return { ok, matched, nonEmpty, share: Math.round(share * 1000) / 1000 };
	};

	/**
	 * ROUND 236 — picks the acks file out of a set of candidate .txt files.
	 *
	 * THE ONE CHOKE POINT both entries use (the round-185 entry-parity
	 * discipline): the browser's upload drop and the batch harness's folder
	 * scan hand their candidates here rather than each applying their own rule,
	 * so the two paths can never drift on what counts as an acks file.
	 *
	 * Content decides. The filename is a SECONDARY safeguard only: an
	 * "istock"/"acks" word raises confidence and breaks a tie between two
	 * qualifying files, and a module code that contradicts the module being
	 * converted raises a loud warning (Chris's decision 2026-07-29 — use the
	 * file, because content is the authority, but say so clearly).
	 *
	 * @param {Array<{name: string, text: string}>} candidates
	 * @param {ConversionRun} [run] - for the mismatch/selection notes
	 * @returns {{name: string, text: string}|null}
	 */
	static PickIstockAcks(candidates, run = null) {
		const cfg = DataService.Data.AcksFormats.istock_acks_file ?? {};
		const det = cfg.detect ?? {};
		const legacyOnly = det.enabled === false
			|| (typeof process !== "undefined" && process.env && process.env.ISTOCKDETECT_OFF);

		// ROUND 235 behaviour, preserved verbatim behind the toggle: filename only.
		if (legacyOnly) {
			const nameRe = new RegExp(cfg.filename_pattern ?? "istock-acks\\.txt$", "i");
			return (candidates ?? []).find((c) => nameRe.test(c.name)) ?? null;
		}

		const hints = det.filename_hint_words ?? [];
		const scored = [];
		for (const c of candidates ?? []) {
			const verdict = this.LooksLikeIstockAcks(c.text);
			if (!verdict.ok) continue;
			const lower = String(c.name).toLowerCase();
			const hintScore = hints.filter((w) => lower.includes(w)).length;
			scored.push({ c, verdict, hintScore });
		}
		if (!scored.length) return null;

		// most matching lines wins; filename hints break a tie (the safeguard)
		scored.sort((a, b) => (b.verdict.matched - a.verdict.matched)
			|| (b.hintScore - a.hintScore));
		const best = scored[0];

		if (run) {
			if (scored.length > 1) {
				run.AddNote("warn", "AcksBuilder",
					`${scored.length} uploaded .txt files look like iStock acknowledgements; using `
					+ `"${best.c.name}" (${best.verdict.matched} entries — the most, `
					+ `${best.hintScore ? "and its name carries an iStock/acks hint" : "no filename hint available"}).`);
			}
			if (!best.hintScore) {
				run.AddNote("info", "AcksBuilder",
					`"${best.c.name}" was accepted as the verified iStock acknowledgements file on its `
					+ `CONTENTS (${best.verdict.matched} of ${best.verdict.nonEmpty} lines are iStock `
					+ `acknowledgements); its filename carries no "istock"/"acks" hint.`);
			}
			// filename module code vs the module actually being converted
			const codeRe = det.module_code_pattern ? new RegExp(det.module_code_pattern) : null;
			const named = codeRe ? String(best.c.name).toUpperCase().match(codeRe)?.[1] : null;
			if (named && run.moduleCode && named !== String(run.moduleCode).toUpperCase()) {
				run.AddNote("warn", "AcksBuilder",
					`⚠ "${best.c.name}" names module ${named}, but this conversion is ${run.moduleCode}. `
					+ `Its titles ARE being used (the file's contents are valid iStock acknowledgements) — `
					+ `check you uploaded the right module's file.`);
			}
		}
		return best.c;
	};

	static #istockEntry(item, prefix, adapted, run) {
		const fmt = DataService.Data.AcksFormats;
		const rx = fmt.extraction_regexes;

		// decode %-escapes first: writers paste URLs whose slugs carry
		// encoded dashes/quotes (%E2%80%93 …) that would break the
		// [a-z0-9-]+ slug run; folding then strips any leftover diacritics
		let cleanUrl = item.url;
		try { cleanUrl = decodeURIComponent(item.url); } catch { /* keep raw on bad escapes */ }
		cleanUrl = Utils.Fold(cleanUrl).replace(/\s+/g, "-");

		const id = cleanUrl.match(new RegExp(rx.istock_id_from_url))?.[1]
			?? `${item.description} ${item.itemNo}`.match(new RegExp(rx.istock_id_in_text, "i"))?.[1]
			?? cleanUrl.match(/\b(\d{8,10})\b/)?.[1]
			?? null;

		// ROUND 235 (Chris) — the VERIFIED title from the uploaded
		// *_istock-acks.txt outranks everything else: it is the iStock API's own
		// title for this exact asset id (definitely correct), so when the map
		// carries the id, fill the normal entry template with it — which, for a
		// photo, reproduces the file's own line exactly. Ids not in the file fall
		// through to the slug rule / ACK-TODO below unchanged.
		const verified = id ? run.istockAcks?.get(id) : null;
		if (verified) {
			return this.#plain(Utils.FillTemplate(fmt.entry_templates.istock, {
				TypePrefix: prefix, Title: verified.title, AssetId: id, Adapted: adapted,
			}), "istock", item);
		}

		// the slug IS the official title (verified rule) — only a bare id
		// with no URL needs manual sourcing
		const slug = cleanUrl.match(new RegExp(rx.istock_slug_from_url))?.[1] ?? null;
		if (slug) {
			const st = fmt.istock_slug_title;
			const title = Utils.TitleCaseWords(slug.split("-").filter(Boolean),
				st.special_tokens, st.lowercase_small_words);
			// ROUND 236 — the line is COMPLETE but its title is DERIVED, not
			// confirmed against the iStock API. #unverifiedEntry marks it so the
			// designer can see which titles still need checking; when the acks
			// file covered this id we never reach here (the verified branch above
			// returned already), so reaching this line IS the unverified case.
			return this.#unverifiedEntry(Utils.FillTemplate(fmt.entry_templates.istock, {
				TypePrefix: prefix, Title: title, AssetId: id ?? "", Adapted: adapted,
			}), id, "url-slug", item, run);
		}
		if (id) {
			// id known, no slug → ACK-TODO[istock-name] with the writer's
			// description carried for the developer's reference
			return this.#todo(item, "istock-name", { id, "writer-desc": item.description }, run,
				Utils.FillTemplate(fmt.entry_templates.istock, {
					TypePrefix: prefix, Title: "[OFFICIAL ISTOCK TITLE REQUIRED]",
					AssetId: id, Adapted: adapted,
				}));
		}
		// neither id nor slug → asset-id TODO
		return this.#todo(item, "asset-id", { title: item.description }, run);
	};

	/**
	 * Builds a YouTube acknowledgement.
	 *
	 * WHAT: pulls the video id out of the URL, then asks oEmbed (a web
	 * standard YouTube supports for fetching a resource's title/author from
	 * its URL alone — see DataService.FetchOembed) for the video's real
	 * title and channel name, so the writer never has to type them in by
	 * hand. An item type of "screenshot" (a screenshot OF a video, not the
	 * video itself) gets its own template wording
	 * (entry_templates.youtube_screenshot) instead of the normal
	 * embedded-video wording.
	 *
	 * WHY A TODO, NOT A GUESS, WHEN OEMBED FAILS: a failed fetch could mean
	 * a private/deleted video, a network hiccup, or a malformed URL — any
	 * of those needs a human to look at the actual link, so the run also
	 * logs a "possible dead link worth checking" warning note alongside the
	 * ACK-TODO rather than silently falling back to writer-typed text.
	 *
	 * @param {Object} item - a Media List row (see the shape note above)
	 * @param {ConversionRun} run - the run (for AddNote / #todo's tallying)
	 * @returns {Promise<Object>} an entry (see the shape note above) — a
	 *   real acknowledgement when the video id parses AND oEmbed succeeds,
	 *   else an ACK-TODO ("video-meta")
	 */
	static async #youtubeEntry(item, run) {
		const fmt = DataService.Data.AcksFormats;
		const videoId = item.url.match(new RegExp(fmt.extraction_regexes.youtube_id))?.[1];

		if (!videoId) return this.#todo(item, "video-meta", { url: item.url, reason: "error" }, run);

		const meta = await DataService.FetchOembed(item.url, videoId);
		if (!meta.ok) {
			run.AddNote("warn", "AcksBuilder",
				`YouTube metadata unavailable for item ${item.itemNo} (${meta.reason}) — possible dead link worth checking: ${item.url}`);
			return this.#todo(item, "video-meta", { url: item.url, reason: meta.reason }, run);
		}

		const isScreenshot = Utils.Fold(item.itemType).includes("screenshot");
		const template = isScreenshot ? fmt.entry_templates.youtube_screenshot : fmt.entry_templates.youtube;
		return this.#plain(Utils.FillTemplate(template, {
			Title: meta.title, Channel: meta.channel, URL: item.url,
			RetrievedDate: Utils.TodayStamp(),   // the program's own fetch date
		}), "youtube", item);
	};

	/**
	 * Builds a Pixabay acknowledgement.
	 *
	 * WHAT: Pixabay images are released CC0 (no attribution legally
	 * required, but the corpus still credits them per §3.11 of the acks
	 * spec) and use the asset-number form, keyed by the digit run at the
	 * end of the URL. Pixabay AUDIO uses a different, simpler linked
	 * template (no asset number needed) — detected from the item's own
	 * type text containing "audio" or "music".
	 *
	 * @param {Object} item - a Media List row (see the shape note above)
	 * @param {string} prefix - the type prefix ("Image", "Video", …) from #typePrefix
	 * @param {ConversionRun} run - the run (for #todo's tallying)
	 * @returns {Object} an entry (see the shape note above) — a real
	 *   acknowledgement, or an ACK-TODO ("asset-id") when an image URL has
	 *   no extractable asset number
	 */
	static #pixabayEntry(item, prefix, run) {
		const fmt = DataService.Data.AcksFormats;
		const isAudio = Utils.Fold(item.itemType).includes("audio")
			|| Utils.Fold(item.itemType).includes("music");
		if (isAudio) {
			return this.#plain(Utils.FillTemplate(fmt.entry_templates.pixabay_audio, {
				Title: item.description, Creator: item.source || "Pixabay", URL: item.url,
			}), "pixabay", item);
		}
		// asset number: the digit run in the pixabay URL slug
		const id = item.url.match(/(\d{5,9})\/?$/)?.[1] ?? item.url.match(/(\d{5,9})/)?.[1] ?? "";
		if (!id) return this.#todo(item, "asset-id", { title: item.description }, run);
		return this.#plain(Utils.FillTemplate(fmt.entry_templates.pixabay_image, {
			TypePrefix: prefix, Title: item.description, AssetId: id,
		}), "pixabay", item);
	};

	/**
	 * Builds a Wikimedia Commons acknowledgement.
	 *
	 * WHY A TODO WHEN THE LICENCE IS MISSING: Wikimedia Commons media is
	 * released under a variety of named Creative Commons licences (CC BY,
	 * CC BY-SA 4.0, public domain, …), and the exact licence name is a
	 * legal detail that must be the REAL one from the source page — never
	 * a guessed default like "Attribution 2.0". The licence name is only
	 * available here when the writer happened to type it into the Media
	 * List description as "creative commons <name> licence"; when that
	 * phrase isn't present, this surfaces a visible ACK-TODO instead of
	 * guessing.
	 *
	 * @param {Object} item - a Media List row (see the shape note above)
	 * @param {string} prefix - the type prefix ("Image", "Video", …) from #typePrefix
	 * @param {ConversionRun} run - the run (for #todo's tallying)
	 * @returns {Object} an entry (see the shape note above) — a real
	 *   acknowledgement when a licence name was found in the description,
	 *   else an ACK-TODO ("licence")
	 */
	static #wikiEntry(item, prefix, run) {
		const fmt = DataService.Data.AcksFormats;
		// the licence name is rarely in writer docs — when absent it is a
		// visible TODO, never a guessed "Attribution 2.0"
		const licence = item.description.match(/creative commons ([\w .-]+?) licence/i)?.[1] ?? null;
		if (!licence) {
			return this.#todo(item, "licence", { url: item.url }, run,
				Utils.FillTemplate(fmt.entry_templates.wiki_commons, {
					TypePrefix: prefix, Title: item.description, Author: item.source || "",
					URL: item.url, LicenceName: "[LICENCE NAME REQUIRED]",
				}));
		}
		return this.#plain(Utils.FillTemplate(fmt.entry_templates.wiki_commons, {
			TypePrefix: prefix, Title: item.description, Author: item.source || "",
			URL: item.url, LicenceName: licence,
		}), "wikicommons", item);
	};

	/**
	 * Builds a generic "other website" acknowledgement — the fallback
	 * branch for any source that doesn't match one of the named
	 * classifications handled above (istock / youtube / pixabay /
	 * wikicommons / twinkl / heygen / ai / other_stock).
	 *
	 * WHY THE WRITER'S DESCRIPTION IS TRUSTED HERE, UNLIKE iStock: there is
	 * no verified derivation available for an arbitrary website (no slug
	 * rule, no oEmbed), so the writer's own Media List description is the
	 * best available title and is used as-is, inside a "website
	 * permission" template that also credits the source and links the URL.
	 *
	 * @param {Object} item - a Media List row (see the shape note above)
	 * @param {string} prefix - the type prefix ("Image", "Video", …) from #typePrefix
	 * @param {ConversionRun} run - the run (for #todo's tallying)
	 * @returns {Object} an entry (see the shape note above) — a real
	 *   acknowledgement when the item has a URL, else an ACK-TODO
	 *   ("asset-id") for a named asset with no link at all
	 */
	static #websiteEntry(item, prefix, run) {
		const fmt = DataService.Data.AcksFormats;
		if (!item.url) {
			// a named asset with no link at all → asset-id TODO
			return this.#todo(item, "asset-id", { title: item.description }, run);
		}
		return this.#plain(Utils.FillTemplate(fmt.entry_templates.website_permission, {
			TypePrefix: prefix, Title: item.description, Source: item.source || "", URL: item.url,
		}), "website", item);
	};

	// ---- entry plumbing ----------------------------------------------------

	/**
	 * Wraps a finished line of acknowledgement text as the spec's
	 * one-<p>-per-ack element (lesson_groups.entry_element in
	 * Acks_Formats.json) and packages it into the shared entry shape (see
	 * the note at the top of the ENTRY BUILDING section above). Every
	 * source-specific builder above (#istockEntry, #youtubeEntry, …) calls
	 * this once it has a finished, human-readable line ready to ship.
	 *
	 * @param {string} text - the finished acknowledgement line (already
	 *   filled in from its template — title, URL, etc.)
	 * @param {string} sourceClass - which classification built this
	 *   ("istock", "youtube", "pixabay", "wikicommons", "website", …)
	 * @param {Object} item - the Media List row this entry came from
	 * @returns {Object} an entry with todoComment always null — #plain is
	 *   only ever used for a COMPLETE acknowledgement, never an ACK-TODO
	 *   (building an ACK-TODO is #todo's job)
	 */
	static #plain(text, sourceClass, item) {
		const entry = DataService.Data.AcksFormats.lesson_groups.entry_element;
		return { html: Utils.FillTemplate(entry, { entry: text }), todoComment: null, sourceClass, item };
	};

	/**
	 * ROUND 236 (Chris) — a COMPLETE iStock acknowledgement whose TITLE was
	 * derived rather than verified.
	 *
	 * The third state of the ACK-TODO contract. An ACK-TODO says "information
	 * is missing" and ships a bracketed slot; this line is not missing anything
	 * — it reads exactly like a finished acknowledgement — but its title came
	 * from the image URL's slug instead of the iStock API, and nothing on the
	 * page told the designer which was which. It now carries the ❗ marker, and
	 * #unverifiedNote puts one red explanation at the top of the acks block.
	 *
	 * DELIBERATELY NOT the ackTodo class: keeping it a plain <p> (identical in
	 * structure to the human's own acknowledgement, differing only by the
	 * marker character) means the PRIMARY skeleton gate — which reads class
	 * names but strips text — sees no change at all, and compare_structure
	 * still harvests the line's text as a real acknowledgement rather than
	 * discarding it as a to-do. The visible marker and the machine-readable
	 * comment carry the signal instead.
	 *
	 * @param {string} text - the finished acknowledgement line
	 * @param {string|null} id - the iStock asset id, when known
	 * @param {string} source - where the title came from ("url-slug")
	 * @param {object} item - the media item (carried on the entry as usual)
	 * @param {ConversionRun} run - records the id for #unverifiedNote
	 */
	static #unverifiedEntry(text, id, source, item, run) {
		const cfg = DataService.Data.AcksFormats.istock_unverified ?? {};
		const off = cfg.enabled === false
			|| (typeof process !== "undefined" && process.env && process.env.ISTOCKUNVERIFIED_OFF);
		if (off) return this.#plain(text, "istock", item);

		if (run) (run.istockUnverified ??= []).push(id ?? "(no id)");
		const entry = this.#plain((cfg.marker ?? "❗ ") + text, "istock", item);
		entry.todoComment = Utils.FillTemplate(cfg.todo_comment ?? "", {
			id: id ?? "", source,
		});
		entry.unverified = true;
		return entry;
	};

	/**
	 * ROUND 236 — the ONE red designer note explaining the ❗ markers.
	 *
	 * Placed at the top of the acknowledgements block (Chris's decision
	 * 2026-07-29) so it is read in context, immediately above the lines it
	 * refers to. Two wordings, because the two situations need different
	 * actions from the designer: NO file was supplied at all (upload it), or a
	 * file was supplied but does not cover every asset (top it up / check those
	 * specific ids). Carries class cv2-note, so like every other converter note
	 * it is excluded from the skeleton, compare_structure and body_compare by
	 * construction (round 72) — it can never move a gate.
	 *
	 * @param {ConversionRun} run
	 * @returns {string} the note's HTML, or "" when every title was verified
	 */
	static #unverifiedNote(run) {
		const cfg = DataService.Data.AcksFormats.istock_unverified ?? {};
		if (cfg.enabled === false) return "";
		if (typeof process !== "undefined" && process.env && process.env.ISTOCKUNVERIFIED_OFF) return "";

		const ids = run?.istockUnverified ?? [];
		if (!ids.length) return "";

		// count DISTINCT assets, not occurrences: the same photo is often
		// listed several times across a module, and the acks block itself
		// de-duplicates per lesson group — so a raw occurrence count would
		// promise the designer more ❗ lines than the page actually shows.
		const unique = [...new Set(ids)];
		const count = unique.length;
		const plural = count === 1 ? "" : "s";
		const max = cfg.note_ids_max ?? 12;
		const shown = unique.slice(0, max).join(", ")
			+ (unique.length > max ? `, … (+${unique.length - max} more)` : "");

		const text = run?.istockAcksSupplied
			? Utils.FillTemplate(cfg.note_partial ?? "", {
				count, plural, those: count === 1 ? "that" : "those", ids: shown,
			})
			: Utils.FillTemplate(cfg.note_no_file ?? "", {
				count, plural, were: count === 1 ? "was" : "were",
			});

		run?.AddNote("warn", "AcksBuilder",
			`${count} iStock title${plural} could not be verified`
			+ (run?.istockAcksSupplied
				? ` (the supplied acknowledgements file does not cover them)`
				: ` (no *istock-acks*.txt was supplied)`)
			+ `; each is marked ❗ and the acks block carries a designer note.`);

		return Utils.FillTemplate(cfg.note_form ?? "", {
			noteClass: cfg.note_class ?? "cv2-note", text,
		});
	};

	/**
	 * THE ACK-TODO emitter — builds a visible ❗ line plus a machine-readable
	 * HTML comment recording exactly what is missing, and tallies the build
	 * gate: every call runs run.CountAckTodo(), so the run's summary panel
	 * shows how many incomplete acknowledgements this module has.
	 *
	 * HOW: the comment is always `<!-- ACK-TODO[type] attr="value" … -->`
	 * (machine-parseable, so a future tool could scan every output file for
	 * outstanding TODOs). The visible line either uses the caller-supplied
	 * `entryLine` — when a builder above already assembled a partial line
	 * with a bracketed placeholder slot, e.g. iStock's
	 * "[OFFICIAL ISTOCK TITLE REQUIRED]" — or, when no entryLine is given,
	 * falls back to a generic "{prefix}: {slot}, {description}." built from
	 * the `type`'s slot text in Acks_Formats.json (ack_todo.types).
	 *
	 * @param {Object} item - the Media List row this TODO is for
	 * @param {string} type - the TODO's kind, a key into ack_todo.types,
	 *   e.g. "asset-id" | "istock-name" | "licence" | "video-meta"
	 * @param {Object} attrs - key → value pairs recorded in the HTML
	 *   comment (e.g. { title: item.description })
	 * @param {ConversionRun} run - the run (for CountAckTodo)
	 * @param {?string} entryLine - a pre-built visible line to use verbatim
	 *   instead of the generic fallback, or null to use the fallback
	 * @returns {Object} an entry (see the shape note above) with
	 *   sourceClass "todo" and a non-null todoComment
	 */
	static #todo(item, type, attrs, run, entryLine = null) {
		const fmt = DataService.Data.AcksFormats;
		run.CountAckTodo();

		const attrText = Object.entries(attrs)
			.map(([k, v]) => `${k}="${String(v).replace(/"/g, "'")}"`).join(" ");
		const comment = `<!-- ACK-TODO[${type}] ${attrText} -->`;

		// default visible line when no partial entry was built: the slot text
		const slot = fmt.ack_todo.types[type]?.slot ?? "[DETAILS REQUIRED]";
		const line = entryLine
			?? `${this.#typePrefix(item, run)}: ${slot}, ${item.description || item.url || `item ${item.itemNo}`}.`;

		return {
			html: Utils.FillTemplate(fmt.ack_todo.visible_form, { entryLineWithBracketedSlots: line }),
			todoComment: comment,
			sourceClass: "todo",
			item,
		};
	};

	/**
	 * Looks up the short descriptive word placed before an acknowledgement's
	 * title (e.g. "Image", "Video") from the writer's own item-type text,
	 * via Acks_Formats.json's type_prefix_map.
	 *
	 * WHY THE FALLBACK IS LOGGED: a type absent from the map still needs
	 * SOME prefix so the line reads sensibly, so this Title-Cases the raw
	 * type text itself ("jpg"→"Jpg") as a best-effort fallback — but that
	 * fallback is a genuine gap (the map should really have an entry for
	 * this type), so it is always logged via run.AddNote as a warning
	 * telling the developer to add it to type_prefix_map. (See also
	 * #isUnknownType and the "UNKNOWN ITEM TYPE" comment in #buildEntry,
	 * which turns this same gap into a visible ❗ flag on the finished
	 * line too, not just a background log note.)
	 *
	 * @param {Object} item - a Media List row (see the shape note above)
	 * @param {ConversionRun} run - the run (for AddNote)
	 * @returns {string} the prefix word, e.g. "Image" (no trailing colon —
	 *   callers add their own punctuation via the entry templates)
	 */
	static #typePrefix(item, run) {
		const map = DataService.Data.AcksFormats.type_prefix_map;
		const key = Utils.Fold(item.itemType ?? "");
		if (map[key]) return map[key];
		const fallback = (item.itemType ?? "Item").charAt(0).toUpperCase()
			+ (item.itemType ?? "Item").slice(1).toLowerCase();
		if (key) {
			run.AddNote("warn", "AcksBuilder",
				`Unknown media item type "${item.itemType}" (item ${item.itemNo}) — used "${fallback}" as the prefix; add it to Acks_Formats type_prefix_map.`);
		}
		return fallback;
	};

	/**
	 * Checks whether an item's type has no entry in type_prefix_map — the
	 * trigger condition for the "UNKNOWN ITEM TYPE" re-flag in #buildEntry
	 * above (search this file for that heading for the full explanation).
	 *
	 * @param {Object} item - a Media List row (see the shape note above)
	 * @returns {boolean} true when itemType is non-empty but unrecognised
	 */
	static #isUnknownType(item) {
		const map = DataService.Data.AcksFormats.type_prefix_map;
		const key = Utils.Fold(item.itemType ?? "");
		return !!key && !map[key];
	};

	/**
	 * Re-wraps an already-built PLAIN entry as a visible ❗ ackTodo, keeping
	 * its line content (including any <a> link) and tallying the build gate
	 * — i.e. calling run.CountAckTodo() so this ACK-TODO is counted in the
	 * run's summary tally alongside every other one, exactly like #todo()
	 * does for a TODO built from scratch. Used for unknown-type entries so
	 * every "not enough information" line flags consistently (see the
	 * "UNKNOWN ITEM TYPE" comment in #buildEntry above).
	 *
	 * @param {Object} item - the Media List row this entry came from
	 * @param {Object} entry - the already-built entry (from #plain) to re-wrap
	 * @param {ConversionRun} run - the run (for CountAckTodo)
	 * @returns {Object} a new entry (see the shape note above) with
	 *   sourceClass "todo" and a non-null todoComment
	 */
	static #todoFromEntry(item, entry, run) {
		const fmt = DataService.Data.AcksFormats;
		run.CountAckTodo();
		const inner = String(entry.html).replace(/^\s*<p>/, "").replace(/<\/p>\s*$/, "");
		const type = String(item.itemType ?? "").replace(/"/g, "'");
		return {
			html: Utils.FillTemplate(fmt.ack_todo.visible_form, { entryLineWithBracketedSlots: inner }),
			todoComment: `<!-- ACK-TODO[unknown-type] type="${type}" item="${item.itemNo}" -->`,
			sourceClass: "todo",
			item,
		};
	};

	/**
	 * Classifies a media item into one of the known source categories
	 * (istock / youtube / pixabay / wikicommons / twinkl / heygen / ai /
	 * other_stock / website / skip / tekura) so #buildEntry knows which
	 * attribution template and title-extraction rule applies.
	 *
	 * HOW: checks, in order, (1) the item's own type against a skip list
	 * (e.g. "lesson link" items never get acknowledged), (2) the item's URL
	 * against a list of known domains (istock.com, youtube.com, …), (3) the
	 * item's "source" text against a list of source keywords (for cases
	 * where the URL alone doesn't identify the site), and finally falls
	 * back to the data's configured default classification ("website").
	 * Every list this checks against comes from
	 * Acks_Formats.json's source_classification — nothing is hard-coded here,
	 * so a new source site is added by editing that data, not this code.
	 *
	 * @param {Object} item - a Media List row (see the shape note above)
	 * @returns {string} the sourceClass key, e.g. "istock" | "skip" | "website"
	 */
	static #classify(item) {
		const rules = DataService.Data.AcksFormats.source_classification;
		const url = Utils.Fold(item.url ?? "");
		const source = Utils.Fold(item.source ?? "");
		const type = Utils.Fold(item.itemType ?? "");

		if (rules.skip_types.includes(type)) return "skip";
		for (const r of rules.by_domain) if (url.includes(r.match)) return r.source;
		for (const r of rules.by_source_keyword) if (source.includes(r.match)) return r.source;
		return rules.default;
	};

	// =======================================================================
	// LESSON GROUPING (the evidence chain)
	// =======================================================================

	/**
	 * Groups built entries by lesson — which page (lesson) each
	 * acknowledgement should be listed under — strongest evidence first.
	 * See "LESSON MAPPING" in the file header above for the four-step
	 * fallback chain; each step is commented inline below, right where it
	 * runs, with its own "---- evidence N: ... ----" banner.
	 *
	 * WHY A FALLBACK CHAIN AT ALL: the Media List itself does not record
	 * which lesson/page a given item belongs to, so this has to be
	 * INFERRED from other evidence — and every inference weaker than a
	 * direct content match is surfaced via run.AddNote so a human can spot
	 * a bad guess (per the run's "nothing swallowed quietly" contract).
	 *
	 * @param {Object[]} entries - built entries (nulls already filtered out
	 *   by Build())
	 * @param {ConversionRun} run - the run (for run.pages + AddNote)
	 * @returns {Object[]} [{ label: "1.0", entries: […] }, …] one group per
	 *   page, in page order (always at least one group, even with 0 pages)
	 */
	static #groupByLesson(entries, run) {
		const labels = run.pages.map((p) => p.lessonLabel ?? "0.0");
		const groups = labels.map((label) => ({ label, entries: [] }));
		if (!groups.length) groups.push({ label: "0.0", entries: [] });

		// ---- evidence 1: content match — URL/asset-id per page -------------
		// (collect each page's normalised URLs + bare asset ids once)
		const pageKeys = run.pages.map((p) => {
			const keys = new Set();
			for (const it of p.items) {
				const texts = [it.text ?? "", it.blackAfter ?? "", it.block?.text ?? ""];
				for (const l of (it.block?.links ?? [])) texts.push(l.target);
				for (const t of texts) {
					for (const u of String(t).matchAll(/https?:\/\/[^\s\]\)"<>]+/g)) {
						keys.add(this.#normaliseUrl(u[0]));
						const gm = u[0].match(/gm-?(\d{6,10})/);
						if (gm) keys.add(gm[1]);
						const yt = u[0].match(new RegExp(DataService.Data.AcksFormats.extraction_regexes.youtube_id));
						if (yt) keys.add(yt[1]);
					}
				}
			}
			return keys;
		});

		const placed = new Map();   // entry → group index
		for (const e of entries) {
			const url = this.#normaliseUrl(e.item.url ?? "");
			const id = (e.item.url ?? "").match(/gm-?(\d{6,10})/)?.[1]
				?? (e.item.url ?? "").match(new RegExp(DataService.Data.AcksFormats.extraction_regexes.youtube_id))?.[1];
			const hits = [];
			pageKeys.forEach((keys, pi) => {
				if ((url && keys.has(url)) || (id && keys.has(id))) hits.push(pi);
			});
			if (hits.length === 1) placed.set(e, hits[0]);
			else if (hits.length > 1) placed.set(e, hits[0]);   // first use wins
		}

		// ---- evidence 2: WT page records (only when trustworthy) -----------
		if (run.pageRecordsUsable) {
			const spans = run.pages.map((p, i) => ({
				from: p.wtPageStart ?? 0,
				to: run.pages[i + 1]?.wtPageStart ?? Infinity,
			}));
			for (const e of entries) {
				if (placed.has(e) || !e.item.wtPage) continue;
				const pi = spans.findIndex((s) => e.item.wtPage >= s.from && e.item.wtPage < s.to);
				if (pi >= 0) placed.set(e, pi);
			}
		}

		// ---- evidence 3: neighbour interpolation ----------------------------
		// media lists run in document order — an unplaced item between two
		// placed neighbours inherits the earlier one's lesson (surfaced)
		const ordered = [...entries];   // already in media-list row order
		for (let i = 0; i < ordered.length; i++) {
			const e = ordered[i];
			if (placed.has(e)) continue;
			let prev = null;
			for (let j = i - 1; j >= 0; j--) if (placed.has(ordered[j])) { prev = placed.get(ordered[j]); break; }
			let next = null;
			for (let j = i + 1; j < ordered.length; j++) if (placed.has(ordered[j])) { next = placed.get(ordered[j]); break; }

			if (prev !== null && (next === null || next === prev)) {
				placed.set(e, prev);
				run.AddNote("info", "AcksBuilder",
					`Media item ${e.item.itemNo} placed in lesson ${groups[prev].label} by neighbour interpolation — verify its group.`);
			} else if (prev !== null) {
				placed.set(e, prev);   // between two different lessons → earlier
				run.AddNote("warn", "AcksBuilder",
					`Media item ${e.item.itemNo} sits between lessons ${groups[prev].label} and ${groups[next].label} — placed in ${groups[prev].label}; verify.`);
			}
		}

		// ---- evidence 4: fallback — first group, loudly ----------------------
		for (const e of entries) {
			if (!placed.has(e)) {
				placed.set(e, 0);
				run.AddNote("warn", "AcksBuilder",
					`Media item ${e.item.itemNo} could not be mapped to a lesson — placed in the first group (${groups[0].label}); verify.`);
			}
			groups[placed.get(e)].entries.push(e);
		}

		return groups;
	};

	/**
	 * Normalises a URL so two different-looking links to the SAME resource
	 * compare equal — used by #groupByLesson's evidence-1 pass (content
	 * match) to check whether a media item's URL also appears somewhere in
	 * a page's own content.
	 *
	 * WHAT IT STRIPS: the "https://" / "www." prefix, case/diacritic/
	 * whitespace differences (via Utils.Fold), tracking-only query params
	 * (?si=, ?feature=, any utm_*, per Acks_Formats.json's
	 * url_normalise_strip_params list — a YouTube share link and a plain
	 * watch link to the same video should still match), and trailing
	 * punctuation/slashes.
	 *
	 * @param {string} url - a raw URL (or "")
	 * @returns {string} the normalised form, safe to compare with ===
	 */
	static #normaliseUrl(url) {
		if (!url) return "";
		const strip = DataService.Data.AcksFormats.extraction_regexes.url_normalise_strip_params;
		let u = Utils.Fold(url).replace(/^https?:\/\//, "").replace(/^www\./, "");
		// remove the listed query params + any utm_*; then trailing junk
		u = u.replace(/[?&](si|feature|utm_[a-z]+)=[^&]*/g, "");
		return u.replace(/[?&]+$/, "").replace(/[\/.,;]+$/, "");
	};

	/**
	 * A tiny awaitable pause. `await this.#sleep(ms)` blocks the async
	 * MapSeries loop in Build() for `ms` milliseconds before moving to the
	 * next media item, so requests to YouTube's free oEmbed endpoint go out
	 * throttled rather than all at once (Acks_Formats.json's
	 * oembed.throttle_ms; see the "Browser-only progress reporting" comment
	 * in Build() for why this makes the acks step the slowest part of a
	 * real browser conversion).
	 *
	 * @param {number} ms - milliseconds to wait
	 * @returns {Promise<void>}
	 */
	static #sleep(ms) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { AcksBuilder };
