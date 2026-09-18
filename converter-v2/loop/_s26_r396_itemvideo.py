#!/usr/bin/env python3
"""CAROUSEL VIDEO ITEMS: for every carousel, each item that CONTAINS a videoSection — its class (`item` vs `item video`), the
carousel's kind (all-video / mixed), gold vs Claude, per template / subject. python3 _s26_r396_itemvideo.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r396_widgetwrap.py"), encoding="utf-8").read()
exec(src[:src.index("ROOTS = ")])
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def carousels(s):
    """yield per carousel: list of (item class, has_video)."""
    st = []; out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing: continue
        if closing:
            if st:
                e = st.pop()
                if e[1] == "carousel" and e[2] is not None: out.append(e[2])
                if e[1] == "item" and st:
                    car = next((x for x in reversed(st) if x[1] == "carousel"), None)
                    if car is not None and car[2] is not None: car[2].append((e[0], e[3]))
            continue
        c = CLS.search(attrs); toks = (c.group(1) if c else "").split(); cls = " ".join(sorted(toks))
        kind = "carousel" if ("carousel" in toks and "row" in toks) else ("item" if "item" in toks and not any(t.startswith("carousel-") for t in toks) else None)
        if "videoSection" in toks:
            for x in reversed(st):
                if x[1] == "item": x[3] = True; break
        st.append([cls, kind, [] if kind == "carousel" else None, False])
    return out
from collections import Counter, defaultdict
G = defaultdict(Counter); C = defaultdict(Counter); GP = defaultdict(lambda: defaultdict(set)); CP = defaultdict(lambda: defaultdict(set)); CM = defaultdict(lambda: defaultdict(set))
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for side, s, D, DP in (("gold", gh, G, GP), ("claude", ch, C, CP)):
            for items in carousels(s):
                vids = [it for it in items if it[1]]
                if not vids: continue
                kind = "ALL-VIDEO" if len(vids) == len(items) else "MIXED"
                for cls, _ in vids:
                    lab = "item video" if "video" in cls.split() else ("item" if cls == "item" else cls)
                    for k in ("ALL", f"kind={kind}", f"kind={kind} · tmpl+subj={tf}/{subj}"):
                        D[k][lab] += 1; DP[k][lab].add(hp if side == "gold" else cp)
                        if side == "claude": CM[k][lab].add(code)
print("==== carousel items that contain a video: class `item video` vs `item` ====")
for k in sorted(set(G) | set(C), key=lambda x: (not x.startswith("ALL"), x.count("·"), -sum(G[x].values()) - sum(C[x].values()))):
    tg = sum(G[k].values()); tc = sum(C[k].values())
    if k.count("·") and tg + tc < 12: continue
    gv = G[k]["item video"]; cv = C[k]["item video"]
    print(f"   {k:62s} gold {tg:4d} (video {gv:4d} = {gv/tg if tg else 0:.2f}; pages {len(GP[k]['item video']):3d}/{len(set().union(*GP[k].values())) if GP[k] else 0:3d})   claude {tc:4d} (video {cv:4d} = {cv/tc if tc else 0:.2f}; pages {len(set().union(*CP[k].values())) if CP[k] else 0:3d} / mods {len(set().union(*CM[k].values())) if CM[k] else 0:3d})")
