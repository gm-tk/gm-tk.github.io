#!/usr/bin/env python3
"""_s53_r2_hlevel.py — session 53 Round 2: THE WRITER'S HEADING DIGIT vs THE GOLD'S LEVEL vs CLAUDE'S, per family. For every
`[H2]`–`[H5]` item (outputs/_s52_items) located as a heading in the BODY of the gold paired page: delta = gold level − writer digit,
and the same for Claude. Per family (and per template): the distribution of the gold's delta and Claude's, split by whether the
writer's digit is the page's TOP heading digit (the re-leveller ranks the page's levels to h3…). WSL, from reference/tests/:
    python3 ../../outputs/_s53_r2_hlevel.py > ../../outputs/_s53_r2_hlevel.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
sys.path.append(os.path.abspath(os.path.join("..", "..", "outputs")))
import _corpus
import _discrepancy_audit as DA
from anchor_compare import CLAUDE, HUMAN
import _placement_census as PC
O = os.path.abspath(os.path.join("..", "..", "outputs"))

def items_of(mod):
    p = os.path.join(O, "_s52_items", mod + ".tsv")
    if not os.path.exists(p): return []
    out = []
    for line in open(p, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 9: continue
        pg, k, typ, tag, dirv, bold, ttext, payload, txt = f[:9]
        body = payload if typ == "tag" else txt
        out.append({"pg": int(pg), "type": typ, "tag": tag, "ttext": ttext, "t": PC.norm(re.sub(r"\*+|<[^>]+>", "", body))})
    return out

famof = lambda m: re.sub(r"\d.*$", "", m)
tot = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list); mods = collections.defaultdict(set)
pages = collections.defaultdict(set)
for mod in sorted(m for m in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m))):
    items = items_of(mod)
    if not items: continue
    prs = DA.pairs(mod)
    if not prs: continue
    gix, cix, pg = {}, {}, {}
    for n, cp, hp in prs:
        for tag, t, raw, reg in PC.parse(hp):
            if reg.startswith("body") and re.fullmatch(r"h[1-6]", tag): gix.setdefault(t[:40], (int(tag[1]), reg)); pg.setdefault(t[:40], os.path.basename(cp))
        for tag, t, raw, reg in PC.parse(cp):
            if reg.startswith("body") and re.fullmatch(r"h[1-6]", tag): cix.setdefault(t[:40], (int(tag[1]), reg))
    top = {}
    for it in items:
        m = re.fullmatch(r"h([1-5])", it["tag"] or "")
        if it["type"] == "tag" and m: top[it["pg"]] = min(top.get(it["pg"], 9), int(m.group(1)))
    for it in items:
        m = re.fullmatch(r"h([1-5])", it["tag"] or "")
        if not (it["type"] == "tag" and m) or len(it["t"]) < 4: continue
        d = int(m.group(1)); k = it["t"][:40]
        if k not in gix: continue
        gl = gix[k][0]; cl = cix.get(k, (None,))[0]
        pos = "TOP" if d == top.get(it["pg"]) else "sub"
        key = (famof(mod), f"H{d}", pos)
        tot[key][(gl - d, None if cl is None else cl - d)] += 1; mods[key].add(mod); pages[key].add(pg.get(k))
fam_rows = collections.defaultdict(collections.Counter)
print("family  writer  pos   n  | gold delta dist | claude delta dist | cells (gold,claude) top")
rows = sorted(tot.items(), key=lambda kv: -sum(kv[1].values()))
for key, c in rows:
    n = sum(c.values())
    if n < 8: continue
    g = collections.Counter(); cc = collections.Counter()
    for (gd, cd), v in c.items(): g[gd] += v; cc[cd] += v
    print(f"{key[0]:8s} {key[1]:3s} {key[2]:3s} {n:5d} ({len(mods[key]):2d} m / {len(pages[key]):3d} p) | "
          + " ".join(f"{d:+d}:{v / n:.2f}" for d, v in g.most_common(3)) + " | "
          + " ".join(f"{('%+d' % d) if d is not None else 'ABS'}:{v / n:.2f}" for d, v in cc.most_common(3)) + " | "
          + ", ".join(f"{k}:{v}" for k, v in c.most_common(3)))
