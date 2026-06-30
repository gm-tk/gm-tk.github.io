# PageForge — Cowork Build Instructions

> **What this is.** A complete, self-contained brief for a Claude Cowork project whose goal is to build a **brand-new, 100% client-side web app** (the rebuilt PageForge) that takes the **Module Development** functionality from the existing PageForge V1 as its foundation, **removes everything tied to V1's deprecated "Standard" mode**, and adds two new capabilities: **native Word comment capture** and a **Page Stitcher**.
>
> This app is an **interim production replacement** for the current online PageForge while a separate ground-up rewrite ("PageForge V2") is developed elsewhere. It must ship and serve real users now.
>
> Treat this document as the project's source of truth. Where it specifies an algorithm or contract, follow it. Where it leaves an output format open, **design it, justify it, and validate it against the available corpus** (see §2).

---

## 1. Mission, in one paragraph

Build a clean static web app that a designer uses to prepare the inputs for a downstream Claude Project (the one that turns parsed instructions into finished HTML modules). On the **Module Development** screen the user drops a Writer's Template `.docx` and, optionally, a Media List `.docx`; pressing **Convert** produces, and offers as one-press downloads, (a) the **parsed Writer's Template `.txt`** — now carrying the reviewers' actionable Word comments as red notes placed in context — and (b) the **parsed Media List `.txt`**. A separate **Page Stitcher** screen takes a base module-homepage HTML plus the individually-generated lesson HTML files and splices them into one unified, downloadable HTML file. Everything runs entirely in the browser; nothing is uploaded, stored, or sent to a server.

---

## 2. Resources you (Cowork) have, and how to use each

You have access to the full body of material that has been used to develop PageForge V2. Use it as follows.

**a. The existing PageForge V1 source** — GitHub repo `gm-tk/gm-tk.github.io` (a GitHub Pages static site). This is your **foundation**: you will copy a specific subset of its files verbatim and discard the rest (see §4). Clone it read-only; do not push to it.

**b. The PageForge V2 codebase + its developer docs** — in particular `Comment_Capture_Process_Explained.md` (provided). This is the **authoritative algorithm reference for the comment-capture feature**. V2 is a *different architecture* from V1 (it emits HTML through a `ContentConverter`/`DocxExtractor` stack; V1 emits plain-text `.txt` through `DocxParser` + `OutputFormatter`). So you **port the algorithm and the data, not the integration code** (see §6). Its `data/Comment_Authors.json` whitelist and its `omit_boilerplate` / `action_keep` regexes carry over directly as data.

**c. The full corpus of finalized HTML** — every HTML file for every module the team has ever produced. Use it as a **validation oracle**: a smoke check that the comment-author whitelist resolves the great majority of real comments (§6.6), and a real-module round-trip for the Page Stitcher (§7).

---

## 3. Hard invariants (do not violate)

1. **100% client-side.** All parsing, conversion, and stitching happen in the browser. No backend, no network calls touching user files, no storage. The site must remain a deployable static bundle (GitHub Pages). Keep the existing "100% Client-Side / No Data Stored" framing.
2. **Content fidelity.** Writer-supplied text passes through unchanged. Never rephrase, correct, or auto-edit writer content. Comment notes are *additive metadata*, never edits to the source text.
3. **No browser storage** in the app (no `localStorage` / `sessionStorage`); keep state in memory for the session.
4. **Carried-over V1 behavior is preserved and stays tested.** The Module Development conversion you inherit already works and ships with passing tests; do not regress it.

---

## 4. The foundation: what to carry over from V1, what to drop

### Carry over verbatim (then adapt only as the features require)

JavaScript modules (`js/`):

