"""_measure_r342_blacktags.py — session-9 PICK measurement: writer [tags] typed in a NON-RED colour.
The engine scans only red runs (Input_Doc_Rules.red_runs.red_hex_values = ff0000/ee0000) for tags; a tag in any other
colour is invisible to TagNormaliser and ships as literal text (the protected literal-tag-leak gate: 288/46).
Over every Writers Template docx: every bracket group whose content folds to a Tag_Lexicon alias (approximation of
TagNormaliser: lowercase, numbering stripped, whitespace collapsed; exact alias OR first-token alias for the structural
families) is tallied by the colour of the run holding its '[' — red / near-red (hue red, not in the list) / black / other —
and by position (paragraph-leading vs mid-paragraph). Output: per-module rows + corpus totals, JSON + log."""
import os, re, sys, json, zipfile, glob, collections
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
GOLD=os.path.join(ROOT,"01-Finalized_Modules_"); CLAUDE=os.path.join(ROOT,"01-Claude_Modules_")
DATA=os.path.join(ROOT,"pageforge-site","converter-v2","data")
lex=json.load(open(os.path.join(DATA,"Tag_Lexicon.json"),encoding="utf-8"))
rules=json.load(open(os.path.join(DATA,"Input_Doc_Rules.json"),encoding="utf-8"))
RED=set(x.lower() for x in rules["red_runs"]["red_hex_values"])
aliases={}
for canon,ent in lex["tags"].items():
    for a in [canon]+list(ent.get("aliases",[])):
        aliases[re.sub(r"\s+"," ",a.lower()).strip()]=canon
NUM=re.compile(r"\s*#?\d+(?:\.\d+)*[a-z]?\b\s*")
def fold(s):
    s=s.lower().replace("_"," "); s=NUM.sub(" ",s); s=re.sub(r"[^a-z0-9/ :\-]"," ",s); return re.sub(r"\s+"," ",s).strip()
def tag_of(inner):
    f=fold(inner)
    if not f: return None
    if f in aliases: return aliases[f]
    # "[H3] text" typed inline: the bracket holds only the tag, so f is the tag — handled above. For "[Activity Individual]",
    # "[Body text continued]" etc. try progressively shorter prefixes (longest first)
    toks=f.split(" ")
    for n in range(len(toks),0,-1):
        p=" ".join(toks[:n])
        if p in aliases: return aliases[p]
    m=re.match(r"^(h[1-6])\b",f)
    return m.group(1) if m else None
def hue_red(hexv):
    try: r,g,b=int(hexv[0:2],16),int(hexv[2:4],16),int(hexv[4:6],16)
    except Exception: return False
    return r>=0xB0 and g<=0x40 and b<=0x40
def runs_of(para):
    out=[]
    for m in re.finditer(r"<w:r\b[\s\S]*?</w:r>",para):
        r=m.group(0)
        col=re.search(r'<w:color w:val="([0-9A-Fa-f]{6})"',r); col=(col.group(1).lower() if col else "auto")
        t="".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>",r))
        t=t.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").replace("&quot;",'"').replace("&apos;","'")
        if "<w:br" in r: t="\n"+t if r.find("<w:br")<r.find("<w:t") else t+"\n"
        out.append((col,t))
    return out
