#!/usr/bin/env python3
"""s52 Round 11 — the FULL backstop's finalise: the changelog entry, the LOOP_STATE Position roll (the FULL marker → archive; the
no-round line re-written with LAST FULL = r534 / ledger scoped #0), the Round-log line. No engine / data / AppVersion change. WSL."""
import io, os, re, subprocess
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"; CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s); assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head)
entry = f"""## 2026-09-26 (session 52 Round 11, build 260620.93 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r534 engine (scoped #7 since the s51-r12 FULL — the cadence-8 backstop one ship early), 0 pages differ, every gate identical

### 1. WHAT RAN

`outputs/_s52_full_fullship_par.sh` (a copy of `_s29_r416_fullship_par.sh`): `_batch_plan.py`'s 42 batches through `batch_convert.cjs --force`, 4 parallel workers under WSL, 19:01 → 19:08, every batch rc 0. Then `outputs/_s52_full_postship.sh`: `run_all_gates.sh`, the skeleton state + delta vs the r534 snapshot, `_gatecheck.py cs bc` (its skeleton rows CACHED from r526 — the known quirk, ignored) then `_gatecheck.py skeleton defect --commit --round 534` (live, every gate HELD), `_ship_ledger.py record-full --round 534`, the fast-loop re-snapshot, the content-manifest snapshot, every selftest (50 PASS / GREEN, 0 FAIL), the feature index, the DIFF MINER.

### 2. PROOF

`_content_manifest.py diff` → **IDENTICAL, 0 pages differ** (2,673 pages / 543 modules). Skeleton delta vs the pre-regeneration snapshot: **+0.0000pp, 0 movers**, new-only 0, gone 0.

### 3. PROTECTED GATES

Skeleton **56.3343 % @ 2486**, ≥50 1638, ≥75 305, ≥90 29, RAW 39.971 %; compare_structure exact 17024 / EXTRA 198 / missing 661; body_compare ANY 233; clean 2585 / 2627 = 98.40 %; leak 52 / 42; tags 9557; every verifier ✓, every COUNT held (`_s52_full_gates.log`). Plateau: neither (a change-free backstop).

**Ledger:** FULL recorded at round 534 (260620.93); scoped-since counter 0 (8 of headroom) · session 52 Round 11.
"""
wr(PC, head + entry.strip() + "\n\n" + sc[len(head):]); print("changelog ok")
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); L = rd(S).split("\n")
fl = [i for i, l in enumerate(L) if l.startswith("- **FULL BACKSTOP IN FLIGHT — NOT PROVEN**")]; assert len(fl) == 1
nr = [i for i, l in enumerate(L) if l.startswith("- **Before the FULL: no round in flight**")]; assert len(nr) == 1
marker, prior = L[fl[0]], L[nr[0]]
new_nr = prior.replace("- **Before the FULL: no round in flight** (26 Sept 2026 18:", f"- **No round in flight** (26 Sept 2026 {T}, session 52 Round 11 — THE FULL-SHIP BACKSTOP at 260620.93 DONE and committed (no engine change, 0 pages differ); before it 18:", 1)
new_nr = new_nr.replace("**LAST FULL = r526 (the session-51 Round 12 backstop)**", "**LAST FULL = r534 (the session-52 Round 11 backstop)**", 1)
new_nr = re.sub(r"ledger \*\*scoped #7\*\* — \*\*the FULL backstop is due next \(cadence 8\)\*\*", "ledger **scoped #0** (8 of headroom)", new_nr, count=1)
assert "scoped #0" in new_nr and "LAST FULL = r534" in new_nr, new_nr[:400]
L[nr[0]] = new_nr; del L[fl[0]]
rl = [i for i, l in enumerate(L) if l == "## Round log"]; assert len(rl) == 1
L.insert(rl[0] + 1, f"- s52-r11 (no engine change, 26 Sept 19:00 → {T}) · THE LEDGER'S FULL-SHIP BACKSTOP at 260620.93 (scoped #7 → 0; the cadence-8 "
                    "backstop one ship early): 42 batches / 4 workers, 0 pages differ, every gate identical (56.3343 %, ≥50 1638, ≥75 305, ≥90 29); "
                    "selftests 50 / 0; the miner re-run · plateau: neither.")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 52 — the Round-11 FULL marker (verbatim) + done\n\n" + marker + "\n- **Done:** 0 pages differ; every gate identical; ledger reset.\n")
wr(S, "\n".join(L)); print("LOOP_STATE ok", os.path.getsize(S))
