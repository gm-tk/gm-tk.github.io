#!/usr/bin/env python3
"""_s53_tagfate.py — session 53 Round 2: THE WRITER-CUE FATE CENSUS (a NEW instrument; the s52 handover asked for the empty lanes
re-read with one). For every Writers-Template item (outputs/_s52_items/<CODE>.tsv — the engine's own item stream: a tag with its
payload, or a black line) find its text on the GOLD paired page and on CLAUDE's paired page (the placement census parser:
block tag + container region) and record its FATE on each side as `<tag>@<region>`. Aggregate by the writer's CUE (the item's own
tag, bold lead, list bullet) → the gold's forms vs Claude's forms, with the per-cue consensus: a cue whose gold form is consistent
(≥ 0.60) while Claude's dominant form differs is a candidate the skeleton rows may not show as one class (the cue unifies it).
WSL, from reference/tests/:  python3 ../../outputs/_s53_tagfate.py [--codes …] > ../../outputs/_s53_tagfate.log"""
import os, re, sys, collections, json
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
        raw = re.sub(r"<[^>]+>", "", body)
        out.append({"pg": int(pg), "type": typ, "tag": tag, "dir": dirv, "bold": bold, "ttext": ttext,
                    "bullet": bool(re.match(r"\s*(?:[•\-–]|\d+[.)])\s", raw)), "lead_bold": raw.lstrip().startswith("**"),
                    "t": PC.norm(re.sub(r"\*+", "", raw))})
    return out

def cue_of(it):
    if it["type"] == "tag":
        c = f"tag:{it['tag'] or '?'}"
    elif it["type"] == "black":
        c = "black"
    else:
        c = it["type"]
    if it["bullet"]: c += ":bullet"
    elif it["lead_bold"]: c += ":boldlead"
    return c

def index(blocks):
    ex, px = {}, {}
    for tag, t, raw, reg in blocks:
        if len(t) < 12: continue
        ex.setdefault(t, (tag, reg)); px.setdefault(t[:40], (tag, reg))
    return ex, px

def look(ix, t):
    ex, px = ix
    return ex.get(t) or px.get(t[:40])

def coarse(reg):
    return re.sub(r"panel\d+:", "panel:", reg)

args = sys.argv[1:]
codes = args[args.index("--codes") + 1:] if "--codes" in args else None
mods = codes or sorted(m for m in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m)))
fate = collections.Counter(); cue_tot = collections.Counter(); cue_gold = collections.defaultdict(collections.Counter)
cue_cl = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); mset = collections.defaultdict(set)
fams = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
t0 = __import__("time").time()
for mod in mods:
    items = items_of(mod)
    if not items: continue
    prs = DA.pairs(mod)
    if not prs: continue
    gb, cb = [], []
    pg_of = {}
    for n, cp, hp in prs:
        g = PC.parse(hp); c = PC.parse(cp)
        gb += g; cb += c
        for _, t, _, _ in g: pg_of.setdefault(t[:40], os.path.basename(cp))
    gix, cix = index(gb), index(cb)
    for it in items:
        if len(it["t"]) < 12: continue
        g = look(gix, it["t"])
        if not g: continue
        c = look(cix, it["t"])
        gf = f"{g[0]}@{coarse(g[1])}"; cf = f"{c[0]}@{coarse(c[1])}" if c else "ABSENT"
        cue = cue_of(it)
        cue_tot[cue] += 1; cue_gold[cue][gf] += 1; cue_cl[cue][cf] += 1
        if gf != cf:
            k = (cue, gf, cf); fate[k] += 1; mset[k].add(mod); fams[k][famof(mod)] += 1
            pages[k].add(pg_of.get(it["t"][:40], mod))
            if len(ex[k]) < 3: ex[k].append(f"{pg_of.get(it['t'][:40], mod)} {it['ttext'][:30]!r} {it['t'][:50]!r}")
print(f"modules {len(mods)}; items located on the gold {sum(cue_tot.values())}; in {__import__('time').time() - t0:.0f} s\n")
print("## Per cue — the gold's forms vs Claude's (top cues by located items)\n")
for cue, n in cue_tot.most_common(40):
    gtop = cue_gold[cue].most_common(3); ctop = cue_cl[cue].most_common(3)
    print(f"{n:6d}  {cue:28s} GOLD " + ", ".join(f"{f} {v / n:.2f}" for f, v in gtop) + "  |  CLAUDE " + ", ".join(f"{f} {v / n:.2f}" for f, v in ctop))
print("\n## Transitions (cue, gold form → Claude form), largest first — body/activity only, chrome excluded\n")
rows = [(k, v) for k, v in fate.items() if not re.search(r"@(header|menu|footer|acks)", k[1] + k[2])]
rows.sort(key=lambda kv: -kv[1])
for (cue, gf, cf), v in rows[:120]:
    k = (cue, gf, cf); share = cue_gold[cue][gf] / cue_tot[cue]
    print(f"{v:5d} items / {len(pages[k]):4d} pages / {len(mset[k]):3d} mods  {cue:24s} {gf:28s} → {cf:28s} (gold form share of cue {share:.2f})  "
          f"[{', '.join(f'{f} {x}' for f, x in fams[k].most_common(5))}]")
    for e in ex[k]: print("        e.g.", e)
json.dump({"|".join(k): [v, len(pages[k]), len(mset[k])] for k, v in fate.items()}, open(os.path.join(O, "_s53_tagfate.json"), "w"))
