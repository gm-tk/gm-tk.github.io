#!/usr/bin/env python3
"""ROUND 544 finalise (session 54 Round 7 — the red answer column; D10-3's widget-build lane). WSL. argv: MEAN RAW."""
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
        "CEDO202, GENO901, HES1007, JPFUN01). Checked at r544: none rides (MXDI202 is in r544's set, but r469b's other pages are not).")
entry = f"""## 2026-09-27 (round 544, build 260621.02) — THE RED ANSWER COLUMN: a `[Drag and drop]` matching table whose ANSWER column the writer typed red (`• Sarah spent $12 … ║ «3x = 12»`; a four-column table = two pair sets) now builds the KB 03B standard layout — the prompts the questions, the red answers the drags; 21 widgets / 8 modules, 18 the gold's own layout, verifier defect 0

### 1. WHAT CHANGED

**The class** (D10-3's widget-build lane, dragAndDrop): the r69 pair reader refused any red text and any width other than 2, and the maths writers mark the answer column red — `• Sarah spent $12 at the arcade … ║ «3x = 12»` (MXEO301 5.1), `3² ║ «3 × 3» ║ 3^6 ║ «3 × 3 × 3 × 3 × 3 × 3»` (MXEO301 1.0 — two pair sets in one four-column table), `4.14 pm ║ «16:14 hours» ║ 17:25 hours ║ «5:25 pm»` (MXFL301 7.0). The session-54 census (`outputs/_s54_r3_ddtable.cjs`, re-run on the r543 engine): **24 tables / 22 pages / 9 modules** (MXFL 11, MXEO 4, MXDI 3, ENGR 2, BLL 2, MXDB 2). The gold builds the standard matching layout, the right-hand pairs after the left-hand ones (MXEO301 1.0: drags `3 × 3`, `2 × 2 × 2 × 2`, `5 × … × 5`, then `3 × 3 × 3 × 3 × 3 × 3` …), the prompt's list bullet dropped.

**The fix** (`InteractiveBuilder.#dragAndDrop` + the new `#ddRedAnswerPairs`, data `interactive_builders.dragAndDrop.red_answer_column` {`max_width` 4, `strip_bullet`}, env **`DDREDANS_OFF`**): every row of every column pair empty or a black prompt beside a red-only answer; a black first row over them is the column-label header (dropped); a URL or a writer `[tag]` declines; the pairs feed r69's own standard render (its distinct-answer test included). Every table the r69 form already built is untouched (the branch fires only where the red guard or the width refused).

### 2. PROOF

- OFF probe (`DDREDANS_OFF=1`) over all 545 modules: **6,432 / 6,432 identical**; ON → 27 pages / **8 modules**, 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 544 --commit` PASS: 0 stale, containment 8 ⊆ 8, the 12-module spot-check byte-identical.
- **21 hand-off boxes → built widgets** (BLL174 / 175, ENGR302, MXDB302 ×2, MXDI202 ×3, MXEO301 ×4, MXFL301 ×3, MXFL302 ×6); `_verify_dragdrop.cjs` on the 8 modules: 33 widgets, defect 0 ✓. The gold's own widget (`outputs/_s54_r4_ddlayout.py`): **18 the same standard layout, 0 a different one**, 3 where the gold has no drag-and-drop sharing a drag (BLL175 1.0, MXDB302 1.0, MXEO301 5.0 — A1).
- Coverage dashboard: dragAndDrop built 184 → 205, interactive coverage 46.2 → 46.4 %.

### 3. PROTECTED GATES

Skeleton **56.3998 → {MEAN} % @ 2486 (held — a widget-build round, skeleton-blind by design)**, ≥50 1648, ≥75 309, ≥90 29; RAW 40.1172 → {RAW} %; compare_structure exact 17062 / EXTRA 206 / missing 581 held; body_compare ANY 233 held; leak 52 / 42; tags 9557; every verifier ✓, the dragdrop COUNT held 24 (`_r544_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 544`; `--gate-baseline-check` PASS. The still-a-box test moved 21 (≥ 20 — progress): the plateau window stays at 0.

**Ledger:** scoped #2 since the s54-r5 FULL · data `interactive_builders.dragAndDrop.red_answer_column` · env `DDREDANS_OFF` · code `InteractiveBuilder.#dragAndDrop` / `#ddRedAnswerPairs` · session 54 Round 7.
"""
F.finalise(
    N=544, old_build="260621.01", new_build="260621.02", entry=entry,
    config_comment="THE RED ANSWER COLUMN (session 54 Round 7; a matching table's red answer column, 2 or 4 columns). Env DDREDANS_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 544 BASELINE (the red answer column, `DDREDANS_OFF`; SCOPED, scoped #2 "
        f"since the s54-r5 FULL): SCAFFOLD mean {MEAN}% / >=50% 1648 / >=75% 309 / >=90% 29 / RAW {RAW}% @ 2486 pairs (held); cs exact 17062 / "
        f"EXTRA 206 / missing 581; body ANY 233; dragdrop widgets 24 on the gate set.**",
    og11="| `DDREDANS_OFF` | 544 | **THE RED ANSWER COLUMN** (session 54 Round 7). Reverts `interactive_builders.dragAndDrop.red_answer_column`: a matching table "
         "whose answer column is red (2 or 4 columns) is refused by the r69 red / width guards again — the 21 widgets return to hand-off boxes (the r543 output). |",
    og14=f"- **Build:** `260621.02` (round 544 — **the red answer column**; `DDREDANS_OFF`; scoped #2 since the s54-r5 FULL; 8 modules; 21 hand-off "
         f"boxes → built widgets, verifier defect 0; skeleton {MEAN} % (held), RAW {RAW} %).",
    gb_note=f"Round 544 (session 54 Round 7, 2026-09-27) — THE RED ANSWER COLUMN (DDREDANS_OFF): 8 modules; 21 hand-off boxes -> built standard widgets; "
            f"skeleton {MEAN} held; every other gate held; dragdrop count 24 held; scoped #2 since the s54-r5 FULL.",
    no_round=f"- **No round in flight** (27 Sept 2026 {T} NZDT, session 54 Round 7 — r544 (the red answer column) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r544** (260621.02); **LAST FULL = r542 (the session-54 Round 5 backstop)**; ledger **scoped #2** (6 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): " + RIDE,
    last_shipped=f"- LAST SHIPPED: **r544** (build 260621.02, 27 Sept {T} NZDT, session 54 Round 7 — THE RED ANSWER COLUMN, `DDREDANS_OFF`; SCOPED, "
                 "**scoped #2 since the s54-r5 FULL**; 8 modules; 21 hand-off boxes → built widgets (verifier defect 0; 18 the gold's layout, 0 different); "
                 f"skeleton {MEAN} % (held), RAW {RAW} %; every other gate held).",
    before_them_add="r542 the drag-and-drop label row",
    plateau="- Plateau window (§4): **0 of 3** — r544 a widget-build round, still-a-box moved 21 (≥ 20: progress); ",
    standing="- Standing facts: AppVersion **260621.02** (r544 the red answer column — session 54 Round 7, 27 Sept); before it 260621.01 (",
    roundlog=f"- s54-r7 (engine r544, build 260621.02, 27 Sept 05:36 → {T} NZDT) · THE RED ANSWER COLUMN (D10-3 build lane: a matching table's red answer "
             "column, 2 or 4 columns — 24 tables / 22 pages / 9 modules, the MX maths writers) · SHIPPED scoped #2 · 8 modules · 21 hand-off boxes → built "
             "widgets, gold layout 18 same / 0 different, verifier defect 0 · skeleton held (blind by design) · plateau 0 of 3.",
    archive_extra="- **What shipped (r544, 260621.02):** `#dragAndDrop` red-answer branch + `#ddRedAnswerPairs`; data `dragAndDrop.red_answer_column`. One probe, "
                  "shipped as built. Dashboard dragAndDrop 184 → 205 built.",
)
