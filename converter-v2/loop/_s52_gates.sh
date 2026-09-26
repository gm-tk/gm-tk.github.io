#!/usr/bin/env bash
# s52 — the gate suite + the exact skeleton means after a ship. Usage (WSL): bash _s52_gates.sh rNNN
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests || exit 1
R="$1"; O=../../outputs
echo "[$(date +%T)] gates"
bash run_all_gates.sh > $O/_${R}_gates.log 2>&1; echo "  rc=$?"
grep -E "RESULT|COUNT" $O/_${R}_gates.log | grep -v -E "✓|PASS|HANDLED" | head -10
echo "  red RESULT lines: $(grep -c 'RESULT.*✗' $O/_${R}_gates.log)   parse errors: $(grep 'pairs skipped (parse error)' $O/_${R}_gates.log | head -1)"
grep -E "TOTAL [0-9]+ \| HANDLED" $O/_${R}_gates.log | head -1
python3 _skeleton_compare.py --json /tmp/_${R}_sk.json > /dev/null 2>&1
python3 -c "import json;d=json.load(open('/tmp/_${R}_sk.json'));print('EXACT', d['pages'], round(d['scaffold_mean']*100,4), round(d['raw_mean']*100,4))"
echo "[$(date +%T)] done"
