#!/usr/bin/env python3
"""Session 51 Round 12 — record THE FULL-SHIP BACKSTOP at 260620.86 (no engine change): the BUILD_CHANGELOG entry and the
LOOP_STATE Position / Round log. WSL, from outputs/:  python3 _s51_full_record.py HH:MM"""
import io, re, sys, os, shutil
ROOT = "../.."
CL = f"{ROOT}/pageforge-site/converter-v2/BUILD_CHANGELOG.md"
LS = f"{ROOT}/LOOP_STATE.md"
T = sys.argv[1]
entry = """## 2026-09-26 (session 51 Round 12, build 260620.86 — NO engine change) — THE LEDGER'S FULL-SHIP BACKSTOP: the whole corpus regenerated with the r526 engine is byte-identical to the shipped manifest (545 dirs / 543 modules / 2,673 pages; 0 pages differ)

### 1. WHAT RAN

The ledger's backstop (`_ship_ledger.py`: scoped #5 since the r520 FULL — r522, r523, r525, r526 plus r523's re-run; taken early, three of the cadence's 8 left, as the clean check after this session's four shipped engine rounds, three declined-and-backed-out patches (r524, r527, r527 v2) and the r526 commit that landed in two parts (5bce0fe + 84b660d)) — no engine, data or registry change and no ride-along (LOOP §2). `outputs/_s51_full_regen.sh`: `_batch_plan.py`'s 42 batches as `batch_convert.cjs` calls, 4 parallel workers under WSL — 6 min 24 s, every batch rc 0, `_stalecheck.sh` 0 stale (TRR104 / TRR105 listed by `fresh` as not regenerated: the two recorded no-source dirs, no Claude build — as at every FULL).

### 2. PROOF

- **`_content_manifest.py diff`: IDENTICAL — 0 pages differ** from the shipped manifest: every scoped ship since r520 was complete (none under-scoped), and the backed-out r524 / r527 patches left nothing behind. Identical bytes cannot move a metric.
- `outputs/_s51_full_postship.sh`: `run_all_gates.sh` — every verifier RESULT ✓, every COUNT held (flipcard 61, math 323, menulabels 111, dragdrop 21, bingo 52 / 624, typing 25 / 232), tags 9557 / 9557 (0 real failures); skeleton `--json` vs the pre-backstop state: 0 movers, +0.0000pp; `_gatecheck.py cs bc` (its skeleton rows CACHED at 55.75 — LOOP §6, ignored) then `skeleton defect --commit --round 526`: every gate HELD; `_fastloop_diff.py --gate-baseline-check` PASS; the fast-loop baseline and the content manifest re-snapshotted; the verifier selftests + the skeleton and feature-index selftests GREEN (50 PASS / GREEN lines, 0 FAIL); the feature index rebuilt; the DIFF MINER re-mined (197 CANDIDATE, the table unchanged).
- Ledger: `record-full --round 526 --build 260620.86` — LAST FULL = r526; scoped-since 0 (8 of headroom).

### 3. PROTECTED GATES — EXACT

Skeleton **56.1010 % @ 2486** (≥50 1627, ≥75 292, ≥90 28), RAW 39.844 %; cs 16830 / 204 / 879; body ANY 234; clean 2585 / 2627; leak 52 / 42 — all EXACT. Plateau: neither (a change-free backstop).

"""
with io.open(CL, encoding="utf-8", newline="") as f: s = f.read()
assert "session 51 Round 12" not in s[:5000], "already recorded"
i = s.index("\n## 20") + 1
s2 = s[:i] + entry + s[i:]
io.open(CL + ".tmp", "w", encoding="utf-8", newline="").write(s2); assert os.path.getsize(CL + ".tmp") > len(s)
os.replace(CL + ".tmp", CL)
print("changelog ok")

src = io.open(LS, encoding="utf-8", newline="").read(); L = src.split("\n")
shutil.copyfile(LS, f"{ROOT}/_Backups/loop_state/LOOP_STATE.md.pre-s51-r12.bak")
mk = [k for k, l in enumerate(L) if l.startswith("- **ROUND s51-r12 IN FLIGHT")]
assert len(mk) == 1, mk
del L[mk[0]]
nr = [k for k, l in enumerate(L) if l.startswith("- **Before rs51-r12: no round in flight**")]
assert len(nr) == 1, nr
l = L[nr[0]]
l = re.sub(r"^- \*\*Before rs51-r12: no round in flight\*\* \(26 Sept 2026 13:26, session 51 Round 7 — r526 \(the BLL introduction heading's own full-width row\) SHIPPED and committed; the in-flight marker is cleared\)\.",
           f"- **No round in flight** (26 Sept 2026 {T}, session 51 Round 12 — the FULL-SHIP BACKSTOP at 260620.86 (no engine change, 0 pages differ) DONE and committed; the in-flight marker is cleared).", l)
l = l.replace("**LAST FULL = r520 (the session-50 Round 14 backstop)**; ledger **scoped #5** (3 of headroom)",
              "**LAST FULL = r526 (the session-51 Round 12 backstop)**; ledger **scoped #0** (8 of headroom)")
assert "Round 12" in l and "scoped #0" in l, "no-round line"
L[nr[0]] = l
pl = [k for k, x in enumerate(L) if x.startswith("- Plateau window (§4): **0 of 3** — ")]
assert len(pl) == 1
L[pl[0]] = L[pl[0]].replace("- Plateau window (§4): **0 of 3** — ", "- Plateau window (§4): **0 of 3** — s51-r12 the FULL backstop, change-free (neither); ", 1)
rl = [k for k, x in enumerate(L) if x.startswith("- compaction at 13:54 during s51-r12")]
assert len(rl) == 1
L.insert(rl[0], f"- s51-r12 (no engine change, 26 Sept 13:54 → {T}) · THE FULL-SHIP BACKSTOP at 260620.86 (scoped #5 since the r520 FULL; the clean check after four ships, three backed-out patches and the split r526 commit): 545 dirs regenerated in 6 min 24 s, **0 pages differ**; every gate HELD (56.1010 %, cs 16830 / 204 / 879, body ANY 234), `--gate-baseline-check` PASS; ledger record-full (LAST FULL = r526); miner 197 CANDIDATE, table unchanged · plateau 0 of 3 (neither).")
out = "\n".join(L)
io.open(LS + ".tmp", "w", encoding="utf-8", newline="").write(out); assert os.path.getsize(LS + ".tmp") > 90000
os.replace(LS + ".tmp", LS)
print("LOOP_STATE", len(src.encode()), "->", os.path.getsize(LS))
