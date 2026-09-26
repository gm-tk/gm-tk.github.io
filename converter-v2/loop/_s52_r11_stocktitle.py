#!/usr/bin/env python3
"""_s52_r11_stocktitle.py — session 52 Round 11: body paragraphs (outside the hand-off boxes) that are a stock-photo TITLE / credit
line ('… Stock Photo - Download Image Now - iStock', '… Stock Illustration …', 'Photo: … iStock …', 'Getty Images'), gold vs Claude,
by form. Regex-level. WSL."""
import re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
P = re.compile(r"<p\b([^>]*)>(.*?)</p>", re.S)
FORMS = [("download-image-now", re.compile(r"download image now", re.I)),
         ("stock photo/illustration/vector title", re.compile(r"\bstock (?:photo|illustration|vector|image)s?\b", re.I)),
         ("iStock / Getty credit", re.compile(r"\bistock\b|getty images", re.I))]
def spans_of(s):
    out = []
    for h in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
        d = 0
        for x in re.finditer(r"<(/?)div\b[^>]*>", s[h.start():]):
            d += -1 if x.group(1) else 1
            if d == 0: out.append((h.start(), h.start() + x.end())); break
    return out
def census(root):
    st = collections.Counter(); pages = collections.defaultdict(set); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
    for f in glob.glob(root + "/*/*/*.html"):
        mod = f.split("/")[-2]
        s = open(f, encoding="utf-8", errors="replace").read(); b = s.find('id="body"'); e = s.find('class="acks'); sp = spans_of(s)
        if b < 0: continue
        for m in P.finditer(s, b):
            if e > 0 and m.start() > e: break
            if "cv2-note" in m.group(1) or any(a <= m.start() < z for a, z in sp): continue
            t = re.sub(r"<[^>]+>", " ", m.group(2)); t = re.sub(r"\s+", " ", t).strip()
            if not t or len(t) > 220: continue
            k = next((n for n, rx in FORMS if rx.search(t)), None)
            if not k: continue
            st[k] += 1; pages[k].add(f); mods[k].add(mod)
            if len(ex[k]) < 3: ex[k].append(f"{mod}: {t[:90]}")
    return st, pages, mods, ex
for side, root in (("GOLD", R + "/01-Finalized_Modules_"), ("CLAUDE", R + "/01-Claude_Modules_")):
    st, pages, mods, ex = census(root)
    print(side)
    for k, n in st.most_common():
        print(f"  {n:4d} paras / {len(pages[k]):3d} pages / {len(mods[k]):3d} mods  {k}")
        for x in ex[k]: print("      e.g.", x)
