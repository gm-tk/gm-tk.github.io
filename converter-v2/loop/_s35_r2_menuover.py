#!/usr/bin/env python3
"""Session 35 Round 2 PICK measurement — THE MENU-REGION OVERRUN: a Claude text element (>= 40 chars) in the region BEFORE
`<div id="body">` whose text the paired GOLD page carries in its BODY (after the gold's own #body / the first inquiryPanel /
the first content row) and NOT in its own header region. Pairing: the gate's own (_discrepancy_audit.pairs). Run under WSL."""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def texts(h): return [norm(m.group(2)) for m in re.finditer(r'<(p|h[2-6]|li)\b[^>]*>((?:(?!</?(?:p|h[2-6]|li)\b).)*?)</\1>', h, re.S)]
def split_gold(g):
    for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
        i = g.find(mark)
        if i > 0: return g[:i], g[i:]
    return g, ""
per = collections.OrderedDict(); pages = 0; hit_pages = 0; hits = 0
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        ch = open(cp, encoding="utf-8", errors="replace").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        i = ch.find('<div id="body">')
        if i < 0: continue
        pages += 1
        ghead, gbody = split_gold(gh)
        gh_t = set(texts(ghead)); gb_t = set(texts(gbody))
        over = [t for t in texts(ch[:i]) if len(t) >= 40 and t in gb_t and t not in gh_t]
        if over:
            hit_pages += 1; hits += len(over); per.setdefault(code, []).append((os.path.basename(cp), len(over)))
print("paired pages %d; pages with a menu-region element the gold keeps in its BODY: %d; elements %d; modules %d" % (pages, hit_pages, hits, len(per)))
for code, items in sorted(per.items(), key=lambda kv: -sum(d for _, d in kv[1]))[:40]:
    print("  %-10s pages %2d  over %3d  e.g. %s" % (code, len(items), sum(d for _, d in items), ", ".join("%s %d" % (p[:20], d) for p, d in items[:3])))
