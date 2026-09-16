"""_measure_r351_ddshapes.py — ROUND 351 PICK measurement (the D10-3 dragAndDrop kickoff, shape (2)+): classifies EVERY declined
dragAndDrop bundle in _r350_ddcolumn.json (the live-bundle table dump, r349/r350 corpus) into an AUTHORING shape, sized in
bundles / pages / modules and per template family + series. Diagnostic only — never imported by the engine."""
import json,re,collections,os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
recs=json.load(open(os.path.join(HERE,'_r350_ddcolumn.json'),encoding='utf-8'))
fam={}
for f in ('Standard','Bilingual','Fundamentals','Inquiry'):
    for m in os.listdir(os.path.join(ROOT,'01-Finalized_Modules_',f)): fam[m]=f
CA=re.compile(r'correct answers?',re.I); TAG=re.compile(r'^\[[^\]]+\]$')
def series(c): return re.match(r'[A-Z]+',c).group(0)
def shape(r):
    if r['nTables']==0: return 'T0 prose (no table)'
    if r['nTables']>=2: return 'T2 two+ tables'
    t=r['tables'][0]; w=r['width']; n=len(t)
    if r['extraTypes']: return 'X extraTypes'
    if r['media']: return 'M harvested media'
    cells=[c for row in t for c in row]
    anyurl=any(c['url'] for c in cells)
    hdr=t[0]; data=t[1:]
    hdr_red=any(c['red'] for c in hdr); hdr_url=any(c['url'] for c in hdr)
    data_red=any(c['red'] for row in data for c in row); data_url=any(c['url'] for row in data for c in row)
    hdr_text=[c['t'] for c in hdr]
    audio_col=any(re.search(r'audio',x,re.I) for x in hdr_text) or any(TAG.match(row[0]['t']) for row in data if row and row[0]['t'])
    if n==1: return f'W1 one-row word tiles (w={min(w,9)}{"+" if w>9 else ""})'
    if w>=3 and audio_col and data_url: return 'P phonics audio|image|answer (r342 type)'
    if anyurl:
        if w==2 and not data_red:
            cols=[sum(1 for row in data if len(row)>i and row[i]['url']) for i in range(2)]
            if cols[0]==len(data) and cols[1]==len(data): return 'I2 image|image pairs'
            return 'I2 image|word (r350 shape 1 residue: '+('hdr-url' if hdr_url else 'ragged/mixed')+')'
        if w==2: return 'I2 image|word with red data'
        return 'I3 images in a 3+ col table'
    # text-only tables
    if w==2:
        empty=sum(1 for row in data for c in row if not c['t'])
        if hdr_red and not data_red:
            return 'S2 label|answer, RED header row only'
        if data_red:
            if all(any(CA.search(x) for x in c['redRuns']) for row in data for c in row if c['red']): return 'S2 label|answer, [correct answer] marks in data'
            return 'S2 label|answer, other red in data'
        if empty: return 'S2 label|answer, empty cells'
        ans=[row[1]['t'] for row in data if len(row)>1]
        if len(set(ans))<len(ans): return 'S2 label|answer, repeated answers (categorisation)'
        return 'S2 label|answer CLEAN (why declined?)'
    # w>=3
    hdr_clean=all(c['t'] and not c['red'] for c in hdr)
    filled=sum(1 for row in data for c in row if c['t']); tot=sum(len(row) for row in data)
    if not hdr_clean:
        if hdr_red: return 'C3 no clean header (red hdr)'
        return 'C3 no clean header (empty hdr cell)'
    if data_red:
        if all(any(CA.search(x) for x in c['redRuns']) for row in data for c in row if c['red']):
            if n==2 and all(c['slashItems']>=2 for c in data[0]): return 'K3 header cats + ONE row of [correct answers] / a / b lists'
            return 'K3 header cats + [correct answer] marked cells'
        return 'C3 header cats + other red in data'
    if filled==tot: return 'G3 full grid, header + every cell filled'
    # ragged
    onecol=[sum(1 for row in data if len(row)>i and row[i]['t']) for i in range(w)]
    if sum(1 for x in onecol if x)==1: return 'A3 header cats + items pooled in ONE column'
    return 'A4 header cats + items under columns (ragged)'
agg=collections.defaultdict(lambda:{'b':0,'p':set(),'m':set(),'fam':collections.Counter(),'ser':collections.Counter(),'ex':[]})
for r in recs:
    if r['built']: continue
    s=shape(r); a=agg[s]; a['b']+=1; a['p'].add((r['code'],r['page'])); a['m'].add(r['code']); a['fam'][fam.get(r['code'],'?')]+=1; a['ser'][series(r['code'])]+=1
    if len(a['ex'])<4: a['ex'].append(f"{r['code']} p{r['page']} #{r['index']} {len(r['tables'][0]) if r['tables'] else 0}x{r['width']}")
rows=sorted(agg.items(),key=lambda kv:-kv[1]['b'])
print(f"declined dragAndDrop bundles: {sum(1 for r in recs if not r['built'])} (built {sum(1 for r in recs if r['built'])})")
print(f"{'bundles':>7} {'pages':>5} {'mods':>4}  shape")
for s,a in rows:
    print(f"{a['b']:7d} {len(a['p']):5d} {len(a['m']):4d}  {s}")
    print(f"{'':19}fam={dict(a['fam'])} series={dict(a['ser'].most_common(6))}")
    print(f"{'':19}e.g. {'; '.join(a['ex'])}")
