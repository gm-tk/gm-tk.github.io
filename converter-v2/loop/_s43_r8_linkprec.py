#!/usr/bin/env python3
"""Session 43 Round 8 — precision of a link-weave round: every href the ON pages (saved by `_s42_probe_run.sh <TAG> SAVE` under
outputs/_<TAG>_on/) carry that the disk page does not, checked against the gold module (the same URL as an href anywhere in its pages),
split by host kind (a developer asset host — Drive / SharePoint / D2L / a picture source — vs a public web page) and by the anchor text.
Usage (WSL, outputs/): python3 _s43_r8_linkprec.py <TAG>"""
import os, re, sys, glob, html, collections
TAG = sys.argv[1]
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ON = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"_{TAG}_on")
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"))
import _corpus
CL = os.path.join(ROOT, "01-Claude_Modules_"); GO = os.path.join(ROOT, "01-Finalized_Modules_")
A = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S)
def key(u): return re.sub(r"^https?://(www\.)?", "", html.unescape(u).strip().rstrip(".,;:/"), flags=re.I).lower()
DEV = re.compile(r"drive\.google|docs\.google|sharepoint\.com|desire2learn|images\.app\.goo\.gl|safelinks|istock|shutterstock|alamy|stock\.adobe|canva\.com|claude\.site", re.I)
agg = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set)
for p in glob.glob(os.path.join(ON, "**", "*.html"), recursive=True):
    name = os.path.basename(p); code = os.path.basename(os.path.dirname(p))
    if not re.match(r"[A-Z]", code): code = re.match(r"([A-Z]+[0-9A-Z]*?)(?:_\d)", name).group(1) if re.match(r"([A-Z]+[0-9A-Z]*?)(?:_\d)", name) else code
    dp = os.path.join(_corpus.mdir(CL, code), name)
    if not os.path.isfile(dp): continue
    strip = lambda s: re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    onl = [(key(h), re.sub(r"<[^>]+>", "", t).strip()) for h, t in A.findall(strip(open(p, encoding="utf-8").read()))]
    dsk = collections.Counter(key(h) for h, _ in A.findall(strip(open(dp, encoding="utf-8").read())))
    gh = {key(h) for g in glob.glob(os.path.join(_corpus.mdir(GO, code), "*.html")) for h, _ in A.findall(open(g, encoding="utf-8", errors="replace").read().split("<div class=\"acks")[0])}   # the gold BODY only (its acks credit every source)
    seen = collections.Counter()
    for k, t in onl:
        seen[k] += 1
        if seen[k] <= dsk.get(k, 0): continue           # this href was already on the disk page
        kind = "dev asset host" if DEV.search(k) else "public web"
        g = "gold has URL" if k in gh else "gold lacks URL"
        kk = (kind, g); agg[kk] += 1; mods[kk].add(code)
        if len(ex[kk]) < 6: ex[kk].append(f"{code}: «{t[:30]}» {k[:45]}")
print(f"added hrefs: {sum(agg.values())}")
for kk, n in sorted(agg.items(), key=lambda kv: -kv[1]):
    print(f"{kk[0]:15s} | {kk[1]:15s} | {n:4d} | {len(mods[kk]):3d} modules | {' ;; '.join(ex[kk])[:330]}")
