# KB_AMALGAMATION_STATUS.md — every front-facing HTML Convertor KB decision and where PageForge stands on it

**Written:** 14 September 2026 (Round 0b of the autonomous loop, `LOOP__Autonomous_Rounds.md` §1c).
**KB read:** `00-Other-TK-Resources/htmlconvertor-kb` at commit `ee2853c` (CL-0001 → CL-0095, constraints 1–92, families 14.1–14.12).
**PageForge read:** build 260618.84 (round 313), `data/Subject_Global_Parameters.json` (captured 2026-07-12 = doc-14 of 2026-07-09, refreshed round 244), `BUILD_CHANGELOG.md` (CL references up to CL-0070), and the CORPUS ITSELF — every gold and Claude page counted by `CONVERTER_V2/outputs/_measure_r0b_kbstatus.py` (`_r0b_kbfacts.json`) and the two signature sweeps (`_r0b_kbsignatures.json`, `_r0b_kbsignatures2.json`). Counts below are **gold pages / Claude pages** (2379 / 2102 non-acks pages) unless stated.

**How to read a status.**
- **LIVE** — the engine emits it today; the corpus shows it.
- **PARTIAL** — emitted on part of the population; the gap is named.
- **CAPTURED-INERT** — recorded in a data file (`Subject_Global_Parameters.json`, `master_enabled:false`) or fenced off; no output effect.
- **NOT CAPTURED** — nothing in the engine or data implements it.
- **NO SCOPE** — not one module in the corpus is in scope (a forward rule; nothing to regenerate).
- **N/A (mechanism)** — not front-facing (chat behaviour, mode triage, KB housekeeping): listed once, never a queue row.
- **UNVERIFIED** — no probe yet; the row says what would settle it.

**The order of authority (LOOP §1b):** a KB rule outranks the module's own gold within its scope. Where a row says the GOLD disagrees with the rule (e.g. the acks statements), the KB rule is still the target and the gate movement it causes is a NAMED OVERRIDE, not a regression.

---

## A. Universal constraints (00_MASTER_INSTRUCTIONS 00D/00E/00G/00H) — one row per constraint

