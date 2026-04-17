# 22. Years 4–6 Lesson Page Recalibration (Phase 13)


### Overview

Phase 13 applies a calibration snapshot recalibration to PageForge's Years 4–6
lesson page output based on a side-by-side comparison of `OSAI201-01.html`
against the human developer's correct reference file. Four structural
discrepancies in the `<head>` and `<header>` regions plus the module menu
were identified and fixed at the template-engine, html-converter, and
configuration layers. Although the trigger was a Years 4–6 lesson page, each
fix was examined for applicability to the other template levels (1–3, 7–8,
9–10, NCEA, bilingual, fundamentals, inquiry, combo) and applied consistently
where the structural pattern matches the shared LMS template rather than
being year-specific.

All existing phase tests continue to pass. The 488 pre-existing tests plus
23 new Phase 13 tests (in `tests/years46LessonRecalibration.test.js`) total
511 tests — all passing, 0 failing.

**Status:** DONE — 2 source files modified, 1 configuration file modified,
3 existing tests updated (Phase 7 Change 2 superseded by Phase 13), 1 new
test file added with 23 tests, 511 total tests passing.

### Files Modified

| File | Changes |
|------|---------|
| `js/template-engine.js` | `<title>` element no longer includes lesson decimal number (Discrepancy 1); `_generateHeader()` honours new `headerPattern.lessonPage.titleSource: "lesson"` to render lesson-specific title in `<h1><span>` (Discrepancy 2) with the `"Lesson N:"` prefix stripped via new `TemplateEngine._stripLessonPrefix()` static helper; trailing space inside `<h1><span>` removed (both overview + lesson); Te Reo `<h1>` suppression tightened — now requires `titles` array to include `"tereo"` (no auto-emit when a Te Reo title was incidentally parsed); lesson-page `#module-menu-button` omits the `tooltip="Overview"` attribute when `moduleMenu.lessonPage.tooltipOn` is `null` (Discrepancy 3); embedded fallback data updated to mirror `templates.json` with `sectionHeadings`, `tooltipOn: null`, and `titleSource: "lesson"` |
| `js/html-converter.js` | New `_extractLessonTitle(bodyBlocks)` method scans body content blocks for the first `[H1]`/`[H2]` heading and returns its clean text (with .docx bold/italic artefacts stripped); returns `null` if no heading found; called by `assemblePage()` for lesson pages; extracted title stored on `skeletonData.lessonTitle` for the template engine to consume. `_generateLessonMenuContent()` rewritten (Discrepancy 4) — reads `sectionHeadings` from `config.moduleMenu.lessonPage.sectionHeadings`; captures the writer's verbatim intro text during section-boundary detection (instead of discarding it); emits the new two-tier structure `<h5>{sectionHeading}</h5><p>{writer intro}</p><ul>…</ul>`; sections with no list items + no detected intro are suppressed; empty-content fallback preserves the old heading-only behaviour; uses `labels` from config only as fallback when no writer intro paragraph exists |
| `templates/templates.json` | `baseConfig.moduleMenu.lessonPage`: added `sectionHeadings` object (`learning: "Learning Intentions"`, `success: "How will I know if I've learned it?"`); changed `tooltipOn` from `"module-menu-button"` to `null`; preserved existing `labels` as fallback. `baseConfig.headerPattern.lessonPage.titleSource` changed from `"module"` to `"lesson"`. All per-template `labels` overrides for lesson-page intros preserved so writer fallback retains the historical year-specific wording |
| `tests/lmsCompliance.test.js` | Phase 7 Change 2 block replaced — the 3 tests that asserted `"0.0"` / `"1.0"` / `"3.0"` inside `<title>` now assert the Phase 13 rule (no decimal in `<title>`) and verify the decimal is still present in `#module-code`. The rest of the Phase 7 suite is untouched |
| `tests/years46LessonRecalibration.test.js` | New file — 23 tests covering all four discrepancies, lesson-title extraction, prefix stripping, fallback-with-warning behaviour, Te Reo suppression across levels, overview-page invariance, two-tier module menu rendering, and an end-to-end OSAI201-01 calibration snapshot assertion |

