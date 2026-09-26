#!/usr/bin/env python3
"""_s51_marker.py — raise a round's in-flight marker: the ONE '- **No round in flight**' line becomes
'- **Before r<N>: no round in flight**' and the marker file's text goes above it. Asserts; never shrinks the file. WSL:
python3 _s51_marker.py N MARKERFILE"""
import io, os, sys, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md")
N, mf = sys.argv[1], sys.argv[2]
src = io.open(S, encoding="utf-8", newline="").read(); L = src.split("\n")
hits = [i for i, l in enumerate(L) if l.startswith("- **No round in flight**")]
assert len(hits) == 1, hits
assert not any(l.startswith("- **ROUND ") and "IN FLIGHT" in l for l in L), "a marker is already up"
L[hits[0]] = L[hits[0]].replace("- **No round in flight**", f"- **Before r{N}: no round in flight**", 1)
L[hits[0]:hits[0]] = io.open(mf, encoding="utf-8").read().rstrip("\n").split("\n")
out = "\n".join(L); assert len(out) > len(src)
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", f"LOOP_STATE.md.pre-r{N}-marker.bak"))
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(out); os.replace(S + ".tmp", S)
print("marker r" + N, os.path.getsize(S))
