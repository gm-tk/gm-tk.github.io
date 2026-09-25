import json
a = {(p["module"], p["page"]): p for p in json.load(open("_r502_sk_pre.json"))["per_page"]}
b = {(p["module"], p["page"]): p for p in json.load(open("_fastloop_baseline/skeleton.json"))["per_page"]}
mv = sorted(((b[k]["scaffold"] - a[k]["scaffold"], k) for k in b if k in a and abs(b[k]["scaffold"] - a[k]["scaffold"]) > 1e-9), reverse=True)
up = [m for m in mv if m[0] > 0]; dn = [m for m in mv if m[0] < 0]
print(f"movers {len(mv)}: up {len(up)} / down {len(dn)}; pp-sum {100*sum(m[0] for m in mv):+.1f}; only-in-new {len(set(b)-set(a))} only-in-old {len(set(a)-set(b))}")
x50 = [(k, a[k]['scaffold'], b[k]['scaffold']) for d, k in mv if (a[k]['scaffold'] < .5) != (b[k]['scaffold'] < .5)]
x75 = [(k, a[k]['scaffold'], b[k]['scaffold']) for d, k in mv if (a[k]['scaffold'] < .75) != (b[k]['scaffold'] < .75)]
print("≥50 crossings:", len(x50), " ".join(f"{k[1]} {100*o:.1f}->{100*n:.1f}" for k, o, n in x50))
print("≥75 crossings:", len(x75), " ".join(f"{k[1]} {100*o:.1f}->{100*n:.1f}" for k, o, n in x75))
print("top up:", " ".join(f"{k[1]} {100*d:+.1f}" for d, k in up[:8]))
print("down:", " ".join(f"{k[1]} {100*a[k]['scaffold']:.1f}->{100*b[k]['scaffold']:.1f}" for d, k in dn))
