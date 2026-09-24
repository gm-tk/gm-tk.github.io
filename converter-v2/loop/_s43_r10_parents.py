#!/usr/bin/env python3
"""Session 43 Round 10 — the parent census for a link round: every <a href> the ON pages (outputs/_<TAG>_on/<CODE>/<page>) add
over the disk pages, by its immediate parent element. WSL, from reference/tests: python3 ../../outputs/_s43_r10_parents.py r478"""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE
tag = sys.argv[1]; ON = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"_{tag}_on")
A = re.compile(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S)
def anchors(s):
    out = collections.Counter()
    for m in A.finditer(s):
        # the nearest open element before the anchor
        pre = s[:m.start()]
        stack = []
        for t in re.finditer(r"<(/?)([a-zA-Z0-9]+)\b[^>]*?(/?)>", pre[-4000:]):
            if t.group(3) or t.group(2).lower() in ("br", "img", "hr", "input", "source", "meta", "link"): continue
            if t.group(1):
                while stack and stack.pop() != t.group(2).lower(): pass
            else: stack.append(t.group(2).lower())
        out[(m.group(1), stack[-1] if stack else "?")] += 1
    return out
par = collections.Counter(); ex = collections.defaultdict(list)
for code in sorted(os.listdir(ON)):
    cd = _corpus.mdir(CLAUDE, code)
    for p in glob.glob(os.path.join(ON, code, "*.html")):
        d = os.path.join(cd, os.path.basename(p))
        a_on = anchors(open(p, encoding="utf-8").read()); a_d = anchors(open(d, encoding="utf-8").read()) if os.path.exists(d) else collections.Counter()
        for k, n in (a_on - a_d).items():
            par[k[1]] += n
            if len(ex[k[1]]) < 4: ex[k[1]].append(f"{os.path.basename(p)} {k[0][:50]}")
print("added <a> by parent:", dict(par))
for k, v in ex.items(): print(f"  {k}: " + " ;; ".join(v))
