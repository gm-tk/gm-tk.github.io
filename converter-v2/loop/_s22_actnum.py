#!/usr/bin/env python3
"""Session 22 paired probe: activity `number=` attributes, gold vs Claude, per paired page.
The skeleton gate keeps `number` (KEEP_ATTR) so a wrong number is a mismatched line, but the miner
keys its classes by the full signature (one class per number value) so the mechanism never reaches
the floor. Here: per pair, the ordered list of numbers on each side; classify the page as
  SAME        identical lists
  DIGIT-SHIFT same count, every Claude lesson-digit differs from the gold's (letters may agree)
  LETTERS     same digits, different letter sequence / count
  OTHER       anything else
and check the WT: the digits of every `[Activity N?]`-style tag in the module's parsed WT.
"""
import os, sys, re, json, collections
BASE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(BASE, "..", "reference", "tests"))
if BASE in sys.path:
    sys.path.remove(BASE)
sys.path.insert(0, TESTS)
import _corpus
import _diff_miner as dm
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN

RE_ACT = re.compile(r'<div\b[^>]*\bclass="[^"]*\bactivity\b[^"]*"[^>]*\bnumber="([^"]+)"')
RE_NUM = re.compile(r'^(\d+)([A-Za-z]*)$')
RE_WTTAG = re.compile(r'\[(?:Activity|Interactive activity|Activity box|Interactive)[^\]\d]{0,40}?(\d{1,2})([A-Z])?\b', re.I)

def nums(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    return RE_ACT.findall(t.split("<body", 1)[1] if "<body" in t else t)

def split(n):
    m = RE_NUM.match(n.strip())
    return (int(m.group(1)), m.group(2).upper()) if m else (None, n)

def main():
    cls = collections.Counter(); bytmpl = collections.defaultdict(collections.Counter)
    ex = collections.defaultdict(list); mods = collections.defaultdict(set)
    for code in _corpus.gate_mods(CLAUDE):
        mm = _corpus.mdir(HUMAN, code)
        parent = os.path.basename(os.path.dirname(mm)) if mm else "flat"
        tmpl = parent if parent in _corpus.TEMPLATE_DIRS else "flat"
        wt = dm.wt_of(code) or ""
        if isinstance(wt, (tuple, list)):
            wt = "\n".join(x for x in wt if isinstance(x, str))
        wt_digits = collections.Counter(int(m.group(1)) for m in RE_WTTAG.finditer(wt))
        for n, cp, hp in pairs(code):
            if not (cp and hp and os.path.exists(cp) and os.path.exists(hp)):
                continue
            g, c = nums(hp), nums(cp)
            if not g and not c:
                continue
            gs, cs = [split(x) for x in g], [split(x) for x in c]
            gd = {d for d, _ in gs if d is not None}; cd = {d for d, _ in cs if d is not None}
            if g == c:
                k = "SAME"
            elif not g or not c:
                k = "ONE-SIDE-EMPTY"
            elif gd and cd and gd.isdisjoint(cd):
                k = "DIGIT-SHIFT"
            elif gd == cd:
                k = "LETTERS"
            else:
                k = "OTHER"
            cls[k] += 1; bytmpl[tmpl][k] += 1; mods[k].add(code)
            if k in ("DIGIT-SHIFT", "OTHER") and len(ex[k]) < 40:
                ex[k].append((code, os.path.basename(hp), g[:5], c[:5],
                              "wt-digits=" + ",".join("%d:%d" % kv for kv in sorted(wt_digits.items()))[:60]))
    print("classes:", dict(cls))
    for k in cls: print("  ", k, "modules", len(mods[k]))
    for t in sorted(bytmpl): print("  ", t, dict(bytmpl[t]))
    for k in ("DIGIT-SHIFT", "OTHER"):
        print("== examples", k)
        for e in ex[k][:25]: print("   ", e)
    json.dump({"classes": cls, "examples": ex, "modules": {k: sorted(v) for k, v in mods.items()}},
              open(os.path.join(BASE, "_s22_actnum.json"), "w"), indent=1)

main()
