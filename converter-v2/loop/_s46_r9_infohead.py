#!/usr/bin/env python3
"""Session 46 Round 9 — hover definitions whose FIRST LETTERS Claude drops: a Claude info= value V such that the SAME module's gold
carries an info= value that is (1–3 characters) + V (normalised). The writer's run split (`[roll over definition:` red, ` T ` red,
`o move to …` black) — the red first letter is lost. Also the reverse (Claude longer). WSL, from outputs/:
    python3 _s46_r9_infohead.py > _s46_r9_infohead.log"""
import os, re, sys, glob, io, collections, html as H
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
def n(t): return re.sub(r"\s+", " ", H.unescape(t)).strip()
def infos(d):
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*.html"))):
        s = io.open(p, encoding="utf-8", errors="replace").read()
        out += [(os.path.basename(p), n(v)) for v in re.findall(r'info="([^"]*)"', s)]
    return out
cut = collections.Counter(); rows = []; mods = collections.Counter(); total = 0
for code in _corpus.gate_mods(GOLD):
    gd = _corpus.mdir(GOLD, code); cd = _corpus.mdir(CL, code)
    if not os.path.isdir(cd): continue
    gv = [v for _, v in infos(gd)]; gset = set(v.lower() for v in gv)
    for page, v in infos(cd):
        total += 1
        if not v or v.lower() in gset: continue
        low = v.lower()
        hit = next((g for g in gv if len(g) > len(v) and len(g) - len(v) <= 3 and g.lower().endswith(low) and len(v) >= 6), None)
        if hit:
            cut[hit[: len(hit) - len(v)]] += 1; mods[code] += 1
            rows.append(f"  {code:9s} {page:22s} claude «{v[:60]}»  gold «{hit[:60]}»")
print(f"Claude info= values {total}; first letters dropped (gold = 1–3 chars + Claude's): {sum(cut.values())} in {len(mods)} modules")
print("dropped prefixes:", dict(cut.most_common(20)))
print("modules:", dict(mods.most_common(30)))
print("\n".join(rows))
