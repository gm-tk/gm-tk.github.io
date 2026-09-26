#!/usr/bin/env python3
"""ROUND 543 finalise (session 54 Round 6 — the marked category sort; D10-3's widget-build lane). WSL. argv: MEAN RAW."""
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
        "CEDO202, GENO901, HES1007, JPFUN01). Checked at r543: none rides (BLL240 is in r543's set but r540's other seven are not).")
entry = f"""## 2026-09-27 (round 543, build 260621.01) — THE MARKED CATEGORY SORT: a drag-and-drop sort whose header the writer marked in red (`[H4] Benefits ║ [H4] Risks`, `AI can [static heading]`, a fully-red `Short vowel ║ Long vowel` row) or whose ITEMS are typed red (`/sk/ sound ║ /s/ sound` over `scooter ║ science`) now builds the KB 03B column layout, 2 columns included; 21 widgets / 17 modules, 18 the gold's own column layout, verifier defect 0

### 1. WHAT CHANGED

**The class** (D10-3's widget-build lane, dragAndDrop — the largest un-built type): the r351 column reader refused any red cell and any 2-column table; the writer marks a sort's header with a red heading marker or a red label row, or types the drag items red under a black header (the session-54 census `outputs/_s54_r3_ddtable.cjs`: red-item sorts 16 bundles / 14 pages / 12 modules — BLL240 / 250, MXFU402, MXDI103, CEDT501 ×2, MXFL202 ×2, MXDB302, FRFUN07, WJFUN109 …; plus the heading-labelled rows r542's label-row rule sends on as sorts — OSSM501, OSAI201 / 301 / 501, OSBY401 …).

**The fix** (`InteractiveBuilder.#dragAndDropColumn`, data `interactive_builders.dragAndDrop.column.marked`, env **`DDCOLMARK_OFF`**): a header cell's red run that is a heading marker (`header_marker_pattern` — `[Hn]`, `[static]` / `[static heading]`, `[column heading]` / `[column title]`) is stripped and the black text is the label; a fully-red short cell is the label (`red_label`); a data cell of red text only (black separators allowed) gives its item(s); a half-red table (red AND black items) declines; a table so marked (a marked header, or every item red) may be 2 columns wide (`min_columns` 2 — an unmarked 2-column table stays the r69 pair reader's). **Repair (attempt 1, after the first ship FAILED on the skeleton mean −0.00003pp):** the members rule (`#ddWithMembers`) re-rendered the writer's asterisked list of the phrases above CEDT501 6.1's table as paragraphs although every phrase is a drag item (the gold shows the instruction line only) — under a marked sort only, a black line that merely repeats a drag item is consumed (`echo_consumed`); CEDT501_6_1 −0.62 → +0.79. An unmarked table reads exactly as r351 (the OFF probe is byte-identical on every module).

### 2. PROOF

- OFF probe (`DDCOLMARK_OFF=1`) over all 545 modules: **6,432 / 6,432 identical**; ON → 36 pages / **17 modules**, 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 543 --commit` PASS (the second ship; the first FAILED and was restored — `_s54_restore.sh 543`, manifest 0 pages differ): 0 stale, containment 17 ⊆ 17, the 12-module spot-check byte-identical.
- **21 hand-off boxes → built column widgets**; `_verify_dragdrop.cjs` on the 17 modules: 29 widgets, defect 0 ✓. The gold's own widget (`outputs/_s54_r4_ddlayout.py`): **18 the same column layout**, 1 different (OSGM401 4.0 — `[H4] Description ║ [H4] Gaming feature`, the gold's standard match), 2 where the gold has no drag-and-drop sharing a drag (MXDI202 8.0, MXFL202 2.0 — A1, judged on the verifier).
- The skeleton's `match()`: 4 pages moved, 3 up / 1 down, +1.35pp-sum; the dip NAMED: MXFL202_2_0 −0.21 with its position-free overlap 90 → 91 of 178 (`outputs/_s54_companion.py` — an alignment artefact).
- The verifier COUNT on its recorded set grew 23 → 24 (ENFUN04 3 → 4) — recorded. Coverage dashboard: dragAndDrop built 163 → 184, interactive coverage 45.9 → 46.2 %.

### 3. PROTECTED GATES

Skeleton **56.3993 → {MEAN} % @ 2486 (+0.0005pp)**, ≥50 1647 → 1648, ≥75 309, ≥90 29; RAW 40.0821 → {RAW} %; compare_structure exact 17062 / EXTRA 206 / missing 581 held; body_compare ANY 233 held; leak 52 / 42; tags 9557; every verifier ✓ (`_r543_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 543`; `--gate-baseline-check` PASS. A widget-build round (LOOP §4): the still-a-box test moved 21 (≥ 20 — progress) — the plateau window resets.

**Ledger:** scoped #1 since the s54-r5 FULL · data `interactive_builders.dragAndDrop.column.marked` · env `DDCOLMARK_OFF` · code `InteractiveBuilder.#dragAndDropColumn` + `#ddWithMembers` (echo) · session 54 Round 6.
"""
F.finalise(
    N=543, old_build="260621.00", new_build="260621.01", entry=entry,
    config_comment="THE MARKED CATEGORY SORT (session 54 Round 6; a red-marked header or red items make a column sort, 2 columns included). Env DDCOLMARK_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 543 BASELINE (the marked category sort, `DDCOLMARK_OFF`; SCOPED, scoped #1 "
        f"since the s54-r5 FULL): SCAFFOLD mean {MEAN}% / >=50% 1648 / >=75% 309 / >=90% 29 / RAW {RAW}% @ 2486 pairs (+0.0005pp); cs exact 17062 / "
        f"EXTRA 206 / missing 581; body ANY 233; dragdrop widgets 24 on the gate set.**",
    og11="| `DDCOLMARK_OFF` | 543 | **THE MARKED CATEGORY SORT** (session 54 Round 6). Reverts `interactive_builders.dragAndDrop.column.marked`: a red-marked header, "
         "red items and every 2-column table are refused by the r351 column reader again (and the r543 echo consumption goes) — the 21 widgets return to "
         "hand-off boxes (the r542 output). |",
    og14=f"- **Build:** `260621.01` (round 543 — **the marked category sort**; `DDCOLMARK_OFF`; scoped #1 since the s54-r5 FULL; 17 modules; 21 hand-off "
         f"boxes → built column widgets, verifier defect 0; skeleton {MEAN} % (+0.0005pp), RAW {RAW} %).",
    gb_note=f"Round 543 (session 54 Round 6, 2026-09-27) — THE MARKED CATEGORY SORT (DDCOLMARK_OFF): 17 modules; 21 hand-off boxes -> built column widgets; "
            f"skeleton 56.3993 -> {MEAN} (+0.0005pp), >=50 +1; dragdrop count 23 -> 24 recorded; scoped #1 since the s54-r5 FULL.",
    no_round=f"- **No round in flight** (27 Sept 2026 {T} NZDT, session 54 Round 6 — r543 (the marked category sort) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r543** (260621.01); **LAST FULL = r542 (the session-54 Round 5 backstop)**; ledger **scoped #1** (7 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): " + RIDE,
    last_shipped=f"- LAST SHIPPED: **r543** (build 260621.01, 27 Sept {T} NZDT, session 54 Round 6 — THE MARKED CATEGORY SORT, `DDCOLMARK_OFF`; SCOPED, "
                 "**scoped #1 since the s54-r5 FULL**; 17 modules; 21 hand-off boxes → built column widgets (verifier defect 0; 18 the gold's layout, 1 different); "
                 f"skeleton 56.3993 → {MEAN} % (+0.0005pp), ≥50 1648, RAW {RAW} %; every other gate held).",
    before_them_add="r541 the alert whose title is a heading",
    plateau="- Plateau window (§4): **0 of 3** — r543 a widget-build round, still-a-box moved 21 (≥ 20: progress, reset); ",
    standing="- Standing facts: AppVersion **260621.01** (r543 the marked category sort — session 54 Round 6, 27 Sept); before it 260621.00 (",
    roundlog=f"- s54-r6 (engine r543, build 260621.01, 27 Sept 05:07 → {T} NZDT) · THE MARKED CATEGORY SORT (D10-3 build lane: a red heading marker / red label row / "
             "red items make a column sort, 2 columns included) · the first ship FAILED on the skeleton mean −0.00003pp (CEDT501 6.1's echoed phrase list), "
             "restored, repaired (`echo_consumed`) · SHIPPED scoped #1 · 17 modules · 21 hand-off boxes → built widgets, gold layout 18 same / 1 different · "
             "skeleton +0.0005pp, ≥50 +1 · plateau reset.",
    archive_extra="- **What shipped (r543, 260621.01):** `#dragAndDropColumn` marked-sort reading + `#ddWithMembers` echo consumption; data `column.marked`. "
                  "Ship 1 FAILED (mean −0.00003pp: CEDT501_6_1 −0.62, overlap flat, +2 Claude lines = the writer's asterisked phrase list re-rendered); "
                  "restored; repaired; ship 2 PASS (+0.0005pp). dragdrop count 23 → 24 recorded.",
)
