#!/usr/bin/env python3
"""Session 28 / Task 3 — the WJFUN tile dialect, measured: per module the gold's phase structure (fundamentalsPanel count,
phases-nav labels, menu tab count) against every candidate delimiter in the Writers Template ([Tile N …] markers, [End page]
markers, the 'Tab N *label*' side-nav list, [H1] headings, LI/SC-for-tile tags). Which delimiter predicts the gold's phase count?"""
import os, re, glob, io
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_", "Fundamentals")
RED = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534")
rows = []
for d in sorted(glob.glob(os.path.join(GOLD, "WJFUN*")) + glob.glob(os.path.join(GOLD, "JPFUN0[12]"))):
    code = os.path.basename(d)
    wt = glob.glob(os.path.join(d, f"{code} Writers Template*_parsed.txt"))
    html = glob.glob(os.path.join(d, "*.html"))
    if not wt or not html: continue
    t = RED.sub("", io.open(wt[0], encoding="utf-8", errors="replace").read())
    h = io.open(html[0], encoding="utf-8", errors="replace").read()
    panels = len(re.findall(r'class="fundamentalsPanel"', h))
    nav = re.findall(r'<div class="phases">(.*?)</div>\s*</div>', h, re.S)
    navlabels = re.findall(r'<div phase="\d+">\s*<p>(.*?)</p>', h, re.S)
    tabs = len(re.findall(r'<div class="tab-pane">', h))
    tile_markers = re.findall(r"\[\s*tile\s*(\d+)[^\]]*\]", t, re.I)
    tile_any = len(re.findall(r"\[\s*tile\b[^\]]*\]", t, re.I))
    endpage = len(re.findall(r"\[\s*end page\s*\]", t, re.I))
    tabn = re.findall(r"^\s*Tab\s+(\d+)\s+\*?([^*\n]+)", t, re.M | re.I)
    h1 = re.findall(r"\[H1\]\s*([^\n]+)", t, re.I)
    li = len(re.findall(r"\[\s*learning intention[^\]]*\]", t, re.I))
    sc = len(re.findall(r"\[\s*success criteria[^\]]*\]", t, re.I))
    lessons = len(re.findall(r"\[\s*lesson content\s*\]", t, re.I))
    rows.append((code, panels, len(navlabels), tabs, len(set(tile_markers)), tile_any, endpage, len(tabn), len(h1), li, sc, lessons,
                 " / ".join(x.strip() for x in navlabels)[:60], " / ".join(x[1].strip() for x in tabn)[:60]))
print("code      gold: panels nav tabs | WT: tileN tileAny endpage tabN h1 LI SC lessonContent | gold nav labels | WT Tab labels")
for r in rows:
    print(f"{r[0]:9} {r[1]:6} {r[2]:3} {r[3]:4} | {r[4]:5} {r[5]:7} {r[6]:7} {r[7]:4} {r[8]:2} {r[9]:2} {r[10]:2} {r[11]:2} | {r[12]} | {r[13]}")
def agree(idx, name):
    n = sum(1 for r in rows if r[0].startswith("WJFUN") and r[idx] == r[1] and r[1] > 0)
    print(f"  {name:12} == gold panel count on {n}/{sum(1 for r in rows if r[0].startswith('WJFUN'))} WJFUN modules")
print("\n== which WT count predicts the gold's panel count?")
for idx, name in ((4, "tileN"), (5, "tileAny"), (6, "endpage"), (7, "tabN"), (8, "h1"), (11, "lessonContent")):
    agree(idx, name)
n = sum(1 for r in rows if r[0].startswith("WJFUN") and r[6] + 1 == r[1]); print(f"  endpage+1    == gold on {n}")
n = sum(1 for r in rows if r[0].startswith("WJFUN") and r[2] == r[1]); print(f"  gold nav count == gold panel count on {n} (sanity)")
