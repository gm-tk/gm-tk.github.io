# ROUND 425 finish — name every body_compare / skeleton mover between the r423 fast-loop baseline and the scoped
# re-score of the 24 modules (the 12 XOTP + the 12-module spot-check sample). Reads the scoped structs the
# fast-loop tool just wrote (reference/tests/body_compare.json = the scoped run; _fastloop_current/skeleton_scoped.json).
import json, os, sys
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T); os.chdir(T)
import _fastloop_diff as fd
cs, bc, sk, df = fd.baseline_structs()
aff = set(open("../../outputs/_affected_r425.txt").read().split()) | set(open("../../outputs/_scoped_spotcheck_sample.txt").read().split())
sbc = json.load(open("body_compare.json"))
ssk = json.load(open(os.path.join(fd.CURRENT, "skeleton_scoped.json")))["per_page"]
bbase = {r["page"]: r for r in bc if r["module"] in aff}
bnew = {r["page"]: r for r in sbc if r["module"] in aff}
print("body_compare rows — baseline (24 mods):", len(bbase), "new:", len(bnew))
for p in sorted(set(bbase) | set(bnew)):
    a, b = bbase.get(p), bnew.get(p)
    fa = fd._bc_broken(a) if a else None; fb = fd._bc_broken(b) if b else None
    if fa != fb:
        why = []
        if b:
            if b["over_capture"] >= 0.40 and b["biggest_widget_chars"] > 400 and b["lost_blocks"] >= 3: why.append(f"over_capture {b['over_capture']:.2f} / widget {b['biggest_widget_chars']} chars / lost {b['lost_blocks']}")
            if b["multi_type"] >= 4: why.append(f"multi_type {b['multi_type']}")
            if b["empty_widgets"]: why.append(f"empty_widgets {b['empty_widgets']}")
        print(f"  {p:28s} broken {fa} -> {fb}  {'NEW PAGE' if a is None else ''} {'; '.join(why)}")
skb = {(r["module"], r["page"]): r["scaffold"] for r in sk if r["module"] in aff}
skn = {(r["module"], r["page"]): r["scaffold"] for r in ssk if r["module"] in aff}
print("skeleton rows — baseline (24 mods):", len(skb), "new:", len(skn))
new_only = [k for k in skn if k not in skb]; gone = [k for k in skb if k not in skn]
movers = [(k, skb[k], skn[k]) for k in skn if k in skb and abs(skn[k] - skb[k]) > 1e-12]
print("new-only pages:", len(new_only), "gone:", len(gone), "movers:", len(movers))
for k, a, b in movers: print("  mover", k, f"{a*100:.2f} -> {b*100:.2f}")
print("new pages mean:", sum(skn[k] for k in new_only) / len(new_only) * 100 if new_only else None, "≥50:", sum(1 for k in new_only if skn[k] >= 0.5))
