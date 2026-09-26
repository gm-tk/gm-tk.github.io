#!/usr/bin/env python3
"""ROUND 541 finalise (session 54 Round 1 — the alert whose title is a heading; s53's toggled-OFF round finished). WSL. argv: MEAN RAW."""
import sys
import _s54_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
RIDE = ("`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — "
        "CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion "
        "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05; its `bullet_bold_lead` data block is ALREADY in `Emit_Templates.json` "
        "(the r491 ride-along note) — verify and strike at the next accordion round) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
        "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect "
        "ownership fix) / `_r540_declined.patch` (the writer s side / beside word → the side column, 13 pages / 8 modules — BLL110 / 120 / 130 / 240, "
        "CEDO202, GENO901, HES1007, JPFUN01). `_r524_declined.patch` TAKEN by r541 (form B, below) — struck.")
entry = f"""## 2026-09-27 (round 541, build 260620.99) — THE ALERT WHOSE TITLE IS A HEADING: the writer's EMPTY `[Alert]` / `[Important]` / `[Alert Solid]` line followed by a `[Hn]` title now boxes the heading and its run (form A), and the `[Alert] [H3] …` co-tag opens the box (form B, the parked r524 patch); 38 modules / 117 pages, skeleton +0.0183pp, compare_structure exact +38 / missing −80

### 1. WHAT CHANGED

**The class** (`outputs/_s53_r8_alertrun.py`, session 53 Round 8): the writer types the callout tag ALONE (`[Alert]`, `[Summary alert box]`, `[Important]`, `[Alert Solid]`) and its title on the next line under a heading tag (`[H3] Keen to learn more?` — ANZH105, BLL252, DAN1003, HIS1005 …). The strict callout gathered only black text, so the box shipped EMPTY with the "Empty [alert]" red flag and the heading + its lines went free in the next row. The gold boxes the heading on 55 of 67 such sites, the first line after it on 40 / 42, the second on 13 / 21. Form B — the tag and the heading in ONE span (`[Alert] [H2] Key questions`, XGF9001–9006; `[Important] [H3] Step 1 …`, CEDT501) — gold 31 / 41 boxed, Claude 0.

**The fix.** Form A: `ContentConverter.#emptyCalloutHeadingBox` (run first inside `#summaryHeadingAlert`) — a content row holding ONLY that empty box, followed by a row whose column opens with an h2–h5, becomes one box (its own class) holding the heading and the column's following run; the rest of the column moves to a new row in a column of the same class (the r529 form); the empty row and its flag go. The run: every following paragraph / list / converter note (`run_rule "all"`), EXCEPT under a SUMMARY heading (Lesson summary / Summary / Key points / What have we learned — data `summary_run`), which takes r529's measured short run (one plain paragraph, any lists, one closing paragraph after a list). Data `body_region.empty_callout_heading_box` (`r529_handoff: false`), env **`CALLOUTHEADBOX_OFF`**. Form B rides as the parked r524 patch: `TagNormaliser` activity-heading co-tag, callout sub-rule — with no activity tag, a callout tag + heading tags only → the callout takes the primary slot (a right-hand span keeps the r505 / r506 side path); data `Tag_Lexicon activity_heading_cotag.callouts`, env **`CALLOUTHDCOTAG_OFF`**.

**The design, measured (session 54 Round 1; each an in-memory probe over all 545 modules + the gate's own `match()` + compare_structure's per-page split `outputs/_s54_csdelta.py`):** `run_rule all` + form B +0.0191pp but cs **EXTRA +25** (SSCI205 +17: the gold's summary box holds the recap and leaves the closing narrative free, 8 / 8 pages — the first ship FAILED on it, the 50 modules restored with both toggles set, `_content_manifest.py diff` 0 pages); the r529 hand-off (`r529_handoff: true`) +0.0148pp (HIS 15.17 → 9.74pp-sum, SSOG 2.31 → 0.24); a run stopping at a Red Flag note +0.0189pp; at most ONE plain paragraph +0.0121pp / EXTRA +7 (HIS1006_11_0 −12.6: the gold's `activity dropbox` holds the whole summary); **the shipped design, the summary heading's short run: +0.0182pp, cs exact +38 / EXTRA +8 / missing −80.**

### 2. PROOF

- OFF probe (`CALLOUTHEADBOX_OFF=1 CALLOUTHDCOTAG_OFF=1`) over all 545 modules: **6,432 / 6,432 identical**, 0 ASSEMBLE ERROR; ON → **117 pages / 38 modules**, 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 541 --commit --accept-named EXTRA` PASS: 0 stale, containment 38 ⊆ 38, the 12-module spot-check byte-identical.
- The skeleton gate's `match()`: **98 pages moved, 62 up / 36 down, +45.32pp-sum**. Largest ups: DAN1003 (6 pages +16.3), HIS1005 / 1008, SSEA203 (+9.5), ANZH105_8_0 +7.3, XGF9006_7_0 +6.8. Dips NAMED: HIS1006_11_0 −12.6 (the gold holds the summary in an `activity dropbox` box; the short summary run splits it), HIS1007_3_1 −8.2 (the writer asked for the right-hand column in a separate red line the converter drops; gold `col-md-4` side box), ENGC403_12_0 −6.0 (the gold builds the writer's second `[add important box]` as a tab widget — class C), TEDC402_8_0 −4.2 (TEDC keeps its Lesson Summary bare, r529's 0 / 6), HPRE301_6_0 −3.1, HES1006_5_0 −2.9 / SSFUN02_0_0 −2.4 (the gold leaves the writer's box open).
- **compare_structure EXTRA +8 NAMED** (`_r541s1_csdelta.log`): DAN1003 ×5 = `[Alert Solid]` → the KB class `alert solid`, the gold's side `alertActivity` box (a class the gate does not count as a callout — the gold DOES box it); HES1006_5_0 ×2 and MXFU302_1_0 ×1 = the gold leaves the writer's `[Alert]` content free.

### 3. PROTECTED GATES

Skeleton **56.3799 → {MEAN} % @ 2486 (+0.0183pp)**, ≥50 1645 → 1647, ≥75 305 → 309, ≥90 29; RAW 40.0275 → {RAW} %; compare_structure exact 17024 → 17062 / EXTRA 198 → 206 (NAMED) / missing 661 → 581; body_compare ANY 233 held; leak 52 / 42 EXACT; tags 9557 / 9557; every verifier ✓, every COUNT held (`_r541_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 541`; `--gate-baseline-check` PASS. Plateau: **not a plateau round** (+0.0183pp < 0.02, but ≥50 / ≥75 and compare_structure moved — §4: a plateau round moves no other protected gate) — the window resets.

**Ledger:** scoped #6 since the s52-r11 FULL · data `body_region.empty_callout_heading_box` + `Tag_Lexicon activity_heading_cotag.callouts` · env `CALLOUTHEADBOX_OFF` / `CALLOUTHDCOTAG_OFF` · code `ContentConverter.#emptyCalloutHeadingBox`, `TagNormaliser` co-tag callout sub-rule · built session 53 Round 8, finished session 54 Round 1.
"""
F.finalise(
    N=541, old_build="260620.98", new_build="260620.99", entry=entry,
    config_comment="THE ALERT WHOSE TITLE IS A HEADING (session 53 Round 8 / session 54 Round 1; the empty callout takes the following [Hn] and its run; the callout + heading co-tag). Env CALLOUTHEADBOX_OFF / CALLOUTHDCOTAG_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 541 BASELINE (the alert whose title is a heading, `CALLOUTHEADBOX_OFF` / `CALLOUTHDCOTAG_OFF`; SCOPED, scoped #6 "
        f"since the s52-r11 FULL): SCAFFOLD mean {MEAN}% / >=50% 1647 / >=75% 309 / >=90% 29 / RAW {RAW}% @ 2486 pairs (+0.0183pp); cs exact 17062 / "
        f"EXTRA 206 (+8 NAMED) / missing 581; body ANY 233.**",
    og11="| `CALLOUTHEADBOX_OFF` | 541 | **THE ALERT WHOSE TITLE IS A HEADING, form A** (session 54 Round 1). Reverts `body_region.empty_callout_heading_box`: the writer's empty "
         "`[Alert]` / `[Important]` ships empty with its red flag and the following heading goes free (the r539 output). `CALLOUTHDCOTAG_OFF` (same round, form B, the "
         "r524 patch): the `[Alert] [H3] …` co-tag's heading takes the primary slot again. |",
    og14=f"- **Build:** `260620.99` (round 541 — **the alert whose title is a heading**; `CALLOUTHEADBOX_OFF` / `CALLOUTHDCOTAG_OFF`; scoped #6 since the s52-r11 FULL; "
         f"38 modules / 117 pages; skeleton {MEAN} % (+0.0183pp), RAW {RAW} %; cs exact +38 / missing −80 / EXTRA +8 NAMED).",
    gb_note=f"Round 541 (session 54 Round 1, 2026-09-27) — THE ALERT WHOSE TITLE IS A HEADING (CALLOUTHEADBOX_OFF / CALLOUTHDCOTAG_OFF): 38 modules / 117 pages; skeleton "
            f"56.3799 -> {MEAN} (+0.0183pp); cs exact 17024 -> 17062, missing 661 -> 581, EXTRA 198 -> 206 NAMED (DAN1003 x5 the gold's alertActivity side box, "
            f"HES1006 x2 / MXFU302 x1 the gold leaves the box open); scoped #6 since the s52-r11 FULL.",
    no_round=f"- **No round in flight** (27 Sept 2026 {T} NZDT, session 54 Round 1 — r541 (the alert whose title is a heading) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r541** (260620.99); **LAST FULL = r534 (the session-52 Round 11 backstop)**; ledger **scoped #6** (2 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): " + RIDE,
    last_shipped=f"- LAST SHIPPED: **r541** (build 260620.99, 27 Sept {T} NZDT, session 54 Round 1 — THE ALERT WHOSE TITLE IS A HEADING, `CALLOUTHEADBOX_OFF` / "
                 "`CALLOUTHDCOTAG_OFF`; SCOPED, **scoped #6 since the s52-r11 FULL**; 38 modules / 117 pages; skeleton 56.3799 → "
                 f"{MEAN} % (+0.0183pp), ≥50 1647, ≥75 309, RAW {RAW} %; cs exact 17062 / EXTRA 206 (+8 NAMED) / missing 581; every other gate held).",
    before_them_add="r538 the family heading digit pin block 2",
    plateau="- Plateau window (§4): **0 of 3** — r541 +0.0183pp with ≥50 +2 / ≥75 +4 / cs exact +38 / missing −80 (not a plateau round under §4's text: reset); ",
    standing="- Standing facts: AppVersion **260620.99** (r541 the alert whose title is a heading — session 54 Round 1, 27 Sept); before it 260620.98 (",
    roundlog=f"- s54-r1 (engine r541, build 260620.99, 27 Sept 01:52 NZST → {T} NZDT) · FINISHED s53's toggled-OFF r541, THE ALERT WHOSE TITLE IS A HEADING (form A + "
             "the r524 co-tag, form B) · five designs probed; the first ship FAILED on cs EXTRA +25 (SSCI205's summary box) — restored; the summary heading's short run "
             "shipped · scoped #6 · 38 modules / 117 pages · skeleton **+0.0183pp**, ≥50 +2, ≥75 +4, cs exact +38 / missing −80 / EXTRA +8 NAMED · plateau reset.",
    archive_extra="- **What shipped (r541, 260620.99):** `ContentConverter.#emptyCalloutHeadingBox` (+ `r529_handoff` false, `summary_run`); the r524 co-tag callout "
                  "sub-rule. Probes: all+B +0.0191 / EXTRA +25; hand-off +0.0148; Red-Flag stop +0.0189; max 1 plain +0.0121 / EXTRA +7; summary short run "
                  "+0.0182 / EXTRA +8 (shipped). Restore of the failed ship: `_s54_restore.sh 541` → manifest 0 pages differ.",
    extra_remove=("- **r541 BUILT, TOGGLED OFF, UNCOMMITTED",),
)
