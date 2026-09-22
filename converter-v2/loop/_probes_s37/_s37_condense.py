#!/usr/bin/env python3
"""Session 37 §5d condense of LOOP_STATE.md — nothing deleted, everything moved verbatim
to LOOP_STATE_ARCHIVE.md with a pointer left in place.

Four moves:
  1. Session 27 / 28 / 29 / 30 start notes (4 long lines) -> archive, one pointer line.
  2. The LAST SHIPPED tail r432 / r431 / r430 / r429 verbatim gate rows -> archive, pointer kept.
  3. The s36-r6 Round-log line (2,024 chars, over the 500 cap) -> archive, condensed in place.
  4. The s36-r5 Round-log line (1,249 chars, over the 500 cap) -> archive, condensed in place
     (its full evidence already sits under Declined classes).
"""
import io, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(ROOT)  # FINAL_MODULE_DATA
STATE = os.path.join(ROOT, 'LOOP_STATE.md')
ARCH = os.path.join(ROOT, 'LOOP_STATE_ARCHIVE.md')

src = io.open(STATE, encoding='utf-8').read()
lines = src.split('\n')
before = len(src.encode('utf-8'))

archive_blocks = []


def find_line(pred, what):
    hits = [i for i, l in enumerate(lines) if l is not None and pred(l)]
    if len(hits) != 1:
        sys.exit('ABORT: %s matched %d lines, expected 1' % (what, len(hits)))
    return hits[0]


# ---- 1. session start notes 27 / 28 / 29 / 30 -------------------------------
idx = []
for tag in ('**Session 27 started:**', '**Session 28 (pre-loop',
            '**Session 29 started:**', '**Session 30 started:**'):
    idx.append(find_line(lambda l, t=tag: l.startswith(t), tag))
if idx != sorted(idx) or idx[-1] - idx[0] != 3:
    sys.exit('ABORT: session 27-30 start notes are not four consecutive lines: %r' % idx)

archive_blocks.append(
    ('Session start notes 27 / 28 / 29 / 30 (verbatim, s37 §5d condense #1)',
     '\n\n'.join(lines[i] for i in idx)))

pointer1 = ("**Session start notes 27 / 28 / 29 / 30** -> LOOP_STATE_ARCHIVE.md "
            "'Session start notes 27 / 28 / 29 / 30 (verbatim, s37 §5d condense #1)'. "
            "In one line each: **s27** 19 Sept, the first post-intake session, LOOP_STATE condensed "
            "636->69 KB, miner queue current, plateau 2 of 3 at the start; **s28** 20 Sept, PRE-LOOP "
            "(not a loop session) — Chris's four `NEXT_SESSION__Pre_Loop_Fixes.md` tasks, and the "
            "CORRECTED post-intake census (552 gold dirs / 762 docx) first recorded there; **s29** "
            "20 Sept, r410 finished from the handover then 9 shipped rounds, `verify_after_transfer.sh`'s "
            "three stale expectations fixed; **s30** 21 Sept, clean start, r419-r422. Every figure in "
            "them is superseded by the Position section below.")
lines[idx[0]] = pointer1
for i in idx[1:]:
    lines[i] = None

# ---- 2. the LAST SHIPPED tail ------------------------------------------------
li = find_line(lambda l: l.startswith('- LAST SHIPPED: **r436**'), 'LAST SHIPPED line')
ls = lines[li]
cut = ls.find('Before it **r432**')
keep_from = ls.find('Before it **r428**')
if cut < 0 or keep_from < 0 or keep_from < cut:
    sys.exit('ABORT: cannot locate the r432/r428 split points in the LAST SHIPPED line')
moved = ls[cut:keep_from]
archive_blocks.append(
    ('Position — LAST SHIPPED tail r432 / r431 / r430 / r429 (verbatim, s37 §5d condense #2)',
     moved.strip()))
lines[li] = (ls[:cut]
             + 'The verbatim r432 / r431 / r430 / r429 gate rows (each a SCOPED ship: r432 +0.0972pp '
               'the lesson WALT/SC menu, r431 +0.0630pp the inner-word label over-fire, r430 +0.0015pp '
               'the Inquiry opener part 2, r429 +0.0135pp the r100 opener + TWHR9) -> LOOP_STATE_ARCHIVE.md '
               "'Position — LAST SHIPPED tail r432 / r431 / r430 / r429 (verbatim, s37 §5d condense #2)'. "
             + ls[keep_from:])

# ---- 3 + 4. the two over-cap Round-log lines --------------------------------
r6 = find_line(lambda l: l.startswith('- s36-r6 (no engine change'), 's36-r6 round-log line')
archive_blocks.append(('Round-log line s36-r6, full text (verbatim, s37 §5d condense #3)', lines[r6]))
lines[r6] = ("- s36-r6 (no engine change, 23 Sept ≈02:00 → 02:55) · PICK PASS on the three §4 lanes "
             "s36 had not used — ALL THREE EMPTY AT THE FLOOR. Loss ledger 46.62pp (−0.23 this session), "
             "every decomposable row dispositioned, Bilingual worst at 63.68pp = the quiz engines "
             "(Needs Chris #4). Recognition/no-build: 20 panel-free pages decomposed into 8 UNFILLED "
             "Writers Templates (NO SOURCE), the 5 dual-build pairing modules (#6) and 7 scattered singles. "
             "Widget census: dashboard rebuilt on r436, coverage 50.7 %, every un-built shape ≤ 13 sites. "
             "Full text -> LOOP_STATE_ARCHIVE.md 'Round-log line s36-r6, full text (verbatim, s37 §5d condense #3)'.")

r5 = find_line(lambda l: l.startswith('- s36-r5 (NO engine change'), 's36-r5 round-log line')
archive_blocks.append(('Round-log line s36-r5, full text (verbatim, s37 §5d condense #4)', lines[r5]))
lines[r5] = ("- s36-r5 (NO engine change — DECLINED on measurement, 23 Sept 01:25 → ≈01:50) · PICK PASS "
             "on the miner's module-menu rows #36 / #37 / #49: **THE MODULE MENU'S SECTION CONTENT IS A LIST** "
             "— menu-level dominance 0.945 looked overwhelming but the rule FAILS at the line level "
             "(bold-labelled menu line = gold `<p>` 147 vs `<li>` 29; corpus list share gold 0.772 vs "
             "Claude 0.743). Built, probed (+0.0 SCAFFOLD on all four changed pages), REVERTED. "
             "The evidence and the never-re-open condition are under Declined classes; the full line -> "
             "LOOP_STATE_ARCHIVE.md 'Round-log line s36-r5, full text (verbatim, s37 §5d condense #4)'.")

# ---- write ------------------------------------------------------------------
out = '\n'.join(l for l in lines if l is not None)
stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
with io.open(ARCH, 'a', encoding='utf-8') as fh:
    for head, body in archive_blocks:
        fh.write('\n\n## %s\n\n%s\n' % (head, body))

io.open(STATE, 'w', encoding='utf-8').write(out)
after = len(out.encode('utf-8'))
print('LOOP_STATE.md %d -> %d bytes (-%d)  [%s]' % (before, after, before - after, stamp))
print('archived %d blocks' % len(archive_blocks))
