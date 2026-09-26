#!/usr/bin/env python3
"""ROUND 542 finalise (session 54 Round 4 — the drag-and-drop label row; D10-3's widget-build lane). WSL. argv: MEAN RAW."""
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
        "CEDO202, GENO901, HES1007, JPFUN01). Checked at r542: none rides (no page of theirs is in r542's set).")
entry = f"""## 2026-09-27 (round 542, build 260621.00) — THE DRAG-AND-DROP LABEL ROW: a two-column `[Drag and drop]` table whose FIRST row is the writer's red column-label row (`Question ║ Answer`, `Word ║ [correct]`, `Clause [static] ║ Description`, `║ Correct answer – can we jumble them up though please`) now builds the KB 03B standard matching widget — the label row dropped, its instruction the Writers Note; 17 widgets / 17 modules, verifier defect 0, skeleton-neutral by design

### 1. WHAT CHANGED

**The class** (D10-3's widget-build lane; dragAndDrop is the largest un-built type, 1,024 hand-off boxes). The session-54 census of the refused single-table drag-and-drops (`outputs/_s54_r3_ddtable.cjs`, a Build hook over every module, joined to the r286 decline traces): the r69 pair reader refuses ANY table carrying red text, and **47** refused two-column tables carry their red ONLY in the first row — the writer's column-label row. Two shapes hide there: N:N matching under a role label (`Question ║ Answer`, `Word ║ [correct]`, `(Static) ║ (Draggable)` — the gold's standard layout, SCES201 / OSSM401 / WJFUN211) and a two-category sort under heading labels (`[H4] Benefits ║ [H4] Risks`, `[static heading] AI can ║ AI can't`, a `sort` instruction — the gold's COLUMN layout, OSSM501 / OSAI201).

**The fix** (`InteractiveBuilder.#dragAndDrop`, data `interactive_builders.dragAndDrop.label_row`, env **`DDLABELROW_OFF`**): a first row with red text over red-free rows, whose text carries a matching-role cue (`role_pattern`) and no category cue (`category_pattern` — a `[Hn]` marker, `static` / `column heading`, `sort` / `categor` / `group`) and no URL, is the header — dropped; a real-word red run in it rides along as the red Writers Note (the r350 `#ddIsNote` test). Under a dropped label row only, a drawn blank in a label (`blank_pattern` — BLL266, the gold's FIB) and a table whose every label equals its answer exactly (`decline_identity` — BLLR201–203 `cartoonist ║ cartoonist`) keep the hand-off box. Every widget the r69 form already built is untouched by construction (the branch runs only where the red guard refused).

### 2. PROOF

- OFF probe (`DDLABELROW_OFF=1`) over all 545 modules: **6,432 / 6,432 identical**; ON → 34 pages / **17 modules** (their `_interactives.txt` reports + 17 pages), 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 542 --commit` PASS: 0 stale, containment 17 ⊆ 17, the 12-module spot-check byte-identical.
- **17 hand-off boxes → built widgets** (BLL111 / 121 / 131 / 167, CHFUN05 / 06, ENFUN05 / 08, ENGC302, MXEX301, MXFUN01 / 02, OSBY101, OSSM401, PWY1002, WJFUN205 / 211). `_verify_dragdrop.cjs` on the 17: **21 widgets / 129 drags, defect 0 ✓**. The gold's own widget for each (`outputs/_s54_r4_ddlayout.py`, matched by shared drags): **11 the same standard layout, 0 a different layout**, 6 where the gold has no drag-and-drop sharing a drag (BLL167, CHFUN05 / 06, ENGC302, MXFUN02, OSBY101 — the writer asked for one: A1, judged on the verifier). Two probe designs dropped on the gold check: without the blank / identity / unbracketed-heading guards 22 widgets (BLL266 gold FIB, OSAI201 2.0 gold column, BLLR201–203 identity tables); a case-folded identity test wrongly refused BLL111 / 121 / 131's `a ║ A` letter matches (the gold's standard) — made exact.
- The verifier COUNT on its recorded 14-module set GREW 21 → 23 (CHFUN05 1 → 2, ENFUN08 1 → 2) — recorded (`VERIFY_COUNT_RECORD=1`).

### 3. PROTECTED GATES

Skeleton **56.3982 → {MEAN} % @ 2486 (+0.0011pp)**, ≥50 1647, ≥75 309, ≥90 29 held; RAW 40.0522 → {RAW} %; compare_structure exact 17062 / EXTRA 206 / missing 581 held; body_compare ANY 233 held; leak 52 / 42; tags 9557; every verifier ✓ (`_r542_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 542`; `--gate-baseline-check` PASS. A widget-build round (LOOP §4): skeleton-blind by design; the still-a-box test moved 17 (< 20) — plateau **1 of 3**.

**Ledger:** scoped #7 since the s52-r11 FULL · data `interactive_builders.dragAndDrop.label_row` · env `DDLABELROW_OFF` · code `InteractiveBuilder.#dragAndDrop` · session 54 Round 4.
"""
F.finalise(
    N=542, old_build="260620.99", new_build="260621.00", entry=entry,
    config_comment="THE DRAG-AND-DROP LABEL ROW (session 54 Round 4; a red column-label row over a two-column pair table is the header). Env DDLABELROW_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 542 BASELINE (the drag-and-drop label row, `DDLABELROW_OFF`; SCOPED, scoped #7 "
        f"since the s52-r11 FULL): SCAFFOLD mean {MEAN}% / >=50% 1647 / >=75% 309 / >=90% 29 / RAW {RAW}% @ 2486 pairs (+0.0011pp); cs exact 17062 / "
        f"EXTRA 206 / missing 581; body ANY 233; dragdrop widgets 23 on the gate set.**",
    og11="| `DDLABELROW_OFF` | 542 | **THE DRAG-AND-DROP LABEL ROW** (session 54 Round 4). Reverts `interactive_builders.dragAndDrop.label_row`: a two-column pair table "
         "with a red first (column-label) row is refused by the r69 red guard again — the 17 widgets return to hand-off boxes (the r541 output). |",
    og14=f"- **Build:** `260621.00` (round 542 — **the drag-and-drop label row**; `DDLABELROW_OFF`; scoped #7 since the s52-r11 FULL; 17 modules; 17 hand-off "
         f"boxes → built widgets, verifier defect 0; skeleton {MEAN} % (+0.0011pp), RAW {RAW} %).",
    gb_note=f"Round 542 (session 54 Round 4, 2026-09-27) — THE DRAG-AND-DROP LABEL ROW (DDLABELROW_OFF): 17 modules; 17 hand-off boxes -> built widgets; "
            f"skeleton 56.3982 -> {MEAN} (+0.0011pp); every other gate held; dragdrop count 21 -> 23 recorded; scoped #7 since the s52-r11 FULL.",
    no_round=f"- **No round in flight** (27 Sept 2026 {T} NZDT, session 54 Round 4 — r542 (the drag-and-drop label row) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r542** (260621.00); **LAST FULL = r534 (the session-52 Round 11 backstop)**; ledger **scoped #7** (1 of headroom — "
             "the FULL backstop is due at the next ship). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): " + RIDE,
    last_shipped=f"- LAST SHIPPED: **r542** (build 260621.00, 27 Sept {T} NZDT, session 54 Round 4 — THE DRAG-AND-DROP LABEL ROW, `DDLABELROW_OFF`; SCOPED, "
                 "**scoped #7 since the s52-r11 FULL**; 17 modules; 17 hand-off boxes → built widgets (verifier defect 0; 11 match the gold's layout, 0 differ); "
                 f"skeleton 56.3982 → {MEAN} % (+0.0011pp), RAW {RAW} %; every other gate held).",
    before_them_add="r539 the one-level shift under a body [H1]",
    plateau="- Plateau window (§4): **1 of 3** — r542 a widget-build round, still-a-box moved 17 (< 20: counts); ",
    standing="- Standing facts: AppVersion **260621.00** (r542 the drag-and-drop label row — session 54 Round 4, 27 Sept); before it 260620.99 (",
    roundlog=f"- s54-r4 (engine r542, build 260621.00, 27 Sept 04:14 → {T} NZDT) · THE DRAG-AND-DROP LABEL ROW (D10-3 build lane: a red column-label row over a "
             "2-column pair table is the header — `_s54_r3_ddtable.cjs`: 47 refused tables red only in row 1) · SHIPPED scoped #7 · 17 modules · 17 hand-off boxes → "
             "built widgets, verifier defect 0, gold layout 11 same / 0 different · skeleton +0.0011pp (blind by design) · plateau 1 of 3.",
    archive_extra="- **What shipped (r542, 260621.00):** `InteractiveBuilder.#dragAndDrop` label-row branch + its blank / identity guards; data `dragAndDrop.label_row`. "
                  "Probes: v1 22 widgets (BLL266 FIB, OSAI201 column, BLLR identity — guarded), v2 case-folded identity (BLL111/121/131 lost — made exact), v3 17 "
                  "widgets shipped. dragdrop count 21 → 23 recorded.",
)
