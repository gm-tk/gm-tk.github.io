#!/usr/bin/env python3
"""_s53_r1_emptyalert.py — session 53 Round 1: THE EMPTY [Alert] / [Important] FOLLOWED BY A TAGGED ITEM. The writer types the
callout tag alone on its line and then tags its content ([H3] Title, [Body] text). The strict gather collects only BLACK text, so
the box is empty. For every such WT site (outputs/_s52_items/<CODE>.tsv): the next tagged item's text and the black line after it
— where does the GOLD put them (inside an alert chain?) and where does Claude (same)? Grouped by the next tag, family, template.
WSL, from reference/tests/:  python3 ../../outputs/_s53_r1_emptyalert.py > ../../outputs/_s53_r1_emptyalert.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS
from _discrepancy_audit import pairs

O = os.path.dirname(os.path.abspath(__file__))
nt = CS.norm_text
famof = lambda m: re.sub(r"\d.*$", "", m)
CALL = {"alert", "important"}

def items_of(mod):
    p = os.path.join(O, "_s52_items", mod + ".tsv")
    if not os.path.exists(p): return []
    out = []
    for line in open(p, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 9: continue
        pg, k, typ, tag, dirv, bold, ttext, payload, txt = f[:9]
        body = payload if typ == "tag" else txt
        out.append({"pg": int(pg), "type": typ, "tag": tag, "dir": dirv, "ttext": ttext, "payload": payload, "txt": txt,
                    "n": nt(re.sub(r"\*+|<[^>]+>", "", body))})
    return out

def where(els, key):
    for e in els:
        if key and len(key) >= 6 and e["text"].startswith(key):
            ch = set(e["chain"])
            return "ALERT" if "alert" in ch else ("WIDGET" if any(c.startswith("cv2") or c in ("accordion", "tabs", "carousel") for c in ch) else "free"), e["tag"]
    return None, None

tpl_of = {}
for t in ("Standard", "Bilingual", "Fundamentals", "Inquiry"):
    d = os.path.join(CS._corpus.ROOT if hasattr(CS._corpus, "ROOT") else "", "01-Finalized_Modules_", t)
res = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set); fams = collections.defaultdict(collections.Counter)
follow = collections.Counter()
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE)
               if os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
for mod in mlist:
    items = items_of(mod)
    sites = []
    for x, it in enumerate(items):
        if not (it["type"] == "tag" and it["tag"] in CALL and it["dir"] == "CONTAINER_OPEN" and not it["n"]): continue
        if re.search(r"\b(rhs|rhc|right)\b", it["ttext"], re.I): continue
        y = x + 1
        while y < len(items) and items[y]["pg"] == it["pg"] and items[y]["type"] == "black" and not items[y]["n"]: y += 1
        if y >= len(items) or items[y]["pg"] != it["pg"] or items[y]["type"] != "tag": continue
        nx = items[y]
        kind = nx["tag"] if re.fullmatch(r"h[2-6]|body", nx["tag"] or "") else None
        if not kind: continue
        key1 = nx["n"][:40]
        z = y + 1
        while z < len(items) and items[z]["pg"] == it["pg"] and items[z]["type"] == "black" and not items[z]["n"]: z += 1
        key2 = items[z]["n"][:40] if z < len(items) and items[z]["pg"] == it["pg"] and items[z]["type"] == "black" else ""
        if not key1 and kind == "body" and key2: key1, key2 = key2, ""
        if not key1: continue
        nxt2 = items[z]["tag"] if z < len(items) and items[z]["type"] == "tag" else ("black" if key2 else "-")
        sites.append((kind, key1, key2, it["ttext"], nxt2))
    if not sites: continue
    gels, cels = [], []
    for n, cp, hp in pairs(mod):
        cels += CS.parse_page(cp).elements; gels += CS.parse_page(hp).elements
    for kind, k1, k2, tt, nxt2 in sites:
        g1, gt = where(gels, k1); c1, ct = where(cels, k1)
        g2, _ = where(gels, k2) if k2 else ("-", None); c2, _ = where(cels, k2) if k2 else ("-", None)
        kk = f"{kind:5s} gold {g1}/{g2} claude {c1}/{c2}"
        res[kk] += 1; mods[kk].add(mod); fams[kk][famof(mod)] += 1
        if len(ex[kk]) < 5: ex[kk].append(f"{mod} {tt[:28]!r} -> {k1[:40]!r} (gold<{gt}>) then {nxt2}:{k2[:30]!r}")
for kk, n in res.most_common():
    print(f"{n:4d} sites / {len(mods[kk]):3d} modules  {kk}   [{', '.join(f'{f} {x}' for f, x in fams[kk].most_common(6))}]")
    for e in ex[kk]: print("      e.g.", e)
