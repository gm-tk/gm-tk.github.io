# 31. Module Development Mode

> **Multi-session phase.** Session 1 (this log) establishes the mode shell,
> the toggle, and the new front-page UI only — **no** conversion logic and
> **no** results/download page. Sessions 2 and 3 append `###` sub-headings to
> this same file.

---

## Session 1 — Mode Shell, Toggle & Front Page

### Overview

PageForge gains a **top-level mode** selected by a two-option switch rendered
above both front-page bodies:

- **Module Development mode** — *selected by default on page load.* A
  streamlined front page with two **independent, optional** `.docx` upload
  slots — **Writer's Template** and **Media List** — plus a single **Activate**
  button. It carries **no** phase selector, **no** template selector, and **no**
  HTML-related controls.
- **Standard mode** — the existing PageForge front page (`#upload-section`):
  drop zone, template selector, Convert button. Selected only when the user
  toggles to it, and shown **exactly as it currently is**.

The Activate button is disabled when **neither** file is staged and enabled as
soon as **at least one** is provided (template only, media list only, or both).
Its click handler is a deliberate **stub** — `handleModuleConversion()` — left
with a `// TODO(Session 2): implement conversion` comment. No conversion runs in
this session.

**Status:** DONE — Session 1 of 3. 697/697 tests pass (682 baseline → 697,
+15 across two new test files).

### Design — state machine first, DOM adapter second

The new `js/mode-toggle.js` defines a single `ModeToggle` class. Because the
Node test runner has **no DOM**, the class is a **state machine first**: all
mode state (`mode`), upload state (`uploads`), the enable rule
(`isActivateEnabled()`) and the control contract (`getControlManifest()`) live
in pure methods that require no `document`. Every DOM touch is isolated behind
an injected `document` (constructor option) and degrades to a no-op when an
element is absent, so the same class can be unit-tested headlessly and
self-bootstrapped in the browser (`DOMContentLoaded` → `window.pageForgeMode`).

Key surface:

| Member | Purpose |
|--------|---------|
| `getMode()` / `setMode(m)` / `toggleMode()` | Active mode; default `'module'`. |
| `isModuleDevMode()` / `isStandardMode()` | Mode predicates. |
| `isModuleDevVisible()` / `isStandardVisible()` | Visibility predicates (derive from mode). |
| `setUpload(slot, file)` / `clearUpload(slot)` | Record/clear one of two slots (`'template'`, `'mediaList'`). |
| `hasUpload(slot)` / `hasAnyUpload()` | Slot occupancy queries. |
| `isActivateEnabled()` | `true` iff ≥1 slot holds a file. |
| `getUploadState()` | `{ template: bool, mediaList: bool }` snapshot. |
| `getControlManifest(mode)` | Declarative `[{id, kind, slot?}]` contract per mode. |
| `handleModuleConversion()` | **Stub** (no-op). Session 2 entry point. |
| `init()` | Resolve elements, bind events, apply default mode (browser only). |

`ModeToggle.CONTROL_MANIFEST` is the locked contract: `module` declares exactly
two `kind:'upload'` controls (`module-template-input`, `module-media-input`)
plus one `kind:'button'` (`btn-module-activate`) and **zero** `kind:'selector'`
controls; `standard` retains `file-input` (upload), `template-dropdown`
(selector), and `btn-convert` (button).

### Visibility wiring

`_applyVisibility()` toggles the shared `.hidden` class between the two
front-page containers and keeps the mode radios in sync:

- **Module Development active** → `#upload-section` (the entire Standard front
  page, including phase/template controls and the existing Convert button) gets
  `.hidden`; `#module-dev-section` is shown.
- **Standard active** → `#module-dev-section` gets `.hidden`; `#upload-section`
  is shown unchanged.

To avoid any flash before scripts run, `#upload-section` ships with `class="hidden"`
in the static HTML (module mode being the default); `init()` re-asserts the same
state idempotently. `js/app.js` was **not** modified — it only ever removes
`.hidden` from `#upload-section` in its own `reset()`/`_showError()` paths, which
fire exclusively inside a Standard-mode flow.

### Files touched

| File | Before | After | Change |
|------|-------:|------:|--------|
| `js/mode-toggle.js` | — (new) | 388 | New `ModeToggle` class — state machine + injectable DOM adapter + control manifest + stub handler + browser bootstrap. |
| `index.html` | 182 | 250 | Added `#mode-toggle` two-option radio switch; added `#module-dev-section` (two `.docx` slots + Activate); added `hidden` to `#upload-section`; added `<script src="js/mode-toggle.js">` before `js/app.js`. |
| `css/styles.css` | 941 | 1044 | Added Mode Toggle (segmented radio control) and Module Development Front Page styles (intro, 2-col upload grid collapsing to 1 col ≤720px, slot titles, `.module-drop`). Reuses existing `.drop-zone`, `.staged-file-info`, `.btn-convert`, `.hidden`, `.sr-only` and `:root` variables. |
| `tests/test-runner.js` | 161 | 162 | Added `loadScript('js/mode-toggle.js')` after `html-converter.js`. |
| `tests/mode-toggle.test.js` | — (new) | 151 | **8** `it()` cases (see below). |
| `tests/module-mode-upload.test.js` | — (new) | 93 | **7** `it()` cases (see below). |

