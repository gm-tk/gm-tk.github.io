## 2026-09-19 (round 395, build 260619.66) — THE FLIP-CARD COLUMN WIDTH FOLLOWS THE CARD COUNT: a 2-card or 4-card flipCard group renders its cards in `col-md-6 col-12 paddingLR` (`interactive.flipCard.card_col_by_count`, `InteractiveBuilder.#flipCardsByCount`, env `FLIPCOL_OFF`); the autonomous loop's session 26 Round 9 — the r394 column census followed through; SCOPED regeneration of the 37 affected modules (scoped ship #7 since the r388 full — the NEXT ship is the FULL backstop); skeleton 53.674 → 53.684 % (+0.010pp; 16 movers 15 up / 1 down), ≥75 194 → 195, ≥50 1163 / ≥90 18 EXACT, RAW 37.779 → 37.784 %; every other gate EXACT, every verifier RESULT identical

### 1. WHAT CHANGED

The flipCard `card` template hard-codes `col-md-4 col-12 paddingLR` for every card. The paired widget census (`outputs/_s26_r395_flipcols.py` → `.out`, every `flipCardsContainer`'s card count and column class, gold vs Claude, per subject): **4 cards — gold `col-md-6` 48 (39 pages) + `col-md-6 col-sm-6` 9 + `col-md-3` 16 + `col-md-4` 2 → `col-md-6` 0.76; Claude `col-md-4` 57 on 49 pages / 43 modules. 2 cards — gold `col-md-6` 39 (28 pages) + `col-6 col-md-6` 11 + `col-md-4` 8 → 0.86; Claude `col-md-4` 19 on 18 pages / 14 modules.** 3 cards `col-md-4` 100 and 5–12 cards `col-md-4` — Claude already matches. Per subject the 4-card form is a TIE in English (col-md-6 10 / col-md-3 9) and col-md-3-led in ConnectED (4 / 3) and NCEA1 (2 / 1); the 2-card form is col-md-4 in NCEA1 (2 / 2) and a tie in the subject-less TEDC modules (col-md-6 4 / col-md-4 3) — those keep the default. A 1-card group is `col-md-12` in the gold (17 of 27 = 0.63) but Claude's 1-card groups sit on 8 pages — under the floor, recorded, not taken.

**The fix (DATA OVER CODE):** `interactive.flipCard.card_col_by_count {enabled, env: "FLIPCOL_OFF", default: "col-md-4 col-12 paddingLR", by_count: {"2": "col-md-6 col-12 paddingLR", "4": "col-md-6 col-12 paddingLR"}, exclude_subjects_by_count: {"2": ["NCEA1", ""], "4": ["1-10 English", "ConnectED", "NCEA1"]}}` — `#flipCardsByCount(tpl, cards, run)` swaps the default column class for the by-count class in each finished card (the first occurrence = the wrapper column) at the four `tpl.card` join sites (the table builder, the r2xx composer, the alternating and transposed readers); the module's subject comes from `module_meta` (the r389 / r391 precedent). The image-front `card_image_front` family (`col-md-6 col-sm-6`, the gold's own form for it) is untouched. OFF = the r394 output (the probe 2109 / 2109).

### 2. HOW IT WAS FOUND

- The r394 column census (`_s26_r394_colrow.out`) listed the gold's flip-card columns directly in the text column as `col-md-6 paddingLR` 72 (59 pages) against `col-md-4` 45 — Claude's 176 all `col-md-4` → the by-count census.
- KB-first: 02C names `flipCardsContainer` on the wrapper row and nothing on the column width; 07C's `col-md-6 col-12 paddingLR` is the word / image grid → §1b level 3 / 4 (the gold's own consensus). A wrapper class token, structure-only → derivable (the card count is the writer's own table).
- The first cut (no exclusions) scored 20 up / 4 down with the dips all English 4-card pages (ENGS202_4_0 −1.5, ENGC301_2_0 −0.9, ENGS202_2_0 −0.8) → the per-subject census in full → the exclusions; the second cut 15 up / 1 down.

### 3. THE PROBE + THE SCOPED REGENERATION + THE GATES

- Probe over all 416 (`_s26_r395_probe.cjs`): **OFF 2109 / 2109; ON 39 pages / 37 modules**. Scored with the gate's own `match()` before regenerating: 38 paired, **15 up / 1 down / 22 same, pp-sum +19.4** (22 pages unmoved: the card column sits inside the WIDGET zone on those pages, invisible to the scaffold; TEFUN08_0_0 −0.2 the one dip).
- 37 modules in 4 batches (all rc 0); `fresh --affected` **0 truly stale**; the manifest diff = **39 pages / 37 modules, 0 added / removed** (= the probe's ON set); **probe ON == disk 202 / 202**.
- **PRIMARY skeleton (`_s26_r395_sk_final.json`, delta `_s26_r395_sk_delta.log`): SCAFFOLD 53.6736 → 53.6835 % (+0.010pp) / ≥50 1163 / ≥75 194 → 195 (OSOH201_2_0 crosses up) / ≥90 18 / median 54.2 → 54.3 / RAW 37.779 → 37.784 % @ 1956, skipped 0; 16 movers (15 up / 1 down, pp-sum +19.4), 0 outside the affected set**. Best: ENGJ402_7_0 +5.4, ENFUN01_0_0 +2.5, OSSC501_2_0 +1.9. compare_structure **11723 / 172 / 626** EXACT; body_compare **42 / 4 / 173 / 218** EXACT; clean **2079 / 2102**, leak **26 / 23** EXACT; every verifier RESULT identical to r394 (the flipCard verifier included); 15 selftests + the feature-index selftest GREEN; fast-loop / manifest / feature index refreshed.
- The DIFF MINER re-mined (`_diff_miner_s26_r395.log`): **173 CANDIDATE rows (174 → 173: #3649 `body EXTRA div.flipCardsContainer.row › div.col-12.col-md-4.paddingLR` GONE; nothing new).**

### 4. RECORDED

- A plateau-magnitude round (+0.010pp) but ≥75 +1 moved — §4's window stays at 0 of 3 (both conditions are needed).
- The ledger stands at scoped #7 since the r388 full: **the next ship must be a FULL regeneration.**
- 1-card groups → `col-md-12` (gold 0.63 on 16 pages; Claude 8 pages) is under the floor — take it when a full regeneration makes the floor moot, or leave it.
