# 17. LMS Compliance Recalibration (Phase 7)


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


---

[← Back to index](../CLAUDE.md)
