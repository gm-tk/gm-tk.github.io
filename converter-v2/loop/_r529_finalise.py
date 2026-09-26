#!/usr/bin/env python3
"""ROUND 529 finalise (session 52 Round 2 — the summary heading's alert box). WSL. argv: MEAN RAW."""
import sys
import _s52_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 529, build 260620.88) — THE SUMMARY HEADING'S ALERT BOX: a lesson's closing `Lesson Summary` / `Key points` / `Summary` / `What have we learned` heading typed as a plain heading opens the `div.alert > row > col-12` box the gold puts it in (KB 14.8 'Lesson summary alert' for HPE; KB 05B `<h4>Key points</h4>`; per family); 19 modules, skeleton +0.1122pp, compare_structure exact +119 / missing −138

### 1. WHAT CHANGED

**The class** (the s51-r13 lead — compare_structure's MISSING `div.alert`, 768 elements / 298 pages / 149 modules — cue-censused this round: `_s52_items_dump.cjs` dumps every module's item stream, `_s52_r2_alertcue.py` finds each gold alert box whose first element Claude leaves bare in the WT: 288 boxes, 258 located; the largest cue families are the writer's `[Alert]` + a heading (25 runs / 8 modules — the parked r524 lane) and SUMMARY HEADINGS with no bracket cue at all). `_s52_r2_headalert.py` / `…2.py` (every Claude-bare heading matched to its gold heading): **Lesson Summary** HIS 13 / 17, HPRE 14 / 14, SSOG 9 / 11, SSEA 5 / 5, CEDK 1 / 1 (XGF 0 / 8, TEDC 0 / 6 leave it bare; SSCI 8 / 12 is one module each way — SSCI205 all, SSCI104 none — a tie, not listed); **Key points** PES 24 / 24 (gold `<h4>`); **Summary** SSFUN 4 / 4 (`<h4>`); **What have we learned** BLLR 3 / 3 (`<h5>`). XGF's Key questions (8 / 11) is a different box (a bare `div.alert > h4 + ul`) and is not listed.

**The fix** (`ContentConverter.#summaryHeadingAlert`, a page post-pass between `#journalInstructionBox` and `#introHeadingFullRow`; data `body_region.summary_heading_alert` {{rules [{{pattern, families, level, hint_inside}}], exclude_ancestor_pattern, skip_if_rest_pattern, box_open, box_close}}, env **`SUMALERT_OFF`**): a heading that is a content column's direct child, outside every box and widget, whose text matches a rule for the module's family opens the box. The box holds what the gold's holds (`_s52_r2_sumbox.py`: HIS `p` 57 / 60, PES `ul` 34 / 35, SSOG `p ol p` / `p ul p`, SSCI / SSEA the hint right AFTER the box, HPRE `p ol` / `p p.hint p`): the heading, one plain paragraph, any lists, one closing paragraph after a list, and the hint only where the rule says `hint_inside` (HPE — KB 14.8's sequence); the rest of the column moves to a new row in a column of the same class. A summary whose column goes on to the end-of-module dropbox is that box's (HIS1006's last page — −13.25 unguarded). The first cut (the column's whole remainder boxed) scored +0.0945pp with SSEA203 / SSCI205 / XGF9004 down; the extent rule and the XGF / SSCI exclusions removed those.

### 2. PROOF

- In-memory probe over all 545 modules: `SUMALERT_OFF=1` → 6,432 / 6,432 pages identical; ON → **78 pages / 19 modules**; 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 529 --commit` PASS: 0 stale, containment 19 ⊆ 19, the 12-module spot-check byte-identical. The first scoped ship (with SSCI) FAILED on compare_structure EXTRA +10 (SSCI104 8 + HPRE301 2); SSCI was withdrawn and the corpus restored (`SUMALERT_OFF=1 _s45_regen.sh 529` → `_content_manifest.py diff` 0 pages) before the re-probe.
- The skeleton gate's own `match()` (`_s51_prescore.py`): **+0.1122pp, 61 up / 11 down** (PES1007_2_0 +14.5, PES1004_2_0 +11.8, PES1003_4_0 +11.2, …; the dips ≤ 2.0 — HPRE301_3_0 −1.99 (the KB-form hint, below), HIS1002_6_0 −1.18, SSEA203_3_0 −1.05).
- **NAMED KB override (`--accept-named "EXTRA container"`):** compare_structure EXTRA 201 → 203 = HPRE301_2_0 / HPRE301_3_0's `Need help?` hint inside the box — KB 14.8 lists `[Hint Button] Need help?` in the HPE lesson-summary alert (HPRE203's gold, 6 pages, has it inside); HPRE301's gold puts it after the box.

### 3. PROTECTED GATES

Skeleton **56.1269 → {MEAN} % @ 2486 (+0.1122pp)**, ≥50 1628 → 1632, ≥75 295 → 300, ≥90 28; RAW 39.855 → {RAW} %; compare_structure exact 16867 → 16986 (+119) / missing 810 → 672 (−138) / EXTRA 201 → 203 (+2, NAMED above); body_compare ANY 234 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r529_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 529`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.1122pp).