`js/app.js` was **left byte-for-byte unchanged at 1364 lines**. It already
exceeded the 700-line core-orchestrator threshold from a prior session, so per
the file-size hygiene rule a new dedicated module was created instead of
bloating it ("only create a new module if the host would otherwise cross
threshold"). No JS file crossed its threshold *as a result of* this session:
the new `mode-toggle.js` is 388 lines (≤500 sub-module ceiling).

### Test coverage

`tests/mode-toggle.test.js` (8 `it()`), via a minimal injected mock document:

1. defaults to Module Development mode on load;
2. toggle switches to Standard (radio `change` fired);
3. toggle switches back to Module Development;
4. Standard front page hidden while in Module Development mode;
5. Module Development front page hidden while in Standard mode;
6. exposes exactly two upload slots (both resolve to `type="file"`; manifest
   declares two `upload` controls; `UPLOAD_SLOTS === ['template','mediaList']`);
7. exposes no phase/template **selector** controls (zero `selector`-kind in the
   module manifest; `template-dropdown` is not a module control);
8. Standard page still renders its template selector when active (section
   visible; `selector`-kind present; `template-dropdown` resolves to `<select>`).

`tests/module-mode-upload.test.js` (7 `it()`), pure state + Activate-button
disabled sync via a minimal mock:

1. Activate disabled with no files (`isActivateEnabled()` false; button
   `disabled`; state `{template:false, mediaList:false}`);
2. enabled with Writer's Template only;
3. enabled with Media List only;
4. enabled with both;
5. template-only state recorded (`{template:true, mediaList:false}`);
6. media-list-only state recorded (`{template:false, mediaList:true}`);
7. both-files state recorded (`{template:true, mediaList:true}`).

### Invariants locked in

1. **Default mode is Module Development** — `new ModeToggle().getMode() === 'module'`.
2. **Two optional slots** — `ModeToggle.UPLOAD_SLOTS` is exactly
   `['template', 'mediaList']`.
3. **Activate enable rule** — enabled iff ≥1 slot holds a file; never on zero.
4. **No phase/template controls in Module Development** — the `module` manifest
   contains zero `selector`-kind controls.
5. **Standard untouched** — `#upload-section` and `js/app.js` are unchanged; the
   toggle only adds/removes `.hidden` on the two front-page containers.
6. **No conversion in Session 1** — `handleModuleConversion()` is a no-op stub.
7. **Headless-testable** — `ModeToggle` runs as a pure state machine with no
   `document`; DOM operations no-op when unbound.

### Notes for later sessions

- **Session 2** will implement `handleModuleConversion()` (parse the staged
  Writer's Template and/or Media List). The two staged `File` objects are
  already available via `ModeToggle.uploads` / `getUploadState()`.
- **Session 3** will add the Module Development results/download page.

---

### Session 2 — Conversion Logic Behind Activate

**Status:** DONE — Session 2 of 3. 712/712 tests pass (697 baseline → 712, +15
across two new test files). Still **no** results/download page (Session 3).

#### Overview

The Session 1 `handleModuleConversion()` stub is replaced with a real
implementation. On **Activate** it converts whichever of the two optional files
are staged and stores **one output per uploaded slot** on
`ModeToggle.moduleOutputs` (the new in-memory app-state field Session 3's
results page will read). It deliberately does **not** build the results/download
page.

- **Writer's Template** — reuses the existing writer's-template pipeline
  **exactly as-is**, with the intro-skip **not** re-implemented:
  `DocxParser.parse()` runs the `[TITLE BAR]` boundary detection in
  `_findContentStart()` (discarding the leading generic statements + submission
  checklists), then `OutputFormatter.formatAll()` emits from `contentStartIndex`.
  The module-mode template path therefore produces the **same plain-text output
  format** the Standard pipeline already produces (`formatAll().full`) — it does
  **not** run the phase/template/HTML conversion that Standard mode layers on top.
- **Media List** — a new **straight full conversion** in the
  single-responsibility sub-module `js/media-list-converter.js`. It reuses the
  shared `DocxParser` for `.docx` reading (no re-implementation) and the shared
  `OutputFormatter` for the output format, but **always starts at block 0** —
  **no** `[TITLE BAR]` / page-section skipping and **no** phase/template
  processing of any kind.

#### Existing pipeline located (Step 1 record)

| Concern | Symbol | File |
|---------|--------|------|
| Conversion orchestration | `App.convertDocument()` | `js/app.js:335` |
| Shared docx reader | `DocxParser.parse()` (`JSZip.loadAsync`) | `js/docx-parser.js:75` |
| Intro-skip boundary detection | `DocxParser._findContentStart()` (finds `[TITLE BAR]`) | `js/docx-parser.js:695` |
| Intro-skip discard | `OutputFormatter.formatContent(content, startIndex, …)` from `contentStartIndex` | `js/formatter.js:70` |
| Output text format | `OutputFormatter.formatAll()` → `{full, metadataOnly, contentOnly}` | `js/formatter.js:15` |

The Writer's Template path calls `parse()` + `formatAll()` verbatim; the skip is
inherited, never duplicated.

#### Design — headless-testable async

`.docx` parsing is async, but the Node runner has no DOM/JSZip (and never loads
`DocxParser`). Both `MediaListConverter.convert()` and
`ModeToggle.handleModuleConversion()` use a tiny maybe-promise resolver
(`ModeToggle._resolveMaybe`): when the injected parser is synchronous (tests),
the whole flow returns the output array **directly**; in the browser the real
`DocxParser.parse()` returns a Promise and the flow returns a Promise. The
formatting core, `MediaListConverter.convertParsedResult()`, is a **pure
synchronous** function over an already-parsed result, exercised directly against
the real (loaded) `OutputFormatter`. Conversion dependencies (`parser`,
`formatter`, `mediaListConverter`) are **constructor-injected** on `ModeToggle`,
defaulting lazily to the browser globals.

`convertParsedResult()` emits the **same envelope** as `formatAll()` —
`formatMetadata()` + `\n` + `_stripEmptyRedText(formatContent(content, 0, true))`
— so when nothing is skipped its output is **byte-identical** to the writer
pipeline (locked by a test).

#### Output state contract

`ModeToggle.moduleOutputs` — `null` until a non-no-op Activate, then an array of
one entry per uploaded slot:
`{ source: 'template' | 'mediaList', filename, content }`. Filenames derive from
the input stem (sans `.docx`): template → `<stem>_parsed.txt`, media list →
`<stem>_media_list.txt`.

#### Files touched

| File | Before | After | Change |
|------|-------:|------:|--------|
| `js/media-list-converter.js` | — (new) | 108 | New `MediaListConverter` — straight full-document conversion reusing `DocxParser` + `OutputFormatter`; pure sync `convertParsedResult()` core; async-or-sync `convert()`. |
| `js/mode-toggle.js` | 388 | 498 | Real `handleModuleConversion()` + `_convertSlot` / `_finishConversion` / `_deriveFilename` / lazy `_get*` accessors + static `_resolveMaybe`; injectable `parser`/`formatter`/`mediaListConverter`; new `moduleOutputs` state field. (≤500 sub-module ceiling.) |
| `index.html` | 250 | 251 | `<script src="js/media-list-converter.js">` added **before** `js/mode-toggle.js`. |
| `tests/test-runner.js` | 162 | 163 | `loadScript('js/media-list-converter.js')` added **before** `js/mode-toggle.js`. |
| `tests/media-list-converter.test.js` | — (new) | 172 | **8** `it()` cases (see below). |
| `tests/module-conversion-flow.test.js` | — (new) | 183 | **7** `it()` cases (see below). |

`js/app.js` and the entire Standard-mode flow are **untouched**.

#### Test coverage

`tests/media-list-converter.test.js` (**8** `it()`):
1. `convert()` reuses the injected DocxParser and converts the whole document;
2. does **not** skip leading pages/sections (contrast: the writer pipeline does);
3. output is **byte-identical** to the writer converter when nothing is skipped (red/bold/table markers present);
4. multi-section list content preserved in document order;
5. **no** phase/template/HTML processing (no `<div>`, `class="…"`, doctype, tags);
6. single-entry media list handled;
7. empty document handled gracefully;
8. malformed input (`null` / `{}` / non-array content) handled gracefully.

`tests/module-conversion-flow.test.js` (**7** `it()`):
1. template-only → exactly **one** output (media converter not invoked);
2. media-list-only → exactly **one** output (template parser not invoked);
3. both → exactly **two** outputs (`['template','mediaList']` order);
4. the writer's template path **invokes the existing intro-skipping function** (`_findContentStart` + `formatAll`; leading checklist discarded, body retained);
5. converted outputs **written to `moduleOutputs`** (null before; holds the returned array after);
6. Activate with **no files is a no-op** (`[]`; no converter calls; state stays null);
7. **sensible filenames** (`ENGS301_parsed.txt`, `MediaList_media_list.txt`).

#### Invariants locked in

1. **Template reuses the existing skip** — module-mode template conversion calls `DocxParser.parse()` (→ `_findContentStart` `[TITLE BAR]` detection) + `OutputFormatter.formatAll()` (→ `formatContent` from `contentStartIndex`); the skip is never re-implemented.
2. **Media List never skips** — `convertParsedResult()` always starts at block 0.
3. **Format parity** — with nothing skipped, `MediaListConverter` output equals the writer pipeline's `formatAll().full` byte-for-byte.
4. **No phase/template processing on either module-mode path** — both emit plain text only; HTML conversion stays Standard-mode-only.
5. **One output per uploaded input** — 1 or 2 entries on `ModeToggle.moduleOutputs`.
6. **No-op on empty** — Activate with zero files returns `[]` and leaves `moduleOutputs` null.
7. **Headless-testable async** — synchronous injected parser ⇒ synchronous return; browser ⇒ Promise.

#### Notes for Session 3

- Read `window.pageForgeMode.moduleOutputs` (array of `{source, filename, content}`) to render the results/download page; one entry per uploaded slot.
- The outputs are plain text in the existing converter format; download as `.txt` (e.g. via the existing `OutputManager` download patterns).

---

### Session 3 — Results / Download Screen

**Status:** DONE — Session 3 of 3 (final). 721/721 tests pass (712 baseline →
721, **+9** across one new test file). Completes the Module Development mode:
toggle + front page (S1) → Activate conversion (S2) → results/download screen
(S3).

#### Overview

After the Activate conversion completes, Module Development mode now navigates to
a dedicated **results / download screen**. It is **purely a download surface**:
it lists the converted plain-text output file(s) held on
`ModeToggle.moduleOutputs` (one per uploaded slot, from Session 2) and offers an
instant download control for each, **showing only the downloads for files that
were actually produced**:

- Writer's Template uploaded → the writer's-template output download.
- Media List uploaded → the media-list output download.
- Both uploaded → both downloads (template first, media list second).

The screen carries **no** phase/template controls and **no** HTML preview, and
provides a single **Convert Another Module** control that returns to the Module
Development front page — mirroring Standard mode's "Parse Another File" reset,
which simply toggles section `.hidden` visibility.

#### Existing patterns located (Step 1 record — reused, not reinvented)

| Concern | Symbol | File |
|---------|--------|------|
| Screen navigation (show/hide via `.hidden`) | `App.showResults()` / `App.reset()` | `js/app.js:493` / `js/app.js:539` |
| Download helper (Blob + `URL.createObjectURL` + `<a download>` + click + revoke) | `OutputManager.downloadFile(filename)` | `js/output-manager.js:96` |
| File registration for the helper | `OutputManager.addFile()` / `getFile()` / `clear()` | `js/output-manager.js:28` |

The results screen reuses `OutputManager.downloadFile()` verbatim as the download
primitive (registering each output via `addFile()` on first use) and the same
`.classList.add/remove('hidden')` section-toggle idiom for navigation.

#### Design — new sub-module, single-line host hook

`js/mode-toggle.js` was already at **498/500** lines (its established sub-module
ceiling per S1/S2), leaving no room for a results page. Per the file-size
hygiene rule ("only introduce a new module if the host would otherwise cross
threshold"), the screen lives in a new single-responsibility sibling sub-module,
**`js/module-results-page.js`** (`ModuleResultsPage`), and the host hook is a
**single line**:

```js
// js/mode-toggle.js — _finishConversion (the sole sync+async completion funnel)
this.moduleOutputs = outputs;
ModuleResultsPage.present(this, outputs);   // ← the one added line (498 → 499)
return outputs;
```

`ModuleResultsPage.present(toggle, outputs)` lazily creates + caches the page on
the toggle (`toggle._resultsPage`, bound to the toggle's `_document`) and calls
`show(outputs)`. Because both the sync and async conversion paths funnel through
`_finishConversion` (`js/mode-toggle.js:240` and `:238`), this single hook covers
both. `mode-toggle.js` ends at **499 (≤500)**; no extraction was required.

Like `ModeToggle`, `ModuleResultsPage` is a **state machine first, DOM adapter
second**: `getOutputs()`, `hasOutputs()`, `isResultsVisible()`,
`getDownloadItems()`, `getControlManifest()` and `triggerDownload()` are pure and
need no `document`; every DOM touch is isolated behind an injected `document` and
no-ops when an element is absent (so the DOM-less Node runner exercises it
directly, and the existing S2 document-less conversion-flow tests keep passing —
`present()` → `show()` no-ops without a document).

**Mode-switch robustness.** The results section and the S1 mode toggle are
independent visibility controllers, so switching top-level mode *while the
results screen is up* could leave it stacked over a front page. Rather than
spend host lines, `ModuleResultsPage` binds both mode radios to **hide the
results section** on change (`_bindModeReset` / `_hideForModeChange`);
`ModeToggle._applyVisibility` still owns which **front** page is then shown, so
this only ever hides (never reveals) a section. `mode-toggle.js` is untouched by
this.

#### Output state contract consumed

Reads `ModeToggle.moduleOutputs` (S2): an array of `{ source: 'template' |
'mediaList', filename, content }`, one per uploaded slot. `SLOT_LABELS` maps
`template → "Writer's Template"`, `mediaList → "Media List"`. Downloads use the
S2 filenames verbatim (`<stem>_parsed.txt`, `<stem>_media_list.txt`).

#### Files touched

| File | Before | After | Change |
|------|-------:|------:|--------|
| `js/module-results-page.js` | — (new) | 353 | New `ModuleResultsPage` — pure state (outputs/visibility/download-items/control-manifest) + DOM adapter (render list, back control, mode-switch hide) + `triggerDownload` delegating to the existing `OutputManager` helper + static `present()` host hook. (≤500 sub-module ceiling.) |
| `js/mode-toggle.js` | 498 | 499 | One-line `ModuleResultsPage.present(this, outputs)` hook in `_finishConversion`; refreshed the now-stale class JSDoc (same line count). (≤500.) |
| `index.html` | 251 | 271 | Added `#module-results-section` (heading, intro, `#module-results-list`, `#module-results-empty`, `.actions-bar` with `#btn-module-back`), reusing existing `.file-list-panel` / `.actions-bar` / `.btn` / `.module-dev-intro` / `.hidden` classes (no new CSS); added `<script src="js/module-results-page.js">` **before** `js/mode-toggle.js`. |
| `tests/test-runner.js` | 163 | 164 | `loadScript('js/module-results-page.js')` added **before** `js/mode-toggle.js`. |
| `tests/module-results-page.test.js` | — (new) | 193 | **9** `it()` cases (see below). |

`js/app.js` and the entire Standard-mode flow are **untouched**. No CSS changes
(the screen reuses existing classes).

#### Test coverage

`tests/module-results-page.test.js` (**9** `it()`), via a minimal injected mock
document and a spy `OutputManager`:

1. renders the results screen after a conversion completes (visible; results
   section revealed; front page hidden; download buttons rendered);
2. shows the Writer's Template download when only the template was converted;
3. shows the Media List download when only the media list was converted;
4. shows both downloads when both files were converted (template first);
5. download control invokes the **existing** download helper with the correct
   filename **and** content (`addFile({filename, content})` then
   `downloadFile(filename)` on the spy `OutputManager`);
6. shows **no** HTML preview and **no** phase/template controls (control manifest
   has zero `selector`/`preview` kinds — only `download` + `back`);
7. return-to-front-page control navigates back to the Module Development front
   page (firing the back button hides results + reveals the front page);
8. empty-state guard when no outputs are present (`show([])` → no items, no
   download controls, empty-state revealed, list cleared, screen still active);
9. hides the results screen when the top-level mode is switched (no stacking).

#### Invariants locked in

1. **Download surface only** — the results control manifest contains exactly
   `download` (one per produced output) + one `back`; **zero** `selector` and
   **zero** `preview` controls.
2. **Only produced files appear** — `getDownloadItems()` / the rendered list have
   exactly one entry per `moduleOutputs` entry, in produced order.
3. **Reuses the existing download helper** — downloads route through
   `OutputManager.addFile()` + `downloadFile()`; no new download primitive.
4. **Reuses the existing navigation idiom** — show/return toggle the shared
   `.hidden` class between `#module-dev-section` and `#module-results-section`,
   as Standard mode does.
5. **Single-line host hook** — `_finishConversion` gains exactly one line;
   `mode-toggle.js` stays at 499 (≤500); no extraction needed.
6. **Headless-testable** — all output/navigation state is pure; DOM ops no-op
   without a document, so S2's document-less conversion-flow tests are unaffected.
7. **Empty-state safe** — an empty/`null` `show()` reveals the empty-state and
   renders no download controls (never throws).

---

### Media List Refinement — Structural Table Extraction

> **Post-Session-3 refinement.** Changes ONLY what the Media List `.txt`
> contains. The Writer's Template path, the OutputFormatter marker behavior, the
> mode UI, the file inputs, and the download wiring are all untouched.

**Status:** DONE. 730/730 tests pass (721 baseline → 730, **+9** across one new
test file; the existing media-list test file's 8 cases were re-pointed to the new
behavior, not grown).

#### Problem

Session 2 converted the Media List slot via a **straight full-document dump**
(`MediaListConverter.convertParsedResult` emitted `formatMetadata` + `formatContent`
from block 0 — every paragraph, heading and table in the file). For a real Media
List `.docx` that means the downloadable `.txt` was polluted with the generic,
per-module boilerplate that precedes the actual data: the template heading, the
submission checklist, the "Before starting ensure you are familiar with…"
guidance, the "Please supply details for ALL external media…" paragraph, and
early-copyright notes. That boilerplate differs from module to module, so it
cannot be stripped by string-matching known phrases.

#### Change — content-agnostic, structural extraction

`MediaListConverter` now emits **only** the genuine media-list table's data rows.
The table is located **structurally, by its HEADER ROW** (by content, never by
position): the first `type === 'table'` block whose first row carries every
REQUIRED media column label —

`Item No.`, `WTPg No.`, `Item Type`, `Description`, `Source`, `URL`

— with an **optional** trailing `ECR approval` column that may be absent. Header
matching is case-insensitive and whitespace/punctuation-tolerant
(`_normaliseHeader` lower-cases and collapses every non-alphanumeric run to a
single space, so `"Item No."` → `"item no"`). Required labels live in
`MediaListConverter.REQUIRED_HEADERS`; the optional one in `OPTIONAL_HEADERS`.

Emitted output (plain text, no envelope, no metadata header):
- the matched table's **header row, once, at the top** (cells tab-separated);
- one **tab-separated line per data row**, every cell in column order;
- the conventional **`Example`/sample row is skipped** (first cell normalises to
  a leading `example`);
- fully-empty rows are skipped.

Everything outside that table — every preceding paragraph, heading, the
submission checklist, hyperlink guidance — is excluded **entirely**, with no
phrase string-matching, so it is robust to per-module boilerplate variation.

**Guard (table not found / malformed / empty input):** returns an **empty
string** (never throws) and surfaces a user-facing error through the **shared,
app-wide toast**. The toast is reached via an injectable `notify` option (spied
in tests) that **falls back to `window.app.showToast`** in the browser — the
established toast mechanism (`App.showToast`, `js/app.js`); `showError` was
deliberately NOT used because it reveals the Standard `#upload-section`. No mode
UI, file-input or download wiring was touched to add this.

The now-dead `OutputFormatter` dependency was removed from the converter
(`_formatter` field, the `formatter` constructor option, and `_getFormatter()`);
`DocxParser` reuse via `convert()` is unchanged.

#### Files touched

| File | Before | After | Change |
|------|-------:|------:|--------|
| `js/media-list-converter.js` | 108 | 201 | Rewrote `convertParsedResult()` to header-row table detection + data-row emission; added `_findMediaTable` / `_isMediaHeaderRow` / `_rowCellTexts` / `_extractCellText` / `_normaliseHeader` / `_notifyError` helpers + `REQUIRED_HEADERS`/`OPTIONAL_HEADERS` statics; added injectable `notify`; removed the dead `OutputFormatter` dependency. (≤500 sub-module ceiling.) |
| `tests/media-list-converter.test.js` | 172 | 200 | Re-pointed all **8** `it()` cases from the old whole-document-dump behavior to structural extraction (surgical per-`it()` `str_replace`); added `MEDIA_HEADERS` + `mlcMediaTable` builders. |
| `tests/media-list-extraction.test.js` | — (new) | 182 | **9** `it()` cases — structural-exclusion / content-agnostic coverage (see below). |

No new JS module (so **no** `index.html` / `tests/test-runner.js` wiring change);
test files are auto-discovered by the runner. `js/mode-toggle.js`,
`js/module-results-page.js`, `js/app.js`, `js/formatter.js`, `js/docx-parser.js`,
`index.html` and the CSS are **untouched**.

#### Test coverage

`tests/media-list-converter.test.js` (**8** `it()`, re-pointed): convert()
reuses the injected DocxParser and extracts the table (intro + `Example`
excluded); excludes preceding boilerplate paragraphs/headings/checklist; emits
data rows in column order with the header once at the top; preserves multiple
data rows in row order; applies no phase/template/HTML processing (no formatter
table-box); single data-row list (header + one row); absent table → empty string
**and** an error surfaced via the injected `notify` spy; malformed inputs
(`null`/`undefined`/`{}`/non-array content) → empty string, never throws.

`tests/media-list-extraction.test.js` (**9** `it()`, new): table identified by
header row **not position** (a decoy non-media table appears first); intro
paragraphs excluded; submission checklist excluded; template/section headings
excluded; the `Example` row skipped; each data cell emitted in column order
(tab-separated, verified per column index); **different/unknown** boilerplate
before the table still fully excluded (proves content-agnostic, no phrase
matching); missing optional `ECR approval` column still parses; absent data table
→ safe empty result without throwing.

#### Invariants locked in

1. **Structural, content-agnostic exclusion** — the target table is found by
   header-row content (`REQUIRED_HEADERS` all present), never by position and
   never by string-matching intro phrases.
2. **Data-only output** — only the matched table's data rows are emitted; the
   header once at the top; the `Example` row and all out-of-table content
   excluded.
3. **Optional ECR approval** — a header row missing only the trailing
   `ECR approval` column still matches.
4. **Safe, non-throwing guard** — no media table ⇒ empty string + a user-facing
   toast (`notify` → `window.app.showToast`); never throws on malformed/empty
   input.
5. **Scope contained to the Media List `.txt`** — Writer's Template conversion,
   OutputFormatter markers, mode UI, file inputs and download wiring unchanged.
6. **Supersedes Session 2's Media List dump** — the S2 "straight full
   conversion" and "format parity with the writer pipeline" invariants no longer
   apply to the Media List path (they were specific to the dump behavior); the
   Writer's Template path retains them.

---

### Media List Refinement — Table Conversion Defects (Item No., Example, Merged Rows)

> **Post-refinement of "Structural Table Extraction".** Changes ONLY what the
> Media List `.txt` table contains. The Writer's Template path, the mode UI, the
> file inputs and the download wiring are all untouched. Builds directly on the
> header-row table detection from the previous refinement.

**Status:** DONE. **739/739** tests pass (730 baseline → 739, **+9** across one
new test file; one assertion in the existing extraction test file was re-pointed
to the reconstructed Item No., not grown).

#### Problem

Once the genuine media table was being located structurally, four row-level
defects remained in how its rows were rendered to the tab-delimited `.txt`:

1. **Blank `Item No.` column.** Genuine data rows carry the Item No. as a Word
   **auto-number** (`<w:numPr>` with a `numId`), so the literal cell text is
   **empty** and the displayed `1.`, `2.`, `3.`… were lost by plain-text
   extraction — every data row began with an empty first column.
2. **Merged boilerplate leak.** A horizontally-merged row spanning the table
   width — e.g. `Reminder: List all external platforms recommended to the
   student in the module for copyright review (old and new links)` — was emitted
   as if it were a data row.
3. The `Example` (cheetah stock-photo) sample row exclusion and the pre-table
   boilerplate exclusion both had to be **preserved** through the above changes.

#### Change — structural, content-agnostic row handling

`MediaListConverter.convertParsedResult()` now, for the located media table:

- **Header row** — emitted **once, first**, with its **literal** labels
  (`Item No.` … `ECR approval`); it is never numbered and never dropped.
- **`Example` row** — skipped (first cell normalises to a leading `example`),
  evaluated **before** ordinal assignment so it consumes no Item No.
- **Merged/spanning boilerplate rows** — dropped via a new
  `_isMergedSpanRow(cells, columnCount)` helper. A horizontal `gridSpan` is
  surfaced by the shared `DocxParser` as a **single `<w:tc>`**, so the detection
  is structural: **(a)** a multi-column table row that collapses to **one cell**,
  or **(b)** a row whose non-empty cells **all repeat the same merged text**.
  No intro-phrase string-matching — robust to per-module boilerplate variation.
- **`Item No.` reconstruction** — every **retained** data row (header, `Example`
  and merged rows excluded) is assigned a **sequential ordinal in document order
  starting at `1`**, formatted with a trailing period (`1.`, `2.`, `3.`…) to
  match how Word renders the source numbered list, and written as the first
  column — overwriting the empty auto-numbered cell.
- **Column structure** — each data row is padded to the header's column count so
  the trailing (usually empty) **`ECR approval`** column is always present;
  cells are joined with `\t`, preserving all seven columns.

Pre-table exclusion (template title, submission checklist + bullets, `MEDIA LIST`
heading, every instructional paragraph) is unchanged — only the matched table is
emitted — and is re-verified by the new tests.

#### Files touched

| File | Before | After | Change |
|------|-------:|------:|--------|
| `js/media-list-converter.js` | 201 | 252 | Reworked `convertParsedResult()`: literal header, Example-then-merged-then-empty skip order, sequential `Item No.` reconstruction, column-count padding; added `_isMergedSpanRow()` helper; updated class + method docstrings. (≤500 sub-module ceiling — comfortably under.) |
| `tests/media-list-extraction.test.js` | 182 | 185 | Re-pointed the single `cells[0]` assertion in "emits each data row cell in column order" from the old literal pass-through (`'7'`) to the reconstructed ordinal (`'1.'`), modelling an empty auto-numbered Item No. cell. No `it()` count change (still 9). |
| `tests/media-list-conversion.test.js` | — (new) | 233 | **9** `it()` cases (see below). |

No new JS module ⇒ **no** `index.html` / `tests/test-runner.js` wiring change;
test files are auto-discovered by the runner. `js/docx-parser.js`,
`js/mode-toggle.js`, `js/module-results-page.js`, `index.html` and the CSS are
**untouched**.

#### Test coverage

`tests/media-list-conversion.test.js` (**9** `it()`, new): header row emitted as
the first output line with all seven column labels (literal `Item No.`); the
`Example` (cheetah) sample row excluded (description + URL); the merged
`Reminder` boilerplate row excluded; `Item No.` reconstructed as sequential
`1.`/`2.`/`3.` across retained data rows; exactly three genuine data rows
retained (`Example` + merged excluded from the count); every pre-table paragraph
(title, checklist heading + bullet, instructions) excluded; the tab-delimited
seven-column structure preserved on every line (with per-column order spot-check);
the trailing `ECR approval` column present and empty on data rows (line ends on
its tab boundary); and a merged row whose spanned cells **repeat** the same text
also dropped (covers the `_isMergedSpanRow` branch (b)).

#### Invariants locked in

1. **Header row always first, always literal** — the column header is emitted as
   the first output line with its literal labels; it is never numbered, never
   dropped.
2. **`Item No.` reconstructed sequentially** — retained data rows are numbered
   `1.`, `2.`, `3.`… in document order (Word auto-numbering re-derived); the
   `Example` and merged rows are excluded from the sequence.
3. **Merged/spanning rows dropped structurally** — a single grid-spanning cell
   **or** a row repeating the same merged text is detected by structure, never by
   matching the `Reminder` phrase.
4. **`Example` row excluded** — the conventional sample row never appears and
   consumes no ordinal.
5. **Pre-table exclusion preserved** — only the matched table is emitted; all
   preceding title/checklist/heading/instruction content stays excluded (now
   re-verified).
6. **Seven-column structure preserved** — every data row carries all seven
   tab-separated columns, including the trailing (usually empty) `ECR approval`.

---

### Session 4 — Download-screen UI (equal-height dropzones, Download All, next-steps panel)

Three Module Development UI refinements plus one new test file. All work is
additive UI chrome on the existing front page + results screen; the conversion
pipeline, privacy model (100% client-side), and download primitive are
untouched. The "Download All" control reuses the **existing** single-file
`OutputManager.downloadFile()` helper once per output (via
`ModuleResultsPage.triggerDownload`) — no new download path was introduced.

#### Changes

1. **Equal-height upload dropzones** (`css/styles.css`). `.module-drop` gained
   `width: 100%`, a shared `min-height: 200px`, and `display: flex` +
   `flex-direction: column` + centred `align-items`/`justify-content`. The
   `min-height` guarantees the two side-by-side zones
   (`Drop Writer's Template…` / `Drop Media List…`) render identically in the
   empty state **and** that neither collapses once a file is selected and the
   green staged-file chip appears beneath it. The slot grid already sat in a
   `repeat(2, minmax(0,1fr))` grid, so the shared `min-height` is what locks the
   two zones to the same height.
2. **"Download All" button** (`index.html` + `js/module-results-page.js`). A new
   `#module-download-all-bar` container sits between the file list and the
   actions bar. `ModuleResultsPage._renderDownloadAll()` injects a
   `Download All` button **only when `hasBothOutputs()`** (a Writer's Template
   `.txt` AND a Media List `.txt` are both present); single-file runs render an
   empty bar (collapsed via `.module-download-all-bar:empty { display:none }`),
   relying on the existing per-file button. Clicking it calls the new
   `triggerDownloadAll()`, which loops `triggerDownload()` once per output, so
   the canonical `downloadFile()` primitive fires exactly once per file.
3. **Next-steps instructions panel** (`index.html` + `js/module-results-page.js`).
   A new `#module-next-steps` panel renders beneath the downloads whenever
   `hasOutputs()` is true: an `<h3>` headed
   `Next steps — convert these files into finalized HTML` plus an ordered
   (`<ol>`) list of six steps (`Continue with Google` sign-in → open the
   `HTML Convertor` project → start a new chat → upload all three files
   (Writer's Template `.txt` + Media List `.txt` + an example completed module)
   → send the message → review and download the HTML). Heading + steps live in
   static `ModuleResultsPage.NEXT_STEPS_HEADING` / `NEXT_STEPS` arrays (pure,
   so the step list and count are assertable headlessly via `getNextSteps()`).
   The panel is cleared and re-hidden in the empty state.

#### Files touched (before → after line counts)

| File | Before | After |
|------|--------|-------|
| `js/module-results-page.js` | 353 | 480 |
| `index.html` | 271 | 273 |
| `css/styles.css` | 1044 | 1116 |
| `tests/module-dev-download-ui.test.js` | 0 (new) | 159 |

`js/module-results-page.js` (480) remains under the 500-line extracted-sub-module
threshold — no extraction required. No new JS module was created (methods were
added to the existing results-page class), so no `index.html` `<script>` or
`tests/test-runner.js` `loadScript` wiring was needed; the runner auto-discovers
`*.test.js` (now "Loading 55 test file(s)").

#### Tests

`tests/module-dev-download-ui.test.js` (**6** `it()`, new): Download All renders
when both `.txt` outputs are present; Download All hidden when only one output is
present (both template-only and media-only branches); clicking Download All
invokes the download helper exactly twice, once per file in output order (spy
`OutputManager`); the next-steps panel renders with its six ordered `<li>` steps
inside an `<ol>` and the heading; the rendered instructions contain the
`Continue with Google` and `HTML Convertor` strings; and the empty state clears +
hides both the next-steps panel and the Download All bar.

Final suite: **745/745 passing** (was 739; +6), 0 failed.

#### Invariants locked in

1. **Equal dropzone height in every state** — both `.module-drop` zones share a
   `min-height` floor, so they match height empty and after either slot is
   filled; neither collapses behind its staged-file chip.
2. **Download All is both-only** — the control renders/enables solely when both
   the Writer's Template `.txt` and Media List `.txt` are present
   (`hasBothOutputs()`); single-file runs never show it.
3. **Reuses the single-file download primitive** — `triggerDownloadAll()` calls
   `triggerDownload()` per output, so `OutputManager.downloadFile()` is invoked
   exactly once per file; no second download code path exists.
4. **Next-steps shown whenever there is output** — the panel renders for any
   non-empty output set (one or both files) and is cleared + hidden when empty;
   its six steps and heading are author-controlled UI chrome (pure constants),
   not writer content.

---

### Conversion-Complete View Refinements — Download Layout, Full-Width Next-Steps & Standardised Filenames

> **Module Development mode only.** Every change below is scoped to the
> post-conversion "Conversion complete" results view (`#module-results-section`
> + `ModuleResultsPage` + the Module Development filename generation in
> `ModeToggle._deriveFilename`). The Standard mode results view
> (`#results-section`, `App`, the `js/app.js` filenames) is **untouched** —
> confirmed by grep: `Convert Another Module` / the Module "Download All" live
> only in the Module Development markup + sub-module, and the **shared**
> `.file-list-panel` class was NOT edited (only wrapped).

**Status:** DONE. **751/751** tests pass (745 baseline → 751, **+6** across one
new test file; one existing filename assertion block was re-pointed, not grown).

#### Changes

1. **"Convert Another Module" button removed** (`index.html`). The
   `#btn-module-back` control and its enclosing `.actions-bar` were deleted from
   `#module-results-section`. The button was **not** shared markup — Standard
   mode's reset is the separate `#btn-reset` ("Parse Another File") in
   `#results-section` — so the removal is inherently scoped to Module
   Development. `ModuleResultsPage.returnToFrontPage()` / `_bindBack()` /
   `_bindModeReset()` are **left intact** (they no-op when the element is absent,
   and `tests/module-results-page.test.js` still exercises them through its own
   mock document), so no JS or test was removed.
2. **Horizontal download layout** (`index.html` + `css/styles.css`). The file
   rows (`#module-results-list`) + empty-state (`#module-results-empty`) are now
   wrapped in a `.module-downloads-files` column, and that column + the
   `#module-download-all-bar` sit inside a new `.module-downloads-row` flex row
   (`display:flex; flex-wrap:wrap; align-items:flex-start; gap:1rem`). The list
   column is **narrowed** to `flex: 0 1 480px` (narrower than full width) so the
   "Download All" button sits to its **right** rather than below. The shared
   `.file-list-panel` class was **not** modified (Standard mode's
   `#file-list-panel` is unaffected); the narrowing lives on the new wrapper.
3. **Auto-width "Download All" button** (`css/styles.css`). `.module-download-all`
   dropped its `width:100%` / `max-width:360px` block-stretch for
   `width: fit-content; align-self: flex-start` (intrinsic width). The bar
   (`.module-download-all-bar`) dropped `width:100%` / `max-width:720px` /
   `margin:0 auto` / `justify-content:center` for a top-aligned flex item; the
   `:empty { display:none }` collapse for single-file runs is retained.
4. **Full-width next-steps panel** (`css/styles.css`). `.next-steps-panel`
   dropped `max-width:720px` and `margin:0.25rem auto 0` (auto-centering) for
   `width:100%; margin:0.25rem 0 0`, so it now spans the full page content-area
   width (`<main>` `--max-width:1100px`).
5. **Emphasised reference phrase** (`js/module-results-page.js`). In
   `NEXT_STEPS[3]` (list item 4, "Into that new chat, upload all three files…")
   exactly the trailing phrase **"plus an example completed module to use as a
   formatting reference"** is wrapped in `<strong>…</strong>` (matching the
   established inline-emphasis treatment in this panel, alongside `<code>`); the
   rest of the item is unchanged.
6. **Standardised download filenames** (`js/mode-toggle.js`). `_deriveFilename`
   now emits `<MODULE_CODE> <label>_parsed.txt` — the module code being the input
   filename's **leading token** (any descriptive middle segment, e.g.
   "AI Digital Citizenship", dropped) and `<label>` being `"Writer's Template"`
   or `"Media List"`. The Media List suffix is **unified** from `_media_list` to
   `_parsed`. e.g. `OSAI201 AI Digital Citizenship.docx` →
   `OSAI201 Writer's Template_parsed.txt` / `OSAI201 Media List_parsed.txt`. The
   two `_convertSlot` call-sites now pass labels (`"Writer's Template"` /
   `"Media List"`) instead of suffixes. **Standard mode filenames
   (`js/app.js`, `code + '_parsed.txt'`) are untouched.**

#### Files touched (before → after line counts)

| File | Before | After | Change |
|------|-------:|------:|--------|
| `index.html` | 273 | 271 | Removed `#btn-module-back` + its `.actions-bar`; wrapped list/empty + download-all-bar in `.module-downloads-row` › `.module-downloads-files`. |
| `css/styles.css` | 1116 | 1128 | Added `.module-downloads-row` + `.module-downloads-files`; reworked `.module-download-all-bar` + `.module-download-all` to a right-of-list auto-width button; made `.next-steps-panel` full-width. (CSS has no line ceiling.) |
| `js/module-results-page.js` | 480 | 480 | Wrapped the trailing reference phrase in `NEXT_STEPS[3]` in `<strong>` (no line-count change). (≤500 sub-module ceiling.) |
| `js/mode-toggle.js` | 499 | 500 | Rewrote `_deriveFilename` to `<MODULE_CODE> <label>_parsed.txt` (leading-token code, unified `_parsed` suffix); updated both `_convertSlot` call-sites. Consolidated into a single compact method so the file held its 500-line ceiling rather than crossing it. (≤500 sub-module ceiling.) |
| `tests/module-conversion-flow.test.js` | 183 | 185 | Re-pointed test 7 from the old `ENGS301_parsed.txt` / `MediaList_media_list.txt` to the standardised `OSAI201 Writer's Template_parsed.txt` / `OSAI201 Media List_parsed.txt`. No `it()` count change (still 7). |
| `tests/module-dev-filenames.test.js` | — (new) | 76 | **6** `it()` cases (see below). |

No new JS module was introduced (the filename change was contained within
`mode-toggle.js`), so **no** `index.html` `<script>` or `tests/test-runner.js`
`loadScript` wiring change was needed; the runner auto-discovers `*.test.js`.

#### Test coverage

`tests/module-dev-filenames.test.js` (**6** `it()`, new — drives
`ModeToggle._deriveFilename` on a headless `new ModeToggle()` instance): Writer's
Template filename for a given module code → `OSAI201 Writer's Template_parsed.txt`;
Media List filename for a given module code → `OSAI201 Media List_parsed.txt`;
both conform to the `^OSAI201 .+_parsed\.txt$` pattern; the descriptive middle
segment ("AI Digital Citizenship") is dropped; the Media List suffix is `_parsed`
(never `_media_list`); and a differently-formatted (bare-code) filename
`ENGS301.docx` still yields the correctly-prefixed `ENGS301 Writer's
Template_parsed.txt`.

Final suite: **751/751 passing** (was 745; +6), 0 failed.

#### Invariants locked in

1. **Standard mode results view untouched** — only `#module-results-section`,
   `ModuleResultsPage`, and the Module Development filename path changed;
   `#results-section`, `#btn-reset`, the shared `.file-list-panel` class, and the
   `js/app.js` filenames are unchanged.
2. **No "Convert Another Module" control in Module Development** — the
   `#btn-module-back` markup is gone; the (guarded, browser-dead) JS binding
   remains only so the existing back-navigation unit test keeps passing.
3. **Download All is auto-width, right of the file list** — the button sizes to
   its content (`fit-content`, `align-self:flex-start`) and sits in the flex row
   beside the narrowed (`flex:0 1 480px`) file-list column, never full-width and
   never below it; the bar still collapses (`:empty`) on single-file runs.
4. **Next-steps spans the full content width** — no `max-width` / auto-centering
   constraint remains on `.next-steps-panel`.
5. **Filenames are `<MODULE_CODE> <label>_parsed.txt`** — leading-token module
   code, descriptive middle segment dropped, unified `_parsed.txt` suffix for
   both the Writer's Template and the Media List.
6. **mode-toggle.js held at the 500-line sub-module ceiling** — the filename
   change was consolidated into one compact `_deriveFilename` so the file did not
   cross its threshold.

---

### Conversion-Complete View Restyle — Header Consolidation, Centred Display Heading & Full-Width Cards

> **Module Development mode, presentation only.** A pure CSS/layout restyle of
> the post-conversion "Conversion complete" results view
> (`#module-results-section` + `ModuleResultsPage`) plus a small markup
> relocation of the shared header chrome (`.app-header`). No conversion logic,
> no privacy-model change, no Standard-mode change: `#results-section`,
> `js/app.js`, and the shared `.file-list-panel` / `.file-entry` classes were
> NOT edited (the cards container is widened via the `#module-results-list` ID
> selector + a new wrapperless layout, never by touching the shared class).

**Status:** DONE. **748/748** tests pass (751 baseline → 748, **−3** from
removing the now-defunct "Download All" `it()` cases; no new tests).

#### Changes

1. **"100% Client-Side" badge moved into the title row** (`index.html` +
   `css/styles.css`). The `.privacy-badge` left the far-right of the header bar
   and now renders **inline immediately right of the "PageForge" title**,
   vertically centred with it. New `.header-titles` (flex column) wraps a new
   `.title-row` (flex row, `align-items:center`, `gap:0.6rem`) holding the `<h1>`
   + badge, with the `.app-subtitle` directly beneath — unchanged.
2. **Mode toggle moved into the header bar** (`index.html` + `css/styles.css`).
   The `#mode-toggle` block (Mode label + segmented Module Development / Standard
   control) was **relocated out of its centred body position** (it used to sit
   above the front pages) into `.header-inner` as its **second flex child**, so
   the `space-between` header now reads **left** = title + badge + subtitle,
   **right** = Mode label + toggle. Position-only: the markup, the
   `mode-option-module` / `mode-option-standard` IDs, the radio wiring and all
   `ModeToggle` behaviour are byte-for-byte unchanged. `.mode-toggle` dropped its
   body spacing (`justify-content:center` + `padding:1rem 0 0.5rem` → `padding:0`).
3. **"Conversion complete" heading centred + enlarged** (`index.html` +
   `css/styles.css`). The heading's class changed from the shared
   `module-slot-title` (1rem, left-aligned) to a new dedicated
   `.module-results-title` (**2rem**, weight 700, `text-align:center`,
   `margin:0`). The shared `.module-slot-title` (front-page slot headings
   "Writer's Template" / "Media List") is **untouched**. The descriptive
   `.module-dev-intro` paragraph stays centred as before.
4. **File result cards made full-width** (`index.html` + `css/styles.css`). The
   `.module-downloads-row` flex row and the narrowed `.module-downloads-files`
   (`flex:0 1 480px`) column wrappers were **removed**; `#module-results-list`
   (the `.file-list-panel`) now sits directly in the section at `width:100%`, and
   `#module-results-section` became a centred flex column (mirroring
   `#module-dev-section`: `align-items:center; gap:1.25rem; padding:1.5rem 0 2rem`).
   Each card is the **shared `.file-entry`** — already `justify-content:space-between`,
   so filename + type label sit left and the per-file Download button right; the
   cards now stack vertically at full container width. `.file-entry` /
   `.file-list-panel` CSS was **not** modified.
5. **Standalone "Download All" removed** (`index.html` + `css/styles.css` +
   `js/module-results-page.js`). Deleted the `#module-download-all-bar` markup;
   the `_renderDownloadAll()`, `_bindDownloadAll()`, `triggerDownloadAll()` and
   `hasBothOutputs()` methods, the `downloadAllBar` element ref and the
   `_renderDownloadAll()` call in `show()`; and the `.module-download-all-bar` /
   `.module-download-all` CSS. `grep -rn` confirmed no other code path referenced
   any of these before deletion; the only surviving "Download All" string is the
   **unrelated Standard-mode** "Download All as ZIP" (`js/app.js` /
   `index.html`), which is out of scope and untouched. The per-file Download
   buttons inside each card are unchanged.

#### Files touched (before → after line counts)

| File | Before | After | Change |
|------|-------:|------:|--------|
| `index.html` | 271 | 268 | Wrapped title + badge in `.header-titles` › `.title-row`; relocated `#mode-toggle` into `.header-inner`; removed the body `#mode-toggle`; heading class `module-slot-title` → `module-results-title`; unwrapped the download list (removed `.module-downloads-row` / `.module-downloads-files` / `#module-download-all-bar`). |
| `css/styles.css` | 1128 | 1135 | Added `.header-titles` + `.title-row`; `.mode-toggle` body spacing → `padding:0`; replaced the `.module-downloads-row` / `.module-downloads-files` / `.module-download-all-bar` / `.module-download-all` block with `#module-results-section` (centred flex column) + `.module-results-title` (2rem centred heading) + `#module-results-list { width:100% }`; `.next-steps-panel` kept. (CSS has no line ceiling.) |
| `js/module-results-page.js` | 480 | 410 | Removed `hasBothOutputs()`, `triggerDownloadAll()`, `_renderDownloadAll()`, `_bindDownloadAll()`, the `downloadAllBar` el ref, and the `_renderDownloadAll()` call in `show()`. (≤500 sub-module ceiling — comfortably under.) |
| `tests/module-dev-download-ui.test.js` | 159 | 100 | Removed the **3** Download-All `it()` cases (render-when-both / hide-when-one / invoke-helper-twice), the now-unused `mddSpyOutputManager` spy and the `module-download-all-bar` mock element; dropped the Download-All assertion from the empty-state case; updated the header comment + `describe` title. The **3** next-steps `it()` cases are unchanged (6 → 3). |

No new JS module and no new test file ⇒ **no** `index.html` `<script>` or
`tests/test-runner.js` `loadScript` wiring change. `js/mode-toggle.js` (500),
`js/app.js` (1364) and `js/output-manager.js` are untouched.

#### Test coverage

`tests/module-dev-download-ui.test.js` (**3** `it()`, was 6): renders the
next-steps instructions panel with its six ordered steps; the instructions
contain the `Continue with Google` and `HTML Convertor` strings; clears and
hides the next-steps panel in the empty state. The three removed cases tested
the deleted Download-All control and would otherwise call the now-deleted
`hasBothOutputs()` / `triggerDownloadAll()`.

Final suite: **748/748 passing** (was 751; −3), 0 failed.

#### Invariants locked in

1. **Header consolidation** — `#mode-toggle` appears **exactly once** and lives
   inside `<header>`; the `space-between` `.header-inner` shows title + inline
   "100% Client-Side" badge + subtitle on the left, Mode label + segmented toggle
   on the right.
2. **Mode-toggle move is position-only** — markup, the `mode-option-module` /
   `mode-option-standard` IDs, the radio wiring and `ModeToggle` behaviour are
   unchanged; only its DOM location and `.mode-toggle` body spacing moved.
3. **Heading is centred + enlarged via its own class** — `.module-results-title`
   (2rem, centred); the shared `.module-slot-title` (front-page slots) is
   unchanged.
4. **Cards are full-width, stacked** — `#module-results-list` spans the full
   content width; each shared `.file-entry` keeps filename + type label left and
   the per-file Download button right; `.file-entry` / `.file-list-panel` CSS is
   unedited.
5. **No "Download All" in Module Development** — its markup, the four
   `ModuleResultsPage` methods, the CSS and its three tests are gone; only the
   per-file Download remains. Standard-mode "Download All as ZIP" is untouched.
6. **Standard mode untouched** — `#results-section`, `js/app.js`, and the shared
   `.file-list-panel` / `.file-entry` classes were not modified.
7. **File-size hygiene held** — `js/module-results-page.js` 480 → 410 (≤500);
   `js/mode-toggle.js` / `js/app.js` untouched; no extraction required.

---

### Front-Page & Results-Screen Markup Simplification — Labels, Hints, Paired Chips, Convert Label & Results Width

> **Module Development mode, presentation only.** Pure markup/CSS refinements to
> the two Module Development screens — the front/upload page (`#module-dev-section`)
> and the results/download page (`#module-results-section`). No conversion logic,
> no privacy-model change, no Standard-mode change, no JS touched. `#upload-section`,
> `#results-section`, `js/app.js`, `js/mode-toggle.js` and `js/module-results-page.js`
> are all unchanged.

**Status:** DONE. **748/748** tests pass (748 baseline → 748, **±0** — these are
presentational markup/CSS changes; no test parses `index.html` or asserts on the
altered strings, so no test was added or modified).

#### Changes — front page (`#module-dev-section`)

1. **Intro line simplified** (`index.html`). The two-sentence
   `.module-dev-intro` copy "Upload a Writer's Template and/or a Media List. Both
   are optional — provide at least one to activate." was reduced to the single
   sentence **"Upload a Writer's Template and/or a Media List."**; the trailing
   "Both are optional — provide at least one to activate." sentence was deleted.
2. **Slot heading labels removed** (`index.html`). The two
   `<h2 class="module-slot-title">` labels above the drop zones — **Writer's
   Template** and **Media List** — were deleted. Only the two label elements were
   removed; the drop zones themselves are untouched. The `.module-slot-title` CSS
   rule was **deliberately left in place** (the task scoped the removal to "only
   those two label elements"; it does not reference the rule elsewhere now, but
   removing the rule was out of the stated scope).
3. **"Optional" drop-zone hints removed** (`index.html`). The
   `<p class="drop-zone-hint">Optional</p>` line inside **each** of the two
   `.module-drop` zones was deleted; the "Drop … .docx or click to browse" prompt
   text is retained. The shared `.drop-zone-hint` CSS rule is **untouched** (it is
   still used by the Standard front page hint and the `#module-results-empty`
   empty-state line).
4. **Paired uploaded-file chips — verified, no change needed** (`index.html`).
   The selected-file chips (`#module-template-info` / `#module-media-info`,
   toggled via `.hidden` by `ModeToggle._renderSlot`, which only flips visibility
   and sets the filename text — it never relocates the node) **already** sit
   inside their own `.module-upload-slot` column, directly beneath their paired
   drop zone, within the existing two-column `.module-upload-grid`
   (`repeat(2, minmax(0,1fr))`). `.module-upload-slot` is already a vertical stack
   (`display:flex; flex-direction:column`), so each chip already renders directly
   under its own zone with the columns side-by-side. The desired end state was
   confirmed present; per the "keep the diff minimal" guidance no markup move or
   CSS change was introduced for the chips.
5. **Primary action relabelled** (`index.html`). The button visible text was
   changed from **Activate** to **Convert**. Only the text node changed; the
   `id="btn-module-activate"`, the `class="btn btn-convert"`, the
   `aria-label="Activate module development conversion"`, and the
   `ModeToggle._bindActivate` handler wiring are all unchanged.

#### Changes — results / download page (`#module-results-section`)

6. **Results intro paragraph removed** (`index.html`). The
   `<p class="module-dev-intro">Your parsed text file(s) are ready. Download each
   below — …</p>` paragraph was deleted from the results section entirely; the
   `Conversion complete` heading is now immediately followed by
   `#module-results-list`.
7. **`.module-dev-intro` CSS rule retained** (`css/styles.css`). Per the "if and
   only if referenced nowhere else" guard, `grep -n "module-dev-intro"` across
   `index.html`, `js/` and `css/styles.css` after the edit shows the rule is
   **still referenced** by the front-page intro (`index.html:53`). The rule was
   therefore **kept** (deleting it would have broken the front-page intro styling).
8. **Results section width constrained** (`css/styles.css`). `width: 70%;` and
   `margin: 0 auto;` were appended to the **existing** `#module-results-section`
   rule (the centred flex-column rule with `gap:1.25rem; padding:1.5rem 0 2rem`)
   via a targeted `str_replace` — no duplicate selector, no inline style on the
   element.

#### Files touched (before → after line counts)

| File | Before | After | Change |
|------|-------:|------:|--------|
| `index.html` | 268 | 259 | Front page: shortened `.module-dev-intro` to one sentence (−1); removed two `.module-slot-title` headings (−2); removed two `Optional` `.drop-zone-hint` lines (−2); `Activate` → `Convert` button text. Results: removed the `.module-dev-intro` paragraph (−4). |
| `css/styles.css` | 1135 | 1137 | Appended `width: 70%;` + `margin: 0 auto;` to the existing `#module-results-section` rule (+2). (CSS has no line ceiling.) |

No JS file was touched (so **no** `index.html` `<script>` / `tests/test-runner.js`
`loadScript` wiring change, and **no** file-size threshold was approached:
`js/mode-toggle.js` stays at 500, `js/module-results-page.js` at 410). No test
file was added or modified — no test reads `index.html` (the runner's only
`readFileSync` loads JS modules), and the `Activate` / `Writer's Template` /
`Media List` strings present in the test suite are JS method names
(`isActivateEnabled`), `it()` descriptions, `ModuleResultsPage` `SLOT_LABELS`, and
`_deriveFilename` label arguments — none of which were changed.

#### Invariants locked in

1. **Front-page intro is one sentence** — `.module-dev-intro` on
   `#module-dev-section` reads exactly "Upload a Writer's Template and/or a Media
   List." with no trailing optional/activate sentence.
2. **No slot heading labels, no "Optional" hints** — neither
   `.module-slot-title` heading nor any `Optional` `.drop-zone-hint` remains inside
   `#module-dev-section`; the drop-zone prompt text and the shared
   `.drop-zone-hint` / `.module-slot-title` CSS rules are intact.
3. **Each chip is paired under its own zone** — `#module-template-info` and
   `#module-media-info` sit inside their respective `.module-upload-slot` columns,
   directly beneath their paired drop zone, with the two columns side-by-side.
4. **Primary action says "Convert"** — the button label is `Convert`; its `id`,
   classes, `aria-label` and handler wiring are unchanged.
5. **No intro paragraph on the results screen** — `#module-results-section`
   contains no `.module-dev-intro` paragraph; the `.module-dev-intro` CSS rule is
   retained because the front-page intro still uses it.
6. **Results screen is 70%-wide, centred** — the existing
   `#module-results-section` rule carries `width: 70%; margin: 0 auto;` (single
   rule, no duplicate selector, no inline style).
7. **Standard mode + pipeline untouched** — no JS, no conversion logic, no
   `#upload-section` / `#results-section` / `js/app.js` change; 748/748 tests
   unchanged.

---

[← Back to index](../CLAUDE.md)
