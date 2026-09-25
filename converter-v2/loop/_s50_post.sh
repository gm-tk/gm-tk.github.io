#!/usr/bin/env bash
# Session 50 — the post-finalise chain of a SCOPED round (under WSL): --gate-baseline-check, the feature index (--rehtml,
# --merge, --selftest), the DIFF MINER. Usage: bash _s50_post.sh N
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs; N="$1"
echo "[$(date +%T)] gate-baseline-check"
python3 _fastloop_diff.py --gate-baseline-check 2>&1 | tail -2
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_r${N}_index.log 2>&1; echo "  rc=$?"; tail -1 $O/_r${N}_index.log
echo "[$(date +%T)] DIFF MINER"
python3 _diff_miner.py > $O/_diff_miner_r${N}.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_r${N}.log | cut -c1-200
echo "[$(date +%T)] POST_DONE"
