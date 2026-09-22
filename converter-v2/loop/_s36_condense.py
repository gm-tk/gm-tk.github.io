#!/usr/bin/env python3
"""Session 36 §5d condense (LOOP_STATE.md 102.7 KB > the 100 KB target after r433's finalise): the verbatim s34 / s35 session-start
notes move to LOOP_STATE_ARCHIVE.md, each summarised in one line in place — no decision deleted. Run under WSL."""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
lines = st.split("\n")
i34 = [i for i, l in enumerate(lines) if l.startswith("**Session 34 started:**")]
i35 = [i for i, l in enumerate(lines) if l.startswith("**Session 35 started:**")]
assert len(i34) == 1 and len(i35) == 1 and i35[0] == i34[0] + 1, (i34, i35)
v34, v35 = lines[i34[0]], lines[i35[0]]
assert "Session 34 / 35 start notes (verbatim" not in ar
ar = ar.rstrip("\n") + "\n\n## Session 34 / 35 start notes (verbatim, s36 §5d condense — archived from LOOP_STATE.md 2026-09-22 ≈23:10 NZST)\n\n" + v34 + "\n\n" + v35 + "\n"
lines[i34[0]] = ("**Session 34 started:** 2026-09-22 13:49 NZST (Opus 5; 12 rounds / 10 h). Health check: tree DIRTY at b892ff1 with exactly the two r427 files "
                 "the Position named IN FLIGHT (the crashed session had run steps 5–6; only step 7 was missing) → Round 1 = r427 finished; census 552 / 545 / 2699 / "
                 "2993 / 762 / 24 EXACT; KB HEAD 44c7c8e → 526d30d (CL-0101, no module rule). Verbatim: LOOP_STATE_ARCHIVE.md 'Session 34 / 35 start notes (verbatim, s36 §5d condense)'.")
lines[i35[0]] = ("**Session 35 started:** 2026-09-22 16:32 NZST (Opus 5; 12 rounds / 10 h). Health check clean at b1e1250; census EXACT (no intake trigger; (b)–(d) clear); "
                 "LOOP_STATE.md 99 KB → condensed to 88 KB (`_s35_condense.py`); KB HEAD 526d30d → 9f58148 (CL-0102–0104, no module rule); the miner's queue (r429 corpus) "
                 "current, 196 CANDIDATE; the s34 exhaustion verdict PROVISIONAL → Round 1 = the three cheapest re-checks, then the lanes (r430 / r431 / r432 followed). "
                 "Verbatim: LOOP_STATE_ARCHIVE.md 'Session 34 / 35 start notes (verbatim, s36 §5d condense)'.")
wr(R + "LOOP_STATE_ARCHIVE.md", ar); wr(R + "LOOP_STATE.md", "\n".join(lines))
print("condense OK")
