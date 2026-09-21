#!/usr/bin/env python3
"""Session 30 Round 2 — the activity box's INNER shape (bare: the h3 / content directly inside the box; row>col: an inner
`div.row > div.col-12` first) by the box's class ladder, gold vs Claude, over every paired page (+ per template / subject
for the alertPadding boxes). Output: _s30_r2_boxinner.out"""
import os, sys, re, json
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE
META = json.load(open("/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data/Module_Structure_Index.json", encoding="utf-8")).get("module_meta", {})

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.boxes = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        rec = {"tag": tag, "cls": cls, "first": None}
        if self.stack and self.stack[-1]["first"] is None and tag not in ("br",):
            self.stack[-1]["first"] = (tag, cls)
        self.stack.append(rec)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if tag == "div" and "activity" in rec["cls"]:
                    self.boxes.append(rec)
                del self.stack[i:]; break

def boxes(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.boxes

def shape(b):
    f = b["first"]
    if not f: return "empty"
    if f[0] == "div" and "row" in f[1]: return "row>col"
    if f[0] in ("h2", "h3", "h4", "h5", "p", "ul", "ol", "img", "table", "a"): return "bare"
    if f[0] == "div": return "div." + ".".join(sorted(f[1]))[:30]
    return f[0]

def main():
    g = defaultdict(Counter); c = defaultdict(Counter); gg = defaultdict(Counter)
    for code in _corpus.gate_mods(CLAUDE):
        pr = pairs(code)
        if not pr: continue
        m = META.get(code, {}); grp = (m.get("template_type") or "?", m.get("subject") or "?")
        for _k, cp, hp in pr:
            for b in boxes(hp):
                key = "alertPadding" if "alertPadding" in b["cls"] else ("interactive" if "interactive" in b["cls"] else "plain")
                g[key][shape(b)] += 1
                if key == "alertPadding": gg[grp][shape(b)] += 1
            for b in boxes(cp):
                key = "alertPadding" if "alertPadding" in b["cls"] else ("interactive" if "interactive" in b["cls"] else "plain")
                c[key][shape(b)] += 1
    L = ["GOLD activity boxes by class kind → inner shape"]
    for k, v in g.items():
        n = sum(v.values()); L.append(f"  {k:14s} n={n:5d}  bare {v['bare']/n:.2f}  row>col {v['row>col']/n:.2f}  {dict(v.most_common(5))}")
    L.append("CLAUDE activity boxes by class kind → inner shape")
    for k, v in c.items():
        n = sum(v.values()); L.append(f"  {k:14s} n={n:5d}  bare {v['bare']/n:.2f}  row>col {v['row>col']/n:.2f}  {dict(v.most_common(5))}")
    L.append("GOLD alertPadding boxes per (template, subject) n >= 10")
    for grp, v in sorted(gg.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(v.values())
        if n < 10: continue
        L.append(f"  {str(grp):55s} n={n:4d} bare {v['bare']/n:.2f} row>col {v['row>col']/n:.2f}")
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r2_boxinner.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)

main()
