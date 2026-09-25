#!/usr/bin/env python3
"""ROUND 511 finalise (session 50 Round 2 — D15-19 THE YELLOW-✅ DROPDOWN QUIZ, DDYELLOW_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 511, build 260620.74) — D15-19 THE YELLOW-✅ DROPDOWN QUIZ: the writer's yellow highlight builds a dropDown unannounced, under Chris's strict checks (the dropDown kickoff after r507's multiChoiceQuiz) + the mark placed after the previous one (MXDB302 8A: 7 questions, 6 = the gold's, the 7th the writer's correct answer where the gold slipped)

### 1. WHAT CHANGED

**Chris's D15-19** (25 Sept 2026, Option B — *"Trust yellow ✅ ticks, with strict checks"*; one widget type per kickoff, multiChoiceQuiz first (r507), then dropDown): a quiz may be built from the writer's YELLOW highlight without an announcement ONLY where (a) exactly one OPTION per question carries a ✅, (b) the bundle is not the writer's D2L quiz under a `[Button] … quiz`, (c) the writer never says "no correct answers". GREEN is never trusted; an answer is never invented.

**The fix** (`InteractiveBuilder.#ddMarkKinds`; data `interactive_builders.dropDown.yellow_ticks`; env `DDYELLOW_OFF`): the r309 colour-mark path (announced marks only) now also opens, unannounced, for YELLOW highlight marks alone (`#ddBlockMarks` / `#ddCellMarkTexts` filter `hl` marks by colour), when a yellow mark exists in the bundle, the item above the opener is not a D2L-quiz button (`d2l_button_pattern`) and nothing in the bundle says there are no correct answers (`no_answers_pattern`: "no correct / right / wrong answers", "answers will vary"). Guard (a) is every mark reading's own rule — `#ddMarkAnswer` returns 0 on zero or two-plus hit options and the bundle declines. A bundle without a yellow mark is byte-identical.

**Found by the kickoff's verifier check and fixed with it** (`#ddRebuild`; data `colour_marks.sequential_ranges`; env `DDMARKSEQ_OFF`): a colour mark was placed at the FIRST occurrence of its text in the paragraph, so MXDB302 8A Q5 `(0, 1, ✅2, 3) decimal places so there need to be (0, 1, ✅2, 3)` put both marks on the first group and the second group shipped as prose (6 units for the gold's 7). The marks arrive in document order, so each is now placed after the previous one (the first occurrence when none follows). Proven inert on every existing build (the corpus-wide probe with `DDYELLOW_OFF=1`: 0 pages changed).

### 2. THE POPULATION (`outputs/_s50_r511_ddyellow.cjs`, every dropDown bundle in the corpus, in memory)

623 dropDown bundles; **27 carry a yellow mark** (≈ 24 modules): 3 were already built (announced — ENGJ301 6A, SCCH301 ×2), **r511 builds 1 more — MXDB302 8A** (the D1 paragraph form); the other 23 are shapes no reading handles yet, recorded (each below the 20-site shape floor): the TABLE forms ≈ 12 (ENFUN03 / 08, ENGC201, ENGI303, ENGI401, ENGR302 3C, ENGS202, FRFUN07 / 08, MXFU202, OSAH501, OSAI501 — each a different table layout), numbered / lettered option LINES 3 (ENFUN02, ENGR302 5B's parens split across lines, ENGS301), a highlighted word with NO option list 3 (HES1002 ×2, CEDR401 — never invented), and single stray marks (CHFUN05, CHI1004's upload-box guide); SCCH301 #27 and SCES201 ×2 are ANNOUNCED yet unbuilt (their shapes, not D15-19's).

### 3. PROOF AND GATES

- In-memory probe over all 545 modules: `DDYELLOW_OFF=1` → 0 pages changed; ON → **MXDB302 only** (1 page + its worklist). `scoped_ship.sh … --round 511` PASS (0 stale, containment 1 ⊆ 1, the 12-module spot-check byte-identical).
- **`_verify_dropdown.cjs`** (every module): groups 332 → 333, units 218 → 225, **exact 150 → 156**, copy-edit 1 → 2, defect 0. The new copy-edit is NAMED — MXDB302 8A Q3 `The equation becomes (3.7 × 6.3, ✅37 × 63, 37 × 6.3, 3.7 × 63)`: the build follows the writer's tick (3.7 × 6.3 with the decimal points removed IS 37 × 63); the gold answers `37 × 6.3` — a human slip.
- **Gate-neutral by design** (a widget build — the skeleton collapses a widget to one line): skeleton {MEAN} % @ 2486 EXACT, ≥50 1609, ≥75 280, ≥90 26, RAW {RAW} %; cs / body / clean / leak EXACT; tags 9557; every verifier ✓, every COUNT held (`_r511_gates.log`); `--gate-baseline-check` PASS. Plateau: neither (a widget build, skeleton-blind).

**Ledger:** scoped #6 since the r505 FULL · data `interactive_builders.dropDown.yellow_ticks`, `dropDown.colour_marks.sequential_ranges` · env `DDYELLOW_OFF`, `DDMARKSEQ_OFF` · code `InteractiveBuilder.#ddMarkKinds` / `#ddBlockMarks` / `#ddCellMarkTexts` / `#ddRebuild` · tools `_s50_r511_ddyellow.cjs`, `_r511_finalise.py` · session 50 Round 2. **Next D15-19 kickoff:** none left by type (multiChoiceQuiz r507, dropDown r511); the residue is the per-shape list above.
"""
F.finalise(
    N=511, old_build="260620.73", new_build="260620.74", entry=entry,
    config_comment="D15-19 THE YELLOW-✅ DROPDOWN QUIZ (session 50 Round 2): the writer's yellow highlight builds a dropDown unannounced "
                   "under the three checks; colour marks placed in document order. Env DDYELLOW_OFF / DDMARKSEQ_OFF.",
    og9=None,
    og11="| `DDYELLOW_OFF` / `DDMARKSEQ_OFF` | 511 | **D15-19 THE YELLOW-✅ DROPDOWN QUIZ** (session 50 Round 2). `DDYELLOW_OFF` reverts "
         "`dropDown.yellow_ticks` (an unannounced yellow highlight is ignored again; byte-identical to r510). `DDMARKSEQ_OFF` reverts "
         "`dropDown.colour_marks.sequential_ranges` (each colour mark at its text's first occurrence; inert unless a paragraph repeats "
         "a marked text — MXDB302 8A Q5). |",
    og14=f"- **Build:** `260620.74` (round 511 — **D15-19 the yellow-✅ dropDown quiz**; `DDYELLOW_OFF`; scoped #6 since the r505 FULL; "
         f"MXDB302 8A built (7 units, 6 exact, 1 the writer's correct answer where the gold slipped); dropDown exact 150 → 156; gate-neutral).",
    gb_note=f"Round 511 (session 50 Round 2, 2026-09-26) — D15-19 THE YELLOW DROPDOWN QUIZ (DDYELLOW_OFF; DDMARKSEQ_OFF): MXDB302 8A "
            f"built from the writer's unannounced yellow ticks (7 units; dropDown verifier corpus-wide exact 150 -> 156, copy-edit 1 -> 2 "
            f"NAMED: the gold's own slip on Q3); gate-neutral (skeleton {MEAN} EXACT); scoped #6.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 2 — r511 (D15-19 the yellow-✅ dropDown quiz) SHIPPED "
             "and committed; the in-flight marker is cleared). LAST SHIPPED **r511** (260620.74); **LAST FULL = r505 (the session-49 "
             "Round 6 backstop)**; ledger **scoped #6** (2 of headroom — a FULL backstop is due after two more scoped ships). Ride-along "
             "patches (LOOP §3 step 1 reads this list at every PICK): `outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, "
             "ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, "
             "SSOG105, TWHA906, XGF9004) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page). Checked at r511 (MXDB302 only): none rides.",
    last_shipped=f"- LAST SHIPPED: **r511** (build 260620.74, 26 Sept {T}, session 50 Round 2 — D15-19 THE YELLOW-✅ DROPDOWN QUIZ, "
                 "`DDYELLOW_OFF` + `DDMARKSEQ_OFF`; SCOPED, **scoped #6 since the r505 FULL**; MXDB302 8A built (7 units: 6 = the gold, "
                 f"1 the writer's correct tick where the gold slipped); dropDown exact 150 → 156, defect 0; gate-neutral: skeleton {MEAN} % "
                 "EXACT).",
    before_them_add="KB 10 §5 the empty lesson menu's red flag",
    plateau="- Plateau window (§4): **0 of 3** — r511 a widget build, skeleton-blind (neither); ",
    standing="- Standing facts: AppVersion **260620.74** (r511 D15-19 the yellow-✅ dropDown quiz — session 50 Round 2, 26 Sept); "
             "before it 260620.73 (",
    roundlog=f"- s50-r2 (engine r511, build 260620.74, 26 Sept 00:24 → {T}; ≈ 30 min lost to a `pgrep -f` self-match hang) · D15-19 THE "
             "YELLOW-✅ DROPDOWN QUIZ (+ the colour mark placed after the previous one) · SHIPPED scoped #6 · 27 yellow-marked dropDown "
             "bundles: 1 newly built (MXDB302 8A, 7 units), 23 recorded by shape · dropDown exact 150 → 156, defect 0 · gate-neutral · "
             "plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r511, 260620.74):** `dropDown.yellow_ticks` (DDYELLOW_OFF), `dropDown.colour_marks.sequential_ranges` "
                  "(DDMARKSEQ_OFF); `#ddMarkKinds` / `#ddBlockMarks` / `#ddCellMarkTexts` / `#ddRebuild`. Probe OFF 0; ON MXDB302 only; "
                  "gate-neutral.",
)
