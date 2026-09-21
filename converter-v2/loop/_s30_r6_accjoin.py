#!/usr/bin/env python3
"""Session 30 Round 6 PICK — the accordion + one-table bundles (_s30_r6_accdump.tsv) joined to the DISK truth (un-built boxes vs
built accordions on the bundle's page) and, for the un-built pages, the table shape + the gold's widget for the first data cell."""
import re, os, glob, sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
sys.path.insert(0, "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests")
import _corpus
from anchor_compare import CLAUDE
from _discrepancy_audit import HUMAN
HERE = os.path.dirname(os.path.abspath(__file__))
TYP = sys.argv[1] if len(sys.argv) > 1 else "accordion"
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, f"_s30_r6_{TYP[:3]}dump.tsv"), encoding="utf-8") if "\t" in l]

def page_state(code, page):
    f = os.path.join(_corpus.mdir(CLAUDE, code), code + "_" + page.replace(".", "_") + ".html")
    if not os.path.exists(f): return None
    s = open(f, encoding="utf-8", errors="replace").read()
    return len(re.findall(r"INTERACTIVE \(un-built\) #\d+: " + TYP + r"\b", s)), len(re.findall(r'class="' + TYP + r'[ "]', s))

def fold(t): return re.sub(r"[^a-z0-9 ]", "", str(t).lower()).strip()
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.texts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); self.stack.append({"tag": tag, "cls": (a.get("class") or "").split(), "text": []})
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if tag in ("p", "li", "td", "th", "h3", "h4", "h5", "div", "span"):
                    t = fold("".join(rec["text"]))
                    if t and len(t) < 300:
                        w = next((c for s in reversed(self.stack[:i + 1]) for c in s["cls"] if c in ("accordion", "tabs", "flipCard", "carousel", "clickDrop", "table-responsive", "multiChoiceQuiz", "dragAndDrop", "modal", "TKmodal", "cv2-interactive", "alert", "activity")), None)
                        self.texts.append((t, w))
                del self.stack[i:]; break
    def handle_data(self, d):
        for s in self.stack: s["text"].append(d)
_gc = {}
def gold_texts(code):
    if code in _gc: return _gc[code]
    out = []
    for f in glob.glob(os.path.join(_corpus.mdir(HUMAN, code), "*.html")):
        p = P(); p.feed(open(f, encoding="utf-8", errors="replace").read()); out += p.texts
    _gc[code] = out; return out

c = Counter(); gold = Counter(); ex = []; mods = set()
for r in rows:
    if len(r) < 16 or int(r[10]) > 2: continue
    st = page_state(r[0], r[1])
    if st is None: continue
    nb, built = st
    state = "unbuilt-page" if nb and not built else ("built-page" if built and not nb else "mixed-page")
    key = (state, r[3].split("x")[1] + "col", "red" if int(r[4]) > 0 else "plain", "url" if int(r[5]) > 0 else "text")
    c[key] += 1
    if state == "unbuilt-page":
        mods.add(r[0])
        cells = [fold(x) for x in r[9].split(" | ") if len(fold(x)) >= 6]
        hit = "absent"
        for cell in cells[:2]:
            for t, w in gold_texts(r[0]):
                if cell == t or (len(cell) >= 12 and cell in t): hit = w or "free"; break
            if hit != "absent": break
        gold[(key[1], hit)] += 1
        if len(ex) < 16: ex.append(f"{r[0]} p{r[1]} {r[3]} red={r[4]} → gold {hit}  [{r[8][:60]}] [{r[9][:55]}]")
print(TYP, "+ one table bundles:", sum(c.values()))
for k, v in c.most_common(14): print(f"  {v:4d} {k}")
print("un-built pages: modules", len(mods))
print("gold widget for the un-built (width, widget):", gold.most_common(12))
print("\n".join(ex))
