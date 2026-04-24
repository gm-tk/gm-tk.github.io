# 21. OSAI201 Layout-Table Sidebar Defects (Phase 13)


### Overview

Phase 13 fixes three concrete content-loss defects discovered in the
OSAI201 "Picture This!" / "What is AI?" writer template, all of which
trace back to the Phase 6 / Phase 6.1 layout-table unwrapping pipeline.
The document contained a two-column layout table whose right cell held
`[image]` + hyperlink URL in paragraph 1 and a fully-red CS writer
instruction in paragraph 2, preceded by a standalone `[H2] Lesson 1:
What is AI?` red paragraph and followed by a `[body]` paragraph.
Parsing this section dropped the `[image]` tag, truncated the URL
with a dangling `🔴[RED` red-text fragment, and lost the entire CS
writer-instruction paragraph. All three defects originated inside a
single method — `LayoutTableUnwrapper._createSidebarBlock()` — and are
fixed at the root rather than papered over downstream. The H2 heading
proved not to be dropped by the unwrapper or block-scoper (verified by
new tests); its perceived disappearance in the user's original output
was a side-effect of the sidebar-cell text corruption below.

**Status:** DONE — 1 file modified (js/layout-table-unwrapper.js),
1 test file created (tests/osai201Defects.test.js with 9 tests),
488 tests passing (was 479 — 9 new tests added), 0 failing. All
previously-passing tests continue to pass.

### Files Modified

| File | Changes |
|------|---------|
| `js/layout-table-unwrapper.js` | Rewrote `_createSidebarBlock()` to: (1) tighten the URL extraction regex from `/(https?:\/\/[^\s\]]+)/` to `/(https?:\/\/[^\s\[\]\uD83D]+)/` so the high surrogate of the 🔴 red-text emoji (U+1F534 = `\uD83D\uDD34`) and `[` stop the match, preventing `URL🔴[RED` fragments from being captured as part of the URL; (2) preserve the `[image]` marker in the synthetic sidebar_image paragraph by emitting a multi-run structure with a red `[image]` run followed by a plain space and a hyperlinked URL run (instead of a single bare-URL run); (3) classify each paragraph in the sidebar cell as either "image/alert-absorbed" (contains the URL, `[image]` tag, or alert tag/content) or "extra" (e.g., a fully-red CS writer instruction), and emit extras as additional preserved paragraph blocks (with `_cellRole: 'sidebar_extra'`) rather than discarding them. Also updated `unwrapLayoutTables()` to accept either a single block or an array of blocks back from `_createSidebarBlock()`. |
| `tests/osai201Defects.test.js` | New file — 9 tests covering Defect 1 (H2 heading preservation, direct unwrap), Defect 2 (image tag + URL in sidebar block + correct `_sidebarImageUrl` annotation), Defect 3 (CS paragraph preserved somewhere in the output, no truncated red-text fragments, writer-instruction classification via BlockScoper.detectWriterInstruction), pipeline-level assertion (H2 + body survive unwrap AND block-scope), and a sanity check that the `[body]` paragraph after the table resolves intact. |

### Defects — Root Causes and Fixes

#### Defect 1 — `[H2] Lesson 1: What is AI?` heading appears lost
- **Reported symptom:** The H2 heading immediately preceding the layout
  table never appears anywhere in the converted output.
- **Root cause:** **The H2 heading is NOT dropped** by the unwrapper,
  block-scoper, page-boundary, or tag normaliser. Two new tests verify
  this — both the single-stage (unwrap only) and pipeline-level
  (unwrap + block-scope) tests confirm the H2 block survives intact.
  The user's perception that the heading had "disappeared" was caused
  by a downstream rendering artefact of Defects 2 and 3: the sidebar
  cell's corrupted text (`URL🔴[RED`) plus the vanished CS paragraph
  made the content around the table look truncated in the review
  panel, which read as "the H2 is missing" when really it was the
  right-cell text that was broken.
- **Fix:** No code fix required for the H2 heading itself. The new
  tests lock in the invariant that paragraphs immediately preceding a
  layout table are never consumed by the unwrapper, so any future
  regression is caught.

#### Defect 2 — `[image]` red tag lost + URL captures `🔴[RED` fragment
- **Reported symptom:** The `[image]` marker disappears cleanly from
  the right-cell output, and the URL displayed ends with a dangling
  `🔴[RED` fragment.
