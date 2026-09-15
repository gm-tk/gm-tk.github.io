import os,re,sys,json
sys.path.insert(0, os.path.join('..','reference','tests')); import _corpus
from _discrepancy_audit import pairs, CLAUDE
dips=['MXEX401_5_0.html','HIS1005_7_0.html','MXFU401_1_0.html','TWHA905_0_0.html','TWHK903_0_0.html']
for d in dips:
    code=d.split('_')[0]
    for n,cp,hp in pairs(code):
        if os.path.basename(cp)==d:
            c=open(cp,encoding='utf-8',errors='replace').read(); h=open(hp,encoding='utf-8',errors='replace').read()
            def cnt(s): return dict(vs=s.count('videoSection'), ifr=s.count('<iframe'), btn=len(re.findall(r'class="button',s)), ext=s.count('externalButton'))
            print(d,'<->',os.path.basename(hp),'claude',cnt(c),'gold',cnt(h))
            # which youtube ids embedded in claude, present in gold as embed?
            ids=set(re.findall(r'(?:embed/|youtu\.be/|v=)([A-Za-z0-9_-]{6,})',c))
            for i in ids:
                j=h.find(i)
                seg=h[max(0,j-500):j+100] if j>=0 else ''
                print('   id',i,'gold:', 'EMBED' if ('iframe' in seg or 'videoSection' in seg) else ('BUTTON' if 'button' in seg else ('ABSENT' if j<0 else 'OTHER')))
