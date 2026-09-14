#!/usr/bin/env python3
"""_measure_r316_lessonpair.py — ROUND 316 (loop Round 3) measurement probe: the lesson page's
bilingual title pair (KB constraint 79 + the TITLE BAR parsing rule; 01A 'YEARS 9-10 and NCEA
lesson pages — a single title, unless the LESSON itself is bilingual').

WHAT IT MEASURES (every Claude lesson page, paired with its gold page through the gate's own
pairing — _discrepancy_audit.pairs, void-aware since round 315):
  * Claude header title spans: count; whether one carries a ' | ' (a pipe-joined pair); whether
    one starts with the module code (the writer's "TRR106 The vowels: Uu | ..." carried through).
  * Gold header title spans on the paired page: count, and for a Claude pipe page WHICH half the
    gold puts first (as-written = the pipe's left half first; reo-first = the right half first).
  * Per family and per template folder.
Paths are dynamic (CLAUDE.md §13). Run from anywhere:  python3 _measure_r316_lessonpair.py
Writes _r316_lessonpair.json next to itself and prints the summary.
"""
import os, re, sys, json, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus                                   # nesting-aware corpus paths
from _discrepancy_audit import pairs, CLAUDE     # the gate's pairing

H1 = re.compile(r"<h1><span>(.*?)</span></h1>", re.S)
TAG = re.compile(r"<[^>]+>")

def fold(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def header_spans(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'<div id="header".*?<div id="body"', s, re.S)
    seg = m.group(0) if m else s[:8000]
    out = []
    for x in H1.findall(seg):
        x = TAG.sub("", x)
        x = x.replace("&ndash;", "–").replace("&amp;", "&").replace("&#39;", "'")
        out.append(re.sub(r"\s+", " ", x).strip())
    return out

def main():
    codes = _corpus.mods(CLAUDE)
    rows = []
    fam_tot = collections.Counter(); fam_pipe = collections.Counter(); fam_code = collections.Counter()
    fam_pipe_gold2 = collections.Counter(); fam_order = collections.defaultdict(collections.Counter)
    tmpl_pipe = collections.Counter()
    for code in codes:
        fam = re.match(r"[A-Z]+", code).group(0)
        cdir = _corpus.mdir(CLAUDE, code)
        tmpl = os.path.basename(os.path.dirname(cdir)) if cdir else "?"
        for n, cp, hp in pairs(code):
            if n == 0 or str(n).startswith("0."):      # overview pages are out of scope
                continue
            csp = header_spans(cp); hsp = header_spans(hp)
            pipe = next((x for x in csp if " | " in x or "|" in x), None)
            codepfx = any(x.startswith(code) for x in csp)
            fam_tot[fam] += 1
            row = {"code": code, "fam": fam, "tmpl": tmpl, "page": os.path.basename(cp), "gold": os.path.basename(hp),
                   "claude_spans": csp, "gold_spans": hsp, "pipe": bool(pipe), "code_prefix": codepfx}
            if pipe:
                fam_pipe[fam] += 1; tmpl_pipe[tmpl] += 1
                left, right = [t.strip() for t in pipe.split("|", 1)]
                left = re.sub(r"^" + re.escape(code) + r"\s*[–\-:]?\s*", "", left).strip()
                row["halves"] = [left, right]
                if len(hsp) >= 2:
                    fam_pipe_gold2[fam] += 1
                    g0, g1 = fold(hsp[0]), fold(hsp[1])
                    if g0 and (g0 == fold(right) or g0 in fold(right) or fold(right) in g0): order = "reo-first"
                    elif g0 and (g0 == fold(left) or g0 in fold(left) or fold(left) in g0): order = "as-written"
                    else: order = "gold-other-pair"
                    row["gold_order"] = order; fam_order[fam][order] += 1
                else:
                    row["gold_order"] = f"gold-{len(hsp)}-span"; fam_order[fam][row["gold_order"]] += 1
            if codepfx: fam_code[fam] += 1
            rows.append(row)
    pipe_rows = [r for r in rows if r["pipe"]]
    code_rows = [r for r in rows if r["code_prefix"]]
    summary = {
        "lesson_pairs": len(rows), "pipe_pages": len(pipe_rows), "code_prefix_pages": len(code_rows),
        "pipe_modules": sorted(set(r["code"] for r in pipe_rows)),
        "code_prefix_modules": sorted(set(r["code"] for r in code_rows)),
        "pipe_by_family": {f: {"pipe": fam_pipe[f], "of_lesson_pairs": fam_tot[f], "gold_two_span": fam_pipe_gold2[f],
                               "gold_order": dict(fam_order[f])} for f in fam_pipe},
        "pipe_by_template": dict(tmpl_pipe),
        "code_prefix_by_family": dict(fam_code),
    }
    out = os.path.join(HERE, "_r316_lessonpair.json")
    json.dump({"summary": summary, "pipe_rows": pipe_rows, "code_prefix_rows": code_rows}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("wrote", out)

if __name__ == "__main__":
    main()
