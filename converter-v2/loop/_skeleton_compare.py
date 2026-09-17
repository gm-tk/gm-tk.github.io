#!/usr/bin/env python3
"""SKELETON COMPARE — the text-immune STRUCTURAL match metric (round 50).

For every paired (Claude, human) page, build the simplified structural skeletons
(_structural_skeleton.py) and compare them line-by-line — a 0-100% STRUCTURAL MATCH
that covers 100% of the page and is immune to the developer's text rewording. This is
the measurement the project was missing: it answers "does Claude's STRUCTURE match the
human's", not "how close are the ~30% of text-matched elements".

Reports: corpus mean/median structural match, the distribution (how many pages are
≥90% / ≥75% / <50% structural match), per-module means, and the worst pages (with a
short structural diff so the defect is actionable). Pairs by content (heading overlap)
then numeric — same as _discrepancy_audit.py.

USAGE:
  python3 _skeleton_compare.py                 # corpus measurement
  python3 _skeleton_compare.py --json OUT.json
  python3 _skeleton_compare.py --worst 30      # also print the worst-page diffs
"""
import os, sys, re, difflib
import _corpus  # round128: nesting-aware corpus paths
from collections import defaultdict
import _structural_skeleton as S
from _structural_skeleton import skeleton
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE


def _skel(path, scaffold):
    S._SCAFFOLD = scaffold
    sk = skeleton(path).splitlines()
    return sk[sk.index("body.container-fluid"):] if "body.container-fluid" in sk else sk


# ROUND 355 (the autonomous loop's session-15 Round 5 — a measurement-tool round, the r315 pairing-parser precedent).
# difflib's AUTOJUNK heuristic (on by default) marks any line that occurs in more than 1 % of a sequence of 200+ lines as
# "junk" and refuses to match on it — and a page skeleton IS made of such lines ("p", "WIDGET", "div.row"). So every page
# whose skeleton reaches 200 lines (the long single-page Fundamentals / BLL modules) was scored with most of its structure
# ignored: CHFUN06 0.0 read 56.1 % at 198 lines and 25.5 % at 203 (r352 restored five <p> the gold has); BLL170 0.0 read
# 14.1 % where its true ratio is 58.2 %. Measured on the r354 corpus (outputs/_r355_sk_noautojunk.log): 128 pages change,
# 126 UP (BLL170 14 → 58, TEFUN02 13 → 57, BLL210 14 → 55, BLL140 16 → 56 …), the corpus mean 50.96 → 51.98 %, ≥ 50 %
# 1073 → 1093 — an INSTRUMENT correction, re-baselined and never claimed as a gain. The scorer now compares with
# autojunk=False; SKAUTOJUNK=1 restores the pre-355 numbers for a one-off comparison.
AUTOJUNK = bool(os.environ.get("SKAUTOJUNK"))


def match(claude_path, human_path, scaffold=False):
    a = _skel(claude_path, scaffold)
    b = _skel(human_path, scaffold)
    return difflib.SequenceMatcher(None, b, a, autojunk=AUTOJUNK).ratio(), a, b


def _score_pairs(pairlist):
    """Score (code, cp, hp) pairs. ROUND 190: a pair whose parse RAISES is COUNTED and
    reported, never silently dropped — the pre-190 `except: continue` hid 238 pairs (~15%
    of the population) from the PRIMARY gate for months (the r149 vacuous-gate class)."""
    rows, skipped = [], []
    for code, cp, hp in pairlist:
        try:
            rraw, _, _ = match(cp, hp, scaffold=False)
            rsca, _, _ = match(cp, hp, scaffold=True)
        except Exception as e:
            skipped.append((code, os.path.basename(cp), f"{type(e).__name__}: {e}"[:80]))
            continue
        rows.append((rsca, rraw, code, os.path.basename(cp), cp, hp))
    return rows, skipped


def selftest():
    """--selftest (r149 discipline): LIVENESS — a synthetic bare-attr fragment must SCORE
    (the pre-190 crash class); DETECTION — a raising pair must be COUNTED, not hidden."""
    import tempfile
    from _structural_skeleton import Node, label
    with tempfile.TemporaryDirectory() as td:
        a, b = os.path.join(td, "a.html"), os.path.join(td, "b.html")
        open(a, "w").write('<html><body><div class="row"><div class="accordion" layout>'
                           '<p>x</p></div></div></body></html>')
        open(b, "w").write('<html><body><div class="row"><div class="accordion">'
                           '<p>x</p></div></div></body></html>')
        r, _, _ = match(a, b, scaffold=False)          # pre-190: AttributeError right here
        assert r == 1.0, f"bare attr must contribute no token (ratio {r})"
        assert label(Node("div", {"layout": None})) == "div"
        assert label(Node("div", {"layout": "speech"})) == "div[layout=speech]"
        print("LIVENESS ok — bare KEEP_ATTR attribute scores; valued attr still renders")
        rows, skipped = _score_pairs([("ZZ", os.path.join(td, "missing.html"), b)])
        assert rows == [] and len(skipped) == 1, "a raising pair must land in the skipped count"
        print("DETECTION ok — a raising pair is COUNTED (loud), not silently dropped")
    print("SELFTEST PASS")


