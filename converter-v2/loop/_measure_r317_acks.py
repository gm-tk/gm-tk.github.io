#!/usr/bin/env python3
"""_measure_r317_acks.py — ROUND 317 (loop Round 4) measurement probe: KB constraints 45 + 90, the
acknowledgements block's template form.

WHAT IT MEASURES (every Claude page with an acks block, paired through the gate's own pairing):
  * the block's container class on both sides, and whether the apology / copyright / AI statements
    are TYPED in it (the pre-rule form the KB now forbids) or left to the template classes;
  * THE EXPECTED SKELETON DELTA of moving Claude to the KB form — computed by SIMULATING the form on
    the current page text (class -> 'acks acksTemplate', the apology and copyright acksLesson divs
    removed, the AI statement removed) and scoring the simulated page against the gold with the
    gate's own scorer (_skeleton_compare.match, scaffold=True) — the number the round records as
    the NAMED override delta before any code is written.
Paths are dynamic (CLAUDE.md §13). Run from anywhere:  python3 _measure_r317_acks.py
Writes _r317_acks.json next to itself and prints the summary.
"""
import os, re, sys, json, collections, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
import _skeleton_compare as SK

CLS = re.compile(r'<div class="(acks[^"]*)">')
APOL = "Every effort has been made to acknowledge"; COPY = "Copyright ©"; AI = "created with assistance from AI"
DIV = re.compile(r'[ \t]*<div class="acksLesson">\s*<p>(?:<i>)?[^<]*(?:</i>)?</p>\s*</div>\n?')

def simulate(html):
    """The KB form applied to the page text (the same thing AcksBuilder will emit)."""
    out = html
    out = CLS.sub(lambda m: '<div class="' + ('acks acksTemplate acksAI' if 'acksAI' in m.group(1) else 'acks acksTemplate') + '">', out, count=1)
    def drop(m):
        return "" if (APOL in m.group(0) or COPY in m.group(0) or AI in m.group(0)) else m.group(0)
    return DIV.sub(drop, out)

def main():
    rows = []; tmp = tempfile.mkdtemp(prefix="r317sim_")
    fam = collections.defaultdict(lambda: collections.Counter())
    for code in _corpus.mods(CLAUDE):
        cdir = _corpus.mdir(CLAUDE, code); tmpl = os.path.basename(os.path.dirname(cdir)) if cdir else "?"
        for n, cp, hp in pairs(code):
            html = open(cp, encoding="utf-8", errors="replace").read()
            m = CLS.search(html)
            if not m: continue
            cls = " ".join(sorted(m.group(1).split()))
            typed = (APOL in html) + (COPY in html)
            ghtml = open(hp, encoding="utf-8", errors="replace").read()
            gm = CLS.search(ghtml); gcls = " ".join(sorted(gm.group(1).split())) if gm else "(none)"
            gtyped = (APOL in ghtml) + (COPY in ghtml)
            before = SK.match(cp, hp, scaffold=True)[0]
            sim = simulate(html)
            sp = os.path.join(tmp, os.path.basename(cp)); open(sp, "w", encoding="utf-8").write(sim)
            after = SK.match(sp, hp, scaffold=True)[0]
            rows.append({"code": code, "tmpl": tmpl, "page": os.path.basename(cp), "gold": os.path.basename(hp), "claude_class": cls,
                         "claude_typed": typed, "gold_class": gcls, "gold_typed": gtyped, "changed": sim != html,
                         "scaffold_before": before, "scaffold_after": after, "delta_pp": 100 * (after - before)})
            fam[tmpl]["pages"] += 1
            if sim != html: fam[tmpl]["changed"] += 1; fam[tmpl]["delta_pp_sum"] += 100 * (after - before)
    changed = [r for r in rows if r["changed"]]
    n_all = len(json.load(open(os.path.join(HERE, "_r316_sk_final.json"), encoding="utf-8"))["per_page"])
    ppsum = sum(r["delta_pp"] for r in changed)
    summary = {
        "paired_acks_pages": len(rows), "would_change": len(changed),
        "claude_class_counts": dict(collections.Counter(r["claude_class"] for r in rows)),
        "gold_class_counts": dict(collections.Counter(r["gold_class"] for r in rows)),
        "gold_typed_on_paired": sum(1 for r in rows if r["gold_typed"] == 2),
        "by_template": {k: {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in fam.items()},
        "expected_pp_sum": round(ppsum, 2), "expected_corpus_mean_delta_pp": round(ppsum / n_all, 4), "skeleton_pairs": n_all,
        "worst": sorted(((round(r["delta_pp"], 2), r["page"]) for r in changed))[:8],
        "best": sorted(((round(r["delta_pp"], 2), r["page"]) for r in changed))[-4:],
        "crossing_50_down": sum(1 for r in changed if r["scaffold_before"] >= .5 > r["scaffold_after"]),
        "crossing_75_down": sum(1 for r in changed if r["scaffold_before"] >= .75 > r["scaffold_after"]),
        "crossing_90_down": sum(1 for r in changed if r["scaffold_before"] >= .9 > r["scaffold_after"]),
    }
    json.dump({"summary": summary, "rows": rows}, open(os.path.join(HERE, "_r317_acks.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
