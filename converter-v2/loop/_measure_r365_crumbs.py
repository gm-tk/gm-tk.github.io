#!/usr/bin/env python3
"""r365 PICK (session 21) — the CRUMBS completeness class (DIFF_QUEUE census: 27 pages / 23 modules with derivable misses).
For every gate module: every paired page's gold crumb labels (div.crumbs > div > p) vs Claude's; the gold dir's build shape
(a single-file inquiry build beside paged files = a DUAL BUILD the gate pairs by position); the WT dialect (labelled tab list,
empty [Tab N] openers, [page N] / [End page] counts, a 'Navigation with N sections' instruction, [section N] openers).
Writes _r365_crumbs.json + prints the per-module table for modules where either side has crumbs."""
import os, re, sys, json, io, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE

def rd(p): return io.open(p, encoding="utf-8", errors="replace").read()
CR = re.compile(r'<div class="crumbs[^"]*"[^>]*>(.*?)</div>\s*<div class="inquiryPanel', re.S | re.I)
CR2 = re.compile(r'<div class="crumbs[^"]*"[^>]*>(.*?)\n\s*</div>', re.S | re.I)
def crumbs(html):
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    m = CR.search(html) or CR2.search(html)
    if not m: return None
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip() for t in re.findall(r"<p[^>]*>(.*?)</p>", m.group(1), flags=re.S)]

def wt_text(code, gold_dir):
    for pat in ("*Writers Template_parsed.txt", "*Writer's Template_parsed.txt", "*Writers Template + Media List_parsed.txt", "*parsed.txt"):
        c = glob.glob(os.path.join(gold_dir, pat))
        if c: return rd(c[0])
    c = glob.glob(os.path.join(ROOT, "03-All_Parsed_Files", code + " *parsed.txt"))
    return rd(c[0]) if c else ""

def dialect(wt):
    tabs = re.findall(r"\[\s*tab\s*(\d+)\s*\][^\n]*?(?:\[/RED TEXT\]🔴)?\s*([^\n🔴\[]*)", wt, flags=re.I)
    labelled = sum(1 for n, lab in tabs if lab.strip())
    empty = sum(1 for n, lab in tabs if not lab.strip())
    pages = len(re.findall(r"\[\s*page\s*\d+\s*\]", wt, flags=re.I))
    endp = len(re.findall(r"\[\s*end page\s*\]", wt, flags=re.I))
    nav = len(re.findall(r"navigation with \d+ sections", wt, flags=re.I))
    sect = len(re.findall(r"\[\s*section\s*\d+", wt, flags=re.I))
    return {"tabs": len(tabs), "tabs_labelled": labelled, "tabs_empty": empty, "page_openers": pages, "end_page": endp, "nav_instruction": nav, "section_openers": sect}

rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    ps = list(pairs(code))
    if not ps: continue
    gold_dir = os.path.dirname(ps[0][2])
    ghtml = [os.path.basename(p) for p in glob.glob(os.path.join(gold_dir, "*.html")) if "claude" not in os.path.basename(p).lower()]
    paged = [f for f in ghtml if re.search(r"[-_.]\d+\.\d+\.html$", f)]
    single = [f for f in ghtml if f not in paged]
    per = []
    for n, cp, hp in ps:
        g = crumbs(rd(hp)); c = crumbs(rd(cp))
        if g is None and c is None: continue
        per.append({"n": n, "claude": os.path.basename(cp), "gold": os.path.basename(hp), "gold_crumbs": g, "claude_crumbs": c})
    if not per: continue
    wt = wt_text(code, gold_dir)
    d = dialect(wt)
    fam = os.path.normpath(gold_dir).split(os.sep)[-2]
    labels_in_wt = None
    gl = [x for p in per for x in (p["gold_crumbs"] or [])]
    if gl:
        norm = re.sub(r"[^a-z0-9]+", " ", wt.lower())
        labels_in_wt = sum(1 for x in gl if re.sub(r"[^a-z0-9]+", " ", x.lower()).strip() and re.sub(r"[^a-z0-9]+", " ", x.lower()).strip() in norm)
    rows.append({"module": code, "family": fam, "gold_html": len(ghtml), "gold_paged": len(paged), "gold_single": single,
                 "dual_build": bool(paged) and bool(single), "dialect": d, "pages": per,
                 "gold_crumb_total": len(gl), "labels_in_wt": labels_in_wt,
                 "claude_crumb_total": sum(len(p["claude_crumbs"] or []) for p in per)})
json.dump(rows, io.open(os.path.join(HERE, "_r365_crumbs.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"modules with crumbs on either side: {len(rows)}")
print("module      fam          goldHTML paged single dual | gold crumbs / in WT | claude | dialect")
for r in rows:
    d = r["dialect"]
    print(f"{r['module']:10} {r['family']:12} {r['gold_html']:3} {r['gold_paged']:3} {len(r['gold_single']):2} {'DUAL' if r['dual_build'] else '    '} | {r['gold_crumb_total']:3} / {str(r['labels_in_wt']):>4} | {r['claude_crumb_total']:3} | tabs {d['tabs']} (lab {d['tabs_labelled']} empty {d['tabs_empty']}) pages {d['page_openers']} endp {d['end_page']} nav {d['nav_instruction']} sect {d['section_openers']}")
    for p in r["pages"]:
        if (p["gold_crumbs"] or []) != (p["claude_crumbs"] or []):
            print(f"     {p['claude']} <-> {p['gold']}: gold {p['gold_crumbs']} | claude {p['claude_crumbs']}")
miss = [r for r in rows if r["gold_crumb_total"] > r["claude_crumb_total"]]
print("\nmodules where the gold has MORE crumbs than Claude:", len(miss), [r["module"] for r in miss])
print("of which DUAL-BUILD gold dirs:", [r["module"] for r in miss if r["dual_build"]])
