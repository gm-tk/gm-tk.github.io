# 18. Tag Normalisation Robustness (Phase 1 Patch)


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


---

[← Back to index](../CLAUDE.md)
