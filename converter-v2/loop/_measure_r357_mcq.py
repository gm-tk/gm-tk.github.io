#!/usr/bin/env python3
"""_measure_r357_mcq.py — classify the live MCQ bundle dump (_r357_mcq.json): for every un-built MCQ, is there an ANNOUNCED answer
convention (highlight / green / red / bold / ticks) and are the marks present on the members (block.marks hl/green, red option lines,
bold option lines)? Which shape: prose option lines vs table cells? Sizes per shape (sites / pages / modules) and per template family."""
import json, re, collections, os
HERE=os.path.dirname(os.path.abspath(__file__))
recs=json.load(open(os.path.join(HERE,'_r357_mcq.json'),encoding='utf8'))
ANN = {
 'hl': re.compile(r'(correct|right)\s+answers?[^.\n]{0,50}?(highlight|shaded)|highlight(ed)?[^.\n]{0,30}?(correct|answers?)', re.I),
 'green': re.compile(r'(correct|right)\s+answers?[^.\n]{0,40}?green|green[^.\n]{0,30}?(correct|answer)', re.I),
 'red': re.compile(r'(correct|right)\s+answers?[^.\n]{0,40}?\bred\b|\bred\b[^.\n]{0,30}?(correct|answer)', re.I),
 'bold': re.compile(r'(correct|right)\s+answers?[^.\n]{0,40}?\bbold|\bbold[^.\n]{0,30}?(correct|answer)', re.I),
 'tick': re.compile(r'(correct|right)\s+answers?[^.\n]{0,40}?(tick|✓|✔|✅|asterisk|\*)', re.I),
 'italic': re.compile(r'(correct|right)\s+answers?[^.\n]{0,40}?italic', re.I),
}
CORRECT=re.compile(r'\[\s*(correct|right|answer)\s*\]|\(correct\)', re.I)
def ann_of(r):
    txt=" ".join([o['t'] for o in r['openers']]+[m['t'] for m in r['members'] if len(m['t'].split())<=25]+r['instr'])
    return [k for k,rx in ANN.items() if rx.search(txt)]
def marks_of(r):
    kinds=collections.Counter()
    for m in r['members']:
        for mk in m['marks']: kinds[mk['k']]+=1
        if m['k']=='black' and m['red']: kinds['red-black']+=1
        if m['k']!='black' and m['red'] and not CORRECT.search(m['t']) and m['tag'] not in ('mcq','question','multiple choice quiz'): kinds['red-line']+=1
        if re.search(r'\*\*[^*]{2,}\*\*', m['t']) or re.search(r'\*\*[^*]{2,}\*\*', m.get('after','')): kinds['bold']+=1
        if CORRECT.search(m['t']): kinds['[correct]']+=1
        for row in m.get('rows',[]) or []:
            for c in row:
                for mk in c['marks']: kinds['cell-'+mk['k']]+=1
                if c['red']: kinds['cell-red']+=1
    for t in r['tables']:
        for row in t['rows']:
            for c in row:
                for mk in c['marks']: kinds['tbl-'+mk['k']]+=1
                if c['red']: kinds['tbl-red']+=1
    return kinds
def shape_of(r):
    hasTable = r['nTables']>0 or any(m['k']=='table' for m in r['members'])
    lines=[m for m in r['members'] if m['k']=='black']
    return ('table' if hasTable else 'prose')
out=[]
for r in recs:
    a=ann_of(r); mk=marks_of(r); sh=shape_of(r)
    out.append((r,a,mk,sh))
unb=[x for x in out if not x[0]['built']]
print("MCQ bundles",len(recs),"built",len(recs)-len(unb),"un-built",len(unb))
def size(xs): return f"{len(xs):4} sites / {len(set((x[0]['code'],x[0]['page']) for x in xs)):4} pages / {len(set(x[0]['code'] for x in xs)):4} modules"
print("\nun-built by shape:"); 
for sh in ('prose','table'): print("  ",sh, size([x for x in unb if x[3]==sh]))
print("\nun-built by ANNOUNCEMENT (any):", size([x for x in unb if x[1]]))
for k in ANN: print(f"   announced {k:7}", size([x for x in unb if k in x[1]]))
print("un-built with NO announcement:", size([x for x in unb if not x[1]]))
print("\nun-built by mark evidence:")
for k in ['hl','green','red-line','red-black','bold','[correct]','tbl-hl','tbl-green','tbl-red','cell-hl']:
    print(f"   {k:10}", size([x for x in unb if x[2][k]]))
print("\nannounced AND matching marks present, by shape (the derivable candidates):")
match={'hl':['hl','tbl-hl','cell-hl'],'green':['green','tbl-green'],'red':['red-line','red-black','tbl-red','cell-red'],'bold':['bold'],'tick':[],'italic':[]}
for k,mks in match.items():
    xs=[x for x in unb if k in x[1] and any(x[2][m] for m in mks)]
    for sh in ('prose','table'):
        ys=[x for x in xs if x[3]==sh]
        if ys: print(f"   {k:6} {sh:5}", size(ys), " modules:", sorted(set(x[0]['code'] for x in ys))[:30])
print("\nun-announced but [correct]-marked yet un-built (the current builder's own declines):", size([x for x in unb if not x[1] and x[2]['[correct]']]))
print("extraTypes un-built:", size([x for x in unb if x[0]['extraTypes']]))
# per-template
def tmpl(code):
    for t in ('Standard','Bilingual','Fundamentals','Inquiry'):
        if os.path.isdir(os.path.join(HERE,'..','..','01-Finalized_Modules_',t,code)): return t
    return '?'
cand=[x for x in unb if any(k in x[1] and any(x[2][m] for m in match[k]) for k in match)]
print("\nall announced+marked candidates:", size(cand))
print("  per template:", collections.Counter(tmpl(x[0]['code']) for x in cand))
print("  per announcement kind:", collections.Counter(tuple(x[1]) for x in cand).most_common())
print("\nexamples (announced + marked, un-built):")
for x in cand[:14]:
    r=x[0]; print(" ",r['code'],r['page'],'#',r['index'],x[1],dict(x[2]),x[3]); print("     opener:", [o['t'][:100] for o in r['openers']][:2]); print("     members:", [(m['k'],m['t'][:50],m['marks'][:2]) for m in r['members'][:6]])
json.dump([{'code':x[0]['code'],'page':x[0]['page'],'index':x[0]['index'],'ann':x[1],'marks':dict(x[2]),'shape':x[3]} for x in cand], open(os.path.join(HERE,'_r357_mcq_candidates.json'),'w'), indent=0)
