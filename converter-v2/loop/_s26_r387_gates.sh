#!/usr/bin/env bash
# ROUND 387 — after the scoped regeneration: probe-vs-disk identity, the full skeleton score (json), the gate suite.
# reference/tests under WSL: bash ../../outputs/_s26_r387_gates.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] probe ON pages vs regenerated disk"
python3 - <<'PY' > $O/_s26_r387_regen_vs_probe.log 2>&1
import os, sys
sys.path.insert(0, ".")
import _corpus
from anchor_compare import CLAUDE
O = "../../outputs"; ON = os.path.join(O, "_s26_r387_on")
codes = [l.strip() for l in open(os.path.join(O, "_s26_r387_changed_modules.txt")) if l.strip()]
n = same = diff = 0
for c in codes:
    d = _corpus.mdir(CLAUDE, c)
    for f in sorted(os.listdir(d)):
        if not f.endswith(".html"): continue
        p = os.path.join(ON, c, f)
        if not os.path.exists(p): continue
        n += 1
        if open(p, "rb").read() == open(os.path.join(d, f), "rb").read(): same += 1
        else: diff += 1; print("DIFF", c, f)
print(f"probe ON vs regenerated disk over the {len(codes)} modules: pages {n} / identical {same} / differ {diff}")
PY
tail -2 $O/_s26_r387_regen_vs_probe.log
echo "[$(date +%T)] full skeleton score (json)"
python3 _skeleton_compare.py --json $O/_s26_r387_sk_final.json > $O/_s26_r387_sk_full.log 2>&1; echo "  rc=$?"; sed -n 3,12p $O/_s26_r387_sk_full.log
echo "[$(date +%T)] gate suite"
bash run_all_gates.sh > $O/_s26_r387_gates.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] GATES_DONE"
