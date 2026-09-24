#!/usr/bin/env python3
"""Session 45 Round 7 — lesson pages whose Claude #module-menu-content carries NO text while the gold's carries some: is the gold's menu
text in Claude's BODY instead (a placement defect) or absent? Per module, with the WT marker that precedes the block (the tag line before
the gold menu's first sentence). WSL, from outputs/: python3 _s45_r7_emptymenu.py > _s45_r7_emptymenu.log"""
import os, re, io, json, glob, collections, html as H
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
def n(t): return re.sub(r"[^a-z0-9ā-ž ]+", "", re.sub(r"\s+", " ", H.unescape(t).lower())).strip()
def split_regions(path):
    s = io.open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    m = s.find('id="module-menu-content"'); b = s.find('id="body"')
    if m >= 0: m = s.find(">", m) + 1
    bs = s.rfind("<", 0, b) if b >= 0 else -1
    menu = s[m:bs] if (m > 0 and bs > m) else ""
    body = s[s.find(">", b) + 1:] if b >= 0 else s
    body = re.sub(r'<p class="cv2-note"[^>]*>.*?</p>', " ", body, flags=re.S)
    tx = lambda h: n(re.sub(r"<[^>]+>", " ", h))
    return tx(menu), tx(body)
pp = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_diff_miner.json"), encoding="utf-8"))["per_page"]
per = collections.defaultdict(lambda: collections.Counter()); ex = {}
for rec in pp:
    code, cpage, gpage = rec["module"], rec["page"], rec["gold"]
    if re.search(r"_0_0\.html$", cpage): continue
    gm, gb = split_regions(os.path.join(_corpus.mdir(GOLD, code), gpage))
    cm, cb = split_regions(os.path.join(_corpus.mdir(CL, code), cpage))
    if len(gm) < 40 or len(cm) > 0: continue
    words = gm.split()
    sh = [" ".join(words[i:i + 5]) for i in range(0, max(1, len(words) - 4), 3)]
    inbody = sum(1 for x in sh if x in cb) / max(1, len(sh))
    k = "in-body" if inbody >= 0.5 else "absent"
    per[code][k] += 1
    ex.setdefault((code, k), cpage)
tot = collections.Counter()
for c, v in per.items(): tot.update(v)
print("lesson pages, Claude menu EMPTY, gold menu has text:", dict(tot), "modules", len(per))
for c, v in sorted(per.items(), key=lambda x: -sum(x[1].values())):
    print(f"  {c:10s} {dict(v)}  e.g. {ex.get((c, 'in-body')) or ex.get((c, 'absent'))}")
