#!/usr/bin/env python3
"""Session 22 — Claude's two_rows boxes OUTSIDE the ENFUN registry family: where do they come from, and what is the
gold's anatomy for the same-numbered box on the paired page? Reads _activity_anatomy_{claude,gold}.jsonl (r229 core)."""
import os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
def load(side):
    return [json.loads(l) for l in open(os.path.join(HERE, "_activity_anatomy_%s.jsonl" % side), encoding="utf-8")]
C = load("claude"); G = load("gold")
def pkey(p):
    import re
    m = re.search(r"[._-](\d{1,2})(?:[._](\d))?\.html$", p or "")
    return (int(m.group(1)), int(m.group(2) or 0)) if m else p
gidx = collections.defaultdict(list)
for r in G:
    gidx[(r["mod"], pkey(r.get("page")), r.get("number"))].append(r)
two = [r for r in C if r.get("anatomy") == "two_rows" and not str(r["mod"]).startswith("ENFUN")]
print("Claude two_rows outside ENFUN:", len(two), "boxes on", len({(r["mod"], r.get("page")) for r in two}), "pages /", len({r["mod"] for r in two}), "modules")
by = collections.Counter(("".join(ch for ch in r["mod"] if ch.isalpha()), r.get("tpl")) for r in two)
print("by prefix|template:", by.most_common(14))
print("widget col:", collections.Counter(r.get("widget_col") for r in two).most_common(6))
print("prose col:", collections.Counter(r.get("prose_col") for r in two).most_common(6))
print("box classes:", collections.Counter(r.get("box_classes") for r in two).most_common(6))
print("first widget type:", collections.Counter((r.get("types") or ["?"])[0] for r in two).most_common(8))
gold_forms = collections.Counter(); gold_wcol = collections.Counter(); ex = []
for r in two:
    gs = gidx.get((r["mod"], pkey(r.get("page")), r.get("number")), [])
    g = gs[0] if gs else None
    gold_forms[g.get("anatomy") if g else "no-same-number-gold-box"] += 1
    if g: gold_wcol[g.get("widget_col")] += 1
    if len(ex) < 14: ex.append((r["mod"], r.get("page"), r.get("number"), r.get("types"), r.get("widget_col"), (g or {}).get("anatomy"), (g or {}).get("widget_col")))
print("gold anatomy of the same-numbered box:", gold_forms.most_common())
print("gold widget col where two_rows:", gold_wcol.most_common(5))
for e in ex: print("  ", e)
