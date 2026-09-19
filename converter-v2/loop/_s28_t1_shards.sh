#!/usr/bin/env bash
# Session 28 / Task 1 — the label-independent shard builds over the 552-dir gold corpus, in parallel.
#   granular registry: 8 shards (build_granular_registry.py --shard K 8)  -> outputs/_granreg_shard_Kof8.json
#   feature index:     16 shards (build_feature_index.cjs --shard K 16)   -> outputs/_feature_index_shardK.json
# Run under WSL from anywhere: bash _s28_t1_shards.sh ; logs in outputs/_s28_t1_shard_*.log
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
echo "[$(date +%T)] granular shards 0..7 + feature-index shards 0..15 starting"
for K in 0 1 2 3 4 5 6 7; do
  ( python3 build_granular_registry.py --shard $K 8 > $O/_s28_t1_shard_gran_$K.log 2>&1; echo "gran $K rc=$?" ) &
done
for K in $(seq 0 15); do
  ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --shard $K 16 > $O/_s28_t1_shard_feat_$K.log 2>&1; echo "feat $K rc=$?" ) &
done
wait
echo "[$(date +%T)] SHARDS_DONE"
ls $O/_granreg_shard_*of8.json | wc -l
ls $O/_feature_index_shard*.json | wc -l
