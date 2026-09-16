#!/usr/bin/env bash
# ROUND 352 PICK — the member-item census of every selfCheck bundle, 4 shards (WSL, from reference/tests)
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
for k in 0 1 2 3; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_measure_r352_scmembers.cjs --shard $k 4 $(cat $O/_r352_sc_modules.txt) > $O/_r352_sc_shard$k.log 2>&1 &
done; wait
node $O/_measure_r352_scmembers.cjs --merge
tail -n 1 $O/_r352_sc_shard*.log
echo "[$(date +%T)] SC_DONE"
