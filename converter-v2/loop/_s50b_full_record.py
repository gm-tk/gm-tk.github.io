#!/usr/bin/env python3
"""Session 50 Round 14 — record THE FULL-SHIP BACKSTOP at 260620.81 (no engine change): the BUILD_CHANGELOG entry and the
LOOP_STATE Position / Round log. WSL, from outputs/."""
import io, re
ROOT = "../.."
CL = f"{ROOT}/pageforge-site/converter-v2/BUILD_CHANGELOG.md"
LS = f"{ROOT}/LOOP_STATE.md"
entry = """## 2026-09-26 (session 50 Round 14, build 260620.81 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r520 engine is byte-identical to the shipped manifest (545 dirs / 543 modules / 2,673 pages; 0 pages differ)

### 1. WHAT RAN

The ledger's backstop (`_ship_ledger.py`: scoped #6 since the r513 FULL — r514, r515, r517, r518, r519, r520; taken at the session's close, two of the cadence's 8 left, after a PICK pass found no class at the floor on any lane) — no engine, data or registry change and no ride-along (LOOP §2). `outputs/_s50b_full_regen.sh`: `_batch_plan.py`'s 42 batches as `batch_convert.cjs` calls, 4 parallel workers under WSL — 6 min 19 s, every batch rc 0, `_stalecheck.sh` 0 stale.

### 2. PROOF

- **`_content_manifest.py fresh` (affected = none): all 543 modules BYTE-IDENTICAL to the shipped manifest** — every scoped ship since r513 was complete (none under-scoped). Identical bytes cannot move a metric.
- `outputs/_s50b_full_postship.sh`: `run_all_gates.sh` — every verifier RESULT ✓, every COUNT held (dragdrop 21, typing 14 / 145, bingo 52, flipcard 61, math 323, menulabels 111), tags 9557 / 9557; skeleton `--json` vs the pre-backstop state: 0 movers, +0.0000pp; `_gatecheck.py cs bc` (its skeleton rows CACHED — LOOP §6) then `skeleton defect --commit --round 520`: every gate HELD; `--gate-baseline-check` PASS; the fast-loop baseline and the content manifest re-snapshotted; the 17 verifier selftests + the skeleton and feature-index selftests GREEN (50 PASS / GREEN lines, 0 FAIL); the feature index rebuilt; the DIFF MINER re-mined (195 CANDIDATE).
- Ledger: `record-full --round 520 --build 260620.81` — LAST FULL = r520; scoped-since 0 (8 of headroom).

### 3. PROTECTED GATES — EXACT

Skeleton **55.7489 % @ 2486** (≥50 1612, ≥75 285, ≥90 26), RAW 39.594 %; cs 16769 / 204 / 886; body ANY 235; clean 2585 / 2627; leak 52 / 42 — all EXACT. Plateau: neither (a change-free backstop).

"""
with io.open(CL, encoding="utf-8", newline="") as f: s = f.read()
i = s.index("\n## 20") + 1
s = s[:i] + entry + s[i:]
with io.open(CL, "w", encoding="utf-8", newline="") as f: f.write(s)
print("changelog ok")

with io.open(LS, encoding="utf-8", newline="") as f: L = f.read().split("\n")
mk = [k for k, l in enumerate(L) if l.startswith("- **SESSION-50 ROUND 14 IN FLIGHT")]
assert len(mk) == 1, mk
del L[mk[0]]
nr = [k for k, l in enumerate(L) if l.startswith("- **No round in flight**")]
assert len(nr) == 1, nr
l = L[nr[0]]
l = re.sub(r"^- \*\*No round in flight\*\* \(26 Sept 2026 [0-9:]+, session 50 Round 13 — r520 \(the FIB form's remainder\) SHIPPED and committed; the in-flight marker is cleared\)\.",
           "- **No round in flight** (26 Sept 2026 05:58, session 50 Round 14 — the FULL-SHIP BACKSTOP at 260620.81 (no engine change, 0 pages differ) DONE and committed; the in-flight marker is cleared).", l)
l = l.replace("**LAST FULL = r513 (the session-50 Round 5 backstop)**; ledger **scoped #6** (2 of headroom)",
              "**LAST FULL = r520 (the session-50 Round 14 backstop)**; ledger **scoped #0** (8 of headroom)")
assert "Round 14" in l and "scoped #0" in l, "no-round line"
L[nr[0]] = l
pl = [k for k, x in enumerate(L) if x.startswith("- Plateau window (§4): **2 of 3** — ")]
assert len(pl) == 1
L[pl[0]] = L[pl[0]].replace("- Plateau window (§4): **2 of 3** — ", "- Plateau window (§4): **2 of 3** — s50-r14 the FULL backstop, change-free (neither); ", 1)
for k, x in enumerate(L):
    if "`DIFF_QUEUE.md` 26 Sept 05:24 on the r520 corpus" in x:
        L[k] = x.replace("`DIFF_QUEUE.md` 26 Sept 05:24 on the r520 corpus", "`DIFF_QUEUE.md` 26 Sept 05:56 on the r520 FULL-backstop corpus")
rl = [k for k, x in enumerate(L) if x.startswith("- s50-r13 (engine r520")]
assert len(rl) == 1
L.insert(rl[0] + 1, "- s50-r14 (no engine change, 26 Sept 05:28 → 05:58) · a PICK pass (no class at the floor on any lane — the miner's 195 rows dispositioned, the dashboard's blockers one-off shapes, the Fundamentals over-capture family recorded before, `_s50_r14_headfrag.cjs` 276 fragments almost all labels / notes: DECLINED) then THE FULL-SHIP BACKSTOP at 260620.81 (scoped #6 since the r513 FULL): 545 dirs regenerated in 6 min 19 s, **0 pages differ**; every gate HELD, the full gatecheck's --commit wrote 0 changed aggregates; ledger record-full (LAST FULL = r520); miner 195 CANDIDATE · plateau 2 of 3 (neither).")
with io.open(LS, "w", encoding="utf-8", newline="") as f: f.write("\n".join(L))
print("LOOP_STATE ok")
