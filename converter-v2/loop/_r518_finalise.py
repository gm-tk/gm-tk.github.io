#!/usr/bin/env python3
"""ROUND 518 finalise (session 50 Round 10 — the typing verifier learns the table form + the three guards it called for,
TYPTABLEGUARD_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 518, build 260620.79) — THE TYPING VERIFIER LEARNS THE TABLE FORM, and the three defects its new checks found in r517's builds are guarded (GEWHA / PWY1001 / PWY1002 layout tables, MXFU202's `[image]` cells): 4 modules decline to the hand-off box; the typing count test now covers the table quizzes (14 quizzes / 145 inputs on the gate set, 140 the gold's own); gate-neutral

### 1. WHAT CHANGED

**The tool** (`reference/tests/_verify_typing.cjs`; LOOP §3 step 6 — every widget round is judged on its verifier, and a verifier that cannot see a form passes it vacuously): r517's table form (`div.typing layout="standard"` > table) was invisible to the verifier, which parsed only the typingContainer form. `parseTable` / `defectsTable` now read it — the layout, every input's form-control / type / placeholder / caseSensitive, a non-empty and un-bracketed answer, the reset / checkAnswer / showAnswer row, no writer bracket left in the table — its quizzes and inputs count in the same totals, and the selftest gains a MXFUN01 table fixture (LIVENESS 3 quizzes / 61 inputs; DETECTION: an emptied answer, a bracketed answer, the layout removed — all caught).

**What it found on its first run over r517's 17 modules — DEFECTS 10, fixed** (`InteractiveBuilder.#typingTable`; data `interactive_builders.typing.table_form.tag_answer_pattern`; env **`TYPTABLEGUARD_OFF`** = the r517 output exactly): GEWHA, PWY1001 and PWY1002 hold LAYOUT tables whose red cells are TAGS (`[MTK Quiz Questionnaire] [engagement trigger]`, `Body`, `Table`, `Typing self check`, `[Tickbox [autocheck]]`, `select option Y/N`), not answers; MXFU202_5_0's table kept `[image] 117 - 71.jpg` cells. A red run still bracketed after the single-bracket unwrap, or a tag word, now declines the table, and so does a built table that would still show a writer bracket — those four tables go back to the hand-off box.

### 2. PROOF

- In-memory probe over all 545 modules: `TYPTABLEGUARD_OFF=1` → 0 pages changed; ON → **4 modules** (GEWHA, MXFU202, PWY1001, PWY1002). `scoped_ship.sh … --round 518` PASS (0 stale, containment 4 ⊆ 4, the 12-module spot-check byte-identical).
- `_verify_typing.cjs` over r517's 17 modules: **27 quizzes / 309 inputs, DEFECTS 0**; 253 answers (82 %) the gold's own, 48 no gold match, 8 in a module whose gold has no typing. On the gate's recorded 7-module set the count GREW 8 → 14 quizzes, 57 → 145 inputs (MXEO301 1 → 5, MXFL302 1 → 3 — the table form counted), recorded with `VERIFY_COUNT_RECORD=1`; 140 of the 145 the gold's own answers.

### 3. PROTECTED GATES

Gate-neutral: skeleton {MEAN} % @ 2486 EXACT, RAW {RAW} %, cs / body / clean / leak EXACT; tags 9557; every verifier ✓, every COUNT held or recorded (`_r518_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 518`; `--gate-baseline-check` PASS. Plateau: neither (a measurement-tool round + a guard).

**Ledger:** scoped #4 since the r513 FULL · tool `_verify_typing.cjs` (parseTable / defectsTable / the MXFUN01 selftest fixture) · data `interactive_builders.typing.table_form.tag_answer_pattern` · env `TYPTABLEGUARD_OFF` · code `InteractiveBuilder.#typingTable` · `gate_baseline.json.typing` counts 14 / 145 · session 50 Round 10.
"""
F.finalise(
    N=518, old_build="260620.78", new_build="260620.79", entry=entry,
    config_comment="THE TYPING VERIFIER LEARNS THE TABLE FORM + the guards it called for (session 50 Round 10): a tag-word or "
                   "still-bracketed red answer, or a leftover writer bracket, declines the table. Env TYPTABLEGUARD_OFF.",
    og9=None,
    og11="| `TYPTABLEGUARD_OFF` | 518 | **THE TYPING TABLE FORM'S GUARDS** (session 50 Round 10, found by `_verify_typing.cjs`'s new table "
         "checks). Reverts `typing.table_form.tag_answer_pattern` + the bracket checks: GEWHA / PWY1001 / PWY1002's layout tables and "
         "MXFU202's `[image]` table build again (r517's output exactly). |",
    og14=f"- **Build:** `260620.79` (round 518 — **the typing verifier learns the table form + its guards**; `TYPTABLEGUARD_OFF`; scoped #4 "
         f"since the r513 FULL; 4 modules decline; typing count 14 / 145 recorded; gate-neutral).",
    gb_note=f"Round 518 (session 50 Round 10, 2026-09-26) — _verify_typing.cjs LEARNS THE TABLE FORM; its first run found 10 defects in "
            f"r517's builds (layout tables with tag words, [image] cells) -> guarded (TYPTABLEGUARD_OFF), 4 modules back to the hand-off box; "
            f"typing counts 8 / 57 -> 14 / 145 recorded (the table quizzes counted); gate-neutral; scoped #4.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 10 — r518 (the typing verifier's table form + its guards) "
             "SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r518** (260620.79); **LAST FULL = r513 (the "
             "session-50 Round 5 backstop)**; ledger **scoped #4** (4 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at "
             "every PICK): `outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 "
             "pages / 9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: "
             "Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix). Checked at r518: none rides.",
    last_shipped=f"- LAST SHIPPED: **r518** (build 260620.79, 26 Sept {T}, session 50 Round 10 — THE TYPING VERIFIER LEARNS THE TABLE FORM "
                 "+ the guards it called for, `TYPTABLEGUARD_OFF`; SCOPED, **scoped #4 since the r513 FULL**; 4 modules back to the "
                 f"hand-off box; typing count 14 / 145 recorded; gate-neutral: skeleton {MEAN} % EXACT).",
    before_them_add="KB c64 the animated-character Vimeo scaffold",
    plateau="- Plateau window (§4): **0 of 3** — r518 a measurement-tool round + guard, gate-neutral (neither); ",
    standing="- Standing facts: AppVersion **260620.79** (r518 the typing verifier's table form + guards — session 50 Round 10, 26 Sept); "
             "before it 260620.78 (",
    roundlog=f"- s50-r10 (engine r518, build 260620.79, 26 Sept ≈04:05 → {T}) · a PICK pass (radioQuiz: marks on ≈ 30 of 101, declined "
             "at s40-r6, not reopened) then THE TYPING VERIFIER LEARNS THE TABLE FORM — its first run found 10 defects in r517's builds "
             "(layout tables, `[image]` cells), guarded · SHIPPED scoped #4 · 4 modules back to the hand-off box, typing count 14 / 145 "
             "recorded · gate-neutral · plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r518, 260620.79):** `_verify_typing.cjs` parseTable / defectsTable / MXFUN01 fixture; "
                  "`typing.table_form.tag_answer_pattern` + bracket guards (TYPTABLEGUARD_OFF). Probe OFF 0; ON 4 modules; gate-neutral.",
)
