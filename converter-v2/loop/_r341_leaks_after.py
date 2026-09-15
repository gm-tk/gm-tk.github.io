"""_r341_leaks_after.py — list every literal-[tag] leak the protected gate counts (same detector as _structural_defect_audit.py),
with the leaked text, per page; tally by the normalised tag word. Session-9 PICK evidence."""
import os, sys, re, collections, json
HERE=os.path.dirname(os.path.abspath(__file__)); TESTS=os.path.normpath(os.path.join(HERE,"..","reference","tests")); sys.path.insert(0,TESTS)
import _corpus
from _discrepancy_audit import CLAUDE
import _structural_defect_audit as A
codes=sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,d)))
tally=collections.Counter(); per=collections.defaultdict(list); pages=set()
for code in codes:
    d=_corpus.mdir(CLAUDE,code)
    for f in sorted(os.listdir(d)):
        if not f.endswith('.html'): continue
        html=open(os.path.join(d,f),encoding='utf-8').read()
        body=html[html.find('id="body"'):] if 'id="body"' in html else html
        vis=A.visible_text(body)
        for m in A.LITERAL_TAG.finditer(vis):
            t=m.group(0); ctx=vis[max(0,m.start()-60):m.end()+40].replace('\n',' ')
            key=re.sub(r'\s+',' ',t.strip().lower())
            tally[key]+=1; per[code].append((f,t,re.sub(r'\s+',' ',ctx))); pages.add((code,f))
print(sum(tally.values()),"leaks on",len(pages),"pages /",len(per),"modules")
print("\nby leaked tag (top 40):")
for k,v in tally.most_common(40): print("  %4d  %s"%(v,k))
print("\nper module:")
for code in sorted(per,key=lambda c:-len(per[c])):
    print("\n##",code,len(per[code]),"leaks on",len(set(x[0] for x in per[code])),"pages")
    seen=collections.Counter()
    for f,t,ctx in per[code]:
        k=re.sub(r'\s+',' ',t.strip().lower())
        if seen[k]>=2: continue
        seen[k]+=1
        print("   ",f,"|",t,"|",ctx[:150])
json.dump({c:per[c] for c in per},open(os.path.join(HERE,'_r341_leaks_after.json'),'w'),indent=1)
