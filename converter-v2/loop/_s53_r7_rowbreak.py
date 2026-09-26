#!/usr/bin/env python3
"""_s53_r7_rowbreak.py — session 53 Round 7: WHERE DOES CLAUDE OPEN A NEW TOP-LEVEL ROW THE GOLD DOES NOT? For every paired page: the
#body's top-level rows on each side, each described by the FIRST block inside it (tag + a text key) and the LAST block of the row
before it. A Claude row whose first block's text sits, on the gold page, in the SAME top-level row as the previous Claude row's last
block = an EXTRA row break. Tallied by (what ended the previous row → what opened the new row) — the break's cue — per family.
WSL, from reference/tests/:  python3 ../../outputs/_s53_r7_rowbreak.py > ../../outputs/_s53_r7_rowbreak.log"""
import os, re, sys, collections, html as H
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
famof = lambda m: re.sub(r"\d.*$", "", m)
BLOCK = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "img", "iframe", "audio"}
VOID = {"img", "br", "input", "col", "hr", "meta", "link", "source", "area", "base", "wbr", "iframe", "audio"}
def norm(s): return re.sub(r"\s+", " ", re.sub(r"[^0-9a-zāēīōū ]+", " ", H.unescape(s).lower())).strip()

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.st = []; self.body = None; self.row = -1; self.blocks = []; self.cur = None; self.skip = 0
    def handle_starttag(self, t, a):
        a = dict(a); cls = set((a.get("class") or "").split())
        if t in ("script", "style"): self.skip += 1; return
        if t in VOID:
            if self.body is not None and t in ("img", "iframe", "audio") and self.cur is None:
                self.blocks.append((self.row, t, os.path.basename((a.get("src") or "").split("?")[0])[:30], self._ctx()))
            return
        d = len(self.st); self.st.append((t, cls, a.get("id")))
        if a.get("id") == "body": self.body = d; return
        if self.body is None: return
        if d == self.body + 1 and t == "div" and "row" in cls: self.row += 1
        if t in BLOCK and self.cur is None: self.cur = [t, [], d, self._ctx()]
    def _ctx(self):
        for t, cls, i in reversed(self.st):
            if cls & {"activity", "alert", "alertActivity", "cv2-interactive", "accordion", "carousel", "tabs"}: return sorted(cls & {"activity", "alert", "alertActivity", "cv2-interactive", "accordion", "carousel", "tabs"})[0]
        return "free"
    def handle_endtag(self, t):
        if t in ("script", "style"): self.skip = max(0, self.skip - 1); return
        if t in VOID: return
        for i in range(len(self.st) - 1, -1, -1):
            if self.st[i][0] == t:
                if self.cur is not None and i <= self.cur[2]:
                    txt = norm("".join(self.cur[1]))
                    if txt: self.blocks.append((self.row, self.cur[0], txt[:40], self.cur[3]))
                    self.cur = None
                if self.body is not None and i <= self.body: self.body = None
                del self.st[i:]; break
    def handle_data(self, d):
        if self.cur is not None and not self.skip: self.cur[1].append(d)

def parse(p):
    x = P()
    try: x.feed(open(p, encoding="utf-8", errors="replace").read())
    except Exception: pass
    return [b for b in x.blocks if b[0] >= 0]

brk = collections.Counter(); fam = collections.defaultdict(collections.Counter); pg = collections.defaultdict(set); ex = collections.defaultdict(list)
tot_extra = 0
for mod in sorted(m for m in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m))):
    for n, cp, hp in pairs(mod):
        g = parse(hp); c = parse(cp)
        grow = {}
        for r, t, k, cx in g: grow.setdefault(k, r)
        for i in range(1, len(c)):
            (r0, t0, k0, x0), (r1, t1, k1, x1) = c[i - 1], c[i]
            if r1 == r0 or len(k0) < 6 or len(k1) < 6: continue
            if k0 in grow and k1 in grow and grow[k0] == grow[k1]:
                cue = (f"{t0}@{x0}", f"{t1}@{x1}")
                brk[cue] += 1; fam[cue][famof(mod)] += 1; pg[cue].add(os.path.basename(cp)); tot_extra += 1
                if len(ex[cue]) < 3: ex[cue].append(f"{os.path.basename(cp)} …{k0[-30:]!r} | {k1[:30]!r}")
print(f"extra Claude row breaks (the gold keeps both blocks in one top-level row): {tot_extra}\n")
for cue, v in brk.most_common(40):
    print(f"{v:5d} breaks {len(pg[cue]):4d} pages  prev {cue[0]:22s} → next {cue[1]:22s} [{', '.join(f'{f} {x}' for f, x in fam[cue].most_common(5))}]")
    for e in ex[cue]: print("        e.g.", e)
