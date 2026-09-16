#!/usr/bin/env bash
# ROUND 352 PICK — the member-item census of every clickDrop bundle, 4 shards over the clickDrop family (WSL, from reference/tests)
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
for k in 0 1 2 3; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_measure_r352_cdmembers.cjs --shard $k 4 $(cat $O/_r352_cd_modules.txt) > $O/_r352_cd_shard$k.log 2>&1 &
done; wait
node $O/_measure_r352_cdmembers.cjs --merge
tail -n 1 $O/_r352_cd_shard*.log
echo "[$(date +%T)] CD_DONE"
