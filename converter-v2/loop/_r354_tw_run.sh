#!/usr/bin/env bash
# ROUND 354 PICK — the invocation-tag words census over ALL 416 gated modules (4 shards, WSL, from reference/tests)
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
for k in 0 1 2 3; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_measure_r354_tagwords.cjs --shard $k 4 $(cat $O/_r342_shard_00 $O/_r342_shard_01 $O/_r342_shard_02 $O/_r342_shard_03) > $O/_r354_tw_shard$k.log 2>&1 &
done; wait
node $O/_measure_r354_tagwords.cjs --merge
for k in 0 1 2 3; do tail -n 1 $O/_r354_tw_shard$k.log; done
echo "[$(date +%T)] TW_DONE"
