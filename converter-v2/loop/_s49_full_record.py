#!/usr/bin/env python3
"""SESSION 49 Round 6 — record THE FULL-SHIP BACKSTOP at 260620.68 (no engine change, no AppVersion bump). WSL."""
import io, os, json, re, shutil
import _s49_fin as F
T = F.now()
ROOT, CV = F.ROOT, F.CV
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = F.rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(session 49 Round 6," not in sc[:6000]
entry = """## 2026-09-25 (session 49 Round 6, build 260620.68 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r505 engine is byte-identical to the shipped manifest (545 dirs / 543 modules / 2,673 pages; 0 pages differ)

### 1. WHAT RAN

The ledger's backstop (`_ship_ledger.py`: scoped #8 since the r498 FULL — r499, r500, r502, r503, r504, r505 and the two proof re-scores; the cadence is 8) — no engine, data or registry change and no ride-along (LOOP §2). `outputs/_s49_full_regen.sh`: `_batch_plan.py`'s 42 batches as `batch_convert.cjs … --force` calls, 4 parallel workers under WSL, a 900 s wall each — **42 / 42 rc 0 in 6 min 13 s**; `_stalecheck.sh` 0 stale.

### 2. PROOF

- **`_content_manifest.py fresh` (affected = none): all 543 modules BYTE-IDENTICAL to the shipped manifest; `changed` = none.** Identical bytes cannot move a metric.
- `outputs/_s49_full_postship.sh`: `run_all_gates.sh` — every verifier RESULT ✓ and every r501 COUNT line "held (per module too)", tags 9557 / 9557; skeleton `--json` + `_s29_skdelta.py` vs the pre-backstop state: **0 movers, 0 new / 0 gone pages**; `_gatecheck.py cs bc` FIRST (its skeleton row was the documented CACHED one), then `skeleton defect --commit --round 505`: **every protected gate HELD — and the r501 writer reported "0 changed (all already equal)": the full run's own aggregates equal the baseline the scoped commits wrote since r501** (`_fastloop_diff.py --gate-baseline-check` PASS); ledger `record-full --round 505` (LAST FULL = r505, the counter 8 → 0); fast-loop baseline and content manifest re-snapshotted (2,673 pages / 543 modules); **50 selftests GREEN, 0 FAIL**; the feature index GREEN; the DIFF MINER re-run (2,486 pairs, 9,359 classes, **193 CANDIDATE**).

### 3. PROTECTED GATES — EXACT

Skeleton **55.5401 % @ 2486** (≥50 1599, ≥75 276, ≥90 26), RAW 39.467 %; cs 16766 / 199 / 888 / 24; body ANY 232; clean 2585 / 2627; leak 52 / 42 — all EXACT. Plateau: neither (a change-free backstop).

**Ledger:** FULL ship recorded at round 505 (the counter reset) · tools `_s49_full_regen.sh`, `_s49_full_postship.sh`, `_s49_full_record.py` · session 49 Round 6.

"""
F.wr(PC, head + entry + sc[len(head):]); print("changelog ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json")
G = F.rd(P).split("\n")
hits = [i for i, l in enumerate(G) if re.match(r'^    "_note_r\d+": ', l)]
G.insert(hits[0], '    "_note_s49_full": ' + json.dumps("Session 49 Round 6 (2026-09-25) — THE FULL-SHIP BACKSTOP at 260620.68 (no engine change): 545 dirs "
         "regenerated, all 543 modules byte-identical to the manifest; the full gatecheck HELD every gate and its --commit wrote 0 changed "
         "aggregates (the tool-written baseline confirmed); ledger LAST FULL = r505.", ensure_ascii=False) + ",")
out = "\n".join(G); json.loads(out); F.wr(P, out); print("gate_baseline note ok")
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = F.rd(S); L = ss.split("\n")
fl = [i for i, l in enumerate(L) if l.startswith("- **ROUND s49-r6 (THE FULL BACKSTOP) IN FLIGHT")]; assert len(fl) == 1
nr = [i for i, l in enumerate(L) if l.startswith("- **No round in flight**")]; assert len(nr) == 1
marker, prior = L[fl[0]], L[nr[0]]
L[fl[0]] = prior.replace("- **No round in flight** (25 Sept 2026 ", f"- **No round in flight** (25 Sept 2026 {T} — the session-49 Round 6 FULL backstop DONE, 0 pages differ; before it ", 1) \
    .replace("**LAST FULL = r498**; ledger **scoped #8 — the FULL backstop is DUE (the next round)**", "**LAST FULL = r505 (the session-49 Round 6 backstop)**; ledger **scoped #0** (8 of headroom)", 1)
assert "LAST FULL = r505" in L[fl[0]], "no-round rewrite"
del L[nr[0]]
pl = [i for i, l in enumerate(L) if l.startswith("- Plateau window (§4): **")]; assert len(pl) == 1
L[pl[0]] = re.sub(r"^- Plateau window \(§4\): \*\*(\d) of 3\*\* — ", lambda m: f"- Plateau window (§4): **{m.group(1)} of 3** — s49-r6 the FULL backstop, change-free (neither); ", L[pl[0]], count=1)
rl = [i for i, l in enumerate(L) if l == "## Round log"]; assert len(rl) == 1
L.insert(rl[0] + 1, f"- s49-r6 (no engine change, 25 Sept 19:57 → {T}) · THE FULL-SHIP BACKSTOP at 260620.68 (scoped #8 since the r498 FULL): 545 dirs "
         "regenerated in 6 min 13 s, **0 pages differ**; every gate HELD, the full gatecheck's --commit wrote 0 changed aggregates; ledger "
         "record-full (LAST FULL = r505); miner 193 CANDIDATE · plateau 0 of 3 (neither).")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 49 — Round 6 (the FULL backstop) — the in-flight marker + the prior no-round line (verbatim)\n\n" + marker + "\n" + prior + "\n")
F.wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
