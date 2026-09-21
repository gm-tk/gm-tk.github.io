#!/usr/bin/env python3
"""Session 30 Round 3 PICK — pair every unclassified one-table bundle (_s30_r3_dddump.tsv) with the gold: find the gold page of the
same module whose text contains the table's first data-row cells; the WIDGET class (the nearest widget-marker ancestor) holding the
first cell; tally per (table width, red cells?, url cells?) → gold widget. Output: _s30_r3_ddpair.out"""
import os, sys, re, json, glob
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import HUMAN
from _structural_skeleton import WIDGET_MARKERS
WM = set(WIDGET_MARKERS) | {"flipCardsContainer", "ddContainer", "questionContainer", "table-responsive", "activity"}
HERE = os.path.dirname(os.path.abspath(__file__))

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.texts = []   # (folded text, widget ladder)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        self.stack.append({"tag": tag, "cls": cls, "text": []})
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if tag in ("p", "li", "td", "th", "h3", "h4", "h5", "div", "span", "label", "option"):
                    t = fold("".join(rec["text"]))
                    if t and len(t) < 400:
                        lad = [c for s in self.stack[:i + 1] for c in s["cls"] if c in WM]
                        self.texts.append((t, lad[-1] if lad else "free"))
                del self.stack[i:]; break
    def handle_data(self, d):
        for s in self.stack: s["text"].append(d)

def fold(t): return re.sub(r"[^a-z0-9 ]", "", str(t).lower()).strip()
_cache = {}
def gold_texts(code):
    if code in _cache: return _cache[code]
    out = []
    for f in glob.glob(os.path.join(_corpus.mdir(HUMAN, code), "*.html")):
        p = P(); p.feed(open(f, encoding="utf-8", errors="replace").read()); out += p.texts
    _cache[code] = out; return out

def main():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "_s30_r3_dddump.tsv"), encoding="utf-8") if "\t" in l]
    tally = defaultdict(Counter); mods = defaultdict(lambda: defaultdict(set)); ex = defaultdict(list)
    for r in rows:
        if len(r) < 12: continue
        code, page, typ, dims, red, urls, inv, after, r0, r1, nmem, extra = r[:12]
        w = dims.split("x")[1] if "x" in dims else "?"
        cells = [fold(c) for c in (r1 or r0).split(" | ") if len(fold(c)) >= 4]
        if not cells: tally[(w, "n/a")]["(no textual cell)"] += 1; continue
        gt = gold_texts(code)
        hit = None
        for c in cells[:3]:
            for t, lad in gt:
                if c == t or (len(c) >= 10 and c in t):
                    hit = lad; break
            if hit: break
        key = (w, "red" if int(red) > 0 else "plain", "url" if int(urls) > 0 else "text")
        res = hit or "absent"
        tally[key][res] += 1; mods[key][res].add(code)
        if len(ex[(key, res)]) < 2: ex[(key, res)].append(f"{code} p{page}: «{inv[:30]}» {dims} [{r1[:60]}]")
    L = [f"dragAndDrop one-table bundles: {len(rows)}", "by (width, red?, url?) → the gold widget holding the first data cell (n >= 15):"]
    for k, t in sorted(tally.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(t.values())
        if n < 15: continue
        L.append(f"  {str(k):26s} n={n:4d} " + " ".join(f"{kk}={vv}({len(mods[k][kk])}m)" for kk, vv in t.most_common(6)))
    L.append("examples:")
    for k, v in list(ex.items())[:40]:
        L.append(f"  {k}: " + " | ".join(v))
    txt = "\n".join(L)
    open(os.path.join(HERE, "_s30_r3_ddpair.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:9000])
main()
