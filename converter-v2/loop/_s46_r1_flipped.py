#!/usr/bin/env python3
"""Session 46 Round 1 — which accordion bundles flipped between two dumps (OFF → ON). WSL, from outputs/:
    python3 _s46_r1_flipped.py [_s46_r1_accdump_OFF.json] [_s46_r1_accdump.json]"""
import json, sys, collections
a = sys.argv[1] if len(sys.argv) > 1 else "_s46_r1_accdump_OFF.json"
b = sys.argv[2] if len(sys.argv) > 2 else "_s46_r1_accdump.json"
key = lambda r: (r["code"], r["page"], r["index"])
A = {key(r): r for r in json.load(open(a))}
B = {key(r): r for r in json.load(open(b))}
sys.argv = ["x"]
exec(open("_s46_r1_accclass.py").read().split("by = collections")[0])
up = [k for k in B if B[k]["built"] and k in A and not A[k]["built"]]
down = [k for k in B if not B[k]["built"] and k in A and A[k]["built"]]
print(f"built OFF {sum(r['built'] for r in A.values())} → ON {sum(r['built'] for r in B.values())}; newly built {len(up)}, newly declined {len(down)}; keys only in one: {len(set(A) ^ set(B))}")
by = collections.defaultdict(list)
for k in up: by[classify(A[k])].append(k)
for c, ks in sorted(by.items(), key=lambda x: -len(x[1])):
    print(f"  {len(ks):3d} {c:30s} " + ", ".join(f"{k[0]} {k[1]} #{k[2]}" for k in sorted(ks)))
for k in down: print("  DOWN", k)
