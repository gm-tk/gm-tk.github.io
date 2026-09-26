#!/usr/bin/env python3
"""_s52_r9_videourl.py — session 52 Round 9: every bare VIDEO-URL paragraph in Claude's body outside the hand-off boxes (YouTube /
Vimeo / an .mp4) — does the GOLD embed that video (its id in an <iframe src> / <video> / <source>) on the paired page, elsewhere
in the module, or not at all; and does Claude already embed it on the page (a duplicate line)? Per family. WSL, from
reference/tests/:  python3 ../../outputs/_s52_r9_videourl.py"""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import compare_structure as CS
import _corpus
P = re.compile(r"<p\b[^>]*>\s*(?:<a\b[^>]*>)?\s*(https?://[^\s<\"]+)\s*(?:</a>)?\s*</p>", re.I)
def vid(u):
    m = re.search(r"(?:youtu\.be/|youtube(?:-nocookie)?\.com/(?:watch\?v=|embed/|shorts/|live/))([\w-]{11})", u)
    if m: return m.group(1)
    m = re.search(r"vimeo\.com/(?:video/)?(\d{6,})", u)
    if m: return m.group(1)
    m = re.search(r"/([^/]+\.mp4)", u, re.I)
    return m.group(1) if m else None
def spans_of(s):
    out = []
    for h in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
        d = 0
        for x in re.finditer(r"<(/?)div\b[^>]*>", s[h.start():]):
            d += -1 if x.group(1) else 1
            if d == 0: out.append((h.start(), h.start() + x.end())); break
    return out
st = collections.Counter(); fam = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); mods = collections.defaultdict(set)
for mod in sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m))):
    try: gall = "".join(open(f, encoding="utf-8", errors="replace").read() for f in glob.glob(os.path.join(_corpus.mdir(CS.HUMAN, mod), "*.html")))
    except Exception: gall = ""
    gmedia_all = " ".join(re.findall(r"<(?:iframe|video|source)\b[^>]*>", gall))
    for n, cp, hp in pairs(mod):
        s = open(cp, encoding="utf-8", errors="replace").read(); b = s.find('id="body"'); sp = spans_of(s)
        g = open(hp, encoding="utf-8", errors="replace").read()
        gmedia = " ".join(re.findall(r"<(?:iframe|video|source)\b[^>]*>", g))
        cmedia = " ".join(re.findall(r"<(?:iframe|video|source)\b[^>]*>", s))
        for m in P.finditer(s, max(b, 0)):
            if any(a <= m.start() < z for a, z in sp): continue
            v = vid(m.group(1)); short = "shorts/" in m.group(1)
            if not v: continue
            k = ("SHORT " if short else "") + ("gold EMBEDS it on the page" if v in gmedia else "gold embeds it elsewhere" if v in gmedia_all else
                 "gold: link/text only" if v in gall else "gold: absent") + (" | claude embeds it too" if v in cmedia else "")
            st[k] += 1; fam[k][re.sub(r"\d.*$", "", mod)] += 1; pages[k].add(cp); mods[k].add(mod)
for k, n in st.most_common():
    print(f"{n:4d} paras / {len(pages[k]):3d} pages / {len(mods[k]):3d} mods  {k}   top: {', '.join(f'{a} {b}' for a, b in fam[k].most_common(8))}")
