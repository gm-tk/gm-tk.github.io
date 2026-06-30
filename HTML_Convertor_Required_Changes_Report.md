# HTML Convertor Claude Project — Required Changes Report

**Source of changes:** PageForge V1.5 (the client-side web app).
**Target of changes:** the downstream **HTML Convertor** Claude Project (`00-Other-TK-Resources/HTML Convertor Claude Files`).
**Prepared:** 2026-06-30.

---

## 0. Scope and intent — read first

This is a **requirements and behaviour specification**. It describes, comprehensively, the two new capabilities the HTML Convertor must gain so it remains compatible with the current PageForge V1.5 web app, and exactly how the new SPLIT MODE output must be shaped so PageForge's **Page Stitcher** can recombine it.

What this report **deliberately does not do**, by request:

- It does **not** tell you which project file or section to change, and it does **not** contain the edited file text. It specifies *what the behaviour must become* and *why*; deciding where each requirement lands in the project's files (and writing those edits) is a separate, later step.
- **No HTML Convertor file has been modified.** Nothing here has been applied.

One authority note: the SPLIT MODE marker/keyword contract in §3 is the exact shape PageForge's Page Stitcher (`js/page-stitcher.js`) enforces at the other end. Those tokens and that structure are **not** stylistic suggestions — if they are not reproduced exactly, the stitch will fail or silently misplace content.

---

## 1. Background — what changed in PageForge, and why it reaches downstream

Two PageForge V1.5 capabilities create downstream obligations:

**(a) Native Word-comment capture.** PageForge now reads the writer `.docx`'s native Word margin comments (`word/comments.xml`), keeps only the **actionable** ones authored by the six Creative-Services reviewers, and re-emits each as a note **inside the parsed `.txt`** that the HTML Convertor already consumes. The Convertor therefore now receives a new *kind* of content in its input and must render it correctly in the finished HTML.

**(b) SPLIT MODE / Page Stitcher.** PageForge gained a **Page Stitcher** that recombines a single-page module that was generated in pieces. The *splitting* — emitting those pieces in the precise format the stitcher expects — has to happen **in the HTML Convertor** (the tool that actually generates module HTML). The Convertor does not yet know how to do this, and the trigger/format must be introduced.

**No action is needed for the former "Example Distiller."** It has been removed from PageForge entirely; the reverted (older) HTML Convertor file set already predates it, so there is nothing to add or remove on that account. This report covers only (a) and (b).

---

## 2. Change Area 1 — Render whitelisted reviewer comments as red designer messages

### 2.1 What PageForge now places in the parsed `.txt`

For every Word comment that survives PageForge's whitelist **and** its actionability filter, PageForge inserts a single line into the parsed `.txt`, using the **existing red-text marker the Convertor already understands**, with the comment author prepended:

```
🔴[RED TEXT] Note from {Author}: {the reviewer's comment text, verbatim} [/RED TEXT]🔴
```

Concrete example as it will appear in the `.txt`:

```
🔴[RED TEXT] Note from Kate Scanlon: Please replace this stock image with an iStock photo of a NZ classroom. [/RED TEXT]🔴
```

Essential properties of these notes:

