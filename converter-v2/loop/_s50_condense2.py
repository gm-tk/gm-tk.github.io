#!/usr/bin/env python3
"""Session 50 §5d condense #2 (WSL): the s49-r1…r11 Round-log lines and the s46-r6 / s44-r5 / s44-r3 Declined-classes entries
move to LOOP_STATE_ARCHIVE.md verbatim; one pointer line each stays hot."""
import io, os, re, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
s = io.open(S, encoding="utf-8", newline="").read()
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s50-condense2.bak"))
L = s.split("\n")
rl = [i for i, l in enumerate(L) if re.match(r"^- s49-r\d+ \(", l)]
assert len(rl) == 11, len(rl)
dc = [i for i, l in enumerate(L) if l.startswith("- **Session 46 Round 6 (25 Sept ≈13:05") or l.startswith("- **Session 44 Round 5 (25 Sept 01:40")
      or l.startswith("- **Session 44 Round 3 (25 Sept 00:45")]
assert len(dc) == 3, dc
moved_rl = [L[i] for i in rl]; moved_dc = [L[i] for i in dc]
first_rl = rl[0]; first_dc = dc[0]
for i in sorted(rl + dc, reverse=True):
    del L[i]
# pointers (indices shift: insert the later one first)
ptr_rl = ("- s49-r1…r11 round-log lines (11 lines, session 49: r501 the gate-tool round, r502–r509 shipped (the D15 queue, the nested "
          "bracket, the empty-menu flag), the r505 FULL backstop (Round 6), r510 built and toggled OFF at the stop) → LOOP_STATE_ARCHIVE.md "
          "'Round log s49-r1…r11 (verbatim, s50 §5d condense #2)'.")
ptr_dc = ("- **Session 46 Round 6 / Session 44 Rounds 5 + 3 (PICK passes, no engine change: the literal-tag leak's other mechanisms, clickDrop "
          "refusals traced, the XDLS choice board's five declined pages; writer bold in bilingual prose, placement P3 KB-correct, KB c62 "
          "re-sized; the TRR1 identical pair / audio-word line)** → LOOP_STATE_ARCHIVE.md 'Declined classes — s46-r6 / s44-r5 / s44-r3 "
          "(verbatim, s50 §5d condense #2)'; every verdict stands.")
pos = sorted([(first_rl, ptr_rl), (first_dc, ptr_dc)], key=lambda x: -x[0])
for p, t in pos:
    # the index of the first moved line, adjusted for the lines deleted before it
    shift = sum(1 for i in rl + dc if i < p)
    L.insert(p - shift, t)
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Round log s49-r1…r11 (verbatim, s50 §5d condense #2)\n\n" + "\n".join(moved_rl) + "\n"
    "\n## Declined classes — s46-r6 / s44-r5 / s44-r3 (verbatim, s50 §5d condense #2)\n\n" + "\n".join(moved_dc) + "\n")
out = "\n".join(L)
tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); os.replace(tmp, S)
print("LOOP_STATE", len(s.encode()), "->", os.path.getsize(S))
