#!/usr/bin/env python3
"""Session 44 Round 5 — KB constraint 62 ("each activity wrapper contains at most ONE interactive component; split + renumber"): count the
activity boxes holding 2+ interactive components on the Claude pages vs the gold pages (scored population), by template and family.
An interactive component = a direct-or-nested element whose class is a widget root (the compare_structure widget list minus `activity`
and the layout classes) or a cv2 hand-off box; nested widgets inside a counted widget are not counted again.
WSL, from reference/tests: python3 ../../outputs/_s44_r5_multiwidget.py"""
import os, re, sys, glob, io, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
import _corpus, compare_structure as cs
ROOT = os.path.normpath(os.path.join(os.getcwd(), "..", "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
W = set(cs.INTERACTIVE_CLASSES) - {"activity", "question", "choice", "label", "circle", "noBG", "marg0", "paddingB", "showGrid", "rQNumbers",
                                   "dropContainer", "dragContainer", "clickDropContent", "flipCardsContainer", "hintDropContent", "carouselBorder"}
W |= {"cv2-interactive"}
VOID = {"br", "img", "hr", "input", "source", "meta", "link", "audio", "wbr"}
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st = []; s.boxes = []
    def handle_starttag(s, t, a):
        if t in VOID: return
        cls = (dict(a).get("class") or "").split()
        is_act = t == "div" and "activity" in cls
        is_w = any(c in W for c in cls) and not is_act
        inside_w = any(x[2] for x in s.st)
        if is_w and not inside_w:
            for x in reversed(s.st):
                if x[1] is not None: x[1]["n"] += 1; break
        box = {"n": 0} if is_act else None
        if box is not None: s.boxes.append(box)
        s.st.append((t, box, is_w or inside_w))
    def handle_endtag(s, t):
        while s.st:
            if s.st.pop()[0] == t: break
def boxes(path):
    x = P()
    try: x.feed(io.open(path, encoding="utf-8", errors="replace").read())
    except Exception: return []
    return [b["n"] for b in x.boxes]
res = {"claude": collections.Counter(), "gold": collections.Counter()}
fam = collections.defaultdict(lambda: collections.Counter()); pages = collections.Counter(); mods = set()
for code in _corpus.gate_mods(CL):
    for side, root in (("claude", CL), ("gold", GOLD)):
        try: d = _corpus.mdir(root, code)
        except Exception: continue
        for p in glob.glob(os.path.join(d, "*.html")):
            ns = boxes(p)
            for n in ns: res[side]["2+" if n >= 2 else str(n)] += 1
            m = sum(1 for n in ns if n >= 2)
            if m and side == "claude":
                pages[code] += 1; mods.add(code); fam[re.match(r"[A-Z]+\d?", code).group(0)]["boxes"] += m
print("activity boxes by interactive count:", {k: dict(v) for k, v in res.items()})
print("Claude pages with a 2+ box:", sum(pages.values()), "modules:", len(mods))
print("by family (Claude 2+ boxes):", dict(sorted(((f, c["boxes"]) for f, c in fam.items()), key=lambda x: -x[1])[:25]))
