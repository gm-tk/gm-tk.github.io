#!/usr/bin/env python3
"""Session 27: move the session-26 start note to the archive, write the session-27 start note."""
import io, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOT = os.path.join(ROOT, 'LOOP_STATE.md')
ARC = os.path.join(ROOT, 'LOOP_STATE_ARCHIVE.md')
lines = io.open(HOT, encoding='utf-8').read().split('\n')
i26 = next(i for i, l in enumerate(lines) if l.startswith('**Session 26 started:**'))
i_prev = next(i for i, l in enumerate(lines) if l.startswith('**Sessions 1–24 start notes:**'))
s26 = lines[i26]
note27 = (
    "**Session 27 started:** 2026-09-19 08:42 NZST (Claude Code, Opus 5, on Chris's Windows machine; hard stop 18:42 NZST). "
    "Budget: **12 rounds or 10 hours** (the §7 default — `/loop-start` with no argument). Kickoff: the standing `/loop-start` message "
    "(the miner mandatory, chrome-first; the sessions 15–18 exhaustion verdicts VOID; `REGENERATE CORPUS` scoped by §0a / §0b; §5c never end "
    "the turn to wait; the §6 context diet). Health check: git CLEAN at 975cd27 (the session-26 stop commit; r397 = f944f07 beneath it — nothing "
    "uncommitted, nothing to reconcile); no stale locks; `verify_after_transfer.sh` PASS (symlinks 5/5, engine 62/62 + gates 81/81 byte-identical, "
    "census 2109 pages / 416 modules / 454 gold dirs / 619 docx, both git histories intact); LOOP_STATE.md was 99.6 KB → §5d CONDENSED FIRST to 69 KB "
    "(`_s27_condense.py`: the s19–s25 STOPPED entries, the verbatim D10-1…D10-9 block and the sessions 5–9 decisions moved to the archive, each "
    "summarised in place — no decision deleted). KB repo HEAD d61628c — UNCHANGED since session 26. **The miner check (§1d):** `DIFF_QUEUE.md` "
    "(19 Sept 05:47, the r397 corpus) is NEWER than every Claude page, gold page, docx, engine and data file (0 / 0 / 0 / 0 / 0 newer) → the queue IS "
    "the current corpus's; 173 CANDIDATE rows, all dispositioned. Plateau window 2 of 3 at the start (r396 / r397) — one more sub-0.02pp round with "
    "no protected gate moving = the §4 plateau stop, so Round 1 must be a class the paired census scores ≥ 0.02pp BEFORE regenerating. The ledger is "
    "at scoped #1 since the r396 FULL (7 of headroom). Instrument angle for this session (the s26 'Next session starts with' line): extend the "
    "PAIRED WIDGET / WRAPPER CENSUS (`_s26_r394_clickdrop.py` … `_s26_r397_thb.py`) to hintSlider / tabs / dropbox / TKmodal tiles and the "
    "position-free element census; score every candidate with `_skeleton_compare.match()` on the probe's ON pages before regenerating."
)
lines[i_prev] = "**Sessions 1–26 start notes:** in `LOOP_STATE_ARCHIVE.md` (sections 'Session start notes', 'Session start notes 19–21', 'Session start notes 22–24' and 'Session start notes 25–26')."
lines[i26] = note27
with io.open(ARC, 'a', encoding='utf-8', newline='\n') as f:
    f.write('\n## Session start notes 25–26 (archived from LOOP_STATE.md 2026-09-19 08:45 NZST, session 27)\n\n' + s26 + '\n')
with io.open(HOT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines))
print('ok', os.path.getsize(HOT))
