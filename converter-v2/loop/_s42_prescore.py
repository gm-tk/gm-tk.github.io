#!/usr/bin/env python3
"""SESSION 42 (parametrised: python3 ../../outputs/_s42_prescore.py <TAG> <BASE_MEAN> <BASE_PAIRS>) — pre-score the ON corpus with the gate's own
pairing and match(). The page SET changes (TRR116 gains lessons 1–5, others gain / lose files), so the pairing is recomputed on
BOTH sides: OLD = pairs() over the disk (the r452 state); NEW = pairs() with the Claude dir of each changed module pointed at
the ON pages saved by `_r461_probe_run.sh SAVE` (outputs/_r461_on/<CODE>). Prints every pair on both sides, the module sums,
and the corpus-mean estimate on the NEW population (pairs 2477 + the added pairs).
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r461_prescore.py
"""
import os, sys
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA
import _corpus
from _skeleton_compare import match
from anchor_compare import CLAUDE

O = os.path.abspath(os.path.join("..", "..", "outputs")); TAG = sys.argv[1]
codes = [c.strip() for c in open(os.path.join(O, "_" + TAG + "_ON_modules.txt")) if c.strip()]
_mdir = _corpus.mdir
ON = {"on": False}
def mdir(root, *parts):
    if ON["on"] and os.path.abspath(root) == os.path.abspath(CLAUDE) and parts and parts[0] in codes:
        return os.path.join(O, "_" + TAG + "_on", parts[0])
    return _mdir(root, *parts)
_corpus.mdir = mdir
DA._corpus.mdir = mdir

def score(code):
    out = {}
    for n, cp, hp in DA.pairs(code):
        s, r = match(cp, hp, scaffold=True)[0], match(cp, hp, scaffold=False)[0]
        out[os.path.basename(hp)] = (os.path.basename(cp), s, r)
    return out

tot_old = tot_new = 0.0; n_old = n_new = 0; b50o = b50n = b75o = b75n = 0
for code in codes:
    ON["on"] = False; old = score(code)
    ON["on"] = True; new = score(code)
    print(f"\n## {code}: pairs {len(old)} -> {len(new)}")
    for h in sorted(set(old) | set(new)):
        o = old.get(h); w = new.get(h)
        os_ = f"{o[0]:18s} {100*o[1]:5.1f}" if o else f"{'—':18s}   ——"
        ws_ = f"{w[0]:18s} {100*w[1]:5.1f} (raw {100*w[2]:5.1f})" if w else f"{'—':18s}   ——"
        print(f"   {h:24s} OLD {os_}  NEW {ws_}")
    so = sum(v[1] for v in old.values()); sn = sum(v[1] for v in new.values())
    tot_old += so; tot_new += sn; n_old += len(old); n_new += len(new)
    b50o += sum(1 for v in old.values() if v[1] >= 0.5); b50n += sum(1 for v in new.values() if v[1] >= 0.5)
    b75o += sum(1 for v in old.values() if v[1] >= 0.75); b75n += sum(1 for v in new.values() if v[1] >= 0.75)
    print(f"   module sum {100*so:.1f} over {len(old)} -> {100*sn:.1f} over {len(new)}  (mean {100*so/max(1,len(old)):.1f} -> {100*sn/max(1,len(new)):.1f})")

BASE_MEAN, BASE_PAIRS = float(sys.argv[2]), int(sys.argv[3])
base_sum = BASE_MEAN * BASE_PAIRS
new_pairs = BASE_PAIRS - n_old + n_new
new_mean = (base_sum - 100 * tot_old + 100 * tot_new) / new_pairs
print(f"\nchanged modules: pairs {n_old} -> {n_new}; pp-sum {100*tot_old:.1f} -> {100*tot_new:.1f} ({100*(tot_new-tot_old):+.1f})")
print(f"corpus: {BASE_MEAN:.4f} % @ {BASE_PAIRS} -> ≈ {new_mean:.4f} % @ {new_pairs}  ({new_mean-BASE_MEAN:+.4f}pp);  >=50 {b50n-b50o:+d}, >=75 {b75n-b75o:+d}")
