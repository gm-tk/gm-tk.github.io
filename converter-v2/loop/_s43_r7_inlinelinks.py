#!/usr/bin/env python3
"""Session 43 Round 7 PICK — THE INLINE LINK THAT LOSES ITS HREF. The writer's inline hyperlink in the parsed text is
`__anchor words__ [LINK: url]` (the underlined run + the link). For every such NON-MEDIA link in a module's Writers Template, on Claude's
pages: the anchor words present as an <a href=url> (KEPT), the words present but no href to that URL anywhere (HREF LOST — the
ANZH104-6.0 "Google Lens" case), or the words absent (TEXT LOST). The container of the words on Claude's page (activity box / widget
/ table / alert / free body …) and the gold's treatment (an <a> with that URL or not) are recorded. Run under WSL from
reference/tests: python3 ../../outputs/_s43_r7_inlinelinks.py > ../../outputs/_s43_r7_inlinelinks.log"""
import os, re, sys, glob, html, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
LINK = re.compile(r"__([^_]{2,120}?)__\s*\[LINK:\s*(https?://[^\]\s]+)\s*\]")
MEDIA = re.compile(r"istockphoto|shutterstock|gettyimages|unsplash|pexels|youtu\.?be|vimeo|\.(?:jpe?g|png|gif|svg|webp|mp3|mp4|wav)\b", re.I)
CONT = ["activity", "cv2-interactive", "accordion", "tab-pane", "carousel", "flipCard", "TKmodal", "alert", "supervisor", "speechBubble", "table"]
def norm(s): return re.sub(r"\s+", " ", re.sub(r"[^0-9a-zāēīōū]+", " ", html.unescape(s).lower())).strip()
def ukey(u): return re.sub(r"^https?://(www\.)?", "", html.unescape(u).strip().rstrip(".,;:/"), flags=re.I).lower()
def container(s, pos):
    stack = []
    for m in re.finditer(r"<(/?)(div|table)\b([^>]*)>", s[:pos], re.I):
        if m.group(1):
            if stack: stack.pop()
        else:
            c = re.search(r'class="([^"]*)"', m.group(3)); stack.append(("table" if m.group(2).lower() == "table" else "") + " " + (c.group(1) if c else ""))
    for cls in reversed(stack):
        for w in CONT:
            if w in cls.split() or (w == "table" and cls.startswith("table")): return w
    return "body"
agg = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list); pages = collections.defaultdict(set)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not (os.path.isdir(hd) and os.path.isdir(cd)): continue
    wt = ""
    for f in glob.glob(os.path.join(hd, "*_parsed.txt")):
        if "media list_parsed" in f.lower() and "writers template" not in f.lower(): continue
        wt += open(f, encoding="utf-8", errors="replace").read() + "\n"
    if not wt: continue
    C = [(os.path.basename(p), re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), open(p, encoding="utf-8", errors="replace").read(), flags=re.S))
         for p in glob.glob(os.path.join(cd, "*.html"))]
    chref = {ukey(u) for _, s in C for u in re.findall(r'href="([^"]+)"', s)}
    ghtml = "\n".join(open(p, encoding="utf-8", errors="replace").read() for p in glob.glob(os.path.join(hd, "*.html")))
    ghref = {ukey(u) for u in re.findall(r'href="([^"]+)"', ghtml)}
    for m in LINK.finditer(wt):
        words, url = m.group(1).strip(), m.group(2)
        if MEDIA.search(url): continue
        k = ukey(url); w = norm(words)
        if len(w) < 3: continue
        if k in chref: fate, cont, pg = "KEPT", "-", None
        else:
            fate, cont, pg = "TEXT LOST", "-", None
            for name, s in C:
                txt = norm(re.sub(r"<[^>]+>", " ", s))
                if w in txt:
                    # locate the words in the raw page for the container
                    idx = s.lower().find(words.lower()[:25])
                    fate, cont, pg = "HREF LOST", container(s, idx) if idx >= 0 else "?", name
                    break
        g = "gold <a>" if k in ghref else "gold no <a>"
        key = (fate, cont, g); agg[key] += 1; mods[key].add(code)
        if pg: pages[key].add((code, pg))
        if len(ex[key]) < (40 if key[1] == "tab-pane" else 3): ex[key].append(f"{code}: «{words[:30]}» {k[:40]}")
print("fate | Claude container | gold | links | pages | modules | examples")
for key, n in sorted(agg.items(), key=lambda kv: -kv[1])[:30]:
    print(f"{key[0]:9s} | {key[1]:15s} | {key[2]:11s} | {n:5d} | {len(pages[key]):4d} | {len(mods[key]):3d} | {' ;; '.join(ex[key])[:220]}")
