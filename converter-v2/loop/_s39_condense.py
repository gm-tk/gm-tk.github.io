#!/usr/bin/env python3
"""Session 39 §5d condense of LOOP_STATE.md (114.8 KB at the start, over the 100 KB target) —
nothing deleted, everything moved verbatim to LOOP_STATE_ARCHIVE.md with a pointer left in place.

Five moves:
  1. Session 36 / 37 start notes (2 long lines) -> archive, one pointer line.
  2. The session-36 STOPPED entry (superseded by s37's and by the s38 decisions) -> archive, pointer heading.
  3. The 17 Round-log lines of sessions 30-34 -> archive, one pointer line after the s27-s29 pointer.
  4. The LAST SHIPPED tail r435 / r434 / r433 verbatim gate rows -> archive, pointer kept.
  5. The two long Declined-classes entries s37-r3 / s37-r2 -> archive, condensed in place (verdict,
     the never-re-open condition and the scripts kept).
"""
import io, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(ROOT)  # FINAL_MODULE_DATA
STATE = os.path.join(ROOT, 'LOOP_STATE.md')
ARCH = os.path.join(ROOT, 'LOOP_STATE_ARCHIVE.md')

src = io.open(STATE, encoding='utf-8', newline='').read()
if '\r\n' in src:
    sys.exit('ABORT: CRLF in LOOP_STATE.md')
lines = src.split('\n')
before = len(src.encode('utf-8'))
n_sections_before = sum(1 for l in lines if l.startswith('## '))

archive_blocks = []


def find_line(pred, what):
    hits = [i for i, l in enumerate(lines) if l is not None and pred(l)]
    if len(hits) != 1:
        sys.exit('ABORT: %s matched %d lines, expected 1' % (what, len(hits)))
    return hits[0]


# ---- 1. session start notes 36 / 37 -----------------------------------------
i36 = find_line(lambda l: l.startswith('**Session 36 started:**'), 's36 start note')
i37 = find_line(lambda l: l.startswith('**Session 37 started:**'), 's37 start note')
if i37 != i36 + 1:
    sys.exit('ABORT: s36 / s37 start notes not consecutive')
archive_blocks.append(('Session start notes 36 / 37 (verbatim, s39 §5d condense #1)',
                       lines[i36] + '\n\n' + lines[i37]))
lines[i36] = ("**Session start notes 36 / 37** -> LOOP_STATE_ARCHIVE.md 'Session start notes 36 / 37 "
              "(verbatim, s39 §5d condense #1)'. One line each: **s36** 22 Sept 21:37, clean start at "
              "1cc1b36, r433 (the FULL backstop) → r436 shipped, then §4 EXHAUSTION; **s37** 23 Sept ≈06:50, "
              "clean start at 94c3c03, four rounds all DECLINED (r438 built and reverted), §4 EXHAUSTION with "
              "five instrument faults fixed. Every figure in them is superseded by the Position section below.")
lines[i37] = None

# ---- 2. the session-36 STOPPED entry ----------------------------------------
s36 = find_line(lambda l: l.startswith('## >>> STOPPED 2026-09-23 ≈03:20 NZST (session 36)'), 's36 STOPPED')
archive_blocks.append(('STOPPED entry, session 36 (verbatim, s39 §5d condense #2)', lines[s36]))
lines[s36] = ("## STOPPED entry, session 36 (23 Sept ≈03:20, §4 EXHAUSTION, miner quoted; r433–r436 shipped) "
              "-> LOOP_STATE_ARCHIVE.md 'STOPPED entry, session 36 (verbatim, s39 §5d condense #2)'. "
              "Superseded by the session-37 entry above and by the session-38 decisions.")

# ---- 3. the Round-log lines of sessions 30-34 --------------------------------
prefixes = ['- s34-r4 (', '- s34-r3 (', '- s34-r2 (', '- s33-r5 / s34-r1 (', '- s33-r4 (',
            '- s33-r3 (', '- s33-r2 (', '- s33-r1 (', '- s31-r3 (', '- s31-r2 (', '- s31-r1 (',
            '- s30-r1 (', '- s30-r6 (', '- s30-r5 (', '- s30-r4 (', '- s30-r3 (', '- s30-r2 (']
rl = [find_line(lambda l, p=p: l.startswith(p), p) for p in prefixes]
archive_blocks.append(('Round-log lines s30–s34 (verbatim, s39 §5d condense #3)',
                       '\n'.join(lines[i] for i in rl)))
for i in rl:
    lines[i] = None
p29 = find_line(lambda l: l.startswith('- s27–s29 round-log lines'), 's27-s29 pointer')
lines[p29] = (lines[p29] + '\n'
              + "- s30–s34 round-log lines (17 lines, sessions 30–34: engine r419–r429, r425 built inert then "
                "finished, r422 enabled, the 22 Sept Round 0d of the 38) → LOOP_STATE_ARCHIVE.md "
                "'Round-log lines s30–s34 (verbatim, s39 §5d condense #3)'.")

