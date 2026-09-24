#!/usr/bin/env python3
"""Session 41 §5d condense #4 (after the D14 record): MOVE the four session-40 Declined-classes entries and the s41-r1…r7
round-log lines verbatim to LOOP_STATE_ARCHIVE.md, pointer lines left. .pre-s41-condense4.bak kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s41-condense4.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8"))
d = [i for i, l in enumerate(L) if l.startswith("- **Session 40 Round ")]
assert len(d) == 4 and d == list(range(d[0], d[0] + 4)), d
dec = L[d[0]:d[-1] + 1]
L[d[0]:d[-1] + 1] = ["- **Session 40 declined classes (4 entries: Rounds 3 / 5 / 6 / 11 — the D13-4 multiChoiceQuiz kickoff, the `[RHS alert]` "
                     "family, the remaining quiz types, the stock image's own words as a caption)** → LOOP_STATE_ARCHIVE.md 'Declined "
                     "classes — session 40 entries (verbatim, s41 §5d condense #4)'; every verdict stands, grep the class name there."]
r = [i for i, l in enumerate(L) if l.startswith("- s41-r") and l[7] in "1234567" and l[8] == " "]
assert len(r) == 7 and r == list(range(r[0], r[0] + 7)), r
rl = L[r[0]:r[-1] + 1]
L[r[0]:r[-1] + 1] = ["- s41-r1…r7 round-log lines (7 lines, session 41: engine r453 / r454 shipped, r455 declined, r456–r459 shipped — the MTK "
                     "overview tabs, the red activity marker, the page-model lane) → LOOP_STATE_ARCHIVE.md 'Round log s41-r1…r7 (verbatim, "
                     "s41 §5d condense #4)'."]
k = [i for i, l in enumerate(L) if l.startswith("**Session 41 started:**")]; assert len(k) == 1
L[k[0]] += " **§5d condense #4 at ≈13:10** (after the D14 record): the four s40 declined entries and the s41-r1…r7 round-log lines moved verbatim (`outputs/_s41_condense4.py`)."
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Declined classes — session 40 entries (verbatim, s41 §5d condense #4)\n\n" + "\n".join(dec) + "\n"
    "\n## Round log s41-r1…r7 (verbatim, s41 §5d condense #4)\n\n" + "\n".join(rl) + "\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
