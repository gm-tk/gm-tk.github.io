"""Session 17 PICK probe: the `body.mathJax` class — gold vs Claude per paired page, with the <math> presence on each side (new evidence since the session-5 decline: r346's OMML extraction)."""
import os, sys, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
rows=[]
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code)))
    for n, cp, hp in pairs(code):
        c=open(cp,encoding='utf8',errors='ignore').read(); h=open(hp,encoding='utf8',errors='ignore').read()
        def body_mj(s):
            m=re.search(r'<body[^>]*class="([^"]*)"',s); return bool(m and 'mathJax' in m.group(1))
        rows.append((code,tmpl,os.path.basename(cp),body_mj(h),body_mj(c),len(re.findall(r'<math[\s>]',h)),len(re.findall(r'<math[\s>]',c))))
# corpus-wide
gm=[r for r in rows if r[3]]; cm=[r for r in rows if r[4]]
print("paired pages",len(rows),"gold mathJax pages",len(gm),"claude mathJax pages",len(cm))
print("gold mathJax & gold <math>:",sum(1 for r in gm if r[5]),"| gold mathJax & no gold <math>:",sum(1 for r in gm if not r[5]))
print("gold <math> pages:",sum(1 for r in rows if r[5]),"of which gold mathJax:",sum(1 for r in rows if r[5] and r[3]))
print("claude <math> pages:",sum(1 for r in rows if r[6]),"claude mathJax:",len(cm))
gap=[r for r in rows if r[3] and not r[4]]; over=[r for r in rows if r[4] and not r[3]]
print("GAP gold mathJax / claude not:",len(gap),"pages /",len(set(r[0] for r in gap)),"modules; OVER claude mathJax / gold not:",len(over))
# per module: does the gold put mathJax on every page of a module that has any?
bym=collections.defaultdict(list)
for r in rows: bym[r[0]].append(r)
print("\nmodule | tmpl | pages | gold mathJax pages | gold <math> pages | claude mathJax | claude <math> | GAP pages")
for m,rs in bym.items():
    if any(r[3] for r in rs) or any(r[4] for r in rs):
        print(f"{m:8} {rs[0][1]:12} {len(rs):3} {sum(1 for r in rs if r[3]):3} {sum(1 for r in rs if r[5]):3} {sum(1 for r in rs if r[4]):3} {sum(1 for r in rs if r[6]):3} {sum(1 for r in rs if r[3] and not r[4]):3}")
# modules where gold has mathJax on ALL pages
allm=[m for m,rs in bym.items() if all(r[3] for r in rs)]
somem=[m for m,rs in bym.items() if any(r[3] for r in rs) and not all(r[3] for r in rs)]
print("\ngold mathJax on ALL pages:",len(allm),allm); print("gold mathJax on SOME pages:",len(somem),somem)
# among gold-mathJax modules: is there any equation in the module (gold side)?
for m in allm+somem:
    rs=bym[m]; print(m, "gold <math> pages", sum(1 for r in rs if r[5]), "claude <math> pages", sum(1 for r in rs if r[6]))
