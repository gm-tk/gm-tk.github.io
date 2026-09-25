#!/usr/bin/env python3
"""SESSION 50 Round 5 — record THE FULL-SHIP BACKSTOP at 260620.75 (no engine change, no AppVersion bump). WSL."""
import io, os, json, re
import _s50_fin as F
T = F.now()
ROOT, CV = F.ROOT, F.CV
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = F.rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(session 50 Round 5," not in sc[:6000]
entry = """## 2026-09-26 (session 50 Round 5, build 260620.75 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r513 engine is byte-identical to the shipped manifest (545 dirs / 543 modules / 2,673 pages; 0 pages differ)

### 1. WHAT RAN

The ledger's backstop (`_ship_ledger.py`: scoped #7 since the r505 FULL — r510, r511, r513; one of the cadence's 8 left, taken at once) — no engine, data or registry change and no ride-along (LOOP §2). `outputs/_s50_full_regen.sh`: `_batch_plan.py`'s 42 batches as `batch_convert.cjs` calls, 4 parallel workers under WSL — 6 min 19 s, every batch rc 0, `_stalecheck.sh` 0 stale.

### 2. PROOF

- **`_content_manifest.py fresh` (affected = none): all 543 modules BYTE-IDENTICAL to the shipped manifest.** Identical bytes cannot move a metric.
- `outputs/_s50_full_postship.sh`: `run_all_gates.sh` — every verifier RESULT ✓, every COUNT held, tags 9557 / 9557; skeleton `--json` vs the pre-backstop state: 0 movers, +0.0000pp; `_gatecheck.py cs bc` then `skeleton defect --commit --round 513`: every gate HELD, the commit wrote 0 changed aggregates; `--gate-baseline-check` PASS; the fast-loop baseline and the content manifest re-snapshotted; 50 selftest lines GREEN, 0 FAIL; the feature index rebuilt (selftest GREEN); the DIFF MINER re-run (194 CANDIDATE, 0 parse errors).

### 3. PROTECTED GATES — EXACT

Skeleton **55.6929 % @ 2486** (≥50 1607, ≥75 281, ≥90 26), RAW 39.539 %; cs 16768 / 204 / 887; body ANY 233; clean 2585 / 2627; leak 52 / 42 — all EXACT. Plateau: neither (a change-free backstop).

**Ledger:** FULL ship recorded at round 513 (the counter reset) · tools `_s50_full_regen.sh`, `_s50_full_postship.sh`, `_s50_full_record.py` · session 50 Round 5.

"""
F.wr(PC, head + entry + sc[len(head):]); print("changelog ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json")
G = F.rd(P).split("\n")
hits = [i for i, l in enumerate(G) if re.match(r'^    "_note_r\d+": ', l)]
G.insert(hits[0], '    "_note_s50_full": ' + json.dumps("Session 50 Round 5 (2026-09-26) — THE FULL-SHIP BACKSTOP at 260620.75 (no engine change): 545 dirs "
         "regenerated, all 543 modules byte-identical to the manifest; the full gatecheck HELD every gate and its --commit wrote 0 changed "
         "aggregates; ledger LAST FULL = r513.", ensure_ascii=False) + ",")
out = "\n".join(G); json.loads(out); F.wr(P, out); print("gate_baseline note ok")
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = F.rd(S); L = ss.split("\n")
fl = [i for i, l in enumerate(L) if l.startswith("- **ROUND s50-r5 (THE FULL BACKSTOP) IN FLIGHT")]; assert len(fl) == 1
nr = [i for i, l in enumerate(L) if l.startswith("- **No round in flight**")]; assert len(nr) == 1
marker, prior = L[fl[0]], L[nr[0]]
new = prior.replace("- **No round in flight** (26 Sept 2026 ", f"- **No round in flight** (26 Sept 2026 {T} — the session-50 Round 5 FULL backstop DONE, 0 pages differ; before it ", 1) \
    .replace("**LAST FULL = r505 (the session-49 Round 6 backstop)**; ledger **scoped #7** (1 of headroom — the NEXT round is the FULL backstop)",
             "**LAST FULL = r513 (the session-50 Round 5 backstop)**; ledger **scoped #0** (8 of headroom)", 1)
assert "LAST FULL = r513" in new, "no-round rewrite"
L[fl[0]] = new
del L[nr[0]]
pl = [i for i, l in enumerate(L) if l.startswith("- Plateau window (§4): **")]; assert len(pl) == 1
L[pl[0]] = re.sub(r"^- Plateau window \(§4\): \*\*(\d) of 3\*\* — ", lambda m: f"- Plateau window (§4): **{m.group(1)} of 3** — s50-r5 the FULL backstop, change-free (neither); ", L[pl[0]], count=1)
rl = [i for i, l in enumerate(L) if l == "## Round log"]; assert len(rl) == 1
L.insert(rl[0] + 1, f"- s50-r5 (no engine change, 26 Sept 02:05 → {T}) · THE FULL-SHIP BACKSTOP at 260620.75 (scoped #7 since the r505 FULL): 545 dirs "
         "regenerated in 6 min 19 s, **0 pages differ**; every gate HELD, the full gatecheck's --commit wrote 0 changed aggregates; ledger "
         "record-full (LAST FULL = r513); miner 194 CANDIDATE · plateau 0 of 3 (neither).")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 50 — Round 5 (the FULL backstop) — the in-flight marker + the prior no-round line (verbatim)\n\n" + marker + "\n" + prior + "\n")
F.wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
