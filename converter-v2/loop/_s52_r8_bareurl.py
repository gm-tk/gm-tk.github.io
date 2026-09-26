#!/usr/bin/env python3
"""_s52_r8_bareurl.py — session 52 Round 8: THE BARE-URL PARAGRAPH. A body <p> whose whole visible text is one URL (a linked or
plain `https://…`), by host class (istock / image host, video: youtube / vimeo / .mp4, d2l / tekura, other) and by container
(in an activity box or free) — gold vs Claude, pages and modules, per family (top). Regex-level. WSL."""
import re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
P = re.compile(r"<p\b[^>]*>\s*(?:<a\b[^>]*>)?\s*(https?://[^\s<]+)\s*(?:</a>)?\s*</p>", re.I)
def host(u):
    u = u.lower()
    if "istockphoto" in u or "shutterstock" in u or "gettyimages" in u or "unsplash" in u or "pexels" in u or "freepik" in u or "adobe.stock" in u or "stock.adobe" in u: return "stock-image"
    if "youtu" in u or "vimeo" in u or u.endswith(".mp4") or "/video" in u: return "video"
    if "desire2learn" in u or "tekura" in u or "d2l" in u: return "d2l/tekura"
    if re.search(r"\.(png|jpe?g|gif|svg|webp)(\?|$)", u): return "image-file"
    return "other"
def census(root):
    st = collections.Counter(); pages = collections.defaultdict(set); mods = collections.defaultdict(set); fam = collections.defaultdict(collections.Counter)
    for f in glob.glob(root + "/*/*/*.html"):
        mod = f.split("/")[-2]; fm = re.sub(r"\d.*$", "", mod)
        s = open(f, encoding="utf-8", errors="replace").read(); b = s.find('id="body"')
        if b < 0: continue
        spans = []
        for h in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
            d = 0
            for x in re.finditer(r"<(/?)div\b[^>]*>", s[h.start():]):
                d += -1 if x.group(1) else 1
                if d == 0: spans.append((h.start(), h.start() + x.end())); break
        for m in P.finditer(s, b):
            if any(a <= m.start() < z for a, z in spans): continue   # inside an un-built hand-off box
            pre = s[max(b, m.start() - 3000):m.start()]
            inact = pre.rfind('class="activity') > pre.rfind('<div class="row">\n<div class="col-md-8') if 'class="activity' in pre else False
            k = host(m.group(1)) + (" in-activity" if inact else "")
            st[k] += 1; pages[k].add(f); mods[k].add(mod); fam[k][fm] += 1
    return st, pages, mods, fam
g = census(R + "/01-Finalized_Modules_"); c = census(R + "/01-Claude_Modules_")
for side, (st, pages, mods, fam) in (("GOLD", g), ("CLAUDE", c)):
    print(side)
    for k, n in st.most_common():
        print(f"  {k:26s} {n:5d} paras / {len(pages[k]):4d} pages / {len(mods[k]):3d} mods  top: {', '.join(f'{a} {b}' for a, b in fam[k].most_common(6))}")
