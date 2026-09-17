#!/usr/bin/env python3
"""_measure_r357_plainmath.py — session 17 PICK probe: the gold's <math> elements that have NO OMML source (the human developer converted the
writer's PLAIN-TEXT arithmetic to MathML). For every gold <math> on a paired page: its collapsed text; is it on Claude's page as <math>
(OMML-sourced, r346)? else is the text in the Writers Template as plain text? Then the REVERSE share: WT lines that carry an arithmetic
expression (digits with × ÷ + − = / ^ or a fraction) in the modules concerned — what share does the gold ship as <math>?"""
import os, sys, re, json, collections, glob
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); PARSED = os.path.join(ROOT, "03-All_Parsed_Files")
import html as H
def mtext(m):
    t=re.sub(r'<[^>]+>','',m); t=H.unescape(t); return re.sub(r'\s+','',t)
def wt_text(code):
    out=[]
    for f in glob.glob(os.path.join(PARSED, code+"*_parsed.txt")):
        try: out.append(open(f,encoding='utf8',errors='ignore').read())
        except Exception: pass
    return "\n".join(out)
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
cls=collections.Counter(); pg=collections.defaultdict(set); md=collections.defaultdict(set); ex=collections.defaultdict(list)
permod=collections.defaultdict(collections.Counter)
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code))); wt=None
    for _, cp, hp in pairs(code):
        h=open(hp,encoding='utf8',errors='ignore').read()
        gm=re.findall(r'<math.*?</math>',h,re.S)
        if not gm: continue
        c=open(cp,encoding='utf8',errors='ignore').read()
        cm=set(mtext(x) for x in re.findall(r'<math.*?</math>',c,re.S))
        if wt is None: wt=wt_text(code); wtc=re.sub(r'\s+','',wt)
        for m in gm:
            t=mtext(m)
            if t in cm: k='CLAUDE-HAS'
            elif len(t)>=2 and t in wtc: k='PLAIN-IN-WT'
            elif len(t)>=2 and re.sub(r'[×x*·]','',t).replace('−','-') in re.sub(r'[×x*·]','',wtc).replace('−','-'): k='PLAIN-IN-WT~'
            else: k='NO-SOURCE'
            cls[(tmpl,k)]+=1; pg[(tmpl,k)].add(os.path.basename(cp)); md[(tmpl,k)].add(code); permod[code][k]+=1
            if len(ex[(tmpl,k)])<8: ex[(tmpl,k)].append((code, os.path.basename(cp), t[:50]))
print("gold <math> elements on paired pages by source (template | class | elements | pages | modules):")
for k in sorted(cls): print(f"  {k[0]:12} {k[1]:13} {cls[k]:5} {len(pg[k]):4} {len(md[k]):4}")
print("\nper module:")
for code,cc in sorted(permod.items()): print(f"  {code:8}", dict(cc))
print("\nexamples:")
for k in ex:
    print(" ",k)
    for e in ex[k]: print("    ",e)
