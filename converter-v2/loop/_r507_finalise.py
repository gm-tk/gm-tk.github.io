#!/usr/bin/env python3
"""ROUND 507 finalise (session 49 Round 8 — D15-19 the yellow-✅ multiChoiceQuiz build, MCQYELLOW_OFF). WSL. argv: MEAN RAW."""
import sys
import _s49_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-25 (round 507, build 260620.70) — D15-19 THE YELLOW-✅ MULTIPLE-CHOICE QUIZ: the writer's yellow highlight builds the quiz without an announcement, under the three strict checks (4 quizzes / 19 questions on 4 modules — 17 carry exactly the gold's answer; TEFUN04's D2L quizzes and ARFUN04's answer-key form declined)

### 1. WHAT CHANGED

**The decision** (Chris, 25 Sept 2026, D15-19 — "19. Unannounced quiz answers: Option B (Trust yellow ✅ ticks, with strict checks) — as recommended"): widening D13-4 — a quiz may be built from the writer's YELLOW highlight (the parser's ✅) without an announcement, only where (a) exactly one OPTION per question is ticked (options counted, never highlighted runs), (b) the bundle is not the writer's D2L quiz, (c) the writer never says "no correct answers"; green is not trusted; one type per kickoff — multiChoiceQuiz first; judged on the widget's verifier against the gold's own answers.

**Triangulated** (the D15 report): CEDW501 5B "The bubble" — WT `a. ✅A group of people you live with during lockdown.` (no announcement) → gold `CEDW501_5.0.html` `mcqOption value="correct"` on exactly that option → PageForge a hand-off box `⚙ INTERACTIVE (un-built) #34: multiChoiceQuiz`.

**The fix** (`InteractiveBuilder.#multiChoiceQuiz`; data `interactive_builders.multiChoiceQuiz.yellow_ticks`; env `MCQYELLOW_OFF`; `InteractiveScanner` records `bundle.prevItemText`, the item just above the opener): the r309 `block.marks` side-channel's YELLOW highlights are put back into the member text with `Utils.MarkAnswers` (the r448 carry-through's own helper) and a ticked OPTION becomes `value="correct"` — only in a bundle with no `[correct]` / `[incorrect]` mark of the writer's own (those keep the r305 reading) and only when: (a) every question has exactly one ticked option; (b) the item above the opener is not a writer `[Button]` naming a quiz (`d2l_button_pattern` — `[Button] Go to quiz` TEFUN01 / 03, ENGR202 and `[Button] Quiz` TEFUN04, whose gold builds 0 multiChoiceQuiz: first tried with "go to quiz" only, TEFUN04 built 4 quizzes and was caught); (c) no "no correct answers" (`no_answers_pattern` — OSAI101). A highlighted ANSWER-KEY line (`✅Correct Answer: B` — ARFUN04, whose options are lettered b–e while its gold reads B as the 2nd option) is never an option or a tick: set aside, the question has no ticked option and guard (a) declines (first tried without it: ARFUN04 built a fifth option "Correct answer: b" as the answer — caught by the answer check).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **8 files / 4 modules** — CEDO502_3_0, CEDR501_4_0, CEDW501_5_0, MXEX302_1_0 (+ their interactives lists): **4 multiChoiceQuiz groups / 19 questions built, 4 hand-off boxes gone** (the pages' multiChoiceQuiz boxes 6 → 2). Regenerated = ON byte-for-byte; `scoped_ship.sh` PASS.
- **Against the gold's own answers** (`_r507_answers.cjs`, every new question paired with the module's gold quizzes — `<p>` and `<li>` question forms): **17 / 19 = the gold's correct option**; 1 "differs" is a pairing artefact (the gold REPLACED the writer's "Which sport uses the term home run?" and the checker paired it with "slam dunk" → basketball; the built answer, Baseball, is the writer's), 1 the gold dropped (CEDR501 "What do both interviews have in common"). `_verify_mcq.cjs` on the 4: **defect 0 ✓**, SELFTEST GREEN (its own gold pairing reads only `<p class="mcqQuestionText">`, so it reports 16 "no gold" — a verifier follow-up).
- The rest of the D15 report's ≈ 63: the D2L bundles (guard b), ARFUN04 (the key form), the other line bundles the r305 guards decline, and the 40 yellow TABLE bundles (the builder reads no table; many shapes — ENGR102 11 two-column, CEDO501 ≈ 12 options-across, CEDR501 6 single-cell … — each below the floor) — recorded.

### 3. PROTECTED GATES

