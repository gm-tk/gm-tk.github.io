#!/usr/bin/env python3
"""Session 42 — the WRITER'S TAG behind a placement-census transition. For every gold block whose (gold region → Claude region)
matches the arguments (the `_placement_census.py` coarse regions, prefix-matched), find the block's line in the module's Writers
Template and the nearest writer tag(s) above it (red `[...]` markers within 8 lines, the block's own line first), then aggregate:
tag → blocks / pages / modules, per family, with examples. A tag the converter should have acted on = a recognition gap; no tag =
the developer's own choice (class C).
Usage (WSL, from CONVERTER_V2/reference/tests):
  python3 ../../outputs/_s42_wtctx.py body:alert body:free [--codes …] > ../../outputs/_s42_wtctx_<name>.log"""
import os, re, sys, collections
sys.path.append(os.path.join("..", "..", "outputs")); sys.path.insert(0, os.getcwd())
import _corpus, _discrepancy_audit as DA
from anchor_compare import CLAUDE, HUMAN
import _placement_census as PC

GA, CB = sys.argv[1], sys.argv[2]
codes = None
if "--codes" in sys.argv: codes = set(sys.argv[sys.argv.index("--codes") + 1:])
TAG = re.compile(r"\[([^\]\[]{1,60})\]")
def wt_lines(hd):
    out = []
    for f in sorted(os.listdir(hd)) if os.path.isdir(hd) else []:
        if f.endswith("_parsed.txt") and "media list_parsed" not in f.lower():
            out += open(os.path.join(hd, f), encoding="utf-8", errors="replace").read().splitlines()
    return out
def tags_of(line):
    s = re.sub(r"\[/?RED TEXT\]", "", line)
    red = "🔴" in line
    return [t.strip().lower()[:40] for t in TAG.findall(s) if red and not t.strip().lower().startswith(("url", "link", "http"))]
agg = collections.Counter(); pages = collections.defaultdict(set); mods = collections.defaultdict(set)
fam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list); total = 0; notfound = 0
for code in sorted(_corpus.gate_mods(CLAUDE)):
    if codes and code not in codes: continue
    hd = _corpus.mdir(HUMAN, code); f0 = re.match(r"[A-Z]+", code).group(0)
    W = wt_lines(hd); Wn = [PC.norm(re.sub(r"🔴|\[/?RED TEXT\]|\[[^\]]{0,60}\]", " ", l)) for l in W]
    for _, cp, hp in DA.pairs(code):
        G = [b for b in PC.parse(hp) if PC.keep(b[1])]; C = [b for b in PC.parse(cp) if PC.keep(b[1])]
        cmap = collections.defaultdict(list)
        for tag, t, raw, reg in C: cmap[t].append(reg); cmap["\x00" + t[:40]].append(reg)
        for tag, t, raw, greg in G:
            if not PC.coarse(greg).startswith(GA): continue
            cr = cmap.get(t) or (cmap.get("\x00" + t[:40]) if len(t) >= 40 else None)
            if not cr or any(PC.coarse(r) == PC.coarse(greg) for r in cr): continue
            if not any(PC.coarse(r).startswith(CB) for r in cr): continue
            total += 1
            key = t[:40]; li = next((i for i, n in enumerate(Wn) if key and key in n), None)
            if li is None:
                notfound += 1; k = "(text not in WT)"
            else:
                k = None
                for j in range(li, max(-1, li - 9), -1):
                    tg = tags_of(W[j])
                    if tg: k = (" + ".join(tg[:2])) + ("" if j == li else f"  (line -{li - j})"); break
                k = k or "(no tag within 8 lines)"
            kk = re.sub(r"\s+\(line -\d+\)$", "", k)
            agg[kk] += 1; pages[kk].add(f"{code}/{os.path.basename(cp)}"); mods[kk].add(code); fam[kk][f0] += 1
            if len(ex[kk]) < 5 and all(e[0] != code for e in ex[kk]): ex[kk].append((code, os.path.basename(cp), k, raw[:70]))
    PC._cache.clear()
print(f"{GA} -> {CB}: {total} blocks; WT line not found {notfound}")
for k, n in agg.most_common(45):
    print(f"{n:5d} blk {len(pages[k]):4d} pg {len(mods[k]):3d} mod  [{k}]  fam: " + ", ".join(f"{f} {c}" for f, c in fam[k].most_common(5)))
    for e in ex[k][:3]: print(f"        {e[0]} {e[1]} {e[2][:40]} “{e[3]}”")
