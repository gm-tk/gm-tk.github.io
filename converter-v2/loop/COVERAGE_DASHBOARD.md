# PageForge — corpus discrepancy dashboard

_Generated 2026-09-26 04:53 · corpus 535 modules / 2627 pages_

**What this is.** Every remaining difference between our HTML and the human's, measured across the whole library and ranked by how many modules it costs. Use it to choose the next round. It changes nothing — it only reports.

## ⚠ Freshness

- skeleton state predates the newest engine change (2026-09-25) — its rows may lag.
- feature index predates the newest engine change (2026-09-26) — its rows may lag.

## 1. The two numbers that matter

**Interactive coverage — 45.4%** (3450 of 7593 writer-tagged widgets actually build).
The other 4143 ship as a hand-off box. This is what a tester sees when they say the conversion looks unfinished, and it is invisible to the protected gates by design.

**Page scaffold match — 55.5% mean** (1592 of 2491 pages at 50%+, 277 at 75%+).
The protected primary gate. It measures page structure with widget internals collapsed, so it moves very little while coverage is the real gap.

**Structurally clean — 98.4%** (42 pages carry a visible defect)  ·  **body breakdown — 235 pages** (the protected body gate).

## 2. The ranked queue

Sorted by modules affected. `Unlock` = individual occurrences a complete fix would address. `Regen` = modules needing a rebuild, from the feature index — it deliberately **over-selects** (a module is included if the writer tagged the feature at all, even where nothing currently goes wrong), because under-selecting is the one error that ships a stale corpus.

Body rows use `body_compare.py`'s own thresholds, so this table and the protected gate always agree.

| # | Class | Modules | Pages | Unlock | Shapes | Regen | What it is |
|---|---|--:|--:|--:|--:|--:|---|
| 1 | un-built dragAndDrop | 367 | 715 | 1019 | 863 | 390 (29% skipped) | Writers tagged 1158 dragAndDrop widgets; 1019 ship as a hand-off box instead of a built widget. |
| 2 | content lost vs the human (advisory) | 218 | 493 | 493 | — | — | The human page carries 3+ body blocks ours does not, without tripping the over-capture rule — content is going missing by some other route. |
| 3 | un-built multiChoiceQuiz | 188 | 310 | 433 | 358 | 235 (57% skipped) | Writers tagged 449 multiChoiceQuiz widgets; 433 ship as a hand-off box instead of a built widget. |
| 4 | un-built carousel | 175 | 198 | 260 | 211 | 391 (29% skipped) | Writers tagged 1017 carousel widgets; 260 ship as a hand-off box instead of a built widget. |
| 5 | un-built flipCard | 160 | 214 | 282 | 238 | 267 (52% skipped) | Writers tagged 590 flipCard widgets; 282 ship as a hand-off box instead of a built widget. |
| 6 | un-built dropDown | 144 | 220 | 279 | 232 | 275 (50% skipped) | Writers tagged 623 dropDown widgets; 279 ship as a hand-off box instead of a built widget. |
| 7 | un-built clickDrop | 129 | 191 | 338 | 265 | 192 (65% skipped) | Writers tagged 579 clickDrop widgets; 338 ship as a hand-off box instead of a built widget. |
| 8 | empty widget box | 129 | 172 | 172 | — | — | A hand-off box was emitted with nothing in it. |
| 9 | un-built accordion | 122 | 189 | 263 | 228 | 248 (55% skipped) | Writers tagged 803 accordion widgets; 263 ship as a hand-off box instead of a built widget. |
| 10 | un-built selfCheck | 83 | 131 | 203 | 159 | 243 (56% skipped) | Writers tagged 246 selfCheck widgets; 203 ship as a hand-off box instead of a built widget. |
| 11 | un-built typing | 83 | 146 | 193 | 171 | 240 (57% skipped) | Writers tagged 212 typing widgets; 193 ship as a hand-off box instead of a built widget. |
| 12 | un-built radioQuiz | 76 | 93 | 110 | 104 | 84 (85% skipped) | Writers tagged 110 radioQuiz widgets; 110 ship as a hand-off box instead of a built widget. |
| 13 | un-built modal | 71 | 108 | 184 | 147 | 126 (77% skipped) | Writers tagged 367 modal widgets; 184 ship as a hand-off box instead of a built widget. |
| 14 | page scaffold under 25% | 71 | 92 | 92 | — | — | The page's overall structure barely resembles the human's — these are the pages a tester screenshots. |
| 15 | un-built reorder | 67 | 95 | 115 | 107 | 77 (86% skipped) | Writers tagged 115 reorder widgets; 115 ship as a hand-off box instead of a built widget. |
| 16 | un-built tabs | 58 | 94 | 113 | 105 | 104 (81% skipped) | Writers tagged 170 tabs widgets; 113 ship as a hand-off box instead of a built widget. |
| 17 | widget over-capture | 50 | 60 | 60 | — | — | A widget's capture ran past its boundary and swallowed body the human keeps free (gate rule: 40%+ of the page in one widget, 400+ chars, 3+ blocks lost). |
| 18 | un-built speechBubble | 45 | 54 | 68 | 47 | 150 (73% skipped) | Writers tagged 778 speechBubble widgets; 68 ship as a hand-off box instead of a built widget. |
| 19 | un-built selectionBox | 44 | 63 | 87 | 69 | 74 (87% skipped) | Writers tagged 87 selectionBox widgets; 87 ship as a hand-off box instead of a built widget. |
| 20 | un-built slider | 36 | 47 | 55 | 45 | 42 (92% skipped) | Writers tagged 55 slider widgets; 55 ship as a hand-off box instead of a built widget. |
| 21 | A_literal_tag_leak | 29 | 42 | 52 | — | — | Raw writer markup like [H2] is visible as text on the finished page. |
| 22 | un-built infoTrigger | 26 | 35 | 43 | 37 | 277 (50% skipped) | Writers tagged 43 infoTrigger widgets; 43 ship as a hand-off box instead of a built widget. |
| 23 | un-built shapeHover | 18 | 27 | 30 | 28 | 18 (97% skipped) | Writers tagged 32 shapeHover widgets; 30 ship as a hand-off box instead of a built widget. |
| 24 | un-built hintSlider | 16 | 17 | 18 | 17 | 51 (91% skipped) | Writers tagged 59 hintSlider widgets; 18 ship as a hand-off box instead of a built widget. |
| 25 | un-built hint | 14 | 20 | 48 | 22 | 28 (95% skipped) | Writers tagged 97 hint widgets; 48 ship as a hand-off box instead of a built widget. |
| 26 | runaway absorption | 6 | 6 | 6 | — | — | One widget absorbed four or more different widget types — a capture that never found a terminator. |
| 27 | un-built glossary | 2 | 2 | 2 | 2 | 4 (99% skipped) | Writers tagged 3 glossary widgets; 2 ship as a hand-off box instead of a built widget. |

