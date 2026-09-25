import json
d = json.load(open("_fastloop_baseline/skeleton.json"))
p = d["per_page"]; n = len(p)
m = sum(r["scaffold"] for r in p) / n * 100; rw = sum(r["raw"] for r in p) / n * 100
print(f"pages {n} mean {m:.4f} raw {rw:.3f} ge50 {sum(r['scaffold']>=0.5 for r in p)} ge75 {sum(r['scaffold']>=0.75 for r in p)} ge90 {sum(r['scaffold']>=0.9 for r in p)}")
