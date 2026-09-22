#!/usr/bin/env python3
"""Session 36 §5d condense #5 (LOOP_STATE.md 103.2 KB after the stop record): the session-31 and session-34 STOPPED entries move
verbatim to LOOP_STATE_ARCHIVE.md behind one pointer line (both are superseded — s31's r425 was finished by s33, and s34's
exhaustion verdict was overturned by s35's three shipped rounds), and the r430 / r431 / r432 Follow-up entries — every item of
which this session dispositioned — collapse to one pointer line. The s35 and s36 STOPPED entries stay hot. Run under WSL."""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
lines = st.split("\n"); moved = []

def take(prefix):
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, prefix
    moved.append(lines[idx[0]]); return idx[0]

i34 = take("## >>> STOPPED 2026-09-22 ≈16:15 NZST (session 34)")
i31 = take("## >>> STOPPED 2026-09-21 ≈22:00 NZST (session 31)")
lines[i34] = ("## STOPPED entries, sessions 31 and 34 → LOOP_STATE_ARCHIVE.md 'STOPPED entries sessions 31 / 34 (verbatim, s36 §5d condense #5)' "
              "— s31 stopped on Chris's `/loop-stop` with r425 inert (finished by s33 Round 1); s34 stopped on §4 EXHAUSTION, a verdict s35's "
              "three shipped rounds then overturned. Both superseded; every verdict inside them stands.")
lines[i31] = None
lines = [l for l in lines if l is not None]

# the r430 / r431 / r432 Follow-up entries — all dispositioned this session
keep = []
for l in lines:
    if l.startswith("- **(r432) The lesson-menu residue:") or l.startswith("- **(r431) The menu-overrun residue") or l.startswith("- **(r430) The remaining Inquiry PANELS-DIFF residue"):
        moved.append(l); continue
    keep.append(l)
lines = keep
i = next(k for k, l in enumerate(lines) if l.startswith("- **(r433) The MXFUN family's heading levels"))
lines.insert(i + 1, "- The r430 / r431 / r432 residue entries (the lesson-menu forms, the menu-overrun rows, the Inquiry PANELS-DIFF singles) → LOOP_STATE_ARCHIVE.md 'Follow-up candidates — the r430–r432 residue (s36 §5d condense #5)'. **Session 36 dispositioned all of them**: the lesson-menu residue became r435 and r436, the menu-overrun rows became r433 (MXFUN) and r434 (ARFUN) with CEDR302 recorded as a single-module outlier, and the PANELS-DIFF singles were decomposed by `_s36_r6_panelfree.py` into 8 unfilled Writers Templates (no source), the 5 dual-build pairing modules and 7 scattered singles.")

assert "STOPPED entries sessions 31 / 34 (verbatim, s36" not in ar
ar = ar.rstrip("\n") + "\n\n## STOPPED entries sessions 31 / 34 + Follow-up candidates, the r430–r432 residue (verbatim, s36 §5d condense #5 — archived 2026-09-23 ≈03:25 NZST)\n\n" + "\n\n".join(moved) + "\n"
wr(R + "LOOP_STATE_ARCHIVE.md", ar); wr(R + "LOOP_STATE.md", "\n".join(lines))
print("condense #5 OK")
