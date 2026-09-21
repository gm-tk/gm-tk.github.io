# score build-5 (parked) pages against the gold with the gate's own scorer, next to the live (build 7) pages
import sys, os, json
sys.path.insert(0, "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests")
os.chdir("/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests")
import _skeleton_compare as sk
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
codes = open(f"{ROOT}/CONVERTER_V2/outputs/_affected_r425.txt").read().split()
pl5, pl7 = [], []
for c in codes:
    for n in ("1_0", "2_0"):
        hp = f"{ROOT}/01-Finalized_Modules_/Standard/{c}/{c}_{n}.html"
        pl5.append((c, f"{ROOT}/CONVERTER_V2/outputs/_s31_r425_build5_output/{c}/{c}_{n}.html", hp))
        pl7.append((c, f"{ROOT}/01-Claude_Modules_/Standard/{c}/{c}_{n}.html", hp))
r5, s5 = sk._score_pairs(pl5); r7, s7 = sk._score_pairs(pl7)
m5 = {r[3]: r[0] for r in r5}; m7 = {r[3]: r[0] for r in r7}
up = down = same = 0; tot = 0.0
for k in sorted(m5):
    d = m7[k] - m5[k]; tot += d
    if d > 1e-9: up += 1
    elif d < -1e-9: down += 1
    else: same += 1
    if abs(d) > 1e-9: print(f"{k:22s} {m5[k]*100:6.2f} -> {m7[k]*100:6.2f}  {d*100:+.2f}pp")
print(f"pages up {up} / down {down} / same {same}; sum {tot*100:+.2f}pp; mean b5 {sum(m5.values())/len(m5)*100:.3f} -> b7 {sum(m7.values())/len(m7)*100:.3f}")
