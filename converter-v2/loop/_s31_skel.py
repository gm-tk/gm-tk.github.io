#!/usr/bin/env python3
"""_s31_skel.py — print the gate's own SCAFFOLD skeleton of one or more HTML pages (the lines the PRIMARY gate diffs).
Usage (reference/tests/): python3 ../../outputs/_s31_skel.py <html path> [...]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _structural_skeleton as S
from _skeleton_compare import _skel
for p in sys.argv[1:]:
    lines = _skel(p, True)
    print(f"=== {p}  ({len(lines)} lines)")
    print("\n".join(lines))
