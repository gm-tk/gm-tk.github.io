# SPLIT MODE & Stitch Contract

> **Pairs with:** PageForge V1.5 **Page Stitcher** (`js/page-stitcher.js`).
> **For the downstream converter:** drop this in to the *HTML Convertor* Claude Project as `13_SPLIT_MODE.md` and register it (see §9). Written to match that project's house style.

---

## 1. What problem this solves

Most modules are built as **one single-page HTML file** — the whole module lives in one `#body`, with each lesson delimited by its own `<!-- 1 -->`, `<!-- 2 -->` … comment (e.g. `BLL210.html`). When such a module is **very long**, generating the whole page in one pass can exceed a single response's length and the conversion **aborts or truncates**.

**SPLIT MODE** lets the converter emit a long single-page module **in pieces** — a small **base homepage** plus one **section file per lesson** — so every generation stays within limits. The PageForge **Page Stitcher** then recombines those pieces into **one single-page file that is identical to a normally-built single-page module**. The split is a *generation-time* convenience only; it leaves **no trace** in the final stitched output.

> SPLIT MODE is **not** the multi-file page-boundary system (`[LESSON]`/`[End page]` → `-00.html`, `-01.html` …). That produces genuinely separate lesson *pages*. SPLIT MODE targets modules that are meant to be **one page** but are too long to emit at once.

---

## 2. Trigger & triage

- Trigger phrase: **`SPLIT MODE`** (like `COMPARISON MODE` / `UPDATE MODE`, this is an explicit, user-invoked mode).
- Use it only for a **single-page** module (no `[LESSON]`/`[End page]` page boundaries, or a module type that ships as one page) whose full output is too long to emit in one pass.
- If the module is genuinely multi-page (has `[LESSON]`/`[End page]`), use the normal Page Boundary System instead — **do not** split.

All other conversion rules are unchanged: never modify writer text, never invent structure, never render `[tags]` as text, raise visible red flags for ambiguities, omit `stickyNav` (it is a templating error), prompt for image mode, etc.

---

## 3. What SPLIT MODE emits

Two kinds of files, all for the **same module code `<CODE>`**:

### 3a. The base homepage — `<CODE>-base.html`

The **complete single-page scaffold**, exactly as a normal single-page module, **except** that `#body` contains **only an ordered list of splice markers — one per lesson/section — and no lesson content**:

```html
<!DOCTYPE html>
<html lang="en" template="<phase>" class="notranslate" translate="no">
<head>
    <meta charset="utf-8">
    <meta content="IE=edge" http-equiv="X-UA-Compatible">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <title><CODE></title>
    <script type="text/javascript" src="https://tekura.desire2learn.com/shared/refresh_template/js/idoc_scripts.js"></script>
</head>
<body class="<body-class>">
    <div id="header"> … module-code, title h1(s), menu button, full #module-menu-content … </div>
    <!-- colourlevel="<phase>" -->
    <div id="body">
        <!-- PAGEFORGE-SPLICE id="intro" -->
        <!-- PAGEFORGE-SPLICE id="01" -->
        <!-- PAGEFORGE-SPLICE id="02" -->
        <!-- PAGEFORGE-SPLICE id="03" -->
    </div>
    <div id="footer"> … footer nav … </div>
    <div class="row"><div class="col-md-8 col-12"><div class="acks"> … Acknowledgements … </div></div></div>
</body>
</html>
```

- The header, menu, footer and acknowledgements are **fully built** in the base (they are short and shared).
- `#body` holds **only** the `PAGEFORGE-SPLICE` markers, **in the order the lessons must appear**.
- **Do not** emit `stickyNav` anywhere.

### 3b. One section file per slot — `<CODE>-lesson-<id>.html`

Each file carries the **raw `#body` content for exactly one slot**, wrapped in section markers. The content is **exactly what belongs inside `#body`** for that lesson — including the lesson's own `<!-- N -->` comment — at the normal indentation:

```html
<!-- PAGEFORGE-SECTION id="01" -->
<!-- 1 -->
<div class="row"> … lesson 1 content … </div>
<div class="activity"> … </div>
<!-- /PAGEFORGE-SECTION -->
```

