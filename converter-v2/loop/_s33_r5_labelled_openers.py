#!/usr/bin/env python3
"""Session 33 Round 5 PICK — the LABELLED-REPEATED-OPENER [Tab N] dialect, measured over every parsed Writers Template.
Shape: a crumb LIST of >= 3 labelled `[Tab N] <label>` lines, then panel OPENERS that repeat a list label (`[Tab 2] Silent b`) instead of
the r100 EMPTY `[Tab N]` opener. Reports per module: list labels, empty openers, repeated-label openers, other labelled tabs; the gold's
shell (crumbs / inquiryPanel / single page) and Claude's current shell. Usage (WSL): python3 _s33_r5_labelled_openers.py > _s33_r5_labelled_openers.log"""
import os, re, glob, unicodedata
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
TAB = re.compile("\[RED TEXT\]\s*\[\s*tab\s*(\d+)\s*\]\s*\[/RED TEXT\]\s*🔴?\s*(.*)$", re.I)
def fold(s):
    s = unicodedata.normalize("NFKD", s).lower()
    s = re.sub(r"[‘’'\"“”*_]", "", s); s = re.sub(r"\s+", " ", s).strip()
    return s
def shell(path):
    try: h = open(path, encoding="utf-8", errors="ignore").read()
    except Exception: return None
    return {"crumbs": h.count('class="crumbs"'), "panels": h.count("inquiryPanel"), "phases": h.count('class="phases"'),
            "body": (re.search(r'<body class="([^"]*)"', h) or [None, ""])[1]}
rows = []
for gd in sorted(glob.glob(R + "01-Finalized_Modules_/*/*/")):
    code = os.path.basename(gd.rstrip("/")); tmpl = gd.rstrip("/").split("/")[-2]
    wts = [p for p in glob.glob(gd + "*_parsed.txt") if "Writers Template" in os.path.basename(p)]
    if not wts: continue
    lines = []
    for p in wts: lines += open(p, encoding="utf-8", errors="ignore").read().split("\n")
    tabs = []
    for i, l in enumerate(lines):
        m = TAB.search(l)
        if m: tabs.append((i, int(m.group(1)), fold(m.group(2))))
    if len(tabs) < 3: continue
    # the crumb list = the leading run of labelled tabs with ascending N (allow one repeat)
    lst = []
    for i, n, lab in tabs:
        if lab and (not lst or n > lst[-1][1]): lst.append((i, n, lab))
        else: break
    if len(lst) < 3: continue
    rest = tabs[len(lst):]
    empty = [t for t in rest if not t[2]]
    labs = [x[2] for x in lst]
    def matches(lab):
        return any(lab == L or (len(lab) >= 3 and (lab in L or L in lab)) for L in labs)
    rep = [t for t in rest if t[2] and matches(t[2])]
    other = [t for t in rest if t[2] and not matches(t[2])]
    gh = sorted(glob.glob(gd + "*.html")); cd = R + f"01-Claude_Modules_/{tmpl}/{code}/"
    ch = sorted(glob.glob(cd + "*.html"))
    gs = shell(gh[0]) if gh else None; cs = shell(ch[0]) if ch else None
    rows.append((code, tmpl, len(lst), len(empty), len(rep), len(other), len(gh), len(ch), gs, cs))
print("modules with a labelled [Tab N] crumb list (>= 3):", len(rows))
print("\n== the DIALECT: list >= 3, EMPTY openers < 2, repeated-label openers >= 2")
cand = [r for r in rows if r[3] < 2 and r[4] >= 2]
for r in sorted(cand):
    code, tmpl, nl, ne, nr, no, ng, nc, gs, cs = r
    print(f"  {code:8s} {tmpl:11s} list {nl:2d} empty {ne} repeated {nr:2d} other {no:2d} | gold {ng:2d} pages crumbs={gs['crumbs'] if gs else '-'} panels={gs['panels'] if gs else '-'} body={gs['body'][:28] if gs else '-'} | Claude {nc:2d} pages crumbs={cs['crumbs'] if cs else '-'} panels={cs['panels'] if cs else '-'}")
print("\n== by template:", {t: sum(1 for r in cand if r[1] == t) for t in set(r[1] for r in cand)})
print("== gold single-page with crumbs among them:", sum(1 for r in cand if r[6] == 1 and r[8] and r[8]["crumbs"]), "/ Claude already with crumbs:", sum(1 for r in cand if r[9] and r[9]["crumbs"]))
print("\n== the r100 form for comparison: list >= 3 and EMPTY openers >= 2")
for r in sorted(rows):
    code, tmpl, nl, ne, nr, no, ng, nc, gs, cs = r
    if ne >= 2: print(f"  {code:8s} {tmpl:11s} list {nl:2d} empty {ne:2d} repeated {nr:2d} other {no:2d} | gold {ng:2d}p crumbs={gs['crumbs'] if gs else '-'} | Claude {nc:2d}p crumbs={cs['crumbs'] if cs else '-'}")
print("\n== the rest (list >= 3, no dialect match):")
for r in sorted(rows):
    code, tmpl, nl, ne, nr, no, ng, nc, gs, cs = r
    if ne < 2 and nr < 2: print(f"  {code:8s} {tmpl:11s} list {nl:2d} empty {ne} repeated {nr} other {no:2d} | gold {ng:2d}p crumbs={gs['crumbs'] if gs else '-'} | Claude {nc:2d}p crumbs={cs['crumbs'] if cs else '-'}")