- `docx-parser.js` — `DocxParser`. The shared `.docx` reader (JSZip), `_findContentStart()` `[TITLE BAR]` boundary detection, namespace-aware DOM walk. **Foundation for comment capture** (it already opens the zip and walks `document.xml`).
- `formatter.js` — `OutputFormatter`. Produces the parsed-`.txt` envelope (`formatAll` / `formatContent` / `formatMetadata`) and the red/bold/table markers the downstream Claude Project reads. **Foundation for inserting comment notes** (reuse its red-text marker).
- `output-manager.js` — `OutputManager`. The download primitive (`addFile` / `downloadFile`, Blob + object URL).
- `media-list-converter.js` — `MediaListConverter`. Structural media-table extraction to `.txt` (header-row detection, `Item No.` reconstruction, `Example`/merged-row skipping).
- `module-results-page.js` — `ModuleResultsPage`. The results/download screen (state-machine + DOM adapter).
- `mode-toggle.js` — `ModeToggle`. The Module Development orchestrator: upload slots, `handleModuleConversion()`, results hook. (It is the module-dev *engine*, not merely a UI toggle.)
- `mode-toggle-filename.js` — `ModeToggleFilename`. Output-filename derivation.

Tests (`tests/`): the ten Module Development test files and the runner —
`mode-toggle.test.js`, `module-mode-upload.test.js`, `module-conversion-flow.test.js`, `module-results-page.test.js`, `module-dev-download-ui.test.js`, `module-dev-filenames.test.js`, `module-dev-next-steps.test.js`, `media-list-converter.test.js`, `media-list-conversion.test.js`, `media-list-extraction.test.js`, plus `test-runner.js` (auto-discovers `*.test.js`).

HTML / CSS: the `index.html` Module Development markup (`#module-dev-section`, `#module-results-section`), the header chrome, the standalone `#toast` element, the JSZip CDN tag; and the corresponding `css/styles.css` rules (`:root` variables, header, `.btn`/`.btn-convert`, `.drop-zone*`, `.module-*`, `.file-list-panel`/`.file-entry`, `.next-steps-*`, `.hidden`, `.sr-only`, `#toast`).

### Resolve this one coupling during carry-over (do it first)

V1's user-facing toast lived on the now-discarded Standard `App` class (`App.showToast`, rendering into the standalone `#toast` element). `MediaListConverter` calls `window.app.showToast` as its browser fallback for the "media table not found" error. Because `App` is being dropped:

- Create a small standalone **`js/toast.js`** following the carried-over modules' pattern (pure logic, DOM isolated behind an injected `document`, no-ops when `#toast` is absent, self-bootstraps to a global e.g. `window.pageForgeToast`). **Lift the toast-render logic verbatim** from V1's `App.showToast` (set `#toast` text, add `visible` class, `setTimeout` to remove it — same timing). Keep the `#toast` element and its CSS.
- Re-point `MediaListConverter`'s browser fallback from `window.app.showToast` to the new global; keep its injectable `notify` option and precedence unchanged.

### Drop entirely (this is the "Standard mode" bloat)

`app.js`, `debug-panel-renderer.js`, the whole conversion-to-HTML pipeline (`tag-normaliser*`, `ordinal-resolver`, `tag-defragmenter`, `subtag-matcher`, `interactive-tag-matcher`, `block-scoper*`, `block-subtag-matcher`, `block-tag-matcher`, `layout-table-unwrapper`, `page-boundary`, `template-engine`, `interactive-extractor*`, `interactive-cell-parser`, `interactive-data-extractor`, `interactive-placeholder-renderer`, `interactive-glossary`, `html-converter*`), `templates/templates.json`, every non-module test file, and all Standard HTML sections / CSS (`#upload-section`, `#processing-section`, `#results-section`, `#debug-panel`). Drop V1's entire `docs/` history — start the new repo's documentation clean.

> Sanity check before deleting: confirm by grep that nothing in the carried-over set still references a dropped symbol. The only known cross-link is the toast fallback above; resolve it first, then the rest is safe to remove.

---

## 5. Engineering conventions for all new code

Match the carried-over modules so the whole codebase stays consistent and testable:

