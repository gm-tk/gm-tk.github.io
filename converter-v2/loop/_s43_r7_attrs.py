#!/usr/bin/env python3
"""Session 43 Round 7 PICK — THE ATTRIBUTE CENSUS (the skeleton scores tag + id + class; every other attribute is invisible to it).
Over the paired pages (the gate population), for every element SIGNATURE (tag + its first class token, e.g. `a`, `div.button`,
`iframe`, `img.img-fluid`, `div.TKmodal`) present in both corpora, the share of elements carrying each attribute NAME in the gold vs in
Claude, and — for attributes with a small value vocabulary — the dominant value in each. Ranked by (gold share − Claude share) ×
gold element count, so a large, consistent gold attribute Claude never emits floats to the top. Comments and <head> are skipped.
Run under WSL from reference/tests: python3 ../../outputs/_s43_r7_attrs.py > ../../outputs/_s43_r7_attrs.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
TAG = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)\b([^<>]*?)/?>", re.S)
ATTR = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+)))?')
SKIP_ATTRS = {"class", "id"}
def census(path, E, A, V):
    s = open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<head\b.*?</head>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S | re.I)
    for m in TAG.finditer(s):
        tag = m.group(1).lower()
        if tag in ("html", "body", "br", "hr", "span", "b", "i", "strong", "em", "u", "sup", "sub"): continue
        attrs = {}
        for a in ATTR.finditer(m.group(2)):
            attrs[a.group(1).lower()] = a.group(2) if a.group(2) is not None else (a.group(3) if a.group(3) is not None else (a.group(4) or ""))
        cls = (attrs.get("class") or "").split()
        sig = tag + ("." + cls[0] if cls else "")
        E[sig] += 1
        for k, v in attrs.items():
            if k in SKIP_ATTRS: continue
            A[(sig, k)] += 1
            if len(v) <= 40: V[(sig, k)][v] += 1
GE, GA, GV = collections.Counter(), collections.Counter(), collections.defaultdict(collections.Counter)
CE, CA, CV = collections.Counter(), collections.Counter(), collections.defaultdict(collections.Counter)
gm = collections.defaultdict(set)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    for _k, cp, gp in pairs(code):
        try:
            before = dict(GA); census(gp, GE, GA, GV); census(cp, CE, CA, CV)
            for key in GA:
                if GA[key] != before.get(key, 0): gm[key].add(code)
        except Exception: continue
rows = []
for (sig, k), gn in GA.items():
    ge, ce = GE[sig], CE.get(sig, 0)
    if ge < 50 or ce < 20: continue
    gs, cs = gn / ge, CA.get((sig, k), 0) / ce
    if gs - cs < 0.25: continue
    rows.append(((gs - cs) * ge, sig, k, ge, gs, ce, cs, len(gm[(sig, k)])))
rows.sort(reverse=True)
print("ATTRIBUTES THE GOLD CARRIES AND CLAUDE DOES NOT (signature present in both; gold share − Claude share ≥ 0.25)")
print("weight | signature | attr | gold elems | gold share | Claude elems | Claude share | gold modules | gold values (top) | Claude values (top)")
for w, sig, k, ge, gs, ce, cs, nm in rows[:45]:
    gv = ", ".join(f"{v!r}:{n}" for v, n in GV[(sig, k)].most_common(3))
    cv = ", ".join(f"{v!r}:{n}" for v, n in CV[(sig, k)].most_common(2))
    print(f"{w:7.0f} | {sig:28s} | {k:16s} | {ge:6d} | {gs:.2f} | {ce:6d} | {cs:.2f} | {nm:4d} | {gv[:90]} | {cv[:60]}")
print()
print("ATTRIBUTES CLAUDE CARRIES AND THE GOLD DOES NOT (Claude share − gold share ≥ 0.25)")
rows2 = []
for (sig, k), cn in CA.items():
    ge, ce = GE.get(sig, 0), CE[sig]
    if ce < 50 or ge < 20: continue
    gs, cs = GA.get((sig, k), 0) / ge, cn / ce
    if cs - gs < 0.25: continue
    rows2.append(((cs - gs) * ce, sig, k, ge, gs, ce, cs))
rows2.sort(reverse=True)
for w, sig, k, ge, gs, ce, cs in rows2[:25]:
    cv = ", ".join(f"{v!r}:{n}" for v, n in CV[(sig, k)].most_common(3))
    print(f"{w:7.0f} | {sig:28s} | {k:16s} | gold {ge:6d} {gs:.2f} | Claude {ce:6d} {cs:.2f} | {cv[:80]}")
