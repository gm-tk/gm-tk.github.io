# CLAUDE.md — ParseMaster Project Reference

> **Project:** ParseMaster — Writer Template Parser & HTML Converter
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

ParseMaster is a client-side web application that reads Writer Template `.docx` files and converts them into fully marked-up HTML files for the D2L/Brightspace LMS. It also produces clean, structured plain text output (legacy mode). Interactive components are rendered as structured placeholders with all associated data extracted and preserved in a supplementary Interactive Reference Document — the Claude AI Project focuses exclusively on building the interactive component code.

### Current Capabilities

1. **Parse** `.docx` → structured internal representation (DONE — Phase 0)
2. **Tag normalisation** → canonical tag forms with category classification (DONE — Phase 1)
3. **Page boundary detection** → multi-page splitting with validation rules (DONE — Phase 1)
4. **Template configuration** → JSON-driven template system with auto-detection (DONE — Phase 2)
5. **HTML conversion** → fully marked-up HTML for all non-interactive content (DONE — Phase 3)
6. **Interactive placeholders** → structured placeholders with data extraction and tier classification (DONE — Phase 4)
7. **Output** multiple downloadable HTML files per module (DONE — Phase 3)
8. **Output** a supplementary interactive reference document (DONE — Phase 4)
9. **Multi-file output system** → file list panel, individual/bulk download, ZIP export (DONE — Phase 5)

The HTML files will contain all content correctly marked up with the correct tags, classes, grid structure, and hierarchy — everything EXCEPT the code for interactive activities. Interactive activities will be left as clearly marked placeholders with all relevant data preserved, so the Claude AI Project can focus exclusively on building the interactive component code.

### What This Means for the Workflow

**Current workflow:**
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
App startup:
  → TemplateEngine.loadTemplates() loads templates.json (or embedded fallback)
  → Template dropdown populated with 9 template options

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
  → OutputFormatter.formatAll() converts to text (legacy output)
    → Metadata block formatted
    → Content formatted with formatting markers
  → TemplateEngine.detectTemplate() auto-selects template from module code (Phase 2)
    → Dropdown updated, "Auto-detected" label shown
  → TagNormaliser processes all content blocks (Phase 1)
    → Extracts square-bracket tags from red text and plain text
    → Normalises tag variants to canonical forms
    → Classifies tags by category
    → Extracts writer instructions from red text
  → PageBoundary assigns pages (Phase 1)
    → Applies 4 validation rules
    → Splits content into overview + lesson pages
    → Assigns filenames (MODULE_CODE-XX.html)
  → HtmlConverter generates HTML for each page (Phase 3 + Phase 4)
    → TemplateEngine generates document skeleton per page
    → HtmlConverter.convertPage() renders all non-interactive content blocks
    → InteractiveExtractor detects interactive tags, extracts data, classifies tier
    → Interactive components rendered as structured placeholders (green=Tier 1, red=Tier 2)
    → Data blocks consumed by interactives are skipped in body rendering
    → Module menu content populated
    → Complete HTML files assembled with skeleton + body content
  → InteractiveExtractor generates reference document with all extracted data
  → OutputManager stores all generated files (Phase 5)
    → HTML files stored with page type and lesson number metadata
    → Interactive reference document stored as reference type
    → File sizes calculated for display
  → App.showResults() displays output (Phase 5 UI)
    → Metadata panel includes template name, pages generated, interactive count
    → Conversion summary panel shows pages, template, interactives, tags, warnings
    → File list panel shows all generated files with icons, metadata, per-file actions
    → Preview panel shows selected file content with copy/download buttons
    → First HTML file auto-selected for preview on load
    → "Download All as ZIP" creates ZIP archive of all files via JSZip
    → "Copy Interactive Reference" copies reference document to clipboard
    → "Legacy Text Output" switches to plain text view with back navigation
    → "Parse Another File" resets everything cleanly
    → Debug panel shows template config, tag & page analysis, interactive details, skeleton preview
