#!/usr/bin/env python3
"""Session 34 Round 2 PICK measurement — THE INQUIRY SHELL COMPLETENESS CENSUS (queue rows #4158 body MISSING div.inquiryPanel 37 / 34,
#9363 root body.inquiry 27 / 26, #435 crumbs MISSING 21 / 18, #4178 / #4231 the panel's inner row).
For every gold page that carries the inquiry shell (div.crumbs + div.inquiryPanel), find the paired Claude page (same module; the gold's
single page ↔ Claude's page 0 unless Claude split the module) and count: gold crumb items / panels, Claude crumb items / panels, the
<body> class on both, and what the WT offers ([Tab N] openers: labelled / empty; a `[Side tab navigation]`; a crumb LIST vs repeated labels).
Buckets:
  SHELL-OK        Claude has crumbs + the same panel count
  PANELS-DIFF     Claude has the shell but a different panel count
  SHELL-MISSING   gold has the shell, Claude has none (the r100 `_bllInquiry` never fired)
  SPLIT           Claude built several pages against the gold's one
Run under WSL: python3 _s34_r2_inqshell.py
"""
import re, os, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
rows = []
for gdir in sorted(glob.glob(R + "01-Finalized_Modules_/*/*/")):
    code = os.path.basename(gdir.rstrip("/"))
    tmpl = gdir.rstrip("/").split("/")[-2]
    gpages = [p for p in sorted(glob.glob(gdir + "*.html")) if "acks" not in os.path.basename(p).lower()]
    shell_pages = []
    for p in gpages:
        h = open(p, encoding="utf-8", errors="replace").read()
        if 'class="crumbs"' in h or "inquiryPanel" in h:
            shell_pages.append((p, h))
    if not shell_pages: continue
    cdir = (glob.glob(R + "01-Claude_Modules_/*/" + code + "/") or [None])[0]
    cpages = sorted(glob.glob(cdir + "*.html")) if cdir else []
    cpages = [p for p in cpages if "acks" not in os.path.basename(p).lower()]
    wt = ""
    for t in glob.glob(gdir + "*parsed.txt"):
        if "Writers" in t or "writers" in t or len(glob.glob(gdir + "*parsed.txt")) == 1: wt += open(t, encoding="utf-8", errors="replace").read()
    tabs = re.findall(r'\[\s*tab\s*(\d+)\s*\]\s*\[/RED TEXT\]\s*🔴?\s*([^\n]*)', wt, re.I)
    labelled = sum(1 for _, t in tabs if t.strip()); empty = sum(1 for _, t in tabs if not t.strip())
    sidetab = "[Side tab navigation]" in wt or "side tab" in wt.lower()
    for p, h in shell_pages:
        gcr = len(re.findall(r'<div class="crumbs"', h)); gitems = len(re.findall(r'class="crumbs".*?</div>\s*</div>', h, re.S))
        gcrumb_items = 0
        m = re.search(r'<div class="crumbs"[^>]*>(.*?)</div>\s*(?:<div class="inquiryPanel|<div class="row)', h, re.S)
        if m: gcrumb_items = len(re.findall(r'<div\b', m.group(1)))
        gpan = len(re.findall(r'class="inquiryPanel', h))
        gbody = (re.search(r'<body[^>]*class="([^"]*)"', h) or [None, ""])[1]
        # pair: Claude page — if Claude has one page, it; else the page whose stem matches
        gname = os.path.basename(p)
        if len(cpages) == 1: cp = cpages[0]
        else:
            cp = None
            stemg = re.sub(r'[-_.]', '', gname.replace(".html", "").replace(code, ""))
            for c in cpages:
                stemc = re.sub(r'[-_.]', '', os.path.basename(c).replace(".html", "").replace(code, ""))
                if stemc == stemg or (stemg == "" and stemc == "00"): cp = c; break
            if cp is None and cpages: cp = cpages[0]
        if not cp:
            rows.append((tmpl, code, gname, "NO-CLAUDE", gcrumb_items, gpan, 0, 0, gbody, "", len(cpages), labelled, empty, sidetab)); continue
        ch = open(cp, encoding="utf-8", errors="replace").read()
        ccr = len(re.findall(r'<div class="crumbs"', ch)); cpan = len(re.findall(r'class="inquiryPanel', ch))
        m = re.search(r'<div class="crumbs"[^>]*>(.*?)</div>\s*(?:<div class="inquiryPanel|<div class="row)', ch, re.S)
        ccrumb_items = len(re.findall(r'<div\b', m.group(1))) if m else 0
        cbody = (re.search(r'<body[^>]*class="([^"]*)"', ch) or [None, ""])[1]
        if len(cpages) > 1 and len(gpages) == 1: b = "SPLIT"
        elif cpan == 0 and ccr == 0: b = "SHELL-MISSING"
        elif cpan == gpan: b = "SHELL-OK"
        else: b = "PANELS-DIFF"
        rows.append((tmpl, code, gname, b, gcrumb_items, gpan, ccrumb_items, cpan, gbody, cbody, len(cpages), labelled, empty, sidetab))
cnt = collections.Counter(r[3] for r in rows)
print("gold pages with the inquiry shell:", len(rows), dict(cnt))
print("by template:", {t: dict(collections.Counter(r[3] for r in rows if r[0] == t)) for t in sorted(set(r[0] for r in rows))})
print("\n%-12s %-9s %-22s %-14s gold(cr/pan) claude(cr/pan) gbody/cbody           cpages WT[Tab] lab/emp side" % ("template", "code", "gold page", "bucket"))
for r in rows:
    print("%-12s %-9s %-22s %-14s %2d/%-2d        %2d/%-2d        %-22s %2d     %2d/%-2d   %s" % (r[0], r[1], r[2][:22], r[3], r[4], r[5], r[6], r[7], (r[8] + "|" + r[9])[:22], r[10], r[11], r[12], "Y" if r[13] else ""))
miss = [r for r in rows if r[3] == "SHELL-MISSING"]
print("\nSHELL-MISSING by WT shape:", dict(collections.Counter(("labelled" if r[11] >= 2 and r[12] < 2 else "empty" if r[12] >= 2 else "no-tabs") for r in miss)))
print("SHELL-MISSING body class:", dict(collections.Counter(r[9] for r in miss)))
print("SHELL-OK body class:", dict(collections.Counter(r[9] for r in rows if r[3] == "SHELL-OK")))
