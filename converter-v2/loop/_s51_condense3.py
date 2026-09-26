#!/usr/bin/env python3
"""_s51_condense3.py — session 51 §5d condense #3: the session-50 Round-log lines (s50-r1 … s50-r16) move verbatim to
LOOP_STATE_ARCHIVE.md; one pointer line replaces them. WSL."""
import io, os, re, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s51-condense3.bak"))
L = io.open(S, encoding="utf-8", newline="").read().split("\n")
idx = [i for i, l in enumerate(L) if re.match(r"^- s50-r\d+ \(", l)]
assert 10 <= len(idx) <= 20, idx
title = "Round log s50-r1…r16 (verbatim, s51 §5d condense #3)"
io.open(A, "a", encoding="utf-8", newline="\n").write(f"\n## {title}\n\n" + "\n".join(L[i] for i in idx) + "\n")
ptr = (f"- s50-r1…r16 round-log lines ({len(idx)} lines, session 50: engine r510–r521 — the generic interactive bracket, D15-19 the "
       f"yellow-✅ dropDown, the bare [hover] paren def, the writers' missing spellings, KB c64 the animated character, the typing table "
       f"form + its verifier, the drag-and-drop FIB form + its remainder, the new activity id ends the walk; r512 / r516 declined; two FULL "
       f"backstops; the R11 / R16 PICK passes) → LOOP_STATE_ARCHIVE.md '{title}'.")
L[idx[0]] = ptr
for i in sorted(idx[1:], reverse=True): del L[i]
io.open(S, "w", encoding="utf-8", newline="").write("\n".join(L))
print("moved", len(idx), "LOOP_STATE", os.path.getsize(S))
