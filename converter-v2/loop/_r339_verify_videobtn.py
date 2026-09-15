"""_r339_verify_videobtn.py — ROUND 339 standing verifier: anchored buttons whose href is a VIDEO url (youtube watch/shorts/embed, youtu.be, vimeo video id) across the whole Claude corpus. Run under WSL from outputs."""
import os,re,sys,collections
sys.path.insert(0, os.path.join('..','reference','tests')); import _corpus
OUT=os.path.join('..','..','01-Claude_Modules_')
HOST=re.compile(r'youtube\.com/(?:watch\?|shorts/|embed/)|youtu\.be/|vimeo\.com/(?:video/)?\d',re.I)
A=re.compile(r'<a href="([^"]+)"[^>]*>\s*<div class="([^"]*button[^"]*)">([^<]*)</div>\s*</a>',re.I)
tot=collections.Counter(); mods=set(); pages=set(); ex=[]
for code in _corpus.mods(OUT):
    d=_corpus.mdir(OUT,code)
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        if not f.endswith('.html'): continue
        h=open(os.path.join(d,f),encoding='utf-8',errors='replace').read()
        for m in A.finditer(h):
            if HOST.search(m.group(1)):
                tot[m.group(2)]+=1; mods.add(code); pages.add(code+'/'+f)
                if len(ex)<12: ex.append((code,f,m.group(2),m.group(3).strip()[:40],m.group(1)[:60]))
print('anchored buttons with a VIDEO href corpus-wide:',sum(tot.values()),'| pages',len(pages),'| modules',len(mods))
print('by class:',dict(tot))
for e in ex: print('  ',e)
