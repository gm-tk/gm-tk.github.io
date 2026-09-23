# PageForge — corpus discrepancy dashboard

_Generated 2026-09-24 04:52 · corpus 535 modules / 2658 pages_

**What this is.** Every remaining difference between our HTML and the human's, measured across the whole library and ranked by how many modules it costs. Use it to choose the next round. It changes nothing — it only reports.

## ⚠ Freshness

- skeleton state predates the newest engine change (2026-09-24) — its rows may lag.
- body_compare predates the newest engine change (2026-09-24) — its rows may lag.
- feature index predates the newest engine change (2026-09-24) — its rows may lag.

## 1. The two numbers that matter

**Interactive coverage — 44.9%** (3271 of 7286 writer-tagged widgets actually build).
The other 4015 ship as a hand-off box. This is what a tester sees when they say the conversion looks unfinished, and it is invisible to the protected gates by design.

**Page scaffold match — 54.7% mean** (1544 of 2477 pages at 50%+, 260 at 75%+).
The protected primary gate. It measures page structure with widget internals collapsed, so it moves very little while coverage is the real gap.

**Structurally clean — 98.3%** (45 pages carry a visible defect)  ·  **body breakdown — 237 pages** (the protected body gate).

## 2. The ranked queue

Sorted by modules affected. `Unlock` = individual occurrences a complete fix would address. `Regen` = modules needing a rebuild, from the feature index — it deliberately **over-selects** (a module is included if the writer tagged the feature at all, even where nothing currently goes wrong), because under-selecting is the one error that ships a stale corpus.

Body rows use `body_compare.py`'s own thresholds, so this table and the protected gate always agree.

