"""_r341_ulol_sites.py — the `ul ⇐ ol` substitution sites (gold ul where Claude ol) per paired page, with the Claude <ol> first-item text."""
import os, sys, re, difflib, collections
HERE=os.path.dirname(os.path.abspath(__file__)); TESTS=os.path.normpath(os.path.join(HERE,"..","reference","tests")); sys.path.insert(0,TESTS)
import _corpus, _skeleton_compare as S
from _discrepancy_audit import pairs, CLAUDE
codes=sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,d)))
sites=[]
for code in codes:
    for n,cp,hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary",os.path.basename(hp)+os.path.basename(cp),re.I): continue
        try: _,a,b=S.match(cp,hp,scaffold=True)
        except Exception: continue
        sm=difflib.SequenceMatcher(None,b,a)
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag!="replace" or (i2-i1)!=(j2-j1): continue
            for k in range(i2-i1):
                g=b[i1+k].strip(); c=a[j1+k].strip()
                if g=="ul" and c=="ol":
                    # which ol on the claude page? count ol lines before j1+k in the claude skeleton
                    nth=sum(1 for x in a[:j1+k] if x.strip()=="ol")
                    sites.append((code,os.path.basename(cp),os.path.basename(hp),nth))
print(len(sites),"sites on",len(set((s[0],s[1]) for s in sites)),"pages /",len(set(s[0] for s in sites)),"modules")
for s in sites: print(*s)
