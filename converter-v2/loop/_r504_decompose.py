import json
a = [p for p in json.load(open("_r504_sk_pre.json"))["per_page"] if p["module"] == "CEDT301"]
b = [p for p in json.load(open("_fastloop_current/skeleton_scoped.json"))["per_page"] if p["module"] == "CEDT301"]
print("before (split):", len(a), "pairs", " ".join(f"{p['page']} {100*p['scaffold']:.1f}" for p in a), f"mean {100*sum(p['scaffold'] for p in a)/len(a):.1f}",
      f">=50 {sum(p['scaffold']>=.5 for p in a)} >=75 {sum(p['scaffold']>=.75 for p in a)}")
print("after (single):", len(b), "pairs", " ".join(f"{p['page']} {100*p['scaffold']:.1f} raw {100*p['raw']:.1f}" for p in b))
pre = json.load(open("_fastloop_baseline/skeleton.json"))["per_page"]
rest = [p for p in pre if p["module"] != "CEDT301"]
print(f"corpus without CEDT301: {100*sum(p['scaffold'] for p in rest)/len(rest):.4f} @ {len(rest)}")
