#!/usr/bin/env python3
"""_measure_r357_alertactivity.py — session 17 PICK probe: the gold's `div.alertActivity` sidebars (the KB 05B / 01F activity text sidebar) that
Claude does not ship — what is their WRITERS-TEMPLATE source? For every gold alertActivity on a paired page: its heading + first words, whether
that text exists in the module's parsed Writers Template (fuzzy: the first 40 normalised chars), and the bracket tag that precedes it there.
Per template family. Run from anywhere."""
import os, sys, re, json, collections, glob
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PARSED = os.path.join(ROOT, "03-All_Parsed_Files")
def norm(s): return re.sub(r'[^a-z0-9]+',' ',re.sub(r'<[^>]+>',' ',s).lower()).strip()
def wt_text(code):
    fs=[f for f in glob.glob(os.path.join(PARSED, code+"*_parsed.txt"))]
    out=[]
    for f in fs:
        try: out.append(open(f,encoding='utf8',errors='ignore').read())
        except Exception: pass
    return "\n".join(out)
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
tally=collections.Counter(); pages=collections.defaultdict(set); mods=collections.defaultdict(set); tags=collections.Counter(); heads=collections.Counter(); ex=collections.defaultdict(list)
claude_sites=collections.Counter()
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code)))
    wt=None
    for _, cp, hp in pairs(code):
        h=open(hp,encoding='utf8',errors='ignore').read(); c=open(cp,encoding='utf8',errors='ignore').read()
        gboxes=re.findall(r'<div class="alertActivity[^"]*"[^>]*>(.*?)</div>\s*</div>', h, re.S)
        cn=len(re.findall(r'class="alertActivity',c))
        if not gboxes: continue
        if wt is None: wt=wt_text(code); wtn=norm(wt); wtlines=wt.split("\n")
        for g in gboxes:
            hm=re.search(r'<h[1-6][^>]*>(.*?)</h[1-6]>',g,re.S); head=norm(hm.group(1))[:40] if hm else ''
            body=norm(re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>','',g,flags=re.S))
            probe=body[:40]
            found = bool(probe) and len(probe)>=12 and probe in wtn
            key=(tmpl,'IN-WT' if found else ('NO-SOURCE' if probe else 'EMPTY'))
            if key[1]=='EMPTY' and len(ex[(tmpl,'EMPTY')])<6: ex[(tmpl,'EMPTY')].append((code, os.path.basename(cp), re.sub(r'\s+',' ',g)[:160]))
            tally[key]+=1; pages[key].add(os.path.basename(cp)); mods[key].add(code); heads[(tmpl,head[:20])]+=1
            if found:
                # locate the WT line and the nearest preceding bracket tag
                idx=None
                for i,l in enumerate(wtlines):
                    if probe[:25] in norm(l): idx=i; break
                tag='?'
                if idx is not None:
                    for j in range(idx, max(-1,idx-4), -1):
                        ln=re.sub(r'\[/?RED TEXT\]','',wtlines[j])
                        m=re.findall(r'\[([^\]]{1,40})\]', ln)
                        if m: tag=m[0].strip().lower(); break
                tag=re.sub(r'\d+','N',tag)[:30]
                tags[(tmpl,tag)]+=1
                if len(ex[(tmpl,tag)])<4: ex[(tmpl,tag)].append((code, os.path.basename(cp), head[:30], body[:60]))
print("gold alertActivity sidebars on paired pages, by WT source:")
for k in sorted(tally): print(f"  {k[0]:12} {k[1]:10} boxes {tally[k]:4} pages {len(pages[k]):4} modules {len(mods[k]):4}")
print("\nIN-WT boxes by the nearest preceding bracket tag (template | tag | boxes):")
for (t,tag),v in sorted(tags.items(), key=lambda x:-x[1])[:40]: print(f"  {t:12} {v:4} {tag}")
print("\nheadings (top):")
for (t,hd),v in sorted(heads.items(), key=lambda x:-x[1])[:25]: print(f"  {t:12} {v:4} {hd}")
print("\nexamples:")
for k in sorted(ex, key=lambda k:-tags[k])[:12]:
    print(" ",k)
    for e in ex[k]: print("    ",e)
