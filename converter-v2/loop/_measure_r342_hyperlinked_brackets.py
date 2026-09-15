"""_measure_r342_hyperlinked_brackets.py — every run INSIDE a w:hyperlink whose text carries a bracket group, over all Writers
Templates, tallied by the bracket's first word and by run colour; plus the hyperlink target host. The safety side of the
'a hyperlinked bracket run is a tag' rule: which bracket heads occur, and are any of them content (footnote-style [1] links…)?"""
import os,re,glob,zipfile,collections
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
GOLD=os.path.join(ROOT,"01-Finalized_Modules_"); CL=os.path.join(ROOT,"01-Claude_Modules_")
gated=set(os.path.basename(p) for p in glob.glob(os.path.join(CL,"*","*")) if os.path.isdir(p))
heads=collections.Counter(); cols=collections.Counter(); hosts=collections.Counter(); mods=collections.defaultdict(collections.Counter); ex={}
for wt in sorted(glob.glob(os.path.join(GOLD,"*","*","*.docx"))):
    if not re.search(r"writers template",os.path.basename(wt),re.I): continue
    code=os.path.basename(os.path.dirname(wt))
    try:
        z=zipfile.ZipFile(wt); x=z.read("word/document.xml").decode("utf-8"); rels=z.read("word/_rels/document.xml.rels").decode("utf-8")
    except Exception: continue
    rmap=dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',rels))
    for hm in re.finditer(r'<w:hyperlink\b([^>]*)>([\s\S]*?)</w:hyperlink>',x):
        rid=re.search(r'r:id="([^"]+)"',hm.group(1)); tgt=rmap.get(rid.group(1),"") if rid else ""
        for rm in re.finditer(r"<w:r\b[\s\S]*?</w:r>",hm.group(2)):
            run=rm.group(0); col=re.search(r'<w:color w:val="([0-9A-Fa-f]{6})"',run); col=col.group(1).lower() if col else "auto"
            t="".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>",run))
            for bm in re.finditer(r"\[([^\[\]\n]{1,80})\]",t):
                head=re.sub(r"[^a-z ]"," ",bm.group(1).lower()).split()
                head=head[0] if head else "(digits/empty)"
                heads[head]+=1; cols[col]+=1; hosts[re.sub(r"^https?://([^/]+).*$",r"\1",tgt) or "(none)"]+=1
                if code in gated: mods[head][code]+=1
                ex.setdefault(head,(code,bm.group(0)[:40],col))
print("hyperlinked bracket runs:",sum(heads.values()))
print("by first word:");[print("  %4d  %-18s e.g. %s"%(v,k,ex[k])) for k,v in heads.most_common(30)]
print("by run colour:",cols.most_common(8))
print("by target host:",hosts.most_common(8))
print("gated modules per head (top):",{k:len(v) for k,v in mods.items()})
