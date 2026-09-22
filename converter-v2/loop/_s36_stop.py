#!/usr/bin/env python3
"""Session 36 — the Round 6 / 7 PICK-pass record and the STOPPED entry (§4 EXHAUSTION, every lane tried).
Run under WSL: python3 _s36_stop.py"""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")

# 1. the Round-log lines for the two PICK passes
o = "- s36-r5 (NO engine change — DECLINED on measurement"; assert st.count(o) == 1
lines = ("- s36-r7 (no engine change, 23 Sept ≈02:55 → 03:15) · PICK PASS — A NEW INSTRUMENT, THE ACTIVITY-BOX BOUNDARY "
         "(`_s36_r7_actbound.py`, `_s36_r7_shift.py`): the r436 ledger's largest addressable non-chrome family is container-shift "
         "(3.83pp). Title-matched activity boxes, paired: **4,617** — Claude's box holds MORE on 2,410 (387 modules), LESS on 1,572 "
         "(347), the same count with different content on 392, identical on 243. Diffuse by construction — no shape at the floor. The "
         "clean off-by-one slice (equal count, exactly ONE element swapped) is **184 boxes**, and its top pattern (gold `p`@last ↔ "
         "Claude `p`@last, 108 boxes / 79 modules) decomposes into the un-built-widget placeholder text against the human's own "
         "description (the D10-3 build gap) and editorial rewording deeper in the string (curly vs straight quotes, a reworded tail) — "
         "class C both ways. NOTHING AT THE FLOOR; the instrument is kept for the next session.\n"
         "- s36-r6 (no engine change, 23 Sept ≈02:00 → 02:55) · PICK PASS — the three §4 lanes this session had not used. **The loss "
         "ledger** re-run on the r436 corpus (`_s36_r6_ledger.out`): total 46.62pp (46.85 at the s35 stop — this session's four rounds "
         "took 0.23pp off it); the families are wrapper-empty 7.04 / chrome 5.37 / alignment-residue 5.08 / editorial-gold 3.94 / "
         "editorial-claude 3.57, and every decomposable row inside them is already dispositioned (chrome's biggest, `MISSING "
         "module-menu li` 0.68pp, is r436's KB-override class; wrapper-empty's are the `<br>` soft-break (s27 closed), the journal "
         "button (Needs Chris #5) and the image build backlog (s24)). Bilingual is still the worst family at 63.68pp = the quiz "
         "engines (Needs Chris #4). **Recognition / no-build**: the new panel census (`_s36_r6_panelfree.py`) found 20 pages / 20 "
         "modules where the gold has inquiry / fundamentals panels and Claude built NONE — but 8 of them (CEDR201 / 301 / 302, CEDT201 "
         "/ 202 / 203 / 204, CEDW303) have a 146–190-line UNFILLED Writers Template ('Brief introductory text to pique student "
         "interest', '[H2] Lesson # and title'): NO SOURCE, the gold was built from content that never reached the WT. 5 more are the "
         "dual-build pairing group (BLL240, CEDK501, CEDT207, CEDT301, MXFUN01 — Needs Chris #6); the remaining 7 are scattered "
         "singles, below the 10-module chrome floor. Also measured and dismissed: the sentence-that-resolved-to-a-tag class "
         "(`_s36_r6_sentencetag.py`) — 5,657 long bracket fragments resolve by the normaliser's embedded fallback and virtually all "
         "are legitimate widget invocations; only ~7 corpus-wide are CEDR302-style directives, so its 89-element menu is a single-module "
         "outlier. **The widget census**: the dashboard rebuilt on the r436 corpus (`_s36_r6_dashboard_run.sh`) — coverage 50.7 %, "
         "every un-built SHAPE still ≤ 13 sites, the big populations (dragAndDrop 930 boxes, clickDrop 347, accordion 293) are the "
         "quiz-engine / D10-3 question. NOTHING AT THE FLOOR in any of the three.\n")
st = st.replace(o, lines + o)

# 2. the STOPPED entry
o = "## >>> STOPPED 2026-09-22 ≈19:40 NZST (session 35)"; assert st.count(o) == 1
stopped = ("## >>> STOPPED 2026-09-23 ≈03:20 NZST (session 36) on §4 EXHAUSTION — WITH the miner's queue quoted (`DIFF_QUEUE.md` 00:43 on "
           "the r436 corpus = the CURRENT corpus, 196 CANDIDATE rows) and **EVERY §4 LANE TRIED**: the miner's rows (→ r434 shipped, r437 "
           "declined), the KB queue (§D has no NOT CAPTURED row ≥ 20 derivable; KB HEAD 3d0d646 unchanged all session), per-family "
           "registry rows / §1d exception 1 (→ r433, r434), the widget census (dashboard rebuilt on r436: coverage 50.7 %, every un-built "
           "shape ≤ 13 sites), recognition / no-build (20 no-shell pages decomposed: 8 UNFILLED Writers Templates = no source, 5 the "
           "dual-build pairing group, 7 scattered singles), and the loss ledger (46.62pp, down 0.23 this session; every decomposable row "
           "dispositioned) — PLUS three NEW instruments this session (the menu-overrun content read → r435 / r436, the menu section-child "
           "census → the r437 decline, the activity-box boundary census → 4,617 paired boxes, diffuse, nothing at the floor). **FOUR ROUNDS "
           "SHIPPED in 5.5 h: r433** the MXFUN code-content phase dialect + THE FULL-REGENERATION BACKSTOP (+0.0090pp, the corpus's three "
           "lowest pages fixed) · **r434** the ARFUN phase-tile labels + the title-bar payload ownership (+0.0039pp) · **r435** the lesson "
           "menu ends at the writer's `[Body]` (+0.0230pp) · **r436** the lesson continuation page inherits its lesson's menu (+0.0498pp) — "
           "the Round-log lines carry each one. Plus TWO recorded verdicts: **r437** the menu's section content is a list — built, probed, "
           "DECLINED and reverted; and the repeated module-overview menu (126 pages / 30 modules) DECLINED as a named pre-KB override. "
           "Skeleton **54.5220 → 54.6077 %** @ 2491 (+0.0857pp; 59.9 % of achievable), ≥50 1546 → 1549, ≥75 256, RAW 38.358 → 38.418; cs "
           "exact 15462 → 15576 (+114); one named acceptance (r435's MXS1004 missing +1); 49 selftests GREEN every round; no compaction. "
           "Plateau 0 of 3. Build 260620.09; **ledger scoped #3 since the r433 FULL (5 of headroom)**. THE MODULE-MENU CHROME REGION IS NOW "
           "DISPOSITIONED END TO END. NEEDS CHRIS: the \"Needs Chris\" list (#4 the quiz engines — still the largest lever at 844 boxes; #6 "
           "the dual-build pairing). Tree clean at the stop commit. <<<\n\n")
st = st.replace(o, stopped + o)
wr(R + "LOOP_STATE.md", st)
print("stop record OK")
