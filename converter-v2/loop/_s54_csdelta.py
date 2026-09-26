#!/usr/bin/env python3
"""_s54_csdelta.py — session 54: compare_structure's per-page exact / EXTRA / missing counts for two Claude page sets over the
same gold pages — the pages on disk (ON after a failed ship, or the shipped corpus) against a probe's SAVED pages
(PROBE_SAVE dir: <dir>/<CODE>/<page>.html) — and every element whose category changed. Reproduces compare_module()'s
index pairing and its categories exactly. WSL, from reference/tests/:
    python3 ../../outputs/_s54_csdelta.py MODLIST SAVEDIR [--saved-is-on]
By default the SAVED pages are the OFF side and the disk the ON side; --saved-is-on swaps them."""
import os, sys
sys.path.insert(0, os.getcwd())
import compare_structure as CS

mods = [l.strip() for l in open(sys.argv[1]) if l.strip()]
save = sys.argv[2]; saved_is_on = "--saved-is-on" in sys.argv
fam = lambda t: "h" if t.startswith("h") else t


def cats(cp, hp):
    hindex = {}
    for e in hp.elements: hindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
    out = []
    for e in cp.elements:
        m = hindex.get((fam(e["tag"]), e["text"][:80]))
        if not m: continue
        cch, hch = e["chain"], m[0]["chain"]
        if cch == hch: k = "exact"
        elif set(cch) == set(hch): k = "wrapper_set"
        else:
            cset, hset = set(cch), set(hch)
            if (cset - hset) & CS.CALLOUT_CLASSES: k = "EXTRA"
            elif (hset - cset) & CS.CALLOUT_CLASSES: k = "missing"
            elif "row" in hset and "row" not in cset: k = "rowwrap"
            else: k = "other"
        out.append((e["tag"], e["text"][:60], k, list(cch)[-3:], list(m[0]["chain"])[-3:]))
    return out


tot = {"exact": 0, "EXTRA": 0, "missing": 0}
bymod = {}
for mod in mods:
    cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    sdir = os.path.join(save, mod)
    if not cdir or not hdir or not os.path.isdir(sdir): continue
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    for ci in range(min(len(cpages), len(hpages))):
        sp = os.path.join(sdir, cpages[ci])
        if not os.path.exists(sp): continue
        hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        disk = cats(CS.parse_page(os.path.join(cdir, cpages[ci])), hp)
        saved = cats(CS.parse_page(sp), hp)
        on, off = (saved, disk) if saved_is_on else (disk, saved)
        d = {k: sum(1 for x in on if x[2] == k) - sum(1 for x in off if x[2] == k) for k in tot}
        if not any(d.values()): continue
        for k in tot: tot[k] += d[k]
        bymod[mod] = {k: bymod.get(mod, {}).get(k, 0) + d[k] for k in tot}
        print(f"{cpages[ci]:22s} ~ {hpages[ci]:24s} exact {d['exact']:+d}  EXTRA {d['EXTRA']:+d}  missing {d['missing']:+d}")
        offk = {}
        for x in off: offk.setdefault((x[0], x[1]), []).append(x[2])
        for x in on:
            was = offk.get((x[0], x[1]), ["?"]).pop(0) if offk.get((x[0], x[1])) else "?"
            if was != x[2] and (x[2] == "EXTRA" or was == "EXTRA"):
                print(f"     <{x[0]}> {x[1]!r}: {was} -> {x[2]}  claude {x[3]} human {x[4]}")
print("\nby module:", "; ".join(f"{m} ex{v['exact']:+d} EX{v['EXTRA']:+d} mi{v['missing']:+d}" for m, v in sorted(bymod.items(), key=lambda kv: -kv[1]['EXTRA'])))
print("TOTAL", tot)
