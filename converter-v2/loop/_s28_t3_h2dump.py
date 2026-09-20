#!/usr/bin/env python3
"""session 28 task 3 — dump the h2 lists (ON vs gold) and each gold fundamentalsPanel's first heading for the named modules."""
import os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ON = os.path.join(HERE, "_s28_t3_on")
H = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.S)
def fold(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()
for code in sys.argv[1:]:
    onp = os.path.join(ON, code, f"{code}_0_0.html")
    gp = glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code, f"{code}_0_0.html"))[0]
    o = open(onp, encoding="utf-8", errors="replace").read(); g = open(gp, encoding="utf-8", errors="replace").read()
    print(f"== {code}")
    print("  ON   h2:", [fold(m.group(2)) for m in H.finditer(o) if m.group(1) == "2"])
    print("  gold h2:", [fold(m.group(2)) for m in H.finditer(g) if m.group(1) == "2"])
    for side, html in (("ON  ", o), ("gold", g)):
        outs = []
        for pm in re.finditer(r'<div class="(?:introduction )?fundamentalsPanel"[^>]*>', html):
            hm = H.search(html[pm.end():pm.end() + 6000])
            outs.append(f"h{hm.group(1)} {fold(hm.group(2))[:40]}" if hm else "(none)")
        print(f"  {side} panel-first-headings:", outs)
    print("  ON   phases nav:", re.findall(r'<div phase="\d+">\s*<p>(.*?)</p>', o)[:8])
    print("  gold phases nav:", re.findall(r'<div phase="\d+">\s*<p>(.*?)</p>', g)[:8])
