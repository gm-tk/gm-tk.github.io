#!/usr/bin/env python3
"""Session 35 Round 1 PICK measurement — WHICH PANEL IS MISSING on the PANELS-DIFF Inquiry pages (r429 corpus).
For every gold page carrying div.crumbs + div.inquiryPanel whose paired Claude page has the shell with a different
panel count: print the gold crumb labels and the Claude crumb labels side by side, mark the labels present on one side
only, and say whether the missing label's text exists in the module's parsed Writers Template.
Run under WSL: python3 _s35_r1_crumbdiff.py
"""
import re, os, glob, html, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"

def crumb_labels(h):
    m = re.search(r'<div class="crumbs"[^>]*>(.*?)</div>\s*(?:<div class="inquiryPanel|<div class="row|<div class="col)', h, re.S)
    if not m:
        return []
    inner = m.group(1)
    labs = []
    for d in re.findall(r'<div\b[^>]*>(.*?)</div>', inner, re.S):
        t = re.sub(r'<[^>]+>', ' ', d)
        t = html.unescape(re.sub(r'\s+', ' ', t)).strip()
        labs.append(t)
    return labs

def panel_titles(h):
    out = []
    for p in re.findall(r'<div class="inquiryPanel[^"]*"[^>]*>(.*?)(?=<div class="inquiryPanel|</body>)', h, re.S):
        m = re.search(r'<h[1-6][^>]*>(.*?)</h[1-6]>', p, re.S)
        t = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1)))).strip() if m else '(no heading)'
        out.append(t[:50])
    return out

def norm(s):
    return re.sub(r'[^a-z0-9āēīōū]+', '', s.lower())

rows = []
for gdir in sorted(glob.glob(R + "01-Finalized_Modules_/*/*/")):
    code = os.path.basename(gdir.rstrip("/"))
    gpages = [p for p in sorted(glob.glob(gdir + "*.html")) if "acks" not in os.path.basename(p).lower()]
    cdir = (glob.glob(R + "01-Claude_Modules_/*/" + code + "/") or [None])[0]
    if not cdir:
        continue
    cpages = [p for p in sorted(glob.glob(cdir + "*.html")) if "acks" not in os.path.basename(p).lower()]
    wt = ""
    for t in glob.glob(gdir + "*parsed.txt"):
        wt += open(t, encoding="utf-8", errors="replace").read()
    wtn = norm(wt)
    for gp in gpages:
        gh = open(gp, encoding="utf-8", errors="replace").read()
        if 'class="crumbs"' not in gh:
            continue
        gl = crumb_labels(gh)
        gpan = len(re.findall(r'<div class="inquiryPanel', gh))
        # pair: Claude page with the shell (single-file → page 0)
        cand = [(cp, open(cp, encoding="utf-8", errors="replace").read()) for cp in cpages]
        cand = [(cp, ch) for cp, ch in cand if 'class="crumbs"' in ch]
        if not cand:
            continue
        cp, ch = cand[0]
        cl = crumb_labels(ch)
        cpan = len(re.findall(r'<div class="inquiryPanel', ch))
        if gpan == cpan:
            continue
        gset = [norm(x) for x in gl]; cset = [norm(x) for x in cl]
        gonly = [x for x in gl if norm(x) not in cset]
        conly = [x for x in cl if norm(x) not in gset]
        print("=== %s  gold %d panels / Claude %d  (%s)" % (code, gpan, cpan, os.path.basename(gp)[:40]))
        print("   gold crumbs  : " + " | ".join(gl))
        print("   Claude crumbs: " + " | ".join(cl))
        for x in gonly:
            print("   GOLD-ONLY «%s» in WT: %s" % (x, "YES" if norm(x) and norm(x) in wtn else "no"))
        for x in conly:
            print("   CLAUDE-ONLY «%s»" % x)
        print("   gold panel titles  : " + " | ".join(panel_titles(gh)))
        print("   Claude panel titles: " + " | ".join(panel_titles(ch)))
        rows.append((code, gpan, cpan, gonly, conly))

print()
print("modules PANELS-DIFF:", len(rows))
c = collections.Counter()
for code, g, cc, go, co in rows:
    for x in go:
        c[norm(x)[:24]] += 1
print("gold-only crumb labels (normalised) by frequency:", c.most_common(20))
