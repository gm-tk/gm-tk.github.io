"""ROUND 333 PICK probe part 3 — discriminator hunt for the `alert rhs` boxes (Standard): context features of each Claude box
(what precedes it: an activity box / plain content; its length; whether it opens with a heading) × the gold's wrapper."""
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
res=collections.Counter(); rows=[]
for code in sorted(x for x in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,x))):
    tmpl=os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE,code)))
    if tmpl!="Standard": continue
    for n,cp,hp in pairs(code):
        if re.search(r'acks|glossary',os.path.basename(hp),re.I): continue
        c=open(cp,encoding="utf-8",errors="replace").read().split('<div id="body"',1)[-1]
        g=open(hp,encoding="utf-8",errors="replace").read().split('<div id="body"',1)[-1]
        gb=[]
        for m in re.finditer(r'<div class="((?:alert|alertActivity)[^"]*)"',g):
            st=m.start(); gb.append((m.group(1),text(g[st:balanced(g,st)])))
        for m in re.finditer(r'<div class="(alert[^"]*\brhs\b[^"]*)"',c):
            st=m.start(); en=balanced(c,st); raw=c[st:en]; txt=text(raw); key=" ".join(txt.split()[:8])
            hit="-"
            if len(key)>=12:
                for gcls,gtxt in gb:
                    if key in gtxt: hit=re.sub(r"\s*(paddingL|alertL)","",gcls); break
                if hit=="-" and key in text(g): hit="plain"
            if hit=="-": continue
            before=c[:st]
            # the last opened-and-closed block before this box (skip row/col wrappers)
            prev=re.findall(r'<div class="(activity[^"]*|alert[^"]*|cv2-interactive[^"]*)"',before[-4000:])
            prev_act="after-activity" if prev and prev[-1].startswith("activity") and balanced(before, before.rfind('<div class="'+prev[-1]+'"'))>=len(before)-200 else "after-content"
            words=len(txt.split()); heading=bool(re.match(r'\s*<div class="alert[^"]*">\s*<h\d',raw))
            in_act = "in-activity" if re.search(r'<div class="activity[^"]*"[^>]*>(?:(?!</div>\s*</div>\s*</div>).)*$',before[-3000:],re.S) and before[-3000:].count('<div class="activity')>before[-3000:].count("</div>")-0 else ""
            res[(hit, prev_act, "h" if heading else "noh", "short" if words<=40 else "long")]+=1
            rows.append((code,os.path.basename(cp),hit,prev_act,heading,words))
for k,v in sorted(res.items()): print(f"{v:4} {k}")
print()
by=collections.defaultdict(collections.Counter)
for code,p,hit,pa,h,w in rows: by[code[:4]][hit]+=1
for s,cnt in sorted(by.items()): print(s, dict(cnt))
