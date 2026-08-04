/**
 * InteractiveScanner.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Finds every interactive ACTIVITY BLOCK in a page's item stream and
 * bundles it: openers + the interactive tag + all members, ending at the
 * first terminator. Phase 1 never BUILDS interactives — the bundles feed
 * the placeholder emitter and the {CODE}_interactives.txt manifest.
 *
 * THE BLOCK MODEL (Interactive_Boundary_Rules.md §1):
 *   [ OPENERS ] → [ INTERACTIVE TAG ] → [ MEMBERS … ] ‖ [ TERMINATOR ]
 * The terminator is NOT consumed — it is the next thing to render normally.
 *
 * DATA THIS FILE READS (no boundary knowledge in code):
 * Interactive_Boundary_ChildTag_Bank.json —
 *   _meta.opener_rule.opener_tags            which tags can precede a block
 *   _meta.member_rule.terminators_absolute    hard stops, always
 *   _meta.member_rule.terminators_conditional h2–h5, per-widget flag
 *   interactives[type].heading_is_terminator  the per-widget flag
 * Tag_Lexicon.json (via TagNormaliser)        which tags are INTERACTIVE
 *
 * SAFE DEFAULTS (also from the bank's rules):
 * - heading_is_terminator === null (unknown widget) → headings TERMINATE
 *   (errs toward more normal conversion — the safer Phase-1 failure mode).
 * - A nested interactive terminates the current block and starts its own;
 *   worst case the nested widget gets its own placeholder, which is safe.
 * ===========================================================================
 */

class InteractiveScanner {

	/**
	 * Scans one page, returning interactive bundles and marking the item
	 * ranges they consumed (so the converter can skip them).
	 *
	 * WHAT A BUNDLE LOOKS LIKE:
	 * {
	 *   index: 3,                    // 1-based, run-wide (set by caller)
	 *   type: "dragAndDrop",         // bank/manifest type
	 *   canonTag: "drag and drop",   // lexicon canonical
	 *   modifier: "autocheck",       // remainder/extra hints ("" if none)
	 *   activityId: "2B" | null,     // captured from the opener
	 *   headingText: "Can you spot a good prompt…",
	 *   openerItems: [...], memberItems: [...],   // raw items (in order)
	 *   tables: [tableBlock…],       // content_data
	 *   instructions: ["please scramble …"],      // → red flags too
	 *   media: [{text,target}…],     // links seen inside the block
	 *   positionContext: "After heading \"What is AI?\"",
	 *   startIndex, endIndex,        // item-range consumed [start, end)
	 *   redFlags: ["…"],             // anything ambiguous, surfaced
	 * }
	 *
	 * @param {Object} page - PageSplitter page (items walked in order)
	 * @param {TagNormaliser} normaliser - for widget-type lookups
	 * @param {ConversionRun} run - tallies + notes
	 * @returns {Object[]} bundles (page-local; caller assigns run indexes)
	 */
	static ScanPage(page, normaliser, run) {
		const bank = DataService.Data.BoundaryBank;
		const openerTags = new Set(bank._meta.opener_rule.opener_tags);
		const absolute = new Set(bank._meta.member_rule.terminators_absolute);
		// GENERAL widget boundary: every registered STANDALONE CALLOUT tag (the keys of
		// Emit_Templates.callouts.by_tag) ALSO hard-terminates widget capture. A callout box such as
		// [side alert]/[alert]/[wananga]/[supervisor note] sitting beside or after a widget is the
		// writer's OWN separate element — never a member of the widget — so #swallowMembers must stop
		// there. DATA-DRIVEN + REUSABLE: because this reads the callouts.by_tag keys directly, any
		// FUTURE tag added to callouts.by_tag automatically becomes a boundary too, with nothing else
		// to update. [Side alert] in particular is its own canonical tag and is NOT listed in
		// terminators_absolute, so without this special case a side alert sitting right next to an
		// activity widget could get swallowed into the widget as if it were part of it. Data
		// callout_tags_terminate; env CALLOUTTERM_OFF reverts to a shorter, hard-coded literal list
		// (alert/important/whakatauki/quote only — missing wananga/supervisor note/side alert and any
		// future callout tag).
		if (bank._meta.member_rule.callout_tags_terminate !== false
			&& !(typeof process !== "undefined" && process.env && process.env.CALLOUTTERM_OFF)) {
			const _byTag = DataService.Data.EmitTemplates?.callouts?.by_tag || {};
			for (const _t of Object.keys(_byTag)) absolute.add(_t);
		}
		const items = page.items;
		const bundles = [];

		// BILINGUAL reoMode flag (mirrors the equivalent check in ContentConverter's own setup:
		// dual_language enabled + reoTranslate body_class / mtkFlag / TRR|PNR code prefix). Used by
		// the post-scan activity-number pass below to assign a widget bundle the activity number that
		// lives in an "Activity NX:" table ROW (not an [Activity N] tag).
		const _dlCfg = DataService.Data.EmitTemplates?.elements?.dual_language;
		// The "MTK WRITERS TEMPLATE" house header that many Writers Templates carry at the top is NOT,
		// by itself, a reliable signal that the module is bilingual (see PageSplitter for the full
		// reasoning) — most modules with that header are ordinary single-language modules. So it only
		// counts as a bilingual trigger when data explicitly says use_mtk_flag:true, or the env var
		// MTKREO_OFF=1 is set to force the older, more permissive behaviour back on for comparison.
		const _mtkArm = (!!_dlCfg && _dlCfg.use_mtk_flag === true)
			|| !!(typeof process !== "undefined" && process.env && process.env.MTKREO_OFF);
		const reoMode = !!_dlCfg && _dlCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.REOTRANSLATE_OFF)
			&& (/reoTranslate/i.test(run?.resolvedRules?.body_class || "") || (_mtkArm && !!run?.mtkFlag)
				|| (_dlCfg.code_prefixes || []).some((p) => String(run?.moduleCode || "").toUpperCase().startsWith(String(p).toUpperCase())));

		// rolling context: the most recent heading/element text, so each
		// bundle can say where it sits ("After heading …") for the manifest
		let lastContext = page.isOverview ? "Top of overview page" : "Top of page";

		for (let i = 0; i < items.length; i++) {
			const it = items[i];
			if (it.type === "tag" && it.parse.primary?.directive === "ELEMENT") {
				const txt = (it.blackAfter || it.parse.remainders.join(" ")).trim();
				if (txt) lastContext = `After ${it.parse.primary.tag} "${txt.slice(0, 60)}"`;
			}

			// ---- activity WITHOUT a widget keyword but WITH a data table ---
			// (the BLL phonics pattern — verified on BLL146 Activities
			// 1A/1C/1D: "[Activity N]" + instructions + a TABLE of widget
			// data, with the widget type only described in prose). Such an
			// activity IS a build-task: capture it un-built as an
			// UNCLASSIFIED bundle with a red flag, never as a plain content
			// table. Deferred to the normal path when a real interactive
			// tag appears before the table (its opener-lookback will own
			// this activity item instead).
			if (it.type === "tag" && it.consumedBy === undefined
				&& it.parse.primary?.tag === "activity"
				&& it.parse.primary?.directive === "CONTAINER_OPEN") {
				let tableAhead = false;
				for (let j = i + 1; j < items.length; j++) {
					const peek = items[j];
					if (peek.consumedBy !== undefined) break;
					if (peek.type === "table") { tableAhead = true; break; }
					if (peek.type !== "tag") continue;
					const pp = peek.parse.primary;
					if (!pp) continue;
					if (pp.directive === "INTERACTIVE") break;        // normal path owns it
					if (pp.tag === "activity" || absolute.has(pp.tag)
						|| pp.directive === "PAGE_BOUNDARY") break;    // window over, no table
				}
				if (tableAhead) {
					const bundle = {
						type: "unclassified", canonTag: "activity",
						modifier: "", headingText: "",
						activityId: it.parse.numbers[0]?.toUpperCase() ?? null,
						openerItems: [], memberItems: [], tables: [],
						instructions: [], media: [],
						redFlags: ["Activity has a data table but NO recognised interactive keyword — widget type must be identified from the captured content."],
						positionContext: lastContext,
						startIndex: i, endIndex: i + 1,
					};
					// the activity item itself is the first member (its
					// blackAfter carries the activity title/instructions)
					this.#collectMember(bundle, it, run);
					bundle.endIndex = this.#swallowMembers(bundle, items, i + 1,
						/* headings terminate the unknown widget: */ true, absolute, run, normaliser);
					for (let k = bundle.startIndex; k < bundle.endIndex; k++) {
						items[k].consumedBy = bundles.length;
					}
					bundles.push(bundle);
					i = bundle.endIndex - 1;
					continue;
				}
			}

