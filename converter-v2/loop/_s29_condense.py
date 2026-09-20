#!/usr/bin/env python3
"""Session 29 §5d condense of LOOP_STATE.md (20 Sept 2026).

Moves, verbatim, to LOOP_STATE_ARCHIVE.md:
  (a) the ten 'Decisions from Chris' blocks for sessions 14-25 (each a standing-kickoff-only record)
  (b) the two 'Session 27 - Round 3 / Round 4 PICK pass' sections
and replaces each group in LOOP_STATE.md with a one-paragraph summary. Nothing is deleted.
"""
import re, sys, datetime
ROOT = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/'
STATE = ROOT + 'LOOP_STATE.md'
ARCH = ROOT + 'LOOP_STATE_ARCHIVE.md'
stamp = '2026-09-20 session 29 §5d condense'

lines = open(STATE, encoding='utf-8').read().split('\n')
n = len(lines)

def find(prefix, start=0):
    for i in range(start, n):
        if lines[i].startswith(prefix):
            return i
    raise SystemExit('heading not found: ' + prefix)

# (a) decisions sessions 25 .. 14 : from the s25 heading up to (not incl.) the session-10 heading
a0 = find('## Decisions from Chris (session 25')
a1 = find('## Decisions from Chris (session 10')
assert a0 < a1
dec_block = lines[a0:a1]
sessions = re.findall(r'^## Decisions from Chris \(session (\d+)', '\n'.join(dec_block), re.M)
assert sessions == ['25', '24', '23', '21', '19', '18', '17', '16', '15', '14'], sessions

# (b) session 27 round 3 / round 4 PICK passes : from the R3 heading to (not incl.) '## Round log'
b0 = find('## Session 27 — Round 3 PICK pass')
b1 = find('## Round log')
assert b0 < b1
pick_block = lines[b0:b1]
assert any(l.startswith('## Session 27 — Round 4 PICK pass') for l in pick_block)

summary_a = [
    "## Decisions from Chris (sessions 14–25 — 2026-09-16 23:30 → 2026-09-18 ≈20:40 NZST) → LOOP_STATE_ARCHIVE.md 'Decisions from Chris sessions 14–25 (verbatim, archived at the " + stamp + ")'. Every one of the ten sessions (14, 15, 16, 17, 18, 19, 21, 23, 24, 25) held ONLY the standing §7 `/loop-start` kickoff (12 rounds or 10 hours; the miner mandatory from s19, its PICK chrome-first; the sessions 15–18 exhaustion verdicts void; `REGENERATE CORPUS` scoped by §0a / §0b; RUN UNINTERRUPTED; the §6 context diet; commit after every round, never push) and, in s14 / s19 / s23, the standing `/loop-stop` message (finish-and-commit if provable in ≤ 10 minutes, else toggle OFF and describe; record decisions; \"Next session starts with:\"; the §5 report; no push). **No numbered decision was asked or given in any of them**; every D10-1…D10-9 decision stood, nothing re-asked. Applied stops: s14 r350 finalised + committed at the stop (≈15 min, judged right); s19 Round 6 already committed, Round 7 had no code; s23 the r376 commit already in. The one optional question raised (s17 / s18: does D10-3 extend to the quiz-engine types — multiChoiceQuiz first) is still open and still not a block. The needs-Chris items those sessions queued (the journal button; the dual-build gold dirs' pairing; the activity-number provenance round; the 12 empty-lesson-menu repeaters; the speech bubble's character image) are the five in the session-26 STOPPED entry (archive: 'STOPPED entry, session 26').",
    "",
]
summary_b = [
    "## Session 27 — Round 3 + Round 4 PICK passes (no engine change; 19 Sept ≈10:55 → 12:35 NZST) → LOOP_STATE_ARCHIVE.md 'Session 27 — Round 3 / Round 4 PICK passes (verbatim, archived at the " + stamp + ")'. R3: eight classes measured on the r399 corpus, none at the floor (`_s27_r3_alerttag.py` / `_sidepad.py` / `_imgside.py` / `_headprefix.py` / `_grid2.py` / `_h4.py` / `_emptyalert.py` / `_alerthead.py`). R4: the D10-3 build lane measured to its floor (dragAndDrop 795 declines / 663 signatures; no type has an un-built dialect ≥ 20 sites) and the `<br>` follow-up CLOSED (`_s27_r4_brseries.py` / `_goldbr.py` / `_brjoin.py`). The one-line summaries are the s27-r3 / s27-r4 Round-log lines below.",
    "",
]

new_lines = lines[:a0] + summary_a + lines[a1:b0] + summary_b + lines[b1:]

arch_add = [
    "",
    "## Decisions from Chris sessions 14–25 (verbatim, archived at the " + stamp + ")",
    "(moved verbatim from LOOP_STATE.md lines %d–%d on %s; the summary that replaced them is in LOOP_STATE.md)" % (a0 + 1, a1, datetime.date.today().isoformat()),
    "",
] + dec_block + [
    "",
    "## Session 27 — Round 3 / Round 4 PICK passes (verbatim, archived at the " + stamp + ")",
    "(moved verbatim from LOOP_STATE.md lines %d–%d on %s)" % (b0 + 1, b1, datetime.date.today().isoformat()),
    "",
] + pick_block

with open(ARCH, 'a', encoding='utf-8') as f:
    f.write('\n'.join(arch_add).rstrip('\n') + '\n')
open(STATE, 'w', encoding='utf-8', newline='\n').write('\n'.join(new_lines))
import os
print('LOOP_STATE.md', n, '->', len(new_lines), 'lines;', os.path.getsize(STATE), 'bytes; archive', os.path.getsize(ARCH), 'bytes')
print('moved: decisions lines %d-%d (%d), pick passes lines %d-%d (%d)' % (a0 + 1, a1, len(dec_block), b0 + 1, b1, len(pick_block)))