**Ledger:** scoped #2 since the s51-r12 FULL (r526) · data `body_region.summary_heading_alert` · env `SUMALERT_OFF` · code `ContentConverter.#summaryHeadingAlert` · session 52 Round 2.
"""
F.finalise(
    N=529, old_build="260620.87", new_build="260620.88", entry=entry,
    config_comment="THE SUMMARY HEADING'S ALERT BOX (session 52 Round 2; KB 14.8 / 05B; per family). Env SUMALERT_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 529 BASELINE (the summary heading's alert box, `SUMALERT_OFF`; "
        f"SCOPED, scoped #2 since the s51-r12 FULL): SCAFFOLD mean {MEAN}% / >=50% 1632 / >=75% 300 / >=90% 28 / RAW {RAW}% @ 2486 pairs "
        f"(+0.1122pp); cs exact 16986 / EXTRA 203 (+2 NAMED, KB 14.8) / missing 672; body ANY 234.**",
    og11="| `SUMALERT_OFF` | 529 | **THE SUMMARY HEADING'S ALERT BOX** (session 52 Round 2). Reverts `body_region.summary_heading_alert`: "
         "the bare `Lesson Summary` / `Key points` / `Summary` / `What have we learned` heading stays in the plain content column (the r528 "
         "output exactly). |",
    og14=f"- **Build:** `260620.88` (round 529 — **the summary heading's alert box**; `SUMALERT_OFF`; scoped #2 since the s51-r12 FULL; "
         f"19 modules; skeleton {MEAN} % (+0.1122pp), RAW {RAW} %, cs exact +119 / missing −138).",
    gb_note=f"Round 529 (session 52 Round 2, 2026-09-26) — THE SUMMARY HEADING'S ALERT BOX (SUMALERT_OFF): 19 modules; skeleton 56.1269 -> "
            f"{MEAN} (+0.1122pp), >=50 1632, >=75 300; cs exact 16986 / EXTRA 203 (+2 NAMED: HPRE301's hint inside, KB 14.8) / missing 672; "
            f"every other gate held; scoped #2.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 52 Round 2 — r529 (the summary heading's alert box) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r529** (260620.88); **LAST FULL = r526 (the session-51 Round 12 "
             "backstop)**; ledger **scoped #2** (6 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / "
             "9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: "
             "Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix) / `_r524_declined.patch` "
             "(the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list after its title). Checked at "
             "r529: none rides — no patch has ALL its pages inside r529's 19 modules (r469b: HIS1002 / HPRE203 / SSOG105 in, 6 out).",
    last_shipped=f"- LAST SHIPPED: **r529** (build 260620.88, 26 Sept {T}, session 52 Round 2 — THE SUMMARY HEADING'S ALERT BOX, "
                 "`SUMALERT_OFF`; SCOPED, **scoped #2 since the s51-r12 FULL**; 19 modules; skeleton 56.1269 → "
                 f"{MEAN} % (+0.1122pp), ≥50 1632, ≥75 300, RAW {RAW} %; cs exact +119 / missing −138 / EXTRA +2 NAMED (KB 14.8); every "
                 "other gate held).",
    before_them_add="r526 the BLL introduction heading's own full-width row",
    plateau="- Plateau window (§4): **0 of 3** — r529 +0.1122pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.88** (r529 the summary heading's alert box — session 52 Round 2, 26 Sept); before it "
             "260620.87 (",
    roundlog=f"- s52-r2 (engine r529, build 260620.88, 26 Sept 15:48 → {T}) · a PICK pass (the s51-r13 `div.alert` MISSING cue census: "
             "288 bare gold boxes, `_s52_r2_alertcue.py`) then THE SUMMARY HEADING'S ALERT BOX (Lesson Summary / Key points / Summary / "
             "What have we learned, per family; KB 14.8 / 05B) · SHIPPED scoped #2 (the first ship FAILED on cs EXTRA +10 — SSCI withdrawn, "
             "the corpus restored) · 19 modules · skeleton **+0.1122pp**, ≥50 +4, ≥75 +5, cs exact +119 / missing −138 / EXTRA +2 NAMED · "
             "plateau reset (0 of 3).",
    archive_extra="- **What shipped (r529, 260620.88):** `ContentConverter.#summaryHeadingAlert`; data `body_region.summary_heading_alert`. "
                  "Probe OFF 6,432 / 6,432 identical; ON 78 pages / 19 modules; +0.1122pp; cs missing −138; EXTRA +2 NAMED (HPRE301, KB 14.8).",
)
