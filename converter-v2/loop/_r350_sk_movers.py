import json, sys
a=json.load(open('_r349_sk_final.json'))['per_page']; b=json.load(open('_r350_sk_final.json'))['per_page']
def key(p): return p if isinstance(p,str) else p.get('page') or p.get('key')
A={k:v for k,v in a.items()} if isinstance(a,dict) else {key(p):p for p in a}
B={k:v for k,v in b.items()} if isinstance(b,dict) else {key(p):p for p in b}
def sc(v):
    if isinstance(v,dict): return v.get('scaffold', v.get('scaffold_match', v.get('sc')))
    return v
def raw(v):
    if isinstance(v,dict): return v.get('raw', v.get('raw_match'))
    return None
aff=set(l.strip() for l in open('_r350_on_changed_modules.txt') if l.strip())
mv=[]
for k in A:
    if k in B:
        x,y=sc(A[k]),sc(B[k])
        if x is not None and y is not None and abs(x-y)>1e-9: mv.append((k,x,y,y-x,raw(A[k]),raw(B[k])))
mv.sort(key=lambda t:t[3])
print('moved',len(mv),'up',sum(1 for m in mv if m[3]>0),'down',sum(1 for m in mv if m[3]<0),'scaffold pp-sum',round(sum(m[3] for m in mv)*100,2), 'raw pp-sum', round(sum((m[5] or 0)-(m[4] or 0) for m in mv)*100,2))
out=[m[0] for m in mv if m[0].split('_')[0] not in aff]
print('movers OUTSIDE the affected set:', out or 'none')
for m in mv: print(f'{m[0]:22s} {m[0].split("_")[0]:9s} {m[1]*100:6.2f} -> {m[2]*100:6.2f}  {m[3]*100:+6.2f}   raw {(m[4] or 0)*100:5.1f}->{(m[5] or 0)*100:5.1f}')
print('added',[k for k in B if k not in A],'dropped',[k for k in A if k not in B])
