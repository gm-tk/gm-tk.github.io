"""ROUND 333 PICK probe part 4 — the GOLD's enclosing COLUMN + row-sibling shape for every rhs-box match (Standard):
is the gold box a side column (col-md-4) beside a col-md-8 sibling, or a full-width box?"""
import os,re,collections,sys,unicodedata
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,"..","reference","tests"))
import _corpus
from anchor_compare import CLAUDE
from _discrepancy_audit import pairs
def balanced(s,st):
    d=0
    for m in re.finditer(r"<div\b|</div>",s[st:]):
        d+=1 if m.group(0)=="<div" else -1
        if d==0: return st+m.end()
    return len(s)
def fold(t):
    t=unicodedata.normalize("NFKD",t); t="".join(ch for ch in t if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+"," ",t.lower()).strip()
def text(html): return fold(re.sub(r"<[^>]+>"," ",re.sub(r'<p class="cv2-note"[^>]*>.*?</p>',"",html,flags=re.S)))
def enclosing_col(g, st):
    # nearest enclosing <div class="col..."> whose balanced span contains st
    j=st
    while True:
        j=g.rfind('<div class="col',0,j)
        if j<0: return "?", None
        if balanced(g,j)>st: return re.search(r'class="([^"]*)"',g[j:j+80]).group(1), j
        j-=1
def sibling_cols(g, colst):
    # the row enclosing this col → list of its direct col classes
    j=colst
    while True:
        j=g.rfind('<div class="row',0,j)
        if j<0: return []
        if balanced(g,j)>colst: break
        j-=1
    en=balanced(g,j); seg=g[j:en]; cols=[]; k=len('<div class="row')
    inner=seg[seg.find(">")+1:]
    # direct children: walk top-level divs
    pos=0; depth=0
    while True:
        m=re.compile(r"<div\b|</div>").search(inner,pos)
        if not m: break
        if m.group(0)=="<div":
            if depth==0:
                cm=re.match(r'<div class="([^"]*)"',inner[m.start():]); cols.append(cm.group(1) if cm else "(no class)")
            depth+=1
        else: depth-=1
        pos=m.end()
        if depth<0: break
    return cols
res=collections.Counter(); byhit=collections.defaultdict(collections.Counter)
for code in sorted(x for x in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,x))):
    tmpl=os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE,code)))
    if tmpl!="Standard": continue
    for n,cp,hp in pairs(code):
        if re.search(r'acks|glossary',os.path.basename(hp),re.I): continue
        c=open(cp,encoding="utf-8",errors="replace").read().split('<div id="body"',1)[-1]
        g=open(hp,encoding="utf-8",errors="replace").read().split('<div id="body"',1)[-1]
        gb=[]
        for m in re.finditer(r'<div class="((?:alert|alertActivity)[^"]*)"',g):
            st=m.start(); gb.append((m.group(1),text(g[st:balanced(g,st)]),st))
        for m in re.finditer(r'<div class="(alert[^"]*\brhs\b[^"]*)"',c):
            st=m.start(); txt=text(c[st:balanced(c,st)]); key=" ".join(txt.split()[:8])
            if len(key)<12: continue
            for gcls,gtxt,gst in gb:
                if key in gtxt:
                    col,colst=enclosing_col(g,gst); sib=sibling_cols(g,colst) if colst else []
                    colw=re.sub(r"\s*(offset-md-0|col-12|paddingL|paddingR)","",col).strip()
                    hit=re.sub(r"\s*(paddingL|alertL)","",gcls)
                    shape="side(col-md-4)" if "col-md-4" in col else ("full" if col.startswith("col-12") or col=="col-md-12 col-12" else col)
                    res[(hit,shape,"|".join(re.sub(r" col-12| offset-md-0","",s) for s in sib))]+=1
                    byhit[hit][shape]+=1
                    break
for k,v in sorted(res.items(), key=lambda x:(x[0][0],-x[1])): print(f"{v:4} {k}")
print(); print({h:dict(c) for h,c in byhit.items()})
