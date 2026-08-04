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
 * OUTPUT NAMING (locked decision, 12/06/26):
 * {CODE}-00.html, -01.html, … in document order (the brief's contract
 * form; data: Emit_Templates.output_naming). The interactives manifest is
 * {CODE}_interactives.txt.
 *
 * ACKS PLACEMENT (policy, locked):
 * The acknowledgements block goes on the FIRST page only, after #footer.
 * ===========================================================================
 */

class PageAssembler {

	/**
	 * ROUND 243 (Dev-Feedback R6 — Chris, 2026-07-31): THE ONE SOURCE OF TRUTH
	 * for page output filenames, shared by the emit loop below AND the r226
	 * choice-page tile hrefs (ContentConverter.#choicePageTiles). The library
	 * convention the developer imports against is `{code}_{lesson}_{part}.html`
	 * (SCCH302_0_0.html); every page already carries exactly that number as its
	 * lessonLabel ("0.0" overview, "N.0" lesson, "N.M" sub-page, dotted writer
	 * lessons verbatim), so the filename is the label with "." → "_". The 12/06/26
	 * dash form `{code}-{NN}.html` is kept as legacy_page_file; env PAGENAME_OFF
	 * (or a page_file template without {page}) reverts byte-for-byte. A label
	 * collision (two pages resolving the same name — measured ~nonexistent; the
	 * splitter derives distinct labels) is disambiguated deterministically with
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
			// command-line harness never sets run.onProgress, so this whole block is a
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

		// "MODULE NAME" METADATA TITLE (ROUND 212 — the PNR101/102/104 MTK
		// "Te Aka Taumatua" bilingual family). This template has NO [TITLE BAR]
		// payload anywhere (the drop-down-menu table's [TITLE BAR] row is left
		// empty); the module's bilingual title lives in the front-matter metadata
		// table's "Module Name" row instead ("Ngā tau: 1 | Numbers: 1"). When no
		// title was derived at all, pipe-split that value and ship its halves in
		// PAYLOAD ORDER (Te Reo first on all three golds — the same positional
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

		// English-title BACKUP: the module must never ship with a Te-Reo-only
		// title. When the [TITLE BAR] gave a SINGLE title that does NOT match
		// the front-matter Course (i.e. it's the Te Reo name), promote that
		// lone title to the Te Reo slot and use Course as the English title
		// (front_matter_metadata.course_is_english_title_backup; verified
		// need on OSAI301: payload was only "Kirirarautanga Matihiko AI").
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
			// whole rule, falling back instead to an older, narrower check for what
			// counts as "placeholder text".
			run.englishTitle = course;
			run.teReoTitle = "";
			run.AddNote("info", "PageAssembler",
				`[TITLE BAR] held only placeholder text — using the front-matter Course "${course}" as the English title; no Te Reo title (the real one is not in the WT).`);
		} else if (tb?.single && course
			// a REAL title left after dropping a placeholder half (mixed bar) is the
			// English title — NOT Te Reo — so don't run the lone-title promotion on it
			&& !(titlePhOn && tb?.droppedPlaceholder)
			// The lone-title → Te Reo promotion below assumes that when the Writers
			// Template's [TITLE BAR] gives just ONE title, and that title differs from
			// the front-matter Course field, the lone title must be the Te Reo name
			// (this rule exists to handle a module like OSAI301, whose only title text
			// was "Kirirarautanga matihiko AI"). That assumption MISFIRES when the lone
			// title is actually the ENGLISH module title and the Course field just
			// happens to hold a broader subject name instead: one module (ENGC102) had
			// WT title "*KEEPING IT REAL*" and Course "Communication", and without this
			// guard the converter shipped <h1>Communication</h1> as the English title
			// (wrong — that's just the subject name) with "Keeping it real" wrongly
			// shoved into the Te Reo slot; another module (ENGS302) went even further
			// and put its Māori Course name "Te Ara Hou" into the ENGLISH slot. GUARD:
			// only promote the lone title to the Te Reo slot when it is ACTUALLY
			// written in Te Reo Māori (the Māori alphabet never uses the letters
			// b c d f j l q s v x y z; it only uses g/h/k/m/n/p/r/t/w plus vowels +
			// macrons, including the ng/wh digraphs). An English lone title is left as
			// the English title, with no Te Reo title invented out of nothing (the
			// real Te Reo title, if this module has one, simply isn't present anywhere
			// in this WT, so we don't guess at it). This has been checked against the
			// existing library of already-built modules with no regressions (see
			// outputs/_probe_lonetitle.cjs), and OSAI301 still gets promoted correctly.
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
		// ROUND 243: through the shared PageFileNames helper (the library
		// {code}_{lesson}_{part}.html form; env PAGENAME_OFF = the dash legacy).
		const filenames = PageAssembler.PageFileNames(run);
		// ROUND 228 (Chris — Change Ledger CL-0044, constraint 71): footer nav
		// hrefs ship EMPTY — prev/next/home alike; D2L wires the real links at
		// publish time. Measured: the gold library is 97% empty (the populated
		// remainder is the publish-time D2L quickLink wiring itself), so this
		// matches both the design-team directive AND the gold. The per-position
		// <li> composition (value_map) is unchanged — only the href fill.
		// Data footer.nav_links_empty.enabled; env FOOTEREMPTY_OFF reverts to
		// the round-8 sibling chaining.
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
				// that carry no actual content. TidyDeveloperNotes is "gate-neutral" —
				// this clean-up cannot affect the automated regression comparisons used
				// to check the converter's output against known-good modules, because
				// developer-comment markup is excluded from those comparisons anyway.
				// THE ORDER MATTERS: OmitPlaceholderResidue must run BEFORE
				// TidyDeveloperNotes, so an already-omitted placeholder prompt can never
				// be accidentally relocated or merged back in by the tidy-up pass.
				// DOMAIN LINK-TEXT DISPLAY (ROUND 213 — Chris, the BLL241 supervisor-
				// note screenshot): a link on a configured domain whose visible text
				// is itself a URL shows the domain's canonical display form
				// ("https://speldsa.org.au") while the href keeps the full deep URL.
				// Applied to the page BEFORE the acknowledgements block only — the
				// human developers keep the FULL URL text in their acknowledgements
				// (measured), and canonicalise it in the body (67/68 sites).
				// Data: Emit_Templates elements.link_text_display; env LINKTEXT_OFF.
				// NO-EMOJI RULE (ROUND 234 — Change Ledger CL-0051): after the note
				// tidy and BEFORE the link-text pass, EmojiStrip removes emoji from
				// the rendered writer content (Extended_Pictographic clusters minus
				// the ledger's exempt ticks & crosses; arrows become plain arrows;
				// 2+ consecutive emoji-prefixed lines become a <ul>; ONE red
				// disclosure note per affected page, built through the standard
				// NotesAndComments.redFlag machinery so the r219 note scheme and
				// NOTESCHEME_OFF apply to it like any other note). Applied to the
				// page BEFORE the acknowledgements block only — the acks keep
				// their verbatim oEmbed titles and the converter's own ❗ ack-todo
				// markers. Verbatim zones (cv2-interactive hand-off boxes,
				// cv2-note / cv2-comment quotes) are skipped inside the pass.
				// Data: Input_Doc_Rules.emoji_strip; env EMOJISTRIP_OFF.
				content: HtmlFormatter.Indent(
					(() => {
						const tidied = NotesAndComments.TidyDeveloperNotes(
							NotesAndComments.OmitPlaceholderResidue(html));
						const deEmoji = (seg) => ListsAndRuns.EmojiStrip(seg, () =>
							NotesAndComments.redFlag(
								DataService.Data.InputDocRules?.emoji_strip?.disclosure ?? "",
								run, "diagnostic"));
						const ai = tidied.indexOf("<div class=\"acks");
						return ai < 0
							? ListsAndRuns.LinkTextDisplay(deEmoji(tidied))
							: ListsAndRuns.LinkTextDisplay(deEmoji(tidied.slice(0, ai))) + tidied.slice(ai);
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
			content: ManifestBuilder.Build(run),
			kind: "manifest",
		});

		// ---- the distilled reference template (ROUND 249) --------------------
		// When the person uploaded reference HTML pages at conversion time (see
		// ModuleResolver.PrepareRun's reference-module block), the mined
		// structural profile ships as its own JSON output — the file Chris
		// needs to add that reference module to PageForge's templated modules.
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

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { PageAssembler };
