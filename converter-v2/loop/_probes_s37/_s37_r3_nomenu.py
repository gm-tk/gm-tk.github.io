#!/usr/bin/env python3
"""Session 37 Round 3 PICK — THE PAGES WHERE CLAUDE BUILDS NO MODULE MENU AT ALL.

The miner's completeness census (DIFF_QUEUE.md, the r436 corpus) makes module-menu the largest
derivable chrome region left: 5,451 derivable misses on 729 pages / 204 modules. Its worked example
is MXFL202 — `gold 53 items (51 in WT) / Claude 0` on four separate lesson pages.

Session 36 dispositioned part of this population: 126 pages / 30 modules where Claude's menu is empty
and THE GOLD REPEATS THE MODULE OVERVIEW MENU were DECLINED as a named KB override (KB 01B makes a
lesson page's menu that lesson's own [Lesson Overview] block, so an empty menu is KB-correct there).
That decline is NOT this class, and the two must be separated before anything is picked.

So split the empty-Claude-menu pages three ways:
  (a) the gold's menu REPEATS the module overview   -> the s36 DECLINED class, KB-correct
  (b) the gold's menu is ITS OWN and the WT carries its text -> derivable, a real candidate
  (c) the gold's menu is its own but NOT in the WT   -> gold-invented, no source

and report (b) by template and module family, with the per-module page counts, so the round can be
scoped. Counted on the CLAUDE + GOLD PAGES THEMSELVES and on the WT text — the Round-2 lesson is that
a raw-WT window is not a proxy for what the engine sees, so the WT is used here only to answer
"does this text exist in the source at all", which is exactly what the miner's `in WT` column means.

Run under WSL:  python3 _s37_r3_nomenu.py
"""
import re, os, sys, glob, html, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"))
from _discrepancy_audit import pairs
import _corpus


def norm(s):
    return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


ELEM = re.compile(r'<(p|h[1-6]|li|span)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li|span)\b).)*?)</\1>', re.S)
TAG = re.compile(r'\[([^\[\]\n]{1,60})\]')


def menu_items(path, is_gold):
    s = open(path, encoding="utf-8", errors="replace").read()
    i = -1
    if is_gold:
        for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
            j = s.find(mark)
            if j > 0:
                i = j
                break
    else:
        i = s.find('<div id="body">')
    head = s[:i] if i > 0 else s
    k = head.find("module-menu-content")
    if k < 0:
        return []
    return [norm(x.group(2)) for x in ELEM.finditer(head[k:]) if len(norm(x.group(2))) >= 3]


def wt_text(code):
    gd = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    if not gd:
        return ""
    b = []
    for t in sorted(glob.glob(gd + "*parsed.txt")):
        n = os.path.basename(t)
        if re.search(r'media\s*list', n, re.I) and not re.search(r'writer', n, re.I):
            continue
        b.append(open(t, encoding="utf-8", errors="replace").read())
    return "\n".join(b)


kind = collections.Counter()
kmods = collections.defaultdict(set)
bpages = collections.Counter()
btpl = collections.Counter()
ex = collections.defaultdict(list)

for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try:
        pl = pairs(code)
    except Exception:
        continue
    tpl = None
    ov = [(n, cp, hp) for n, cp, hp in pl if re.search(r'_0_0\.html$', os.path.basename(cp))]
    g_ov = set(menu_items(ov[0][2], True)) if ov else set()
    wt = wt_text(code)
    wtn = norm(TAG.sub(' ', wt)) if wt else ""
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I):
            continue
        if tpl is None:
            tpl = os.path.basename(os.path.dirname(os.path.dirname(cp)))
        c = menu_items(cp, False)
        if c:
            continue                                   # Claude built SOMETHING
        g = menu_items(hp, True)
        if len(g) < 8:
            continue                                   # not a substantial gold menu
        page = os.path.basename(cp)
        share_ov = (sum(1 for t in g if t in g_ov) / len(g)) if g_ov else 0.0
        if share_ov >= 0.8:
            k = "(a) the gold REPEATS the module overview menu — the s36 DECLINED KB override"
        else:
            in_wt = sum(1 for t in g if len(t) >= 6 and t in wtn) / max(1, len([t for t in g if len(t) >= 6]))
            if in_wt >= 0.5:
                k = "(b) the gold's OWN menu and its text IS in the Writers Template — DERIVABLE"
                bpages[code] += 1
                btpl[tpl or "?"] += 1
            else:
                k = "(c) the gold's own menu but its text is NOT in the WT — gold-invented, no source"
        kind[k] += 1
        kmods[k].add(code)
        if len(ex[k]) < 6:
            ex[k].append("%s %s — gold %d items, e.g. «%s»" % (code, page, len(g), plain(g[0])[:26]))

print("=" * 100)
print("PAGES WITH AN EMPTY CLAUDE MODULE MENU AND A SUBSTANTIAL GOLD MENU (>= 8 items) — %d"
      % sum(kind.values()))
print("=" * 100)
for k, v in kind.most_common():
    print("   %-70s %4d  mods %4d" % (k[:70], v, len(kmods[k])))

print("\n   (b) THE DERIVABLE GROUP, by template: %s" % dict(btpl))
print("   (b) by module (pages each), top 25:")
for k, v in bpages.most_common(25):
    print("      %-12s %3d" % (k, v))
print("   (b) totals: %d pages / %d modules" % (sum(bpages.values()), len(bpages)))

print()
for k, _ in kind.most_common():
    print("  " + k)
    for e in ex[k]:
        print("     " + e)
