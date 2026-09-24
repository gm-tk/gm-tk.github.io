#!/usr/bin/env python3
"""Session 43 Round 5 PICK — KB constraint 52's POSITIVE half: an iStock image's alt is its iStock / Getty title (the acks file, else
the URL slug). For every <img> on every Claude page (live tags only — a Mode-P commented-out reference counted separately), classify
the alt (empty / filled), whether the image is an iStock asset (the placeholder text or the src names iStock-<id>), whether that id's
URL (with its slug) is in the module's Writers Template (so the title is RECOVERABLE), and the nearest widget container class
(flipCard / carousel / TKmodal / speechBubble / table / accordion / tabs / body). Gold alongside: the share of the gold's iStock
images whose alt is filled. Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s43_r5_alt.py > …log"""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
WIDGETS = ["flipCard", "carousel", "TKmodal", "speechBubble", "bubble", "accordion", "tab-pane", "clickDrop", "dragAndDrop", "table",
           "alertImage", "activity", "super-content"]
IMG = re.compile(r"<img\b[^>]*>", re.I)
def ctx(s, pos):
    """the innermost known container class open before pos (a cheap stack walk over div/table/td opens and closes)."""
    stack = []
    for m in re.finditer(r"<(/?)(div|table|td|li)\b([^>]*)>", s[:pos], re.I):
        if m.group(1):
            if stack: stack.pop()
        else:
            cls = re.search(r'class="([^"]*)"', m.group(3))
            stack.append((m.group(2).lower(), cls.group(1) if cls else ""))
    for tag, cls in reversed(stack):
        for w in WIDGETS:
            if w in cls.split() or (w == "table" and tag == "table") or (w == "bubble" and "bubble" in cls): return w
    return "body"
agg = collections.Counter(); mods = collections.defaultdict(set); gagg = collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not (os.path.isdir(hd) and os.path.isdir(cd)): continue
    wt = " ".join(open(f, encoding="utf-8", errors="replace").read() for f in glob.glob(os.path.join(hd, "*_parsed.txt")))
    wt_ids = set(re.findall(r"istockphoto\.com/[^\s\]]*?gm-?(\d{6,10})", wt))
    for p in glob.glob(os.path.join(cd, "*.html")):
        s = open(p, encoding="utf-8", errors="replace").read()
        live = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), s, flags=re.S)       # blank the comments, keep offsets
        for m in IMG.finditer(live):
            tag = m.group(0)
            alt = re.search(r'\balt="([^"]*)"', tag)
            filled = bool(alt and alt.group(1).strip())
            idm = re.search(r"iStock-(\d{6,10})", tag)
            kind = "iStock" if idm else "other"
            rec = "recoverable" if idm and idm.group(1) in wt_ids else ("-" if not idm else "no WT url")
            k = (ctx(live, m.start()), kind, rec, "filled" if filled else "EMPTY")
            agg[k] += 1; mods[k].add(code)
    for p in glob.glob(os.path.join(hd, "*.html")):
        s = re.sub(r"<!--.*?-->", " ", open(p, encoding="utf-8", errors="replace").read(), flags=re.S)
        for m in IMG.finditer(s):
            tag = m.group(0)
            if not re.search(r"iStock-?\d{6,10}", tag): continue
            alt = re.search(r'\balt="([^"]*)"', tag)
            gagg["filled" if alt and alt.group(1).strip() else "EMPTY"] += 1
print("GOLD iStock images:", dict(gagg))
print("container | kind | title | alt | images | modules")
for k, n in sorted(agg.items(), key=lambda kv: -kv[1]):
    print(f"{k[0]:13s} | {k[1]:6s} | {k[2]:11s} | {k[3]:6s} | {n:6d} | {len(mods[k]):4d}")
