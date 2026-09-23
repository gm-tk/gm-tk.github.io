#!/usr/bin/env python3
"""Session 40 r449 — the TABLE-form multiChoiceQuiz bundles with an explicit ([correct]-style) or ANNOUNCED (r309 fence)
answer mark: their table layouts (rows x cols, where the mark sits), to see whether one layout reaches the 20-site floor."""
import io, os, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
CORR = re.compile(r"\[\s*(?:correct|answer|right|tick|true)\b[^\]]*\]|\((?:correct|answer)\)", re.I)
ANN = re.compile(r"correct\s+answers?[^\n]{0,40}?highlight|highlighted\s+answers?[^\n]{0,30}?correct|answers?\s+(?:are\s+|is\s+)?highlighted", re.I)
out = collections.Counter(); ex = collections.defaultdict(list)
for l in io.open(os.path.join(HERE, "_s40_r449_mcq.jsonl"), encoding="utf-8"):
    b = json.loads(l)
    if b["built"]: continue
    tabs = [m for m in b["members"] if m["type"] == "table"]
    if not tabs: continue
    blob = json.dumps(b, ensure_ascii=False)
    ann = bool(ANN.search(blob))
    for t in tabs:
        rows = t.get("rows") or []
        if not rows: continue
        ncol = max(len(r) for r in rows)
        cm = t.get("cellMarks") or []
        ycells = [(ri, ci) for ri, r in enumerate(cm) for ci, c in enumerate(r) for mk in c if mk.get("kind") == "hl" and mk.get("color") == "yellow"]
        brcells = [(ri, ci) for ri, r in enumerate(rows) for ci, c in enumerate(r) if CORR.search(c)]
        sig = "bracket" if brcells else ("yellow-announced" if ycells and ann else ("yellow-unannounced" if ycells else None))
        if not sig: continue
        mcols = sorted({c for _, c in (brcells or ycells)})
        k = (sig, f"{len(rows)}r x {ncol}c" if len(rows) <= 3 else f"many-rows x {ncol}c", f"mark in col {mcols}")
        out[k] += 1; ex[k].append(f"{b['code']}#{b['idx']}")
for k, n in out.most_common(30): print(f"{n:3d}  {k}  e.g. {', '.join(ex[k][:4])}")
print("total marked table bundles by signal:", collections.Counter(k[0] for k in out.elements()))