| # | Class | Modules | Pages | Unlock | Shapes | Regen | What it is |
|---|---|--:|--:|--:|--:|--:|---|
| 1 | un-built dragAndDrop | 338 | 641 | 922 | 774 | 357 (35% skipped) | Writers tagged 1032 dragAndDrop widgets; 922 ship as a hand-off box instead of a built widget. |
| 2 | content lost vs the human (advisory) | 226 | 534 | 534 | — | — | The human page carries 3+ body blocks ours does not, without tripping the over-capture rule — content is going missing by some other route. |
| 3 | un-built carousel | 197 | 254 | 319 | 244 | 386 (30% skipped) | Writers tagged 998 carousel widgets; 319 ship as a hand-off box instead of a built widget. |
| 4 | un-built multiChoiceQuiz | 183 | 294 | 401 | 330 | 228 (59% skipped) | Writers tagged 413 multiChoiceQuiz widgets; 401 ship as a hand-off box instead of a built widget. |
| 5 | un-built flipCard | 152 | 200 | 261 | 218 | 259 (53% skipped) | Writers tagged 551 flipCard widgets; 261 ship as a hand-off box instead of a built widget. |
| 6 | un-built dropDown | 134 | 201 | 257 | 211 | 264 (52% skipped) | Writers tagged 598 dropDown widgets; 257 ship as a hand-off box instead of a built widget. |
| 7 | empty widget box | 132 | 176 | 176 | — | — | A hand-off box was emitted with nothing in it. |
| 8 | un-built accordion | 131 | 212 | 293 | 254 | 248 (55% skipped) | Writers tagged 803 accordion widgets; 293 ship as a hand-off box instead of a built widget. |
| 9 | un-built clickDrop | 126 | 181 | 346 | 252 | 191 (65% skipped) | Writers tagged 581 clickDrop widgets; 346 ship as a hand-off box instead of a built widget. |
| 10 | un-built typing | 83 | 169 | 262 | 233 | 237 (57% skipped) | Writers tagged 270 typing widgets; 262 ship as a hand-off box instead of a built widget. |
| 11 | page scaffold under 25% | 77 | 105 | 105 | — | — | The page's overall structure barely resembles the human's — these are the pages a tester screenshots. |
| 12 | un-built selfCheck | 71 | 103 | 137 | 103 | 237 (57% skipped) | Writers tagged 163 selfCheck widgets; 137 ship as a hand-off box instead of a built widget. |
| 13 | un-built modal | 68 | 101 | 170 | 136 | 126 (77% skipped) | Writers tagged 367 modal widgets; 170 ship as a hand-off box instead of a built widget. |
| 14 | un-built reorder | 65 | 88 | 104 | 98 | 75 (86% skipped) | Writers tagged 104 reorder widgets; 104 ship as a hand-off box instead of a built widget. |
| 15 | un-built radioQuiz | 60 | 74 | 89 | 84 | 73 (87% skipped) | Writers tagged 89 radioQuiz widgets; 89 ship as a hand-off box instead of a built widget. |
| 16 | un-built tabs | 57 | 93 | 112 | 104 | 104 (81% skipped) | Writers tagged 169 tabs widgets; 112 ship as a hand-off box instead of a built widget. |
| 17 | widget over-capture | 46 | 58 | 58 | — | — | A widget's capture ran past its boundary and swallowed body the human keeps free (gate rule: 40%+ of the page in one widget, 400+ chars, 3+ blocks lost). |
| 18 | un-built speechBubble | 45 | 55 | 69 | 48 | 150 (73% skipped) | Writers tagged 782 speechBubble widgets; 69 ship as a hand-off box instead of a built widget. |
| 19 | un-built selectionBox | 39 | 56 | 80 | 62 | 65 (88% skipped) | Writers tagged 80 selectionBox widgets; 80 ship as a hand-off box instead of a built widget. |
| 20 | un-built slider | 33 | 44 | 52 | 42 | 39 (93% skipped) | Writers tagged 52 slider widgets; 52 ship as a hand-off box instead of a built widget. |
| 21 | A_literal_tag_leak | 32 | 45 | 75 | — | — | Raw writer markup like [H2] is visible as text on the finished page. |
| 22 | un-built infoTrigger | 26 | 35 | 43 | 37 | 276 (50% skipped) | Writers tagged 43 infoTrigger widgets; 43 ship as a hand-off box instead of a built widget. |
| 23 | un-built shapeHover | 18 | 27 | 30 | 28 | 17 (97% skipped) | Writers tagged 32 shapeHover widgets; 30 ship as a hand-off box instead of a built widget. |
| 24 | un-built hintSlider | 16 | 17 | 18 | 17 | 51 (91% skipped) | Writers tagged 59 hintSlider widgets; 18 ship as a hand-off box instead of a built widget. |
| 25 | un-built hint | 14 | 20 | 48 | 22 | 28 (95% skipped) | Writers tagged 97 hint widgets; 48 ship as a hand-off box instead of a built widget. |
| 26 | runaway absorption | 5 | 5 | 5 | — | — | One widget absorbed four or more different widget types — a capture that never found a terminator. |
| 27 | un-built glossary | 2 | 2 | 2 | 2 | 4 (99% skipped) | Writers tagged 3 glossary widgets; 2 ship as a hand-off box instead of a built widget. |

## 3. Interactive coverage by widget type

| Type | Built | Total | Coverage | Declined | Distinct shapes | Modules |
|---|--:|--:|--:|--:|--:|--:|
| dragAndDrop | 110 | 1032 | 10.7% | 922 | 774 | 338 |
| multiChoiceQuiz | 12 | 413 | 2.9% | 401 | 330 | 183 |
| clickDrop | 235 | 581 | 40.4% | 346 | 252 | 126 |
| carousel | 679 | 998 | 68.0% | 319 | 244 | 197 |
| accordion | 510 | 803 | 63.5% | 293 | 254 | 131 |
| typing | 8 | 270 | 3.0% | 262 | 233 | 83 |
| flipCard | 290 | 551 | 52.6% | 261 | 218 | 152 |
| dropDown | 341 | 598 | 57.0% | 257 | 211 | 134 |
| modal | 197 | 367 | 53.7% | 170 | 136 | 68 |
| selfCheck | 26 | 163 | 16.0% | 137 | 103 | 71 |
| tabs | 57 | 169 | 33.7% | 112 | 104 | 57 |
| reorder | 0 | 104 | 0.0% | 104 | 98 | 65 |
| radioQuiz | 0 | 89 | 0.0% | 89 | 84 | 60 |
| selectionBox | 0 | 80 | 0.0% | 80 | 62 | 39 |
| speechBubble | 713 | 782 | 91.2% | 69 | 48 | 45 |
| slider | 0 | 52 | 0.0% | 52 | 42 | 33 |
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
| dragAndDrop | `(a captured TABLE)` | 654 | 110 | 14% |
| multiChoiceQuiz | `mcq` | 290 | 11 | 4% |
| typing | `(a captured TABLE)` | 147 | 0 | 0% |
| multiChoiceQuiz | `(a captured TABLE)` | 144 | 0 | 0% |
| dropDown | `(a captured TABLE)` | 101 | 11 | 10% |
| dragAndDrop | `button+txt` | 99 | 9 | 8% |
| multiChoiceQuiz | `mcq+txt` | 88 | 1 | 1% |
| carousel | `embed` | 59 | 1 | 2% |
| dropDown | `button+txt` | 43 | 3 | 6% |
| clickDrop | `video:yt` | 37 | 6 | 14% |
| multiChoiceQuiz | `button+txt` | 34 | 0 | 0% |
| dragAndDrop | `audio` | 25 | 0 | 0% |
| dragAndDrop | `answer` | 25 | 0 | 0% |

