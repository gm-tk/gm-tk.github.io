#!/usr/bin/env python3
"""Session 22 follow-up: for every paired page where the activity digits differ (DIGIT-SHIFT / OTHER),
is Claude's digit its OWN page ordinal (self-consistent -> the pages are split differently from the
gold = a pairing / page-split question) or not (a numbering defect)? Same for the gold.
Ordinals: Claude from the filename `_N_M`; gold from its `<h1>N.M</h1>` chip, else the filename digits.
"""
import os, sys, re, json, collections
BASE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(BASE, "..", "reference", "tests"))
if BASE in sys.path:
    sys.path.remove(BASE)
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN

RE_ACT = re.compile(r'<div\b[^>]*\bclass="[^"]*\bactivity\b[^"]*"[^>]*\bnumber="(\d+)[A-Za-z]*"')
RE_CHIP = re.compile(r'<h1>\s*(\d+)\.(\d+)\s*</h1>')
RE_CORD = re.compile(r'_(\d+)_(\d+)\.html$')
RE_GORD = re.compile(r'[._-](\d{1,2})(?:[._](\d))?\.html$')

def digits(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    return [int(x) for x in RE_ACT.findall(t)], t

def main():
    out = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set)
    for code in _corpus.gate_mods(CLAUDE):
        mm = _corpus.mdir(HUMAN, code)
        parent = os.path.basename(os.path.dirname(mm)) if mm else "flat"
        tmpl = parent if parent in _corpus.TEMPLATE_DIRS else "flat"
        for n, cp, hp in pairs(code):
            if not (cp and hp and os.path.exists(cp) and os.path.exists(hp)):
                continue
            gd, gt = digits(hp); cd, ct = digits(cp)
            if not gd or not cd:
                continue
            gset, cset = set(gd), set(cd)
            if gset == cset:
                out["same-digits"] += 1; continue
            m = RE_CORD.search(os.path.basename(cp)); cord = int(m.group(1)) if m else None
            m2 = RE_CHIP.search(ct); cchip = int(m2.group(1)) if m2 else None
            m3 = RE_CHIP.search(gt); gord = int(m3.group(1)) if m3 else None
            if gord is None:
                m4 = RE_GORD.search(os.path.basename(hp)); gord = int(m4.group(1)) if m4 else None
            c_self = (cord is not None and cset == {cord})
            g_self = (gord is not None and gset == {gord})
            ord_same = (cord == gord)
            key = "claude-self=%s gold-self=%s ordinals-equal=%s" % (c_self, g_self, ord_same)
            out[key] += 1; mods[key].add(code)
            if len(ex[key]) < 8:
                ex[key].append((code, os.path.basename(hp), sorted(gset), "gord=%s" % gord, os.path.basename(cp), sorted(cset), "cord=%s chip=%s" % (cord, cchip)))
    for k, v in out.most_common():
        print("%5d  %-60s modules %d" % (v, k, len(mods.get(k, ()))))
    for k in ex:
        print("==", k)
        for e in ex[k]: print("   ", e)

main()
