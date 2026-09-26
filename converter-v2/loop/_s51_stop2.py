#!/usr/bin/env python3
"""_s51_stop2.py — the stop's verify note: verify_after_transfer.sh FAILs on exactly the two uncommitted r528 checksums (expected)."""
import io, os
S = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "LOOP_STATE.md"))
s = io.open(S, encoding="utf-8", newline="").read()
a = "uncommitted and proven inert — NOT a crashed round (Position names it)."
b = "uncommitted and proven inert — NOT a crashed round (Position names it); `verify_after_transfer.sh` FAILs on exactly those two checksums — expected."
c = "Nothing regenerated; the corpus on disk is the r526 state."
d = "Nothing regenerated; the corpus on disk is the r526 state. `verify_after_transfer.sh` reads FAIL on exactly these two files' engine checksums — expected while r528 is loose, not a broken tree."
assert s.count(a) == 1 and s.count(c) == 1
s = s.replace(a, b).replace(c, d)
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(S + ".tmp", S)
n = [l for l in s.split("\n") if l.startswith("**Next session starts with:**")][0]
print("next-line chars", len(n), "size", os.path.getsize(S))
