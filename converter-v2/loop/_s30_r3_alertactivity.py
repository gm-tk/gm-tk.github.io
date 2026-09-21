#!/usr/bin/env python3
"""Session 30 Round 3 PICK — THE GOLD'S `div.alertActivity` (gold 505 / Claude 135 on the label census): for every gold
alertActivity box on a paired page, its lead text → Claude's container holding that text (alert solid / alert / alertActivity /
activity / none / absent), per (template, subject) and per module prefix; plus the gold box's column (a side col-md-4? full?).
Output: _s30_r3_alertactivity.out"""
import os, sys, re, json
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE
META = json.load(open("/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data/Module_Structure_Index.json", encoding="utf-8")).get("module_meta", {})
BOX = {"alert", "alertActivity", "activity", "supervisor", "super-content", "whakatauki", "wananga", "cv2-interactive", "alertImage"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.boxes = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        self.stack.append({"tag": tag, "cls": cls, "text": []})
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if tag == "div" and (set(rec["cls"]) & BOX):
                    col = next((" ".join(sorted(c for c in s["cls"] if c.startswith("col-") or c.startswith("offset"))) for s in reversed(self.stack[:i]) if s["tag"] == "div" and any(c.startswith("col-") for c in s["cls"])), "(none)")
                    self.boxes.append({"cls": " ".join(sorted(set(rec["cls"]) & BOX | (set(rec["cls"]) & {"solid", "top", "blank"}))), "text": re.sub(r"\s+", " ", "".join(rec["text"])).strip().lower(), "col": col})
                del self.stack[i:]; break
    def handle_data(self, d):
        for s in self.stack: s["text"].append(d)

def parse(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.boxes

def main():
    res = Counter(); grp = defaultdict(Counter); pref = defaultdict(Counter); cols = Counter(); ex = defaultdict(list)
    for code in _corpus.gate_mods(CLAUDE):
        pr = pairs(code)
        if not pr: continue
        m = META.get(code, {}); g = (m.get("template_type") or "?", m.get("subject") or "?")
        pf = re.match(r"[A-Z]+", code).group(0) if re.match(r"[A-Z]+", code) else code
        for _k, cp, hp in pr:
            gb = [b for b in parse(hp) if "alertActivity" in b["cls"]]
            if not gb: continue
            cb = parse(cp); ctxt = open(cp, encoding="utf-8", errors="replace").read().lower()
            for b in gb:
                key = b["text"][:40]
                cols[b["col"]] += 1
                if len(key) < 10: res["short"] += 1; continue
                hit = next((c for c in cb if key in c["text"]), None)
                if hit: r = "claude:" + hit["cls"]
                elif re.sub(r"\s+", " ", key) in re.sub(r"\s+", " ", ctxt): r = "claude:free-text"
                else: r = "absent"
                res[r] += 1; grp[g][r] += 1; pref[pf][r] += 1
                if len(ex[r]) < 4: ex[r].append(f"{code} {os.path.basename(cp)}: «{b['text'][:60]}»")
    n = sum(res.values())
    L = [f"GOLD alertActivity boxes on the paired pages: {n}", "  " + str(res.most_common())]
    L.append("  gold column: " + str(cols.most_common(6)))
    L.append("by prefix (n >= 10):")
    for k, t in sorted(pref.items(), key=lambda kv: -sum(kv[1].values())):
        nn = sum(t.values())
        if nn < 10: continue
        L.append(f"  {k:8s} n={nn:4d} " + " ".join(f"{kk}={vv/nn:.2f}" for kk, vv in t.most_common(4)))
    L.append("by (template, subject) (n >= 15):")
    for k, t in sorted(grp.items(), key=lambda kv: -sum(kv[1].values())):
        nn = sum(t.values())
        if nn < 15: continue
        L.append(f"  {str(k):52s} n={nn:4d} " + " ".join(f"{kk}={vv/nn:.2f}" for kk, vv in t.most_common(4)))
    L.append("examples:")
    for k, v in ex.items(): L.append(f"  [{k}] " + " | ".join(v))
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r3_alertactivity.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:6000])
main()
