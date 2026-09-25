#!/usr/bin/env python3
"""ROUND 517 finalise (session 50 Round 9 — THE TYPING QUIZ'S TABLE FORM, TYPTABLE_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 517, build 260620.78) — THE TYPING QUIZ'S TABLE FORM: a `[Type and check]` / `[typing quiz]` table whose answers the writer typed in RED builds the gold's `div.typing layout="standard"` table with an input per red answer (32 quizzes / 324 inputs / 17 modules; 70 % of the answers are the gold's own, 0 malformed; gate-neutral)

### 1. WHAT CHANGED

**The lane** (Chris's D10-3 build lane; **D13-4**: typing is built ONLY where the writer marked the answer — r449 shipped shape 1, the red answer on the question line). The dashboard's first-ranked blocker for the type: `(a captured TABLE)` — 98 declines, 0 builds. `_s50_r9_typtable.cjs`: 113 typing / selfCheck bundles hold ONE table with red cells (65 without media, 68 modules), the writer saying "Answers are in red" / "Correct answers are in red"; the gold's form (MXFUN01's nine `[Type and check]` tables): `div.typing layout="standard"` > `div.table-responsive` > the writer's table, each red run an `<input class="form-control" … answer="…">`, black text kept, the red "Question | Answer" label row dropped.

**The fix** (`InteractiveBuilder.#typingTable`, tried after the r449 reading in the typing case and before the r69 reading in the selfCheck case; data `interactive_builders.typing.table_form`; env `TYPTABLE_OFF`): every red run in a cell → an input (answer = the run; a bracketed `[cannot]` means the word — BLL252; "23.30 or 23.3" → the KB 03D `answer="23.30||23.3"` form); a first row of bold labels (a red column title in it included — MXFU202) → the header row; a red label row → dropped. A selfCheck-typed bundle is read only when the writer's own opener says type / typing (the alias word "check" folds `[Type and check]` to selfCheck). **Declines to the hand-off box:** media anywhere; the writer's words asking for another widget, images, words outside the table, highlighting or colour (deny_pattern); an all-red body row (letter tiles); a red LABEL instead of an answer — `correct` beside the black answer (BLLR203), `(Question 1)` (SSCI205) — found by the first probe's answer check and made a decline (label_answer_pattern); an answer over max_answer_words; fewer than min_answers.

### 2. PROOF

- In-memory probe over all 545 modules: `TYPTABLE_OFF=1` → the 17 modules' 124 comparable files equal the manifest (0 differ), nothing else changes; ON → **17 modules** (BLL152 / 156 / 252, CEDK501, ENGI303, GEWHA, MXDI201 / 202, MXEO301, MXEX302, MXFL302, MXFU202 / 402, MXFUN01 / 03, PWY1001 / 1002). `scoped_ship.sh … --round 517` PASS (0 stale, containment 17 ⊆ 17, the 12-module spot-check byte-identical).
- **The answers** (`outputs/_s50_r517_answers.cjs` — the table form's check; `_verify_typing.cjs` reads the typingContainer form only): **32 table quizzes / 324 inputs, 0 malformed; 226 (70 %) equal a gold typing answer** (80 % in the modules whose gold has typing at all — MXFUN01 61 / 61, MXEO301 63 / 67, MXFL302 19 / 21, BLL156 14 / 14 …); 35 inputs sit in modules whose gold has no typing input (CEDK501, GEWHA, PWY1001 / 1002 — the developer's substitution, A1).

### 3. PROTECTED GATES

- **Gate-neutral by design** (a widget build — the skeleton collapses a widget to one line): skeleton {MEAN} % @ 2486 EXACT, ≥50 1612, ≥75 285, ≥90 26; **RAW 39.555 → {RAW} %** (the widget internals now carry real structure); cs / clean / leak EXACT; **body_compare ANY 236 → 235** (CEDK501_6_0's over-capture cleared); tags 9557; every verifier ✓, every COUNT held (`_r517_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 517`; `--gate-baseline-check` PASS. Plateau: neither (a widget build).

**Ledger:** scoped #3 since the r513 FULL · data `interactive_builders.typing.table_form` · env `TYPTABLE_OFF` · code `InteractiveBuilder.#typingTable` + the typing / selfCheck dispatch · tools `_s50_r9_typtable.cjs`, `_s50_r517_answers.cjs`, `_r517_finalise.py` · session 50 Round 9. **Recorded:** `_verify_typing.cjs` should learn the table form (its count test would then cover these 32 quizzes); the remaining red-table bundles are the declines above (≈ 80 — mostly drag-and-drop / tile / image requests the writer made in words).
"""
F.finalise(
    N=517, old_build="260620.77", new_build="260620.78", entry=entry,
    config_comment="THE TYPING QUIZ'S TABLE FORM (session 50 Round 9): a table whose answers the writer typed in red builds the gold's "
                   "div.typing layout=standard table with an input per answer. Env TYPTABLE_OFF.",
    og9=None,
    og11="| `TYPTABLE_OFF` | 517 | **THE TYPING QUIZ'S TABLE FORM** (session 50 Round 9). Reverts `interactive_builders.typing.table_form`: a "
         "typing / `[Type and check]` table with red answers is a hand-off box again; byte-identical to r515. |",
    og14=f"- **Build:** `260620.78` (round 517 — **the typing quiz's table form**; `TYPTABLE_OFF`; scoped #3 since the r513 FULL; 17 "
         f"modules, 32 quizzes / 324 inputs, 70 % gold answers; gate-neutral, RAW {RAW} %).",
    gb_note=f"Round 517 (session 50 Round 9, 2026-09-26) — THE TYPING TABLE FORM (TYPTABLE_OFF): 17 modules, 32 table quizzes / 324 inputs "
            f"(226 = a gold typing answer, 0 malformed); gate-neutral (skeleton {MEAN} EXACT), RAW 39.555 -> {RAW}, body ANY 236 -> 235; "
            f"scoped #3.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 9 — r517 (the typing quiz's table form) SHIPPED and committed; "
             "the in-flight marker is cleared). LAST SHIPPED **r517** (260620.78); **LAST FULL = r513 (the session-50 Round 5 backstop)**; "
             "ledger **scoped #3** (5 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 "
             "modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r468_declined.patch` (the "
             "lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / `_r489_accbullet_declined.patch` (the accordion bulleted "
             "bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR "
             "table-dialect ownership fix). Checked at r517 (17 modules): none lies wholly inside.",
    last_shipped=f"- LAST SHIPPED: **r517** (build 260620.78, 26 Sept {T}, session 50 Round 9 — THE TYPING QUIZ'S TABLE FORM, `TYPTABLE_OFF`; "
                 "SCOPED, **scoped #3 since the r513 FULL**; 17 modules, 32 quizzes / 324 inputs, 226 = the gold's answers (70 %), 0 "
                 f"malformed; gate-neutral: skeleton {MEAN} % EXACT, RAW {RAW} %, body ANY −1).",
    before_them_add="the writers' missing spellings",
    plateau="- Plateau window (§4): **0 of 3** — r517 a widget build, skeleton-blind (neither); ",
    standing="- Standing facts: AppVersion **260620.78** (r517 the typing quiz's table form — session 50 Round 9, 26 Sept); before it "
             "260620.77 (",
    roundlog=f"- s50-r9 (engine r517, build 260620.78, 26 Sept 03:30 → {T}) · a PICK pass (the worst pages: three menu-swallow outliers, "
             "JPFUN02's developer phases) then THE TYPING QUIZ'S TABLE FORM (red answers in a table → the gold's typing table; the first "
             "probe's bracketed answers and red labels fixed) · SHIPPED scoped #3 · 17 modules, 32 quizzes / 324 inputs, 70 % gold answers · "
             "gate-neutral, body ANY −1 · plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r517, 260620.78):** `interactive_builders.typing.table_form` (TYPTABLE_OFF); "
                  "`InteractiveBuilder.#typingTable`. Probe OFF = manifest; ON 17 modules; gate-neutral.",
)
