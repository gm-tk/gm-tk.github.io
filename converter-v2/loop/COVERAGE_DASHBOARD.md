# PageForge — corpus discrepancy dashboard

_Generated 2026-09-20 15:12 · corpus 520 modules / 2548 pages_

**What this is.** Every remaining difference between our HTML and the human's, measured across the whole library and ranked by how many modules it costs. Use it to choose the next round. It changes nothing — it only reports.

## ⚠ Freshness

- body_compare predates the newest engine change (2026-09-20) — its rows may lag.
- feature index predates the newest engine change (2026-09-20) — its rows may lag.

## 1. The two numbers that matter

**Interactive coverage — 50.5%** (2877 of 5693 writer-tagged widgets actually build).
The other 2816 ship as a hand-off box. This is what a tester sees when they say the conversion looks unfinished, and it is invisible to the protected gates by design.

**Page scaffold match — 53.8% mean** (1406 of 2349 pages at 50%+, 236 at 75%+).
The protected primary gate. It measures page structure with widget internals collapsed, so it moves very little while coverage is the real gap.

**Structurally clean — 98.3%** (44 pages carry a visible defect)  ·  **body breakdown — 248 pages** (the protected body gate).

## 2. The ranked queue

Sorted by modules affected. `Unlock` = individual occurrences a complete fix would address. `Regen` = modules needing a rebuild, from the feature index — it deliberately **over-selects** (a module is included if the writer tagged the feature at all, even where nothing currently goes wrong), because under-selecting is the one error that ships a stale corpus.

Body rows use `body_compare.py`'s own thresholds, so this table and the protected gate always agree.

| # | Class | Modules | Pages | Unlock | Shapes | Regen | What it is |
|---|---|--:|--:|--:|--:|--:|---|
| 1 | un-built dragAndDrop | 331 | 654 | 907 | 741 | 357 (35% skipped) | Writers tagged 1010 dragAndDrop widgets; 907 ship as a hand-off box instead of a built widget. |
| 2 | content lost vs the human (advisory) | 225 | 523 | 523 | — | — | The human page carries 3+ body blocks ours does not, without tripping the over-capture rule — content is going missing by some other route. |
| 3 | un-built carousel | 186 | 244 | 309 | 244 | 385 (30% skipped) | Writers tagged 985 carousel widgets; 309 ship as a hand-off box instead of a built widget. |
| 4 | un-built flipCard | 146 | 204 | 254 | 216 | 259 (53% skipped) | Writers tagged 545 flipCard widgets; 254 ship as a hand-off box instead of a built widget. |
| 5 | un-built accordion | 131 | 213 | 293 | 254 | 248 (55% skipped) | Writers tagged 802 accordion widgets; 293 ship as a hand-off box instead of a built widget. |
| 6 | empty widget box | 130 | 190 | 190 | — | — | A hand-off box was emitted with nothing in it. |
| 7 | un-built clickDrop | 125 | 191 | 343 | 250 | 191 (65% skipped) | Writers tagged 578 clickDrop widgets; 343 ship as a hand-off box instead of a built widget. |
| 8 | page scaffold under 25% | 84 | 111 | 111 | — | — | The page's overall structure barely resembles the human's — these are the pages a tester screenshots. |
| 9 | un-built selfCheck | 72 | 104 | 163 | 105 | 237 (57% skipped) | Writers tagged 163 selfCheck widgets; 163 ship as a hand-off box instead of a built widget. |
| 10 | un-built modal | 68 | 103 | 170 | 141 | 126 (77% skipped) | Writers tagged 367 modal widgets; 170 ship as a hand-off box instead of a built widget. |
| 11 | un-built tabs | 61 | 97 | 117 | 107 | 104 (81% skipped) | Writers tagged 174 tabs widgets; 117 ship as a hand-off box instead of a built widget. |
| 12 | widget over-capture | 43 | 54 | 54 | — | — | A widget's capture ran past its boundary and swallowed body the human keeps free (gate rule: 40%+ of the page in one widget, 400+ chars, 3+ blocks lost). |
| 13 | un-built speechBubble | 39 | 49 | 63 | 47 | 150 (73% skipped) | Writers tagged 779 speechBubble widgets; 63 ship as a hand-off box instead of a built widget. |
| 14 | un-built slider | 33 | 44 | 52 | 42 | 39 (93% skipped) | Writers tagged 52 slider widgets; 52 ship as a hand-off box instead of a built widget. |
| 15 | A_literal_tag_leak | 31 | 44 | 73 | — | — | Raw writer markup like [H2] is visible as text on the finished page. |
| 16 | un-built infoTrigger | 25 | 34 | 42 | 36 | 273 (51% skipped) | Writers tagged 42 infoTrigger widgets; 42 ship as a hand-off box instead of a built widget. |
| 17 | un-built shapeHover | 18 | 27 | 30 | 28 | 17 (97% skipped) | Writers tagged 32 shapeHover widgets; 30 ship as a hand-off box instead of a built widget. |
| 18 | un-built hintSlider | 16 | 17 | 18 | 17 | 48 (91% skipped) | Writers tagged 59 hintSlider widgets; 18 ship as a hand-off box instead of a built widget. |
| 19 | un-built hint | 14 | 20 | 53 | 24 | 28 (95% skipped) | Writers tagged 102 hint widgets; 53 ship as a hand-off box instead of a built widget. |
| 20 | runaway absorption | 6 | 6 | 6 | — | — | One widget absorbed four or more different widget types — a capture that never found a terminator. |
| 21 | un-built glossary | 2 | 2 | 2 | 2 | 4 (99% skipped) | Writers tagged 3 glossary widgets; 2 ship as a hand-off box instead of a built widget. |

