# 16. ENGS301 Inconsistency Fixes


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


---

[← Back to index](../CLAUDE.md)
