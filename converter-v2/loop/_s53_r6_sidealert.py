#!/usr/bin/env python3
"""_s53_r6_sidealert.py — session 53 Round 6: WHICH `[Alert]` / `[Important]` BOXES DOES THE GOLD PUT IN A SIDE COLUMN? For every
alert / important CONTAINER_OPEN item of the WT item streams (outputs/_s52_items) whose text (payload, else the next black line) is
found on the gold paired page: gold side (`body…:alert:side`) vs main, Claude side vs main; with the writer's cue — the bracket
text (ttext), the item BEFORE it (a media / heading / body / table…), the item AFTER, and the family. WSL, from reference/tests/:
    python3 ../../outputs/_s53_r6_sidealert.py > ../../outputs/_s53_r6_sidealert.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
sys.path.append(os.path.abspath(os.path.join("..", "..", "outputs")))
import _corpus
import _discrepancy_audit as DA
from anchor_compare import CLAUDE, HUMAN
import _placement_census as PC

O = os.path.abspath(os.path.join("..", "..", "outputs"))
famof = lambda m: re.sub(r"\d.*$", "", m)

def items_of(mod):
    p = os.path.join(O, "_s52_items", mod + ".tsv")
    if not os.path.exists(p): return []
    out = []
    for line in open(p, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 9: continue
        pg, k, typ, tag, dirv, bold, ttext, payload, txt = f[:9]
        body = payload if typ == "tag" else txt
        out.append({"pg": int(pg), "type": typ, "tag": tag, "dir": dirv, "ttext": ttext, "t": PC.norm(re.sub(r"\*+|<[^>]+>", "", body))})
    return out

def side(reg): return "SIDE" if reg.endswith(":side") else "main"
rows = []
for mod in sorted(m for m in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m))):
    items = items_of(mod)
    if not items: continue
    prs = DA.pairs(mod)
    if not prs: continue
    gix, cix = {}, {}
    for n, cp, hp in prs:
        for tag, t, raw, reg in PC.parse(hp):
            if len(t) >= 12 and "alert" in reg: gix.setdefault(t[:40], reg)
        for tag, t, raw, reg in PC.parse(cp):
            if len(t) >= 12: cix.setdefault(t[:40], reg)
    for x, it in enumerate(items):
        if not (it["type"] == "tag" and it["tag"] in ("alert", "important") and it["dir"] == "CONTAINER_OPEN"): continue
        key = it["t"][:40]
        if len(key) < 12:
            y = x + 1
            while y < len(items) and items[y]["type"] == "black" and not items[y]["t"]: y += 1
            key = items[y]["t"][:40] if y < len(items) and items[y]["type"] == "black" else ""
        if len(key) < 12 or key not in gix: continue
        prev = next((items[j] for j in range(x - 1, -1, -1) if items[j]["type"] != "black" or items[j]["t"]), None)
        nxt = next((items[j] for j in range(x + 1, len(items)) if items[j]["type"] == "tag" or items[j]["type"] == "table"), None)
        pc = (prev["tag"] or prev["type"]) if prev else "-"; nc = (nxt["tag"] or nxt["type"]) if nxt else "-"
        rows.append((famof(mod), mod, it["tag"], it["ttext"][:40], pc, nc, side(gix[key]), side(cix.get(key, "ABSENT")) if key in cix else "ABSENT", key))
tot = collections.Counter((r[6], r[7]) for r in rows)
print("gold / claude:", tot.most_common())
for label, idx in (("PREV item", 4), ("NEXT tag", 5), ("family", 0), ("tag", 2)):
    c = collections.defaultdict(collections.Counter)
    for r in rows: c[r[idx]][r[6]] += 1
    print(f"\n{label}: gold SIDE share (n ≥ 6)")
    for k, v in sorted(c.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(v.values())
        if n >= 6: print(f"  {k:24s} n={n:4d}  side {v['SIDE'] / n:.2f}  (claude side {sum(1 for r in rows if r[idx] == k and r[7] == 'SIDE') / n:.2f})")
print("\nthe gold-SIDE / Claude-main items:")
for r in rows:
    if r[6] == "SIDE" and r[7] != "SIDE": print("  ", r[:8])
