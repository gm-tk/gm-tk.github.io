import json
b = {r["module"]: r for r in json.load(open("_fastloop_baseline/structural_comparison.json")) if "module" in r}
n = {r["module"]: r for r in json.load(open("../reference/tests/structural_comparison.json")) if "module" in r}
for m in sorted(set(open("_affected_r506.txt").read().split())):
    x, y = b.get(m, {}), n.get(m, {})
    d = {k: y.get(k, 0) - x.get(k, 0) for k in ("matched", "exact_chain", "claude_extra_container", "claude_missing_container")}
    if any(d.values()): print(m, d)
sk = json.load(open("_fastloop_current/skeleton_scoped.json"))["per_page"]; pre = {(p["module"], p["page"]): p["scaffold"] for p in json.load(open("_r506_sk_pre.json"))["per_page"]}
for p in sk:
    k = (p["module"], p["page"]); o = pre.get(k)
    if o is not None and abs(o - p["scaffold"]) > 1e-9: print("  sk", p["page"], f"{100*o:.1f} -> {100*p['scaffold']:.1f}")
