import os, sys
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s45_r7_emptymenu.py"), encoding="utf-8").read().split("pp = json.load")[0]
exec(src)
gm, gb = split_regions(os.path.join(_corpus.mdir(GOLD, "TEDC401"), "TEDC401-2.0.html"))
cm, cb = split_regions(os.path.join(_corpus.mdir(CL, "TEDC401"), "TEDC401_2_0.html"))
print(len(gm), repr(gm[:120]))
print(len(cm), repr(cm[:300]))
