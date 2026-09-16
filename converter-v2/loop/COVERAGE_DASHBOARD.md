# PageForge — corpus discrepancy dashboard

_Generated 2026-09-17 09:46 · corpus 443 modules / 2103 pages_

**What this is.** Every remaining difference between our HTML and the human's, measured across the whole library and ranked by how many modules it costs. Use it to choose the next round. It changes nothing — it only reports.

## ⚠ Freshness

- feature index predates the newest engine change (2026-09-17) — its rows may lag.

## 1. The two numbers that matter

**Interactive coverage — 51.5%** (2550 of 4953 writer-tagged widgets actually build).
The other 2403 ship as a hand-off box. This is what a tester sees when they say the conversion looks unfinished, and it is invisible to the protected gates by design.

**Page scaffold match — 51.0% mean** (1072 of 1955 pages at 50%+, 159 at 75%+).
The protected primary gate. It measures page structure with widget internals collapsed, so it moves very little while coverage is the real gap.

**Structurally clean — 98.9%** (23 pages carry a visible defect)  ·  **body breakdown — 180 pages** (the protected body gate).

## 2. The ranked queue

Sorted by modules affected. `Unlock` = individual occurrences a complete fix would address. `Regen` = modules needing a rebuild, from the feature index — it deliberately **over-selects** (a module is included if the writer tagged the feature at all, even where nothing currently goes wrong), because under-selecting is the one error that ships a stale corpus.

Body rows use `body_compare.py`'s own thresholds, so this table and the protected gate always agree.

| # | Class | Modules | Pages | Unlock | Shapes | Regen | What it is |
|---|---|--:|--:|--:|--:|--:|---|
| 1 | un-built dragAndDrop | 287 | 573 | 795 | 663 | 309 (32% skipped) | Writers tagged 882 dragAndDrop widgets; 795 ship as a hand-off box instead of a built widget. |
| 2 | content lost vs the human (advisory) | 185 | 418 | 418 | — | — | The human page carries 3+ body blocks ours does not, without tripping the over-capture rule — content is going missing by some other route. |
| 3 | un-built carousel | 141 | 187 | 240 | 181 | 342 (25% skipped) | Writers tagged 903 carousel widgets; 240 ship as a hand-off box instead of a built widget. |
| 4 | page scaffold under 25% | 129 | 165 | 165 | — | — | The page's overall structure barely resembles the human's — these are the pages a tester screenshots. |
| 5 | un-built flipCard | 121 | 168 | 215 | 179 | 222 (51% skipped) | Writers tagged 484 flipCard widgets; 215 ship as a hand-off box instead of a built widget. |
| 6 | un-built accordion | 109 | 178 | 250 | 214 | 212 (53% skipped) | Writers tagged 705 accordion widgets; 250 ship as a hand-off box instead of a built widget. |
| 7 | un-built clickDrop | 107 | 173 | 323 | 230 | 158 (65% skipped) | Writers tagged 516 clickDrop widgets; 323 ship as a hand-off box instead of a built widget. |
| 8 | empty widget box | 99 | 135 | 135 | — | — | A hand-off box was emitted with nothing in it. |
| 9 | un-built selfCheck | 65 | 96 | 153 | 98 | 188 (59% skipped) | Writers tagged 153 selfCheck widgets; 153 ship as a hand-off box instead of a built widget. |
| 10 | un-built modal | 60 | 94 | 157 | 130 | 114 (75% skipped) | Writers tagged 359 modal widgets; 157 ship as a hand-off box instead of a built widget. |
| 11 | un-built tabs | 45 | 67 | 76 | 71 | 84 (81% skipped) | Writers tagged 122 tabs widgets; 76 ship as a hand-off box instead of a built widget. |
| 12 | widget over-capture | 35 | 42 | 42 | — | — | A widget's capture ran past its boundary and swallowed body the human keeps free (gate rule: 40%+ of the page in one widget, 400+ chars, 3+ blocks lost). |
| 13 | un-built speechBubble | 33 | 43 | 53 | 40 | 112 (75% skipped) | Writers tagged 604 speechBubble widgets; 53 ship as a hand-off box instead of a built widget. |
| 14 | un-built slider | 30 | 41 | 47 | 38 | 36 (92% skipped) | Writers tagged 47 slider widgets; 47 ship as a hand-off box instead of a built widget. |
| 15 | un-built infoTrigger | 22 | 31 | 37 | 31 | 224 (51% skipped) | Writers tagged 37 infoTrigger widgets; 37 ship as a hand-off box instead of a built widget. |
| 16 | A_literal_tag_leak | 21 | 23 | 26 | — | — | Raw writer markup like [H2] is visible as text on the finished page. |
| 17 | un-built shapeHover | 16 | 25 | 27 | 25 | 16 (96% skipped) | Writers tagged 29 shapeHover widgets; 27 ship as a hand-off box instead of a built widget. |
| 18 | un-built hintSlider | 11 | 12 | 12 | 12 | 41 (91% skipped) | Writers tagged 44 hintSlider widgets; 12 ship as a hand-off box instead of a built widget. |
| 19 | un-built hint | 7 | 13 | 17 | 17 | 19 (96% skipped) | Writers tagged 66 hint widgets; 17 ship as a hand-off box instead of a built widget. |
| 20 | runaway absorption | 4 | 4 | 4 | — | — | One widget absorbed four or more different widget types — a capture that never found a terminator. |
| 21 | un-built glossary | 1 | 1 | 1 | 1 | 3 (99% skipped) | Writers tagged 2 glossary widgets; 1 ship as a hand-off box instead of a built widget. |

