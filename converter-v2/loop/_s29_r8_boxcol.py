#!/usr/bin/env python3
"""_s29_r8_boxcol.py — the activity box's OWN column class (the first `div.col-*` inside the box's first `div.row`): gold vs Claude,
per subject | template and per family prefix, split by box kind (interactive / plain). The r331-declined widened wrapper re-measured
per FAMILY (the intake families were never in that census). Run under WSL from CONVERTER_V2/reference/tests:
python3 ../../outputs/_s29_r8_boxcol.py
"""
import os, re, sys, json, glob, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_"); GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]

def boxes(html):
    out = []; stack = []
    for m in re.finditer(r"<(/?)div\b([^>]*)>", html):
        if m.group(1):
            if stack:
                st = stack.pop()
                if st[1] is not None: out.append((st[1], st[0], html[st[2]:m.start()]))
        else:
            if m.group(2).rstrip().endswith("/"): continue
            cls = re.search(r'class="([^"]*)"', m.group(2)); c = cls.group(1) if cls else ""
            num = re.search(r'number="([^"]*)"', m.group(2))
            isact = bool(re.search(r"(^|\s)activity(\s|$)", c)) and "cv2" not in c
            stack.append((c, (num.group(1).upper() if num else "-") if isact else None, m.end()))
    return out

def first_col(inner):
    m = re.search(r'<div class="row[^"]*">\s*<div class="([^"]*)"', inner)
    if not m: return "(no row>col)"
    return " ".join(sorted(m.group(1).split()))

def prefix(code): return re.match(r"[A-Z]+", code).group(0)

mods = _corpus.gate_mods(CLAUDE)
G = collections.defaultdict(collections.Counter); C = collections.defaultdict(collections.Counter)
Gf = collections.defaultdict(collections.Counter); Cf = collections.defaultdict(collections.Counter)
pages_by_fam = collections.defaultdict(set)
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); g = (mm.get("template_type", ""), mm.get("subject", "")); fam = prefix(code)
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        for n, cl, inner in boxes(gh):
            kind = "interactive" if "interactive" in cl.split() else "plain"
            G[(g, kind)][first_col(inner)] += 1; Gf[(fam, kind)][first_col(inner)] += 1
        for n, cl, inner in boxes(c):
            kind = "interactive" if "interactive" in cl.split() else "plain"
            C[(g, kind)][first_col(inner)] += 1; Cf[(fam, kind)][first_col(inner)] += 1
            pages_by_fam[fam].add(cp)
def show(D, E, label):
    print("\n== %s: gold col class (top) vs Claude (top), n >= 10 ==" % label)
    for k, cnt in sorted(D.items(), key=lambda x: -sum(x[1].values())):
        n = sum(cnt.values())
        if n < 10: continue
        top, tv = cnt.most_common(1)[0]
        cc = E.get(k, collections.Counter()); cn = sum(cc.values()); ctop = cc.most_common(1)[0] if cn else ("-", 0)
        flag = "  <-- DIFFERS" if cn and ctop[0] != top and tv / n >= 0.6 else ""
        print("  %-40s %-12s gold n=%4d  %-22s %.2f | claude n=%4d  %-22s %.2f%s" % (str(k[0])[:40], k[1], n, top, tv / n, cn, ctop[0], (ctop[1] / cn) if cn else 0, flag))
show(G, C, "subject|template")
show(Gf, Cf, "family prefix")
