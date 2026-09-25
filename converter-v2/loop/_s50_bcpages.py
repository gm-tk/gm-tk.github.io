"""_s50_bcpages.py — session 50: for each named Claude page, every hand-off box body_compare sees
(its banner, its member chars; EMPTY when < 40) and the free-block count. Run under WSL from reference/tests/:
  python3 ../../outputs/_s50_bcpages.py ANZH301/ANZH301_4_0.html [DIR=override claude root]"""
import os, sys
sys.path.insert(0, os.getcwd())
import body_compare as bc, _corpus
root = os.environ.get("CLROOT")
for a in sys.argv[1:]:
    mod, f = a.split("/")
    p = os.path.join(root, mod, f) if root else os.path.join(_corpus.mdir(bc.CLAUDE, mod), f)
    cp = bc.parse(p)
    tot = max(1, cp.all_chars)
    print(f"== {a}  all_chars={cp.all_chars} free_blocks={len(cp.free_blocks)}")
    for k, v in cp.cv2_text.items():
        print(f"   {'EMPTY ' if v < 40 else '      '}{v:6d} ({100*v/tot:4.0f}%)  {cp.cv2_banner.get(k, '')[:110]}")
