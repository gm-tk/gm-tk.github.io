#!/usr/bin/env python3
"""Session 45 Round 10 — record the FULL-SHIP BACKSTOP at build 260620.53 (no engine change): BUILD_CHANGELOG.md (a short entry, no version
bump), gate_baseline.json (a note), OPERATING_GUIDE §14 (a line), LOOP_STATE.md (Position LAST FULL, ledger, round log, next-session). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "FULL-SHIP BACKSTOP at 260620.53" not in sc[:4000]
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO); a14 = "- **Build:** `260620.53` (round 490"; assert so.count(a14) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
entry = """## 2026-09-25 (session 45 Round 10, build 260620.53 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r490 engine is byte-identical to the ship

- **Why:** seven scoped ships since the r482 FULL (r483–r488, r490; the cadence is 8 and the next scoped ship would reach it) — a scoped ship proves only its affected set + a 12-module sample; the backstop proves the whole chain (r486 the quote form, r487 the named hover anchor, r488 the story carousel shell, r490 the LO WALT alert) at once.
- **Run** (`outputs/_s45_full_regen.sh` — `_batch_plan.py`'s plan, 42 batches, 4 parallel workers under WSL, 08:03 → 08:10): all rc 0; `_stalecheck.sh` 0 stale; **`_content_manifest.py diff`: IDENTICAL — 0 pages differ** from the shipped manifest (all 545 modules).
- **Gates on the fully fresh corpus** (`outputs/_s45_full_postship.sh`): `run_all_gates.sh` rc 0, every verifier RESULT ✓; skeleton **55.3705 % @ 2491**, ≥50 1585, ≥75 277, ≥90 26, RAW 39.285 % — **0 movers** vs r490; `_gatecheck.py skeleton defect` **PASS** on the 0-stale corpus (the `cs bc` call re-prints CACHED skeleton rows — the documented trap; its own cs / bc rows HELD); selftests 50 green / 0 fail; feature index GREEN; the miner 194 CANDIDATE (byte-identical to r490's queue). Ledger `record-full --round 490 --build 260620.53` → **LAST FULL = r490, scoped #0 (8 of headroom)**; fast-loop baseline re-snapshot; content manifest snapshot.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
so = so.replace(a14, "- **FULL backstop** at `260620.53` (session 45 Round 10, 25 Sept): all 545 modules regenerated, **0 pages differ** from the "
                "shipped manifest; every gate HELD; ledger reset (LAST FULL = r490).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-s45-full.bak")
G = rd(P).split("\n")
k = [i for i, l in enumerate(G) if l.strip().startswith('"_note_r490": ')]; assert len(k) == 1
G.insert(k[0], '    "_note_s45_full": "FULL-SHIP BACKSTOP at build 260620.53 (session 45 Round 10, 2026-09-25, no engine change): all 545 modules regenerated '
         '— 0 pages differ from the shipped manifest; skeleton 55.3705 @ 2491 (0 movers), cs / body / clean / leak EXACT; ledger LAST FULL = r490.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-s45-full.bak")
i = find("- **No round in flight** (25 Sept 2026 ≈08:05, session 45 Round 9")
L[i] = L[i].replace("**LAST FULL = r482 (the s44 backstop)**; ledger **scoped #7** (1 of headroom — the FULL backstop is due at the next scoped ship)",
                    "**LAST FULL = r490 (the session-45 Round 10 backstop, 0 pages differ)**; ledger **scoped #0** (8 of headroom)", 1)
assert "LAST FULL = r490" in L[i]
k = find("## Round log")
L.insert(k + 1, "- s45-r10 (no engine change, 25 Sept 08:02 → 08:35 real clock) · THE FULL-SHIP BACKSTOP at 260620.53 (scoped #7 since the r482 FULL — "
         "r483–r488, r490): all 545 modules regenerated in 7 min, **0 pages differ** from the shipped manifest; skeleton 0 movers; every gate "
         "HELD on the fresh corpus; ledger record-full (LAST FULL = r490) · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = L[k].replace("LAST FULL = **r482** (the s44 backstop); ledger scoped #7 (the FULL backstop due at the next scoped ship)",
                    "LAST FULL = **r490** (the s45 Round 10 backstop, 0 pages differ); ledger scoped #0", 1)
assert "LAST FULL = **r490**" in L[k]
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
