#!/usr/bin/env python3
"""Session 43 — compare two widget-loss census runs bundle by bundle (key = code, page, index, type).
Usage: python3 _s43_wl_compare.py <base.json> <on.json> [TYPE]"""
import json, sys, collections
A = {(r["code"], r["page"], r["index"], r["type"]): r for r in json.load(open(sys.argv[1]))}
B = {(r["code"], r["page"], r["index"], r["type"]): r for r in json.load(open(sys.argv[2]))}
T = sys.argv[3] if len(sys.argv) > 3 else None
cat = collections.defaultdict(list)
for k in sorted(set(A) | set(B)):
    if T and k[3] != T: continue
    a, b = A.get(k), B.get(k)
    if a and not b: cat["built -> BOX (lossy before)" if a["lost"] else "built -> BOX (lossless before)"].append(k)
    elif b and not a: cat["box -> BUILT"].append(k)
    elif a["lost"] and not b["lost"]: cat["lossy -> lossless build"].append(k)
    elif a["lost"] and b["lost"]:
        cat["lossy -> still lossy" + (" (fewer)" if b["lost"] < a["lost"] else "")].append(k)
    elif not a["lost"] and b["lost"]: cat["lossless -> LOSSY"].append(k)
for c, ks in cat.items():
    if c.startswith("lossless ->") is False and c == "lossy -> still lossy": pass
    print(f"{c}: {len(ks)} bundles / {len({k[0] for k in ks})} modules")
    if c != "unchanged":
        for k in ks[:60]:
            a, b = A.get(k), B.get(k)
            print(f"   {k[0]} p{k[1]} #{k[2]} {k[3]}  lost {a['lost'] if a else '-'} -> {b['lost'] if b else '-'}  " + (" || ".join((a or b)["lostText"])[:160]))