## 3. Interactive coverage by widget type

| Type | Built | Total | Coverage | Declined | Distinct shapes | Modules |
|---|--:|--:|--:|--:|--:|--:|
| dragAndDrop | 103 | 1010 | 10.2% | 907 | 741 | 331 |
| clickDrop | 235 | 578 | 40.7% | 343 | 250 | 125 |
| carousel | 676 | 985 | 68.6% | 309 | 244 | 186 |
| accordion | 509 | 802 | 63.5% | 293 | 254 | 131 |
| flipCard | 291 | 545 | 53.4% | 254 | 216 | 146 |
| modal | 197 | 367 | 53.7% | 170 | 141 | 68 |
| selfCheck | 0 | 163 | 0.0% | 163 | 105 | 72 |
| tabs | 57 | 174 | 32.8% | 117 | 107 | 61 |
| speechBubble | 716 | 779 | 91.9% | 63 | 47 | 39 |
| hint | 49 | 102 | 48.0% | 53 | 24 | 14 |
| slider | 0 | 52 | 0.0% | 52 | 42 | 33 |
| infoTrigger | 0 | 42 | 0.0% | 42 | 36 | 25 |
| shapeHover | 2 | 32 | 6.2% | 30 | 28 | 18 |
| hintSlider | 41 | 59 | 69.5% | 18 | 17 | 16 |
| glossary | 1 | 3 | 33.3% | 2 | 2 | 2 |

**Read the shapes column as a warning.** A type declining across hundreds of distinct authoring shapes cannot be closed one shape per round. The lever is section 4.

## 4. Cross-cutting blockers — fix these, not the shapes

A blocker is something a builder almost never accepts. Every shape carrying it fails, so one change to the fallback's vocabulary clears many shapes at once.

| Inside | The builder refuses | Declines | Builds | Build rate |
|---|---|--:|--:|--:|
| dragAndDrop | `(a captured TABLE)` | 635 | 103 | 14% |
| dragAndDrop | `button+txt` | 90 | 9 | 9% |
| carousel | `embed` | 59 | 1 | 2% |
| clickDrop | `video:yt` | 37 | 6 | 14% |
| dragAndDrop | `audio` | 25 | 0 | 0% |

**No builder at all: infoTrigger, selfCheck, slider** — 257 tagged widgets with no code path whatsoever. The single largest untouched block in the corpus.

## 5. Worst pages right now

Lowest structural match in the library, with the likeliest cause attached. These are what a tester will screenshot.

| Module | Page | Scaffold | Likely cause |
|---|---|--:|---|
| MXFUN01 | MXFUN01_0_0.html | 0.7% | 1 content blocks missing |
| BLL240 | BLL240_1_0.html | 4.5% | structural — inspect |
| MXFUN02 | MXFUN02_0_0.html | 5.8% | widget over-capture; 1 empty widget boxes |
| JPFUN02 | JPFUN02_0_0.html | 6.0% | 47 content blocks missing; widget over-capture |
| SSFUN07 | SSFUN07_2_0.html | 6.1% | widget over-capture |
| CEDT104 | CEDT104_0_0.html | 7.0% | widget over-capture; 2 empty widget boxes |
| CEDT301 | CEDT301_6_0.html | 7.4% | widget over-capture |
| MXFUN03 | MXFUN03_0_0.html | 8.1% | widget over-capture; 1 empty widget boxes |
| TWHK901 | TWHK901_0_0.html | 9.3% | 24 content blocks missing; widget over-capture |
| JPFUN01 | JPFUN01_0_0.html | 9.3% | widget over-capture |
| TRR304 | TRR304_3_0.html | 9.5% | widget over-capture |
| ARFUN04 | ARFUN04_0_0.html | 9.8% | widget over-capture; 1 empty widget boxes |
| TWHA905 | TWHA905_0_0.html | 10.4% | widget over-capture |
| EXIP901 | EXIP901_4_0.html | 10.5% | widget over-capture |
| XDLS911 | XDLS911_1_0.html | 10.8% | widget over-capture |
| ANZHFUN05 | MODULE_0_0.html | 11.0% | widget over-capture |
| EXPFUN05 | EXPFUN05_0_0.html | 11.1% | widget over-capture |
| TRR116 | TRR116_0_0.html | 12.1% | widget over-capture |
| MXDB301 | MXDB301_3_0.html | 12.1% | 4 content blocks missing; widget over-capture |
| TEDC401 | TEDC401_3_0.html | 12.2% | widget over-capture; 1 empty widget boxes |
| ENGJ302 | ENGJ302_1_0.html | 12.3% | 15 content blocks missing |
| CHI1004 | CHI1004_7_0.html | 13.0% | structural — inspect |
| ENGFUN02 | ENGFUN02_1_0.html | 13.4% | structural — inspect |
| CEDW201 | CEDW201_0_0.html | 13.8% | 1 un-built widgets |
| CEDT207 | CEDT207_0_0.html | 14.2% | 3 content blocks missing |

## 6. How to use this

1. Take the top row of the queue whose fix is a **blocker** (section 4), not a shape.
2. Measure that blocker properly before writing code — the standing rule.
3. Scope the rebuild with `regen_scope.cjs --feature <name> --plan`.
4. Re-run this dashboard after the round; coverage should move, not just the gates.

**Re-run:** `python3 CONVERTER_V2/outputs/_coverage_dashboard.py --refresh`
**Rebuild the census first** (after any builder change) with `_measure_r271_variations.cjs --shard K 16` ×16, else coverage under-reports.
