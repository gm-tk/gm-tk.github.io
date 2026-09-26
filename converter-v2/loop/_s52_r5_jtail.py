#!/usr/bin/env python3
"""_s52_r5_jtail.py — session 52 Round 5: THE JOURNAL BUTTON ENDS THE ACTIVITY? For every Claude activity box that holds a
journal element (h4.goJournal, or a button whose text names the journal) with content AFTER it inside the same box — where
does the gold put that tail content: inside an activity box, or outside (the button ended the box)? And the gold's own
boxes: is the journal element the box's last block? Per family. Own parser (block records in document order, each with
its enclosing activity-box instance). WSL, from reference/tests/:  python3 ../../outputs/_s52_r5_jtail.py"""
import os, re, sys, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
famof = lambda m: re.sub(r"\d.*$", "", m)
norm = lambda s: re.sub(r"[^a-z0-9āēīōū ]", "", re.sub(r"\s+", " ", s).strip().lower())
BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td"}
VOID = {"img", "br", "hr", "input", "source", "meta", "link"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.recs = []; self.cur = None; self.box = 0; self.btn = False
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        a = dict(attrs); cls = (a.get("class") or "").split()
        bid = None
        if tag == "div" and "activity" in cls: self.box += 1; bid = self.box
        self.stack.append((tag, bid, cls))
        if tag == "div" and "button" in cls: self.btn = True; self.recs.append({"tag": "button", "box": self.inbox(), "t": [], "cls": cls}); self.cur = self.recs[-1]
        elif tag in BLOCK and self.cur is None:
            self.recs.append({"tag": tag, "box": self.inbox(), "t": [], "cls": cls}); self.cur = self.recs[-1]
    def inbox(self):
        for tag, bid, cls in reversed(self.stack):
            if bid: return bid
        return None
    def handle_endtag(self, tag):
        if tag in VOID: return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                t = self.stack[i]
                del self.stack[i:]
                if self.cur is not None and (tag in BLOCK or (tag == "div" and "button" in t[2])): self.cur = None
                break
    def handle_data(self, d):
        if self.cur is not None: self.cur["t"].append(d)
def parse(path):
    p = P()
    try: p.feed(open(path, encoding="utf-8", errors="replace").read()); p.close()
    except Exception: pass
    out = []
    for r in p.recs:
        t = norm("".join(r["t"]))
        if t: out.append((r["tag"], r["box"], t, "goJournal" in r["cls"]))
    return out
isj = lambda r: r[3] or (r[0] == "h4" and "go to your journal" in r[2]) or (r[0] == "button" and "journal" in r[2])
res = collections.Counter(); fams = collections.defaultdict(collections.Counter); ex = []
gl = collections.Counter(); pages_out = set(); mods_out = set()
firsts = collections.defaultdict(collections.Counter); pagefam = collections.defaultdict(lambda: collections.defaultdict(set))
import compare_structure as CS
mods = sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m)))
for mod in mods:
    for n, cp, hp in pairs(mod):
        c = parse(cp); h = parse(hp)
        hidx = {}
        for r in h: hidx.setdefault(r[2][:60], r)
        # gold boxes: is the journal element last in its box?
        byb = collections.defaultdict(list)
        for r in h:
            if r[1]: byb[r[1]].append(r)
        for b, rs in byb.items():
            k = next((x for x, r in enumerate(rs) if isj(r)), None)
            if k is not None: gl["gold: journal LAST in its box" if all(isj(r) for r in rs[k:]) else "gold: content AFTER the journal"] += 1
        byb = collections.defaultdict(list)
        for r in c:
            if r[1]: byb[r[1]].append(r)
        for b, rs in byb.items():
            k = next((x for x, r in enumerate(rs) if isj(r)), None)
            if k is None: continue
            tail = [r for r in rs[k + 1:] if not isj(r)]
            # the gold box of this Claude box: the gold box of its first matched pre-journal element
            home = next((hidx[r[2][:60]][1] for r in rs[:k] if r[2][:60] in hidx and hidx[r[2][:60]][1]), None)
            if tail:
                g0 = hidx.get(tail[0][2][:60])
                k0 = "none" if not g0 else ("same" if g0[1] == home else "another" if g0[1] else "outside")
                firsts[k0][f"{rs[k][0]}{'.gj' if rs[k][3] else ''} -> {tail[0][0]}"] += 1
                pagefam[k0][famof(mod)].add(os.path.basename(cp))
            for r in tail:
                g = hidx.get(r[2][:60])
                if not g: res["tail: not in gold"] += 1; continue
                key = ("tail: gold in the SAME box" if g[1] == home else "tail: gold in ANOTHER box") if g[1] else "tail: gold OUTSIDE (the box ended)"
                res[key] += 1; fams[key][famof(mod)] += 1
                if not g[1]:
                    pages_out.add(os.path.basename(cp)); mods_out.add(mod)
                    if len(ex) < 14: ex.append(f"{os.path.basename(cp)} <{r[0]}> {r[2][:60]!r}")
print(dict(gl)); print(dict(res))
for k in firsts: print("FIRST TAIL", k, dict(firsts[k].most_common(8)))
for k in pagefam: print("PAGES", k, {f: len(s) for f, s in sorted(pagefam[k].items(), key=lambda x: -len(x[1]))})
print(f"pages with an OUTSIDE tail {len(pages_out)} / modules {len(mods_out)}")
for k, c in fams.items(): print(k, dict(c.most_common(14)))
for x in ex: print("   ", x)
