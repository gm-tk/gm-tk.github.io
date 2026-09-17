#!/usr/bin/env python3
"""Session 22 pre-coding measure, variant R2 (minimal):
  on a lesson page, for each numbered box in page order:
    digit  := the page's lesson number (Claude's own chip <h1>N.0</h1>/<h1>NN</h1>; else the mode of the
              page's own digits), when the box's digit differs;
    letter := the writer's letter if it is a single A-Z not yet used on the page, else the next unused
              letter (placeholders like X, duplicates).
  decimal MTK numbers and pages with no lesson number are left alone.
Paired effect vs the gold over the gate's pairs, per template; examples of GAINED / LOST.
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
RE_CHIP = re.compile(r'<h1>\s*(\d+)(?:\.\d+)?\s*</h1>')
RE_LET = re.compile(r'^(\d+)([A-Za-z]?)$')

def nums(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    return RE_ACT.findall(t), t

def lesson_no(t, lst):
    m = RE_CHIP.search(t)
    if m: return int(m.group(1))
    ds = [int(RE_LET.match(x).group(1)) for x in lst if RE_LET.match(x)]
    return collections.Counter(ds).most_common(1)[0][0] if ds else None

def r2(lst, ln):
    if ln is None or ln == 0 or any("." in x for x in lst) or not all(RE_LET.match(x) for x in lst):
        return list(lst), False
    if any(RE_LET.match(x).group(2) == "" for x in lst) or len(lst) > 26:
        return list(lst), False   # the bare-number form (single-page modules) is not this rule
    used = set(); out = []; changed = False
    for x in lst:
        d, l = RE_LET.match(x).groups(); l = l.upper()
        nd = ln
        if not (len(l) == 1 and l in string.ascii_uppercase and l not in used):
            l = next(c for c in string.ascii_uppercase if c not in used)
        used.add(l)
        y = "%d%s" % (nd, l)
        if y != x: changed = True
        out.append(y)
    return out, changed

def main():
    P = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
    changed_pages = collections.defaultdict(set)
    for code in _corpus.gate_mods(CLAUDE):
        mm = _corpus.mdir(HUMAN, code)
        parent = os.path.basename(os.path.dirname(mm)) if mm else "flat"
        tmpl = parent if parent in _corpus.TEMPLATE_DIRS else "flat"
        cdir = _corpus.mdir(CLAUDE, code)
        for f in sorted(os.listdir(cdir)):
            if not f.endswith(".html"): continue
            l, t = nums(os.path.join(cdir, f))
            if not l: continue
            new, ch = r2(l, lesson_no(t, l))
            if ch: changed_pages[tmpl].add((code, f))
        for n, cp, hp in pairs(code):
            if not (cp and hp and os.path.exists(cp) and os.path.exists(hp)): continue
            gl, gt = nums(hp); cl, ct = nums(cp)
            if not gl or not cl: continue
            new, ch = r2(cl, lesson_no(ct, cl))
            P[tmpl]["pairs"] += 1
            if ch: P[tmpl]["changed"] += 1
            now, after = (gl == cl), (gl == new)
            P[tmpl]["match-now"] += now; P[tmpl]["match-after"] += after
            if now and not after:
                P[tmpl]["LOST"] += 1
                if len(ex["lost-" + tmpl]) < 10: ex["lost-" + tmpl].append((code, os.path.basename(hp), gl[:6], cl[:6], new[:6]))
            if after and not now:
                P[tmpl]["GAINED"] += 1
                if len(ex["gained-" + tmpl]) < 10: ex["gained-" + tmpl].append((code, os.path.basename(hp), gl[:6], cl[:6], new[:6]))
            m = min(len(gl), len(cl))
            P[tmpl]["boxes"] += m
            P[tmpl]["box-now"] += sum(1 for i in range(m) if gl[i] == cl[i])
            P[tmpl]["box-after"] += sum(1 for i in range(m) if gl[i] == new[i])
            if ch and not now and not after:
                P[tmpl]["changed-still-mismatch"] += 1
                if len(ex["still-" + tmpl]) < 10: ex["still-" + tmpl].append((code, os.path.basename(hp), gl[:6], cl[:6], new[:6]))
    for t in sorted(P): print("  ", t, dict(P[t]), "| Claude pages R2 would change:", len(changed_pages[t]), "modules", len({c for c, _ in changed_pages[t]}))
    for k in sorted(ex):
        print("==", k)
        for e in ex[k]: print("   ", e)
    json.dump({"paired": P, "changed": {t: sorted(v) for t, v in changed_pages.items()}},
              open(os.path.join(BASE, "_s22_actnum4.json"), "w"), indent=1, default=dict)

main()
