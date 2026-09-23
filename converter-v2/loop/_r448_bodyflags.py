#!/usr/bin/env python3
"""Round 448 — name the body_compare sub-count movers (over-capture 56 -> 57, empty 201 -> 200): for every page of the
affected modules, body_compare's own parse() of the OFF page (outputs/_r448_off, ANSWERKEY_OFF=1) and of the shipped page,
then its own flag arithmetic. Run from reference/tests under WSL."""
import os, sys, glob
sys.path.insert(0, os.getcwd())
import body_compare as B, _corpus
O = os.path.join("..", "..", "outputs")
aff = [l.strip() for l in open(os.path.join(O, "_affected_r448.txt")) if l.strip()]
def flags(cp, hp):
    total = max(1, cp.all_chars); w = list(cp.cv2_text.values()); mx = max(w) if w else 0
    hfree = len(hp.free_blocks) if hp else 0; lost = hfree - len(cp.free_blocks)
    return dict(over=(mx / total >= 0.40 and mx > 400 and lost >= 3), empty=sum(1 for v in w if v < 40), oc=round(mx / total, 2), mx=mx, lost=lost)
for mod in aff:
    cdir, hdir = _corpus.mdir(B.CLAUDE, mod), _corpus.mdir(B.HUMAN, mod)
    if not os.path.isdir(cdir) or not os.path.isdir(hdir): continue
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=B.pkey)
    hpages = sorted(_corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=B.pkey)
    for i, cf in enumerate(cpages):
        off = os.path.join(O, "_r448_off", mod, cf)
        if not os.path.exists(off): continue
        hp = B.parse(os.path.join(hdir, hpages[i])) if i < len(hpages) else None
        a = flags(B.parse(off), hp); b = flags(B.parse(os.path.join(cdir, cf)), hp)
        if a["over"] != b["over"] or (a["empty"] > 0) != (b["empty"] > 0):
            print(f"{mod}/{cf}: OFF over={a['over']} ({a['oc']}, {a['mx']} ch, lost {a['lost']}) empty={a['empty']}  ->  ON over={b['over']} ({b['oc']}, {b['mx']} ch) empty={b['empty']}")
