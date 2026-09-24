#!/usr/bin/env python3
"""Session 44 Round 7 — record the FULL-SHIP BACKSTOP at build 260620.46 (no engine change): BUILD_CHANGELOG.md (a short entry, no version
bump), gate_baseline.json (a note), OPERATING_GUIDE §14 (a line), LOOP_STATE.md (Position LAST FULL, ledger, round log, next-session). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "FULL-SHIP BACKSTOP at 260620.46" not in sc[:4000]
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO); a14 = "- **Build:** `260620.46` (round 482"; assert so.count(a14) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
entry = """## 2026-09-25 (session 44 Round 7, build 260620.46 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r482 engine is byte-identical to the shipped manifest

- **Why:** eight scoped ships since the r474 FULL (r475–r482; `_ship_ledger.py`: cadence 8 reached). A scoped ship proves only its affected set + a 12-module sample; the backstop proves the whole chain.
- **Run** (`outputs/_s44_full_regen.sh` — `_batch_plan.py`'s plan, 42 batches, 4 parallel workers under WSL, 01:55 → 02:02): all rc 0; `_stalecheck.sh` 0 stale; **`_content_manifest.py diff`: IDENTICAL — 0 pages differ** (every r475–r482 affected set was complete).
- **Gates on the fully fresh corpus** (`outputs/_s44_full_postship.sh`): `run_all_gates.sh` rc 0; skeleton **55.3280 % @ 2491**, ≥50 1582, ≥75 275, ≥90 25, RAW 39.237 % — 0 movers vs r482; `_gatecheck.py skeleton defect` (the full skeleton run) **every row HELD**; cs exact 16691 / EXTRA 208 / missing 872, body ANY 238, clean 2587 / 2633, leak 75 / 46 — EXACT (the `cs bc` call printed a CACHED pre-r479 skeleton row, 55.23 — the §6 trap; the full run supersedes it). Ledger `record-full --round 482` (scoped counter 8 → 0); the fast-loop baseline and the content manifest re-snapshotted; 17 selftests + the skeleton selftest green; the feature index green; the miner 195 CANDIDATE.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
so = so.replace(a14, "- **FULL backstop** at `260620.46` (session 44 Round 7, 25 Sept): all 545 modules regenerated, **0 pages differ** from the shipped "
                "manifest; every gate HELD; ledger reset (LAST FULL = r482).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-s44-full.bak")
G = rd(P).split("\n")
k = [i for i, l in enumerate(G) if l.strip().startswith('"_note_r482": ')]; assert len(k) == 1
G.insert(k[0], '    "_note_s44_full": "FULL-SHIP BACKSTOP at build 260620.46 (session 44 Round 7, 2026-09-25, no engine change): all 545 modules regenerated '
         '— 0 pages differ from the shipped manifest; skeleton 55.3280 @ 2491 (0 movers), cs / body / clean / leak EXACT; ledger LAST FULL = r482.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-s44-full.bak")
i = find("- **No round in flight** (25 Sept 2026 ≈02:10, session 44 Round 6")
L[i] = L[i].replace("**LAST FULL = r474**; ledger **scoped #8 — the FULL backstop is DUE**", "**LAST FULL = r482 (the session-44 Round 7 backstop, "
                    "0 pages differ)**; ledger **scoped #0** (8 of headroom)", 1)
assert "LAST FULL = r482" in L[i]
k = find("## Round log")
L.insert(k + 1, "- s44-r7 (no engine change, 25 Sept 01:55 → 02:25) · THE FULL-SHIP BACKSTOP at 260620.46 (the ledger's cadence 8 after r475–r482): all "
         "545 modules regenerated in 7 min, **0 pages differ** from the shipped manifest; every gate HELD on the fresh corpus; ledger record-full "
         "(LAST FULL = r482) · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = L[k].replace("LAST FULL = **r474**; ledger scoped #8 (**the FULL backstop is DUE**)", "LAST FULL = **r482** (the s44 backstop); ledger "
                    "scoped #0", 1)
assert "LAST FULL = **r482**" in L[k]
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
