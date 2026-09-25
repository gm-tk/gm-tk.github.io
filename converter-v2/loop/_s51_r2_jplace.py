#!/usr/bin/env python3
"""_s51_r2_jplace.py — session 51 Round 2 PICK: every text block on a paired page (gold and Claude) that is a JOURNAL
instruction naming an activity id ("…complete activity 4A … journal"), with its container path (the §1g census parser).
Reports, per family, where the gold puts it (activity box / free / alert …) against Claude. WSL, from reference/tests/."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE

J = re.compile(r"(journal.*activit(?:y|ies)\s*\d|activit(?:y|ies)\s*\d.*journal)", re.I)
cnt = collections.Counter(); fam = collections.defaultdict(collections.Counter); ex = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    for n, cp, hp in pairs(code):
        g = [b for b in PC.parse(hp) if J.search(b[2])]
        c = [b for b in PC.parse(cp) if J.search(b[2])]
        if not g and not c: continue
        reg = lambda b: b[3]
        gr = sorted(set(reg(b) for b in g)); cr = sorted(set(reg(b) for b in c))
        k = f"gold {'+'.join(gr) or '—'}  |  claude {'+'.join(cr) or '—'}"
        cnt[k] += 1; fam[re.sub(r"\d.*$", "", code)][k] += 1
        ex.append(f"{code} {os.path.basename(cp)}: {k}")
for k, v in cnt.most_common(30): print(v, k)
print("--- by family (AGH):")
for k, v in fam["AGH"].most_common(): print(" ", v, k)
print("\n".join(x for x in ex if "claude —" in x and not x.startswith("AGH")))
