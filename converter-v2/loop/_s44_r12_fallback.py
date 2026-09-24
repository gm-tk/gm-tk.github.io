#!/usr/bin/env python3
"""Session 44 Round 12 — KB c79's remaining mechanism: lesson pages whose header <h1><span> is the MODULE title (the overview's) — the
disclosed fallback — measured on the scored pairs: what the gold's paired page has, and whether the gold's lesson title is in the module's
Writers Template (and on which kind of WT line: a tag line, the lesson overview, a heading…). WSL, from reference/tests:
python3 ../../outputs/_s44_r12_fallback.py"""
import os, re, sys, glob, io, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus, _discrepancy_audit as DA
from anchor_compare import CLAUDE
ROOT = os.path.normpath(os.path.join(os.getcwd(), "..", "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
def h1s(p):
    s = io.open(p, encoding="utf-8", errors="replace").read()
    i = s.find('<div id="header"'); j = s.find('id="module-head-buttons"', i)
    seg = s[i:j if j > 0 else i + 3000]
    return [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", m))).strip() for m in re.findall(r"<h1><span>(.*?)</span></h1>", seg, re.S)]
def norm(t): return re.sub(r"[^\wĀ-ſ ]+", "", t.lower()).strip()
res = collections.Counter(); kinds = collections.Counter(); ex = []; mods = set(); fam = collections.Counter()
for code in _corpus.gate_mods(CLAUDE):
    try: cdir = _corpus.mdir(CLAUDE, code)
    except Exception: continue
    ov = os.path.join(cdir, f"{code}_0_0.html")
    if not os.path.exists(ov): continue
    ovt = [norm(x) for x in h1s(ov)]
    wts = glob.glob(os.path.join(_corpus.mdir(GOLD, code), "*_parsed.txt"))
    wt = "\n".join(io.open(w, encoding="utf-8", errors="replace").read() for w in wts)
    wtl = [(l, norm(re.sub(r"🔴|\[/?RED TEXT\]|\*", "", l))) for l in wt.split("\n")]
    for n, cp, hp in DA.pairs(code):
        if os.path.basename(cp).endswith("_0_0.html"): continue
        ct = [norm(x) for x in h1s(cp)]
        if not ct or ct != ovt: continue
        res["fallback"] += 1; mods.add(code); fam[re.match(r"[A-Z]+\d?", code).group(0)] += 1
        gt = h1s(hp)
        if not gt: res["gold none"] += 1; continue
        if [norm(x) for x in gt] == ovt: res["gold ALSO the module title"] += 1; continue
        g0 = norm(gt[0])
        hit = next((l for l, nl in wtl if g0 and len(g0) > 3 and g0 in nl), None)
        if not hit: res["gold own title, NOT in WT"] += 1; continue
        res["gold own title, IN WT"] += 1
        tag = re.search(r"\[([^\]]{1,40})\]", hit)
        kinds[(tag.group(1).strip().lower() if tag else "(untagged line)")] += 1
        if len(ex) < 14: ex.append(f"{code} {os.path.basename(cp)} gold «{gt[0][:40]}» WT: {re.sub(r'🔴|\[/?RED TEXT\]', '', hit).strip()[:90]}")
print("lesson pages on the module-title fallback:", dict(res), "modules", len(mods))
print("by family:", dict(fam.most_common(12)))
print("the WT line holding the gold's own title, by its tag:", dict(kinds.most_common(12)))
for e in ex: print("  ", e)
