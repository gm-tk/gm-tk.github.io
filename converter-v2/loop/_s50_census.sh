#!/usr/bin/env bash
# Session 50 — rebuild the r271 interactive census (16 shards, 4 at a time) + merge, then the coverage dashboard --refresh.
# Run under WSL: bash _s50_census.sh TAG
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs; TAG="${1:-s50}"
echo "[$(date +%T)] r271 census — 16 shards"
seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r271_variations.cjs --shard {} 16 > '"$O"'/_'"$TAG"'_var_shard{}.log 2>&1 || echo "shard {} rc=$?"'
node --require ./_deflate_raw_polyfill.cjs $O/_measure_r271_variations.cjs --merge > $O/_${TAG}_var_merge.log 2>&1; echo "  merge rc=$?"
echo "[$(date +%T)] dashboard --refresh"
cd $O && timeout 1500 python3 _coverage_dashboard.py --refresh > _${TAG}_dash.log 2>&1; echo "  dashboard rc=$?"
echo "[$(date +%T)] done"
