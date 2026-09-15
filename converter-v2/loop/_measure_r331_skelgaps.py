#!/usr/bin/env python3
"""_measure_r331_skelgaps.py — ROUND 331 (loop session 5, Round 2) PICK probe: the skeleton SCAFFOLD gate's
own difflib opcodes, tallied corpus-wide — which skeleton LINES are most often MISSING in Claude (gold-only)
and EXTRA in Claude (Claude-only), per template folder. A ranking instrument for the next class, not a gate.
Paths are dynamic (CLAUDE.md §13). Run from anywhere:  python3 _measure_r331_skelgaps.py [--top N]
Writes _r331_skelgaps.json next to itself and prints the summary.
"""
import os, sys, re, json, difflib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
import _skeleton_compare as S
from _discrepancy_audit import pairs, CLAUDE

TOP = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 40

def main():
    codes = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
    miss = collections.defaultdict(collections.Counter)   # tmpl -> line -> count (gold-only)
    extra = collections.defaultdict(collections.Counter)  # tmpl -> line -> count (claude-only)
    miss_pages = collections.defaultdict(collections.Counter); extra_pages = collections.defaultdict(collections.Counter)
    miss_mods = collections.defaultdict(lambda: collections.defaultdict(set)); extra_mods = collections.defaultdict(lambda: collections.defaultdict(set))
    npairs = 0
    for code in codes:
        cdir = _corpus.mdir(CLAUDE, code); tmpl = os.path.basename(os.path.dirname(cdir))
        for n, cp, hp in pairs(code):
            if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
            if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
            try:
                _, a, b = S.match(cp, hp, scaffold=True)
            except Exception:
                continue
            npairs += 1
            sm = difflib.SequenceMatcher(None, b, a)
            seen_m, seen_e = set(), set()
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag in ("delete", "replace"):
                    for l in b[i1:i2]:
                        k = l.strip(); miss[tmpl][k] += 1; seen_m.add(k)
                if tag in ("insert", "replace"):
                    for l in a[j1:j2]:
                        k = l.strip(); extra[tmpl][k] += 1; seen_e.add(k)
            for k in seen_m: miss_pages[tmpl][k] += 1; miss_mods[tmpl][k].add(code)
            for k in seen_e: extra_pages[tmpl][k] += 1; extra_mods[tmpl][k].add(code)
    out = {"pairs": npairs, "by_template": {}}
    print(f"pairs scored: {npairs}")
    for tmpl in sorted(set(miss) | set(extra)):
        out["by_template"][tmpl] = {
            "missing": [(k, v, miss_pages[tmpl][k], len(miss_mods[tmpl][k])) for k, v in miss[tmpl].most_common(TOP)],
            "extra": [(k, v, extra_pages[tmpl][k], len(extra_mods[tmpl][k])) for k, v in extra[tmpl].most_common(TOP)],
        }
        print(f"\n===== {tmpl} — gold lines MISSING in Claude (occ | pages | modules) =====")
        for k, v in miss[tmpl].most_common(TOP):
            print(f"  {v:6} | {miss_pages[tmpl][k]:5} | {len(miss_mods[tmpl][k]):4} | {k}")
        print(f"\n===== {tmpl} — Claude lines EXTRA vs gold (occ | pages | modules) =====")
        for k, v in extra[tmpl].most_common(TOP):
            print(f"  {v:6} | {extra_pages[tmpl][k]:5} | {len(extra_mods[tmpl][k]):4} | {k}")
    json.dump(out, open(os.path.join(HERE, "_r331_skelgaps.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nwrote _r331_skelgaps.json")

if __name__ == "__main__":
    main()
