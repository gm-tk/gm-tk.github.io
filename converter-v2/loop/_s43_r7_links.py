#!/usr/bin/env python3
"""Session 43 Round 7 PICK — THE LINK CENSUS: does every hyperlink the writer typed reach Claude's module? For every URL in a module's
Writers Template (the combined WT + ML files counted; the Media List's own table rows excluded — they feed the acks), classified as
media (an image / video / audio host or file) or a LINK (everything else), check Claude's module: the URL as an href / src anywhere on
its pages, or anywhere in its visible text / comments / the {CODE}_interactives.txt worklist (a hand-off keeps it). Links LOST from
Claude are then checked against the gold (does the gold carry the same URL?). Aggregated by the writer tag at / above the URL's line,
with families and examples. Run under WSL from reference/tests: python3 ../../outputs/_s43_r7_links.py > …log"""
import os, re, sys, glob, html, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
URL = re.compile(r"https?://[^\s\]\)\"'<>|║│]+")
MEDIA = re.compile(r"istockphoto|shutterstock|gettyimages|unsplash|pexels|youtu\.?be|vimeo|\.(?:jpe?g|png|gif|svg|webp|mp3|mp4|wav)\b", re.I)
TAG = re.compile(r"🔴\[RED TEXT\]\s*\[([^\]\[]{1,40})\]")
def key(u):
    u = html.unescape(u).strip().rstrip(".,;:")
    u = re.sub(r"^https?://(www\.)?", "", u, flags=re.I).rstrip("/").lower()
    return u
agg = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list); fam = collections.defaultdict(collections.Counter)
tot = collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not (os.path.isdir(hd) and os.path.isdir(cd)): continue
    L = []
    for f in glob.glob(os.path.join(hd, "*_parsed.txt")):
        if "media list_parsed" in f.lower() and "writers template" not in f.lower(): continue
        L += open(f, encoding="utf-8", errors="replace").read().splitlines()
    if not L: continue
    ctext = "\n".join(open(p, encoding="utf-8", errors="replace").read() for p in glob.glob(os.path.join(cd, "*.html")))
    ctext += "\n".join(open(p, encoding="utf-8", errors="replace").read() for p in glob.glob(os.path.join(cd, "*_interactives.txt")))
    ckeys = {key(u) for u in URL.findall(html.unescape(ctext))}
    gtext = "\n".join(open(p, encoding="utf-8", errors="replace").read() for p in glob.glob(os.path.join(hd, "*.html")))
    gkeys = {key(u) for u in URL.findall(html.unescape(gtext))}
    in_media_table = False
    for i, line in enumerate(L):
        if re.search(r"media list|item\s*no|asset\s*(?:type|id)", line, re.I) and "TABLE" in "".join(L[max(0, i - 2): i + 1]): in_media_table = True
        for u in URL.findall(line):
            if MEDIA.search(u): continue
            k = key(u)
            if len(k) < 8: continue
            tot["links"] += 1
            if any(k == c or (len(k) > 25 and (k in c or c in k)) for c in ckeys): continue
            tag = None
            for j in range(i, max(-1, i - 8), -1):
                m = TAG.search(L[j])
                if m: tag = re.sub(r"\d+", "N", m.group(1).strip().lower()[:25]); break
            tag = tag or "(no tag)"
            ing = "gold HAS it" if any(k == g or (len(k) > 25 and (k in g or g in k)) for g in gkeys) else "gold lacks it"
            kk = (tag, ing); agg[kk] += 1; mods[kk].add(code); fam[kk][re.match(r"[A-Z]+", code).group(0)] += 1
            if len(ex[kk]) < 3: ex[kk].append(f"{code} L{i + 1}: {k[:70]}")
print(f"writer links (non-media) {tot['links']}; lost from Claude {sum(agg.values())}")
print("tag | gold | lost links | modules | families | examples")
for kk, n in sorted(agg.items(), key=lambda kv: -kv[1])[:40]:
    print(f"{kk[0]:25s} | {kk[1]:13s} | {n:4d} | {len(mods[kk]):3d} | {dict(fam[kk].most_common(4))} | {' ;; '.join(ex[kk])[:230]}")