			// ---- interactives INSIDE a table row (data pattern 8) ----------
			// Speech bubbles & co. often arrive as "[speech bubble] text ║
			// [image] url" table rows — the invocation lives in a CELL, so
			// the table itself is the whole bundle (verified on OSAH401).
			if (it.type === "table" && it.consumedBy === undefined) {
				// reoMode SAFETY CHECK: a bilingual English|Māori CONTENT table is NOT a widget, even
				// when one of its body cells happens to embed an `[Interactive] [X]` reference (the
				// writer is just mentioning a widget inline, as part of the intro prose). Skip the
				// interactive-in-table capture in that case, so the table unfolds normally via
				// BilingualBuilder's `bilingualTable` instead. Without this check the intro table was
				// wrongly over-captured as a flipCard widget (measured on 64 of 140 bilingual bundles),
				// which then made the activity box wrap the WRONG content, get mis-numbered, and the
				// reo/eng prose never rendered at all. Data dual_language.content_table_guard; env
				// REOTABLE_OFF.
				const _ctgOn = reoMode
					&& !(typeof process !== "undefined" && process.env && process.env.REOTABLE_OFF)
					&& (DataService.Data.EmitTemplates?.elements?.dual_language?.content_table_guard?.enabled !== false);
				const cellType = (_ctgOn && this.#bilingualContentTable(it.block))
					? null
					: this.#interactiveInTable(it.block, normaliser);
				if (cellType) {
					const bankEntry2 = bank.interactives[cellType.type] ?? null;
					const tableBundle = {
						type: cellType.type, canonTag: cellType.canonTag,
						modifier: "", activityId: null, headingText: "",
						openerItems: [], memberItems: [it], tables: [it.block],
						instructions: [], media: [], redFlags: bankEntry2 ? [] : [
							`Widget type "${cellType.type}" has no boundary-bank entry.`],
						positionContext: lastContext,
						startIndex: i, endIndex: i + 1,
					};
					this.#harvestMedia(tableBundle, it);
					// FLIPCARD [Embedded] DATA-TABLE ABSORB. The [Embedded][Flipcard] DECLARATION table
					// is captured right here (its [Flipcard] invocation lives inside one of its own
					// cells); but its SEPARATE following [Item N] data table carries no invocation of its
					// own, so left alone it would escape this bundle entirely and leak into the page as a
					// raw, unstyled table (69 such leaks were once observed across a handful of PNR
					// modules). Absorb any immediately-following member-tagged data table(s) into THIS
					// same bundle, so the end result is ONE flipCard placeholder (the [Item N]/[Image]
					// data sits inside it as a developer reference, not a visible leak). A following table
					// that carries its OWN invocation, or its own [back] face content, is deliberately
					// LEFT for that separate bundle to claim instead (see the #interactiveInTable guard
					// above). Data member_rule.flipcard_data_table_absorb; env FLIPDATA_OFF.
					const fda = DataService.Data.BoundaryBank?._meta?.member_rule?.flipcard_data_table_absorb;
					if (fda && fda.enabled !== false && cellType.type === (fda.widget_type ?? "flipCard")
						&& !(typeof process !== "undefined" && process.env && process.env.FLIPDATA_OFF)
						&& new RegExp("\\[\\s*" + (fda.trigger_tag ?? "embedded") + "\\b", "i").test(it.block.text ?? "")) {
						const memRe = new RegExp("\\[\\s*(" + (fda.member_tags ?? ["item"]).join("|") + ")\\b", "i");
						let j = i + 1;
						while (j < items.length && items[j].type === "table" && items[j].consumedBy === undefined
							&& !this.#interactiveInTable(items[j].block, normaliser)
							&& memRe.test(items[j].block?.text ?? "")) {
							tableBundle.memberItems.push(items[j]);
							tableBundle.tables.push(items[j].block);
							this.#harvestMedia(tableBundle, items[j]);
							items[j].consumedBy = bundles.length;
							tableBundle.endIndex = j + 1;
							j++;
						}
					}
					it.consumedBy = bundles.length;
					bundles.push(tableBundle);
					i = tableBundle.endIndex - 1;
					continue;
				}
			}

			// HOVER/ROLLOVER DEFINITION marker whose definition is NOT introduced by the word "trigger"
			// (so the SINGLE-BRACKET inline-trigger handling further below, which keys off that word,
			// never reaches it). Two shapes are handled here:
			//   - COLON self-closed: "[hover: DEF]" / "[hover definition: DEF]" — the definition sits
			//     inside the bracket, after the first colon. Written as "[Hover: …]" this would
			//     otherwise resolve as a plain [body] tag and SPLIT the paragraph in two; written as
			//     "[hover definition: …]" it resolves as an infoTrigger, but the "trigger"-keyed handling
			//     mentioned above still DROPS the definition text.
			//   - MARKER-THEN-DEF: "[hover text] DEF" — the definition follows the closing bracket,
			//     inside the SAME red span (e.g. ENGC101: "**adjectives** [hover text] Describing
			//     words.").
			// Both shapes are woven onto the nearest preceding word as the infoTrigger sentinel (the same
			// mechanism the single-bracket inline trigger uses below), so the paragraph stays in one
			// piece instead of splitting. This must run BEFORE the INTERACTIVE-tag skip a little further
			// down, because the "[Hover: …]" shape resolves to a plain [body] tag and would never reach
			// the standalone-widget path otherwise.
			// Data EmitTemplates.elements.hover_definition_inline; env HOVERDEF_OFF.
			if (it.consumedBy === undefined && this.#weaveHoverDefinition(items, i, normaliser)) continue;

			if (it.type !== "tag" || it.parse.primary?.directive !== "INTERACTIVE") continue;
			if (it.consumedBy !== undefined) continue;   // already inside a bundle

			// ACCORDION-AS-PHASES SUPPRESSION (registry-gated to specific module families — see
			// #accordionPhaseRow): on a gated page, an accordion-opening invocation never opens a
			// widget bundle at all. Some modules author their content as a single big [Accordion] with
			// numbered [Accordion N] panels, but the finished page actually presents those panels as
			// separate "phases" (a phases nav + one panel per phase), not as a built accordion widget.
			// So here the numbered/bare accordion tags are deliberately left UNCONSUMED, so a later
			// pre-pass in ContentConverter can turn them into phase-boundary markers instead
			// (numbered → a phase break, bare opener → a no-op); a "[link to … accordion menu]"
			// cross-link form is left for that same pre-pass to dissolve into ordinary prose (its
			// blackAfter text is genuine content the finished page keeps as-is).
			// Data fundamentals_panels.phase_text.accordion_delimiter; env FUNPANACC_OFF.
			if (InteractiveScanner.#accordionPhaseForm(it, run)) continue;

			// MTK DROP-DOWN-MENU MARKER SUPPRESSION (ROUND 212 — the PNR101/102/104
			// bilingual family): the "[Content for DROP DOWN MENU]" opener parses as a
			// "dropdown" INTERACTIVE invocation, but it is a MENU section marker, not a
			// widget — opening a bundle here would swallow the module-menu table into an
			// orange placeholder. On a bilingual (reoTranslate/TRR/PNR) module whose
			// opener is DIRECTLY followed by the menu table (the PNR shape — the
			// paragraph-form TRR203/TRR301 siblings are deliberately untouched), the
			// marker is left unconsumed so ContentConverter's #partitionItems can route
			// that table to the module menu instead.
			// Data: elements.dual_language.dropdown_menu. Env toggle: REODROPMENU_OFF.
			if (InteractiveScanner.#dropdownMenuMarker(items, i, run)) continue;

			// ---- the invocation ------------------------------------------
			const canonTag = it.parse.primary.tag;
			const type = this.#widgetTypeFor(canonTag, it.parse.primary.alias, normaliser);

			// STANDALONE INLINE MARKER (in free body, not inside any open widget): it
			// is NOT a widget — the human renders it inline ON the surrounding text
			// (a [highlight text] highlight, or a [rollover definition] tooltip span).
			// Before this fix it opened a widget that either SWALLOWED the following
			// paragraphs (XGF9001 #7 ate 1,537 chars; SSFUN07-00 an inline rollover ate
			// the page) or left a tiny EMPTY box. Phase 1 can't build the inline
			// annotation, so we drop the marker literal and re-expose its own-line text
			// as plain free body — the surrounding content converts normally, in place.
			// Both inline_markers and standalone_inline_markers get THIS role; only
			// inline_markers are ALSO absorbed inside an open widget (see #swallowMembers).
			// (Bank policy member_rule.{inline_markers,standalone_inline_markers}; body-breakdown #2/#3.)
			const _mr = DataService.Data.BoundaryBank._meta.member_rule;
			const _isWordSelect = (_mr.inline_markers ?? []).includes(type);
			const _isStandalone = (_mr.standalone_inline_markers ?? []).includes(type);
			// TABLE-QUALIFIED widget: "[Table wordSelect]" / "[Table dragAndDrop]" is a
			// STANDALONE table-data interactive (the human builds a clickable table), NOT an inline
			// highlight marker — the "Table" qualifier on the tag is the writer flagging the data form.
			// So a marker tag that ALSO carries a [table] tag is NOT dissolved inline; it falls through
			// to the normal bundle path and captures its following table (OSAI401-01 Activity 1A's
			// [Table wordSelect] "What can AI do" was rendering as a RAW <table>, un-wrapped).
			// Data: member_rule.table_qualifier_tags.
			const _tableQual = (_mr.table_qualifier_tags ?? ["table"]);
			const _hasTableQualifier = it.parse.tags.some((t) => _tableQual.includes(t.tag));
			if ((_isWordSelect || _isStandalone) && !_hasTableQualifier) {
				// INFO-TRIGGER (a standalone hover/rollover DEFINITION) authored INLINE as
				// "anchor [hovertrigger: DEFINITION] continuation". The parser splits that into the
				// PRECEDING anchor item, THIS marker (its blackAfter = the DEFINITION), and a "]"
				// CLOSER item (its blackAfter = the rest of the sentence). The old code re-exposed the
				// DEFINITION as body text (a LEAK) and left the closer to render as a SEPARATE <p> (a
				// SPLIT). Re-STITCH: fold the definition onto the anchor as an inline annotation —
				// encoded as a private-use sentinel … that #inlineMarkup turns into a
				// <span class="infoTrigger" info="DEF"> when the anchor is a clear bold/italic run (and
				// drops it to plain text otherwise) — and re-join the continuation, so the whole thing
				// is ONE paragraph. (ENGC201-00 "This **whakatauki** [hovertrigger: Proverb] reinforces…"
				// → one <p> with <span class="infoTrigger" info="Proverb">whakatauki</span> reinforces…)
				if (_isStandalone && !_isWordSelect) {
					// SINGLE-BRACKET inline trigger. "anchor [audio trigger DEF]" / "anchor [hover
					// trigger DEF]" carries the DEFINITION INSIDE its own SELF-CLOSED red span (the
					// bracket opens AND closes within this one marker), so there is NO separate "]"
					// closer item — the split-bracket path further below never fires, and left
					// unhandled the marker would BREAK the paragraph and drop the definition entirely
					// (e.g. "Being an online kaitiaki [audio trigger kai-ti-a-ki] means …" would render
					// as three separate <p> elements instead of one). Detect this self-closed form,
					// recover the DEFINITION in its ORIGINAL letter case from the marker text that
					// follows the word "trigger" (parse.remainders has already been folded to
					// lowercase and mangled, so it can't be used for the info= attribute), encode it
					// using the U+E000…U+E001 sentinel characters directly after the preceding anchor
					// word, and re-join the continuation — producing ONE paragraph that #inlineMarkup
					// later turns into <span class="infoTrigger" info="DEF">anchor</span>. The separate
					// split-bracket acronym form ("[hover trigger DEF" with a separate "]" later) is
					// NOT self-closed, so it is left untouched by this branch.
					// Data: EmitTemplates.elements.info_trigger_inline.enabled; env INFOTRIG_OFF.
					const _itCfg = DataService.Data.EmitTemplates.elements?.info_trigger_inline;
					const _inlineTrigOn = (_itCfg?.enabled !== false)
						&& !(typeof process !== "undefined" && process.env && process.env.INFOTRIG_OFF);
					if (_inlineTrigOn) {
						const rawMarker = String(it.text ?? "")
							.replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").trim();
						const selfClosed = /\]\s*$/.test(rawMarker);            // bracket closes in THIS marker
						const mTrig = rawMarker.match(/\btrigger\b\s*:?\s*([\s\S]*?)\s*\]\s*$/i);
						const infoInside = mTrig ? mTrig[1].trim() : "";        // original-case definition
						// An instruction-shaped "def" (e.g. "[Hover trigger over image + captions.
						// Please embed these images and have drop-down boxes…]") is really a writer NOTE
						// to the developer, not an actual definition: skip the weave here so it falls
						// through to the ordinary CS-note handling instead (the finished page strips
						// notes like this). Data elements.hover_weave_hygiene; env HOVERHYG_OFF.
						if (selfClosed && infoInside && !InteractiveScanner.#hoverDefIsInstruction(infoInside)) {
							const IT0 = String.fromCharCode(0xE000), IT1 = String.fromCharCode(0xE001);
							const sentinel = IT0 + infoInside + IT1;
							const continuation = String(it.blackAfter ?? "").trim();
							// anchor host = nearest PRECEDING item that still carries text — skip
							// already-consumed empties so back-to-back triggers (kaitiaki THEN taonga in
							// one sentence) each anchor on their own word, not on a hollow sibling.
							// A candidate whose trailing text is a bare URL can never host the sentinel —
							// the URL-detection machinery reads straight through the private-use
							// characters used to encode it, corrupting the link. When only media is
							// adjacent like this there is no usable word to anchor the definition to, so
							// fall through to the no-host case below instead.
							let h = i - 1, host = null;
							while (h >= 0) {
								const cand = items[h];
								const ctext = cand.type === "black" ? cand.text : cand.blackAfter;
								if (String(ctext ?? "").trim()) {
									if (InteractiveScanner.#urlTailHost(ctext)) { host = null; break; }
									host = cand; break;
								}
								h--;
							}
							if (host && host.type === "black") {
								host.text = String(host.text ?? "").replace(/\s+$/, "") + sentinel
									+ (continuation ? ` ${continuation}` : "");
								it.type = "black"; it.text = ""; it.blackAfter = ""; continue;
							} else if (host) {
								host.blackAfter = String(host.blackAfter ?? "").replace(/\s+$/, "") + sentinel
									+ (continuation ? ` ${continuation}` : "");
								it.type = "black"; it.text = ""; it.blackAfter = ""; continue;
							}
							// no usable anchor host → keep the continuation (no word to annotate)
							it.type = "black"; it.text = continuation; it.blackAfter = ""; continue;
						}
					}
					const nx = items[i + 1];
					const hasCloser = nx && nx.type === "tag" && !nx.parse?.primary && /^\s*\]/.test(nx.text ?? "");
					if (hasCloser) {
						const def = String(it.blackAfter ?? "").replace(/^[\s:]+/, "").trim();
						const continuation = String(nx.blackAfter ?? "").trim();
						// SOME writers put the ANCHOR term INSIDE the marker bracket, before the sub-tag:
						// "become [obsolete [rollover definition: no longer in use] ]" (SSFUN07) — here the
						// marker's own text is "obsolete [rollover definition:". Recover that leading term
						// (the part before the first "[") so it is neither LOST nor mis-anchored on the
						// preceding word; it becomes the wrapped anchor. ENGC201's "[hovertrigger:" has no
						// leading term → "" → the anchor stays the preceding black word (structure 1).
						const inMarkerAnchor = String(it.text ?? "")
							.replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "")
							.split("[")[0].trim();
						nx.type = "black"; nx.text = ""; nx.blackAfter = "";   // consume the "]" closer
						const tail = (def ? `${def}` : "") + (continuation ? ` ${continuation}` : "");
						const host = items[i - 1];
						const anchorPrefix = inMarkerAnchor ? ` ${inMarkerAnchor}` : "";   // recovered in-marker term sits right before the sentinel
						if (host && host.type === "black") {
							host.text = String(host.text ?? "").replace(/\s+$/, "") + anchorPrefix + tail;
							it.type = "black"; it.text = ""; it.blackAfter = "";
						} else if (host && host.type === "tag") {
							host.blackAfter = String(host.blackAfter ?? "").replace(/\s+$/, "") + anchorPrefix + tail;
							it.type = "black"; it.text = ""; it.blackAfter = "";
						} else {
							// no usable anchor host — keep the continuation (drop the definition: no anchor)
							it.type = "black"; it.text = continuation; it.blackAfter = "";
						}
						continue;
					}
					// no "]" closer → a BARE standalone marker: fall back to the safe default (re-expose
					// its own text as free body so it cannot swallow the rest of the page).
					it.type = "black"; it.text = it.blackAfter ?? ""; it.blackAfter = ""; continue;
				}
				// wordSelect/highlight: the text after the marker IS body content — keep it (unchanged).
				it.type = "black";
				it.text = it.blackAfter ?? "";
				it.blackAfter = "";
				continue;
			}

			const bankEntry = bank.interactives[type] ?? null;
			// null/missing flag → unknown widget → headings terminate (safe)
			let headingTerminates = bankEntry ? bankEntry.heading_is_terminator !== false : true;
			// A carousel/slideshow's slide TITLES are [H#] headings that live INSIDE the widget; if
			// left at the boundary bank's default of heading_is_terminator:true, capture would stop
			// dead at the first slide title — no carousel would ever get built, and every slide would
			// be orphaned as separate content instead. Force false for these slideshow types
			// specifically, so slide titles are captured as part of the widget; the LONE
			// SECTION-BREAK HEADING rule further below still correctly bounds a REAL section heading
			// that comes after the whole carousel. Data member_rule.slideshow_heading_internal;
			// env CARSLIDE_OFF.
			if ((bank._meta.member_rule.slideshow_heading_internal ?? []).includes(type)
				&& !(typeof process !== "undefined" && process.env && process.env.CARSLIDE_OFF)) {
				headingTerminates = false;
			}

			const bundle = {
				type, canonTag,
				// pre-fold widget VARIANT (e.g. rotateBanner before it folds to carousel) so a
				// shared parent builder can branch on the sub-form the writer used.
				variant: this.#resolveWidgetType(canonTag, it.parse.primary?.alias, normaliser),
				modifier: this.#modifierFor(it),
				activityId: null, headingText: "",
				openerItems: [], memberItems: [], tables: [],
				instructions: [], media: [], redFlags: [],
				positionContext: lastContext,
				startIndex: i, endIndex: i + 1,
			};
			if (!bankEntry) {
				bundle.redFlags.push(`Widget type "${type}" has no boundary-bank entry — heading-terminates default applied.`);
			}

			// ---- openers: walk BACK to the [Activity N] wrapper -----------
			// The widget belongs to the nearest preceding [Activity] whose
			// run reaches here without an intervening terminator. Crucially
			// (OSAI301 1A fix), the cv2 box must hold ONLY the widget + its
			// data: the activity wrapper, its title, and its instruction
			// [body] stay OUTSIDE the box as activity-level content, and any
			// content ABOVE the [activity] tag (e.g. a section [body] +
			// [video]) is never touched. So the lookback stops AT the
			// [activity] tag and records it as the bundle's owner; it does
			// not slurp the activity's lead body into the box.
			let s = i - 1;
			let activityIdx = -1;
			while (s >= 0) {
				const prev = items[s];
				if (prev.consumedBy !== undefined) break;
				if (prev.type === "tag" && prev.parse.tags.some((t) => t.tag === "activity")) {
					activityIdx = s; break;                 // found the owner
				}
				// cross the activity's own heading / lead body / media —
				// these sit between [Activity] and the widget tag — but a
				// terminator or a NON-opener tag stops the walk
				if (prev.type === "black") { s--; continue; }
				if (prev.type === "tag" && (!prev.parse.primary || openerTags.has(prev.parse.primary?.tag))
					&& prev.parse.primary?.tag !== "activity") { s--; continue; }
				break;
			}

			if (activityIdx >= 0) {
				// the bundle is OWNED by an activity: the converter renders
				// the activity wrapper + everything between it and the widget
				// as activity-level content, then the cv2 box (widget + data)
				// nested inside. Mark the activity + in-between items so the
				// converter knows this range is one activity unit.
				bundle.activityOwner = items[activityIdx];
				bundle.activityLeadItems = items.slice(activityIdx + 1, i); // title/body/media before the widget
				bundle.activityId = items[activityIdx].parse.numbers[0]?.toUpperCase() ?? bundle.activityId;
				bundle.startIndex = activityIdx;
				bundle.openerItems = [];   // nothing goes INSIDE the box from the openers
			} else {
				// no activity wrapper (inline widget) — box starts at the tag
				bundle.openerItems = [];
				bundle.startIndex = i;
			}

			// capture the activity id + heading from the openers
			for (const op of bundle.openerItems) {
				if (op.type !== "tag") continue;
				const tag = op.parse.primary?.tag;
				if (tag === "activity" && op.parse.numbers.length) {
					bundle.activityId = op.parse.numbers[0].toUpperCase();
				}
				if (tag === "activity heading" || tag === "heading") {
					// original-case: embedded payload first, following text second
					bundle.headingText = (normaliser.RenderText(op.text) || op.blackAfter).trim();
				}
			}
			// id may also ride on the interactive tag itself ([Activity 7 drag and
			// drop]) — but ONLY when the span genuinely carries the [Activity] tag.
			// A widget's own trailing number ([Flipcard 1], [Accordion 2]) is a
			// PANEL index, not an activity id, and must not enable cross-widget
			// absorption (the XGF9001 over-capture: flipCard "1" → swallowed the page).
			if (!bundle.activityId && it.parse.numbers.length
				&& it.parse.tags.some((t) => t.tag === "activity")) {
				bundle.activityId = it.parse.numbers[0].toUpperCase();
			}

			// the interactive tag's own trailing text is learner-facing
			// content for the widget (or an embedded instruction — both are
			// members; instruction detection happens per-member below)
			this.#collectMember(bundle, it, run);

			// ---- members: walk FORWARD until a terminator -----------------
			bundle.endIndex = this.#swallowMembers(bundle, items, i + 1, headingTerminates, absolute, run, normaliser);
			// TRAILING-MEDIA FIX: a [video]/[audio] the writer placed AFTER the
			// widget's content was swallowed as a member, but the human renders it
			// as its OWN element. Trim it back out so the normal converter path
			// emits it standalone (data: BoundaryBank._meta.member_rule.trailing_media_extract).
			bundle.endIndex = this.#trimTrailingMedia(bundle, bundle.endIndex);
			// BACKWARD LEAD-PAIR ABSORB. The forward scan that captures members always starts at the
			// FIRST interactive tag, so a REPEATING (lead-in label, widget) series always loses its
			// very first label — it sits ABOVE (before) the tag, outside the scanned range. Having
			// captured the members, detect the clean widget-first alternation pattern and walk back UP
			// through the preceding items to recover that missed leading label (this extends
			// startIndex backward; the ownership-marking loop below then consumes it along with
			// everything else). See #absorbLeadingPattern for the full explanation. Data
			// member_rule.leading_pattern_absorb; env INTLEADPAIR_OFF.
			this.#absorbLeadingPattern(bundle, items, i);
			// BACKWARD SAME-BLOCK AVATAR ABSORB (round 246). A speech bubble the writer typed as
			// ONE PARAGRAPH — "[Image] <words> <title> [LINK: iStock url] [speech bubble] <text>" —
			// splits into separate red-span ITEMS, so the [image] sits just ABOVE the invocation and
			// outside the bundle. Recover it (same source BLOCK only) so the builder can emit the
			// human's one-row avatar+bubble instead of a loose image followed by a hand-off box.
			// See #absorbSameBlockImage. Data member_rule.same_block_image_absorb; env SBNOTBL_OFF.
			this.#absorbSameBlockImage(bundle, items, i);
			// ROUND 217 (Chris, boundary audit): a BARE GENERIC INVOCATION bundle — the
			// standalone "[Interactive]" re-tag (Tag_Lexicon qualifier_alias_demote.
			// standalone_becomes) — that captured NOTHING AT ALL (no forward members, no
			// backward absorb, no learner text on its own opener) DISSOLVES here rather
			// than shipping an EMPTY dashed placeholder box: the item is left unconsumed
			// and flows down the ordinary unhandled-tag path (a gate-neutral cv2 note —
			// the pre-217 rendering for these spans was an instruction note too). Without
			// this, the 217 alias re-tag pushed body_compare's EMPTY-container count up
			// (+7 pages) for exactly the bare spans whose invocation names a widget but
			// whose content the walk could not reach. A bundle that captured ANYTHING
			// (AGH1001-01: instruction line + data table) is untouched.
			// Data member_rule.bare_invocation_dissolve_empty; rides env INTALIAS_OFF.
			// A bundle is "too thin" when it captured NO data table and under
			// min_member_chars of member text (mirrors body_compare's 40-char
			// EMPTY-container threshold) — nothing buildable was specified, so the
			// items are left unconsumed: a captured [image]/media member then renders
			// down its NORMAL standalone path (visible Mode P/D placeholder) and the
			// invocation itself down the unhandled-tag/note path — both the pre-217
			// forms. A TABLE member always keeps the bundle (the table IS the
			// buildable widget data, however short its text).
			const _bid = DataService.Data.BoundaryBank._meta.member_rule.bare_invocation_dissolve_empty;
			if (_bid && _bid.enabled !== false && (_bid.types ?? []).includes(bundle.type)) {
				let _chars = 0;
				for (const m of (bundle.memberItems ?? [])) {
					// count the RENDERED length: the writer's **bold**/*italic* markers
					// are formatting, not content (ANZH203-06's 38-char bold title read
					// as 42 raw and dodged the threshold)
					_chars += (((m.type === "black" ? m.text : m.blackAfter) ?? "")
						.replace(/\*/g, "").trim()).length;
				}
				if (!(bundle.tables ?? []).length && _chars < (_bid.min_member_chars ?? 40)) {
					continue;
				}
			}
			// mark ownership so the converter and later scans skip the range
			for (let k = bundle.startIndex; k < bundle.endIndex; k++) {
				items[k].consumedBy = bundles.length;
			}
			bundles.push(bundle);

			i = bundle.endIndex - 1;   // resume at the terminator (loop i++)
		}

