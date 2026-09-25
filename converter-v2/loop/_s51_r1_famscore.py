#!/usr/bin/env python3
"""_s51_r1_famscore.py — session 51 Round 1 PICK (the per-family lane): mean skeleton SCAFFOLD per module family (code prefix)
and per template, from the newest full skeleton state; the families with the largest total gap (pages x (100 - mean)).
WSL, from reference/tests/. argv[1] = the sk_final json."""
import json, sys, re, collections
d = json.load(open(sys.argv[1]))
pages = d["per_page"]
if isinstance(pages, dict): pages = [dict(v, page=k) for k, v in pages.items()]
print("keys:", list(pages[0].keys())[:12]) if pages else None
fam = collections.defaultdict(list)
for p in pages:
    name = p.get("page") or p.get("gold") or p.get("claude") or ""
    code = p.get("module") or re.split(r"[/_]", name)[0]
    s = p.get("scaffold_pct", p.get("scaffold", p.get("score")))
    if s is None: continue
    fam[re.sub(r"\d.*$", "", code)].append(float(s) * (100 if float(s) <= 1.0 else 1))
rows = sorted(((f, len(v), sum(v) / len(v), sum(100 - x for x in v)) for f, v in fam.items()), key=lambda r: -r[3])
tot = sum(r[3] for r in rows)
print(f"families {len(rows)}  pages {sum(r[1] for r in rows)}  total gap {tot:.0f}")
for f, n, m, g in rows[:40]: print(f"{f:10s} pages {n:4d}  mean {m:5.1f}  gap {g:7.0f}  ({g / tot * 100:4.1f} %)")
