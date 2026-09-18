#!/usr/bin/env python3
"""Why does CEDK501_5_1 drop 52.0 -> 42.9 when one `<p>[</p>` line is removed? The gate's skeleton lines OFF vs ON vs gold and
the matched blocks. python3 _s26_r393_cedk.py"""
import os, sys, difflib
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUT = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
from _skeleton_compare import match
code, pg = sys.argv[1], sys.argv[2]
for n, cp, hp in pairs(code):
    if cp.endswith(pg):
        onp = os.path.join(OUT, "_s26_r393_on", code, pg)
        r0, a0, b0 = match(cp, hp, scaffold=True); r1, a1, b1 = match(onp, hp, scaffold=True)
        print(f"{pg}: OFF {r0*100:.1f} (claude {len(a0)} lines / gold {len(b0)}) → ON {r1*100:.1f} (claude {len(a1)})")
        sm0 = difflib.SequenceMatcher(None, b0, a0, autojunk=False); sm1 = difflib.SequenceMatcher(None, b1, a1, autojunk=False)
        m0 = sum(bl.size for bl in sm0.get_matching_blocks()); m1 = sum(bl.size for bl in sm1.get_matching_blocks())
        print("matched lines OFF", m0, "ON", m1)
        d = [l for l in difflib.unified_diff(a0, a1, lineterm="", n=0)]; print("claude OFF→ON diff:", d[2:8])
        print("OFF blocks:", [(b.a, b.b, b.size) for b in sm0.get_matching_blocks() if b.size][:14])
        print("ON  blocks:", [(b.a, b.b, b.size) for b in sm1.get_matching_blocks() if b.size][:14])
        i = next((k for k, l in enumerate(a0) if l not in a1), None)
        if i is not None: print("removed line index", i, "context:", a0[max(0, i-3):i+3])
