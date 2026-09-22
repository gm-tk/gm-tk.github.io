#!/usr/bin/env python3
"""_intake_split.py — LOOP §1f Phase 3 "SPLIT BY POPULATION": after an intake's full regeneration, score the PRE-EXISTING
modules and the NEW batch separately on every decomposable gate, reading the fast-loop structs the snapshot just wrote
(outputs/_fastloop_baseline/ = the live full run). The pre-existing subset must reproduce the last shipped round EXACTLY.
Usage (WSL, from anywhere):  python3 _intake_split.py <new-codes.txt> [<last-shipped-sk_final.json>]
Generalised from _s28_t1_split.cjs (r408) for the 22 Sept 2026 Round 0d; kept for the next intake."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(HERE, "..", "reference", "tests")
sys.path.insert(0, TESTS); os.chdir(TESTS)
import _fastloop_diff as fd
new = set(open(os.path.abspath(os.path.join(os.environ.get("PWD", HERE), sys.argv[1])) if not os.path.isabs(sys.argv[1]) else sys.argv[1]).read().split())
cs, bc, sk, df = fd.baseline_structs()
def part(rows, key): return [r for r in rows if r[key] in new], [r for r in rows if r[key] not in new]
def cs_m(rows): return fd.cs_metrics(rows)
def bc_m(rows): return fd.bc_metrics(rows)
def sk_m(rows): return fd.sk_metrics(rows)
cs_n, cs_o = part(cs, "module"); bc_n, bc_o = part(bc, "module"); sk_n, sk_o = part(sk, "module")
def dfsplit(dj, keep):
    out = {}
    for key in ("per_module_pages", "per_module_clean", "per_module", "per_module_pages_with_class"):
        out[key] = {m: v for m, v in dj.get(key, {}).items() if (m in new) == keep}
    return out
df_n, df_o = dfsplit(df, True), dfsplit(df, False)
def show(label, c, b, s, d):
    print(f"== {label}")
    print(f"  skeleton: pairs {s['sk_pages']}  SCAFFOLD {s['sk_mean']:.4f}  >=50 {s['sk_ge50']}  >=75 {s['sk_ge75']}" + (f"  >=90 {s['sk_ge90']}" if 'sk_ge90' in s else ""))
    print(f"  compare_structure: matched {c.get('cs_matched')}  exact {c['cs_exact']}  EXTRA {c['cs_extra']}  missing {c['cs_missing']}  row-wrap {c.get('cs_rowwrap', c.get('cs_row_wrap'))}")
    print(f"  body_compare: pages {b['body_pages']}  ANY {b['body_any']}")
    print(f"  defect: clean {d['df_clean']} / {d['df_total']} = {d['df_clean_pct']:.2f} %  leak {d['df_leak_occ']} occ / {d['df_leak_pages']} pages")
show("PRE-EXISTING population (must equal the last shipped round EXACTLY)", cs_m(cs_o), bc_m(bc_o), sk_m(sk_o), fd.df_metrics(df_o))
show("NEW batch (its own figures)", cs_m(cs_n), bc_m(bc_n), sk_m(sk_n), fd.df_metrics(df_n))
show("WHOLE population (the re-based absolutes)", cs_m(cs), bc_m(bc), sk_m(sk), fd.df_metrics(df))
if len(sys.argv) > 2:
    p2 = sys.argv[2] if os.path.isabs(sys.argv[2]) else os.path.join(os.environ.get("PWD", HERE), sys.argv[2]); old = json.load(open(p2))["per_page"]
    om = {(r["module"], r["page"]): r["scaffold"] for r in old}
    mv = [(k, om[k], r["scaffold"]) for r in sk_o for k in [(r["module"], r["page"])] if k in om and abs(om[k] - r["scaffold"]) > 1e-12]
    print(f"== pre-existing pages vs {os.path.basename(sys.argv[2])}: movers {len(mv)}")
    for k, a, b in mv[:20]: print("   ", k, f"{a*100:.2f} -> {b*100:.2f}")
# the new batch, per module
print("== NEW batch per module (skeleton mean / pairs; body ANY; leak pages)")
per = {}
for r in sk_n: per.setdefault(r["module"], []).append(r["scaffold"])
bcany = {}
for r in bc_n:
    if fd._bc_broken(r): bcany[r["module"]] = bcany.get(r["module"], 0) + 1
leak = {m: v.get("A_literal_tag_leak", 0) for m, v in df_n.get("per_module_pages_with_class", {}).items() if v.get("A_literal_tag_leak")}
for m in sorted(new):
    v = per.get(m, [])
    print(f"  {m:8s} sk {sum(v)/len(v)*100 if v else 0:6.1f} % / {len(v):2d} pairs   bodyANY {bcany.get(m, 0)}   leak-pages {leak.get(m, 0)}")
