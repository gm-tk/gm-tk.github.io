#!/usr/bin/env python3
"""_s54_r9_imgfate.py — session 54 Round 9: THE IMAGE'S FATE, keyed by its stock id. For every paired page, every Claude <img> whose
src / alt carries a stock id (iStock-NNN / gmNNN / shutterstock NNN) is looked up on the GOLD paired page (and, failing that, on every
gold page of the module) by the same id, and both placements are classified: main column (col-md-8 / col-12 body), side column
(col-md-4 …), activity box, alertImage, alert, widget (a known widget class), acks, or ABSENT. Tallied by (Claude placement → gold
placement) and by family. WSL, from reference/tests/:  python3 ../../outputs/_s54_r9_imgfate.py > ../../outputs/_s54_r9_imgfate.log"""
import os, re, sys, glob, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _corpus
from anchor_compare import CLAUDE, HUMAN

WIDGETS = ("dragAndDrop", "flipCard", "carousel", "accordion", "tabs", "clickDrop", "modal", "speechBubble", "dropDown", "multiChoiceQuiz",
           "cv2-interactive", "hintSlider", "selfCheck", "reorder", "memoryGame", "imageLabel", "infoImage")
ID = re.compile(r"(?:iStock-|gm)(\d{6,})|shutterstock[^\d]{0,40}(\d{6,})", re.I)


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.imgs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img":
            key = " ".join(filter(None, [a.get("src", ""), a.get("alt", "")]))
            m = ID.search(key)
            if m: self.imgs.append((m.group(1) or m.group(2), self.where()))
            return
        if tag in ("br", "hr", "input", "source", "meta", "link"): return
        self.stack.append((tag, (a.get("class") or "") + " " + (a.get("id") or "")))
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag: del self.stack[i:]; break
    def where(self):
        cls = [c for _, c in self.stack]
        j = " ".join(cls)
        if "acks" in j: return "acks"
        for w in WIDGETS:
            if re.search(r"\b" + w + r"\b", j): return "widget"
        if re.search(r"\balertImage\b", j): return "alertImage"
        if re.search(r"\bactivity\b", j): return "activity"
        if re.search(r"\balert", j): return "alert"
        if re.search(r"\bcol-md-[1-5]\b", j): return "side"
        if "header" in j or "module-menu" in j: return "menu"
        return "main"


def imgs(path):
    p = P()
    try: p.feed(open(path, encoding="utf-8", errors="replace").read())
    except Exception: return []
    return p.imgs


fam = lambda m: re.sub(r"\d.*$", "", m)
tally = collections.Counter(); byfam = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set)
for mod in sorted(set(_corpus.gate_mods(CLAUDE))):
    pp = list(pairs(mod))
    if not pp: continue
    allgold = {}
    for gp in glob.glob(os.path.join(_corpus.mdir(HUMAN, mod), "*.html")):
        for i, w in imgs(gp): allgold.setdefault(i, w)
    for n, cp, hp in pp:
        g = {}
        for i, w in imgs(hp): g.setdefault(i, w)
        for i, w in imgs(cp):
            gw = g.get(i) or (("other-page:" + allgold[i]) if i in allgold else "ABSENT")
            k = (w, gw); tally[k] += 1; byfam[k][fam(mod)] += 1; pages[k].add(os.path.basename(cp))
print("Claude stock images by (Claude placement → gold placement of the same id):")
tot = sum(tally.values())
for k, v in tally.most_common(30):
    print(f"  {v:5d} ({v / tot:5.1%})  {k[0]:10s} → {k[1]:22s} {len(pages[k]):4d} pages  {dict(byfam[k].most_common(6))}")
print("total", tot)

# per family: of Claude MAIN-column images the gold has on the same page, the share the gold puts in the SIDE column
fm = collections.defaultdict(collections.Counter); fp = collections.defaultdict(set)
for (cw, gw), c in tally.items():
    if cw != "main" or gw.startswith("other-page") or gw == "ABSENT": continue
    for f, n in byfam[(cw, gw)].items(): fm[f][gw] += n
print("\nper family (Claude main-column images the gold has on the page): side share")
for f, c in sorted(fm.items(), key=lambda kv: -sum(kv[1].values())):
    n = sum(c.values())
    if n < 8: continue
    print(f"  {f:8s} n={n:4d}  side {c['side'] / n:.2f}  main {c['main'] / n:.2f}  widget {c['widget'] / n:.2f}  other {(n - c['side'] - c['main'] - c['widget']) / n:.2f}")
