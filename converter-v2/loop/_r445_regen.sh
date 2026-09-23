#!/usr/bin/env bash
# ROUND 445 (session 39 Round 7 — D13-2, the comparison table) — the scoped regeneration: the 19 affected modules + the
# 12-module spot-check sample, WITH the fix ON, one _regen_safe.sh batch per line of the _batch_plan (REGEN_TIMEOUT raised).
# Usage (WSL): bash _r445_regen.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
export REGEN_TIMEOUT=600
test -s $O/_affected_r445.txt || exit 2   # the 19 r445 codes
echo "[$(date +%T)] spot-check plan"
python3 _scoped_spotcheck.py plan --affected $O/_affected_r445.txt --n 12 --seed 445 > $O/_r445_spotcheck_plan.log 2>&1
tail -4 $O/_r445_spotcheck_plan.log
SAMPLE=$(grep -o '_batch_plan.py --codes .*' $O/_r445_spotcheck_plan.log | head -1 | sed 's/_batch_plan.py --codes //')
echo "sample: $SAMPLE"
ALL="$(cat $O/_affected_r445.txt | tr '\n' ' ') $SAMPLE"
echo "[$(date +%T)] batch plan over $(echo $ALL | wc -w) modules"
python3 _batch_plan.py --codes $ALL > $O/_r445_batch_plan.log 2>&1
grep -c '_regen_safe.sh' $O/_r445_batch_plan.log
i=0
grep -o '_regen_safe.sh .*' $O/_r445_batch_plan.log | while read -r line; do
  i=$((i+1))
  echo "[$(date +%T)] batch $i: $line" | cut -c1-160
  bash ./$line > $O/_r445_regen_batch_$i.log 2>&1
  rc=$?
  tail -2 $O/_r445_regen_batch_$i.log | cut -c1-160
  echo "   rc=$rc"
done
echo "[$(date +%T)] fresh check"
python3 _content_manifest.py fresh --affected $O/_affected_r445.txt 2>&1 | tail -4
python3 _scoped_spotcheck.py verify 2>&1 | tail -3
echo "[$(date +%T)] done"
