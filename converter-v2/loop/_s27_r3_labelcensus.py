#!/usr/bin/env python3
"""Session 27 Round 1 instrument — THE POSITION-FREE LABEL CENSUS.
For every pair the PRIMARY gate scores (its own pairing, its own scaffold skeleton, its own labels), take the
skeleton as a MULTISET of labels (indent stripped) and diff the two multisets: per label, the count Claude has
over the gold (EXTRA) and under it (MISSING) — the lines that can never match whatever the alignment does.
Aggregated per label with pages / modules / template / subject; the per-page position-free ratio is also
reported (an upper bound on the gate's difflib ratio; the gap = the order loss).
  wsl: python3 _s27_r3_labelcensus.py  →  _s27_r3_labelcensus.out / .json"""
import os, sys, re, json, time
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
from _skeleton_compare import _skel
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict

meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf

def groups(code):
    tf = fam.get(code, "flat"); subj = (meta.get(code, {}) or {}).get("subject") or "None"
    return tf, subj

t0 = time.time()
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
EXTRA = Counter(); MISS = Counter()
EXTRA_P = defaultdict(set); MISS_P = defaultdict(set); EXTRA_M = defaultdict(set); MISS_M = defaultdict(set)
EXTRA_G = defaultdict(Counter); MISS_G = defaultdict(Counter)   # label -> group -> count
GOLD_TOT = Counter(); CL_TOT = Counter(); GOLD_PAGES = defaultdict(set); CL_PAGES = defaultdict(set)
npairs = 0; ratios = []; pf_ratios = []; order_gap = 0.0
per_page = []
for code in codes:
    tf, subj = groups(code)
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            a = [l.strip() for l in _skel(cp, True)]; b = [l.strip() for l in _skel(hp, True)]
        except Exception as e:
            print("PARSE ERROR", code, os.path.basename(cp), e); continue
        npairs += 1
        ca, cb = Counter(a), Counter(b)
        inter = sum((ca & cb).values())
        pf = 2.0 * inter / max(1, len(a) + len(b))
        pf_ratios.append(pf)
        for lab in set(ca) | set(cb):
            g, c = cb[lab], ca[lab]
            GOLD_TOT[lab] += g; CL_TOT[lab] += c
            if g: GOLD_PAGES[lab].add(hp)
            if c: CL_PAGES[lab].add(cp)
            if c > g:
                EXTRA[lab] += c - g; EXTRA_P[lab].add(cp); EXTRA_M[lab].add(code)
                EXTRA_G[lab]["template=" + tf] += c - g; EXTRA_G[lab]["subject=" + subj] += c - g
            elif g > c:
                MISS[lab] += g - c; MISS_P[lab].add(hp); MISS_M[lab].add(code)
                MISS_G[lab]["template=" + tf] += g - c; MISS_G[lab]["subject=" + subj] += g - c
        per_page.append((code, os.path.basename(cp), len(a), len(b), inter))

out = []
def P(s=""): out.append(s); print(s)
P(f"pairs {npairs}; position-free ratio mean {100*sum(pf_ratios)/max(1,len(pf_ratios)):.3f} % (the gate's difflib ratio is at most this; the gap is the ORDER loss)")
P(f"total skeleton lines: gold {sum(GOLD_TOT.values())} / claude {sum(CL_TOT.values())}; EXTRA lines (claude over gold, per page) {sum(EXTRA.values())}; MISSING lines (gold over claude) {sum(MISS.values())}")
P()
def fmt_groups(gc, tot):
    return "; ".join(f"{k} {v} ({v/tot:.2f})" for k, v in gc.most_common(4))
P("==== EXTRA — labels Claude ships more of than the gold on the same page (sum of per-page excess) ====")
P(f"{'excess':>7} {'pages':>6} {'mods':>5} {'gold-tot':>8} {'cl-tot':>7}  label  |  where")
for lab, v in EXTRA.most_common(60):
    P(f"{v:7d} {len(EXTRA_P[lab]):6d} {len(EXTRA_M[lab]):5d} {GOLD_TOT[lab]:8d} {CL_TOT[lab]:7d}  {lab}  |  {fmt_groups(EXTRA_G[lab], v)}")
P()
P("==== MISSING — labels the gold has more of than Claude on the same page (sum of per-page deficit) ====")
P(f"{'deficit':>7} {'pages':>6} {'mods':>5} {'gold-tot':>8} {'cl-tot':>7}  label  |  where")
for lab, v in MISS.most_common(60):
    P(f"{v:7d} {len(MISS_P[lab]):6d} {len(MISS_M[lab]):5d} {GOLD_TOT[lab]:8d} {CL_TOT[lab]:7d}  {lab}  |  {fmt_groups(MISS_G[lab], v)}")
P()
P(f"run {time.time()-t0:.1f} s")
open(os.path.join(OUTPUTS, "_s27_r3_labelcensus.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
json.dump({"pairs": npairs, "pf_mean": sum(pf_ratios)/max(1,len(pf_ratios)),
           "extra": {k: [v, len(EXTRA_P[k]), len(EXTRA_M[k]), GOLD_TOT[k], CL_TOT[k], dict(EXTRA_G[k])] for k, v in EXTRA.most_common(400)},
           "missing": {k: [v, len(MISS_P[k]), len(MISS_M[k]), GOLD_TOT[k], CL_TOT[k], dict(MISS_G[k])] for k, v in MISS.most_common(400)},
           "per_page": per_page},
          open(os.path.join(OUTPUTS, "_s27_r3_labelcensus.json"), "w"), indent=0)
