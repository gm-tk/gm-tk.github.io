"""_measure_r351_colsort_gold.py — ROUND 351 PICK: the CLEAN category-sort candidates (one table, width>=3, clean text header,
no red / url anywhere) and what the GOLD built for each (the dragAndDrop block on the gold page that carries the header labels
and the items): layout=column (a sort), layout=standard (a match), other, or none found. Diagnostic only."""
import json,re,os,collections,html
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..')); GOLD=os.path.join(ROOT,'01-Finalized_Modules_')
recs=json.load(open(os.path.join(HERE,'_r350_ddcolumn.json'),encoding='utf-8'))
fam={}
for f in os.listdir(GOLD):
    for m in os.listdir(os.path.join(GOLD,f)): fam[m]=(f,os.path.join(GOLD,f,m))
TAG=re.compile(r'\[[^\]]*\]')
def clean_hdr(t): return all(c['t'] and not c['red'] and not c['url'] and not TAG.search(c['t']) for c in t[0])
def cand(r):
    if r['built'] or r['nTables']!=1 or r['width']<3 or r['extraTypes'] or r['media']: return False
    t=r['tables'][0]
    if len(t)<2 or not clean_hdr(t): return False
    if any(c['red'] or c['url'] or TAG.search(c['t']) for row in t[1:] for c in row): return False
    return True
def norm(s): return re.sub(r'\W+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip().lower()
def items(t):
    out=[]
    for row in t[1:]:
        for c in row:
            for it in re.split(r'\s/\s|•',c['t']):
                it=it.strip(' *')
                if it: out.append(norm(it)[:40])
    return out
res=[]
for r in recs:
    if not cand(r): continue
    t=r['tables'][0]; hdr=[norm(c['t'].strip('*'))[:40] for c in t[0]]; its=items(t)
    f,d=fam.get(r['code'],('?',None)); best=None
    if d:
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.html'): continue
            h=open(os.path.join(d,fn),encoding='utf-8',errors='replace').read()
            for m in re.finditer(r'<div class="dragAndDrop[^"]*" layout="([^"]+)"',h):
                seg=norm(h[m.start():m.start()+12000])
                hs=sum(1 for x in hdr if x and x in seg); ist=sum(1 for x in its if x and x in seg)
                score=hs+ist
                if best is None or score>best[0]: best=(score,m.group(1),hs,ist,fn,h[m.start():m.start()+60])
    res.append({'code':r['code'],'fam':f,'page':r['page'],'index':r['index'],'rows':len(t),'w':r['width'],'hdr':hdr,'nitems':len(its),
                'gold':None if not best or best[0]<max(2,(len(hdr)+len(its))//3) else {'layout':best[1],'hdr_hits':best[2],'item_hits':best[3],'file':best[4],'open':best[5]}})
json.dump(res,open(os.path.join(HERE,'_r351_colsort_gold.json'),'w',encoding='utf-8'),indent=0)
c=collections.Counter(); byfam=collections.defaultdict(collections.Counter)
for x in res:
    k=x['gold']['layout'] if x['gold'] else 'none'; c[k]+=1; byfam[x['fam']][k]+=1
pages=set((x['code'],x['page']) for x in res); mods=set(x['code'] for x in res)
print('candidates',len(res),'bundles',len(pages),'pages',len(mods),'modules'); print('gold layout:',dict(c)); 
for f,cc in byfam.items(): print('  ',f,dict(cc))
for x in res: print(f"{x['code']:8} {x['fam'][:4]} p{x['page']:4} #{x['index']:<3} {x['rows']}x{x['w']} items={x['nitems']:2d} gold={x['gold']['layout'] if x['gold'] else '-':9} hits={x['gold']['hdr_hits'] if x['gold'] else 0}/{x['gold']['item_hits'] if x['gold'] else 0} {x['gold']['open'][:55] if x['gold'] else ''} hdr={x['hdr'][:4]}")
