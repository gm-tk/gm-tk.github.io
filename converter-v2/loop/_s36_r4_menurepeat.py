#!/usr/bin/env python3
"""Session 36 Round 4 PICK measurement — THE REPEATED OVERVIEW MENU. On a lesson page whose module menu Claude leaves EMPTY,
what does the gold's menu hold? Specifically: is it the module's OWN OVERVIEW menu repeated verbatim?
For every paired module with an overview page: build the gold's overview-menu text set and Claude's; then for each paired LESSON
page compare the gold's lesson menu against that overview set (share of the gold lesson-menu items that are in the gold overview
menu) and record what Claude has. Report per module and corpus-wide, and split by template family.
Run under WSL: python3 _s36_r4_menurepeat.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
ELEM = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
def menu_of(path, is_gold):
    s = open(path, encoding="utf-8", errors="replace").read()
    i = s.find('<div id="body">') if not is_gold else -1
    if is_gold:
        for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
            j = s.find(mark)
            if j > 0: i = j; break
    head = s[:i] if i > 0 else s
    k = head.find("module-menu-content")
    m = head[k:] if k > 0 else ""
    return [norm(x.group(2)) for x in ELEM.finditer(m) if len(norm(x.group(2))) >= 3]
fam_of = {}
for d in glob.glob(ROOT + "/01-Finalized_Modules_/*/*/"):
    fam_of[os.path.basename(d.rstrip("/"))] = d.split("/")[-3]
rows = []; bucket = collections.Counter(); byfam = collections.defaultdict(collections.Counter); mods = {}
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    ov = [(n, cp, hp) for n, cp, hp in pl if re.search(r'_0_0\.html$', os.path.basename(cp))]
    if not ov: continue
    g_ov = set(menu_of(ov[0][2], True)); c_ov = set(menu_of(ov[0][1], False))
    if len(g_ov) < 8: continue                       # the module has no substantial overview menu
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        m = re.search(r'_(\d+)_(\d+)\.html$', os.path.basename(cp))
        if not m or m.group(1) == "0": continue      # lesson pages only
        g_l = menu_of(hp, True); c_l = menu_of(cp, False)
        if not g_l: continue
        share = sum(1 for t in g_l if t in g_ov) / len(g_l)
        kind = ("gold REPEATS the overview menu" if share >= 0.8 else
                "gold menu partly the overview's" if share >= 0.4 else "gold menu is the lesson's own")
        cl = "claude EMPTY" if not c_l else ("claude repeats too" if sum(1 for t in c_l if t in c_ov) / len(c_l) >= 0.8 else "claude has its own")
        bucket["%-34s | %s" % (kind, cl)] += 1
        byfam[fam_of.get(code, "?")]["%s|%s" % (kind[:12], cl)] += 1
        rows.append((code, os.path.basename(cp), kind, cl, len(g_l), len(c_l)))
        if kind.startswith("gold REPEATS") and cl == "claude EMPTY":
            mods.setdefault(code, []).append(os.path.basename(cp))
print("paired LESSON pages of modules with a substantial gold overview menu: %d" % len(rows))
for k, v in bucket.most_common(): print("   %-70s %4d" % (k, v))
print("\nby template family:")
for fam, c in sorted(byfam.items()): print("   %-14s %s" % (fam, dict(c.most_common(4))))
print("\nTHE CLASS — gold repeats the overview menu, Claude's lesson menu is EMPTY: %d pages / %d modules" % (sum(len(v) for v in mods.values()), len(mods)))
for code, ps in sorted(mods.items(), key=lambda kv: -len(kv[1])):
    print("   %-10s %2d pages  (%s)" % (code, len(ps), fam_of.get(code, "?")))
