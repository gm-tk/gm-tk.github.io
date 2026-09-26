#!/usr/bin/env python3
"""_s51_r6_bodymem_join.py — join _s51_r6_bodymem.log (every [Body] member of every widget bundle) with the GOLD placement of its
text (the §1g census parser over the module's gold pages; jacc >= 0.6): gold free / inside a widget / inside an activity / alert /
absent. Grouped by bundle type × afterContent × built. WSL, from reference/tests/."""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from anchor_compare import HUMAN

fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", re.sub(r"\*", "", t.lower())).split())
cache = {}
agg = collections.defaultdict(collections.Counter); mods = collections.defaultdict(set)
for l in open("../../outputs/_s51_r6_bodymem.log", encoding="utf-8"):
    if not l.startswith("BM\t"): continue
    _, code, typ, pos, after, built, text = l.rstrip("\n").split("\t")[:7]
    if code not in cache:
        cache[code] = [b for f in sorted(glob.glob(os.path.join(_corpus.mdir(HUMAN, code), "*.html"))) for b in PC.parse(f)]
    t = fold(text)
    best = max(cache[code], key=lambda b: PC.jacc(b[1], t), default=None)
    r = best[3] if best and PC.jacc(best[1], t) >= 0.6 else "absent"
    k = "free" if re.search(r"(^|:)free", r) else ("widget" if ":widget" in r else ("activity" if "activity" in r else ("alert" if "alert" in r else ("absent" if r == "absent" else "other"))))
    key = f"{typ:16s} after={after} built={built}"
    agg[key][k] += 1; mods[key].add(code)
tot = collections.Counter()
for key, c in sorted(agg.items(), key=lambda kv: -sum(kv[1].values())):
    n = sum(c.values()); tot.update(c)
    print(f"{key}  n={n:4d} mods={len(mods[key]):3d}  free {c['free']:4d} widget {c['widget']:4d} activity {c['activity']:4d} alert {c['alert']:3d} other {c['other']:3d} absent {c['absent']:4d}")
print("TOTAL", dict(tot))
