"""ROUND 331 — position-independent line overlap (bag intersection with the gold skeleton) OFF vs ON on the dip pages."""
import sys, os, collections
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,"..","reference","tests"))
import _skeleton_compare as S
from _discrepancy_audit import pairs
OFF=os.path.join(HERE,"_r331_off_pages")
for code, page in [("TRR113","TRR113_0_0.html"),("TRR109","TRR109_3_0.html"),("TRR112","TRR112_0_0.html")]:
    for n, cp, hp in pairs(code):
        if os.path.basename(cp)!=page: continue
        _, a_on, b = S.match(cp, hp, scaffold=True); _, a_off, _ = S.match(os.path.join(OFF, code, page), hp, scaffold=True)
        B=collections.Counter(l.strip() for l in b)
        def bag(a):
            A=collections.Counter(l.strip() for l in a); return sum(min(v,B[k]) for k,v in A.items())
        hl=lambda a: sum(1 for l in a if l.strip().startswith("h"))
        print(f"{page}: position-free overlap OFF {bag(a_off)} -> ON {bag(a_on)} (gold {len(b)} lines); Claude h-lines {hl(a_off)} -> {hl(a_on)}")
