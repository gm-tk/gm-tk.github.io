#!/usr/bin/env python3
"""Session 26 Round 4 (r390) — write the PICK section into LOOP_STATE.md (before the code, per §3). Idempotent; LF preserved."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md")
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 4 PICK (engine r390)" in s:
    print("already"); sys.exit(0)
PICK = """## Session 26 — Round 4 PICK (engine r390): THE SUPERVISOR NOTE'S EXPLICIT CLOSER — a `[Supervisor button] … [End Supervisor button]` / `[Supervisor note] … [end supervisor note]` pair is a SPAN: everything between is the panel's content
- **The lead:** the r388 paired row-break census, direction A, kind `row` = `div.row.super-content` (the non-activity supervisor panel): Claude breaks the row after the panel and the gold puts the next text INSIDE the panel — 27 / 6 = 0.82 overall, **Leaving to Learn 22 / 0 = 1.00 (22 pages)**. The panel-content census (`outputs/_s26_r390_supclose.py` → `.out`, paired per group): LtL in-panel 22 / free 0 (4 modules), English 4 / 2 (ENGR102's empty panels), ANZH 1 / 0; Mathematics 0 / 9, BLL 0 / 4, OS 0 / 1, ConnectED 0 / 1 (the gold agrees with Claude there).
- **The mechanism (triangulated on XDLS904 lesson 1 / XDLS502 lesson 3 — WT → gold → Claude):** the writer opens `[Supervisor Button]` (r170 promotes it to the `supervisor note` CONTAINER_OPEN), types paragraphs + bullets whose items END in an inline red `[link to XFUN06]` marker, and CLOSES with `[End Supervisor button]` (XDLS904 / 905 / 906: 21 pairs) or `[end supervisor note]` (XDLS502, XDLS901). The gold's panel holds everything to the closer (p, ul, p, ul …); Claude's own_row panel is ALWAYS STRICT (`#calloutOpen(…, spans = false)` — "emitted complete") so `MediaBuilder.gatherFollowing` stops at the first tag item (the bullet's inline `[link to …]`) and the rest ships as free rows. The live parser: `[End Supervisor button]` → `end supervisor button` CONTAINER_CLOSE, `[end supervisor note]` → `end supervisor note` CONTAINER_CLOSE. Corpus-wide the explicit supervisor closer exists ONLY in the LtL family (the WT census: XDLS904/905/906 21 + XDLS901 1 + XDLS502 1 + XTAS102 1); every other family's note has no closer → untouched by construction.
- **KB-first check:** 05B / 01F give the panel form (`row.supervisor > super-content-button > super-content row > row > col-12 + col-12`); nothing on a writer-closed span → §1b level 3 / 4. A writer's explicit closer is the r105 span rule the alert family already honours (`#explicitCloseAhead`) — structure-only, derivable.
- **Fix (DATA OVER CODE):** `callouts.by_tag."supervisor note".explicit_close_span {enabled, env: SUPSPAN_OFF}`: the own_row branch tests `#explicitCloseAhead(bodyItems, i, tag, stopAtActivity = true)` — the family set now also accepts the closer of a `tag_promote` source (`end supervisor button` for `supervisor note`), and an `[Activity]` opener ends the scan (an own-row span never swallows an activity) — and on a hit opens the panel in SPAN mode (`#calloutOpen(…, true)`, stack mode `span-own`): the loop renders the items between inside the panel's column (emit() opens no content row while the own-row span is open — `ownSpanClose`), autoClose treats it as a writer's span (a heading never closes it; a section marker / page boundary does), the closer pops it. OFF = the strict panel (the r389 output). Expected ON: the LtL pages (~24) only. Regeneration: SCOPED (the probe's ON list) = scoped ship #2 since the r388 full.
- **Not taken:** the r162 in-panel italic strip is not applied to the span's loop-rendered items (XDLS is in `strip_italic_subjects` — record if the probe shows an `<i>`); ENGR102's empty panels (4 / 2, no closer — a different mechanism: the note's text sits in a `[body]` after the opener); MXDI103's panel truncation (the gold panel continues past a black run — no closer, Maths 0 / 9 at the row boundary).

"""
anchor = "## Round log\n"
i = s.index(anchor)
s = s[:i] + PICK + s[i:]
io.open(LS, "w", encoding="utf-8", newline="").write(s)
print("PICK written", len(s))