- **State machine first, DOM adapter second.** Each module exposes its real logic as pure methods that need no `document`; every DOM touch is isolated behind an injected `document` and no-ops when an element is absent. This is what lets the DOM-less Node test runner exercise everything directly — mandatory for new modules too.
- **Constructor-injected dependencies**, lazily defaulting to browser globals (the pattern `this._x = options.x || null;` then a lazy `_getX()` that falls back to the global). This is how the tests inject mocks/spies.
- **Single responsibility per file**, kebab-case names, parent-prefix for sub-modules. Keep modules focused and reasonably small; prefer extracting a sibling over growing a file past readability. (This is also what stops the new app from re-accumulating bloat.)
- **Reuse, don't reinvent.** Use the carried-over `DocxParser`, `OutputFormatter`, `OutputManager`, `ModuleResultsPage` rather than parallel implementations. New work *extends* them additively without breaking their existing output contracts or tests.
- **Data-driven where V2 already is.** Author lists and filter regexes live in `data/*.json`, editable without code changes.
- **Wire every new module in two places**: a `<script>` tag in `index.html` (dependency order) and a `loadScript()` line in `tests/test-runner.js`.

---

## 6. Feature 1 — Native Word comment capture (into the Writer's Template `.txt`)

**Goal.** When the writer's `.docx` (and/or the Media List `.docx`) carries native Word editor comments (the yellow margin comments in `word/comments.xml`), keep only the actionable ones from the Creative-Services reviewers and re-emit each as a **red note in the parsed Writer's Template `.txt`, immediately before the thing it refers to**. Authoritative algorithm reference: `Comment_Capture_Process_Explained.md` (V2). Port it to V1's `DocxParser` + `.txt` output.

### 6.1 Extraction — extend `DocxParser` additively

Add comment-awareness to the parse without changing `DocxParser`'s existing output contract (existing template/media-list paths and their tests must be unaffected — make the comment data an additive field, populated only when comment capture runs).

- **Comment bodies** — parse `word/comments.xml` into a `Map<id, {author, text}>`: for each `<w:comment w:id w:author …>…</w:comment>`, decode `w:author`, join **all** inner `<w:t>` runs, collapse whitespace. (Comments never nest.)
- **Anchors** — during the `document.xml` block walk, scan each chunk for `<w:commentRangeStart … w:id="N">`; attach the matching comment to that block (`block.comments = [{author, text, …}]`).
- **Table-row media key (`rowUrl`)** — when an anchor sits inside a table row, read that `<w:tr>`'s hyperlink relationship (`r:id`), resolve it through the document rels, and record it on the comment as `rowUrl`. This is what lets a Media-List comment later find its body element.
- **Carry-forward** — a comment whose anchor is in an empty / image-only paragraph (which the parser drops) must attach to the **next kept block**; trailing comments attach to the **last** block. Nothing is silently lost.

> Inputs note specific to V1: the Module Development screen has *separate* Writer's Template and Media List slots, whereas the corpus is often a combined file. Parse comments from **whichever uploaded `.docx` carries them**. Body-anchored comments come from the Writer's Template. Media-row (`rowUrl`) comments may come from either file and are matched against the Writer's Template body (§6.4).

### 6.2 Whitelist — data-driven, six authors

Port V2's `data/Comment_Authors.json` to `data/comment-authors.json`. Surface only comments whose author resolves to one of: **Kate Scanlon, Nadia Stanton, Caroline Schwer, Simon Vita, Amanda Griffiths, Creative Services**. Word's `w:author` is inconsistent, so normalise both the stored author and each whitelist entry before comparing: strip a trailing ` [N]` disambiguator, lowercase, treat `.`/`_` as space, collapse whitespace, and also accept reversed `Last First` order. The resolver returns the **canonical display name** to print (e.g. always `Kate Scanlon`) or drops the comment. Keep the per-author enable flag and a master on/off toggle.

### 6.3 Actionable vs. boilerplate — the content filter

Port the asymmetric rule: **omit a comment only if it is boilerplate AND has no action signal** — `omit(text) && !(keep && keep(text))`. So a note mixing both (e.g. "Replace with iStock. Used with permission.") is **kept** because the action signal wins.

