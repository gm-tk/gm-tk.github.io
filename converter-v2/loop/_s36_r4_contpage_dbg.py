#!/usr/bin/env python3
"""Session 36 Round 4 PICK measurement — THE LESSON CONTINUATION PAGE'S MENU. A writer splits one lesson across several pages
(`[Lesson 3.0] Tools`, `[Lesson 3.1] … continued`): the lesson's `[Lesson Overview]` block sits at the start of the lesson, so
Claude fills the menu on the lesson's FIRST page and leaves every continuation page's menu empty. KB 01B: a lesson page's
simplified menu IS that lesson's overview block — and a continuation page is part of the same lesson.
For every paired page whose Claude filename has a non-zero PART (`_N_M` with M >= 1): compare the gold's menu with the gold menu
of that lesson's FIRST page (`_N_0`), and report what Claude has on each. Run under WSL: python3 _s36_r4_contpage.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
ELEM = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
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
tab = collections.Counter(); mods = collections.defaultdict(list); ex = collections.defaultdict(list)
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    byname = {os.path.basename(cp): (cp, hp) for n, cp, hp in pl}
    for name, (cp, hp) in sorted(byname.items()):
        m = re.search(r'_(\d+)_(\d+)\.html$', name)
        if not m: continue
        lesson, part = int(m.group(1)), int(m.group(2))
        if lesson == 0 or part == 0: continue                       # continuation pages only
        first = re.sub(r'_(\d+)_(\d+)\.html$', "_%d_0.html" % lesson, name)
        if first not in byname: continue
        g_first = set(menu_of(byname[first][1], True))
        if len(g_first) < 3: continue                               # the lesson's first page has no menu to inherit
        g_c = menu_of(hp, True); c_c = menu_of(cp, False)
        if not g_c:
            tab["gold continuation menu EMPTY too"] += 1; print("   GOLD-EMPTY:", code, name); continue
        share = sum(1 for t in g_c if t in g_first) / len(g_c)
        kind = ("gold REPEATS the lesson's menu" if share >= 0.8 else
                "gold PARTLY" if share >= 0.4 else "gold has a DIFFERENT menu")
        cl = "claude EMPTY" if not c_c else "claude has one"
        tab["%-30s | %s" % (kind, cl)] += 1
        if kind.startswith("gold REPEATS") and cl == "claude EMPTY":
            mods[code].append(name)
        if len(ex[kind + "|" + cl]) < 5: ex[kind + "|" + cl].append("%s %s" % (code, name))
print("paired CONTINUATION pages (part >= 1) whose lesson's first page has a gold menu: %d" % sum(tab.values()))
for k, v in tab.most_common(): print("   %-62s %4d" % (k, v))
print("\nTHE CLASS — the gold repeats the lesson's menu on the continuation page, Claude's is EMPTY: %d pages / %d modules"
      % (sum(len(v) for v in mods.values()), len(mods)))
for code, ps in sorted(mods.items(), key=lambda kv: -len(kv[1])): print("   %-10s %2d  %s" % (code, len(ps), " ".join(ps)[:90]))
print("\nexamples:")
for k, v in sorted(ex.items()): print("  %-46s %s" % (k, ", ".join(v)))
