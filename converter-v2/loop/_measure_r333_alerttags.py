"""ROUND 333 PICK probe part 2 — for each Claude `alert rhs` / `alert summary` box on a paired page: the WRITER'S bracket
spelling (from the _parsed.txt line carrying the box's lead words) crossed with what the GOLD wraps the same text in."""
import os,re,collections,sys,unicodedata,glob
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,"..","reference","tests"))
import _corpus
from anchor_compare import CLAUDE, HUMAN
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
        st=m.start(); en=balanced(s,st); out.append((m.group(1), text(s[st:en]), s[st:en]))
    return out
def wt_lines(code):
    d=_corpus.mdir(HUMAN,code); fs=[f for f in glob.glob(os.path.join(d,"*_parsed.txt")) if "media list" not in os.path.basename(f).lower() or "writers template" in os.path.basename(f).lower()]
    out=[]
    for f in fs:
        for ln in open(f,encoding="utf-8",errors="replace"): out.append(ln.rstrip("\n"))
    return out
res=collections.Counter(); ex=collections.defaultdict(list)
for code in sorted(x for x in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,x))):
    tmpl=os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE,code)))
    if tmpl!="Standard": continue
    lines=None
    for n,cp,hp in pairs(code):
        if re.search(r'acks|glossary',os.path.basename(hp),re.I): continue
        c=open(cp,encoding="utf-8",errors="replace").read().split('<div id="body"',1)[-1]
        g=open(hp,encoding="utf-8",errors="replace").read().split('<div id="body"',1)[-1]
        cb=[b for b in boxes(c,r'<div class="(alert[^"]*)"') if re.search(r"\b(rhs|summary)\b",b[0])]
        if not cb: continue
        if lines is None: lines=wt_lines(code)
        gb=boxes(g,r'<div class="((?:alert|alertActivity|alertImage|whakatauki|super-content)[^"]*)"')
        for cls,txt,raw in cb:
            key=" ".join(txt.split()[:8]); tok="rhs" if " rhs" in " "+cls else "summary"
            hit=None
            if len(key)>=12:
                for gcls,gtxt,_ in gb:
                    if key in gtxt: hit=gcls; break
                if hit is None and key in text(g): hit="plain"
            # writer tag: the parsed line whose fold contains the first 5 words
            k5=" ".join(txt.split()[:5]); tag="?"
            for ln in lines:
                if k5 and k5 in fold(ln):
                    tags=re.findall(r"\[[^\]]*\]",ln); tags=[t for t in tags if re.search(r"alert|rhs|rhc|summary|side|box",t,re.I)]
                    tag=" ".join(tags)[:60] if tags else "(no alert tag on line)"; break
            res[(tok,tag.lower(),hit or "-")]+=1
            if len(ex[(tok,tag.lower(),hit)])<1: ex[(tok,tag.lower(),hit)].append(f"{code}/{os.path.basename(cp)}")
for k,v in sorted(res.items(), key=lambda x:(x[0][0],-x[1])): print(f"{v:4} {k}  {ex[(k[0],k[1],k[2] if k[2]!='-' else None)][:1]}")
