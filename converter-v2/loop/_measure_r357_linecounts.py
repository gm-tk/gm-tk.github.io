#!/usr/bin/env python3
"""_measure_r357_linecounts.py — session 17 PICK probe: POSITION-FREE per-page skeleton-line COUNT deltas.
For every paired page (scaffold skeleton, the gate's own lines, repeat-collapse markers dropped), count each distinct
line on the gold side and the Claude side; per line, tally the pages where gold > Claude (DEFICIT) and Claude > gold
(SURPLUS) with the summed difference, per template folder. Unlike the opcode tallies (_r331_skelgaps) this ignores
position, so a line Claude ships in the wrong place does not count twice. Run from anywhere: python3 ... [--top N]"""
import os, sys, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus, _skeleton_compare as S
from _discrepancy_audit import pairs, CLAUDE
TOP = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 45
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
defi = collections.defaultdict(collections.Counter); surp = collections.defaultdict(collections.Counter)
defp = collections.defaultdict(collections.Counter); surp_p = collections.defaultdict(collections.Counter)
defm = collections.defaultdict(lambda: collections.defaultdict(set)); surm = collections.defaultdict(lambda: collections.defaultdict(set))
detail = collections.defaultdict(list)
n=0
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code)))
    for _, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary', os.path.basename(hp) + os.path.basename(cp), re.I): continue
        try: _, a, b = S.match(cp, hp, scaffold=True)
        except Exception: continue
        n+=1
        ca = collections.Counter(l.strip() for l in a if not l.strip().startswith("┌")); cb = collections.Counter(l.strip() for l in b if not l.strip().startswith("┌"))
        for k in set(ca)|set(cb):
            d = cb[k]-ca[k]
            if d>0: defi[tmpl][k]+=d; defp[tmpl][k]+=1; defm[tmpl][k].add(code); detail[(tmpl,'D',k)].append((os.path.basename(cp),cb[k],ca[k]))
            elif d<0: surp[tmpl][k]+=-d; surp_p[tmpl][k]+=1; surm[tmpl][k].add(code); detail[(tmpl,'S',k)].append((os.path.basename(cp),cb[k],ca[k]))
print("pairs",n)
out={}
for tmpl in sorted(defi):
    print(f"\n===== {tmpl} — gold has MORE of the line than Claude (DEFICIT: sum | pages | modules) =====")
    for k,v in defi[tmpl].most_common(TOP): print(f"  {v:6} | {defp[tmpl][k]:5} | {len(defm[tmpl][k]):4} | {k}")
    print(f"\n===== {tmpl} — Claude has MORE of the line than gold (SURPLUS: sum | pages | modules) =====")
    for k,v in surp[tmpl].most_common(TOP): print(f"  {v:6} | {surp_p[tmpl][k]:5} | {len(surm[tmpl][k]):4} | {k}")
    out[tmpl]={"deficit":[(k,v,defp[tmpl][k],len(defm[tmpl][k])) for k,v in defi[tmpl].most_common(200)],
               "surplus":[(k,v,surp_p[tmpl][k],len(surm[tmpl][k])) for k,v in surp[tmpl].most_common(200)]}
json.dump({"pairs":n,"by_template":out,"detail":{f"{t}|{s}|{k}":v for (t,s,k),v in detail.items()}}, open(os.path.join(HERE,"_r357_linecounts.json"),"w",encoding="utf-8"), indent=0, ensure_ascii=False)
