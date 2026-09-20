#!/usr/bin/env python3
"""_s29_r6_widgetflow.py — the paired row-break census AFTER A WIDGET, by widget kind (the _s26_rowpair.py direction-B
WIDGET candidate decomposed: 0.63 on 129 pages / 76 modules on the r414 corpus).
For every paired page: Claude's top-level `#body > div.row > div.col-*` columns; X = a direct child that is a widget
(an un-built `cv2-interactive` hand-off box, or a built widget by class) and Y = the NEXT direct child that is a text
element (p / ul / ol / h*) in the SAME column. The gold: the top-level row holding Y's text vs the row holding the last
text of X (the widget's own text — for a hand-off box its dump text; for a built widget its visible text) or, failing
that, the last text before X in the column. Same gold row = the gold FLOWS (Claude right); different = the gold BREAKS
(Claude flowed wrongly). Keys: widget kind × (template, subject).
Run under WSL from CONVERTER_V2/reference/tests:  python3 ../../outputs/_s29_r6_widgetflow.py
"""
import os, re, sys, json, html as H, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.path.abspath(os.path.join(HERE, "..", "..", "01-Claude_Modules_"))
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]
BUILT = ["dragAndDrop", "clickDrop", "flipCardsContainer", "accordion", "carousel", "dropQuiz", "mcqOptions", "speechBubble", "tabs", "hintSlider", "TKmodal", "selfCheck", "shapeHover", "rotateBanner", "wordDrag", "memoryGame", "selectionBox", "reorder", "typing"]
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track", "iframe"}

