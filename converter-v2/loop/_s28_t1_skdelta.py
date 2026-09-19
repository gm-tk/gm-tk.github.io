#!/usr/bin/env python3
"""session 28 / task 1 skeleton delta: the 19-Sept fast-loop baseline skeleton.json -> _s28_t1_sk_final.json;
movers named, bucket crossings, outside-affected check, the WJFUN / JPFUN family before -> after."""
import json, statistics
a = json.load(open('_fastloop_baseline/skeleton.json')); b = json.load(open('_s28_t1_sk_final.json'))
aff = set(l.strip() for l in open('_s28_t1_affected.txt') if l.strip())
A = {p['page']: p for p in a['per_page']}; B = {p['page']: p for p in b['per_page']}
print(f"scaffold {a['scaffold_mean']*100:.4f} -> {b['scaffold_mean']*100:.4f} ({(b['scaffold_mean']-a['scaffold_mean'])*100:+.4f}pp); RAW {a['raw_mean']*100:.3f} -> {b['raw_mean']*100:.3f}; pairs {a['pages']} -> {b['pages']}, skipped {a['skipped_parse_errors']} -> {b['skipped_parse_errors']}")
mv = []
for k in B:
    if k in A and abs(B[k]['scaffold'] - A[k]['scaffold']) > 1e-9:
        mv.append((round((B[k]['scaffold'] - A[k]['scaffold']) * 100, 1), k, B[k]['module']))
mv.sort()
up = [m for m in mv if m[0] > 0]; dn = [m for m in mv if m[0] < 0]
gone = [k for k in A if k not in B]; new = [k for k in B if k not in A]
print(f"movers {len(mv)}: up {len(up)} / down {len(dn)}; pp-sum {sum(m[0] for m in mv):+.1f}; outside affected {len([m for m in mv if m[2] not in aff])}; pairs gone {len(gone)} / new {len(new)}")
print("pairs gone (sample):", gone[:8]); print("pairs new (sample):", new[:8])
print("worst 10:", [(m[0], m[1]) for m in mv[:10]])
print("best 10:", [(m[0], m[1]) for m in mv[-10:]])
for t in (0.5, 0.75, 0.9):
    ua = sum(1 for k in A if A[k]['scaffold'] >= t); ub = sum(1 for k in B if B[k]['scaffold'] >= t)
    cu = [k for k in B if k in A and A[k]['scaffold'] < t <= B[k]['scaffold']]
    cd = [k for k in B if k in A and B[k]['scaffold'] < t <= A[k]['scaffold']]
    print(f">= {int(t*100)}: {ua} -> {ub}  up {len(cu)} {cu[:12]}  down {len(cd)} {cd}")
# the pre-existing (non-affected) population must be EXACT
pre = [k for k in B if k in A and B[k]['module'] not in aff]
print(f"unaffected pairs {len(pre)}: mean before {statistics.mean(A[k]['scaffold'] for k in pre)*100:.4f} after {statistics.mean(B[k]['scaffold'] for k in pre)*100:.4f}")
# per-family: WJFUN + JPFUN01/02 (the Task-3 class), and every intake prefix
def fam(pred, label):
    ka = [k for k in A if pred(A[k]['module'])]; kb = [k for k in B if pred(B[k]['module'])]
    if not kb: return
    print(f"  {label:10} pairs {len(ka):3} -> {len(kb):3}  mean {statistics.mean(A[k]['scaffold'] for k in ka)*100 if ka else 0:5.1f} -> {statistics.mean(B[k]['scaffold'] for k in kb)*100:5.1f}  median {statistics.median(B[k]['scaffold'] for k in kb)*100:5.1f}")
print("== families")
fam(lambda m: m.startswith('WJFUN') or m in ('JPFUN01', 'JPFUN02'), 'WJFUN+JPF')
import re
for p in sorted(set(re.match(r'[A-Z]+', m).group(0) for m in aff)):
    fam(lambda m, p=p: re.match(r'[A-Z]+', m).group(0) == p and m in aff, p)
# the per-module mean for the WJFUN family, before/after
pm_a = {}; pm_b = {}
for k, v in A.items(): pm_a.setdefault(v['module'], []).append(v['scaffold'])
for k, v in B.items(): pm_b.setdefault(v['module'], []).append(v['scaffold'])
w = sorted(m for m in pm_b if m.startswith('WJFUN') or m in ('JPFUN01', 'JPFUN02'))
print("== WJFUN/JPFUN per-module mean before -> after:")
print("  " + "  ".join(f"{m} {statistics.mean(pm_a.get(m, [0]))*100:.0f}->{statistics.mean(pm_b[m])*100:.0f}" for m in w))
