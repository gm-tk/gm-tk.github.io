#!/usr/bin/env python3
"""Session 30 Round 2 PICK census — `div.alert.solid`: Claude 496 vs gold 241 on the same pages (the s29-r10 label census).
For every paired page: each Claude `div.alert.solid` box → its lead text → the gold box on the same page holding that text
(matched by the first 40 folded chars of the box text, or any 60-char substring) → the gold box's class ladder.
Also the writer source per module from the parsed WT: counts of `[important…]` vs `[alert solid…]` vs `[alert…]` tags.
Output: _s30_r2_alertsolid.out"""
import os, sys, re, glob
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE
BOX_CLS = {"alert", "wananga", "whakatauki", "quoteText", "alertActivity", "activity", "supervisor", "super-content", "learningSupport", "cultural"}

class P(HTMLParser):
    """collect every div with a class containing 'alert' (or any box class) with its text"""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.boxes = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        if tag in ("script", "style"): self.skip += 1
        rec = {"tag": tag, "cls": cls, "text": [], "depth": len(self.stack)}
        self.stack.append(rec)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if rec["tag"] == "div" and (set(rec["cls"]) & BOX_CLS):
                    rec["ftext"] = re.sub(r"\s+", " ", "".join(rec["text"])).strip().lower()
                    # the box's ancestor chain of box classes
                    rec["anc"] = [" ".join(s["cls"]) for s in self.stack[:i] if s["tag"] == "div" and (set(s["cls"]) & BOX_CLS)]
                    self.boxes.append(rec)
                del self.stack[i:]
                break
        if tag in ("script", "style") and self.skip: self.skip -= 1
    def handle_data(self, d):
        if self.skip: return
        for r in self.stack: r["text"].append(d)

def parse(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.boxes

def wt_counts(code):
    d = _corpus.mdir(HUMAN, code); c = Counter()
    for f in glob.glob(os.path.join(d, "*_parsed.txt")):
        s = open(f, encoding="utf-8", errors="replace").read().lower()
        c["important"] += len(re.findall(r"\[\s*important", s))
        c["alert solid"] += len(re.findall(r"\[\s*alert\s+(?:box\s+)?solid", s))
        c["alert other"] += len(re.findall(r"\[\s*alert\b", s)) - c["alert solid"]
    return c

def main():
    tot = Counter(); per_mod = {}; examples = defaultdict(list)
    bygroup = defaultdict(Counter)
    for code in _corpus.gate_mods(CLAUDE):
        pr = pairs(code)
        if not pr: continue
        mc = Counter(); wt = None
        for _k, cp, hp in pr:
            cb = [b for b in parse(cp) if "alert" in b["cls"] and "solid" in b["cls"]]
            if not cb: continue
            gb = parse(hp)
            for b in cb:
                key = b["ftext"][:40]
                if len(key) < 12:
                    mc["cl_short"] += 1; continue
                hit = None
                for g in gb:
                    if key and key in g["ftext"] and abs(len(g["ftext"]) - len(b["ftext"])) < max(200, len(b["ftext"])):
                        hit = g; break
                if hit is None:
                    # any 60-char substring of the claude text
                    t = b["ftext"]
                    for off in range(0, max(1, len(t) - 60), 40):
                        sub = t[off:off + 60]
                        if len(sub) < 40: break
                        for g in gb:
                            if sub in g["ftext"]:
                                hit = g; break
                        if hit: break
                if hit is None:
                    mc["absent"] += 1; continue
                gcls = " ".join(sorted(hit["cls"]))
                mc[gcls] += 1
                if len(examples[gcls]) < 4:
                    examples[gcls].append(f"{code} {os.path.basename(cp)}: «{b['ftext'][:70]}»")
        if mc:
            wt = wt_counts(code)
            per_mod[code] = (mc, wt)
            tot.update(mc)
    L = ["SESSION 30 ROUND 2 — div.alert.solid on Claude's paired pages → the gold box's class for the same text",
         f"TOTAL Claude alert-solid boxes matched: {sum(v for k, v in tot.items() if k not in ('absent', 'cl_short'))}; absent (text not in the gold page) {tot['absent']}; short-text skipped {tot['cl_short']}",
         "gold class ladder for the matched boxes:"]
    for k, v in tot.most_common():
        if k in ("absent", "cl_short"): continue
        L.append(f"  {v:5d}  {k}")
    L.append("")
    L.append("per module: gold classes | WT tag counts (important / alert solid / alert other)")
    for code, (mc, wt) in sorted(per_mod.items(), key=lambda kv: -sum(kv[1][0].values())):
        L.append(f"  {code:9s} {dict(mc)} | WT important {wt['important']} / alert solid {wt['alert solid']} / alert other {wt['alert other']}")
    L.append("")
    L.append("examples:")
    for k, ex in examples.items():
        L.append(f"  [{k}]")
        for e in ex: L.append("    " + e)
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r2_alertsolid.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:7000])

main()
