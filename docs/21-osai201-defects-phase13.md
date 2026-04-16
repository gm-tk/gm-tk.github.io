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


---

[← Back to index](../CLAUDE.md)