mods=sorted(set(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(GOLD,"*","*","*.docx"))))
claude_dirs=set(os.path.basename(p) for p in glob.glob(os.path.join(CLAUDE,"*","*")) if os.path.isdir(p))
rows=[]; tot=collections.Counter(); colours=collections.Counter(); tagc=collections.Counter(); nonred_tags=collections.Counter()
for code in mods:
    wts=[p for p in glob.glob(os.path.join(GOLD,"*",code,"*.docx")) if re.search(r"writers template",os.path.basename(p),re.I)]
    if not wts: continue
    wt=sorted(wts)[0]
    try: x=zipfile.ZipFile(wt).read("word/document.xml").decode("utf-8")
    except Exception as e: print("ERR",code,e); continue
    c=collections.Counter(); cols=collections.Counter(); ex=[]
    for pm in re.finditer(r"<w:p\b[\s\S]*?</w:p>",x):
        rs=runs_of(pm.group(0))
        if not rs: continue
        text="".join(t for _,t in rs)
        # map char offsets to run colours
        spans=[]; pos=0
        for col,t in rs: spans.append((pos,pos+len(t),col)); pos+=len(t)
        for bm in re.finditer(r"\[([^\[\]\n]{1,80})\]",text):
            tg=tag_of(bm.group(1))
            if not tg: continue
            col=next((cc for a,b,cc in spans if a<=bm.start()<b),"auto")
            lead = text[:bm.start()].strip()=="" or text[:bm.start()].rstrip().endswith("\n")
            kind="red" if col in RED else ("nearred" if hue_red(col) else ("black" if col in ("auto","000000","0f0f0f","1a1a1a","212121","262626") else "other"))
            c[kind]+=1; c[kind+"_"+("lead" if lead else "mid")]+=1
            if kind!="red":
                cols[col]+=1; nonred_tags[tg]+=1
                if len(ex)<6: ex.append(f"{col}:{'L' if lead else 'M'}:{bm.group(0)[:40]}")
            tagc[(kind,tg)]+=1
    nonred=c["nearred"]+c["black"]+c["other"]
    rows.append(dict(code=code,tmpl=os.path.basename(os.path.dirname(os.path.dirname(wt))),claude=code in claude_dirs,red=c["red"],nearred=c["nearred"],black=c["black"],other=c["other"],
                     nonred_lead=c["nearred_lead"]+c["black_lead"]+c["other_lead"],nonred_mid=c["nearred_mid"]+c["black_mid"]+c["other_mid"],colours=dict(cols),examples=ex))
    for k,v in c.items(): tot[k]+=v
    for k,v in cols.items(): colours[k]+=v
json.dump(dict(rows=rows,totals=dict(tot),colours=dict(colours),nonred_tags=dict(nonred_tags)),open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"_r342_blacktags.json"),"w"),indent=1)
print("WT modules scanned:",len(rows),"| tag brackets: red",tot["red"],"| near-red",tot["nearred"],"| black",tot["black"],"| other",tot["other"])
print("non-red by position: leading",tot["nearred_lead"]+tot["black_lead"]+tot["other_lead"],"mid",tot["nearred_mid"]+tot["black_mid"]+tot["other_mid"])
print("\nnon-red colours:"); [print("  %5d  %s"%(v,k)) for k,v in colours.most_common(20)]
print("\nnon-red tags (canon):"); [print("  %5d  %s"%(v,k)) for k,v in nonred_tags.most_common(25)]
aff=[r for r in rows if r["nearred"]+r["black"]+r["other"]>0]
print("\nmodules with >=1 non-red tag:",len(aff),"(Claude dirs:",sum(1 for r in aff if r["claude"]),")  >=5:",sum(1 for r in aff if r["nearred"]+r["black"]+r["other"]>=5),"(Claude:",sum(1 for r in aff if r["claude"] and r["nearred"]+r["black"]+r["other"]>=5),")")
print("per template (modules with >=1 / >=5 non-red):")
for t in sorted(set(r["tmpl"] for r in rows)):
    rr=[r for r in rows if r["tmpl"]==t]; print("  %-13s %3d WTs | >=1: %3d | >=5: %3d | non-red brackets %5d | red %6d"%(t,len(rr),sum(1 for r in rr if r["nearred"]+r["black"]+r["other"]>0),sum(1 for r in rr if r["nearred"]+r["black"]+r["other"]>=5),sum(r["nearred"]+r["black"]+r["other"] for r in rr),sum(r["red"] for r in rr)))
print("\ntop modules by non-red tags:")
for r in sorted(aff,key=lambda r:-(r["nearred"]+r["black"]+r["other"]))[:40]:
    print("  %-9s %-12s claude=%s red=%4d nearred=%3d black=%3d other=%3d lead=%3d mid=%3d %s | %s"%(r["code"],r["tmpl"],"Y" if r["claude"] else "n",r["red"],r["nearred"],r["black"],r["other"],r["nonred_lead"],r["nonred_mid"],dict(sorted(r["colours"].items(),key=lambda kv:-kv[1])[:3]),"; ".join(r["examples"][:3])))
