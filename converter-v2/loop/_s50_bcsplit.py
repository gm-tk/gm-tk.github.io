"""_s50_bcsplit.py — session 50: split a scoped ship's body_compare ANY / compare_structure missing moves by page.
Baseline = outputs/_fastloop_baseline/*.json; new = reference/tests/{body_compare,structural_comparison}.json
(left full + coherent by _fastloop_diff.py). Run under WSL from CONVERTER_V2/outputs/."""
import json, os, sys
B = "_fastloop_baseline"; T = os.path.join("..", "reference", "tests")
def load(p): return json.load(open(p, encoding="utf-8"))
def flags(r):
    f = []
    if r["over_capture"] >= 0.40 and r["biggest_widget_chars"] > 400 and r["lost_blocks"] >= 3: f.append("over_capture")
    if r["multi_type"] >= 4: f.append("multi_type=%d" % r["multi_type"])
    if r["empty_widgets"]: f.append("empty=%s" % json.dumps(r["empty_widgets"])[:160])
    return f
def key(r): return r.get("page") or r.get("claude") or r.get("file") or json.dumps({k: r[k] for k in list(r)[:2]})
bb = load(os.path.join(B, "body_compare.json")); nb = load(os.path.join(T, "body_compare.json"))
print("body_compare row keys:", list(bb[0].keys())[:12])
bm = {key(r): r for r in bb}; nm = {key(r): r for r in nb}
for k in sorted(set(bm) | set(nm)):
    fo = flags(bm[k]) if k in bm else ["(absent)"]; fn = flags(nm[k]) if k in nm else ["(absent)"]
    if bool(fo) != bool(fn) or (fo != fn and (fo or fn)):
        print("BC", k, "|", fo, "->", fn)
bc = load(os.path.join(B, "structural_comparison.json")); nc = load(os.path.join(T, "structural_comparison.json"))
print("cs row keys:", list(bc[0].keys())[:14])
cm = {key(r): r for r in bc}; ncm = {key(r): r for r in nc}
for k in sorted(set(cm) | set(ncm)):
    a = cm.get(k, {}); b = ncm.get(k, {})
    da = {x: b.get(x, 0) - a.get(x, 0) for x in ("exact_chain", "claude_missing_container", "claude_extra_container", "matched")}
    if any(da.values()): print("CS", k, da)
