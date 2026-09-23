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
