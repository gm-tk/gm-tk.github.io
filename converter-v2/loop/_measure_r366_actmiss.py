#!/usr/bin/env python3
"""r366 PICK decomposition (session 21, Round 3) — the DIFF MINER's activity rows #534 (MISSING `p`, 677 pages) and #539
(MISSING `h3`, 342 pages) decomposed BY MECHANISM. For every paired page (the gate's own pairing + skeleton via
_diff_miner.page_lines): every gold skeleton line in the `activity` region whose tag is p / h3 / h4 / ul / ol and whose text
has NO source among Claude's skeleton lines of the page — where is that text on Claude's page?
  visible-elsewhere  : a Claude skeleton line carries it (a MOVED / alignment diff, not a miss)
  in-capture         : inside a cv2-interactive block (the widget ate it)
  in-widget-or-note  : in Claude's HTML but in no skeleton line and no capture (a built widget's inside, or a Writers Note)
  absent-in-wt       : not on Claude's page at all, but the WT has it (derivable, lost)
  not-in-wt          : not on Claude's page and not in the WT (class C)
plus whether the gold line is the FIRST element of its box (a title / lead) or later. Aggregated by (tag, location, first),
by template, by module. Writes _r366_actmiss.{json,log}."""
import os, re, sys, json, io, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
for p in (HERE, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
from _diff_miner import page_lines
from _measure_ceiling import wt_blob, has_source, unorm, load_meta

TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")
def captures_blob(html):
    out = []
    for m in re.finditer(r'<div class="cv2-interactive[^"]*"[^>]*>', html):
        depth = 1; pos = m.end()
        for t in TAG.finditer(html, m.end()):
            if t.group(2).lower() != "div": continue
            depth += -1 if t.group(1) else 1
            if depth == 0: pos = t.start(); break
        out.append(re.sub(r"<[^>]+>", " ", html[m.end():pos]))
    return " " + unorm(" \n ".join(out)) + " "

meta = load_meta()
rows = []; skipped = 0
codes = sorted(_corpus.gate_mods(CLAUDE))
for ci, code in enumerate(codes):
    try: wt = (wt_blob(code) or ("",))[0]
    except Exception: wt = ""
    m = meta.get(code) or {}
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        try:
            g, _gm = page_lines(hp); c, _cm = page_lines(cp)
        except Exception:
            skipped += 1; continue
        cskel = " " + unorm(" \n ".join(l.text for l in c if l.text and l.sig != "WIDGET")) + " "
        craw_html = io.open(cp, encoding="utf-8", errors="replace").read()
        craw_html = re.sub(r"<!--.*?-->", "", craw_html, flags=re.S)
        craw = " " + unorm(re.sub(r"<[^>]+>", " ", craw_html)) + " "
        ccap = captures_blob(craw_html)
        in_box = False; first_pending = False
        for l in g:
            sig = l.sig or ""
            if sig.startswith("div.activity") or sig.startswith("div#") and ".activity" in sig:
                in_box = True; first_pending = True; continue
            if l.region != "activity": in_box = False; continue
            tag = re.split(r"[#.\[]", sig)[0]
            if tag in ("div", "span", "WIDGET", "table", "tr", "td", "th", "tbody", "thead", "img", "a", "b", "i", "strong", "em", "br"):
                if tag == "WIDGET": first_pending = False
                continue
            if tag not in ("p", "h3", "h4", "h2", "ul", "ol", "li"): continue
            first = first_pending; first_pending = False
            t = unorm(l.text or "")
            if not t or len(t.split()) < 2: continue
            if has_source(t, cskel): loc = "visible-elsewhere"
            elif has_source(t, ccap): loc = "in-capture"
            elif has_source(t, craw): loc = "in-widget-or-note"
            elif wt and has_source(t, wt): loc = "absent-in-wt"
            else: loc = "not-in-wt"
            if loc == "visible-elsewhere": continue
            rows.append({"module": code, "page": os.path.basename(cp), "gold": os.path.basename(hp), "tag": tag, "first": first, "loc": loc,
                         "text": (l.text or "")[:90], "template": m.get("template_type", "?"), "subject": m.get("subject", "?")})
    if ci % 50 == 0: print(f"  … {ci}/{len(codes)} modules, {len(rows)} rows", flush=True)
json.dump(rows, io.open(os.path.join(HERE, "_r366_actmiss.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
P(f"gold activity-region p/h lines with no source in Claude's skeleton: {len(rows)} (pairs skipped {skipped})")
def agg(rs, key):
    d = collections.defaultdict(lambda: [0, set(), set()])
    for r in rs:
        k = key(r); d[k][0] += 1; d[k][1].add(r["module"] + "/" + r["page"]); d[k][2].add(r["module"])
    return sorted(((k, v[0], len(v[1]), len(v[2])) for k, v in d.items()), key=lambda x: -x[1])
P("\nBY (tag, location, first-in-box): lines / pages / modules")
for k, n, pg, md in agg(rows, lambda r: (r["tag"], r["loc"], "FIRST" if r["first"] else "later")): P(f"  {str(k):50} {n:5} / {pg:4} / {md:3}")
P("\nBY location: lines / pages / modules")
for k, n, pg, md in agg(rows, lambda r: r["loc"]): P(f"  {k:22} {n:5} / {pg:4} / {md:3}")
for loc in ("in-capture", "absent-in-wt", "in-widget-or-note"):
    sub = [r for r in rows if r["loc"] == loc]
    P(f"\n== {loc}: by template (lines / pages / modules)")
    for k, n, pg, md in agg(sub, lambda r: r["template"]): P(f"  {k:14} {n:5} / {pg:4} / {md:3}")
    P(f"   by tag+first:", agg(sub, lambda r: (r["tag"], "FIRST" if r["first"] else "later"))[:6])
    P(f"   top modules:", agg(sub, lambda r: r["module"])[:15])
    P(f"   examples:", [(r["module"], r["page"], r["tag"], r["text"][:50]) for r in sub[:6]])
io.open(os.path.join(HERE, "_r366_actmiss.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
