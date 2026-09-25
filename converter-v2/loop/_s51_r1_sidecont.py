#!/usr/bin/env python3
"""_s51_r1_sidecont.py — session 51 Round 1 PICK: every activity-sidebar side column in Claude's output (an activity box's
row carrying `col-md-4 … > div.alertActivity`) and what the NEXT row opens with. When the writer's RHS box sat INSIDE the
activity, the box closed at the RHS tag and the activity's remaining content (the widget, the questions) ships in the next row —
as a new activity box (untitled, or opening on a hand-off) or as free content. The gold keeps the activity whole beside its
sidebar. WSL, from reference/tests/. Reads the Claude corpus on disk."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE

SIDE = re.compile(r'<div class="[^"]*\bcol-md-4\b[^"]*">\s*<div class="alertActivity[^"]*"', re.I)
ROW = re.compile(r'<div class="row[^"]*">', re.I)
strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
cnt = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    d = _corpus.mdir(CLAUDE, code)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".html"): continue
        html = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
        for m in SIDE.finditer(html):
            # the activity box this sidebar pairs with: the last activity open before it
            prev = html.rfind('<div class="activity', 0, m.start())
            pm = re.match(r'<div class="(activity[^"]*)"[^>]*?(?: number="([^"]*)")?', html[prev:prev + 200]) if prev >= 0 else None
            # the next row after this side column's row closes
            nx = ROW.search(html, m.end())
            if not nx: cnt["END"] += 1; continue
            seg = html[nx.start(): nx.start() + 3000]
            a = re.match(r'<div class="row[^"]*">\s*<div class="[^"]*">\s*<div class="(activity[^"]*)"[^>]*?(?: number="([^"]*)")?>', seg)
            if a:
                inner = seg[a.end(): a.end() + 1200]
                titled = re.search(r"^\s*<div class=\"row\">\s*<div class=\"col-12\">\s*<h[2-5]", inner) is not None
                handoff = "cv2-int-ref" in inner[:400] or "cv2-interactive" in inner[:400]
                kind = "NEXT-BOX titled" if titled else ("NEXT-BOX handoff-first" if handoff else "NEXT-BOX untitled")
            else:
                kind = "NEXT free"
            cnt[kind] += 1; mods[kind].add(code)
            ex[kind].append(f"{f} prev={pm.group(2) if pm else '?'} next={a.group(2) if a else '-'} | {strip(seg)[:110]}")
for k, n in cnt.most_common(): print(n, k, "modules", len(mods[k]))
for k in ("NEXT-BOX handoff-first", "NEXT-BOX untitled", "NEXT-BOX titled"):
    print("==", k); print("\n".join(ex[k][:25]))
