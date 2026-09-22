#!/usr/bin/env python3
"""Session 34 STOP (§4 EXHAUSTION, 22 Sept 2026 ≈16:15 NZST): the Round 5 PICK-pass line, the panel-title decline under Declined
classes, the STOPPED entry (≤ 1,500 characters) at the top of the STOPPED entries, the r429 follow-up line dispositioned, the
next-session line. Run under WSL: python3 _s34_stop.py
"""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md")

# Round 5 PICK-pass line in the Round log
o = "- s34-r4 (engine r429, build 260620.02"; assert st.count(o) == 1
line = ("- s34-r5 (no engine change, 22 Sept ≈16:05 → 16:12) · PICK PASS — the r429 follow-up measured: THE INQUIRY PANEL'S FIRST-HEADING LEVEL BY FAMILY "
        "(`_s34_r5_paneltitle.py` / `.log`): the gold's panel first heading is h2 233 / h3 119 / h4 14 (0.63 h2 overall; BLL2 0.86, CEDW 0.90, CEDO 0.74, "
        "TWHA 0.72, EXPFUN 0.72, CEDT 0.68 — the r385 rule holds); no family reaches h3 ≥ 0.60 (CEDR 0.58, BLL1 0.55, TWHR 0.56 n = 9, TWHK / CEDK mixed "
        "three ways); 33 pages mismatch in BOTH directions → DECLINED. The 16:00 queue = the 15:03 queue (no new or gone candidate class). §4 EXHAUSTION.\n")
st = st.replace(o, line + o)

# the decline under Declined classes
o = "- **Session 34 Round 2 PICK pass (22 Sept ≈14:00) — #4235"; assert st.count(o) == 1
st = st.replace(o, ("- **Session 34 Round 5 PICK pass (22 Sept ≈16:05) — the inquiry panel's first-heading level by family (the r429 follow-up) — DECLINED on "
                    "measurement (`_s34_r5_paneltitle.py` / `.log`).** Over every paired gold page with `div.inquiryPanel` (56 modules): the panel's first heading is "
                    "h2 233 / h3 119 / h4 14 / none 18 — h2 at 0.63 overall and ≥ 0.68 in BLL2 / CEDW / CEDO / TWHA / EXPFUN / CEDT; no family reaches h3 ≥ 0.60 "
                    "(CEDR 14 / 24 = 0.58, BLL1 27 / 50 = 0.55, TWHR 5 / 9, TWHT 3 / 5; CEDK and TWHK split three ways with h4); the 33 mismatching pages run both "
                    "ways (EXPFUN gold h3 / Claude h2 9 panels, BLL2 gold h2 / Claude h3 8, BLL1 7, CEDK h4 / h2 7). The r385 h2 promotion stands; TWHR907's −5.4 (r429) "
                    "is a named page, not a family rule.\n" + o))

# the follow-up line → dispositioned
o = "- **(r429) The panel's first-heading level by family.**"; assert st.count(o) == 1
st = st.replace(o, "- **(r429, DECLINED s34-r5 — see Declined classes) The panel's first-heading level by family.**")

# the STOPPED entry at the top of the STOPPED entries
o = "\n## >>> STOPPED 2026-09-21 ≈22:00 NZST (session 31)"; assert st.count(o) == 1
stopped = ("\n## >>> STOPPED 2026-09-22 ≈16:15 NZST (session 34) on §4 EXHAUSTION — declared WITH the miner's queue quoted: `DIFF_QUEUE.md` (16:00 today, "
           "the r429 corpus = the CURRENT corpus) = 196 CANDIDATE rows, every one dispositioned (the r427 → r429 diffs added no structural class; the inquiry rows "
           "shipped as r428 / r429, #4235 / #4196 / F7 / F15 declined this session); KB §D no NOT CAPTURED row ≥ 20 pages; the dashboard rebuilt on r428 "
           "(coverage 50.7 %, the largest un-built shape among the 50 intake modules 11 sites); the intake's §7 list and the Follow-up candidates dispositioned "
           "(the r428 / r429 items: CEDO402's `[Side Tabs]` shell 1 module; the panel-title level DECLINED); every §4 lane tried this session — the miner's rows, "
           "the KB queue, the widget census by content, recognition (the 7 no-source), per-family registry rows (r429), the loss ledger (46.94pp; Bilingual = the "
           "quiz-engine types). Five rounds in 2 h 25: **r427 FINISHED** (the code-prefix chip deltas, recovered at §3 step 7 from the session-33 crash — gate-neutral) · "
           "**r428 THE INQUIRY-TEMPLATE FALLBACK SHELL** (17 modules, +0.2062pp, ≥50 +5, cs exact +59; three gate-tool corrections) · Round 3 a PICK pass · "
           "**r429 the r100 opener robustness + the TWHR9 row** (11 modules, +0.0135pp, cs exact +11; TWHR907 named) · Round 5 a PICK pass. Skeleton **54.1406 → "
           "54.3603 %** (+0.2197pp; 59.6 % of the 91.2 % ceiling), ≥50 1531 → 1536, ≥75 254, ≥90 23, RAW 38.069 → 38.225; cs exact 15372 → 15442; every other "
           "gate EXACT; 49 selftests GREEN every round; no compaction. Plateau window 1 of 3. Build 260620.02; ledger scoped #4 since the intake FULL. NEEDS "
           "CHRIS: the open lines of the \"Needs Chris\" section (the quiz-engine decision #4 is the largest lever). Tree clean at the stop commit. <<<\n")
st = st.replace(o, stopped + o)

i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the \"Amended:\" line; "
               "the §7 diff check; `git status` CLEAN at the session-34 stop commit). No round in flight (r429 shipped by session 34 Round 4 — see the Position section). "
               "**The session-34 §4 EXHAUSTION verdict (the STOPPED entry above, the miner quoted on the r429 corpus) stands until NEW evidence:** an intake (§1f), a KB "
               "module rule, a Needs-Chris decision (the quiz-engine types #4 — 844 boxes, the largest lever; the 12 lesson-menu repeaters; the dual-build pairing), "
               "or a lane no session has tried. If a session runs anyway, start with the three cheapest re-checks: CEDO402's `[Side Tabs]`-widget shell (1 module — a "
               "sixth Inquiry dialect if TWHR905 / CEDW303 share it), the r100 mode's three labelled openers TWHA902's scanner swallows (4 / 9 panels), and the miner's "
               "196 rows re-read on the r429 corpus. NEEDS CHRIS: the open lines of the \"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("stop OK", len(stopped))