- **Root cause (two bugs in one method):**
  1. **URL regex over-capture.** The hyperlinked URL run was followed
     by a red-coloured space run (`" "`). After `_buildFormattedText()`
     concatenated the runs, the resulting text looked like
     `...URL🔴[RED TEXT]   [/RED TEXT]🔴`. The URL extraction regex
     `/(https?:\/\/[^\s\]]+)/` excluded only whitespace and `]`, so the
     match greedily walked past the URL and swallowed the first few
     chars of the following red-text marker (`🔴[RED`) — resulting in
     `_sidebarImageUrl = "URL🔴[RED"`. This broken URL was then passed
     to `_renderImagePlaceholder()` and rendered as-is.
  2. **`[image]` tag discarded.** The synthetic image paragraph was
     built with `runs: [{ text: imageUrl || '[IMAGE]', ... isRed: false }]`
     — a single, non-red run containing ONLY the URL. The red `[image]`
     marker that was present in the original cell paragraph was dropped
     entirely from the text stream, so any downstream logic that looks
     for the `[image]` tag (e.g., the review panel's text display, tag
     analysis, future rendering improvements) could not see it.
- **Fix:**
  1. Tightened the URL regex to `/(https?:\/\/[^\s\[\]\uD83D]+)/`. The
     added `\uD83D` character class stops the match at the high
     surrogate of any red-text emoji (U+1F534 = `\uD83D\uDD34`), and
     the added `[` stops at the opening of any subsequent square-bracket
     tag fragment. Result: `_sidebarImageUrl` now contains only the
     clean URL.
  2. Rebuilt the synthetic image paragraph to carry THREE runs: a red
     `[image]` run (so the marker appears in `_buildFormattedText`
     output with proper `🔴[RED TEXT] [image] [/RED TEXT]🔴` wrapping),
     a plain space, and a hyperlinked plain URL run. The paragraph's
     `text` property is set to `"[image] URL"` so downstream consumers
     that read `para.text` directly still see the tag.

#### Defect 3 — Fully-red CS writer-instruction paragraph dropped
- **Reported symptom:** The second paragraph in the right cell
  (`CS: can a cross be put through the brain image to show it is AI
  is not a brain.`, entirely red) is replaced by a broken opening
  `🔴[RED` wrapper and nothing else.
- **Root cause:** `_createSidebarBlock()` with `role === 'sidebar_image'`
  collected text from ALL paragraphs in the cell into an `allText`
  buffer and an `alertText[]` accumulator, extracted the URL and clean
  text — then built a SINGLE synthetic paragraph whose only payload
  was the (broken) URL. The remaining paragraph content — including
  the fully-red CS writer instruction — was discarded. Worse, the
  over-capturing URL regex from Defect 2 made the URL string end with
  `🔴[RED`, which is where the "dangling red-text fragment" came from.
  The CS paragraph content itself was lost; the fragment was not the
  CS paragraph but a shard of the red space run that followed the URL
  inside the SAME paragraph.
- **Fix:** `_createSidebarBlock()` now performs a two-pass
  classification of the cell's paragraphs:
  - **Pass 1** decides which paragraphs are "absorbed" into the
    synthetic sidebar block. For `sidebar_image`, a paragraph is
    absorbed if it contains the `[image]` tag OR a URL. For
    `sidebar_alert`, a paragraph is absorbed if it contains an alert
    tag OR contributes non-empty clean text.
  - **Pass 2** collects all non-absorbed paragraphs (with meaningful
    text) into an `extras[]` array. Each extra is wrapped as a
    standalone paragraph block with `_cellRole: 'sidebar_extra'` and
    emitted into the content stream right after the synthetic sidebar
    block.
  - `unwrapLayoutTables()` was updated to accept either a single
    block or an array of blocks back from `_createSidebarBlock()`.
  - The fully-red CS paragraph is now preserved verbatim as a
    `sidebar_extra` block. Its original `runs[]` array (with
    `formatting.isRed: true`) survives unchanged, so downstream
    writer-instruction detection
    (`BlockScoper.detectWriterInstruction`) continues to classify it
    correctly — a new test verifies this classification on the
    `"CS: can a cross …"` text.

### The New Test Suite (tests/osai201Defects.test.js)

