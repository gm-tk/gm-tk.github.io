#!/usr/bin/env python3
"""Session 37 Round 3 — IS THE FOOTER MISMATCH A FOOTER RULE, OR A PAGE-COUNT DIFFERENCE?
After stripping HTML comments (the human comments a link out rather than deleting it) the footer link
set agrees on 90.3 % of 2,497 paired pages. The largest remaining shape is `gold prev-lesson |
claude prev-lesson,next-lesson` (80 pages): Claude emits a Next link where the gold has none. The
converter's rule is already the human's — Next on every page except the module's LAST — so the
question is whether these pages are ones where CLAUDE'S last page and THE GOLD'S last page are not the
same page, i.e. the two builds split the module into a different number of pages. If so this is not a
footer class at all; it is the page-split / dual-build class (Needs Chris #6).
Run under WSL:  python3 _s37_r3_footer2.py"""
import re, os, sys, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"))
from _discrepancy_audit import pairs
import _corpus
IDS = ("prev-lesson", "next-lesson", "home-nav")
COMMENT = re.compile(r'<!--.*?-->', re.S)
def links(path):
    s = COMMENT.sub(' ', open(path, encoding="utf-8", errors="replace").read())
    i = s.find('id="footer"')
    if i < 0: i = s.find('class="footer')
    if i < 0: return None
    return tuple(k for k in IDS if re.search(r'id="%s"' % k, s[i:i + 4000]))
tab = collections.Counter(); ex = collections.defaultdict(list)
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    rows = [(n, cp, hp) for n, cp, hp in pl
            if not re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I)]
    if not rows: continue
    cdir = os.path.dirname(rows[0][1]); gdir = os.path.dirname(rows[0][2])
    npc = len([f for f in glob.glob(cdir + "/*.html") if not re.search(r'acks|glossary', f, re.I)])
    npg = len([f for f in glob.glob(gdir + "/*.html") if not re.search(r'acks|glossary', f, re.I)])
    for n, cp, hp in rows:
        g, c = links(hp), links(cp)
        if g is None or c is None or g == c: continue
        if not ("next-lesson" in c and "next-lesson" not in g): continue
        k = ("CLAUDE HAS MORE PAGES than the gold (%d vs %d) — a page-split difference" % (npc, npg)
             if npc > npg else
             "same page count (%d) — a genuine footer difference" % npc if npc == npg else
             "GOLD has more pages (%d vs %d)" % (npg, npc))
        k = re.sub(r'\(\d+ vs \d+\)', '', k); k = re.sub(r'\(\d+\)', '', k)
        tab[k] += 1
        if len(ex[k]) < 6: ex[k].append("%s %s (claude %d pages / gold %d)" % (code, os.path.basename(cp), npc, npg))
print("PAGES WHERE CLAUDE EMITS next-lesson AND THE GOLD DOES NOT — %d" % sum(tab.values()))
print("=" * 88)
for k, v in tab.most_common(): print("   %-62s %4d" % (k.strip(), v))
print()
for k, _ in tab.most_common():
    print("  " + k.strip()); [print("     " + e) for e in ex[k]]
