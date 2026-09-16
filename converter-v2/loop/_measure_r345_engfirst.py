#!/usr/bin/env python3
"""_measure_r345_engfirst.py — ROUND 345 (the autonomous loop, session 12 — Chris's D10-2: the bilingual lesson-title pair is
ENGLISH FIRST in a Standard-template module; the MTK reoTranslate rule — Māori first — untouched).

For every paired LESSON page whose Claude header carries TWO `<h1><span>` title lines (the r316 lesson pair) and whose body
class is NOT reoTranslate: the two halves, which half carries a macron (`reo_detect "macron"`), the order Claude ships, and
the order the gold ships (its first `<h1><span>` fold-matched to a half). Classes: ENG-FIRST-ALREADY (the macron half is
second) / REO-FIRST (the macron half is first — the D10-2 swap population) / UNDECIDED (no half or both halves carry a macron
— the writer's order stands, recorded). Gold agreement per class. Bilingual (reoTranslate) pages listed for information only.

Paths are dynamic (CLAUDE.md §13). Run from anywhere under WSL:  python3 _measure_r345_engfirst.py [--all]
Writes _r345_engfirst.json next to itself and prints the summary.
"""
import os, re, sys, json, html, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE

H1 = re.compile(r"<h1><span>(.*?)</span></h1>", re.S)
TAG = re.compile(r"<[^>]+>")
MAC = re.compile(r"[āēīōūĀĒĪŌŪ]")

def plain(s): return html.unescape(TAG.sub("", s)).replace("*", "").strip()
def fold(s):
    s = unicodedata.normalize("NFKD", s); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s.lower())
def header(page):
    m = re.search(r'<div id="header".*?<div id="body"', page, re.S); return m.group(0) if m else page[:12000]

def main():
    scan_all = "--all" in sys.argv
    codes = _corpus.mods(CLAUDE) if scan_all else _corpus.gate_mods(CLAUDE)
    rows = []; C = collections.Counter(); byT = collections.defaultdict(collections.Counter); aff = set()
    for code in codes:
        cdir = _corpus.mdir(CLAUDE, code); tmpl = os.path.basename(os.path.dirname(cdir)) if cdir else "?"
        for n, cp, hp in pairs(code):
            if n == 0 or str(n).startswith("0."): continue
            ch = open(cp, encoding="utf-8", errors="replace").read()
            spans = [plain(x) for x in H1.findall(header(ch))]
            if len(spans) < 2: continue
            bil = bool(re.search(r'<body class="[^"]*\breoTranslate\b', ch))
            a, b = spans[0], spans[1]
            ma, mb = bool(MAC.search(a)), bool(MAC.search(b))
            cls = "REO-FIRST" if (ma and not mb) else ("ENG-FIRST-ALREADY" if (mb and not ma) else "UNDECIDED")
            gh = open(hp, encoding="utf-8", errors="replace").read()
            gs = [plain(x) for x in H1.findall(header(gh))]
            g1 = gs[0] if gs else ""
            gold_first = "a" if (g1 and fold(g1) == fold(a)) else ("b" if (g1 and fold(g1) == fold(b)) else ("other" if g1 else "none"))
            # after the D10-2 swap the first half would be: a (unchanged) unless REO-FIRST → b
            after_first = "b" if cls == "REO-FIRST" else "a"
            row = {"code": code, "tmpl": tmpl, "page": os.path.basename(cp), "gold": os.path.basename(hp), "bilingual": bil, "a": a[:80], "b": b[:80],
                   "macron_a": ma, "macron_b": mb, "class": cls, "gold_first": gold_first, "gold_h1": g1[:80],
                   "gold_agrees_now": gold_first == "a", "gold_agrees_after": gold_first == after_first}
            rows.append(row)
            if bil: C[("bilingual", cls, gold_first)] += 1; continue
            C[(tmpl, cls, gold_first)] += 1; byT[tmpl][cls] += 1
            if cls == "REO-FIRST": aff.add(code)
    tgt = [r for r in rows if not r["bilingual"]]
    summary = {"population": "all" if scan_all else "gate_mods", "two_span_lesson_pages": len(rows),
               "non_bilingual_pages": len(tgt), "swap_population(REO-FIRST)": sum(1 for r in tgt if r["class"] == "REO-FIRST"),
               "swap_modules": sorted(aff), "by_template_class": {k: dict(v) for k, v in byT.items()},
               "by_template_class_goldfirst": {" | ".join(k): v for k, v in sorted(C.items())},
               "gold_agrees_now(non-bilingual)": sum(1 for r in tgt if r["gold_agrees_now"]),
               "gold_agrees_after(non-bilingual)": sum(1 for r in tgt if r["gold_agrees_after"])}
    json.dump({"summary": summary, "rows": rows}, open(os.path.join(HERE, "_r345_engfirst.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if scan_all:
        open(os.path.join(HERE, "_affected_r345.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(sorted(aff)) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for r in tgt: print(f"  {r['tmpl']:12s} {r['page']:22s} {r['class']:18s} gold_first={r['gold_first']:6s} | {r['a'][:38]} | {r['b'][:38]} || G: {r['gold_h1'][:36]}")

if __name__ == "__main__":
    main()
