#!/usr/bin/env python3
"""Session 36 §5d condense #4 (LOOP_STATE.md 100.7 KB after the Round-5 decline record): the SHIPPED / struck Follow-up entries
(r376, r320, the r370 'declined by substance' one) move to LOOP_STATE_ARCHIVE.md behind one pointer line — they are closed items
kept only for their evidence — and the three verbatim Decisions-from-Chris blocks for sessions 29 / 30 / 31 (which all record the
SAME standing kickoff and no new numbered decision) collapse to one line each. No open item and no decision is lost.
Run under WSL: python3 _s36_condense4.py"""
import re
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
lines = st.split("\n")

# (a) the closed Follow-up entries
closed = []
keep = []
for l in lines:
    if l.startswith("- **(SHIPPED as r376") or l.startswith("- **(SHIPPED as r320") or l.startswith("- **(r370, declined by substance)"):
        closed.append(l); continue
    keep.append(l)
assert len(closed) == 3, closed
lines = keep
i = next(k for k, l in enumerate(lines) if l.startswith("- **(r370) MXEX101's repeated media sections."))
lines.insert(i + 1, "- Closed Follow-up entries (r376 the dropbox bundle SHIPPED, r320 `release_split` SHIPPED then struck, the r370 SUBMISSION-CHECKLIST item declined by substance) → LOOP_STATE_ARCHIVE.md 'Follow-up candidates — the closed entries (s36 §5d condense #4)'.")

# (b) the sessions 29 / 30 / 31 Decisions blocks
for ses, repl in (
    ("## Decisions from Chris (session 31", "## Decisions from Chris (session 31 — 2026-09-21 19:15 → ≈22:00 NZST): the standing `/loop-start` kickoff only, plus `/loop-stop` at the end — NO new numbered decision. Verbatim: LOOP_STATE_ARCHIVE.md 'Decisions from Chris sessions 29–31 (verbatim, s36 §5d condense #4)'."),
    ("## Decisions from Chris (session 30", "## Decisions from Chris (session 30 — 2026-09-21 15:36 → ≈19:10 NZST): the standing `/loop-start` kickoff only — NO new numbered decision. Verbatim: LOOP_STATE_ARCHIVE.md 'Decisions from Chris sessions 29–31 (verbatim, s36 §5d condense #4)'."),
    ("## Decisions from Chris (session 29", "## Decisions from Chris (session 29 — 2026-09-20 ≈14:30 → 22:43 NZST): the standing `/loop-start` kickoff, plus `/loop-stop` at the end — NO new numbered decision. Verbatim: LOOP_STATE_ARCHIVE.md 'Decisions from Chris sessions 29–31 (verbatim, s36 §5d condense #4)'."),
):
    idx = [k for k, l in enumerate(lines) if l.startswith(ses)]
    assert len(idx) == 1, ses
    closed.append(lines[idx[0]])
    lines[idx[0]] = repl

assert "Follow-up candidates — the closed entries (s36" not in ar
ar = (ar.rstrip("\n")
      + "\n\n## Follow-up candidates — the closed entries + Decisions from Chris sessions 29–31 (verbatim, s36 §5d condense #4 — archived from LOOP_STATE.md 2026-09-23 ≈01:55 NZST)\n\n"
      + "\n\n".join(closed) + "\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar)
wr(R + "LOOP_STATE.md", "\n".join(lines))
print("condense #4 OK")
