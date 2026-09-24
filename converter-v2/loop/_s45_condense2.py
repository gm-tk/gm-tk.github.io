#!/usr/bin/env python3
"""Session 45 — §5d condense #2: the session-44 per-round pointer headers and the s44 Round-log lines move VERBATIM to the archive. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s45-condense2.bak")
ss = io.open(S, encoding="utf-8", newline="").read(); L = ss.split("\n")
TAG = "(verbatim, s45 §5d condense #2)"
# 1. the s44 per-round pointer headers (each '## Session 44 — Round N PICK (engine rNNN) … SHIPPED; …' + its blank line)
hdr = [i for i, l in enumerate(L) if l.startswith("## Session 44 — Round ") and "PICK (engine r" in l]
assert len(hdr) == 7, hdr
moved_h = [L[i] for i in hdr]
for i in sorted(hdr, reverse=True):
    del L[i]
    if i < len(L) and L[i] == "": del L[i]
k = [i for i, l in enumerate(L) if l.startswith("## Per-round pointer headers, sessions 31 / 33")]; assert len(k) == 1
L.insert(k[0], "## Per-round pointer headers, session 44 (engine r479–r485, 7 headers) → LOOP_STATE_ARCHIVE.md 'Per-round pointer headers, session 44 "
         + TAG + "'. Grep the engine number there.\n")
# 2. the s44 Round-log lines
rl = [i for i, l in enumerate(L) if l.startswith("- s44-r")]
assert len(rl) == 12, rl
moved_r = [L[i] for i in rl]
first = rl[0]
for i in sorted(rl, reverse=True): del L[i]
L.insert(first, "- s44-r1…r12 round-log lines (12 lines, session 44: engine r478–r485 shipped + the r482 FULL backstop, the R5 / R10 / R12 PICK "
         "passes) → LOOP_STATE_ARCHIVE.md 'Round log s44-r1…r12 " + TAG + "'.")
ns = "\n".join(L)
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(ns); os.replace(S + ".tmp", S)
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Per-round pointer headers, session 44 " + TAG + "\n\n" + "\n\n".join(moved_h) + "\n"
    "\n## Round log s44-r1…r12 " + TAG + "\n\n" + "\n".join(moved_r) + "\n")
print("LOOP_STATE", len(ss.encode()), "->", len(ns.encode()))
