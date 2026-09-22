# Loop intake — the 38 pre-intake never-converted modules (22 September 2026)

**Written 22 Sept 2026 by the autonomous loop itself (session 33 Round 3 = LOOP §1f Round 0d, the
first intake the loop has run unattended under Chris's D12-3).** The trigger was not new files
arriving: the 22 Sept `/loop-review`'s adversarial check found that the gold-only gap was 57
modules, not the 19 the loop recorded — 38 gold modules held a Writers Template and its
`_parsed.txt` but had never once been converted (never in `compare_set.txt`; a full regeneration
enumerates Claude dirs, so nothing ever reached them). Handover into `LOOP__Autonomous_Rounds.md`
/ `LOOP_STATE.md`; artefacts mirrored in `pageforge-site/converter-v2/loop/`.

---

## 1. The one-minute summary

- **All 38 convert — 0 refusals, 0 ghost dirs.** 161 Claude pages against 125 gold pages; 114
  skeleton pairs (CEDW303 is a `compare_exclusions.txt` revision brief — converted, not scored).
- **Corpus 2583 → 2744 pages / 507 → 545 dirs / 2377 → 2491 pairs.** The gold-only gap is now
  exactly the 7 modules with no Writers Template (GER1003–1007, SAM1005, SAM1006).
- **Every protected gate held on the pre-existing population, page for page** (0 movers on
  2377 pairs; every decomposable gate EXACT = r422e). The new batch enters at **51.42 % mean
  scaffold** (67 of 114 pages ≥ 50, 16 ≥ 75, 3 ≥ 90); the whole population re-based to
  **54.1172 % @ 2491**.
- **The finding that ranks the queue:** eight single-page Inquiry golds that Claude splits into
  lesson pages (BLL250 8 pages / BLL260 13 / BLL270 5 / CEDK401 12 / CEDO402 6 / TWHT903 5 /
  CEDR101 2 / CEDR401 2 against the gold's ONE) and one the other way (CEDR203: 1 Claude page vs
  11 gold). Their `page_model` registry rows were never mined because they were never members
  of a Style-Anchor level. That is the next round (a registry round, §1f Phase 4 — the WJFUN /
  CHFUN precedent).
- The ceiling re-measured on 2491 pairs: **91.2 %** (was 90.9) → 54.117 % = **59.4 % of
  achievable**. `DIFF_QUEUE.md` re-mined: **190 CANDIDATE** rows (184 before); the six new
  rows are all this batch's single-page family. `COVERAGE_DASHBOARD.md` rebuilt (coverage
  50.7 %). The ship ledger: FULL at `intake-2026-09-22`, counter 0.

## 2. The numbers that changed (already corrected in LOOP_STATE.md, the loop file §0, the verify script)

| figure | before (r422e) | now |
|---|---:|---:|
| Claude module dirs | 507 | **545** |
| Claude pages | 2,583 | **2,744** |
| skeleton pairs | 2,377 | **2,491** |
| gold dirs / docx | 552 / 762 | 552 / 762 (unchanged) |
| skeleton SCAFFOLD mean / ≥50 / ≥75 / ≥90 | 54.2466 / 1464 / 238 / 20 | **54.1172 / 1531 / 254 / 23** |
| compare_structure exact / EXTRA / missing / row-wrap | 14318 / 186 / 689 / 23 | **15131 / 194 / 773 / 23** |
| body_compare over-capture / runaway / EMPTY / ANY | 55 / 5 / 193 / 251 | **57 / 5 / 206 / 265** |
| structurally clean / leak | 2532 / 2576 = 98.29 %; 73 / 44 | **2690 / 2736 = 98.32 %; 75 / 46** |
| ceiling (scaffold) | 90.9 % | **91.2 %** |
| ship ledger | scoped #1 since r425 | **FULL at intake-2026-09-22, counter 0** |

Every "worse" absolute is the new batch's own contribution — `_intake_split.py` (new, kept for
the next intake) shows the 2377 pre-existing pairs EXACT on every row. Read every later delta
on the 2491-pair population (LOOP §1e).

