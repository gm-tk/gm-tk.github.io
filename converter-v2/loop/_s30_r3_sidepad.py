#!/usr/bin/env python3
"""Session 30 Round 3 PICK — THE TWO-COLUMN ROW'S PADDING CLASSES: for every `div.row` on every paired page that holds a
main column (col-md-8 / col-md-9 / col-md-7 …) AND a side column (col-md-4 / col-md-3 …), the padding tokens on each
(paddingR / paddingL), gold vs Claude, per (template, subject) and by the side column's content kind (alert / alertActivity /
img / alertImage / video / other). Output: _s30_r3_sidepad.out"""
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
        self.stack = []; self.rows = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        rec = {"tag": tag, "cls": cls, "cols": [], "first": None}
        if tag == "div" and self.stack:
            par = self.stack[-1]
            if par["tag"] == "div" and "row" in par["cls"] and any(c.startswith("col-") for c in cls):
                par["cols"].append({"cls": cls, "first": None})
            # the side column's first child kind
            for s in reversed(self.stack):
                if s["tag"] == "div" and any(c.startswith("col-") for c in s["cls"]):
                    break
        for s in reversed(self.stack):
            if s["tag"] == "div" and "row" in s["cls"] and s["cols"] and s["cols"][-1]["first"] is None and self.stack[-1] is not s:
                # first child of the latest column
                col = s["cols"][-1]
                if self.stack[-1]["tag"] == "div" and any(c.startswith("col-") for c in self.stack[-1]["cls"]):
                    col["first"] = tag + ("." + ".".join(sorted(cls)) if cls else "")
            break
        self.stack.append(rec)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if tag == "div" and "row" in rec["cls"] and len(rec["cols"]) == 2:
                    self.rows.append(rec["cols"])
                del self.stack[i:]; break

def kind(col):
    f = col["first"] or ""
    if "alertImage" in f: return "alertImage"
    if "alertActivity" in f: return "alertActivity"
    if f.startswith("div.alert"): return "alert"
    if f.startswith("img"): return "img"
    if "video" in f or "ratio" in f: return "video"
    if "audio" in f: return "audio"
    return f[:24] or "?"

def rows(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.rows

def main():
    g = Counter(); c = Counter(); gk = defaultdict(Counter); ck = defaultdict(Counter); gg = defaultdict(Counter); cg = defaultdict(Counter)
    for code in _corpus.gate_mods(CLAUDE):
        pr = pairs(code)
        if not pr: continue
        m = META.get(code, {}); grp = (m.get("template_type") or "?", m.get("subject") or "?")
        for _k, cp, hp in pr:
            for side, tally, byk, byg in ((hp, g, gk, gg), (cp, c, ck, cg)):
                for cols in rows(side):
                    a, b = cols
                    wa = next((x for x in a["cls"] if re.match(r"col-md-\d+$", x)), None); wb = next((x for x in b["cls"] if re.match(r"col-md-\d+$", x)), None)
                    if not wa or not wb: continue
                    na, nb = int(wa.split("-")[-1]), int(wb.split("-")[-1])
                    if na + nb != 12 or na == nb: continue
                    main_, side_ = (a, b) if na > nb else (b, a)
                    order = "main-first" if na > nb else "side-first"
                    pm = "paddingR" in main_["cls"] or "paddingL" in main_["cls"]
                    ps = "paddingR" in side_["cls"] or "paddingL" in side_["cls"]
                    key = (order, "main+pad" if pm else "main-plain", "side+pad" if ps else "side-plain")
                    tally[key] += 1
                    byk[kind(side_)][key] += 1
                    byg[grp][key] += 1
    L = ["TWO-COLUMN ROWS (a main + a side column, widths summing to 12) — padding tokens, gold vs Claude"]
    for lab, t in (("GOLD", g), ("CLAUDE", c)):
        n = sum(t.values()); L.append(f"{lab} rows {n}")
        for k, v in t.most_common(): L.append(f"   {v:5d} {v/max(1,n):.2f}  {k}")
    L.append("GOLD by the side column's content kind (n >= 20): main+pad share")
    for k, t in sorted(gk.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(t.values())
        if n < 20: continue
        mp = sum(v for kk, v in t.items() if kk[1] == "main+pad"); sp = sum(v for kk, v in t.items() if kk[2] == "side+pad")
        cn = sum(ck.get(k, Counter()).values()); cmp_ = sum(v for kk, v in ck.get(k, Counter()).items() if kk[1] == "main+pad")
        L.append(f"   {k:26s} gold n={n:4d} main+pad {mp/n:.2f} side+pad {sp/n:.2f} | claude n={cn:4d} main+pad {(cmp_/cn if cn else 0):.2f}")
    L.append("GOLD by (template, subject) (n >= 20): main+pad share | Claude")
    for k, t in sorted(gg.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(t.values())
        if n < 20: continue
        mp = sum(v for kk, v in t.items() if kk[1] == "main+pad")
        cn = sum(cg.get(k, Counter()).values()); cmp_ = sum(v for kk, v in cg.get(k, Counter()).items() if kk[1] == "main+pad")
        L.append(f"   {str(k):52s} gold n={n:4d} main+pad {mp/n:.2f} | claude n={cn:4d} main+pad {(cmp_/cn if cn else 0):.2f}")
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r3_sidepad.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:7000])
main()