```

### Class Responsibilities

| Class | File | Purpose |
|-------|------|---------|
| `DocxParser` | `js/docx-parser.js` | Extracts structured content from .docx XML |
| `OutputFormatter` | `js/formatter.js` | Converts parsed data to plain text output (legacy) |
| `TagNormaliser` | `js/tag-normaliser.js` | Tag taxonomy, normalisation, and red text processing |
| `PageBoundary` | `js/page-boundary.js` | Page boundary detection, validation, and assignment |
| `TemplateEngine` | `js/template-engine.js` | Template config loading, resolution, auto-detection, skeleton generation |
| `InteractiveExtractor` | `js/interactive-extractor.js` | Interactive component detection, data extraction, placeholder generation, reference document |
| `HtmlConverter` | `js/html-converter.js` | Core HTML conversion engine — transforms content blocks into marked-up HTML |
| `OutputManager` | `js/output-manager.js` | Multi-file output storage, file listing, individual/ZIP download, clipboard copy |
| `App` | `js/app.js` | UI controller — upload, file list, preview, ZIP download, legacy mode, debug panel, template selection |

---

## 3. FILE STRUCTURE

```
gm-tk.github.io/
├── index.html              # Single-page application shell
├── css/
│   └── styles.css          # All application styles (including debug panel, template selector, multi-file layout)
├── js/
│   ├── docx-parser.js      # .docx XML parser (core extraction engine)
│   ├── formatter.js         # Plain text output formatter (legacy)
│   ├── tag-normaliser.js    # Tag taxonomy & normalisation engine (Phase 1)
│   ├── page-boundary.js     # Page boundary detection & validation (Phase 1)
│   ├── template-engine.js   # Template config loading, resolution & skeleton generation (Phase 2)
│   ├── interactive-extractor.js # Interactive data extraction, placeholder generation & reference doc (Phase 4)
│   ├── html-converter.js    # Core HTML conversion engine (Phase 3, updated Phase 4)
│   ├── output-manager.js    # Multi-file output management, ZIP download, clipboard copy (Phase 5)
│   └── app.js              # UI controller (with file list, preview, ZIP download, legacy mode, debug panel)
├── templates/
│   └── templates.json       # Template configuration (Phase 2)
├── CLAUDE.md               # Project reference & instructions
├── README.md               # Project documentation
└── .nojekyll               # Disables Jekyll processing on GitHub Pages
```

---

## 4. HOW THE PARSER WORKS

### DocxParser (js/docx-parser.js)

The parser is a hand-rolled XML walker that extracts content from `.docx` files. Standard libraries (mammoth.js, python-docx, etc.) silently drop content inside tracked changes and SDT wrappers, so this custom parser was built specifically to handle Writer Template documents.

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
- **Template selection** — dropdown populated from TemplateEngine, auto-detects from module code on parse (Phase 2)
- **Processing** — shows spinner + progress steps during parse with pipeline stage counts
- **Results** — displays metadata panel, conversion summary, file list panel, preview panel
- **Multi-file output** — file list with per-file download/copy, preview of selected file (Phase 5)
- **ZIP download** — "Download All as ZIP" creates ZIP archive via JSZip (Phase 5)
- **Legacy mode** — switchable legacy text output with back navigation (Phase 5)
- **Tag & Page Analysis** — after parsing, runs TagNormaliser and PageBoundary on content blocks, displays results in a collapsible debug panel
- **Error handling** — specific error messages for known failure modes (missing XML, invalid XML, corrupted file)
- **Accessibility** — screen reader announcements, keyboard navigation, ARIA labels

### Section Visibility

The UI uses CSS `.hidden` class to toggle between these states:
1. `#upload-section` — initial file upload view
2. `#processing-section` — spinner during parse
3. `#results-section` — multi-panel output display with file list + preview
4. `#legacy-output-panel` — legacy text output (toggleable within results)
5. `#debug-panel` — collapsible tag & page analysis debug panel (appears below results after parse)

### Multi-File Output System (Phase 5)

The results section uses a side-by-side layout with a file list panel (left) and preview panel (right):

- **File List Panel** (`#file-list-panel`) — shows all generated files with icons, filenames, metadata (page type, size), and per-file download/copy action buttons. Clicking a file loads its content in the preview. The selected file gets a `.selected` visual highlight. Files are stored in `OutputManager`.
- **Preview Panel** — shows the content of the currently selected file in a readonly textarea. Header displays the filename and has Copy/Download buttons for the current file.
- **Global Actions Bar** — "Download All as ZIP" (creates ZIP via JSZip), "Copy Interactive Reference" (copies reference doc), "Legacy Text Output" (switches to text mode), "Parse Another File" (resets everything).
- **Legacy Output Panel** (`#legacy-output-panel`) — hidden by default; when activated via "Legacy Text Output" button, hides the file list + preview layout and shows the plain text output with Copy All, Download .txt, and Back to HTML buttons.
- **Responsive** — stacks vertically on mobile (file list above preview).