- `id` on the section **must match** a `PAGEFORGE-SPLICE id` in the base.
- Put **only** that slot's body content between the markers — no `<html>`, `<head>`, `<body>`, `#header`, or `#footer`.
- The filename (`-lesson-01`) is a convenience; the **`PAGEFORGE-SECTION id` marker is authoritative**.

### Id convention

Use the lesson identity as the id: `intro` for the module-introduction section, then zero-padded lesson numbers `01`, `02`, … matching the `<!-- N -->` lesson comments. Ids are case-insensitive and must be unique within the module.

### Manual-stitch GUIDE blocks (optional; stripped on stitch)

The converter may add highly detailed, human-readable **manual-stitch guidance** to the base and/or section files for developers who assemble by hand. All such guidance MUST be wrapped in a delimited block:

```html
<!-- PAGEFORGE-GUIDE-START -->
<!-- …instructions: which splice point this fills, the order, where the insertable content begins/ends… -->
<!-- PAGEFORGE-GUIDE-END -->
```

The Page Stitcher **strips every `PAGEFORGE-GUIDE-START … PAGEFORGE-GUIDE-END` block** during stitching (the base is cleaned before markers are located, and the assembled output again), so the unified file carries none of these instructions. The block is removed as a whole, so its text may safely quote markers (including `-->`) — and because guides are stripped **before base/section classification** as well as before stitching (§5), a section file whose guidance quotes a `PAGEFORGE-SPLICE` marker is still correctly classed as a section, never mistaken for a base.

---

## 4. The round-trip guarantee

Stitching the base + all section files yields a single file whose `#body` is **the section contents concatenated in slot order** — byte-for-byte the same `#body` a one-pass single-page build would have produced (lessons delimited by their `<!-- N -->` comments). **No `PAGEFORGE-*` markers survive** in the stitched output — including the manual-stitch GUIDE blocks (§3c), which are stripped entirely. The header, menu, footer, acks and all scaffold attributes (`<html template>`, `<body class>`, `level`, etc.) come straight from the base, untouched.

---

## 5. How the Page Stitcher reassembles (PageForge V1.5)

`js/page-stitcher.js` (Page Stitcher mode):

All files are dropped into **one upload container** (accumulating across several drops, with a
removable per-file list — §10a-bis); PageForge auto-classifies them. To tell the **base** from a **section**, the classifier **strips every `PAGEFORGE-GUIDE-START … PAGEFORGE-GUIDE-END` block first** (exactly as the stitch core does before locating markers, §3c/§4), then treats a file as the base only if the cleaned text carries a **real** splice marker — `<!-- PAGEFORGE-SPLICE id="…" -->` — or the file is named `<CODE>-base.html`; every other file is a **section** (so the `-base` / `-lesson-NN` suffixes are a human-readable aid, not required for detection).

> **Strip guides _before_ the base test — this is essential, not optional.** Every section file carries manual-stitch GUIDE blocks that *quote* the splice marker verbatim in their human instructions (e.g. “paste it in place of the matching `<!-- PAGEFORGE-SPLICE id="01" -->` marker”). The guides quote the **complete** marker, so a stricter marker pattern alone is not enough — a classifier that matches before stripping guides would flag every section as a base and abort with a spurious *“more than one base homepage”* error. Strip the GUIDE blocks first, **then** match a real marker.

1. Read the base homepage; collect every `<!-- PAGEFORGE-SPLICE id="X" -->` marker **in document order**.
2. For each uploaded section file, determine its `id` and `content`:
   1. between its `<!-- PAGEFORGE-SECTION id="X" -->` … `<!-- /PAGEFORGE-SECTION -->` markers (**authoritative**); else
   2. the inner HTML of a `#body` if the file is a full page; else
   3. the whole file, with the id taken from the `-lesson-NN` / `-NN` filename.
3. **Validate before emitting** (never produce a broken file):
   - every base slot has exactly one matching section,
   - every uploaded section matches a base slot (no orphans/extras),
   - no duplicate slot ids, at least one slot.
   Any mismatch is reported (toast + on-screen summary); nothing is downloaded.
4. Replace each splice marker with its section's content, preserving order and leaving the surrounding scaffold untouched.
5. Offer the unified `<CODE>.html` for download, plus a placement summary.

---