| Test | Asserts |
|------|---------|
| Defect 1 — H2 survives unwrap | `[H2] Lesson 1: What is AI?` paragraph still present in the unwrapped content stream |
| Defect 1 — unwrapper does not consume preceding paragraphs | First block is still the H2 paragraph with `[H2]` tag and `"Lesson 1"` text after unwrapping |
| Defect 2 — `[image]` tag + URL coexist | After unwrapping, some block contains both `[image]` and the iStock URL |
| Defect 2 — `_sidebarImageUrl` is clean | `_sidebarImageUrl === 'https://www.istockphoto.com/photo/fun-unicorn-3d-illustration-gm978974888-266040224'` (no `🔴[RED` appended) |
| Defect 3 — CS paragraph preserved | The text `"can a cross be put through"` is found somewhere in the unwrapped stream (direct block text, `_sidebarParagraphs`, or `_sidebarAlertContent`) |
| Defect 3 — no truncated red-text fragments | For every block, `count('🔴[RED TEXT]') === count('[/RED TEXT]🔴')` AND no block contains a bare `🔴[RED` not followed by ` TEXT]` |
| Defect 3 — writer-instruction classification | `BlockScoper.detectWriterInstruction("CS: can a cross be put through the brain image to show it is AI is not a brain.")` returns `isWriterNote: true` |
| Pipeline — H2 + [body] survive scope analysis | After `unwrapLayoutTables()` followed by `BlockScoper.scopeBlocks()`, both the H2 heading and the `[body]` paragraph remain in the content array |
| `[body]` paragraph intact | `[body]` tag + `"AI stands for artificial intelligence"` prose still present after unwrap |

### Test Fixtures

The test file defines three helpers — `_mkRun(text, opts)`,
`_mkParaFromRuns(runs, opts)`, `_mkBlockParaFromRuns(...)`, and
`_mkBlockTable(rowsSpec)` — that mirror the DocxParser output
structure for multi-run paragraphs (a capability the existing
`mkPara` / `mkTable` helpers in `layoutTableUnwrapper.test.js` don't
provide since they only build single-run paragraphs). The core
fixture `_buildOsaiSnippet()` assembles a three-block content array:

1. A standalone red `[H2] Lesson 1: What is AI?` paragraph
2. A two-column layout table whose:
   - Left cell has `[speech bubble]` (red) + plain "Kia ora …" text
   - Right cell has two paragraphs: `[image]` (red) + red space +
     hyperlinked URL + trailing red space, then a fully-red CS writer
     instruction
3. A `[body]` paragraph (red tag + plain prose) — the SDT-wrapped
   tracked-change case, modelled at the resolved level since
   DocxParser's `<w:ins>` unwrap / `<w:del>` strip handling is what
   the unwrapper receives

### Invariants Locked In By Phase 13

1. **Paragraphs immediately preceding a layout table are never
   consumed by the unwrapper.** Any such paragraph — regardless of
   red-text content, heading level, or tag — passes through as-is.
2. **Red-only tag runs at the start of a paragraph (e.g., `[image]`
   before a hyperlink) are preserved through sidebar synthesis.** The
   tag marker survives in the synthetic paragraph's `runs[]` with
   `isRed: true`, so `_buildFormattedText` and downstream consumers
   continue to see it.
3. **Fully-red paragraphs in sidebar cells produce a properly-closed
   `🔴[RED TEXT] … [/RED TEXT]🔴` wrapper and are preserved as
   `sidebar_extra` blocks.** They are available for writer-instruction
   classification per Phase 6 rules and will not leak a truncated
   `🔴[RED` fragment into any other block.
4. **URL extraction from sidebar-cell formatted text never swallows
   the following red-text emoji.** The regex class
   `[^\s\[\]\uD83D]` guarantees that the `\uD83D` high surrogate of
   🔴 (U+1F534) terminates any URL match, so `_sidebarImageUrl`
   holds a clean URL even when a red-coloured run (such as a
   trailing space) immediately follows the hyperlink.


---

### Session E — Body Content Rendering Fixes

Two narrow body-content rendering bugs discovered during calibration,
both template-agnostic.

- **Change 1 — Alert + layout-table pairing.** When the writer uses
  `[alert]` immediately followed by a layout table whose main cell
  carries bullets/paragraphs and whose sidebar cell carries an image,
  PageForge previously emitted an EMPTY `<div class="alert">` — the
  main-cell content never reached the alert body. Root cause: the
  alert-content collector pushed the main-cell paragraphs as plain
  text, losing list structure; the synthetic sidebar block then
  broke collection and the paired layout was never constructed.
  Fix: in `_renderBlocks()`'s `[alert]` branch, detect following
  blocks carrying `_unwrappedFrom: 'layout_table'` + `_cellRole:
  'main_content'`, consume them as alert body (preserving lists via
  `_renderList`), and pair with any adjacent sidebar block
  (`_sidebarImageUrl` / `_sidebarAlertContent`) using
  `_wrapSideBySide()` at column widths `col-md-6 col-12 paddingR`
  (alert) + `col-md-3 col-12 paddingL` (image). `_wrapSideBySide()`
  gained two optional parameters for the column classes; existing
  callers retain the default `col-md-8` + `col-md-4` widths.
