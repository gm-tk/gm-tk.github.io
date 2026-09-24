#!/usr/bin/env python3
"""Session 44 Round 10 — the KB queue's UNVERIFIED rows, measured on the Claude corpus (and the gold for scale):
 c7  — no <span> inside a BODY h2–h5 (spans only on the header h1): body headings (inside #body, outside the module menu) holding a <span>,
       by the span's class (infoTrigger etc.);
 c15 — `noShuffle` only on explicit request: built widget roots carrying noShuffle, by type.
WSL, from outputs/: python3 _s44_r10_kbverify.py"""
import os, re, glob, io, collections
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
HS = re.compile(r"<(h[2-5])\b[^>]*>(.*?)</\1>", re.S)
def body(s):
    i = s.find('<div id="body"'); j = s.find('<div id="footer"')
    return s[i:j] if i >= 0 else ""
for side, root in (("CLAUDE", CL), ("GOLD", GOLD)):
    spans = collections.Counter(); pages = collections.defaultdict(set); ex = collections.defaultdict(list); nsh = collections.Counter()
    for p in glob.glob(os.path.join(root, "*", "*", "*.html")):
        s = io.open(p, encoding="utf-8", errors="replace").read(); b = body(s)
        for m in HS.finditer(b):
            for sm in re.finditer(r'<span\b([^>]*)>', m.group(2)):
                cls = (re.search(r'class="([^"]*)"', sm.group(1)) or [None, "(no class)"])[1]
                spans[(m.group(1), cls)] += 1; pages[(m.group(1), cls)].add(p)
                if len(ex[(m.group(1), cls)]) < 2: ex[(m.group(1), cls)].append(os.path.basename(p) + " " + re.sub(r"<[^>]+>", "", m.group(2))[:40])
        for m in re.finditer(r'<div class="([A-Za-z]+)([^"]*\bnoShuffle\b[^"]*)"', s): nsh[m.group(1)] += 1
    print(f"== {side} c7 body-heading spans (top):")
    for k, v in spans.most_common(10): print(f"   {k[0]} span.{k[1]}: {v} occ / {len(pages[k])} pages  e.g. {ex[k]}")
    print(f"== {side} c15 noShuffle widget roots:", dict(nsh.most_common()))
