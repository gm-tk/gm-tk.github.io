# PageForge — corpus discrepancy dashboard

_Generated 2026-09-22 11:54 · corpus 534 modules / 2736 pages_

**What this is.** Every remaining difference between our HTML and the human's, measured across the whole library and ranked by how many modules it costs. Use it to choose the next round. It changes nothing — it only reports.

## ⚠ Freshness

- **Census is stale** — the interactive census predates the newest engine/data change (2026-09-22 vs 2026-09-22) — coverage is UNDER-reported until it is rebuilt.
- body_compare predates the newest engine change (2026-09-22) — its rows may lag.

## 1. The two numbers that matter

**Interactive coverage — 50.7%** (2902 of 5723 writer-tagged widgets actually build).
The other 2821 ship as a hand-off box. This is what a tester sees when they say the conversion looks unfinished, and it is invisible to the protected gates by design.

**Page scaffold match — 54.1% mean** (1531 of 2491 pages at 50%+, 254 at 75%+).
The protected primary gate. It measures page structure with widget internals collapsed, so it moves very little while coverage is the real gap.

**Structurally clean — 98.3%** (46 pages carry a visible defect)  ·  **body breakdown — 265 pages** (the protected body gate).

## 2. The ranked queue

Sorted by modules affected. `Unlock` = individual occurrences a complete fix would address. `Regen` = modules needing a rebuild, from the feature index — it deliberately **over-selects** (a module is included if the writer tagged the feature at all, even where nothing currently goes wrong), because under-selecting is the one error that ships a stale corpus.

Body rows use `body_compare.py`'s own thresholds, so this table and the protected gate always agree.

| # | Class | Modules | Pages | Unlock | Shapes | Regen | What it is |
|---|---|--:|--:|--:|--:|--:|---|
| 1 | un-built dragAndDrop | 338 | 667 | 919 | 771 | 357 (35% skipped) | Writers tagged 1029 dragAndDrop widgets; 919 ship as a hand-off box instead of a built widget. |
| 2 | content lost vs the human (advisory) | 241 | 540 | 540 | — | — | The human page carries 3+ body blocks ours does not, without tripping the over-capture rule — content is going missing by some other route. |
| 3 | un-built carousel | 197 | 255 | 320 | 246 | 386 (30% skipped) | Writers tagged 996 carousel widgets; 320 ship as a hand-off box instead of a built widget. |
| 4 | un-built flipCard | 152 | 210 | 260 | 217 | 259 (53% skipped) | Writers tagged 550 flipCard widgets; 260 ship as a hand-off box instead of a built widget. |
| 5 | empty widget box | 143 | 206 | 206 | — | — | A hand-off box was emitted with nothing in it. |
| 6 | un-built accordion | 131 | 213 | 293 | 254 | 248 (55% skipped) | Writers tagged 802 accordion widgets; 293 ship as a hand-off box instead of a built widget. |
| 7 | un-built clickDrop | 125 | 191 | 343 | 250 | 191 (65% skipped) | Writers tagged 578 clickDrop widgets; 343 ship as a hand-off box instead of a built widget. |
| 8 | page scaffold under 25% | 102 | 130 | 130 | — | — | The page's overall structure barely resembles the human's — these are the pages a tester screenshots. |
| 9 | un-built selfCheck | 71 | 103 | 137 | 103 | 237 (57% skipped) | Writers tagged 163 selfCheck widgets; 137 ship as a hand-off box instead of a built widget. |
| 10 | un-built modal | 68 | 103 | 170 | 141 | 126 (77% skipped) | Writers tagged 367 modal widgets; 170 ship as a hand-off box instead of a built widget. |
| 11 | un-built tabs | 61 | 97 | 117 | 107 | 104 (81% skipped) | Writers tagged 174 tabs widgets; 117 ship as a hand-off box instead of a built widget. |
| 12 | widget over-capture | 46 | 57 | 57 | — | — | A widget's capture ran past its boundary and swallowed body the human keeps free (gate rule: 40%+ of the page in one widget, 400+ chars, 3+ blocks lost). |
| 13 | un-built speechBubble | 45 | 55 | 69 | 48 | 150 (73% skipped) | Writers tagged 778 speechBubble widgets; 69 ship as a hand-off box instead of a built widget. |
| 14 | un-built slider | 33 | 44 | 52 | 42 | 39 (93% skipped) | Writers tagged 52 slider widgets; 52 ship as a hand-off box instead of a built widget. |
| 15 | A_literal_tag_leak | 32 | 46 | 75 | — | — | Raw writer markup like [H2] is visible as text on the finished page. |
| 16 | un-built infoTrigger | 26 | 35 | 43 | 37 | 276 (50% skipped) | Writers tagged 43 infoTrigger widgets; 43 ship as a hand-off box instead of a built widget. |
| 17 | un-built shapeHover | 18 | 27 | 30 | 28 | 17 (97% skipped) | Writers tagged 32 shapeHover widgets; 30 ship as a hand-off box instead of a built widget. |
| 18 | un-built hintSlider | 16 | 17 | 18 | 17 | 51 (91% skipped) | Writers tagged 59 hintSlider widgets; 18 ship as a hand-off box instead of a built widget. |
| 19 | un-built hint | 14 | 20 | 48 | 22 | 28 (95% skipped) | Writers tagged 97 hint widgets; 48 ship as a hand-off box instead of a built widget. |
| 20 | runaway absorption | 5 | 5 | 5 | — | — | One widget absorbed four or more different widget types — a capture that never found a terminator. |
| 21 | un-built glossary | 2 | 2 | 2 | 2 | 4 (99% skipped) | Writers tagged 3 glossary widgets; 2 ship as a hand-off box instead of a built widget. |