## 3. What the loop must do at its next start

1. The miner check (§1d) is satisfied: `DIFF_QUEUE.md` was produced at 11:51 on 22 Sept on this
   corpus (2491 pairs / 533 modules). Re-verify with the newer-than check as usual.
2. **Pre-intake exhaustion verdicts are VOID** (§4) — the last one (session 30, 21 Sept) was on
   a 495-module corpus; this corpus has 545.
3. Take the round order in §7 below: the single-page Inquiry page-model registry rows first.

## 4. The influx of discrepancies, measured (the scoped miner over the 38 — `outputs/_diff_miner_scoped.{md,json}`, 115 pairs, 1380 classes, 11 CANDIDATE)

### 4.1 One family dominates: the single-page Inquiry page model
- **F15 MISSING `nav:crumbs`** — 14 modules / 14 pages (BLL250 / 260 / 270, CEDK401, CEDO201,
  CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDW303, TWHK902, TWHR905, TWHT903); gold 1.00 on
  Inquiry/lesson and Inquiry/overview. **F16 MISSING the inquiry footer
  `home-nav,prev-lesson,next-lesson`** — 10 modules. Full-miner rows **#438 crumbs MISSING
  `div.crumbs > div`** (23 pages / 20 modules), **#496 footer `li>a#prev-lesson`** (15 / 15),
  **#4098 body MISSING `div#body > div.inquiryPanel`** (38 pages / 35 modules — this batch pushed
  it over the floor). The gold builds ONE page with an in-page crumb nav and inquiry panels; Claude
  either splits the module into lesson pages (the eight over-split modules) or builds one page
  without the inquiry shell (CEDO201, CEDT102, TWHK902, TWHR905 …). The gated siblings
  (BLL210 / 220 / 230 = `page_model_exceptions`; CEDK101, CEDO102, CEDT101, TWHK901) build the one
  page. **A registry row, not a rule** — `Style_Anchor_Registry` level rows / `page_model`
  exceptions for these codes, measured per module in memory before any regeneration (the r408
  "faithful row" that scored a family DOWN is the caution).
- **#63 / #73 / #85 module-menu EXTRA on the BLL single-page modules** (WIDGET / `h5` / `p` items
  Claude adds where the gold has none — 10–17 modules): the same modules; expect them to collapse
  with the page model.

### 4.2 The other candidate classes worth the queue's attention
- **F1 / F2 — the lesson chip: Claude `decimal-number` ("1.0") where the gold has
  `lesson-number` ("1")** — 14 modules / 41 pages (BLL255 … BLL276, SSCI104, SSEA203, SSOG105);
  Standard/lesson gold 0.64. The BLL2 Standard family's chip form; check the family's gated
  siblings (BLL240 …) before calling it a family convention — the miner's consensus on the whole
  corpus is what decides (the full-miner chrome facts).
- **#4177 body EXTRA `div.col-12.col-md-6 > img.img-fluid`** — 23 pages / 19 Standard modules,
  consensus 0.99: Claude puts an image in a half-width column the gold does not have. Read three
  modules (WT → gold → Claude) before deciding; likely the BLL image-pair table shape.
- **CEDR203 — 1 Claude page vs 11 gold pages**: the reverse case; a per-module read (its WT may
  carry `[Tab N]` crumbs the splitter reads as one page).

### 4.3 What the new modules do not change
- No new widget authoring shape: the 38 carry hand-off boxes of the known types (carousel,
  dragAndDrop, flipCard, modal …); no verifier module set needs extending.
- No new subject / prefix: every code was already in `Module_Structure_Index.module_meta` and
  `Subject_Prefix_Map.json`.
- The KB queue (§1c) is unchanged.

