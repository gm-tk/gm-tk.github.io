# CLAUDE.md — PageForge Project Reference

> **Project:** PageForge — Writer Template Parser & HTML Converter
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
16. [ENGS301 Inconsistency Fixes](#16-engs301-inconsistency-fixes)
17. [LMS Compliance Recalibration](#17-lms-compliance-recalibration-phase-7)
18. [Tag Normalisation Robustness](#18-tag-normalisation-robustness-phase-1-patch)
19. [UI Overhaul & Rebranding](#19-ui-overhaul--rebranding-phase-8)
20. [Calibration Comparison Tool](#20-calibration-comparison-tool-phase-9)
21. [Visual Comparison Review Page](#21-visual-comparison-review-page-phase-10)
22. [Standalone Calibration Page](#22-standalone-calibration-page-phase-10)
23. [Review Page UX Improvements](#23-review-page-ux-improvements-phase-11)
24. [Per-Panel Sync Buttons](#24-per-panel-sync-buttons-phase-12)

---

## 1. PROJECT OVERVIEW

### What PageForge Does Today

PageForge is a client-side web application that reads Writer Template `.docx` files and converts them into fully marked-up HTML files for the D2L/Brightspace LMS. It also produces clean, structured plain text output (legacy mode). Interactive components are rendered as structured placeholders with all associated data extracted and preserved in a supplementary Interactive Reference Document — the Claude AI Project focuses exclusively on building the interactive component code.

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
10. **Block scoping** → hierarchical block grouping with open/close matching, ordinal normalization, compound tag splitting, layout direction, writer instruction detection (DONE — Phase 6)
11. **Layout table unwrapping** → detects Word tables used as two-column layout grids, unwraps their content into the main content stream, creates sidebar blocks for companion images and alerts (DONE — Phase 6.1)
12. **LMS compliance recalibration** → lesson number decimal format, title element format, activity class refinements (alertPadding, dropbox), table header semantics (rowSolid, th/thead/tbody), br→p conversion, info trigger definition formatting, download journal button, whakatauki author line, image iStock alt text, ALL-CAPS heading detection (DONE — Phase 7)
13. **Tag normalisation robustness** → pre-processing de-fragmentation of fractured red-text boundaries from MS Word XML, bracket whitespace cleanup, ordinal suffix stripping in resolveOrdinalOrNumber (DONE — Phase 1 Patch)
14. **UI overhaul & rebranding** → project renamed from ParseMaster to PageForge, upload decoupled from conversion with staged file + Convert button, template dropdown with auto-detect hint, conversion summary moved to debug panel, legacy text output replaced with direct download, "Copy Interactive Reference" button removed from action bar (DONE — Phase 8)
15. **Calibration comparison tool** → development utility for uploading human-developed HTML reference files, logging side-by-side comparison snapshots (original writer template content, PageForge output, human correct output), displaying logged snapshots with expand/delete, and exporting structured calibration reports as .txt for Claude AI analysis (DONE — Phase 9)
16. **Visual comparison review page** → dedicated review.html page with three synchronised viewing panels (PageForge rendered HTML, human reference HTML, parsed Writer Template content), file map sidebar, template-aware CSS injection for authentic LMS rendering in iframes, per-panel one-shot Sync buttons for cross-panel content alignment via textual-anchor matching with tiered fallback (exact → fuzzy → proportional), Raw HTML toggle mode with scroll-position preservation via textual-anchor matching, human reference file upload, "Copy to Snapshot" contextual buttons that save to sessionStorage for the standalone Conversion Error Log page, and a "Conversion Error Log" button that opens calibrate.html; toolbar row with Raw HTML button and Conversion Error Log button separated from header; accessed from main results via "Visual Comparison Review" button; data transferred via sessionStorage with chunked fallback (DONE — Phase 10, enhanced Phase 11, Phase 12)
17. **Standalone conversion error log page** → dedicated calibrate.html page (renamed from "Calibration Comparison Tool" to "Conversion Error Log"), with Step 1 (Upload Human Reference Files) removed and remaining steps renumbered; auto-populates form fields from sessionStorage keys set by the review page's "Copy to Snapshot" buttons on tab focus; managed by CalibrateApp controller class (DONE — Phase 10, renamed Phase 11)
18. **Review page UX improvements** → toolbar row relocated from header to dedicated row below title bar, "Calibration Tool" renamed to "Conversion Error Log" across all pages/code/labels, scroll-position preservation when toggling Raw HTML view using textual-anchor fuzzy matching with proportional fallback, reusable `normaliseTextForMatch` static method for text normalisation (DONE — Phase 11)
19. **Per-panel Sync buttons** → replaced global continuous Sync toggle with three per-panel one-shot Sync buttons (one per panel: PageForge Output, Human Reference, Writer Template); each button extracts a textual anchor from its panel's current viewport position and scrolls the other two panels to the best-matching content using tiered fallback (exact normalised match → fuzzy word match → proportional scroll); works across rendered and Raw HTML views; visual feedback via button pulse and target panel flash; no continuous scroll-coupling (DONE — Phase 12)

The HTML files will contain all content correctly marked up with the correct tags, classes, grid structure, and hierarchy — everything EXCEPT the code for interactive activities. Interactive activities will be left as clearly marked placeholders with all relevant data preserved, so the Claude AI Project can focus exclusively on building the interactive component code.

### What This Means for the Workflow

**Current workflow:**
```
Writer Template .docx → PageForge → HTML files (with interactive placeholders)
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
  → Convert button starts disabled

User drops/selects .docx file (Phase 8: staged upload)
  → App.stageFile() validates file type (.docx only)
  → File stored as this.stagedFile (NOT parsed yet)
  → Staged file info shown (filename displayed below drop zone)
  → Module code extracted from filename (regex: /[A-Z]{4}\d{3}/)
  → TemplateEngine.detectTemplate() auto-detects template from module code
    → Auto-detected template stored internally (this.autoDetectedTemplate)
    → Hint shown near staged file: "Auto-detected: Years 4–6"
    → Dropdown stays on default "Select template (auto-detected on upload)"
  → Convert button enabled
  → NO parsing or conversion runs at this stage

User clicks "Convert Document" button (Phase 8)
  → App.convertDocument() resolves template:
    → If user manually selected from dropdown → use manual selection
    → Otherwise → use auto-detected template
  → DocxParser.parse() extracts and processes XML
    → JSZip extracts word/document.xml from .docx ZIP
    → DOMParser parses XML into DOM
    → _walkBody() recursively extracts paragraphs, tables
    → Tracked changes resolved (del removed, ins kept)
    → SDT wrappers unwrapped
    → Content boundaries detected ([TITLE BAR] marker)
    → Metadata extracted from boilerplate
  → OutputFormatter.formatAll() converts to text (for download)
    → Metadata block formatted
    → Content formatted with formatting markers
  → LayoutTableUnwrapper.unwrapLayoutTables() detects and unwraps layout tables (Phase 6.1)
    → Scans tables for structural tags ([Activity], [body], [Button], interactives)
    → Checks contextual override (tables following interactive type tags are data, not layout)
    → Unwraps layout tables: extracts cell paragraphs into main content stream
    → Creates sidebar blocks for companion images and alerts
    → Modifies content array in-place before any downstream processing
  → TagNormaliser processes all content blocks (Phase 1)
    → Extracts square-bracket tags from red text and plain text
    → Normalises tag variants to canonical forms
    → Classifies tags by category
    → Extracts writer instructions from red text
  → BlockScoper scans content blocks for hierarchical structure (Phase 6)
    → Groups container elements (accordion, carousel, flip cards, etc.) with children
    → Matches opening/closing tags with fuzzy spelling tolerance
    → Detects implicit boundaries (page breaks, next activity, lookahead limit)
    → Normalises ordinal sub-tags to indexed form
    → Splits compound tags in red text blocks
    → Extracts layout direction and writer instructions
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
  → App.showResults() displays output (Phase 8 UI)
    → Metadata panel includes template name, pages generated, interactive count
    → File list panel shows all generated files with icons, metadata, per-file actions
    → Preview panel shows selected file content with copy/download buttons
    → First HTML file auto-selected for preview on load
    → "Download All as ZIP" creates ZIP archive of all files via JSZip
    → "Download Text Template" triggers direct download of plain text output
    → "Parse Another File" resets everything cleanly (including staged file, Convert button, template dropdown)
    → Debug panel (collapsed by default) shows conversion summary, template config, tag & page analysis, block scoping, interactive details, skeleton preview
```

### Class Responsibilities

| Class | File | Purpose |
|-------|------|---------|
| `DocxParser` | `js/docx-parser.js` | Extracts structured content from .docx XML |
| `OutputFormatter` | `js/formatter.js` | Converts parsed data to plain text output (legacy) |
| `TagNormaliser` | `js/tag-normaliser.js` | Tag taxonomy, normalisation, red text processing, and raw text de-fragmentation |
| `BlockScoper` | `js/block-scoper.js` | Hierarchical block scoping, ordinal normalization, compound splitting, layout detection |
| `LayoutTableUnwrapper` | `js/layout-table-unwrapper.js` | Detects and unwraps layout tables, extracts cell content into main stream, creates sidebar blocks |
| `PageBoundary` | `js/page-boundary.js` | Page boundary detection, validation, and assignment |
| `TemplateEngine` | `js/template-engine.js` | Template config loading, resolution, auto-detection, skeleton generation |
| `InteractiveExtractor` | `js/interactive-extractor.js` | Interactive component detection, data extraction, placeholder generation, reference document |
| `HtmlConverter` | `js/html-converter.js` | Core HTML conversion engine — transforms content blocks into marked-up HTML |
| `OutputManager` | `js/output-manager.js` | Multi-file output storage, file listing, individual/ZIP download, clipboard copy |
| `CalibrationManager` | `js/calibration-manager.js` | Calibration comparison tool — human reference file upload, comparison snapshot logging, snapshot display, calibration report export (standalone calibrate.html page Phase 10) |
| `ReviewApp` | `js/review-app.js` | Review page controller — data deserialisation, three-panel rendering, file map, template-aware CSS injection, per-panel one-shot Sync buttons with cross-panel textual-anchor matching (tiered fallback: exact → fuzzy → proportional), raw HTML toggle with scroll-position preservation via textual-anchor matching, human reference upload, copy-to-sessionStorage snapshot buttons, conversion error log launcher |
| `CalibrateApp` | `js/calibrate-app.js` | Conversion Error Log page controller — data deserialisation from sessionStorage, CalibrationManager instantiation, auto-population of snapshot form fields from sessionStorage keys, navigation |
| `App` | `js/app.js` | UI controller — staged upload, Convert button, file list, preview, ZIP download, text download, debug panel, template selection, visual review launcher |

---

## 3. FILE STRUCTURE

```
gm-tk.github.io/
├── index.html              # Single-page application shell
├── review.html             # Visual Comparison Review page (Phase 10)
├── calibrate.html          # Standalone Conversion Error Log page (Phase 10, renamed Phase 11)
├── css/
│   ├── styles.css          # All application styles (including debug panel, template selector, multi-file layout)
│   └── review-styles.css   # Review page styles (three-panel layout, toolbar row, per-panel sync buttons, raw HTML view) (Phase 10, updated Phase 11, Phase 12)
├── js/
│   ├── docx-parser.js      # .docx XML parser (core extraction engine)
│   ├── formatter.js         # Plain text output formatter (legacy)
│   ├── tag-normaliser.js    # Tag taxonomy & normalisation engine (Phase 1, enhanced Phase 6, Phase 1 Patch)
│   ├── block-scoper.js      # Block scoping engine — hierarchical grouping & analysis (Phase 6)
│   ├── layout-table-unwrapper.js # Layout table detection & unwrapping (Phase 6.1)
│   ├── page-boundary.js     # Page boundary detection & validation (Phase 1)
│   ├── template-engine.js   # Template config loading, resolution & skeleton generation (Phase 2)
│   ├── interactive-extractor.js # Interactive data extraction, placeholder generation & reference doc (Phase 4)
│   ├── html-converter.js    # Core HTML conversion engine (Phase 3, updated Phase 4)
│   ├── output-manager.js    # Multi-file output management, ZIP download, clipboard copy (Phase 5)
│   ├── calibration-manager.js # Calibration comparison tool — reference upload, snapshot logging, report export (Phase 9, standalone calibrate.html Phase 10)
│   ├── review-app.js       # Review page controller — three-panel rendering, CSS injection, per-panel one-shot Sync buttons with textual-anchor matching, raw HTML toggle with scroll preservation, copy-to-sessionStorage (Phase 10, enhanced Phase 11, Phase 12)
│   ├── calibrate-app.js    # Conversion Error Log page controller — data loading, CalibrationManager instantiation, auto-population from sessionStorage (Phase 10, renamed Phase 11)
│   └── app.js              # UI controller (with file list, preview, ZIP download, debug panel, visual review launcher)
├── tests/
│   ├── test-runner.js       # Minimal Node.js test runner (no external dependencies)
│   ├── tagNormaliserExisting.test.js # Regression tests for existing tag normalisation
│   ├── blockScoping.test.js # Block scoping engine tests
│   ├── ordinalNormalization.test.js # Ordinal-to-number sub-tag normalization tests
│   ├── compoundTags.test.js # Compound tag splitting tests
│   ├── layoutDirection.test.js # Layout direction extraction tests
│   ├── writerInstructions.test.js # Writer instruction detection tests
│   ├── fragmentReassembly.test.js # Red-text fragment reassembly tests
│   ├── interactiveInference.test.js # Interactive type inference from table structure tests
│   ├── videoNormalization.test.js # Video tag normalization tests
│   ├── alertNormalization.test.js # Alert/boxout container normalization tests
│   ├── insideTab.test.js   # [Inside tab] marker handling tests
│   ├── normalizeSubtags.test.js # Comprehensive ordinal & verbose sub-tag normalization tests
│   ├── layoutTableUnwrapper.test.js # Layout table detection, unwrapping, column role assignment tests
│   ├── engs301Fixes.test.js # ENGS301 inconsistency fixes: heading levels, incomplete headings, tag recognition, interactive rendering, data capture
│   ├── lmsCompliance.test.js # LMS compliance recalibration tests: lesson number format, title element, activity classes, table semantics, info trigger, download journal, whakatauki, image alt text
│   ├── defragmentation.test.js # Tag de-fragmentation tests: red-text boundary stitching, bracket space collapsing, whitespace trimming, processBlock integration, ordinal suffix stripping
│   └── reviewPageChanges.test.js # Review page Phase 11+12 tests: toolbar relocation, Conversion Error Log rename, per-panel Sync button DOM structure/positioning/CSS, global Sync toggle complete removal, one-shot align trigger implementation, content-matching with textual-anchor helpers, visual feedback, no continuous scroll-coupling, Raw HTML scroll preservation, normaliseTextForMatch helper
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

PageForge detects where actual module content begins by searching for the `[TITLE BAR]` tag. Everything before this is boilerplate (submission checklists, LOT tags, guidance text) and is used only for metadata extraction.

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

- **Staged file upload** (Phase 8) — drag-and-drop zone + click-to-browse, validates `.docx` extension, stages the file without triggering conversion. Shows staged file indicator with filename. Extracts module code from filename for template auto-detection.
- **Convert button** (Phase 8) — disabled by default, enabled when a file is staged, triggers the full conversion pipeline on click. Uses the manually selected template (if any) or the auto-detected template.
- **Template selection** — dropdown populated from TemplateEngine, default option reads "Select template (auto-detected on upload)". On file stage, auto-detected template stored internally with hint shown near file info. Manual dropdown selection takes priority over auto-detected.
- **Processing** — shows spinner + progress steps during conversion with pipeline stage counts
- **Results** — displays metadata panel, file list panel, preview panel
- **Multi-file output** — file list with per-file download/copy, preview of selected file (Phase 5)
- **ZIP download** — "Download All as ZIP" creates ZIP archive via JSZip (Phase 5)
- **Text download** (Phase 8) — "Download Text Template" triggers direct download of plain text output as .txt file
- **Debug panel** — after conversion, runs TagNormaliser and PageBoundary on content blocks, displays conversion summary + analysis results in a collapsible debug panel (collapsed by default)
- **Error handling** — specific error messages for known failure modes (missing XML, invalid XML, corrupted file)
- **Accessibility** — screen reader announcements, keyboard navigation, ARIA labels

### Section Visibility

The UI uses CSS `.hidden` class to toggle between these states:
1. `#upload-section` — initial file upload view (includes staged file info, template selector, Convert button)
2. `#processing-section` — spinner during conversion
3. `#results-section` — multi-panel output display with file list + preview + Visual Comparison Review button
4. `#debug-panel` — collapsible debug panel with conversion summary + analysis (appears below results after conversion)

### Multi-File Output System (Phase 5, updated Phase 8)

The results section uses a side-by-side layout with a file list panel (left) and preview panel (right):

- **File List Panel** (`#file-list-panel`) — shows all generated files with icons, filenames, metadata (page type, size), and per-file download/copy action buttons. Clicking a file loads its content in the preview. The selected file gets a `.selected` visual highlight. Files are stored in `OutputManager`. The interactive reference document is accessible here with per-file copy/download buttons.
- **Preview Panel** — shows the content of the currently selected file in a readonly textarea. Header displays the filename and has Copy/Download buttons for the current file.
- **Global Actions Bar** — "Download All as ZIP" (creates ZIP via JSZip), "Visual Comparison Review" (opens review.html in new tab with serialised data), "Download Text Template" (triggers direct .txt download), "Parse Another File" (resets everything including staged file, Convert button, template dropdown, visual review button).
- **Responsive** — stacks vertically on mobile (file list above preview).

### Staged Upload & Convert Flow (Phase 8)

The upload process is decoupled from conversion:

1. User drops/selects a `.docx` file → file is **staged** (stored as `this.stagedFile`)
2. Staged file indicator shows the filename below the drop zone
3. Module code is extracted from filename for template auto-detection
4. Auto-detected template stored internally (`this.autoDetectedTemplate`), hint shown as "Auto-detected: [name]"
5. Template dropdown remains on default option — user can optionally override by selecting a different template
6. **Convert button** becomes enabled
7. Clicking Convert triggers full pipeline (`convertDocument()` method)
8. Template resolution: manual dropdown selection takes priority; otherwise auto-detected template is used
9. Uploading a new file replaces the staged file, re-runs detection, keeps Convert enabled
10. "Parse Another File" resets: clears staged file, disables Convert button, resets dropdown

### Template Selector (Phase 2, updated Phase 8)

The template selector is a dropdown that appears between the drop zone and the Convert button. It:

1. Populates on page load from `TemplateEngine.getTemplateList()` (9 templates)
2. Default option: "Select template (auto-detected on upload)" — remains selected after file staging
3. Auto-detected template stored internally, hint shown near staged file info
4. User can manually select a different template — this takes priority on conversion
5. Resets when "Parse Another File" is clicked

### Debug Panel (Phase 1 + Phase 2 + Phase 4 + Phase 6, updated Phase 8)

The debug panel (`#debug-panel`) is a collapsible panel that appears after conversion. It starts **collapsed by default** using a `<details>` element. It contains:

1. **Conversion Summary** (Phase 8) — pages generated, template used, interactives detected, tags normalised + unrecognised, boundary rules fired. Previously displayed in the main results area; now consolidated here.
2. **Template Configuration** (Phase 2) — selected template ID, name, HTML template attribute, key config differences from base, overview page skeleton preview (first 50 lines), and footer navigation links for each page
3. **Tag Normalisation Results** — total tags, unrecognised tags, red text instructions, category breakdown, and a detailed table of all tags found (raw → normalised form)
4. **Page Boundary Results** — number of pages detected, filename/type/lesson number for each page, and which boundary validation rules fired
5. **Block Scoping Analysis** (Phase 6) — total scoped blocks, unscoped content count, scoped block details table (type, start/end index, children, closure reason, sub-tags), and scoping warnings
6. **Interactive Components** (Phase 4) — total count, tier breakdown, detailed table of all interactives (file, activity, type, tier, pattern, data summary), and a preview of the generated reference document

### Calibration Comparison Tool (Phase 9)

The calibration panel (`#calibration-section`) is a collapsible `<details>` element that appears after conversion, positioned between the results section and the debug panel. It starts **collapsed by default** and provides a development/testing utility for comparing PageForge output against human-developed reference HTML. It contains:

1. **Step 1 — Upload Human Reference Files** — drag-and-drop or file picker for `.html` files; stores content in memory (privacy model maintained); displays uploaded files with filename, size, and matched/unmatched status against generated filenames; allows removing individual files
2. **Step 2 — Log Comparison Snapshots** — form with 4 fields (3 required: original writer template content, PageForge generated output, human developer correct output; 1 optional: notes/commentary) plus a source file dropdown populated from generated files; "Log Snapshot" button only enabled when all 3 required fields have content; snapshots stored in memory as sequential objects with ID, timestamp, and all field data
3. **Logged Snapshots Display** — chronological list of logged snapshots with compact cards showing number, file, time, and content preview; expandable `<details>` to view full content of all 4 fields; individual delete with confirmation; count badge updates on add/delete
4. **Step 3 — Export Calibration Report** — generates structured plain text document formatted for Claude AI analysis; includes context notes about content differences and writer comments; download as `.txt` file or copy to clipboard; "Clear All Snapshots" with confirmation

All calibration data is ephemeral — cleared on "Parse Another File", page reload, or new conversion. Managed by `CalibrationManager` class instantiated in `App`.

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

After PageForge produces the `.txt` file, it is fed into a Claude AI Project that has extensive knowledge files defining how to convert the text into HTML. The key knowledge files are:

#### 00_MASTER_INSTRUCTIONS.md
- Defines the role, core philosophy, input requirements
- Outlines the 7-phase conversion pipeline
- Lists all 44 constraints
- References all other knowledge files

#### 01_PIPELINE_EXTRACTION_TAGS.md
Contains 5 sections:
- **Section 01 — Template Levels:** HTML tag patterns, head sections, heading patterns, module menu structures, title patterns, footer patterns per year level
- **Section 02 — PageForge Text Format:** File structure, metadata block, format conventions
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
  Title element: MODULE_CODE 0.0 English Title (no Te Reo, no module prefix)
  Footer: next-lesson + home-nav only

Lesson page (-01, -02, etc.):
  Header: #module-code has decimal lesson number (1.0, 2.0, etc.)
  h1 span: MODULE title (not lesson-specific title)
  Module menu: Simplified (no tabs), populated from [Lesson Overview] content
    - Content between [Lesson Overview] and [Lesson Content] → module menu
    - "We are learning:" and "I can:" labels from template config (not writer text)
    - List items have italic stripped, description paragraph included
    - [Lesson Content] marks start of body content
  Title element: MODULE_CODE N.0 English Title (includes decimal lesson number)
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
| `video`, `embed video`, `imbed video`, `insert video`, `embed film`, `imbed film`, `Interactive: Video: Title`, `audio animation video` | `video` |
| `audio` | `audio` |
| `audio image`, `audioimage`, `audioImage` | `audio_image` |
| `image zoom` | `image_zoom` |
| `image label` | `image_label` |

#### Activity Tags
| Writer Variants | Normalised |
|---|---|
| `activity NA`, `activity` | `activity` + ID |
| `activity heading`, `activity heading h3`, `activity heading H3`, `activity title` (with optional heading level H2-H5) | `activity_heading` + level |
| `end activity`, `end of activity` | `end_activity` |

#### Link/Button Tags
| Writer Variants | Normalised |
|---|---|
| `button` | `button` |
| `button- external link`, `button-external link`, `button - external`, `button-external` | `external_link_button` |
| `external link button` | `external_link_button` |
| `external link` | `external_link` |
| `go to journal` | `go_to_journal` |
| `download journal` | `download_journal` |
| `upload to dropbox` | `upload_to_dropbox` |
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
| `flip cards`, `flip card`, `flipcard`, `flipcards`, `flip card N`, `flipcard image` | `flip_card` |
| `accordion`, `accordion N` | `accordion` |
| `end accordions` | `end_accordions` |
| `click drop`, `clickdrop`, `drop click` | `click_drop` |
| `carousel`, `slide show`, `slideshow` | `carousel` |
| `rotating banner` | `rotating_banner` |
| `slide N` | `carousel_slide` |
| `tabs` | `tabs` |
| `tab N` | `tab` |
| `speech bubble` + any suffix | `speech_bubble` |
| `hint slider`, `hintslider`, `hint slider N`, `hintslider N` | `hint_slider` |
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
| `mcq`, `multi choice quiz`, `multichoice dropdown quiz`, `multi choice dropdown quiz`, `dropdown quiz` | `mcq` |
| `multi choice quiz survey` | `multichoice_quiz_survey` |
| `radio quiz`, `true false` | `radio_quiz` |
| `checklist` | `checklist` |
| `info trigger` + optional text, `hovertrigger`, `hover trigger` | `info_trigger` |
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

1. NEVER modify writer text — trust PageForge output as-is
2. Preserve macronised characters: ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō, Ū
3. Preserve bold/italic from within table cells
4. NEVER render square-bracket tags as visible text
5. NEVER add inline CSS, JavaScript, or invented class names

---

## 12. INTERACTIVE COMPONENTS

### Categories of Interactives

Interactive components are the complex elements that require custom JavaScript/HTML code from the component library. PageForge does NOT generate code for these — instead, it:

1. **Detects** the interactive type from the normalised tag (DONE — Phase 4)
2. **Extracts** all associated data (from tables, lists, red text instructions) (DONE — Phase 4)
3. **Classifies** interactives by tier (Tier 1 = PageForge renders in Phase 7, Tier 2 = Claude AI Project builds) (DONE — Phase 4)
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

**Tier 1 interactives** (accordion, flip_card, speech_bubble, tabs) use a green dashed border (#1a7a1a) with green background (#e6f9e6) and a wrench icon, indicating PageForge will render them in Phase 7. **Tier 2 interactives** use a red dashed border (#c0392b) with red background (#fde8e8) and a warning icon, indicating they require the Claude AI Project.

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
| **Tier 1** | PageForge renders full HTML (Phase 7) | `accordion`, `flip_card`, `speech_bubble`, `tabs` | Green dashed border |
| **Tier 2** | Claude AI Project builds (placeholder only) | Everything else | Red dashed border |

Tier classification is automatic based on the normalised interactive type. It affects:
- The visual appearance of the placeholder in the generated HTML
- The reference document entry (tier label and description)
- Future Phase 7 rendering (Tier 1 interactives will be fully rendered by PageForge)

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

#### tag-normaliser.js — DONE (Phase 1, updated Phase 4.5 Round 3, Round 3C, enhanced Phase 6, Phase 1 Patch)
- Implements the complete normalisation table from Section 10
- Takes raw tag text, returns normalised form + sub-identifier
- Handles red text extraction (tag-only, tag+instruction, pure instruction, whitespace-only)
- Case-insensitive matching with flexible hyphen/space handling
- Classifies tags by category (structural, heading, body, styling, media, activity, link, interactive, subtag)
- Handles special cases: info trigger image merge, D&D modifier extraction, trailing number/ID extraction
- **`[Table wordSelect]` / `[Table word select]`** — recognised as `word_select` interactive (not a generic table) before the generic table match fires
- **`[drop]` sub-tag** — recognised as synonym for `[back]` in the simple table mapping (used in click_drop front/back patterns)
- **`[Activity heading H3]` and variants** (Round 3B) — `activity heading`, `activity heading hN`, `activity title` with optional heading level H2-H5; returns level in the normalised result (defaults to 3 if no level specified)
- **Red-text fragment reassembly** (Round 3C, enhanced Phase 6) — `reassembleFragmentedTags()` method detects adjacent red-text markers split across Word formatting runs and merges them when their combined content forms a valid `[tag]` pattern; handles 2-way through 6-way splits using longest-match-first approach; non-trimming regex preserves original whitespace for direct concatenation; called from `_buildFormattedText()` in HtmlConverter and InteractiveExtractor
- **`[story heading]` sub-tag** (Round 3C) — recognised as subtag for dropdown_quiz_paragraph interactive
- **`multichoice dropdown quiz paragraph`** (Round 3C) — added as variant for `dropdown_quiz_paragraph`
- **Video tag variants** (Phase 6) — `_matchVideoTag()` method matches `[embed video]`, `[imbed video]`, `[insert video]`, `[embed film]`, `[imbed film]`, `[Interactive: Video: Title]`, and `[audio animation video]` patterns before heading tag matching
- **`[slideshow]`** (Phase 6) — single-word variant normalised to `carousel` alongside existing `slide show`
- **Ordinal sub-tag recognition** — `_matchSubTag()` method recognises verbose ordinal sub-tags (e.g., `[First tab of accordion]`, `[Forth card, front H4 title]`, `[Inside tab]`, `[New tab]`, `[Accordion three: Routine]`, `[Card 1]`, `[Flipcard 1]`, `[Slide 1 - video]`, `[Carousel Image 1]`, `[Tab 1 body]`) so they are not reported as unrecognised; returns normalised forms with category 'subtag' and extracted index/level/modifier
- **`resolveOrdinalOrNumber(word)`** — public method that converts ordinal words (`first`–`tenth`), cardinal words (`one`–`ten`), misspellings (`forth`→4), and numeric strings to their integer equivalents; case-insensitive; returns null for unrecognised input
- **`defragmentRawText(text)`** (Phase 1 Patch) — pre-processing method that runs before tag extraction; stitches fractured red-text boundaries (`[/RED TEXT]🔴...🔴[RED TEXT]` → stripped), collapses multiple spaces inside square brackets, trims leading/trailing whitespace inside brackets; automatically called at the start of `processBlock()`
- **`resolveOrdinalOrNumber(word)`** (enhanced Phase 1 Patch) — now strips trailing ordinal suffixes (`1st`→1, `2nd`→2, `3rd`→3, `4th`→4, etc.) before parsing as integer, in addition to existing word ordinal/cardinal lookup and plain number parsing
- Public API: `processBlock(text)`, `normaliseTag(tagText)`, `getCategory(normalisedName)`, `reassembleFragmentedTags(text)`, `resolveOrdinalOrNumber(word)`, `defragmentRawText(text)`

#### block-scoper.js — DONE (Phase 6)
- Hierarchical block scoping engine that groups container elements with their children
- Stack-based open/close tracking for nested blocks (activities, interactives, alerts)
- **Block scoping** (`scopeBlocks()`) — scans content blocks, identifies opening tags for container types (accordion, carousel, flip_card, drag_and_drop, activity, alert/boxout, tabs, speech_bubble, etc.), matches closing tags, tracks children and sub-tags within each block
- **Fuzzy closer matching** (`_fuzzyMatchCloser()`) — matches closing tags despite spelling variations (e.g., `[End accordian]` matches `accordion`), generic closers (`[End interactive]`, `[End component]`), and compacted forms (`[endaccordion]`)
- **Implicit boundary detection** — blocks auto-close at: page break/end page tags, next activity opening, same-type reopening, and lookahead limit (200 lines with no closer found)
- **Ordinal-to-number normalization** (`normaliseSubTag()`) — converts verbose ordinal sub-tags to indexed forms: `[First tab of accordion]` → `{subTagType: 'tab', index: 1}`, `[Second card, front H4 title]` → `{subTagType: 'card_front', index: 2, headingLevel: 'H4', headingText: 'title'}`; handles misspellings (`forth` → 4); supports accordion tabs, flip card front/back, carousel slides, word-numbered items; `contentHint` field distinguishes content-type suffixes (`body`, `content`, `image`, `video`, `heading`) from heading labels on tab/accordion sub-tags; copy-paste mismatch detection on ordinal flip card backs corrects index when ordinal word doesn't match preceding `card_front` (e.g., ENGJ402 line 1024 "Third card, back" after "Forth card, front" → uses index 4); `[New tab N]` variant with trailing number supported; `[front of card title and image N]` handles "and" alongside "&"
- **Compound tag splitting** (`splitCompoundTags()`) — splits multiple bracket pairs in red text into individual tags: `[Body] [LESSON] 6` → 2 separate tag objects; handles no-space brackets `[Front][H3]`, triple brackets `[Card 1] [Front] [H3]`, trailing text after last bracket, and `[image of X and HN]` patterns
- **Layout direction extraction** (`extractLayoutDirection()`) — extracts positioning from tags like `[Image embedded left]`, `[Body right]`, `[Body bold]`, `[Body bullet points]`, `[Flip card image]`; returns `{element, position, style}` objects
- **Layout pair detection** (`detectLayoutPairs()`) — groups adjacent layout blocks into side-by-side pairs (e.g., image-right + body-left)
- **Writer instruction detection** (`detectWriterInstruction()`) — classifies tag text as writer notes vs functional elements using prefix patterns (`CS`, `Dev team`, `Note:`, `If correct`, etc.), sentence length analysis (>3 words = instruction), copyright detection, and button label extraction (≤3 words after `[Button]`)
- **Interactive type inference** (`inferInteractiveFromTable()`) — infers quiz/drag-drop types from table structure: True/False columns → `radio_quiz_true_false`, `[Correct]` markers → `multichoice_quiz`, 2-column matching pairs → `drag_and_drop`, Question header with 3+ columns → `multichoice_quiz`, single column numbered → `ordered_list`
- **Video tag normalization** (`normaliseVideoTag()`) — covers all video variants (`embed video`, `imbed video`, `insert video`, `embed film`, `Interactive: Video: Title`, `audio animation video`); returns `{type: 'video', title}` or null
- **Video timing extraction** (`extractVideoTiming()`) — extracts start/end timestamps from editorial instructions; normalises `M:SS`, `MM:SS`, `:SS` formats to `MM:SS`; supports patterns like "Start video at 1:30", "Finish playing at 2:45", combined "start...and end/finish" instructions
- **Alert/boxout normalization** (`normaliseAlertTag()`) — maps box/alert/thought bubble variants to structured form: `[Box out to the right]` → `{type: 'alert', variant: 'box_right'}`, `[Thought bubble green]` → `{type: 'alert', variant: 'thought_bubble', colour: 'green'}`, plus `[Supervisor note]`, `[Definition]`, `[Equation]`, `[alert/summary box]`, `[coloured box]`, `[alert.top]` and other variants
- **`[Inside tab]` marker** — recognised as a no-op marker within accordion/tab scope (not a new tab boundary)
- **Warnings array** — tracks scoping issues (unclosed blocks, lookahead limit reached, etc.)
- Public API: `scopeBlocks(contentBlocks)`, `normaliseSubTag(tagText, parentBlockType, lastIndex)`, `splitCompoundTags(text)`, `extractLayoutDirection(tagText)`, `detectLayoutPairs(blocks)`, `detectWriterInstruction(tagText)`, `inferInteractiveFromTable(tableData)`, `normaliseVideoTag(tagText)`, `extractVideoTiming(text)`, `normaliseAlertTag(tagText)`

#### layout-table-unwrapper.js — DONE (Phase 6.1)
- Detects Word tables used as two-column layout grids and unwraps their content into the main content stream
- **Layout table detection** (`isLayoutTable()`) — scans table cells for structural tags (activity, interactive, body, heading, UI elements); returns true if any cell contains high-confidence tags ([Activity], [multichoice dropdown quiz], etc.) or if ≥1 cell has ≥2 medium-confidence structural tags ([body]+[button], [H3]+[body], etc.)
- **Contextual override** (`_shouldOverrideAsDataTable()`) — prevents false positives: tables immediately following interactive type tags (flipcard, drag_and_drop, hintslider, carousel, accordion, etc.) within 5 blocks are treated as data tables for those interactives; overridden only if the table itself contains an [Activity] tag
- **Table unwrapping** (`_unwrapTable()`) — extracts cell paragraphs as individual content blocks, preserving the original paragraph data objects from the parser; each unwrapped block gets `_unwrappedFrom: 'layout_table'` and `_cellRole` metadata
- **Column role assignment** (`_assignColumnRoles()`) — classifies each cell as `main_content` (activity/body/heading/interactive/UI tags), `sidebar_image` (only image tags or plain image URL), `sidebar_alert` (only alert/important tags), or `content` (generic text)
- **Sidebar block creation** (`_createSidebarBlock()`) — creates annotated paragraph blocks for sidebar cells with `_sidebarImageUrl` or `_sidebarAlertContent` metadata, preserving original cell paragraphs for rendering
- **Pipeline position** — runs BEFORE tag normalisation, block scoping, page boundary, and HTML conversion; modifies the content array in-place
- Public API: `unwrapLayoutTables(contentBlocks, startIndex)`, `isLayoutTable(tableData)`

#### page-boundary.js — DONE (Phase 1)
- Implements all 4 Page Boundary Validation Rules
- Takes the content blocks array, returns page assignments
- Each page knows its type (overview, lesson), content blocks, and output filename
- Handles lesson numbering (explicit, sequential, mixed)
- Tracks boundary decisions (which rules fired and why)
- Public API: `assignPages(contentBlocks, moduleCode)`

#### html-converter.js — DONE (Phase 3, updated Phase 4, recalibrated Phase 4.5, structural fixes Round 3, Round 3C)
- The main conversion engine
- Takes parsed content + template configuration + interactive extractor → produces HTML strings
- Handles:
  - Document skeleton assembly (skeleton from TemplateEngine + body content)
  - **Overview page content routing** — splits content at `[MODULE INTRODUCTION]` into menu tab content (before) and body content (after)
  - **Lesson page content routing** — splits content at `[LESSON OVERVIEW]` / `[LESSON CONTENT]` boundaries; menu content goes to module menu, body content starts after `[LESSON CONTENT]`; when `[LESSON CONTENT]` is missing, uses heuristic fallback (menu ends at first heading/activity/interactive/styling tag) to prevent empty body
  - **Layout table rendering** (Round 3B) — 2-column tables with `[body]` text in one cell and `[image]` in the other (with no interactive tags) are rendered as Bootstrap side-by-side layout (`col-md-8` text + `col-md-4` image) preserving document column order
  - **Sidebar block rendering** (Phase 6.1) — unwrapped layout table sidebar blocks (from LayoutTableUnwrapper) are rendered as `alertImage` (companion images in `col-md-4`) or `alertActivity` (sidebar alerts in `col-md-4`), paired side-by-side with preceding main content via `_wrapSideBySide()`
  - **Module menu tab content** — populates Overview (h4 headings) and Information (h5 headings) tab panes with correctly routed content
  - **Lesson module menu content** — populates lesson page module menu with actual "We are learning:" / "I can:" content from `[LESSON OVERVIEW]`, using template config labels, with italic stripped from list items, and optional description paragraph; only bullet-pointed items collected for learning/success criteria sections (ordered/numbered items like activity questions are excluded)
  - Body content (paragraphs, headings, lists, tables, alerts, media, etc.)
  - **Content grouping** — consecutive body content (headings, paragraphs, lists, images, videos, quotes, etc.) grouped in single row wrappers; new rows only created for structural boundaries (activities, interactives, alerts) or column class changes
  - Formatting conversion (`**bold**` → `<b>`, `*italic*` → `<i>`, `***both***` → `<b><i>`, `__underline__` → `<u>`)
  - Hyperlink conversion (`__text__ [LINK: URL]` → `<a href target="_blank">`)
  - HTML escaping of content text with tag preservation
  - Red text processing (strip, extract tags; CS instructions captured for reference doc but NOT rendered as HTML comments)
  - Interactive placeholder insertion (structured placeholders via InteractiveExtractor with data extraction, tier classification, and consumed-block skipping)
  - **Inline info trigger rendering** — `[info trigger]` tags rendered as `<span class="infoTrigger" info="definition">word</span>` inline elements
  - **External link inline rendering** (Round 3C) — `[external link]` renders the URL as a visible inline `<a>` link within the paragraph text (text before tag stays as `<p>` content, URL after tag becomes a clickable `<a>` link with the URL as visible text); distinct from `[external link button]` which creates a styled button element
  - Grid wrapping (all content inside `<div class="row"><div class="col-md-8 col-12">`)
  - Video embedding (YouTube, YouTube Shorts, Vimeo with correct embed URLs)
  - Image placeholders (placehold.co + commented-out iStock references)
  - **Activity wrapper grid structure** — activities wrapped in outer `row → col-md-12 → activity div → inner row → col-12 → content`; duplicate activity numbers handled gracefully (previous activity flushed before new one opens); activity class is `activity interactive` for activities containing interactives, plain `activity` for non-interactive activities (no `alertPadding` class)
  - **Activity auto-closure** (Round 3, expanded Round 3B, revised Round 3C) — activity wrappers close only at clear section boundaries: `[H2]`/`[H3]` headings (section-level) or structural tags always close; `[H4]`/`[H5]` are sub-headings WITHIN activities and do NOT close; `[body]` tags only close AFTER an interactive has been consumed (before that, body text is instruction text within the activity); `[image]`, `[video]`, `[button]`, `[alert]` tags are content within activities and do NOT close the wrapper
  - **Activity heading extraction** (Round 3) — `[Activity 1A] Heading text` patterns extract the heading text after the tag and render it as `<h3>` inside the activity wrapper
  - **Activity heading tag recognition** (Round 3B) — `[Activity heading H3]`, `[Activity heading]`, `[Activity title]` and variants with optional heading level (H2-H5) are all recognised; heading level from the tag is used (defaults to `<h3>` if no level specified)
  - **Table interactive tag promotion** (Round 3) — when a table block contains both interactive and non-interactive tags (e.g., `[speech bubble]` + `[image]` in table cells), the interactive tag is promoted to primary position so the block is processed as an interactive rather than rendered as a grid table
  - **Implicit click_drop detection** (Round 3) — table blocks containing `[front]` and `[back]` (or `[drop]`) sub-tags but no explicit interactive tag get a synthetic `click_drop` interactive tag injected, ensuring they are processed as interactive placeholders
  - **Alert multi-paragraph consumption** — `[alert]`, `[important]`, and cultural alert tags consume ALL following untagged paragraphs until the next structural/tagged boundary
  - **Heading rules** — no spans on h2-h5, full-heading bold/italic stripping, H1→H2 in body, consecutive heading tags produce separate elements
  - **H1 splitting** — on overview pages, bold heading + italic description separated into heading + `<p>`
  - **Success Criteria normalisation** — heading normalised to "How will I know if I've learned it?"
  - **Module menu formatting** — h4 headings in Overview tab, h5 headings in Information tab, italic stripped from list items and intro text
  - **Quote formatting** — splits quote text and attribution into separate `<p class="quoteText">` and `<p class="quoteAck">` elements; italic `<i>` tags stripped from quote text (CSS handles styling)
  - **Whakatauki pipe splitting** — content with `|` separator splits into 2 or 3 `<p>` elements (Māori, English, optional Author)
  - Lesson page rules (lesson number prefix stripping, module menu label normalisation)
  - Module menu content population (overview tabs with actual content, lesson menu with routed content)
  - **Activity class refinements** (Phase 7) — outer wrapper uses default `col-md-8 col-12` (not `col-md-12`); class includes `alertPadding` when sidebar present, `dropbox` for upload_to_dropbox interactives
  - **Table header semantics** (Phase 7) — first row uses `<thead>` with `<tr class="rowSolid">` and `<th>` cells; data rows in `<tbody>` with `<td>`; no `<br>` tags (multi-paragraph cells use `<p>`)
  - **Info trigger formatting** (Phase 7) — `_formatInfoTriggerDefinition()` capitalises first letter and adds trailing period for multi-word definitions
  - **Download journal** (Phase 7) — `[download journal]` renders `downloadButton` class + `hint`/`hintDropContent` elements
  - **Image alt text** (Phase 7) — `alt` attribute populated from iStock number when available (e.g., `alt="iStock-12345678"`)
  - **ALL-CAPS heading detection** (Phase 7) — H2-H5 headings with >60% uppercase get a DEV CHECK HTML comment
  - **Sidebar alert class** (Phase 7) — sidebar alerts in `col-md-4` use `alert top` class instead of `alertActivity`
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
- **Lesson number format** (Phase 7) — `lessonDisplayNumber` (decimal `N.0`) for `#module-code` display; `lessonPadded` (zero-padded `01`) for filenames/footers; `<title>` includes `0.0` for overview, `N.0` for lessons
- Handles module menu (full-tabbed for overview with correct structure, simplified for lessons)
- **Tooltip placement** — `tooltip="Overview"` on `#module-menu-content` only for overview pages, on `#module-menu-button` only for lesson pages
- **Tab HTML structure** — no active/data-toggle/href/id/fade/in attributes, row wrapper, inner grid per tab-pane
- Handles footer navigation (prev/next/home with correct page links)
- Public API: `loadTemplates()`, `getTemplateList()`, `detectTemplate(moduleCode)`, `getConfig(templateId)`, `generateSkeleton(config, pageData)`

#### interactive-extractor.js — DONE (Phase 4, structural fixes & placeholder redesign Round 3, Round 3C)
- Detects interactive component tags in the content stream
- Classifies interactives by tier (Tier 1: PageForge renders, Tier 2: Claude AI Project builds)
- Identifies the data pattern (13 patterns) being used
- Extracts all associated data (tables, numbered items, red text instructions, media references)
- **Sub-tag grouping** — numbered sub-tags (slides, tabs, accordions, flip cards, shapes, hints, click drops) consumed as data within their parent interactive, not treated as separate interactives
- **Relaxed boundary detection** — within numbered items scope, headings/body/media/styling content is captured as item data; only structural/activity/different-interactive boundaries break. For flip_card, click_drop, and hint_slider, the lookahead also skips past body/heading/media blocks to find sub-tags further ahead.
- **Speech bubble conversation detection** (fixed Round 3, updated Round 3B) — Pattern 9 conversation layout detected from tag modifier, cleanText, OR red text instructions (writer instruction "Conversation layout" now correctly found when inside red text region but outside brackets); forward lookahead consumes "Prompt N:" / "AI response:" paragraphs; stops at `[body]` tags and other structural boundaries; ANY untagged paragraph following a captured conversation entry is consumed as continuation (not just AI responses), enabling multi-paragraph entries; falls back to raw formatted text with red markers stripped if cleanText is empty; conversation data rendered as 2-column table in placeholder (label | content)
- **Table-embedded interactive detection** — interactive tags inside table cells (e.g., `[speech bubble]` in an image+text table) are detected and the entire table is consumed as the interactive's data block
- **Boundary detection with table data** (fixed Round 3) — for `expectsSubTags` types (flip_card, click_drop, hint_slider), when table data has already been captured, boundary tags that are NOT sub-tags of the current interactive properly terminate extraction (prevents consuming one extra block)
- **Untagged block handling for sub-tag types** (fixed Round 3) — untagged paragraphs within `expectsSubTags` interactive scope are consumed rather than breaking extraction, preventing flip card/click drop sub-content from leaking as body elements
- **Rich placeholder HTML** (redesigned Round 3) — placeholders include a styled header bar with type/activity/pattern info, a separator, and a content preview body showing captured data (tables, conversation entries, front/back cards, numbered items); colour-coded by tier (green for Tier 1, red for Tier 2)
- **Conditional grid wrapper** (fixed Round 3) — placeholder omits its own row/col wrapper when `insideActivity` is true (activity wrapper provides grid context), includes row/col when standalone
- **Dropdown quiz paragraph compound extraction** (Round 3C) — `dropdown_quiz_paragraph` interactives span multiple blocks: story paragraphs with inline `[Dropdown N]` markers, optional `[story heading]` sub-tag, and an options table are all collected into a single interactive placeholder; `[Dropdown N]` markers are treated as inline position markers (not separate interactives); content preview shows story text with dropdown positions marked and options table
- **Noisy table cell content extraction** (Round 3C) — `_extractCellContentClean()` method strips CS instructions, tag markers, and formatting artifacts from table cells, keeping only meaningful body text and URLs; used for speech bubble and similar interactives where cells may contain extra writer notes
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

#### calibration-manager.js — DONE (Phase 9)
- Development utility for comparing PageForge output against human-developed reference HTML
- **Human reference file upload** — drag-and-drop or file picker for `.html` files; stores content in memory (privacy model maintained); validates file type; detects duplicates; matches uploaded filenames against generated filenames; displays file list with size/matched status; individual file removal
- **Comparison snapshot logging** — form with 3 required fields (original writer template content, PageForge output, human correct output) and 1 optional field (notes/commentary); source file dropdown populated from generated files; validation enables/disables Log button; snapshots stored as sequential objects with ID, timestamp, sourceFile, and all field data
- **Snapshot list display** — chronological list of compact cards with expand/delete; preview text truncated to 80 chars; full content view in `<details>` element; individual delete with `confirm()` dialog; count badge
- **Calibration report export** — generates structured plain text document with module/template metadata, context notes for Claude AI analysis, and all snapshots in order; download as `.txt` file via Blob/URL; clipboard copy with modern API + `execCommand` fallback; "Clear All" with confirmation
- **Full reset** — clears all data (reference files, snapshots) on "Parse Another File" or new conversion; no data persists between sessions
- Instantiated by `App` with callback hooks for `showToast`, `getModuleCode`, `getTemplateName`, `getGeneratedFileList`
- Public API: `init()`, `populateSourceFileDropdown()`, `reset()`

### Extended App Flow (Current — Phase 10)

```
User drops .docx file (or clicks to browse)
  → App.stageFile() validates .docx extension
  → File stored as this.stagedFile (NOT processed yet)
  → Staged file indicator shown with filename
  → Module code extracted from filename (regex: /[A-Z]{4}\d{3}/)
  → If module code found: TemplateEngine.detectTemplate() auto-detects template
    → Auto-detected template stored internally (this.autoDetectedTemplate)
    → "Auto-detected" hint shown on staged file indicator
    → Template dropdown NOT changed (stays on placeholder)
  → Convert button enabled
  → User can optionally select a different template from dropdown
    → Manual selection sets this.userManuallySelectedTemplate = true

User clicks "Convert Document"
  → App.convertDocument() resolves template (manual > auto-detected > null)
  → Processing section shown with spinner
  → DocxParser.parse() extracts content
  → OutputFormatter.formatAll() produces legacy text output (stored for download)
  → LayoutTableUnwrapper.unwrapLayoutTables() processes content array:
    → Scans all tables for structural tags (activity, body, heading, interactive, UI)
    → Checks contextual override (data tables following interactive type tags preserved)
    → Layout tables: cell paragraphs extracted into main content stream
    → Sidebar cells (images, alerts) become annotated sidebar blocks
    → Content array modified in-place before all downstream processing
  → TagNormaliser processes all tags
  → BlockScoper.scopeBlocks() performs hierarchical block analysis:
    → Groups container elements (accordions, carousels, flip cards, etc.) with children
    → Matches opening/closing tags with fuzzy spelling tolerance
    → Detects implicit boundaries (page breaks, next activity, lookahead limit)
    → Normalises ordinal sub-tags to indexed form
    → Splits compound tags in red text blocks
    → Extracts layout direction and writer instructions
    → Results stored in analysis for debug panel
  → PageBoundary validates and assigns pages
  → App._extractTitle() extracts English/Te Reo titles from [TITLE BAR] content
    → Searches non-red text on same block or subsequent blocks
    → Splits English/Te Reo on double-space separator
    → Falls back to metadata subject if no title found
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
  → App.showResults() displays results (Phase 8 UI):
    → Metadata panel shows template, pages, interactive count with tier breakdown
    → File list panel shows all files with icons, metadata, per-file download/copy
    → Preview panel shows selected file content with copy/download buttons
    → First HTML file auto-selected for preview
    → "Download All as ZIP" creates ZIP archive via JSZip
    → "Download Text Template" triggers direct .txt file download (no modal/toggle)
    → "Parse Another File" resets all state (staged file, template, results)
    → Visual Comparison Review button enabled
    → Debug panel (collapsible) shows conversion summary, template config, tag & page analysis, block scoping, interactive details

User clicks "Visual Comparison Review" button (Phase 10)
  → App._serialiseForReview() serialises all data (generated HTML files, page data with content block texts, metadata, template info, templateAttribute)
  → Data stored in sessionStorage as pageforge_review_data (with chunked fallback for large payloads)
  → window.open('review.html') opens review page in new tab
  → ReviewApp loads and deserialises data from sessionStorage
  → File map and three panels rendered with template-aware CSS injection for authentic LMS styling
  → User uploads human reference files via Human Reference panel upload zone
  → User clicks per-panel Sync buttons — one-shot textual-anchor matching scrolls other two panels to corresponding content
  → User clicks "Copy PF"/"Copy Human"/"Copy WT" buttons — content saved to sessionStorage keys

User clicks "Conversion Error Log" button on review page (Phase 10, renamed Phase 11)
  → ReviewApp._openConversionErrorLog() serialises {generatedFileList, metadata, templateName} to sessionStorage key pageforge_calibrate_data
  → window.open('calibrate.html') opens Conversion Error Log page in new tab
  → CalibrateApp loads data, instantiates CalibrationManager, auto-populates form fields from sessionStorage snapshot keys
  → User logs snapshots and exports calibration report
  → User can switch back to review tab, copy more content, switch to Conversion Error Log tab — fields auto-populate on focus
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

- **Automated unit tests** — `node tests/test-runner.js` runs 479 tests across 17 test files covering tag normalisation, block scoping, ordinal normalization, compound tag splitting, layout direction, writer instructions, fragment reassembly, interactive inference, video normalization, alert normalization, `[Inside tab]` handling, comprehensive sub-tag normalization (verbose ordinals, copy-paste mismatch detection, contentHint, carousel slides, flip card patterns), layout table detection/unwrapping (detection heuristics, contextual override, column role assignment, sidebar creation, content stream integrity), ENGS301 inconsistency fixes (heading level extraction, incomplete heading fallback, title case conversion, unrecognized tag implementations, hintslider/flipcard tag recognition, multichoice dropdown quiz, interactive data capture), LMS compliance recalibration (lesson number decimal format, title element format, activity classes, table header semantics, info trigger definition formatting, download journal, whakatauki author, image alt text), tag de-fragmentation (red-text boundary stitching, bracket space collapsing, bracket whitespace trimming, processBlock integration, ordinal suffix stripping), and review page Phase 11+12 changes (toolbar relocation DOM structure, Conversion Error Log rename consistency, per-panel Sync button DOM presence/positioning/CSS, global Sync toggle complete removal, one-shot align trigger implementation, content-matching with textual-anchor helpers, visual feedback, no continuous scroll-coupling, Raw HTML scroll-position preservation with textual-anchor matching, normaliseTextForMatch helper unit tests)
- **Test runner** — minimal Node.js runner (`tests/test-runner.js`) with `describe()`, `it()`, `assert*()` functions; uses `vm.runInThisContext()` to load source files (tag-normaliser, block-scoper, layout-table-unwrapper, formatter, template-engine, interactive-extractor, html-converter) with class declarations in global scope; exposes `__testFs`, `__testPath`, `__testRootDir` globals for file-reading tests; no external dependencies
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

---

## 16. ENGS301 INCONSISTENCY FIXES

### Overview

Fixes for 13 specific inconsistencies discovered in the ENGS301 module ("Picture This!"), grouped into 8 root causes across 6 implementation areas. All fixes are backward-compatible and do not affect existing functionality for other modules.

**Status:** DONE — All 13 issues fixed, 28 new tests added (380 total with Phase 7), all tests passing.

### Files Modified

| File | Changes |
|------|---------|
| `js/tag-normaliser.js` | Added recognition for: incomplete heading `[H ]`, `[hovertrigger]`, `hintslider` (one word), `flipcard` (one word), `[button- external link]` variants, `[Go to journal]`, `[multichoice dropdown quiz]` variants |
| `js/html-converter.js` | Fixed heading level demotion; added incomplete heading fallback; added `[go_to_journal]` rendering; added hovertrigger inline rendering; added `_renderHintSlider()` and `_renderFlipCard()` methods; added yellow highlight markers |
| `js/interactive-extractor.js` | Added plain-text capture for `word_select`/`word_highlighter`; preserved `[IMAGE:]` references in cell extraction; preserved short red-text content descriptors |
| `js/app.js` | Added `_convertToTitleCase()` for ALL CAPS titles; added bilingual title splitting at sentence-ending punctuation + Te Reo detection |
| `js/formatter.js` | Added list counter tracking per `numId` with format-aware output (decimal, lowerLetter, upperLetter); added yellow highlight markers |
| `tests/test-runner.js` | Added `js/formatter.js` to loaded scripts |
| `tests/engs301Fixes.test.js` | New file — 28 tests covering all ENGS301 fixes |

### Issue-by-Issue Summary

#### Issue #1 — Title bar ALL CAPS and bilingual split
- **Root cause:** `_extractTitle()` did not convert ALL CAPS to title case or split bilingual titles without double-space separator
- **Fix:** Added `_convertToTitleCase()` in `app.js` (converts when >60% uppercase); added sentence-ending punctuation split with Te Reo detection (macrons, common Māori words)

#### Issue #2 — `[IMAGE:]` references lost in drag-and-drop data
- **Root cause:** `_extractCellText()` used `cleanText` which strips all `[tags]` including `[IMAGE: filename]`
- **Fix:** Re-extract `[IMAGE: ...]` references from raw formatted text after clean extraction

#### Issue #3 — `[hovertrigger]` not recognised
- **Root cause:** Tag not in normalisation table; pattern spans multiple red-text regions
- **Fix:** Added `hovertrigger` regex in tag-normaliser.js mapping to `info_trigger`; added `_extractHovertriggerData()` and `_renderHovertriggerParagraph()` in html-converter.js for cross-red-text-boundary detection

#### Issue #4 — `[multichoice dropdown quiz]` not recognised
- **Root cause:** Tag variant not in normalisation table
- **Fix:** Added `multichoice dropdown quiz`, `multi choice dropdown quiz`, and `dropdown quiz` mappings to `mcq` with `modifier: 'dropdown'`

#### Issue #5 — Incomplete heading `[H ]` crashes
- **Root cause:** Heading regex required a digit after `H`
- **Fix:** Added `^h\s*$` regex match returning `level: null, modifier: 'incomplete'`; html-converter.js uses `_lastHeadingLevel` fallback with developer warning comment

#### Issue #6 — `[button- external link]` not recognised
- **Root cause:** Button suffix variants with irregular spacing/dashes not handled
- **Fix:** Added regex `^button\s*[-–—]?\s*(external\s*link|external|link|download)$` before simple lookup table

#### Issue #7 — Heading level not respected (H2 demoted to H3)
- **Root cause:** "Lesson N" prefix stripping logic also set `headingLevel = 3`
- **Fix:** Removed heading level demotion; now strips prefix text only, preserving the original heading level

#### Issue #8 — Word highlighter plain-text data not captured
- **Root cause:** `_extractData()` only looked for table data, not plain-text paragraphs
- **Fix:** Added special case for `word_highlighter` and `word_select` to capture all following untagged paragraphs as numbered items (pattern 4)

#### Issue #9 — `[Go to journal]` not recognised
- **Root cause:** Tag not in normalisation table or rendering logic
- **Fix:** Added `go_to_journal` to simple lookup table (category: link); added rendering as `<h4 class="goJournal">Go to your journal</h4>`

#### Issue #10 — `[hintslider]` (one word) not recognised + no rendering
- **Root cause:** Hint slider regex required a space (`^hint\s+slider`); no rendering method existed
- **Fix:** Changed regex to `^hint\s*slider`; added `_renderHintSlider()` method that parses table data and renders `<div class="hintSlider">` with `hintRow dark` divs

#### Issue #11 — Short red-text content descriptors stripped
- **Root cause:** `_extractCellText()` stripped all red text as writer instructions
- **Fix:** Preserve short red-text content (1-5 words without instruction verbs) as content labels

#### Issue #12 — `[flipcard]` (one word) not recognised + no rendering
- **Root cause:** Flip card regex required a space (`^flip\s+cards?`); no rendering method existed
- **Fix:** Added exact-match alternatives for `flipcard`, `flipcards`, `flipcard image`, `flipcards image` (without breaking `[Flipcard 1]` sub-tag recognition); added `_renderFlipCard()` method that reads columns as cards and renders `<div class="row flipCardsContainer">`

#### Issue #13 — Formatter list numbering and yellow highlighting
- **Root cause:** Formatter used hardcoded `'1. '` for all ordered lists; no highlight extraction
- **Fix:** Added `_listCounters` per `numId` with format-aware output (decimal→`1.`, lowerLetter→`a.`, upperLetter→`A.`); added yellow highlight `✅` marker in both formatter.js and html-converter.js

---

## 17. LMS COMPLIANCE RECALIBRATION (Phase 7)

### Overview

A detailed audit comparing PageForge's HTML output against the actual D2L/Brightspace LMS template reference revealed 18 gaps where generated HTML did not fully match the structural patterns required by the LMS. All changes are backward-compatible and grouped by priority: 5 high-priority structural fixes, 4 medium-priority class/attribute fixes, 4 lower-priority enhancements, and 5 already-correct verifications.

**Status:** DONE — All 18 issues addressed, 39 new tests added (380 total), all tests passing.

### Files Modified

| File | Changes |
|------|---------|
| `js/template-engine.js` | Added `lessonDisplayNumber` (decimal format `N.0`) for `#module-code` display; separated display format from filename format (`lessonPadded`); updated `<title>` element to include decimal lesson number (`MODULE_CODE N.0 Title` for lessons, `MODULE_CODE 0.0 Title` for overview); updated `_generateHeader()` to use `lessonDisplayNumber` |
| `js/html-converter.js` | Changed activity outer wrapper from `col-md-12` to `colClass` (default `col-md-8 col-12`); added `activityHasSidebar`/`activityHasDropbox` tracking flags; activity class now includes `alertPadding` when sidebar present, `dropbox` when upload_to_dropbox interactive present; sidebar alerts render with `alert top` class instead of `alertActivity`; table cells use `<p>` tags instead of `<br />`; table header row gets `class="rowSolid"` with `<th>` elements and `<thead>`/`<tbody>` sections; added `_formatInfoTriggerDefinition()` for multi-word capitalisation + period; added `download_journal` rendering with `downloadButton` class + hint elements; whakatauki pipe split now supports 3-part (Māori \| English \| Author); image `alt` text populated from iStock number; added ALL-CAPS heading DEV CHECK comment for H2-H5 |
| `js/tag-normaliser.js` | Added `download_journal` (category: link) and `upload_to_dropbox` (category: interactive) to simple lookup table and interactive types set |
| `tests/test-runner.js` | Added `template-engine.js`, `interactive-extractor.js`, and `html-converter.js` to loaded scripts for test environment |
| `tests/lmsCompliance.test.js` | New file — 39 tests covering all 18 LMS compliance changes |

### Change-by-Change Summary

#### Change 1 — Lesson Number Format in `#module-code` (Decimal Format)
- **Previous:** Zero-padded integer (`01`, `02`, `03`) via `String(lessonNum).padStart(2, '0')`
- **Fix:** Introduced `lessonDisplayNumber` (decimal format `1.0`, `2.0`, `3.0`) for `#module-code` `<h1>` content; `lessonPadded` (zero-padded `01`, `02`) preserved for filenames and footer navigation hrefs

#### Change 2 — `<title>` Element Format for Lesson Pages
- **Previous:** `MODULE_CODE English Title` for all pages
- **Fix:** Overview pages: `MODULE_CODE 0.0 English Title`; Lesson pages: `MODULE_CODE N.0 English Title`

#### Change 3 — Activity Wrapper Outer Column Class
- **Previous:** Activity wrappers wrapped in `col-md-12 col-12` in all 4 closing code paths
- **Fix:** Changed all 4 activity-closing code paths (auto-close, duplicate flush, end_activity, final close) to use `colClass` (default `col-md-8 col-12`)

#### Change 4 — Activity `alertPadding` Class When Sidebar Present
- **Previous:** Activity div never included `alertPadding` class
- **Fix:** Added `activityHasSidebar` flag; set to `true` when sidebar block paired with activity via `_wrapSideBySide()`; all 4 activity-closing paths append `alertPadding` to class string when flag is true

#### Change 5 — Activity `.dropbox` Class for Upload Activities
- **Previous:** Activities only got `activity` or `activity interactive`
- **Fix:** Added `upload_to_dropbox` tag to normaliser (category: interactive); added `activityHasDropbox` flag set when interactive type is `upload_to_dropbox`; activity class logic: `activity dropbox` if dropbox, `activity interactive` if other interactive, `activity` if none

#### Change 6 — Alert `.top` Class in `col-4` Sidebar
- **Previous:** Sidebar alerts rendered with `<div class="alertActivity">`
- **Fix:** Changed `_renderSidebarBlock()` sidebar_alert output to `<div class="alert top">` with standard alert inner structure

#### Change 7 — `offset-md-0` on All Sidebar `col-md-4` Columns (Verified)
- **Status:** Already correct — `_wrapSideBySide()` and `_renderLayoutTable()` both include `offset-md-0` on `col-md-4` sidebar columns

#### Change 8 — No `<br>` Tags — Use `<p>` Instead
- **Previous:** `_renderCellContent()` joined multi-paragraph cells with `<br />`
- **Fix:** Single-paragraph cells render as plain text; multi-paragraph cells wrap each paragraph in `<p>` tags

#### Change 9 — Table Header Row: `rowSolid` Class and `<th>` Elements
- **Previous:** All rows rendered identically with `<tr>` and `<td>`, wrapped in single `<tbody>`
- **Fix:** First row rendered in `<thead>` with `<tr class="rowSolid">` and `<th>` cells; subsequent rows rendered in `<tbody>` with plain `<tr>` and `<td>` cells

#### Change 10 — Table `.table` Base Class (Verified)
- **Status:** Already correct — `_renderTable()` uses `<table class="table noHover tableFixed">`

#### Change 11 — Info Trigger Multi-Word Definition Formatting
- **Previous:** Definition text used as-is in `info` attribute
- **Fix:** Added `_formatInfoTriggerDefinition()` method: single-word definitions unchanged; multi-word definitions get capitalised first letter and trailing period (e.g., `"equal distance from two points"` → `"Equal distance from two points."`); applied to both `_extractInfoTriggerData()` and `_renderHovertriggerParagraph()`

#### Change 12 — Download Journal Button Structure
- **Previous:** No `[download journal]` tag recognition or rendering
- **Fix:** Added `download_journal` to normaliser (category: link); rendering produces `<a href="docs/MODULE_CODE Journal.docx" target="_blank"><div class="button downloadButton">Download journal</div></a>` followed by `<div class="hint"></div>` and `<div class="hintDropContent" hintType="oneDrive"></div>`

#### Change 13 — H1 Title Case / Other Headings Sentence Case (Conservative)
- **Previous:** ALL-CAPS detection only in `_convertToTitleCase()` for title bar text
- **Fix:** Added ALL-CAPS detection in heading rendering: if >60% of letters are uppercase in H2-H5 heading text, a `<!-- ⚠️ DEV CHECK: Heading appears to be ALL CAPS — should be Sentence case -->` comment is inserted before the heading element; text is NOT auto-transformed (conservative approach to protect proper nouns and Te Reo Māori)

#### Change 14 — `table-responsive` Wrapper (Verified)
- **Status:** Already correct — `_renderTable()` wraps tables in `<div class="table-responsive">`

#### Change 15 — Video iframe Attributes (Verified)
- **Status:** Already correct — YouTube standard videos include `width="560"`, `height="315"`, `loading="lazy"`, `title="YouTube video player"`, `frameborder="0"`, `allow="..."`, `referrerpolicy="strict-origin-when-cross-origin"`, `allowfullscreen`

#### Change 16 — External Button `externalButton` Class (Verified)
- **Status:** Already correct — `external_link_button` handler renders `<div class="externalButton">`

#### Change 17 — Whakatauki Optional Author Line
- **Previous:** Whakatauki only handled 2-part content (Māori | English)
- **Fix:** `_collectMultiLineContent()` now requests up to 3 lines; pipe splitting iterates all parts, supporting 3-part whakatauki (Māori | English | Author) where the third `<p>` renders the author attribution

#### Change 18 — Image Alt Text from iStock Number
- **Previous:** All images used `alt=""` — empty alt text
- **Fix:** `_renderImage()` uses `imgInfo.istockId` (e.g., `iStock-12345678`) as `alt` attribute value when available; `_renderImagePlaceholder()` extracts iStock number from `imageRef` URL via `gm(\d+)` pattern for layout table images; images without iStock references keep `alt=""`

---

## 18. TAG NORMALISATION ROBUSTNESS (Phase 1 Patch)

### Overview

Two critical issues in source data parsed from Microsoft Word documents were causing failures in the interactive block parsing pipeline:

1. **Tag Fragmentation:** Word's underlying XML frequently fractures single tags with redundant `[RED TEXT]` boundary markers (e.g., splitting `[link #1]` into `[lin` and `k #1]` across separate red-text regions).
2. **Ordinal Suffix Handling:** Numeric ordinal suffixes like `1st`, `2nd`, `3rd`, `4th` were not being stripped in `resolveOrdinalOrNumber()`, limiting the robustness of ordinal resolution.

All fixes are backward-compatible — the 380 pre-existing tests continue to pass alongside the 27 new tests (407 total).

**Status:** DONE — 2 changes implemented, 27 new tests added (407 total), all tests passing.

### Files Modified

| File | Changes |
|------|---------|
| `js/tag-normaliser.js` | Added `defragmentRawText()` public method; integrated into `processBlock()` pipeline as Step 0; enhanced `resolveOrdinalOrNumber()` with ordinal suffix stripping (`1st`→1, `2nd`→2, `3rd`→3, `4th`→4, etc.) |
| `tests/defragmentation.test.js` | New file — 27 tests covering red-text boundary stitching, bracket space collapsing, bracket whitespace trimming, processBlock integration, and ordinal suffix stripping |

### Change-by-Change Summary

#### Change 1 — `defragmentRawText(text)` Pre-Processing Method
- **Problem:** Microsoft Word's XML engine frequently splits a single red-text tag across multiple formatting runs, producing redundant `[/RED TEXT]🔴` + `🔴[RED TEXT]` boundary pairs mid-tag. For example, `[speech bubble]` becomes `🔴[RED TEXT] [speech [/RED TEXT]🔴🔴[RED TEXT] bubble] [/RED TEXT]🔴`. This prevents the tag extraction regex from matching the complete tag.
- **Fix:** New public method `defragmentRawText(text)` runs three cleaning passes:
  1. **Boundary stitching:** Regex `\[\/RED TEXT\]🔴\s*🔴\[RED TEXT\]` → stripped entirely. This collapses redundant close/re-open red-text markers so the inner content becomes continuous.
  2. **Multi-space collapse:** `\[([^\]]+)\]` callback replaces `\s{2,}` with single space inside all square brackets.
  3. **Bracket trimming:** Two regex passes trim leading and trailing whitespace inside square brackets (e.g., `[ H2 ]` → `[H2]`, `[body ]` → `[body]`).
- **Integration:** Automatically called at the start of `processBlock()` as "Step 0" before any red-text region extraction. This ensures all downstream tag extraction operates on clean, stitched text.
- **Safety:** The boundary stitching regex only targets the exact `[/RED TEXT]🔴...🔴[RED TEXT]` pattern and requires zero or whitespace-only content between the markers. It does not affect non-adjacent red-text regions with body text between them.

#### Change 2 — `resolveOrdinalOrNumber(word)` Ordinal Suffix Stripping
- **Problem:** Numeric ordinal strings like `"1st"`, `"2nd"`, `"3rd"`, `"4th"` were not being resolved because `parseInt()` returns NaN when the string contains trailing non-numeric characters, and the ordinal word map only covers word forms.
- **Fix:** Before falling through to `parseInt()`, the method now strips trailing ordinal suffixes (`st`, `nd`, `rd`, `th`) via regex `/(st|nd|rd|th)$/` and attempts `parseInt()` on the stripped result. This handles `"1st"`→1, `"2nd"`→2, `"3rd"`→3, `"4th"`→4, `"10th"`→10, `"21st"`→21, etc.
- **Order of resolution:** (1) Direct ordinal/cardinal word map lookup → (2) Suffix stripping + parseInt → (3) Plain parseInt. Existing behavior for word ordinals (`"first"`→1), cardinal words (`"one"`→1), and plain numbers (`"5"`→5) is entirely unchanged.

---

## 19. UI OVERHAUL & REBRANDING (Phase 8)

### Overview

Phase 8 combines a global rebranding (ParseMaster → PageForge) with a comprehensive UI overhaul that decouples the upload and conversion steps, consolidates the results screen, and removes redundant action buttons. All changes are backward-compatible — the 407 pre-existing tests continue to pass with zero modifications to test files (beyond the rebranded header comment).

**Status:** DONE — 3 phases implemented across 11 files, 407 tests passing (no new tests required — all changes are UI/cosmetic).

### Files Modified

| File | Changes |
|------|---------|
| `index.html` | Rebranded title/h1/footer; removed "Why PageForge?" section; added staged file indicator (`#staged-file-info`); added Convert button (`#btn-convert`); removed `#conversion-summary` div; removed `#btn-copy-reference`; removed `#btn-legacy-output`; removed `#legacy-output-panel`; added `#btn-download-text`; simplified debug panel header |
| `css/styles.css` | Rebranded header comment; removed About Section styles; added Staged File Info styles; added Convert Button styles; removed Legacy Output Panel styles; removed Conversion Summary styles; updated responsive rules |
| `js/app.js` | Rebranded JSDoc; new `stageFile()` method (staged upload without conversion); new `convertDocument()` method (pipeline triggered by button); new `_getResolvedTemplateId()` (manual > auto-detected priority); updated `_autoDetectTemplate()` (stores internally, shows hint); new `_handleDownloadText()` (direct Blob download); new `_renderDebugConversionSummary()` (summary stats in debug panel); removed legacy mode methods; removed Copy Interactive Reference handler; updated `reset()` for new state |
| `js/html-converter.js` | Rebranded JSDoc header and formatting markers comment |
| `js/interactive-extractor.js` | Rebranded JSDoc header and 3 string literals ("Generated by", "rendered by", "Rendered by") |
| `js/tag-normaliser.js` | Rebranded JSDoc header |
| `js/block-scoper.js` | Rebranded JSDoc header |
| `js/page-boundary.js` | Rebranded JSDoc header |
| `js/output-manager.js` | Rebranded JSDoc header |
| `tests/test-runner.js` | Rebranded JSDoc header and console.log output |
| `README.md` | Rebranded all 5 occurrences of ParseMaster to PageForge |

### Phase 1 — Global Rebranding (ParseMaster → PageForge)

All case variations of "ParseMaster" replaced across the entire codebase (excluding CLAUDE.md which was updated separately):

| Variation | Replacement | Example Locations |
|-----------|-------------|-------------------|
| `ParseMaster` (PascalCase) | `PageForge` | JSDoc headers, comments, string literals |
| `parsemaster` (lowercase) | `pageforge` | Not found in codebase |
| `PARSEMASTER` (uppercase) | `PAGEFORGE` | Not found in codebase |
| `parse-master` (kebab-case) | `page-forge` | Not found in codebase |
| `parse_master` (snake_case) | `page_forge` | Not found in codebase |
| `Parse Master` (Title Case) | `Page Forge` | Not found in codebase |
| `ParseMaster_output` (in filenames) | `PageForge_output` | js/app.js fallback filename |

**19 total occurrences** found and replaced across 11 files. Post-replacement grep verification confirmed zero remaining occurrences.

### Phase 2 — Homepage UI Modifications

#### Change 1 — Remove "Why PageForge?" Section
- **Previous:** Collapsible `<details class="about-section">` block below the template selector explaining what the tool does and why it exists
- **Fix:** Removed the entire `<details>` element from `index.html`; removed all associated CSS styles (`.about-section`, `.about-toggle`, `.about-text`, `.about-text h3`, `.about-text ul`, `.about-text li`)

#### Change 2 — Decouple Upload from Automatic Conversion (Staged Upload)
- **Previous:** Dropping a `.docx` file immediately triggered the full parsing and conversion pipeline via `handleFile()`
- **Fix:** File drop/selection now calls `stageFile(file)` which:
  1. Validates `.docx` extension
  2. Stores file as `this.stagedFile` (no processing)
  3. Shows staged file indicator with filename (`#staged-file-info`)
  4. Extracts module code from filename for auto-detection
  5. Runs `_autoDetectTemplate()` if module code found (stores internally, shows hint)
  6. Enables the Convert button
  7. Updates drop zone text to "File staged — click to change"
- **New properties:** `this.stagedFile`, `this.autoDetectedTemplate`, `this.userManuallySelectedTemplate`

#### Change 3 — New "Convert Document" Button
- **Previous:** Conversion was automatic on file drop
- **Fix:** Added `<button id="btn-convert" class="btn btn-convert" disabled>Convert Document</button>` to `index.html`; button starts disabled, enabled by `stageFile()`, triggers `convertDocument()` on click; `convertDocument()` contains the full pipeline logic previously in `handleFile()` (parse → format → unwrap → normalise → scope → assign pages → convert HTML → store output → display results)

#### Change 4 — Template Selection Logic Update
- **Previous:** Auto-detection changed the dropdown selection and showed "Auto-detected" label
- **Fix:** Auto-detected template stored internally (`this.autoDetectedTemplate`) without changing dropdown; hint text ("Auto-detected: Template Name") shown on staged file indicator; manual dropdown selection sets `this.userManuallySelectedTemplate = true`; `_getResolvedTemplateId()` resolves template with priority: manual selection > auto-detected > null; dropdown placeholder text changed to "Select template (auto-detected on upload)"

### Phase 3 — Post-Processing UI & Results Screen Adjustments

#### Change 5 — Consolidate Summary Data into Debug Section
- **Previous:** Conversion summary panel (`#conversion-summary`) displayed as a visible section above the file list with pages generated, template used, interactive count, tags processed, and warnings
- **Fix:** Removed `#conversion-summary` div from HTML; removed CSS styles (`.conversion-summary`, `.summary-item`, `.summary-label`, `.summary-value`); added `_renderDebugConversionSummary()` method in `app.js` that renders the same stats as the first sub-section within the collapsible debug panel; `_renderDebugPanel()` calls this method before template config and tag analysis sections

#### Change 6 — Replace "Legacy Text Output" with Direct Download Button
- **Previous:** "Legacy Text Output" button toggled a full-screen legacy output panel (`#legacy-output-panel`) with textarea, Copy All, Download .txt, and Back to HTML buttons; required `_showLegacyMode()` and `_hideLegacyMode()` methods
- **Fix:** Removed `#legacy-output-panel` from HTML; removed all legacy mode CSS (`.legacy-output-panel` and its textarea); removed `_showLegacyMode()`, `_hideLegacyMode()`, and related event listeners; added `<button id="btn-download-text">&#128196; Download Text Template</button>` to action bar; new `_handleDownloadText()` method creates a Blob from `this.formattedOutput` and triggers a direct browser download as `.txt` file; filename uses module code if available, falls back to `PageForge_output.txt`

#### Change 7 — Remove "Copy Interactive Reference" Button
- **Previous:** `#btn-copy-reference` in the global action bar called `OutputManager.copyToClipboard()` for the interactive reference document
- **Fix:** Removed button from HTML; removed event listener and `_handleCopyReference()` method from `app.js`; interactive reference document remains accessible via per-file Copy button in the file list panel (OutputManager's `copyToClipboard()` method preserved for per-file use)

---

## 20. CALIBRATION COMPARISON TOOL (Phase 9)

### Overview

Phase 9 adds a **Calibration Comparison Tool** — a development/testing utility that allows uploading human-developed HTML reference files, then logging side-by-side comparison snapshots between the original Writer Template content, PageForge's generated output, and the human developer's correct output. These logged snapshots are exportable as a structured text document designed to be fed into Claude AI for analysis and code recalibration guidance. All existing functionality from all previous phases remains working — 407 pre-existing tests continue to pass with zero modifications.

**Status:** DONE — New `CalibrationManager` class created, integrated with `App`, 407 tests passing (no new tests required — all changes are UI/interaction with no algorithmic logic to unit test).

### Files Created

| File | Purpose |
|------|---------|
| `js/calibration-manager.js` | New class — handles human reference file upload, comparison snapshot logging, snapshot list display, calibration report generation/export/clipboard copy |

### Files Modified

| File | Changes |
|------|---------|
| `index.html` | Added `#calibration-section` with full calibration panel HTML (`<details>` element containing upload dropzone, snapshot form with 4 fields + source file dropdown, logged snapshots list, export controls); added `<script src="js/calibration-manager.js">` before `app.js` |
| `css/styles.css` | Added complete calibration panel styles: `.calibration-panel`, `.calibration-toggle`, `.calibration-content`, `.calibration-description`, `.calibration-dropzone` (with hover/drag-over states), `.calibration-uploaded-files`, `.calibration-file-item` (with `-name`, `-size`, `-matched`, `-unmatched`, `-remove` variants), `.snapshot-form`, `.snapshot-field` (with label, textarea, inline, select variants), `.field-hint`, `.snapshot-actions`, `.snapshot-count`, `.snapshot-list`, `.snapshot-empty-state`, `.snapshot-entry` (with `-header`, `-number`, `-file`, `-time` variants), `.snapshot-delete`, `.snapshot-preview-text`, `.snapshot-entry-details`, `.snapshot-full-content`, `.snapshot-full-field` (with `pre` and `strong`), `.export-actions`; added responsive rules for snapshot-field-inline, snapshot-actions, export-actions at 768px breakpoint |
| `js/app.js` | Added `this.calibrationSection` DOM reference in `_bindElements()`; added `_initCalibrationManager()` method that instantiates `CalibrationManager` with callback hooks (`showToast`, `getModuleCode`, `getTemplateName`, `getGeneratedFileList`); called from constructor after `_initTemplateEngine()`; `showResults()` now shows `#calibration-section` and calls `calibrationManager.populateSourceFileDropdown()`; `reset()` now calls `calibrationManager.reset()` and hides `#calibration-section` |

### Architecture

The Calibration Comparison Tool is implemented as a separate `CalibrationManager` class (`js/calibration-manager.js`) following the project's modular architecture. It is instantiated by `CalibrateApp` on the standalone `calibrate.html` page (Phase 10), with callback hooks for `showToast`, `getModuleCode`, `getTemplateName`, and `getGeneratedFileList`.

**Integration points (Phase 10):**
- `CalibrateApp` constructor → instantiates `CalibrationManager` with callback hooks from deserialized sessionStorage data
- `CalibrateApp._initCalibrationManager()` → calls `init()` and `populateSourceFileDropdown()`
- `CalibrateApp._populateFromSessionStorage()` → reads sessionStorage keys set by review page's copy buttons, populates form fields, triggers `_updateLogButtonState()`

**Data flow:**
- Human reference files stored in `CalibrationManager.humanReferenceFiles[]` as `{ filename, content, size, matchedToGenerated }` objects
- Comparison snapshots stored in `CalibrationManager.calibrationSnapshots[]` as `{ id, timestamp, sourceFile, originalContent, pageforgeOutput, humanOutput, notes }` objects
- All data is ephemeral — cleared on reset/reload (privacy model maintained)

### CalibrationManager Class Details

**Constructor options (callback hooks from App):**
- `showToast(msg)` — displays toast notifications via App's existing toast system
- `getModuleCode()` — returns current module code from App's parsed metadata
- `getTemplateName()` — returns current template name from App's resolved template config
- `getGeneratedFileList()` — returns array of generated filenames from App

**Public API:**
- `init()` — binds DOM elements and wires up event listeners (called once after HTML is in DOM)
- `populateSourceFileDropdown()` — populates the source file `<select>` from generated file list
- `reset()` — clears all data (reference files, snapshots), resets UI, collapses panel

**Internal methods:**
- `_handleReferenceFiles(files)` — validates `.html` extension, prevents duplicates, reads content via `FileReader`, detects filename match against generated files
- `_renderUploadedFiles()` — renders uploaded file list with filename, size, matched/unmatched status, and remove buttons
- `_removeReferenceFile(index)` — removes a reference file by index with toast notification
- `_updateLogButtonState()` — enables/disables Log Snapshot button based on required field content
- `_logSnapshot()` — creates snapshot object, adds to array, clears form, updates display + export buttons, shows toast
- `_clearForm()` — resets all form fields without logging
- `_renderSnapshotList()` — renders chronological list of snapshot cards with expand/delete; updates count badge
- `_deleteSnapshot(id)` — deletes a snapshot by ID after `confirm()` dialog
- `_updateExportButtonState()` — enables/disables export/copy buttons based on snapshot count
- `_generateReport()` — generates structured plain text calibration report with header, context notes, and all snapshots
- `_exportReport()` — generates report and triggers browser download as `.txt` file
- `_copyReport()` — generates report and copies to clipboard (modern API with `execCommand` fallback)
- `_fallbackCopy(text)` — clipboard fallback using hidden textarea + `execCommand('copy')`
- `_clearAllSnapshots()` — clears all snapshots after `confirm()` dialog
- `_formatFileSize(bytes)` — formats bytes to human-readable string (B, KB, MB)
- `_formatTime(isoString)` — formats ISO timestamp to HH:MM
- `_truncate(str, maxLen)` — truncates string with ellipsis
- `_escapeHtml(str)` — escapes HTML special characters for safe rendering

### Calibration Report Format

The exported report follows this structure:

```
==========================================
PAGEFORGE CALIBRATION REPORT
==========================================
Module: {moduleCode}
Template: {templateName}
Generated: {date/time}
Total Snapshots: {count}

IMPORTANT CONTEXT FOR ANALYSIS:
- The "Original Content" shows raw parsed text from the Writer Template
  document BEFORE PageForge attempted to convert it.
- The "PageForge Output" shows what the current algorithm actually produced.
- The "Human Output" shows what a human developer correctly produced —
  this is the TARGET that PageForge should aim to replicate.
- Note: The human reference files may have text content differences from
  the Writer Template due to post-production edits made directly to the
  HTML files (not reflected back in the Writer Template).
- Note: Writer comments/instructions (red text) in the Writer Template
  may not appear in the human HTML files, as they served only as
  development guidance.

==========================================

------------------------------------------
SNAPSHOT 1 of {total}
------------------------------------------
Source File: {sourceFile or "Not specified"}
Logged: {timestamp}

--- ORIGINAL WRITER TEMPLATE CONTENT ---
{originalContent}

--- PAGEFORGE GENERATED OUTPUT ---
{pageforgeOutput}

--- HUMAN DEVELOPER CORRECT OUTPUT ---
{humanOutput}

--- NOTES ---
{notes or "No notes provided."}

------------------------------------------
...
==========================================
END OF CALIBRATION REPORT
==========================================
```

### UI Layout

**Phase 10 change:** The calibration tool has been relocated from the main page (`#calibration-section`) to a standalone page (`calibrate.html`), with Step 1 (Upload Human Reference Files) removed and the remaining steps renumbered. The review page (`review.html`) provides "Copy to Snapshot" buttons that save content to sessionStorage keys, and a "Conversion Error Log" button (renamed from "Calibration Tool" in Phase 11) that opens `calibrate.html` in a new tab. `CalibrateApp` auto-populates the form fields from those sessionStorage keys on page load and on tab focus. See Section 21 for the review page details and Section 22 for the standalone calibration page details.

The Conversion Error Log (formerly "calibration tool") is now a standalone page (`calibrate.html`):

```
calibrate.html
  ├── .calibrate-header (back link, title, module code badge)
  └── .calibrate-content
      └── .calibration-panel
          └── .calibration-content
              ├── Step 1: Log Comparison Snapshots (was Step 2)
              │   └── .snapshot-form (4 fields + dropdown + buttons)
              ├── Logged Snapshots
              │   └── #snapshot-list (snapshot cards)
              └── Step 2: Export Calibration Report (was Step 3)
                  └── .export-actions (export + copy + clear buttons)
```

### Important Caveats (Documented in Code Comments)

1. **Content differences are expected:** The human reference HTML files may contain text that differs from both the Writer Template and PageForge's output, because the human developer may have received direct feedback and made edits to the final HTML without updating the Writer Template.
2. **Writer comments won't be in human files:** Red text / writer instructions in the Writer Template are development guidance only — they will not appear in the human-developed HTML files.
3. **This is a development tool:** The calibration panel is for internal algorithm refinement, not for end-user consumption.
4. **Organisation-neutral:** No organisation names appear in the calibration tool's UI, labels, or code comments. Content within snapshots naturally preserves whatever text appears in the source documents.

---

## 21. VISUAL COMPARISON REVIEW PAGE (Phase 10)

### Overview

Phase 10 provides a dedicated **Visual Comparison Review** page (`review.html`) with three synchronised viewing panels, template-aware CSS injection for authentic LMS rendering, a 6-tier intelligent content matching algorithm for cross-panel synchronisation, and "Copy to Snapshot" buttons that save content to sessionStorage for consumption by the standalone Conversion Error Log page (`calibrate.html`). The Calibration Comparison Tool has been extracted from the review page into its own standalone page (see Section 22), renamed to "Conversion Error Log" in Phase 11. A "Visual Comparison Review" button on the main results page launches the review page in a new tab after serialising all necessary data to sessionStorage. Phase 11 added proportional scroll sync, Raw HTML scroll-position preservation, toolbar relocation, and the Conversion Error Log rename.

**Status:** DONE — 4 files created (review.html, calibrate.html, js/review-app.js, js/calibrate-app.js), 1 file created earlier (css/review-styles.css), 2 files modified (js/app.js, css/review-styles.css), 479 tests passing (72 tests in reviewPageChanges.test.js covering Phase 11 toolbar/rename/scroll changes and Phase 12 per-panel Sync buttons).

### Files Created

| File | Purpose |
|------|---------|
| `review.html` | Standalone HTML page for the Visual Comparison Review tool — header bar with back link/title/module code, separate toolbar row with Raw HTML button/Conversion Error Log button, three-panel layout with file map and per-panel Sync buttons, template-aware CSS-injected PageForge/Human Reference iframes, Writer Template content panel, "Copy to Snapshot" buttons saving to sessionStorage |
| `js/review-app.js` | Controller class for the review page — data deserialisation from sessionStorage, template-aware CSS injection for iframe rendering, per-panel one-shot Sync buttons with cross-panel textual-anchor matching (tiered fallback: exact → fuzzy → proportional), raw HTML toggle with scroll-position preservation via textual-anchor matching, human reference file upload, copy-to-sessionStorage snapshot buttons, conversion error log launcher |
| `css/review-styles.css` | Review page-specific styles — three-panel flex layout, toolbar row, file map sidebar, per-panel sync button styles with pulse/flash feedback, raw HTML view, writer block styling, conversion error log button, responsive breakpoints |
| `calibrate.html` | Standalone Conversion Error Log page — snapshot form with 3 required fields + 1 optional + source file dropdown, logged snapshots display, export/copy/clear controls (see Section 22) |
| `js/calibrate-app.js` | Controller class for the Conversion Error Log page — data deserialisation from sessionStorage, CalibrationManager instantiation, auto-population of form fields from sessionStorage keys set by review page's copy buttons (see Section 22) |

### Files Modified

| File | Changes |
|------|---------|
| `review.html` | Removed entire `#review-calibration-section` with embedded calibration tool HTML; removed `<script src="js/calibration-manager.js">`; added `#btn-calibration-tool` button in header right side; changed copy button IDs to `btn-copy-pf`, `btn-copy-human`, `btn-copy-wt` with text "Copy PF", "Copy Human", "Copy WT"; title changed to "PageForge Visual Comparison Review"; only loads `js/review-app.js` |
| `js/review-app.js` | Major rewrite: added `CSS_MAPPING` constant with 8 template CSS URL mappings; added `_injectCssForRendering()` for template-aware iframe styling; added `_openCalibrationTool()` for calibrate.html launch; enhanced `_annotateHtml()` with `data-pf-activity`, `data-pf-inner`, and structural element annotation; replaced `_syncHumanPanel()` with 6-tier `_syncHumanPanelIntelligent()`; added tier helper methods (`_findStructuralId`, `_extractActivityNumber`, `_extractHeadingText`, `_extractWordGroups`, `_findByWordGroups`); changed `_copyToSessionStorage()` to save to sessionStorage keys instead of form fields; removed CalibrationManager dependency entirely |
| `js/app.js` | Added `templateAttribute` extraction (`config._templateAttribute`) and inclusion in serialised JSON for `_serialiseForReview()` |
| `css/review-styles.css` | Added `.review-calibrate-btn` styles; changed file map width from 190px to 180px; added `.file-map-entry-row` for horizontal layout; removed `.review-calibration-section` styles |

### Architecture

The Visual Comparison Review page is a standalone HTML page (`review.html`) that loads its own controller class (`ReviewApp` in `js/review-app.js`). It does not depend on the main page's `App` class, `DocxParser`, `CalibrationManager`, or any other main-page class — it receives all data via sessionStorage.

**Data transfer flow (main page → review page):**
1. User clicks "Visual Comparison Review" button on main results page
2. `App._serialiseForReview()` serialises all data to JSON string (including `templateAttribute`)
3. JSON stored in sessionStorage key `pageforge_review_data` (or chunked for large payloads)
4. `window.open('review.html')` opens the review page in a new tab
5. `ReviewApp._loadData()` reads and parses data from sessionStorage
6. Review page renders with all panels populated, CSS injection applied to iframes

**Data transfer flow (review page → calibrate page):**
1. User clicks "Copy PF" / "Copy Human" / "Copy WT" buttons after sync-clicking a block
2. `_copyToSessionStorage(type)` saves content to `pageforge_snapshot_pf` / `pageforge_snapshot_human` / `pageforge_snapshot_wt` + `pageforge_snapshot_file` in sessionStorage
3. User clicks "Conversion Error Log" button in review page toolbar
4. `_openConversionErrorLog()` serialises `{generatedFileList, metadata, templateName}` to `pageforge_calibrate_data` and opens `calibrate.html`
5. `CalibrateApp._populateFromSessionStorage()` reads snapshot keys and populates form fields
6. `window.addEventListener('focus', ...)` re-checks sessionStorage keys on tab focus for subsequent copies

**Privacy model maintained:** sessionStorage is ephemeral (cleared on tab close), tab-scoped, and client-side only. No data is uploaded or stored persistently.

### Data Serialisation

The `App._serialiseForReview()` method serialises:

```javascript
{
    generatedHtmlFiles: {},      // filename → HTML content map
    generatedFileList: [],       // ordered array of filenames
    metadata: {},                // moduleCode, subject, course, writer, date
    templateId: '',              // selected template ID
    templateName: '',            // resolved template display name
    templateAttribute: '',       // template attribute value (e.g., '4-6', '9-10', 'NCEA') for CSS injection
    humanReferenceFiles: [],     // empty array (upload handled on review page)
    pageData: [                  // per-page content block texts
        {
            filename: 'MODULE-00.html',
            type: 'overview',
            lessonNumber: null,
            contentBlockTexts: ['block text 0', 'block text 1', ...]
        },
        ...
    ]
}
```

**Chunked storage fallback:** If the JSON string exceeds 4MB, `_storeChunked()` splits it into 4MB chunks stored as `pageforge_review_chunk_0`, `pageforge_review_chunk_1`, etc., with a `pageforge_review_chunks` key storing the count. `ReviewApp._loadData()` automatically detects and reassembles chunked data.

### Template-Aware CSS Injection

The `CSS_MAPPING` constant at the top of `review-app.js` maps template attribute values to arrays of external LMS stylesheet URLs. When loading HTML into iframes (both PageForge and Human Reference panels), `_injectCssForRendering()`:

1. Detects the `template="..."` attribute from the HTML's `<html>` tag
2. Looks up the matching stylesheet URLs from `CSS_MAPPING`
3. Builds `<link rel="stylesheet">` tags for each URL
4. Injects them before `</head>` in the HTML string
5. Removes the `idoc_scripts.js` `<script>` tag (prevents script execution in sandbox)
6. Adds the `.pf-sync-highlight` style for content highlight annotations

**Supported template mappings:**

| Template Attribute | CSS Source |
|-------------------|------------|
| `1-3` | tekuradev colour schemes + 1-3 colours + shared styles |
| `4-6` | tekura colour schemes + 4-6 colours + shared styles |
| `7-8` | tekura colour schemes + 7-8 colours + shared styles |
| `9-10` | tekura colour schemes + 9-10 colours + shared styles |
| `NCEA` | tekuradev colour schemes + NCEA colours + shared styles |
| `combo` | tekuradev + tekura colour schemes + combo colours + shared styles |
| `ECH` | tekura colour schemes + ECH colours + shared styles |
| `inquiry` | tekura colour schemes + inquiry colours + shared styles |

This ensures that rendered HTML in the comparison iframes looks exactly as it would in the D2L/Brightspace LMS, with correct colour schemes, typography, and layout.

### ReviewApp Class Details

**Constructor flow:**
1. `_loadData()` — reads and parses sessionStorage data
2. `_bindElements()` — caches all DOM references
3. `_bindEvents()` — wires up sync toggle, raw HTML button, file upload, copy-to-sessionStorage buttons, conversion error log button, iframe click handlers
4. `_render()` — renders file map, reference file list, auto-selects first file

**Public API:**
- `showToast(message)` — displays toast notification

**Internal methods:**
- `_loadData()` — loads and parses serialised data from sessionStorage (supports chunked storage)
- `_render()` — initial rendering of all panels
- `_renderFileMap()` — renders the file map sidebar with generated filenames, page types, and reference badges
- `_selectFile(filename)` — selects a file, updates all three panels simultaneously
- `_loadPageforgePanel(filename)` — loads annotated and CSS-injected HTML into PageForge iframe (or raw view)
- `_loadHumanPanel(filename)` — loads matching reference file (CSS-injected) into Human iframe, or shows upload prompt
- `_loadWriterPanel(filename)` — renders formatted content block texts for the selected page
- `_injectCssForRendering(htmlString, templateAttribute)` — detects template from `<html template="...">`, builds `<link>` tags from `CSS_MAPPING`, injects before `</head>`, removes `idoc_scripts.js`, adds highlight annotation style
- `_annotateHtml(htmlContent, filename)` — post-processes generated HTML: adds `data-pf-block` attributes to `<div id="body">` children, adds `data-pf-activity` from `.activity[number]` elements and HTML comments, adds `data-pf-inner` to inner elements (h2-h5, p, ul, ol, etc.), annotates structural elements (#header, #footer, #module-menu-content); uses DOMParser
- `_onSyncClick(sourcePanel)` — handles per-panel Sync button click: extracts textual anchor from source panel's viewport, scrolls other two panels to matching content via `_syncPanelToAnchor()`, applies visual feedback (button pulse + target panel flash), shows toast; no ongoing scroll-coupling created
- `_syncPanelToAnchor(panel, anchorText, fallbackFraction)` — scrolls a single target panel to content matching a textual anchor; delegates to `_scrollWriterToAnchor`, `_scrollRawViewToAnchor`, or `_scrollIframeToAnchor` depending on panel type and current view mode (rendered vs raw HTML)
- `_panelDisplayName(panel)` — returns human-readable display name for a panel identifier
- `static normaliseTextForMatch(text)` — reusable text normalisation: strips HTML tags, decodes entities, lowercases, removes punctuation (preserves macrons), collapses whitespace; used by Sync buttons and Raw HTML scroll-position preservation
- `_extractVisibleAnchor(panel)` — extracts a textual anchor (normalised text snippet + scroll fraction) from the element currently at the top of the visible area in a panel; works for rendered iframes, raw HTML views, and writer blocks
- `_extractAnchorFromRawView(rawViewContainer)` — extracts anchor text from the line currently visible at the top of a raw HTML `<pre><code>` view
- `_scrollRawViewToAnchor(rawViewContainer, anchorText, fallbackFraction)` — searches raw HTML lines for anchor text using word-level fuzzy matching (30% threshold); falls back to proportional scroll
- `_scrollIframeToAnchor(iframe, anchorText, fallbackFraction)` — searches rendered iframe elements for anchor text using word-level fuzzy matching; falls back to proportional scroll
- `_scrollWriterToAnchor(anchorText, fallbackFraction)` — searches writer blocks for anchor text using word-level fuzzy matching; falls back to proportional scroll
- `_toggleRawHtmlMode()` — extracts visible anchor BEFORE switching views, toggles rendered/raw mode, restores scroll position using `_restoreScrollFromAnchor()` after rendering completes via `requestAnimationFrame`
- `_restoreScrollFromAnchor(anchor)` — after view toggle, scrolls all three panels to the textual anchor position; handles iframe load timing via event listeners with timeout fallback
- `_showRawHtml(panel, htmlContent)` — displays raw HTML in a panel's raw view container
- `_showCopyToSnapshotButtons()` / `_hideCopyToSnapshotButtons()` — toggle contextual copy buttons on panel headers
- `_copyToSessionStorage(type)` — saves highlighted block content to sessionStorage keys (`pageforge_snapshot_pf`, `pageforge_snapshot_human`, `pageforge_snapshot_wt`, `pageforge_snapshot_file`) for the standalone Conversion Error Log page
- `_getHighlightedHtml(iframe, blockIndex)` — extracts outerHTML of highlighted element in iframe
- `_openConversionErrorLog()` — serialises calibration data to `pageforge_calibrate_data` sessionStorage key and opens `calibrate.html` in a new tab
- `_handleReferenceFiles(files)` — validates/reads uploaded .html reference files, stores in `this.humanReferenceFiles`
- `_renderRefFileList()` — renders uploaded reference file list with matched/unmatched status and remove buttons
- `_getPageData(filename)` — looks up page data for a filename
- `_findReference(filename)` / `_hasMatchingReference(filename)` — reference file lookup helpers

### Three-Panel Layout

```
┌─────────────┬──────────────────┬───────────────────┬───────────────────┐
│  FILE MAP   │  PAGEFORGE HTML  │  HUMAN REFERENCE  │  WRITER TEMPLATE  │
│  (sidebar)  │  (iframe)        │  (iframe/upload)   │  (div content)    │
│  ~180px     │  flex: 1         │  flex: 1           │  flex: 1          │
│             │                  │                   │                   │
│  file-00    │  Sandboxed       │  Sandboxed         │  Scrollable div   │
│  file-01    │  iframe with     │  iframe with       │  with formatted   │
│  file-02    │  CSS-injected    │  CSS-injected      │  text blocks,     │
│  ...        │  srcdoc +        │  srcdoc            │  data-block-index │
│             │  data-pf-block   │  (or upload zone)  │  attributes       │
│             │  annotations     │                   │                   │
└─────────────┴──────────────────┴───────────────────┴───────────────────┘
```

**File Map Panel:** Fixed-width sidebar (~180px) with clickable file entries. Each entry shows filename and page type in a horizontal row layout (`.file-map-entry-row`), with a green "REF" badge if a matching human reference file has been uploaded. Currently selected file is highlighted with a blue left border.

**PageForge HTML Panel:** Uses a sandboxed `<iframe>` with `sandbox="allow-same-origin"` and `srcdoc` to render the generated HTML. The HTML is annotated with `data-pf-block`, `data-pf-activity`, and `data-pf-inner` attributes. Template-aware CSS is injected for authentic LMS rendering. Panel header includes a "Sync" button (one-shot align trigger) and a "Copy PF" button for snapshot export.

**Human Reference Panel:** Also uses a sandboxed `<iframe>` with `srcdoc` and template-aware CSS injection. Initially shows an upload prompt (drag-and-drop zone + file picker). Once reference files are uploaded, displays the matching file in the iframe or a "no matching file" message. Panel header includes a "Sync" button (one-shot align trigger), an "Upload more files" button, and a "Copy Human" button for snapshot export.

**Writer Template Panel:** A scrollable `<div>` containing formatted text representations of each content block. Each block is wrapped in a `<div class="writer-block" data-block-index="N">` with a block index badge and monospace `<pre>` content. Alternating backgrounds distinguish blocks. Panel header includes a "Sync" button (one-shot align trigger) and a "Copy WT" button for snapshot export.

### Per-Panel Sync Buttons (One-Shot Align Trigger)

**Buttons:** Three identical "⇄ Sync" buttons, one in each panel's header bar (PageForge Output, Human Reference, Writer Template). Each button is a one-shot action — not a toggle. No continuous scroll-coupling is created.

**Sync click flow:**
1. User clicks the Sync button on any panel (the "source" panel)
2. `_onSyncClick(sourcePanel)` extracts a textual anchor from the source panel's current viewport position using `_extractVisibleAnchor()`
3. The source panel does NOT move
4. The other two panels are scrolled to the best-matching content using `_syncPanelToAnchor()` with tiered fallback:
   - **Exact normalised match:** Anchor text word-level matching with 30% minimum threshold
   - **Fuzzy word match:** Searches all text-bearing elements (h1-h5, p, li, td, th, div) for word overlap
   - **Proportional scroll:** Falls back to scroll-percentage mapping if no textual match found
5. Visual feedback: clicked button pulses briefly (`.review-sync-btn-pulse`), target panels flash briefly (`.review-panel-sync-flash`)
6. Toast notification shows which panel was the source (e.g., "Synced from Writer Template")
7. After the jump, all panels are fully independent — no ongoing coupling

**Cross-view-mode compatibility:** The matching logic works regardless of each panel's current view mode (rendered iframe or Raw HTML). Source anchor extraction and target scrolling both handle rendered elements and raw text lines.

**Concrete example:** If the user scrolls the Writer Template panel to show a specific heading, then clicks the Writer Template's Sync button, the PageForge Output panel and Human Reference panel both jump to the corresponding heading (or nearest content) within their respective views. The Writer Template panel stays where it is.

### Raw HTML Mode

**Toggle button:** `</> Raw HTML` button in the header bar. Toggles between rendered and raw views for both PageForge and Human Reference panels simultaneously. Button text changes to "Rendered" when in raw mode.

**Raw HTML view:** Replaces iframe content with a `<pre><code>` block showing the raw HTML source in a dark-themed monospace view (background: #1e1e2e, text: #cdd6f4). Writer Template panel remains unchanged (already shows text content).

**Sync + Raw HTML interaction:** Per-panel Sync buttons work in both rendered and raw HTML views. The textual-anchor matching operates on raw text lines (for raw view) or rendered DOM elements (for iframe view), and handles mixed-mode scenarios where the source and target panels are in different view modes.

### Copy-to-Snapshot Buttons (sessionStorage-Based)

The Copy-to-Snapshot buttons are available in each panel header:
- **"Copy WT" button** (Writer Template panel header) — saves the formatted text content to `sessionStorage.setItem('pageforge_snapshot_wt', content)` and the current filename to `sessionStorage.setItem('pageforge_snapshot_file', filename)`
- **"Copy PF" button** (PageForge panel header) — saves the outerHTML of the highlighted element to `sessionStorage.setItem('pageforge_snapshot_pf', content)` and the current filename to `pageforge_snapshot_file`
- **"Copy Human" button** (Human Reference panel header, if reference file loaded) — saves the outerHTML of the highlighted element to `sessionStorage.setItem('pageforge_snapshot_human', content)` and the current filename to `pageforge_snapshot_file`

Each button shows a toast notification on click.

The standalone Calibration page (`calibrate.html`) reads these sessionStorage keys on load and on tab focus, auto-populating the snapshot form fields. This enables a workflow where the user copies content on the review page, switches to the calibration tab, and sees the fields pre-populated.

### Conversion Error Log Integration

The review page no longer embeds the Calibration Comparison Tool directly. Instead:

**Removed from review page:**
- `#review-calibration-section` element removed from `review.html`
- `<script src="js/calibration-manager.js">` removed from `review.html`
- `CalibrationManager` no longer instantiated by `ReviewApp`

**Added to review page (Phase 10, updated Phase 11):**
- "Conversion Error Log" button (`#btn-calibration-tool`) in the toolbar row (relocated from header in Phase 11)
- `_openConversionErrorLog()` method serialises `{generatedFileList, metadata, templateName}` to `sessionStorage.setItem('pageforge_calibrate_data', ...)` and opens `calibrate.html` via `window.open()`

**Standalone Conversion Error Log page:** See Section 22 for full details on `calibrate.html` and `CalibrateApp`.

### User Workflow

1. User uploads a Writer Template `.docx` on the main PageForge page and clicks "Convert Document"
2. PageForge processes the document and shows results (file list, preview, etc.)
3. User clicks the "Visual Comparison Review" button in the actions bar
4. Data is serialised to sessionStorage (including `templateAttribute`); a new tab opens with `review.html`
5. Review page loads showing file map (left), PageForge output with authentic LMS styling (centre-left), upload prompt (centre-right), Writer Template content (right)
6. User uploads human-developed HTML files via the Human Reference panel's upload zone
7. User clicks through pages in the file map — all three panels update simultaneously with CSS-injected rendering
8. User clicks the Sync button on any panel — the other two panels automatically jump to the corresponding content position using textual-anchor matching (with proportional fallback); no ongoing scroll-coupling is created
9. User clicks Raw HTML to see the source code behind the rendered views — all three panels automatically scroll to preserve the user's current viewing position using textual-anchor matching (with proportional fallback)
10. User clicks "Copy PF" / "Copy Human" / "Copy WT" buttons — content is saved to sessionStorage keys
12. User clicks "Conversion Error Log" button in toolbar — `calibrate.html` opens in a new tab
13. Conversion Error Log page auto-populates form fields from sessionStorage keys
14. User logs snapshots and exports the calibration report for Claude AI analysis
15. User can switch back to the review tab, copy more content, switch to Conversion Error Log tab — form fields auto-populate on tab focus

---

## 22. STANDALONE CALIBRATION PAGE (Phase 10)

### Overview

Phase 10 extracts the Calibration Comparison Tool from the review page into a standalone page (`calibrate.html`) managed by a new `CalibrateApp` controller class. Phase 11 renamed the page from "Calibration Comparison Tool" to "Conversion Error Log" to better reflect its purpose of documenting conversion algorithm discrepancies. The page receives data via sessionStorage from the review page and auto-populates snapshot form fields from sessionStorage keys set by the review page's "Copy to Snapshot" buttons.

**Status:** DONE — 2 new files created (calibrate.html, js/calibrate-app.js), 479 tests passing (72 tests in reviewPageChanges.test.js covering Phase 11+12 changes).

### Files Created

| File | Purpose |
|------|---------|
| `calibrate.html` | Standalone Conversion Error Log page — header bar with back link and module code badge, page title "Conversion Error Log", snapshot form (Step 1), logged snapshots display, export controls (Step 2) |
| `js/calibrate-app.js` | Controller class — data loading from `pageforge_calibrate_data` sessionStorage key, CalibrationManager instantiation with callback hooks, auto-population from sessionStorage snapshot keys on load and focus |

### Architecture

The Conversion Error Log page is a standalone HTML page (`calibrate.html`) that loads `CalibrationManager` (shared class) and its own `CalibrateApp` controller. It does not depend on `App`, `ReviewApp`, `DocxParser`, or any other class — it receives all data via sessionStorage.

**SessionStorage keys consumed:**

| Key | Source | Purpose |
|-----|--------|---------|
| `pageforge_calibrate_data` | `ReviewApp._openConversionErrorLog()` | JSON with `generatedFileList`, `metadata`, `templateName` — used for source file dropdown population and module code display |
| `pageforge_snapshot_wt` | `ReviewApp._copyToSessionStorage('wt')` | Writer Template content — auto-populates "Original Content" textarea |
| `pageforge_snapshot_pf` | `ReviewApp._copyToSessionStorage('pf')` | PageForge output — auto-populates "PageForge Generated Output" textarea |
| `pageforge_snapshot_human` | `ReviewApp._copyToSessionStorage('human')` | Human reference output — auto-populates "Human Developer Correct Output" textarea |
| `pageforge_snapshot_file` | `ReviewApp._copyToSessionStorage(any)` | Current filename — auto-selects matching option in source file dropdown |

Snapshot keys are read-once: `CalibrateApp._populateFromSessionStorage()` reads each key and then immediately calls `sessionStorage.removeItem()` to clear it, preventing stale data on subsequent tab focuses.

### CalibrateApp Class Details

**Constructor flow:**
1. `_loadData()` — reads and parses `pageforge_calibrate_data` from sessionStorage
2. `_bindElements()` — caches DOM references (module code display, back button, toast)
3. `_initCalibrationManager()` — instantiates `CalibrationManager` with callback hooks (`showToast`, `getModuleCode`, `getTemplateName`, `getGeneratedFileList`); calls `init()` and `populateSourceFileDropdown()`; shows module code badge if available
4. `_bindEvents()` — back button handler (tries `window.close()`, falls back to `review.html`); `window.addEventListener('focus', ...)` handler for auto-population
5. `_populateFromSessionStorage()` — reads all snapshot sessionStorage keys, populates form fields, auto-selects source file, clears keys, triggers `_updateLogButtonState()`

**Public API:**
- `showToast(message)` — displays toast notification with 3-second auto-dismiss

### Page Layout

```
calibrate.html
  ├── .calibrate-header
  │   └── .calibrate-header-inner
  │       ├── #btn-back (← Back to Visual Review)
  │       ├── h1.calibrate-title (Conversion Error Log)
  │       └── #calibrate-module-code (module code badge, hidden by default)
  └── .calibrate-content
      └── .calibration-panel
          └── .calibration-content
              ├── Step 1: Log Comparison Snapshots
              │   └── .snapshot-form
              │       ├── #snapshot-original (textarea — field 1, required)
              │       ├── #snapshot-pageforge (textarea — field 2, required)
              │       ├── #snapshot-human (textarea — field 3, required)
              │       ├── #snapshot-notes (textarea — field 4, optional)
              │       ├── #snapshot-source-file (select dropdown)
              │       └── .snapshot-actions (#btn-log-snapshot + #btn-clear-snapshot-form)
              ├── Logged Snapshots
              │   └── #snapshot-list (snapshot cards with expand/delete)
              └── Step 2: Export Calibration Report
                  └── .export-actions (#btn-export-calibration + #btn-copy-calibration + #btn-clear-all-snapshots)
```

The page uses inline `<style>` for page-specific layout styles (`.calibrate-page`, `.calibrate-header`, `.calibrate-header-inner`, `.calibrate-back-link`, `.calibrate-title`, `.calibrate-module-code`, `.calibrate-content`) and reuses the shared calibration CSS classes from `css/styles.css` (`.calibration-panel`, `.calibration-content`, `.snapshot-form`, `.snapshot-field`, etc.).

### Auto-Population Workflow

1. User is on the review page with panels loaded
2. User clicks a block in the PageForge panel — all panels sync
3. User clicks "Copy PF" → PageForge HTML saved to `pageforge_snapshot_pf`
4. User clicks "Copy Human" → Human reference HTML saved to `pageforge_snapshot_human`
5. User clicks "Copy WT" → Writer Template text saved to `pageforge_snapshot_wt`
6. User switches to the Conversion Error Log tab (or clicks "Conversion Error Log" to open it)
7. `CalibrateApp._populateFromSessionStorage()` runs (on page load or tab focus)
8. Form fields are populated with the saved content
9. Source file dropdown auto-selects the matching filename
10. SessionStorage keys are cleared after reading
11. `CalibrationManager._updateLogButtonState()` enables the Log button if all 3 required fields have content
12. User can add optional notes, then click "Log Snapshot"
13. User can repeat: switch to review tab, copy more content, switch back — fields auto-populate on focus

---

## 23. REVIEW PAGE UX IMPROVEMENTS (Phase 11)

### Overview

Phase 11 addresses three usability issues on the Visual Comparison Review page: (1) toolbar controls relocated from the header bar to a dedicated row below the title, (2) "Calibration Tool" renamed to "Conversion Error Log" across the entire codebase to better reflect its purpose of documenting conversion algorithm discrepancies, and (3) scroll-position preservation when toggling between rendered and Raw HTML views using a textual-anchor fuzzy-matching algorithm with proportional fallback. A reusable static `normaliseTextForMatch()` method was created for text normalisation shared across the scroll-preservation and sync logic. Note: Phase 11 originally included a continuous proportional scroll sync system; this was entirely replaced by the per-panel Sync buttons in Phase 12 (see Section 24).

**Status:** DONE — 6 files modified, 1 file created. Phase 11 changes retained (toolbar relocation, rename, Raw HTML scroll-preservation); Phase 11 continuous scroll sync superseded by Phase 12 per-panel Sync buttons. Test file updated to 72 tests (479 total), all tests passing.

### Files Modified

| File | Changes |
|------|---------|
| `review.html` | Removed `.review-header-right` div from header; added `.review-toolbar` div between header and three-panel layout containing Raw HTML button and Conversion Error Log button (Sync toggle removed in Phase 12); button text changed from "Calibration Tool" to "Conversion Error Log" |
| `js/review-app.js` | Renamed `_openCalibrationTool()` → `_openConversionErrorLog()`; added `static normaliseTextForMatch(text)` reusable helper for text normalisation (strips HTML, decodes entities, lowercases, removes punctuation, preserves macrons, collapses whitespace); added `_extractVisibleAnchor(panel)` and `_extractAnchorFromRawView(rawViewContainer)` for capturing the currently visible content anchor; added `_scrollRawViewToAnchor()`, `_scrollIframeToAnchor()`, and `_scrollWriterToAnchor()` for fuzzy-matching anchor text in target panels; added `_restoreScrollFromAnchor(anchor)` for post-toggle scroll restoration; refactored `_toggleRawHtmlMode()` to extract anchor before switching and restore after via `requestAnimationFrame`; added `writerPanelBody`, `pageforgePanelBody`, `humanPanelBody` DOM references; updated JSDoc comments to reference "Conversion Error Log" |
| `css/review-styles.css` | Removed `.review-header-right` styles; added `.review-toolbar` styles (flex row, background, border, padding); added `.review-toolbar` responsive styles in `@media (max-width: 900px)` block; renamed "Calibration Tool Button" CSS comment to "Conversion Error Log Button" |
| `calibrate.html` | Changed `<title>` from "PageForge — Calibration Comparison Tool" to "PageForge — Conversion Error Log"; changed `<h1>` from "Calibration Comparison Tool" to "Conversion Error Log" |
| `js/calibrate-app.js` | Updated JSDoc header to reference "Conversion Error Log" instead of "Calibration Comparison Tool" |
| `tests/test-runner.js` | Added `global.__testFs`, `global.__testPath`, `global.__testRootDir` globals so test files loaded via `vm.runInThisContext()` can read project files for DOM structure analysis |

### Files Created

| File | Purpose |
|------|---------|
| `tests/reviewPageChanges.test.js` | 72 tests covering: toolbar relocation (8 tests), Conversion Error Log rename consistency (8 tests), per-panel Sync button DOM structure (9 tests), global Sync toggle complete removal (13 tests), one-shot align trigger implementation (7 tests), content-matching with textual-anchor helpers (8 tests), visual feedback (4 tests), no continuous scroll-coupling (6 tests), Raw HTML scroll-preservation (3 tests), normaliseTextForMatch helper (7 unit tests). See Section 24 for Phase 12 test details. |

### Change-by-Change Summary

#### Change 1 — Toolbar Relocation
- **Previous:** Sync toggle, Raw HTML button, and Calibration Tool button were in a `.review-header-right` div inside the `<header>` element alongside the back link, title, and module code badge
- **Fix:** Removed `.review-header-right` entirely from `<header>`; created a new `.review-toolbar` `<div>` positioned between `</header>` and the `.review-layout` three-panel container; all controls moved to the toolbar with left-aligned flex layout; toolbar has its own background (`var(--color-bg)`), border-bottom, and responsive flex-wrap at 900px breakpoint

#### Change 2 — "Calibration Tool" → "Conversion Error Log" Rename
- **Previous:** Button on review page said "Calibration Tool"; calibrate.html title said "PageForge — Calibration Comparison Tool"; heading said "Calibration Comparison Tool"; method was `_openCalibrationTool()`
- **Fix:** Button text changed to "Conversion Error Log" (review.html); `<title>` changed to "PageForge — Conversion Error Log" (calibrate.html); `<h1>` changed to "Conversion Error Log" (calibrate.html); method renamed to `_openConversionErrorLog()` (review-app.js); JSDoc comments updated (review-app.js, calibrate-app.js); CSS comment updated (review-styles.css); all error messages and toast text updated

#### Change 3 — Proportional Scroll Sync (Superseded by Phase 12)
- **Note:** The continuous proportional scroll sync implemented in Phase 11 (`_bindScrollSync`, `syncModeEnabled`, `_scrollSyncLock`, debounced handlers) has been entirely removed and replaced by the per-panel one-shot Sync buttons in Phase 12. See Section 24 for the replacement implementation.

#### Change 4 — Raw HTML Scroll-Position Preservation
- **Previous:** Toggling Raw HTML reset scroll to top in both PageForge and Human Reference panels, requiring manual scrolling to find the same content region
- **Fix:** New textual-anchor matching system preserves scroll position across view toggles:
  - **Anchor extraction (`_extractVisibleAnchor`):** Before toggling, identifies the element nearest to the top of the visible area in the PageForge panel; extracts its text content, normalises it via `normaliseTextForMatch()`, and captures the first 120 characters as an anchor along with the current scroll fraction
  - **Text normalisation (`normaliseTextForMatch`):** Static method shared across all anchor-matching logic; strips HTML tags, decodes `&amp;`/`&lt;`/`&gt;`/`&nbsp;` entities, lowercases, removes punctuation (preserves macronised vowels ā/ē/ī/ō/ū), collapses whitespace
  - **Raw view anchor search (`_scrollRawViewToAnchor`):** Splits raw HTML into lines, normalises each line, counts matching words from the anchor (split on whitespace, filtered to >2 chars); requires ≥30% word match; scrolls to best-matching line; falls back to proportional scroll
  - **Iframe anchor search (`_scrollIframeToAnchor`):** Queries all text-bearing elements (h1-h5, p, li, td, th, div.activity, etc.), normalises their text, counts word matches against anchor; requires ≥30% match; calls `scrollIntoView()` on best match; falls back to proportional scroll
  - **Writer panel anchor search (`_scrollWriterToAnchor`):** Searches `.writer-block` elements using the same word-matching algorithm; falls back to proportional scroll
  - **Post-toggle restoration (`_restoreScrollFromAnchor`):** After `_loadPageforgePanel` and `_loadHumanPanel` complete, uses double `requestAnimationFrame` to wait for DOM rendering, then scrolls all three panels to the anchor. For rendered-to-raw toggle, calls `_scrollRawViewToAnchor` on both PageForge and Human raw views. For raw-to-rendered toggle, attaches one-time iframe `load` event listeners (with 500ms timeout fallback) then calls `_scrollIframeToAnchor`. Writer panel always uses `_scrollWriterToAnchor`.

### New Public API on ReviewApp

- `static normaliseTextForMatch(text)` — reusable text normalisation helper (strips HTML, decodes entities, lowercases, removes punctuation, preserves macrons, collapses whitespace)

---

## 24. PER-PANEL SYNC BUTTONS (Phase 12)

### Overview

Phase 12 replaces the global continuous Sync toggle (implemented in Phase 11) with three per-panel one-shot Sync buttons — one anchored to each of the three visual comparison panels (PageForge Output, Human Reference, Writer Template). The interaction model changes from "continuous scroll-coupling" to "one-shot align trigger": clicking a panel's Sync button extracts a textual anchor from that panel's current viewport position, then scrolls the other two panels to the best-matching content using a tiered fallback chain (exact normalised match → fuzzy word match → proportional scroll). No ongoing scroll-coupling is created — after the jump completes, all panels can be scrolled independently. The implementation reuses and extends the `normaliseTextForMatch`, `_extractVisibleAnchor`, `_scrollRawViewToAnchor`, `_scrollIframeToAnchor`, and `_scrollWriterToAnchor` helpers originally created for the Raw HTML scroll-position preservation feature in Phase 11. All existing functionality from previous phases remains working — the 407 pre-Phase-11 tests continue to pass alongside the 72 tests in the updated `reviewPageChanges.test.js` (479 total).

**Status:** DONE — 3 files modified (review.html, js/review-app.js, css/review-styles.css), 1 test file rewritten (tests/reviewPageChanges.test.js with 72 tests replacing 45), 479 tests passing, 0 failing.

### Files Modified

| File | Changes |
|------|---------|
| `review.html` | Removed global Sync toggle (`<label>` with checkbox `#sync-mode-toggle`, `.review-sync-slider`, `.review-sync-label`) from toolbar row; added `<button id="btn-sync-pageforge" class="btn btn-sm review-sync-btn">` to PageForge panel header; added `<button id="btn-sync-human" class="btn btn-sm review-sync-btn">` to Human Reference panel header; added `<button id="btn-sync-writer" class="btn btn-sm review-sync-btn">` to Writer Template panel header; all three buttons use `&#8644; Sync` text and consistent `review-sync-btn` class; toolbar now contains only Raw HTML and Conversion Error Log buttons |
| `js/review-app.js` | **Removed:** `syncModeEnabled` property, `_scrollSyncLock` property, `_bindScrollSync()` method (entire proportional scroll sync system including debounce helper, `getScrollable()`, `getScrollFraction()`, `setScrollFraction()`, `onPanelScroll()`, debounced scroll handlers, scroll event listener bindings for writer/raw/iframe panels), `_attachIframeScrollHandler()` method, `_attachIframeClickHandler()` method (iframe click-to-sync handler), `_syncToBlock()` method, `_highlightInIframe()` method, `_syncWriterPanel()` method, `_syncHumanPanelIntelligent()` method (6-tier matching algorithm), `_highlightAndScroll()` method, `_findStructuralId()` method, `_extractActivityNumber()` method, `_extractHeadingText()` method, `_extractWordGroups()` method, `_findByWordGroups()` method, `_updateSyncModeIndicator()` method, `syncModeToggle` DOM reference, sync-mode-disable guard in `_restoreScrollFromAnchor()`. **Added:** `btnSyncPageforge`, `btnSyncHuman`, `btnSyncWriter` DOM references; `_onSyncClick(sourcePanel)` method (one-shot align trigger with visual feedback); `_syncPanelToAnchor(panel, anchorText, fallbackFraction)` method (delegates to appropriate scroll helper based on panel type and view mode); `_panelDisplayName(panel)` helper. **Updated:** JSDoc header to describe per-panel sync instead of 6-tier sync mode; `_bindEvents()` to wire up three Sync button click handlers instead of sync toggle change listener; `_restoreScrollFromAnchor()` simplified (no longer needs to disable/restore sync mode or set scroll lock) |
| `css/review-styles.css` | **Removed:** `.review-sync-toggle` styles (label, checkbox hide, slider, slider::after, checked states, label text), `.review-sync-active` indicator class. **Added:** `.review-sync-btn` styles (font-size, padding, background, border, color, transition, border-radius), `.review-sync-btn:hover` styles, `.review-sync-btn-pulse` styles (active/pressed state with primary colour and box-shadow for button click feedback), `.review-panel-sync-flash` styles (inset box-shadow for target panel flash on sync jump). **Updated:** CSS section comment from "Sync Mode Toggle" to "Per-Panel Sync Buttons" |

### Files Rewritten

| File | Changes |
|------|---------|
| `tests/reviewPageChanges.test.js` | Complete rewrite: 72 tests (was 45) organised into 10 `describe` blocks covering Phase 11 retained functionality + Phase 12 new functionality. Old tests for `_bindScrollSync`, `syncModeEnabled`, `_scrollSyncLock`, debounce, `getScrollable`, sync-disable-during-restore removed. New tests added for per-panel Sync button DOM presence, CSS, global toggle removal, `_onSyncClick` implementation, `_syncPanelToAnchor`, visual feedback, no continuous coupling |

### Change-by-Change Summary

#### Change 1 — Replace Global Sync Toggle with Per-Panel Sync Buttons (HTML)
- **Previous:** `<label class="review-sync-toggle">` with hidden checkbox `#sync-mode-toggle`, slider element, and "Sync" label text inside the `.review-toolbar` row
- **Fix:** Removed the entire `<label>` element from the toolbar. Added a `<button id="btn-sync-{panel}" class="btn btn-sm review-sync-btn">` to each of the three panel headers, positioned between the panel filename and the Copy button. All three buttons use the same `&#8644; Sync` text, `review-sync-btn` class, and tooltip "Sync other panels to this panel's position"

#### Change 2 — One-Shot Align Trigger Implementation (JS)
- **Previous:** `syncModeEnabled` boolean controlled by checkbox toggle; when ON, clicking in PageForge iframe triggered `_syncToBlock()` which ran `_syncHumanPanelIntelligent()` (6-tier matching algorithm) and `_syncWriterPanel()` (direct block index match); continuous `_bindScrollSync()` proportionally coupled all panel scrolls
- **Fix:** New `_onSyncClick(sourcePanel)` method handles all three Sync buttons:
  1. Applies visual feedback — pulse class on clicked button, flash class on target panels
  2. Calls `_extractVisibleAnchor(sourcePanel)` to get the textual anchor and scroll fraction from the source panel's current viewport position
  3. Filters out the source panel, leaving only the two target panels
  4. For each target, calls `_syncPanelToAnchor(panel, anchorText, fallbackFraction)` which delegates to `_scrollWriterToAnchor()`, `_scrollRawViewToAnchor()`, or `_scrollIframeToAnchor()` based on panel type and current view mode (rendered vs raw HTML)
  5. Shows a toast notification identifying the source panel
  6. No state is set — no ongoing coupling created

#### Change 3 — Content-Matching Logic (Reuse of Phase 11 Helpers)
- The per-panel Sync buttons reuse the textual-anchor matching infrastructure created in Phase 11 for Raw HTML scroll-position preservation:
  - `_extractVisibleAnchor(panel)` — works for rendered iframes (finds nearest element to viewport top), raw HTML views (estimates line from scroll position), and writer blocks (finds nearest `.writer-block` to scroll top)
  - `_scrollIframeToAnchor(iframe, anchorText, fallbackFraction)` — word-level fuzzy matching against rendered DOM elements with ≥30% threshold; falls back to proportional scroll
  - `_scrollRawViewToAnchor(rawViewContainer, anchorText, fallbackFraction)` — word-level fuzzy matching against raw HTML lines with ≥30% threshold; falls back to proportional scroll
  - `_scrollWriterToAnchor(anchorText, fallbackFraction)` — word-level fuzzy matching against `.writer-block` text; falls back to proportional scroll
  - `static normaliseTextForMatch(text)` — shared text normalisation (strip HTML, decode entities, lowercase, remove punctuation, preserve macrons, collapse whitespace)
- The new `_syncPanelToAnchor()` method acts as a dispatcher, checking the panel type and current view mode to call the correct scroll helper

#### Change 4 — Visual Feedback
- **Button pulse:** When a Sync button is clicked, `.review-sync-btn-pulse` class is added (primary background + white text + box-shadow), auto-removed after 400ms
- **Target panel flash:** Both target panels receive `.review-panel-sync-flash` class (inset box-shadow), auto-removed after 500ms
- **Toast notification:** "Synced from [Panel Name]" displayed via `showToast()` after each sync click

#### Change 5 — Complete Removal of Old Global Sync System
- **Removed from JS:** `syncModeEnabled` property, `_scrollSyncLock` property, `_bindScrollSync()` call from constructor, entire `_bindScrollSync()` method definition (including inner functions `debounce()`, `getScrollable()`, `getScrollFraction()`, `setScrollFraction()`, `onPanelScroll()`), three debounced scroll handler variables, scroll event listener bindings on `writerPanelBody`, `pageforgeRaw`, `humanRaw`, iframe load-event scroll re-attachment, `_attachIframeScrollHandler()` method, `syncModeToggle` DOM reference, sync toggle change event listener, `_updateSyncModeIndicator()` method, `_attachIframeClickHandler()` method, `_syncToBlock()` method, `_highlightInIframe()` method, `_syncWriterPanel()` method, `_syncHumanPanelIntelligent()` method, `_highlightAndScroll()` method, `_findStructuralId()` method, `_extractActivityNumber()` method, `_extractHeadingText()` method, `_extractWordGroups()` method, `_findByWordGroups()` method, sync-mode-disable guard in `_restoreScrollFromAnchor()`, `syncModeEnabled` check in `_bindEvents()` sync toggle listener
- **Removed from HTML:** `<label class="review-sync-toggle">`, `<input type="checkbox" id="sync-mode-toggle">`, `<span class="review-sync-slider">`, `<span class="review-sync-label">`
- **Removed from CSS:** `.review-sync-toggle` (all variants), `.review-sync-slider` (all variants including `::after`, checked states), `.review-sync-label`, `.review-sync-active`

#### Change 6 — CSS Additions
- `.review-sync-btn` — compact button styling matching panel header layout: `font-size: 0.68rem`, `padding: 0.2rem 0.5rem`, surface background, border colour, secondary text, 4px border-radius, smooth transitions
- `.review-sync-btn:hover` — primary-light background, primary border/text on hover
- `.review-sync-btn-pulse` — primary background, white text, primary border, box-shadow glow for button click feedback (400ms duration)
- `.review-panel-sync-flash` — inset box-shadow (`2px var(--color-primary)`) for target panel flash on sync jump (500ms duration via `transition: box-shadow 0.3s ease-out`)

### Test Coverage

72 tests in `tests/reviewPageChanges.test.js`:

| Category | Count | Tests |
|----------|-------|-------|
| Toolbar relocation (Phase 11) | 8 | `.review-toolbar` exists, positioned after header/before layout, contains Raw HTML + Error Log buttons, header has no controls, no `.review-header-right`, header has back/title/badge only, CSS defined, responsive |
| Conversion Error Log rename (Phase 11) | 8 | Button text correct, no old text, page title, page heading, new method name, no old method name, JSDoc updated, no old heading |
| Per-panel Sync button DOM structure | 9 | Sync button in PageForge header, Sync button in Human Reference header, Sync button in Writer Template header, consistent `review-sync-btn` class on all three, all use &#8644; Sync text, CSS for `.review-sync-btn`, CSS for `.review-sync-btn-pulse`, CSS for `.review-panel-sync-flash` |
| Global Sync toggle complete removal | 13 | No `sync-mode-toggle` checkbox, no `.review-sync-toggle` label, no `syncModeEnabled`, no `_scrollSyncLock`, no `_bindScrollSync`, no `_attachIframeScrollHandler`, no `_attachIframeClickHandler`, no `_updateSyncModeIndicator`, no debounced scroll handlers, no `.review-sync-toggle` CSS, no `.review-sync-slider` CSS, no `.review-sync-active` CSS, no 6-tier sync methods |
| One-shot align trigger | 7 | `_onSyncClick` exists, accepts `sourcePanel`, bound to all three buttons in `_bindEvents`, calls `_extractVisibleAnchor(sourcePanel)`, filters out source panel from targets, `_syncPanelToAnchor` exists, handles rendered/raw modes |
| Content-matching helpers retained | 8 | `normaliseTextForMatch`, `_extractVisibleAnchor`, `_scrollRawViewToAnchor`, `_scrollIframeToAnchor`, `_scrollWriterToAnchor`, `_extractAnchorFromRawView`, `fallbackFraction` proportional fallback, `_restoreScrollFromAnchor` for Raw HTML toggle |
| Visual feedback | 4 | Pulse class added to clicked button, pulse class removed after timeout, flash class on target panels, toast notification after sync |
| No continuous scroll-coupling | 6 | No `addEventListener('scroll'` bindings, no `onPanelScroll`, no `getScrollable`, no `getScrollFraction`, no `setScrollFraction`, no `debounce` function |
| Raw HTML scroll preservation (Phase 11) | 3 | Anchor extraction before toggle, `requestAnimationFrame` for post-render, proportional fallback |
| `normaliseTextForMatch` unit tests | 7 | null/empty, HTML stripping, lowercase, whitespace collapse, macron preservation, entity decoding, punctuation removal |
