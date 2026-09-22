#!/usr/bin/env python3
"""Session 36 — rewrite LOOP_STATE.md's final 'Next session starts with' line. Run under WSL: python3 _s36_nextline.py"""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/LOOP_STATE.md"
s = io.open(p, encoding="utf-8").read()
i = s.rfind("**Next session starts with:**"); assert i > 0
new = (
"**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude "
"pages; the \"Amended:\" line; the §7 diff check; `git status` CLEAN at the session-36 stop commit). No round in flight; LAST SHIPPED "
"**r436** (build 260620.09); the ship ledger is at **scoped #3 since the r433 FULL (5 of headroom)**. **The session-36 §4 EXHAUSTION "
"verdict (the STOPPED entry above) stands until NEW evidence** — an intake (§1f), a KB module rule, a Needs-Chris decision, or an "
"instrument nobody has built. Every listed lane was tried this session AND three new instruments were built; the two that paid (the "
"menu-overrun CONTENT read and the continuation-page census) became r433–r436, which is the pattern to repeat: **build a new instrument "
"rather than re-walk the six lanes.** Unbuilt angles worth a session: (1) a paired census of the ACTIVITY-BOX boundary keyed on the "
"WRITER'S shape rather than on the rendered box — this session's `_s36_r7_actbound.py` matched 4,617 boxes by title and found the "
"population diffuse (2,410 over-capture / 1,572 under) precisely because it keys on the OUTPUT; the WT-side question \"which writer shape "
"makes the box end early\" has never been measured; (2) the body's ROW COMPOSITION around a paragraph that follows a menu block (the r435 "
"dips — the Follow-up section's entry; related to the s25 minor-heading decline, so it needs new evidence to re-open); (3) CEDR302's "
"89-element overview menu (one module, but the last large single-page menu overrun left in the corpus). NEEDS CHRIS: the open lines of the "
"\"Needs Chris\" section — **#4 the quiz-engine widget types is still the single largest lever in the corpus** (844 hand-off boxes; the "
"Bilingual family alone loses 63.68pp), and #6 the dual-build gold pairing now touches BLL240 / CEDK501 / CEDT207 / CEDT301 / MXFUN01.\n")
io.open(p, "w", encoding="utf-8", newline="\n").write(s[:i] + new)
print("next-session line written")
