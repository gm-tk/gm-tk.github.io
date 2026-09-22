#!/usr/bin/env python3
"""Session 36 Round 3 PICK measurement — THE `[Body]` LEAD-IN INSIDE A LESSON-MENU REGION.
The lesson menu's section-stop treats a `[Body]` tag as menu-safe (menu.lesson_menu_section_stop.menu_section_safe_tags), so a
`[Body] "Welcome to Lesson N…"` paragraph that follows the WALT / SC block is carried into #module-menu-content. Question: what does
the GOLD do with the text of such a `[Body]` tag — menu or body?

For every paired LESSON page: walk the WT's lesson section; find the `[Lesson Overview]` / `[Overview]` / implicit block; for each
`[Body]`-tagged run INSIDE the block's span (i.e. before the block's terminating heading), locate its text on the gold page and
report menu / body / absent, split by whether the run is BEFORE the first WALT lead line or AFTER the last list line ("the tail").
Also report where Claude put it. Run under WSL: python3 _s36_r3_bodylead.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
RED = re.compile(r'\U0001f534\[RED TEXT\](.*?)\[/RED TEXT\]\U0001f534', re.S)
LESSON_RE = re.compile(r'\[\s*(?:lesson|page)\s*(\d+)\b[^\]]*\]', re.I)
WALT_RE = re.compile(r'^\s*(?:we are learning|i can|you will show|success criteria|learning intentions|ng[āa] whāinga)', re.I)
def split_gold(g):
    for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
        i = g.find(mark)
        if i > 0: return g[:i], g[i:]
    return g, ""
def where(text, page, is_gold):
    t = norm(text)[:40]
    if len(t) < 12: return "short"
    if is_gold: head, body = split_gold(page)
    else:
        i = page.find('<div id="body">'); head, body = (page[:i], page[i:]) if i > 0 else ("", page)
    if t in norm(head): return "menu"
    if t in norm(body): return "body"
    return "absent"
def wt_lesson_section(wt, n):
    starts = [(m.start(), int(m.group(1))) for m in LESSON_RE.finditer(wt)]
    idx = [i for i, (p, k) in enumerate(starts) if k == n]
    if not idx: return ""
    a = starts[idx[0]][0]
    b = next((p for p, k in starts[idx[0] + 1:] if k != n), len(wt))
    return wt[a:b]
stats = collections.Counter(); bypos = collections.Counter(); ex = collections.defaultdict(list); mods = collections.Counter()
pages = {}; waltlead = collections.Counter()
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    gdir = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    wt = ""
    for t in glob.glob(gdir + "*parsed.txt") if gdir else []:
        if "Writers" in t or "writers" in t: wt += open(t, encoding="utf-8", errors="replace").read()
    if not wt: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        m = re.search(r'_(\d+)_(\d+)\.html$', os.path.basename(cp))
        if not m or m.group(1) == "0": continue
        sec = wt_lesson_section(wt, int(m.group(1)))
        if not sec: continue
        lines = sec.splitlines()
        # the block: from the overview marker (or the first WALT line) to the first heading tag
        start = None; stop = len(lines)
        for i, l in enumerate(lines):
            if start is None and (re.search(r'\[\s*(?:lesson\s+)?overview\s*\]', l, re.I) or WALT_RE.match(re.sub(r'\U0001f534\[RED TEXT\].*?\[/RED TEXT\]\U0001f534', '', l))):
                start = i; continue
            if start is not None and re.search(r'\[\s*h[1-5]\s*\]|\[\s*title bar', l, re.I): stop = i; break
        if start is None: continue
        ch = open(cp, encoding="utf-8", errors="replace").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        seen_list = False
        for i in range(start, stop):
            l = lines[i]
            reds = list(RED.finditer(l))
            if not reds:
                if l.strip().startswith(("•", "-", "*")): seen_list = True
                continue
            tagtxt = " ".join(r.group(1) for r in reds).lower()
            if not re.search(r'\[\s*body\s*\]|\[\s*body text\s*\]', tagtxt): continue
            after = l[reds[-1].end():].strip()
            if len(norm(after)) < 12: continue
            gw = where(after, gh, True); cw = where(after, ch, False)
            pos = "tail (after the list)" if seen_list else "lead (before the list)"
            stats["gold=%s claude=%s" % (gw, cw)] += 1
            bypos["%-24s gold=%s claude=%s" % (pos, gw, cw)] += 1
            mods[code] += 1
            pages.setdefault((pos, gw, cw), set()).add(code + "/" + os.path.basename(cp))
            if WALT_RE.match(after): waltlead[(pos, gw, cw)] += 1
            k = "%s | gold=%s claude=%s" % (pos, gw, cw)
            if len(ex[k]) < 6: ex[k].append("%s %s: %s" % (code, os.path.basename(cp), after[:70]))
print("[Body]-tagged runs inside a lesson's overview block: %d (modules %d)" % (sum(stats.values()), len(mods)))
for k, v in stats.most_common(): print("   %-34s %4d" % (k, v))
print("by position in the block:")
for k, v in bypos.most_common(): print("   %-60s %4d" % (k, v))
print("PAGES per (position, gold, claude) — and how many of those runs THEMSELVES start with a WALT / SC lead line:")
for k in sorted(pages, key=lambda k: -len(pages[k])):
    print("   %-24s gold=%-6s claude=%-6s pages %3d  runs %3d  WALT-lead runs %d" % (k[0], k[1], k[2], len(pages[k]), bypos["%-24s gold=%s claude=%s" % k], waltlead[k]))
print("the pages that would MOVE (claude=menu today):")
for k in sorted(pages):
    if k[2] == "menu": print("   %-24s gold=%-6s : %s" % (k[0], k[1], " ".join(sorted(pages[k]))[:150]))
print("by module (top 20):")
for k, v in mods.most_common(20): print("   %-10s %d" % (k, v))
print("examples:")
for k, v in sorted(ex.items()):
    print("  " + k)
    for e in v: print("     " + e)
