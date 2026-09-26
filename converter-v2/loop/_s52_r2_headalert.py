#!/usr/bin/env python3
"""_s52_r2_headalert.py — session 52 Round 2: every heading Claude renders (h2–h5), matched to the paired gold page by
(heading, text[:80]) — is the gold's heading inside an alert box, and is Claude's? Grouped by heading text (≥ 4 hits),
with the per-family split, so a heading-text-keyed box (a 'Lesson Summary' / 'Key points' convention) can be sized.
WSL, from reference/tests/:  python3 ../../outputs/_s52_r2_headalert.py > ../../outputs/_s52_r2_headalert.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS
famof = lambda m: re.sub(r"\d.*$", "", m)
tot = collections.Counter(); galert = collections.Counter(); calert = collections.Counter(); galert_cbare = collections.Counter()
fams = collections.defaultdict(collections.Counter); famsA = collections.defaultdict(collections.Counter)
mods = collections.defaultdict(set); modsA = collections.defaultdict(set); gcls = collections.defaultdict(collections.Counter)
unmatched = collections.Counter()
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE)
               if os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
for mod in mlist:
    cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        hindex = {}
        for e in hp.elements:
            if e["tag"][:1] == "h": hindex.setdefault(e["text"][:80], []).append(e)
        for e in cp.elements:
            if e["tag"] not in ("h2", "h3", "h4", "h5") or not e["text"]: continue
            t = e["text"][:40]
            m = hindex.get(e["text"][:80])
            if not m: unmatched[t] += 1; continue
            g = m.pop(0)
            if not m: del hindex[e["text"][:80]]
            tot[t] += 1; fams[t][famof(mod)] += 1; mods[t].add(mod)
            ga = "alert" in set(g["chain"]); ca = "alert" in set(e["chain"])
            if ga: galert[t] += 1; famsA[t][famof(mod)] += 1; modsA[t].add(mod)
            if ca: calert[t] += 1
            if ga and not ca: galert_cbare[t] += 1
rows = sorted((galert_cbare[t], t) for t in tot if galert_cbare[t] >= 3)
rows.reverse()
print(f"heading texts matched: {sum(tot.values())} headings; texts where the gold boxes it and Claude does not (>= 3):")
for n, t in rows[:40]:
    print(f"{n:4d} gold-alert/claude-bare | {t!r:42s} total {tot[t]:4d} gold-alert {galert[t]:4d} ({galert[t]/tot[t]:.2f}) claude-alert {calert[t]:3d} "
          f"mods {len(mods[t])} / alert-mods {len(modsA[t])} | gold-alert fams: {', '.join(f'{f} {c}' for f, c in famsA[t].most_common(6))} | all fams: "
          f"{', '.join(f'{f} {c}' for f, c in fams[t].most_common(6))}")
