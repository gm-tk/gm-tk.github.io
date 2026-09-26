#!/usr/bin/env python3
"""_s53_r7_bodycls.py — session 53 Round 7: THE <body> CLASS, gold vs Claude, over every skeleton pair. Per (gold class set, Claude class
set): pages, modules, families; and for `mathJax` — whether the page carries math (<math> / \\( / $$ / MathJax script) on each side.
WSL, from reference/tests/:  python3 ../../outputs/_s53_r7_bodycls.py > ../../outputs/_s53_r7_bodycls.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
famof = lambda m: re.sub(r"\d.*$", "", m)
BODY = re.compile(r"<body\b([^>]*)>", re.I)
def bcls(p):
    s = open(p, encoding="utf-8", errors="replace").read()
    m = BODY.search(s); c = (re.search(r'class="([^"]*)"', m.group(1)) or [None, ""])[1] if m else "NOBODY"
    math = bool(re.search(r"<math\b|\\\(|\$\$|mathjax", s, re.I))
    return " ".join(sorted(c.split())) or "(none)", math
cnt = collections.Counter(); mods = collections.defaultdict(set); fams = collections.defaultdict(collections.Counter); mj = collections.Counter()
for mod in sorted(m for m in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m))):
    for n, cp, hp in pairs(mod):
        (g, gm), (c, cm) = bcls(hp), bcls(cp)
        k = (g, c); cnt[k] += 1; mods[k].add(mod); fams[k][famof(mod)] += 1
        if "mathJax" in g.split(): mj[("gold mathJax", "claude has math" if cm else "claude no math", "gold math" if gm else "gold no math")] += 1
for k, v in cnt.most_common(25):
    print(f"{v:5d} pages {len(mods[k]):4d} mods  gold [{k[0]}]  claude [{k[1]}]  {'SAME' if k[0] == k[1] else 'DIFF'}  [{', '.join(f'{f} {x}' for f, x in fams[k].most_common(6))}]")
print("\nmathJax pages:", mj.most_common())
