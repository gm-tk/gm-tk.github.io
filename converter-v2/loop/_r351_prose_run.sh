#!/usr/bin/env bash
# ROUND 351 PICK — the member-item census of every table-less / multi-table dragAndDrop bundle, 4 shards over the 297 D&D modules (WSL, from reference/tests)
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
for k in 0 1 2 3; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_measure_r351_ddprose.cjs --shard $k 4 $(cat $O/_r350_dd_modules.txt) > $O/_r351_pr_shard$k.log 2>&1 &
done; wait
node $O/_measure_r351_ddprose.cjs --merge
tail -n 1 $O/_r351_pr_shard*.log
echo "[$(date +%T)] PROSE_DONE"
