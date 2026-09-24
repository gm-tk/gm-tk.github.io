#!/usr/bin/env python3
"""Session 41 Round 10 — the OUT-H split: for each gold box title (first-element h3) that sits on the Claude page as a heading OUTSIDE
every Claude box, what follows it on the Claude page: (a) a Claude activity box opens within the next 400 chars (the box starts one
element late — the title is just before it), (b) a box opens later on the page, (c) no box follows. Per family + examples.
Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, collections, html as H
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _corpus
from anchor_compare import CLAUDE
exec(open(os.path.join("..", "..", "outputs", "_s41_r10_boxtitle2.py")).read().split("cases = collections.Counter()")[0].split("from anchor_compare import CLAUDE")[1])
res = collections.Counter(); fam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    f = re.match(r"[A-Z]+", code).group(0)
    for _, cp, hp in DA.pairs(code):
        g = open(hp, encoding="utf-8", errors="replace").read(); c = open(cp, encoding="utf-8", errors="replace").read()
        cb = spans(c); cfirst = [first_el(c, a) for _, _, a in cb]
        for gs, ge, ga in spans(g):
            tag, t, _ = first_el(g, ga)
            if tag != "h3" or len(t) < 4: continue
            key = t[:30]
            has = lambda x: x and (x == t or x.startswith(key) or t.startswith(x[:30]))
            if any(ft == "h3" and has(fx) for ft, fx, _ in cfirst): continue
            for m in EL.finditer(c):
                if not m.group(1).startswith("h") or not has(norm(m.group(2))): continue
                pos = m.start()
                if any(a <= pos < b for a, b, _ in cb): break
                nxt = [a for a, _, _ in cb if a > pos]
                gap = c[m.end():nxt[0]] if nxt else ""
                between = len(EL.findall(gap)) if nxt else -1
                k = ("(a) box opens right after (0 elements between)" if nxt and between == 0 else
                     ("(a2) box opens after 1-2 elements" if nxt and between <= 2 else ("(b) a box later" if nxt else "(c) no box after")))
                res[k] += 1; fam[f][k] += 1
                if len(ex[k]) < 30: ex[k].append(f"{code} {os.path.basename(cp)} {m.group(1)}: {t[:60]}")
                break
for k, n in res.most_common(): print(f"{n:5d} {k}")
for f, c in sorted(fam.items(), key=lambda x: -sum(x[1].values()))[:25]: print(f"{f:7s}", dict(c))
for k in res: print(f"\n== {k}"); [print("  ", e) for e in ex[k][:15]]
