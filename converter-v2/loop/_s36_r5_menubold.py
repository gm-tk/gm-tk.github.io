#!/usr/bin/env python3
"""Session 36 Round 5 PICK measurement — THE BOLD-LABELLED MENU PARAGRAPH. In a module overview's two-column menu the writer
sometimes types a run of bold-labelled lines under a section heading — `__**Reading:**__ Students develop basic literacy…`,
`__**Writing:**__ …` (the BLL "Do:" block). Claude renders each as a `<p><b>…`; the miner says the gold has nothing at that
position (row #49, 23 pages / 23 modules, consensus 1.00) — because the gold renders them as `<li>` items.
For every paired OVERVIEW page: find the gold's module-menu elements and Claude's; for each WT line inside the overview's menu
region that starts with a bold label, report the ELEMENT the gold used for that text (li / p / h5 / absent) and Claude's.
Run under WSL: python3 _s36_r5_menubold.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
ELEM = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
BOLDLABEL = re.compile(r'^\s*(?:__)?\*\*\s*([^*:]{2,40}?)\s*:?\s*\*\*(?:__)?\s*:?\s+(\S.*)$')
RED = re.compile(r'\U0001f534\[RED TEXT\](.*?)\[/RED TEXT\]\U0001f534', re.S)
def menu_elems(path, is_gold):
    s = open(path, encoding="utf-8", errors="replace").read()
    i = -1
    if is_gold:
        for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
            j = s.find(mark)
            if j > 0: i = j; break
    else: i = s.find('<div id="body">')
    head = s[:i] if i > 0 else s
    k = head.find("module-menu-content")
    m = head[k:] if k > 0 else ""
    return [(x.group(1), norm(x.group(2))) for x in ELEM.finditer(m)]
tab = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list); labels = collections.Counter()
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    ov = [(n, cp, hp) for n, cp, hp in pl if re.search(r'_0_0\.html$', os.path.basename(cp))]
    if not ov: continue
    _, cp, hp = ov[0]
    gdir = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    wt = ""
    for t in glob.glob(gdir + "*parsed.txt") if gdir else []:
        if "Writers" in t or "writers" in t: wt += open(t, encoding="utf-8", errors="replace").read()
    if not wt: continue
    g = menu_elems(hp, True); c = menu_elems(cp, False)
    if not g and not c: continue
    gmap = {}; cmap = {}
    for tag, t in g: gmap.setdefault(t, tag)
    for tag, t in c: cmap.setdefault(t, tag)
    # the WT's overview head: everything before the first [Lesson] / [Page] boundary
    b = re.search(r'\[\s*(?:lesson|page)\s*\d', wt, re.I)
    headtxt = wt[:b.start()] if b else wt[:12000]
    for line in headtxt.splitlines():
        plain = RED.sub(" ", line).strip()
        m2 = BOLDLABEL.match(plain)
        if not m2: continue
        body = m2.group(2)
        t = norm(body)[:40]
        if len(t) < 12: continue
        gt = next((tag for tt, tag in gmap.items() if tt.startswith(t)), "absent")
        ct = next((tag for tt, tag in cmap.items() if tt.startswith(t)), "absent")
        tab["gold=%-6s claude=%s" % (gt, ct)] += 1
        labels[m2.group(1).strip().lower()] += 1
        mods["gold=%s claude=%s" % (gt, ct)].add(code)
        k2 = "gold=%s claude=%s" % (gt, ct)
        if len(ex[k2]) < 5: ex[k2].append("%s: **%s** %s" % (code, m2.group(1).strip(), body[:55]))
print("bold-labelled lines inside an overview's menu region: %d" % sum(tab.values()))
for k, v in tab.most_common():
    key = k.replace("gold=", "gold=").replace("  ", " ")
    print("   %-34s %4d   modules %d" % (k, v, len(mods[re.sub(r'\s+', ' ', k)] or [])))
print("\nthe labels themselves (top 15):")
for k, v in labels.most_common(15): print("   %-28s %d" % (k, v))
print("\nexamples:")
for k, v in sorted(ex.items()):
    print("  " + k)
    for e in v: print("     " + e)
