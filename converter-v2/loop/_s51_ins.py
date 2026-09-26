#!/usr/bin/env python3
"""_s51_ins.py — insert the contents of a text file right after the ONE line of LOOP_STATE.md that starts with a given prefix
(asserted unique); refuses to write a result smaller than the original. WSL:  python3 _s51_ins.py "<prefix>" FILE [ "<prefix2>" FILE2 … ]"""
import io, os, sys, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md")
src = io.open(S, encoding="utf-8", newline="").read()
L = src.split("\n")
args = sys.argv[1:]
assert len(args) % 2 == 0 and args
for k in range(0, len(args), 2):
    pre, f = args[k], args[k + 1]
    hits = [i for i, l in enumerate(L) if l.startswith(pre)]
    assert len(hits) == 1, (pre, hits)
    add = io.open(f, encoding="utf-8").read().rstrip("\n").split("\n")
    L[hits[0] + 1:hits[0] + 1] = add
out = "\n".join(L)
assert len(out) > len(src), "refusing to shrink LOOP_STATE.md"
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-ins.bak"))
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(out)
assert os.path.getsize(S + ".tmp") > 1000
os.replace(S + ".tmp", S)
print("LOOP_STATE", len(src.encode()), "->", os.path.getsize(S))
