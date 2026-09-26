#!/usr/bin/env python3
"""_s52_r12_actbox.py — session 52 Round 12: THE UNBOXED ACTIVITY. Every gold activity box (div.activity…) on a paired page: where
does Claude put its blocks (matched by text) — in ONE Claude activity box, split over several, or FREE (no activity box)? A gold box
whose matched blocks are all free in Claude is an unboxed activity; reported with its first block, the gold box's number= / class,
per family. Own parser (the jtail one). WSL, from reference/tests/:  python3 ../../outputs/_s52_r12_actbox.py"""
import os, re, sys, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import compare_structure as CS
import _corpus
norm = lambda s: re.sub(r"[^a-z0-9āēīōū ]", "", re.sub(r"\s+", " ", s).strip().lower())
BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.recs = []; self.cur = None; self.box = 0; self.meta = {}; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("img", "br", "hr", "input", "source", "meta", "link"): return
        a = dict(attrs); cls = (a.get("class") or "").split()
        bid = None
        if tag == "div" and "activity" in cls: self.box += 1; bid = self.box; self.meta[bid] = (" ".join(cls), a.get("number") or "")
        hand = tag == "div" and any(c.startswith("cv2-interactive") for c in cls)
        self.stack.append((tag, bid, hand))
        if tag in BLOCK and self.cur is None: self.recs.append({"box": self.inbox(), "t": [], "hand": any(h for _, _, h in self.stack)}); self.cur = self.recs[-1]
    def inbox(self):
        for tag, bid, hand in reversed(self.stack):
            if bid: return bid
        return None
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                if self.cur is not None and tag in BLOCK: self.cur = None
                break
    def handle_data(self, d):
        if self.cur is not None: self.cur["t"].append(d)
def parse(path):
    p = P()
    try: p.feed(open(path, encoding="utf-8", errors="replace").read()); p.close()
    except Exception: pass
    out = [(r["box"], norm("".join(r["t"])), r["hand"]) for r in p.recs]
    return [x for x in out if len(x[1]) >= 12], p.meta
st = collections.Counter(); fam = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); ex = collections.defaultdict(list); gcls = collections.defaultdict(collections.Counter)
for mod in sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m))):
    for n, cp, hp in pairs(mod):
        c, _ = parse(cp); h, hm = parse(hp)
        cidx = {}
        for box, t, hand in c: cidx.setdefault(t[:60], (box, hand))
        byb = collections.defaultdict(list)
        for box, t, hand in h:
            if box: byb[box].append(t)
        for b, ts in byb.items():
            hits = [cidx[t[:60]] for t in ts if t[:60] in cidx]
            if not hits: k = "gold box: no text matched"
            else:
                boxes = {x[0] for x in hits if x[0]}; free = [x for x in hits if not x[0] and not x[1]]; inhand = [x for x in hits if not x[0] and x[1]]
                if len(free) == len(hits): k = "UNBOXED (all matched blocks free)"
                elif inhand and len(inhand) == len(hits): k = "in a hand-off box"
                elif len(boxes) == 1 and not free: k = "one Claude box"
                elif len(boxes) > 1: k = "split over boxes"
                else: k = "partly boxed"
            st[k] += 1; fam[k][re.sub(r"\d.*$", "", mod)] += 1; pages[k].add(cp); gcls[k][hm.get(b, ("", ""))[0]] += 1
            if k.startswith("UNBOXED") and len(ex[k]) < 8: ex[k].append(f"{os.path.basename(cp)} [{hm.get(b, ('', ''))[0]} n={hm.get(b, ('', ''))[1]}] {ts[0][:60]!r}")
for k, n in st.most_common():
    print(f"{n:5d} boxes / {len(pages[k]):4d} pages  {k}   fams: {', '.join(f'{a} {b}' for a, b in fam[k].most_common(8))}")
    if k.startswith("UNBOXED"):
        print("      gold classes:", gcls[k].most_common(6))
        for x in ex[k]: print("      e.g.", x)
