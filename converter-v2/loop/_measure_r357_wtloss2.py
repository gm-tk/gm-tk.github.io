#!/usr/bin/env python3
"""_measure_r357_wtloss2.py — stage 2 of the free-body text-loss census: re-test every LOST paragraph of _r357_wtloss.json against the
DISK corpus (= the r356 engine output) with a finer test — list markers stripped, a `|` bilingual pair tested half by half, 5-word windows
at both ends of every half, URLs and bare media references excluded — and classify the confirmed losses by the writer's context."""
import json, re, collections, os, html, glob
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.normpath(os.path.join(HERE,'..','..'))
import sys; sys.path.insert(0, os.path.join(HERE,'..','reference','tests')); import _corpus
CLAUDE=os.path.join(ROOT,'01-Claude_Modules_')
recs=[r for r in json.load(open(os.path.join(HERE,'_r357_wtloss.json'),encoding='utf8')) if not r.get('summary')]
def norm(s): 
    s=html.unescape(s or '').lower().replace('\u2019',"'").replace('\u2018',"'")
    return re.sub(r'[^\w]+',' ',s,flags=re.U).strip()
cache={}
def pagetext(code):
    if code in cache: return cache[code]
    d=_corpus.mdir(CLAUDE,code); big=[]
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith('.html'):
                h=open(os.path.join(d,f),encoding='utf8',errors='ignore').read()
                h=re.sub(r'<!--.*?-->',' ',h,flags=re.S); h=re.sub(r'<(script|style)\b.*?</\1>',' ',h,flags=re.S|re.I)
                attrs=" ".join(re.findall(r'\s(?:alt|title|data-text|placeholder)="([^"]*)"',h))
                big.append(norm(re.sub(r'<[^>]+>',' ',h)+" "+attrs))
    cache[code]=" "+" ".join(big)+" "; return cache[code]
URL=re.compile(r'https?://\S+|www\.\S+',re.I)
MEDIAREF=re.compile(r'stock (photo|illustration|vector|image)|download image now|istockphoto|getty|\(youtube\.com\)|– youtube$|\byoutube\b',re.I)
def halves(text):
    t=re.sub(r'\*\*|__|\*','',text); t=URL.sub(' ',t)
    t=re.sub(r'^\s*(?:[•\-–●]\s*)?(?:\d+[.)]\s*)?(?:[a-z][.)]\s+)?','',t,flags=re.I)
    return [h.strip() for h in re.split(r'\s\|\s|\|',t) if len(norm(h).split())>=3]
out=[]
for r in recs:
    txt=r['text']
    if URL.search(txt) and len(norm(URL.sub(' ',txt)).split())<4: r['cls']='url'; out.append(r); continue
    if MEDIAREF.search(txt): r['cls']='media-ref'; out.append(r); continue
    hs=halves(txt)
    if not hs: r['cls']='short'; out.append(r); continue
    big=pagetext(r['code']); found=0
    for h in hs:
        w=norm(h).split(); n=min(5,len(w)); head=" ".join(w[:n]); tail=" ".join(w[-n:])
        if (" "+head+" ") in big or (" "+tail+" ") in big: found+=1
    r['cls']='found' if found==len(hs) else ('partial' if found else 'LOST')
    out.append(r)
c=collections.Counter(r['cls'] for r in out); print(c)
lost=[r for r in out if r['cls']=='LOST']
def tagkey(t):
    t=(t or '').lower(); t=re.sub(r'\d+','N',t); t=re.sub(r'[^a-z\[\]/ N:-]+',' ',t); return t.strip()[:36]
cc=collections.Counter(); pg=collections.defaultdict(set); ex=collections.defaultdict(list)
for r in lost:
    k=('same:'+tagkey(r['sameTag'])) if r['sameTag'] else ('prev%s:'%('' if r['prevDist']<=2 else '>2')+tagkey(r['prevTag']))
    cc[k]+=1; pg[k].add((r['code'],r['wtPage']))
    if len(ex[k])<3: ex[k].append((r['code'],r['wtPage'],r['text'][:100]))
print("\nCONFIRMED lost paragraphs:",len(lost),"on",len(set((r['code'],r['wtPage']) for r in lost)),"WT pages /",len(set(r['code'] for r in lost)),"modules")
print("by context (n | wt-pages | modules | context | example):")
for k,v in cc.most_common(40): print(f"  {v:5} {len(pg[k]):5} {len(set(p[0] for p in pg[k])):4} | {k:40} {ex[k][0]}")
json.dump(lost, open(os.path.join(HERE,'_r357_wtloss_confirmed.json'),'w'), indent=0, ensure_ascii=False)
