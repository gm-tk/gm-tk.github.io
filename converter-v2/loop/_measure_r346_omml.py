#!/usr/bin/env python3
"""_measure_r346_omml.py — ROUND 346 (the autonomous loop, session 12 — Chris's D10-7: Word equations → MathML).
For EVERY gold dir (all 454; the combined `Writers Template + Media List.docx` counts — the r313 filename trap):
  * OMML in the writer's docx: m:oMathPara (a display equation paragraph) and m:oMath (an equation) counts, how many
    oMath sit INSIDE an oMathPara (block) vs beside w:r runs in a w:p (inline), and the OMML element vocabulary;
  * the gold's <math> elements per page: count and the display attribute split (bare / inline / block), plus the
    `mathJax` body-class carriers;
  * the Claude pages' <math> count (expected 0 before the round) and mathJax carriers.
Paths are dynamic (CLAUDE.md §13). Run from anywhere under WSL:  python3 _measure_r346_omml.py
Writes _r346_omml.json next to itself and prints the summary.
"""
import os, re, sys, json, zipfile, collections
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from anchor_compare import CLAUDE, HUMAN

OMATHPARA = re.compile(r"<m:oMathPara\b.*?</m:oMathPara>", re.S)
OMATH = re.compile(r"<m:oMath\b[^>]*>.*?</m:oMath>", re.S)
MEL = re.compile(r"<m:([A-Za-z]+)\b")
MATH = re.compile(r"<math\b([^>]*)>", re.I)

def docx_xml(path):
    try:
        with zipfile.ZipFile(path) as z: return z.read("word/document.xml").decode("utf-8", "replace")
    except Exception as e: return ""

def main():
    rows = []; tot = collections.Counter(); vocab = collections.Counter(); gold_disp = collections.Counter(); byT = collections.defaultdict(collections.Counter)
    for code in _corpus.mods(HUMAN):
        gdir = _corpus.mdir(HUMAN, code)
        if not gdir or not os.path.isdir(gdir): continue
        tmpl = os.path.basename(os.path.dirname(gdir))
        docs = [f for f in os.listdir(gdir) if f.lower().endswith(".docx") and not f.startswith("~")]
        wt = [f for f in docs if re.search(r"writers? template", f, re.I)] or docs
        n_para = n_math = n_block = n_inline = 0; v = collections.Counter()
        for f in wt:
            xml = docx_xml(os.path.join(gdir, f))
            if not xml: continue
            paras = OMATHPARA.findall(xml); n_para += len(paras)
            inpara = sum(len(OMATH.findall(p)) for p in paras)
            allm = len(OMATH.findall(xml)); n_math += allm; n_block += inpara; n_inline += allm - inpara
            for m in MEL.findall(xml): v[m] += 1
        # gold pages
        g_math = 0; g_disp = collections.Counter(); g_mj = 0; g_pages = 0
        for f in os.listdir(gdir):
            if not f.lower().endswith(".html"): continue
            h = open(os.path.join(gdir, f), encoding="utf-8", errors="replace").read()
            ms = MATH.findall(h); g_math += len(ms); g_pages += 1 if ms else 0
            for a in ms:
                d = re.search(r'display\s*=\s*"([^"]*)"', a); g_disp[d.group(1) if d else "bare"] += 1
            if re.search(r'<body class="[^"]*\bmathJax\b', h): g_mj += 1
        cdir = _corpus.mdir(CLAUDE, code); c_math = 0; c_mj = 0
        if cdir and os.path.isdir(cdir):
            for f in os.listdir(cdir):
                if not f.lower().endswith(".html"): continue
                h = open(os.path.join(cdir, f), encoding="utf-8", errors="replace").read()
                c_math += len(MATH.findall(h)); c_mj += 1 if re.search(r'<body class="[^"]*\bmathJax\b', h) else 0
        if n_math or g_math or c_math:
            rows.append({"code": code, "tmpl": tmpl, "wt_docx": wt, "omath": n_math, "omathpara": n_para, "block": n_block, "inline": n_inline,
                         "vocab": dict(v), "gold_math": g_math, "gold_math_pages": g_pages, "gold_display": dict(g_disp), "gold_mathjax_pages": g_mj,
                         "claude_math": c_math, "claude_mathjax_pages": c_mj})
            tot["wt_modules"] += 1 if n_math else 0; tot["omath"] += n_math; tot["block"] += n_block; tot["inline"] += n_inline
            tot["gold_math"] += g_math; tot["claude_math"] += c_math; vocab.update(v); gold_disp.update(g_disp)
            if n_math: byT[tmpl]["modules"] += 1; byT[tmpl]["omath"] += n_math
    summary = {"modules_with_omml": tot["wt_modules"], "omath_total": tot["omath"], "block(oMathPara)": tot["block"], "inline(beside runs)": tot["inline"],
               "by_template": {k: dict(v) for k, v in byT.items()}, "omml_vocabulary": dict(vocab.most_common()),
               "gold_math_total": tot["gold_math"], "gold_display_split": dict(gold_disp), "claude_math_total": tot["claude_math"],
               "omml_modules": sorted([r["code"] for r in rows if r["omath"]], key=lambda c: -next(r["omath"] for r in rows if r["code"] == c))}
    json.dump({"summary": summary, "rows": rows}, open(os.path.join(HERE, "_r346_omml.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for r in sorted(rows, key=lambda r: -r["omath"]):
        if r["omath"] or r["gold_math"]:
            print(f"  {r['tmpl']:12s} {r['code']:9s} omath {r['omath']:4d} (block {r['block']:3d} / inline {r['inline']:3d})  gold <math> {r['gold_math']:4d} on {r['gold_math_pages']} pages {r['gold_display']}  mathJax pages {r['gold_mathjax_pages']}  claude <math> {r['claude_math']}")

if __name__ == "__main__":
    main()
