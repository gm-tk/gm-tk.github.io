#!/usr/bin/env python3
"""Session 34 Round 2 — THE INQUIRY-SHELL DIALECT CENSUS over the SHELL-MISSING + PANELS-DIFF modules of _s34_r2_inqshell.log:
what delimits the gold's panels in each module's Writers Template? Counts per WT: [Tab N] (bare), [Tab N] <label> (black label after),
[Tab N: label] / [Tab N – label] (label inside the red span), [Page N], [Lesson N content], [End page]; the gold's crumb labels; and
whether each crumb label is found in the WT (derivable) and WHERE (a tab line / a page line / a lesson line / an [H2] line / elsewhere).
Run under WSL: python3 _s34_r2_inqdialects.py
"""
import re, os, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
MODS = "BLL240 BLL250 BLL260 CEDK401 CEDK501 CEDO201 CEDO204 CEDO402 CEDR101 CEDR201 CEDR203 CEDR301 CEDR302 CEDR401 CEDT102 CEDT104 CEDT201 CEDT202 CEDT203 CEDT204 CEDT207 CEDT208 CEDT301 CEDW201 CEDW303 TWHA905 TWHK901 TWHK902 TWHR905 TWHT903 CEDK102 CEDO202 CEDR204 TWHA902 TWHA904 TWHK907 TWHR907".split()
RED = re.compile(r'🔴\[RED TEXT\]\s*(.*?)\s*\[/RED TEXT\]🔴\s*([^\n]*)')
def norm(s): return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
summary = collections.Counter()
for code in MODS:
    gdir = (glob.glob(R + "01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    if not gdir: print(code, "no gold dir"); continue
    wts = sorted(glob.glob(gdir + "*parsed.txt"), key=lambda t: (0 if "Writers" in t else 1, len(t)))
    wt = open(wts[0], encoding="utf-8", errors="replace").read() if wts else ""
    # the gold's shell page: the one with the most inquiryPanels
    best = None
    for g in glob.glob(gdir + "*.html"):
        if "acks" in os.path.basename(g).lower(): continue
        h = open(g, encoding="utf-8", errors="replace").read()
        n = len(re.findall(r'class="inquiryPanel', h))
        if n and (best is None or n > best[1]): best = (g, n, h)
    if not best: print(code, "no shell page"); continue
    g, gpan, h = best
    labels = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<div[^>]*crumb="\d+"[^>]*>(.*?)</div>', h, re.S)]
    if not labels: labels = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<div class="crumbs">(.*?)</div>\s*<div class="inquiryPanel', h, re.S)]
    tabs_bare = tabs_black = tabs_inner = pages = lessons = endpages = 0
    tab_lines = {}
    for m in RED.finditer(wt):
        red, black = m.group(1), m.group(2).strip()
        r = red.strip()
        if re.match(r'^\[\s*tab\s*\d+\s*\]$', r, re.I):
            if black: tabs_black += 1; tab_lines[norm(black)] = "tab-black"
            else: tabs_bare += 1
        elif re.match(r'^\[\s*tab\s*\d+\b', r, re.I):
            tabs_inner += 1; lab = re.sub(r'^\[\s*tab\s*\d+\s*[:–\-]?\s*', '', r, flags=re.I).rstrip(']').strip(); tab_lines[norm(lab)] = "tab-inner"
            if black: tab_lines[norm(black)] = "tab-inner-black"
        elif re.match(r'^\[\s*page\s*\d+\s*\]$', r, re.I): pages += 1
        elif re.match(r'^\[\s*lesson\s*\d+\s*content\s*\]$', r, re.I): lessons += 1; tab_lines[norm(black)] = "lesson-black"
        elif re.match(r'^\[\s*end\s*page\s*\]$', r, re.I): endpages += 1
    h2s = [norm(m.group(2)) for m in RED.finditer(wt) if re.match(r'^\[\s*h[12]\s*\]$', m.group(1).strip(), re.I)]
    where = []
    for lab in labels:
        n = norm(lab)
        if not n: where.append("?"); continue
        if n in tab_lines: where.append(tab_lines[n])
        elif any(n == x or n in x for x in h2s): where.append("h2")
        elif n in norm(wt): where.append("text")
        else: where.append("ABSENT")
    placeholder = wt.count("Learning outcome/intention") >= 2
    kind = ("EMPTY-WT" if placeholder else
            "tab-inner" if tabs_inner >= 3 else
            "tab-black-repeat" if tabs_black >= 6 and tabs_bare < 2 else
            "page-h2" if pages >= 3 and tabs_bare + tabs_black + tabs_inner == 0 else
            "lesson" if lessons >= 3 and tabs_bare + tabs_black + tabs_inner == 0 else
            "mixed")
    summary[kind] += 1
    print(f"{code:8s} {kind:16s} gold panels {gpan:2d}  WT: tab-bare {tabs_bare:2d} tab-black {tabs_black:2d} tab-inner {tabs_inner:2d} page {pages:2d} lesson {lessons:2d} endpage {endpages:2d} | labels {len(labels)}: {'/'.join(where)}")
    print(f"           crumbs: {' | '.join(labels)[:150]}")
print("\nby dialect:", dict(summary))
