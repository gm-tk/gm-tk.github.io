"""_r342_audio_visible.py — the link-blue [audio] class: how many literal [audio…] brackets sit in FREE-BODY visible text (outside
hand-off boxes and notes) across the corpus, per module / page — the part a tag-recognition fix could change on the page."""
import os,sys,re,collections,glob
HERE=os.path.dirname(os.path.abspath(__file__)); TESTS=os.path.normpath(os.path.join(HERE,"..","reference","tests")); sys.path.insert(0,TESTS)
import _structural_defect_audit as A
CL=os.path.normpath(os.path.join(HERE,"..","..","01-Claude_Modules_"))
RE=re.compile(r"\[\s*audio\b[^\]]{0,30}\]",re.I)
vis=collections.Counter(); vispages=set(); boxed=collections.Counter()
for f in glob.glob(os.path.join(CL,"*","*","*.html")):
    code=os.path.basename(os.path.dirname(f)); h=open(f,encoding="utf-8").read()
    body=h[h.find('id="body"'):] if 'id="body"' in h else h
    v=len(RE.findall(A.visible_text(body))); t=len(RE.findall(re.sub(r"<[^>]+>"," ",body)))
    if v: vis[code]+=v; vispages.add((code,os.path.basename(f)))
    if t-v>0: boxed[code]+=t-v
print("FREE-BODY visible [audio…] brackets:",sum(vis.values()),"on",len(vispages),"pages /",len(vis),"modules")
print("  ",sorted(vis.items(),key=lambda kv:-kv[1])[:20])
print("inside hand-off boxes / notes:",sum(boxed.values()),"brackets /",len(boxed),"modules")
