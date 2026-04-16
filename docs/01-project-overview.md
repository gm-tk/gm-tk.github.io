# 1. Project Overview


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
15. **Feature removal — Visual Comparison Review & Conversion Error Log** → complete removal of the Visual Comparison Review page (review.html, ReviewApp, review-styles.css), Conversion Error Log page (calibrate.html, CalibrateApp, CalibrationManager), all associated UI elements (Visual Comparison Review button, calibration panel), sessionStorage serialisation/chunking, snapshot form CSS, test globals, and 72 review page tests; core conversion pipeline unchanged (DONE — Phase 14)
16. **Years 4–6 lesson page recalibration** → lesson page `<title>` stripped of decimal lesson number (now `MODULE_CODE English Title` on BOTH overview and lesson pages); lesson page `<h1><span>` uses the lesson-specific title (first `[H2]` in body, `"Lesson N:"` prefix stripped) via new `pageData.lessonTitle` extracted by `HtmlConverter._extractLessonTitle()`; trailing space removed from inside `<h1><span>` content (both overview and lesson); Te Reo `<h1>` suppressed on lesson pages for 1-3 / 4-6 / 7-8 (driven by `headerPattern.lessonPage.titles`); `tooltip="Overview"` removed from lesson `#module-menu-button` (driven by `moduleMenu.lessonPage.tooltipOn: null`); lesson module menu rewritten to new two-tier structure — `<h5>{sectionHeading}</h5><p>{writer's intro verbatim}</p><ul>…</ul>` — where `sectionHeadings` come from template config (`Learning Intentions` / `How will I know if I've learned it?`) and the writer's own intro text (e.g. "We are learning:", "I can:", "You will show your understanding by:") is preserved as the paragraph, reversing the prior rule that substituted config labels; new `templates.json` schema fields: `moduleMenu.lessonPage.sectionHeadings`, `moduleMenu.lessonPage.tooltipOn: null`, `headerPattern.lessonPage.titleSource: "lesson"` (DONE — Phase 13)
17. **Multi-template skeleton calibration** → `<title>` element now uses `titlePattern` config field with token substitution (`{moduleCode} {englishTitle}`) instead of hardcoded format; `#module-code` lesson display format is template-specific via new `headerPattern.lessonPage.moduleCodeFormat` field — `"decimal"` (N.0) for template 4-6, `"zero-padded"` (01, 02) for all others; `<head>` script set varies per template — templates 1-3 and 7-8 include `stickyNav.js` before `idoc_scripts.js` and use `tekuradev.desire2learn.com`, template 4-6 uses `tekura.desire2learn.com` only; `tooltip="Overview"` on overview-page `#module-menu-content` now template-specific — present on 4-6 only, null for 1-3 and 7-8; footer link ordering changed — overview pages emit next-lesson then home-nav, lesson pages emit home-nav first then prev-lesson then next-lesson; new `templates.json` schema fields: `additionalHeadScripts`, `headerPattern.lessonPage.moduleCodeFormat`; per-template overrides added for 1-3 and 7-8 (`scriptUrl`, `additionalHeadScripts`, `moduleMenu.overviewPage.tooltipOn: null`) and 4-6 (`headerPattern.lessonPage.moduleCodeFormat: "decimal"`) (DONE — Phase 15)

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


---

[← Back to index](../CLAUDE.md)