| # | Rule (short) | Provenance | Scope in corpus | PageForge status | Carrier / evidence |
|---|---|---|---|---|---|
| 1 | Never change writer wording; permitted normalisations: menu-label casing (24), ALL-CAPS title → sentence case, **label-prefix strip** (`Lesson N` / `FUNdamental:` — CL-0095), emoji removal disclosed (74), MTK-quiz content silently omitted (65) | pre-ledger; CL-0051; CL-0082; CL-0095 | every module | **PARTIAL** — verbatim principle LIVE; emoji strip LIVE (r234); ALL-CAPS title UNVERIFIED; label-prefix strip **NOT CAPTURED** (Claude keeps a `Lesson N` body heading on 89 pages vs gold 18; `FUNdamental:` appears in 1 WT) | `ListsAndRuns.EmojiStrip`; no prefix-strip rule |
| 2 | No inline CSS/JS except the red-note style, BLL `text-transform: lowercase` on the title span, WJFUN highlight spans (CL-0066) | pre-ledger; CL-0010; CL-0066 | every module; BLL 110; WJ 0 | **LIVE** — red-note style on every note; BLL lowercase transform on 248 of 262 Claude BLL pages (gold 300 of 320); WJFUN NO SCOPE | `NotesAndComments.redFlag`; header titles |
| 3 | Never invent classes/structures | pre-ledger | every module | **LIVE** by construction (shapes live in `Emit_Templates.json`) | DATA OVER CODE |
| 4 | Never hide student content or designer notes in comments | pre-ledger; CL-0008/0010 | every module | **LIVE** — notes render red+bold with a source prefix (Writers Note 1573 pages, Red Flag 586, Designer/Developer To Do 497, Note from 141) | round 72 / 219 |
| 5 | Never render `[tags]` as visible text | pre-ledger | every module | **PARTIAL** — the literal-tag leak gate: 288 occurrences / 46 pages remain (round 313) | protected gate (`_structural_defect_audit.py`) |
| 6 | Never guess an interactive; red flag + visible fallback | pre-ledger | every module | **LIVE** — the hand-off box (`cv2-interactive`) + Writers Note | InteractiveBuilder null → placeholder |
| 7 | No `<span>` inside body h2–h5 (spans only on h1) | pre-ledger | every module | **UNVERIFIED** — the sweep's `<hN><span>` hits (360 Claude pages) are dominated by the canonical overview-menu `<h4><span>` (67); a body-region probe would settle it | — |
| 8 | Balanced divs | pre-ledger | every module | **LIVE** (HtmlFormatter) | — |
| 9 | Row/col grid for body content | pre-ledger | every module | **LIVE** | SkeletonBuilder |
| 10 | Derive the skeleton from the structural reference | pre-ledger | every module | **LIVE** (registries + PrecedenceResolver) | Granular/Module_Structure registries |
| 11 | Consult component sections before interactive HTML | pre-ledger | — | N/A (chat mechanism); PageForge equivalent = `Emit_Templates.interactive_builders` | — |
| 12 | Page-boundary validation | pre-ledger | every module | **LIVE** (PageSplitter; 1939 pairs) | — |
| 13 | Normalise tags before mapping | pre-ledger | every module | **LIVE** (TagNormaliser + `Tag_Lexicon.json`) | 9557/9557 tags |
| 14 | Writer tag decides the component, not table headers | pre-ledger | every module | **LIVE** (Decision Framework A1) | — |
| 15 | `noShuffle` only on explicit request | pre-ledger | mcq/dragAndDrop modules | **UNVERIFIED** (mcq builder r305 — check its shuffle default) | `interactive_builders.mcq` |
| 16 | Lesson pages: zero-padded lesson number chip; lesson's own title (→ 79) | pre-ledger; CL-0069 | 1534 paired lesson pages | **PARTIAL** — chip emitted on 2032 pages; padding format deliberately not codified by CL-0069 (gold `N.N` 1100 : `0N` 287); title → row 79 | — |
| 17 | Wide wrappers `col-md-12`/`col-12`/`col-md-11`; carousel viewer width contextual | pre-ledger; CL-0062 | interactive modules | **CAPTURED** (cl0062 "already satisfied live", r244) | `_universal_conventions.cl0062_carousel_viewer_width` |
| 18 | `[rotating banner]` → `rotateBanner` | pre-ledger | rotating-banner modules | **CAPTURED** (carousel builder's rotating-banner variant, r295) | InteractiveBuilder |
| 19–22 | Mode B reference-file rules (replace codes/titles, classify via 06, template attr from code, no custom CSS/stickyNav carry-over) | pre-ledger | — | N/A except **21 LIVE** — Claude `template=` distribution mirrors gold (1-3 622 · NCEA 528 · 7-8 274 · 4-6 258 · combo 242 · 9-10 178) | ModuleResolver |
| 23 | Lesson-page menu labels normalised to `<h5>` (We are learning: / I can: / You will show your understanding by:) | pre-ledger | lesson pages with a menu | **LIVE** — 216 / 247 / 260 Claude pages carry the three labels (gold 408 / 333 / 357; the difference is menu detection, tracked by the menu rounds) | MenuBuilder |
| 24 | Menu list items: no italics, lowercase start, verb form | pre-ledger | lesson menus | **LIVE** — 0 Claude menus carry `<li><i>` (gold 9 pages / 41 items; r145 `MENUITALIC_OFF`); casing/verb form UNVERIFIED | `MenuBuilder.stripTextItalic` |
| 25 | (superseded by 79) | CL-0069 | — | SUPERSEDED | — |
| 26 | D&D standard layout: text in `questionContainer`, images in `dragContainer` | pre-ledger | dragAndDrop modules (292) | **NOT CAPTURED** — no dragAndDrop builder (coverage chain) | — |
| 27 | DropQuiz standalone pairs use list layout | pre-ledger | dropdown modules | **UNVERIFIED** (dropDown builder r294 — check its layout choice) | `interactive_builders.dropDown` |
| 28 | Lowercase `<!doctype html>`; XHTML self-closing void tags | pre-ledger | every page | **CAPTURED-LIVE (round 315, 2026-09-15 — the loop's Round 2)** — `HtmlFormatter.Indent`'s `formatter.xhtml_voids` pass (`XHTMLVOID_OFF`): `<!doctype html>` on 2102/2102 Claude pages, every void self-closed ` />` (the form of the gold's 572 lowercase-doctype pages, 77% ` />`); the gold majority (1810 UPPER, plain voids) predates the rule — a KB-over-gold override, gate-neutral. Side effect: exposed and repaired the void-unaware `anchor_compare` parsers (the skeleton gate's pairing) — 15 more true pairs | `HtmlFormatter` + `Emit_Templates.formatter.xhtml_voids`; gate-neutral |
| 29 | Speech-bubble image-column padding sides (left → `paddingR`, right → `paddingL`; HPE head-only exception) | CL-0055; CL-0067 | speechBubble modules | **CAPTURED-INERT** (cl0055 "live emit deferred"; gold majority is unpadded — a KB override) | `_universal_conventions.cl0055_bubble_image_padding` |
| 30 | Ask for the image mode | pre-ledger | — | N/A (PageForge has its own Mode P/D control) | App.js |
| 31 | Mode D clean `<img>`; Mode P commented reference | pre-ledger | every module | **LIVE** | MediaBuilder.image |
| 32 | One image mode per conversion | pre-ledger | every module | **LIVE** | ConversionRun |
| 33 | Acks at the bottom of the overview page, after the footer | pre-ledger | every module | **LIVE** (413 Claude overview pages carry the block) | AcksBuilder |
| 34 | Raw docx: convert from the first `[TITLE BAR]`; ignore front matter | pre-ledger | every module | **LIVE** | DocxExtractor / PageSplitter |
| 35 | Media List optional; never supplies content or boundaries | pre-ledger | 153 two-file modules | **LIVE** | MediaListParser |
| 36 | Graded MCQ = `multiChoiceQuiz` family, never `multiQuiz` | pre-ledger | mcq modules | **CAPTURED** — the r305 mcq builder emits `multiChoiceQuiz` (4 pages built; 0 legacy) | `_verify_mcq.cjs` |
| 37 | No answer keys in comments; designer notes as visible red+bold with source prefixes; the permitted-comment list | pre-ledger; CL-0010/0013/0046 | every module | **LIVE** (r219 prefixes; `<!-- Lesson N.N -->` labels 413 pages; Mode P image comments) | NotesAndComments |
| 38 | `autoCheck` auto-applied on ECH / 1-3 / 4-6 templates | pre-ledger | 1-3 + 4-6 modules (880 Claude pages) | **UNVERIFIED** — check the built widgets' `autoCheck` attribute by template | builders |
| 39 | One-off designer overrides | pre-ledger | — | N/A (mechanism) | — |
| 40 | Comparison Mode | pre-ledger | — | N/A (mechanism) | — |
| 41 | Caption `<p class="captionText">` under an image | pre-ledger | image-caption modules (26 WTs tag captions) | **PARTIAL** — Claude 38 pages / 106 occ vs gold 155 / 557 | `elements.image` caption path |
| 42 | Numbered steps = semantic `<ol>` (+`start=N`), never typed numbers | CL-0030 area | activity modules | **PARTIAL** — `<ol start=` 3 Claude pages vs gold 156; typed `<p>1.` numbering remains on 28 Claude pages | ListsAndRuns |
| 43 | Activity ending in a dropbox/portfolio button carries the `dropbox` wrapper modifier (BLL carve-out: never) | pre-ledger; CL-0021 | every dropbox activity outside BLL (187 WT modules mention a dropbox) | **CAPTURED-LIVE (round 314, 2026-09-15 — the loop's Round 1)** — three rules now carry it: round 305's `body_region.activity_dropbox_postpass` (`ACTDROPBOX_OFF`) marks a box whose own span holds the upload button; round 308's `dbxbutton` builds the gold's "Upload to dropbox" button; and **round 314's `activity_wrapper.owned_activity_keeps_trailing_dropbox` (`ACTDBXINSIDE_OFF`) keeps a widget-owned activity box OPEN for the writer's trailing dropbox marker so the button lands INSIDE the box** (the gold's form 702/733 non-BLL, 1024/1024 BLL) and the postpass then marks it. Post-round corpus (depth-balanced activity spans, button inside or the immediate follower): non-BLL inside+marked **146**, inside-unmarked **8**, trailing **19** (the writer's marker sits AFTER the activity's end in the WT — current output correct) — a residue of 27 boxes, largest family TWHA 8, all below the 20-page queue floor; BLL inside 131 / trailing 37, **all plain** (the carve-out, honoured 100%). Pre-round the same measure read 208 non-BLL lacking. NAMED follow-up (§D): the dropbox button as the box's LAST child (gold 87% non-BLL / 97% BLL) | `ContentConverter.#dropboxTailHold` + `InteractiveBuilder.UploadBoxCandidate` + `Emit_Templates.activity_wrapper.owned_activity_keeps_trailing_dropbox`; `ActivitiesBuilder.activityDropboxPostpass`; **skeleton-visible** (`div.activity.dropbox`) |
| 44 | clickDrop `rel` omitted by default | pre-ledger | clickDrop modules | **CAPTURED** — Claude emits 0 `rel` (gold 49 pages carry it — pre-rule) | InteractiveBuilder |
| 45 | Acks wrapper `acks acksTemplate` (+`acksAI`) | pre-ledger; CL-0045; CL-0090 | every module (413 overview pages) | **CAPTURED-LIVE (round 317, 2026-09-15 — the loop's Round 4)** — `acks acksTemplate` on 394 Claude pages + `acks acksTemplate acksAI` on 19: 413/413 (gold: the old bare `acks` on 421 blocks — a KB-over-gold override) | AcksBuilder / `Acks_Formats.json` — see row 90 |
| 46 | Labelled diagrams = `imageLabel layout="labelLine"` | pre-ledger | labelled-diagram modules (gold 31 pages) | **NOT CAPTURED** (no builder; complex type) | — |
| 47 | Drop a body heading identical to the lesson `<h1>` (ignoring `Lesson N`) | pre-ledger | lesson pages | **PARTIAL** — Claude keeps a `Lesson N`-prefixed body heading on 89 pages (gold 18) | ContentConverter heading drop / relevel; skeleton-visible |
| 48 | Typing-quiz `placeholder="Type here"` | pre-ledger | typing modules (gold 283 pages) | **NOT CAPTURED** (no typing builder; the 13 Claude pages with `placeholder=""` are other inputs) | — |
| 49–51 | Update Mode, timestamps, ledger | — | — | N/A (mechanism) | — |
| 52 | Alt text: concise, never "stock photo"; iStock API name preferred | CL-0001 | every image | **LIVE** (r240 `img_alt_lazy`; 0 Claude alts contain "stock photo", gold 52 pages do) | MediaBuilder.FinishImg, `*_istock-acks.txt` map |
| 53 | iStock acks file authoritative when supplied | CL-0002 | modules with an acks file | **CAPTURED** (input-deferred; wired through the r240 map) | — |
| 54 | Video acks entry format + published title | CL-0003/0026 | modules with videos | **IN EFFECT** (verified round 219) | AcksBuilder |
| 55 | "Go to dropbox" / "Go to portfolio" labels; BLL/LS/HPE "Upload to Dropbox" | CL-0004; CL-0023 | dropbox modules | **LIVE — the text defect CLEARED (round 323, 2026-09-15, the loop's session-3 Round 10)**: one trailing full stop stripped from every `[button]`-family label (`buttons.label_trailing_stop`, `BTNSTOP_OFF`); was 441 of 3,052 Claude buttons on 221 pages / 90 modules (gold 9 of 5,553), now 29 | buttons emitter (`#buttonLabelTrim`); gate-neutral |
| 56 | Activity wrappers never `col-md-10` | CL-0007 | every activity | **CAPTURED** — 0 Claude occurrences (gold 271 pre-rule) | `_universal_conventions.cl0007` |
| 57 | Captured reviewer comments as `Note from {author}:` red+bold, in position | CL-0008/0010 | every module | **LIVE** (141 Claude pages) | `Comment_Authors.json` |
| 58 | Split Mode packaging | CL-0009/0011/0012 | — | N/A (PageForge's Page Stitcher consumes it; not a converter output) | pageforge-site stitcher |
| 59 | `Designer/Developer To Do:` prefix for deferred pieces | CL-0013 | every module | **LIVE** (497 Claude pages) | NotesAndComments |
| 60 | Subject global parameters apply within scope | CL-0014 | family modules (see B) | **CAPTURED-INERT** (`master_enabled:false`) | `Subject_Global_Parameters.json`, `SUBJECTPARAMS_OFF` |
| 61 | iStock ID = the gm-leading number | CL-0029/0091 | 365 WT modules carry dual-ID URLs | **LIVE** — 2536 Claude iStock filenames use the gm-leading number, **0** use the trailing one (101 ids come from single-ID URLs) | MediaBuilder filename rule |
| 62 | One interactive per activity; split + renumber + Red Flag | CL-0030 | multi-interactive activities | **CAPTURED-INERT** (cl0030 "live universal flip = measured decline", r229) | `_universal_conventions.cl0030` |
| 63 | Activity inner column `col-12`; one inner row at default width, split only when widened | CL-0036/0048/0077 | every activity | **LIVE** — Claude 6115 / 6115 inner columns are `col-12` (gold 6763 / 7499) | ActivitiesBuilder |
| 64 | Creative Services videos = Vimeo scaffold + To Do | CL-0037 | CS-video modules | **CAPTURED-INERT** (video kind non-derivable from V2's inputs — r233 decline) | `_universal_conventions.cl0037` |
| 65 | `[MTKquiz]` = numbered activity shell: title h3, instructions, To Do note, blank-href "Go to quiz"; **never the quiz content** | CL-0038; CL-0082 | 12 WT modules | **CAPTURED-LIVE (round 322, 2026-09-15, the loop's session-3 Round 9 — Chris's decision 3)**: the box holds ONLY h3 + instructions + the To Do note + the LAST-child "Go to quiz" button; the quiz content is omitted SILENTLY (`MTKQUIZOMIT_OFF` reverts; gate `_verify_mtkquiz.cjs` 61 shells / 23 modules defect 0). Residue NAMED: 8 Path-2b markers captured by a non-quiz container bundle keep the r232 form; 32 of 61 shells still box-less (no synthesised box / default `Quiz` h3). Was: the button LIVE (r232), the omission NOT CAPTURED (56 of 80 shells carried quiz markup) | `interactive_builders.mtk_quiz.omit_quiz_content`; `Tag_Lexicon._meta.mtk_quiz_retag.omit_quiz_content_drop`; skeleton-visible |
| 66 | Acks titles verbatim incl. ". stock photo" | CL-0039 | iStock modules | **UNVERIFIED** (compare Claude acks entry titles with the API map) | AcksBuilder |
| 67 | Canonical overview tab set (Overview → Knowledge → Practices → Information → Standards), `<h4><span>` titles, `<h5>` labels, omission rule, `overflowYScroll scroll="500"` for long panels | CL-0040 | tabbed overviews | **LIVE** for the tab set + headings (`tooltip="Overview"` 493 pages, `<h4><span>` 328 pages, `tab-pane` 249 pages); **scroll rule NOT CAPTURED** (0 vs gold 27 pages) | MenuBuilder (`Module_Menu_Scaffold.json`) |
| 68 | Supervisor `super-content-button` family; `row supervisor` outermost; legacy trio never emitted | CL-0041 | 93 WT modules | **LIVE** (265 Claude pages; 0 legacy) | ActivitiesBuilder / PanelsBuilder |
| 69 | (superseded by 79) | CL-0042/0069 | — | SUPERSEDED (its OSSC form is LIVE, r230) | — |
| 70 | OSSC `[Lesson Overview]` lead-in paragraph | CL-0043 | OSSC (3 modules) | **CAPTURED** ("verified already in effect", r230) | — |
| 71 | Footer nav `href=""` | CL-0044 | every page | **LIVE** — 0 Claude footer anchors carry an href (gold 68 pages do) | round 228 |
| 72 | Requested AI asset → `acksAI` in anticipation + To Do | CL-0045 | AI-request modules | **PARTIAL** (r241 `hasAi` decision; 19 Claude pages) | AcksBuilder |
| 73 | Acks group label `<!-- Lesson N.N -->` | CL-0046 | every module | **LIVE** (413 Claude pages; 0 `Page N.N`) | AcksBuilder |
| 74 | No emoji (ticks/crosses kept), removal disclosed | CL-0051 | every module (emoji in 452 WTs by the loose scan) | **LIVE (verify the residue)** — r234 `EMOJISTRIP_OFF`; the sweep still finds pictographic characters on 87 Claude pages / 901 occurrences, and it is NOT the 🔴 red-text marker (1 occurrence corpus-wide) — a residue probe should say whether they sit inside gate-excluded notes or in content | ListsAndRuns.EmojiStrip |
| 75 | Standalone `[external link]` → `externalButton`; inline → anchor; "Go to website" default label | CL-0050; CL-0078 | 16 WT modules tag external links; gold 417 pages carry externalButtons | **PARTIAL** — Claude 117 pages / 200 buttons; "Go to website" LIVE (108 pages) | buttons emitter |
| 76 | (Update Mode reporting) | CL-0052 | — | N/A (mechanism) | — |
| 77 | No `col-md-8` directly inside `col-md-8` | CL-0061 | every module | **CAPTURED** ("already satisfied live", r244 — 0 Claude violations, gold ≥ 8) | `_universal_conventions.cl0061` |
| 78 | Interactives Build Mode | CL-0068/0074 | — | N/A (PageForge's worklist hand-off IS the producer side) | ManifestBuilder |
| 79 | Lesson page `<h1><span>` = the lesson's own title (fixed source order; `Lesson N` stripped; module title only as a disclosed fallback; a second h1 only for the lesson's own bilingual pair) | CL-0069/0076 | 1534 paired lesson pages | **PARTIAL — the BILINGUAL-PAIR mechanism CAPTURED-LIVE (round 316, 2026-09-15, the loop's Round 3)**: a lesson whose own title is a pipe-joined pair now ships the lesson's English + Te Reo pair as two h1 spans, module code stripped, Te Reo first in `reoTranslate` modules (07D MTK rule 7) — gold two-span on 40/40 measured pages; Claude pipe-joined titles 45 → 0, code-prefixed lesson titles 30 → 4 (MXEO102's module-title fallback, the source-order seam). STILL QUEUED (the other c79 mechanisms, sizes from r0b): Claude falls back to the module title on 141 lesson pages (gold itself on 233; MXEO102's red-text `[H2] Lesson 1.0 …` source is one cause); the code-prefixed joined form; `Lesson One` word-numbers; trailing full stops; sub-page fallbacks (ANZH304 0.1–0.6); and the 118 gold pages that REPEAT the module pair (a human anti-pattern the KB rejects — never chase). **The `Lesson N` LABEL mechanism CAPTURED-LIVE (round 324, the loop's session-3 Round 11):** a label-only header title (`Lesson One` / `Lesson #3 Title` / `Lesson 5 continued`) takes the lesson's own title — 44 → 0 label titles, exact titles 528 → 550 over 1,247 paired lesson pages (`LESSONLABEL_OFF`); residue: Claude = module title while the gold has its own on 44 pages (no single derivable source ≥ 20), 8 trailing-punctuation titles, the pair order (decision 4). **The MTK source mechanism CAPTURED-LIVE (round 321, Chris's decision 2):** `header.mtk_titles` — the module title from the per-page `[H1]` repetition or the Module Code cell, Māori first on every page, both module titles on a lesson with no own title, no stray-heading titles (TRR overviews 13 → 0 without a title; `Finished!` titles 9 → 0) | ContentConverter header titles; **skeleton-visible** (h1 count) |
| 80–81 | PageForge Compare Mode | CL-0071/0072/0081 | — | N/A (mechanism) | — |
| 82 | `<body class="…">` on every page | CL-0075 | every page | **LIVE** — 0 Claude pages missing it (gold 99) | PageAssembler |
| 83 | No `loading="lazy"` inside moving widgets (banner, carousel, D&D, clickDrop, flipCard, memoryGame, sketcher) | CL-0083 | every image inside those hosts | **CAPTURED-LIVE (round 318, 2026-09-15 — the loop's Round 5)** — `HtmlFormatter.#lazyFreeHosts` (`formatter.lazy_free_hosts`, `LAZYHOST_OFF`): 0 of 2612 host-internal Claude images carry the attribute (were 2424 on 228 pages / 146 modules by the depth-walk measure); the gold agrees inside hosts (76.6% without) | r240 `img_alt_lazy` adds it everywhere; gate-neutral (attribute not in KEEP_ATTR) |
| 84 / 94 | The eight AI-Guidelines PDF tags → `embedPDF`/`centralFile` block; the renamed *Responding to Suspected Use* file | CL-0084; CL-0094 | **0 WT modules** carry the tags | **NOT CAPTURED, NO SCOPE** (forward rule; record only) | — |
| 85 | Three-part `[TITLE BAR]` → three `<h1><span>` (Languages only) | CL-0085 | 5 WT modules with two pipes (the Languages cohort) | **NOT CAPTURED** (< 20 pages; record) | header title split |
| 86–88, 91 | Admin Mode, the front-facing test, designer-facing output, admin output policy | CL-0086/0087/0088/0092 | — | N/A (mechanism) | — |
| 89 | `learningSupport` on `<html>` for every X-prefixed code | CL-0089 (locked admin) | 36 modules / 228 Claude pages | **CAPTURED-LIVE (round 319, 2026-09-15 — the loop's Round 6)** — `skeleton.html_class_cohorts` (`HTMLCOHORT_OFF`): 228 of 228 X pages carry it, 0 non-X pages (gold 72 of 250 — the KB outranks) | PageAssembler shell; gate-neutral (the `<html>` tag is outside the skeleton) |
| 90 | `acksTemplate`/`acksAI` generate their statements — never type the apology, AI or copyright lines (`currentYear` too); keep only "All other images ©" | CL-0090 (locked admin) | every module (413 overview pages) | **CAPTURED-LIVE (round 317, 2026-09-15 — the loop's Round 4)** — the round-241 omit now applies to every block (`standing_items.kb_template_form`, `ACKSTEMPLATE_OFF`): 0 of 413 Claude blocks type the apology / copyright / AI statements, 413 keep the catch-all (gold types them on 443 — pre-rule; a NAMED override, skeleton −0.024pp on 387 named pages, identical net of them) | `Acks_Formats.standing_items.template_variant_omit` (`ACKSBOILER_OFF`) — extend to every block; corpus-wide; **skeleton-visible** (two `acksLesson` divs fewer) |
| 92 | `jp-text` / `ch-text` / `pinyin` on every run (macron boundary; module language decides shared Han) | CL-0093 (locked admin) | 3 WT modules with CJK (CHFUN); 7 Claude pages | **NOT CAPTURED** (0 Claude spans; gold 1245 `ch-text` + 1083 `pinyin` on 5 pages) — < 20 pages; record | ListsAndRuns.inlineMarkup |
| (95) | Label-prefix strip on body headings (constraint 1 amendment) | CL-0095 | see row 1 | **NOT CAPTURED** (see rows 1 / 47) | — |

---

## B. Subject global parameters (14_SUBJECT_GLOBAL_PARAMETERS) — one row per family, the conventions listed

All ten families are CAPTURED in `data/Subject_Global_Parameters.json` (round 218/244) with `overrides_gold:true`, behind `master_enabled:false` — **CAPTURED-INERT** unless a row says otherwise. Corpus presence is from `Module_Structure_Index.json` (gold modules / with a Claude dir / gold pages).

| Family | Corpus presence | Conventions (kind) | Status | Notes |
|---|---|---|---|---|
| 14.1 Languages P1–4 | 5 / 5 / 5 (CHFUN01–05; JPNFUN none yet) | all-combo (CL-0033); central `imageCentral` assets (CL-0032); Audiovisual package tag family + finalised registry `14C` (CL-0070); set characters repeated; **three-part title** (CL-0085); stickyNav every page; language fonts (CL-0093) | all-combo **LIVE** (cl0033, r231); the rest **CAPTURED-INERT** (family `active:false`); three-part title and language fonts **NOT CAPTURED** | the CHFUN modules ARE Fundamentals-shaped (`<body class="fundamentals …">`) — the sub-type comes from the body class, as the KB says |
| 14.2 Pathways L1 | 0 / 0 / 0 | sections nav; 3 lessons × sub-parts; persona pattern; deferred persona/overview/K-P statements | **NO SCOPE** | — |
| 14.3 Taonga (Arts) | 10 / 10 / 77 (ART, ARFUN) | FUN-style intro + clickable lessons; side-nav tabs; A–F lesson layout; unique overview; **tui per-phase folders/poses, deferral lifted** (CL-0073) | **CAPTURED-INERT** (`active:false`); the CL-0073 path form (`tui_characters/phase_{N}/tui_{P}.jpg`) is NOT in the July capture — diff item | 0 gold pages carry `tui_characters/` |
| 14.4 CED Phase 5 | 6 / 6 / 76 | 3-tab overview; dictionary alert; sticky-nav dictionary links; `alert cultural layout="combined"`; flipCard `.noBG`; PDFs deferred **except the AI-Guidelines eight** (CL-0084) | **CAPTURED-INERT** (`active:true` in the data, master off); `alert cultural combined` 0 Claude vs 39 gold pages; `flipCard noBG` 14 vs 161 | the AI-PDF carve-out is NOT in the July capture — diff item |
| 14.5 H&PE FUNdamentals | 15 / 15 / 15 (HPFUN, PHEFUN) | 5–6 RHS tabs; intro first, reflection last; one engagement quiz | **CAPTURED-INERT** | structural recognition is 06 §3.3 (LIVE: `fundamentals` body class 80 Claude pages) |
| 14.6 LS | 18 / 18 / 124 (XLP, XDLS) | `learningSupport` (→ constraint 89); hoa ako terminology; no tab navs; clickDrop choicePage layout; speech-bubble prompts; 6-activity pattern; dropbox copy; move-forward alerts; XLP unique overview | **CAPTURED-INERT** (`active:true`, master off); `learningSupport` **NOT CAPTURED** (row 89) | — |
| 14.7 BLL | 110 / 92 / 320 | `template="1-3"` for BLL2xx (CL-0035); Sassoon font hook; page-1 animated-person video scaffold; elkonin boxes; green activity boxes; **`.dropbox` never added to `.activity`**; "Upload to Dropbox"; book-style story carousel; timer; BLL lowercase title transform | **CAPTURED-INERT** (`active:true`, master off) except the lowercase title transform (LIVE, 248 of 262 pages) and the dropbox carve-out (LIVE — 292 of 292 Claude BLL dropbox activities carry no modifier); template level per sub-series **UNVERIFIED** | the carve-out matters for the row-43 queue item: BLL activities are EXCLUDED from the modifier rule |
| 14.8 HPE content | 22 / 21 / 192 (HES, PHE, PES, HPRE) | intro-page overview; lesson-summary alert; stickyNav; ≤3 dropboxes; quiz rules; phase-specific checkpoint/celebration copy; **characters + `health & PE characters/` paths, head-only `paddingR` exception** (CL-0067, captured r244); **celebration gif DELIVERED** (CL-0080) | **CAPTURED-INERT**; the gif delivery (deferral retired) is NOT in the capture — diff item | 0 Claude pages carry `imageCentral`; gold 97 |
| 14.9 BLLR | 1 / 1 / 7 (BLLR201) | phase 2 `template="4-6"`; bookworm avatar by code range; deferred art/audio; secret-shelf red note | **CAPTURED-INERT**; < 20 pages | — |
| 14.10 MiW / WJ | 0 / 0 / 0 | NZ map; FUN tiles; side-nav tabs; Kea character; `[MTK Quiz]` precedence (CL-0058); audioImage grids (CL-0059); wordSelect span (CL-0060); inline audio button (CL-0063); fit-based wrapper widths (CL-0065); static highlight spans (CL-0066) | **NO SCOPE** (captured for the future) | — |
| 14.11 cross-cutting | — | "Upload to Dropbox" (BLL/LS/HPE); BLL-only dropbox carve-out; stickyNav in the head (Languages / CED P5 / HPE); deferred-item red-note convention | label **LIVE** (797 Claude buttons, 420 with a stray full stop); stickyNav **NOT CAPTURED** — 5 Claude pages vs 1502 gold; gold uses it on ≥ 80% of pages in 30 series (AGH, HIS, MX*, ENG*, CED*, HES, PHE …) and on 0% in TRR/PNR/XLP/OSSC/HPRE — a per-series convention beyond the KB's three families; red-note convention **LIVE** | stickyNav is gate-neutral (in `<head>`) |
| 14.12 Technology | 8 / 8 / 8 (TEFUN) | five strand icons `Technology/strand/active-*.svg`; shared `congradulations/` gif; `col-8` text + `col-4` gif layout | **NOT CAPTURED** — the family is absent from the July capture (added to the KB 13 Aug, CL-0080); 0 Claude pages carry either asset | new family — diff item |

**The 14_ text diff since the 9-July capture** (what `Subject_Global_Parameters.json` does not yet hold): CL-0067 HPE characters (captured r244 ✓); CL-0070 Languages AV package finalised + `14C` registry + CHFUN/JPNFUN reference points; CL-0073 Taonga tui per-phase folders, art deferral lifted; CL-0080 Technology family (new §14.12) + the HPE celebration-gif deferral retired; CL-0084/0094 the AI-Guidelines PDF carve-out in §14.4; CL-0085 the Languages three-part title; CL-0089 `learningSupport` by X prefix (re-scoped in §14.6); CL-0093 language fonts (§14.1 cross-reference); §14.11 unchanged in substance.

---

## C. The change ledger CL-0001 → CL-0095 — lane and pointer

Front-facing = changes the generated HTML/CSS (constraint 87). Each front-facing row points at the constraint or family row above that carries its status.

| CL | Lane | Points to | Status |
|---|---|---|---|
| 0001 alt text | FF | c52 | LIVE |
| 0002 iStock acks file | FF | c53 | CAPTURED |
| 0003 video acks format | FF | c54 | IN EFFECT |
| 0004 "Go to dropbox" label | FF | c55 | LIVE |
| 0005 col-md-10 (reverted) | FF | c56 | SUPERSEDED by 0007 |
| 0006 Update Mode routing | mech | — | N/A |
| 0007 wrapper widths | FF | c56/c17 | CAPTURED |
| 0008 reviewer comments | FF | c57 | LIVE (prefix per 0010) |
| 0009 / 0011 / 0012 Split Mode | mech (packaging) | c58 | N/A |
| 0010 red-note prefixes | FF | c37 | LIVE |
| 0013 To Do prefix | FF | c59 | LIVE |
| 0014 file 14 created | mech | — | N/A |
| 0015 Languages | FF | 14.1 | CAPTURED-INERT |
| 0016 Pathways | FF | 14.2 | NO SCOPE |
| 0017 Taonga | FF | 14.3 | CAPTURED-INERT |
| 0018 CED P5 | FF | 14.4 | CAPTURED-INERT |
| 0019 H&PE FUN | FF | 14.5 | CAPTURED-INERT |
| 0020 LS | FF | 14.6 | CAPTURED-INERT |
| 0021 BLL | FF | 14.7 | CAPTURED-INERT (carve-out LIVE) |
| 0022 HPE content | FF | 14.8 | CAPTURED-INERT |
| 0023 "Upload to Dropbox" | FF | c55 / 14.11 | LIVE |
| 0024 BLLR | FF | 14.9 | CAPTURED-INERT |
| 0025 MiW/WJ | FF | 14.10 | NO SCOPE |
| 0026 / 0027 video title | FF | c54 | IN EFFECT |
| 0028 Exclusion 1 | mech | — | N/A |
| 0029 iStock gm-leading ID | FF | c61 | LIVE |
| 0030 one interactive per activity | FF | c62 | CAPTURED-INERT |
| 0031 (reverted) | FF | 14.7 | SUPERSEDED by 0035 |
| 0032 Languages central images | FF | 14.1 | CAPTURED-INERT |
| 0033 Languages all combo | FF | 14.1 | LIVE (inert guarantee) |
| 0034 (superseded) | FF | 14.3 | SUPERSEDED by 0073 |
| 0035 BLL2xx = 1-3 | FF | 14.7 | UNVERIFIED per sub-series |
| 0036 widened-activity text width | FF | c63 | SUPERSEDED by 0077 |
| 0037 CS Vimeo | FF | c64 | CAPTURED-INERT |
| 0038 MTKquiz button | FF | c65 | LIVE (button) |
| 0039 acks published title | FF | c66 | UNVERIFIED |
| 0040 canonical overview menu | FF | c67 | LIVE (scroll rule not) |
| 0041 supervisor family | FF | c68 | LIVE |
| 0042 OSSC lesson h1 | FF | c69→79 | LIVE (OSSC) |
| 0043 OSSC lead-in | FF | c70 | CAPTURED |
| 0044 footer hrefs | FF | c71 | LIVE |
| 0045 acksAI anticipation | FF | c72 | PARTIAL |
| 0046 Lesson N.N label | FF | c73 | LIVE |
| 0047 / 0049 / 0056 / 0057 / 0064 / 0079 exclusions | mech | — | N/A |
| 0048 prose/interactive rows | FF | c63 | SUPERSEDED by 0077 |
| 0050 external link button | FF | c75 | PARTIAL |
| 0051 no emoji | FF | c74 | LIVE (residue to verify) |
| 0052 / 0053 Update Mode | mech | — | N/A |
| 0054 `js/…` includes | FF | (crossword/wordFind head includes) | UNVERIFIED (PageForge's stitcher injects them) |
| 0055 bubble padding | FF | c29 | CAPTURED-INERT |
| 0058 WJ MTK precedence | FF | 14.10 / c65 | NO SCOPE |
| 0059 / 0060 / 0063 / 0065 / 0066 WJFUN rules | FF | 14.10 | NO SCOPE |
| 0061 no col-8 in col-8 | FF | c77 | CAPTURED |
| 0062 carousel viewer width | FF | c17 | CAPTURED |
| 0067 HPE characters | FF | 14.8 | CAPTURED-INERT (r244) |
| 0068 Interactives Build Mode | mech | c78 | N/A |
| 0069 lesson h1 universal | FF | c79 | PARTIAL → QUEUE |
| 0070 Languages AV finalised | FF | 14.1 / 14C | NOT CAPTURED (post-capture) |
| 0071 / 0072 / 0081 PageForge Compare Mode | mech | — | N/A |
| 0073 tui folders | FF | 14.3 | NOT CAPTURED (post-capture; 0 scope pages) |
| 0074 Mode 6 cadence | mech | — | N/A |
| 0075 body tag | FF | c82 | LIVE |
| 0076 retired-wording sweep | mech (c79 reinforced) | c79 | — |
| 0077 inner col-12 + conditional split | FF | c63 | LIVE |
| 0078 "Go to website" | FF | c75 | LIVE |
| 0080 Technology + gif delivered | FF | 14.12 / 14.8 | NOT CAPTURED |
| 0082 MTK quiz shell, no content | FF | c65 | NOT CAPTURED (content) |
| 0083 lazy-load exclusion | FF | c83 | NOT CAPTURED |
| 0084 / 0094 AI PDFs | FF | c84 | NO SCOPE |
| 0085 three-part title | FF | c85 | NOT CAPTURED (< 20 pages) |
| 0086 / 0087 / 0088 / 0092 Admin Mode family | mech | — | N/A |
| 0089 learningSupport | FF | c89 | NOT CAPTURED → QUEUE |
| 0090 acks statements | FF | c90 | NOT CAPTURED → QUEUE |
| 0091 iStock ID (re-asserted) | FF | c61 | LIVE |
| 0093 language fonts | FF | c92 | NOT CAPTURED (< 20 pages) |
| 0095 label-prefix strip | FF | c1 / c47 | NOT CAPTURED |

---

## D. The KB queue — NOT CAPTURED / PARTIAL rows with ≥ 20 in-scope pages, ranked (LOOP §1c: these outrank gold-matching classes in the same area)

| Rank | Row | In-scope population (Claude) | Gate visibility | Derivable from | Note |
|---|---|---|---|---|---|
| ~~1~~ | c43 dropbox wrapper modifier + placement | **SHIPPED round 314** (65 pages / 43 modules; residue 27 non-BLL boxes, below the floor) | skeleton-visible | — | see row 43. Follow-up candidate (not yet queued — needs its own PICK/measure): "the dropbox bundle terminates its activity" (gold last-child 87% non-BLL / 97% BLL; Claude post-r314 boxes with content after the button: to be sized) |
| ~~2~~ | c90 + c45 acks wrapper class + no typed statements | **SHIPPED round 317** (394 pages, full regeneration; 413/413 blocks in the KB form) | skeleton −0.024pp on the 387 named pages, identical net of them | — | see rows 45 / 90 |
| 3 | c79 lesson h1 = lesson title | **the bilingual-pair mechanism SHIPPED round 316** (45 pages / 17 modules); the remaining source-order / fallback mechanisms: 141 module-title fallbacks + the MXEO102 class, sized per mechanism before the next PICK | skeleton-visible (h1 count) | the boundary tag / `[H2]` / `[Lesson Overview]` source order | the "227 missing dual-h1 pages" figure was inflated by the 118 gold pages that repeat the MODULE pair (the KB rejects those); the lesson-scoped pair population was 45 |
| ~~4~~ | c89 `learningSupport` on X-prefixed `<html>` | **SHIPPED round 319** (228 pages / 35 modules) | gate-neutral | — | see row 89 |
| ~~5~~ | c83 no `loading="lazy"` in moving widgets | **SHIPPED round 318** (2424 images / 228 pages / 146 modules, full regeneration) | gate-neutral | — | see row 83 |
| ~~6~~ | c28 lowercase `<!doctype html>` + XHTML self-closing voids | **SHIPPED round 315** (2102 pages, full regeneration) | gate-neutral | — | see row 28; the pairing-parser repair rode along |
| 7 | c47 / c95 `Lesson N` body-heading strip / drop | 89 pages | skeleton-visible | the heading's own prefix vs the `<h1>` | |
| 8 | c65 MTK quiz content omission (CL-0082) | 56 shells (12 WT modules) | skeleton-visible (override vs gold) | the `[MTKquiz]` marker | silent omission, no note |
| 9 | c55 button labels ending in a full stop | 420 buttons | gate-neutral (text) | the label's own trailing punctuation | |
| 10 | 14.11 stickyNav include | 33 KB-scoped modules; a ≥ 80% gold convention in 30 series | gate-neutral (head) | family / series convention | |
| 11 | c67 `overflowYScroll` on long panels | 27 gold pages | skeleton-visible (class) | panel length | small |
| ~~—~~ | 05D universal button form — every call-to-action `[button]` is `<a href target=_blank><div class=button>` (+ constraint 65's blank quiz href) | **SHIPPED round 326** (713 pages / 286 modules, full regeneration; Claude bare buttons 1,800 → 338, 285 lost hyperlinks recovered) | skeleton-visible (`<a>` node; +0.057pp, ≥50 −1 named) | — | not a numbered constraint — the component doc's one button form; the reveal-type labels (`Check answers` / `Reset`) stay the gold's JS `button clickDrop` (its own round); constraint 55's label half (`Quiz` / `Portfolio` / `Dropbox` bare labels, 50 pages) is a queue candidate |
| — | c92 language fonts (7 pages), c85 three-part title (5 modules), c84 AI PDFs (0), 14.3/14.8/14.12 central assets (0 Claude pages) | < 20 | — | — | recorded, not queued |

---

## E. Sources and how to refresh

- Re-run `python3 CONVERTER_V2/outputs/_measure_r0b_kbstatus.py` (≈ 55 s under WSL) after any regeneration or KB commit; it writes `outputs/_r0b_kbfacts.json`. The two signature sweeps (`_r0b_kbsignatures.json`, `_r0b_kbsignatures2.json`) were produced by the session's scratch scripts and are kept as evidence files.
- The KB's own `12G` amalgamation log starts at CL-0086; the CL-0001–CL-0085 backfill it promises has not been run there — this file is PageForge's side of that backfill.
- When a queue row ships, set its status here AND update the `PageForge status:` line of the matching `12G` entry in the KB repo (the only field that log edits in place).
