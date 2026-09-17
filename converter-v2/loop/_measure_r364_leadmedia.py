#!/usr/bin/env python3
"""r364 (session 21) — the LEAD-MEDIA half measured as its own class (LOOP §3 step 3).
For every page the ON probe changed ONLY through lead_media_tags (the set difference of
_r364s21_changed_pages.txt minus _r364s21_changed_pages_NOMEDIA.txt), find each activity box whose
ON page carries MORE media elements (img / iframe / video / audio) than the disk page, and ask the
gold: does the SAME-NUMBERED gold box carry a media element too?  Share by template family and
subject prefix.  Writes _r364_leadmedia.json + prints the summary."""
import os, re, sys, json, collections, io
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs

def rd(p): return io.open(p, encoding="utf-8", errors="replace").read()
BOX = re.compile(r'<div class="activity[^"]*"[^>]*number="([^"]+)"')
MEDIA = re.compile(r'<(img|iframe|video|audio)\b', re.I)
def boxes(html):
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    out = {}
    ms = list(BOX.finditer(html))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(html)
        seg = html[m.end():end]
        out.setdefault(m.group(1).upper(), 0)
        out[m.group(1).upper()] += len(MEDIA.findall(seg))
    return out

allc = set(l.strip() for l in io.open(os.path.join(HERE, "_r364s21_changed_pages.txt")) if l.strip())
nomed = set(l.strip() for l in io.open(os.path.join(HERE, "_r364s21_changed_pages_NOMEDIA.txt")) if l.strip())
only = sorted(allc - nomed)
ON = os.path.join(HERE, "_r364_on_s21")
rows = []; byfam = collections.defaultdict(lambda: [0, 0]); bysub = collections.defaultdict(lambda: [0, 0])
nopair = 0; nobox_gold = 0
for rel in only:
    code, base = rel.split("/")
    gold = None; disk = None
    for n, cp, hp in pairs(code):
        if os.path.basename(cp) == base: gold, disk = hp, cp; break
    if not gold: nopair += 1; continue
    fam = os.path.normpath(gold).split(os.sep)[-3]
    bd, bo, bg = boxes(rd(disk)), boxes(rd(os.path.join(ON, code, base))), boxes(rd(gold))
    for num, cnt in bo.items():
        if cnt <= bd.get(num, 0): continue
        if num not in bg: nobox_gold += 1; verdict = "gold-no-box"
        else: verdict = "gold-media" if bg[num] > 0 else "gold-no-media"
        rows.append({"module": code, "page": base, "family": fam, "box": num, "disk": bd.get(num, 0), "on": cnt, "gold": bg.get(num), "verdict": verdict})
        if verdict != "gold-no-box":
            byfam[fam][0] += 1; bysub[code[:3]][0] += 1
            if verdict == "gold-media": byfam[fam][1] += 1; bysub[code[:3]][1] += 1
json.dump(rows, io.open(os.path.join(HERE, "_r364_leadmedia.json"), "w", encoding="utf-8"), indent=1)
tot = sum(v[0] for v in byfam.values()); yes = sum(v[1] for v in byfam.values())
print(f"lead-media-only pages {len(only)} (no pair {nopair}); boxes that GAINED media in ON: {len(rows)}; gold has no such box {nobox_gold}")
print(f"of the {tot} boxes the gold also numbers: gold carries media in {yes} = {yes/max(1,tot):.2f}")
print("by template family (n / share):", {k: (v[0], round(v[1]/max(1,v[0]), 2)) for k, v in sorted(byfam.items())})
print("by subject prefix (n / share):", {k: (v[0], round(v[1]/max(1,v[0]), 2)) for k, v in sorted(bysub.items(), key=lambda x: -x[1][0])})
c = collections.Counter(r["verdict"] for r in rows); print("verdicts", dict(c))
print("gold-no-media examples:", [(r["module"], r["page"], r["box"]) for r in rows if r["verdict"] == "gold-no-media"][:12])
