#!/usr/bin/env python3
"""_s53_r7_sigbal.py — session 53 Round 7: THE SKELETON BALANCE (alignment-free). For every paired page the skeleton gate's own
scaffold lines (`_skeleton_compare._skel(path, True)`), each reduced to `parent > sig` (its nearest shallower line = parent); the
multiset difference per page: DEFICIT (gold has, Claude lacks) and SURPLUS (Claude has, gold lacks), summed over all pairs; per row the
pages, modules and top families. A row the miner splits across many aligned classes shows here as ONE number.
WSL, from reference/tests/:  python3 ../../outputs/_s53_r7_sigbal.py > ../../outputs/_s53_r7_sigbal.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
import _skeleton_compare as K
from anchor_compare import CLAUDE, HUMAN

famof = lambda m: re.sub(r"\d.*$", "", m)

def ps(lines):
    out = []; stack = []
    for l in lines:
        d = len(l) - len(l.lstrip(" ")); sig = l.strip()
        if not sig: continue
        while stack and stack[-1][0] >= d: stack.pop()
        par = stack[-1][1] if stack else "ROOT"
        if sig.startswith("┌"):   # a repeat marker is transparent: its children keep the marker's own parent
            stack.append((d, par)); continue
        out.append(f"{par} > {sig}"); stack.append((d, sig))
    return collections.Counter(out)

DEF = collections.Counter(); SUR = collections.Counter()
dp = collections.defaultdict(set); sp = collections.defaultdict(set); dm = collections.defaultdict(set); sm = collections.defaultdict(set)
df = collections.defaultdict(collections.Counter); sf = collections.defaultdict(collections.Counter)
npg = 0
for mod in sorted(m for m in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m))):
    for n, cp, hp in pairs(mod):
        try: g = ps(K._skel(hp, True)); c = ps(K._skel(cp, True))
        except Exception: continue
        npg += 1; pg = os.path.basename(cp)
        for k in set(g) | set(c):
            d = g[k] - c[k]
            if d > 0: DEF[k] += d; dp[k].add(pg); dm[k].add(mod); df[k][famof(mod)] += d
            elif d < 0: SUR[k] += -d; sp[k].add(pg); sm[k].add(mod); sf[k][famof(mod)] += -d
print(f"pairs {npg}; deficit lines {sum(DEF.values())}; surplus lines {sum(SUR.values())}\n")
for title, C, P, M, F in (("DEFICIT (gold has, Claude lacks)", DEF, dp, dm, df), ("SURPLUS (Claude has, gold lacks)", SUR, sp, sm, sf)):
    print(f"## {title}\n")
    for k, v in C.most_common(45):
        print(f"{v:6d} lines {len(P[k]):5d} pages {len(M[k]):4d} mods  {k[:95]:95s}  [{', '.join(f'{f} {x}' for f, x in F[k].most_common(4))}]")
    print()
