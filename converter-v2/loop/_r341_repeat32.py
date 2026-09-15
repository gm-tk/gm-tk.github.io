"""_r341_repeat32.py — the Standard `┌ 2× repeated ⇐ ┌ 3× repeated` substitution: WHICH element is repeated (the line after the marker) on each side."""
import os, sys, re, difflib, collections
HERE=os.path.dirname(os.path.abspath(__file__)); TESTS=os.path.normpath(os.path.join(HERE,"..","reference","tests")); sys.path.insert(0,TESTS)
import _corpus, _skeleton_compare as S
from _discrepancy_audit import pairs, CLAUDE
codes=sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,d)))
tally=collections.Counter(); pages=collections.defaultdict(set); ex=[]
for code in codes:
    tmpl=os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE,code)))
    if tmpl!="Standard": continue
    for n,cp,hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary",os.path.basename(hp)+os.path.basename(cp),re.I): continue
        try: _,a,b=S.match(cp,hp,scaffold=True)
        except Exception: continue
        sm=difflib.SequenceMatcher(None,b,a)
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag!="replace" or (i2-i1)!=(j2-j1): continue
            for k in range(i2-i1):
                g=b[i1+k].strip(); c=a[j1+k].strip()
                if g=="┌ 2× repeated:" and c=="┌ 3× repeated:":
                    gn=b[i1+k+1].strip() if i1+k+1<len(b) else "?"; cn=a[j1+k+1].strip() if j1+k+1<len(a) else "?"
                    tally[(gn,cn)]+=1; pages[(gn,cn)].add(cp)
                    if len(ex)<6: ex.append((code,os.path.basename(cp),gn,cn))
for (gn,cn),n in tally.most_common(15): print(f"{n:3d} occ | {len(pages[(gn,cn)]):3d} pages | gold 2× {gn!r:28} ⇐ claude 3× {cn!r}")
print(ex)
