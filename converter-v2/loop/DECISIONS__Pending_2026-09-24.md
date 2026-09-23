# Pending decisions — 24 September 2026 (written by the loop's session 40)

> This file records measurements that ended in a DECLINE because the rules say a human must choose. Nothing here blocks the loop. Answer through `/loop-decisions` when convenient.

## 1. The `[RHS alert]` family (claude-audit answer 4, the brief's Phase 3) — MEASURED, DECLINED

**What was measured** (`CONVERTER_V2/outputs/_rhsalert_measure.py` / `.log`): every Writers Template tag spelled `[rhs alert…]`, `[alert rhs…]`, `[alert box rhs…]`, `[right-hand alert…]`, `[alert box right hand side…]` — **176 tags / 73 modules**. For the 139 tags (67 modules) whose text could be found on the human's page, the human built:

| human's form | tags | share |
|---|---:|---:|
| a right-hand side column holding an `alert top` box | 42 | 0.30 |
| a right-hand side column holding an `alertActivity` box | 39 | 0.28 |
| a full-width alert | 27 | 0.19 |
| an ordinary body paragraph | 18 | 0.13 |
| a speech bubble | 7 | 0.05 |
| an `alertActivity` box not in a side column | 6 | 0.04 |

By template, the two side-column forms together: **Standard 0.62** (60 of 97), Fundamentals 0.56 (18 of 32), Inquiry 0.30 (3 of 10).

**Why it was declined.** The approved brief says: build only if ONE human form holds at least 0.60 of the tags. The largest single form holds 0.30; even the two side-column forms added together hold 0.58. PageForge already puts an `rhs` alert in a side column (round 333, choosing `alert top` or `alertActivity` by where the box sits) and matches the human on 55 of the 139.

**The choice, if you want one.**
- **Keep it as it is** (recommended) — the writers' own spelling does not tell the human's form apart; round 333 already handles the common case.
- **Make the side column the rule in Standard modules only** (0.62) — it would move roughly the 18 Standard tags PageForge renders full-width or as body text into a side column, and move about 7 Standard tags the human kept full-width the wrong way.
- **Write it into the rulebook** — a Social Sciences / Standard KB rule saying "an RHS alert is always the side box" would outrank the human's split, and PageForge would follow it as a named override.

## 2. Quiz answers the writer HIGHLIGHTED without saying so — build them, or leave the hand-off box?

**Where D13-4 stands after session 40.** You said: build the quiz engines only where the writer marked the answer, and trust a highlight or green text only where the writer *announced* it ("correct answers are highlighted") — round 309's check, because in one module (OSAI101) green text marks every OPTION, not the answer. Under that rule:

- **typing** — built where the answer is typed in red on the question line (round 449: 8 quizzes / 57 answers, 55 of them exactly the human's own answers);
- **multiple choice, dropdown, reorder, radio, selection box** — measured and declined: the largest group with a written or announced answer is 10 boxes (the build floor is 20).

**What is left.** About **190 hand-off boxes** where the writer DID mark the answer with a highlighter but never said so: typing ≈ 77 (a green highlighter, 12 modules — mostly Maths), multiple choice ≈ 63 (23 as lines, 40 in tables), dropdown ≈ 29, radio ≈ 16, reorder ≈ 9. In the parser's own text file these show as the ✅ tick.

**The choice.**
- **Keep the rule** — these stay hand-off boxes (the box now shows the ✅ ticks, round 448, so the developer still sees the answers).
- **Trust a highlight when the page structure proves it** — build where exactly one option per question is highlighted (never every option, the OSAI101 case). The loop would build one type at a time, each with its own answer check against the human's page.

**Recommendation:** the second, typing first (the green-highlighter maths quizzes are the largest group), because the ✅ tick is the writers' own "correct answer" signal and the one-per-question guard answers the OSAI101 risk.
