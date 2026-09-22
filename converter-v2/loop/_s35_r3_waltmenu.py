#!/usr/bin/env python3
"""Session 35 Round 3 — THE GOLD'S CONVENTION for a lesson page's WALT / SC block: over every paired LESSON page, where does
the GOLD put a WALT / SC lead-in element ("we are learning", "learning intentions", "you will show your understanding",
"how will i know", "i can", "success criteria", "we are learning about") — its MENU region or its BODY — and where does
Claude put it. Per template / subject. Run under WSL."""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
LEAD = re.compile(r'^(we are learning|learning intentions|you will show your understanding|how will i know|i can\b|success criteria|whainga ako|paearu angitu)', re.I)
def fold(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip().lower().replace("ā", "a").replace("ē", "e").replace("ī", "i").replace("ō", "o").replace("ū", "u")
def leads(h): return [fold(m.group(2)) for m in re.finditer(r'<(p|h[2-6]|li|b|strong)\b[^>]*>((?:(?!</?(?:p|h[2-6]|li)\b).)*?)</\1>', h, re.S) if LEAD.search(fold(m.group(2)))]
def split_gold(g):
    for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
        i = g.find(mark)
        if i > 0: return g[:i], g[i:]
    return g, ""
tot = collections.Counter(); bytpl = collections.defaultdict(collections.Counter); mods = collections.defaultdict(set)
for cdir in sorted(glob.glob(ROOT + "/01-Claude_Modules_/*/*/")):
    code = os.path.basename(cdir.rstrip("/")); tpl = cdir.rstrip("/").split("/")[-2]
    try: pl = pairs(code)
    except Exception: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        m = re.search(r'_(\d+)_(\d+)\.html$', os.path.basename(cp))
        if not m or m.group(1) == "0": continue
        gh = open(hp, encoding="utf-8", errors="replace").read(); ch = open(cp, encoding="utf-8", errors="replace").read()
        ghead, gbody = split_gold(gh)
        i = ch.find('<div id="body">'); chead, cbody = (ch[:i], ch[i:]) if i > 0 else ("", ch)
        g_menu, g_body = leads(ghead), leads(gbody); c_menu, c_body = leads(chead), leads(cbody)
        if not (g_menu or g_body): continue
        k = ("gold-menu" if g_menu and not g_body else "gold-body" if g_body and not g_menu else "gold-both")
        k2 = ("claude-menu" if c_menu and not c_body else "claude-body" if c_body and not c_menu else "claude-both" if c_menu else "claude-none")
        tot[(k, k2)] += 1; bytpl[tpl][(k, k2)] += 1; mods[(k, k2)].add(code)
print("lesson pages with a WALT / SC lead element on the gold page, by (gold region, Claude region):")
for k, v in tot.most_common(): print("  %-28s pages %4d  modules %3d" % (k, v, len(mods[k])))
for tpl, c in bytpl.items():
    print("  " + tpl + ": " + ", ".join("%s=%d" % ("/".join(k), v) for k, v in c.most_common()))
print("=== per PREFIX (letters of the code): gold-menu-only / gold-body-only / gold-both pages ===")
pref = collections.defaultdict(collections.Counter)
for (k, k2), s in mods.items():
    pass
# recompute per page with the prefix
pref = collections.defaultdict(collections.Counter)
for cdir in sorted(glob.glob(ROOT + "/01-Claude_Modules_/*/*/")):
    code = os.path.basename(cdir.rstrip("/"))
    try: pl = pairs(code)
    except Exception: continue
    px = re.match(r'[A-Za-z]+', code).group(0)
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        m = re.search(r'_(\d+)_(\d+)\.html$', os.path.basename(cp))
        if not m or m.group(1) == "0": continue
        gh = open(hp, encoding="utf-8", errors="replace").read()
        ghead, gbody = split_gold(gh)
        g_menu, g_body = leads(ghead), leads(gbody)
        if not (g_menu or g_body): continue
        pref[px]["menu" if g_menu and not g_body else "body" if g_body and not g_menu else "both"] += 1
for px, c in sorted(pref.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values()); print("  %-8s pages %4d  menu %.2f  body %.2f  both %.2f" % (px, t, c["menu"]/t, c["body"]/t, c["both"]/t))
