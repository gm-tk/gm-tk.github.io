#!/usr/bin/env python3
"""WHOLLY-BOLD PARAGRAPHS: `<p><b>…</b></p>` (nothing outside the bold) — gold vs Claude counts per group; and what the gold
ships at the aligned position of Claude's (via the miner's page_lines diff: heading? plain p? nothing?). python3 _s26_r398_pbold.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
PB = re.compile(r"<p\b[^>]*>\s*<(b|strong)>(?:(?!</\1>).)*</\1>\s*(?:[.:!?])?\s*</p>", re.S)
G = defaultdict(Counter); C = defaultdict(Counter); CP = defaultdict(set); CM = defaultdict(set); GP = defaultdict(set); EX = []
H = defaultdict(Counter)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    keys = ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subj}")
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        cl = "".join(live_pieces(ch)); gl = "".join(live_pieces(gh))
        c = len(PB.findall(cl)); g = len(PB.findall(gl))
        # the gold's heading counts as a proxy for where bold-only lines went
        gh4 = len(re.findall(r"<h[45]\b", gl)); ch4 = len(re.findall(r"<h[45]\b", cl))
        for k in keys:
            C[k]["p>b"] += c; G[k]["p>b"] += g; C[k]["h4/h5"] += ch4; G[k]["h4/h5"] += gh4
        if c: CP[keys[2]].add(cp); CM[keys[2]].add(code); CP["ALL"].add(cp); CM["ALL"].add(code)
        if g: GP[keys[2]].add(hp); GP["ALL"].add(hp)
        if c and len(EX) < 4:
            m = PB.search(cl); EX.append(f"{os.path.basename(cp)[:-5]}: {re.sub(r'\s+',' ', m.group(0))[:110]}")
print("==== wholly-bold paragraphs <p><b>…</b></p> — gold vs Claude (with h4/h5 counts as the heading proxy) ====")
for k in sorted(G, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), -C[x]["p>b"])):
    if C[k]["p>b"] + G[k]["p>b"] < 15: continue
    print(f"   {k:46s} p>b gold {G[k]['p>b']:5d} (pages {len(GP.get(k, set())):3d})  claude {C[k]['p>b']:5d} (pages {len(CP.get(k, set())):3d} / mods {len(CM.get(k, set())):3d})   h4/h5 gold {G[k]['h4/h5']:5d}  claude {C[k]['h4/h5']:5d}")
print("   examples:"); [print("     ", e) for e in EX]
