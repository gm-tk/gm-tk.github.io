"""Session 17 PICK probe: context of the `p ⇐ h5` and `h5 ⇐ 2× repeated` substitution lines (Standard) — inside the module menu (the D10-9 named override) or in the body?"""
import os, sys, re, json, difflib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus, _skeleton_compare as S
from _discrepancy_audit import pairs, CLAUDE
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
want = {("p","h5"), ("h5","┌ 2× repeated:")}
ctx = collections.Counter(); pages = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in codes:
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary', os.path.basename(hp) + os.path.basename(cp), re.I): continue
        try: _, a, b = S.match(cp, hp, scaffold=True)
        except Exception: continue
        sm = difflib.SequenceMatcher(None, b, a, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "replace" or (i2 - i1) != (j2 - j1): continue
            for k,(gl, cl) in enumerate(zip(b[i1:i2], a[j1:j2])):
                key=(gl.strip(), cl.strip())
                if key not in want: continue
                j=j1+k
                # find nearest enclosing marker by scanning back for menu / body markers
                back=" | ".join(x.strip() for x in a[max(0,j-6):j])
                inmenu = any(re.search(r'module-menu|menu-content|nav', x) for x in a[max(0,j-12):j]) and not any(re.search(r'div#body|activity|div\.row', x) for x in a[max(0,j-12):j])
                indent = len(cl) - len(cl.lstrip())
                ctx[(key, 'menu' if inmenu else 'body')] += 1
                pages[(key, 'menu' if inmenu else 'body')].add(os.path.basename(cp))
                if len(ex[(key,'menu' if inmenu else 'body')])<12: ex[(key,'menu' if inmenu else 'body')].append((os.path.basename(cp), back, gl.strip()))
for k in ctx: print(k, ctx[k], "occ", len(pages[k]), "pages")
for k in ex:
    print("==",k)
    for e in ex[k]: print("  ",e)
