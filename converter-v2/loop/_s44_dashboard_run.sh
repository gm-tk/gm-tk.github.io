#!/usr/bin/env bash
# SESSION 44 Round 3 (25 Sept 2026) — refresh the coverage dashboard on the r479 corpus (§3 step 1 / §4 widget-build lane): the r271
# variation census (the quiz types included) + the r286 decline recorder, 16 shards each, 4 at a time, then _coverage_dashboard --refresh.
# Run under WSL: bash _s44_dashboard_run.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
unset CENSUS_QUIZ_OFF
echo "[$(date +%T)] r271 census — 16 shards"
seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r271_variations.cjs --shard {} 16 > '"$O"'/_s44_var_shard{}.log 2>&1 || echo "shard {} rc=$?"'
node --require ./_deflate_raw_polyfill.cjs $O/_measure_r271_variations.cjs --merge > $O/_s44_var_merge.log 2>&1; echo "  merge rc=$?"
echo "[$(date +%T)] r286 decline recorder — 16 shards"
seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r286_declines.cjs --shard {} 16 > '"$O"'/_s44_dec_shard{}.log 2>&1 || echo "dec shard {} rc=$?"'
node --require ./_deflate_raw_polyfill.cjs $O/_measure_r286_declines.cjs --merge > $O/_s44_dec_merge.log 2>&1; echo "  merge rc=$?"
echo "[$(date +%T)] dashboard --refresh"
python3 $O/_coverage_dashboard.py --refresh > $O/_s44_dashboard.log 2>&1; echo "  rc=$?"; tail -3 $O/_s44_dashboard.log
echo "[$(date +%T)] DASH_DONE"
