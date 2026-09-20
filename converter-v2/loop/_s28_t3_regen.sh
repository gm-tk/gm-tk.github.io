#!/usr/bin/env bash
# SESSION 28 / TASK 3 (ROUND 410) — scoped regeneration of the probe's affected set (outputs/_s28_t3_regen_list.txt), batches of 11,
# 4 batches in parallel, batch_convert.cjs run directly with a 900 s wall (the r405 / r407 recipe). WSL, from anywhere.
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
tr -d '\r' < $O/_s28_t3_regen_list.txt | grep . > $O/_s28_t3_regen_codes.txt
split -l 11 -d $O/_s28_t3_regen_codes.txt $O/_s28_t3_regen_batch_
N=$(ls $O/_s28_t3_regen_batch_?? | wc -l)
echo "[$(date +%T)] regenerating $(wc -l < $O/_s28_t3_regen_codes.txt) modules in $N batches of 11, 4 in parallel"
run() { b=$1; STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs $(cat $O/_s28_t3_regen_batch_$b) --force > $O/_s28_t3_regen_batch_$b.log 2>&1; echo "batch $b rc=$?"; }
i=0
for f in $O/_s28_t3_regen_batch_??; do
  b=${f##*_}
  run $b &
  i=$((i+1)); if [ $((i % 4)) -eq 0 ]; then wait; fi
done
wait
echo "[$(date +%T)] REGEN_DONE"
grep -l "rc=[^0]\|Error\|ERR" $O/_s28_t3_regen_batch_??.log 2>/dev/null | head
