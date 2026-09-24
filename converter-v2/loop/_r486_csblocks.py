#!/usr/bin/env python3
"""ROUND 486 — decompose compare_structure's movement BLOCK BY BLOCK: for every module of the affected set, classify every matched
Claude block (compare_structure's own parse_page / chain / category rules) on the OLD pages (outputs/_r486_off — the toggle-OFF
render) and the NEW pages (the disk), keyed by (page, tag family, text[:80]); print the old → new category transitions.
A block that was EXACT and is now anything else is a REAL regression; EXTRA → MISSING is a reclassification of a block that was
already mismatched. Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r486_csblocks.py"""
import os, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS
import _corpus
OUT = os.path.join(os.getcwd(), "..", "..", "outputs")
OFF = os.path.join(OUT, "_r486_off")
mods = [l.strip() for l in open(os.path.join(OUT, "_affected_r486.txt")) if l.strip()]
fam = lambda t: "h" if t.startswith("h") else t
def cat(cch, hch):
    if cch == hch: return "exact"
    if set(cch) == set(hch): return "wrapper_set"
    cset, hset = set(cch), set(hch)
    if (cset - hset) & CS.CALLOUT_CLASSES: return "EXTRA"
    if (hset - cset) & CS.CALLOUT_CLASSES: return "MISSING"
    if "row" in hset and "row" not in cset: return "row_wrap"
    return "other"
def blocks(cdir, hdir, mod):
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(_corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    out = collections.Counter(); ex = {}
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        hindex = {}
        for e in hp.elements: hindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
        for e in cp.elements:
            m = hindex.get((fam(e["tag"]), e["text"][:80]))
            if not m: continue
            k = (cpages[ci], fam(e["tag"]), e["text"][:80])
            c = cat(e["chain"], m[0]["chain"])
            out[(k, c)] += 1; ex[k] = (e["chain"], m[0]["chain"])
    return out, ex
trans = collections.Counter(); exs = collections.defaultdict(list)
for mod in mods:
    hdir = _corpus.mdir(CS.HUMAN, mod); ndir = _corpus.mdir(CS.CLAUDE, mod); odir = os.path.join(OFF, mod)
    if not os.path.isdir(odir): print("no OFF dir", mod); continue
    ob, oex = blocks(odir, hdir, mod); nb, nex = blocks(ndir, hdir, mod)
    ok = collections.defaultdict(list); nk = collections.defaultdict(list)
    for (k, c), n in ob.items(): ok[k] += [c] * n
    for (k, c), n in nb.items(): nk[k] += [c] * n
    for k in set(ok) | set(nk):
        a = sorted(ok.get(k, [])); b = sorted(nk.get(k, []))
        for i in range(max(len(a), len(b))):
            t = (a[i] if i < len(a) else "UNMATCHED", b[i] if i < len(b) else "UNMATCHED")
            if t[0] != t[1]:
                trans[t] += 1
                if len(exs[t]) < 6: exs[t].append(f"{mod}/{k[0]} «{k[2][:45]}» claude {list(nex.get(k, oex.get(k))[0])} gold {list(nex.get(k, oex.get(k))[1])}")
print("old → new category transitions (blocks whose category changed):")
for t, n in trans.most_common():
    print(f"  {n:3d}  {t[0]:10s} → {t[1]:10s}")
    for e in exs[t]: print("        ", e)
