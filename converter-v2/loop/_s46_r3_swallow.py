#!/usr/bin/env python3
"""Session 46 Round 3 — the text the GOLD keeps as free body (outside every widget / activity box) that Claude ships INSIDE an un-built
widget's hand-off box: per box widget type, and where in the box it sits (the box's LAST blocks = a capture that ran past the widget's end
vs. the middle). Pairing = the miner's own (outputs/_diff_miner.json per_page). WSL, from outputs/: python3 _s46_r3_swallow.py"""
import os, re, sys, io, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
from _s46_goldloc import P, fold
import _corpus
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
HUMAN = os.path.join(ROOT, "01-Finalized_Modules_"); CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
WID = re.compile(r"accordion|accContent|carousel|flipCard|tabs|clickDrop|dropDown|shapeHover|modal|dragAndDrop|multiChoiceQuiz|cv2-interactive|activity|speechBubble|dropQuiz|typing|reorder|radioQuiz|selfCheck|hint")
pp = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_diff_miner.json"), encoding="utf-8"))["per_page"]
def nodes(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.nodes
ALL = []   # session 46 Round 4: every swallowed block (code, page, box type, text) for the member-level probe
by = collections.Counter(); pos = collections.Counter(); mods = collections.defaultdict(set); pages = collections.defaultdict(set); ex = collections.defaultdict(list)
for rec in pp:
    code, page, gold = rec["module"], rec["page"], rec["gold"]
    try:
        g = nodes(os.path.join(_corpus.mdir(HUMAN, code), gold)); c = nodes(os.path.join(_corpus.mdir(CLAUDE, code), page))
    except Exception:
        continue
    gfree = set()
    for d, st in g:
        if not any(i == "body" for _, _, i in st): continue
        if any(WID.search(cl or "") for _, cl, _ in st): continue
        t = fold(d)
        if len(t) >= 30: gfree.add(t)
    # Claude hand-off boxes: collect each box's text blocks in order, with the box's widget type
    boxes = collections.OrderedDict()
    for d, st in c:
        box = None
        for tag, cl, idv in st:
            if "cv2-int-raw" in (cl or ""): box = box or "raw"
        if not box: continue
        # the box index = the nearest cv2-interactive ancestor's position in the stack
        key = tuple((tag, cl) for tag, cl, _ in st if "cv2-interactive" in (cl or ""))
        boxes.setdefault(key, []).append(d)
    for key, texts in boxes.items():
        head = next((t for t in texts if "INTERACTIVE (un-built)" in t), "")
        m = re.search(r"#\d+:\s*([^—\n]+?)\s*(?:—|$)", head)
        wtype = (m.group(1).strip() if m else "?")[:40]
        body = [t for t in texts if "INTERACTIVE (un-built)" not in t and len(fold(t)) >= 30]
        for i, t in enumerate(body):
            if fold(t) in gfree:
                by[wtype] += 1; mods[wtype].add(code); pages[wtype].add((code, page))
                pos["tail" if i >= len(body) - 3 else "middle"] += 1
                if len(ex[wtype]) < 4: ex[wtype].append(f"{code}/{page}: {t.strip()[:70]}")
                ALL.append({"code": code, "page": page, "type": wtype, "text": t.strip()[:120]})
print("gold-free text inside Claude hand-off boxes, by the box's widget type:")
for w, n in by.most_common(25):
    print(f"  {n:5d} blocks {len(pages[w]):4d} pg {len(mods[w]):3d} mod  {w}")
    for e in ex[w][:2]: print("         ", e)
print("position in the box:", dict(pos))
json.dump(ALL, open("_s46_r3_swallow.json", "w"), ensure_ascii=False)
print(len(ALL), "swallowed blocks written to _s46_r3_swallow.json")
