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

All files are dropped into **one upload container**; PageForge auto-classifies them. To tell the **base** from a **section**, the classifier **strips every `PAGEFORGE-GUIDE-START … PAGEFORGE-GUIDE-END` block first** (exactly as the stitch core does before locating markers, §3c/§4), then treats a file as the base only if the cleaned text carries a **real** splice marker — `<!-- PAGEFORGE-SPLICE id="…" -->` — or the file is named `<CODE>-base.html`; every other file is a **section** (so the `-base` / `-lesson-NN` suffixes are a human-readable aid, not required for detection).

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
