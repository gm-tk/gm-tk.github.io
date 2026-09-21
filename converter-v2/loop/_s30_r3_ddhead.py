#!/usr/bin/env python3
"""Session 30 Round 3 PICK — the 2-column dragAndDrop tables whose only red is the HEADER row (the r69 text form bails on any
red): for each such bundle (from _s30_r3_dddump.tsv) find the gold widget holding a data cell → the gold's dragAndDrop `layout`
attribute (standard = matching pairs / column = category sort / other) or the non-D&D widget, per site. Output: _s30_r3_ddhead.out"""
import os, sys, re, glob
from collections import Counter
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import HUMAN
HERE = os.path.dirname(os.path.abspath(__file__))
def fold(t): return re.sub(r"[^a-z0-9 ]", "", str(t).lower()).strip()

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.texts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        self.stack.append({"tag": tag, "cls": cls, "text": [], "layout": a.get("layout")})
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if tag in ("p", "li", "td", "th", "div", "span", "h4", "h5"):
                    t = fold("".join(rec["text"]))
                    if t and len(t) < 300:
                        w = next(((c, s["layout"]) for s in reversed(self.stack[:i + 1]) for c in s["cls"] if c in ("dragAndDrop", "flipCard", "multiChoiceQuiz", "dropQuiz", "accordion", "tabs", "carousel", "radioQuiz", "reorder", "memoryGame", "typing", "wordSelect", "table-responsive", "cv2-interactive", "clickDrop", "dropDown", "speechBubble")), None)
                        self.texts.append((t, w))
                del self.stack[i:]; break
    def handle_data(self, d):
        for s in self.stack: s["text"].append(d)

def main():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "_s30_r3_dddump.tsv"), encoding="utf-8") if "\t" in l]
    sel = [r for r in rows if len(r) >= 16 and r[3].endswith("x2") and r[12] == "0" and int(r[5]) == 0 and r[14] == "distinct" and int(r[15]) >= 2]
    L = [f"2-column dragAndDrop tables with a red HEADER row only: {len(sel)} sites / {len({r[0] for r in sel})} modules"]
    tally = Counter()
    for r in sel:
        code = r[0]; cells = [fold(c) for c in r[9].split(" | ") if len(fold(c)) >= 3]
        gt = []
        for f in glob.glob(os.path.join(_corpus.mdir(HUMAN, code), "*.html")):
            p = P(); p.feed(open(f, encoding="utf-8", errors="replace").read()); gt += p.texts
        hit = None
        for c in cells[:2]:
            for t, w in gt:
                if c == t or (len(c) >= 10 and c in t): hit = w; break
            if hit: break
        res = "absent" if hit is None else (f"{hit[0]}[{hit[1]}]" if hit[0] == "dragAndDrop" else hit[0])
        tally[res] += 1
        L.append(f"  {code:9s} p{r[1]:6s} {r[3]:5s} m{r[10]:2s} → {res:24s} hdr[{r[8][:50]}] row1[{r[9][:50]}]")
    L.insert(1, "  gold: " + str(tally.most_common()))
    txt = "\n".join(L)
    open(os.path.join(HERE, "_s30_r3_ddhead.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)
main()