### Template Selector (Phase 2)

The template selector is a dropdown that appears between the drop zone and the "About" section. It:

1. Populates on page load from `TemplateEngine.getTemplateList()` (9 templates)
2. Auto-selects a template when a file is parsed (based on module code suffix) and shows "Auto-detected" label
3. Can be manually overridden by the user
4. Resets when "Parse Another File" is clicked

### Debug Panel (Phase 1 + Phase 2 + Phase 4)

The debug panel (`#debug-panel`) is a temporary development/testing panel that appears after parsing. It shows:

1. **Template Configuration** (Phase 2) — selected template ID, name, HTML template attribute, key config differences from base, overview page skeleton preview (first 50 lines), and footer navigation links for each page
2. **Tag Normalisation Results** — total tags, unrecognised tags, red text instructions, category breakdown, and a detailed table of all tags found (raw → normalised form)
3. **Page Boundary Results** — number of pages detected, filename/type/lesson number for each page, and which boundary validation rules fired
4. **Interactive Components** (Phase 4) — total count, tier breakdown, detailed table of all interactives (file, activity, type, tier, pattern, data summary), and a preview of the generated reference document

The debug panel uses a `<details>` element so it starts collapsed. It does NOT interfere with the multi-file output system or the legacy text output functionality.

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
  h1 spans: Module code prefix stripped, English + Te Reo split on double-space
  Module menu: Full tabbed (Overview + Information tabs) with routed content
    - Tooltip on #module-menu-content only (NOT on #module-menu-button)
    - Content before [MODULE INTRODUCTION] → tab panes
    - Content after [MODULE INTRODUCTION] → <div id="body">
  Title element: MODULE_CODE English Title (no Te Reo, no module prefix)
  Footer: next-lesson + home-nav only

Lesson page (-01, -02, etc.):
  Header: #module-code has zero-padded lesson number (01, 02, etc.)
  h1 span: MODULE title (not lesson-specific title)
  Module menu: Simplified (no tabs), populated from [Lesson Overview] content
    - Content between [Lesson Overview] and [Lesson Content] → module menu
    - "We are learning:" and "I can:" labels from template config (not writer text)
    - List items have italic stripped, description paragraph included
    - [Lesson Content] marks start of body content
  Title element: MODULE_CODE English Title (same as overview — never lesson number)
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
2. **Tag + instruction:** `🔴[RED TEXT] [drag and drop column autocheck] They are in correct place [/RED TEXT]🔴` → extract tag, capture instruction for interactive reference document only (NOT rendered in HTML)
3. **Pure instruction:** `🔴[RED TEXT] CS: please make images small [/RED TEXT]🔴` → captured for reference but NOT rendered as HTML comments
4. **Whitespace-only:** `🔴[RED TEXT]   [/RED TEXT]🔴` → disregard entirely
5. **NEVER render red text as visible student content**
6. **NEVER render CS/writer instructions as `<!-- CS: ... -->` HTML comments** — they are internal workflow notes captured only in the interactive reference document

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
| `external_link` | `<a href="URL" target="_blank">Text</a>` |
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
This content is routed into the module menu with template config labels:
- Description paragraph(s) before the first label section are included
- "We are learning:" / "I can:" labels come from template config, NOT from the writer's text
- List items under each label section populate the menu
- Italic formatting (`<i>`) is stripped from module menu list items and text

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

1. NEVER modify writer text — trust ParseMaster output as-is
2. Preserve macronised characters: ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō, Ū
3. Preserve bold/italic from within table cells
4. NEVER render square-bracket tags as visible text
5. NEVER add inline CSS, JavaScript, or invented class names

---

## 12. INTERACTIVE COMPONENTS

### Categories of Interactives

Interactive components are the complex elements that require custom JavaScript/HTML code from the component library. ParseMaster does NOT generate code for these — instead, it:

