#!/usr/bin/env bash
# SESSION 40 r449 (a copy of the s29 script; after r410 — the dashboard re-built on the post-intake corpus, LOOP_INTAKE §7 item 2) — LOOP §4 amendment: regenerate COVERAGE_DASHBOARD.md at the START of a
# build round. The r271 variation census (16 shards, 4 at a time) + its merge, the r286 all-type decline recorder (16 shards,
# 4 at a time) + its merge, then the dashboard with --refresh (the defect audit --json). Run from reference/tests under WSL.
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] r271 variation census — 16 shards"
seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r271_variations.cjs --shard {} 16 > '"$O"'/_s40_r449_var_shard{}.log 2>&1; echo "var shard {} rc=$?"'
node --require ./_deflate_raw_polyfill.cjs $O/_measure_r271_variations.cjs --merge > $O/_s40_r449_var_merge.log 2>&1; echo "  merge rc=$?"; tail -2 $O/_s40_r449_var_merge.log
echo "[$(date +%T)] r286 decline recorder — 16 shards"
seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r286_declines.cjs --shard {} 16 > '"$O"'/_s40_r449_dec_shard{}.log 2>&1; echo "dec shard {} rc=$?"'
node --require ./_deflate_raw_polyfill.cjs $O/_measure_r286_declines.cjs --merge > $O/_s40_r449_dec_merge.log 2>&1; echo "  merge rc=$?"
echo "[$(date +%T)] dashboard --refresh"
python3 $O/_coverage_dashboard.py --refresh > $O/_s40_r449_dashboard.log 2>&1; echo "  rc=$?"; tail -3 $O/_s40_r449_dashboard.log
echo "[$(date +%T)] DASH_DONE"
