#!/usr/bin/env python3
"""_measure_r357_textmatch.py — session 17 PICK probe: compare_structure's "text-matched 34.5 %" decomposed. For every Claude content element
(compare_structure's own parse — free body only, widget subtrees skipped) that does NOT match a gold element on the paired page by
(tag family, text[:80]): WHY? (a) same text under another tag family on the page (a structural swap — which pair?), (b) the text is on
ANOTHER page of the module (pagination), (c) a near match — the gold element's text contains / is contained in Claude's (a prefix / suffix
difference — list number, trailing words), (d) Claude-only text (notes, box chrome, To-Do lines), (e) nowhere in the gold module. Per
template; the swap pairs and the near-match shapes sized in pages."""
import os, sys, re, collections
HERE=os.path.dirname(os.path.abspath(__file__)); TESTS=os.path.normpath(os.path.join(HERE,'..','reference','tests')); sys.path.insert(0,TESTS)
import _corpus, compare_structure as CS
from compare_structure import parse_page, page_sort_key, CLAUDE, HUMAN
codes=sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,d)))
fam=lambda t:'h' if t.startswith('h') else t
reason=collections.Counter(); rpg=collections.defaultdict(set); swap=collections.Counter(); spg=collections.defaultdict(set); near=collections.Counter(); npg=collections.defaultdict(set); ex=collections.defaultdict(list)
tot=0; matched=0
NOTE=re.compile(r'^(note from|kate scanlon|nadia stanton|caroline schwer|writers? note|❗|to do|todo|cs:|red flag)',re.I)
for code in codes:
    cdir=_corpus.mdir(CLAUDE,code); hdir=_corpus.mdir(HUMAN,code)
    if not os.path.isdir(cdir) or not os.path.isdir(hdir): continue
    tmpl=os.path.basename(os.path.dirname(cdir))
    cpages=sorted([f for f in os.listdir(cdir) if f.endswith('.html')],key=page_sort_key); hpages=sorted([f for f in os.listdir(hdir) if f.endswith('.html')],key=page_sort_key)
    hparsed=[parse_page(os.path.join(hdir,f)) for f in hpages]
    modtexts=collections.defaultdict(set)   # text -> set(tag fam) across the whole gold module
    modblob=[]
    for hp in hparsed:
        for e in hp.elements: modtexts[e['text'][:80]].add(fam(e['tag'])); modblob.append(e['text'])
    modblob=" \u0001 ".join(modblob)
    for ci in range(min(len(cpages),len(hpages))):
        cp=parse_page(os.path.join(cdir,cpages[ci])); hp=hparsed[ci]
        hindex=collections.defaultdict(list); htexts=collections.defaultdict(set); pageblob=" \u0001 ".join(e['text'] for e in hp.elements)
        for e in hp.elements: hindex[(fam(e['tag']),e['text'][:80])].append(e); htexts[e['text'][:80]].add(fam(e['tag']))
        for e in cp.elements:
            tot+=1; t=e['text'][:80]; f=fam(e['tag'])
            if hindex.get((f,t)): matched+=1; continue
            if e['tag'] in ('img','iframe','audio','table'): r='media/table-unmatched'
            elif not t: r='empty'
            elif NOTE.search(e['text']) or e['text'].startswith(('❗','note from')): r='claude-note'
            elif t in htexts: 
                r='SWAP-tag'; k=(tmpl,f,'→',sorted(htexts[t])[0]); swap[k]+=1; spg[k].add(cpages[ci])
                if len(ex[k])<3: ex[k].append((code,cpages[ci],e['text'][:70]))
            elif len(t)>=12 and t in pageblob: r='NEAR-contained'   # Claude text is a substring of a gold element (gold longer / merged)
            elif len(t)>=12 and any(len(k)>=12 and k in e['text'] for k in htexts): r='NEAR-contains'   # a gold element is a substring of Claude's (Claude longer / merged)
            elif t in modtexts: r='OTHER-PAGE'
            elif len(t)>=12 and t in modblob: r='OTHER-PAGE-contained'
            else: r='NOT-IN-GOLD'
            reason[(tmpl,r)]+=1; rpg[(tmpl,r)].add(cpages[ci])
            if r.startswith('NEAR') and len(ex[(tmpl,r)])<6: ex[(tmpl,r)].append((code,cpages[ci],e['tag'],e['text'][:90]))
            if r=='NOT-IN-GOLD' and len(ex[(tmpl,r)])<8: ex[(tmpl,r)].append((code,cpages[ci],e['tag'],e['text'][:90]))
print("Claude content elements",tot,"matched",matched,f"({matched/tot:.1%})")
print("\nunmatched by reason (template | reason | n | pages):")
for k,v in sorted(reason.items(), key=lambda x:-x[1]): print(f"  {k[0]:12} {k[1]:22} {v:6} {len(rpg[k]):5}")
print("\nSWAP pairs (Claude tag → gold tag, same text; n | pages):")
for k,v in swap.most_common(20): print(f"  {k[0]:12} {k[1]:5} {k[2]} {k[3]:5} {v:6} {len(spg[k]):5}   {ex[k][:2]}")
print("\nexamples:")
for k in ex:
    if isinstance(k[1],str) and k[1].startswith(('NEAR','NOT')): print(" ",k); [print("    ",e) for e in ex[k]]
