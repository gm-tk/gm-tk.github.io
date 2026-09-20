#!/usr/bin/env python3
"""_s29_r10_alertlead.py — Claude's alert-family box whose FIRST CHILD is a bare <h4>/<p> (the span-mode lead emitted BEFORE the inner
row > col-12): count them, and for each find the gold box with the same lead text on the paired page — is the gold's lead INSIDE its
row > col-12 (wrapped) or bare? Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s29_r10_alertlead.py
"""
import os, re, sys, collections, json
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]
OPEN = re.compile(r'<div class="(alert(?: [^"]*)?|alertActivity|important[^"]*)"[^>]*>\s*(<(h[1-6]|p)\b[^>]*>)?', re.S)
WRAPPED = re.compile(r'<div class="(alert(?: [^"]*)?|alertActivity|important[^"]*)"[^>]*>\s*<div class="row">\s*<div class="col-12">\s*<(h[1-6]|p)\b[^>]*>([^<]{0,120})', re.S)
def fold(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip().lower()[:60]
def gold_forms(g):
    """map lead-text -> form for every gold alert box"""
    out = {}
    for m in re.finditer(r'<div class="(alert(?: [^"]*)?|alertActivity|important[^"]*)"[^>]*>', g):
        seg = g[m.end():m.end() + 600]
        w = re.match(r'\s*<div class="row">\s*<div class="col-12[^"]*">\s*<(h[1-6]|p)\b[^>]*>(.*?)</\1>', seg, re.S)
        b = re.match(r'\s*<(h[1-6]|p)\b[^>]*>(.*?)</\1>', seg, re.S)
        if w: out[fold(w.group(2))] = ("wrapped", w.group(1))
        elif b: out[fold(b.group(2))] = ("bare", b.group(1))
    return out
tot = collections.Counter(); bygroup = collections.defaultdict(collections.Counter); pages = set(); mods = set()
for code in _corpus.gate_mods(CLAUDE):
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); grp = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read(); g = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        gf = None
        for m in re.finditer(r'<div class="(alert(?: [^"]*)?|alertActivity|important[^"]*)"[^>]*>', c):
            seg = c[m.end():m.end() + 600]
            b = re.match(r'\s*<(h[1-6]|p)\b[^>]*>(.*?)</\1>\s*<div class="row">\s*<div class="col-12">', seg, re.S)
            if not b: continue
            if gf is None: gf = gold_forms(g)
            key = fold(b.group(2)); res = gf.get(key)
            verdict = "gold-absent" if res is None else ("gold-" + res[0] + "-" + res[1])
            tot[verdict] += 1; bygroup[grp][verdict] += 1; pages.add(cp); mods.add(code)
print("Claude bare-lead alert boxes (lead then row>col-12):", sum(tot.values()), "on", len(pages), "pages /", len(mods), "modules")
for k, v in tot.most_common(): print(f"   {k:28s} {v}")
print("\nby (template, subject):")
for grp, cnt in sorted(bygroup.items(), key=lambda x: -sum(x[1].values())):
    print(f"   {str(grp)[:48]:48s} n={sum(cnt.values()):3d}  " + "  ".join(f"{k}={v}" for k, v in cnt.most_common()))
