#!/usr/bin/env python3
"""Session 22 pre-coding measure for the candidate rule
    R: every numbered activity box on a LESSON page is numbered <page ordinal><sequential letter A, B, C ...>
       in page order (decimal MTK numbers `N.M` and single-page modules excluded).
(1) GOLD convention, per template: share of gold lesson pages (>= 1 numbered box, letter form) whose
    numbers are exactly [ord+A, ord+B, ...]; and the weaker 'digits all == ordinal'.
(2) CLAUDE today: share of Claude lesson pages already in the R form; pages R would change.
(3) PAIRED effect: over gate pairs, the number-list agreement (gold list == Claude list) today vs
    under R applied to Claude's list (same box count kept). Also: pairs where the ordinals differ
    (a page-split difference R cannot fix) counted separately.
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
RE_CHIP = re.compile(r'<h1>\s*(\d+)\.(\d+)\s*</h1>')
RE_CORD = re.compile(r'_(\d+)_(\d+)\.html$')
RE_GORD = re.compile(r'[._-](\d{1,2})(?:[._](\d))?\.html$')
RE_LET = re.compile(r'^(\d+)([A-Z])$')

def nums(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    return RE_ACT.findall(t), t

def gold_ord(path, t):
    m = RE_CHIP.search(t)
    if m: return int(m.group(1))
    m = RE_GORD.search(os.path.basename(path))
    return int(m.group(1)) if m else None

def claude_ord(path):
    m = RE_CORD.search(os.path.basename(path))
    return int(m.group(1)) if m else None

def r_form(ordn, k):
    return ["%d%s" % (ordn, string.ascii_uppercase[i]) for i in range(k)]

def classify(lst, ordn):
    if not lst or ordn is None or ordn == 0: return "skip"
    if any("." in x for x in lst): return "decimal"
    if not all(RE_LET.match(x) for x in lst): return "other-form"
    if lst == r_form(ordn, len(lst)): return "R"
    if all(int(RE_LET.match(x).group(1)) == ordn for x in lst): return "digit-ok-letters-not"
    return "digit-wrong"

def main():
    gold = collections.defaultdict(collections.Counter); cl = collections.defaultdict(collections.Counter)
    paired = collections.defaultdict(collections.Counter)
    ex = collections.defaultdict(list)
    for code in _corpus.gate_mods(CLAUDE):
        mm = _corpus.mdir(HUMAN, code)
        parent = os.path.basename(os.path.dirname(mm)) if mm else "flat"
        tmpl = parent if parent in _corpus.TEMPLATE_DIRS else "flat"
        hdir = _corpus.mdir(HUMAN, code); cdir = _corpus.mdir(CLAUDE, code)
        for f in sorted(os.listdir(hdir)):
            if not f.endswith(".html"): continue
            p = os.path.join(hdir, f); l, t = nums(p); k = classify(l, gold_ord(p, t)); gold[tmpl][k] += 1
            if k == "digit-ok-letters-not" and len(ex["gold-" + tmpl]) < 6: ex["gold-" + tmpl].append((code, f, l[:6]))
        for f in sorted(os.listdir(cdir)):
            if not f.endswith(".html"): continue
            p = os.path.join(cdir, f); l, t = nums(p); k = classify(l, claude_ord(p)); cl[tmpl][k] += 1
        for n, cp, hp in pairs(code):
            if not (cp and hp and os.path.exists(cp) and os.path.exists(hp)): continue
            gl, gt = nums(hp); cll, ct = nums(cp)
            go, co = gold_ord(hp, gt), claude_ord(cp)
            if not gl or not cll or co is None or co == 0 or any("." in x for x in gl + cll): continue
            key = tmpl
            paired[key]["pairs"] += 1
            if go != co:
                paired[key]["ordinal-differs"] += 1
            now = (gl == cll); after = (gl == r_form(co, len(cll)))
            paired[key]["match-now"] += now; paired[key]["match-after-R"] += after
            if now and not after:
                paired[key]["LOST"] += 1
                if len(ex["lost-" + key]) < 8: ex["lost-" + key].append((code, os.path.basename(hp), gl[:5], cll[:5], co))
            if after and not now:
                paired[key]["GAINED"] += 1
                if len(ex["gained-" + key]) < 8: ex["gained-" + key].append((code, os.path.basename(hp), gl[:5], cll[:5], co))
            # per-box view: count of positions whose number agrees (min length)
            m = min(len(gl), len(cll))
            paired[key]["boxes"] += m
            paired[key]["box-agree-now"] += sum(1 for i in range(m) if gl[i] == cll[i])
            ra = r_form(co, len(cll))
            paired[key]["box-agree-after"] += sum(1 for i in range(m) if gl[i] == ra[i])
    print("== GOLD pages by template (R = ordinal + sequential letters) ==")
    for t in sorted(gold): print("  ", t, dict(gold[t]))
    print("== CLAUDE pages by template ==")
    for t in sorted(cl): print("  ", t, dict(cl[t]))
    print("== PAIRED effect by template ==")
    for t in sorted(paired): print("  ", t, dict(paired[t]))
    for k in sorted(ex):
        print("==", k)
        for e in ex[k]: print("   ", e)
    json.dump({"gold": gold, "claude": cl, "paired": paired}, open(os.path.join(BASE, "_s22_actnum3.json"), "w"), indent=1, default=dict)

main()