## 5. The modules that do not convert
None of the 38. The corpus-wide no-build list is now: **7 with no Writers Template**
(GER1003–1007, SAM1005, SAM1006 — needs Chris #10) and the three Claude dirs that hold only a
`_run.json` (TRR104 / TRR105 no Writers Template; TRR115 the pre-existing refusal).

## 6. Traps this round hit, recorded so the next one does not
1. `scoped_ship.sh` step 6 records a scoped ship on EVERY run (no-commit or failed included) —
   r425 read as scoped #8 when it was #7. Run it once per round; commit with
   `_fastloop_diff.py --commit` directly.
2. `_scoped_spotcheck.py plan` can draw a `compare_exclusions.txt` module (CEDR302); an explicit
   code list then scores its page and a `--commit` would patch it into the baseline. Drop such
   codes from the re-score list.
3. `_gatecheck.py` asserts 0-stale by mtime — a full-regeneration tool; for a scoped ship the
   content manifest is the freshness proof and `_fastloop_diff.py` the verdict.
4. `_coverage_dashboard.py --refresh` compares the census against `data/*.json` mtimes INCLUDING
   `Module_Feature_Index.json`: rebuild the feature index BEFORE the variation census, or use
   `--allow-stale` when both are on the same corpus (as here).
5. A concurrent `/loop-review` session committed to `pageforge-site` while Round 1 ran (c942de2,
   loop files only). No harm this time; a loop session should check `list_sessions` /
   `git log` before its own commit when the tree has moved under it.

## 7. Recommended round order (Phase 7 — re-ranked, not appended)

1. **The single-page Inquiry page-model registry rows** (§4.1) — 8 over-split modules at
   3–10 % (+ CEDR203 the reverse), the crumbs / inquiryPanel / footer rows #438 / #496 / #4098
   and the module-menu rows #63 / #73 / #85 collapse with it. Data only (`Style_Anchor_Registry`
   level membership / `page_model_exceptions`), measured per module in memory first, its own
   ledgered round with its own named delta (§1f Phase 4 rule). **Start here.**
2. **The lesson chip `lesson-number` vs `decimal-number`** (F1 / F2, 14 modules) — a family
   convention check against the whole corpus's chrome facts.
3. **#4177 the `col-md-6 > img` EXTRA** (19 Standard modules) — triangulate three modules.
4. Then the standing queue in `DIFF_QUEUE.md` (190 CANDIDATE, chrome first), the KB queue, the
   "Follow-up candidates" and the lanes §4 names.

## 8. Where everything is
`CONVERTER_V2/outputs/`: `_intake_2026-09-22_delta.txt` (the 38: template, sources, index),
`_intake_2026-09-22_codes.txt`, `_intake_2026-09-22_convert.sh` + `_batch_0{0..3}.log`,
`_intake_2026-09-22_results.txt` (pages / refusals per module), `_intake_2026-09-22_fullship_par.sh`
+ `_fullship_regen.log`, `_intake_2026-09-22_gates.sh` + `_gates.log` / `_sk_final.json` (=
`_r0d-20260922_sk_final.json`) / `_skdelta.log` / `_gatecheck*.log` / `_fastloop_snapshot.log` /
`_manifest_snapshot.log` / `_selftests.log`, **`_intake_split.py`** + `_intake_2026-09-22_split.log`,
`_intake_2026-09-22_instruments.sh` + `_ceiling_intake_2026-09-22.{json,md,log}` /
`_intake_2026-09-22_dashboard_run.sh` / `_diff_miner__intake_2026-09-22.log` /
`_diff_miner_scoped.{md,json}` / `_intake_2026-09-22_index.log`, `_intake_2026-09-22_finalise.py`,
`_intake_2026-09-22_checksums.sh`. Root: `DIFF_QUEUE.md`, `COVERAGE_DASHBOARD.md`,
`NEW_MODULES__Intake_2026-09-22.md`, this file. Mirror: `pageforge-site/converter-v2/loop/`.

## 9. Open items that need Chris
None new. The standing list is `LOOP_STATE.md` "Needs Chris — open decisions" (14 lines);
this round changes no page count on any of them.
