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

[← Back to index](../CLAUDE.md)
