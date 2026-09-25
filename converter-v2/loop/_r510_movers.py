import json, os
pre = {(p["module"], p["page"]): p for p in json.load(open("_r510_sk_pre.json"))["per_page"]}
new = {(p["module"], p["page"]): p for p in json.load(open(os.environ.get("SKNEW", "_fastloop_baseline/skeleton.json")))["per_page"]}
a = {k: v for k, v in pre.items() if k in new or k[0] in {m for m, _ in new}}
mv = sorted(((new[k]["scaffold"] - a[k]["scaffold"], k) for k in new if k in a and abs(new[k]["scaffold"] - a[k]["scaffold"]) > 1e-9), reverse=True)
up = [m for m in mv if m[0] > 0]; dn = [m for m in mv if m[0] < 0]
print(f"movers {len(mv)}: up {len(up)} / down {len(dn)}; pp-sum {100*sum(m[0] for m in mv):+.1f}")
x50 = [(k, a[k]['scaffold'], new[k]['scaffold']) for d, k in mv if (a[k]['scaffold'] < .5) != (new[k]['scaffold'] < .5)]
x75 = [(k, a[k]['scaffold'], new[k]['scaffold']) for d, k in mv if (a[k]['scaffold'] < .75) != (new[k]['scaffold'] < .75)]
print("≥50 crossings:", len(x50), " ".join(f"{k[1]} {100*o:.1f}->{100*n:.1f}" for k, o, n in x50))
print("≥75 crossings:", len(x75), " ".join(f"{k[1]} {100*o:.1f}->{100*n:.1f}" for k, o, n in x75))
print("top up:", " ".join(f"{k[1]} {100*d:+.1f}" for d, k in up[:10]))
print("down:", " ".join(f"{k[1]} {100*a[k]['scaffold']:.1f}->{100*new[k]['scaffold']:.1f}" for d, k in dn))
