#!/usr/bin/env python3
"""ROUND 336 PICK probe (loop session 6) — the ACTIVITY BOX'S SUB-HEADINGS: every heading INSIDE an activity box after its
title (the first heading), gold vs Claude level per template; and, paired by the box's number= id on paired pages, the
gold level where Claude ships each level. The r334 sibling class (r334 pinned only the FIRST heading to h3).
Run from anywhere:  python3 _measure_r336_subhead.py   → prints the summary, writes _r336_subhead.json next to itself."""
import re, glob, os, collections, json, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
OPEN = re.compile(r'<div class="(activity[^"]*)"([^>]*)>')
HEAD = re.compile(r'<h([1-6])(?:\s[^>]*)?>')
DIV = re.compile(r'<div\b|</div>')

def boxes(html):
    """yield (class, number, inner_html) for every balanced activity div (nested activities are not expected)."""
    body = html.split('<div id="body"', 1)[-1]
    for m in OPEN.finditer(body):
        depth = 1; i = m.end()
        for d in DIV.finditer(body, m.end()):
            depth += 1 if d.group(0) == "<div" else -1
            if depth == 0: i = d.start(); break
        num = re.search(r'number="([^"]*)"', m.group(2)); yield m.group(1), (num.group(1) if num else ""), body[m.end():i]

def strip_widgets(inner):
    # drop cv2 hand-off boxes and note paragraphs so their headings do not count
    inner = re.sub(r'<div class="cv2-interactive[\s\S]*?</div>\s*</div>\s*</div>', '', inner)
    inner = re.sub(r'<p class="cv2-(?:note|comment)"[^>]*>[\s\S]*?</p>', '', inner)
    return inner

def census(root):
    sub = collections.defaultdict(collections.Counter); per_box = {}
    for f in glob.glob(os.path.join(ROOT, root, "*", "*", "*.html")):
        if re.search(r"acks|ackn", f, re.I): continue
        tmpl = os.path.basename(os.path.dirname(os.path.dirname(f))); code = os.path.basename(os.path.dirname(f))
        page = os.path.basename(f)
        s = open(f, encoding="utf-8", errors="replace").read()
        for cls, num, inner in boxes(s):
            hs = HEAD.findall(strip_widgets(inner))
            if len(hs) < 2: continue
            for lv in hs[1:]: sub[tmpl]["h" + lv] += 1
            per_box[(code, page, num)] = (tmpl, hs)
    return sub, per_box

gsub, gbox = census("01-Finalized_Modules_"); csub, cbox = census("01-Claude_Modules_")
print("== sub-heading levels inside activity boxes (2nd+ heading), per template ==")
for t in sorted(set(gsub) | set(csub)):
    gn = sum(gsub[t].values()); cn = sum(csub[t].values())
    print(f"{t:12} GOLD {dict(gsub[t].most_common())} (n={gn}, h4 share {gsub[t]['h4']/gn if gn else 0:.3f}) | CLAUDE {dict(csub[t].most_common())} (n={cn})")

# pair by (code, page key, number): gold pages are CODE-NN.M.html / CODE_N_M.html; Claude CODE_N_M.html — key on the number id + code only
def key(code, page, num):
    return (code, num)
gmap = collections.defaultdict(list)
for (code, page, num), (tmpl, hs) in gbox.items():
    if num: gmap[key(code, page, num)].append((tmpl, hs, page))
pair = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); mods = collections.defaultdict(set); writer = collections.Counter()
for (code, page, num), (tmpl, hs) in cbox.items():
    if not num or key(code, page, num) not in gmap: continue
    g = gmap[key(code, page, num)][0]
    ghs = g[1]
    # compare the 2nd+ headings position-wise while both have one
    for i in range(1, min(len(hs), len(ghs))):
        pair[tmpl][(f"gold h{ghs[i]}", f"claude h{hs[i]}")] += 1
        if ghs[i] != hs[i]: pages[tmpl].add((code, page)); mods[tmpl].add(code)
print("\n== paired boxes (same code + number=): gold level vs Claude level for the 2nd+ headings ==")
out = {"census_gold": {t: dict(v) for t, v in gsub.items()}, "census_claude": {t: dict(v) for t, v in csub.items()}, "paired": {}}
for t in sorted(pair):
    tot = sum(pair[t].values()); same = sum(v for (a, b), v in pair[t].items() if a[5:] == b[7:])
    print(f"{t:12} pairs {tot} same {same} ({same/tot if tot else 0:.3f}) | differing pages {len(pages[t])} modules {len(mods[t])}")
    for (a, b), v in pair[t].most_common(10): print(f"    {a:9} <= {b:10} {v}")
    out["paired"][t] = {"pairs": tot, "same": same, "diff_pages": sorted(f"{c}/{p}" for c, p in pages[t]), "diff_modules": sorted(mods[t]),
                        "table": {f"{a}|{b}": v for (a, b), v in pair[t].items()}}
json.dump(out, open(os.path.join(HERE, "_r336_subhead.json"), "w", encoding="utf-8"), indent=1)
print("TOTAL differing pages", sum(len(v) for v in pages.values()), "modules", len(set().union(*mods.values())) if mods else 0)
