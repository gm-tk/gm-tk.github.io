#!/usr/bin/env python3
"""Session 46 STOP (§4 BUDGET — the 12-round default reached): the STOPPED entry (the s45 one archived verbatim), the session's
Decisions-from-Chris line, the "Next session starts with:" line. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
shutil.copyfile(S, S + ".pre-s46-stop.bak")
stop = ("## >>> STOPPED 2026-09-25 15:57 NZST (session 46) on §4 BUDGET — the 12-round default reached (≈ 7 h 05 min; the 10 h cap not "
        "reached). **TEN ENGINE ROUNDS SHIPPED + THE FULL BACKSTOP, every one committed:** r491 / r492 the accordion (marker-cell table; the "
        "panel after a table), r493 the BLL closing section, r494 the carousel slide-table tail, r495 KB c5 the literal-tag leak (75 → 52), "
        "r496 / r497 the XDLS choice board's four declined pages, r498 / r499 / r500 the hover definitions (first letters kept; the marker "
        "after the full stop anchored; back-to-back split triggers — drops 153 → 103). **The FULL backstop** (Round 10): 545 modules, 0 pages "
        "differ. **One PICK pass** (R6). Skeleton **55.3705 → 55.4588 % @ 2491 (+0.0883pp)**, ≥50 1585 → 1592, ≥75 277, ≥90 26, RAW 39.285 → "
        "39.425; cs exact 16702 → 16746; leak 75 → 52 occ; clean 2587 → 2591; body ANY 232; **60.5 % of achievable** (ceiling 91.7 %). One "
        "NAMED dip (r499 ≥75 −1, DAN1006_2_0) won back by r500. Plateau 0 of 3. Needs Chris: #17–#19, #22, #23 (none new). <<<")
k = find("## >>> STOPPED 2026-09-25 08:45 NZST (session 45)"); s45 = L[k]
L[k] = ("## STOPPED entry, session 45 (25 Sept 08:45, §4 BUDGET; r486–r488 / r490 shipped + the r490 FULL backstop) -> LOOP_STATE_ARCHIVE.md "
        "'STOPPED entry, session 45 (verbatim, s46 stop)'. Superseded by the session-46 entry above; every verdict stands.")
L.insert(k, stop)
k = find("## Decisions from Chris (session 45 — 2026-09-25 05:14")
L.insert(k, "## Decisions from Chris (session 46 — 2026-09-25 08:51 → 15:57 NZST): the standing `/loop-start` kickoff only (the default "
         "budget, 12 rounds or 10 hours — the 12 rounds reached first) — NO new numbered decision; no new Needs-Chris item.")
L.insert(k + 1, "")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** the standing `/loop-start`. LAST SHIPPED **r500** (260620.63, the back-to-back split trigger); LAST "
        "FULL = **r498** (the s46 Round 10 backstop, 0 pages differ); ledger scoped #4 (4 of headroom); plateau **0 of 3**; 2,491 pairs; "
        "census 552 / 545 / 2,679; the miner 195 CANDIDATE. PICK candidates in Follow-up: the s46-r9 hover residue (14 drops on a term named "
        "elsewhere — a named-anchor pass; the first-letter shapes r498 did not reach), XDLS903_1_0 (the last declined choice-board page), the "
        "s46-r1 / r2 accordion residue, the gathering lane, the §1g census CANDIDATE rows. Ride-along patches `_r469_declined.patch` / "
        "`_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22, #23.")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## STOPPED entry, session 45 (verbatim, s46 stop)\n\n" + s45 + "\n")
out = "\n".join(L); assert len(stop) <= 1700, len(stop)
wr(S, out); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S), "| stop entry", len(stop), "chars")
