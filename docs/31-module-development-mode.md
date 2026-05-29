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

[← Back to index](../CLAUDE.md)
