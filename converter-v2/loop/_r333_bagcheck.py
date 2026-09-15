"""ROUND 333 — position-independent line overlap (bag intersection with the gold skeleton) OFF vs ON on the dip pages.
OFF pages come from the ALERTRHS_OFF in-memory probe (--save _r333_off_pages)."""
import sys, os, collections
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,"..","reference","tests"))
import _skeleton_compare as S
from _discrepancy_audit import pairs
OFF=os.path.join(HERE,"_r333_off_pages")
DIPS=[("TEFUN05","TEFUN05_0_0.html"),("ANZH304","ANZH304_6_0.html"),("TEFUN04","TEFUN04_0_0.html"),("MXFL301","MXFL301_1_0.html"),
      ("ANZH303","ANZH303_6_0.html"),("ANZH203","ANZH203_4_0.html"),("MXEX302","MXEX302_6_0.html"),("ENGI102","ENGI102_6_0.html")]
for code, page in DIPS:
    for n, cp, hp in pairs(code):
        if os.path.basename(cp)!=page: continue
        offp=os.path.join(OFF, code, page)
        if not os.path.exists(offp): print(code,page,"no OFF page"); continue
        _, a_on, b = S.match(cp, hp, scaffold=True); _, a_off, _ = S.match(offp, hp, scaffold=True)
        B=collections.Counter(l.strip() for l in b)
        def bag(a):
            A=collections.Counter(l.strip() for l in a); return sum((A&B).values()), len(a)
        (on_i,on_n),(off_i,off_n)=bag(a_on),bag(a_off)
        import difflib
        def score(a): return difflib.SequenceMatcher(None,b,a).ratio()
        print(f"{page}: gate OFF {score(a_off)*100:.2f} -> ON {score(a_on)*100:.2f} | bag overlap OFF {off_i}/{off_n} -> ON {on_i}/{on_n} | gold lines {len(b)}")
