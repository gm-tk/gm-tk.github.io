#!/usr/bin/env python3
"""Session 36 Round 4 — the DISCRIMINATOR for the repeated-overview-menu class: on a paired lesson page whose Claude menu is EMPTY,
does the module's Writers Template give that lesson a menu source of its own (a `[Lesson Overview]` / `[Overview]` marker or a
WALT / SC lead line inside the lesson's section)? Cross-tabulated against what the GOLD's lesson menu is (the overview repeated vs
the lesson's own). If "no WT source" lines up with "gold repeats" and "has a WT source" with "gold's own", the rule is derivable
from the Writers Template alone. Run under WSL: python3 _s36_r4_disc.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
ELEM = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
WALT = re.compile(r'(we are learning|learning intentions?|you will show|how will i know|i can\b|success criteria|wh[aā]inga ako|paearu angitu)', re.I)
LESSON_RE = re.compile(r'\[\s*(?:lesson|page)\s*(\d+)\b[^\]]*\]', re.I)
def menu_of(path, is_gold):
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
    return [norm(x.group(2)) for x in ELEM.finditer(m) if len(norm(x.group(2))) >= 3]
def wt_lesson_section(wt, n):
    starts = [(m.start(), int(m.group(1))) for m in LESSON_RE.finditer(wt)]
    idx = [i for i, (p, k) in enumerate(starts) if k == n]
    if not idx: return None
    a = starts[idx[0]][0]
    b = next((p for p, k in starts[idx[0] + 1:] if k != n), len(wt))
    return wt[a:b]
tab = collections.Counter(); ex = collections.defaultdict(list)
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    ov = [(n, cp, hp) for n, cp, hp in pl if re.search(r'_0_0\.html$', os.path.basename(cp))]
    if not ov: continue
    g_ov = set(menu_of(ov[0][2], True))
    if len(g_ov) < 8: continue
    gdir = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    wt = ""
    for t in glob.glob(gdir + "*parsed.txt") if gdir else []:
        if "Writers" in t or "writers" in t: wt += open(t, encoding="utf-8", errors="replace").read()
    if not wt: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        m = re.search(r'_(\d+)_(\d+)\.html$', os.path.basename(cp))
        if not m or m.group(1) == "0": continue
        c_l = menu_of(cp, False)
        if c_l: continue                                   # only the pages Claude leaves EMPTY
        g_l = menu_of(hp, True)
        if not g_l: continue
        share = sum(1 for t in g_l if t in g_ov) / len(g_l)
        goldkind = "gold REPEATS the overview" if share >= 0.8 else ("gold PARTLY" if share >= 0.4 else "gold's OWN lesson menu")
        sec = wt_lesson_section(wt, int(m.group(1)))
        if sec is None: src = "no lesson section found in the WT"
        elif re.search(r'\[\s*(?:lesson\s+)?overview\s*\]', sec[:4000], re.I): src = "WT: an [Overview] marker"
        elif WALT.search(sec[:4000]): src = "WT: a WALT / SC lead, no marker"
        else: src = "WT: NO menu source at all"
        tab["%-26s | %s" % (goldkind, src)] += 1
        k2 = "%s | %s" % (goldkind, src)
        if len(ex[k2]) < 5: ex[k2].append("%s %s" % (code, os.path.basename(cp)))
print("paired LESSON pages with an EMPTY Claude menu, in modules that have a substantial gold overview menu: %d" % sum(tab.values()))
for k, v in tab.most_common(): print("   %-70s %4d" % (k, v))
print("\nexamples:")
for k, v in sorted(ex.items()): print("  %s\n     %s" % (k, ", ".join(v)))
