#!/usr/bin/env python3
"""_s29_r7_boxnum.py — THE ACTIVITY-NUMBER MISMATCH census: pair every Claude activity box with a gold box on the same paired page
by the box's TITLE (its first <h3>, unique on both sides), then compare the number= attribute: same / Claude numberless /
phase (leading digits) differs / letter differs / both. Per template | subject, with the mechanism hints (how many boxes each
side has on the page, whether the page is a single-file Fundamentals overview). Run under WSL from CONVERTER_V2/reference/tests:
python3 ../../outputs/_s29_r7_boxnum.py
"""
import os, re, sys, json, html as H, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_"); GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]
def fold(t): return re.sub(r"[^a-z0-9]+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t)).lower()).strip()

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
            stack.append((c, (num.group(1).upper().strip() if num else "-") if isact else None, m.end()))
    return out

def title(inner):
    s = re.sub(r"<!--[\s\S]*?-->", " ", inner)
    m = re.search(r"<h3\b([^>]*)>([\s\S]*?)</h3>", s)
    return fold(m.group(2)) if m else ""

def split_num(n):
    m = re.match(r"^(\d+(?:\.\d+)?)\s*([A-Z]?)$", n)
    return (m.group(1), m.group(2)) if m else (None, None)

mods = _corpus.gate_mods(CLAUDE)
C = collections.Counter(); G = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
pages_mis = set(); mods_mis = set(); per_mod = collections.Counter(); per_mod_tot = collections.Counter()
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); g = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        gb = [(n, title(i)) for n, cl, i in boxes(gh) if n != "-"]
        cb = [(n, title(i)) for n, cl, i in boxes(c)]
        gt = collections.Counter(x[1] for x in gb if x[1]); ct = collections.Counter(x[1] for x in cb if x[1])
        gmap = {x[1]: x[0] for x in gb if x[1] and gt[x[1]] == 1}
        for cn, ti in cb:
            if not ti or ct[ti] != 1 or ti not in gmap: continue
            gn = gmap[ti]
            per_mod_tot[code] += 1
            if cn == gn: k = "same"
            elif cn == "-": k = "Claude numberless"
            else:
                gp, gl = split_num(gn); cpp, cl = split_num(cn)
                if gp is None or cpp is None: k = "unparsed"
                elif gp != cpp and gl != cl: k = "phase AND letter differ"
                elif gp != cpp: k = "phase differs (letter same)"
                else: k = "letter differs (phase same)"
            C[k] += 1; G[g][k] += 1
            if k != "same":
                pages_mis.add(cp); mods_mis.add(code); per_mod[code] += 1
                if len(ex[k]) < 10: ex[k].append("%s %s gold #%s claude #%s «%s» (boxes gold %d / claude %d)" % (code, os.path.basename(cp), gn, cn, ti[:34], len(gb), len(cb)))
tot = sum(C.values())
print("Claude boxes title-paired with a gold box: %d | mismatched numbers %d = %.2f | pages %d / modules %d" % (tot, tot - C["same"], (tot - C["same"]) / tot, len(pages_mis), len(mods_mis)))
for k, v in C.most_common(): print("  %5d  %s" % (v, k))
print("\nby group (n paired, mismatch share, breakdown):")
for k, c in sorted(G.items(), key=lambda x: -(sum(x[1].values()) - x[1]["same"]))[:22]:
    n = sum(c.values()); mis = n - c["same"]
    print("  %-13s %-28s n=%4d mismatch %3d = %.2f  %s" % (k[0], k[1][:28], n, mis, mis / n, {kk: vv for kk, vv in c.most_common() if kk != "same"}))
print("\nmodules with the most mismatches:")
for code, v in per_mod.most_common(25): print("  %-9s %3d / %3d" % (code, v, per_mod_tot[code]))
print("\nexamples:")
for k, L in ex.items():
    print(" ", k)
    for e in L: print("     ", e)
