#!/usr/bin/env python3
"""Session 46 Round 11 — split r499's two named dips by page: the skeleton per-page scaffold (>=75 bucket crossings) and the
compare_structure exact-chain count per module, baseline (_fastloop_baseline) vs the scoped re-score (_fastloop_current).
WSL, from outputs/: python3 _s46_r11_split.py"""
import os, json
O = os.path.dirname(os.path.abspath(__file__))
def ld(d, f): return json.load(open(os.path.join(O, d, f), encoding="utf-8"))
def pages(sk):
    out = {}
    for r in sk.get("per_page", sk.get("pages_detail", [])):
        if isinstance(r, dict):
            k = r.get("page") or r.get("claude") or r.get("pair") or r.get("name"); v = r.get("scaffold", r.get("score"))
        else:
            k, v = r[0], r[1]
        out[str(k)] = v
    return out
b = ld("_fastloop_baseline", "skeleton.json"); c = ld("_fastloop_current", "skeleton_scoped.json") if os.path.exists(os.path.join(O, "_fastloop_current", "skeleton_scoped.json")) else ld("_fastloop_current", "skeleton.json")
print("skeleton keys:", list(b.keys())[:8], "|", list(c.keys())[:8])
pb, pc = pages(b), pages(c)
mv = [(k, pb[k], pc[k]) for k in pc if k in pb and abs((pc[k] or 0) - (pb[k] or 0)) > 1e-9]
print(f"skeleton movers {len(mv)}")
for k, x, y in sorted(mv, key=lambda t: t[2] - t[1]):
    f = lambda v: v * 100 if v <= 1 else v
    print(f"  {k:40s} {f(x):6.1f} -> {f(y):6.1f} ({f(y) - f(x):+.1f})")
sb = ld("_fastloop_baseline", "structural_comparison.json"); scur = ld("_fastloop_current", "structural_comparison.json")
print("cs keys:", list(sb.keys())[:8])
def cs_mod(s):
    out = {}
    for k, v in (s.get("per_module") or s.get("modules") or {}).items():
        out[k] = v.get("exact", v.get("exact_chain")) if isinstance(v, dict) else v
    return out
mb, mc = cs_mod(sb), cs_mod(scur)
for k in sorted(mc):
    if k in mb and mb[k] != mc[k]: print(f"  cs {k:10s} exact {mb[k]} -> {mc[k]}")
