# CLAUDE.md — ParseMaster Project Reference

> **Project:** ParseMaster — Te Kura Writer Template Parser & HTML Converter
> **Repository:** gm-tk.github.io (GitHub Pages)
> **Runtime:** 100% client-side browser application (no server, no backend)
> **Stack:** Vanilla JavaScript, HTML5, CSS3, JSZip (CDN)

---

## TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [Current Architecture](#2-current-architecture)
3. [File Structure](#3-file-structure)
4. [How the Parser Works](#4-how-the-parser-works)
5. [How the Formatter Works](#5-how-the-formatter-works)
6. [How the UI Works](#6-how-the-ui-works)
7. [Current Output Format](#7-current-output-format)
8. [The Downstream Pipeline](#8-the-downstream-pipeline)
9. [Template System Knowledge](#9-template-system-knowledge)
10. [Tag Taxonomy & Normalisation](#10-tag-taxonomy--normalisation)
11. [HTML Conversion Rules](#11-html-conversion-rules)
12. [Interactive Components](#12-interactive-components)
13. [Future Architecture — HTML Conversion Engine](#13-future-architecture--html-conversion-engine)
14. [Template Configuration System](#14-template-configuration-system)
15. [Development Guidelines](#15-development-guidelines)

---

## 1. PROJECT OVERVIEW

### What ParseMaster Does Today

ParseMaster is a client-side web application that reads Te Kura Writer Template `.docx` files and converts them into clean, structured plain text files. These text files are then manually fed into a Claude AI Project for conversion into finalized HTML pages for the D2L/Brightspace LMS.

### What ParseMaster Will Do (Planned)

ParseMaster will be extended to handle the full conversion pipeline:

1. **Parse** `.docx` → structured internal representation (DONE)
2. **Convert** structured representation → fully marked-up HTML files (PLANNED)
3. **Output** multiple downloadable HTML files per module (PLANNED)
4. **Output** a supplementary interactive reference document (PLANNED)

The HTML files will contain all content correctly marked up with the correct tags, classes, grid structure, and hierarchy — everything EXCEPT the code for interactive activities. Interactive activities will be left as clearly marked placeholders with all relevant data preserved, so the Claude AI Project can focus exclusively on building the interactive component code.

### What This Means for the Workflow

**Current workflow:**
```
Writer Template .docx → ParseMaster → .txt file → Claude AI Project → HTML files
```

**Future workflow:**
```
Writer Template .docx → ParseMaster → HTML files (with interactive placeholders)
                                     → Interactive Reference Document
                                     ↓
                          Claude AI Project → HTML files (with interactives built)
```

### Privacy Model

All processing happens in the browser. No data is uploaded, transmitted, or stored. This is a technical constraint (static GitHub Pages site), not just a policy. This MUST be maintained in all future development.

---

## 2. CURRENT ARCHITECTURE

### Technology Constraints

- **No build system** — no webpack, no bundler, no npm at runtime
- **No server** — static files served from GitHub Pages
- **No frameworks** — vanilla JS classes, no React/Vue/Angular
- **Single external dependency** — JSZip loaded from CDN
- **Browser APIs only** — DOMParser for XML, FileReader for uploads, Blob for downloads

### Application Flow

```
User drops .docx file
  → App.handleFile() validates file type
  → DocxParser.parse() extracts and processes XML
    → JSZip extracts word/document.xml from .docx ZIP
    → DOMParser parses XML into DOM
    → _walkBody() recursively extracts paragraphs, tables
    → Tracked changes resolved (del removed, ins kept)
    → SDT wrappers unwrapped
    → Content boundaries detected ([TITLE BAR] marker)
    → Metadata extracted from boilerplate
  → OutputFormatter.formatAll() converts to text
    → Metadata block formatted
    → Content formatted with formatting markers
  → App.showResults() displays output
    → User can Copy or Download
```

### Class Responsibilities

| Class | File | Purpose |
|-------|------|---------|
| `DocxParser` | `js/docx-parser.js` | Extracts structured content from .docx XML |
| `OutputFormatter` | `js/formatter.js` | Converts parsed data to plain text output |
| `App` | `js/app.js` | UI controller — upload, display, clipboard, download |

---

## 3. FILE STRUCTURE

```
gm-tk.github.io/
├── index.html              # Single-page application shell
├── css/
│   └── styles.css          # All application styles
├── js/
│   ├── docx-parser.js      # .docx XML parser (core extraction engine)
│   ├── formatter.js         # Plain text output formatter
│   └── app.js              # UI controller
├── README.md               # Project documentation
└── .nojekyll               # Disables Jekyll processing on GitHub Pages
```

### Future File Structure (Planned)

```
gm-tk.github.io/
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── docx-parser.js          # .docx XML extraction (existing, unchanged)
│   ├── formatter.js             # Plain text formatter (existing, may be deprecated)
│   ├── app.js                   # UI controller (extended for new workflow)
│   ├── tag-normaliser.js        # Tag taxonomy & normalisation engine (NEW)
│   ├── page-boundary.js         # Page boundary detection & validation (NEW)
│   ├── html-converter.js        # HTML generation engine (NEW)
│   ├── template-engine.js       # Template skeleton builder (NEW)
│   └── interactive-extractor.js # Interactive data extraction & reference doc (NEW)
├── templates/
│   └── templates.json           # Template configuration (NEW — see Section 14)
├── README.md
└── .nojekyll
```

---

## 4. HOW THE PARSER WORKS

### DocxParser (js/docx-parser.js)

The parser is a hand-rolled XML walker that extracts content from `.docx` files. Standard libraries (mammoth.js, python-docx, etc.) silently drop content inside tracked changes and SDT wrappers, so this custom parser was built specifically to handle Te Kura Writer Template documents.

### Extraction Process

1. **Unzip** — Uses JSZip to extract `word/document.xml` from the `.docx` ZIP archive
2. **Parse relationships** — Reads `word/_rels/document.xml.rels` for hyperlink URLs and image references
3. **Parse numbering** — Reads `word/numbering.xml` for list type definitions (bullet vs ordered)
4. **Parse main document** — Uses DOMParser to parse `word/document.xml` into a DOM tree
5. **Walk body** — Recursively walks `<w:body>` extracting content in document order

### Critical XML Handling Rules

These rules are the foundation of correct extraction and must never be changed:

| XML Element | Action | Reason |
|-------------|--------|--------|
| `<w:del>` | **REMOVE ENTIRELY** — strip tag AND all content including `<w:delText>` | Deleted content must never appear in output |
| `<w:ins>` | **STRIP TAG, KEEP CONTENT** — remove wrapper, retain all `<w:t>` text within | Inserted text is the writer's final intent |
| `<w:sdt>` | **UNWRAP AND TRAVERSE** — descend into `<w:sdtContent>`, process children normally | Google Docs wraps paragraphs in SDT elements |

### Data Structures

The parser produces these key data structures:

#### Content Blocks (this.content array)
```javascript
// Ordered array of content blocks in document order
[
  { type: 'paragraph', data: paragraphObject, index: 0 },
  { type: 'table', data: tableObject },
  { type: 'pageBreak', data: null },
  { type: 'paragraph', data: paragraphObject, index: 1 },
  // ...
]
```

#### Paragraph Object
```javascript
{
  runs: [
    {
      text: "Hello world",
      formatting: {
        bold: false,
        italic: true,
        underline: false,
        strikethrough: false,
        color: "FF0000",      // hex colour (null if auto)
        highlight: null,
        isRed: true            // true if colour matches known red values
      },
      hyperlink: "https://..." // URL if this run is inside a hyperlink (null otherwise)
    }
  ],
  text: "Hello world",        // concatenated text from all runs
  heading: 2,                  // heading level (1-6) or null
  listLevel: 0,                // nesting level (0-based) or null
  listNumId: "1",              // numbering definition ID or null
  listFormat: "bullet",        // "bullet", "decimal", "lowerLetter", etc.
  isListItem: true             // true if this is a list item
}
```

#### Table Object
```javascript
{
  rows: [
    {
      cells: [
        {
          paragraphs: [ /* array of paragraph objects */ ]
        }
      ]
    }
  ]
}
```

### Red Colour Detection

The parser identifies "red text" (writer instructions to CS/developers) using a combination of known hex values and a heuristic:

```javascript
// Known red values used in Writer Templates
const knownReds = [
  'FF0000', 'ED1C24', 'CC0000', 'C00000', 'FF3333',
  'FF1111', 'DD0000', 'EE0000', 'BB0000', 'AA0000',
  'FF2222', 'FF4444', 'E00000', 'D00000', 'B00000'
];

// Heuristic: R > 180 && G < 80 && B < 80
```

### Content Boundary Detection

ParseMaster detects where actual module content begins by searching for the `[TITLE BAR]` tag. Everything before this is boilerplate (submission checklists, LOT tags, guidance text) and is used only for metadata extraction.

### Metadata Extraction

Metadata is extracted from the boilerplate area (before `[TITLE BAR]`):
- **Module Code** — from filename first (regex: `/[A-Z]{4}\d{3}/`), then boilerplate text, then first few content blocks
- **Subject** — from boilerplate text matching `Subject:\s+...`
- **Course** — from boilerplate text matching `Course:\s+...`
- **Writer** — from boilerplate text matching `Key Contact|Writer|Author:\s+...`
- **Date** — from boilerplate text matching `Date\s*(?:submitted)?:\s+\d{1,2}[/-]\d{1,2}[/-]\d{2,4}`

### Stats Tracking

The parser tracks these statistics:
- `totalParagraphs` — number of paragraphs extracted
- `totalTables` — number of tables extracted
- `totalHyperlinks` — number of hyperlink relationships found
- `deletionsRemoved` — number of `<w:del>` elements removed
- `insertionsKept` — number of `<w:ins>` elements unwrapped
- `sdtUnwrapped` — number of `<w:sdt>` elements unwrapped
- `redTextSegments` — number of text runs with red colour detected
- `contentStartParagraph` — index where content starts

---

## 5. HOW THE FORMATTER WORKS

### OutputFormatter (js/formatter.js)

The formatter converts the parser's structured data into the plain text format currently used. In the future architecture, this class will be supplemented (or replaced) by the HTML converter.

### Output Format

- **Metadata block** — `=====` delimited header with module code, subject, course, writer, date
- **Content section** — starts with `--- CONTENT START ---`
- **Paragraphs** — plain text with formatting markers (`**bold**`, `*italic*`, `__underline__`)
- **Red text** — wrapped in `🔴[RED TEXT] content [/RED TEXT]🔴`
- **Hyperlinks** — `text [LINK: URL]` format
- **Lists** — `•` for bullets, `1.` for ordered, 2-space indent per level
- **Tables** — ASCII art with `┌─── TABLE ───` / `└─── END TABLE ───` delimiters, `║` column separator

---

## 6. HOW THE UI WORKS

### App (js/app.js)

The App class manages all user interaction:

- **File upload** — drag-and-drop zone + click-to-browse, validates `.docx` extension
- **Processing** — shows spinner + progress steps during parse
- **Results** — displays metadata panel, stats panel, output textarea, action buttons
- **Actions** — Copy All, Copy Content Only, Download as .txt, Parse Another File
- **Error handling** — specific error messages for known failure modes (missing XML, invalid XML, corrupted file)
- **Accessibility** — screen reader announcements, keyboard navigation, ARIA labels

### Section Visibility

The UI uses CSS `.hidden` class to toggle between three states:
1. `#upload-section` — initial file upload view
2. `#processing-section` — spinner during parse
3. `#results-section` — output display with actions

---

## 7. CURRENT OUTPUT FORMAT

The plain text output follows this structure (see `OSAI201_parsed.txt` for a full example):

```
=====================================
MODULE METADATA
=====================================
Module Code: OSAI201
Subject: Online Safety
Course: AI Digital Citizenship
=====================================

--- CONTENT START ---

🔴[RED TEXT] [TITLE BAR]  [/RED TEXT]🔴OSAI AI Digital Citizenship  Kirirarautanga Matihiko AI

🔴[RED TEXT] [H1]  [/RED TEXT]🔴**Tirohanga Whānui | Overview**

🔴[RED TEXT] [H2]  [/RED TEXT]🔴**Learning Intentions**
...
```

### Key Format Conventions

| Element | Format in Output |
|---------|-----------------|
| Square-bracket tags | Inside red text markers: `🔴[RED TEXT] [TAG] [/RED TEXT]🔴` |
| Bold text | `**text**` |
| Italic text | `*text*` |
| Bold + Italic | `***text***` |
| Underline | `__text__` |
| Hyperlinks | `__link text__ [LINK: URL]` |
| Bullet lists | `• item` with 2-space indent per level |
| Tables | `┌─── TABLE ───` / `└─── END TABLE ───` with `║` separators |
| Cell line breaks | `/` within table cells |
| Red text (writer instructions) | `🔴[RED TEXT] content [/RED TEXT]🔴` |
| Images | `[IMAGE: filename]` inside runs |

---

## 8. THE DOWNSTREAM PIPELINE

### Current Pipeline (Claude AI Project)

After ParseMaster produces the `.txt` file, it is fed into a Claude AI Project that has extensive knowledge files defining how to convert the text into HTML. The key knowledge files are:

#### 00_MASTER_INSTRUCTIONS.md
- Defines the role, core philosophy, input requirements
- Outlines the 7-phase conversion pipeline
- Lists all 44 constraints
- References all other knowledge files

#### 01_PIPELINE_EXTRACTION_TAGS.md
Contains 5 sections:
- **Section 01 — Template Levels:** HTML tag patterns, head sections, heading patterns, module menu structures, title patterns, footer patterns per year level
- **Section 02 — ParseMaster Text Format:** File structure, metadata block, format conventions
- **Section 03 — Page Boundaries:** 4 validation rules, page-to-file mapping, lesson numbering
- **Section 04 — Tag Taxonomy:** Complete normalisation table (all writer tag variants → normalised forms)
- **Section 05 — Tag Interpretation:** How each normalised tag maps to HTML output

#### 02_DATA_CONTENT_VERIFICATION.md
Contains 3 sections:
- **Section 06 — Interactive Data Patterns:** 13 data patterns writers use for interactive content
- **Section 07 — Content Rules:** Text preservation, grid structure, merging rules
- **Section 08 — Verification:** Full checklist, red flag protocol, 44 constraints, edge cases

#### 06_TEMPLATE_RECOGNITION.md
- Legacy vs Refresh template detection
- Refresh sub-type identification (Standard, Bilingual, Fundamentals, Inquiry, Combo)
- Structural norms by sub-type
- Known pitfalls in reference files
- Mode B validation checklist

#### Component Files (03, 04, 05 — not uploaded but referenced)
- COMP_00–COMP_14 covering all interactive components
- These define exact HTML structures for each interactive type
- NOT needed for Phase 1 of the HTML converter (interactive placeholders only)

---

## 9. TEMPLATE SYSTEM KNOWLEDGE

### Template Levels (Year Levels)

Module code prefix indicates year level and determines the `template` attribute on the `<html>` tag:

| Code Suffix | Year Level | Template Attribute | Example |
|-------------|-----------|-------------------|---------|
| `101` | Years 1–3 | `template="1-3"` | OSAI101 |
| `201` | Years 4–6 | `template="4-6"` | OSAI201 |
| `301` | Years 7–8 | `template="7-8"` | OSAI301 |
| `401` | Years 9–10 | `template="9-10"` | OSAI401 |
| `501` / NCEA | NCEA | `template="NCEA"` | OSAI501 |

### HTML Tag Patterns

| Level | HTML Tag |
|-------|---------|
| Years 1–3 | `<html lang="en" level="" template="1-3" class="notranslate" translate="no" >` |
| Years 4–6 | `<html lang="en" level="" template="4-6" class="notranslate" translate="no" >` |
| Years 7–8 | `<html lang="en" level="" template="7-8" class="notranslate" translate="no" >` |
| Years 9–10 | `<html lang="en" level="" template="9-10" class="notranslate" translate="no">` |
| NCEA | `<html lang="en" level="" template="NCEA" class="notranslate " translate="no">` |

**Note:** `level=""` is ALWAYS empty. Do not populate it.

### Refresh Template Sub-Types

| Sub-Type | `template=` | `<body>` class | Navigation | Footer class |
|----------|-------------|---------------|------------|-------------|
| Standard | `1-3`/`4-6`/`7-8`/`9-10` | `container-fluid` | None | `footer-nav` |
| Bilingual | `1-3` | `container-fluid reoTranslate` | None | `footer-nav` |
| Fundamentals | `combo` | `fundamentals container-fluid` | `div.phases` | `footer-nav fundamentals-nav` |
| Inquiry | `combo` | `inquiry container-fluid` | `div.crumbs` | `footer-nav inquiry-nav` |
| Combo | `combo` | `container-fluid` | None | `footer-nav` |

### Document Shell (Refresh Baseline)

```html
<!doctype html>
<html lang="en" level="" template="..." class="notranslate" translate="no">
<head>
  <meta charset="utf-8" />
  <meta content="IE=edge" http-equiv="X-UA-Compatible" />
  <meta content="width=device-width, initial-scale=1" name="viewport" />
  <title>MODULE_CODE Module Title</title>
  <script type="text/javascript" src="https://tekura.desire2learn.com/shared/refresh_template/js/idoc_scripts.js"></script>
</head>
<body class="container-fluid">
  <div id="header">
    <div id="module-code"><h1>MODULE_CODE</h1></div>
    <h1><span>English Title </span></h1>
    <!-- Years 9-10/NCEA: add second h1 for Te Reo title -->
    <div id="module-head-buttons">
      <div id="module-menu-button" class="circle-button btn1" tooltip="Overview"></div>
    </div>
    <div id="module-menu-content" class="moduleMenu">
      <!-- Module menu content here -->
    </div>
  </div>
  <div id="body">
    <!-- All content rows here -->
  </div>
  <div id="footer">
    <ul class="footer-nav">
      <li><a href="" id="prev-lesson" target="_self"></a></li>
      <li><a href="" id="next-lesson" target="_self"></a></li>
      <li><a href="" class="home-nav" target="_parent"></a></li>
    </ul>
  </div>
</body>
</html>
```

### Key Structural Rules

1. **DOCTYPE:** Always lowercase `<!doctype html>`
2. **Void elements:** XHTML-style self-closing (`<meta ... />`, `<img ... />`, `<link ... />`)
3. **Grid:** ALL body content inside `<div class="row"><div class="col-md-8 col-12">` (default)
4. **Body headings:** `<h2>`–`<h5>` have NO `<span>` wrappers — spans only inside `<h1>` header titles
5. **Heading formatting:** Never wrap entire headings in italic/bold (usually .docx artefact)
6. **No inline CSS/JS:** Never add custom styles or scripts

### Page Structure

```
Overview page (-00):
  Header: #module-code has full MODULE_CODE
  Module menu: Full tabbed (Overview + Information tabs)
  Title element: MODULE_CODE English Title
  Footer: next-lesson + home-nav only

Lesson page (-01, -02, etc.):
  Header: #module-code has zero-padded lesson number (01, 02, etc.)
  h1 span: MODULE title (not lesson-specific title)
  Module menu: Simplified (no tabs) or Full tabs (if both overview + info content)
  Title element: MODULE_CODE lesson# only
  Footer: prev + next + home (middle pages), prev + home (final page)

Years 9-10/NCEA: DUAL h1 titles (English + Te Reo) on EVERY page
```

### Module Menu Label Patterns (Lesson Pages)

| Template Level | Learning Label | Success Label |
|----------------|---------------|---------------|
| 1-3, 4-6 | `<h5>We are learning:</h5>` | `<h5>You will show your understanding by:</h5>` |
| 7-8 | `<h5>We are learning:</h5>` | `<h5>I can:</h5>` |
| 9-10 | `<h5>We are learning:</h5>` | `<h5>I can:</h5>` |

**Critical:** These labels are ALWAYS normalised to the standard patterns above regardless of what the writer used.

### Footer Navigation

| Page Position | Navigation Links |
|--------------|-----------------|
| Overview (-00) | `next-lesson` + `home-nav` |
| Middle pages | `prev-lesson` + `next-lesson` + `home-nav` |
| Final page | `prev-lesson` + `home-nav` |

Navigation hrefs: `MODULE_CODE-XX.html` (e.g., `OSAI201-00.html`, `OSAI201-01.html`)

---

## 10. TAG TAXONOMY & NORMALISATION

### Normalisation Algorithm

```
1. Strip red text markers: 🔴[RED TEXT] ... [/RED TEXT]🔴 → extract inner content
2. Identify square-bracket tags within extracted content
3. Trim whitespace from both ends of tag content
4. Compare case-insensitively against normalisation table
5. Extract trailing number or letter-number ID (e.g., "1A", "3", "5C")
6. Map to normalised form + extracted sub-identifier
```

### Complete Tag Normalisation Table

#### Page Structure Tags
| Writer Variants (case-insensitive) | Normalised Form |
|---|---|
| `title bar` | `title_bar` |
| `module introduction` | `module_introduction` |
| `lesson`, `lesson N` | `lesson` + number |
| `lesson overview` | `lesson_overview` |
| `lesson content` | `lesson_content` |
| `end page` | `end_page` |

#### Heading & Body Tags
| Writer Variants | Normalised |
|---|---|
| `h1`–`h5` | `heading` + level |
| `body`, `body text` | `body` |

#### Content Styling Tags
| Writer Variants | Normalised |
|---|---|
| `alert` | `alert` |
| `important` | `important` |
| `alert-wananga`, `alert wananga` | `alert_cultural_wananga` |
| `alert-talanoa`, `alert talanoa` | `alert_cultural_talanoa` |
| `alert-combined`, `alert combined` | `alert_cultural_combined` |
| `whakatauki` | `whakatauki` |
| `quote` | `quote` |
| `rhetorical question` | `rhetorical_question` |
| `full page translate`, `reo translate` | `reo_translate` |

#### Media Tags
| Writer Variants | Normalised |
|---|---|
| `image`, `image N` | `image` |
| `video` | `video` |
| `audio` | `audio` |
| `audio image`, `audioimage`, `audioImage` | `audio_image` |
| `image zoom` | `image_zoom` |
| `image label` | `image_label` |

#### Activity Tags
| Writer Variants | Normalised |
|---|---|
| `activity NA`, `activity` | `activity` + ID |
| `activity heading`, `activity title`, `heading` (in activity context) | `activity_heading` |
| `end activity`, `end of activity` | `end_activity` |

#### Link/Button Tags
| Writer Variants | Normalised |
|---|---|
| `button` | `button` |
| `external link button` | `external_link_button` |
| `external link` | `external_link` |
| `engagement quiz button` | `engagement_quiz_button` |
| `supervisor button` | `supervisor_button` |
| `modal button` | `modal_button` |
| `audio button` | `audio_button` |

#### Interactive Component Tags
| Writer Variants | Normalised |
|---|---|
| `drag and drop` + variants | `drag_and_drop` |
| `dropdown`, `drop down`, `dropdown N` | `dropdown` |
| `dropdown quiz paragraph`, `dropquiz` | `dropdown_quiz_paragraph` |
| `flip cards`, `flip card`, `flip card N` | `flip_card` |
| `accordion`, `accordion N` | `accordion` |
| `end accordions` | `end_accordions` |
| `click drop`, `clickdrop`, `drop click` | `click_drop` |
| `carousel`, `slide show` | `carousel` |
| `rotating banner` | `rotating_banner` |
| `slide N` | `carousel_slide` |
| `tabs` | `tabs` |
| `tab N` | `tab` |
| `speech bubble` + any suffix | `speech_bubble` |
| `hint slider`, `hint slider N` | `hint_slider` |
| `hint` | `hint` |
| `shape hover` | `shape_hover` |
| `shape N` | `shape` |
| `reorder` | `reorder` |
| `slider chart` | `slider_chart` |
| `slider` | `slider` |
| `memory game` | `memory_game` |
| `word drag` | `word_drag` |
| `typing self-check`, `typing quiz` | `typing_quiz` |
| `self check`, `self-check` | `self_check` |
| `word highlighter`, `word select` | `word_select` |
| `mcq`, `multi choice quiz` | `mcq` |
| `multi choice quiz survey` | `multichoice_quiz_survey` |
| `radio quiz`, `true false` | `radio_quiz` |
| `checklist` | `checklist` |
| `info trigger` + optional text | `info_trigger` |
| `info trigger image` | `info_trigger_image` |
| `info audio trigger`, `audio trigger` | `audio_trigger` |
| `venn diagram` | `venn_diagram` |
| `timeline` | `timeline` |
| `self reflection` | `self_reflection` |
| `reflection slider` | `reflection_slider` |
| `stop watch`, `stopwatch` | `stop_watch` |
| `number line` | `number_line` |
| `crossword` | `crossword` |
| `word find`, `wordfind` | `word_find` |
| `bingo` | `bingo` |
| `clicking order` | `clicking_order` |
| `puzzle` | `puzzle` |
| `sketcher` | `sketcher` |
| `glossary` | `glossary` |
| `embed pdf` | `embed_pdf` |
| `embed padlet` | `embed_padlet` |
| `embed desmos`, `desmos graph` | `embed_desmos` |

### Red Text Handling Rules

Content in `🔴[RED TEXT]...[/RED TEXT]🔴` is writer instruction to CS/developers. NOT student-facing.

1. **Tag-only red text:** `🔴[RED TEXT] [H2] [/RED TEXT]🔴` → extract `[H2]` tag, process normally
2. **Tag + instruction:** `🔴[RED TEXT] [drag and drop column autocheck] They are in correct place [/RED TEXT]🔴` → extract tag, preserve instruction as HTML comment
3. **Pure instruction:** `🔴[RED TEXT] CS: please make images small [/RED TEXT]🔴` → HTML comment only
4. **Whitespace-only:** `🔴[RED TEXT]   [/RED TEXT]🔴` → disregard entirely
5. **NEVER render red text as visible student content**

---

## 11. HTML CONVERSION RULES

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
| `module_introduction` | Module intro content inside `<div id="body">` |
| `lesson` + number | New HTML file with lesson header |
| `lesson_overview` | Module menu content for lesson page |
| `lesson_content` | Signals start of body content (no HTML tag) |
| `end_page` | End of current HTML file |
| `heading` level 2 | `<h2>Heading Text</h2>` (no span) |
| `heading` level 3 | `<h3>Heading Text</h3>` |
| `heading` level 4 | `<h4>Heading Text</h4>` |
| `heading` level 5 | `<h5>Heading Text</h5>` |
| `body` | `<p>paragraph text</p>` |
| `alert` | `<div class="alert"><div class="row"><div class="col-12"><p>content</p></div></div></div>` |
| `important` | `<div class="alert solid"><div class="row"><div class="col-12"><p>content</p></div></div></div>` |
| `whakatauki` | `<div class="whakatauki"><p>Māori text</p><p>English text</p></div>` |
| `quote` | `<p class="quoteText">"Quote"</p><p class="quoteAck">Attribution</p>` |
| `video` | YouTube embed with `youtube-nocookie.com`, `ratio ratio-16x9` wrapper |
| `image` | `<img class="img-fluid" loading="lazy" src="https://placehold.co/600x400?text=..." alt="">` + commented iStock reference |
| `button` | `<a href="URL" target="_blank"><div class="button">Text</div></a>` |
| `external_link` | `<a href="URL" target="_blank">Text</a>` |
| `activity` + ID | `<div class="activity interactive" number="ID">` or `<div class="activity alertPadding" number="ID">` |

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

### Content Preservation Rules

1. NEVER modify writer text — trust ParseMaster output as-is
2. Preserve macronised characters: ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō, Ū
3. Preserve bold/italic from within table cells
4. NEVER render square-bracket tags as visible text
5. NEVER add inline CSS, JavaScript, or invented class names

---

## 12. INTERACTIVE COMPONENTS

### Categories of Interactives

Interactive components are the complex elements that require custom JavaScript/HTML code from the Te Kura component library. In the future architecture, ParseMaster will NOT generate code for these — instead, it will:

1. **Detect** the interactive type from the normalised tag
2. **Extract** all associated data (from tables, lists, red text instructions)
3. **Insert a placeholder** in the HTML output marking where the interactive goes
4. **Generate a reference entry** in the supplementary interactive reference document

### Interactive Data Patterns

Writers provide interactive data in 13 distinct patterns:

| Pattern | Description | Used By |
|---------|-------------|---------|
| 1 | Single data table | D&D, dropdown quiz, reorder, memory game, etc. |
| 2 | Front/back table rows | Flip cards, click drops |
| 3 | Hint/slide table | Hint slider |
| 4 | Numbered items (paragraph) | Dropdown quiz paragraph |
| 5 | Numbered slides | Carousel, rotating banner |
| 6 | Numbered shapes/tabs | Shape hover, tabs |
| 7 | Numbered accordions | Accordion |
| 8 | Speech bubble in table row | Speech bubbles |
| 9 | Conversation layout | Chat demonstrations |
| 10 | Word select table | Word select |
| 11 | Axis labels | Slider chart |
| 12 | Info trigger image | Info trigger image |
| 13 | Self-assessment/survey table | multiChoiceQuiz survey |

### Placeholder Format (Proposed for HTML Output)

```html
<!-- ========== INTERACTIVE PLACEHOLDER ========== -->
<!-- Type: drag_and_drop_column_autocheck -->
<!-- Activity: 2A -->
<!-- Data Source: Table (6 rows × 2 columns) -->
<!-- Writer Instructions: "They are currently in the correct place" -->
<!-- See Interactive Reference Document for full data -->
<div class="activity interactive" number="2A">
  <div class="row">
    <div class="col-md-12 col-12">
      <h3>Activity Heading</h3>
      <p>Activity instructions from writer...</p>
      <p style="color: red;">INTERACTIVE PLACEHOLDER: drag_and_drop_column_autocheck — see interactive reference document</p>
    </div>
  </div>
</div>
<!-- ========== END INTERACTIVE PLACEHOLDER ========== -->
```

### Interactive Reference Document (Proposed Format)

The supplementary reference document will list every interactive needed across all HTML files:

```
=====================================
INTERACTIVE REFERENCE — MODULE_CODE
=====================================

TOTAL INTERACTIVES: 7

-------------------------------------
INTERACTIVE 1 of 7
-------------------------------------
File: OSAI201-01.html
Activity: 2A
Type: drag_and_drop_column_autocheck
Position: After paragraph "Hover over the tiles..."

Writer Instructions:
  "They are currently in the correct place"

Data (Table — 2 columns × 6 rows):
  Column Headers: Category 1 | Category 2
  Row 1: Item A | Item B
  Row 2: Item C | Item D
  ...

Associated Media:
  Image: https://www.istockphoto.com/photo/...

-------------------------------------
INTERACTIVE 2 of 7
-------------------------------------
...
```

---

## 13. FUTURE ARCHITECTURE — HTML CONVERSION ENGINE

### New Modules to Create

#### tag-normaliser.js
- Implements the complete normalisation table from Section 10
- Takes raw tag text, returns normalised form + sub-identifier
- Handles red text extraction (tag-only, tag+instruction, pure instruction)
- Case-insensitive matching with fuzzy tolerance for writer variability

#### page-boundary.js
- Implements all 4 Page Boundary Validation Rules
- Takes the content blocks array, returns page assignments
- Each page knows its type (overview, lesson), content blocks, and output filename
- Handles lesson numbering (explicit, sequential, mixed)

#### html-converter.js
- The main conversion engine
- Takes parsed content + template configuration → produces HTML strings
- Handles:
  - Document skeleton (html tag, head, body structure)
  - Header section (module code, titles, module menu)
  - Body content (paragraphs, headings, lists, tables, alerts, media, etc.)
  - Footer section (navigation links)
  - Formatting conversion (markdown markers → HTML tags)
  - Red text processing (strip, extract tags, preserve as comments)
  - Interactive placeholder insertion
  - Grid wrapping (row/col structure)

#### template-engine.js
- Loads and applies template configurations from `templates.json`
- Selects the correct template based on user dropdown selection
- Applies template-specific rules (different module menu structures, footer classes, etc.)
- Generates the document shell with correct attributes

#### interactive-extractor.js
- Detects interactive component tags in the content stream
- Identifies the data pattern being used
- Extracts all associated data (tables, lists, red text instructions, media references)
- Produces placeholder HTML for the main output
- Produces reference entries for the interactive reference document

### Extended App Flow

```
User drops .docx file
  → User selects template from dropdown
  → DocxParser.parse() extracts content (existing, unchanged)
  → TagNormaliser processes all tags
  → PageBoundary validates and assigns pages
  → For each page:
    → TemplateEngine generates document shell
    → HtmlConverter processes content blocks
    → InteractiveExtractor handles interactive placeholders
  → App offers download of:
    → Individual HTML files (MODULE_CODE-00.html, -01.html, etc.)
    → Interactive Reference Document (.txt or .html)
    → All files as ZIP
```

---

## 14. TEMPLATE CONFIGURATION SYSTEM

### Design Principles

1. **JSON-driven** — all template rules in a single `templates.json` file
2. **Easy to extend** — adding a new template = adding a new JSON object
3. **Easy to tweak** — changing a rule for an existing template = editing a JSON value
4. **Override pattern** — templates inherit from a base configuration and override specific rules
5. **No code changes needed** — template additions/changes should never require JS code changes

### Proposed templates.json Structure

```json
{
  "version": "1.0",
  "baseConfig": {
    "doctype": "<!doctype html>",
    "htmlAttributes": {
      "lang": "en",
      "level": "",
      "class": "notranslate",
      "translate": "no"
    },
    "scriptUrl": "https://tekura.desire2learn.com/shared/refresh_template/js/idoc_scripts.js",
    "bodyClass": "container-fluid",
    "voidElementStyle": "xhtml",
    "defaultColumnClass": "col-md-8 col-12",
    "headingSpanRule": "h1-header-only",
    "footerClass": "footer-nav",
    "moduleMenu": {
      "overviewPage": {
        "type": "full-tabs",
        "tabs": ["Overview", "Information"],
        "tooltipOn": "module-menu-content",
        "headingLevel": "h4",
        "overviewTitleTag": "h4-span"
      },
      "lessonPage": {
        "type": "simplified",
        "tooltipOn": "module-menu-button",
        "headingLevel": "h5"
      }
    },
    "titlePattern": {
      "overviewPage": "{moduleCode} {englishTitle}",
      "lessonPage": "{moduleCode} {lessonNumber}"
    },
    "headerPattern": {
      "overviewPage": {
        "moduleCodeContent": "{moduleCode}",
        "titles": ["english"]
      },
      "lessonPage": {
        "moduleCodeContent": "{lessonNumberZeroPadded}",
        "titleSource": "module",
        "titles": ["english"]
      }
    },
    "imageDefaults": {
      "class": "img-fluid",
      "loading": "lazy",
      "placeholderBase": "https://placehold.co"
    },
    "videoEmbed": {
      "youtube": "youtube-nocookie.com/embed",
      "wrapperClass": "videoSection ratio ratio-16x9"
    },
    "gridRules": {
      "defaultContent": "col-md-8 col-12",
      "wideInteractive": "col-md-12 col-12",
      "wideInteractiveImages": "col-md-10 col-12",
      "carousel": "col-md-8 col-12"
    },
    "interactivePlaceholder": true
  },
  "templates": {
    "1-3": {
      "name": "Years 1–3",
      "templateAttribute": "1-3",
      "inherits": "baseConfig",
      "overrides": {
        "moduleMenu": {
          "lessonPage": {
            "labels": {
              "learning": "We are learning:",
              "success": "You will show your understanding by:"
            }
          }
        }
      }
    },
    "4-6": {
      "name": "Years 4–6",
      "templateAttribute": "4-6",
      "inherits": "baseConfig",
      "overrides": {
        "moduleMenu": {
          "lessonPage": {
            "labels": {
              "learning": "We are learning:",
              "success": "You will show your understanding by:"
            }
          }
        }
      }
    },
    "7-8": {
      "name": "Years 7–8",
      "templateAttribute": "7-8",
      "inherits": "baseConfig",
      "overrides": {
        "moduleMenu": {
          "lessonPage": {
            "labels": {
              "learning": "We are learning:",
              "success": "I can:"
            }
          }
        }
      }
    },
    "9-10": {
      "name": "Years 9–10",
      "templateAttribute": "9-10",
      "inherits": "baseConfig",
      "overrides": {
        "headerPattern": {
          "overviewPage": {
            "titles": ["english", "tereo"]
          },
          "lessonPage": {
            "titles": ["english", "tereo"]
          }
        },
        "moduleMenu": {
          "lessonPage": {
            "labels": {
              "learning": "We are learning:",
              "success": "I can:"
            }
          }
        }
      }
    },
    "NCEA": {
      "name": "NCEA",
      "templateAttribute": "NCEA",
      "inherits": "baseConfig",
      "overrides": {
        "headerPattern": {
          "overviewPage": {
            "titles": ["english", "tereo"]
          },
          "lessonPage": {
            "titles": ["english", "tereo"]
          }
        },
        "moduleMenu": {
          "overviewPage": {
            "tabs": ["Overview", "Information", "Standards"],
            "tooltipOn": null
          },
          "lessonPage": {
            "labels": {
              "learning": "We are learning:",
              "success": "I can:"
            }
          }
        }
      }
    },
    "bilingual": {
      "name": "Bilingual",
      "templateAttribute": "1-3",
      "inherits": "baseConfig",
      "overrides": {
        "bodyClass": "container-fluid reoTranslate",
        "contentDuplication": "eng-reo",
        "headerPattern": {
          "overviewPage": { "titles": ["english", "tereo"] },
          "lessonPage": { "titles": ["english", "tereo"] }
        }
      }
    },
    "fundamentals": {
      "name": "Fundamentals",
      "templateAttribute": "combo",
      "inherits": "baseConfig",
      "overrides": {
        "bodyClass": "fundamentals container-fluid",
        "navigation": "phases",
        "footerClass": "footer-nav fundamentals-nav"
      }
    },
    "inquiry": {
      "name": "Inquiry",
      "templateAttribute": "combo",
      "inherits": "baseConfig",
      "overrides": {
        "bodyClass": "inquiry container-fluid",
        "navigation": "crumbs",
        "footerClass": "footer-nav inquiry-nav"
      }
    },
    "combo": {
      "name": "Combo (Standalone)",
      "templateAttribute": "combo",
      "inherits": "baseConfig"
    }
  }
}
```

### How Template Overrides Work

The template engine resolves configuration by:
1. Loading the `baseConfig` as the default
2. Finding the selected template in `templates`
3. Deep-merging `overrides` on top of `baseConfig`
4. The merged result is the active configuration for that conversion

### Adding a New Template

To add a new template, add a new entry to the `templates` object in `templates.json`:

```json
"new-template-name": {
  "name": "Display Name",
  "templateAttribute": "value-for-html-tag",
  "inherits": "baseConfig",
  "overrides": {
    // Only specify what differs from baseConfig
  }
}
```

### Adding Template-Specific Content Rules

For templates that need specific content interpretation rules, add a `contentRules` object:

```json
"overrides": {
  "contentRules": {
    "stripFullHeadingItalic": true,
    "normaliseModuleMenuLabels": true,
    "moduleMenuItemFormatting": {
      "noItalicWrap": true,
      "lowercaseStart": true,
      "verbFormMatching": true
    }
  }
}
```

---

## 15. DEVELOPMENT GUIDELINES

### Code Style

- **Vanilla JavaScript** — no frameworks, no build system
- **ES6+ class syntax** — `class ClassName { }` with `'use strict';`
- **No arrow functions in class methods** — use `function` for browser compatibility
- **JSDoc comments** — document all public methods with `@param` and `@returns`
- **Descriptive variable names** — `contentBlocks` not `cb`
- **Error handling** — throw named errors, catch in App with user-friendly messages

### Testing Approach

- Test with real Writer Template `.docx` files (like the OSAI201 example)
- Verify tag normalisation against the complete normalisation table
- Verify page boundary detection against the 4 rules
- Verify HTML output structure against the document shell baseline
- Compare generated HTML visually with known-good reference modules

### Key Invariants

1. **Privacy** — No network requests for user data. All processing in-browser.
2. **Content fidelity** — Writer text must pass through unchanged.
3. **Tag completeness** — Every tag must be normalised or flagged.
4. **Structural correctness** — All HTML must follow the grid rules.
5. **Interactive isolation** — Interactive code is NEVER generated; only placeholders.

### Browser Compatibility

Target modern browsers: Chrome, Firefox, Safari, Edge (latest 2 versions). No IE11 support needed. Can use ES6 features (classes, template literals, const/let, destructuring, async/await).