## 3. Interactive coverage by widget type

| Type | Built | Total | Coverage | Declined | Distinct shapes | Modules |
|---|--:|--:|--:|--:|--:|--:|
| dragAndDrop | 110 | 1029 | 10.7% | 919 | 771 | 338 |
| clickDrop | 235 | 578 | 40.7% | 343 | 250 | 125 |
| carousel | 676 | 996 | 67.9% | 320 | 246 | 197 |
| accordion | 509 | 802 | 63.5% | 293 | 254 | 131 |
| flipCard | 290 | 550 | 52.7% | 260 | 217 | 152 |
| modal | 197 | 367 | 53.7% | 170 | 141 | 68 |
| selfCheck | 26 | 163 | 16.0% | 137 | 103 | 71 |
| tabs | 57 | 174 | 32.8% | 117 | 107 | 61 |
| speechBubble | 709 | 778 | 91.1% | 69 | 48 | 45 |
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
| dragAndDrop | `(a captured TABLE)` | 651 | 110 | 14% |
| dragAndDrop | `button+txt` | 95 | 9 | 9% |
| carousel | `embed` | 59 | 1 | 2% |
| clickDrop | `video:yt` | 37 | 6 | 14% |
| dragAndDrop | `audio` | 25 | 0 | 0% |
| dragAndDrop | `answer` | 25 | 0 | 0% |

**No builder at all: infoTrigger, slider** — 95 tagged widgets with no code path whatsoever. The single largest untouched block in the corpus.

## 5. Worst pages right now

Lowest structural match in the library, with the likeliest cause attached. These are what a tester will screenshot.

| Module | Page | Scaffold | Likely cause |
|---|---|--:|---|
| MXFUN01 | MXFUN01_0_0.html | 0.7% | 1 content blocks missing |
| BLL260 | BLL260_6_1.html | 3.2% | widget over-capture; 1 empty widget boxes |
| BLL240 | BLL240_1_0.html | 4.5% | structural — inspect |
| BLL250 | BLL250_2_5.html | 4.9% | widget over-capture; 1 empty widget boxes |
| BLL270 | BLL270_2_0.html | 5.2% | widget over-capture; 1 empty widget boxes |
| TWHT903 | TWHT903_1_0.html | 5.4% | widget over-capture |
| CEDK401 | CEDK401_2_0.html | 5.7% | widget over-capture |
| MXFUN02 | MXFUN02_0_0.html | 5.8% | widget over-capture; 1 empty widget boxes |
| JPFUN02 | JPFUN02_0_0.html | 6.0% | 47 content blocks missing; widget over-capture |
| SSFUN07 | SSFUN07_2_0.html | 6.1% | widget over-capture |
| CEDT104 | CEDT104_0_0.html | 7.0% | widget over-capture; 2 empty widget boxes |
| CEDT301 | CEDT301_6_0.html | 7.4% | widget over-capture |
| MXFUN03 | MXFUN03_0_0.html | 8.1% | widget over-capture; 1 empty widget boxes |
| CEDR401 | CEDR401_1_0.html | 8.3% | widget over-capture; 8 empty widget boxes |
| XOTPB08 | XOTPB08_2_0.html | 8.5% | widget over-capture |
| ANZHFUN05 | ANZHFUN05_0_0.html | 9.1% | widget over-capture |
| TWHK901 | TWHK901_0_0.html | 9.3% | 24 content blocks missing; widget over-capture |
| TRR304 | TRR304_3_0.html | 9.5% | widget over-capture |
| CEDR101 | CEDR101_1_0.html | 9.8% | widget over-capture |
| ARFUN04 | ARFUN04_0_0.html | 9.8% | widget over-capture; 1 empty widget boxes |
| TWHA905 | TWHA905_0_0.html | 10.5% | widget over-capture |
| EXIP901 | EXIP901_4_0.html | 10.6% | widget over-capture |
| XDLS911 | XDLS911_1_0.html | 10.8% | widget over-capture |
| TWHK902 | TWHK902_0_0.html | 11.0% | 19 content blocks missing; widget over-capture; 1 empty widget boxes |
| EXPFUN05 | EXPFUN05_0_0.html | 11.1% | widget over-capture |

## 6. How to use this

1. Take the top row of the queue whose fix is a **blocker** (section 4), not a shape.
2. Measure that blocker properly before writing code — the standing rule.
3. Scope the rebuild with `regen_scope.cjs --feature <name> --plan`.
4. Re-run this dashboard after the round; coverage should move, not just the gates.

**Re-run:** `python3 CONVERTER_V2/outputs/_coverage_dashboard.py --refresh`
**Rebuild the census first** (after any builder change) with `_measure_r271_variations.cjs --shard K 16` ×16, else coverage under-reports.