1. **Detects** the interactive type from the normalised tag (DONE — Phase 4)
2. **Extracts** all associated data (from tables, lists, red text instructions) (DONE — Phase 4)
3. **Classifies** interactives by tier (Tier 1 = ParseMaster renders in Phase 7, Tier 2 = Claude AI Project builds) (DONE — Phase 4)
4. **Inserts a structured placeholder** in the HTML output marking where the interactive goes (DONE — Phase 4)
5. **Generates a reference entry** in the supplementary interactive reference document (DONE — Phase 4)

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

### Placeholder Format (Implemented — Phase 4, redesigned Phase 4.5 Round 3)

Interactive placeholders are generated by `InteractiveExtractor.processInteractive()` and include structured HTML comments plus a rich visual placeholder showing captured data. The placeholder is colour-coded by tier and includes a content preview of extracted data.

```html
<!-- ========== INTERACTIVE: drag_and_drop (column_autocheck) | Activity: 2A | File: OSAI201-01.html ========== -->
<div class="activity interactive" number="2A">
  <div class="row">
    <div class="col-md-12 col-12">
      <!-- INTERACTIVE_START: drag_and_drop -->
      <!-- Data Pattern: 1 -->
      <!-- Data Summary: Table (6 rows × 2 columns) -->
      <!-- Writer Instructions: They are currently in the correct place -->
      <div style="border: 2px dashed #c0392b; padding: 15px; margin: 10px 0; background: #fde8e8;">
        <div style="font-weight: bold; color: #c0392b; margin-bottom: 8px;">
          ⚠️ INTERACTIVE: drag_and_drop | Activity: 2A | Pattern: 1
        </div>
        <hr style="border-top: 1px solid #c0392b; margin: 8px 0;" />
        <div style="font-size: 0.9em;">
          <table style="width:100%; border-collapse:collapse; margin:5px 0; font-size:0.9em;">
            <!-- Captured table data rows rendered here -->
          </table>
          <p style="color: #888; font-style: italic;">Writer: They are currently in the correct place</p>
        </div>
      </div>
      <!-- INTERACTIVE_END: drag_and_drop -->
    </div>
  </div>
</div>
<!-- ========== END INTERACTIVE: drag_and_drop ========== -->
```

