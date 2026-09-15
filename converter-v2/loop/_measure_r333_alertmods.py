"""ROUND 333 PICK probe — the non-KB alert modifier classes Claude ships (`alert rhs`, `alert summary`): for each such Claude
box on a paired page, what wrapper does the GOLD put around the same lead text (matched by folded first words)?"""
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
def boxes(s, cls_re):
    out=[]
    for m in re.finditer(cls_re,s):
        st=m.start(); en=balanced(s,st); out.append((m.group(1), text(s[st:en])))
    return out
res=collections.Counter(); ex=collections.defaultdict(list)
for code in sorted(x for x in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,x))):
    tmpl=os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE,code)))
    for n,cp,hp in pairs(code):
        if re.search(r'acks|glossary',os.path.basename(hp),re.I): continue
        c=open(cp,encoding="utf-8",errors="replace").read().split('<div id="body"',1)[-1]
        g=open(hp,encoding="utf-8",errors="replace").read().split('<div id="body"',1)[-1]
        cb=[b for b in boxes(c,r'<div class="(alert[^"]*)"') if re.search(r"\b(rhs|summary)\b",b[0])]
        if not cb: continue
        gb=boxes(g,r'<div class="((?:alert|alertActivity|alertImage|whakatauki|super-content)[^"]*)"')
        for cls,txt in cb:
            key=" ".join(txt.split()[:8])
            tok="rhs" if " rhs" in " "+cls else "summary"
            hit=None
            if len(key)>=12:
                for gcls,gtxt in gb:
                    if key in gtxt: hit=gcls; break
                if hit is None and key in text(g): hit="(plain body — no box)"
            res[(tmpl,tok,"gold: "+(hit or "(text not found)"))]+=1
            if len(ex[(tmpl,tok,hit)])<2: ex[(tmpl,tok,hit)].append(f"{code}/{os.path.basename(cp)}")
for k,v in sorted(res.items(), key=lambda x:-x[1]): print(f"{v:4} {k}  e.g. {ex[(k[0],k[1],k[2][6:] if k[2].startswith('gold: ') else k[2])][:1]}")
