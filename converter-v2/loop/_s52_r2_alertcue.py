#!/usr/bin/env python3
"""_s52_r2_alertcue.py — session 52 Round 2: THE div.alert MISSING CUE CENSUS (the s51-r13 lead). For every gold alert box
(a run of consecutive gold elements whose chain holds 'alert') whose first element Claude renders WITHOUT an alert, find
that text in the module's WT item stream (outputs/_s52_items/<CODE>.tsv) and report the writer's cue: the item itself
(its tag / bold lead) and the nearest non-empty item before it. Grouped by cue, family, template. WSL, from reference/tests/:
    python3 ../../outputs/_s52_r2_alertcue.py > ../../outputs/_s52_r2_alertcue.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS

O = os.path.join(os.path.dirname(os.path.abspath(__file__)))
fam = lambda t: "h" if t.startswith("h") else t
famof = lambda m: re.sub(r"\d.*$", "", m)
nt = CS.norm_text

def items_of(mod):
    p = os.path.join(O, "_s52_items", mod + ".tsv")
    if not os.path.exists(p): return []
    out = []
    for line in open(p, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 9: continue
        pg, k, typ, tag, dirv, bold, ttext, payload, txt = f[:9]
        body = payload if typ == "tag" else txt
        out.append({"pg": int(pg), "k": int(k), "type": typ, "tag": tag, "dir": dirv, "bold": bold, "ttext": ttext,
                    "payload": payload, "txt": txt, "n": nt(re.sub(r"\*+|<[^>]+>", "", body))})
    return out

def cue_of(items, idx):
    it = items[idx]
    j = idx - 1
    while j >= 0 and items[j]["pg"] == it["pg"] and not items[j]["n"] and items[j]["type"] != "tag": j -= 1
    pv = items[j] if j >= 0 and items[j]["pg"] == it["pg"] else None
    self_c = (f"tag:{it['tag']}" if it["type"] == "tag" else "black") + (":B" if it["bold"] else "")
    if pv is None: prev_c = "PAGESTART"
    elif pv["type"] == "tag": prev_c = f"tag:{pv['tag'] or pv['ttext'][:20]}" + ("+payload" if pv["n"] else "")
    else: prev_c = "black" + (":B" if pv["bold"] else "") + (":short" if len(pv["n"]) < 40 else "")
    return self_c, prev_c, pv

runs_total = 0; runs_missing = 0; found = 0
by_cue = collections.Counter(); by_self = collections.Counter(); by_prev = collections.Counter()
cue_mods = collections.defaultdict(set); cue_fams = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
lead_tags = collections.Counter(); prevtexts = collections.Counter()
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE)
               if os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
for mod in mlist:
    cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    if not cpages or not hpages: continue
    items = None
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        cindex = {}
        for e in cp.elements: cindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
        els = hp.elements; i = 0
        while i < len(els):
            if "alert" not in set(els[i]["chain"]): i += 1; continue
            j = i
            while j < len(els) and "alert" in set(els[j]["chain"]): j += 1
            run = els[i:j]; i = j; runs_total += 1
            first = next((e for e in run if len(e["text"]) >= 8), None)
            if not first: continue
            m = cindex.get((fam(first["tag"]), first["text"][:80]))
            if not m or "alert" in set(m[0]["chain"]): continue
            runs_missing += 1
            lead_tags[first["tag"]] += 1
            if items is None: items = items_of(mod)
            key = first["text"][:40]
            hit = next((x for x, it in enumerate(items) if key and key in it["n"]), None)
            if hit is None:
                by_cue["NOT-IN-WT-ITEMS"] += 1; cue_mods["NOT-IN-WT-ITEMS"].add(mod); continue
            found += 1
            s, p, pv = cue_of(items, hit)
            c = f"{s} <- {p}"
            by_cue[c] += 1; by_self[s] += 1; by_prev[p] += 1; cue_mods[c].add(mod); cue_fams[c][famof(mod)] += 1
            if pv is not None and pv["type"] == "black" and len(pv["n"]) < 40: prevtexts[pv["n"][:30]] += 1
            if pv is not None and pv["type"] == "tag": prevtexts["TAG " + (pv["ttext"][:30])] += 1
            if len(ex[c]) < 4:
                ex[c].append(f"{cpages[ci]} gold<{first['tag']}> {first['text'][:45]!r} | item {items[hit]['type']}:{items[hit]['tag']} "
                             f"{(items[hit]['payload'] or items[hit]['txt'])[:40]!r} | prev {(pv['ttext'] + ' ' + (pv['payload'] or pv['txt'])) [:50] if pv else '-'!r}")
print(f"gold alert runs {runs_total}; missing in Claude (first element bare) {runs_missing}; located in the WT items {found}")
print("gold lead element:", dict(lead_tags.most_common(6)))
print("\nITEM itself:", ", ".join(f"{k} {v}" for k, v in by_self.most_common(10)))
print("PREV item:  ", ", ".join(f"{k} {v}" for k, v in by_prev.most_common(14)))
print("\nPREV short texts / tags:", ", ".join(f"{k!r} {v}" for k, v in prevtexts.most_common(30)))
print()
for c, n in by_cue.most_common(22):
    print(f"{n:4d} runs / {len(cue_mods[c]):3d} modules  {c}   [{', '.join(f'{f} {x}' for f, x in cue_fams[c].most_common(6))}]")
    for e in ex[c]: print("      e.g.", e)