- **Change 2 — `contentRules.suppressDuplicateLessonTitleH2` flag
  (default OFF).** Some writers open a lesson with `[H2] *Lesson 1:
  What is AI?*`, duplicating the page `<h1>`. When this flag is set
  to `true` in the resolved template config AND the page is a lesson
  page AND the first rendered body block is an `[H1]`/`[H2]` whose
  normalised text (stripping `*`/`**`/`***`, `Lesson N:` /
  `Lesson N -` / `Lesson N.` prefix case-insensitively) matches
  `pageData.lessonTitle`, the heading is skipped. Default is `false`,
  so behaviour is unchanged unless a template opts in. Added to
  `templates/templates.json` baseConfig and mirrored in the
  `TemplateEngine._embeddedData()` fallback.

**Files touched:** `js/html-converter.js`, `templates/templates.json`,
`js/template-engine.js` (embedded fallback only). New tests:
`tests/alertWithSidebarImage.test.js` (6 cases),
`tests/suppressDuplicateLessonTitleH2.test.js` (7 cases).

**Post-merge test count:** 534/534 passing (was 521 — 13 new tests).


---

### Session F — [alert] preceding-body wrap + TABLE bullets+image pairing + iStock src normalisation

Three narrow body-content rendering calibrations discovered during the
"AI environmental strain" writer-template review. All three share the
same writer-template pattern: a `[body]` paragraph immediately followed
by a standalone `[alert]` marker and then a layout-style table whose
left cell contains an intro sentence + bullet list and whose right cell
contains an `[image]` marker + iStockPhoto URL. Previously this pattern
produced an empty `<div class="alert">`, a silently-dropped table, and
a generic `placehold.co` placeholder image.

**Sub-bug A — `[alert]` marker wraps the immediately-preceding `[body]`.**
The `[alert]` branch in `_renderBlocks` previously called `flushPending()`
before any sub-branch decided whether the pending `[body]` content
should remain a sibling row or be consumed by the alert. Result: the
body flushed as a standalone `col-md-8` row and the alert (with no
own-content and no layout-table pairing) emitted an empty inner
`col-12`. Fix: the initial `flushPending()` is now deferred; each
sub-branch (layout-table pairing, preceding-body wrap, fallback
`_collectAlertContent`) performs its own flush at the correct point.
A new check pops the last pendingContent entry when it was emitted by
an immediately-preceding `[body]` (or untagged) paragraph and wraps it
inside the alert's inner `<div class="row"><div class="col-12">…</div></div>`.
Headings, list items, and non-adjacent preceding bodies are excluded,
so the existing heading-before-alert and alert-at-start-of-document
cases continue to emit empty alerts as before.

**Sub-bug B — TABLE row with bullets + `[image]` cells emits a paired
`col-md-6 paddingR` alert + `col-md-3 paddingL` image layout.** The
block processor promotes the table's `[image]` tag to primary, so the
block-renderer's `tagName === 'image'` branch previously consumed the
table as if it were a standalone image — silently dropping the bullet
content and the iStock URL (because a `type: 'table'` block carries no
`cleanText`/`formattedText` for `_extractImageInfo` to read). Fix: two
new helpers on `HtmlConverterRenderers` — `_detectBulletsAndImageTable`
(returns `{bulletsColIdx, imageColIdx, introText, bulletItems, imageRef}`
when one cell has bullet list items and the sibling cell has an
`[image]` marker, otherwise `null`) and `_renderBulletsAndImageTable`
(emits the paired `col-md-6 col-12 paddingR` alert + `col-md-3 col-12
paddingL` image row). A dispatch check inserted before the `[image]`
branch routes qualifying tables through the new helper. Bullets-only
and image-only tables return `null` and fall through to the existing
single-column handlers. The `[image]` branch also gained a
`pBlock.type !== 'table'` guard so it never steals a table block again.

**Sub-bug C — iStockPhoto URLs resolve to `images/iStock-<ID>.jpg`.**
`renderImage` and `renderImagePlaceholder` previously emitted
`src="placehold.co/…?text=Image+Placeholder"` plus a commented-out
iStock reference. Fix: when the URL matches the iStockPhoto pattern
and a `-gm<NUMERIC_ID>-` segment is present, both helpers now emit
`src="images/iStock-<NUMERIC_ID>.jpg"` directly, with `alt=""` kept
empty per the "no fabricated alt text" invariant. Non-iStockPhoto URLs
retain their existing `placehold.co` placeholder behaviour.

**Files touched (before → after line counts):**

| File | Before | After |
|------|-------:|------:|
| `js/html-converter-block-renderer.js` | 1124 | 1184 |
| `js/html-converter-renderers.js`      |  798 |  930 |
| `tests/lmsCompliance.test.js`         |  682 |  690 |

Both JS sub-modules were already above the ≤500-line sub-module
hygiene threshold before this session (see `docs/29` HC-R6). The +60
and +132 increments land against the same known overshoot — flagged
for the `docs/29` remediation backlog; no extraction attempted as part
of this bug-fix session.