## 6. Worked mini-example

**Base (`DEMO101-base.html`):**

```html
<div id="body">
    <!-- PAGEFORGE-SPLICE id="01" -->
    <!-- PAGEFORGE-SPLICE id="02" -->
</div>
```

**`DEMO101-lesson-01.html`:**

```html
<!-- PAGEFORGE-SECTION id="01" -->
<!-- 1 -->
<div class="row"><p>Lesson one.</p></div>
<!-- /PAGEFORGE-SECTION -->
```

**`DEMO101-lesson-02.html`:** likewise for lesson two.

**Stitched `#body`:**

```html
<div id="body">
    <!-- 1 -->
<div class="row"><p>Lesson one.</p></div>
    <!-- 2 -->
<div class="row"><p>Lesson two.</p></div>
</div>
```

---

## 7. Hard rules (carried from the converter's constraints)

- **Content fidelity** — section content is the writer's converted HTML, unchanged; the stitcher never edits it.
- **No `stickyNav`** — never emit the `stickyNav` script (templating error) in the base or any section.
- **No invented structure** — the base scaffold and section content are produced by the normal conversion rules; SPLIT MODE only changes *how the output is packaged*, not what it contains.
- **Visible content always wins** — if a section can't be produced, raise a visible red flag in that section file rather than emitting an empty slot.

---

## 8. Failure handling

- A slot with no section, an extra section with no slot, a duplicate id, or a base with no markers → the Page Stitcher reports the exact problem and **does not** emit a file.
- A section file that is a full page (has `#body`) is still accepted — its `#body` inner is used — so previously hand-split lesson pages can also be combined.

---

## 9. Integrating this into the HTML Convertor project (downstream)

Add this file as `13_SPLIT_MODE.md` and, via that project's **UPDATE MODE**, register it:

- `_project_instructions_.md` → **MODE TRIAGE**: add `SPLIT MODE` phrase → Split Mode (precedence trigger, like Comparison/Update).
- `_project_instructions_.md` → **FILE MAP**: add the `13_SPLIT_MODE.md` line.
- `00_MASTER_INSTRUCTIONS.md` → mode definitions + the "when to load which file" map.

