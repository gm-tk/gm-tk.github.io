#!/usr/bin/env python3
"""Session 30 Round 2 PICK — the D10-3 build lane re-read on the post-intake decline records (_r286_declines.json, 20 Sept):
per un-built type, the largest authoring-SHAPE families (signature → sites / modules), so the '≥ 20 sites' floor is judged
on the CURRENT corpus. Output: _s30_r2_shapes.out"""
import json, os
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "_r286_declines.json"), encoding="utf-8"))
# discover the record shape
recs = d if isinstance(d, list) else (d.get("declines") or d.get("records") or d.get("items") or [])
if not recs and isinstance(d, dict):
    # maybe keyed by module
    for k, v in d.items():
        if isinstance(v, list): recs += [dict(r, _mod=k) for r in v if isinstance(r, dict)]
L = [f"records: {len(recs)}"]
if recs:
    L.append("keys of a record: " + ", ".join(sorted(recs[0].keys())))
bytype = defaultdict(Counter); mods = defaultdict(lambda: defaultdict(set)); reasons = defaultdict(Counter)
for r in recs:
    t = r.get("type") or r.get("widget") or r.get("kind") or "?"
    sig = r.get("signature") or r.get("shape") or r.get("sig") or r.get("members") or "?"
    if isinstance(sig, (list, tuple)): sig = "+".join(map(str, sig))
    m = r.get("module") or r.get("code") or r.get("_mod") or "?"
    bytype[t][str(sig)] += 1; mods[t][str(sig)].add(m)
    reasons[t][str(r.get("reason") or r.get("why") or r.get("blocker") or "?")[:80]] += 1
for t, c in sorted(bytype.items(), key=lambda kv: -sum(kv[1].values())):
    L.append(f"\n== {t}: declines {sum(c.values())} / shapes {len(c)} / modules {len(set().union(*mods[t].values()))}")
    for sig, n in c.most_common(8):
        L.append(f"   {n:4d} sites / {len(mods[t][sig]):3d} mods  {sig[:150]}")
    L.append("   reasons: " + "; ".join(f"{k} ({v})" for k, v in reasons[t].most_common(5)))
txt = "\n".join(L)
open(os.path.join(HERE, "_s30_r2_shapes.out"), "w", encoding="utf-8").write(txt + "\n")
print(txt[:8000])
