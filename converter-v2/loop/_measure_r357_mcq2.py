#!/usr/bin/env python3
"""_measure_r357_mcq2.py — session 17 PICK, stage 2: simulate the MCQ builder's question/option grouping over the live dump and count the
un-built bundles where the r309 MARK channel (hl / green) or a RED option line / cell names EXACTLY ONE option per question for EVERY
question (the completeness fence) — shape A (prose option lines) and shape B (question line + a one-row option table). Also the
same-type extraTypes guard's population. Sizes as sites / pages / modules, per template."""
import json, re, collections, os
HERE=os.path.dirname(os.path.abspath(__file__))
recs=json.load(open(os.path.join(HERE,'_r357_mcq.json'),encoding='utf8'))
def tmpl(code):
    for t in ('Standard','Bilingual','Fundamentals','Inquiry'):
        if os.path.isdir(os.path.join(HERE,'..','..','01-Finalized_Modules_',t,code)): return t
    return '?'
LIST=re.compile(r'^\s*(?:[•\-–]\s*)?(?:\d+[.)]\s*)?(?:[A-Za-z][.)]\s+)?')
def strip(s): return re.sub(r'\s+',' ',re.sub(r'\*\*','',s or '')).strip()
def opt(s): return strip(LIST.sub('',strip(s)))
def fold(s): return re.sub(r'^[\s.,;:!?\'"“”‘’\-–—]+|[\s.,;:!?\'"“”‘’\-–—]+$','',re.sub(r'^[A-Za-z][.)]\s+','',(s or '').lower()).replace('  ',' ')).strip()
QEND=re.compile(r'\?\s*$|^\s*(?:\d+[.)]\s*)?\*\*.*\*\*\s*$')
def sim_prose(r):
    """returns (questions, reason) — each question {text, opts:[{t,marked}]}"""
    qs=[]; cur=None; seen_open=False
    for m in r['members']:
        if m['k']=='table': return None,'table'
        t=m['t']; 
        if m['k']=='tag' and m['tag'] in ('mcq',) and not seen_open: seen_open=True; continue
        if m['k']=='tag' and m['tag'] in ('embed','button','image','video','audio','link'): continue
        if m['k']=='tag' and m['tag'] and m['tag'] not in ('mcq','question','answer','body'): return None,'foreign:'+m['tag']
        if m['k']=='tag' and re.fullmatch(r'\[[^\]]*\]',strip(t) or ''): continue   # a bracketed instruction
        lines=[]
        if m['k']=='black' or (m['k']=='tag'):
            if strip(t): lines.append((t, m['k']=='tag' and m['cls'] in ('instruction','noise',None), m['marks']))
            for ln in (m.get('after') or '').split('\n'):
                if strip(ln): lines.append((ln, False, []))
        for ln,isred,marks in lines:
            s=strip(ln)
            if re.match(r'^(question\s*\d+|possible answers?)\s*:?$', s, re.I):
                if s.lower().startswith('question'): cur={'text':'', 'opts':[]}; qs.append(cur)
                continue
            if QEND.search(s) and (cur is None or cur['opts']):
                cur={'text':opt(s),'opts':[]}; qs.append(cur); continue
            if cur is None: cur={'text':opt(s),'opts':[]}; qs.append(cur); continue
            if not cur['text']: cur['text']=opt(s); continue
            o=opt(s)
            if not o or len(o)<2: continue
            marked = isred or any(fold(mk['t']) and (fold(mk['t'])==fold(o) or fold(o) in fold(mk['t']) or (len(fold(mk['t']))>=3 and fold(mk['t']) in fold(o))) for mk in marks)
            kinds=set(mk['k'] for mk in marks) | ({'red'} if isred else set())
            cur['opts'].append({'t':o,'marked':marked,'kinds':kinds})
    return qs,'ok'
def sim_table_rows(r):
    """shape B: black question line followed by a one-row table of >=2 option cells with exactly one marked (hl/green or whole-cell red)"""
    qs=[]; pend=None
    for m in r['members']:
        if m['k']=='black' and strip(m['t']): pend=opt(m['t']); continue
        if m['k']=='table':
            rows=m.get('rows') or []
            if len(rows)==1 and len(rows[0])>=2 and pend:
                cells=rows[0]
                opts=[{'t':opt(c['t']),'marked':bool(c['marks']) or (c['red'] and not re.search(r'\[[^\]]*\]',c['t']))} for c in cells]
                qs.append({'text':pend,'opts':opts}); pend=None; continue
            return None
    return qs if qs else None
res=collections.Counter(); sites=collections.defaultdict(list)
for r in recs:
    if r['built']: continue
    key=None
    same_extra = bool(r['extraTypes']) and all(x=='multiChoiceQuiz' for x in r['extraTypes'])
    foreign_extra = bool(r['extraTypes']) and not same_extra
    if foreign_extra: key='extraTypes-foreign'
    else:
        qsB=sim_table_rows(r)
        if qsB and len(qsB)>=1 and all(len(q['opts'])>=2 and sum(o['marked'] for o in q['opts'])==1 for q in qsB):
            key='B:table-row-options'+('+sameExtra' if same_extra else '')
        else:
            qs,why=sim_prose(r)
            if qs is None: key='decline:'+why
            elif not qs: key='no-questions'
            else:
                ok=all(len(q['opts'])>=2 and sum(o['marked'] for o in q['opts'])==1 for q in qs)
                anymark=any(o['marked'] for q in qs for o in q['opts'])
                kinds=set(k for q in qs for o in q['opts'] for k in o.get('kinds',()))
                if ok: key='A:prose-marked-complete['+','.join(sorted(kinds))+']'+('+sameExtra' if same_extra else '')
                elif anymark: key='A-partial:some-marks'
                else: key='no-marks'
    res[key]+=1; sites[key].append(r)
def size(xs): return f"{len(xs):4} sites / {len(set((x['code'],x['page']) for x in xs)):4} pages / {len(set(x['code'] for x in xs)):4} modules"
for k,v in res.most_common(): print(f"  {k:48} {size(sites[k])}  {collections.Counter(tmpl(x['code']) for x in sites[k]).most_common()}")
A=[x for k in sites if k.startswith('A:') for x in sites[k]]; B=[x for k in sites if k.startswith('B:') for x in sites[k]]
print("\nSHAPE A total:", size(A)); print("SHAPE B total:", size(B)); print("A+B:", size(A+B))
print("A modules:", sorted(collections.Counter(x['code'] for x in A).items()))
print("B modules:", sorted(collections.Counter(x['code'] for x in B).items()))
json.dump({'A':[(x['code'],x['page'],x['index']) for x in A],'B':[(x['code'],x['page'],x['index']) for x in B]}, open(os.path.join(HERE,'_r357_mcq_AB.json'),'w'))
