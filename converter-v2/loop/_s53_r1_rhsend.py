#!/usr/bin/env python3
"""_s53_r1_rhsend.py — session 53 Round 1: A RIGHT-HAND CALLOUT WITH AN EXPLICIT END. `[Alert RHS] … [end alert]` (and the
`[close alert box]` form r535 reads as an end): the explicit end switches the box to SPAN mode, which never takes the r505 / r506
side-column path. For every RHS callout OPEN (alert / important / side alert, ttext names rhs / rhc / right) in the WT item streams
(outputs/_s52_items/<CODE>.tsv): END (an end / close of it follows on the same page) or NO-END; its first content line; where the
GOLD puts that line (side column = a col-md-4 / col-lg-4 ancestor, or alert / alertActivity) and where Claude does.
WSL, from reference/tests/:  python3 ../../outputs/_s53_r1_rhsend.py > ../../outputs/_s53_r1_rhsend.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS
from _discrepancy_audit import pairs

O = os.path.dirname(os.path.abspath(__file__))
nt = CS.norm_text
famof = lambda m: re.sub(r"\d.*$", "", m)
CALL = {"alert", "important", "side alert"}

def items_of(mod):
    p = os.path.join(O, "_s52_items", mod + ".tsv")
    if not os.path.exists(p): return []
    out = []
    for line in open(p, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 9: continue
        pg, k, typ, tag, dirv, bold, ttext, payload, txt = f[:9]
        body = payload if typ == "tag" else txt
        out.append({"pg": int(pg), "type": typ, "tag": tag, "dir": dirv, "ttext": ttext, "n": nt(re.sub(r"\*+|<[^>]+>", "", body))})
    return out

def where(els, key):
    for e in els:
        if key and len(key) >= 8 and e["text"].startswith(key):
            ch = " ".join(e["chain"])
            side = bool(re.search(r"col-(?:md|lg)-4", ch))
            box = "alert" in ch.split() or "alertActivity" in ch
            return ("SIDE" if side else "main") + ("+box" if box else "")
    return None

res = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set); fams = collections.defaultdict(collections.Counter)
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE)
               if os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
for mod in mlist:
    items = items_of(mod); sites = []
    for x, it in enumerate(items):
        if not (it["type"] == "tag" and it["tag"] in CALL and it["dir"] == "CONTAINER_OPEN" and re.search(r"\b(rhs|rhc|right)", it["ttext"], re.I)): continue
        end = "NO-END"; first = it["n"][:40]
        for y in range(x + 1, len(items)):
            j = items[y]
            if j["pg"] != it["pg"]: break
            if j["type"] == "tag" and j["dir"] == "CONTAINER_OPEN" and j["tag"] in CALL: break
            if j["type"] == "tag" and j["dir"] == "CONTAINER_CLOSE" and j["tag"] in ("end alert", "end important", "end side alert"): end = "END"; break
            if j["type"] == "tag" and re.match(r"\[\s*close\s+(alert|important)", j["ttext"], re.I): end = "CLOSE"; break
            if not first and j["n"] and len(j["n"]) >= 8: first = j["n"][:40]
        if first: sites.append((end, first, it["ttext"]))
    if not sites: continue
    gels, cels = [], []
    for n, cp, hp in pairs(mod):
        cels += CS.parse_page(cp).elements; gels += CS.parse_page(hp).elements
    for end, k, tt in sites:
        kk = f"{end:6s} gold {where(gels, k)} claude {where(cels, k)}"
        res[kk] += 1; mods[kk].add(mod); fams[kk][famof(mod)] += 1
        if len(ex[kk]) < 4: ex[kk].append(f"{mod} {tt[:30]!r} -> {k[:40]!r}")
for kk, n in res.most_common():
    print(f"{n:4d} sites / {len(mods[kk]):3d} modules  {kk}   [{', '.join(f'{f} {x}' for f, x in fams[kk].most_common(6))}]")
    for e in ex[kk]: print("      e.g.", e)
