#!/usr/bin/env python3
"""_discrepancy_audit.py — COMPREHENSIVE per-module + example-harvesting
Claude-vs-human discrepancy audit, built on full_compare's element matcher.

WHY (Chris's ask, round 43): a systematic, thorough comparison of EVERY Claude
page vs its human counterpart, surfacing the MOST COMMON discrepancies across
every page of every module. full_compare.py gives the corpus rollup; this adds
the two things a "highly detailed" survey needs:
  1. a PER-MODULE discrepancy profile for every paired module (so no module is
     invisible inside the corpus total), and
  2. CONCRETE EXAMPLES for every discrepancy subtype (the actual text + how the
     human rendered it vs how Claude rendered it), so each pattern is tangible
     and can be triaged derivable-vs-editorial by eye.

It reuses full_compare's parser/matcher verbatim (same buckets: LEVEL / TAG /
WIDTH / WRAP / DUP / exact), so the totals reconcile with full_compare.py.

USAGE:
  python3 _discrepancy_audit.py                 # all paired modules
  python3 _discrepancy_audit.py --json OUT.json # also dump the raw audit
"""
import json
import _corpus  # round128: nesting-aware corpus paths
import os
import re
import sys
from collections import Counter, defaultdict

from anchor_compare import parse, match_elements, CLAUDE, HUMAN

EX_CAP = 12   # max concrete examples kept per discrepancy subtype


# ---------------------------------------------------------------------------
# ROBUST, CODE-AWARE page pairing (fixes the full_compare.page_key bug).
#
# full_compare.page_key() splits the filename on the LAST '-' then reads the
# first number. That works for Claude ("CODE-00.html") and for human files that
# use a dash ("CODE-1.0.html"), but the human gold also uses TWO other naming
# conventions this misses:
#   • DOT-separated   "AGH1008.00.html"  → no dash, so it reads the CODE digits
#                                           ("1008.00") → wrong key → never pairs
#   • single-page     "TEFUN01.html" / "CEDT101 Who's at my table.html" → 0
# The buggy key silently dropped 39 of 193 modules (~20% of the corpus — whole
# families: AGH, CEDT, CEDR, CEDW, TEFUN, XTAS, XMES, XDLS, …). We strip the
# module code FIRST, then read the trailing page number, so all three forms pair.
# ---------------------------------------------------------------------------
def pkey(name, code):
    base = name[:-5] if name.lower().endswith(".html") else name
    rest = base[len(code):] if base.upper().startswith(code.upper()) else base
    rest = re.sub(r"(?<=\d)_(?=\d)", ".", rest)   # ROUND 243: library-form _L_S reads as L.S
    m = re.search(r"(\d+(?:\.\d+)?)", rest)        # first number AFTER the code
    return float(m.group(1)) if m else 0.0


def _page_sig(path):
    """A page's content fingerprint = the bag of words across its headings (h1-h5).
    Used to pair pages by CONTENT when the two sides number pages differently."""
    t = parse(path)
    w = set()
    for e in t.elements:
        if e["tag"] in ("h1", "h2", "h3", "h4", "h5") and "text" in e:
            w |= set(e["text"].split())
    return w


