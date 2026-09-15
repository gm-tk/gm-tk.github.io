"""ROUND 331 — for each gold alertImage sidebar whose image file is on the paired Claude page: WHERE is that image
on the Claude page relative to the activity box of the same number (inside / the row right after / the row right
before / elsewhere)?  And the reverse precision: a Claude image sitting alone in the row right AFTER an activity box —
how often does the gold sidebar it?"""
import json,re,os,collections,sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,"..","reference","tests"))
import _corpus
from anchor_compare import CLAUDE
from _discrepancy_audit import pairs
import importlib.util
spec=importlib.util.spec_from_file_location("m", os.path.join(HERE,"_measure_r331_alertimage.py")); M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
d=json.load(open(os.path.join(HERE,"_r331_alertimage.json"),encoding="utf-8"))
def top_rows(html):
    """top-level <div class="row"> blocks of the body: [(start,end,inner)]"""
    out=[]; i=0
    while True:
        m=re.search(r'<div class="row">', html[i:])
        if not m: break
        st=i+m.start(); en=M.balanced(html,st); out.append((st,en,html[st:en])); i=en
    return out
where=collections.Counter(); rev=collections.Counter(); ex=collections.defaultdict(list)
pages={}
for r in d["rows"]:
    src=os.path.basename(r["src"]); m=re.search(r"iStock-(\d+)",src); key=m.group(1) if m else re.sub(r"\.(jpg|jpeg|png|gif|webp|svg)$","",src,flags=re.I)
    if not key: where["(no src)"]+=1; continue
    cp=os.path.join(_corpus.mdir(CLAUDE,r["code"]), r["page"])
    if cp not in pages: pages[cp]=M.body(open(cp,encoding="utf-8",errors="replace").read())
    s=pages[cp]
    if key.lower() not in s.lower(): where["absent from Claude page"]+=1; continue
    rows=top_rows(M.strip_cv2(s))
    # which top-level row holds the image, which holds the activity number
    img_i=[k for k,(a,b,inner) in enumerate(rows) if key.lower() in inner.lower()]
    act_i=[k for k,(a,b,inner) in enumerate(rows) if r["gold_num"] and re.search(r'class="[^"]*activity[^"]*"[^>]*number="%s"'%re.escape(r["gold_num"]), inner)]
    if not img_i: where["in cv2 dump"]+=1; continue
    if not act_i: where["no Claude box with that number"]+=1; continue
    ii, ai = img_i[0], act_i[0]
    if ii==ai:
        inner=rows[ai][2]
        # inside the box or a sibling in the same row?
        boxes=M.activities(inner)
        inside=any(key.lower() in b[2].lower() for b in boxes)
        where["INSIDE the box" if inside else "same row, outside the box"]+=1
        if inside and len(ex["inside"])<5: ex["inside"].append((r["code"],r["page"],r["gold_num"]))
    elif ii==ai+1: where["the row right AFTER the box"]+=1; ex["after"].append((r["code"],r["page"],r["gold_num"])) if len(ex["after"])<5 else None
    elif ii==ai-1: where["the row right BEFORE the box"]+=1; ex["before"].append((r["code"],r["page"],r["gold_num"])) if len(ex["before"])<5 else None
    else: where[f"elsewhere (distance {ii-ai:+d})" if abs(ii-ai)<=3 else "elsewhere (far)"]+=1
print("gold sidebar image — location on the Claude page relative to the same-numbered box:")
for k,v in where.most_common(): print(f"  {v:5}  {k}")
print("examples:", dict(ex))
# reverse: Claude image-only rows right after an activity row -> gold sidebar?
hit=collections.Counter()
codes=sorted(x for x in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE,x)))
gold_keys={}
for r in d["rows"]:
    src=os.path.basename(r["src"]); m=re.search(r"iStock-(\d+)",src); key=(m.group(1) if m else re.sub(r"\.(jpg|jpeg|png|gif|webp|svg)$","",src,flags=re.I)).lower()
    gold_keys.setdefault((r["code"],r["page"]),set()).add(key)
for code in codes:
    tmpl=os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE,code)))
    for n,cp,hp in pairs(code):
        if re.search(r'acks|glossary',os.path.basename(hp),re.I): continue
        s=M.strip_cv2(M.body(open(cp,encoding="utf-8",errors="replace").read()))
        rows=top_rows(s)
        for k in range(1,len(rows)):
            inner=rows[k][2]; prev=rows[k-1][2]
            if re.search(r'class="[^"]*activity[^"]*"',prev) and re.search(r"<img\b",inner) and not re.search(r"<(p|h[1-6]|ul|ol|table|iframe)\b", re.sub(r"<p[^>]*class=\"cv2-note\"[^>]*>.*?</p>","",inner,flags=re.S)):
                srcs=re.findall(r'src="([^"]*)"',inner); keys=[ (re.search(r"iStock-(\d+)",x).group(1) if re.search(r"iStock-(\d+)",x) else re.sub(r"\.(jpg|jpeg|png|gif|webp|svg)$","",os.path.basename(x),flags=re.I)).lower() for x in srcs]
                g=gold_keys.get((code,os.path.basename(cp)),set())
                hit[(tmpl, "gold SIDEBAR (same image)" if any(x in g for x in keys) else "gold no sidebar")]+=1
print("\nREVERSE: a Claude image-only row right AFTER an activity row → gold sidebar with that image?")
for k,v in sorted(hit.items()): print(f"  {v:5}  {k}")
