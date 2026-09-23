#!/usr/bin/env python3
"""Round 447 — classify each pre-score mover by the GOLD page's own journal form: h4.goJournal / a green
'…journal' button / neither. The D13-5 named override is the green-button (and no-journal) golds; a DOWN on an
h4 gold would be a defect. Reads _r447_prescore.log. Run from CONVERTER_V2/reference/tests under WSL."""
import os, re, io, glob
O = os.path.join("..", "..", "outputs")
ROOT = os.path.normpath(os.path.join("..", "..", ".."))
H4 = re.compile(r'<h4 class="goJournal">', re.I)
BTN = re.compile(r'<div class="button">[^<]*journal[^<]*</div>', re.I)
rows = []
for ln in io.open(os.path.join(O, "_r447_prescore.log"), encoding="utf-8"):
    m = re.match(r"(\S+)\s+(\S+)\s+<->\s+(.+?)\s+([\d.]+) ->\s+([\d.]+)\s+\(([-+][\d.]+)\)", ln)
    if not m: continue
    code, cf, hf, a, b, d = m.groups()
    g = glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code, hf))
    s = io.open(g[0], encoding="utf-8", errors="replace").read() if g else ""
    form = "h4" if H4.search(s) else ("button" if BTN.search(s) else "neither")
    rows.append((float(d), code, cf, form))
import collections
agg = collections.defaultdict(lambda: [0, 0, 0.0])
for d, code, cf, form in rows:
    k = form; agg[k][0 if d > 0 else 1] += 1; agg[k][2] += d
for k, (u, dn, pp) in sorted(agg.items()):
    print(f"gold form {k:8s}: {u:3d} up / {dn:3d} down, pp-sum {pp:+.1f}")
print("DOWN movers on an h4 gold:")
for d, code, cf, form in sorted(rows):
    if form == "h4" and d < 0: print(f"  {code} {cf} {d:+.1f}")