## 3. Interactive coverage by widget type

| Type | Built | Total | Coverage | Declined | Distinct shapes | Modules |
|---|--:|--:|--:|--:|--:|--:|
| dragAndDrop | 87 | 882 | 9.9% | 795 | 663 | 287 |
| clickDrop | 193 | 516 | 37.4% | 323 | 230 | 107 |
| accordion | 455 | 705 | 64.5% | 250 | 214 | 109 |
| carousel | 663 | 903 | 73.4% | 240 | 181 | 141 |
| flipCard | 269 | 484 | 55.6% | 215 | 179 | 121 |
| modal | 202 | 359 | 56.3% | 157 | 130 | 60 |
| selfCheck | 0 | 153 | 0.0% | 153 | 98 | 65 |
| tabs | 46 | 122 | 37.7% | 76 | 71 | 45 |
| speechBubble | 551 | 604 | 91.2% | 53 | 40 | 33 |
| slider | 0 | 47 | 0.0% | 47 | 38 | 30 |
| infoTrigger | 0 | 37 | 0.0% | 37 | 31 | 22 |
| shapeHover | 2 | 29 | 6.9% | 27 | 25 | 16 |
| hint | 49 | 66 | 74.2% | 17 | 17 | 7 |
| hintSlider | 32 | 44 | 72.7% | 12 | 12 | 11 |
| glossary | 1 | 2 | 50.0% | 1 | 1 | 1 |

**Read the shapes column as a warning.** A type declining across hundreds of distinct authoring shapes cannot be closed one shape per round. The lever is section 4.

## 4. Cross-cutting blockers — fix these, not the shapes

A blocker is something a builder almost never accepts. Every shape carrying it fails, so one change to the fallback's vocabulary clears many shapes at once.

| Inside | The builder refuses | Declines | Builds | Build rate |
|---|---|--:|--:|--:|
| dragAndDrop | `(a captured TABLE)` | 566 | 87 | 13% |
| dragAndDrop | `button+txt` | 78 | 8 | 9% |
| carousel | `embed` | 59 | 1 | 2% |
| clickDrop | `button+txt` | 44 | 7 | 14% |
| clickDrop | `video:yt` | 36 | 6 | 14% |
| dragAndDrop | `audio` | 25 | 0 | 0% |

**No builder at all: infoTrigger, selfCheck, slider** — 237 tagged widgets with no code path whatsoever. The single largest untouched block in the corpus.

## 5. Worst pages right now

Lowest structural match in the library, with the likeliest cause attached. These are what a tester will screenshot.

| Module | Page | Scaffold | Likely cause |
|---|---|--:|---|
| MXFUN01 | MXFUN01_0_0.html | 0.7% | 1 content blocks missing |
| ARFUN04 | ARFUN04_0_0.html | 0.9% | widget over-capture; 1 empty widget boxes |
| MXFUN02 | MXFUN02_0_0.html | 2.9% | widget over-capture; 1 empty widget boxes |
| MXFUN03 | MXFUN03_0_0.html | 3.4% | widget over-capture; 1 empty widget boxes |
| EXPFUN03 | EXPFUN03_0_0.html | 3.5% | structural — inspect |
| EXPFUN05 | EXPFUN05_0_0.html | 3.7% | widget over-capture |
| BLL144 | BLL144_1_0.html | 3.7% | widget over-capture |
| BLL240 | BLL240_1_0.html | 4.5% | structural — inspect |
| EXPFUN04 | EXPFUN04_0_0.html | 4.6% | 1 empty widget boxes |
| EXPFUN02 | EXPFUN02_0_0.html | 4.9% | structural — inspect |
| BLL110 | BLL110_0_0.html | 5.3% | widget over-capture |
| BLL120 | BLL120_0_0.html | 5.8% | widget over-capture |
| CEDT104 | CEDT104_0_0.html | 6.0% | widget over-capture; 1 empty widget boxes |
| TEDC401 | TEDC401_3_0.html | 6.1% | widget over-capture; 1 empty widget boxes |
| CEDW201 | CEDW201_0_0.html | 6.5% | 1 un-built widgets |
| TWHK901 | TWHK901_0_0.html | 6.9% | 26 content blocks missing; widget over-capture |
| TRR304 | TRR304_3_0.html | 7.5% | widget over-capture |
| TWHA901 | TWHA901_0_0.html | 7.6% | widget over-capture |
| EXIP901 | EXIP901_4_0.html | 7.7% | widget over-capture |
| XGF9001 | XGF9001_2_0.html | 7.7% | widget over-capture |
| SSFUN07 | SSFUN07_3_0.html | 7.8% | widget over-capture |
| TWHA905 | TWHA905_0_0.html | 8.3% | widget over-capture |
| XDLS911 | XDLS911_1_0.html | 9.0% | widget over-capture |
| TEDC402 | TEDC402_8_0.html | 9.3% | widget over-capture; 1 empty widget boxes |
| TEFUN03 | TEFUN03_0_0.html | 9.8% | widget over-capture |

## 6. How to use this

1. Take the top row of the queue whose fix is a **blocker** (section 4), not a shape.
2. Measure that blocker properly before writing code — the standing rule.
3. Scope the rebuild with `regen_scope.cjs --feature <name> --plan`.
4. Re-run this dashboard after the round; coverage should move, not just the gates.

**Re-run:** `python3 CONVERTER_V2/outputs/_coverage_dashboard.py --refresh`
**Rebuild the census first** (after any builder change) with `_measure_r271_variations.cjs --shard K 16` ×16, else coverage under-reports.
