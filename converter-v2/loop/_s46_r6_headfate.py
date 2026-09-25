#!/usr/bin/env python3
"""Session 46 Round 6 — the black [Hn] lines (_s46_r6_blackhead.json): where does the gold put the text after the marker (its tag)?
WSL, from outputs/: python3 _s46_r6_headfate.py"""
import json, collections, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s46_goldloc import locate
R = json.load(open("_s46_r6_blackhead.json"))
print(len(R), "black heading lines", len(set(r["code"] for r in R)), "modules", len(set((r["code"], r["page"]) for r in R)), "pages")
fate = collections.Counter()
for r in R:
    lvl = re.match(r"^\s*\[\s*(?:heading\s*)?(h[1-6])", r["text"], re.I).group(1).lower()
    t = re.sub(r"^\s*\[[^\]}]*[\]}]\s*", "", r["text"]).replace("*", "").strip()
    if len(t) < 6:
        fate["(marker alone)"] += 1; print(f"   {r['code']} {r['page']} {'C' if r['consumed'] else ' '} {r['text'][:60]!r} | next {r['next']}"); continue
    h = locate(r["code"], t[:40])
    k = h[0][2] if h else "absent"
    fate[f"{lvl}->{k}"] += 1
    print(f"   {r['code']} {r['page']} {'C' if r['consumed'] else ' '} {r['text'][:60]!r} | gold: {k}")
print(dict(fate))