### Discrepancy-by-Discrepancy Summary

#### Discrepancy 1 — Lesson page `<title>` must NOT include the lesson decimal
- **Previous:** `<title>OSAI201 1.0 AI Digital Citizenship</title>` (lesson)
  and `<title>OSAI201 0.0 AI Digital Citizenship</title>` (overview)
- **Human reference:** `<title>OSAI201 AI Digital Citizenship</title>`
- **Fix:** `TemplateEngine.generateSkeleton()` now builds `titleContent` as
  `pageData.moduleCode + ' ' + englishOnlyTitle` for BOTH overview and lesson
  pages, removing the decimal entirely. `#module-code` display still shows
  the decimal (`1.0`, `2.0`, etc.) — only the `<title>` element changed.
- **Applied to:** All templates — the `<title>` rule is LMS-wide, not
  year-specific, so Years 1–3, 4–6, 7–8, 9–10, NCEA, bilingual,
  fundamentals, inquiry, and combo all get the decimal-free `<title>`.
- **Open question noted:** The overview-page behaviour was also changed
  because the Phase 7 pattern (`MODULE_CODE 0.0 English Title`) did not
  match the human reference pattern (`MODULE_CODE English Title`). If an
  overview-specific human reference later reveals the `0.0` prefix IS
  expected in the overview, this decision should be revisited.

#### Discrepancy 2 — Lesson header `<h1>` must be lesson-specific + single + no trailing space
- **Previous:** Lesson page emitted `<h1><span>AI Digital Citizenship </span></h1>`
  (module title + trailing space) plus auto-added Te Reo `<h1>` if a Te Reo
  title was present from title-bar parsing.
- **Human reference:** `<h1><span>What is AI?</span></h1>` (single, lesson
  title, no trailing space, no Te Reo on 4-6).
- **Fix:**
  1. New `HtmlConverter._extractLessonTitle(bodyBlocks)` scans the body
     content blocks for the first `[H2]` (or `[H1]`) heading tag and returns
     its clean text.
  2. `HtmlConverter.assemblePage()` calls this for lesson pages and passes
     the result as `skeletonData.lessonTitle`.
  3. `TemplateEngine._generateHeader()` reads `headerPattern.lessonPage.titleSource`:
     - `"lesson"` (new default for base config) → uses `pageData.lessonTitle`,
       stripped of `"Lesson N:"` / `"Lesson N -"` prefix via
       `TemplateEngine._stripLessonPrefix()`. Falls back to module title with
       a `console.warn` if `pageData.lessonTitle` is missing.
     - `"module"` (legacy) → uses the module English title (preserved as an
       option for any template that explicitly needs module-title headers).
  4. Trailing space inside `<h1><span>` removed — applies to BOTH overview
     and lesson pages, both English and Te Reo h1s.
  5. Te Reo `<h1>` emission now requires `titles` array to include `"tereo"`.
     Previously it auto-emitted whenever `tereoTitle` existed; now the
     array must explicitly allow it. This means 1-3 / 4-6 / 7-8 lesson
     pages never emit a Te Reo h1 regardless of parsed title content.
- **Applied to:** All templates. Overview pages for 9-10 and NCEA continue
  to emit Te Reo h1 because their `headerPattern.overviewPage.titles` is
  `["english", "tereo"]`. Bilingual template continues to emit Te Reo h1
  on both page types because it overrides both overview and lesson `titles`
  to `["english", "tereo"]`.

#### Discrepancy 3 — Lesson `#module-menu-button` must have no `tooltip` attribute
- **Previous:** Lesson page emitted
  `<div id="module-menu-button" class="circle-button btn1" tooltip="Overview"></div>`.
