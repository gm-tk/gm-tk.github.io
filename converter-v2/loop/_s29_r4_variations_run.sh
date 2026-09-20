#!/usr/bin/env bash
# Session 29 Round 4 PICK — the r271 variation census re-run on the r412 corpus (16 shards in parallel under WSL), then merge + report.
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
echo "[$(date +%T)] shards"
for k in $(seq 0 15); do
  ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_measure_r271_variations.cjs --shard $k 16 > $O/_s29_r4_var_shard_$k.log 2>&1 ) &
done
wait
ls -la --time-style=+%H:%M $O/_r271_var_shard*.json | awk '{print $6, $7}' | sort | uniq -c | head -3
echo "[$(date +%T)] merge"
node $O/_measure_r271_variations.cjs --merge > $O/_s29_r4_var_merge.log 2>&1; tail -25 $O/_s29_r4_var_merge.log
echo "[$(date +%T)] report dragAndDrop"
node $O/_measure_r271_variations.cjs --report dragAndDrop > $O/_s29_r4_var_report_dd.log 2>&1; head -50 $O/_s29_r4_var_report_dd.log
echo "[$(date +%T)] done"
