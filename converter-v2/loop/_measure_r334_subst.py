"""ROUND 334 PICK instrument — SUBSTITUTION pairs in the PRIMARY gate's own difflib opcodes: for every paired page,
each `replace` opcode whose gold and Claude segments are the same length is read line-for-line as "gold ships X where
Claude ships Y"; tallied corpus-wide per template with page/module counts. Surfaces class-level swaps (e.g. a class
token) rather than the generic missing/extra tallies of _measure_r331_skelgaps.py. Run from anywhere."""
import os, sys, re, json, difflib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus, _skeleton_compare as S
from _discrepancy_audit import pairs, CLAUDE
TOP = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 40
codes = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
sub = collections.defaultdict(collections.Counter); pg = collections.defaultdict(collections.Counter); md = collections.defaultdict(lambda: collections.defaultdict(set))
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code)))
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary', os.path.basename(hp) + os.path.basename(cp), re.I): continue
        try: _, a, b = S.match(cp, hp, scaffold=True)
        except Exception: continue
        sm = difflib.SequenceMatcher(None, b, a); seen = set()
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "replace" or (i2 - i1) != (j2 - j1): continue
            for gl, cl in zip(b[i1:i2], a[j1:j2]):
                k = (gl.strip(), cl.strip())
                if k[0] == k[1]: continue
                sub[tmpl][k] += 1; seen.add(k)
        for k in seen: pg[tmpl][k] += 1; md[tmpl][k].add(code)
out = {}
for tmpl in sorted(sub):
    rows = [(g, c, v, pg[tmpl][(g, c)], len(md[tmpl][(g, c)])) for (g, c), v in sub[tmpl].most_common(TOP)]
    out[tmpl] = rows
    print(f"\n===== {tmpl} — gold line ⇐ Claude line (occ | pages | modules) =====")
    for g, c, v, p, m in rows: print(f"  {v:6} | {p:5} | {m:4} | {g}  ⇐  {c}")
json.dump(out, open(os.path.join(HERE, "_r334_subst.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
