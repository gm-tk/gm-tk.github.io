#!/usr/bin/env python3
"""Session 34 §5d condense at the stop (22 Sept ≈16:20): (1) the session-34 start note had been glued to the end of the session-33
line — split it onto its own line; (2) its 3,400-character r427 forensic narrative moves VERBATIM to LOOP_STATE_ARCHIVE.md ('Session 34
start note (verbatim)') and a ≤ 1,200-character summary stays; (3) the STOPPED entry trimmed to ≤ 1,500 characters. LOOP_STATE.md back
under the 100 KB target. Run under WSL: python3 _s34_condense2.py
"""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
lines = st.split("\n")
i17 = [i for i, l in enumerate(lines) if l.startswith("**Session 33 started:**")]
assert len(i17) == 1
l = lines[i17[0]]
k = l.index("**Session 34 started:**"); assert k > 0
s33, s34 = l[:k], l[k:]
short = ("**Session 34 started:** 2026-09-22 13:49 NZST (Claude Code, Opus 5, Chris's Windows machine; hard stop ≈23:49 NZST). Budget: **12 rounds or 10 hours** "
         "(the `/loop-start` default). Kickoff: the standing `/loop-start` message (unchanged since the 22 Sept review). **Health check:** no stale locks; `git status` "
         "DIRTY at b892ff1 (the session-33 crash-recovery commit) — exactly the two r427 files the Position section named as IN FLIGHT; `verify_after_transfer.sh` engine "
         "60 / 62 (those two), gates 81 / 81, census 552 / 545 / 2699 / 2993 / 762 / 24 EXACT (no intake trigger; (b)–(d) clear); LOOP_STATE.md 94.5 KB; the loop file's "
         "\"Amended:\" line at line 9; the §7 diff check clean; the mirror byte-identical. KB HEAD 44c7c8e → 526d30d (CL-0101, six skill descriptions — no module rule; "
         "recorded in `KB_AMALGAMATION_STATUS.md`). **The r427 recovery note was wrong on one point** — the crashed session had run §3 steps 5 AND 6 (probe, scoped "
         "regeneration, scoped ship PASS, the full gates, selftests, index, miner — all in `outputs/_s33_r427_*`, 12:31 → 12:52) and only step 7 was missing; the corpus on "
         "disk was the r427 ON state. Round 1 = r427 finished at step 7 (no regeneration, nothing re-proven); then the miner's queue, the intake §7 items, the lanes. "
         "Plateau 0 of 3; ledger scoped #2 since the intake FULL. The verbatim health-check narrative: LOOP_STATE_ARCHIVE.md 'Session 34 start note (verbatim)'.")
lines[i17[0]] = s33
lines.insert(i17[0] + 1, short)
st = "\n".join(lines)
# trim the STOPPED entry to <= 1500
i = st.index("## >>> STOPPED 2026-09-22 ≈16:15 NZST (session 34)")
j = st.index("<<<", i) + 3
entry = st[i:j]
trimmed = ("## >>> STOPPED 2026-09-22 ≈16:15 NZST (session 34) on §4 EXHAUSTION — declared WITH the miner's queue quoted: `DIFF_QUEUE.md` (16:00 today, the r429 corpus "
           "= the CURRENT corpus) = 196 CANDIDATE rows, every one dispositioned (r427 → r429 added no structural class; the inquiry rows shipped as r428 / r429; #4235, "
           "#4196, F7 / F15 declined today); KB §D no NOT CAPTURED row ≥ 20 pages; the dashboard rebuilt on r428 (coverage 50.7 %; the largest un-built shape among the "
           "50 intake modules 11 sites); the intake's §7 list and the Follow-up candidates dispositioned; every §4 lane tried this session (the miner's rows, the KB queue, "
           "the widget census, recognition, per-family registry rows — r429, the loss ledger 46.94pp). Five rounds in 2 h 25: **r427 FINISHED** (the chip deltas, "
           "recovered at §3 step 7 — gate-neutral) · **r428 THE INQUIRY-TEMPLATE FALLBACK SHELL** (17 modules, +0.2062pp, ≥50 +5, cs exact +59; three gate-tool "
           "corrections) · Round 3 a PICK pass · **r429 the r100 opener robustness + the TWHR9 row** (11 modules, +0.0135pp; TWHR907 named) · Round 5 a PICK pass "
           "(the panel-title level declined). Skeleton **54.1406 → 54.3603 %** (+0.2197pp; 59.6 % of the 91.2 % ceiling), ≥50 1531 → 1536, ≥75 254, ≥90 23, RAW "
           "38.069 → 38.225; cs exact 15372 → 15442; every other gate EXACT; 49 selftests GREEN; no compaction. Plateau 1 of 3. Build 260620.02; ledger scoped #4. "
           "NEEDS CHRIS: the \"Needs Chris\" list (#4 the quiz engines, the largest lever). Tree clean at the stop commit. <<<")
assert len(trimmed) <= 1500, len(trimmed)
st = st[:i] + trimmed + st[j:]
assert "## Session 34 start note (verbatim)" not in ar
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n## Session 34 start note (verbatim, archived from LOOP_STATE.md 2026-09-22 ≈16:20 NZST, session 34 §5d condense at the stop)\n\n" + s34 + "\n")
wr(R + "LOOP_STATE.md", st)
print("ok", len(st.encode("utf-8")), "bytes; STOPPED", len(trimmed))