- `omit_boilerplate` (record-keeping / copyright / permission / attribution): the family in the V2 data — *used with/by/under, with permission, public domain, creative commons, crown copyright, copyright act, all rights reserved, cc0, ©, te kura created/produced/…, links only, extract only, okay to use, all iStock/YouTube/Shutterstock, licence/license, a bare "link"*, etc.
- `action_keep` (the designer must do something): *please, replace, recreate/re-create, embed, insert, remove, crop, resize, swap, delete, overlay, jumble, source, can/could you/we, designer to, cannot/can't/unable/need*, and a **trailing "?"** (any question).

Keep both regex families in the data file so they can be tuned without code changes.

### 6.4 Placement into the `.txt`

Render each surviving comment as a red note **prefixed with the author's display name**, using `OutputFormatter`'s **existing red-text marker convention** (locate it and reuse it — do not invent a new marker, and do not emit raw HTML; the `.txt` is consumed by the downstream Claude Project, which renders the red styling). Two placement paths, mirroring V2:

- **Body-anchored** (no `rowUrl`): emit the note in the `.txt` immediately **before the text of the block it is attached to**. A single source block can produce several output lines — track "already emitted" blocks so each block's comments appear **once**, before its first line.
- **Media-anchored** (`rowUrl`): the comment is about a media item that the Media-List row references but that isn't itself in the body text. Match it to the **Writer's-Template body element that uses the same media** and emit the note before that element. Build **media keys** from the row URL: the exact URL, plus an extracted reference id — iStock (`gm-######` and `/id/####` → `istock:<id>`) and YouTube (`youtu.be/…`, `v=…`, `/embed/…` → `yt:<id>`). For each body element, collect the media keys of the URLs/placeholders it references and look them up. Id-matching matters because most images render as a placeholder with no live link — the shared trace is the iStock reference number.

**Guards (port all):** a comment never surfaces against its own anchor block; each comment surfaces **once** even if several body elements use the same media; the §6.3 filter still applies to media comments. If a Media List is uploaded with **no** Writer's Template (no body to attach to), media comments have nowhere contextual to land — fall back to listing the surviving ones in the Media List `.txt` and surface a toast noting they could not be placed in context.

### 6.5 Suggested module split (all headless-testable)

