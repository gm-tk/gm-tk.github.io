#!/usr/bin/env bash
# SESSION 40 ROUND 8 (24 Sept 2026) — the §3 step-1 PICK: the dashboard re-built (the r271 variation census + the r286 decline recorder, 16 shards each, 4 at a time; then --refresh). Derived from _intake_2026-09-22_dashboard_run.sh. Run under WSL.
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] r271 variation census — 16 shards"
seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r271_variations.cjs --shard {} 16 > '"$O"'/_s40_r8_var_shard{}.log 2>&1; echo "var shard {} rc=$?"'
node --require ./_deflate_raw_polyfill.cjs $O/_measure_r271_variations.cjs --merge > $O/_s40_r8_var_merge.log 2>&1; echo "  merge rc=$?"; tail -2 $O/_s40_r8_var_merge.log
echo "[$(date +%T)] r286 decline recorder — 16 shards"
seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r286_declines.cjs --shard {} 16 > '"$O"'/_s40_r8_dec_shard{}.log 2>&1; echo "dec shard {} rc=$?"'
node --require ./_deflate_raw_polyfill.cjs $O/_measure_r286_declines.cjs --merge > $O/_s40_r8_dec_merge.log 2>&1; echo "  merge rc=$?"
echo "[$(date +%T)] dashboard --refresh"
python3 $O/_coverage_dashboard.py --refresh > $O/_s40_r8_dashboard.log 2>&1; echo "  rc=$?"; tail -3 $O/_s40_r8_dashboard.log
echo "[$(date +%T)] DASH_DONE"
