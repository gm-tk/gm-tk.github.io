#!/usr/bin/env python3
"""Session 36 Round 2 PICK — the menu-region OVERRUN read by content: for the named modules (argv), every paired page where a Claude
text element (>= 40 chars) sits BEFORE `<div id="body">` while the gold carries that text in its BODY — print the Claude menu
element (tag + text), the gold's element signature + innermost wrapper for the same text, and the WT line (with its tag) that
carries it. Run under WSL: python3 _s36_r2_overwhat.py ARFUN02 ARFUN03 ARFUN05 …"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
ELEM_RE = re.compile(r'<(p|h[1-6]|li)\b([^>]*)>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
def elems(h):
    out = []
    for m in ELEM_RE.finditer(h):
        cls = re.search(r'class="([^"]*)"', m.group(2))
        out.append((m.group(1) + ("." + cls.group(1).replace(" ", ".") if cls else ""), norm(m.group(3)), plain(m.group(3)), m.start()))
    return out
def split_gold(g):
    for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
        i = g.find(mark)
        if i > 0: return g[:i], g[i:]
    return g, ""
def wrapper_of(h, pos):
    head = h[:pos]
    opens = list(re.finditer(r'<div\b([^>]*)>', head)); closes = len(re.findall(r'</div>', head))
    depth = len(opens) - closes; chain = []
    for m in opens[-max(depth, 0):][-3:]:
        c = re.search(r'class="([^"]*)"', m.group(1)); i = re.search(r'id="([^"]*)"', m.group(1))
        chain.append(("#" + i.group(1) if i else "") + ("." + c.group(1).replace(" ", ".") if c else "div"))
    return " > ".join(chain)
RED = re.compile(r'\U0001f534\[RED TEXT\](.*?)\[/RED TEXT\]\U0001f534', re.S)
for code in sys.argv[1:]:
    try: pl = pairs(code)
    except Exception: print("%s: no pairs" % code); continue
    gdir = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    wt = ""
    for t in glob.glob(gdir + "*parsed.txt") if gdir else []:
        if "Writers" in t or "writers" in t: wt += open(t, encoding="utf-8", errors="replace").read()
    wtlines = wt.splitlines()
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        ch = open(cp, encoding="utf-8", errors="replace").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        i = ch.find('<div id="body">')
        if i < 0: continue
        ghead, gbody = split_gold(gh)
        gh_t = {e[1] for e in elems(ghead)}; gb = elems(gbody); gb_t = {e[1]: e for e in gb}
        over = [e for e in elems(ch[:i]) if len(e[1]) >= 40 and e[1] in gb_t and e[1] not in gh_t]
        if not over: continue
        print("=== %s %s  (Claude menu elements %d; over %d)" % (code, os.path.basename(cp), len(elems(ch[:i])), len(over)))
        for sig, t, txt, pos in over:
            g = gb_t[t]
            wr = wrapper_of(gbody, g[3])
            # the WT line carrying this text
            key = txt[:28].lower()
            wl = next((l for l in wtlines if key and key in re.sub(r'\s+', ' ', l).lower()), "")
            tag = " ".join(m.group(1).strip() for m in RED.finditer(wl))[:60]
            print("   claude %-10s %-58s | gold %-8s in %-45s | WT: %s" % (sig, txt[:58], g[0], wr[-45:], tag))