- `data/comment-authors.json` — authors + normalisation config + `content_filter` regexes + media-match config + toggles (ported).
- `comment-extractor.js` — `comments.xml` parse + anchor capture + `rowUrl` + carry-forward (drives `DocxParser`'s extended output).
- `comment-filter.js` — whitelist/normalisation + omittable filter (pure, data-driven).
- `comment-inserter.js` — body placement + media-key build + media-match + note rendering via the formatter's red marker.

### 6.6 Tests

New small test files (5–12 cases each), all via injected mocks: author normalisation resolves the six variants and rejects non-whitelisted; the asymmetric filter keeps action-bearing boilerplate and drops pure boilerplate; body comments land before their block exactly once; a `rowUrl` comment media-matches to the body element by iStock id and by YouTube id and emits once with the right author prefix; the media-only-upload fallback path; guards (no self-match, single surfacing). Verify the whitelist against the corpus stat as a smoke check (a large majority of comments resolve to the six authors). Keep the inherited media-list `.txt` tests green (comment capture must not alter the media-list extraction output).

---

## 7. Feature 2 — Page Stitcher (separate mode)

**Why separate.** It's not part of preparing the initial Claude-Project upload, and only some modules need it (the ones whose single long homepage caused the converter to abort, so lessons were generated as separate files).

**Goal.** Take a **base module-homepage HTML** plus the **individually-generated lesson HTML files** and splice each lesson's content into its correct place in the homepage, then download **one unified HTML file**. Client-side only.

### 7.1 The insertion contract (decide and document this first)

Robust splicing needs an explicit, unambiguous way to know *where* each lesson goes. **Do not infer position heuristically.** Specify a contract and have the Stitcher honor it, e.g.:

- The base homepage contains explicit **insertion markers** (an HTML comment token or a placeholder element with a stable id, one per lesson slot, carrying the lesson's identifier), and
- each lesson file is identified (by filename convention or a matching id in the file) so it maps to exactly one marker.

The Stitcher replaces each marker with that lesson's body content (the inner content region, not its full `<html>` wrapper), preserving document order and the homepage's surrounding scaffold untouched. Define exactly which region of a lesson file is extracted and inserted.

### 7.2 Behavior & guards

Validate before emitting: every marker is filled, every uploaded lesson is placed, no lesson is orphaned, no marker is left empty. Report any mismatch via the toast (and/or an on-screen summary) and do not silently produce a broken file. Output one downloadable unified HTML file via `OutputManager`.

### 7.3 Module split & tests

- `page-stitcher.js` — pure core: given the base HTML + a map of lesson-id → lesson HTML, return the unified HTML; plus a thin DOM/upload adapter.
- Tests: a marker is replaced by the correct lesson body in order; multiple lessons placed correctly; unknown/extra lesson reported; missing lesson for a marker reported; the homepage scaffold around the insertions is unchanged; full round-trip on a representative base+lessons fixture.

---

## 8. UI / UX

Two top-level modes, selected by a simple, accessible mode switch in the header (reuse the carried-over toggle's markup/CSS pattern, **re-labeled and re-wired** for these two modes — follow the headless-testable visibility-controller pattern; it should only ever show one section and hide the other):

- **Module Development** (default). One Word-documents upload area accepting the Writer's Template `.docx` and/or the Media List `.docx` (1–2 files, auto-classified by content), with at least one required to enable **Convert**. One **Convert** press converts **every document provided** and routes to the results screen, which lists **each file produced** (Writer's Template `.txt`, Media List `.txt`) with per-file download and a "Download all" when more than one exists. Keep the existing "next steps" guidance panel.
- **Page Stitcher** (separate). One container for the base homepage + all of its section files (auto-classified), a **Stitch** action, and a download of the unified HTML (plus a short placement summary).

Preserve the header chrome and the "100% Client-Side / No Data Stored" badge. Keep formatting minimal and consistent with the carried-over styles; no new inline styles.

---

## 9. Testing & acceptance

- **All carried-over module tests stay green** (the inherited ten files), proving the inherited conversion is intact.
- **New tests per feature** as listed in §6.6 and §7.3 — small files, headless, run `node tests/test-runner.js` (auto-discovers `*.test.js`) frequently as a checkpoint.
- **Comment-capture smoke check** against the corpus author distribution.
- **Acceptance:** the full suite passes (capture the final pass/total); the app loads and runs entirely client-side with no console errors; each mode performs its end-to-end flow on a real example; the bundle is a clean static site deployable to GitHub Pages.

---

## 10. Deliverables & migration

- A clean repository tree: `index.html`, `css/styles.css`, `js/` (carried-over + new modules), `data/` (`comment-authors.json`), `tests/`, a `.nojekyll`, and a fresh **README** describing the two modes, the two features, the privacy model, and how to run the tests. **No V1 `docs/` history** — start clean (you have my blessing to drop the old paper trail; the README is the new entry point).
- Ready to push to a GitHub Pages repo and serve as the interim production PageForge.
- Brief inline code comments where a ported algorithm is non-obvious (e.g. the media-key matching), pointing back to this brief.

---

## 11. Recommended build sequence

1. **Foundation + decouple.** Copy the carry-over set; add `js/toast.js` and re-point `MediaListConverter`; strip everything Standard; get the inherited ten tests green on the clean tree. (Stable baseline before any feature work.)
2. **Comment capture (Feature 1).** Extend `DocxParser` additively; port the data file, filter, whitelist, and placement (body + media-match); tests + corpus smoke check. Verify the media-list `.txt` output is byte-unchanged by this.
3. **Wire the unified Convert + results** for the Module Development outputs; "Download all"; next-steps copy.
4. **Page Stitcher (Feature 2).** Define the insertion contract; build the splicer + adapter + tests as a separate mode.
5. **Polish, full-suite green, README, deploy-ready.**

> Throughout: prefer extending the inherited modules over parallel rewrites, keep every new module headless-testable with injected dependencies, and validate the comment whitelist against the real corpus you have — that data is the reason this can be built with confidence rather than guesswork.
