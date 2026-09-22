#!/usr/bin/env python3
"""Session 34 Round 3 PICK measurement — THE IMAGE ROW: a gold `div.row` whose direct children are >= 2 columns each holding ONLY an
<img> (+ an optional caption <p>) — the human's side-by-side image layout. How many gold pages / rows carry it, what column widths
(by count), and on the paired Claude page: are the same images (by src stem / alt) emitted CONSECUTIVELY in one column (the derivable
"N consecutive [Image] tags → an image row" class) or scattered / inside widgets? Also the WT: are the images consecutive [Image] lines?
Run under WSL: python3 _s34_r3_imgrow.py
"""
import os, re, glob, json, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
import sys
sys.path.insert(0, R + "CONVERTER_V2/reference/tests")
import _corpus
from _discrepancy_audit import pairs as _pairs
pairs = []
for code in _corpus.gate_mods(R + "01-Claude_Modules_"):
    try:
        for n, cp, hp in _pairs(code):
            if re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I): continue
            pairs.append((code, hp, cp))
    except Exception:
        continue
def gpath(code, name): return name
def cpath(code, name): return name
def stem(src):
    s = os.path.basename(src)
    if "?text=" in s: s = s.split("?text=")[-1]
    return re.sub(r'\.(jpg|png|jpeg|gif|webp|svg)$', '', s, flags=re.I).lower()
# a crude block parser: find <div class="row ..."> ... matching </div> by depth
def rows_of(html):
    out = []
    for m in re.finditer(r'<div class="row[^"]*"[^>]*>', html):
        i = m.end(); depth = 1; j = i
        while depth and j < len(html):
            nxt_open = html.find("<div", j); nxt_close = html.find("</div>", j)
            if nxt_close < 0: break
            if nxt_open >= 0 and nxt_open < nxt_close: depth += 1; j = nxt_open + 4
            else: depth -= 1; j = nxt_close + 6
        out.append(html[m.start():j])
    return out
def cols_of(row_html):
    inner = row_html[row_html.find(">") + 1:]
    cols = []
    for m in re.finditer(r'<div class="(col[^"]*)"[^>]*>', inner):
        i = m.end(); depth = 1; j = i
        while depth and j < len(inner):
            no = inner.find("<div", j); nc = inner.find("</div>", j)
            if nc < 0: break
            if no >= 0 and no < nc: depth += 1; j = no + 4
            else: depth -= 1; j = nc + 6
        cols.append((m.group(1), inner[m.end():j]))
    return cols
def img_only(col_html):
    t = re.sub(r'<img[^>]*>', '', col_html)
    t = re.sub(r'<p class="captionText">.*?</p>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t).strip()
    return bool(re.search(r'<img', col_html)) and not t
tot_rows = 0; pages = set(); widths = collections.Counter(); ncols = collections.Counter()
consec = scattered = widget = missing = 0
wt_consec = wt_not = 0
examples = []
for code, g, c in pairs:
    gp, cp = gpath(code, g), cpath(code, c)
    if not gp or not cp: continue
    gh = open(gp, encoding="utf-8", errors="replace").read(); ch = open(cp, encoding="utf-8", errors="replace").read()
    for row in rows_of(gh):
        cols = cols_of(row)
        if len(cols) < 2 or not all(img_only(h) for _, h in cols): continue
        # top-level image row only (not inside a widget shell)
        tot_rows += 1; pages.add((code, g)); ncols[len(cols)] += 1
        widths[" | ".join(re.sub(r'\s+', ' ', w) for w, _ in cols)] += 1
        stems = [stem(s) for _, h in cols for s in re.findall(r'<img[^>]*src="([^"]+)"', h)]
        keys = [re.search(r'\d{6,}', s) for s in stems]
        keys = [k.group(0) if k else s for k, s in zip(keys, stems)]
        pos = [ch.find(k) for k in keys]
        found = [p for p in pos if p >= 0]
        if not keys or len(found) < len(keys): missing += 1; continue
        # consecutive in one column? the Claude text between the first and last image should hold only img / blank / caption
        a, b = min(found), max(found)
        between = ch[a:b]
        inner = re.sub(r'<img[^>]*>|<!--.*?-->|<p class="captionText">.*?</p>', '', between, flags=re.S)
        if "cv2-interactive" in between or "flipCard" in between or "carousel" in between: widget += 1
        elif not re.sub(r'<[^>]+>', '', inner).strip() and "<div class=\"row" not in inner: consec += 1
        else: scattered += 1
        if len(examples) < 8 and not re.sub(r'<[^>]+>', '', inner).strip(): examples.append((code, g, len(cols), [w for w, _ in cols]))
print(f"gold image rows (>=2 image-only columns, any depth): {tot_rows} on {len(pages)} pages")
print("by column count:", dict(ncols))
print("top width patterns:")
for k, v in widths.most_common(10): print(f"   {v:4d}  {k}")
print(f"paired Claude page: images CONSECUTIVE in one column {consec} / scattered {scattered} / inside a widget {widget} / not all present {missing}")
print("examples (consecutive):", examples)