## 3. Interactive coverage by widget type

| Type | Built | Total | Coverage | Declined | Distinct shapes | Modules |
|---|--:|--:|--:|--:|--:|--:|
| dragAndDrop | 139 | 1158 | 12.0% | 1019 | 863 | 367 |
| multiChoiceQuiz | 16 | 449 | 3.6% | 433 | 358 | 188 |
| clickDrop | 241 | 579 | 41.6% | 338 | 265 | 129 |
| flipCard | 308 | 590 | 52.2% | 282 | 238 | 160 |
| dropDown | 344 | 623 | 55.2% | 279 | 232 | 144 |
| accordion | 540 | 803 | 67.2% | 263 | 228 | 122 |
| carousel | 757 | 1017 | 74.4% | 260 | 211 | 175 |
| selfCheck | 43 | 246 | 17.5% | 203 | 159 | 83 |
| typing | 19 | 212 | 9.0% | 193 | 171 | 83 |
| modal | 183 | 367 | 49.9% | 184 | 147 | 71 |
| reorder | 0 | 115 | 0.0% | 115 | 107 | 67 |
| tabs | 57 | 170 | 33.5% | 113 | 105 | 58 |
| radioQuiz | 0 | 110 | 0.0% | 110 | 104 | 76 |
| selectionBox | 0 | 87 | 0.0% | 87 | 69 | 44 |
| speechBubble | 710 | 778 | 91.3% | 68 | 47 | 45 |
| slider | 0 | 55 | 0.0% | 55 | 45 | 36 |
| hint | 49 | 97 | 50.5% | 48 | 22 | 14 |
| infoTrigger | 0 | 43 | 0.0% | 43 | 37 | 26 |
| shapeHover | 2 | 32 | 6.2% | 30 | 28 | 18 |
| hintSlider | 41 | 59 | 69.5% | 18 | 17 | 16 |
| glossary | 1 | 3 | 33.3% | 2 | 2 | 2 |

**Read the shapes column as a warning.** A type declining across hundreds of distinct authoring shapes cannot be closed one shape per round. The lever is section 4.

## 4. Cross-cutting blockers — fix these, not the shapes

A blocker is something a builder almost never accepts. Every shape carrying it fails, so one change to the fallback's vocabulary clears many shapes at once.

