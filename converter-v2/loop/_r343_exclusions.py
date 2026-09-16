#!/usr/bin/env python3
"""_r343_exclusions.py — ROUND 343 (Chris's decision D10-6): the DURABLE, re-applicable record of the gate-tool change.
reference/tests/ lives OUTSIDE the git repo (CLAUDE.md §4), so this script + compare_exclusions.txt + _corpus.py are mirrored into
pageforge-site/converter-v2/loop/ and this script re-applies the edits on a fresh tree (idempotent; LF / CRLF kept per file):
  1. reference/tests/compare_exclusions.txt — the eight CED revision-brief codes (written from the mirror if absent);
  2. _corpus.py gains excluded() + gate_mods(root) (mods(root) minus the list; mods() stays INCLUSIVE);
  3. the eight scored-population lines switch to gate_mods(): _skeleton_compare.py, _structural_defect_audit.py, compare_structure.py,
     body_compare.py, scaffold_audit.py, _discrepancy_audit.py, strict_compare.py, anchor_compare.py (+ outputs/_measure_ceiling.py).
Run from anywhere: python3 outputs/_r343_exclusions.py
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
EXC = os.path.join(T, "compare_exclusions.txt")
if not os.path.exists(EXC):
    src = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2", "loop", "compare_exclusions.txt")
    wr(EXC, rd(src)); print("compare_exclusions.txt restored from the mirror")
CORPUS_ADD = '''
# ---------------------------------------------------------------------------------------------------------------------
# ROUND 343 (Chris's decision D10-6, 2026-09-16): the SCORED population is the corpus minus compare_exclusions.txt.
# mods() stays inclusive (regeneration / manifest / registries / feature index cover every module); the GATES call
# gate_mods(). One list, honoured by every gate — see compare_exclusions.txt for the reason each module is there.
EXCLUSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "compare_exclusions.txt")

def excluded():
    """The module codes compare_exclusions.txt lists (comments after '#' ignored); empty when the file is absent."""
    try:
        with open(EXCLUSIONS_FILE, encoding="utf-8") as f:
            return {ln.split("#", 1)[0].strip() for ln in f if ln.split("#", 1)[0].strip()}
    except FileNotFoundError:
        return set()

def gate_mods(root):
    """mods(root) minus the compare exclusions — the population every scored gate measures."""
    ex = excluded()
    return [c for c in mods(root) if c not in ex]
'''
p = os.path.join(T, "_corpus.py"); s = rd(p)
if "def gate_mods" not in s:
    wr(p, s.rstrip("\n") + "\n" + CORPUS_ADD); print("_corpus.py: gate_mods added")
EDITS = {
 "_skeleton_compare.py": [("    _all = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))",
                           "    _all = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))   # r343: minus compare_exclusions.txt")],
 "_structural_defect_audit.py": [("    _all = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))",
                           "    _all = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))   # r343: minus compare_exclusions.txt")],
 "compare_structure.py": [("        m for m in _corpus.mods(CLAUDE)\n        if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m)))",
                           "        m for m in _corpus.gate_mods(CLAUDE)   # r343: minus compare_exclusions.txt\n        if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m)))")],
 "body_compare.py": [("    mods = sys.argv[1:] or sorted(d for d in _corpus.mods(CLAUDE)\n                                  if os.path.isdir(_corpus.mdir(CLAUDE, d)))",
                      "    mods = sys.argv[1:] or sorted(d for d in _corpus.gate_mods(CLAUDE)   # r343: minus compare_exclusions.txt\n                                  if os.path.isdir(_corpus.mdir(CLAUDE, d)))")],
 "scaffold_audit.py": [("    mods = sys.argv[1:] or sorted(d for d in _corpus.mods(CLAUDE)\n                                  if os.path.isdir(_corpus.mdir(CLAUDE, d)))",
                        "    mods = sys.argv[1:] or sorted(d for d in _corpus.gate_mods(CLAUDE)   # r343: minus compare_exclusions.txt\n                                  if os.path.isdir(_corpus.mdir(CLAUDE, d)))")],
 "_discrepancy_audit.py": [("    codes = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))",
                           "    codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))   # r343: minus compare_exclusions.txt")],
 "strict_compare.py": [("    codes = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))",
                        "    codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))   # r343: minus compare_exclusions.txt")],
 "anchor_compare.py": [("def all_codes():\n    return sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))",
                        "def all_codes():\n    return sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))   # r343: minus compare_exclusions.txt")],
}
for f, pairs in EDITS.items():
    p = os.path.join(T, f); s = rd(p); crlf = "\r\n" in s[:2000]; changed = False
    for a, b in pairs:
        a2, b2 = (a.replace("\n", "\r\n"), b.replace("\n", "\r\n")) if crlf else (a, b)
        if b2 in s: continue
        assert s.count(a2) == 1, (f, s.count(a2)); s = s.replace(a2, b2, 1); changed = True
    if changed: wr(p, s); print("patched", f)
p = os.path.join(HERE, "_measure_ceiling.py"); s = rd(p)
a = "        codes = _corpus.mods(HUMAN)"; b = "        codes = _corpus.gate_mods(HUMAN)   # r343: minus compare_exclusions.txt (D10-6)"
if b not in s and s.count(a) == 1: wr(p, s.replace(a, b, 1)); print("patched _measure_ceiling.py")
print("r343 exclusions: applied / already in place")