def fold(t): return re.sub(r"[^a-z0-9]+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t)).lower()).strip()

def tree(html):
    """element tree of #body: nodes {name, cls, kids, start, end, text}"""
    bi = re.search(r'<div[^>]*id="body"[^>]*>', html)
    if not bi: return None
    root = {"name": "body", "cls": "", "kids": [], "start": bi.end(), "end": len(html)}
    stack = [root]
    for m in re.finditer(r"<(/?)(\w+)([^>]*)>", html[bi.end():]):
        close, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        pos = bi.end() + m.start(); pend = bi.end() + m.end()
        if name in VOID and not close:
            stack[-1]["kids"].append({"name": name, "cls": (re.search(r'class="([^"]*)"', attrs) or [None, ""])[1] if 'class=' in attrs else "", "kids": [], "start": pos, "end": pend}); continue
        if close:
            if len(stack) == 1: root["end"] = pos; break
            n = stack.pop(); n["end"] = pos; n["inner_end"] = pos
            continue
        if attrs.rstrip().endswith("/"): continue
        c = re.search(r'class="([^"]*)"', attrs)
        n = {"name": name, "cls": c.group(1) if c else "", "kids": [], "start": pos, "inner_start": pend, "end": None}
        stack[-1]["kids"].append(n); stack.append(n)
    return root

def wkind(n):
    c = n["cls"]
    if n["name"] == "div" and "cv2-interactive" in c: return "handoff"
    for b in BUILT:
        if re.search(r"(^|\s)%s(\s|$)" % re.escape(b), c): return "built:" + b
    return None

def texts_of(html, n):
    return fold(html[n.get("inner_start", n["start"]):n["end"]]) if n.get("end") else ""

def gold_rows(ghtml):
    t = tree(ghtml)
    if not t: return {}
    rowtexts = {}
    ri = 0
    for r in t["kids"]:
        if not (r["name"] == "div" and re.search(r"(^|\s)row(\s|$)", r["cls"])): continue
        ri += 1
        # every text element line (p/li/h*/td) inside the row → row index
        seg = ghtml[r["start"]:r["end"] or len(ghtml)]
        for m in re.finditer(r"<(p|li|h[1-6]|td|th|span)\b[^>]*>([\s\S]*?)</\1>", seg):
            f = fold(m.group(2))[:60]
            if len(f) >= 12 and f not in rowtexts: rowtexts[f] = ri
    return rowtexts

def lookup(rowtexts, f):
    f = f[:60]
    if f in rowtexts: return rowtexts[f]
    return None

mods = _corpus.gate_mods(CLAUDE)
B = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); modsB = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); grp = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        try: c = open(cp, encoding="utf-8").read(); g = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        ct = tree(c)
        if not ct: continue
        grows = gold_rows(g)
        for r in ct["kids"]:
            if not (r["name"] == "div" and re.search(r"(^|\s)row(\s|$)", r["cls"])): continue
            for col in r["kids"]:
                if not (col["name"] == "div" and re.search(r"(^|\s)col", col["cls"])): continue
                kids = [k for k in col["kids"] if k["name"] != "br"]
                for i, x in enumerate(kids[:-1]):
                    wk = wkind(x)
                    if not wk: continue
                    y = kids[i + 1]
                    if y["name"] not in ("p", "ul", "ol") or re.search(r"cv2-(note|comment)", y["cls"]): continue
                    yt = ""
                    m = re.search(r"<(p|li)\b[^>]*>([\s\S]*?)</\1>", c[y["start"]:y["end"] or y["start"] + 2000]) if y["name"] != "p" else None
                    yt = fold(m.group(2)) if m else fold(c[y.get("inner_start", y["start"]):y["end"] or y["start"]])
                    if len(yt) < 12: continue
                    # the widget's last text: the last p/li/td/h inside X; else the last text before X in the column
                    xseg = c[x["start"]:x["end"] or x["start"]]
                    xts = [fold(mm2.group(2)) for mm2 in re.finditer(r"<(p|li|h[1-6]|td|th)\b[^>]*>([\s\S]*?)</\1>", xseg)]
                    xts = [z for z in xts if len(z) >= 12 and "interactive un built" not in z and "writers note" not in z and "red flag" not in z]
                    xt = xts[-1] if xts else None
                    if xt is None:
                        for k in reversed(kids[:i]):
                            zz = [fold(mm2.group(2)) for mm2 in re.finditer(r"<(p|li|h[1-6]|td|th)\b[^>]*>([\s\S]*?)</\1>", c[k["start"]:k["end"] or k["start"]])]
                            zz = [z for z in zz if len(z) >= 12]
                            if zz: xt = zz[-1]; break
                    gy = lookup(grows, yt); gx = lookup(grows, xt) if xt else None
                    if gy is None or gx is None: v = "gold-nowhere"
                    elif gy == gx: v = "gold-flows"
                    else: v = "GOLD-BREAKS"
                    for key in ((wk, "ALL", ""), (wk,) + grp, ("ANY",) + grp, ("ANY", "ALL", "")):
                        B[key][v] += 1
                    if v == "GOLD-BREAKS":
                        pages[wk].add(cp); modsB[wk].add(code); pages["ANY"].add(cp); modsB["ANY"].add(code)
                        if len(ex[wk]) < 3: ex[wk].append("%s Y=«%s»" % (os.path.basename(cp), yt[:40]))
print("after-WIDGET boundaries (Claude flows the next text into the same column) — does the gold BREAK?")
for key, cnt in sorted(B.items(), key=lambda x: (x[0][0] != "ANY", x[0][0], -(x[1]["GOLD-BREAKS"] + x[1]["gold-flows"]))):
    n = cnt["GOLD-BREAKS"] + cnt["gold-flows"]
    if n < 5: continue
    print("  %-22s %-13s %-26s breaks %3d / flows %3d = %.2f  [nowhere %d]%s" % (key[0], key[1], key[2][:26], cnt["GOLD-BREAKS"], cnt["gold-flows"], cnt["GOLD-BREAKS"] / n, cnt["gold-nowhere"],
          ("  pages %d / mods %d" % (len(pages[key[0]]), len(modsB[key[0]]))) if key[1] == "ALL" else ""))
for k, v in ex.items(): print("  e.g. %s: %s" % (k, " | ".join(v)))