- **Human reference:** `<div id="module-menu-button" class="circle-button btn1"></div>`.
- **Fix:** `moduleMenu.lessonPage.tooltipOn` changed from `"module-menu-button"`
  to `null` in `templates.json` baseConfig. `_generateModuleMenu()` already
  respected this value; changing the config is sufficient. Overview-page
  behaviour is unaffected — the `tooltip="Overview"` attribute still appears
  on `#module-menu-content` because `moduleMenu.overviewPage.tooltipOn`
  remains `"module-menu-content"`.
- **Applied to:** All templates — lesson pages across 1–3, 4–6, 7–8, 9–10,
  NCEA, bilingual, fundamentals, inquiry, and combo all inherit the base
  `tooltipOn: null`.

#### Discrepancy 4 — Two-tier module menu structure (section heading + writer intro + list)
- **Previous:** Lesson module menu emitted:
  ```
  <h5>We are learning:</h5>     ← config labels (overriding writer text)
  <ul><li>…</li></ul>
  <h5>You will show your understanding by:</h5>
  <ul><li>…</li></ul>
  ```
  The writer's exact intro text was discarded in favour of config label text.
- **Human reference:**
  ```
  <h5>Learning Intentions</h5>   ← LMS section title (new config key)
  <p>We are learning:</p>        ← writer's verbatim intro paragraph
  <ul><li>…</li></ul>
  <h5>How will I know if I've learned it?</h5>
  <p>I can:</p>
  <ul><li>…</li></ul>
  ```
