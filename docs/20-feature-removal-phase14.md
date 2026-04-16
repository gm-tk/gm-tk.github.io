# 20. Feature Removal — Visual Comparison Review & Conversion Error Log (Phase 14)


### Overview

Phase 14 performs a complete removal of two development/testing utility features from the PageForge project: the **Visual Comparison Review** page (Phases 10–12) and the **Conversion Error Log** page (formerly "Calibration Comparison Tool", Phases 9–11). These features were internal development tools for comparing PageForge output against human-developed reference HTML. They have served their purpose and are no longer needed. The core conversion pipeline (parsing, tag normalisation, block scoping, layout table unwrapping, page boundary detection, template configuration, interactive extraction, HTML conversion, output management) remains completely untouched and fully functional.

**Status:** DONE — 7 files deleted, 4 files modified, 72 tests removed, 439 remaining tests all passing.

### Files Deleted (7)

| File | Purpose (before removal) |
|------|--------------------------|
| `review.html` | Visual Comparison Review standalone page — three synchronised viewing panels, file map, template-aware CSS injection, per-panel Sync buttons, Raw HTML toggle, copy-to-snapshot buttons |
| `calibrate.html` | Conversion Error Log standalone page — snapshot form, logged snapshots display, export/copy/clear controls |
| `js/review-app.js` | ReviewApp controller class — data deserialisation, three-panel rendering, CSS injection, textual-anchor matching, scroll-position preservation, one-shot Sync buttons |
| `js/calibrate-app.js` | CalibrateApp controller class — data loading from sessionStorage, CalibrationManager instantiation, auto-population of form fields |
| `js/calibration-manager.js` | CalibrationManager class — human reference file upload, comparison snapshot logging, report export |
| `css/review-styles.css` | Review page-specific styles — three-panel layout, toolbar row, sync buttons, raw HTML view, file map sidebar, responsive breakpoints |
| `tests/reviewPageChanges.test.js` | 72 tests covering Phase 11 toolbar relocation, Conversion Error Log rename, Phase 12 per-panel Sync buttons, scroll-position preservation, normaliseTextForMatch helper |

### Files Modified (4)

| File | Changes |
|------|---------|
| `index.html` | Removed `<link rel="stylesheet" href="css/review-styles.css">` stylesheet reference; removed `<button id="btn-visual-review">` ("Visual Comparison Review" button) from the global actions bar |
| `js/app.js` | Removed `_serialiseForReview()` method (JSON serialisation of all data for review page); removed `_openVisualReview()` method (sessionStorage storage + window.open); removed `_storeChunked()` method (chunked sessionStorage fallback for large payloads); removed `_clearReviewStorage()` method (sessionStorage cleanup); removed `this.btnVisualReview` DOM reference from `_bindElements()`; removed Visual Comparison Review button click event listener from `_bindEvents()`; removed visual review button enable in `_processOutput()`; removed visual review button disable in `reset()` |
| `css/styles.css` | Removed all `.calibration-*` rules (14 selectors: panel, toggle, content, description, dropzone + variants, uploaded-files, file-item + 5 sub-variants); removed all `.snapshot-*` rules (18 selectors: form, field + variants, actions, count, list, empty-state, entry + 5 sub-variants, delete, preview-text, details + summary, full-content, full-field + sub-selectors); removed `.field-hint` rule; removed `.export-actions` rule; removed responsive `@media (max-width: 768px)` rules for `.snapshot-field-inline`, `.snapshot-actions`, `.export-actions` |
| `tests/test-runner.js` | Removed `global.__testFs`, `global.__testPath`, `global.__testRootDir` assignments (only used by the deleted `reviewPageChanges.test.js`) |

### What Was NOT Removed

- `_getBlockTextForAnalysis()` in `js/app.js` — still used by `_runAnalysis()` for the debug panel tag analysis
- `config._templateAttribute` display in the debug panel — core debug functionality, not review-page-specific
- All core conversion pipeline classes and methods remain completely intact
- All 439 remaining tests continue to pass (18 test files across 17 test suites)

### Test Count Change

| Before | After | Difference |
|--------|-------|------------|
| 511 tests (19 test files) | 439 tests (18 test files) | −72 tests (1 test file removed) |

---


---

[← Back to index](../CLAUDE.md)
