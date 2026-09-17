#!/usr/bin/env python3
"""Session 22 pre-coding measure, variants that need NO lesson-number source:
  L  (letters only): on a page, a box whose letter is not a single unused A-Z (placeholder X, a duplicate)
                     takes the next unused letter; digits untouched.
  DL (mode digit + letters): as L, plus a box whose digit differs from the page's majority digit
                     (>= 2 boxes, a strict majority) takes the majority digit first.
Paired effect vs the gold over the gate's pairs, per template.
"""
import os, sys, re, json, collections, string
BASE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(BASE, "..", "reference", "tests"))
if BASE in sys.path:
    sys.path.remove(BASE)
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN

RE_ACT = re.compile(r'<div\b[^>]*\bclass="[^"]*\bactivity\b[^"]*"[^>]*\bnumber="([^"]*)"')
RE_LET = re.compile(r'^(\d+)([A-Za-z]?)$')

def nums(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    return RE_ACT.findall(t), t

def eligible(lst):
    if not lst or len(lst) > 26 or any("." in x for x in lst): return False
    if not all(RE_LET.match(x) and RE_LET.match(x).group(2) for x in lst): return False
    return True

def fix(lst, with_digit):
    if not eligible(lst): return list(lst)
    ds = [int(RE_LET.match(x).group(1)) for x in lst]
    mode = None
    if with_digit and len(ds) >= 2:
        c = collections.Counter(ds).most_common()
        if len(c) == 1 or c[0][1] > c[1][1]:
            if c[0][1] * 2 > len(ds): mode = c[0][0]
    used = set(); out = []   # used = full numbers: letters restart at A for every digit (1A, 2A, 3A are distinct)
    for x in lst:
        d, l = RE_LET.match(x).groups(); l = l.upper(); d = int(d)
        if mode is not None: d = mode
        if not (len(l) == 1 and l in string.ascii_uppercase and (d, l) not in used):
            l = next(c for c in string.ascii_uppercase if (d, c) not in used)
        used.add((d, l)); out.append("%d%s" % (d, l))
    return out

def main():
    P = {v: collections.defaultdict(collections.Counter) for v in ("L", "DL")}
    ex = collections.defaultdict(list); changed = {v: collections.defaultdict(set) for v in ("L", "DL")}
    for code in _corpus.gate_mods(CLAUDE):
        mm = _corpus.mdir(HUMAN, code)
        parent = os.path.basename(os.path.dirname(mm)) if mm else "flat"
        tmpl = parent if parent in _corpus.TEMPLATE_DIRS else "flat"
        cdir = _corpus.mdir(CLAUDE, code)
        for f in sorted(os.listdir(cdir)):
            if not f.endswith(".html"): continue
            l, t = nums(os.path.join(cdir, f))
            for v, wd in (("L", False), ("DL", True)):
                if fix(l, wd) != l: changed[v][tmpl].add((code, f))
        for n, cp, hp in pairs(code):
            if not (cp and hp and os.path.exists(cp) and os.path.exists(hp)): continue
            gl, gt = nums(hp); cl, ct = nums(cp)
            if not gl or not cl: continue
            for v, wd in (("L", False), ("DL", True)):
                new = fix(cl, wd); S = P[v][tmpl]
                S["pairs"] += 1
                if new != cl: S["changed"] += 1
                now, after = (gl == cl), (gl == new)
                S["match-now"] += now; S["match-after"] += after
                if now and not after:
                    S["LOST"] += 1
                    if len(ex[v + "-lost-" + tmpl]) < 8: ex[v + "-lost-" + tmpl].append((code, os.path.basename(hp), gl[:6], cl[:6], new[:6]))
                if after and not now:
                    S["GAINED"] += 1
                    if len(ex[v + "-gained-" + tmpl]) < 8: ex[v + "-gained-" + tmpl].append((code, os.path.basename(hp), gl[:6], cl[:6], new[:6]))
                m = min(len(gl), len(cl))
                S["boxes"] += m
                S["box-now"] += sum(1 for i in range(m) if gl[i] == cl[i])
                S["box-after"] += sum(1 for i in range(m) if gl[i] == new[i])
    for v in ("L", "DL"):
        print("==== variant", v)
        for t in sorted(P[v]): print("  ", t, dict(P[v][t]), "| Claude pages changed:", len(changed[v][t]), "modules", len({c for c, _ in changed[v][t]}))
    for k in sorted(ex):
        print("==", k)
        for e in ex[k]: print("   ", e)
    json.dump({"paired": P, "changed": {v: {t: sorted(s) for t, s in d.items()} for v, d in changed.items()}},
              open(os.path.join(BASE, "_s22_actnum5.json"), "w"), indent=1, default=dict)

main()
