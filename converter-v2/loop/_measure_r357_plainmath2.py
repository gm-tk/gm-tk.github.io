#!/usr/bin/env python3
"""_measure_r357_plainmath2.py — session 17 PICK probe, stage 2 (the REVERSE share test): every arithmetic expression the WRITER typed as plain
text (an infix expression with digits on both sides of × ÷ + − = or a bare fraction a/b) in every module — does the GOLD ship it inside <math>
(the human's MathML conversion) or as plain text? Per subject family and template. The share decides whether "plain arithmetic → MathML" is a
derivable rule (≥ 0.60) or the human's per-module choice."""
import os, sys, re, json, collections, glob, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); PARSED = os.path.join(ROOT, "03-All_Parsed_Files")
EXPR = re.compile(r'(?<![\w/])(\$?\d[\d,]*(?:\.\d+)?\s*(?:[×÷=+−\-*/]|x(?=\s*\d))\s*(?:\$?\d[\d,]*(?:\.\d+)?|[a-z])(?:\s*[×÷=+−\-*/]\s*\$?\d[\d,]*(?:\.\d+)?)*)', re.I)
FRAC = re.compile(r'(?<![\d/])(\d{1,3}/\d{1,3})(?![\d/])')
def collapse(s): return re.sub(r'\s+','',H.unescape(s))
def wt_lines(code):
    out=[]
    for f in glob.glob(os.path.join(PARSED, code+"*_parsed.txt")):
        try: out += open(f,encoding='utf8',errors='ignore').read().split("\n")
        except Exception: pass
    return out
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
res=collections.Counter(); ex=collections.defaultdict(list); permod=collections.defaultdict(collections.Counter)
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code))); subj=re.sub(r'\d.*','',code)[:3]
    gold_pages=[]
    for _, cp, hp in pairs(code):
        h=open(hp,encoding='utf8',errors='ignore').read()
        maths=[collapse(re.sub(r'<[^>]+>','',m)) for m in re.findall(r'<math.*?</math>',h,re.S)]
        plain=collapse(re.sub(r'<[^>]+>',' ',re.sub(r'<math.*?</math>','',h,flags=re.S)))
        gold_pages.append((maths,plain))
    if not gold_pages: continue
    seen=set()
    for l in wt_lines(code):
        if l.startswith('•') or 'RED TEXT' in l and len(l)<40: pass
        for m in list(EXPR.finditer(l)) + list(FRAC.finditer(l)):
            e=m.group(1).strip()
            if re.fullmatch(r'\d{1,2}/\d{1,2}',e) and re.search(r'(19|20)\d\d',l): continue   # a date
            if re.search(r'(19|20)\d\d\s*[-−]\s*(19|20)\d\d', e): continue                    # a year range
            ce=collapse(e).replace('−','-').replace('x','×').replace('*','×')
            if len(ce)<3 or ce in seen: continue
            seen.add(ce)
            key=None
            for maths,plain in gold_pages:
                mm=[x.replace('−','-').replace('x','×') for x in maths]
                if any(ce==x or (len(ce)>=5 and ce in x) for x in mm): key='GOLD-MATH'; break
                if ce.replace('/','') in [x for x in mm] and '/' in ce: key='GOLD-MATH'; break
            if key is None:
                for maths,plain in gold_pages:
                    if ce in plain.replace('−','-').replace('x','×'): key='GOLD-PLAIN'; break
            if key is None: key='NOT-IN-GOLD'
            res[(tmpl,subj,key)]+=1; permod[code][key]+=1
            if len(ex[(tmpl,subj,key)])<5: ex[(tmpl,subj,key)].append((code,e[:40]))
print("writer plain-text arithmetic expressions → gold form (template | subject | class | n):")
by=collections.defaultdict(collections.Counter)
for (t,s,k),v in res.items(): by[(t,s)][k]+=v
for (t,s),cc in sorted(by.items(), key=lambda x:-sum(x[1].values())):
    tot=sum(cc.values()); print(f"  {t:12} {s:4} total {tot:4}  math {cc['GOLD-MATH']:4} ({cc['GOLD-MATH']/tot:.2f})  plain {cc['GOLD-PLAIN']:4}  not-in-gold {cc['NOT-IN-GOLD']:4}")
print("\nper module (modules with ≥ 5 expressions):")
for code,cc in sorted(permod.items(), key=lambda x:-sum(x[1].values())):
    tot=sum(cc.values())
    if tot>=5: print(f"  {code:8} total {tot:4} math {cc['GOLD-MATH']:4} ({cc['GOLD-MATH']/tot:.2f}) plain {cc['GOLD-PLAIN']:4} not-in-gold {cc['NOT-IN-GOLD']:4}")
print("\nexamples:")
for k in sorted(ex, key=lambda k:-res[k])[:12]: print(" ",k,res[k],ex[k])
