#!/usr/bin/env python3
"""ROUND 526 finalise (session 51 Round 7 — the BLL introduction heading's own full-width row). WSL. argv: MEAN RAW."""
import sys
import _s51_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 526, build 260620.86) — THE BLL INTRODUCTION HEADING'S OWN FULL-WIDTH ROW: on a Blended Literacy page the writer's `[Introduction]` heading stands alone in a `div.row > div.col-12` row (the gold's form on 65 of 79 overviews), not at the head of the `col-md-8` content column; per series (BLL17 / BLL24 / BLL26 keep theirs); 66 modules, skeleton +0.0550pp

### 1. WHAT CHANGED

**The class** (the loss ledger's largest family, BLL — 298 pages, 10.2 % of the gap; the scoped miner over BLL `_s51_bll_miner.md`, row #1374 `div.row` › gold `div.col-12` vs Claude `div.col-12.col-md-8`, 107 pages / 78 modules): the writer's mid-document `[Introduction]` (a title-bar alias) renders as `<h3>Introduction</h3>` at the head of the ordinary content column; the Blended Literacy gold puts that heading ALONE in a full-width row (`_s51_r7_intro.py`: `row > col-12 > h3` alone on 65 of 79 overviews, 0.82). By series (`_s51_r7_intro2.py`): the full-width row in BLL11 7/8, BLL12 7/7, BLL13 8/8, BLL14 4/4, BLL15 7/7, BLL16 6/6, BLL21 7/7, BLL22 7/7, BLL23 5/7, BLL25 7/7; the `col-md-8` column in BLL17 (5 of 7) and BLL26 (4 of 5); BLL24 a 3 : 3 tie.

**The fix** (`ContentConverter.#introHeadingFullRow`, a page post-pass just inside `#pageNumberNormalise`; data `body_region.intro_heading_full_row` {{subjects ["1-10 Blended Literacy"], exclude_series [BLL17, BLL24, BLL26], heading_pattern, column_class "col-12"}}, env **`INTROROW_OFF`**): in a module whose subject is listed and whose series is not excluded, a row whose column OPENS with `<h3>Introduction</h3>` is split — the heading alone in `row > col-12`, the rest in the row's own column. A per-group rule (LOOP §1d exception 2) keyed by the family's own gold. The first build (every series) scored +0.0438pp with BLL261–264 down 4pp each; the series scope removed those.

### 2. PROOF

- In-memory probe over all 545 modules: `INTROROW_OFF=1` → 6,432 / 6,432 pages identical; ON → **66 modules** (BLL only); 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 526` PASS: 0 stale, containment 66 ⊆ 66, a re-planned 12-module spot-check byte-identical.
- The skeleton gate's own `match()` (`_s51_prescore.py`): **+0.0549pp, 58 up / 3 down** (BLL253_0_0 +7.2, …; the three dips BLL237 / 236 / 142 −1.2 to −1.7, each the short overview's alignment).

### 3. PROTECTED GATES

Skeleton **56.0460 → {MEAN} % @ 2486 (+0.0550pp)**, ≥50 1627 held, ≥75 290 → 292, ≥90 26; RAW 39.798 → {RAW} %; compare_structure exact 16830 / EXTRA 204 / missing 879 held; body_compare ANY 234 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r526_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 526`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.0550pp).

**Ledger:** scoped #5 since the s50-r14 FULL (r520) · data `body_region.intro_heading_full_row` · env `INTROROW_OFF` · code `ContentConverter.#introHeadingFullRow` · session 51 Round 7.
"""
F.finalise(
    N=526, old_build="260620.85", new_build="260620.86", entry=entry,
    config_comment="THE BLL INTRODUCTION HEADING'S OWN FULL-WIDTH ROW (session 51 Round 7; per series). Env INTROROW_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 526 BASELINE (the BLL introduction heading's own full-width "
        f"row, `INTROROW_OFF`; SCOPED, scoped #5 since the s50-r14 FULL): SCAFFOLD mean {MEAN}% / >=50% 1627 / >=75% 292 / >=90% 26 / "
        f"RAW {RAW}% @ 2486 pairs (+0.0550pp); cs exact 16830; body ANY 234.**",
    og11="| `INTROROW_OFF` | 526 | **THE BLL INTRODUCTION HEADING'S OWN FULL-WIDTH ROW** (session 51 Round 7). Reverts "
         "`body_region.intro_heading_full_row`: the `[Introduction]` heading opens the ordinary `col-md-8 col-12` content column again "
         "(the r525 output exactly). |",
    og14=f"- **Build:** `260620.86` (round 526 — **the BLL introduction heading's own full-width row**; `INTROROW_OFF`; scoped #5 since "
         f"the s50-r14 FULL; 66 modules; skeleton {MEAN} % (+0.0550pp), RAW {RAW} %).",
    gb_note=f"Round 526 (session 51 Round 7, 2026-09-26) — THE BLL INTRODUCTION HEADING'S OWN FULL-WIDTH ROW (INTROROW_OFF): 66 BLL "
            f"modules; skeleton 56.0460 -> {MEAN} (+0.0550pp), >=75 292; every other gate held; scoped #5.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 51 Round 7 — r526 (the BLL introduction heading's own full-width row) "
             "SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r526** (260620.86); **LAST FULL = r520 (the "
             "session-50 Round 14 backstop)**; ledger **scoped #5** (3 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at "
             "every PICK): `outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, "
             "10 pages / 9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) "
             "/ `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] "
             "<widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix) / `_r524_declined.patch` (the callout + "
             "heading co-tag, 17 modules — rides only once an alert's run gathers the list after its title). Checked at r526: none rides "
             "(no patch's pages lie in the 66 BLL modules).",
    last_shipped=f"- LAST SHIPPED: **r526** (build 260620.86, 26 Sept {T}, session 51 Round 7 — THE BLL INTRODUCTION HEADING'S OWN "
                 "FULL-WIDTH ROW, `INTROROW_OFF`; SCOPED, **scoped #5 since the s50-r14 FULL**; 66 modules; skeleton 56.0460 → "
                 f"{MEAN} % (+0.0550pp), ≥75 292, RAW {RAW} %; every other gate held).",
    before_them_add="the bold activity id after a widget tag",
    plateau="- Plateau window (§4): **0 of 3** — r526 +0.0550pp (a real gain: reset); s51-r6 a PICK pass (neither); ",
    standing="- Standing facts: AppVersion **260620.86** (r526 the BLL introduction heading's own full-width row — session 51 Round 7, "
             "26 Sept); before it 260620.85 (",
    roundlog=f"- s51-r7 (engine r526, build 260620.86, 26 Sept 13:08 → {T}) · a PICK pass (activity-sidebar followers 18 : 12; XGF9004's "
             "18-page WT; the BLL scoped miner) then THE BLL INTRODUCTION HEADING'S OWN FULL-WIDTH ROW (gold 65 / 79; per series, "
             "BLL17 / 24 / 26 excluded) · SHIPPED scoped #5 · 66 modules · skeleton **+0.0550pp**, ≥75 +2, every other gate held · plateau "
             "reset (0 of 3).",
    archive_extra="- **What shipped (r526, 260620.86):** `ContentConverter.#introHeadingFullRow`; data `body_region.intro_heading_full_row`. "
                  "Probe OFF 6,432 / 6,432 identical; ON 66 modules; +0.0550pp; every other gate held.",
)
