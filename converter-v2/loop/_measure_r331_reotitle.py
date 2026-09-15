"""ROUND 331 PICK probe — the bilingual SECTION TITLE ([H2] after a [H1] N.M id): where does the gold put it (inside the
section's activity box / outside before it) and at what level; vs Claude. All 8 writer-id modules (WT .docx read directly)."""
import os,re,sys,zipfile,collections
from xml.etree import ElementTree as ET
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,"..","reference","tests"))
import _corpus
from anchor_compare import CLAUDE, HUMAN
W="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
def cells(path):
    z=zipfile.ZipFile(path); root=ET.fromstring(z.read("word/document.xml")); out=[]
    for tr in root.iter(W+"tr"):
        tcs=tr.findall(W+"tc")
        out.append([ "\n".join("".join(t.text or "" for t in p.iter(W+"t")) for p in tc.iter(W+"p")) for tc in tcs])
    return out
def balanced(s,st):
    d=0
    for m in re.finditer(r"<div\b|</div>",s[st:]):
        d+=1 if m.group(0)=="<div" else -1
        if d==0: return st+m.end()
    return len(s)
def fold(t): return re.sub(r"[^a-z0-9āēīōū]+"," ",t.lower()).strip()
def find_title(html,title):
    """(level, inside_activity) of the heading whose text folds to the title; None if not found."""
    f=fold(title)
    if not f: return None
    for m in re.finditer(r"<h([1-6])[^>]*>(.*?)</h\1>",html,re.S):
        t=fold(re.sub(r"<[^>]+>","",m.group(2)))
        if t==f or (len(f)>8 and (t.startswith(f) or f.startswith(t))):
            # inside an activity div?
            inside=False
            for a in re.finditer(r'<div class="[^"]*\bactivity\b[^"]*"',html):
                if a.start()<m.start()<balanced(html,a.start()): inside=True; break
            return (m.group(1), inside)
    return None
gold=collections.Counter(); claude=collections.Counter(); per=collections.defaultdict(collections.Counter)
for code in ["PNR101","PNR102","PNR104","TRR109","TRR110","TRR111","TRR112","TRR113"]:
    gdir=_corpus.mdir(HUMAN,code); cdir=_corpus.mdir(CLAUDE,code)
    wt=[os.path.join(gdir,f) for f in os.listdir(gdir) if f.lower().endswith(".docx") and "media list" not in f.lower()]
    if not wt: continue
    rows=cells(wt[0]); titles=[]
    for i,r in enumerate(rows):
        if r and re.match(r"^\s*\[H1\]\s*\d{1,2}\.\d{1,2}\s*$",r[0].strip()):
            nxt=rows[i+1] if i+1<len(rows) else None
            if nxt and re.match(r"^\s*\[H2\]",nxt[0].strip()): titles.append(re.sub(r"^\s*\[H2\]\s*","",nxt[0].strip()))
    ghtml="\n".join(open(os.path.join(gdir,f),encoding="utf-8",errors="replace").read() for f in os.listdir(gdir) if f.endswith(".html"))
    chtml="\n".join(open(os.path.join(cdir,f),encoding="utf-8",errors="replace").read() for f in os.listdir(cdir) if f.endswith(".html")) if cdir and os.path.isdir(cdir) else ""
    for t in titles:
        g=find_title(ghtml,t); c=find_title(chtml,t) if chtml else None
        gk=("gold h%s %s"%(g[0],"INSIDE box" if g[1] else "outside")) if g else "gold: title not found"
        ck=("claude h%s %s"%(c[0],"INSIDE box" if c[1] else "outside")) if c else "claude: not found"
        gold[gk]+=1; claude[ck]+=1; per[code][gk]+=1
    print(code, "titles", len(titles), dict(per[code]))
print("\nGOLD:", dict(gold)); print("CLAUDE:", dict(claude))
