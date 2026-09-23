import os, sys, glob, collections
sys.path.insert(0, os.getcwd())
from _skeleton_compare import _skel
R = os.path.normpath(os.path.join("..", "..", ".."))
d = glob.glob(os.path.join(R, "01-Claude_Modules_", "*", "ENGI405", "ENGI405_5_0.html"))[0]
o = os.path.join("..", "..", "outputs", "_r447_on", "ENGI405", "ENGI405_5_0.html")
g = glob.glob(os.path.join(R, "01-Finalized_Modules_", "*", "ENGI405", "ENGI405_5.2.html"))[0]
A, B, G = collections.Counter(_skel(d, True)), collections.Counter(_skel(o, True)), collections.Counter(_skel(g, True))
print("lines disk/on/gold:", sum(A.values()), sum(B.values()), sum(G.values()))
for k in sorted(set(A) | set(B)):
    if A[k] != B[k]: print(f"  {k!r}: disk {A[k]} on {B[k]} gold {G[k]}")