def pairs(code, content_thresh=0.2):
    """Pair every Claude page with its TRUE human counterpart. The two sides number
    pages differently (sub-pagination: human '0.0,0.1,…' vs Claude '00,01,…'; plus
    off-by-one / renumbering), and pairing by NUMBER mis-pairs sub-paginated modules
    (Claude '03' is the human's '2.1' by content, not '3.0' by number). So: (1) match
    by CONTENT first — best heading-word overlap, greedy, thresholded (the real
    counterpart regardless of numbering); then (2) numeric key-match the LEFTOVERS
    content missed (short / reworded pages). Maximises correct coverage."""
    cdir, hdir = _corpus.mdir(CLAUDE, code), _corpus.mdir(HUMAN, code)
    if not (os.path.isdir(cdir) and os.path.isdir(hdir)):
        return []
    cf = sorted(f for f in os.listdir(cdir) if f.endswith(".html"))
    # ROUND 440 (D13-6): the gold listing goes through compare_gold_pages.txt (_corpus.gold_pages; GOLDPAGES_OFF=1 = all).
    hf = _corpus.gold_pages(code, sorted(f for f in os.listdir(hdir) if f.endswith(".html")))
    if not cf or not hf:
        return []
    matched = []
    usedc, usedh = set(), set()
    # (0) ROUND 440: a `pin` line pairs its two files before the content match (both must exist and be unused)
    for pc, ph in _corpus.gold_pins(code):
        if pc in cf and ph in hf and pc not in usedc and ph not in usedh:
            usedc.add(pc); usedh.add(ph); matched.append((pc, ph))
    # (1) content match (greedy, global best-overlap first)
    csig = {f: _page_sig(os.path.join(cdir, f)) for f in cf}
    hsig = {f: _page_sig(os.path.join(hdir, f)) for f in hf}
    cand = []
    for cfn in cf:
        for hfn in hf:
            a, b = csig[cfn], hsig[hfn]
            ov = len(a & b) / len(a | b) if (a and b) else 0.0
            if ov >= content_thresh:
                cand.append((ov, cfn, hfn))
    cand.sort(reverse=True)
    for ov, cfn, hfn in cand:
        if cfn in usedc or hfn in usedh:
            continue
        usedc.add(cfn); usedh.add(hfn)
        matched.append((cfn, hfn))
    # (2) numeric key-match the leftovers
    lc = [f for f in cf if f not in usedc]
    lh = [f for f in hf if f not in usedh]
    if lc and lh:
        hm = {}
        for f in lh:
            hm.setdefault(pkey(f, code), f)
        for f in lc:
            n = pkey(f, code)
            if n in hm and hm[n] not in usedh:
                usedh.add(hm[n]); matched.append((f, hm[n]))
    matched.sort(key=lambda p: pkey(p[0], code))
    return [(pkey(cfn, code), os.path.join(cdir, cfn), os.path.join(hdir, hfn))
            for cfn, hfn in matched]


def render(e):
    """Compact rendering signature of a content element: tag @ wrapper-chain [col]."""
    chain = ">".join(e["chain"]) or "·"
    return f"{e['tag']} @ {chain} [{e['col'] or '-'}]"


def audit(codes):
    per_mod = {}
    examples = defaultdict(list)      # "CAT|subtype" -> [ {mod,page,text,human,claude} ]
    totals = Counter()
    sub = {"WRAP": Counter(), "TAG": Counter(), "LEVEL": Counter(), "WIDTH": Counter()}
    inv_c, inv_h = Counter(), Counter()
    pages = 0
    for code in codes:
        pr = pairs(code)
        if not pr:
            continue
        m = per_mod.setdefault(code, Counter())
        for n, cp, hp in pr:
            ct, ht = parse(cp), parse(hp)
            for k, v in ct.inv.items():
                inv_c[k] += v
            for k, v in ht.inv.items():
                inv_h[k] += v
            cels = [e for e in ct.elements if e["tag"] != "WIDGET" and "text" in e]
            hels = [e for e in ht.elements if e["tag"] != "WIDGET" and "text" in e]
            matched, c_only, h_only = match_elements(cels, hels)
            m["pages"] += 1
            m["matched"] += len(matched)
            m["claude_total"] += len(cels)
            m["human_total"] += len(hels)
            m["c_only"] += len(c_only)
            m["h_only"] += len(h_only)
            pages += 1

            # duplication (same rule as full_compare)
            ctext, htext = Counter(e["text"] for e in cels), Counter(e["text"] for e in hels)
            for txt, cn in ctext.items():
                hn = htext.get(txt, 0)
                if cn >= 2 and hn >= 1 and cn > hn and len(txt) >= 8:
                    d = cn - hn
                    m["DUP"] += d
                    totals["DUP"] += d
                    if len(examples["DUP|repeat"]) < EX_CAP:
                        examples["DUP|repeat"].append(
                            {"mod": code, "page": n, "text": txt[:90],
                             "human": f"x{hn}", "claude": f"x{cn}"})

            for ce, he in matched:
                exact = True
                bh = ce["level"] is not None and he["level"] is not None
                if bh and ce["level"] != he["level"]:
                    m["LEVEL"] += 1
                    totals["LEVEL"] += 1
                    exact = False
                    s = f"h{he['level']}->h{ce['level']}"
                    sub["LEVEL"][s] += 1
                    key = f"LEVEL|{s}"
                    if len(examples[key]) < EX_CAP:
                        examples[key].append({"mod": code, "page": n, "text": he["text"][:90],
                                              "human": render(he), "claude": render(ce)})
                elif ce["tag"] != he["tag"]:
                    m["TAG"] += 1
                    totals["TAG"] += 1
                    exact = False
                    s = f"{he['tag']}->{ce['tag']}"
                    sub["TAG"][s] += 1
                    key = f"TAG|{s}"
                    if len(examples[key]) < EX_CAP:
                        examples[key].append({"mod": code, "page": n, "text": he["text"][:90],
                                              "human": render(he), "claude": render(ce)})
                if ce["col"] != he["col"]:
                    m["WIDTH"] += 1
                    totals["WIDTH"] += 1
                    exact = False
                    s = f"{he['col'] or 'none'}->{ce['col'] or 'none'}"
                    sub["WIDTH"][s] += 1
                    key = f"WIDTH|{s}"
                    if len(examples[key]) < EX_CAP:
                        examples[key].append({"mod": code, "page": n, "text": he["text"][:70],
                                              "human": render(he), "claude": render(ce)})
                if ce["chain"] != he["chain"]:
                    m["WRAP"] += 1
                    totals["WRAP"] += 1
                    exact = False
                    s = f"{'>'.join(he['chain']) or '·'}->{'>'.join(ce['chain']) or '·'}"
                    sub["WRAP"][s] += 1
                    key = f"WRAP|{s}"
                    if len(examples[key]) < EX_CAP:
                        examples[key].append({"mod": code, "page": n, "text": he["text"][:70],
                                              "human": render(he), "claude": render(ce)})
                if exact:
                    m["exact"] += 1
                    totals["exact"] += 1
    return per_mod, examples, totals, sub, inv_c, inv_h, pages


