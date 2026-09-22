#!/usr/bin/env python3
"""Session 37 Round 3 PICK — WHAT DECIDES THE FOOTER'S LINK SET?

The miner's alignment-free chrome facts (DIFF_QUEUE.md, the r436 corpus) put three footer rows near
the top of the queue, and they are one class seen three ways — Claude's footer carries a DIFFERENT SET
OF NAVIGATION LINKS from the gold's:

  F26 EXTRA footer:links=prev-lesson,next-lesson,home-nav   283 pages / 128 modules  consensus 0.40
  F27 EXTRA footer:links=next-lesson,home-nav               112 pages / 110 modules  consensus 0.88
  F29 EXTRA footer:links=prev-lesson,home-nav                77 pages /  77 modules  consensus 0.86
  F30 MISSING footer:links=home-nav,next-lesson              70 pages /  69 modules  consensus 0.03

Footer is a CHROME region, which §3 step 1 ranks before body, and 110 modules is far over the chrome
floor of 10.

THE HYPOTHESIS a human would form: the link set is POSITIONAL — the first page of a module has no
"Previous", the last has no "Next", an overview page has its own form — and Claude is applying a
different positional rule from the human's. This measures exactly that, per page position and per
template, so the rule can be keyed on whatever actually decides it rather than guessed.

A link is counted by its ID (`prev-lesson` / `next-lesson` / `home-nav`), which is how the gold, the
miner and the skeleton all identify it — NOT by link text, which the writer can word freely.

Run under WSL:  python3 _s37_r3_footer.py
"""
import re, os, sys, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"))
from _discrepancy_audit import pairs
import _corpus

IDS = ("prev-lesson", "next-lesson", "home-nav")


# THE HUMAN COMMENTS A LINK OUT RATHER THAN DELETING IT. On a module's last page the gold ships
# `<!-- <li><a href="" id="next-lesson" ...></li> -->` (AGH1003_08.0). A regex over the raw text
# counts that as PRESENT, which inverts the whole measurement — the first run of this instrument
# reported 156 last pages where "the gold keeps Next and Claude drops it" and every one of them was
# a commented-out link, i.e. the two sides AGREE. Strip comments first; the skeleton's HTML parser
# drops them, so this is also what every protected gate sees.
COMMENT = re.compile(r'<!--.*?-->', re.S)


def footer_links(path):
    s = COMMENT.sub(' ', open(path, encoding="utf-8", errors="replace").read())
    i = s.find('id="footer"')
    if i < 0:
        i = s.find('class="footer')
    if i < 0:
        return None
    foot = s[i:i + 4000]
    # home-nav is a CLASS in both builds (`<a href="" class="home-nav">`), not an id — matching it
    # with id= alone made it invisible in the first runs of this instrument, and it is exactly the
    # fact the miner's F27 / F29 rows turn on. Match id= OR class= for every link.
    return tuple(k for k in IDS if re.search(r'(?:id|class)="%s"' % k, foot))


def fmt(t):
    return ",".join(t) if t else "(none)"


pair_tab = collections.Counter()
pos_tab = collections.defaultdict(collections.Counter)
tpl_tab = collections.defaultdict(collections.Counter)
ex = collections.defaultdict(list)
agree = 0
total = 0

for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try:
        pl = pairs(code)
    except Exception:
        continue
    rows = [(n, cp, hp) for n, cp, hp in pl
            if not re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I)]
    if not rows:
        continue
    tpl = os.path.basename(os.path.dirname(os.path.dirname(rows[0][1])))

    def keyf(r):
        m = re.search(r'_(\d+)_(\d+)\.html$', os.path.basename(r[1]))
        return (int(m.group(1)), int(m.group(2))) if m else (999, 999)
    rows.sort(key=keyf)
    last = len(rows) - 1
    for idx, (n, cp, hp) in enumerate(rows):
        g = footer_links(hp)
        c = footer_links(cp)
        if g is None or c is None:
            continue
        total += 1
        page = os.path.basename(cp)
        isov = bool(re.search(r'_0_0\.html$', page))
        pos = ("overview" if isov else
               "FIRST lesson page" if idx == 0 or (idx == 1 and re.search(r'_0_0\.html$', os.path.basename(rows[0][1]))) else
               "LAST page" if idx == last else "middle page")
        if g == c:
            agree += 1
            pos_tab[pos]["AGREE " + fmt(g)] += 1
            continue
        k = "gold %-38s | claude %s" % (fmt(g), fmt(c))
        pair_tab[k] += 1
        pos_tab[pos]["gold %s | claude %s" % (fmt(g), fmt(c))] += 1
        tpl_tab[tpl]["gold %s | claude %s" % (fmt(g), fmt(c))] += 1
        if len(ex[k]) < 4:
            ex[k].append("%s %s (%s, %s)" % (code, page, pos, tpl))

print("=" * 104)
print("THE FOOTER'S NAVIGATION LINK SET — %d paired pages, %d agree (%.1f %%), %d differ"
      % (total, agree, 100.0 * agree / max(1, total), total - agree))
print("=" * 104)
print("\nthe MISMATCH forms, most common first:")
for k, v in pair_tab.most_common(16):
    print("   %-66s %5d" % (k[:66], v))

print("\nBY PAGE POSITION (the positional hypothesis):")
for pos in ("overview", "FIRST lesson page", "middle page", "LAST page"):
    t = pos_tab.get(pos)
    if not t:
        continue
    tot = sum(t.values())
    ag = sum(v for k, v in t.items() if k.startswith("AGREE"))
    print("\n   %-20s %5d pages, %d agree (%.0f %%)" % (pos, tot, ag, 100.0 * ag / max(1, tot)))
    for k, v in t.most_common(6):
        print("        %-60s %5d" % (k[:60], v))

print("\nBY TEMPLATE (mismatches only):")
for tpl, t in sorted(tpl_tab.items(), key=lambda x: -sum(x[1].values())):
    print("   %-16s %4d mismatched" % (tpl, sum(t.values())))
    for k, v in t.most_common(3):
        print("        %-60s %5d" % (k[:60], v))

print("\nexamples:")
for k, _ in pair_tab.most_common(6):
    print("  " + k)
    for e in ex[k]:
        print("     " + e)