**`tests/lmsCompliance.test.js`** — CHANGE 18's four `it()` cases were
updated to assert the new `src="images/iStock-<ID>.jpg"` + `alt=""`
contract rather than the old `placehold.co/?text=Image+Placeholder` +
`alt="iStock-<ID>"` contract. Case count unchanged.

**New test files:**

| File | `it()` cases |
|------|-------------|
| `tests/alert-tag-preceding-body-association.test.js`   | 8 |
| `tests/table-with-inline-image-rendering.test.js`      | 9 |

Cases covered (`alert-tag-preceding-body-association.test.js`): alert
wraps a single preceding body paragraph; alert does NOT wrap a
preceding heading block; alert does NOT wrap a body separated by an
intervening heading; two consecutive `[body]` + `[alert]` sequences
each wrap their own preceding body; alert as the first block renders
empty (regression guard); unicode/punctuation survive the wrap intact;
exact `<div class="alert"><div class="row"><div class="col-12"><p>…</p></div></div></div>`
nesting; fallback `_collectAlertContent` path still consumes a
following untagged paragraph when no preceding `[body]` is present.

Cases covered (`table-with-inline-image-rendering.test.js`): paired
`col-md-6 paddingR` alert + `col-md-3 paddingL` image row with
bullet list rendered inside the alert; `**bold**` markdown stripped
from the intro sentence (plain `<p>` — not wrapped in `<b>`); bullet
items rendered as `<li>` with any leading `•` character stripped;
iStock URL `…-gm2206845926-…` maps to `src="images/iStock-2206845926.jpg"`
with `alt=""` and no `placehold.co`; non-iStock URL retains
`placehold.co` placeholder; `<img …>` carries `class="img-fluid"`,
`loading="lazy"`, and `alt=""`; bullets-only table (no image cell)
retains single-column grid behaviour; image-only table (no bullets)
retains single-column handling; full `[body] + [alert] + TABLE + [body]`
integration matches the reference input → target output mapping.

**Invariants locked in by this session:**

- `[alert]` marker with no content of its own and no layout-table
  pairing wraps the immediately-preceding `[body]` block inside its
  inner `<div class="row"><div class="col-12">…</div></div>` — not as
  a sibling row and not as an empty alert.
- A TABLE row containing a bullets cell + an `[image]` cell emits a
  single two-column row with `col-md-6 col-12 paddingR` wrapping an
  alert (`<p>intro</p><ul><li>…</li></ul>`) and `col-md-3 col-12
  paddingL` wrapping `<img>`. Bullets-only and image-only tables retain
  their existing single-column behaviour (verified by regression
  cases).
- iStockPhoto URLs (matching `https://www.istockphoto.com/<type>/<slug>-gm<ID>-<variantID>`)
  are normalised to `src="images/iStock-<ID>.jpg"` via the digits
  immediately following `-gm`. `alt=""` stays empty — no alt text is
  fabricated from the iStock id or the URL.

**Final pass/total:** 648/648 tests passing (up from 631 — 17 new
`it()` cases across two files; four existing `lmsCompliance` cases
updated in place to match the new iStock src contract; no
regressions).


---

### Session G — Gate `_renderBulletsAndImageTable` alert wrapper behind caller flag

**Problem.** Session F added `_detectBulletsAndImageTable` +
`_renderBulletsAndImageTable` on `HtmlConverterRenderers` to emit the
paired `col-md-6 col-12 paddingR` alert + `col-md-3 col-12 paddingL`
image row for TABLE blocks pairing a bullets cell with an `[image]`
cell. The renderer unconditionally wrapped the bullets column in
`<div class="alert">`, regardless of whether the writer authored an
`[alert]` marker before the table. The standalone `[image]`-branch
dispatch in `html-converter-block-renderer.js` called the renderer for
any qualifying bare two-column table, so any such table silently gained
an alert element it was not asked for — a hidden auto-alerting rule
that produced LMS output styled as "alert boxes" for content the writer
never tagged as an alert. (The separate `[alert]`-marker-going-empty
defect when authored before such a table is tracked as a follow-up and
is **not** addressed by this session.)

**Fix.** `_renderBulletsAndImageTable` now takes a third `options`
parameter (`{ alertWrap?: boolean }`, default `false`). The
`<div class="alert">…</div>` wrapper around the inner
`<div class="row"><div class="col-12">…</div></div>` is emitted only
when the caller passes `{ alertWrap: true }`. When `alertWrap` is
`false` (or omitted), the inner row/col-12 grid renders directly inside
the `col-md-6 col-12 paddingR` column, with no alert div in between.
The outer row scaffolding, column class names, `<img>` emission, iStock
`-gm<ID>-` → `images/iStock-<ID>.jpg` mapping, leading-bullet stripping,
`placehold.co` fallback for non-iStock URLs, and every other structural
element are unchanged.

