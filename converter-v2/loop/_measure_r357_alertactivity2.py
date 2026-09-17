#!/usr/bin/env python3
"""_measure_r357_alertactivity2.py — session 17 PICK probe, stage 2: for every gold alertActivity box whose text IS in the Writers Template,
what does CLAUDE ship for the same text on the paired page — an alertActivity, another alert-family box (class), or free body — and which
writer tag introduced it. Also the reverse share: writer [alert]/[important]/... tags (non-positional) → does the gold ship them as a sidebar
(alertActivity / alert top) or as the full-width alert?"""
import os, sys, re, json, collections, glob
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); PARSED = os.path.join(ROOT, "03-All_Parsed_Files")
def norm(s): return re.sub(r'[^a-z0-9]+',' ',re.sub(r'<[^>]+>',' ',s).lower()).strip()
def wt_lines(code):
    out=[]
    for f in glob.glob(os.path.join(PARSED, code+"*_parsed.txt")):
        try: out += open(f,encoding='utf8',errors='ignore').read().split("\n")
        except Exception: pass
    return out
def claude_ctx(c, probe):
    """the class of the nearest enclosing div.alert*/alertActivity for the first occurrence of probe in the Claude page's text"""
    # walk the page as tags+text, keep a stack of div classes
    stack=[]; 
    for m in re.finditer(r'<(/?)(\w+)([^>]*)>|([^<]+)', c):
        if m.group(4):
            if probe[:25] in norm(m.group(4)):
                for cls in reversed(stack):
                    if cls.startswith('alert') or cls.startswith('activity'): return cls
                return 'free-body'
            continue
        tag=m.group(2).lower()
        if tag=='div':
            if m.group(1): 
                if stack: stack.pop()
            else:
                cm=re.search(r'class="([^"]*)"', m.group(3)); stack.append(cm.group(1) if cm else '')
    return 'NOT-ON-PAGE'
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
res=collections.Counter(); pages=collections.defaultdict(set); mods=collections.defaultdict(set); ex=collections.defaultdict(list)
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code))); wl=None
    for _, cp, hp in pairs(code):
        h=open(hp,encoding='utf8',errors='ignore').read()
        gboxes=re.findall(r'<div class="alertActivity[^"]*"[^>]*>(.*?)</div>\s*</div>', h, re.S)
        if not gboxes: continue
        c=open(cp,encoding='utf8',errors='ignore').read()
        if wl is None: wl=wt_lines(code); wn=[norm(l) for l in wl]
        for g in gboxes:
            body=norm(re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>','',g,flags=re.S)); probe=body[:40]
            if len(probe)<12: continue
            idx=next((i for i,l in enumerate(wn) if probe[:25] in l), None)
            if idx is None: continue
            tag='?'
            for j in range(idx, max(-1,idx-4), -1):
                ln=re.sub(r'\[/?RED TEXT\]','',wl[j]); m=re.findall(r'\[([^\]]{1,40})\]', ln)
                if m: tag=re.sub(r'\d+','N',m[0].strip().lower())[:28]; break
            ctx=claude_ctx(c, probe)
            ctx=re.sub(r'\s+',' ',ctx).strip()
            key=(tmpl, tag, ctx); res[key]+=1; pages[key].add(os.path.basename(cp)); mods[key].add(code)
            if len(ex[key])<3: ex[key].append((code, os.path.basename(cp), wl[idx][:90] if idx is not None else ''))
print("gold alertActivity (IN-WT) → Claude's rendering of the same text (template | writer tag | Claude context | boxes | pages | modules)")
for k,v in sorted(res.items(), key=lambda x:-x[1])[:45]:
    print(f"  {k[0]:12} {k[1]:28} {k[2]:36} {v:4} {len(pages[k]):4} {len(mods[k]):4}")
print("\nby Claude context only:")
byctx=collections.Counter(); byp=collections.defaultdict(set)
for k,v in res.items(): byctx[(k[0],k[2])]+=v; byp[(k[0],k[2])] |= pages[k]
for k,v in sorted(byctx.items(), key=lambda x:-x[1]): print(f"  {k[0]:12} {k[1]:36} {v:4} boxes {len(byp[k]):4} pages")
print("\nexamples:")
for k in sorted(ex, key=lambda k:-res[k])[:10]:
    print(" ",k, res[k])
    for e in ex[k]: print("    ",e)