**No builder at all: infoTrigger, radioQuiz, reorder, selectionBox, slider** — 368 tagged widgets with no code path whatsoever. The single largest untouched block in the corpus.

## 5. Worst pages right now

Lowest structural match in the library, with the likeliest cause attached. These are what a tester will screenshot.

| Module | Page | Scaffold | Likely cause |
|---|---|--:|---|
| MXFUN01 | MXFUN01_0_0.html | 5.5% | widget over-capture |
| JPFUN02 | JPFUN02_0_0.html | 6.0% | 47 content blocks missing; widget over-capture |
| SSFUN07 | SSFUN07_2_0.html | 6.1% | widget over-capture |
| MXFUN02 | MXFUN02_0_0.html | 8.0% | widget over-capture; 2 empty widget boxes |
| ANZHFUN05 | ANZHFUN05_0_0.html | 9.1% | widget over-capture |
| TRR304 | TRR304_3_0.html | 9.5% | widget over-capture |
| ARFUN04 | ARFUN04_0_0.html | 9.8% | widget over-capture; 1 empty widget boxes |
| EXIP901 | EXIP901_4_0.html | 10.0% | widget over-capture |
| XDLS911 | XDLS911_1_0.html | 10.8% | widget over-capture |
| EXPFUN05 | EXPFUN05_0_0.html | 11.1% | widget over-capture |
| XOTPB08 | XOTPB08_2_0.html | 12.0% | widget over-capture |
| MXDB301 | MXDB301_3_0.html | 12.0% | 4 content blocks missing; widget over-capture |
| TRR116 | TRR116_0_0.html | 12.1% | widget over-capture |
| ENGJ302 | ENGJ302_1_0.html | 12.3% | 15 content blocks missing |
| CHI1004 | CHI1004_7_0.html | 13.0% | structural — inspect |
| TEDC401 | TEDC401_3_0.html | 13.4% | widget over-capture; 1 empty widget boxes |
| ENGFUN02 | ENGFUN02_1_0.html | 13.4% | structural — inspect |
| JPFUN01 | JPFUN01_0_0.html | 13.7% | widget over-capture |
| PWYWHA1 | PWYWHA1_0_0.html | 13.8% | 12 content blocks missing; widget over-capture |
| MXDI103 | MXDI103_8_0.html | 14.4% | 1 content blocks missing; widget over-capture |
| PES1007 | PES1007_7_0.html | 14.4% | 15 content blocks missing |
| EXPFUN03 | EXPFUN03_0_0.html | 14.8% | structural — inspect |
| TEFUN03 | TEFUN03_0_0.html | 14.9% | widget over-capture |
| GER1002 | GER1002_2_0.html | 15.0% | widget over-capture; 3 empty widget boxes |
| ANZH301 | ANZH301_1_0.html | 15.0% | 11 content blocks missing; widget over-capture |

## 6. How to use this

1. Take the top row of the queue whose fix is a **blocker** (section 4), not a shape.
2. Measure that blocker properly before writing code — the standing rule.
3. Scope the rebuild with `regen_scope.cjs --feature <name> --plan`.
4. Re-run this dashboard after the round; coverage should move, not just the gates.

**Re-run:** `python3 CONVERTER_V2/outputs/_coverage_dashboard.py --refresh`
**Rebuild the census first** (after any builder change) with `_measure_r271_variations.cjs --shard K 16` ×16, else coverage under-reports.
