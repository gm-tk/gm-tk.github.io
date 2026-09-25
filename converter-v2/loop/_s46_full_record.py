#!/usr/bin/env python3
"""Session 46 Round 10 — record the FULL-SHIP BACKSTOP at build 260620.61 (no engine change): BUILD_CHANGELOG.md (a short entry, no version
bump), gate_baseline.json (a note + the re-base of two stale values the fresh-corpus verdict exposed), OPERATING_GUIDE §14 (a line),
LOOP_STATE.md (the in-flight line → a no-round line, LAST FULL, ledger, round log). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "FULL-SHIP BACKSTOP at 260620.61" not in sc[:4000]
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO); a14 = "- **Build:** `260620.61` (round 498"; assert so.count(a14) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
entry = """## 2026-09-25 (session 46 Round 10, build 260620.61 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r498 engine is byte-identical to the shipped manifest (0 pages differ); two stale baseline values re-based

- **Why:** eight scoped ships since the r490 FULL (r491–r498 — the cadence 8 reached at r498); a scoped ship proves only its affected set + a 12-module sample, the backstop bounds any accumulated under-scoping.
- **Run** (`outputs/_s46_full_regen.sh` — `_batch_plan.py`'s plan, 42 batches, 4 parallel workers under WSL, 14:30 → 14:37): all rc 0; `_stalecheck.sh` 0 stale; **`_content_manifest.py changed`: IDENTICAL — 0 pages differ**.
- **Gates on the fully fresh corpus** (`outputs/_s46_full_postship.sh`): `run_all_gates.sh` rc 0, every verifier RESULT ✓; skeleton **55.4469 % @ 2491** (median 56.5 %), ≥50 1591, ≥75 277, ≥90 26, RAW 39.419 %, 0 movers vs r498; cs 16745 / 198 / 888; body ANY 232; clean 2591 / 2633; leak 52 / 42; selftests 50 / 0; the miner 195 CANDIDATE. Ledger `record-full` (LAST FULL = r498, scoped counter 0).
- **Re-based in `gate_baseline.json`** (the `_gatecheck.py` verdict read them as live-vs-baseline IMPROVED — stale, not a change): `skeleton.mean_scaffold_pct` 55.41 → 55.45 (the r495–r498 finalises set `pages_ge_50` / `raw_mean_pct` but not the mean) and `median_scaffold_pct` 56.3 → 56.5; `body_compare.any_breakdown` 238 → 232 (r497's −3 and earlier rounds' drops never written back).

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
so = so.replace(a14, "- **FULL backstop** at `260620.61` (session 46 Round 10, 25 Sept): all 545 modules regenerated, **0 pages differ** from the "
                "shipped manifest; every gate HELD; ledger reset (LAST FULL = r498); `gate_baseline.json` skeleton mean 55.45 / median 56.5, body ANY 232 "
                "re-based.\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-s46-full.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    hits = [i for i, l in enumerate(G) if l.strip().rstrip(",") == f'"{key}": {old}']
    assert len(hits) == 1, (key, hits); G[hits[0]] = G[hits[0]].replace(f'"{key}": {old}', f'"{key}": {new}')
setv("mean_scaffold_pct", "55.41", "55.45"); setv("median_scaffold_pct", "56.3", "56.5"); setv("any_breakdown", "238", "232")
k = [i for i, l in enumerate(G) if l.strip().startswith('"_note_r498": ')]; assert len(k) == 1
G.insert(k[0], '    "_note_s46_full": "FULL-SHIP BACKSTOP at build 260620.61 (session 46 Round 10, 2026-09-25, no engine change): all 545 modules regenerated '
         '— 0 pages differ from the shipped manifest; skeleton 55.4469 @ 2491 (0 movers), cs / body / clean / leak EXACT; ledger LAST FULL = r498; '
         're-based skeleton.mean_scaffold_pct 55.41 -> 55.45, median 56.3 -> 56.5, body_compare.any_breakdown 238 -> 232 (stale values).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-s46-full.bak")
i = find("- **ROUND 10 IN FLIGHT (NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP**"); del L[i]
i = find("- **No round in flight** (25 Sept 2026 ≈14:35, session 46 Round 9")
L[i] = L[i].replace("- **No round in flight** (25 Sept 2026 ≈14:35, session 46 Round 9 — r498 (the hover definition's red first letter) SHIPPED and "
                    "committed; the in-flight marker is cleared).",
                    "- **No round in flight** (25 Sept 2026 ≈14:55, session 46 Round 10 — the FULL-SHIP BACKSTOP done and committed, 0 pages differ; "
                    "before it Round 9's r498 (the hover definition's red first letter) SHIPPED).", 1)
L[i] = L[i].replace("**LAST FULL = r490 (the s45 Round 10 backstop)**; ledger **scoped #8 — THE FULL BACKSTOP IS DUE (take it next)**",
                    "**LAST FULL = r498 (the session-46 Round 10 backstop, 0 pages differ)**; ledger **scoped #0** (8 of headroom)", 1)
assert "LAST FULL = r498" in L[i] and "Round 10" in L[i]
k = find("## Round log")
L.insert(k + 1, "- s46-r10 (no engine change, 25 Sept 14:29 → 14:55 real clock) · THE FULL-SHIP BACKSTOP at 260620.61 (scoped #8 since the r490 "
         "FULL — r491–r498): all 545 modules regenerated in 6 min 15 s, **0 pages differ** from the shipped manifest; skeleton 0 movers; every "
         "gate HELD on the fresh corpus; ledger record-full (LAST FULL = r498); `gate_baseline.json` skeleton mean / median + body ANY re-based "
         "(stale values) · plateau 0 of 3 (neither).")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
