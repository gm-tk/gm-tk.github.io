#!/usr/bin/env python3
"""_measure_r347_tables.py — ROUND 347 (Chris's D10-5: the KB 05D table form).
Over every gold page and every Claude page (gate_mods population; --all for every dir), outside hand-off boxes
(cv2-interactive subtrees stripped): every <table class="…"> class set, per template folder; the two-column tables'
header pairs and which class the gold gives them (the tableFixed test: exactly two columns + a contrast-lexicon header
pair); Claude's current class set. Paths dynamic (CLAUDE.md §13). Run under WSL: python3 _measure_r347_tables.py [--all]
Writes _r347_tables.json and prints the summary."""
import os, re, sys, json, html, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests")); sys.path.insert(0, TESTS)
import _corpus
from anchor_compare import CLAUDE, HUMAN

TBL = re.compile(r"<table\b([^>]*)>([\s\S]*?)</table>", re.I)
CLS = re.compile(r'class="([^"]*)"')
TR = re.compile(r"<tr\b[^>]*>([\s\S]*?)</tr>", re.I)
TD = re.compile(r"<t[dh]\b[^>]*>([\s\S]*?)</t[dh]>", re.I)
TAG = re.compile(r"<[^>]+>")
CONTRAST = [("can", "cannot"), ("can", "can't"), ("pros", "cons"), ("advantages", "disadvantages"), ("advantage", "disadvantage"),
            ("before", "after"), ("do", "don't"), ("do", "dont"), ("dos", "don'ts"), ("true", "false"), ("similarities", "differences"),
            ("fact", "opinion"), ("facts", "opinions"), ("strengths", "weaknesses"), ("positive", "negative"), ("positives", "negatives"),
            ("yes", "no"), ("cause", "effect"), ("causes", "effects"), ("then", "now"), ("past", "present"), ("good", "bad"),
            ("benefits", "risks"), ("benefits", "costs"), ("for", "against"), ("agree", "disagree"), ("right", "wrong"),
            ("helpful", "unhelpful"), ("safe", "unsafe"), ("healthy", "unhealthy"), ("wants", "needs"), ("needs", "wants"),
            ("living", "non-living"), ("renewable", "non-renewable"), ("physical", "chemical"), ("push", "pull"), ("input", "output"),
            ("problem", "solution"), ("question", "answer"), ("english", "māori"), ("english", "te reo"), ("te reo māori", "english")]
def fold(s):
    s = unicodedata.normalize("NFKD", html.unescape(TAG.sub("", s))); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z' ]+", " ", s.lower()).strip()
def contrast(h1, h2):
    a, b = fold(h1), fold(h2)
    for x, y in CONTRAST:
        if (a.startswith(x) and b.startswith(y)) or (a.startswith(y) and b.startswith(x)): return f"{x}/{y}"
    return None
def strip_boxes(h):
    # drop hand-off / widget subtrees the gates exclude (top-level balanced cv2-interactive spans)
    out = []; i = 0
    while True:
        j = h.find('class="cv2-interactive', i)
        if j < 0: out.append(h[i:]); break
        k = h.rfind("<div", 0, j); out.append(h[i:k]); depth = 0; p = k
        for m in re.finditer(r"<div\b|</div>", h[k:]):
            depth += 1 if m.group(0) == "<div" else -1
            if depth == 0: p = k + m.end(); break
        i = p
    return "".join(out)
def tables(h):
    for m in TBL.finditer(strip_boxes(h)):
        cls = CLS.search(m.group(1)); cls = " ".join(sorted(cls.group(1).split())) if cls else ""
        rows = [TD.findall(r) for r in TR.findall(m.group(2))]
        cols = max((len(r) for r in rows), default=0); two = bool(rows) and all(len(r) == 2 for r in rows)
        hdr = rows[0] if rows else []
        pair = contrast(hdr[0], hdr[1]) if two and len(hdr) == 2 else None
        yield cls, cols, two, pair, [fold(x)[:30] for x in hdr[:2]]

def main():
    scan_all = "--all" in sys.argv
    codes = _corpus.mods(HUMAN) if scan_all else _corpus.gate_mods(HUMAN)
    G = collections.defaultdict(collections.Counter); C = collections.Counter(); two_g = collections.Counter(); pair_g = collections.Counter()
    two_c = 0; pair_c = collections.Counter(); pairs_seen = collections.Counter(); nonpair_two_g = collections.Counter(); aff = set(); tot_g = tot_c = 0
    for code in codes:
        gdir = _corpus.mdir(HUMAN, code); tmpl = os.path.basename(os.path.dirname(gdir)) if gdir else "?"
        if gdir and os.path.isdir(gdir):
            for f in os.listdir(gdir):
                if not f.endswith(".html"): continue
                for cls, cols, two, pair, hdr in tables(open(os.path.join(gdir, f), encoding="utf-8", errors="replace").read()):
                    G[tmpl][cls] += 1; tot_g += 1
                    if two: two_g[cls] += 1
                    if pair: pair_g[(pair, cls)] += 1; pairs_seen[pair] += 1
                    elif two and cls == "table tableFixed": nonpair_two_g[tuple(hdr)] += 1
        cdir = _corpus.mdir(CLAUDE, code)
        if cdir and os.path.isdir(cdir):
            for f in os.listdir(cdir):
                if not f.endswith(".html"): continue
                for cls, cols, two, pair, hdr in tables(open(os.path.join(cdir, f), encoding="utf-8", errors="replace").read()):
                    C[cls] += 1; tot_c += 1; aff.add(code)
                    if two: two_c += 1
                    if pair: pair_c[pair] += 1
    summary = {"population": "all" if scan_all else "gate_mods", "gold_tables": tot_g, "gold_class_by_template": {k: dict(v.most_common()) for k, v in G.items()},
               "gold_two_column_by_class": dict(two_g.most_common()), "gold_contrast_pairs_by_class": {f"{p} | {c}": n for (p, c), n in sorted(pair_g.items(), key=lambda t: -t[1])},
               "gold_tableFixed_two_col_without_pair(headers)": {" | ".join(k): v for k, v in nonpair_two_g.most_common(25)},
               "claude_tables": tot_c, "claude_class": dict(C.most_common()), "claude_two_column": two_c, "claude_contrast_pairs": dict(pair_c.most_common()),
               "claude_modules_with_tables": len(aff)}
    json.dump(summary, open(os.path.join(HERE, "_r347_tables.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if scan_all: open(os.path.join(HERE, "_affected_r347.txt"), "w", newline="\n").write("\n".join(sorted(aff)) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