def main():
    codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))   # r343: minus compare_exclusions.txt
    per_mod, examples, totals, sub, inv_c, inv_h, pages = audit(codes)

    matched = sum(m["matched"] for m in per_mod.values())
    print(f"DISCREPANCY AUDIT — {pages} paired pages across {len(per_mod)} modules")
    print(f"text-matched content elements: {matched}\n")
    print("== corpus category totals (matched-element discrepancies) ==")
    for k in ["exact", "WRAP", "WIDTH", "TAG", "LEVEL", "DUP"]:
        print(f"  {k:7} {totals[k]:6}  ({100*totals[k]/(matched or 1):4.1f}% of matched)")

    # per-module worst, by total flagged discrepancies + by impurity rate
    print("\n== per-module: worst by flagged-discrepancy count (top 25) ==")
    rows = []
    for code, m in per_mod.items():
        flags = m["LEVEL"] + m["TAG"] + m["WIDTH"] + m["WRAP"]
        rate = 100 * m["exact"] / (m["matched"] or 1)
        rows.append((flags, code, m["matched"], m["exact"], rate, m))
    for flags, code, mt, ex, rate, m in sorted(rows, reverse=True)[:25]:
        print(f"  {code:9} flags={flags:4} matched={mt:4} exact={ex:4} ({rate:4.1f}%)"
              f"  WRAP={m['WRAP']:3} WIDTH={m['WIDTH']:3} TAG={m['TAG']:3} LEVEL={m['LEVEL']:3} DUP={m['DUP']:2}")

    # lowest exact-rate modules (>=20 matched, so the rate is meaningful)
    print("\n== per-module: lowest exact-chain rate (>=20 matched elements) ==")
    rr = [(100 * m["exact"] / (m["matched"] or 1), code, m["matched"], m["exact"])
          for code, m in per_mod.items() if m["matched"] >= 20]
    for rate, code, mt, ex in sorted(rr)[:25]:
        print(f"  {code:9} exact {ex:4}/{mt:4} = {rate:4.1f}%")

    _print_subtypes(sub)

    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        dump = {
            "pages": pages,
            "modules": len(per_mod),
            "matched": matched,
            "totals": dict(totals),
            "subtypes": {cat: dict(c) for cat, c in sub.items()},
            "inv_claude": dict(inv_c),
            "inv_human": dict(inv_h),
            "per_module": {c: dict(m) for c, m in per_mod.items()},
            "examples": {k: v for k, v in examples.items()},
        }
        json.dump(dump, open(out, "w"), indent=1)
        print(f"\nwrote {out}  ({len(examples)} discrepancy subtypes with examples)")


def _print_subtypes(sub):
    for cat in ["WRAP", "WIDTH", "TAG", "LEVEL"]:
        print(f"\n== top {cat} subtypes (human->claude), corrected full pairing ==")
        for s, n in sub[cat].most_common(12):
            print(f"  {n:5}  {s}")


if __name__ == "__main__":
    main()
