#!/usr/bin/env python3
"""Session 37 Round 3 — THE SINGLE-PAGE MODULE'S FOOTER. Of the 80 same-page-count footer mismatches
where Claude emits next-lesson and the gold does not, the examples are single-page modules
(ANZHFUN05, BLL120, BLL140, BLL150 — one page in both builds). A module with exactly ONE page has no
next lesson to link to, so the link points nowhere. Measure the whole single-page population: what
does the gold do, what does Claude do, and is the consensus strong enough to be a rule?
Run under WSL:  python3 _s37_r3_single.py"""
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
    foot = s[i:i + 4000]
    # home-nav is a CLASS in both builds (`<a href="" class="home-nav">`), not an id — matching it
    # with id= made it invisible in the first run of this instrument, which is exactly the fact the
    # miner's F27 / F29 rows turn on. Match id= OR class= for every link.
    return tuple(k for k in IDS if re.search(r'(?:id|class)="%s"' % k, foot))
def fmt(t): return ",".join(t) if t else "(none)"
gold = collections.Counter(); claude = collections.Counter(); pairtab = collections.Counter()
mods = collections.defaultdict(set); tpl_tab = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    rows = [(n, cp, hp) for n, cp, hp in pl
            if not re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I)]
    if not rows: continue
    cdir = os.path.dirname(rows[0][1]); gdir = os.path.dirname(rows[0][2])
    npc = len([f for f in glob.glob(cdir + "/*.html") if not re.search(r'acks|glossary', f, re.I)])
    npg = len([f for f in glob.glob(gdir + "/*.html") if not re.search(r'acks|glossary', f, re.I)])
    if npc != 1 or npg != 1: continue                      # SINGLE-PAGE modules in BOTH builds only
    tpl = os.path.basename(os.path.dirname(cdir))
    for n, cp, hp in rows:
        g, c = links(hp), links(cp)
        if g is None or c is None: continue
        gold[fmt(g)] += 1; claude[fmt(c)] += 1
        k = "gold %-22s | claude %s" % (fmt(g), fmt(c)); pairtab[k] += 1; mods[k].add(code)
        tpl_tab[tpl][k] += 1
        if len(ex[k]) < 6: ex[k].append("%s %s (%s)" % (code, os.path.basename(cp), tpl))
tot = sum(pairtab.values())
print("SINGLE-PAGE MODULES (one page in BOTH builds) — %d paired pages / %d modules"
      % (tot, len({m for s in mods.values() for m in s})))
print("=" * 88)
print("\n   what the GOLD's footer carries:")
for k, v in gold.most_common(): print("      %-26s %4d   = %.2f" % (k, v, v / max(1, tot)))
print("\n   what CLAUDE's footer carries:")
for k, v in claude.most_common(): print("      %-26s %4d   = %.2f" % (k, v, v / max(1, tot)))
print("\n   paired:")
for k, v in pairtab.most_common(): print("      %-50s %4d  mods %3d" % (k, v, len(mods[k])))
print("\n   by template:")
for t, c in sorted(tpl_tab.items(), key=lambda x: -sum(x[1].values())):
    print("      %-14s %3d" % (t, sum(c.values())))
    for k, v in c.most_common(3): print("           %-50s %3d" % (k, v))
print("\n   examples:")
for k, _ in pairtab.most_common(4):
    print("   " + k); [print("      " + e) for e in ex[k]]