- **A widget-build round** (§4: judged on its verifier; skeleton-blind — the widget is one WIDGET line): skeleton {MEAN} % @ 2486 EXACT, RAW 39.469 → {RAW} %; cs / body / clean / leak EXACT; tags 9557 / 9557; every verifier ✓, every COUNT held (`_r507_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 507`; `--gate-baseline-check` PASS. Plateau: neither (a widget build).

**Ledger:** scoped #2 since the r505 FULL · data `multiChoiceQuiz.yellow_ticks` · env `MCQYELLOW_OFF` · code `InteractiveBuilder.#multiChoiceQuiz`, `InteractiveScanner` (`prevItemText`) · tools `_r507_answers.cjs`, `_r507_finalise.py` · session 49 Round 8. Next D15-19 type (a later kickoff): dropDown.
"""
F.finalise(
    N=507, old_build="260620.69", new_build="260620.70", entry=entry,
    config_comment="D15-19 THE YELLOW-✅ MULTIPLE-CHOICE QUIZ (session 49 Round 8): the writer's yellow highlight builds the quiz "
                   "unannounced under the three checks. Env MCQYELLOW_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 507 BASELINE (D15-19 the yellow-✅ multiChoiceQuiz, "
        f"`MCQYELLOW_OFF`; SCOPED, scoped #2 since the r505 FULL; a widget build, skeleton-blind): SCAFFOLD mean {MEAN}% / >=50% 1599 / "
        f">=75% 276 / >=90% 26 / RAW {RAW}% @ 2486 pairs — EXACT; 4 quizzes / 19 questions, 17 = the gold's answer.**",
    og11="| `MCQYELLOW_OFF` | 507 | **D15-19 THE YELLOW-✅ MULTIPLE-CHOICE QUIZ** (session 49 Round 8). Reverts "
         "`interactive_builders.multiChoiceQuiz.yellow_ticks`: a quiz whose only answer mark is the writer's yellow highlight stays a "
         "hand-off box (the r305 `[correct]` reading alone); byte-identical to r506. |",
    og14=f"- **Build:** `260620.70` (round 507 — **D15-19 the yellow-✅ multiChoiceQuiz**; `MCQYELLOW_OFF`; scoped #2 since the r505 "
         f"FULL; 4 quizzes / 19 questions, 17 = the gold's answer; skeleton {MEAN} % EXACT).",
    gb_note=f"Round 507 (session 49 Round 8, 2026-09-25) — D15-19 THE YELLOW-TICK MULTIPLE-CHOICE QUIZ (MCQYELLOW_OFF): 4 quizzes / "
            f"19 questions built on CEDO502 / CEDR501 / CEDW501 / MXEX302 (17 = the gold's answer); skeleton-blind (EXACT), RAW -> {RAW}; "
            f"_verify_mcq defect 0; scoped #2.",
    no_round=f"- **No round in flight** (25 Sept 2026 {T}, session 49 Round 8 — r507 (D15-19 the yellow-✅ multiChoiceQuiz) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r507** (260620.70); **LAST FULL = r505 (the session-49 Round 6 "
             "backstop)**; ledger **scoped #2** (6 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages) / "
             "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages) / `_r489_accbullet_declined.patch` (the accordion bulleted "
             "bold lead, 8 accordions / 4 modules) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page).",
    last_shipped=f"- LAST SHIPPED: **r507** (build 260620.70, 25 Sept {T}, session 49 Round 8 — D15-19 THE YELLOW-✅ MULTIPLE-CHOICE "
                 "QUIZ, `MCQYELLOW_OFF`; SCOPED, **scoped #2 since the r505 FULL**; 4 quizzes / 19 questions on CEDO502 / CEDR501 / "
                 "CEDW501 / MXEX302, 17 = the gold's answer, `_verify_mcq` defect 0; the D2L (TEFUN04) and answer-key (ARFUN04) forms "
                 f"declined; skeleton-blind: {MEAN} % EXACT, RAW {RAW} %).",
    before_them_add="D15-18 part 1 the RHS side column",
    plateau="- Plateau window (§4): **0 of 3** — r507 a widget build, skeleton-blind (neither); ",
    standing="- Standing facts: AppVersion **260620.70** (r507 D15-19 the yellow-✅ multiChoiceQuiz — session 49 Round 8, 25 Sept); "
             "before it 260620.69 (",
    roundlog=f"- s49-r8 (engine r507, build 260620.70, 25 Sept ≈20:50 → {T}) · D15-19 THE YELLOW-✅ MULTIPLE-CHOICE QUIZ (guards: one "
             "ticked option per question, no D2L `[Button] … quiz`, no \"no correct answers\"; an answer-key line set aside) · SHIPPED "
             "scoped #2 · 4 quizzes / 19 questions, 17 = the gold's, verifier defect 0 · skeleton-blind · plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r507, 260620.70):** `multiChoiceQuiz.yellow_ticks` (env `MCQYELLOW_OFF`), `#multiChoiceQuiz` + "
                  "`InteractiveScanner.prevItemText`. Probe OFF 0; ON 8 files / 4 modules; 17 / 19 answers = the gold's.",
)
