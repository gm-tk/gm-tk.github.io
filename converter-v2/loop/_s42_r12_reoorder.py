#!/usr/bin/env python3
"""Session 42 Round 12 PICK — the MTK bilingual PAIR ORDER (KB c79 / 07D rule 7: MTK is Māori first). For every Bilingual-template paired
page, count adjacent same-tag element pairs `<X eng>…</X><X reo>…</X>` (English first) vs `<X reo>…<X eng>` (Māori first), per tag and
per container (activity box / free body / menu), on the gold and on Claude's page. Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus, _discrepancy_audit as DA
from anchor_compare import CLAUDE, HUMAN
PAIR = re.compile(r'<(h[1-6]|p|li)\s+(eng|reo)\b[^>]*>.*?</\1>\s*<\1\s+(eng|reo)\b[^>]*>', re.S)
def census(s):
    c = collections.Counter()
    for m in PAIR.finditer(s):
        a, b = m.group(2), m.group(3)
        if a == b: continue
        pre = s[:m.start()]
        where = "menu" if pre.rfind('id="module-menu-content"') > pre.rfind('id="body"') else (
            "activity" if pre.rfind('<div class="activity') > pre.rfind('</div>\n\t\t\t\t</div>') else "body")
        c[(m.group(1), where, "eng-first" if a == "eng" else "reo-first")] += 1
    return c
G = collections.Counter(); C = collections.Counter(); P = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    if "/Bilingual/" not in _corpus.mdir(CLAUDE, code).replace("\\", "/") + "/": continue
    for _, cp, hp in DA.pairs(code):
        g = census(open(hp, encoding="utf-8", errors="replace").read()); c = census(open(cp, encoding="utf-8", errors="replace").read())
        G.update(g); C.update(c)
        for k, n in c.items():
            if k[2] == "eng-first": P[k].add(f"{code}/{os.path.basename(cp)}")
print("tag  where     order       gold   claude   claude-pages")
for k in sorted(set(G) | set(C)):
    print(f"{k[0]:4s} {k[1]:9s} {k[2]:10s} {G[k]:6d} {C[k]:7d}   {len(P[k]) if k[2] == 'eng-first' else ''}")
for k in sorted(P, key=lambda k: -len(P[k]))[:4]:
    print(k, sorted(P[k])[:10])
