"""Session 50 — a page's skeleton score against the gold for OFF (saved dir) / disk / NEW (saved dir). Tests dir, WSL:
python3 ../../outputs/_s50_sk3.py OFFDIR NEWDIR CODE [CODE…]  (every paired page of each module)"""
import os, sys, difflib
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _skeleton_compare as K
offd, newd = sys.argv[1:3]
r = lambda a, b: 100 * difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
tot = [0, 0, 0]
for code in sys.argv[3:]:
    for _, cp, hp in DA.pairs(code):
        pg = os.path.basename(cp); g = K._skel(hp, True)
        vals = []
        for p in (os.path.join(offd, code, pg), cp, os.path.join(newd, code, pg)):
            vals.append(r(g, K._skel(p, True)) if os.path.exists(p) else float("nan"))
        if abs(vals[0] - vals[2]) > 0.05 or abs(vals[1] - vals[2]) > 0.05:
            print(f"{pg:28s} OFF {vals[0]:5.1f}  disk {vals[1]:5.1f}  NEW {vals[2]:5.1f}  (NEW-OFF {vals[2]-vals[0]:+5.1f})")
        for i in range(3): tot[i] += vals[i]
print(f"SUM OFF {tot[0]:.1f} disk {tot[1]:.1f} NEW {tot[2]:.1f}")
