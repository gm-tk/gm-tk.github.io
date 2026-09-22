#!/usr/bin/env python3
"""Session 37 Round 2 TRIANGULATION — the `flip card` named-in-free-text unclassified boxes.
Lists every one: module, page, activity id, the WT window that names it, and whether the HUMAN GOLD
built a flip card on that page. The gold's build is the target (A1: the writer's tag decides the
component; here the writer named the component in prose the scanner ignored).
Run under WSL:  python3 _s37_r2_flip.py"""
import re, os, sys, glob, json, io, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
CV2 = os.path.join(ROOT, "CONVERTER_V2")
sys.path.insert(0, os.path.join(CV2, "reference", "tests"))
from _discrepancy_audit import pairs
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
def fold(s): return re.sub(r'[^a-z0-9 ]+', ' ', s.lower())
lex = json.load(io.open(os.path.join(CV2, "data", "Tag_Lexicon.json"), encoding="utf-8"))
FLIP = [a.lower() for a in lex["tags"]["flip card"]["aliases"] if len(str(a)) >= 4]
RED = re.compile(r'INTERACTIVE \(un-built\) #\d+:\s*unclassified\s*—\s*([^<—]{1,40}?)\s*—', re.I)
GOLDFLIP = re.compile(r'flip-?card|flipCard|card-flip|\bflipper\b', re.I)
def wt_text(code):
    gd = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    if not gd: return ""
    b = []
    for t in sorted(glob.glob(gd + "*parsed.txt")):
        n = os.path.basename(t)
        if re.search(r'media\s*list', n, re.I) and not re.search(r'writer', n, re.I): continue
        b.append(open(t, encoding="utf-8", errors="replace").read())
    return "\n".join(b)
goldmap = {}
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    for n, cp, hp in pl: goldmap[os.path.abspath(cp)] = hp
rows = []; fam = collections.Counter(); goldyes = collections.Counter()
for f in sorted(glob.glob(ROOT + "/01-Claude_Modules_/*/*/*.html")):
    s = open(f, encoding="utf-8", errors="replace").read()
    if "unclassified" not in s: continue
    code = os.path.basename(os.path.dirname(f))
    wt = wt_text(code)
    if not wt: continue
    for m in RED.finditer(s):
        act = m.group(1).strip()
        num = (re.search(r'([0-9]+[A-Za-z]?)', act) or [None, None])[1]
        if not num: continue
        win = ""
        for t in re.finditer(r'\[\s*activity[^\]]*\]', wt, re.I):
            seg = wt[t.start():t.start() + 700]
            if re.search(r'\b' + re.escape(num) + r'\b', seg[:260], re.I):
                cut = seg.find("TABLE"); win = seg[:cut if cut > 0 else 700]; break
        if not win: continue
        fw = fold(plain(win))
        hit = next((a for a in FLIP if a in fw), None)
        if not hit: continue
        hp = goldmap.get(os.path.abspath(f))
        gb = "?" if not hp else ("GOLD BUILT a flip card" if GOLDFLIP.search(open(hp, encoding="utf-8", errors="replace").read()) else "gold has NO flip card")
        goldyes[gb] += 1
        fam[re.match(r'[A-Z]+', code).group(0)] += 1
        rows.append((code, os.path.basename(f), act, hit, gb))
print("FLIP-CARD NAMED IN FREE TEXT, LEFT UNCLASSIFIED — %d boxes / %d modules"
      % (len(rows), len({r[0] for r in rows})))
print("=" * 96)
print("\nthe GOLD's verdict on those pages:")
for k, v in goldyes.most_common(): print("   %-34s %5d" % (k, v))
print("\nby module family:")
for k, v in fam.most_common(): print("   %-10s %4d" % (k, v))
print("\nevery box:")
for r in rows: print("   %-10s %-24s %-14s alias «%s»  %s" % r)
