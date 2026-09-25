#!/usr/bin/env python3
"""ROUND 510 finalise (session 50 Round 1 — THE WIDGET NAMED AFTER A GENERIC INTERACTIVE BRACKET, IQFREEWIDGET_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 510, build 260620.73) — THE WIDGET NAMED AFTER A GENERIC INTERACTIVE BRACKET: `[interactive activity] drag and drop`, `[Interactive tool] Flip cards`, `[Interactive] Please create a drag and drop …` now name the writer's widget instead of a plain activity box (284 spans / 41 modules; 43 modules regenerated; skeleton +0.1109pp)

### 1. WHAT CHANGED

**The class** (KB constraint 14 — the writer's tag decides the component; the r92 `[Activity 1A drag and drop]` precedent reads activity + widget in one span, the widget primary): the bracket only says "an interactive goes here" and the writer names the widget in the SAME red span after it. Those words sat in `free`, so the span parsed as a plain activity box and the widget was never recognised. **Census** (`outputs/_s50_r510_spans.cjs` → `_s50_r510_spans.log`, every red span whose parse changes): **284 spans / 41 modules** — drag and drop 110, flip card 38, dropdown 27, mcq 25, memory game 17, carousel 14, radio quiz 12, checklist 6, crossword 6, accordion 5, timeline 5, word select 4, slider 3, word find 3, click drop 2, sketcher 2, reorder 2, typing 2, puzzle 1 (HPFUN1–9, MXDI2, MXFL1–2, MXFU2, TWHA906, TWHK907, ANZH2–4, HIS1003 / 1004, SSFUN, TRR109–113, EXBP901, HPRE203, SSEA203).

**The fix** (`TagNormaliser.Parse`, before step 4; data `Tag_Lexicon.json` `_meta.interactive_qualifier_free_widget`; env `IQFREEWIDGET_OFF`): when EVERY bracket of a span matches the generic qualifier (`interactive` / `interactive activity|tool|element|widget`, an optional id) and no widget tag was found, the free text is resolved as a fragment and its first INTERACTIVE tag joins the span — **only when its alias starts within the first `max_lead_words` = 4 words** (the writer NAMES it: `drag and drop images into circles`, `please create a drag and drop activity`; ANZH301 / 302's `Please include this template here. Are there digital drawing tools …` had read as an empty sketcher box) and the text does not match `free_deny_pattern` (`text to speech` — HIS1004's three requests had read as speech bubbles).

**Two builder guards the new recognition needed** (each proven inert on every existing build):
- **The category-sort opener** (`InteractiveBuilder.#dragAndDrop`; data `interactive_builders.dragAndDrop.standard_decline_opener`; env `DDSORTOPENER_OFF`): the r69 pair reading declines when the bundle's red tag says the items go INTO coloured squares / zones / categories / groups / columns — HPFUN101 1A's 2×2 zone table (Blue / Green / Yellow / Red, the statements typed after it) had built two nonsense pairs; it keeps the correctly-labelled dragAndDrop hand-off box. The whole dragAndDrop family (360 modules) with `IQFREEWIDGET_OFF=1`: 0 pages changed.
- **The all-red answers column** (`InteractiveBuilder.#ddTable` form (b); data `interactive_builders.dropDown.column_answer_fold`; env `DDCOLFOLD_OFF`): when the first row's red answer recurs below, it is a question, not the column head, and the options are distinct ignoring case — MXDI202 10A had dropped row 1 and offered `Length / Weight / length` (the verifier's duplicate-option defect on all 7 units) → 8 units, defect 0. Inert with `IQFREEWIDGET_OFF=1` on r510's 43 modules (0 files differ) and on the whole dropDown family.

### 2. PROOF

- In-memory probe over all 545 modules: OFF 0 pages changed (242 comparable files of the 43 modules = the shipped manifest's md5s); ON **43 modules** (`outputs/_affected_r510.txt`). Regenerated with `_s49_regen_par.sh`; `scoped_ship.sh … --round 510` PASS ×3 (the 43; HIS1004 after the deny pattern; MXDI202 after the fold): 0 stale, containment exact, the 12-module spot-check byte-identical each time.
- **On the 43 modules** (disk vs the OFF probe): hand-offs labelled 'unclassified' **355 → 181**, the writer's widget named instead (dragAndDrop 9 → 96, flipCard 9 → 31, dropDown 6 → 25, multiChoiceQuiz 40 → 62, memoryGame 0 → 15, radioQuiz 5 → 15, carousel 28 → 39, crossword 0 → 6 …); built **dragAndDrop 2 → 12** (verifier: 12 widgets / 76 drags, defect 0; `_s50_r510_dndcheck.cjs`: 57 new drags on 10 pages, 52 = 91 % found in the gold's own text), **dropQuiz 0 → 2** (13 units, defect 0), **flipCard roots 35 → 112** (verifier over the 43: card texts 69 → 216, exact 35 → 137, copy-edit 6 → 24, divergence 0; the 27 new unmatched cards are recorded — TWHA906's red `Facing:` / `Reverse:` face labels and a red first letter split from its word inside the card-table cells), multiChoiceQuiz 13 questions exact.

### 3. PROTECTED GATES

- **Skeleton 55.5883 → {MEAN} % @ 2486 (+0.1109pp)** — 76 up / 16 down (+275.6pp-sum, `outputs/_r510_movers.py`); **≥50 1602 → 1609** (11 up-crossings; 2 down: HPFUN401_0_0 50.2 → 47.0, TWHA906_0_0 51.4 → 37.3); **≥75 277 → 280**; ≥90 26; **RAW 39.516 → {RAW} %**. **The down movers, NAMED:** TWHA906_0_0 −14.1 is the A1 case — its twenty writer widgets are named where OFF said 'unclassified', and their content now sits in the hand-off boxes the skeleton collapses to one line (OFF's 8 unnumbered plain boxes → 2); restoring an unnumbered box around such a widget was probed and measured WORSE (the six worst modules' pp-sum 1367.8 → 1346.0) and withdrawn. The others are ≤ 6.4pp (MXFL204_3_0, MXFU202_9_0, MXFL201_8_0, HPFUN101_0_0, HPFUN401_0_0, TRR109 ×3 …), each a named widget's capture.
- **compare_structure exact 16762 → 16768 (+6)**, EXTRA 204, missing 887 (net 0: HIS1004 +1 then −1).
- **body_compare ANY 230 → 233 (+3), NAMED** (`outputs/_s50_bcsplit.py`, `_s50_bcpages.py`): HPFUN403_0_0 — the writer's drawing-tool (sketcher) box whose only member is its example image's filename (28 chars, under the 40-char 'empty' line); MXFL204_1_0 — the writer's wordFind box, empty because the words are "listed above"; ANZH304_2_0 over-capture — the drag-and-drop's six text sections typed as `[Body]` after the tag ("Each section of text has a corresponding visual"), the gold also holds them inside a widget (flip cards), free blocks 12 → 12; MXFL204_2_0 over-capture — Activity 2A's two hand-off boxes became one of exactly their combined size (2775 + 1406 = 4181 chars), free blocks 0 → 1. MXFU202_8_0 cleared. (Before the lead-word limit the ANY delta was +9: ANZH301 / 302's empty sketcher boxes, HIS1003's two, HIS1004_5_0 — fixed, not named.)
- Clean 98.40 %, leak 52 / 42, tags 9557 / 9557 EXACT; every verifier ✓, every COUNT held (`_r510_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 510 --accept-named`; `--gate-baseline-check` PASS. Plateau: **reset** (a real gain).

**Ledger:** scoped #5 since the r505 FULL · data `Tag_Lexicon.json _meta.interactive_qualifier_free_widget` (+ `max_lead_words`, `free_deny_pattern`), `Emit_Templates.json interactive_builders.dragAndDrop.standard_decline_opener`, `interactive_builders.dropDown.column_answer_fold` · env `IQFREEWIDGET_OFF`, `DDSORTOPENER_OFF`, `DDCOLFOLD_OFF` · code `TagNormaliser.Parse`, `InteractiveBuilder.#dragAndDrop`, `#ddTable` · tools `_s49_r11_unknownquiz.cjs`, `_s50_r510_spans.cjs`, `_s50_probe_par.sh`, `_s50_bcsplit.py`, `_s50_bcpages.py`, `_s50_skoffon.py`, `_s50_sk3.py`, `_r510_movers.py`, `_r510_finalise.py` · built session 49 Round 11 (toggled OFF at its stop), finished session 50 Round 1.
"""
F.finalise(
    N=510, old_build="260620.72", new_build="260620.73", entry=entry,
    config_comment="THE WIDGET NAMED AFTER A GENERIC INTERACTIVE BRACKET (session 50 Round 1): `[interactive activity] drag and drop` "
                   "names the writer's widget; + the dragAndDrop category-sort opener guard and the dropDown all-red answers column. "
                   "Env IQFREEWIDGET_OFF / DDSORTOPENER_OFF / DDCOLFOLD_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 510 BASELINE (the widget named after a generic interactive "
        f"bracket, `IQFREEWIDGET_OFF`; SCOPED, scoped #5 since the r505 FULL): SCAFFOLD mean {MEAN}% / >=50% 1609 / >=75% 280 / >=90% 26 / "
        f"RAW {RAW}% @ 2486 pairs (+0.1109pp, 76 up / 16 down NAMED); cs exact 16768 (+6); body ANY 233 (+3 NAMED).**",
    og11="| `IQFREEWIDGET_OFF` / `DDSORTOPENER_OFF` / `DDCOLFOLD_OFF` | 510 | **THE WIDGET NAMED AFTER A GENERIC INTERACTIVE BRACKET** "
         "(session 50 Round 1). `IQFREEWIDGET_OFF` reverts `Tag_Lexicon _meta.interactive_qualifier_free_widget` (the span is a plain "
         "activity box again; byte-identical to r509). `DDSORTOPENER_OFF` reverts `dragAndDrop.standard_decline_opener` (inert unless "
         "r510 is on: HPFUN101 1A builds its zone table as pairs again). `DDCOLFOLD_OFF` reverts `dropDown.column_answer_fold` (MXDI202 "
         "10A: row 1 dropped, the duplicate `length` option back). |",
    og14=f"- **Build:** `260620.73` (round 510 — **the widget named after a generic interactive bracket**; `IQFREEWIDGET_OFF`; scoped #5 "
         f"since the r505 FULL; 43 modules; skeleton {MEAN} % (+0.1109pp), ≥50 1609, ≥75 280; cs exact 16768; body ANY 233 NAMED).",
    gb_note=f"Round 510 (session 50 Round 1, 2026-09-26) — THE WIDGET NAMED AFTER A GENERIC INTERACTIVE BRACKET (IQFREEWIDGET_OFF; guards "
            f"DDSORTOPENER_OFF, DDCOLFOLD_OFF): 43 modules; SCAFFOLD 55.5883 -> {MEAN} @ 2486 (+0.1109pp, 76 up / 16 down NAMED), >=50 "
            f"1602 -> 1609, >=75 277 -> 280, RAW 39.516 -> {RAW}; cs exact 16762 -> 16768; body ANY 230 -> 233 NAMED (HPFUN403_0_0 / "
            f"MXFL204_1_0 empty-by-design boxes, ANZH304_2_0 / MXFL204_2_0 capture artefacts); clean / leak EXACT; scoped #5.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 1 — r510 (the widget named after a generic interactive bracket) "
             "SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r510** (260620.73); **LAST FULL = r505 (the session-49 "
             "Round 6 backstop)**; ledger **scoped #5** (3 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every "
             "PICK): `outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 "
             "pages / 9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page). Checked at r510: none lies wholly inside its 43 "
             "modules (r469 / r469b each reach modules outside it), so none rode along.",
    last_shipped=f"- LAST SHIPPED: **r510** (build 260620.73, 26 Sept {T}, session 50 Round 1 — THE WIDGET NAMED AFTER A GENERIC "
                 "INTERACTIVE BRACKET, `IQFREEWIDGET_OFF` + guards `DDSORTOPENER_OFF` / `DDCOLFOLD_OFF`; SCOPED, **scoped #5 since the "
                 f"r505 FULL**; 43 modules; 'unclassified' hand-offs 355 → 181; dragAndDrop built 2 → 12, flipCard roots 35 → 112; "
                 f"**skeleton 55.5883 → {MEAN} % @ 2486 (+0.1109pp)**, 76 up / 16 down NAMED, **≥50 1609 (+7)**, **≥75 280 (+3)**; "
                 "cs exact +6; body ANY +3 NAMED).",
    before_them_add="the nested bracket",
    plateau="- Plateau window (§4): **0 of 3** — r510 +0.1109pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.73** (r510 the widget named after a generic interactive bracket — session 50 Round 1, "
             "26 Sept); before it 260620.72 (",
    roundlog=f"- s50-r1 (engine r510, build 260620.73, 25 Sept 23:12 → 26 Sept {T}) · FINISHED THE WIDGET NAMED AFTER A GENERIC "
             "INTERACTIVE BRACKET (KB c14) + the HPFUN101 category-sort guard, a 4-word lead limit, the text-to-speech deny, the "
             "dropDown all-red column fold · SHIPPED scoped #5 · 43 modules · skeleton **+0.1109pp**, ≥50 +7, ≥75 +3, cs exact +6, "
             "body ANY +3 NAMED · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r510, 260620.73):** `Tag_Lexicon _meta.interactive_qualifier_free_widget` (+ max_lead_words 4, "
                  "free_deny_pattern), `dragAndDrop.standard_decline_opener`, `dropDown.column_answer_fold`; `TagNormaliser.Parse`, "
                  "`InteractiveBuilder.#dragAndDrop` / `#ddTable`. Probe OFF 0; ON 43 modules; skeleton +0.1109pp; body ANY +3 NAMED.",
)
