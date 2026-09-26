#!/usr/bin/env python3
"""s54 Round 5 — the FULL backstop's finalise (a copy of _s52_full_fin.py): the changelog entry, the LOOP_STATE Position roll (the FULL marker →
archive; the 'Before the FULL' no-round line re-written with LAST FULL = r542 / ledger scoped #0), the Round-log line. No engine / data / AppVersion
change. WSL."""
import io, os, re, subprocess
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"; CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s); assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head)
entry = f"""## 2026-09-27 (session 54 Round 5, build 260621.00 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r542 engine (scoped #7 since the s52-r11 FULL — the cadence-8 backstop one ship early, the s52 precedent)

### 1. WHAT RAN

`outputs/_s54_full_fullship_par.sh` (a copy of `_s52_full_fullship_par.sh`): `_batch_plan.py`'s 42 batches (545 modules) through `batch_convert.cjs --force`, 4 parallel workers under WSL, 04:41 → 04:47 NZDT, every batch rc 0. Then `outputs/_s54_full_postship.sh`: `run_all_gates.sh`, the skeleton state + its delta vs the pre-regeneration snapshot, `_gatecheck.py cs bc` then `skeleton defect --commit --round 542` (the cs bc run printed the CACHED s52 skeleton rows — the §6 trap; the live skeleton run is the verdict), `_ship_ledger.py record-full --round 542`, the fast-loop and content-manifest snapshots, the selftests (50 PASS / GREEN, 0 FAIL), the feature index (GREEN) and the DIFF MINER (198 CANDIDATE, unchanged).

### 2. PROOF

`_content_manifest.py diff` → **IDENTICAL, 0 pages differ** (2,673 pages / 543 modules), taken before the snapshot. Skeleton delta vs the pre-regeneration snapshot: **+0.0000pp, 0 movers**, new-only 0, gone 0.

### 3. PROTECTED GATES

Skeleton **56.3993 % @ 2486**, ≥50 1647, ≥75 309, ≥90 29, RAW 40.082 %; compare_structure exact 17062 / EXTRA 206 / missing 581; body_compare ANY 233; clean 2585 / 2627; leak 52 / 42; tags 9557; every verifier ✓, every COUNT held (`_s54_full_gates.log`); `--gate-baseline-check` PASS.

**Ledger:** FULL recorded at round 542 (260621.00); scoped-since counter 0 (8 of headroom) · session 54 Round 5.
"""
wr(PC, head + entry.strip() + "\n\n" + sc[len(head):]); print("changelog ok")
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); L = rd(S).split("\n")
fl = [i for i, l in enumerate(L) if l.startswith("- **FULL BACKSTOP IN FLIGHT — NOT PROVEN**")]; assert len(fl) == 1
nr = [i for i, l in enumerate(L) if l.startswith("- **Before the FULL: no round in flight**")]; assert len(nr) == 1
marker, prior = L[fl[0]], L[nr[0]]
new_nr = prior.replace("- **Before the FULL: no round in flight** (27 Sept 2026 04:33 NZDT,",
                       f"- **No round in flight** (27 Sept 2026 {T} NZDT, session 54 Round 5 — THE FULL-SHIP BACKSTOP at 260621.00 DONE and committed (no engine change, 0 pages differ); before it 04:33 NZDT,", 1)
new_nr = new_nr.replace("**LAST FULL = r534 (the session-52 Round 11 backstop)**", "**LAST FULL = r542 (the session-54 Round 5 backstop)**", 1)
new_nr = re.sub(r"ledger \*\*scoped #7\*\* \(1 of headroom — the FULL backstop is due at the next ship\)", "ledger **scoped #0** (8 of headroom)", new_nr, count=1)
assert "scoped #0" in new_nr and "LAST FULL = r542" in new_nr and new_nr.startswith("- **No round in flight**"), new_nr[:500]
L[nr[0]] = new_nr; del L[fl[0]]
rl = [i for i, l in enumerate(L) if l == "## Round log"]; assert len(rl) == 1
L.insert(rl[0] + 1, f"- s54-r5 (no engine change, 27 Sept 04:39 → {T} NZDT) · THE LEDGER'S FULL-SHIP BACKSTOP at 260621.00 (scoped #7 → 0; the cadence-8 "
                    "backstop one ship early): 42 batches / 545 modules / 4 workers, 0 pages differ, every gate identical (56.3993 %, ≥50 1647, ≥75 309, ≥90 29); "
                    "selftests 50 / 0; the miner re-run (198 CANDIDATE) · plateau: neither.")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 54 — the Round-5 FULL marker (verbatim) + done\n\n" + marker + "\n- **Done:** 0 pages differ; every gate identical; ledger reset (LAST FULL = r542).\n")
wr(S, "\n".join(L)); print("LOOP_STATE ok", os.path.getsize(S))
