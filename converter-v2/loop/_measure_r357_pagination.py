#!/usr/bin/env python3
"""_measure_r357_pagination.py — session 17 PICK probe: PAGINATION. Every gold page (by its N.M label) with no Claude page of the same
label, and every Claude page with no gold page: how many, per template; and for a gold-only SUB-page (M > 0) what the writer typed at its
start — is there a boundary tag ([end page] / [new page] / [page N] / [lesson N continued] / [part N]) in the WT just before the sub-page's
first words that Claude did not honour, or a heading, or nothing (the human's own split — class C)?"""
import os, sys, re, collections, glob, html
HERE=os.path.dirname(os.path.abspath(__file__)); TESTS=os.path.normpath(os.path.join(HERE,'..','reference','tests')); sys.path.insert(0,TESTS)
import _corpus
from compare_structure import CLAUDE, HUMAN
ROOT=os.path.normpath(os.path.join(HERE,'..','..')); PARSED=os.path.join(ROOT,'03-All_Parsed_Files')
def label(f):
    m=re.search(r'_(\d+)_(\d+)(?:_\d+)?\.html$',f) or re.search(r'[_-](\d+)\.(\d+)\.html$',f)
    return (int(m.group(1)),int(m.group(2))) if m else None
def norm(s): return re.sub(r'[^a-z0-9āēīōū]+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s)).lower()).strip()
def wt_lines(code):
    out=[]
    for f in glob.glob(os.path.join(PARSED, code+"*_parsed.txt")):
        try: out+=open(f,encoding='utf8',errors='ignore').read().split("\n")
        except Exception: pass
    return out
codes=sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,d)))
cnt=collections.Counter(); ctx=collections.Counter(); ex=collections.defaultdict(list); mods=collections.defaultdict(set)
for code in codes:
    cd=_corpus.mdir(CLAUDE,code); hd=_corpus.mdir(HUMAN,code)
    if not os.path.isdir(hd): continue
    tmpl=os.path.basename(os.path.dirname(cd))
    cl={label(f):f for f in os.listdir(cd) if f.endswith('.html') and label(f)}
    hl={label(f):f for f in os.listdir(hd) if f.endswith('.html') and label(f)}
    gold_only=sorted(set(hl)-set(cl)); claude_only=sorted(set(cl)-set(hl))
    cnt[(tmpl,'gold-only pages')]+=len(gold_only); cnt[(tmpl,'claude-only pages')]+=len(claude_only)
    if gold_only: mods[(tmpl,'gold-only')].add(code)
    if claude_only: mods[(tmpl,'claude-only')].add(code)
    if not gold_only: continue
    wl=wt_lines(code); wn=[norm(l) for l in wl]
    for lb in gold_only:
        h=open(os.path.join(hd,hl[lb]),encoding='utf8',errors='ignore').read()
        body=h[h.find('id="body"'):] if 'id="body"' in h else h
        # the first substantive text of the page body (after the header): first p/h with >= 4 words
        first=None
        for m in re.finditer(r'<(p|h[1-6]|li)\b[^>]*>(.*?)</\1>',body,re.S):
            t=norm(m.group(2))
            if len(t.split())>=4: first=t; break
        kind='sub-page' if lb[1]>0 else 'lesson'
        if not first: ctx[(tmpl,kind,'no-text')]+=1; continue
        probe=" ".join(first.split()[:6]); idx=next((i for i,l in enumerate(wn) if probe in l),None)
        if idx is None: ctx[(tmpl,kind,'text-not-in-WT')]+=1; ex[(tmpl,kind,'text-not-in-WT')].append((code,hl[lb],first[:60])); continue
        tag='none'
        for j in range(idx, max(-1,idx-5), -1):
            ln=re.sub(r'\[/?RED TEXT\]','',wl[j]); m=re.findall(r'\[([^\]]{1,50})\]', ln)
            if m: tag=m[0].strip().lower(); break
        t=re.sub(r'\d+','N',tag)
        if re.search(r'end page|new page|page break|next page|page N|continued|part N|lesson N|\bN\.N\b',t): k='BOUNDARY-TAG:'+t[:30]
        elif re.match(r'h\d|hN',t): k='heading-tag'
        elif tag=='none': k='no-tag'
        else: k='other-tag:'+t[:24]
        ctx[(tmpl,kind,k)]+=1
        if len(ex[(tmpl,kind,k)])<4: ex[(tmpl,kind,k)].append((code,hl[lb],wl[idx][:80]))
print("page-label census (template | what | n):")
for k,v in sorted(cnt.items()): print(f"  {k[0]:12} {k[1]:18} {v:5}   modules {len(mods[(k[0],k[1].split()[0])])}")
print("\ngold-only pages by the writer's context at their first words (template | page kind | context | n):")
for k,v in sorted(ctx.items(), key=lambda x:-x[1])[:30]: print(f"  {k[0]:12} {k[1]:9} {k[2]:36} {v:4}   {ex[k][:2]}")
