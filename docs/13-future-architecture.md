# 13. Future Architecture — HTML Conversion Engine


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

#### template-engine.js — DONE (Phase 2, updated Phase 15)
- Loads template configurations from `templates/templates.json` (with embedded fallback)
- Provides `getTemplateList()` for UI dropdown population (9 templates)
- Auto-detects template from module code suffix via `detectTemplate(moduleCode)`
- Deep-merges `baseConfig` with per-template overrides via `getConfig(templateId)`
- Generates complete HTML document skeletons via `generateSkeleton(config, pageData)`
- Handles header section (module code, titles, dual h1 for 9-10/NCEA)
- **Title bar parsing** — strips module code prefix, splits English/Te Reo on double-space, English-only `<title>`
- **Title element format** (Phase 15) — `<title>` uses `titlePattern` config field with token substitution (`{moduleCode}`, `{englishTitle}`); no decimal lesson number in `<title>` for any page type or template
- **Lesson number format** (Phase 7, updated Phase 15) — `lessonDisplayNumber` (decimal `N.0`) used for `#module-code` display only on templates with `moduleCodeFormat: "decimal"` (4-6); `lessonPadded` (zero-padded `01`) used for `#module-code` display on all other templates and for filenames/footers on all templates
- **Head scripts** (Phase 15) — `additionalHeadScripts` config array emitted before the main `scriptUrl` script; templates 1-3 and 7-8 include `stickyNav.js` before `idoc_scripts.js` and use `tekuradev.desire2learn.com`; template 4-6 uses `tekura.desire2learn.com` only
- Handles module menu (full-tabbed for overview with correct structure, simplified for lessons)
- **Tooltip placement** (updated Phase 15) — `tooltip="Overview"` on `#module-menu-content` only for overview pages where `tooltipOn` is `"module-menu-content"` (4-6 only); null for 1-3 and 7-8 overview pages; lesson pages never have tooltip on button (Phase 13)
- **Tab HTML structure** — no active/data-toggle/href/id/fade/in attributes, row wrapper, inner grid per tab-pane
- **Footer navigation** (updated Phase 15) — overview pages: next-lesson then home-nav; lesson pages: home-nav first, then prev-lesson, then next-lesson
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

### Extended App Flow (Current)

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
    → Debug panel (collapsible) shows conversion summary, template config, tag & page analysis, block scoping, interactive details
```

---


---

[← Back to index](../CLAUDE.md)
