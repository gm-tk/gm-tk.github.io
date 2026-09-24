#!/usr/bin/env python3
"""Session 41 §5d condense #3 (after r461): MOVE the twelve s40 round-log lines (s40-r1 … s40-r12) verbatim to
LOOP_STATE_ARCHIVE.md and leave one pointer line; log the condense on the session-41 start note. .pre-s41-condense3.bak kept."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s41-condense3.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8"))
idx = [i for i, l in enumerate(L) if l.startswith("- s40-r")]
assert len(idx) == 12 and idx == list(range(idx[0], idx[0] + 12)), idx
moved = L[idx[0]:idx[-1] + 1]
L[idx[0]:idx[-1] + 1] = ["- s40-r1…r12 round-log lines (12 lines, session 40: engine r447–r452 shipped, four declined, one measurement-tool "
                          "round, the r452 FULL backstop) → LOOP_STATE_ARCHIVE.md 'Round log s40-r1…r12 (verbatim, s41 §5d condense #3)'."]
k = [i for i, l in enumerate(L) if l.startswith("**Session 41 started:**")]; assert len(k) == 1
L[k[0]] = L[k[0]] + " **§5d condense #3 at ≈12:30** (after r461): the twelve s40 round-log lines moved verbatim (`outputs/_s41_condense3.py`)."
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Round log s40-r1…r12 (verbatim, s41 §5d condense #3)\n\n" + "\n".join(moved) + "\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