- **Fix:**
  1. New `templates.json` field `moduleMenu.lessonPage.sectionHeadings`
     with `learning` and `success` keys. Default values
     `"Learning Intentions"` and `"How will I know if I've learned it?"` in
     the baseConfig. The existing `labels` field is retained as a fallback
     for the intro paragraph text when the writer didn't provide one.
  2. `HtmlConverter._generateLessonMenuContent()` rewritten. During the
     section-boundary detection loop (which matches phrases like "we are
     learning", "i can", "success criteria", "you will show"), the writer's
     `cleanText` is now captured into `learningIntroText` / `successIntroText`
     variables instead of being skipped. Rendering then emits, per section:
     ```
     <h5>{sectionHeadings.learning|success}</h5>
     <p>{writer intro text verbatim}</p>
     <ul>{list items}</ul>
     ```
  3. Empty-section handling: a section with neither intro text NOR items is
     suppressed entirely. A section with intro but no items emits `<h5><p>`
     only (no empty `<ul>`). A section with items but no detected intro
     falls back to the config `labels` text for the `<p>`.
  4. When `menuContentBlocks` is empty, both section headings are still
     emitted with placeholder HTML comments, preserving the previous
     empty-fallback layout.
- **Applied to:** All templates — the two-tier rule comes from the LMS
  refresh template and is not year-specific. Years 1–3, 4–6, 7–8, 9–10, and
  NCEA all inherit the same default `sectionHeadings`. The per-template
  `labels` overrides (preserving historical phrasing like "You will show
  your understanding by:" for 1-3 / 4-6 vs "I can:" for 7-8 / 9-10 / NCEA)
  remain in place as fallbacks for modules where the writer omitted the
  intro paragraph.

### New Public APIs

**`TemplateEngine._stripLessonPrefix(text)`** (static helper) — Strips
`"Lesson N:"`, `"Lesson N"`, `"Lesson N -"`, or `"Lesson N –"` prefix from
a lesson heading text. Used inside `_generateHeader()` when `titleSource`
is `"lesson"`. Returns empty string for null/non-string inputs.

**`HtmlConverter._extractLessonTitle(bodyBlocks)`** — Scans body content
blocks for the first `[H1]` or `[H2]` heading tag. Returns the clean
heading text with wrapping bold/italic `.docx` artefacts stripped via
`_stripFullHeadingFormatting()`. Returns `null` if no heading found. Called
from `assemblePage()` for lesson pages; the result populates
`skeletonData.lessonTitle`.

### New `templates.json` Schema Fields

| Field | Location | Values | Purpose |
|-------|----------|--------|---------|
| `moduleMenu.lessonPage.sectionHeadings` | baseConfig + overrides | `{learning: string, success: string}` | LMS section heading text emitted as `<h5>` above the writer's intro paragraph on lesson pages. Defaults: `"Learning Intentions"` and `"How will I know if I've learned it?"` |
| `moduleMenu.lessonPage.tooltipOn: null` | baseConfig | `null` \| `"module-menu-button"` | Controls the tooltip attribute on lesson-page menu button. Default is now `null` (no attribute). Retained as `"module-menu-button"` capability for any template that explicitly needs it |
| `headerPattern.lessonPage.titleSource: "lesson"` | baseConfig | `"lesson"` \| `"module"` | Source of the lesson-page `<h1><span>` text. `"lesson"` (default) uses `pageData.lessonTitle`; `"module"` uses the module English title (legacy behaviour) |

### Lesson-Title Extraction Pipeline Addendum

The lesson-title extraction step is performed by `HtmlConverter` during
`assemblePage()`, AFTER the content split (`_splitLessonContent()`) and
BEFORE skeleton generation. Pipeline placement:

```
HtmlConverter.assemblePage(pageData, config, moduleInfo):
  → _splitLessonContent(pageData) → {menuBlocks, bodyBlocks}
  → _extractLessonTitle(bodyBlocks)        ← NEW (Phase 13)
  → build skeletonData with lessonTitle
  → _templateEngine.generateSkeleton(config, skeletonData)
    → _generateHeader() consults titleSource + lessonTitle
    → _stripLessonPrefix() for display
  → convertPage(bodyPageData, config)
  → _replaceModuleMenuContent()
    → _generateLessonMenuContent() emits 2-tier structure
```

This keeps lesson-title extraction inside HtmlConverter (rather than
page-boundary.js) because the split between menu blocks and body blocks is
a concern of HtmlConverter, and the lesson title is explicitly defined as
"first [H2] in the BODY blocks" — not first [H2] in the whole page segment.
If moved to PageBoundary, the extraction would have to duplicate the
`_splitLessonContent()` logic, which is undesirable.

### Test Coverage

23 tests in `tests/years46LessonRecalibration.test.js`:

| Category | Tests |
|----------|-------|
| Discrepancy 1 (no decimal in `<title>`) | 3 — lesson title, overview title, `#module-code` decimal preserved |
| Discrepancy 2 (lesson h1) | 7 — lessonTitle in h1, no trailing space (lesson + overview), single h1 (4-6), dual h1 (9-10), prefix stripping, fallback with warning, `_extractLessonTitle` unit test |
| Discrepancy 3 (menu button tooltip) | 4 — 4-6 / 1-3 / 7-8 lesson pages, overview invariance |
| Discrepancy 4 (two-tier menu) | 7 — learning section structure, success section structure, verbatim writer intro preservation, intro-without-items, empty fallback, sectionHeadings consistency across years, legacy labels retained |
| End-to-end calibration snapshot | 1 — OSAI201-01 header + title + menu button assertion in a single skeleton |
| Phase 7 regression cover | 1 — updated Phase 7 Change 2 tests in `lmsCompliance.test.js` now assert the new no-decimal rule |

### Invariants Locked In By Phase 13

1. **`<title>` never contains a lesson decimal** across all templates and
   page types. Format is always `MODULE_CODE English Title`.
2. **Lesson page `<h1><span>` uses the lesson-specific title** (first `[H2]`
   in body with `"Lesson N:"` prefix stripped) for all templates whose
   `headerPattern.lessonPage.titleSource` is `"lesson"`. Falls back to
   module title with a console warning when extraction fails.
3. **No trailing space inside any `<h1><span>` content**, for both
   overview and lesson pages.
4. **Te Reo `<h1>` is opt-in via `titles` array**, never auto-emitted from
   parsed Te Reo title content.
5. **Lesson `#module-menu-button` has no `tooltip` attribute** unless a
   template explicitly sets `tooltipOn: "module-menu-button"`.
6. **Lesson module menu always emits the two-tier structure** when there is
   content: `<h5>` section heading (from config) + `<p>` writer intro
   (verbatim) + `<ul>` items.
7. **Writer intro paragraphs are preserved verbatim** — config `labels` are
   used only as a fallback when the writer didn't provide an intro line.
8. **Overview-page behaviour is unchanged by Phase 13**: tabbed menu,
   `tooltip="Overview"` on `#module-menu-content`, dual h1 for 9-10 / NCEA /
   bilingual, full module code in `#module-code`. All verified by tests.

### Open Questions / Future Considerations

- **Overview `<title>` change applies too.** The recalibration removed the
  decimal from the overview `<title>` as well as the lesson `<title>`,
  because the human pattern does not include the decimal anywhere. If a
  future overview-page reference reveals the `0.0` prefix IS actually
  expected on overview pages, the fix would be a minor branch inside
  `generateSkeleton()` to restore `MODULE_CODE 0.0 Title` for overviews
  only. The current rule was chosen for consistency with the human pattern
  observed to date.
- **Prefix-stripping edge cases.** The lesson-prefix regex
  (`^\s*Lesson\s+\d+\s*[:.\-–—]?\s*`) handles common forms. Non-Latin
  lesson-prefix formats (e.g., `Akoranga N:`) are not currently stripped —
  if/when encountered, extend `TemplateEngine._stripLessonPrefix()` to
  cover them.

---

### Session D — Per-Template Lesson Menu Rendering Styles

Session D introduces a `menuStyle` config key on
`moduleMenu.lessonPage`, allowing each template to select one of three
distinct lesson-page module menu rendering styles observed across the
5 LMS templates.

- **`menuStyle` values:**
  - `"synthesise-headings"` — Current Phase 13 baseline. Emits
    synthesised `<h5>` section headings (e.g. `<h5>Learning Intentions</h5>`)
    above the writer's verbatim `<p>We are learning:</p>` intro.
  - `"promote-to-h5"` — Promotes the writer's `We are learning:` / `I can:`
    body lines directly to `<h5>` (trailing colon kept). No synthesised
    parent headings. Preceding descriptive `<p>` preserved.
  - `"lesson-overview-bold"` — Emits a single `<h4>Lesson Overview</h4>`
    at top; body lines become `<p><b>We are learning:</b></p>` etc.;
    intro descriptive paragraph is DROPPED.

- **Per-template assignment:**
  - `1-3`, `9-10`, `NCEA` → `"promote-to-h5"`
  - `4-6` → `"synthesise-headings"` (baseline retained)
  - `7-8` → `"lesson-overview-bold"`

- **Output shape differences (short examples):**
  - `synthesise-headings`: `<h5>Learning Intentions</h5><p>We are learning:</p><ul>…`
  - `promote-to-h5`: `<h5>We are learning:</h5><ul>…`
  - `lesson-overview-bold`: `<h4>Lesson Overview</h4><p><b>We are learning:</b></p><ul>…`

- **Files touched:** `js/html-converter.js` (dispatch in
  `_generateLessonMenuContent()` + two new helpers
  `_generateLessonMenuPromoteToH5()` /
  `_generateLessonMenuOverviewBold()`), `templates/templates.json`
  (baseConfig default + 4 per-template overrides),
  `js/template-engine.js` (`_embeddedData()` mirror).

- **New test files:**
  `tests/lessonMenuPromoteAndBaseline.test.js` (7 tests covering
  baseline + promote-to-h5), `tests/lessonMenuOverviewBold.test.js`
  (6 tests covering lesson-overview-bold including intro-drop).

- **Post-merge test count:** 521/521 passing, 0 failing.

---


---

[← Back to index](../CLAUDE.md)
