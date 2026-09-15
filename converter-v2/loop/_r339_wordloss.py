#!/usr/bin/env python3
"""_r339_wordloss.py — ROUND 339 proof: over the affected pages, the ON output (outputs/_r339_on/<code>/<page>) must lose no
writer word vs the disk page; the only permitted losses are the dropped button labels (the embed's own play button / the
video's title) and converter notes (chrome). Run from reference/tests under WSL after the probe's --save run."""
import os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); import _corpus
OUT = os.path.join(HERE, "..", "..", "01-Claude_Modules_"); ON = os.path.join(HERE, "_r339_on")
AFF = [l.strip() for l in open(os.path.join(HERE, "_r339_affected.txt")) if l.strip()]

def words(html):
    body = html.split("<body", 1)[-1]
    body = re.sub(r"<script[\s\S]*?</script>", "", body)
    body = re.sub(r'<p class="cv2-note"[^>]*>[\s\S]*?</p>', "", body)   # converter notes are chrome
    t = re.sub(r"<[^>]+>", " ", body); t = re.sub(r"&[a-z#0-9]+;", " ", t)
    return collections.Counter(w.lower() for w in re.findall(r"[\w'’-]+", t))

lost_total = collections.Counter(); pages = 0; embeds = 0; links_lost = 0
for c in AFF:
    d = os.path.join(ON, c)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        a = open(os.path.join(_corpus.mdir(OUT, c), f), encoding="utf-8").read(); b = open(os.path.join(d, f), encoding="utf-8").read()
        if a == b: continue
        pages += 1; embeds += b.count("videoSection") - a.count("videoSection")
        lost = words(a) - words(b)
        for w, n in lost.items(): lost_total[w] += n
        # hrefs that vanished (other than the video URLs that became iframes)
        ha = set(re.findall(r'href="(https?://[^"]+)"', a)); hb = set(re.findall(r'href="(https?://[^"]+)"', b))
        gone = [h for h in ha - hb if not re.search(r"youtu|vimeo", h)]
        if gone: links_lost += len(gone); print(c, f, "NON-VIDEO LINK LOST:", gone)
        big = [w for w in lost if len(w) > 12]
        if big: print(c, f, "lost long words:", big[:8])
print("pages", pages, "| new videoSection embeds", embeds, "| non-video links lost", links_lost)
print("lost words (all):", lost_total.most_common(40))
