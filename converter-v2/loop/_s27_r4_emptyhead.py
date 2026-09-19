#!/usr/bin/env python3
"""Session 27 Round 4 — THE EMPTY [H2]/[H3] FLAG (56 flags): on Claude's page, what element FOLLOWS the flag
(a short <p> = the heading text the writer typed on the next line?), and does the gold ship that text as a
heading (which level)?  wsl: python3 _s27_r4_emptyhead.py -> _s27_r4_emptyhead.out"""
import os, re, sys
from collections import Counter, defaultdict
OUT = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
CLAUDE = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Claude_Modules_'
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
def fold(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip().lower()
def fold2(t): return re.sub(r"[^\w ]+", " ", fold(t)).strip()
gold_dirs = {}
for tf in os.listdir(HUMAN):
    d = os.path.join(HUMAN, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): gold_dirs[m] = os.path.join(d, m)
FLAG = re.compile(r'<p class="cv2-note"[^>]*>Red Flag: Empty \[(H[2-5])\][^<]*</p>\s*(<(\w+)[^>]*>(.*?)</\3>)?', re.S)
C = Counter(); NEXT = Counter(); G = Counter(); EX = defaultdict(list); pages = set(); mods = set(); BYG = defaultdict(Counter)
for tf in os.listdir(CLAUDE):
    td = os.path.join(CLAUDE, tf)
    if not os.path.isdir(td): continue
    for code in sorted(os.listdir(td)):
        cd = os.path.join(td, code)
        if not os.path.isdir(cd): continue
        gd = gold_dirs.get(code); gh = None
        for f in sorted(os.listdir(cd)):
            if not f.endswith(".html"): continue
            html = open(os.path.join(cd, f), encoding="utf-8", errors="replace").read()
            for m in FLAG.finditer(html):
                tag = m.group(1); nxt = m.group(3) or "END"; txt = fold(m.group(4) or "")
                words = len(txt.split())
                kind = f"{nxt}:{'short' if 0 < words <= 12 else ('long' if words else 'empty')}"
                C[tag] += 1; NEXT[kind] += 1; pages.add(code + "/" + f); mods.add(code)
                gv = "n/a"
                if nxt == "p" and 0 < words <= 12 and gd:
                    if gh is None:
                        gh = [open(os.path.join(gd, x), encoding="utf-8", errors="replace").read() for x in os.listdir(gd) if x.endswith(".html")]
                    key = fold2(txt)
                    gv = "gold:absent"
                    for h in gh:
                        for hm in re.finditer(r"<(h[1-6]|p|li|b|strong)[^>]*>(.*?)</\1>", h, re.S):
                            if fold2(hm.group(2)) == key: gv = "gold:" + hm.group(1); break
                        if gv != "gold:absent": break
                    G[gv] += 1; BYG[tf][gv] += 1
                if len(EX[(tag, kind, gv)]) < 3: EX[(tag, kind, gv)].append(f"{code}/{f} «{txt[:50]}»")
out = []
def P(s=""): out.append(s); print(s)
P(f"Empty [Hn] flags: {sum(C.values())} on {len(pages)} pages / {len(mods)} modules  by tag {dict(C)}")
P("next element after the flag: " + "; ".join(f"{k} {v}" for k, v in NEXT.most_common()))
P("gold element for the short <p> text that follows: " + "; ".join(f"{k} {v}" for k, v in G.most_common()))
for tf, c in BYG.items(): P(f"   {tf}: " + "  ".join(f"{k} {v}" for k, v in c.most_common()))
P()
for key, ex in EX.items():
    for e in ex: P(f"   {key}: {e}")
open(os.path.join(OUT, "_s27_r4_emptyhead.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
