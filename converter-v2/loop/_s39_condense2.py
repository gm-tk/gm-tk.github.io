#!/usr/bin/env python3
"""Session 39 §5d condense #2 of LOOP_STATE.md (97.6 KB after r440's finalise, near the 100 KB target) —
nothing deleted, everything moved verbatim to LOOP_STATE_ARCHIVE.md with a pointer left in place.

Three moves:
  1. The r440 PICK text kept inside the Position's "No round in flight" bullet -> archive; the bullet is trimmed.
  2. The session-37 STOPPED entry (superseded by the session-38 decisions and session 39's rounds) -> archive, pointer heading.
  3. The "Next session starts with" line (2,496 chars, over the §5d 800 cap) -> archive; replaced with a current one.
"""
import io, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE = os.path.join(ROOT, 'LOOP_STATE.md')
ARCH = os.path.join(ROOT, 'LOOP_STATE_ARCHIVE.md')
src = io.open(STATE, encoding='utf-8', newline='').read()
lines = src.split('\n')
before = len(src.encode('utf-8'))
n_sec = sum(1 for l in lines if l.startswith('## '))
blocks = []


def one(pred, what):
    hits = [i for i, l in enumerate(lines) if pred(l)]
    if len(hits) != 1:
        sys.exit('ABORT: %s matched %d lines' % (what, len(hits)))
    return hits[0]


# 1 ---------------------------------------------------------------------------------------------------
i = one(lambda l: l.startswith('- **No round in flight** (23 Sept 2026 ≈16:40'), 'position bullet')
cut = lines[i].find(' The r440 PICK, as written before its edits')
if cut < 0:
    sys.exit('ABORT: r440 PICK marker text not found')
blocks.append(('Round 440 PICK as written before its edits (verbatim, s39 §5d condense #2a)', lines[i][cut:].strip()))
lines[i] = (lines[i][:cut] + " The r440 PICK text (written before its edits, per §3 step 1) -> LOOP_STATE_ARCHIVE.md "
            "'Round 440 PICK as written before its edits (verbatim, s39 §5d condense #2a)'.")

# 2 ---------------------------------------------------------------------------------------------------
j = one(lambda l: l.startswith('## >>> STOPPED 2026-09-23 ≈09:00 NZST (session 37)'), 's37 STOPPED')
blocks.append(('STOPPED entry, session 37 (verbatim, s39 §5d condense #2b)', lines[j]))
lines[j] = ("## STOPPED entry, session 37 (23 Sept ≈09:00, §4 EXHAUSTION, miner quoted; four rounds, all DECLINED; five "
            "instrument faults fixed; Needs Chris #4 re-sized to 1,935 boxes) -> LOOP_STATE_ARCHIVE.md 'STOPPED entry, "
            "session 37 (verbatim, s39 §5d condense #2b)'. Superseded: session 38 answered every Needs-Chris item, and "
            "session 39 shipped r439 / r440 from them.")

# 3 ---------------------------------------------------------------------------------------------------
k = one(lambda l: l.startswith('**Next session starts with:**'), 'next-session line')
blocks.append(('"Next session starts with" line as left by sessions 37 / 38 (verbatim, s39 §5d condense #2c)', lines[k]))
lines[k] = ("**Next session starts with:** (interim — session 39 in progress; rewritten at its stop) the standing "
            "`/loop-start`. LAST SHIPPED r440 (260620.11); census 552 / 545 / 2,666 / 2,470 pairs; ledger scoped #5 since "
            "the r433 FULL; plateau 0 of 3. The D13 order continues: D13-12 (data only), D13-8, D13-14 + 15 + 11, D13-2, "
            "D13-9, D13-5, the D13-4 answer-key carry-through, D13-7 at the next FULL, then the D13-4 quiz builds "
            "(multiChoiceQuiz first). The claude-audit kickoff's Phases 3 / 3b / 4 are unstarted Chris-approved work.")

out = '\n'.join(lines)
with io.open(ARCH, 'a', encoding='utf-8', newline='') as fh:
    for h, b in blocks:
        fh.write('\n\n## %s\n\n%s\n' % (h, b))
tmp = STATE + '.tmp'
io.open(tmp, 'w', encoding='utf-8', newline='').write(out)
if os.path.getsize(tmp) < 50000:
    sys.exit('ABORT: suspiciously small')
os.replace(tmp, STATE)
after = len(out.encode('utf-8'))
print('LOOP_STATE.md %d -> %d bytes (-%d) [%s]; ## sections %d -> %d' % (
    before, after, before - after, datetime.datetime.now().strftime('%H:%M'), n_sec,
    sum(1 for l in out.split('\n') if l.startswith('## '))))
