#!/usr/bin/env python3
"""Session 45 Round 11 — Writers-Template TABLES whose text opens (within the first cell's first 120 characters, markers stripped) with a
learning-intentions lead ('Learning Intentions' / 'We are learning' / 'Whāinga Ako'): per module, the table shape (rows × cols), the tag
line before it, and where the gold puts the WALT sentence (menu / body / absent) and where Claude does. WSL, from outputs/."""
import os, re, io, sys, glob, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s45_r7_emptymenu.py"), encoding="utf-8").read().split("pp = json.load")[0])
RED = re.compile(r"🔴\[RED TEXT\]|\[/RED TEXT\]🔴")
LEAD = re.compile(r"(learning intentions?|we are learning|wh[aā]inga ako)", re.I)
agg = collections.Counter(); ex = collections.defaultdict(list)
for code in _corpus.gate_mods(GOLD):
    gd = _corpus.mdir(GOLD, code); cd = _corpus.mdir(CL, code)
    wts = [p for p in glob.glob(os.path.join(gd, "*_parsed.txt")) if "writers template" in p.lower()]
    if not wts or not os.path.isdir(cd): continue
    lines = []
    for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
    gp = [split_regions(p) for p in glob.glob(os.path.join(gd, "*.html"))]
    cp = [split_regions(p) for p in glob.glob(os.path.join(cd, "*.html"))]
    i = 0
    while i < len(lines):
        if lines[i].startswith("┌─── TABLE"):
            j = i + 1; rows = []
            while j < len(lines) and not lines[j].startswith("└─── END TABLE"): rows.append(lines[j]); j += 1
            first = RED.sub(" ", rows[0] if rows else "")
            first = re.sub(r"\[[^\]]*\]", " ", first).replace("*", "").lstrip("│ ").strip()
            if LEAD.search(first[:120]):
                cols = max((r.count("║") + 1 for r in rows), default=1)
                prev = next((RED.sub(" ", lines[k]).strip() for k in range(i - 1, max(0, i - 6), -1) if lines[k].strip()), "")
                txt = n(RED.sub(" ", " ".join(rows)))
                m = re.search(r"we are learning\s+(\S+(?:\s+\S+){5})", txt)
                key = m.group(0) if m else " ".join(txt.split()[2:8])
                gw = "menu" if any(key in a for a, _ in gp) else ("body" if any(key in b for _, b in gp) else "absent")
                cw = "menu" if any(key in a for a, _ in cp) else ("body" if any(key in b for _, b in cp) else "absent")
                k = (f"{len(rows)}x{cols}", gw, cw)
                agg[k] += 1
                if len(ex[k]) < 5: ex[k].append(f"{code} «{prev[:40]}»")
            i = j
        i += 1
for k, v in agg.most_common(): print(f"{v:4d} {k}  {' | '.join(ex[k])}")
tot = collections.Counter()
for (s, g, c), v in agg.items(): tot[(g, c)] += v
print("\n(gold, claude):", dict(tot))