The only call site of `_renderBulletsAndImageTable` —
`html-converter-block-renderer.js:889` (the standalone `[image]`-branch
dispatch that fires before the bare `tagName === 'image'` branch) —
now passes `{ alertWrap: false }` explicitly, even though it equals the
new default. The explicit pass-through makes the intent
grep-discoverable and documents that this is the bare-table path that
must NOT emit an alert.

**Files touched (before → after line counts):**

| File | Before | After |
|------|-------:|------:|
| `js/html-converter-renderers.js`                         |  930 |  943 |
| `js/html-converter-block-renderer.js`                    | 1184 | 1184 |
| `tests/table-with-inline-image-rendering.test.js`        |  240 |  271 |

Both JS files are already above the ≤500-line sub-module hygiene
threshold and tracked in the `docs/29` remediation backlog (HC-R6).
The edits in this session are small surgical additions (+13 lines in
`html-converter-renderers.js` for the options signature, JSDoc, and
if/else alert-wrap branching; +0 net in
`html-converter-block-renderer.js` — a single-line in-place edit at
the dispatch call site). No sub-module extraction attempted; no
rewrite.

**`tests/table-with-inline-image-rendering.test.js`** — the first
`it()` case ("emits a single row with col-md-6 paddingR alert and
col-md-3 paddingL image") was renamed to "emits a single row with
col-md-6 paddingR and col-md-3 paddingL image (no alert wrapper for
bare tables)" and updated to (a) assert absence of `<div class="alert">`,
and (b) assert that the intro `<p>` + bullet `<ul>` render directly
inside `<div class="col-md-6 col-12 paddingR"><div class="row"><div class="col-12">…`
with no alert div between the paddingR column and the inner row. All
other existing cases are agnostic to the alert wrapper (iStock src
mapping, bullet stripping, `class="img-fluid"`, `loading="lazy"`,
`alt=""`, non-iStock `placehold.co` fallback, bullets-only / image-only
single-column fallthrough) and were left entirely unchanged. The
integration `it()` case that uses an explicit `[alert]` marker in its
fixture (Session F Sub-bug A + B integration) continues to find a
`<div class="alert">` in the output — now the one wrapping the
preceding `[body]` paragraph (Session F's preceding-body wrap), not
the one formerly emitted by the table renderer. Its existing
assertions (the alert text contains "The building and running of AI",
the paired row emits `col-md-6 paddingR`, the iStock URL resolves to
`images/iStock-2206845926.jpg`, trailing body renders as `<p>`)
continue to pass without modification.

**New `it()` case added:**

| File | New `it()` cases |
|------|-------------:|
| `tests/table-with-inline-image-rendering.test.js` | 1 |

Case covered: `bare bullets+image table (no preceding [alert]) does
not emit <div class="alert">` — fixture is the same bullets + `[image]`
TABLE pattern as the neighbouring cases with no `[alert]` marker in
any preceding block; asserts the paired `col-md-6 col-12 paddingR` and
`col-md-3 col-12 paddingL` columns still render AND that the output
contains no `<div class="alert">` anywhere. This is the explicit
regression guard for the hidden auto-alerting rule.

**Cross-check — pre-existing alert-related tests:**

- `tests/alertWithSidebarImage.test.js` (Session E layout-table
  pairing path, gated on `LayoutTableUnwrapper.isLayoutTable() === true`)
  — does NOT call `_renderBulletsAndImageTable`. Confirmed with
  `grep -rn "_renderBulletsAndImageTable"` returning the single call
  site in `html-converter-block-renderer.js:889`. All Session E alert
  + sidebar-image assertions pass unchanged.
- `tests/alert-tag-preceding-body-association.test.js` (Session F
  Sub-bug A, preceding-body wrap) — all eight `it()` cases untouched
  and continue to pass.
- `tests/lmsCompliance.test.js` / `tests/alertNormalization.test.js`
  / other alert-surfacing tests — no regressions.

**Final pass/total:** 656/656 tests passing — the single new
regression-guard `it()` case in
`tests/table-with-inline-image-rendering.test.js` contributed +1; one
existing case renamed and assertion-updated in place; no regressions.

**Invariants locked in by this session:**

- `_renderBulletsAndImageTable` no longer emits a `<div class="alert">`
  wrapper unless the caller passes `{ alertWrap: true }` via the new
  third `options` argument. The default (`alertWrap: false`) emits the
  inner `<div class="row"><div class="col-12">…</div></div>` grid
  directly inside the `col-md-6 col-12 paddingR` column.
- The standalone `[image]`-branch dispatch
  (`html-converter-block-renderer.js:889`) passes `{ alertWrap: false }`
  explicitly, so bare bullets-plus-image TABLE blocks without a
  preceding `[alert]` marker no longer gain a hidden alert element.
- The Session E layout-table pairing call path (via
  `LayoutTableUnwrapper` → sidebar-block rendering) does not reach
  `_renderBulletsAndImageTable` and continues to emit its alert
  wrapper through its own code path — confirmed by the unchanged
  `alertWithSidebarImage.test.js` pass count.
- The separate defect where an authored `[alert]` marker before a
  bullets+image TABLE renders empty (the writer's intent is for the
  alert to wrap the bullets column, paired with the image column on
  its right) is not fixed by this session and remains open for a
  follow-up execute session.


---

### Session H — [alert] marker consumes a following bullets+image table via new sub-branch

**Problem summary:** After Session G gated the hidden alert wrapper
on `_renderBulletsAndImageTable` behind an `alertWrap` caller flag,
bare bullets+image tables no longer emitted a phantom alert, but the
writer-template pattern of `[alert]` marker directly followed by a
bullets+image TABLE still produced a double defect: (1) the `[alert]`
handler's three existing sub-branches all fell through — Session E
layout-table pairing (`isLayoutTable()` returns false because a
bullets-only left cell does not meet the ≥2-structural-tags
threshold), Session F Sub-bug A preceding-body wrap (no adjacent
`[body]` paragraph), and the `_collectAlertContent` fallback (next
block is a table, not an untagged paragraph) — emitting an empty
`<div class="alert"><div class="row"><div class="col-12"></div></div></div>`
inside a `col-md-8 col-12` column; AND (2) the TABLE was then
processed independently by the standalone `[image]`-branch dispatch,
which (post-Session G) emitted the paired layout without an alert
wrapper. The writer saw an empty alert AND an un-alerted
bullets+image pairing instead of a single alert-wrapped paired layout.

**New sub-branch added to the `[alert]` handler of `_renderBlocks`:**
Positioned after the Session E layout-table pairing check and before
the Session F Sub-bug A preceding-body wrap. The new sub-branch
peeks at the next block at index `i + 1`; if it is a table without a
`[table]` tag (matching the same `!this._renderers._hasTableTag(...)`
gate as the standalone `[image]`-branch dispatch) and the
`_detectBulletsAndImageTable` detector returns a non-null descriptor,
it calls `flushPending()`, then
`this._renderers._renderBulletsAndImageTable(descriptor, config, { alertWrap: true })`
and pushes the result to `htmlParts` (or `activityParts` when
`inActivity`). The outer loop counter is advanced by `i += 2`
(consuming both the alert marker and the paired table) and the
handler `continue`s. If the detector returns `null` or the next
block is not a table, the new sub-branch does not fire and control
falls through to the existing Session F Sub-bug A preceding-body
wrap sub-branch unchanged. The Session E layout-table pairing
sub-branch, the Session F Sub-bug A preceding-body wrap sub-branch,
and the `_collectAlertContent` fallback are all entirely untouched.

**File touched:**

| File | Before | After | Change |
|------|-------:|------:|--------|
| `js/html-converter-block-renderer.js` | 1184 | 1211 | +27 lines (new sub-branch, additive only) |
| `tests/table-with-inline-image-rendering.test.js` | 271 | 281 | +10 lines (integration `it()` assertion updated to reflect Session H ordering — the first alert now wraps the table's bullets-column intro rather than the preceding `[body]` paragraph; `<p>` position relative to alert asserted) |

**New test file added:**

| File | New `it()` cases |
|------|-------------:|
| `tests/alert-before-bullets-image-table.test.js` | 8 |

Cases covered:
1. `[alert]` + bullets+image TABLE emits exactly one
   `<div class="alert">` and the alert wraps the bullets column
   (sits inside `col-md-6 col-12 paddingR`, before `col-md-3 col-12 paddingL`).
2. Paired row uses `col-md-6 col-12 paddingR` for the alert/bullets
   column and `col-md-3 col-12 paddingL` for the image column.
3. Intro sentence renders as `<p>…</p>` and bullets as `<ul><li>…</li>…</ul>`,
   both inside the alert's inner `<div class="row"><div class="col-12">…</div></div>`
   scaffolding.
4. iStockPhoto URL containing `-gm<NUMERIC_ID>-` in the image cell
   resolves to `src="images/iStock-<NUMERIC_ID>.jpg"` with `alt=""`.
5. Non-iStockPhoto URL retains the `placehold.co` placeholder (no
   false-positive iStock mapping).
6. Emitted `<img>` carries `class="img-fluid"`, `loading="lazy"`, and
   uses self-closing `/>` style.
7. Regression guard: `[alert]` + bullets+image TABLE produces
   exactly one `<div class="alert">` occurrence (not two), and the
   output does not contain the empty-alert scaffolding pattern
   `<div class="alert">\s*<div class="row">\s*<div class="col-12">\s*</div>`
   (regex shape reused from `alert-tag-preceding-body-association.test.js`).
8. Fall-through guard: `[alert]` followed by a two-column table
   that is NOT bullets+image (plain text in both cells) does NOT
   fire the new sub-branch — the cell text still reaches the
   output via whichever existing handler picks it up, and no
   spurious `col-md-6 col-12 paddingR` + `col-md-3 col-12 paddingL`
   pairing is emitted.

**Cross-check — pre-existing alert-related tests:**

- `tests/alertWithSidebarImage.test.js` — Session E layout-table
  pairing path (gated on `LayoutTableUnwrapper.isLayoutTable() === true`)
  runs before the new Session H sub-branch and takes first claim.
  All six `it()` cases pass unchanged.
- `tests/alert-tag-preceding-body-association.test.js` — no fixture
  in that test file pairs an `[alert]` marker with a bullets+image
  TABLE, so the new sub-branch never fires for those fixtures.
  All eight `it()` cases pass unchanged.
- `tests/table-with-inline-image-rendering.test.js` — nine of ten
  `it()` cases untouched (the bare-table fixtures have no `[alert]`
  marker, so the new sub-branch never fires). The one integration
  `it()` case ("integrates with a [body] + [alert] + TABLE + [body]
  stream from the reference test case") used the exact writer
  pattern that Session H targets; its assertion that "the first
  alert should wrap the first body paragraph" reflected Session F
  Sub-bug A's claim and is obsolete under Session H's new ordering.
  The assertion was updated in place to assert the new (correct)
  semantic: the first alert wraps the TABLE's bullets-column intro
  ("AI is not safe for our environment due to:"), and the preceding
  `[body]` paragraph renders as its own un-alerted row above the
  paired layout. All other assertions in that `it()` case
  (col-md-6 paddingR, iStock URL mapping, trailing body `<p>`)
  pass unchanged.
- `tests/lmsCompliance.test.js` / `tests/alertNormalization.test.js`
  / OSAI201 calibration snapshot — no regressions.

**Final pass/total:** 664/664 tests passing — 8 new `it()` cases
contributed by `tests/alert-before-bullets-image-table.test.js`; one
existing integration-case assertion updated in place in
`tests/table-with-inline-image-rendering.test.js` to reflect the
Session H ordering; no regressions.

**Invariants locked in by this session:**

- The `[alert]` handler now recognises a following bullets+image
  TABLE via the existing `_detectBulletsAndImageTable` detector as
  a new sub-branch that runs after the Session E layout-table
  pairing check (gated on `isLayoutTable()`) and before the
  Session F Sub-bug A preceding-body wrap. When the detector
  matches, the `[alert]` handler consumes both blocks and emits a
  single alert-wrapped paired layout via
  `_renderBulletsAndImageTable(descriptor, config, { alertWrap: true })`
  — eliminating the empty-alert + separate-un-alerted-pairing
  double-render. When the detector returns `null` or the next
  block is not a table, the new sub-branch does not fire and
  control falls through to the existing Session F Sub-bug A
  preceding-body wrap sub-branch unchanged.
- Sub-branch ordering in the `[alert]` handler (top-to-bottom):
  Session E layout-table pairing (`_unwrappedFrom === 'layout_table'`
  consumption + sidebar pairing) → Session H bullets+image TABLE
  pairing (this session) → Session F Sub-bug A preceding-body
  wrap → `_collectAlertContent` fallback. Each sub-branch performs
  its own `flushPending()` on match; no pre-branch flush is
  reintroduced.
- The `[alert]` + bullets+image TABLE pairing always emits the
  `{ alertWrap: true }` variant from `_renderBulletsAndImageTable`
  (the writer's authored `[alert]` intent), while the bare TABLE
  dispatch at `html-converter-block-renderer.js:889` continues to
  pass `{ alertWrap: false }` — the two call sites remain the
  only callers of `_renderBulletsAndImageTable` and they disagree
  only on the wrapper flag.

**File-size status (non-blocking):**
`js/html-converter-block-renderer.js` grew 1184 → 1211 lines with
this change and remains above the 700-line core threshold
(previously flagged in docs/29 remediation backlog). The Session H
edit is purely additive (new sub-branch, ~27 lines); no extraction
is attempted here. Follow-up split is tracked in the docs/29 backlog.


---

[← Back to index](../CLAUDE.md)
