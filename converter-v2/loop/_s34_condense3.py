#!/usr/bin/env python3
"""Session 34 §5d condense (2): the 'Loop review 2026-09-22' section's two long bullets — 'Adversarial check of the amended files' and
'Left / queued for the loop' (both actioned: r425 / r422 / the 38 intaken / the verify-script and _round_close items still pending) —
move VERBATIM to LOOP_STATE_ARCHIVE.md ('Loop review 2026-09-22 — the two long bullets (verbatim)'); a one-line pointer stays.
Run under WSL: python3 _s34_condense3.py
"""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
lines = st.split("\n")
ia = [i for i, l in enumerate(lines) if l.startswith("- **Adversarial check of the amended files (four readers, after the first commit 36b4272):**")]
il = [i for i, l in enumerate(lines) if l.startswith("- **Left / queued for the loop:** Round 1 = finish r425 (unchanged)")]
assert len(ia) == 1 and len(il) == 1 and il[0] == ia[0] + 1, (ia, il)
moved = lines[ia[0]] + "\n" + lines[il[0]]
pointer = ("- **The adversarial check of the amended files and the 'Left / queued for the loop' list** (verbatim in LOOP_STATE_ARCHIVE.md 'Loop review "
           "2026-09-22 — the two long bullets'): the must-fixes were applied in the follow-up commit; the queued rounds were all run by sessions 33 / 34 "
           "(r425 finished, r422 enabled, the 38 intaken, r426–r429); still open from that list — `verify_after_transfer.sh`'s toolchain check calls native "
           "`python3` (replace with a `wsl -e python3 --version` check), `_round_close.sh` line 13 should copy the skills / settings / hook into the mirror "
           "(the `_s3x_rNNN_mirror.sh` scripts do), and the eight over-cap Round-log lines were condensed by session 34.")
lines[ia[0]:il[0] + 1] = [pointer]
st = "\n".join(lines)
assert "## Loop review 2026-09-22 — the two long bullets" not in ar
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n## Loop review 2026-09-22 — the two long bullets (verbatim, archived from LOOP_STATE.md 2026-09-22 ≈16:22 NZST, session 34 §5d condense)\n\n" + moved + "\n")
wr(R + "LOOP_STATE.md", st)
print("ok", len(st.encode("utf-8")), "bytes")
