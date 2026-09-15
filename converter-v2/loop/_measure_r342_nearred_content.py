"""_measure_r342_nearred_content.py — the RISK side of the near-red class: for every run in a near-red colour (hue red,
not ff0000/ee0000), is the run's paragraph a TAG line (starts with a bracket / holds only brackets + instruction) or is
it CONTENT the writer merely coloured? Per colour + per module: paragraphs whose near-red text holds a '[' vs not, with
samples of the no-bracket ones (those would become red-text instructions under a near-red rule)."""
import os,re,json,zipfile,glob,collections
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
GOLD=os.path.join(ROOT,"01-Finalized_Modules_")
RED={"ff0000","ee0000"}
def hue_red(h):
    try: r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    except Exception: return False
    return r>=0xB0 and g<=0x40 and b<=0x40
percol=collections.defaultdict(collections.Counter); permod=collections.defaultdict(collections.Counter); samples=collections.defaultdict(list)
for wt in sorted(glob.glob(os.path.join(GOLD,"*","*","*.docx"))):
    if not re.search(r"writers template",os.path.basename(wt),re.I): continue
    code=os.path.basename(os.path.dirname(wt))
    try: x=zipfile.ZipFile(wt).read("word/document.xml").decode("utf-8")
    except Exception: continue
    for pm in re.finditer(r"<w:p\b[\s\S]*?</w:p>",x):
        para=pm.group(0); nr=collections.defaultdict(str); allt=""
        for m in re.finditer(r"<w:r\b[\s\S]*?</w:r>",para):
            r=m.group(0); col=re.search(r'<w:color w:val="([0-9A-Fa-f]{6})"',r); col=col.group(1).lower() if col else "auto"
            t="".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>",r)); allt+=t
            if col not in RED and hue_red(col): nr[col]+=t
        for col,t in nr.items():
            if not t.strip(): continue
            kind="bracket" if "[" in t or "]" in t else "nobracket"
            percol[col][kind]+=1; permod[code][col+":"+kind]+=1
            if kind=="nobracket" and len(samples[(code,col)])<3: samples[(code,col)].append(re.sub(r"\s+"," ",t)[:90])
print("per colour (paragraphs with near-red text): bracket vs no-bracket")
for col,c in sorted(percol.items(),key=lambda kv:-sum(kv[1].values())): print("  %s  bracket %4d  nobracket %4d"%(col,c["bracket"],c["nobracket"]))
print("\nper module (any near-red):")
for code,c in sorted(permod.items(),key=lambda kv:-sum(kv[1].values())):
    nb=sum(v for k,v in c.items() if k.endswith("nobracket")); br=sum(v for k,v in c.items() if k.endswith("bracket") and not k.endswith("nobracket"))
    print("  %-9s bracket %3d  nobracket %3d  %s"%(code,br,nb,dict(c)))
    for (cd,col),ss in samples.items():
        if cd==code:
            for s in ss: print("       %s: %r"%(col,s))
