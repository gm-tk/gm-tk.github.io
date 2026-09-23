#!/usr/bin/env python3
"""Session 39 §5d condense #3 of LOOP_STATE.md (95.5 KB after r443) — nothing deleted, everything moved verbatim to
LOOP_STATE_ARCHIVE.md with a pointer left in place.

Three moves inside the Position section:
  1. LAST SHIPPED: the verbatim gate rows of r442 … r436 (everything from 'Before it **r442**' to the r432 pointer)
     -> archive; a one-line summary per round stays.
  2. Plateau window: every reading older than r440 -> archive; the current window statement stays.
  3. Standing facts: the AppVersion history older than 260620.09 -> archive; the recent builds stay.
"""
import io, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE = os.path.join(ROOT, 'LOOP_STATE.md')
ARCH = os.path.join(ROOT, 'LOOP_STATE_ARCHIVE.md')
src = io.open(STATE, encoding='utf-8', newline='').read()
lines = src.split('\n')
before = len(src.encode('utf-8'))
blocks = []


def one(pred, what):
    h = [i for i, l in enumerate(lines) if pred(l)]
    if len(h) != 1:
        sys.exit('ABORT: %s matched %d' % (what, len(h)))
    return h[0]


def cut_between(i, start_marker, end_marker, title, replacement):
    l = lines[i]
    a = l.find(start_marker)
    b = l.find(end_marker, a + 1) if end_marker else len(l)
    if a < 0 or b < 0 or b <= a:
        sys.exit('ABORT: markers not found for %s' % title)
    blocks.append((title, l[a:b].strip()))
    lines[i] = l[:a] + replacement + (l[b:] if end_marker else '')


i = one(lambda l: l.startswith('- LAST SHIPPED: **r443**'), 'LAST SHIPPED')
cut_between(i, 'Before it **r442**', 'The verbatim r435 / r434 / r433 gate rows',
            'Position — LAST SHIPPED tail r442 / r441 / r440 / r439 / r436 (verbatim, s39 §5d condense #3a)',
            'Before it (verbatim gate rows -> LOOP_STATE_ARCHIVE.md \'Position — LAST SHIPPED tail r442 / r441 / r440 / '
            'r439 / r436 (verbatim, s39 §5d condense #3a)\'): **r442** (260620.13, +0.0642pp @ 2476, the twelve lesson-menu '
            'repeaters, D13-8, scoped #6); **r441** (260620.12, output-inert, the language labels confirmed, D13-12); '
            '**r440** (260620.11, the dual-build golds, D13-6 — a POPULATION RE-BASE 54.6077 @ 2491 -> 54.7442 % @ 2470, '
            'scoped #5); **r439** (260620.10, gate-neutral, writeFont, the claude-audit Phase 2 finished, scoped #4); '
            '**r436** (260620.09, +0.0498pp, the lesson continuation page inherits its menu, scoped #3). ')

i = one(lambda l: l.startswith('- Plateau window (§4): **0 of 3**'), 'plateau')
cut_between(i, '; r440 is a gate-configuration', ' Read every delta on the post-intake population',
            'Position — plateau readings r440 and older (verbatim, s39 §5d condense #3b)',
            '; r440 and every older reading -> LOOP_STATE_ARCHIVE.md \'Position — plateau readings r440 and older '
            '(verbatim, s39 §5d condense #3b)\' (the last reset before r442 was r435).')

i = one(lambda l: l.startswith('- Standing facts: AppVersion 260620.14'), 'facts')
cut_between(i, '; before it 260620.08 (', '; every toggle is listed in OPERATING_GUIDE.md §11',
            'Position — Standing facts AppVersion history 260620.08 and older (verbatim, s39 §5d condense #3c)',
            '; 260620.08 and every older build -> LOOP_STATE_ARCHIVE.md \'Position — Standing facts AppVersion history '
            '260620.08 and older (verbatim, s39 §5d condense #3c)\'')

out = '\n'.join(lines)
with io.open(ARCH, 'a', encoding='utf-8', newline='') as fh:
    for h, b in blocks:
        fh.write('\n\n## %s\n\n%s\n' % (h, b))
tmp = STATE + '.tmp'
io.open(tmp, 'w', encoding='utf-8', newline='').write(out)
if os.path.getsize(tmp) < 50000:
    sys.exit('ABORT: suspiciously small')
os.replace(tmp, STATE)
print('LOOP_STATE.md %d -> %d bytes (-%d) [%s]' % (before, len(out.encode('utf-8')), before - len(out.encode('utf-8')),
                                                   datetime.datetime.now().strftime('%H:%M')))