def main():
    if "--selftest" in sys.argv:
        selftest(); return
    _all = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))   # r343: minus compare_exclusions.txt
    # scoped run (fast inner loop): positional args = module codes to score; flags and
    # their values (--json OUT, --worst N) are skipped. No positional args => full corpus
    # (byte-identical to the original default).
    _args, codes, _i = sys.argv[1:], [], 0
    while _i < len(_args):
        _a = _args[_i]
        if _a in ("--json", "--worst"):
            _i += 2; continue
        if _a.startswith("-"):
            _i += 1; continue
        codes.append(_a); _i += 1
    codes = codes or _all
    pairlist = []
    for code in codes:
        for n, cp, hp in pairs(code):
            # skip acks / glossary / non-content pages (different page TYPE — not a fair structural pair)
            if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
            if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
            pairlist.append((code, cp, hp))
    rows, skipped = _score_pairs(pairlist)   # rows: (scaffold_ratio, raw_ratio, code, claude_name, cp, hp)
    per_mod = defaultdict(list)
    for rsca, rraw, code, name, cp, hp in rows:
        per_mod[code].append(rsca)
    if not rows:
        print("no pairs"); return
    rows.sort()
    sca = [r for r, *_ in rows]
    raw = [r for _, r, *_ in rows]
    print(f"SKELETON STRUCTURAL MATCH — {len(rows)} paired pages (text-immune, 100% of structure)\n")
    # ROUND 190: the LOUD skip counter — must be 0; a non-zero N means pages are INVISIBLE
    # to the PRIMARY gate (the pre-190 silent-drop hid 238 pairs). Never remove this line.
    print(f"pairs skipped (parse error): {len(skipped)}" + ("" if not skipped else "  << MUST BE 0"))
    for code, name, err in skipped[:10]:
        print(f"  SKIPPED {code} {name}: {err}")
    if skipped:
        print()
    print(f"RAW match (full structure, incl. widget internals): mean {100*sum(raw)/len(raw):.1f}%")
    print(f"   ^ low because Phase-1 widgets are by-design PLACEHOLDERS vs the human's built widgets.\n")
    print(f"SCAFFOLD match (widgets collapsed to one marker — the Phase-1 target: rows/cols/")
    print(f"activities/sections + widget POSITIONS): mean {100*sum(sca)/len(sca):.1f}%  median {100*sorted(sca)[len(sca)//2]:.1f}%")
    for thr in (0.95, 0.90, 0.75, 0.50):
        c = sum(1 for v in sca if v >= thr)
        print(f"  pages >= {int(thr*100):3}% SCAFFOLD match: {c:4} ({100*c/len(sca):4.1f}%)")
    print(f"  pages <  50% scaffold match: {sum(1 for v in sca if v < 0.50)}")

    print("\n== per-module mean SCAFFOLD match (worst 25) ==")
    mm = sorted(((sum(v)/len(v), code, len(v)) for code, v in per_mod.items()))
    for r, code, k in mm[:25]:
        print(f"  {code:9} {100*r:5.1f}%  ({k} pages)")

    print("\n== worst individual pages by SCAFFOLD match (top 20) ==")
    for rsca, rraw, code, name, cp, hp in rows[:20]:
        print(f"  {name:26} scaffold {100*rsca:5.1f}%  (raw {100*rraw:4.0f}%)")

    if "--worst" in sys.argv:
        k = int(sys.argv[sys.argv.index("--worst") + 1])
        print("\n" + "=" * 60 + "\nWORST-PAGE SCAFFOLD DIFFS (human → claude, widgets=WIDGET)\n" + "=" * 60)
        for rsca, rraw, code, name, cp, hp in rows[:k]:
            _, a, b = match(cp, hp, scaffold=True)
            print(f"\n#### {name}  —  {100*rsca:.0f}% scaffold match ####")
            diff = list(difflib.unified_diff(b, a, "human", "claude", lineterm="", n=1))
            print("\n".join(diff[:36]))

    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        import json
        json.dump({"pages": len(rows), "skipped_parse_errors": len(skipped),
                   "scaffold_mean": sum(sca)/len(sca), "raw_mean": sum(raw)/len(raw),
                   "per_page": [{"module": c, "page": nm, "scaffold": rs, "raw": rr}
                                for rs, rr, c, nm, *_ in rows],
                   "per_module_scaffold_mean": {c: sum(v)/len(v) for c, v in per_mod.items()}},
                  open(out, "w"), indent=1)
        print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