- **Six whitelisted authors only.** A comment is surfaced only if its author resolves to one of: **Kate Scanlon, Nadia Stanton, Caroline Schwer, Simon Vita, Amanda Griffiths, Creative Services**. The printed `{Author}` is always the canonical display name from that list (PageForge normalises Word's inconsistent author strings before matching).
- **Already filtered to the actionable.** PageForge omits pure copyright/permission/attribution boilerplate *unless* it also carries an action signal (an asymmetric rule — e.g. "Replace with iStock. Used with permission." is **kept** because "replace" wins). So by the time a note reaches the Convertor it is something a designer must see or act on — copyright, editorial, or Creative-Services direction.
- **Positioned in context.** Each note is placed **immediately before the element it refers to** in the `.txt`. A comment that was anchored to a Media List row (which is not itself body text) is placed before the body element that uses the **same media item** (matched by URL and, for iStock/YouTube, by the extracted reference id). The Convertor should preserve this "note then the thing it's about" ordering in the HTML.
- **Same marker, fixed new lead.** These notes use the **identical** `🔴[RED TEXT] … [/RED TEXT]🔴` marker the Convertor already treats as a writer→CS instruction. What distinguishes a captured reviewer comment from a writer's own red-font instruction is the fixed **`Note from {Author}: ` lead** — a literal "Note from " followed by one of the six whitelisted display names and a colon.

### 2.2 How this relates to what the Convertor already does

The Convertor already has a **Red Text Handling** rule and a **Comment & Red Flag Policy**: it strips the `🔴[RED TEXT]` marker, ignores whitespace-only blocks, extracts any embedded `[tag]`, and surfaces a *substantive* instruction as a **visible red flag** — `<p style="color: red;">RED FLAG: …</p>` — never as a hidden HTML comment, never as student-facing content. That `<p style="color: red;">` red flag is described in the project as the **sole permitted inline style** and the canonical way to put "anything a designer needs to know or action" in front of the designer.

This means Change Area 1 is an **extension of an existing, well-understood rule**, not a new mechanism. A reviewer comment is a substantive, tagless red-text block, so under the current rule it would already tend to surface as a red flag. The required change is to make that **reliable, attributed, and intentional** for this new category — and to make sure the Convertor never mistakes one for something it can drop, bury, or rewrite.

### 2.3 Required behaviour

The Convertor must, for every `🔴[RED TEXT] Note from {Author}: … [/RED TEXT]🔴` note whose `{Author}` is one of the six whitelisted reviewers:

1. **Render it as a red designer message in the finished HTML — the same red style as every other important message to the designer** (i.e. the established `<p style="color: red;">…</p>` form). This is the explicit ask: copyright, editor, and Creative-Services comments get the same red treatment as RED FLAG notes.
2. **Preserve the attribution and the comment text verbatim.** The designer needs to know *who* raised it (copyright vs editor vs Creative-Services context) and read the exact wording. Do not paraphrase, summarise, truncate, or drop the author name. (Content-fidelity is already a hard rule of the project; it applies here too — the comment text is not student content, but it is still passed through unchanged.)
3. **Keep it in position** — render the red message immediately **before** the element the note refers to, mirroring where PageForge placed it in the `.txt`.
4. **Treat it as designer-facing, never student-facing**, and **never** relocate it into an HTML comment. (This fits the project's existing "comments are not a communication channel" philosophy — these belong in visible red, not `<!-- … -->`.)
5. **Do not attempt to parse a `[tag]` out of a prose comment.** These notes are sentences, not tag carriers. The existing "tag-only → extract the tag" branch must not swallow or mangle an author-prefixed comment.
6. **Preserve the `Note from {author}:` lead verbatim — do not genericise it.** The Convertor's current red-text examples re-label a CS instruction as `RED FLAG: …` (and sometimes reword it, e.g. "CS instruction — …"). For these captured reviewer comments that is wrong: render the note's text **exactly as supplied**, keeping the literal `Note from {author}: ` prefix, inside the red paragraph — e.g. `<p style="color: red;">Note from Creative Services: Designer, use the Google Chrome logo that is listed in the Media List.</p>`. The `Note from {author}:` lead is BOTH the recognition signal (it marks a captured reviewer comment, distinct from a writer's own red-font CS instruction) AND the required output form — it must never be dropped, reworded, or replaced with a generic `RED FLAG:` label.

### 2.4 Edge cases the spec must address

- **Whitespace-only red-text blocks** continue to be disregarded (unchanged behaviour). A reviewer note always has author + text, so this never drops a real comment.
- **A note that mixes a copyright/permission phrase with an action** (e.g. "…used with permission, but please crop to 4:3") has already passed PageForge's filter and **must be shown** — do not re-suppress it as boilerplate downstream.
- **Multiple notes before one element** (several reviewer comments on the same item) must each surface, in order, before that element.
- **Media-anchored notes**: the note already arrives positioned before the body element that uses the same media; the Convertor renders it there. It must not require the media item to be "in the body text" to show the note.
- **A reviewer comment that references an interactive** must still never disclose an interactive's correct answer in a way that reaches a hidden comment — but since these are rendered as *visible* red messages, the existing answer-secrecy rule is satisfied (the secrecy rule is specifically about hidden HTML comments).

### 2.5 Acceptance criteria for Change Area 1

- A parsed `.txt` containing `🔴[RED TEXT] Note from {whitelisted author}: {text} [/RED TEXT]🔴` produces, in the finished HTML, a **visible red** message reading `Note from {author}: {text}` **verbatim** (not re-labelled `RED FLAG:`, not reworded), positioned before the referenced element.
- No such note is ever emitted as a hidden HTML comment, rendered as student content, or dropped.
- Writer red-font CS instructions (no author prefix) continue to behave exactly as before.
- Whitespace-only and tag-only red-text blocks behave exactly as before.

---

## 3. Change Area 2 — SPLIT MODE (generate a single-page module in stitchable pieces)

### 3.1 The problem SPLIT MODE solves

Most modules are built as **one single-page HTML file**: the whole module lives in one `#body`, and each lesson is delimited by its own `<!-- 1 -->`, `<!-- 2 -->` … HTML comment (e.g. `BLL210.html`). When such a module is **very long**, generating the entire page in a single pass can exceed one response and the conversion **truncates or aborts**.

**SPLIT MODE** lets the Convertor emit that long single-page module **in pieces** — a small **base homepage** plus **one section file per lesson** — so each generation stays within limits. PageForge's **Page Stitcher** then recombines the pieces into **one single-page file that is byte-identical to a normally-built single-page module**. The split is a *generation-time convenience only*; it must leave **no trace** in the final stitched output.

> SPLIT MODE is **not** the Convertor's existing multi-page **Page Boundary System** (`[LESSON]` / `[End page]` → `-00.html`, `-01.html`, …), which produces genuinely separate lesson *pages*. SPLIT MODE targets modules that are meant to be **one page** but are too long to emit at once. These two systems must never be conflated.

### 3.2 Proactive single-page identification + suggesting SPLIT MODE

The Convertor already determines page structure during triage/extraction (it detects `[LESSON]` / `[End page]` boundaries to drive the multi-page system). The required new behaviour:

- When the Convertor determines a module is **single-page** — i.e. it has **no** `[LESSON]` / `[End page]` page boundaries, or it is a module type that ships as one page — it should **say so** and **proactively offer SPLIT MODE** as an option the user may invoke, explaining in one line what it does (emit the page in stitchable pieces that PageForge's Page Stitcher recombines into one file).
- The offer should be **especially prominent when the single-page output is large** (many lessons / heavy interactive content) and therefore at real risk of exceeding one response.
- The suggestion is an **offer, not an automatic action.** SPLIT MODE only runs when the user explicitly invokes it (see §3.3). If the user does nothing, the Convertor continues to produce the normal single-page file.

The intent: a user who asks for a single-page module is told, up front, "this is a single-page module; if it's too long to build in one go, you can run SPLIT MODE and stitch it back together in PageForge."

### 3.3 Trigger and triage

- **Trigger phrase:** `SPLIT MODE` — an explicit, user-invoked mode, in the same family as the project's existing `COMPARISON MODE` and `UPDATE MODE` (a precedence trigger).
- **Applicability:** only for a **single-page** module whose full output is too long to emit in one pass. If the module is genuinely multi-page (`[LESSON]` / `[End page]`), the normal Page Boundary System is used instead — **do not** split.
- **All other conversion rules are unchanged** while in SPLIT MODE: never modify writer text, never invent structure, never render `[tags]` as visible text, raise visible red flags for ambiguities, omit `stickyNav` (it is a templating error), prompt for image mode, render the reviewer comments of §2, etc. SPLIT MODE changes only **how the output is packaged**, not what it contains.

### 3.4 SPLIT MODE output #1 — the base homepage (`<CODE>-base.html`)

The base is the **complete single-page scaffold**, exactly as a normal single-page module, **except** that `#body` contains **only an ordered list of splice markers — one per lesson/section — and no lesson content**:

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

Rules for the base:

- The **header, menu, footer, and acknowledgements are fully built** in the base. They are short and shared, so they are produced once, here — not split.
- `#body` holds **only** the `PAGEFORGE-SPLICE` markers, **in the exact order the lessons must appear** in the finished page.
- There is **one splice marker per lesson/section** that the module contains.
- **Do not emit `stickyNav`** anywhere in the base.
- All scaffold attributes (`<html template>`, `<body class>`, the `colourlevel` comment, `level`, etc.) are produced exactly as for a normal single-page build — the stitched output inherits them verbatim from the base.

### 3.5 SPLIT MODE output #2 — one section file per slot (`<CODE>-lesson-<id>.html`)

Each section file carries the **raw `#body` content for exactly one slot**, wrapped in section markers. The content between the markers is **exactly what belongs inside `#body`** for that one lesson — **including that lesson's own `<!-- N -->` comment** — at the normal indentation:

```html
<!-- PAGEFORGE-SECTION id="01" -->
<!-- 1 -->
<div class="row"> … lesson 1 content … </div>
<div class="activity"> … </div>
<!-- /PAGEFORGE-SECTION -->
```

Rules for a section file:

- The `id` on the section **must match** a `PAGEFORGE-SPLICE id` in the base.
- Put **only** that slot's `#body` content between the markers — **no** `<html>`, `<head>`, `<body>`, `#header`, or `#footer`.
- Include the lesson's `<!-- N -->` delimiter comment as the first line of the slot content (this is what makes the stitched `#body` identical to a one-pass build).
- One file per slot. Every base slot needs exactly one section file, and every section file must correspond to a base slot.

### 3.6 The id and filename conventions

- **Id values:** use the lesson identity as the id — `intro` for the module-introduction section, then zero-padded lesson numbers `01`, `02`, … matching the `<!-- N -->` lesson comments.
- **Ids are case-insensitive and must be unique** within the module.
- **The marker id is authoritative; the filename is a human-readable convenience.** Name the base `<CODE>-base.html` and each section `<CODE>-lesson-<id>.html` (e.g. `BLL210-lesson-01.html`), but PageForge identifies the base by the presence of `PAGEFORGE-SPLICE` markers and matches sections by their `PAGEFORGE-SECTION id` — so the suffixes are an aid, not a requirement.

### 3.7 Keyword / marker reference (reproduce these EXACTLY)

| Purpose | Exact token | Where it goes |
|---|---|---|
| Base body slot (one per lesson, in order) | `<!-- PAGEFORGE-SPLICE id="X" -->` | Inside `<div id="body">` of `<CODE>-base.html`, nothing else in `#body` |
| Section start | `<!-- PAGEFORGE-SECTION id="X" -->` | First line of each section file |
| Section end | `<!-- /PAGEFORGE-SECTION -->` | Last line of each section file |
| Lesson delimiter (carried inside the section) | `<!-- N -->` (the lesson's own number) | First line of the section's slot content, between the section markers |
| Base filename (aid) | `<CODE>-base.html` | — |
| Section filename (aid) | `<CODE>-lesson-<id>.html` | — |
| Id values | `intro`, then `01`, `02`, … (case-insensitive, unique) | The `id="…"` of each splice/section marker |

The marker spelling, the `id="…"` attribute syntax, the `PAGEFORGE-SPLICE` / `PAGEFORGE-SECTION` / `/PAGEFORGE-SECTION` names, and the one-marker-per-lesson-in-order rule are all load-bearing. Any deviation (different casing, missing closing marker, mismatched id, extra `#body` wrapper in a section) breaks the stitch.

### 3.8 The round-trip guarantee (why the exactness matters)

Stitching the base + all section files must yield a single file whose `#body` is **the section contents concatenated in slot order** — byte-for-byte the same `#body` a one-pass single-page build would have produced (lessons delimited by their `<!-- N -->` comments). **No `PAGEFORGE-*` markers survive** in the stitched output. The header, menu, footer, acknowledgements, and all scaffold attributes come straight from the base, untouched. SPLIT MODE is correct only if this holds; the marker contract exists precisely to make it hold.

### 3.9 How PageForge's Page Stitcher consumes these (so the split is valid)

So the Convertor author understands what must be true for a successful stitch, this is what PageForge does at the other end (single upload container; files auto-classified):

1. It reads the **base** (the file carrying `PAGEFORGE-SPLICE` markers, or named `<CODE>-base.html`) and collects every `<!-- PAGEFORGE-SPLICE id="X" -->` marker **in document order**.
2. For each other (section) file it determines an `id` and `content`, in this precedence: the text between `<!-- PAGEFORGE-SECTION id="X" -->` … `<!-- /PAGEFORGE-SECTION -->` (**authoritative**); else the inner HTML of a `#body` if the file is a full page; else the whole file, with the id taken from the `-lesson-NN` / `-NN` filename.
3. It **validates before emitting anything** (it never produces a broken file): every base slot has exactly one matching section; every section matches a base slot (no orphans/extras); no duplicate ids; at least one slot. Any mismatch is reported and nothing is downloaded.
4. It replaces each splice marker with its section's content, preserving order and leaving the surrounding scaffold untouched.
5. It offers the unified `<CODE>.html` for download, plus a placement summary.

The practical implications for the Convertor's SPLIT MODE output: **ids must line up one-to-one** between base and sections, **every lesson must have both** a base slot and a section file, **no id may repeat**, and **the base must contain at least one slot**. If the Convertor cannot produce a given section, it must still emit that section file with a **visible red flag inside it** rather than omitting the slot (an omitted slot fails validation; a red-flagged slot stitches and tells the designer what is missing).

### 3.10 Validation and failure handling the Convertor must honour when emitting

- Emit exactly one section file per base slot, and one base slot per section — keep them in agreement.
- Never emit an empty slot. If a lesson's content cannot be produced, emit the section file with a visible red flag (`<p style="color: red;">RED FLAG: …</p>`) describing what is missing — visible content always wins over a silent gap.
- Keep ids unique and consistent between the base and the sections.
- Do not place `PAGEFORGE-*` markers anywhere except as specified (no stray markers in section content, none left in any human-facing place).

### 3.11 Hard rules carried over from the converter's constraints

- **Content fidelity** — section content is the writer's converted HTML, unchanged.
- **No `stickyNav`** — never emit the `stickyNav` script (a templating error) in the base or any section.
- **No invented structure** — the base scaffold and the section content are produced by the normal conversion rules; SPLIT MODE only changes *packaging*.
- **Visible content always wins** — a missing section becomes a red flag in that section file, never an empty slot.
- **The reviewer-comment rendering of §2 still applies** inside section content.

### 3.12 Worked mini-example

**Base — `DEMO101-base.html`:**

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

**`DEMO101-lesson-02.html`:** likewise for lesson two (`id="02"`, `<!-- 2 -->`).

**Stitched `#body` (what PageForge produces):**

```html
<div id="body">
    <!-- 1 -->
<div class="row"><p>Lesson one.</p></div>
    <!-- 2 -->
<div class="row"><p>Lesson two.</p></div>
</div>
```

### 3.13 Acceptance criteria for SPLIT MODE

- On a single-page module, the Convertor proactively identifies it as single-page and offers SPLIT MODE (with a one-line explanation), more prominently when the output is large.
- When the user invokes `SPLIT MODE`, the Convertor emits one `<CODE>-base.html` (full scaffold; `#body` = ordered `PAGEFORGE-SPLICE` markers only; no `stickyNav`) and one `<CODE>-lesson-<id>.html` per slot (section-marker-wrapped raw `#body` content including the `<!-- N -->` comment; nothing else).
- Ids line up one-to-one between base and sections; none repeat; there is at least one slot.
- Dropping all emitted files into PageForge's Page Stitcher validates cleanly and produces a `<CODE>.html` whose `#body` equals a one-pass single-page build, with no `PAGEFORGE-*` markers remaining.
- A multi-page module is **not** split — it continues to use the Page Boundary System.

---

## 4. Interaction, naming, and sequencing notes

- **SPLIT MODE sits alongside the existing modes.** It is an explicit, user-invoked, precedence-style mode like the project's Comparison and Update modes; it needs a place in the project's mode triage and mode definitions, and the single-page-detection prompt of §3.2 needs to live wherever the conversion pipeline first establishes page structure.
- **Change Area 1 is an extension of existing rules**, not a new subsystem — it touches the project's Red Text Handling / Comment & Red Flag Policy understanding (so the author-prefixed reviewer notes are recognised, attributed, and rendered red), and the same red rendering applies to section content produced under SPLIT MODE.
- **Keep the two changes independent.** They can be specified and adopted separately; neither depends on the other.

## 5. Out of scope (recap)

- This report does not say which file/section to edit or supply edited text; it specifies required behaviour only.
- No HTML Convertor file has been changed. Applying these requirements (and mapping them to the project's files, mode triage, file map, and change ledger) is a separate, later step to be done deliberately and on request.
