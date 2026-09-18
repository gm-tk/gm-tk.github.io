#!/usr/bin/env python3
"""Session 26 Round 7 candidate — ADJACENT SIBLING <ol>s: Claude ships 202 `</ol>\s*<ol>` pairs, the gold 0. What does the gold
ship on those pages? Per page with >=1 Claude pair: Claude ol count, pairs, gold ol count, gold `start=` use, li counts, and what
the gold puts between its consecutive lists. Verdict buckets: MERGED (gold ol == claude ol - pairs), SAME (gold ol == claude ol),
OTHER. Live body only (the r392 carve). python3 _s26_r393_adjol.py"""
import os, sys, re, json
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
ADJO = re.compile(r"</ol>\s*<ol\b")
OL = re.compile(r"<ol\b[^>]*>"); LI = re.compile(r"<li\b")
buck = Counter(); bys = defaultdict(Counter); pages = 0; mods = set(); starts = Counter(); EX = []; between = Counter()
def ol_lis(s):
    # li count inside ol elements (rough: count li between each <ol ...> and its </ol>)
    n = 0
    for m in re.finditer(r"<ol\b[^>]*>(.*?)</ol>", s, re.S): n += len(LI.findall(m.group(1)))
    return n
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception:
            continue
        cl = "".join(live_pieces(ch)); gl = "".join(live_pieces(gh))
        cpairs = len(ADJO.findall(cl))
        if not cpairs: continue
        pages += 1; mods.add(code)
        col = len(OL.findall(cl)); gol = len(OL.findall(gl))
        gst = [m.group(0) for m in OL.finditer(gl) if "start=" in m.group(0)]
        starts["gold ol with start="] += len(gst); starts["gold ol"] += gol
        if gol == col - cpairs: b = "MERGED (gold ol = claude ol - pairs)"
        elif gol == col: b = "SAME count (gold keeps separate lists)"
        elif gol < col - cpairs: b = "gold FEWER than merged"
        else: b = "gold MORE than claude"
        buck[b] += 1; bys[f"{tf}/{subj}"][b] += 1
        # what sits between the gold's consecutive ols
        for m in re.finditer(r"</ol>(.*?)<ol\b", gl, re.S):
            mid = re.sub(r"\s+", " ", m.group(1)).strip()
            tag = re.findall(r"<([a-z0-9]+)\b", mid)
            between[",".join(tag[:4]) if tag else "(nothing)"] += 1
        if len(EX) < 8:
            m = ADJO.search(cl)
            EX.append(f"{os.path.basename(cp)[:-5]} [{b[:6]}] claude ol {col} pairs {cpairs} li {ol_lis(cl)} | gold ol {gol} li {ol_lis(gl)} start= {len(gst)} | …{re.sub(r'\s+',' ',cl[max(0,m.start()-70):m.start()])[-60:]} ⟂ {re.sub(r'\s+',' ',cl[m.end():m.end()+60])[:50]}")
print(f"==== Claude pages with an adjacent <ol> pair: {pages} pages / {len(mods)} modules ====")
for b, n in buck.most_common(): print(f"   {b:44s} {n:4d}  ({n/pages:.2f})")
print("   gold start= use:", dict(starts))
print("   between the gold's consecutive <ol>s (first tags):", between.most_common(8))
print("   by template/subject (>=5 pages):")
for k in sorted(bys, key=lambda x: -sum(bys[x].values())):
    t = sum(bys[k].values())
    if t >= 5: print(f"     {k:40s} n={t:3d}  " + "  ".join(f"{b.split(' ')[0]} {c}" for b, c in bys[k].most_common()))
print("   examples:"); [print("     ", e) for e in EX]
