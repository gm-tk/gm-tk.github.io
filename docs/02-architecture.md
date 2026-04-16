# 2. Current Architecture


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
| `App` | `js/app.js` | UI controller — staged upload, Convert button, file list, preview, ZIP download, text download, debug panel, template selection |

---


---

[← Back to index](../CLAUDE.md)
