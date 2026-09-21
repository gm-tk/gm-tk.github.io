#!/usr/bin/env python3
"""Session 30 Round 3 PICK — BOLD INSIDE A TABLE HEADER CELL: for every Claude `<th>` whose text is wholly / partly inside <b>,
the gold's same-text cell (matched by folded text among the gold's th / td) — is it a `th` with <b>, a `th` without, a `td` with /
without? Per (template, subject) and per table kind (Claude's table class). Excludes cells whose text is absent from the gold page.
Also the reverse: gold th cells with <b> whose Claude cell has none. Output: _s30_r3_thbold.out"""
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
        self.stack = []; self.cells = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        self.stack.append({"tag": tag, "cls": cls, "text": [], "btext": [], "inb": 0})
        if tag in ("b", "strong"):
            for s in self.stack: s["inb"] += 1
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if tag in ("b", "strong"):
                    for s in self.stack[:i]: s["inb"] -= 1
                if tag in ("th", "td"):
                    txt = re.sub(r"\s+", " ", "".join(rec["text"])).strip()
                    bt = re.sub(r"\s+", " ", "".join(rec["btext"])).strip()
                    tcls = next((" ".join(s["cls"]) for s in reversed(self.stack[:i]) if s["tag"] == "table"), "")
                    inwidget = any(c in ("cv2-interactive", "dragAndDrop", "flipCard", "carousel", "accordion", "tabs", "clickDrop", "typing", "dropQuiz", "multiChoiceQuiz") for s in self.stack[:i] for c in s["cls"])
                    if txt: self.cells.append({"tag": tag, "text": txt, "bold": "whole" if bt and bt == txt else ("part" if bt else "none"), "tcls": tcls, "widget": inwidget})
                del self.stack[i:]; break
    def handle_data(self, d):
        for s in self.stack:
            s["text"].append(d)
            if s["inb"]: s["btext"].append(d)

def parse(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.cells
def fold(t): return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()

def main():
    res = Counter(); grp = defaultdict(Counter); kind = defaultdict(Counter); pages = set(); mods = set(); rev = Counter(); ex = []
    for code in _corpus.gate_mods(CLAUDE):
        pr = pairs(code)
        if not pr: continue
        m = META.get(code, {}); g = (m.get("template_type") or "?", m.get("subject") or "?")
        for _k, cp, hp in pr:
            cc = [c for c in parse(cp) if not c["widget"]]; hc = [c for c in parse(hp) if not c["widget"]]
            hidx = defaultdict(list)
            for c in hc: hidx[fold(c["text"])].append(c)
            for c in cc:
                if c["tag"] != "th" or c["bold"] == "none": continue
                f = fold(c["text"])
                if len(f) < 2 or not hidx.get(f): res["absent"] += 1; continue
                h = hidx[f][0]
                r = f"{h['tag']}:{h['bold']}"
                res[r] += 1; grp[g][r] += 1; kind[c["bold"]][r] += 1; pages.add(cp); mods.add(code)
                if r == "th:none" and len(ex) < 8: ex.append(f"{code} {os.path.basename(cp)}: «{c['text'][:40]}»")
            cidx = defaultdict(list)
            for c in cc: cidx[fold(c["text"])].append(c)
            for h in hc:
                if h["tag"] == "th" and h["bold"] != "none":
                    f = fold(h["text"]); cm = cidx.get(f)
                    if cm and cm[0]["bold"] == "none": rev[cm[0]["tag"]] += 1
    n = sum(v for k, v in res.items() if k != "absent")
    L = [f"Claude <th> cells with bold, matched on the gold page: {n} (absent {res['absent']}) on {len(pages)} pages / {len(mods)} modules"]
    for k, v in res.most_common(): L.append(f"  {v:5d} {v/max(1,n):.2f} {k}")
    L.append("by Claude's bold kind:")
    for k, t in kind.items():
        nn = sum(t.values()); L.append(f"  {k:6s} n={nn:5d} " + " ".join(f"{kk} {vv/nn:.2f}" for kk, vv in t.most_common()))
    L.append("by (template, subject) n >= 20 — th:none share (the gold drops the bold in a header cell):")
    for k, t in sorted(grp.items(), key=lambda kv: -sum(kv[1].values())):
        nn = sum(t.values())
        if nn < 20: continue
        L.append(f"  {str(k):52s} n={nn:5d} th:none {t['th:none']/nn:.2f} th:whole {t['th:whole']/nn:.2f} th:part {t['th:part']/nn:.2f} td:* {(t['td:none']+t['td:whole']+t['td:part'])/nn:.2f}")
    L.append("REVERSE — gold th with bold where Claude's same cell has none: " + str(dict(rev)))
    L.append("examples (th:none): " + " | ".join(ex))
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r3_thbold.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)
main()
