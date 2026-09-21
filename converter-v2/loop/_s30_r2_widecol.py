#!/usr/bin/env python3
"""Session 30 Round 2 PICK census — THE WIDENED ACTIVITY WRAPPER PER BUILT WIDGET LAYOUT (D10-3's open item; KB c17 / c56:
`col-md-12 col-12` for wide interactives). For every `div.activity…` box on every paired page (gold and Claude): the OUTER column
class (the nearest ancestor div.col-*), the box's classes, and the WIDGET TYPE inside (the first descendant carrying a widget
marker class; `cv2-interactive` = an un-built hand-off box on Claude's side). Gold: share of `col-md-12` per widget type and per
(template, subject). Claude: the same for its BUILT widgets. Output: _s30_r2_widecol.out"""
import os, sys, re, json
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE
from _structural_skeleton import WIDGET_MARKERS
WM = set(WIDGET_MARKERS) | {"cv2-interactive", "flipCardsContainer", "ddContainer", "questionContainer"}
META = json.load(open("/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data/Module_Structure_Index.json", encoding="utf-8"))
mm = META.get("module_meta", {})
def grp(code):
    m = mm.get(code, {})
    return (m.get("template_type") or "?", m.get("subject") or "?")

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.boxes = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        rec = {"tag": tag, "cls": cls, "widget": None, "isbox": tag == "div" and "activity" in cls, "col": None}
        if rec["isbox"]:
            for s in reversed(self.stack):
                if s["tag"] == "div" and any(c.startswith("col-") for c in s["cls"]):
                    rec["col"] = " ".join(sorted(c for c in s["cls"] if c.startswith("col-") or c.startswith("offset-"))); break
        w = set(cls) & WM
        if w:
            wname = sorted(w)[0]
            if "cv2-interactive" in w: wname = "UNBUILT"
            for s in reversed(self.stack):
                if s["isbox"] and s["widget"] is None:
                    s["widget"] = wname; break
        self.stack.append(rec)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if rec["isbox"]: self.boxes.append(rec)
                del self.stack[i:]; break

def boxes(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.boxes

def main():
    g_type = defaultdict(Counter); c_type = defaultdict(Counter)
    g_grp = defaultdict(Counter); c_grp = defaultdict(Counter)
    g_cls = defaultdict(Counter)
    for code in _corpus.gate_mods(CLAUDE):
        pr = pairs(code)
        if not pr: continue
        tg = grp(code)
        for _k, cp, hp in pr:
            for b in boxes(hp):
                w = b["widget"] or ("interactive-noWidget" if "interactive" in b["cls"] else "none")
                col = b["col"] or "(none)"
                g_type[w][col] += 1
                if w not in ("none",): g_grp[(w, tg)][col] += 1
                g_cls[w][" ".join(sorted(b["cls"]))] += 1
            for b in boxes(cp):
                w = b["widget"] or ("interactive-noWidget" if "interactive" in b["cls"] else "none")
                col = b["col"] or "(none)"
                c_type[w][col] += 1
                if w not in ("none",): c_grp[(w, tg)][col] += 1
    L = ["SESSION 30 ROUND 2 — the activity box's OUTER column by the widget type inside (paired pages)", "",
         "GOLD — per widget type: boxes | col-md-12 share | column ladder"]
    for w, c in sorted(g_type.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(c.values()); wide = sum(v for k, v in c.items() if "col-md-12" in k)
        L.append(f"  {w:24s} n={n:5d}  wide={wide/n:.2f}  {dict(c.most_common(5))}")
    L.append(""); L.append("CLAUDE — per widget type: boxes | col-md-12 share | column ladder")
    for w, c in sorted(c_type.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(c.values()); wide = sum(v for k, v in c.items() if "col-md-12" in k)
        L.append(f"  {w:24s} n={n:5d}  wide={wide/n:.2f}  {dict(c.most_common(5))}")
    L.append(""); L.append("GOLD — per (widget type, template, subject) with n >= 10: wide share")
    for (w, tg), c in sorted(g_grp.items(), key=lambda kv: (kv[0][0], -sum(kv[1].values()))):
        n = sum(c.values())
        if n < 10: continue
        wide = sum(v for k, v in c.items() if "col-md-12" in k)
        cc = c_grp.get((w, tg), Counter()); cn = sum(cc.values()); cw = sum(v for k, v in cc.items() if "col-md-12" in k)
        L.append(f"  {w:20s} {str(tg):50s} gold n={n:4d} wide={wide/n:.2f} | claude n={cn:4d} wide={(cw/cn if cn else 0):.2f}")
    L.append(""); L.append("GOLD — box class ladder per widget type (top 3)")
    for w, c in sorted(g_cls.items(), key=lambda kv: -sum(kv[1].values()))[:14]:
        L.append(f"  {w:24s} {dict(c.most_common(3))}")
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r2_widecol.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:9000])

main()
