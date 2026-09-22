#!/usr/bin/env python3
"""Session 36 Round 6 PICK measurement — WHICH MODULES carry the Inquiry family's `container-shift: panel -> free` loss
(2.31pp over 95 pages in the r436 loss ledger: content the gold holds inside a `div.inquiryPanel` that Claude renders as free
body). For every paired Inquiry-template page, count the gold's panels and Claude's, and report the pages where the gold has
panels and Claude has none (the shell never built) separately from those where both have panels but the content sits outside.
Run under WSL: python3 _s36_r6_panelfree.py"""
import re, os, sys, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
PANEL = re.compile(r'<div[^>]*class="[^"]*\b(?:inquiryPanel|fundamentalsPanel)\b', re.I)
CRUMB = re.compile(r'<div[^>]*class="[^"]*\bcrumbs\b|<div[^>]*\bcrumb="', re.I)
fam = {}
for d in glob.glob(ROOT + "/01-Finalized_Modules_/*/*/"): fam[os.path.basename(d.rstrip("/"))] = d.split("/")[-3]
noshell = collections.defaultdict(list); bothbut = collections.defaultdict(list); ok = 0
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        g = open(hp, encoding="utf-8", errors="replace").read(); c = open(cp, encoding="utf-8", errors="replace").read()
        gp = len(PANEL.findall(g)); cpn = len(PANEL.findall(c))
        if gp == 0: continue
        if cpn == 0: noshell[code].append((os.path.basename(cp), gp))
        elif abs(gp - cpn) >= 2: bothbut[code].append((os.path.basename(cp), gp, cpn))
        else: ok += 1
print("paired pages whose GOLD has panels: shells matched (within 1) %d" % ok)
print("\nA. the gold has panels, CLAUDE HAS NONE — the shell never built: %d pages / %d modules"
      % (sum(len(v) for v in noshell.values()), len(noshell)))
for code, ps in sorted(noshell.items(), key=lambda kv: -len(kv[1])):
    print("   %-10s %-14s %2d pages   %s" % (code, fam.get(code, "?"), len(ps), " ".join("%s(g%d)" % p for p in ps)[:86]))
print("\nB. both have panels but the COUNT differs by >= 2: %d pages / %d modules"
      % (sum(len(v) for v in bothbut.values()), len(bothbut)))
for code, ps in sorted(bothbut.items(), key=lambda kv: -len(kv[1]))[:20]:
    print("   %-10s %-14s %2d pages   %s" % (code, fam.get(code, "?"), len(ps), " ".join("%s(g%d/c%d)" % p for p in ps)[:80]))
