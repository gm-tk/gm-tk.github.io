#!/usr/bin/env python3
"""_s51_r5_alertlist.py — session 51 Round 5 PICK: Claude alert boxes (div.alert*, not alertActivity) whose ONLY content is one
short line (<= 12 words) and that are followed — right after the box closes, same column — by a free <ul>/<ol>. For each, where
the GOLD puts that list's first item (the §1g census parser, text matched on the paired page): inside an alert or not.
WSL, from reference/tests/."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE

BOX = re.compile(r'<div class="(alert(?:\s[^"]*)?)">\s*<div class="row">\s*<div class="col-12">\s*(<(p|h[1-6])\b[^>]*>(.*?)</\3>)\s*</div>\s*</div>\s*</div>\s*(<(ul|ol)\b[^>]*>\s*<li\b[^>]*>(.*?)</li>)', re.S)
strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", t.lower()).split())
res = collections.Counter(); fam = collections.defaultdict(collections.Counter); ex = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    for n, cp, hp in pairs(code):
        html = open(cp, encoding="utf-8", errors="replace").read()
        hits = [m for m in BOX.finditer(html) if len(strip(m.group(4)).split()) <= 12]
        if not hits: continue
        g = PC.parse(hp)
        for m in hits:
            li = fold(strip(m.group(7)))
            best = max(g, key=lambda b: PC.jacc(b[1], li), default=None)
            where = best[3] if best and PC.jacc(best[1], li) >= 0.6 else "—"
            k = "alert" if "alert" in where else where
            res[k] += 1; fam[re.sub(r"\d.*$", "", code)][k] += 1
            if len(ex) < 12: ex.append(f"{os.path.basename(cp)} [{m.group(1)}] '{strip(m.group(4))[:40]}' + {m.group(6)} '{strip(m.group(7))[:40]}' -> gold {where}")
print("title-only alerts followed by a free list:", sum(res.values()), dict(res.most_common(6)))
for f, c in sorted(fam.items(), key=lambda kv: -sum(kv[1].values()))[:15]: print(f"  {f:8s} {dict(c.most_common(4))}")
print("\n".join(ex))
