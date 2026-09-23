#!/usr/bin/env python3
"""Session 41 Round 8 PICK — THE OVER-CAPTURE PAGES: for every body_compare over-capture page (the gate's rule), the biggest
top-level hand-off box on the Claude page (by text length), its reference code and its worklist type + the first lines of its
captured content, tallied by type. Run under WSL from CONVERTER_V2/reference/tests."""
import json, os, re, sys, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE
rows = json.load(open("../../outputs/_fastloop_baseline/body_compare.json"))
oc = [r for r in rows if r["over_capture"] >= 0.40 and r["biggest_widget_chars"] > 400 and r["lost_blocks"] >= 3]
def top_boxes(s):
    out = []; i = 0
    while True:
        m = re.search(r'<div class="cv2-interactive[^"]*"[^>]*>', s[i:])
        if not m: break
        st = i + m.start(); depth = 0; j = st
        for t in re.finditer(r"<(/?)div\b[^>]*>", s[st:]):
            depth += -1 if t.group(1) else 1
            if depth == 0: j = st + t.end(); break
        out.append((m.group(0), s[st:j])); i = j if j > st else st + 1
    return out
tally = collections.Counter(); ex = collections.defaultdict(list)
for r in oc:
    code, page = r["page"].split("/")
    p = os.path.join(_corpus.mdir(CLAUDE, code), page)
    s = open(p, encoding="utf-8", errors="replace").read()
    boxes = top_boxes(s)
    if not boxes: tally["(no box)"] += 1; continue
    best = max(boxes, key=lambda b: len(re.sub(r"<[^>]+>", "", b[1])))
    ref = re.search(r'data-cv2-ref="([^"]+)"', best[0]); ref = ref.group(1) if ref else ""
    typ = "?"
    wl = os.path.join(_corpus.mdir(CLAUDE, code), f"{code}_interactives.txt")
    if ref and os.path.exists(wl):
        w = open(wl, encoding="utf-8", errors="replace").read()
        k = w.find(ref.replace(f"{code}-", f"{code}-INT-"))
        m = re.search(r"Type:\s*(\S+)", w[k:k + 800]) if k >= 0 else None
        typ = m.group(1) if m else "?"
    elif "bilingual-unbuilt" in best[0]: typ = "bilingual-unbuilt"
    tally[typ] += 1
    txt = H.unescape(re.sub(r"<[^>]+>", " ", best[1])); txt = re.sub(r"\s+", " ", txt).strip()
    ex[typ].append(f"{r['page']} over={r['over_capture']} lost={r['lost_blocks']} :: {txt[:150]}")
print("over-capture pages", len(oc))
for t, n in tally.most_common(): print(f"{n:4d} {t}")
for t, n in tally.most_common(6):
    print(f"\n== {t}")
    for e in ex[t][:6]: print("  ", e)