# ---- 4. the LAST SHIPPED tail r435 / r434 / r433 -----------------------------
li = find_line(lambda l: l.startswith('- LAST SHIPPED: **r436**'), 'LAST SHIPPED line')
ls = lines[li]
cut = ls.find('Before it **r435**')
keep_from = ls.find('The verbatim r432 / r431 / r430 / r429')
if cut < 0 or keep_from < 0 or keep_from < cut:
    sys.exit('ABORT: cannot locate the r435 / r432 split points in the LAST SHIPPED line')
archive_blocks.append(('Position — LAST SHIPPED tail r435 / r434 / r433 (verbatim, s39 §5d condense #4)',
                       ls[cut:keep_from].strip()))
lines[li] = (ls[:cut]
             + "The verbatim r435 / r434 / r433 gate rows (r435 +0.0230pp the lesson menu ends at the "
               "writer's `[Body]`; r434 +0.0039pp the ARFUN phase-tile labels + the title-bar payload; r433 "
               "+0.0090pp the MXFUN code-content dialect + THE FULL BACKSTOP — LAST FULL = r433) -> "
               "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail r435 / r434 / r433 (verbatim, s39 §5d "
               "condense #4)'. "
             + ls[keep_from:])

# ---- 5. the two long Declined-classes entries --------------------------------
d3 = find_line(lambda l: l.startswith("- **Session 37 Round 3 (23 Sept ≈08:30) — THE FOOTER'S NAVIGATION"), 'decl s37-r3')
d2 = find_line(lambda l: l.startswith('- **Session 37 Round 2 (23 Sept ≈07:50) — THE WIDGET TYPE'), 'decl s37-r2')
archive_blocks.append(('Declined classes s37-r3 / s37-r2, full text (verbatim, s39 §5d condense #5)',
                       lines[d3] + '\n' + lines[d2]))
lines[d3] = ("- **Session 37 Round 3 (23 Sept ≈08:30) — THE FOOTER'S NAVIGATION LINK SET (miner chrome rows "
             "F26 / F27 / F29 / F30, ranked #4–#5) — DECLINED: no discriminator; the rates already match.** "
             "With two instrument faults fixed (strip HTML comments — the gold comments a Next link out; "
             "`home-nav` is a CLASS): 2,497 pairs, 90.3 % agree; the last page's gold is split (prev-only 0.76) "
             "and Claude already sits at 0.79 — the rates match, the per-page assignment has no discriminator "
             "(the r437 precedent); 48 of the 128 Claude-Next pages are Needs Chris #6 page counts; the largest "
             "coherent miss is 8 CEDT modules, under the chrome floor. The 175 empty-Claude-menu pages: 88 the "
             "s36 KB override, 44 gold-invented, 43 / 22 modules derivable but every sub-shape below floor. "
             "Scripts `_s37_r3_footer*.py`, `_s37_r3_single.py`, `_s37_r3_nomenu.py`. Full text → archive "
             "'Declined classes s37-r3 / s37-r2, full text (verbatim, s39 §5d condense #5)'.")
lines[d2] = ("- **Session 37 Round 2 (23 Sept ≈07:50) — THE WIDGET TYPE THE WRITER NAMED IN THE FREE TEXT "
             "(engine r438) — DECLINED on measurement; built, probed, REVERTED.** The raw-WT 700-character "
             "census (flip card 67 boxes / 35 modules at 0.836) was a five-fold over-count: on the text the "
             "scanner actually sees the population is 15 pages / 7 modules, under both floors. Keep: free-text "
             "alias matching false-positives on prose (`memory` out of instruction text), so any future form must "
             "be type-scoped AND positionally guarded; classifying is not building (the un-paired table form "
             "stays a placeholder and the type change shifted activity ownership — TEFUN03). Reverted "
             "byte-identical, `_content_manifest.py fresh` 0 truly stale; recorded in "
             "`Interactive_Boundary_ChildTag_Bank.json` `unclassified_activity_lead._declined_r438_free_text_type`. "
             "**Never re-open without BOTH a census over the SCANNER'S OWN text and a builder that can read a "
             "face table.** Scripts `_s37_r2_unclass.py`, `_s37_r2_flip.py`. Full text → the same archive block.")

# ---- write ------------------------------------------------------------------
out = '\n'.join(l for l in lines if l is not None)
n_sections_after = sum(1 for l in out.split('\n') if l.startswith('## '))
stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
with io.open(ARCH, 'a', encoding='utf-8', newline='') as fh:
    for head, body in archive_blocks:
        fh.write('\n\n## %s\n\n%s\n' % (head, body))
tmp = STATE + '.tmp'
io.open(tmp, 'w', encoding='utf-8', newline='').write(out)
if os.path.getsize(tmp) < 50000:
    sys.exit('ABORT: condensed file suspiciously small')
os.replace(tmp, STATE)
after = len(out.encode('utf-8'))
print('LOOP_STATE.md %d -> %d bytes (-%d)  [%s]' % (before, after, before - after, stamp))
print('archived %d blocks; ## sections %d -> %d' % (len(archive_blocks), n_sections_before, n_sections_after))
