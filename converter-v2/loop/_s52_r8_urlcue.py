#!/usr/bin/env python3
"""_s52_r8_urlcue.py — session 52 Round 8: every bare-URL paragraph in Claude's free body / activity boxes (outside the un-built
hand-off boxes), classified by its WT item context (outputs/_s52_items/<CODE>.tsv): the item whose text holds the URL, and the
nearest non-empty item before it. Grouped by host class and cue. WSL."""
import os, re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"; O = os.path.dirname(os.path.abspath(__file__))
P = re.compile(r"<p\b[^>]*>\s*(?:<a\b[^>]*>)?\s*(https?://[^\s<\"]+)\s*(?:</a>)?\s*</p>", re.I)
def host(u):
    u = u.lower()
    if re.search(r"istockphoto|shutterstock|gettyimages|unsplash|pexels|freepik|stock\.adobe", u): return "stock"
    if re.search(r"youtu|vimeo|\.mp4", u): return "video"
    if re.search(r"desire2learn|tekura|d2l", u): return "d2l"
    return "other"
items = {}
def load(mod):
    if mod in items: return items[mod]
    p = os.path.join(O, "_s52_items", mod + ".tsv"); rows = []
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            f = line.rstrip("\n").split("\t")
            if len(f) >= 9: rows.append(f)
    items[mod] = rows; return rows
st = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list); pg = collections.defaultdict(set)
for f in glob.glob(R + "/01-Claude_Modules_/*/*/*.html"):
    mod = f.split("/")[-2]
    s = open(f, encoding="utf-8", errors="replace").read(); b = s.find('id="body"')
    if b < 0: continue
    spans = []
    for hh in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
        d = 0
        for x in re.finditer(r"<(/?)div\b[^>]*>", s[hh.start():]):
            d += -1 if x.group(1) else 1
            if d == 0: spans.append((hh.start(), hh.start() + x.end())); break
    for m in P.finditer(s, b):
        if any(a <= m.start() < z for a, z in spans): continue
        url = m.group(1).replace("&amp;", "&"); h = host(url)
        rows = load(mod); key = url[:60]
        k = next((i for i, r in enumerate(rows) if key in (r[6] + r[7] + r[8]).replace("&amp;", "&")), None)
        if k is None: cue = "not-in-items"
        else:
            r = rows[k]
            own = "own:tag:" + r[3] if r[2] == "tag" else ("own:black-url-only" if re.fullmatch(r"\s*https?://\S+\s*", r[8]) else "own:black+text")
            j = k - 1
            while j >= 0 and rows[j][2] == "black" and (not rows[j][8].strip() or re.fullmatch(r"\s*https?://\S+\s*", rows[j][8])): j -= 1
            pv = rows[j] if j >= 0 else None
            prev = "PAGESTART" if pv is None else (f"prev:tag:{pv[3] or pv[6][:18]}" if pv[2] == "tag" else ("prev:table" if pv[2] == "table" else "prev:black"))
            cue = own + " | " + prev
        st[h][cue] += 1; pg[h + cue].add(f)
        if len(ex[h + cue]) < 2: ex[h + cue].append(f"{os.path.basename(f)} {url[:70]}")
for h in st:
    print(f"== {h}: {sum(st[h].values())}")
    for cue, n in st[h].most_common(9):
        print(f"   {n:4d} ({len(pg[h + cue]):3d} pages)  {cue}   e.g. {ex[h + cue][0] if ex[h + cue] else ''}")
