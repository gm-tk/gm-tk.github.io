"""_r342_col12_sites.py — sites where the gold ships `div.col-md-8.col-12` (or col-md-12.col-12) and Claude ships a bare `div.col-12`
at the same skeleton slot (the session-9 PICK's one unexamined Standard row). Prints, per site, the gold and Claude skeleton context
(3 lines before / 4 after, with indentation) so the wrapper's OWNER can be read; tallies the Claude line that follows the col-12."""
import os, sys, re, difflib, collections, json
HERE=os.path.dirname(os.path.abspath(__file__)); TESTS=os.path.normpath(os.path.join(HERE,"..","reference","tests")); sys.path.insert(0,TESTS)
import _corpus, _skeleton_compare as S
from _discrepancy_audit import pairs, CLAUDE
GOLD_LINES={"div.col-md-8.col-12","div.col-md-12.col-12"}
codes=sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,d)))
sites=[]; nxt=collections.Counter(); prv=collections.Counter(); tmplc=collections.Counter(); pages=set(); mods=set()
for code in codes:
    tmpl=os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE,code)))
    for n,cp,hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary",os.path.basename(hp)+os.path.basename(cp),re.I): continue
        try: _,a,b=S.match(cp,hp,scaffold=True)
        except Exception: continue
        sm=difflib.SequenceMatcher(None,b,a)
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag!="replace" or (i2-i1)!=(j2-j1): continue
            for k in range(i2-i1):
                g=b[i1+k].strip(); c=a[j1+k].strip()
                if g in GOLD_LINES and c=="div.col-12":
                    gi=i1+k; ci=j1+k
                    gctx=b[max(0,gi-3):gi+5]; cctx=a[max(0,ci-3):ci+5]
                    cn=a[ci+1].strip() if ci+1<len(a) else "<end>"; cpv=a[ci-1].strip() if ci>0 else "<start>"
                    nxt[cn]+=1; prv[cpv]+=1; tmplc[tmpl]+=1; pages.add((code,os.path.basename(cp))); mods.add(code)
                    sites.append(dict(code=code,tmpl=tmpl,cp=os.path.basename(cp),hp=os.path.basename(hp),gold=g,gctx=gctx,cctx=cctx))
print(len(sites),"sites on",len(pages),"pages /",len(mods),"modules; per template:",dict(tmplc))
print("\nClaude line AFTER the col-12:"); [print("  %4d  %s"%(v,k)) for k,v in nxt.most_common(15)]
print("\nClaude line BEFORE the col-12:"); [print("  %4d  %s"%(v,k)) for k,v in prv.most_common(15)]
json.dump(sites,open(os.path.join(HERE,"_r342_col12_sites.json"),"w"),indent=1)
print("\n--- first 12 sites with context (gold | claude) ---")
for s in sites[:12]:
    print("\n##",s["code"],s["tmpl"],s["cp"],"<-",s["hp"],"gold:",s["gold"])
    for gl,cl in zip(s["gctx"],s["cctx"]): print("  %-48s | %s"%(gl.rstrip()[:48],cl.rstrip()[:60]))
