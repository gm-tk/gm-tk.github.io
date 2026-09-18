#!/usr/bin/env python3
"""r392 skeleton delta: r391 -> r392 (_sk_final.json), movers named, bucket crossings, outside-affected check."""
import json
a = json.load(open('_s26_r392_sk_final.json')); b = json.load(open('_s26_r393_sk_final.json'))
aff = set(l.strip() for l in open('_s26_r393_affected.txt') if l.strip())
A = {p['page']: p for p in a['per_page']}; B = {p['page']: p for p in b['per_page']}
print(f"scaffold {a['scaffold_mean']*100:.4f} -> {b['scaffold_mean']*100:.4f} ({(b['scaffold_mean']-a['scaffold_mean'])*100:+.4f}pp); RAW {a['raw_mean']*100:.3f} -> {b['raw_mean']*100:.3f}; pairs {a['pages']} -> {b['pages']}, skipped {a['skipped_parse_errors']} -> {b['skipped_parse_errors']}")
mv = []
for k in B:
    if k in A and abs(B[k]['scaffold'] - A[k]['scaffold']) > 1e-9:
        mv.append((round((B[k]['scaffold'] - A[k]['scaffold']) * 100, 1), k, B[k]['module']))
mv.sort()
up = [m for m in mv if m[0] > 0]; dn = [m for m in mv if m[0] < 0]
print(f"movers {len(mv)}: up {len(up)} / down {len(dn)}; pp-sum {sum(m[0] for m in mv):+.1f}; outside affected {len([m for m in mv if m[2] not in aff])}")
print("worst:", [(m[0], m[1]) for m in mv[:6]])
print("best:", [(m[0], m[1]) for m in mv[-6:]])
for t in (0.5, 0.75, 0.9):
    ua = sum(1 for k in A if A[k]['scaffold'] >= t); ub = sum(1 for k in B if B[k]['scaffold'] >= t)
    cu = [(B[k]['module'], k) for k in B if k in A and A[k]['scaffold'] < t <= B[k]['scaffold']]
    cd = [(B[k]['module'], k) for k in B if k in A and B[k]['scaffold'] < t <= A[k]['scaffold']]
    print(f">= {int(t*100)}: {ua} -> {ub} up: {cu} down: {cd}")
