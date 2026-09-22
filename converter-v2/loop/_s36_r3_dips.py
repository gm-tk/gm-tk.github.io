#!/usr/bin/env python3
"""Session 36 Round 3 — name the r435 dips: for each named page, print the text elements that MOVED out of Claude's menu
(disk menu -> ON body) and say where the GOLD has each one. Run under WSL: python3 _s36_r3_dips.py CODE/PAGE.html …"""
import re, os, sys, glob, html
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
ON = os.path.join(HERE, "_s36_r435_on")
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
ELEM = re.compile(r'<(p|h[1-6]|li)\b([^>]*)>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
def elems(h): return [(m.group(1), norm(m.group(3)), plain(m.group(3))) for m in ELEM.finditer(h)]
def split_gold(g):
    for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
        i = g.find(mark)
        if i > 0: return g[:i], g[i:]
    return g, ""
def menu_body(p, is_gold):
    s = open(p, encoding="utf-8", errors="replace").read()
    if is_gold: return split_gold(s)
    i = s.find('<div id="body">')
    return (s[:i], s[i:]) if i > 0 else ("", s)
for spec in sys.argv[1:]:
    code, page = spec.split("/")
    hp = next((h for n, c, h in pairs(code) if os.path.basename(c) == page), None)
    cp = next((c for n, c, h in pairs(code) if os.path.basename(c) == page), None)
    onp = os.path.join(ON, code, page)
    if not (hp and cp and os.path.exists(onp)): print("%s: missing (%s)" % (spec, onp)); continue
    dm, db = menu_body(cp, False); om, ob = menu_body(onp, False); gm, gb = menu_body(hp, True)
    dmt = {e[1]: e for e in elems(dm)}; omt = {e[1] for e in elems(om)}
    gmt = {e[1] for e in elems(gm)}; gbt = {e[1] for e in elems(gb)}
    moved = [e for t, e in dmt.items() if t not in omt and len(t) >= 12]
    print("=== %s  (menu elements disk %d -> ON %d; gold %d)" % (spec, len(elems(dm)), len(elems(om)), len(elems(gm))))
    for tag, t, txt in moved:
        gw = "MENU" if t in gmt else ("body" if t in gbt else "absent")
        print("    moved out of the menu: %-4s gold=%-6s  %s" % (tag, gw, txt[:88]))
    if not moved: print("    (nothing left the menu — the dip is elsewhere: compare the body order)")
