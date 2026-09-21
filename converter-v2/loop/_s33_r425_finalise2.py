#!/usr/bin/env python3
"""r425 FINISH finalise, part 2 (after the concurrent 'reviewer fixes' commit c942de2 rewrote the loop file's §0 while part 1 ran):
the loop file's §0 census table + paragraph and verify_after_transfer.sh's expect values. Run under WSL."""
import re, shutil
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
old = ("| Claude module dirs | 416 | **495** |\n| Claude pages | 2,109 | **2,559** |\n| gold dirs | 454 | **552** |\n"
       "| Writers Template / Media List docx | 619 | **762** |\n| skeleton paired pages | 1,956 | **2,353** |")
assert s.count(old) == 1
s = s.replace(old, ("| Claude module dirs | 416 | **507** |\n| Claude pages | 2,109 | **2,583** |\n| gold dirs | 454 | **552** |\n"
                    "| Writers Template / Media List docx | 619 | **762** |\n| skeleton paired pages | 1,956 | **2,377** |"))
o = "Current (22 September 2026, build 260619.96):"; assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260619.97 — r425 finished, the 12 XOTP modules IN):")
o = ("**552 gold dirs against 495 Claude dirs is CORRECT, not a fault — but the gap is 57, not 19.**\n"
     "19 are the September intake's no-builds (§2): the 12 XOTP modules until the r425 adapter is\n"
     "enabled, and 7 with no Writers Template at all.")
assert s.count(o) == 1
s = s.replace(o, ("**552 gold dirs against 507 Claude dirs is CORRECT, not a fault — but the gap is 45, not 7.**\n"
                  "7 are the September intake's no-builds (§2): the modules with no Writers Template at all (the 12\n"
                  "XOTP modules joined the corpus when r425 finished on 22 September 2026, session 33 Round 1)."))
o = ("recorded no-build. After r425 ships the figures become 507 dirs / 2,583 pages / 2,377 pairs —\n"
     "update this table AND `_MIGRATION/verify_after_transfer.sh` lines 77–78 (`expect` values, a\n"
     "dated comment, `.pre-r425.bak` kept) at that finalise.")
assert s.count(o) == 1
s = s.replace(o, ("recorded no-build. (r425 finished 22 September 2026: the table above and\n"
                  "`_MIGRATION/verify_after_transfer.sh` lines 77–78 were updated at that finalise, `.pre-s33.bak` kept.)"))
wr(p, s)
p = R + "_MIGRATION/verify_after_transfer.sh"; s = rd(p)
shutil.copyfile(p, p + ".pre-s33.bak")
o1 = '"495"   # r423 (2026-09-21): 494 -> 495'; o2 = '"2559"   # r423 (2026-09-21): 2555 -> 2559'
assert s.count(o1) == 1 and s.count(o2) == 1
s = s.replace(o1, '"507"   # r425 finished (2026-09-22): 495 -> 507, the 12 XOTP reader modules (the activity-table adapter enabled); r423 (2026-09-21): 494 -> 495')
s = s.replace(o2, '"2583"   # r425 finished (2026-09-22): 2559 -> 2583, the 12 XOTP modules x 2 pages; r423 (2026-09-21): 2555 -> 2559')
wr(p, s)
print("FINALISE2_DONE")
