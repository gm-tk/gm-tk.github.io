#!/usr/bin/env python3
"""Session 42 §5d condense #1 (after r466, LOOP_STATE.md 98.4 KB — near the 100 KB target): MOVE verbatim to LOOP_STATE_ARCHIVE.md
(1) the withdrawn r464 PICK section, (2) the ten session-40 / 41 pointer headers (one pointer line left), (3) the s41-r8…r12 round-log
lines, (4) the Position 'Before it' rows r459 → r453. Pointer lines left. .pre-s42-condense1.bak kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s42-condense1.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8"))
arch = []
# (1) the withdrawn r464 PICK section
p0 = [i for i, l in enumerate(L) if l.startswith("## Session 41 — Round 12 PICK (engine r464)")]; assert len(p0) == 1; p0 = p0[0]
p1 = p0 + 1
while not L[p1].startswith("## "): p1 += 1
arch.append(("Session 41 — Round 12 PICK (engine r464, WITHDRAWN by D14-21) (verbatim, s42 §5d condense #1)", L[p0:p1]))
L[p0:p1] = ["## Session 41 — Round 12 PICK (engine r464, WITHDRAWN by D14-21) → LOOP_STATE_ARCHIVE.md 'Session 41 — Round 12 PICK (engine "
            "r464, WITHDRAWN by D14-21) (verbatim, s42 §5d condense #1)'.", ""]
# (2) the session-40 / 41 pointer headers (each '## Session 4x — Round N (engine rNNN, build …) — … SHIPPED; …' + a blank line)
idx = [i for i, l in enumerate(L) if (l.startswith("## Session 41 — Round ") or l.startswith("## Session 40 — Round "))
       and "SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md" in l]
assert len(idx) == 9, idx
blk = [L[i] for i in idx]
for i in sorted(idx, reverse=True):
    if i + 1 < len(L) and L[i + 1] == "": del L[i + 1]
    del L[i]
ins = min(idx)
L.insert(ins, "## Sessions 40 / 41 — every shipped round (engine r447–r449, r451–r454, r460, r461) — each PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md under 'Session N — Round M PICK (engine rXXX) + what shipped' (grep the engine number); the nine pointer "
         "headers → 'Session 40 / 41 pointer headers (verbatim, s42 §5d condense #1)'.")
L.insert(ins + 1, "")
arch.append(("Session 40 / 41 pointer headers (verbatim, s42 §5d condense #1)", blk))
# (3) the s41-r8…r12 round-log lines
r = [i for i, l in enumerate(L) if any(l.startswith(f"- s41-r{n} ") for n in (8, 9, 10, 11, 12))]
assert len(r) == 5 and r == list(range(r[0], r[0] + 5)), r
arch.append(("Round log s41-r8…r12 (verbatim, s42 §5d condense #1)", L[r[0]:r[-1] + 1]))
L[r[0]:r[-1] + 1] = ["- s41-r8…r12 round-log lines (5 lines, session 41: engine r460 / r461 shipped, r462 / r463 declined, r464 built then "
                     "WITHDRAWN by D14-21) → LOOP_STATE_ARCHIVE.md 'Round log s41-r8…r12 (verbatim, s42 §5d condense #1)'."]
# (4) the Position 'Before it' rows r459 → r453
b = [i for i, l in enumerate(L) if any(l.startswith(f"- Before it: **r{n}**") for n in (459, 458, 457, 456, 454, 453))]
assert len(b) == 6 and b == list(range(b[0], b[0] + 6)), b
arch.append(("Position — LAST SHIPPED tail r459 → r453 (verbatim, s42 §5d condense #1)", L[b[0]:b[-1] + 1]))
L[b[0]:b[-1] + 1] = ["- Before them: **r459 / r458 / r457 / r456 / r454 / r453** (the page-model lane, the red activity marker, the MTK "
                     "overview tabs — session 41) — the verbatim gate rows → LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail r459 → "
                     "r453 (verbatim, s42 §5d condense #1)'."]
k = [i for i, l in enumerate(L) if l.startswith("**Session 42 started:**")]; assert len(k) == 1
L[k[0]] += (" **§5d condense #1 at ≈14:58** (after r466, 98.4 KB): the withdrawn r464 PICK, the nine s40 / s41 pointer headers, the "
            "s41-r8…r12 round-log lines and the r459 → r453 Position rows moved verbatim (`outputs/_s42_condense1.py`).")
with io.open(A, "a", encoding="utf-8", newline="\n") as f:
    for title, lines in arch:
        f.write("\n## " + title + "\n\n" + "\n".join(lines).rstrip() + "\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
