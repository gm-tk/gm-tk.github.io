# 11. HTML Conversion Rules


### Page Boundary Validation (4 Rules — apply BEFORE assigning content to pages)

**Rule 1 — Pre-MODULE-INTRODUCTION End Page → DISREGARD**
`[End page]` between `[TITLE BAR]` and `[MODULE INTRODUCTION]` is a false boundary. Title bar + module introduction combine into single -00 page.

**Rule 2 — Missing End Page Between Lessons → INSERT**
`[LESSON n]` appears without preceding `[End page]` since previous lesson → insert implicit boundary.

**Rule 3 — Empty Lesson Segment → DISREGARD End Page**
Segment has `[LESSON]` but NO body tags AND NO `[Lesson content]` → disregard closing `[End page]`.

**Rule 4 — Orphaned Title Bar → MERGE**
Segment contains ONLY `[TITLE BAR]` + headings + `[End page]`, no body content → merge with following segment.

### Page-to-File Mapping

| Content Segment | Output File |
|---|---|
| `[TITLE BAR]` + overview + `[MODULE INTRODUCTION]` + intro | `MODULE_CODE-00.html` |
| First `[LESSON]` through `[End page]` | `MODULE_CODE-01.html` |
| Second `[LESSON]` through `[End page]` | `MODULE_CODE-02.html` |
| Each subsequent lesson | `-03.html`, `-04.html`, etc. |

### Tag-to-HTML Mapping (Non-Interactive Tags)

| Normalised Tag | HTML Output |
|---|---|
| `title_bar` | `<div id="header">` with module code + title |
| `module_introduction` | Content routing boundary on overview pages (see below) |
| `lesson` + number | New HTML file with lesson header |
| `lesson_overview` | Module menu content for lesson page |
| `lesson_content` | Signals start of body content (no HTML tag) |
| `end_page` | End of current HTML file |
| `heading` level 2 | `<h2>Heading Text</h2>` (no span) |
| `heading` level 3 | `<h3>Heading Text</h3>` |
| `heading` level 4 | `<h4>Heading Text</h4>` |
| `heading` level 5 | `<h5>Heading Text</h5>` |
| `body` | `<p>paragraph text</p>` |
| `alert` | `<div class="alert"><div class="row"><div class="col-12"><p>content</p><p>more content</p></div></div></div>` — consumes ALL following untagged paragraphs |
| `important` | `<div class="alert solid"><div class="row"><div class="col-12"><p>content</p></div></div></div>` — same multi-paragraph rules as alert |
| `whakatauki` | `<div class="whakatauki"><p>Māori text</p><p>English text</p></div>` |
| `quote` | `<p class="quoteText">"Quote"</p><p class="quoteAck">Attribution</p>` |
| `video` | YouTube embed with `youtube-nocookie.com`, `ratio ratio-16x9` wrapper |
| `image` | `<img class="img-fluid" loading="lazy" src="https://placehold.co/600x400?text=..." alt="">` + commented iStock reference |
| `button` | `<a href="URL" target="_blank"><div class="button">Text</div></a>` |
| `external_link` | `<p>preceding text <a href="URL" target="_blank">URL</a>.</p>` — inline visible URL link within paragraph text |
| `activity` + ID | `<div class="row"><div class="col-md-12 col-12"><div class="activity interactive" number="ID"><div class="row"><div class="col-12">` content `</div></div></div></div></div>` |
| `info_trigger` | Inline: `<span class="infoTrigger" info="definition">trigger word</span>` within `<p>` |

### Overview Page Content Routing

On overview pages (`-00`), content is split into TWO zones by the `[MODULE INTRODUCTION]` tag:

**ZONE 1 — Module menu tabs** (content between `[TITLE BAR]` and `[MODULE INTRODUCTION]`):
This content goes into the module menu tab panes, split between Overview and Information tabs:
- **Overview tab**: H1 title + description, first two H2 sections (Learning Intentions + Success Criteria)
- **Information tab**: Third H2 onwards (Planning time, What do I need, Connections, etc.)

**ZONE 2 — Body content** (content after `[MODULE INTRODUCTION]` through `[End page]`):
This content goes into `<div id="body">` as normal body content.

### Lesson Page Content Routing

On lesson pages (`-01`, `-02`, etc.), content is split into TWO zones by the `[LESSON OVERVIEW]` and `[LESSON CONTENT]` tags:

**ZONE 1 — Module menu** (content between `[LESSON OVERVIEW]` and `[LESSON CONTENT]`):
This content is routed into the module menu using the Phase 13 two-tier structure:
- Description paragraph(s) before the first label section are included
- **Section heading `<h5>` comes from template config** (`sectionHeadings.learning`
  and `sectionHeadings.success` — e.g. `Learning Intentions` and
  `How will I know if I've learned it?`)
- **Intro paragraph `<p>` is preserved VERBATIM from the writer's text** (e.g.
  "We are learning:", "I can:", "You will show your understanding by:",
  "Success Criteria") — this reverses the earlier rule of substituting
  config labels for writer text. Config `labels` are used only as a fallback
  when no intro paragraph is detected.
- List items under each section populate the `<ul>` after the intro paragraph
- Italic formatting (`<i>`) is stripped from module menu list items and text
- Emitted per section: `<h5>{sectionHeading}</h5><p>{writer intro}</p><ul>…</ul>`

**ZONE 2 — Body content** (content after `[LESSON CONTENT]` through `[End page]`):
This content goes into `<div id="body">` as normal body content, starting with the lesson heading.

### Title Bar Parsing

The `[TITLE BAR]` content requires three processing steps:
1. **Strip module code prefix** — Remove the alphabetic prefix (e.g., "OSAI") from title text
2. **Split on double-space** — Separate English and Te Reo titles into two `<h1><span>` elements
3. **`<title>` uses English only** — Never include Te Reo title in the `<title>` element

### Module Menu Tab Structure (Overview Pages)

```html
<div id="module-menu-content" class="moduleMenu" tooltip="Overview">
    <div class="row">
        <div class="tabs col-12">
            <ul class="nav nav-tabs">
                <li><a>Overview</a></li>
                <li><a>Information</a></li>
            </ul>
            <div class="tab-content">
                <div class="tab-pane">
                    <div class="row"><div class="col-md-8 col-12">
                        <!-- Overview tab content -->
                    </div></div>
                </div>
                <div class="tab-pane">
                    <div class="row"><div class="col-md-8 col-12">
                        <!-- Information tab content -->
                    </div></div>
                </div>
            </div>
        </div>
    </div>
</div>
```

Key rules:
- No `class="active"`, `data-toggle`, `href`, `id`, `fade`, or `in` attributes on tab elements
- `tooltip="Overview"` goes on `#module-menu-content` only (NOT on `#module-menu-button`) for overview pages
- Each `<div class="tab-pane">` contains inner grid wrapping
- Overview tab headings use `<h4>`; Information tab headings use `<h5>`
- Only the Overview tab's primary title uses `<h4><span>`
- "Success Criteria" heading normalised to "How will I know if I've learned it?"

### Heading Formatting Rules

- **No `<b>` or `<i>` wrapping on headings (h2-h5)** — bold/italic on headings is a .docx artefact
- **Consecutive heading tags produce separate heading elements** — never merge
- **Module menu list items and intro text ("We are learning:", etc.) strip `<i>` wrappers**

### Whakatauki Formatting

Whakatauki content with a `|` pipe separator splits into two `<p>` elements:
```html
<div class="whakatauki">
    <p>Māori text</p>
    <p>English translation</p>
</div>
```

### Formatting Markers to HTML

| Marker | HTML |
|--------|------|
| `**text**` | `<b>text</b>` |
| `*text*` | `<i>text</i>` |
| `***text***` | `<b><i>text</i></b>` |
| `__text__` | `<u>text</u>` |

### Grid Structure Rules

- ALL content inside `<div id="body">` must be inside Bootstrap grid: `<div class="row"><div class="col-md-8 col-12">content</div></div>`
- `col-md-8 col-12` is the DEFAULT for direct children of `.row`
- Wide interactives (D&D column) use `col-md-12 col-12`
- D&D column with many images uses `col-md-10 col-12`
- ALL carousel types use `col-md-8 col-12` for viewer column
- **Content grouping** — consecutive body content (headings, paragraphs, lists, images, videos, quotes, links, buttons, whakatauki, rhetorical questions) that share the same column class are grouped in a SINGLE row wrapper. New rows are created only when:
  - The column class changes (e.g., for a wide interactive)
  - A structural boundary occurs (activity wrapper, interactive component, alert, grid table)
  - An element has its own row structure (untagged tables rendered as grid)

### Content Preservation Rules

1. NEVER modify writer text — trust PageForge output as-is
2. Preserve macronised characters: ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō, Ū
3. Preserve bold/italic from within table cells
4. NEVER render square-bracket tags as visible text
5. NEVER add inline CSS, JavaScript, or invented class names

---


---

[← Back to index](../CLAUDE.md)
