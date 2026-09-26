#!/usr/bin/env python3
"""_s51_r3_unboxed.py — session 51 Round 3 PICK: every GOLD activity box (div.activity, by its number and position) whose text
blocks Claude has on the paired page but OUTSIDE any activity box ("unboxed"), or splits across a box and free text. Per gold box:
its number, its first text (the title), the share of its matched blocks Claude keeps inside a box. Grouped by the box's first
words (the title / the instruction form) and by family, so a recurring unboxed KIND shows up. WSL, from reference/tests/.
Writes outputs/_s51_r3_unboxed.tsv."""
import os, re, sys, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
from _structural_skeleton import body_source

VOID = {"br", "img", "input", "hr", "meta", "link", "source", "area", "col", "wbr", "embed", "param", "track"}
TEXT = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th"}


class Boxes(HTMLParser):
    """blocks = [(box_key or None, text)] in document order; box_key = 'N#k' for the k-th activity box (number N)."""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.blocks = []; self.k = 0; self.buf = None; self.depth_text = 0
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        a = dict(attrs); cls = a.get("class", "") or ""
        box = None
        if tag == "div" and re.search(r"\bactivity\b", cls):
            self.k += 1; box = f"{a.get('number', '?')}#{self.k}"
        self.stack.append((tag, box))
        if tag in TEXT and self.buf is None: self.buf = []; self.depth_text = len(self.stack)
    def handle_endtag(self, tag):
        if tag in VOID: return
        while self.stack:
            t, _ = self.stack.pop()
            if self.buf is not None and len(self.stack) < self.depth_text:
                txt = re.sub(r"\s+", " ", "".join(self.buf)).strip()
                if txt: self.blocks.append((self.cur_box(), txt))
                self.buf = None
            if t == tag: break
    def handle_data(self, d):
        if self.buf is not None: self.buf.append(d)
    def cur_box(self):
        for t, b in reversed(self.stack):
            if b: return b
        return None


def parse(path):
    try: s = open(path, encoding="utf-8", errors="replace").read()
    except OSError: return []
    p = Boxes()
    try: p.feed(body_source(s)); p.close()
    except Exception: pass
    return [(b, t) for b, t in p.blocks if len(t) >= 20 or len(t.split()) >= 4]


fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", t.lower()).split())
kinds = collections.Counter(); fam = collections.Counter(); famp = collections.defaultdict(set); rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    f = re.sub(r"\d.*$", "", code)
    for n, cp, hp in pairs(code):
        g = parse(hp); c = [(b, fold(t)) for b, t in parse(cp)]
        if not g or not c: continue
        gb = collections.defaultdict(list)
        for b, t in g:
            if b: gb[b].append(t)
        for box, texts in gb.items():
            inb = free = 0
            for t in texts:
                ft = fold(t)
                best = max(c, key=lambda x: PC.jacc(x[1], ft), default=None)
                if not best or PC.jacc(best[1], ft) < 0.6: continue
                if best[0]: inb += 1
                else: free += 1
            if free and not inb:
                first = texts[0][:60]
                kinds[" ".join(fold(first).split()[:3])] += 1; fam[f] += 1; famp[f].add(os.path.basename(cp))
                rows.append((code, os.path.basename(cp), box, str(free), first))
print("gold boxes Claude renders wholly unboxed:", len(rows), "pages", len({(r[0], r[1]) for r in rows}))
print("by family:", [(k, v, len(famp[k])) for k, v in fam.most_common(25)])
print("by first words:"); [print(f"  {v:4d}  {k}") for k, v in kinds.most_common(45)]
with open("../../outputs/_s51_r3_unboxed.tsv", "w") as fh:
    for r in rows: fh.write("\t".join(r) + "\n")
