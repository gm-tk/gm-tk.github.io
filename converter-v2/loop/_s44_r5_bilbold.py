#!/usr/bin/env python3
"""Session 44 Round 5 — writer BOLD inside bilingual prose: for every Claude `<p reo|eng>` / `<li reo|eng>` in the Bilingual folder that
carries a <b>/<strong>, find the gold element with the same text on the gold pages of the module; count gold-bold vs gold-plain, per module
and per container (inside div.activity / free / alert). Also the gold's own bold rate on its bilingual paragraphs. WSL, from outputs/:
python3 _s44_r5_bilbold.py"""
import os, re, glob, io, collections, html as H
from html.parser import HTMLParser
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_", "Bilingual"); CL = os.path.join(ROOT, "01-Claude_Modules_", "Bilingual")
def norm(t): return re.sub(r"[^\wĀ-ſ ]+", "", re.sub(r"\s+", " ", H.unescape(t))).strip().lower()
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st = []; s.out = []; s.cur = None
    def handle_starttag(s, t, a):
        if t in ("br", "img", "hr", "input", "source", "meta", "link", "audio"): return
        s.st.append((t, dict(a).get("class") or ""))
        if t in ("p", "li") and s.cur is None: s.cur = {"tag": t, "txt": [], "bold": False, "st": list(s.st), "depth": len(s.st)}
        elif s.cur is not None and t in ("b", "strong"): s.cur["bold"] = True
    def handle_endtag(s, t):
        if s.cur is not None and t == s.cur["tag"] and len(s.st) == s.cur["depth"]:
            s.cur["txt"] = norm("".join(s.cur["txt"])); s.out.append(s.cur); s.cur = None
        while s.st:
            if s.st.pop()[0] == t: break
    def handle_data(s, d):
        if s.cur is not None: s.cur["txt"].append(d)
def parse(d):
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*.html"))):
        x = P()
        try: x.feed(io.open(p, encoding="utf-8", errors="replace").read())
        except Exception: continue
        out += x.out
    return out
def where(st):
    cl = " ".join(c for _, c in st)
    return "activity" if re.search(r"\bactivity\b", cl) else "alert" if re.search(r"\balert", cl) else "handoff" if "cv2" in cl else "free"
tot = collections.Counter(); per = collections.defaultdict(collections.Counter); gall = collections.Counter()
for cdir in sorted(glob.glob(os.path.join(CL, "*"))):
    code = os.path.basename(cdir); gd = os.path.join(GOLD, code)
    if not os.path.isdir(gd): continue
    g = parse(gd); c = parse(cdir)
    gi = collections.defaultdict(list)
    for e in g:
        if len(e["txt"]) >= 6: gi[e["txt"]].append(e); gall["bold" if e["bold"] else "plain"] += 1
    for e in c:
        if not e["bold"] or len(e["txt"]) < 6: continue
        m = gi.get(e["txt"])
        if not m: tot["no-match"] += 1; per[code]["no-match"] += 1; continue
        k = ("gold-bold" if m[0]["bold"] else "gold-plain") + ":" + where(e["st"])
        tot[k] += 1; per[code][k.split(":")[0]] += 1
print("Claude bold p/li in Bilingual, by the gold's matching element:", dict(tot.most_common()))
print("gold's own p/li bold rate (>= 6 chars):", dict(gall))
for code, c in sorted(per.items()): print(f"  {code:8} {dict(c)}")
