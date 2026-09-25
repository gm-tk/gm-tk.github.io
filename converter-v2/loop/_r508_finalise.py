#!/usr/bin/env python3
"""ROUND 508 finalise (session 49 Round 9 — the nested bracket, NESTBRACKET_OFF). WSL. argv: MEAN RAW."""
import sys
import _s49_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-25 (round 508, build 260620.71) — THE NESTED BRACKET: `[Drag and drop [autocheck]]` is a drag-and-drop with a condition, not a typing quiz — the writer's widget name no longer vanishes (50 pages / 10 modules; "typing" hand-offs 77 → 19, 9 more dragAndDrops built; skeleton +0.0449pp, ≥50 +3, ≥75 +1)

### 1. WHAT CHANGED

**The find** (the D15 decisions session's loop-authority item (a), measured this round): `TagNormaliser.Parse` extracts bracket fragments with `/\\[([^\\[\\]]+)\\]/` — innermost only — so a NESTED red bracket kept just its inner words: `[Drag and drop [autocheck]]` → `autocheck` → an alias of `typing quiz` (`Tag_Lexicon.json` `_meta.condition_primary_demote`) → the hand-off box said "⚙ INTERACTIVE (un-built): typing" and the dragAndDrop builder never ran; `[Multichoice [autocheck]]`, `[reorder [autocheck]]`, `[drop down quiz [autocheck]]` the same. KB constraint 14: the writer's tag decides the component. Census (`outputs/_s49_r9_nested.cjs`): **108 nested red brackets / 24 modules, 76 with `autocheck` inside** (outer: drag and drop 25, multichoice 16, reorder 9, mtk quiz 6, radioquiz 5, dropquiz 3, memory game / wordfind …). The separate-bracket form `[Drag and drop] [autocheck]` already read right.

**The fix** (`TagNormaliser.Parse`, before step 2; data `Tag_Lexicon.json` `_meta.nested_bracket_flatten`; env `NESTBRACKET_OFF`): `[a [b] c]` is flattened into `[a c] [b]` (an empty outer part — `[[hover trigger]]` — leaves `[b]` alone), so the widget tag is read and the condition rides beside it (`[Drag and drop [autocheck]]` → primary `drag and drop`, tags drag and drop + typing quiz — the r-demote keeps the widget primary).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **50 pages / 10 modules** (FRNO901 FRNO902 GEWHA JPFUN01 JPFUN02 PWY1001 PWY1002 PWY1007 PWY1008 PWY1009). Regenerated = ON byte-for-byte (69 / 69); `scoped_ship.sh` PASS.
- **The hand-offs name their real widget** (`_r508_tally.sh`, the 50 pages): "typing" **77 → 19**; dragAndDrop 5 → 20, multiChoiceQuiz 10 → 24, reorder 3 → 12, radioQuiz 1 → 4, memoryGame 1 → 4, wordFind 1 → 3, selectionBox 1 → 3, dropDown 17 → 18, clickingOrder 0 → 1 — the types the golds build there (FRNO901 gold: dragAndDrop 7 / mcq 6 / reorder 55; PWY1001: dragAndDrop 4 / mcq 9 / radio 1; typing ≈ 0). **Built dragAndDrops 3 → 12**; `_verify_dragdrop.cjs` over the 10 modules: 14 widgets, **defect 0 ✓**.
- Not this round: the one-word `radioquiz` (no alias — `[radioquiz [autocheck]]` still reads `typing quiz`, 5); `[mtk quiz] [autocheck]` (the demote prefers an INTERACTIVE tag only, 6).

### 3. PROTECTED GATES

- Skeleton **55.5434 → {MEAN} % @ 2486**, RAW 39.475 → {RAW} %; **≥50 1599 → 1602 (+3)**, **≥75 276 → 277 (+1)**; **26 movers, 21 up / 5 down** (pp-sum +111.8): PWY1001_1_1 **48.7 → 60.7**, PWY1009_3_1_0 +10.8, PWY1008_2_1_0 +10.0, FRNO902_7_0 **42.1 → 52.0**, FRNO902_2_0 44.0 → 50.2, FRNO902_3_0 48.8 → 51.8, PWY1009_2_1_0 **72.1 → 75.9**; the 5 down NAMED — PWY1009_3_3_0 52.5 → 48.0 (a ≥50 loss inside the +3 net: its box is now the reorder / dragAndDrop hand-off the gold builds as a widget), PWY1009_2_2_0 −1.9, PWY1008_3_1_0 −1.1, JPFUN01_0_0 / FRNO902_8_0 −0.2. cs / body / clean / leak EXACT; every verifier ✓, every COUNT held (`_r508_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 508`; `--gate-baseline-check` PASS. Plateau: +0.0449pp — a real gain: reset.

**Ledger:** scoped #3 since the r505 FULL · data `Tag_Lexicon._meta.nested_bracket_flatten` · env `NESTBRACKET_OFF` · code `TagNormaliser.Parse` · tools `_s49_r9_nested.cjs`, `_s49_r9_tagparse.cjs`, `_r508_tally.sh`, `_r508_finalise.py` · session 49 Round 9 (a PICK pass: the placement census re-run, `_pc_s49.md` — SAME 40.3 %, MOVED 22.3 %, its CANDIDATE rows the known lanes).
"""
F.finalise(
    N=508, old_build="260620.70", new_build="260620.71", entry=entry,
    config_comment="THE NESTED BRACKET (session 49 Round 9): `[Drag and drop [autocheck]]` flattens to `[Drag and drop] [autocheck]` — the "
                   "widget name no longer vanishes. Env NESTBRACKET_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 508 BASELINE (the nested bracket, `NESTBRACKET_OFF`; SCOPED, "
        f"scoped #3 since the r505 FULL): SCAFFOLD mean {MEAN}% / >=50% 1602 / >=75% 277 / >=90% 26 / RAW {RAW}% @ 2486 pairs — "
        f"+0.0449pp (21 up / 5 down), >=50 +3, >=75 +1; 'typing' hand-offs 77 → 19, 9 dragAndDrops built.**",
    og11="| `NESTBRACKET_OFF` | 508 | **THE NESTED BRACKET** (session 49 Round 9). Reverts `Tag_Lexicon._meta.nested_bracket_flatten`: "
         "`[Drag and drop [autocheck]]` reads innermost-only again (`autocheck` → typing quiz, the widget name lost); byte-identical to "
         "r507. |",
    og14=f"- **Build:** `260620.71` (round 508 — **the nested bracket**; `NESTBRACKET_OFF`; scoped #3 since the r505 FULL; 50 pages / 10 "
         f"modules; skeleton {MEAN} % @ 2486, +0.0449pp, ≥50 +3, ≥75 +1).",
    gb_note=f"Round 508 (session 49 Round 9, 2026-09-25) — THE NESTED BRACKET (NESTBRACKET_OFF): 50 pages / 10 modules; SCAFFOLD "
            f"55.5434 -> {MEAN} @ 2486, 21 up / 5 down; >=50 1599 -> 1602; >=75 276 -> 277; typing hand-offs 77 -> 19, dragAndDrops "
            f"built 3 -> 12 (verifier defect 0); scoped #3.",
    no_round=f"- **No round in flight** (25 Sept 2026 {T}, session 49 Round 9 — r508 (the nested bracket) SHIPPED and committed; the "
             "in-flight marker is cleared). LAST SHIPPED **r508** (260620.71); **LAST FULL = r505 (the session-49 Round 6 backstop)**; "
             "ledger **scoped #3** (5 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages) / "
             "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages) / `_r489_accbullet_declined.patch` (the accordion bulleted "
             "bold lead, 8 accordions / 4 modules) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page).",
    last_shipped=f"- LAST SHIPPED: **r508** (build 260620.71, 25 Sept {T}, session 49 Round 9 — THE NESTED BRACKET, `NESTBRACKET_OFF`; "
                 "SCOPED, **scoped #3 since the r505 FULL**; 50 pages / 10 modules; 'typing' hand-offs 77 → 19, dragAndDrops built 3 → "
                 f"12, verifier defect 0; **skeleton 55.5434 → {MEAN} % @ 2486 (+0.0449pp)**, 21 up / 5 down, **≥50 1602 (+3)**, **≥75 "
                 "277 (+1)**; cs / body / clean / leak EXACT).",
    before_them_add="D15-18 part 2 the lost RHS boxes",
    plateau="- Plateau window (§4): **0 of 3** — r508 +0.0449pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.71** (r508 the nested bracket — session 49 Round 9, 25 Sept); before it 260620.70 (",
    roundlog=f"- s49-r9 (engine r508, build 260620.71, 25 Sept 21:10 → {T}) · a PICK pass (the placement census re-run: SAME 40.3 %) then "
             "THE NESTED BRACKET (`[Drag and drop [autocheck]]` flattened — the widget name kept; KB c14) · SHIPPED scoped #3 · 50 pages / "
             "10 modules, 'typing' hand-offs 77 → 19, 9 dragAndDrops built · skeleton **+0.0449pp**, ≥50 +3, ≥75 +1 · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r508, 260620.71):** `Tag_Lexicon._meta.nested_bracket_flatten` (env `NESTBRACKET_OFF`), "
                  "`TagNormaliser.Parse`. Probe OFF 0; ON 50 pages / 10 modules; +0.0449pp.",
)
