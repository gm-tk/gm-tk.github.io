#!/usr/bin/env python3
"""ROUND 505 finalise (session 49 Round 5 — D15-18 part 1, the RHS box is always the side column, RHSALWAYS_OFF). WSL.
argv[1] = skeleton mean (4 dp), argv[2] = RAW (3 dp)."""
import sys
import _s49_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-25 (round 505, build 260620.68) — D15-18 PART 1: A RIGHT-HAND BOX IS ALWAYS THE SIDE COLUMN in Standard and Fundamentals modules — the `right hand side` spellings count, and a box with no content row before it pairs with the row that follows (22 pages / 17 modules; the RHS family's Claude = gold 70 → 78 tags, 0 lost)

### 1. WHAT CHANGED

**The decision** (Chris, 25 Sept 2026, D15-18 — "18. Right-hand alert box: Option B (An RHS tag always becomes the right-hand side box) — as recommended"): every RHS-alert spelling in Standard and Fundamentals modules (not Inquiry — its golds 3 / 10) becomes the right-hand side column, the box style still chosen by position (r333: `alertActivity` after an activity, `alert top` after content); it overrides the claude-audit brief's per-shape 0.60 rule and each module's own gold where it differs; the lost boxes are fixed too (part 2, next).

**The instrument, repaired first** (`outputs/_rhsalert_measure.py`, the D15 report's correction 4; the pre-copy `_rhsalert_measure.pre-r505.py`): a plain `col-4` / `col-3` side column now counts (r333 counted both), and a table-marker line (`┌─── TABLE ───`) is never read as the tag's text (the six TEDC402 rows). **176 tags / 73 modules; 139 found on the human's page: side column 92 = 0.66 (Standard 68 / 97 = 0.70, Fundamentals 21 / 32 = 0.66, Inquiry 3 / 10)**; PageForge side 66, = gold on 70. The non-Inquiry misses (`_r505_rhs_split.py`, 66): 34 built FULL-WIDTH — the `right hand side` spellings r333's `rhs` / `rhc` words never matched, and boxes with no content row closed just before them (the page-top Ākonga notes, MXFL, HIS) — and 32 rendered as body (XGF9001's co-tagged `[Alert RHS] [H3]` ×9, TEDC402's table cells ×7, `…of activity box`, SCBI301 — part 2).

**The fix** (`ContentConverter` — the r333 branch; data `callouts.positional_side_alert.always_side`; env `RHSALWAYS_OFF`; only where `Module_Structure_Index` says Standard / Fundamentals): (1) `extra_keywords` `right` / `right-hand` join r333's words (`[Alert box right hand side]`, `[important note: in right]`, `[alert note: right of …]`); (2) `forward_pair` — a box with no content row closed just before it is HELD (the r123 `pendingSideAlert` path the alert-table form already uses) and attached as the right sibling of the row still open, else of the next content row at its first ordinary break (never the alert-table hold that gathers headings until media — tried first: XGF9006's box travelled past a heading).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **22 pages / 17 modules** (ANZHFUN05 BLL242 BLL244 DTC1004 EXPFUN07 HIS1004 MXFL104 MXFL301 TEDC402 TEFUN01 03 04 06 07 08 XGF9006 XLP03). Regenerated = ON byte-for-byte (73 / 73); `scoped_ship.sh` PASS (0 stale, containment 17 ⊆ 17, the 12-module spot-check byte-identical).
- **The family's own measure on the ON pages** (`_r505_measure_on.py`, `_r505_tagdelta.log`): Claude = gold **70 → 78 / 139**; 13 tags moved — **8 GAIN** (ANZHFUN05 / TEFUN01 / TEFUN03 / EXPFUN07 Ākonga notes, BLL242 / BLL244 `right hand side`, MXFL104, MXFL301), **0 LOSE**, 5 moved on unfound or NAMED golds (TEFUN04 / 06 / 08 absent, TEFUN07 body, HIS1004_10 side-alertActivity → side-alert-top). Out-of-family right-hand asks now paired: DTC1004 `[important note: in right]`, XLP03 `[alert note: right of]`, XGF9006 ×6 `[Alert.RHS]`.
- Not reached (recorded): a box that SPANS to an explicit `[End alert]` (BLL251 / 254–257 / 272 `[Alert box right hand side of page]` … `[End of alert box]` — r333 keeps spans on the ordinary path), the WJFUN tile pages (their tile builder), the lost boxes (part 2).

### 3. PROTECTED GATES

- Skeleton **55.5331 → {MEAN} % @ 2486**, RAW 39.465 → {RAW} %; ≥50 1599, ≥75 276 HELD; **22 movers, 15 up / 7 down** (pp-sum +17.6): XGF9006_5_0 +6.7, BLL244_1_0 +5.9, MXFL301_7_0 +3.4, DTC1004_6_0 +2.7, BLL242_1_1 +2.7 …; **the 7 down NAMED** — XGF9006_2_0 36.0 → 31.7 / _3_0 34.1 → 30.2 / _4_0 25.6 → 24.7 (two RHS boxes on one page now each pair with their own row — the second forward), EXPFUN07_0_0 32.8 → 29.8, TEFUN01 / 03 / 07 −0.1 to −0.5 (the Ākonga box moves to the side column the gold uses; the gold's column is `col-md-3 offset-md-0` inside the Fundamentals introduction). **cs exact 16762 → 16766 (+4), EXTRA 200 → 199 (−1)**; body / clean / leak EXACT; every verifier ✓, every COUNT held (`_r505_gates.log`). Aggregates written by `scoped_ship.sh … --commit --round 505`; `--gate-baseline-check` PASS. Plateau: +0.0070pp (< 0.02) but cs exact +4 / EXTRA −1 — neither.

**Named overrides:** the RHS side column over the gold's full-width / paragraph forms (TEFUN07 and the Standard ones as they are reached) — by Chris's D15-18.

**Ledger:** **scoped #8 since the r498 FULL — the FULL backstop is DUE** (the next round) · data `positional_side_alert.always_side` · env `RHSALWAYS_OFF` · code `ContentConverter` (the r333 branch) · tools `_rhsalert_measure.py` (repaired), `_r505_rhs_split.py`, `_r505_measure_on.py`, `_r505_tagdelta.py`, `_r505_finalise.py` · the r469 ride-along patch checked: its pages (ANZH301 / 302, ENGC403) are outside this set · session 49 Round 5.
"""
F.finalise(
    N=505, old_build="260620.67", new_build="260620.68", entry=entry,
    config_comment="D15-18 PART 1 — THE RHS BOX IS ALWAYS THE SIDE COLUMN (session 49 Round 5): right-hand spellings count, and a box "
                   "with no preceding row pairs with the following one (Standard / Fundamentals). Env RHSALWAYS_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 505 BASELINE (D15-18 part 1 the RHS side column, "
        f"`RHSALWAYS_OFF`; SCOPED, scoped #8 since the r498 FULL — the FULL backstop due): SCAFFOLD mean {MEAN}% / >=50% 1599 / >=75% 276 / "
        f">=90% 26 / RAW {RAW}% @ 2486 pairs — 15 up / 7 down NAMED; cs exact 16766 (+4), EXTRA 199 (−1).**",
    og11="| `RHSALWAYS_OFF` | 505 | **D15-18 PART 1 — THE RHS BOX IS ALWAYS THE SIDE COLUMN** (session 49 Round 5). Reverts "
         "`callouts.positional_side_alert.always_side`: the `right` / `right-hand` spellings stop counting and a box with no preceding "
         "content row renders full-width again (r333 alone); byte-identical to r504. |",
    og14=f"- **Build:** `260620.68` (round 505 — **D15-18 part 1, the RHS side column**; `RHSALWAYS_OFF`; scoped #8 since the r498 FULL; "
         f"22 pages / 17 modules; skeleton {MEAN} % @ 2486; the family's Claude = gold 70 → 78).",
    gb_note=f"Round 505 (session 49 Round 5, 2026-09-25) — D15-18 PART 1 THE RHS BOX IS ALWAYS THE SIDE COLUMN (RHSALWAYS_OFF): 22 pages "
            f"/ 17 modules; SCAFFOLD 55.5331 -> {MEAN} @ 2486, 15 up / 7 down NAMED; cs exact +4, EXTRA -1; the RHS family's Claude = gold "
            f"70 -> 78 / 139; scoped #8 (FULL due).",
    no_round=f"- **No round in flight** (25 Sept 2026 {T}, session 49 Round 5 — r505 (D15-18 part 1, the RHS side column) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r505** (260620.68); **LAST FULL = r498**; ledger **scoped #8 — "
             "the FULL backstop is DUE (the next round)**. Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403; checked at r505, outside its set) / "
             "`_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules) / `_r463_declined.patch` (the "
             "WJFUN tile's \"Year N\" lead, 1 page).",
    last_shipped=f"- LAST SHIPPED: **r505** (build 260620.68, 25 Sept {T}, session 49 Round 5 — D15-18 PART 1, THE RHS BOX IS ALWAYS THE "
                 "SIDE COLUMN, `RHSALWAYS_OFF`; SCOPED, **scoped #8 since the r498 FULL — FULL due**; 22 pages / 17 modules; the RHS "
                 f"family's Claude = gold 70 → 78 / 139, 0 lost; **skeleton 55.5331 → {MEAN} % @ 2486**, 15 up / 7 down NAMED; cs exact "
                 "+4, EXTRA −1; body / clean / leak EXACT).",
    before_them_add="the BLL2xx Knowledge / Practices tabs",
    plateau="- Plateau window (§4): **0 of 3** — r505 +0.0070pp but cs exact +4 / EXTRA −1 (neither); ",
    standing="- Standing facts: AppVersion **260620.68** (r505 D15-18 part 1 the RHS side column — session 49 Round 5, 25 Sept); before "
             "it 260620.67 (",
    roundlog=f"- s49-r5 (engine r505, build 260620.68, 25 Sept 19:52 → {T}) · D15-18 PART 1 THE RHS BOX IS ALWAYS THE SIDE COLUMN (the "
             "instrument repaired first: side 0.66 / Standard 0.70; `right` spellings + forward pairing) · SHIPPED scoped #8 · 22 pages / "
             "17 modules, family = gold 70 → 78 · skeleton +0.0070pp, 15 up / 7 down NAMED, cs exact +4 · plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r505, 260620.68):** `positional_side_alert.always_side` (env `RHSALWAYS_OFF`), the r333 branch in "
                  "`ContentConverter`. Probe OFF 0; ON 22 pages / 17 modules; scoped_ship PASS; the family 70 → 78 (8 gain / 0 lose).",
)