(Those edits are the downstream project's to make through its own Update Mode + change ledger — they are out of scope for the PageForge build, which owns the Page Stitcher side of the contract.)

---

## 10. INTERACTIVE INSERTION — the Page Stitcher's second job (2026-07-28)

The same Stitch button also recombines the OTHER split: module pages generated by the **HTML
Generator (V2 converter)** in EXTRACT mode + the built interactives from the **Interactives
Claude project** (`CLAUDE_PROJECT__Interactives/` at the corpus root holds that project's
instructions + knowledge). Which job runs is **auto-detected from the uploaded files** — no
toggle.

### 10a. The two anchors (the search-by-code contract)

- **Page marker** (ROUND 235: the hand-off is now the converter's DEFAULT for every run —
  the former "Extract un-built interactives" UI switch is gone; template:
  `Emit_Templates.json` → `interactive_placeholder.extract` + `.collapse`):

  ```html
  <div class="cv2-interactive cv2-int-ref" data-cv2-index="7" data-cv2-ref="XDLS908-01-01" style="…">
    <div style="…">XDLS908-INT-01-01-dragAndDrop <span class="cv2-int-toggle" …>▼</span></div>
    <div class="cv2-int-raw" style="…collapsed…"> …the raw captured content (the inline dashed box)… </div>
  </div>
  ```

  The wrapper now ALSO carries `cv2-interactive` (so the module gates keep excluding the whole
  box) and CONTAINS the raw captured content, collapsed by default behind the ▼/▲ toggle. The
  stitcher is unaffected: it matches the element by class token `cv2-int-ref` + `data-cv2-ref`
  and replaces the WHOLE balanced element, so the hidden raw content is swapped out together
  with the marker. The visible label is still the FULL reference code
  (`{code}-INT-{NN}-{seq}-{type}`); the `data-cv2-ref` attribute is the bare id
  (`{code}-{NN}-{seq}`). The same label heads the matching entry in `{CODE}_interactives.txt`
  (`REFERENCE CODE:` line). (The legacy content-less marker form — a bare
  `<div class="cv2-int-ref" …>{label}</div>` — is still produced under
  `INTEXTRACT_ON` + `INTCOLLAPSE_OFF` and still matches this contract.)

- **Built block** (produced by the Interactives Claude project, any number per file):

  ```html
  <section class="cv2-built" data-cv2-ref="XDLS908-INT-01-01-dragAndDrop"> …finished widget HTML… </section>
  ```

  The full code is the standard; the bare id is tolerated. Both forms normalise to the same key
  (`PageStitcher.bareRefId`), so either side matches.

### 10a-bis. The upload container (2026-07-30) — ADDITIVE, LISTED, EDITABLE

The two halves of an interactive-insertion job normally sit in **different folders**: the HTML
Generator downloads its pages as one zip (extracted to one folder) and the Interactives Claude
project downloads the built interactives as another. Assembling that upload therefore takes
**more than one drag-and-drop action**, so the single container is **accumulating**:

- **Every drop / browse ADDS** to the staged set — it never replaces it (`PageStitcherMode.addFiles`).
  Re-adding the **same filename** replaces just that entry in place (newest wins), so a corrected
  file is simply dropped again. `setFiles()` remains the replace-everything call.
- **Every staged file is listed** under the drop zone with a **✕** that removes only that file
  (`removeFile(i)`), plus a *Remove all files* link (`clearFiles()`) — the set is corrected
  **before** Stitch is pressed.
- **`{CODE}_interactives.txt` is silently discarded on arrival** (`PageStitcherMode.isIgnoredUpload`,
  matching `*_interactives.txt`). The HTML Generator ships that worklist in the same zip as the
  pages, so "select all" sweeps it in easily; by stitch time the interactives are already built and
  it has no part to play. It is never staged, never counted, and **never mentioned** — no toast, no
  summary line, nothing in the UI copy. The same filter is applied again inside
  `_partitionUploads()` so a caller handing read files straight to `stitchReadFiles()` gets the
  identical silence. Other `.txt` files are untouched by this rule.

### 10b. Detection

`PageStitcherMode._partitionUploads()`: `.txt` files are set aside (the generated worklist
silently, per §10a-bis; anything else simply unused); a file
holding ≥1 parseable `cv2-built` section is a **built-interactives file**; if any built file is
present OR any page carries a `cv2-int-ref` marker, the upload is **interactive insertion** —
otherwise the original split-mode lesson stitch runs unchanged.

### 10c. Behaviour

- Every marker whose code matches a build is replaced by the section's **inner HTML**; both
  anchors (marker element + section wrapper) disappear from the output.
- Pages with no markers pass through untouched; ALL uploaded pages are re-emitted so the
  developer gets the complete final set. One page → direct download; several → `<CODE>-final.zip`.
- **Head-include injection (All_Interactives alignment, 2026-07-28):** the template library's
  only two script-dependency widgets are `crossword` and `wordFind`. When a placed build carries
  one of those wrapper classes and the page head lacks the include, the stitcher inserts
  `<script type="text/javascript" src="js/crossword.js"></script>` (resp. `wordFind.js`) before
  `</head>` — exactly once, never duplicating an existing include — and reports it in the
  summary (`PageStitcher.INTERACTIVES.headIncludes`).
- **Hard errors (nothing downloads):** a duplicated reference code across the built files; a
  build with no `data-cv2-ref`, empty content, or an unclosed section; no pages uploaded; pages
  without any marker (→ "re-generate with the HTML Generator — its default hand-off emits the
  reference-code boxes"); markers but no built file.
- **Warnings (pages still download):** a marker with no build is LEFT IN PLACE (loud, visible,
  and the output page remains valid input for a later pass with the missing file); a build that
  matched no marker is reported unused.

### 10d. Proof

Headless suites in `tests/page-stitcher.test.js` (core + adapter detection), plus the
end-to-end probe `CONVERTER_V2/outputs/_probe_stitcher_e2e.cjs`: real WT → in-memory extract
conversion → synthetic builds from the real txt codes → the shipped stitcher core. ALL LEGS PASS
on ENFUN05 (1 page / 21 codes) and XDLS908 (9 pages / 65 codes) — every marker replaced, every
build placed exactly once, zero anchors remaining.
