#!/usr/bin/env python3
"""Session 26 — Round 12 (a PICK pass, no engine change) + the STOPPED entry (≤ 1,500 chars) + the 'Next session starts with' line
(≤ 800 chars). LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r12 (no engine change)" in s:
    print("already applied"); sys.exit(0)
# Round 12 — the PICK pass stub (above the Round log) and its Round-log line
stub = ("## Session 26 — Round 12 PICK pass (no engine change — the budget's last round): five classes measured, none taken — the flip group's parent "
        "column by card count (`_s26_r398_flipparent.py`: col-md-8 0.28–0.66, diffuse; 7–9 cards → the activity box's col-12 0.61 = ownership, not width); "
        "the wholly-bold paragraph (`_s26_r398_pbold.py`: Claude 1781 vs the gold 1079, the gold's h4 / h5 8186 vs Claude's 4744 — the session-11 decline of "
        "'the whole-bold short paragraph → h5' stands); the inner `row › col-12` inside activity boxes (`_s26_r398_actrow.py`: 234 on 157 gold pages, every one "
        "a widget-internal panel row — hintDropContent 114, clickDropContent 63); rows directly inside the activity col-12 (`_s26_r398_colrow12.py`: no Claude "
        "inner-row kind left after r394); the speech bubble's character image (r397's decline, a needs-Chris question). Full text in the Round log line below.\n\n")
i = s.index("## Round log\n")
s = s[:i] + stub + s[i:]
line = ("- s26-r12 (no engine change) · THE BUDGET'S LAST ROUND — a PICK pass: the flip group's parent column by card count (diffuse, 0.28–0.66), the "
        "wholly-bold paragraph (the s11 decline stands; the gold's h4 / h5 8186 vs Claude's 4744 is the un-taken heading gap), the activity box's inner "
        "`row › col-12` (234 gold, all widget-internal panel rows), the col-12 inner rows (nothing left after r394), the speech bubble's character image "
        "(needs Chris) — DECLINED, no code · 19 Sept ≈06:15 · corpus byte-identical to r397; every r397 gate stands · build 260619.68\n")
assert len(line) <= 560, len(line)
anchor = "- s26-r11 (engine r397)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
# the STOPPED entry, above the session-25 one
STOP = ("## >>> STOPPED 2026-09-19 ≈06:15 NZST (session 26) on §4 BUDGET — 12 rounds done (the §7 default; 6 h 50 min of the 10). ELEVEN SHIPPED: r387 the "
        "whakataukī flows on · r388 the plain / solid alert (FULL) · r389 the built flipCard closes its column · r390 the supervisor note's explicit closer · "
        "r391 the LtL own-row panel column · r392 adjacent lists are one list · r393 a glyph-only line renders nothing · r394 the clickDrop buttons sit in "
        "the column (+0.114pp, ≥50 +4 / ≥75 +3 / ≥90 +3) · r395 the flip-card width by card count · r396 the captioned video slide is `item video` (FULL "
        "backstop: all 416, 0 stale, no residue) · r397 a table header cell is plain; Round 12 a PICK pass, declined. Skeleton **53.351 → 53.695 %** "
        "(+0.344pp; 58.4 % of the 91.9 % ceiling), ≥50 1151 → 1163, ≥75 185 → 195, ≥90 15 → 18; compare_structure exact 11641 → 11723; every other gate "
        "EXACT or better; every verifier RESULT identical; 15 + 1 selftests GREEN every round. The miner re-mined after every ship: 179 → 173 CANDIDATE "
        "rows, all dispositioned. Plateau window 2 of 3 (r396 gate-invisible, r397 +0.012pp). Build 260619.68; ledger scoped #1 since the r396 FULL. NEEDS "
        "CHRIS (five): the journal button; the dual-build pairing; the activity-number provenance round; the 12 empty-lesson-menu repeaters; NEW — the "
        "speech bubble's character image (the gold adds one in Online Safety 0.95 / TEDC 0.91 — a placeholder-image policy per subject is Chris's call). "
        "Tree clean at the stop commit. <<<\n\n")
assert len(STOP) <= 1500 + 2, len(STOP)
a = s.index("## >>> STOPPED 2026-09-18 ≈20:40 NZST (session 25)")
s = s[:a] + STOP + s[a:]
# the Next-session line (the trailing paragraph)
n = s.rindex("**Next session starts with:**")
NEXT = ("**Next session starts with:** the standing `/loop-start`; health check (locks, `verify_after_transfer.sh` PASS, `wc -c`); `git status` in "
        "pageforge-site: a CLEAN tree at the session-26 stop commit (r397 = f944f07 beneath it); the miner's queue (≈05:50, the r397 corpus) is current — "
        "173 CANDIDATE rows, all dispositioned; this session's productive instrument was the PAIRED WIDGET / WRAPPER CENSUS (`_s26_r394_clickdrop.py`, "
        "`_s26_r395_flipcols.py`, `_s26_r396_widgetwrap.py`, `_s26_r397_thb.py`) — extend it to hintSlider / tabs / dropbox / TKmodal "
        "tiles and the position-free element census; score every candidate with `_skeleton_compare.match()` on the probe's ON pages BEFORE regenerating; "
        "the ledger is at scoped #1 since the r396 FULL; the five needs-Chris items are in the STOPPED entry.\n")
assert len(NEXT) <= 800, len(NEXT)
s = s[:n] + NEXT
s = s.replace("- Standing facts: AppVersion 260619.68;", "- Standing facts: AppVersion 260619.68 (session 26 stopped ≈06:15 on the 12-round budget);", 1)
wr(LS, s)
print("LOOP_STATE:", len(s.encode("utf-8")), "bytes; STOPPED", len(STOP), "chars; NEXT", len(NEXT), "chars")
