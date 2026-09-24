#!/usr/bin/env python3
"""Session 44 Round 5 — KB constraint 62 sized on TASK components only (the KB: "D&D, quizzes, self check, games, ordering, sliders";
supporting widgets — carousel / accordion / flipCard / tabs / modal / speechBubble / hint / infoTrigger — never counted). Claude: a built
widget root of a task class, or a hand-off box whose banner names a task type ({CODE}-INT-{p}-{n}-{type}). Gold: a task-class widget root.
Per side: activity boxes by task count; Claude's 2+ boxes by type pair and family. WSL, from reference/tests:
python3 ../../outputs/_s44_r5_multitask.py"""
import os, re, sys, glob, io, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
import _corpus
ROOT = os.path.normpath(os.path.join(os.getcwd(), "..", "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
TASK = {"dragAndDrop", "clickDrop", "multiChoiceQuiz", "dropDown", "typing", "radioQuiz", "dropQuiz", "selectionBox", "selfCheck", "bingo",
        "memoryGame", "crossword", "wordFind", "wordSelect", "reorder", "clickingOrder", "slider", "sliderChart", "sketcher", "puzzle", "wordHighlighter"}
VOID = {"br", "img", "hr", "input", "source", "meta", "link", "audio", "wbr"}
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st = []; s.boxes = []; s.banner = None
    def _box(s):
        for x in reversed(s.st):
            if x[1] is not None: return x[1]
        return None
    def handle_starttag(s, t, a):
        if t in VOID: return
        d = dict(a); cls = (d.get("class") or "").split()
        is_act = t == "div" and "activity" in cls
        inside = any(x[2] for x in s.st)
        typ = next((c for c in cls if c in TASK), None) if not is_act else None
        is_w = bool(typ) or "cv2-interactive" in cls
        if typ and not inside:
            b = s._box()
            if b is not None: b["types"].append(typ)
        box = {"types": []} if is_act else None
        if box is not None: s.boxes.append(box)
        if "cv2-int-ref" in cls and not inside: s.banner = s._box()
        s.st.append((t, box, is_w or inside))
    def handle_endtag(s, t):
        while s.st:
            if s.st.pop()[0] == t: break
    def handle_data(s, d):
        if s.banner is not None:
            m = re.search(r"-INT-\d+-\d+-([A-Za-z]+)", d)
            if m:
                if m.group(1) in TASK: s.banner["types"].append(m.group(1) + "*")
                s.banner = None
def boxes(path):
    x = P()
    try: x.feed(io.open(path, encoding="utf-8", errors="replace").read())
    except Exception: return []
    return [b["types"] for b in x.boxes]
res = {"claude": collections.Counter(), "gold": collections.Counter()}; pair = collections.Counter(); fam = collections.Counter()
pages = set(); mods = set(); gpages = set()
for code in _corpus.gate_mods(CL):
    for side, root in (("claude", CL), ("gold", GOLD)):
        try: d = _corpus.mdir(root, code)
        except Exception: continue
        for p in glob.glob(os.path.join(d, "*.html")):
            for ty in boxes(p):
                n = len(ty); res[side]["2+" if n >= 2 else str(n)] += 1
                if n >= 2:
                    if side == "claude":
                        pages.add(p); mods.add(code); pair[" + ".join(sorted(t.rstrip("*") for t in ty))] += 1
                        fam[re.match(r"[A-Z]+\d?", code).group(0)] += 1
                    else: gpages.add(p)
print("activity boxes by TASK-component count:", {k: dict(v) for k, v in res.items()})
print(f"Claude 2+ boxes on {len(pages)} pages / {len(mods)} modules; gold 2+ boxes on {len(gpages)} pages")
print("Claude 2+ by type set:", dict(pair.most_common(15)))
print("Claude 2+ by family:", dict(fam.most_common(20)))
