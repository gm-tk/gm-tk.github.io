#!/usr/bin/env python3
"""_measure_r357_br.py — session 17 PICK probe: the gold's `<br>` lines the skeleton counts and Claude lacks (position-free deficit 1626 / 597
pages): where do they sit — inside a text paragraph (a writer's soft line break the gold KEPT as <br>, while r227 ships split <p>s), as
spacing (<p><br></p>, doubled <br>), inside a table cell, inside a widget, or in a list item? And on the pages concerned, does the WT paragraph
carry a soft break (the r227 '\n') at that spot? Per template. The r227 measurement ('split-p 84 vs br 31 on the top-8 carriers') is re-done
over EVERY paired page."""
import os, sys, re, collections, html
HERE=os.path.dirname(os.path.abspath(__file__)); TESTS=os.path.normpath(os.path.join(HERE,'..','reference','tests')); sys.path.insert(0,TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
WIDGET=re.compile(r'class="[^"]*\b(carousel|accordion|flipCard|dragAndDrop|clickDrop|TKmodal|tab-content|speechBubble|mcq|dropQuiz|selfCheck|cv2-)',re.I)
codes=sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,d)))
ctx=collections.Counter(); pg=collections.defaultdict(set); ex=collections.defaultdict(list); tot=collections.Counter()
for code in codes:
    tmpl=os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE,code)))
    for _,cp,hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary',os.path.basename(hp)+os.path.basename(cp),re.I): continue
        h=open(hp,encoding='utf8',errors='ignore').read(); c=open(cp,encoding='utf8',errors='ignore').read()
        gb=len(re.findall(r'<br\s*/?>',h,re.I)); cb=len(re.findall(r'<br\s*/?>',c,re.I))
        tot[(tmpl,'gold')]+=gb; tot[(tmpl,'claude')]+=cb
        if gb<=cb: continue
        body=h[h.find('id="body"'):] if 'id="body"' in h else h
        # walk with a stack to classify each br
        stack=[]; 
        for m in re.finditer(r'<(/?)([a-zA-Z0-9]+)([^>]*)>|([^<]+)',body):
            if m.group(4): 
                if stack and m.group(4).strip(): stack[-1][2]+=1   # text seen inside current element
                continue
            close,tag,attrs=m.group(1),m.group(2).lower(),m.group(3)
            if tag=='br':
                par=stack[-1][0] if stack else '?'
                inwidget=any(s[1] for s in stack)
                # look at what follows the br: another br / close tag / text
                after=body[m.end():m.end()+40].lstrip()
                kind=('spacing' if re.match(r'<br|</p>|</div>|<p>',after,re.I) or (stack and stack[-1][2]==0) else 'inline')
                k=(tmpl, 'widget' if inwidget else par, kind); ctx[k]+=1; pg[k].add(os.path.basename(cp))
                if len(ex[k])<3: ex[k].append((code,os.path.basename(hp),re.sub(r'\s+',' ',body[max(0,m.start()-70):m.end()+50])[:130]))
                continue
            if tag in ('img','meta','link','hr','input','source','wbr','area','base','col','embed','track'): continue
            if close:
                for i in range(len(stack)-1,-1,-1):
                    if stack[i][0]==tag: del stack[i:]; break
            elif not attrs.rstrip().endswith('/'):
                stack.append([tag, bool(WIDGET.search(attrs)) or (stack and stack[-1][1]), 0])
print("total <br>:", dict(tot))
print("\ngold <br> on pages where gold > Claude (template | parent | kind | n | pages):")
for k,v in sorted(ctx.items(), key=lambda x:-x[1])[:30]: print(f"  {k[0]:12} {k[1]:8} {k[2]:8} {v:5} {len(pg[k]):4}   {ex[k][0][2]}")