**Tier 1 interactives** (accordion, flip_card, speech_bubble, tabs) use a green dashed border (#1a7a1a) with green background (#e6f9e6) and a wrench icon, indicating ParseMaster will render them in Phase 7. **Tier 2 interactives** use a red dashed border (#c0392b) with red background (#fde8e8) and a warning icon, indicating they require the Claude AI Project.

**Content preview rendering by data pattern:**
- **Pattern 1 (single table):** Rendered as an HTML `<table>` with headers and up to 5 data rows (truncated with "... and N more rows" if needed)
- **Pattern 2 (front/back):** Each card shown as "Card N: front → back" entries
- **Pattern 3 (hint/slide):** Hint/slide items listed with labels
- **Pattern 9 (conversation):** Conversation entries with bold "Prompt N:" / "AI response:" labels
- **Numbered items:** Items listed with numbered labels
- **Fallback:** "No structured data detected" if no data was captured

**Grid wrapper rule:** When `insideActivity` is true, the placeholder omits its own `<div class="row"><div class="col-...">` wrapper since the activity wrapper provides the grid context. When outside an activity, the placeholder includes its own row/col wrapper.

### Interactive Tier Classification (Implemented — Phase 4)

Each interactive is classified into one of two tiers:

| Tier | Description | Types | Placeholder Colour |
|------|-------------|-------|-------------------|
| **Tier 1** | ParseMaster renders full HTML (Phase 7) | `accordion`, `flip_card`, `speech_bubble`, `tabs` | Green dashed border |
| **Tier 2** | Claude AI Project builds (placeholder only) | Everything else | Red dashed border |

Tier classification is automatic based on the normalised interactive type. It affects:
- The visual appearance of the placeholder in the generated HTML
- The reference document entry (tier label and description)
- Future Phase 7 rendering (Tier 1 interactives will be fully rendered by ParseMaster)

### Interactive Reference Document (Implemented — Phase 4)

The supplementary reference document lists every interactive needed across all HTML files. It is generated by `InteractiveExtractor.generateReferenceDocument()` and available for viewing/copying/downloading via the HTML file selector dropdown in the UI:

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

#### tag-normaliser.js — DONE (Phase 1, updated Phase 4.5 Round 3)
- Implements the complete normalisation table from Section 10
- Takes raw tag text, returns normalised form + sub-identifier
- Handles red text extraction (tag-only, tag+instruction, pure instruction, whitespace-only)
- Case-insensitive matching with flexible hyphen/space handling
- Classifies tags by category (structural, heading, body, styling, media, activity, link, interactive, subtag)
- Handles special cases: info trigger image merge, D&D modifier extraction, trailing number/ID extraction
- **`[Table wordSelect]` / `[Table word select]`** — recognised as `word_select` interactive (not a generic table) before the generic table match fires
- **`[drop]` sub-tag** — recognised as synonym for `[back]` in the simple table mapping (used in click_drop front/back patterns)
- Public API: `processBlock(text)`, `normaliseTag(tagText)`, `getCategory(normalisedName)`

#### page-boundary.js — DONE (Phase 1)
- Implements all 4 Page Boundary Validation Rules
- Takes the content blocks array, returns page assignments
- Each page knows its type (overview, lesson), content blocks, and output filename
- Handles lesson numbering (explicit, sequential, mixed)
- Tracks boundary decisions (which rules fired and why)
- Public API: `assignPages(contentBlocks, moduleCode)`

#### html-converter.js — DONE (Phase 3, updated Phase 4, recalibrated Phase 4.5, structural fixes Round 3)
- The main conversion engine
- Takes parsed content + template configuration + interactive extractor → produces HTML strings
- Handles:
  - Document skeleton assembly (skeleton from TemplateEngine + body content)
  - **Overview page content routing** — splits content at `[MODULE INTRODUCTION]` into menu tab content (before) and body content (after)
  - **Lesson page content routing** — splits content at `[LESSON OVERVIEW]` / `[LESSON CONTENT]` boundaries; menu content goes to module menu, body content starts after `[LESSON CONTENT]`
  - **Module menu tab content** — populates Overview (h4 headings) and Information (h5 headings) tab panes with correctly routed content
  - **Lesson module menu content** — populates lesson page module menu with actual "We are learning:" / "I can:" content from `[LESSON OVERVIEW]`, using template config labels, with italic stripped from list items, and optional description paragraph
  - Body content (paragraphs, headings, lists, tables, alerts, media, etc.)
  - **Content grouping** — consecutive body content (headings, paragraphs, lists, images, videos, quotes, etc.) grouped in single row wrappers; new rows only created for structural boundaries (activities, interactives, alerts) or column class changes
  - Formatting conversion (`**bold**` → `<b>`, `*italic*` → `<i>`, `***both***` → `<b><i>`, `__underline__` → `<u>`)
  - Hyperlink conversion (`__text__ [LINK: URL]` → `<a href target="_blank">`)
  - HTML escaping of content text with tag preservation
  - Red text processing (strip, extract tags; CS instructions captured for reference doc but NOT rendered as HTML comments)
  - Interactive placeholder insertion (structured placeholders via InteractiveExtractor with data extraction, tier classification, and consumed-block skipping)
  - **Inline info trigger rendering** — `[info trigger]` tags rendered as `<span class="infoTrigger" info="definition">word</span>` inline elements
  - Grid wrapping (all content inside `<div class="row"><div class="col-md-8 col-12">`)
  - Video embedding (YouTube, YouTube Shorts, Vimeo with correct embed URLs)
  - Image placeholders (placehold.co + commented-out iStock references)
  - **Activity wrapper grid structure** — activities wrapped in outer `row → col-md-12 → activity div → inner row → col-12 → content`; duplicate activity numbers handled gracefully (previous activity flushed before new one opens)
  - **Activity auto-closure** (Round 3) — after an activity's interactive placeholder is emitted (`activityHasInteractive` flag), the activity wrapper is automatically closed when the next `[body]`, heading, or structural tag is encountered, preventing non-activity content from being swallowed inside the activity wrapper
  - **Activity heading extraction** (Round 3) — `[Activity 1A] Heading text` patterns extract the heading text after the tag and render it as `<h3>` inside the activity wrapper
  - **Table interactive tag promotion** (Round 3) — when a table block contains both interactive and non-interactive tags (e.g., `[speech bubble]` + `[image]` in table cells), the interactive tag is promoted to primary position so the block is processed as an interactive rather than rendered as a grid table
  - **Implicit click_drop detection** (Round 3) — table blocks containing `[front]` and `[back]` (or `[drop]`) sub-tags but no explicit interactive tag get a synthetic `click_drop` interactive tag injected, ensuring they are processed as interactive placeholders
  - **Alert multi-paragraph consumption** — `[alert]`, `[important]`, and cultural alert tags consume ALL following untagged paragraphs until the next structural/tagged boundary
  - **Heading rules** — no spans on h2-h5, full-heading bold/italic stripping, H1→H2 in body, consecutive heading tags produce separate elements
  - **H1 splitting** — on overview pages, bold heading + italic description separated into heading + `<p>`
  - **Success Criteria normalisation** — heading normalised to "How will I know if I've learned it?"
  - **Module menu formatting** — h4 headings in Overview tab, h5 headings in Information tab, italic stripped from list items and intro text
  - **Quote formatting** — splits quote text and attribution into separate `<p class="quoteText">` and `<p class="quoteAck">` elements; italic `<i>` tags stripped from quote text (CSS handles styling)
  - **Whakatauki pipe splitting** — content with `|` separator splits into Māori and English `<p>` elements
  - Lesson page rules (lesson number prefix stripping, module menu label normalisation)
  - Module menu content population (overview tabs with actual content, lesson menu with routed content)
- Maintains `collectedInteractives` array populated during conversion for reference doc generation
- Public API: `convertPage(pageData, config)`, `assemblePage(pageData, config, moduleInfo)`

#### template-engine.js — DONE (Phase 2)
- Loads template configurations from `templates/templates.json` (with embedded fallback)
- Provides `getTemplateList()` for UI dropdown population (9 templates)
- Auto-detects template from module code suffix via `detectTemplate(moduleCode)`
- Deep-merges `baseConfig` with per-template overrides via `getConfig(templateId)`
- Generates complete HTML document skeletons via `generateSkeleton(config, pageData)`
- Handles header section (module code, titles, dual h1 for 9-10/NCEA)
- **Title bar parsing** — strips module code prefix, splits English/Te Reo on double-space, English-only `<title>`
- Handles module menu (full-tabbed for overview with correct structure, simplified for lessons)
- **Tooltip placement** — `tooltip="Overview"` on `#module-menu-content` only for overview pages, on `#module-menu-button` only for lesson pages
- **Tab HTML structure** — no active/data-toggle/href/id/fade/in attributes, row wrapper, inner grid per tab-pane
- Handles footer navigation (prev/next/home with correct page links)
- Public API: `loadTemplates()`, `getTemplateList()`, `detectTemplate(moduleCode)`, `getConfig(templateId)`, `generateSkeleton(config, pageData)`

#### interactive-extractor.js — DONE (Phase 4, structural fixes & placeholder redesign Round 3)
- Detects interactive component tags in the content stream
- Classifies interactives by tier (Tier 1: ParseMaster renders, Tier 2: Claude AI Project builds)
- Identifies the data pattern (13 patterns) being used
- Extracts all associated data (tables, numbered items, red text instructions, media references)
- **Sub-tag grouping** — numbered sub-tags (slides, tabs, accordions, flip cards, shapes, hints, click drops) consumed as data within their parent interactive, not treated as separate interactives
- **Relaxed boundary detection** — within numbered items scope, headings/body/media/styling content is captured as item data; only structural/activity/different-interactive boundaries break. For flip_card, click_drop, and hint_slider, the lookahead also skips past body/heading/media blocks to find sub-tags further ahead.
- **Speech bubble conversation detection** (fixed Round 3) — Pattern 9 conversation layout consumes "Prompt N:" / "AI response:" paragraphs; stops at `[body]` tags and other structural boundaries; ANY untagged paragraph following a captured conversation entry is consumed as continuation (not just AI responses), enabling multi-paragraph entries; falls back to raw formatted text with red markers stripped if cleanText is empty
- **Table-embedded interactive detection** — interactive tags inside table cells (e.g., `[speech bubble]` in an image+text table) are detected and the entire table is consumed as the interactive's data block
- **Boundary detection with table data** (fixed Round 3) — for `expectsSubTags` types (flip_card, click_drop, hint_slider), when table data has already been captured, boundary tags that are NOT sub-tags of the current interactive properly terminate extraction (prevents consuming one extra block)
- **Untagged block handling for sub-tag types** (fixed Round 3) — untagged paragraphs within `expectsSubTags` interactive scope are consumed rather than breaking extraction, preventing flip card/click drop sub-content from leaking as body elements
- **Rich placeholder HTML** (redesigned Round 3) — placeholders include a styled header bar with type/activity/pattern info, a separator, and a content preview body showing captured data (tables, conversation entries, front/back cards, numbered items); colour-coded by tier (green for Tier 1, red for Tier 2)
- **Conditional grid wrapper** (fixed Round 3) — placeholder omits its own row/col wrapper when `insideActivity` is true (activity wrapper provides grid context), includes row/col when standalone
- Produces reference entry objects for the interactive reference document
- Generates complete plain text reference document for all interactives in a module
- **Inline interactives** — interactives not inside a named `[activity]` block get no `<div class="activity">` wrapper
- Column class selection based on interactive type (wide for D&D column, info trigger image)
- Public API: `processInteractive(contentBlocks, startIndex, pageFilename, activityId, insideActivity)`, `generateReferenceDocument(allInteractives, moduleCode)`

#### output-manager.js — DONE (Phase 5)
- Stores generated file entries (HTML files + interactive reference document)
- Each file has metadata: filename, content, type (html/reference), pageType, lessonNumber, size
- Provides `getFileList()` with formatted sizes for UI display
- Individual file download via Blob/URL technique
- Bulk ZIP download via JSZip (`downloadAsZip()`)
- Clipboard copy per file (`copyToClipboard()`) with modern API + fallback
- File count helpers (`getFileCount()`, `getHtmlFileCount()`)
- `clear()` resets all stored files
- Public API: `addFile(fileInfo)`, `getFileList()`, `getFileContent(filename)`, `downloadFile(filename)`, `downloadAsZip(zipFilename)`, `copyToClipboard(filename)`, `clear()`

### Extended App Flow (Current — Phase 5)

```
User drops .docx file
  → Template auto-detected from module code
  → DocxParser.parse() extracts content
  → OutputFormatter.formatAll() produces legacy text output
  → TagNormaliser processes all tags
  → PageBoundary validates and assigns pages
  → HtmlConverter generates HTML for each page:
    → TemplateEngine.generateSkeleton() creates document shell
    → HtmlConverter.convertPage() renders body content
    → InteractiveExtractor.processInteractive() handles interactive tags:
      → Detects interactive type and classifies tier (1 or 2)
      → Looks ahead to extract associated data (tables, numbered items, media)
      → Generates structured placeholder HTML
      → Collects reference entry with all extracted data
      → Returns blocksConsumed so HtmlConverter skips data blocks
    → HtmlConverter.assemblePage() combines skeleton + content + module menu
  → InteractiveExtractor.generateReferenceDocument() produces reference doc
  → OutputManager stores all generated files (HTML + reference doc)
  → App displays results (Phase 5 UI):
    → Metadata panel shows template, pages, interactive count with tier breakdown
    → Conversion summary shows pages, template, interactives, tags, warnings
    → File list panel shows all files with icons, metadata, per-file download/copy
    → Preview panel shows selected file content with copy/download buttons
    → First HTML file auto-selected for preview
    → "Download All as ZIP" creates ZIP archive
    → "Copy Interactive Reference" copies reference doc
    → "Legacy Text Output" toggles to plain text view
    → Debug panel shows template config, tag & page analysis, interactive details
```

---

## 14. TEMPLATE CONFIGURATION SYSTEM

### Design Principles

1. **JSON-driven** — all template rules in a single `templates.json` file
2. **Easy to extend** — adding a new template = adding a new JSON object
3. **Easy to tweak** — changing a rule for an existing template = editing a JSON value
4. **Override pattern** — templates inherit from a base configuration and override specific rules
5. **No code changes needed** — template additions/changes should never require JS code changes

### templates.json Structure (Implemented)

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
      "lessonPage": "{moduleCode} {englishTitle}"
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