| Inside | The builder refuses | Declines | Builds | Build rate |
|---|---|--:|--:|--:|
| multiChoiceQuiz | `mcq` | 307 | 15 | 5% |
| multiChoiceQuiz | `(a captured TABLE)` | 172 | 0 | 0% |
| dragAndDrop | `button+txt` | 145 | 16 | 10% |
| dropDown | `(a captured TABLE)` | 114 | 13 | 10% |
| multiChoiceQuiz | `mcq+txt` | 99 | 1 | 1% |
| typing | `(a captured TABLE)` | 87 | 11 | 11% |
| selfCheck | `button+txt` | 58 | 10 | 15% |
| dropDown | `button+txt` | 55 | 4 | 7% |
| multiChoiceQuiz | `button+txt` | 48 | 1 | 2% |
| clickDrop | `video:yt` | 37 | 6 | 14% |
| dragAndDrop | `image:istock` | 32 | 0 | 0% |
| dragAndDrop | `button` | 28 | 0 | 0% |
| dragAndDrop | `answer` | 27 | 0 | 0% |
| dragAndDrop | `audio` | 25 | 0 | 0% |
| dragAndDrop | `image` | 25 | 0 | 0% |

**No builder at all: infoTrigger, radioQuiz, reorder, selectionBox, slider** — 410 tagged widgets with no code path whatsoever. The single largest untouched block in the corpus.

## 5. Worst pages right now

Lowest structural match in the library, with the likeliest cause attached. These are what a tester will screenshot.

| Module | Page | Scaffold | Likely cause |
|---|---|--:|---|
| MXFUN01 | MXFUN01_0_0.html | 5.5% | widget over-capture |
| JPFUN02 | JPFUN02_0_0.html | 6.0% | 47 content blocks missing; widget over-capture |
| SSFUN07 | SSFUN07_2_0.html | 6.1% | widget over-capture |
| MXFUN02 | MXFUN02_0_0.html | 8.0% | widget over-capture; 4 empty widget boxes |
| ANZHFUN05 | ANZHFUN05_0_0.html | 9.1% | widget over-capture |
| ARFUN04 | ARFUN04_0_0.html | 9.8% | widget over-capture; 1 empty widget boxes |
| TRR304 | TRR304_3_0.html | 10.0% | 8 content blocks missing; widget over-capture |
| EXIP901 | EXIP901_4_0.html | 10.0% | widget over-capture |
| XDLS911 | XDLS911_1_0.html | 10.8% | widget over-capture |
| EXPFUN05 | EXPFUN05_0_0.html | 11.1% | widget over-capture |
| XOTPB08 | XOTPB08_2_0.html | 12.0% | widget over-capture |
| MXDB301 | MXDB301_3_0.html | 12.0% | 4 content blocks missing; widget over-capture |
| ENGJ302 | ENGJ302_1_0.html | 12.3% | 15 content blocks missing |
| TEDC401 | TEDC401_3_0.html | 13.4% | widget over-capture; 1 empty widget boxes |
| ENGFUN02 | ENGFUN02_1_0.html | 13.4% | structural — inspect |
| JPFUN01 | JPFUN01_0_0.html | 13.7% | widget over-capture |
| PWYWHA1 | PWYWHA1_0_0.html | 13.8% | 12 content blocks missing; widget over-capture |
| MXDI103 | MXDI103_8_0.html | 14.4% | 1 content blocks missing; widget over-capture |
| PES1007 | PES1007_7_0.html | 14.4% | 15 content blocks missing |
| TEFUN03 | TEFUN03_0_0.html | 14.7% | widget over-capture |
| EXPFUN03 | EXPFUN03_0_0.html | 14.8% | structural — inspect |
| GER1002 | GER1002_2_0.html | 15.0% | widget over-capture; 3 empty widget boxes |
| ANZH301 | ANZH301_1_0.html | 15.0% | 11 content blocks missing; widget over-capture |
| MXFL401 | MXFL401_2_0.html | 15.2% | 15 content blocks missing; widget over-capture |
| SSOG301 | SSOG301_6_0.html | 15.3% | widget over-capture |

## 6. How to use this

1. Take the top row of the queue whose fix is a **blocker** (section 4), not a shape.
2. Measure that blocker properly before writing code — the standing rule.
3. Scope the rebuild with `regen_scope.cjs --feature <name> --plan`.
4. Re-run this dashboard after the round; coverage should move, not just the gates.

**Re-run:** `python3 CONVERTER_V2/outputs/_coverage_dashboard.py --refresh`
**Rebuild the census first** (after any builder change) with `_measure_r271_variations.cjs --shard K 16` ×16, else coverage under-reports.