		// ── activity numbering ──────────────────────────────────────────
		// Capture the writer's number whether inside the bracket ([Activity 1A],
		// 71% of templates) or just outside it ([Activity] 1A, ~1%); then ensure
		// per-page uniqueness in document order — ~30% of modules reuse a number
		// and the human developers renumber sequentially (a second 1A → 1B).
		const seenAct = new Set();

		// ── BILINGUAL activity-number assignment (reoMode only) ──
		// The bilingual activity NUMBER is a table ROW ("Activity 1A:" / "Ngohe 1A:") inside
		// the English|Māori content table, NOT an [Activity N] TAG, so the opener-lookback
		// above never set activityId for these widgets. Walk the items in order, track the
		// most recent activity-number row, and hand it to the FIRST following widget bundle
		// (claimed-per-row → one number = one box; a second bundle before the next row stays
		// inline, matching the finished page's single box per activity). Sets bundle.activityId +
		// bundle.reoActivity; ContentConverter's bundle path then opens the wrapper (reoAct).
		// Runs BEFORE the standard uniqueness loop so a stray standard id renumbers around it.
		// Data activity_wrapper.reo_bundle_activity; env REOACT_OFF. reoMode-scoped → standard
		// (non-bilingual) modules — where "Activity NX:" text can also coincidentally appear, e.g.
		// ENGS302 — are byte-identical either way.
		// The OVERVIEW page is the tabbed menu, NEVER lesson activities — the finished pages ship
		// ZERO div.activity on every bilingual overview page (measured). So even when the page
		// splitter (which does not yet handle this case perfectly) spills lesson content onto the
		// overview, no activity wrapper is built there — doing so would pollute the menu page.
		const _reoActCfg = DataService.Data.EmitTemplates?.activity_wrapper?.reo_bundle_activity;
		const _reoActOn = reoMode && !page.isOverview && !!_reoActCfg && _reoActCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.REOACT_OFF);
		if (_reoActOn) {
			const startMap = new Map();
			for (const b of bundles) if (!startMap.has(b.startIndex)) startMap.set(b.startIndex, b);
			let lastNum = null, claimed = true;
			for (let idx = 0; idx < items.length; idx++) {
				if (items[idx].type === "table") {
					const n = this.#reoActivityNum(items[idx].block);
					if (n) { lastNum = n; claimed = false; }
				}
				const b = startMap.get(idx);
				if (b && !b.activityId && lastNum && !claimed && b.canonTag !== "activity") {
					let id = lastNum;
					while (seenAct.has(id)) id = this.#nextActivityId(id);
					b.activityId = id; b.reoActivity = true; seenAct.add(id);
					claimed = true;   // one number → one box; the next bundle waits for the next row
				}
			}
		}

		for (const b of bundles) {
			if (b.activityOwner === undefined && b.canonTag !== "activity") continue;
			let id = b.activityId;
			if (!id && b.activityOwner) {
				const m = (b.activityOwner.text || "").match(/activit(?:y|ies)\b[^a-z0-9]*#?\s*(\d+\s*[a-z]?)/i);
				if (m) id = m[1].replace(/\s+/g, "").toUpperCase();
			}
			if (!id) continue;
			while (seenAct.has(id)) id = this.#nextActivityId(id);
			seenAct.add(id);
			b.activityId = id;
		}
		return bundles;
	};

	/**
	 * Swallows members forward from startJ until the first terminator
	 * (the bank's member_rule: membership = "not a terminator"). Shared by
	 * the normal interactive path and the unclassified-activity path.
	 *
	 * @returns {number} endIndex — the item range consumed is [.., endIndex)
	 */
	/**
	 * Is this a bilingual `English|Māori` CONTENT table? (Mirrors the same check in
	 * BilingualBuilder.bilingualHeader: row-0 col-0 reads roughly "english", row-0 col-1 reads
	 * roughly "māori|te reo".) Such a table is the writer's reo/eng PROSE — never a widget, even
	 * when a body cell embeds an `[Interactive] [X]` reference — so `#interactiveInTable` must NOT
	 * capture it; it unfolds separately via `BilingualBuilder.bilingualTable` instead. This file has
	 * no access to the shared `Utils` helper class, so text folding for comparison (stripping
	 * `*`/red-marker/`🔴`/extra spaces) is done inline here rather than via Utils.Fold.
	 *
	 * @param {Object} block - a table block (block.rows = array of row arrays of cell text)
	 * @returns {boolean}
	 */
	static #bilingualContentTable(block) {
		const cfg = DataService.Data.EmitTemplates?.elements?.dual_language;
		const rows = block?.rows ?? [];
		if (!rows.length || !Array.isArray(rows[0]) || rows[0].length < 2) return false;
		const fold = (s) => String(s ?? "")
			.replace(/\u{1f534}|\[\/?RED TEXT\]|\*/gu, "").toLowerCase().trim();
		return new RegExp(cfg?.header_english || "english", "i").test(fold(rows[0][0]))
			&& new RegExp(cfg?.header_maori || "māori|maori|te reo", "i").test(fold(rows[0][1]));
	};

	/**
	 * Does this table OPEN a bilingual SECTION (a `[H1] N.M` decimal sub-section number, e.g.
	 * 1.1 / 2.3)? Mirrors `BilingualBuilder.bilingualSectionNum`. A widget bundle must TERMINATE
	 * at one, so it never swallows the next section's heading into itself (which would produce an
	 * over-extended activity box covering more than one section). Robust to `**bold**` /
	 * `🔴[RED TEXT]` cell markers.
	 *
	 * @param {Object} block - a table block
	 * @returns {boolean}
	 */
	static #sectionOpenerRe = /\[\s*h1\s*\]\s*\d+\.\d+/i;
	static #bilingualSectionOpener(block) {
		const rows = block?.rows ?? [];
		if (!rows.length || !Array.isArray(rows[0]) || rows[0].length < 2) return false;
		const strip = (s) => String(s ?? "").replace(/🔴|\[\/?RED TEXT\]|\*/g, "");
		for (let r = 0; r < Math.min(rows.length, 3); r++)
			for (const c of (rows[r] || []))
				if (InteractiveScanner.#sectionOpenerRe.test(strip(c))) return true;
		return false;
	};

	/**
	 * Is this tag item a standalone RED "Phase N" fundamentals phase delimiter? (No resolved
	 * primary tag, class noise/instruction, ENTIRE folded text matching the phase_text
	 * delimiter_pattern, on a fundamentals single-file module.) Some fundamentals-style modules
	 * mark where one "phase" of the lesson ends and the next begins using plain red text like
	 * "Phase 2" rather than a bracketed tag. Used by #swallowMembers (which has no access to this
	 * method's enclosing scope, so it calls it directly) as a HARD member-walk terminator — the red
	 * twin of terminators_absolute_text (never a member of any widget, always ends capture). Data
	 * fundamentals_panels.phase_text.red_delimiter (+ scanner_hard_terminator); env
	 * FUNPANRED_OFF.
	 *
	 * This method ALSO accepts a second, BRACKETED phase-boundary OPENER shape used by a different
	 * family of modules: "[Phase one content begins]"/"[Start of phase two content]" — without this,
	 * a widget such as an engagement quiz could swallow the next phase's opener bracket, trapping
	 * the phase boundary marker inside the widget's captured content instead of letting it end the
	 * widget. OPENER pattern only — the matching CLOSER form ("[End of Phase One]") never needs this
	 * same protection (a widget never tries to consume it); the call site's !primary guard already
	 * excludes closers anyway, since they resolve to "end other"/"end page" directives rather than
	 * a plain red span. Data fundamentals_panels.phase_text.bracketed_delimiter
	 * (+ scanner_hard_terminator); env FUNPANBRACKET_OFF.
	 *
	 * @param {Object} it - a page item (item.type, item.parse)
	 * @param {ConversionRun} run - for resolvedRules.body_class / page_model
	 * @returns {boolean}
	 */
	static #redPhaseDelimiter(it, run) {
		const fp = DataService.Data.EmitTemplates?.body_region?.fundamentals_panels?.phase_text;
		if (!fp) return false;
		if (typeof process !== "undefined" && process.env && process.env.FUNDPHASE_OFF) return false;
		if (!/(^|\s)fundamentals(\s|$)/.test(run?.resolvedRules?.body_class || "")) return false;
		if (run?.resolvedRules?.page_model !== "single-file") return false;
		if (!(it.parse?.class === "noise" || it.parse?.class === "instruction")) return false;
		const folded = (it.parse?.folded ?? "").trim();
		const rd = fp.red_delimiter;
		if (rd && rd.enabled !== false && rd.scanner_hard_terminator !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FUNPANRED_OFF)
			&& new RegExp(fp.delimiter_pattern || "^phase\\s+\\d+$", "i").test(folded)) return true;
		const br = fp.bracketed_delimiter;
		if (br && br.enabled !== false && br.scanner_hard_terminator !== false && br.opener_pattern
			&& !(typeof process !== "undefined" && process.env && process.env.FUNPANBRACKET_OFF)
			&& new RegExp(br.opener_pattern, "i").test(folded)) return true;
		return false;
	};

	/**
	 * ACCORDION-AS-PHASES: which suppressed FORM is this item, or null when this behaviour isn't
	 * gated on for the current module? Some modules author their whole lesson as ONE [Accordion]
	 * widget with numbered [Accordion N] panels — but the FINISHED page presents those panels as
	 * fundamentals "phases" chrome (a phases nav + one panel per phase), never as a built accordion
	 * widget. The tricky part: these accordion tags are normally CONSUMED into a widget bundle by
	 * the scanner (unlike the other phase-delimiter shapes above, which are always left unconsumed),
	 * so the scanner must be told NOT to bundle them at all on a gated module.
	 * Gate = data flag + env + fundamentals body_class + single-file page + a registry row (see
	 * #accordionPhaseRow) restricting this to specific module families — because numbered
	 * [Accordion N] is ALSO the ordinary, standard way many OTHER (non-fundamentals) modules author
	 * a genuine, real accordion widget, so this suppression must never fire for those.
	 * Returns one of three forms: "break" = a numbered invocation, i.e. a PHASE BOUNDARY (a later
	 * pre-pass turns it into a phase-break marker; it's also treated as a HARD member-walk
	 * terminator here so no other widget bundle can swallow it), "noop" = the bare [accordion]
	 * opener with no number (a later pre-pass simply consumes and discards it), "dissolve" = any
	 * other accordion-primary form, such as the writer's own "[link to this section of the
	 * accordion menu]" cross-link — left unconsumed so a later pre-pass can dissolve it back into
	 * ordinary prose (re-exposing its blackAfter text). Data
	 * fundamentals_panels.phase_text.accordion_delimiter; env FUNPANACC_OFF
	 * (FUNDPHASE_OFF reverts the whole phase-text machinery, not just this suppression).
	 *
	 * @param {Object} it - a page item (item.type, item.parse)
	 * @param {ConversionRun} run - for resolvedRules.body_class / page_model / moduleCode
	 * @returns {"break"|"noop"|"dissolve"|null}
	 */
	/**
	 * Is this INTERACTIVE invocation actually the MTK bilingual template's
	 * "[Content for DROP DOWN MENU]" module-menu marker (ROUND 212 — the
	 * PNR101/102/104 family)? The marker resolves to the "dropdown" widget tag,
	 * but it introduces the module MENU table, not a widget: a bundle opened
	 * here would capture that table into a placeholder and the menu would never
	 * be built. Gated to bilingual (reoTranslate / TRR / PNR-prefix) modules
	 * whose opener is DIRECTLY followed by a TABLE item (the PNR shape) — a
	 * real "[dropdown]" widget on any other module, and the paragraph-form
	 * TRR203/TRR301 siblings (their menu content is loose paragraphs, not a
	 * table — a separate follow-up class), are completely unaffected.
	 * Data: elements.dual_language.dropdown_menu. Env toggle: REODROPMENU_OFF.
	 *
	 * @param {Object[]} items - the page's item stream
	 * @param {number} i - index of the tag item (primary directive INTERACTIVE)
	 * @param {ConversionRun} run - module identity + resolved rules
	 * @returns {boolean} true = suppress (not a widget; leave unconsumed)
	 */
	static #dropdownMenuMarker(items, i, run) {
		const dl = DataService.Data.EmitTemplates?.elements?.dual_language;
		const cfg = dl?.dropdown_menu;
		if (!cfg || cfg.enabled === false || dl.enabled === false) return false;
		if (typeof process !== "undefined" && process.env && process.env.REODROPMENU_OFF) return false;
		if (items[i + 1]?.type !== "table") return false;   // the PNR table shape only
		const _mtkArm = dl.use_mtk_flag === true
			|| !!(typeof process !== "undefined" && process.env && process.env.MTKREO_OFF);
		const reo = /reoTranslate/i.test(run?.resolvedRules?.body_class || "")
			|| (_mtkArm && !!run?.mtkFlag)
			|| (dl.code_prefixes || []).some((p) =>
				String(run?.moduleCode || "").toUpperCase().startsWith(String(p).toUpperCase()));
		if (!reo) return false;
		return new RegExp(cfg.opener_pattern ?? "^\\[content for drop[ -]?down menu\\]$", "i")
			.test((items[i].parse?.folded ?? "").trim());
	};

	static #accordionPhaseForm(it, run) {
		const acc = DataService.Data.EmitTemplates?.body_region?.fundamentals_panels?.phase_text?.accordion_delimiter;
		if (!acc || acc.enabled === false || acc.scanner_suppress === false) return null;
		if (typeof process !== "undefined" && process.env
			&& (process.env.FUNPANACC_OFF || process.env.FUNDPHASE_OFF)) return null;
		if (it.type !== "tag" || it.parse?.primary?.tag !== (acc.tag || "accordion")) return null;
		if (!/(^|\s)fundamentals(\s|$)/.test(run?.resolvedRules?.body_class || "")) return null;
		if (run?.resolvedRules?.page_model !== "single-file") return null;
		if (!InteractiveScanner.#accordionPhaseRow(acc, run)) return null;
		const folded = (it.parse?.folded ?? "").trim();
		if (new RegExp(acc.numbered_pattern || "^\\[accordion\\s+\\d+\\]$", "i").test(folded)) return "break";
		if (new RegExp(acc.bare_pattern || "^\\[accordion\\]$", "i").test(folded)) return "noop";
		return "dissolve";
	};

	/** The accordion_delimiter registry row for this run, or null. Looks the module up by its exact
	 *  code first (a per-module "series" override), then falls back to its subject+phase group — the
	 *  same two-tier lookup shape used elsewhere for per-family registry data. */
	static #accordionPhaseRow(acc, run) {
		const reg = acc.registry || {};
		if (reg.series && reg.series[run?.moduleCode]) return reg.series[run.moduleCode];
		const subj = (run?.moduleCode || "").match(/^[A-Za-z]+/)?.[0] || "";
		const rawPhase = run?.resolvedRules?.template_phase ?? "";
		const phase = DataService.Data.EmitTemplates.skeleton?.template_attr_map?.[rawPhase] ?? rawPhase;
		const lk = `${subj}|${phase}`.toLowerCase();
		const hit = Object.keys(reg.groups || {}).find((k) => k.toLowerCase() === lk);
		return hit ? reg.groups[hit] : null;
	};

	/** reoMode for a run (mirrors the scan-time flag) — used by #swallowMembers, which has no closure. */
	static #reoModeFor(run) {
		const cfg = DataService.Data.EmitTemplates?.elements?.dual_language;
		// The MTK house header is honoured as a bilingual signal only when data explicitly says
		// use_mtk_flag:true, or the env var MTKREO_OFF=1 forces the older, more permissive
		// behaviour back on (see PageSplitter for why the header alone isn't trusted by default).
		const _mtkArm = (!!cfg && cfg.use_mtk_flag === true)
			|| !!(typeof process !== "undefined" && process.env && process.env.MTKREO_OFF);
		return !!cfg && cfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.REOTRANSLATE_OFF)
			&& (/reoTranslate/i.test(run?.resolvedRules?.body_class || "") || (_mtkArm && !!run?.mtkFlag)
				|| (cfg.code_prefixes || []).some((p) => String(run?.moduleCode || "").toUpperCase().startsWith(String(p).toUpperCase())));
	};

	/**
	 * The bilingual activity NUMBER ("1A") carried in a table's "Activity NX:" / "Ngohe NX:" label
	 * row, or null. The number is digit(s) + a single letter followed by a colon (the writer's
	 * label form); ordinary prose mentioning "activity" without that digit+letter+colon shape never
	 * matches.
	 *
	 * @param {Object} block - a table block
	 * @returns {string|null}
	 */
	static #reoActivityNum(block) {
		const text = (block && block.text) || "";
		const m = /\b(?:activity|ngohe)\s*([0-9]+\s*[A-Za-z])\s*:/i.exec(text);
		return m ? m[1].replace(/\s+/g, "").toUpperCase() : null;
	};

	/** Next activity number on a collision: 1A → 1B; "1" → "1A". */
	static #nextActivityId(id) {
		const m = id.match(/^(.*?)([A-Za-z])$/);
		return m ? m[1] + String.fromCharCode(m[2].toUpperCase().charCodeAt(0) + 1) : id + "A";
	};

	static #swallowMembers(bundle, items, startJ, headingTerminates, absolute, run, normaliser = null) {
		let j = startJ;
		for (; j < items.length; j++) {
			const next = items[j];

			if (next.type === "table") {           // content_data — usually a member
				// reoMode SECTION boundary: a `[H1] N.M` decimal section-opener table starts a NEW
				// section box (BilingualBuilder.bilingualSection), so a widget bundle must STOP here
				// and never swallow the next section's heading/prose into itself (which would produce
				// an over-extended activity box spanning more than one section). Gated by the
				// section_grouping flag + env REONEST_OFF.
				const _scfg = DataService.Data.EmitTemplates?.elements?.dual_language?.section_grouping;
				if (_scfg && _scfg.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.REONEST_OFF)
					&& InteractiveScanner.#reoModeFor(run) && InteractiveScanner.#bilingualSectionOpener(next.block)) break;
				// A following TABLE whose cell carries a DIRECT DIFFERENT-type display-terminator
				// invocation is a NEW section, not this widget's data. For example, a table-authored
				// [speechbubble] could otherwise get trapped inside the current activity by the
				// "table is always a member" swallow rule below; terminate here instead, so the main
				// loop's #interactiveInTable opens it as its own separate free-body bundle. DIRECT
				// invocation only — this deliberately does NOT use the looser face-tag inference from
				// #interactiveInTable below, so ordinary face/data tables are left untouched.
				// Env ACTSPLIT_OFF.
				const mrT = DataService.Data.BoundaryBank._meta.member_rule;
				if (mrT.same_activity_display_terminates && normaliser
					&& !(typeof process !== "undefined" && process.env && process.env.ACTSPLIT_OFF)) {
					const ct = this.#tableDirectInvocation(next.block, normaliser);
					if (ct && ct !== bundle.type && (mrT.display_terminator_types ?? []).includes(ct)) break;
				}
				// A MEMBER-based flipCard must TERMINATE at a FOLLOWING table that is itself a
				// DIFFERENT-type display widget (e.g. a [speech bubble] authored as a table, appearing
				// right after a set of flip cards) instead of absorbing it as more of its own data — an
				// absorbed table like that makes the member-card builder bail out to a plain
				// placeholder instead of building the cards. Uses the table's DIRECT invocation, so a
				// plain card-DATA table (an ordinary [back]/[front] face-data table, which is NOT a
				// display widget) is still absorbed as normal. Scoped to listed types. Data
				// member_rule.table_display_terminates_types; env FLIPTBL_OFF.
				if (normaliser && (mrT.table_display_terminates_types ?? []).includes(bundle.type)
					&& !(typeof process !== "undefined" && process.env && process.env.FLIPTBL_OFF)) {
					const ct2 = this.#tableDirectInvocation(next.block, normaliser);
					if (ct2 && ct2 !== bundle.type && (mrT.display_terminator_types ?? []).includes(ct2)) break;
				}
				// A member-based CAROUSEL/slideshow must LIKEWISE TERMINATE at a FOLLOWING table that
				// is itself a DIFFERENT-type DISPLAY widget (e.g. a [speech bubble] authored as a table,
				// appearing right after a run of slides) instead of ABSORBING it. Absorbing a
				// display-table like that makes the carousel builder bail to a placeholder AND denies
				// the speech bubble its own separate bundle (the carousel would run right past its last
				// slide into the next, unrelated widget). Same mechanism as the flipCard guard just
				// above, scoped to the slideshow types (which never use a data table themselves), so a
				// plain image/video carousel is unaffected and the main loop's #interactiveInTable opens
				// the table as its own free-body bundle. The writer tagged TWO separate widgets and the
				// finished page builds two — the writer's tag corresponds to the finished element. Data
				// member_rule.table_display_terminates_types_slideshow; env CARTBL_OFF.
				if (normaliser && (mrT.table_display_terminates_types_slideshow ?? []).includes(bundle.type)
					&& !(typeof process !== "undefined" && process.env && process.env.CARTBL_OFF)) {
					const ct3 = this.#tableDirectInvocation(next.block, normaliser);
					if (ct3 && ct3 !== bundle.type && (mrT.display_terminator_types ?? []).includes(ct3)) break;
				}
				// NUMBERED-SERIES CONTAINMENT (ROUND 214, Chris — OSOH501-01 panel 4). Inside a
				// numbered-series host, a member TABLE that itself carries a DIFFERENT-type
				// interactive invocation (the [Click drop] values table typed inside the last
				// [Accordion 4] panel) becomes a NESTED sub-bundle — rendered in place inside the
				// panel (built when its builder succeeds, else an honest nested placeholder)
				// instead of arriving as a foreign data table that bails the host's rich build.
				// Same gating + data as the tag form above (member_rule.numbered_series_absorb);
				// requires a REAL series already captured (>= min_panels numbered tags). Env ACCNEST_OFF.
				const serCfg = mrT.numbered_series_absorb;
				if (normaliser && serCfg && serCfg.enabled !== false
					&& (serCfg.hosts ?? []).includes(bundle.type)
					&& !(typeof process !== "undefined" && process.env && process.env.ACCNEST_OFF)) {
					const ctN = this.#tableDirectInvocation(next.block, normaliser);
					if (ctN && ctN !== bundle.type) {
						const numReT = new RegExp(
							(serCfg.numbered_pattern ?? "\\[\\s*{type}\\s+\\d+").replace("{type}", bundle.type), "i");
						const nPanels = [...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])]
							.filter((m) => m && m.type === "tag" && m.parse?.primary?.tag === bundle.type
								&& numReT.test(String(m.text ?? ""))).length;
						if (nPanels >= (serCfg.min_panels ?? 2)) {
							const sub = {
								type: ctN, canonTag: ctN, modifier: null,
								activityId: null, headingText: "",
								openerItems: [], memberItems: [], tables: [],
								instructions: [], media: [], redFlags: [],
								positionContext: bundle.positionContext,
								startIndex: j, endIndex: j + 1, nested: true,
							};
							this.#collectMember(sub, next, run);
							sub.tables.push(next.block);
							bundle.memberItems.push({ type: "nested", nestedBundle: sub });
							(bundle.nestedBundles ??= []).push(sub);
							run.AddNote("info", "InteractiveScanner",
								`${bundle.type}: nested [${ctN}] table absorbed as a sub-bundle; host continues.`);
							continue;
						}
					}
				}
				bundle.tables.push(next.block);
				bundle.memberItems.push(next);
				continue;
			}
			if (next.type === "black") {           // free_text_content
				// A standalone "Phase N" line (a fundamentals PHASE BOUNDARY used by one family of
				// modules) is a HARD terminator: it is never a widget member, so a quiz or other widget
				// at the end of a phase must not swallow the next phase's delimiter and content along
				// with it (that family's own "[end quiz]" closer resolves to "end mcq", which is not an
				// absolute terminator on its own). Data-driven text terminators; env FUNDPHASE_OFF
				// reverts (the line is swallowed again, as a plain member).
				const _absTxt = DataService.Data.BoundaryBank._meta.member_rule.terminators_absolute_text ?? [];
				if (_absTxt.length && !(typeof process !== "undefined" && process.env && process.env.FUNDPHASE_OFF)) {
					const _bt = String(next.text || "").trim();
					if (_bt && _absTxt.some((re) => new RegExp(re, "i").test(_bt))) break;
				}
				bundle.memberItems.push(next);
				this.#harvestMedia(bundle, next);
				continue;
			}

			const p = next.parse.primary;
			// A standalone RED "Phase N" span (no primary tag, class noise/instruction, ENTIRE
			// folded text matching the phase_text delimiter_pattern) is a fundamentals PHASE
			// BOUNDARY: a HARD terminator, never a member — the red-text twin of the BLACK-line
			// terminators_absolute_text check above (without this, some phase-boundary spans were
			// getting swallowed into widget bundles, so those phases never opened as their own
			// content). Gated to fundamentals body_class + single-file + the data flag. Data
			// fundamentals_panels.phase_text.red_delimiter; env FUNPANRED_OFF.
			if (!p && this.#redPhaseDelimiter(next, run)) break;
			// A suppressed numbered/bare accordion invocation is a fundamentals PHASE BOUNDARY on
			// a gated page (accordion-as-phases): a HARD terminator, never a member — no bundle may
			// swallow a phase delimiter (the same principle as the other phase-delimiter checks
			// above; scanner_hard_terminator). The "dissolve" link form is NOT a boundary and keeps
			// the default member handling. Data fundamentals_panels.phase_text
			// .accordion_delimiter; env FUNPANACC_OFF.
			if (p?.directive === "INTERACTIVE"
				&& (DataService.Data.EmitTemplates?.body_region?.fundamentals_panels?.phase_text
					?.accordion_delimiter?.scanner_hard_terminator !== false)) {
				const _accForm = this.#accordionPhaseForm(next, run);
				if (_accForm === "break" || _accForm === "noop") break;
			}
			// INSTRUCTION-DOMINANT span: a writer instruction that happens to name-drop tag-words
			// (e.g. "...reset button at the end of this activity") can get misread as a phantom tag.
			// Inside an open bundle it must NOT terminate the walk (which would orphan the widget's
			// following data table, leaving it stranded outside the widget) nor render as a phantom
			// button — swallow it as an instruction MEMBER instead. Scoped to this member walk only;
			// classification elsewhere in the pipeline is unchanged.
			// Data member_rule.instruction_dominant_member; env INSTRDOM_OFF.
			const _mrID = DataService.Data.BoundaryBank._meta.member_rule;
			if (normaliser && (_mrID.instruction_dominant_member ?? false)
				&& !(typeof process !== "undefined" && process.env && process.env.INSTRDOM_OFF)
				&& normaliser.IsInstructionDominant(next.parse, _mrID.instruction_dominant_min_words ?? 8)) {
				// BRIDGE-TO-DATA ONLY: swallow the instruction (the answer-key / randomise note)
				// solely when it sits right before the widget's DATA TABLE (a uses_data_table widget) —
				// so the fix bridges the widget to its table (ENGS302 1A) but can NEVER extend a bundle
				// across an instruction into FREE PROSE the human keeps (no over-capture).
				const _entryID = DataService.Data.BoundaryBank.interactives[bundle.type];
				const _nextTable = items[j + 1] && items[j + 1].type === "table" && items[j + 1].consumedBy === undefined;
				if (_entryID?.uses_data_table && _nextTable) {
					this.#collectMember(bundle, next, run);
					continue;
				}
			}

			// FACE-WIDGET body resumption: a flipCard/speechBubble — whose signature carries
			// front/back and NEVER 'body' — that has ALREADY captured a face treats a following
			// [Body] ELEMENT as the writer RESUMING free body. The finished page keeps that [Body]
			// OUTSIDE the widget (e.g. two flip cards, then separate [Body] text below them). A
			// [Body]-based flip form with NO faces (a module whose card backs are themselves [Body]
			// tags) never trips this, so its [Body] members are preserved as part of the widget.
			// Data: member_rule.body_terminates_after_face.
			const _mrB = DataService.Data.BoundaryBank._meta.member_rule;
			// FACE / REVEAL member terminator (the general form of the rule above). A [Body] ELEMENT
			// after the widget has already captured a FACE/REVEAL member — [front]/[back]/[drop]/
			// [answer] — is the writer RESUMING free body (the finished page keeps it OUTSIDE the
			// widget). Keyed off the CAPTURED member, not the widget's signature, so it also covers a
			// clickDrop's FRONT/DROP reveal form (whose signature does not formally list front/back).
			// A [Body]-BASED form with NO face/reveal member ever captures one → never trips → its
			// [body] members stay content. Data: member_rule.face_member_tags.
			if (_mrB.body_terminates_after_face && p?.tag === "body" && p?.directive !== "INTERACTIVE") {
				const faceTags = _mrB.face_member_tags ?? ["front", "back", "drop", "answer"];
				// For a DATA-TABLE widget, count a face tag only on a genuine captured face MEMBER
				// (a [front]/[back]/[drop]/[answer], which is a SUBTAG), NOT on the widget's OWN
				// invocation, whose MODIFIER words can coincidentally look like a face word (e.g.
				// "[reorder – show answer]" resolves to tags [reorder, answer]). Counting the
				// invocation itself would falsely fire this terminator on the very FIRST following
				// [body], so a data-table widget (reorder/dragAndDrop/…) would capture NOTHING and
				// its data table would leak outside the activity entirely. Genuine face members are
				// SUBTAG; the invocation itself is INTERACTIVE — that's the distinction this checks.
				// SCOPED to uses_data_table widgets: for those, a following table is unambiguously the
				// widget's data (post-table body-termination is handled below by
				// body_terminates_after_table), so suppressing the false face-terminator here cannot
				// over-capture free body; FACE/REVEAL widgets (flipCard/clickDrop/speechBubble) keep
				// their exact original behaviour unchanged. Data member_rule.face_excludes_invocation;
				// env FACEINVOKE_OFF reverts.
				const _entryF = DataService.Data.BoundaryBank.interactives[bundle.type];
				const excludeInvocation = (_mrB.face_excludes_invocation ?? true)
					&& !(typeof process !== "undefined" && process.env && process.env.FACEINVOKE_OFF)
					&& _entryF?.uses_data_table === true;
				// find the MOST-RECENT captured face member
				let recentFace = null;
				for (let k = bundle.memberItems.length - 1; k >= 0; k--) {
					const m = bundle.memberItems[k];
					if (m.type === "tag" && !(excludeInvocation && m.parse?.primary?.directive === "INTERACTIVE")
						&& m.parse?.tags?.some((t) => faceTags.includes(t.tag))) { recentFace = m; break; }
				}
				// An EMPTY face — a [back]/[front] with NO inline content of its own — takes its
				// content from the FOLLOWING [body] ELEMENT(s) instead (a card form like [Front] [H5]
				// title [image] [back] [body], where the title+image ride the front and the back text
				// is a separate following [body]). That [body] IS the face's content, not a free-body
				// section break, so keep capturing while the most-recent face is still empty (its
				// content is still arriving). A face that already carries inline content, followed by
				// a SEPARATE free [body], still terminates as described above. Data
				// member_rule.face_empty_keeps_body; env FACEBODY_OFF.
				const faceKeepsBody = recentFace
					&& !String(recentFace.blackAfter ?? "").replace(/\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu, "").trim()
					&& (_mrB.face_empty_keeps_body ?? true)
					&& !(typeof process !== "undefined" && process.env && process.env.FACEBODY_OFF);
				if (recentFace && !faceKeepsBody) break;   // [Body] resumes free body after a CONTENT-carrying face member
			}

			// SELF-CAPTIONED widget (speechBubble): the bubble TEXT rides on the widget's OWN
			// invocation ([speech bubble] <text>), not in a [front]/[back] face or a data table — so a
			// [Body] ELEMENT after it is the writer RESUMING FREE BODY. The human renders the bubble
			// small and the [body] + everything after as normal page content (XGF9001-00, where one
			// [speech bubble] swallowed "This module will help you…" + bullets + a video + a 2nd
			// bubble). Terminate once the invocation already carries its text. Same section-break family
			// as body_terminates_after_face/_after_table; a per-type list (NOT a blanket rule) keeps it
			// from ever firing for table/face-authored widgets (e.g. flipCard) whose invocation text may
			// legitimately precede a [body]. Measured: 56 such over-captures across 19 modules, and 0
			// empty-invocation-then-[body] counter-cases (a [body] is never the bubble's OWN text).
			// Data: member_rule.body_terminates_after_invocation_text_types.
			if (p?.tag === "body" && p?.directive !== "INTERACTIVE"
				&& (_mrB.body_terminates_after_invocation_text_types ?? []).includes(bundle.type)) {
				const sawInvocationText = bundle.memberItems.some((m) => m.type === "tag"
					&& m.parse?.primary?.directive === "INTERACTIVE"
					&& String(m.blackAfter ?? "")
						.replace(/\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu, "").trim().length > 0);
				// CONVERSATION form: the bubble text rides on captured [black] members (the
				// Prompt/AI-response lines), NOT the invocation — whose "Conversation layout" modifier
				// sits INSIDE the tag, so blackAfter is empty. Without this check, a conversation-style
				// speech bubble could swallow a following [body] paragraph that should render on its
				// own, and even merge in a second, unrelated conversation. Once the bubble has captured
				// black content, a following [Body] is a section break. A [body] is never a
				// speechBubble's OWN content.
				const sawBlackContent = bundle.memberItems.some((m) =>
					m.type === "black" && String(m.text ?? "").trim().length > 0);
				if (sawInvocationText || sawBlackContent) break;   // bubble text already captured → [body] resumes free body
			}

			// SHAPE-PATTERN SECTION BREAK. A shapeHover widget authors repeating [shape n] > [body] >
			// [image] groups; a [body] that begins AFTER the current shape group is already COMPLETE
			// (an [image]/media member seen since the most recent [shape n], with NO new [shape n]
			// opening a fresh group) is the writer RESUMING free body — the finished page keeps it
			// OUTSIDE the widget as ordinary following prose. Every legitimate shape-description
			// [body] is immediately preceded by its own [shape n] (with no image captured in the
			// group yet), so it never trips this check. Same family as
			// body_terminates_after_face/_table/_invocation_text above; the LONE SECTION-BREAK
			// HEADING rule further below handles the section heading that typically follows.
			// Data member_rule.body_section_break_after_shape (+ _types); env SHAPEBODY_OFF.
			if (p?.tag === "body" && p?.directive !== "INTERACTIVE"
				&& (_mrB.body_section_break_after_shape ?? false)
				&& (_mrB.body_section_break_after_shape_types ?? ["shapeHover"]).includes(bundle.type)
				&& !(typeof process !== "undefined" && process.env && process.env.SHAPEBODY_OFF)) {
				let sawImageSinceShape = false, reachedShape = false;
				for (let k = bundle.memberItems.length - 1; k >= 0; k--) {
					const m = bundle.memberItems[k];
					if (m.type === "tag" && m.parse?.tags?.some((t) => /^shape\b/.test(t.tag))) { reachedShape = true; break; }
					if (m.type === "tag" && ["image", "video", "audio"].includes(m.parse?.primary?.tag)) sawImageSinceShape = true;
				}
				if (reachedShape && sawImageSinceShape) break;   // shape group complete → this [body] resumes free body
			}

			// SLIDE-PATTERN SECTION BREAK. A carousel slide is typically shaped [slide n] > [H#] >
			// [body] (main text, before the image) > [image] > [body] (an example caption, after the
			// image) — ONE caption after the image. A FURTHER [body] (an [image] seen since the last
			// [slide n] AND a [body] ALREADY captured after that image — i.e. a SECOND post-image
			// body) is the writer RESUMING free body after the last slide; the finished page renders
			// it as an ordinary <p> after the whole carousel. Same family as
			// body_section_break_after_shape above, but a slideshow specifically allows one
			// post-image caption per slide before treating anything further as a section break.
			// Data member_rule.body_section_break_after_slide (+ _types); env CARSLIDE_OFF.
			if (p?.tag === "body" && p?.directive !== "INTERACTIVE"
				&& (_mrB.body_section_break_after_slide ?? false)
				&& (_mrB.body_section_break_after_slide_types ?? ["carousel", "rotateBanner"]).includes(bundle.type)
				&& !(typeof process !== "undefined" && process.env && process.env.CARSLIDE_OFF)) {
				let sawBodySince = false, postImageBody = false, reachedSlide = false;
				for (let k = bundle.memberItems.length - 1; k >= 0; k--) {
					const m = bundle.memberItems[k];
					if (m.type === "tag" && m.parse?.tags?.some((t) => /^slide\b/.test(t.tag))) { reachedSlide = true; break; }
					const mp = m.type === "tag" ? m.parse?.primary : null;
					const isBody = mp?.tag === "body" || (m.type === "black" && String(m.text ?? "").trim().length > 0);
					if (isBody) sawBodySince = true;
					if (["image", "video", "audio"].includes(mp?.tag) && sawBodySince) postImageBody = true;
				}
				if (reachedSlide && postImageBody) break;   // 2nd post-image body → free body resumes after the carousel
			}

			// MEDIA-SERIES SECTION BREAK (round 247, ENGS404-00). A carousel authored as a
			// back-to-back RUN of [image]/[video] members directly after the invocation —
			// "[insert image carousel] [image 1] [image 2] [image 3] [image 4]" — IS the series:
			// the writer's own list delimits the widget, and the first following non-media ELEMENT
			// tag (a [body], a heading, a [button], a data marker…) is the SECTION resuming. The
			// old walk kept absorbing to the page end, so the whole introduction/vocabulary section
			// dumped into the placeholder and the build always declined. Scoped hard (measured,
			// outputs/_detect_r247.cjs over ALL corpus dirs): fires only when the bundle has NO
			// [slide N] marker AND every substantive captured member so far is the invocation, a
			// media member, a video's own link/title black line, or a writer instruction — i.e. the
			// capture is still a PURE media run (>= media_series_min_run). Interleaved dialects
			// (image>body>image slide captions) never satisfy the pure-run test and keep the old
			// behaviour BY CONSTRUCTION; the measured zero-risk terminator set is "any tag ELEMENT
			// whose primary is not image/video/audio/caption" (no built bundle carries a [body]
			// after its run; the 11 heading-tailed builds were themselves over-captures —
			// EXPFUN02/ENGJ403's trailing sections baked in as bogus slides — corrected by this
			// rule toward the writer's structure). Data member_rule.media_series_break
			// (+ _types/_min_run); env CARSERIES_OFF.
			if (p && p.directive !== "INTERACTIVE"
				&& !["image", "video", "audio", "caption"].includes(p.tag)
				&& (_mrB.media_series_break ?? false)
				&& (_mrB.media_series_break_types ?? ["carousel", "rotateBanner"]).includes(bundle.type)
				&& !(typeof process !== "undefined" && process.env && process.env.CARSERIES_OFF)) {
				let mediaRun = 0, pure = true, sawSlideMarker = false, lastWasVideo = false;
				for (const m of bundle.memberItems) {
					if (!m) continue;
					if (m.type === "table" || m.type === "nested") { pure = false; break; }
					if (m.type === "black") {
						if (!String(m.text ?? "").trim()) continue;
						// a link/title line directly after a video is that video's reference line
						if (lastWasVideo && (m.block?.links?.length || /https?:\/\//.test(String(m.text ?? "")))) { lastWasVideo = false; continue; }
						pure = false; break;
					}
					const mp = m.parse?.primary;
					if (!mp) {
						if (["instruction", "noise"].includes(m.parse?.class)) continue;   // writer notes ride along
						pure = false; break;
					}
					if (mp.directive === "INTERACTIVE") { lastWasVideo = false; continue; }   // the invocation itself
					if (mp.tag === "slide n" || mp.tag === "slide"
						|| (m.parse?.tags ?? []).some((t) => t.tag === "slide n")) { sawSlideMarker = true; break; }
					if (["image", "video", "audio"].includes(mp.tag)) { mediaRun++; lastWasVideo = mp.tag === "video"; continue; }
					pure = false; break;
				}
				if (pure && !sawSlideMarker && mediaRun >= (_mrB.media_series_min_run ?? 2)) {
					break;   // the media run IS the carousel → this element resumes the section
				}
			}

			// SAME-TYPE GROUP SPLIT. A SECTION heading BETWEEN two same-type widget GROUPS must split
			// them (e.g. an [H4] section heading sitting between one set of flip cards and a second,
			// unrelated set of flip cards — the finished page ships TWO separate flip-card containers
			// with that heading rendered free between them, not fused into one big container).
			// Discriminator: a heading whose IMMEDIATELY-FOLLOWING member is a SAME-type INTERACTIVE
			// opener (a new [flip card]) is a between-group section heading — a card-FRONT heading, by
			// contrast, is followed by its own [image], never by another [flip card]. Terminate so the
			// heading renders as free content and the next group opens its own separate bundle. Scoped
			// to listed widget types (the multi-instance widgets whose heading_is_terminator flag is
			// false). Data member_rule.heading_splits_same_type_groups; env FLIPGROUP_OFF.
			if (p && ["h2", "h3", "h4", "h5"].includes(p.tag) && normaliser
				&& (_mrB.heading_splits_same_type_groups ?? []).includes(bundle.type)
				&& !(typeof process !== "undefined" && process.env && process.env.FLIPGROUP_OFF)) {
				const nx = items[j + 1];
				if (nx && nx.type === "tag" && nx.parse?.primary?.directive === "INTERACTIVE") {
					const nxType = this.#widgetTypeFor(nx.parse.primary.tag, nx.parse.primary.alias, normaliser);
					if (nxType === bundle.type) break;   // section heading before a new same-type group → split here
				}
			}

			// TABLE-DATA SECTION-BREAK resumption (OSBY201-02 + OSAI501-01): a [Body] ELEMENT or an
			// [H2]-[H5] section HEADING that appears AFTER a TABLE-DATA widget (uses_data_table —
			// typing/dragAndDrop/dropQuiz/memoryGame…) has captured its table is the writer starting
			// a NEW SECTION. The table is the widget's content; the [body]/heading and ANYTHING after
			// it (a following speechBubble + video — the unicorn bubble the memoryGame was swallowing)
			// belong OUTSIDE the widget. This OVERRIDES heading_is_terminator:false (that flag only
			// protects the widget's OWN internal headings, which sit in/before the data — a heading
			// AFTER the data table is not internal). Slideshow widgets (carousel/rotateBanner) are
			// EXEMPT (their trailing [body] is a slide caption the image-carousel builder handles).
			// Data: member_rule.{body,heading}_terminates_after_table (+ _exempt_types/_levels).
			if (p?.directive !== "INTERACTIVE" && bundle.tables.length > 0) {
				const entry = DataService.Data.BoundaryBank.interactives[bundle.type];
				const exempt = (_mrB.body_terminates_after_table_exempt_types ?? []).includes(bundle.type);
				const headingLevels = _mrB.heading_terminates_after_table_levels ?? ["h2", "h3", "h4", "h5"];
				const isBreak = (_mrB.body_terminates_after_table && p?.tag === "body")
					|| (_mrB.heading_terminates_after_table && headingLevels.includes(p?.tag));
				if (entry?.uses_data_table && !exempt && isBreak) break;   // section break resumes after the data table
			}

			// LONE SECTION-BREAK HEADING.
			// A heading_is_terminator:false widget legitimately holds internal headings, but across
			// the corpus those fall into only three shapes: (a) the LEAD title (a heading BEFORE any
			// captured content), (b) a CLUSTER of two or more sibling panel/front headings, or (c) a
			// card FRONT immediately followed by its [image]. A SINGLE heading that lands AFTER the
			// widget has captured at least one genuine content member, has NO sibling [H2]-[H5]
			// before the bundle's next ABSOLUTE terminator, AND is FOLLOWED BY ordinary section
			// content (a [body]/[video]/[audio]/table/list — NOT an [image] front, NOT widget
			// sub-content) is the writer STARTING A NEW SECTION that the widget must not own — the
			// finished page renders that heading and what follows it OUTSIDE the widget. DISTINCT
			// from heading_terminates_after_table above (that needs a captured TABLE; this fires when
			// the captured content is floating black members / images with no table yet — e.g. a
			// shapeHover's text-box labels). The LEAD + CLUSTER + follow=image exclusions keep every
			// legitimate internal heading intact. Data:
			// member_rule.lone_heading_section_break (+ lone_heading_follow_section_tags); env LONEHEAD_OFF.
			// Slideshow types (carousel/rotateBanner) carry a slide TITLE per slide; the LAST
			// slide's heading is "lone" (no sibling heading after it) and would otherwise falsely
			// trip this rule, truncating the carousel before its final slide. Their headings were
			// blanket-exempted here — but that let the SECTION heading AFTER the whole carousel
			// (OSOH501-01 "[H3] How to use hauora…" following the 4th slide) be swallowed as a
			// bogus 5th slide, killing the build (the empty trailing slide bails the builder).
			// ROUND 214 (Chris, OSOH501): the exemption is now PRECISE — a heading whose nearest
			// preceding substantive member is a [Slide N]/[slide] MARKER is that slide's title
			// (always internal, the r96 OSAI501-04 protection); any OTHER heading in a slideshow
			// runs the standard lone+follow test below, whose follow=image exclusion keeps a
			// heading-opened slide's title inside (its [image] follows) while a trailing section
			// heading (followed by [body] text) correctly terminates the carousel.
			// Data slideshow_heading_internal (+ slideshow_heading_lone_break); env CARTRAIL_OFF.
			let slideshowExempt = (_mrB.slideshow_heading_internal ?? []).includes(bundle.type);
			if (slideshowExempt && (_mrB.slideshow_heading_lone_break ?? false)
				// REO/bilingual modules keep the r96 blanket exemption (the r145 exclusion
				// class): their text-form carousels flow through the bilingual placeholder
				// pipeline, and splitting one at a lone heading re-exposes raw members the
				// merged dump was containing (measured: TRR301 +1 literal-tag leak).
				&& !InteractiveScanner.#reoModeFor(run)
				// Only an IMAGE-carrying carousel (the buildable image-slide form) runs the
				// precise test: its interior slide titles are protected by the follow=image
				// exclusion, so only a genuine trailing section heading breaks. A TEXT-form
				// carousel (heading+body slides, NO [image] member yet — MXDB302's quiz
				// carousels) keeps the blanket exemption: every one of its slide headings is
				// followed by body text, so the lone test would cut its LAST slide off
				// (measured: MXDB302-06 scaffold 54.8→25.0 without this guard).
				&& bundle.memberItems.some((m) => m && m.type === "tag" && m.parse?.primary?.tag === "image")
				&& !(typeof process !== "undefined" && process.env && process.env.CARTRAIL_OFF)) {
				let precededByMarker = false;
				for (let k = bundle.memberItems.length - 1; k >= 0; k--) {
					const m = bundle.memberItems[k];
					if (m.type === "black" && !String(m.text ?? "").trim()) continue;
					if (m.type === "tag") {
						const mp = m.parse?.primary;
						if (mp?.directive === "INSTRUCTION" || m.parse?.class === "instruction") continue;
						precededByMarker = mp?.tag === "slide n" || mp?.tag === "slide"
							|| (m.parse?.tags ?? []).some((t) => t.tag === "slide n");
					}
					break;   // first substantive member decides
				}
				slideshowExempt = precededByMarker;
			}
			if (headingTerminates === false && p && ["h2", "h3", "h4", "h5"].includes(p.tag)
				&& (_mrB.lone_heading_section_break ?? false)
				&& !slideshowExempt
				&& !(typeof process !== "undefined" && process.env && process.env.LONEHEAD_OFF)) {
				const faceTags = _mrB.face_member_tags ?? ["front", "back", "drop", "answer"];
				const widgetSubTags = new Set([...faceTags, "shape n", "tab n", "slide n"]);
				const isGenuineContent = (m) => {
					if (m.type === "black") return String(m.text ?? "").trim().length > 0;
					if (m.type === "table") return true;
					if (m.type === "tag") {
						const mp = m.parse?.primary;
						if (!mp || mp.directive === "INSTRUCTION") return false;
						if (["image", "video", "audio", "button"].includes(mp.tag)) return true;
						if (m.parse?.tags?.some((t) => widgetSubTags.has(t.tag))) return true;
					}
					return false;
				};
				// (1) the widget already captured >=1 genuine content member (NOT the LEAD-title case)
				const contentCaptured = bundle.memberItems.some(isGenuineContent);
				if (contentCaptured) {
					// PANEL-LABEL exclusion. A NUMBERED multi-panel widget authors each panel as
					// [clickdrop N image] > [clickdrop N text] > [H#] label > [body] > [image]*3. EVERY
					// panel heading is followed by its own [body], and the LAST panel's heading is
					// "lone" (no sibling [H#] after it), so the plain LONE SECTION-BREAK HEADING check
					// above would falsely terminate the widget right at the last panel — fragmenting a
					// single clickDrop widget into an activity box + a stray numberless box + a leaked
					// plain-body paragraph. A heading whose NEAREST preceding captured member (skipping
					// the widget's own empty [clickdrop N text] opener and any retained notes, with NO
					// free body/media/table in between) is a SAME-TYPE interactive panel opener is that
					// panel's LABEL, never a section break — the same idea as exclusion (c) above ("a
					// card FRONT immediately followed by its [image]"). A shapeHover's genuine section
					// heading, by contrast, is preceded by shape CONTENT (image/body), not a same-type
					// opener, so it still correctly terminates. Data
					// lone_heading_panel_label_exclude; env LONECLUSTER_OFF.
					// SINGLE-TYPE guard: only a clean same-type panel cluster (all absorbed extraTypes
					// === bundle.type — e.g. clickDrop+clickDrop+…) qualifies. A MULTI-TYPE mega-merge
					// (several different widget types absorbed together) is NOT a panel cluster — its
					// internal [H#] headings are genuine widget boundaries, so keep the ordinary
					// termination behaviour there (otherwise an already-over-merged bundle would only
					// grow further).
					const singleTypeCluster = !(bundle.extraTypes ?? []).some((t) => t !== bundle.type);
					let isPanelLabel = false;
					if ((_mrB.lone_heading_panel_label_exclude ?? true) && normaliser && singleTypeCluster
						&& !(typeof process !== "undefined" && process.env && process.env.LONECLUSTER_OFF)) {
						for (let k = bundle.memberItems.length - 1; k >= 0; k--) {
							const m = bundle.memberItems[k];
							if (m.type === "black") { if (String(m.text ?? "").trim()) break; continue; }
							if (m.type === "table") break;
							if (m.type === "tag") {
								const mp = m.parse?.primary;
								if (mp?.directive === "INSTRUCTION") continue;   // skip a retained note
								if (mp?.directive === "INTERACTIVE") {
									isPanelLabel = this.#widgetTypeFor(mp.tag, mp.alias, normaliser) === bundle.type;
								}
								break;   // first substantive tag decides
							}
						}
					}
					const stopsBundle = (it2) => {
						if (it2.type !== "tag") return false;
						const pp = it2.parse?.primary;
						if (!pp) return false;
						if (pp.tag === "activity" || it2.parse.tags?.some((t) => t.tag === "activity")) return true;
						if (pp.tag === "h1" || absolute.has(pp.tag)) return true;
						return pp.directive === "INTERACTIVE" || pp.directive === "CONTAINER_CLOSE" || pp.directive === "PAGE_BOUNDARY";
					};
					// (2) LONE: no sibling [H2]-[H5] between here and the bundle's next absolute terminator
					let lone = true;
					for (let k = j + 1; k < items.length; k++) {
						const it2 = items[k];
						if (stopsBundle(it2)) break;
						if (it2.type === "tag" && ["h2", "h3", "h4", "h5"].includes(it2.parse?.primary?.tag)) { lone = false; break; }
					}
					// (3) FOLLOWED BY ordinary section content (skip notes; an [image] front => false)
					const sectionTags = _mrB.lone_heading_follow_section_tags ?? ["video", "audio", "list"];
					let followSection = false;
					for (let k = j + 1; k < items.length; k++) {
						const it2 = items[k];
						if (it2.type === "black") { followSection = String(it2.text ?? "").trim().length > 0; break; }
						if (it2.type === "table") { followSection = true; break; }
						if (it2.type === "tag") {
							const pp = it2.parse?.primary;
							if (!pp) continue;
							if (pp.directive === "INSTRUCTION") continue;   // a retained note — keep scanning
							followSection = sectionTags.includes(pp.tag);   // [image]/front/etc => false (keep inside)
							break;
						}
					}
					// WITHIN-PANEL HEADING CLUSTER (ROUND 214, Chris — OSOH501-01 panel 4). Inside a
					// NUMBERED-SERIES host (numbered_series_absorb), a lone heading that CONTINUES a
					// same-level heading run already captured since the last panel opener is that
					// panel's internal sub-heading cluster, never a section break — OSOH501's
					// [Accordion 4] holds [H5] Manaaki / [H5] Tika / [H5] Whanaungatanga: the first
					// two survive the LONE test (a sibling lies ahead) but the LAST is forward-lone
					// and used to truncate the panel right before it (the human nests all three in
					// accContent). Scoped to numbered-series hosts only, so the r77 shapeHover
					// section-break behaviour is untouched everywhere else. Env ACCNEST_OFF.
					let panelCluster = false;
					const _serCfg = _mrB.numbered_series_absorb;
					if (_serCfg && _serCfg.enabled !== false && (_serCfg.hosts ?? []).includes(bundle.type)
						&& !(typeof process !== "undefined" && process.env && process.env.ACCNEST_OFF)) {
						for (let k = bundle.memberItems.length - 1; k >= 0; k--) {
							const m = bundle.memberItems[k];
							if (m.type !== "tag") continue;
							const mt = m.parse?.primary?.tag;
							if (mt === bundle.type) break;              // reached the panel opener
							if (mt === p.tag) { panelCluster = true; break; }   // a same-level sibling already in this panel
						}
					}
					if (lone && followSection && !isPanelLabel && !panelCluster) break;   // lone heading starts a new section → terminate the widget here (unless a same-type panel LABEL / an in-panel cluster member)
				}
			}

			// (new interactive) — when the open bundle belongs to an
			// [Activity N] and no new [Activity] has appeared, the human
			// developers build BOTH widgets inside ONE activity block
			// (bank policy same_activity_multi_widget; verified BLL155 1A:
			// carousel + [self check] = one activity). Absorb as an extra
			// widget type instead of splitting. Openerless inline bundles
			// still split as before.
			if (p?.directive === "INTERACTIVE") {
				const meta = DataService.Data.BoundaryBank._meta.member_rule;
				const extra = normaliser ? this.#widgetTypeFor(p.tag, p.alias, normaliser) : null;
				// INLINE MARKERS ([highlight text] → wordSelect/wordHighlighter) are NOT
				// standalone widgets — they mark text the human highlights INLINE on the
				// surrounding container. Inside an open widget they must be ABSORBED as a
				// plain member (never a terminator), so the host's text stays whole:
				// XGF9001's flip-card back "Being [highlight text] gifted means…" must
				// remain ONE back, not split into "Being" + an empty wordSelect. (Bank
				// policy member_rule.inline_markers; body-breakdown #2.)
				if (extra !== null && (meta.inline_markers ?? []).includes(extra)) {
					this.#collectMember(bundle, next, run);
					continue;
				}
				// NESTED-INTERACTIVE ABSORB. A DIFFERENT-type interactive the writer authored INSIDE
				// this host's content (e.g. a [shape hover] typed inside an [Accordion 5] panel) is
				// ABSORBED as a NESTED sub-bundle rather than terminating the host outright (which is
				// what the default `break` at the foot of this block would otherwise do). The nested
				// widget is recursively swallowed into its own sub-bundle (its members ride along
				// inside the host's consumed range, so the main scanning loop never re-scans them
				// separately), and a {type:"nested"} marker is pushed into the host's members at the
				// nested widget's position. The host then keeps walking AFTER the nested widget, so a
				// later SAME-type continuation (e.g. the writer resuming "[Accordion 5]" content
				// further down, perhaps under a duplicate panel number) still rejoins the SAME host —
				// producing one single accordion container with the shapeHover nested inside one of
				// its panels, matching the finished page. MAP host->[nested types] (data
				// member_rule.nested_interactive_absorb) keeps this tight: for example, only
				// accordion->shapeHover is allowed, nothing broader. env NESTABSORB_OFF reverts to
				// the older behaviour where a nested widget simply terminates the host instead.
				const nestList = (meta.nested_interactive_absorb ?? {})[bundle.type] ?? [];
				if (extra !== null && extra !== bundle.type && nestList.includes(extra)
					&& !(typeof process !== "undefined" && process.env && process.env.NESTABSORB_OFF)) {
					j = this.#absorbNestedSubBundle(bundle, items, j, next, extra, p, absolute, run, normaliser) - 1;
					continue;
				}
				// NUMBERED-SERIES CONTAINMENT (ROUND 214, Chris — OSOH501-01). When the writer
				// authors an accordion as a NUMBERED panel series ([Accordion 1] … [Accordion 2] …
				// [Accordion 4]), the numbers are an explicit FORWARD GUARANTEE: everything between
				// [Accordion N] and [Accordion N+1] belongs to panel N — including a different-type
				// interactive the writer placed INSIDE the panel (a [modal] image set, a [tabs]
				// letter-nav, a [Click drop] values table). The human's finished pages group ALL the
				// numbered panels into one accordion and nest those widgets inside the panel's
				// accContent (measured corpus-wide: outputs/_measure_accnest.py — 28 modules author
				// widgets between numbered panels; outputs/_measure_accnest_gold.py — 83 modules'
				// golds nest widget markup inside accContent). So: while the HOST is a numbered
				// series (a data-listed host type with a numbered opener/member), a different-type
				// INTERACTIVE invocation is absorbed as a NESTED sub-bundle (the r95 mechanism)
				// rather than terminating the host — (a) ALWAYS when a LATER numbered same-type tag
				// still lies ahead (Chris's between-panels rule, provably inside the series), and
				// (b) after the LAST numbered panel (tail) only when the series is real (>=
				// min_panels numbered tags already captured) — the tail window is still bounded by
				// every existing terminator (lone section heading / callout / [Activity] / [H1] /
				// page boundary). Data member_rule.numbered_series_absorb; env ACCNEST_OFF.
				const seriesCfg = meta.numbered_series_absorb;
				if (extra !== null && extra !== bundle.type && seriesCfg && seriesCfg.enabled !== false
					&& (seriesCfg.hosts ?? []).includes(bundle.type)
					&& !(typeof process !== "undefined" && process.env && process.env.ACCNEST_OFF)) {
					const numRe = new RegExp(
						(seriesCfg.numbered_pattern ?? "\\[\\s*{type}\\s+\\d+").replace("{type}", bundle.type),
						"i");
					const isNumbered = (m) => m && m.type === "tag"
						&& m.parse?.primary?.tag === bundle.type && numRe.test(String(m.text ?? ""));
					const panelsSoFar = [...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])]
						.filter(isNumbered).length;
					// look AHEAD: does a later numbered same-type tag lie before a hard stop?
					let laterPanel = false;
					for (let k = j + 1; k < items.length; k++) {
						const it2 = items[k];
						if (it2.type !== "tag") continue;
						const pp = it2.parse?.primary;
						if (!pp) continue;
						if (pp.tag === bundle.type && numRe.test(String(it2.text ?? ""))) { laterPanel = true; break; }
						if (pp.tag === "h1" || pp.tag === "activity" || absolute.has(pp.tag)
							|| pp.directive === "PAGE_BOUNDARY" || pp.directive === "CONTAINER_CLOSE") break;
					}
					const tailOk = (seriesCfg.tail !== false) && panelsSoFar >= (seriesCfg.min_panels ?? 2);
					if ((laterPanel && panelsSoFar >= 1) || tailOk) {
						j = this.#absorbNestedSubBundle(bundle, items, j, next, extra, p, absolute, run, normaliser) - 1;
						continue;
					}
				}
				// SAME widget type = a CONTINUATION (multi-panel: accordion strips,
				// flip-card decks) — always absorbed so the panels stay one bundle.
				// A DIFFERENT type = a new widget; absorbed only when this bundle
				// belongs to a REAL [Activity N] (BLL155 carousel + selfCheck = one
				// activity). Otherwise it TERMINATES — the XGF9001 fix: a flipCard
				// must NOT swallow the following accordion + the rest of the page.
				const sameType = extra !== null && extra === bundle.type;
				// A DIFFERENT-type DISPLAY/narration follower (display_terminator_types —
				// speechBubble/flipCard/tabs) is a NEW presentational SECTION, not another step of
				// the same activity's task. The finished page CLOSES the activity and renders the
				// follower OUTSIDE it, as its own separate element (this is a strong, well-measured
				// pattern across the corpus for these particular widget types). Terminate instead of
				// absorbing — the follower then starts its OWN bundle, resolved either by the
				// activity look-back as free-body content (it simply stops once it reaches the
				// already-consumed original widget), or, if a new [Activity] tag intervenes first,
				// that tag's absolute terminator opens a brand NEW activity container for it (this
				// already happens naturally — the loop breaks at [activity] before reaching the
				// widget). TASK-style followers (typing/dropQuiz/reorder/mcq — usually kept inside
				// the SAME activity) and same-type continuations are unaffected by this rule. Data:
				// member_rule.{same_activity_display_terminates, display_terminator_types}; env
				// ACTSPLIT_OFF.
				const displayTerminates = meta.same_activity_display_terminates
					&& !(typeof process !== "undefined" && process.env && process.env.ACTSPLIT_OFF)
					&& extra !== null && !sameType
					&& (meta.display_terminator_types ?? []).includes(extra);
				if (meta.same_activity_multi_widget && normaliser && !displayTerminates
					&& (sameType || bundle.activityId)) {
					(bundle.extraTypes ??= []).push(extra);
					this.#collectMember(bundle, next, run);
					run.AddNote("info", "InteractiveScanner",
						`${bundle.activityId ? "Activity " + bundle.activityId : bundle.type}: additional widget [${p.tag}] absorbed (${bundle.type} + ${extra}).`);
					continue;
				}
				if (displayTerminates) break;   // display/narration follower → activity closes here
				// CONVERSATION + clickDrop reveal: a CONVERSATION-style speechBubble absorbs an
				// immediately-following clickDrop as its own inline response — the writer's "Click to
				// see its response:" instruction plus a [Click drop] (front/drop) tag together form
				// the LAST turn of the conversation. The conversation builder renders it as that last
				// bubble's CLICK reveal (following the Writers Template's literal [Click drop]
				// instruction, rather than a hover interaction, since a hover can't be reliably
				// derived from the source document). Narrow: only a speechBubble whose invocation
				// carries the "Conversation layout" cue absorbs a clickDrop this way, and only ONE;
				// the clickDrop's [front]/[drop] members are then collected as usual, and a following
				// [body] still terminates per the FACE / REVEAL member terminator rule above. Data:
				// member_rule.conversation_absorbs_clickdrop.
				if (extra === "clickDrop" && bundle.type === "speechBubble"
					&& (meta.conversation_absorbs_clickdrop ?? true)
					&& [...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])].some((m) =>
						m.type === "tag" && /conversation/i.test(String(m.text ?? "")))) {
					(bundle.extraTypes ??= []).push(extra);
					this.#collectMember(bundle, next, run);
					continue;
				}
				break;
			}
			// (new [Activity N]) — absolute
			if (p?.tag === "activity" || next.parse.tags.some((t) => t.tag === "activity")) break;
			// the bank's absolute terminator list (alert, important,
			// end activity, page boundaries, section markers, h1 …)
			if (p && absolute.has(p.tag)) break;
			if (p?.directive === "CONTAINER_CLOSE") break;   // explicit close ends the open container (over-capture #3)
				if (p?.directive === "PAGE_BOUNDARY") break;   // belt & braces
			// conditional terminators: h2–h5 per the widget's flag
			if (p && ["h2", "h3", "h4", "h5"].includes(p.tag) && headingTerminates) break;

			// not a terminator → swallowed as a member
			this.#collectMember(bundle, next, run);
		}
		return j;
	};

	/**
	 * TRAILING-MEDIA FIX. Trim trailing [video]/[audio] members (the writer's
	 * post-widget media) back out of a just-closed bundle so they render as their
	 * OWN standalone elements via the normal converter path.
	 *
	 * WHY: writers often drop an explainer [video] AFTER an interactive's content
	 * (OSBY301: a YouTube video after the last accordion panel). The boundary scan
	 * swallows it as a member, but the finished HTML places it in its own row. So
	 * we pop any trailing media tags off the bundle and shrink the consumed range;
	 * the scanner then resumes AT that item (i = endIndex - 1; i++) and it converts
	 * normally, in document order, right after the widget.
	 *
	 * Data-driven: the tag list is BoundaryBank._meta.member_rule.trailing_media_extract.
	 *
	 * @param {Object} bundle    - the bundle whose members were just collected
	 * @param {number} endIndex  - the bundle's current end index (exclusive)
	 * @returns {number} the (possibly reduced) end index
	 */
	static #trimTrailingMedia(bundle, endIndex) {
		const mr = DataService.Data.BoundaryBank?._meta?.member_rule ?? {};
		// SLIDESHOW widgets (carousel/rotateBanner) are EXEMPT: a trailing [video]/[audio]
		// is the last SLIDE, not post-widget media — trimming it would drop a slide and
		// duplicate it as a standalone element after the widget. (member_rule.trailing_media_extract_exempt_types)
		if ((mr.trailing_media_extract_exempt_types ?? []).includes(bundle.type)) return endIndex;
		const extract = mr.trailing_media_extract ?? [];
		if (!extract.length) return endIndex;
		// The last memberItem always lines up with items[endIndex-1] (members are
		// swallowed in document order), so each pop shrinks the range by one item.
		while (bundle.memberItems.length) {
			const last = bundle.memberItems[bundle.memberItems.length - 1];
			if (last.type !== "tag") break;
			if (!extract.includes(last.parse?.primary?.tag)) break;
			bundle.memberItems.pop();
			endIndex -= 1;
		}
		return endIndex;
	};

	/**
	 * BACKWARD LEAD-PAIR ABSORB.
	 *
	 * The general idea: "detect a repeating pattern, then go back UP to recover the missed
	 * first pairing." Because a bundle is scanned FORWARD from the first interactive tag (see
	 * ScanPage above), a REPEATING (lead-in label, widget) series always loses its very first
	 * label — it sits ABOVE the tag, outside the forward scan (e.g. a series of speech bubbles
	 * each introduced by a short lead-in like "…what we see:" would have its very first
	 * lead-in orphaned as ordinary body text, while its later siblings "…feel:"/"…think:" get
	 * correctly captured as part of the widget).
	 *
	 * After #swallowMembers has run, collapse the captured members into a per-source-block
	 * token string (W=interactive tag, L=standalone black label, O=table). ONLY on a STRICT
	 * clean widget-first alternation (^W(LW)+$: two or more widgets, exactly one label per
	 * interior widget, no runs of multiple labels, no tables) do we extrapolate the pattern
	 * backward: walk up over UNCONSUMED black items whose label SIGNATURE equals the DOMINANT
	 * interior-label signature (i.e. they look "similarly structured" to the labels already
	 * captured) and are label-shaped (num/alpha/colon/bullet — never free prose or a URL),
	 * capped at exactly the number of MISSING labels and close to the interior labels' word
	 * count. Matched labels are prepended to memberItems and startIndex is moved back to
	 * include them (the caller's ownership-marking loop then consumes them along with
	 * everything else). Data member_rule.leading_pattern_absorb; env INTLEADPAIR_OFF.
	 * inline_only.
	 */
	static #absorbLeadingPattern(bundle, items, tagIdx) {
		const cfg = DataService.Data.BoundaryBank?._meta?.member_rule?.leading_pattern_absorb;
		if (!cfg || cfg.enabled === false) return;
		if (typeof process !== "undefined" && process.env && process.env.INTLEADPAIR_OFF) return;
		if (cfg.inline_only !== false && bundle.activityOwner) return;   // inline widgets only

		// collapse members -> per-role token string; noise/instruction fragments ride the widget block
		let toks = "";
		const labelTexts = [];
		for (const m of bundle.memberItems) {
			if (m.type === "tag" && m.parse?.primary?.directive === "INTERACTIVE") toks += "W";
			else if (m.type === "black") { toks += "L"; labelTexts.push(m.text ?? ""); }
			else if (m.type === "table") toks += "O";
		}
		if (!new RegExp(cfg.widget_first_alternation ?? "^W(LW)+$").test(toks)) return;

		// the DOMINANT interior-label signature must be a genuine lead-in shape (Chris: "similarly
		// structured") — else the labels are incidental and nothing above should be pulled in.
		const counts = {};
		for (const t of labelTexts) { const s = this.#labelSignature(t, cfg); counts[s] = (counts[s] || 0) + 1; }
		const domSig = Object.keys(counts).sort((a, b) => counts[b] - counts[a])[0];
		if (!(cfg.label_like ?? []).includes(domSig)) return;

		const wc = (t) => String(t ?? "").replace(/\*+/g, "").trim().split(/\s+/).filter(Boolean).length;
		const maxLbl = labelTexts.reduce((a, t) => Math.max(a, wc(t)), 0);
		const cap = Math.max(maxLbl + (cfg.max_above_words_over_labels ?? 2), cfg.min_above_words_cap ?? 12);
		const nW = (toks.match(/W/g) || []).length;
		const missing = nW - labelTexts.length;         // labels needed to balance the front (=1 here)
		if (missing < 1) return;

		// walk UP, absorbing contiguous UNCONSUMED black labels that MATCH the interior signature —
		// the recovered leading pairing(s). Stops at the first non-matching / consumed / non-black
		// item, so it can never cross into unrelated section content.
		let s = tagIdx - 1;
		const absorbed = [];
		while (s >= 0 && absorbed.length < missing) {
			const prev = items[s];
			if (!prev || prev.consumedBy !== undefined || prev.type !== "black") break;
			if (this.#labelSignature(prev.text, cfg) !== domSig) break;
			if (wc(prev.text) > cap) break;
			absorbed.unshift(prev);
			s--;
		}
		if (!absorbed.length) return;
		bundle.memberItems.unshift(...absorbed);
		bundle.startIndex = s + 1;
		for (const a of absorbed) this.#harvestMedia(bundle, a);
	};

	/**
	 * BACKWARD SAME-BLOCK AVATAR ABSORB (round 246, ticket 1 of the basic-interactive
	 * builders round).
	 *
	 * THE WRITER'S FORM (measured, TEDC401/TEDC402/SSCI104): the avatar and its bubble are
	 * ONE Writers Template paragraph —
	 *     [Image] avatar Tina  smiling  <iStock title> [LINK: https://…gm2235638824-…]
	 *     [speech bubble] RHS  See how the table gives the details…
	 * The extractor splits that paragraph into separate red-span ITEMS, and the forward
	 * member walk starts AT the [speech bubble] invocation, so the [image] item sits just
	 * ABOVE it, outside the bundle. Today it therefore renders as a loose standalone image
	 * (plus its "avatar Tina" caption) with the bubble text stranded in a hand-off box
	 * below; the finished page ships ONE `row speechBubble` containing both.
	 *
	 * THE DISCRIMINATOR IS THE SHARED SOURCE `block` — the round-105 "continuous sentence
	 * vs a paragraph later" rule. An [image] in a DIFFERENT paragraph is the writer's own
	 * separate element and is never touched, so this can only ever pull in an image the
	 * writer glued to the bubble itself.
	 *
	 * MEASURED corpus-wide (outputs/_measure_r246_sbblock.cjs, all 445 module dirs): of the
	 * 343 declined no-table speechBubble bundles, EXACTLY 55 match (TEDC401 33, TEDC402 21,
	 * SSCI104 1) — and the human gold builds an avatar+bubble row at **55 of 55**. The other
	 * decline classes (229 with no media at all, 22 non-iStock, 21 iStock-but-not-same-block)
	 * are left untouched: their gold agreement is only 49-72%, well short of a build.
	 *
	 * CONSERVATIVE BY CONSTRUCTION — the absorb runs only for a bundle the builder's new
	 * `no_table_image` branch can definitely finish: no table, no extra widget types, exactly
	 * one nameable iStock image (id pattern) and no video in media, a contiguous run of
	 * same-block items ending at the invocation that contains exactly ONE [image] tag and
	 * otherwise only the writer's descriptive instruction/noise spans. Anything else and the
	 * bundle is left exactly as it was — the image keeps rendering standalone and the widget
	 * keeps its honest hand-off box. Absorbed instruction spans are pushed to
	 * bundle.instructions so they still surface as red Writers Notes (§6 — never silently
	 * strip a documented instruction), just after the widget rather than before it.
	 *
	 * @param {object} bundle - the open speechBubble bundle
	 * @param {object[]} items - the page's item stream
	 * @param {number} tagIdx - index of the widget's invocation tag (the bundle's start)
	 */
	static #absorbSameBlockImage(bundle, items, tagIdx) {
		const cfg = DataService.Data.BoundaryBank?._meta?.member_rule?.same_block_image_absorb;
		if (!cfg || cfg.enabled === false) return;
		if (typeof process !== "undefined" && process.env && process.env.SBNOTBL_OFF) return;
		if (!(cfg.types ?? ["speechBubble"]).includes(bundle.type)) return;
		if ((bundle.tables ?? []).length || (bundle.extraTypes ?? []).length) return;

		// exactly ONE nameable iStock image already harvested from the block's links, no video
		const urls = (bundle.media ?? []).map((m) => String(m?.target ?? m?.text ?? ""));
		if (urls.some((u) => new RegExp(cfg.video_pattern ?? "youtu\\.?be|youtube\\.com|vimeo", "i").test(u))) return;
		const idRe = new RegExp(cfg.istock_id_pattern ?? "gm-?\\d{6,10}", "i");
		if (urls.filter((u) => idRe.test(u)).length !== 1) return;

		// SHARED PREDICATE — the members must be text the builder's no_table_image branch can
		// actually render. Consulted HERE, before anything is consumed, so the absorb can never
		// swallow an avatar the builder would then decline (which would trap the image inside a
		// hand-off box); one definition, so absorb and build cannot drift apart.
		const bTpl = DataService.Data.EmitTemplates?.interactive_builders?.speechBubble;
		if (!InteractiveBuilder.NoTableBubbleParagraphs(bundle.memberItems, null, bTpl?.no_table_image)) return;

		const blk = items[tagIdx]?.block;
		if (!blk) return;

		// walk UP over the CONTIGUOUS run of unconsumed items sharing that one source block
		const run = [];
		for (let s = tagIdx - 1; s >= 0; s--) {
			const prev = items[s];
			if (!prev || prev.consumedBy !== undefined || prev.block !== blk) break;
			run.unshift(prev);
			if (run.length > (cfg.max_absorb ?? 6)) return;      // an unexpectedly busy paragraph → bail
		}
		if (!run.length) return;

		// exactly one [image] tag; everything else must be the image's own descriptive
		// instruction/noise span (a structural tag means the paragraph carries a real
		// second element and the absorb would swallow it)
		const imgs = run.filter((it) => it.type === "tag" && it.parse?.primary?.tag === (cfg.image_tag ?? "image"));
		if (imgs.length !== 1) return;
		const ok = new Set(cfg.other_item_classes ?? ["instruction", "noise"]);
		for (const it of run) {
			if (it === imgs[0]) continue;
			if (it.type !== "tag" || it.parse?.primary || !ok.has(it.parse?.class)) return;
		}

		bundle.memberItems.unshift(...run);
		bundle.startIndex = tagIdx - run.length;
		bundle.sameBlockImage = imgs[0];              // the builder's no_table_image branch keys on this
		for (const a of run) {
			this.#harvestMedia(bundle, a);
			// keep the writer's descriptive note visible (it renders after the widget)
			if (a !== imgs[0] && a.type === "tag" && (a.parse?.class === "instruction" || a.parse?.instructionFragment)) {
				bundle.instructions.push(String(a.text ?? "").replace(/\s+/g, " ").trim());
			}
		}
	};

	/** The lead-in LABEL shape (data-driven, first match wins; else "prose"). */
	static #labelSignature(text, cfg) {
		const t = String(text ?? "").replace(/\*+/g, "").trim();
		if (!t) return "empty";
		for (const s of (cfg.label_signatures ?? [])) {
			if (new RegExp(s.re).test(t)) return s.name;
		}
		return "prose";
	};

	/**
	 * Picks the bank widget type for a canonical tag.
	 *
	 * HOW: lexicon tags map to one or more widget_types (e.g. carousel →
	 * [carousel, rotateBanner]). When there are several, the alias the
	 * writer actually used picks the variant: an alias sharing a word with
	 * a widget type's folded name wins (e.g. "rotating banner" → rotateBanner,
	 * "self check" → selfCheck). Otherwise the first listed type is used.
	 * Generic rule — no per-widget code.
	 *
	 * @returns {string} widget type key into the boundary bank
	 */
	static #widgetTypeFor(canonTag, alias, normaliser) {
		const resolved = this.#resolveWidgetType(canonTag, alias, normaliser);
		// VARIANT FOLDING: a VARIANT widget_type (rotateBanner/wordHighlighter) is the SAME main
		// widget as its parent — return the parent so the type flows to the parent's BUILDER /
		// manifest tier / boundary entry instead of being treated as a separate, un-built duplicate.
		// Data: BoundaryBank._meta.widget_type_taxonomy.variant_of; env VARFOLD_OFF.
		const tax = DataService.Data.BoundaryBank?._meta?.widget_type_taxonomy;
		if (tax?.variant_of && !(typeof process !== "undefined" && process.env && process.env.VARFOLD_OFF)) {
			return tax.variant_of[resolved] ?? resolved;
		}
		return resolved;
	};

	/**
	 * The UNFOLDED widget type from a canonical tag + the matched alias (the variant
	 * fold of #widgetTypeFor is NOT applied here). Lets a shared parent BUILDER branch on the
	 * sub-form the writer actually used — e.g. a [rolling/rotating/banner] tag folds to
	 * `carousel` for capture purposes, but the finished page builds a distinct rotateBanner
	 * STRIP layout for it, so the builder needs to know the opener was specifically the
	 * rotateBanner variant, not a generic carousel. Generic mechanism — no per-widget code.
	 *
	 * @returns {string} the pre-fold widget type key
	 */
	static #resolveWidgetType(canonTag, alias, normaliser) {
		const types = normaliser.GetWidgetTypes(canonTag);
		if (!types.length) return canonTag;              // e.g. "modal" (no bank type)
		if (types.length === 1) return types[0];
		let resolved = types[0];
		const aliasWords = new Set((alias ?? "").split(" "));
		for (const t of types) {
			// fold the camelCase type into words: rotateBanner → rotate banner
			const words = t.replace(/([A-Z])/g, " $1").toLowerCase().split(" ").filter(Boolean);
			if (words.some((w) => aliasWords.has(w))) { resolved = t; break; }
		}
		return resolved;
	};

	/**
	 * Weaves a hover/rollover/mouseover DEFINITION marker onto its nearest preceding word as
	 * the infoTrigger sentinel, for two shapes that the SINGLE-BRACKET inline trigger handling
	 * (see the "trigger"-keyed logic in ScanPage above) does NOT reach:
	 *   (A) COLON self-closed   "[hover: DEF]" / "[hover definition: DEF]" / "[rollover
	 *       definition: DEF]"   — the def is the payload after the FIRST colon, inside
	 *       the bracket. ("[Hover: …]" resolves to a plain [body] tag and SPLITS the paragraph;
	 *       "[hover definition: …]" resolves to an infoTrigger, but the "trigger"-keyed handling
	 *       elsewhere still DROPS the def via its own bare-marker guard.)
	 *   (C) MARKER-THEN-DEF      "[hover text] DEF"  — the bracket closes and the def
	 *       follows it inside the SAME red span (e.g. "**adjectives** [hover text] Describing
	 *       words. can make…").
	 * Returns true if it wove the definition in (the caller then `continue`s past the item);
	 * false leaves the item for normal handling. The U+E000…U+E001 sentinel +
	 * ContentConverter.#inlineMarkup machinery is the SAME mechanism the single-bracket inline
	 * trigger uses, so a bold anchor (**adjectives**) and a plain word (gestures) both build
	 * <span class="infoTrigger" info="DEF">anchor</span>.
	 *
	 * SAFETY: the head must start hover/rollover/mouseover (data head_pattern); a marker
	 * carrying "trigger" (skip_if_tag_keyword) is left to the single-bracket inline trigger
	 * handling instead; a marker that resolves to a NON-infoTrigger interactive widget
	 * (shapeHover, hover audio player…) is skipped; a marker with no recoverable def is left
	 * untouched (never a leaked literal). Data EmitTemplates.elements.hover_definition_inline;
	 * env HOVERDEF_OFF reverts.
	 */
	/**
	 * hover-weave HYGIENE: shared safety guards for BOTH sentinel-weave paths in this file (the
	 * single-bracket info_trigger_inline handling in ScanPage, and the hover_definition_inline
	 * handling just above). Without these guards, a small minority of weaves would anchor the
	 * sentinel onto the wrong host — e.g. gluing it onto a bare URL or media filename fragment
	 * (whose "word" is meaningless, like "png" or a random link ID) instead of a real word, or
	 * weaving in text that was actually a developer instruction rather than a genuine
	 * definition. Both guards only ever DECLINE a mis-weave (they never invent a new anchor out
	 * of nothing), so an already-correct weave is always left untouched. Data
	 * elements.hover_weave_hygiene; env HOVERHYG_OFF.
	 */
	static #hoverHygieneCfg() {
		const cfg = DataService.Data.EmitTemplates.elements?.hover_weave_hygiene;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.HOVERHYG_OFF) return null;
		return cfg;
	}

	/** A recovered hover DEF that reads as a writer INSTRUCTION is not a definition. */
	static #hoverDefIsInstruction(def) {
		const cfg = InteractiveScanner.#hoverHygieneCfg();
		if (!cfg || cfg.instruction_def_guard === false) return false;
		const re = new RegExp(cfg.instruction_cue_pattern
			?? "\\b(?:please|can you|could you|note to (?:dev|cs)\\b|dev team)\\b", "i");
		return re.test(String(def ?? ""));
	}

	/** True when a host candidate's trailing text is a MEDIA REFERENCE — a bare URL (+ "]"/")"
	 *  residue) or a media filename ("Masons day in Percentages.png") — not prose. The URL/media
	 *  machinery reads straight through a sentinel glued to such text, and its last "word" ("png",
	 *  "qJIHqK") is never the hover anchor. Pattern lives in data (media_tail_pattern). */
	static #urlTailHost(text) {
		const cfg = InteractiveScanner.#hoverHygieneCfg();
		if (!cfg || cfg.url_host_skip === false) return false;
		const re = new RegExp(cfg.media_tail_pattern
			?? "(?:https?:\\/\\/[^\\s<>&\"]+|\\.(?:png|jpe?g|gif|svg|webp|pdf|docx?|pptx?|xlsx?))[\\s\\]\\)]*$", "i");
		return re.test(String(text ?? "").trim());
	}

	static #weaveHoverDefinition(items, i, normaliser) {
		const it = items[i];
		if (!it || it.type !== "tag") return false;
		const cfg = DataService.Data.EmitTemplates.elements?.hover_definition_inline;
		if (!cfg || cfg.enabled === false) return false;
		if (typeof process !== "undefined" && process.env && process.env.HOVERDEF_OFF) return false;
		// TWO split/orphaned hover-bracket shapes the main colon/marker-then-def handling above
		// doesn't reach, both behind cfg.split_bracket + env HOVERSPLIT_OFF (independent of HOVERDEF_OFF):
		//   (A1) ORPHAN-LEAD-BRACKET — the marker's opening "[" was left in the preceding BLACK run,
		//        so the span begins "hover definition] DEF" (no leading "[") and head_pattern (^\[)
		//        fails. WT: "…specific areas or **regions** [🔴hover definition] a distinct…🔴". Restore
		//        the "[" (gated: head keyword at the very start + a "]" present) and strip the orphan
		//        "[" off the host so it never leaks as "regions [".
		//   (A2) DEF-IN-NEXT-ITEM — the marker carries NO usable def of its own (an UNCLOSED
		//        "[hover definition:" with no "]", OR a closed-but-empty "[hover definition]") and its
		//        blackAfter is empty; the def is the FOLLOWING red/black item ("DEF…]" + the paragraph
		//        continuation in ITS blackAfter). WT: "…topographies 🔴[hover definition:🔴 🔴the shape
		//        and features…🔴 on planet Earth…". Consume that item as the def. The def-in-BLACK form
		//        (no red def item) is NOT touched (left exactly as before — never a regression).
		const split = cfg.split_bracket;
		const splitOff = split && split.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.HOVERSPLIT_OFF);
		let rawMarker = String(it.text ?? "")
			.replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").trim();
		// ROUND 239 (Dev-Feedback R2, B3 — SCCH302-03 "boiling point"): the bare "[define: DEF]"
		// head joins the weave ("[hover define:" already worked because it starts with "hover").
		// cfg.define_heads.head_pattern is the base alternation + "define"; the toggle swaps
		// back to the base pattern. "definition" was MEASURED and DECLINED for this scanner
		// side (247 [definition…] spans are widget-member SUBTAGS — weaving them would break
		// widget capture); the render-stitch already carries it (round 201).
		// Data flag: elements.hover_definition_inline.define_heads   Env toggle: DEFINEHEAD_OFF
		const _dh = cfg.define_heads;
		const _dhOn = _dh && _dh.enabled !== false && _dh.head_pattern
			&& !(typeof process !== "undefined" && process.env && process.env.DEFINEHEAD_OFF);
		const headStr = (_dhOn ? _dh.head_pattern : null)
			?? cfg.head_pattern ?? "^\\[\\s*(?:hover|rollover|mouseover)\\b";
		const headRe = new RegExp(headStr, "i");
		// (A1) restore an orphaned leading "[" before testing the head
		let leadOrphan = false;
		if (splitOff && split.lead_orphan !== false && !rawMarker.startsWith("[") && rawMarker.includes("]")
			&& new RegExp(headStr.replace("\\[\\s*", ""), "i").test(rawMarker)) {
			rawMarker = "[" + rawMarker; leadOrphan = true;
		}
		// (A3) ANCHOR-BEFORE-BRACKET. After DocxExtractor merges the writer's adjacent red runs,
		// the marker span can read "ANCHOR [hover…: DEF]" — the hovered WORD sits inside the span,
		// before the bracket, so head_pattern (^\[) fails and left unhandled it would leak as a
		// plain CS note instead of becoming a hover span. Lift the anchor out (it weaves onto the
		// host below); rawMarker becomes the "[hover…]" marker for the def recovery. Runs AFTER
		// (A1) so an orphaned-"[" form (which the
		// A1 block has already turned into a "[hover…" leader) is never mistaken for an anchor.
		let leadingAnchor = "";
		if (splitOff && split.leading_anchor !== false && !rawMarker.startsWith("[")
			&& !(typeof process !== "undefined" && process.env && process.env.HOVERANCHOR_OFF)) {
			const am = rawMarker.match(new RegExp(
				"^(.*?\\S)\\s*(\\[\\s*(?:hover|roll\\s*-?\\s*over|rollover|mouse\\s*-?\\s*over|mouseover)\\b[\\s\\S]*)$", "i"));
			if (am && /\p{L}/u.test(am[1])) { leadingAnchor = am[1].trim(); rawMarker = am[2].trim(); }
		}
		if (!headRe.test(rawMarker)) return false;
		const skipKw = cfg.skip_if_tag_keyword ? new RegExp(cfg.skip_if_tag_keyword, "i") : null;
		if (skipKw && skipKw.test(rawMarker)) return false;        // a "trigger" form → handled by the single-bracket inline trigger logic instead
		const prim = it.parse?.primary;
		if (prim && prim.directive === "INTERACTIVE" && normaliser) {
			const wt = normaliser.GetWidgetTypes(prim.tag) ?? [];
			if (wt.length && !wt.includes("infoTrigger")) return false;   // a real widget, not a tooltip
		}
		// recover the DEFINITION (original case). Split the marker into its FIRST bracket +
		// whatever trails it INSIDE the span. A colon-def INSIDE the bracket ("[hover: DEF]",
		// "[hover on X: DEF]") is form (A) — text after the "]" (e.g. a sentence "." the writer
		// left inside the red span: "[hover: …]. ") is then sentence TAIL, NOT the def. Only when
		// the bracket holds NO colon-def is the text AFTER the "]" the def — form (C) "[hover text]
		// Describing words.". This ordering stops a trailing "]." from being mis-read as a 1-char
		// def (CEDO202 "sustainably" had info=".").
		let def = "", tail = "", consumeNext = false, contItem = it;
		const mk = rawMarker.match(/^\[([^\]]*)\]([\s\S]*)$/);
		if (mk) {
			const inner = mk[1].trim();
			const afterBracket = mk[2].trim();
			const colon = inner.match(/^[^:]*:\s*([\s\S]+)$/);
			if (colon && colon[1].trim()) { def = colon[1].trim(); tail = afterBracket; }   // (A)
			else if (afterBracket) { def = afterBracket; }                                  // (C)
		}
		// (A2) the marker yields no self-def — pull it from the FOLLOWING red/black item
		if (!def && splitOff && split.unclosed_next_item !== false && !String(it.blackAfter ?? "").trim()) {
			const nxt = items[i + 1];
			const nxtPrim = nxt && nxt.parse && nxt.parse.primary;
			const nxtOk = nxt && nxt.consumedBy === undefined && (nxt.type === "black"
				|| (nxt.type === "tag" && (!nxtPrim || nxtPrim.directive !== "INTERACTIVE")
					&& (nxt.parse?.class === "instruction" || nxt.parse?.class === "noise")));
			if (nxtOk) {
				const dtxt = String(nxt.text ?? "")
					.replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "")
					.replace(/^\s*\]\s*/, "").replace(/\s*\]\s*$/, "").trim();   // drop a stray late "]"
				if (dtxt) { def = dtxt; tail = ""; consumeNext = true; contItem = nxt; }
			}
		}
		// (A4) DEF-IN-OWN-BLACK-TAIL (ROUND 222c — module ENGJ403's standard hover idiom,
		// 12 occurrences measured: a red "[hover info ‘pitch’:" span with NO closing "]",
		// the DEFINITION as the span's OWN black tail ("When you share your script main
		// idea."), then a bare "]" red span whose own black tail continues the sentence.
		// The (A2) shape above requires an EMPTY own tail, so this form fell through and
		// leaked as a "Writers Note:" + a fragmented paragraph — the human weaves the
		// quoted word as <span class="infoTrigger">. The def comes from the marker's own
		// black tail; the stray "]" closer span is consumed and ITS black tail rejoins
		// the sentence. Data split_bracket.def_black_tail; env HOVERTAIL_OFF.
		if (!def && splitOff && split.def_black_tail !== false && !rawMarker.includes("]")
			&& !(typeof process !== "undefined" && process.env && process.env.HOVERTAIL_OFF)) {
			const ownBlack = String(it.blackAfter ?? "").trim();
			if (ownBlack) {
				def = ownBlack.replace(/\s*\]\s*$/, "").trim();
				it.blackAfter = "";
				const nxt = items[i + 1];
				const ntext = nxt ? String(nxt.text ?? "")
					.replace(/\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu, "").trim() : "";
				if (nxt && nxt.consumedBy === undefined && nxt.type === "tag"
					&& (nxt.parse?.class === "noise" || nxt.parse?.class === "instruction")
					&& /^\]$/.test(ntext)) {
					consumeNext = true; contItem = nxt;   // its black tail = the sentence continuation
				}
			}
		}
		if (!def) return false;                                    // no def → leave untouched
		// A recovered "def" that reads as a writer INSTRUCTION (e.g. "For each concept, please
		// have the rollover definitions below. Ngā mihi") is not a genuine definition: CONSUME the
		// marker exactly like the no-anchor branch does (the finished page strips instructions
		// like this). NOT a plain decline — if this marker's text happens to contain a word like
		// "image", ordinary handling elsewhere could mis-resolve it into an extra placeholder
		// <img> that then wrongly absorbs the NEXT bare URL out of its own line, corrupting an
		// unrelated link. The tail/continuation stay as plain body; nothing is reordered or
		// leaked. Data elements.hover_weave_hygiene.instruction_cue_pattern; env HOVERHYG_OFF.
		if (InteractiveScanner.#hoverDefIsInstruction(def)) {
			const cont = String(contItem.blackAfter ?? "").trim();
			it.type = "black"; it.text = ((leadingAnchor ? `${leadingAnchor} ` : "") + tail + (cont ? ` ${cont}` : "")).trim(); it.blackAfter = "";
			if (consumeNext) { contItem.type = "black"; contItem.text = ""; contItem.blackAfter = ""; }
			return true;
		}
		const IT0 = String.fromCharCode(0xE000), IT1 = String.fromCharCode(0xE001);
		const sentinel = IT0 + def + IT1;
		const blackCont = String(contItem.blackAfter ?? "").trim();
		// QUOTED NAMED ANCHOR (ROUND 222c, with A4 above): the writer names the hovered
		// word in quotes inside the marker head — "[hover info ‘pitch’: …" — so the
		// sentinel should attach to THAT word in the preceding host prose (its LAST
		// occurrence), not blindly to the host's final word. When the quoted word is
		// not found in the host, fall back to the plain last-word append (unchanged).
		const qm = rawMarker.match(/^\[[^\]:]*?['‘"]([^'’"‘\]]+)['’"]/);
		const quotedAnchor = qm ? qm[1].trim() : "";
		// what rejoins the line after the woven span: the sentence TAIL (attached directly, e.g.
		// a ".") then the following black continuation (space-separated).
		// For the ANCHOR-BEFORE-BRACKET form (A3 above), the hovered word was lifted off the marker
		// span; re-attach it to the host RIGHT BEFORE the sentinel so #inlineMarkup wraps THAT word
		// (not the host's own last word). e.g. host "He kākano ahau i ruia mai i" + " Rangiātea" +
		// sentinel(def).
		const append = (leadingAnchor ? ` ${leadingAnchor}` : "") + sentinel + tail + (blackCont ? ` ${blackCont}` : "");
		// anchor host = nearest PRECEDING item that still carries text (skip consumed empties).
		// A candidate whose trailing text is a bare URL (e.g. an [image]/[Image link] item's media
		// reference) can NEVER host the sentinel: the URL-detection machinery reads straight through
		// the private-use characters, corrupting the URL entirely and leaving stray characters
		// visible in the output. When the adjacent context is media rather than prose, there's no
		// real word to anchor the definition to — fall to the no-anchor branch below (the
		// definition is dropped, the marker is consumed). Data
		// elements.hover_weave_hygiene.url_host_skip; env HOVERHYG_OFF.
		let h = i - 1, host = null;
		while (h >= 0) {
			const cand = items[h];
			const ctext = cand.type === "black" ? cand.text : cand.blackAfter;
			if (String(ctext ?? "").trim()) {
				if (InteractiveScanner.#urlTailHost(ctext)) { host = null; break; }
				host = cand; break;
			}
			h--;
		}
		// strip a trailing orphaned "[" (A1) off the host so "regions [" never leaks
		const hostBase = (s) => { let b = String(s ?? "").replace(/\s+$/, ""); if (leadOrphan) b = b.replace(/\s*\[\s*$/, ""); return b; };
		// weave: quoted named anchor → the sentinel lands right after the LAST occurrence
		// of that word in the host prose; otherwise the historical append (last word).
		const weaveInto = (base) => {
			if (quotedAnchor) {
				const w = quotedAnchor.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
				const re = new RegExp(`\\b(${w})\\b(?![\\s\\S]*\\b${w}\\b)`, "i");
				if (re.test(base)) {
					return base.replace(re, `$1${sentinel}`)
						+ tail + (blackCont ? ` ${blackCont}` : "");
				}
			}
			return base + append;
		};
		if (host && host.type === "black") {
			host.text = weaveInto(hostBase(host.text));
		} else if (host) {
			host.blackAfter = weaveInto(hostBase(host.blackAfter));
		} else {
			// no usable anchor word → keep the lifted anchor + tail/continuation as plain body, drop the def
			it.type = "black"; it.text = ((leadingAnchor ? `${leadingAnchor} ` : "") + tail + (blackCont ? ` ${blackCont}` : "")).trim(); it.blackAfter = "";
			if (consumeNext) { contItem.type = "black"; contItem.text = ""; contItem.blackAfter = ""; }
			return true;
		}
		it.type = "black"; it.text = ""; it.blackAfter = "";
		if (consumeNext) { contItem.type = "black"; contItem.text = ""; contItem.blackAfter = ""; }
		return true;
	};

	/**
	 * The modifier = whatever meaningful text rode along with the
	 * invocation: the tag fragment's remainder ("autocheck"), plus any
	 * secondary non-subtag keywords ("[drag and drop quiz]").
	 *
	 * @returns {string} "" when there is none
	 */
	static #modifierFor(item) {
		const parts = [];
		for (const t of item.parse.tags) {
			if (t.remainder) parts.push(t.remainder);
		}
		// numbering already captured as activityId — strip leftover digits
		return parts.join(" ").replace(/\b\d+[a-z]?\b/g, "").replace(/\s+/g, " ").trim();
	};

	/**
	 * Files one member item into the bundle, splitting out writer
	 * instructions (they are BOTH bundled and red-flagged — §4 of the
	 * boundary rules: surface now, build later).
	 */
	static #collectMember(bundle, item, run) {
		bundle.memberItems.push(item);
		this.#harvestMedia(bundle, item);

		if (item.type !== "tag") return;
		const parse = item.parse;
		if (parse.class === "instruction" || parse.instructionFragment) {
			// the whole span is a writer instruction
			bundle.instructions.push(item.text.replace(/\s+/g, " ").trim());
		}
	};

	/**
	 * Absorb a DIFFERENT-type interactive invocation as a NESTED sub-bundle of the open
	 * host (the ROUND-95 mechanism, factored out at round 214 so both the per-type map
	 * (nested_interactive_absorb) and the numbered-series containment rule
	 * (numbered_series_absorb) share ONE implementation). The nested widget is recursively
	 * swallowed into its own sub-bundle (registered for its own cv2-index + manifest entry,
	 * later rendered in place — BUILT when its builder succeeds, else an honest nested
	 * placeholder), a {type:"nested"} marker is pushed into the host's members at the nested
	 * widget's position, and the host keeps walking AFTER the nested widget's members.
	 *
	 * @returns {number} the nested widget's end index (the host resumes there)
	 */
	static #absorbNestedSubBundle(bundle, items, j, next, extra, p, absolute, run, normaliser) {
		const subEntry = DataService.Data.BoundaryBank.interactives[extra] ?? null;
		const subHeadingTerm = subEntry ? subEntry.heading_is_terminator !== false : true;
		const sub = {
			type: extra, canonTag: p.tag,
			modifier: this.#modifierFor(next),
			activityId: null, headingText: "",
			openerItems: [], memberItems: [], tables: [],
			instructions: [], media: [], redFlags: [],
			positionContext: bundle.positionContext,
			startIndex: j, endIndex: j + 1, nested: true,
		};
		this.#collectMember(sub, next, run);             // the nested widget's own opener tag
		const subEnd = this.#swallowMembers(sub, items, j + 1, subHeadingTerm, absolute, run, normaliser);
		sub.endIndex = subEnd;
		bundle.memberItems.push({ type: "nested", nestedBundle: sub });
		(bundle.nestedBundles ??= []).push(sub);
		run.AddNote("info", "InteractiveScanner",
			`${bundle.type}: nested [${p.tag}] absorbed as a sub-bundle (${extra}); host continues.`);
		return subEnd;
	}

	/**
	 * Does a table carry an interactive invocation inside its cells?
	 * Scans the table's red spans through the normaliser; the first
	 * INTERACTIVE primary wins (data pattern 8: speech-bubble-in-table-row).
	 *
	 * @returns {Object|null} { type, canonTag } or null
	 */
	static #interactiveInTable(block, normaliser) {
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		const spans = [];
		for (const m of (block.text ?? "").matchAll(RED)) {
			const parse = normaliser.Parse(m[1]);
			if (parse.primary?.directive === "INTERACTIVE") {
				return {
					canonTag: parse.primary.tag,
					type: this.#widgetTypeFor(parse.primary.tag, parse.primary.alias, normaliser),
				};
			}
			spans.push(m[1]);
		}
		// ORPHAN FACE TABLE. A free-body table with NO invocation of its own, whose cells still
		// carry flipCard FACE tags (BOTH [front] AND [back], per the data's require list), is
		// orphan flip-card data: the finished page builds a flipCard from it, but without this
		// check the raw <table> with its literal [Front]/[Back]/[Image] tags would leak straight
		// into the output as visible text. Capture it as a flipCard bundle instead — the builder
		// declines this un-paired table form, so it renders as an honest placeholder with the
		// [tag] data INSIDE it (a developer reference, not a learner-facing leak), and the page
		// gets a WIDGET marker matching the finished page's shape. The CALL SITE only reaches here
		// for a table with consumedBy===undefined, so a face table already captured by a
		// [flipCard]/[Embedded] bundle is never touched twice. Data member_rule.face_table_capture;
		// env FACETABLE_OFF.
		const ftc = DataService.Data.BoundaryBank?._meta?.member_rule?.face_table_capture;
		if (ftc && ftc.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.FACETABLE_OFF)) {
			const joined = spans.join(" ");
			const need = ftc.require ?? ["front", "back"];
			if (need.every((t) => new RegExp("\\[\\s*" + t + "\\b", "i").test(joined))) {
				const wtype = ftc.widget_type ?? "flipCard";
				return { canonTag: wtype, type: wtype };
			}
		}
		return null;
	};

	/**
	 * The type of the FIRST DIRECT interactive invocation in a table's cells — the "direct"
	 * half of #interactiveInTable, WITHOUT that method's looser ORPHAN FACE TABLE inference, so
	 * this fires only on a literal [speechbubble]/[flipcard]/[tabs] invocation actually present
	 * in a cell, never on an orphan face/data table that merely looks like one.
	 *
	 * @returns {string|null} widget type, or null
	 */
	static #tableDirectInvocation(block, normaliser) {
		const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
		for (const m of (block.text ?? "").matchAll(RED)) {
			const parse = normaliser.Parse(m[1]);
			if (parse.primary?.directive === "INTERACTIVE") {
				return this.#widgetTypeFor(parse.primary.tag, parse.primary.alias, normaliser);
			}
		}
		return null;
	};

	/** Collects hyperlinks + pasted URLs from an item into bundle.media. */
	static #harvestMedia(bundle, item) {
		const block = item.block;
		if (block?.links?.length) {
			for (const l of block.links) {
				if (!bundle.media.some((m) => m.target === l.target)) bundle.media.push(l);
			}
		}
		// bare pasted URLs in the visible text (common for iStock/video)
		const text = item.type === "black" ? item.text : (item.blackAfter ?? "");
		for (const u of text.matchAll(/https?:\/\/[^\s\]\)"<>]+/g)) {
			if (!bundle.media.some((m) => m.target === u[0])) {
				bundle.media.push({ text: "", target: u[0] });
			}
		}
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { InteractiveScanner };
